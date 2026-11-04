"""MHUP-A slice 1: the structural, publication and data-admission gates (design v0.1r5 section 3.4; Appendix L: L-G, L-G1,
L-I2 for barrier P). OFFLINE: invented masters, synthetic owner records, plans, tickets and markers in a temporary
project; the runner's PROJECT_ROOT, the orphan marker, the installed-data root and the dispatch gate's PROJECT_ROOT
are patched to it in-process (the test harness only; the production APIs take no such argument).

Every rule is refused once: an unbound request that needs a binding; a forged binding digest; a request without a
ticket; a request reusing a run id that a resume marked FAILED_TO_START; a second request for a pair with a DONE
ticket (in this and in another session's ledger); a request for a target with a freeze line; a request after each
lifecycle marker; a REAL_HOLDOUT request before any plan; a REAL_DEVELOPMENT request for a holdout target without the
seal; a stale pin; barrier P. And the happy paths: a ticketed REAL_HOLDOUT run on an opened synthetic game publishes
a HOLDOUT_MODE_H record; a diagnostic run publishes under the diagnostic root only; the standalone launcher's
new command-line rules.
"""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import e2r_code2_fixtures as C
import e2r_fixtures as F
import mhupa_fixtures as X
import _common.contract_dispatch as CD
import _common.contract_registry as REG
import _common.contract_runner as CR
import _common.contract_vocab as V
from _common.contract_records import record_digest, validate_run_request
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from _common import owner_records as OR
from contract_adapters import e_001

BATCH = 'wf-' + 'a' * 32
SESSION = 'b' * 32
RUN = 'mg-' + 'c' * 32


def e1_pins(game):
    reg = InstalledRegistry()
    e = reg.active_entry(game, *C.E1)
    return e, reg.declaration(e['declaration_digest'])


def request(game, target, *, mode, run_id=RUN, binding=None, version, sha):
    e, d = e1_pins(game)
    product = {'REAL_HOLDOUT': 'WF_FORECAST', 'REAL_DEVELOPMENT': 'WF_FORECAST'}.get(mode, 'SYNTHETIC_TEST_OUTPUT')
    r = F.request(d, target, 'UNORDERED_SET', run_mode=mode, product=product, sha=sha, run_id=run_id,
                  entry_digest=record_digest(e))
    r['ledger_version'] = version
    if binding is not None:
        r['binding'] = binding
    return r


