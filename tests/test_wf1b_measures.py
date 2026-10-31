"""WF-1B tests: the R3 stage-2 measures MR0, MR1/MR1-T, MR4, MR5, MR7, MR16 and the league-table ranks.
OFFLINE, invented per-target codes only (no repository data file, no real draw).

R3 17.14 tests covered here (in full or for this module's part): MRT-03 (k = 0 gives 0 excess sigma; the deficit
example; confidence never "100%"), MRT-07 (planted hit-rate tilt detected by MR4 and MR7; null tracks near nominal),
MRT-08 (determinism of the measure outputs), MRT-09 (tie display), MRT-10 (MR5 per-target values), MRT-12 (count
and float fields), MRT-16 (d) and (c) labels (SELECTION_UNVERIFIED on an incomplete grid; MR5's N1 figure only a
reference), MRT-19 (MR7 against an independent exact oracle), MRT-22 (MR16 intervals against an independent exact
implementation; k_3 and powers of R3's reference table; no double count with MR4), MRT-23 (analysis units and
channels).
"""
from __future__ import annotations

import math
import random
import sys
import unittest
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from evaluation import divisions, measures, numerics  # noqa: E402

DV, MS, NU = divisions, measures, numerics
PB, OZ = 'POWERBALL', 'OZLOTTO'


# ---------------------------------------------------------------- independent oracles (test-only)

def _pmf_sum(n, p, js):
    return sum((comb(n, j) * p ** j * (1 - p) ** (n - j) for j in js), Fraction(0))


def oracle_upper(n, p, k):
    """P(X >= k), exact; sums whichever side has fewer terms."""
    if k <= 0:
        return Fraction(1)
    if n - k + 1 <= k:
        return _pmf_sum(n, p, range(k, n + 1))
    return 1 - _pmf_sum(n, p, range(0, k))


def oracle_lower(n, p, k):
    """P(X <= k), exact."""
    return 1 - oracle_upper(n, p, k + 1) if k < n else Fraction(1)


def oracle_mr7(game, n, s):
    """Distribution of the sum of n independent one-draw main-match counts, by direct Fraction convolution."""
    pm = DV.main_match_probabilities(game)
    dist = {0: Fraction(1)}
    for _ in range(n):
        new = {}
        for tot, pr in dist.items():
            for m in range(8):
                new[tot + m] = new.get(tot + m, Fraction(0)) + pr * pm[m]
        dist = new
    up = sum((pr for tot, pr in dist.items() if tot >= s), Fraction(0))
    lo = sum((pr for tot, pr in dist.items() if tot <= s), Fraction(0))
    return up, lo


def oracle_cp(k, n, conf=Fraction(95, 100)):
    """Clopper-Pearson by bisection (60 halvings) on exact Fraction lower tails, summed directly."""
    alpha = (1 - conf) / 2

    def solve(f):  # f decreasing in q on [0, 1]: find q with f(q) = alpha
        lo, hi = Fraction(0), Fraction(1)
        for _ in range(60):
            mid = (lo + hi) / 2
            if f(mid) > alpha:
                lo = mid
            else:
                hi = mid
        return float((lo + hi) / 2)
    # lower bound q_L: P(X >= k | q_L) = alpha. With r = 1 - q, P(X >= k | q) = P(Y <= n - k | r) for
    # Y ~ Binomial(n, r), which decreases in r; so solve for r and return 1 - r.
    lower = 0.0 if k == 0 else 1 - solve(lambda r: oracle_lower(n, r, n - k))
    upper = 1.0 if k == n else solve(lambda q: oracle_lower(n, q, k))          # P(X <= k | q) = alpha
    return lower, upper


def tracks(game, codes, first=1286):
    """Per-target dicts from (m, b) or (m, s) codes, ascending draw numbers."""
    out = []
    for i, (m, x) in enumerate(codes):
        t = {'draw_number': first + i, 'main_matches': m}
        if game == PB:
            t.update(powerball_match=x, division=DV.division(game, m, powerball_match=x))
        else:
            t.update(supplementary_matches=x, division=DV.division(game, m, supplementary_matches=x))
        out.append(t)
    return out


def fair_codes(game, n, rng):
    out = []
    for _ in range(n):
        ticket = set(range(1, 8))
        if game == PB:
            drawn = set(rng.sample(range(1, 36), 7))
            out.append((len(ticket & drawn), int(rng.randint(1, 20) == 1)))
        else:
            ten = rng.sample(range(1, 48), 10)
            out.append((len(ticket & set(ten[:7])), len(ticket & set(ten[7:]))))
    return out


ALL = (MS.mr0, MS.mr1, MS.mr4, MS.mr7, MS.mr16)


