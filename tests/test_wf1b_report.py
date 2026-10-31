"""WF-1B end to end on invented data: a small walk-forward batch through the installed driver, then one report
(design v0.1r1 section 6.1's order; the WF-1B supplement v0.1r1's layout). OFFLINE; temporary project folder; an
invented master (never a real result) and an invented N1 root (never a beacon value)."""
from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import json
import re
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / 'src'), str(HERE.parent / 'src' / 'methods'), str(HERE)]
from test_e6_beta_bernoulli import write_varied_master                     # noqa: E402
import _common.contract_runner as CR                                       # noqa: E402
import _common.walk_forward as WF                                          # noqa: E402
from _common.contract_receipts import validate_score_record                # noqa: E402
from _common.game_profiles import POWERBALL, OZLOTTO                       # noqa: E402
from evaluation import n1 as N1                                            # noqa: E402
from evaluation import outcome_reader as OR                                # noqa: E402
from evaluation import report as RP                                        # noqa: E402
from evaluation import report_writer as RW                                 # noqa: E402

TEST_POLICY = {'policy_id': 'N1_ROOT_TEST_ONLY_V1', 'output_value': 'AB' * 64}   # invented; test harness only


def small_adapters():
    import Method_Contract_Runner as M
    return {'E_6': M.ADAPTERS['E_6'], 'E_7': M.ADAPTERS['E_7']}


class Batch(unittest.TestCase):
    GAME, PROFILE, FIRST, LAST = 'POWERBALL', POWERBALL, 1566, 1576

    @classmethod
    def setUpClass(cls):
        cls._td = tempfile.TemporaryDirectory()
        cls.proj = Path(cls._td.name) / 'project'
        write_varied_master(cls.proj, cls.PROFILE, cls.PROFILE.holdout_first, 0)
        cls.stack = contextlib.ExitStack()
        cls.stack.enter_context(mock.patch.object(CR, 'PROJECT_ROOT', cls.proj))
        cls.stack.enter_context(mock.patch.object(CR, 'ORPHAN_MARKER',
                                                  cls.proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'))
        cls.stack.enter_context(mock.patch.object(N1, 'R', 200))
        cls.adapters = small_adapters()
        cls.plan = WF.make_plan(cls.GAME, cls.FIRST, cls.LAST, cls.adapters)
        out = []
        assert WF.run_batch(cls.GAME, cls.plan['batch_id'], cls.adapters, echo=out.append) == 0, out

    @classmethod
    def tearDownClass(cls):
        cls.stack.close()
        cls._td.cleanup()

    def drawn_numbers(self):
        """Every drawn main number of the invented master in the window, as text tokens."""
        rows = (self.proj / 'source_data' / f'{self.GAME}_results_master.csv').read_text().splitlines()[1:]
        return {int(r.split(',')[0]): r.split(',')[2:] for r in rows}

    def run(self, result=None):
        return super().run(result)


class Order(Batch):

    def test_row_and_plan_precede_the_first_outcome_read(self):
        seen = {}
        real = OR.read_outcomes

        def spy(**kw):
            if 'rows' not in seen:                     # the state at the FIRST outcome read
                rows = RP.search_rows(self.GAME)
                seen['rows'] = [r['row_type'] for r in rows]
                seen['plans'] = list((self.proj / 'results' / 'real' / 'development' / 'scores').rglob('scoring_plan.json'))
            seen['calls'] = seen.get('calls', 0) + 1
            return real(**kw)
        with mock.patch.object(OR, 'read_outcomes', side_effect=spy):
            res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST)
        self.assertEqual(seen['rows'][-1], 'RANKING_REPORT')
        self.assertTrue(any(res['attempt_id'] in str(p) for p in seen['plans']))
        self.assertEqual(seen['calls'], 1)                 # one outcome read per report

    def test_refusals_append_nothing(self):
        before = len(RP.search_rows())
        for args in ((self.FIRST, 1577), (self.FIRST - 1000, self.LAST), (self.LAST, self.FIRST)):
            with self.assertRaises(RP.ReportRefused):
                RP.run_report(self.GAME, self.plan['batch_id'], *args)
        with self.assertRaises(RP.ReportRefused):
            RP.run_report(self.GAME, 'wf-' + '0' * 32, self.FIRST, self.LAST)
        with self.assertRaises(RP.ReportRefused):                  # window outside the batch's
            RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST - 5, self.LAST)
        self.assertEqual(len(RP.search_rows()), before)

    def test_failure_after_outcomes_keeps_the_row(self):
        before = len(RP.search_rows(self.GAME))
        real = RP.MS.mr7

        def boom(game, targets, *a, **kw):        # fails only on real data, i.e. after the outcomes are read
            if targets:
                raise RuntimeError('injected')
            return real(game, targets, *a, **kw)
        with mock.patch.object(RP.MS, 'mr7', side_effect=boom):
            with self.assertRaises(RuntimeError):
                RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST)
        rows = RP.search_rows(self.GAME)
        self.assertEqual(len(rows), before + 1)
        self.assertEqual(rows[-1]['row_type'], 'RANKING_REPORT')


