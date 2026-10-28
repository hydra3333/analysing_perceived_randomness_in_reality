"""Offline-only receipt security tests; NO subprocess, network, or real data."""
from __future__ import annotations

import copy
from types import MappingProxyType
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'src' / 'methods'))
import _common.multigame_result_registry as result_registry
from coordinator_private.multigame_coordinator_exit_receipt import (
    issue_coordinator_receipt, verify_receipt_before_consume, _canonical, _hash
)

CODE_HASH = 'a'*64


def setup(root):
    group = root / 'group-test'
    run = root / 'runs' / 'mg-receipttest001'
    group.mkdir(); run.mkdir(parents=True)
    (group / 'receipts').mkdir()
    identity = dict(group_id='group-test', worker_sequence=1,
                    run_id=run.name, game_id='OZLOTTO', draw_number=1479,
                    method_id='E_1', variant_id='FULL_HISTORY_RAW_COUNTS_V1')
    labels = {k: v for k, v in identity.items() if k not in ('group_id', 'worker_sequence')}
    status = {**labels, 'mode':'COORDINATED', 'state':'SUCCESS',
              'pid':3001, 'process_create_time_epoch':1711111111.25}
    result = {**labels, 'draw_key': f"{identity['game_id']}_{identity['draw_number']}",
              'schema':'TEST_ONLY_COORDINATED_E1_RESULT_V1',
              'data_kind':'TEST_ONLY_FAKE_SCIENCE', 'mode':'COORDINATED',
              'payload':{'balls':'no lottery data'}}
    rbytes = _canonical(result)
    status['canonical_result_sha256'] = _hash(rbytes)
    manifest = {**labels, 'mode':'COORDINATED', 'state':'PASS',
                'orphan_suspected':False, 'marker_write_failed':False,
                'canonical_result_sha256':_hash(rbytes), 'synthetic_only':False}
    for name, obj in [('status.json',status),('manifest.json',manifest),
                      ('canonical_result.json',result)]:
        (run/name).write_bytes(_canonical(obj))
    agg = {'group_id':identity['group_id'],'success':True,'status':'PASS',
           'orphan_suspected':False,'marker_write_failed':False,
           'workers':[{'sequence':1,'run_id':identity['run_id'],'state':'SUCCESS'}]}
    (group/'manifest.json').write_bytes(_canonical(agg))
    return group, run, identity, result


# Test-only temporary scientific registration is never written to code.
# The shipped production allowlist remains EMPTY and scientific coordination OFF.
_FAKE_SCIENCE = MappingProxyType({('OZLOTTO','E_1','FULL_HISTORY_RAW_COUNTS_V1','COORDINATED'):
                                  ('TEST_ONLY_COORDINATED_E1_RESULT_V1','TEST_ONLY_FAKE_SCIENCE')})

def records(group, run, identity):
    from _common.multigame_console_protocol import prepare_success_records
    result=json.loads((run/'canonical_result.json').read_bytes())
    return prepare_success_records(game_id=identity['game_id'],
        method_id=identity['method_id'], run_id=identity['run_id'],
        target=identity['draw_number'], result=result)

def issue(group,run,identity,**changes):
    params = dict(group_dir=group, run_dir=run, identity=identity,
                  coordinator_sha256=CODE_HASH, root_pid=2201,
                  root_create_time_epoch=1711111000.125,
                  wrapper_exit_code=0,
                  exit_observed_utc='2026-10-24T02:25:31+00:00',
                  console_publication_records=None)
    params.update(changes)
    if params['console_publication_records'] is None:
        params['console_publication_records']=records(group,run,identity)
    with patch.object(result_registry, '_COORDINATED_SCIENCE_ALLOWLIST', _FAKE_SCIENCE):
        return issue_coordinator_receipt(**params)


def consume(group,run,identity):
    with patch.object(result_registry, '_COORDINATED_SCIENCE_ALLOWLIST', _FAKE_SCIENCE):
        return verify_receipt_before_consume(group_dir=group,run_dir=run,
            identity=identity,coordinator_sha256=CODE_HASH,
            global_orphan_marker=group.parent/'UNRESOLVED_ORPHAN.json')


