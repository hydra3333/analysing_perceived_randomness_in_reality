"""E_3 and E_4 revision 1 (exact polynomial fits): variants, each variant's own fit, no peeking, release state.

OFFLINE, synthetic only. Every master here is invented and written to a temporary folder; no file under the
repository's data folders is opened and no real draw value is read. The installed contract data is only read.
Specification: doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md. Built from the new-method template
(doc/METHOD_TEMPLATE/test_template.py.txt).
"""
from __future__ import annotations

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
from _common import polynomial_fits as PF
from _common.contract_dispatch import DispatchRefused, dispatch_gate, METHODS_ROOT, method_folder
from _common.contract_forecast import assemble_forecast, BarrelOutput, MethodOutput, ScoredRanking
from _common.contract_publication import read_run
from _common.contract_records import record_digest
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from _common.multigame_method_registry import method_status
from E_003 import contract as E3
from E_004 import contract as E4
from E_003.variants import VARIANTS as V3
from E_004.variants import VARIANTS as V4

GAMES = (POWERBALL, OZLOTTO)
METHODS = (('E_3', E3), ('E_4', E4))
SPEC = {   # design note v0.1 section 5, written out here (not read from the modules)
    'POLY_LS_W52_D2_V1': ('LS', 52, 2, None, None),
    'POLY_LS_W52_D3_V1': ('LS', 52, 3, None, None),
    'POLY_LS_W104_D3_V1': ('LS', 104, 3, None, None),
    'POLY_INTERP_W52_D4_H4_V1': ('INTERP', 52, 4, 4, (50, 40, 26, 11, 1)),
    'POLY_MINIMAX_W52_D2_H4_V1': ('MINIMAX', 52, 2, 4, None),
    'POLY_MINIMAX_W52_D3_H4_V1': ('MINIMAX', 52, 3, 4, None),
}
FIT_VERSION = {'LS': 'POLY_LS_RAW_V1', 'INTERP': 'POLY_INTERP_CHEB_NODES_SMOOTHED_V1', 'MINIMAX': 'POLY_MINIMAX_SMOOTHED_V1'}


def view_for(td: Path, game: str, method: str, variant: str, target: int, suffix: int = 0):
    sha = write_varied_master(td, get_profile(game), target, suffix)
    reg = InstalledRegistry()
    d = reg.declaration(reg.active_entry(game, method, variant)['declaration_digest'])
    req, view, task = F.load_view(td, d, target, 'UNORDERED_SET', sha)
    return d, req, view, task


def deep_target(profile):
    """A development target with more than 104 eligible draws in both games."""
    return F.targets(profile)[2]


class Variants(unittest.TestCase):
    def test_tables_are_exactly_the_specification_and_identical(self):
        self.assertEqual(dict(V3), SPEC)
        self.assertEqual(dict(V4), SPEC)

    def test_interpolation_nodes_are_the_chebyshev_formula(self):
        for variant, (fit, m, d, _h, nodes) in SPEC.items():
            if fit == 'INTERP':
                want = tuple(math.floor((m - 1) * (1 + math.cos((2 * k + 1) * math.pi / (2 * d + 2))) / 2 + 0.5)
                             for k in range(d + 1))
                self.assertEqual(nodes, want)
                self.assertEqual(len(set(nodes)), d + 1)


class EachVariantsOwnFit(unittest.TestCase):
    """compute() equals the fit done HERE from the specification's table, for both methods: E_3 scores the
    constant coefficient and E_4 the linear one of the same polynomial; and the variants differ."""

    def own_fit(self, cfg, y):
        fit, m, d, h, nodes = cfg
        ts = PF.abscissae(m)
        if fit == 'LS':
            return PF.least_squares(ts, y, d)
        s = PF.smoothed(y, h)
        if fit == 'INTERP':
            return PF.interpolate([ts[c] for c in nodes], [s[c] for c in nodes])
        return PF.minimax(ts, s, d)[0]

    def test_scores_are_the_specified_coefficients(self):
        for profile in GAMES:
            target = deep_target(profile)
            seen = {}
            for variant, cfg in SPEC.items():
                with tempfile.TemporaryDirectory() as td:
                    _d, _r, view, task3 = view_for(Path(td), profile.game_id, 'E_3', variant, target)
                    _d, _r, _v, task4 = view_for(Path(td), profile.game_id, 'E_4', variant, target)
                    rows = view.simple_rows()[-cfg[1]:]
                    out3, out4 = E3.compute(task3, view), E4.compute(task4, view)
                    for b in profile.barrels:
                        with self.subTest(game=profile.game_id, variant=variant, barrel=b.barrel_id):
                            for j in range(b.low, b.high + 1):
                                y = [1 if j in (r['main'] if b.barrel_id == 'MAIN' else [r['powerball']]) else 0
                                     for r in rows]
                                c = self.own_fit(cfg, y)
                                self.assertEqual(out3.barrels[b.barrel_id].ranking.scores[j], float(c[0]))
                                self.assertEqual(out4.barrels[b.barrel_id].ranking.scores[j], float(c[1]))
                            self.assertIsNone(out3.barrels[b.barrel_id].probability)
                            seen.setdefault(b.barrel_id, {})[variant] = tuple(
                                out3.barrels[b.barrel_id].ranking.scores[j] for j in range(b.low, b.high + 1))
            for bid, by_variant in seen.items():
                self.assertEqual(len(set(by_variant.values())), len(SPEC), f'{profile.game_id} {bid}: variants coincide')


