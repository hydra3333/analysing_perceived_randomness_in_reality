"""Shared gaps helper, revision 1 (wave 2 design note v0.1r2 sections 3, 4.2 and 10). Exact arithmetic only.

Used by E_2, E_17, E_18 and E_19 (revision 1 of each); a change here is a new revision of every user (E2R-R14A).
A history is a list of draws, oldest first; each draw is the list of labels drawn from one barrel low..high.
Positions run 1..W; the target is position W + 1.

- Appearances, completed gaps, gaps inside a window, projected ages (3.1, 3.2). A never-seen label is treated as
  last seen at position 0, so its projected age is W + 1.
- Exposures by age (3.3), by two routes: a per-draw walk, and from completed gaps plus the open stretch. The
  stretch before a label's first appearance (unknown age) is excluded; the open stretch counts as at risk
  without an event.
- Age bins (3.4): upper edges are the distinct values ceil(f L/K), f = 1/5, 2/5, 3/5, 1, 8/5, 13/5.
- The certified sign of sum_k a_k ln k (4.2, 10): route 1 by prime exponents from trial division and bounds on
  each ln p; route 2 by its own exact-zero test (prime exponents from a smallest-prime-factor sieve) and then
  bounds on each ln k directly. Both refuse, as a ValueError, if MAX_TERMS series terms do not certify a sign.
Nothing here reads a file, starts a process or uses floating point.
"""
from __future__ import annotations

from fractions import Fraction

BIN_FACTORS = (Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(1), Fraction(8, 5), Fraction(13, 5))
FIRST_TERMS = 8
MAX_TERMS = 1024


def _checked(draws, low, high):
    if not (isinstance(low, int) and isinstance(high, int) and 1 <= low <= high):
        raise ValueError('the barrel must be a range of positive whole numbers')
    for d in draws:
        if len(set(d)) != len(d) or any(not (isinstance(x, int) and low <= x <= high) for x in d):
            raise ValueError('a draw holds a repeated or out-of-range label')
    return draws


# ---------------------------------------------------------------- appearances, gaps and ages
def appearances(draws, low, high):
    """{label: ascending positions 1..W at which it was drawn}."""
    app = {j: [] for j in range(low, high + 1)}
    for i, d in enumerate(_checked(draws, low, high), 1):
        for x in d:
            app[x].append(i)
    return app


def completed_gaps(app):
    return {j: [b - a for a, b in zip(p, p[1:])] for j, p in app.items()}


def gaps_in_window(app, W, window):
    """Completed gaps with both appearances inside the newest `window` draws (all gaps when window is None)."""
    if window is not None and not (isinstance(window, int) and 1 <= window <= W):
        raise ValueError('the window must be between 1 and the number of draws')
    lo = 0 if window is None else W - window
    return {j: [b - a for a, b in zip(p, p[1:]) if a > lo] for j, p in app.items()}


def gaps_by_scan(draws, low, high, window=None):
    """The same as gaps_in_window(appearances(...)), written as a scan of the draws (a second route)."""
    W = len(draws)
    if window is not None and not (isinstance(window, int) and 1 <= window <= W):
        raise ValueError('the window must be between 1 and the number of draws')
    start = 1 if window is None else W - window + 1
    last = {j: None for j in range(low, high + 1)}
    out = {j: [] for j in last}
    for i, d in enumerate(_checked(draws, low, high), 1):
        for x in d:
            if last[x] is not None and last[x] >= start:
                out[x].append(i - last[x])
            last[x] = i
    return out


def projected_ages(W, app):
    """{label: W + 1 - its last appearance}, with 0 as the last appearance of a never-seen label."""
    return {j: W + 1 - (p[-1] if p else 0) for j, p in app.items()}


# ---------------------------------------------------------------- exposures by age
def label_exposures_by_walk(draws, low, high, window=None):
    """{label: (R, E)}: at-risk and event counts by age, from a per-draw walk; only the newest `window` draws
    if given, with ages measured from the true last appearance."""
    W = len(draws)
    start = 1 if window is None else W - window + 1
    if window is not None and not (isinstance(window, int) and 1 <= window <= W):
        raise ValueError('the window must be between 1 and the number of draws')
    last = {j: None for j in range(low, high + 1)}
    out = {j: ({}, {}) for j in last}
    for i, d in enumerate(_checked(draws, low, high), 1):
        present = set(d)
        if i >= start:
            for j, p in last.items():
                if p is not None:
                    k = i - p
                    R, E = out[j]
                    R[k] = R.get(k, 0) + 1
                    if j in present:
                        E[k] = E.get(k, 0) + 1
        for j in present:
            last[j] = i
    return out


