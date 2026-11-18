"""MHUP-B slice 3, layer L8: the two sequencers and their launchers (design v0.1r7 section 6.1 and Appendix F; code plan
v0.3 L8 and sections 7, 9 and 12A; EX_237 section 5). OFFLINE: the temporary weekly project; everything invented.

The sequencers start their children through `sequencer_children.run_child`. Here that one function is replaced by a
stand-in that runs the SAME tool's `main()` in this process with the same arguments and hands back its exit code and
its machine-readable last line. So what is tested is the real sequencing against the real tools; what is NOT tested
here is the Windows launch chain itself (a .bat started from a Python parent), which is T017's.

 Weekly     the order of Appendix F after two missed draws; OV-1's `record` after every score and at once on
            FROZE_NEXT; the table only after the session is closed. A failure injected at every child in turn, then
            the same command again: the final records equal an uninterrupted session's (plan section 9).
 Isolation  plan section 7: the table formatter failing, OV-1's recorder blocked, both, every reporting child failing:
            the session is closed, the lock gone, the live records equal those of a clean run, and the exit status
            is the distinct reporting one. OV-1's STATE line is read: a stopped stream (exit 0) is announced.
 Batches    --fill (plan, run, report, admit, publish; a second --fill finds nothing to do), --rerun (never admitted,
            the table unchanged), --report on a batch of the first kind and of the second, and --batch continuing
            after a failure at every child. No weekly record is touched.
 Statics    neither sequencer nor their shared module imports method or evaluator code or names anything that acts
            on a process; the live path's modules import no reporting module; every file in src/ is classified.
"""
from __future__ import annotations

import ast
import contextlib
import io
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

import mhupb_fixtures as B
import test_mhupb_league as L
import test_mhupb_ov1 as O
import _common.score_identities as SI
import _common.walk_forward as WF
import _common.weekly_records as WR
from _common import owner_records as OR
from evaluation import league_publish as LP
from evaluation import league_sources as LS
from evaluation import league_table as LT
from evaluation import ov1 as OV

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import Development_Batch_Orchestrator as DBO            # noqa: E402
import Weekly_Session_Orchestrator as WSO               # noqa: E402
import sequencer_children as SC                         # noqa: E402


def tool_main(exe: str, script: str):
    import Method_Walk_Forward
    import Method_Weekly_Forecast
    from evaluation import Method_League_Table, Method_OV1, Method_Rankings_Report, Method_Weekly_Score
    if exe == 'Run_Method_Rankings.bat':
        return Method_Rankings_Report.main
    return {('Run_Experiment.bat', 'Method_Weekly_Forecast.py'): Method_Weekly_Forecast.main,
            ('Run_Experiment.bat', 'Method_Walk_Forward.py'): Method_Walk_Forward.main,
            ('Run_Evaluation.bat', 'Method_Weekly_Score.py'): Method_Weekly_Score.main,
            ('Run_Evaluation.bat', 'Method_OV1.py'): Method_OV1.main,
            ('Run_Evaluation.bat', 'Method_League_Table.py'): Method_League_Table.main}[(exe, script)]


