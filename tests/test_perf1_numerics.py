"""PERF-1: the faster exact binomial sum and Clopper-Pearson interval give the same results as WF-1B's.

The oracles below are WF-1B v3's code, copied unchanged: the plain Horner sum, the Fraction tails and the exact
bisection. Every comparison is exact (integers, or float64 equality). Invented inputs only; no file is read."""
from __future__ import annotations

import ast
import random
import sys
import unittest
from fractions import Fraction
from math import comb
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / 'src'), str(HERE.parent / 'src' / 'methods')]
from evaluation import numerics as NU   # noqa: E402


# ---------------------------------------------------------------- oracles: WF-1B v3, unchanged

def _horner_sum(n, a, c, lo, hi):
    length = hi - lo
    acc = comb(n, hi)
    cpow = 1
    for i in range(length - 1, -1, -1):
        cpow *= c
        acc = acc * a + comb(n, lo + i) * cpow
    return acc * a ** lo * c ** (n - hi)


def _upper(n, p, k):
    if k <= 0:
        return Fraction(1)
    if k > n:
        return Fraction(0)
    a, b = p.numerator, p.denominator
    c = b - a
    num = _horner_sum(n, a, c, k, n) if n - k + 1 <= k else b ** n - _horner_sum(n, a, c, 0, k - 1)
    return Fraction(num, b ** n)


def _lower(n, p, k):
    if k < 0:
        return Fraction(0)
    if k >= n:
        return Fraction(1)
    a, b = p.numerator, p.denominator
    c = b - a
    num = _horner_sum(n, a, c, 0, k) if k + 1 <= n - k else b ** n - _horner_sum(n, a, c, k + 1, n)
    return Fraction(num, b ** n)


def _bisect(pred_high):
    lo, hi = 0.0, 1.0
    while True:
        mid = lo + (hi - lo) / 2
        if mid <= lo or mid >= hi:
            break
        if pred_high(Fraction(mid)):
            hi = mid
        else:
            lo = mid
    return hi if pred_high((Fraction(lo) + Fraction(hi)) / 2) is False else lo


def _cp_oracle(k, n, conf=Fraction(95, 100)):
    half = (1 - conf) / 2
    lower = 0.0 if k == 0 else _bisect(lambda q: _upper(n, q, k) > half)
    upper = 1.0 if k == n else _bisect(lambda q: _lower(n, q, k) < half)
    return lower, upper


# ---------------------------------------------------------------- tests

class ExactSum(unittest.TestCase):

    def test_binary_splitting_equals_horner(self):
        rng = random.Random(20261101)
        cases = [(1, 0, 0), (1, 0, 1), (1, 1, 1), (17, 0, 17), (17, 5, 5), (40, 0, 15), (40, 16, 40)]
        cases += [(n, lo, rng.randint(lo, n)) for n in (rng.randint(1, 300) for _ in range(1500))
                  for lo in (rng.randint(0, n),)]
        for n, lo, hi in cases:
            for a, c in ((0, 1), (1, 0), (1, 1), (rng.randint(1, 2 ** 64), rng.randint(1, 2 ** 64))):
                with self.subTest(n=n, lo=lo, hi=hi, a=a, c=c):
                    self.assertEqual(NU._pmf_num_sum(n, a, c, lo, hi), _horner_sum(n, a, c, lo, hi))

    def test_report_size_sums(self):
        """n = 10,000 at a float probability (denominator 2**63), both short and long ranges."""
        q = Fraction(0.004417893020241)
        a, b = q.numerator, q.denominator
        for lo, hi in ((0, 37), (0, 4999), (5001, 10000), (9990, 10000)):
            with self.subTest(lo=lo, hi=hi):
                self.assertEqual(NU._pmf_num_sum(10000, a, b - a, lo, hi), _horner_sum(10000, a, b - a, lo, hi))


class ClopperPearson(unittest.TestCase):

    def test_every_k_up_to_n_40(self):
        for n in range(1, 41):
            for k in range(n + 1):
                with self.subTest(k=k, n=n):
                    self.assertEqual(NU.clopper_pearson(k, n), _cp_oracle(k, n))

    def test_report_sizes(self):
        """MR16's n (220 and 291 targets) and N1's R; also another confidence level."""
        for k, n in ((1, 220), (11, 220), (110, 220), (219, 220), (3, 291), (150, 291), (1, 2000), (999, 2000),
                     (37, 10000)):
            with self.subTest(k=k, n=n):
                self.assertEqual(NU.clopper_pearson(k, n), _cp_oracle(k, n))
        self.assertEqual(NU.clopper_pearson(7, 50, Fraction(99, 100)), _cp_oracle(7, 50, Fraction(99, 100)))

    def test_the_guided_path_is_used(self):
        """At N1's size the decimal-guided search is confirmed without falling back to the exact bisection."""
        with mock.patch.object(NU, '_bisect_float', side_effect=AssertionError('fell back')):
            for k in (0, 1, 37, 2500, 4999, 9990, 10000):
                with self.subTest(k=k):
                    lo, hi = NU.clopper_pearson(k, 10000)
                    self.assertTrue(0.0 <= lo < k / 10000 < hi <= 1.0 or k in (0, 10000))

    def test_a_wrong_guide_falls_back_to_the_exact_bisection(self):
        n, k, half = 60, 9, Fraction(1, 40)
        exact = lambda q: NU._upper_gt_exact(n, q, k, half)        # noqa: E731
        want = _bisect(lambda q: _upper(n, q, k) > half)
        for guide in (lambda d: True, lambda d: False, lambda d: d > NU.Decimal('0.3'),
                      lambda d: d > NU.Decimal(want) * 2):
            with self.subTest(guide=guide):
                self.assertEqual(NU._bisect_guided(guide, exact), want)


class ProgressLines(unittest.TestCase):

    def test_progress_lines_carry_counts_only(self):
        """Every progress() call in report.py formats only len(...) of something, or the search-log row number."""
        tree = ast.parse((HERE.parent / 'src' / 'evaluation' / 'report.py').read_text(encoding='utf-8'))
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'progress']
        self.assertGreaterEqual(len(calls), 6)
        for call in calls:
            (arg,) = call.args
            for v in ast.walk(arg):
                if isinstance(v, ast.FormattedValue):
                    ok = (isinstance(v.value, ast.Call) and getattr(v.value.func, 'id', '') == 'len') or \
                         (isinstance(v.value, ast.Name) and v.value.id == 'row')
                    self.assertTrue(ok, ast.unparse(v.value))


if __name__ == '__main__':
    unittest.main()
