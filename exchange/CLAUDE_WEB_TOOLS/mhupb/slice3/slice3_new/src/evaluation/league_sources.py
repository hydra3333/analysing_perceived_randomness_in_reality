"""MHUP-B layer L4: the league table's sources, READ-ONLY (design supplement v0.8 sections 3 and 4; code plan v0.3 L4).

Three adapters return the same small row shape, one row per scored forecast and readout:

    {'method', 'revision', 'variant', 'target', 'readout', 'main', 'pb', 'division', 'kind', 'source', 'witnessed'}

 (a) the weekly score ledger: every routine score line, by its effective class (kinds FORWARD, LATE_PRE_DRAW,
     CATCH_UP, DEVELOPMENT);
 (b) the development score ledgers of the canonical attempts listed in LEAGUE_SOURCES_<GAME>.json (kind
     DEVELOPMENT), each read only if its SHA-256 is the one the list names;
 (c) the sealed Mode H score ledger (kind MODE_H_SEALED): shown, NEVER summed; read only if its SHA-256 is the one in
     its SCORE_COMPLETE record.

A record carries both barrels, so the one-score key is (method, revision, variant, target, readout); the scoring policy
is not in it. Two summed sources with the same key refuse, naming the key. A listed source that is absent or fails its
identity is reported as "not available" for the variants it supplies; it is never read as "no scores".

This module also reads the things a publication pins (so the same bytes can be rebuilt later from the pinned prefix of
every ledger), the publication manifests in the archive, and what a report attempt must show before it is admitted.
It opens nothing for writing; league_publish.py is the only writer of the league's files.
"""
from __future__ import annotations

import json
from pathlib import Path

import _common.contract_runner as CR
import _common.contract_vocab as V
import _common.jsonl_ledger as JL
import _common.owner_records as OR
import _common.release_records as RR
import _common.score_identities as SI
import _common.walk_forward as WF
import _common.weekly_records as WR
from _common.contract_receipts import validate_score_record
from _common.contract_records import canonical, record_digest, sha256_hex
from _common.game_profiles import get_profile

TABLE_VERSION = 'MHUPB_LEAGUE_TABLE_V1'
MANIFEST_SCHEMA = 'LEAGUE_PUBLICATION_V1'
READOUTS = ('TOP', 'WORST')
KINDS = ('DEVELOPMENT', 'CATCH_UP', 'LATE_PRE_DRAW', 'FORWARD')          # the summed kinds, in column order
KIND_OF_CLASS = {'PROSPECTIVE': 'FORWARD', 'LATE_PRE_DRAW': 'LATE_PRE_DRAW', 'CATCH_UP': 'CATCH_UP',
                 'DEVELOPMENT_WF_EXPLORATORY': 'DEVELOPMENT'}
MODE_H_KIND = 'MODE_H_SEALED'
MODE_H_LEDGER = 'mode_h_score_ledger.jsonl'
WEEKLY_SOURCE = 'WEEKLY_SCORE_LEDGER'
ROW_TYPE = 'WEEKLY_TABLE'


class LeagueRefused(Exception):
    """The league table refuses: the message names the key, source or record. Nothing was written."""


def project_root() -> Path:
    return Path(CR.PROJECT_ROOT)


def league_dir(root: Path, game_id: str) -> Path:
    return Path(root) / 'results' / 'method_rankings' / game_id / 'league'


def archive_dir(root: Path, game_id: str) -> Path:
    return league_dir(root, game_id) / 'archive'


def current_dir(root: Path, game_id: str) -> Path:
    return league_dir(root, game_id) / 'current'


def derived_dir(root: Path, game_id: str) -> Path:
    return league_dir(root, game_id) / 'derived'


def reports_dir(root: Path, game_id: str) -> Path:
    return Path(root) / 'results' / 'method_rankings' / game_id


def scores_folder(game_id: str, batch_id: str, attempt_id: str) -> Path:
    return WF.roots('WF_BATCH')['scores'] / game_id / batch_id / attempt_id


# ---------------------------------------------------------------- small readers

