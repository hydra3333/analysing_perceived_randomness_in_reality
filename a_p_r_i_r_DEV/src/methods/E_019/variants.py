"""E_19 (Periodic Recurrence-Hazard Peaks): the fixed settings of each E_19 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the cycle T, the trend prior c, the shrinkage d, the minimum
    history.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_019/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_19 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision.
"""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (cycle T; trend prior c; shrinkage d; minimum history)
VARIANTS = MappingProxyType({
    'PERIODIC_T2_V1': (2, Fraction(100), Fraction(20), 104),
    'PERIODIC_T3_V1': (3, Fraction(100), Fraction(20), 104),
    'PERIODIC_T4_V1': (4, Fraction(100), Fraction(20), 104),
})
