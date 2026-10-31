"""WF-1B numerics (design v0.1r1 sections 6.6 and 9.3-9.5; MRT-03 and MRT-04 in substance). Fair-draw arithmetic
only. Values are pinned from the published evidence (exchange/EX_077_Claude/ev_wf1_reference.txt,
exchange/EX_079_Claude/ev_wf1_tails.txt and ev_wf1_numerics2.txt), not re-derived from this module."""
from __future__ import annotations

import decimal
import math
import sys
import time
import unittest
from decimal import Decimal
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from evaluation import numerics as N   # noqa: E402


def lgamma_log10_upper(n: int, p: float, k: int) -> float:
    """R3 17.11's former production route (log-space lgamma sum), the independent cross-check (MRT-04)."""
    lp, lq = math.log(p), math.log1p(-p)
    terms = [math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * lp + (n - j) * lq
             for j in range(k, n + 1)]
    m = max(terms)
    return (m + math.log(sum(math.exp(t - m) for t in terms))) / math.log(10)


class Sigma(unittest.TestCase):

    def test_r3_table(self):
        """R3 17.5.3's 1-6 sigma table (ev_wf1_reference.txt section 1)."""
        table = {1: '0.158655', 2: '0.0227501', 3: '0.00134990', 4: '3.16712e-5', 5: '2.86652e-7', 6: '9.86588e-10'}
        for s, q in table.items():
            got = N.sigma_from_p(Fraction(q))
            self.assertIsNone(got['label'])
            self.assertAlmostEqual(got['sigma'], s, delta=2e-5)   # the table's Q values carry 6 digits

    def test_mrt03_deficit_example(self):
        """Zero Division 9 wins in 291 Powerball draws: P_lo 0.0111058 = 2.28673 deficit sigma (MRT-03)."""
        pd9 = Fraction(51597, 3362260)      # Powerball division 9 (2 main + Powerball), R3 17.4.2
        p_lo = N.binom_lower(291, pd9, 0)
        self.assertEqual(f"{float(p_lo):.6g}", '0.0111058')
        self.assertEqual(f"{N.z_minus(p_lo)['sigma']:.6g}", '2.28673')

    def test_extremes(self):
        """ev_wf1_tails.txt section C."""
        self.assertEqual(N.sigma_from_p(Fraction(1, 10 ** 300))['sigma'], 37.0470962993612)
        self.assertEqual(N.sigma_from_p(Fraction(1, 10 ** 700))['sigma'], 56.68955328257109)
        self.assertEqual(N.sigma_from_p(Fraction(1, 2) - Fraction(1, 10 ** 20))['sigma'], 2.5066282746310004e-20)
        self.assertEqual(N.sigma_from_p(Fraction(1, 2)), {'sigma': 0.0, 'label': None})
        self.assertEqual(N.sigma_from_p(Fraction(1)), {'sigma': 0.0, 'label': None})

    def test_above_bound(self):
        tiny = Fraction(1, 10 ** 220000)       # below Q(1000), about 10**-217150.6
        self.assertEqual(N.sigma_from_p(tiny), {'sigma': 1000.0, 'label': 'SIGMA_ABOVE_BOUND'})
        near = Fraction(1, 10 ** 217000)       # above Q(1000): a finite sigma just under 1000
        got = N.sigma_from_p(near)
        self.assertIsNone(got['label'])
        self.assertTrue(999.0 < got['sigma'] < 1000.0)

    def test_refusals(self):
        for bad in (Fraction(0), Fraction(-1, 3), Fraction(4, 3)):
            with self.assertRaises(ValueError):
                N.sigma_from_p(bad)
        with self.assertRaises(TypeError):
            N.sigma_from_p(0.01)

    def test_two_routes_agree(self):
        """ev_wf1_numerics2.txt section 1: series and continued fraction agree on x in [5, 6] to 1.7e-47."""
        with decimal.localcontext(N._ctx()):
            for i in range(11):
                x = Decimal(5) + Decimal(i) / 10
                a = 1 - N._erf_series(x)
                b = N._erfc_cf(x)
                self.assertLess(abs(a - b) / b, Decimal('1e-40'))

    def test_pi_constant(self):
        """The module's pi constant against an independent decimal computation (Machin's formula)."""
        with decimal.localcontext(decimal.Context(prec=110)):
            def arctan_inv(x):
                x = Decimal(x)
                total, term, n, sign = Decimal(0), 1 / x, 1, 1
                while term > Decimal(10) ** -108:
                    total += sign * term / n
                    term /= x * x
                    n += 2
                    sign = -sign
                return total
            pi = 4 * (4 * arctan_inv(5) - arctan_inv(239))
            self.assertLess(abs(pi - Decimal(N._PI_TEXT)), Decimal(10) ** -99)

    def test_round_trip(self):
        """Q(sigma) recovers p to well below float64 resolution for ordinary values."""
        for p in (Fraction(1, 7), Fraction(1, 1000), Fraction(3, 10 ** 9), Fraction(1, 10 ** 40)):
            s = N.sigma_from_p(p)['sigma']
            with decimal.localcontext(N._ctx()):
                q = N._upper_tail(Decimal(s))
                self.assertLess(abs(q / N._fraction_to_decimal(p) - 1), Decimal('1e-12') * Decimal(str(max(1.0, s))))