class Structural(unittest.TestCase):
    """Design 3.4(a): which modes may name which targets, and which binding each needs (no file is read)."""

    def test_mode_target_binding_rules(self):
        p = POWERBALL
        sha = 'f' * 64
        ok = lambda **kw: validate_run_request(request('POWERBALL', version=1, sha=sha, **kw))
        bad = lambda **kw: self.assertRaises(ValueError, validate_run_request, request('POWERBALL', version=1, sha=sha, **kw))
        plan_b = {'kind': 'MODE_H_BATCH', 'batch_id': BATCH, 'plan_digest': 'd' * 64, 'run_id': RUN}
        sess_b = {'kind': 'WEEKLY_SESSION', 'session_id': SESSION, 'session_digest': 'd' * 64, 'run_id': RUN}
        # synthetic: within the prefix, no binding
        ok(target=1300, mode='SYNTHETIC_CONTRACT_TEST')
        bad(target=p.holdout_first, mode='SYNTHETIC_CONTRACT_TEST')
        bad(target=1300, mode='SYNTHETIC_CONTRACT_TEST', binding=X.DIAGNOSTIC)
        # REAL_DEVELOPMENT: within the prefix unbound or diagnostic; above it a session (after the holdout) or diagnostic
        ok(target=1300, mode='REAL_DEVELOPMENT')
        ok(target=1300, mode='REAL_DEVELOPMENT', binding=X.DIAGNOSTIC)
        bad(target=1300, mode='REAL_DEVELOPMENT', binding=sess_b)
        bad(target=p.holdout_first, mode='REAL_DEVELOPMENT')
        ok(target=p.holdout_first, mode='REAL_DEVELOPMENT', binding=X.DIAGNOSTIC)
        bad(target=p.holdout_first, mode='REAL_DEVELOPMENT', binding=sess_b)
        ok(target=p.holdout_last + 1, mode='REAL_DEVELOPMENT', binding=sess_b)
        bad(target=p.holdout_last + 1, mode='REAL_DEVELOPMENT', binding=plan_b)
        # REAL_HOLDOUT: holdout targets only, Mode H binding only
        ok(target=p.holdout_first, mode='REAL_HOLDOUT', binding=plan_b)
        ok(target=p.holdout_last, mode='REAL_HOLDOUT', binding=plan_b)
        bad(target=p.holdout_first, mode='REAL_HOLDOUT')
        bad(target=p.holdout_first - 1, mode='REAL_HOLDOUT', binding=plan_b)
        bad(target=p.holdout_last + 1, mode='REAL_HOLDOUT', binding=plan_b)
        bad(target=p.holdout_first, mode='REAL_HOLDOUT', binding=sess_b)
        bad(target=p.holdout_first, mode='REAL_HOLDOUT', binding=X.DIAGNOSTIC)
        # the binding's own shape: a wrong run id, a bad batch id, an unknown kind, an extra field
        bad(target=p.holdout_first, mode='REAL_HOLDOUT', binding=dict(plan_b, run_id='mg-' + 'e' * 32))
        bad(target=p.holdout_first, mode='REAL_HOLDOUT', binding=dict(plan_b, batch_id='wf-short'))
        bad(target=p.holdout_first, mode='REAL_HOLDOUT', binding=dict(plan_b, kind='SOMETHING'))
        bad(target=p.holdout_first, mode='REAL_HOLDOUT', binding=dict(plan_b, extra=1))
        bad(target=1300, mode='REAL_DEVELOPMENT', binding={'kind': 'OWNER_DIAGNOSTIC', 'run_id': RUN})
        # the ledger version: any positive version; zero refused
        ok(target=1300, mode='REAL_DEVELOPMENT')
        validate_run_request(request('POWERBALL', 1300, mode='REAL_DEVELOPMENT', version=7, sha=sha))
        with self.assertRaises(ValueError):
            validate_run_request(request('POWERBALL', 1300, mode='REAL_DEVELOPMENT', version=0, sha=sha))
        # FINAL_NEXT_DRAW stays reserved in this package (no producible product), whatever its binding
        with self.assertRaises(ValueError):
            V.producible('FINAL_NEXT_DRAW', V.FORECAST)
        self.assertEqual(V.producible('REAL_HOLDOUT', V.FORECAST), ('WF_FORECAST', 'HOLDOUT_MODE_H'))
        with self.assertRaises(ValueError):
            V.producible('REAL_HOLDOUT', V.DIAGNOSTIC)


