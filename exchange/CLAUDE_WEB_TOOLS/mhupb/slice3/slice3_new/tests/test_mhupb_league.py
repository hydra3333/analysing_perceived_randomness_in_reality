"""MHUP-B slice 3, layer L4: the league table (design supplement v0.8 sections 3 to 5; code plan v0.3 L4 and sections
7 to 9). OFFLINE: the temporary weekly project of mhupb_fixtures; every draw, clock reading, release date and source
list is invented. The development score ledgers the adapters read are made by the installed report tool
(report.run_report), never written by hand (plan section 8); the committed real ledgers are read in
test_mhupb_league_real.py, kept apart.

 Figures      every column of the table against an ORACLE written here from the score lines alone (no league code).
 Sources      one score per key across sources (refuses, naming the key); a listed source that is gone or altered is
              "not available" for its variants and is never a partial total; Mode H as sealed is shown, never summed.
 Publication  the five steps; a fault after every durable step, then a rerun: a row only for a complete set, the
              same publication finished with the same bytes, or marked incomplete; no version reused; unchanged
              inputs publish nothing; the `current` copies recover; torn or doubled search-log rows refuse.
 Admission    complete attempts only; a repeat changes no byte; a changed identity, an overlapping key and an
              exploratory rerun refuse with the file byte-identical; the replace is atomic.
 Views        the history recomputes nothing; every reconstruction row carries its label.
 Seams        OV-1's reconcile reads the publication manifests; the adapters and the formatter write nothing.
"""
from __future__ import annotations

import ast
import contextlib
import csv
import io
import json
from datetime import timedelta
from fractions import Fraction
from pathlib import Path
from unittest import mock

import mhupb_fixtures as B
import test_mhupb_dev_batch as D
import _common.contract_publication as CP
import _common.release_records as RR
import _common.score_identities as SI
import _common.walk_forward as WF
import _common.weekly_records as WR
from _common import owner_records as OR
from _common.contract_records import canonical, record_digest, sha256_hex
from evaluation import Method_League_Table as TOOL
from evaluation import league_publish as LP
from evaluation import league_sources as LS
from evaluation import league_table as LT
from evaluation import ov1 as OV
from evaluation import report as RP
from evaluation import report_writer as RW

STEPS = ('_create', '_row', '_move', '_remove', '_replace_file')


@contextlib.contextmanager
def league_fault(k: int):
    """Raise Boom after the k-th durable step of the league writer (0: only count). Yields the list of steps taken."""
    steps = []

    def wrap(name, real):
        def step(*args):
            out = real(*args)
            steps.append(name)
            if k and len(steps) == k:
                raise B.Boom(f'injected fault after league step {k} ({name})')
            return out
        return step
    with contextlib.ExitStack() as stack:
        for name in STEPS:
            stack.enter_context(mock.patch.object(LP, name, wrap(name, getattr(LP, name))))
        yield steps


class League(D.Dev):
    """A weekly project with one variant, a helper for writer-made development attempts, and the archive's oracles."""

    def setUp(self):
        super().setUp()
        self.retired = {}                                   # (method, revision, variant) -> release date
        self.stack.enter_context(mock.patch.object(RR, 'released_history', self._history))

    def _history(self, root):
        out = dict(self._released(root))
        out.update({(self.GAME, *k): d for k, d in self.retired.items()})
        return out

    # ------------------------------------------------------------ development attempts, as the installed tools make them
    def v1_batch(self, back=3):
        """A batch of the first kind over the last `back` prefix targets, run to the end."""
        last = self.p.holdout_first - 1
        plan = WF.make_plan(self.GAME, last - back + 1, last, B.adapters())
        self.assertEqual(self.run_plan(plan)[0], 0)
        return plan

    def report(self, plan, first=None, last=None):
        first, last = first or plan['window_first'], last or plan['window_last']
        res = RP.run_report(self.GAME, plan['batch_id'], first, last)
        now = CP.utc_now()
        contents = RW.build(res, generated_utc=now, seed_line='N1_NOT_RUN: fixture', n1_policies_on_file=0, environment={})
        RW.write(res, contents, now[:19].replace('-', '').replace(':', '') + 'Z')
        return res['attempt_id']

    def dev_records(self, plan, attempt):
        raw = (LS.scores_folder(self.GAME, plan['batch_id'], attempt) / 'score_ledger.jsonl').read_bytes()
        return [json.loads(x) for x in raw.decode('ascii').splitlines()]

    # ------------------------------------------------------------ reading what was published
    def archive(self):
        folder = LS.archive_dir(self.proj, self.GAME)
        return {f.name: f.read_bytes() for f in sorted(folder.iterdir())} if folder.is_dir() else {}

    def table_rows(self):
        return [r for r in RP.search_rows(self.GAME) if r['row_type'] == 'WEEKLY_TABLE']

    def current(self):
        folder = LS.current_dir(self.proj, self.GAME)
        return {f.name: f.read_bytes() for f in sorted(folder.iterdir())} if folder.is_dir() else {}

    def csv_of(self, name):
        raw = self.archive()[f'{name}.csv']
        return list(csv.DictReader(io.StringIO(raw.decode('ascii'))))

    def check_archive(self, *, settled: bool):
        """The archive's invariants, written from the supplement (5.1), not from the writer: a row only for a complete
        set; one row per publication; versions never reused; and, once settled, every manifest logged or marked, and
        `current` exactly the newest logged set with no notice."""
        files = self.archive()
        manifests = {n[:-len('.manifest.json')]: json.loads(raw) for n, raw in files.items() if n.endswith('.manifest.json')}
        rows = [r['attempt_id'] for r in self.table_rows()]
        self.assertEqual(len(rows), len(set(rows)), 'two rows name one publication')
        for name in rows:
            m = manifests[name]
            self.assertEqual(record_digest(m), next(r['plan_digest'] for r in self.table_rows() if r['attempt_id'] == name))
            for ext in ('txt', 'csv'):
                self.assertEqual(sha256_hex(files[f'{name}.{ext}']), m[f'{ext}_sha256'], 'a logged member is not its digest')
        versions = [m['version'] for m in manifests.values()]
        self.assertEqual(len(versions), len(set(versions)))
        if settled:
            for name in manifests:
                self.assertTrue(name in rows or f'{name}.PUBLICATION_INCOMPLETE.json' in files, name)
            if rows:
                newest = max(rows, key=lambda n: manifests[n]['version'])
                self.assertEqual(self.current(), {f'{newest}.{ext}': files[f'{newest}.{ext}'] for ext in ('txt', 'csv')})
        return manifests, rows

    def change_inputs(self, i):
        """A new roster (an invented release date) makes the next publication differ, without running anything."""
        m = self.members()[0]
        self.release_dates[(m['method_id'], m['variant_id'])] = f'2026-01-{2 + i:02d}'


