#!/usr/bin/env python3
"""D4 Powerball primary/secondary isolated synthetic arithmetic qualification.

No imports of production mode, scanner, histories, packed files, or saved legacy
matches. No writes. This is a focused mathematical oracle; the existing Q4h
synthetic integration harness tests report persistence and separate Holm families.
"""
from __future__ import annotations

import math
import random
import statistics

import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S


def reference_gaps(sets):
    """Independent brute-force evaluator of each adjacent synthetic pair."""
    out = []
    for a, b in zip(sets, sets[1:]):
        if a and b:
            out.append(min(abs(x-y) for x in a for y in b))
    return out


def reference_geometric(gaps):
    if not gaps:
        return None
    return round(math.fsum(math.log10(int(g)+1) for g in sorted(gaps))/len(gaps), 12)


def reference_permutation(sets, seed, iterations):
    rng = random.Random(seed)
    observed = reference_gaps(sets)
    med = statistics.median(observed) if observed else None
    geom = reference_geometric(observed)
    meds, geoms = [], []
    for _ in range(iterations):
        shuffled = list(sets)
        rng.shuffle(shuffled)
        gaps = reference_gaps(shuffled)
        if gaps:
            meds.append(statistics.median(gaps))
            geoms.append(reference_geometric(gaps))
    def centred(observed, v):
        if observed is None or not v:
            return None
        c = round(statistics.median(v), 12) if observed == geom else statistics.median(v)
        return (1 + sum(abs(x-c) >= abs(observed-c) for x in v))/(1+len(v))
    return med, geom, centred(med,meds), centred(geom,geoms), len(meds)


def main():
    # Hand-computed tiny fixture: zero gap -> log10(1)=0; 9 -> log10(10)=1.
    assert S.geometric_mean_log_gap([0,9]) == 0.5
    assert S.geometric_mean_log_gap([9,0]) == 0.5
    assert S.geometric_mean_log_gap([0,0]) == 0.0
    assert S.geometric_mean_log_gap([]) is None
    assert S.geometric_mean_log_gap([0,3,15]) == round((0+math.log10(4)+math.log10(16))/3,12)
    for bad in ([1,-1],[3.5],['3']):
        try:
            S.geometric_mean_log_gap(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid gap accepted')

    # Multiple offsets, empty draws and a repeated position. Primary and
    # secondary must share exactly the same draws/shuffles/validity rule.
    sets = ((0,3), (0,9), (), (30,), (0,70), (100,), (), (100,))
    count = 10000
    seed = 271828
    med, geom, mp, gp, valid = reference_permutation(sets,seed,count)
    actual = S.permutation_test(sets, seed=seed, iterations=count,
                                geometric_primary=True)
    assert actual['observed_median'] == med
    assert actual['geometric_primary']['observed'] == geom
    assert actual['median_secondary']['observed'] == med
    assert actual['centered_two_sided_p'] == mp
    assert actual['median_secondary']['centered_two_sided_p'] == mp
    assert actual['geometric_primary']['centered_two_sided_p'] == gp
    assert actual['valid_permutations'] == valid
    assert actual['valid_permutations'] + actual['undefined_permutations'] == count
    assert actual == S.permutation_test(sets, seed=seed, iterations=count,
                                        geometric_primary=True)

    # Every existing top-level median result is retained, exactly.
    previous = S.permutation_test(sets, seed=seed, iterations=count)
    for key, value in previous.items():
        assert actual[key] == value, key

    # N/A all empty, and a single populated draw, must not invent p-values.
    for missing in (((),(),()), ((),(0,),())):
        q = S.permutation_test(missing,seed=seed,iterations=17,geometric_primary=True)
        assert q['geometric_primary']['observed'] is None
        assert q['median_secondary']['observed'] is None
        assert q['geometric_primary']['centered_two_sided_p'] is None
        assert q['median_secondary']['centered_two_sided_p'] is None
        assert q['valid_permutations'] == 0

    # Two Holm families are independent and conservatively retain six slots.
    names = S.CONSTANTS
    p = dict(zip(names,(0.001,0.04,None,0.20,0.8,0.02)))
    q = dict(zip(names,(0.9,0.01,0.03,None,0.8,0.2)))
    a = S.holm_six_constants(p)
    b = S.holm_six_constants(q)
    assert a['pi'] == 0.006 and b['phi'] == 0.06
    assert a['e'] is None and b['log2'] is None
    assert a != b
    print('Q4K D4 SYNTHETIC STATISTICS PASS: hand-checks=5 independent-oracle=10000 '
          'median-compatibility=PASS all-empty-N/A=PASS separate-Holm=PASS '
          'production-scans=0 REAL-history-reads=0')


if __name__ == '__main__':
    main()