class Sequenced(L.League, O.Stream):
    """The league and OV-1 fixtures, with every child of a sequencer run in-process by the real tool."""
    EXTRA = 2

    def setUp(self):
        super().setUp()
        self.keep = 1
        self.calls = []                                   # (tool, command, exit code, state)
        self.inject = {}                                  # call number (from 1) -> 'before' | 'after'
        self.stack.enter_context(mock.patch.object(SC, 'check_environment', lambda: None))
        self.stack.enter_context(mock.patch.object(SC, 'ROOT', self.proj))
        self.stack.enter_context(mock.patch.object(SC, 'run_child', self.child))
        real = SI.canonical_coverage                      # the planner's coverage: the early prefix counts as covered,
        self.covered = set()                              # so a routine fill is a dozen pairs, not the whole era
        self.stack.enter_context(mock.patch.object(SI, 'canonical_coverage',
                                                   lambda root, game: real(root, game) | frozenset(self.covered)))

    def fresh(self):
        """A new project for the next case of a sweep."""
        self.tearDown()
        self.setUp()

    def child(self, argv, echo=print):
        exe = Path(argv[0]).name
        n = len(self.calls) + 1
        if exe == 'python.exe':                           # the process check: CLEAN, with the resume token it writes
            self.resume_token(self.lock_session())
            self.calls.append(('process_check', 'check-no-runs', 0, 'CLEAN'))
            return 0, {}
        script, args = (None, argv[1:]) if exe == 'Run_Method_Rankings.bat' else (argv[1], argv[2:])
        name = (script or 'Method_Rankings_Report.py')[len('Method_'):-len('.py')]
        command = args[0] if script else 'report'
        if self.inject.get(n) == 'before':
            self.calls.append((name, command, 1, 'INJECTED_BEFORE'))
            return 1, {}
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                code = tool_main(exe, script)(list(args))
            except SystemExit as exc:                     # argparse
                code = exc.code
            except Exception as exc:                      # a child that dies: a traceback and exit 1
                print(f'Traceback: {type(exc).__name__}: {exc}')
                code = 1
        fields = {}
        for line in buf.getvalue().splitlines():
            fields = SC.parse_result(line) or fields
        self.out.append(buf.getvalue())
        if self.inject.get(n) == 'after':                   # the child did its work; the sequencer is told it failed
            self.calls.append((name, command, 1, 'INJECTED_AFTER'))
            return 1, {}
        self.calls.append((name, command, code, fields.get('state')))
        return code, fields

    def lock_session(self):
        return OR.session_lock_path(self.proj, self.GAME).read_text(encoding='ascii').split()[0]

    def weekly(self):
        self.calls, self.out = [], []
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = WSO.main(['--game', self.GAME])
        return code, buf.getvalue()

    def batch(self, *args):
        self.calls, self.out = [], []
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = DBO.main(['--game', self.GAME, *args])
        return code, buf.getvalue()

    def names(self):
        return [(c[0], c[1]) for c in self.calls]

    def locked(self):
        return OR.session_lock_path(self.proj, self.GAME).exists()

    def weekly_records(self):
        """Every byte under the game's weekly folders (a development batch's own runs live under the development roots)."""
        return {k: v for k, v in self.weekly_bytes().items() if k.startswith('results/real/weekly/')}

    def cover_early_prefix(self, keep_last=2):
        """Everything but the last `keep_last` prefix draws and the former holdout counts as covered for the planner."""
        for m in self.members():
            for t in range(self.p.first_draw + 1, self.p.holdout_last + 1):
                if t < self.p.holdout_first - keep_last or t >= self.p.holdout_first:
                    self.covered.add((m['method_id'], m['method_revision'], m['variant_id'], t))


WEEK = [('Weekly_Forecast', 'status'), ('Weekly_Forecast', 'open-session'),
        ('Weekly_Forecast', 'next'), ('Weekly_Score', 'score'), ('OV1', 'record'),
        ('Weekly_Forecast', 'next'), ('Weekly_Score', 'score'), ('OV1', 'record'),
        ('Weekly_Forecast', 'next'), ('OV1', 'record'),
        ('Weekly_Forecast', 'close-session'), ('League_Table', 'publish'), ('Weekly_Forecast', 'status')]


