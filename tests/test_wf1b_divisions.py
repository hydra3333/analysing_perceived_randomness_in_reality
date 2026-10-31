"""WF-1B tests: divisions, match records and fair-draw moments (R3 17.4, 17.8; R2 2.5). OFFLINE, invented numbers.

R3 tests covered here: MRT-01 (division tables, counts and published odds), MRT-02 (exhaustive and exclusive
classification; invalid s rejected), MRT-05 in part (the supplementaries never leave the match-record step).
Agreement with the installed `validate_score_record` is checked for every classification cell.
Nothing here reads a repository data file or a real draw.
"""
from __future__ import annotations

import math
import random
import sys
import unittest
from fractions import Fraction
from math import comb
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / 'src'
sys.path.insert(0, str(_SRC))
sys.path.insert(0, str(_SRC / 'methods'))

from evaluation import divisions, measures, numerics  # noqa: E402,F401
from _common.contract_receipts import track_id, validate_score_record  # noqa: E402

DV = divisions
PB, OZ = 'POWERBALL', 'OZLOTTO'

# R3 17.4.2 and 17.4.3, copied from the text.
R3_PB = {1: Fraction(1, 134490400), 2: Fraction(19, 134490400), 3: Fraction(49, 33622600),
         4: Fraction(931, 33622600), 5: Fraction(3969, 67245200), 6: Fraction(5733, 6724520),
         7: Fraction(75411, 67245200), 8: Fraction(28665, 5379616), 9: Fraction(51597, 3362260)}
R3_PB_ABOUT = {1: 134490400, 2: 7078442, 3: 686176, 4: 36115, 5: 16943, 6: 1173, 7: 892, 8: 188}
R3_PB_BITS = {1: 27.003, 2: 22.755, 3: 19.388, 4: 15.140, 5: 14.048, 6: 10.196, 7: 9.800, 8: 7.552, 9: 6.026}
R3_PB_COUNTS = (1, 19, 196, 3724, 7938, 114660, 150822, 716625, 2063880)
R3_OZ = {1: Fraction(1, 62891499), 2: Fraction(7, 20963833), 3: Fraction(259, 62891499),
         4: Fraction(798, 20963833), 5: Fraction(4662, 20963833), 6: Fraction(345800, 62891499),
         7: Fraction(887075, 62891499)}
R3_OZ_ABOUT = {1: 62891499, 2: 2994833, 3: 242824, 4: 26270, 5: 4497, 6: 182, 7: 71}
R3_OZ_PUBLISHED = {1: 62891499, 2: 2994834, 3: 242825, 4: 26271, 5: 4497, 6: 182, 7: 71}
R3_OZ_BITS = {1: 25.906, 2: 21.514, 3: 17.890, 4: 14.681, 5: 12.135, 6: 7.507, 7: 6.148}
R3_OZ_COUNTS = (1, 21, 259, 2394, 13986, 345800, 887075)
R3_AT_LEAST = {PB: (1, 0.823922, 0.431748, 0.124830, 0.0182608, 0.00120975, 2.92958e-5, 1.48709e-7),
               OZ: (1, 0.703560, 0.276337, 0.0566231, 0.00576327, 0.000264917, 4.46801e-6, 1.59004e-8)}


def sig6(x: float) -> float:
    return float(f'{x:.6g}')


def _div(game, m, x):
    if game == PB:
        return DV.division(game, m, powerball_match=x)
    return DV.division(game, m, supplementary_matches=x)


