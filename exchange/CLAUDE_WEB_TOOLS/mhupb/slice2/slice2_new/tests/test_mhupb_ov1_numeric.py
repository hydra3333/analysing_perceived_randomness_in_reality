"""MHUP-B slice 2, layer L5: OV-1's numerical kernel (code plan v0.3 sections 6.2, 6.3, 6.5). OFFLINE; invented
weights only; no project record, master or result is read.

The oracles here share no code with the kernel:
  * ORACLE_EXP: exp of a rational by `fractions.Fraction` Taylor series with an explicit remainder, on a 10^-90 grid;
  * the logarithm is checked THROUGH the exponential (lo <= log m <= hi  iff  exp(lo) <= m <= exp(hi));
  * `decimal` at 90 digits is a third opinion only (feasibility evidence, not proof: EX_223 CP-Q2);
  * the distribution is checked against brute force over every subset on small barrels, and by a third counting route.
The full-size brute force (6,724,520 and 62,891,499 subsets) is an evidence run (ov1_bruteforce_evidence.py).
"""
from __future__ import annotations

import ast
import itertools
import random
import unittest
from decimal import Decimal, getcontext
from fractions import Fraction as F
from math import comb, isqrt
from pathlib import Path

from evaluation import ov1_numeric as N

S = 10 ** 50
GRID = 10 ** 90