class Weekly(Sequenced):

    def test_the_order_of_a_session_after_two_missed_draws(self):
        self.register()
        code, text = self.weekly()
        self.assertEqual(code, WSO.EXIT_COMPLETE, text)
        self.assertEqual(self.names(), WEEK)
        self.assertEqual([c[3] for c in self.calls if c[0] == 'OV1'], ['NOTHING_DUE', 'NOTHING_DUE', 'RECORDED'])
        self.assertEqual([c[3] for c in self.calls if c[1] == 'next'], ['FROZE', 'FROZE', 'FROZE_NEXT'])
        self.assertFalse(self.locked())
        self.assertEqual([(l['target_draw_number'], l['set_kind']) for l in self.lines()],
                         [(self.first, 'CATCH_UP_SET'), (self.first + 1, 'CATCH_UP_SET'), (self.first + 2, 'NEXT_DRAW_SET')])
        self.assertEqual(self.kinds(), [('ELIGIBILITY', self.first + 2)])      # OV-1's pre-draw entry, made at once
        self.assertEqual(len(self.table_rows()), 1)
        self.assertIn('complete: forecasts frozen, scores written, OV-1 recorded, league table published', text)
        # a second run before the next result: nothing is made, nothing is published again
        code, text = self.weekly()
        self.assertEqual(code, WSO.EXIT_COMPLETE)
        self.assertEqual([c[3] for c in self.calls if c[1] == 'next'], ['OPEN'])
        self.assertEqual([c[3] for c in self.calls if c[0] == 'OV1'], ['NOTHING_DUE'])      # asked again; nothing due
        self.assertEqual([c[3] for c in self.calls if c[0] == 'League_Table'], ['UP_TO_DATE'])
        self.assertEqual(len(self.lines()), 3)

    def test_a_failure_at_every_child_then_the_same_command_again(self):
        """Plan section 9, the weekly sequencer: between every pair of children. The child either did not run
        ('before') or ran and the sequencer saw a failure ('after'). The rerun continues from the records alone and
        the final state equals an uninterrupted session's: same freeze lines and scores, every pair run once, one
        table, the lock gone."""
        self.register()
        self.assertEqual(self.weekly()[0], 0)
        reference, table = self.science(), self.csv_of(self.table_rows()[0]['attempt_id'])
        ov1 = self.kinds()
        for mode in ('before', 'after'):
            for k in range(1, len(WEEK) + 1):
                self.fresh()
                self.register()
                self.inject = {k: mode}
                code, text = self.weekly()
                tool, command = WEEK[k - 1]
                live = tool in ('Weekly_Forecast', 'Weekly_Score') and k < len(WEEK)
                reporting = {'OV1': WSO.EXIT_OV1, 'League_Table': WSO.EXIT_TABLE}.get(tool, 0)
                self.assertEqual(code, WSO.EXIT_LIVE_STOP if live else reporting, (mode, k, text))
                if live:
                    self.assertIn('run the same command again to resume', text)
                    opened = k > 2 or (k == 2 and mode == 'after')
                    closed = k == len(WEEK) - 2 and mode == 'after'           # close-session itself did its work
                    self.assertEqual(self.locked(), opened and not closed, (mode, k))     # an open session's lock is left
                else:
                    self.assertFalse(self.locked(), (mode, k))                # the live path closed whatever came after
                self.inject = {}
                for _ in range(3):
                    code, text = self.weekly()
                    if code == 0:
                        break
                self.assertEqual(code, 0, (mode, k, text))
                self.assertFalse(self.locked())
                self.assertEqual(self.science(), reference, (mode, k))
                self.assertEqual(set(self.done_counts().values()), {1}, (mode, k))
                self.assertEqual(self.kinds(), ov1, (mode, k))
                rows = self.table_rows()
                self.assertEqual(self.csv_of(rows[-1]['attempt_id'])[0]['all_hits'], table[0]['all_hits'])
                self.check_archive(settled=True)

    def test_a_stop_of_the_live_path_leaves_the_lock_and_starts_no_reporting(self):
        self.register()
        with mock.patch('evaluation.weekly_score.score', side_effect=RuntimeError('disk')):
            code, text = self.weekly()
        self.assertEqual(code, WSO.EXIT_LIVE_STOP)
        self.assertEqual(self.names()[-1], ('Weekly_Score', 'score'))
        self.assertNotIn(('League_Table', 'publish'), self.names())
        self.assertNotIn(('Weekly_Forecast', 'close-session'), self.names())
        self.assertTrue(self.locked())
        self.assertIn('STOPPED at score (draw', text)
        code, text = self.weekly()                               # the lock is found: process check, resume, go on
        self.assertEqual(code, 0, text)
        self.assertEqual(self.names()[:3], [('Weekly_Forecast', 'status'), ('process_check', 'check-no-runs'),
                                            ('Weekly_Forecast', 'open-session')])
        self.assertEqual(self.calls[2][3], 'RESUMED')


