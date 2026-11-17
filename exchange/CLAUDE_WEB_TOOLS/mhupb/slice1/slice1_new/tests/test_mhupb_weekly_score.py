"""MHUP-B slice 1, layer L3: the scoring half of the weekly session and the outcome reader's weekly release rule (design
v0.1r7 sections 5.3, 6.3, 6.5, 6.6, Appendices E, G, I and L; code plan v0.3 section 5, L3). OFFLINE and INVENTED: see
mhupb_fixtures.

What is shown (the design's test names in brackets):
- the quantities of a score line against an oracle that reads the invented master itself; the drawn numbers, the
  exposure flags and the date flag;
- a line frozen by one session at one master version and scored by a later session at a newer one: bound to the first
  session's line, training pin and outcome pin both recorded [L-W2];
- the freeze-before-outcome rule for a draw after the holdout: no freeze line, no developed record, a draw the master
  does not hold, and each kind of evidence that does not verify (a changed forecast, a missing DONE ticket, a changed
  session record, a changed freeze line) refuse, serve no outcome and write no score byte;
- one routine score per scientific identity, whatever the score run id or the scoring session [L-S1]; a crash mid-score
  resumes with the unscored records only; a failure record gets its line, with no quantities;
- the witness ledger [L-V1 to L-V3] and the publication status derived from it;
- diagnostic-score serves only diagnostic records and writes no byte [L-G2, L-G3];
- the command line; no network and no process control in any routine command (static).
"""
from __future__ import annotations

import ast
import contextlib
import csv
import io
import json
import unittest
from datetime import timedelta
from pathlib import Path
from unittest import mock

import mhupa_fixtures as X
import mhupb_fixtures as B
import _common.contract_runner as CR
import _common.weekly_records as WR
import _common.weekly_session as WS
from _common import jsonl_ledger as JL
from _common import owner_records as OR
from _common import score_identities as SI
from _common.contract_records import canonical, record_digest
from evaluation import outcome_reader as RD
from evaluation import weekly_score as SC

ROOT = Path(__file__).resolve().parents[1]
EVALUATOR_SIDE = ('src/evaluation/weekly_score.py', 'src/evaluation/Method_Weekly_Score.py')


def master_row(proj: Path, game: str, target: int) -> dict:
    """The oracle's own reading of the invented master (no project code): the target's date and numbers."""
    with (proj / 'source_data' / f'{game}_results_master.csv').open(newline='') as fh:
        for row in csv.reader(fh):
            if row[0] == str(target):
                return {'date': row[1], 'main': sorted(int(x) for x in row[2:9]),
                        'extra': int(row[9]) if game == 'POWERBALL' else sorted(int(x) for x in row[9:12])}
    raise AssertionError('no such draw in the invented master')


