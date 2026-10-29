"""E2R-T16 at run level, E_1 through the contract, and run-level prefix and hygiene checks (E2R-CODE-2).

OFFLINE, synthetic only: invented masters in temporary workspaces, temporary run folders. No process is
started or stopped, nothing is killed, no file in the repository is written, no real draw value is read.
"""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import e2r_fixtures as F
import e2r_code2_fixtures as C
from e2r_fixtures import ROOT

from _common import contract_publication as CP
from _common import contract_runner as CR
from _common.contract_forecast import MethodOutput, BarrelOutput, ScoredRanking
from _common.contract_publication import FILES, RunPublication, read_run
from _common.contract_records import record_digest
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import OZLOTTO, POWERBALL

sys.path.insert(0, str(ROOT / 'src' / 'methods'))
from contract_adapters import e_001   # noqa: E402


def e1_pins(game):
    reg = InstalledRegistry()
    e = reg.active_entry(game, *C.E1)
    return e, reg.declaration(e['declaration_digest'])


class Base(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.td = Path(self._td.name)
        self.marker = self.td / 'no_marker'
        self._marker = C.installed(marker=self.marker)
        self._marker.__enter__()

    def tearDown(self):
        self._marker.__exit__(None, None, None)
        self._td.cleanup()

    def run_e1(self, game, target, *, ws_name='ws', suffix=0, run_id=None, **kw):
        ws, sha = C.workspace(self.td / ws_name, game, target, suffix)
        e, d = e1_pins(game)
        req = C.request(d, e, target, sha, run_id=run_id or CP.new_run_id())
        return req, d, CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=ws,
                                              run_root=self.td / 'runs', **kw)

    def probe(self, *, compute=C.probe_compute, verify=C.no_verify, run_id='mg-synthetic-probe-0001', decl=None,
              product=None):
        self.data = data = C.copy_data_root(self.td)
        d = decl or C.release_declaration()
        C.install_declaration(data, d)
        e = C.entry(d, 'SUPPORTED')
        C.append_entry(data, e)
        ws, sha = C.workspace(self.td / 'pws', 'POWERBALL', 1300)
        req = C.request(d, e, 1300, sha, run_id=run_id)
        if product is not None:
            req['product_kind'] = product
        with C.installed(data=data, methods=self.td / 'methods'):
            return d, CR.run_contract_method(req, compute=compute, verify=verify, repo_root=ws,
                                             run_root=self.td / 'runs')

    def consumed(self, folder, data_root=None):
        with C.installed(data=data_root):
            return read_run(folder)

    @staticmethod
    def files(folder):
        return sorted(p.name for p in folder.iterdir())


