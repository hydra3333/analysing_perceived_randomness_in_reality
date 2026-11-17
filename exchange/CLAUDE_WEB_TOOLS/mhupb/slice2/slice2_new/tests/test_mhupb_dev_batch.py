"""MHUP-B slice 2, layer L6: the window contract and the two kinds of development run (design supplement v0.8 sections
7.1A and 7.2; code plan v0.3 section 5, L6; an always-review subject: holdout access and N-1). OFFLINE: the temporary
weekly project of mhupb_fixtures (the game's Mode H study sealed, the system declared developed); every draw, clock
reading, release instant and source list is invented.

 Equal draws The owner's clarification of 18 November 2026 (EX_234, EX_235): a former holdout draw is an ordinary draw with
             no record of the archived Mode H study as a condition; a bulk catch-up computes what week-by-week operation
             computes; a revised version is a new identity and the old one keeps its history.
 Plans       WF_BATCH_PLAN_V2 beside the first schema, which keeps its rules. A routine fill's pairs are worked out by
             the driver and checked against an ORACLE written from the supplement's rules; an exploratory rerun runs
             what the owner names. Refused windows refuse and write nothing.
 The gate    every refusal of the DEV_BATCH branch once (none of them about the Mode H archive); rule 2A by the release instant; a target still open in the
             weekly session is never a batch's; the mode-to-pin rule.
 Evidence    every forecast is REAL_DEVELOPMENT, tier DEVELOPMENT_WF_EXPLORATORY, N-1 (it trains to the draw before its
             target), under the development roots; no byte of any sealed Mode H path, freeze line or weekly ledger
             changes (snapshots before and after every command).
 Reports     a V2 batch reported on its own pairs, holdout outcomes released only after the seal, no registered family
             (EXPLORATORY_COHORT), with the comparison section; the first plan kind's report keeps its cap.
"""
from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path
from unittest import mock

import mhupb_fixtures as B
import _common.contract_dispatch as CD
import _common.contract_publication as CP
import _common.release_records as RR
import _common.score_identities as SI
import _common.walk_forward as WF
import _common.weekly_records as WR
import _common.weekly_session as WS
from _common import owner_records as OR
from _common.contract_records import canonical, record_digest, sha256_hex, validate_run_request
from evaluation import outcome_reader as RD
from evaluation import reforecast_compare as RC
from evaluation import report as RP
from evaluation import report_writer as RW


