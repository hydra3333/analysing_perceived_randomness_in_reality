"""WF-1 design v0.1r1 - numerics probe 2 (Claude, 30 October 2026; EX_078 WF1-R3-C04).
Checks the two normal-tail routes with the route switch moved to x = 5, and an exact binomial tail
computed on its shorter side over a common integer denominator (exact, so no cancellation).
Fair-draw arithmetic only.  python3 -I probe_numerics2.py"""
import sys, time
from decimal import Decimal as D, getcontext
from fractions import Fraction
from math import comb
getcontext().prec = 80
PI = D('3.14159265358979323846264338327950288419716939937510582097494459')

def erf_series(x):
    total, term, n = D(0), x, 0
    while True:
        add = term / (2 * n + 1); total += add
        if abs(add) < D(10) ** -75: break
        n += 1; term = -term * x * x / n
    return 2 * total / PI.sqrt()

def erfc_cf(x, depth):
    f = D(0)
    for k in range(depth, 0, -1): f = D(k) / 2 / (x + f)
    return (-(x * x)).exp() / (x + f) / PI.sqrt()

def binom_tail_exact(n, a, b, k):
    """P(X >= k), X ~ Bin(n, a/b), exactly: the shorter side over the common denominator b^n."""
    def pmf_num(j): return comb(n, j) * a ** j * (b - a) ** (n - j)
    if k <= 0: return Fraction(1)
    if k > n: return Fraction(0)
    if n - k + 1 <= k:
        num = sum(pmf_num(j) for j in range(k, n + 1))
    else:
        num = b ** n - sum(pmf_num(j) for j in range(0, k))
    return Fraction(num, b ** n)

out = []
w = max(abs((1 - erf_series(D(x) / 10)) - erfc_cf(D(x) / 10, 400)) / erfc_cf(D(x) / 10, 400) for x in range(50, 61))
out.append(f'1. series vs continued fraction (depth 400) on x in [5.0, 6.0]: worst relative difference {float(w):.1e}')
w = max(abs(erfc_cf(D(x), 400) - erfc_cf(D(x), 4000)) / erfc_cf(D(x), 4000) for x in (5, 8, 20, 45))
out.append(f'2. continued fraction depth 400 vs 4000 at x = 5, 8, 20, 45: worst relative difference {float(w):.1e}')
for n, a, b, k in ((5000, 1, 10 ** 9, 40), (5000, 1, 10 ** 9, 3), (5000, 51597, 3362260, 120), (432, 611573, 26898080, 16)):
    t0 = time.perf_counter(); p = binom_tail_exact(n, a, b, k); dt = time.perf_counter() - t0
    import math
    lg = math.log10(p.numerator) - math.log10(p.denominator)
    out.append(f'3. exact P(X>={k}), n={n}, p={a}/{b}: log10 {lg:.4f}, in {dt:.3f} s')
print('\n'.join(out))