class CrossLabelInvariant(unittest.TestCase):
    """E34-O02: every draw holds exactly K labels of a barrel, so the 0/1 series of all labels add up to the
    constant K; least squares, the clipped smoother and interpolation are linear, so the exact per-label
    polynomials add up to the constant K too: sum p_j(0) = K and sum p'_j(0) = 0, per barrel, before rounding.
    Not imposed on MINIMAX, which is not linear. Checked on both algorithms (compute's and verify's)."""

    def test_least_squares_and_interpolation_polynomials_sum_to_the_constant_k(self):
        for profile in GAMES:
            target = deep_target(profile)
            for name, mod in METHODS:
                for variant, cfg in SPEC.items():
                    if cfg[0] == 'MINIMAX':
                        continue
                    with self.subTest(game=profile.game_id, method=name, variant=variant), \
                            tempfile.TemporaryDirectory() as td:
                        _d, _r, view, task = view_for(Path(td), profile.game_id, name, variant, target)
                        for second in (False, True):
                            fits = mod._fits(task, view, second_algorithm=second)
                            for b in profile.barrels:
                                total = [sum(c[k] for c in fits[b.barrel_id].values()) for k in range(cfg[2] + 1)]
                                self.assertEqual(total, [b.selected] + [0] * cfg[2])


class InsufficientHistory(unittest.TestCase):
    def test_fewer_draws_than_the_window_gives_an_insufficient_history_record(self):
        for name, mod in METHODS:
            for variant in ('POLY_LS_W104_D3_V1', 'POLY_MINIMAX_W52_D2_H4_V1'):
                with self.subTest(method=name, variant=variant), tempfile.TemporaryDirectory() as td:
                    target = POWERBALL.first_draw + 30
                    d, _r, view, task = view_for(Path(td), 'POWERBALL', name, variant, target)
                    out = mod.compute(task, view)
                    self.assertEqual(dict(out.barrels), {})
                    rec = assemble_forecast(d, task, view, out)
                    self.assertEqual(rec['record_status'], 'INSUFFICIENT_HISTORY')
                    mod.verify(task, view, rec, None)


class NoPeeking(unittest.TestCase):
    def test_record_identical_whatever_the_target_and_later_rows_say(self):
        for profile in GAMES:
            target = deep_target(profile)
            for name, mod in METHODS:
                for variant in SPEC:
                    with self.subTest(game=profile.game_id, method=name, variant=variant):
                        digests = set()
                        for suffix in (0, 1, 2):
                            with tempfile.TemporaryDirectory() as td:
                                d, _r, view, task = view_for(Path(td), profile.game_id, name, variant, target, suffix)
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
            for name, _m in METHODS:
                for variant in SPEC:
                    e1 = reg.active_entry(profile.game_id, name, variant)
                    e2 = e1                    # REL-1: the installed entry_0002 is already SUPPORTED
                    self.assertEqual((e2['entry_sequence'], e2['registry_status']), (2, 'SUPPORTED'))
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
            for name, mod in METHODS:
                for variant in SPEC:
                    with self.subTest(game=profile.game_id, method=name, variant=variant):
                        d, e = self.released[(profile.game_id, name, variant)]
                        req = C.request(d, e, target, sha, run_id=CP.new_run_id())
                        res = CR.run_contract_method(req, compute=mod.compute, verify=mod.verify, repo_root=ws,
                                                     run_root=self.td / 'runs')
                        self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: PREDICTION_AVAILABLE'))
                        c1 = json.loads((res.folder / 'forecast.json').read_bytes())
                        for b in profile.barrels:
                            self.assertEqual(c1['barrels'][b.barrel_id]['probability'], {'kind': 'NONE'})
                        self.assertEqual(read_run(res.folder)['forecast'], (True, 'CONSUMABLE'))

    def test_verify_refuses_a_record_that_differs(self):
        target = deep_target(POWERBALL)
        ws = self.td / 'ws_bad'
        sha = write_varied_master(ws, POWERBALL, target, 0)
        for name, mod in METHODS:
            for variant in ('POLY_LS_W52_D2_V1', 'POLY_INTERP_W52_D4_H4_V1', 'POLY_MINIMAX_W52_D3_H4_V1'):
                with self.subTest(method=name, variant=variant):
                    d, e = self.released[('POWERBALL', name, variant)]

                    def tampered(task, view, mod=mod):
                        out = mod.compute(task, view)
                        sc = dict(out.barrels['MAIN'].ranking.scores)
                        hi, lo = max(sc, key=sc.get), min(sc, key=sc.get)
                        sc[hi], sc[lo] = sc[lo], sc[hi]
                        return MethodOutput(barrels=dict(out.barrels, MAIN=BarrelOutput(ScoredRanking(sc))))
                    req = C.request(d, e, target, sha, run_id=CP.new_run_id())
                    res = CR.run_contract_method(req, compute=tampered, verify=mod.verify, repo_root=ws,
                                                 run_root=self.td / 'runs')
                    self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
                    self.assertIn(f'{name} check', res.reason)

    def test_compute_refuses_a_task_it_was_not_written_for(self):
        from _common.contract_task import MethodTask
        with tempfile.TemporaryDirectory() as td:
            _d, _r, view, task = view_for(Path(td), 'POWERBALL', 'E_3', 'POLY_LS_W52_D2_V1', deep_target(POWERBALL))
            for mod, change in ((E3, {'method_id': 'E_4'}), (E4, {}), (E3, {'variant_id': 'POLY_OTHER_V1'}),
                                (E3, {'observation_view': 'OPERATOR_DRAWN_ORDER'}), (E3, {'include_dates': True})):
                with self.subTest(module=mod.METHOD_ID, change=change):
                    with self.assertRaises(ValueError):
                        mod.compute(MethodTask(**dict(task.as_dict(), **change)), view)


