"""E_1 revision 3 (MHUP-1 design v0.1r5 section 2; owner decision MHUP-Q10; EX_125 C01). OFFLINE.

E1R3-T01: revision 3's contract records equal E_1 revision 2's frozen reference (tests/fixtures/e1_r2_reference_v1.json,
computed from the base commit outside the repository, in both games, under the synthetic kind and under REAL_DEVELOPMENT)
apart from method_revision, declaration_digest and the content digest. E1R3-T02: on the same invented prefix, revision
3's REAL_HOLDOUT record (bound and ticketed to a synthetic Mode H plan on an opened synthetic game) equals its
REAL_DEVELOPMENT record label for label, with the same permitted-view digest and tie order: one data kind (design 3.3).
E1R3-T03: the adapter passes the view data kind, never the run mode. E1R3-T04: the installed registry chain (the archive itself is test_code3_retirement's).
Every master is invented in a temporary folder; nothing under archive/ is read; no real draw is read.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import e2r_code2_fixtures as C
import e2r_fixtures as F
import mhupa_fixtures as X
from test_e6_beta_bernoulli import write_varied_master
import _common.contract_dispatch as CD
import _common.contract_registry as REG
import _common.contract_runner as CR
from _common.contract_records import record_digest
from _common.contract_registry import InstalledRegistry
from _common.contract_task import view_data_kind
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from _common import owner_records as OR
from contract_adapters import e_001

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'tests' / 'fixtures' / 'e1_r2_reference_v1.json'
R1_REFERENCE = ROOT / 'tests' / 'fixtures' / 'e1_r1_reference_v1.json'
DIFFERS = ('method_revision', 'declaration_digest', 'canonical_content_digest')
MODE_FIELDS = ('run_mode', 'product_kind', 'canonical_content_digest')
BATCH = 'wf-' + 'a' * 32


def pins(game, revision):
    reg = InstalledRegistry()
    e = next(x for x in reg.chain(game, *C.E1) if x['method_revision'] == revision)
    return e, reg.declaration(e['declaration_digest'])


def same_except(a, b, fields):
    return {k: v for k, v in a.items() if k not in fields} == {k: v for k, v in b.items() if k not in fields}


class IdentityWithRevision2(unittest.TestCase):
    """E1R3-T01."""

    def test_reference_provenance(self):
        ref = json.loads(REFERENCE.read_bytes())
        self.assertEqual(ref['schema'], 'E1_R2_REFERENCE_V1')
        self.assertEqual(len(ref['records']), 16)
        self.assertEqual(sorted({r['run_mode'] for r in ref['records']}), ['REAL_DEVELOPMENT', 'SYNTHETIC_CONTRACT_TEST'])
        self.assertEqual({r['method_revision'] for r in ref['records']}, {'2'})
        # The counting and tie code did not change in revision 3: those two sources equal today's bytes.
        for rel in ('src/methods/E_001/__init__.py', 'src/methods/E_001/e1_historical_appearance_frequency.py'):
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                             ref['base_r2_sources_sha256'][rel], rel)
        # And the two that did change are not the archived revision-2 bytes.
        for rel in ('src/methods/E_001/multigame_e1.py', 'src/methods/contract_adapters/e_001.py'):
            self.assertNotEqual(hashlib.sha256((ROOT / rel).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                                ref['base_r2_sources_sha256'][rel], rel)

    def test_r3_equals_r2_label_for_label_in_both_kinds(self):
        ref = json.loads(REFERENCE.read_bytes())
        with tempfile.TemporaryDirectory() as td, C.installed(marker=Path(td) / 'no_marker'):
            td = Path(td)
            for r2 in ref['records']:
                game, t, mode = r2['game_id'], r2['target_draw_number'], r2['run_mode']
                e3, d3 = pins(game, '3')
                e2, d2 = pins(game, '2')
                ws = td / f'{game}_{t}_{mode}'
                sha = write_varied_master(ws, get_profile(game), t, 0)
                req = C.request(d3, e3, t, sha, run_id='mg-' + '2' * 32)
                req['run_mode'], req['product_kind'] = mode, r2['product_kind']
                with (mock.patch.object(CR, 'PROJECT_ROOT', ws) if mode == 'REAL_DEVELOPMENT' else contextlib.nullcontext()):
                    res = CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=ws,
                                                 run_root=td / f'runs_{game}_{t}_{mode}')
                self.assertEqual(res.outcome, 'SUCCESS', (game, t, mode, res.reason))
                r3 = json.loads((res.folder / 'forecast.json').read_bytes())
                self.assertTrue(same_except(r3, r2, DIFFERS), (game, t, mode))
                self.assertEqual((r2['method_revision'], r3['method_revision']), ('2', '3'))
                self.assertEqual((r2['declaration_digest'], r3['declaration_digest']),
                                 (e2['declaration_digest'], e3['declaration_digest']))
                self.assertNotEqual(r2['canonical_content_digest'], r3['canonical_content_digest'])

    def test_r3_still_equals_the_revision_1_reference(self):
        """The chain of identity holds across both revisions: r3 equals r1's frozen synthetic records too."""
        ref = json.loads(R1_REFERENCE.read_bytes())
        with tempfile.TemporaryDirectory() as td, C.installed(marker=Path(td) / 'no_marker'):
            td = Path(td)
            for r1 in ref['records']:
                game, t = r1['game_id'], r1['target_draw_number']
                e3, d3 = pins(game, '3')
                sha = write_varied_master(td / f'{game}_{t}', get_profile(game), t, 0)
                res = CR.run_contract_method(C.request(d3, e3, t, sha, run_id='mg-' + '1' * 32), compute=e_001.compute,
                                             verify=e_001.verify, repo_root=td / f'{game}_{t}', run_root=td / f'runs_{game}_{t}')
                self.assertEqual(res.outcome, 'SUCCESS')
                self.assertTrue(same_except(json.loads((res.folder / 'forecast.json').read_bytes()), r1, DIFFERS), (game, t))


