#!/usr/bin/env python3
"""OUTLANDISH_01 Q4d pure reporting arithmetic, SYNTHETIC qualification stage.

NO file access, scanner, CLI, production profile, or Q5 authorisation.
Accept ONLY already-verified, classified matching facts from the Q3/Q4 pipeline.
The caller is responsible for source/drawset/manifest firewall validation.
The primary transition statistic is only PROPOSED, owner-vetoable before Q5.
"""
from __future__ import annotations

from bisect import bisect_left
from collections import Counter, defaultdict
from math import exp, fsum, isfinite, lgamma, log, log10, log1p
import random
import statistics
from typing import Iterable, Mapping

FAMILY_LENGTHS = {'K7S': 16, 'K7': 14, 'K6S': 14, 'K7mix': 14, 'K6': 12}
GAME_FAMILIES = {
    'powerball': {'K7S': 'P1', 'K7': 'P2', 'K6S': 'P3'},
    'oz': {'K7': 'O1', 'K7mix': 'O2', 'K6': 'O3'},
}
CONSTANTS = ('pi', 'phi', 'e', 'log2', 'gamma', 'lemniscate')
PRIMARY_FAMILY = {'powerball': 'K6S', 'oz': 'K6'}
# Owner D4 (16 Nov 2026), Powerball ONLY. Oz remains undecided.
GEOMETRIC_PRIMARY = 'P3_ANY_MEAN_LOG10_MIN_ABS_GAP_PLUS_ONE_V1'
MEDIAN_SECONDARY = 'P3_ANY_MEDIAN_MIN_ABS_GAP_V1'
# Owner D6 (16 Nov): three co-primary Oz views, one 18-test Holm family.
OZ_D6_VIEWS = ('O1_any', 'O2_any_slot', 'O3_any')
OZ_D6_FAMILIES = {'O1_any': 'K7', 'O2_any_slot': 'K7mix', 'O3_any': 'K6'}
OZ_D6_PRIMARY = 'OZ_D6_MEAN_LOG10_MIN_ABS_GAP_PLUS_ONE_V1'

# (view, original family, relative membership, patterns per draw, condition parent)
# A view represents DRAW-ATTRIBUTED event counts. Nesting is intentional.
VIEW_RULES = {
    'powerball': (
        ('P1_any', 'K7S', 'any', 5040, None),
        ('P1_drawn', 'K7S', 'drawn', 1, 'P1_any'),
        ('P1_reordered', 'K7S', 'reordered', 5039, None),
        ('P2_any', 'K7', 'any', 5040, None),
        ('P2_drawn', 'K7', 'drawn', 1, 'P2_any'),
        ('P2_reordered', 'K7', 'reordered', 5039, None),
        ('P3_any', 'K6S', 'any', 5040, None),
        ('P3_subsequence', 'K6S', 'subsequence', 7, 'P3_any'),
        ('P3_reordered', 'K6S', 'reordered', 5033, None),
    ),
    'oz': (
        ('O1_any', 'K7', 'any', 5040, None),
        ('O1_drawn', 'K7', 'drawn', 1, 'O1_any'),
        ('O1_reordered', 'K7', 'reordered', 5039, None),
        ('O2_any_slot', 'K7mix', 'any', 105840, None),
        ('O2_supplementary_last', 'K7mix', 'last', 15120, 'O2_any_slot'),
        ('O2_subsequence', 'K7mix', 'subsequence', 21, 'O2_supplementary_last'),
        ('O2_last_reordered', 'K7mix', 'last_reordered', 15099, None),
        ('O3_any', 'K6', 'any', 5040, None),
        ('O3_subsequence', 'K6', 'subsequence', 7, 'O3_any'),
        ('O3_reordered', 'K6', 'reordered', 5033, None),
    ),
}


def _draws(draw_numbers: Iterable[int]) -> tuple[int, ...]:
    ids = tuple(draw_numbers)
    if (not ids or any(type(v) is not int or v < 1 for v in ids)
            or any(right != left+1 for left, right in zip(ids, ids[1:]))):
        raise ValueError('drawset must be complete, strictly consecutive integer positions')
    return ids


