"""E_18 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (window in draws for the completed gaps, or None for all; prior pseudo-gaps c; minimum history)
VARIANTS = MappingProxyType({
    'MIX4_ALL_C10_V1': (None, Fraction(10), 104),
    'MIX4_W208_C10_V1': (208, Fraction(10), 208),
    'MIX4_W104_C10_V1': (104, Fraction(10), 104),
})