def oracle(score_lines, dev_records, game):
    """(variant key) -> the table's main figures, counted here from the records alone: weekly routine lines by their
    class, development records by their track. Shares no code with the league modules."""
    out: dict = {}

    def add(key, target, hits, kind):
        e = out.setdefault(key, {'rows': [], 'kinds': {}})
        e['rows'].append((target, hits, kind))
    for s in score_lines:
        if s['scoring_policy_id'] != 'WEEKLY_SCORE_POLICY_V1' or s['readouts'] is None:
            continue
        top = s['readouts']['TOP']
        if 'unavailable' not in top:
            kind = {'PROSPECTIVE': 'forward', 'CATCH_UP': 'catch_up', 'LATE_PRE_DRAW': 'late_pre_draw',
                    'DEVELOPMENT_WF_EXPLORATORY': 'development'}[s['effective_class']]
            add((s['method_id'], s['method_revision'], s['variant_id']), s['target_draw_number'], top['main_matches'], kind)
    for r in dev_records:
        g, method, variant, readout, mode = r['track_id'].split(':')
        if readout == 'TOP':
            add((method, r['method_revision'], variant), r['draw_number'], r['main_matches'], 'development')
    n_pool = {'POWERBALL': 35, 'OZLOTTO': 47}[game]
    res = {}
    for key, e in out.items():
        rows = sorted(e['rows'])
        n, hits = len(rows), sum(h for _t, h, _k in rows)
        res[key] = {'all_draws': n, 'all_hits': hits, 'all_chance': str(Fraction(49 * n, n_pool)),
                    'forward_draws': sum(1 for r in rows if r[2] == 'forward'),
                    'forward_hits': sum(r[1] for r in rows if r[2] == 'forward'),
                    'last10_hits': sum(r[1] for r in rows[-10:]),
                    'development_draws': sum(1 for r in rows if r[2] == 'development'),
                    'development_hits': sum(r[1] for r in rows if r[2] == 'development'),
                    'catch_up_draws': sum(1 for r in rows if r[2] == 'catch_up'),
                    'catch_up_hits': sum(r[1] for r in rows if r[2] == 'catch_up'),
                    'first_target': rows[0][0], 'last_target': rows[-1][0]}
    return res