def canonical_file(path: Path, what: str) -> dict:
    if OR.absent(path) or path.is_symlink() or not path.is_file():
        raise LeagueRefused(f'{what}: not there')
    raw = path.read_bytes()
    try:
        rec = json.loads(raw.decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        raise LeagueRefused(f'{what}: not JSON') from None
    if type(rec) is not dict or canonical(rec) != raw:
        raise LeagueRefused(f'{what}: not a canonical record')
    return rec


def _jsonl(raw: bytes, what: str) -> list[dict]:
    """Canonical JSON lines, each ending in a newline. Anything else refuses."""
    out = []
    if raw and not raw.endswith(b'\n'):
        raise LeagueRefused(f'{what}: does not end at a line end')
    for i, line in enumerate(raw.split(b'\n')[:-1], start=1):
        try:
            rec = json.loads(line.decode('ascii'))
        except (ValueError, UnicodeDecodeError):
            raise LeagueRefused(f'{what}: line {i} is not JSON') from None
        if type(rec) is not dict or canonical(rec) != line + b'\n':
            raise LeagueRefused(f'{what}: line {i} is not a canonical record')
        out.append(rec)
    return out


def lines_pin(rows) -> dict:
    """How a publication pins an unchained ledger: how many lines, and the SHA-256 of exactly those lines."""
    return {'lines': len(rows), 'sha256': sha256_hex(b''.join(canonical(r) for r in rows))}


def _prefix(rows, pin, what: str) -> list:
    """The pinned prefix of a ledger read now. Refuses if the ledger no longer starts with it."""
    if pin is None:
        return list(rows)
    n = pin.get('lines')
    if type(n) is not int or n < 0 or n > len(rows) or lines_pin(rows[:n]) != pin:
        raise LeagueRefused(f'{what} no longer starts with the lines this publication pinned')
    return list(rows[:n])


# ---------------------------------------------------------------- the roster (Sup 3.1)

def roster(root: Path, game_id: str) -> list[list]:
    """Every released (method, revision, variant) of the game as [method, revision, variant, release date, status]:
    CURRENT for a released, unretired entry, RETIRED for one a later record retired or superseded. In identity order."""
    current = {k[1:]: d for k, d in RR.released_variants(root).items() if k[0] == game_id}
    ever = {k[1:]: d for k, d in RR.released_history(root).items() if k[0] == game_id}
    out = [[*k, str(current[k]), 'CURRENT'] for k in current]
    out += [[*k, str(d), 'RETIRED'] for k, d in ever.items() if k not in current]
    return sorted(out)


# ---------------------------------------------------------------- (a) the weekly score ledger

def _weekly(root: Path, game_id: str, pins) -> dict:
    try:
        lines = WR.forecast_ledger(root, game_id)
        SI.scored_identities(root, game_id, lines)             # the whole ledger: shape, linkage, one line per identity
        scores = WR.score_ledger(root, game_id)
        witness = WR.witness_ledger(root, game_id)
    except (OR.RecordRefused, JL.LedgerRefused) as exc:
        raise LeagueRefused(f'the weekly records do not verify: {exc}') from None
    if pins is not None:
        if not JL.extent_still_there(lines, pins['forecast_ledger']):
            raise LeagueRefused('the forecast ledger no longer holds the extent this publication pinned')
        lines = lines[:pins['forecast_ledger']['lines']]
        scores = _prefix(scores, pins['weekly_score_ledger'], 'the weekly score ledger')
        witness = _prefix(witness, pins['witness_ledger'], 'the witness ledger')
    by_target = {line['target_draw_number']: line for line in lines}
    witnessed = set()                                          # targets whose freeze line was verified before its draw
    for w in witness:
        line = by_target.get(w['target_draw_number'])
        if (line is not None and w['kind'] == 'WITNESS_VERIFIED' and w['freeze_line_digest'] == record_digest(line) and
                WR.parse_utc(w['received_utc'], 'witness received_utc') < WR.parse_utc(line['deadline_utc'])):
            witnessed.add(w['target_draw_number'])
    rows, failed, unavailable, amended = [], [], 0, {}
    for s in scores:
        ident = (s['method_id'], s['method_revision'], s['variant_id'], s['target_draw_number'])
        if s['scoring_policy_id'] != WR.ROUTINE_POLICY:        # a correction stands beside its line; the table uses
            if s['amendment_of'] in amended:                   # the routine line, and a branching chain refuses
                raise LeagueRefused(f'two corrections name the same score line of {ident}: the chain branches')
            amended[s['amendment_of']] = ident
            continue
        kind = KIND_OF_CLASS.get(s['effective_class'])
        if kind is None:
            raise LeagueRefused(f'weekly score line of {ident}: class {s["effective_class"]} is not a weekly class')
        if s['record_kind'] == 'PREDICTION_FAILED':
            failed.append(ident)
            continue
        for ro in READOUTS:
            r = s['readouts'][ro]
            if 'unavailable' in r:
                unavailable += 1
                continue
            rows.append({'method': ident[0], 'revision': ident[1], 'variant': ident[2], 'target': ident[3],
                         'readout': ro, 'main': r['main_matches'], 'pb': r.get('powerball_match'),
                         'division': r['division'], 'kind': kind, 'source': WEEKLY_SOURCE,
                         'witnessed': kind == 'FORWARD' and ident[3] in witnessed, 'drawn_main': s['drawn_main']})
    return {'rows': rows, 'failed': failed, 'unavailable_readouts': unavailable, 'amendments': len(amended),
            'pins': {'forecast_ledger': JL.extent(lines), 'weekly_score_ledger': lines_pin(scores),
                     'witness_ledger': lines_pin(witness)}}


# ---------------------------------------------------------------- (b) the canonical development attempts

def score_records(raw: bytes, game_id: str, what: str) -> list[dict]:
    """The score records of one development or Mode H score ledger, each validated as the installed writer's record."""
    out = []
    for rec in _jsonl(raw, what):
        if rec.get('schema') != V.SCORE:
            continue                                           # the Mode H ledger also holds rank lines
        try:
            validate_score_record(rec)
        except (ValueError, TypeError, KeyError) as exc:
            raise LeagueRefused(f'{what}: a score record does not validate: {exc}') from None
        parts = rec['track_id'].split(':')
        if len(parts) != 5 or parts[0] != game_id or rec['game_id'] != game_id or parts[4] != 'WF' or parts[3] not in READOUTS:
            raise LeagueRefused(f'{what}: a score record of another game, mode or readout')
        out.append(rec)
    return out


def _dev_row(rec: dict, kind: str, source: str) -> dict:
    _g, method, variant, readout, _m = rec['track_id'].split(':')
    return {'method': method, 'revision': rec['method_revision'], 'variant': variant, 'target': rec['draw_number'],
            'readout': readout, 'main': rec['main_matches'], 'pb': rec.get('powerball_match'),
            'division': rec['division'], 'kind': kind, 'source': source, 'witnessed': False,
            'drawn_main': rec['drawn_main']}


def source_rows(game_id: str, entry: dict) -> list[dict]:
    """The rows of one listed attempt, after its identity has been checked. LeagueRefused says why it is not available."""
    aid = entry['attempt_id']
    folder = scores_folder(game_id, entry['batch_id'], aid)
    path = folder / 'score_ledger.jsonl'
    if OR.absent(path) or path.is_symlink() or not path.is_file():
        raise LeagueRefused('its score ledger is not there')
    raw = path.read_bytes()
    if sha256_hex(raw) != entry['score_ledger_sha256']:
        raise LeagueRefused('its score ledger is not the bytes the source list names')
    sp = canonical_file(folder / 'scoring_plan.json', 'its scoring plan')
    if (sp.get('attempt_id'), sp.get('batch_id'), sp.get('game_id'), sp.get('window_first'), sp.get('window_last'),
            sp.get('plan_digest'), sp.get('evaluator_version')) != (
            aid, entry['batch_id'], game_id, entry['window_first'], entry['window_last'], entry['plan_digest'],
            entry['evaluator_version']):
        raise LeagueRefused('its scoring plan is not the attempt, batch, window and plan the source list names')
    rows = []
    for rec in score_records(raw, game_id, f'score ledger of {aid}'):
        if not entry['window_first'] <= rec['draw_number'] <= entry['window_last'] or \
                rec['evaluator_version'] != entry['evaluator_version']:
            raise LeagueRefused('a score record outside the listed window or of another evaluator version')
        rows.append(_dev_row(rec, 'DEVELOPMENT', aid))
    return rows


def _affected(game_id: str, entry: dict):
    """The (method, variant) pairs a listed attempt supplies, from its batch plan; None (every variant) if the plan
    itself cannot be read."""
    try:
        plan = WF.load_plan(game_id, entry['batch_id'])
    except WF.BatchRefused:
        return None
    return sorted({(m['method_id'], m['variant_id']) for m in plan['cohort']})


# ---------------------------------------------------------------- (c) the sealed Mode H ledger: shown, never summed

def mode_h_identity(root: Path, game_id: str) -> dict | None:
    """What names the game's sealed Mode H score ledger: its batch, attempt and the SHA-256 in SCORE_COMPLETE."""
    try:
        rec = OR.batch_id_record(root, game_id)
        done = None if rec is None else OR.marker(root, game_id, rec['batch_id'], 'SCORE_COMPLETE')
    except OR.RecordRefused as exc:
        raise LeagueRefused(f'the Mode H records do not verify: {exc}') from None
    if done is None:
        return None
    return {'batch_id': rec['batch_id'], 'attempt_id': done.get('attempt_id'),
            'score_ledger_sha256': done['score_ledger_sha256']}


def _mode_h(root: Path, game_id: str) -> dict:
    try:
        ident = mode_h_identity(root, game_id)
        if ident is None:
            return {'rows': [], 'identity': None, 'not_available': 'no completed Mode H score is recorded'}
        path = OR.mode_h_scores_root(root) / game_id / ident['batch_id'] / str(ident['attempt_id']) / MODE_H_LEDGER
        if OR.absent(path) or path.is_symlink() or not path.is_file():
            raise LeagueRefused('the ledger file is not there')
        raw = path.read_bytes()
        if sha256_hex(raw) != ident['score_ledger_sha256']:
            raise LeagueRefused('the ledger is not the bytes its SCORE_COMPLETE record names')
        rows = [_dev_row(r, MODE_H_KIND, MODE_H_KIND) for r in score_records(raw, game_id, 'the sealed Mode H ledger')]
    except LeagueRefused as exc:
        return {'rows': [], 'identity': None, 'not_available': str(exc)}
    return {'rows': rows, 'identity': ident, 'not_available': None}


# ---------------------------------------------------------------- everything one table needs, and its pins

def sources_file_digest(root: Path, game_id: str) -> str | None:
    path = SI.league_sources_path(root, game_id)
    return None if OR.absent(path) else sha256_hex(path.read_bytes())


def collect(root: Path, game_id: str, pins: dict | None = None) -> tuple[dict, dict]:
    """(data, pins). With `pins` (a publication manifest's inputs) the same reading is repeated on exactly the pinned
    inputs: the listed sources and roster as pinned, the pinned prefix of every weekly ledger. LeagueRefused if a
    summed key appears twice, a weekly record does not verify, or a pinned input is no longer there."""
    get_profile(game_id)
    try:
        entries = SI.league_sources(root, game_id) if pins is None else pins['sources']
    except OR.RecordRefused as exc:
        raise LeagueRefused(str(exc)) from None
    people = roster(root, game_id) if pins is None else pins['roster']
    weekly = _weekly(root, game_id, pins)
    rows, not_available = list(weekly['rows']), []
    for e in entries:
        try:
            rows += source_rows(game_id, e)
        except LeagueRefused as exc:
            not_available.append({'source': e['attempt_id'], 'reason': str(exc), 'variants': _affected(game_id, e)})
    seen = {}
    for r in rows:
        key = (r['method'], r['revision'], r['variant'], r['target'], r['readout'])
        if key in seen:
            raise LeagueRefused(f'one score per draw and readout: {key} is supplied by {seen[key]} and by {r["source"]}')
        seen[key] = r['source']
    mode_h = _mode_h(root, game_id)
    out_pins = {'sources_file_sha256': sources_file_digest(root, game_id) if pins is None else pins['sources_file_sha256'],
                'sources': entries, 'roster': people, **weekly['pins'], 'mode_h': mode_h['identity'],
                'not_available': [[n['source'], n['reason']] for n in not_available]}
    data = {'game_id': game_id, 'roster': people, 'rows': rows, 'failed': weekly['failed'],
            'unavailable_readouts': weekly['unavailable_readouts'], 'amendments': weekly['amendments'],
            'mode_h': mode_h, 'not_available': not_available, 'sources': entries,
            'sources_file_sha256': out_pins['sources_file_sha256'], 'pins': out_pins}
    return data, out_pins


def canonical_keys(root: Path, game_id: str) -> dict:
    """key -> source for every key a summed source supplies now (used by the admission step)."""
    data, _pins = collect(root, game_id)
    if data['not_available']:
        n = data['not_available'][0]
        raise LeagueRefused(f'a listed source is not available ({n["source"]}: {n["reason"]}); nothing can be admitted '
                            f'until it is')
    return {(r['method'], r['revision'], r['variant'], r['target'], r['readout']): r['source'] for r in data['rows']}


# ---------------------------------------------------------------- the publication manifests (read side)

def search_rows(game_id: str) -> list[dict]:
    import csv
    import io
    path = WF.roots()['search_log']
    if OR.absent(path):
        return []
    raw = path.read_bytes()
    if not raw.endswith(b'\n'):
        raise LeagueRefused('the search log does not end at a line end (an unfinished row); nothing is appended to it')
    return [r for r in csv.DictReader(io.StringIO(raw.decode('ascii'))) if r.get('game_id') == game_id]


def validate_manifest(m: dict, game_id: str, name: str) -> dict:
    fields = {'schema', 'game_id', 'version', 'latest_draw', 'published_utc', 'name', 'txt_sha256', 'csv_sha256',
              'inputs', 'tool', 'table_version'}
    if (type(m) is not dict or set(m) != fields or m['schema'] != MANIFEST_SCHEMA or m['game_id'] != game_id or
            m['name'] != name or type(m['version']) is not int or m['version'] < 1 or
            type(m['latest_draw']) is not int or type(m['inputs']) is not dict or
            not all(type(m[f]) is str and V.SHA256.fullmatch(m[f]) for f in ('txt_sha256', 'csv_sha256')) or
            name != publication_name(game_id, m['latest_draw'], m['version'], m['published_utc'])):
        raise LeagueRefused(f'publication manifest {name}: not a {MANIFEST_SCHEMA} record of this game and name')
    ext = m['inputs'].get('forecast_ledger')
    if type(ext) is not dict or set(ext) != {'lines', 'last_line_digest'}:
        raise LeagueRefused(f'publication manifest {name}: it pins no forecast-ledger extent')
    return m


def publication_name(game_id: str, latest_draw: int, version: int, published_utc: str) -> str:
    stamp = published_utc[:19].replace('-', '').replace(':', '') + 'Z'
    return f'league_{game_id}_d{latest_draw:05d}_v{version:05d}_{stamp}'


def manifests(root: Path, game_id: str) -> list[dict]:
    """Every publication manifest in the archive, validated, in version order, each with 'logged' (its WEEKLY_TABLE
    row exists) and 'incomplete' (a PUBLICATION_INCOMPLETE note stands beside it). Two manifests of one version, a
    manifest that does not validate, or two rows naming one manifest refuse."""
    folder = archive_dir(root, game_id)
    out = []
    logged: dict[str, int] = {}
    for r in search_rows(game_id):
        if r.get('row_type') == ROW_TYPE:
            logged[r.get('attempt_id')] = logged.get(r.get('attempt_id'), 0) + 1
    twice = sorted(n for n, c in logged.items() if c > 1)
    if twice:
        raise LeagueRefused(f'two search-log rows name the publication {twice[0]}')
    if folder.is_dir():
        for path in sorted(folder.glob('league_*.manifest.json')):
            name = path.name[:-len('.manifest.json')]
            m = validate_manifest(canonical_file(path, f'publication manifest {name}'), game_id, name)
            out.append({'manifest': m, 'digest': record_digest(m), 'name': name, 'logged': name in logged,
                        'incomplete': not OR.absent(folder / f'{name}.PUBLICATION_INCOMPLETE.json')})
    out.sort(key=lambda p: p['manifest']['version'])
    versions = [p['manifest']['version'] for p in out]
    if len(set(versions)) != len(versions):
        raise LeagueRefused('two publication manifests carry the same version number')
    missing = sorted(set(logged) - {p['name'] for p in out})
    if missing:
        raise LeagueRefused(f'a search-log row names the publication {missing[0]}, whose manifest is not in the archive')
    return out


def latest_logged(root: Path, game_id: str) -> dict | None:
    done = [p for p in manifests(root, game_id) if p['logged']]
    return done[-1] if done else None


def publication_names(root: Path, game_id: str) -> list[dict]:
    """What OV-1's reconcile step checks (Sup 6.8; EX_225 RC-225-1): the forecast-ledger extent every logged or
    pending publication pinned. A publication marked incomplete is not evidence and names nothing."""
    return [{'what': f'league publication {p["name"]}', **p['manifest']['inputs']['forecast_ledger']}
            for p in manifests(root, game_id) if not p['incomplete']]


# ---------------------------------------------------------------- report attempts (read side of the admission step)

def report_attempts(root: Path, game_id: str, batch_id: str) -> list[dict]:
    """The RANKING_REPORT search-log rows of one batch, oldest first."""
    return [r for r in search_rows(game_id) if r.get('row_type') == 'RANKING_REPORT' and r.get('batch_id') == batch_id]


def attempt_entry(root: Path, game_id: str, attempt_id: str) -> tuple[dict, list[dict]]:
    """(the source-list entry, the rows) of one COMPLETE, correctly labelled development report attempt, verified
    from its own records: its search-log row, its scoring plan, its batch plan, its score ledger and the report
    files' manifest. LeagueRefused says what is missing; a listed plan is not a score."""
    mine = [r for r in search_rows(game_id) if r.get('row_type') == 'RANKING_REPORT' and r.get('attempt_id') == attempt_id]
    if len(mine) != 1:
        raise LeagueRefused(f'{attempt_id}: no single RANKING_REPORT search-log row names this attempt')
    row = mine[0]
    batch_id = row.get('batch_id', '')
    try:
        plan = WF.load_plan(game_id, batch_id)
    except WF.BatchRefused as exc:
        raise LeagueRefused(f'{attempt_id}: its batch plan does not load: {exc}') from None
    kind = WF.kind_of(plan)
    if kind == 'MODE_H_BATCH':
        raise LeagueRefused(f'{attempt_id}: a Mode H attempt is never a summed source')
    batch_kind = plan['plan_kind'] if kind == 'DEV_BATCH' else 'WF_BATCH_PLAN_V1'
    if batch_kind not in SI.LEAGUE_SOURCE_KINDS:
        raise LeagueRefused(f'{attempt_id}: an exploratory rerun is never admitted (supplement 4 rule 2A)')
    folder = scores_folder(game_id, batch_id, attempt_id)
    sp = canonical_file(folder / 'scoring_plan.json', f'{attempt_id}: scoring plan')
    body = {k: v for k, v in sp.items() if k != 'search_log_row'}
    if (record_digest(body) != row.get('plan_digest') or sp.get('attempt_id') != attempt_id or
            sp.get('batch_id') != batch_id or sp.get('game_id') != game_id or sp.get('mode') != 'WF' or
            sp.get('plan_digest') != record_digest(plan) or sp.get('plan_kind', 'WF_BATCH_PLAN_V1') != batch_kind):
        raise LeagueRefused(f'{attempt_id}: its scoring plan is not the one its search-log row and batch plan name')
    first, last = sp['window_first'], sp['window_last']
    found = sorted(reports_dir(root, game_id).glob(f'ranking_{game_id}_WF_{first}-{last}_*_{attempt_id}.json'))
    if len(found) != 1:
        raise LeagueRefused(f'{attempt_id}: its report did not complete (no report manifest file)')
    man = canonical_file(found[0], f'{attempt_id}: report manifest')
    base = found[0].name[:-len('.json')]
    members = {ext: found[0].with_name(f'{base}.{ext}') for ext in ('txt', 'csv')}
    if (man.get('schema') != 'RANKING_REPORT_MANIFEST_V1' or man.get('attempt_id') != attempt_id or
            man.get('batch_id') != batch_id or man.get('mode') != 'WF' or
            man.get('evidence_tier') != 'DEVELOPMENT_WF_EXPLORATORY' or
            man.get('scoring_plan_digest') != row.get('plan_digest') or
            (man.get('window_first'), man.get('window_last')) != (first, last) or
            man.get('plan_kind', 'WF_BATCH_PLAN_V1') != batch_kind or
            any(OR.absent(p) or sha256_hex(p.read_bytes()) != man.get(f'{ext}_sha256' if ext == 'csv' else 'text_sha256')
                for ext, p in members.items())):
        raise LeagueRefused(f'{attempt_id}: its report files are not a complete development report of this attempt')
    path = folder / 'score_ledger.jsonl'
    if OR.absent(path) or OR.absent(folder / 'rank_ledger.jsonl'):
        raise LeagueRefused(f'{attempt_id}: its score or rank ledger is not there')
    raw = path.read_bytes()
    entry = {'attempt_id': attempt_id, 'batch_id': batch_id, 'batch_kind': batch_kind,
             'plan_digest': record_digest(plan), 'window_first': first, 'window_last': last,
             'score_ledger_sha256': sha256_hex(raw), 'evaluator_version': sp['evaluator_version']}
    rows = source_rows(game_id, entry)
    selected = {(s[0], s[1], s[2]): s[3] for s in sp['selected_forecasts']}
    # Every score is checked against the frozen forecast it scores (read again here; no outcome is read): the ledger
    # must hold exactly one record for every available readout of every selected forecast, and each record's matches
    # must be those of its frozen ticket against the drawn numbers the record itself carries.
    from . import collect as COL
    want = {}
    for (method, variant, t), cell in COL.collect(plan, first, last)['cells'].items():
        if cell['valid'] and selected.get((method, variant, t)) == cell['forecast_content_digest']:
            for readout, ticket in cell['entries'].items():
                want[(method, variant, t, readout)] = ticket
    got, drawn = set(), {}
    for rec in score_records(raw, game_id, f'score ledger of {attempt_id}'):
        _g, method, variant, readout, _m = rec['track_id'].split(':')
        key = (method, variant, rec['draw_number'], readout)
        ticket = want.get(key)
        if ticket is None or key in got or selected.get(key[:3]) != rec['forecast_content_digest']:
            raise LeagueRefused(f'{attempt_id}: a score record of {key} is not the one score of a forecast its scoring '
                                f'plan selected from its batch')
        if drawn.setdefault(rec['draw_number'], (rec['drawn_main'], rec.get('drawn_powerball'))) != \
                (rec['drawn_main'], rec.get('drawn_powerball')):
            raise LeagueRefused(f'{attempt_id}: two score records disagree about the numbers drawn in draw {key[2]}')
        if rec['main_matches'] != len(set(ticket[0]) & set(rec['drawn_main'])) or \
                (game_id == 'POWERBALL' and rec['powerball_match'] != (1 if ticket[1] == rec['drawn_powerball'] else 0)):
            raise LeagueRefused(f'{attempt_id}: the score record of {key} does not hold the matches of its frozen ticket '
                                f'against the drawn numbers it records')
        got.add(key)
    if got != set(want) or {k[:3] for k in want} != set(selected):
        raise LeagueRefused(f'{attempt_id}: its score ledger does not hold a score for every forecast and readout its '
                            f'scoring plan selected (the report is not complete)')
    return entry, rows


def batch_state(root: Path, game_id: str, batch_id: str, first: int | None = None, last: int | None = None) -> dict:
    """Where one development batch's job stands, from the records alone (the development sequencer's question): its
    kind and window, the complete report attempts for the window, and which of them is listed."""
    try:
        plan = WF.load_plan(game_id, batch_id)
    except WF.BatchRefused as exc:
        raise LeagueRefused(f'unknown or altered batch: {exc}') from None
    kind = WF.kind_of(plan)
    if kind == 'MODE_H_BATCH':
        raise LeagueRefused('the Mode H batch is not a development batch')
    batch_kind = plan['plan_kind'] if kind == 'DEV_BATCH' else 'WF_BATCH_PLAN_V1'
    if first is None or last is None:
        if kind != 'DEV_BATCH':
            raise LeagueRefused('a batch of the first kind needs --first and --last')
        first, last = plan['window_first'], plan['window_last']
    try:
        listed = {s['attempt_id'] for s in SI.league_sources(root, game_id)}
    except OR.RecordRefused as exc:
        raise LeagueRefused(str(exc)) from None
    complete, reasons = [], []
    for r in report_attempts(root, game_id, batch_id):
        if (r.get('window_first'), r.get('window_last')) != (str(first), str(last)):
            continue
        try:
            entry, _rows = attempt_entry(root, game_id, r['attempt_id'])
            complete.append(entry['attempt_id'])
        except LeagueRefused as exc:
            if batch_kind in SI.LEAGUE_SOURCE_KINDS:
                reasons.append(str(exc))
            elif _exploratory_complete(root, game_id, r, first, last):
                complete.append(r['attempt_id'])
    admitted = [a for a in complete if a in listed]
    return {'batch_id': batch_id, 'batch_kind': batch_kind, 'first': first, 'last': last, 'complete': complete,
            'admitted': admitted[0] if admitted else None, 'incomplete_reasons': reasons}


def _exploratory_complete(root: Path, game_id: str, row: dict, first: int, last: int) -> bool:
    """An exploratory attempt is never admitted; the sequencer only needs to know that its report was written."""
    found = sorted(reports_dir(root, game_id).glob(f'ranking_{game_id}_WF_{first}-{last}_*_{row["attempt_id"]}.json'))
    return len(found) == 1
