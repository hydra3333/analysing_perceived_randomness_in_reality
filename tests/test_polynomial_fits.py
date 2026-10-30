"""The shared helper _common/polynomial_fits.py, revision 1 (E_3/E_4 design note v0.1 section 3). OFFLINE.

Pure mathematics on invented series: no data file, no process, no repository write. Every expected value in
WorkedExamples was computed by hand and re-checked by computation (design note section 6).
"""
from __future__ import annotations

from fractions import Fraction as Fr
import hashlib
from pathlib import Path
import unittest

from e2r_fixtures import ROOT
from _common import polynomial_fits as PF


def invented(label, n, threshold=52):
    """An invented 0/1 series (about one 1 in five), deterministic. Never a real result."""
    return [1 if hashlib.sha256(f'pf:{label}:{i}'.encode()).digest()[0] < threshold else 0 for i in range(n)]


def ts_of(*values):
    return [Fr(v) for v in values]


class WorkedExamples(unittest.TestCase):
    def test_least_squares_flat_line(self):
        self.assertEqual(PF.least_squares(ts_of(-3, -2, -1), [1, 0, 1], 1), [Fr(2, 3), Fr(0)])

    def test_least_squares_rising_line_exceeds_one(self):
        c = PF.least_squares(ts_of(-4, -3, -2, -1), [0, 0, 1, 1], 1)
        self.assertEqual(c, [Fr(3, 2), Fr(2, 5)])          # p(0) = 3/2 > 1: scores are not probabilities

    def test_minimax_constant(self):
        c, err, ref = PF.minimax(ts_of(-3, -2, -1), [Fr(0), Fr(1, 3), Fr(1)], 0)
        self.assertEqual((c, err), ([Fr(1, 2)], Fr(1, 2)))

    def test_minimax_on_raw_alternating_data_is_the_constant_half(self):
        y = [i % 2 for i in range(12)]
        c, err, _ = PF.minimax(PF.abscissae(12), y, 2)
        self.assertEqual((c, err), ([Fr(1, 2), Fr(0), Fr(0)], Fr(1, 2)))

    def test_interpolation(self):
        c = PF.interpolate(ts_of(-3, -2, -1), [0, 1, 0])
        self.assertEqual(c, [Fr(-3), Fr(-4), Fr(-1)])       # p(t) = -(t + 2)^2 + 1
        self.assertEqual(PF.interpolate_newton(ts_of(-3, -2, -1), [0, 1, 0]), c)

    def test_abscissae_and_smoothing(self):
        self.assertEqual(PF.abscissae(3), ts_of(-3, -2, -1))
        self.assertEqual(PF.smoothed([0, 0, 1, 1, 0], 1), [Fr(0), Fr(1, 3), Fr(2, 3), Fr(2, 3), Fr(1, 2)])
        self.assertEqual(PF.smoothed([1, 0], 0), [Fr(1), Fr(0)])


class LeastSquares(unittest.TestCase):
    def test_two_algorithms_agree_and_the_normal_equations_hold(self):
        for window in (10, 52, 104):
            ts = PF.abscissae(window)
            for degree in range(0, 6):
                ls = PF.LeastSquares(ts, degree)
                for label in range(4):
                    with self.subTest(window=window, degree=degree, label=label):
                        y = invented(label, window)
                        c = ls.fit(y)
                        self.assertEqual(c, PF.least_squares_by_recurrence(ts, y, degree))
                        self.assertEqual(c, PF.least_squares(ts, y, degree))
                        res = [yi - PF.evaluate(c, t) for t, yi in zip(ts, y)]
                        for k in range(degree + 1):                 # the residual is orthogonal to every t^k
                            self.assertEqual(sum(r * t ** k for r, t in zip(res, ts)), 0)

    def test_a_polynomial_is_reproduced_exactly(self):
        ts = PF.abscissae(30)
        y = [3 * t ** 2 - t + Fr(1, 7) for t in ts]
        self.assertEqual(PF.least_squares(ts, y, 2), [Fr(1, 7), Fr(-1), Fr(3)])


class Interpolation(unittest.TestCase):
    def test_lagrange_equals_newton_and_passes_through_the_points(self):
        for n in range(1, 7):
            ts = [Fr(-(3 * k + 1)) for k in range(n)]
            for label in range(3):
                y = [Fr(v, 7) for v in invented(label, n, 128)]
                c = PF.interpolate(ts, y)
                self.assertEqual(c, PF.interpolate_newton(ts, y))
                self.assertEqual([PF.evaluate(c, t) for t in ts], y)


