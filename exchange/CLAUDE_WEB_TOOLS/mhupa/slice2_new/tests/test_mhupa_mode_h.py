"""MHUP-A (design v0.1r5 sections 4.1, 4.2, 5.1-5.4, 6.7, Appendix H, Appendix L items L-H, L-H1-L-H3, L-U1, L-U2,
L-U4): the Mode H study from the manifest to the seal, on a temporary project holding an INVENTED master, a copy of
the code closure and an INVENTED Python environment. OFFLINE. A small cohort (E_6 and E_7, six variants; the cohort
is restricted in every caller alike) keeps the 60-run batch short. No real draw is read; nothing in the repository
is written.
"""
from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import json
import shutil
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

import mhupa_slice2_fixtures as X
import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.contract_dispatch as CD
import _common.walk_forward as WF
from _common import closure as CL
from _common import master_versions as MV
from _common import owner_records as OR
from _common.contract_records import canonical, record_digest, sha256_hex
from _common.game_profiles import POWERBALL
from evaluation import mode_h as MH
from evaluation import outcome_reader as OREAD
from evaluation import report as RP
from evaluation import report_writer as RW
from evaluation import seed_policies as SP
from evaluation import n1 as N1
from evaluation import divisions as DV

G = 'POWERBALL'
P = POWERBALL


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class Stub:
    """An adapter whose compute misbehaves at one target and otherwise is the real method's."""

    def __init__(self, real, target, exc):
        self.real, self.target, self.exc = real, target, exc

    def compute(self, task, view):
        if task.target_draw_number == self.target:
            raise self.exc
        return self.real.compute(task, view)

    def verify(self, *a):
        return self.real.verify(*a)


