"""Wave 2 revision 1 (E_2, E_17, E_18, E_19): variants, each variant's own rule, relations, no peeking, contract.

OFFLINE, synthetic only. Every master here is invented and written to a temporary folder; no file under the
repository's data folders is opened and no real draw value is read. The installed contract data is only read.
Specification: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md. Built from the wave 1 tests
(themselves from the new-method template's test_template.py.txt). Each variant's rule is written again here,
from the design note, without the shared helper; E_17's log-age sign is recomputed with 60-digit decimal
logarithms, and E_18's weights are checked against an optimality certificate written here.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Fr
from importlib import import_module
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest import mock

import e2r_fixtures as F
import e2r_code2_fixtures as C
from test_e6_beta_bernoulli import write_varied_master

from _common import contract_publication as CP
from _common import contract_runner as CR
from _common.contract_dispatch import DispatchRefused, dispatch_gate, METHODS_ROOT, method_folder
from _common.contract_forecast import assemble_forecast, BarrelOutput, MethodOutput, ScoredRanking
from _common.contract_publication import read_run
from _common.contract_records import record_digest, score_groups
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from _common.multigame_method_registry import method_status
from E_002 import contract as E2
from E_017 import contract as E17
from E_018 import contract as E18
from E_019 import contract as E19

GAMES = (POWERBALL, OZLOTTO)
MODULES = {'E_2': E2, 'E_17': E17, 'E_18': E18, 'E_19': E19}
SPEC = {   # design note v0.1r2 section 6, written out here (not read from the modules); last item = minimum history
    'E_2': {'RECUR_MEAN_ALL_V1': ('mean', None, 104), 'RECUR_MEDIAN_ALL_V1': ('median', None, 104),
            'RECUR_MEAN_LAST8_V1': ('mean', 8, 104)},
    'E_17': {'HAZARD_BINS_C100_V1': ('bins', Fr(100), None, 52), 'HAZARD_BINS_W208_C100_V1': ('bins', Fr(100), 208, 208),
             'HAZARD_LOGAGE_SIGN_V1': ('logage', None, None, 52)},
    'E_18': {'MIX4_ALL_C10_V1': (None, Fr(10), 104), 'MIX4_W208_C10_V1': (208, Fr(10), 208),
             'MIX4_W104_C10_V1': (104, Fr(10), 104)},
    'E_19': {'PERIODIC_T2_V1': (2, Fr(100), Fr(20), 104), 'PERIODIC_T3_V1': (3, Fr(100), Fr(20), 104),
             'PERIODIC_T4_V1': (4, Fr(100), Fr(20), 104)},
}
FIT_VERSION = {'E_2': 'RECURRENCE_INTERVAL_ALIGNMENT_V1', 'E_17': 'DISCRETE_RECURRENCE_HAZARD_V1',
               'E_18': 'FIXED_LIBRARY_GAP_MIXTURE_MINCHISQ_V1', 'E_19': 'PERIODIC_RESIDUE_HAZARD_V1'}
EDGES = {(35, 7): [1, 2, 3, 5, 8, 13], (20, 1): [4, 8, 12, 20, 32, 52], (47, 7): [2, 3, 5, 7, 11, 18],
         (10, 2): [1, 2, 3, 5, 8, 13]}                                  # section 3.4, written out
EX = [[1, 2], [3, 4], [1, 5], [2, 6], [1, 7], [3, 8], [1, 9], [2, 10], [4, 5], [1, 6], [3, 7], [1, 8]]
B10 = NS(barrel_id='MAIN', low=1, high=10, selected=2)


def view_for(td: Path, game: str, method: str, variant: str, target: int, suffix: int = 0):
    sha = write_varied_master(td, get_profile(game), target, suffix)
    reg = InstalledRegistry()
    d = reg.declaration(reg.active_entry(game, method, variant)['declaration_digest'])
    req, view, task = F.load_view(td, d, target, 'UNORDERED_SET', sha)
    return d, req, view, task


def deep_target(profile):
    """A development target with more than 208 eligible draws in both games."""
    return F.targets(profile)[2]


def drawn_sets(rows, b):
    return [set(r['main']) if b.barrel_id == 'MAIN' else {r['powerball']} for r in rows]


# ------------------------------------------------------------------ each rule written again, from the design note
def positions(drawn, j):
    return [i for i, d in enumerate(drawn, 1) if j in d]


def exposures(drawn, labels, window=None):
    """{label: [(age, event)]} over draws after the label's first appearance (inside the window if given)."""
    W = len(drawn)
    start = 1 if window is None else W - window + 1
    out = {}
    for j in labels:
        p, rows, last = positions(drawn, j), [], None
        for i in range(1, W + 1):
            if last is not None and i >= start:
                rows.append((i - last, j in drawn[i - 1]))
            if j in drawn[i - 1]:
                last = i
        out[j] = rows
    return out