class Quantities(B.Weekly):

    def test_every_score_line_against_the_master_and_the_frozen_forecast(self):
        sid, _states = self.session()
        scores = self.scores()
        self.assertEqual(len(scores), 6)
        folders = {f.name: f for f in self.run_folders()}
        for s in scores:
            row = master_row(self.proj, self.GAME, s['target_draw_number'])
            self.assertEqual(s['drawn_main'], row['main'])
            self.assertEqual(s['drawn_powerball'], row['extra'] if self.GAME == 'POWERBALL' else None)
            self.assertEqual(s['draw_date_is_derived'], row['date'] == self.p.derived_date(s['target_draw_number']).isoformat())
            self.assertTrue(s['draw_date_is_derived'])
            forecast = json.loads((folders[s['run_id']] / 'forecast.json').read_bytes())
            self.assertEqual(forecast['canonical_content_digest'], s['scored_record_digest'])
            self.assertEqual(forecast['target_draw_number'], s['target_draw_number'])
            for readout, side in (('TOP', 'top'), ('WORST', 'worst')):
                labels = forecast['barrels']['MAIN'][side]['labels']
                got = s['readouts'][readout]
                self.assertEqual(got['main_matches'], len(set(labels) & set(row['main'])))
                if self.GAME == 'POWERBALL':
                    self.assertEqual(got['powerball_match'], int(forecast['barrels']['POWERBALL'][side]['labels'][0] == row['extra']))
                else:
                    self.assertEqual(got['supplementary_matches'], len(set(labels) & set(row['extra'])))
                    self.assertNotIn('powerball_match', got)
            self.assertEqual((s['scoring_policy_id'], s['amendment_of'], s['scoring_session_id']),
                             ('WEEKLY_SCORE_POLICY_V1', None, sid))
            self.assertEqual((s['effective_class'], s['tier'], s['run_mode'], s['missing_batch']),
                             ('CATCH_UP', 'CATCH_UP', 'CATCH_UP', True))
            self.assertEqual(s['exposure_flag'], OR.exposure_flag(self.GAME, s['target_draw_number']))
            self.assertIsNotNone(s['rank'])
        flags = {s['target_draw_number']: s['exposure_flag'] for s in scores}
        if self.GAME == 'POWERBALL':                         # 1587 and 1588 carry HX-2, whatever their label (6.4)
            self.assertEqual(flags, {1587: {'record': OR.EXPOSURE_RECORD, 'decision': 'HX-2'},
                                     1588: {'record': OR.EXPOSURE_RECORD, 'decision': 'HX-2'}})
        else:
            self.assertEqual(set(flags.values()), {None})
        # the Oz Lotto supplementaries themselves are never stored (R2 2.5)
        text = WR.score_ledger_path(self.proj, self.GAME).read_text(encoding='ascii')
        self.assertNotIn('drawn_supplementar', text)

    def test_a_date_off_the_weekly_rule_is_flagged(self):
        sid = self.open()['session_id']
        self.next(sid)
        real = RD.read_outcome_rows

        def off_date(**kw):
            return {t: (main, extra, '1999-01-01') for t, (main, extra, _d) in real(**kw).items()}
        with mock.patch.object(SC.RD, 'read_outcome_rows', off_date):
            self.score(sid, self.first)
        self.assertEqual({s['draw_date_is_derived'] for s in self.scores()}, {False})


class QuantitiesOzLotto(Quantities):
    GAME = 'OZLOTTO'


class AcrossWeeks(B.Weekly):
    EXTRA = 0

    def test_a_line_of_one_session_scored_by_a_later_one_at_a_newer_master(self):          # L-W2
        s1, states = self.session()
        self.assertEqual(states, [('FROZE_NEXT', self.first)])
        line = self.lines()[0]
        self.assertEqual(SC.RD.outcome_release_allowed(self.proj, self.GAME, self.first), False)     # not yet accepted
        self.grow([self.first])
        self.now = self.at(self.first + 1, hours_before=40)
        s2 = self.open()['session_id']
        self.assertEqual(self.next(s2), ('FROZE', self.first))
        self.score(s2, self.first)
        for s in self.scores():
            self.assertEqual((s['training_ledger_version'], s['training_master_sha256']), (2, self.rows[1]['master_sha256']))
            self.assertEqual((s['outcome_ledger_version'], s['outcome_master_sha256']), (3, self.rows[2]['master_sha256']))
            self.assertEqual((s['scoring_session_id'], s['freeze_line_digest'], s['freeze_line_number']),
                             (s2, record_digest(line), 1))
            self.assertEqual((s['effective_class'], s['run_mode']), ('PROSPECTIVE', 'FINAL_NEXT_DRAW'))
        self.assertEqual({r['session_id'] for r in self.lines()[0]['records']}, {s1})
        self.assertEqual(OR.forecast_ledger_path(self.proj, self.GAME).read_bytes(), canonical(line))  # the line untouched


