"""E_2-readiness contract (E2R-1 v0.3r3): the dispatch gate (section 12A.3, E2R-R57, E2R-T14).

E2R-CODE-2. One gate for every normal dispatch, standalone or coordinated. It reads only the installed
contract data, the method folder's IN_DEVELOPMENT.txt flag and, since MHUP-A, the value-free owner records,
plans, tickets and markers a real-mode request's binding names (design v0.1r5 section 3.4(b)); it never
reads a master, ledger or any draw data, so a refused request has read no data (E2R-R23A). It always loads
the installed registry afresh and returns fresh copies of the active entry and its declaration (reviewer's
EX_036 watchpoint): a caller's own copy is never trusted. Admission is not authorisation for a scientific
run; every other safety, environment, data-admission and owner gate stays separate (E2R-R57 item 3).

MHUP-A adds two things, both at fixed roots no caller can choose (E2RC2-B01):
- barrier P, src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt (Appendix J): while it exists every
  dispatch-gated run refuses, like the orphan marker;
- publication admission for a bound request: a Mode H binding must name the game's one plan with its digest,
  tied to the opening record's study manifest and frozen at the admitted version v_a, listing this exact pair,
  with the request pinning exactly the plan's frozen (ledger_version, master_sha256), an open ticket for this
  run id, no DONE ticket for the pair and no lifecycle marker; a session binding must name an existing session
  record with its digest listing this variant, with the request pinning exactly the session's frozen version,
  an open ticket, no DONE ticket for the pair in any session's ledger of the game, no freeze line for the
  target, the developed record, and a mode that agrees with the variant's release date; the diagnostic binding
  admits REAL_DEVELOPMENT only and, for a holdout or later target, only with the opening record and the game's
  seal. The runner adds the second half of the pin rule after the reader: the pin must also be the ledger's
  current last row (STALE_PIN). Every record the gate reads fails closed: a record, ledger or marker that exists
  but is not a plain file, or a ledger line of an unknown shape, refuses rather than reading as absent (EX_142
  B01, B02). A request that needs a binding and has none refuses before anything is read.
"""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import _common.contract_vocab as V
from _common.contract_records import binding_kind, record_digest, validate_run_request
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import get_profile
from _common import owner_records as OR

METHODS_ROOT = Path(__file__).resolve().parents[1]      # src/methods
PROJECT_ROOT = Path(__file__).resolve().parents[3]      # the fixed root the owner records are read under
FLAG_NAME = 'IN_DEVELOPMENT.txt'


class DispatchRefused(Exception):
    """A refused dispatch. `text` is the one warning both launchers print; it names the method,
    the revision and the reason, and contains no data."""

    def __init__(self, text: str, reason: str):
        super().__init__(text)
        self.text = text
        self.reason = reason


def method_folder(method_id: str) -> str:
    """The locator-only folder for a method ID (E2R-R53, reviewer's ADD-C07): E_2 -> E_002."""
    if type(method_id) is not str or not V.METHOD_ID.fullmatch(method_id):
        raise ValueError('invalid method ID')
    return f'E_{int(method_id[2:]):03d}'


def refusal_text(game_id, method_id, variant_id, revision, reason: str) -> str:
    def show(v):
        return v if type(v) is str and v.isascii() and v.isprintable() and len(v) <= 96 else '?'
    return (f'DISPATCH REFUSED: {show(game_id)} {show(method_id)} {show(variant_id)} revision '
            f'{show(revision)}: {reason}. No data was read.')


def _roots() -> tuple[Path, Path]:
    """The installed registry and the method folders. No caller can choose them (reviewer's
    E2RC2-CODE-B01): they are the fixed module constants, read at call time; only a test harness
    patches those constants, in-process, for its temporary copies."""
    import _common.contract_registry as R
    return Path(R.DATA_ROOT), Path(METHODS_ROOT)


def _admit(ident, *, pinned_entry, pinned_declaration) -> tuple[dict, dict]:
    game, method, variant, revision = ident

    def refuse(code, detail):
        raise DispatchRefused(refusal_text(*ident, f'{code}: {detail}'), code)

    data_root, methods_root = _roots()
    barrier = OR.barrier_path(data_root)
    if barrier.exists() or barrier.is_symlink():      # Appendix J: barrier P stops every dispatch-gated run, legacy too
        refuse('INSTALL_IN_PROGRESS', f'{OR.BARRIER_NAME} exists; an install is in progress and no dispatch-gated run '
                                      'is admitted')
    try:
        registry = InstalledRegistry(data_root)      # fresh every call, never a cached or caller copy
    except (ValueError, OSError) as exc:
        refuse('REGISTRY_INVALID', f'the installed registry did not load ({type(exc).__name__})')
    try:
        entry = registry.active_entry(game, method, variant)
    except ValueError:
        refuse('NO_REGISTRY_ENTRY', 'no installed registry chain for this game, method and variant')
    if entry['registry_status'] != 'SUPPORTED':
        refuse('NOT_SUPPORTED', f'the active registry entry is {entry["registry_status"]}')
    if pinned_entry is not None and pinned_entry != record_digest(entry):
        refuse('STALE_REGISTRY_ENTRY', 'the request does not pin the active registry entry')
    if entry['method_revision'] != revision:
        refuse('REVISION_MISMATCH', f'the active entry approves revision {entry["method_revision"]}')
    if pinned_declaration is not None and entry['declaration_digest'] != pinned_declaration:
        refuse('DECLARATION_MISMATCH', 'the request names a different declaration')
    flag = methods_root / method_folder(method) / FLAG_NAME
    if flag.exists() or flag.is_symlink():
        refuse('IN_DEVELOPMENT_FLAG_PRESENT', f'src/methods/{method_folder(method)}/{FLAG_NAME} exists')
    return entry, registry.declaration(entry['declaration_digest'])


