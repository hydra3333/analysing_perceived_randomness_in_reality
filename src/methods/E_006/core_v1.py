"""E_6 (Per-Number Fitted Distribution Models): the family's shared calculation, used by every E_6 variant.

What this file is for
    It connects the mathematics of E_6 (beta_bernoulli.py, beside this file) to the research code. compute()
    turns the draws before a target into one estimate for every number of every barrel; verify() works the
    same estimates out again by a different exact algorithm and refuses the record if they differ. Each
    variant's own method.py passes its task here, and the variant's forgetting factor is looked up, by the
    task's variant ID, in the VARIANTS table of beta_bernoulli.py.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md section 2.
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2 (a family's shared
    core file).

Which of the project's own modules it uses
    E_006.beta_bernoulli         VARIANTS, and the two exact algorithms posterior_means and
    posterior_means_by_recursion
    _common.contract_forecast    the types a method returns (MethodOutput, BarrelOutput, ScoredRanking,
    ProbabilityVector)
    _common.game_profiles        get_profile: each game's barrels (lowest and highest number, how many are drawn)

What uses it
    E_006/<VARIANT>/method.py of every E_6 variant, and this family's tests.

How it computes (the header this file had before the tidy-up, kept)
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

# The fixed identity and output settings of this family; they never change:
#   METHOD_ID         the method's ID as the records name it
#   OBSERVATION_VIEW  the view of the earlier draws this family accepts: numbers as a set, no dates
#   PROVENANCE        the text stored with the published values, saying how they were computed
METHOD_ID = 'E_6'
OBSERVATION_VIEW = 'UNORDERED_SET'
PROVENANCE = ('E_6 r1 Beta-Bernoulli estimates (posterior means; discounted updates for the decay variants): '
              'exact rational arithmetic, each rounded once to float64')


def _lam(task) -> Fraction:
    """Check that the task is for this family and return the variant's forgetting factor.

    task: the frozen MethodTask the research code built (method, variant, observation view).
    Returns the variant's entry of VARIANTS, for example Fraction(74, 75) (1 means every earlier draw counts equally).
    Refuses (ValueError) a task for another method, an unknown variant, or any view but the unordered one without dates.
    """
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
    """The exact estimate of every number of every barrel, by one of the two algorithms.

    task: the frozen MethodTask.  view: the permitted view (the draws before the target).
    method: posterior_means (the first route) or posterior_means_by_recursion (the second, for verify()).
    Returns {barrel: {number: exact estimate}}, for example {'MAIN': {1: Fraction(41, 200), 2: Fraction(39, 200), ...}}.
    """
    lam = _lam(task)
    return {b.barrel_id: method(_barrel_draws(view, b.barrel_id), b.low, b.high, b.selected, lam)
            for b in get_profile(task.game_id).barrels}


def compute(task, view) -> MethodOutput:
    """Compute the estimates for one target draw, from the draws before it only.

    task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
    Returns a MethodOutput holding, for each barrel, every number's exact estimate rounded once to a float64, both as
    its score and as its published chance (the estimates of a barrel sum to the number drawn), for example
        MethodOutput(barrels={'MAIN': BarrelOutput(ranking=ScoredRanking({1: 0.205, 2: 0.195, ...}),
                                                   probability=ProbabilityVector([0.205, 0.195, ...], PROVENANCE))}).
    Unlike the other families it never returns an empty output: every number of every barrel always gets an estimate.
    """
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
