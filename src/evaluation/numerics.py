"""WF-1B numerics: exact tails and deterministic high-precision transforms (design WF-1 v0.1r1 section 6.6).

Exact integer and rational values:
  - binomial tails as Fractions, summed on the shorter side over the common denominator b**n (no cancellation);
  - MR7's fair-draw null as the integer coefficients of A(z)**n, where A(z) is one draw's main-match weight
    polynomial (R3 17.4.4); bounded at n <= 1000 (`MR_EXACT_BOUND_EXCEEDED` above it).
Deterministic, bounded-accuracy decimal transforms (not exact values):
  - sigma = Phi_inv(1 - p) by bisection on the normal tail Q in 80-digit decimal arithmetic. Q uses the erf series
    for x = z/sqrt(2) < 5 and the Laplace continued fraction (400 terms) from 5 up. 1 - p is never formed in
    floating point; near p = 1/2 the comparison uses d = 1/2 - p, formed exactly as a Fraction.
  - log10 of a p-value, to 15 significant digits, from the Fraction (never from an underflowed float);
  - the Clopper-Pearson interval: the float64 that bisection on the exact binomial tails returns, found by the
    same bisection guided by 80-digit decimal tails and then confirmed with the exact tails (PERF-1).
Each transform is accurate to a relative 1e-30 or better before ONE correctly rounded conversion to float64.

Standard library only. Every decimal computation runs in a local context; the global context is never changed.
Fair-draw arithmetic only: this module reads no file.
"""
from __future__ import annotations

import decimal
import functools
from decimal import Decimal
from fractions import Fraction
from math import comb

__all__ = [
    'binom_upper', 'binom_lower', 'pmf_weights', 'mr7_null', 'mr7_tails', 'sigma_from_p', 'p_output',
    'clopper_pearson', 'z_plus', 'z_minus', 'format_sigma', 'format_prob',
    'MR7_EXACT_MAX_N', 'SIGMA_BOUND', 'FLOAT64_MIN_NORMAL',
]

# ---------------------------------------------------------------- constants

MR7_EXACT_MAX_N = 1000                      # design 6.6: MR7's exact null is computed for n <= 1000
SIGMA_BOUND = 1000                          # design 6.6: sigma above 1000 is reported as SIGMA_ABOVE_BOUND
FLOAT64_MIN_NORMAL = Fraction(1, 1 << 1022)  # 2.2250738585072014e-308, exactly

_PREC = 80                                  # design 6.6: 80-digit decimal arithmetic
_CF_DEPTH = 400                             # continued-fraction terms (design 6.6)
_SWITCH_X = 5                               # route switch at x = z/sqrt(2) = 5 (design 6.6, v0.1r1)
_EXP_LIMIT = 999999999                      # decimal exponent range for the local contexts (valid on 32-bit too)
_REL_STOP = Decimal('1e-36')                # bisection stops at a bracket below 1e-36 relative
_MAX_BISECT = 4000                          # safety stop; never reached for 0 < p < 1/2
_BITS = 512                                 # bits kept when a huge Fraction is converted to decimal

# pi to 100 decimal places (the test file checks it against an independent decimal computation).
_PI_TEXT = ('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706'
            '79')


def _ctx(prec: int = _PREC) -> decimal.Context:
    """A fresh decimal context (round half even, wide exponent range, no traps except the invalid ones)."""
    return decimal.Context(prec=prec, rounding=decimal.ROUND_HALF_EVEN, Emin=-_EXP_LIMIT, Emax=_EXP_LIMIT,
                           traps=[decimal.InvalidOperation, decimal.DivisionByZero, decimal.Overflow])


with decimal.localcontext(_ctx(_PREC + 20)):
    _PI = +Decimal(_PI_TEXT)
    _SQRT_PI = _PI.sqrt()
    _SQRT2 = Decimal(2).sqrt()


# ---------------------------------------------------------------- argument checks

def _check_int(name: str, v) -> int:
    if isinstance(v, bool) or not isinstance(v, int):
        raise TypeError(f'{name} must be an int')
    return v


def _check_prob(name: str, p) -> Fraction:
    if isinstance(p, bool) or not isinstance(p, (Fraction, int)):
        raise TypeError(f'{name} must be a Fraction (or an int), never a float')
    p = Fraction(p)
    if p < 0 or p > 1:
        raise ValueError(f'{name} must lie in [0, 1]')
    return p


