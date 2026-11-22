"""Shared helper, revision 1: exact polynomial fits to a short series (E_3 and E_4; design note v0.1 section 3).

Exact rational arithmetic only (fractions.Fraction): no floating point, no library solver, so every result is
the same on every platform. It imports nothing from the project, reads nothing and starts nothing.

A polynomial is returned as its coefficients [a_0, a_1, ..., a_D] in the variable t, so p(t) = sum a_k t^k.
The methods place the window's draws at t = -M..-1 and the target at t = 0, so p(0) = a_0 is the fitted value
at the target and p'(0) = a_1 is the fitted slope there.

Fits:
  least_squares               normal equations (one factorisation shared by every series of the same window)
  least_squares_by_recurrence the same result by Forsythe's orthogonal-polynomial recurrence (for verification)
  interpolate                 Lagrange form through D + 1 points
  interpolate_newton          the same result by Newton divided differences (for verification)
  minimax                     discrete Chebyshev (minimax) approximation by Stiefel's single-point exchange
  minimax_certificate         the alternation-theorem check that a polynomial is the minimax one

A change to any behaviour here is a change to every method that uses it: each gets a new revision (E2R-R14A).
"""
from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

MINIMAX_EXCHANGE_CAP = 10000


# ---------------------------------------------------------------- inputs and small tools

def abscissae(window: int) -> list[Fraction]:
    """t = -window .. -1 for the window's draws, oldest first; the target is t = 0."""
    if type(window) is not int or window < 1:
        raise ValueError('the window must be a positive integer')
    return [Fraction(i - window) for i in range(window)]


def smoothed(series: Sequence, half_width: int) -> list[Fraction]:
    """S_i = the mean of series[i - h .. i + h], clipped to the series (no value outside it is used)."""
    if type(half_width) is not int or half_width < 0:
        raise ValueError('the half-width must be a non-negative integer')
    n = len(series)
    return [Fraction(sum(series[max(0, i - half_width):min(n, i + half_width + 1)]),
                     min(n, i + half_width + 1) - max(0, i - half_width)) for i in range(n)]


def _check(ts: Sequence, ys: Sequence, degree: int, need: int) -> None:
    if type(degree) is not int or degree < 0:
        raise ValueError('the degree must be a non-negative integer')
    if len(ts) != len(ys) or len(ts) < need:
        raise ValueError(f'needs at least {need} points and one value per point')
    if any(type(t) is not Fraction for t in ts) or len(set(ts)) != len(ts):
        raise ValueError('abscissae must be distinct exact fractions')
    if any(type(y) not in (int, Fraction) for y in ys):
        raise ValueError('values must be exact (int or Fraction)')


def evaluate(coeffs: Sequence[Fraction], t: Fraction) -> Fraction:
    value = Fraction(0)
    for c in reversed(coeffs):
        value = value * t + c
    return value