class Project(unittest.TestCase):
    """A temporary project: invented masters grown past the holdout for both games, the runner and gate roots patched."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.td = Path(self._td.name)
        self.proj = self.td / 'project'
        self.rows = {}
        for p in (POWERBALL, OZLOTTO):
            self.rows[p.game_id] = X.grow_master(self.proj, p, [list(range(p.holdout_first, p.holdout_last + 2))])
        self.marker = self.proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        self.data = C.copy_data_root(self.td)
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(mock.patch.object(CR, 'PROJECT_ROOT', self.proj))
        self.stack.enter_context(mock.patch.object(CR, 'ORPHAN_MARKER', self.marker))
        self.stack.enter_context(mock.patch.object(CD, 'PROJECT_ROOT', self.proj))
        self.stack.enter_context(mock.patch.object(REG, 'DATA_ROOT', self.data))

    def tearDown(self):
        self.stack.close()
        self._td.cleanup()

    def v2(self, game):
        return 2, self.rows[game][1]['master_sha256']

    def opened(self, game):
        return X.write_opening_record(self.proj, game, freeze_version=1, freeze_sha=self.rows[game][0]['master_sha256'])

    def plan_for(self, game, targets=None):
        e, _d = e1_pins(game)
        p = get_profile(game)
        cohort = [{'method_id': 'E_1', 'variant_id': C.E1[1], 'method_revision': e['method_revision'],
                   'declaration_digest': e['declaration_digest'], 'registry_entry_digest': record_digest(e)}]
        return X.write_mode_h_plan(self.proj, game, BATCH, cohort, targets or list(range(p.holdout_first, p.holdout_last + 1)))

    def holdout_request(self, game, target, plan, run_id=RUN):
        v, sha = self.v2(game)
        return request(game, target, mode='REAL_HOLDOUT', run_id=run_id, binding=X.binding_for_plan(plan, run_id),
                       version=v, sha=sha)

    def attempts(self, game):
        return OR.mode_h_batch_folder(self.proj, game, BATCH) / 'attempts.jsonl'

    def refused(self, req, code):
        with self.assertRaises(CD.DispatchRefused) as cm:
            CD.dispatch_gate(req)
        self.assertEqual(cm.exception.reason, code, cm.exception.text)
        self.assertNotIn(str(self.proj), cm.exception.text)

    def launch(self, req, run_root=None):
        kind = req.get('binding', {}).get('kind')
        if run_root is None:
            run_root = {'MODE_H_BATCH': OR.mode_h_runs_root(self.proj), 'OWNER_DIAGNOSTIC': OR.diagnostic_runs_root(self.proj),
                        'WEEKLY_SESSION': OR.weekly_runs_root(self.proj)}.get(kind, self.proj / 'results' / 'real' / 'development' / 'contract_runs')
        return CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=self.proj, run_root=run_root)


class ModeHBinding(Project):
    """Design 3.4(b), the Mode H binding, on Powerball and Oz Lotto."""

    def test_the_full_ticketed_path_publishes_a_holdout_record(self):
        for game in ('POWERBALL', 'OZLOTTO'):
            p = get_profile(game)
            self.opened(game)
            plan = self.plan_for(game)
            req = self.holdout_request(game, p.holdout_first, plan)
            X.open_ticket(self.attempts(game), req, scope_kind='MODE_H_BATCH', scope_id=BATCH)
            entry, decl = CD.dispatch_gate(req)
            self.assertEqual(entry['method_revision'], '3')
            res = self.launch(req)
            self.assertEqual(res.outcome, 'SUCCESS', res.reason)
            rec = json.loads((res.folder / 'forecast.json').read_bytes())
            receipt = json.loads((res.folder / 'forecast_receipt.json').read_bytes())
            self.assertEqual((rec['run_mode'], rec['product_kind'], rec['target_draw_number']),
                             ('REAL_HOLDOUT', 'WF_FORECAST', p.holdout_first))
            self.assertEqual((receipt['evidence_tier'], receipt['ledger_version']), ('HOLDOUT_MODE_H', 2))
            self.assertTrue(res.folder.is_relative_to(OR.mode_h_runs_root(self.proj)))
            # the record names only draws before its target
            self.assertEqual(rec['training_last_draw_number'], p.holdout_first - 1)

    def test_refusals_one_per_rule(self):
        game, p = 'POWERBALL', POWERBALL
        v, sha = self.v2(game)
        # REAL_HOLDOUT before any plan (and before the opening record): no plan resolves
        plan_b = {'kind': 'MODE_H_BATCH', 'batch_id': BATCH, 'plan_digest': 'd' * 64, 'run_id': RUN}
        self.refused(request(game, p.holdout_first, mode='REAL_HOLDOUT', binding=plan_b, version=v, sha=sha), 'BINDING_NOT_RESOLVED')
        plan = self.plan_for(game)
        good = self.holdout_request(game, p.holdout_first, plan)
        # a forged plan digest
        self.refused(dict(good, binding=dict(good['binding'], plan_digest='0' * 64)), 'BINDING_NOT_RESOLVED')
        # a pair the plan does not list (another target)
        other = self.holdout_request(game, p.holdout_last + 1, plan)
        other['run_mode'], other['product_kind'] = 'REAL_HOLDOUT', 'WF_FORECAST'
        with self.assertRaises(CD.DispatchRefused):                     # structurally outside the holdout
            CD.dispatch_gate(other)
        narrow = self.plan_for(game, targets=[p.holdout_first + 1])
        self.refused(self.holdout_request(game, p.holdout_first, narrow), 'PAIR_NOT_IN_PLAN')
        plan = X.write_mode_h_plan(self.proj, game, BATCH, narrow['cohort'], list(range(p.holdout_first, p.holdout_last + 1)))
        good = self.holdout_request(game, p.holdout_first, plan)
        # no ticket at all
        self.refused(good, 'NO_OPEN_TICKET')
        # a ticket for another request (a different run id)
        X.open_ticket(self.attempts(game), dict(good, run_id='mg-' + 'd' * 32, binding=dict(good['binding'], run_id='mg-' + 'd' * 32)),
                      scope_kind='MODE_H_BATCH', scope_id=BATCH)
        self.refused(good, 'NO_OPEN_TICKET')
        # a ticket for this run id and pair, but for another request (its digest differs)
        X.open_ticket(self.attempts(game), dict(good, include_dates=not good['include_dates']),
                      scope_kind='MODE_H_BATCH', scope_id=BATCH)
        self.refused(good, 'NO_OPEN_TICKET')
        # the right ticket, but the holdout is not opened
        X.open_ticket(self.attempts(game), good, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        self.refused(good, 'HOLDOUT_NOT_OPENED')
        self.opened(game)
        CD.dispatch_gate(good)                                            # admitted now
        # a run id a resume marked FAILED_TO_START is never reused
        X.failed_to_start_ticket(self.attempts(game), good, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        self.refused(good, 'NO_OPEN_TICKET')
        # a second request for a pair with a DONE ticket
        again = dict(good, run_id='mg-' + 'e' * 32, binding=dict(good['binding'], run_id='mg-' + 'e' * 32))
        X.open_ticket(self.attempts(game), again, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        CD.dispatch_gate(again)
        X.done_ticket(self.attempts(game), again, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        third = dict(good, run_id='mg-' + 'f' * 32, binding=dict(good['binding'], run_id='mg-' + 'f' * 32))
        X.open_ticket(self.attempts(game), third, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        self.refused(third, 'PAIR_ALREADY_DONE')
        # another pair is still fine, until a lifecycle marker appears
        t2 = self.holdout_request(game, p.holdout_first + 1, plan, run_id='mg-' + '1' * 32)
        X.open_ticket(self.attempts(game), t2, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        CD.dispatch_gate(t2)
        for marker in OR.LIFECYCLE_MARKERS:
            X.write_marker(self.proj, game, BATCH, marker)
            self.refused(t2, 'BATCH_CLOSED')
            (OR.mode_h_batch_folder(self.proj, game, BATCH) / f'{marker}.json').unlink()
        CD.dispatch_gate(t2)
        # a plan that is not the game's one plan (another batch id)
        X.write_mode_h_plan(self.proj, game, 'wf-' + '9' * 32, plan['cohort'], plan['targets'])     # moves the batch-id record
        self.refused(t2, 'BINDING_NOT_RESOLVED')

    def test_an_unbound_holdout_request_never_reaches_the_gate_and_an_old_pin_is_stale(self):
        game, p = 'POWERBALL', POWERBALL
        self.opened(game)
        plan = self.plan_for(game)
        v, sha = self.v2(game)
        unbound = request(game, p.holdout_first, mode='REAL_HOLDOUT', version=v, sha=sha)
        with self.assertRaises(CD.DispatchRefused) as cm:
            CD.dispatch_gate(unbound)
        self.assertEqual(cm.exception.reason, 'INVALID_RUN_REQUEST')
        with self.assertRaises(CD.DispatchRefused):
            self.launch(unbound)
        self.assertFalse(OR.mode_h_runs_root(self.proj).exists())        # nothing published
        # a bound request pinning version 1 while the ledger's last row is version 2: admitted by the gate (it reads no
        # ledger), refused at data admission as STALE_PIN, with a terminal record and no forecast
        stale = request(game, p.holdout_first, mode='REAL_HOLDOUT', binding=X.binding_for_plan(plan, RUN), version=1,
                        sha=self.rows[game][0]['master_sha256'])
        X.open_ticket(self.attempts(game), stale, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        res = self.launch(stale)
        self.assertEqual(res.outcome, 'VALIDATION_FAILURE')
        self.assertIn('STALE_PIN', res.reason)
        self.assertFalse((res.folder / 'forecast.json').exists())

    def test_the_plan_pin_is_the_ledgers_current_row(self):
        """walk_forward.ledger_pin (design 3.2): a new batch pins the current last row, both games."""
        import _common.walk_forward as WF
        for game in ('POWERBALL', 'OZLOTTO'):
            self.assertEqual(WF.ledger_pin(game), (2, self.rows[game][1]['master_sha256']))

    def test_the_wrong_publication_root_is_refused_before_anything_is_read(self):
        game, p = 'POWERBALL', POWERBALL
        self.opened(game)
        plan = self.plan_for(game)
        req = self.holdout_request(game, p.holdout_first, plan)
        X.open_ticket(self.attempts(game), req, scope_kind='MODE_H_BATCH', scope_id=BATCH)
        with self.assertRaises(CR.RunRefused) as cm:
            self.launch(req, run_root=self.proj / 'results' / 'real' / 'development' / 'contract_runs')
        self.assertEqual(cm.exception.reason, 'DATA_SOURCE_REFUSED')
        with self.assertRaises(CR.RunRefused):                          # and never a workspace outside the project
            CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=self.td / 'elsewhere',
                                   run_root=OR.mode_h_runs_root(self.proj))


class BarrierP(Project):
    """Appendix J (L-I2): while INSTALL_IN_PROGRESS.txt exists every dispatch-gated run refuses, bound or not."""

    def test_everything_refuses_while_the_barrier_exists(self):
        barrier = OR.barrier_path(self.data)
        e, d = e1_pins('POWERBALL')
        synthetic = C.request(d, e, 1300, 'f' * 64)
        CD.dispatch_gate(synthetic)
        barrier.write_text('INSTALL MHUP_A test\n')
        self.refused(synthetic, 'INSTALL_IN_PROGRESS')
        with self.assertRaises(CD.DispatchRefused) as cm:                 # the legacy runner's gate too
            CD.legacy_gate('POWERBALL', *C.E1, '3')
        self.assertEqual(cm.exception.reason, 'INSTALL_IN_PROGRESS')
        barrier.unlink()
        CD.dispatch_gate(synthetic)


class DiagnosticRoute(Project):
    """Design 3.4, decision MHUP-Q11: the owner's unofficial re-test route."""

    def test_diagnostic_runs(self):
        game, p = 'POWERBALL', POWERBALL
        v, sha = self.v2(game)
        # a development-prefix target: admitted without any record, published under the diagnostic root only
        req = request(game, 1300, mode='REAL_DEVELOPMENT', binding=X.DIAGNOSTIC, version=v, sha=sha)
        res = self.launch(req)
        self.assertEqual(res.outcome, 'SUCCESS', res.reason)
        self.assertTrue(res.folder.is_relative_to(OR.diagnostic_runs_root(self.proj)))
        with self.assertRaises(CR.RunRefused):                          # not under the development root
            self.launch(dict(req, run_id='mg-' + '2' * 32), run_root=self.proj / 'results' / 'real' / 'development' / 'contract_runs')
        # a holdout target: needs the opening record and the seal
        hold = request(game, p.holdout_first, mode='REAL_DEVELOPMENT', run_id='mg-' + '7' * 32, binding=X.DIAGNOSTIC,
                       version=v, sha=sha)
        self.refused(hold, 'HOLDOUT_NOT_OPENED')
        self.opened(game)
        self.refused(hold, 'MODE_H_NOT_SEALED')
        self.plan_for(game)
        self.refused(hold, 'MODE_H_NOT_SEALED')
        X.write_marker(self.proj, game, BATCH, 'SCORE_COMPLETE')          # another lifecycle marker is not the seal
        self.refused(hold, 'MODE_H_NOT_SEALED')
        X.write_marker(self.proj, game, BATCH, 'MODE_H_SEALED')
        res = self.launch(hold)
        self.assertEqual(res.outcome, 'SUCCESS', res.reason)
        rec = json.loads((res.folder / 'forecast.json').read_bytes())
        self.assertEqual((rec['run_mode'], rec['target_draw_number']), ('REAL_DEVELOPMENT', p.holdout_first))
        # the diagnostic route admits REAL_DEVELOPMENT only
        self.refused(dict(hold, run_mode='SYNTHETIC_CONTRACT_TEST', product_kind='SYNTHETIC_TEST_OUTPUT'), 'INVALID_RUN_REQUEST')