class ReleaseRule(B.Weekly):
    EXTRA = 2

    def outcome(self, target):
        return RD.read_outcomes(repo_root=self.proj, game_id=self.GAME, master_sha256=self.rows[-1]['master_sha256'],
                                targets=[target], ledger_version=self.rows[-1]['version'])

    def refused_everywhere(self, sid, target, pattern=None):
        """The rule says no, the reader serves nothing, and the scorer writes nothing."""
        before = self.weekly_bytes()
        self.assertFalse(RD.outcome_release_allowed(self.proj, self.GAME, target))
        with self.assertRaises(RD.OutcomeRefused):
            self.outcome(target)
        with self.assertRaises(SC.ScoreRefused) as cm:
            self.score(sid, target)
        if pattern:
            self.assertRegex(str(cm.exception), pattern)
        self.assertEqual(self.weekly_bytes(), before)

    def test_no_freeze_line_no_outcome_and_the_other_refusals(self):
        self.assertEqual(self.outcome(self.p.holdout_first - 1)[self.p.holdout_first - 1][0][0] > 0, True)   # the prefix
        for t in (self.p.holdout_first, self.p.holdout_last):                 # the holdout: Mode H's rule, unchanged
            self.assertFalse(RD.outcome_release_allowed(self.proj, self.GAME, t))
            with self.assertRaises(RD.OutcomeRefused):
                self.outcome(t)
        sid = self.open()['session_id']
        self.refused_everywhere(sid, self.first, 'no freeze line')
        self.assertEqual(self.next(sid), ('FROZE', self.first))
        self.assertTrue(RD.outcome_release_allowed(self.proj, self.GAME, self.first))
        self.assertEqual(self.outcome(self.first)[self.first][0], tuple(master_row(self.proj, self.GAME, self.first)['main']))
        self.refused_everywhere(sid, self.first + 1, 'no freeze line')        # accepted, not yet frozen
        self.refused_everywhere(sid, self.first + 2)                          # the next draw: the master does not hold it
        self.refused_everywhere(sid, 'x')
        developed = OR.developed_record_path(self.proj, self.GAME)
        developed.rename(self.td / 'd.json')
        self.assertFalse(RD.outcome_release_allowed(self.proj, self.GAME, self.first))
        with self.assertRaises(RD.OutcomeRefused):
            self.outcome(self.first)
        (self.td / 'd.json').rename(developed)
        with self.assertRaisesRegex(SC.ScoreRefused, 'not the game\'s active session'):
            self.score('f' * 32, self.first)
        marker = CR.ORPHAN_MARKER
        marker.parent.mkdir(parents=True)
        marker.write_text('{}')
        with self.assertRaisesRegex(SC.ScoreRefused, 'UNRESOLVED_ORPHAN_MARKER'):
            self.score(sid, self.first)
        marker.unlink()
        self.assertEqual(self.scores(), [])
        self.score(sid, self.first)
        self.assertEqual(len(self.scores()), 3)
        self.assertEqual(self.loop(sid)[-1], ('FROZE_NEXT', self.first + 2))
        # the next draw is frozen and open: its result is not in the scoring session's master, so it is not scored
        self.refused_everywhere(sid, self.first + 2, 'no accepted result')

    def test_evidence_that_does_not_verify_serves_no_outcome(self):
        sid = self.open()['session_id']
        self.next(sid)
        line = self.lines()[0]
        folder = [f for f in self.run_folders() if f.name == line['records'][0]['run_id']][0]
        attempts = OR.session_attempts_path(self.proj, self.GAME, sid)
        session = OR.session_record_path(self.proj, self.GAME, sid)
        ledger = OR.forecast_ledger_path(self.proj, self.GAME)

        def changed_forecast():
            rec = json.loads((folder / 'forecast.json').read_bytes())
            rec['barrels']['MAIN']['top']['labels'] = rec['barrels']['MAIN']['worst']['labels']
            (folder / 'forecast.json').write_bytes(canonical(rec))

        def missing_done_ticket():
            rows = attempts.read_bytes().split(b'\n')[:-1]
            attempts.write_bytes(b'\n'.join(r for r in rows if b'"kind":"DONE"' not in r or
                                            line['records'][0]['run_id'].encode() not in r) + b'\n')

        def changed_session_record():
            rec = json.loads(session.read_bytes())
            rec['roster'][0]['release_date'] = '2025-01-01'
            session.write_bytes(canonical(rec))

        def changed_freeze_line():
            rec = json.loads(ledger.read_bytes())
            rec['records'][0]['scored_record_digest'] = '0' * 64
            ledger.write_bytes(canonical(rec))

        def no_terminal_record():
            (folder / 'terminal.json').rename(folder / 'gone.json')

        def a_second_done_ticket():
            t = [json.loads(r) for r in attempts.read_bytes().split(b'\n')[:-1] if b'"kind":"DONE"' in r][0]
            attempts.write_bytes(attempts.read_bytes() + canonical(dict(t, utc='2030-01-01T00:00:00Z')))
        self.assertTrue((folder / 'terminal.json').is_file())
        for plant in (changed_forecast, missing_done_ticket, changed_session_record, changed_freeze_line,
                      no_terminal_record, a_second_done_ticket):
            with self.subTest(defect=plant.__name__):
                saved = self.weekly_bytes()
                plant()
                self.refused_everywhere(sid, self.first)
                for name, raw in saved.items():
                    (self.proj / name).write_bytes(raw)
                (folder / 'gone.json').unlink(missing_ok=True)
                self.assertTrue(RD.outcome_release_allowed(self.proj, self.GAME, self.first))
        self.score(sid, self.first)
        self.assertEqual(len(self.scores()), 3)


