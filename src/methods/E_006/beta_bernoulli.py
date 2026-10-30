"""E_6 revision 1: per-number Beta-Bernoulli posterior means, in exact rational arithmetic.

The mathematics only (specification section 2). It imports nothing from the project, reads nothing
and returns exact fractions; the caller rounds each one to a float64 exactly once.

For one barrel with labels low..high, `selected` labels drawn per draw, and the eligible draws before
the target listed oldest first (the last one is the newest, N - 1):
  r      = selected / L, the fair-draw inclusion rate, with L = high - low + 1
  prior  = Beta(r, 1 - r): centred on r and worth exactly one draw
  w(a)   = lam ** a for a draw that is a draws older than the newest (the newest has weight 1)
  k_j    = sum of w over the draws in which label j was drawn;  W = sum of w over all draws
  p_j    = (r + k_j) / (1 + W)
Because every draw selects exactly `selected` labels, sum_j k_j = selected * W, so sum_j p_j equals
`selected` exactly (7 for a main barrel, 1 for the Powerball). Nothing is renormalised.

For lam = 1 this is the ordinary conjugate Beta-Bernoulli posterior mean. For lam < 1 it is a discounted
(power-likelihood) Beta update: each draw's evidence enters with weight lam ** age, so it is not the
posterior of the plain independent-Bernoulli model (the reviewer's terminology note, EX_051).
"""
from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from types import MappingProxyType

# The fixed variants of revision 1 (specification section 2.5): variant_id -> forgetting factor lam.
# Changing or adding an entry is a code change and needs a new revision (E2R-R14A).
VARIANTS = MappingProxyType({
    'BETA_BERNOULLI_FULL_MEMORY_V1': Fraction(1),
    'BETA_BERNOULLI_DECAY_74_75_V1': Fraction(74, 75),
    'BETA_BERNOULLI_DECAY_149_150_V1': Fraction(149, 150),
})


def _check(draws: Sequence[Sequence[int]], low: int, high: int, selected: int, lam: Fraction) -> None:
    if type(lam) is not Fraction or not 0 < lam <= 1:
        raise ValueError('the forgetting factor must be an exact fraction in (0, 1]')
    if type(low) is not int or type(high) is not int or type(selected) is not int or not 1 <= selected <= high - low:
        raise ValueError('invalid barrel description')
    for i, labels in enumerate(draws):
        if (not isinstance(labels, (list, tuple)) or len(labels) != selected or len(set(labels)) != selected or
                any(type(x) is not int or not low <= x <= high for x in labels)):
            raise ValueError(f'draw {i}: needs {selected} distinct labels in {low}..{high}')


def posterior_means(draws: Sequence[Sequence[int]], low: int, high: int, selected: int,
                    lam: Fraction) -> dict[int, Fraction]:
    """The exact estimate p_j for every label (a posterior mean when lam = 1), by direct weights lam ** age."""
    _check(draws, low, high, selected, lam)
    r = Fraction(selected, high - low + 1)
    newest = len(draws) - 1
    k = {j: Fraction(0) for j in range(low, high + 1)}
    total = Fraction(0)
    for i, labels in enumerate(draws):
        w = lam ** (newest - i)          # exact: an integer power of an exact fraction
        total += w
        for j in labels:
            k[j] += w
    p = {j: (r + k[j]) / (1 + total) for j in k}
    if sum(p.values()) != selected:      # exact identity of the specification; never expected to fail
        raise ValueError('internal error: the posterior means do not sum to the selected count')
    return p


def posterior_means_by_recursion(draws: Sequence[Sequence[int]], low: int, high: int, selected: int,
                                 lam: Fraction) -> dict[int, Fraction]:
    """The same quantity by a different algorithm (k <- lam * k + x, oldest to newest), for verification."""
    _check(draws, low, high, selected, lam)
    k = [Fraction(0)] * (high - low + 1)
    total = Fraction(0)
    for labels in draws:
        drawn = set(labels)
        k = [lam * kj + (1 if low + i in drawn else 0) for i, kj in enumerate(k)]
        total = lam * total + 1
    r = Fraction(selected, high - low + 1)
    return {low + i: (r + kj) / (1 + total) for i, kj in enumerate(k)}