def bin_index(k, edges):
    return len([e for e in edges if k > e])


def own_rule(method, cfg, drawn, K, L):
    labels = range(1, L + 1)
    W = len(drawn)
    r = Fr(K, L)
    G = {j: W + 1 - (positions(drawn, j) or [0])[-1] for j in labels}
    if method == 'E_2':
        stat, last_n, _m = cfg
        out = {}
        for j in labels:
            p = positions(drawn, j)
            g = [b - a for a, b in zip(p, p[1:])]
            g = g[-last_n:] if last_n else g
            if not g:
                c = Fr(L, K)
            elif stat == 'mean':
                c = Fr(sum(g), len(g))
            else:
                s = sorted(g)
                c = Fr(s[len(s) // 2]) if len(s) % 2 else Fr(s[len(s) // 2 - 1] + s[len(s) // 2], 2)
            out[j] = -abs(G[j] - c) / c
        return out
    edges = EDGES[(L, K)]

    def hazard_bins(c, window):
        ex = exposures(drawn, labels, window)
        Rb, Eb = [0] * (len(edges) + 1), [0] * (len(edges) + 1)
        for rows in ex.values():
            for age, ev in rows:
                Rb[bin_index(age, edges)] += 1
                Eb[bin_index(age, edges)] += ev
        return [(Eb[i] + c * r) / (Rb[i] + c) for i in range(len(Rb))]

    if method == 'E_17':
        form, c, window, _m = cfg
        if form == 'bins':
            h = hazard_bins(c, window)
            return {j: h[bin_index(G[j], edges)] for j in labels}
        rows = [row for rs in exposures(drawn, labels).values() for row in rs]
        with localcontext() as ctx:
            ctx.prec = 60
            z = [Decimal(age).ln() for age, _e in rows]
            y = [Decimal(int(ev)) for _a, ev in rows]
            zb, yb = sum(z) / len(z), sum(y) / len(y)
            s = sum((zi - zb) * (yi - yb) for zi, yi in zip(z, y))
        sigma = (s > 0) - (s < 0)
        return {j: Fr(sigma * G[j]) for j in labels}
    if method == 'E_19':
        T, c, d, _m = cfg
        h = hazard_bins(c, None)
        ex = exposures(drawn, labels)
        O = {j: [sum(ev for age, ev in ex[j] if age % T == q) for q in range(T)] for j in labels}
        X = {j: [sum((h[bin_index(age, edges)] for age, _e in ex[j] if age % T == q), Fr(0)) for q in range(T)]
             for j in labels}
        phi = [(sum(O[j][q] for j in labels) + d) / (sum((X[j][q] for j in labels), Fr(0)) + d) for q in range(T)]
        out = {}
        for j in labels:
            psi = (O[j][G[j] % T] + d * phi[G[j] % T]) / (X[j][G[j] % T] + d) / ((sum(O[j]) + d) / (sum(X[j]) + d))
            out[j] = h[bin_index(G[j], edges)] * psi
        return out
    window, c, _m = cfg                                       # E_18
    p_of = (2 * r, r, r / 2, 2 * r)

    def pmf(i, g):
        p = p_of[i]
        if i == 3:
            return Fr(0) if g < 2 else (g - 1) * p * p * (1 - p) ** (g - 2)
        return p * (1 - p) ** (g - 1)

    def surv(i, g):
        return 1 - sum((pmf(i, x) for x in range(1, g)), Fr(0))
    ranges = list(zip([1] + [e + 1 for e in edges], edges + [None]))
    P = [[surv(i, lo) - (surv(i, hi + 1) if hi is not None else 0) for lo, hi in ranges] for i in range(4)]
    start = 1 if window is None else W - window + 1
    out = {}
    for j in labels:
        p = positions(drawn, j)
        g = [b - a for a, b in zip(p, p[1:]) if a >= start]
        o = [0] * len(ranges)
        for x in g:
            o[bin_index(x, edges)] += 1
        q = [(o[b] + c * P[1][b]) / (len(g) + c) for b in range(len(ranges))]
        w = E18.fit_weights(q, P, P[1])
        assert kkt(q, P, w), (j, w)
        out[j] = sum((w[i] * pmf(i, G[j]) for i in range(4)), Fr(0)) / sum((w[i] * surv(i, G[j]) for i in range(4)), Fr(0))
    return out


def kkt(q, P, w):
    """Optimality on the simplex for sum_b (q_b - (P w)_b)^2 / P_FAIR(b), written here independently."""
    if min(w) < 0 or sum(w) != 1:
        return False
    res = [q[b] - sum(w[c] * P[c][b] for c in range(4)) for b in range(len(q))]
    grad = [-2 * sum(P[c][b] * res[b] / P[1][b] for b in range(len(q))) for c in range(4)]
    support = [grad[c] for c in range(4) if w[c] > 0]
    return len(set(support)) == 1 and all(grad[c] >= support[0] for c in range(4) if w[c] == 0)


class Variants(unittest.TestCase):
    def test_tables_are_exactly_the_specification(self):
        for name in MODULES:
            table = import_module(f'{method_folder(name)}.variants').VARIANTS
            self.assertEqual({v: tuple(c) for v, c in table.items()}, SPEC[name])


class WorkedExamples(unittest.TestCase):
    """The design note's section 9 through each module's own rule, both routes (values from the reviewed reference)."""

    def check(self, mod, cfg, want):
        for second in (False, True):
            self.assertEqual(mod._scores(EX, B10, cfg, second), want)

    def test_all_examples(self):
        f = Fr
        self.check(E2, ('mean', None, 1), {1: f(-6, 11), 2: f(-3, 7), 3: f(-5, 9), 4: f(-3, 7), 5: f(-1, 3), 6: f(-1, 2),
                                           7: f(-2, 3), 8: f(-5, 6), 9: f(-1, 5), 10: f(0)})
        self.check(E2, ('median', None, 1), {1: f(-1, 2), 2: f(-3, 7), 3: f(-5, 9), 4: f(-3, 7), 5: f(-1, 3), 6: f(-1, 2),
                                             7: f(-2, 3), 8: f(-5, 6), 9: f(-1, 5), 10: f(0)})
        self.check(E2, ('mean', 2, 1), {1: f(-3, 5), 2: f(-3, 7), 3: f(-5, 9), 4: f(-3, 7), 5: f(-1, 3), 6: f(-1, 2),
                                        7: f(-2, 3), 8: f(-5, 6), 9: f(-1, 5), 10: f(0)})
        self.check(E17, ('bins', f(10), None, 1), {1: f(1, 16), 2: f(5, 28), 3: f(1, 5), 4: f(5, 28), 5: f(5, 28),
                                                   6: f(4, 25), 7: f(1, 5), 8: f(1, 16), 9: f(7, 16), 10: f(5, 28)})
        self.check(E17, ('logage', None, None, 1), {1: f(1), 2: f(5), 3: f(2), 4: f(4), 5: f(4), 6: f(3), 7: f(2),
                                                    8: f(1), 9: f(6), 10: f(5)})
        self.check(E19, (2, f(10), f(2), 1), {1: f(720891, 22042832), 2: f(132345, 836528), 3: f(491691, 2340704),
                                              4: f(365312, 1920393), 5: f(1443725, 5974556), 6: f(1247104, 10295265),
                                              7: f(156111, 597683), 8: f(180160, 4013631), 9: f(381367, 631035),
                                              10: f(1456600, 8668639)})
        e18 = E18._scores(EX, B10, (None, f(2), 1), False)
        self.assertEqual(e18, E18._scores(EX, B10, (None, f(2), 1), True))
        self.assertEqual((e18[1], e18[2], e18[9], e18[10]),
                         (f(3245348069700918737, 12312977064543699845), f(14637830234015105351, 49052738629126710095),
                          f(1, 5), f(1, 5)))


class EachVariantsOwnRule(unittest.TestCase):
    """compute() equals the rule written again in this test, for every method, variant, game and barrel; and the
    variants of each method differ."""

    def test_scores(self):
        for profile in GAMES:
            target = deep_target(profile)
            for name, mod in MODULES.items():
                seen = {}
                for variant, cfg in SPEC[name].items():
                    with tempfile.TemporaryDirectory() as td:
                        _d, _r, view, task = view_for(Path(td), profile.game_id, name, variant, target)
                        out = mod.compute(task, view)
                        rows = view.simple_rows()
                    self.assertGreater(len(rows), 208)
                    for b in profile.barrels:
                        with self.subTest(game=profile.game_id, method=name, variant=variant, barrel=b.barrel_id):
                            want = own_rule(name, cfg, drawn_sets(rows, b), b.selected, b.high - b.low + 1)
                            got = out.barrels[b.barrel_id]
                            self.assertEqual(got.ranking.scores, {j: float(v) for j, v in want.items()})
                            self.assertIsNone(got.probability)
                            seen.setdefault(b.barrel_id, set()).add(tuple(want[j] for j in sorted(want)))
                for bid, values in seen.items():
                    self.assertEqual(len(values), 3, f'{profile.game_id} {name} {bid}: variants coincide')


class Relations(unittest.TestCase):
    """The design note's section 7, by ranked groups and exact identities."""

    def groups(self, scores, low):
        return score_groups([scores[j] for j in sorted(scores)], low)

    def test_e17_log_age_ranks_purely_by_projected_age(self):
        for profile in GAMES:
            with self.subTest(game=profile.game_id), tempfile.TemporaryDirectory() as td:
                _d, _r, view, task = view_for(Path(td), profile.game_id, 'E_17', 'HAZARD_LOGAGE_SIGN_V1',
                                              deep_target(profile))
                out = E17.compute(task, view)
                rows = view.simple_rows()
                for b in profile.barrels:
                    drawn = drawn_sets(rows, b)
                    ages = {j: len(drawn) + 1 - (positions(drawn, j) or [0])[-1] for j in range(b.low, b.high + 1)}
                    sc = out.barrels[b.barrel_id].ranking.scores
                    v = sc[max(ages, key=ages.get)]
                    sigma = (v > 0) - (v < 0)
                    self.assertNotEqual(sigma, 0)
                    self.assertEqual(sc, {j: float(sigma * g) for j, g in ages.items()})
                    self.assertEqual(self.groups(sc, b.low), self.groups({j: sigma * g for j, g in ages.items()}, b.low))

    def test_e17_bins_tie_within_a_bin(self):
        s = E17._scores(EX, B10, ('bins', Fr(10), None, 1), False)
        self.assertEqual(s[4], s[5])                                   # ages 4 and 4
        self.assertEqual(s[2], s[10])                                  # ages 5 and 5, the same bin as 4
        self.assertEqual(s[2], s[4])

    def test_e19_divided_by_e17_bins_is_the_periodic_factor(self):
        for T in (2, 3, 4):
            e19 = E19._scores(EX, B10, (T, Fr(10), Fr(2), 1), False)
            e17 = E17._scores(EX, B10, ('bins', Fr(10), None, 1), False)
            drawn = [set(d) for d in EX]
            want = own_rule('E_19', (T, Fr(10), Fr(2), 1), drawn, 2, 10)
            for j in e19:
                h = own_rule('E_17', ('bins', Fr(10), None, 1), drawn, 2, 10)[j]
                self.assertEqual(e19[j] / e17[j], want[j] / h)

    def test_e18_nests_the_fair_law(self):
        b = NS(barrel_id='MAIN', low=1, high=5, selected=1)
        draws = [[1], [2], [1], [3], [1], [2], [1]]                     # labels 4 and 5 never drawn, label 3 once
        for second in (False, True):
            s = E18._scores(draws, b, (None, Fr(10), 1), second)
            for j in (3, 4, 5):
                self.assertEqual(s[j], Fr(1, 5))                       # no completed gap: FAIR exactly, score r


class InsufficientHistory(unittest.TestCase):
    def test_too_few_draws_gives_an_insufficient_history_record(self):
        cases = [('E_2', 'RECUR_MEAN_ALL_V1', 30), ('E_17', 'HAZARD_BINS_W208_C100_V1', 150),
                 ('E_18', 'MIX4_W208_C10_V1', 150), ('E_19', 'PERIODIC_T2_V1', 50)]
        for name, variant, n in cases:
            with self.subTest(method=name), tempfile.TemporaryDirectory() as td:
                d, _r, view, task = view_for(Path(td), 'POWERBALL', name, variant, POWERBALL.first_draw + n)
                out = MODULES[name].compute(task, view)
                self.assertEqual(dict(out.barrels), {})
                rec = assemble_forecast(d, task, view, out)
                self.assertEqual(rec['record_status'], 'INSUFFICIENT_HISTORY')
                MODULES[name].verify(task, view, rec, None)

    def test_exactly_the_minimum_is_enough(self):
        for name, variant in (('E_17', 'HAZARD_LOGAGE_SIGN_V1'), ('E_18', 'MIX4_W104_C10_V1')):
            minimum = SPEC[name][variant][-1]
            with self.subTest(method=name), tempfile.TemporaryDirectory() as td:
                d, _r, view, task = view_for(Path(td), 'POWERBALL', name, variant, POWERBALL.first_draw + minimum)
                self.assertEqual(len(view.simple_rows()), minimum)
                self.assertEqual(sorted(MODULES[name].compute(task, view).barrels), ['MAIN', 'POWERBALL'])


class NoPeeking(unittest.TestCase):
    def test_record_identical_whatever_the_target_and_later_rows_say(self):
        for profile in GAMES:
            for name, mod in MODULES.items():
                for variant in SPEC[name]:
                    with self.subTest(game=profile.game_id, method=name, variant=variant):
                        digests = set()
                        for suffix in (0, 1, 2):
                            with tempfile.TemporaryDirectory() as td:
                                d, _r, view, task = view_for(Path(td), profile.game_id, name, variant,
                                                             deep_target(profile), suffix)
                                digests.add(assemble_forecast(d, task, view, mod.compute(task, view))['canonical_content_digest'])
                        self.assertEqual(len(digests), 1)


class ThroughTheContract(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.td = Path(self._td.name)
        self.data = C.copy_data_root(self.td)
        reg = InstalledRegistry(self.data)
        self.released = {}
        for profile in GAMES:
            for name in MODULES:
                for variant in SPEC[name]:
                    e1 = reg.active_entry(profile.game_id, name, variant)
                    e2 = dict(e1, entry_sequence=2, registry_status='SUPPORTED', previous_entry_digest=record_digest(e1),
                              registry_status_reason='test harness: simulated release')
                    C.append_entry(self.data, e2)
                    self.released[(profile.game_id, name, variant)] = (reg.declaration(e1['declaration_digest']), e2)
        (self.td / 'methods').mkdir()
        self.ctx = C.installed(data=self.data, methods=self.td / 'methods', marker=self.td / 'no_marker')
        self.ctx.__enter__()

    def tearDown(self):
        self.ctx.__exit__(None, None, None)
        self._td.cleanup()

    def run_one(self, profile, name, variant, compute, verify, tag):
        target = deep_target(profile)
        ws = self.td / f'ws_{tag}'
        sha = write_varied_master(ws, profile, target, 0)
        d, e = self.released[(profile.game_id, name, variant)]
        req = C.request(d, e, target, sha, run_id=CP.new_run_id())
        return CR.run_contract_method(req, compute=compute, verify=verify, repo_root=ws, run_root=self.td / 'runs')

    def test_every_variant_runs_and_is_consumable(self):
        for profile in GAMES:
            for name, mod in MODULES.items():
                for variant in SPEC[name]:
                    with self.subTest(game=profile.game_id, method=name, variant=variant):
                        res = self.run_one(profile, name, variant, mod.compute, mod.verify,
                                           f'{profile.game_id}_{name}_{variant}')
                        self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: PREDICTION_AVAILABLE'))
                        rec = json.loads((res.folder / 'forecast.json').read_bytes())
                        for b in profile.barrels:
                            self.assertEqual(rec['barrels'][b.barrel_id]['probability']['kind'], 'NONE')
                        self.assertEqual(read_run(res.folder)['forecast'], (True, 'CONSUMABLE'))

    def test_verify_refuses_a_record_that_differs(self):
        for name, mod in MODULES.items():
            variant = next(iter(SPEC[name]))
            with self.subTest(method=name):

                def tampered(task, view, mod=mod):
                    out = mod.compute(task, view)
                    sc = dict(out.barrels['MAIN'].ranking.scores)
                    hi, lo = max(sc, key=sc.get), min(sc, key=sc.get)
                    sc[hi], sc[lo] = sc[lo], sc[hi]
                    return MethodOutput(barrels=dict(out.barrels, MAIN=BarrelOutput(ranking=ScoredRanking(sc))))
                res = self.run_one(POWERBALL, name, variant, tampered, mod.verify, f'bad_{name}')
                self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
                self.assertIn(f'{name} check', res.reason)

    def test_verify_refuses_a_flipped_log_age_sign(self):
        def flipped(task, view):
            out = E17.compute(task, view)
            sc = {j: -v for j, v in out.barrels['MAIN'].ranking.scores.items()}
            return MethodOutput(barrels=dict(out.barrels, MAIN=BarrelOutput(ranking=ScoredRanking(sc))))
        res = self.run_one(POWERBALL, 'E_17', 'HAZARD_LOGAGE_SIGN_V1', flipped, E17.verify, 'flip')
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertIn('E_17 check', res.reason)

    def test_e18_verify_refuses_weights_that_are_not_optimal(self):
        fair_only = lambda q, P, Pf: [Fr(0), Fr(1), Fr(0), Fr(0)]      # noqa: E731 - feasible, but not the optimum
        with mock.patch.object(E18, 'fit_weights', fair_only):
            res = self.run_one(POWERBALL, 'E_18', 'MIX4_ALL_C10_V1', E18.compute, E18.verify, 'kkt')
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertIn('optimality certificate', res.reason)

    def test_compute_refuses_a_task_it_was_not_written_for(self):
        from _common.contract_task import MethodTask
        with tempfile.TemporaryDirectory() as td:
            _d, _r, view, task = view_for(Path(td), 'POWERBALL', 'E_2', 'RECUR_MEAN_ALL_V1', deep_target(POWERBALL))
            for mod, change in ((E2, {'method_id': 'E_17'}), (E17, {}), (E18, {}), (E19, {}),
                                (E2, {'variant_id': 'RECUR_OTHER_V1'}),
                                (E2, {'observation_view': 'OPERATOR_DRAWN_ORDER'}), (E2, {'include_dates': True})):
                with self.subTest(module=mod.METHOD_ID, change=change):
                    with self.assertRaises(ValueError):
                        mod.compute(MethodTask(**dict(task.as_dict(), **change)), view)


class AsInstalled(unittest.TestCase):
    def test_declarations_and_entries_match_the_specification(self):
        reg = InstalledRegistry()
        for name in MODULES:
            for game in ('POWERBALL', 'OZLOTTO'):
                self.assertEqual(len(reg.chain(game, name, 'NOT_YET_SPECIFIED')), 1)   # the placeholder stays
                for variant, cfg in SPEC[name].items():
                    chain = reg.chain(game, name, variant)
                    self.assertEqual([(e['entry_sequence'], e['registry_status']) for e in chain], [(1, 'FORMULA_OPEN')])
                    d = reg.declaration(chain[0]['declaration_digest'])
                    self.assertEqual((d['minimum_history_draws'], d['fit_sampling_model_version'], d['observation_views'],
                                      d['uses_dates'], d['stochastic_fit'], d['diagnostic_schema_id']),
                                     (cfg[-1], FIT_VERSION[name], ['UNORDERED_SET'], False, False, None))
                    for ch in d['channels'].values():
                        self.assertEqual((ch['ranking_kind'], ch['probability_kind'], ch['probability_sum_tolerance']),
                                         ('RANKING_WITH_SCORES', 'NONE', None))

    def test_every_request_is_refused_and_the_roster_says_formula_open(self):
        reg = InstalledRegistry()
        for name in MODULES:
            for profile in GAMES:
                for variant in SPEC[name]:
                    e = reg.active_entry(profile.game_id, name, variant)
                    req = C.request(reg.declaration(e['declaration_digest']), e, profile.first_draw + 10, 'f' * 64)
                    with self.assertRaises(DispatchRefused) as cm:
                        dispatch_gate(req)
                    self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
                self.assertEqual(method_status(profile.game_id, name), 'FORMULA_OPEN')

    def test_flags_present_and_runner_lists_each(self):
        import Method_Contract_Runner as M
        for name, mod in MODULES.items():
            self.assertTrue((METHODS_ROOT / method_folder(name) / 'IN_DEVELOPMENT.txt').is_file())
            self.assertIs(M.ADAPTERS[name], mod)


class FolderGuards(unittest.TestCase):
    def test_method_folders_are_exactly_these_files_and_read_nothing(self):
        for name in MODULES:
            folder = METHODS_ROOT / method_folder(name)
            self.assertEqual(sorted(p.name for p in folder.iterdir() if p.name != '__pycache__'),
                             ['IN_DEVELOPMENT.txt', '__init__.py', 'contract.py', 'variants.py'])
            for f in sorted(folder.glob('*.py')):
                text = f.read_text('utf-8')
                for word in ('game_draws_reader', 'source' + '_data', 'contract_receipts', 'contract_publication',
                             'contract_runner', 'open(', 'read_bytes', 'write_bytes', 'import os', 'subprocess',
                             'import math', 'numpy', 'scipy', 'random', 'decimal', '** 0.5', 'FILL' + ' IN'):
                    self.assertNotIn(word, text, f'{f.name} mentions {word}')


if __name__ == '__main__':
    unittest.main()