class Base(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.tmp = Path(self._td.name)
        self.proj = X.project(self.tmp, P)
        self.env = X.fake_environment(self.tmp)
        self.adapters = X.small_adapters()
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(X.patched(self.proj, self.env))
        self.up = X.updater_module()

    def tearDown(self):
        self.stack.close()
        self._td.cleanup()

    # --- helpers
    def rows(self):
        return MV.load_verified_source(self.proj, G)[1]

    def ledger_dicts(self):
        return self.up.Store(self.proj, G).ledger_rows()

    def search_rows(self, row_type=None):
        rows = RP.search_rows(G)
        return [r for r in rows if row_type is None or r['row_type'] == row_type]

    def markers(self, batch_id):
        return OR.lifecycle_markers_present(self.proj, G, batch_id)

    def run_folders(self):
        root = WF.roots('MODE_H_BATCH')['runs']
        return sorted(p for p in root.glob('*/*/*/*') if p.is_dir()) if root.exists() else []

    def tickets(self, plan):
        return OR.tickets(WF._attempts_path(plan), scope_kind='MODE_H_BATCH', scope_id=plan['batch_id'], game_id=G)

    def open_study(self):
        man = MH.manifest(G)
        opening = MH.open_holdout(G, OR.OPENING_STATEMENT)
        return man, opening

    def score(self, **kw):
        policy = SP.approved_policy()
        a = dict(echo=None, n1_runner=N1.runner(policy), seed_line=f"policy {policy['policy_id']}, R = {N1.R}",
                 n1_policies_on_file=SP.count_policies(), environment={})
        a.update(kw)
        return MH.score(G, **a)

    def hand_bound_run(self, plan, mem, target):
        """A request bound to the plan, issued by hand (no ticket): the dispatch gate decides."""
        req = WF.request_for(plan, mem, target, CP.new_run_id())
        before = len(self.run_folders())
        with self.assertRaises((CR.RunRefused, CD.DispatchRefused)) as cm:
            CR.run_contract_method(req, compute=self.adapters[mem['method_id']].compute,
                                   verify=self.adapters[mem['method_id']].verify, repo_root=self.proj,
                                   run_root=WF.roots('MODE_H_BATCH')['runs'])
        self.assertEqual(len(self.run_folders()), before, 'a refused hand-bound run left a record')
        return cm.exception.text


# ====================================================================== the manifest and the opening record

class ManifestAndOpening(Base):

    def test_manifest_fields_and_refusals(self):
        self.assertIsNone(OR.study_manifest(self.proj, G))
        rec = MH.manifest(G)
        self.assertEqual(rec['schema'], OR.STUDY_MANIFEST_SCHEMA)
        self.assertEqual(rec['targets'], list(range(P.holdout_first, P.holdout_last + 1)))
        self.assertEqual(sorted(rec['exposure']), ['1585', '1586'])
        self.assertEqual(rec['exposure']['1585'], {'record': OR.EXPOSURE_RECORD, 'decision': 'HX-1'})
        self.assertEqual([m['method_id'] for m in rec['cohort']], ['E_6'] * 3 + ['E_7'] * 3)
        self.assertEqual(rec['families'], ['MODEH_POWERBALL_MR7_MAIN_V1', 'MODEH_POWERBALL_MR7_PB_V1'])
        self.assertEqual((rec['freeze_version'], rec['freeze_master_sha256']), (1, self.rows()[0].master_sha256))
        self.assertEqual(rec['closure'], CL.closure_inventory(self.proj))
        self.assertEqual(rec['environment']['digest'], CL.environment_inventory(self.env)['digest'])
        self.assertIn('src/evaluation/mode_h.py', rec['closure']['files'])
        self.assertIn('Run_Evaluation.bat', rec['closure']['files'])
        self.assertIn('requirements.txt', rec['closure']['files'])
        self.assertTrue(all(not k.startswith(('tests/', 'doc/', 'source_data/', 'results/')) for k in rec['closure']['files']))
        self.assertEqual(rec['excluded'], list(CL.EXCLUDED))
        self.assertTrue(any(m['method_id'] == 'E_2' for m in rec['not_runnable']))      # marked, never suppressed
        path = OR.study_manifest_path(self.proj, G)
        self.assertEqual(path.read_bytes(), canonical(rec))
        self.assertEqual(OR.validate_study_manifest(rec, G), rec)
        log = self.search_rows('MODE_H_STUDY_MANIFEST')
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]['plan_digest'], sha(path.read_bytes()))
        with self.assertRaises(MH.ModeHRefused):                                   # create-only
            MH.manifest(G)
        self.assertEqual(len(self.search_rows()), 1)

    def test_manifest_refuses_a_grown_ledger_an_orphan_and_sourceless_bytecode(self):
        X.first_update(self.proj, P)                                               # the ledger already past v_f
        with self.assertRaises(MH.ModeHRefused) as cm:
            MH.manifest(G)
        self.assertIn('before the holdout is opened it must end at 1576', str(cm.exception))
        # a fresh project: an orphan under site-packages refuses the manifest
        self.stack.close(); self._td.cleanup(); self.setUp()
        orphan = self.env.site_packages / 'stray.pth'
        orphan.write_text('x')
        with self.assertRaises(MH.ModeHRefused) as cm:
            MH.manifest(G)
        self.assertIn('no RECORD lists', str(cm.exception))
        orphan.unlink()
        # a sourceless json.pyc planted in src/methods/ refuses the manifest (design 4.1)
        planted = self.proj / 'src' / 'methods' / 'json.pyc'
        planted.write_bytes(b'\x00sentinel')
        with self.assertRaises(MH.ModeHRefused) as cm:
            MH.manifest(G)
        self.assertIn('sourceless byte-code under src/: src/methods/json.pyc', str(cm.exception))
        planted.unlink()
        # a cache under __pycache__/ is irrelevant: it never enters the closure
        cache = self.proj / 'src' / 'methods' / '__pycache__'
        cache.mkdir()
        (cache / 'json.cpython-399.pyc').write_bytes(b'\x00sentinel')
        rec = MH.manifest(G)
        self.assertFalse(any('__pycache__' in k for k in rec['closure']['files']))
        self.assertFalse((self.proj / 'results' / 'real' / 'holdout' / G / 'MODE_H_STUDY_MANIFEST_V1.json').is_symlink())
        self.assertIsNone(OR.opening_record(self.proj, G))

    def test_opening_record_and_the_updater_agree(self):
        with self.assertRaises(MH.ModeHRefused):                                   # no manifest yet
            MH.open_holdout(G, OR.OPENING_STATEMENT)
        man = MH.manifest(G)
        with self.assertRaises(MH.ModeHRefused):                                   # the sentence, exactly
            MH.open_holdout(G, 'I open the holdout.')
        self.assertFalse(self.up.holdout_opened(self.proj, G))
        rec = MH.open_holdout(G, OR.OPENING_STATEMENT)
        self.assertEqual(rec['schema'], 'HOLDOUT_OPENED_V1')
        self.assertEqual(rec['study_manifest_sha256'], sha(OR.study_manifest_path(self.proj, G).read_bytes()))
        self.assertEqual((rec['freeze_version'], rec['freeze_master_sha256']), (man['freeze_version'], man['freeze_master_sha256']))
        self.assertEqual(OR.opening_record(self.proj, G), rec)
        # the updater v0.2 reads the same record with its own checks, and its ledger grammar is the fixture's
        self.assertTrue(self.up.holdout_opened(self.proj, G))
        self.assertEqual(tuple(self.up.LEDGER_COLUMNS), tuple(MV.LEDGER_COLUMNS))
        self.assertEqual(self.up.freeze_state(self.proj, G, self.ledger_dicts()), 'FIRST_UPDATE')
        self.assertFalse(self.up.mode_h_sealed(self.proj, G))
        self.assertEqual(len(self.search_rows('HOLDOUT_OPENED')), 1)
        with self.assertRaises(MH.ModeHRefused):                                   # permanent
            MH.open_holdout(G, OR.OPENING_STATEMENT)
        with self.assertRaises(MH.ModeHRefused):                                   # the manifest after the opening
            MH.manifest(G)
        # the opening record authorises no run: a Mode H-bound request without a plan is refused
        mem = man['cohort'][0]
        fake_plan = {'batch_id': 'wf-' + '0' * 32, 'game_id': G, 'schema': WF.MODE_H_PLAN_SCHEMA}
        req = WF.request_for({**fake_plan, 'observation_view': WF.VIEW, 'include_dates': False, 'run_mode': 'REAL_HOLDOUT',
                              'product_kind': 'FORECAST', 'master_file': f'{G}_results_master.csv', 'ledger_version': 1,
                              'master_sha256': man['freeze_master_sha256'], 'targets': man['targets'], 'cohort': man['cohort'],
                              'study_manifest_sha256': rec['study_manifest_sha256'], 'window_first': 1577, 'window_last': 1586},
                             mem, 1577, CP.new_run_id())
        with self.assertRaises((CR.RunRefused, CD.DispatchRefused)):
            CR.run_contract_method(req, compute=self.adapters['E_6'].compute, verify=self.adapters['E_6'].verify,
                                   repo_root=self.proj, run_root=WF.roots('MODE_H_BATCH')['runs'])
        self.assertEqual(self.run_folders(), [])

    def test_the_cohort_must_be_exactly_the_released_set(self):
        """EX_148 B03 (b), (c), (d): the full cohort (no small-cohort restriction), against the validated release records."""
        self.stack.close()
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(X.patched(self.proj, self.env, small_cohort=False))
        # (b) E_1 revision 3 is SUPPORTED in the registry, but its release record (written by the install) is absent
        with self.assertRaises(MH.ModeHRefused) as cm:
            MH.manifest(G)
        self.assertIn('SUPPORTED in the registry but not released: E_1 revision 3 FULL_HISTORY_RAW_COUNTS_V1', str(cm.exception))
        self.assertIsNone(OR.study_manifest(self.proj, G))
        self.assertEqual(self.search_rows(), [])
        # (c) a conflicting release record (a second record naming baseline entries) refuses
        rel = X.write_e1r3_release(self.proj)
        folder = rel.parent
        dup = folder / 'RELEASE_DUP_V1.json'
        base = json.loads((folder / 'RELEASE_BASELINE_20261031_V1.json').read_bytes())
        dup.write_bytes(X.RR.canonical(dict(base, package='DUP', install_record_sha256=json.loads(rel.read_bytes())['install_record_sha256'],
                                            released_utc='2026-11-20T10:00:00.000000Z', local_date='2026-11-20')))
        with self.assertRaises(MH.ModeHRefused) as cm:
            MH.manifest(G)
        self.assertIn('the release records refuse', str(cm.exception))
        dup.unlink()
        # a malformed release record refuses too
        bad = folder / 'RELEASE_BAD_V1.json'
        bad.write_bytes(b'{"schema": "RELEASE_RECORD_V1"}')
        with self.assertRaises(MH.ModeHRefused) as cm:
            MH.manifest(G)
        self.assertIn('the release records refuse', str(cm.exception))
        bad.unlink()
        # a released variant missing from the runnable set (its registry entry made unsupported by a newer entry)
        # is reported from the other side: released set and cohort differ
        # the other direction: a released variant that the registry's runnable set lacks refuses too
        real_cohort = WF.cohort
        with mock.patch.object(WF, 'cohort', lambda g, a: (real_cohort(g, a)[0][1:], [])):
            with self.assertRaises(MH.ModeHRefused) as cm:
                MH.manifest(G)
        self.assertIn('released but not in the registry\'s runnable set', str(cm.exception))
        # (d) with MHUP-A's own release record present: the 39 baseline variants and E_1 revision 3, exactly
        rec = MH.manifest(G)
        self.assertEqual(len(rec['cohort']), 40)
        self.assertEqual({(m['method_id'], m['method_revision']) for m in rec['cohort'] if m['method_id'] == 'E_1'},
                         {('E_1', '3')})
        released = {k for k in X.RR.released_variants(self.proj) if k[0] == G}
        self.assertEqual(released, {(G, m['method_id'], m['method_revision'], m['variant_id']) for m in rec['cohort']})

    def test_the_cohort_refuses_a_released_variant_the_registry_no_longer_runs(self):
        """EX_148 B03 (a) at the manifest: a newer registry entry supersedes a released revision with no retires item;
        the old revision drops out of the released set and the new one has no release record: refused."""
        reg = self.proj / 'src' / 'methods' / '_common' / 'contract_data' / 'registry' / G / 'E_6' / 'BETA_BERNOULLI_FULL_MEMORY_V1'
        e1 = json.loads((reg / 'entry_0001.json').read_bytes())
        e2 = dict(e1, entry_sequence=2, method_revision='2', previous_entry_digest='0' * 64)
        (reg / 'entry_0002.json').write_bytes(canonical(e2))
        released = X.RR.released_variants(self.proj)
        self.assertNotIn((G, 'E_6', '1', 'BETA_BERNOULLI_FULL_MEMORY_V1'), released)
        self.assertNotIn((G, 'E_6', '2', 'BETA_BERNOULLI_FULL_MEMORY_V1'), released)
        self.assertIn((G, 'E_6', '1', 'BETA_BERNOULLI_DECAY_74_75_V1'), released)
        with self.assertRaises(MH.ModeHRefused) as cm:
            with mock.patch.object(WF, 'cohort', lambda g, a: ([m for m in X._small_cohort(g, a)[0]], [])):
                MH.manifest(G)
        self.assertIn('not released: E_6 revision 1 BETA_BERNOULLI_FULL_MEMORY_V1', str(cm.exception))

    def test_open_refuses_after_a_ledger_row_beyond_the_frozen_version(self):
        MH.manifest(G)
        X.first_update(self.proj, P)
        with self.assertRaises(MH.ModeHRefused) as cm:
            MH.open_holdout(G, OR.OPENING_STATEMENT)
        self.assertIn('not the version the study manifest froze', str(cm.exception))
        self.assertIsNone(OR.opening_record(self.proj, G))


