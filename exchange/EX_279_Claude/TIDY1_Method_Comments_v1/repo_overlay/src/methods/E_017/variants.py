"""E_17 (Discrete Recurrence Hazard Curves): the fixed settings of each E_17 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the form ("bins" or "logage"), the prior strength c (None for
    "logage"), the window in draws (None for all), the minimum history.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_017/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_17 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision.
"""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (form 'bins' or 'logage'; prior strength c, or None; window in draws, or None for all; minimum history)
VARIANTS = MappingProxyType({
    'HAZARD_BINS_C100_V1': ('bins', Fraction(100), None, 52),
    'HAZARD_BINS_W208_C100_V1': ('bins', Fraction(100), 208, 208),
    'HAZARD_LOGAGE_SIGN_V1': ('logage', None, None, 52),
})
