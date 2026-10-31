"""E2R-T14: the dispatch gate truth table and the release transition (E2R-CODE-2). OFFLINE, synthetic only.

Both launchers are exercised: the standalone contract runner (Method_Contract_Runner.main and
contract_runner.run_contract_method) and the coordinator side (coordinator_private.contract_coordinated_gate).
Registries, method folders and masters are temporary copies or invented files; nothing in the
repository is written, no real draw value is read, no process is started.
"""
from __future__ import annotations

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import e2r_fixtures as F
import e2r_code2_fixtures as C
from e2r_fixtures import ROOT
sys.path.insert(0, str(ROOT / 'src'))

from _common import contract_dispatch as CD
from _common import contract_runner as CR
from _common.contract_dispatch import DispatchRefused, dispatch_gate
from _common.contract_forecast import validate_forecast
from _common.contract_records import record_digest
from _common.contract_registry import InstalledRegistry
from coordinator_private.contract_coordinated_gate import gate_coordinated_contract_request


class Base(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.td = Path(self._td.name)
        self.data = C.copy_data_root(self.td)
        self.methods = self.td / 'methods'
        self.methods.mkdir()
        self.ws, self.sha = C.workspace(self.td / 'ws', 'POWERBALL', 1300)
        self._marker = C.installed(marker=self.td / 'no_marker')
        self._marker.__enter__()

    def tearDown(self):
        self._marker.__exit__(None, None, None)
        self._td.cleanup()

    def flag(self, method='E_2', present=True):
        p = self.methods / CD.method_folder(method) / CD.FLAG_NAME
        if present:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('in development\n')
        else:
            p.unlink()

    def both(self, req):
        """(standalone result or refusal text, coordinator refusal text)."""
        try:
            with C.installed(data=self.data, methods=self.methods):
                standalone = CR.run_contract_method(req, compute=C.probe_compute, verify=C.no_verify,
                                                    repo_root=self.ws, run_root=self.td / 'runs')
        except DispatchRefused as exc:
            standalone = exc.text
        with self.assertRaises(DispatchRefused) as cm, C.installed(data=self.data, methods=self.methods):
            gate_coordinated_contract_request(req)
        return standalone, cm.exception.text

    def assert_refused_same(self, req, code):
        standalone, coordinated = self.both(req)
        self.assertIsInstance(standalone, str, 'the standalone runner admitted a request the gate must refuse')
        self.assertEqual(standalone, coordinated, 'both launchers must print the same refusal text')
        self.assertIn(f': {code}: ', standalone)
        self.assertTrue(standalone.startswith('DISPATCH REFUSED: '))
        self.assertTrue(standalone.endswith('No data was read.'))
        self.assertFalse((self.td / 'runs').exists(), 'a refused request created a run folder')


class T14TruthTable(Base):
    def test_status_times_flag(self):
        for status in ('SUPPORTED', 'FORMULA_OPEN', 'UNSUPPORTED_FOR_GAME'):
            for flagged in (False, True):
                with self.subTest(status=status, flag=flagged):
                    self.tearDown()
                    self.setUp()
                    d = C.release_declaration()
                    C.install_declaration(self.data, d)
                    e = C.entry(d, status)
                    C.append_entry(self.data, e)
                    if flagged:
                        self.flag()
                    req = C.request(d, e, 1300, self.sha)
                    if status == 'SUPPORTED' and not flagged:
                        standalone, coordinated = self.both(req)
                        self.assertEqual(standalone.outcome, 'SUCCESS')
                        self.assertIn(': COORDINATED_CONTRACT_DISPATCH_NOT_ENABLED: ', coordinated)
                    else:
                        self.assert_refused_same(req, 'NOT_SUPPORTED' if status != 'SUPPORTED'
                                                 else 'IN_DEVELOPMENT_FLAG_PRESENT')

    def test_missing_stale_and_mismatched_entries(self):
        d = C.release_declaration()
        C.install_declaration(self.data, d)
        e1 = C.entry(d, 'FORMULA_OPEN')
        C.append_entry(self.data, e1)
        e2 = C.entry(d, 'SUPPORTED', seq=2, prev=e1)
        C.append_entry(self.data, e2)
        unregistered = dict(d, variant_id='NEVER_REGISTERED_V1')
        self.assert_refused_same(C.request(unregistered, e2, 1300, self.sha), 'NO_REGISTRY_ENTRY')
        self.assert_refused_same(C.request(d, e1, 1300, self.sha), 'STALE_REGISTRY_ENTRY')
        other = dict(d, minimum_history_draws=2)
        self.assert_refused_same(C.request(other, e2, 1300, self.sha), 'DECLARATION_MISMATCH')
        # An approval for revision 1 is not an approval for revision 2's code.
        d2 = C.release_declaration(revision='2')
        self.assert_refused_same(C.request(d2, e2, 1300, self.sha), 'REVISION_MISMATCH')
        # The NOT_YET_SPECIFIED placeholders can never be requested.
        ph = InstalledRegistry(self.data).active_entry('POWERBALL', 'E_3', 'NOT_YET_SPECIFIED')
        req = dict(C.request(d, e2, 1300, self.sha), method_id='E_3', variant_id='NOT_YET_SPECIFIED',
                   registry_entry_digest=record_digest(ph))
        self.assert_refused_same(req, 'INVALID_RUN_REQUEST')

    def test_installed_e1_admitted_and_e2_to_e62_refused(self):
        reg = InstalledRegistry()
        e = reg.active_entry('POWERBALL', *C.E1)
        d = reg.declaration(e['declaration_digest'])
        got_e, got_d = dispatch_gate(C.request(d, e, 1300, self.sha))
        self.assertEqual((got_e, got_d), (e, d))
        for i in range(2, 63):
            with self.subTest(method=f'E_{i}'):
                ph = reg.active_entry('POWERBALL', f'E_{i}', 'NOT_YET_SPECIFIED')
                req = dict(C.request(d, e, 1300, self.sha), method_id=f'E_{i}', variant_id='NOT_YET_SPECIFIED',
                           registry_entry_digest=record_digest(ph))
                with self.assertRaises(DispatchRefused):
                    dispatch_gate(req)

    def test_gate_fetches_the_registry_again_every_time(self):
        """Reviewer's EX_036 watchpoint: a caller's copy is never trusted or reused."""
        reg = InstalledRegistry()
        e = reg.active_entry('POWERBALL', *C.E1)
        d = reg.declaration(e['declaration_digest'])
        req = C.request(d, e, 1300, self.sha)
        entry1, decl1 = dispatch_gate(req)
        entry1['registry_status'] = 'FORMULA_OPEN'
        decl1['channels']['MAIN']['top_rule_id'] = 'MAP_SET'
        entry2, decl2 = dispatch_gate(req)
        self.assertEqual((entry2, decl2), (e, d))
        with mock.patch.object(CD, 'InstalledRegistry', wraps=InstalledRegistry) as spy:
            dispatch_gate(req)
            dispatch_gate(req)
        self.assertEqual(spy.call_count, 2)

    def test_refusal_reads_no_data_and_creates_nothing(self):
        d = C.release_declaration()
        C.install_declaration(self.data, d)
        e = C.entry(d, 'FORMULA_OPEN')
        C.append_entry(self.data, e)
        req = C.request(d, e, 1300, self.sha)
        opened = []
        real_open = Path.open
        ws = self.ws.resolve()

        def watch(path, *a, **k):
            if Path(path).resolve().is_relative_to(ws):
                opened.append(path)
            return real_open(path, *a, **k)
        with mock.patch.object(CR, 'load_pinned_draw_view', side_effect=AssertionError('data read')), \
                mock.patch.object(Path, 'open', watch):
            with self.assertRaises(DispatchRefused), C.installed(data=self.data, methods=self.methods):
                CR.run_contract_method(req, compute=C.probe_compute, verify=C.no_verify, repo_root=self.ws,
                                       run_root=self.td / 'runs')
        self.assertEqual(opened, [])
        self.assertFalse((self.td / 'runs').exists())

    def test_standalone_launcher_prints_the_refusal(self):
        """Method_Contract_Runner.py itself: a refused run exits 2 and prints the gate's text only."""
        sys.path.insert(0, str(ROOT / 'src' / 'methods'))
        import Method_Contract_Runner as M
        reg = InstalledRegistry()
        ph = reg.active_entry('POWERBALL', 'E_2', 'NOT_YET_SPECIFIED')
        e = reg.active_entry('POWERBALL', *C.E1)
        args = ['run', '--game', 'POWERBALL', '--method', 'E_1', '--variant', C.E1[1], '--revision', '1',
                '--target', '1300', '--view', 'UNORDERED_SET', '--mode', 'SYNTHETIC_CONTRACT_TEST',
                '--declaration-digest', e['declaration_digest'], '--registry-entry-digest', record_digest(ph),
                '--master-sha256', self.sha, '--workspace', str(self.ws)]
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            code = M.main(args)
        self.assertEqual(code, 2)
        self.assertIn('DISPATCH REFUSED: POWERBALL E_1 FULL_HISTORY_RAW_COUNTS_V1 revision 1: STALE_REGISTRY_ENTRY', err.getvalue())
        self.assertEqual(out.getvalue(), '')
        self.assertFalse((self.ws / 'contract_runs').exists())


class T14ReleaseTransition(Base):
    def test_release_transition(self):
        d = C.release_declaration()
        decl_file = C.install_declaration(self.data, d)
        e1 = C.entry(d, 'FORMULA_OPEN')
        e1_file = C.append_entry(self.data, e1)
        self.flag()                                                  # installed non-runnable (E2R-R58)
        decl_bytes, e1_bytes = decl_file.read_bytes(), e1_file.read_bytes()
        self.assert_refused_same(C.request(d, e1, 1300, self.sha), 'NOT_SUPPORTED')
        # Release package, step 1 of 2: a SUPPORTED entry is appended for the same declaration.
        e2 = C.entry(d, 'SUPPORTED', seq=2, prev=e1)
        C.append_entry(self.data, e2)
        self.assert_refused_same(C.request(d, e2, 1300, self.sha), 'IN_DEVELOPMENT_FLAG_PRESENT')
        # Removing the flag alone, without the entry, never releases: shown above in reverse order too.
        self.flag(present=False)
        with C.installed(data=self.data, methods=self.methods):
            res = CR.run_contract_method(C.request(d, e2, 1300, self.sha, run_id='mg-release-transition-01'),
                                         compute=C.probe_compute, verify=C.no_verify, repo_root=self.ws,
                                         run_root=self.td / 'admitted_runs')
        self.assertEqual(res.outcome, 'SUCCESS')
        self.assertEqual((decl_file.read_bytes(), e1_file.read_bytes()), (decl_bytes, e1_bytes))
        import json
        validate_forecast(json.loads((res.folder / 'forecast.json').read_bytes()), d)
        self.assert_refused_same(C.request(d, e1, 1300, self.sha), 'STALE_REGISTRY_ENTRY')
        self.assert_refused_same(C.request(dict(d, uses_dates=True), e2, 1300, self.sha), 'DECLARATION_MISMATCH')

    def test_flag_removal_without_entry_never_releases(self):
        d = C.release_declaration()
        C.install_declaration(self.data, d)
        e1 = C.entry(d, 'FORMULA_OPEN')
        C.append_entry(self.data, e1)
        self.assert_refused_same(C.request(d, e1, 1300, self.sha), 'NOT_SUPPORTED')   # no flag at all


class Package2RosterFromRegistry(unittest.TestCase):
    """Package 2's per-method roster is now read from the installed contract registry."""

    def test_same_statuses_as_the_old_fixed_roster(self):
        from _common.multigame_method_registry import all_statuses, method_status
        for game in ('POWERBALL', 'OZLOTTO'):
            released = {1, 2, 3, 4, 6, 7, 8, 9, 10, 17, 18, 19}          # E_1, and REL-1's eleven methods
            want = {f'E_{i}': ('SUPPORTED' if i in released else 'FORMULA_OPEN') for i in range(1, 63)}
            self.assertEqual(dict(all_statuses(game)), want)
            self.assertEqual(method_status(game, 'E_1'), 'SUPPORTED')
            with self.assertRaises(ValueError):
                method_status(game, 'E_63')

    def test_flag_makes_the_roster_open(self):
        from _common.multigame_method_registry import method_status
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / 'E_001').mkdir()
            with mock.patch.object(CD, 'METHODS_ROOT', Path(td)):
                self.assertEqual(method_status('POWERBALL', 'E_1'), 'SUPPORTED')
                (Path(td) / 'E_001' / CD.FLAG_NAME).write_text('x')
                self.assertEqual(method_status('POWERBALL', 'E_1'), 'FORMULA_OPEN')


