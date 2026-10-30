"""WF-1 design note v0.1 - reference and probe script (Claude, 30 October 2026).

Computes every number quoted in the design note's sections 9 and 10 from first principles. Invented
data and fair-draw arithmetic only: it reads no repository data file, no results and no real draw.
Standard library only (plus NumPy for one timing comparison, optional).

  python3 -I reference_wf1.py            all checks, about a minute
"""
from __future__ import annotations

import hashlib
import struct
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb

# ---------------------------------------------------------------- exact game constants (R3 17.4)

PB_MAIN = [comb(7, m) * comb(28, 7 - m) for m in range(8)]          # out of C(35,7)
OZ_MAIN = [comb(7, m) * comb(40, 7 - m) for m in range(8)]          # out of C(47,7)
assert sum(PB_MAIN) == comb(35, 7) == 6724520 and sum(OZ_MAIN) == comb(47, 7) == 62891499

# ---------------------------------------------------------------- deterministic normal tail (decimal)

getcontext().prec = 80
D = Decimal


def _erfc_cf(x: Decimal) -> Decimal:
    """erfc(x) for x >= 3 by the Laplace continued fraction, evaluated backwards to a fixed depth."""
    depth = 400
    f = D(0)
    for k in range(depth, 0, -1):
        f = D(k) / 2 / (x + f)
    return (-(x * x)).exp() / (x + f) / D(3.14159265358979323846264338327950288419716939937510582097494459).sqrt()


def _erf_series(x: Decimal) -> Decimal:
    total, term, n = D(0), x, 0
    x2 = x * x
    while True:
        add = term / (2 * n + 1)
        total += add
        if abs(add) < D(10) ** -70:
            break
        n += 1
        term = -term * x2 / n
    return 2 * total / D(3.14159265358979323846264338327950288419716939937510582097494459).sqrt()


def upper_tail(z: Decimal) -> Decimal:
    """Q(z) = P(Z >= z) for a standard normal, z >= 0."""
    x = z / D(2).sqrt()
    if x < 3:
        return (1 - _erf_series(x)) / 2
    return _erfc_cf(x) / 2


def sigma_from_p(p: Fraction) -> float:
    """Z_plus = max(0, Phi_inv(1 - p)), solved by bisection on the decimal tail; never forms 1 - p in
    floating point. Returns a correctly rounded float of a value accurate far beyond 1e-12."""
    if p >= Fraction(1, 2):
        return 0.0
    target = D(p.numerator) / D(p.denominator)
    lo, hi = D(0), D(60)
    for _ in range(200):
        mid = (lo + hi) / 2
        if upper_tail(mid) > target:
            lo = mid
        else:
            hi = mid
    return float((lo + hi) / 2)


# ---------------------------------------------------------------- exact binomial tails and MR7

def binom_upper(n: int, p: Fraction, k: int) -> Fraction:
    return sum((Fraction(comb(n, j)) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1)), Fraction(0))


def binom_lower(n: int, p: Fraction, k: int) -> Fraction:
    return sum((Fraction(comb(n, j)) * p ** j * (1 - p) ** (n - j) for j in range(0, k + 1)), Fraction(0))


def mr7_counts(weights: list[int], n: int) -> list[int]:
    """Integer coefficients of (sum_m w_m z^m)^n, built one draw at a time (exact)."""
    poly = [1]
    for _ in range(n):
        new = [0] * (len(poly) + 7)
        for s, c in enumerate(poly):
            if c:
                for m, w in enumerate(weights):
                    new[s + m] += c * w
        poly = new
    return poly


# ---------------------------------------------------------------- N1 generator (design section 7)

def _lp(b: bytes) -> bytes:
    return struct.pack('<I', len(b)) + b