class Figures(League):
    EXTRA = 2

    def test_every_figure_equals_the_oracle_and_forward_is_kept_apart(self):
        """Catch-up scores, a forward (PROSPECTIVE) score with a verified witness, and an admitted development attempt:
        each column equals the count made here from the records; the forward column holds PROSPECTIVE only."""
        from evaluation import weekly_score as SC
        self.keep = 2
        sid, states = self.session()
        nxt = states[-1][1]
        self.assertEqual(states[-1][0], 'FROZE_NEXT')
        ref = 'a1b2c3d4e5f6a7b8c9d0a1b2c3d4e5f6a7b8c9d0'
        SC.witness(self.GAME, nxt, 'github', ref)
        SC.verify(self.GAME, nxt, 'project-owner', WR.utc_text(self.now + timedelta(minutes=5)), f'pushed commit {ref}')
        self.grow([nxt])
        self.now = self.at(nxt + 1, hours_before=30)
        self.session()
        plan = self.v1_batch()
        attempt = self.report(plan)
        self.assertEqual(LP.admit(self.GAME, attempt_id=attempt)['state'], 'ADMITTED')
        res = LP.publish(self.GAME)
        self.assertEqual(res['state'], 'PUBLISHED')
        want = oracle(self.scores(), self.dev_records(plan, attempt), self.GAME)
        got = {(r['method'], r['revision'], r['variant']): r for r in self.csv_of(res['name'])}
        self.assertEqual(set(got), set(want))
        for key, w in want.items():
            for col, value in w.items():
                self.assertEqual(got[key][col], str(value), (key, col))
            self.assertEqual(got[key]['forward_draws'], '1')                    # the one draw frozen before its result
            self.assertEqual(got[key]['forward_witness_verified'], '1')
            self.assertEqual(got[key]['labels'], 'LOW_N')
            self.assertEqual(got[key]['rank_provisional'], 'yes')
        line = WR.freeze_line_for(self.lines(), nxt)
        self.assertEqual(WR.publication_status(self.proj, self.GAME, line)[0], 'PUBLISHED_BEFORE_DRAW')
        # the order: hits above chance per draw, exact; ties by identity; ranks 1..n without gaps
        rows = self.csv_of(res['name'])
        rates = [(-Fraction(int(r['all_hits']), int(r['all_draws'])), r['method'], r['revision'], r['variant']) for r in rows]
        self.assertEqual(rates, sorted(rates))
        self.assertEqual([r['rank'] for r in rows], [str(i) for i in range(1, len(rows) + 1)])
        text = self.archive()[f'{res["name"]}.txt'].decode('ascii')
        self.assertIn(LT.ORDER_SENTENCE, text)
        self.assertIn('No P value', text)
        self.assertNotIn('p =', text.lower())
        self.assertIn(attempt, text)                                             # the source is named by identity
        self.assertIn(f'starts at draw {plan["window_first"]}', text)
        self.assertIn('HX-2', text)                                              # draws 1587 and 1588 carry the flag
        self.assertEqual({r['exposure_flagged_draws'] for r in rows}, {'2'})

    def test_no_scores_one_draw_and_retired_rows(self):
        """A released variant with no score is NO_SCORES and unranked; a variant with one scored draw is never ordered
        by its rate; a retired revision is shown as published."""
        self.keep = 1
        self.session()
        self.keep = 2                                        # a second variant released now: no score yet
        self.retired[('E_6', '0', 'OLD_VARIANT_V1')] = '2025-06-01'
        rows = self.csv_of(LP.publish(self.GAME)['name'])
        by = {r['variant']: r for r in rows}
        new = self.members()[1]['variant_id']
        self.assertEqual((by[new]['rank'], by[new]['labels'], by[new]['all_draws']), ('', 'NO_SCORES', '0'))
        self.assertEqual((by['OLD_VARIANT_V1']['status'], by['OLD_VARIANT_V1']['labels']),
                         ('RETIRED', 'NO_SCORES;RETIRED_AS_PUBLISHED'))
        data, _pins = LS.collect(self.proj, self.GAME)
        one = dict(data, rows=[r for r in data['rows'] if r['target'] == self.first])
        e = LT.summarise(one)[0]
        self.assertEqual((e['all_draws'], e['rank']), (1, None))               # one draw: listed, never ranked by a rate

    def test_the_formatter_is_pure(self):
        self.session()
        data, _pins = LS.collect(self.proj, self.GAME)
        ident = {'name': 'league_X', 'version': 1, 'latest_draw': LT.latest_draw(data), 'published_utc': 'T'}
        self.assertEqual(LT.build(data, ident), LT.build(json.loads(json.dumps(data)), ident))
        row = lambda v, t, hits, kind='DEVELOPMENT': {'method': 'M', 'revision': '1', 'variant': v, 'target': t, 'readout': 'TOP',
                                                    'main': hits, 'pb': 0, 'division': 0, 'kind': kind, 'source': 's',
                                                    'witnessed': False, 'drawn_main': []}
        made = dict(data, roster=[], failed=[], not_available=[], mode_h={'rows': [], 'identity': None, 'not_available': 'x'},
                    rows=[row('A', 1, 1), row('A', 2, 1), row('A', 3, 1), row('A', 4, 1),          # 4 hits in 4 draws: 1
                          row('B', 1, 0), row('B', 2, 3),                                         # 3 hits in 2 draws: 3/2
                          row('C', 1, 7),                                                         # one draw: never ranked
                          row('D', 5, 2), row('D', 6, 1),                                         # 3/2 again: tie, by identity
                          *[row('E', t, 1 if t > 2 else 0) for t in range(1, 13)]])               # 12 draws, 10 hits late
        order = [(e['variant'], e['rank']) for e in LT.summarise(made)]
        self.assertEqual(order, [('B', 1), ('D', 2), ('A', 3), ('E', 4), ('C', None)])           # by rate, not by hits
        e = {x['variant']: x for x in LT.summarise(made)}
        self.assertEqual((e['E']['all_hits'], e['E']['last10_hits'], e['E']['missing_targets']), (10, 10, 0))
        self.assertEqual((e['D']['first_target'], e['D']['last_target'], e['A']['all_chance']), (5, 6, 4 * Fraction(49, 35)))
        gap = LT.summarise(dict(made, rows=[row('G', 1, 0), row('G', 4, 0)]))[0]
        self.assertEqual(gap['missing_targets'], 2)                                              # draws 2 and 3
        self.assertEqual(LT.dec(Fraction(1, 8), 2), '0.12')                    # half to even, by whole numbers
        self.assertEqual(LT.dec(Fraction(-3, 8), 2, sign=True), '-0.38')
        self.assertEqual(LT.dec(Fraction(7, 5), 2, sign=True), '+1.40')
        self.assertEqual(LT.chance_per_draw('OZLOTTO'), Fraction(49, 47))