def _events(events: Iterable, *, game: str, draws: tuple[int, ...], N: int) -> tuple:
    """Surface guards, not a replacement for Q3 classification or Q4 replay."""
    if game not in GAME_FAMILIES or type(N) is not int or N < 1:
        raise ValueError('invalid game/digit prefix')
    ret = tuple(events)
    known = set(draws)
    seen = set()
    old_key = None
    for item in ret:
        draw, family, start, digits = (item.draw_number, item.family,
                                       item.start_digit_offset, item.matched_digits)
        if type(draw) is not int or draw not in known or family not in GAME_FAMILIES[game]:
            raise ValueError('event has incorrect game/draw identity')
        L = FAMILY_LENGTHS[family]
        if (type(start) is not int or start < 0 or start+L > N
                or not isinstance(digits, str) or len(digits) != L
                or not digits.isascii() or not digits.isdecimal()):
            raise ValueError('event has invalid fixed-width digits/EOF')
        identity = (draw, family, start)
        key = (start, family, draw)
        if identity in seen or (old_key is not None and key < old_key):
            raise ValueError('duplicate or unsorted events')
        old_key = key
        seen.add(identity)
    return ret


def _view(c, rule: str) -> bool:
    if rule == 'any':
        return True
    if rule == 'drawn':
        return c.drawn_order is True
    if rule == 'subsequence':
        # Oz O2's relative subsequence additionally requires supplemental-last.
        return c.drawn_subsequence_order is True
    if rule == 'last':
        return c.supplementary_last is True
    if rule == 'last_reordered':
        return c.supplementary_last is True and c.drawn_subsequence_order is False
    if rule == 'reordered':
        return c.reordered_only is True
    raise ValueError('internal view rule unknown')


def binomial_two_sided(n: int, successes: int, q: float) -> float:
    """Exact binomial two-sided probability-order p, labelled APPROXIMATE as a model.

    Dependence of overlapping windows violates independence assumptions;
    the arithmetic is exact for Binomial(n,q), not a scientific calibration.
    """
    if (type(n) is not int or type(successes) is not int or not 0 <= successes <= n
            or not isinstance(q, (float,int)) or not 0 < q < 1):
        raise ValueError('invalid conditional binomial inputs')
    if n == 0:
        return 1.0
    lq, lr = log(q), log1p(-q)
    def lp(k):
        return lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)+k*lq+(n-k)*lr
    observed = lp(successes)
    eligible = [lp(k) for k in range(n+1) if lp(k) <= observed + 1e-10]
    maximum = max(eligible)
    return min(1.0, exp(maximum)*sum(exp(v-maximum) for v in eligible))


def category_summary(game: str, classified: Iterable, draws: Iterable[int],
                     N: int) -> tuple[dict, ...]:
    """Nesting-preserving views, event/offset/draw counts, model expectations."""
    ids = _draws(draws)
    classified = tuple(classified)
    events = _events((c.event for c in classified), game=game, draws=ids, N=N)
    for c, e in zip(classified, events):
        if c.category != GAME_FAMILIES[game][e.family]:
            raise ValueError('classification/family disagreement')
    counts: dict[str, int] = {}
    subsets = {}
    for name, family, membership, S, parent in VIEW_RULES[game]:
        selected = [e for e,c in zip(events,classified)
                    if e.family == family and _view(c, membership)]
        counts[name] = len(selected)
        subsets[name] = selected
    out = []
    for name, family, membership, S, parent in VIEW_RULES[game]:
        selected = subsets[name]
        L = FAMILY_LENGTHS[family]
        # This expectation is for draw-attributed EVENTS, not distinct offsets.
        exp_events = len(ids)*S*max(0,N-L+1)/(10**L)
        q = None
        observed_p = None
        conditional_expected = None
        if parent is not None:
            parent_S = next(s for view,_,_,s,_ in VIEW_RULES[game] if view == parent)
            q = S/parent_S
            conditional_expected = counts[parent]*q
            observed_p = binomial_two_sided(counts[parent], len(selected), q)
        out.append(dict(view=name, family=family, length=L, draw_count=len(ids),
                        eligible_starts_per_draw=max(0,N-L+1), sequences_per_draw=S,
                        events=len(selected), distinct_offsets=len({e.start_digit_offset for e in selected}),
                        distinct_draws=len({e.draw_number for e in selected}),
                        analytical_expected_events=exp_events,
                        conditional_parent=parent, conditional_q=q,
                        conditional_expected=conditional_expected,
                        conditional_binomial_two_sided_model_p=observed_p))
    return tuple(out)


