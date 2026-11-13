"""MHUP-A (design v0.1r5 sections 4.1, 4.2, 6.1, 6.7): the owner's command Method_Mode_H.py, in process, on the
temporary project of the Mode H tests. OFFLINE. Exit codes: 0 done; 1 failed after a record was written; 2 refused
before anything was written or invalid arguments. The launcher (Run_Evaluation.bat) is a Windows file and is not run
here; its static test is test_mhupa_launchers.py.
"""
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import mhupa_slice2_fixtures as X
import _common.owner_records as OR
import _common.walk_forward as WF
from _common.game_profiles import POWERBALL
from evaluation import Method_Mode_H as CLI
from evaluation import mode_h as MH

G = 'POWERBALL'


class Cli(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.tmp = Path(self._td.name)
        self.proj = X.project(self.tmp, POWERBALL)
        self.env = X.fake_environment(self.tmp)
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(X.patched(self.proj, self.env))

    def tearDown(self):
        self.stack.close()
        self._td.cleanup()

    def run_cli(self, *argv) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = CLI.main(list(argv))
            except SystemExit as exc:                      # argparse
                rc = exc.code
        return rc, out.getvalue(), err.getvalue()

    def test_arguments(self):
        rc, out, err = self.run_cli('statements')
        self.assertEqual(rc, 0)
        self.assertIn(f'open: {OR.OPENING_STATEMENT}', out)
        self.assertIn(f'advance: {OR.ADVANCE_STATEMENT}', out)
        self.assertIn(f'declare-developed: {OR.DEVELOPED_STATEMENT}', out)
        self.assertEqual(self.run_cli('manifest')[0], 2)                      # --game required
        self.assertEqual(self.run_cli('manifest', '--game', 'LOTTO')[0], 2)   # not a game
        self.assertEqual(self.run_cli('open', '--game', G)[0], 2)             # --statement required
        self.assertEqual(self.run_cli('bogus')[0], 2)
        self.assertEqual(self.run_cli()[0], 2)

    def test_the_commands_in_order_and_their_refusals(self):
        rc, out, err = self.run_cli('open', '--game', G, '--statement', OR.OPENING_STATEMENT)
        self.assertEqual(rc, 2)
        self.assertIn('[MODE-H] REFUSED: no study manifest', err)
        self.assertIn('Nothing was written by this command', err)
        rc, out, err = self.run_cli('manifest', '--game', G)
        self.assertEqual((rc, err), (0, ''))
        self.assertIn('[MODE-H] MANIFEST written for POWERBALL: 6 variants, targets 1577-1586, frozen master version 1', out)
        self.assertEqual(self.run_cli('manifest', '--game', G)[0], 2)          # create-only
        rc, out, err = self.run_cli('open', '--game', G, '--statement', 'I open the holdout')
        self.assertEqual(rc, 2)
        self.assertIn('typed exactly', err)
        rc, out, err = self.run_cli('open', '--game', G, '--statement', OR.OPENING_STATEMENT)
        self.assertEqual((rc, err), (0, ''))
        self.assertIn('HOLDOUT OPENED for POWERBALL: freeze version 1', out)
        self.assertIn('display rule is unchanged', out)
        self.assertEqual(self.run_cli('open', '--game', G, '--statement', OR.OPENING_STATEMENT)[0], 2)
        rc, out, err = self.run_cli('advance', '--game', G, '--statement', OR.ADVANCE_STATEMENT)
        self.assertEqual(rc, 2)
        self.assertIn('no row beyond the admitted version', err)
        rc, out, err = self.run_cli('score', '--game', G)
        self.assertEqual(rc, 2)
        self.assertIn('version 1; the admitted version is 2', err)             # no first update yet
        rc, out, err = self.run_cli('declare-developed', '--game', G, '--statement', OR.DEVELOPED_STATEMENT)
        self.assertEqual(rc, 2)
        self.assertIn('not sealed', err)
        # after the first update and a complete batch, the score runs and seals; a second one is refused
        X.first_update(self.proj, POWERBALL)
        rc, out, err = self.run_cli('score', '--game', G)
        self.assertEqual(rc, 2)
        self.assertIn('no Mode H plan', err)
        plan = WF.make_mode_h_plan(G, X.small_adapters())
        rc, out, err = self.run_cli('score', '--game', G)
        self.assertEqual(rc, 2)
        self.assertIn('no BATCH_COMPLETE marker', err)
        self.assertEqual(WF.run_batch(G, plan['batch_id'], X.small_adapters(), echo=lambda *_: None), 0)
        # a failure after SCORING_STARTED exits 1 and the records stay; the rerun resumes and exits 0
        with mock.patch.object(MH.RP, 'rebuild_from_ledgers', side_effect=RuntimeError('synthetic crash')):
            rc, out, err = self.run_cli('score', '--game', G)
        self.assertEqual(rc, 1)
        self.assertIn('[MODE-H] FAILED: RuntimeError: synthetic crash. Records written so far stay; a rerun resumes.', err)
        markers = OR.lifecycle_markers_present(self.proj, G, plan['batch_id'])
        self.assertEqual(markers, ['BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE'])
        rc, out, err = self.run_cli('score', '--game', G)
        self.assertEqual((rc, err), (0, ''), err)
        self.assertIn('SEALED: attempt mh-', out)
        self.assertIn('120 score lines, 60 rank lines', out)                   # 60 valid cells, two readouts each
        rc, out, err = self.run_cli('score', '--game', G)
        self.assertEqual(rc, 2)
        self.assertIn('sealed', err)
        rc, out, err = self.run_cli('declare-developed', '--game', G, '--statement', OR.DEVELOPED_STATEMENT)
        self.assertEqual((rc, err), (0, ''))
        self.assertIn('DEVELOPED declared for POWERBALL (GOAL-1)', out)
        self.assertEqual(self.run_cli('declare-developed', '--game', G, '--statement', OR.DEVELOPED_STATEMENT)[0], 2)


if __name__ == '__main__':
    unittest.main()