class Sources(League):

    def setUp(self):
        super().setUp()
        self.session()
        self.plan = self.v1_batch()
        self.attempt = self.report(self.plan)

    def test_one_score_per_key_across_sources(self):
        """Two report attempts over the same batch hold the same keys. The second is not admitted, and the source file
        is byte-identical; if both were ever listed, the table refuses and names the key."""
        second = self.report(self.plan)
        with self.assertRaisesRegex(LS.LeagueRefused, 'has 2 complete reports'):         # none listed yet: name one
            LP.admit(self.GAME, batch_id=self.plan['batch_id'], first=self.plan['window_first'], last=self.plan['window_last'])
        LP.admit(self.GAME, attempt_id=self.attempt)
        before = SI.league_sources_path(self.proj, self.GAME).read_bytes()
        with self.assertRaisesRegex(LS.LeagueRefused, 'already supplied by ' + self.attempt):
            LP.admit(self.GAME, attempt_id=second)
        self.assertEqual(SI.league_sources_path(self.proj, self.GAME).read_bytes(), before)
        self.assertEqual(LP.admit(self.GAME, batch_id=self.plan['batch_id'], first=self.plan['window_first'],
                                  last=self.plan['window_last']), {'state': 'ALREADY_ADMITTED', 'attempt_id': self.attempt})
        entry, _rows = LS.attempt_entry(self.proj, self.GAME, second)
        listed = SI.league_sources(self.proj, self.GAME)
        self.write_sources(canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': self.GAME, 'sources': [*listed, entry]}))
        with self.assertRaisesRegex(LS.LeagueRefused, 'one score per draw and readout'):
            LP.publish(self.GAME)
        self.assertEqual(self.archive(), {})                 # nothing of a publication was written

    def test_a_missing_or_altered_source_is_not_available_never_a_partial_total(self):
        LP.admit(self.GAME, attempt_id=self.attempt)
        good = self.csv_of(LP.publish(self.GAME)['name'])[0]
        self.assertGreater(int(good['all_draws']), int(good['catch_up_draws']))
        path = LS.scores_folder(self.GAME, self.plan['batch_id'], self.attempt) / 'score_ledger.jsonl'
        raw = path.read_bytes()
        second = self.report(self.plan)                          # another complete attempt, for the admission below
        shorter = b''.join(raw.splitlines(keepends=True)[:-1])   # still a well-formed ledger: only its digest gives it away
        for damage in (shorter, raw[:-1] + b' \n', None):
            if damage is None:
                path.unlink()
            else:
                path.write_bytes(damage)
            with self.assertRaisesRegex(LS.LeagueRefused, 'nothing can be admitted until it is'):
                LP.admit(self.GAME, attempt_id=second)              # its keys cannot be compared with a source that is gone
            res = LP.publish(self.GAME)
            row = self.csv_of(res['name'])[0]
            self.assertEqual(row['not_available'], self.attempt)
            self.assertEqual((row['all_draws'], row['all_hits'], row['last10_hits'], row['rank']), ('', '', '', ''))
            text = self.archive()[f'{res["name"]}.txt'].decode('ascii')
            self.assertIn(f'not available: {self.attempt}', text)
            self.assertIn('NOT AVAILABLE', text)
            path.write_bytes(raw)
            LP.publish(self.GAME)                            # back: a further publication, with the total again
        self.assertEqual(self.csv_of(self.table_rows()[-1]['attempt_id'])[0]['all_draws'], good['all_draws'])
        with self.assertRaisesRegex(LS.LeagueRefused, 'not the attempt, batch, window'):
            LS.source_rows(self.GAME, dict(SI.league_sources(self.proj, self.GAME)[0], window_last=self.plan['window_last'] - 1))

    def test_mode_h_as_sealed_is_shown_and_never_summed(self):
        """The fixture's SCORE_COMPLETE record names a digest. A ledger that is not those bytes is 'not available'; the
        ledger it names is shown in its own column and changes no total."""
        ident = LS.mode_h_identity(self.proj, self.GAME)
        self.assertEqual(ident['score_ledger_sha256'], self.SCORE_DIGEST)
        raw = (LS.scores_folder(self.GAME, self.plan['batch_id'], self.attempt) / 'score_ledger.jsonl').read_bytes()
        path = OR.mode_h_scores_root(self.proj) / self.GAME / ident['batch_id'] / ident['attempt_id'] / LS.MODE_H_LEDGER
        path.parent.mkdir(parents=True)
        path.write_bytes(raw)                                # writer-made records, but not the bytes the record names
        data, _pins = LS.collect(self.proj, self.GAME)
        self.assertIn('not the bytes its SCORE_COMPLETE record names', data['mode_h']['not_available'])
        self.assertEqual(data['mode_h']['rows'], [])
        before = LT.summarise(data)
        with mock.patch.object(LS, 'mode_h_identity', lambda root, game: dict(ident, score_ledger_sha256=sha256_hex(raw))):
            data2, pins2 = LS.collect(self.proj, self.GAME)
        after = LT.summarise(data2)
        self.assertEqual(pins2['mode_h']['score_ledger_sha256'], sha256_hex(raw))
        self.assertEqual(sum(e['mode_h'][0] for e in after), len([r for r in data2['mode_h']['rows'] if r['readout'] == 'TOP']))
        self.assertGreater(sum(e['mode_h'][0] for e in after), 0)
        for a, b in zip(before, after):                      # shown beside; no total moves
            self.assertEqual({k: v for k, v in a.items() if k != 'mode_h'}, {k: v for k, v in b.items() if k != 'mode_h'})

    def test_late_pre_draw_is_counted_once_and_never_forward_and_a_witness_must_be_verified_in_time(self):
        """Sup 3.5: a LATE_PRE_DRAW record is in the all-draws total, in its own column, never in the forward column.
        Sup 3.2: the witness count takes only a verified witness of that freeze line, received before the draw."""
        rows, lines = self.scores(), self.lines()
        t = rows[0]['target_draw_number']
        line = WR.freeze_line_for(lines, t)
        late = [dict(r, effective_class='LATE_PRE_DRAW') if r['target_draw_number'] == t else r for r in rows]
        with mock.patch.object(WR, 'score_ledger', lambda root, game: late), \
                mock.patch.object(SI, 'scored_identities', lambda *a: frozenset()):
            e = LT.summarise(LS.collect(self.proj, self.GAME)[0])[0]
        self.assertEqual((e['kinds']['LATE_PRE_DRAW'][0], e['forward_draws'], e['all_draws']), (1, 0, self.EXTRA))
        forward = [dict(r, effective_class='PROSPECTIVE') if r['target_draw_number'] == t else r for r in rows]
        base = {'schema': WR.WITNESS_SCHEMA, 'game_id': self.GAME, 'target_draw_number': t, 'witness_kind': 'github',
                'freeze_line_digest': record_digest(line), 'ref': 'abc'}
        before = WR.utc_text(WR.parse_utc(line['deadline_utc']) - timedelta(hours=1))
        after = WR.utc_text(WR.parse_utc(line['deadline_utc']) + timedelta(hours=1))
        cases = (([dict(base, kind='WITNESS_VERIFIED', received_utc=before)], 1),
                 ([dict(base, kind='WITNESS_RECORDED')], 0),                                       # a claim, not verified
                 ([dict(base, kind='WITNESS_VERIFIED', received_utc=after)], 0),                   # received after the draw
                 ([dict(base, kind='WITNESS_VERIFIED', received_utc=before, freeze_line_digest='0' * 64)], 0))
        for witness, want in cases:
            with mock.patch.object(WR, 'score_ledger', lambda root, game: forward), \
                    mock.patch.object(WR, 'witness_ledger', lambda root, game, w=witness: w), \
                    mock.patch.object(SI, 'scored_identities', lambda *a: frozenset()):
                e = LT.summarise(LS.collect(self.proj, self.GAME)[0])[0]
            self.assertEqual((e['forward_draws'], e['forward_witness_verified']), (1, want), witness)

    def test_a_branching_correction_chain_refuses(self):
        rows = self.scores()
        first = rows[0]
        fake = [dict(first, scoring_policy_id='CORRECTION_POLICY_V2', amendment_of=record_digest(first),
                     score_run_id=first['score_run_id'][:-1] + c) for c in '01']
        with mock.patch.object(WR, 'score_ledger', lambda root, game: rows + fake[:1]), \
                mock.patch.object(SI, 'scored_identities', lambda *a: frozenset()):
            data, _pins = LS.collect(self.proj, self.GAME)
            self.assertEqual(data['amendments'], 1)          # one correction: counted, and the routine score is used
            self.assertEqual(len(data['rows']), 2 * len(rows))
        with mock.patch.object(WR, 'score_ledger', lambda root, game: rows + fake), \
                mock.patch.object(SI, 'scored_identities', lambda *a: frozenset()):
            with self.assertRaisesRegex(LS.LeagueRefused, 'the chain branches'):
                LS.collect(self.proj, self.GAME)


class Publication(League):

    def setUp(self):
        super().setUp()
        self.session()

    def test_unchanged_inputs_publish_nothing_and_a_change_takes_the_next_version(self):
        first = LP.publish(self.GAME)
        files, rows = self.archive(), self.table_rows()
        again = LP.publish(self.GAME)
        self.assertEqual((again['state'], again['name']), ('UP_TO_DATE', first['name']))
        self.assertEqual((self.archive(), self.table_rows()), (files, rows))
        self.change_inputs(1)
        second = LP.publish(self.GAME)
        self.assertEqual(second['state'], 'PUBLISHED')
        self.assertIn('_v00002_', second['name'])
        for name, raw in files.items():                       # the archive is the record: nothing in it changed
            self.assertEqual(self.archive()[name], raw)
        self.check_archive(settled=True)
        # both entry points use the one writer: the tool's command gives the same result line and writes nothing new
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(TOOL.main(['publish', '--game', self.GAME]), 0)
        self.assertEqual(out.getvalue().splitlines()[-1], f'[LEAGUE] RESULT state=UP_TO_DATE game={self.GAME} name={second["name"]}')

    def test_a_fault_after_every_durable_step_then_a_rerun(self):
        """Plan section 9: for every k, fault after the k-th durable write of a publication (the manifest, each archive
        member, the row, every step of the current copy), then rerun. A row exists only for a complete set, the
        interrupted publication is finished with the manifest's own bytes and identity, nothing archived changes, no
        version is reused, and the rerun makes no second publication."""
        LP.publish(self.GAME)                                 # so the current folder holds an older set to replace
        self.change_inputs(0)
        with league_fault(0) as counted:
            LP.publish(self.GAME)
        total = len(counted)
        self.assertEqual(counted[:4], ['_create', '_create', '_create', '_row'])
        self.assertEqual(total, 12)                           # 4 + two new copies, the notice, two old removed, two moves, the notice removed
        for k in range(1, total + 1):
            self.change_inputs(k)
            before = self.archive()
            with self.assertRaises(B.Boom), league_fault(k):
                LP.publish(self.GAME)
            manifests, rows = self.check_archive(settled=False)
            for name, raw in before.items():
                self.assertEqual(self.archive()[name], raw)
            pending = [n for n in manifests if n not in rows]
            self.assertEqual(len(pending), 1 if k < 4 else 0, k)
            if 7 <= k < total:
                self.assertIn(LP.NOTICE, self.current(), k)   # a mixed or unfinished copy is never called current
            res = LP.publish(self.GAME)
            self.assertEqual(res['state'], 'UP_TO_DATE', k)   # the interrupted one was finished; no second publication
            manifests2, rows2 = self.check_archive(settled=True)
            self.assertEqual(set(manifests2), set(manifests), k)
            self.assertEqual(len(rows2), len(rows) + len(pending), k)
            self.assertNotIn(LP.NOTICE, self.current())
        self.assertEqual(sorted(m['version'] for m in self.check_archive(settled=True)[0].values()), list(range(1, total + 3)))

    def test_an_interrupted_publication_whose_table_cannot_be_rebuilt_is_marked_never_logged(self):
        LP.publish(self.GAME)
        version = 1
        for k in (1, 2):                                      # only the manifest exists; the manifest and one member
            self.change_inputs(k)
            with self.assertRaises(B.Boom), league_fault(k):
                LP.publish(self.GAME)
            with mock.patch.object(LT, 'ORDER_SENTENCE', 'A different sentence.'):  # the bytes can no longer be rebuilt
                res = LP.publish(self.GAME)
            version += 2
            self.assertEqual(res['state'], 'PUBLISHED')
            self.assertEqual(len(res['repair']['incomplete']), 1, k)
            self.assertIn(f'_v{version:05d}_', res['name'])   # the marked one keeps its version for ever
            files = self.archive()
            marked = res['repair']['incomplete'][0]
            note = json.loads(files[f'{marked}.PUBLICATION_INCOMPLETE.json'])
            self.assertEqual(note['manifest_digest'], sha256_hex(files[f'{marked}.manifest.json']))
            self.assertNotIn(marked, [r['attempt_id'] for r in self.table_rows()])
            self.check_archive(settled=True)
            self.assertEqual(LP.repair(self.GAME)['incomplete'], [])          # marked once; never tried again
            self.assertNotIn(marked, [n['what'].split()[-1] for n in LS.publication_names(self.proj, self.GAME)])
            self.assertEqual(LP.publish(self.GAME)['state'], 'UP_TO_DATE')     # the inputs have not changed since

    def test_an_unfinished_publication_with_a_damaged_member_is_marked(self):
        """The manifest and the text member exist; the member's bytes are then damaged. The table can still be rebuilt,
        but the member in the archive is not it: nothing is overwritten, the publication is marked, never logged."""
        with self.assertRaises(B.Boom), league_fault(2):
            LP.publish(self.GAME)
        name = next(iter(self.check_archive(settled=False)[0]))
        member = LS.archive_dir(self.proj, self.GAME) / f'{name}.txt'
        damaged = member.read_bytes() + b'x'
        member.write_bytes(damaged)
        res = LP.repair(self.GAME)
        self.assertEqual((res['finished'], res['incomplete']), ([], [name]))
        self.assertEqual(member.read_bytes(), damaged)        # never overwritten
        self.assertIn('holds other bytes', self.archive()[f'{name}.PUBLICATION_INCOMPLETE.json'].decode('ascii'))
        self.assertEqual(self.table_rows(), [])
        self.assertIn('_v00002_', LP.publish(self.GAME)['name'])

    def test_the_tools_other_commands(self):
        def run(*args):
            out = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                code = TOOL.main([*args, '--game', self.GAME])
            return code, out.getvalue().splitlines()
        self.assertEqual(run('history')[0], 2)                # nothing published yet: refused, nothing written
        with self.assertRaises(B.Boom), league_fault(1):
            LP.publish(self.GAME)
        code, lines = run('sources-check')
        self.assertEqual((code, lines[-1]), (0, f'[LEAGUE] RESULT state=CHECKED game={self.GAME} name=-'))
        self.assertIn('1 unfinished', lines[0])
        code, lines = run('repair')
        self.assertEqual((code, lines[-1]), (0, f'[LEAGUE] RESULT state=REPAIRED game={self.GAME} name=-'))
        self.assertIn('finished with the same bytes and identity', lines[0])
        self.assertIn('0 unfinished', run('sources-check')[1][0])
        for command, state in (('history', 'WRITTEN'), ('history', 'UNCHANGED'), ('reconstruction', 'WRITTEN')):
            code, lines = run(command)
            self.assertEqual(code, 0, lines)
            self.assertRegex(lines[-1], rf'^\[LEAGUE\] RESULT state={state} game={self.GAME} name=league_{command}_{self.GAME}_\S+$')
        self.assertEqual(len(list(LS.derived_dir(self.proj, self.GAME).iterdir())), 2)
        code, lines = run('admit', '--attempt', 'rr-' + '0' * 32)
        self.assertEqual((code, lines[-1]), (2, f'[LEAGUE] RESULT state=REFUSED game={self.GAME} name=-'))
        with mock.patch.object(LP, 'publish', side_effect=RuntimeError('disk')):
            code, lines = run('publish')
        self.assertEqual((code, lines[-1]), (1, f'[LEAGUE] RESULT state=FAILED game={self.GAME} name=-'))
        for bad in (['admit'], ['admit', '--attempt', 'a', '--batch', 'b'], ['batch-state'], ['admit', '--batch', 'b', '--first', '1']):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                TOOL.main([*bad, '--game', self.GAME])

    def test_a_grown_ledger_does_not_stop_an_interrupted_publication(self):
        """The manifest pins a prefix of every ledger, so a session that runs between the fault and the rerun does not
        change the interrupted publication's bytes: it is finished as pinned, then a new one follows."""
        states = self.session()[1]
        with self.assertRaises(B.Boom), league_fault(1):
            LP.publish(self.GAME)
        name = next(iter(self.check_archive(settled=False)[0]))
        nxt = states[-1][1]
        self.grow([nxt])
        self.now = self.at(nxt + 1, hours_before=30)
        self.session()
        res = LP.publish(self.GAME)
        self.assertEqual((res['repair']['finished'], res['state']), ([name], 'PUBLISHED'))
        rows = self.table_rows()
        self.assertEqual([r['attempt_id'] for r in rows], [name, res['name']])
        self.assertLess(int(rows[0]['window_last']), int(rows[1]['window_last']))
        self.check_archive(settled=True)

    def test_the_current_copies_are_restored_from_the_archive(self):
        res = LP.publish(self.GAME)
        folder = LS.current_dir(self.proj, self.GAME)
        good = self.current()
        (folder / f'{res["name"]}.txt').write_bytes(b'damaged\n')
        (folder / 'stray.txt').write_bytes(b'x')
        (folder / LP.NOTICE).write_bytes(b'left by an interrupted copy\n')
        self.assertTrue(LP.sources_check(self.GAME)['current_notice'])
        self.assertEqual(LP.repair(self.GAME)['current'], 'CURRENT_REFRESHED')
        self.assertEqual(self.current(), good)
        self.assertEqual(LP.repair(self.GAME)['current'], 'CURRENT_OK')
        arch = LS.archive_dir(self.proj, self.GAME) / f'{res["name"]}.csv'
        arch.write_bytes(arch.read_bytes() + b'x')            # a damaged ARCHIVE member is never copied or repaired over
        with self.assertRaisesRegex(LS.LeagueRefused, 'not the bytes its manifest names'):
            LP.sources_check(self.GAME)

    def test_a_torn_or_doubled_search_log_row_refuses(self):
        res = LP.publish(self.GAME)
        log = WF.roots()['search_log']
        raw = log.read_bytes()
        weekly = self.weekly_bytes()
        self.change_inputs(1)
        log.write_bytes(raw + b'WEEKLY_TABLE,2026')           # an unfinished row
        with self.assertRaisesRegex(LS.LeagueRefused, 'unfinished row'):
            LP.publish(self.GAME)
        log.write_bytes(raw + raw.splitlines(keepends=True)[-1])
        with self.assertRaisesRegex(LS.LeagueRefused, 'two search-log rows name the publication ' + res['name']):
            LP.publish(self.GAME)
        self.assertEqual(self.weekly_bytes(), weekly)         # the live records are untouched by any of it
        self.assertEqual(len([n for n in self.archive() if n.endswith('.manifest.json')]), 1)
        log.write_bytes(raw)
        (LS.archive_dir(self.proj, self.GAME) / f'{res["name"]}.manifest.json').rename(self.td / 'gone.json')
        with self.assertRaisesRegex(LS.LeagueRefused, 'whose manifest is not in the archive'):
            LP.publish(self.GAME)

    def test_the_orphan_marker_blocks_every_writing_command(self):
        import _common.contract_runner as CR
        marker = Path(CR.ORPHAN_MARKER)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_bytes(b'{}')
        for call in (lambda: LP.publish(self.GAME), lambda: LP.repair(self.GAME), lambda: LP.history(self.GAME),
                     lambda: LP.reconstruction(self.GAME), lambda: LP.admit(self.GAME, attempt_id='rr-x')):
            with self.assertRaisesRegex(LS.LeagueRefused, 'UNRESOLVED_ORPHAN_MARKER'):
                call()
        self.assertEqual(self.archive(), {})

    def test_history_recomputes_nothing_and_every_reconstruction_row_is_labelled(self):
        first = LP.publish(self.GAME)
        self.change_inputs(1)
        second = LP.publish(self.GAME)
        with mock.patch.object(LS, 'collect', side_effect=AssertionError('the history must not read a source')), \
                mock.patch.object(LT, 'build', side_effect=AssertionError('the history must not rebuild a table')):
            res = LP.history(self.GAME)
            self.assertEqual(LP.history(self.GAME)['state'], 'UNCHANGED')
        text = res['path'].read_bytes()
        a, b = self.archive()[f'{second["name"]}.txt'], self.archive()[f'{first["name"]}.txt']
        self.assertLess(text.index(a), text.index(b))         # newest first, byte for byte
        self.keep = 2                                         # a variant released today: no back-history yet
        m = self.members()[0]
        self.release_dates[(m['method_id'], m['variant_id'])] = str(self.p.derived_date(self.first + 1))
        rec = LP.reconstruction(self.GAME)['path'].read_bytes().decode('ascii').splitlines()
        label = LT.RECONSTRUCTION_LABEL.format(date=CP.utc_now()[:10])
        self.assertEqual(rec[0], label)
        rows = list(csv.DictReader(io.StringIO('\n'.join(rec[1:]))))
        self.assertEqual(len(rows), self.EXTRA)
        self.assertTrue(all(r['label'] == label for r in rows))
        self.assertEqual([r['released_at_this_draw_date'] for r in rows], ['no', 'yes'])
        self.assertEqual([r['running_draws'] for r in rows], ['1', '2'])
        self.assertEqual(rows[1]['running_hits'], str(sum(int(r['matches']) for r in rows)))
        self.assertEqual([r['rank_after_this_draw'] for r in rows], ['', '1'])


class Admission(League):

    def setUp(self):
        super().setUp()
        self.plan = self.v1_batch()

    def test_only_a_complete_correctly_labelled_attempt_is_admitted(self):
        """A plan is not a score: no report, a report without its files, a report whose files or ledger changed, and a
        scoring plan that is not the logged one each refuse and leave no source file."""
        path = SI.league_sources_path(self.proj, self.GAME)
        window = dict(first=self.plan['window_first'], last=self.plan['window_last'])
        with self.assertRaisesRegex(LS.LeagueRefused, 'has no complete report'):
            LP.admit(self.GAME, batch_id=self.plan['batch_id'], **window)
        res = RP.run_report(self.GAME, self.plan['batch_id'], window['first'], window['last'])       # scores, no report files
        with self.assertRaisesRegex(LS.LeagueRefused, 'its report did not complete'):
            LP.admit(self.GAME, attempt_id=res['attempt_id'])
        attempt = self.report(self.plan)
        folder = LS.scores_folder(self.GAME, self.plan['batch_id'], attempt)
        raw = (folder / 'score_ledger.jsonl').read_bytes()
        lines = raw.splitlines(keepends=True)
        one = json.loads(lines[0])
        more = canonical(dict(one, main_matches=(one['main_matches'] + 1) % 8, division=one['division']))
        other = canonical(dict(json.loads(lines[-1]), drawn_main=[1, 2, 3, 4, 5, 6, 8]))
        for damaged, why in ((b''.join(lines[:-1]), 'does not hold a score for every forecast and readout'),
                             (raw + lines[0], 'not the one score of a forecast'),
                             (more + b''.join(lines[1:]), 'does not hold the matches of its frozen ticket'),
                             (b''.join(lines[:-1]) + other, 'disagree about the numbers drawn')):
            (folder / 'score_ledger.jsonl').write_bytes(damaged)
            with self.assertRaisesRegex(LS.LeagueRefused, why):
                LP.admit(self.GAME, attempt_id=attempt)
        (folder / 'score_ledger.jsonl').write_bytes(raw)
        sp = (folder / 'scoring_plan.json').read_bytes()
        (folder / 'scoring_plan.json').write_bytes(canonical(dict(json.loads(sp), declared_tests=1)))
        with self.assertRaisesRegex(LS.LeagueRefused, 'not the one its search-log row'):
            LP.admit(self.GAME, attempt_id=attempt)
        (folder / 'scoring_plan.json').write_bytes(sp)
        txt = next(LS.reports_dir(self.proj, self.GAME).glob(f'*{attempt}.txt'))
        raw = txt.read_bytes()
        txt.write_bytes(raw + b'x')
        with self.assertRaisesRegex(LS.LeagueRefused, 'not a complete development report'):
            LP.admit(self.GAME, attempt_id=attempt)
        txt.write_bytes(raw)
        self.assertTrue(OR.absent(path))
        self.assertEqual(LP.admit(self.GAME, batch_id=self.plan['batch_id'], **window),
                         {'state': 'ADMITTED', 'attempt_id': attempt})
        entry = SI.league_sources(self.proj, self.GAME)[0]
        self.assertEqual(entry['batch_kind'], 'WF_BATCH_PLAN_V1')
        self.assertEqual(entry['score_ledger_sha256'], sha256_hex((folder / 'score_ledger.jsonl').read_bytes()))
        self.assertEqual(SI.canonical_coverage(self.proj, self.GAME),
                         {(m['method_id'], m['method_revision'], m['variant_id'], t) for m, t in WF.plan_pairs(self.plan)})

    def test_a_repeat_changes_no_byte_and_a_changed_identity_refuses(self):
        attempt = self.report(self.plan)
        LP.admit(self.GAME, attempt_id=attempt)
        path = SI.league_sources_path(self.proj, self.GAME)
        raw, stat = path.read_bytes(), path.stat()
        with league_fault(0) as steps:
            for kw in ({'attempt_id': attempt}, {'batch_id': self.plan['batch_id'], 'first': self.plan['window_first'],
                                                 'last': self.plan['window_last']}):
                self.assertEqual(LP.admit(self.GAME, **kw)['state'], 'ALREADY_ADMITTED')
        self.assertEqual(steps, [])                           # not rewritten: not one durable step
        self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_ino), (raw, stat.st_mtime_ns, stat.st_ino))
        entry = SI.league_sources(self.proj, self.GAME)[0]
        for change in ({'score_ledger_sha256': 'f' * 64}, {'window_last': entry['window_last'] - 1},
                       {'evaluator_version': 'OTHER'}):
            self.sources = [dict(entry, **change)]
            self.write_sources()
            changed = path.read_bytes()
            with self.assertRaisesRegex(LS.LeagueRefused, 'already listed with a different'):
                LP.admit(self.GAME, attempt_id=attempt)
            self.assertEqual(path.read_bytes(), changed)

    def test_the_replace_is_atomic_and_an_interrupted_job_resumes(self):
        """A fault before the replace leaves the old file (here: no file); the rerun admits once; a fault between the
        admission and the publication, and after the row, each ends with one canonical score per key and one row."""
        attempt = self.report(self.plan)
        path = SI.league_sources_path(self.proj, self.GAME)
        with mock.patch.object(Path, 'replace', side_effect=B.Boom('before the replace')), self.assertRaises(B.Boom):
            LP.admit(self.GAME, attempt_id=attempt)
        self.assertTrue(OR.absent(path))                      # the old state, whole
        self.assertEqual(LP.admit(self.GAME, attempt_id=attempt)['state'], 'ADMITTED')
        for k in (1, 4):                                      # after the manifest; after the row
            self.change_inputs(k)
            with self.assertRaises(B.Boom), league_fault(k):
                LP.publish(self.GAME)
            self.assertEqual(LP.admit(self.GAME, attempt_id=attempt)['state'], 'ALREADY_ADMITTED')
            self.assertEqual(LP.publish(self.GAME)['state'], 'UP_TO_DATE')
            self.check_archive(settled=True)
        self.assertEqual(len(SI.league_sources(self.proj, self.GAME)), 1)
        keys = LS.canonical_keys(self.proj, self.GAME)
        self.assertEqual(len(keys), 2 * len(WF.plan_pairs(self.plan)))        # TOP and WORST, once each

    def test_a_routine_fill_is_admitted_and_an_exploratory_rerun_never(self):
        self.cover_the_prefix()                               # all but two prefix targets are covered (a fixture entry)
        self.sources = []
        SI.league_sources_path(self.proj, self.GAME).unlink() # ...but the league itself lists nothing yet
        fill = WF.make_dev_plan(self.GAME, 'EXPLORATORY_RERUN', B.adapters(), first=self.p.holdout_first - 2,
                                last=self.p.holdout_first - 1)
        self.assertEqual(self.run_plan(fill)[0], 0)
        attempt = self.report(fill)
        st = LS.batch_state(self.proj, self.GAME, fill['batch_id'])
        self.assertEqual((st['batch_kind'], st['complete'], st['admitted']), ('EXPLORATORY_RERUN', [attempt], None))
        for kw in ({'attempt_id': attempt}, {'batch_id': fill['batch_id']}):
            with self.assertRaisesRegex(LS.LeagueRefused, 'exploratory rerun is never admitted'):
                LP.admit(self.GAME, **kw)
        self.assertTrue(OR.absent(SI.league_sources_path(self.proj, self.GAME)))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(TOOL.main(['batch-state', '--game', self.GAME, '--batch', fill['batch_id']]), 0)
        self.assertEqual(out.getvalue().splitlines()[-1],
                         f'[LEAGUE] RESULT state=BATCH game={self.GAME} kind=EXPLORATORY_RERUN first={fill["window_first"]} '
                         f'last={fill["window_last"]} report={attempt} admitted=-')


