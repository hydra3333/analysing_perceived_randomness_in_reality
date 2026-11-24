"""E_3 (Occurrence-Curve Endpoint Forecast): the family's shared calculation, used by every E_3 variant.

What this file is for
    It holds the whole calculation of E_3. compute() turns the draws before a target into one score for
    every number of every barrel; verify() works the same scores out again by a second, differently written
    route and refuses the record if they differ. Each variant's own method.py passes its task here, and the
    variant's fixed settings are looked up, by the task's variant ID, in E_003/variants.py.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md sections 2 to 4.
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2 (a family's shared
    core file).

Which of the project's own modules it uses
    E_003.variants              VARIANTS: each variant's fixed settings
    _shared.polynomial_fits_v1  exact polynomial fits to a short series (least squares, interpolation, minimax)
    _common.contract_forecast   the types a method returns (MethodOutput, BarrelOutput, ScoredRanking)
    _common.game_profiles       get_profile: each game's barrels (lowest and highest number, how many are drawn)

What uses it
    E_003/<VARIANT>/method.py of every E_3 variant, and this family's tests.

How it computes (the header this file had before the tidy-up, kept)
    The shared standalone runner has already checked the release rule and loaded the prefix-only view before
    compute() is called. compute() reads only the view and the frozen task it is given. For each barrel and each
    label it takes the label's 0/1 series over the last M eligible draws (t = -M..-1; the target is t = 0), fits
    the variant's polynomial with the shared helper, and scores the label by p(0), the fitted curve's value at the target.
    These are curve values, not chances, so no probability vector is returned (design note v0.1 section 4).
    With fewer than M eligible draws nothing is returned and the contract records INSUFFICIENT_HISTORY.
    verify() recomputes by a second, differently written algorithm (least squares: Forsythe recurrence;
    interpolation: Newton divided differences; minimax: the alternation certificate) and refuses any difference.
"""
from __future__ import annotations

from E_003.variants import VARIANTS
from _shared import polynomial_fits_v1 as PF
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

# The fixed identity and output settings of this family; they never change:
#   METHOD_ID         the method's ID as the records name it
#   OBSERVATION_VIEW  the view of the earlier draws this family accepts: numbers as a set, no dates
METHOD_ID = 'E_3'
OBSERVATION_VIEW = 'UNORDERED_SET'
SCORE_COEFFICIENT = 0                  # p(t) = a_0 + a_1 t + ...: E_3 scores a_0


def _config(task):
    """Check that the task is for this family and return the variant's fixed settings.

    task: the frozen MethodTask the research code built (method, variant, observation view).
    Returns the variant's line of VARIANTS, for example ('LS', 52, 2, None, None), which holds, in order:
        the kind of fit ("LS", "INTERP" or "MINIMAX"), the window M, the degree D, the smoothing half-width H, the
        interpolation positions.
    Refuses (ValueError) a task for another method, an unknown variant, or any view but the unordered one without dates.
    """
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
    """The one coefficient of a fitted polynomial that this family scores by.

    coeffs: the polynomial's coefficients [a_0, a_1, ...], for example [Fraction(9, 44), Fraction(1, 300)].
    Returns coeffs[SCORE_COEFFICIENT], for example Fraction(9, 44) for those coefficients; 0 if the polynomial is
    too short to have that coefficient.
    """
    return coeffs[SCORE_COEFFICIENT] if len(coeffs) > SCORE_COEFFICIENT else 0


def compute(task, view) -> MethodOutput:
    """Compute the scores for one target draw, from the draws before it only.

    task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
    Returns a MethodOutput holding, for each barrel, every number's exact score rounded once to a float64, for example
        MethodOutput(barrels={'MAIN': BarrelOutput(ranking=ScoredRanking({1: 0.2045, 2: 0.1273, ...}))}).
    With fewer earlier draws than the variant's window it returns MethodOutput(barrels={}), which is recorded as
    INSUFFICIENT_HISTORY.
    """
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