class Isolation(Sequenced):
    """Plan section 7: a fault in a reporting layer never changes a live record."""

    def setUp(self):
        super().setUp()
        self.register()

    def reference(self):
        self.assertEqual(self.weekly()[0], 0)
        ref = self.science()
        self.fresh()
        return ref

    def test_the_formatter_failing_gives_the_distinct_status_and_a_later_publish_writes_the_table(self):
        ref = self.reference()
        with mock.patch.object(LT, 'build', side_effect=RuntimeError('formatter')):
            code, text = self.weekly()
        self.assertEqual(code, WSO.EXIT_TABLE)
        self.assertEqual((self.science(), self.locked(), self.table_rows()), (ref, False, []))
        self.assertIn('the league table was not written. The forecasts and scores are safe.', text)
        self.assertIn('Method_League_Table.py publish --game', text)
        self.assertEqual(self.names()[-2:], [('League_Table', 'publish'), ('Weekly_Forecast', 'status')])
        self.assertEqual(LP.publish(self.GAME)['state'], 'PUBLISHED')
        self.check_archive(settled=True)

    def test_a_refusing_adapter_degrades_the_table_and_never_the_session(self):
        ref = self.reference()
        with mock.patch.object(LS, 'collect', side_effect=LS.LeagueRefused('one score per draw and readout: a key twice')):
            code, text = self.weekly()
        self.assertEqual((code, self.science(), self.locked()), (WSO.EXIT_TABLE, ref, False))
        self.assertEqual(self.calls[-2][2:], (2, 'REFUSED'))

    def test_ov1_blocked_or_silent_gives_its_own_status_and_both_give_the_third(self):
        ref = self.reference()
        with mock.patch.object(OV, 'record', side_effect=OV.OV1Blocked('the ledger chain is broken')):
            code, text = self.weekly()
        self.assertEqual((code, self.science(), self.locked()), (WSO.EXIT_OV1, ref, False))
        self.assertEqual(len(self.table_rows()), 1)              # the table is still published
        self.assertIn('OV-1\'s recorder did not finish', text)
        self.assertIn('Method_OV1.py record --game', text)
        self.assertEqual(self.kinds(), [])                       # nothing was written for that draw
        self.fresh()
        with mock.patch.object(OV, 'record', side_effect=OV.OV1Blocked('x')), \
                mock.patch.object(LT, 'build', side_effect=RuntimeError('formatter')):
            code, text = self.weekly()
        self.assertEqual((code, self.science(), self.locked()), (WSO.EXIT_BOTH, ref, False))
        # every reporting child exits non-zero: the session is already closed, the lock gone, the status the reporting one
        self.assertEqual([c[2] for c in self.calls if c[0] in ('OV1', 'League_Table')], [1, 1, 1, 1])
        self.assertEqual(self.names().index(('Weekly_Forecast', 'close-session')) + 1, self.names().index(('League_Table', 'publish')))

    def test_ov1s_state_line_is_read_not_only_its_exit_code(self):
        """EX_237 section 5. A stopped stream exits 0: the sequencer announces it. A child that exits 0 without a
        known state is trouble. A game that is not registered is neither."""
        OV.stop(self.GAME, OV.STOP_STATEMENT)
        code, text = self.weekly()
        self.assertEqual(code, WSO.EXIT_COMPLETE)
        self.assertEqual({c[3] for c in self.calls if c[0] == 'OV1'}, {'STOPPED'})
        self.assertIn('THE FORMAL STREAM OF THIS GAME IS STOPPED AND STAYS STOPPED', text)
        self.assertIn('go on as normal', text)
        self.assertEqual(len(self.lines()), 3)                   # forecasting and scoring went on
        self.fresh()                                             # not registered at all
        OV.registration_path(self.proj, self.GAME).unlink(missing_ok=True)
        if OV.ledger_path(self.proj, self.GAME).exists():
            OV.ledger_path(self.proj, self.GAME).unlink()
        code, text = self.weekly()
        self.assertEqual(code, WSO.EXIT_COMPLETE, text)
        self.assertEqual({c[3] for c in self.calls if c[0] == 'OV1'}, {'NOT_REGISTERED'})
        self.assertNotIn('STOPPED', text)
        self.fresh()
        from evaluation import Method_OV1
        with mock.patch.object(Method_OV1, '_result', lambda *a: None):          # exit 0 and no state line
            code, text = self.weekly()
        self.assertEqual(code, WSO.EXIT_OV1)
        self.assertIn('state none', text)


