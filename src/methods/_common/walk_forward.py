"""WF-1A: the walk-forward driver's logic (releases and WF-1 design v0.1r1 section 5; owner-ratified 31 October 2026).

Orchestration only: it imports no method code (the caller passes the runner's ADAPTERS) and no evaluation code,
and it reads no draw. It reads the installed registry, the method folders' development flags, and one line of
the game's master ledger (the version-1 INIT line, for the master pin). Every run is one ordinary standalone
contract run through the unchanged `run_contract_method`, so every refusal of the runner, the dispatch gate and
the reader applies unchanged. The STOP rule (design 5.3, EX_078 WF1-R3-B01) classifies each run by its terminal
reason and fails closed. Nothing here deletes, moves, rewrites, retries automatically, kills or recovers anything.

The roots are fixed: they derive, at call time, from the runner's PROJECT_ROOT constant, which no caller can
choose (a test harness patches it in-process, as the existing tests do):
  <project>/results/real/development/wf_batches/<GAME>/<batch_id>/   plan.json, segment_*.json
  <project>/results/real/development/contract_runs/                   the runs (the runner's real run root)
  <project>/results/audit/SEARCH_LOG.csv                              one WF_BATCH row per plan (R3 7.4)
"""
from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import uuid

import _common.contract_dispatch as CD
import _common.contract_publication as CP
import _common.contract_registry as REG
import _common.contract_runner as CR
import _common.contract_vocab as V
from _common.contract_dispatch import DispatchRefused
from _common.contract_receipts import consumable, validate_terminal
from _common.contract_records import canonical, record_digest, sha256_hex
from _common.contract_registry import InstalledRegistry
from _common.game_draws_reader import _trusted_file_bytes
from _common.game_profiles import get_profile

DRIVER_VERSION = 'WF1A_DRIVER_V1'
PLAN_SCHEMA = 'WF_BATCH_PLAN_V1'
SEGMENT_SCHEMA = 'WF_BATCH_SEGMENT_V1'
BATCH_ID = re.compile(r'wf-[0-9a-f]{32}\Z', re.ASCII)
VIEW = 'UNORDERED_SET'
SEARCH_LOG_HEADER = ('row_type', 'utc', 'game_id', 'mode', 'window_first', 'window_last', 'cohort_size',
                     'cohort_digest', 'family_ids', 'test_count', 'measures', 'batch_id', 'attempt_id',
                     'plan_digest', 'tool', 'tool_version', 'tool_sha256')

# Released methods that cannot run on real data through the contract, with the reason. They are listed in every
# plan as not in the cohort, never silently dropped (mark, never suppress).
NOT_REAL_CAPABLE = {'E_1': ("E_1 revision 1's multi-game function accepts synthetic contract data only (E2RC-C04 "
                            "option (a)); E_1 joins walk-forward batches as revision 2 (owner decision WF1-13)")}

# The STOP rule (design 5.3): only these (outcome, reason prefix) pairs continue; everything else stops.
CONTINUE = frozenset({('SUCCESS', 'PUBLISHED'), ('RUNTIME_FAILURE', 'METHOD_FAILED'),
                      ('NUMERIC_INVALID', 'METHOD_FAILED'), ('VALIDATION_FAILURE', 'CONTRACT_REFUSED_OUTPUT'),
                      ('NUMERIC_INVALID', 'CONTRACT_REFUSED_OUTPUT'),
                      ('VALIDATION_FAILURE', CP.NO_TICKET_NO_DIAGNOSTIC)})


class BatchRefused(Exception):
    """Refused before any run (and, at plan time, before anything is written)."""


def roots() -> dict:
    project = Path(CR.PROJECT_ROOT)
    dev = project / 'results' / 'real' / 'development'
    return {'project': project, 'batches': dev / 'wf_batches', 'runs': dev / 'contract_runs',
            'search_log': project / 'results' / 'audit' / 'SEARCH_LOG.csv'}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def tool_sha256() -> str:
    """SHA-256 of this module's source, line endings normalised to LF (the Git content)."""
    return sha256_hex(Path(__file__).read_bytes().replace(b'\r\n', b'\n'))


def reason_prefix(reason: str) -> str:
    return reason.split(':', 1)[0] if isinstance(reason, str) else ''


def classify(outcome: str, reason: str) -> str:
    """'CONTINUE' only for the listed (outcome, reason prefix) pairs; 'STOP' for anything else (fail closed)."""
    if isinstance(reason, str) and ':' in reason and (outcome, reason_prefix(reason)) in CONTINUE:
        return 'CONTINUE'
    return 'STOP'


