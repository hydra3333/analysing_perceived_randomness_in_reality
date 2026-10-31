"""WF-1A tests: the walk-forward driver (releases and WF-1 design v0.1r1 sections 5 and 10; owner-ratified 31 October 2026).
OFFLINE.

Every batch runs in a temporary project folder holding an invented master, ledger and INIT record (the existing
fixtures' varied rows; never a real result). The test harness patches the runner's PROJECT_ROOT and ORPHAN_MARKER
constants to that folder, as the existing tests patch fixed constants; the installed registry and method folders
are used as installed (after REL-1). A small cohort (E_6 and E_7, six variants; E_1 revision 1 is not real-capable, so it is named in each plan as not in
the cohort) over three targets keeps it fast.
Nothing in the repository is written, and no real draw is read.
"""
from __future__ import annotations

import ast
import contextlib
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import e2r_code2_fixtures as C
from test_e6_beta_bernoulli import write_varied_master
import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.walk_forward as WF
from _common.contract_records import canonical, record_digest
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import POWERBALL, get_profile

ROOT = Path(__file__).resolve().parents[1]
FIRST, LAST = 1574, 1576


def small_adapters():
    import Method_Contract_Runner as M
    return {'E_1': M.ADAPTERS['E_1'], 'E_6': M.ADAPTERS['E_6'], 'E_7': M.ADAPTERS['E_7']}


class Stub:
    """An adapter whose compute misbehaves at one target and otherwise is the real method's."""

    def __init__(self, real, target, exc):
        self.real, self.target, self.exc = real, target, exc

    def compute(self, task, view):
        if task.target_draw_number == self.target:
            raise self.exc
        return self.real.compute(task, view)

    def verify(self, *a):
        return self.real.verify(*a)


