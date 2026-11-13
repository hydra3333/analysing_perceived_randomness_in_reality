"""MHUP-A: the value-free owner records, markers and tickets the gates read (design v0.1r5 sections 3.4, 4.2,
5.2, 6.1, 6.5 and Appendix J).

Orchestration-only, read-only. Nothing here reads a master, a ledger row's draws or any outcome: every record
read is value-free (identities, digests, times, statements). Every function takes the root it reads under
(the project root or a synthetic workspace); production callers pass their fixed module constants, never a
caller-supplied path (E2RC2-B01). Writers of these records arrive with later packages (Method_Mode_H.py, the
Mode H batch kind, the weekly programs); this module is their shared contract, so that a record a writer
produces is exactly what the gates accept.

Records and where they live (relative to the root):
  source_data/HOLDOUT_OPENED_<GAME>.json                       HOLDOUT_OPENED_V1, the opening record (4.2)
  source_data/DEVELOPED_<GAME>.json                            DEVELOPED_V1, the owner's GOAL-1 record (6.7)
  results/real/holdout/<GAME>/MODE_H_STUDY_MANIFEST_V1.json    the study manifest (4.1); only its SHA-256 is read here
  results/real/holdout/<GAME>/MODE_H_BATCH_ID.json             MODE_H_BATCH_ID_V1, the game's one plan (5.1)
  results/real/holdout/wf_batches/<GAME>/<batch_id>/plan.json  MODE_H_BATCH_PLAN_V1 (5.1)
  results/real/holdout/wf_batches/<GAME>/<batch_id>/attempts.jsonl   TICKET_V1 lines (3.4)
  results/real/holdout/wf_batches/<GAME>/<batch_id>/<MARKER>.json    the lifecycle markers (5.2)
  results/real/weekly/<GAME>/sessions/SESSION_<id>.json         SESSION_V1 (6.1)
  results/real/weekly/<GAME>/sessions/SESSION_<id>_attempts.jsonl    TICKET_V1 lines
  results/real/weekly/<GAME>/FORECAST_LEDGER_V1.jsonl           freeze lines (6.5); only the target is read here
  results/real/diagnostic/contract_runs/                        the diagnostic root (3.4), never read by any scorer
  src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt    barrier P (Appendix J)
"""
from __future__ import annotations

from collections.abc import Mapping
import hashlib
import json
from pathlib import Path
import re

from _common.contract_records import canonical, record_digest
import _common.contract_vocab as V
from _common.game_profiles import get_profile

OPENING_SCHEMA = 'HOLDOUT_OPENED_V1'
DEVELOPED_SCHEMA = 'DEVELOPED_V1'
STUDY_MANIFEST_SCHEMA = 'MODE_H_STUDY_MANIFEST_V1'
BATCH_ID_SCHEMA = 'MODE_H_BATCH_ID_V1'
MODE_H_PLAN_SCHEMA = 'MODE_H_BATCH_PLAN_V1'
SESSION_SCHEMA = 'SESSION_V1'
TICKET_SCHEMA = 'TICKET_V1'
FREEZE_LINE_SCHEMA = 'FREEZE_LINE_V1'
LIFECYCLE_MARKERS = ('BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE', 'MODE_H_SEALED')
SEAL = 'MODE_H_SEALED'
TICKET_KINDS = frozenset(('OPEN', 'DONE', 'FAILED_TO_START', 'SET_STARTED', 'RESUMED'))
BARRIER_NAME = 'INSTALL_IN_PROGRESS.txt'
BATCH_ID = re.compile(r'wf-[0-9a-f]{32}\Z', re.ASCII)
SESSION_ID = re.compile(r'[0-9a-f]{32}\Z', re.ASCII)
_SHA = V.SHA256
_UTC = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z\Z', re.ASCII)


class RecordRefused(ValueError):
    """A record is absent, unreadable or invalid; the caller refuses."""


# ---------------------------------------------------------------- paths (fixed layout under a root)

def opening_record_path(root: Path, game_id: str) -> Path:
    return Path(root) / 'source_data' / f'HOLDOUT_OPENED_{game_id}.json'


def developed_record_path(root: Path, game_id: str) -> Path:
    return Path(root) / 'source_data' / f'DEVELOPED_{game_id}.json'


def holdout_root(root: Path, game_id: str) -> Path:
    return Path(root) / 'results' / 'real' / 'holdout' / game_id


