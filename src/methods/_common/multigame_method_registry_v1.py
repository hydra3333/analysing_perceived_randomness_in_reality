"""Conservative scoped register: no structural or scientific method silently excluded.

Only E_1 has a currently accepted implementation. Other methods are
FORMULA_OPEN pending the existing research/family approval process.
"""
from __future__ import annotations
from types import MappingProxyType

from _common.game_profiles_v1 import get_profile

SUPPORTED = 'SUPPORTED'
UNSUPPORTED = 'UNSUPPORTED_FOR_GAME'
OPEN = 'FORMULA_OPEN'
_METHODS = tuple(f'E_{i}' for i in range(1, 63))
_REGISTRY = MappingProxyType({
    game: MappingProxyType({eid: (SUPPORTED if eid == 'E_1' else OPEN)
                            for eid in _METHODS})
    for game in ('POWERBALL', 'OZLOTTO')
})
# This is a scientific execution/support roster, NOT a view-entitlement list.
# The general-purpose reader does not consult this registry. In particular,
# registering a scientific method does NOT enable coordinated/FINAL consumption.


def method_status(game_id: str, method_id: str) -> str:
    get_profile(game_id)
    if type(method_id) is not str or method_id not in _REGISTRY[game_id]:
        raise ValueError('unregistered E-number')
    return _REGISTRY[game_id][method_id]


def all_statuses(game_id: str):
    get_profile(game_id)
    return _REGISTRY[game_id]
