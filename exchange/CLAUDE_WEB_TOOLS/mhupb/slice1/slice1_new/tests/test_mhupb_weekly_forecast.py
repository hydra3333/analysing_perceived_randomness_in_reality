"""MHUP-B slice 1, layer L2: the forecasting half of the weekly session (design v0.1r7 sections 6.1 to 6.5, Appendices
F, I and L; code plan v0.3 section 5, L2). OFFLINE and INVENTED: see mhupb_fixtures.

What is shown (the design's test names in brackets):
- one whole session in MH-1's order on both games; a rerun before the next result makes nothing [L-W1];
- two and four missed draws caught up oldest first [L-R5];
- an interruption after every durable step (ticket, run, DONE ticket, freeze line, score line), each resumed under the
  same session with a fresh token and, separately, continued by a successor session after a cleared lock: the same
  science as the uninterrupted run, exactly one DONE ticket per pair, no pair run again once DONE [L-W3, L-W3b];
- the resume token: older than five minutes, used twice, absent, of another session; changed code refuses [L-W4];
- the hour rule and the deadline; a straddling set classified record by record; a set started and interrupted is
  completed with less than an hour left, never NONE; once the result is accepted the rest are CATCH_UP and marked
  MISSING_BATCH [Appendix I];
- STALE when the master grows; the next session continues from the game-wide DONE tickets [L-W4];
- the roster cases: a variant added after scored draws, added while a forecast is open, retired with an open
  forecast; a variant released on or after a draw date gets a development record, never MISSING_BATCH [L-R1 to L-R3];
- the chain broken by an edit, a removal and a reorder; a torn last line; a clock that runs backwards;
- reading "scored": identities only, a foreign, malformed or duplicated identity refuses, and a taint planted in
  every outcome-derived field of the score ledger reaches no request, ticket, freeze line or status line [CP-Q5];
- across all of it, no record classed PROSPECTIVE without a freeze time before its deadline [L-W5];
- the oracles agree with the package: the chain checker and the roster-closure checker [R-4].
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import unittest
from datetime import timedelta
from pathlib import Path
from unittest import mock

import mhupb_fixtures as B
import mhupa_slice2_fixtures as S2
import _common.contract_runner as CR
import _common.weekly_records as WR
import _common.weekly_session as WS
from _common import closure as CL
from _common import jsonl_ledger as JL
from _common import owner_records as OR
from _common import score_identities as SI
from _common.contract_records import canonical, record_digest

REAL_DIGESTS = WS._digests
ROOT = Path(__file__).resolve().parents[1]
METHODS_SIDE = ('src/methods/_common/weekly_session.py', 'src/methods/_common/weekly_records.py',
                'src/methods/_common/score_identities.py', 'src/methods/_common/jsonl_ledger.py',
                'src/methods/Method_Weekly_Forecast.py')


class Checks:
    """Invariants asserted at the end of every scenario."""

    def check_invariants(self):
        lines = self.lines()
        self.assertTrue(B.oracle_chain_ok(OR.forecast_ledger_path(self.proj, self.GAME)) or not lines)
        closed = SI.closed_targets(self.GAME, lines, SI.scored_identities(self.proj, self.GAME, lines))
        self.assertEqual(closed, B.oracle_closed_targets(OR.forecast_ledger_path(self.proj, self.GAME),
                                                         WR.score_ledger_path(self.proj, self.GAME)))
        self.assertTrue(all(n == 1 for n in self.done_counts().values()), self.done_counts())
        # every run that completed has its DONE ticket: a completed run is never left unticketed and run again
        self.assertEqual(len([f for f in self.run_folders() if (f / 'terminal.json').is_file()]),
                         sum(self.done_counts().values()))
        named = set()
        for line in lines:
            deadline = WR.parse_utc(line['deadline_utc'])
            for r in line['records']:
                key = (r['method_id'], r['method_revision'], r['variant_id'], line['target_draw_number'])
                self.assertNotIn(key, named)                                  # no record counted at two targets
                named.add(key)
                if r['effective_class'] == 'PROSPECTIVE' and r['record_kind'] == 'FORECAST':        # L-W5
                    self.assertEqual(r['run_mode'], 'FINAL_NEXT_DRAW')
                    self.assertLess(WR.parse_utc(r['frozen_at_utc']), deadline)
        self.assertEqual(set(self.done_counts()), named | {k for k in self.done_counts() if k not in named})
        return closed


class WholeSession(B.Weekly, Checks):

    def test_one_session_in_order_and_a_rerun_makes_nothing(self):
        sid, states = self.session()
        self.assertEqual(states, [('FROZE', self.first), ('FROZE', self.first + 1), ('FROZE_NEXT', self.first + 2)])
        lines = self.lines()
        self.assertEqual([(l['target_draw_number'], l['set_kind'], l['deadline_met']) for l in lines],
                         [(self.first, 'CATCH_UP_SET', None), (self.first + 1, 'CATCH_UP_SET', None),
                          (self.first + 2, 'NEXT_DRAW_SET', True)])
        for line in lines:
            self.assertEqual(len(line['records']), 3)
            self.assertEqual(line['writing_session_id'], sid)
            want = ('FINAL_NEXT_DRAW', 'PROSPECTIVE', 'PROSPECTIVE', False) if line['set_kind'] == 'NEXT_DRAW_SET' \
                else ('CATCH_UP', 'CATCH_UP', 'CATCH_UP', True)
            for r in line['records']:
                self.assertEqual((r['run_mode'], r['tier'], r['effective_class'], r['missing_batch']), want)
                self.assertEqual((r['ledger_version'], r['master_sha256']), (2, self.rows[1]['master_sha256']))
        self.assertEqual(self.check_invariants(), {self.first, self.first + 1})
        self.assertFalse(OR.session_lock_path(self.proj, self.GAME).exists())
        # L-W1: the same week again, before the next result: OPEN, and not one new byte except the new session's own
        before = self.weekly_bytes()
        sid2, states2 = self.session()
        self.assertEqual(states2, [('OPEN', self.first + 2)])
        after = self.weekly_bytes()
        new = set(after) - set(before)
        self.assertEqual({Path(n).name for n in new}, {f'SESSION_{sid2}.json'})
        self.assertEqual({n: after[n] for n in before}, before)
        # every forecast is frozen before its outcome: the records' training view ends before the target
        for folder in self.run_folders():
            rec = json.loads((folder / 'forecast.json').read_bytes())
            self.assertEqual(rec['training_last_draw_number'], rec['target_draw_number'] - 1)

    def test_next_never_passes_a_frozen_target_that_is_not_scored(self):
        """Appendix F, properties (i) and (ii): the order is the forecasting half's own. A sequencer that forgot to
        score gets the same FROZE N again, and nothing is forecast for a later draw."""
        sid = self.open()['session_id']
        self.assertEqual(self.next(sid), ('FROZE', self.first))
        before = self.weekly_bytes()
        for _ in range(3):
            self.assertEqual(self.next(sid), ('FROZE', self.first))
        self.assertEqual(self.weekly_bytes(), before)
        with self.assertRaisesRegex(WS.SessionRefused, 'not closed'):
            WS.close_session(self.GAME, sid)
        self.score(sid, self.first)
        self.assertEqual(self.next(sid), ('FROZE', self.first + 1))

    def test_status_block(self):
        s = WS.status(self.GAME)
        self.assertEqual([b['target'] for b in s['backlog']], [self.first, self.first + 1])
        self.assertEqual((s['next_target'], s['session_lock'], s['active_variants']), (self.first + 2, None, 3))
        self.assertIn('can start', s['next_state'])
        sid = self.open()['session_id']
        self.next(sid)
        s = WS.status(self.GAME)
        self.assertEqual((s['session_lock'], s['backlog'][0]['state'], s['backlog'][0]['unscored']),
                         (sid, 'frozen, not yet scored', 3))
        text = '\n'.join(WS.status_lines(s))
        self.assertIn(f'backlog: draw {self.first} OUTCOME_AVAILABLE: frozen, not yet scored (3 record(s) unscored)', text)
        self.now = self.at(self.first + 2, minutes_before=30)
        self.assertIn('OUTCOME_PENDING', WS.status(self.GAME)['next_state'])


class WholeSessionOzLotto(WholeSession):
    GAME = 'OZLOTTO'


class MissedDraws(B.Weekly, Checks):
    EXTRA = 4

    def test_four_missed_draws_oldest_first(self):                              # L-R5
        sid, states = self.session()
        self.assertEqual(states, [('FROZE', self.first + i) for i in range(4)] + [('FROZE_NEXT', self.first + 4)])
        self.assertEqual(self.check_invariants(), {self.first + i for i in range(4)})
        frozen = [WR.parse_utc(l['frozen_utc']) for l in self.lines()]
        self.assertEqual(frozen, sorted(frozen))
        scored = [s['target_draw_number'] for s in self.scores()]
        self.assertEqual(scored, sorted(scored))                                # N is closed before N + 1 is forecast
        first_done = {}
        for rows in self.tickets().values():
            for t in rows:
                if t['kind'] == 'OPEN':
                    first_done.setdefault(t['target_draw_number'], t['utc'])
        for s in self.scores():
            if s['target_draw_number'] < self.first + 4:
                self.assertLess(s['scored_utc'], first_done[s['target_draw_number'] + 1])


class Interruptions(B.Weekly, Checks):
    EXTRA = 1

    def setUp(self):
        super().setUp()
        self.keep = 2

    def _cohort(self, game_id, adapters_):
        members, excluded = super()._cohort(game_id, adapters_)
        return members[:self.keep], excluded

    def _released(self, root):
        keys = sorted(super()._released(root))
        return {k: self.RELEASED for k in keys[:self.keep]}

    def uninterrupted(self):
        with B.fault_after(0) as steps:
            self.session()
        return self.science(), list(steps)

    def test_every_step_resumed_and_continued_by_a_successor(self):
        want, steps = self.uninterrupted()
        self.assertEqual([s.split()[0] for s in steps].count('run'), 4)
        self.assertEqual(len(steps), 17, steps)        # 2 x (OPEN, run, DONE) + line; 2 scores; SET_STARTED + 6 + line
        for how in ('resume', 'successor'):
            for k in range(1, len(steps) + 1):
                with self.subTest(how=how, k=k, step=steps[k - 1]):
                    self.tearDown()
                    self.setUp()
                    sid = self.open()['session_id']
                    with B.fault_after(k), self.assertRaises(B.Boom):
                        self.loop(sid)
                    self.assertTrue(OR.session_lock_path(self.proj, self.GAME).exists())     # a dead process leaves it
                    done_before = dict(self.done_counts())
                    if how == 'resume':
                        with self.assertRaises(WS.SessionRefused):
                            self.open()                                                      # no second session
                        self.resume_token(sid)
                        self.assertEqual(self.open(resume=True)['session_id'], sid)
                        states = self.loop(sid)
                        WS.close_session(self.GAME, sid)
                    else:
                        self.clear_lock()
                        sid2, states = self.session()
                        self.assertNotEqual(sid2, sid)
                    # a fault after the last freeze line leaves nothing to do: the forecast is OPEN
                    self.assertEqual(states[-1], ('OPEN' if k == len(steps) else 'FROZE_NEXT', self.first + 1))
                    self.assertEqual(self.science(), want)
                    self.check_invariants()
                    for pair, n in done_before.items():                # a pair that was DONE was never run again
                        runs = [t for rows in self.tickets().values() for t in rows
                                if t['kind'] == 'OPEN' and OR.pair_of(t) == pair]
                        closed = [t for rows in self.tickets().values() for t in rows
                                  if t['kind'] == 'FAILED_TO_START' and OR.pair_of(t) == pair]
                        self.assertEqual(len(runs) - len(closed), 1, pair)
                    if how == 'successor':
                        for line in self.lines():
                            for r in line['records']:                  # every earlier record named with its own binding
                                self.assertEqual(record_digest(WR.session(self.proj, self.GAME, r['session_id'])),
                                                 r['session_digest'])

    def test_a_session_record_without_its_lock_is_just_a_past_session(self):
        real, calls = WS.CP.create_only, []

        def second_fails(path, raw):
            calls.append(path)
            if len(calls) == 2:
                raise B.Boom('crash after the session record, before the lock')
            return real(path, raw)
        with mock.patch.object(WS.CP, 'create_only', second_fails), self.assertRaises(B.Boom):
            self.open()
        self.assertFalse(OR.session_lock_path(self.proj, self.GAME).exists())
        self.assertEqual(len(list(WR.sessions_folder(self.proj, self.GAME).glob('SESSION_*.json'))), 1)
        sid, states = self.session()                                    # nothing to resume: a new session runs
        self.assertEqual(states[-1][0], 'FROZE_NEXT')
        self.check_invariants()

    def test_resume_tokens_and_changed_code(self):
        sid = self.open()['session_id']
        with self.assertRaisesRegex(WS.SessionRefused, 'no resume token'):
            self.open(resume=True)
        self.resume_token(sid, age=timedelta(minutes=5, seconds=30))
        with self.assertRaisesRegex(WS.SessionRefused, 'older than five minutes'):
            self.open(resume=True)
        self.resume_token('f' * 32)                                     # another session's token is not this one's
        self.resume_token(sid)
        self.assertEqual(self.open(resume=True)['session_id'], sid)
        with self.assertRaisesRegex(WS.SessionRefused, 'already used'):
            self.open(resume=True)
        self.now += timedelta(seconds=30)
        self.resume_token(sid)
        self.digests = ('d' * 64, 'e' * 64)                             # the code changed under the session (L-W4)
        with self.assertRaisesRegex(WS.SessionRefused, 'CODE_CHANGED'):
            self.open(resume=True)
        with self.assertRaisesRegex(WS.SessionRefused, 'CODE_CHANGED'):
            self.next(sid)
        self.digests = ('c' * 64, 'e' * 64)
        self.assertEqual(self.next(sid)[0], 'FROZE')
        resumed = [t for t in self.tickets()[sid] if t['kind'] == 'RESUMED']
        self.assertEqual(len(resumed), 1)
        self.assertTrue(resumed[0]['resume_token'].startswith(f'RESUME_{sid}_'))
        self.clear_lock()
        with self.assertRaisesRegex(WS.SessionRefused, 'no session lock'):
            self.open(resume=True)
        with self.assertRaisesRegex(WS.SessionRefused, 'not the game\'s active session'):
            self.next(sid)

    def test_open_session_refusals(self):
        up = OR.updater_lock_path(self.proj)
        up.write_text('updater')
        with self.assertRaisesRegex(WS.SessionRefused, 'updater'):
            self.open()
        up.unlink()
        OR.developed_record_path(self.proj, self.GAME).rename(self.td / 'developed.json')
        with self.assertRaisesRegex(WS.SessionRefused, 'NOT_DEVELOPED'):
            self.open()
        (self.td / 'developed.json').rename(OR.developed_record_path(self.proj, self.GAME))
        # a developed record is believed only as the declaration of this game's sealed Mode H study (design 6.7)
        genuine = OR.developed_record_path(self.proj, self.GAME).read_bytes()
        for change in (dict(mode_h_score_digest='d' * 64), dict(mode_h_batch_id='wf-' + 'e' * 32),
                       dict(owner_statement='I say so'), dict(mode_h_batch_id=None)):
            with self.subTest(developed=change):
                self.write_developed(**change)
                OR.validate_developed_record(json.loads(OR.developed_record_path(self.proj, self.GAME).read_bytes()), self.GAME)
                with self.assertRaisesRegex(WS.SessionRefused, 'NOT_DEVELOPED'):
                    self.open()
        OR.developed_record_path(self.proj, self.GAME).write_bytes(genuine)
        seal = OR.marker_path(self.proj, self.GAME, self.BATCH, 'MODE_H_SEALED')
        seal.rename(self.td / 'seal.json')
        with self.assertRaisesRegex(WS.SessionRefused, 'not sealed'):
            self.open()
        (self.td / 'seal.json').rename(seal)
        marker = CR.ORPHAN_MARKER
        marker.parent.mkdir(parents=True)
        marker.write_text('{}')
        with self.assertRaisesRegex(WS.SessionRefused, 'UNRESOLVED_ORPHAN_MARKER'):
            self.open()
        marker.unlink()
        self.assertFalse(OR.weekly_root(self.proj, self.GAME).exists())            # refusals wrote nothing
        with mock.patch.object(B.RR, 'released_variants', lambda root: {}), \
                self.assertRaisesRegex(WS.SessionRefused, 'not the released set'):
            self.open()                                                             # SUPPORTED but not released
        sid = self.open()['session_id']
        with self.assertRaisesRegex(WS.SessionRefused, 'session lock exists'):
            self.open()
        with self.assertRaisesRegex(WS.SessionRefused, 'not closed'):
            WS.close_session(self.GAME, sid)                                         # not a clean end: the lock stays
        self.assertTrue(OR.session_lock_path(self.proj, self.GAME).exists())

    def test_a_stop_class_run_leaves_no_done_ticket_and_is_run_again(self):
        sid = self.open()['session_id']
        real = CR.run_contract_method
        calls = []

        def stale_once(request, **kw):
            calls.append(request['run_id'])
            if len(calls) == 2:
                return CR.RunResult(Path('nowhere'), 'VALIDATION_FAILURE', 'DATA_ADMISSION_REFUSED: ValueError: planted', {})
            return real(request, **kw)
        with mock.patch.object(WS.CR, 'run_contract_method', stale_once), self.assertRaises(WS.SessionStopped):
            self.next(sid)
        self.assertEqual(sum(self.done_counts().values()), 1)
        self.assertEqual(self.lines(), [])
        self.resume_token(sid)
        self.open(resume=True)
        self.assertEqual(self.loop(sid)[-1][0], 'FROZE_NEXT')
        failed = [t for t in self.tickets()[sid] if t['kind'] == 'FAILED_TO_START']
        self.assertEqual([t['run_id'] for t in failed], [calls[1]])                  # that run id is never reused
        self.check_invariants()


class Deadline(B.Weekly, Checks):
    EXTRA = 0

    def setUp(self):
        super().setUp()
        self.m = self.first                                             # the next draw; nothing to catch up

    def test_the_hour_rule(self):
        for minutes, state in ((61, 'FROZE_NEXT'), (59, 'NONE'), (0, 'NONE'), (-30, 'NONE')):
            with self.subTest(minutes_before=minutes):
                self.tearDown()
                self.setUp()
                self.now = self.at(self.m, minutes_before=minutes)
                sid = self.open()['session_id']
                self.assertEqual(self.next(sid), (state, self.m))
                self.assertEqual(len(self.lines()), 1 if state == 'FROZE_NEXT' else 0)
                self.assertEqual(self.run_folders() == [], state == 'NONE')
                self.assertEqual(WS.close_session(self.GAME, sid), 'OPEN' if state == 'FROZE_NEXT' else 'NONE')

    def test_a_straddling_set_is_classified_record_by_record(self):
        self.now = self.at(self.m, minutes_before=61)
        sid = self.open()['session_id']
        real = CR.run_contract_method
        runs = []

        def slow(request, **kw):
            runs.append(request)
            if len(runs) == 3:
                self.now = self.at(self.m, minutes_before=-5)           # the third run freezes after midnight
            return real(request, **kw)
        with mock.patch.object(WS.CR, 'run_contract_method', slow):
            self.assertEqual(self.next(sid), ('FROZE_NEXT', self.m))
        line = self.lines()[0]
        self.assertEqual([r['effective_class'] for r in line['records']], ['PROSPECTIVE', 'PROSPECTIVE', 'LATE_PRE_DRAW'])
        self.assertEqual({r['tier'] for r in line['records']}, {'PROSPECTIVE'})          # the tier is immutable
        self.assertEqual((line['deadline_met'], line['set_kind']), (False, 'NEXT_DRAW_SET'))
        self.check_invariants()
        # the result arrives; a later session scores it; the late record keeps its class and is never re-forecast
        self.clear_lock()
        self.grow([self.m])
        self.now = self.at(self.m + 1, hours_before=40)
        sid2, states = self.session()
        self.assertEqual(states, [('FROZE', self.m), ('FROZE_NEXT', self.m + 1)])
        self.assertEqual(sorted(s['effective_class'] for s in self.scores()), ['LATE_PRE_DRAW', 'PROSPECTIVE', 'PROSPECTIVE'])
        self.assertEqual(len(self.run_folders()), 6)
        self.check_invariants()

    def interrupted_set(self):
        """S1 writes SET_STARTED for M, completes one variant, and dies. Returns S1's id."""
        self.now = self.at(self.m, minutes_before=61)
        sid = self.open()['session_id']
        with B.fault_after(4), self.assertRaises(B.Boom):               # SET_STARTED, OPEN, run, DONE
            self.next(sid)
        self.assertEqual((sum(self.done_counts().values()), self.lines()), (1, []))
        return sid

    def test_an_interrupted_set_is_completed_with_less_than_an_hour_left(self):      # L-W3b
        for how in ('resume', 'successor'):
            with self.subTest(how=how):
                self.tearDown()
                self.setUp()
                sid = self.interrupted_set()
                self.now = self.at(self.m, minutes_before=20)           # less than an hour: a new set could not start
                if how == 'resume':
                    self.resume_token(sid)
                    self.open(resume=True)
                    use = sid
                else:
                    self.clear_lock()
                    use = self.open()['session_id']
                self.assertEqual(self.next(use), ('FROZE_NEXT', self.m))             # completed, never NONE
                line = self.lines()[0]
                self.assertEqual((len(line['records']), line['deadline_met']), (3, True))
                self.assertEqual({r['session_id'] for r in line['records']}, {sid} if how == 'resume' else {sid, use})
                self.assertEqual(sum(1 for rows in self.tickets().values() for t in rows if t['kind'] == 'SET_STARTED'), 1)
                self.check_invariants()

    def test_an_interrupted_set_after_the_result_is_accepted(self):
        sid = self.interrupted_set()
        self.clear_lock()
        self.grow([self.m])                                             # M's result is accepted
        self.now = self.at(self.m + 1, hours_before=40)
        sid2 = self.open()['session_id']
        self.assertEqual(self.next(sid2), ('FROZE', self.m))
        line = self.lines()[0]
        self.assertEqual(line['set_kind'], 'CATCH_UP_SET')
        got = sorted((r['run_mode'], r['effective_class'], r['missing_batch'], r['session_id'] == sid) for r in line['records'])
        self.assertEqual(got, [('CATCH_UP', 'CATCH_UP', True, False), ('CATCH_UP', 'CATCH_UP', True, False),
                               ('FINAL_NEXT_DRAW', 'PROSPECTIVE', False, True)])
        self.assertEqual(line['deadline_met'], True)
        self.score(sid2, self.m)
        self.check_invariants()

    def test_a_set_started_ticket_that_breaks_the_hour_rule_is_not_believed(self):     # EX_229 F-229-4
        self.now = self.at(self.m, minutes_before=30)
        sid = self.open()['session_id']
        self.assertEqual(self.next(sid), ('NONE', self.m))               # too late to start a set
        deadline_utc = WR.deadline(self.GAME, self.m)[0]
        forged = OR.ticket('SET_STARTED', scope_kind='WEEKLY_SESSION', scope_id=sid, game_id=self.GAME, method_id=None,
                           variant_id=None, method_revision=None, target_draw_number=self.m, run_id=None,
                           utc=WR.utc_text(self.now), extra={'run_mode': 'FINAL_NEXT_DRAW',
                                                             'deadline_utc': WR.utc_text(deadline_utc)})
        B.X.append_ticket(OR.session_attempts_path(self.proj, self.GAME, sid), forged)
        before = self.weekly_bytes()
        for call in (lambda: self.next(sid), lambda: WS.close_session(self.GAME, sid), lambda: WS.status(self.GAME)):
            with self.assertRaisesRegex(WS.SessionRefused, 'at least an hour before the deadline'):
                call()
        self.assertEqual((self.weekly_bytes(), self.run_folders()), (before, []))    # no set is completed under it

    def test_the_clock_behind_the_last_freeze_line_refuses(self):
        self.now = self.at(self.m, minutes_before=61)
        sid, _states = self.session()
        self.grow([self.m])
        self.now = self.at(self.m, hours_before=5)                      # earlier than the line already written
        sid2 = self.open()['session_id']
        self.assertEqual(self.next(sid2), ('FROZE', self.m))            # that line exists; nothing is appended
        self.score(sid2, self.m)
        with self.assertRaisesRegex(WS.SessionStopped, 'clock is behind'):
            self.next(sid2)
        self.assertEqual(len(self.lines()), 1)