class Dev(B.Weekly):
    EXTRA = 2                                     # two accepted draws after the holdout
    UNCOVERED = 2                                 # prefix targets that no canonical source covers

    def setUp(self):
        super().setUp()
        self.keep = 1                             # one variant of E_6 unless a test widens the cohort
        self.instants = {}                        # (method, variant) -> release instant, overriding RELEASED_UTC
        self.stack.enter_context(mock.patch.object(RR, 'release_instants', self._instants))
        self.sources = []

    RELEASED_UTC = '2026-01-01T00:00:00.000000Z'

    def _cohort(self, game_id, adapters_):
        members, excluded = super()._cohort(game_id, adapters_)
        first = [m for m in members if m['method_id'] == 'E_6'][:self.keep]
        return first + [m for m in members if m['method_id'] != 'E_6'], excluded

    def _released(self, root):
        return {(self.GAME, m['method_id'], m['method_revision'], m['variant_id']):
                self.release_dates.get((m['method_id'], m['variant_id']), self.RELEASED)
                for m in self._cohort(self.GAME, B.adapters())[0]}

    def _instants(self, root):
        return {k: self.instants.get((k[1], k[3]), self.RELEASED_UTC) for k in self._released(root)}

    # ------------------------------------------------------------ helpers
    def members(self):
        return WF.cohort(self.GAME, B.adapters())[0]

    def cover_the_prefix(self):
        """A plan of the first kind over all but the last UNCOVERED prefix targets, listed as a canonical source the
        way the league's admission step (layer L4) will list it."""
        last = self.p.holdout_first - 1 - self.UNCOVERED
        plan = WF.make_plan(self.GAME, self.p.first_draw + 1, last, B.adapters())
        self.list_source(plan, 'WF_BATCH_PLAN_V1')
        return plan

    def list_source(self, plan, kind, **change):
        entry = {'attempt_id': 'rr-' + plan['batch_id'][3:], 'batch_id': plan['batch_id'], 'batch_kind': kind,
                 'plan_digest': record_digest(plan), 'window_first': plan['window_first'],
                 'window_last': plan['window_last'], 'score_ledger_sha256': 'a' * 64, 'evaluator_version': 'fixture'}
        entry.update(change)
        self.sources.append(entry)
        self.write_sources()

    def write_sources(self, raw=None):
        path = SI.league_sources_path(self.proj, self.GAME)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw if raw is not None else canonical(
            {'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME, 'sources': self.sources}))

    def fill(self):
        return WF.make_dev_plan(self.GAME, 'ROUTINE_FILL', B.adapters())

    def rerun(self, first, last, variants=None):
        return WF.make_dev_plan(self.GAME, 'EXPLORATORY_RERUN', B.adapters(), variants=variants, first=first, last=last)

    def run_plan(self, plan):
        out = []
        return WF.run_batch(self.GAME, plan['batch_id'], B.adapters(), echo=out.append), out

    def hand_plan(self, kind, pairs):
        """A valid plan of the second kind for pairs the planner itself would not choose (to reach the gate's own
        refusals): written exactly as make_dev_plan writes one, with its search-log row."""
        members = {(m['method_id'], m['method_revision'], m['variant_id']): m for m in self.members()}
        version, pin = WF.ledger_pin(self.GAME)
        batch = 'wf-' + __import__('uuid').uuid4().hex
        used = [members[k] for k in sorted({tuple(x[:3]) for x in pairs})]
        plan = {'schema': WF.DEV_PLAN_SCHEMA, 'plan_kind': kind, 'batch_id': batch, 'game_id': self.GAME,
                'profile_version': self.p.version, 'window_first': min(x[3] for x in pairs),
                'window_last': max(x[3] for x in pairs), 'created_utc': WF.utc_now(), 'driver_version': WF.DRIVER_VERSION,
                'run_mode': 'REAL_DEVELOPMENT', 'product_kind': 'WF_FORECAST', 'observation_view': WF.VIEW,
                'include_dates': False, 'master_file': f'{self.GAME}_results_master.csv', 'ledger_version': version,
                'master_sha256': pin, 'cohort': used,
                'not_in_cohort': [], 'cohort_digest': sha256_hex(canonical({'cohort': used})), 'pairs': pairs,
                'pairs_digest': sha256_hex(canonical({'pairs': pairs}))}
        folder = WF.roots('DEV_BATCH')['batches'] / self.GAME / batch
        folder.mkdir(parents=True)
        (folder / 'plan.json').write_bytes(canonical(plan))
        WF._append_search_row({'row_type': 'DEV_BATCH', 'utc': plan['created_utc'], 'game_id': self.GAME, 'mode': 'WF',
                               'batch_id': batch, 'plan_digest': record_digest(plan)})
        return plan

    def one_run(self, plan, pair):
        """Issue one pair of a plan through the driver's own loop: None if the run ended in a CONTINUE class, else the
        stop text (which names the gate's or the runner's refusal)."""
        mem = next(m for m in plan['cohort'] if (m['method_id'], m['method_revision'], m['variant_id']) == tuple(pair[:3]))
        return WF._loop(plan, [(mem, pair[3])], B.adapters(), [])

    def key(self, i=0):
        m = self.members()[i]
        return [m['method_id'], m['method_revision'], m['variant_id']]

    def protected_bytes(self):
        """Every byte a development job must never change: the sealed Mode H paths, the weekly folder and run root, the
        masters. (A session's own REAL_DEVELOPMENT runs live under the development run root, beside a batch's.)"""
        out = {}
        for base in (self.proj / 'results' / 'real' / 'holdout', OR.weekly_root(self.proj, self.GAME),
                     OR.weekly_runs_root(self.proj), self.proj / 'source_data'):
            if base.is_dir():
                for f in sorted(base.rglob('*')):
                    if f.is_file():
                        out[str(f.relative_to(self.proj))] = f.read_bytes()
        return out

    def forecasts_of(self, plan):
        out = {}
        runs = WF.roots('DEV_BATCH')['runs'] / self.GAME
        tickets = OR.tickets(OR.dev_batch_folder(self.proj, self.GAME, plan['batch_id']) / 'attempts.jsonl',
                             scope_kind='DEV_BATCH', scope_id=plan['batch_id'], game_id=self.GAME)
        for t in tickets:
            if t['kind'] != 'DONE':
                continue
            folder = runs / t['method_id'] / t['variant_id'] / t['run_id']
            f = folder / CP.FILES['forecast']
            if f.is_file():
                out[(t['method_id'], t['variant_id'], t['target_draw_number'])] = (
                    json.loads(f.read_bytes()), json.loads((folder / CP.FILES['forecast_receipt']).read_bytes()))
        return out

    def oracle_fill_pairs(self, covered_to):
        """The routine fill's pairs from the supplement's rules (7.1A, 7.2), written without the planner's code: for
        each released variant, every prefix target above `covered_to`, every holdout target (the study is sealed),
        and every accepted later target whose freeze line was frozen before the variant's release instant and does
        not name it."""
        pairs = []
        lines = {l['target_draw_number']: l for l in self.lines()}
        for m in self.members():
            k = [m['method_id'], m['method_revision'], m['variant_id']]
            pairs += [[*k, t] for t in range(covered_to + 1, self.p.holdout_last + 1)]
            inst = self.instants.get((m['method_id'], m['variant_id']), self.RELEASED_UTC)
            for t, line in sorted(lines.items()):
                named = any((r['method_id'], r['variant_id']) == (m['method_id'], m['variant_id']) for r in line['records'])
                if t <= self.last_draw and line['frozen_utc'] < inst and not named:
                    pairs.append([*k, t])
        return pairs


class Plans(Dev):
    def test_a_routine_fill_plans_exactly_the_uncovered_pairs_and_runs_them(self):
        v1 = self.cover_the_prefix()
        before = self.protected_bytes()
        plan = self.fill()
        self.assertEqual(plan['pairs'], self.oracle_fill_pairs(v1['window_last']))
        self.assertEqual(len(plan['pairs']), self.UNCOVERED + 10)
        self.assertEqual((plan['schema'], plan['plan_kind'], plan['run_mode']), ('WF_BATCH_PLAN_V2', 'ROUTINE_FILL', 'REAL_DEVELOPMENT'))
        rows = [r for r in RP.search_rows(self.GAME) if r['row_type'] == 'DEV_BATCH']
        self.assertEqual([r['plan_digest'] for r in rows], [record_digest(plan)])
        self.assertEqual(WF.load_plan(self.GAME, plan['batch_id']), plan)
        self.assertEqual(WF.kind_of(plan), 'DEV_BATCH')
        code, out = self.run_plan(plan)
        self.assertEqual(code, 0, out)
        made = self.forecasts_of(plan)
        self.assertEqual(sorted(made), sorted((p[0], p[2], p[3]) for p in plan['pairs']))
        for (m, v, t), (fc, rc) in made.items():
            self.assertEqual((fc['run_mode'], rc['evidence_tier']), ('REAL_DEVELOPMENT', 'DEVELOPMENT_WF_EXPLORATORY'))
            self.assertEqual(fc['training_last_draw_number'], t - 1)          # N-1: trained to the draw before
            self.assertEqual((rc['ledger_version'], rc['master_sha256']), (plan['ledger_version'], plan['master_sha256']))
        self.assertEqual(self.protected_bytes(), before)                      # no sealed or weekly byte changed
        self.assertEqual(WF.pending(plan), [])
        code, out = self.run_plan(plan)                                            # a rerun of the command runs nothing
        self.assertEqual((code, len(self.forecasts_of(plan))), (0, len(plan['pairs'])))
        st = WF.status(self.GAME, plan['batch_id'])
        self.assertEqual(st[f"{self.key()[0]} {self.key()[2]}"]['pending'], 0)
        # once the attempt is listed as a canonical source there is nothing left to fill
        self.list_source(plan, 'ROUTINE_FILL')
        with self.assertRaises(WF.BatchRefused):
            self.fill()
        self.assertEqual(self.protected_bytes(), before)

    def test_rule_2a_back_history_by_the_release_instant(self):
        """A variant released after two weekly targets were frozen gets them as development back-history; a variant
        the freeze lines name does not; a target frozen at or after the release instant is the weekly session's."""
        v1 = self.cover_the_prefix()
        sid, states = self.session()                                          # freezes first, first + 1 (catch-up), M
        frozen = [WR.parse_utc(l['frozen_utc']) for l in self.lines()]
        self.methods.add('E_7')                                               # released after those freezes
        later = WR.utc_text(max(frozen) + timedelta(hours=1))
        for m in self.members():
            if m['method_id'] == 'E_7':
                self.instants[(m['method_id'], m['variant_id'])] = later
                self.release_dates[(m['method_id'], m['variant_id'])] = later[:10]
        keys = [[m['method_id'], m['method_revision'], m['variant_id']] for m in self.members()]
        e7 = [k for k in keys if k[0] == 'E_7']
        covered = [[*k, t] for k in keys                                      # everything up to the holdout's end is covered:
                   for t in range((self.p.first_draw if k[0] == 'E_7' else v1['window_last']) + 1,
                                  self.p.holdout_last + 1)]                   # E_7 is new, so from its first target
        self.list_source(self.hand_plan('ROUTINE_FILL', covered), 'ROUTINE_FILL')
        before = self.protected_bytes()
        for k in e7:                                                          # were E_7 released BEFORE those freezes (and
            self.instants[(k[0], k[2])] = WR.utc_text(min(frozen) - timedelta(days=1))    # merely missed by the session),
        with self.assertRaises(WF.BatchRefused):                              # the targets would not be a fill's (rule 2A)
            self.fill()
        for k in keys:                                                        # every variant's release instant is now after
            self.instants[(k[0], k[2])] = later                               # the freezes: E_6 is still excluded, because
        plan = self.fill()                                                    # the freeze lines name it
        self.assertEqual(plan['pairs'], [[*k, t] for k in e7 for t in (self.first, self.first + 1)])
        self.assertEqual(plan['pairs'], self.oracle_fill_pairs(self.p.holdout_last))
        code, out = self.run_plan(plan)
        self.assertEqual(code, 0, out)
        for (m, v, t), (fc, rc) in self.forecasts_of(plan).items():
            self.assertEqual((fc['run_mode'], rc['evidence_tier'], fc['training_last_draw_number']),
                             ('REAL_DEVELOPMENT', 'DEVELOPMENT_WF_EXPLORATORY', t - 1))
        self.assertEqual(self.protected_bytes(), before)
        # the same-day cases at the gate: frozen before the release instant is admitted (above); at or after: refused
        again = self.hand_plan('ROUTINE_FILL', [[*e7[0], self.first]])
        for instant, refusal in ((WR.utc_text(frozen[0]), 'FROZEN_AFTER_RELEASE'),
                                 (WR.utc_text(frozen[0] - timedelta(seconds=1)), 'FROZEN_AFTER_RELEASE')):
            self.instants[(e7[0][0], e7[0][2])] = instant
            self.assertIn(refusal, self.one_run(again, [*e7[0], self.first]))
        self.instants[(e7[0][0], e7[0][2])] = WR.utc_text(frozen[0] + timedelta(milliseconds=1))   # frozen just before it
        with mock.patch.object(OR, 'session_ticket_for_pair', return_value=True):
            self.assertIn('PAIR_HAS_WEEKLY_TICKET', self.one_run(again, [*e7[0], self.first]))
        named = self.hand_plan('ROUTINE_FILL', [[*self.key(0), self.first]])  # E_6: the freeze line names it
        self.instants[(self.key(0)[0], self.key(0)[2])] = later              # (even were its release instant later)
        self.assertIn('PAIR_HAS_WEEKLY_RECORD', self.one_run(named, [*self.key(0), self.first]))
        self.assertIsNone(self.one_run(again, [*e7[0], self.first]))          # and admitted when all of rule 2A holds
        self.assertEqual(self.protected_bytes(), before)

    def test_an_exploratory_rerun_and_its_refused_windows(self):
        self.cover_the_prefix()
        self.session()                                                        # weekly lines for first, first + 1 and M
        m = self.last_draw + 1
        before = self.protected_bytes()
        k = self.key()
        plan = self.rerun(self.p.holdout_last, self.first + 1, variants=[(k[0], k[2])])
        self.assertEqual(plan['pairs'], [[*k, t] for t in (self.p.holdout_last, self.first, self.first + 1)])
        self.assertEqual(plan['plan_kind'], 'EXPLORATORY_RERUN')
        code, out = self.run_plan(plan)
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.forecasts_of(plan)), 3)                     # whether or not scored before
        self.assertEqual(self.protected_bytes(), before)
        for kw, why in (({'first': self.first, 'last': m}, 'the next draw is not accepted'),
                        ({'first': self.p.first_draw, 'last': self.p.first_draw + 3}, 'the first draw has no history'),
                        ({'first': 5, 'last': 4}, 'not a window'), ({'first': None, 'last': 10}, 'no window'),
                        ({'first': self.first, 'last': self.first, 'variants': [('E_99', 'X')]}, 'not a released variant'),
                        ({'first': self.first, 'last': self.first, 'variants': []}, 'no variant'),
                        ({'first': self.first, 'last': self.first, 'variants': [(k[0], k[2]), (k[0], k[2])]}, 'named twice')):
            with self.subTest(why=why), self.assertRaises(WF.BatchRefused):
                self.rerun(kw['first'], kw['last'], variants=kw.get('variants'))
        with self.assertRaises(WF.BatchRefused):
            WF.make_dev_plan(self.GAME, 'ROUTINE_FILL', B.adapters(), first=1, last=2)
        with self.assertRaises(WF.BatchRefused):
            WF.make_dev_plan(self.GAME, 'SOMETHING', B.adapters())
        self.assertEqual(len([r for r in RP.search_rows(self.GAME) if r['row_type'] == 'DEV_BATCH']), 1)   # refusals log nothing
        # the two kinds give the same forecast content for the same pair, pin and revision
        fill = self.hand_plan('ROUTINE_FILL', [[*k, self.p.holdout_last]])
        self.assertIsNone(self.one_run(fill, [*k, self.p.holdout_last]))
        a = self.forecasts_of(plan)[(k[0], k[2], self.p.holdout_last)]
        b = self.forecasts_of(fill)[(k[0], k[2], self.p.holdout_last)]
        self.assertEqual(a[0]['canonical_content_digest'], b[0]['canonical_content_digest'])
        res = RC.compare({'forecast': a[0], 'receipt': a[1]}, {'forecast': b[0], 'receipt': b[1]})
        self.assertEqual((res['equal'], res['preconditions_hold'], res['differences']), (True, True, []))
        # the same through the batches' own records (one attempt against another), with a key only one batch holds
        from evaluation import collect as COL
        lo, hi = self.p.holdout_last, self.first + 1
        rows = RC.compare_plans(plan, COL.collect(plan, lo, hi), fill, COL.collect(fill, lo, hi),
                                [(k[0], k[2], self.p.holdout_last), (k[0], k[2], self.first)])
        self.assertEqual([r['status'] for r in rows], ['IDENTICAL_CONTENT', 'NOT_COMPARED'])
        self.assertTrue(rows[0]['preconditions_hold'])
        self.assertNotEqual(rows[0]['first']['run_id'], rows[0]['second']['run_id'])
        self.assertIn('second: no record in that batch', rows[1]['why'])
        text = '\n'.join(RC.section_lines({'against': 'another attempt', 'mode_h_batch_id': fill['batch_id'], 'pairs': rows,
                                           'counts': {'IDENTICAL_CONTENT': 1, 'NOT_COMPARED': 1}, 'not_checked': RC.NOT_CHECKED}))
        self.assertIn('IDENTICAL_CONTENT', text)
        self.assertIn('preconditions all hold', text)
        self.assertEqual(self.protected_bytes(), before)
        # an accepted draw that the weekly session has not frozen yet is the session's, never a rerun's
        self.grow([m], [m + 1])
        with self.assertRaises(WF.BatchRefused):
            self.rerun(self.first, m + 1)
        self.assertEqual(self.rerun(self.first, m)['window_last'], m)         # M is accepted and frozen: admitted

    def test_the_command_line(self):
        import contextlib
        import io
        import Method_Walk_Forward as M
        self.cover_the_prefix()
        k = self.key()

        def main(*argv):
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    code = M.main(list(argv))
                except SystemExit as exc:                                     # argparse's own refusal
                    code = exc.code
            return code, out.getvalue() + err.getvalue()
        code, text = main('plan', '--rerun', '--game', self.GAME, '--first', str(self.p.holdout_first), '--last',
                          str(self.p.holdout_first + 1), '--variants', f'{k[0]}:{k[2]}')
        self.assertEqual(code, 0, text)
        self.assertIn('EXPLORATORY_RERUN, 2 pairs of 1 variants', text)
        batch = text.split('PLAN ')[1].split(':')[0]
        self.assertEqual(main('run', '--game', self.GAME, '--batch', batch)[0], 0)
        code, text = main('plan', '--fill', '--game', self.GAME)
        self.assertEqual(code, 0, text)
        self.assertIn(f'ROUTINE_FILL, {self.UNCOVERED + 10} pairs', text)
        for argv in (('plan', '--fill', '--rerun', '--game', self.GAME), ('plan', '--game', self.GAME, '--variants', 'E_6:X', '--first', '2', '--last', '3'),
                     ('plan', '--rerun', '--game', self.GAME, '--first', '1200', '--last', '1201', '--variants', 'E_6')):
            self.assertEqual(main(*argv)[0], 2, argv)
        code, text = main('plan', '--fill', '--game', self.GAME, '--first', '1200', '--last', '1201')
        self.assertEqual((code, 'REFUSED' in text), (2, True))

    def strip_mode_h(self):
        """Remove every record of the archived Mode H study from the project: its plan's lifecycle markers (the seal
        among them) and the batch-id record. The opening record stays: the installed reader asks for it at or above
        the former holdout, and that reader is not part of this slice."""
        for name in OR.LIFECYCLE_MARKERS:
            OR.marker_path(self.proj, self.GAME, self.BATCH, name).unlink()
        OR.batch_id_record_path(self.proj, self.GAME).unlink()

    def test_a_former_holdout_draw_is_an_ordinary_draw_with_no_mode_h_record(self):
        """The owner's clarification (EX_234 section 3): with the seal and every other Mode H marker gone, the former
        holdout draws are planned, forecast (N-1), reported and scored like any historical draw."""
        self.cover_the_prefix()
        self.strip_mode_h()
        k = self.key()
        plan = self.fill()
        holdout = list(range(self.p.holdout_first, self.p.holdout_last + 1))
        self.assertEqual([p[3] for p in plan['pairs']][self.UNCOVERED:], holdout)
        self.assertEqual(self.run_plan(plan)[0], 0)
        made = self.forecasts_of(plan)
        for t in holdout:
            fc, rc = made[(k[0], k[2], t)]
            self.assertEqual((fc['run_mode'], rc['evidence_tier'], fc['training_last_draw_number']),
                             ('REAL_DEVELOPMENT', 'DEVELOPMENT_WF_EXPLORATORY', t - 1))
        self.assertTrue(all(RD.development_release_allowed(self.proj, self.GAME, t) for t in holdout))
        res = RP.run_report(self.GAME, plan['batch_id'], plan['window_first'], plan['window_last'])
        scores = [json.loads(x) for x in (res['scores_folder'] / 'score_ledger.jsonl').read_bytes().split(b'\n')[:-1]]
        self.assertEqual(sorted({s['draw_number'] for s in scores}), sorted(p[3] for p in plan['pairs']))
        self.assertIn('unavailable', res['sealed_comparison'])                # the optional archive comparison: not a condition
        rerun = self.rerun(self.p.holdout_first - 1, self.p.holdout_first + 1)    # and an exploratory rerun across the boundary
        self.assertEqual(self.run_plan(rerun)[0], 0)
        self.assertFalse(RD.outcome_release_allowed(self.proj, self.GAME, self.p.holdout_first))   # the Mode H scorer's own rule: unchanged

    def test_a_revised_version_is_a_new_identity_and_the_old_one_keeps_its_history(self):
        """EX_234 section 2. Every key carries the revision. With revision 1 covered up to the end of the prefix, a
        revised version (revision 2) is planned from its first eligible target, and revision 1's covered keys and
        records are untouched. A revision the installed registry does not hold is not runnable: nothing archived is
        ever executed."""
        v1 = self.cover_the_prefix()
        k = self.key()
        old = SI.canonical_coverage(self.proj, self.GAME)
        self.assertEqual({key[1] for key in old}, {'1'})
        current = WF.cohort

        def revised(game_id, adapters_):
            members, excluded = current(game_id, adapters_)
            return [dict(m, method_revision='2') for m in members], excluded
        with mock.patch.object(WF, 'cohort', revised):
            plan = self.fill()
        self.assertEqual(plan['pairs'], [[k[0], '2', k[2], t] for t in range(self.p.first_draw + 1, self.p.holdout_last + 1)])
        self.assertEqual(SI.canonical_coverage(self.proj, self.GAME), old)    # the old version's history is as it was
        self.assertEqual(WF.load_plan(self.GAME, v1['batch_id']), v1)
        self.assertIn('method_revision', SI.IDENTITY_FIELDS)                  # a score's identity names its revision
        self.assertIn('REVISION_MISMATCH', self.one_run(plan, plan['pairs'][0]))   # not installed: not runnable

    def test_the_first_plan_kind_is_untouched(self):
        plan = WF.make_plan(self.GAME, self.p.first_draw + 1, self.p.first_draw + 3, B.adapters())
        self.assertEqual((plan['schema'], WF.kind_of(plan), 'pairs' in plan, 'plan_kind' in plan),
                         ('WF_BATCH_PLAN_V1', 'WF_BATCH', False, False))
        self.assertEqual(len(WF.plan_pairs(plan)), 3 * len(plan['cohort']))
        self.assertNotIn('binding', WF.request_for(plan, plan['cohort'][0], self.p.first_draw + 2, CP.new_run_id()))
        with self.assertRaises(WF.BatchRefused):                              # its cap is where it was
            WF.make_plan(self.GAME, self.p.holdout_first - 1, self.p.holdout_first, B.adapters())
        with self.assertRaises(RP.ReportRefused):
            RP.run_report(self.GAME, plan['batch_id'], self.p.first_draw + 1, self.p.holdout_first)


