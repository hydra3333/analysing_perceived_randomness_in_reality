"""MHUP-A test fixtures: invented masters that grow, and the value-free owner records, plans, tickets and markers the
gates read (design v0.1r5 sections 3, 4.2, 5.1, 5.2, 6.1). Everything here is INVENTED; no real draw is read or
written. The prefix hashes below are computed independently of _common.master_versions (an R-4 oracle)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path

from test_e6_beta_bernoulli import varied_row, write_varied_master
from _common.contract_records import canonical, record_digest
from _common.game_draws_reader import header_for
from _common.game_profiles import get_profile
from _common import owner_records as OR

LEDGER_COLUMNS = ('version', 'utc', 'action', 'master_sha256', 'first_draw', 'last_draw', 'draw_count',
                  'added_count', 'added_first', 'added_last', 'grab_file', 'grab_sha256',
                  'backup_file', 'backup_sha256', 'tool_version', 'tool_sha256', 'note')
T0 = datetime(2026, 10, 21, 3, 0, 0, tzinfo=timezone.utc)
UTC_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def utc_at(i: int) -> str:
    return (T0 + timedelta(hours=i)).isoformat()


def master_paths(root: Path, game: str):
    f = Path(root) / 'source_data'
    return f / f'{game}_results_master.csv', f / f'{game}_results_master_ledger.csv', f / f'{game}_results_master_init_verification.json'


def write_ledger(path: Path, rows: list[dict]) -> None:
    lines = [','.join(LEDGER_COLUMNS)]
    for r in rows:
        lines.append(','.join(str(r.get(c, '')) for c in LEDGER_COLUMNS))
    path.write_bytes(('\r\n'.join(lines) + '\r\n').encode('ascii'))


def grow_master(root: Path, profile, versions: list[list[int] | None], *, variant: int = 0, crlf: bool = False) -> list[dict]:
    """Start from write_varied_master's version-1 master (last row holdout_first - 1) and append one ledger version per
    entry of `versions`: a list of draw numbers to add (an UPDATE), or None (a NO_CHANGE). Rewrites the ledger with
    the full LEDGER_COLUMNS header. Returns the ledger rows written (as dicts). The appended rows keep the master's
    line ending; `crlf` rebuilds the whole master with CRLF first (the owner's updater writes CRLF)."""
    game = profile.game_id
    master, ledger, evidence = master_paths(root, game)
    write_varied_master(root, profile, profile.holdout_first, variant)
    raw = master.read_bytes()
    if crlf:
        raw = raw.replace(b'\n', b'\r\n')
        master.write_bytes(raw)
        ev = json.loads(evidence.read_text())
        ev['master_sha256'] = sha(raw)
        evidence.write_text(json.dumps(ev))
    eol = b'\r\n' if crlf else b'\n'
    rows = [{'version': 1, 'utc': utc_at(0), 'action': 'INIT', 'master_sha256': sha(raw), 'first_draw': profile.first_draw,
             'last_draw': profile.holdout_first - 1, 'draw_count': profile.holdout_first - profile.first_draw,
             'added_count': profile.holdout_first - profile.first_draw, 'added_first': profile.first_draw,
             'added_last': profile.holdout_first - 1, 'tool_version': '0.1', 'tool_sha256': '0' * 64,
             'note': 'fixture INIT'}]
    for i, add in enumerate(versions, start=2):
        prev = rows[-1]
        if add is None:
            rows.append({'version': i, 'utc': utc_at(i), 'action': 'NO_CHANGE', 'master_sha256': prev['master_sha256'],
                         'first_draw': profile.first_draw, 'last_draw': prev['last_draw'], 'draw_count': prev['draw_count'],
                         'added_count': 0, 'grab_file': f'grab_{i}.csv', 'grab_sha256': '1' * 64, 'tool_version': '0.2',
                         'tool_sha256': '0' * 64, 'note': 'fixture NO_CHANGE'})
            continue
        assert add[0] == prev['last_draw'] + 1 and all(y == x + 1 for x, y in zip(add, add[1:]))
        raw = raw + eol.join(varied_row(profile, d, variant).encode('ascii') for d in add) + eol
        rows.append({'version': i, 'utc': utc_at(i), 'action': 'UPDATE', 'master_sha256': sha(raw),
                     'first_draw': profile.first_draw, 'last_draw': add[-1], 'draw_count': prev['draw_count'] + len(add),
                     'added_count': len(add), 'added_first': add[0], 'added_last': add[-1], 'grab_file': f'grab_{i}.csv',
                     'grab_sha256': '1' * 64, 'backup_file': f'backup_{i}.csv', 'backup_sha256': prev['master_sha256'],
                     'tool_version': '0.2', 'tool_sha256': '0' * 64, 'note': 'fixture UPDATE'})
    master.write_bytes(raw)
    write_ledger(ledger, rows)
    return rows


def independent_prefix_sha(master_raw: bytes, draw_count: int) -> str:
    """The oracle: the digest of the header plus `draw_count` rows, each with its own line ending, by a different route
    (a byte scan for line endings, not splitlines)."""
    n, pos = 0, 0
    while n < 1 + draw_count:
        nl = master_raw.index(b'\n', pos)
        pos = nl + 1
        n += 1
    return sha(master_raw[:pos])


# ---------------------------------------------------------------- owner records, plans, tickets, markers

def write_study_manifest(root: Path, game: str, payload: dict | None = None) -> str:
    p = OR.study_manifest_path(root, game)
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(payload or {'schema': OR.STUDY_MANIFEST_SCHEMA, 'game_id': game, 'fixture': True})
    p.write_bytes(raw)
    return sha(raw)


def write_opening_record(root: Path, game: str, *, freeze_version: int, freeze_sha: str, manifest_sha: str | None = None,
                         **overrides) -> dict:
    if manifest_sha is None:
        manifest_sha = write_study_manifest(root, game)
    rec = {'schema': OR.OPENING_SCHEMA, 'game': game, 'study_manifest_sha256': manifest_sha,
           'opened_utc': '2026-11-13T09:00:00Z', 'owner_statement': 'fixture: the owner opens the holdout',
           'freeze_version': freeze_version, 'freeze_master_sha256': freeze_sha}
    rec.update(overrides)
    p = OR.opening_record_path(root, game)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, sort_keys=True))
    return rec