class Batches(Sequenced):

    def setUp(self):
        super().setUp()
        self.session()                                         # the weekly records a batch must never touch
        self.cover_early_prefix()

    def test_fill_runs_reports_admits_and_publishes_and_a_second_fill_finds_nothing(self):
        weekly = self.weekly_records()
        code, text = self.batch('--fill')
        self.assertEqual(code, 0, text + ''.join(self.out))
        self.assertEqual(self.names(), [('Walk_Forward', 'plan'), ('Walk_Forward', 'run'), ('League_Table', 'batch-state'),
                                        ('Rankings_Report', 'report'), ('League_Table', 'admit'), ('League_Table', 'publish')])
        self.assertEqual([c[3] for c in self.calls][-2:], ['ADMITTED', 'PUBLISHED'])
        self.assertEqual(self.weekly_records(), weekly)          # it opens no weekly record
        entry = SI.league_sources(self.proj, self.GAME)[0]
        self.assertEqual(entry['batch_kind'], 'ROUTINE_FILL')
        plan = WF.load_plan(self.GAME, entry['batch_id'])
        filled = sorted({t for _m, t in WF.plan_pairs(plan)})
        self.assertEqual(filled[:2], [self.p.holdout_first - 2, self.p.holdout_first - 1])
        row = self.csv_of(self.table_rows()[-1]['attempt_id'])[0]
        self.assertEqual(int(row['development_draws']), len(filled))
        self.assertEqual(int(row['all_draws']), len(filled) + self.EXTRA)
        self.assertIn(f'--batch {entry["batch_id"]}', text)    # what to type if anything stops
        sources = SI.league_sources_path(self.proj, self.GAME).read_bytes()
        code, text = self.batch('--fill')                      # every pair now has its canonical score
        self.assertEqual(code, 0, text)
        self.assertEqual([(c[0], c[1], c[3]) for c in self.calls],
                         [('Walk_Forward', 'plan', 'NOTHING_TO_FILL'), ('League_Table', 'publish', 'UP_TO_DATE')])
        self.assertEqual(SI.league_sources_path(self.proj, self.GAME).read_bytes(), sources)
        code, text = self.batch('--batch', entry['batch_id'])  # continuing a finished batch does nothing twice
        self.assertEqual(code, 0, text)
        self.assertEqual([c[3] for c in self.calls][-2:], ['ALREADY_ADMITTED', 'UP_TO_DATE'])
        self.assertNotIn(('Rankings_Report', 'report'), self.names())
        self.assertEqual(len(LS.report_attempts(self.proj, self.GAME, entry['batch_id'])), 1)

    def test_a_failure_at_every_child_of_a_fill_then_continue_with_the_batch(self):
        """Plan section 9, the development sequencer. Every child in turn does its work and is then reported to the
        sequencer as failed (the harder case: the work exists). Continuing with --batch ends with exactly one report,
        one canonical score per key and one row per publication."""
        for k in range(1, 7):
            if k > 1:
                self.fresh()
                self.session()
                self.cover_early_prefix()
            self.inject = {k: 'after'}
            code, text = self.batch('--fill')
            self.assertEqual(code, DBO.EXIT_STOP, (k, text))
            self.assertIn('STOPPED at', text)
            batch = sorted(p.parent.name for p in (WF.roots('DEV_BATCH')['batches'] / self.GAME).glob('wf-*/plan.json'))
            self.assertEqual(len(batch), 1, k)
            self.inject = {}
            code, text = self.batch('--batch', batch[0])
            self.assertEqual(code, 0, (k, text + ''.join(self.out)))
            self.assertEqual(len(LS.report_attempts(self.proj, self.GAME, batch[0])), 1, k)
            self.assertEqual([s['batch_id'] for s in SI.league_sources(self.proj, self.GAME)], batch, k)
            keys = LS.canonical_keys(self.proj, self.GAME)
            self.assertEqual(len(keys), 2 * (len(WF.plan_pairs(WF.load_plan(self.GAME, batch[0]))) + self.EXTRA), k)
            self.assertEqual(len(self.table_rows()), 1, k)
            self.check_archive(settled=True)

    def test_a_rerun_is_reported_and_never_admitted(self):
        self.assertEqual(self.batch('--fill')[0], 0)
        before = (SI.league_sources_path(self.proj, self.GAME).read_bytes(), self.archive(), self.table_rows(),
                  self.weekly_records())
        m = self.members()[0]
        first, last = self.p.holdout_first - 1, self.p.holdout_first    # a prefix draw and a former holdout draw
        code, text = self.batch('--rerun', '--first', str(first), '--last', str(last), '--variants',
                                f'{m["method_id"]}:{m["variant_id"]}')
        self.assertEqual(code, 0, text + ''.join(self.out))
        self.assertEqual(self.names(), [('Walk_Forward', 'plan'), ('Walk_Forward', 'run'), ('League_Table', 'batch-state'),
                                        ('Rankings_Report', 'report')])
        self.assertIn('An exploratory rerun is never admitted', text)
        self.assertEqual((SI.league_sources_path(self.proj, self.GAME).read_bytes(), self.archive(), self.table_rows(),
                          self.weekly_records()), before)
        self.assertEqual(len(list(LS.reports_dir(self.proj, self.GAME).glob(f'ranking_*_{first}-{last}_*.txt'))), 1)

    def test_report_scores_an_existing_batch_of_either_kind_without_running_a_forecast(self):
        """EX_225 R-5: the third form on a batch of the first kind (how the early Powerball draws will be scored) and
        on a batch of the second kind. No forecast is run; a repeat reports, admits and publishes nothing twice."""
        plan = self.v1_batch()
        runs = len(self.run_folders())
        window = ['--first', str(plan['window_first']), '--last', str(plan['window_last'])]
        for _ in range(2):
            code, text = self.batch('--report', '--batch', plan['batch_id'], *window)
            self.assertEqual(code, 0, text + ''.join(self.out))
            self.assertNotIn('Walk_Forward', [c[0] for c in self.calls])
        self.assertEqual([c[3] for c in self.calls], ['BATCH', 'ALREADY_ADMITTED', 'UP_TO_DATE'])
        self.assertEqual(len(self.run_folders()), runs)
        self.assertEqual(len(LS.report_attempts(self.proj, self.GAME, plan['batch_id'])), 1)
        self.assertEqual(SI.league_sources(self.proj, self.GAME)[0]['batch_kind'], 'WF_BATCH_PLAN_V1')
        self.covered -= {k for k in self.covered if k[3] >= self.p.holdout_first}       # the former holdout: to fill
        fill = WF.make_dev_plan(self.GAME, 'ROUTINE_FILL', B.adapters())
        self.assertEqual(self.run_plan(fill)[0], 0)
        code, text = self.batch('--report', '--batch', fill['batch_id'], '--first', str(fill['window_first']),
                                '--last', str(fill['window_last']))
        self.assertEqual(code, 0, text + ''.join(self.out))
        self.assertEqual([s['batch_kind'] for s in SI.league_sources(self.proj, self.GAME)], ['WF_BATCH_PLAN_V1', 'ROUTINE_FILL'])
        self.assertEqual(len(self.table_rows()), 2)

    def test_a_fill_waits_for_a_report_that_is_not_yet_admitted(self):
        """Code plan L4: the existing report attempts are admitted before any routine fill. While a development report
        is not a canonical source, a fill plans nothing (it would run that report's pairs again) and says what to type;
        an exploratory rerun's report never stands in the way."""
        plan = self.v1_batch()
        attempt = self.report(plan)                            # reported, as the two real attempts are; not admitted
        code, text = self.batch('--fill')
        self.assertEqual(code, DBO.EXIT_STOP)
        said = ''.join(self.out)
        self.assertIn(f'--report --batch {plan["batch_id"]} --first {plan["window_first"]} --last {plan["window_last"]}', said)
        self.assertEqual(list((WF.roots('DEV_BATCH')['batches'] / self.GAME).glob('wf-*/plan.json')),
                         [WF.roots('DEV_BATCH')['batches'] / self.GAME / plan['batch_id'] / 'plan.json'])       # nothing planned
        code, text = self.batch('--report', '--batch', plan['batch_id'], '--first', str(plan['window_first']),
                                '--last', str(plan['window_last']))
        self.assertEqual(code, 0, text + ''.join(self.out))
        self.assertEqual([c[3] for c in self.calls], ['BATCH', 'ADMITTED', 'PUBLISHED'])        # the report it had; not again
        self.assertEqual(SI.league_sources(self.proj, self.GAME)[0]['attempt_id'], attempt)
        m = self.members()[0]
        code, text = self.batch('--rerun', '--first', str(self.first), '--last', str(self.first), '--variants',
                                f'{m["method_id"]}:{m["variant_id"]}')
        self.assertEqual(code, 0, text + ''.join(self.out))
        code, text = self.batch('--fill')                      # the rerun's report is in the log and does not block
        self.assertEqual(code, 0, text + ''.join(self.out))
        self.assertEqual(self.calls[0][3], 'NOTHING_TO_FILL')

    def test_arguments(self):
        for bad in ([], ['--fill', '--rerun'], ['--rerun'], ['--fill', '--first', '1', '--last', '2'], ['--report', '--first',
                    '1', '--last', '2'], ['--fill', '--variants', 'A:B'], ['--batch', 'wf-x', '--first', '1', '--last', '2']):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                DBO.main(['--game', self.GAME, *bad])
        self.assertEqual(self.calls, [])


