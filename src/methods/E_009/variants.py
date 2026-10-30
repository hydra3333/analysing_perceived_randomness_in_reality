"""E_9 revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (factor lambda, minimum history)
VARIANTS = MappingProxyType({
    'EXP_DECAY_5_6_V1': (Fraction(5, 6), 1),
    'EXP_DECAY_18_19_V1': (Fraction(18, 19), 1),
    'EXP_DECAY_37_38_V1': (Fraction(37, 38), 1),
})
