"""Exact reference formulas for wave 2 (E_2, E_17, E_19, E_18) and the shared gaps helper (Claude, 30 Oct 2026).

Design note: Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1.md. Pure arithmetic in fractions on
invented draws. Never reads a data file. A history is a list of draws, oldest first; each draw is the list of
labels drawn from the barrel low..high (K per draw). W = len(history); the target is position W + 1.
"""
from fractions import Fraction as Fr

BIN_FACTORS = (Fr(1, 5), Fr(2, 5), Fr(3, 5), Fr(1), Fr(8, 5), Fr(13, 5))


def ceil_fr(x):
    return -((-x.numerator) // x.denominator)


# ---------------------------------------------------------------- the shared helper (recurrence_gaps)
def appearances(hist, low, high):
    """label -> ascending positions 1..W at which it was drawn."""
    app = {j: [] for j in range(low, high + 1)}
    for i, d in enumerate(hist, 1):
        if len(set(d)) != len(d) or any(not low <= x <= high for x in d):
            raise ValueError('bad draw')
        for x in d:
            app[x].append(i)
    return app


def completed_gaps(app):
    return {j: [b - a for a, b in zip(p, p[1:])] for j, p in app.items()}


def projected_age(W, app):
    """Age at the target: W + 1 - last appearance; a never-seen label counts as last seen at position 0."""
    return {j: W + 1 - (p[-1] if p else 0) for j, p in app.items()}


def exposures_by_age(hist, low, high, window=None):
    """Pooled at-risk counts R[k] and event counts E[k] by age k, over the eligible draws (only the newest
    `window` draws if given). A label is at risk from the draw after its first appearance; age at draw i is
    i - (its last appearance before i). Exposures before a label's first appearance (unknown age) are excluded."""
    W = len(hist)
    start = 1 if window is None else W - window + 1
    R, E = {}, {}
    last = {j: None for j in range(low, high + 1)}
    for i, d in enumerate(hist, 1):
        s = set(d)
        for j in last:
            if last[j] is not None and i >= start:
                k = i - last[j]
                R[k] = R.get(k, 0) + 1
                if j in s:
                    E[k] = E.get(k, 0) + 1
        for j in s:
            last[j] = i
    return R, E


def exposures_from_gaps(hist, low, high, window=None):
    """Second route: each completed gap g ending at position e contributes ages 1..g, event at g; the open
    stretch after the last appearance contributes ages 1..W-last without an event."""
    W = len(hist)
    start = 1 if window is None else W - window + 1
    app = appearances(hist, low, high)
    R, E = {}, {}
    for j, p in app.items():
        for a, b in zip(p, p[1:]):
            for k in range(1, b - a + 1):
                if a + k >= start:
                    R[k] = R.get(k, 0) + 1
            if b >= start:
                E[b - a] = E.get(b - a, 0) + 1
        if p:
            for k in range(1, W - p[-1] + 1):
                if p[-1] + k >= start:
                    R[k] = R.get(k, 0) + 1
    return R, E


def bin_edges(L, K):
    """Upper edges of the age bins: the distinct values ceil(f L/K), f = 1/5, 2/5, 3/5, 1, 8/5, 13/5."""
    m = Fr(L, K)
    out = []
    for f in BIN_FACTORS:
        e = ceil_fr(f * m)
        if not out or e > out[-1]:
            out.append(e)
    return out


def bin_of(k, edges):
    return sum(1 for e in edges if k > e)


def bin_ranges(edges):
    lo = [1] + [e + 1 for e in edges]
    hi = list(edges) + [None]
    return list(zip(lo, hi))


def harmonic(k):
    return sum((Fr(1, i) for i in range(1, k + 1)), Fr(0))


# ---------------------------------------------------------------- E_2
def median(xs):
    s = sorted(xs)
    n = len(s)
    return Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)