# ====================================================================== the plan: the frozen study and its refusals

class PlanRefusals(Base):

    def setUp(self):
        super().setUp()
        self.man, self.opening = self.open_study()

    def assert_plan_refused(self, fragment: str):
        with self.assertRaises(WF.BatchRefused) as cm:
            WF.make_mode_h_plan(G, self.adapters)
        self.assertIn(fragment, str(cm.exception))
        self.assertIsNone(OR.batch_id_record(self.proj, G))
        self.assertEqual(self.search_rows('MODE_H_BATCH'), [])

    def test_plan_needs_the_complete_first_update(self):
        self.assert_plan_refused('the ledger\'s last row is version 1; the admitted version is 2')
        X.first_update(self.proj, P, upto=P.holdout_last - 1)                         # one draw short
        self.assert_plan_refused('before the holdout\'s last draw 1586')
        with self.assertRaises(self.up.Refused):                                      # and the updater refuses now too
            self.up.freeze_state(self.proj, G, self.ledger_dicts())

    def test_plan_refuses_a_changed_closure_or_environment_naming_the_first_difference(self):
        X.first_update(self.proj, P)
        target = self.proj / 'src' / 'evaluation' / 'mode_h.py'
        original = target.read_bytes()
        target.write_bytes(original + b'# one more byte\n')
        self.assert_plan_refused('closure: changed src/evaluation/mode_h.py')
        target.write_bytes(original)
        extra = self.proj / 'src' / 'methods' / 'Extra_Method.py'
        extra.write_text('x = 1\n')
        self.assert_plan_refused('closure: added src/methods/Extra_Method.py')
        extra.unlink()
        bat = self.proj / 'Run_Evaluation.bat'
        bat_bytes = bat.read_bytes()
        bat.unlink()
        self.assert_plan_refused('closure: removed Run_Evaluation.bat')
        bat.write_bytes(bat_bytes)
        # L-U2: one byte changed in an installed distribution's file under the same version
        core = self.env.site_packages / 'fakepkg' / 'core.py'
        core_bytes = core.read_bytes()
        core.write_bytes(core_bytes.replace(b'return 2', b'return 3'))
        self.assert_plan_refused('fakepkg/core.py differs from its RECORD hash')
        core.write_bytes(core_bytes)
        # L-U4: an altered interpreter digest, an added unlisted site-packages file, a new distribution
        interp = self.env.base_prefix / 'bin' / 'python3.99'
        interp_bytes = interp.read_bytes()
        interp.write_bytes(interp_bytes + b'\n')
        self.assert_plan_refused('environment interpreter: changed bin/python3.99')
        interp.write_bytes(interp_bytes)
        stray = self.env.site_packages / 'stray.pth'
        stray.write_text('x')
        self.assert_plan_refused('no RECORD lists')
        stray.unlink()
        info = self.env.site_packages / 'other-2.0.dist-info'
        info.mkdir()
        (info / 'RECORD').write_text('other-2.0.dist-info/RECORD,,\n')
        self.assert_plan_refused('environment distributions: added other-2.0.dist-info')
        shutil.rmtree(info)
        cfg = self.env.venv_prefix / 'pyvenv.cfg'
        cfg_text = cfg.read_text()
        cfg.write_text(cfg_text.replace('3.99.0', '3.99.1'))
        self.assert_plan_refused('environment: pyvenv_cfg differs')
        cfg.write_text(cfg_text)
        # a planted cache under site-packages/__pycache__/ changes nothing; a sourceless .pyc beside it refuses
        cache = self.env.site_packages / 'fakepkg' / '__pycache__'
        cache.mkdir()
        (cache / 'core.cpython-399.pyc').write_bytes(b'\x00sentinel')
        plan = WF.make_mode_h_plan(G, self.adapters)
        self.assertEqual(plan['ledger_version'], 2)

    def test_plan_is_frozen_from_the_manifest_once(self):
        rows = X.first_update(self.proj, P)
        plan = WF.make_mode_h_plan(G, self.adapters)
        self.assertEqual(plan['schema'], OR.MODE_H_PLAN_SCHEMA)
        self.assertEqual((plan['window_first'], plan['window_last'], plan['targets']), (1577, 1586, self.man['targets']))
        self.assertEqual(plan['run_mode'], 'REAL_HOLDOUT')
        self.assertEqual((plan['ledger_version'], plan['master_sha256']), (2, rows[1]['master_sha256']))
        self.assertEqual(plan['cohort'], self.man['cohort'])
        self.assertEqual(plan['study_manifest_sha256'], self.opening['study_manifest_sha256'])
        rec = OR.batch_id_record(self.proj, G)
        self.assertEqual((rec['batch_id'], rec['plan_digest']), (plan['batch_id'], record_digest(plan)))
        self.assertEqual(WF.load_plan(G, plan['batch_id']), plan)
        self.assertEqual(len(self.search_rows('MODE_H_BATCH')), 1)
        with self.assertRaises(WF.BatchRefused) as cm:                                 # the one plan
            WF.make_mode_h_plan(G, self.adapters)
        self.assertIn('already has its one Mode H plan', str(cm.exception))
        # a development plan over holdout targets is still refused (the WF kind stops below the holdout)
        with self.assertRaises(WF.BatchRefused):
            WF.make_plan(G, 1577, 1586, self.adapters)
        # the cohort must equal the manifest's: a method withdrawn from the adapters at plan time refuses
        self.stack.close(); self._td.cleanup(); self.setUp()
        X.first_update(self.proj, P)
        with self.assertRaises(WF.BatchRefused) as cm:
            WF.make_mode_h_plan(G, {'E_6': self.adapters['E_6']})
        self.assertIn('differs from the study manifest', str(cm.exception))

    def test_an_extra_ledger_row_needs_a_study_version_advance(self):
        X.first_update(self.proj, P)
        import mhupa_fixtures as F
        F.grow_master(self.proj, P, [list(range(P.holdout_first, P.holdout_last + 1)), None])    # v3: a NO_CHANGE row
        self.assert_plan_refused('the ledger\'s last row is version 3; the admitted version is 2')
        with self.assertRaises(MH.ModeHRefused):                                      # the sentence, exactly
            MH.advance(G, 'I advance.')
        adv = MH.advance(G, OR.ADVANCE_STATEMENT)
        self.assertEqual((adv['admitted_version_before'], adv['admitted_version_after']), (2, 3))
        self.assertEqual([r['version'] for r in adv['rows_beyond_admitted']], [3])
        self.assertEqual(len(self.search_rows('STUDY_VERSION_ADVANCE')), 1)
        with self.assertRaises(MH.ModeHRefused):                                      # create-only
            MH.advance(G, OR.ADVANCE_STATEMENT)
        # the advance does not reopen the updater's window
        with self.assertRaises(self.up.Refused) as cm:
            self.up.freeze_state(self.proj, G, self.ledger_dicts())
        self.assertIn('admitted version 3', str(cm.exception))
        # and a plan cannot be frozen after an advance (the plan is frozen at v_a); the study stays blocked
        self.assert_plan_refused('a study version advance exists before the plan')