def _down(q: F) -> F:
    return F((q.numerator * GRID) // q.denominator, GRID)


def _up(q: F) -> F:
    return F(-((-q.numerator * GRID) // q.denominator), GRID)


def ORACLE_EXP_EXACT(u: F) -> tuple[F, F]:
    """(lo, hi) with lo <= exp(u) <= hi for a rational u, by exact fractions: r = u / 2^j with |r| <= 1/2; the exact
    sum of 80 Taylor terms; the remainder bounded by 2 |r|^80 / 80!; then squared back j times, rounded outward on a
    10^-90 grid only between squarings (every value there is positive)."""
    j = 0
    while abs(u) > F(2 ** j, 2):
        j += 1
    r = u / 2 ** j
    term, total = F(1), F(1)
    for k in range(1, 80):
        term = term * r / k
        total += term
    rem = abs(term * r / 80) * 2
    lo, hi = _down(total - rem), _up(total + rem)
    for _ in range(j):
        lo, hi = _down(lo * lo), _up(hi * hi)
    return lo, hi


def ORACLE_EXP(u: F) -> tuple[F, F]:
    """The same bounds, fast: whole numbers on the 10^-90 grid, each Taylor term rounded outward. Written for the
    tests, sharing no code with the kernel (other precision, other reduction, other term count), and itself checked
    against ORACLE_EXP_EXACT below."""
    if u < 0:
        lo, hi = ORACLE_EXP(-u)
        return _down(1 / hi), _up(1 / lo)
    j = 0
    while u > F(2 ** j, 2):
        j += 1
    r_lo = (u.numerator * GRID) // (u.denominator * 2 ** j)
    r_hi = -((-u.numerator * GRID) // (u.denominator * 2 ** j))
    lo = hi = tl = tu = GRID
    for k in range(1, 70):
        tl = (tl * r_lo) // (GRID * k)
        tu = -((-tu * r_hi) // (GRID * k))
        lo += tl
        hi += tu
    hi += 2 * (-((-tu * r_hi) // (GRID * 70))) + 1
    for _ in range(j):
        lo, hi = (lo * lo) // GRID, -((-hi * hi) // GRID)
    return F(lo, GRID), F(hi, GRID)


def dec(n: int) -> Decimal:
    getcontext().prec = 90
    return Decimal(n) / Decimal(S)


def weights_from(n, tickets):
    w = [0] * n
    for top, worst in tickets:
        for j in top:
            w[j] += 1
        for j in worst:
            w[j] -= 1
    return w


def rosters(rng, n, variants, clusters=5, swaps=3):
    bases = [rng.sample(range(n), n) for _ in range(clusters)]
    out = []
    for i in range(variants):
        r = bases[i % clusters][:]
        for _ in range(swaps):
            a, b = rng.randrange(n), rng.randrange(n)
            r[a], r[b] = r[b], r[a]
        out.append((r[:7], r[-7:]))
    return weights_from(n, out)


_REF = {}


def reference_log_factor(w, lam, x) -> Decimal:
    """The true log-factor by `decimal` at 90 digits, from the definitions (third opinion)."""
    getcontext().prec = 90
    key = (tuple(w), lam)
    if key not in _REF:
        dist = route3(w)
        v = F(7 * (len(w) - 7), len(w) - 1) * F(sum(x * x for x in w), len(w))
        sd = (Decimal(v.numerator) / Decimal(v.denominator)).sqrt()
        th = Decimal(lam[0]) / Decimal(lam[1]) / sd
        m = sum(Decimal(c) * (th * xx).exp() for xx, c in dist.items()) / Decimal(comb(len(w), 7))
        _REF[key] = (th, m.ln())
    th, log_m = _REF[key]
    return th * x - log_m


def route3(w):
    """A third counting route, written for the test only: a generating polynomial in two variables held as a dict
    {(how many taken, sum): ways}, multiplied one number at a time WITHOUT the kernel's in-place trick."""
    poly = {(0, 0): 1}
    for wj in w:
        new = dict(poly)
        for (k, s), c in poly.items():
            if k < 7:
                new[(k + 1, s + wj)] = new.get((k + 1, s + wj), 0) + c
        poly = new
    return {s: c for (k, s), c in poly.items() if k == 7}


CASES = {
    'reviewer counterexample N=35': [40] * 7 + [-40] * 7 + [0] * 21,
    'one variant N=35': [1] * 7 + [-1] * 7 + [0] * 21,
    'one variant N=47': [1] * 7 + [-1] * 7 + [0] * 33,
    'two levels N=35': [4] * 7 + [-1] * 28,            # seven numbers carry all the positive weight: Z^2 = N - 1
    'two levels N=47': [40] * 7 + [-7] * 40,
    'skewed N=47': weights_from(47, [(list(range(7)), [7 + (i * 7 + j) % 40 for j in range(7)]) for i in range(300)]),
    '40 overlapping N=35': rosters(random.Random(11), 35, 40),
    '80 overlapping N=47': rosters(random.Random(12), 47, 80),
}


class Primitives(unittest.TestCase):
    def test_exp_encloses_the_fraction_oracle_and_decimal(self):
        rng = random.Random(20261118)
        args = [0, 1, -1, S - 1, S, S + 1, 2 * S + 1, 3 * S - 1, -S, -S - 1, 4 * S + 3, 37 * S, -37 * S]
        args += [rng.randrange(-8 * S, 8 * S) for _ in range(30)] + [rng.randrange(-90 * S, 90 * S) for _ in range(8)]
        for a in args:
            lo, hi = N.exp_enc(a)
            o_lo, o_hi = ORACLE_EXP_EXACT(F(a, S))
            self.assertLessEqual(F(lo, S), o_lo, a)
            self.assertGreaterEqual(F(hi, S), o_hi, a)
            self.assertLess(F(hi - lo, S), o_hi * F(1, 10 ** 44) + F(3, S), a)   # and tight (relative, or 3 grid units)
            ref = dec(a).exp()
            self.assertTrue(dec(lo) <= ref <= dec(hi), a)
            f_lo, f_hi = ORACLE_EXP(F(a, S))                                  # the fast oracle against the exact one:
            self.assertLessEqual(f_lo, o_hi, a)                               # the two enclosures must overlap,
            self.assertGreaterEqual(f_hi, o_lo, a)
            self.assertLess(f_hi - f_lo, f_hi * F(1, 10 ** 80) + F(3, GRID), a)   # and the fast one is narrow
        for a in [rng.randrange(-8 * S, 8 * S) for _ in range(300)]:          # a wider grid, by the fast oracle
            lo, hi = N.exp_enc(a)
            f_lo, f_hi = ORACLE_EXP(F(a, S))
            self.assertLessEqual(F(lo, S), f_lo, a)
            self.assertGreaterEqual(F(hi, S), f_hi, a)

    def test_exp_of_a_very_large_argument_is_enclosed_without_overflow(self):
        lo, hi = N.exp_enc(5000 * S)
        self.assertTrue(0 < lo <= hi)
        self.assertGreater(len(str(lo)), 2000)
        lo, hi = N.exp_enc(-5000 * S)
        self.assertEqual(lo, 0)
        self.assertLessEqual(hi, 1)

    def test_log_is_checked_through_the_exponential_oracle_and_decimal(self):
        rng = random.Random(20261119)
        self.assertEqual(N.log_enc(S, S)[0], 0)                               # log 1 = 0 exactly at the lower end
        self.assertTrue(0 <= N.log_enc(S, S)[1] < 10)
        for m in [S + 1, 2 * S, 4 * S, 5 * S + 5 * S // 10] + [S + rng.randrange(1, 4 * S) for _ in range(60)]:
            lo, hi = N.log_enc(m, m)
            self.assertLessEqual(ORACLE_EXP(F(lo, S))[1], F(m, S), m)        # exp(lo) <= m
            self.assertGreaterEqual(ORACLE_EXP(F(hi, S))[0], F(m, S), m)     # exp(hi) >= m
            self.assertLess(hi - lo, 10 ** 6, m)                              # narrower than 1e-44
            self.assertTrue(dec(lo) <= dec(m).ln() <= dec(hi), m)
        lo, hi = N.log_enc(2 * S, 3 * S)                                      # an interval argument
        self.assertLessEqual(ORACLE_EXP(F(lo, S))[1], 2)
        self.assertGreaterEqual(ORACLE_EXP(F(hi, S))[0], 3)

    def test_enclosures_hold_with_few_terms_so_the_remainders_matter(self):
        """With the series cut short the remainder terms carry the bound (with the full term counts they are far below
        the last digit). The enclosures must still contain the truth, only wider."""
        rng = random.Random(5)
        keep = (N._EXP_TERMS, N._LOG_TERMS)
        try:
            N._EXP_TERMS, N._LOG_TERMS = 6, 4
            for a in [S, S // 2, 3 * S + 7, -2 * S] + [rng.randrange(-6 * S, 6 * S) for _ in range(40)]:
                lo, hi = N.exp_enc(a)
                o_lo, o_hi = ORACLE_EXP(F(a, S))
                self.assertLessEqual(F(lo, S), o_lo, a)
                self.assertGreaterEqual(F(hi, S), o_hi, a)
                self.assertGreater(hi - lo, 10 ** 30, a)                      # visibly wider: the remainder is at work
            for m in [2 * S, 4 * S, 5 * S] + [S + rng.randrange(S // 2, 4 * S) for _ in range(40)]:
                lo, hi = N.log_enc(m, m)
                self.assertLessEqual(ORACLE_EXP(F(lo, S))[1], F(m, S), m)
                self.assertGreaterEqual(ORACLE_EXP(F(hi, S))[0], F(m, S), m)
                self.assertGreater(hi - lo, 10 ** 30, m)
        finally:
            N._EXP_TERMS, N._LOG_TERMS = keep

    def test_squaring_rounds_each_end_the_right_way_exactly(self):
        """The squaring step of exp: the lower end is the exact floor and the upper end the exact ceiling of the square
        (the accumulated slack of a whole exp would hide a flipped direction, so the step is checked on its own)."""
        rng = random.Random(6)
        for _ in range(200):
            lo = rng.randrange(1, 9 * S)
            hi = lo + rng.randrange(0, 1000)
            out_lo, out_hi = N._square(lo, hi)
            self.assertTrue(out_lo * S <= lo * lo < (out_lo + 1) * S)
            self.assertTrue((out_hi - 1) * S < hi * hi <= out_hi * S)
        self.assertEqual(N._square(S, S), (S, S))

    def test_sqrt_bounds_are_exact(self):
        for p, q in ((2, 1), (1, 3), (196, 34), (7 * 28 * 22400, 34 * 35), (0, 5), (10 ** 40 + 1, 7)):
            lo, hi = N.sqrt_enc(p, q)
            self.assertLessEqual(lo * lo * q, p * S * S)
            self.assertGreater(hi * hi * q, p * S * S)
            self.assertLessEqual(hi - lo, 2)

    def test_refusals(self):
        for bad in ((S - 1, S), (2 * S, S), (6 * S, 6 * S)):                  # below 1; out of order; y > 0.7
            with self.assertRaises(N.Refuse):
                N.log_enc(*bad)
        for bad in (-1, S + 1):
            with self.assertRaises(N.Refuse):
                N._exp_small(bad)
        with self.assertRaises(N.Refuse):
            N.exp_enc(1.0)
        with self.assertRaises(N.Refuse):
            N.sqrt_enc(1, 0)
        for w in ([1] * 35, [1.0, -1.0] + [0] * 33, [0] * 7, [True, -1] + [0] * 33):
            with self.assertRaises(N.Refuse):
                N.variance(w)
        with self.assertRaises(N.Refuse):
            N.crossing([0] * 5)


class Distribution(unittest.TestCase):
    def test_counts_equal_brute_force_on_small_barrels(self):
        rng = random.Random(7)
        for n in (8, 9, 11, 13, 15):
            for _ in range(6):
                w = [rng.randrange(-5, 6) for _ in range(n - 1)]
                w.append(-sum(w))
                brute = {}
                for sub in itertools.combinations(w, 7):
                    brute[sum(sub)] = brute.get(sum(sub), 0) + 1
                self.assertEqual(N.counts(w), brute)
                self.assertEqual(N.counts_by_number(w), brute)
                self.assertEqual(N.counts_by_group(w), brute)
                self.assertEqual(route3(w), brute)

    def test_full_size_routes_agree_and_the_variance_is_the_formula(self):
        for name, w in CASES.items():
            dist = N.counts(w)
            self.assertEqual(dist, route3(w), name)
            total = comb(len(w), 7)
            self.assertEqual(sum(dist.values()), total, name)
            self.assertEqual(sum(x * c for x, c in dist.items()), 0, name)
            n = len(w)
            mean = F(sum(w), n)
            formula = F(7 * (n - 7), n - 1) * F(1, n) * sum((x - mean) ** 2 for x in w)      # Sup 6.1, as written
            self.assertEqual(F(*N.variance(w)), formula, name)
            self.assertEqual(F(sum(x * x * c for x, c in dist.items()), total), formula, name)

    def test_z_never_exceeds_the_proved_bound(self):
        """|Z| <= sqrt(N(N-1)/(N-K)) for any weights that sum to zero (plan 6.2), so the series stay in range. The
        two-level patterns give Z^2 = N - 1 exactly, close under the bound."""
        rng = random.Random(8)
        cases = list(CASES.values()) + [rosters(rng, n, v) for n in (35, 47) for v in (1, 3, 20)]
        for w in cases:
            n = len(w)
            num, den = N.variance(w)
            for x in N.counts(w):
                self.assertLessEqual(x * x * den * (n - 7), n * (n - 1) * num)               # Z^2 <= N(N-1)/(N-K)
        for name in ('two levels N=35', 'two levels N=47'):
            w = CASES[name]
            num, den = N.variance(w)
            x = max(N.counts(w))
            self.assertEqual(x * x * den, (len(w) - 1) * num, name)


class FactorTable(unittest.TestCase):
    def test_stored_is_never_above_the_true_factor_and_the_loss_is_below_twice_the_margin(self):
        for name, w in CASES.items():
            t = N.factor_table(w)
            xs = sorted(t['counts'])
            for lam, row in zip(N.LAMBDAS, t['rows']):
                self.assertEqual(sorted(row), xs)
                for x in (xs[0], xs[len(xs) // 3], xs[len(xs) // 2], xs[-1]):
                    ref = reference_log_factor(w, lam, x)
                    self.assertLessEqual(dec(row[x]), ref, (name, lam, x))
                    self.assertLess(ref - dec(row[x]), Decimal(2) / Decimal(10 ** 30), (name, lam, x))
                    self.assertGreater(ref - dec(row[x]), Decimal(1) / Decimal(10 ** 30) - Decimal(1) / Decimal(10 ** 40))

    def test_pointwise_bound_by_exact_fractions_for_one_variant(self):
        """stored <= true  iff  m * exp(stored) <= exp(theta x); proved with ORACLE_EXP and a rational bracket of
        sqrt(V), sharing nothing with the kernel."""
        w = CASES['one variant N=35']
        t = N.factor_table(w)
        v = F(*t['variance'])
        big = 10 ** 80
        root_lo = F(isqrt(v.numerator * big * big // v.denominator), big)
        root_hi = root_lo + F(1, big)
        total = t['total']
        for (num, den), row in zip(N.LAMBDAS, t['rows']):
            th_lo, th_hi = sorted((F(num, den) / root_hi, F(num, den) / root_lo))

            def enc(x):
                a, b = sorted((th_lo * x, th_hi * x))
                return ORACLE_EXP(a)[0], ORACLE_EXP(b)[1]
            m_hi = sum(c * enc(x)[1] for x, c in t['counts'].items()) / total
            for x in row:
                self.assertLessEqual(m_hi * ORACLE_EXP(F(row[x], S))[1], enc(x)[0], (num, den, x))

    def test_certificate_holds_by_the_independent_oracle_on_adversarial_weights(self):
        adversarial = dict(CASES)
        adversarial['all variants identical x 2000'] = [2000] * 7 + [-2000] * 7 + [0] * 33
        adversarial['4000 variants N=47'] = rosters(random.Random(13), 47, 4000, clusters=7)
        for name, w in adversarial.items():
            t = N.factor_table(w)
            for row in t['rows']:
                mean_hi = sum(c * ORACLE_EXP(F(row[x], S))[1] for x, c in t['counts'].items())
                self.assertLessEqual(mean_hi, t['total'], name)
                self.assertGreater(mean_hi, t['total'] * (1 - F(1, 10 ** 28)), name)          # and barely below 1

    def test_zero_variance_is_the_registered_skip(self):
        self.assertIsNone(N.factor_table([0] * 35))
        self.assertIsNone(N.factor_table([0] * 47))

    def test_a_failed_certificate_or_a_wide_enclosure_refuses(self):
        w = CASES['one variant N=35']
        real = N.exp_enc
        try:
            N.exp_enc = lambda a: (real(a)[0], real(a)[1] + 10 ** 25)        # an upper end too loose: no bound proved
            with self.assertRaises(N.Refuse):
                N.factor_table(w)
        finally:
            N.exp_enc = real
        margin = N.MARGIN
        try:
            N.MARGIN = 0                                                      # no room for the enclosure
            with self.assertRaises(N.Refuse):
                N.factor_table(w)
        finally:
            N.MARGIN = margin

    def test_the_certificate_catches_an_error_in_the_derivation(self):
        """Plan 6.3: the certificate is a second, independent guarantee. A logarithm that is wrong by 1e-28 (inside an
        enclosure that still looks narrow) would make every stored factor too large; the pointwise width check cannot
        see it, and the certificate refuses."""
        real = N.log_enc
        try:
            N.log_enc = lambda a, b: tuple(v - 10 ** 22 for v in real(a, b))
            with self.assertRaises(N.Refuse) as caught:
                N.factor_table(CASES['one variant N=35'])
            self.assertIn('certificate', str(caught.exception))
        finally:
            N.log_enc = real

    def test_frozen_fixture_digests(self):
        """A later kernel must reproduce these bytes exactly, or it is a reviewed amendment (plan L5)."""
        got = {name: N.table_digest(N.factor_table(CASES[name]))
               for name in FROZEN}
        self.assertEqual(got, FROZEN)
        t = N.factor_table(CASES['one variant N=35'])
        self.assertTrue(N.table_bytes(t).startswith(b'OV1_KERNEL_V1 digits=50 margin=100000000000000000000 total=6724520 '))


FROZEN = {
    'reviewer counterexample N=35': '64fabc019f24098ce28cfbc70bf2b74881514f0caa9be03e50ac76beed287e71',
    'one variant N=47': '0161aefb70f669654cda1d24d276eaa23aa5cc51f76a699576a5e9ff2fb355d1',
    'skewed N=47': 'd6f0e7b7a94f252cd8f9da898e341179b5aa125e4caacb7fb972b441c26c806a',
}


class Crossing(unittest.TestCase):
    def test_the_bar_at_the_edge(self):
        getcontext().prec = 90
        ln40 = int(Decimal(40).ln() * Decimal(S))                             # floor(S ln 40), from decimal
        self.assertLessEqual(ORACLE_EXP(F(ln40, S))[1], 40)                   # confirmed by the fraction oracle
        self.assertGreaterEqual(ORACLE_EXP(F(ln40 + 1, S))[0], 40)
        tiny = 10 ** 10                                                       # 1e-40
        self.assertTrue(N.crossing([ln40 + tiny] * 6))
        self.assertFalse(N.crossing([ln40 - tiny] * 6))
        self.assertFalse(N.crossing([ln40] * 6))                              # exactly at floor(S ln 40): not proved
        self.assertFalse(N.crossing([-10 ** 6 * S] * 6))
        self.assertTrue(N.crossing([10 ** 4 * S] + [-10 ** 6 * S] * 5))
        self.assertFalse(N.crossing([0] * 6))
        self.assertEqual(N.mixture_lower([0] * 6), S)
        self.assertEqual(N.fixed_text(N.mixture_lower([0] * 6)), '1.000000000000')

    def test_running_sums_stay_below_a_float_free_reference_over_many_draws(self):
        """300 invented fair draws, a different roster each draw: the exact integer sums of stored log-factors stay at
        or below the decimal reference, by at most draws * 2e-30."""
        rng = random.Random(20261120)
        logs, refs, n_counted = [0] * 6, [Decimal(0)] * 6, 0
        for i in range(1, 41):
            w = rosters(rng, 35, 5 + (i * 7) % 30, clusters=3 + i % 5)
            t = N.factor_table(w)
            if t is None:
                continue
            drawn = rng.sample(range(35), 7)
            x = sum(w[j] for j in drawn)
            n_counted += 1
            for a, lam in enumerate(N.LAMBDAS):
                logs[a] += t['rows'][a][x]
                refs[a] += reference_log_factor(w, lam, x)
        for a in range(6):
            self.assertLessEqual(dec(logs[a]), refs[a])
            self.assertLess(refs[a] - dec(logs[a]), Decimal(2 * n_counted) / Decimal(10 ** 30))

    def test_display_texts(self):
        self.assertEqual(N.z_text(0, 5, 1), '0.000000000000')
        self.assertEqual(N.z_text(3, 9, 1), '1.000000000000')
        self.assertEqual(N.z_text(-3, 9, 4), '-2.000000000000')
        self.assertEqual(N.fixed_text(-S // 3, 4), '-0.3333')
        self.assertEqual(N.fixed_text(-1, 4), '0.0000')


class Static(unittest.TestCase):
    def test_the_kernel_has_no_float_no_library_exp_or_log_and_no_true_division(self):
        path = Path(N.__file__)
        tree = ast.parse(path.read_text(encoding='ascii'))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {a.name for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported |= {f'{node.module}.{a.name}' for a in node.names}
            self.assertNotIsInstance(node, ast.Div, 'true division in the kernel')
            if isinstance(node, ast.Constant):
                self.assertNotIsInstance(node.value, (float, complex), 'a float constant in the kernel')
            if isinstance(node, ast.Name):
                self.assertNotIn(node.id, ('float', 'complex', 'Decimal', 'Fraction', 'round', 'pow', 'divmod'))
            if isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, ('exp', 'log', 'sqrt', 'expm1', 'log1p', 'fsum', 'pow'))
        self.assertEqual(imported, {'__future__.annotations', 'hashlib', 'math.comb', 'math.isqrt'})


if __name__ == '__main__':
    unittest.main()