class E1ThroughTheContract(Base):
    def test_e1_runs_and_equals_e1_own_result(self):
        from E_001.multigame_e1 import forecast as e1_forecast
        from _common.contract_task import permitted_view_digest
        from _common.game_draws_reader import load_pinned_draw_view
        from _common.contract_records import reader_pin
        for p in (POWERBALL, OZLOTTO):
            for target in F.targets(p)[:3]:
                with self.subTest(game=p.game_id, target=target):
                    self.tearDown(); self.setUp()
                    req, d, res = self.run_e1(p.game_id, target)
                    self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: PREDICTION_AVAILABLE'))
                    self.assertEqual(res.folder, self.td / 'runs' / p.game_id / 'E_1' / C.E1[1] / req['run_id'])
                    self.assertEqual(self.files(res.folder), ['forecast.json', 'forecast_receipt.json', 'terminal.json'])
                    c1 = json.loads((res.folder / 'forecast.json').read_bytes())
                    view = load_pinned_draw_view(repo_root=self.td / 'ws', run_manifest=reader_pin(req))
                    rows = [{'draw': r['draw'], 'MAIN': r['main'], **({'POWERBALL': [r['powerball']]} if 'powerball' in r else {})}
                            for r in view.simple_rows()]
                    own = e1_forecast(p, rows, permitted_view_digest(view, req['run_mode']), target,
                                      data_kind='SYNTHETIC_CONTRACT_TEST')
                    for bid, b in own['barrels'].items():
                        self.assertEqual(c1['barrels'][bid]['ranking'], b['ranking'])
                        self.assertEqual(c1['barrels'][bid]['top']['labels'], b['top'])
                        self.assertEqual(c1['barrels'][bid]['worst']['labels'], b['worst'])
                    self.assertEqual(self.consumed(res.folder)['forecast'], (True, 'CONSUMABLE'))

    def test_e1_identity_check_refuses_a_different_record(self):
        def bad_compute(task, view):
            out = e_001.compute(task, view)
            first = out.barrels['MAIN'].ranking.scores
            low = min(first)
            changed = dict(first)
            changed[low] = first[low] + 1000
            return MethodOutput({**out.barrels, 'MAIN': BarrelOutput(ScoredRanking(changed))})
        ws, sha = C.workspace(self.td / 'ws', 'POWERBALL', 1300)
        e, d = e1_pins('POWERBALL')
        res = CR.run_contract_method(C.request(d, e, 1300, sha), compute=bad_compute, verify=e_001.verify, repo_root=ws,
                                     run_root=self.td / 'runs')
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertIn('E_1 identity check', res.reason)
        self.assertEqual(self.files(res.folder), ['terminal.json'])

    def test_e1_wrapper_refuses_non_synthetic_data(self):
        """E_1's own function refuses anything but SYNTHETIC_CONTRACT_TEST data (unchanged E_1 code)."""
        class T:
            method_id, game_id, run_mode, target_draw_number = 'E_1', 'POWERBALL', 'REAL_DEVELOPMENT', 1300
        class View:
            def simple_rows(self):
                return []
            def e1_view_digest(self, *, data_kind):
                return 'a' * 64
        with self.assertRaises(ValueError):
            e_001.compute(T(), View())


