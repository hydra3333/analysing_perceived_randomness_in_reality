"""Tests of the two OV-1 series of a game: the arithmetic of one draw's line, who counts at a draw, and what the
print-outs say.

Each test is named for the rule it proves and plants the fault or the change that rule is about. Everything runs
on invented draws and toy methods.
(The simple scheme v0.2 section 5 step 6; specification v0.6 sections 10.1 to 10.5 for the arithmetic, which the
scheme keeps. Both series are exploratory indicators.)
"""
import csv
import io
import types
import unittest
from pathlib import Path

import research_fixtures as fx
from research import ov1_ledger
from research import ov1_numeric as kernel
from research.game_state import TargetFacts

GAME = fx.GAME
LAST_AT_START = fx.LAST_AT_START
THREE_METHODS = ('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5}))


def drawn_main(tree: Path, draw: int) -> list:
    """The seven main numbers of an invented draw, read straight from the tree's results file."""
    for row in csv.reader(io.StringIO((tree / 'source_data' / f'{GAME}_results_master.csv').read_text(encoding='ascii'))):
        if row[0] == str(draw):
            return [int(number) for number in row[2:9]]
    raise AssertionError(f'draw {draw} is not on file')


class WithASecondSeries(fx.JobCase):
    """A tree whose methods are in place since draw 1160, with the draws that then arrived."""

    def counted_tree(self, variants=THREE_METHODS, arrived: int = 3, name: str = 'tree') -> Path:
        """Make the tree: a first job with results through 1160 (every method counts from 1161), then `arrived`
        more draws and a second job."""
        tree = self.tree(variants=variants, name=name)
        self.assertEqual(fx.run_job(tree)[0], 0)
        if arrived:
            fx.write_results(tree, GAME, LAST_AT_START + arrived, version=2)
            code, said = fx.run_job(tree)
            self.assertEqual(code, 0, said)
        return tree


class TheSecondSeries(WithASecondSeries):
    """Each method counting from the draw after its establishment draw, up to its retirement draw."""

    def test_each_line_holds_the_weights_x_and_factors_of_its_counted_pairs_as_the_kernel_gives_them(self):
        tree = self.counted_tree()
        series = fx.ledger_lines(tree)
        self.assertEqual([line['content']['draw'] for line in series], [1161, 1162, 1163])
        running = [0] * len(kernel.LAMBDAS)
        for line in series:
            content, draw = line['content'], line['content']['draw']
            weights, x_from_scores = [0] * 35, 0
            for name in ('TOY_A_V1', 'TOY_B_V1', 'TOY_C_V1'):
                forecast = next(l['content'] for l in fx.list_lines(tree, 'E_901', name) if l['content']['target'] == draw)
                score = next(l['content'] for l in fx.list_lines(tree, 'E_901', name, 'scores')
                             if l['content']['target'] == draw)
                for number in forecast['barrels']['MAIN']['top']:
                    weights[number - 1] += 1
                for number in forecast['barrels']['MAIN']['worst']:
                    weights[number - 1] -= 1
                x_from_scores += score['matches']['MAIN']['top'] - score['matches']['MAIN']['worst']
            x = sum(weights[number - 1] for number in drawn_main(tree, draw))
            self.assertEqual((content['weights'], content['x']), (weights, x))
            self.assertEqual(x, x_from_scores)
            table = kernel.factor_table(weights)
            self.assertEqual(content['variance'], list(table['variance']))
            self.assertEqual(content['log_factors'], [str(row[x]) for row in table['rows']])
            running = [before + row[x] for before, row in zip(running, table['rows'])]
            self.assertEqual(content['running_logs'], [str(value) for value in running])
            self.assertEqual(content['score_lower_bound'], kernel.fixed_text(kernel.mixture_lower(running)))
            self.assertEqual(content['z'], kernel.z_text(x, *table['variance']))
            self.assertEqual(content['crossed'], kernel.crossing(running))
            self.assertEqual(sorted(line), ['audit', 'content', 'line'])
        self.assertEqual(series[0]['audit'], {'counted_before_result': 3, 'counted_after_result': 0,
                                              'computed_in': {'DEV': 3}})
        self.assertEqual(series[1]['audit']['counted_after_result'], 3,
                         'draws 1162 and 1163 arrived together with 1161: their forecasts were made afterwards')

    def test_a_member_with_no_forecast_is_recorded_as_no_pair_with_its_reason(self):
        tree = self.counted_tree(variants=('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5, 'fail_at': [1162]})))
        line = fx.ledger_lines(tree)[1]['content']
        self.assertEqual(line['cohort'], [{'variant': 'E_901/TOY_A_V1', 'state': 'counted'},
                                          {'variant': 'E_901/TOY_B_V1', 'state': 'counted'},
                                          {'variant': 'E_901/TOY_C_V1', 'state': 'no_pair', 'reason': 'METHOD_FAILED'}])
        self.assertLessEqual(max(abs(weight) for weight in line['weights']), 2, 'the weights come from the counted pairs')
        text = fx.report_text(tree, f'ov1/ov1_prevailing_{GAME}.txt')
        self.assertIn('Lines with a "no pair" member: 1, the first at draw 1162', text)

    def test_when_no_member_has_a_counted_pair_the_factor_is_exactly_one(self):
        tree = self.counted_tree(variants=(('TOY_A_V1', {'fail_at': [1162]}),))
        first, second = (line['content'] for line in fx.ledger_lines(tree)[:2])
        self.assertTrue(second['factor_is_one'])
        self.assertIsNone(second['z'])
        self.assertEqual(second['log_factors'], ['0'] * len(kernel.LAMBDAS))
        self.assertEqual(second['running_logs'], first['running_logs'])
        self.assertEqual(second['variance'], [0, 1])

    def test_a_member_whose_calculation_failed_stops_the_series_at_that_draw_and_it_is_said(self):
        tree = self.counted_tree(variants=('TOY_A_V1', ('TOY_B_V1', {'reverse': True, 'crash_at': [1163]})), arrived=0)
        fx.write_results(tree, GAME, LAST_AT_START + 4, version=2)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 1)
        self.assertEqual([line['content']['draw'] for line in fx.ledger_lines(tree)], [1161, 1162],
                         'a line is never made without a member that counts at its draw')
        stopped = [line for line in said if 'the second OV-1 series stops early' in line]
        self.assertEqual(len(stopped), 2, 'said when found and once more at the end of the job')
        self.assertIn('draw 1163: E_901/TOY_B_V1 has no line for it yet', stopped[0])
        self.assertIn('BLOCKED', fx.report_text(tree, f'ov1/ov1_prevailing_{GAME}.txt'))
        self.assertEqual([line['content']['draw'] for line in fx.ledger_lines(tree, which='exploratory')][-1], 1164,
                         'the series over all draws goes on with the methods that have a scored pair')

    def test_a_later_method_counts_from_the_draw_after_its_own_establishment_draw_and_not_before(self):
        tree = self.counted_tree(variants=('TOY_A_V1', 'TOY_B_V1'), arrived=2)
        self.add_variant(tree, 'TOY_LATE_V1', {'rotate': 11})
        fx.write_results(tree, GAME, LAST_AT_START + 4, version=3)
        self.assertEqual(fx.run_job(tree)[0], 0)
        self.assertEqual(self.status(tree, 'TOY_LATE_V1').eligible_from, LAST_AT_START + 5)
        fx.write_results(tree, GAME, LAST_AT_START + 5, version=4)
        self.assertEqual(fx.run_job(tree)[0], 0)
        sizes = {line['content']['draw']: len(line['content']['cohort']) for line in fx.ledger_lines(tree)}
        self.assertEqual(sizes, {1161: 2, 1162: 2, 1163: 2, 1164: 2, 1165: 3})
        everywhere = {line['content']['draw']: len(line['content']['cohort'])
                      for line in fx.ledger_lines(tree, which='exploratory')}
        self.assertEqual(everywhere[1161], 3, 'the series over all draws counts it wherever it has a scored pair')

    def test_a_method_given_an_establishment_draw_by_hand_counts_from_the_draw_after_it(self):
        tree = self.counted_tree(variants=('TOY_A_V1', 'TOY_B_V1'), arrived=0)
        fx.set_in_place(tree, 'E_901', 'TOY_A_V1', 1152)
        fx.set_in_place(tree, 'E_901', 'TOY_B_V1', 1156)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        sizes = {line['content']['draw']: len(line['content']['cohort']) for line in fx.ledger_lines(tree)}
        self.assertEqual(sizes, {1153: 1, 1154: 1, 1155: 1, 1156: 1, 1157: 2, 1158: 2, 1159: 2, 1160: 2})

    def test_with_no_method_in_place_before_a_draw_on_file_the_series_is_empty_and_says_where_it_starts(self):
        tree = self.counted_tree(arrived=0)
        self.assertEqual(fx.ledger_lines(tree), [])
        self.assertTrue((tree / 'results/research' / GAME / 'ov1/prevailing.jsonl').is_file(), 'the header alone')
        code, said = fx.run_job(tree)
        self.assertTrue(any('starts at draw 1161; no line yet' in line for line in said), said)


class TheSeriesOverAllDraws(WithASecondSeries):
    """Every method at every draw it has a scored pair."""

    def test_it_runs_from_the_first_scored_draw_and_its_file_holds_what_the_print_out_shows(self):
        tree = self.counted_tree()
        series = fx.ledger_lines(tree, which='exploratory')
        self.assertEqual([line['content']['draw'] for line in series], list(range(fx.FIRST_TOY_TARGET, 1164)))
        rows = [row for row in csv.reader(io.StringIO(fx.report_text(tree, f'ov1/ov1_exploratory_{GAME}.csv')))
                if row and row[0].isdigit()]
        self.assertEqual([int(row[0]) for row in rows], [line['content']['draw'] for line in series])
        self.assertEqual(series[-1]['content']['running_logs'],
                         [str(sum(int(line['content']['log_factors'][index]) for line in series))
                          for index in range(len(kernel.LAMBDAS))])

    def test_from_the_draw_every_method_counts_in_both_the_two_series_have_the_same_line_factors(self):
        tree = self.counted_tree()
        second = {line['content']['draw']: line['content'] for line in fx.ledger_lines(tree)}
        every = {line['content']['draw']: line['content'] for line in fx.ledger_lines(tree, which='exploratory')}
        for draw, content in second.items():
            self.assertEqual((content['weights'], content['x'], content['log_factors']),
                             (every[draw]['weights'], every[draw]['x'], every[draw]['log_factors']), draw)


class TheArithmeticOfOneLine(unittest.TestCase):
    """ov1_ledger.draw_line on states made by hand."""

    @staticmethod
    def state(identity: str, top, worst, top_matches: int, worst_matches: int):
        """A stand-in for one method's records at draw 1200: its two sets and its score line's matches."""
        facts = TargetFacts(status='FORECAST', reason=None, content_digest='d' * 64,
                            sets={'MAIN': {'top': tuple(top), 'worst': tuple(worst)}}, view_digest='v' * 64,
                            result_on_file=False, rerun=None, role='PROD')
        return types.SimpleNamespace(variant=types.SimpleNamespace(identity=identity), held=False, targets={1200: facts},
                                     score_contents={1200: {'matches': {'MAIN': {'top': top_matches,
                                                                                 'worst': worst_matches}}}})

    def test_x_from_the_weights_and_x_from_the_score_lines_must_agree(self):
        drawn = [1, 2, 3, 4, 5, 6, 7]
        good = self.state('E_901/A', range(1, 8), range(8, 15), 7, 0)
        line = ov1_ledger.draw_line(GAME, 1200, [good], drawn, [0] * 6)
        self.assertEqual(line['content']['x'], 7)
        wrong = self.state('E_901/A', range(1, 8), range(8, 15), 6, 0)
        with self.assertRaisesRegex(ValueError, 'X is 7 from the weights and 6 from the score lines'):
            ov1_ledger.draw_line(GAME, 1200, [wrong], drawn, [0] * 6)

    def test_weights_that_cancel_give_a_variance_of_zero_and_a_factor_of_exactly_one(self):
        first = self.state('E_901/A', range(1, 8), range(8, 15), 7, 0)
        second = self.state('E_901/B', range(8, 15), range(1, 8), 0, 7)
        content = ov1_ledger.draw_line(GAME, 1200, [first, second], [1, 2, 3, 4, 5, 6, 7], [5, 5, 5, 5, 5, 5])['content']
        self.assertEqual((content['weights'], content['x'], content['variance']), ([0] * 35, 0, [0, 1]))
        self.assertTrue(content['factor_is_one'])
        self.assertEqual(content['running_logs'], ['5'] * 6)

    def test_a_member_without_a_line_for_the_draw_blocks_the_line(self):
        absent = self.state('E_901/A', range(1, 8), range(8, 15), 7, 0)
        absent.targets = {}
        with self.assertRaisesRegex(ov1_ledger.Blocked, 'E_901/A has no line for it yet'):
            ov1_ledger.draw_line(GAME, 1200, [absent], [1, 2, 3, 4, 5, 6, 7], [0] * 6)


class ThePrintOuts(WithASecondSeries):
    """What the two OV-1 print-outs show beside the numbers."""

    def test_the_print_out_of_the_second_series_gives_the_plain_counts(self):
        tree = self.counted_tree()
        text = fx.report_text(tree, f'ov1/ov1_prevailing_{GAME}.txt')
        for wanted in (f'The tree that made this report: DEV at {tree}', 'Draws counted: 3',
                       'Counted forecasts made before the result was on file: 3; after: 6',
                       'Where the counted forecasts were computed: DEV 9', 'Lines with a "no pair" member: 0'):
            self.assertIn(wanted, text)
        self.assertNotRegex(text, 'SUPPORTED|QUALIFIED|sandbox')


if __name__ == '__main__':
    unittest.main()
