#!/usr/bin/env python3
"""How large an effect ten draws can show: exact fair-draw arithmetic for the readiness sheet (Claude web chat,
13 November 2026). Illustration only: it reads no data, and it is not the Mode H report's statistics (the report
computes its own exact and N1 figures). Standard library; exact fractions.
The quantity is MR7's: the total number of a track's 7 picked main numbers that are drawn, summed over n draws, under
fair draws (hypergeometric per draw, independent draws); and, for Powerball, the count of correct Powerball numbers."""
from fractions import Fraction as F
from math import comb, sqrt

N_DRAWS, TRACKS = 10, 80


def hyp(N, K=7, n=7):
    return [F(comb(K, k) * comb(N - K, n - k), comb(N, n)) for k in range(n + 1)]


def conv(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def report(name, per_draw):
    d = [F(1)]
    for _ in range(N_DRAWS):
        d = conv(d, per_draw)
    mean = sum(k * x for k, x in enumerate(d))
    m1 = sum(k * x for k, x in enumerate(per_draw))
    sd1 = sqrt(float(sum(k * k * x for k, x in enumerate(per_draw)) - m1 * m1))
    tail = lambda s: sum(d[s:])
    crit = lambda a: next(s for s in range(len(d)) if tail(s) <= a)
    print(f'{name}: fair expectation {float(mean):.2f} over {N_DRAWS} draws ({float(m1):.3f} per draw, SD {sd1:.3f})')
    for label, a in (('one pre-chosen track, 5% one-sided', F(5, 100)),
                     (f'best of {TRACKS} tracks, 5% family-wise (Bonferroni)', F(5, 100 * TRACKS)),
                     ('3 sigma one-sided (0.00135)', F(135, 100000))):
        s = crit(a)
        print(f'    {label}: at least {s} (exact tail {float(tail(s)):.2e}); that is {float(s / mean):.2f} times the fair expectation')
    s5 = crit(F(5, 100))
    print(f'    if the {TRACKS} tracks were independent and fair, P(at least one reaches the one-track 5% line) = '
          f'{float(1 - (1 - tail(s5)) ** TRACKS):.2f}')
    for lift in (0.05, 0.10):
        n = ((1.645 + 0.842) * sd1 / (lift * float(m1))) ** 2
        print(f'    draws needed for one pre-chosen track to show a {lift:.0%} lift (5% one-sided, 80% power, normal approx.): about {n:,.0f}')


report('POWERBALL main numbers (7 picked of 35; 7 drawn)', hyp(35))
report('OZLOTTO main numbers (7 picked of 47; 7 drawn)', hyp(47))
report('POWERBALL number (1 picked of 20)', [F(19, 20), F(1, 20)])
