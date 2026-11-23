"""E_18 (Mixtures of Recurrence Modes): the fixed settings of each E_18 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the window in draws for the completed gaps (None for all),
    the prior pseudo-gaps c, the minimum history.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_018/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_18 revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision.
"""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (window in draws for the completed gaps, or None for all; prior pseudo-gaps c; minimum history)
VARIANTS = MappingProxyType({
    'MIX4_ALL_C10_V1': (None, Fraction(10), 104),
    'MIX4_W208_C10_V1': (208, Fraction(10), 208),
    'MIX4_W104_C10_V1': (104, Fraction(10), 104),
})