class Stream:
    """SHAKE-256 output of a length-prefixed key, read as 64-bit little-endian words."""

    def __init__(self, fields: list[str]):
        self.key = b''.join(_lp(f.encode('utf-8')) for f in fields)
        self.buf = hashlib.shake_256(self.key).digest(256)
        self.pos = 0

    def word(self) -> int:
        if self.pos + 8 > len(self.buf):
            self.buf = hashlib.shake_256(self.key).digest(2 * len(self.buf))   # prefix-consistent
        w = int.from_bytes(self.buf[self.pos:self.pos + 8], 'little')
        self.pos += 8
        return w

    def below(self, k: int) -> int:
        limit = (1 << 64) - ((1 << 64) % k)
        while True:
            w = self.word()
            if w < limit:
                return w % k


def fair_draw(root_hex: str, policy: str, game: str, replicate: int, target: int):
    s = Stream(['PREDICTIVE_RANDOMNESS/N1_FAIR_DRAW_V1', policy, root_hex, game, str(replicate), str(target)])
    if game == 'POWERBALL':
        pool = list(range(1, 36))
        for i in range(7):
            j = i + s.below(35 - i)
            pool[i], pool[j] = pool[j], pool[i]
        return frozenset(pool[:7]), 1 + s.below(20)
    pool = list(range(1, 48))
    for i in range(10):
        j = i + s.below(47 - i)
        pool[i], pool[j] = pool[j], pool[i]
    return frozenset(pool[:7]), frozenset(pool[7:10])