class SessionBinding(Project):
    """Design 3.4(b), the session binding, with synthetic session records (the writers arrive with MHUP-B)."""

    def session(self, game, release_date):
        e, _d = e1_pins(game)
        roster = [{'method_id': 'E_1', 'variant_id': C.E1[1], 'method_revision': e['method_revision'],
                   'release_date': release_date}]
        return X.write_session(self.proj, game, SESSION, roster)

    def dev_request(self, game, target, session, run_id=RUN):
        v, sha = self.v2(game)
        return request(game, target, mode='REAL_DEVELOPMENT', run_id=run_id, binding=X.binding_for_session(session, run_id),
                       version=v, sha=sha)

    def test_session_rules(self):
        game, p = 'POWERBALL', POWERBALL
        target = p.holdout_last + 1
        sess = self.session(game, release_date=p.derived_date(target).isoformat())   # released ON the draw date: development
        req = self.dev_request(game, target, sess)
        self.refused(dict(req, binding=dict(req['binding'], session_digest='0' * 64)), 'BINDING_NOT_RESOLVED')
        self.refused(req, 'NOT_DEVELOPED')
        X.write_developed_record(self.proj, game)
        self.refused(req, 'NO_OPEN_TICKET')
        path = OR.session_attempts_path(self.proj, game, SESSION)
        X.open_ticket(path, req, scope_kind='WEEKLY_SESSION', scope_id=SESSION)
        CD.dispatch_gate(req)
        # a freeze line for the target closes it
        X.write_freeze_line(self.proj, game, target)
        self.refused(req, 'TARGET_FROZEN')
        OR.forecast_ledger_path(self.proj, game).unlink()
        # a DONE ticket for the pair in ANOTHER session's ledger
        other = 'e' * 32
        X.done_ticket(OR.session_attempts_path(self.proj, game, other), dict(req, run_id='mg-' + '3' * 32),
                      scope_kind='WEEKLY_SESSION', scope_id=other)
        self.refused(req, 'PAIR_ALREADY_DONE')
        OR.session_attempts_path(self.proj, game, other).unlink()
        CD.dispatch_gate(req)
        # a variant released before the draw date may not publish a development record for it
        early = self.session(game, release_date=p.derived_date(target - 1).isoformat())   # one draw before: a forecast
        req2 = self.dev_request(game, target, early, run_id='mg-' + '4' * 32)
        X.open_ticket(path, req2, scope_kind='WEEKLY_SESSION', scope_id=SESSION)
        self.refused(req2, 'MODE_DISAGREES_WITH_RELEASE')
        # a variant not in the roster
        sess3 = X.write_session(self.proj, game, SESSION, [])
        req3 = self.dev_request(game, target, sess3, run_id='mg-' + '5' * 32)
        X.open_ticket(path, req3, scope_kind='WEEKLY_SESSION', scope_id=SESSION)
        self.refused(req3, 'NOT_IN_SESSION_ROSTER')
        # the happy path publishes under the weekly root with the right pins
        sess4 = self.session(game, release_date=p.derived_date(target).isoformat())
        req4 = self.dev_request(game, target, sess4, run_id='mg-' + '6' * 32)
        X.open_ticket(path, req4, scope_kind='WEEKLY_SESSION', scope_id=SESSION)
        X.write_opening_record(self.proj, game, freeze_version=1, freeze_sha=self.rows[game][0]['master_sha256'])
        res = self.launch(req4)
        self.assertEqual(res.outcome, 'SUCCESS', res.reason)
        self.assertTrue(res.folder.is_relative_to(OR.weekly_runs_root(self.proj)))