class Minimax(unittest.TestCase):
    def test_certificate_holds_and_minimax_beats_least_squares_on_the_worst_error(self):
        for window, degree in ((52, 2), (52, 3), (104, 3), (20, 0), (20, 1)):
            ts = PF.abscissae(window)
            for label in range(6):
                with self.subTest(window=window, degree=degree, label=label):
                    s = PF.smoothed(invented(label, window), 4)
                    c, err, ref = PF.minimax(ts, s, degree)
                    self.assertEqual(PF.minimax_certificate(ts, s, c, degree), err)
                    self.assertEqual(len(ref), degree + 2)
                    ls = PF.least_squares(ts, s, degree)
                    self.assertLessEqual(err, max(abs(v - PF.evaluate(ls, t)) for t, v in zip(ts, s)))
                    for k in range(degree + 1):                     # a nudge to any coefficient is worse
                        for delta in (Fr(1, 10 ** 6), Fr(-1, 10 ** 6)):
                            nudged = list(c)
                            nudged[k] += delta
                            self.assertGreater(max(abs(v - PF.evaluate(nudged, t)) for t, v in zip(ts, s)), err)

    def test_certificate_refuses_a_polynomial_that_is_not_minimax(self):
        ts = PF.abscissae(52)
        s = PF.smoothed(invented(1, 52), 4)
        ls = PF.least_squares(ts, s, 2)
        c, _err, _ref = PF.minimax(ts, s, 2)
        self.assertNotEqual(ls, c)
        with self.assertRaises(ValueError):
            PF.minimax_certificate(ts, s, ls, 2)

    def test_certificate_refuses_exactly_one_alternation_too_few(self):
        ts, ys = PF.abscissae(4), [1, -1, 0, 0]
        zero = [Fr(0), Fr(0)]                     # errors 1, -1, 0, 0: two alternations at the maximum, needs three
        with self.assertRaises(ValueError):
            PF.minimax_certificate(ts, ys, zero, 1)
        _c, err, _ref = PF.minimax(ts, ys, 1)
        self.assertLess(err, 1)                   # and indeed the zero line is not the minimax line

    def test_the_returned_reference_alternates_at_the_minimax_error(self):     # E34-O01: sign orientation
        for window, degree in ((52, 2), (52, 3), (20, 1)):
            ts = PF.abscissae(window)
            for label in range(6):
                with self.subTest(window=window, degree=degree, label=label):
                    s = PF.smoothed(invented(label, window), 4)
                    c, err, ref = PF.minimax(ts, s, degree)
                    e = [s[r] - PF.evaluate(c, ts[r]) for r in ref]
                    self.assertEqual(ref, sorted(set(ref)))
                    self.assertEqual({abs(x) for x in e}, {err})
                    self.assertTrue(all(a == -b for a, b in zip(e, e[1:])))

    def test_tied_largest_errors_take_the_lowest_index(self):                # E34-O01: violating-index ties
        # Degree 0 on 0, 1, 1, 0: the initial reference (0, 3) levels at h = 0 with c = 0; indices 1 and 2 tie
        # for the largest error, so index 1 enters (replacing 0, whose sign matches) and the result is (1, 3).
        # Taking the highest index instead would end at (2, 3) with the same polynomial.
        c, err, ref = PF.minimax(PF.abscissae(4), [0, 1, 1, 0], 0)
        self.assertEqual((c, err, ref), ([Fr(1, 2)], Fr(1, 2), [1, 3]))

    def test_an_intermediate_reference_with_zero_levelled_error_is_exchanged(self):   # E34-O01: h = 0
        # (-5, 0), (-3, 1), (-1, 2) are collinear, so the initial reference for degree 1 levels at h = 0,
        # while the points between are off that line: the exchange must continue rather than stop.
        ts, ys = PF.abscissae(5), [0, 1, 1, 1, 2]
        self.assertEqual([(2 * k * 4 + 2) // 4 for k in range(3)], [0, 2, 4])
        c, err, ref = PF.minimax(ts, ys, 1)
        self.assertGreater(err, 0)
        self.assertEqual(PF.minimax_certificate(ts, ys, c, 1), err)
        self.assertNotEqual(ref, [0, 2, 4])

    def test_the_exchange_cap_raises_rather_than_returning(self):           # E34-O01: the cap
        from unittest import mock
        with mock.patch.object(PF, 'MINIMAX_EXCHANGE_CAP', 1):
            with self.assertRaises(RuntimeError):
                PF.minimax(PF.abscissae(4), [0, 1, 1, 0], 0)       # needs one exchange, then a second pass
        self.assertEqual(PF.MINIMAX_EXCHANGE_CAP, 10000)

    def test_an_exact_polynomial_has_zero_error(self):
        ts = PF.abscissae(15)
        c, err, _ = PF.minimax(ts, [Fr(0)] * 15, 3)
        self.assertEqual((c, err), ([Fr(0)] * 4, Fr(0)))
        self.assertEqual(PF.minimax_certificate(ts, [Fr(0)] * 15, c, 3), 0)


class Refusals(unittest.TestCase):
    def test_bad_inputs_are_refused(self):
        ts = PF.abscissae(5)
        for call in (lambda: PF.least_squares(ts, [0, 1, 0, 1, 0], 5),          # too few points for degree 5
                     lambda: PF.least_squares(ts, [0, 1, 0, 1, 0.5], 1),        # a float value
                     lambda: PF.least_squares([Fr(0), Fr(0), Fr(1)], [0, 1, 0], 1),   # repeated abscissa
                     lambda: PF.least_squares([0.0, 1.0, 2.0], [0, 1, 0], 1),   # float abscissae
                     lambda: PF.minimax(list(reversed(ts)), [0, 1, 0, 1, 0], 1),  # not increasing
                     lambda: PF.minimax(ts, [0, 1, 0, 1, 0], 4),                # needs D + 2 points
                     lambda: PF.smoothed([0, 1], -1), lambda: PF.abscissae(0),
                     lambda: PF.least_squares(ts, [0, 1, 0, 1, 0], -1)):
            with self.assertRaises(ValueError):
                call()


class StaticGuards(unittest.TestCase):
    def test_exact_arithmetic_only_and_no_outside_access(self):
        text = (ROOT / 'src' / 'methods' / '_common' / 'polynomial_fits.py').read_text('utf-8')
        for word in ('import math', 'float(', 'numpy', 'scipy', 'open(', 'read_bytes', 'write_bytes', 'import os',
                     'subprocess', 'game_draws_reader', 'source' + '_data', 'contract_'):
            self.assertNotIn(word, text, f'polynomial_fits.py mentions {word}')


if __name__ == '__main__':
    unittest.main()
