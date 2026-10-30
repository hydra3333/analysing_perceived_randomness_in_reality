"""The shared helper _common/occurrence_counts.py, revision 1 (wave 1 design note v0.1r1 section 11). OFFLINE.

Pure arithmetic on invented draws: no data file, no process, no repository write. Expected values are the
design note's worked examples (computed by its reference script) or are recomputed here from scratch.
"""
from __future__ import annotations

from fractions import Fraction as Fr
import hashlib
import unittest

from e2r_fixtures import ROOT
from _common import occurrence_counts as OC

EX = [[1, 2], [1, 3], [2, 4], [1, 5]]          # the design note's example: 5 labels, K = 2, oldest first


def invented(n, low=1, high=35, k=7, seed='oc'):
    """n invented draws of k distinct labels from low..high, deterministic. Never a real result."""
    out = []
    for i in range(n):
        pool = list(range(low, high + 1))
        pool.sort(key=lambda j: hashlib.sha256(f'{seed}:{i}:{j}'.encode()).digest())
        out.append(sorted(pool[:k]))
    return out


class WorkedExamples(unittest.TestCase):
    def test_window_counts(self):
        self.assertEqual(OC.window_counts(EX, 1, 5, 2), {1: 1, 2: 1, 3: 0, 4: 1, 5: 1})
        self.assertEqual(OC.window_counts(EX, 1, 5, 4), {1: 3, 2: 2, 3: 1, 4: 1, 5: 1})

    def test_decayed_counts(self):
        want = {1: Fr(11, 8), 2: Fr(5, 8), 3: Fr(1, 4), 4: Fr(1, 2), 5: Fr(1)}
        self.assertEqual(OC.decayed_counts(EX, 1, 5, Fr(1, 2)), want)
        self.assertEqual(OC.decayed_counts_by_recursion(EX, 1, 5, Fr(1, 2)), want)

    def test_period_counts_newest_period_complete_and_remainder_dropped(self):
        five = [[3, 4]] + EX                       # 5 draws, P = 2: the oldest draw is the unused remainder
        want = {1: [2, 1], 2: [1, 1], 3: [1, 0], 4: [0, 1], 5: [0, 1]}
        self.assertEqual(OC.period_counts(five, 1, 5, 2), want)
        self.assertEqual(OC.period_counts_by_index(five, 1, 5, 2), want)


class TwoRoutesAgree(unittest.TestCase):
    def test_every_function_equals_its_second_form(self):
        for barrel in ((1, 35, 7), (1, 20, 1), (1, 47, 7)):
            draws = invented(120, *barrel, seed=str(barrel))
            for S in (1, 13, 52, 120):
                with self.subTest(barrel=barrel, S=S):
                    self.assertEqual(OC.window_counts(draws, barrel[0], barrel[1], S),
                                     OC.window_counts_by_prefix(draws, barrel[0], barrel[1], S))
            for lam in (Fr(5, 6), Fr(18, 19), Fr(37, 38), Fr(74, 75)):
                with self.subTest(barrel=barrel, lam=lam):
                    self.assertEqual(OC.decayed_counts(draws, barrel[0], barrel[1], lam),
                                     OC.decayed_counts_by_recursion(draws, barrel[0], barrel[1], lam))
            for P in (1, 13, 26, 52, 120):
                with self.subTest(barrel=barrel, P=P):
                    self.assertEqual(OC.period_counts(draws, barrel[0], barrel[1], P),
                                     OC.period_counts_by_index(draws, barrel[0], barrel[1], P))


class Identities(unittest.TestCase):
    def test_counts_add_up(self):
        draws = invented(100)
        for S in (1, 37, 100):
            self.assertEqual(sum(OC.window_counts(draws, 1, 35, S).values()), 7 * S)
        for P in (13, 26, 52):
            pc = OC.period_counts(draws, 1, 35, P)
            for b in range(100 // P):
                self.assertEqual(sum(c[b] for c in pc.values()), 7 * P)       # each period holds K*P selections
        lam = Fr(18, 19)
        total = sum(OC.decayed_counts(draws, 1, 35, lam).values())
        self.assertEqual(total, 7 * sum(lam ** a for a in range(100)))

    def test_against_a_from_scratch_count(self):
        draws = invented(60, seed='scratch')
        for S in (5, 60):
            for j in (1, 17, 35):
                self.assertEqual(OC.window_counts(draws, 1, 35, S)[j], sum(1 for d in draws[-S:] if j in d))


class Refusals(unittest.TestCase):
    def test_bad_inputs_are_refused(self):
        for call in (lambda: OC.window_counts(EX, 1, 5, 0), lambda: OC.window_counts(EX, 1, 5, 5),
                     lambda: OC.window_counts([[1, 1]], 1, 5, 1),                 # a repeated label
                     lambda: OC.window_counts([[6]], 1, 5, 1),                    # out of range
                     lambda: OC.decayed_counts(EX, 1, 5, Fr(1)), lambda: OC.decayed_counts(EX, 1, 5, 0.5),
                     lambda: OC.decayed_counts_by_recursion(EX, 1, 5, Fr(0)),
                     lambda: OC.period_counts(EX, 1, 5, 5), lambda: OC.period_counts_by_index(EX, 1, 5, 0),
                     lambda: OC.window_counts(EX, 0, 5, 1)):
            with self.assertRaises(ValueError):
                call()


class StaticGuards(unittest.TestCase):
    def test_exact_arithmetic_only_and_no_outside_access(self):
        text = (ROOT / 'src' / 'methods' / '_common' / 'occurrence_counts.py').read_text('utf-8')
        for word in ('import math', 'float(', 'numpy', 'scipy', 'open(', 'read_bytes', 'write_bytes', 'import os',
                     'subprocess', 'game_draws_reader', 'source' + '_data', 'contract_', 'random'):
            self.assertNotIn(word, text, f'occurrence_counts.py mentions {word}')


if __name__ == '__main__':
    unittest.main()