class ScoringGuards(B.Weekly):
    EXTRA = 1

    def test_one_routine_score_per_identity_whatever_the_run_or_session(self):             # L-S1
        sid = self.open()['session_id']
        self.next(sid)
        out = []
        self.assertEqual(self.score(sid, self.first, out)['scored'], 3)
        good = WR.score_ledger_path(self.proj, self.GAME).read_bytes()
        again = self.score(sid, self.first, out)
        self.assertEqual((again['scored'], again['already']), (0, 3))
        self.assertIn('already scored; nothing written', out[-1])
        self.clear_lock()
        s2 = self.open()['session_id']                                   # another scoring session, another score run id
        self.assertEqual(self.score(s2, self.first)['scored'], 0)
        self.assertEqual(WR.score_ledger_path(self.proj, self.GAME).read_bytes(), good)
        self.assertEqual(len({s['score_run_id'] for s in self.scores()}), 1)
        dup = dict(self.scores()[0], score_run_id='ws-' + 'a' * 32)       # a second routine line planted by hand
        WR.score_ledger_path(self.proj, self.GAME).write_bytes(good + canonical(dup))
        with self.assertRaisesRegex(SC.ScoreRefused, 'scored twice'):
            self.score(s2, self.first)
        with self.assertRaisesRegex(WS.SessionRefused, 'scored twice'):
            self.next(s2)

    def test_a_crash_mid_score_resumes_with_the_unscored_records_only(self):
        sid = self.open()['session_id']
        self.next(sid)
        with B.fault_after(2), self.assertRaises(B.Boom):
            self.score(sid, self.first)
        first_two = WR.score_ledger_path(self.proj, self.GAME).read_bytes()
        self.assertEqual(first_two.count(b'\n'), 2)
        self.assertEqual(self.next(sid), ('FROZE', self.first))          # still unclosed; nothing is forecast again
        got = self.score(sid, self.first)
        self.assertEqual((got['scored'], got['already']), (1, 2))
        self.assertTrue(WR.score_ledger_path(self.proj, self.GAME).read_bytes().startswith(first_two))
        self.assertEqual(len(SI.scored_identities(self.proj, self.GAME)), 3)
        self.assertEqual(self.next(sid), ('FROZE_NEXT', self.first + 1))

    def test_a_failure_record_is_named_scored_as_missing_and_never_run_again(self):
        sid = self.open()['session_id']
        real = CR.run_contract_method
        calls = []

        def fail_first(request, **kw):
            calls.append(request['variant_id'])
            if len(calls) == 1:
                def broken(task, view):
                    raise RuntimeError('planted method failure')
                return real(request, **dict(kw, compute=broken))
            return real(request, **kw)
        with mock.patch.object(WS.CR, 'run_contract_method', fail_first):
            self.assertEqual(self.next(sid), ('FROZE', self.first))
        line = self.lines()[0]
        failed = [r for r in line['records'] if r['record_kind'] == 'PREDICTION_FAILED']
        self.assertEqual([(r['variant_id'], r['terminal_class'], r['effective_class'], r['frozen_at_utc']) for r in failed],
                         [(calls[0], 'RUNTIME_FAILURE METHOD_FAILED', 'CATCH_UP', None)])
        self.score(sid, self.first)
        lines = {s['variant_id']: s for s in self.scores()}
        self.assertEqual((lines[calls[0]]['record_kind'], lines[calls[0]]['readouts'], lines[calls[0]]['rank']),
                         ('PREDICTION_FAILED', None, None))
        self.assertEqual(sum(1 for s in lines.values() if s['readouts'] is not None), 2)
        self.assertEqual(self.next(sid), ('FROZE_NEXT', self.first + 1))  # closed: the failure is not run again
        self.assertEqual(len([f for f in self.run_folders()]), 6)