class Gate(Dev):
    def test_every_refusal_of_the_dev_batch_branch(self):
        self.session()
        k = self.key()
        t = self.p.holdout_first
        plan = self.hand_plan('EXPLORATORY_RERUN', [[*k, t], [*k, t + 1]])
        folder = OR.dev_batch_folder(self.proj, self.GAME, plan['batch_id'])
        good_plan = (folder / 'plan.json').read_bytes()
        log = WF.roots()['search_log']
        good_log = log.read_bytes()

        def refused(code, pair=None, target_plan=None):
            got = self.one_run(target_plan or plan, pair or [*k, t])
            self.assertIsNotNone(got)
            self.assertIn(code, got)
        # the plan's own identity
        log.write_bytes(b''.join(x + b'\n' for x in good_log.split(b'\n')[:-1] if plan['batch_id'].encode() not in x))
        refused('PLAN_NOT_LOGGED')
        log.write_bytes(good_log)
        (folder / 'plan.json').write_bytes(canonical(dict(plan, created_utc='2026-01-01T00:00:00.000000Z')))
        refused('BINDING_NOT_RESOLVED')                                       # the binding names the unaltered plan's digest
        (folder / 'plan.json').write_bytes(good_plan[:-1])
        refused('BINDING_NOT_RESOLVED')
        (folder / 'plan.json').write_bytes(good_plan)
        # the pin, the pair and the tickets (requests built by hand, as a foreign caller would)
        mem = plan['cohort'][0]

        def gate(change=None, *, pair_target=t, ticket=True, binding=None):
            req = WF.request_for(plan, mem, pair_target, CP.new_run_id())
            req.update(change or {})
            if binding is not None:
                req['binding'] = dict(req['binding'], **binding)
            if ticket:
                WF._append_attempt(plan, req)
            try:
                CD.dispatch_gate(req)
            except CD.DispatchRefused as exc:
                return exc.reason
            return None
        self.assertEqual(gate(ticket=False), 'NO_OPEN_TICKET')
        self.assertEqual(gate({'master_sha256': 'f' * 64}), 'PIN_DISAGREES_WITH_PLAN')
        self.assertEqual(gate(pair_target=t + 2), 'PAIR_NOT_IN_PLAN')
        self.assertEqual(gate(binding={'plan_digest': 'f' * 64}), 'BINDING_NOT_RESOLVED')
        self.assertEqual(gate(binding={'batch_id': 'wf-' + 'f' * 32}), 'BINDING_NOT_RESOLVED')
        self.assertIsNone(gate())
        self.assertIsNone(self.one_run(plan, [*k, t]))                        # a real run: DONE
        self.assertEqual(gate(), 'PAIR_ALREADY_DONE')
        self.assertIn('PAIR_ALREADY_DONE', self.one_run(plan, [*k, t]))
        # the binding belongs to REAL_DEVELOPMENT only
        req = WF.request_for(plan, mem, t + 1, CP.new_run_id())
        validate_run_request(req)
        after = WF.request_for(plan, mem, self.first, CP.new_run_id())        # a target after the holdout, for the weekly modes
        validate_run_request(after)
        for base, mode in ((req, 'REAL_HOLDOUT'), (after, 'CATCH_UP'), (after, 'FINAL_NEXT_DRAW')):
            with self.assertRaises(ValueError) as caught:
                validate_run_request(dict(base, run_mode=mode))
            self.assertIn('must be bound to', str(caught.exception))
        with self.assertRaises(ValueError):
            validate_run_request(dict(req, binding=dict(req['binding'], run_id=CP.new_run_id())))
        # a target still open in the weekly session is never a batch's; the next draw is never a development target
        m = self.last_draw + 1
        self.assertIsNotNone(WR.freeze_line_for(self.lines(), m))             # M is frozen (next-draw set), not accepted
        open_plan = self.hand_plan('EXPLORATORY_RERUN', [[*k, m], [*k, m + 1]])
        refused('TARGET_NOT_FROZEN', [*k, m + 1], open_plan)
        refused('MODE_PIN', [*k, m], open_plan)                               # the runner, after the reader
        self.assertEqual(self.forecasts_of(open_plan), {})
        # barriers
        marker = self.proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_bytes(b'{}')
        with self.assertRaises(WF.BatchRefused):
            self.fill()
        self.assertEqual(self.run_plan(plan)[0], 2)
        marker.unlink()

    def test_an_interrupted_batch_resumes_and_no_pair_is_run_twice(self):
        self.cover_the_prefix()
        plan = self.fill()
        real = WF.CR.run_contract_method
        calls = []

        def dies(request, **kw):
            calls.append(request['target_draw_number'])
            if len(calls) == 3:
                raise KeyboardInterrupt
            return real(request, **kw)
        with mock.patch.object(WF.CR, 'run_contract_method', dies):
            code, out = self.run_plan(plan)
        self.assertEqual(code, 1)
        self.assertEqual(len(self.forecasts_of(plan)), 2)
        code, out = self.run_plan(plan)
        self.assertEqual(code, 0, out)
        self.assertTrue(any('FAILED_TO_START' in line for line in out))       # the open ticket closed; the run id not reused
        tickets = OR.tickets(OR.dev_batch_folder(self.proj, self.GAME, plan['batch_id']) / 'attempts.jsonl',
                             scope_kind='DEV_BATCH', scope_id=plan['batch_id'], game_id=self.GAME)
        done = [OR.pair_of(t) for t in tickets if t['kind'] == 'DONE']
        self.assertEqual((len(done), len(set(done))), (len(plan['pairs']), len(plan['pairs'])))
        self.assertEqual(sum(1 for t in tickets if t['kind'] == 'FAILED_TO_START'), 1)


