"""Shared helper, version 1: exact occurrence counts.

What this file is for
    It counts, for one barrel, how often each number was drawn: in the newest draws, in consecutive periods,
    or with weights that shrink with age. Every count has a second, differently written form that the methods
    use to check themselves. Exact whole numbers and fractions only, so every result is the same on every PC.

Which part of the specification it carries out
    The wave 1 design, doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md: section 3 (the rules
    these counts serve) and section 11 (the package, which lists what this helper holds).
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2 (a helper used by more
    than one family, versioned by its name).

Which of the project's own modules it uses
    None. It also reads nothing and starts nothing.

What uses it
    E_007/core_v1.py, E_008/core_v1.py, E_009/core_v1.py and E_010/core_v1.py; and tests/test_occurrence_counts.py.

The functions (the header this file had before the tidy-up, kept)
    Exact integers and fractions only (no floating point), so every result is the same on every platform. It
    imports nothing from the project, reads nothing and starts nothing.

    `draws` is the list of the labels drawn in one barrel at each eligible draw, oldest first; the newest draw
    has age 0. Labels run from `low` to `high`. Every function has a second, differently written form, which the
    methods' verify() uses:
      window_counts            count of each label in the newest S draws
      window_counts_by_prefix  the same, from running (prefix) totals
      decayed_counts           sum of lambda**age over the draws containing each label (direct powers)
      decayed_counts_by_recursion  the same, by s <- lambda*s + x
      period_counts            counts of each label in consecutive periods of P draws, counted back from the
                               newest draw (oldest period first); any older remainder is not used
      period_counts_by_index   the same, by assigning each draw to its period index

    A change to any behaviour here is a change to every method that uses it: each gets a new revision (E2R-R14A).
"""
from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction


def _check(draws: Sequence[Sequence[int]], low: int, high: int) -> None:
    """Refuse arguments that do not describe a barrel and its draws.

    draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's lowest and highest number.
    Returns nothing. Refuses (ValueError) a range that is not positive whole numbers, or a draw holding a repeated
    number or one outside the range.
    """
    if type(low) is not int or type(high) is not int or not 1 <= low <= high:
        raise ValueError('labels must be a positive integer range')
    for d in draws:
        if len(set(d)) != len(d) or any(type(x) is not int or not low <= x <= high for x in d):
            raise ValueError('each draw must hold distinct labels in range')


def _span(S: int, n: int) -> None:
    """Refuse a window that is not a whole number from 1 to the number of draws.

    S: the window, in draws.  n: how many draws there are.  Returns nothing; refuses (ValueError) otherwise.
    """
    if type(S) is not int or not 1 <= S <= n:
        raise ValueError(f'the window must be an integer from 1 to the number of draws ({n})')


def window_counts(draws, low, high, S):
    """How often each number was drawn in the newest S draws.

    draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's range.  S: the window.
    Returns {number: count}, every number of the barrel included, for example {1: 9, 2: 12, ..., 35: 10}.
    """
    _check(draws, low, high)
    _span(S, len(draws))
    counts = {j: 0 for j in range(low, high + 1)}
    for d in draws[len(draws) - S:]:
        for j in d:
            counts[j] += 1
    return counts


def window_counts_by_prefix(draws, low, high, S):
    """The same counts as window_counts, from running totals (the second route, for checking).

    draws, low, high, S: as for window_counts.
    Returns {number: count}, for example {1: 9, 2: 12, ..., 35: 10}.
    """
    _check(draws, low, high)
    _span(S, len(draws))
    out = {}
    for j in range(low, high + 1):
        prefix = [0]
        for d in draws:
            prefix.append(prefix[-1] + (1 if j in d else 0))
        out[j] = prefix[len(draws)] - prefix[len(draws) - S]
    return out


def _lam(lam) -> None:
    """Refuse a decay factor that is not an exact fraction strictly between 0 and 1.

    lam: the decay factor, for example Fraction(5, 6).  Returns nothing; refuses (ValueError) otherwise.
    """
    if type(lam) is not Fraction or not 0 < lam < 1:
        raise ValueError('lambda must be an exact fraction strictly between 0 and 1')


def decayed_counts(draws, low, high, lam):
    """Each number's count with every appearance weighted by lam to the power of its age.

    draws: the numbers drawn at each earlier draw, oldest first (the newest has age 0 and weight 1).
    low, high: the barrel's range.  lam: the decay factor.
    Returns {number: exact weighted count}, for example {1: Fraction(91, 36), 2: Fraction(5, 6), ...}.
    """
    _check(draws, low, high)
    _lam(lam)
    newest = len(draws) - 1
    out = {j: Fraction(0) for j in range(low, high + 1)}
    for i, d in enumerate(draws):
        w = lam ** (newest - i)
        for j in d:
            out[j] += w
    return out


def decayed_counts_by_recursion(draws, low, high, lam):
    """The same weighted counts as decayed_counts, by stepping through the draws (the second route).

    draws, low, high, lam: as for decayed_counts. At each draw every count is multiplied by lam, and 1 is added
    for a number that was drawn.
    Returns {number: exact weighted count}, for example {1: Fraction(91, 36), 2: Fraction(5, 6), ...}.
    """
    _check(draws, low, high)
    _lam(lam)
    out = {j: Fraction(0) for j in range(low, high + 1)}
    for d in draws:
        present = set(d)
        out = {j: lam * s + (1 if j in present else 0) for j, s in out.items()}
    return out


def _period(P: int, n_draws: int) -> int:
    """Check the period length and return how many whole periods the history holds.

    P: the period, in draws.  n_draws: how many draws there are.
    Returns the number of whole periods, for example 4 for P = 13 and 60 draws.
    Refuses (ValueError) a period that is not a positive whole number, or one longer than the history.
    """
    if type(P) is not int or P < 1 or n_draws < P:
        raise ValueError('the period must be a positive integer no longer than the history')
    return n_draws // P


def period_counts(draws, low, high, P):
    """How often each number was drawn in each period of P draws, counted back from the newest draw.

    draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's range.  P: the period.
    Returns {number: [count in each period, oldest period first]}, for example {1: [2, 4, 3, 1], 2: [3, 3, 2, 2], ...}.
    Draws older than the oldest whole period are not used.
    """
    _check(draws, low, high)
    n = _period(P, len(draws))
    start = len(draws) - n * P
    out = {j: [] for j in range(low, high + 1)}
    for b in range(n):
        block = draws[start + b * P:start + (b + 1) * P]
        for j in out:
            out[j].append(sum(1 for d in block if j in d))
    return out


def period_counts_by_index(draws, low, high, P):
    """The same counts as period_counts, by giving each draw its period number (the second route).

    draws, low, high, P: as for period_counts.
    Returns {number: [count in each period, oldest period first]}, for example {1: [2, 4, 3, 1], ...}.
    """
    _check(draws, low, high)
    n = _period(P, len(draws))
    out = {j: [0] * n for j in range(low, high + 1)}
    newest = len(draws) - 1
    for i, d in enumerate(draws):
        back = (newest - i) // P            # 0 for the newest period
        if back < n:
            for j in d:
                out[j][n - 1 - back] += 1
    return out
