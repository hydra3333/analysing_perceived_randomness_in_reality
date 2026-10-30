"""The shared gaps helper _common/recurrence_gaps.py, revision 1 (wave 2 design note v0.1r2 sections 3, 4.2, 10). OFFLINE.

Pure arithmetic on invented draws: no data file, no process, no repository write. Expected values are the
design note's worked examples (computed and asserted by its reviewed reference script) or are recomputed here
from scratch. The log-sign checks use 60-digit decimal logarithms only as an independent cross-check.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Fr
import hashlib
import itertools
import unittest

from e2r_fixtures import ROOT
from _common import recurrence_gaps as RG

EX = [[1, 2], [3, 4], [1, 5], [2, 6], [1, 7], [3, 8], [1, 9], [2, 10], [4, 5], [1, 6], [3, 7], [1, 8]]   # 10 labels, K = 2
ZERO_WITNESS = [[1], [1], [2], [2], [1], [1], [1], [2]]          # EX_071: a_k = 6, -12, 0, 6; the log sum is exactly 0


def invented(n, low=1, high=35, k=7, seed='rg'):
    """n invented draws of k distinct labels from low..high, deterministic. Never a real result."""
    out = []
    for i in range(n):
        pool = sorted(range(low, high + 1), key=lambda j: hashlib.sha256(f'{seed}:{i}:{j}'.encode()).digest())
        out.append(sorted(pool[:k]))
    return out


def ex069_witness():
    """EX_069's W2-B01 witness: 104 invented draws, 7 of 35, ordered by SHA-256 of '32|position|label'."""
    return [sorted(sorted(range(1, 36), key=lambda j: hashlib.sha256(f'32|{t}|{j}'.encode('ascii')).digest())[:7])
            for t in range(1, 105)]


def decimal_sign(a):
    with localcontext() as ctx:
        ctx.prec = 60
        v = sum((Decimal(c) * Decimal(k).ln() for k, c in a.items()), Decimal(0))
    return (v > 0) - (v < 0)


class WorkedExamples(unittest.TestCase):
    def test_gaps_ages_and_exposures(self):
        app = RG.appearances(EX, 1, 10)
        self.assertEqual(RG.completed_gaps(app), {1: [2, 2, 2, 3, 2], 2: [3, 4], 3: [4, 5], 4: [7], 5: [6], 6: [6],
                                                  7: [6], 8: [6], 9: [], 10: []})
        self.assertEqual(RG.projected_ages(12, app), {1: 1, 2: 5, 3: 2, 4: 4, 5: 4, 6: 3, 7: 2, 8: 1, 9: 6, 10: 5})
        for route in (RG.label_exposures_by_walk, RG.label_exposures_from_gaps):
            R, E = RG.pooled(route(EX, 1, 10))
            self.assertEqual((R, E), ({1: 22, 2: 20, 3: 15, 4: 11, 5: 7, 6: 5, 7: 1}, {2: 4, 3: 2, 4: 2, 5: 1, 6: 4, 7: 1}))
        a = RG.log_age_coefficients(R, E)
        self.assertEqual(a, {1: -308, 2: 44, 3: -48, 4: 8, 5: -17, 6: 254, 7: 67})
        self.assertEqual(RG.prime_exponents_by_trial(a), {2: 314, 3: 206, 5: -17, 7: 67})
        self.assertEqual((RG.log_sign_route_1(a), RG.log_sign_route_2(a)), (1, 1))

    def test_bins_of_the_three_real_barrels(self):
        self.assertEqual(RG.bin_edges(35, 7), [1, 2, 3, 5, 8, 13])
        self.assertEqual(RG.bin_edges(20, 1), [4, 8, 12, 20, 32, 52])
        self.assertEqual(RG.bin_edges(47, 7), [2, 3, 5, 7, 11, 18])
        self.assertEqual(RG.bin_ranges([1, 2, 3, 5, 8, 13]),
                         [(1, 1), (2, 2), (3, 3), (4, 5), (6, 8), (9, 13), (14, None)])
        self.assertEqual([RG.bin_of(k, [1, 2, 3, 5, 8, 13]) for k in (1, 2, 3, 4, 5, 6, 13, 14, 99)],
                         [0, 1, 2, 3, 3, 4, 5, 6, 6])
        self.assertEqual(RG.bin_edges(10, 4), [1, 2, 3, 4, 7])           # m = 5/2: 1/2 and 1 both give 1, merged


