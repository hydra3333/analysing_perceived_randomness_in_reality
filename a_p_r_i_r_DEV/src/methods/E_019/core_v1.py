"""E_19 (Periodic Recurrence-Hazard Peaks): the family's shared calculation, used by every E_19 variant.

What this file is for
    It holds the whole calculation of E_19. compute() turns the draws before a target into one score for
    every number of every barrel; verify() works the same scores out again by a second, differently written
    route and refuses the record if they differ. Each variant's own method.py passes its task here, and the
    variant's fixed settings are looked up, by the task's variant ID, in E_019/variants.py.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md section 4.3.
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2 (a family's shared
    core file).

Which of the project's own modules it uses
    E_019.variants              VARIANTS: each variant's fixed settings
    _shared.recurrence_gaps_v1  each number's appearances, gaps and age at the target; exposures by age; age bins
    _common.contract_forecast   the types a method returns (MethodOutput, BarrelOutput, ScoredRanking)
    _common.game_profiles       get_profile: each game's barrels (lowest and highest number, how many are drawn)

What uses it
    E_019/<VARIANT>/method.py of every E_19 variant, and this family's tests.

How it computes (the header this file had before the tidy-up, kept)
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
from _shared import recurrence_gaps_v1 as RG
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

# The fixed identity and output settings of this family; they never change:
#   METHOD_ID                the method's ID as the records name it
#   OBSERVATION_VIEW         the view of the earlier draws this family accepts: numbers as a set, no dates
#   PUBLISHES_PROBABILITIES  whether the scores are also published as chances (only where they sum to the number drawn)
#   PROVENANCE               the text stored with the published values, saying how they were computed
METHOD_ID = 'E_19'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = False
PROVENANCE = 'E_19 r1 (Periodic Recurrence-Hazard Peaks): exact rational arithmetic, each value rounded once to float64'


def _config(task):
    """Check that the task is for this family and return the variant's fixed settings.

    task: the frozen MethodTask the research code built (method, variant, observation view).
    Returns the variant's line of VARIANTS, for example (2, Fraction(100), Fraction(20), 104), which holds, in order:
        the cycle T, the trend prior c, the shrinkage d, the minimum history.
    Refuses (ValueError) a task for another method, an unknown variant, or any view but the unordered one without dates.
    """
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
    """The exact score of every number of one barrel.

    A number's score is the trend hazard at the number's age times its own factor for that age's place in the cycle.
    draws: the numbers drawn in this barrel at each earlier draw, oldest first.
    b: the barrel (its lowest and highest number, and how many are drawn).
    cfg: the variant's settings, as _config() returns them.
    second: False for the first route; True for the second, differently written route that verify() uses.
    Returns {number: exact score}, for example {1: Fraction(21, 100), 2: Fraction(9, 50), ...}.
    """
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
    """Compute the scores for one target draw, from the draws before it only.

    task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
    Returns a MethodOutput holding, for each barrel, every number's exact score rounded once to a float64, for example
        MethodOutput(barrels={'MAIN': BarrelOutput(ranking=ScoredRanking({1: 0.2019, 2: 0.1827, ...}))}).
    With fewer earlier draws than the variant's minimum it returns MethodOutput(barrels={}), which is recorded as
    INSUFFICIENT_HISTORY.
    """
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
