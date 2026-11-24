"""E_10 (Multi-Horizon Frequency Contrasts): the fixed settings of each E_10 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the short window S, the long window Lw (None for all earlier
    draws), the minimum history.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_010/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_10 revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision.
"""
from fractions import Fraction
from types import MappingProxyType

# variant_id: (short window S; long window Lw, or None for all eligible draws; minimum history)
VARIANTS = MappingProxyType({
    'CONTRAST_S13_L104_V1': (13, 104, 104),
    'CONTRAST_S26_L208_V1': (26, 208, 208),
    'CONTRAST_S52_FULL_V1': (52, None, 104),
})
