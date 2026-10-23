"""Review-candidate synthetic-only E_1 U-view and standalone firewall tests.

This suite creates invented CSV files in isolated temp dirs. It neither
imports nor reads the actual source_data CSV files or the original holdout.
"""
from __future__ import annotations

import csv
from unittest.mock import patch
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'src' / 'methods'))
from _common.e1_training_view_v0_1 import (  # noqa
    U_COLUMNS, load_permitted_u_view, build_e1_forecast)
from _common.e1_standalone_contract_v0_1 import (  # noqa
    verify_and_consume, canonical_json, sha)
import E_001_Historical_Appearance_Frequency as runner  # noqa

FIXTURE = json.loads((BASE / 'tests' / 'p3_e1_synthetic_v0_3.json').read_text())
TARGET = 1152


def csv_rows(path: Path, *, with_future: bool = False, future_poison: str | None = None,
             unordered: bool = True):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        columns = list(U_COLUMNS) if unordered else ['Draw_Number','Date','Drawn_1','Drawn_2',
                                  'Drawn_3','Drawn_4','Drawn_5','Drawn_6','Drawn_7','Powerball']
        writer.writerow(columns)
        for row in FIXTURE['rows']:
            day = date(2018,4,19) + timedelta(days=7*(row['draw']-1144))
            writer.writerow([row['draw'], day.isoformat(), *row['main'], row['powerball']])
        if with_future:
            if future_poison is None:
                writer.writerow([TARGET, '2018-06-14', 1,2,3,4,5,6,7,1])
            else:
                stream.write(future_poison + '\n')