class ReceiptTests(unittest.TestCase):
    def test_valid_issue_and_consume(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,result=setup(Path(t))
            path=issue(group,run,ident)
            self.assertEqual(path.parent,group/'receipts')
            self.assertFalse((run/'exit_receipt.json').exists())
            self.assertEqual(result,consume(group,run,ident))
            issued=json.loads(path.read_bytes())
            self.assertEqual(issued['schema'],'MULTIGAME_COORDINATOR_EXIT_RECEIPT_V2_REVIEW')
            self.assertEqual(set(issued['artifact_sha256']),
                {'status.json','manifest.json','canonical_result.json'})
            self.assertEqual(issued['root_pid'],2201)

    def test_preexisting_receipt_is_tamper_fail_no_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t))
            path=group/'receipts'/(ident['run_id']+'.json')
            path.write_bytes(b'SPOOFED')
            with self.assertRaises(FileExistsError):issue(group,run,ident)
            self.assertEqual(path.read_bytes(),b'SPOOFED')
            with self.assertRaises(ValueError):consume(group,run,ident)

    def test_receipt_absent_or_global_marker_blocks(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t))
            with self.assertRaises(ValueError):consume(group,run,ident)
            issue(group,run,ident)
            (Path(t)/'UNRESOLVED_ORPHAN.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'orphan'):consume(group,run,ident)

    def test_failed_group_and_orphan_group_block_even_with_receipt(self):
        for mode in ('FAIL','ORPHAN_SUSPECTED','MARKER_FAILED','WORKER_FAILED'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as t:
                group,run,ident,_=setup(Path(t));issue(group,run,ident)
                path=group/'manifest.json';obj=json.loads(path.read_bytes())
                if mode=='FAIL':obj['success']=False;obj['status']='FAIL'
                elif mode=='ORPHAN_SUSPECTED':obj['orphan_suspected']=True
                elif mode=='MARKER_FAILED':obj['marker_write_failed']=True
                else:obj['workers'][0]['state']='FAILED'
                path.write_bytes(_canonical(obj))
                with self.assertRaises(ValueError):consume(group,run,ident)

    def test_status_manifest_result_late_mutations(self):
        for name in ('status.json','manifest.json','canonical_result.json'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as t:
                group,run,ident,_=setup(Path(t));issue(group,run,ident)
                path=run/name; obj=json.loads(path.read_bytes());obj['late_write']=True
                path.write_bytes(_canonical(obj))
                with self.assertRaisesRegex(ValueError,'changed|tampered'):
                    consume(group,run,ident)

    def test_wrong_worker_game_draw_variant_or_coordinator_digest(self):
        for key, val in [('worker_sequence',2),('game_id','POWERBALL'),
                         ('draw_number',1480),('variant_id','WRONG_VARIANT')]:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as t:
                group,run,ident,_=setup(Path(t)); issue(group,run,ident)
                with self.assertRaises(ValueError):consume(group,run,{**ident,key:val})
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t));issue(group,run,ident)
            with self.assertRaises(ValueError):verify_receipt_before_consume(
                group_dir=group,run_dir=run,identity=ident,
                coordinator_sha256='b'*64,
                global_orphan_marker=Path(t)/'UNRESOLVED_ORPHAN.json')

    def test_coordinator_exit_metadata_fails_closed(self):
        for mutation in (dict(wrapper_exit_code=2),dict(root_pid=0),
                         dict(root_create_time_epoch=-1),
                         dict(exit_observed_utc='2026-10-24T12:00:00'),
                         dict(console_publication_records=[]),
                         dict(coordinator_sha256='nope')):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as t:
                group,run,ident,_=setup(Path(t))
                with self.assertRaises(ValueError):issue(group,run,ident,**mutation)
                self.assertEqual(list((group/'receipts').iterdir()),[])

    def test_issuer_rejects_tampered_worker_records(self):
        for name in ('status.json','manifest.json','canonical_result.json'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as t:
                group,run,ident,_=setup(Path(t))
                file=run/name; data=json.loads(file.read_bytes());data['game_id']='POWERBALL'
                file.write_bytes(_canonical(data))
                with self.assertRaises(ValueError):issue(group,run,ident)

    def test_symlink_receipts_directory_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t))
            (group/'receipts').rmdir()
            try:
                (group/'receipts').symlink_to(run,target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest('platform disallows symlinks')
            with self.assertRaises(ValueError):issue(group,run,ident)

    def test_integrity_before_result_open(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t));issue(group,run,ident)
            (run/'canonical_result.json').unlink()
            marker=Path(t)/'UNRESOLVED_ORPHAN.json'; marker.write_text('{}')
            with self.assertRaisesRegex(ValueError,'orphan'):
                consume(group,run,ident)
            marker.unlink()
            (group/'manifest.json').write_bytes(_canonical({'status':'FAIL'}))
            with self.assertRaisesRegex(ValueError,'group'):
                consume(group,run,ident)

    def test_existing_poc_gates_remain_disabled_and_original_hash_known(self):
        p=ROOT/'src'/'Powerball_Experiment_Coordinator.py'
        content=p.read_text(encoding='utf-8')
        self.assertIn('ENABLE_PROCESS_TERMINATION = False',content)
        self.assertIn('ENABLE_SCIENTIFIC_COORDINATION = False',content)
        self.assertIn("parser.add_argument('--poc'",content.replace('"','\''))
        self.assertIn('check_exited_worker_for_orphan',content)


    def test_c1_console_digest_is_bound_to_exact_single_read(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t))
            lines=records(group,run,ident)
            file=run/'canonical_result.json'
            altered=json.loads(file.read_bytes())
            altered['payload']['balls']='synthetically altered after console write'
            altered_bytes=_canonical(altered)
            file.write_bytes(altered_bytes)
            # Simulate even a worker that rewrote its status/manifest hashes
            # to match the changed result: the console binding still fails.
            for name in ('status.json','manifest.json'):
                p=run/name; val=json.loads(p.read_bytes())
                val['canonical_result_sha256']=_hash(altered_bytes)
                p.write_bytes(_canonical(val))
            with self.assertRaisesRegex(ValueError, 'console|mismatch|digest|record'):
                issue(group,run,ident,console_publication_records=lines)
            self.assertEqual(list((group/'receipts').iterdir()),[])

    def test_c1_canonical_file_opened_once_during_issuance(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t))
            raw_read=Path.read_bytes
            reads=[]
            def counting_read(path):
                if path == run/'canonical_result.json':
                    reads.append(path)
                return raw_read(path)
            # Precompute console lines, then monitor issuer's file reads only.
            transcript=records(group,run,ident)
            with patch.object(Path, 'read_bytes', counting_read):
                issue(group,run,ident,console_publication_records=transcript)
            self.assertEqual(len(reads),1)

    def test_c1_rejects_spoofed_console_digest_or_result(self):
        for index in (1,2):
            with self.subTest(index=index),tempfile.TemporaryDirectory() as t:
                group,run,ident,_=setup(Path(t))
                lines=list(records(group,run,ident));lines[index]='RESULT BAD' if index==1 else 'DIGEST '+('b'*64)
                with self.assertRaises(ValueError):
                    issue(group,run,ident,console_publication_records=lines)
                self.assertEqual(list((group/'receipts').iterdir()),[])

    def test_c2_requires_exit_observed_timestamp_not_issuance_time(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,_=setup(Path(t))
            with self.assertRaises(ValueError):
                issue(group,run,ident,exit_observed_utc=None)
            candidate=(ROOT/'src'/'Powerball_Experiment_Coordinator.py').read_text()
            self.assertIn('w.exit_observed_utc = ISO()',candidate)
            self.assertIn('exit_observed_utc=w.exit_observed_utc',candidate)
            self.assertNotIn('exit_observed_utc=ISO()',candidate)

    def test_coordinator_private_import_is_append_only_and_location_checked(self):
        source=(ROOT/'src'/'Powerball_Experiment_Coordinator.py').read_text()
        self.assertIn('sys.path.append(method_root)',source)
        self.assertNotIn('sys.path.insert(0, method_root)',source)
        self.assertIn('actual_issuer != expected_issuer',source)
        self.assertIn('untrusted coordinator receipt issuer location',source)
        self.assertIn("'multigame_coordinator_exit_receipt.py').resolve(strict=True)",source)

    def test_verifier_opens_canonical_result_once_and_returns_that_object(self):
        with tempfile.TemporaryDirectory() as t:
            group,run,ident,result=setup(Path(t))
            issue(group,run,ident)
            orig=Path.read_bytes
            opened=[]
            def track_read(path):
                if path == run/'canonical_result.json':
                    opened.append(path)
                return orig(path)
            with patch.object(Path,'read_bytes',track_read):
                consumed=consume(group,run,ident)
            self.assertEqual(consumed,result)
            self.assertEqual(len(opened),1)

    def test_coordinator_private_module_and_noop_removed(self):
        self.assertFalse((ROOT/'src'/'methods'/'_common'/'multigame_coordinator_exit_receipt_v1.py').exists())
        self.assertTrue((ROOT/'src'/'coordinator_private'/'multigame_coordinator_exit_receipt.py').is_file())
        source=(ROOT/'src'/'Powerball_Experiment_Coordinator.py').read_text()
        self.assertNotIn("final['workers'] = reports",source)

if __name__=='__main__':unittest.main()