class AsInstalled(unittest.TestCase):
    def test_declarations_and_entries_match_the_specification(self):
        reg = InstalledRegistry()
        for name, _m in METHODS:
            for game in ('POWERBALL', 'OZLOTTO'):
                self.assertEqual(len(reg.chain(game, name, 'NOT_YET_SPECIFIED')), 1)   # the placeholder stays
                for variant, cfg in SPEC.items():
                    chain = reg.chain(game, name, variant)
                    self.assertEqual([(e['entry_sequence'], e['registry_status']) for e in chain], [(1, 'FORMULA_OPEN'), (2, 'SUPPORTED')])   # REL-1
                    d = reg.declaration(chain[0]['declaration_digest'])
                    self.assertEqual((d['minimum_history_draws'], d['fit_sampling_model_version'], d['observation_views'],
                                      d['uses_dates'], d['stochastic_fit'], d['diagnostic_schema_id']),
                                     (cfg[1], FIT_VERSION[cfg[0]], ['UNORDERED_SET'], False, False, None))
                    for ch in d['channels'].values():
                        self.assertEqual((ch['ranking_kind'], ch['score_type'], ch['probability_kind']),
                                         ('RANKING_WITH_SCORES', 'FLOAT64', 'NONE'))

    def test_every_request_is_admitted_and_the_roster_says_supported(self):
        reg = InstalledRegistry()
        for name, _m in METHODS:
            for profile in GAMES:
                for variant in SPEC:
                    e = reg.active_entry(profile.game_id, name, variant)
                    req = C.request(reg.declaration(e['declaration_digest']), e, profile.first_draw + 10, 'f' * 64)
                    entry, _decl = dispatch_gate(req)                  # REL-1: admitted; reads no data
                    self.assertEqual(record_digest(entry), record_digest(e))
                self.assertEqual(method_status(profile.game_id, name), 'SUPPORTED')

    def test_flags_absent_and_runner_lists_both(self):
        import Method_Contract_Runner as M
        for name, mod in METHODS:
            self.assertFalse((METHODS_ROOT / method_folder(name) / 'IN_DEVELOPMENT.txt').exists())   # REL-1
            self.assertIs(M.ADAPTERS[name], mod)


class FolderGuards(unittest.TestCase):
    def test_method_folders_are_exactly_these_files_and_read_nothing(self):
        for name, _m in METHODS:
            folder = METHODS_ROOT / method_folder(name)
            self.assertEqual(sorted(p.name for p in folder.iterdir() if p.name != '__pycache__'),
                             ['__init__.py', 'contract.py', 'variants.py'])   # REL-1 removed the flag
            for f in sorted(folder.glob('*.py')):
                text = f.read_text('utf-8')
                for word in ('game_draws_reader', 'source' + '_data', 'contract_receipts', 'contract_publication',
                             'contract_runner', 'open(', 'read_bytes', 'write_bytes', 'import os', 'subprocess',
                             'import math', 'numpy', 'scipy', 'FILL' + ' IN'):
                    self.assertNotIn(word, text, f'{f.name} mentions {word}')


if __name__ == '__main__':
    unittest.main()