class Base(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.proj = Path(self._td.name) / 'project'
        write_varied_master(self.proj, POWERBALL, POWERBALL.holdout_first, 0)
        self.marker = self.proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(mock.patch.object(CR, 'PROJECT_ROOT', self.proj))
        self.stack.enter_context(mock.patch.object(CR, 'ORPHAN_MARKER', self.marker))
        self.adapters = small_adapters()
        self.out = []

    def tearDown(self):
        self.stack.close()
        self._td.cleanup()

    def plan(self, **kw):
        a = dict(game_id='POWERBALL', first=FIRST, last=LAST, adapters=self.adapters)
        a.update(kw)
        return WF.make_plan(**a)

    def run_batch(self, plan, adapters=None):
        return WF.run_batch('POWERBALL', plan['batch_id'], adapters or self.adapters, echo=self.out.append)

    def run_folders(self):
        root = WF.roots()['runs']
        return sorted(p for p in root.glob('*/*/*/*') if p.is_dir()) if root.exists() else []

    def terminals(self):
        return [json.loads((f / 'terminal.json').read_bytes()) for f in self.run_folders() if (f / 'terminal.json').exists()]

    def segments(self, plan):
        folder = WF.roots()['batches'] / 'POWERBALL' / plan['batch_id']
        return [json.loads(p.read_bytes()) for p in sorted(folder.glob('segment_*.json'))]


class PlanRefusals(Base):
    def assert_refused(self, **kw):
        with self.assertRaises(WF.BatchRefused):
            self.plan(**kw)
        self.assertFalse((self.proj / 'results').exists())            # nothing written, no search-log row

    def test_window_cohort_marker_and_ledger(self):
        self.assert_refused(last=POWERBALL.holdout_first)               # the holdout's first draw
        self.assert_refused(first=POWERBALL.first_draw)                 # the era's first draw has no history
        self.assert_refused(first=LAST, last=FIRST)
        self.assert_refused(adapters={})                                # empty cohort
        self.marker.parent.mkdir(parents=True)
        self.marker.write_text('{}')
        self.assert_refused()
        self.marker.unlink()
        ledger = self.proj / 'source_data' / 'POWERBALL_results_master_ledger.csv'
        good = ledger.read_bytes()
        ledger.write_bytes(good + good.splitlines(True)[1])             # a second ledger row
        self.assert_refused()
        ledger.write_bytes(good)
        self.plan()                                                     # and now it plans

    def test_supported_but_flagged_is_refused_by_name(self):
        methods = Path(self._td.name) / 'methods'
        (methods / 'E_006').mkdir(parents=True)
        (methods / 'E_006' / 'IN_DEVELOPMENT.txt').write_text('test harness')
        with C.installed(methods=methods):
            with self.assertRaises(WF.BatchRefused) as cm:
                self.plan()
        self.assertIn('E_6', str(cm.exception))


class TheBatch(Base):
    def test_runs_in_order_and_every_run_is_consumable(self):
        plan = self.plan()
        self.assertEqual([(m['method_id'], m['variant_id']) for m in plan['cohort']],
                         [('E_6', 'BETA_BERNOULLI_DECAY_149_150_V1'), ('E_6', 'BETA_BERNOULLI_DECAY_74_75_V1'),
                          ('E_6', 'BETA_BERNOULLI_FULL_MEMORY_V1'), ('E_7', 'BETA_SHRINK_FULL_C52_V1'),
                          ('E_7', 'BETA_SHRINK_W104_C52_V1'), ('E_7', 'BETA_SHRINK_W52_C52_V1')])
        self.assertEqual([(x['method_id'], x['variant_id']) for x in plan['not_in_cohort']],
                         [('E_1', 'FULL_HISTORY_RAW_COUNTS_V1')])           # named with its reason, not run
        self.assertEqual(self.run_batch(plan), 0)
        seg, = self.segments(plan)
        self.assertEqual([(r['method_id'], r['variant_id'], r['target']) for r in seg['runs']],
                         [(m['method_id'], m['variant_id'], t) for m in plan['cohort'] for t in range(FIRST, LAST + 1)])
        self.assertEqual({r['class'] for r in seg['runs']}, {'CONTINUE'})
        folders = self.run_folders()
        self.assertEqual(len(folders), 18)
        for f in folders:
            self.assertTrue(f.is_relative_to(self.proj / 'results' / 'real' / 'development' / 'contract_runs'))
            self.assertEqual(CP.read_run(f)['forecast'], (True, 'CONSUMABLE'))
            receipt = json.loads((f / 'forecast_receipt.json').read_bytes())
            self.assertEqual((receipt['run_mode'], receipt['evidence_tier'], receipt['master_sha256']),
                             ('REAL_DEVELOPMENT', 'DEVELOPMENT_WF_EXPLORATORY', plan['master_sha256']))
        rows = list(csv.reader((self.proj / 'results' / 'audit' / 'SEARCH_LOG.csv').read_text().splitlines()))
        self.assertEqual(rows[0], list(WF.SEARCH_LOG_HEADER))
        self.assertEqual(len(rows), 2)
        self.assertEqual((rows[1][0], rows[1][11], rows[1][13]), ('WF_BATCH', plan['batch_id'], record_digest(plan)))
        st = WF.status('POWERBALL', plan['batch_id'])
        self.assertEqual(st.pop('ignored_attempt_lines'), 0)
        self.assertEqual({v['done'] for v in st.values()}, {3})
        self.assertEqual({v['attempts'] for v in st.values()}, {3})
        self.assertEqual(self.run_batch(plan), 0)                       # nothing pending: no new run
        self.assertEqual(len(self.run_folders()), 18)
        self.assertEqual(self.segments(plan)[-1]['runs'], [])

    def test_plan_is_frozen_and_checked(self):
        plan = self.plan()
        path = WF.roots()['batches'] / 'POWERBALL' / plan['batch_id'] / 'plan.json'
        with self.assertRaises(FileExistsError):
            CP.create_only(path, b'{}')
        path.chmod(0o644)
        raw = path.read_bytes()
        path.unlink()
        path.write_bytes(raw.replace(b'"window_last":1576', b'"window_last":1575'))
        self.assertEqual(self.run_batch(plan), 2)                       # altered plan: refused before any run
        self.assertEqual(self.run_folders(), [])


class ResumeAndStop(Base):
    def test_ctrl_c_before_a_run_folder_then_resume(self):
        plan = self.plan()
        real, calls = CR.run_contract_method, []

        def interrupting(*a, **k):
            calls.append(1)
            if len(calls) == 5:
                raise KeyboardInterrupt
            return real(*a, **k)
        with mock.patch.object(CR, 'run_contract_method', interrupting):
            self.assertEqual(self.run_batch(plan), 1)
        self.assertEqual(len(self.run_folders()), 4)
        before = {f: {p.name: p.read_bytes() for p in f.iterdir()} for f in self.run_folders()}
        self.assertEqual(self.run_batch(plan), 0)
        self.assertEqual(len(self.run_folders()), 18)
        for f, files in before.items():                                 # earlier attempts untouched
            self.assertEqual({p.name: p.read_bytes() for p in f.iterdir()}, files)

    def test_interrupted_terminal_stops_and_its_pair_runs_again(self):
        plan = self.plan()
        stub = dict(self.adapters, E_6=Stub(self.adapters['E_6'], 1575, KeyboardInterrupt()))
        self.assertEqual(self.run_batch(plan, stub), 1)
        bad = [t for t in self.terminals() if t['outcome_reason'] == 'INTERRUPTED']
        self.assertEqual(len(bad), 1)
        self.assertEqual(len(self.run_folders()), 2)                    # E_6 1574, then the interrupted 1575
        self.assertEqual(self.run_batch(plan), 0)
        self.assertEqual(len(self.run_folders()), 19)                   # the pair ran again; nothing removed

    def test_changed_master_stops_with_zero_later_runs(self):
        plan = self.plan()
        master = self.proj / 'source_data' / 'POWERBALL_results_master.csv'
        master.write_bytes(master.read_bytes() + b'\n')                 # dispatch admits; the reader refuses the pin
        self.assertEqual(self.run_batch(plan), 1)
        t, = self.terminals()                                           # exactly one attempt, then STOP
        self.assertTrue(t['outcome_reason'].startswith('DATA_ADMISSION_REFUSED:'))
        self.assertEqual(self.run_batch(plan), 1)                       # the cause persists: one more attempt only
        self.assertEqual(len(self.terminals()), 2)
        self.assertIn('DATA_ADMISSION_REFUSED', self.out[-1])

    def test_marker_between_targets_stops(self):
        plan = self.plan()
        real = CR.run_contract_method

        def then_marker(*a, **k):
            res = real(*a, **k)                                         # the second call is refused by the marker
            self.marker.parent.mkdir(parents=True, exist_ok=True)
            if not self.marker.exists():
                self.marker.write_text('{}')
            return res
        with mock.patch.object(CR, 'run_contract_method', then_marker):
            self.assertEqual(self.run_batch(plan), 1)
        self.assertEqual(len(self.run_folders()), 1)                    # the marker refused the next run
        self.assertIn('UNRESOLVED_ORPHAN_MARKER', self.out[-1])
        self.assertEqual(self.run_batch(plan), 2)                       # resume: refused at the start
        self.assertEqual(len(self.run_folders()), 1)

    def test_escaping_exception_and_unknown_reason_stop(self):
        plan = self.plan()
        with mock.patch.object(CR, 'run_contract_method', side_effect=OSError('disk')) as m:
            self.assertEqual(self.run_batch(plan), 1)
        self.assertEqual(m.call_count, 1)                               # stopped at the first escape
        self.assertEqual(self.run_folders(), [])
        calls = []

        def unknown(*a, **k):
            calls.append(1)
            return CR.RunResult(Path('x'), 'SUCCESS', 'SOMETHING_NEW: x', {})
        with mock.patch.object(CR, 'run_contract_method', unknown):
            self.assertEqual(self.run_batch(plan), 1)
        self.assertEqual(len(calls), 1)

    def test_switch_off_stops_before_anything(self):
        plan = self.plan()
        with mock.patch.object(CR, 'ENABLE_CONTRACT_REAL_DEVELOPMENT', False):
            self.assertEqual(self.run_batch(plan), 1)
        self.assertEqual(self.run_folders(), [])
        self.assertIn('REAL_DEVELOPMENT_DISABLED', self.out[-1])

    def test_method_failure_continues_and_is_not_retried(self):
        plan = self.plan()
        stub = dict(self.adapters, E_6=Stub(self.adapters['E_6'], 1575, RuntimeError('planted')))
        self.assertEqual(self.run_batch(plan, stub), 0)
        failed = [t for t in self.terminals() if t['outcome'] != 'SUCCESS']
        self.assertEqual(len(failed), 3)                                # each E_6 variant at 1575
        self.assertEqual({t['outcome_reason'].split(':')[0] for t in failed}, {'METHOD_FAILED'})
        self.assertEqual(self.run_batch(plan), 0)                       # a method failure is never retried
        self.assertEqual(len(self.run_folders()), 18)

    def test_start_checks_refuse_a_changed_registry_or_a_new_flag(self):
        plan = self.plan()
        methods = Path(self._td.name) / 'methods'
        (methods / 'E_006').mkdir(parents=True)
        (methods / 'E_006' / 'IN_DEVELOPMENT.txt').write_text('test harness')
        with C.installed(methods=methods):
            self.assertEqual(self.run_batch(plan), 2)
        data = C.copy_data_root(Path(self._td.name))
        reg = InstalledRegistry(data)
        e2 = reg.active_entry('POWERBALL', 'E_6', 'BETA_BERNOULLI_FULL_MEMORY_V1')
        C.append_entry(data, dict(e2, entry_sequence=3, registry_status='FORMULA_OPEN',
                                  previous_entry_digest=record_digest(e2)))
        with C.installed(data=data):
            self.assertEqual(self.run_batch(plan), 2)
        self.assertEqual(self.run_folders(), [])


class AttemptBinding(Base):
    """EX_083 WF1A-R2-B01: a pair is done only through an attempt of THIS batch whose run proves the planned request."""

    def folder_of(self, plan, mem, target):
        attempts, _ = WF._attempts(plan)
        rid = attempts[(mem['method_id'], mem['variant_id'], target)][-1]
        return WF.roots()['runs'] / 'POWERBALL' / mem['method_id'] / mem['variant_id'] / rid

    def rewrite(self, path, rec):
        path.chmod(0o644)
        path.unlink()
        path.write_bytes(canonical(rec))

    def test_forged_terminal_without_an_attempt_is_not_done(self):
        """The reviewer's counterexample: a well-formed SUCCESS terminal with no attempt line and no records."""
        plan = self.plan()
        mem = plan['cohort'][0]
        req = WF.request_for(plan, mem, FIRST, 'mg-forgedforgedforged0001')
        folder = WF.roots()['runs'] / 'POWERBALL' / mem['method_id'] / mem['variant_id'] / req['run_id']
        folder.mkdir(parents=True)
        term = {'schema': 'RUN_TERMINAL_RECORD_V1', 'run_id': req['run_id'], 'game_id': 'POWERBALL',
                'method_id': mem['method_id'], 'variant_id': mem['variant_id'], 'method_revision': mem['method_revision'],
                'target_draw_number': FIRST, 'execution_path': 'STANDALONE', 'outcome': 'SUCCESS',
                'outcome_reason': 'PUBLISHED: PREDICTION_AVAILABLE', 'registry_entry_digest': mem['registry_entry_digest'],
                'receipt_digests': ['c' * 64]}
        (folder / 'terminal.json').write_bytes(canonical(term))
        self.assertIn((mem, FIRST), WF.pending(plan))                   # no attempt line: not done
        WF._append_attempt(plan, req)                                   # even with a matching attempt line ...
        self.assertEqual(WF.attempt_state(plan, mem, FIRST, req['run_id'],
                                          InstalledRegistry().declaration(mem['declaration_digest']))[0], 'NOT_DONE')
        self.assertIn((mem, FIRST), WF.pending(plan))                   # ... no forecast and receipt: not done

    def test_a_new_master_pin_reruns_every_pair(self):
        plan_a = self.plan()
        self.assertEqual(self.run_batch(plan_a), 0)
        write_varied_master(self.proj, POWERBALL, 1500, 1)              # the admitted master changes (a new pin)
        plan_b = self.plan()
        self.assertNotEqual(plan_b['master_sha256'], plan_a['master_sha256'])
        self.assertEqual(len(WF.pending(plan_b)), 18)                   # nothing of batch A counts for B
        self.assertEqual(self.run_batch(plan_b), 0)
        self.assertEqual(len(self.run_folders()), 36)
        for f in self.run_folders():
            r = json.loads((f / 'forecast_receipt.json').read_bytes())
            self.assertIn(r['master_sha256'], (plan_a['master_sha256'], plan_b['master_sha256']))
        self.assertEqual(self.run_batch(plan_a), 0)                     # A stays proven under its own pin
        self.assertEqual(len(self.run_folders()), 36)

    def test_another_batch_with_the_same_pins_is_not_reused(self):
        plan_a = self.plan()
        self.assertEqual(self.run_batch(plan_a), 0)
        plan_b = self.plan()
        self.assertEqual(plan_b['master_sha256'], plan_a['master_sha256'])
        self.assertEqual(len(WF.pending(plan_b)), 18)
        a_lines = WF._attempts_path(plan_a).read_bytes()                # A's attempt lines copied into B's log
        with open(WF._attempts_path(plan_b), 'ab') as fh:
            fh.write(a_lines)
        self.assertEqual(len(WF.pending(plan_b)), 18)                   # another batch's lines are ignored
        self.assertEqual(WF.status('POWERBALL', plan_b['batch_id'])['ignored_attempt_lines'], 18)

    def test_corrupt_or_mismatched_records_make_the_pair_run_again(self):
        plan = self.plan()
        self.assertEqual(self.run_batch(plan), 0)
        m = plan['cohort']
        f0 = self.folder_of(plan, m[0], FIRST)                          # a terminal that is not canonical bytes
        raw = (f0 / 'terminal.json').read_bytes()
        (f0 / 'terminal.json').chmod(0o644)
        (f0 / 'terminal.json').unlink()
        (f0 / 'terminal.json').write_bytes(raw.replace(b'{', b'{ ', 1))
        f1 = self.folder_of(plan, m[1], FIRST)                          # the forecast's content changed
        rec = json.loads((f1 / 'forecast.json').read_bytes())
        self.rewrite(f1 / 'forecast.json', dict(rec, warnings=['tampered']))
        self.assertEqual(WF.attempt_state(plan, m[1], FIRST, f1.name,
                                          InstalledRegistry().declaration(m[1]['declaration_digest']))[1][:24],
                         'forecast not consumable:')
        f2 = self.folder_of(plan, m[2], FIRST)                          # receipt and terminal changed together
        rec = json.loads((f2 / 'forecast_receipt.json').read_bytes())
        new = dict(rec, master_sha256='d' * 64)
        self.rewrite(f2 / 'forecast_receipt.json', new)
        term = json.loads((f2 / 'terminal.json').read_bytes())
        self.rewrite(f2 / 'terminal.json', dict(term, receipt_digests=[record_digest(new)]))
        f3 = self.folder_of(plan, m[3], FIRST)                          # the forecast removed
        (f3 / 'forecast.json').chmod(0o644)
        (f3 / 'forecast.json').unlink()
        decl = InstalledRegistry().declaration
        self.assertEqual(WF.attempt_state(plan, m[2], FIRST, f2.name, decl(m[2]['declaration_digest'])),
                         ('NOT_DONE', 'receipt master_sha256 differs from the planned request'))
        self.assertEqual(sorted((p[0]['variant_id'], p[1]) for p in WF.pending(plan)),
                         sorted((m[i]['variant_id'], FIRST) for i in range(4)))
        self.assertEqual(self.run_batch(plan), 0)                       # they run again; nothing is removed
        self.assertEqual(len(self.run_folders()), 22)

    def test_an_attempt_without_a_folder_and_junk_lines(self):
        plan = self.plan()
        mem = plan['cohort'][0]
        WF._append_attempt(plan, WF.request_for(plan, mem, FIRST, 'mg-neverrannever0000001'))
        wrong = WF.request_for(plan, mem, FIRST + 1, 'mg-wrongdigestwrong00001')    # digest of another pair
        line = canonical({'schema': WF.ATTEMPT_SCHEMA, 'batch_id': plan['batch_id'], 'method_id': mem['method_id'],
                          'variant_id': mem['variant_id'], 'target_draw_number': FIRST,
                          'run_id': wrong['run_id'], 'request_digest': record_digest(wrong)})
        with open(WF._attempts_path(plan), 'ab') as fh:
            fh.write(b'not json\n{"schema":"WF_BATCH_ATTEMPT_V1"}\n' + line)
        self.assertIn((mem, FIRST), WF.pending(plan))
        self.assertEqual(WF.status('POWERBALL', plan['batch_id'])['ignored_attempt_lines'], 3)
        self.assertEqual(self.run_batch(plan), 0)
        self.assertEqual(len(self.run_folders()), 18)


class NotRealCapable(Base):
    def test_a_listed_method_is_named_in_the_plan_and_never_run(self):
        self.assertEqual(set(WF.NOT_REAL_CAPABLE), {'E_1'})             # E_1 r1 until its revision 2 (WF1-13)
        with mock.patch.dict(WF.NOT_REAL_CAPABLE, {'E_6': 'test harness: not real-capable'}):
            plan = self.plan()
        self.assertEqual([m['method_id'] for m in plan['cohort']], ['E_7'] * 3)
        self.assertEqual(sorted((x['method_id'], x['reason']) for x in plan['not_in_cohort']),
                         sorted([('E_1', WF.NOT_REAL_CAPABLE['E_1'])] + [('E_6', 'test harness: not real-capable')] * 3))
        self.assertEqual(self.run_batch(plan), 0)
        self.assertEqual(len(self.run_folders()), 9)

    def test_why_e1_revision_1_is_not_in_the_cohort(self):
        """E_1's frozen revision-1 function refuses real data, so a run of it would only ever fail."""
        from E_001.multigame_e1 import forecast
        rows = [{'draw': POWERBALL.first_draw, 'MAIN': [1, 2, 3, 4, 5, 6, 7], 'POWERBALL': [1]}]
        forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='SYNTHETIC_CONTRACT_TEST')
        with self.assertRaises(ValueError):
            forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='REAL_DEVELOPMENT')


