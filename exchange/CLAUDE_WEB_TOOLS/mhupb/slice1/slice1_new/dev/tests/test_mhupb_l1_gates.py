"""MHUP-B slice 1, layer L1: the weekly run modes and their gates (design v0.1r7 sections 3.4, 6.4 and Appendix E; code
plan v0.3 section 5, L1). OFFLINE: invented masters grown past the holdout, synthetic owner records, plans, tickets and
markers in a temporary project (the harness of test_mhupa_gates).

1. The vocabulary: CATCH_UP and FINAL_NEXT_DRAW are producible forecast rows with their own tiers and no diagnostic row;
   both need a session binding and a target after the holdout.
2. The gate matrix: every request row of Appendix E at every stage S0 to S5 and under each barrier (X). The expected
   cell is typed in below from Appendix E (TABLE) and cross-checked by ORACLE, a second "what should happen" function
   written from the design's rules and not from the gate's code (R-4); the actual result must equal both. A refused
   cell must leave the project's results untouched; a cell refused by the runner after the reader (STALE_PIN, MODE_PIN)
   leaves only its own failure terminal record, never a forecast.
3. The mode-to-pin rule (design 3.4(a); plan CF-2; EX_223 CP-Q9): REAL_DEVELOPMENT (session-bound), CATCH_UP,
   FINAL_NEXT_DRAW and the diagnostic route at last_draw(v), at last_draw(v) + 1 and beyond.
4. One data kind for every real mode (design 3.3): the same prefix gives the same ranking, tie order, selections and
   permitted-view digest in REAL_DEVELOPMENT, CATCH_UP and FINAL_NEXT_DRAW; only the mode, product and tier differ.
"""
from __future__ import annotations

import json
import unittest

import e2r_code2_fixtures as C
import e2r_fixtures as F
import mhupa_fixtures as X
import _common.contract_dispatch as CD
import _common.contract_runner as CR
import _common.contract_vocab as V
from _common.contract_forecast import validate_forecast
from _common.contract_records import record_digest, validate_run_request
from _common.contract_task import view_data_kind
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from _common import owner_records as OR
from test_mhupa_gates import BATCH, SESSION, Project, e1_pins

EXTRA = 3                                             # invented draws after the holdout that the master holds


def request(game, target, mode, *, run_id, binding=None, pin):
    e, d = e1_pins(game)
    r = F.request(d, target, 'UNORDERED_SET', run_mode=mode, product='WF_FORECAST', sha=pin[1], run_id=run_id,
                  entry_digest=record_digest(e))
    r['ledger_version'] = pin[0]
    if binding is not None:
        r['binding'] = binding
    return r


