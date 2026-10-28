"""Offline contract tests: no Windows coordinator, live data or scientific run."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'src'/'methods')]
from coordinator_private.multigame_launch_spec import build_synthetic_launch_spec
from _common.multigame_console_protocol import verify_success_records
from _common.multigame_standalone_contract import json_bytes
from _common.multigame_coordinated_manifest import publish_coordinated_success

METHOD=ROOT/'src'/'methods'/'POC_MultiGame_Synthetic_Worker.py'
spec=importlib.util.spec_from_file_location('e001_multigame_synthetic_review',METHOD)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ID='mg-synthetic12345678'
VARIANT='SYNTHETIC_PLUMBING_V1'
CODE='coord-review1'


def args(**updates):
    opts=dict(group_id=CODE,worker_sequence=1,run_id=ID,game_id='POWERBALL',
              draw_number=1576,method_id='E_1',variant_id=VARIANT)
    opts.update(updates)
    return opts


def execute(root,**update):
    opts=args(**update)
    cmd=['--synthetic-contract-probe','--game='+opts['game_id'],
         '--target='+str(opts['draw_number']),'--run-id='+opts['run_id'],
         '--group-id='+opts['group_id'],
         '--worker-sequence='+str(opts['worker_sequence']),
         '--variant='+opts['variant_id']]
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream):
        rc=module.main(cmd,test_synthetic_root=root)
    return rc,stream.getvalue().splitlines(),opts


class LaunchAndWorkerManifestTests(unittest.TestCase):
    def test_plan_is_immutable_and_does_not_start_process(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            p=build_synthetic_launch_spec(synthetic_root=root,**args())
            self.assertEqual(p.run_dir,root/'POWERBALL'/ID)
            self.assertEqual(p.identity(),args())
            self.assertTrue(p.command_arguments[0].endswith('.py'))
            self.assertNotIn('source_data',' '.join(p.command_arguments))
            self.assertFalse(root.exists())
            with self.assertRaises(AttributeError):
                p.game_id='OZLOTTO'

    def test_valid_worker_is_self_report_only_and_console_exact(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            rc,records,identity=execute(root)
            self.assertEqual(rc,0)
            run=root/'POWERBALL'/ID
            result_raw=(run/'canonical_result.json').read_bytes()
            result=json.loads(result_raw)
            verify_success_records(records,game_id='POWERBALL',method_id='E_1',
                run_id=ID,target=1576,canonical_result=result_raw)
            self.assertTrue(result['not_a_forecast'])
            self.assertEqual(result['mode'],'SYNTHETIC_CONTRACT_TEST')
            self.assertEqual(result['variant_id'],VARIANT)
            self.assertEqual(result['schema'],'SYNTHETIC_COORDINATOR_PLUMBING_ONLY_V1')
            status=json.loads((run/'status.json').read_bytes())
            manifest=json.loads((run/'manifest.json').read_bytes())
            self.assertEqual(status['state'],'SUCCESS')
            self.assertEqual(status['mode'],'SYNTHETIC_CONTRACT_TEST')
            self.assertEqual(manifest['state'],'PASS')
            self.assertEqual(manifest['mode'],'SYNTHETIC_CONTRACT_TEST')
            self.assertFalse(manifest['worker_exit_certified'])
            self.assertTrue(manifest['coordinator_receipt_required'])
            self.assertEqual(manifest['canonical_result_sha256'],hashlib.sha256(result_raw).hexdigest())
            self.assertFalse((run/'exit_receipt.json').exists())
            self.assertFalse((root/CODE/'receipts').exists())

    def test_run_collision_fails_closed_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            self.assertEqual(execute(root)[0],0)
            path=root/'POWERBALL'/ID/'canonical_result.json';raw=path.read_bytes()
            with self.assertRaises(SystemExit):execute(root)
            self.assertEqual(path.read_bytes(),raw)

    def test_games_with_same_draw_do_not_overlap(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            self.assertEqual(execute(root)[0],0)
            spec=build_synthetic_launch_spec(synthetic_root=root,**args(game_id='OZLOTTO',draw_number=1576))
            self.assertEqual(spec.game_id,'OZLOTTO')
            self.assertNotEqual(spec.run_dir,root/'POWERBALL'/ID)
            self.assertFalse((root/'OZLOTTO').exists())

    def test_wrong_target_and_registry_rejected_before_run_dir(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            for changed in (dict(draw_number=1577),dict(draw_number=1578),dict(draw_number=1144),
                            dict(method_id='E_2'),dict(run_id='..'),
                            dict(variant_id='wrong/variant'),dict(variant_id='FULL_HISTORY_RAW_COUNTS_V1'),dict(variant_id='UNREGISTERED_VARIANT'),dict(group_id='bad&shell'),
                            dict(worker_sequence=0)):
                with self.subTest(changed=changed):
                    with self.assertRaises(ValueError):
                        build_synthetic_launch_spec(synthetic_root=root,**args(**changed))
            self.assertFalse(root.exists())

    def test_reject_unsafe_roots(self):
        with tempfile.TemporaryDirectory() as td:
            for root in (Path(td)/'results'/'multigame_synthetic_runs',
                         Path(td)/'source_data'/'multigame_synthetic_runs',
                         Path(td)/'unqualified'):
                with self.assertRaises(ValueError):
                    build_synthetic_launch_spec(synthetic_root=root,**args())

    def test_manifest_refuses_digest_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            run=root/'POWERBALL'/ID;run.mkdir(parents=True)
            identity=args()
            result={**identity,'draw_key':'POWERBALL_1576','mode':'SYNTHETIC_CONTRACT_TEST','schema':'SYNTHETIC_COORDINATOR_PLUMBING_ONLY_V1','data_kind':'SYNTHETIC_CONTRACT_TEST'}
            status={**identity,'mode':'SYNTHETIC_CONTRACT_TEST','state':'SUCCESS',
                'pid':3,'process_create_time_epoch':123.45,
                'canonical_result_sha256':'0'*64}
            (run/'status.json').write_bytes(json_bytes(status))
            with self.assertRaisesRegex(ValueError,'digest'):
                publish_coordinated_success(run_dir=run,identity=identity,status=status,result=result)
            self.assertEqual(sorted(p.name for p in run.iterdir()),['status.json'])

    def test_manifest_rejects_wrong_status_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs';run=root/'POWERBALL'/ID;run.mkdir(parents=True)
            identity=args();result={**identity,'draw_key':'POWERBALL_1576','mode':'SYNTHETIC_CONTRACT_TEST','schema':'SYNTHETIC_COORDINATOR_PLUMBING_ONLY_V1','data_kind':'SYNTHETIC_CONTRACT_TEST'}
            status={**identity,'mode':'SYNTHETIC_CONTRACT_TEST','state':'SUCCESS','pid':4,
                'process_create_time_epoch':123.45,
                'canonical_result_sha256':hashlib.sha256(json_bytes(result)).hexdigest()}
            (run/'status.json').write_bytes(json_bytes({**status,'game_id':'OZLOTTO'}))
            with self.assertRaisesRegex(ValueError,'status'):
                publish_coordinated_success(run_dir=run,identity=identity,status=status,result=result)
            self.assertFalse((run/'manifest.json').exists())

    def test_unresolved_global_orphan_blocks_launch(self):
        # No live global marker is modified. The method's marker lookup is
        # explicitly checked in source and checked via patching only the
        # method's reference to os.path.lexists.
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'multigame_synthetic_runs'
            original=module.os.path.lexists
            try:
                module.os.path.lexists=lambda p: True
                with self.assertRaises(SystemExit):execute(root)
            finally:
                module.os.path.lexists=original
            self.assertFalse(root.exists())

    def test_no_enable_or_network_or_termination_code(self):
        text=METHOD.read_text('utf-8')
        self.assertNotIn('subprocess',text)
        self.assertNotIn('urlopen',text)
        self.assertNotIn('taskkill',text)
        self.assertNotIn('from coordinator_private', text)
        self.assertNotIn('import coordinator_private', text)
        coord=(ROOT/'src'/'Powerball_Experiment_Coordinator.py').read_text('utf-8')
        self.assertIn('ENABLE_SCIENTIFIC_COORDINATION = False',coord)
        self.assertIn('ENABLE_PROCESS_TERMINATION = False',coord)

    def test_receipt_consumer_cannot_treat_plumbing_as_forecast(self):
        from coordinator_private.multigame_coordinator_exit_receipt import (
            issue_coordinator_receipt,verify_receipt_before_consume)
        with tempfile.TemporaryDirectory() as td:
            home=Path(td)
            root=home/'multigame_synthetic_runs'
            rc,records,ident=execute(root)
            self.assertEqual(rc,0)
            run=root/'POWERBALL'/ID
            group=home/CODE
            (group/'receipts').mkdir(parents=True)
            group_manifest={ 'group_id':CODE, 'success':True, 'status':'PASS',
                'orphan_suspected':False, 'marker_write_failed':False,
                'workers':[{'run_id':ID,'sequence':1,'state':'SUCCESS'}] }
            (group/'manifest.json').write_bytes(json_bytes(group_manifest))
            receipt=issue_coordinator_receipt(group_dir=group,run_dir=run,
                identity=ident,coordinator_sha256='b'*64,root_pid=321,
                root_create_time_epoch=1700000000.1,wrapper_exit_code=0,
                exit_observed_utc='2026-10-24T02:15:00+00:00',
                console_publication_records=records)
            self.assertTrue(receipt.exists())
            self.assertEqual(json.loads(receipt.read_bytes())['mode'],'SYNTHETIC_CONTRACT_TEST')
            with self.assertRaisesRegex(ValueError,'synthetic contract'):
                verify_receipt_before_consume(group_dir=group,run_dir=run,
                    identity=ident,coordinator_sha256='b'*64,
                    global_orphan_marker=home/'UNRESOLVED_ORPHAN.json')


if __name__=='__main__':unittest.main()