def e2(hist, low, high, K, stat, last_n=None):
    L = high - low + 1
    W = len(hist)
    app = appearances(hist, low, high)
    gaps, G = completed_gaps(app), projected_age(W, app)
    out = {}
    for j in app:
        g = gaps[j][-last_n:] if last_n else gaps[j]
        if not g:
            c = Fr(L, K)                                       # fallback: the fair mean gap
        elif stat == 'mean':
            c = Fr(sum(g), len(g))
        else:
            c = median(g)
        out[j] = -abs(G[j] - c) / c
    return out


# ---------------------------------------------------------------- E_17
def binned_hazard(hist, low, high, K, c, window=None):
    L = high - low + 1
    r = Fr(K, L)
    edges = bin_edges(L, K)
    R, E = exposures_by_age(hist, low, high, window)
    nb = len(edges) + 1
    Rb, Eb = [0] * nb, [0] * nb
    for k, n in R.items():
        Rb[bin_of(k, edges)] += n
    for k, n in E.items():
        Eb[bin_of(k, edges)] += n
    return [(Eb[b] + c * r) / (Rb[b] + c) for b in range(nb)], edges


def e17_bins(hist, low, high, K, c, window=None):
    h, edges = binned_hazard(hist, low, high, K, c, window)
    G = projected_age(len(hist), appearances(hist, low, high))
    return {j: h[bin_of(g, edges)] for j, g in G.items()}


def e17_logslope(hist, low, high, K):
    R, E = exposures_by_age(hist, low, high)
    H = {k: harmonic(k) for k in R}
    n = sum(R.values())
    sz = sum(R[k] * H[k] for k in R)
    sy = sum(E.values())
    szy = sum(E[k] * H[k] for k in E)
    szz = sum(R[k] * H[k] ** 2 for k in R)
    sxy = szy - sz * sy / n
    sxx = szz - sz * sz / n
    beta = sxy / sxx if sxx else Fr(0)
    zbar, ybar = sz / n, Fr(sy, n)
    G = projected_age(len(hist), appearances(hist, low, high))
    return {j: ybar + beta * (harmonic(g) - zbar) for j, g in G.items()}, beta


# ---------------------------------------------------------------- E_19
def e19(hist, low, high, K, T, c=100, d=20):
    """Trend (E_17's binned hazard, same c) times a per-label periodic factor in age mod T, with the label's
    own overall level divided out. Pooled residue ratios phi; per-label ratios shrunk towards them by d."""
    h, edges = binned_hazard(hist, low, high, K, c)
    last = {j: None for j in range(low, high + 1)}
    O = {j: [0] * T for j in last}
    X = {j: [Fr(0)] * T for j in last}
    for i, dr in enumerate(hist, 1):
        s = set(dr)
        for j in last:
            if last[j] is not None:
                k = i - last[j]
                X[j][k % T] += h[bin_of(k, edges)]
                if j in s:
                    O[j][k % T] += 1
        for j in s:
            last[j] = i
    Op = [sum(O[j][q] for j in O) for q in range(T)]
    Xp = [sum(X[j][q] for j in X) for q in range(T)]
    phi = [(Op[q] + d) / (Xp[q] + d) for q in range(T)]
    psi = {}
    for j in O:
        level = (sum(O[j]) + d) / (sum(X[j]) + d)
        psi[j] = [(O[j][q] + d * phi[q]) / (X[j][q] + d) / level for q in range(T)]
    G = projected_age(len(hist), appearances(hist, low, high))
    return {j: h[bin_of(g, edges)] * psi[j][g % T] for j, g in G.items()}, phi, psi


# ---------------------------------------------------------------- E_18
def surv_geom(p, G):
    return (1 - p) ** (G - 1)


def surv_nb2(p, G):
    return Fr(1) if G <= 1 else (1 - p) ** (G - 1) + (G - 1) * p * (1 - p) ** (G - 2)


