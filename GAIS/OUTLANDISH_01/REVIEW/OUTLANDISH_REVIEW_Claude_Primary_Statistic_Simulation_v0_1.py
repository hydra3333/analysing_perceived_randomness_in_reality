#!/usr/bin/env python3
"""OUTLANDISH_01 reviewer's primary-statistic simulation, v0.1 (Claude, memo 005).

Purpose
    Evidence behind the owner's 16 Nov decision to make the geometric-mean gap
    the Powerball primary W -> W+1 statistic, with the median gap as the
    pre-declared secondary. It compares how often each statistic detects a
    planted adjacency effect, and how often it raises a false alarm.

Model (simulated data only)
    N = 10^10 digits, 433 draws, P3_any events per draw ~ Poisson(0.504),
    which gives about 218 events per constant, as v0.2 B5.1 expects.
    Event positions are uniform. An "effect" gives a fraction f of draws one
    extra hit within +/- width digits of a hit of the previous draw.
    For each data set, both statistics use the SAME evaluable pairs, the SAME
    per-pair minimum absolute gaps and the SAME whole-draw-set shuffles
    (empty draws included), with the centred two-sided p of v0.2 B5.4.
      median statistic   = median of the gaps                 (former primary)
      geometric statistic = mean of log10(gap + 1)            (new primary)
    Detection is p below 0.05/6, the six-constant Holm threshold for the
    smallest p-value (column 1, 2), and below 0.05/12 for two equal primaries
    (columns 3 to 5).

What it does NOT do
    No project data of any kind: no constants, receipts, histories or results.
    It does not import project code; it re-implements the statistic so that it
    is an independent check. It writes nothing.

Usage (Windows CMD, from the repository root)
    ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\REVIEW\\OUTLANDISH_REVIEW_Claude_Primary_Statistic_Simulation_v0_1.py" --run
    --full gives the reviewer's sample sizes (slower, about 30 to 60 minutes).

Reviewer's --full result (Linux, Python 3.13.18), detection per constant:
    effect                          median/6  geomean/6 | median/12 geomean/12 either/12
    none                              0.0%      0.7%    |   0.0%      0.3%      0.3%
    sparse: ~5 pairs within 1e6       0.0%     81.0%    |   0.0%     78.0%     78.0%
    sparse: ~9 pairs within 1e6       2.0%     99.0%    |   0.0%     97.0%     97.0%
    sparse: ~17 pairs within 1e6     28.0%    100.0%    |  21.0%    100.0%    100.0%
    broad: ~34 pairs within 1e9      94.0%     96.0%    |  91.0%     94.0%     95.0%
    broad: ~68 pairs within 1e9     100.0%    100.0%    | 100.0%    100.0%    100.0%
    broad: ~68 pairs within 2e9      97.0%    100.0%    |  93.0%    100.0%    100.0%
Larger confirming runs (1,000 shuffles each, same model):
    none, 600 sets:                       median 0.7%, geometric 0.7% (nominal 0.83%)
    broad ~34 pairs within 1e9, 400 sets: median 96.2%, geometric 97.0%
    broad ~17 pairs within 1e9, 400 sets: median 30.0%, geometric 48.2%
Quick mode uses fewer data sets and shuffles, so its figures are noisier; a
quick-mode row can show the median a few points ahead on a broad effect by
chance (the reviewer's quick run showed 97.5% against 90.0% on 40 sets).
"""
from __future__ import annotations

import argparse
import bisect
import math
import random
import statistics
import sys
import time

sys.dont_write_bytecode = True

N = 10**10
DRAWS = 433
MEAN_EVENTS = 0.504            # 218.2 expected P3_any events / 433 draws

SCENARIOS = (
    ('none', 0.00, 10**6),
    ('sparse: ~5 pairs within 1e6', 0.03, 10**6),
    ('sparse: ~9 pairs within 1e6', 0.05, 10**6),
    ('sparse: ~17 pairs within 1e6', 0.10, 10**6),
    ('broad: ~34 pairs within 1e9', 0.20, 10**9),
    ('broad: ~68 pairs within 1e9', 0.40, 10**9),
    ('broad: ~68 pairs within 2e9', 0.40, 2 * 10**9),
)