class Children(unittest.TestCase):

    def test_commands_plain_arguments_and_the_result_line(self):
        root = SC.ROOT
        self.assertEqual(SC.command('experiment', 'Method_Weekly_Forecast.py', 'next', '--game', 'OZLOTTO', '--session', 'a' * 32),
                         [str(root / 'Run_Experiment.bat'), 'Method_Weekly_Forecast.py', 'next', '--game', 'OZLOTTO',
                          '--session', 'a' * 32])
        self.assertEqual(SC.command('rankings', '--first', 1286)[0], str(root / 'Run_Method_Rankings.bat'))
        proc = SC.command('process', 'check-no-runs', '--game', 'POWERBALL')
        self.assertEqual(proc[1:4], ['-I', '-B', '-X'])
        self.assertEqual((Path(proc[0]).name, Path(proc[5]).name, proc[-2:]), ('python.exe', 'process_check.py', ['--root', str(root)]))
        self.assertTrue(proc[4].startswith('pycache_prefix=') and proc[4].endswith('no_pycache_ever'))
        for bad in ('a b', 'x;y', 'a&b', '%PATH%', 'a"b', '', 'a|b', '^x', 'a>b'):
            with self.assertRaises(SC.SequencerRefused):
                SC.command('evaluation', 'Method_OV1.py', bad)
        with self.assertRaises(SC.SequencerRefused):
            SC.command('shell', 'x')
        self.assertEqual(SC.parse_result('[WEEKLY-FORECAST] RESULT state=FROZE target=1587 session=' + 'a' * 32 + '\n'),
                         {'state': 'FROZE', 'target': '1587', 'session': 'a' * 32})
        self.assertEqual(SC.parse_result('[OV1] RESULT state=NOTHING_DUE game=POWERBALL next=-')['next'], '-')
        for line in ('[OV1] RESULT', 'RESULT state=X', '[OV1] the RESULT state=X', '[OV1] RESULT state=X extra'):
            self.assertIsNone(SC.parse_result(line), line)

    def test_a_real_child_is_read_to_the_end_and_waited_for(self):
        lines = []
        code, fields = SC.run_child([sys.executable, '-c',
                                     'import sys\nfor i in range(2000): print("line", i)\n'
                                     'print("[TOOL] RESULT state=DONE n=2000"); sys.stderr.write("to stderr\\n"); sys.exit(7)'],
                                    echo=lines.append)
        self.assertEqual((code, fields), (7, {'state': 'DONE', 'n': '2000'}))
        self.assertEqual((len(lines), lines[0], lines[1999]), (2002, 'line 0', 'line 1999'))
        self.assertIn('to stderr', lines)

    def test_only_inside_the_project_venv(self):
        with mock.patch.dict('os.environ', {'VIRTUAL_ENV': '/somewhere/else'}):
            with self.assertRaisesRegex(SC.SequencerRefused, 'wrong Python environment|VIRTUAL_ENV'):
                SC.check_environment()
        with mock.patch.object(SC, 'check_environment', side_effect=SC.SequencerRefused('wrong Python environment')), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(WSO.main(['--game', 'OZLOTTO']), WSO.EXIT_REFUSED)
            self.assertEqual(DBO.main(['--game', 'OZLOTTO', '--fill']), DBO.EXIT_REFUSED)
        self.assertIn('Nothing was started', out.getvalue())


