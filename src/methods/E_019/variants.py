"""E_19 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (cycle T; trend prior c; shrinkage d; minimum history)
VARIANTS = MappingProxyType({
    'PERIODIC_T2_V1': (2, Fraction(100), Fraction(20), 104),
    'PERIODIC_T3_V1': (3, Fraction(100), Fraction(20), 104),
    'PERIODIC_T4_V1': (4, Fraction(100), Fraction(20), 104),
})