class StaleAndRoster(B.Weekly, Checks):
    EXTRA = 1

    def test_stale_when_the_master_grows_and_the_next_session_continues(self):       # L-W4
        sid = self.open()['session_id']
        with B.fault_after(3), self.assertRaises(B.Boom):               # one variant DONE for the first target
            self.next(sid)
        self.grow([self.first + 1])                                     # a hand-grown master under an open session
        self.resume_token(sid)
        self.open(resume=True)
        self.assertEqual(self.next(sid), ('STALE', None))
        before = self.weekly_bytes()
        self.assertEqual(self.next(sid), ('STALE', None))
        self.assertEqual(self.weekly_bytes(), before)
        self.assertEqual(WS.close_session(self.GAME, sid), 'STALE')
        self.now = self.at(self.first + 2, hours_before=40)
        sid2, states = self.session()
        self.assertEqual(states, [('FROZE', self.first), ('FROZE', self.first + 1), ('FROZE_NEXT', self.first + 2)])
        first = self.lines()[0]
        self.assertEqual(sorted(r['session_id'] == sid for r in first['records']), [False, False, True])
        self.assertEqual(sorted(r['ledger_version'] for r in first['records']), [2, 3, 3])     # each its own training pin
        self.check_invariants()

    def test_a_variant_added_after_scored_draws_and_one_retired(self):               # L-R1, L-R2, L-R3
        sid, _states = self.session()                                   # E_6: first target scored, the next one open
        old = OR.forecast_ledger_path(self.proj, self.GAME).read_bytes()
        self.methods.add('E_7')                                         # an install releases E_7 (three variants)
        self.grow([self.first + 1])
        self.now = self.at(self.first + 2, hours_before=40)
        sid2, states = self.session()
        self.assertEqual(states, [('FROZE', self.first + 1), ('FROZE_NEXT', self.first + 2)])
        lines = self.lines()
        self.assertTrue(OR.forecast_ledger_path(self.proj, self.GAME).read_bytes().startswith(old))   # byte-identical
        self.assertEqual([len(l['records']) for l in lines], [3, 3, 6])     # the open forecast closed without E_7
        self.assertEqual({r['method_id'] for r in lines[1]['records']}, {'E_6'})
        self.assertEqual(self.check_invariants(), {self.first, self.first + 1})
        self.methods.discard('E_6')                                     # E_6 retired while its forecast is open
        self.grow([self.first + 2])
        self.now = self.at(self.first + 3, hours_before=40)
        sid3, states = self.session()
        self.assertEqual(states, [('FROZE', self.first + 2), ('FROZE_NEXT', self.first + 3)])
        self.assertEqual(sum(1 for s in self.scores() if s['target_draw_number'] == self.first + 2 and s['method_id'] == 'E_6'), 3)
        self.assertEqual({r['method_id'] for r in self.lines()[3]['records']}, {'E_7'})      # absent from the next line
        status = WS.status(self.GAME)
        self.assertEqual((len(status['joined_since_last_session']), len(status['left_since_last_session'])), (0, 0))
        self.check_invariants()

    def test_released_on_or_after_the_draw_date_is_development_never_missing_batch(self):
        members = [m for m in B._real_cohort(self.GAME, B.adapters())[0] if m['method_id'] == 'E_6']
        late = members[0]['variant_id']
        self.release_dates[('E_6', late)] = self.p.derived_date(self.first).isoformat()      # ON the first draw's date
        sid, states = self.session()
        first, nxt = self.lines()
        got = {r['variant_id']: (r['run_mode'], r['tier'], r['effective_class'], r['missing_batch']) for r in first['records']}
        self.assertEqual(got.pop(late), ('REAL_DEVELOPMENT', 'DEVELOPMENT_WF_EXPLORATORY', 'DEVELOPMENT_WF_EXPLORATORY', False))
        self.assertEqual(set(got.values()), {('CATCH_UP', 'CATCH_UP', 'CATCH_UP', True)})
        self.assertEqual({r['run_mode'] for r in nxt['records']}, {'FINAL_NEXT_DRAW'})
        # design 6.4 (EX_229 F-229-1): the development record is under the development run root, the others under the
        # weekly run root; each record's tier follows its run mode, not its folder
        where = {f.name: f for f in self.run_folders()}
        for line in (first, nxt):
            for r in line['records']:
                root = OR.development_runs_root(self.proj) if r['run_mode'] == 'REAL_DEVELOPMENT' else OR.weekly_runs_root(self.proj)
                self.assertTrue(where[r['run_id']].is_relative_to(root / self.GAME), r['run_mode'])
        self.assertEqual(len(list((OR.development_runs_root(self.proj) / self.GAME).glob('*/*/*'))), 1)
        self.assertEqual({s['tier'] for s in self.scores() if s['variant_id'] == late}, {'DEVELOPMENT_WF_EXPLORATORY'})
        self.check_invariants()


