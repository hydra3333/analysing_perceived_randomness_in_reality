"""E_8 revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (period length P, minimum history = 2P)
VARIANTS = MappingProxyType({
    'HIER_PERIODS_P13_V1': (13, 26),
    'HIER_PERIODS_P26_V1': (26, 52),
    'HIER_PERIODS_P52_V1': (52, 104),
})