def components(L, K):
    """The fixed component library, in this order: FAST, FAIR, SLOW, REGULAR (survival functions S(G) = P(gap >= G))."""
    r = Fr(K, L)
    return (lambda G: surv_geom(2 * r, G),               # FAST: geometric, mean L/(2K): rapid returns
            lambda G: surv_geom(r, G),                   # FAIR: geometric, mean L/K: the fair law
            lambda G: surv_geom(r / 2, G),               # SLOW: geometric, mean 2L/K: long absences
            lambda G: surv_nb2(2 * r, G))                # REGULAR: negative binomial, shape 2, mean L/K: even returns


def bin_probs(S, edges):
    return [S(lo) - (S(hi + 1) if hi is not None else 0) for lo, hi in bin_ranges(edges)]


def solve(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]


def fit_weights(q, P, Pf):
    """Minimise sum_b (q_b - sum_c w_c P[c][b])^2 / Pf[b] over the simplex, exactly, by trying every support."""
    C = len(P)
    best = None
    for mask in range(1, 2 ** C):
        S = [c for c in range(C) if mask >> c & 1]
        n = len(S)
        A = [[sum(P[a][b] * P[cc][b] / Pf[b] for b in range(len(q))) for cc in S] + [Fr(1)] for a in S]
        A.append([Fr(1)] * n + [Fr(0)])
        rhs = [sum(P[a][b] * q[b] / Pf[b] for b in range(len(q))) for a in S] + [Fr(1)]
        sol = solve(A, rhs)
        if sol is None or any(x < 0 for x in sol[:n]):
            continue
        w = [Fr(0)] * C
        for c, x in zip(S, sol[:n]):
            w[c] = x
        F = sum((q[b] - sum(w[c] * P[c][b] for c in range(C))) ** 2 / Pf[b] for b in range(len(q)))
        if best is None or F < best[0]:
            best = (F, w)
    return best[1]


def gaps_in_window(app, W, window):
    """Completed gaps with both appearances inside the newest `window` draws (all gaps if window is None)."""
    lo = 0 if window is None else W - window
    return {j: [b - a for a, b in zip(p, p[1:]) if a > lo] for j, p in app.items()}


def e18(hist, low, high, K, c, window=None):
    L = high - low + 1
    W = len(hist)
    edges = bin_edges(L, K)
    comps = components(L, K)
    P = [bin_probs(S, edges) for S in comps]
    Pf = P[1]
    app = appearances(hist, low, high)
    gaps, G = gaps_in_window(app, W, window), projected_age(W, app)
    out, weights = {}, {}
    for j in app:
        g = gaps[j]
        o = [0] * len(Pf)
        for x in g:
            o[bin_of(x, edges)] += 1
        q = [(o[b] + c * Pf[b]) / (len(g) + c) for b in range(len(Pf))]
        w = fit_weights(q, P, Pf)
        Gj = G[j]
        num = sum(w[i] * (comps[i](Gj) - comps[i](Gj + 1)) for i in range(len(comps)))
        den = sum(w[i] * comps[i](Gj) for i in range(len(comps)))
        out[j], weights[j] = num / den, w
    return out, weights


# ---------------------------------------------------------------- worked examples
EXAMPLE = [[1, 2], [3, 4], [1, 5], [2, 6], [1, 7], [3, 8], [1, 9], [2, 10], [4, 5], [1, 6], [3, 7], [1, 8]]


def fmt(d):
    return ', '.join(f'{j}: {v}' for j, v in sorted(d.items()))


