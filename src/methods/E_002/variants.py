"""E_2 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision."""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (statistic 'mean' or 'median'; the last n gaps, or None for all; minimum history)
VARIANTS = MappingProxyType({
    'RECUR_MEAN_ALL_V1': ('mean', None, 104),
    'RECUR_MEDIAN_ALL_V1': ('median', None, 104),
    'RECUR_MEAN_LAST8_V1': ('mean', 8, 104),
})