def study_manifest_path(root: Path, game_id: str) -> Path:
    return holdout_root(root, game_id) / f'{STUDY_MANIFEST_SCHEMA}.json'


def batch_id_record_path(root: Path, game_id: str) -> Path:
    return holdout_root(root, game_id) / 'MODE_H_BATCH_ID.json'


def mode_h_batch_folder(root: Path, game_id: str, batch_id: str) -> Path:
    return Path(root) / 'results' / 'real' / 'holdout' / 'wf_batches' / game_id / batch_id


def mode_h_runs_root(root: Path) -> Path:
    return Path(root) / 'results' / 'real' / 'holdout' / 'contract_runs'


def diagnostic_runs_root(root: Path) -> Path:
    return Path(root) / 'results' / 'real' / 'diagnostic' / 'contract_runs'


def weekly_root(root: Path, game_id: str) -> Path:
    return Path(root) / 'results' / 'real' / 'weekly' / game_id


def weekly_runs_root(root: Path) -> Path:
    return Path(root) / 'results' / 'real' / 'weekly' / 'contract_runs'


def session_record_path(root: Path, game_id: str, session_id: str) -> Path:
    return weekly_root(root, game_id) / 'sessions' / f'SESSION_{session_id}.json'


def session_attempts_path(root: Path, game_id: str, session_id: str) -> Path:
    return weekly_root(root, game_id) / 'sessions' / f'SESSION_{session_id}_attempts.jsonl'


def forecast_ledger_path(root: Path, game_id: str) -> Path:
    return weekly_root(root, game_id) / 'FORECAST_LEDGER_V1.jsonl'


def barrier_path(data_root: Path) -> Path:
    return Path(data_root) / BARRIER_NAME


# ---------------------------------------------------------------- small readers

def _plain_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def absent(path: Path) -> bool:
    """True only when nothing at all is at `path`: no file, no folder, no symlink (dangling or not). An optional record
    or ledger is 'not yet created' only in this state; anything present that is not a plain file refuses (EX_142 B02:
    present-but-invalid evidence is never read as absence)."""
    return not path.exists() and not path.is_symlink()