def label_exposures_from_gaps(draws, low, high, window=None):
    """The same counts, built from each completed gap (ages 1..g, the event at g) and the open stretch after
    the last appearance (ages 1..W - last, no event)."""
    W = len(draws)
    start = 1 if window is None else W - window + 1
    if window is not None and not (isinstance(window, int) and 1 <= window <= W):
        raise ValueError('the window must be between 1 and the number of draws')
    out = {}
    for j, p in appearances(draws, low, high).items():
        R, E = {}, {}
        for a, b in zip(p, p[1:]):
            for k in range(max(1, start - a), b - a + 1):
                R[k] = R.get(k, 0) + 1
            if b >= start:
                E[b - a] = E.get(b - a, 0) + 1
        if p:
            for k in range(max(1, start - p[-1]), W - p[-1] + 1):
                R[k] = R.get(k, 0) + 1
        out[j] = (R, E)
    return out


def pooled(per_label):
    """Sum per-label (R, E) counts over the labels."""
    R, E = {}, {}
    for Rj, Ej in per_label.values():
        for k, n in Rj.items():
            R[k] = R.get(k, 0) + n
        for k, n in Ej.items():
            E[k] = E.get(k, 0) + n
    return R, E


# ---------------------------------------------------------------- age bins
def bin_edges(L, K):
    m = Fraction(L, K)
    out = []
    for f in BIN_FACTORS:
        x = f * m
        e = -((-x.numerator) // x.denominator)
        if not out or e > out[-1]:
            out.append(e)
    return out


def bin_of(k, edges):
    return sum(1 for e in edges if k > e)


def bin_ranges(edges):
    """[(first age, last age or None for the open last bin)] for each bin."""
    return list(zip([1] + [e + 1 for e in edges], list(edges) + [None]))


# ---------------------------------------------------------------- the certified sign of sum_k a_k ln k
def log_age_coefficients(R, E):
    """a_k = n E_k - e R_k, integers summing to 0; sum_k a_k ln k is n times the log-age covariance S_zy."""
    n, e = sum(R.values()), sum(E.values())
    return {k: n * E.get(k, 0) - e * r for k, r in R.items()}


def prime_exponents_by_trial(a):
    """{p: sum_k a_k v_p(k)} by trial division, zero exponents dropped."""
    out = {}
    for k, c in a.items():
        n, d = k, 2
        while d * d <= n:
            while n % d == 0:
                out[d] = out.get(d, 0) + c
                n //= d
            d += 1
        if n > 1:
            out[n] = out.get(n, 0) + c
    return {p: x for p, x in out.items() if x}


def prime_exponents_by_sieve(a):
    """The same map from a smallest-prime-factor sieve (an independently written route)."""
    top = max(a) if a else 1
    spf = list(range(top + 1))
    i = 2
    while i * i <= top:
        if spf[i] == i:
            for m in range(i * i, top + 1, i):
                if spf[m] == m:
                    spf[m] = i
        i += 1
    out = {}
    for k, c in a.items():
        while k > 1:
            p = spf[k]
            out[p] = out.get(p, 0) + c
            k //= p
    return {p: x for p, x in out.items() if x}


def _atanh_bounds(x, terms):
    """For rational 0 < x < 1: the partial sum of atanh's series (a lower bound), and it plus a geometric bound on
    the tail (an upper bound)."""
    s, xp, x2 = Fraction(0), x, x * x
    for i in range(terms):
        s += xp / (2 * i + 1)
        xp *= x2
    return s, s + xp / ((2 * terms + 1) * (1 - x2))


def ln_bounds(k, terms):
    """Rational bounds on ln k (integer k >= 1): ln k = a ln 2 + 2 atanh((m - 1)/(m + 1)) with k = 2^a m,
    1 <= m < 2, and ln 2 = 2 atanh(1/3)."""
    if not (isinstance(k, int) and k >= 1):
        raise ValueError('ln_bounds needs a whole number of at least 1')
    a = k.bit_length() - 1
    l2lo, l2hi = _atanh_bounds(Fraction(1, 3), terms)
    m = Fraction(k, 2 ** a)
    lo, hi = (Fraction(0), Fraction(0)) if m == 1 else _atanh_bounds((m - 1) / (m + 1), terms)
    return 2 * a * l2lo + 2 * lo, 2 * a * l2hi + 2 * hi


def bounded_sign(coeffs):
    """The sign of sum c_q ln q over a map {q: c_q} of integers, by bounds whose series terms double until the
    interval excludes 0. Only for a combination known not to be 0; refuses at MAX_TERMS."""
    terms = FIRST_TERMS
    while terms <= MAX_TERMS:
        lo = hi = Fraction(0)
        for q, c in coeffs.items():
            low, high = ln_bounds(q, terms)
            lo += c * (low if c > 0 else high)
            hi += c * (high if c > 0 else low)
        if lo > 0:
            return 1
        if hi < 0:
            return -1
        terms *= 2
    raise ValueError('the sign of the log combination was not certified within the term cap')


def log_sign_route_1(a):
    """The method's route: prime exponents by trial division (empty means exactly 0), then bounds on ln p."""
    e = prime_exponents_by_trial(a)
    return 0 if not e else bounded_sign(e)


def log_sign_route_2(a):
    """verify()'s route: its own exact-zero test by the sieve, then bounds on each ln k directly."""
    if not prime_exponents_by_sieve(a):
        return 0
    return bounded_sign({k: c for k, c in a.items() if c})
