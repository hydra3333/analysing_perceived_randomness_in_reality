"""E_2 revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given; the contract assembles,
ranks, applies ties and validates the record (E2R-R07). Specification: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md section 4.1.
Recurrence-interval alignment: c_j is the mean or median of the label's completed gaps (all, or its last
n), or the fair mean gap L/K if it has none; s_j = -|G_j - c_j| / c_j, G_j being its projected age.
Scores only: no probability vector is published (owner decision W2-4).
With fewer eligible draws than the variant's minimum, nothing is returned and the contract records
INSUFFICIENT_HISTORY. verify() recomputes by a second, differently written route and refuses any difference.
"""
from __future__ import annotations

from fractions import Fraction

from E_002.variants import VARIANTS
from _common import recurrence_gaps as RG
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = 'E_2'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = False
PROVENANCE = 'E_2 r1 (Expected Recurrence-Interval Alignment): exact rational arithmetic, each value rounded once to float64'


def _config(task):
    if task.method_id != METHOD_ID:
        raise ValueError(f'this module computes {METHOD_ID} only')
    if task.variant_id not in VARIANTS:
        raise ValueError(f'unknown {METHOD_ID} variant {task.variant_id!r}')
    if task.observation_view != OBSERVATION_VIEW or task.include_dates:
        raise ValueError(f'{METHOD_ID} uses the unordered view without dates')
    return VARIANTS[task.variant_id]


def _barrel_draws(view, barrel_id):
    """The labels drawn in one barrel at each eligible draw, oldest first."""
    rows = view.simple_rows()
    if barrel_id == 'MAIN':
        return [list(r['main']) for r in rows]
    return [[r['powerball']] for r in rows]


def _median_by_sorting(g):
    s = sorted(g)
    n = len(s)
    return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def _median_by_counting(g):
    """The median from a count of each gap length, without sorting the gaps."""
    counts = {}
    for x in g:
        counts[x] = counts.get(x, 0) + 1
    n, seen, lower = len(g), 0, None
    for value in range(1, max(counts) + 1):
        seen += counts.get(value, 0)
        if lower is None and seen >= (n + 1) // 2:
            lower = value
        if seen >= n // 2 + 1:
            return Fraction(lower + value, 2) if n % 2 == 0 else Fraction(lower)
    raise ValueError('median not found')


def _scores(draws, b, cfg, second):
    stat, last_n, _minimum = cfg
    fair_gap = Fraction(b.high - b.low + 1, b.selected)
    app = RG.appearances(draws, b.low, b.high)
    ages = RG.projected_ages(len(draws), app)
    out = {}
    if not second:
        gaps = RG.completed_gaps(app)
        for j in app:
            g = gaps[j][-last_n:] if last_n else gaps[j]
            if not g:
                c = fair_gap
            elif stat == 'mean':
                c = Fraction(sum(g), len(g))
            else:
                c = _median_by_sorting(g)
            out[j] = -abs(ages[j] - c) / c
        return out
    # second route: the mean by telescoping the appearance positions; the median by counting; gaps by a scan
    scanned = RG.gaps_by_scan(draws, b.low, b.high)
    for j, p in app.items():
        if len(p) < 2:
            c = fair_gap
        elif stat == 'mean':
            q = p[-(last_n + 1):] if last_n else p
            c = Fraction(q[-1] - q[0], len(q) - 1)
        else:
            c = _median_by_counting(scanned[j][-last_n:] if last_n else scanned[j])
        out[j] = -abs(ages[j] - c) / c
    return out


def _exact(task, view, second: bool):
    """{barrel_id: {label: exact score}}, or None when the history is shorter than the variant's minimum."""
    cfg = _config(task)
    barrels = get_profile(task.game_id).barrels
    if len(view.simple_rows()) < cfg[-1]:
        return None
    return {b.barrel_id: _scores(_barrel_draws(view, b.barrel_id), b, cfg, second) for b in barrels}


def compute(task, view) -> MethodOutput:
    exact = _exact(task, view, second=False)
    if exact is None:
        return MethodOutput(barrels={})                    # the contract records INSUFFICIENT_HISTORY
    out = {}
    for bid, s in exact.items():
        floats = {j: float(v) for j, v in s.items()}        # correctly rounded, once
        out[bid] = BarrelOutput(ranking=ScoredRanking(floats))
    return MethodOutput(barrels=out)


def verify(task, view, forecast, diagnostic) -> None:
    """Raise ValueError unless the record equals the second route's recomputation."""
    if diagnostic is not None:
        raise ValueError(f'{METHOD_ID} declares no diagnostic record')
    if forecast is None:
        raise ValueError(f'{METHOD_ID} always has a forecast record')
    exact = _exact(task, view, second=True)
    if exact is None:
        if forecast['record_status'] != 'INSUFFICIENT_HISTORY':
            raise ValueError(f'{METHOD_ID} check: too few draws, but the record is not INSUFFICIENT_HISTORY')
        return
    if set(forecast['barrels']) != set(exact):
        raise ValueError(f'{METHOD_ID} check: barrels differ')
    for bid, s in exact.items():
        b = next(x for x in get_profile(task.game_id).barrels if x.barrel_id == bid)
        want = [float(s[j]) for j in range(b.low, b.high + 1)]
        rec = forecast['barrels'][bid]
        if rec['scores'] != want:
            raise ValueError(f'{METHOD_ID} check: the record differs from the recomputation in barrel {bid}')
        if rec['probability'] != {'kind': 'NONE'}:
            raise ValueError(f'{METHOD_ID} check: a score-only method published a probability in barrel {bid}')