def _marker_present() -> bool:
    m = Path(CR.ORPHAN_MARKER)
    return m.exists() or m.is_symlink()


def ledger_pin(game_id: str) -> str:
    """The master SHA-256 from the game's version-1 INIT ledger line (the same shape the reader requires).
    Reads only the ledger file, through the reader's trusted-file helper."""
    p = get_profile(game_id)
    raw = _trusted_file_bytes(roots()['project'] / 'source_data' / f'{game_id}_results_master_ledger.csv')
    rows = list(csv.DictReader(io.StringIO(raw.decode('ascii'))))
    if (len(rows) != 1 or rows[0].get('version') != '1' or rows[0].get('action') != 'INIT' or
            rows[0].get('first_draw') != str(p.first_draw) or rows[0].get('last_draw') != str(p.holdout_first - 1) or
            rows[0].get('draw_count') != str(p.holdout_first - p.first_draw) or
            not V.SHA256.fullmatch(rows[0].get('master_sha256') or '')):
        raise BatchRefused(f'{game_id}: the master ledger is not the version-1 INIT line the reader requires')
    return rows[0]['master_sha256']


def _registry() -> InstalledRegistry:
    """The installed registry at its fixed location, read at call time (as the dispatch gate does)."""
    return InstalledRegistry(Path(REG.DATA_ROOT))


def _flag(method_id: str) -> Path:
    return Path(CD.METHODS_ROOT) / CD.method_folder(method_id) / CD.FLAG_NAME


def cohort(game_id: str, adapters: Mapping) -> list[dict]:
    """Every (method, variant) with an active SUPPORTED entry for the game, no development flag, and an adapter,
    in method-number then variant order (design 5.2, O01). A SUPPORTED entry whose flag is present is refused.
    Returns (members, excluded): released variants that cannot run on real data (NOT_REAL_CAPABLE) are listed with
    their reason, not run."""
    reg = _registry()
    members, inconsistent, excluded = [], [], []
    for (g, m, v) in sorted(reg.chain_keys(), key=lambda k: (int(k[1][2:]), k[2])):
        if g != game_id:
            continue
        e = reg.active_entry(g, m, v)
        if e['registry_status'] != 'SUPPORTED':
            continue
        if _flag(m).exists():
            inconsistent.append(f'{m} {v}')
            continue
        if m not in adapters:
            continue
        if m in NOT_REAL_CAPABLE:
            excluded.append({'method_id': m, 'variant_id': v, 'reason': NOT_REAL_CAPABLE[m]})
            continue
        d = reg.declaration(e['declaration_digest'])
        if VIEW not in d['observation_views'] or d['uses_dates']:
            raise BatchRefused(f'{m} {v}: the driver runs unordered, date-free views only')
        members.append({'method_id': m, 'variant_id': v, 'method_revision': e['method_revision'],
                        'declaration_digest': e['declaration_digest'], 'registry_entry_digest': record_digest(e),
                        'minimum_history_draws': d['minimum_history_draws']})
    if inconsistent:
        raise BatchRefused('SUPPORTED but still flagged IN_DEVELOPMENT (inconsistent installed state): ' +
                           ', '.join(inconsistent))
    return members, excluded


def _append_search_row(row: Mapping) -> int:
    """Append one row; create the file with its header if absent. Returns the new row's number (1 = first)."""
    path = roots()['search_log']
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        buf = io.StringIO()
        csv.writer(buf, lineterminator='\n').writerow(SEARCH_LOG_HEADER)
        CP.create_only(path, buf.getvalue().encode('ascii'))
    old = path.read_bytes()
    lines = old.decode('ascii').splitlines()
    if not lines or lines[0] != ','.join(SEARCH_LOG_HEADER) or not old.endswith(b'\n'):
        raise BatchRefused('the search log exists but its header or ending is not the expected one; nothing appended')
    buf = io.StringIO()
    csv.writer(buf, lineterminator='\n').writerow([row.get(k, '') for k in SEARCH_LOG_HEADER])
    with open(path, 'ab') as fh:
        fh.write(buf.getvalue().encode('ascii'))
        fh.flush()
        os.fsync(fh.fileno())
    return len(lines)


