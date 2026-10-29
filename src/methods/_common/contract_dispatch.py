"""E_2-readiness contract (E2R-1 v0.3r3): the dispatch gate (section 12A.3, E2R-R57, E2R-T14).

E2R-CODE-2. One gate for every normal dispatch, standalone or coordinated. It reads only the installed
contract data and the method folder's IN_DEVELOPMENT.txt flag; it never reads a master, ledger or any
draw data, so a refused request has read no data (E2R-R23A). It always loads the installed registry
afresh and returns fresh copies of the active entry and its declaration (reviewer's EX_036 watchpoint):
a caller's own copy is never trusted. Admission is not authorisation for a scientific run; every
other safety, environment, data-admission and owner gate stays separate (E2R-R57 item 3).
"""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import _common.contract_vocab as V
from _common.contract_records import record_digest, validate_run_request
from _common.contract_registry import InstalledRegistry

METHODS_ROOT = Path(__file__).resolve().parents[1]      # src/methods
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
    return _admit(ident, pinned_entry=request['registry_entry_digest'],
                  pinned_declaration=request['declaration_digest'])


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
