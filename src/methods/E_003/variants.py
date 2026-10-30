"""E_3 revision 1: the fixed variants (design note v0.1 section 5). Changing or adding one is a new revision.

Each variant is (fit, window M, degree D, smoothing half-width H, interpolation node positions):
  LS       least squares on the raw 0/1 series (H and nodes unused)
  INTERP   interpolation through the smoothed series at the given window positions (the Chebyshev nodes of
           the first kind mapped onto 0..M-1, rounded to the nearest position; fixed here so that no floating
           point is used at run time; the tests recompute them from the formula)
  MINIMAX  Chebyshev minimax on the smoothed series
E_3 and E_4 use the same six configurations; their tests check that the two tables are identical.
"""
from types import MappingProxyType

VARIANTS = MappingProxyType({
    'POLY_LS_W52_D2_V1': ('LS', 52, 2, None, None),
    'POLY_LS_W52_D3_V1': ('LS', 52, 3, None, None),
    'POLY_LS_W104_D3_V1': ('LS', 104, 3, None, None),
    'POLY_INTERP_W52_D4_H4_V1': ('INTERP', 52, 4, 4, (50, 40, 26, 11, 1)),
    'POLY_MINIMAX_W52_D2_H4_V1': ('MINIMAX', 52, 2, 4, None),
    'POLY_MINIMAX_W52_D3_H4_V1': ('MINIMAX', 52, 3, 4, None),
})
