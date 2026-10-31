"""WF-1B: N1's seed policy records (design v0.1r1 sections 7.6, 8.1-8.4 and 10; decisions WF1-9, WF1-12; EX_109 B01).

The negative fixtures use an invented root ('AB' x 64), never a beacon value."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from evaluation import seed_policies as SP   # noqa: E402

INSTALLED = 'N1_ROOT_NIST_C2_20261031T1030Z_V1'


class Installed(unittest.TestCase):

    def test_the_installed_records(self):
        recs = {r['policy_id']: r for r in SP._records()}
        self.assertEqual(set(recs), set(SP.ANNOUNCED))
        self.assertEqual(recs['N1_ROOT_NIST_C2_20261106T0000Z_V1']['status'], 'REPLACED_BEFORE_PULSE')
        p = SP.approved_policy()
        self.assertEqual(p['policy_id'], INSTALLED)
        self.assertEqual((p['time_stamp'], p['chain_index'], p['pulse_index'], p['status_code'], p['version']),
                         ('2026-10-31T10:30:00.000Z', 2, 2007128, 0, '2.0'))
        self.assertEqual(p['uri'], 'https://beacon.nist.gov/beacon/2.0/chain/2/pulse/2007128')
        self.assertEqual([s['url'] for s in p['sources']],
                         ['https://beacon.nist.gov/beacon/2.0/pulse/time/1793442600000', p['uri']])
        self.assertEqual(p['signature_verification'], 'NOT_PERFORMED')
        self.assertEqual(SP.count_policies(), 2)

    def test_announced_epochs_match_their_time_stamps(self):
        from datetime import datetime, timezone
        for pid, a in SP.ANNOUNCED.items():
            t = datetime.strptime(a['time_stamp'], '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
            self.assertEqual(int(t.timestamp()) * 1000, a['epoch_ms'], pid)


class Binding(unittest.TestCase):
    """Every way a record can fail to describe the announced pulse and its two official reads is refused."""

    def setUp(self):
        self.good = json.loads((SP.FOLDER / f'{INSTALLED}.json').read_text())
        self.good['output_value'] = 'AB' * 64                     # invented, never a beacon value

    def refused(self, rec):
        with self.assertRaises(ValueError):
            SP.validate(rec)

    def variant(self, **changes):
        rec = copy.deepcopy(self.good)
        rec.update(changes)
        return rec

    def test_the_good_fixture_passes(self):
        SP.validate(self.good)

    def test_wrong_time_chain_version_and_status(self):
        self.refused(self.variant(time_stamp='2099-01-01T00:00:00.000Z'))
        self.refused(self.variant(time_stamp='2026-10-31T10:31:00.000Z'))
        self.refused(self.variant(chain_index=1))
        self.refused(self.variant(chain_index='2'))
        self.refused(self.variant(version='1.0'))
        self.refused(self.variant(status_code=1))
        self.refused(self.variant(status_code=False))

    def test_malformed_pulse_index_and_uri(self):
        self.refused(self.variant(pulse_index='not-an-integer'))
        self.refused(self.variant(pulse_index=0))
        self.refused(self.variant(pulse_index=True))
        self.refused(self.variant(pulse_index=2007129))             # no longer matches the URI and source
        self.refused(self.variant(uri='https://beacon.nist.gov/beacon/2.0/chain/2/pulse/2007129'))
        self.refused(self.variant(uri='http://beacon.nist.gov/beacon/2.0/chain/2/pulse/2007128'))

    def test_wrong_origin_and_reads(self):
        for srcs in ([], [self.good['sources'][0]],
                     [dict(self.good['sources'][0], url='https://example.com/beacon/2.0/pulse/time/1793442600000'),
                      self.good['sources'][1]],
                     [dict(self.good['sources'][0], url='https://beacon.nist.gov/beacon/2.0/pulse/last'),
                      self.good['sources'][1]],
                     [self.good['sources'][1], self.good['sources'][0]],
                     [self.good['sources'][0], dict(self.good['sources'][1], read_by=self.good['sources'][0]['read_by'])],
                     ['https://beacon.nist.gov/beacon/2.0/pulse/time/1793442600000', self.good['uri']]):
            with self.subTest(sources=srcs):
                self.refused(self.variant(sources=srcs))
        self.refused(self.variant(verified_by=self.good['fetched_by']))

    def test_mismatched_or_unannounced_policy(self):
        self.refused(self.variant(policy_id='N1_ROOT_NIST_C2_20261101T0000Z_V1'))
        self.refused(self.variant(policy_id='N1_ROOT_NIST_C2_20261106T0000Z_V1'))   # announced, but another pulse

    def test_root_certificate_and_signature_fields(self):
        self.refused(self.variant(output_value=('AB' * 64).lower()))
        self.refused(self.variant(output_value='AB' * 63))
        self.refused(self.variant(certificate_id=self.good['certificate_id'].upper()))
        self.refused(self.variant(signature_verification='VERIFIED'))
        self.refused(self.variant(owner_file_sha256='x'))
        for missing in ('owner_file_sha256', 'certificate_id', 'sources', 'signature_verification', 'approved_by'):
            bad = copy.deepcopy(self.good)
            del bad[missing]
            self.refused(bad)

    def test_other_statuses_carry_no_root(self):
        SP.validate({'schema': SP.SCHEMA, 'policy_id': INSTALLED, 'status': 'REFUSED'})
        self.refused({'schema': SP.SCHEMA, 'policy_id': INSTALLED, 'status': 'REFUSED', 'output_value': 'AB' * 64})


class Selection(unittest.TestCase):

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.dir = Path(self.td.name)
        self.good = json.loads((SP.FOLDER / f'{INSTALLED}.json').read_text())
        self.good['output_value'] = 'AB' * 64

    def tearDown(self):
        self.td.cleanup()

    def put(self, rec, name=None):
        (self.dir / f"{name or rec['policy_id']}.json").write_text(json.dumps(rec))

    def test_only_one_valid_approved_record_is_used(self):
        with mock.patch.object(SP, 'FOLDER', self.dir):
            self.assertIsNone(SP.approved_policy())                 # no record: N1 off (7.6), no fallback root
            self.put({'schema': SP.SCHEMA, 'policy_id': 'N1_ROOT_NIST_C2_20261106T0000Z_V1',
                      'status': 'REPLACED_BEFORE_PULSE'})
            self.assertIsNone(SP.approved_policy())
            self.put(self.good)
            self.assertEqual(SP.approved_policy()['output_value'], 'AB' * 64)
            self.assertEqual(SP.count_policies(), 2)
            bad = dict(self.good, time_stamp='2099-01-01T00:00:00.000Z')
            self.put(bad)
            with self.assertRaises(ValueError):                       # a bad record stops everything (fail closed)
                SP.approved_policy()

    def test_two_approved_records_or_a_misnamed_file_are_refused(self):
        with mock.patch.object(SP, 'FOLDER', self.dir):
            self.put(self.good)
            self.put(self.good, name='copy_of_the_same_policy')
            with self.assertRaises(ValueError):
                SP.approved_policy()
        with mock.patch.object(SP, 'FOLDER', self.dir), mock.patch.dict(
                SP.ANNOUNCED, {'N1_ROOT_TEST_SECOND_V1': dict(SP.ANNOUNCED[INSTALLED])}):
            (self.dir / 'copy_of_the_same_policy.json').unlink()
            second = dict(self.good, policy_id='N1_ROOT_TEST_SECOND_V1')
            self.put(second)
            with self.assertRaises(ValueError):                       # two APPROVED policies: refused
                SP.approved_policy()


if __name__ == '__main__':
    unittest.main()