class Binomial(unittest.TestCase):

    def test_published_sizes(self):
        """ev_wf1_numerics2.txt section 3 (MRT-04 sizes), exact on the shorter side and fast."""
        t0 = time.perf_counter()
        cases = [(5000, Fraction(1, 10 ** 9), 40, '-260.0208'), (5000, Fraction(1, 10 ** 9), 3, '-16.6815'),
                 (5000, Fraction(51597, 3362260), 120, '-5.6100'), (432, Fraction(611573, 26898080), 16, '-1.3876')]
        for n, p, k, want in cases:
            got = N.p_output(N.binom_upper(n, p, k))['p_log10']
            self.assertEqual(f'{float(got):.4f}', want, (n, p, k, got))
        self.assertLess(time.perf_counter() - t0, 5.0)

    def test_published_lower(self):
        """ev_wf1_tails.txt section D: n=5000, p=51597/3362260, P(X<=0): log10 -33.582."""
        got = N.p_output(N.binom_lower(5000, Fraction(51597, 3362260), 0))['p_log10']
        self.assertEqual(f'{float(got):.3f}', '-33.582', got)

    def test_against_lgamma_route(self):
        for n, p, k in ((291, Fraction(51597, 3362260), 9), (291, Fraction(1, 20), 25), (432, Fraction(1, 7), 80),
                        (219, Fraction(3, 1000), 4), (1000, Fraction(1, 2), 560)):
            exact = N.binom_upper(n, p, k)
            ref = lgamma_log10_upper(n, float(p), k)
            self.assertAlmostEqual(float(N.p_output(exact)['p_log10']), ref, delta=1e-9 * max(1, abs(ref)))

    def test_identities_and_edges(self):
        n, p = 57, Fraction(2, 9)
        for k in range(-1, n + 2):
            self.assertEqual(N.binom_upper(n, p, k) + N.binom_lower(n, p, k - 1), 1)
        self.assertEqual(N.binom_upper(n, p, 0), 1)
        self.assertEqual(N.binom_upper(n, p, n + 1), 0)
        self.assertEqual(N.binom_lower(n, p, n), 1)
        self.assertEqual(N.binom_lower(n, p, -1), 0)
        self.assertEqual(N.binom_upper(10, Fraction(1, 2), 10), Fraction(1, 1024))
        self.assertEqual(N.binom_upper(0, p, 0), 1)
        with self.assertRaises(TypeError):
            N.binom_upper(10, 0.5, 3)

    def test_tail_below_float64(self):
        p = N.binom_upper(5000, Fraction(1, 10 ** 9), 40)        # about 10**-260: still in float64's range
        self.assertIsNone(N.p_output(p)['label'])
        p = N.binom_upper(5000, Fraction(1, 10 ** 9), 80)        # about 10**-6xx: below it
        out = N.p_output(p)
        self.assertEqual(out['label'], 'P_BELOW_FLOAT64_RANGE')
        self.assertEqual(out['p_float'], float(p))
        self.assertLess(float(out['p_log10']), -308)
        sub = N.p_output(Fraction(1, 10 ** 310))                  # a subnormal float, correctly rounded
        self.assertEqual((sub['p_float'], sub['p_log10'], sub['label']), (1e-310, '-310', 'P_BELOW_FLOAT64_RANGE'))
        self.assertEqual(N.p_output(Fraction(1, 10 ** 300))['p_log10'], '-300')
        ok = N.p_output(Fraction(1, 1000))
        self.assertEqual((ok['p_float'], ok['p_log10'], ok['label']), (0.001, '-3', None))
        self.assertEqual(N.p_output(Fraction(1))['p_log10'], '0')