# ====================================================================== the batch, the score and the seal

class Pipeline(Base):
    """One study from the opening record to the developed record, with the resume paths and the hand-bound runs."""

    def setUp(self):
        super().setUp()
        self.man, self.opening = self.open_study()
        X.first_update(self.proj, P)
        self.plan = WF.make_mode_h_plan(G, self.adapters)
        self.bid = self.plan['batch_id']
        self.out = []

    def run_batch(self, adapters=None):
        return WF.run_batch(G, self.bid, adapters or self.adapters, echo=self.out.append)

    def test_the_study(self):
        plan, bid = self.plan, self.bid
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))
        # ---- an interrupted run leaves an OPEN ticket; the resume closes it FAILED_TO_START and never reuses the id
        stub = dict(self.adapters, E_6=Stub(self.adapters['E_6'], 1579, KeyboardInterrupt()))
        self.assertEqual(self.run_batch(stub), 1)
        tk = self.tickets(plan)
        opens = [t for t in tk if t['kind'] == 'OPEN']
        dones = [t for t in tk if t['kind'] == 'DONE']
        self.assertEqual(len(opens), len(dones) + 1)
        interrupted = opens[-1]
        self.assertEqual((interrupted['method_id'], interrupted['target_draw_number']), ('E_6', 1579))
        self.assertEqual(self.markers(bid), [])
        # ---- a method failure at one target is DONE (CONTINUE class) and scored as missing
        failing = dict(self.adapters, E_7=Stub(self.adapters['E_7'], 1580, ValueError('synthetic failure')))
        self.assertEqual(self.run_batch(failing), 0)
        tk = self.tickets(plan)
        self.assertEqual([t['kind'] for t in tk if t['run_id'] == interrupted['run_id']], ['OPEN', 'FAILED_TO_START'])
        self.assertEqual(sum(t['kind'] == 'FAILED_TO_START' for t in tk), 1)
        done_pairs = {(t['method_id'], t['variant_id'], t['target_draw_number']) for t in tk if t['kind'] == 'DONE'}
        self.assertEqual(len(done_pairs), 60)
        failed = [t for t in tk if t['kind'] == 'DONE' and t['terminal_class'].startswith('RUNTIME_FAILURE')]
        self.assertEqual(sorted({t['method_id'] for t in failed}), ['E_7'])
        self.assertEqual({t['target_draw_number'] for t in failed}, {1580})
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE'])
        complete = OR.marker(self.proj, G, bid, 'BATCH_COMPLETE')
        self.assertEqual((complete['pairs'], complete['plan_digest']), (60, record_digest(plan)))
        states, bad = WF.pair_states(plan)
        self.assertEqual(set(states.values()), {'DONE'})
        self.assertEqual(bad, 0)
        folders = self.run_folders()
        self.assertEqual(len(folders), 61)                                        # 60 runs + the interrupted folder
        receipts = [json.loads((f / CP.FILES['forecast_receipt']).read_bytes()) for f in folders
                    if (f / CP.FILES['forecast_receipt']).exists()]
        self.assertEqual(len(receipts), 57)                                       # 60 - 3 failed E_7 pairs at 1580
        self.assertEqual({(r['ledger_version'], r['master_sha256']) for r in receipts}, {(2, plan['master_sha256'])})
        self.assertEqual({r['run_mode'] for r in receipts}, {'REAL_HOLDOUT'})
        st = WF.status(G, bid)
        self.assertEqual(st['lifecycle_markers'], ['BATCH_COMPLETE'])
        self.assertEqual(st['E_6 BETA_BERNOULLI_FULL_MEMORY_V1']['done'], 10)
        # ---- after BATCH_COMPLETE: a further run invocation and a hand-bound run are refused, no record
        self.assertEqual(self.run_batch(), 2)
        self.assertIn('lifecycle marker(s) present: BATCH_COMPLETE', self.out[-1])
        mem = plan['cohort'][0]
        self.assertIn('BATCH_CLOSED', self.hand_bound_run(plan, mem, 1577))
        # the updater: still refused for the game (opened, unsealed, ledger at v_a)
        with self.assertRaises(self.up.Refused):
            self.up.freeze_state(self.proj, G, self.ledger_dicts())
        # ---- a copy of the project for the uninterrupted attempt (the L-H2 oracle): same attempt id in both
        twin = self.tmp / 'twin'
        shutil.copytree(self.proj, twin)
        fixed = uuid.UUID(int=0x5eed)
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))      # not before SCORING_STARTED
        # ---- the score, interrupted: before the ledger (the outcome read fails), then after SCORE_COMPLETE
        with mock.patch.object(MH.uuid, 'uuid4', return_value=fixed), \
                mock.patch.object(OREAD, 'read_outcomes', side_effect=OSError('disk gone')):
            with self.assertRaises(OSError):
                self.score()
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE', 'SCORING_STARTED'])
        started = OR.marker(self.proj, G, bid, 'SCORING_STARTED')
        self.assertEqual(started['attempt_id'], 'mh-' + fixed.hex)
        self.assertEqual(started['roster_digest'], OR.roster_digest(self.proj, G, plan))
        self.assertEqual(len(self.search_rows('MODE_H_REPORT')), 1)
        folder = WF.roots('MODE_H_BATCH')['scores'] / G / bid / started['attempt_id']
        self.assertTrue((folder / 'scoring_plan.json').is_file())
        self.assertFalse((folder / MH.SCORE_LEDGER).exists())
        # the freeze-before-outcome rule now releases the plan's targets, and only those, to the reader
        self.assertTrue(OREAD.outcome_release_allowed(self.proj, G, 1577))
        self.assertTrue(OREAD.outcome_release_allowed(self.proj, G, 1586))
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1587))
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1576))
        self.assertIn('BATCH_CLOSED', self.hand_bound_run(plan, mem, 1577))             # during scoring: refused
        # resume: a crash right after SCORE_COMPLETE, before the report
        real_write_marker = OR.write_marker

        def crash_after_score_complete(root, game, b, name, rec):
            raw = real_write_marker(root, game, b, name, rec)
            if name == 'SCORE_COMPLETE':
                raise RuntimeError('power cut')
            return raw
        with mock.patch.object(OR, 'write_marker', crash_after_score_complete):
            with self.assertRaises(RuntimeError):
                self.score()
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE'])
        ledger_bytes = (folder / MH.SCORE_LEDGER).read_bytes()
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))      # after SCORE_COMPLETE: never again
        self.assertEqual(len(self.search_rows('MODE_H_REPORT')), 1)
        # resume: a crash after the report, before the seal; the finalisation reads no outcome (reader mocked to fail)
        def crash_before_seal(root, game, b, name, rec):
            if name == 'MODE_H_SEALED':
                raise RuntimeError('power cut again')
            return real_write_marker(root, game, b, name, rec)
        with mock.patch.object(OR, 'write_marker', crash_before_seal), \
                mock.patch.object(OREAD, 'read_outcomes', side_effect=AssertionError('an outcome was read')):
            with self.assertRaises(RuntimeError):
                self.score()
        base = RW.mode_h_base_name({'game_id': G, 'first': 1577, 'last': 1586, 'attempt_id': started['attempt_id']})
        self.assertEqual(base, f"mode_h_POWERBALL_1577-1586_{started['attempt_id']}")      # deterministic, attempt-bound
        report_folder = RP.roots()['reports'] / G
        report_txt = (report_folder / f'{base}.txt').read_bytes()
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE'])
        with mock.patch.object(OREAD, 'read_outcomes', side_effect=AssertionError('an outcome was read')):
            res = self.score()
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE', 'MODE_H_SEALED'])
        self.assertEqual(res['attempt_id'], started['attempt_id'])
        self.assertEqual((folder / MH.SCORE_LEDGER).read_bytes(), ledger_bytes)  # untouched by the resumes
        self.assertEqual((report_folder / f'{base}.txt').read_bytes(), report_txt)
        self.assertEqual(len(self.search_rows('MODE_H_REPORT')), 1)              # one row, one attempt
        self.assertEqual(len(list((WF.roots('MODE_H_BATCH')['scores'] / G / bid).iterdir())), 1)
        seal = OR.marker(self.proj, G, bid, 'MODE_H_SEALED')
        self.assertEqual(seal['score_ledger_sha256'], sha(ledger_bytes))
        self.assertEqual(seal['report_sha256'], sha(report_txt))
        # ---- the uninterrupted twin produces the same ledger and report bytes (L-H2)
        with X.patched(twin, self.env), mock.patch.object(MH.uuid, 'uuid4', return_value=fixed):
            res_twin = self.score()
        twin_folder = twin / folder.relative_to(self.proj)
        self.assertEqual((twin_folder / MH.SCORE_LEDGER).read_bytes(), ledger_bytes)
        for ext in ('txt', 'csv', 'json'):
            self.assertEqual((twin / report_folder.relative_to(self.proj) / f'{base}.{ext}').read_bytes(),
                             (report_folder / f'{base}.{ext}').read_bytes(), ext)
        self.assertEqual(res_twin['score_ledger_sha256'], res['score_ledger_sha256'])
        # ---- the ledger and the report
        scores, ranks = MH._ledger_lines(folder / MH.SCORE_LEDGER)
        self.assertEqual((len(scores), len(ranks)), (57 * 2, 57))                  # two readouts per valid cell
        self.assertEqual({s['exposure_flag']['decision'] for s in scores if s['draw_number'] in (1585, 1586)}, {'HX-1'})
        self.assertFalse(any('exposure_flag' in s for s in scores if s['draw_number'] < 1585))
        self.assertEqual({s['draw_number'] for s in scores}, set(range(1577, 1587)))
        text = report_txt.decode('ascii')
        self.assertIn('Evidence tier: HOLDOUT_MODE_H', text)
        self.assertIn('Exposure flags (information only', text)
        self.assertIn('draw 1585 HX-1', text)
        self.assertIn('no wall-clock field', text)
        self.assertIn('Admitted master version: 2 (the plan\'s frozen version v_a; no study version advance)', text)
        self.assertIsNone(json.loads((report_folder / f'{base}.json').read_bytes())['mode_h']['study_version_advance'])
        manifest_json = json.loads((report_folder / f'{base}.json').read_bytes())
        self.assertIsNone(manifest_json['generated_utc'])
        self.assertEqual(manifest_json['mode_h']['score_attempt_id'], started['attempt_id'])
        # the report is byte-deterministic from the ledger lines
        tracks = [(m, ro) for m in plan['cohort'] for ro in ('OWN_SET', 'RANKED')]  # noqa: F841  (count below)
        self.assertEqual(sorted(p.name for p in report_folder.iterdir()), sorted(f'{base}.{e}' for e in ('txt', 'csv', 'json')))
        # ---- after the seal: a second routine attempt, a hand-bound run and a run invocation are refused
        with self.assertRaises(MH.ModeHRefused) as cm:
            self.score()
        self.assertIn('sealed', str(cm.exception))
        self.assertIn('BATCH_CLOSED', self.hand_bound_run(plan, mem, 1577))
        self.assertEqual(self.run_batch(), 2)
        # the updater is free again for the game; the other game is untouched
        self.assertEqual(self.up.freeze_state(self.proj, G, self.ledger_dicts()), 'SEALED')
        self.assertTrue(self.up.mode_h_sealed(self.proj, G) and OR.mode_h_sealed(self.proj, G))
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))
        # ---- GOAL-1: the developed record, once, after the seal
        with self.assertRaises(MH.ModeHRefused):
            MH.declare_developed(G, 'developed')
        dev = MH.declare_developed(G, OR.DEVELOPED_STATEMENT)
        self.assertEqual(dev['mode_h_score_digest'], sha(ledger_bytes))
        self.assertEqual(dev['mode_h_score_attempt_id'], started['attempt_id'])
        self.assertEqual(OR.developed_record(self.proj, G), dev)
        with self.assertRaises(MH.ModeHRefused):
            MH.declare_developed(G, OR.DEVELOPED_STATEMENT)
        self.assertEqual(len(self.search_rows('DEVELOPED')), 1)
        # the search log: one row of each kind, in order
        kinds = [r['row_type'] for r in self.search_rows()]
        self.assertEqual(kinds, ['MODE_H_STUDY_MANIFEST', 'HOLDOUT_OPENED', 'MODE_H_BATCH', 'MODE_H_REPORT', 'DEVELOPED'])

    def test_scorer_refusals_before_and_during(self):
        plan, bid = self.plan, self.bid
        with self.assertRaises(MH.ModeHRefused) as cm:                                 # no BATCH_COMPLETE
            self.score()
        self.assertIn('no BATCH_COMPLETE marker', str(cm.exception))
        with self.assertRaises(MH.ModeHRefused):                                       # developed needs the seal
            MH.declare_developed(G, OR.DEVELOPED_STATEMENT)
        # a pair still pending after a complete pass is a STOP and never BATCH_COMPLETE (design 5.2: every planned
        # pair DONE); the pass here runs nothing and the records then still show one pair pending
        real_pending = WF.pending
        calls = []

        def pending_then_one(p):
            calls.append(1)
            return [] if len(calls) == 1 else real_pending(p)[:1]
        with mock.patch.object(WF, 'pending', pending_then_one):
            self.assertEqual(self.run_batch(), 1)
        self.assertIn('still pending after a complete pass', self.out[-1])
        self.assertEqual(self.markers(bid), [])
        self.assertEqual(self.run_batch(), 0)
        # a tampered report after SCORE_COMPLETE is refused, nothing written
        real_write_marker = OR.write_marker

        def crash_before_seal(root, game, b, name, rec):
            if name == 'MODE_H_SEALED':
                raise RuntimeError('power cut')
            return real_write_marker(root, game, b, name, rec)
        with mock.patch.object(OR, 'write_marker', crash_before_seal):
            with self.assertRaises(RuntimeError):
                self.score()
        started = OR.marker(self.proj, G, bid, 'SCORING_STARTED')
        base = RW.mode_h_base_name({'game_id': G, 'first': 1577, 'last': 1586, 'attempt_id': started['attempt_id']})
        report = RP.roots()['reports'] / G / f'{base}.txt'
        good = report.read_bytes()
        report.write_bytes(good + b'\n')
        with self.assertRaises(MH.ModeHRefused) as cm:
            self.score()
        self.assertIn('differs from the bytes rebuilt', str(cm.exception))
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE'])
        report.write_bytes(good)
        # a roster that differs from the one scoring started with (a DONE ticket forged for another run id)
        folder = WF.roots('MODE_H_BATCH')['scores'] / G / bid / started['attempt_id']
        tk_path = WF._attempts_path(plan)
        before = tk_path.read_bytes()
        forged = dict(next(t for t in self.tickets(plan) if t['kind'] == 'DONE'))
        forged['run_id'] = 'mg-' + 'f' * 32
        tk_path.write_bytes(before + canonical(forged))
        with self.assertRaises(MH.ModeHRefused) as cm:
            self.score()
        self.assertIn('roster', str(cm.exception))
        tk_path.write_bytes(before)
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))        # SCORE_COMPLETE stands
        res = self.score()
        self.assertEqual(self.markers(bid)[-1], 'MODE_H_SEALED')
        self.assertEqual(res['attempt_id'], started['attempt_id'])

    def test_an_advance_after_the_plan_moves_the_admitted_pin(self):
        import mhupa_fixtures as F
        plan, bid = self.plan, self.bid
        rows = F.grow_master(self.proj, P, [list(range(P.holdout_first, P.holdout_last + 1)), None])   # v3: a NO_CHANGE row
        self.assertEqual(self.run_batch(), 2)                                               # refused: last row is not v_a
        self.assertIn('the admitted version is 2', self.out[-1])
        self.assertEqual(self.run_folders(), [])
        # an advance record that does not name exactly the rows beyond v_a refuses every reader of the admitted version
        bad = {'schema': OR.ADVANCE_SCHEMA, 'game_id': G, 'study_manifest_sha256': self.opening['study_manifest_sha256'],
               'admitted_version_before': 2, 'admitted_version_after': 3, 'owner_statement': OR.ADVANCE_STATEMENT,
               'advanced_utc': '2026-11-20T10:00:00Z',
               'rows_beyond_admitted': [{'version': 3, 'action': 'UPDATE', 'master_sha256': 'd' * 64}]}
        adv_path = OR.advance_record_path(self.proj, G)
        OR.write_record(adv_path, bad)
        with self.assertRaises(OR.RecordRefused):
            OR.admitted_version(self.opening, OR.advance_record(self.proj, G), MV.load_verified_source(self.proj, G)[1])
        with self.assertRaises(WF.BatchRefused):
            WF._study(G)
        self.assertEqual(self.run_batch(), 2)
        with self.assertRaises(self.up.Refused):
            self.up.freeze_state(self.proj, G, self.ledger_dicts())
        adv_path.unlink()
        # the owner's advance (written by the command) names the row exactly; runs then carry the admitted pin v_a' = 3
        adv = MH.advance(G, OR.ADVANCE_STATEMENT)
        self.assertEqual((adv['admitted_version_before'], adv['admitted_version_after']), (2, 3))
        self.assertEqual(WF._admitted_pin(plan), (3, rows[2]['master_sha256']))
        self.assertEqual(self.run_batch(), 0)
        receipts = [json.loads((f / CP.FILES['forecast_receipt']).read_bytes()) for f in self.run_folders()]
        self.assertEqual({(r['ledger_version'], r['master_sha256']) for r in receipts}, {(3, rows[2]['master_sha256'])})
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE'])
        # the plan itself stays frozen at v_a (its pin is the gate's other admissible pin)
        self.assertEqual((plan['ledger_version'], plan['master_sha256']), (2, rows[1]['master_sha256']))
        # an advance tied to another study manifest is refused by the gate before anything else about the pair
        good = adv_path.read_bytes()
        rec = json.loads(good.decode('ascii'))
        rec['study_manifest_sha256'] = 'e' * 64
        adv_path.write_bytes(canonical(rec))
        text = self.hand_bound_run(plan, plan['cohort'][0], 1577)
        self.assertIn('PLAN_NOT_TIED_TO_STUDY', text)
        self.assertIn('study version advance', text)
        adv_path.write_bytes(good)
        self.assertIn('BATCH_CLOSED', self.hand_bound_run(plan, plan['cohort'][0], 1577))
        # the scorer and the report disclose the advance; the updater stays refused until the seal
        with self.assertRaises(self.up.Refused) as cm:
            self.up.freeze_state(self.proj, G, self.ledger_dicts())
        self.assertIn('admitted version 3', str(cm.exception))
        res = self.score()
        self.assertEqual(self.markers(bid)[-1], 'MODE_H_SEALED')
        self.assertEqual(self.up.freeze_state(self.proj, G, self.ledger_dicts()), 'SEALED')
        text = res['paths'][0].read_text(encoding='ascii')
        self.assertIn('Study version advance (design 4.1, disclosed): admitted version 2 -> 3', text)
        self.assertIn('outcomes read at version 3', text)
        manifest_json = json.loads(res['paths'][2].read_bytes())
        self.assertEqual(manifest_json['mode_h']['admitted_version'], 3)
        self.assertEqual(manifest_json['mode_h']['study_version_advance']['rows_beyond_admitted'][0]['version'], 3)

    def test_a_resumed_attempt_must_find_the_roster_it_started_with(self):
        plan, bid = self.plan, self.bid
        self.assertEqual(self.run_batch(), 0)
        with mock.patch.object(OREAD, 'read_outcomes', side_effect=OSError('disk gone')):
            with self.assertRaises(OSError):
                self.score()
        sp = OR.marker_path(self.proj, G, bid, 'SCORING_STARTED')
        good = sp.read_bytes()
        rec = json.loads(good.decode('ascii'))
        rec['roster_digest'] = 'f' * 64                                  # a consistent ledger, another recorded roster
        sp.write_bytes(canonical(rec))
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))
        with self.assertRaises(MH.ModeHRefused) as cm:
            self.score()
        self.assertIn('roster differs from the one this attempt started scoring', str(cm.exception))
        self.assertEqual(self.markers(bid), ['BATCH_COMPLETE', 'SCORING_STARTED'])
        folder = WF.roots('MODE_H_BATCH')['scores'] / G / bid / rec['attempt_id']
        self.assertFalse((folder / MH.SCORE_LEDGER).exists())
        sp.write_bytes(good)
        self.assertTrue(OREAD.outcome_release_allowed(self.proj, G, 1577))
        res = self.score()
        self.assertEqual(res['attempt_id'], rec['attempt_id'])
        self.assertEqual(self.markers(bid)[-1], 'MODE_H_SEALED')

    def _stop_before_score_complete(self):
        """Run the score up to the ledger and stop before SCORE_COMPLETE is written; return the ledger path."""
        real = OR.write_marker

        def stop(root, game, b, name, rec):
            if name == 'SCORE_COMPLETE':
                raise RuntimeError('power cut before SCORE_COMPLETE')
            return real(root, game, b, name, rec)
        with mock.patch.object(OR, 'write_marker', stop):
            with self.assertRaises(RuntimeError):
                self.score()
        started = OR.marker(self.proj, G, self.bid, 'SCORING_STARTED')
        return WF.roots('MODE_H_BATCH')['scores'] / G / self.bid / started['attempt_id'] / MH.SCORE_LEDGER

    def test_a_bad_ledger_never_completes(self):
        """EX_148 B04: before SCORE_COMPLETE the existing ledger must be exactly the scorer's lines for the frozen
        forecasts and the drawn numbers it records; every tamper refuses with no SCORE_COMPLETE, and no outcome is read."""
        self.assertEqual(self.run_batch(), 0)
        path = self._stop_before_score_complete()
        good = path.read_bytes()
        lines = good.split(b'\n')[:-1]
        recs = [json.loads(x) for x in lines]
        si = [i for i, r in enumerate(recs) if r['schema'] == 'POST_OUTCOME_SCORE_RECORD_V1']
        ri = [i for i, r in enumerate(recs) if r['schema'] == RP.RANK_SCHEMA]

        def with_lines(ls):
            return b''.join(x + b'\n' for x in ls)

        def edited(i, **kw):
            r = dict(recs[i], **kw)
            return lines[:i] + [canonical(r)[:-1]] + lines[i + 1:]
        other = next(i for i in si if recs[i]['draw_number'] != recs[si[0]]['draw_number'])
        cases = {
            'one score line removed': lines[:si[3]] + lines[si[3] + 1:],
            'one rank line removed': lines[:ri[2]] + lines[ri[2] + 1:],
            'one line duplicated': lines[:si[3] + 1] + [lines[si[3]]] + lines[si[3] + 1:],
            'a foreign valid-looking score line': lines + [canonical(dict(recs[si[0]], forecast_content_digest='e' * 64))[:-1]],
            'a receipt binding changed': edited(si[1], freeze_receipt_digest='f' * 64),
            'a match count changed': edited(si[0], main_matches=(recs[si[0]]['main_matches'] + 1) % 8),
            'a drawn number disagreeing within a draw': edited(other, drawn_main=sorted(
                recs[other]['drawn_main'][:-1] + [next(x for x in range(1, 36) if x not in recs[other]['drawn_main'])])),
            'an invalid score record (drawn numbers not ascending)': edited(other, drawn_main=list(reversed(recs[other]['drawn_main']))),
            'lines reordered': [lines[si[1]], lines[si[0]]] + lines[2:],
        }
        for name, ls in cases.items():
            with self.subTest(name):
                path.write_bytes(with_lines(ls))
                with mock.patch.object(OREAD, 'read_outcomes', side_effect=AssertionError('an outcome was read')):
                    with self.assertRaises(MH.ModeHRefused):
                        self.score()
                self.assertEqual(self.markers(self.bid), ['BATCH_COMPLETE', 'SCORING_STARTED'])
        path.write_bytes(good)
        with mock.patch.object(OREAD, 'read_outcomes', side_effect=AssertionError('an outcome was read')):
            self.score()
        self.assertEqual(self.markers(self.bid)[-1], 'MODE_H_SEALED')
        self.assertEqual(OR.marker(self.proj, G, self.bid, 'SCORE_COMPLETE')['score_ledger_sha256'], sha(good))

    def test_the_report_resumes_file_by_file(self):
        """EX_148 B02: a stop after the report's .txt, then after its .csv; each resume verifies what exists, creates only
        what is missing, never overwrites, reads no outcome, and the seal follows all three."""
        self.assertEqual(self.run_batch(), 0)
        real = MH.CP.create_only

        def stop_after(ext):
            def create(p, raw):
                real(p, raw)
                if Path(p).name.startswith('mode_h_') and Path(p).suffix == '.' + ext:
                    raise RuntimeError(f'power cut after the .{ext}')
            return create
        with mock.patch.object(MH.CP, 'create_only', stop_after('txt')):
            with self.assertRaises(RuntimeError):
                self.score()
        started = OR.marker(self.proj, G, self.bid, 'SCORING_STARTED')
        base = RW.mode_h_base_name({'game_id': G, 'first': 1577, 'last': 1586, 'attempt_id': started['attempt_id']})
        folder = RP.roots()['reports'] / G
        present = lambda: sorted(q.suffix for q in folder.iterdir() if q.name.startswith(base))
        self.assertEqual(present(), ['.txt'])
        txt = (folder / f'{base}.txt').read_bytes()
        with mock.patch.object(MH.CP, 'create_only', stop_after('csv')), \
                mock.patch.object(OREAD, 'read_outcomes', side_effect=AssertionError('an outcome was read')):
            with self.assertRaises(RuntimeError):
                self.score()
        self.assertEqual(present(), ['.csv', '.txt'])
        self.assertEqual((folder / f'{base}.txt').read_bytes(), txt)
        self.assertEqual(self.markers(self.bid), ['BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE'])
        # a present file with other bytes refuses, nothing is written
        csv_path = folder / f'{base}.csv'
        good_csv = csv_path.read_bytes()
        csv_path.write_bytes(good_csv + b'x')
        with self.assertRaises(MH.ModeHRefused) as cm:
            self.score()
        self.assertIn(f'{base}.csv differs', str(cm.exception))
        self.assertEqual(present(), ['.csv', '.txt'])
        csv_path.write_bytes(good_csv)
        with mock.patch.object(OREAD, 'read_outcomes', side_effect=AssertionError('an outcome was read')):
            res = self.score()
        self.assertEqual(present(), ['.csv', '.json', '.txt'])
        self.assertEqual(self.markers(self.bid)[-1], 'MODE_H_SEALED')
        seal = OR.marker(self.proj, G, self.bid, 'MODE_H_SEALED')
        self.assertEqual(seal['report_sha256'], sha(txt))
        self.assertEqual(seal['report_manifest_sha256'], sha((folder / f'{base}.json').read_bytes()))
        self.assertEqual(len(self.search_rows('MODE_H_REPORT')), 1)
        self.assertEqual(res['attempt_id'], started['attempt_id'])

    def test_closure_change_after_the_plan_stops_every_step(self):
        target = self.proj / 'src' / 'methods' / '_common' / 'walk_forward.py'
        original = target.read_bytes()
        target.write_bytes(original + b'#\n')
        self.assertEqual(self.run_batch(), 2)
        self.assertIn('closure: changed src/methods/_common/walk_forward.py', self.out[-1])
        self.assertEqual(self.run_folders(), [])
        target.write_bytes(original)
        self.assertEqual(self.run_batch(), 0)
        core = self.env.site_packages / 'fakepkg' / 'core.py'
        core_bytes = core.read_bytes()
        core.write_bytes(core_bytes + b'\n')
        with self.assertRaises(MH.ModeHRefused) as cm:
            self.score()
        self.assertIn('differs from its RECORD hash', str(cm.exception))
        self.assertEqual(self.markers(self.bid), ['BATCH_COMPLETE'])
        core.write_bytes(core_bytes)
        # an orphan marker blocks the score too
        marker = Path(CR.ORPHAN_MARKER)
        marker.parent.mkdir(parents=True)
        marker.write_text('{}')
        with self.assertRaises(MH.ModeHRefused) as cm:
            self.score()
        self.assertIn('UNRESOLVED_ORPHAN_MARKER', str(cm.exception))
        marker.unlink()
        self.score()
        self.assertEqual(self.markers(self.bid)[-1], 'MODE_H_SEALED')


