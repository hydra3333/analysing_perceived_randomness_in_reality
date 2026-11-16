"""Post hoc, exploratory arithmetic on the reports' own per-track totals (no draw value involved):
(1) how big are the aggregate leans once the overlap between methods is allowed for (overlap estimated from the spread of
the track totals themselves); (2) what the family test could detect; (3) cross-game consistency per variant."""
import re, sys, math, statistics as st
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from parse_report import parse
num = r'([-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)'

def load(path):
    lines, T, meta = parse(path)
    A = {r['unit'].split(':', 1)[1]: int(re.search(r'main matches (\d+)', r['extra'][0]).group(1)) for r in T[('A', 'MR7.MAIN')]}
    R = {r['unit'].split(':', 1)[1].replace(':WF', ''): float(re.search(r'favoured\) ' + num, r['extra'][0]).group(1)) for r in T[('A', 'MR5.MAIN')]}
    return A, R

def null(N, K=7, draws=10):
    pm = [F(math.comb(K, k) * math.comb(N - K, K - k), math.comb(N, K)) for k in range(K + 1)]
    tot = [F(1)]
    for _ in range(draws):
        new = [F(0)] * (len(tot) + K)
        for i, x in enumerate(tot):
            for j, y in enumerate(pm): new[i + j] += x * y
        tot = new
    mean = float(sum(i * p for i, p in enumerate(tot))); var = float(sum(i * i * p for i, p in enumerate(tot))) - mean ** 2
    return tot, mean, var

def lean(name, values, mean0, var0):
    m = len(values); avg = sum(values) / m; s2 = st.variance(values)
    rho = max(0.0, 1 - s2 / var0)                      # equicorrelation estimate: E[s^2] = var0 (1 - rho)
    z_one = (avg - mean0) / math.sqrt(var0)            # as if all m were one and the same ticket
    z_ind = (avg - mean0) / math.sqrt(var0 / m)        # as if all m were independent
    z_rho = (avg - mean0) / math.sqrt(var0 * (1 + (m - 1) * rho) / m)
    print(f'  {name}: mean {avg:.3f} vs fair {mean0:.3f}; spread s^2 {s2:.2f} vs single-track variance {var0:.2f} -> overlap rho ~ {rho:.2f} (effective number ~ {m/(1+(m-1)*rho):.1f}); z if identical {z_one:+.2f}, with the estimated overlap {z_rho:+.2f}, if independent {z_ind:+.2f}')

res = {}
for path, game, N in ((sys.argv[1], 'OZLOTTO', 47), (sys.argv[2], 'POWERBALL', 35)):
    A, R = load(path); tot, mean0, var0 = null(N)
    print(game)
    top = [v for u, v in A.items() if ':TOP:' in u]; worst = [v for u, v in A.items() if ':WORST:' in u]
    lean('TOP main matches (40 tracks)', top, mean0, var0)
    lean('WORST main matches (40 tracks)', worst, mean0, var0)
    var = sorted({u.rsplit(':', 2)[0] for u in A})
    d = [A[v + ':TOP:WF'] - A[v + ':WORST:WF'] for v in var]
    cov = -7 * (7 / N) ** 2 * (N - 7) / (N - 1)        # per draw, two disjoint 7-number tickets
    vard = 10 * (2 * (var0 / 10) - 2 * cov)
    lean('TOP minus WORST (40 variants)', d, 0.0, vard)
    fair = (N + 1) / 2; var_r = ((N * N - 1) / 12) / 7 * (N - 7) / (N - 1) / 10
    lean('fair minus mean rank of the drawn numbers (40 variants; positive = favoured them)', [fair - R[v] for v in var], 0.0, var_r)
    # what the family test could detect
    thr = next(s for s in range(len(tot)) if float(sum(tot[s:])) <= 0.05 / 80)
    print(f'  family test: a track needs {thr} or more main matches in 10 draws (fair {mean0:.1f}) for Bonferroni P <= 0.05 over 80 tracks: {thr/10:.1f} per draw, {100*(thr/mean0-1):.0f}% above chance; the best observed was {max(A.values())}')
    res[game] = (A, R, var, fair)
# cross-game consistency
(A1, R1, var, f1), (A2, R2, _, f2) = res['OZLOTTO'], res['POWERBALL']
def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    a, b = rk(x), rk(y); ma, mb = sum(a) / len(a), sum(b) / len(b)
    return sum((p - ma) * (q - mb) for p, q in zip(a, b)) / math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b))
print('CROSS-GAME (40 variants, the same methods in both games)')
print(f'  Spearman correlation of the mean-rank advantage (Oz Lotto vs Powerball): {spearman([f1 - R1[v] for v in var], [f2 - R2[v] for v in var]):+.2f}')
print(f'  Spearman correlation of TOP minus WORST main matches: {spearman([A1[v+":TOP:WF"]-A1[v+":WORST:WF"] for v in var], [A2[v+":TOP:WF"]-A2[v+":WORST:WF"] for v in var]):+.2f}')
both = [v for v in var if R1[v] < f1 and R2[v] < f2]
print(f'  variants favouring the drawn numbers in both games (mean rank below fair in both): {len(both)} of 40 (Oz alone {sum(1 for v in var if R1[v]<f1)}, Powerball alone {sum(1 for v in var if R2[v]<f2)})')
fam = lambda v: v.split(':')[0]
print('  by method (number of variants; mean TOP-WORST Oz, Powerball; mean rank advantage Oz, Powerball):')
for m in sorted({fam(v) for v in var}, key=lambda s: int(s.split('_')[1])):
    vs = [v for v in var if fam(v) == m]
    print(f'    {m:5s} n={len(vs)}  T-W {sum(A1[v+":TOP:WF"]-A1[v+":WORST:WF"] for v in vs)/len(vs):+5.1f} {sum(A2[v+":TOP:WF"]-A2[v+":WORST:WF"] for v in vs)/len(vs):+5.1f}   rank adv {sum(f1-R1[v] for v in vs)/len(vs):+5.2f} {sum(f2-R2[v] for v in vs)/len(vs):+5.2f}')
v = 'E_4:POLY_LS_W104_D3_V1'
print(f'  {v}: Oz TOP {A1[v+":TOP:WF"]} WORST {A1[v+":WORST:WF"]} mean rank {R1[v]} (fair 24); Powerball TOP {A2[v+":TOP:WF"]} WORST {A2[v+":WORST:WF"]} mean rank {R2[v]} (fair 18)')