class T16RunLevel(Base):
    def test_publication_order_and_create_only(self):
        req, d, res = self.run_e1('POWERBALL', 1300, run_id='mg-order-check-0001')
        t = json.loads((res.folder / 'terminal.json').read_bytes())
        rc = json.loads((res.folder / 'forecast_receipt.json').read_bytes())
        self.assertEqual(t['receipt_digests'], [record_digest(rc)])
        self.assertFalse({k for k in rc if 'scor' in k})
        mtimes = [(res.folder / FILES[k]).stat().st_mtime_ns for k in ('forecast', 'forecast_receipt', 'terminal')]
        self.assertEqual(mtimes, sorted(mtimes))
        with self.assertRaises(FileExistsError):
            CP.create_only(res.folder / 'forecast.json', b'{}')
        with self.assertRaises(FileExistsError):              # the same run ID never gets a second folder
            RunPublication(self.td / 'runs', req, entry_digest=req['registry_entry_digest'], provenance={})
        self.assertFalse([p for p in res.folder.iterdir() if '.part-' in p.name])

    def test_interrupted_after_the_receipt_is_not_consumable(self):
        """The run stops after D1 and before D2 (no terminal record can be written): files stay, nothing is
        cleaned up, and the output is not consumable."""
        with mock.patch.object(RunPublication, 'terminal', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.run_e1('POWERBALL', 1300, run_id='mg-interrupted-0001')
        folder = self.td / 'runs' / 'POWERBALL' / 'E_1' / C.E1[1] / 'mg-interrupted-0001'
        self.assertEqual(self.files(folder), ['forecast.json', 'forecast_receipt.json'])
        _e, d = e1_pins('POWERBALL')
        self.assertEqual(self.consumed(folder)['forecast'], (False, 'NO_TERMINAL_RECORD'))

    def test_failure_after_a_receipt_names_no_receipt(self):
        """C1 and D1 are published, then the diagnostic publication fails: D2 says RUNTIME_FAILURE, names
        no receipt, and the forecast is not consumable although its own files are valid."""
        with mock.patch.object(RunPublication, 'freeze_diagnostic', side_effect=OSError('disk full (simulated)')):
            d, res = self.probe()
        self.assertEqual(res.outcome, 'RUNTIME_FAILURE')
        self.assertTrue(res.reason.startswith('PUBLICATION_FAILED: OSError'))
        self.assertEqual(res.terminal['receipt_digests'], [])
        self.assertEqual(self.files(res.folder), ['forecast.json', 'forecast_receipt.json', 'terminal.json'])
        self.assertEqual(self.consumed(res.folder, data_root=self.data)['forecast'], (False, 'TERMINAL_RUNTIME_FAILURE'))

    def test_probe_with_diagnostic_publishes_both(self):
        d, res = self.probe()
        self.assertEqual(res.outcome, 'SUCCESS')
        self.assertEqual(self.files(res.folder), ['diagnostic.json', 'diagnostic_receipt.json', 'forecast.json',
                                                  'forecast_receipt.json', 'terminal.json'])
        self.assertEqual(len(res.terminal['receipt_digests']), 2)
        got = self.consumed(res.folder, data_root=self.data)
        self.assertEqual(got, {'forecast': (True, 'CONSUMABLE'), 'diagnostic': (True, 'CONSUMABLE')})
        self.assertEqual(CP.run_disposition(res.terminal), 'SUCCESS')

    def test_method_failures_end_in_terminal_records(self):
        def boom(task, view):
            raise RuntimeError('synthetic method failure')

        def nan(task, view):
            out = C.probe_compute(task, view)
            sc = dict(out.barrels['MAIN'].ranking.scores)
            sc[min(sc)] = float('nan')
            return MethodOutput({**out.barrels, 'MAIN': BarrelOutput(ScoredRanking(sc), out.barrels['MAIN'].probability)},
                                diagnostic=out.diagnostic)

        def refuse(task, view, c1, c2):
            raise ValueError('synthetic verify refusal')
        for name, kw, outcome in (('boom', {'compute': boom}, 'RUNTIME_FAILURE'),
                                  ('nan', {'compute': nan}, 'NUMERIC_INVALID'),
                                  ('verify', {'verify': refuse}, 'VALIDATION_FAILURE')):
            with self.subTest(case=name):
                self.tearDown(); self.setUp()
                d, res = self.probe(**kw)
                self.assertEqual(res.outcome, outcome, res.reason)
                self.assertEqual(self.files(res.folder), ['terminal.json'])
                self.assertEqual(res.terminal['receipt_digests'], [])

    def test_bad_pin_is_a_data_admission_failure(self):
        ws, sha = C.workspace(self.td / 'ws', 'POWERBALL', 1300)
        e, d = e1_pins('POWERBALL')
        res = CR.run_contract_method(C.request(d, e, 1300, '0' * 64), compute=e_001.compute, verify=e_001.verify,
                                     repo_root=ws, run_root=self.td / 'runs')
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertTrue(res.reason.startswith('DATA_ADMISSION_REFUSED'))
        self.assertEqual(self.files(res.folder), ['terminal.json'])


class RefusalsBeforeAnything(Base):
    def test_orphan_marker_refuses_first(self):
        self.marker.write_text('{}')
        with self.assertRaises(CR.RunRefused) as cm:
            self.run_e1('POWERBALL', 1300)
        self.assertEqual(cm.exception.reason, 'UNRESOLVED_ORPHAN_MARKER')
        self.assertFalse((self.td / 'runs').exists())

    def test_real_development_is_switched_off(self):
        self.assertIs(CR.ENABLE_CONTRACT_REAL_DEVELOPMENT, False)
        e, d = e1_pins('POWERBALL')
        req = F.request(d, 1300, 'UNORDERED_SET', run_mode='REAL_DEVELOPMENT', entry_digest=record_digest(e))
        with mock.patch.object(CR, 'load_pinned_draw_view', side_effect=AssertionError('data read')):
            with self.assertRaises(CR.RunRefused) as cm:
                CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=self.td,
                                       run_root=self.td / 'runs')
        self.assertEqual(cm.exception.reason, 'REAL_DEVELOPMENT_DISABLED')
        self.assertFalse((self.td / 'runs').exists())

    def test_synthetic_workspace_must_stay_out_of_the_project(self):
        proj = self.td / 'project'
        for sub in ('', 'source_data', 'results/x', 'transitory_data', 'src', 'tests', 'doc', 'review', 'exchange'):
            with self.subTest(sub=sub), self.assertRaises(ValueError):
                CR.check_synthetic_workspace(proj / sub, proj)
        self.assertEqual(CR.check_synthetic_workspace(proj / 'CLAUDE_CODE_WORKING_FOLDER_TREE' / 'scratch' / 'w', proj),
                         (proj / 'CLAUDE_CODE_WORKING_FOLDER_TREE' / 'scratch' / 'w').resolve())
        self.assertEqual(CR.check_synthetic_workspace(self.td / 'elsewhere', proj), (self.td / 'elsewhere').resolve())