class StaticCode2Guards(unittest.TestCase):
    def test_switch_closed_and_no_flag_in_the_tree(self):
        self.assertIs(CR.ENABLE_CONTRACT_REAL_DEVELOPMENT, False)
        # A flag may sit only in the folder of a method in development: no active SUPPORTED entry in either
        # game (E2R-R58: the release package removes the flag and appends SUPPORTED together). E_1 has none.
        reg = InstalledRegistry()
        supported = {m for (g, m, v) in reg.chain_keys() if reg.active_entry(g, m, v)['registry_status'] == 'SUPPORTED'}
        for p in sorted((ROOT / 'src').rglob(CD.FLAG_NAME)):
            rel = p.relative_to(ROOT / 'src' / 'methods').parts
            self.assertEqual(len(rel), 2, f'a flag outside a method folder: {p}')
            method = 'E_' + str(int(rel[0][2:]))
            self.assertEqual(CD.method_folder(method), rel[0])
            self.assertNotIn(method, supported, f'{method} is released but still flagged')
        self.assertFalse((ROOT / 'src' / 'methods' / 'E_001' / CD.FLAG_NAME).exists())

    def test_wrappers_read_no_data_and_name_no_receipts(self):
        for f in sorted((ROOT / 'src' / 'methods' / 'contract_adapters').glob('*.py')):
            text = f.read_text(encoding='utf-8')
            for word in ('game_draws_reader', 'source_data', 'contract_receipts', 'contract_publication',
                         'contract_runner', 'open(', 'read_bytes', 'write_bytes'):
                self.assertNotIn(word, text, f'{f.name} mentions {word}')

    def test_method_folder_locator(self):
        self.assertEqual([CD.method_folder(m) for m in ('E_1', 'E_2', 'E_62')], ['E_001', 'E_002', 'E_062'])
        for bad in ('E_0', 'e_1', 'E_1x', 1):
            with self.assertRaises(ValueError):
                CD.method_folder(bad)


