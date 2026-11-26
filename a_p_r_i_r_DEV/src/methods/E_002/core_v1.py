"""E_2 (Expected Recurrence-Interval Alignment): the family's shared calculation, used by every E_2 variant.

What this file is for
    It holds the whole calculation of E_2. compute() turns the draws before a target into one score for
    every number of every barrel; verify() works the same scores out again by a second, differently written
    route and refuses the record if they differ. Each variant's own method.py passes its task here, and the
    variant's fixed settings are looked up, by the task's variant ID, in E_002/variants.py.

Which part of the specification it carries out
    The method: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md section 4.1.
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2 (a family's shared
    core file).

Which of the project's own modules it uses
    E_002.variants              VARIANTS: each variant's fixed settings
    _shared.recurrence_gaps_v1  each number's appearances, gaps and age at the target; exposures by age; age bins
    _common.contract_forecast   the types a method returns (MethodOutput, BarrelOutput, ScoredRanking)
    _common.game_profiles       get_profile: each game's barrels (lowest and highest number, how many are drawn)

What uses it
    E_002/<VARIANT>/method.py of every E_2 variant, and this family's tests.

How it computes (the header this file had before the tidy-up, kept)
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
from _shared import recurrence_gaps_v1 as RG
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

# The fixed identity and output settings of this family; they never change:
#   METHOD_ID                the method's ID as the records name it
#   OBSERVATION_VIEW         the view of the earlier draws this family accepts: numbers as a set, no dates
#   PUBLISHES_PROBABILITIES  whether the scores are also published as chances (only where they sum to the number drawn)
#   PROVENANCE               the text stored with the published values, saying how they were computed
METHOD_ID = 'E_2'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = False
PROVENANCE = 'E_2 r1 (Expected Recurrence-Interval Alignment): exact rational arithmetic, each value rounded once to float64'


def _config(task):
    """Check that the task is for this family and return the variant's fixed settings.

    task: the frozen MethodTask the research code built (method, variant, observation view).
    Returns the variant's line of VARIANTS, for example ('mean', None, 104), which holds, in order:
        the statistic ("mean" or "median"), the last n gaps used (None for all), the minimum history.
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


def _median_by_sorting(g):
    """The median of a list of gap lengths, by sorting them.

    g: the gaps, for example [3, 9, 4].
    Returns the middle value as a Fraction, for example Fraction(4); for an even count, the mean of the two middle
    values, for example Fraction(7, 2) for [3, 4].
    """
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
    """The exact score of every number of one barrel.

    A number's score is minus the distance between the number's age at the target and its usual gap, as a share of that
    gap.
    draws: the numbers drawn in this barrel at each earlier draw, oldest first.
    b: the barrel (its lowest and highest number, and how many are drawn).
    cfg: the variant's settings, as _config() returns them.
    second: False for the first route; True for the second, differently written route that verify() uses.
    Returns {number: exact score}, for example {1: Fraction(-2, 5), 2: Fraction(-1, 10), ...}.
    """
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