class Seams(League):

    def test_ov1_reconcile_reads_the_publication_manifests(self):
        """EX_237 section 5: `ov1.publication_names` is connected. Every publication names the forecast-ledger extent
        it pinned; a ledger that no longer holds it, or a manifest that does not validate, blocks OV-1's missed line."""
        self.session()
        self.assertEqual(OV.publication_names(self.proj, self.GAME), [])
        res = LP.publish(self.GAME)
        lines = self.lines()
        names = OV.publication_names(self.proj, self.GAME)
        self.assertEqual(names, [{'what': f'league publication {res["name"]}', 'lines': len(lines),
                                  'last_line_digest': record_digest(lines[-1])}])
        st = {'rows': []}
        OV.reconcile(self.proj, self.GAME, st, lines, False, self.now)
        with self.assertRaisesRegex(OV.OV1Blocked, 'league publication ' + res['name']):
            OV.reconcile(self.proj, self.GAME, st, lines[:-1], False, self.now)
        path = LS.archive_dir(self.proj, self.GAME) / f'{res["name"]}.manifest.json'
        path.write_bytes(path.read_bytes().replace(b'"version":1', b'"version":7'))
        with self.assertRaisesRegex(OV.OV1Blocked, 'publication records do not verify'):
            OV.reconcile(self.proj, self.GAME, st, lines, False, self.now)

    def test_the_adapters_and_the_formatter_open_nothing_for_writing(self):
        """Sup 4 rule 4, statically: league_sources.py and league_table.py hold no call that creates, writes, renames
        or removes a file; league_publish.py is the only league module that does."""
        folder = Path(LS.__file__).parent
        writing = {'write_bytes', 'write_text', 'open', 'unlink', 'replace', 'rename', 'mkdir', 'rmdir', 'touch',
                   'create_only', 'append', '_append_search_row', 'link', 'symlink_to'}
        for name in ('league_sources.py', 'league_table.py'):
            tree = ast.parse((folder / name).read_text(encoding='ascii'))
            calls = {n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
            calls |= {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
            allowed = {'append', 'replace'} if name == 'league_sources.py' else {'append'}     # list.append, str.replace
            self.assertEqual((calls & writing) - allowed, set(), name)
        text = (folder / 'league_sources.py').read_text(encoding='ascii')
        self.assertEqual(text.count('.replace('), 2)          # both on the time-stamp text of a publication's name
        self.assertNotIn('outcome_reader', text + (folder / 'league_table.py').read_text(encoding='ascii') +
                         (folder / 'league_publish.py').read_text(encoding='ascii'))


if __name__ == '__main__':
    import unittest
    unittest.main()