class Records(Batch):

    def test_ledgers_and_report(self):
        res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST, n1_runner=N1.runner(TEST_POLICY))
        folder = res['scores_folder']
        scores = [json.loads(l) for l in (folder / 'score_ledger.jsonl').read_text().splitlines()]
        self.assertTrue(scores)
        for s in scores:
            validate_score_record(s)
        n_tracks = len(res['per_track'])
        self.assertEqual(n_tracks, 2 * len(self.plan['cohort']))
        contents = RW.build(res, generated_utc='2026-10-31T00:00:00Z', seed_line='policy N1_ROOT_TEST_ONLY_V1, R = 200',
                            n1_policies_on_file=1, environment={'python_version': 'test'})
        text = contents['txt'].decode('ascii')
        # Layout (WB-1): header, Part A (RK-4 block first), glossary, fair-draw reference, Part B, detail, notes.
        pos = [text.index(s) for s in (RW.PART_A, RW.RK4_TITLE, 'GLOSSARY', 'FAIR-DRAW REFERENCE', RW.PART_B,
                                       'PER-TRACK DETAIL', 'NOTES')]
        self.assertEqual(pos, sorted(pos))
        part_a = text[text.index(RW.RK4_TITLE):text.index('GLOSSARY')]
        block_end = part_a.index('+' + '-' * 98, 10)
        rest_of_a = part_a[block_end:]
        for forbidden in ('EXACT_LOCAL', 'Z_plus', 'SELECTION_UNVERIFIED', 'BONFERRONI', 'N1_CALIBRATED', 'P_up'):
            self.assertNotIn(forbidden, rest_of_a)
        self.assertIn('descriptive ranking', rest_of_a)
        # CSV kinds
        kinds = {r['table_kind'] for r in csv.DictReader(io.StringIO(contents['csv'].decode('ascii')))}
        self.assertLessEqual({'DESCRIPTIVE', 'SIGNIFICANCE'}, kinds)
        # No drawn number in any report file (decision WF1-10): no drawn 7-set appears as a run of its numbers.
        drawn = self.drawn_numbers()
        for blob in (contents['txt'], contents['csv'], contents['json']):
            s = blob.decode('ascii')
            for t in range(self.FIRST, self.LAST + 1):
                seq = ','.join(drawn[t][:7])
                self.assertNotIn(seq, s)
        # N1 ran on the invented root: MR1 has N1 p-values.
        mr1 = next(iter(res['results'].values()))['MR1']['sub_measures']['MR1']
        self.assertIsNotNone(res['n1'])
        paths = RW.write(res, contents, '20261031T000000Z')
        self.assertEqual(len(paths), 3)
        with self.assertRaises(FileExistsError):
            RW.write(res, contents, '20261031T000000Z')


