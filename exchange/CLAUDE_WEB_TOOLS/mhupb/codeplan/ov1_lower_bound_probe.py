"""OV-1 numerical-contract PROBE for the MHUP-B code plan (plan stage; NOT project code; invented data only).

It shows that the numerical contract of the ratified design supplement v0.7 section 6.5 (EX_209 B02, EX_211 F02) can be
met with integer arithmetic alone, and measures what it costs. Nothing here reads a master, a result or any project
record. Usage: python3 -I ov1_lower_bound_probe.py [--brute]   (--brute adds the full-size brute-force oracles)

The kernel (what the code plan proposes for src/evaluation/ov1_numeric.py):
  * every real number is an integer n meaning n / S, S = 10**D (fixed point; D = 50);
  * every operation rounds DOWN for a lower bound and UP for an upper bound (Python's // on ints is an exact floor);
  * exp and log are enclosed by Taylor series with an explicit remainder term, on reduced arguments;
  * sums of stored log-factors are exact integer sums: no rounding accumulates over draws.
The stored log-factor of a draw is  l_stored = (lower end of the enclosure of the true log-factor) - MARGIN.
Two guarantees are then CHECKED, not assumed:
  (G1) pointwise: l_stored <= true log-factor (by construction; cross-checked against decimal at 90 digits);
  (G2) certificate: sum over the exact fair-draw distribution of exp_upper(l_stored(x)) <= 1, in exact integers, for
       every component. So the stored process is itself a nonnegative supermartingale under fair draws, and Ville's
       inequality applies to what the software actually stores, whatever the route by which l was computed.
"""
import itertools, math, random, sys, time
from decimal import Decimal, getcontext, ROUND_FLOOR
from fractions import Fraction as F

D = 50
S = 10 ** D
MARGIN = 10 ** (D - 30)                      # 1e-30 in fixed point: the registered safety margin
K = 7
LAMBDAS = (F(-1, 5), F(-1, 10), F(-1, 20), F(1, 20), F(1, 10), F(1, 5))     # exact rationals


class Refuse(Exception):
    pass


# ------------------------------------------------------------------ directed fixed-point arithmetic
def fdiv(a, b):
    return a // b                              # floor (b > 0)


