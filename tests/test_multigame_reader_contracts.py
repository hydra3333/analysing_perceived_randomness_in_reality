"""Package 2 v0.11: in-sandbox OFFLINE N-1 and frozen forecast regression.

Only synthetic fixtures and the accepted development masters are opened; no
holdout or Windows coordinator/lifecycle invocation occurs in this module.
"""
import csv
from datetime import date
import hashlib
import inspect
import json
import os
import re
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src' / 'methods'))
from _common.game_draws_reader import (DrawView, load_pinned_draw_view, header_for,
                                           _parse_prefix, _owned)
from E_001.e1_common_reader_bridge import prepared_e1_forecast
from E_001.e1_historical_appearance_frequency import canonical_bytes
from _common.game_profiles import POWERBALL, OZLOTTO
from _common.multigame_result_registry import _COORDINATED_SCIENCE_ALLOWLIST

SHA = {'POWERBALL':'ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8',
       'OZLOTTO':'4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f'}


def pin(game, target, *, method='E_1', variant='FULL_HISTORY_RAW_COUNTS_V1',
        kind='UNORDERED_SET', dates=False, sha=None):
    return dict(schema='DEVELOPMENT_MASTER_PIN_V1_REVIEW', game_id=game,
                method_id=method, variant_id=variant, draw_number=target,
                view_kind=kind, include_dates=dates,
                master_file=f'{game}_results_master.csv', ledger_version=1,
                master_sha256=sha or SHA[game])


def fake_root(root, game='OZLOTTO', *, size=9, corrupt_suffix=b'\xff\x00 secret after N',
              later_suffix=b'FAKE_AFTER_TARGET,\xff,garbage', date_shift=None):
    """A synthetic stand-in for an owner-attested master; no result values."""
    p=OZLOTTO if game=='OZLOTTO' else POWERBALL
    d=root/'source_data';d.mkdir(parents=True,exist_ok=True)
    lines=[','.join(header_for(game)).encode('ascii')+b'\n']
    for i in range(size):
        draw=p.first_draw+i
        main=list(range(7+i%2,14+i%2)) if game=='OZLOTTO' else list(range(3+i%2,10+i%2))
        when=p.derived_date(draw).isoformat()
        if date_shift is not None and i==date_shift: when='1900-01-01'
        seq=[draw,when,*main]
        if game=='POWERBALL': seq += [2]
        else: seq += [40,41,42]
        lines.append((','.join(map(str,seq))+'\n').encode('ascii'))
    # No CSV parser may ever consume this suffix. Its first field is the target.
    lines.append(str(p.first_draw+size).encode('ascii')+b','+corrupt_suffix+b'\n')
    if later_suffix is not None:
        lines.append(later_suffix+b'\n')
    raw=b''.join(lines)
    sha=hashlib.sha256(raw).hexdigest()
    (d/f'{game}_results_master.csv').write_bytes(raw)
    # Provenance records are fixtures only; the production owner-managed master
    # tool has already validated the real INIT master at its pinned SHA.
    ledger=(
        'version,utc,action,master_sha256,first_draw,last_draw,draw_count\n'
        f'1,fixture,INIT,{sha},{p.first_draw},{p.holdout_first-1},{p.holdout_first-p.first_draw}\n'
    )
    (d/f'{game}_results_master_ledger.csv').write_bytes(ledger.encode('ascii'))
    evidence={'master_sha256':sha,'master_file':f'{game}_results_master.csv',
              'game':game,'first_draw':p.first_draw,'last_draw':p.holdout_first-1,
              'draw_count':p.holdout_first-p.first_draw,
              'source':'LOTTERYWEST_GOV_RESULTS_SEARCH'}
    (d/f'{game}_results_master_init_verification.json').write_text(json.dumps(evidence))
    return sha, p.first_draw+size


