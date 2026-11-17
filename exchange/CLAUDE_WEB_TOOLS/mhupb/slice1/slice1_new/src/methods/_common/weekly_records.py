"""MHUP-B: the weekly session's records (design v0.1r7 sections 6.1 to 6.6 and Appendices F and I): where they live,
their full shapes, the deadline, and the effective class as one pure function.

Orchestration-only and value-free: no master, no draw, no outcome is read here. The forecasting half writes session
records and freeze lines; the scoring half writes score and witness lines; both validate through this module, so a
record a writer produces is exactly what every reader accepts. `owner_records` keeps the minimal readers the dispatch
gate uses (it reads only a session's identity, pin and roster, and a freeze line's target).
"""
from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import re

import _common.contract_vocab as V
from _common.game_profiles import get_profile
from _common import owner_records as OR

RecordRefused = OR.RecordRefused
SESSION_TOOL = 'Method_Weekly_Forecast.py'
FORECAST_VERSION = 'MHUPB_WEEKLY_FORECAST_V1'
SCORE_LINE_SCHEMA = 'WEEKLY_SCORE_LINE_V1'
WITNESS_SCHEMA = 'WITNESS_LINE_V1'
ROUTINE_POLICY = 'WEEKLY_SCORE_POLICY_V1'          # the ratified measure set and formulas of WF-1B, per target
SET_KINDS = ('CATCH_UP_SET', 'NEXT_DRAW_SET')
RECORD_KINDS = ('FORECAST', 'PREDICTION_FAILED')
EFFECTIVE_CLASSES = ('PROSPECTIVE', 'LATE_PRE_DRAW', 'CATCH_UP', 'DEVELOPMENT_WF_EXPLORATORY', 'HOLDOUT_MODE_H')
HOUR_RULE = timedelta(minutes=60)                  # a next-draw set starts only with at least this long to its deadline
RESUME_TOKEN_MAX_AGE = timedelta(minutes=5)
_SHA = V.SHA256
_UTC = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z\Z', re.ASCII)


# ---------------------------------------------------------------- paths

def score_ledger_path(root: Path, game_id: str) -> Path:
    return OR.weekly_root(root, game_id) / 'SCORE_LEDGER_V1.jsonl'


def witness_ledger_path(root: Path, game_id: str) -> Path:
    return OR.weekly_root(root, game_id) / 'WITNESS_LEDGER_V1.jsonl'


def sessions_folder(root: Path, game_id: str) -> Path:
    return OR.weekly_root(root, game_id) / 'sessions'


# ---------------------------------------------------------------- the clock (patched only by the test harness)

def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def local_midnight(day: date) -> datetime:
    """00:00 local time at the start of `day`, from the PC's clock and time zone, as an aware datetime (design 6.4)."""
    return datetime(day.year, day.month, day.day).astimezone()


def utc_text(when: datetime) -> str:
    return when.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def parse_utc(text: object, what: str = 'time') -> datetime:
    if type(text) is not str or not _UTC.fullmatch(text):
        raise RecordRefused(f'{what}: not a UTC instant')
    body = text[:-1]
    fmt = '%Y-%m-%dT%H:%M:%S.%f' if '.' in body else '%Y-%m-%dT%H:%M:%S'
    try:
        return datetime.strptime(body, fmt).replace(tzinfo=timezone.utc)
    except ValueError:
        raise RecordRefused(f'{what}: not a UTC instant') from None