def make_plan(game_id: str, first: int, last: int, adapters: Mapping) -> dict:
    """Design 5.2: check, freeze the plan (create-only), append one WF_BATCH search-log row."""
    p = get_profile(game_id)
    if _marker_present():
        raise BatchRefused('UNRESOLVED_ORPHAN_MARKER: no experiment is permitted')
    if type(first) is not int or type(last) is not int or first > last:
        raise BatchRefused('the window must be two whole draw numbers, first <= last')
    if first < p.first_draw + 1:
        raise BatchRefused(f'first must be at least {p.first_draw + 1}: the era\'s first draw has no history')
    if last >= p.holdout_first:
        raise BatchRefused(f'last must be below the holdout\'s first draw, {p.holdout_first}')
    members, excluded = cohort(game_id, adapters)
    if not members:
        raise BatchRefused('the cohort is empty: no released variant with a runner adapter')
    pin = ledger_pin(game_id)
    batch_id = 'wf-' + uuid.uuid4().hex
    plan = {'schema': PLAN_SCHEMA, 'batch_id': batch_id, 'game_id': game_id, 'profile_version': p.version,
            'window_first': first, 'window_last': last, 'created_utc': utc_now(), 'driver_version': DRIVER_VERSION,
            'run_mode': 'REAL_DEVELOPMENT', 'product_kind': V.producible('REAL_DEVELOPMENT', V.FORECAST)[0],
            'observation_view': VIEW, 'include_dates': False, 'master_file': f'{game_id}_results_master.csv',
            'ledger_version': 1, 'master_sha256': pin, 'cohort': members, 'not_in_cohort': excluded,
            'cohort_digest': sha256_hex(canonical({'cohort': members}))}
    folder = roots()['batches'] / game_id / batch_id
    folder.mkdir(parents=True, exist_ok=False)
    CP.create_only(folder / 'plan.json', canonical(plan))
    _append_search_row({'row_type': 'WF_BATCH', 'utc': plan['created_utc'], 'game_id': game_id, 'mode': 'WF',
                        'window_first': first, 'window_last': last, 'cohort_size': len(members),
                        'cohort_digest': plan['cohort_digest'], 'batch_id': batch_id,
                        'plan_digest': record_digest(plan), 'tool': 'Method_Walk_Forward.py',
                        'tool_version': DRIVER_VERSION, 'tool_sha256': tool_sha256()})
    return plan


def load_plan(game_id: str, batch_id: str) -> dict:
    if not isinstance(batch_id, str) or not BATCH_ID.fullmatch(batch_id):
        raise BatchRefused('invalid batch ID')
    get_profile(game_id)
    path = roots()['batches'] / game_id / batch_id / 'plan.json'
    if not path.is_file() or path.is_symlink():
        raise BatchRefused(f'no plan for batch {batch_id} in {game_id}')
    plan = json.loads(path.read_bytes().decode('ascii'))
    if (plan.get('schema') != PLAN_SCHEMA or plan.get('batch_id') != batch_id or plan.get('game_id') != game_id or
            canonical(plan) != path.read_bytes() or
            plan.get('cohort_digest') != sha256_hex(canonical({'cohort': plan.get('cohort')}))):
        raise BatchRefused('the plan file is not a valid, unaltered WF_BATCH_PLAN_V1')
    if record_digest(plan) not in _logged_plan_digests(batch_id):
        raise BatchRefused('the plan does not match its WF_BATCH search-log row (altered after it was made?)')
    return plan


def _logged_plan_digests(batch_id: str) -> set:
    path = roots()['search_log']
    if not path.is_file() or path.is_symlink():
        return set()
    rows = list(csv.DictReader(io.StringIO(path.read_bytes().decode('ascii'))))
    return {r.get('plan_digest') for r in rows if r.get('row_type') == 'WF_BATCH' and r.get('batch_id') == batch_id}


def start_checks(plan: Mapping, adapters: Mapping) -> None:
    """Design 5.3, at the start of every run invocation: registry and flag reads only, before any run."""
    if _marker_present():
        raise BatchRefused('UNRESOLVED_ORPHAN_MARKER: no experiment is permitted')
    reg = _registry()
    for mem in plan['cohort']:
        ident = f"{mem['method_id']} {mem['variant_id']}"
        try:
            e = reg.active_entry(plan['game_id'], mem['method_id'], mem['variant_id'])
        except ValueError:
            raise BatchRefused(f'{ident}: no installed registry chain') from None
        if (record_digest(e) != mem['registry_entry_digest'] or e['declaration_digest'] != mem['declaration_digest'] or
                e['method_revision'] != mem['method_revision'] or e['registry_status'] != 'SUPPORTED'):
            raise BatchRefused(f'{ident}: the installed registry no longer matches the plan')
        if _flag(mem['method_id']).exists():
            raise BatchRefused(f'{ident}: an IN_DEVELOPMENT flag is present')
        if mem['method_id'] not in adapters:
            raise BatchRefused(f'{ident}: no runner adapter')


