"""MHUP-B slice 3, layer L7: the consolidated report, the two labelled OV-1 views and the retired index (design
supplement v0.8 section 8; code plan v0.3 L7; the owner's clarification of 18 November 2026; EX_235 section 2;
EX_237 section 5). OFFLINE: the temporary weekly project; everything invented.

 Retrospective  THE SCIENCE OF USE (B). (1) Against an ORACLE written here that shares no code with the package: the
                weights from the forecast files on disk, the drawn numbers through the outcome reader, the fair-draw
                distribution by its own count, the factors in floating point. (2) Against USE (A): over the draws the
                formal stream counted, with the same variants, the retrospective X and Z are the formal ledger's.
                A member without a scored pair is counted as such; tickets that contradict the scores refuse.
 Two views      each under its own label in the text, the CSV and the manifest; no P value and no guarantee claimed
                for the retrospective one; the formal ledger and registration are byte-identical after any report.
 No pooling     the text, CSV and manifest hold no pooled or joint figure; a P value appears only on local,
                labelled, secondary rows; every part names its source.
 Parts          forward and catch-up kept apart and equal to counts made here; the matched-target view; the quoted
                reports by digest; each retired revision once; a failing part or report changes nothing else.
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import math
from pathlib import Path
from unittest import mock

import mhupb_fixtures as B
import test_mhupb_league as L
import test_mhupb_ov1 as O
import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.weekly_records as WR
from _common.contract_records import sha256_hex
from evaluation import Method_Weekly_Report as TOOL
from evaluation import consolidated_report as CRP
from evaluation import league_publish as LP
from evaluation import league_sources as LS
from evaluation import ov1 as OV
from evaluation import ov1_numeric as NUM
from evaluation import ov1_retrospective as RET
from evaluation import outcome_reader as RD


class Report(L.League, O.Stream):
    """The league fixture (development attempts, admission) with the OV-1 stream's helpers (register, week, result)."""
    EXTRA = 0

    def setUp(self):
        super().setUp()
        self.keep = 2

    def history(self, weeks=2, *, register=True, dev_keep=None):
        """An admitted development attempt over three prefix draws, then `weeks` forward draws frozen before their
        results, scored and (when registered) recorded by OV-1. Returns the forward targets."""
        keep, self.keep = self.keep, dev_keep or self.keep     # the development batch may hold fewer variants
        plan = self.v1_batch()
        LP.admit(self.GAME, attempt_id=self.report(plan))
        self.keep = keep
        if register:
            self.register()
        targets = []
        self.week(record=register)
        for _ in range(weeks):
            t = self.last_draw + 1
            self.result(t)
            self.week(record=register)
            targets.append(t)
        return plan, targets

    def run(self, result=None, **kw):
        if result is not None:
            return super().run(result)
        res = CRP.run_report(self.GAME, **kw)
        return res, CRP.build(res, CP.utc_now())

    # ------------------------------------------------------------ ORACLE (no code of the package's OV-1 or league modules)
    def oracle_series(self, members, targets):
        """target -> (weights, X, floating-point log-factors per lambda), from the files on disk: every forecast file
        of a member for the target (both tickets), the drawn numbers through the outcome reader, the fair-draw
        distribution of X by a count written here, V by its formula."""
        n = 35 if self.GAME == 'POWERBALL' else 47
        lam = (-0.2, -0.1, -0.05, 0.05, 0.1, 0.2)
        row = self.rows[-1]
        drawn = RD.read_outcome_rows(repo_root=self.proj, game_id=self.GAME, master_sha256=row['master_sha256'],
                                     targets=sorted(targets), ledger_version=row['version'])
        out = {}
        for t in sorted(targets):
            w = [0] * n
            for folder in self.run_folders():
                f = folder / CP.FILES['forecast']
                if not f.is_file():
                    continue
                fc = json.loads(f.read_bytes())
                if fc['target_draw_number'] != t or (fc['method_id'], fc['method_revision'], fc['variant_id']) not in members:
                    continue
                main = fc['barrels']['MAIN']
                for j in main['top']['labels']:
                    w[j - 1] += 1
                for j in main['worst']['labels']:
                    w[j - 1] -= 1
            x = sum(w[d - 1] for d in drawn[t][0])
            v = 7 * (n - 7) / (n - 1) * sum(a * a for a in w) / n
            if v == 0:
                out[t] = (w, x, None)
                continue
            dist = {(0, 0): 1}                                # (numbers chosen, sum of weights) -> how many ways
            for a in w:
                new = dict(dist)
                for (c, s), k in dist.items():
                    if c < 7:
                        new[(c + 1, s + a)] = new.get((c + 1, s + a), 0) + k
                dist = new
            counts = {s: k for (c, s), k in dist.items() if c == 7}
            self.assertEqual(sum(counts.values()), math.comb(n, 7))
            logs = []
            for l in lam:
                e0 = sum(k * math.exp(l * s / math.sqrt(v)) for s, k in counts.items()) / math.comb(n, 7)
                logs.append(l * x / math.sqrt(v) - math.log(e0))
            out[t] = (w, x, logs)
        return out