def dispatch_gate(request: object) -> tuple[dict, dict]:
    """Admit a RUN_REQUEST_V1 or raise DispatchRefused. Returns (active_entry, declaration), both new
    caller-owned copies fetched from the installed registry by this call.

    Admitted only if all hold: the request is a valid stage-1 request; the installed registry has a
    chain for its (game, method, variant); the chain's active entry is SUPPORTED; the request pins
    exactly that active entry's digest; the entry's revision and declaration digest equal the
    request's; and there is no src/methods/E_<nnn>/IN_DEVELOPMENT.txt.
    """
    r = request if isinstance(request, Mapping) else {}
    ident = (r.get('game_id'), r.get('method_id'), r.get('variant_id'), r.get('method_revision'))
    try:
        validate_run_request(request)
    except ValueError as exc:
        raise DispatchRefused(refusal_text(*ident, f'INVALID_RUN_REQUEST: {exc}'), 'INVALID_RUN_REQUEST') from None
    entry, declaration = _admit(ident, pinned_entry=request['registry_entry_digest'],
                                pinned_declaration=request['declaration_digest'])
    _resolve_binding(request, ident)
    return entry, declaration


def _project_root() -> Path:
    """The fixed root the owner records, plans, tickets and markers are read under (patched only by a test harness)."""
    return Path(PROJECT_ROOT)