def physical_overlaps(game: str, events: Iterable, draws: Iterable[int], N: int) -> dict:
    """Direct interval intersections within the SAME draw; never transitive closure."""
    ids = _draws(draws)
    ev = _events(events, game=game, draws=ids, N=N)
    per_draw = defaultdict(list)
    for x in ev:
        per_draw[x.draw_number].append(x)
    paircounts = Counter()
    direct = same = shifted = 0
    for _, ordered in per_draw.items():
        active = []
        for e in ordered:  # event input globally sorted by start
            start = e.start_digit_offset
            active = [old for old in active
                      if old.start_digit_offset + FAMILY_LENGTHS[old.family] > start]
            for prior in active:
                pair = tuple(sorted((prior.family, e.family)))
                paircounts['+'.join(pair)] += 1
                direct += 1
                if prior.start_digit_offset == e.start_digit_offset:
                    same += 1
                else:
                    shifted += 1
            active.append(e)
    return dict(events=len(ev), direct_same_draw_pairs=direct,
                same_start_pairs=same, shifted_start_pairs=shifted,
                family_pair_counts=dict(sorted(paircounts.items())))


def closest_gap(starts_a: Iterable[int], starts_b: Iterable[int]):
    """Select deterministic (abs(b-a), b-a, a, b) minimum in O(A log B)."""
    a = sorted(set(starts_a))
    b = sorted(set(starts_b))
    if not a or not b:
        return None
    if any(type(x) is not int or x < 0 for x in (*a,*b)):
        raise ValueError('invalid nonnegative offsets')
    best = None
    for start in a:
        i = bisect_left(b,start)
        for j in (i-1,i):
            if 0 <= j < len(b):
                other=b[j]
                candidate=(abs(other-start),other-start,start,other)
                if best is None or candidate < best:
                    best=candidate
    return best


def _transition_gaps(sets: Iterable[Iterable[int]]) -> list[int]:
    """Every evaluable adjacent pair contributes exactly one nonnegative gap."""
    seq = tuple(tuple(s) for s in sets)
    return [closest_gap(a, b)[0] for a, b in zip(seq, seq[1:]) if a and b]


def geometric_mean_log_gap(gaps: Iterable[int]) -> float | None:
    """D4 primary: mean log10(g+1), sorted + fsum, 12-decimal canonical result.

    This is log10 of the geometric mean of (g+1), NOT log10(mean(g)+1).
    Zero gaps contribute log10(1)=0. Empty/evaluable-free input is N/A.
    """
    ordered = sorted(gaps)
    if not ordered:
        return None
    if any(type(g) is not int or g < 0 for g in ordered):
        raise ValueError('adjacent-pair gaps must be nonnegative integers')
    return round(fsum(log10(g + 1) for g in ordered) / len(ordered), 12)


def _transition_summaries(sets: Iterable[Iterable[int]]):
    gaps = _transition_gaps(sets)
    return statistics.median(gaps) if gaps else None, len(gaps)