class Families(Batch):
    """Design 6.2A (EX_078 C03): the roster and M are fixed; the guarantee needs every track complete and exact."""

    def family(self, res):
        roster = sorted(tr['track_id'] for tr in res['per_track'].values())
        return {'family_id': 'TEST_FAMILY_MR7_MAIN', 'game_id': self.GAME, 'measure': 'MR7.MAIN', 'M': len(roster),
                'roster': roster, 'roster_digest': hashlib.sha256('\n'.join(roster).encode()).hexdigest(),
                'window_first': self.FIRST, 'window_last': self.LAST}

    def test_complete_incomplete_and_empty(self):
        res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST)
        res['families'] = [self.family(res)]
        f = RW.families_global(res)[0]
        self.assertTrue(f['guaranteed'])
        self.assertIsNone(f['label'])
        self.assertEqual(f['P_bonf'], min(1, f['M'] * f['min_P_up']))
        key = sorted(res['per_track'])[0]
        res['per_track'][key]['status'] = 'GRID_INCOMPLETE'                  # one failed cell somewhere
        f = RW.families_global(res)[0]
        self.assertFalse(f['guaranteed'])
        self.assertEqual(f['label'], 'BONFERRONI_REFERENCE_UNCALIBRATED')
        self.assertEqual(f['M'], len(res['per_track']))                      # M is never reduced
        self.assertIn((res['per_track'][key]['track_id'], 'GRID_INCOMPLETE'), f['broken'])
        res['per_track'][key]['status'] = 'GRID_EMPTY'
        res['results'][key]['MR7']['sub_measures']['MR7.MAIN']['significance'] = None
        f = RW.families_global(res)[0]
        self.assertEqual((f['M'], f['tracks_with_p']), (len(res['per_track']), len(res['per_track']) - 1))
        self.assertEqual(f['P_bonf'], min(1, len(res['per_track']) * f['min_P_up']))   # M, never the tracks with a p
        self.assertEqual(f['label'], 'BONFERRONI_REFERENCE_UNCALIBRATED')
        fam = self.family(res)
        fam['roster'] = fam['roster'][1:] + ['POWERBALL:E_99:NOT_A_VARIANT_V1:TOP:WF']   # a roster that differs
        res['per_track'][key]['status'] = 'GRID_COMPLETE'
        res['families'] = [fam]
        self.assertFalse(RW.families_global(res)[0]['guaranteed'])


class Duplicates(Batch):
    """Design 6.1 step 3: equal duplicate runs pass (the earliest is used); unequal ones are REPRODUCIBILITY_FAIL."""
    FIRST, LAST = 1574, 1576

    def test_equal_and_unequal_duplicates(self):
        import _common.contract_publication as CP
        from evaluation import collect as COL
        mem, t = self.plan['cohort'][0], 1575
        req = WF.request_for(self.plan, mem, t, CP.new_run_id())
        WF._append_attempt(self.plan, req)
        ad = self.adapters[mem['method_id']]
        res = CR.run_contract_method(req, compute=ad.compute, verify=ad.verify, repo_root=self.proj,
                                     run_root=WF.roots()['runs'])
        self.assertEqual(res.outcome, 'SUCCESS')
        cell = COL.collect(self.plan, self.FIRST, self.LAST)['cells'][(mem['method_id'], mem['variant_id'], t)]
        self.assertTrue(cell['valid'])
        self.assertEqual(cell['consumable_runs'], 2)
        self.assertNotEqual(cell['run_id'], req['run_id'])                 # the earlier freeze is selected
        real = COL._load

        def altered(path):
            rec = real(path)
            if rec is not None and req['run_id'] in str(path) and 'canonical_content_digest' in rec:
                rec = dict(rec, canonical_content_digest='f' * 64)
            return rec
        with mock.patch.object(COL, '_load', side_effect=altered):
            got = COL.collect(self.plan, self.FIRST, self.LAST)
        cell = got['cells'][(mem['method_id'], mem['variant_id'], t)]
        self.assertEqual((cell['valid'], cell['reason']), (False, 'REPRODUCIBILITY_FAIL'))
        valid, invalid = COL.track_cells(got, mem['method_id'], mem['variant_id'], 'TOP')
        self.assertEqual(invalid['REPRODUCIBILITY_FAIL'], 1)
        self.assertEqual(COL.track_status(valid, invalid), 'GRID_INCOMPLETE')


