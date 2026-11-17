"""OV-1 as an exact test martingale (design supplement v0.4, section 6). Invented fair draws only; no project data is read.

For frozen integer weights w (one per number), the fair-draw distribution of X = sum of w over a uniform K-subset is
computed EXACTLY by dynamic programming. For a fixed lambda, exp(lambda*Z) / E0[exp(lambda*Z)] has null mean exactly 1,
so the running product is a nonnegative martingale and P(it ever reaches 1/alpha) <= alpha (Ville's inequality), for any
weights fixed before each draw. The evidence score is the equal-weight mixture over LAMBDAS.
Usage: python3 -I ov1_eprocess_check.py"""
import math, random
from fractions import Fraction as F
K = 7
LAMBDAS = (-0.20, -0.10, -0.05, 0.05, 0.10, 0.20)
def pmf_x(w):
    """Exact pmf of the summed weight of a uniform K-subset: {x: probability as a Fraction}."""
    N = len(w); dp = [dict() for _ in range(K + 1)]; dp[0][0] = 1
    for wj in w:
        for k in range(K - 1, -1, -1):
            for s, c in dp[k].items():
                dp[k + 1][s + wj] = dp[k + 1].get(s + wj, 0) + c
    tot = math.comb(N, K); assert sum(dp[K].values()) == tot
    return {x: F(c, tot) for x, c in dp[K].items()}
def var_formula(w):
    N = len(w); m = F(sum(w), N)
    return F(K * (N - K), N - 1) * sum((x - m) ** 2 for x in w) / N
def tables(w):
    p = pmf_x(w); mean = sum(x * q for x, q in p.items()); var = sum((x - mean) ** 2 * q for x, q in p.items())
    assert mean == F(K * sum(w), len(w)) and var == var_formula(w)          # exact identities
    sd = math.sqrt(var); xs = sorted(p); pr = [float(p[x]) for x in xs]; zs = [(x - float(mean)) / sd for x in xs]
    fac = []
    for lam in LAMBDAS:
        m = sum(q * math.exp(lam * z) for q, z in zip(pr, zs)); fac.append([math.exp(lam * z) / m for z in zs])
    return xs, pr, zs, fac, float(var)
# 1. the reviewer's counterexample (EX_208 R-3): 40 variants, identical TOP seven and WORST seven, Powerball N = 35
w = [40] * 7 + [-40] * 7 + [0] * 21
xs, pr, zs, fac, var = tables(w)
print(f'1. identical tickets, N=35: Var(D) = {var / 1600:.16f} (EX_208: 2.3058823529411767)')
conv = {0: 1.0}
for _ in range(104):
    new = {}
    for s, a in conv.items():
        for x, q in zip(xs, pr): new[s + x] = new.get(s + x, 0.0) + a * q
    conv = new
cut = 2.5758293 * math.sqrt(104 * var)
print(f'   P(|S_104| >= 2.5758293) = {sum(a for s, a in conv.items() if abs(s) >= cut):.13f} (EX_208: 0.0107176149616)')
# 2. each mixture component has null mean exactly 1 for these and for random overlapping weights
rng = random.Random(20261117)
def random_weights(N, variants=40, clusters=5):
    w = [0] * N; bases = [rng.sample(range(N), N) for _ in range(clusters)]
    for v in range(variants):
        r = bases[v % clusters][:]
        for _ in range(3):
            a, b = rng.randrange(N), rng.randrange(N); r[a], r[b] = r[b], r[a]
        for j in r[:7]: w[j] += 1
        for j in r[-7:]: w[j] -= 1
    return w
worst = 0.0
for ww in [w] + [random_weights(N) for N in (35, 47) for _ in range(3)]:
    _, pr2, _, fac2, _ = tables(ww)
    worst = max(worst, max(abs(sum(q * f for q, f in zip(pr2, fl)) - 1.0) for fl in fac2))
print(f'2. largest |null mean of a component - 1| over 7 weight patterns: {worst:.2e}')
# 3. Ville in practice: under fair draws, how often does the evidence score EVER reach 20 or 40 within 1040 draws?
def run(xs, pr, fac, n, tilt=0.0):
    probs = pr if tilt == 0.0 else None
    if tilt:
        t = [q * math.exp(tilt * z) for q, z in zip(pr, zs_cur)]; s = sum(t); probs = [a / s for a in t]
    logs = [0.0] * len(LAMBDAS); best = 0.0; first20 = first40 = None
    idx = rng.choices(range(len(xs)), weights=probs, k=n)
    for i, k in enumerate(idx, 1):
        for a in range(len(LAMBDAS)): logs[a] += math.log(fac[a][k])
        e = sum(math.exp(l) for l in logs) / len(LAMBDAS)
        if first20 is None and e >= 20: first20 = i
        if first40 is None and e >= 40: first40 = i; break
    return first20, first40
for name, ww in (('identical tickets N=35', w), ('overlapping tickets N=35', random_weights(35)), ('overlapping tickets N=47', random_weights(47))):
    xs, pr, zs_cur, fac, var = tables(ww); R = 20000
    res = [run(xs, pr, fac, 1040) for _ in range(R)]
    print(f'3. fair draws, {name}: ever >= 20 within 1040 draws: {sum(1 for a, b in res if a) / R:.4f} (bound 0.05);'
          f' ever >= 40: {sum(1 for a, b in res if b) / R:.4f} (bound 0.025)')
# 4. how long to a result when the draws lean (the pmf of X exponentially tilted so that the mean of Z is about delta)
xs, pr, zs_cur, fac, var = tables(random_weights(35))
for delta in (0.11, 0.22, 0.35):
    out = []
    for thr_i, thr in ((0, 20), (1, 40)):
        t = sorted((run(xs, pr, fac, 4000, tilt=delta)[thr_i] or 10 ** 9) for _ in range(1500))
        out.append(f'score {thr}: median {t[len(t) // 2]}, 80% by {t[int(0.8 * len(t))]}')
    print(f'4. mean Z about {delta:.2f} per draw: draws needed, ' + '; '.join(out))