class Retrospective(Report):

    def test_the_series_equals_an_oracle_made_from_the_files_on_disk(self):
        plan, forward = self.history(register=False)
        data, _pins = LS.collect(self.proj, self.GAME)
        v = RET.view(self.proj, self.GAME, data)
        members = {(c['method'], c['revision'], c['variant']) for c in v['cohort']}
        self.assertEqual(len(members), 2)
        targets = list(range(plan['window_first'], plan['window_last'] + 1)) + forward
        self.assertEqual([s['target'] for s in v['series']], targets)
        want = self.oracle_series(members, targets)
        sums = [0.0] * 6
        for s in v['series']:
            w, x, logs = want[s['target']]
            self.assertEqual((s['x'], s['pairs'], s['cohort_without_pair']), (x, 2, 0), s['target'])
            if logs is None:
                self.assertEqual(s['state'], 'V0_SKIPPED')
            else:
                self.assertEqual(s['state'], 'COUNTED')
                v_exact = 7 * (len(w) - 7) / (len(w) - 1) * sum(a * a for a in w) / len(w)
                self.assertAlmostEqual(float(s['z']), x / math.sqrt(v_exact), places=9)
                sums = [a + b for a, b in zip(sums, logs)]
            score = sum(math.exp(a) for a in sums) / 6
            self.assertAlmostEqual(float(s['score_text']), score, places=9)
            self.assertLessEqual(float(s['score_text']), score + 1e-12)        # a proved LOWER bound, never above
        self.assertEqual(v['final_score_text'], v['series'][-1]['score_text'])
        self.assertEqual(v['highest_score_text'], max((s['score_text'] for s in v['series']), key=float))
        self.assertEqual((v['counted'] + v['skipped_v0'], v['first_target_at_or_above_reference']), (len(targets), None))
        self.assertEqual(v, RET.view(self.proj, self.GAME, data))             # the same inputs, the same result
        # a window is part of the view's identity and limits the series; sums start again at the window's first draw
        late = RET.view(self.proj, self.GAME, data, first=forward[0])
        self.assertEqual([s['target'] for s in late['series']], forward)
        self.assertNotEqual(late['identity_digest'], v['identity_digest'])
        only = sum(math.exp(sum(want[t][2][i] for t in forward if want[t][2])) for i in range(6)) / 6
        self.assertAlmostEqual(float(late['final_score_text']), only, places=9)

    def test_over_the_formal_streams_draws_the_arithmetic_is_the_formal_ledgers(self):
        """Use (B) against use (A): the forward draws were counted by the registered stream. With the same variants and
        the window set to those draws, the retrospective X, Z and running score are the formal FACTOR lines'."""
        _plan, forward = self.history()
        factors = {r['target_draw_number']: r for r in self.ov1_rows() if r['kind'] == 'FACTOR'}
        self.assertEqual(sorted(factors), forward)
        data, _pins = LS.collect(self.proj, self.GAME)
        v = RET.view(self.proj, self.GAME, data, first=forward[0], last=forward[-1])
        for s in v['series']:
            f = factors[s['target']]
            self.assertFalse(f['skipped'])
            self.assertEqual((s['x'], s['z'], s['score_text']), (f['x'], f['z'], f['score_text']), s['target'])
        self.assertEqual(v['final_score_text'], OV.status(self.GAME)['score_text'])

    def test_cohorts_missing_pairs_and_contradictions(self):
        plan, forward = self.history(register=False)
        self.keep = 3                                          # a third variant released now: it has no scored pair
        data, _pins = LS.collect(self.proj, self.GAME)
        v = RET.view(self.proj, self.GAME, data)
        self.assertEqual([c['pairs'] for c in v['cohort']].count(0), 1)
        self.assertEqual({s['cohort_without_pair'] for s in v['series']}, {1})          # counted as missing, never guessed
        self.assertIn('NO SCORED PAIR IN THE WINDOW', '\n'.join(RET.lines(v)))
        every = RET.view(self.proj, self.GAME, data, cohort='ALL')
        self.assertEqual((every['cohort_scope'], len(every['cohort'])), ('EVERY_SCORED_IDENTITY', 2))
        one = [v['cohort'][0]['method'], v['cohort'][0]['revision'], v['cohort'][0]['variant']]
        named = RET.view(self.proj, self.GAME, data, cohort=[one])
        self.assertEqual((named['cohort_scope'], {s['pairs'] for s in named['series']}), ('NAMED_LIST', {1}))
        self.assertEqual(len({v['identity_digest'], every['identity_digest'], named['identity_digest']}), 3)
        with self.assertRaisesRegex(RET.RetroRefused, 'neither released nor scored'):
            RET.view(self.proj, self.GAME, data, cohort=[['E_6', '9', 'NO_SUCH_V1']])
        good = RET.tickets(self.proj, self.GAME, data)
        key = sorted(k for k in good if k[:3] == tuple(one))[0]
        row = next(r for r in data['rows'] if (r['method'], r['revision'], r['variant'], r['target'], r['readout']) == (*key, 'TOP'))
        drawn, rest = row['drawn_main'], [j for j in range(1, 36) if j not in row['drawn_main']]
        hits = (row['main'] + 1) % 8                         # a ticket with a different number of matches than was scored
        other = tuple(drawn[:hits] + rest[:7 - hits])
        with mock.patch.object(RET, 'tickets', lambda *a: {**good, key: (other, good[key][1])}):
            with self.assertRaisesRegex(RET.RetroRefused, 'they must agree'):
                RET.view(self.proj, self.GAME, data, cohort=[one])
        with mock.patch.object(RET, 'tickets', lambda *a: {k: t for k, t in good.items() if k != key}):
            with self.assertRaisesRegex(RET.RetroRefused, 'no frozen forecast giving both tickets'):
                RET.view(self.proj, self.GAME, data)
        bad = dict(data, rows=[dict(r, drawn_main=[1, 2, 3, 4, 5, 6, 7]) if r is data['rows'][0] else r for r in data['rows']])
        with self.assertRaisesRegex(RET.RetroRefused, 'disagree about the numbers drawn'):
            RET.view(self.proj, self.GAME, bad)

    def test_all_weights_equal_is_a_neutral_draw(self):
        """Two variants whose tickets cancel give every number weight zero: V = 0, factor 1, typed V0_SKIPPED."""
        _plan, _forward = self.history(register=False, weeks=1)
        data, _pins = LS.collect(self.proj, self.GAME)
        good = RET.tickets(self.proj, self.GAME, data)
        t = min(r['target'] for r in data['rows'])
        a, b = sorted(k for k in good if k[3] == t)
        swap = {**good, b: (good[a][1], good[a][0])}          # b's TOP is a's WORST and the reverse
        rows = []
        for r in data['rows']:                                 # and b's scored matches are those of the swapped tickets
            if (r['method'], r['revision'], r['variant'], r['target']) == b:
                ticket = swap[b][0 if r['readout'] == 'TOP' else 1]
                r = dict(r, main=len(set(ticket) & set(r['drawn_main'])))
            rows.append(r)
        with mock.patch.object(RET, 'tickets', lambda *x: swap):
            v = RET.view(self.proj, self.GAME, dict(data, rows=rows))
        first = v['series'][0]
        self.assertEqual((first['target'], first['state'], first['x'], first['z'], first['score_text']),
                         (t, 'V0_SKIPPED', 0, None, NUM.fixed_text(NUM.S)))
        self.assertEqual(v['skipped_v0'], 1)

    def test_reaching_the_reference_line_is_reported_as_an_observation(self):
        """The first draw at or above 40 is named once, as an observation about history, with no P value. (Invented
        data cannot reach 40, so the kernel's comparison is made to say so from the second draw on.)"""
        self.history(register=False, weeks=1)
        data, _pins = LS.collect(self.proj, self.GAME)
        calls = []
        with mock.patch.object(NUM, 'crossing', lambda sums: calls.append(1) or len(calls) >= 2):
            v = RET.view(self.proj, self.GAME, data)
        self.assertEqual(v['first_target_at_or_above_reference'], v['series'][1]['target'])
        self.assertEqual([s['at_or_above_reference'] for s in v['series']], [False, True, True, True])
        text = '\n'.join(RET.lines(v))
        self.assertIn(f'first reached at draw {v["series"][1]["target"]} (an observation about history; not the '
                      f'registered finding and not a P value)', text)
        self.assertEqual(text.count('(at or above the reference line)'), 3)

    def test_the_view_cannot_reach_the_formal_ledger(self):
        """Statically: the retrospective module imports the kernel and the sources, never the recorder, and holds no
        writing call."""
        text = Path(RET.__file__).read_text(encoding='ascii')
        for banned in ('import ov1\n', 'from . import ov1 ', 'ledger_path', 'registration', 'JL.append', 'create_only',
                       'write_bytes', 'write_text', 'outcome_reader', '_append_search_row'):
            self.assertNotIn(banned, text.replace('ov1_retrospective', '').replace('ov1_numeric', '').replace(
                'the registered', '').replace('not the registered', ''), banned)


