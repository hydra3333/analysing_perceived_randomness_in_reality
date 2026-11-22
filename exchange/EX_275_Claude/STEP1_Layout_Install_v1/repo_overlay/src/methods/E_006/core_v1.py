"""E_6 revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view
before compute() is called. compute() reads only the
view and the frozen task it is given; it returns a MethodOutput with no identity fields, and the contract
assembles, ranks, applies ties and validates the record (E2R-R07). verify() then recomputes the scores by
a different exact algorithm and refuses the record if anything differs, before anything is published.
"""
from __future__ import annotations

from fractions import Fraction

from E_006.beta_bernoulli import VARIANTS, posterior_means, posterior_means_by_recursion
from _common.contract_forecast import BarrelOutput, MethodOutput, ProbabilityVector, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = 'E_6'
OBSERVATION_VIEW = 'UNORDERED_SET'
PROVENANCE = ('E_6 r1 Beta-Bernoulli estimates (posterior means; discounted updates for the decay variants): '
              'exact rational arithmetic, each rounded once to float64')


def _lam(task) -> Fraction:
    if task.method_id != METHOD_ID:
        raise ValueError('this module computes E_6 only')
    if task.variant_id not in VARIANTS:
        raise ValueError(f'unknown E_6 variant {task.variant_id!r}')
    if task.observation_view != OBSERVATION_VIEW or task.include_dates:
        raise ValueError('E_6 uses the unordered view without dates')
    return VARIANTS[task.variant_id]


def _barrel_draws(view, barrel_id: str) -> list[list[int]]:
    """The labels drawn in one barrel at each eligible draw, oldest first."""
    rows = view.simple_rows()
    if barrel_id == 'MAIN':
        return [list(r['main']) for r in rows]
    return [[r['powerball']] for r in rows]


def _exact(task, view, method) -> dict[str, dict[int, Fraction]]:
    lam = _lam(task)
    return {b.barrel_id: method(_barrel_draws(view, b.barrel_id), b.low, b.high, b.selected, lam)
            for b in get_profile(task.game_id).barrels}


def compute(task, view) -> MethodOutput:
    out = {}
    for bid, p in _exact(task, view, posterior_means).items():
        floats = {j: float(pj) for j, pj in p.items()}            # correctly rounded, once
        out[bid] = BarrelOutput(ranking=ScoredRanking(floats),
                                probability=ProbabilityVector([floats[j] for j in sorted(floats)], PROVENANCE))
    return MethodOutput(barrels=out)


def verify(task, view, forecast, diagnostic) -> None:
    """Raise ValueError unless the record's scores and probabilities equal an independent recomputation."""
    if diagnostic is not None:
        raise ValueError('E_6 declares no diagnostic record')
    if forecast is None:
        raise ValueError('E_6 always has a forecast record')
    exact = _exact(task, view, posterior_means_by_recursion)
    if set(forecast['barrels']) != set(exact):
        raise ValueError('E_6 check: barrels differ')
    for bid, p in exact.items():
        b = next(x for x in get_profile(task.game_id).barrels if x.barrel_id == bid)
        if sum(p.values()) != b.selected:
            raise ValueError(f'E_6 check: barrel {bid} does not sum to {b.selected} exactly')
        want = [float(p[j]) for j in range(b.low, b.high + 1)]
        rec = forecast['barrels'][bid]
        if rec['scores'] != want or rec['probability'].get('vector') != want:
            raise ValueError(f'E_6 check: the record differs from the recomputed posterior means in barrel {bid}')