class RunLevelPrefixAndHygiene(Base):
    def test_forecast_bytes_ignore_the_suffix_and_the_receipt_does_not(self):
        """Run-level E2R-T03: rewriting draws at and after the target changes the master and the receipt's
        master SHA-256, never the frozen forecast bytes."""
        out = []
        for i, suffix in enumerate((0, 1)):
            req, d, res = self.run_e1('POWERBALL', 1300, ws_name=f'ws{i}', suffix=suffix)
            out.append(((res.folder / 'forecast.json').read_bytes(),
                        json.loads((res.folder / 'forecast_receipt.json').read_bytes())['master_sha256']))
        self.assertEqual(out[0][0], out[1][0])
        self.assertNotEqual(out[0][1], out[1][1])

    def test_no_run_identity_or_path_in_the_forecast(self):
        req, d, res = self.run_e1('OZLOTTO', 1600, run_id='mg-hygiene-check-0001')
        raw = (res.folder / 'forecast.json').read_bytes().decode('ascii')
        for leak in ('mg-hygiene-check-0001', str(self.td), 'contract_runs', req['master_sha256'], 'STANDALONE',
                     req['registry_entry_digest']):
            self.assertNotIn(leak, raw)

    def test_launcher_end_to_end(self):
        """Method_Contract_Runner.py: pins, then a synthetic run, exit code 0, nothing printed but status."""
        import Method_Contract_Runner as M
        ws, sha = C.workspace(self.td / 'ws', 'POWERBALL', 1300)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(M.main(['pins', '--game', 'POWERBALL', '--method', 'E_1', '--variant', C.E1[1]]), 0)
        pins = dict(line.split(': ', 1) for line in out.getvalue().splitlines())
        args = ['run', '--game', 'POWERBALL', '--method', 'E_1', '--variant', C.E1[1], '--revision', pins['method_revision'],
                '--target', '1300', '--view', 'UNORDERED_SET', '--mode', 'SYNTHETIC_CONTRACT_TEST',
                '--declaration-digest', pins['declaration_digest'], '--registry-entry-digest', pins['registry_entry_digest'],
                '--master-sha256', sha, '--workspace', str(ws)]
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(CR, 'ORPHAN_MARKER', self.marker), contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(err):
            code = M.main(args)
        self.assertEqual(code, 0, err.getvalue())
        lines = out.getvalue().splitlines()
        self.assertTrue(lines[0].startswith('[CONTRACT] SUCCESS run=mg-'))
        self.assertEqual(len(lines), 2)
        folder = Path(lines[1].split('folder=', 1)[1])
        self.assertTrue(folder.is_relative_to((ws / 'contract_runs').resolve()))


