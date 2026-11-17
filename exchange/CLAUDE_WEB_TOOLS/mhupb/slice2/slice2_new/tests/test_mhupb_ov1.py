"""MHUP-B slice 2, layer L5: OV-1's recorder (design supplement v0.8 sections 6.1, 6.5, 6.8; code plan v0.3 section 5 L5
and sections 6.5, 6.6, 7, 9). OFFLINE: the temporary weekly project of mhupb_fixtures; every draw, clock reading and
release date is invented.

 Registration   once per game, before its first target; no draw already made can enter; no second registration.
 Cut-off        01:30 UTC on the draw's date: 11:00 or 12:00 in Adelaide, never after noon (to the end of 2045); an
                eligibility line one second before it, and a stop at it and one second after it.
 Classification every target is counted, skipped, missed or a stop, from the records alone, in draw order, once.
                The weights, X and the factor are recomputed by ORACLES that share no code with the recorder: the
                weights from the forecast files, X from the outcome reader, the factor by `decimal` at 90 digits.
 Missed         only after the cut-off, only from a forecast ledger that verifies and reconciles; every reconciliation
                failure blocks and writes nothing, and the stream resumes by itself.
 Stops          each cause planted once; no factor line for that target or any later one; forecasting carries on.
 Restart        a fault after each append, then a rerun: the same bytes as an uninterrupted run; verify rebuilds all.
 Durability     EX_233 S2-F02: a record's own time is read before the record is durable, so the registration and every
                eligibility line count only with a CONFIRMED line read after the record; a stalled write, or an
                interruption, that carries a record past its limit ends in a stop and is never counted.
 Isolation      no failure of the recorder changes a byte of the live path's records.
"""
from __future__ import annotations

import ast
import json
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from unittest import mock

import mhupb_fixtures as B
import test_mhupb_ov1_numeric as KT
import _common.contract_publication as CP
import _common.weekly_records as WR
import _common.weekly_session as WS
from _common import jsonl_ledger as JL
from _common import owner_records as OR
from _common.contract_records import canonical, record_digest
from evaluation import ov1 as OV
from evaluation import ov1_numeric as NUM
from evaluation import outcome_reader as RD