class MR7Null(unittest.TestCase):

    def test_published_means_and_mass(self):
        """ev_wf1_reference.txt section 3: Powerball n=291 and 432 have 2038 and 3025 coefficients, mean 1.4 a draw;
        Oz Lotto n=219 has 1534 coefficients, mean 10731/47 per window."""
        for game, n, length, mean in (('POWERBALL', 291, 2038, Fraction(2037, 5)),
                                      ('POWERBALL', 432, 3025, Fraction(3024, 5)),
                                      ('OZLOTTO', 219, 1534, Fraction(10731, 47))):
            c = N.mr7_null(game, n)
            w, total = N.pmf_weights(game)
            self.assertEqual(len(c), length)
            self.assertEqual(sum(c), total ** n)
            self.assertEqual(Fraction(sum(s * x for s, x in enumerate(c)), total ** n), mean)

    def test_small_case_by_convolution(self):
        w, total = N.pmf_weights('OZLOTTO')
        conv = [1]
        for _ in range(3):
            nxt = [0] * (len(conv) + 7)
            for i, a in enumerate(conv):
                for m, b in enumerate(w):
                    nxt[i + m] += a * b
            conv = nxt
        self.assertEqual(list(N.mr7_null('OZLOTTO', 3)), conv)
        up, lo = N.mr7_tails('OZLOTTO', 3, 5)
        self.assertEqual(up, Fraction(sum(conv[5:]), total ** 3))
        self.assertEqual(lo, Fraction(sum(conv[:6]), total ** 3))
        self.assertEqual(up + lo - Fraction(conv[5], total ** 3), 1)

    def test_weights(self):
        self.assertEqual(N.pmf_weights('POWERBALL'), ([comb(7, m) * comb(28, 7 - m) for m in range(8)], comb(35, 7)))
        self.assertEqual(N.pmf_weights('OZLOTTO')[1], comb(47, 7))

    def test_bound(self):
        with self.assertRaises(ValueError) as cm:
            N.mr7_null('POWERBALL', 1001)
        self.assertEqual(str(cm.exception), 'MR_EXACT_BOUND_EXCEEDED')
        self.assertEqual(N.mr7_null('POWERBALL', 0), (1,))


class ClopperPearson(unittest.TestCase):

    def test_known_values(self):
        # k = 0: upper = 1 - (alpha/2)**(1/n); k = n: lower = (alpha/2)**(1/n).
        lo, hi = N.clopper_pearson(0, 10)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 1 - 0.025 ** 0.1, places=14)
        lo, hi = N.clopper_pearson(10, 10)
        self.assertEqual(hi, 1.0)
        self.assertAlmostEqual(lo, 0.025 ** 0.1, places=14)
        # A classic value: 5 of 20 gives (0.0865715, 0.4910459) to 7 digits.
        lo, hi = N.clopper_pearson(5, 20)
        self.assertAlmostEqual(lo, 0.0865715, places=6)
        self.assertAlmostEqual(hi, 0.4910459, places=6)

    def test_bounds_hit_the_tails(self):
        n, k = 291, 7
        lo, hi = N.clopper_pearson(k, n)
        self.assertLessEqual(abs(float(N.binom_upper(n, Fraction(lo), k)) - 0.025), 1e-12)
        self.assertLessEqual(abs(float(N.binom_lower(n, Fraction(hi), k)) - 0.025), 1e-12)

    def test_refusals(self):
        for k, n in ((0, 0), (-1, 5), (6, 5)):
            with self.assertRaises(ValueError):
                N.clopper_pearson(k, n)


class Display(unittest.TestCase):

    def test_formats(self):
        self.assertEqual(N.format_sigma(2.28673), '2.29')
        self.assertEqual(N.format_prob(0.0111058123), '1.11058e-02')


if __name__ == '__main__':
    unittest.main()