class ConsumptionGates(Base):
    """E2RC2-B02: read_run establishes every gate itself; nothing a caller passes can vouch for one."""

    def test_no_caller_supplied_gate_or_declaration(self):
        import inspect
        params = set(inspect.signature(read_run).parameters)
        self.assertEqual(params, {'folder'})

    def test_an_active_orphan_marker_blocks_consumption(self):
        req, d, res = self.run_e1('POWERBALL', 1300)
        self.assertEqual(self.consumed(res.folder)['forecast'], (True, 'CONSUMABLE'))
        self.marker.write_text('{}')
        self.assertEqual(self.consumed(res.folder)['forecast'], (False, 'UNRESOLVED_ORPHAN_MARKER'))
        self.marker.unlink()
        self.assertEqual(self.consumed(res.folder)['forecast'], (True, 'CONSUMABLE'))

    def test_coordinated_runs_are_never_consumable_here(self):
        """A folder whose records claim the COORDINATED path (CODE-2 can no longer publish one; this one is
        fabricated) has group and exit-receipt gates CODE-2 cannot evidence: never consumable here."""
        req, d, res = self.run_e1('POWERBALL', 1300)
        for name in ('terminal.json', 'forecast_receipt.json'):
            rec = json.loads((res.folder / name).read_bytes())
            rec['execution_path'] = 'COORDINATED'
            (res.folder / name).unlink()
            (res.folder / name).write_bytes(CP.canonical(rec))
        got = self.consumed(res.folder)['forecast']
        self.assertEqual(got[0], False)
        self.assertTrue(got[1].startswith('COORDINATED_EVIDENCE_NOT_AVAILABLE'))

    def test_declaration_and_admitting_entry_come_from_the_installed_registry(self):
        d, res = self.probe()
        # Under the installed registry this probe's declaration and entry do not exist: not consumable.
        self.assertEqual(self.consumed(res.folder)['forecast'], (False, 'DECLARATION_NOT_INSTALLED'))
        self.assertEqual(self.consumed(res.folder, data_root=self.data)['forecast'], (True, 'CONSUMABLE'))
        # A receipt naming an entry that is not in the chain is refused.
        rc_path = res.folder / 'forecast_receipt.json'
        rc = json.loads(rc_path.read_bytes())
        moved = self.td / 'moved' / 'POWERBALL' / d['method_id'] / d['variant_id'] / rc['run_id']
        moved.mkdir(parents=True)
        for f in res.folder.iterdir():
            (moved / f.name).write_bytes(f.read_bytes())
        self.assertEqual(self.consumed(moved, data_root=self.data)['forecast'], (True, 'CONSUMABLE'))
        rc['registry_entry_digest'] = 'e' * 64
        (moved / 'forecast_receipt.json').unlink()
        (moved / 'forecast_receipt.json').write_bytes(CP.canonical(rc))
        self.assertEqual(self.consumed(moved, data_root=self.data)['forecast'],
                         (False, 'ADMITTING_ENTRY_NOT_INSTALLED_OR_NOT_SUPPORTED'))

    def test_folder_must_match_its_records(self):
        req, d, res = self.run_e1('POWERBALL', 1300)
        other = self.td / 'elsewhere' / 'OZLOTTO' / 'E_1' / C.E1[1] / req['run_id']
        other.mkdir(parents=True)
        for f in res.folder.iterdir():
            (other / f.name).write_bytes(f.read_bytes())
        self.assertEqual(self.consumed(other)['forecast'], (False, 'RUN_FOLDER_DOES_NOT_MATCH_RECORDS'))