def offset_minutes(when: datetime) -> int:
    return int(when.utcoffset().total_seconds() // 60)


def deadline(game_id: str, target: int) -> tuple[datetime, int]:
    """(the deadline as a UTC instant, the local offset in minutes): 00:00 local on the target's derived draw date. The
    local clock is not an independent witness (design 6.5)."""
    local = local_midnight(get_profile(game_id).derived_date(target))
    return local.astimezone(timezone.utc), offset_minutes(local)


# ---------------------------------------------------------------- the effective class (Appendix I), one pure function

def effective_class(run_mode: str, frozen_at_utc: datetime | None, deadline_utc: datetime, *, failed: bool = False) -> str:
    """A record's effective class from its own facts only: the run mode (hence the immutable tier), its own freeze
    time and the target's deadline. A failure record is missing in its mode's class. The session binding and the
    freeze line's roster are identity, not inputs: a record classified in one session has the same class in another."""
    if run_mode == 'REAL_HOLDOUT':
        return 'HOLDOUT_MODE_H'
    if run_mode == 'CATCH_UP':
        return 'CATCH_UP'
    if run_mode == 'REAL_DEVELOPMENT':
        return 'DEVELOPMENT_WF_EXPLORATORY'
    if run_mode == 'FINAL_NEXT_DRAW':
        if failed:
            return 'PROSPECTIVE'
        if frozen_at_utc is None:
            raise RecordRefused('a FINAL_NEXT_DRAW forecast has no freeze time')
        return 'PROSPECTIVE' if frozen_at_utc < deadline_utc else 'LATE_PRE_DRAW'
    raise RecordRefused(f'no effective class for run mode {run_mode!r}')


def tier_of(run_mode: str) -> str:
    return V.producible(run_mode, V.FORECAST)[1]


# ---------------------------------------------------------------- small checkers

def _need(rec: Mapping, fields, what: str) -> None:
    if type(rec) is not dict:
        raise RecordRefused(f'{what}: not an object')
    extra, missing = set(rec) - set(fields), set(fields) - set(rec)
    if extra or missing:
        raise RecordRefused(f'{what}: fields are not exactly its own (missing {sorted(missing)}, extra {sorted(extra)})')


def _sha(v, what: str, *, optional: bool = False) -> None:
    if v is None and optional:
        return
    if type(v) is not str or not _SHA.fullmatch(v):
        raise RecordRefused(f'{what}: not 64 lower-case hex digits')


def _text_id(v, pattern, what: str) -> None:
    if type(v) is not str or not pattern.fullmatch(v):
        raise RecordRefused(f'{what}: malformed')


def _iso_date(v, what: str) -> date:
    try:
        d = date.fromisoformat(v)
    except (TypeError, ValueError):
        raise RecordRefused(f'{what}: not an ISO date') from None
    if d.isoformat() != v:
        raise RecordRefused(f'{what}: not an ISO date')
    return d


# ---------------------------------------------------------------- SESSION_V1 (design 6.1)

SESSION_FIELDS = ('schema', 'session_id', 'game_id', 'started_utc', 'ledger_version', 'master_sha256', 'last_draw',
                  'developed_record_sha256', 'closure_digest', 'environment_digest', 'roster', 'not_runnable', 'tool',
                  'tool_version')
ROSTER_FIELDS = ('method_id', 'method_revision', 'variant_id', 'release_date', 'declaration_digest',
                 'registry_entry_digest', 'minimum_history_draws')


def validate_session(rec: Mapping, game_id: str, what: str = 'session record') -> dict:
    _need(rec, SESSION_FIELDS, what)
    if rec['schema'] != OR.SESSION_SCHEMA or rec['game_id'] != game_id:
        raise RecordRefused(f'{what}: wrong schema or game')
    _text_id(rec['session_id'], OR.SESSION_ID, f'{what}.session_id')
    parse_utc(rec['started_utc'], f'{what}.started_utc')
    OR.pin_of(rec, what)
    p = get_profile(game_id)
    if type(rec['last_draw']) is not int or rec['last_draw'] < p.holdout_last:
        raise RecordRefused(f'{what}: last_draw is not a draw at or after the holdout\'s last')
    for f in ('developed_record_sha256', 'closure_digest', 'environment_digest'):
        _sha(rec[f], f'{what}.{f}')
    if type(rec['roster']) is not list or not rec['roster']:
        raise RecordRefused(f'{what}: roster missing or empty')
    seen = set()
    for m in rec['roster']:
        _need(m, ROSTER_FIELDS, f'{what}: a roster entry')
        _text_id(m['method_id'], V.METHOD_ID, f'{what}: roster method_id')
        _text_id(m['variant_id'], V.VARIANT_ID, f'{what}: roster variant_id')
        _text_id(m['method_revision'], V.REVISION, f'{what}: roster method_revision')
        _iso_date(m['release_date'], f'{what}: roster release_date')
        _sha(m['declaration_digest'], f'{what}: roster declaration_digest')
        _sha(m['registry_entry_digest'], f'{what}: roster registry_entry_digest')
        if type(m['minimum_history_draws']) is not int or m['minimum_history_draws'] < 0:
            raise RecordRefused(f'{what}: roster minimum_history_draws')
        key = (m['method_id'], m['variant_id'])
        if key in seen:
            raise RecordRefused(f'{what}: a variant is listed twice')
        seen.add(key)
    if type(rec['not_runnable']) is not list:
        raise RecordRefused(f'{what}: not_runnable is not a list')
    return dict(rec)


def session(root: Path, game_id: str, session_id: str) -> dict:
    """The full session record: the gate's reader (canonical bytes, identity, pin) plus the full shape."""
    return validate_session(OR.session_record(root, game_id, session_id), game_id)


# ---------------------------------------------------------------- FREEZE_LINE_V1 (design 6.5)

FREEZE_FIELDS = ('schema', 'game_id', 'target_draw_number', 'target_draw_date', 'set_kind', 'writing_session_id',
                 'frozen_utc', 'local_offset_minutes', 'deadline_utc', 'deadline_offset_minutes', 'deadline_met',
                 'records', 'not_runnable', 'closure_digest', 'environment_digest', 'tool', 'tool_version',
                 'line_number', 'previous_line_digest')
NAMED_FIELDS = ('method_id', 'method_revision', 'variant_id', 'session_id', 'session_digest', 'run_id', 'run_mode',
                'tier', 'record_kind', 'terminal_class', 'done_ticket_digest', 'scored_record_digest',
                'freeze_receipt_digest', 'terminal_digest', 'ledger_version', 'master_sha256', 'frozen_at_utc',
                'release_date', 'effective_class', 'missing_batch')


def validate_named_record(r: Mapping, game_id: str, target: int, deadline_utc: datetime, what: str) -> dict:
    _need(r, NAMED_FIELDS, what)
    _text_id(r['method_id'], V.METHOD_ID, f'{what}.method_id')
    _text_id(r['variant_id'], V.VARIANT_ID, f'{what}.variant_id')
    _text_id(r['method_revision'], V.REVISION, f'{what}.method_revision')
    _text_id(r['session_id'], OR.SESSION_ID, f'{what}.session_id')
    _text_id(r['run_id'], V.RUN_ID, f'{what}.run_id')
    for f in ('session_digest', 'done_ticket_digest', 'scored_record_digest', 'terminal_digest', 'master_sha256'):
        _sha(r[f], f'{what}.{f}')
    if r['run_mode'] not in ('CATCH_UP', 'FINAL_NEXT_DRAW', 'REAL_DEVELOPMENT'):
        raise RecordRefused(f'{what}: run mode {r["run_mode"]!r} is not a weekly session\'s')
    if r['tier'] != tier_of(r['run_mode']):
        raise RecordRefused(f'{what}: tier does not follow from the run mode')
    if r['record_kind'] not in RECORD_KINDS:
        raise RecordRefused(f'{what}: unknown record kind')
    failed = r['record_kind'] == 'PREDICTION_FAILED'
    _sha(r['freeze_receipt_digest'], f'{what}.freeze_receipt_digest', optional=failed)
    if failed != (r['freeze_receipt_digest'] is None) or failed != (r['frozen_at_utc'] is None):
        raise RecordRefused(f'{what}: a forecast has its receipt and freeze time; a failure has neither')
    if type(r['terminal_class']) is not str or not r['terminal_class']:
        raise RecordRefused(f'{what}: terminal_class missing')
    if failed == r['terminal_class'].startswith('SUCCESS '):
        raise RecordRefused(f'{what}: record kind and terminal class disagree')
    if type(r['ledger_version']) is not int or r['ledger_version'] < 1:
        raise RecordRefused(f'{what}: ledger_version')
    frozen = None if failed else parse_utc(r['frozen_at_utc'], f'{what}.frozen_at_utc')
    released = _iso_date(r['release_date'], f'{what}.release_date')
    if r['effective_class'] != effective_class(r['run_mode'], frozen, deadline_utc, failed=failed):
        raise RecordRefused(f'{what}: effective_class is not what Appendix I gives this record')
    before = released < get_profile(game_id).derived_date(target)
    if r['missing_batch'] is not (before and r['run_mode'] != 'FINAL_NEXT_DRAW'):
        raise RecordRefused(f'{what}: missing_batch is not what design 6.4 gives this record')
    if r['run_mode'] == 'CATCH_UP' and not before or r['run_mode'] == 'REAL_DEVELOPMENT' and before:
        raise RecordRefused(f'{what}: run mode disagrees with the release date')
    return dict(r)


def validate_freeze_line(line: Mapping, game_id: str, what: str = 'freeze line') -> dict:
    _need(line, FREEZE_FIELDS, what)
    p = get_profile(game_id)
    if line['schema'] != OR.FREEZE_LINE_SCHEMA or line['game_id'] != game_id:
        raise RecordRefused(f'{what}: wrong schema or game')
    target = line['target_draw_number']
    if type(target) is not int or target <= p.holdout_last:
        raise RecordRefused(f'{what}: the target is not a draw after the holdout')
    if line['target_draw_date'] != p.derived_date(target).isoformat():
        raise RecordRefused(f'{what}: target_draw_date is not the target\'s derived date')
    if line['set_kind'] not in SET_KINDS:
        raise RecordRefused(f'{what}: unknown set kind')
    _text_id(line['writing_session_id'], OR.SESSION_ID, f'{what}.writing_session_id')
    parse_utc(line['frozen_utc'], f'{what}.frozen_utc')
    dl = parse_utc(line['deadline_utc'], f'{what}.deadline_utc')
    for f in ('local_offset_minutes', 'deadline_offset_minutes'):
        if type(line[f]) is not int or abs(line[f]) > 16 * 60:
            raise RecordRefused(f'{what}: {f}')
    if dl + timedelta(minutes=line['deadline_offset_minutes']) != datetime.combine(
            p.derived_date(target), datetime.min.time(), tzinfo=timezone.utc):
        raise RecordRefused(f'{what}: the deadline is not 00:00 local on the draw\'s date at the recorded offset')
    for f in ('closure_digest', 'environment_digest'):
        _sha(line[f], f'{what}.{f}')
    if type(line['records']) is not list or not line['records']:
        raise RecordRefused(f'{what}: no record named')
    seen, finals_on_time = set(), []
    for r in line['records']:
        validate_named_record(r, game_id, target, dl, f'{what}: a named record')
        key = (r['method_id'], r['method_revision'], r['variant_id'])
        if key in seen:
            raise RecordRefused(f'{what}: a variant is named twice')
        seen.add(key)
        if r['run_mode'] == 'FINAL_NEXT_DRAW' and r['record_kind'] == 'FORECAST':
            finals_on_time.append(r['effective_class'] == 'PROSPECTIVE')
    modes = {r['run_mode'] for r in line['records']}
    if line['set_kind'] == 'NEXT_DRAW_SET' and modes != {'FINAL_NEXT_DRAW'}:
        raise RecordRefused(f'{what}: a next-draw set names only FINAL_NEXT_DRAW records')
    if line['deadline_met'] is not (all(finals_on_time) if finals_on_time else None):
        raise RecordRefused(f'{what}: deadline_met does not summarise its FINAL_NEXT_DRAW records')
    if type(line['not_runnable']) is not list:
        raise RecordRefused(f'{what}: not_runnable is not a list')
    if type(line['line_number']) is not int or line['line_number'] < 1:
        raise RecordRefused(f'{what}: line_number')
    _sha(line['previous_line_digest'], f'{what}.previous_line_digest', optional=True)
    return dict(line)


def named_key(r: Mapping) -> tuple:
    return (r['method_id'], r['method_revision'], r['variant_id'])


def forecast_ledger(root: Path, game_id: str) -> list[dict]:
    """Every freeze line of the game's forecast ledger: canonical bytes, the chain, each line's full shape, one line
    per target, and freeze times that never run backwards. Anything else refuses."""
    from _common import jsonl_ledger as JL
    rows, _torn = JL.read_lines(OR.forecast_ledger_path(root, game_id))
    JL.verify_chain(rows, 'forecast ledger')
    seen, last = set(), None
    for line in rows:
        validate_freeze_line(line, game_id)
        if line['target_draw_number'] in seen:
            raise RecordRefused('forecast ledger: two freeze lines for one target')
        seen.add(line['target_draw_number'])
        when = parse_utc(line['frozen_utc'])
        if last is not None and when < last:
            raise RecordRefused('forecast ledger: a freeze time earlier than the line before it')
        last = when
    return rows


def freeze_line_for(rows, target: int) -> dict | None:
    for line in rows:
        if line['target_draw_number'] == target:
            return line
    return None


# ---------------------------------------------------------------- one session-bound run: its request and its evidence

VIEW = 'UNORDERED_SET'                              # the weekly session runs unordered, date-free views (as the driver)
SESSION_RUN_MODES = ('CATCH_UP', 'FINAL_NEXT_DRAW', 'REAL_DEVELOPMENT')


def request_for(session: Mapping, member: Mapping, target: int, run_id: str, run_mode: str) -> dict:
    """The exact RUN_REQUEST_V1 a session issues for one variant, target and run id. It pins the session's master
    version and is bound to the session record's digest; the ticket names this request's digest."""
    from _common.contract_records import record_digest
    game = session['game_id']
    return {'schema': V.RUN_REQUEST, 'game_id': game, 'method_id': member['method_id'],
            'variant_id': member['variant_id'], 'method_revision': member['method_revision'],
            'target_draw_number': target, 'observation_view': VIEW, 'include_dates': False, 'run_mode': run_mode,
            'product_kind': V.producible(run_mode, V.FORECAST)[0], 'declaration_digest': member['declaration_digest'],
            'registry_entry_digest': member['registry_entry_digest'], 'run_id': run_id,
            'master_file': f'{game}_results_master.csv', 'ledger_version': session['ledger_version'],
            'master_sha256': session['master_sha256'],
            'binding': {'kind': 'WEEKLY_SESSION', 'session_id': session['session_id'],
                        'session_digest': record_digest(session), 'run_id': run_id}}


def run_folder(root: Path, game_id: str, method_id: str, variant_id: str, run_id: str) -> Path:
    return OR.weekly_runs_root(root) / game_id / method_id / variant_id / run_id


def _canonical_file(path: Path):
    import json
    from _common.contract_records import canonical
    if not path.is_file() or path.is_symlink():
        return None
    raw = path.read_bytes()
    try:
        rec = json.loads(raw.decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        return None
    return rec if type(rec) is dict and canonical(rec) == raw else None


def run_evidence(root: Path, request: Mapping, declaration: Mapping) -> dict:
    """What the run folder of one session-bound request proves, or RecordRefused. Returned only for a run that ended
    in a CONTINUE class (the driver's STOP rule) under exactly this request: {'terminal', 'terminal_class',
    'forecast', 'receipt'}; forecast and receipt are None unless the run was a SUCCESS with a consumable forecast
    carrying this request's pins, mode, view, declaration and registry entry. The checks are the driver's
    (walk_forward.attempt_state), for a session's request."""
    import _common.contract_publication as CP
    import _common.walk_forward as WF
    from _common.contract_receipts import consumable, validate_terminal
    folder = run_folder(root, request['game_id'], request['method_id'], request['variant_id'], request['run_id'])
    if not folder.is_dir() or folder.is_symlink():
        raise RecordRefused('no run folder')
    term = _canonical_file(folder / CP.FILES['terminal'])
    if term is None:
        raise RecordRefused('no valid terminal record')
    try:
        validate_terminal(term)
    except ValueError as exc:
        raise RecordRefused(f'invalid terminal record: {exc}') from None
    for k in ('run_id', 'game_id', 'method_id', 'variant_id', 'method_revision', 'registry_entry_digest',
              'target_draw_number'):
        if term[k] != request[k]:
            raise RecordRefused(f'terminal {k} differs from the session\'s request')
    if term['execution_path'] != 'STANDALONE':
        raise RecordRefused('terminal execution path is not STANDALONE')
    if WF.classify(term['outcome'], term['outcome_reason']) != 'CONTINUE':
        raise RecordRefused(f"terminal {term['outcome']} {WF.reason_prefix(term['outcome_reason'])} is not a completed run")
    out = {'terminal': term, 'terminal_class': f"{term['outcome']} {WF.reason_prefix(term['outcome_reason'])}",
           'forecast': None, 'receipt': None}
    if term['outcome'] != 'SUCCESS':
        return out
    forecast = _canonical_file(folder / CP.FILES['forecast'])
    receipt = _canonical_file(folder / CP.FILES['forecast_receipt'])
    if forecast is None or receipt is None:
        raise RecordRefused('SUCCESS without a valid forecast and receipt')
    ok, why = consumable(forecast, receipt, term, gates_pass=True, declaration=declaration)
    if not ok:
        raise RecordRefused(f'forecast not consumable: {why}')
    for k in ('master_sha256', 'ledger_version', 'run_mode', 'product_kind', 'registry_entry_digest', 'run_id',
              'master_file'):
        if receipt[k] != request[k]:
            raise RecordRefused(f'receipt {k} differs from the session\'s request')
    if receipt['execution_path'] != 'STANDALONE' or receipt['evidence_tier'] != tier_of(request['run_mode']):
        raise RecordRefused('receipt execution path or tier differs')
    for k in ('declaration_digest', 'method_revision', 'observation_view', 'include_dates', 'run_mode', 'product_kind',
              'target_draw_number', 'game_id'):
        if forecast[k] != request[k]:
            raise RecordRefused(f'forecast {k} differs from the session\'s request')
    out.update(forecast=forecast, receipt=receipt)
    return out


def session_tickets(root: Path, game_id: str) -> dict:
    """session id -> its validated tickets, for every attempts ledger of the game (fixed root; nothing filtered)."""
    out = {}
    for path in OR.all_session_attempt_paths(root, game_id):
        sid = OR.session_id_of_attempts_path(path)
        if not OR.SESSION_ID.fullmatch(sid):
            raise RecordRefused(f'{path.name}: not a session attempts ledger name')
        out[sid] = OR.tickets(path, scope_kind='WEEKLY_SESSION', scope_id=sid, game_id=game_id)
    return out


def done_records(tickets_by_session: Mapping, target: int) -> dict:
    """(method, revision, variant) -> (session id, DONE ticket, its OPEN ticket) for one target, over every session's
    ledger. Exactly one DONE ticket per pair (the dispatch gate admits no second run); anything else refuses."""
    out = {}
    for sid, rows in tickets_by_session.items():
        opens = {t['run_id']: t for t in rows if t['kind'] == 'OPEN'}
        for t in rows:
            if t['kind'] != 'DONE' or t['target_draw_number'] != target:
                continue
            key = (t['method_id'], t['method_revision'], t['variant_id'])
            opened = opens.get(t['run_id'])
            if key in out or opened is None or OR.pair_of(opened) != OR.pair_of(t):
                raise RecordRefused(f'target {target}: the DONE tickets of {key} are not exactly one, with its OPEN ticket')
            out[key] = (sid, t, opened)
    return out


# ---------------------------------------------------------------- the cross-session check (design 6.3, Appendix E)

def verify_named_records(root: Path, game_id: str, line: Mapping) -> list[dict]:
    """For every record a freeze line names: the session that produced it exists with the digest the line records;
    that session's attempts ledger holds the record's DONE ticket, with the digest the line records, and its OPEN
    ticket names exactly the session's request; and the run folder proves that run with the digest the line records.
    Returns, in the line's order, each record's evidence ({'named', 'forecast', 'receipt', 'terminal'}); anything
    absent or invalid refuses. Nothing here requires a record's pin to equal the reader's (the equal-pin rule is for
    new publications only): a line of one session is verified, and scored, by a later one."""
    from _common.contract_records import record_digest
    from _common.contract_registry import InstalledRegistry
    import _common.contract_registry as REG
    registry = InstalledRegistry(Path(REG.DATA_ROOT))
    target = line['target_draw_number']
    tickets_by_session = session_tickets(root, game_id)
    done = done_records(tickets_by_session, target)
    out = []
    for r in line['records']:
        key = named_key(r)
        what = f'target {target}, {key[0]} revision {key[1]} {key[2]}'
        owner = session(root, game_id, r['session_id'])
        if record_digest(owner) != r['session_digest']:
            raise RecordRefused(f'{what}: its session record does not have the digest the freeze line records')
        found = done.get(key)
        if found is None or found[0] != r['session_id'] or found[1]['run_id'] != r['run_id'] or \
                record_digest(found[1]) != r['done_ticket_digest']:
            raise RecordRefused(f'{what}: its DONE ticket is not the one the freeze line records')
        member = OR.roster_entry(owner, *key)
        if member is None:
            raise RecordRefused(f'{what}: its session\'s roster does not list it')
        request = request_for(owner, member, target, r['run_id'], r['run_mode'])
        if record_digest(request) != found[2]['request_digest']:
            raise RecordRefused(f'{what}: its ticket does not name its session\'s request')
        try:
            declaration = registry.declaration(member['declaration_digest'])
        except ValueError:
            raise RecordRefused(f'{what}: its declaration is not installed') from None
        ev = run_evidence(root, request, declaration)
        failed = ev['forecast'] is None
        digest = record_digest(ev['terminal']) if failed else ev['forecast']['canonical_content_digest']
        if (failed != (r['record_kind'] == 'PREDICTION_FAILED') or digest != r['scored_record_digest'] or
                record_digest(ev['terminal']) != r['terminal_digest'] or ev['terminal_class'] != r['terminal_class'] or
                (None if failed else record_digest(ev['receipt'])) != r['freeze_receipt_digest'] or
                (None if failed else ev['receipt']['frozen_at_utc']) != r['frozen_at_utc'] or
                (owner['ledger_version'], owner['master_sha256']) != (r['ledger_version'], r['master_sha256'])):
            raise RecordRefused(f'{what}: its run folder does not hold the record the freeze line names')
        out.append({'named': dict(r), 'forecast': ev['forecast'], 'receipt': ev['receipt'], 'terminal': ev['terminal']})
    return out


# ---------------------------------------------------------------- WEEKLY_SCORE_LINE_V1 (design 6.6)

SCORE_FIELDS = ('schema', 'game_id', 'method_id', 'method_revision', 'variant_id', 'target_draw_number',
                'scored_record_digest', 'scoring_policy_id', 'amendment_of',
                'score_run_id', 'scorer_version', 'scoring_session_id', 'outcome_ledger_version', 'outcome_master_sha256',
                'scored_utc', 'freeze_line_digest', 'freeze_line_number', 'record_kind', 'run_id', 'run_mode', 'tier',
                'frozen_at_utc', 'effective_class', 'missing_batch', 'training_ledger_version', 'training_master_sha256',
                'freeze_receipt_digest', 'readouts', 'rank', 'drawn_main', 'drawn_powerball', 'exposure_flag',
                'draw_date_is_derived')
READOUTS = ('TOP', 'WORST')
MAIN_POOL = {'POWERBALL': 35, 'OZLOTTO': 47}             # the main barrel's size (R2; evaluation.divisions has the same)
SCORE_RUN_ID = re.compile(r'ws-[0-9a-f]{32}\Z', re.ASCII)


def validate_score_line(s: Mapping, what: str = 'score line') -> dict:
    """The shape of one weekly score line. The arithmetic is the evaluator's; this checks identity, provenance and that
    the quantities are present exactly when the record was a forecast."""
    _need(s, SCORE_FIELDS, what)
    if s['schema'] != SCORE_LINE_SCHEMA:
        raise RecordRefused(f'{what}: wrong schema')
    p = get_profile(s['game_id'])
    _text_id(s['method_id'], V.METHOD_ID, f'{what}.method_id')
    _text_id(s['variant_id'], V.VARIANT_ID, f'{what}.variant_id')
    _text_id(s['method_revision'], V.REVISION, f'{what}.method_revision')
    if type(s['target_draw_number']) is not int or s['target_draw_number'] <= p.holdout_last:
        raise RecordRefused(f'{what}: the target is not a draw after the holdout')
    for f in ('scored_record_digest', 'outcome_master_sha256', 'freeze_line_digest', 'training_master_sha256'):
        _sha(s[f], f'{what}.{f}')
    if type(s['scoring_policy_id']) is not str or not V.VERSION_TAG.fullmatch(s['scoring_policy_id']):
        raise RecordRefused(f'{what}: scoring_policy_id')
    _sha(s['amendment_of'], f'{what}.amendment_of', optional=True)
    if (s['scoring_policy_id'] == ROUTINE_POLICY) != (s['amendment_of'] is None):
        raise RecordRefused(f'{what}: a routine score amends nothing; an amendment carries another policy id')
    _text_id(s['score_run_id'], SCORE_RUN_ID, f'{what}.score_run_id')
    _text_id(s['scoring_session_id'], OR.SESSION_ID, f'{what}.scoring_session_id')
    _text_id(s['run_id'], V.RUN_ID, f'{what}.run_id')
    parse_utc(s['scored_utc'], f'{what}.scored_utc')
    for f in ('outcome_ledger_version', 'training_ledger_version', 'freeze_line_number'):
        if type(s[f]) is not int or s[f] < 1:
            raise RecordRefused(f'{what}: {f}')
    if s['outcome_ledger_version'] < s['training_ledger_version']:
        raise RecordRefused(f'{what}: the outcome pin is older than the training pin')
    if s['record_kind'] not in RECORD_KINDS or s['run_mode'] not in SESSION_RUN_MODES or s['tier'] != tier_of(s['run_mode']):
        raise RecordRefused(f'{what}: record kind, run mode or tier')
    failed = s['record_kind'] == 'PREDICTION_FAILED'
    if s['effective_class'] not in EFFECTIVE_CLASSES or type(s['missing_batch']) is not bool or \
            type(s['draw_date_is_derived']) is not bool:
        raise RecordRefused(f'{what}: effective class or flags')
    if failed != (s['frozen_at_utc'] is None) or failed != (s['freeze_receipt_digest'] is None):
        raise RecordRefused(f'{what}: a forecast has its receipt and freeze time; a failure has neither')
    if not failed:
        parse_utc(s['frozen_at_utc'], f'{what}.frozen_at_utc')
        _sha(s['freeze_receipt_digest'], f'{what}.freeze_receipt_digest')
    if failed:
        if s['readouts'] is not None or s['rank'] is not None:
            raise RecordRefused(f'{what}: a failure record carries no quantities')
    elif type(s['readouts']) is not dict or set(s['readouts']) != set(READOUTS) or \
            not all(type(v) is dict and v for v in s['readouts'].values()):
        raise RecordRefused(f'{what}: readouts')
    main = s['drawn_main']
    if type(main) is not list or len(main) != 7 or sorted(set(main)) != main or \
            not all(type(x) is int and 1 <= x <= MAIN_POOL[s['game_id']] for x in main):
        raise RecordRefused(f'{what}: drawn_main')
    if (s['game_id'] == 'POWERBALL') != (type(s['drawn_powerball']) is int):
        raise RecordRefused(f'{what}: drawn_powerball')
    if s['exposure_flag'] != OR.exposure_flag(s['game_id'], s['target_draw_number']):
        raise RecordRefused(f'{what}: exposure_flag is not the recorded decision for this draw')
    return dict(s)


def score_ledger(root: Path, game_id: str) -> list[dict]:
    """Every line of the game's weekly score ledger: canonical bytes and full shape. Anything else refuses."""
    from _common import jsonl_ledger as JL
    rows, _torn = JL.read_lines(score_ledger_path(root, game_id))
    for s in rows:
        validate_score_line(s)
        if s['game_id'] != game_id:
            raise RecordRefused('score ledger: a line of another game')
    return rows


# ---------------------------------------------------------------- the witness ledger (design 6.5, Appendix G)

WITNESS_KINDS = ('github', 'email')
VERIFIER_ROLES = ('project-owner', 'reviewer')


def witness_ledger(root: Path, game_id: str) -> list[dict]:
    from _common import jsonl_ledger as JL
    rows, _torn = JL.read_lines(witness_ledger_path(root, game_id))
    for w in rows:
        if w.get('schema') != WITNESS_SCHEMA or w.get('kind') not in ('WITNESS_RECORDED', 'WITNESS_VERIFIED') or \
                w.get('game_id') != game_id or type(w.get('target_draw_number')) is not int:
            raise RecordRefused('witness ledger: a line of an unknown shape')
        _sha(w.get('freeze_line_digest'), 'witness ledger: freeze_line_digest')
    return rows


def publication_status(game_id: str, line: Mapping, witness_rows) -> tuple[str, str]:
    """(status, detail) of one freeze line, derived at report time and never stored in a score line or a frozen record
    (design 6.5): PUBLISHED_BEFORE_DRAW when a WITNESS_VERIFIED line for this line's digest was received before the
    target's deadline; otherwise TIMELINESS_UNVERIFIED, with what is on file. It never changes an effective class."""
    from _common.contract_records import record_digest
    digest = record_digest(line)
    mine = [w for w in witness_rows if w['freeze_line_digest'] == digest and
            w['target_draw_number'] == line['target_draw_number']]
    limit = parse_utc(line['deadline_utc'])
    for w in mine:
        if w['kind'] == 'WITNESS_VERIFIED' and parse_utc(w['received_utc'], 'witness received_utc') < limit:
            return 'PUBLISHED_BEFORE_DRAW', 'witness verified, received before the deadline'
    if any(w['kind'] == 'WITNESS_VERIFIED' for w in mine):
        return 'TIMELINESS_UNVERIFIED', 'witness verified, received after the deadline'
    if mine:
        return 'TIMELINESS_UNVERIFIED', 'witness recorded, not verified'
    return 'TIMELINESS_UNVERIFIED', 'no witness'
