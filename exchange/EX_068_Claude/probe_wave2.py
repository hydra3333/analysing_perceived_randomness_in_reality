"""Author probes for wave 2 on invented draws only (never real data). Deterministic: sha256 orderings, no PRNG."""
import hashlib, sys, time
from fractions import Fraction as Fr
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R


def u(*a):
    return int.from_bytes(hashlib.sha256(':'.join(map(str, a)).encode()).digest()[:8], 'big') / 2 ** 64


def fair(n, low, high, k, seed):
    out = []
    for i in range(n):
        pool = sorted(range(low, high + 1), key=lambda j: hashlib.sha256(f'{seed}:{i}:{j}'.encode()).digest())
        out.append(sorted(pool[:k]))
    return out


def planted(n, low, high, k, seed, rule):
    """rule(i, prev_draws, j) -> weight multiplier; draws k labels by weighted sampling without replacement."""
    out = []
    for i in range(n):
        labels = list(range(low, high + 1))
        chosen = []
        for s in range(k):
            ws = [rule(i, out, j) for j in labels]
            t = u(seed, i, s) * sum(ws)
            acc = 0
            for j, w in zip(labels, ws):
                acc += w
                if t < acc:
                    break
            chosen.append(j)
            labels.remove(j)
        out.append(sorted(chosen))
    return out


VARIANTS = {
    'E2_MEAN': lambda h, lo, hi, K: R.e2(h, lo, hi, K, 'mean'),
    'E2_MEDIAN': lambda h, lo, hi, K: R.e2(h, lo, hi, K, 'median'),
    'E2_MEAN_LAST8': lambda h, lo, hi, K: R.e2(h, lo, hi, K, 'mean', 8),
    'E17_BINS_C100': lambda h, lo, hi, K: R.e17_bins(h, lo, hi, K, 100),
    'E17_BINS_W208_C100': lambda h, lo, hi, K: R.e17_bins(h, lo, hi, K, 100, 208),
    'E17_LOGSLOPE': lambda h, lo, hi, K: R.e17_logslope(h, lo, hi, K)[0],
    'E19_T2': lambda h, lo, hi, K: R.e19(h, lo, hi, K, 2)[0],
    'E19_T3': lambda h, lo, hi, K: R.e19(h, lo, hi, K, 3)[0],
    'E19_T4': lambda h, lo, hi, K: R.e19(h, lo, hi, K, 4)[0],
    'E18_C10': lambda h, lo, hi, K: R.e18(h, lo, hi, K, 10)[0],
    'E18_W208_C10': lambda h, lo, hi, K: R.e18(h, lo, hi, K, 10, 208)[0],
    'E18_W104_C10': lambda h, lo, hi, K: R.e18(h, lo, hi, K, 10, 104)[0],
}

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'timing':
        for name, (n, lo, hi, K) in {'PB MAIN 433': (433, 1, 35, 7), 'PB POWERBALL 433': (433, 1, 20, 1),
                                     'Oz MAIN 218': (218, 1, 47, 7)}.items():
            h = fair(n, lo, hi, K, name)
            row = []
            for v, f in VARIANTS.items():
                t0 = time.perf_counter()
                f(h, lo, hi, K)
                row.append(f'{v} {time.perf_counter() - t0:.2f}s')
            print(name, '; '.join(row))
    elif which == 'fair':
        h = fair(433, 1, 35, 7, 'fairprobe')
        hp = fair(433, 1, 20, 1, 'fairprobe-pb')
        betas, phis, w18 = [], [], []
        for W in range(104, 434, 11):
            betas.append(R.e17_logslope(h[:W], 1, 35, 7)[1])
            phis.append(R.e19(h[:W], 1, 35, 7, 2)[1])
            w = R.e18(h[:W], 1, 35, 7, 10)[1]
            w18.append(sum(1 - x[1] for x in w.values()) / 35)
        print('MAIN fair, targets', len(betas), 'beta>0 at', sum(b > 0 for b in betas),
              'beta range', float(min(betas)), float(max(betas)))
        print('MAIN fair E_19 T=2 phi range', min(float(p[0]) for p in phis), max(float(p[0]) for p in phis),
              min(float(p[1]) for p in phis), max(float(p[1]) for p in phis))
        print('MAIN fair E_18 C10 mean non-fair weight per target: min', float(min(w18)), 'max', float(max(w18)))
        bp = [R.e17_logslope(hp[:W], 1, 20, 1)[1] for W in range(104, 434, 11)]
        print('PB fair beta>0 at', sum(b > 0 for b in bp), 'of', len(bp))
    elif which == 'planted':
        # (a) clustering: a label drawn last draw is 1.6x as likely; (b) a 2-cycle: label 17 x3 on odd draws;
        # (c) a regular cycle: label 5 x4 when its age is 5, x0.25 otherwise
        def last_age(prev, j):
            for a, d in enumerate(reversed(prev), 1):
                if j in d:
                    return a
            return None
        rules = {
            'clustering': lambda i, prev, j: 1.6 if prev and j in prev[-1] else 1.0,
            'two-cycle 17': lambda i, prev, j: 3.0 if (j == 17 and i % 2) else 1.0,
            'cycle5 label 5': lambda i, prev, j: (4.0 if last_age(prev, j) == 5 else 0.25) if j == 5 else 1.0,
        }
        for name, rule in rules.items():
            h = planted(433, 1, 35, 7, name, rule)
            s, beta = R.e17_logslope(h, 1, 35, 7)
            hz, _ = R.binned_hazard(h, 1, 35, 7, 100)
            _, phi, _ = R.e19(h, 1, 35, 7, 2)
            _, w = R.e18(h, 1, 35, 7, 10)
            print(f'{name}: beta {float(beta):+.4f}; E_17 bin hazards', [round(float(x), 3) for x in hz],
                  '; E_19 T2 phi', [round(float(x), 3) for x in phi],
                  '; E_18 weights label 5', [round(float(x), 3) for x in w[5]], 'label 17',
                  [round(float(x), 3) for x in w[17]])
