"""Non-launching Package 2 v0.11 timing, AST, and safety proof checks.

No subprocesses, Windows lifecycle operations, gate changes, master updates,
scientific score evaluation or holdout reads. The protected-function AST check uses the
packaged v0.6 fixture under tests/fixtures/coordinator_v0_6_baseline/ (P2-R1-O3); V06_BASELINE
may point at another copy.
"""
from __future__ import annotations
import ast
import hashlib
import os
from pathlib import Path
import queue
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'),str(ROOT/'src'/'methods')]
from _common.multigame_ancestry_release_v1 import RELEASE_POLL_SECONDS,RELEASE_WAIT_SECONDS
from _common.multigame_result_registry_v1 import _COORDINATED_SCIENCE_ALLOWLIST
from coordinator_private.multigame_windows_lifecycle_v1 import PIPE_READER_JOIN_TIMEOUT_SECONDS as LIFE_JOIN
import Powerball_Experiment_Coordinator as coord

PROTECTED=(
    'accept_ancestry_candidate','check_exited_worker_for_orphan',
    'departed_members_check','read_status','record_unresolved_orphan',
    'register_root','require_no_unresolved_orphan','save_new',
    'status_and_result','status_orphan_evidence','terminate_owned_tree',
)


class StaticSafetyTests(unittest.TestCase):
    def test_switches_closed_and_empty_scientific_allowlist(self):
        self.assertIs(coord.ENABLE_PROCESS_TERMINATION,False)
        self.assertIs(coord.ENABLE_SCIENTIFIC_COORDINATION,False)
        self.assertIs(coord.ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE,False)
        self.assertEqual(len(_COORDINATED_SCIENCE_ALLOWLIST),0)

    def test_human_speed_timeout_constants(self):
        self.assertEqual((coord.POLL_SECONDS_DEFAULT,coord.POLL_SECONDS_MIN,
                          coord.POLL_SECONDS_MAX),(1.0,.5,5.0))
        self.assertEqual(coord.PIPE_EOF_WAIT_SECONDS,5.0)
        self.assertEqual(RELEASE_POLL_SECONDS,coord.POLL_SECONDS_MIN)
        self.assertEqual(RELEASE_WAIT_SECONDS,15.0)
        self.assertEqual(coord.LINE_QUEUE_PUT_TIMEOUT_SECONDS,.12)
        self.assertEqual(coord.PIPE_READER_JOIN_TIMEOUT_SECONDS,.05)
        self.assertEqual(LIFE_JOIN,coord.PIPE_READER_JOIN_TIMEOUT_SECONDS)
        self.assertEqual(list(coord.receive_messages(queue.Queue(),poll_seconds=1.0)),[])
        for bad in (.01,.49,5.01):
            with self.assertRaises(ValueError):
                list(coord.receive_messages(queue.Queue(),poll_seconds=bad))
        q=queue.Queue();q.put((1,'invented synthetic log'))
        self.assertEqual(list(coord.receive_messages(q,poll_seconds=1.0)),
                         [(1,'invented synthetic log')])

    def test_protected_v06_ast_mechanically_equal(self):
        # P2-R1-O3: never skips. The committed v0.6 coordinator (commit d09d669) is packaged as a
        # hash-pinned, non-importable fixture; V06_BASELINE may still point at another copy.
        baseline=(Path(os.environ['V06_BASELINE']) if 'V06_BASELINE' in os.environ
                  else ROOT/'tests'/'fixtures'/'coordinator_v0_6_baseline'/
                       'Powerball_Experiment_Coordinator_v0_6.py.txt')
        self.assertTrue(baseline.is_file(), f'v0.6 baseline coordinator missing: {baseline}')
        # Git stores LF; a Windows checkout may hold CRLF, so hash the LF form.
        before=baseline.read_bytes().replace(b'\r\n',b'\n')
        self.assertEqual(hashlib.sha256(before).hexdigest(),
            '2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b')
        after=(ROOT/'src'/'Powerball_Experiment_Coordinator.py').read_bytes()
        def functions(raw):
            return {x.name:ast.dump(x,include_attributes=False)
                    for x in ast.parse(raw).body if isinstance(x,ast.FunctionDef)}
        b,c=functions(before),functions(after)
        for name in PROTECTED:
            with self.subTest(name=name):
                self.assertEqual(b[name],c[name])

    def test_legacy_waits_untouched_and_new_literals_named(self):
        source=(ROOT/'src'/'Powerball_Experiment_Coordinator.py').read_text()
        life=(ROOT/'src'/'coordinator_private'/'multigame_windows_lifecycle_v1.py').read_text()
        self.assertNotIn('messages.put((number, line.rstrip("\\r\\n")), timeout=0.12)',source)
        self.assertNotIn('w.reader.join(timeout=0.05)',source)
        self.assertNotIn('worker.reader.join(timeout=0.05)',life)
        self.assertIn('timeout=LINE_QUEUE_PUT_TIMEOUT_SECONDS',source)
        self.assertIn('timeout=PIPE_READER_JOIN_TIMEOUT_SECONDS',source)
        self.assertIn('timeout=PIPE_READER_JOIN_TIMEOUT_SECONDS',life)
        self.assertIn('timeout=3.0',source)  # protected termination path
        self.assertIn('wait(timeout=3)',source)

    def test_method_loader_import_firewall_except_accepted_legacy_e1(self):
        accepted_legacy='E_001_Historical_Appearance_Frequency.py'
        for method in (ROOT/'src'/'methods').glob('*.py'):
            if method.name==accepted_legacy:
                # Its own previously accepted standalone historical reader is
                # grandfathered; do not modify a frozen E1 golden source file.
                continue
            contents=method.read_text('utf-8')
            tree=ast.parse(contents)
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom):
                    self.assertNotIn('game_draws_reader_v1',node.module or '')
                elif isinstance(node,ast.Import):
                    for alias in node.names:
                        self.assertNotIn('game_draws_reader_v1',alias.name)
            self.assertNotIn('source_data',contents)

    def test_no_retired_acquisition_overlay_importable(self):
        from importlib.util import find_spec
        for module in ('_common.lotterywest_api_client_v1',
                       '_common.multigame_results_build_v1',
                       '_common.multigame_offline_source_pipeline_v1',
                       'multigame_results_tool_v1','multigame_scraper_entry_v0_1'):
            with self.subTest(module=module):
                self.assertIsNone(find_spec(module))

if __name__=='__main__': unittest.main()
