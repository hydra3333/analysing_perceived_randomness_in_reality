"""Exact enumerations used to test calibration claims (fractions, no floats).
1. Adaptive cross-track maximum: true 1/16 vs fixed-forecast replay 15/128.
2. Single-track hit count: true law equals replay law (invariance).
3. Forecast-weighted single track: true law differs from replay.
4. Adaptive stopping at a nominal 5% boundary within 20 draws: 6467/65536.
Lesson: build the smallest exhaustive toy that could break a claim.
"""
import itertools
from collections import Counter
from fractions import Fraction as F
from scipy.stats import binom
H = list(itertools.product([0, 1], repeat=4))
fA = lambda h: (0, 0, 0, 0)
fB = lambda h: (0, h[0], h[1], h[2])
hits = lambda f, y: sum(a == b for a, b in zip(f, y))
true = F(sum(1 for h in H if max(hits(fA(h), h), hits(fB(h), h)) == 4), 16)
rep = sum(F(sum(1 for y in H if max(hits(fA(h), y), hits(fB(h), y)) == 4), 16) for h in H) / 16
print('1. cross-track max  true', true, ' replay', rep)
t = Counter(hits(fB(h), h) for h in H); r = Counter()
for h in H:
    for y in H: r[hits(fB(h), y)] += F(1, 256)
print('2. single-track hits equal:', {k: F(v, 16) for k, v in t.items()} == dict(r))
sc = lambda f, y: sum((2 if a == 1 else 1) * b for a, b in zip(f, y))
t = Counter(sc(fB(h), h) for h in H); r = Counter()
for h in H:
    for y in H: r[sc(fB(h), y)] += F(1, 256)
print('3. weighted equal:', {k: F(v, 16) for k, v in t.items()} == dict(r))
alive = {0: F(1)}; crossed = F(0)
for n in range(1, 21):
    new = {}
    for k, pr in alive.items():
        for h in (0, 1):
            kk, p = k + h, pr / 2
            if binom.sf(kk - 1, n, 0.5) <= 0.05: crossed += p
            else: new[kk] = new.get(kk, 0) + p
    alive = new
print('4. stopping-rule false alarm', crossed, float(crossed))