class DivisionTables(unittest.TestCase):
    """MRT-01."""

    def test_exact_fractions_equal_r3(self):
        self.assertEqual(DV.division_probabilities(PB), R3_PB)
        self.assertEqual(DV.division_probabilities(OZ), R3_OZ)
        for g, tab in ((PB, R3_PB), (OZ, R3_OZ)):
            for d, p in tab.items():
                self.assertIs(type(DV.division_probability(g, d)), Fraction)
                self.assertEqual(DV.division_probability(g, d), p)

    def test_integer_counts_equal_r3(self):
        self.assertEqual(DV.division_outcome_counts(PB), R3_PB_COUNTS)
        self.assertEqual(DV.division_outcome_counts(OZ), R3_OZ_COUNTS)
        self.assertEqual(DV.outcome_total(PB), 134490400)
        self.assertEqual(DV.outcome_total(OZ), 62891499)
        self.assertEqual(comb(35, 7), 6724520)

    def test_probabilities_sum_to_one(self):
        for g in DV.GAMES:
            total = sum(DV.division_probabilities(g).values(), Fraction(0)) + DV.no_division_probability(g)
            self.assertEqual(total, 1)
            self.assertEqual(sum(DV.main_match_probabilities(g), Fraction(0)), 1)

    def test_any_division(self):
        self.assertEqual(DV.any_division_probability(PB), Fraction(611573, 26898080))
        self.assertEqual(DV.any_division_probability(OZ), Fraction(416512, 20963833))
        self.assertEqual(round(float(1 / DV.any_division_probability(PB)), 2), 43.98)
        self.assertEqual(round(float(1 / DV.any_division_probability(OZ)), 2), 50.33)

    def test_about_one_in_and_bits(self):
        for d, about in R3_PB_ABOUT.items():
            self.assertEqual(round(1 / R3_PB[d]), about, d)          # nearest whole number
        self.assertEqual(round(float(1 / R3_PB[9]), 1), 65.2)       # PD9 to one decimal
        for d, b in R3_PB_BITS.items():
            self.assertEqual(round(-math.log2(R3_PB[d]), 3), b, d)
        for d, about in R3_OZ_ABOUT.items():
            self.assertEqual(round(1 / R3_OZ[d]), about, d)
        for d, b in R3_OZ_BITS.items():
            self.assertEqual(round(-math.log2(R3_OZ[d]), 3), b, d)

    def test_published_odds(self):
        # Powerball rule 9.4 odds are the rounded values above. Lotterywest's published Oz odds equal the exact
        # value rounded UP for OD2-OD7 (R3 17.4.3); OD1 is exact.
        for d in range(2, 8):
            inv = 1 / R3_OZ[d]
            self.assertEqual(-((-inv.numerator) // inv.denominator), R3_OZ_PUBLISHED[d], d)
        self.assertEqual(1 / R3_OZ[1], R3_OZ_PUBLISHED[1])

    def test_formula_per_cell(self):
        # Powerball: P(m) x P(b), P(b = 1) = 1/20 independent of m (R3 17.4.2).
        pm = DV.main_match_probabilities(PB)
        for m, b in DV.classification_cells(PB):
            p = pm[m] * (Fraction(1, 20) if b else Fraction(19, 20))
            self.assertEqual(Fraction(DV.cell_count(PB, m, b), DV.outcome_total(PB)), p)
        # Oz Lotto: summing P(m, s) over s gives the hypergeometric main law C(7,m) C(40,7-m) / C(47,7).
        om = DV.main_match_probabilities(OZ)
        for m in range(8):
            tot = sum(DV.cell_count(OZ, m, s) for s in range(min(3, 7 - m) + 1))
            self.assertEqual(Fraction(tot, comb(47, 7)), om[m])
            self.assertEqual(om[m], Fraction(comb(7, m) * comb(40, 7 - m), comb(47, 7)))


class Classification(unittest.TestCase):
    """MRT-02 and agreement with the installed score-record validator."""

    def test_exhaustive_and_exclusive(self):
        expected_pb = {(7, 1): 1, (7, 0): 2, (6, 1): 3, (6, 0): 4, (5, 1): 5, (4, 1): 6, (5, 0): 7, (3, 1): 8,
                       (2, 1): 9}
        cells = DV.classification_cells(PB)
        self.assertEqual(len(cells), 16)
        for m, b in cells:
            self.assertEqual(_div(PB, m, b), expected_pb.get((m, b), 0))
        expected_oz = {}
        for m, s in DV.classification_cells(OZ):
            expected_oz[(m, s)] = (1 if m == 7 else 2 if (m == 6 and s == 1) else 3 if (m == 6 and s == 0) else
                                   4 if (m == 5 and s >= 1) else 5 if (m == 5 and s == 0) else 6 if m == 4 else
                                   7 if (m == 3 and s >= 1) else 0)
            self.assertEqual(_div(OZ, m, s), expected_oz[(m, s)])
        self.assertEqual(len(expected_oz), 4 + 4 + 4 + 4 + 4 + 3 + 2 + 1)
        # every division is reached by at least one cell, and each cell maps to exactly one division
        for g, exp in ((PB, expected_pb), (OZ, expected_oz)):
            reached = {_div(g, m, x) for m, x in DV.classification_cells(g)}
            self.assertEqual(reached, set(range(DV.DIVISION_COUNT[g] + 1)))

    def test_invalid_inputs_rejected(self):
        bad = [
            (PB, dict(main_matches=8, powerball_match=0)), (PB, dict(main_matches=3, powerball_match=2)),
            (PB, dict(main_matches=3)), (PB, dict(main_matches=3, powerball_match=True)),
            (PB, dict(main_matches=3, powerball_match=1, supplementary_matches=0)),
            (OZ, dict(main_matches=5, supplementary_matches=3)),       # s > 7 - m
            (OZ, dict(main_matches=7, supplementary_matches=1)),       # s > 7 - m
            (OZ, dict(main_matches=6, supplementary_matches=2)),       # s > 7 - m
            (OZ, dict(main_matches=0, supplementary_matches=4)),       # s > 3
            (OZ, dict(main_matches=2, supplementary_matches=-1)),
            (OZ, dict(main_matches=2)), (OZ, dict(main_matches=2, supplementary_matches=0, powerball_match=0)),
            (OZ, dict(main_matches=2.0, supplementary_matches=0)), ('LOTTO', dict(main_matches=2)),
        ]
        for game, kw in bad:
            with self.assertRaises(ValueError, msg=(game, kw)):
                DV.division(game, **kw)

    def _record(self, game, m, x, d):
        s = {'schema': 'POST_OUTCOME_SCORE_RECORD_V1', 'game_id': game, 'draw_number': 1300 if game == PB else 1500,
             'track_id': track_id(game, 'E_2', 'SYNTHETIC_CONTRACT_PROBE', 'TOP', 'WF'), 'mode': 'WF',
             'method_revision': '1', 'forecast_content_digest': 'c' * 64, 'freeze_receipt_digest': 'd' * 64,
             'drawn_main': [1, 2, 3, 4, 5, 6, 7], 'main_matches': m, 'division': d,
             'evaluator_version': 'SYNTHETIC_EVAL_V1'}
        if game == PB:
            s.update(drawn_powerball=3, powerball_match=x)
        else:
            s.update(supplementary_matches=x)
        return s

    def test_agrees_with_installed_validator(self):
        for g in DV.GAMES:
            for m, x in DV.classification_cells(g):
                validate_score_record(self._record(g, m, x, _div(g, m, x)))
            # the validator's own ranges are exactly the classifier's
            with self.assertRaises(ValueError):
                validate_score_record(self._record(g, 0, 0, DV.DIVISION_COUNT[g] + 1))
        with self.assertRaises(ValueError):
            validate_score_record(self._record(OZ, 6, 2, 0))
        with self.assertRaises(ValueError):
            DV.division(OZ, 6, supplementary_matches=2)


class MatchRecords(unittest.TestCase):
    """The per-draw match record (R3 17.4.1) and the supplementary rule (R2 2.5; MRT-05 in part)."""

    def test_powerball_examples(self):
        ticket = [2, 7, 11, 18, 24, 30, 35]
        drawn = [2, 5, 11, 12, 19, 26, 30]
        self.assertEqual(DV.match_record(PB, ticket, 4, drawn, 4),
                         {'main_matches': 3, 'powerball_match': 1, 'division': 8})
        self.assertEqual(DV.match_record(PB, ticket, 4, drawn, 5),
                         {'main_matches': 3, 'powerball_match': 0, 'division': 0})
        self.assertEqual(DV.match_record(PB, ticket, 9, ticket, 9),
                         {'main_matches': 7, 'powerball_match': 1, 'division': 1})
        self.assertEqual(DV.match_record(PB, ticket, 9, list(reversed(ticket)), 1)['division'], 2)

    def test_oz_examples_and_supplementaries_never_returned(self):
        ticket = [1, 2, 3, 4, 5, 6, 40]
        drawn = [1, 2, 3, 4, 5, 20, 21]
        supps = [6, 41, 47]
        rec = DV.match_record(OZ, ticket, None, drawn, supps)
        self.assertEqual(rec, {'main_matches': 5, 'supplementary_matches': 1, 'division': 4})
        self.assertEqual(set(rec), {'main_matches', 'supplementary_matches', 'division'})
        rec2 = DV.match_record(OZ, ticket, None, drawn, [30, 41, 47])
        self.assertEqual(rec2, {'main_matches': 5, 'supplementary_matches': 0, 'division': 5})
        rec3 = DV.match_record(OZ, [1, 2, 3, 30, 41, 46, 47], None, drawn, [30, 41, 47])
        self.assertEqual(rec3, {'main_matches': 3, 'supplementary_matches': 3, 'division': 7})

    def test_invalid_records_rejected(self):
        t = [1, 2, 3, 4, 5, 6, 7]
        for args in [(PB, t, 21, t, 1), (PB, t, 1, t, 0), (PB, [1, 1, 2, 3, 4, 5, 6], 1, t, 1),
                     (PB, [1, 2, 3, 4, 5, 6, 36], 1, t, 1), (PB, t[:6], 1, t, 1), (PB, t, None, t, 1),
                     (OZ, t, 1, t, [8, 9, 10]), (OZ, t, None, t, [7, 9, 10]), (OZ, t, None, t, [8, 9]),
                     (OZ, t, None, t, [8, 8, 9]), (OZ, t, None, [1, 2, 3, 4, 5, 6, 48], [8, 9, 10])]:
            with self.assertRaises(ValueError, msg=args):
                DV.match_record(*args)

    def test_random_invented_draws_agree_with_direct_counting(self):
        rng = random.Random(20261031)
        for game in DV.GAMES:
            n = DV.MAIN_POOL[game]
            for _ in range(2000):
                ticket = rng.sample(range(1, n + 1), 7)
                if game == PB:
                    drawn = rng.sample(range(1, 36), 7)
                    tpb, dpb = rng.randint(1, 20), rng.randint(1, 20)
                    rec = DV.match_record(game, ticket, tpb, drawn, dpb)
                    m, x = len(set(ticket) & set(drawn)), int(tpb == dpb)
                    self.assertEqual(rec['powerball_match'], x)
                else:
                    ten = rng.sample(range(1, 48), 10)
                    drawn, supps = ten[:7], ten[7:]
                    rec = DV.match_record(game, ticket, None, drawn, supps)
                    m, x = len(set(ticket) & set(drawn)), len(set(ticket) & set(supps))
                    self.assertEqual(rec['supplementary_matches'], x)
                self.assertEqual(rec['main_matches'], m)
                self.assertEqual(rec['division'], _div(game, m, x))


class FairMoments(unittest.TestCase):
    """R3 17.4.4."""

    def test_means_and_variances(self):
        self.assertEqual(DV.MEAN0[PB], Fraction(7, 5))
        self.assertEqual(DV.MEAN0[OZ], Fraction(49, 47))
        self.assertEqual(DV.VAR0[PB], Fraction(392, 425))
        self.assertEqual(DV.VAR0[OZ], Fraction(39200, 50807))
        self.assertEqual(round(float(DV.VAR0[PB]), 5), 0.92235)
        self.assertEqual(round(math.sqrt(DV.VAR0[PB]), 5), 0.96039)
        self.assertEqual(round(float(DV.VAR0[OZ]), 5), 0.77155)
        self.assertEqual(round(math.sqrt(DV.VAR0[OZ]), 5), 0.87838)
        self.assertEqual(round(float(DV.MEAN0[OZ]), 5), 1.04255)
        self.assertEqual(DV.PB_HIT_PROBABILITY, Fraction(1, 20))
        self.assertEqual(DV.PB_HIT_VARIANCE, Fraction(475, 10000))
        fm = DV.fair_moments(PB)
        self.assertEqual((fm['mean0'], fm['var0'], fm['pb_hit_probability']),
                         (Fraction(7, 5), Fraction(392, 425), Fraction(1, 20)))
        self.assertNotIn('pb_hit_probability', DV.fair_moments(OZ))

    def test_tail_rows(self):
        for g in DV.GAMES:
            got = DV.fair_moments(g)['p_main_at_least']
            for m in range(8):
                self.assertEqual(sig6(float(got[m])), R3_AT_LEAST[g][m], (g, m))
            self.assertEqual(DV.main_match_at_least(g, 8), 0)

    def test_hypergeometric_formula(self):
        for g, other in ((PB, 28), (OZ, 40)):
            n = DV.MAIN_POOL[g]
            self.assertEqual(DV.main_match_probabilities(g),
                             tuple(Fraction(comb(7, m) * comb(other, 7 - m), comb(n, 7)) for m in range(8)))
            self.assertEqual(sum(DV.main_match_weights(g)), comb(n, 7))


if __name__ == '__main__':
    unittest.main()
