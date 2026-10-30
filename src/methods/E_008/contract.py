"""E_8 revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given; the contract assembles,
ranks, applies ties and validates the record (E2R-R07). Specification: doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md section 3.4.
Hierarchical rates across periods (beta-binomial, method of moments): the newest n*P draws in n periods
of P; the between-period excess variance, pooled over labels and clamped to [0, r(1 - r)], gives one
weight w for the latest period; s_j = w p_{j,latest} + (1 - w) m_j. The values sum to K exactly.
With fewer eligible draws than the variant's minimum, nothing is returned and the contract records
INSUFFICIENT_HISTORY. verify() recomputes by a second, differently written route and refuses any difference.
"""
from __future__ import annotations

from fractions import Fraction

from E_008.variants import VARIANTS
from _common import occurrence_counts as OC
from _common.contract_forecast import BarrelOutput, MethodOutput, ProbabilityVector, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = 'E_8'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = True
PROVENANCE = 'E_8 r1 (Hierarchical Dirichlet-Multinomial Propensity): exact rational arithmetic, each value rounded once to float64'


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


def _scores(draws, b, cfg, second):
    P, _minimum = cfg
    L = b.high - b.low + 1
    r = Fraction(b.selected, L)
    if not second:                                   # two-pass formula, in rates
        counts = OC.period_counts(draws, b.low, b.high, P)
        n = len(next(iter(counts.values())))
        m, latest, excess = {}, {}, []
        for j, cs in counts.items():
            p = [Fraction(x, P) for x in cs]
            mj = sum(p, Fraction(0)) / n
            V = sum(((x - mj) ** 2 for x in p), Fraction(0)) / (n - 1)
            excess.append((V - (mj * (1 - mj) + V / n) / P) * Fraction(P, P - 1))
            m[j], latest[j] = mj, p[-1]
    else:                                            # second route: integer counts, sum-of-squares formula
        counts = OC.period_counts_by_index(draws, b.low, b.high, P)
        n = len(next(iter(counts.values())))
        m, latest, excess = {}, {}, []
        for j, cs in counts.items():
            total = sum(cs)
            mj = Fraction(total, n * P)
            V = Fraction(sum(x * x for x in cs) * n - total * total, n * (n - 1) * P * P)
            excess.append((V - (mj * (1 - mj) + V / n) / P) * Fraction(P, P - 1))
            m[j], latest[j] = mj, Fraction(cs[-1], P)
    t = min(max(Fraction(0), sum(excess, Fraction(0)) / L), r * (1 - r))
    w = (P * t) / ((P - 1) * t + r * (1 - r))
    return {j: w * latest[j] + (1 - w) * m[j] for j in m}


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
        out[bid] = BarrelOutput(ranking=ScoredRanking(floats),
                                probability=ProbabilityVector([floats[j] for j in sorted(floats)], PROVENANCE))
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
        if sum(s.values()) != b.selected:
            raise ValueError(f'{METHOD_ID} check: barrel {bid} does not sum to {b.selected} exactly')
        if rec['probability'].get('vector') != want:
            raise ValueError(f'{METHOD_ID} check: the probability vector differs in barrel {bid}')
