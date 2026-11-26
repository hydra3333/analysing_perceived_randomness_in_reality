"""Tests of the engine's records: the two list files, the three small files beside a method, and scoring.

Each test is named for the rule it proves and plants the fault that rule must catch.
(The simple scheme v0.2 sections 4 and 5 "The records"; specification v0.6 section 8 for scoring.)
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

import research_fixtures as fixtures
from research import method_flags as flags
from research import reader, scoring, variant_lists as lists


def target_body(target: int, status: str = 'FORECAST', reason: str | None = None) -> dict:
    """A TARGET line for an invented method."""
    content = {'game': 'POWERBALL', 'family': 'E_901', 'variant': 'TOY_COUNTS_V1', 'target': target, 'status': status}
    if reason:
        content['reason'] = reason
    return {'line': 'TARGET', 'content': content, 'content_digest': 'd' * 64, 'envelope': {}}


def score_body(target: int) -> dict:
    """A SCORE line for a target."""
    return {'line': 'SCORE', 'content': {'target': target, 'forecast_content_digest': 'd' * 64}, 'envelope': {}}


class TheTwoLists(unittest.TestCase):
    """Plain line records: a header, then one line a draw; what makes a pair of lists usable."""

    def setUp(self):
        """Two empty lists of an invented method whose first target is 100."""
        self.folder = tempfile.TemporaryDirectory()
        self.forecasts_path, self.scores_path = lists.variant_list_paths(Path(self.folder.name), 'POWERBALL', 'E_901',
                                                                         'TOY_COUNTS_V1')
        identity = ('POWERBALL', 'E_901', 'TOY_COUNTS_V1', 'f' * 64)
        self.forecasts = lists.create_list(self.forecasts_path, lists.make_header('FORECASTS', *identity, first_target=100))
        self.scores = lists.create_list(self.scores_path, lists.make_header('SCORES', *identity))

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def add(self, *entries) -> None:
        """Append entries: ('F', target), ('N', target) for NO_FORECAST, ('S', target) for a score."""
        for kind, target in entries:
            if kind == 'S':
                lists.append_line(self.scores, score_body(target))
            else:
                lists.append_line(self.forecasts, target_body(target, *(('NO_FORECAST', 'METHOD_FAILED') if kind == 'N' else ())))

    def check(self) -> dict:
        """Read both lists from disk and check them."""
        return lists.check_lists(lists.read_list(self.forecasts_path, 'FORECASTS'), lists.read_list(self.scores_path, 'SCORES'))

    def test_a_method_failure_between_two_scored_forecasts_is_valid(self):
        self.add(('F', 100), ('S', 100), ('N', 101), ('F', 102), ('S', 102))
        self.assertEqual(self.check(), {'first_target': 100, 'next_target': 103, 'scored': {100, 102}})

    def test_a_forecast_not_yet_scored_is_valid(self):
        self.add(('F', 100), ('S', 100), ('F', 101))
        self.assertEqual(self.check()['scored'], {100})

    def test_a_gap_and_a_repeat_in_the_targets_are_faults(self):
        for second in (102, 100):
            self.tearDown()
            self.setUp()
            lists.append_line(self.forecasts, target_body(100))
            lists.append_line(self.forecasts, target_body(second))
            with self.assertRaisesRegex(lists.ListFault, 'no gap and no repeat'):
                self.check()

    def test_a_score_without_a_forecast_and_a_score_of_a_no_forecast_are_faults(self):
        for target in (105, 101):
            self.tearDown()
            self.setUp()
            self.add(('F', 100), ('N', 101), ('S', target))
            with self.assertRaisesRegex(lists.ListFault, 'has no FORECAST line'):
                self.check()

    def test_a_second_score_for_a_draw_is_a_fault(self):
        self.add(('F', 100), ('S', 100), ('S', 100))
        with self.assertRaisesRegex(lists.ListFault, 'no draw is scored twice'):
            self.check()

    def test_a_score_beyond_an_unscored_forecast_is_a_fault(self):
        self.add(('F', 100), ('F', 101), ('S', 101))
        with self.assertRaisesRegex(lists.ListFault, 'in draw order and complete'):
            self.check()

    def test_a_line_that_is_not_a_record_is_a_fault_and_nothing_links_one_line_to_the_next(self):
        self.add(('F', 100), ('F', 101), ('F', 102))
        original = self.forecasts_path.read_bytes()
        rows = original.split(b'\r\n')
        self.assertEqual(len(rows), 5)
        for row in rows[:-1]:
            self.assertNotIn('prev', json.loads(row))
        self.forecasts_path.write_bytes(original.replace(rows[2], b'{not json'))
        with self.assertRaisesRegex(lists.ListFault, 'line 3: not a readable record'):
            lists.read_list(self.forecasts_path, 'FORECASTS')
        self.forecasts_path.write_bytes(b'\r\n'.join(rows[:2] + rows[3:]))          # a line taken out: found as a gap
        with self.assertRaisesRegex(lists.ListFault, 'no gap and no repeat'):
            self.check()

    def test_a_list_of_the_wrong_kind_and_a_line_of_the_wrong_kind_are_faults(self):
        with self.assertRaisesRegex(lists.ListFault, 'not the header of a SCORES list'):
            lists.read_list(self.forecasts_path, 'SCORES')
        lists.append_line(self.forecasts, score_body(100))
        with self.assertRaisesRegex(lists.ListFault, 'a SCORE line in a FORECASTS list'):
            lists.read_list(self.forecasts_path, 'FORECASTS')

    def test_a_list_of_the_earlier_format_is_not_read_as_this_one(self):
        self.forecasts_path.write_bytes(self.forecasts_path.read_bytes().replace(b'RESEARCH_LIST_V2', b'RESEARCH_LIST_V1'))
        with self.assertRaisesRegex(lists.ListFault, 'not the header of a FORECASTS list of format RESEARCH_LIST_V2'):
            lists.read_list(self.forecasts_path, 'FORECASTS')

    def test_a_torn_last_line_in_each_file_is_cut_and_redone_to_the_uninterrupted_bytes(self):
        self.add(('F', 100), ('S', 100), ('F', 101), ('S', 101))
        whole = (self.forecasts_path.read_bytes(), self.scores_path.read_bytes())
        for path, kind, complete in ((self.forecasts_path, 'FORECASTS', whole[0]), (self.scores_path, 'SCORES', whole[1])):
            last = complete[:-2].split(b'\r\n')[-1]
            for torn_bytes in (len(last) // 2, len(last) + 1):          # half a line; a whole line but for its last byte
                path.write_bytes(complete[:len(complete) - len(last) - 2 + torn_bytes])
                listed = lists.read_list(path, kind)
                self.assertEqual((len(listed.lines), listed.torn_bytes), (1, torn_bytes))
                with self.assertRaisesRegex(lists.ListFault, 'must be cut'):
                    lists.append_line(listed, {'line': 'TARGET'})
                self.assertEqual(lists.cut_torn_tail(listed), torn_bytes)
                lists.append_line(listed, json.loads(last))
                self.assertEqual(path.read_bytes(), complete)
        self.check()

    def test_a_file_with_no_complete_line_reads_as_no_list_and_is_begun_again(self):
        header_bytes = self.forecasts_path.read_bytes()
        self.forecasts_path.write_bytes(header_bytes[:20])
        self.assertIsNone(lists.read_list(self.forecasts_path, 'FORECASTS'))
        lists.create_list(self.forecasts_path, self.forecasts.header)
        self.assertEqual(self.forecasts_path.read_bytes(), header_bytes)
        self.assertIsNone(lists.read_list(Path(self.folder.name) / 'absent.jsonl', 'FORECASTS'))

    def test_the_header_names_the_method_and_the_fingerprint_of_the_software_that_made_the_list(self):
        header = lists.read_list(self.forecasts_path, 'FORECASTS').header
        self.assertEqual(header, {'line': 'HEADER', 'format': 'RESEARCH_LIST_V2', 'list': 'FORECASTS', 'game': 'POWERBALL',
                                  'family': 'E_901', 'variant': 'TOY_COUNTS_V1', 'variant_fingerprint': 'f' * 64,
                                  'first_target': 100})
        self.assertNotIn('first_target', lists.read_list(self.scores_path, 'SCORES').header)
        self.assertEqual(str(self.forecasts_path.relative_to(self.folder.name)).replace(os.sep, '/'),
                         'results/research/POWERBALL/variants/E_901/TOY_COUNTS_V1/forecasts.jsonl')

    def test_every_line_ends_crlf(self):
        self.add(('F', 100), ('S', 100))
        for path in (self.forecasts_path, self.scores_path):
            data = path.read_bytes()
            self.assertEqual((data.count(b'\r\n'), data.count(b'\n')), (2, 2))

    def test_keep_below_drops_the_lines_at_and_above_a_draw_and_nothing_else(self):
        self.add(('F', 100), ('S', 100), ('F', 101), ('S', 101), ('F', 102), ('S', 102), ('F', 103))
        whole = self.forecasts_path.read_bytes()
        self.assertEqual(lists.keep_below(self.forecasts_path, 'FORECASTS', 104), 0)
        self.assertEqual(self.forecasts_path.read_bytes(), whole)
        self.assertEqual(lists.keep_below(self.forecasts_path, 'FORECASTS', 102), 2)
        self.assertEqual(self.forecasts_path.read_bytes(), b'\r\n'.join(whole.split(b'\r\n')[:3]) + b'\r\n')
        self.assertEqual(lists.keep_below(self.scores_path, 'SCORES', 101), 2)
        self.assertEqual(self.check(), {'first_target': 100, 'next_target': 102, 'scored': {100}})
        self.assertEqual(lists.keep_below(Path(self.folder.name) / 'absent.jsonl', 'SCORES', 1), 0)

    def test_write_whole_writes_only_when_the_bytes_would_change(self):
        path = Path(self.folder.name) / 'series.jsonl'
        header = {'line': 'HEADER', 'format': lists.LIST_FORMAT, 'list': 'EXPLORATORY'}
        lines = [{'line': 'EXPLORATORY', 'content': {'draw': 100}, 'audit': {}}]
        self.assertTrue(lists.write_whole(path, header, lines))
        self.assertFalse(lists.write_whole(path, header, lines))
        self.assertTrue(lists.write_whole(path, header, lines + lines))
        self.assertEqual(len(lists.read_list(path, 'EXPLORATORY').lines), 2)
        self.assertEqual([entry.name for entry in path.parent.iterdir() if entry.name.endswith('.writing')], [])


class TheSmallFilesBesideAMethod(unittest.TestCase):
    """Scheme section 4: I_AM_RETIRED and IN_PLACE_SINCE, plain "key = value" text in the method's own folder."""

    def setUp(self):
        """An empty folder standing for a method's folder."""
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.folder = Path(self._temporary.name)

    def test_with_no_small_file_a_method_is_active_and_counts_nowhere_in_the_second_series(self):
        status = flags.status_of(self.folder, 'POWERBALL')
        self.assertEqual(status, flags.MethodStatus(None, None, None))
        self.assertFalse(status.is_withdrawn_at(1601) or status.in_prevailing_cohort_at(1601))

    def test_retirement_and_establishment_decide_by_draw_number(self):
        flags.write_retired(self.folder, {'POWERBALL': 1601, 'OZLOTTO': 1712}, 'the gap table was built from the wrong column')
        flags.settle_in_place(self.folder, 'ab12', 'POWERBALL', 1595)
        status = flags.status_of(self.folder, 'POWERBALL')
        self.assertEqual(status, flags.MethodStatus(1601, 'the gap table was built from the wrong column', 1596))
        self.assertEqual([status.is_withdrawn_at(draw) for draw in (1600, 1601, 1602)], [False, True, True])
        self.assertEqual([status.in_prevailing_cohort_at(draw) for draw in (1595, 1596, 1600, 1601)],
                         [False, True, True, False])
        self.assertEqual(flags.status_of(self.folder, 'OZLOTTO'), flags.MethodStatus(1712, status.withdrawn_reason, None))

    def test_the_files_are_plain_text_a_person_can_read_and_write(self):
        flags.write_retired(self.folder, {'POWERBALL': 1601}, 'superseded by V2')
        self.assertEqual((self.folder / flags.RETIRED_NAME).read_bytes(),
                         b'; ' + flags.RETIRED_FIRST_LINE.encode('ascii') + b'\r\n'
                         b'retired_from_POWERBALL = 1601\r\nreason = superseded by V2\r\n')
        (self.folder / flags.RETIRED_NAME).write_text('retired_from_POWERBALL = 1650\nreason = typed by hand\n',
                                                      encoding='ascii')
        self.assertEqual(flags.status_of(self.folder, 'POWERBALL'), flags.MethodStatus(1650, 'typed by hand', None))

    def test_the_establishment_draw_is_written_once_for_a_version_and_afresh_when_the_code_changes(self):
        self.assertTrue(flags.settle_in_place(self.folder, 'ab12', 'POWERBALL', 1595))
        self.assertFalse(flags.settle_in_place(self.folder, 'ab12', 'POWERBALL', 1599), 'written once for this version')
        self.assertTrue(flags.settle_in_place(self.folder, 'ab12', 'OZLOTTO', 1710), 'the other game, when first worked')
        self.assertEqual(flags.read_flag(self.folder / flags.IN_PLACE_NAME),
                         {'fingerprint': 'ab12', 'in_place_since_POWERBALL': '1595', 'in_place_since_OZLOTTO': '1710'})
        self.assertTrue(flags.settle_in_place(self.folder, 'cd34', 'POWERBALL', 1601), 'the code changed')
        self.assertEqual(flags.read_flag(self.folder / flags.IN_PLACE_NAME),
                         {'fingerprint': 'cd34', 'in_place_since_POWERBALL': '1601'})

    def test_an_establishment_file_that_cannot_be_read_is_written_afresh_and_stops_nothing(self):
        for damaged in (b'\xff\xfe', b'no equals sign here\r\n', b'fingerprint = ab12\r\nin_place_since_POWERBALL = soon\r\n'):
            (self.folder / flags.IN_PLACE_NAME).write_bytes(damaged)
            self.assertTrue(flags.settle_in_place(self.folder, 'ab12', 'POWERBALL', 1595))
            self.assertEqual(flags.status_of(self.folder, 'POWERBALL').eligible_from, 1596)

    def test_a_retired_file_without_a_draw_for_the_game_is_given_the_next_draw_and_its_reason_is_kept(self):
        self.assertFalse(flags.settle_retired(self.folder, 'POWERBALL', 1600), 'no file: nothing to do')
        (self.folder / flags.RETIRED_NAME).write_text('reason = tried by hand\n', encoding='ascii')
        self.assertTrue(flags.settle_retired(self.folder, 'POWERBALL', 1600))
        self.assertFalse(flags.settle_retired(self.folder, 'POWERBALL', 1605), 'the draw is written once')
        self.assertTrue(flags.settle_retired(self.folder, 'OZLOTTO', 1711))
        self.assertEqual(flags.read_flag(self.folder / flags.RETIRED_NAME),
                         {'retired_from_POWERBALL': '1601', 'retired_from_OZLOTTO': '1712', 'reason': 'tried by hand'})

    def test_a_retired_file_that_cannot_be_read_is_a_fault_that_names_the_file(self):
        path = self.folder / flags.RETIRED_NAME
        for damaged, said in ((b'\xff\xfe', 'not plain text'), (b'retired I think\r\n', 'line 1: not "key = value"'),
                              (b'retired_from_POWERBALL = soon\r\n', 'must be a draw number')):
            path.write_bytes(damaged)
            with self.assertRaisesRegex(flags.FlagFault, said) as fault:
                flags.settle_retired(self.folder, 'POWERBALL', 1600)
                flags.status_of(self.folder, 'POWERBALL')
            self.assertIn(str(path), str(fault.exception))

    def test_the_reason_of_a_retirement_is_one_line_of_plain_text(self):
        for reason in ('', '   ', 'two\nlines', 'caf' + chr(233)):
            with self.assertRaises(flags.FlagFault):
                flags.write_retired(self.folder, {'POWERBALL': 1601}, reason)
        self.assertFalse((self.folder / flags.RETIRED_NAME).exists())

    def test_a_small_file_is_put_in_place_whole(self):
        flags.write_retired(self.folder, {'POWERBALL': 1601}, 'a reason')
        self.assertEqual([entry.name for entry in self.folder.iterdir()], [flags.RETIRED_NAME])


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
