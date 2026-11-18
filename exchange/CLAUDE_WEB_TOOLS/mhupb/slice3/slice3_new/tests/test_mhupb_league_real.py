"""MHUP-B slice 3, layer L4: the adapters on the COMMITTED REAL score records (code plan v0.3 section 8; EX_223 CP-Q9).

Kept apart from test_mhupb_league.py on purpose: passing on writer-made fixtures is not the same claim as reading the
real records. This module only READS, from the tree it runs in: the two development score ledgers and the two sealed
Mode H score ledgers the owner committed on 17 November 2026 (`cc665ce`), and their plans, markers and search-log rows.
It checks counts and identities against the census of plan section 8 (made by `score_census.py`), and that "Mode H as
sealed" never enters a total. It writes nothing, runs nothing and reads no master. Where the records are not in the
tree (a clone without `results/`), every test is skipped, saying so.

NOT covered here: the admission step's check of every score against its frozen forecast needs the batch's run folders,
which are on the owner's PC only (they are not committed). That check runs on writer-made records in
test_mhupb_league.py, and on the real ones at the first use on the owner's PC.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

import _common.contract_runner as CR
import _common.walk_forward as WF
from _common.contract_records import record_digest, sha256_hex
from evaluation import league_sources as LS
from evaluation import league_table as LT

ROOT = Path(__file__).resolve().parents[1]
CENSUS = {'OZLOTTO': {'attempt': 'rr-4be324abd2e04dfd84b3e8087e308770', 'batch': 'wf-a75988650fb04cc399f8f7409ea27243',
                      'window': (1474, 1693), 'scored': (1475, 1693), 'score_lines': 11916, 'holdout': (1694, 1703)},
          'POWERBALL': {'attempt': 'rr-97bb48617b994a8ea18332cd36bbc98f', 'batch': 'wf-3347ad1160df45faaaab1e2eedcedd0f',
                        'window': (1286, 1576), 'scored': (1286, 1576), 'score_lines': 22884, 'holdout': (1577, 1586)}}


class RealRecords(unittest.TestCase):

    def setUp(self):
        self.patch = mock.patch.object(CR, 'PROJECT_ROOT', ROOT)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        for game, c in CENSUS.items():
            if not (LS.scores_folder(game, c['batch'], c['attempt']) / 'score_ledger.jsonl').is_file():
                self.skipTest('the committed real score records are not in this tree')

    def entry(self, game):
        """The source-list entry the admission step would write, built here from the real files (the admission's own
        forecast check cannot run in a tree without the run folders)."""
        c = CENSUS[game]
        folder = LS.scores_folder(game, c['batch'], c['attempt'])
        sp = json.loads((folder / 'scoring_plan.json').read_bytes())
        plan = WF.load_plan(game, c['batch'])
        return {'attempt_id': c['attempt'], 'batch_id': c['batch'], 'batch_kind': 'WF_BATCH_PLAN_V1',
                'plan_digest': record_digest(plan), 'window_first': sp['window_first'], 'window_last': sp['window_last'],
                'score_ledger_sha256': sha256_hex((folder / 'score_ledger.jsonl').read_bytes()),
                'evaluator_version': sp['evaluator_version']}

    def test_the_development_adapter_reads_the_real_ledgers_as_the_census_counted_them(self):
        for game, c in CENSUS.items():
            entry = self.entry(game)
            self.assertEqual((entry['window_first'], entry['window_last']), c['window'])
            rows = LS.source_rows(game, entry)
            self.assertEqual(len(rows), c['score_lines'], game)
            self.assertEqual((min(r['target'] for r in rows), max(r['target'] for r in rows)), c['scored'])
            self.assertEqual(len({(r['method'], r['variant'], r['readout']) for r in rows}), 80)       # 80 tracks
            self.assertEqual(len({(r['method'], r['revision'], r['variant'], r['target'], r['readout']) for r in rows}),
                             len(rows))                                                               # every key once
            self.assertEqual({r['revision'] for r in rows}, {'1', '2'})                              # CF-10
            self.assertEqual({r['kind'] for r in rows}, {'DEVELOPMENT'})
            row = [r for r in LS.search_rows(game) if r['attempt_id'] == c['attempt']]
            self.assertEqual([r['row_type'] for r in row], ['RANKING_REPORT'])
            with self.assertRaisesRegex(LS.LeagueRefused, 'not the bytes the source list names'):
                LS.source_rows(game, dict(entry, score_ledger_sha256='0' * 64))

    def test_mode_h_as_sealed_is_read_by_its_recorded_digest_and_never_summed(self):
        for game, c in CENSUS.items():
            ident = LS.mode_h_identity(ROOT, game)
            self.assertIsNotNone(ident, game)
            entry = self.entry(game)
            with mock.patch.object(LS.SI, 'league_sources', lambda root, g, e=entry: [e]), \
                    mock.patch.object(LS, 'sources_file_digest', lambda root, g: 'a' * 64):
                data, pins = LS.collect(ROOT, game)
            mh = data['mode_h']
            self.assertIsNone(mh['not_available'], game)
            self.assertEqual(len(mh['rows']), 800, game)                       # 40 variants x 10 draws x TOP and WORST
            self.assertEqual((min(r['target'] for r in mh['rows']), max(r['target'] for r in mh['rows'])), c['holdout'])
            self.assertEqual(pins['mode_h'], ident)
            self.assertEqual(len(data['rows']), c['score_lines'])              # the summed rows: development only
            self.assertFalse(any(c['holdout'][0] <= r['target'] <= c['holdout'][1] for r in data['rows']))
            entries = LT.summarise(data)
            self.assertEqual(sum(e['all_draws'] for e in entries), c['score_lines'] // 2)            # TOP records
            self.assertEqual(sum(e['mode_h'][0] for e in entries), 400)
            self.assertEqual(sum(e['kinds']['DEVELOPMENT'][0] for e in entries), c['score_lines'] // 2)
            # an independent count of the TOP hits straight from the file
            folder = LS.scores_folder(game, c['batch'], c['attempt'])
            hits = sum(json.loads(x)['main_matches'] for x in (folder / 'score_ledger.jsonl').read_text().splitlines()
                       if ':TOP:' in json.loads(x)['track_id'])
            self.assertEqual(sum(e['all_hits'] for e in entries), hits)
            built = LT.build(data, {'name': 'league_REAL_CHECK', 'version': 1, 'latest_draw': LT.latest_draw(data),
                                    'published_utc': '2026-11-18T00:00:00.000000Z'})
            text = built['txt'].decode('ascii')
            self.assertIn(c['attempt'], text)
            self.assertIn(f'starts at draw {c["scored"][0]}', text)
            self.assertIn(ident['score_ledger_sha256'], text)
            self.assertNotIn('not available', text)


if __name__ == '__main__':
    unittest.main()
