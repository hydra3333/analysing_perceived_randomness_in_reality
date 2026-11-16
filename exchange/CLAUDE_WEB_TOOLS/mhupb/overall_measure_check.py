"""Null calibration and power of the proposed overall measure (design supplement v0.2, section 5). Invented draws only:
every draw here is simulated; no project data is read.

Per draw d: w_j = (number of variants with number j in their TOP seven) - (number with j in their WORST seven);
X_d = sum of w_j over the drawn numbers; under fair draws E[X_d] = 0 and Var[X_d] = K(N-K)/(N-1) * popvar(w), exactly,
given the tickets. Z_d = X_d / sqrt(Var). S_n = sum(Z_d) / sqrt(n).  Usage: python3 -I overall_measure_check.py"""
import math, random, statistics
K = 7
def var_x(w, N):
    m = sum(w) / N
    return K * (N - K) / (N - 1) * sum((x - m) ** 2 for x in w) / N
def z_of(w, drawn, N):
    v = var_x(w, N)
    return None if v == 0 else sum(w[j] for j in drawn) / math.sqrt(v)
def weights_fixed(N, rng, variants=40, clusters=5):
    """Overlapping tickets: variants in a cluster share a base ranking, lightly perturbed."""
    w = [0] * N
    bases = [rng.sample(range(N), N) for _ in range(clusters)]
    for v in range(variants):
        r = bases[v % clusters][:]
        for _ in range(3):
            a, b = rng.randrange(N), rng.randrange(N); r[a], r[b] = r[b], r[a]
        for j in r[:7]: w[j] += 1
        for j in r[-7:]: w[j] -= 1
    return w
def weights_adaptive(N, hist, rng, windows=(8, 13, 26, 52, 104, 9999)):
    """Adaptive methods: each ranks numbers by frequency in its own trailing window of the simulated past (ties random);
    half the methods favour frequent numbers, half favour overdue ones."""
    w = [0] * N
    for i, W in enumerate(windows):
        cnt = [0] * N
        for d in hist[-W:]:
            for j in d: cnt[j] += 1
        order = sorted(range(N), key=lambda j: (cnt[j], rng.random()), reverse=(i % 2 == 0))
        for j in order[:7]: w[j] += 1
        for j in order[-7:]: w[j] -= 1
    return w
def draw(N, rng, w=None, edge=0.0):
    """A fair draw, or (edge > 0) a draw in which a number's chance is tilted by edge * w_j / max|w| (sequential sampling)."""
    if edge == 0.0 or w is None: return rng.sample(range(N), K)
    mx = max(1, max(abs(x) for x in w)); p = [1.0 + edge * x / mx for x in w]; out = []
    for _ in range(K):
        t = rng.random() * sum(p); a = 0.0
        for j in range(N):
            a += p[j]
            if t <= a: break
        out.append(j); p[j] = 0.0
    return out
def run(N, n, reps, adaptive, edge, seed):
    rng = random.Random(seed); S = []
    for _ in range(reps):
        hist = [rng.sample(range(N), K) for _ in range(120)] if adaptive else None
        wf = None if adaptive else weights_fixed(N, rng)
        tot = 0.0; used = 0
        for _ in range(n):
            w = weights_adaptive(N, hist, rng) if adaptive else wf
            d = draw(N, rng, w, edge)
            z = z_of(w, d, N)
            if z is not None: tot += z; used += 1
            if adaptive: hist.append(d)
        S.append(tot / math.sqrt(used))
    return S
def tail(S, z): return sum(1 for s in S if s >= z) / len(S)
Z5, Z1 = 1.6449, 2.5758   # one-sided 5% and 0.5%
print('NULL (fair draws): share of runs with S >= z; the target is 0.050 and 0.005')
for N, game in ((35, 'POWERBALL-like'), (47, 'OZLOTTO-like')):
    for adaptive in (False, True):
        for n in (52, 208):
            S = run(N, n, 4000 if adaptive else 20000, adaptive, 0.0, 12345 + N + n + adaptive)
            print(f'  {game:15s} {"adaptive" if adaptive else "fixed   "} n={n:3d}: mean {statistics.mean(S):+.3f} sd {statistics.pstdev(S):.3f}'
                  f'  P(S>=1.645) {tail(S, Z5):.4f}  P(S>=2.576) {tail(S, Z1):.4f}')
print('POWER (tilted draws, fixed tickets; edge = relative tilt for the most favoured number): share with S >= 2.576')
for N, game in ((35, 'POWERBALL-like'), (47, 'OZLOTTO-like')):
    for edge in (0.10, 0.20):
        for n in (104, 416):
            S = run(N, n, 3000, False, edge, 999 + N + n)
            print(f'  {game:15s} edge {edge:.2f} n={n:3d}: mean S {statistics.mean(S):+.2f}  passes {tail(S, Z1):.3f}')
