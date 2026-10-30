"""E_7 revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (window M, or None for all eligible draws; prior strength c; minimum history)
VARIANTS = MappingProxyType({
    'BETA_SHRINK_W52_C52_V1': (52, Fraction(52), 52),
    'BETA_SHRINK_W104_C52_V1': (104, Fraction(52), 104),
    'BETA_SHRINK_FULL_C52_V1': (None, Fraction(52), 1),
})