class Witness(B.Weekly):
    EXTRA = 0

    def test_witness_lines_and_the_derived_publication_status(self):                       # L-V1 to L-V3
        m = self.first
        self.now = self.at(m, minutes_before=61)
        sid = self.open()['session_id']
        real = CR.run_contract_method
        n = []

        def slow(request, **kw):
            n.append(1)
            if len(n) == 3:
                self.now = self.at(m, minutes_before=-5)
            return real(request, **kw)
        with mock.patch.object(WS.CR, 'run_contract_method', slow):
            self.next(sid)                                               # two PROSPECTIVE records and one LATE_PRE_DRAW
        line = self.lines()[0]
        status = lambda: WR.publication_status(self.GAME, self.lines()[0], WR.witness_ledger(self.proj, self.GAME))
        self.assertEqual(status(), ('TIMELINESS_UNVERIFIED', 'no witness'))
        for bad in (dict(target=m + 1), dict(kind='carrier-pigeon'), dict(ref='  '), dict(ref='caf\xe9')):
            args = dict(target=m, kind='github', ref='abc123def')
            args.update(bad)
            with self.subTest(bad=bad), self.assertRaises(SC.ScoreRefused):
                SC.witness(self.GAME, args['target'], args['kind'], args['ref'])
        before = (self.td / 'x').exists()
        receipt = 'PushEvent created_at 2026-10-13T11:00:00Z commit abc123def'
        with self.assertRaisesRegex(SC.ScoreRefused, 'record the witness first'):
            SC.verify(self.GAME, m, 'reviewer', '2026-10-13T11:00:00Z', receipt)
        self.assertFalse(WR.witness_ledger_path(self.proj, self.GAME).exists() or before)
        w = SC.witness(self.GAME, m, 'github', 'abc123def')
        self.assertEqual((w['freeze_line_digest'], w['kind']), (record_digest(line), 'WITNESS_RECORDED'))
        self.assertEqual(status(), ('TIMELINESS_UNVERIFIED', 'witness recorded, not verified'))
        early = WR.utc_text(self.at(m, hours_before=1))
        for bad in (dict(evidence=''), dict(evidence='a receipt that names another commit'), dict(verified_by='Dana'),
                    dict(received_utc='yesterday'), dict(target=m + 1)):
            args = dict(target=m, verified_by='reviewer', received_utc=early, evidence=receipt)
            args.update(bad)
            with self.subTest(bad=bad), self.assertRaises(SC.ScoreRefused):
                SC.verify(self.GAME, args['target'], args['verified_by'], args['received_utc'], args['evidence'])
        self.assertEqual(len(WR.witness_ledger(self.proj, self.GAME)), 1)
        late = WR.utc_text(self.at(m, hours_before=-2))
        SC.verify(self.GAME, m, 'reviewer', late, receipt)               # received after the deadline: kept, not promoting
        self.assertEqual(status(), ('TIMELINESS_UNVERIFIED', 'witness verified, received after the deadline'))
        # the result arrives and is scored; a verification added after the score changes the status, and no score byte
        self.clear_lock()
        self.grow([m])
        self.now = self.at(m + 1, hours_before=40)
        s2 = self.open()['session_id']
        self.next(s2)
        self.score(s2, m)
        scored = WR.score_ledger_path(self.proj, self.GAME).read_bytes()
        v = SC.verify(self.GAME, m, 'project-owner', early, receipt)
        self.assertEqual((v['digest_binding'], v['kind']), ('human-checked', 'WITNESS_VERIFIED'))
        self.assertEqual(status(), ('PUBLISHED_BEFORE_DRAW', 'witness verified, received before the deadline'))
        self.assertEqual(WR.score_ledger_path(self.proj, self.GAME).read_bytes(), scored)
        self.assertEqual(sorted(s['effective_class'] for s in self.scores()), ['LATE_PRE_DRAW', 'PROSPECTIVE', 'PROSPECTIVE'])
        self.assertEqual(OR.forecast_ledger_path(self.proj, self.GAME).read_bytes().split(b'\n')[0] + b'\n', canonical(line))
        self.assertNotIn('witness', json.dumps(self.scores()) + json.dumps(self.lines()))    # never stored in either
        # a torn last line in the witness ledger is ignored and completed by the next writer
        path = WR.witness_ledger_path(self.proj, self.GAME)
        path.write_bytes(path.read_bytes() + b'{"schema": "WITNESS')
        SC.witness(self.GAME, m, 'email', '<id-1@example.invalid>')
        self.assertEqual(len(WR.witness_ledger(self.proj, self.GAME)), 4)
        self.assertEqual(len(list(path.parent.glob(path.name + '.torn_*'))), 1)