class Registry(Batch):
    """MRT-13 (registry texts and the mode texts in the glossary), MRT-18 (one row per report run), MRT-06 (N1 refuses
    in-sample input) and MRT-16 (a) / MRT-19 (N1 replays MR7's exact distribution within Monte Carlo error)."""
    FIRST, LAST = 1568, 1576

    def test_glossary_rows_and_n1(self):
        before = len(RP.search_rows(self.GAME))
        res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST)
        self.assertEqual(len(RP.search_rows(self.GAME)), before + 1)
        c = RW.build(res, generated_utc='x', seed_line='N1_NOT_RUN: seed policy not approved', n1_policies_on_file=0,
                     environment={})
        text = c['txt'].decode('ascii')
        glossary = text[text.index('GLOSSARY'):text.index('FAIR-DRAW REFERENCE')]
        mreg = json.loads((RP.REGISTRY_DIR / 'MEASURE_REGISTRY_V1.json').read_text())
        for code in ('WF', 'IS'):
            self.assertIn(mreg['modes'][code]['plain_meaning'].replace('**', ''), glossary)
        for m in mreg['measures']:
            self.assertIn(m['one_liner'], glossary)
        for line in text.splitlines():
            self.assertNotRegex(line, r'^(WF|IS)\s*$')
        for sid in set(re.findall(r'^(MR[0-9.A-Z-]+) - ', text, re.M)):
            self.assertTrue(any(sid.split('.')[0] == m['id'] or sid.startswith(m['id']) for m in mreg['measures']), sid)
        # N1 refuses an in-sample track.
        bad = dict(res['per_track'])
        k = next(iter(bad))
        bad[k] = dict(bad[k], track_id=bad[k]['track_id'][:-3] + ':IS')
        with self.assertRaises(ValueError):
            N1.runner(TEST_POLICY)(self.GAME, bad, res['per_variant'], [])

    def test_n1_replays_mr7_exactly_within_monte_carlo_error(self):
        res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST)
        key = sorted(res['per_track'])[0]
        tr = res['per_track'][key]
        with mock.patch.object(N1, 'R', 4000):
            sim = N1.simulate(TEST_POLICY, self.GAME, sorted(tr['entries']))
        mm, _div = N1._replay(sim, self.GAME, tr['entries'])
        s_rep = mm.sum(axis=1)
        n = len(tr['entries'])
        tails = N1._tail_table(self.GAME, n)
        for s in range(0, 20, 3):
            emp = float((s_rep >= s).mean())
            exact = float(tails[s])
            se = max((exact * (1 - exact) / 4000) ** 0.5, 1 / 4000)
            self.assertLess(abs(emp - exact), 5 * se, (s, emp, exact))