def _solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Exact Gauss-Jordan elimination; the first non-zero pivot in each column (no choice by size)."""
    n = len(matrix)
    m = [list(row) + [v] for row, v in zip(matrix, rhs)]
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            raise ValueError('singular system')
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return [m[i][n] for i in range(n)]


# ---------------------------------------------------------------- least squares

class LeastSquares:
    """Least squares of degree D at fixed abscissae: the normal matrix is inverted once and reused."""

    def __init__(self, ts: Sequence[Fraction], degree: int):
        _check(ts, [0] * len(ts), degree, degree + 1)
        self.ts, self.degree = list(ts), degree
        powers = [[t ** k for k in range(2 * degree + 1)] for t in self.ts]
        normal = [[sum(p[a + b] for p in powers) for b in range(degree + 1)] for a in range(degree + 1)]
        self._rows = [[p[a] for a in range(degree + 1)] for p in powers]
        self._inverse = [_solve(normal, [Fraction(int(i == j)) for i in range(degree + 1)]) for j in range(degree + 1)]

    def fit(self, ys: Sequence) -> list[Fraction]:
        _check(self.ts, ys, self.degree, self.degree + 1)
        rhs = [sum(row[a] * y for row, y in zip(self._rows, ys)) for a in range(self.degree + 1)]
        # self._inverse[j] is column j of the inverse; coefficient a = sum_j inverse[a][j] * rhs[j]
        return [sum(self._inverse[j][a] * rhs[j] for j in range(self.degree + 1)) for a in range(self.degree + 1)]


def least_squares(ts: Sequence[Fraction], ys: Sequence, degree: int) -> list[Fraction]:
    return LeastSquares(ts, degree).fit(ys)


def least_squares_by_recurrence(ts: Sequence[Fraction], ys: Sequence, degree: int) -> list[Fraction]:
    """Forsythe: orthogonal polynomials P_0 = 1, P_1 = t - alpha_1, P_{k+1} = (t - alpha_{k+1}) P_k - beta_k P_{k-1}."""
    _check(ts, ys, degree, degree + 1)

    def at(poly, t):
        return evaluate(poly, t)

    def mul_t_minus(poly, a):                     # (t - a) * poly, as coefficients
        out = [Fraction(0)] * (len(poly) + 1)
        for k, c in enumerate(poly):
            out[k + 1] += c
            out[k] -= a * c
        return out

    def axpy(x, a, y):                            # x + a * y, padded
        n = max(len(x), len(y))
        x, y = x + [Fraction(0)] * (n - len(x)), y + [Fraction(0)] * (n - len(y))
        return [xi + a * yi for xi, yi in zip(x, y)]

    polys, norms = [], []
    prev, cur = None, [Fraction(1)]
    for k in range(degree + 1):
        vals = [at(cur, t) for t in ts]
        norm = sum(v * v for v in vals)
        polys.append(cur)
        norms.append(norm)
        if k == degree:
            break
        alpha = sum(t * v * v for t, v in zip(ts, vals)) / norm
        nxt = mul_t_minus(cur, alpha)
        if prev is not None:
            nxt = axpy(nxt, -(norm / norms[k - 1]), prev)
        prev, cur = cur, nxt
    coeffs = [Fraction(0)] * (degree + 1)
    for poly, norm in zip(polys, norms):
        c = sum(y * at(poly, t) for t, y in zip(ts, ys)) / norm
        coeffs = axpy(coeffs, c, poly)
    return coeffs[:degree + 1]


# ---------------------------------------------------------------- interpolation

def interpolate(ts: Sequence[Fraction], ys: Sequence) -> list[Fraction]:
    """The polynomial of degree len(ts) - 1 through the points, as coefficients (Lagrange form expanded)."""
    _check(ts, ys, len(ts) - 1, 1)
    n = len(ts)
    coeffs = [Fraction(0)] * n
    for i in range(n):
        basis, denom = [Fraction(1)], Fraction(1)
        for j in range(n):
            if j != i:
                basis = [Fraction(0)] + basis                     # multiply by t ...
                for k in range(len(basis) - 1):
                    basis[k] -= ts[j] * basis[k + 1]              # ... minus t_j
                denom *= ts[i] - ts[j]
        for k in range(n):
            coeffs[k] += ys[i] * basis[k] / denom
    return coeffs


def interpolate_newton(ts: Sequence[Fraction], ys: Sequence) -> list[Fraction]:
    """The same polynomial by Newton divided differences (for verification)."""
    _check(ts, ys, len(ts) - 1, 1)
    n = len(ts)
    dd = [Fraction(y) for y in ys]
    for level in range(1, n):
        for i in range(n - 1, level - 1, -1):
            dd[i] = (dd[i] - dd[i - 1]) / (ts[i] - ts[i - level])
    coeffs = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):                                # Horner on the Newton form
        shifted = [Fraction(0)] + coeffs[:-1]
        coeffs = [s - ts[i] * c for s, c in zip(shifted, coeffs)]
        coeffs[0] += dd[i]
    return coeffs


# ---------------------------------------------------------------- minimax (discrete Chebyshev approximation)

def minimax(ts: Sequence[Fraction], ys: Sequence, degree: int) -> tuple[list[Fraction], Fraction, list[int]]:
    """Minimise max_i |ys[i] - p(ts[i])| over polynomials of degree <= D, by Stiefel's single-point exchange.

    Returns (coefficients, the minimax error, the final reference indices). The points must be given in
    increasing order of t. Deterministic: the initial reference is fixed, the largest error is taken at its
    lowest index, and the exchange rules below have no free choices. The levelled error |h| increases strictly
    at each exchange, so the loop ends; the cap is a safeguard that is never expected to be reached.
    """
    n, m = len(ts), degree + 2
    _check(ts, ys, degree, m)
    if any(ts[i] >= ts[i + 1] for i in range(n - 1)):
        raise ValueError('abscissae must be increasing')
    ref = [(2 * k * (n - 1) + (m - 1)) // (2 * (m - 1)) for k in range(m)]   # round(k (n-1)/(m-1)), halves up
    if len(set(ref)) != m:
        raise ValueError('internal error: the initial reference is not distinct')
    for _ in range(MINIMAX_EXCHANGE_CAP):
        system = [[ts[r] ** j for j in range(degree + 1)] + [Fraction((-1) ** k)] for k, r in enumerate(ref)]
        solution = _solve(system, [Fraction(ys[r]) for r in ref])
        coeffs, h = solution[:-1], solution[-1]
        errors = [ys[i] - evaluate(coeffs, ts[i]) for i in range(n)]
        worst = max(range(n), key=lambda i: (abs(errors[i]), -i))
        if abs(errors[worst]) <= abs(h):
            return coeffs, abs(h), ref
        sign_h = 1 if h >= 0 else -1

        def sigma(k):                              # the sign the error must have at reference position k
            return sign_h * (1 if k % 2 == 0 else -1)
        s = 1 if errors[worst] > 0 else -1
        if worst < ref[0]:
            ref = [worst] + ref[1:] if s == sigma(0) else [worst] + ref[:-1]
        elif worst > ref[-1]:
            ref = ref[:-1] + [worst] if s == sigma(m - 1) else ref[1:] + [worst]
        else:
            k = next(k for k in range(m - 1) if ref[k] < worst < ref[k + 1])
            if s == sigma(k):
                ref[k] = worst
            else:
                ref[k + 1] = worst
    raise RuntimeError('minimax exchange did not converge within the cap')


def minimax_certificate(ts: Sequence[Fraction], ys: Sequence, coeffs: Sequence[Fraction], degree: int) -> Fraction:
    """Raise ValueError unless coeffs is the minimax polynomial of degree <= D (the alternation theorem):
    its error reaches its maximum E at D + 2 points, in increasing t, with alternating signs (or E = 0).
    Returns E."""
    _check(ts, ys, degree, degree + 2)
    if len(coeffs) != degree + 1:
        raise ValueError('wrong number of coefficients')
    errors = [ys[i] - evaluate(coeffs, ts[i]) for i in range(len(ts))]
    top = max(abs(e) for e in errors)
    if top == 0:
        return top
    order = sorted(range(len(ts)), key=lambda i: ts[i])
    signs = [1 if errors[i] > 0 else -1 for i in order if abs(errors[i]) == top]
    alternations = 1 + sum(1 for a, b in zip(signs, signs[1:]) if a != b)
    if alternations < degree + 2:
        raise ValueError(f'not minimax: the maximum error alternates only {alternations} times, needs {degree + 2}')
    return top
