"""Fail-closed Package-2 result/variant registration, NOT scientific permission.

The synthetic probe is a separate registered VARIANT of E_1 and is never a
scientific result.  Scientific variants record known methodological identity,
but NO coordinated/FINAL result schema is activated in Package 2.  A later
scientifically reviewed adapter must explicitly register its actual (mode,
result schema, data kind) here, after independent review and owner approval.

Nothing in this module permits process launches, holdout access, or scoring.
"""
from __future__ import annotations

from types import MappingProxyType
from _common.game_profiles import get_profile
from _common.multigame_method_registry import method_status, SUPPORTED

SYNTHETIC_MODE = 'SYNTHETIC_CONTRACT_TEST'
SYNTHETIC_VARIANT = 'SYNTHETIC_PLUMBING_V1'
SYNTHETIC_SCHEMA = 'SYNTHETIC_COORDINATOR_PLUMBING_ONLY_V1'
SCIENTIFIC_MODES = frozenset({'COORDINATED', 'FINAL'})

# Registration of variants is NOT registration of coordinated output schemas.
_KNOWN_SCIENCE_VARIANTS = MappingProxyType({
    ('POWERBALL', 'E_1'): frozenset({'FULL_HISTORY_RAW_COUNTS_V1'}),
    ('OZLOTTO', 'E_1'): frozenset({'FULL_HISTORY_RAW_COUNTS_V1'}),
})
_PROBE_VARIANTS = MappingProxyType({
    ('POWERBALL', 'E_1'): frozenset({SYNTHETIC_VARIANT}),
    ('OZLOTTO', 'E_1'): frozenset({SYNTHETIC_VARIANT}),
})

# Key: (game_id, method_id, variant_id, mode); value: (schema, data_kind).
# EMPTY UNTIL a reviewed coordinated/FINAL scientific producer exists.
# An accepted standalone legacy E_1 schema does not automatically qualify.
_COORDINATED_SCIENCE_ALLOWLIST = MappingProxyType({})


def require_synthetic_variant(game_id: str, method_id: str, variant_id: str) -> None:
    get_profile(game_id)
    if (method_status(game_id, method_id) != SUPPORTED or
            variant_id not in _PROBE_VARIANTS.get((game_id, method_id), ())):
        raise ValueError('unregistered synthetic-only method variant')


def registered_scientific_binding(*, game_id: str, method_id: str,
                                  variant_id: str, mode: str) -> tuple[str, str]:
    """Return explicitly registered coordinated schema/data_kind or fail closed."""
    get_profile(game_id)
    if (mode not in SCIENTIFIC_MODES or
            method_status(game_id, method_id) != SUPPORTED or
            variant_id not in _KNOWN_SCIENCE_VARIANTS.get((game_id, method_id), ())):
        raise ValueError('not an eligible registered scientific variant')
    accepted = _COORDINATED_SCIENCE_ALLOWLIST.get((game_id, method_id, variant_id, mode))
    if (type(accepted) is not tuple or len(accepted) != 2 or
            any(type(x) is not str or not x for x in accepted)):
        raise ValueError('no reviewed coordinated/FINAL scientific contract registered')
    return accepted


def require_scientific_contract(*, game_id: str, method_id: str,
                                variant_id: str, mode: str, result: dict) -> None:
    """Fail closed unless exact registered schema, data_kind and mode match."""
    accepted = registered_scientific_binding(game_id=game_id, method_id=method_id,
                                             variant_id=variant_id, mode=mode)
    if (type(result) is not dict or
            (result.get('schema'), result.get('data_kind')) != accepted or
            result.get('mode') != mode):
        raise ValueError('unregistered scientific result schema or data kind')
