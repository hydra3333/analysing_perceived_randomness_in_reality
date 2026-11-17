"""MHUP-B slice 2: the full-size brute-force check of OV-1's exact distribution (code plan v0.3 section 6.5). An evidence
run, not a unit test: for each weight pattern it enumerates EVERY 7-number subset of the barrel and requires the counts
to equal the kernel's (both of its routes). Invented weights only.
Usage: python3 -I ov1_bruteforce_evidence.py TREE        (TREE: a built dev tree)
"""
import itertools
import sys
import time
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'src'))
from evaluation import ov1_numeric as N                                       # noqa: E402


def tickets(n, pairs):
    w = [0] * n
    for top, worst in pairs:
        for j in top:
            w[j] += 1
        for j in worst:
            w[j] -= 1
    return w


CASES = [
    ('N=35, the reviewer\'s counterexample (40 identical variants)', [40] * 7 + [-40] * 7 + [0] * 21),
    ('N=35, 23 overlapping variants', tickets(35, [([(i * 3 + j * 5) % 35 for j in range(7)],
                                                    [(i * 3 + j * 5 + 17) % 35 for j in range(7)]) for i in range(23)])),
    ('N=47, 31 overlapping variants', tickets(47, [([(i * 4 + j * 6) % 47 for j in range(7)],
                                                    [(i * 4 + j * 6 + 23) % 47 for j in range(7)]) for i in range(31)])),
]
for name, w in CASES:
    assert sum(w) == 0 and len(set(w)) > 2, name
    t = time.time()
    brute = {}
    for sub in itertools.combinations(w, 7):
        x = sum(sub)
        brute[x] = brute.get(x, 0) + 1
    assert sum(brute.values()) == comb(len(w), 7)
    assert brute == N.counts_by_number(w) == N.counts_by_group(w) == N.counts(w), name
    print(f'{name}: all {comb(len(w), 7):,} subsets enumerated; {len(brute)} values of X; equal to both routes of the '
          f'kernel ({time.time() - t:.0f} s)', flush=True)
print(f'python {sys.version.split()[0]}; kernel {N.KERNEL_VERSION}; BRUTE-FORCE EVIDENCE PASS')