def transitions(game: str, events: Iterable, draw_numbers: Iterable[int], N: int,
                *, family: str | None = None):
    ids = _draws(draw_numbers)
    events = _events(events, game=game, draws=ids, N=N)
    selected_family = PRIMARY_FAMILY[game] if family is None else family
    if selected_family not in GAME_FAMILIES[game]:
        raise ValueError('wrong transition family for game')
    offsets = defaultdict(list)
    for e in events:
        if e.family == selected_family:
            offsets[e.draw_number].append(e.start_digit_offset)
    sets=tuple(tuple(sorted(set(offsets[i]))) for i in ids)
    rows=[]
    gaps=[]
    for i, (a,b) in enumerate(zip(sets,sets[1:])):
        pair=closest_gap(a,b)
        if pair is not None:
            gaps.append(pair[0])
        rows.append(dict(W=ids[i], W_plus_1=ids[i+1],
                         count_W=len(a), count_next=len(b),
                         evaluable=pair is not None,
                         minimum_abs_gap=None if pair is None else pair[0],
                         signed_gap=None if pair is None else pair[1],
                         start_W=None if pair is None else pair[2],
                         start_next=None if pair is None else pair[3],
                         zero_physical_gap=pair is not None and pair[0] == 0))
    meta=dict(game=game, family=selected_family, total_adjacent_pairs=len(rows),
              evaluable_pairs=len(gaps), non_evaluable_pairs=len(rows)-len(gaps),
              observed_median_absolute_gap=statistics.median(gaps) if gaps else None,
              # D4 Powerball primary; event extraction and adjacent-pair rows unchanged.
              observed_primary_mean_log10_gap_plus_one=(geometric_mean_log_gap(gaps)
                  if (game == 'powerball' and selected_family == 'K6S') or
                     (game == 'oz' and selected_family in OZ_D6_FAMILIES.values()) else None),
              undefined_reason=None if gaps else 'NO_EVALUABLE_ADJACENT_PAIRS')
    return tuple(rows), meta, sets


def permutation_test(offsets_per_draw: Iterable[Iterable[int]], *, seed: int,
                     iterations: int = 10_000, geometric_primary: bool = False) -> dict:
    """Shuffle whole draw-offset sets, including empty draws, once per trial.

    The legacy median output fields are preserved verbatim. When
    geometric_primary=True, the SAME shuffle loop additionally computes the
    owner-D4 Powerball primary, alongside the old median as an exploratory
    secondary with a separate centred two-sided p-value. Oz's old Q4d callers
    retain the median-only default until an explicit Oz owner decision.
    """
    sets = tuple(tuple(sorted(set(s))) for s in offsets_per_draw)
    if (len(sets) < 2 or type(seed) is not int or not 0 <= seed < 2**64
            or type(iterations) is not int or not 1 <= iterations <= 1_000_000
            or type(geometric_primary) is not bool):
        raise ValueError('invalid permutation configuration')
    if any(type(v) is not int or v < 0 for s in sets for v in s):
        raise ValueError('invalid offsets')
    observed_gaps = _transition_gaps(sets)
    observed = statistics.median(observed_gaps) if observed_gaps else None
    n_observed = len(observed_gaps)
    geometric_observed = (geometric_mean_log_gap(observed_gaps)
                          if geometric_primary else None)
    rng = random.Random(seed)
    valid = []
    geometric_valid = []
    evaluated_counts = []
    for _ in range(iterations):
        shuffled = list(sets)  # every draw, including zero-match draws
        rng.shuffle(shuffled)
        gaps = _transition_gaps(shuffled)
        evaluated_counts.append(len(gaps))
        if gaps:
            valid.append(statistics.median(gaps))
            if geometric_primary:
                geometric_valid.append(geometric_mean_log_gap(gaps))
    invalid = iterations - len(valid)
    answer = dict(seed=seed, generator='PYTHON_RANDOM_SHUFFLE_WHOLE_DRAW_SETS_V1',
                  iterations_requested=iterations, valid_permutations=len(valid),
                  undefined_permutations=invalid, observed_evaluable_pairs=n_observed,
                  permutation_evaluable_min=min(evaluated_counts),
                  permutation_evaluable_max=max(evaluated_counts),
                  observed_median=observed, permuted_median_center=None,
                  tail_upper_inclusive=None, tail_lower_inclusive=None,
                  centered_two_sided_p=None, undefined_reason=None)
    if observed is None:
        answer['undefined_reason'] = 'OBSERVED_NO_EVALUABLE_ADJACENT_PAIRS'
    elif not valid:
        answer['undefined_reason'] = 'NO_VALID_PERMUTATIONS'
    else:
        mid = statistics.median(valid)
        extreme = sum(abs(v - mid) >= abs(observed - mid) for v in valid)
        answer.update(permuted_median_center=mid,
                      centered_two_sided_p=(1 + extreme) / (len(valid) + 1),
                      tail_upper_inclusive=(1 + sum(v >= observed for v in valid)) / (len(valid) + 1),
                      tail_lower_inclusive=(1 + sum(v <= observed for v in valid)) / (len(valid) + 1))
    if geometric_primary:
        # Both summaries are defined on the same evaluable pairs; a single
        # trial is included/excluded together for both statistics.
        if len(geometric_valid) != len(valid):
            raise AssertionError('dual permutation evaluability disagreement')
        g = dict(statistic=GEOMETRIC_PRIMARY,
                 observed=geometric_observed,
                 permuted_median_center=None,
                 tail_upper_inclusive=None,
                 tail_lower_inclusive=None,
                 centered_two_sided_p=None,
                 undefined_reason=answer['undefined_reason'])
        if observed is not None and valid:
            # All geometric statistics have already been rounded to 12 places;
            # round the permutation centre too before ANY tail comparison.
            centre = round(statistics.median(geometric_valid), 12)
            extreme = sum(abs(v - centre) >= abs(geometric_observed - centre)
                          for v in geometric_valid)
            g.update(permuted_median_center=centre,
                     centered_two_sided_p=(1 + extreme) / (len(valid) + 1),
                     tail_upper_inclusive=(1 + sum(v >= geometric_observed for v in geometric_valid)) / (len(valid) + 1),
                     tail_lower_inclusive=(1 + sum(v <= geometric_observed for v in geometric_valid)) / (len(valid) + 1))
        answer['geometric_primary'] = g
        answer['median_secondary'] = dict(statistic=MEDIAN_SECONDARY,
                                          observed=observed,
                                          permuted_median_center=answer['permuted_median_center'],
                                          centered_two_sided_p=answer['centered_two_sided_p'],
                                          tail_upper_inclusive=answer['tail_upper_inclusive'],
                                          tail_lower_inclusive=answer['tail_lower_inclusive'],
                                          undefined_reason=answer['undefined_reason'])
    return answer