class Launcher(Project):
    """Method_Contract_Runner.py (design 3.4, decision MHUP-Q11): --ledger-version is required; REAL_HOLDOUT,
    FINAL_NEXT_DRAW and CATCH_UP are refused at the command line (no binding or ticket is issued there); --binding
    OWNER_DIAGNOSTIC publishes a REAL_DEVELOPMENT run under the diagnostic root; a synthetic run takes no binding."""

    def cli(self, game, target, mode, *extra):
        e, _d = e1_pins(game)
        v, sha = self.v2(game)
        return ['run', '--game', game, '--method', 'E_1', '--variant', C.E1[1], '--revision', e['method_revision'],
                '--target', str(target), '--view', 'UNORDERED_SET', '--mode', mode,
                '--declaration-digest', e['declaration_digest'], '--registry-entry-digest', record_digest(e),
                '--master-sha256', sha, '--ledger-version', str(v), *extra]

    def main(self, args):
        import Method_Contract_Runner as M
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = M.main(args)
            except SystemExit as exc:
                code = exc.code
        return code, out.getvalue(), err.getvalue()

    def test_command_line_rules(self):
        game, p = 'POWERBALL', POWERBALL
        for mode, target in (('REAL_HOLDOUT', p.holdout_first), ('FINAL_NEXT_DRAW', p.holdout_last + 1),
                             ('CATCH_UP', p.holdout_last + 1)):
            code, out, err = self.main(self.cli(game, target, mode))
            self.assertEqual((code, out), (2, ''), err)
            self.assertIn('DISPATCH REFUSED', err)
            self.assertIn('No data was read', err)
        self.assertFalse((self.proj / 'results').exists())
        # --ledger-version is required
        args = self.cli(game, 1300, 'REAL_DEVELOPMENT', '--binding', 'OWNER_DIAGNOSTIC')
        i = args.index('--ledger-version')
        code, _out, err = self.main(args[:i] + args[i + 2:])
        self.assertEqual(code, 2)
        self.assertIn('--ledger-version', err)
        # a synthetic run takes no binding
        ws, wsha = C.workspace(self.td / 'ws', game, 1300)
        code, _out, err = self.main(self.cli(game, 1300, 'SYNTHETIC_CONTRACT_TEST', '--workspace', str(ws), '--binding',
                                             'OWNER_DIAGNOSTIC'))
        self.assertEqual(code, 2)
        self.assertIn('--binding is for real runs only', err)
        self.assertFalse((ws / 'contract_runs').exists())
        # the diagnostic route publishes under the diagnostic root
        code, out, err = self.main(self.cli(game, 1300, 'REAL_DEVELOPMENT', '--binding', 'OWNER_DIAGNOSTIC'))
        self.assertEqual(code, 0, err)
        folder = Path(out.splitlines()[1].split('folder=', 1)[1])
        self.assertTrue(folder.is_relative_to(OR.diagnostic_runs_root(self.proj).resolve()))
        self.assertFalse((self.proj / 'results' / 'real' / 'development').exists())
        # without the binding, the development root as before
        code, out, err = self.main(self.cli(game, 1300, 'REAL_DEVELOPMENT'))
        self.assertEqual(code, 0, err)
        folder = Path(out.splitlines()[1].split('folder=', 1)[1])
        self.assertTrue(folder.is_relative_to((self.proj / 'results' / 'real' / 'development' / 'contract_runs').resolve()))


