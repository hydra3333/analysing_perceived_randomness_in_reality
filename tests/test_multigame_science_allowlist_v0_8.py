"""Adversarial synthetic/scientific separation tests; NO real data or processes.

Production scientific coordinated allowlist remains empty. One older test
fixture explicitly patches a fake registration ONLY for the duration of a
unit test. That fixture is not runnable by the coordinator/worker.
"""
from __future__ import annotations
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src'/'methods')]
import _common.multigame_result_registry_v1 as registry
from _common.multigame_standalone_contract_v1 import json_bytes
from coordinator_private.multigame_launch_spec_v1 import build_synthetic_launch_spec
from coordinator_private.multigame_coordinator_exit_receipt_v2 import (
    issue_coordinator_receipt, verify_receipt_before_consume
)
from test_multigame_exit_receipt_v0_8 import (setup, records, CODE_HASH)

WORKER=ROOT/'src'/'methods'/'POC_MultiGame_Synthetic_Worker.py'
worker_spec=importlib.util.spec_from_file_location('synthetic_probe_v08',WORKER)
worker=importlib.util.module_from_spec(worker_spec)
worker_spec.loader.exec_module(worker)


def completed_synthetic(root: Path):
    run_id='mg-synthvariant008'
    group_id='group-synthv08'
    args=['--synthetic-contract-probe','--game=POWERBALL',
          '--target=1576','--run-id='+run_id,'--group-id='+group_id,
          '--worker-sequence=1','--variant=SYNTHETIC_PLUMBING_V1']
    with contextlib.redirect_stdout(io.StringIO()) as stream:
        rc=worker.main(args,test_synthetic_root=root/'multigame_synthetic_runs')
    if rc!=0:
        raise AssertionError('synthetic worker fixture failed')
    run=root/'multigame_synthetic_runs'/'POWERBALL'/run_id
    group=root/group_id
    (group/'receipts').mkdir(parents=True)
    identity={'group_id':group_id,'worker_sequence':1,'run_id':run_id,
              'game_id':'POWERBALL','draw_number':1576,
              'method_id':'E_1','variant_id':'SYNTHETIC_PLUMBING_V1'}
    (group/'manifest.json').write_bytes(json_bytes({
        'group_id':group_id,'status':'PASS','success':True,
        'orphan_suspected':False,'marker_write_failed':False,
        'workers':[{'run_id':run_id,'sequence':1,'state':'SUCCESS'}]}))
    receipt=issue_coordinator_receipt(group_dir=group,run_dir=run,identity=identity,
        coordinator_sha256=CODE_HASH,root_pid=2201,
        root_create_time_epoch=1711111000.125,wrapper_exit_code=0,
        exit_observed_utc='2026-10-24T02:25:31+00:00',
        console_publication_records=stream.getvalue().splitlines())
    return group,run,identity,receipt


class SyntheticSeparationTests(unittest.TestCase):
    def test_no_scientific_coordination_contract_activated(self):
        self.assertEqual(dict(registry._COORDINATED_SCIENCE_ALLOWLIST),{})
        for game in ('POWERBALL','OZLOTTO'):
            with self.subTest(game=game):
                registry.require_synthetic_variant(game,'E_1','SYNTHETIC_PLUMBING_V1')
                with self.assertRaisesRegex(ValueError,'synthetic-only'):
                    registry.require_synthetic_variant(game,'E_1','FULL_HISTORY_RAW_COUNTS_V1')
                with self.assertRaisesRegex(ValueError,'registered'):
                    registry.registered_scientific_binding(game_id=game,method_id='E_1',
                       variant_id='FULL_HISTORY_RAW_COUNTS_V1',mode='COORDINATED')

    def test_launcher_rejects_science_variant_as_plumbing(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            with self.assertRaisesRegex(ValueError,'synthetic-only'):
                build_synthetic_launch_spec(group_id='group-test', worker_sequence=1,
                    run_id='mg-synthvariant008',game_id='POWERBALL',draw_number=1576,
                    method_id='E_1',variant_id='FULL_HISTORY_RAW_COUNTS_V1',synthetic_root=root)
            self.assertFalse(root.exists())

    def test_synthetic_has_four_modes_and_no_forecast_consumer(self):
        with tempfile.TemporaryDirectory() as td:
            group,run,identity,receipt=completed_synthetic(Path(td))
            self.assertEqual(json.loads((run/'status.json').read_bytes())['mode'],registry.SYNTHETIC_MODE)
            self.assertEqual(json.loads((run/'manifest.json').read_bytes())['mode'],registry.SYNTHETIC_MODE)
            self.assertEqual(json.loads((run/'canonical_result.json').read_bytes())['mode'],registry.SYNTHETIC_MODE)
            self.assertEqual(json.loads(receipt.read_bytes())['mode'],registry.SYNTHETIC_MODE)
            with self.assertRaisesRegex(ValueError,'synthetic contract'):
                verify_receipt_before_consume(group_dir=group,run_dir=run,
                    identity=identity,coordinator_sha256=CODE_HASH,
                    global_orphan_marker=Path(td)/'UNRESOLVED_ORPHAN.json')

    def test_synthetic_consumer_refuses_before_result_read(self):
        with tempfile.TemporaryDirectory() as td:
            group,run,identity,_=completed_synthetic(Path(td))
            orig=Path.read_bytes
            opened=[]
            def tracked(path):
                if path == run/'canonical_result.json':opened.append(str(path))
                return orig(path)
            with patch.object(Path,'read_bytes',tracked):
                with self.assertRaisesRegex(ValueError,'synthetic contract'):
                    verify_receipt_before_consume(group_dir=group,run_dir=run,
                        identity=identity,coordinator_sha256=CODE_HASH,
                        global_orphan_marker=Path(td)/'UNRESOLVED_ORPHAN.json')
            self.assertEqual(opened,[])

    def test_forged_receipt_mode_does_not_convert_synthetic_to_science(self):
        with tempfile.TemporaryDirectory() as td:
            group,run,identity,receipt=completed_synthetic(Path(td))
            data=json.loads(receipt.read_bytes());data['mode']='COORDINATED'
            receipt.write_bytes(json_bytes(data))
            with self.assertRaisesRegex(ValueError,'registered|scientific'):
                verify_receipt_before_consume(group_dir=group,run_dir=run,
                    identity=identity,coordinator_sha256=CODE_HASH,
                    global_orphan_marker=Path(td)/'UNRESOLVED_ORPHAN.json')

    def test_missing_deny_flags_are_not_scientific_approval(self):
        # Simulate a well-formed COORDINATED worker with no 'not_a_forecast'
        # and no synthetic_only=True marker.  It is STILL not registered.
        with tempfile.TemporaryDirectory() as td:
            group,run,ident,_=setup(Path(td))
            value=json.loads((run/'canonical_result.json').read_bytes())
            self.assertNotIn('not_a_forecast',value)
            self.assertNotIn('synthetic_only',value)
            with self.assertRaisesRegex(ValueError,'no reviewed coordinated'):
                issue_coordinator_receipt(group_dir=group,run_dir=run,identity=ident,
                    coordinator_sha256=CODE_HASH,root_pid=2201,
                    root_create_time_epoch=1711111000.125,wrapper_exit_code=0,
                    exit_observed_utc='2026-10-24T02:25:31+00:00',
                    console_publication_records=records(group,run,ident))
            self.assertEqual(list((group/'receipts').iterdir()),[])

if __name__=='__main__':unittest.main()