def main() -> int:
    out = []
    say = out.append

    # 1. The sigma table of R3 17.5.3 and MRT-03's deficit example.
    say('1. Sigma conversion (decimal, deterministic), against R3 17.5.3:')
    for z, p in ((1, '0.158655'), (2, '0.0227501'), (3, '0.00134990'), (4, '3.16712e-5'), (5, '2.86652e-7'),
                 (6, '9.86588e-10')):
        q = upper_tail(D(z))
        say(f'   {z} sigma: Q = {float(q):.6g} (R3 {p}); back-converted {sigma_from_p(Fraction(str(float(q)))):.6f}')
    plo = binom_lower(291, Fraction(51597, 3362260), 0)
    say(f'   deficit example: zero PD9 wins in 291: P_lo = {float(plo):.6g}, deficit sigma = {sigma_from_p(plo):.5f}'
        ' (R3: 0.0111058, 2.28673)')

    # 2. MR16 reference rows (R3 17.6, MR16 table).
    say('2. MR16 reference rows, exact:')
    pb_any = Fraction(611573, 26898080)
    oz_any = Fraction(416512, 20963833)
    pb_m3 = Fraction(sum(PB_MAIN[3:]), comb(35, 7))
    oz_m3 = Fraction(sum(OZ_MAIN[3:]), comb(47, 7))
    three = Fraction(134990, 10 ** 8)
    for name, n, p in (('Powerball any division', 291, pb_any), ('Powerball 3+ main', 291, pb_m3),
                       ('Powerball hit', 291, Fraction(1, 20)), ('Oz Lotto any division', 220, oz_any),
                       ('Oz Lotto 3+ main', 220, oz_m3)):
        k = 0
        while binom_upper(n, p, k) > three:
            k += 1
        pw = [binom_upper(n, min(Fraction(1), c * p), k) for c in (Fraction(3, 2), Fraction(2))]
        say(f'   {name:24} n={n}: expected {float(n * p):.1f}; k_3 = {k} ({float(k / (n * p)):.2f}x);'
            f' power {float(pw[0]):.2f} / {float(pw[1]):.2f}')

    # 3. MR7's exact null for the default windows, and its cost.
    say('3. MR7 exact null distribution (integer coefficients):')
    for game, w, n in (('POWERBALL', PB_MAIN, 291), ('POWERBALL', PB_MAIN, 432), ('OZLOTTO', OZ_MAIN, 219)):
        t0 = time.perf_counter()
        c = mr7_counts(w, n)
        dt = time.perf_counter() - t0
        tot = sum(c)
        mean = Fraction(sum(s * x for s, x in enumerate(c)), tot)
        assert tot == sum(w) ** n
        say(f'   {game} n={n}: {len(c)} coefficients, built in {dt:.2f} s; exact mean {mean} per window'
            f' = {float(mean / n):.6f} per draw')

    # 4. N1 generator: speed, determinism and a distribution check on an invented root.
    root = 'AB' * 64            # INVENTED test root; never a real beacon value
    pol = 'N1_ROOT_TEST_ONLY_V1'
    t0 = time.perf_counter()
    R, T = 200, 291
    counts = [0] * 8
    pbh = 0
    ticket = frozenset(range(1, 8))
    for r in range(1, R + 1):
        for t in range(1286, 1286 + T):
            m, b = fair_draw(root, pol, 'POWERBALL', r, t)
            counts[len(m & ticket)] += 1
            pbh += b == 7
    dt = time.perf_counter() - t0
    say(f'4. N1 generator: {R * T} Powerball draws in {dt:.2f} s, so R = 10,000 x 291 draws takes about'
        f' {dt * 10000 / R:.0f} s')
    exp = [Fraction(x, comb(35, 7)) * R * T for x in PB_MAIN]
    chi = sum((counts[m] - exp[m]) ** 2 / exp[m] for m in range(5)) + \
        (sum(counts[5:]) - sum(exp[5:])) ** 2 / sum(exp[5:])
    say(f'   main-match counts {counts}; chi-square over 6 cells (5 df) = {float(chi):.2f}; Powerball hits'
        f' {pbh} of {R * T} (expected {R * T / 20:.0f})')
    a = fair_draw(root, pol, 'POWERBALL', 17, 1400)
    b = fair_draw(root, pol, 'POWERBALL', 17, 1400)
    c = fair_draw(root, pol, 'POWERBALL', 18, 1400)
    say(f'   determinism: replicate 17 target 1400 twice -> equal {a == b}; replicate 18 differs {a != c};'
        f' first draw {sorted(a[0])} + {a[1]} (invented root)')
    oz = fair_draw(root, pol, 'OZLOTTO', 1, 1500)
    say(f'   Oz Lotto shape: 7 main {sorted(oz[0])}, 3 supplementary {sorted(oz[1])}, disjoint {not (oz[0] & oz[1])}')
    # stream key bytes (published so a second implementation can match them)
    k = Stream(['PREDICTIVE_RANDOMNESS/N1_FAIR_DRAW_V1', pol, root, 'POWERBALL', '17', '1400'])
    say(f'   key SHA-256 for that draw: {hashlib.sha256(k.key).hexdigest()}; first word {k.word():016x}')

    # 5. MR1 exact comparison in N1 (design section 7.4).
    pd = [Fraction(1, 134490400), Fraction(19, 134490400), Fraction(49, 33622600), Fraction(931, 33622600),
          Fraction(3969, 67245200), Fraction(5733, 6724520), Fraction(75411, 67245200), Fraction(28665, 5379616),
          Fraction(51597, 3362260)]
    obs = [0, 0, 0, 0, 0, 1, 0, 3, 4]
    rep = [0, 0, 0, 0, 1, 0, 0, 0, 5]

    def prod(c):
        out_ = Fraction(1)
        for p_, e in zip(pd, c):
            out_ *= p_ ** e
        return out_
    # MR1 is the sum of -log2 p over wins; rep >= obs  <=>  prod(p^rep) <= prod(p^obs)
    exact = prod(rep) <= prod(obs)
    import math
    fl = sum(-math.log2(p_) * e for p_, e in zip(pd, rep)) >= sum(-math.log2(p_) * e for p_, e in zip(pd, obs))
    say(f'5. MR1 comparison decided exactly by rational products: replicate >= observed is {exact}'
        f' (float route agrees: {fl})')

    print('\n'.join(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