class Classification(unittest.TestCase):
    def test_the_stop_table(self):
        cont = [('SUCCESS', 'PUBLISHED: PREDICTION_AVAILABLE'), ('RUNTIME_FAILURE', 'METHOD_FAILED: X: y'),
                ('NUMERIC_INVALID', 'METHOD_FAILED: nan'), ('VALIDATION_FAILURE', 'CONTRACT_REFUSED_OUTPUT: bad'),
                ('NUMERIC_INVALID', 'CONTRACT_REFUSED_OUTPUT: nan'),
                ('VALIDATION_FAILURE', 'NO_TICKET_NO_DIAGNOSTIC: valid output with no available TOP or WORST')]
        stop = [('VALIDATION_FAILURE', 'DATA_ADMISSION_REFUSED: ValueError: pin'), ('RUNTIME_FAILURE', 'INTERRUPTED'),
                ('RUNTIME_FAILURE', 'PUBLICATION_FAILED: OSError: x'), ('SUCCESS', 'SOMETHING_NEW: x'),
                ('SUCCESS', 'PUBLISHED'), ('RUNTIME_FAILURE', 'PUBLISHED: x'), ('VALIDATION_FAILURE', 'METHOD_FAILED: x'),
                ('SUCCESS', None), (None, 'PUBLISHED: x')]
        for o, r in cont:
            self.assertEqual(WF.classify(o, r), 'CONTINUE', (o, r))
        for o, r in stop:
            self.assertEqual(WF.classify(o, r), 'STOP', (o, r))


