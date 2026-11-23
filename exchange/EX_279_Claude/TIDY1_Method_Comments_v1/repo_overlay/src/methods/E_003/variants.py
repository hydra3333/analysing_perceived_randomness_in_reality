"""E_3 (Occurrence-Curve Endpoint Forecast): the fixed settings of each E_3 variant.

What this file is for
    One table, VARIANTS, with one line for each variant: the kind of fit ("LS", "INTERP" or "MINIMAX"), the window M,
    the degree D, the smoothing half-width H, the interpolation positions.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md (its section on the variants).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2.

Which of the project's own modules it uses
    None.

What uses it
    E_003/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
    E_3 revision 1: the fixed variants (design note v0.1 section 5). Changing or adding one is a new revision.

    Each variant is (fit, window M, degree D, smoothing half-width H, interpolation node positions):
      LS       least squares on the raw 0/1 series (H and nodes unused)
      INTERP   interpolation through the smoothed series at the given window positions (the Chebyshev nodes of
               the first kind mapped onto 0..M-1, rounded to the nearest position; fixed here so that no floating
               point is used at run time; the tests recompute them from the formula)
      MINIMAX  Chebyshev minimax on the smoothed series
    E_3 and E_4 use the same six configurations; their tests check that the two tables are identical.
"""
from types import MappingProxyType

# variant_id: (fit; window M; degree D; smoothing half-width H, or None; interpolation positions, or None)
VARIANTS = MappingProxyType({
    'POLY_LS_W52_D2_V1': ('LS', 52, 2, None, None),
    'POLY_LS_W52_D3_V1': ('LS', 52, 3, None, None),
    'POLY_LS_W104_D3_V1': ('LS', 104, 3, None, None),
    'POLY_INTERP_W52_D4_H4_V1': ('INTERP', 52, 4, 4, (50, 40, 26, 11, 1)),
    'POLY_MINIMAX_W52_D2_H4_V1': ('MINIMAX', 52, 2, 4, None),
    'POLY_MINIMAX_W52_D3_H4_V1': ('MINIMAX', 52, 3, 4, None),
})
