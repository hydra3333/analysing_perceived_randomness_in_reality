"""Wave 1 revision 1 (E_7, E_8, E_9, E_10): variants, each variant's own rule, normalisation, overlap, no peeking.

OFFLINE, synthetic only. Every master here is invented and written to a temporary folder; no file under the
repository's data folders is opened and no real draw value is read. The installed contract data is only read.
Specification: doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md. Built from the new-method
template (doc/METHOD_TEMPLATE/test_template.py.txt).
"""
from __future__ import annotations

from fractions import Fraction as Fr
import json
import math
from pathlib import Path
import tempfile
import unittest

import e2r_fixtures as F
import e2r_code2_fixtures as C
from test_e6_beta_bernoulli import write_varied_master

from _common import contract_publication as CP
from _common import contract_runner as CR
from _common.contract_dispatch import DispatchRefused, dispatch_gate, METHODS_ROOT, method_folder
from _common.contract_forecast import assemble_forecast, BarrelOutput, MethodOutput, ProbabilityVector, ScoredRanking
from _common.contract_publication import read_run
from _common.contract_records import record_digest, score_groups
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from _common.multigame_method_registry import method_status
from E_007 import contract as E7
from E_008 import contract as E8
from E_009 import contract as E9
from E_010 import contract as E10

GAMES = (POWERBALL, OZLOTTO)
MODULES = {'E_7': E7, 'E_8': E8, 'E_9': E9, 'E_10': E10}
PROBS = {'E_7': True, 'E_8': True, 'E_9': False, 'E_10': False}
SPEC = {   # design note v0.1r1 section 6, written out here (not read from the modules); last item = minimum history
    'E_7': {'BETA_SHRINK_W52_C52_V1': (52, 52, 52), 'BETA_SHRINK_W104_C52_V1': (104, 52, 104),
            'BETA_SHRINK_FULL_C52_V1': (None, 52, 1)},
    'E_8': {'HIER_PERIODS_P13_V1': (13, 26), 'HIER_PERIODS_P26_V1': (26, 52), 'HIER_PERIODS_P52_V1': (52, 104)},
    'E_9': {'EXP_DECAY_5_6_V1': (Fr(5, 6), 1), 'EXP_DECAY_18_19_V1': (Fr(18, 19), 1),
            'EXP_DECAY_37_38_V1': (Fr(37, 38), 1)},
    'E_10': {'CONTRAST_S13_L104_V1': (13, 104, 104), 'CONTRAST_S26_L208_V1': (26, 208, 208),
             'CONTRAST_S52_FULL_V1': (52, None, 104)},
}
FIT_VERSION = {'E_7': 'BETA_SHRINKAGE_WINDOW_V1', 'E_8': 'HIER_BETA_BINOMIAL_PERIODS_MOM_V1',
               'E_9': 'EXP_DECAYED_COUNT_V1', 'E_10': 'TWO_WINDOW_RATE_CONTRAST_V1'}


def view_for(td: Path, game: str, method: str, variant: str, target: int, suffix: int = 0):
    sha = write_varied_master(td, get_profile(game), target, suffix)
    reg = InstalledRegistry()
    d = reg.declaration(reg.active_entry(game, method, variant)['declaration_digest'])
    req, view, task = F.load_view(td, d, target, 'UNORDERED_SET', sha)
    return d, req, view, task


def deep_target(profile):
    """A development target with more than 208 eligible draws in both games."""
    return F.targets(profile)[2]


def series(rows, b):
    """For each label, its 0/1 inclusion series over the rows, oldest first (computed here, from scratch)."""
    drawn = [set(r['main']) if b.barrel_id == 'MAIN' else {r['powerball']} for r in rows]
    return {j: [1 if j in d else 0 for d in drawn] for j in range(b.low, b.high + 1)}


def own_rule(method, cfg, x, K, L):
    """Each method's rule written again here from the design note, per label (x: {label: 0/1 series})."""
    r, W = Fr(K, L), len(next(iter(x.values())))
    if method == 'E_7':
        M, c, _m = cfg
        size = W if M is None else M
        return {j: (c * r + sum(s[W - size:])) / (c + size) for j, s in x.items()}
    if method == 'E_9':
        lam, _m = cfg
        return {j: sum(lam ** (W - 1 - i) * v for i, v in enumerate(s)) for j, s in x.items()}
    if method == 'E_10':
        S, Lw, _m = cfg
        long = W if Lw is None else Lw
        return {j: Fr(sum(s[W - S:]), S) - Fr(sum(s[W - long:W - S]), long - S) for j, s in x.items()}
    P, _m = cfg
    n = W // P
    rates = {j: [Fr(sum(s[W - (n - b) * P:W - (n - b - 1) * P]), P) for b in range(n)] for j, s in x.items()}
    excess, m = [], {}
    for j, p in rates.items():
        mean = sum(p, Fr(0)) / n
        var = sum(((v - mean) ** 2 for v in p), Fr(0)) / (n - 1)
        excess.append((var - (mean * (1 - mean) + var / n) / P) * Fr(P, P - 1))
        m[j] = mean
    t = min(max(Fr(0), sum(excess, Fr(0)) / L), r * (1 - r))
    w = (P * t) / ((P - 1) * t + r * (1 - r))
    return {j: w * rates[j][-1] + (1 - w) * m[j] for j in rates}