class OneDataKind(unittest.TestCase):
    """E1R3-T02 (design 3.3): the same prefix gives the same digest, ranking and tie order in every real mode."""

    def test_holdout_record_equals_development_record_on_the_same_prefix(self):
        for p in (POWERBALL, OZLOTTO):
            game = p.game_id
            with tempfile.TemporaryDirectory() as td:
                td = Path(td)
                proj = td / 'project'
                rows = X.grow_master(proj, p, [list(range(p.holdout_first, p.holdout_last + 2))])
                data = C.copy_data_root(td)
                e3, d3 = pins(game, '3')
                with contextlib.ExitStack() as st:
                    st.enter_context(mock.patch.object(CR, 'PROJECT_ROOT', proj))
                    st.enter_context(mock.patch.object(CR, 'ORPHAN_MARKER', proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'))
                    st.enter_context(mock.patch.object(CD, 'PROJECT_ROOT', proj))
                    st.enter_context(mock.patch.object(REG, 'DATA_ROOT', data))
                    X.write_opening_record(proj, game, freeze_version=1, freeze_sha=rows[0]['master_sha256'])
                    cohort = [{'method_id': 'E_1', 'variant_id': C.E1[1], 'method_revision': '3',
                               'declaration_digest': e3['declaration_digest'], 'registry_entry_digest': record_digest(e3)}]
                    plan = X.write_mode_h_plan(proj, game, BATCH, cohort, list(range(p.holdout_first, p.holdout_last + 1)))
                    v, sha = 2, rows[1]['master_sha256']
                    records = {}
                    for t in (p.holdout_first, p.holdout_first + 4, p.holdout_last):
                        rid_h, rid_d = f'mg-holdout-{t}-' + 'a' * 8, f'mg-devel-{t}-' + 'b' * 8
                        hold = F.request(d3, t, 'UNORDERED_SET', run_mode='REAL_HOLDOUT', product='WF_FORECAST', sha=sha,
                                         run_id=rid_h, entry_digest=record_digest(e3))
                        hold['ledger_version'] = v
                        hold['binding'] = X.binding_for_plan(plan, rid_h)
                        X.open_ticket(OR.mode_h_batch_folder(proj, game, BATCH) / 'attempts.jsonl', hold,
                                      scope_kind='MODE_H_BATCH', scope_id=BATCH)
                        res_h = CR.run_contract_method(hold, compute=e_001.compute, verify=e_001.verify, repo_root=proj,
                                                       run_root=OR.mode_h_runs_root(proj))
                        dev = F.request(d3, t, 'UNORDERED_SET', run_mode='REAL_DEVELOPMENT', product='WF_FORECAST', sha=sha,
                                        run_id=rid_d, entry_digest=record_digest(e3))
                        dev['ledger_version'] = v
                        dev['binding'] = X.DIAGNOSTIC
                        X.write_marker(proj, game, BATCH, 'MODE_H_SEALED')          # the diagnostic route needs the seal
                        res_d = CR.run_contract_method(dev, compute=e_001.compute, verify=e_001.verify, repo_root=proj,
                                                       run_root=OR.diagnostic_runs_root(proj))
                        (OR.mode_h_batch_folder(proj, game, BATCH) / 'MODE_H_SEALED.json').unlink()
                        self.assertEqual((res_h.outcome, res_d.outcome), ('SUCCESS', 'SUCCESS'), (game, t, res_h.reason, res_d.reason))
                        h = json.loads((res_h.folder / 'forecast.json').read_bytes())
                        d = json.loads((res_d.folder / 'forecast.json').read_bytes())
                        self.assertTrue(same_except(h, d, MODE_FIELDS), (game, t))
                        self.assertEqual(h['permitted_view_digest'], d['permitted_view_digest'])
                        self.assertEqual((h['run_mode'], d['run_mode']), ('REAL_HOLDOUT', 'REAL_DEVELOPMENT'))
                        records[t] = h
                    # three different targets give three different records (the prefix grew), each with the right training end
                    self.assertEqual(len({r['permitted_view_digest'] for r in records.values()}), 3)
                    for t, r in records.items():
                        self.assertEqual(r['training_last_draw_number'], t - 1)


class MethodOwnChecks(unittest.TestCase):
    """Revision 3's own refusals: a run mode is not a view data kind; a short training view is refused."""

    def records(self, profile, target):
        return [{'draw': profile.first_draw + i, **{d.barrel_id: list(range(d.low, d.low + d.selected)) for d in profile.barrels}}
                for i in range(target - profile.first_draw)]

    def test_data_kind_and_view_length(self):
        from E_001 import multigame_e1 as E1
        for p in (POWERBALL, OZLOTTO):
            target = p.first_draw + 3
            good = self.records(p, target)
            for kind in ('REAL_HOLDOUT', 'REAL_DEVELOPMENT', 'FINAL_NEXT_DRAW', 'CATCH_UP', 'OWNER_DIAGNOSTIC', ''):
                with self.assertRaises(ValueError, msg=kind):
                    E1.forecast(p, good, 'a' * 64, target, data_kind=kind)
            for kind in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT'):
                out = E1.forecast(p, good, 'a' * 64, target, data_kind=kind)
                self.assertEqual((out['data_kind'], out['draw_number']), (kind, target))
                with self.assertRaises(ValueError):                      # one record short
                    E1.forecast(p, good[:-1], 'a' * 64, target, data_kind=kind)
                with self.assertRaises(ValueError):                      # one record too many
                    E1.forecast(p, self.records(p, target + 1), 'a' * 64, target, data_kind=kind)


class Adapter(unittest.TestCase):
    """E1R3-T03: the adapter hands E_1 the view data kind of the run mode, never the run mode itself."""

    def test_view_data_kind_mapping(self):
        for mode in ('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'CATCH_UP'):
            self.assertEqual(view_data_kind(mode), 'REAL_HISTORICAL_DEVELOPMENT')
        for mode in ('SYNTHETIC_CONTRACT_TEST', 'SYNTHETIC_NULL', 'IN_SAMPLE_DIAGNOSTIC'):
            self.assertEqual(view_data_kind(mode), mode)
        src = (ROOT / 'src' / 'methods' / 'contract_adapters' / 'e_001.py').read_text(encoding='ascii')
        self.assertIn('data_kind=view_data_kind(task.run_mode)', src)
        self.assertNotIn('data_kind=task.run_mode', src)
        e1 = (ROOT / 'src' / 'methods' / 'E_001' / 'multigame_e1.py').read_text(encoding='ascii')
        self.assertNotIn('historical_development_target_allowed', e1)
        self.assertNotIn('REAL_DEVELOPMENT', e1)


class RegistryAndArchive(unittest.TestCase):
    """E1R3-T04."""

    def test_revision_3_active_and_revision_2_archived(self):
        for game in ('POWERBALL', 'OZLOTTO'):
            reg = InstalledRegistry()
            chain = reg.chain(game, *C.E1)
            self.assertEqual([(e['entry_sequence'], e['method_revision'], e['registry_status']) for e in chain],
                             [(1, '1', 'SUPPORTED'), (2, '2', 'SUPPORTED'), (3, '3', 'SUPPORTED')])
            d3 = reg.declaration(chain[2]['declaration_digest'])
            d2 = reg.declaration(chain[1]['declaration_digest'])
            self.assertEqual(dict(d3, method_revision='2'), d2)
            reason = chain[2]['registry_status_reason']
            self.assertIn('MHUP-Q10', reason)
            self.assertIn('Revision 2 is archived', reason)
            self.assertEqual(chain[2]['previous_entry_digest'], record_digest(chain[1]))
        # The archived revision-2 files and their README are checked, byte for byte, by test_code3_retirement (the
        # one test file allowed to name the archive).


if __name__ == '__main__':
    unittest.main()