class Sources(Dev):
    def test_canonical_coverage_and_the_source_list(self):
        self.assertEqual(SI.canonical_coverage(self.proj, self.GAME), frozenset())     # never written: nothing listed
        v1 = self.cover_the_prefix()
        cov = SI.canonical_coverage(self.proj, self.GAME)
        k = self.key()
        self.assertEqual(cov, {(*k, t) for t in range(v1['window_first'], v1['window_last'] + 1)})
        self.sources[0]['window_last'] -= 5                                   # an attempt over part of its batch's window
        self.write_sources()
        self.assertEqual(len(SI.canonical_coverage(self.proj, self.GAME)), len(cov) - 5)
        good = SI.league_sources_path(self.proj, self.GAME).read_bytes()
        rerun = self.hand_plan('EXPLORATORY_RERUN', [[*k, self.p.holdout_first]])
        entry = dict(self.sources[0])
        bad = {
            'not canonical bytes': good[:-1],
            'another game': canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': 'OZLOTTO', 'sources': []}),
            'an unknown field': canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME, 'sources': [dict(entry, note='x')]}),
            'an attempt twice': canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME, 'sources': [entry, entry]}),
            'a plan digest that is not the plan\'s': canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME,
                                                                'sources': [dict(entry, plan_digest='f' * 64)]}),
            'a batch that does not exist': canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME,
                                                      'sources': [dict(entry, batch_id='wf-' + 'f' * 32)]}),
            'an exploratory rerun listed as canonical': canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME, 'sources': [
                dict(entry, attempt_id='rr-x', batch_id=rerun['batch_id'], batch_kind='EXPLORATORY_RERUN',
                     plan_digest=record_digest(rerun))]}),
            'a rerun listed under another kind': canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME, 'sources': [
                dict(entry, attempt_id='rr-x', batch_id=rerun['batch_id'], batch_kind='ROUTINE_FILL',
                     plan_digest=record_digest(rerun))]}),
        }
        for name, raw in bad.items():
            with self.subTest(source_list=name):
                self.write_sources(raw)
                with self.assertRaises(OR.RecordRefused):
                    SI.canonical_coverage(self.proj, self.GAME)
                with self.assertRaises(WF.BatchRefused):                      # and the planner refuses with it
                    self.fill()


