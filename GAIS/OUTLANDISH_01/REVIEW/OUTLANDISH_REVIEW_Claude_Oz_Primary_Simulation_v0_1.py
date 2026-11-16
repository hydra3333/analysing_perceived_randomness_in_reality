"""OUTLANDISH_01 reviewer evidence for memo 008: choosing the Oz Lotto primary (owner decision D6).

Simulated data only. Reads no project data, no draw history and no constant; imports no project
code. For each Oz match family it fabricates 220 draws of random hit positions in 10^10 digits,
optionally plants a consecutive-draw effect, and applies the D4 statistic (mean over evaluable
adjacent pairs of log10(minimum absolute gap + 1)) with a whole-draw-set permutation test and a
centred two-sided p. It prints how often one constant is detected at 0.05/6 (the family as sole
primary) and at 0.05/18 (three co-primary families, the hardest Holm step).

Run:  python OUTLANDISH_REVIEW_Claude_Oz_Primary_Simulation_v0_1.py          (about 4 to 8 minutes)
      python OUTLANDISH_REVIEW_Claude_Oz_Primary_Simulation_v0_1.py --quick  (about 1 minute, noisier)
Needs Python 3 and NumPy. Final line: REVIEWER OZ PRIMARY SIMULATION DONE
"""
import sys
import time
import numpy as np

N, D = 10**10, 220
# (label, expected hits per draw at 10^10 digits): 5040, 15120, 105840 and 5040 accepted strings.
FAMILIES = (('O1_any (K7)', 0.504), ('O2_supp_last', 1.512), ('O2_any_slot (K7mix)', 10.584), ('O3_any (K6)', 50.4))


def dataset(rng, lam, model, strength, width):
    sets = [np.sort(rng.integers(0, N, size=rng.poisson(lam))) for _ in range(D)]
    if model != 'none':
        for w in range(D - 1):
            a = sets[w]
            if a.size == 0:
                continue
            if model == 'pair':    # with probability `strength`, one hit of draw W gains a partner in W+1
                src = a[rng.integers(0, a.size, size=1)] if rng.random() < strength else a[:0]
            else:                  # 'event': each hit of draw W gains a partner in W+1 with probability `strength`
                src = a[rng.random(a.size) < strength]
            if src.size:
                extra = np.clip(src + rng.integers(-width, width + 1, size=src.size), 0, N - 1)
                sets[w + 1] = np.sort(np.concatenate([sets[w + 1], extra]))
    return sets


def log_gap_matrix(sets):
    """L[i, j] = log10(min |a - b| + 1) over a in set i, b in set j; nan if either set is empty."""
    L = np.full((D, D), np.nan)
    idx = [i for i in range(D) if sets[i].size]
    if len(idx) < 2:
        return L
    allv = np.concatenate([sets[i] for i in idx])
    starts = np.cumsum([0] + [sets[i].size for i in idx])[:-1]
    for i in idx:
        a = sets[i]
        k = np.searchsorted(a, allv)
        lo = np.abs(allv - a[np.clip(k - 1, 0, a.size - 1)])
        hi = np.abs(a[np.clip(k, 0, a.size - 1)] - allv)
        L[i, idx] = np.log10(np.minimum.reduceat(np.minimum(lo, hi), starts) + 1.0)
    return L


def stat(L, order):
    v = L[order[..., :-1], order[..., 1:]]
    cnt = np.sum(~np.isnan(v), axis=-1)
    with np.errstate(invalid='ignore'):
        m = np.nansum(v, axis=-1) / cnt
    return np.where(cnt > 0, m, np.nan), cnt


def pvalue(L, rng, perms):
    obs, cnt = stat(L, np.arange(D))
    if cnt == 0:
        return None, 0
    orders = rng.permuted(np.tile(np.arange(D), (perms, 1)), axis=1)
    vals, _ = stat(L, orders)
    vals = np.round(vals[~np.isnan(vals)], 12)
    obs = round(float(obs), 12)
    c = round(float(np.median(vals)), 12)
    return (1 + int(np.sum(np.abs(vals - c) >= abs(obs - c)))) / (vals.size + 1), int(cnt)


def main():
    quick = '--quick' in sys.argv[1:]
    perms, n_null, n_eff = (1000, 100, 30) if quick else (3000, 400, 100)
    cells = [('none', 0, 0)]
    cells += [('pair', f, w) for w in (10**3, 10**5, 10**7) for f in (0.05, 0.15)]
    cells += [('event', q, w) for w in (10**3, 10**5, 10**7) for q in (0.002, 0.01)]
    print(f'draws={D} digits={N} permutations={perms} null_sets={n_null} effect_sets={n_eff}')
    t0 = time.time()
    for part in (0, 1):            # two independent streams, as in the run reported in memo 008
        rng = np.random.default_rng(1000 + part)
        for name, lam in FAMILIES[part::2]:
            for model, s, w in cells:
                n = n_null if model == 'none' else n_eff
                hit6 = hit18 = 0
                pairs = []
                for _ in range(n):
                    p, c = pvalue(log_gap_matrix(dataset(rng, lam, model, s, w)), rng, perms)
                    pairs.append(c)
                    hit6 += p is not None and p < 0.05 / 6
                    hit18 += p is not None and p < 0.05 / 18
                print(f'{name:<20} {model:<5} strength={s:<6} width={w:<9} pairs={np.mean(pairs):5.0f}  '
                      f'detect_at_6={hit6 / n:6.1%} detect_at_18={hit18 / n:6.1%}', flush=True)
    print(f'REVIEWER OZ PRIMARY SIMULATION DONE in {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