# ---------------------------------------------------------------- exact binomial tails

def _pmf_num_sum(n: int, a: int, c: int, lo: int, hi: int) -> int:
    """sum_{j=lo..hi} C(n, j) a**j c**(n-j), exactly, as an integer (lo <= hi).

    Written as a**lo c**(n-hi) times P(lo, hi), where P(l, h) = sum_{j=l..h} C(n, j) a**(j-l) c**(h-j). P is
    evaluated by binary splitting, P(l, h) = P(l, m) c**(h-m) + a**(m+1-l) P(m+1, h), with Horner's rule on short
    ranges; the binomial coefficients come from the exact recurrence C(n, j+1) = C(n, j) (n - j) / (j + 1).
    The same integer as the plain Horner sum (PERF-1), in far fewer long multiplications."""
    binoms = [comb(n, lo)]
    for j in range(lo, hi):
        binoms.append(binoms[-1] * (n - j) // (j + 1))
    apow: dict[int, int] = {}
    cpow: dict[int, int] = {}

    def _pow(cache: dict, base: int, e: int) -> int:
        v = cache.get(e)
        if v is None:
            v = cache[e] = base ** e
        return v

    def part(l: int, h: int) -> int:
        if h - l < 16:
            acc = binoms[h - lo]
            cp = 1
            for j in range(h - 1, l - 1, -1):
                cp *= c
                acc = acc * a + binoms[j - lo] * cp
            return acc
        m = (l + h) // 2
        return part(l, m) * _pow(cpow, c, h - m) + _pow(apow, a, m + 1 - l) * part(m + 1, h)

    return part(lo, hi) * a ** lo * c ** (n - hi)


def _upper_num(n: int, a: int, b: int, k: int) -> int:
    """Numerator over b**n of P(X >= k), X ~ Bin(n, a/b), for 1 <= k <= n, on the shorter side."""
    c = b - a
    if n - k + 1 <= k:
        return _pmf_num_sum(n, a, c, k, n)
    return b ** n - _pmf_num_sum(n, a, c, 0, k - 1)


def binom_upper(n: int, p: Fraction, k: int) -> Fraction:
    """P(X >= k) for X ~ Binomial(n, p), exactly. k <= 0 gives 1; k > n gives 0."""
    n = _check_int('n', n)
    k = _check_int('k', k)
    p = _check_prob('p', p)
    if n < 0:
        raise ValueError('n must be >= 0')
    if k <= 0:
        return Fraction(1)
    if k > n:
        return Fraction(0)
    a, b = p.numerator, p.denominator
    return Fraction(_upper_num(n, a, b, k), b ** n)


def binom_lower(n: int, p: Fraction, k: int) -> Fraction:
    """P(X <= k) for X ~ Binomial(n, p), exactly. k < 0 gives 0; k >= n gives 1."""
    n = _check_int('n', n)
    k = _check_int('k', k)
    p = _check_prob('p', p)
    if n < 0:
        raise ValueError('n must be >= 0')
    if k < 0:
        return Fraction(0)
    if k >= n:
        return Fraction(1)
    a, b = p.numerator, p.denominator
    c = b - a
    if k + 1 <= n - k:                       # the lower side (k + 1 terms) is the shorter
        num = _pmf_num_sum(n, a, c, 0, k)
    else:
        num = b ** n - _pmf_num_sum(n, a, c, k + 1, n)
    return Fraction(num, b ** n)


# ---------------------------------------------------------------- MR7's exact null

_GAMES = {'POWERBALL': 28, 'OZLOTTO': 40}    # non-winning main numbers: 35 - 7 and 47 - 7


def _check_game(game) -> str:
    if game not in _GAMES:
        raise ValueError("game must be 'POWERBALL' or 'OZLOTTO'")
    return game


def pmf_weights(game: str) -> tuple[list[int], int]:
    """One draw's main-match weights for m = 0..7 and their total (R3 17.4.4, hypergeometric)."""
    other = _GAMES[_check_game(game)]
    w = [comb(7, m) * comb(other, 7 - m) for m in range(8)]
    return w, comb(7 + other, 7)


def _dec_digits_to_int(s: str) -> int:
    """Decimal digit string to int, in pieces short enough for every interpreter's int/str conversion limit."""
    if len(s) <= 4000:
        return int(s)
    h = len(s) // 2
    return _dec_digits_to_int(s[:h]) * 10 ** (len(s) - h) + _dec_digits_to_int(s[h:])


@functools.lru_cache(maxsize=None)
def _mr7_null_cached(game: str, n: int) -> tuple[int, ...]:
    w, total = pmf_weights(game)
    if n == 0:
        return (1,)
    # Kronecker substitution in base 10**width: A(10**width)**n holds every coefficient of A(z)**n in its own
    # slot of `width` digits. Each coefficient is below total**n < 10**(width - 1), so no slot overflows into
    # the next. The power is done in decimal (libmpdec multiplies huge operands by number-theoretic transform)
    # with the Inexact and Rounded traps on, so any loss of exactness would raise instead of passing silently.
    width = (total ** n).bit_length() * 30103 // 100000 + 2
    length = 7 * n + 1
    ctx = decimal.Context(prec=length * width + 2, rounding=decimal.ROUND_HALF_EVEN, Emin=decimal.MIN_EMIN,
                          Emax=decimal.MAX_EMAX,
                          traps=[decimal.InvalidOperation, decimal.DivisionByZero, decimal.Overflow,
                                 decimal.Inexact, decimal.Rounded])
    with decimal.localcontext(ctx):
        a = Decimal(0)
        for coef in reversed(w):
            a = a.scaleb(width) + coef
        r = a ** n
        digits = format(r, 'f')
    if not digits.isdigit() or len(digits) > length * width:
        raise RuntimeError('MR7 null: unexpected decimal result')
    digits = digits.rjust(length * width, '0')
    end = len(digits)
    out = [_dec_digits_to_int(digits[end - (i + 1) * width:end - i * width]) for i in range(length)]
    # Self-checks (cheap): the total mass and the exact mean (n x 7 x 7 / pool size per draw).
    if sum(out) != total ** n or sum(s * x for s, x in enumerate(out)) * (7 + _GAMES[game]) != 49 * n * total ** n:
        raise RuntimeError('MR7 null: self-check failed')
    return tuple(out)


def mr7_null(game: str, n: int) -> tuple[int, ...]:
    """Integer coefficients of A(z)**n (index = total main matches S over n draws; they sum to W**n).

    n > 1000 raises ValueError('MR_EXACT_BOUND_EXCEEDED'). Built once per (game, n) and cached."""
    _check_game(game)
    n = _check_int('n', n)
    if n < 0:
        raise ValueError('n must be >= 0')
    if n > MR7_EXACT_MAX_N:
        raise ValueError('MR_EXACT_BOUND_EXCEEDED')
    return _mr7_null_cached(game, n)


def mr7_tails(game: str, n: int, S: int) -> tuple[Fraction, Fraction]:
    """(P_up, P_lo) = (P(S_null >= S), P(S_null <= S)) for the total main matches over n fair draws, exactly."""
    coeffs = mr7_null(game, n)
    S = _check_int('S', S)
    denom = pmf_weights(game)[1] ** n
    top = len(coeffs) - 1
    if S <= 0:
        up = denom
    elif S > top:
        up = 0
    else:
        up = sum(coeffs[S:])
    if S < 0:
        lo = 0
    elif S >= top:
        lo = denom
    else:
        lo = sum(coeffs[:S + 1])
    return Fraction(up, denom), Fraction(lo, denom)


# ---------------------------------------------------------------- normal tail in decimal

def _erf_series(x: Decimal) -> Decimal:
    """erf(x) by its Maclaurin series, in 80-digit decimal (used for x < 5)."""
    with decimal.localcontext(_ctx()):
        x = +x
        if x == 0:
            return Decimal(0)
        x2 = x * x
        total = Decimal(0)
        term = x
        n = 0
        stop = Decimal(10) ** -(_PREC + 10)
        while True:
            add = term / (2 * n + 1)
            total += add
            if abs(add) <= abs(total) * stop:
                break
            n += 1
            term = -term * x2 / n
        return 2 * total / _SQRT_PI


def _erfc_cf(x: Decimal) -> Decimal:
    """erfc(x) by the Laplace continued fraction (400 terms, evaluated backwards), in 80-digit decimal (x >= 5)."""
    with decimal.localcontext(_ctx()):
        x = +x
        f = Decimal(0)
        for k in range(_CF_DEPTH, 0, -1):
            f = Decimal(k) / 2 / (x + f)
        return (-(x * x)).exp() / (x + f) / _SQRT_PI


def _upper_tail(z: Decimal) -> Decimal:
    """Q(z) = P(Z >= z) for a standard normal, z >= 0, in 80-digit decimal (both routes as in design 6.6)."""
    with decimal.localcontext(_ctx()):
        x = z / _SQRT2
        if x < _SWITCH_X:
            return (1 - _erf_series(x)) / 2
        return _erfc_cf(x) / 2


def _fraction_to_decimal(fr: Fraction, prec: int = _PREC + 20) -> Decimal:
    """A positive Fraction as a decimal to `prec` digits, correct to a relative 2**-500 before rounding.

    Huge numerators and denominators are first cut to their top 512 bits (an O(size) shift), so the cost does not
    depend on how extreme the value is."""
    num, den = fr.numerator, fr.denominator
    if num <= 0:
        raise ValueError('positive Fraction required')
    sn = max(0, num.bit_length() - _BITS)
    sd = max(0, den.bit_length() - _BITS)
    # The numerator is widened by 2 x _BITS before the integer division, so the quotient keeps at least _BITS
    # significant bits whatever the two sizes (a small numerator over a huge denominator included).
    q = ((num >> sn) << (2 * _BITS)) // (den >> sd)
    e2 = sn - sd - 2 * _BITS
    with decimal.localcontext(_ctx(prec)):
        return Decimal(q) * (Decimal(2) ** e2)


@functools.lru_cache(maxsize=1)
def _q_at_bound() -> Decimal:
    """Q(1000), about 10**-217150.6 (decimal handles the exponent; no underflow)."""
    return _upper_tail(Decimal(SIGMA_BOUND))


def _sigma_decimal(p: Fraction) -> Decimal:
    """The root z of Q(z) = p, for 0 < p < 1/2 and Q(1000) <= p, accurate to a relative 1e-30 or better."""
    d = Fraction(1, 2) - p                    # exact: 1 - p is never formed in floating point
    p_dec = _fraction_to_decimal(p)
    d_dec = _fraction_to_decimal(d)
    with decimal.localcontext(_ctx()):
        p_dec = +p_dec
        d_dec = +d_dec
        # Bracket: z > 2.5 d, because erf(x)/2 < x/sqrt(pi) gives d < z/sqrt(2 pi); and
        # Q(z) <= exp(-z*z/2)/2 gives Q(hi) < p for hi = sqrt(2 ln(1/p)) + 1.
        lo = Decimal('2.5') * d_dec
        hi = (2 * (-p_dec.ln())).sqrt() + 1

        def q_above_p(z: Decimal) -> bool:
            x = z / _SQRT2
            if x < _SWITCH_X:
                return _erf_series(x) / 2 < d_dec        # Q(z) > p  <=>  erf(x)/2 < 1/2 - p
            return _erfc_cf(x) / 2 > p_dec

        if not (q_above_p(lo) and not q_above_p(hi)):
            raise RuntimeError('sigma: bracket check failed')
        for _ in range(_MAX_BISECT):
            if hi - lo <= lo * _REL_STOP:
                return (lo + hi) / 2
            mid = (lo * hi).sqrt() if hi > 2 * lo else (lo + hi) / 2
            if q_above_p(mid):
                lo = mid
            else:
                hi = mid
    raise RuntimeError('sigma: bisection did not converge')


def sigma_from_p(p: Fraction) -> dict:
    """sigma = max(0, Phi_inv(1 - p)) for a one-sided tail p (R3 17.5.1).

    p >= 1/2 gives 0.0 exactly. p <= 0 (or p > 1) raises ValueError. A p below Q(1000) gives
    {'sigma': 1000.0, 'label': 'SIGMA_ABOVE_BOUND'}. Otherwise {'sigma': float, 'label': None}, where the float is
    the one correctly rounded conversion of a decimal value accurate to a relative 1e-30 or better."""
    p = _check_prob('p', p)
    if p <= 0:
        raise ValueError('p must be > 0')
    if p >= Fraction(1, 2):
        return {'sigma': 0.0, 'label': None}
    # Bound check by logarithms first (bit lengths), then exactly against Q(1000) only near the bound.
    # log2 Q(1000) is about -721,360.6; the bit-length estimate of log2 p is within 1 of the truth.
    log2_est = p.numerator.bit_length() - p.denominator.bit_length()
    if log2_est < -721400:
        return {'sigma': float(SIGMA_BOUND), 'label': 'SIGMA_ABOVE_BOUND'}
    if log2_est < -721300 and _fraction_to_decimal(p) < _q_at_bound():
        return {'sigma': float(SIGMA_BOUND), 'label': 'SIGMA_ABOVE_BOUND'}
    return {'sigma': float(_sigma_decimal(p)), 'label': None}


def z_plus(p_up: Fraction) -> dict:
    """Local excess sigma, R3 17.5.1: Z_plus = max(0, Phi_inv(1 - P_up)). This is sigma_from_p(P_up) exactly
    (P_up = 1, for k = 0, gives 0 excess sigma)."""
    return sigma_from_p(p_up)


def z_minus(p_lo: Fraction) -> dict:
    """Local deficit sigma, R3 17.5.1: Z_minus = max(0, Phi_inv(1 - P_lo)). This is sigma_from_p(P_lo) exactly."""
    return sigma_from_p(p_lo)


# ---------------------------------------------------------------- p-value output

def p_output(p: Fraction) -> dict:
    """{'p_float', 'p_log10', 'label'} for a p-value in (0, 1] (design 6.6, output rules).

    p_float is float(p), correctly rounded (it may be subnormal or 0.0). p_log10 is log10(p) to 15 significant
    digits, from the Fraction itself. The label is 'P_BELOW_FLOAT64_RANGE' when p < 2.2250738585072014e-308."""
    p = _check_prob('p', p)
    if p <= 0:
        raise ValueError('p must be > 0')
    p_float = float(p)                       # Fraction -> float is a correctly rounded integer division
    if p == 1:
        log_text = '0'
    else:
        x = _fraction_to_decimal(p, 100)
        with decimal.localcontext(_ctx(100)):
            lg = x.log10()
        with decimal.localcontext(_ctx(15)):
            log_text = format((+lg).normalize(), 'f')      # 15 significant digits, no trailing zeros
    label = 'P_BELOW_FLOAT64_RANGE' if p < FLOAT64_MIN_NORMAL else None
    return {'p_float': p_float, 'p_log10': log_text, 'label': label}


# ---------------------------------------------------------------- Clopper-Pearson

def _bisect_float(pred_high) -> float:
    """The float64 nearest the root p* in (0, 1) of a monotone predicate pred_high(Fraction) that is True for
    p > p* and False for p < p*. Bisects over float64 values until the bracket is two adjacent floats, then
    decides between them at their exact midpoint (correct rounding)."""
    lo, hi = 0.0, 1.0
    while True:
        mid = lo + (hi - lo) / 2
        if mid <= lo or mid >= hi:
            break
        if pred_high(Fraction(mid)):
            hi = mid
        else:
            lo = mid
    return hi if pred_high((Fraction(lo) + Fraction(hi)) / 2) is False else lo


def _tail_dec(n: int, q: Decimal, lo: int, hi: int) -> Decimal:
    """sum_{j=lo..hi} C(n, j) q**j (1-q)**(n-j) in the current decimal context (0 < q < 1). A guide only."""
    p = 1 - q
    r = q / p
    t = Decimal(comb(n, lo)) * q ** lo * p ** (n - lo)
    total = t
    for j in range(lo, hi):
        t = t * r * (n - j) / (j + 1)
        total += t
    return total


def _upper_gt_exact(n: int, q: Fraction, k: int, half: Fraction) -> bool:
    """P(X >= k; q) > half, exactly, by integer comparison (1 <= k <= n; 0 < q < 1)."""
    return _upper_num(n, q.numerator, q.denominator, k) * half.denominator > half.numerator * q.denominator ** n


def _lower_lt_exact(n: int, q: Fraction, k: int, half: Fraction) -> bool:
    """P(X <= k; q) < half, exactly, by integer comparison (0 <= k < n; 0 < q < 1)."""
    a, b = q.numerator, q.denominator
    c = b - a
    if k + 1 <= n - k:
        num = _pmf_num_sum(n, a, c, 0, k)
    else:
        num = b ** n - _pmf_num_sum(n, a, c, k + 1, n)
    return num * half.denominator < half.numerator * b ** n


def _upper_gt_dec(n: int, q: Decimal, k: int, half: Decimal) -> bool:
    if n - k + 1 <= k:
        return _tail_dec(n, q, k, n) > half
    return 1 - _tail_dec(n, q, 0, k - 1) > half


def _lower_lt_dec(n: int, q: Decimal, k: int, half: Decimal) -> bool:
    if k + 1 <= n - k:
        return _tail_dec(n, q, 0, k) < half
    return 1 - _tail_dec(n, q, k + 1, n) < half


def _bisect_guided(guide, exact) -> float:
    """The float64 that _bisect_float(exact) returns, found with the cheap predicate `guide` (PERF-1).

    The bisection runs as in _bisect_float, deciding each step with `guide`. It ends at two adjacent floats
    lo < hi; the exact predicate is then evaluated at their exact midpoint and, on the side that midpoint does
    not settle, at lo or hi. If they show that exact() changes between lo and hi, (lo, hi) is the one adjacent
    pair where the monotone exact predicate changes, which is where _bisect_float ends too, and the same
    midpoint rule picks the same float. If not, _bisect_float(exact) is run and returned."""
    with decimal.localcontext(_ctx(_PREC)):
        lo, hi = 0.0, 1.0
        while True:
            mid = lo + (hi - lo) / 2
            if mid <= lo or mid >= hi:
                break
            if guide(Decimal(mid)):
                hi = mid
            else:
                lo = mid
    at_mid = exact((Fraction(lo) + Fraction(hi)) / 2)
    if at_mid is False:
        confirmed = hi == 1.0 or exact(Fraction(hi)) is True
    else:
        confirmed = lo == 0.0 or exact(Fraction(lo)) is False
    if not confirmed:
        return _bisect_float(exact)
    return hi if at_mid is False else lo


def clopper_pearson(k: int, n: int, conf: Fraction = Fraction(95, 100)) -> tuple[float, float]:
    """The exact two-sided Clopper-Pearson interval for k successes in n trials (alpha/2 in each tail).

    The lower bound solves P(X >= k; p) = alpha/2 and the upper bound P(X <= k; p) = alpha/2. Each is the float64
    that bisection on the exact binomial tails returns (correctly rounded); _bisect_guided finds it with decimal
    tails and confirms it with the exact ones (PERF-1). k = 0 gives lower 0.0; k = n gives upper 1.0."""
    k = _check_int('k', k)
    n = _check_int('n', n)
    if n <= 0:
        raise ValueError('n must be >= 1')
    if k < 0 or k > n:
        raise ValueError('k must lie in 0..n')
    if isinstance(conf, bool) or not isinstance(conf, Fraction):
        raise TypeError('conf must be a Fraction')
    if not (0 < conf < 1):
        raise ValueError('conf must lie strictly between 0 and 1')
    half = (1 - conf) / 2
    with decimal.localcontext(_ctx(_PREC)):
        half_dec = Decimal(half.numerator) / Decimal(half.denominator)
    if k == 0:
        lower = 0.0
    else:
        # P(X >= k; p) rises with p: True above the root.
        lower = _bisect_guided(lambda d: _upper_gt_dec(n, d, k, half_dec),
                               lambda q: _upper_gt_exact(n, q, k, half))
    if k == n:
        upper = 1.0
    else:
        # P(X <= k; p) falls with p: True above the root.
        upper = _bisect_guided(lambda d: _lower_lt_dec(n, d, k, half_dec),
                               lambda q: _lower_lt_exact(n, q, k, half))
    return lower, upper


# ---------------------------------------------------------------- display (R3 17.10.5)

def format_sigma(x: float) -> str:
    """Sigma to 2 decimals (R3 17.10.5)."""
    return f'{x:.2f}'


def format_prob(x: float) -> str:
    """A probability to 6 significant digits in scientific notation (R3 17.10.5)."""
    return f'{x:.5e}'