def cdiv(a, b):
    return -((-a) // b)                        # ceiling (b > 0)


def mul_lo(a, b):
    return fdiv(a * b, S)


def mul_hi(a, b):
    return cdiv(a * b, S)


def _exp_small(a, n=60):
    """Enclosure (lo, hi) of exp(a / S) for 0 <= a <= S (argument in [0, 1]); Taylor with remainder.
    Remainder after n terms: t_n * 1/(1 - u/(n+1)) <= 2 * t_n for u <= 1."""
    assert 0 <= a <= S
    lo = hi = S
    tl = tu = S
    for k in range(1, n):
        tl = fdiv(tl * a, S * k)
        tu = cdiv(tu * a, S * k)
        lo += tl
        hi += tu
    tu = cdiv(tu * a, S * n)                  # the first omitted term, rounded up (at least 1 when a > 0)
    return lo, hi + 2 * tu + 1


def exp_enc(a):
    """Enclosure (lo, hi) of exp(a / S) for any integer a. Halving reduction, then squaring with directed rounding."""
    if a < 0:
        lo, hi = exp_enc(-a)
        return fdiv(S * S, hi), cdiv(S * S, lo)
    j = 0
    while (a >> j) > S:
        j += 1
    r_lo, r_hi = a >> j, -((-a) >> j)          # floor and ceiling of a / 2**j
    lo = _exp_small(r_lo)[0]
    hi = _exp_small(min(r_hi, S))[1] if r_hi <= S else _exp_small(S)[1]
    for _ in range(j):
        lo, hi = mul_lo(lo, lo), mul_hi(hi, hi)
    return lo, hi


def log_enc(m_lo, m_hi, n=400):
    """Enclosure of log(m) for S <= m_lo <= m_hi (m >= 1), by log m = 2 atanh((m-1)/(m+1)).
    Remainder after n terms: 2 y^(2n+1) / ((2n+1)(1 - y^2)); y <= 0.7 is required (refused otherwise)."""
    if m_lo < S:
        raise Refuse('log argument below 1')
    out = []
    for m, up in ((m_lo, False), (m_hi, True)):
        y = cdiv((m - S) * S, m + S) if up else fdiv((m - S) * S, m + S)
        if y * 10 > 7 * S:
            raise Refuse('log argument too large for the series (y > 0.7)')
        y2 = mul_hi(y, y) if up else mul_lo(y, y)
        term, total = y, 0
        for k in range(n):
            total += cdiv(term, 2 * k + 1) if up else fdiv(term, 2 * k + 1)
            term = mul_hi(term, y2) if up else mul_lo(term, y2)
            if term == 0:
                break
        if up:                                  # remainder, rounded up: term / ((2n+1)(1 - y2)) <= term * S / (S - y2)
            total += cdiv(term * S, S - y2) + 1
        out.append(2 * total)
    return out[0], out[1]


def sqrt_enc(p, q):
    """Enclosure of sqrt(p / q), p, q positive integers."""
    lo = math.isqrt(fdiv(p * S * S, q))
    hi = math.isqrt(cdiv(p * S * S, q)) + 1
    return lo, hi


# ------------------------------------------------------------------ the exact fair-draw distribution
def pmf_dp(w):
    """Counts {x: number of K-subsets with summed weight x}; integers only (route 1: one number at a time)."""
    dp = [dict() for _ in range(K + 1)]
    dp[0][0] = 1
    for wj in w:
        for k in range(K - 1, -1, -1):
            for s, c in dp[k].items():
                dp[k + 1][s + wj] = dp[k + 1].get(s + wj, 0) + c
    return dp[K]


def pmf_groups(w):
    """Route 2 (independent algorithm): group equal weights; a group of m numbers of weight v contributes
    C(m, j) ways to take j of them. Convolve the groups."""
    groups = {}
    for wj in w:
        groups[wj] = groups.get(wj, 0) + 1
    cur = {(0, 0): 1}
    for v, m in sorted(groups.items()):
        new = {}
        for (k, s), c in cur.items():
            for j in range(0, min(m, K - k) + 1):
                key = (k + j, s + j * v)
                new[key] = new.get(key, 0) + c * math.comb(m, j)
        cur = new
    return {s: c for (k, s), c in cur.items() if k == K}


def pmf_brute(w):
    out = {}
    for comb in itertools.combinations(w, K):
        x = sum(comb)
        out[x] = out.get(x, 0) + 1
    return out


def variance(w):
    n = len(w)
    assert sum(w) == 0
    return F(K * (n - K), n - 1) * F(sum(x * x for x in w), n)


# ------------------------------------------------------------------ one draw's certified factor table
def factor_table(w):
    """For frozen weights w: {lambda: {x: l_stored}} with the certificate checked, plus diagnostics.
    Returns None for V = 0 (the registered skip)."""
    n = len(w)
    counts = pmf_dp(w)
    total = math.comb(n, K)
    assert sum(counts.values()) == total and sum(x * c for x, c in counts.items()) == 0
    v = variance(w)
    if v == 0:
        return None
    assert sum(x * x * c for x, c in counts.items()) * v.denominator == v.numerator * total      # exact variance identity
    s_lo, s_hi = sqrt_enc(v.numerator, v.denominator)
    table, width, cert_slack = {}, 0, None
    for lam in LAMBDAS:
        num, den = abs(lam.numerator), lam.denominator
        # |theta| = |lambda| / sqrt(V): enclosure
        t_lo, t_hi = fdiv(num * S * S, den * s_hi), cdiv(num * S * S, den * s_lo)
        sign = 1 if lam > 0 else -1
        u = {}                                   # x -> enclosure of theta * x (fixed point)
        for x in counts:
            y = sign * x                          # theta * x = |theta| * (sign * x)
            u[x] = (t_lo * y, t_hi * y) if y >= 0 else (t_hi * y, t_lo * y)
        m_lo = m_hi = 0
        for x, c in counts.items():
            e_lo = exp_enc(u[x][0])[0]
            e_hi = exp_enc(u[x][1])[1]
            m_lo += c * e_lo
            m_hi += c * e_hi
        m_lo, m_hi = fdiv(m_lo, total), cdiv(m_hi, total)
        lg_lo, lg_hi = log_enc(max(m_lo, S), m_hi)          # E0 exp(.) >= 1 by Jensen (mean of X is 0)
        row = {}
        for x in counts:
            lo, hi = u[x][0] - lg_hi, u[x][1] - lg_lo
            width = max(width, hi - lo)
            row[x] = lo - MARGIN
        # (G2) the certificate, exact integers: sum_x count(x) * exp_upper(l_stored(x)) <= C(n, K) * S
        acc = sum(c * exp_enc(row[x])[1] for x, c in counts.items())
        if acc > total * S:
            raise Refuse('certificate failed: the stored factors do not have fair-draw mean <= 1')
        slack = total * S - acc
        cert_slack = slack if cert_slack is None else min(cert_slack, slack)
        table[lam] = row
    if width >= MARGIN:
        raise Refuse('enclosure wider than the registered margin')
    return {'table': table, 'counts': counts, 'total': total, 'var': v, 'width': width, 'cert_slack': cert_slack}


def crossing(logs, bar=40):
    """logs: the six exact running sums of stored log-factors. True only if the PROVED lower bound of the mixture
    is at least the bar: sum_lambda exp_lower(L_lambda) >= 6 * bar, compared as exact integers."""
    return sum(exp_enc(L)[0] for L in logs) >= len(logs) * bar * S


def mixture_lower(logs):
    return fdiv(sum(exp_enc(L)[0] for L in logs), len(logs))


# ------------------------------------------------------------------ reference (decimal, 90 digits; cross-check only)
def reference_log_factor(w, lam, x):
    getcontext().prec = 90
    counts = pmf_dp(w)
    total = math.comb(len(w), K)
    v = variance(w)
    sd = (Decimal(v.numerator) / Decimal(v.denominator)).sqrt()
    th = Decimal(lam.numerator) / Decimal(lam.denominator) / sd
    m = sum(Decimal(c) * (th * x).exp() for x, c in counts.items()) / Decimal(total)
    return th * x - m.ln()


def to_dec(a):
    getcontext().prec = 90
    return Decimal(a) / Decimal(S)


# ------------------------------------------------------------------ weight patterns (invented)
def tickets_to_weights(n, tickets):
    w = [0] * n
    for top, worst in tickets:
        for j in top:
            w[j] += 1
        for j in worst:
            w[j] -= 1
    return w


def random_weights(rng, n, variants, clusters=5, swaps=3):
    bases = [rng.sample(range(n), n) for _ in range(clusters)]
    tickets = []
    for i in range(variants):
        r = bases[i % clusters][:]
        for _ in range(swaps):
            a, b = rng.randrange(n), rng.randrange(n)
            r[a], r[b] = r[b], r[a]
        tickets.append((r[:7], r[-7:]))
    return tickets_to_weights(n, tickets)


def main():
    rng = random.Random(20261117)
    brute = '--brute' in sys.argv
    print(f'fixed point: D = {D} digits; MARGIN = 1e-30; Python {sys.version.split()[0]}')

    # 0. the kernel against known constants and decimal
    getcontext().prec = 90
    e_lo, e_hi = exp_enc(S)
    assert to_dec(e_lo) <= Decimal(1).exp() <= to_dec(e_hi) and e_hi - e_lo < 10 ** 6
    l_lo, l_hi = log_enc(2 * S, 2 * S)
    assert to_dec(l_lo) <= Decimal(2).ln() <= to_dec(l_hi) and l_hi - l_lo < 10 ** 6
    worst = 0
    for _ in range(2000):
        a = rng.randrange(-60 * S, 60 * S)
        lo, hi = exp_enc(a)
        ref = to_dec(a).exp()
        assert to_dec(lo) <= ref <= to_dec(hi), a
        if lo > 0:
            worst = max(worst, float((to_dec(hi) - to_dec(lo)) / ref))
    for _ in range(2000):
        m = S + rng.randrange(0, 4 * S)
        lo, hi = log_enc(m, m)
        assert to_dec(lo) <= to_dec(m).ln() <= to_dec(hi), m
    print(f'0. exp and log enclosures contain the 90-digit decimal value in 4,002 random and fixed cases; '
          f'largest relative exp width {worst:.1e}')

    # 1. the exact distribution: two independent routes, and brute force
    small = [3, -1, 0, 2, -2, -2, 1, 0, -1, 0, 4, -4, 0]        # N = 13, sums to 0
    assert pmf_dp(small) == pmf_groups(small) == pmf_brute(small)
    cases = [('reviewer counterexample N=35', [40] * 7 + [-40] * 7 + [0] * 21),
             ('one variant N=35', [1] * 7 + [-1] * 7 + [0] * 21),
             ('one variant N=47', [1] * 7 + [-1] * 7 + [0] * 33),
             ('skewed N=47: 300 share TOP, WORST spread', tickets_to_weights(47, [(list(range(7)), [7 + (i * 7 + j) % 40 for j in range(7)]) for i in range(300)])),
             ('40 overlapping N=35', random_weights(rng, 35, 40)),
             ('40 overlapping N=47', random_weights(rng, 47, 40)),
             ('400 overlapping N=35', random_weights(rng, 35, 400, clusters=9)),
             ('2000 near-identical N=47', random_weights(rng, 47, 2000, clusters=1, swaps=1))]
    for name, w in cases:
        assert sum(w) == 0 and pmf_dp(w) == pmf_groups(w), name
    print(f'1. exact distribution: route 1 (one number at a time) equals route 2 (grouped binomials) on {len(cases)} '
          f'full-size patterns, and both equal brute force on N=13')
    if brute:
        for name, w in (cases[0], cases[4], cases[2]):
            t = time.time()
            assert pmf_brute(w) == pmf_dp(w), name
            print(f'   brute force over all C({len(w)},7) = {math.comb(len(w), 7):,} subsets equals the DP: {name} '
                  f'({time.time() - t:.0f} s)')

    # 2. per-draw tables: certificate, pointwise bound against decimal, loss
    max_loss = 0
    for name, w in cases:
        t = time.time()
        ft = factor_table(w)
        secs = time.time() - t
        xs = sorted(ft['counts'])
        probe_x = [xs[0], xs[len(xs) // 3], xs[len(xs) // 2], xs[-1]]
        for lam in LAMBDAS:
            for x in probe_x:
                ref = reference_log_factor(w, lam, x)
                stored = to_dec(ft['table'][lam][x])
                assert stored <= ref, (name, lam, x)
                max_loss = max(max_loss, float(ref - stored))
        zmax = max(abs(xs[0]), abs(xs[-1])) / math.sqrt(ft['var'])
        print(f'2. {name}: support {len(xs)} points, max |Z| {zmax:.3f} (bound {math.sqrt(len(w) * (len(w) - 1) / (len(w) - K)):.3f}); '
              f'enclosure width {ft["width"] / S:.1e}; certificate holds (slack {ft["cert_slack"] / (ft["total"] * S):.1e}); {secs:.2f} s')
    print(f'   largest (true - stored) log-factor in the checked cells: {max_loss:.2e}  (MARGIN 1e-30 plus the enclosure width)')
    assert factor_table([0] * 35) is None
    print('   all-zero weights (no complete pair, or cancelling tickets): V = 0, the registered skip (factor 1)')

    # 3. a long run with a changing roster: exact accumulation, stored <= reference at every step
    n_draws = 300
    logs = [0] * len(LAMBDAS)
    ref = [0.0] * len(LAMBDAS)
    first = None
    for i in range(1, n_draws + 1):
        n = 35
        w = random_weights(rng, n, 20 + (i * 7) % 60, clusters=3 + i % 5)
        ft = factor_table(w)
        if ft is None:
            continue
        drawn = rng.sample(range(n), K)
        x = sum(w[j] for j in drawn)
        sd = math.sqrt(ft['var'])
        probs = [c / ft['total'] for c in ft['counts'].values()]
        xs = list(ft['counts'])
        for a, lam in enumerate(LAMBDAS):
            logs[a] += ft['table'][lam][x]                      # exact integer sum
            m = sum(p * math.exp(float(lam) * xx / sd) for p, xx in zip(probs, xs))
            ref[a] += float(lam) * x / sd - math.log(m)
        if first is None and crossing(logs):
            first = i
    drift = max(abs(logs[a] / S - ref[a]) for a in range(len(LAMBDAS)))
    lo = mixture_lower(logs)
    print(f'3. {n_draws} fair draws, roster changing every draw: stored running logs vs float reference differ by at most '
          f'{drift:.1e} (float rounding); proved mixture lower bound now {lo / S:.6f}; reached 40: '
          f'{"never" if first is None else "draw " + str(first)}')
    print(f'   worst-case loss of sensitivity after {n_draws} draws: at most {n_draws} * 2e-30 = {n_draws * 2e-30:.0e} in each log')

    # 4. the comparison with 40 at the edge, and extreme running sums
    getcontext().prec = 90
    ln40 = int((Decimal(40).ln() * Decimal(S)).to_integral_value(rounding=ROUND_FLOOR))      # floor(S * ln 40), reference
    tiny = 10 ** (D - 40)                                       # 1e-40
    assert crossing([ln40 + tiny] * 6) and not crossing([ln40 - tiny] * 6)
    assert not crossing([-10 ** 6 * S] * 6) and crossing([10 ** 4 * S] + [-10 ** 6 * S] * 5)
    big = exp_enc(5000 * S)
    assert big[0] <= big[1] and len(str(big[0])) > 2000
    print('4. threshold: all six logs 1e-40 above log 40 cross; 1e-40 below do not; huge negative logs give lower bound 0; '
          'one very large component crosses; exp(5000) is enclosed without overflow')
    print('PROBE PASS')


if __name__ == '__main__':
    main()
