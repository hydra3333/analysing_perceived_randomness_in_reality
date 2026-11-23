"""E_2 (Expected Recurrence-Interval Alignment): the fixed settings of each E_2 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the statistic ("mean" or "median"), the last n gaps used
    (None for all), the minimum history.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_002/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_2 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision.
"""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (statistic 'mean' or 'median'; the last n gaps, or None for all; minimum history)
VARIANTS = MappingProxyType({
    'RECUR_MEAN_ALL_V1': ('mean', None, 104),
    'RECUR_MEDIAN_ALL_V1': ('median', None, 104),
    'RECUR_MEAN_LAST8_V1': ('mean', 8, 104),
})