class Statics(unittest.TestCase):
    SRC = ROOT / 'src'
    SEQUENCERS = ('sequencer_children.py', 'Weekly_Session_Orchestrator.py', 'Development_Batch_Orchestrator.py')
    # the reporting layers (L4, L5, L7) and the sequencers (L8)
    REPORTING = {'evaluation/league_sources.py', 'evaluation/league_table.py', 'evaluation/league_publish.py',
                 'evaluation/Method_League_Table.py', 'evaluation/ov1_numeric.py', 'evaluation/ov1.py',
                 'evaluation/Method_OV1.py', 'evaluation/ov1_retrospective.py', 'evaluation/consolidated_report.py',
                 'evaluation/Method_Weekly_Report.py', *SEQUENCERS}
    # the live path (L1 to L3) outside src/methods/: the scoring half and everything it imports
    LIVE = {'evaluation/weekly_score.py', 'evaluation/Method_Weekly_Score.py', 'evaluation/outcome_reader.py',
            'evaluation/collect.py', 'evaluation/divisions.py', 'evaluation/measures.py', 'evaluation/numerics.py',
            'evaluation/report.py', 'evaluation/reforecast_compare.py', 'evaluation/__init__.py'}
    # older tools that belong to neither: Mode H, the WF-1B report tool, N1, the coordinator, the updater, the tools
    OTHER = {'evaluation/Method_Mode_H.py', 'evaluation/mode_h.py', 'evaluation/Method_Rankings_Report.py',
             'evaluation/report_writer.py', 'evaluation/n1.py', 'evaluation/n1_generator.py', 'evaluation/seed_policies.py',
             'Powerball_Experiment_Coordinator.py', 'results_master_v0_2.py',
             'scrape_australian_powerball_history_from_2018_04_19_v0_3.py'}
    OTHER_PATTERNS = (r'two_site_results_check_v0_\d+\.py', r'coordinator_private/\w+\.py', r'package_tools/\w+\.py')

    @staticmethod
    def imported(path: Path) -> set[str]:
        out = set()
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if isinstance(node, ast.Import):
                out |= {a.name for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                base = '.' * node.level + (node.module or '')
                out |= {base} | {f'{base}.{a.name}' if node.module else f'{base}{a.name}' for a in node.names}
        return out

    def test_the_sequencers_import_no_method_or_evaluator_code_and_act_on_no_process(self):
        allowed = {'__future__', 'argparse', 'os', 're', 'subprocess', 'sys', 'pathlib', 'sequencer_children'}
        for name in self.SEQUENCERS:
            path = self.SRC / name
            for imp in self.imported(path):
                self.assertIn(imp.split('.')[0], allowed, (name, imp))
            text = path.read_text(encoding='ascii').lower()
            for banned in ('terminate', 'kill', 'psutil', 'signal', 'pid', 'timer', 'timeout', 'poll', 'os.system',
                           'shell=true', 'communicate', 'threading', 'time.sleep', 'import methods', 'import evaluation',
                           '_common'):
                self.assertNotIn(banned, text, (name, banned))
        self.assertNotIn('subprocess', (self.SRC / 'Weekly_Session_Orchestrator.py').read_text(encoding='ascii'))
        self.assertNotIn('subprocess', (self.SRC / 'Development_Batch_Orchestrator.py').read_text(encoding='ascii'))
        text = (self.SRC / 'sequencer_children.py').read_text(encoding='ascii')
        self.assertEqual(text.count('subprocess.Popen('), 1)                  # the one place a child is started
        self.assertIn('shell=False', text)
        self.assertIn('stdin=subprocess.DEVNULL', text)
        self.assertIn('child.wait()', text)

    def test_every_source_file_is_classified_and_the_live_path_imports_no_reporting_module(self):
        files = {str(p.relative_to(self.SRC)).replace('\\', '/') for p in self.SRC.rglob('*.py')}
        named = self.REPORTING | self.LIVE | self.OTHER
        self.assertEqual(len(named), len(self.REPORTING) + len(self.LIVE) + len(self.OTHER))       # no file in two lists
        for f in sorted(files):
            if f.startswith('methods/'):
                continue                                         # all of src/methods/ is the forecasting side (L1, L2)
            if f not in named and not any(re.fullmatch(p, f) for p in self.OTHER_PATTERNS):
                self.fail(f'{f} is in no layer list: say whether it is live, reporting or neither')
        self.assertEqual(named - files, set())
        reporting = {Path(f).stem for f in self.REPORTING}
        live = [self.SRC / f for f in self.LIVE] + [p for p in (self.SRC / 'methods').rglob('*.py')]
        for path in live:
            for imp in self.imported(path):
                self.assertNotIn(imp.split('.')[-1], reporting, (path.name, imp))

    def test_the_two_launchers(self):
        for name, tool in (('Run_Weekly_Session.bat', 'Weekly_Session_Orchestrator.py'),
                           ('Run_Development_Batch.bat', 'Development_Batch_Orchestrator.py')):
            raw = (ROOT / name).read_bytes()
            raw.decode('ascii')
            self.assertEqual(raw.count(b'\n'), raw.count(b'\r\n'), name)
            text = raw.decode('ascii')
            self.assertIn(f'set "TOOL=%ROOT%src\\{tool}"', text)
            self.assertEqual(text.count('"%PY%" -B -u "%TOOL%" %*'), 1)       # the one thing it runs
            for line in ('set "PYTHONDONTWRITEBYTECODE=1"', 'set "PYTHONPYCACHEPREFIX=%ROOT%transitory_data\\no_pycache_ever"',
                         'if exist "%PYTHONPYCACHEPREFIX%" goto :pycache_present', 'setlocal DisableDelayedExpansion',
                         'endlocal & exit /b %RC%'):
                self.assertIn(line, text, (name, line))
            self.assertTrue((ROOT / 'src' / tool).is_file())


if __name__ == '__main__':
    unittest.main()