class Variants(unittest.TestCase):
    def test_tables_are_exactly_the_specification(self):
        for name, mod in MODULES.items():
            from importlib import import_module
            table = import_module(f'{method_folder(name)}.variants').VARIANTS
            self.assertEqual({v: tuple(c) for v, c in table.items()},
                             {v: tuple(Fr(x) if name == 'E_7' and i == 1 else x for i, x in enumerate(c))
                              for v, c in SPEC[name].items()})

    def test_e9_factors_and_half_lives_stay_clear_of_e6(self):
        from E_006.beta_bernoulli import VARIANTS as V6
        halves = {round(math.log(0.5) / math.log(float(lam)), 1) for lam, _m in SPEC['E_9'].values()}
        self.assertEqual(halves, {3.8, 12.8, 26.0})
        self.assertFalse({lam for lam, _m in SPEC['E_9'].values()} & set(V6.values()))


class WorkedExamples(unittest.TestCase):
    """The design note's section 9, through each module's own rule, both routes."""
    from types import SimpleNamespace as _NS
    B5 = _NS(barrel_id='MAIN', low=1, high=5, selected=2)
    B4 = _NS(barrel_id='MAIN', low=1, high=4, selected=2)
    EX = [[1, 2], [1, 3], [2, 4], [1, 5]]

    def check(self, mod, b, draws, cfg, want):
        for second in (False, True):
            self.assertEqual(mod._scores(draws, b, cfg, second), want)

    def test_all_examples(self):
        f = Fr
        self.check(E7, self.B5, self.EX, (2, f(2), 1), {1: f(9, 20), 2: f(9, 20), 3: f(1, 5), 4: f(9, 20), 5: f(9, 20)})
        self.check(E7, self.B5, self.EX, (None, f(2), 1), {1: f(19, 30), 2: f(7, 15), 3: f(3, 10), 4: f(3, 10), 5: f(3, 10)})
        self.check(E9, self.B5, self.EX, (f(1, 2), 1), {1: f(11, 8), 2: f(5, 8), 3: f(1, 4), 4: f(1, 2), 5: f(1)})
        self.check(E10, self.B5, self.EX, (2, 4, 4), {1: f(-1, 2), 2: f(0), 3: f(-1, 2), 4: f(1, 2), 5: f(1, 2)})
        self.check(E8, self.B5, self.EX, (2, 4), {1: f(3, 4), 2: f(1, 2), 3: f(1, 4), 4: f(1, 4), 5: f(1, 4)})
        cap = [[2, 4], [2, 4], [2, 4], [1, 2], [1, 3], [1, 3]]
        self.check(E8, self.B4, cap, (2, 4), {1: f(1), 2: f(0), 3: f(1), 4: f(0)})


class EachVariantsOwnRule(unittest.TestCase):
    """compute() equals the rule written again in this test, for every method, variant, game and barrel; and the
    variants of each method differ."""

    def test_scores_and_probabilities(self):
        for profile in GAMES:
            target = deep_target(profile)
            for name, mod in MODULES.items():
                seen = {}
                for variant, cfg in SPEC[name].items():
                    with tempfile.TemporaryDirectory() as td:
                        _d, _r, view, task = view_for(Path(td), profile.game_id, name, variant, target)
                        out = mod.compute(task, view)
                        rows = view.simple_rows()
                    for b in profile.barrels:
                        with self.subTest(game=profile.game_id, method=name, variant=variant, barrel=b.barrel_id):
                            want = own_rule(name, cfg, series(rows, b), b.selected, b.high - b.low + 1)
                            got = out.barrels[b.barrel_id]
                            self.assertEqual(got.ranking.scores, {j: float(v) for j, v in want.items()})
                            if PROBS[name]:
                                self.assertEqual(sum(want.values()), b.selected)          # exact
                                self.assertTrue(all(0 <= v <= 1 for v in want.values()))
                                self.assertEqual(list(got.probability.vector), [float(want[j]) for j in sorted(want)])
                                self.assertLess(abs(sum(got.probability.vector) - b.selected), 1e-12)
                            else:
                                self.assertIsNone(got.probability)
                            seen.setdefault(b.barrel_id, []).append((tuple(got.ranking.scores[j] for j in sorted(want)),
                                                                     tuple(want[j] for j in sorted(want))))
                for bid, pairs in seen.items():
                    # variants differ exactly where their correct values differ (E_8's variants coincide when the
                    # weight is 0 and their periods cover the same draws, design note section 7)
                    self.assertEqual(len({g for g, _w in pairs}), len({w for _g, w in pairs}),
                                     f'{profile.game_id} {name} {bid}')
                    if name != 'E_8':
                        self.assertEqual(len({w for _g, w in pairs}), len(SPEC[name]))


