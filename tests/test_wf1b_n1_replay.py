"""WF-1B: N1 replays the exact tails of MR4 division sets, MR7 and MR16 events (design v0.1r1 section 7.1; R3 MRT-16 (a),
MRT-19; EX_109 C03). Invented tickets and an invented root ('AB' x 64), never a beacon value or a real draw.

For the hit-sequence class the per-target hit law is the same whatever ticket is picked, so N1's replay must match
the exact binomial (MR4, MR16) and convolution (MR7) tails within Monte Carlo error, for fixed tickets and also for
an adaptive synthetic rule whose ticket depends on the previous simulated draw (MRT-16 (a))."""
from __future__ import annotations

import hashlib
import sys
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from evaluation import divisions as DV      # noqa: E402
from evaluation import measures as MS       # noqa: E402
from evaluation import n1 as N1             # noqa: E402
from evaluation import n1_generator as G    # noqa: E402
from evaluation import numerics as NU       # noqa: E402

POLICY = {'policy_id': 'N1_ROOT_TEST_ONLY_V1', 'output_value': 'AB' * 64}
R = 3000


def tickets(game: str, targets) -> dict:
    """Invented, target-varying tickets (7 main labels; plus a Powerball for Powerball)."""
    size = DV.MAIN_POOL[game]
    out = {}
    for t in targets:
        lab = sorted(range(1, size + 1), key=lambda x: hashlib.sha256(f'{game}:{t}:{x}'.encode()).digest())[:7]
        out[t] = (tuple(sorted(lab)), (1 + int(hashlib.sha256(f'pb:{t}'.encode()).digest()[0]) % 20)
                  if game == 'POWERBALL' else None)
    return out


def within(test, k_rep: np.ndarray, exact_tail, ks, what):
    reps = len(k_rep)
    for k in ks:
        emp = float((k_rep >= k).mean())
        ex = float(exact_tail(k))
        se = max((ex * (1 - ex) / reps) ** 0.5, 1 / reps)
        test.assertLess(abs(emp - ex), 5 * se, (what, k, emp, ex))


class FixedTickets(unittest.TestCase):

    def check_game(self, game, targets):
        ent = tickets(game, targets)
        with mock.patch.object(N1, 'R', R):
            sim = N1.simulate(POLICY, game, targets)
        mm, div = N1._replay(sim, game, ent)
        n = len(targets)
        # MR4 division sets (exact binomial on p_S): any division, the lowest division, and a two-division band.
        D = DV.DIVISION_COUNT[game]
        for name, dset in (('C.all', set(range(1, D + 1))), (f'X.{D}', {D}), (f'B.{D - 1}-{D}', {D - 1, D})):
            p_s = DV.division_set_probability(game, frozenset(dset))
            k_rep = np.isin(div, list(dset)).sum(axis=1)
            within(self, k_rep, lambda k: NU.binom_upper(n, p_s, k), range(0, 9), f'{game} MR4 {name}')
        # MR16 events: at least 2 and 3 main matches.
        for j in (2, 3):
            p = DV.main_match_at_least(game, j)
            within(self, (mm >= j).sum(axis=1), lambda k: NU.binom_upper(n, p, k), range(0, 30, 3), f'{game} MR16.M{j}')
        # MR7: the total main matches against its exact convolution null.
        tails = N1._tail_table(game, n)
        within(self, mm.sum(axis=1), lambda s: tails[s], range(60, 120, 8), f'{game} MR7')
        return mm, div, sim, ent

    def test_powerball(self):
        targets = list(range(1400, 1520))
        mm, div, sim, ent = self.check_game('POWERBALL', targets)
        cols = [sim['index'][t] for t in targets]
        pb = np.array([ent[t][1] for t in targets])
        hits = (sim['extra'][:, cols] == pb[None, :]).sum(axis=1)                      # MR16.PB / MR7.PB
        within(self, hits, lambda k: NU.binom_upper(len(targets), Fraction(1, 20), k), range(0, 12, 2), 'MR7.PB')

    def test_oz_lotto_supplementary_branch(self):
        targets = list(range(1500, 1620))
        mm, div, sim, ent = self.check_game('OZLOTTO', targets)
        # The supplementary classification itself: replayed divisions equal the per-draw classifier's.
        r = 0
        for j, t in enumerate(targets[:40]):
            m, s = G.fair_draw(POLICY['output_value'], POLICY['policy_id'], 'OZLOTTO', r + 1, t)
            rec = DV.match_record('OZLOTTO', ent[t][0], None, m, s)
            self.assertEqual((int(mm[r, j]), int(div[r, j])), (rec['main_matches'], rec['division']))


class AdaptiveTickets(unittest.TestCase):
    """An adaptive synthetic rule: each target's ticket is the previous simulated draw's main numbers (so it depends
    on outcomes). The hit-sequence tails must still match the exact ones (MRT-16 (a))."""

    def test_adaptive_rule(self):
        game, targets, reps = 'POWERBALL', list(range(1400, 1460)), 2000
        root, pid = POLICY['output_value'], POLICY['policy_id']
        k_any, s_tot = np.zeros(reps, dtype=np.int64), np.zeros(reps, dtype=np.int64)
        for r in range(reps):
            ticket, tpb = tuple(range(1, 8)), 1
            for t in targets:
                m, b = G.fair_draw(root, pid, game, r + 1, t)
                rec = DV.match_record(game, ticket, tpb, m, b)
                k_any[r] += rec['division'] >= 1
                s_tot[r] += rec['main_matches']
                ticket, tpb = m, b                                   # adapt to the outcome just seen
        n = len(targets)
        p_any = DV.any_division_probability(game)
        within(self, k_any, lambda k: NU.binom_upper(n, p_any, k), range(0, 8), 'adaptive MR4 C.all')
        tails = N1._tail_table(game, n)
        within(self, s_tot, lambda s: tails[s], range(70, 100, 6), 'adaptive MR7')
        # The adaptive replay is a hit-sequence statistic, so MR1's calibration class stays N1_CALIBRATED; the
        # cross-track maximum and forecast-weighted figures stay references (labels, MRT-16 (b)/(c)).
        out = MS.mr1(game, [{'draw_number': 1400, 'main_matches': 0, 'powerball_match': 0, 'division': 0}],
                     'GRID_COMPLETE', n1={'p_up': Fraction(1, 2), 'ci': (0.4, 0.6), 'R': 10, 'k': 4})
        self.assertEqual(out['sub_measures']['MR1']['significance']['label'], 'N1_CALIBRATED')


if __name__ == '__main__':
    unittest.main()