def request_for(plan: Mapping, mem: Mapping, target: int, run_id: str) -> dict:
    """The exact RUN_REQUEST_V1 this plan issues for one pair and one attempt (run ID)."""
    return {'schema': V.RUN_REQUEST, 'game_id': plan['game_id'], 'method_id': mem['method_id'],
            'variant_id': mem['variant_id'], 'method_revision': mem['method_revision'], 'target_draw_number': target,
            'observation_view': plan['observation_view'], 'include_dates': plan['include_dates'],
            'run_mode': plan['run_mode'], 'product_kind': plan['product_kind'],
            'declaration_digest': mem['declaration_digest'], 'registry_entry_digest': mem['registry_entry_digest'],
            'run_id': run_id, 'master_file': plan['master_file'], 'ledger_version': plan['ledger_version'],
            'master_sha256': plan['master_sha256']}


# ---------------------------------------------------------------- attempts bound to the batch (EX_083 WF1A-R2-B01)
#
# Before each run, the driver appends one WF_BATCH_ATTEMPT_V1 line to the batch's attempts.jsonl, naming the fresh
# run ID and the digest of the exact request it is about to issue. A pair counts as done only through an attempt of
# THIS batch whose run folder holds a valid terminal record matching that request, in a CONTINUE class, and, for a
# SUCCESS, a consumable forecast whose receipt and record carry this plan's master pin, run mode, view, declaration
# and registry entry. Runs of any other batch, folders without an attempt line, and anything that fails a check are
# never counted: the pair runs again. Nothing is deleted or rewritten.

ATTEMPT_SCHEMA = 'WF_BATCH_ATTEMPT_V1'


def _attempts_path(plan: Mapping) -> Path:
    return roots()['batches'] / plan['game_id'] / plan['batch_id'] / 'attempts.jsonl'


def _append_attempt(plan: Mapping, req: Mapping) -> None:
    line = canonical({'schema': ATTEMPT_SCHEMA, 'batch_id': plan['batch_id'], 'method_id': req['method_id'],
                      'variant_id': req['variant_id'], 'target_draw_number': req['target_draw_number'],
                      'run_id': req['run_id'], 'request_digest': record_digest(req)})   # ends with its newline
    with open(_attempts_path(plan), 'ab') as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())


def _attempts(plan: Mapping) -> tuple[dict, int]:
    """(method, variant, target) -> [run IDs] of this batch's well-formed attempt lines whose request digest is the
    plan's own request for that pair and run ID; and the number of lines ignored as malformed or foreign."""
    path = _attempts_path(plan)
    out, bad = {}, 0
    if not path.is_file() or path.is_symlink():
        return out, bad
    members = {(m['method_id'], m['variant_id']): m for m in plan['cohort']}
    for raw in path.read_bytes().split(b'\n'):
        if not raw:
            continue
        try:
            a = json.loads(raw.decode('ascii'))
            mem = members[(a['method_id'], a['variant_id'])]
            ok = (canonical(a) == raw + b'\n' and a['schema'] == ATTEMPT_SCHEMA and a['batch_id'] == plan['batch_id'] and
                  type(a['target_draw_number']) is int and
                  plan['window_first'] <= a['target_draw_number'] <= plan['window_last'] and
                  V.RUN_ID.fullmatch(a['run_id']) is not None and
                  a['request_digest'] == record_digest(request_for(plan, mem, a['target_draw_number'], a['run_id'])))
        except (ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError):
            ok = False
        if not ok:
            bad += 1
            continue
        out.setdefault((a['method_id'], a['variant_id'], a['target_draw_number']), []).append(a['run_id'])
    return out, bad