def _read_json(path: Path, what: str) -> dict:
    if not _plain_file(path):
        raise RecordRefused(f'{what}: no plain file at {path.name}')
    try:
        rec = json.loads(path.read_bytes().decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        raise RecordRefused(f'{what}: not ASCII JSON') from None
    if type(rec) is not dict:
        raise RecordRefused(f'{what}: not an object')
    return rec


def _read_canonical_json(path: Path, what: str) -> dict:
    """A record that must be exactly its canonical bytes (plans, session records, batch-id records)."""
    rec = _read_json(path, what)
    if canonical(rec) != path.read_bytes():
        raise RecordRefused(f'{what}: file bytes are not the record\'s canonical bytes (altered?)')
    return rec


def file_sha256(path: Path) -> str:
    if not _plain_file(path):
        raise RecordRefused(f'no plain file at {path.name}')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _need(rec: Mapping, field: str, what: str):
    if field not in rec:
        raise RecordRefused(f'{what}: {field} is missing')
    return rec[field]


def _sha(rec: Mapping, field: str, what: str) -> str:
    v = _need(rec, field, what)
    if type(v) is not str or not _SHA.fullmatch(v):
        raise RecordRefused(f'{what}: {field} is not 64 lower-case hex digits')
    return v


def _text(rec: Mapping, field: str, what: str) -> str:
    v = _need(rec, field, what)
    if type(v) is not str or not v.strip():
        raise RecordRefused(f'{what}: {field} is empty')
    return v


# ---------------------------------------------------------------- the opening record (4.2)

def validate_opening_record(rec: Mapping, game_id: str, what: str = 'opening record') -> dict:
    """The updater's field checks (results_master lines 135-150) plus the two freeze fields; extra fields are
    accepted as the updater accepts them. Returns the record."""
    get_profile(game_id)
    if type(rec) is not dict or rec.get('schema') != OPENING_SCHEMA:
        raise RecordRefused(f'{what}: schema is not {OPENING_SCHEMA}')
    if rec.get('game') != game_id:
        raise RecordRefused(f'{what}: game is not {game_id}')
    _sha(rec, 'study_manifest_sha256', what)
    _text(rec, 'opened_utc', what)
    _text(rec, 'owner_statement', what)
    fv = _need(rec, 'freeze_version', what)
    if type(fv) is not int or fv < 1:
        raise RecordRefused(f'{what}: freeze_version is not a positive whole number')
    _sha(rec, 'freeze_master_sha256', what)
    return dict(rec)


def opening_record(root: Path, game_id: str) -> dict | None:
    """The game's valid opening record, with its study manifest present and matching, or None if there is no
    record at all. An invalid record, or a record whose manifest is missing or altered, refuses."""
    path = opening_record_path(root, game_id)
    if absent(path):
        return None
    rec = validate_opening_record(_read_json(path, 'opening record'), game_id)
    manifest = study_manifest_path(root, game_id)
    if file_sha256(manifest) != rec['study_manifest_sha256']:
        raise RecordRefused('opening record: the study manifest does not have the SHA-256 the record names')
    return rec


def holdout_opened(root: Path, game_id: str) -> bool:
    return opening_record(root, game_id) is not None


# ---------------------------------------------------------------- the developed record (6.7)

def validate_developed_record(rec: Mapping, game_id: str, what: str = 'developed record') -> dict:
    get_profile(game_id)
    if type(rec) is not dict or rec.get('schema') != DEVELOPED_SCHEMA:
        raise RecordRefused(f'{what}: schema is not {DEVELOPED_SCHEMA}')
    if rec.get('game') != game_id:
        raise RecordRefused(f'{what}: game is not {game_id}')
    _text(rec, 'declared_utc', what)
    _text(rec, 'owner_statement', what)
    _sha(rec, 'mode_h_score_digest', what)
    return dict(rec)


def developed_record(root: Path, game_id: str) -> dict | None:
    path = developed_record_path(root, game_id)
    if absent(path):
        return None
    return validate_developed_record(_read_json(path, 'developed record'), game_id)


# ---------------------------------------------------------------- Mode H: the one plan, its markers (5.1, 5.2)

def batch_id_record(root: Path, game_id: str) -> dict | None:
    path = batch_id_record_path(root, game_id)
    if absent(path):
        return None
    rec = _read_canonical_json(path, 'batch-id record')
    if rec.get('schema') != BATCH_ID_SCHEMA or rec.get('game_id') != game_id:
        raise RecordRefused('batch-id record: wrong schema or game')
    bid = rec.get('batch_id')
    if type(bid) is not str or not BATCH_ID.fullmatch(bid):
        raise RecordRefused('batch-id record: invalid batch_id')
    return rec


def mode_h_plan(root: Path, game_id: str, batch_id: str) -> dict:
    """The game's one Mode H plan, if `batch_id` is the one the batch-id record names."""
    if type(batch_id) is not str or not BATCH_ID.fullmatch(batch_id):
        raise RecordRefused('invalid Mode H batch id')
    rec = batch_id_record(root, game_id)
    if rec is None or rec['batch_id'] != batch_id:
        raise RecordRefused('this batch is not the game\'s one Mode H plan')
    plan = _read_canonical_json(mode_h_batch_folder(root, game_id, batch_id) / 'plan.json', 'Mode H plan')
    if plan.get('schema') != MODE_H_PLAN_SCHEMA or plan.get('batch_id') != batch_id or plan.get('game_id') != game_id:
        raise RecordRefused('Mode H plan: wrong schema, batch or game')
    if type(plan.get('cohort')) is not list or type(plan.get('targets')) is not list:
        raise RecordRefused('Mode H plan: cohort or targets missing')
    pin_of(plan, 'Mode H plan')
    _sha(plan, 'study_manifest_sha256', 'Mode H plan')
    return plan


def pin_of(rec: Mapping, what: str) -> tuple[int, str]:
    """The master version a plan or session record froze: (`ledger_version`, `master_sha256`), both required and
    well-formed (EX_142 B01). Every official publication must pin exactly this and the ledger's current last row."""
    v = _need(rec, 'ledger_version', what)
    if type(v) is not int or v < 1:
        raise RecordRefused(f'{what}: ledger_version is not a positive whole number')
    return v, _sha(rec, 'master_sha256', what)


def plan_lists_pair(plan: Mapping, method_id: str, method_revision: str, variant_id: str, target: int) -> bool:
    members = plan.get('cohort') or []
    return (target in plan.get('targets', []) and
            any(type(m) is dict and (m.get('method_id'), m.get('method_revision'), m.get('variant_id')) ==
                (method_id, method_revision, variant_id) for m in members))


def lifecycle_markers_present(root: Path, game_id: str, batch_id: str) -> list[str]:
    """The batch's lifecycle markers that exist as plain files. A marker name that exists as anything else (a symlink,
    a folder) refuses (EX_142 B02): it can neither close the batch nor stand as the seal."""
    folder = mode_h_batch_folder(root, game_id, batch_id)
    out = []
    for m in LIFECYCLE_MARKERS:
        path = folder / f'{m}.json'
        if absent(path):
            continue
        if not _plain_file(path):
            raise RecordRefused(f'lifecycle marker {m} exists but is not a plain file')
        out.append(m)
    return out


def mode_h_sealed(root: Path, game_id: str) -> bool:
    """True only if the game's one Mode H batch carries the seal."""
    rec = batch_id_record(root, game_id)
    if rec is None:
        return False
    return SEAL in lifecycle_markers_present(root, game_id, rec['batch_id'])


# ---------------------------------------------------------------- tickets (3.4)

def read_jsonl(path: Path) -> tuple[list[dict], bool]:
    """Every complete JSON line of a ledger as a dict; a final line without its newline is ignored and reported
    (design 6.5's torn-last-line rule). Non-dict, undecodable or blank complete lines refuse (a newline-terminated
    blank line is not a torn fragment; EX_144 B02r1). A ledger that was never created, or exists empty, reads as
    empty; a path that exists but is not a plain file (a symlink, a folder) refuses (EX_142 B02)."""
    if absent(path):
        return [], False
    if not _plain_file(path):
        raise RecordRefused(f'{path.name}: exists but is not a plain file')
    raw = path.read_bytes()
    if not raw:
        return [], False                                  # an existing empty ledger: created, nothing written yet
    torn = not raw.endswith(b'\n')
    complete = raw[:raw.rfind(b'\n') + 1] if torn else raw    # every newline-terminated line; the fragment left out
    out = []
    for line in complete.split(b'\n')[:-1]:
        if not line:
            raise RecordRefused(f'{path.name}: a blank complete line (never written by a ledger writer)')   # EX_144 B02r1
        try:
            rec = json.loads(line.decode('ascii'))
        except (ValueError, UnicodeDecodeError):
            raise RecordRefused(f'{path.name}: an undecodable complete line') from None
        if type(rec) is not dict:
            raise RecordRefused(f'{path.name}: a line that is not an object')
        out.append(rec)
    return out, torn


def ticket(kind: str, *, scope_kind: str, scope_id: str, game_id: str, method_id, variant_id, method_revision,
           target_draw_number, run_id, utc: str, request_digest: str | None = None,
           terminal_class: str | None = None, extra: Mapping | None = None) -> dict:
    """The one shape of a TICKET_V1 line (shared by the writers that come later). Canonical bytes, with newline."""
    if kind not in TICKET_KINDS:
        raise ValueError(f'unknown ticket kind {kind!r}')
    t = {'schema': TICKET_SCHEMA, 'kind': kind, 'scope_kind': scope_kind, 'scope_id': scope_id, 'game_id': game_id,
         'method_id': method_id, 'variant_id': variant_id, 'method_revision': method_revision,
         'target_draw_number': target_draw_number, 'run_id': run_id, 'utc': utc,
         'request_digest': request_digest, 'terminal_class': terminal_class}
    if extra:
        t.update(extra)
    return t


def validate_ticket(t: Mapping, *, scope_kind: str, scope_id: str, game_id: str) -> dict:
    what = 'ticket'
    if type(t) is not dict or t.get('schema') != TICKET_SCHEMA:
        raise RecordRefused(f'{what}: schema is not {TICKET_SCHEMA}')
    if t.get('kind') not in TICKET_KINDS:
        raise RecordRefused(f'{what}: unknown kind')
    if (t.get('scope_kind'), t.get('scope_id'), t.get('game_id')) != (scope_kind, scope_id, game_id):
        raise RecordRefused(f'{what}: belongs to another scope or game')
    if type(t.get('utc')) is not str or not _UTC.fullmatch(t['utc']):
        raise RecordRefused(f'{what}: utc is not a UTC instant')
    if t['kind'] in ('OPEN', 'DONE', 'FAILED_TO_START'):
        if (type(t.get('method_id')) is not str or type(t.get('variant_id')) is not str or
                type(t.get('method_revision')) is not str or type(t.get('target_draw_number')) is not int or
                type(t.get('run_id')) is not str or not V.RUN_ID.fullmatch(t['run_id'])):
            raise RecordRefused(f'{what}: {t["kind"]} ticket lacks its pair or run id')
        if t['kind'] == 'OPEN' and (type(t.get('request_digest')) is not str or not _SHA.fullmatch(t['request_digest'])):
            raise RecordRefused(f'{what}: OPEN ticket lacks its request digest')
    return dict(t)


def tickets(path: Path, *, scope_kind: str, scope_id: str, game_id: str) -> list[dict]:
    rows, _torn = read_jsonl(path)
    return [validate_ticket(t, scope_kind=scope_kind, scope_id=scope_id, game_id=game_id) for t in rows]


def pair_of(t: Mapping) -> tuple:
    return (t.get('method_id'), t.get('method_revision'), t.get('variant_id'), t.get('target_draw_number'))


def open_ticket_for(ticket_rows, *, run_id: str, pair: tuple, request_digest: str) -> bool:
    """An OPEN ticket for this run id and pair, naming this exact request, that no later FAILED_TO_START or DONE
    ticket for the same run id has closed."""
    opened = closed = False
    for t in ticket_rows:
        if t['kind'] == 'OPEN' and t['run_id'] == run_id and pair_of(t) == pair and t['request_digest'] == request_digest:
            opened = True
        elif t['kind'] in ('DONE', 'FAILED_TO_START') and t['run_id'] == run_id:
            closed = True
    return opened and not closed


def pair_has_done_ticket(ticket_rows, pair: tuple) -> bool:
    return any(t['kind'] == 'DONE' and pair_of(t) == pair for t in ticket_rows)


# ---------------------------------------------------------------- weekly sessions (6.1) and the forecast ledger (6.5)

def session_record(root: Path, game_id: str, session_id: str) -> dict:
    if type(session_id) is not str or not SESSION_ID.fullmatch(session_id):
        raise RecordRefused('invalid session id')
    rec = _read_canonical_json(session_record_path(root, game_id, session_id), 'session record')
    if rec.get('schema') != SESSION_SCHEMA or rec.get('session_id') != session_id or rec.get('game_id') != game_id:
        raise RecordRefused('session record: wrong schema, session or game')
    if type(rec.get('roster')) is not list:
        raise RecordRefused('session record: roster missing')
    pin_of(rec, 'session record')
    return rec


def roster_entry(session: Mapping, method_id: str, method_revision: str, variant_id: str) -> dict | None:
    for m in session.get('roster', []):
        if type(m) is dict and (m.get('method_id'), m.get('method_revision'), m.get('variant_id')) == (
                method_id, method_revision, variant_id):
            return m
    return None


def release_date_of(member: Mapping):
    """The roster entry's release date (the release record's local date, design 4.3), as a date."""
    from datetime import date
    v = member.get('release_date')
    try:
        d = date.fromisoformat(v)
    except (TypeError, ValueError):
        raise RecordRefused('roster entry: release_date is not an ISO date') from None
    if d.isoformat() != v:
        raise RecordRefused('roster entry: release_date is not an ISO date')
    return d


def all_session_attempt_paths(root: Path, game_id: str) -> list[Path]:
    """Every session attempts ledger of the game, by name. Nothing is filtered: a name of that shape that is not a plain
    file refuses when it is read (EX_142 B02), so an invalid ledger can never read as 'no earlier DONE ticket'."""
    folder = weekly_root(root, game_id) / 'sessions'
    if absent(folder):
        return []
    if folder.is_symlink() or not folder.is_dir():
        raise RecordRefused('the sessions folder exists but is not a plain folder')
    return sorted(folder.glob('SESSION_*_attempts.jsonl'))


def session_id_of_attempts_path(path: Path) -> str:
    return path.name[len('SESSION_'):-len('_attempts.jsonl')]


def pair_done_in_any_session(root: Path, game_id: str, pair: tuple) -> bool:
    for path in all_session_attempt_paths(root, game_id):
        sid = session_id_of_attempts_path(path)
        if pair_has_done_ticket(tickets(path, scope_kind='WEEKLY_SESSION', scope_id=sid, game_id=game_id), pair):
            return True
    return False


FORECAST_LEDGER_SCHEMAS = frozenset((FREEZE_LINE_SCHEMA,))     # slice 2 adds the score, witness and amendment lines


def forecast_ledger_lines(root: Path, game_id: str) -> list[dict]:
    """Every complete line of the game's forecast ledger (6.5), each of a known schema with a whole-number target;
    anything else refuses (EX_142 B02: an unknown or malformed line is never read as 'no freeze line')."""
    rows, _torn = read_jsonl(forecast_ledger_path(root, game_id))
    for r in rows:
        if r.get('schema') not in FORECAST_LEDGER_SCHEMAS:
            raise RecordRefused('forecast ledger: a line of an unknown schema')
        if type(r.get('target_draw_number')) is not int:
            raise RecordRefused('forecast ledger: a line without a whole-number target')
    return rows


def freeze_line_exists(root: Path, game_id: str, target: int) -> bool:
    return any(r['schema'] == FREEZE_LINE_SCHEMA and r['target_draw_number'] == target
               for r in forecast_ledger_lines(root, game_id))


def record_sha(rec: Mapping) -> str:
    return record_digest(rec)


# ================================================================ MHUP-A slice 2: the writers' shared contract
#
# The study manifest (4.1), the study version advance (4.1), the lifecycle markers' contents (5.2), the Mode H
# scores root, the locks (6.1, Appendix J), the exposure flags (5.4) and the create-only writer every Mode H record
# goes through. Still orchestration-only and value-free: no draw, no outcome.

ADVANCE_SCHEMA = 'STUDY_VERSION_ADVANCE_V1'
MARKER_SCHEMAS = {m: f'{m}_V1' for m in LIFECYCLE_MARKERS}
RESUME_TOKEN_SCHEMA = 'RESUME_TOKEN_V1'
CLEARANCE_SCHEMA = 'LOCK_CLEARANCE_V1'
SESSION_LOCK_NAME = 'ACTIVE_SESSION.lock'
UPDATER_LOCK_NAME = '.results_master.lock'
# The owner's exposure decisions (HOLDOUT_EXPOSURE_RECORD_v0_3 item 1): draws whose published results the owner may
# have seen before the holdout opened. Information only; flagged draws are scored and counted like any other (5.4).
EXPOSURE_RECORD = 'HOLDOUT_EXPOSURE_RECORD_v0_3'
EXPOSED_DRAWS = {'POWERBALL': {1585: 'HX-1', 1586: 'HX-1', 1587: 'HX-2', 1588: 'HX-2'}, 'OZLOTTO': {}}
OPENING_STATEMENT = 'I open the holdout of this game for the sealed Mode H study; the study manifest is frozen.'
DEVELOPED_STATEMENT = 'I declare this game\'s system developed (GOAL-1); the weekly session may begin.'
ADVANCE_STATEMENT = 'I advance the admitted study version after written agreement from Claude and the reviewer.'


def advance_record_path(root: Path, game_id: str) -> Path:
    return holdout_root(root, game_id) / f'STUDY_VERSION_ADVANCE_{game_id}_V1.json'


def mode_h_scores_root(root: Path) -> Path:
    return Path(root) / 'results' / 'real' / 'holdout' / 'scores'


def session_lock_path(root: Path, game_id: str) -> Path:
    return weekly_root(root, game_id) / SESSION_LOCK_NAME


def updater_lock_path(root: Path) -> Path:
    return Path(root) / 'source_data' / UPDATER_LOCK_NAME


def marker_path(root: Path, game_id: str, batch_id: str, marker: str) -> Path:
    if marker not in LIFECYCLE_MARKERS:
        raise ValueError(f'unknown lifecycle marker {marker!r}')
    return mode_h_batch_folder(root, game_id, batch_id) / f'{marker}.json'


def write_record(path: Path, rec: Mapping) -> bytes:
    """Create-only publication of a value-free record as its canonical bytes (the one way every Mode H record is
    written; contract_publication.create_only never overwrites). Returns the bytes written."""
    from _common.contract_publication import create_only
    raw = canonical(rec)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    create_only(Path(path), raw)
    return raw


def exposure_flag(game_id: str, target: int) -> dict | None:
    decision = EXPOSED_DRAWS.get(game_id, {}).get(target)
    return None if decision is None else {'record': EXPOSURE_RECORD, 'decision': decision}


# ---------------------------------------------------------------- the study manifest (4.1, Appendix H)

_MANIFEST_FIELDS = ('schema', 'game_id', 'frozen_utc', 'cohort', 'not_runnable', 'targets', 'exposure', 'measures',
                    'families', 'n1_policy_id', 'evaluator_version', 'freeze_version', 'freeze_master_sha256',
                    'admission_rule', 'closure', 'environment', 'excluded', 'not_frozen', 'tool', 'tool_version')


def validate_study_manifest(rec: Mapping, game_id: str, what: str = 'study manifest') -> dict:
    """The manifest's shape (its closure and environment inventories are checked by _common.closure)."""
    p = get_profile(game_id)
    if type(rec) is not dict or rec.get('schema') != STUDY_MANIFEST_SCHEMA:
        raise RecordRefused(f'{what}: schema is not {STUDY_MANIFEST_SCHEMA}')
    if set(rec) != set(_MANIFEST_FIELDS):
        raise RecordRefused(f'{what}: fields are not exactly the manifest\'s')
    if rec['game_id'] != game_id:
        raise RecordRefused(f'{what}: game is not {game_id}')
    if rec['targets'] != list(range(p.holdout_first, p.holdout_last + 1)):
        raise RecordRefused(f'{what}: targets are not the ten holdout draws')
    if type(rec['cohort']) is not list or not rec['cohort']:
        raise RecordRefused(f'{what}: cohort missing or empty')
    for m in rec['cohort']:
        if type(m) is not dict or not {'method_id', 'variant_id', 'method_revision', 'declaration_digest',
                                       'registry_entry_digest', 'minimum_history_draws'} <= set(m):
            raise RecordRefused(f'{what}: a cohort member lacks its identity')
    fv = rec['freeze_version']
    if type(fv) is not int or fv < 1:
        raise RecordRefused(f'{what}: freeze_version is not a positive whole number')
    _sha(rec, 'freeze_master_sha256', what)
    for k in ('closure', 'environment'):
        if type(rec[k]) is not dict or not _SHA.fullmatch(str(rec[k].get('digest', ''))):
            raise RecordRefused(f'{what}: {k} inventory lacks its digest')
    _text(rec, 'frozen_utc', what)
    return dict(rec)


def study_manifest(root: Path, game_id: str) -> dict | None:
    """The game's study manifest, validated, or None if absent. Its canonical bytes are the file's bytes."""
    path = study_manifest_path(root, game_id)
    if absent(path):
        return None
    return validate_study_manifest(_read_canonical_json(path, 'study manifest'), game_id)


def manifest_cohort_digest(manifest: Mapping) -> str:
    return hashlib.sha256(canonical({'cohort': manifest['cohort']})).hexdigest()


# ---------------------------------------------------------------- the study version advance (4.1)

def validate_advance_record(rec: Mapping, game_id: str, what: str = 'study version advance') -> dict:
    if type(rec) is not dict or rec.get('schema') != ADVANCE_SCHEMA:
        raise RecordRefused(f'{what}: schema is not {ADVANCE_SCHEMA}')
    if rec.get('game_id') != game_id:
        raise RecordRefused(f'{what}: game is not {game_id}')
    rows = rec.get('rows_beyond_admitted')
    if type(rows) is not list or not rows:
        raise RecordRefused(f'{what}: no rows named')
    for r in rows:
        if (type(r) is not dict or type(r.get('version')) is not int or r.get('action') not in ('UPDATE', 'NO_CHANGE')
                or not _SHA.fullmatch(str(r.get('master_sha256', '')))):
            raise RecordRefused(f'{what}: a named row lacks version, action or master_sha256')
    v = rec.get('admitted_version_after')
    if type(v) is not int or v != rows[-1]['version']:
        raise RecordRefused(f'{what}: admitted_version_after is not the last named row')
    _text(rec, 'owner_statement', what)
    _text(rec, 'advanced_utc', what)
    _sha(rec, 'study_manifest_sha256', what)
    return dict(rec)


def advance_record(root: Path, game_id: str) -> dict | None:
    path = advance_record_path(root, game_id)
    if absent(path):
        return None
    return validate_advance_record(_read_canonical_json(path, 'study version advance'), game_id)


def admitted_version(opening: Mapping, advance: Mapping | None, ledger_rows) -> int:
    """v_a (design 4.1): freeze_version + 1; or v_a' when a study version advance names exactly the ledger rows
    beyond v_a, by version, action and master_sha256. Anything else refuses. `ledger_rows` are
    master_versions.LedgerRow values of the verified ledger."""
    v_a = opening['freeze_version'] + 1
    if advance is None:
        return v_a
    beyond = [(r.version, r.action, r.master_sha256) for r in ledger_rows if r.version > v_a]
    named = [(r['version'], r['action'], r['master_sha256']) for r in advance['rows_beyond_admitted']]
    if named != beyond:
        raise RecordRefused('the study version advance does not name exactly the ledger rows beyond the admitted version')
    return advance['admitted_version_after']


# ---------------------------------------------------------------- the lifecycle markers' contents (5.2)

def validate_marker(rec: Mapping, marker: str, batch_id: str, what: str | None = None) -> dict:
    what = what or f'{marker} marker'
    if type(rec) is not dict or rec.get('schema') != MARKER_SCHEMAS[marker]:
        raise RecordRefused(f'{what}: schema is not {MARKER_SCHEMAS[marker]}')
    if rec.get('batch_id') != batch_id:
        raise RecordRefused(f'{what}: names another batch')
    _text(rec, 'utc', what)
    _sha(rec, 'plan_digest', what)
    if marker == 'BATCH_COMPLETE':
        if type(rec.get('pairs')) is not int or rec['pairs'] < 1:
            raise RecordRefused(f'{what}: pairs is not a positive whole number')
    if marker in ('SCORING_STARTED', 'MODE_H_SEALED'):
        _text(rec, 'attempt_id', what)
    if marker == 'SCORING_STARTED':
        _sha(rec, 'roster_digest', what)
    if marker in ('SCORE_COMPLETE', 'MODE_H_SEALED'):
        _sha(rec, 'score_ledger_sha256', what)
    if marker == 'MODE_H_SEALED':
        _sha(rec, 'report_sha256', what)
    return dict(rec)


def marker(root: Path, game_id: str, batch_id: str, name: str) -> dict | None:
    """A lifecycle marker's validated content, or None if absent; present-but-invalid refuses."""
    path = marker_path(root, game_id, batch_id, name)
    if absent(path):
        return None
    return validate_marker(_read_canonical_json(path, f'{name} marker'), name, batch_id)


def write_marker(root: Path, game_id: str, batch_id: str, name: str, rec: Mapping) -> bytes:
    """Write one lifecycle marker, create-only, in the design's order: each marker needs the one before it."""
    order = LIFECYCLE_MARKERS.index(name)
    present = lifecycle_markers_present(root, game_id, batch_id)
    if any(LIFECYCLE_MARKERS.index(m) >= order for m in present):
        raise RecordRefused(f'{name}: a marker at or after it already exists ({", ".join(present)})')
    if order > 0 and LIFECYCLE_MARKERS[order - 1] not in present:
        raise RecordRefused(f'{name}: the marker before it ({LIFECYCLE_MARKERS[order - 1]}) does not exist')
    return write_record(marker_path(root, game_id, batch_id, name), validate_marker(rec, name, batch_id))


def roster_digest(root: Path, game_id: str, plan: Mapping) -> str:
    """The exact roster the scorer scores (design 5.3): every planned (method, revision, variant, target) with the
    run id of its DONE ticket, from the batch's attempts ledger, sorted; refuses if any planned pair lacks a DONE
    ticket or has more than one. Computed from the records alone, the same way by the reader and the scorer."""
    rows = tickets(mode_h_batch_folder(root, game_id, plan['batch_id']) / 'attempts.jsonl',
                   scope_kind='MODE_H_BATCH', scope_id=plan['batch_id'], game_id=game_id)
    done = {}
    for t in rows:
        if t['kind'] == 'DONE':
            done.setdefault(pair_of(t), []).append(t['run_id'])
    roster = []
    for m in plan['cohort']:
        for target in plan['targets']:
            pair = (m['method_id'], m['method_revision'], m['variant_id'], target)
            ids = done.get(pair, [])
            if len(ids) != 1:
                raise RecordRefused(f'pair {pair} has {len(ids)} DONE tickets; exactly one is the roster\'s')
            roster.append([*pair, ids[0]])
    return hashlib.sha256(canonical({'roster': roster})).hexdigest()