class OzLottoStudy(unittest.TestCase):
    """The whole study for Oz Lotto (no exposure flags; one family; the supplementaries never stored), and EX_148 B04's
    Oz Lotto branch: a line's supplementary_matches must be in range and agree with its division."""

    def test_oz_lotto_end_to_end_and_its_supplementary_check(self):
        from _common.game_profiles import OZLOTTO
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            proj, env = X.project(tmp, OZLOTTO), X.fake_environment(tmp)
            with X.patched(proj, env):
                man = MH.manifest('OZLOTTO')
                self.assertEqual(man['exposure'], {})
                self.assertEqual(man['families'], ['MODEH_OZLOTTO_MR7_MAIN_V1'])
                MH.open_holdout('OZLOTTO', OR.OPENING_STATEMENT)
                X.first_update(proj, OZLOTTO)
                plan = WF.make_mode_h_plan('OZLOTTO', X.small_adapters())
                self.assertEqual(plan['targets'], list(range(1694, 1704)))
                self.assertEqual(WF.run_batch('OZLOTTO', plan['batch_id'], X.small_adapters(), echo=lambda *_: None), 0)
                policy = SP.approved_policy()
                kw = dict(echo=None, n1_runner=N1.runner(policy), seed_line='x', n1_policies_on_file=SP.count_policies(),
                          environment={})
                real = OR.write_marker

                def stop(root, game, b, name, rec):
                    if name == 'SCORE_COMPLETE':
                        raise RuntimeError('power cut before SCORE_COMPLETE')
                    return real(root, game, b, name, rec)
                with mock.patch.object(OR, 'write_marker', stop):
                    with self.assertRaises(RuntimeError):
                        MH.score('OZLOTTO', **kw)
                started = OR.marker(proj, 'OZLOTTO', plan['batch_id'], 'SCORING_STARTED')
                path = WF.roots('MODE_H_BATCH')['scores'] / 'OZLOTTO' / plan['batch_id'] / started['attempt_id'] / MH.SCORE_LEDGER
                good = path.read_bytes()
                lines = good.split(b'\n')[:-1]
                recs = [json.loads(x) for x in lines]
                i = next(k for k, r in enumerate(recs) if r['schema'] == 'POST_OUTCOME_SCORE_RECORD_V1')
                self.assertNotIn('drawn_powerball', recs[i])
                self.assertFalse(any('supplementar' in k and k != 'supplementary_matches' for k in recs[i]))   # never stored
                d = recs[i]['division']
                ran = []
                for name, change in (('supplementary_matches out of range', {'supplementary_matches': 4}),
                                     ('a division that disagrees with its match counts', {'division': 1 if d != 1 else 2})):
                    with self.subTest(name):
                        r = dict(recs[i], **change)
                        path.write_bytes(b''.join(x + b'\n' for x in lines[:i] + [canonical(r)[:-1]] + lines[i + 1:]))
                        with self.assertRaises(MH.ModeHRefused):
                            MH.score('OZLOTTO', **kw)
                        self.assertNotIn('SCORE_COMPLETE', OR.lifecycle_markers_present(proj, 'OZLOTTO', plan['batch_id']))
                        ran.append(name)
                self.assertEqual(len(ran), 2)
                path.write_bytes(good)
                with mock.patch.object(OREAD, 'read_outcomes', side_effect=AssertionError('an outcome was read')):
                    res = MH.score('OZLOTTO', **kw)
                self.assertEqual(OR.lifecycle_markers_present(proj, 'OZLOTTO', plan['batch_id'])[-1], 'MODE_H_SEALED')
                text = res['paths'][0].read_text(encoding='ascii')
                self.assertIn('Game: OZLOTTO', text)
                self.assertIn('Exposure flags (information only; flagged draws are scored and counted like any other draw): none', text)