class E1LoaderAndRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='e1_synthetic_contract_')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = self.root / 'synthetic.csv'
        csv_rows(self.data)
        self.runs = self.root / 'runs'

    def load(self, file: Path | None = None):
        return load_permitted_u_view(file or self.data, TARGET, source_kind='SYNTHETIC_CONTRACT_TEST')

    def run_cli(self, rid: str):
        return runner.main(['--mode','synthetic-contract','--target',str(TARGET),
                           '--source',str(self.data),'--synthetic-run-root',str(self.runs),
                           '--run-id',rid])

    def consume(self, rid: str):
        return verify_and_consume(self.runs / rid, run_id=rid, target=TARGET,
                                  mode='SYNTHETIC_CONTRACT_TEST')

    def test_golden_prefix_and_count(self):
        records, digest = self.load()
        self.assertEqual(len(records), 8)
        self.assertEqual(records[0]['draw'], 1144)
        self.assertEqual(records[-1]['draw'], 1151)
        forecast = build_e1_forecast(records, digest, TARGET, source_kind='SYNTHETIC_CONTRACT_TEST')
        self.assertEqual(sum(forecast['MAIN']['scores'].values()), 56)
        self.assertEqual(sum(forecast['POWERBALL']['scores'].values()), 8)
        self.assertEqual(digest, '3851fa46400f44a1be6fb85fee72dfc4cc93585cef81b2a394bc0d86c4b895c9')
        self.assertEqual(sha(canonical_json(forecast)), '8a7f917ac8deb9307d31100e7cd811f87897b563d907d5ab5eab911708545eb9')
        self.assertEqual(forecast['MAIN']['top'], [1,8,2,5,7,4,6])
        self.assertEqual(forecast['MAIN']['worst'], [15,19,29,31,20,17,18])
        self.assertEqual(forecast['MAIN']['worst'], list(reversed(forecast['MAIN']['ranking']))[:7])
        self.assertEqual(forecast['POWERBALL']['top'], 1)

    def test_no_future_read_and_no_whole_source_hash_leakage(self):
        old_rows, old_digest = self.load()
        old = build_e1_forecast(old_rows, old_digest, TARGET, source_kind='SYNTHETIC_CONTRACT_TEST')
        # Deliberately append an invalid row N, plus malformed later lines;
        # loader MUST NOT inspect any of them (not even its CSV syntax).
        with self.data.open('a',encoding='utf-8') as f:
            f.write('1152,BAD,IMPOSSIBLE,FUTURE,"UNFINISHED QUOTE\n')
            f.write('malformed junk\n')
        new_rows, new_digest = self.load()
        new = build_e1_forecast(new_rows, new_digest, TARGET, source_kind='SYNTHETIC_CONTRACT_TEST')
        self.assertEqual(old_digest, new_digest)
        self.assertEqual(canonical_json(old), canonical_json(new))
        # Even a changed filename and differing whole-source bytes are irrelevant.
        clone = self.root/'renamed_whole_source.csv'
        shutil.copyfile(self.data, clone)
        self.assertEqual(self.load(clone)[1], old_digest)
        # Change a permitted training value: must change model digest.
        permitted = self.root/'changed_training.csv'
        csv_rows(permitted)
        text = permitted.read_text()
        text = text.replace(',9,10,11,12,1\n', ',9,10,11,13,1\n', 1)
        if text == permitted.read_text():
            # Stable alternative without relying on exact CSV substring.
            lines = text.splitlines(); vals = lines[2].split(','); vals[3] = '17'
            lines[2] = ','.join(vals); text='\n'.join(lines)+'\n'
        permitted.write_text(text)
        self.assertNotEqual(self.load(permitted)[1], old_digest)

    def test_reject_holdout_and_sealed_future(self):
        for target in (1144,1578,1580,1587,1588,2000):
            with self.subTest(target=target), self.assertRaises(ValueError):
                load_permitted_u_view(self.data,target,source_kind='SYNTHETIC_CONTRACT_TEST')

    def test_refuse_wrong_schemas_and_invalid_prefix(self):
        not_u = self.root/'order.csv'; csv_rows(not_u, unordered=False)
        with self.assertRaisesRegex(ValueError, 'drawn-order'):
            self.load(not_u)
        short = self.root/'short.csv'; csv_rows(short)
        lines = short.read_text().splitlines()
        short.write_text('\n'.join(lines[:-1])+'\n')
        with self.assertRaisesRegex(ValueError, 'missing required'):
            self.load(short)
        bad_date = self.root/'bad.csv'; csv_rows(bad_date)
        s=bad_date.read_text().replace('2018-04-19','2018-04-20')
        bad_date.write_text(s)
        with self.assertRaisesRegex(ValueError, 'date not'):
            self.load(bad_date)
        bad_pb = self.root/'pb.csv'; csv_rows(bad_pb)
        s=bad_pb.read_text().splitlines(); parts=s[1].split(','); parts[-1]='21'; s[1]=','.join(parts)
        bad_pb.write_text('\n'.join(s)+'\n')
        with self.assertRaisesRegex(ValueError, 'out of range'):
            self.load(bad_pb)

    def test_early_started_and_success_firewall(self):
        rid='e1-syntheticpass001'
        self.assertEqual(self.run_cli(rid),0)
        run_dir=self.runs/rid
        status=json.loads((run_dir/'status.json').read_text())
        manifest=json.loads((run_dir/'standalone_manifest.json').read_text())
        self.assertEqual(status['state'],'SUCCESS')
        self.assertEqual(status['schema'],'ENGINEERING_POC_STATUS_V1')
        self.assertEqual(status['case'],'E_001_Historical_Appearance_Frequency')
        self.assertGreater(status['process_create_time_epoch'], 0)
        self.assertEqual(status['sys_prefix'], sys.prefix)
        self.assertGreaterEqual(status['elapsed_seconds'], 0)
        self.assertGreaterEqual(status['cpu_time_seconds'], 0)
        self.assertIn(status['peak_field'], ('peak_wset', 'peak_rss', 'UNAVAILABLE'))
        self.assertEqual(manifest['state'],'PASS')
        self.assertFalse(manifest['external_exit_code_verified'])
        out=self.consume(rid)
        self.assertEqual(out['MAIN']['top'][:3],[1,8,2])
        self.assertEqual(self.run_cli(rid),2)  # Existing run dir may never be overwritten.
        # Changing result after publication always fails hash verification.
        raw=(run_dir/'canonical_result.json').read_bytes()
        (run_dir/'canonical_result.json').write_bytes(raw+b' ')
        with self.assertRaises(ValueError):
            self.consume(rid)

    def test_same_forecast_content_different_run_ids(self):
        one='e1-twoidentities01'; two='e1-twoidentities02'
        self.assertEqual(self.run_cli(one), 0)
        self.assertEqual(self.run_cli(two), 0)
        self.assertNotEqual((self.runs/one/'status.json').read_bytes(),
                            (self.runs/two/'status.json').read_bytes())
        self.assertEqual((self.runs/one/'canonical_result.json').read_bytes(),
                         (self.runs/two/'canonical_result.json').read_bytes())

    def test_reject_fake_pass_failed_or_orphan(self):
        rid='e1-firewallchecks01'
        self.assertEqual(self.run_cli(rid),0)
        rd=self.runs/rid
        original=(rd/'standalone_manifest.json').read_bytes()
        for change in ({'state':'FAIL'}, {'orphan_suspected':True},
                       {'marker_write_failed':True}, {'run_id':'e1-otherfakeid'},
                       {'training_view_sha256':'f'*64}):
            m=json.loads(original); m.update(change)
            (rd/'standalone_manifest.json').write_bytes(canonical_json(m))
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.consume(rid)
        (rd/'standalone_manifest.json').write_bytes(original)
        # Incomplete/missing manifests can't be rescued by a valid result.
        (rd/'standalone_manifest.json').unlink()
        with self.assertRaises((OSError, ValueError)):
            self.consume(rid)
        (rd/'standalone_manifest.json').write_bytes(original)
        marker=self.root/'UNRESOLVED_ORPHAN.json'; marker.write_text('{}')
        with self.assertRaisesRegex(ValueError,'orphan'):
            verify_and_consume(rd,run_id=rid,target=TARGET,mode='SYNTHETIC_CONTRACT_TEST',
                               unresolved_orphan_marker=marker)

    def test_failed_run_persists_without_pass(self):
        rid='e1-invalidfixture01'
        self.data.write_text('not,a,valid,header\n')
        self.assertEqual(self.run_cli(rid),1)
        rd=self.runs/rid
        self.assertEqual(json.loads((rd/'status.json').read_text())['state'],'FAILED')
        self.assertEqual(json.loads((rd/'standalone_manifest.json').read_text())['state'],'FAIL')
        # Even if a late result appears after a FAILED run, it cannot be consumed.
        valid_csv=self.root/'late_valid.csv'; csv_rows(valid_csv)
        valid=self.load(valid_csv)
        from _common.e1_training_view_v0_1 import build_e1_forecast
        result=build_e1_forecast(*valid, TARGET, source_kind='SYNTHETIC_CONTRACT_TEST')
        (rd/'canonical_result.json').write_bytes(canonical_json(result))
        with self.assertRaisesRegex(ValueError, 'non-PASS'):
            self.consume(rid)

    def test_interrupt_is_fail_closed(self):
        from unittest.mock import patch
        rid='e1-interruptedstatus01'
        with patch('_common.e1_training_view_v0_1.load_permitted_u_view',
                   side_effect=KeyboardInterrupt):
            self.assertEqual(self.run_cli(rid), 1)
        rd=self.runs/rid
        st=json.loads((rd/'status.json').read_text())
        self.assertEqual(st['state'], 'FAILED')
        self.assertEqual(st['failure_reason'], 'INTERRUPTED')
        self.assertEqual(json.loads((rd/'standalone_manifest.json').read_text())['state'], 'FAIL')
        with self.assertRaises(ValueError):
            self.consume(rid)

    def test_runtime_schema_is_shared_with_poc_helper(self):
        from _common.experiment_runtime_status_and_resources import ProbeStatus
        self.assertEqual(ProbeStatus.__module__, '_common.experiment_runtime_status_and_resources')
        rid='e1-sharedruntime01'
        self.assertEqual(self.run_cli(rid),0)
        status=json.loads((self.runs/rid/'status.json').read_text())
        self.assertIn('elapsed_seconds', status)
        self.assertIn('cpu_time_seconds', status)
        self.assertIn('process_create_time_epoch', status)
        # Candidate remains bounded: none of these identities contain draw N.
        self.assertEqual(status['target_draw'], TARGET)

    def test_original_poc_status_helper_api(self):
        from _common.experiment_runtime_status_and_resources import ProbeStatus
        path=self.root/'poc_status.json'
        probe=ProbeStatus(path,'poc-testexistingapi','canonical-fixture')
        started=json.loads(path.read_text())
        self.assertEqual(started['schema'],'ENGINEERING_POC_STATUS_V1')
        self.assertEqual(started['case'],'canonical-fixture')
        self.assertEqual(started['state'],'STARTED')
        probe.finish('SUCCESS')
        done=json.loads(path.read_text())
        self.assertEqual(done['state'],'SUCCESS')
        self.assertIn('elapsed_seconds',done)
        self.assertIn('cpu_time_seconds',done)

    def test_real_gate_off_refuses_before_source_read(self):
        """Guard independently of the runner's shipped gate value.

        This test patches the gate OFF even after a future activation commit.
        No genuine source_data path is used and the CSV loader is never called.
        """
        fake_project = self.root / 'isolated_fake_project'
        fake_source = fake_project / 'source_data' / 'australian_powerball_history_20261021.csv'
        fake_runner_path = fake_project / 'src' / 'methods' / 'E_001_Historical_Appearance_Frequency.py'
        with (patch.object(runner, 'ENABLE_REAL_HISTORICAL_DEVELOPMENT', False),
              patch.object(runner, '__file__', str(fake_runner_path)),
              patch('_common.e1_training_view_v0_1.load_permitted_u_view',
                    side_effect=AssertionError('disabled real mode must not invoke loader')) as loader):
            with self.assertRaises(SystemExit) as stopped:
                runner.main(['--mode', 'historical-development', '--target', '1152',
                             '--source', str(fake_source), '--run-id', 'e1-gateoff01'])
            self.assertEqual(stopped.exception.code, 2)
            loader.assert_not_called()
        self.assertFalse((fake_project / 'transitory_data' / 'p3_standalone_runs').exists())

    def test_real_gate_on_rejects_invalid_targets_and_sources(self):
        """Patch gate ON only in-test; never inspect the actual real dataset.

        All "source_data" inputs here live under a fake project in a temporary
        directory. Non-source-data paths, bad file names and out-of-range
        targets must fail without opening their CSV. A drawn-order CSV can
        only be identified by reading its HEADER, but no training rows may
        be parsed after that header is rejected.
        """
        fake_project = self.root / 'isolated_fake_project'
        trusted = fake_project / 'source_data'
        trusted.mkdir(parents=True)
        fake_runner_path = fake_project / 'src' / 'methods' / 'E_001_Historical_Appearance_Frequency.py'
        name = 'australian_powerball_history_20261021.csv'
        approved = trusted / name
        approved.write_text('POISON: this is NOT a permitted training CSV\n', encoding='utf-8')
        outside = self.root / 'untrusted'
        outside.mkdir()
        untrusted = outside / name
        untrusted.write_text('POISON: source outside trusted directory\n', encoding='utf-8')
        wrong_name = trusted / 'australian_powerball_drawn_order_20261021.csv'
        wrong_name.write_text('POISON: wrong name\n', encoding='utf-8')
        drawn_order = trusted / 'australian_powerball_history_20261022.csv'
        csv_rows(drawn_order, unordered=False)
        cases = (
            ('holdout_1578', 1578, approved, 2, 0, 'invalid target'),
            ('holdout_1587', 1587, approved, 2, 0, 'invalid target'),
            ('before_first_1144', 1144, approved, 2, 0, 'invalid target'),
            ('after_holdout_1588', 1588, approved, 2, 0, 'invalid target'),
            ('untrusted_directory', 1152, untrusted, 1, 0, 'trusted source_data'),
            ('wrong_filename', 1152, wrong_name, 1, 0, 'approved unordered-file name'),
            ('drawn_order_header', 1152, drawn_order, 1, 1, 'drawn-order'),
        )
        original_path_open = Path.open
        with (patch.object(runner, 'ENABLE_REAL_HISTORICAL_DEVELOPMENT', True),
              patch.object(runner, '__file__', str(fake_runner_path))):
            for case, target, source, expected_rc, expected_opens, failure_text in cases:
                with self.subTest(case=case):
                    source_open_count = []

                    def monitored_open(path, *args, **kwargs):
                        if path == source:
                            source_open_count.append(1)
                        return original_path_open(path, *args, **kwargs)

                    run_id = 'e1-gatecheck-' + case.replace('_', '-')
                    with patch.object(Path, 'open', monitored_open):
                        rc = runner.main(['--mode', 'historical-development',
                                          '--target', str(target), '--source', str(source),
                                          '--run-id', run_id])
                    self.assertEqual(rc, expected_rc)
                    self.assertEqual(len(source_open_count), expected_opens)
                    run_dir = fake_project / 'transitory_data' / 'p3_standalone_runs' / run_id
                    self.assertFalse((run_dir / 'canonical_result.json').exists())
                    self.assertFalse((run_dir / 'standalone_manifest.json').exists() and
                                     json.loads((run_dir / 'standalone_manifest.json').read_text())['state'] == 'PASS')
                    if expected_rc == 1:
                        st = json.loads((run_dir / 'status.json').read_text())
                        self.assertEqual(st['state'], 'FAILED')
                        self.assertIn(failure_text, st['error'])
                        mf = json.loads((run_dir / 'standalone_manifest.json').read_text())
                        self.assertEqual(mf['state'], 'FAIL')
                    else:
                        self.assertFalse(run_dir.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
