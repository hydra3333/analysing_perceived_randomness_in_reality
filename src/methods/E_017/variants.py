"""E_17 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (form 'bins' or 'logage'; prior strength c, or None; window in draws, or None for all; minimum history)
VARIANTS = MappingProxyType({
    'HAZARD_BINS_C100_V1': ('bins', Fraction(100), None, 52),
    'HAZARD_BINS_W208_C100_V1': ('bins', Fraction(100), 208, 208),
    'HAZARD_LOGAGE_SIGN_V1': ('logage', None, None, 52),
})
