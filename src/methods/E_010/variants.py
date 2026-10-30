"""E_10 revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (short window S; long window Lw, or None for all eligible draws; minimum history)
VARIANTS = MappingProxyType({
    'CONTRAST_S13_L104_V1': (13, 104, 104),
    'CONTRAST_S26_L208_V1': (26, 208, 208),
    'CONTRAST_S52_FULL_V1': (52, None, 104),
})
