"""MHUP-B: OV-1's numerical kernel (design supplement v0.8 section 6.5; code plan v0.3 section 6).

Whole numbers only. Every real number r is held as an integer n meaning n / S, with S = 10**50. A lower bound is always
rounded down and an upper bound always rounded up; Python's `//` on integers is an exact floor, so both directions are
exact. No float, no `math.exp` or `math.log` and no `decimal` call is on any path of this module (a static test bans
them), so its results are the same bytes on every platform and Python version. `math.isqrt` and `math.comb` are exact
integer functions.

What the module guarantees, and why (the proofs the code plan's section 6.5 asks for). Write lo(.) and hi(.) for the two
ends a function returns, and [r] for S * r.

 P1 `_exp_small(a)`, 0 <= a <= S, u = a / S in [0, 1].  exp(u) = sum_{k<n} u^k/k! + R_n, and
      R_n = sum_{k>=n} u^k/k! <= (u^n/n!) * sum_{i>=0} (u/(n+1))^i = (u^n/n!) * (n+1)/(n+1-u) <= 2 u^n/n!   (u <= 1 <= n).
    The loop keeps tl_k <= [u^k/k!] <= tu_k: tl_k = floor(tl_{k-1} * a / (S k)) and tu_k = ceil(tu_{k-1} * a / (S k)) are a
    floor and a ceiling of products of nonnegative bounds. So lo = S + sum_{k=1}^{n-1} tl_k <= [exp(u)], and
    hi = S + sum_{k=1}^{n-1} tu_k + 2 tu_n + 1 >= [exp(u)].
 P2 `exp_enc(a)`, any integer a.  For a >= 0 take j with ceil(a / 2^j) <= S; r_lo = floor(a / 2^j), r_hi = ceil(a / 2^j).
    exp(a/S) = exp(a / (2^j S))^(2^j), and exp is increasing, so lo(_exp_small(r_lo)) <= [exp(a/(2^j S))] <=
    hi(_exp_small(r_hi)). Squaring j times with floor(lo*lo/S) and ceil(hi*hi/S) keeps a lower and an upper bound of
    the square, because both are nonnegative. For a < 0: exp(a/S) = 1 / exp(-a/S); with (l, h) the enclosure of
    exp(-a/S), l >= S > 0, floor(S*S/h) <= [exp(a/S)] <= ceil(S*S/l).
 P3 `log_enc(m_lo, m_hi)`, S <= m_lo <= m_hi.  log m = 2 atanh(y), y = (m-1)/(m+1) in [0, 1), increasing in m, and
    atanh(y) = sum_{k>=0} y^(2k+1)/(2k+1) with every term nonnegative. Lower end: y, y^2 and every term rounded down,
    the series cut after any number of terms. Upper end: everything rounded up, n terms summed, and the remainder
      sum_{k>=n} y^(2k+1)/(2k+1) <= y^(2n+1) / (1 - y^2)
    added, itself rounded up (the code's `term` is then an upper bound of [y^(2n+1)], and S - y2 a lower bound of
    [1 - y^2]). y <= 0.7 is required, and refused otherwise, so 1 - y^2 >= 0.51.
 P4 `sqrt_enc(p, q)`: isqrt(floor(p S^2 / q)) <= [sqrt(p/q)] < isqrt(ceil(p S^2 / q)) + 1.
 P5 `counts(w)`: the number of K-subsets of the N numbers whose weights sum to x, by exact integer dynamic programming
    (two independent routes, required to agree). The fair draw picks each K-subset with chance 1 / C(N, K).
 P6 `factor_table(w)`.  theta = lambda / sqrt(V). With [t_lo, t_hi] enclosing |theta| (P4, then a floor and a ceiling
    of a quotient of positive numbers), theta * x for an integer x is enclosed by exact integer multiples. The mean
    m = E0[exp(theta X)] = sum_x count(x) exp(theta x) / C(N, K) is enclosed by P2 (sums of nonnegative lower bounds,
    and of upper bounds), and m >= 1 by Jensen because E0[X] = 0, so max(m_lo, S) is still a lower bound. log m is
    enclosed by P3. The true log-factor at x is theta x - log m, in [u_lo(x) - lg_hi, u_hi(x) - lg_lo].
    The STORED log-factor is  (u_lo(x) - lg_hi) - MARGIN.  The code checks that every enclosure is narrower than MARGIN
    and refuses otherwise. Hence  stored <= true  and  true - stored < 2 * MARGIN.
 P7 The certificate (code plan 6.3), checked in exact integers for each lambda:
      sum_x count(x) * hi(exp_enc(stored(x))) <= C(N, K) * S.
    Since hi(exp_enc(.)) >= [exp(.)] (P2), this proves sum_x P0(x) exp(stored(x)) <= 1: the stored factors have a
    fair-draw mean of at most 1 whatever route produced them. It rests on P2's upper end and P5 only.
 P8 `crossing(logs)`: the running logs are exact integer sums of stored log-factors, each <= the true running log by
    P6. lo(exp_enc(L)) <= [exp(L)] <= [the true component]. The crossing is declared only if the sum of the six lower
    ends is at least 6 * BAR * S: then the true mixture (the average of the six true components) is at least BAR.

A table is built from the weights alone, before any outcome exists. Refuse means: no bound could be established, and
nothing may be stored.
"""
from __future__ import annotations

