"""E_8 (Hierarchical Dirichlet-Multinomial Propensity): the fixed settings of each E_8 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the period length P, the minimum history (2P).
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_008/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_8 revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision.
"""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (period length P, minimum history = 2P)
VARIANTS = MappingProxyType({
    'HIER_PERIODS_P13_V1': (13, 26),
    'HIER_PERIODS_P26_V1': (26, 52),
    'HIER_PERIODS_P52_V1': (52, 104),
})