class Vocabulary(unittest.TestCase):

    def test_rows_tiers_and_sets(self):
        self.assertEqual(V.producible('FINAL_NEXT_DRAW', V.FORECAST), ('WF_FORECAST', 'PROSPECTIVE'))
        self.assertEqual(V.producible('CATCH_UP', V.FORECAST), ('WF_FORECAST', 'CATCH_UP'))
        for mode in V.WEEKLY_MODES:
            self.assertIn(mode, V.RUN_MODES)
            self.assertIn(mode, V.REAL_MODES)
            self.assertNotIn(mode, V.RESERVED_MODES)
            self.assertEqual(view_data_kind(mode), 'REAL_HISTORICAL_DEVELOPMENT')
            for schema in (V.DIAGNOSTIC, V.SCORE):
                with self.assertRaises(ValueError):
                    V.producible(mode, schema)
        self.assertEqual(V.WEEKLY_MODES, frozenset(('FINAL_NEXT_DRAW', 'CATCH_UP')))
        self.assertEqual(V.RESERVED_MODES, frozenset(('IN_SAMPLE_DIAGNOSTIC',)))
        self.assertIn('CATCH_UP', V.EVIDENCE_TIERS)
        with self.assertRaises(ValueError):
            V.producible('IN_SAMPLE_DIAGNOSTIC', V.FORECAST)

    def test_structural_rules_for_the_weekly_modes(self):
        sha, run = 'f' * 64, 'mg-' + 'c' * 32
        sess_b = {'kind': 'WEEKLY_SESSION', 'session_id': SESSION, 'session_digest': 'd' * 64, 'run_id': run}
        plan_b = {'kind': 'MODE_H_BATCH', 'batch_id': BATCH, 'plan_digest': 'd' * 64, 'run_id': run}
        for p in (POWERBALL, OZLOTTO):
            def ok(**kw):
                validate_run_request(request(p.game_id, run_id=run, pin=(2, sha), **kw))

            def bad(**kw):
                with self.assertRaises(ValueError, msg=kw):
                    validate_run_request(request(p.game_id, run_id=run, pin=(2, sha), **kw))
            for mode in sorted(V.WEEKLY_MODES):
                ok(target=p.holdout_last + 1, mode=mode, binding=sess_b)
                ok(target=p.holdout_last + 500, mode=mode, binding=sess_b)
                bad(target=p.holdout_last + 1, mode=mode)                               # unbound
                bad(target=p.holdout_last + 1, mode=mode, binding=plan_b)
                bad(target=p.holdout_last + 1, mode=mode, binding=X.DIAGNOSTIC)
                bad(target=p.holdout_last, mode=mode, binding=sess_b)                   # a holdout draw
                bad(target=p.holdout_first, mode=mode, binding=sess_b)
                bad(target=p.holdout_first - 1, mode=mode, binding=sess_b)              # the development prefix
                bad(target=p.holdout_last + 1, mode=mode, binding=dict(sess_b, run_id='mg-' + 'e' * 32))
                r = request(p.game_id, p.holdout_last + 1, mode, run_id=run, binding=sess_b, pin=(2, sha))
                for product in ('DIAGNOSTIC_OUTPUT', 'SYNTHETIC_TEST_OUTPUT', 'IS_DIAGNOSTIC_ENTRY'):
                    with self.assertRaises(ValueError):
                        validate_run_request(dict(r, product_kind=product))


# ---------------------------------------------------------------- the gate matrix (Appendix E)

