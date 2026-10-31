"""REL-1 tests (releases and WF-1 design v0.1r1 section 4; owner decisions WF1-1 and WF1-2, 31 October 2026). OFFLINE.

The release of the 39 variants of E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19, in both games:
the installed chains, the absence of every development flag, and a run of every released variant through the
installed registry (no simulated release) on an invented workspace, consumed by read_run. Invented masters and
temporary run folders only; no real draw is read, and nothing in the repository is written.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import e2r_code2_fixtures as C
from test_e6_beta_bernoulli import write_varied_master
import _common.contract_publication as CP
import _common.contract_runner as CR
from _common.contract_dispatch import METHODS_ROOT, dispatch_gate, method_folder
from _common.contract_records import record_digest
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import get_profile

RELEASED = ('E_2', 'E_3', 'E_4', 'E_6', 'E_7', 'E_8', 'E_9', 'E_10', 'E_17', 'E_18', 'E_19')
REASON = ('Released by package REL-1 (releases and WF-1 design v0.1r1, owner decisions WF1-1 and WF1-2, '
          'ratified 31 October 2026). Contract runs on real data need the separate real-development gate.')
CHANGED = {'entry_sequence', 'registry_status', 'registry_status_reason', 'effective_date', 'previous_entry_digest'}


def released_chains(reg):
    return sorted(k for k in reg.chain_keys() if k[1] in RELEASED and k[2] != 'NOT_YET_SPECIFIED')


class InstalledChains(unittest.TestCase):
    def test_every_released_chain_is_formula_open_then_supported(self):
        reg = InstalledRegistry()
        keys = released_chains(reg)
        self.assertEqual(len(keys), 78)
        for g, m, v in keys:
            with self.subTest(game=g, method=m, variant=v):
                e1, e2 = reg.chain(g, m, v)
                self.assertEqual((e1['entry_sequence'], e1['registry_status']), (1, 'FORMULA_OPEN'))
                self.assertEqual((e2['entry_sequence'], e2['registry_status']), (2, 'SUPPORTED'))
                self.assertEqual(e2['previous_entry_digest'], record_digest(e1))
                self.assertEqual((e2['registry_status_reason'], e2['effective_date']), (REASON, '2026-10-31'))
                self.assertEqual({k for k in e1 if e1[k] != e2[k]}, CHANGED)        # texts, revision, declaration kept
                self.assertEqual(reg.active_entry(g, m, v), e2)

    def test_placeholders_and_e1_are_unchanged(self):
        reg = InstalledRegistry()
        for g in ('POWERBALL', 'OZLOTTO'):
            for i in range(2, 63):
                self.assertEqual(len(reg.chain(g, f'E_{i}', 'NOT_YET_SPECIFIED')), 1)
            e1 = reg.chain(g, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
            self.assertEqual([(e['entry_sequence'], e['registry_status']) for e in e1], [(1, 'SUPPORTED')])
        sup = {(g, m, v) for (g, m, v) in reg.chain_keys() if reg.active_entry(g, m, v)['registry_status'] == 'SUPPORTED'}
        self.assertEqual(len(sup), 80)

    def test_no_development_flag_remains(self):
        self.assertEqual(sorted(METHODS_ROOT.rglob('IN_DEVELOPMENT.txt')), [])
        for m in RELEASED:
            self.assertTrue((METHODS_ROOT / method_folder(m) / 'contract.py').is_file())


class EveryReleasedVariantRuns(unittest.TestCase):
    """Through the installed registry and the installed method folders: only the orphan marker is patched (to a
    path in a temporary folder that does not exist)."""

    def test_synthetic_run_succeeds_and_is_consumable(self):
        import Method_Contract_Runner as M
        reg = InstalledRegistry()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            with C.installed(marker=td / 'no_marker'):
                for game in ('POWERBALL', 'OZLOTTO'):
                    p = get_profile(game)
                    target = p.holdout_first - 1
                    ws = td / f'ws_{game}'
                    sha = write_varied_master(ws, p, target, 0)
                    for g, m, v in [k for k in released_chains(reg) if k[0] == game]:
                        with self.subTest(game=g, method=m, variant=v):
                            e = reg.active_entry(g, m, v)
                            d = reg.declaration(e['declaration_digest'])
                            req = C.request(d, e, target, sha, run_id=CP.new_run_id())
                            res = CR.run_contract_method(req, compute=M.ADAPTERS[m].compute, verify=M.ADAPTERS[m].verify,
                                                         repo_root=ws, run_root=td / 'runs')
                            self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: PREDICTION_AVAILABLE'))
                            got = CP.read_run(res.folder)
                            self.assertEqual(got['forecast'], (True, 'CONSUMABLE'))
                            rec = json.loads((res.folder / 'forecast.json').read_bytes())
                            self.assertEqual((rec['method_id'], rec['variant_id'], rec['run_mode']),
                                             (m, v, 'SYNTHETIC_CONTRACT_TEST'))

    def test_release_alone_does_not_admit_real_data(self):
        """With the real-development switch off, a released variant's REAL_DEVELOPMENT request is still refused
        before anything is read or created (the switch is the separate WF-1A gate)."""
        import Method_Contract_Runner as M
        reg = InstalledRegistry()
        e = reg.active_entry('POWERBALL', 'E_6', 'BETA_BERNOULLI_FULL_MEMORY_V1')
        d = reg.declaration(e['declaration_digest'])
        dispatch_gate(C.request(d, e, 1300, 'f' * 64))                      # admitted by the release
        req = dict(C.request(d, e, 1300, 'f' * 64), run_mode='REAL_DEVELOPMENT', product_kind='WF_FORECAST')
        with tempfile.TemporaryDirectory() as td, mock.patch.object(CR, 'ENABLE_CONTRACT_REAL_DEVELOPMENT', False), \
                mock.patch.object(CR, 'load_pinned_draw_view', side_effect=AssertionError('data read')), \
                C.installed(marker=Path(td) / 'no_marker'):
            with self.assertRaises(CR.RunRefused) as cm:
                CR.run_contract_method(req, compute=M.ADAPTERS['E_6'].compute, verify=M.ADAPTERS['E_6'].verify,
                                       repo_root=CR.PROJECT_ROOT, run_root=Path(td) / 'runs')
            self.assertEqual(cm.exception.reason, 'REAL_DEVELOPMENT_DISABLED')
            self.assertFalse((Path(td) / 'runs').exists())


if __name__ == '__main__':
    unittest.main()