class Reports(Dev):
    def test_a_v2_batch_is_reported_on_its_own_pairs(self):
        self.cover_the_prefix()
        self.session()
        k = self.key()
        plan = self.fill()                                                    # two prefix targets and the ten holdout targets
        self.assertEqual(self.run_plan(plan)[0], 0)
        before = self.protected_bytes()
        rows = len(RP.search_rows(self.GAME))
        res = RP.run_report(self.GAME, plan['batch_id'], plan['window_first'], plan['window_last'])
        self.assertEqual(res['families'], [])                                 # EXPLORATORY_COHORT throughout
        self.assertEqual(sorted(res['collected']['grids'][(k[0], k[2])]), sorted(p[3] for p in plan['pairs']))
        scores = [json.loads(x) for x in (res['scores_folder'] / 'score_ledger.jsonl').read_bytes().split(b'\n')[:-1]]
        self.assertEqual(sorted({s['draw_number'] for s in scores}), sorted(p[3] for p in plan['pairs']))
        self.assertEqual(res['scoring_plan']['plan_kind'], 'ROUTINE_FILL')
        self.assertEqual(len(RP.search_rows(self.GAME)), rows + 1)
        cmp_ = res['sealed_comparison']
        self.assertIn('the Mode H plan does not load', cmp_['unavailable'])   # the fixture's Mode H plan is a stand-in
        text = RW.build(res, generated_utc='2026-11-18T00:00:00.000000Z', seed_line='N1_NOT_RUN', n1_policies_on_file=0,
                        environment={})['txt'].decode('ascii')
        for want in ('Plan kind: ROUTINE_FILL', 'every table is EXPLORATORY_COHORT', 'Development evidence only',
                     'COMPARISON WITH THE SEALED MODE H FORECASTS', 'Not available: the Mode H plan does not load'):
            self.assertIn(want, text)
        self.assertEqual(self.protected_bytes(), before)                      # the report wrote nothing sealed or weekly
        # a batch with gaps is reported on its own pairs, not on every draw between them
        gaps = self.hand_plan('EXPLORATORY_RERUN', [[*k, self.p.holdout_first], [*k, self.p.holdout_first + 2]])
        self.assertEqual(self.run_plan(gaps)[0], 0)
        res3 = RP.run_report(self.GAME, gaps['batch_id'], self.p.holdout_first, self.p.holdout_first + 2)
        self.assertEqual(res3['collected']['grids'][(k[0], k[2])], [self.p.holdout_first, self.p.holdout_first + 2])
        rows = len(RP.search_rows(self.GAME)) - 1
        # a window outside the batch's own targets refuses, before any row
        with self.assertRaises(RP.ReportRefused):
            RP.run_report(self.GAME, plan['batch_id'], plan['window_first'], plan['window_last'] + 1)
        self.assertEqual(len(RP.search_rows(self.GAME)), rows + 1)
        # a rerun above the holdout is reported once the weekly rule releases its draws
        rerun = self.rerun(self.first, self.first + 1)
        self.assertEqual(self.run_plan(rerun)[0], 0)
        res2 = RP.run_report(self.GAME, rerun['batch_id'], self.first, self.first + 1)
        self.assertEqual((res2['sealed_comparison']['pairs'], res2['scoring_plan']['plan_kind']), ([], 'EXPLORATORY_RERUN'))
        self.assertEqual(self.protected_bytes(), before)
        # a draw after the former holdout that the weekly rule does not release refuses, before any search-log row
        developed = OR.developed_record_path(self.proj, self.GAME)
        raw, rows = developed.read_bytes(), len(RP.search_rows(self.GAME))
        developed.unlink()
        with self.assertRaises(RP.ReportRefused):
            RP.run_report(self.GAME, rerun['batch_id'], self.first, self.first + 1)
        self.assertEqual(len(RP.search_rows(self.GAME)), rows)
        developed.write_bytes(raw)

    def test_the_release_rules_of_the_outcome_reader(self):
        """CF-4, as clarified on 18 November 2026. A development report reads a former holdout draw like any historical
        draw, and a later draw only with its weekly freeze line; the Mode H scorer's own rule is unchanged (after its
        seal it reads nothing again); a prefix draw needs no release."""
        self.session()
        row = self.rows[-1]
        kw = dict(repo_root=self.proj, game_id=self.GAME, master_sha256=row['master_sha256'], ledger_version=row['version'])
        h, m = self.p.holdout_first, self.last_draw + 1
        self.assertEqual([RD.development_release_allowed(self.proj, self.GAME, t)
                          for t in (h - 1, h, self.p.holdout_last, self.first, self.first + 1, m, m + 1)],
                         [False, True, True, True, True, False, False])
        self.assertEqual(sorted(RD.read_outcomes(targets=[h - 1, h, self.first], development=True, **kw)), [h - 1, h, self.first])
        with self.assertRaises(RD.OutcomeRefused):                            # the Mode H scorer's rule: sealed, never again
            RD.read_outcomes(targets=[h], **kw)
        self.assertFalse(RD.outcome_release_allowed(self.proj, self.GAME, h))
        with self.assertRaises(RD.OutcomeRefused):
            RD.read_outcomes(targets=[h, m], development=True, **kw)
        seal = OR.marker_path(self.proj, self.GAME, self.BATCH, 'MODE_H_SEALED')    # the archive's seal is not a condition
        raw = seal.read_bytes()
        seal.unlink()
        self.assertEqual([RD.development_release_allowed(self.proj, self.GAME, t) for t in (h, self.p.holdout_last, self.first)],
                         [True, True, True])
        seal.write_bytes(raw)
        OR.developed_record_path(self.proj, self.GAME).unlink()               # without the developed record: holdout only
        self.assertEqual([RD.development_release_allowed(self.proj, self.GAME, t) for t in (h, self.first)], [True, False])

    def test_families_are_loaded_by_window_and_tier(self):
        """CF-5: the Mode H families are registered for exactly the holdout windows; a development report over that
        window takes none of them."""
        reg = json.loads((RP.REGISTRY_DIR / 'FAMILY_REGISTRY_V1.json').read_bytes())
        for game, lo, hi in (('POWERBALL', 1577, 1586), ('OZLOTTO', 1694, 1703)):
            there = [f for f in reg['families'] if f['game_id'] == game and (f['window_first'], f['window_last']) == (lo, hi)]
            self.assertTrue(there and all(f['evidence_tier'] == 'HOLDOUT_MODE_H' for f in there))
            self.assertEqual(RP.development_families(game, lo, hi), [])
            self.assertEqual(RP.load_families(game, lo, hi), there)           # the Mode H scorer's own call is unchanged
        self.assertEqual(RP.development_families('POWERBALL', 1286, 1576), RP.load_families('POWERBALL', 1286, 1576))
        self.assertTrue(RP.development_families('POWERBALL', 1286, 1576))     # the development families still load

    def test_named_content_comparison(self):
        """Rule 7 on fabricated records: identical named content under different run modes; every kind of difference
        listed; each precondition judged."""
        def fc(mode='REAL_DEVELOPMENT', **change):
            main = {'ranking_kind': 'RANKING_WITH_SCORES', 'ranking_status': 'AVAILABLE', 'ranking': [3, 1, 2],
                    'ranked_groups': [[3], [1], [2]], 'scores': [0.2, 0.1, 0.7], 'score_direction': 'HIGHER_IS_BETTER',
                    'top': {'status': 'PREDICTION_AVAILABLE', 'labels': [3], 'rule_id': 'r'},
                    'worst': {'status': 'PREDICTION_AVAILABLE', 'labels': [2], 'rule_id': 'r'},
                    'tie_identity': {'ranking_tie_readout_version': 'T1'}}
            main.update(change.pop('main', {}))
            out = {'record_status': 'PREDICTION_AVAILABLE', 'run_mode': mode, 'declaration_digest': 'd', 'method_revision': '1',
                   'observation_view': 'UNORDERED_SET', 'include_dates': False, 'permitted_view_digest': 'p',
                   'training_last_draw_number': 9, 'fit_seed_policy_id': None, 'fit_seed_identity': None,
                   'fit_sampling_model_version': 'M', 'barrels': {'MAIN': main}}
            out.update(change)
            return out
        rc = {'registry_entry_digest': 'e', 'environment_identity': {'python_version': '3.13'}}
        same = RC.compare({'forecast': fc(), 'receipt': rc}, {'forecast': fc('REAL_HOLDOUT'), 'receipt': rc})
        self.assertEqual((same['equal'], same['preconditions_hold']), (True, True))
        other = RC.compare({'forecast': fc(), 'receipt': rc},
                           {'forecast': fc('REAL_HOLDOUT', permitted_view_digest='q',
                                           main={'ranking': [1, 3, 2], 'ranked_groups': [[1, 3], [2]], 'scores': [0.2, 0.2, 0.7],
                                                 'top': {'status': 'PREDICTION_AVAILABLE', 'labels': [1]}}),
                            'receipt': dict(rc, environment_identity={'python_version': '3.15'})})
        self.assertFalse(other['equal'])
        self.assertEqual([name for name, ok in other['preconditions'] if not ok],
                         ['the same N-1 history (permitted view and training end)', 'the same environment'])
        text = ' | '.join(other['differences'])
        for want in ('MAIN TOP: [3]', 'MAIN ranking: 2 position(s) differ, the first at position 1', 'MAIN ties', 'MAIN scores: 1 label'):
            self.assertIn(want, text)
        self.assertNotIn('run_mode', json.dumps(RC.named_content(fc())))      # mode-specific fields are left out