if __name__ == '__main__':
    H, low, high, K = EXAMPLE, 1, 10, 2
    print('example: 10 labels, K = 2 (r = 1/5, mean gap 5), 12 draws oldest first:', H)
    app = appearances(H, low, high)
    print('bin edges', bin_edges(10, 2), '; Powerball MAIN', bin_edges(35, 7), 'POWERBALL', bin_edges(20, 1),
          'Oz MAIN', bin_edges(47, 7))
    print('gaps', completed_gaps(app))
    print('projected ages', projected_age(len(H), app))
    R, E = exposures_by_age(H, low, high)
    assert (R, E) == exposures_from_gaps(H, low, high)
    print('R', dict(sorted(R.items())), 'E', dict(sorted(E.items())))
    print('E_2 mean   :', fmt(e2(H, low, high, K, 'mean')))
    print('E_2 median :', fmt(e2(H, low, high, K, 'median')))
    print('E_2 last 2 :', fmt(e2(H, low, high, K, 'mean', 2)))
    h, _ = binned_hazard(H, low, high, K, 10)
    print('E_17 bins c=10 hazards by bin', [str(x) for x in h])
    print('E_17 bins c=10 :', fmt(e17_bins(H, low, high, K, 10)))
    s, beta = e17_logslope(H, low, high, K)
    print('E_17 logslope beta', beta, float(beta), ':', fmt({j: float(v) for j, v in s.items()}))
    s, phi, psi = e19(H, low, high, K, 2, c=10, d=2)
    print('E_19 T=2 c=10 d=2 pooled phi', [str(x) for x in phi], 'psi label 1', [str(x) for x in psi[1]], ':', fmt(s))
    s, w = e18(H, low, high, K, 2)
    print('E_18 c=2 weights', {j: [str(x) for x in v] for j, v in w.items()})
    print('E_18 c=2 :', fmt(s))
    print('E_18 c=2 weights (4 dp):', {j: [round(float(x), 4) for x in v] for j, v in w.items()})
    print('E_18 c=2 scores (4 dp):', {j: round(float(v), 4) for j, v in s.items()})
    s19, _, psi = e19(H, low, high, K, 2, c=10, d=2)
    print('E_19 scores (4 dp):', {j: round(float(v), 4) for j, v in s19.items()},
          'psi (4 dp)', {j: [round(float(x), 4) for x in v] for j, v in psi.items()})
    # the values quoted in the design note
    assert e2(H, low, high, K, 'mean') == {1: Fr(-6, 11), 2: Fr(-3, 7), 3: Fr(-5, 9), 4: Fr(-3, 7), 5: Fr(-1, 3),
                                          6: Fr(-1, 2), 7: Fr(-2, 3), 8: Fr(-5, 6), 9: Fr(-1, 5), 10: Fr(0)}
    assert e2(H, low, high, K, 'median')[1] == Fr(-1, 2) and e2(H, low, high, K, 'mean', 2)[1] == Fr(-3, 5)
    assert binned_hazard(H, low, high, K, 10)[0] == [Fr(1, 16), Fr(1, 5), Fr(4, 25), Fr(5, 28), Fr(7, 16), Fr(1, 5),
                                                     Fr(1, 5)]
    assert e17_logslope(H, low, high, K)[1] == Fr(362495, 1270704)
    assert e19(H, low, high, K, 2, c=10, d=2)[1] == [Fr(448, 379), Fr(160, 199)]
    assert w[1] == [Fr(3245348069700918737, 4925190825817479938), Fr(0, 1), Fr(0, 1), Fr(1679842756116561201, 4925190825817479938)]
    assert w[9] == [0, 1, 0, 0] and s[9] == Fr(1, 5)
    assert bin_edges(35, 7) == [1, 2, 3, 5, 8, 13] and bin_edges(20, 1) == [4, 8, 12, 20, 32, 52]
    assert bin_edges(47, 7) == [2, 3, 5, 7, 11, 18]
    for G in range(1, 40):                                # survival closed forms against summation
        for S, pmf in ((lambda G: surv_geom(Fr(1, 5), G), lambda g: Fr(1, 5) * Fr(4, 5) ** (g - 1)),
                       (lambda G: surv_nb2(Fr(1, 5), G), lambda g: (g - 1) * Fr(1, 25) * Fr(4, 5) ** (g - 2))):
            assert S(G) == 1 - sum((pmf(g) for g in range(1, G)), Fr(0))
    print('ALL EXAMPLE ASSERTIONS PASS')