class LedgerRules(B.Weekly, Checks):
    EXTRA = 2

    def test_the_chain_broken_by_an_edit_a_removal_and_a_reorder(self):
        sid, _states = self.session()
        path = OR.forecast_ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        rows = good.split(b'\n')[:-1]
        self.assertTrue(B.oracle_chain_ok(path))
        edited = json.loads(rows[0])
        edited['tool_version'] = 'EDITED_AFTERWARDS'                    # a well-formed line: only the chain sees it
        cases = {'edit': canonical(edited) + b'\n'.join(rows[1:]) + b'\n', 'removal': b'\n'.join(rows[1:]) + b'\n',
                 'removal of the last': b'\n'.join(rows[:2]) + b'\n' + rows[2][:-40] + b'\n',
                 'reorder': b'\n'.join([rows[1], rows[0], rows[2]]) + b'\n',
                 'non-canonical': good.replace(b'{"closure_digest"', b'{ "closure_digest"', 1)}
        for name, raw in cases.items():
            with self.subTest(case=name):
                path.write_bytes(raw)
                self.assertFalse(B.oracle_chain_ok(path) and name != 'non-canonical')
                with self.assertRaises(OR.RecordRefused):
                    self.lines()
                sid2 = None
                with self.assertRaises(WS.SessionRefused):
                    sid2 = self.open()['session_id']
                    self.next(sid2)
                if sid2 is None:
                    self.fail('open-session itself reads no ledger')
                self.clear_lock()
        path.write_bytes(good)
        self.assertEqual(len(self.lines()), 3)
        # a truncated but internally consistent ledger passes the chain (design 6.5: the chain alone does not prove
        # the ledger was never replaced); an earlier recorded extent reveals it
        ext = JL.extent(self.lines())
        path.write_bytes(b'\n'.join(rows[:2]) + b'\n')
        self.assertTrue(B.oracle_chain_ok(path))
        self.assertEqual(len(self.lines()), 2)
        self.assertFalse(JL.extent_still_there(self.lines(), ext))
        path.write_bytes(good)
        self.assertTrue(JL.extent_still_there(self.lines(), ext))
        self.assertTrue(JL.extent_still_there(self.lines(), JL.extent(self.lines()[:1])))

    def test_a_torn_last_line_is_ignored_reported_and_completed(self):
        sid = self.open()['session_id']
        self.assertEqual(self.next(sid), ('FROZE', self.first))
        for path in (OR.forecast_ledger_path(self.proj, self.GAME), OR.session_attempts_path(self.proj, self.GAME, sid)):
            good = path.read_bytes()
            path.write_bytes(good + b'{"schema": "FREEZE_LINE_V1", "torn')
            rows, torn = OR.read_jsonl(path)
            self.assertTrue(torn)
            self.assertEqual(canonical(rows[-1]), good.split(b'\n')[-2] + b'\n')
        self.score(sid, self.first)
        self.assertEqual(self.next(sid), ('FROZE', self.first + 1))      # the next writer cuts the fragment and appends
        for path in (OR.forecast_ledger_path(self.proj, self.GAME), OR.session_attempts_path(self.proj, self.GAME, sid)):
            self.assertFalse(OR.read_jsonl(path)[1])
            sides = list(path.parent.glob(path.name + '.torn_*'))
            self.assertEqual([s.read_bytes() for s in sides], [b'{"schema": "FREEZE_LINE_V1", "torn'])
        self.assertEqual(len(self.lines()), 2)
        self.check_invariants()