class CatchUp(B.Weekly):
    """EX_234 section 1. Several draws accepted in one update are processed one target at a time, each from the prefix
    to N-1: the forecasts and the scores are what week-by-week operation gives. Only the evidence label differs."""
    EXTRA = 0
    DRAWS = 4

    def content(self):
        """(variant, target) -> what was forecast and how it scored, free of run mode, run id and time."""
        forecasts = {}
        for folder in self.run_folders():
            f = folder / CP.FILES['forecast']
            if f.is_file():
                fc = json.loads(f.read_bytes())
                forecasts[(fc['variant_id'], fc['target_draw_number'])] = (
                    RC.named_content(fc), fc['permitted_view_digest'], fc['training_last_draw_number'])
        scores = {(s['variant_id'], s['target_draw_number']): (s['readouts'], s['rank'], s['drawn_main'], s['drawn_powerball'])
                  for s in self.scores()}
        classes = {(s['variant_id'], s['target_draw_number']): s['effective_class'] for s in self.scores()}
        return forecasts, scores, classes

    def test_a_bulk_catch_up_computes_what_week_by_week_operation_computes(self):
        targets = list(range(self.first, self.first + self.DRAWS))
        for name in OR.LIFECYCLE_MARKERS:                                     # and no Mode H marker is needed for any of it
            OR.marker_path(self.proj, self.GAME, self.BATCH, name).unlink()
        for t in targets:                                                     # week by week: forecast t, then its result
            self.now = self.at(t, hours_before=30)
            self.assertEqual(self.session()[1][-1], ('FROZE_NEXT', t))
            self.grow([t])
        self.now = self.at(targets[-1] + 1, hours_before=30)
        self.session()
        weekly = self.content()
        self.tearDown()
        self.setUp()
        for name in OR.LIFECYCLE_MARKERS:
            OR.marker_path(self.proj, self.GAME, self.BATCH, name).unlink()
        self.grow(targets)                                                    # four weeks missed: one update, one session
        self.now = self.at(targets[-1] + 1, hours_before=30)
        self.assertEqual(self.session()[1], [('FROZE', t) for t in targets] + [('FROZE_NEXT', targets[-1] + 1)])
        bulk = self.content()
        keys = sorted(k for k in weekly[1] if k[1] in targets)
        self.assertEqual(len(keys), 3 * self.DRAWS)
        for key in keys:
            self.assertEqual(bulk[0][key], weekly[0][key], key)               # the same ranking, scores, ties, TOP and WORST,
            self.assertEqual(bulk[0][key][2], key[1] - 1)                     # from the same view, which ends at N-1
            self.assertEqual(bulk[1][key], weekly[1][key], key)               # and the same score against the same draw
        self.assertEqual(({weekly[2][k] for k in keys}, {bulk[2][k] for k in keys}), ({'PROSPECTIVE'}, {'CATCH_UP'}))