class NoTicketAndProducts(Base):
    """E2RC2-C02 and E2RC2-O01."""

    @staticmethod
    def noprob_decl(diagnostic=True):
        """Channels that declare rankings but no probability vector, so a NoRanking output is lawful."""
        d = C.release_declaration()
        d['channels'] = {'MAIN': F.channel(), 'POWERBALL': F.channel(rk='RANKING_ORDER_ONLY', st='NONE', ot='GROUPED')}
        if not diagnostic:
            d['diagnostic_schema_id'] = None
        return d

    def no_ticket(self, task, view):
        from _common.contract_forecast import NoRanking
        return MethodOutput({'MAIN': BarrelOutput(NoRanking('synthetic: no view supports a ranking')),
                             'POWERBALL': BarrelOutput(NoRanking('synthetic: no view supports a ranking'))})

    def test_valid_empty_target_is_diagnostic_only_not_a_failure(self):
        d, res = self.probe(compute=self.no_ticket, decl=self.noprob_decl(diagnostic=False))
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertTrue(res.reason.startswith(CP.NO_TICKET_NO_DIAGNOSTIC + ':'))
        self.assertEqual(self.files(res.folder), ['terminal.json'])
        self.assertEqual(CP.run_disposition(res.terminal), 'DIAGNOSTIC_ONLY')

    def test_no_ticket_with_a_declared_diagnostic_missing_is_invalid(self):
        d, res = self.probe(compute=self.no_ticket, decl=self.noprob_decl())   # declares a diagnostic
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertTrue(res.reason.startswith('CONTRACT_REFUSED_OUTPUT'))
        self.assertEqual(CP.run_disposition(res.terminal), 'FAILED')

    def test_no_ticket_with_a_diagnostic_publishes_only_c2(self):
        def diag_only(task, view):
            out = C.probe_compute(task, view)
            return MethodOutput(self.no_ticket(task, view).barrels, diagnostic=out.diagnostic)
        d, res = self.probe(compute=diag_only, decl=self.noprob_decl())
        self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: DIAGNOSTIC_ONLY'))
        self.assertEqual(self.files(res.folder), ['diagnostic.json', 'diagnostic_receipt.json', 'terminal.json'])
        self.assertEqual(self.consumed(res.folder, data_root=self.data), {'diagnostic': (True, 'CONSUMABLE')})

    def test_insufficient_history_is_published_but_has_no_ticket(self):
        d = C.release_declaration()
        d['minimum_history_draws'] = 5000
        d, res = self.probe(decl=d)
        self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: INSUFFICIENT_HISTORY'))
        c1 = json.loads((res.folder / 'forecast.json').read_bytes())
        self.assertEqual(c1['record_status'], 'INSUFFICIENT_HISTORY')
        for b in c1['barrels'].values():
            self.assertNotEqual(b['top']['status'], 'PREDICTION_AVAILABLE')
            self.assertNotEqual(b['worst']['status'], 'PREDICTION_AVAILABLE')

    def test_diagnostic_only_product_through_the_library(self):
        """E2R-R41/R62: a C2-only request works in the shared runner; only the command line lacks the option."""
        d, res = self.probe(product='DIAGNOSTIC_OUTPUT')
        self.assertEqual((res.outcome, res.reason), ('SUCCESS', 'PUBLISHED: DIAGNOSTIC_ONLY'))
        self.assertEqual(self.files(res.folder), ['diagnostic.json', 'diagnostic_receipt.json', 'terminal.json'])