class Sigma(unittest.TestCase):
    """MRT-03 (the parts that run through the measures)."""

    def test_zero_wins_zero_excess_and_deficit_example(self):
        res = MS.mr4(PB, tracks(PB, [(0, 0)] * 291), 'GRID_COMPLETE')
        x9 = res['sub_measures']['MR4.X.9']
        self.assertEqual(x9['k_S'], 0)
        blk = x9['significance']
        self.assertEqual(blk['P_up'], 1)
        self.assertEqual(blk['Z_plus']['sigma'], 0.0)
        self.assertEqual(blk['sigma_level'], 0)
        self.assertEqual(blk['P_lo'], (1 - Fraction(51597, 3362260)) ** 291)
        self.assertEqual(float(f"{float(blk['P_lo']):.6g}"), 0.0111058)
        self.assertAlmostEqual(blk['Z_minus']['sigma'], 2.28673, delta=5e-6)
        self.assertEqual(blk['label'], 'EXACT_LOCAL')
        pd9 = MS.mr16(PB, tracks(PB, [(0, 0)] * 291), 'GRID_COMPLETE')['sub_measures']['MR16.PD9']
        self.assertEqual(pd9['significance']['Z_plus']['sigma'], 0.0)
        self.assertEqual(pd9['interval'][0], 0)
        m7 = MS.mr7(PB, tracks(PB, [(0, 0)] * 40), 'GRID_COMPLETE')['sub_measures']
        self.assertEqual(m7['MR7.MAIN']['significance']['Z_plus']['sigma'], 0.0)
        self.assertEqual(m7['MR7.PB']['significance']['Z_plus']['sigma'], 0.0)

    def test_confidence_rounded_down_never_100(self):
        self.assertEqual(MS.confidence_display(Fraction('0.00134990')), '99.86501%')
        self.assertEqual(MS.confidence_display(Fraction('0.158655')), '84.13450%')
        self.assertEqual(MS.confidence_display(Fraction(1, 10 ** 40)), '99.99999%')
        self.assertEqual(MS.confidence_display(Fraction(1)), '0.00000%')
        self.assertEqual(MS.confidence_display(Fraction(1, 10 ** 12), 9), '99.999999999%')
        blk = MS.mr4(PB, tracks(PB, [(7, 1)] * 3), 'GRID_COMPLETE')['sub_measures']['MR4.X.1']['significance']
        self.assertFalse(MS.confidence_display(blk['P_up']).startswith('100'))
        self.assertEqual(blk['confidence_pct'], 100 * (1 - blk['P_up']))
        self.assertEqual(blk['sigma_level'], '>= 6')