class N1Display(Batch):
    """EX_109 C01 and C02: every N1 figure is printed with k, R, (k+1)/(R+1) and its Monte Carlo interval, in the text,
    the CSV and the JSON, the RK-4 block agreeing with Part B; range labels are kept beside calibration labels."""
    FIRST, LAST = 1568, 1576

    def family(self, res):
        roster = sorted(tr['track_id'] for tr in res['per_track'].values())
        return {'family_id': 'TEST_FAMILY_MR7_MAIN', 'game_id': self.GAME, 'measure': 'MR7.MAIN', 'M': len(roster),
                'roster': roster, 'roster_digest': hashlib.sha256('\n'.join(roster).encode()).hexdigest(),
                'window_first': self.FIRST, 'window_last': self.LAST}

    def build(self, res):
        c = RW.build(res, generated_utc='x', seed_line='policy N1_ROOT_TEST_ONLY_V1, R = 200', n1_policies_on_file=1,
                     environment={})
        return c['txt'].decode('ascii'), list(csv.DictReader(io.StringIO(c['csv'].decode('ascii')))), json.loads(c['json'])

    def test_monte_carlo_facts_everywhere(self):
        with mock.patch.object(RP, 'load_families', side_effect=lambda g, f, l: []):
            res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST)
        fam = self.family(res)
        res = None
        with mock.patch.object(RP, 'load_families', side_effect=lambda g, f, l: [fam]):
            res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST, n1_runner=N1.runner(TEST_POLICY))
        text, rows, man = self.build(res)
        # MR1 (N1_CALIBRATED) and MR5 (reference) rows carry k, R and the interval, in text and CSV.
        mr1 = [r for r in rows if r['sub_measure'] == 'MR1' and r['table_kind'] == 'SIGNIFICANCE']
        self.assertTrue(mr1)
        for r in mr1:
            self.assertEqual(r['n1_mc_R'], '200')
            k = int(r['n1_mc_k'])
            self.assertEqual(float(r['n1_mc_p']), (k + 1) / 201)
            self.assertLessEqual(float(r['n1_mc_ci95_low_k_over_R']), k / 200)
            self.assertGreaterEqual(float(r['n1_mc_ci95_high_k_over_R']), k / 200)
            self.assertIn('N1_CALIBRATED', r['label'])
        self.assertTrue([r for r in rows if r['sub_measure'] == 'MR5.MAIN:n1_reference' and r['n1_mc_R'] == '200'])
        self.assertIn('Monte Carlo 95% interval on k/R (Clopper-Pearson)', text)
        # In Part B's MR1 table, every row is followed by its own Monte Carlo line.
        part_b = text[text.index(RW.PART_B):]
        table = part_b[part_b.index('MR1 - significance ranking'):]
        table = table[:table.index('\n\n')].splitlines()[2:]
        rows_b = [i for i, l in enumerate(table) if ':WF ' in l]
        self.assertEqual(len(rows_b), len(mr1))
        for i in rows_b:
            self.assertTrue(table[i + 1].strip().startswith('N1 Monte Carlo: k = '), table[i:i + 2])
        self.assertTrue(any(f['block'] == 'significance' and f['R'] == 200 for f in man['n1_figures']))
        # The family's maximum statistic: the same Monte Carlo text in the RK-4 block and in Part B.
        f = RW.families_global(res)[0]
        line = RW.mc_text(f['n1_max'])
        self.assertIsNotNone(line)
        block = text[text.index(RW.RK4_TITLE):text.index('GLOSSARY')]
        part_b = text[text.index(RW.PART_B):text.index('PER-TRACK DETAIL')]
        self.assertIn(line, block)
        self.assertIn(line, part_b)
        fam_row = next(r for r in rows if r['table_kind'] == 'RK4_DISCLOSURE')
        self.assertEqual(fam_row['n1_mc_R'], '200')
        # An incomplete grid: the family's N1 figure is flagged, and its Monte Carlo facts are still shown.
        key = sorted(res['per_track'])[0]
        res['per_track'][key]['status'] = 'GRID_INCOMPLETE'
        text2, _rows2, _m2 = self.build(res)
        self.assertIn('N1_FIXED_FORECAST_REFERENCE, flag SELECTION_UNVERIFIED; ' + line, text2)

    def test_range_labels_are_kept(self):
        from evaluation import numerics as NU
        tiny = Fraction(1, 10 ** 400)
        z, p, lab = RW._sig_text({'Z_plus': NU.z_plus(tiny), 'P_up_output': NU.p_output(tiny), 'label': 'EXACT_LOCAL'})
        self.assertEqual((p, lab), ('10^-400', 'EXACT_LOCAL+P_BELOW_FLOAT64_RANGE'))
        z, p, lab = RW._sig_text({'Z_plus': NU.z_plus(Fraction(1, 10 ** 220000)),
                                  'P_up_output': NU.p_output(Fraction(1, 10 ** 220000)), 'label': 'EXACT_LOCAL'})
        self.assertEqual((z, lab), ('>= 1000', 'EXACT_LOCAL+P_BELOW_FLOAT64_RANGE+SIGMA_ABOVE_BOUND'))
        # Through a whole report: one track's MR7 tail replaced by an extreme exact tail.
        res = RP.run_report(self.GAME, self.plan['batch_id'], self.FIRST, self.LAST)
        key = sorted(res['results'])[0]
        sub = res['results'][key]['MR7']['sub_measures']['MR7.MAIN']
        sub['significance'] = dict(sub['significance'], P_up=tiny, P_up_output=NU.p_output(tiny), Z_plus=NU.z_plus(tiny))
        sub['significance_key'] = NU.z_plus(tiny)['sigma']
        text, rows, _m = self.build(res)
        row = next(r for r in rows if r['sub_measure'] == 'MR7.MAIN' and r['unit_id'] == res['per_track'][key]['track_id']
                   and r['table_kind'] == 'SIGNIFICANCE')
        self.assertEqual((row['p_value'], row['label']), ('10^-400', 'EXACT_LOCAL+P_BELOW_FLOAT64_RANGE'))
        self.assertIn('10^-400  EXACT_LOCAL+P_BELOW_FLOAT64_RANGE', text)


if __name__ == '__main__':
    unittest.main()