class AtomicCreateOnly(Base):
    """E2RC2-C01: publication never replaces a file, also under concurrent writers."""

    def test_existing_target_is_refused_and_untouched(self):
        target = self.td / 'f.json'
        target.write_bytes(b'original')
        with self.assertRaises(FileExistsError):
            CP.create_only(target, b'new')
        self.assertEqual(target.read_bytes(), b'original')
        self.assertEqual(sorted(p.name for p in self.td.iterdir()), ['f.json'])

    def test_dangling_symlink_target_is_refused(self):
        target = self.td / 'g.json'
        try:
            target.symlink_to(self.td / 'nowhere')
        except (OSError, NotImplementedError):
            self.skipTest('platform disallows symlinks')
        with self.assertRaises(FileExistsError):
            CP.create_only(target, b'new')
        self.assertFalse((self.td / 'nowhere').exists())

    def test_concurrent_writers_exactly_one_wins(self):
        import threading
        target = self.td / 'h.json'
        n = 12
        barrier = threading.Barrier(n)
        results = [None] * n

        def writer(i):
            barrier.wait()
            try:
                CP.create_only(target, f'writer {i}\n'.encode('ascii'))
                results[i] = 'won'
            except FileExistsError:
                results[i] = 'refused'
        threads = [threading.Thread(target=writer, args=(i,)) for i in range(n)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        self.assertEqual(results.count('won'), 1)
        self.assertEqual(results.count('refused'), n - 1)
        self.assertEqual(target.read_bytes(), f'writer {results.index("won")}\n'.encode('ascii'))
        self.assertEqual(sorted(p.name for p in self.td.iterdir()), ['h.json'])   # every temporary removed

    def test_no_hard_links_means_no_publication(self):
        target = self.td / 'k.json'
        with mock.patch.object(CP.os, 'link', side_effect=OSError('no hard links on this filesystem')):
            with self.assertRaises(RuntimeError):
                CP.create_only(target, b'x')
        self.assertEqual(sorted(p.name for p in self.td.iterdir()), [])

class NoCallerChosenAuthority(Base):
    """E2RC2-CODE-B01 and B02: the public APIs take no orphan-marker, registry or method-folder locator
    and no execution path; a genuine marker and a withdrawn or flagged variant always refuse."""

    def test_public_signatures(self):
        import inspect
        from _common import contract_dispatch as D
        from coordinator_private.contract_coordinated_gate import gate_coordinated_contract_request
        forbidden = {'orphan_marker', 'data_root', 'methods_root', 'execution_path', 'gates_pass', 'marker',
                     'registry', 'root'}
        for fn in (CR.run_contract_method, read_run, D.dispatch_gate, D.legacy_gate, D.variant_released,
                   D.active_pins, gate_coordinated_contract_request):
            with self.subTest(fn=fn.__name__):
                self.assertFalse(set(inspect.signature(fn).parameters) & forbidden)
        self.assertNotIn('execution_path', inspect.signature(RunPublication).parameters)

    def test_locator_arguments_are_refused(self):
        req, d, res = self.run_e1('POWERBALL', 1300)
        for kw in ({'orphan_marker': self.td / 'elsewhere'}, {'data_root': self.td}, {'methods_root': self.td},
                   {'execution_path': 'COORDINATED'}):
            with self.subTest(kw=kw), self.assertRaises(TypeError):
                CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=self.td / 'ws',
                                       run_root=self.td / 'other_runs', **kw)
            with self.subTest(kw=kw, api='read_run'), self.assertRaises(TypeError):
                read_run(res.folder, **kw)
        self.assertFalse((self.td / 'other_runs').exists())

    def test_a_genuine_marker_always_refuses(self):
        req, d, res = self.run_e1('POWERBALL', 1300)
        self.marker.write_text('{}')            # the marker at the (patched) fixed location
        with self.assertRaises(CR.RunRefused):
            self.run_e1('POWERBALL', 1300, ws_name='ws2')
        self.assertEqual(self.consumed(res.folder)['forecast'], (False, 'UNRESOLVED_ORPHAN_MARKER'))

    def test_every_run_is_standalone(self):
        req, d, res = self.run_e1('OZLOTTO', 1600)
        for name in ('terminal.json', 'forecast_receipt.json'):
            self.assertEqual(json.loads((res.folder / name).read_bytes())['execution_path'], 'STANDALONE')

    def test_data_source_is_fixed(self):
        """A synthetic run cannot read the project, and a real run (if the switch were on) only the project."""
        e, d = e1_pins('POWERBALL')
        req = C.request(d, e, 1300, '0' * 64)
        with self.assertRaises(CR.RunRefused) as cm:
            CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=CR.PROJECT_ROOT,
                                   run_root=self.td / 'runs')
        self.assertEqual(cm.exception.reason, 'DATA_SOURCE_REFUSED')
        real = F.request(d, 1300, 'UNORDERED_SET', run_mode='REAL_DEVELOPMENT', entry_digest=record_digest(e))
        with mock.patch.object(CR, 'ENABLE_CONTRACT_REAL_DEVELOPMENT', True), \
                mock.patch.object(CR, 'load_pinned_draw_view', side_effect=AssertionError('data read')):
            with self.assertRaises(CR.RunRefused) as cm:
                CR.run_contract_method(real, compute=e_001.compute, verify=e_001.verify, repo_root=self.td,
                                       run_root=self.td / 'runs')
        self.assertEqual(cm.exception.reason, 'DATA_SOURCE_REFUSED')
        self.assertFalse((self.td / 'runs').exists())

if __name__ == '__main__':
    unittest.main()