def _patched_roots(data=None, methods=None):
    return C.installed(data=data, methods=methods)


class RosterIsNotAdmission(Base):
    """E2RC2-C03: a SUPPORTED per-method roll-up never approves another, unsupported or stale variant."""

    def add_variant(self, method, variant, status, game='POWERBALL'):
        d = F.declaration(game, method=method, variant=variant)
        C.install_declaration(self.data, d)
        e = C.entry(d, status)
        C.append_entry(self.data, e)
        return d, e

    def test_mixed_variants_of_a_new_method(self):
        from _common.multigame_method_registry import method_status
        from _common.multigame_result_registry import require_synthetic_variant, registered_scientific_binding
        from _common.multigame_worker_launch_handshake import verify_synthetic_worker_request
        from _common.multigame_standalone_contract import begin_synthetic
        from coordinator_private.multigame_launch_spec import build_synthetic_launch_spec
        from _common.game_profiles import POWERBALL
        da, ea = self.add_variant('E_2', 'VARIANT_A_V1', 'SUPPORTED')
        db, eb = self.add_variant('E_2', 'VARIANT_B_V1', 'FORMULA_OPEN')
        with _patched_roots(self.data, self.methods):
            self.assertEqual(method_status('POWERBALL', 'E_2'), 'SUPPORTED')            # the roll-up
            self.assertTrue(CD.variant_released('POWERBALL', 'E_2', 'VARIANT_A_V1'))
            self.assertFalse(CD.variant_released('POWERBALL', 'E_2', 'VARIANT_B_V1'))
            with self.assertRaises(DispatchRefused) as cm:
                dispatch_gate(C.request(db, eb, 1300, self.sha))
            self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
            with self.assertRaises(DispatchRefused) as cm:                              # A's pin cannot admit B
                dispatch_gate(dict(C.request(db, ea, 1300, self.sha)))
            self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
            dispatch_gate(C.request(da, ea, 1300, self.sha))                          # A itself is admitted
            for variant in ('VARIANT_A_V1', 'VARIANT_B_V1'):
                with self.subTest(variant=variant):
                    with self.assertRaises(ValueError):
                        require_synthetic_variant('POWERBALL', 'E_2', variant)
                    with self.assertRaises(ValueError):
                        registered_scientific_binding(game_id='POWERBALL', method_id='E_2', variant_id=variant,
                                                      mode='COORDINATED')
                    with self.assertRaises(ValueError):
                        verify_synthetic_worker_request(game_id='POWERBALL', draw_number=1300, method_id='E_2',
                                                        variant_id=variant, run_id='mg-roster-check-0001',
                                                        group_id='g1', worker_sequence=1,
                                                        root=self.td / 'multigame_synthetic_runs')
                    with self.assertRaises(ValueError):
                        build_synthetic_launch_spec(group_id='g1', worker_sequence=1, run_id='mg-roster-check-0001',
                                                    game_id='POWERBALL', draw_number=1300, method_id='E_2',
                                                    variant_id=variant, synthetic_root=self.td / 'multigame_synthetic_runs')
            with self.assertRaises(ValueError):
                begin_synthetic(self.td / 'p2runs', run_id='mg-roster-check-0002', profile=POWERBALL, target=1300,
                                method_id='E_2', variant_id='VARIANT_B_V1')
            self.assertFalse((self.td / 'p2runs').exists())

    def test_e1_extra_and_withdrawn_variants(self):
        from _common.multigame_method_registry import method_status
        from _common.multigame_standalone_contract import begin_synthetic
        from _common.game_profiles import POWERBALL
        reg = InstalledRegistry()
        e1 = reg.active_entry('POWERBALL', *C.E1)
        d1 = reg.declaration(e1['declaration_digest'])
        dx, ex = self.add_variant('E_1', 'EXTRA_UNRELEASED_V1', 'FORMULA_OPEN')
        dy, ey = self.add_variant('E_1', 'OTHER_RELEASED_V1', 'SUPPORTED')
        with _patched_roots(self.data, self.methods):
            self.assertEqual(method_status('POWERBALL', 'E_1'), 'SUPPORTED')
            with self.assertRaises(DispatchRefused):
                dispatch_gate(C.request(dx, ex, 1300, self.sha))
            with self.assertRaises(ValueError):
                begin_synthetic(self.td / 'p2runs', run_id='mg-roster-check-0003', profile=POWERBALL, target=1300,
                                method_id='E_1', variant_id='EXTRA_UNRELEASED_V1')
            CD.legacy_gate('POWERBALL', *C.E1, '1')                                      # still released
        # FULL_HISTORY withdrawn (entry 2 FORMULA_OPEN) while another E_1 variant stays SUPPORTED.
        C.append_entry(self.data, C.entry(d1, 'FORMULA_OPEN', seq=2, prev=e1))
        with _patched_roots(self.data, self.methods):
            self.assertEqual(method_status('POWERBALL', 'E_1'), 'SUPPORTED')            # roll-up still says so
            with self.assertRaises(DispatchRefused) as cm:
                CD.legacy_gate('POWERBALL', *C.E1, '1')
            self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
            with self.assertRaises(DispatchRefused) as cm:
                dispatch_gate(C.request(d1, e1, 1300, self.sha))
            self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
            with self.assertRaises(ValueError):
                begin_synthetic(self.td / 'p2runs', run_id='mg-roster-check-0004', profile=POWERBALL, target=1300,
                                method_id='E_1', variant_id=C.E1[1])
        self.assertFalse((self.td / 'p2runs').exists())


