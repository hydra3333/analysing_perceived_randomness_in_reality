"""Pure/offline checks only; NEVER starts Windows Popen or reads lottery data."""
from __future__ import annotations
import json
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock
import sys
import tempfile
import threading
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT/'src'))
sys.path.append(str(ROOT/'src'/'methods'))
from coordinator_private.multigame_windows_lifecycle_v1 import (
    parse_synthetic_args,strict_release_eligibility,run_windows_synthetic)
from coordinator_private.multigame_launch_spec_v1 import build_synthetic_launch_spec
from _common.multigame_ancestry_release_v1 import (
    release_document,await_release,RELEASE_NAME)
from _common.multigame_standalone_contract_v1 import json_bytes


def ident():
    return {'group_id':'syn-review1','worker_sequence':1,
            'run_id':'mg-review12345678', 'game_id':'POWERBALL',
            'draw_number':1576, 'method_id':'E_1',
            'variant_id':'SYNTHETIC_PLUMBING_V1'}


def launch(root):
    return build_synthetic_launch_spec(synthetic_root=root,**ident())


class SyntheticLifecycleReviewTests(TestCase):
    def test_cli_strict(self):
        got=parse_synthetic_args(['--synthetic-contract-test','--game=OZLOTTO','--target=1474'])
        self.assertEqual((got.game,got.target),('OZLOTTO',1474))
        for opts in ([],['--synthetic-contract-test'],
                     ['--synthetic-contract-test','--game=POWERBALL','--target=1576','--live'],
                     ['--synthetic-contract-test','--game=POWERBALL','--target=1576','--timeout-seconds=5']):
            with self.subTest(opts=opts),self.assertRaises(SystemExit):
                parse_synthetic_args(opts)

    def test_both_scientific_and_synthetic_gates_default_false(self):
        coordinator=(ROOT/'src'/'Powerball_Experiment_Coordinator.py').read_text()
        self.assertIn('ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE = False',coordinator)
        self.assertIn('ENABLE_SCIENTIFIC_COORDINATION = False',coordinator)
        self.assertIn('ENABLE_PROCESS_TERMINATION = False',coordinator)
        with self.assertRaisesRegex(ValueError,'NOT AUTHORISED'):
            run_windows_synthetic(SimpleNamespace(ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE=False,
                ENABLE_SCIENTIFIC_COORDINATION=False,ENABLE_PROCESS_TERMINATION=False),[])

    def test_pure_eligibility_requires_live_verified_ancestry(self):
        with tempfile.TemporaryDirectory() as td:
            spec=launch(Path(td)/'multigame_synthetic_runs')
            status={**spec.identity(),'mode':'SYNTHETIC_CONTRACT_TEST',
                    'state':'STARTED','pid':321,'process_create_time_epoch':1700000000.1}
            worker=SimpleNamespace(root_process=object(),root_create_time=1699999999.1,
                   proc=Mock(),experiment_member=SimpleNamespace(pid=321,create_time=1700000000.1),
                   ownership_errors=[],unmatched_status='')
            worker.proc.poll.return_value=None
            strict_release_eligibility(launch=spec,worker=worker,status=status)
            for bad in ({**status,'game_id':'OZLOTTO'},
                        {**status,'state':'SUCCESS'},
                        {**status,'pid':322},None):
                with self.assertRaises(ValueError):
                    strict_release_eligibility(launch=spec,worker=worker,status=bad)
            worker.experiment_member=None
            with self.assertRaises(ValueError):
                strict_release_eligibility(launch=spec,worker=worker,status=status)

    def test_handshake_release_is_exact_and_create_only(self):
        with tempfile.TemporaryDirectory() as td:
            run=Path(td)/'test';run.mkdir()
            marker=Path(td)/'UNRESOLVED_ORPHAN.json'
            who=ident()
            release=release_document(who,pid=321,create_time_epoch=1700000000.1)
            def publisher():
                time.sleep(.05)
                (run/RELEASE_NAME).write_bytes(json_bytes(release))
            thread=threading.Thread(target=publisher)
            thread.start()
            await_release(run_dir=run,identity=who,pid=321,
                          create_time_epoch=1700000000.1,
                          orphan_marker=marker,timeout_seconds=1.5)
            thread.join()
            self.assertTrue(release['not_exit_evidence'])
            with self.assertRaisesRegex(ValueError,'mismatch'):
                await_release(run_dir=run,identity=who,pid=322,
                              create_time_epoch=1700000000.1,
                              orphan_marker=marker,timeout_seconds=.1)
            marker.write_text('test')
            with self.assertRaisesRegex(ValueError,'interlock'):
                await_release(run_dir=run,identity=who,pid=321,
                              create_time_epoch=1700000000.1,
                              orphan_marker=marker,timeout_seconds=.1)

    def test_timeout_is_rejection_not_self_certification(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);run=p/'probe';run.mkdir()
            with self.assertRaises(TimeoutError):
                await_release(run_dir=run,identity=ident(),pid=333,
                              create_time_epoch=1700000000.1,
                              orphan_marker=p/'UNRESOLVED_ORPHAN.json',timeout_seconds=.1)
            self.assertFalse((run/RELEASE_NAME).exists())

    def test_no_child_source_network_kill_or_science_registration(self):
        from _common.multigame_result_registry_v1 import _COORDINATED_SCIENCE_ALLOWLIST
        self.assertEqual(len(_COORDINATED_SCIENCE_ALLOWLIST),0)
        src=(ROOT/'src'/'coordinator_private'/'multigame_windows_lifecycle_v1.py').read_text()
        self.assertNotIn('taskkill',src)
        self.assertNotIn('terminate_owned_tree(',src)
        self.assertNotIn('proc.terminate(',src)
        self.assertNotIn('proc.kill(',src)
        self.assertNotIn('source_data',src)
        self.assertNotIn('urlopen(',src)

if __name__=='__main__':
    unittest.main()