def _canonical_json(path: Path):
    """A record file's content, only if it is a plain file holding exactly the canonical bytes of its JSON."""
    if not path.is_file() or path.is_symlink():
        return None
    raw = path.read_bytes()
    try:
        rec = json.loads(raw.decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        return None
    return rec if isinstance(rec, dict) and canonical(rec) == raw else None


def attempt_state(plan: Mapping, mem: Mapping, target: int, run_id: str, declaration: Mapping) -> tuple[str, str]:
    """('DONE', reason) only if this attempt's run folder proves the planned run happened and ended in a CONTINUE
    class; otherwise ('NOT_DONE', why). The checks repeat read_run's record checks with the installed declaration."""
    req = request_for(plan, mem, target, run_id)
    folder = roots()['runs'] / plan['game_id'] / mem['method_id'] / mem['variant_id'] / run_id
    if not folder.is_dir() or folder.is_symlink():
        return 'NOT_DONE', 'no run folder'
    term = _canonical_json(folder / CP.FILES['terminal'])
    if term is None:
        return 'NOT_DONE', 'no valid terminal record'
    try:
        validate_terminal(term)
    except ValueError as exc:
        return 'NOT_DONE', f'invalid terminal record: {exc}'
    for k in ('run_id', 'game_id', 'method_id', 'variant_id', 'method_revision', 'registry_entry_digest'):
        if term[k] != req[k]:
            return 'NOT_DONE', f'terminal {k} differs from the planned request'
    if term['target_draw_number'] != target or term['execution_path'] != 'STANDALONE':
        return 'NOT_DONE', 'terminal target or execution path differs from the planned request'
    if classify(term['outcome'], term['outcome_reason']) != 'CONTINUE':
        return 'NOT_DONE', f"terminal {term['outcome']} {reason_prefix(term['outcome_reason'])}"
    if term['outcome'] != 'SUCCESS':
        return 'DONE', f"{term['outcome']} {reason_prefix(term['outcome_reason'])} (bound to this batch's request)"
    forecast = _canonical_json(folder / CP.FILES['forecast'])
    receipt = _canonical_json(folder / CP.FILES['forecast_receipt'])
    if forecast is None or receipt is None:
        return 'NOT_DONE', 'SUCCESS without a valid forecast and receipt'
    ok, why = consumable(forecast, receipt, term, gates_pass=True, declaration=declaration)
    if not ok:
        return 'NOT_DONE', f'forecast not consumable: {why}'
    for k in ('master_sha256', 'run_mode', 'product_kind', 'registry_entry_digest', 'run_id'):
        if receipt[k] != req[k]:
            return 'NOT_DONE', f'receipt {k} differs from the planned request'
    if receipt['execution_path'] != 'STANDALONE' or receipt['master_file'] != req['master_file']:
        return 'NOT_DONE', 'receipt execution path or master file differs'
    for k in ('declaration_digest', 'method_revision', 'observation_view', 'include_dates', 'run_mode', 'product_kind'):
        if forecast[k] != req[k]:
            return 'NOT_DONE', f'forecast {k} differs from the planned request'
    if forecast['target_draw_number'] != target or forecast['game_id'] != plan['game_id']:
        return 'NOT_DONE', 'forecast target or game differs'
    return 'DONE', 'SUCCESS, consumable, under this plan\'s pins'


def pair_states(plan: Mapping) -> tuple[dict, int]:
    """(method, variant, target) -> 'DONE' or 'NOT_DONE' for every pair of the plan; and the ignored attempt lines."""
    attempts, bad = _attempts(plan)
    reg = _registry()
    out = {}
    for mem in plan['cohort']:
        decl = reg.declaration(mem['declaration_digest'])
        for target in range(plan['window_first'], plan['window_last'] + 1):
            key = (mem['method_id'], mem['variant_id'], target)
            done = any(attempt_state(plan, mem, target, rid, decl)[0] == 'DONE' for rid in attempts.get(key, ()))
            out[key] = 'DONE' if done else 'NOT_DONE'
    return out, bad


def pending(plan: Mapping) -> list[tuple[dict, int]]:
    """Every (member, target) pair that is not proven done by an attempt of this batch, in run order."""
    states, _bad = pair_states(plan)
    return [(mem, t) for mem in plan['cohort'] for t in range(plan['window_first'], plan['window_last'] + 1)
            if states[(mem['method_id'], mem['variant_id'], t)] != 'DONE']


def _loop(plan: Mapping, todo, adapters: Mapping, runs: list):
    """Run the pending pairs in order. Returns None if every one ended in a CONTINUE class, otherwise the stop
    reason (design 5.3). Each run's summary is appended to `runs` as it ends."""
    for mem, target in todo:
        req = request_for(plan, mem, target, CP.new_run_id())
        ident = f"{mem['method_id']} {mem['variant_id']} target {target}"
        _append_attempt(plan, req)                          # bound to this batch before the run (EX_083 B01)
        try:
            res = CR.run_contract_method(req, compute=adapters[mem['method_id']].compute,
                                         verify=adapters[mem['method_id']].verify,
                                         repo_root=Path(CR.PROJECT_ROOT), run_root=roots()['runs'])
        except (CR.RunRefused, DispatchRefused) as exc:
            return f'{ident}: REFUSED: {exc.text}'
        except BaseException as exc:                       # including KeyboardInterrupt before a run folder exists
            runs.append({'run_id': req['run_id'], 'method_id': mem['method_id'], 'variant_id': mem['variant_id'],
                         'target': target, 'outcome': None, 'reason_prefix': None, 'class': 'STOP'})
            return f'{ident}: {type(exc).__name__} escaped the runner: {exc}'
        cls = classify(res.outcome, res.reason)
        runs.append({'run_id': req['run_id'], 'method_id': mem['method_id'], 'variant_id': mem['variant_id'],
                     'target': target, 'outcome': res.outcome, 'reason_prefix': reason_prefix(res.reason),
                     'class': cls})
        if cls == 'STOP':
            return f'{ident}: {res.outcome}: {res.reason}'
    return None


def run_batch(game_id: str, batch_id: str, adapters: Mapping, *, echo=print) -> int:
    """Design 5.3. Returns 0 (every pair done), 1 (stopped) or 2 (refused before any run)."""
    try:
        plan = load_plan(game_id, batch_id)
        start_checks(plan, adapters)
        todo = pending(plan)
    except BatchRefused as exc:
        echo(f'[WALK-FORWARD] REFUSED before any run: {exc}')
        return 2
    started, runs = utc_now(), []
    try:
        stop = _loop(plan, todo, adapters, runs)
    except KeyboardInterrupt:
        stop = 'KeyboardInterrupt between runs'
    left = len(pending(plan)) if stop is None else None
    seg = {'schema': SEGMENT_SCHEMA, 'batch_id': batch_id, 'game_id': game_id, 'started_utc': started,
           'ended_utc': utc_now(), 'stopped': stop is not None, 'stop_reason': stop, 'pairs_pending_at_start': len(todo),
           'runs': runs, 'driver_version': DRIVER_VERSION}
    name = f"segment_{seg['ended_utc'].replace(':', '').replace('-', '').replace('.', '')}_{uuid.uuid4().hex[:8]}.json"
    try:
        CP.create_only(roots()['batches'] / game_id / batch_id / name, canonical(seg))
    except BaseException as exc:
        echo(f'[WALK-FORWARD] the segment record could not be written ({type(exc).__name__}: {exc}); its content:')
        echo(json.dumps(seg, sort_keys=True))
        return 1
    if stop is not None:
        echo(f'[WALK-FORWARD] STOP after {len(runs)} run(s): {stop}')
        return 1
    if left:
        echo(f'[WALK-FORWARD] STOP: {left} pair(s) still pending after a complete pass')
        return 1
    echo(f'[WALK-FORWARD] COMPLETE: {len(runs)} run(s) in this invocation; every pair of the plan is done')
    return 0


def status(game_id: str, batch_id: str) -> dict:
    """Read-only counts per member: pairs proven done by this batch's own attempts, pairs pending, the attempts made
    and how each attempt stands (EX_083 WF1A-R2-B01); and the number of ignored attempt lines."""
    plan = load_plan(game_id, batch_id)
    attempts, bad = _attempts(plan)
    reg = _registry()
    out = {'ignored_attempt_lines': bad}
    for mem in plan['cohort']:
        decl = reg.declaration(mem['declaration_digest'])
        done, made, why = 0, 0, {}
        for target in range(plan['window_first'], plan['window_last'] + 1):
            states = [attempt_state(plan, mem, target, rid, decl)
                      for rid in attempts.get((mem['method_id'], mem['variant_id'], target), ())]
            made += len(states)
            done += any(s == 'DONE' for s, _ in states)
            for s, r in states:
                k = f'{s}: {r}'
                why[k] = why.get(k, 0) + 1
        n = plan['window_last'] - plan['window_first'] + 1
        out[f"{mem['method_id']} {mem['variant_id']}"] = {'done': done, 'pending': n - done, 'attempts': made,
                                                           'attempt_states': why}
    return out