class Censoring(unittest.TestCase):
    def test_before_first_appearance_is_excluded_and_the_open_stretch_is_at_risk(self):
        draws = [[2], [2], [1], [2], [2], [2]]                          # label 1 first seen at 3; label 3 never
        per = RG.label_exposures_by_walk(draws, 1, 3)
        self.assertEqual(per[1], ({1: 1, 2: 1, 3: 1}, {}))              # ages 1..3 after position 3, no event
        self.assertEqual(per[3], ({}, {}))                              # never seen: no exposure at all
        self.assertEqual(per[2][1], {1: 3, 2: 1})                        # label 2 at 1, 2, 4, 5, 6: gaps 1, 2, 1, 1
        self.assertEqual(per, RG.label_exposures_from_gaps(draws, 1, 3))
        ages = RG.projected_ages(6, RG.appearances(draws, 1, 3))
        self.assertEqual(ages, {1: 4, 2: 1, 3: 7})                       # never seen: W + 1

    def test_windows(self):
        draws = invented(60, 1, 20, 1, 'window')
        app = RG.appearances(draws, 1, 20)
        for w in (1, 7, 30, 60):
            with self.subTest(window=w):
                self.assertEqual(RG.gaps_in_window(app, 60, w), RG.gaps_by_scan(draws, 1, 20, w))
                self.assertEqual(RG.label_exposures_by_walk(draws, 1, 20, w), RG.label_exposures_from_gaps(draws, 1, 20, w))
                start = 60 - w + 1
                for j, p in app.items():          # from scratch: both ends inside the window
                    self.assertEqual(RG.gaps_in_window(app, 60, w)[j], [b - a for a, b in zip(p, p[1:]) if a >= start])
        self.assertEqual(RG.gaps_in_window(app, 60, None), RG.completed_gaps(app))


class TwoRoutesAgree(unittest.TestCase):
    def test_exposures_gaps_and_signs_on_invented_histories(self):
        for barrel in ((1, 35, 7), (1, 20, 1), (1, 47, 7)):
            draws = invented(160, *barrel, seed=str(barrel))
            for W in (52, 104, 160):
                h = draws[:W]
                with self.subTest(barrel=barrel, W=W):
                    a_walk = RG.label_exposures_by_walk(h, barrel[0], barrel[1])
                    self.assertEqual(a_walk, RG.label_exposures_from_gaps(h, barrel[0], barrel[1]))
                    app = RG.appearances(h, barrel[0], barrel[1])
                    self.assertEqual(RG.gaps_in_window(app, W, None), RG.gaps_by_scan(h, barrel[0], barrel[1]))
                    a = RG.log_age_coefficients(*RG.pooled(a_walk))
                    self.assertEqual(sum(a.values()), 0)
                    self.assertEqual(RG.prime_exponents_by_trial(a), RG.prime_exponents_by_sieve(a))
                    self.assertEqual(RG.log_sign_route_1(a), RG.log_sign_route_2(a))
                    self.assertEqual(RG.log_sign_route_1(a), decimal_sign(a))

    def test_counts_from_scratch(self):
        draws = invented(80, seed='scratch')
        R, E = RG.pooled(RG.label_exposures_by_walk(draws, 1, 35))
        n_known = sum(80 - p[0] for p in RG.appearances(draws, 1, 35).values() if p)   # draws after first appearance
        self.assertEqual(sum(R.values()), n_known)
        self.assertEqual(sum(E.values()), sum(len(p) - 1 for p in RG.appearances(draws, 1, 35).values() if p))