class OutcomeReaderRule(Base):
    """The freeze-before-outcome rule, decided from the records alone (design 5.3; an always-review subject)."""

    def test_states(self):
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))         # nothing exists
        self.open_study()
        X.first_update(self.proj, P)
        plan = WF.make_mode_h_plan(G, self.adapters)
        bid = plan['batch_id']
        for t in (1577, 1586):
            self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, t))        # plan, no markers
        import mhupa_fixtures as F
        F.write_marker(self.proj, G, bid, 'BATCH_COMPLETE')
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))         # no SCORING_STARTED
        # SCORING_STARTED with a roster digest that is not the records' roster: refused
        OR.write_record(OR.marker_path(self.proj, G, bid, 'SCORING_STARTED'),
                        {'schema': OR.MARKER_SCHEMAS['SCORING_STARTED'], 'batch_id': bid, 'game_id': G,
                         'attempt_id': 'mh-' + '0' * 32, 'roster_digest': 'a' * 64, 'plan_digest': record_digest(plan),
                         'utc': '2026-11-20T10:00:00Z'})
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))
        with self.assertRaises(OREAD.OutcomeRefused):
            OREAD.read_outcomes(repo_root=self.proj, game_id=G, master_sha256=plan['master_sha256'], targets=[1577],
                                ledger_version=2)
        # no DONE ticket at all: the roster digest cannot even be computed -> refused
        with self.assertRaises(OR.RecordRefused):
            OR.roster_digest(self.proj, G, plan)
        # a SCORING_STARTED marker without its roster digest is invalid evidence, never read as a release
        sp = OR.marker_path(self.proj, G, bid, 'SCORING_STARTED')
        sp.unlink()
        OR.write_record(sp, {'schema': OR.MARKER_SCHEMAS['SCORING_STARTED'], 'batch_id': bid, 'game_id': G,
                             'attempt_id': 'mh-' + '0' * 32, 'plan_digest': record_digest(plan), 'utc': '2026-11-20T10:00:00Z'})
        with self.assertRaises(OR.RecordRefused):
            OR.marker(self.proj, G, bid, 'SCORING_STARTED')
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1577))
        # the roster digest binds the run ids of the DONE tickets, not only the pairs: the same pairs under other run
        # ids give another digest (design 5.3: the exact roster, each pair with its DONE ticket)
        tk_path = WF._attempts_path(plan)

        def ledger_with(run_ids):
            lines = b''
            for i, mem in enumerate(plan['cohort']):
                for j, target in enumerate(plan['targets']):
                    req = WF.request_for(plan, mem, target, run_ids(i, j))
                    t = OR.ticket('DONE', scope_kind='MODE_H_BATCH', scope_id=bid, game_id=G, method_id=mem['method_id'],
                                  variant_id=mem['variant_id'], method_revision=mem['method_revision'], target_draw_number=target,
                                  run_id=req['run_id'], utc='2026-11-20T10:00:00Z', terminal_class='SUCCESS PUBLISHED')
                    lines += canonical(t)
            tk_path.write_bytes(lines)
            return OR.roster_digest(self.proj, G, plan)
        d1 = ledger_with(lambda i, j: f'mg-{i:016x}{j:016x}')
        d2 = ledger_with(lambda i, j: f'mg-{i:016x}{j + 1:016x}')
        self.assertNotEqual(d1, d2)
        self.assertEqual(d1, ledger_with(lambda i, j: f'mg-{i:016x}{j:016x}'))
        tk_path.unlink()
        # outside the holdout: never through this rule
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1576))
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, 1587))
        self.assertFalse(OREAD.outcome_release_allowed(self.proj, G, '1577'))
        # the development reader refuses a holdout target whatever the pin
        with self.assertRaises(OREAD.OutcomeRefused):
            OREAD.read_outcomes(repo_root=self.proj, game_id=G, master_sha256=plan['master_sha256'], targets=[1577, 1570],
                                ledger_version=2)
        out = OREAD.read_outcomes(repo_root=self.proj, game_id=G, master_sha256=plan['master_sha256'], targets=[1570],
                                  ledger_version=2)
        self.assertEqual(set(out), {1570})


if __name__ == '__main__':
    unittest.main()