class StaticAndInstalled(unittest.TestCase):
    def test_switch_on_real_run_root_and_gitignore(self):
        self.assertIs(CR.ENABLE_CONTRACT_REAL_DEVELOPMENT, True)
        src = (ROOT / 'src' / 'methods' / 'Method_Contract_Runner.py').read_text('utf-8')
        self.assertIn("run_root = CR.PROJECT_ROOT / 'results' / 'real' / 'development' / 'contract_runs'", src)
        self.assertNotIn("'transitory_data' / 'contract_runs'", src)
        self.assertIn('\nresults/real/development/contract_runs/\n', (ROOT / '.gitignore').read_text('utf-8'))
        self.assertEqual(Path(WF.roots()['runs']), CR.PROJECT_ROOT / 'results' / 'real' / 'development' / 'contract_runs')

    def test_driver_reads_no_draws_and_imports_no_evaluation(self):
        for rel in ('src/methods/_common/walk_forward.py', 'src/methods/Method_Walk_Forward.py'):
            text = (ROOT / rel).read_text('utf-8')
            tree = ast.parse(text)
            names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | \
                    {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)} | \
                    {a.name for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names}
            for bad in ('load_pinned_draw_view', 'DrawView', '_parse_prefix', 'evaluation'):
                self.assertNotIn(bad, names, f'{rel} uses {bad}')
            mods = {(n.module or '') for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
            self.assertFalse(any('evaluation' in m for m in mods), rel)
        wf = (ROOT / 'src/methods/_common/walk_forward.py').read_text('utf-8')
        self.assertEqual(wf.count('_trusted_file_bytes('), 1)            # the ledger line only
        self.assertNotIn('source_data', (ROOT / 'src/methods/Method_Walk_Forward.py').read_text('utf-8'))


if __name__ == '__main__':
    unittest.main()
