"""E_6 revision 1 (Beta-Bernoulli posterior means): specification, E_1 match, no peeking, release state.

OFFLINE, synthetic only. Every master here is invented and written to a temporary folder; no file under the
repository's data folders is opened and no real draw value is read. The installed contract data is only read.
Specification: doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import shutil
import tempfile
import unittest

import e2r_fixtures as F
import e2r_code2_fixtures as C
from e2r_fixtures import ROOT

from _common import contract_publication as CP
from _common import contract_runner as CR
from _common.contract_dispatch import DispatchRefused, dispatch_gate, METHODS_ROOT
from _common.contract_forecast import assemble_forecast, BarrelOutput, MethodOutput, ScoredRanking, ProbabilityVector
from _common.contract_publication import read_run
from _common.contract_records import record_digest, score_groups
from _common.contract_registry import InstalledRegistry
from _common.game_draws_reader import header_for
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from _common.multigame_method_registry import method_status
from E_006 import contract as E6
from E_006.beta_bernoulli import VARIANTS, posterior_means, posterior_means_by_recursion

GAMES = (POWERBALL, OZLOTTO)
FULL = 'BETA_BERNOULLI_FULL_MEMORY_V1'
FILES = ('{g}_results_master.csv', '{g}_results_master_ledger.csv', '{g}_results_master_init_verification.json')


# ---------------------------------------------------------------- an invented, varied synthetic master

def _pick(seed: str, low: int, high: int, k: int, exclude=()) -> list[int]:
    labels = [x for x in range(low, high + 1) if x not in exclude]
    labels.sort(key=lambda x: hashlib.sha256(f'{seed}:{x}'.encode()).digest())
    return labels[:k]


def varied_row(profile, draw: int, variant: int) -> str:
    """An invented, structurally valid row whose numbers vary from draw to draw. Never a real result.
    variant 0 is the base; 1 and 2 give different numbers (used only at and after the target)."""
    seed = f'{profile.game_id}:{draw}:{variant}'
    main = _pick(seed + ':main', 1, 35 if profile is POWERBALL else 47, 7)
    extra = [_pick(seed + ':pb', 1, 20, 1)[0]] if profile is POWERBALL else _pick(seed + ':sup', 1, 47, 3, main)
    return ','.join(map(str, [draw, profile.derived_date(draw).isoformat(), *main, *extra]))


def write_varied_master(root: Path, profile, target: int, variant: int) -> str:
    game = profile.game_id
    folder = root / 'source_data'
    folder.mkdir(parents=True, exist_ok=True)
    rows = [','.join(header_for(game))]
    rows += [varied_row(profile, d, 0 if d < target else variant) for d in range(profile.first_draw, profile.holdout_first)]
    raw = ('\n'.join(rows) + '\n').encode('ascii')
    sha = hashlib.sha256(raw).hexdigest()
    (folder / FILES[0].format(g=game)).write_bytes(raw)
    ledger = ('version,utc,action,master_sha256,first_draw,last_draw,draw_count\n'
              f'1,fixture,INIT,{sha},{profile.first_draw},{profile.holdout_first - 1},'
              f'{profile.holdout_first - profile.first_draw}\n')
    (folder / FILES[1].format(g=game)).write_bytes(ledger.encode('ascii'))
    (folder / FILES[2].format(g=game)).write_text(json.dumps({
        'master_sha256': sha, 'master_file': FILES[0].format(g=game), 'game': game,
        'first_draw': profile.first_draw, 'last_draw': profile.holdout_first - 1,
        'draw_count': profile.holdout_first - profile.first_draw, 'source': 'LOTTERYWEST_GOV_RESULTS_SEARCH'}))
    return sha


def installed_e6(game: str, variant: str):
    reg = InstalledRegistry()
    e = reg.active_entry(game, 'E_6', variant)
    return e, reg.declaration(e['declaration_digest'])


def e6_view(td: Path, game: str, variant: str, target: int, suffix: int = 0):
    """(declaration, request, view, task) for E_6 on an invented master."""
    sha = write_varied_master(td, get_profile(game), target, suffix)
    _e, d = installed_e6(game, variant)
    req, view, task = F.load_view(td, d, target, 'UNORDERED_SET', sha)
    return d, req, view, task


def targets(profile):
    return F.targets(profile)


# ---------------------------------------------------------------- 6.2 the worked example

class WorkedExample(unittest.TestCase):
    """Specification section 2.6: two eligible draws with no number in common, Powerball main barrel."""
    older, newest = [1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]

    def test_full_memory(self):
        p = posterior_means([self.older, self.newest], 1, 35, 7, Fraction(1))
        self.assertEqual((p[1], p[8], p[35]), (Fraction(2, 5), Fraction(2, 5), Fraction(1, 15)))
        both = posterior_means([self.older, self.older], 1, 35, 7, Fraction(1))
        self.assertEqual(both[1], Fraction(11, 15))
        self.assertEqual(sum(p.values()), 7)

    def test_decay_74_75(self):
        lam = VARIANTS['BETA_BERNOULLI_DECAY_74_75_V1']
        p = posterior_means([self.older, self.newest], 1, 35, 7, lam)
        self.assertEqual((p[8], p[1], p[35]), (Fraction(45, 112), Fraction(89, 224), Fraction(15, 224)))
        self.assertEqual(posterior_means([self.older, self.older], 1, 35, 7, lam)[1], Fraction(41, 56))
        self.assertEqual(sum(p.values()), 7)
        self.assertEqual(7 * Fraction(90, 224) + 7 * Fraction(89, 224) + 21 * Fraction(15, 224), 7)

    def test_powerball_barrel_sums_to_one(self):
        for lam in VARIANTS.values():
            p = posterior_means([[3], [3], [17]], 1, 20, 1, lam)
            self.assertEqual(sum(p.values()), 1)
            self.assertEqual(p[5], Fraction(1, 20) / (1 + 1 + lam + lam ** 2))

    def test_variant_table_is_exactly_the_specification(self):
        self.assertEqual(dict(VARIANTS), {'BETA_BERNOULLI_FULL_MEMORY_V1': Fraction(1),
                                          'BETA_BERNOULLI_DECAY_74_75_V1': Fraction(74, 75),
                                          'BETA_BERNOULLI_DECAY_149_150_V1': Fraction(149, 150)})
        for lam in VARIANTS.values():
            self.assertIs(type(lam), Fraction)

    def test_bad_inputs_are_refused(self):
        for draws in ([[1, 2, 3, 4, 5, 6]], [[1, 1, 2, 3, 4, 5, 6]], [[0, 1, 2, 3, 4, 5, 6]], [[1, 2, 3, 4, 5, 6, 36]],
                      [[1, 2, 3, 4, 5, 6, 7.0]]):
            with self.assertRaises(ValueError):
                posterior_means(draws, 1, 35, 7, Fraction(1))
        for lam in (Fraction(0), Fraction(3, 2), 0.5, 1):
            with self.assertRaises(ValueError):
                posterior_means([[1, 2, 3, 4, 5, 6, 7]], 1, 35, 7, lam)


# ---------------------------------------------------------------- 6.3 exact normalisation, two algorithms agree

class ExactNormalisation(unittest.TestCase):
    def test_exact_sums_and_float_tolerance(self):
        for profile in GAMES:
            for barrel in profile.barrels:
                draws = [_pick(f'n:{profile.game_id}:{barrel.barrel_id}:{i}', barrel.low, barrel.high, barrel.selected)
                         for i in range(120)]
                for name, lam in VARIANTS.items():
                    with self.subTest(game=profile.game_id, barrel=barrel.barrel_id, variant=name):
                        p = posterior_means(draws, barrel.low, barrel.high, barrel.selected, lam)
                        self.assertEqual(sum(p.values()), barrel.selected)
                        self.assertEqual(p, posterior_means_by_recursion(draws, barrel.low, barrel.high,
                                                                         barrel.selected, lam))
                        floats = [float(p[j]) for j in sorted(p)]
                        self.assertLessEqual(abs(math.fsum(floats) - barrel.selected), 1e-12)
                        self.assertTrue(all(0.0 < x < 1.0 for x in floats))

    def test_compute_uses_each_variant_own_factor(self):
        """compute() equals the specification formula for each variant's lambda, computed here directly
        (not through the module's own variant lookup), and the decay variants differ from full memory."""
        for profile in GAMES:
            target = targets(profile)[2]
            results = {}
            for variant, lam in (('BETA_BERNOULLI_FULL_MEMORY_V1', Fraction(1)),
                                 ('BETA_BERNOULLI_DECAY_74_75_V1', Fraction(74, 75)),
                                 ('BETA_BERNOULLI_DECAY_149_150_V1', Fraction(149, 150))):
                with self.subTest(game=profile.game_id, variant=variant), tempfile.TemporaryDirectory() as td:
                    _d, _req, view, task = e6_view(Path(td), profile.game_id, variant, target)
                    out = E6.compute(task, view)
                    rows = view.simple_rows()
                    n = len(rows)
                    for b in profile.barrels:
                        r = Fraction(b.selected, b.high - b.low + 1)
                        k = {j: Fraction(0) for j in range(b.low, b.high + 1)}
                        for i, row in enumerate(rows):
                            for j in (row['main'] if b.barrel_id == 'MAIN' else [row['powerball']]):
                                k[j] += lam ** (n - 1 - i)
                        total = sum(lam ** a for a in range(n))
                        want = [float((r + k[j]) / (1 + total)) for j in sorted(k)]
                        sc = out.barrels[b.barrel_id].ranking.scores
                        self.assertEqual([sc[j] for j in sorted(sc)], want)
                        self.assertEqual(list(out.barrels[b.barrel_id].probability.vector), want)
                        results.setdefault(b.barrel_id, {})[variant] = want
            for bid, by_variant in results.items():
                self.assertEqual(len({tuple(v) for v in by_variant.values()}), 3, f'{bid}: variants do not differ')

    def test_newest_draw_has_weight_one(self):
        lam = VARIANTS['BETA_BERNOULLI_DECAY_74_75_V1']
        older = [[1, 2, 3, 4, 5, 6, 7]] * 5
        p_old = posterior_means(older + [[8, 9, 10, 11, 12, 13, 14]], 1, 35, 7, lam)
        p_new = posterior_means([[8, 9, 10, 11, 12, 13, 14]] + older, 1, 35, 7, lam)
        self.assertGreater(p_new[1], p_old[1])     # 1..7 drawn most recently in p_new
        self.assertLess(p_new[8], p_old[8])


# ---------------------------------------------------------------- 6.1 E_1 match

class E1Match(unittest.TestCase):
    def test_full_memory_ranks_like_e1_counts(self):
        for profile in GAMES:
            for target in targets(profile)[:3]:
                with self.subTest(game=profile.game_id, target=target), tempfile.TemporaryDirectory() as td:
                    d, _req, view, task = e6_view(Path(td), profile.game_id, FULL, target)
                    out = E6.compute(task, view)
                    rows = view.simple_rows()
                    n = len(rows)
                    for b in profile.barrels:
                        counts = {j: 0 for j in range(b.low, b.high + 1)}
                        for r in rows:
                            for j in (r['main'] if b.barrel_id == 'MAIN' else [r['powerball']]):
                                counts[j] += 1
                        e1_groups = score_groups([counts[j] for j in sorted(counts)], b.low)
                        sc = out.barrels[b.barrel_id].ranking.scores
                        self.assertEqual(score_groups([sc[j] for j in sorted(sc)], b.low), e1_groups)
                        r = Fraction(b.selected, b.high - b.low + 1)
                        self.assertEqual([sc[j] for j in sorted(sc)],
                                         [float((r + counts[j]) / (1 + n)) for j in sorted(counts)])
                        self.assertGreater(len(e1_groups), 1)   # the invented data is not degenerate

    def test_contract_record_groups_equal_e1_record_groups(self):
        """Against E_1's own contract record: same equal-count groups in the same order (ties may differ)."""
        from contract_adapters import e_001
        for profile in GAMES:
            target = targets(profile)[1]
            with self.subTest(game=profile.game_id), tempfile.TemporaryDirectory() as td:
                d6, _r, view6, task6 = e6_view(Path(td), profile.game_id, FULL, target)
                rec6 = assemble_forecast(d6, task6, view6, E6.compute(task6, view6))
                reg = InstalledRegistry()
                e1 = reg.active_entry(profile.game_id, *C.E1)
                d1 = reg.declaration(e1['declaration_digest'])
                sha = write_varied_master(Path(td), profile, target, 0)
                _req1, view1, task1 = F.load_view(Path(td), d1, target, 'UNORDERED_SET', sha)
                rec1 = assemble_forecast(d1, task1, view1, e_001.compute(task1, view1))
                for bid in rec1['barrels']:
                    self.assertEqual(rec6['barrels'][bid]['ranked_groups'], rec1['barrels'][bid]['ranked_groups'])


# ---------------------------------------------------------------- 6.4 no peeking (T-05 for E_6)

class NoPeeking(unittest.TestCase):
    def test_record_identical_whatever_the_target_and_later_rows_say(self):
        for profile in GAMES:
            for variant in VARIANTS:
                for target in targets(profile)[:2]:
                    with self.subTest(game=profile.game_id, variant=variant, target=target):
                        digests = set()
                        for suffix in (0, 1, 2):
                            with tempfile.TemporaryDirectory() as td:
                                d, _req, view, task = e6_view(Path(td), profile.game_id, variant, target, suffix)
                                rec = assemble_forecast(d, task, view, E6.compute(task, view))
                                digests.add(rec['canonical_content_digest'])
                        self.assertEqual(len(digests), 1)

    def test_the_suffix_variants_really_differ(self):
        p = POWERBALL
        t = targets(p)[1]
        self.assertNotEqual(varied_row(p, t, 0), varied_row(p, t, 1))
        self.assertNotEqual(varied_row(p, t, 0), varied_row(p, t, 2))


# ---------------------------------------------------------------- 6.5 through the contract, under a simulated release

class ThroughTheContract(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.td = Path(self._td.name)
        self.data = C.copy_data_root(self.td)
        reg = InstalledRegistry(self.data)
        self.released = {}
        for game in ('POWERBALL', 'OZLOTTO'):
            for variant in VARIANTS:
                e1 = reg.active_entry(game, 'E_6', variant)
                d = reg.declaration(e1['declaration_digest'])
                e2 = dict(e1, entry_sequence=2, registry_status='SUPPORTED', previous_entry_digest=record_digest(e1),
                          registry_status_reason='test harness: simulated release')
                C.append_entry(self.data, e2)
                self.released[(game, variant)] = (d, e2)
        self.methods = self.td / 'methods'          # a method tree with no IN_DEVELOPMENT.txt
        self.methods.mkdir()
        self.ctx = C.installed(data=self.data, methods=self.methods, marker=self.td / 'no_marker')
        self.ctx.__enter__()

    def tearDown(self):
        self.ctx.__exit__(None, None, None)
        self._td.cleanup()

    def test_every_variant_runs_publishes_and_is_consumable(self):
        for profile in GAMES:
            target = targets(profile)[2]
            ws = self.td / f'ws_{profile.game_id}'
            sha = write_varied_master(ws, profile, target, 0)
            for variant in VARIANTS:
                with self.subTest(game=profile.game_id, variant=variant):
                    d, e = self.released[(profile.game_id, variant)]
                    req = C.request(d, e, target, sha, run_id=CP.new_run_id())
                    res = CR.run_contract_method(req, compute=E6.compute, verify=E6.verify, repo_root=ws,
                                                 run_root=self.td / 'runs')
                    self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: PREDICTION_AVAILABLE'))
                    c1 = json.loads((res.folder / 'forecast.json').read_bytes())
                    for b in profile.barrels:
                        rec = c1['barrels'][b.barrel_id]
                        self.assertEqual(rec['probability']['kind'], E6_KIND[b.barrel_id])
                        self.assertEqual(rec['probability']['vector'], rec['scores'])
                        self.assertEqual(len(rec['top']['labels']), b.selected)
                    self.assertEqual(read_run(res.folder)['forecast'], (True, 'CONSUMABLE'))

    def test_verify_refuses_a_record_that_differs(self):
        profile = POWERBALL
        target = targets(profile)[1]
        ws = self.td / 'ws_bad'
        sha = write_varied_master(ws, profile, target, 0)
        d, e = self.released[('POWERBALL', FULL)]

        def tampered(task, view):
            out = E6.compute(task, view)
            sc = dict(out.barrels['MAIN'].ranking.scores)
            hi, lo = max(sc, key=sc.get), min(sc, key=sc.get)
            sc[hi], sc[lo] = sc[lo], sc[hi]                 # still a valid record, but not E_6's result
            vec = [sc[j] for j in sorted(sc)]
            return MethodOutput(barrels=dict(out.barrels, MAIN=BarrelOutput(ScoredRanking(sc),
                                                                            probability=ProbabilityVector(vec, 'x'))))
        req = C.request(d, e, target, sha, run_id=CP.new_run_id())
        res = CR.run_contract_method(req, compute=tampered, verify=E6.verify, repo_root=ws, run_root=self.td / 'runs')
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertIn('E_6 check', res.reason)
        self.assertFalse((res.folder / 'forecast.json').exists())

    def test_compute_refuses_a_task_it_was_not_written_for(self):
        profile = POWERBALL
        target = targets(profile)[1]
        with tempfile.TemporaryDirectory() as td:
            _d, _req, view, task = e6_view(Path(td), 'POWERBALL', FULL, target)
            from _common.contract_task import MethodTask
            for change in ({'method_id': 'E_1'}, {'variant_id': 'BETA_BERNOULLI_OTHER_V1'},
                           {'observation_view': 'OPERATOR_DRAWN_ORDER'}, {'include_dates': True}):
                with self.subTest(change=change):
                    with self.assertRaises(ValueError):
                        E6.compute(MethodTask(**dict(task.as_dict(), **change)), view)


E6_KIND = {'MAIN': 'MARGINAL_INCLUSION_PROBABILITY', 'POWERBALL': 'PB_CATEGORICAL'}


# ---------------------------------------------------------------- 6.6 as installed: in development, refused

class AsInstalled(unittest.TestCase):
    def test_declarations_and_entries_match_the_specification(self):
        reg = InstalledRegistry()
        keys = {k for k in reg.chain_keys() if k[1] == 'E_6'}
        self.assertEqual(keys, {(g, 'E_6', v) for g in ('POWERBALL', 'OZLOTTO') for v in [*VARIANTS, 'NOT_YET_SPECIFIED']})
        for game in ('POWERBALL', 'OZLOTTO'):
            placeholder = reg.chain(game, 'E_6', 'NOT_YET_SPECIFIED')
            self.assertEqual(len(placeholder), 1)                     # never promoted or edited
            for variant in VARIANTS:
                chain = reg.chain(game, 'E_6', variant)
                self.assertEqual([(e['entry_sequence'], e['registry_status']) for e in chain], [(1, 'FORMULA_OPEN')])
                d = reg.declaration(chain[0]['declaration_digest'])
                fit = 'BETA_BERNOULLI_POSTERIOR_MEAN_V1' if variant == FULL else 'BETA_BERNOULLI_DISCOUNTED_UPDATE_V1'
                self.assertEqual((d['method_revision'], d['observation_views'], d['uses_dates'], d['stochastic_fit'],
                                  d['minimum_history_draws'], d['diagnostic_schema_id'], d['fit_sampling_model_version']),
                                 ('1', ['UNORDERED_SET'], False, False, 1, None, fit))
                self.assertEqual(set(d['channels']), {b.barrel_id for b in get_profile(game).barrels})
                for bid, ch in d['channels'].items():
                    self.assertEqual((ch['ranking_kind'], ch['score_type'], ch['top_rule_id'], ch['worst_rule_id'],
                                      ch['probability_kind'], ch['probability_sum_tolerance']),
                                     ('RANKING_WITH_SCORES', 'FLOAT64', 'TOP_MARGINAL', 'INVERSE', E6_KIND[bid], 1e-12))

    def test_every_e6_request_is_refused_before_any_data_is_read(self):
        reg = InstalledRegistry()
        for game in ('POWERBALL', 'OZLOTTO'):
            for variant in VARIANTS:
                with self.subTest(game=game, variant=variant):
                    e = reg.active_entry(game, 'E_6', variant)
                    d = reg.declaration(e['declaration_digest'])
                    req = C.request(d, e, get_profile(game).first_draw + 10, 'f' * 64)
                    with self.assertRaises(DispatchRefused) as cm:
                        dispatch_gate(req)
                    self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
            self.assertEqual(method_status(game, 'E_6'), 'FORMULA_OPEN')

    def test_supported_but_flagged_is_still_refused(self):
        self.assertTrue((METHODS_ROOT / 'E_006' / 'IN_DEVELOPMENT.txt').is_file())
        with tempfile.TemporaryDirectory() as td:
            data = C.copy_data_root(Path(td))
            reg = InstalledRegistry(data)
            e1 = reg.active_entry('POWERBALL', 'E_6', FULL)
            e2 = dict(e1, entry_sequence=2, registry_status='SUPPORTED', previous_entry_digest=record_digest(e1))
            C.append_entry(data, e2)
            req = C.request(reg.declaration(e1['declaration_digest']), e2, POWERBALL.first_draw + 10, 'f' * 64)
            with C.installed(data=data):                              # the real method folders, flag present
                with self.assertRaises(DispatchRefused) as cm:
                    dispatch_gate(req)
            self.assertEqual(cm.exception.reason, 'IN_DEVELOPMENT_FLAG_PRESENT')

    def test_the_runner_lists_e6(self):
        import Method_Contract_Runner as M
        self.assertIs(M.ADAPTERS['E_6'], E6)            # later methods add their own lines; none is pinned here

    def test_the_method_folder_is_exactly_these_files(self):
        folder = METHODS_ROOT / 'E_006'
        self.assertEqual(sorted(p.name for p in folder.iterdir() if p.name != '__pycache__'),
                         ['IN_DEVELOPMENT.txt', '__init__.py', 'beta_bernoulli.py', 'contract.py'])
        src = (folder / 'beta_bernoulli.py').read_text('utf-8')
        self.assertNotIn('import math', src)                          # exact arithmetic only (spec 2.4)
        self.assertNotIn('float(', src)
        for f in sorted(folder.glob('*.py')):                          # as CODE-2's guard on the E_1 wrapper
            text = f.read_text('utf-8')
            for word in ('game_draws_reader', 'source_data', 'contract_receipts', 'contract_publication',
                         'contract_runner', 'open(', 'read_bytes', 'write_bytes', 'import os', 'subprocess'):
                self.assertNotIn(word, text, f'{f.name} mentions {word}')


if __name__ == '__main__':
    unittest.main()
