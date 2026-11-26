"""E_7 (Bayesian Frequency Shrinkage): the fixed settings of each E_7 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the window M (None for all earlier draws), the prior strength
    c, the minimum history.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_007/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_7 revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision.
"""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (window M, or None for all eligible draws; prior strength c; minimum history)
VARIANTS = MappingProxyType({
    'BETA_SHRINK_W52_C52_V1': (52, Fraction(52), 52),
    'BETA_SHRINK_W104_C52_V1': (104, Fraction(52), 104),
    'BETA_SHRINK_FULL_C52_V1': (None, Fraction(52), 1),
})