def _resolve_binding(request: Mapping, ident) -> None:
    """Design 3.4(b): publication admission for a bound request. Reads value-free records only, at fixed roots."""
    kind = binding_kind(request)
    if kind is None:
        return                                           # a request within today's rules carries no binding
    root = _project_root()
    game, method, variant, revision = ident
    mode, target, run_id = request['run_mode'], request['target_draw_number'], request['run_id']
    pair = (method, revision, variant, target)
    b = request['binding']

    def refuse(code, detail):
        raise DispatchRefused(refusal_text(*ident, f'{code}: {detail}'), code)

    pin = (request['ledger_version'], request['master_sha256'])
    try:
        if kind == 'MODE_H_BATCH':
            plan = OR.mode_h_plan(root, game, b['batch_id'])
            if record_digest(plan) != b['plan_digest']:
                refuse('BINDING_NOT_RESOLVED', 'the binding does not name the plan\'s digest')
            # The plan is tied to the ratified study (design 4.1, 5.1): the game's opening record must exist, the plan
            # must name the opening record's study manifest, and the plan's frozen version must be the admitted version
            # v_a = freeze_version + 1 (the study version advance of 4.1, which may move v_a, arrives with slice 2).
            opening = OR.opening_record(root, game)
            if opening is None:
                refuse('HOLDOUT_NOT_OPENED', 'a Mode H plan binding needs the game\'s opening record')
            if plan['study_manifest_sha256'] != opening['study_manifest_sha256']:
                refuse('PLAN_NOT_TIED_TO_STUDY', 'the plan does not name the opening record\'s study manifest')
            plan_pin = OR.pin_of(plan, 'Mode H plan')
            if plan_pin[0] != opening['freeze_version'] + 1:
                refuse('PLAN_VERSION_NOT_ADMITTED', 'the plan\'s frozen version is not the admitted version v_a')
            # EX_142 B01: the request pins exactly the version the plan froze (the runner separately requires that this
            # is also the ledger's current last row, STALE_PIN). With a study version advance (design 4.1), the one
            # other admissible pin is the advance's admitted version, tied to the same study manifest.
            admissible = {plan_pin}
            advance = OR.advance_record(root, game)
            if advance is not None:
                if advance['study_manifest_sha256'] != opening['study_manifest_sha256']:
                    refuse('PLAN_NOT_TIED_TO_STUDY', 'the study version advance does not name the opening record\'s manifest')
                last = advance['rows_beyond_admitted'][-1]
                admissible.add((last['version'], last['master_sha256']))
            if pin not in admissible:
                refuse('PIN_DISAGREES_WITH_PLAN', 'the request does not pin the master version the plan (or its study '
                                                  'version advance) froze')
            if not OR.plan_lists_pair(plan, method, revision, variant, target):
                refuse('PAIR_NOT_IN_PLAN', 'the plan does not list this method, revision, variant and target')
            markers = OR.lifecycle_markers_present(root, game, b['batch_id'])
            if markers:
                refuse('BATCH_CLOSED', f'lifecycle marker present: {", ".join(markers)}')
            rows = OR.tickets(OR.mode_h_batch_folder(root, game, b['batch_id']) / 'attempts.jsonl',
                              scope_kind='MODE_H_BATCH', scope_id=b['batch_id'], game_id=game)
            if OR.pair_has_done_ticket(rows, pair):
                refuse('PAIR_ALREADY_DONE', 'the pair has a DONE ticket; no second record')
            if not OR.open_ticket_for(rows, run_id=run_id, pair=pair, request_digest=record_digest(request)):
                refuse('NO_OPEN_TICKET', 'no open ticket names this run id, pair and request')
        elif kind == 'WEEKLY_SESSION':
            session = OR.session_record(root, game, b['session_id'])
            if record_digest(session) != b['session_digest']:
                refuse('BINDING_NOT_RESOLVED', 'the binding does not name the session record\'s digest')
            # EX_142 B01: the request pins exactly the version the session froze at open-session (design 6.1); the
            # runner separately requires that this is also the ledger's current last row (STALE_PIN).
            if pin != OR.pin_of(session, 'session record'):
                refuse('PIN_DISAGREES_WITH_SESSION', 'the request does not pin the master version the session froze')
            member = OR.roster_entry(session, method, revision, variant)
            if member is None:
                refuse('NOT_IN_SESSION_ROSTER', 'the session roster does not list this variant')
            if OR.developed_record(root, game) is None:
                refuse('NOT_DEVELOPED', 'no developed record for this game (GOAL-1)')
            if OR.freeze_line_exists(root, game, target):
                refuse('TARGET_FROZEN', 'the forecast ledger already has a freeze line for this target')
            if OR.pair_done_in_any_session(root, game, pair):
                refuse('PAIR_ALREADY_DONE', 'the pair has a DONE ticket in a session ledger of this game')
            rows = OR.tickets(OR.session_attempts_path(root, game, b['session_id']),
                              scope_kind='WEEKLY_SESSION', scope_id=b['session_id'], game_id=game)
            if not OR.open_ticket_for(rows, run_id=run_id, pair=pair, request_digest=record_digest(request)):
                refuse('NO_OPEN_TICKET', 'no open ticket names this run id, pair and request')
            try:
                released_before = OR.release_date_of(member) < get_profile(game).derived_date(target)
            except OR.RecordRefused as exc:
                refuse('BINDING_NOT_RESOLVED', str(exc))
            if mode == 'CATCH_UP' and not released_before:
                refuse('MODE_DISAGREES_WITH_RELEASE', 'CATCH_UP needs a release date before the target\'s draw date')
            if mode == 'REAL_DEVELOPMENT' and released_before:
                refuse('MODE_DISAGREES_WITH_RELEASE', 'a variant released before the draw gets CATCH_UP, not development')
        elif kind == 'OWNER_DIAGNOSTIC':
            if mode != 'REAL_DEVELOPMENT':
                refuse('DIAGNOSTIC_MODE', 'the diagnostic route admits REAL_DEVELOPMENT only')
            if target >= get_profile(game).holdout_first:
                if OR.opening_record(root, game) is None:
                    refuse('HOLDOUT_NOT_OPENED', 'a holdout or later diagnostic target needs the opening record')
                if not OR.mode_h_sealed(root, game):
                    refuse('MODE_H_NOT_SEALED', 'a holdout or later diagnostic target needs the game\'s Mode H seal')
    except OR.RecordRefused as exc:
        refuse('BINDING_NOT_RESOLVED', str(exc))


def legacy_gate(game_id: str, method_id: str, variant_id: str, revision: str) -> tuple[dict, dict]:
    """The same release rule for E_1's legacy standalone runner (owner decision D2-3, 29 October 2026),
    which has no RUN_REQUEST_V1 and so no pins: an active SUPPORTED entry for exactly this game, method,
    variant and revision, and no IN_DEVELOPMENT.txt. Same refusal codes and text; reads no data."""
    return _admit((game_id, method_id, variant_id, revision), pinned_entry=None, pinned_declaration=None)


def variant_released(game_id: str, method_id: str, variant_id: str) -> bool:
    """True only if this exact (game, method, variant) has an active SUPPORTED entry and the method has no
    IN_DEVELOPMENT.txt. For synthetic-only checks that have no run request; it is not an admission."""
    data_root, methods_root = _roots()
    try:
        entry = InstalledRegistry(data_root).active_entry(game_id, method_id, variant_id)
    except ValueError:
        return False
    flag = methods_root / method_folder(method_id) / FLAG_NAME
    return entry['registry_status'] == 'SUPPORTED' and not (flag.exists() or flag.is_symlink())


def active_pins(game_id: str, method_id: str, variant_id: str) -> dict:
    """What a request must pin for this method variant now (read from the installed registry only)."""
    entry = InstalledRegistry(_roots()[0]).active_entry(game_id, method_id, variant_id)
    return {'registry_status': entry['registry_status'], 'method_revision': entry['method_revision'],
            'declaration_digest': entry['declaration_digest'], 'registry_entry_digest': record_digest(entry)}
