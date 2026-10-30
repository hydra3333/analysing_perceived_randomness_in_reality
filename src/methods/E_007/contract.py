"""E_7 revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given; the contract assembles,
ranks, applies ties and validates the record (E2R-R07). Specification: doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md section 3.1.
Beta shrinkage over a window: s_j = (c r + k_j(M)) / (c + M), the posterior mean of a Beta(c r, c(1 - r))
prior updated by the window's counts (r = K/L, the fair-draw rate). The values sum to K exactly.
With fewer eligible draws than the variant's minimum, nothing is returned and the contract records
INSUFFICIENT_HISTORY. verify() recomputes by a second, differently written route and refuses any difference.
"""
from __future__ import annotations

from fractions import Fraction

from E_007.variants import VARIANTS
from _common import occurrence_counts as OC
from _common.contract_forecast import BarrelOutput, MethodOutput, ProbabilityVector, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = 'E_7'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = True
PROVENANCE = 'E_7 r1 (Bayesian Frequency Shrinkage): exact rational arithmetic, each value rounded once to float64'


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
    M, c, _minimum = cfg
    size = len(draws) if M is None else M
    r = Fraction(b.selected, b.high - b.low + 1)
    if not second:
        k = OC.window_counts(draws, b.low, b.high, size)
        return {j: (c * r + k[j]) / (c + size) for j in k}
    # second route: the posterior built by sequential Beta updates, one draw at a time
    alpha = {j: c * r for j in range(b.low, b.high + 1)}
    beta = {j: c * (1 - r) for j in alpha}
    for d in draws[len(draws) - size:]:
        present = set(d)
        for j in alpha:
            if j in present:
                alpha[j] += 1
            else:
                beta[j] += 1
    return {j: alpha[j] / (alpha[j] + beta[j]) for j in alpha}


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