class DiagnosticScore(B.Weekly):
    EXTRA = 1

    def diagnostic_run(self, target, run_id):
        members = [m for m in B._real_cohort(self.GAME, B.adapters())[0] if m['method_id'] == 'E_6']
        session = {'game_id': self.GAME, 'session_id': '0' * 32, 'ledger_version': self.rows[-1]['version'],
                   'master_sha256': self.rows[-1]['master_sha256']}
        req = WR.request_for(session, members[0], target, run_id, 'REAL_DEVELOPMENT')
        req['binding'] = X.DIAGNOSTIC
        res = CR.run_contract_method(req, compute=B.adapters()['E_6'].compute, verify=B.adapters()['E_6'].verify,
                                     repo_root=self.proj, run_root=OR.diagnostic_runs_root(self.proj))
        self.assertEqual(res.outcome, 'SUCCESS', res.reason)
        return res.folder

    def everything(self):
        return sorted((str(f.relative_to(self.proj)), f.read_bytes()) for f in self.proj.rglob('*') if f.is_file())

    def test_diagnostic_score_prints_and_writes_nothing(self):                             # L-G2, L-G3
        prefix = self.p.holdout_first - 2
        folder = self.diagnostic_run(prefix, 'mg-' + '1' * 32)
        after_holdout = self.diagnostic_run(self.first, 'mg-' + '2' * 32)
        before = self.everything()
        out = SC.diagnostic_score(self.GAME, 'mg-' + '1' * 32)
        row = master_row(self.proj, self.GAME, prefix)
        labels = json.loads((folder / 'forecast.json').read_bytes())['barrels']['MAIN']['top']['labels']
        self.assertEqual(out['readouts']['TOP']['main_matches'], len(set(labels) & set(row['main'])))
        self.assertEqual((out['unofficial'], out['target_draw_number']), (True, prefix))
        with self.assertRaisesRegex(SC.ScoreRefused, 'nothing is shown'):
            SC.diagnostic_score(self.GAME, 'mg-' + '2' * 32)             # a draw after the holdout with no freeze line
        with self.assertRaisesRegex(SC.ScoreRefused, 'no diagnostic record'):
            SC.diagnostic_score(self.GAME, 'mg-' + '3' * 32)
        self.assertEqual(self.everything(), before)                      # not one byte, in any ledger or anywhere else
        sid = self.open()['session_id']
        self.next(sid)
        official = self.lines()[0]['records'][0]['run_id']
        with self.assertRaisesRegex(SC.ScoreRefused, 'no diagnostic record'):
            SC.diagnostic_score(self.GAME, official)                     # an official record is not served here
        self.assertEqual(SC.diagnostic_score(self.GAME, 'mg-' + '2' * 32)['target_draw_number'], self.first)   # frozen now
        # the diagnostic record is never official: no freeze line names it and the scorer scores only named records
        self.score(sid, self.first)
        self.assertNotIn('mg-' + '2' * 32, json.dumps(self.lines()) + json.dumps(self.scores()))
        self.assertTrue(after_holdout.is_relative_to(OR.diagnostic_runs_root(self.proj)))
        self.assertEqual(WS.status(self.GAME)['diagnostic_records'], 2)