class HonestOverlap(unittest.TestCase):
    """The design note's section 7, by ranked groups (not TOP and WORST)."""

    def groups(self, scores, low):
        return score_groups([scores[j] for j in sorted(scores)], low)

    def test_e7_full_history_has_e1s_groups_and_e9_at_e6s_factor_has_e6s(self):
        from E_006.beta_bernoulli import VARIANTS as V6, posterior_means
        for profile in GAMES:
            with self.subTest(game=profile.game_id), tempfile.TemporaryDirectory() as td:
                _d, _r, view, task = view_for(Path(td), profile.game_id, 'E_7', 'BETA_SHRINK_FULL_C52_V1',
                                              deep_target(profile))
                out = E7.compute(task, view)
                rows = view.simple_rows()
                for b in profile.barrels:
                    x = series(rows, b)
                    counts = {j: sum(s) for j, s in x.items()}
                    self.assertEqual(self.groups(out.barrels[b.barrel_id].ranking.scores, b.low),
                                     self.groups(counts, b.low))
                    self.assertGreater(len(self.groups(counts, b.low)), 1)
                    draws = [[j for j in x if x[j][i]] for i in range(len(rows))]
                    lam = V6['BETA_BERNOULLI_DECAY_74_75_V1']
                    e9_like = E9._scores(draws, b, (lam, 1), False)
                    e6 = posterior_means(draws, b.low, b.high, b.selected, lam)
                    self.assertEqual(self.groups(e9_like, b.low), self.groups(e6, b.low))

    def test_e8_with_zero_weight_ranks_by_the_count_over_its_periods(self):
        from types import SimpleNamespace as NS
        b = NS(barrel_id='MAIN', low=1, high=5, selected=2)
        ex = [[1, 2], [1, 3], [2, 4], [1, 5]]                      # the worked example: weight 0
        s = E8._scores(ex, b, (2, 4), False)
        self.assertEqual(self.groups(s, 1), self.groups({1: 3, 2: 2, 3: 1, 4: 1, 5: 1}, 1))

    def test_e10_ranks_differently_from_its_short_window_alone(self):
        for profile in GAMES:
            with self.subTest(game=profile.game_id), tempfile.TemporaryDirectory() as td:
                _d, _r, view, task = view_for(Path(td), profile.game_id, 'E_10', 'CONTRAST_S13_L104_V1',
                                              deep_target(profile))
                main = E10.compute(task, view).barrels['MAIN'].ranking.scores
                short = {j: sum(s[-13:]) for j, s in series(view.simple_rows(), profile.barrels[0]).items()}
                self.assertNotEqual(self.groups(main, 1), self.groups(short, 1))


