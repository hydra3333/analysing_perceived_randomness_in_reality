"""E_19 revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given; the contract assembles,
ranks, applies ties and validates the record (E2R-R07). Specification: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md section 4.3.
Periodic recurrence hazard: E_17's binned hazard b(k) (prior c, all draws) as the trend, times a per-label
factor in age mod T shrunk by d towards the pooled one, with the label's overall level divided out:
s_j = b(G_j) psi_{j, G_j mod T}.
Scores only: no probability vector is published (owner decision W2-4).
With fewer eligible draws than the variant's minimum, nothing is returned and the contract records
INSUFFICIENT_HISTORY. verify() recomputes by a second, differently written route and refuses any difference.
"""
from __future__ import annotations

from fractions import Fraction

from E_019.variants import VARIANTS
from _common import recurrence_gaps as RG
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = 'E_19'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = False
PROVENANCE = 'E_19 r1 (Periodic Recurrence-Hazard Peaks): exact rational arithmetic, each value rounded once to float64'


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


def _trend(per_label, b, c):
    """E_17's binned hazard with prior c over all draws, from the given per-label counts."""
    L = b.high - b.low + 1
    r = Fraction(b.selected, L)
    edges = RG.bin_edges(L, b.selected)
    nb = len(edges) + 1
    Rb, Eb = [0] * nb, [0] * nb
    R, E = RG.pooled(per_label)
    for k, n in R.items():
        Rb[RG.bin_of(k, edges)] += n
    for k, n in E.items():
        Eb[RG.bin_of(k, edges)] += n
    h = [(Eb[i] + c * r) / (Rb[i] + c) for i in range(nb)]
    return lambda k: h[RG.bin_of(k, edges)]


def _scores(draws, b, cfg, second):
    T, c, d, _minimum = cfg
    per_label = (RG.label_exposures_from_gaps if second else RG.label_exposures_by_walk)(draws, b.low, b.high)
    trend = _trend(per_label, b, c)
    O = {j: [0] * T for j in per_label}
    X = {j: [Fraction(0)] * T for j in per_label}
    for j, (Rj, Ej) in per_label.items():
        for k, n in Rj.items():
            X[j][k % T] += n * trend(k)
        for k, n in Ej.items():
            O[j][k % T] += n
    if not second:
        Op = [sum(O[j][q] for j in O) for q in range(T)]
        Xp = [sum((X[j][q] for j in X), Fraction(0)) for q in range(T)]
    else:                                            # pooled by residue straight from the pooled counts
        R, E = RG.pooled(per_label)
        Op, Xp = [0] * T, [Fraction(0)] * T
        for k, n in R.items():
            Xp[k % T] += n * trend(k)
        for k, n in E.items():
            Op[k % T] += n
    phi = [(Op[q] + d) / (Xp[q] + d) for q in range(T)]
    ages = RG.projected_ages(len(draws), RG.appearances(draws, b.low, b.high))
    out = {}
    for j, g in ages.items():
        level = (sum(O[j]) + d) / (sum(X[j], Fraction(0)) + d)
        q = g % T
        out[j] = trend(g) * ((O[j][q] + d * phi[q]) / (X[j][q] + d)) / level
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