class LegacyRunnerGate(Base):
    """E2RC2-B01, owner decision D2-3 (29 October 2026): E_1's legacy standalone runner is gated too."""

    def runner(self):
        sys.path.insert(0, str(ROOT / 'src' / 'methods'))
        import E_001_Historical_Appearance_Frequency as R1
        return R1

    def refused(self, args, expect, **patches):
        r1 = self.runner()
        err = io.StringIO()
        with _patched_roots(**patches), contextlib.redirect_stderr(err), \
                mock.patch('E_001.e1_training_view.load_permitted_u_view', side_effect=AssertionError('data read')), \
                mock.patch('E_001.e1_standalone_contract.begin', side_effect=AssertionError('run started')):
            with self.assertRaises(SystemExit) as cm:
                r1.main(args)
        self.assertEqual(cm.exception.code, 2)
        self.assertIn(f'DISPATCH REFUSED: POWERBALL E_1 FULL_HISTORY_RAW_COUNTS_V1 revision 1: {expect}: ', err.getvalue())

    def withdraw(self):
        reg = InstalledRegistry()
        e1 = reg.active_entry('POWERBALL', *C.E1)
        C.append_entry(self.data, C.entry(reg.declaration(e1['declaration_digest']), 'FORMULA_OPEN', seq=2, prev=e1))

    def synthetic_args(self):
        src = self.td / 'synthetic.csv'
        src.write_text('not read\n')
        return ['--mode', 'synthetic-contract', '--target', '1152', '--source', str(src),
                '--synthetic-run-root', str(self.td / 'legacy_runs'), '--run-id', 'e1-gatecheck01']

    def test_withdrawn_or_flagged_e1_is_refused_before_anything(self):
        self.withdraw()
        self.refused(self.synthetic_args(), 'NOT_SUPPORTED', data=self.data)
        flagged = self.td / 'flagged_methods'
        (flagged / 'E_001').mkdir(parents=True)
        (flagged / 'E_001' / CD.FLAG_NAME).write_text('in development\n')
        self.refused(self.synthetic_args(), 'IN_DEVELOPMENT_FLAG_PRESENT', methods=flagged)
        self.assertFalse((self.td / 'legacy_runs').exists())

    def test_real_development_mode_is_refused_too(self):
        r1 = self.runner()
        self.withdraw()
        fake = self.td / 'fake_project'
        args = ['--mode', 'historical-development', '--target', '1152', '--source',
                str(fake / 'nowhere.csv'), '--run-id', 'e1-gatecheck02']
        with mock.patch.object(r1, 'ENABLE_REAL_HISTORICAL_DEVELOPMENT', True), \
                mock.patch.object(r1, '__file__', str(fake / 'src' / 'methods' / 'E_001_Historical_Appearance_Frequency.py')):
            self.refused(args, 'NOT_SUPPORTED', data=self.data)
        self.assertFalse((fake / 'transitory_data').exists())

    def test_released_e1_still_runs_exactly_as_before(self):
        """With the installed registry E_1 is released: the legacy goldens still reproduce (see
        test_e1_standalone and E2R-T09); here, the gate itself admits it."""
        entry, decl = CD.legacy_gate('POWERBALL', *C.E1, '1')
        self.assertEqual(entry['registry_status'], 'SUPPORTED')
        self.assertEqual(decl['method_id'], 'E_1')

if __name__ == '__main__':
    unittest.main()