def poisson(rng: random.Random, lam: float) -> int:
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def dataset(rng: random.Random, f: float, width: int):
    sets = [sorted(rng.randrange(N) for _ in range(poisson(rng, MEAN_EVENTS))) for _ in range(DRAWS)]
    for w in range(DRAWS - 1):
        if sets[w] and rng.random() < f:
            near = rng.choice(sets[w]) + rng.randrange(-width, width)
            sets[w + 1] = sorted(sets[w + 1] + [min(N - 1, max(0, near))])
    return sets


def gaps(sets):
    """Per evaluable adjacent pair, the minimum absolute gap."""
    out = []
    for a, b in zip(sets, sets[1:]):
        if not a or not b:
            continue
        best = None
        for x in a:
            i = bisect.bisect_left(b, x)
            for j in (i - 1, i):
                if 0 <= j < len(b):
                    g = abs(b[j] - x)
                    if best is None or g < best:
                        best = g
        out.append(best)
    return out


def median_stat(g):
    return statistics.median(g)


def geometric_stat(g):
    return math.fsum(math.log10(x + 1) for x in sorted(g)) / len(g)


def centred_p(observed, values):
    centre = statistics.median(values)
    b = sum(abs(v - centre) >= abs(observed - centre) for v in values)
    return (1 + b) / (len(values) + 1)


def both_p(sets, rng, shuffles):
    g0 = gaps(sets)
    if not g0:
        return None, None
    med, geo = [], []
    for _ in range(shuffles):
        trial = sets[:]
        rng.shuffle(trial)
        g = gaps(trial)
        if g:
            med.append(median_stat(g))
            geo.append(geometric_stat(g))
    return centred_p(median_stat(g0), med), centred_p(geometric_stat(g0), geo)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--run', action='store_true', required=True)
    parser.add_argument('--full', action='store_true', help="reviewer's sample sizes (slow)")
    args = parser.parse_args()
    sets_null, sets_effect, shuffles = (300, 100, 2000) if args.full else (100, 40, 1000)
    rng = random.Random(5)
    started = time.perf_counter()
    print(f'simulated: N=1e10, {DRAWS} draws, mean {MEAN_EVENTS} P3 events/draw; '
          f'{shuffles} shuffles; {sets_null} null / {sets_effect} effect data sets per row')
    print(f'{"effect":<32} | {"median/6":>8} {"geomean/6":>9} | {"median/12":>9} {"geomean/12":>10} {"either/12":>9}')
    rows = {}
    for label, f, width in SCENARIOS:
        n = sets_null if f == 0 else sets_effect
        counts = [0, 0, 0, 0, 0]
        for _ in range(n):
            pm, pg = both_p(dataset(rng, f, width), rng, shuffles)
            if pm is None:
                continue
            counts[0] += pm < 0.05 / 6
            counts[1] += pg < 0.05 / 6
            counts[2] += pm < 0.05 / 12
            counts[3] += pg < 0.05 / 12
            counts[4] += min(pm, pg) < 0.05 / 12
        rows[label] = [c / n for c in counts]
        r = rows[label]
        print(f'{label:<32} | {r[0]:>8.1%} {r[1]:>9.1%} | {r[2]:>9.1%} {r[3]:>10.1%} {r[4]:>9.1%}', flush=True)

    null = rows['none']
    sparse = rows['sparse: ~9 pairs within 1e6']
    if null[1] > 0.05 or null[0] > 0.05:
        raise SystemExit('UNEXPECTED: false-alarm rate far above nominal')
    if not sparse[1] > sparse[0] + 0.5:
        raise SystemExit('UNEXPECTED: geometric mean not clearly stronger on the sparse effect')
    print(f'REVIEWER PRIMARY-STATISTIC SIMULATION PASS: geometric mean matched or beat the median; '
          f'sparse ~9 pairs: median {sparse[0]:.0%}, geometric {sparse[1]:.0%}; '
          f'{time.perf_counter() - started:.0f} s')
    print('  SIMULATED DATA ONLY; no project data read; not Q5 authorisation.')


if __name__ == '__main__':
    main()