class LogSign(unittest.TestCase):
    def test_ex069_witness_is_negative(self):
        a = RG.log_age_coefficients(*RG.pooled(RG.label_exposures_by_walk(ex069_witness(), 1, 35)))
        self.assertEqual((RG.log_sign_route_1(a), RG.log_sign_route_2(a), decimal_sign(a)), (-1, -1, -1))

    def test_exact_zero_in_both_routes_and_bounds_alone_refuse(self):
        a = RG.log_age_coefficients(*RG.pooled(RG.label_exposures_by_walk(ZERO_WITNESS, 1, 2)))
        self.assertEqual(a, {1: 6, 2: -12, 3: 0, 4: 6})
        self.assertEqual(RG.prime_exponents_by_trial(a), {})
        self.assertEqual(RG.prime_exponents_by_sieve(a), {})
        self.assertEqual((RG.log_sign_route_1(a), RG.log_sign_route_2(a)), (0, 0))
        with self.assertRaises(ValueError):                              # refused at the cap, never guessed
            RG.bounded_sign({k: c for k, c in a.items() if c})

    def test_every_small_coefficient_vector(self):
        zeros = 0
        for i, cs in enumerate(itertools.product(range(-2, 3), repeat=6)):
            a = dict(enumerate(cs, 1))
            e = RG.prime_exponents_by_trial(a)
            self.assertEqual(e, RG.prime_exponents_by_sieve(a))
            if not e:
                zeros += 1
                self.assertEqual((RG.log_sign_route_1(a), RG.log_sign_route_2(a)), (0, 0))
            elif i % 97 == 0:
                self.assertEqual(RG.log_sign_route_1(a), RG.log_sign_route_2(a))
                self.assertEqual(RG.log_sign_route_1(a), decimal_sign(a))
        self.assertEqual(zeros, 65)

    def test_ln_bounds_bracket_the_logarithm(self):
        for k in (1, 2, 3, 7, 64, 97, 433):
            lo, hi = RG.ln_bounds(k, 8)
            with localcontext() as ctx:
                ctx.prec = 60
                v = Decimal(k).ln()
            self.assertTrue(Decimal(lo.numerator) / Decimal(lo.denominator) <= v <= Decimal(hi.numerator) / Decimal(hi.denominator))
        self.assertEqual(RG.ln_bounds(1, 8), (Fr(0), Fr(0)))


class Refusals(unittest.TestCase):
    def test_bad_inputs_are_refused(self):
        for call in (lambda: RG.appearances([[1, 1]], 1, 5), lambda: RG.appearances([[6]], 1, 5),
                     lambda: RG.appearances([[1]], 0, 5), lambda: RG.label_exposures_by_walk(EX, 1, 10, 0),
                     lambda: RG.label_exposures_from_gaps(EX, 1, 10, 13), lambda: RG.gaps_by_scan(EX, 1, 10, 13),
                     lambda: RG.gaps_in_window(RG.appearances(EX, 1, 10), 12, 0), lambda: RG.ln_bounds(0, 8)):
            with self.assertRaises(ValueError):
                call()


class StaticGuards(unittest.TestCase):
    def test_exact_arithmetic_only_and_no_outside_access(self):
        text = (ROOT / 'src' / 'methods' / '_common' / 'recurrence_gaps.py').read_text('utf-8')
        for word in ('import math', 'float(', '**0.5', '** 0.5', 'numpy', 'scipy', 'open(', 'read_bytes', 'write_bytes',
                     'import os', 'subprocess', 'game_draws_reader', 'source' + '_data', 'contract_', 'random', 'decimal'):
            self.assertNotIn(word, text, f'recurrence_gaps.py mentions {word}')


if __name__ == '__main__':
    unittest.main()