class V011ReaderTests(unittest.TestCase):
    def test_master_source_and_ledger_file_hashes(self):
        for game in SHA:
            with self.subTest(game=game):
                b=(ROOT/'source_data'/f'{game}_results_master.csv').read_bytes()
                self.assertEqual(hashlib.sha256(b).hexdigest(),SHA[game])
                p=POWERBALL if game=='POWERBALL' else OZLOTTO
                self.assertEqual((p.holdout_first,p.holdout_last),
                                 (1577,1586) if game=='POWERBALL' else (1694,1703))

    def test_e1_frozen_1577_forecast_only_without_dev_build(self):
        v=load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('POWERBALL',1577))
        self.assertEqual(len(v.draw_number),433)
        self.assertEqual((int(v.draw_number[0]),int(v.draw_number[-1])),(1144,1576))
        self.assertIsNone(v.draw_date)
        forecast,digest=prepared_e1_forecast(v)
        self.assertEqual(digest,'d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339')
        self.assertEqual(hashlib.sha256(canonical_bytes(forecast)).hexdigest(),
                         '7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e')
        self.assertEqual(forecast['MAIN']['top'],[9,17,7,11,18,30,12])
        self.assertEqual(forecast['MAIN']['worst'],[31,13,8,29,26,33,35])
        self.assertEqual(forecast['POWERBALL']['top'],2)
        self.assertEqual(forecast['POWERBALL']['worst'],12)
        for arr in (v.draw_number,v.main,v.powerball):
            self.assertIs(type(arr.base),bytes)
            self.assertEqual(len(arr.base),arr.size*arr.dtype.itemsize)
            self.assertFalse(arr.flags.writeable)
            with self.assertRaises(ValueError):arr.setflags(write=True)
        self.assertFalse(_COORDINATED_SCIENCE_ALLOWLIST)

    def test_existing_synthetic_e1_goldens_unchanged(self):
        # Pure arithmetic; do not run or enable the real standalone entry point.
        from E_001.e1_training_view import build_e1_forecast
        from E_001.e1_historical_appearance_frequency import canonical_bytes
        from E_001.e1_standalone_contract import sha
        fixture=json.loads((ROOT/'tests'/'p3_e1_synthetic_v0_3.json').read_text())
        rows=fixture['rows']
        digest=hashlib.sha256(canonical_bytes({
            'schema':'E1_SYNTHETIC_CSV_U_TRAINING_VIEW_V1',
            'data_kind':'SYNTHETIC_CONTRACT_TEST', 'records':rows})).hexdigest()
        self.assertEqual(digest,'3851fa46400f44a1be6fb85fee72dfc4cc93585cef81b2a394bc0d86c4b895c9')
        result=build_e1_forecast(rows,digest,1152,source_kind='SYNTHETIC_CONTRACT_TEST')
        self.assertEqual(sha(canonical_bytes(result)),
                         '8a7f917ac8deb9307d31100e7cd811f87897b563d907d5ab5eab911708545eb9')
        self.assertEqual(result['MAIN']['top'],[1,8,2,5,7,4,6])
        self.assertEqual(result['POWERBALL']['top'],1)

    def test_ratified_r2_5_5_synthetic_identity_goldens(self):
        """Distinct from the later standalone-runner synthetic golden pair."""
        from E_001.e1_historical_appearance_frequency import (
            candidate_forecast, training_prefix, training_sha256, tie_digest)
        fixture = json.loads((ROOT/'tests'/'p3_e1_synthetic_v0_3.json').read_text())
        self.assertEqual(fixture['target'], 1152)
        expected = fixture['ratified_identity_golden_vectors_v0_3']
        values = {
            'training_view_sha256': 'df21871f8067e5405b4fdb1eec50c65dddbaa35958872bad3230d3c10a791fd4',
            'tie_main_label_3_sha256': '7ce5ab1bae014adf61f1f02dd152d4b500cb405b65cb3886cdcee8dd9e2c9932',
            'canonical_forecast_sha256': '7b43d659d611791deb14d106a72984f153d9f79cc63b3d25000365de4c811d1e',
        }
        for key, value in values.items():
            self.assertEqual(expected[key], value, f'ratified fixture value drift: {key}')
        rows = fixture['rows']  # Synthetic historical prefix, not target outcome.
        digest = training_sha256(training_prefix(rows, fixture['target']))
        self.assertEqual(digest, values['training_view_sha256'])
        self.assertEqual(tie_digest(digest, fixture['target'], 'MAIN', 3),
                         values['tie_main_label_3_sha256'])
        forecast = candidate_forecast(rows, fixture['target'])
        self.assertEqual(hashlib.sha256(canonical_bytes(forecast)).hexdigest(),
                         values['canonical_forecast_sha256'])
        self.assertEqual(forecast['training_view_sha256'], digest)
        self.assertEqual(forecast['MAIN']['top'], expected['main_top'])
        self.assertEqual(forecast['MAIN']['worst'], expected['main_worst'])
        self.assertEqual(forecast['POWERBALL']['top'], expected['pb_top'])
        self.assertEqual(forecast['POWERBALL']['worst'], expected['pb_worst'])

    def test_t05_complete_drawview_is_suffix_independent_for_every_kind(self):
        """Re-pin changed N+ rows; compare ALL method-facing slots, array bytes and digest.

        Synthetic full-length development stand-ins make N the last authorised
        development target for each game. The entire target+later region is
        deliberately invalid binary; its columns must never be decoded.
        """
        from collections.abc import Mapping

        self.assertNotIn('master_sha256', inspect.getsource(DrawView))
        self.assertNotIn('master_sha256', DrawView.__slots__)

        def source_hashes(folder, game):
            return frozenset(hashlib.sha256((folder/name).read_bytes()).hexdigest()
                             for name in (f'{game}_results_master.csv',
                                          f'{game}_results_master_ledger.csv',
                                          f'{game}_results_master_init_verification.json'))

        def method_snapshot(view, forbidden_hashes):
            # Exhaustive slot inventory: adding any future method-facing field
            # automatically includes it in this comparison and leakage check.
            result = []
            for field in DrawView.__slots__:
                value = getattr(view, field)
                if isinstance(value, np.ndarray):
                    self.assertIs(type(value.base), bytes)
                    self.assertEqual(len(value.base), value.nbytes)
                    self.assertFalse(value.flags.writeable)
                    item = ('array', str(value.dtype), value.shape,
                            value.tobytes(order='C'))
                elif isinstance(value, Mapping):
                    item = ('mapping', tuple(sorted(value.items())))
                else:
                    item = ('scalar', value)
                result.append((field, item))
                # No master, ledger or INIT-file SHA can be carried as any
                # string value in any DrawView slot (including nested metadata).
                def assert_no_source_fingerprint(obj):
                    if isinstance(obj, str):
                        for h in forbidden_hashes:
                            self.assertNotIn(h, obj, f'{field} leaked an orchestration hash')
                    elif isinstance(obj, Mapping):
                        for key, entry in obj.items():
                            assert_no_source_fingerprint(key)
                            assert_no_source_fingerprint(entry)
                    elif isinstance(obj, (tuple, list)):
                        for entry in obj:
                            assert_no_source_fingerprint(entry)
                assert_no_source_fingerprint(value)
            return tuple(result), view.e1_view_digest(), view.simple_rows()

        for game, last_target, prefix_count in (
                ('POWERBALL', 1576, 432), ('OZLOTTO', 1693, 219)):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                a, target = fake_root(root, game=game, size=prefix_count,
                                      corrupt_suffix=b'\xffTARGET_A',
                                      later_suffix=b'AFTER_N_A,\xff')
                self.assertEqual(target, last_target)
                folder = root/'source_data'
                before_hashes = source_hashes(folder, game)
                self.assertIn(a, before_hashes)
                snapshots_a = {}
                for kind in ('UNORDERED_SET', 'OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC'):
                    for dates in (False, True):
                        spec = pin(game, target, variant='SYNTHETIC_DIAGNOSTIC',
                                   kind=kind, dates=dates, sha=a)
                        va = load_pinned_draw_view(repo_root=root, run_manifest=spec)
                        snapshots_a[kind, dates] = method_snapshot(va, before_hashes)
                # Change the *target* and the *later* rows, then re-pin both
                # orchestration-side records to the new whole-file identity.
                b, target_b = fake_root(root, game=game, size=prefix_count,
                                        corrupt_suffix=b'\xffTARGET_B_DIFFERENT',
                                        later_suffix=b'AFTER_N_B,\x00changed')
                self.assertEqual(target_b, target)
                after_hashes = source_hashes(folder, game)
                self.assertNotEqual(a, b)
                self.assertTrue(before_hashes.isdisjoint(after_hashes))
                for kind in ('UNORDERED_SET', 'OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC'):
                    for dates in (False, True):
                        with self.subTest(game=game, kind=kind, dates=dates):
                            spec = pin(game, target, variant='SYNTHETIC_DIAGNOSTIC',
                                       kind=kind, dates=dates, sha=b)
                            vb = load_pinned_draw_view(repo_root=root, run_manifest=spec)
                            self.assertEqual(method_snapshot(vb, before_hashes | after_hashes),
                                             snapshots_a[kind, dates])
                            self.assertFalse(hasattr(vb, 'master_sha256'))
                            if kind == 'UNORDERED_SET':
                                self.assertIsNone(vb.order_evidence)
                            else:
                                self.assertEqual(dict(vb.order_evidence), {
                                    'record': f'{game}_results_master_init_verification.json',
                                    'status': 'OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION'})

    def test_dates_opt_in_schema_digest_and_order_evidence(self):
        for kind in ('UNORDERED_SET','OPERATOR_DRAWN_ORDER','PAIRED_DIAGNOSTIC'):
            for dates in (False,True):
                with self.subTest(kind=kind,dates=dates):
                    m=pin('OZLOTTO',1483,variant='SYNTHETIC_DIAGNOSTIC',kind=kind,dates=dates)
                    v=load_pinned_draw_view(repo_root=ROOT,run_manifest=m)
                    self.assertEqual(v.main.dtype,np.dtype('int64'))
                    self.assertEqual(v.draw_number.dtype,np.dtype('int64'))
                    self.assertEqual((v.main[0]*47).dtype,np.dtype('int64'))
                    self.assertEqual(int(_owned([47],np.int64)[0]*47),2209)
                    self.assertEqual(v.draw_date is not None,dates)
                    arrays=[v.draw_number,v.main,v.draw_date,v.drawn_main]
                    for arr in arrays:
                        if arr is None:continue
                        self.assertEqual(type(arr.base),bytes)
                        self.assertEqual(len(arr.base),arr.nbytes)
                        self.assertFalse(arr.flags.writeable)
                    self.assertEqual(v.order_verification_status,
                                     'OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION')
                    if kind != 'UNORDERED_SET':
                        self.assertEqual(dict(v.order_evidence), {
                            'record': 'OZLOTTO_results_master_init_verification.json',
                            'status': 'OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION'})
                        with self.assertRaises(TypeError):
                            v.order_evidence['record']='tampered'
                    else:
                        self.assertIsNone(v.order_evidence)
                    if kind=='PAIRED_DIAGNOSTIC':
                        self.assertEqual(len(v.simple_rows()),9)  # no double-count
                        self.assertIn('drawn_main',v.simple_rows()[0])
                    with self.assertRaises(AttributeError):v.main=np.zeros(1)
                    if dates:
                        self.assertIn('date',v.simple_rows()[0])
        d0=load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('OZLOTTO',1483,dates=False))
        d1=load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('OZLOTTO',1483,dates=True))
        self.assertNotEqual(d0.e1_view_digest(),d1.e1_view_digest())

    def test_poisoned_suffix_is_never_decoded_or_parsed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            a,target=fake_root(root,corrupt_suffix=b'\xffINVALID,\xff')
            va=load_pinned_draw_view(repo_root=root,run_manifest=pin('OZLOTTO',target,sha=a))
            self.assertEqual(len(va.draw_number),9)
            self.assertNotIn('FAKE_AFTER_TARGET',str(va.simple_rows()))
            self.assertEqual(type(va.main.base),bytes)
            # Change ONLY raw suffix; recompute test-only pin / ledger/record.
            b,_=fake_root(root,corrupt_suffix=b'corrupted,\xffOTHER_AFTER_TARGET')
            vb=load_pinned_draw_view(repo_root=root,run_manifest=pin('OZLOTTO',target,sha=b))
            self.assertEqual(va.simple_rows(),vb.simple_rows())
            self.assertNotEqual(a,b)
            # Whole-master SHA changes, but the prefix predictor digest MUST
            # NOT depend on a future-row-dependent whole-file hash.
            self.assertEqual(va.e1_view_digest(),vb.e1_view_digest())
            self.assertTrue(max(vb.draw_number)<target)

    def test_reject_unpinned_missing_and_replaced_master(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);sha,target=fake_root(root)
            normal=pin('OZLOTTO',target,sha=sha)
            self.assertEqual(len(load_pinned_draw_view(repo_root=root,run_manifest=normal).draw_number),9)
            for changed in (dict(master_sha256='0'*64),dict(ledger_version=2),
                            dict(master_file='../other.csv'),dict(game_id='POWERBALL'),
                            dict(draw_number=1694),dict(method_id='E_0'),
                            dict(view_kind='SECRETS'),dict(include_dates='true')):
                with self.subTest(changed=changed),self.assertRaises(ValueError):
                    load_pinned_draw_view(repo_root=root,run_manifest={**normal,**changed})
            master=root/'source_data'/'OZLOTTO_results_master.csv'
            master.write_bytes(master.read_bytes()+b'extra')
            with self.assertRaisesRegex(ValueError,'SHA-256'):
                load_pinned_draw_view(repo_root=root,run_manifest=normal)
            master.unlink()
            with self.assertRaises(ValueError):load_pinned_draw_view(repo_root=root,run_manifest=normal)

    def test_reject_symlinks_and_hardlinks_and_dateload_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);sha,target=fake_root(root,date_shift=2)
            normal=pin('OZLOTTO',target,sha=sha)
            self.assertEqual(len(load_pinned_draw_view(repo_root=root,run_manifest=normal).main),9)
            with self.assertRaisesRegex(ValueError,'date-dependent'):
                load_pinned_draw_view(repo_root=root,run_manifest={**normal,'include_dates':True})
            p=root/'source_data'/'OZLOTTO_results_master.csv'
            original=p.read_bytes()
            # TH-1: symlink and hardlink refusal are separate subtests, so that a platform
            # which cannot create one kind of link (Windows without the symlink privilege,
            # WinError 1314) still tests the other. A link that cannot be created is a skip,
            # never a pass.
            with self.subTest(link='symlink'):
                (root/'original.csv').write_bytes(original)
                p.unlink()
                try:
                    try:
                        p.symlink_to(root/'original.csv')
                    except (OSError,NotImplementedError):
                        self.skipTest('platform does not permit creating symlinks; symlink refusal not tested here')
                    with self.assertRaises(ValueError):load_pinned_draw_view(repo_root=root,run_manifest=normal)
                finally:
                    if p.is_symlink() or p.exists(): p.unlink()
                    p.write_bytes(original)
            with self.subTest(link='hardlink'):
                sibling=root/'linked.csv'
                try:
                    os.link(p,sibling)
                except (OSError,NotImplementedError):
                    self.skipTest('hardlinks unsupported by test filesystem')
                with self.assertRaisesRegex(ValueError,'hardlinked'):
                    load_pinned_draw_view(repo_root=root,run_manifest=normal)

    def test_only_legacy_e1_allowed_at_boundary(self):
        for change in (dict(method_id='E_2'),dict(variant_id='SYNTHETIC'),
                       dict(view_kind='PAIRED_DIAGNOSTIC'),dict(include_dates=True)):
            with self.subTest(change=change),self.assertRaises(ValueError):
                load_pinned_draw_view(repo_root=ROOT,run_manifest={**pin('POWERBALL',1577),**change})
        for bad in (1578,1586,1600):
            with self.assertRaises(ValueError):load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('POWERBALL',bad))
        with self.assertRaises(ValueError):load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('OZLOTTO',1694))
        # Actual accepted Oz development view supplies 47, so prove the
        # 47*47=2209 invariant on an exported int64 SCIENTIFIC view array.
        oz=load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('OZLOTTO',1693))
        self.assertGreater(int(np.count_nonzero(oz.main==47)),0)
        value=oz.main[oz.main==47][0]
        self.assertEqual(value.dtype,np.dtype('int64'))
        self.assertEqual(int(value*value),2209)

if __name__=='__main__':unittest.main()
