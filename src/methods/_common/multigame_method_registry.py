"""Conservative scoped register: no structural or scientific method silently excluded.

E2R-CODE-2: the statuses are now read from the installed E_2-readiness contract registry
(src/methods/_common/contract_data/, loaded afresh on every call), so there is one record of status.
A method is SUPPORTED for a game when one of its variants has an active SUPPORTED entry for that game
and its folder has no IN_DEVELOPMENT.txt flag; UNSUPPORTED_FOR_GAME when every active entry says so;
otherwise FORMULA_OPEN. With today's installed data this gives exactly the earlier fixed roster:
E_1 SUPPORTED and E_2..E_62 FORMULA_OPEN in both games.
"""
from __future__ import annotations
from types import MappingProxyType

from _common.game_profiles import get_profile

SUPPORTED = 'SUPPORTED'
UNSUPPORTED = 'UNSUPPORTED_FOR_GAME'
OPEN = 'FORMULA_OPEN'
_METHODS = tuple(f'E_{i}' for i in range(1, 63))
# This is a scientific execution/support roster, NOT a view-entitlement list.
# The general-purpose reader does not consult this registry. In particular,
# registering a scientific method does NOT enable coordinated/FINAL consumption.
# A per-method roll-up, never an admission (reviewer's E2RC2-C03): SUPPORTED here never by itself grants a
# run, never selects a variant and never replaces the exact entry pin. Normal method dispatch uses the
# contract dispatch gate (contract_dispatch.dispatch_gate: exact variant, revision, declaration and pinned
# entry). Package 2's consumers add their own exact checks: the launch specification and the worker
# handshake accept only E_1's registered synthetic probe variant; begin_synthetic requires the exact
# variant to be released (contract_dispatch.variant_released); and the coordinated science allowlist is
# empty, so registered_scientific_binding always refuses.


def _roster(game_id: str) -> MappingProxyType:
    import _common.contract_dispatch as D
    import _common.contract_registry as R
    registry = R.InstalledRegistry(R.DATA_ROOT)      # module attributes read at call time
    active = {}
    for g, m, v in registry.chain_keys():
        if g == game_id:
            active.setdefault(m, []).append(registry.active_entry(g, m, v)['registry_status'])
    out = {}
    for m in _METHODS:
        statuses = active.get(m, [])
        flagged = D.METHODS_ROOT / D.method_folder(m) / D.FLAG_NAME
        if SUPPORTED in statuses and not (flagged.exists() or flagged.is_symlink()):
            out[m] = SUPPORTED
        elif statuses and all(s == UNSUPPORTED for s in statuses):
            out[m] = UNSUPPORTED
        else:
            out[m] = OPEN
    return MappingProxyType(out)


def method_status(game_id: str, method_id: str) -> str:
    get_profile(game_id)
    if type(method_id) is not str or method_id not in _METHODS:
        raise ValueError('unregistered E-number')
    return _roster(game_id)[method_id]


def all_statuses(game_id: str):
    get_profile(game_id)
    return _roster(game_id)