class ReadingScored(B.Weekly, Checks):
    EXTRA = 2

    def scored_first(self):
        sid = self.open()['session_id']
        self.next(sid)
        self.score(sid, self.first)
        path = WR.score_ledger_path(self.proj, self.GAME)
        return sid, path, path.read_bytes(), [json.loads(x) for x in path.read_bytes().split(b'\n')[:-1]]

    def test_identities_only_and_refusals(self):                          # EX_223 CP-Q5; EX_229 F-229-2
        sid, path, good, rows = self.scored_first()
        idents = SI.scored_identities(self.proj, self.GAME, self.lines())
        self.assertEqual(len(idents), 3)
        for ident in idents:
            self.assertEqual(len(ident), 7)
            self.assertEqual((ident[0], ident[4], ident[6]), (self.GAME, self.first, 'WEEKLY_SCORE_POLICY_V1'))
            self.assertTrue(all(type(x) in (str, int) for x in ident))
        rest = b''.join(canonical(r) for r in rows[1:])
        first = lambda **change: canonical(dict(rows[0], **change)) + rest          # the first line altered, the others kept
        without = lambda field: canonical({k: v for k, v in rows[0].items() if k != field}) + rest
        top = rows[0]['readouts']['TOP']
        cases = {
            'duplicated': good + canonical(rows[0]),
            'duplicated under another score run': good + canonical(dict(rows[0], score_run_id='ws-' + 'a' * 32)),
            'foreign digest': good + canonical(dict(rows[0], scored_record_digest='0' * 64)),
            'no freeze line': good + canonical(dict(rows[0], target_draw_number=self.first + 9)),
            'identity-only fragment': canonical({f: rows[0][f] for f in ('schema', *SI.IDENTITY_FIELDS)}) + rest,
            'not canonical': good.replace(b'{"amendment_of"', b'{ "amendment_of"', 1),
            'no outcome pin': without('outcome_master_sha256'),
            'no score run id': without('score_run_id'),
            'no scored time': without('scored_utc'),
            'no quantities': without('readouts'),
            'no freeze identity': without('freeze_line_digest'),
            'an extra field': first(extra_field=1),
            'another freeze line digest': first(freeze_line_digest='0' * 64),
            'another freeze line number': first(freeze_line_number=2),
            'a class the freeze line does not record': first(effective_class='PROSPECTIVE'),
            'a run the freeze line does not record': first(run_id='mg-' + '9' * 32),
            'a training pin the freeze line does not record': first(training_ledger_version=1),
            'a readout out of range': first(readouts=dict(rows[0]['readouts'], TOP=dict(top, main_matches=8))),
            'a readout of another game': first(readouts=dict(rows[0]['readouts'], TOP={'main_matches': 1, 'division': 0})),
            'a rank that is not a fraction': first(rank=dict(rows[0]['rank'], mean_rank_main='about 14')),
            'an amendment that names nothing': good + canonical(dict(rows[0], scoring_policy_id='CORRECTED_POLICY_V2',
                                                                    amendment_of='0' * 64)),
            'an amendment without its policy': good + canonical(dict(rows[0], amendment_of=record_digest(rows[0]))),
            'malformed': good + b'{"schema": "WEEKLY_SCORE_LINE_V1", "method_id": 7}\n',
            'unknown schema': good + b'{"schema": "OTHER_V1"}\n', 'blank line': good + b'\n'}
        self.assertIn(b'{"amendment_of"', good)
        for name, raw in cases.items():
            with self.subTest(case=name):
                path.write_bytes(raw)
                before = self.weekly_bytes()
                with self.assertRaises(OR.RecordRefused):
                    SI.scored_identities(self.proj, self.GAME, self.lines())
                with self.assertRaises(WS.SessionRefused):
                    self.next(sid)                       # never read as "scored", never as "not scored"
                with self.assertRaises(WS.SessionRefused):
                    WS.status(self.GAME)
                self.assertEqual(self.weekly_bytes(), before)            # nothing is forecast for a later target
        path.write_bytes(good)
        # an amendment under another policy stands beside the routine line it names and closes nothing by itself (L-S2)
        amend = dict(rows[0], scoring_policy_id='CORRECTED_POLICY_V2', amendment_of=record_digest(rows[0]))
        WR.validate_score_line(amend)
        path.write_bytes(good + canonical(amend))
        self.assertEqual(len(SI.scored_identities(self.proj, self.GAME, self.lines())), 4)
        self.assertEqual(self.next(sid), ('FROZE', self.first + 1))
        self.assertTrue(path.read_bytes().startswith(good))

    def test_identity_shaped_fragments_cannot_close_a_target(self):       # EX_229 F-229-2: the false-closure path
        sid = self.open()['session_id']
        self.assertEqual(self.next(sid), ('FROZE', self.first))          # frozen, not scored
        line = self.lines()[0]
        path = WR.score_ledger_path(self.proj, self.GAME)
        path.write_bytes(b''.join(canonical({
            'schema': WR.SCORE_LINE_SCHEMA, 'game_id': self.GAME, 'method_id': r['method_id'],
            'method_revision': r['method_revision'], 'variant_id': r['variant_id'], 'target_draw_number': self.first,
            'scored_record_digest': r['scored_record_digest'], 'scoring_policy_id': WR.ROUTINE_POLICY})
            for r in line['records']))
        # a reader that looked at identities alone would call the target closed (the oracle is such a reader)
        self.assertEqual(B.oracle_closed_targets(OR.forecast_ledger_path(self.proj, self.GAME), path), {self.first})
        before = self.weekly_bytes()
        with self.assertRaises(WS.SessionRefused):
            self.next(sid)
        with self.assertRaises(WS.SessionRefused):
            WS.close_session(self.GAME, sid)
        self.assertEqual(self.weekly_bytes(), before)
        self.assertEqual(len(self.run_folders()), 3)                     # nothing was forecast for the next target
        path.unlink()
        self.score(sid, self.first)                                      # the real scorer's lines close it
        self.assertEqual(self.next(sid), ('FROZE', self.first + 1))

    def test_valid_score_values_reach_nothing_the_forecasting_half_makes(self):        # EX_223 CP-Q5; EX_229 F-229-2
        """The score ledger is rewritten with VALID, schema-conforming and distinctive values in every outcome-derived
        and provenance field. The forecasting half must accept it (it is a valid ledger) and none of those values may
        reach a method's task or view, a run request, a ticket, a freeze line, a session record, the status block or
        any file a run writes."""
        sid, path, good, rows = self.scored_first()
        marks = {'score_run_id': 'ws-' + '7' * 32, 'scorer_version': 'MARKED_SCORER_V7',
                 'scored_utc': '2031-07-07T07:07:07.777777Z', 'outcome_master_sha256': '7' * 64,
                 'outcome_ledger_version': 77, 'drawn_main': [29, 30, 31, 32, 33, 34, 35], 'drawn_powerball': 19,
                 'readouts': {'TOP': {'main_matches': 7, 'powerball_match': 1, 'division': 1},
                              'WORST': {'unavailable': 'MARKED_REASON'}},
                 'rank': {'mean_rank_main': '7777/7', 'fair_var_main': '7777/77', 'rank_powerball': '19',
                          'fair_var_pb': '7777/777'}, 'draw_date_is_derived': False}
        needles = ('ws-7777777', 'MARKED_SCORER', '2031-07-07', '7' * 64, '7777/7', 'MARKED_REASON',
                   '29, 30, 31, 32, 33, 34, 35', '29,30,31,32,33,34,35', '"outcome_ledger_version": 77',
                   '"outcome_ledger_version":77')
        master = (self.proj / 'source_data' / f'{self.GAME}_results_master.csv').read_text(encoding='ascii')
        self.assertNotIn('29,30,31,32,33,34,35', master)                 # the mark is no draw of the invented master
        marked = [dict(r, **marks) for r in rows]
        for r in marked:
            WR.validate_score_line(r)
        path.write_bytes(b''.join(canonical(r) for r in marked))
        self.assertEqual(len(SI.scored_identities(self.proj, self.GAME, self.lines())), 3)     # a valid ledger
        requests, appended, echoed, seen = [], [], [], []
        real_run, real_append = CR.run_contract_method, JL.append
        e6 = B.adapters()['E_6']
        real_compute = e6.compute

        def compute(task, view):
            seen.append(json.dumps([task.as_dict(), view.simple_rows()], default=str))
            return real_compute(task, view)

        def run(request, **kw):
            requests.append(json.dumps(request))
            return real_run(request, **dict(kw, compute=compute))

        def append(p, record):
            appended.append(json.dumps(record))
            return real_append(p, record)
        with mock.patch.object(WS.CR, 'run_contract_method', run), mock.patch.object(WS.JL, 'append', append):
            self.assertEqual(self.next(sid, echoed), ('FROZE', self.first + 1))
        status = '\n'.join(WS.status_lines(WS.status(self.GAME)))
        self.assertEqual((len(requests), len(appended), len(seen)), (3, 7, 3))
        texts = [*requests, *appended, *echoed, *seen, status, json.dumps(WR.session(self.proj, self.GAME, sid))]
        texts += [raw.decode('ascii') for name, raw in self.weekly_bytes().items() if not name.endswith('SCORE_LEDGER_V1.jsonl')]
        for text in texts:
            for needle in needles:
                self.assertNotIn(needle, text)

    def test_statics_of_the_forecasting_half(self):
        banned = ('main_matches', 'powerball_match', 'division', 'drawn_main', 'drawn_powerball', 'readouts',
                  'mean_rank', 'supplementary')
        for rel in METHODS_SIDE:
            text = (ROOT / rel).read_text(encoding='ascii')
            tree = ast.parse(text)
            docs = {id(n.body[0].value) for n in ast.walk(tree)
                    if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body and
                    isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
            words = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and type(n.value) is str and id(n) not in docs]
            words += [n.id for n in ast.walk(tree) if isinstance(n, ast.Name)] + \
                     [n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)]
            imported = [a.name for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names] + \
                       [n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
            self.assertFalse([m for m in imported if m.split('.')[0] == 'evaluation'], rel)
            for net in ('urllib', 'socket', 'http', 'requests', 'subprocess', 'signal', 'psutil', 'kill', 'terminate',
                        'taskkill'):                                     # no network, no process control (static)
                self.assertFalse([m for m in imported if m.split('.')[0] == net], (rel, net))
                self.assertFalse([w for w in words if w == net], (rel, net))
            if not rel.endswith('weekly_records.py'):                    # it defines the score line's shape for both halves
                for word in banned:                                      # no outcome-derived field is named in the code
                    self.assertFalse([w for w in words if word in w], (rel, word))
        # the score ledger is opened in one place (weekly_records.score_ledger, the strict reader) and that reader is
        # called, on the forecasting side, only by score_identities, which returns identities
        named = [rel for rel in METHODS_SIDE if 'score_ledger_path' in (ROOT / rel).read_text(encoding='ascii')]
        self.assertEqual(named, ['src/methods/_common/weekly_records.py'])
        users = [rel for rel in METHODS_SIDE if 'score_ledger' in (ROOT / rel).read_text(encoding='ascii')]
        self.assertEqual(users, ['src/methods/_common/weekly_records.py', 'src/methods/_common/score_identities.py'])
        session = (ROOT / 'src/methods/_common/weekly_session.py').read_text(encoding='ascii')
        self.assertNotIn('score_ledger', session)                        # it reads scores only through score_identities
        self.assertNotIn('SCORE_LEDGER', session)


class RealClosure(B.Weekly):
    """The session's closure and environment digests are the closure module's (design 4.1, 6.1), not patched here."""
    EXTRA = 0

    def test_digests_are_recorded_and_a_changed_file_refuses(self):
        S2.copy_closure(self.proj)
        env = S2.fake_environment(self.td)
        with mock.patch.object(WS, '_digests', REAL_DIGESTS), \
                mock.patch.object(CL.Environment, 'current', staticmethod(lambda: env)):
            rec = self.open()
            frozen = CL.freeze(self.proj, env)
            self.assertEqual((rec['closure_digest'], rec['environment_digest']),
                             (frozen['closure']['digest'], frozen['environment']['digest']))
            victim = self.proj / 'src' / 'methods' / '_common' / 'occurrence_counts.py'
            victim.write_bytes(victim.read_bytes() + b'\n# changed under the session\n')
            with self.assertRaisesRegex(WS.SessionRefused, 'CODE_CHANGED'):
                self.next(rec['session_id'])


class CommandLine(B.Weekly):

    def main(self, *args):
        import Method_Weekly_Forecast as M
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = M.main(list(args))
            except SystemExit as exc:
                code = exc.code
        return code, out.getvalue().strip().splitlines(), err.getvalue()

    def test_commands_exit_codes_and_the_machine_readable_last_line(self):
        g = self.GAME
        code, out, _err = self.main('status', '--game', g)
        self.assertEqual((code, out[-1]), (0, '[WEEKLY-FORECAST] RESULT state=STATUS target=- session=-'))
        code, out, _err = self.main('open-session', '--game', g)
        sid = out[-1].rsplit('session=', 1)[1]
        self.assertEqual((code, out[-1]), (0, f'[WEEKLY-FORECAST] RESULT state=OPENED target=- session={sid}'))
        code, out, err = self.main('open-session', '--game', g)
        self.assertEqual((code, out[-1].split()[2]), (2, 'state=REFUSED'), err)
        self.assertIn('Nothing was written', err)
        code, out, _err = self.main('next', '--game', g, '--session', sid)
        self.assertEqual((code, out[-1]), (0, f'[WEEKLY-FORECAST] RESULT state=FROZE target={self.first} session={sid}'))
        code, out, err = self.main('close-session', '--game', g, '--session', sid)
        self.assertEqual(code, 2, err)                                   # not a clean end
        code, out, err = self.main('next', '--game', g, '--session', 'f' * 32)
        self.assertEqual(code, 2)
        with mock.patch.object(WS, '_complete_set', side_effect=WS.SessionStopped('planted')):
            self.score(sid, self.first)
            code, out, err = self.main('next', '--game', g, '--session', sid)
        self.assertEqual((code, out[-1].split()[2]), (1, 'state=STOPPED'))
        self.assertIn('rerun the weekly session to resume', err)
        self.assertEqual(self.main('bogus')[0], 2)


if __name__ == '__main__':
    unittest.main()