STAGES = ('S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'X_ORPHAN', 'X_BARRIER')
P, R = 'PUBLISH', 'REFUSE'
# Each row: its attributes (read by ORACLE and by the builder) and, typed from Appendix E, its verdict per stage.
# zone: PREFIX, HOLDOUT, AFTER (a draw after the holdout that the pinned master holds) or NEXT (last_draw + 1).
# release: BEFORE or ON the target's draw date (session rows). pin: CURRENT or STALE. ticket: OPEN, NONE or DONE.
ROWS = {
    'dev prefix, unbound':                 dict(mode='REAL_DEVELOPMENT', zone='PREFIX', bind=None),
    'dev after, session, ticketed, ON':    dict(mode='REAL_DEVELOPMENT', zone='AFTER', bind='SESSION', ticket='OPEN', release='ON'),
    'diagnostic prefix':                   dict(mode='REAL_DEVELOPMENT', zone='PREFIX', bind='DIAGNOSTIC'),
    'diagnostic holdout':                  dict(mode='REAL_DEVELOPMENT', zone='HOLDOUT', bind='DIAGNOSTIC'),
    'diagnostic after':                    dict(mode='REAL_DEVELOPMENT', zone='AFTER', bind='DIAGNOSTIC'),
    'dev after, unbound':                  dict(mode='REAL_DEVELOPMENT', zone='AFTER', bind=None),
    'dev after, session, no ticket':       dict(mode='REAL_DEVELOPMENT', zone='AFTER', bind='SESSION', ticket='NONE', release='ON'),
    'dev after, session, BEFORE':          dict(mode='REAL_DEVELOPMENT', zone='AFTER', bind='SESSION', ticket='OPEN', release='BEFORE'),
    'dev holdout, session':                dict(mode='REAL_DEVELOPMENT', zone='HOLDOUT', bind='SESSION', ticket='OPEN', release='ON'),
    'holdout, plan, ticketed':             dict(mode='REAL_HOLDOUT', zone='HOLDOUT', bind='PLAN', ticket='OPEN'),
    'holdout, plan, pair DONE':            dict(mode='REAL_HOLDOUT', zone='HOLDOUT', bind='PLAN', ticket='DONE'),
    'holdout, plan, no ticket':            dict(mode='REAL_HOLDOUT', zone='HOLDOUT', bind='PLAN', ticket='NONE'),
    'holdout, unbound':                    dict(mode='REAL_HOLDOUT', zone='HOLDOUT', bind=None),
    'holdout, plan, wrong digest':         dict(mode='REAL_HOLDOUT', zone='HOLDOUT', bind='PLAN', ticket='OPEN', forged=True),
    'holdout mode, prefix target':         dict(mode='REAL_HOLDOUT', zone='PREFIX', bind='PLAN', ticket='OPEN'),
    'catch-up, ticketed, BEFORE':          dict(mode='CATCH_UP', zone='AFTER', bind='SESSION', ticket='OPEN', release='BEFORE'),
    'final, ticketed':                     dict(mode='FINAL_NEXT_DRAW', zone='NEXT', bind='SESSION', ticket='OPEN', release='BEFORE'),
    'catch-up, stale pin':                 dict(mode='CATCH_UP', zone='AFTER', bind='SESSION', ticket='OPEN', release='BEFORE', pin='STALE'),
    'final, stale pin':                    dict(mode='FINAL_NEXT_DRAW', zone='NEXT', bind='SESSION', ticket='OPEN', release='BEFORE', pin='STALE'),
    'catch-up, release ON':                dict(mode='CATCH_UP', zone='AFTER', bind='SESSION', ticket='OPEN', release='ON'),
    'final, draw the master holds':        dict(mode='FINAL_NEXT_DRAW', zone='AFTER', bind='SESSION', ticket='OPEN', release='BEFORE'),
    'final, target has a freeze line':     dict(mode='FINAL_NEXT_DRAW', zone='NEXT', bind='SESSION', ticket='OPEN', release='BEFORE', frozen=True),
    'catch-up, target has a freeze line':  dict(mode='CATCH_UP', zone='AFTER', bind='SESSION', ticket='OPEN', release='BEFORE', frozen=True),
    'catch-up, unbound':                   dict(mode='CATCH_UP', zone='AFTER', bind=None),
    'final, unbound':                      dict(mode='FINAL_NEXT_DRAW', zone='NEXT', bind=None),
    'catch-up, no ticket':                 dict(mode='CATCH_UP', zone='AFTER', bind='SESSION', ticket='NONE', release='BEFORE'),
    'final, no ticket':                    dict(mode='FINAL_NEXT_DRAW', zone='NEXT', bind='SESSION', ticket='NONE', release='BEFORE'),
    'catch-up, holdout target':            dict(mode='CATCH_UP', zone='HOLDOUT', bind='SESSION', ticket='OPEN', release='BEFORE'),
    'final, holdout target':               dict(mode='FINAL_NEXT_DRAW', zone='HOLDOUT', bind='SESSION', ticket='OPEN', release='BEFORE'),
    'catch-up, pair DONE in another session': dict(mode='CATCH_UP', zone='AFTER', bind='SESSION', ticket='OPEN', release='BEFORE', done_elsewhere=True),
}
ALL_R = dict.fromkeys(STAGES, R)
ONLY_S5 = dict(ALL_R, S5=P)
TABLE = {
    'dev prefix, unbound':                 dict(S0=P, S1=P, S2=P, S3=P, S4=P, S5=P, X_ORPHAN=R, X_BARRIER=R),
    'dev after, session, ticketed, ON':    ONLY_S5,
    'diagnostic prefix':                   dict(S0=P, S1=P, S2=P, S3=P, S4=P, S5=P, X_ORPHAN=R, X_BARRIER=R),
    'diagnostic holdout':                  dict(ALL_R, S4=P, S5=P),
    'diagnostic after':                    dict(ALL_R, S4=P, S5=P),
    'dev after, unbound':                  ALL_R,
    'dev after, session, no ticket':       ALL_R,
    'dev after, session, BEFORE':          ALL_R,
    'dev holdout, session':                ALL_R,
    'holdout, plan, ticketed':             dict(ALL_R, S2=P),
    'holdout, plan, pair DONE':            ALL_R,
    'holdout, plan, no ticket':            ALL_R,
    'holdout, unbound':                    ALL_R,
    'holdout, plan, wrong digest':         ALL_R,
    'holdout mode, prefix target':         ALL_R,
    'catch-up, ticketed, BEFORE':          ONLY_S5,
    'final, ticketed':                     ONLY_S5,
    'catch-up, stale pin':                 ALL_R,
    'final, stale pin':                    ALL_R,
    'catch-up, release ON':                ALL_R,
    'final, draw the master holds':        ALL_R,
    'final, target has a freeze line':     ALL_R,
    'catch-up, target has a freeze line':  ALL_R,
    'catch-up, unbound':                   ALL_R,
    'final, unbound':                      ALL_R,
    'catch-up, no ticket':                 ALL_R,
    'final, no ticket':                    ALL_R,
    'catch-up, holdout target':            ALL_R,
    'final, holdout target':               ALL_R,
    'catch-up, pair DONE in another session': ALL_R,
}


def ORACLE(row: dict, stage: str) -> str:
    """What the design says should happen (3.4 and Appendix E), from the row's attributes and the stage's facts only."""
    if stage.startswith('X_'):
        return R                                                            # a barrier stops every dispatch-gated run
    n = int(stage[1])
    opened, plan, complete, sealed, developed = n >= 1, n >= 2, n >= 3, n >= 4, n >= 5
    mode, zone, bind = row['mode'], row['zone'], row['bind']
    if mode == 'REAL_DEVELOPMENT':
        if zone == 'PREFIX':
            return P if bind in (None, 'DIAGNOSTIC') else R                 # today's runs; the owner's re-test route
        if bind == 'DIAGNOSTIC':
            return P if opened and sealed else R                            # a sealed holdout is ordinary history
        if bind != 'SESSION' or zone != 'AFTER':
            return R
        return P if (developed and row['ticket'] == 'OPEN' and row['release'] == 'ON') else R
    if mode == 'REAL_HOLDOUT':
        ok = (zone == 'HOLDOUT' and bind == 'PLAN' and not row.get('forged') and row['ticket'] == 'OPEN'
              and opened and plan and not complete)
        return P if ok else R
    # the weekly modes
    if bind != 'SESSION' or zone not in ('AFTER', 'NEXT') or not developed or row['ticket'] != 'OPEN':
        return R
    if row.get('pin') == 'STALE' or row.get('frozen') or row.get('done_elsewhere'):
        return R
    if mode == 'CATCH_UP':
        return P if (zone == 'AFTER' and row['release'] == 'BEFORE') else R
    return P if zone == 'NEXT' else R                                        # FINAL_NEXT_DRAW: only last_draw(v) + 1


class GateMatrix(Project):

    def setUp(self):
        super().setUp()
        for p in (POWERBALL, OZLOTTO):
            self.rows[p.game_id] = X.grow_master(self.proj, p, [list(range(p.holdout_first, p.holdout_last + 1 + EXTRA))])
        self.n = 0

    def run_id(self):
        self.n += 1
        return f'mg-{self.n:032x}'

    def at_stage(self, game, stage):
        n = 5 if stage.startswith('X_') else int(stage[1])
        if n >= 1:
            self.opened(game)
        if n >= 2:
            self.plan = self.plan_for(game, manifest_sha=X.write_study_manifest(self.proj, game))
        for marker, need in (('BATCH_COMPLETE', 3), ('SCORING_STARTED', 4), ('SCORE_COMPLETE', 4), ('MODE_H_SEALED', 4)):
            if n >= need:
                X.write_marker(self.proj, game, BATCH, marker)
        if n >= 5:
            X.write_developed_record(self.proj, game)

    def build(self, game, row, stage):
        """The request of one cell, with the tickets, session record and freeze line the row says exist."""
        p = get_profile(game)
        last = p.holdout_last + EXTRA
        target = {'PREFIX': p.holdout_first - 3, 'HOLDOUT': p.holdout_first + 1, 'AFTER': p.holdout_last + 2,
                  'NEXT': last + 1}[row['zone']]
        rid, pin = self.run_id(), self.v2(game)
        if row['bind'] is None:
            return request(game, target, row['mode'], run_id=rid, pin=pin)
        if row['bind'] == 'DIAGNOSTIC':
            return request(game, target, row['mode'], run_id=rid, binding=X.DIAGNOSTIC, pin=pin)
        if row['bind'] == 'PLAN':
            plan = getattr(self, 'plan', None)
            binding = ({'kind': 'MODE_H_BATCH', 'batch_id': BATCH, 'plan_digest': '0' * 64, 'run_id': rid}
                       if plan is None or row.get('forged') else X.binding_for_plan(plan, rid))
            req = request(game, target, row['mode'], run_id=rid, binding=binding, pin=pin)
            path = OR.mode_h_batch_folder(self.proj, game, BATCH) / 'attempts.jsonl'
            if row['ticket'] in ('OPEN', 'DONE'):
                X.open_ticket(path, req, scope_kind='MODE_H_BATCH', scope_id=BATCH)
            if row['ticket'] == 'DONE':
                X.done_ticket(path, dict(req, run_id='mg-' + 'd' * 32), scope_kind='MODE_H_BATCH', scope_id=BATCH)
            return req
        e, _d = e1_pins(game)
        release = p.derived_date(target - 1 if row['release'] == 'BEFORE' else target).isoformat()
        sid = f'{self.n:032x}'
        sess = X.write_session(self.proj, game, sid, [{'method_id': 'E_1', 'variant_id': C.E1[1],
                               'method_revision': e['method_revision'], 'release_date': release}], pin=pin)
        req = request(game, target, row['mode'], run_id=rid, binding=X.binding_for_session(sess, rid), pin=pin)
        if row['ticket'] == 'OPEN':
            X.open_ticket(OR.session_attempts_path(self.proj, game, sid), req, scope_kind='WEEKLY_SESSION', scope_id=sid)
        if row.get('done_elsewhere'):
            other = 'e' * 32
            X.done_ticket(OR.session_attempts_path(self.proj, game, other), dict(req, run_id='mg-' + 'e' * 32),
                          scope_kind='WEEKLY_SESSION', scope_id=other)
        return req

    def snapshot(self):
        root = self.proj / 'results' / 'real'
        return sorted((str(f.relative_to(root)), f.read_bytes()) for f in root.rglob('*') if f.is_file()) \
            if root.exists() else []

    def cell(self, game, name, stage):
        """(verdict, code) of one cell. A PUBLISH is a consumable forecast in the right tier under the right root."""
        row = ROWS[name]
        req = self.build(game, row, stage)
        stale = row.get('pin') == 'STALE'
        if row.get('frozen'):
            X.write_freeze_line(self.proj, game, req['target_draw_number'])
        if stale:
            self.regrow3(game)
        if stage == 'X_ORPHAN':
            self.marker.parent.mkdir(parents=True, exist_ok=True)
            self.marker.write_text('{}')
        if stage == 'X_BARRIER':
            OR.barrier_path(self.data).write_text('install in progress')
        before = self.snapshot()
        try:
            res = self.launch(req)
        except (CD.DispatchRefused, CR.RunRefused) as exc:
            self.assertEqual(self.snapshot(), before, (name, stage))        # refused: not one byte written
            self.assertIn('No data was read', exc.text)
            out = (R, exc.reason)
        else:
            if res.outcome == 'SUCCESS':
                receipt = json.loads((res.folder / 'forecast_receipt.json').read_bytes())
                self.assertEqual(receipt['evidence_tier'], V.producible(row['mode'], V.FORECAST)[1])
                self.assertEqual(receipt['run_mode'], row['mode'])
                out = (P, receipt['evidence_tier'])
            else:
                self.assertEqual(res.outcome, 'VALIDATION_FAILURE', res.reason)
                self.assertFalse((res.folder / 'forecast.json').exists())
                code = res.reason.split(': ')[2].split(':')[0]               # DATA_ADMISSION_REFUSED: ValueError: <CODE>: ...
                self.assertIn(code, ('STALE_PIN', 'MODE_PIN'), res.reason)
                out = (R, code)
        finally:
            for path in (self.marker, OR.barrier_path(self.data)):
                if path.exists():
                    path.unlink()
            if row.get('frozen'):
                OR.forecast_ledger_path(self.proj, game).unlink()
            if row.get('done_elsewhere'):
                OR.session_attempts_path(self.proj, game, 'e' * 32).unlink()
            if stale:
                self.rows[game] = X.grow_master(self.proj, get_profile(game),
                                                [list(range(get_profile(game).holdout_first, get_profile(game).holdout_last + 1 + EXTRA))])
        return out

    def regrow3(self, game):
        p = get_profile(game)
        X.grow_master(self.proj, p, [list(range(p.holdout_first, p.holdout_last + 1 + EXTRA)), [p.holdout_last + 1 + EXTRA]])

    def test_every_request_row_at_every_stage(self):
        self.assertEqual(set(ROWS), set(TABLE))
        codes = {}
        for stage in STAGES:
            self.tearDown()
            self.setUp()
            game = 'POWERBALL' if stage in ('S0', 'S2', 'S4', 'X_ORPHAN') else 'OZLOTTO'
            self.at_stage(game, stage)
            for name, row in ROWS.items():
                with self.subTest(stage=stage, row=name):
                    self.assertEqual(TABLE[name][stage], ORACLE(row, stage), 'the typed table and the oracle disagree')
                    verdict, code = self.cell(game, name, stage)
                    self.assertEqual(verdict, TABLE[name][stage], code)
                    codes[(name, stage)] = code
        # the refusal each rule gives, once per rule, at the stage where every other condition is met (S5 or S2)
        want = {('dev after, unbound', 'S5'): 'INVALID_RUN_REQUEST', ('dev after, session, no ticket', 'S5'): 'NO_OPEN_TICKET',
                ('dev after, session, BEFORE', 'S5'): 'MODE_DISAGREES_WITH_RELEASE', ('dev holdout, session', 'S5'): 'INVALID_RUN_REQUEST',
                ('dev after, session, ticketed, ON', 'S4'): 'NOT_DEVELOPED', ('catch-up, ticketed, BEFORE', 'S4'): 'NOT_DEVELOPED',
                ('final, ticketed', 'S0'): 'NOT_DEVELOPED', ('diagnostic holdout', 'S0'): 'HOLDOUT_NOT_OPENED',
                ('diagnostic holdout', 'S3'): 'MODE_H_NOT_SEALED', ('diagnostic after', 'S1'): 'MODE_H_NOT_SEALED',
                ('holdout, plan, ticketed', 'S1'): 'BINDING_NOT_RESOLVED', ('holdout, plan, ticketed', 'S3'): 'BATCH_CLOSED',
                ('holdout, plan, ticketed', 'S5'): 'BATCH_CLOSED', ('holdout, plan, pair DONE', 'S2'): 'PAIR_ALREADY_DONE',
                ('holdout, plan, no ticket', 'S2'): 'NO_OPEN_TICKET', ('holdout, unbound', 'S2'): 'INVALID_RUN_REQUEST',
                ('holdout, plan, wrong digest', 'S2'): 'BINDING_NOT_RESOLVED', ('holdout mode, prefix target', 'S2'): 'INVALID_RUN_REQUEST',
                ('catch-up, stale pin', 'S5'): 'STALE_PIN', ('final, stale pin', 'S5'): 'STALE_PIN',
                ('catch-up, release ON', 'S5'): 'MODE_DISAGREES_WITH_RELEASE', ('final, draw the master holds', 'S5'): 'MODE_PIN',
                ('final, target has a freeze line', 'S5'): 'TARGET_FROZEN', ('catch-up, target has a freeze line', 'S5'): 'TARGET_FROZEN',
                ('catch-up, unbound', 'S5'): 'INVALID_RUN_REQUEST', ('final, unbound', 'S5'): 'INVALID_RUN_REQUEST',
                ('catch-up, no ticket', 'S5'): 'NO_OPEN_TICKET', ('final, no ticket', 'S5'): 'NO_OPEN_TICKET',
                ('catch-up, holdout target', 'S5'): 'INVALID_RUN_REQUEST', ('final, holdout target', 'S5'): 'INVALID_RUN_REQUEST',
                ('catch-up, pair DONE in another session', 'S5'): 'PAIR_ALREADY_DONE',
                ('catch-up, ticketed, BEFORE', 'S5'): 'CATCH_UP', ('final, ticketed', 'S5'): 'PROSPECTIVE',
                ('dev after, session, ticketed, ON', 'S5'): 'DEVELOPMENT_WF_EXPLORATORY', ('holdout, plan, ticketed', 'S2'): 'HOLDOUT_MODE_H'}
        for key, code in want.items():
            self.assertEqual(codes[key], code, key)
        for name in ROWS:
            self.assertEqual(codes[(name, 'X_ORPHAN')] in ('UNRESOLVED_ORPHAN_MARKER', 'INVALID_RUN_REQUEST'), True, name)
            self.assertEqual(codes[(name, 'X_BARRIER')] in ('INSTALL_IN_PROGRESS', 'INVALID_RUN_REQUEST'), True, name)


class ModeToPin(Project):
    """Design 3.4(a): the pin-dependent half. The pinned master's last draw is holdout_last + EXTRA."""

    def setUp(self):
        super().setUp()
        for p in (POWERBALL, OZLOTTO):
            self.rows[p.game_id] = X.grow_master(self.proj, p, [list(range(p.holdout_first, p.holdout_last + 1 + EXTRA))])
            self.opened(p.game_id)
            for m in OR.LIFECYCLE_MARKERS:
                X.write_mode_h_plan(self.proj, p.game_id, BATCH, [], [], pin=self.v2(p.game_id),
                                    manifest_sha=X.write_study_manifest(self.proj, p.game_id)) if m == 'BATCH_COMPLETE' else None
                X.write_marker(self.proj, p.game_id, BATCH, m)
            X.write_developed_record(self.proj, p.game_id)
        self.n = 0

    def attempt(self, game, mode, target, *, release='BEFORE', diagnostic=False):
        p = get_profile(game)
        self.n += 1
        rid, sid, pin = f'mg-{self.n:032x}', f'{self.n:032x}', self.v2(game)
        if diagnostic:
            req = request(game, target, mode, run_id=rid, binding=X.DIAGNOSTIC, pin=pin)
        else:
            e, _d = e1_pins(game)
            when = p.derived_date(target - 1 if release == 'BEFORE' else target).isoformat()
            sess = X.write_session(self.proj, game, sid, [{'method_id': 'E_1', 'variant_id': C.E1[1],
                                   'method_revision': e['method_revision'], 'release_date': when}], pin=pin)
            req = request(game, target, mode, run_id=rid, binding=X.binding_for_session(sess, rid), pin=pin)
            X.open_ticket(OR.session_attempts_path(self.proj, game, sid), req, scope_kind='WEEKLY_SESSION', scope_id=sid)
        res = self.launch(req)
        return res.outcome, res.reason, res.folder

    def test_each_mode_at_the_last_draw_the_next_and_beyond(self):
        for game in ('POWERBALL', 'OZLOTTO'):
            last = get_profile(game).holdout_last + EXTRA
            cases = [('CATCH_UP', 'BEFORE', False), ('REAL_DEVELOPMENT', 'ON', False), ('REAL_DEVELOPMENT', None, True)]
            for mode, release, diagnostic in cases:
                with self.subTest(game=game, mode=mode, diagnostic=diagnostic):
                    out, why, _f = self.attempt(game, mode, last, release=release, diagnostic=diagnostic)
                    self.assertEqual(out, 'SUCCESS', why)                                # the last draw the master holds
                    out, why, folder = self.attempt(game, mode, last + 1, release=release, diagnostic=diagnostic)
                    self.assertEqual(out, 'VALIDATION_FAILURE')                          # the next draw: no result yet
                    self.assertIn('MODE_PIN', why)
                    self.assertFalse((folder / 'forecast.json').exists())
                    out, why, folder = self.attempt(game, mode, last + 2, release=release, diagnostic=diagnostic)
                    self.assertEqual(out, 'VALIDATION_FAILURE')                          # beyond: the reader refuses first
                    self.assertIn('outside the pinned version', why)
            with self.subTest(game=game, mode='FINAL_NEXT_DRAW'):
                out, why, folder = self.attempt(game, 'FINAL_NEXT_DRAW', last)
                self.assertEqual(out, 'VALIDATION_FAILURE')                              # a draw the pinned master holds
                self.assertIn('MODE_PIN', why)
                self.assertFalse((folder / 'forecast.json').exists())
                out, why, folder = self.attempt(game, 'FINAL_NEXT_DRAW', last - 1)
                self.assertIn('MODE_PIN', why)
                out, why, _f = self.attempt(game, 'FINAL_NEXT_DRAW', last + 1)
                self.assertEqual(out, 'SUCCESS', why)                                    # exactly last_draw(v) + 1
                out, why, _f = self.attempt(game, 'FINAL_NEXT_DRAW', last + 2)
                self.assertEqual(out, 'VALIDATION_FAILURE')
                self.assertIn('outside the pinned version', why)

    def test_one_data_kind_for_every_real_mode(self):
        """Design 3.3 and T-05: on the same prefix, a forecast made in each mode has the same permitted-view digest,
        ranking, tie order and selections; only the run mode and tier differ, so no gate changes a method-facing byte."""
        for game in ('POWERBALL', 'OZLOTTO'):
            last = get_profile(game).holdout_last + EXTRA
            for target, modes in ((last, (('CATCH_UP', 'BEFORE', False), ('REAL_DEVELOPMENT', 'ON', False),
                                          ('REAL_DEVELOPMENT', None, True))),):
                seen = []
                for mode, release, diagnostic in modes:
                    out, why, folder = self.attempt(game, mode, target, release=release, diagnostic=diagnostic)
                    self.assertEqual(out, 'SUCCESS', why)
                    rec = json.loads((folder / 'forecast.json').read_bytes())
                    validate_forecast(rec, e1_pins(game)[1])
                    seen.append((mode, rec))
                base = seen[0][1]
                for mode, rec in seen[1:]:
                    with self.subTest(game=game, mode=mode):
                        for field in ('permitted_view_digest', 'barrels', 'record_status', 'training_last_draw_number',
                                      'draw_key', 'declaration_digest'):
                            self.assertEqual(rec[field], base[field], field)
                self.assertEqual({m: r['run_mode'] for m, r in seen}, {m: m for m, _r in seen})
            # FINAL_NEXT_DRAW at last + 1 against a development forecast of the same prefix on a master one draw longer
            out, why, folder = self.attempt(game, 'FINAL_NEXT_DRAW', last + 1)
            self.assertEqual(out, 'SUCCESS', why)
            final = json.loads((folder / 'forecast.json').read_bytes())
            p = get_profile(game)
            self.rows[game] = X.grow_master(self.proj, p, [list(range(p.holdout_first, p.holdout_last + 1 + EXTRA)),
                                                           [last + 1]])
            self.n += 1
            v3 = (3, self.rows[game][2]['master_sha256'])
            req = request(game, last + 1, 'REAL_DEVELOPMENT', run_id=f'mg-{self.n:032x}', binding=X.DIAGNOSTIC, pin=v3)
            res = self.launch(req)
            self.assertEqual(res.outcome, 'SUCCESS', res.reason)
            dev = json.loads((res.folder / 'forecast.json').read_bytes())
            for field in ('permitted_view_digest', 'barrels', 'record_status', 'training_last_draw_number', 'draw_key'):
                self.assertEqual(final[field], dev[field], (game, field))
            self.assertEqual((final['run_mode'], dev['run_mode']), ('FINAL_NEXT_DRAW', 'REAL_DEVELOPMENT'))


if __name__ == '__main__':
    unittest.main()