class TicketsAndRecords(unittest.TestCase):
    """owner_records: tickets, the torn-last-line rule, and the opening record's fields."""

    def test_tickets_and_torn_lines(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'attempts.jsonl'
            e, d = e1_pins('POWERBALL')
            req = C.request(d, e, 1300, 'f' * 64)
            t = X.open_ticket(path, req, scope_kind='MODE_H_BATCH', scope_id=BATCH)
            rows = OR.tickets(path, scope_kind='MODE_H_BATCH', scope_id=BATCH, game_id='POWERBALL')
            self.assertEqual(rows, [t])
            with path.open('ab') as fh:
                fh.write(b'{"schema": "TICKET_V1", "kind": "DONE"')          # a torn last line
            rows2, torn = OR.read_jsonl(path)
            self.assertEqual((len(rows2), torn), (1, True))
            self.assertEqual(OR.tickets(path, scope_kind='MODE_H_BATCH', scope_id=BATCH, game_id='POWERBALL'), [t])
            with self.assertRaises(OR.RecordRefused):                     # another scope's ticket is refused, not ignored
                OR.tickets(path, scope_kind='WEEKLY_SESSION', scope_id=BATCH, game_id='POWERBALL')
            with self.assertRaises(ValueError):
                OR.ticket('CLOSED', scope_kind='MODE_H_BATCH', scope_id=BATCH, game_id='POWERBALL', method_id='E_1',
                          variant_id='V', method_revision='3', target_draw_number=1, run_id=RUN, utc='2026-11-14T10:00:00Z')

    def test_opening_record_fields(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.assertIsNone(OR.opening_record(root, 'POWERBALL'))
            rec = X.write_opening_record(root, 'POWERBALL', freeze_version=1, freeze_sha='a' * 64)
            self.assertEqual(OR.opening_record(root, 'POWERBALL')['freeze_version'], 1)
            for bad in (dict(rec, freeze_version=0), dict(rec, freeze_master_sha256='x'), {k: v for k, v in rec.items() if k != 'freeze_version'},
                        dict(rec, game='OZLOTTO'), dict(rec, schema='HOLDOUT_OPENED_V2'), dict(rec, owner_statement='')):
                OR.opening_record_path(root, 'POWERBALL').write_text(json.dumps(bad))
                with self.assertRaises(OR.RecordRefused, msg=bad):
                    OR.opening_record(root, 'POWERBALL')
            OR.opening_record_path(root, 'POWERBALL').write_text(json.dumps(rec))
            OR.study_manifest_path(root, 'POWERBALL').write_bytes(b'{"changed": true}')
            with self.assertRaises(OR.RecordRefused):
                OR.opening_record(root, 'POWERBALL')


if __name__ == '__main__':
    unittest.main()
