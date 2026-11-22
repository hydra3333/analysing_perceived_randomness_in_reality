"""Shared helper, revision 1: exact occurrence counts for E_7, E_8, E_9 and E_10 (wave 1 design note v0.1r1).

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
    if type(low) is not int or type(high) is not int or not 1 <= low <= high:
        raise ValueError('labels must be a positive integer range')
    for d in draws:
        if len(set(d)) != len(d) or any(type(x) is not int or not low <= x <= high for x in d):
            raise ValueError('each draw must hold distinct labels in range')


def _span(S: int, n: int) -> None:
    if type(S) is not int or not 1 <= S <= n:
        raise ValueError(f'the window must be an integer from 1 to the number of draws ({n})')


def window_counts(draws, low, high, S):
    _check(draws, low, high)
    _span(S, len(draws))
    counts = {j: 0 for j in range(low, high + 1)}
    for d in draws[len(draws) - S:]:
        for j in d:
            counts[j] += 1
    return counts


def window_counts_by_prefix(draws, low, high, S):
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
    if type(lam) is not Fraction or not 0 < lam < 1:
        raise ValueError('lambda must be an exact fraction strictly between 0 and 1')


def decayed_counts(draws, low, high, lam):
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
    _check(draws, low, high)
    _lam(lam)
    out = {j: Fraction(0) for j in range(low, high + 1)}
    for d in draws:
        present = set(d)
        out = {j: lam * s + (1 if j in present else 0) for j, s in out.items()}
    return out


def _period(P: int, n_draws: int) -> int:
    if type(P) is not int or P < 1 or n_draws < P:
        raise ValueError('the period must be a positive integer no longer than the history')
    return n_draws // P


def period_counts(draws, low, high, P):
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
