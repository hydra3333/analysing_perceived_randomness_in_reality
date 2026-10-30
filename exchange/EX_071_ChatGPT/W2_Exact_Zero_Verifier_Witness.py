#!/usr/bin/env python3
"""Synthetic W2 zero-sign witness; standard library only; no project or data reads.

Demonstrates that nonzero raw age coefficients can have a zero log-age
combination, and that direct rational log intervals cannot certify that
zero by sign-exclusion, however many terms are used.
"""
from collections import Counter
from fractions import Fraction as F

# 8 valid draws, L=2, K=1. The toy barrel is for a helper/verify boundary
# test, not a released E_17 target (which has its own burn-in).
draws = [(1,), (1,), (2,), (2,), (1,), (1,), (1,), (2,)]
last = {1: None, 2: None}
R, E = Counter(), Counter()
for i, drawn in enumerate(draws, 1):
    assert len(drawn) == 1 and drawn[0] in last
    for label in last:
        if last[label] is not None:
            age = i - last[label]
            R[age] += 1
            if label in drawn:
                E[age] += 1
    last[drawn[0]] = i
n, e = sum(R.values()), sum(E.values())
a = {k: n * E[k] - e * count for k, count in sorted(R.items())}
assert (n, e) == (12, 6)
assert a == {1: 6, 2: -12, 3: 0, 4: 6}
assert a[2] + 2 * a[4] == 0  # exact prime-2 exponent cancellation
assert sum(a.values()) == 0


def atanh_interval(x, terms):
    total = F(0)
    power = x
    for index in range(terms):
        total += power / (2 * index + 1)
        power *= x * x
    upper = total + power / ((2 * terms + 1) * (1 - x * x))
    return (total, upper)


def log_interval(k, terms):
    shift = k.bit_length() - 1
    log2lo, log2hi = atanh_interval(F(1, 3), terms)
    mantissa = F(k, 2 ** shift)
    if mantissa == 1:
        tlo = thi = F(0)
    else:
        tlo, thi = atanh_interval((mantissa - 1) / (mantissa + 1), terms)
    return 2 * (shift * log2lo + tlo), 2 * (shift * log2hi + thi)


for terms in (1, 2, 4, 8, 16, 32):
    lo = hi = F(0)
    for k, coefficient in a.items():
        l, h = log_interval(k, terms)
        lo += coefficient * (l if coefficient > 0 else h)
        hi += coefficient * (h if coefficient > 0 else l)
    assert lo < 0 < hi, terms
    print(f"terms={terms:2d}: direct sign-exclusion unavailable (lower<0<upper)")
print("PASS: prime-factor route proves true zero; direct log bounds cannot exclude zero.")
print("Design implication: verify() needs a terminating independent exact-zero branch.")
