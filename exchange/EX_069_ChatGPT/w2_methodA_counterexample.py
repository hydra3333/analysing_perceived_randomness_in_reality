"""Independent wave-2 R-3 counterexample; synthetic data only, no inputs or randomness.

The exact sign of the log-age covariance is determined by prime-exponent
integer products, never by floating-point logarithms. Harmonic sign uses Fraction.
"""
from fractions import Fraction
import hashlib

L, K, W, SEED = 35, 7, 104, 32
last = [0] * L
R, E = {}, {}
for t in range(1, W + 1):
    labels = sorted(range(1, L + 1),
                    key=lambda j: hashlib.sha256(f'{SEED}|{t}|{j}'.encode('ascii')).digest())[:K]
    current = set(labels)
    for j in range(1, L + 1):
        if last[j - 1]:
            k = t - last[j - 1]
            R[k] = R.get(k, 0) + 1
            if j in current:
                E[k] = E.get(k, 0) + 1
    for j in current:
        last[j - 1] = t

N = sum(R.values())
Y = sum(E.values())
coeff = {k: N * E.get(k, 0) - Y * r for k, r in R.items()}
assert sum(coeff.values()) == 0
H = Fraction(0)
s_H = Fraction(0)
for k in range(1, max(R) + 1):
    H += Fraction(1, k)
    s_H += coeff.get(k, 0) * H

def factors(k):
    d = 2
    while d * d <= k:
        while k % d == 0:
            yield d
            k //= d
        d += 1
    if k > 1:
        yield k

prime_exponents = {}
for k, c in coeff.items():
    for p in factors(k):
        prime_exponents[p] = prime_exponents.get(p, 0) + c
plus = minus = 1
for p, exponent in prime_exponents.items():
    if exponent > 0:
        plus *= p ** exponent
    elif exponent < 0:
        minus *= p ** (-exponent)
assert plus < minus  # log-age fitted slope is negative, exactly.
assert s_H > 0        # harmonic-age fitted slope is positive, exactly.
G = {j: W + 1 - last[j - 1] if last[j - 1] else W + 1 for j in range(1, L + 1)}
assert len(set(G.values())) > 2
print('PASS: 104 deterministic synthetic draws, 35 labels, 7 per draw')
print('S_log sign - (exact prime-factor integer product comparison)')
print('S_H sign + (exact Fraction)', 'numerator', s_H.numerator,
      'denominator', s_H.denominator)
print('Projected ages:', G)
print('Method-A log-age slope ranks youngest-age first; E17 harmonic slope ranks oldest-age first')