class Statics(Dev):
    def test_the_comparison_and_the_coverage_reader_open_nothing_for_writing(self):
        import ast
        src = Path(RC.__file__).resolve().parent
        for path, banned in ((src / 'reforecast_compare.py', {'write_bytes', 'write_text', 'open', 'unlink', 'mkdir',
                                                              'create_only', 'append', 'read_outcomes', 'outcome_reader'}),):
            tree = ast.parse(path.read_text(encoding='ascii'))
            names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | \
                    {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
            self.assertEqual(names & (banned - {'append'}), set(), path.name)
        tree = ast.parse((src.parent / 'methods' / '_common' / 'score_identities.py').read_text(encoding='ascii'))
        for fn in ('canonical_coverage', 'league_sources'):                   # identities only: no score, outcome or forecast
            body = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == fn)
            names = {n.id for n in ast.walk(body) if isinstance(n, ast.Name)} | \
                    {n.attr for n in ast.walk(body) if isinstance(n, ast.Attribute)}
            self.assertEqual(names & {'score_ledger', 'read_outcomes', 'read_outcome_rows', 'forecast_ledger', 'open',
                                      'write_bytes', 'write_text', 'scored_identities', 'run_evidence'}, set(), fn)


if __name__ == '__main__':
    import unittest
    unittest.main()