class MR0andMR1(unittest.TestCase):

    def test_mr1_constants_equal_r3(self):
        self.assertEqual(round(float(MS.MR1_E0[PB]), 6), 0.153679)
        self.assertEqual(round(float(MS.MR1_SD[PB]), 6), 1.025914)
        self.assertEqual(round(float(MS.MR1_E0[OZ]), 6), 0.131326)
        self.assertEqual(round(float(MS.MR1_SD[OZ]), 6), 0.931722)
        self.assertEqual(round(float(MS.BITS[PB][9]), 1), 6.0)
        self.assertEqual(round(float(MS.BITS[PB][1]), 1), 27.0)

    def test_mr1_values_and_labels(self):
        codes = [(2, 1)] * 3 + [(3, 1)] + [(7, 0)] + [(0, 0)] * 45      # 3 PD9, 1 PD8, 1 PD2 in 50
        res = MS.mr1(PB, tracks(PB, codes), 'GRID_COMPLETE')
        s1, st = res['sub_measures']['MR1'], res['sub_measures']['MR1-T']
        bits = 3 * -math.log2(Fraction(51597, 3362260)) + -math.log2(Fraction(28665, 5379616)) + \
            -math.log2(Fraction(19, 134490400))
        self.assertAlmostEqual(s1['MR1'], bits / 50, places=12)
        self.assertAlmostEqual(s1['difference'], bits / 50 - 0.1536790, places=6)
        z = (bits - 50 * float(MS.MR1_E0[PB])) / (math.sqrt(50) * float(MS.MR1_SD[PB]))
        self.assertAlmostEqual(s1['approx']['Z'], z, places=10)
        self.assertEqual(s1['approx']['label'], 'APPROX_UNCALIBRATED')
        self.assertEqual(s1['n1']['label'], 'N1_NOT_RUN')
        self.assertIsNone(s1['n1']['P_up'])
        self.assertEqual(s1['calibration'], 'NOT_A_P_VALUE')
        self.assertEqual(s1['significance_key'], s1['approx']['Z_plus']['sigma'])
        self.assertEqual(st['MR1-T'], Fraction(7, 100) / 50)
        self.assertEqual(st['calibration'], 'NOT_A_P_VALUE')
        # an N1 p-value, when passed in, is N1_CALIBRATED on a complete grid and SELECTION_UNVERIFIED otherwise
        n1 = {'p_up': Fraction(12, 10001), 'ci': (0.0006, 0.002), 'R': 10000}
        c = MS.mr1(PB, tracks(PB, codes), 'GRID_COMPLETE', n1=n1)['sub_measures']['MR1']
        self.assertEqual(c['n1']['label'], 'N1_CALIBRATED')
        self.assertEqual(c['significance_key'], NU.z_plus(Fraction(12, 10001))['sigma'])
        u = MS.mr1(PB, tracks(PB, codes), 'GRID_INCOMPLETE', n1=n1)['sub_measures']['MR1']
        self.assertEqual(u['n1']['label'], 'SELECTION_UNVERIFIED')
        self.assertEqual(u['approx']['label'], 'APPROX_UNCALIBRATED')
        self.assertIn('SELECTION_UNVERIFIED', u['flags'])

    def test_mr1t_weights(self):
        codes = [(7, 1)] * 2 + [(7, 0)] + [(6, 1)] * 4 + [(0, 0)] * 3
        st = MS.mr1(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']['MR1-T']
        self.assertEqual(st['MR1-T'], (Fraction(90, 100) * 2 + Fraction(7, 100) + Fraction(3, 100) * 4) / 10)

    def test_mr1_key_is_exact(self):
        k1 = MS.MR1Key(PB, (0, 0, 0, 0, 0, 0, 0, 0, 1), 100)
        k2 = MS.MR1Key(PB, (0, 0, 0, 0, 0, 0, 0, 0, 2), 200)
        self.assertTrue(k1 == k2)
        self.assertFalse(k1 < k2 or k1 > k2)
        # design 7.4's pair: replicate >= observed is False
        obs = MS.MR1Key(PB, (0, 0, 0, 0, 0, 1, 0, 3, 4), 291)
        rep = MS.MR1Key(PB, (0, 0, 0, 0, 1, 0, 0, 0, 5), 291)
        self.assertFalse(rep >= obs)
        self.assertEqual(rep < obs, rep.value() < obs.value())
        # the exact fallback path: a nonzero exponent vector whose decimal value is exactly zero cannot occur
        # with these primes, but equal keys reached through it still compare equal
        self.assertEqual(MS.MR1Key(OZ, (0,) * 7, 5), MS.MR1Key(OZ, (0,) * 7, 9))
        with self.assertRaises(TypeError):
            _ = MS.MR1Key(PB, (0,) * 9, 5) < MS.MR1Key(OZ, (0,) * 7, 5)

    def test_mr0_profile_and_key(self):
        a = MS.mr0(PB, tracks(PB, [(3, 1)] + [(0, 0)] * 9), 'GRID_COMPLETE')['sub_measures']['MR0']
        b = MS.mr0(PB, tracks(PB, [(2, 1)] * 9 + [(0, 0)]), 'GRID_COMPLETE')['sub_measures']['MR0']
        self.assertEqual(a['W'], (0, 0, 0, 0, 0, 0, 0, 1, 0))
        self.assertEqual(a['expected'][9], 10 * Fraction(51597, 3362260))
        self.assertGreater(a['descriptive_key'], b['descriptive_key'])     # lexicographic: one PD8 beats nine PD9
        self.assertEqual(a['calibration'], 'NOT_A_P_VALUE')
        # OWN_SET: equal V, different n -> MR1 descending breaks the tie (smaller n has larger MR1)
        c = MS.mr0(PB, tracks(PB, [(2, 1)] + [(0, 0)] * 9), 'GRID_COMPLETE')['sub_measures']['MR0']
        d = MS.mr0(PB, tracks(PB, [(2, 1)] + [(0, 0)] * 19), 'GRID_COMPLETE')['sub_measures']['MR0']
        self.assertGreater(c['descriptive_key'], d['descriptive_key'])
        e = MS.mr0(PB, tracks(PB, [(0, 0)] * 9 + [(2, 1)]), 'GRID_COMPLETE')['sub_measures']['MR0']
        self.assertEqual(c['descriptive_key'], e['descriptive_key'])


class MR4(unittest.TestCase):

    def test_sub_measures_and_sets(self):
        res = MS.mr4(PB, tracks(PB, [(0, 0)] * 10), 'GRID_COMPLETE')['sub_measures']
        ids = list(res)
        self.assertEqual(ids, [f'MR4.X.{d}' for d in range(1, 10)] + [f'MR4.C.{d}' for d in range(1, 10)] +
                         ['MR4.B.2-3'])
        self.assertEqual(res['MR4.C.3']['owner_ref'], 'R8')
        self.assertEqual(res['MR4.B.2-3']['owner_ref'], 'R9')
        self.assertEqual(res['MR4.X.3']['owner_ref'], 'R10')
        self.assertEqual(res['MR4.C.9']['p_S'], DV.any_division_probability(PB))
        self.assertEqual(res['MR4.B.2-3']['p_S'], Fraction(19, 134490400) + Fraction(49, 33622600))
        oz = MS.mr4(OZ, tracks(OZ, [(0, 0)] * 10), 'GRID_COMPLETE')['sub_measures']
        self.assertEqual(len(oz), 15)
        self.assertEqual(oz['MR4.C.7']['p_S'], DV.any_division_probability(OZ))

    def test_tails_equal_oracle(self):
        codes = [(2, 1)] * 2 + [(4, 1)] + [(5, 0)] + [(0, 0)] * 26
        res = MS.mr4(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']
        for sid in ('MR4.X.9', 'MR4.C.9', 'MR4.X.6', 'MR4.C.7', 'MR4.B.2-3'):
            s = res[sid]
            k = s['k_S']
            self.assertEqual(s['significance']['P_up'], oracle_upper(30, s['p_S'], k), sid)
            self.assertEqual(s['significance']['P_lo'], oracle_lower(30, s['p_S'], k), sid)
            self.assertEqual(s['significance_key'], (s['significance']['Z_plus']['sigma'], k))
        self.assertEqual((res['MR4.X.9']['k_S'], res['MR4.C.9']['k_S'], res['MR4.C.7']['k_S']), (2, 4, 2))
        self.assertEqual(res['MR4.C.9']['expected'], 30 * DV.any_division_probability(PB))

    def test_oz_divisions_use_supplementaries(self):
        codes = [(6, 1), (5, 1), (3, 1), (3, 0), (4, 2)] + [(0, 0)] * 5
        res = MS.mr4(OZ, tracks(OZ, codes), 'GRID_COMPLETE')['sub_measures']
        self.assertEqual([res[f'MR4.X.{d}']['k_S'] for d in range(1, 8)], [0, 1, 0, 1, 0, 1, 1])


class MR5(unittest.TestCase):
    """MRT-10 and MR5's significance."""

    def test_target_fields_equal_r3_values(self):
        distinct = {j: j for j in range(1, 36)}
        pbd = {j: j for j in range(1, 21)}
        f = MS.mr5_target_fields(PB, distinct, [1, 2, 3, 4, 5, 6, 7], pbd, 20)
        self.assertEqual(f['mean_rank_main'], 4)
        self.assertEqual(f['fair_var_main'], 12)                     # sd sqrt(12) = 3.4641 (R3 4.3)
        self.assertEqual(f['rank_powerball'], 20)
        self.assertEqual(f['fair_var_pb'], Fraction(133, 4))         # 33.25, sd 5.7663 (R3 4.3)
        tied = MS.mid_ranks_from_groups([list(range(1, 36))], 35)
        self.assertEqual(set(tied.values()), {18})                     # all tied: 18 (R3 2.x)
        ptied = MS.mid_ranks_from_groups([list(range(1, 21))], 20)
        self.assertEqual(set(ptied.values()), {Fraction(21, 2)})
        g = MS.mr5_target_fields(PB, tied, [1, 9, 17, 22, 30, 34, 35], ptied, 3)
        self.assertEqual((g['mean_rank_main'], g['fair_var_main'], g['rank_powerball'], g['fair_var_pb']),
                         (18, 0, Fraction(21, 2), 0))
        groups = [[5], [1, 2], [3, 4, 6]] + [[j] for j in range(7, 48)]
        mr = MS.mid_ranks_from_groups(groups, 47)
        self.assertEqual((mr[5], mr[1], mr[2], mr[3], mr[6], mr[7]),
                         (1, Fraction(5, 2), Fraction(5, 2), 5, 5, 7))
        oz = MS.mr5_target_fields(OZ, mr, [5, 1, 3, 7, 8, 9, 10])
        self.assertEqual(oz['mean_rank_main'], (1 + Fraction(5, 2) + 5 + 7 + 8 + 9 + 10) / 7)
        self.assertNotIn('rank_powerball', oz)
        with self.assertRaises(ValueError):
            MS.mr5_target_fields(PB, {j: j for j in range(1, 35)}, [1, 2, 3, 4, 5, 6, 7], pbd, 1)
        with self.assertRaises(ValueError):                           # 1,1 is not a mid-rank pair
            MS.mr5_target_fields(PB, dict(distinct, **{}) | {2: 1}, [1, 2, 3, 4, 5, 6, 7], pbd, 1)

    def test_measure(self):
        distinct = {j: j for j in range(1, 36)}
        pbd = {j: j for j in range(1, 21)}
        tg = []
        for i, (drawn, dpb) in enumerate([([1, 2, 3, 4, 5, 6, 7], 1), ([10, 11, 12, 13, 14, 15, 16], 2),
                                         ([20, 21, 22, 23, 24, 25, 26], 20)]):
            tg.append(dict(MS.mr5_target_fields(PB, distinct, drawn, pbd, dpb), draw_number=1300 + i))
        res = MS.mr5(PB, tg, 'GRID_COMPLETE')
        self.assertEqual(res['analysis_unit'], 'METHOD_VARIANT_RANKING')
        main, pbc = res['sub_measures']['MR5.MAIN'], res['sub_measures']['MR5.PB']
        self.assertEqual(main['MR5'], Fraction(4 + 13 + 23, 3))
        self.assertEqual(main['expectation'], 18)
        self.assertEqual(main['descriptive_order'], 'ascending')
        z = (3 * 18 - (4 + 13 + 23)) / math.sqrt(36)
        self.assertAlmostEqual(main['significance']['Z'], z, places=12)
        self.assertEqual(main['significance']['Z_plus']['sigma'], max(0.0, z))
        self.assertEqual(main['significance']['label'], 'APPROX_UNCALIBRATED')
        self.assertEqual(main['n1_reference']['label'], 'N1_NOT_RUN')
        zpb = (3 * 10.5 - 23) / math.sqrt(3 * 33.25)
        self.assertAlmostEqual(pbc['significance']['Z'], zpb, places=12)
        ref = {'MR5.MAIN': {'p_up': Fraction(7, 10001)}}
        r2 = MS.mr5(PB, tg, 'GRID_COMPLETE', n1=ref)['sub_measures']
        self.assertEqual(r2['MR5.MAIN']['n1_reference']['label'], 'N1_FIXED_FORECAST_REFERENCE')
        self.assertEqual(r2['MR5.PB']['n1_reference']['label'], 'N1_NOT_RUN')
        r3 = MS.mr5(PB, tg, 'GRID_INCOMPLETE', n1=ref)['sub_measures']['MR5.MAIN']
        self.assertEqual(r3['n1_reference']['label'], 'N1_FIXED_FORECAST_REFERENCE')   # never calibrated
        self.assertIn('SELECTION_UNVERIFIED', r3['flags'])

    def test_null_variance_zero(self):
        tied = MS.mid_ranks_from_groups([list(range(1, 48))], 47)
        tg = [dict(MS.mr5_target_fields(OZ, tied, [1, 2, 3, 4, 5, 6, 7]), draw_number=1500 + i) for i in range(4)]
        s = MS.mr5(OZ, tg, 'GRID_COMPLETE')['sub_measures']
        self.assertEqual(list(s), ['MR5.MAIN'])
        self.assertEqual(s['MR5.MAIN']['status'], 'NULL_VARIANCE_ZERO')
        self.assertEqual(s['MR5.MAIN']['MR5'], 24)
        self.assertIsNone(s['MR5.MAIN']['significance']['Z_plus'])
        self.assertIsNone(s['MR5.MAIN']['significance_key'])

    def test_invalid_rank_inputs(self):
        bad = [{'draw_number': 1300, 'mean_rank_main': 18.0, 'fair_var_main': Fraction(1)},
               {'draw_number': 1300, 'mean_rank_main': Fraction(1, 3), 'fair_var_main': Fraction(1)},
               {'draw_number': 1300, 'mean_rank_main': 18, 'fair_var_main': -1}]
        for t in bad:
            r = MS.mr5(OZ, [t], 'GRID_COMPLETE')
            self.assertEqual(r['status'], 'MR_NUMERIC_INVALID')
            self.assertIsNone(r['sub_measures']['MR5.MAIN']['significance_key'])


class MR7(unittest.TestCase):
    """MRT-19 (against an independent exact oracle) and the bound of design 6.6."""

    def test_exact_against_oracle(self):
        rng = random.Random(7)
        for game in DV.GAMES:
            codes = fair_codes(game, 6, rng)
            res = MS.mr7(game, tracks(game, codes), 'GRID_COMPLETE')['sub_measures']
            main = res['MR7.MAIN']
            s = sum(m for m, _ in codes)
            up, lo = oracle_mr7(game, 6, s)
            self.assertEqual(main['S'], s)
            self.assertEqual(main['significance']['P_up'], up)
            self.assertEqual(main['significance']['P_lo'], lo)
            self.assertEqual(main['excess'], s - 6 * DV.MEAN0[game])
            self.assertEqual(main['descriptive_key'], main['excess'])
            self.assertEqual(main['S_per_draw'], Fraction(s, 6))
            self.assertEqual((main['mean0'], main['var0']), (DV.MEAN0[game], DV.VAR0[game]))
            self.assertEqual(main['significance']['label'], 'EXACT_LOCAL')
            if game == PB:
                b = sum(x for _, x in codes)
                pb = res['MR7.PB']
                self.assertEqual(pb['B'], b)
                self.assertEqual(pb['significance']['P_up'], oracle_upper(6, Fraction(1, 20), b))
                self.assertEqual(pb['significance']['P_lo'], oracle_lower(6, Fraction(1, 20), b))
            else:
                self.assertNotIn('MR7.PB', res)
        # a planted tie of S across different code mixes gives equal tails
        a = MS.mr7(PB, tracks(PB, [(2, 0), (2, 0)]), 'GRID_COMPLETE')['sub_measures']['MR7.MAIN']
        b = MS.mr7(PB, tracks(PB, [(4, 0), (0, 0)]), 'GRID_COMPLETE')['sub_measures']['MR7.MAIN']
        self.assertEqual(a['significance']['P_up'], b['significance']['P_up'])

    def test_above_exact_bound(self):
        n = MS.MR7_EXACT_MAX_N + 1
        codes = [(2, 0)] * n
        res = MS.mr7(PB, tracks(PB, codes, first=1), 'GRID_COMPLETE')['sub_measures']
        main = res['MR7.MAIN']
        self.assertEqual(main['status'], 'MR_EXACT_BOUND_EXCEEDED')
        self.assertEqual(main['significance']['label'], 'MR_EXACT_BOUND_EXCEEDED')
        self.assertIsNone(main['significance']['P_up'])
        self.assertEqual(main['approx']['label'], 'APPROX_UNCALIBRATED')
        z = (2 * n - 1.4 * n) / math.sqrt(n * 392 / 425)
        self.assertAlmostEqual(main['approx']['Z'], z, places=9)
        self.assertEqual(main['significance_key'], main['approx']['Z_plus']['sigma'])
        self.assertEqual(res['MR7.PB']['significance']['label'], 'EXACT_LOCAL')       # PB stays exact
        with self.assertRaises(ValueError) as cm:
            NU.mr7_null(PB, n)
        self.assertIn('MR_EXACT_BOUND_EXCEEDED', str(cm.exception))


class MR16(unittest.TestCase):
    """MRT-22."""

    REF = [  # R3 17.6 MR16 reference table
        ('Powerball any division', 291, DV.any_division_probability(PB), 6.6, 16, 2.42, 0.04, 0.25),
        ('Powerball 3+ main', 291, DV.main_match_at_least(PB, 3), 36.3, 55, 1.51, 0.49, 0.99),
        ('Powerball hit', 291, Fraction(1, 20), 14.6, 28, 1.92, 0.11, 0.61),
        ('Oz Lotto any division', 220, DV.any_division_probability(OZ), 4.4, 13, 2.97, 0.02, 0.10),
        ('Oz Lotto 3+ main', 220, DV.main_match_at_least(OZ, 3), 12.5, 25, 2.01, 0.08, 0.52),
    ]

    def test_reference_rows(self):
        for name, n, p, exp, k3, ratio, p15, p2 in self.REF:
            t = MS.mr16_threshold(n, p)
            self.assertEqual(round(float(n * p), 1), exp, name)
            self.assertEqual(t['k_3'], k3, name)
            self.assertEqual(round(float(t['threshold_ratio']), 2), ratio, name)
            self.assertEqual(round(float(t['power_1_5x']), 2), p15, name)
            self.assertEqual(round(float(t['power_2x']), 2), p2, name)
            self.assertLessEqual(NU.binom_upper(n, p, k3), MS.THREE_SIGMA_P_UP)
            self.assertGreater(NU.binom_upper(n, p, k3 - 1), MS.THREE_SIGMA_P_UP)

    def test_track_rows_match_reference(self):
        rng = random.Random(16)
        codes = fair_codes(PB, 291, rng)
        res = MS.mr16(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']
        self.assertEqual(list(res), ['MR16.ANYDIV'] + [f'MR16.PD{d}' for d in range(1, 10)] +
                         ['MR16.M2', 'MR16.M3', 'MR16.M4', 'MR16.PB'])
        self.assertEqual((res['MR16.ANYDIV']['k_3'], res['MR16.M3']['k_3'], res['MR16.PB']['k_3']), (16, 55, 28))
        k3 = sum(1 for m, _ in codes if m >= 3)
        s = res['MR16.M3']
        self.assertEqual((s['k'], s['rate']), (k3, Fraction(k3, 291)))
        self.assertEqual(s['significance']['P_up'], NU.binom_upper(291, DV.main_match_at_least(PB, 3), k3))
        self.assertEqual(s['descriptive_key'], s['interval'][0])
        self.assertEqual(s['interval_label'], 'CONSTANT_RATE_REFERENCE_INTERVAL')
        # no double count with MR4 (and MR16.PB is MR7.PB's tail)
        self.assertEqual(res['MR16.ANYDIV']['same_test_as'], 'MR4.C.9')
        self.assertEqual(res['MR16.PD4']['same_test_as'], 'MR4.X.4')
        self.assertEqual(res['MR16.PB']['same_test_as'], 'MR7.PB')
        for sid, sub in res.items():
            self.assertEqual(sub['counts_in_M'], sid in ('MR16.M2', 'MR16.M3', 'MR16.M4'), sid)
        m4 = MS.mr4(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']
        m7 = MS.mr7(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']
        self.assertEqual(res['MR16.ANYDIV']['significance']['P_up'], m4['MR4.C.9']['significance']['P_up'])
        self.assertEqual(res['MR16.PD9']['significance']['P_up'], m4['MR4.X.9']['significance']['P_up'])
        self.assertEqual(res['MR16.PB']['significance']['P_up'], m7['MR7.PB']['significance']['P_up'])
        oz = MS.mr16(OZ, tracks(OZ, fair_codes(OZ, 20, rng)), 'GRID_COMPLETE')['sub_measures']
        self.assertEqual(list(oz), ['MR16.ANYDIV'] + [f'MR16.OD{d}' for d in range(1, 8)] +
                         ['MR16.M2', 'MR16.M3', 'MR16.M4'])

    def test_clopper_pearson_against_independent_implementation(self):
        for k, n in ((0, 10), (3, 10), (10, 10), (5, 50), (1, 291)):
            lo, hi = NU.clopper_pearson(k, n)
            olo, ohi = oracle_cp(k, n)
            self.assertAlmostEqual(float(lo), olo, delta=1e-12, msg=(k, n))
            self.assertAlmostEqual(float(hi), ohi, delta=1e-12, msg=(k, n))
        self.assertEqual(float(NU.clopper_pearson(0, 10)[0]), 0.0)

    def test_threshold_unreachable(self):
        t = MS.mr16_threshold(1, Fraction(1, 20))
        self.assertEqual((t['k_3'], t['k_3_status'], t['power_2x']), (None, 'MR_UNDEFINED', None))


class LabelsAndStatuses(unittest.TestCase):
    """Design 6.2A and R3 17.3.7 / 17.3.7A; MRT-16 (d) for this module's labels."""

    def test_complete_incomplete_empty(self):
        codes = [(3, 1), (2, 1), (1, 0)] * 12
        for f in ALL:
            comp = f(PB, tracks(PB, codes), 'GRID_COMPLETE')
            inc = f(PB, tracks(PB, codes), 'GRID_INCOMPLETE', invalid_cells={'RUNTIME_FAILURE': 2})
            emp = f(PB, [], 'GRID_EMPTY')
            self.assertEqual(inc['invalid_cells'], {'RUNTIME_FAILURE': 2})
            for sid, sub in comp['sub_measures'].items():
                isub, esub = inc['sub_measures'][sid], emp['sub_measures'][sid]
                if sub['calibration'] == 'EXACT_LOCAL':
                    self.assertEqual(isub['calibration'], 'SELECTION_UNVERIFIED', sid)
                    self.assertEqual(isub['significance']['label'], 'SELECTION_UNVERIFIED', sid)
                    self.assertEqual(isub['significance']['P_up'], sub['significance']['P_up'], sid)
                self.assertIn('SELECTION_UNVERIFIED', isub['flags'])
                self.assertNotIn('SELECTION_UNVERIFIED', sub['flags'])
                self.assertEqual(esub['status'], 'MR_INSUFFICIENT_DATA', sid)
                self.assertIsNone(esub['significance_key'], sid)
                self.assertIsNone(esub['descriptive_key'], sid)
                blk = esub['significance']
                if blk is not None:
                    self.assertIsNone(blk['P_up'], sid)
                    self.assertIsNone(blk['Z_plus'], sid)
                    self.assertIn(blk['label'], ('MR_INSUFFICIENT_DATA',), sid)
        self.assertEqual(MS.mr5(PB, [], 'GRID_EMPTY')['sub_measures']['MR5.MAIN']['status'], 'MR_INSUFFICIENT_DATA')
        self.assertEqual(MS.mr4(PB, [], 'GRID_INCOMPLETE')['sub_measures']['MR4.X.1']['calibration'],
                         'MR_INSUFFICIENT_DATA')
        with self.assertRaises(ValueError):
            MS.mr7(PB, tracks(PB, codes), 'GRID_EMPTY')
        with self.assertRaises(ValueError):
            MS.mr7(PB, tracks(PB, codes), 'COMPLETE')

    def test_low_n(self):
        self.assertIn('LOW_N', MS.mr7(OZ, tracks(OZ, [(1, 0)] * 29), 'GRID_COMPLETE')['flags'])
        self.assertNotIn('LOW_N', MS.mr7(OZ, tracks(OZ, [(1, 0)] * 30), 'GRID_COMPLETE')['flags'])

    def test_invalid_inputs(self):
        good = tracks(PB, [(2, 1), (0, 0)])
        bad_div = [dict(good[0], division=0), good[1]]
        r = MS.mr4(PB, bad_div, 'GRID_COMPLETE')
        self.assertEqual(r['status'], 'MR_NUMERIC_INVALID')
        self.assertTrue(all(s['status'] == 'MR_NUMERIC_INVALID' and s['significance_key'] is None
                            for s in r['sub_measures'].values()))
        self.assertEqual(MS.mr7(PB, [dict(good[0], powerball_match=True), good[1]], 'GRID_COMPLETE')['status'],
                         'MR_NUMERIC_INVALID')
        ozt = tracks(OZ, [(6, 1)])
        self.assertEqual(MS.mr16(OZ, [dict(ozt[0], supplementary_matches=2)], 'GRID_COMPLETE')['status'],
                         'MR_NUMERIC_INVALID')
        with self.assertRaises(ValueError):
            MS.mr0(PB, [good[1], good[0]], 'GRID_COMPLETE')                 # descending draw numbers
        with self.assertRaises(ValueError):
            MS.mr0(PB, [good[0], good[0]], 'GRID_COMPLETE')                 # repeated draw number
        with self.assertRaises(ValueError):
            MS.mr0('LOTTO', good, 'GRID_COMPLETE')


class UnitsAndChannels(unittest.TestCase):
    """MRT-23 and MRT-12 for this module's outputs."""

    def test_units_channels_and_ids(self):
        codes = [(2, 1), (3, 0)] * 5
        units = {'MR0': 'READOUT_TRACK', 'MR1': 'READOUT_TRACK', 'MR4': 'READOUT_TRACK',
                 'MR7': 'READOUT_TRACK', 'MR16': 'READOUT_TRACK'}
        seen = set()
        for f in ALL:
            for game in DV.GAMES:
                r = f(game, tracks(game, codes), 'GRID_COMPLETE')
                self.assertEqual(r['analysis_unit'], units[r['measure']])
                for sid in r['sub_measures']:
                    self.assertNotIn((game, sid), seen)
                    seen.add((game, sid))
                    if game == OZ:
                        self.assertFalse(sid.endswith('.PB'), sid)
        self.assertIn((PB, 'MR7.PB'), seen)
        self.assertIn((PB, 'MR16.PB'), seen)
        self.assertNotIn((OZ, 'MR7.PB'), seen)

    def test_numeric_field_types(self):
        r = MS.mr16(PB, tracks(PB, [(2, 1), (3, 0)] * 20), 'GRID_COMPLETE')['sub_measures']['MR16.PD9']
        self.assertIs(type(r['k']), int)
        self.assertIs(type(r['n']), int)
        self.assertLess(r['k'], 2 ** 63)
        self.assertIs(type(r['significance']['P_up_output']['p_float']), float)
        self.assertIs(type(r['significance']['Z_plus']['sigma']), float)
        m1 = MS.mr1(PB, tracks(PB, [(2, 1)] * 3), 'GRID_COMPLETE')['sub_measures']['MR1']
        for f in ('MR1', 'E0', 'sd0', 'difference', 'sum_bits'):
            self.assertIs(type(m1[f]), float, f)


class PlantedAndNull(unittest.TestCase):
    """MRT-07 (hit-rate tilt for MR4 and MR7) and MRT-08 (determinism)."""

    def test_planted_tilt_detected(self):
        rng = random.Random(99)
        codes = []
        for _ in range(120):                       # a strong invented tilt: one extra main match per draw
            m, b = fair_codes(PB, 1, rng)[0]
            codes.append((min(7, m + 1), b))
        r7 = MS.mr7(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']['MR7.MAIN']
        self.assertGreater(r7['significance']['Z_plus']['sigma'], 5)
        r4 = MS.mr4(PB, tracks(PB, [(3, 1)] * 10 + [(0, 0)] * 50), 'GRID_COMPLETE')['sub_measures']['MR4.X.8']
        self.assertGreater(r4['significance']['Z_plus']['sigma'], 3)

    def test_null_tracks_near_nominal(self):
        rng = random.Random(2026)
        rejections = 0
        trials = 200
        for _ in range(trials):
            r = MS.mr7(OZ, tracks(OZ, fair_codes(OZ, 40, rng)), 'GRID_COMPLETE')['sub_measures']['MR7.MAIN']
            rejections += r['significance']['P_up'] <= Fraction(5, 100)
        self.assertLessEqual(rejections, 22)        # nominal 5% of 200 = 10; generous binomial margin

    def test_determinism(self):
        rng = random.Random(5)
        codes = fair_codes(PB, 50, rng)
        for f in ALL:
            a = f(PB, tracks(PB, codes), 'GRID_COMPLETE')
            b = f(PB, tracks(PB, codes), 'GRID_COMPLETE')
            self.assertEqual(repr(a), repr(b), f.__name__)


class Ranking(unittest.TestCase):
    """MRT-09: standard competition ranking, ties listed by track ID (R3 17.10.4)."""

    def test_competition_ranks_and_tie_order(self):
        rows = [{'track_id': 'T:c', 'v': 5}, {'track_id': 'T:a', 'v': 7}, {'track_id': 'T:b', 'v': 7},
                {'track_id': 'T:d', 'v': 3}, {'track_id': 'T:e', 'v': None}, {'track_id': 'T:f', 'v': None}]
        t = MS.rank_table(rows, 'v')
        self.assertEqual([(e['display'], e['track_id']) for e in t],
                         [('1=', 'T:a'), ('1=', 'T:b'), ('3', 'T:c'), ('4', 'T:d'), ('5=', 'T:e'), ('5=', 'T:f')])
        self.assertEqual([e['undefined'] for e in t], [False] * 4 + [True] * 2)
        asc = MS.rank_table(rows[:4], 'v', descending=False)
        self.assertEqual([(e['display'], e['track_id']) for e in asc],
                         [('1', 'T:d'), ('2', 'T:c'), ('3=', 'T:a'), ('3=', 'T:b')])

    def test_exact_keys(self):
        rows = [{'track_id': 'B', 'k': Fraction(1, 3)}, {'track_id': 'A', 'k': Fraction(2, 6)},
                {'track_id': 'C', 'k': Fraction(333333333333, 10 ** 12)}]
        t = MS.rank_table(rows, 'k')
        self.assertEqual([e['display'] for e in t], ['1=', '1=', '3'])
        self.assertEqual([e['track_id'] for e in t], ['A', 'B', 'C'])
        f = MS.rank_table([{'track_id': 'x', 'k': 0.1 + 0.2}, {'track_id': 'y', 'k': 0.3}], 'k')
        self.assertEqual([e['display'] for e in f], ['1', '2'])          # floats at full float64 equality

    def test_measure_keys_rank(self):
        res = {}
        for tid, codes in (('P:1', [(3, 1)] + [(0, 0)] * 9), ('P:2', [(0, 0)] * 9 + [(3, 1)]),
                           ('P:3', [(2, 1)] * 3 + [(0, 0)] * 7), ('P:4', [(0, 0)] * 20)):
            res[tid] = MS.mr0(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']['MR0']
        rows = [{'track_id': k, 'key': v['descriptive_key']} for k, v in res.items()]
        rows.append({'track_id': 'P:5', 'key': MS.mr0(PB, [], 'GRID_EMPTY')['sub_measures']['MR0']['descriptive_key']})
        t = MS.rank_table(rows, 'key')
        self.assertEqual([(e['display'], e['track_id']) for e in t],
                         [('1=', 'P:1'), ('1=', 'P:2'), ('3', 'P:3'), ('4', 'P:4'), ('5', 'P:5')])
        sig = []
        for tid, codes in (('S:1', [(3, 1)] * 2 + [(0, 0)] * 8), ('S:2', [(3, 1)] * 2 + [(0, 0)] * 8),
                           ('S:3', [(0, 0)] * 10)):
            s = MS.mr4(PB, tracks(PB, codes), 'GRID_COMPLETE')['sub_measures']['MR4.X.8']
            sig.append({'track_id': tid, 'key': s['significance_key']})
        self.assertEqual([e['display'] for e in MS.rank_table(sig, 'key')], ['1=', '1=', '3'])

    def test_bad_rows(self):
        with self.assertRaises(ValueError):
            MS.rank_table([{'track_id': 'a', 'k': 1}, {'track_id': 'a', 'k': 2}], 'k')
        with self.assertRaises(ValueError):
            MS.rank_table([{'track_id': 'a', 'k': float('nan')}], 'k')


class Bonferroni(unittest.TestCase):

    def test_arithmetic(self):
        b = MS.bonferroni(Fraction(1, 1000), 80)
        self.assertEqual(b['P_bonf'], Fraction(80, 1000))
        self.assertEqual(MS.bonferroni(Fraction(1, 10), 80)['P_bonf'], 1)
        self.assertEqual(MS.bonferroni(Fraction(1, 10), 80)['Z_plus']['sigma'], 0.0)


if __name__ == '__main__':
    unittest.main()
