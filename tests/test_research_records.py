"""Tests of the engine's records: the two list files and their invariants, the status file, and scoring.

Each test is named for the rule it proves and plants the fault that rule must catch
(specification v0.6 section 18: "Records (F01)", "The status file"; sections 5.5, 5.6, 5.7, 3.5 and 8).
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import research_fixtures as fixtures
from _common.contract_records import record_digest
from research import reader, scoring, status_file, variant_lists as lists


def target_body(target: int, status: str = 'FORECAST', reason: str | None = None) -> dict:
    """A TARGET line's body (without "prev") for an invented variant."""
    content = {'game': 'POWERBALL', 'family': 'E_901', 'variant': 'TOY_COUNTS_V1', 'target': target, 'status': status}
    if reason:
        content['reason'] = reason
    return {'line': 'TARGET', 'content': content, 'content_digest': record_digest(content), 'envelope': {}}


def score_body(target: int, forecast_digest: str) -> dict:
    """A SCORE line's body (without "prev") naming a forecast by target and content digest."""
    return {'line': 'SCORE', 'content': {'target': target, 'forecast_content_digest': forecast_digest}, 'envelope': {}}


class TheTwoLists(unittest.TestCase):
    """Specification 5.2, 5.6 (invariants 1 to 4) and 5.7 (a torn last line)."""

    def setUp(self):
        """Two empty lists of an invented variant whose first target is 100."""
        self.folder = tempfile.TemporaryDirectory()
        self.forecasts_path, self.scores_path = lists.variant_list_paths(Path(self.folder.name), 'POWERBALL', 'E_901',
                                                                         'TOY_COUNTS_V1')
        identity = ('POWERBALL', 'E_901', 'TOY_COUNTS_V1', 'f' * 64, 'c' * 64)
        self.forecasts = lists.create_list(self.forecasts_path, lists.make_header('FORECASTS', *identity, first_target=100))
        self.scores = lists.create_list(self.scores_path, lists.make_header('SCORES', *identity))

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def add(self, *entries) -> None:
        """Append entries: ('F', target), ('N', target) for NO_FORECAST, ('S', target) for a score of that forecast."""
        for kind, target in entries:
            if kind == 'S':
                digest = next(l['content_digest'] for l in self.forecasts.lines if l['content']['target'] == target)
                lists.append_line(self.scores, score_body(target, digest))
            else:
                lists.append_line(self.forecasts, target_body(target, *(('NO_FORECAST', 'METHOD_FAILED') if kind == 'N' else ())))

    def check(self) -> dict:
        """Read both lists from disk and check them."""
        return lists.check_lists(lists.read_list(self.forecasts_path, 'FORECASTS'), lists.read_list(self.scores_path, 'SCORES'))

    def test_f01_a_method_failure_between_two_scored_forecasts_is_valid(self):
        self.add(('F', 100), ('S', 100), ('N', 101), ('F', 102), ('S', 102))
        summary = self.check()
        self.assertEqual((summary['first_target'], summary['next_target'], summary['first_unscored_forecast']), (100, 103, None))
        self.assertEqual((summary['scored'], summary['no_forecast']), ({100, 102}, {101: 'METHOD_FAILED'}))

    def test_a_pending_forecast_is_valid_and_is_the_first_unscored(self):
        self.add(('F', 100), ('S', 100), ('F', 101))
        self.assertEqual(self.check()['first_unscored_forecast'], 101)

    def test_a_gap_and_a_repeat_in_the_targets_are_refused(self):
        for second in (102, 100):
            self.tearDown()
            self.setUp()
            lists.append_line(self.forecasts, target_body(100))
            lists.append_line(self.forecasts, target_body(second))
            with self.assertRaisesRegex(lists.ListFault, 'no gap and no repeat'):
                self.check()

    def test_a_score_without_a_forecast_and_a_score_of_a_no_forecast_are_refused(self):
        self.add(('F', 100), ('N', 101))
        for target in (105, 101):
            lists.append_line(self.scores, score_body(target, 'a' * 64))
            with self.assertRaisesRegex(lists.ListFault, 'names no FORECAST line'):
                self.check()
            self.tearDown()
            self.setUp()
            self.add(('F', 100), ('N', 101))
        self.check()

    def test_a_score_naming_the_wrong_content_digest_is_refused(self):
        self.add(('F', 100))
        lists.append_line(self.scores, score_body(100, 'a' * 64))
        with self.assertRaisesRegex(lists.ListFault, 'names no FORECAST line'):
            self.check()

    def test_a_second_score_for_a_target_is_refused(self):
        self.add(('F', 100), ('S', 100), ('S', 100))
        with self.assertRaisesRegex(lists.ListFault, 'no target is scored twice'):
            self.check()

    def test_a_score_beyond_an_unscored_forecast_is_refused(self):
        self.add(('F', 100), ('F', 101), ('S', 101))
        with self.assertRaisesRegex(lists.ListFault, 'in order and complete'):
            self.check()

    def test_a_content_digest_that_is_not_the_contents_is_refused(self):
        body = target_body(100)
        body['content_digest'] = 'a' * 64
        lists.append_line(self.forecasts, body)
        with self.assertRaisesRegex(lists.ListFault, 'content digest'):
            self.check()

    def test_a_changed_removed_or_reordered_line_breaks_the_chain(self):
        self.add(('F', 100), ('F', 101), ('F', 102))
        original = self.forecasts_path.read_bytes()
        rows = original.split(b'\n')
        for damaged in (original.replace(b'"target":101', b'"target":201'),
                        b'\n'.join(rows[:2] + rows[3:]), b'\n'.join([rows[0], rows[2], rows[1], rows[3], b''])):
            self.forecasts_path.write_bytes(damaged)
            with self.assertRaisesRegex(lists.ListFault, 'chain is broken'):
                lists.read_list(self.forecasts_path, 'FORECASTS')
        self.forecasts_path.write_bytes(original.replace(rows[2], b'{not json'))
        with self.assertRaisesRegex(lists.ListFault, 'not a readable record'):
            lists.read_list(self.forecasts_path, 'FORECASTS')

    def test_a_list_of_the_wrong_kind_and_a_line_of_the_wrong_kind_are_refused(self):
        with self.assertRaisesRegex(lists.ListFault, 'not the header of a SCORES list'):
            lists.read_list(self.forecasts_path, 'SCORES')
        lists.append_line(self.forecasts, score_body(100, 'a' * 64))
        with self.assertRaisesRegex(lists.ListFault, 'a SCORE line in a FORECASTS list'):
            lists.read_list(self.forecasts_path, 'FORECASTS')

    def test_a_torn_last_line_in_each_file_is_cut_and_redone_to_the_uninterrupted_bytes(self):
        self.add(('F', 100), ('S', 100), ('F', 101), ('S', 101))
        whole = (self.forecasts_path.read_bytes(), self.scores_path.read_bytes())
        for path, kind, complete in ((self.forecasts_path, 'FORECASTS', whole[0]), (self.scores_path, 'SCORES', whole[1])):
            last = complete.rstrip(b'\n').split(b'\n')[-1]
            torn_at = len(complete) - len(last) - 1 + len(last) // 2
            path.write_bytes(complete[:torn_at])
            listed = lists.read_list(path, kind)
            self.assertEqual((len(listed.lines), listed.torn_bytes), (1, len(last) // 2))
            with self.assertRaisesRegex(lists.ListFault, 'must be cut'):
                lists.append_line(listed, {'line': 'TARGET'})
            self.assertEqual(lists.cut_torn_tail(listed), len(last) // 2)
            body = {key: value for key, value in __import__('json').loads(last).items() if key != 'prev'}
            lists.append_line(listed, body)
            self.assertEqual(path.read_bytes(), complete)
        self.check()

    def test_a_list_is_never_created_twice_but_the_debris_of_a_torn_header_is_started_afresh(self):
        with self.assertRaisesRegex(lists.ListFault, 'never created twice'):
            lists.create_list(self.forecasts_path, self.forecasts.header)
        header_bytes = self.forecasts_path.read_bytes()
        self.forecasts_path.write_bytes(header_bytes[:20])
        self.assertIsNone(lists.read_list(self.forecasts_path, 'FORECASTS'))
        lists.create_list(self.forecasts_path, self.forecasts.header)
        self.assertEqual(self.forecasts_path.read_bytes(), header_bytes)
        self.assertIsNone(lists.read_list(Path(self.folder.name) / 'absent.jsonl', 'FORECASTS'))

    def test_the_header_holds_the_identity_the_fingerprint_and_the_forecasting_code_identity(self):
        header = lists.read_list(self.forecasts_path, 'FORECASTS').header
        self.assertEqual((header['game'], header['family'], header['variant'], header['variant_fingerprint'],
                          header['forecasting_code_identity'], header['first_target'], header['prev']),
                         ('POWERBALL', 'E_901', 'TOY_COUNTS_V1', 'f' * 64, 'c' * 64, 100, None))
        self.assertNotIn('first_target', lists.read_list(self.scores_path, 'SCORES').header)
        self.assertEqual(str(self.forecasts_path.relative_to(self.folder.name)).replace(os.sep, '/'),
                         'results/research/POWERBALL/variants/E_901/TOY_COUNTS_V1/forecasts.jsonl')


class TheStatusFile(unittest.TestCase):
    """Specification 3.5: two facts for each game, each set at most once; written by one rename; checked."""

    GAMES = ('POWERBALL', 'OZLOTTO')

    def setUp(self):
        """A new ACTIVE status file of an invented variant."""
        self.folder = tempfile.TemporaryDirectory()
        self.tree = Path(self.folder.name) / 'tree'
        self.path = self.tree / 'src' / 'methods' / 'E_901' / 'TOY_COUNTS_V1' / 'VARIANT_STATUS.ini'
        self.path.parent.mkdir(parents=True)
        self.statuses = status_file.create_active(self.path, 'E_901', 'TOY_COUNTS_V1', self.GAMES)

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def withdrawn_and_eligible(self) -> dict:
        """Powerball eligible from 1596 and withdrawn from 1601; Oz Lotto eligible from 1712."""
        powerball = status_file.with_eligibility(self.statuses['POWERBALL'], 1596,
                                                 '2026-12-01 20:10; results on file through 1595 after a successful results step')
        powerball = status_file.with_withdrawal(powerball, 1601, 'the gap table was built from the wrong column',
                                                '2027-01-05 19:42; results on file through 1600')
        ozlotto = status_file.with_eligibility(self.statuses['OZLOTTO'], 1712,
                                               '2026-12-01 20:31; results on file through 1711 after a successful results step')
        return {'POWERBALL': powerball, 'OZLOTTO': ozlotto}

    def test_a_new_file_is_active_in_every_game_with_nothing_else_set(self):
        self.assertEqual(status_file.read_status(self.path, self.GAMES), {g: status_file.GameStatus() for g in self.GAMES})
        text = self.path.read_text()
        self.assertEqual(text.count('status = ACTIVE'), 2)
        self.assertNotIn('withdrawn', text.split('\n', 2)[2])
        with self.assertRaisesRegex(status_file.StatusRefused, 'never created twice'):
            status_file.create_active(self.path, 'E_901', 'TOY_COUNTS_V1', self.GAMES)

    def test_the_file_reads_as_the_specifications_example_and_round_trips(self):
        statuses = self.withdrawn_and_eligible()
        status_file.write_status(self.path, 'E_901', 'TOY_COUNTS_V1', statuses)
        self.assertEqual(status_file.read_status(self.path, self.GAMES), statuses)
        text = self.path.read_text()
        for line in ('; E_901 / TOY_COUNTS_V1 - operating status in THIS tree.', '[POWERBALL]', 'status = WITHDRAWN',
                     'withdrawn_from_draw = 1601', 'withdrawn_reason = the gap table was built from the wrong column',
                     'prevailing_ov1_first_eligible_draw = 1596', '[OZLOTTO]', 'status = ACTIVE',
                     'prevailing_ov1_first_eligible_draw = 1712', '[check]'):
            self.assertIn(line + '\n', text)

    def test_each_fact_is_set_at_most_once(self):
        statuses = self.withdrawn_and_eligible()
        with self.assertRaisesRegex(status_file.StatusRefused, 'set once and never changed'):
            status_file.with_eligibility(statuses['POWERBALL'], 1700, 'later')
        with self.assertRaisesRegex(status_file.StatusRefused, 'set once'):
            status_file.with_withdrawal(statuses['POWERBALL'], 1650, 'again', 'later')
        with self.assertRaisesRegex(status_file.StatusRefused, 'one line'):
            status_file.with_withdrawal(statuses['OZLOTTO'], 1650, 'two\nlines', 'later')

    def test_withdrawal_and_eligibility_decide_by_draw_number(self):
        powerball = self.withdrawn_and_eligible()['POWERBALL']
        self.assertEqual([powerball.is_withdrawn_at(d) for d in (1600, 1601, 1602)], [False, True, True])
        self.assertEqual([powerball.in_prevailing_cohort_at(d) for d in (1595, 1596, 1600, 1601)], [False, True, True, False])
        self.assertFalse(status_file.GameStatus().in_prevailing_cohort_at(1700))

    def test_a_hand_edit_a_deleted_check_and_a_missing_file_each_refuse_and_name_the_file(self):
        status_file.write_status(self.path, 'E_901', 'TOY_COUNTS_V1', self.withdrawn_and_eligible())
        good = self.path.read_bytes()
        for damaged, message in ((good.replace(b'withdrawn_from_draw = 1601', b'withdrawn_from_draw = 1701'), 'edited by hand'),
                                 (good.replace(b'status = WITHDRAWN', b'status = ACTIVE'), 'edited by hand'),
                                 (good.split(b'[check]')[0], 'no .check. section'),
                                 (good + b'extra = 1\n', 'edited by hand')):
            self.path.write_bytes(damaged)
            with self.assertRaisesRegex(status_file.StatusRefused, f'{self.path.name}.*{message}'):
                status_file.read_status(self.path, self.GAMES)
        self.path.unlink()
        with self.assertRaisesRegex(status_file.StatusRefused, 'missing.*newest backup'):
            status_file.read_status(self.path, self.GAMES)

    def test_a_file_whose_sections_are_not_the_variants_games_refuses(self):
        with self.assertRaisesRegex(status_file.StatusRefused, 'not the variant'):
            status_file.read_status(self.path, ('POWERBALL',))

    def test_a_failed_rename_leaves_the_old_file_and_nothing_new_in_the_variant_folder(self):
        before = self.path.read_bytes()
        with mock.patch.object(status_file, '_rename_into_place', side_effect=OSError('planted: the rename failed')):
            with self.assertRaises(OSError):
                status_file.write_status(self.path, 'E_901', 'TOY_COUNTS_V1', self.withdrawn_and_eligible())
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(status_file.read_status(self.path, self.GAMES), self.statuses)
        self.assertEqual([p.name for p in self.path.parent.iterdir()], ['VARIANT_STATUS.ini'],
                         'the unfinished copy is never among the variant\'s files (EX_283 F283-B01)')
        staged = self.tree / status_file.STAGING_FOLDER
        self.assertEqual([p.name for p in staged.iterdir()], ['E_901__TOY_COUNTS_V1__VARIANT_STATUS.ini.writing'])
        self.assertEqual(status_file.discard_unfinished_writes(self.tree),
                         ['E_901__TOY_COUNTS_V1__VARIANT_STATUS.ini.writing'])
        self.assertEqual(list(staged.iterdir()), [])
        self.assertEqual(status_file.discard_unfinished_writes(self.tree), [])
        status_file.write_status(self.path, 'E_901', 'TOY_COUNTS_V1', self.withdrawn_and_eligible())
        self.assertEqual(status_file.read_status(self.path, self.GAMES), self.withdrawn_and_eligible())
        self.assertEqual(list(staged.iterdir()), [], 'a finished write leaves nothing staged')

    def test_the_writer_refuses_a_path_that_is_not_a_status_file_in_a_variant_folder(self):
        for wrong in (Path(self.folder.name) / 'VARIANT_STATUS.ini',
                      self.tree / 'src' / 'methods' / 'E_901' / 'TOY_COUNTS_V1' / 'OTHER.ini',
                      self.tree / 'src' / 'E_901' / 'TOY_COUNTS_V1' / 'VARIANT_STATUS.ini'):
            with self.subTest(path=wrong):
                with self.assertRaisesRegex(status_file.StatusRefused, 'is written only as'):
                    status_file.write_status(wrong, 'E_901', 'TOY_COUNTS_V1', self.statuses)
                self.assertFalse(wrong.exists())

    def test_a_file_copied_back_from_a_backup_is_accepted(self):
        backup = self.path.read_bytes()
        status_file.write_status(self.path, 'E_901', 'TOY_COUNTS_V1', self.withdrawn_and_eligible())
        self.path.write_bytes(backup)
        self.assertEqual(status_file.read_status(self.path, self.GAMES), self.statuses)


class Scoring(unittest.TestCase):
    """Specification 8 and 5.5: TOP and WORST matches for each barrel and the prize divisions."""

    def setUp(self):
        """Invented results of both games."""
        self.folder = tempfile.TemporaryDirectory()
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'dev')
        fixtures.write_results(self.tree, 'POWERBALL', 1200)
        fixtures.write_results(self.tree, 'OZLOTTO', 1520)
        self.powerball = reader.results_on_file(self.tree, 'POWERBALL')
        self.ozlotto = reader.results_on_file(self.tree, 'OZLOTTO')

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def forecast(self, game_id: str, target: int, top_main, worst_main, top_pb=None, worst_pb=None) -> dict:
        """A FORECAST content with the given TOP and WORST sets."""
        barrels = {'MAIN': {'top': list(top_main), 'worst': list(worst_main)}}
        if game_id == 'POWERBALL':
            barrels['POWERBALL'] = {'top': [top_pb], 'worst': [worst_pb]}
        return {'game': game_id, 'target': target, 'status': 'FORECAST', 'barrels': barrels}

    def test_the_outcome_of_a_draw_is_read_from_its_own_row(self):
        row = fixtures.invented_row('POWERBALL', 1190, 1).split(',')
        outcome = scoring.read_outcome(self.powerball, 1190)
        self.assertEqual(outcome, {'MAIN': sorted(int(x) for x in row[2:9]), 'POWERBALL': [int(row[9])]})
        row = fixtures.invented_row('OZLOTTO', 1500, 1).split(',')
        self.assertEqual(scoring.read_outcome(self.ozlotto, 1500),
                         {'MAIN': sorted(int(x) for x in row[2:9]), 'SUPPLEMENTARY': sorted(int(x) for x in row[9:12])})

    def test_a_draw_not_on_file_and_a_malformed_row_refuse(self):
        for draw in (1201, 1143):
            with self.assertRaisesRegex(reader.ResultsRefused, 'not on file'):
                scoring.read_outcome(self.powerball, draw)
        rows = self.powerball.raw.split(b'\n')
        rows[1190 - 1144 + 1] = b'1190,2019-01-01,1,2,3,4,5,6,x,7'
        damaged = reader.ResultsOnFile('POWERBALL', b'\n'.join(rows), 'x', 1144, 1200, 1)
        with self.assertRaisesRegex(reader.ResultsRefused, 'malformed'):
            scoring.read_outcome(damaged, 1190)

    def test_a_powerball_ticket_matching_everything_wins_division_one_and_one_matching_nothing_wins_none(self):
        outcome = scoring.read_outcome(self.powerball, 1190)
        others = [n for n in range(1, 36) if n not in outcome['MAIN']][:7]
        other_pb = 1 if outcome['POWERBALL'][0] != 1 else 2
        content = scoring.score_content(self.forecast('POWERBALL', 1190, outcome['MAIN'], others, outcome['POWERBALL'][0], other_pb),
                                        'd' * 64, outcome)
        self.assertEqual(content, {'target': 1190, 'forecast_content_digest': 'd' * 64, 'drawn': outcome,
                                   'matches': {'MAIN': {'top': 7, 'worst': 0}, 'POWERBALL': {'top': 1, 'worst': 0}},
                                   'divisions': {'top': 1, 'worst': 0}})

    def test_partial_matches_are_counted_for_each_barrel_and_each_set(self):
        outcome = scoring.read_outcome(self.powerball, 1190)
        others = [n for n in range(1, 36) if n not in outcome['MAIN']]
        top = outcome['MAIN'][:3] + others[:4]
        worst = outcome['MAIN'][3:5] + others[4:9]
        content = scoring.score_content(self.forecast('POWERBALL', 1190, top, worst, 1 if outcome['POWERBALL'][0] != 1 else 2,
                                                      outcome['POWERBALL'][0]), 'd' * 64, outcome)
        self.assertEqual(content['matches'], {'MAIN': {'top': 3, 'worst': 2}, 'POWERBALL': {'top': 0, 'worst': 1}})

    def test_oz_lotto_uses_the_supplementaries_for_the_division_only_and_does_not_store_them(self):
        outcome = scoring.read_outcome(self.ozlotto, 1500)
        top = outcome['MAIN'][:6] + outcome['SUPPLEMENTARY'][:1]
        others = [n for n in range(1, 48) if n not in outcome['MAIN'] and n not in outcome['SUPPLEMENTARY']][:7]
        content = scoring.score_content(self.forecast('OZLOTTO', 1500, top, others), 'd' * 64, outcome)
        self.assertEqual(content['drawn'], {'MAIN': outcome['MAIN']})
        self.assertEqual((content['matches'], content['supplementary_matches']),
                         ({'MAIN': {'top': 6, 'worst': 0}}, {'top': 1, 'worst': 0}))
        self.assertEqual(content['divisions'], {'top': 2, 'worst': 0})
        self.assertNotIn(str(outcome['SUPPLEMENTARY']), str(content))

    def test_a_no_forecast_is_never_scored(self):
        with self.assertRaisesRegex(ValueError, 'only a FORECAST is scored'):
            scoring.score_content({'game': 'POWERBALL', 'target': 1190, 'status': 'NO_FORECAST'}, 'd' * 64,
                                  scoring.read_outcome(self.powerball, 1190))


if __name__ == '__main__':
    unittest.main()