class Stream(B.Weekly):
    EXTRA = 0                                     # no accepted draw after the holdout: M is the first weekly target

    def setUp(self):
        super().setUp()
        self.m = self.last_draw + 1

    # ------------------------------------------------------------ what the owner and the sequencer do
    def register(self):
        return OV.register(self.GAME, OV.REGISTRATION_STATEMENT)

    def record(self):
        """What `record` appended, without the CONFIRMED lines (one follows the registration and every eligibility line;
        the class Durability and the reader's test look at them)."""
        return [w for w in OV.record(self.GAME, echo=lambda s: None)['written'] if w[0] != 'CONFIRMED']

    def week(self, *, record=True):
        """One weekly session as the sequencer runs it: next and score in turn, OV-1's record after every score and at
        once on FROZE_NEXT, then close. Returns (states, everything record wrote)."""
        sid = self.open()['session_id']
        states, wrote = [], []
        while True:
            state, target = self.next(sid)
            states.append((state, target))
            if state != 'FROZE':
                break
            self.score(sid, target)
            wrote += self.record() if record else []
        if state == 'FROZE_NEXT' and record:
            wrote += self.record()
        WS.close_session(self.GAME, sid)
        return states, wrote

    def result(self, target):
        """The draw is made and accepted; the clock moves to 30 hours before the next draw's deadline."""
        self.grow([target])
        self.now = self.at(target + 1, hours_before=30)

    def cut(self, target, seconds=0.0):
        return OV.cutoff(self.GAME, target) + timedelta(seconds=seconds)

    # ------------------------------------------------------------ reading
    def raw_rows(self):
        return OV.stream(self.proj, self.GAME)['rows']

    def ov1_rows(self):
        return [r for r in self.raw_rows() if r['kind'] != 'CONFIRMED']

    def kinds(self):
        return [(r['kind'], r['target_draw_number']) for r in self.ov1_rows()]

    def ledger_bytes(self):
        p = OV.ledger_path(self.proj, self.GAME)
        return p.read_bytes() if p.exists() else b''

    def live_bytes(self):
        """Every byte of the live path's records: everything under the weekly folders except OV-1's two files."""
        return {k: v for k, v in self.weekly_bytes().items() if 'OV1_' not in k}

    def rewrite_scores(self, change):
        """Rewrite the score ledger with change(index, line) applied to every line (None drops the line)."""
        path = WR.score_ledger_path(self.proj, self.GAME)
        rows = [json.loads(x) for x in path.read_bytes().split(b'\n')[:-1]]
        path.write_bytes(b''.join(canonical(r) for r in (change(i, dict(r)) for i, r in enumerate(rows)) if r is not None))

    # ------------------------------------------------------------ ORACLES (no code of ov1.py)
    def oracle_weights(self, target):
        """(weights, eligible count) from the forecast files on disk: every FINAL_NEXT_DRAW forecast for the target
        whose receipt froze before the target's deadline and whose forecast gives both tickets."""
        n = 35 if self.GAME == 'POWERBALL' else 47
        w, count = [0] * n, 0
        deadline = self.at(target)
        for folder in self.run_folders():
            f, r = folder / CP.FILES['forecast'], folder / CP.FILES['forecast_receipt']
            if not f.is_file():
                continue
            fc, rc = json.loads(f.read_bytes()), json.loads(r.read_bytes())
            if fc['target_draw_number'] != target or fc['run_mode'] != 'FINAL_NEXT_DRAW':
                continue
            if datetime.strptime(rc['frozen_at_utc'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc) >= deadline:
                continue
            main = fc['barrels']['MAIN']
            sides = [main['top'], main['worst']] + ([fc['barrels']['POWERBALL']['top'], fc['barrels']['POWERBALL']['worst']]
                                                    if self.GAME == 'POWERBALL' else [])
            if fc['record_status'] != 'PREDICTION_AVAILABLE' or any(s['status'] != 'PREDICTION_AVAILABLE' for s in sides):
                continue
            count += 1
            for j in main['top']['labels']:
                w[j - 1] += 1
            for j in main['worst']['labels']:
                w[j - 1] -= 1
        return w, count

    def oracle_x(self, target, weights):
        row = self.rows[-1]
        drawn = RD.read_outcome_rows(repo_root=self.proj, game_id=self.GAME, master_sha256=row['master_sha256'],
                                     targets=[target], ledger_version=row['version'])[target][0]
        return sum(weights[d - 1] for d in drawn)

    def check_counted(self, elig, factor, previous_sums):
        """One counted draw against the oracles: weights, V, X, each stored log-factor and the running sums."""
        t = elig['target_draw_number']
        w, count = self.oracle_weights(t)
        self.assertEqual((elig['weights'], elig['eligible_count']), (w, count))
        x = self.oracle_x(t, w)
        self.assertEqual(factor['x'], x)
        sums = []
        for a, lam in enumerate(NUM.LAMBDAS):
            stored = int(factor['log_factors'][a])
            ref = KT.reference_log_factor(w, lam, x)
            self.assertLessEqual(KT.dec(stored), ref)                         # never above the true factor
            self.assertLess(ref - KT.dec(stored), Decimal(2) / Decimal(10 ** 30))
            sums.append(previous_sums[a] + stored)
        self.assertEqual([int(v) for v in factor['running_logs']], sums)      # exact integer sums
        return sums


class Registration(Stream):
    def test_register_once_before_the_first_target(self):
        rec = self.register()
        self.assertEqual(rec['first_target'], self.m)
        self.assertEqual(rec['master_pin']['last_draw'], self.m - 1)          # no draw already made can ever enter
        self.assertEqual(rec['rules'], OV.RULES)
        self.assertEqual(rec['rules']['lambdas'], ['-1/5', '-1/10', '-1/20', '1/20', '1/10', '1/5'])
        self.assertEqual((rec['rules']['bar'], rec['rules']['kernel_margin']), (40, str(10 ** 20)))
        self.assertEqual(json.loads(OV.registration_path(self.proj, self.GAME).read_bytes()), rec)
        rows = [r for r in __import__('evaluation.report', fromlist=['x']).search_rows(self.GAME)
                if r['row_type'] == 'OV1_REGISTRATION']
        self.assertEqual([(r['plan_digest'], r['window_first']) for r in rows], [(record_digest(rec), str(self.m))])
        self.assertEqual(OV.status(self.GAME)['next_target'], self.m)
        (first,) = self.raw_rows()                                            # the registration, read back and confirmed
        self.assertEqual((first['kind'], first['confirms'], first['confirmed_digest']), ('CONFIRMED', 'REGISTRATION', record_digest(rec)))
        self.assertGreater(WR.parse_utc(first['confirmed_utc']), WR.parse_utc(rec['registered_utc']))
        self.assertTrue(OV.status(self.GAME)['registration_confirmed'])
        with self.assertRaises(OV.OV1Refused):                                # no second registration, ever
            self.register()
        self.assertEqual(self.record(), [])                                   # nothing is due before the cut-off

    def test_refusals(self):
        with self.assertRaises(OV.OV1Refused):
            OV.register(self.GAME, 'I register OV-1.')
        with self.assertRaises(OV.OV1Refused):                                # not registered: nothing to record
            self.record()
        with self.assertRaises(OV.OV1Refused):
            OV.stop(self.GAME, OV.STOP_STATEMENT)
        OR.developed_record_path(self.proj, self.GAME).unlink()
        with self.assertRaises(OV.OV1Refused):
            self.register()
        self.write_developed()
        marker = self.proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_bytes(b'{}')
        with self.assertRaises(OV.OV1Refused):
            self.register()
        marker.unlink()
        self.assertTrue(OR.absent(OV.registration_path(self.proj, self.GAME)))
        self.week(record=False)                                               # M is frozen: too late to start at M
        with self.assertRaises(OV.OV1Refused):
            self.register()

    def test_after_the_deadline_of_the_next_draw_it_refuses(self):
        self.now = self.at(self.m, minutes_before=-1)
        with self.assertRaises(OV.OV1Refused):
            self.register()

    def test_a_registration_under_other_rules_is_not_this_programs(self):
        rec = self.register()
        path, ledger = OV.registration_path(self.proj, self.GAME), OV.ledger_path(self.proj, self.GAME)
        confirmed = ledger.read_bytes()
        ledger.unlink()                                                       # as a registration no ledger has yet confirmed
        for change in ({'rules': dict(rec['rules'], bar=20)}, {'rules': dict(rec['rules'], kernel_margin='0')},
                       {'first_target': self.m - 1}, {'owner_statement': 'x'}, {'tool_version': 'MHUPB_OV1_V0'}):
            path.write_bytes(canonical(dict(rec, **change)))
            with self.assertRaises(OV.OV1Blocked):
                OV.status(self.GAME)
            with self.assertRaises(OV.OV1Blocked):
                self.record()
            self.assertTrue(OR.absent(ledger))
        path.write_bytes(canonical(rec)[:-1])                                 # not canonical bytes
        with self.assertRaises(OV.OV1Blocked):
            OV.status(self.GAME)
        # and the ledger pins the registration it confirmed: another valid registration in its place is not this stream's
        ledger.write_bytes(confirmed)
        later = WR.utc_text(WR.parse_utc(rec['registered_utc']) + timedelta(seconds=1))
        path.write_bytes(canonical(dict(rec, registered_utc=later)))
        with self.assertRaises(OV.OV1Blocked):
            OV.status(self.GAME)
        path.write_bytes(canonical(rec))
        self.assertTrue(OV.status(self.GAME)['registration_confirmed'])


class CutOff(Stream):
    def test_the_cutoff_is_never_after_noon_in_adelaide(self):
        """01:30 UTC on the draw's date, for every Tuesday and Thursday to the end of 2045, is 11:00 or 12:00 in
        Adelaide on the same date. Adelaide's rule, written out here: daylight time (UTC+10:30) from the first Sunday
        of October, 02:00 standard, to the first Sunday of April, 03:00 daylight; otherwise UTC+9:30."""
        def first_sunday(year, month):
            d = date(year, month, 1)
            return d + timedelta(days=(6 - d.weekday()) % 7)

        def adelaide(utc):
            start = datetime(utc.year, 10, first_sunday(utc.year, 10).day, 2, tzinfo=timezone(timedelta(hours=9, minutes=30)))
            end = datetime(utc.year, 4, first_sunday(utc.year, 4).day, 3, tzinfo=timezone(timedelta(hours=10, minutes=30)))
            daylight = utc >= start or utc < end
            return utc.astimezone(timezone(timedelta(hours=10, minutes=30) if daylight else timedelta(hours=9, minutes=30)))
        d, seen = date(2026, 11, 17), set()
        while d <= date(2045, 12, 31):
            if d.weekday() in (1, 3):
                local = adelaide(datetime(d.year, d.month, d.day, 1, 30, tzinfo=timezone.utc))
                self.assertEqual(local.date(), d)
                self.assertIn((local.hour, local.minute), ((11, 0), (12, 0)))
                seen.add(local.hour)
            d += timedelta(days=1)
        self.assertEqual(seen, {11, 12})
        for game, target in (('POWERBALL', 1600), ('OZLOTTO', 1700)):
            day = __import__('_common.game_profiles', fromlist=['x']).get_profile(game).derived_date(target)
            self.assertEqual(OV.cutoff(game, target), datetime(day.year, day.month, day.day, 1, 30, tzinfo=timezone.utc))

    def test_one_second_before_at_and_one_second_after(self):
        """The interruption exactly between the freeze line and the eligibility line (plan L5, section 7): the set is
        frozen, the recorder did not run. Resumed before the cut-off it writes the line; at or after it, the stop."""
        for seconds, kind in ((-1, 'ELIGIBILITY'), (0, 'STOP'), (1, 'STOP')):
            with self.subTest(seconds=seconds):
                self.tearDown()
                self.setUp()
                self.register()
                self.assertEqual(self.week(record=False)[0][-1], ('FROZE_NEXT', self.m))
                live = self.live_bytes()
                self.now = self.cut(self.m, seconds) - timedelta(milliseconds=1)     # the next reading is that instant
                self.assertEqual(self.record(), [(kind, self.m)])
                row = self.ov1_rows()[0]
                if kind == 'ELIGIBILITY':
                    self.assertLess(WR.parse_utc(row['written_utc']), self.cut(self.m))
                else:
                    self.assertEqual(row['cause'], 'ELIGIBILITY_NOT_VERIFIED')
                    self.assertIn('OV-1 eligibility NOT VERIFIED - PRIMARY STREAM STOP', row['detail'])
                    self.assertTrue(any('STREAM STOPPED' in s for s in OV.status_lines(self.GAME)))
                self.assertEqual(self.live_bytes(), live)                     # the freeze is never undone or changed
                self.assertEqual(self.record(), [])

    def test_the_cutoff_passing_while_the_line_is_prepared_is_a_stop(self):
        self.register()
        self.week(record=False)
        self.now = self.cut(self.m, -1)
        real = OV.eligibility_content

        def slow(*a, **kw):
            out = real(*a, **kw)
            self.now = self.cut(self.m, 2)                                    # the cut-off passes during the work
            return out
        with mock.patch.object(OV, 'eligibility_content', slow):
            self.assertEqual(self.record(), [('STOP', self.m)])
        self.assertEqual(self.ov1_rows()[0]['cause'], 'ELIGIBILITY_NOT_VERIFIED')

    def test_the_result_already_in_the_master_before_the_cutoff_writes_no_eligibility(self):
        self.register()
        self.week(record=False)
        self.grow([self.m])                                                   # (cannot happen under the stated schedule)
        before = self.ledger_bytes()
        with self.assertRaises(OV.OV1Blocked):
            self.record()
        self.assertEqual(self.ledger_bytes(), before)
        self.now = self.cut(self.m, 1)
        self.assertEqual(self.record(), [('STOP', self.m)])

    def test_a_freeze_line_written_after_the_cutoff_is_never_counted(self):
        """A next-draw set started in time, interrupted, and completed after the cut-off: its freeze line carries its
        own later time, so the target was fixed as missed at the cut-off and stays missed."""
        self.register()
        self.now = self.at(self.m, minutes_before=61)
        sid = self.open()['session_id']
        with B.fault_after(4), self.assertRaises(B.Boom):                     # SET_STARTED, OPEN, run, DONE, then dies
            self.next(sid)
        self.now = self.cut(self.m, 5)
        self.assertEqual(self.record(), [('MISSED', self.m)])
        self.resume_token(sid)
        self.open(resume=True)
        self.assertEqual(self.next(sid), ('FROZE_NEXT', self.m))              # completed late, under the same ticket
        line = self.lines()[-1]
        self.assertGreater(WR.parse_utc(line['frozen_utc']), self.cut(self.m))
        self.assertEqual(self.record(), [])                                   # never promoted
        self.assertEqual(self.kinds(), [('MISSED', self.m)])
        self.assertEqual(OV.verify(self.GAME)['missed'], 1)

    def test_the_same_late_line_seen_first_is_still_missed(self):
        self.register()
        self.now = self.at(self.m, minutes_before=61)
        sid = self.open()['session_id']
        with B.fault_after(4), self.assertRaises(B.Boom):
            self.next(sid)
        self.now = self.cut(self.m, 5)
        self.resume_token(sid)
        self.open(resume=True)
        self.assertEqual(self.next(sid), ('FROZE_NEXT', self.m))
        self.assertEqual(self.record(), [('MISSED', self.m)])


class Counted(Stream):
    def test_three_weeks_against_the_oracles(self):
        """Counted draws with a roster that changes and weights that follow the history (E_6 learns from every draw;
        E_7 is released for the third week), then verify."""
        self.register()
        self.assertEqual(self.week(), ([('FROZE_NEXT', self.m)], [('ELIGIBILITY', self.m)]))
        self.result(self.m)
        self.assertEqual(self.week()[1], [('FACTOR', self.m), ('ELIGIBILITY', self.m + 1)])
        self.result(self.m + 1)
        self.methods.add('E_7')
        self.assertEqual(self.week()[1], [('FACTOR', self.m + 1), ('ELIGIBILITY', self.m + 2)])
        self.result(self.m + 2)
        self.assertEqual(self.week()[1], [('FACTOR', self.m + 2), ('ELIGIBILITY', self.m + 3)])
        rows = self.ov1_rows()
        self.assertTrue(B.oracle_chain_ok(OV.ledger_path(self.proj, self.GAME)))
        sums = [0] * 6
        counts = []
        for elig, factor in zip(rows[0::2], rows[1::2]):
            self.assertEqual((elig['kind'], factor['kind']), ('ELIGIBILITY', 'FACTOR'))
            self.assertLess(WR.parse_utc(elig['written_utc']), self.cut(elig['target_draw_number']))
            self.assertEqual(elig['certificate'], 'PASS')
            sums = self.check_counted(elig, factor, sums)
            counts.append(elig['eligible_count'])
            self.assertFalse(factor['crossed'])
        self.assertGreater(counts[2], counts[0])                              # the roster grew
        self.assertNotEqual(rows[0]['weights'], rows[2]['weights'])           # the weights follow the history
        st = OV.status(self.GAME)
        self.assertEqual((st['counted'], st['skipped'], st['missed'], st['awaiting_score']), (3, 0, 0, self.m + 3))
        self.assertEqual(st['score_text'], NUM.fixed_text(NUM.mixture_lower(sums)))
        self.assertEqual(OV.verify(self.GAME), {'lines': 12, 'confirmed': 5, 'eligibility': 4, 'factor': 3, 'missed': 0, 'stop': 0})
        before = self.ledger_bytes()
        self.assertEqual(self.record(), [])                                   # idempotent: nothing twice
        self.assertEqual(self.ledger_bytes(), before)

    def test_only_complete_prospective_pairs_count(self):
        """Sup 6.1, on fabricated evidence: a failure record, a late record, a catch-up record and a forecast lacking a
        ticket contribute nothing; cancelling tickets give V = 0."""
        top, worst = list(range(1, 8)), list(range(8, 15))

        def ev(variant, *, kind='FORECAST', mode='FINAL_NEXT_DRAW', cls='PROSPECTIVE', t=top, w=worst, ok=('top', 'worst')):
            def side(name, labels):
                return {'status': 'PREDICTION_AVAILABLE' if name in ok else 'NO_PREDICTION', 'labels': labels}
            fc = {'record_status': 'PREDICTION_AVAILABLE',
                  'barrels': {'MAIN': {'top': side('top', t), 'worst': side('worst', w)},
                              'POWERBALL': {'top': side('top', [1]), 'worst': side('worst', [2])}}}
            return {'named': {'record_kind': kind, 'run_mode': mode, 'effective_class': cls, 'method_id': 'E_6',
                              'method_revision': '1', 'variant_id': variant, 'scored_record_digest': 'a' * 64},
                    'forecast': None if kind != 'FORECAST' else fc}
        good = ev('A')
        eligible, w = OV.tickets_to_weights('POWERBALL', [
            good, ev('B', kind='PREDICTION_FAILED'), ev('C', cls='LATE_PRE_DRAW'),
            ev('D', mode='CATCH_UP', cls='CATCH_UP'), ev('E', ok=('top',)), ev('F', ok=('worst',))])
        self.assertEqual([e[2] for e in eligible], ['A'])
        self.assertEqual(w, [1] * 7 + [-1] * 7 + [0] * 21)
        eligible, w = OV.tickets_to_weights('POWERBALL', [ev('A'), ev('B', t=worst, w=top)])
        self.assertEqual((len(eligible), w), (2, [0] * 35))                   # they cancel: V = 0, the registered skip
        for bad in (ev('A', t=top[:6]), ev('A', t=top[:6] + [1]), ev('A', w=[0] + worst[:6]), ev('A', t=top[:6] + [36])):
            with self.assertRaises(OR.RecordRefused):
                OV.tickets_to_weights('POWERBALL', [bad])

    def test_a_draw_with_no_prospective_pair_is_the_registered_skip(self):
        """Every record of the set froze after midnight, and the line before the cut-off: no PROSPECTIVE pair, V = 0.
        The skip is decided on the eligibility line, before the outcome, and its factor line (factor 1) follows at
        once; the stream then continues with the next draw."""
        self.register()
        self.now = self.at(self.m, minutes_before=61)
        sid = self.open()['session_id']
        real = WS.CR.run_contract_method

        def late(request, **kw):
            self.now = max(self.now, self.at(self.m, minutes_before=-5))
            return real(request, **kw)
        with mock.patch.object(WS.CR, 'run_contract_method', late):
            self.assertEqual(self.next(sid), ('FROZE_NEXT', self.m))
        self.assertEqual({r['effective_class'] for r in self.lines()[-1]['records']}, {'LATE_PRE_DRAW'})
        self.assertEqual(self.record(), [('ELIGIBILITY', self.m), ('FACTOR', self.m)])
        elig, factor = self.ov1_rows()
        self.assertEqual((elig['skip'], elig['eligible_count'], elig['variance'], elig['factor_table_digest']),
                         (True, 0, '0/1', None))
        self.assertEqual((factor['skipped'], factor['x'], factor['log_factors'], factor['counted_draws']),
                         (True, None, ['0'] * 6, 0))
        self.assertEqual(OV.status(self.GAME)['skipped'], 1)
        WS.close_session(self.GAME, sid)
        self.result(self.m)
        self.assertEqual(self.week()[1], [('ELIGIBILITY', self.m + 1)])
        self.assertEqual(OV.verify(self.GAME)['lines'], 6)


class Missed(Stream):
    EXTRA = 1                                     # one accepted, unforecast draw before M: the ledger gets a catch-up line

    def test_missed_weeks_then_a_counted_draw_in_order(self):
        self.register()
        self.assertEqual(self.record(), [])                                   # before the cut-off nothing is due
        self.now = self.cut(self.m, -1)
        self.assertEqual(self.record(), [])
        self.now = self.cut(self.m, 1)
        self.assertEqual(self.record(), [('MISSED', self.m)])                 # no session that week
        row = self.ov1_rows()[0]
        self.assertEqual((row['reason'], row['label']), ('MISSED_NO_FREEZE', 'RECORDED_AFTER_THE_CUTOFF_FROM_LOCAL_RECORDS'))
        self.assertGreaterEqual(WR.parse_utc(row['written_utc']), self.cut(self.m))
        self.assertEqual(self.record(), [])                                   # M + 1 is the open target now
        self.grow([self.m], [self.m + 1])                                     # two results accepted, still no session
        self.now = self.at(self.m + 2, hours_before=30)
        states, wrote = self.week()
        self.assertEqual(states, [('FROZE', self.first), ('FROZE', self.m), ('FROZE', self.m + 1), ('FROZE_NEXT', self.m + 2)])
        self.assertEqual(self.kinds(), [('MISSED', self.m), ('MISSED', self.m + 1), ('ELIGIBILITY', self.m + 2)])
        self.assertEqual({l['set_kind'] for l in self.lines()[:3]}, {'CATCH_UP_SET'})    # a catch-up line is never counted
        # the missed draws are forecast (N-1) and scored like any draw; they are simply not in the formal stream
        missed = [s for s in self.scores() if s['target_draw_number'] in (self.m, self.m + 1)]
        self.assertEqual(len(missed), 2 * len(self.lines()[1]['records']))
        self.assertTrue(all(s['effective_class'] == 'CATCH_UP' and s['readouts'] is not None for s in missed))
        self.result(self.m + 2)
        self.assertEqual(self.week()[1], [('FACTOR', self.m + 2), ('ELIGIBILITY', self.m + 3)])
        st = OV.status(self.GAME)
        self.assertEqual((st['counted'], st['missed'], st['score_text'] != '1.000000000000'), (1, 2, True))
        self.assertEqual(OV.verify(self.GAME)['missed'], 2)

    def missed_setup(self):
        """M counted (so the OV-1 ledger names a forecast-ledger extent and a freeze line), M + 1 missed-to-be: its
        result is accepted with no session, and the clock is past its cut-off."""
        self.register()
        self.week()
        self.result(self.m)
        sid = self.open()['session_id']
        self.assertEqual(self.next(sid), ('FROZE', self.m))
        self.score(sid, self.m)
        self.assertEqual(self.record(), [('FACTOR', self.m)])
        WS.close_session(self.GAME, sid)
        self.now = self.cut(self.m + 1, 60)
        return OR.forecast_ledger_path(self.proj, self.GAME), self.ledger_bytes()

    def test_every_reconciliation_failure_blocks_and_the_stream_resumes(self):
        """EX_225 RC-225-1: a missed line is refused, and the target blocked, when the forecast ledger is torn,
        truncated or replaced, its chain is broken, a time lies after the clock, or it conflicts with an extent or a
        freeze-line digest named earlier in the OV-1 ledger, the witness ledger or the score ledger."""
        path, ov_before = self.missed_setup()
        good = path.read_bytes()
        lines = [json.loads(x) for x in good.split(b'\n')[:-1]]

        def rechained(rows):
            out = []
            for r in rows:
                out.append(JL.chained({k: v for k, v in r.items() if k not in ('line_number', 'previous_line_digest')}, out))
            return b''.join(canonical(r) for r in out)
        later = dict(lines[-1], frozen_utc=WR.utc_text(self.now + timedelta(days=1)))
        earlier = dict(lines[0], closure_digest='d' * 64)
        faults = {
            'torn': good + b'{"schema": "FREEZE_LINE_V1", "to',
            'truncated (the line an eligibility line sealed is gone)': b''.join(canonical(r) for r in lines[:-1]),
            'chain broken': b''.join(canonical(r) for r in [lines[1], lines[0]]),
            'not canonical': good.replace(b'"schema"', b' "schema"', 1),
            'replaced by a consistent ledger with another first line': rechained([earlier] + lines[1:]),
            'a freeze time after the clock': rechained(lines[:-1] + [later]),
            'emptied': b'',
        }
        for name, raw in faults.items():
            with self.subTest(fault=name):
                path.write_bytes(raw)
                with self.assertRaises(OV.OV1Blocked):
                    self.record()
                self.assertEqual(self.ledger_bytes(), ov_before)              # nothing written, nothing passed over
        path.write_bytes(good)
        # a witness line and a score line that name a freeze line the ledger does not hold
        wpath = WR.witness_ledger_path(self.proj, self.GAME)
        wpath.write_bytes(canonical({'schema': WR.WITNESS_SCHEMA, 'kind': 'WITNESS_RECORDED', 'game_id': self.GAME,
                                     'target_draw_number': self.m + 1, 'freeze_line_digest': 'f' * 64,
                                     'witness_kind': 'github', 'ref': 'abc123', 'recorded_utc': WR.utc_text(self.now)}))
        with self.subTest(fault='a witness line for a freeze line of M + 1 that the ledger lacks'):
            with self.assertRaises(OV.OV1Blocked):
                self.record()
        wpath.unlink()
        spath = WR.score_ledger_path(self.proj, self.GAME)
        scores = spath.read_bytes()
        self.rewrite_scores(lambda i, s: dict(s, target_draw_number=self.m + 1) if i == 0 else s)
        with self.subTest(fault='a score line for M + 1, which has no freeze line'):
            with self.assertRaises(OV.OV1Blocked):
                self.record()
        spath.write_bytes(scores)
        self.assertEqual(self.ledger_bytes(), ov_before)
        self.assertEqual(self.record(), [('MISSED', self.m + 1)])             # resumes by itself once it verifies
        self.assertEqual(self.ov1_rows()[-1]['forecast_ledger_extent'], JL.extent(self.lines()))

    def test_a_freeze_time_later_than_the_clock_blocks(self):
        """Everything in the forecast ledger agrees with every earlier record, but its last freeze time is later than
        this program's clock (the clock went back): absence is not established, so the target is blocked."""
        self.missed_setup()
        t0 = self.now                                                         # after M + 1's cut-off
        self.grow([self.m + 1])
        self.now = t0 + timedelta(hours=2)
        sid = self.open()['session_id']
        self.assertEqual(self.next(sid), ('FROZE', self.m + 1))              # a catch-up line for M + 1, frozen at t0 + 2h
        self.now = t0 + timedelta(hours=1)                                    # the clock is now behind that line
        before = self.ledger_bytes()
        with self.assertRaises(OV.OV1Blocked):
            self.record()
        self.assertEqual(self.ledger_bytes(), before)
        self.now = t0 + timedelta(hours=3)
        self.assertEqual(self.record(), [('MISSED', self.m + 1)])

    def test_a_publication_manifest_that_names_a_lost_extent_blocks(self):
        """The league table's manifests (slice 3) are read through ov1.publication_names; here that reader is stood
        in for, to show a named extent or freeze line that is gone blocks the missed line."""
        path, ov_before = self.missed_setup()
        lines = self.lines()
        for name in ({'what': 'a publication manifest', 'lines': len(lines) + 1, 'last_line_digest': 'a' * 64},
                     {'what': 'a publication manifest', 'lines': len(lines), 'last_line_digest': 'a' * 64},
                     {'what': 'a publication manifest', 'target': self.m + 1, 'freeze_line_digest': 'a' * 64},
                     {'what': 'a publication manifest', 'target': self.m, 'freeze_line_digest': 'a' * 64}):
            with mock.patch.object(OV, 'publication_names', lambda root, game: [name]):
                with self.assertRaises(OV.OV1Blocked):
                    self.record()
        good = [{'what': 'm', **JL.extent(lines)}, {'what': 'm', 'target': self.m, 'freeze_line_digest': record_digest(lines[-1])}]
        with mock.patch.object(OV, 'publication_names', lambda root, game: good):
            self.assertEqual(self.record(), [('MISSED', self.m + 1)])


class Stops(Stream):
    def sealed_and_scored(self):
        """M is frozen and its eligibility sealed; its result is accepted and every record scored; the factor line is
        the next thing due. Returns the session id (still open)."""
        self.register()
        self.week()
        self.result(self.m)
        sid = self.open()['session_id']
        self.assertEqual(self.next(sid), ('FROZE', self.m))
        self.score(sid, self.m)
        return sid

    def after_a_stop(self, cause, sid, *, good_scores=None):
        """`good_scores`: the score ledger's bytes before a line was planted that the live path's own strict reader
        also refuses (slice 1); put back once the stop is recorded, to show forecasting then carries on."""
        if good_scores is not None:
            WR.score_ledger_path(self.proj, self.GAME).write_bytes(good_scores)
        self.assertEqual(self.kinds()[-1], ('STOP', self.m))
        self.assertEqual(self.ov1_rows()[-1]['cause'], cause)
        self.assertNotIn(('FACTOR', self.m), self.kinds())
        before = self.ledger_bytes()
        self.assertEqual(self.record(), [])                                   # stopped: nothing more, ever
        with self.assertRaises(OV.OV1Refused):
            self.register()                                                   # no second registration (OD-4)
        with self.assertRaises(OV.OV1Refused):
            OV.stop(self.GAME, OV.STOP_STATEMENT)
        self.assertEqual(self.next(sid), ('FROZE_NEXT', self.m + 1))          # forecasting carries on as normal
        WS.close_session(self.GAME, sid)
        self.result(self.m + 1)
        self.assertEqual(self.week()[1], [])                                  # and no line for any later target
        self.assertEqual(self.ledger_bytes(), before)
        self.assertEqual(OV.verify(self.GAME)['stop'], 1)
        self.assertEqual(OV.status(self.GAME)['stopped']['cause'], cause)

    def eligible_index(self):
        elig = self.ov1_rows()[0]
        keys = {(e[0], e[1], e[2]) for e in elig['eligible']}
        return [i for i, s in enumerate(self.scores())
                if s['target_draw_number'] == self.m and (s['method_id'], s['method_revision'], s['variant_id']) in keys]

    def test_x_by_matches_and_by_weights_must_agree(self):
        sid = self.sealed_and_scored()
        i = self.eligible_index()[0]

        def bump(j, s):
            if j == i:
                top = dict(s['readouts']['TOP'])
                top['main_matches'] = (top['main_matches'] + 1) % 8
                s['readouts'] = dict(s['readouts'], TOP=top)
            return s
        self.rewrite_scores(bump)
        self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('X_CONTRADICTION', sid)

    def test_eligible_score_lines_must_agree_about_the_draw(self):
        sid = self.sealed_and_scored()
        i = self.eligible_index()[0]
        other = [n for n in range(1, 36) if n not in self.scores()[i]['drawn_main']][:7]
        self.rewrite_scores(lambda j, s: dict(s, drawn_main=other) if j == i else s)
        self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('X_CONTRADICTION', sid)

    def test_x_outside_the_sealed_table_is_a_stop(self):
        sid = self.sealed_and_scored()
        real = NUM.factor_table

        def narrowed(w):
            t = real(w)
            x = sum(self.ov1_rows()[0]['weights'][d - 1] for d in self.scores()[self.eligible_index()[0]]['drawn_main'])
            t['counts'] = {k: v for k, v in t['counts'].items() if k != x}   # the observed X is not in the support
            return t
        with mock.patch.object(NUM, 'table_digest', lambda t: self.ov1_rows()[0]['factor_table_digest']), \
                mock.patch.object(NUM, 'factor_table', narrowed):
            self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('X_CONTRADICTION', sid)

    def test_a_score_line_that_is_not_the_frozen_records_is_a_stop(self):
        sid = self.sealed_and_scored()
        i = self.eligible_index()[0]
        good = WR.score_ledger_path(self.proj, self.GAME).read_bytes()
        self.rewrite_scores(lambda j, s: dict(s, scored_record_digest='9' * 64) if j == i else s)
        self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('SCORE_LINE_CONTRADICTION', sid, good_scores=good)

    def test_two_routine_score_lines_for_one_variant_is_a_stop(self):
        sid = self.sealed_and_scored()
        i = self.eligible_index()[0]
        path = WR.score_ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        path.write_bytes(good + canonical(dict(self.scores()[i], score_run_id='ws-' + '5' * 32)))
        self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('SCORE_LINE_CONTRADICTION', sid, good_scores=good)

    def test_a_draw_whose_date_is_not_its_derived_date_is_a_stop(self):
        sid = self.sealed_and_scored()
        self.rewrite_scores(lambda j, s: dict(s, draw_date_is_derived=False) if s['target_draw_number'] == self.m else s)
        self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('DRAW_DATE_NOT_DERIVED', sid)

    def test_a_table_that_is_not_the_sealed_one_is_a_stop(self):
        sid = self.sealed_and_scored()
        real = NUM.factor_table

        def shifted(w):
            t = real(w)
            x = min(t['rows'][0])
            t['rows'][0][x] += 1                                              # one stored value differs from the sealed table
            return t
        with mock.patch.object(NUM, 'factor_table', shifted):
            self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('FACTOR_TABLE_MISMATCH', sid)

    def test_a_table_that_cannot_be_rebuilt_is_a_stop(self):
        sid = self.sealed_and_scored()

        def refuse(w):
            raise NUM.Refuse('no bound')
        with mock.patch.object(NUM, 'factor_table', refuse):
            self.assertEqual(self.record(), [('STOP', self.m)])
        self.after_a_stop('FACTOR_TABLE_MISMATCH', sid)

    def test_a_replaced_forecast_ledger_blocks_a_sealed_draw_and_is_not_a_stop(self):
        """The freeze line an eligibility line sealed is gone from the forecast ledger (a consistent ledger with
        another line in its place): the input does not verify, so the draw is blocked, never stopped and never
        skipped; with the ledger back, the factor line is written."""
        sid = self.sealed_and_scored()
        path = OR.forecast_ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        line = json.loads(good.split(b'\n')[0])
        path.write_bytes(canonical(dict(line, closure_digest='d' * 64)))
        before = self.ledger_bytes()
        with self.assertRaises(OV.OV1Blocked):
            self.record()
        self.assertEqual(self.ledger_bytes(), before)
        path.write_bytes(good)
        self.assertEqual(self.record(), [('FACTOR', self.m)])

    def test_the_owners_stop_at_an_open_target_and_at_a_sealed_one(self):
        self.register()
        with self.assertRaises(OV.OV1Refused):
            OV.stop(self.GAME, 'stop it')
        line = OV.stop(self.GAME, OV.STOP_STATEMENT)
        self.assertEqual((line['cause'], line['target_draw_number'], line['owner_statement']),
                         ('OWNER_STOP', self.m, OV.STOP_STATEMENT))
        self.assertEqual(self.week()[1], [])
        path = OV.ledger_path(self.proj, self.GAME)                           # a line after a stop is not this program's
        good = path.read_bytes()
        rows = self.raw_rows()
        after = JL.chained({'schema': OV.LINE_SCHEMA, 'kind': 'MISSED', 'game_id': self.GAME, 'target_draw_number': self.m,
                            'registration_digest': rows[0]['registration_digest'],
                            'cutoff_utc': WR.utc_text(self.cut(self.m)), 'written_utc': WR.utc_text(self.cut(self.m, 5)),
                            'reason': OV.MISSED_REASON, 'label': OV.MISSED_LABEL,
                            'forecast_ledger_extent': JL.extent(self.lines())}, rows)
        path.write_bytes(good + canonical(after))
        with self.assertRaises(OV.OV1Blocked):
            OV.status(self.GAME)
        path.write_bytes(good)
        self.tearDown()
        self.setUp()
        sid = self.sealed_and_scored()                                        # sealed, scored, the factor not yet written
        OV.stop(self.GAME, OV.STOP_STATEMENT)
        self.after_a_stop('OWNER_STOP', sid)

    def test_what_is_not_a_stop_waits_or_blocks_and_never_skips(self):
        """A failure is never a skip (plan 6.6). A score line under another policy never enters OV-1; a corrupt score
        ledger blocks; a numerical refusal before the cut-off writes nothing. Each resumes when the input is right."""
        sid = self.sealed_and_scored()
        path = WR.score_ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        i = self.eligible_index()[0]
        # (a) the variant's only line is a corrective one under another policy: its routine score is "not yet written"
        self.rewrite_scores(lambda j, s: dict(s, scoring_policy_id='WEEKLY_SCORE_POLICY_V9', amendment_of='a' * 64)
                            if j == i else s)
        self.assertEqual(self.record(), [])
        self.assertEqual(OV.status(self.GAME)['awaiting_score'], self.m)
        # (b) the routine line AND a corrective line with other quantities: only the routine line is read
        amended = dict(self.scores()[i], amendment_of=record_digest(json.loads(good.split(b'\n')[i])))
        amended['readouts'] = dict(amended['readouts'], TOP=dict(amended['readouts']['TOP'], main_matches=7))
        path.write_bytes(good + canonical(amended))
        with mock.patch.object(OV.JL, 'append', lambda *a, **k: (_ for _ in ()).throw(AssertionError('no append here'))):
            step = OV.factor_step(self.GAME, WR.ROUTINE_POLICY, self.ov1_rows()[0], [0] * 6, 0, self.lines()[-1], self.scores())
        self.assertEqual(step[0], 'FACTOR')
        # (c) a corrupt line: blocked, nothing written
        for raw in (good + b'{"schema": "WEEKLY_SCORE_LINE_V1"}\n', good.replace(b'"schema"', b' "schema"', 1), good[:-40] + b'\n'):
            path.write_bytes(raw)
            with self.assertRaises(OV.OV1Blocked):
                self.record()
        self.assertEqual(self.kinds(), [('ELIGIBILITY', self.m)])
        path.write_bytes(good)
        self.assertEqual(self.record(), [('FACTOR', self.m)])                 # the same factor as if nothing had happened
        self.assertEqual(self.ov1_rows()[-1]['log_factors'], step[1]['log_factors'])
        # (d) the next draw: a numerical refusal before the cut-off writes nothing and is retried; no skip
        self.assertEqual(self.next(sid), ('FROZE_NEXT', self.m + 1))

        def refuse(w):
            raise NUM.Refuse('no bound')
        with mock.patch.object(NUM, 'factor_table', refuse):
            with self.assertRaises(OV.OV1Blocked):
                self.record()
        self.assertEqual(self.kinds()[-1], ('FACTOR', self.m))
        self.assertEqual(self.record(), [('ELIGIBILITY', self.m + 1)])


class Restart(Stream):
    def test_a_fault_after_each_append_then_a_rerun_gives_the_same_bytes(self):
        """Plan section 9, `record`: missed line, missed line, eligibility line and its confirmation in one run; then
        the factor line. With the clock held still, an interrupted and rerun record leaves exactly the bytes of an
        uninterrupted one."""
        self.register()
        path = OV.ledger_path(self.proj, self.GAME)
        first = path.read_bytes()                                             # the registration's confirmation
        self.grow([self.m], [self.m + 1])                                     # two weeks with no session
        self.now = self.at(self.m + 2, hours_before=30)
        self.assertEqual(self.week(record=False)[0][-1], ('FROZE_NEXT', self.m + 2))
        still = self.now + timedelta(minutes=1)
        with mock.patch.object(WR, 'now_utc', lambda: still):
            self.assertEqual(self.record(), [('MISSED', self.m), ('MISSED', self.m + 1), ('ELIGIBILITY', self.m + 2)])
            want = path.read_bytes()
            self.assertEqual([r['kind'] for r in self.raw_rows()], ['CONFIRMED', 'MISSED', 'MISSED', 'ELIGIBILITY', 'CONFIRMED'])
            for k in (1, 2, 3, 4):
                path.write_bytes(first)
                with B.fault_after(k) as steps, self.assertRaises(B.Boom):
                    self.record()
                self.assertEqual(len(path.read_bytes().split(b'\n')) - 1, k + 1)   # the k-th line is durable
                self.record()
                self.assertEqual(path.read_bytes(), want, k)
                self.assertEqual(self.record(), [])
        self.result(self.m + 2)
        sid = self.open()['session_id']
        self.next(sid)
        self.score(sid, self.m + 2)
        self.assertEqual(self.record(), [('FACTOR', self.m + 2)])
        want = path.read_bytes()
        path.write_bytes(b''.join(x + b'\n' for x in want.split(b'\n')[:5]))  # as if the factor line was never written
        with B.fault_after(1), self.assertRaises(B.Boom):
            self.record()
        self.assertEqual(self.record(), [])
        self.assertEqual(path.read_bytes(), want)                             # a factor line holds no time: same bytes
        self.assertEqual(OV.verify(self.GAME), {'lines': 6, 'confirmed': 2, 'eligibility': 1, 'factor': 1, 'missed': 2, 'stop': 0})

    def test_a_torn_last_line_is_kept_aside_and_the_line_is_written_again(self):
        self.register()
        self.week()
        path = OV.ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        path.write_bytes(good + b'{"schema": "OV1_LINE_V1", "kind": "FAC')
        self.assertEqual(self.kinds(), [('ELIGIBILITY', self.m)])             # the fragment is ignored by the reader
        self.result(self.m)
        self.assertEqual(self.week()[1], [('FACTOR', self.m), ('ELIGIBILITY', self.m + 1)])
        self.assertTrue(path.read_bytes().startswith(good))
        self.assertEqual(len(list(path.parent.glob(path.name + '.torn_*'))), 1)
        self.assertEqual(OV.verify(self.GAME)['lines'], 6)

    def test_verify_and_the_reader_catch_every_altered_line(self):
        self.register()
        self.week()
        self.result(self.m)
        self.week()
        path = OV.ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        rows = [json.loads(x) for x in good.split(b'\n')[:-1]]
        self.assertEqual([r['kind'] for r in rows], ['CONFIRMED', 'ELIGIBILITY', 'CONFIRMED', 'FACTOR', 'ELIGIBILITY', 'CONFIRMED'])
        c0, e1, c1, f1, e2, c2 = rows

        def rechained(new):
            """The lines chained afresh, each confirmation and factor line naming the eligibility line before it."""
            out, elig = [], None
            for r in new:
                r = {k: v for k, v in r.items() if k not in ('line_number', 'previous_line_digest')}
                if r['kind'] == 'FACTOR':
                    r['eligibility_line_digest'] = record_digest(elig)
                elif r['kind'] == 'CONFIRMED' and r['confirms'] == 'ELIGIBILITY' and elig is not None:
                    r['confirmed_digest'] = record_digest(elig)
                out.append(JL.chained(r, out))
                if r['kind'] == 'ELIGIBILITY':
                    elig = out[-1]
            return b''.join(canonical(r) for r in out)
        self.assertEqual(rechained(rows), good)
        w = list(e1['weights'])
        i, j = w.index(max(w)), w.index(min(w))
        w[i], w[j] = w[j], w[i]                                               # other weights with the same variance
        logs = [str(int(v) + 1) for v in f1['log_factors']]
        at_cut = WR.utc_text(self.cut(self.m))
        altered = {
            'a byte changed without the chain': good.replace(b'"skip":false', b'"skip":true', 1),
            'a line removed': b''.join(canonical(r) for r in rows[:1] + rows[2:]),
            'the factor line first': b''.join(canonical(r) for r in (c0, f1, e1, c1)),
            'log-factors raised, sums not': rechained([c0, e1, c1, dict(f1, log_factors=logs), e2, c2]),
            'crossed claimed': rechained([c0, e1, c1, dict(f1, crossed=True), e2, c2]),
            'a second eligibility line for the same draw': rechained([c0, e1, c1, dict(e1)]),
            'an eligibility line dated after its cut-off': rechained([c0, dict(e1, written_utc=WR.utc_text(self.cut(self.m, 1)))]),
            'a line of another registration': rechained([c0, dict(e1, registration_digest='a' * 64), c1, f1, e2, c2]),
            'an unknown field': rechained([c0, dict(e1, note='x'), c1, f1, e2, c2]),
            # EX_233 S2-F02: what the reader requires of the confirmations
            'no confirmation of the registration': rechained([e1, c1, f1, e2, c2]),
            'a factor line with no confirmation of its eligibility line': rechained([c0, e1, f1, e2, c2]),
            'a confirmation dated at its cut-off': rechained([c0, e1, dict(c1, confirmed_utc=at_cut), f1, e2, c2]),
            'a confirmation dated before the line it confirms': rechained(
                [c0, e1, dict(c1, confirmed_utc=WR.utc_text(WR.parse_utc(e1['written_utc']) - timedelta(seconds=1))), f1]),
            'a confirmation with another limit': rechained([c0, e1, dict(c1, limit_utc=WR.utc_text(self.cut(self.m, 60))), f1]),
            'two confirmations of one eligibility line': rechained([c0, e1, c1, dict(c1), f1, e2, c2]),
            'a second confirmation of the registration': rechained([c0, dict(c0), e1, c1, f1]),
            'a registration confirmed at its first target\'s cut-off': rechained([dict(c0, confirmed_utc=at_cut)]),
            'a confirmation of another record': b''.join(canonical(r) for r in (
                c0, e1, JL.chained({k: v for k, v in dict(c1, confirmed_digest='a' * 64).items()
                                    if k not in ('line_number', 'previous_line_digest')}, [c0, e1]))),
        }
        for name, raw in altered.items():
            with self.subTest(read=name):
                path.write_bytes(raw)
                with self.assertRaises(OV.OV1Blocked):
                    OV.status(self.GAME)
                with self.assertRaises(OV.OV1Blocked):
                    self.record()
                self.assertEqual(path.read_bytes(), raw)                      # blocked: nothing written
        # lines that are consistent with each other but not with the frozen tickets or the scores: verify finds them
        num, den = NUM.variance(w)
        self.assertEqual(f'{num}/{den}', e1['variance'])
        t = NUM.factor_table(e1['weights'])
        x_other = next(x for x in sorted(t['counts']) if x != f1['x'])
        new_logs = [str(row[x_other]) for row in t['rows']]
        consistent = {
            'other weights, self-consistent': [c0, dict(e1, weights=w), c1, f1, e2, c2],
            'another X with its own factors': [c0, e1, c1, dict(f1, x=x_other, log_factors=new_logs,
                                                                z=NUM.z_text(x_other, *t['variance']),
                                                                **OV._score_fields([int(v) for v in new_logs], 1)), e2, c2],
            'an eligible variant dropped': [c0, dict(e1, eligible=e1['eligible'][1:], eligible_count=e1['eligible_count'] - 1,
                                                     eligible_digest=record_digest({'eligible': e1['eligible'][1:]})),
                                            c1, f1, e2, c2],
        }
        for name, new in consistent.items():
            with self.subTest(verify=name):
                path.write_bytes(rechained(new))
                OV.status(self.GAME)                                          # the lines agree with each other
                with self.assertRaises(OV.OV1Blocked):
                    OV.verify(self.GAME)
        path.write_bytes(good)
        self.assertEqual(OV.verify(self.GAME)['lines'], 6)

    def test_the_bar(self):
        """The crossing is the kernel's integer comparison on the exact running sums; it is recorded on the line where
        it happens and the score runs on. Hand-built lines (the reader checks their arithmetic, not their history)."""
        reg = self.register()
        getc = lambda rows: OV.replay(reg, rows)
        w = [1] * 7 + [-1] * 7 + [0] * 21
        num, den = NUM.variance(w)
        KT.getcontext().prec = 90
        ln40 = int(KT.Decimal(40).ln() * KT.Decimal(10 ** 50))
        rows, sums = list(self.raw_rows()), [0] * 6                           # the registration's confirmation

        def pair(target, logs, counted):
            nonlocal sums
            base = {'schema': OV.LINE_SCHEMA, 'game_id': self.GAME, 'target_draw_number': target,
                    'registration_digest': record_digest(reg)}
            cut = OV.cutoff(self.GAME, target)
            elig = JL.chained({**base, 'kind': 'ELIGIBILITY', 'cutoff_utc': WR.utc_text(cut),
                               'written_utc': WR.utc_text(cut - timedelta(hours=20)), 'freeze_line_digest': 'a' * 64,
                               'freeze_line_number': 1, 'freeze_frozen_utc': WR.utc_text(cut - timedelta(hours=21)),
                               'forecast_ledger_extent': {'lines': 1, 'last_line_digest': 'a' * 64},
                               'eligible': [['E_6', '1', 'A', 'a' * 64]], 'eligible_count': 1,
                               'eligible_digest': record_digest({'eligible': [['E_6', '1', 'A', 'a' * 64]]}),
                               'weights': w, 'variance': f'{num}/{den}', 'skip': False, 'factor_table_digest': 'b' * 64,
                               'certificate': 'PASS', 'kernel_version': NUM.KERNEL_VERSION,
                               'master_pin': {'ledger_version': 2, 'master_sha256': 'c' * 64, 'last_draw': target - 1}}, rows)
            rows.append(elig)
            rows.append(JL.chained({**base, 'kind': 'CONFIRMED', 'confirms': 'ELIGIBILITY', 'confirmed_digest': record_digest(elig),
                                    'limit_utc': WR.utc_text(cut), 'confirmed_utc': elig['written_utc']}, rows))
            sums = [a + b for a, b in zip(sums, logs)]
            rows.append(JL.chained({**base, 'kind': 'FACTOR', 'eligibility_line_digest': record_digest(elig),
                                    'skipped': False, 'outcome_pins': [], 'x': 0, 'z': '0.000000000000',
                                    'log_factors': [str(v) for v in logs], **OV._score_fields(sums, counted)}, rows))
        pair(self.m, [ln40 - 10 ** 10] * 6, 1)                                # 1e-40 under log 40 in every component
        self.assertEqual((rows[-1]['crossed'], getc(rows)['first_crossing']), (False, None))
        self.assertTrue(rows[-1]['score_text'].startswith('39.999999999999'))
        pair(self.m + 1, [2 * 10 ** 10] * 6, 2)                               # now 1e-40 over
        self.assertEqual((rows[-1]['crossed'], getc(rows)['first_crossing']), (True, self.m + 1))
        pair(self.m + 2, [-10 ** 49] * 6, 3)                                  # the score runs on, and falls back
        self.assertEqual((rows[-1]['crossed'], getc(rows)['first_crossing']), (False, self.m + 1))
        OV.ledger_path(self.proj, self.GAME).write_bytes(b''.join(canonical(r) for r in rows))
        text = '\n'.join(OV.status_lines(self.GAME))
        self.assertIn(f'the score reached 40 at draw {self.m + 1}', text)
        self.assertIn('not proof of a cause', text)
        with self.assertRaises(OR.RecordRefused):                             # a crossing that the sums do not give
            getc(rows[:3] + [dict(rows[3], crossed=True)])


class Durability(Stream):
    """EX_233 S2-F02. A time written into a record is read from the clock BEFORE the record is durable, so a write that
    stalls across a limit would leave a late record with an in-time stamp. The registration and every eligibility line
    therefore count only with a CONFIRMED line, whose time is read AFTER the record was read back from disk. A record
    not confirmed before its limit is never used: the stream stops. The same holds across an interruption."""

    def stalled(self, kind, until):
        """`append` as installed, except that a line of `kind` becomes durable only as the clock reaches `until`."""
        real = OV.JL.append

        def append(path, record):
            raw = real(path, record)
            if record.get('kind') == kind:
                self.now = until
            return raw
        return mock.patch.object(OV.JL, 'append', append)

    def confirmations(self, what):
        return [r for r in self.raw_rows() if r['kind'] == 'CONFIRMED' and r['confirms'] == what]

    def test_an_eligibility_line_durable_after_its_cutoff_is_never_counted(self):
        self.register()
        self.week(record=False)
        self.now = self.cut(self.m, -5)                                       # five seconds before the cut-off
        with self.stalled('ELIGIBILITY', self.cut(self.m, 3)):                # the write completes three seconds after it
            self.assertEqual(self.record(), [('ELIGIBILITY', self.m), ('STOP', self.m)])
        elig, stop = self.ov1_rows()
        self.assertLess(WR.parse_utc(elig['written_utc']), self.cut(self.m))  # the line's own time says "in time"
        self.assertEqual((stop['cause'], self.confirmations('ELIGIBILITY')), ('ELIGIBILITY_NOT_VERIFIED', []))
        self.result(self.m)
        self.assertEqual(self.week()[1], [])                                  # the draw is forecast and scored as usual,
        self.assertTrue([s for s in self.scores() if s['target_draw_number'] == self.m])
        self.assertNotIn('FACTOR', [k for k, _t in self.kinds()])             # and never enters the formal stream
        self.assertEqual(OV.verify(self.GAME)['stop'], 1)

    def test_an_interrupted_eligibility_is_confirmed_in_time_or_the_stream_stops(self):
        for seconds in (-2, 2):                                               # the restart: before, or after, the cut-off
            with self.subTest(restart=seconds):
                self.tearDown()
                self.setUp()
                self.register()
                self.week(record=False)
                self.now = self.cut(self.m, -5)
                with B.fault_after(1), self.assertRaises(B.Boom):             # the process dies as the line lands
                    self.record()
                self.assertEqual((self.kinds(), self.confirmations('ELIGIBILITY')), ([('ELIGIBILITY', self.m)], []))
                self.assertEqual(OV.status(self.GAME)['awaiting_confirmation'], self.m)
                self.now = self.cut(self.m, seconds)
                self.record()
                in_time = seconds < 0
                self.assertEqual(self.kinds(), [('ELIGIBILITY', self.m)] + ([] if in_time else [('STOP', self.m)]))
                self.assertEqual(len(self.confirmations('ELIGIBILITY')), 1 if in_time else 0)
                self.result(self.m)
                self.assertEqual(('FACTOR', self.m) in self.week()[1], in_time)

    def test_a_registration_durable_too_late_never_becomes_a_stream(self):
        self.now = self.at(self.m, minutes_before=1)                          # a minute before the first target's deadline
        real = OR.write_record

        def slow(path, rec):
            raw = real(path, rec)
            self.now = self.at(self.m, minutes_before=-1)                     # the write completes a minute after it
            return raw
        with mock.patch.object(OV.OR, 'write_record', slow):
            rec = self.register()
        self.assertLess(WR.parse_utc(rec['registered_utc']), self.at(self.m))  # the record's own time says "in time"
        st = OV.status(self.GAME)
        self.assertEqual((st['stopped']['cause'], st['registration_confirmed']), ('REGISTRATION_NOT_VERIFIED', False))
        self.assertEqual(self.week()[1], [])                                  # no line ever follows; forecasting is as usual
        with self.assertRaises(OV.OV1Refused):
            self.register()                                                   # and there is no second registration

    def test_an_interrupted_registration_is_confirmed_in_time_or_the_stream_stops(self):
        for case in ('in time', 'after the deadline', 'after the first target is frozen'):
            with self.subTest(restart=case):
                self.tearDown()
                self.setUp()
                with mock.patch.object(OV, 'record', side_effect=B.Boom('the process dies')), self.assertRaises(B.Boom):
                    self.register()
                self.assertEqual(self.ledger_bytes(), b'')                    # the registration is on disk, unconfirmed
                self.assertFalse(OV.status(self.GAME)['registration_confirmed'])
                if case == 'after the deadline':
                    self.now = self.at(self.m, minutes_before=-1)
                elif case == 'after the first target is frozen':
                    self.week(record=False)
                self.record()
                st = OV.status(self.GAME)
                if case == 'in time':
                    self.assertEqual((st['registration_confirmed'], st['stopped'], len(self.confirmations('REGISTRATION'))), (True, None, 1))
                    self.assertEqual(self.week()[1], [('ELIGIBILITY', self.m)])
                else:
                    self.assertEqual((st['registration_confirmed'], st['stopped']['cause']), (False, 'REGISTRATION_NOT_VERIFIED'))
                    self.assertEqual(self.record(), [])


class Isolation(Stream):
    def test_no_failure_of_the_recorder_changes_the_live_records(self):
        """Plan section 7, the L5 rows: record raising before the eligibility line and between eligibility and factor;
        the OV-1 ledger unreadable or its chain broken. The session, forecast, score and run records stay byte for
        byte, and the stream continues once the fault is gone."""
        self.register()
        self.assertEqual(self.week(record=False)[0][-1], ('FROZE_NEXT', self.m))
        live, base = self.live_bytes(), self.ledger_bytes()
        with mock.patch.object(OV, 'eligibility_content', side_effect=RuntimeError('fault')), self.assertRaises(RuntimeError):
            self.record()
        self.assertEqual((self.live_bytes(), self.ledger_bytes()), (live, base))
        self.assertEqual(self.record(), [('ELIGIBILITY', self.m)])            # rerun before the cut-off writes the line
        self.result(self.m)
        sid = self.open()['session_id']
        self.next(sid)
        self.score(sid, self.m)
        live = self.live_bytes()
        path = OV.ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        with mock.patch.object(OV, 'factor_step', side_effect=RuntimeError('fault')), self.assertRaises(RuntimeError):
            self.record()
        for raw in (good[:-2] + b'\n', b'not json\n', good + good):           # unreadable; unreadable; chain broken
            path.write_bytes(raw)
            with self.assertRaises(OV.OV1Blocked):
                self.record()
            self.assertEqual(path.read_bytes(), raw)
        self.assertEqual(self.live_bytes(), live)
        self.assertEqual(self.next(sid), ('FROZE_NEXT', self.m + 1))          # the live path does not look at OV-1
        path.write_bytes(good)
        self.assertEqual(self.record(), [('FACTOR', self.m), ('ELIGIBILITY', self.m + 1)])

    def test_statics(self):
        """OV-1 reads no master and no outcome, uses no float, and the live path's modules do not import it."""
        src = Path(OV.__file__).resolve().parent
        tree = ast.parse((src / 'ov1.py').read_text(encoding='ascii'))
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | \
                {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {a.name for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported |= {f'{node.module or "."}.{a.name}' for a in node.names}
            if isinstance(node, ast.Constant):
                self.assertNotIsInstance(node.value, float)
        self.assertEqual(names & {'outcome_reader', 'read_outcomes', 'read_outcome_rows', 'load_verified_source',
                                  'check_source', 'float', 'Decimal', 'Fraction', 'unlink', 'rmtree', 'write_bytes',
                                  'write_text', 'truncate'}, set())
        self.assertEqual(imported, {
            '__future__.annotations', 'datetime.datetime', 'datetime.timezone', 'pathlib.Path',
            '_common.contract_publication', '_common.contract_runner', '_common.jsonl_ledger', '_common.master_versions',
            '_common.owner_records', '_common.score_identities', '_common.walk_forward', '_common.weekly_records',
            '_common.contract_records.canonical', '_common.contract_records.record_digest',
            '_common.contract_records.sha256_hex', '_common.game_profiles.get_profile', '..collect', '..ov1_numeric'})
        common = src.parent / 'methods' / '_common'
        for live in (common / 'weekly_session.py', common / 'weekly_records.py', common / 'score_identities.py',
                     common / 'jsonl_ledger.py', src / 'weekly_score.py', src.parent / 'methods' / 'Method_Weekly_Forecast.py',
                     src / 'Method_Weekly_Score.py'):
            self.assertNotIn('ov1', live.read_text(encoding='ascii').lower(), live.name)

    def test_commands_exit_codes_and_the_last_line(self):
        import contextlib
        import io
        from evaluation import Method_OV1 as M

        def run(*argv):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = M.main(list(argv))
            return code, buf.getvalue().strip().splitlines()[-1]
        g = ('--game', self.GAME)
        self.assertEqual(run('status', *g), (2, f'[OV1] RESULT state=REFUSED game={self.GAME} next=-'))
        self.assertEqual(run('register', *g, '--statement', 'no'), (2, f'[OV1] RESULT state=REFUSED game={self.GAME} next=-'))
        self.assertEqual(run('register', *g, '--statement', OV.REGISTRATION_STATEMENT),
                         (0, f'[OV1] RESULT state=REGISTERED game={self.GAME} next={self.m}'))
        self.assertEqual(run('record', *g), (0, f'[OV1] RESULT state=NOTHING_DUE game={self.GAME} next={self.m}'))
        self.week(record=False)
        self.assertEqual(run('record', *g), (0, f'[OV1] RESULT state=RECORDED game={self.GAME} next={self.m}'))
        self.assertEqual(run('status', *g), (0, f'[OV1] RESULT state=STATUS game={self.GAME} next={self.m}'))
        self.assertEqual(run('verify', *g), (0, f'[OV1] RESULT state=VERIFIED game={self.GAME} next=-'))
        path = OV.ledger_path(self.proj, self.GAME)
        good = path.read_bytes()
        path.write_bytes(b'x\n')
        self.assertEqual(run('record', *g), (1, f'[OV1] RESULT state=BLOCKED game={self.GAME} next=-'))
        path.write_bytes(good)
        self.assertEqual(run('stop', *g, '--statement', OV.STOP_STATEMENT),
                         (0, f'[OV1] RESULT state=STOPPED game={self.GAME} next={self.m}'))
        self.assertEqual(run('record', *g), (0, f'[OV1] RESULT state=STOPPED game={self.GAME} next={self.m}'))


class OzLotto(Stream):
    GAME = 'OZLOTTO'

    def test_the_other_game_has_its_own_stream(self):
        """Games are never pooled: Oz Lotto's stream on its own barrel of 47, its own registration and ledger."""
        self.register()
        self.week()
        self.result(self.m)
        self.assertEqual(self.week()[1], [('FACTOR', self.m), ('ELIGIBILITY', self.m + 1)])
        rows = self.ov1_rows()
        self.assertEqual(len(rows[0]['weights']), 47)
        self.check_counted(rows[0], rows[1], [0] * 6)
        self.assertTrue(OR.absent(OV.ledger_path(self.proj, 'POWERBALL')))
        self.assertEqual(OV.verify(self.GAME)['lines'], 6)


if __name__ == '__main__':
    import unittest
    unittest.main()