def oz_three_family_permutation(sets_by_view: Mapping[str, Iterable[Iterable[int]]],
                                *, seed: int, iterations: int = 10_000) -> dict:
    """D6: ONE common shuffle per trial, applied identically to all three views.

    Uses existing adjacent-pair gap and D4 geometric-mean calculation;
    no median/secondary test. Undefined trials are excluded per view.
    """
    if (not isinstance(sets_by_view, Mapping) or set(sets_by_view) != set(OZ_D6_VIEWS)
            or type(seed) is not int or not 0 <= seed < 2**64
            or type(iterations) is not int or not 1 <= iterations <= 1_000_000):
        raise ValueError('invalid Oz D6 permutation identity')
    ordered = {view: tuple(tuple(sorted(set(row))) for row in sets_by_view[view])
               for view in OZ_D6_VIEWS}
    draw_counts = {len(rows) for rows in ordered.values()}
    if len(draw_counts) != 1 or next(iter(draw_counts)) < 2:
        raise ValueError('Oz three views require the same complete drawset')
    if any(type(offset) is not int or offset < 0
           for rows in ordered.values() for one in rows for offset in one):
        raise ValueError('invalid Oz event offset')
    n = next(iter(draw_counts))
    observed_gaps = {v: _transition_gaps(ordered[v]) for v in OZ_D6_VIEWS}
    observed = {v: geometric_mean_log_gap(observed_gaps[v]) for v in OZ_D6_VIEWS}
    valid = {v: [] for v in OZ_D6_VIEWS}
    evaluated = {v: [] for v in OZ_D6_VIEWS}
    rng = random.Random(seed)
    for _ in range(iterations):
        indices = list(range(n))
        rng.shuffle(indices)
        for view in OZ_D6_VIEWS:
            gaps = _transition_gaps(ordered[view][j] for j in indices)
            evaluated[view].append(len(gaps))
            if gaps:
                valid[view].append(geometric_mean_log_gap(gaps))
    views = {}
    for view in OZ_D6_VIEWS:
        ok = valid[view]
        why = ('OBSERVED_NO_EVALUABLE_ADJACENT_PAIRS' if observed[view] is None
               else 'NO_VALID_PERMUTATIONS' if not ok else None)
        info = dict(statistic=OZ_D6_PRIMARY, event_view=view,
                    observed=observed[view],
                    observed_evaluable_pairs=len(observed_gaps[view]),
                    valid_permutations=len(ok),
                    undefined_permutations=iterations-len(ok),
                    permutation_evaluable_min=min(evaluated[view]),
                    permutation_evaluable_max=max(evaluated[view]),
                    permuted_median_center=None, tail_upper_inclusive=None,
                    tail_lower_inclusive=None, centered_two_sided_p=None,
                    undefined_reason=why)
        if why is None:
            centre = round(statistics.median(ok), 12)
            value = observed[view]
            extreme = sum(abs(z-centre) >= abs(value-centre) for z in ok)
            info.update(permuted_median_center=centre,
                        centered_two_sided_p=(1+extreme)/(len(ok)+1),
                        tail_upper_inclusive=(1+sum(z>=value for z in ok))/(len(ok)+1),
                        tail_lower_inclusive=(1+sum(z<=value for z in ok))/(len(ok)+1))
        views[view] = info
    return dict(seed=seed, generator='PYTHON_RANDOM_SHUFFLE_WHOLE_DRAW_SETS_V1',
                iterations_requested=iterations, views=views)


