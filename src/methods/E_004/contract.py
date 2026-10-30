"""E_4 revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given. For each barrel and each
label it takes the label's 0/1 series over the last M eligible draws (t = -M..-1; the target is t = 0), fits
the variant's polynomial with the shared helper, and scores the label by p'(0), the fitted curve's slope at the target (per draw).
These are curve slopes, not chances, so no probability vector is returned (design note v0.1 section 4).
With fewer than M eligible draws nothing is returned and the contract records INSUFFICIENT_HISTORY.
verify() recomputes by a second, differently written algorithm (least squares: Forsythe recurrence;
interpolation: Newton divided differences; minimax: the alternation certificate) and refuses any difference.
"""
from __future__ import annotations

from E_004.variants import VARIANTS
from _common import polynomial_fits as PF
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = 'E_4'
OBSERVATION_VIEW = 'UNORDERED_SET'
SCORE_COEFFICIENT = 1                  # p(t) = a_0 + a_1 t + ...: E_4 scores a_1


def _config(task):
    if task.method_id != METHOD_ID:
        raise ValueError(f'this module computes {METHOD_ID} only')
    if task.variant_id not in VARIANTS:
        raise ValueError(f'unknown {METHOD_ID} variant {task.variant_id!r}')
    if task.observation_view != OBSERVATION_VIEW or task.include_dates:
        raise ValueError(f'{METHOD_ID} uses the unordered view without dates')
    return VARIANTS[task.variant_id]


def _series(view, barrel, window):
    """{label: its 0/1 series over the last `window` eligible draws, oldest first}, or None if too few draws."""
    rows = view.simple_rows()
    if len(rows) < window:
        return None
    drawn = [set(r['main']) if barrel.barrel_id == 'MAIN' else {r['powerball']} for r in rows[-window:]]
    return {j: [1 if j in d else 0 for d in drawn] for j in range(barrel.low, barrel.high + 1)}


def _fits(task, view, second_algorithm: bool):
    """{barrel_id: {label: coefficients}} or None (insufficient history)."""
    fit, window, degree, half, nodes = _config(task)
    ts = PF.abscissae(window)
    out = {}
    for b in get_profile(task.game_id).barrels:
        series = _series(view, b, window)
        if series is None:
            return None
        if fit == 'LS':
            if second_algorithm:
                out[b.barrel_id] = {j: PF.least_squares_by_recurrence(ts, y, degree) for j, y in series.items()}
            else:
                ls = PF.LeastSquares(ts, degree)              # one factorisation for every label
                out[b.barrel_id] = {j: ls.fit(y) for j, y in series.items()}
        elif fit == 'INTERP':
            pts = [ts[c] for c in nodes]
            method = PF.interpolate_newton if second_algorithm else PF.interpolate
            smooth = {j: PF.smoothed(y, half) for j, y in series.items()}
            out[b.barrel_id] = {j: method(pts, [smooth[j][c] for c in nodes]) for j in series}
        elif fit == 'MINIMAX':
            coeffs = {}
            for j, y in series.items():
                s = PF.smoothed(y, half)
                c, err, _ref = PF.minimax(ts, s, degree)
                if second_algorithm and PF.minimax_certificate(ts, s, c, degree) != err:
                    raise ValueError(f'{METHOD_ID} check: the minimax certificate disagrees with the exchange')
                coeffs[j] = c
            out[b.barrel_id] = coeffs
        else:
            raise ValueError(f'unknown fit {fit!r}')
    return out


def _score(coeffs):
    return coeffs[SCORE_COEFFICIENT] if len(coeffs) > SCORE_COEFFICIENT else 0


def compute(task, view) -> MethodOutput:
    fits = _fits(task, view, second_algorithm=False)
    if fits is None:
        return MethodOutput(barrels={})                       # the contract records INSUFFICIENT_HISTORY
    return MethodOutput(barrels={bid: BarrelOutput(ranking=ScoredRanking({j: float(_score(c)) for j, c in per.items()}))
                                 for bid, per in fits.items()})


def verify(task, view, forecast, diagnostic) -> None:
    """Raise ValueError unless the record equals the second algorithm's result."""
    if diagnostic is not None:
        raise ValueError(f'{METHOD_ID} declares no diagnostic record')
    if forecast is None:
        raise ValueError(f'{METHOD_ID} always has a forecast record')
    fits = _fits(task, view, second_algorithm=True)
    if fits is None:
        if forecast['record_status'] != 'INSUFFICIENT_HISTORY':
            raise ValueError(f'{METHOD_ID} check: too few draws, but the record is not INSUFFICIENT_HISTORY')
        return
    if set(forecast['barrels']) != set(fits):
        raise ValueError(f'{METHOD_ID} check: barrels differ')
    for bid, per in fits.items():
        want = [float(_score(per[j])) for j in sorted(per)]
        if forecast['barrels'][bid]['scores'] != want:
            raise ValueError(f'{METHOD_ID} check: the record differs from the recomputation in barrel {bid}')