class CommandLineAndStatics(B.Weekly):
    EXTRA = 1

    def main(self, *args):
        from evaluation import Method_Weekly_Score as M
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = M.main(list(args))
            except SystemExit as exc:
                code = exc.code
        return code, out.getvalue().strip().splitlines(), err.getvalue()

    def test_commands_exit_codes_and_the_machine_readable_last_line(self):
        g, t = self.GAME, str(self.first)
        sid = self.open()['session_id']
        code, out, err = self.main('score', '--game', g, '--session', sid, '--target', t)
        self.assertEqual((code, out[-1]), (2, f'[WEEKLY-SCORE] RESULT state=REFUSED target={t} session={sid}'), err)
        self.assertIn('Nothing was written', err)
        self.next(sid)
        code, out, _err = self.main('score', '--game', g, '--session', sid, '--target', t)
        self.assertEqual((code, out[-1]), (0, f'[WEEKLY-SCORE] RESULT state=SCORED target={t} session={sid}'))
        code, out, _err = self.main('witness', '--game', g, '--target', t, '--kind', 'email', '--ref', '<m1@example.invalid>')
        self.assertEqual((code, out[-1].split()[2]), (0, 'state=WITNESS_RECORDED'))
        code, out, _err = self.main('verify', '--game', g, '--target', t, '--verified-by', 'project-owner',
                                    '--received-utc', '2026-10-01T00:00:00Z', '--evidence', 'Received: <m1@example.invalid>')
        self.assertEqual((code, out[-1].split()[2]), (0, 'state=WITNESS_VERIFIED'))
        code, out, _err = self.main('diagnostic-score', '--game', g, '--run', 'mg-' + '7' * 32)
        self.assertEqual(code, 2)
        with mock.patch.object(SC, 'score', side_effect=SC.ScoreStopped('planted')):
            code, out, err = self.main('score', '--game', g, '--session', sid, '--target', t)
        self.assertEqual((code, out[-1].split()[2]), (1, 'state=STOPPED'))
        self.assertEqual(self.main('score', '--game', 'KENO', '--session', sid, '--target', t)[0], 2)

    def test_statics_of_the_scoring_half(self):
        for rel in EVALUATOR_SIDE:
            tree = ast.parse((ROOT / rel).read_text(encoding='ascii'))
            imported = [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names] + \
                       [n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
            names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | \
                    {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
            for bad in ('urllib', 'socket', 'http', 'requests', 'subprocess', 'signal', 'psutil', 'os', 'datetime', 'time'):
                self.assertFalse([m for m in imported if m.split('.')[0] == bad], (rel, bad))
            for bad in ('kill', 'terminate', 'compute', 'run_contract_method', 'open_session', 'next_step', 'unlink'):
                self.assertNotIn(bad, names, (rel, bad))                 # no process control, no method run, no forecast
        text = (ROOT / EVALUATOR_SIDE[0]).read_text(encoding='ascii')
        self.assertEqual(text.count('RD.read_outcome'), 2)               # the score, once; diagnostic-score, once
        self.assertLess(text.index('WR.verify_named_records'), text.index('RD.outcome_release_allowed'))
        self.assertLess(text.index('RD.outcome_release_allowed(root, game_id, target)'), text.index('RD.read_outcome_rows('))


if __name__ == '__main__':
    unittest.main()