def holm_adjusted(pvalues: Mapping[str, float | None],
                  hypothesis_order: Iterable[str]) -> dict[str, float | None]:
    """Fixed explicit hypothesis roster, including N/A as p=1.

    May be six (Powerball per-statistic) or eighteen (Oz 3 x 6).
    """
    order_given = tuple(hypothesis_order)
    if (not isinstance(pvalues, Mapping) or not order_given
            or len(set(order_given)) != len(order_given)
            or set(pvalues) != set(order_given)):
        raise ValueError('Holm requires the exact explicit family')
    for p in pvalues.values():
        if p is not None and (type(p) not in (float, int)
                              or not isfinite(p) or not 0 <= p <= 1):
            raise ValueError('invalid raw p-value')
    ranking = sorted(order_given,
                     key=lambda k: ((1.0 if pvalues[k] is None else pvalues[k]), k))
    adjusted = {}
    running = 0.0
    size = len(ranking)
    for rank, key in enumerate(ranking):
        raw = 1.0 if pvalues[key] is None else pvalues[key]
        running = max(running, min(1.0, (size-rank)*raw))
        adjusted[key] = None if pvalues[key] is None else running
    return {key: adjusted[key] for key in order_given}


def holm_six_constants(pvalues: Mapping[str, float | None]) -> dict[str, float | None]:
    """Backward-compatible Powerball family of exactly six constants."""
    return holm_adjusted(pvalues, CONSTANTS)


def decoy_count_tails(real_count: int, decoy_counts: Iterable[int]) -> dict:
    """Finite-sample inclusive tails of genuine REAL summary vs separate NULLs."""
    counts=tuple(decoy_counts)
    if (type(real_count) is not int or real_count < 0 or not counts
            or any(type(v) is not int or v < 0 for v in counts)):
        raise ValueError('invalid REAL/NULL count comparison')
    k=len(counts)
    return dict(K=k, real_count=real_count, decoy_min=min(counts),decoy_max=max(counts),
                upper_inclusive_p=(1+sum(v>=real_count for v in counts))/(k+1),
                lower_inclusive_p=(1+sum(v<=real_count for v in counts))/(k+1),
                comparison='SUMMARY_COUNTS_ONLY_NOT_RAW_EVENT_JOIN')


if __name__=='__main__':
    raise SystemExit('No runnable report on production inputs; use synthetic qualification harness')