class InsufficientHistory(unittest.TestCase):
    def test_too_few_draws_gives_an_insufficient_history_record(self):
        cases = [('E_7', 'BETA_SHRINK_W52_C52_V1'), ('E_8', 'HIER_PERIODS_P26_V1'), ('E_10', 'CONTRAST_S13_L104_V1')]
        for name, variant in cases:
            with self.subTest(method=name), tempfile.TemporaryDirectory() as td:
                d, _r, view, task = view_for(Path(td), 'POWERBALL', name, variant, POWERBALL.first_draw + 30)
                out = MODULES[name].compute(task, view)
                self.assertEqual(dict(out.barrels), {})
                rec = assemble_forecast(d, task, view, out)
                self.assertEqual(rec['record_status'], 'INSUFFICIENT_HISTORY')
                MODULES[name].verify(task, view, rec, None)

    def test_exactly_the_minimum_is_enough(self):
        for name, variant in (('E_8', 'HIER_PERIODS_P13_V1'), ('E_7', 'BETA_SHRINK_FULL_C52_V1')):
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

    def test_every_variant_runs_and_is_consumable(self):
        for profile in GAMES:
            target = deep_target(profile)
            ws = self.td / f'ws_{profile.game_id}'
            sha = write_varied_master(ws, profile, target, 0)
            for name, mod in MODULES.items():
                for variant in SPEC[name]:
                    with self.subTest(game=profile.game_id, method=name, variant=variant):
                        d, e = self.released[(profile.game_id, name, variant)]
                        req = C.request(d, e, target, sha, run_id=CP.new_run_id())
                        res = CR.run_contract_method(req, compute=mod.compute, verify=mod.verify, repo_root=ws,
                                                     run_root=self.td / 'runs')
                        self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: PREDICTION_AVAILABLE'))
                        rec = json.loads((res.folder / 'forecast.json').read_bytes())
                        for b in profile.barrels:
                            kind = rec['barrels'][b.barrel_id]['probability']['kind']
                            want = ('NONE' if not PROBS[name] else
                                    'MARGINAL_INCLUSION_PROBABILITY' if b.barrel_id == 'MAIN' else 'PB_CATEGORICAL')
                            self.assertEqual(kind, want)
                        self.assertEqual(read_run(res.folder)['forecast'], (True, 'CONSUMABLE'))

    def test_verify_refuses_a_record_that_differs(self):
        target = deep_target(POWERBALL)
        ws = self.td / 'ws_bad'
        sha = write_varied_master(ws, POWERBALL, target, 0)
        for name, mod in MODULES.items():
            variant = next(iter(SPEC[name]))
            with self.subTest(method=name):
                d, e = self.released[('POWERBALL', name, variant)]

                def tampered(task, view, mod=mod):
                    out = mod.compute(task, view)
                    main = out.barrels['MAIN']
                    sc = dict(main.ranking.scores)
                    hi, lo = max(sc, key=sc.get), min(sc, key=sc.get)
                    sc[hi], sc[lo] = sc[lo], sc[hi]
                    prob = None if main.probability is None else ProbabilityVector(
                        [sc[j] for j in sorted(sc)], main.probability.provenance)
                    return MethodOutput(barrels=dict(out.barrels, MAIN=BarrelOutput(ranking=ScoredRanking(sc), probability=prob)))
                req = C.request(d, e, target, sha, run_id=CP.new_run_id())
                res = CR.run_contract_method(req, compute=tampered, verify=mod.verify, repo_root=ws,
                                             run_root=self.td / 'runs')
                self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
                self.assertIn(f'{name} check', res.reason)

    def test_verify_refuses_a_probability_vector_that_differs_with_the_same_scores(self):
        target = deep_target(POWERBALL)
        ws = self.td / 'ws_prob'
        sha = write_varied_master(ws, POWERBALL, target, 0)
        for name in ('E_7', 'E_8'):
            mod = MODULES[name]
            variant = next(iter(SPEC[name]))
            with self.subTest(method=name):
                d, e = self.released[('POWERBALL', name, variant)]

                def tampered(task, view, mod=mod):
                    out = mod.compute(task, view)
                    main = out.barrels['MAIN']
                    vec = list(main.probability.vector)
                    hi, lo = vec.index(max(vec)), vec.index(min(vec))
                    vec[hi], vec[lo] = vec[lo], vec[hi]             # the sum is unchanged; the scores untouched
                    self.assertNotEqual(vec, list(main.probability.vector))
                    prob = ProbabilityVector(vec, main.probability.provenance)
                    return MethodOutput(barrels=dict(out.barrels, MAIN=BarrelOutput(ranking=main.ranking, probability=prob)))
                req = C.request(d, e, target, sha, run_id=CP.new_run_id())
                res = CR.run_contract_method(req, compute=tampered, verify=mod.verify, repo_root=ws,
                                             run_root=self.td / 'runs')
                self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
                self.assertIn(f'{name} check', res.reason)

    def test_compute_refuses_a_task_it_was_not_written_for(self):
        from _common.contract_task import MethodTask
        with tempfile.TemporaryDirectory() as td:
            _d, _r, view, task = view_for(Path(td), 'POWERBALL', 'E_7', 'BETA_SHRINK_W52_C52_V1', deep_target(POWERBALL))
            for mod, change in ((E7, {'method_id': 'E_8'}), (E8, {}), (E9, {}), (E10, {}),
                                (E7, {'variant_id': 'BETA_OTHER_V1'}),
                                (E7, {'observation_view': 'OPERATOR_DRAWN_ORDER'}), (E7, {'include_dates': True})):
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
                    for bid, ch in d['channels'].items():
                        kind = ('NONE' if not PROBS[name] else
                                'MARGINAL_INCLUSION_PROBABILITY' if bid == 'MAIN' else 'PB_CATEGORICAL')
                        self.assertEqual((ch['ranking_kind'], ch['probability_kind'],
                                          ch['probability_sum_tolerance']),
                                         ('RANKING_WITH_SCORES', kind, 1e-12 if PROBS[name] else None))

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
                             'import math', 'numpy', 'scipy', 'random', 'FILL' + ' IN'):
                    self.assertNotIn(word, text, f'{f.name} mentions {word}')


if __name__ == '__main__':
    unittest.main()