def write_developed_record(root: Path, game: str) -> dict:
    rec = {'schema': OR.DEVELOPED_SCHEMA, 'game': game, 'declared_utc': '2026-11-15T09:00:00Z',
           'owner_statement': 'fixture: developed', 'mode_h_score_digest': 'd' * 64}
    p = OR.developed_record_path(root, game)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, sort_keys=True))
    return rec


def write_mode_h_plan(root: Path, game: str, batch_id: str, cohort: list[dict], targets: list[int]) -> dict:
    plan = {'schema': OR.MODE_H_PLAN_SCHEMA, 'batch_id': batch_id, 'game_id': game, 'cohort': cohort, 'targets': targets,
            'fixture': True}
    folder = OR.mode_h_batch_folder(root, game, batch_id)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'plan.json').write_bytes(canonical(plan))
    rec = {'schema': OR.BATCH_ID_SCHEMA, 'game_id': game, 'batch_id': batch_id}
    p = OR.batch_id_record_path(root, game)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(canonical(rec))
    return plan


def write_session(root: Path, game: str, session_id: str, roster: list[dict]) -> dict:
    rec = {'schema': OR.SESSION_SCHEMA, 'session_id': session_id, 'game_id': game, 'roster': roster, 'fixture': True}
    p = OR.session_record_path(root, game, session_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(canonical(rec))
    return rec


def append_ticket(path: Path, t: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('ab') as fh:
        fh.write(canonical(t))


def open_ticket(path: Path, request: dict, *, scope_kind: str, scope_id: str, at: str = '2026-11-14T10:00:00Z') -> dict:
    t = OR.ticket('OPEN', scope_kind=scope_kind, scope_id=scope_id, game_id=request['game_id'],
                  method_id=request['method_id'], variant_id=request['variant_id'], method_revision=request['method_revision'],
                  target_draw_number=request['target_draw_number'], run_id=request['run_id'], utc=at,
                  request_digest=record_digest(request))
    append_ticket(path, t)
    return t


def done_ticket(path: Path, request: dict, *, scope_kind: str, scope_id: str, terminal_class: str = 'SUCCESS',
                at: str = '2026-11-14T10:01:00Z') -> dict:
    t = OR.ticket('DONE', scope_kind=scope_kind, scope_id=scope_id, game_id=request['game_id'],
                  method_id=request['method_id'], variant_id=request['variant_id'], method_revision=request['method_revision'],
                  target_draw_number=request['target_draw_number'], run_id=request['run_id'], utc=at,
                  terminal_class=terminal_class)
    append_ticket(path, t)
    return t


def failed_to_start_ticket(path: Path, request: dict, *, scope_kind: str, scope_id: str,
                           at: str = '2026-11-14T10:02:00Z') -> dict:
    t = OR.ticket('FAILED_TO_START', scope_kind=scope_kind, scope_id=scope_id, game_id=request['game_id'],
                  method_id=request['method_id'], variant_id=request['variant_id'], method_revision=request['method_revision'],
                  target_draw_number=request['target_draw_number'], run_id=request['run_id'], utc=at)
    append_ticket(path, t)
    return t


def write_marker(root: Path, game: str, batch_id: str, marker: str) -> None:
    folder = OR.mode_h_batch_folder(root, game, batch_id)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f'{marker}.json').write_bytes(canonical({'schema': f'{marker}_V1', 'fixture': True}))


def write_freeze_line(root: Path, game: str, target: int) -> None:
    p = OR.forecast_ledger_path(root, game)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('ab') as fh:
        fh.write(canonical({'schema': OR.FREEZE_LINE_SCHEMA, 'target_draw_number': target, 'fixture': True}))


def binding_for_plan(plan: dict, run_id: str) -> dict:
    return {'kind': 'MODE_H_BATCH', 'batch_id': plan['batch_id'], 'plan_digest': record_digest(plan), 'run_id': run_id}


def binding_for_session(session: dict, run_id: str) -> dict:
    return {'kind': 'WEEKLY_SESSION', 'session_id': session['session_id'], 'session_digest': record_digest(session),
            'run_id': run_id}


DIAGNOSTIC = {'kind': 'OWNER_DIAGNOSTIC'}