class Views(Report):

    def test_both_views_under_their_labels_and_the_formal_records_untouched(self):
        _plan, forward = self.history()
        LP.publish(self.GAME)
        before = {p: p.read_bytes() for p in (OV.ledger_path(self.proj, self.GAME), OV.registration_path(self.proj, self.GAME))}
        live, archive = self.live_bytes(), self.archive()
        res, out = self.run()
        self.assertEqual({p: p.read_bytes() for p in before}, before)          # the formal ledger: not one byte
        self.assertEqual((self.live_bytes(), self.archive()), (live, archive))
        text = out['txt'].decode('ascii')
        rows = list(csv.DictReader(io.StringIO(out['csv'].decode('ascii'))))
        man = json.loads(out['json'])
        a, b = text.index(f'2. {CRP.FORMAL_LABEL}'), text.index(f'3. {RET.LABEL}')
        formal_text, retro_text = text[a:b], text[b:text.index('4. SECONDARY')]
        # the formal view: its own label, bar 40, counted/skipped/missed, source, the guarantee WITH its assumptions
        s = OV.status(self.GAME)
        self.assertEqual((s['counted'], man['parts']['ov1_formal']['status']['counted']), (len(forward), len(forward)))
        for needle in (f'{s["counted"]} counted', f'bar {s["bar"]}', s['score_text'], '2.5%', 'provided that',
                       man['parts']['ov1_formal']['registration_digest'], 'not external proof', 'not proof of a cause'):
            self.assertIn(needle, formal_text, needle)
        for assumption in OV.RULES['operating_assumptions']:
            self.assertIn(assumption, formal_text)
        # the retrospective view: its own label everywhere it appears; no P value, no guarantee
        self.assertIn(RET.STATEMENT, retro_text)
        for claim in ('2.5%', 'p <', 'p=', 'p =', 'significan', 'guarantee applies', 'false-alarm guarantee holds'):
            self.assertNotIn(claim, retro_text.replace(RET.STATEMENT, '').lower(), claim)
        self.assertEqual({r['label'] for r in rows if r['part'] == 'OV1_RETROSPECTIVE'}, {RET.LABEL})
        self.assertEqual({r['label'] for r in rows if r['part'] == 'OV1_FORMAL'}, {CRP.FORMAL_LABEL})
        self.assertEqual({r['p'] for r in rows if r['part'].startswith('OV1_')}, {''})
        self.assertEqual((man['parts']['ov1_retrospective']['label'], man['parts']['ov1_formal']['label']),
                         (RET.LABEL, CRP.FORMAL_LABEL))
        self.assertEqual(man['parts']['ov1_retrospective']['reference_line'], 40)
        # the registry is the labels' one home
        reg = json.loads((Path(CRP.__file__).parent / 'registry' / 'MEASURE_REGISTRY_V1.json').read_bytes())
        self.assertEqual([u['label'] for u in reg['overall_measures'][0]['uses']], [CRP.FORMAL_LABEL, RET.LABEL])
        self.assertIn('CATCH_UP', [t['tier'] for t in reg['evidence_tiers']])

    def test_a_formal_stream_that_is_not_registered_stopped_or_unreadable_is_said_so(self):
        res, out = self.run()                                  # before anything: no registration, no source
        self.assertEqual(res['formal']['state'], 'NOT_REGISTERED')
        self.assertIn('NOT_REGISTERED', out['txt'].decode('ascii'))
        self.assertEqual((res['retrospective']['state'], res['retrospective']['targets']), ('COMPUTED', 0))
        self.history(weeks=1)
        self.assertEqual(self.run()[0]['formal']['state'], 'RUNNING')
        OV.stop(self.GAME, OV.STOP_STATEMENT)
        res, out = self.run()
        self.assertEqual(res['formal']['state'], 'STOPPED')
        self.assertIn('STREAM STOPPED', out['txt'].decode('ascii'))
        path = OV.ledger_path(self.proj, self.GAME)
        raw = path.read_bytes()
        path.write_bytes(raw[:-2] + b' \n')
        res, out = self.run()
        self.assertEqual(res['formal']['state'], 'NOT_AVAILABLE')
        self.assertEqual(res['retrospective']['state'], 'COMPUTED')            # one part's trouble stops no other part
        path.write_bytes(raw)