import hashlib
from math import comb, isqrt

KERNEL_VERSION = 'OV1_KERNEL_V1'
DIGITS = 50
S = 10 ** DIGITS
MARGIN = 10 ** (DIGITS - 30)                 # 1e-30, the registered safety margin, in fixed point
K = 7                                        # numbers drawn from the main barrel, both games
LAMBDAS = ((-1, 5), (-1, 10), (-1, 20), (1, 20), (1, 10), (1, 5))      # exact fractions (numerator, denominator)
BAR = 40
_EXP_TERMS = 60
_LOG_TERMS = 400


class Refuse(Exception):
    """A bound could not be established. Nothing may be stored, and no crossing may be claimed."""


def _fdiv(a: int, b: int) -> int:
    return a // b                             # exact floor (b > 0)


def _cdiv(a: int, b: int) -> int:
    return -((-a) // b)                       # exact ceiling (b > 0)


def _whole(a, what: str) -> None:
    if type(a) is not int:
        raise Refuse(f'{what} is not a whole number')


def _exp_small(a: int) -> tuple[int, int]:
    """(lo, hi) enclosing S * exp(a / S) for 0 <= a <= S (P1)."""
    if not 0 <= a <= S:
        raise Refuse('exp: reduced argument out of range')
    lo = hi = S
    tl = tu = S
    for k in range(1, _EXP_TERMS):
        tl = _fdiv(tl * a, S * k)
        tu = _cdiv(tu * a, S * k)
        lo += tl
        hi += tu
    tu = _cdiv(tu * a, S * _EXP_TERMS)        # an upper bound of the first omitted term
    return lo, hi + 2 * tu + 1


def _square(lo: int, hi: int) -> tuple[int, int]:
    """(a lower bound of S * (lo/S)^2, an upper bound of S * (hi/S)^2) for 0 <= lo <= hi: an exact floor and ceiling."""
    return _fdiv(lo * lo, S), _cdiv(hi * hi, S)


def exp_enc(a: int) -> tuple[int, int]:
    """(lo, hi) enclosing S * exp(a / S) for any whole a (P2)."""
    _whole(a, 'exp argument')
    if a < 0:
        lo, hi = exp_enc(-a)
        return _fdiv(S * S, hi), _cdiv(S * S, lo)
    j = 0
    while -((-a) >> j) > S:                   # the CEILING of a / 2**j must be within [0, S]
        j += 1
    lo = _exp_small(a >> j)[0]
    hi = _exp_small(-((-a) >> j))[1]
    for _ in range(j):
        lo, hi = _square(lo, hi)
    return lo, hi


def log_enc(m_lo: int, m_hi: int) -> tuple[int, int]:
    """(lo, hi) enclosing S * log(m) for every m with m_lo <= S * m <= m_hi, where m_lo >= S (P3)."""
    _whole(m_lo, 'log argument')
    _whole(m_hi, 'log argument')
    if m_lo < S or m_hi < m_lo:
        raise Refuse('log: argument below 1 or ends out of order')
    ends = []
    for m, up in ((m_lo, False), (m_hi, True)):
        y = _cdiv((m - S) * S, m + S) if up else _fdiv((m - S) * S, m + S)
        if y * 10 > 7 * S:
            raise Refuse('log: argument too large for the series (y > 0.7)')
        y2 = _cdiv(y * y, S) if up else _fdiv(y * y, S)
        term, total = y, 0
        for k in range(_LOG_TERMS):
            total += _cdiv(term, 2 * k + 1) if up else _fdiv(term, 2 * k + 1)
            term = _cdiv(term * y2, S) if up else _fdiv(term * y2, S)
            if term == 0:
                break
        if up:
            total += _cdiv(term * S, S - y2) + 1
        ends.append(2 * total)
    return ends[0], ends[1]


def sqrt_enc(p: int, q: int) -> tuple[int, int]:
    """(lo, hi) enclosing S * sqrt(p / q) for whole p >= 0, q > 0 (P4)."""
    _whole(p, 'sqrt argument')
    _whole(q, 'sqrt argument')
    if p < 0 or q <= 0:
        raise Refuse('sqrt: argument out of range')
    return isqrt(_fdiv(p * S * S, q)), isqrt(_cdiv(p * S * S, q)) + 1


# ---------------------------------------------------------------- the exact fair-draw distribution (P5)

def _check_weights(w) -> list[int]:
    w = list(w)
    if len(w) <= K or not all(type(x) is int for x in w):
        raise Refuse('weights: not whole numbers for a barrel larger than the draw')
    if sum(w) != 0:
        raise Refuse('weights: do not sum to zero')
    return w


def counts_by_number(w) -> dict[int, int]:
    """{x: how many K-subsets have summed weight x}; route 1, one number at a time."""
    dp = [dict() for _ in range(K + 1)]
    dp[0][0] = 1
    for wj in w:
        for k in range(K - 1, -1, -1):
            for s, c in dp[k].items():
                dp[k + 1][s + wj] = dp[k + 1].get(s + wj, 0) + c
    return dp[K]


def counts_by_group(w) -> dict[int, int]:
    """The same counts by an independent route: numbers of equal weight grouped; a group of m numbers of weight v
    gives C(m, j) ways to take j of them; the groups are convolved."""
    groups: dict[int, int] = {}
    for wj in w:
        groups[wj] = groups.get(wj, 0) + 1
    cur = {(0, 0): 1}
    for v, m in sorted(groups.items()):
        new: dict[tuple[int, int], int] = {}
        for (k, s), c in cur.items():
            for j in range(0, min(m, K - k) + 1):
                key = (k + j, s + j * v)
                new[key] = new.get(key, 0) + c * comb(m, j)
        cur = new
    return {s: c for (k, s), c in cur.items() if k == K}


def counts(w) -> dict[int, int]:
    """The exact distribution of X under a fair draw, as counts out of C(N, K): both routes, required to agree, with
    the total, the zero mean and the variance identity checked in exact integers."""
    w = _check_weights(w)
    out = counts_by_number(w)
    if out != counts_by_group(w):
        raise Refuse('distribution: the two routes disagree')
    total = comb(len(w), K)
    num, den = variance(w)
    if (sum(out.values()) != total or sum(x * c for x, c in out.items()) != 0 or
            sum(x * x * c for x, c in out.items()) * den != num * total):
        raise Refuse('distribution: total, mean or variance identity fails')
    return out


def variance(w) -> tuple[int, int]:
    """V = K (N - K) / (N - 1) * (1 / N) * sum of w_j^2 (the weights sum to zero), as a fraction in lowest terms."""
    w = _check_weights(w)
    n = len(w)
    num, den = K * (n - K) * sum(x * x for x in w), (n - 1) * n
    g = _gcd(num, den)
    return num // g, den // g


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


# ---------------------------------------------------------------- one draw's sealed factor table (P6, P7)

def factor_table(w) -> dict | None:
    """For one draw's frozen weights: None when V = 0 (the registered skip), else
    {'rows': [ {x: stored log-factor} for each lambda in LAMBDAS order ], 'counts': {x: count}, 'total': C(N, K),
     'variance': (numerator, denominator)}, with the enclosure width and the certificate checked. Refuse otherwise."""
    w = _check_weights(w)
    v_num, v_den = variance(w)
    if v_num == 0:
        return None
    dist = counts(w)
    total = comb(len(w), K)
    s_lo, s_hi = sqrt_enc(v_num, v_den)
    if s_lo <= 0:
        raise Refuse('table: no positive lower bound for sqrt(V)')
    rows = []
    for num, den in LAMBDAS:
        t_lo, t_hi = _fdiv(abs(num) * S * S, den * s_hi), _cdiv(abs(num) * S * S, den * s_lo)   # |theta|
        sign = 1 if num > 0 else -1
        u = {}
        for x in dist:
            y = sign * x
            u[x] = (t_lo * y, t_hi * y) if y >= 0 else (t_hi * y, t_lo * y)
        m_lo = m_hi = 0
        for x, c in dist.items():
            m_lo += c * exp_enc(u[x][0])[0]
            m_hi += c * exp_enc(u[x][1])[1]
        lg_lo, lg_hi = log_enc(max(_fdiv(m_lo, total), S), _cdiv(m_hi, total))
        row = {}
        for x in dist:
            lo, hi = u[x][0] - lg_hi, u[x][1] - lg_lo
            if hi - lo >= MARGIN:
                raise Refuse('table: an enclosure is not narrower than the registered margin')
            row[x] = lo - MARGIN
        if sum(c * exp_enc(row[x])[1] for x, c in dist.items()) > total * S:
            raise Refuse('table: the certificate fails (the stored factors do not have a fair-draw mean of at most 1)')
        rows.append(row)
    return {'rows': rows, 'counts': dist, 'total': total, 'variance': (v_num, v_den)}


def table_bytes(table: dict) -> bytes:
    """The one serialisation of a factor table: the kernel's version, then a line per lambda and possible X."""
    out = [f'{KERNEL_VERSION} digits={DIGITS} margin={MARGIN} total={table["total"]} '
           f'variance={table["variance"][0]}/{table["variance"][1]}']
    for (num, den), row in zip(LAMBDAS, table['rows']):
        for x in sorted(row):
            out.append(f'{num}/{den} {x} {table["counts"][x]} {row[x]}')
    return ('\n'.join(out) + '\n').encode('ascii')


def table_digest(table: dict) -> str:
    return hashlib.sha256(table_bytes(table)).hexdigest()


# ---------------------------------------------------------------- the running score (P8)

def mixture_lower(logs) -> int:
    """A proved lower bound of S * (the average of exp(running log) over the six components)."""
    logs = list(logs)
    if len(logs) != len(LAMBDAS):
        raise Refuse('score: not one running log for each lambda')
    return _fdiv(sum(exp_enc(L)[0] for L in logs), len(LAMBDAS))


def crossing(logs) -> bool:
    """True only if the proved lower bound of the score is at least BAR: a comparison of exact integers."""
    logs = list(logs)
    if len(logs) != len(LAMBDAS):
        raise Refuse('score: not one running log for each lambda')
    return sum(exp_enc(L)[0] for L in logs) >= len(LAMBDAS) * BAR * S


# ---------------------------------------------------------------- display only

def fixed_text(n: int, places: int = 12) -> str:
    """A fixed-point value n / S as text, cut (toward zero) to `places` decimal places. Display only."""
    _whole(n, 'value')
    q = abs(n) // 10 ** (DIGITS - places)
    return f'{"-" if n < 0 and q else ""}{q // 10 ** places}.{q % 10 ** places:0{places}d}'


def z_text(x: int, v_num: int, v_den: int, places: int = 12) -> str:
    """Z = X / sqrt(V) as text, cut (toward zero) to `places` decimal places, by exact integer square root. Display
    only: no stored factor depends on it."""
    if v_num <= 0 or v_den <= 0:
        raise Refuse('Z: V is not positive')
    q = isqrt(x * x * 10 ** (2 * places) * v_den // v_num)
    return f'{"-" if x < 0 and q else ""}{q // 10 ** places}.{q % 10 ** places:0{places}d}'