class Parts(Report):

    def test_nothing_is_pooled_and_every_part_names_its_source(self):
        """Plan L7's gate: search the text, the CSV and the manifest for any pooled or joint figure and find none; a P
        value appears only on local, labelled rows of the secondary tables."""
        from evaluation import league_table as LT
        self.history()
        LP.publish(self.GAME)
        with mock.patch.object(LT, 'build', side_effect=AssertionError('the report quotes the published table; it never rebuilds one')):
            res, out = self.run()
        text = out['txt'].decode('ascii')
        rows = list(csv.DictReader(io.StringIO(out['csv'].decode('ascii'))))
        man = json.loads(out['json'])
        self.assertIn(CRP.NO_POOLING, text)
        searched = (text + out['csv'].decode('ascii') + out['json'].decode('ascii')).lower()
        for sentence in (CRP.NO_POOLING, RET.STATEMENT, 'games never combined'):
            searched = searched.replace(sentence.lower(), '')
        for word in ('pooled', 'pooling', 'joint', 'combined', 'fisher', 'stouffer', 'overall p', 'both games',
                     'family-wise p', 'bonferroni-adjusted', 'meta-analy'):
            self.assertNotIn(word, searched, word)
        with_p = {r['part'] for r in rows if r['p'] not in ('', '-')}
        self.assertLessEqual(with_p, {'SECONDARY_FORWARD', 'SECONDARY_CATCH_UP'})
        self.assertEqual({r['label'] for r in rows if r['part'].startswith('SECONDARY_')}, {CRP.SECONDARY_LABEL})
        for r in rows:
            if r['part'].startswith('SECONDARY_') and r['p'] not in ('', '-'):
                self.assertTrue(r['labels'] and r['labels'] != '-', r)         # a local figure keeps its own label
        self.assertEqual(set(man['parts']), {'league_table', 'ov1_formal', 'ov1_retrospective', 'secondary',
                                             'matched_targets', 'quoted_reports', 'retired_index_sha256'})
        # identities: the quoted league table is the archive's bytes; the quoted report's digests are its files'
        lg = man['parts']['league_table']
        arch = self.archive()
        self.assertEqual(sha256_hex(arch[f'{lg["name"]}.txt']), lg['txt_sha256'])
        self.assertIn(arch[f'{lg["name"]}.txt'].decode('ascii'), text)
        q = man['parts']['quoted_reports'][0]
        for ext in ('txt', 'csv', 'json'):
            path = LS.reports_dir(self.proj, self.GAME) / f'{q["base"]}.{ext}'
            self.assertEqual(sha256_hex(path.read_bytes()), q['sha256'][ext])
        self.assertEqual(man['plan']['inputs'], LS.collect(self.proj, self.GAME)[1])
        self.assertEqual((man['text_sha256'], man['csv_sha256']), (sha256_hex(out['txt']), sha256_hex(out['csv'])))
        log = [r for r in LS.search_rows(self.GAME) if r['row_type'] == 'WEEKLY_REPORT']
        self.assertEqual([(r['attempt_id'], r['plan_digest']) for r in log], [(res['attempt_id'], res['plan_digest'])])

    def test_forward_and_catch_up_are_kept_apart_and_equal_to_counts_made_here(self):
        """Two draws frozen before their results (forward) and, after two missed weeks, two caught up: each class's
        MR7.MAIN total is the sum of that class's TOP matches in the score ledger, counted here."""
        self.history(register=False, weeks=2)
        a, b = self.last_draw + 1, self.last_draw + 2
        self.grow([a, b])                                      # two results accepted together: a was frozen, b missed
        self.now = self.at(b + 1, hours_before=30)
        self.week(record=False)
        captured = {}

        def stub(game, per_track, per_variant, families):
            captured.setdefault('calls', []).append((per_track, per_variant, families))
            return {'mr1': {}, 'mr5': {}, 'families': {}, 'R': 1, 'policy_id': 'STUB'}
        res, out = self.run(n1_runner=stub)
        want = {}
        for s in self.scores():
            key = (s['effective_class'], s['method_id'], s['method_revision'], s['variant_id'])
            e = want.setdefault(key, [0, 0])
            e[0] += 1
            e[1] += s['readouts']['TOP']['main_matches']
        self.assertEqual({k[0] for k in want}, {'PROSPECTIVE', 'CATCH_UP'})
        for name, cls in CRP.CLASSES:
            c = res['secondary']['classes'][name]
            got = {r['unit']: r for r in c['rows'] if r['sub_measure'] == 'MR7.MAIN' and r['unit'].endswith(':TOP')}
            mine = {f'{self.GAME}:{k[1]}:r{k[2]}:{k[3]}:TOP': v for k, v in want.items() if k[0] == cls}
            self.assertEqual(set(got), set(mine))
            for unit, (n, hits) in mine.items():
                self.assertEqual(got[unit]['n'], n)
                self.assertIn(f'main matches {hits};', got[unit]['descriptive'])
                self.assertIn('LOW_N', got[unit]['labels'])
            self.assertEqual(c['n1'], 'policy STUB, R = 1')
        self.assertEqual(res['secondary']['classes']['FORWARD']['score_lines'], 2 * 3)
        self.assertEqual(res['secondary']['classes']['CATCH_UP']['score_lines'], 2 * 1)
        # the Monte Carlo runner is handed the frozen tickets of exactly the class's draws, and no family
        tickets = RET.tickets(self.proj, self.GAME, res['data'])
        per_track, per_variant, families = captured['calls'][0]
        self.assertEqual(families, [])
        for (m, (rev, v), ro), tr in per_track.items():
            self.assertTrue(tr['track_id'].endswith(':WF'))
            self.assertEqual(sorted(tr['entries']), [x['draw_number'] for x in tr['targets']])
            for t, entry in tr['entries'].items():
                self.assertEqual(entry[0], tickets[(m, rev, v, t)][0 if ro == 'TOP' else 1])
        text = out['txt'].decode('ascii')
        self.assertIn(f'SECONDARY: THE FORWARD AND THE CATCH-UP TABLES ({CRP.SECONDARY_LABEL})', text)
        self.assertIn('nothing here is a confirmatory claim', text)

    def test_the_matched_view_the_retired_index_and_the_written_files(self):
        plan, forward = self.history(register=False, weeks=1, dev_keep=1)   # only the first variant has development scores
        members = self.members()
        gone = members[1]
        self.keep = 1                                          # the second variant is retired; its records stay
        self.retired[(gone['method_id'], gone['method_revision'], gone['variant_id'])] = '2026-01-01'
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(TOOL.main(['--game', self.GAME, '--ov1-cohort', 'all']), 0)
        last = out.getvalue().splitlines()[-1]
        self.assertRegex(last, rf'^\[WEEKLY-REPORT\] RESULT state=WRITTEN game={self.GAME} attempt=wr-[0-9a-f]{{32}}$')
        attempt = last.split('attempt=')[1]
        files = sorted(LS.reports_dir(self.proj, self.GAME).glob(f'weekly_report_*{attempt}*'))
        self.assertEqual([f.name.split(attempt)[1] for f in files], ['.csv', '.json', '.txt', '_retired_index.json'])
        man = json.loads(next(f for f in files if f.name.endswith(f'{attempt}.json')).read_bytes())
        index = json.loads(files[-1].read_bytes())
        self.assertEqual(sha256_hex(files[-1].read_bytes()), man['parts']['retired_index_sha256'])
        self.assertEqual([(r['method'], r['revision'], r['variant']) for r in index['retired']],
                         [(gone['method_id'], gone['method_revision'], gone['variant_id'])])          # once
        entry = index['retired'][0]
        self.assertEqual((entry['last_scored_target'], entry['score_records']), (forward[-1], 2 * 1))
        self.assertEqual(entry['records_in'], [LS.WEEKLY_SOURCE])
        mt = man['parts']['matched_targets']
        self.assertEqual((mt['variants'], mt['matched_draws'], mt['first'], mt['last']), (2, 1, forward[-1], forward[-1]))
        hits = {}
        for s in self.scores():
            hits[s['variant_id']] = hits.get(s['variant_id'], 0) + s['readouts']['TOP']['main_matches']
        self.assertEqual(len(self.dev_records(plan, SI_attempt(self))), 2 * 3)      # one variant's, left out of the match
        self.assertEqual({r['variant']: r['hits'] for r in mt['rows']}, hits)
        self.assertEqual(man['parts']['ov1_retrospective']['cohort_scope'], 'EVERY_SCORED_IDENTITY')
        # the tool ran WF-1B's own Monte Carlo runner (the approved seed policy installed in the tree) on the forward tracks
        from evaluation import seed_policies as SP
        policy = SP.approved_policy()
        if policy is not None:
            self.assertEqual(man['parts']['secondary']['classes']['FORWARD']['n1'], f'policy {policy["policy_id"]}, R = 10000')
            rows = list(csv.DictReader(io.StringIO(next(f for f in files if f.name.endswith('.csv')).read_text())))
            mc = [r for r in rows if r['monte_carlo']]
            self.assertEqual({r['part'] for r in mc}, {'SECONDARY_FORWARD'})
            self.assertEqual({r['item'] for r in mc} & {'MR1', 'MR5.MAIN'}, {'MR1', 'MR5.MAIN'})
            text = next(f for f in files if f.name.endswith('.txt')).read_text()
            self.assertIn(mc[0]['monte_carlo'], text)
        self.assertEqual(man['parts']['league_table']['state'], 'NOT_AVAILABLE')            # none published: said so

    def test_a_failing_report_changes_nothing_else_and_refusals_write_nothing(self):
        self.history(weeks=1)
        LP.publish(self.GAME)
        snap = lambda: (self.weekly_bytes(), self.archive(), self.current(),
                        LS.SI.league_sources_path(self.proj, self.GAME).read_bytes(),
                        sorted(p.name for p in LS.reports_dir(self.proj, self.GAME).glob('weekly_report_*')))
        before, rows = snap(), len(LS.search_rows(self.GAME))
        err = io.StringIO()
        with mock.patch.object(CRP, 'matched_part', side_effect=RuntimeError('injected')), \
                contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(err):
            self.assertEqual(TOOL.main(['--game', self.GAME]), 1)
        self.assertEqual(out.getvalue().splitlines()[-1], f'[WEEKLY-REPORT] RESULT state=FAILED game={self.GAME} attempt=-')
        self.assertEqual(snap(), before)
        self.assertEqual(len(LS.search_rows(self.GAME)), rows + 1)             # the attempt stays counted
        marker = Path(CR.ORPHAN_MARKER)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_bytes(b'{}')
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            self.assertEqual(TOOL.main(['--game', self.GAME]), 2)
        marker.unlink()
        self.assertEqual((snap(), len(LS.search_rows(self.GAME))), (before, rows + 1))
        one = self.members()[0]                                # a named cohort at the command line: one variant, scoped
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(TOOL.main(['--game', self.GAME, '--ov1-cohort', f'{one["method_id"]}:{one["method_revision"]}:'
                                        f'{one["variant_id"]}', '--ov1-first', str(self.first)]), 0)
        named = json.loads(sorted(LS.reports_dir(self.proj, self.GAME).glob('weekly_report_*wr-*[0-9a-f].json'))[-1].read_bytes())
        part = named['parts']['ov1_retrospective']
        self.assertEqual((part['cohort_scope'], len(part['cohort']), part['window']), ('NAMED_LIST', 1, [self.first, None]))
        for bad in ('E_6:1', 'a:b:c:d', ':1:x'):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                TOOL.main(['--game', self.GAME, '--ov1-cohort', bad])
        with mock.patch.object(RET, 'view', side_effect=RET.RetroRefused('injected disagreement')):
            res, built = self.run()
        self.assertEqual(res['retrospective']['state'], 'NOT_AVAILABLE')
        self.assertIn('NOT AVAILABLE: injected disagreement', built['txt'].decode('ascii'))
        self.assertEqual(res['formal']['state'], 'RUNNING')


def SI_attempt(case) -> str:
    return LS.SI.league_sources(case.proj, case.GAME)[0]['attempt_id']


if __name__ == '__main__':
    import unittest
    unittest.main()
