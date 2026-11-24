"""Tests of OV-1, the derived check and the withdrawal (specification v0.6 sections 5.8, 10 and 11), on invented
draws and toy variants.

Each test is named for the rule it proves. The OV-1 lines the job stores are checked against an independent
recomputation from the lists and the results file, and against the passed kernel called directly.
"""
import copy
import csv
import io
import json
import re
import shutil
import types
import unittest
from pathlib import Path
from unittest import mock

import research_fixtures as fx
from research import derived_check, job_lock, ov1_ledger, reports, research_job, results_step, withdraw
from research import ov1_numeric as kernel
from research.game_state import TargetFacts
from research.settings import read_settings
from research.status_file import GameStatus, write_status
from research.variant_folders import read_variant

GAME = fx.GAME
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SPECIFICATION = REPOSITORY_ROOT / 'doc' / 'Predictive_Randomness_System_Specification_v0_6.md'
LAST_AT_START, LAST_IN_SOURCE = fx.LAST_AT_START, fx.LAST_IN_SOURCE
THREE_VARIANTS = ('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5}))


def drawn_main(tree: Path, draw: int) -> list:
    """The seven main numbers of an invented draw, read straight from the tree's results file."""
    for row in csv.reader(io.StringIO((tree / 'source_data' / f'{GAME}_results_master.csv').read_text(encoding='ascii'))):
        if row[0] == str(draw):
            return [int(number) for number in row[2:9]]
    raise AssertionError(f'draw {draw} is not on file')


def cutoff_record(tree: Path) -> dict | None:
    """The not-current marker of the test game as a record, or None if there is none."""
    path = derived_check.cutoff_path(tree, GAME)
    return json.loads(path.read_text(encoding='ascii')) if path.exists() else None


def active_reports(tree: Path, folder: str) -> list:
    """The names of the files in one folder of the active reports ('league', 'next' or 'ov1')."""
    top = tree / 'results/research' / GAME / 'reports' / folder
    return sorted(path.name for path in top.iterdir()) if top.is_dir() else []


class WithALedger(fx.JobCase):
    """A tree whose variants count from draw 1161, with prevailing lines for the draws that then arrived."""

    def counted_tree(self, variants=THREE_VARIANTS, arrived: int = 3, name: str = 'tree') -> Path:
        """Make the tree: a first job with results through 1160 (eligibility draws 1161), then `arrived` more
        draws copied and caught up."""
        tree = self.tree(variants=variants, name=name)
        self.assertEqual(fx.run_job(tree)[0], 0)
        if arrived:
            self.source(LAST_AT_START + arrived, version=2)
            code, said = fx.run_job(tree)
            self.assertEqual(code, 0, said)
        return tree


class PrevailingLines(WithALedger):
    """Specification 10.1 to 10.4 (F03)."""

    def test_each_line_holds_the_weights_x_and_factors_of_its_counted_pairs_as_the_kernel_gives_them(self):
        tree = self.counted_tree()
        ledger = fx.ledger_lines(tree)
        self.assertEqual([line['content']['draw'] for line in ledger], [1161, 1162, 1163])
        running = [0] * len(kernel.LAMBDAS)
        for line in ledger:
            content, draw = line['content'], line['content']['draw']
            weights, x_from_scores = [0] * 35, 0
            for name in ('TOY_A_V1', 'TOY_B_V1', 'TOY_C_V1'):
                forecast = next(l['content'] for l in fx.list_lines(tree, 'E_901', name) if l['content']['target'] == draw)
                score = next(l['content'] for l in fx.list_lines(tree, 'E_901', name, 'scores') if l['content']['target'] == draw)
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
            self.assertEqual(line['envelope']['rerun'], None)
        self.assertEqual(ledger[0]['audit'], {'counted_before_result': 3, 'counted_after_result': 0,
                                              'computed_in': {'QA': 3}})
        self.assertEqual(ledger[1]['audit']['counted_after_result'], 3,
                         'draws 1162 and 1163 arrived together with 1161: their forecasts were made afterwards')

    def test_a_cohort_member_with_no_forecast_is_recorded_as_no_pair_with_its_reason(self):
        tree = self.counted_tree(variants=('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5, 'fail_at': [1162]})))
        line = fx.ledger_lines(tree)[1]['content']
        self.assertEqual(line['cohort'], [{'variant': 'E_901/TOY_A_V1', 'state': 'counted'},
                                          {'variant': 'E_901/TOY_B_V1', 'state': 'counted'},
                                          {'variant': 'E_901/TOY_C_V1', 'state': 'no_pair', 'reason': 'METHOD_FAILED'}])
        self.assertLessEqual(max(abs(weight) for weight in line['weights']), 2, 'the weights come from the counted pairs only')
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

    def test_a_missing_member_blocks_the_line_which_is_never_skipped(self):
        tree = self.counted_tree(variants=('TOY_A_V1', 'TOY_B_V1'), arrived=0)
        twin = self.counted_tree(variants=('TOY_A_V1', 'TOY_B_V1'), arrived=0, name='twin')
        self.source(LAST_AT_START + 2, version=2)
        code, said = fx.run_job(tree, only=['E_901/TOY_A_V1'])
        self.assertEqual(code, 0, said)
        self.assertEqual(fx.ledger_lines(tree), [])
        blocked = [line for line in said if 'blocked, not skipped' in line]
        self.assertEqual(len(blocked), 2, 'said once when found and once more at the end of the job')
        self.assertIn('draw 1161: the forecast of E_901/TOY_B_V1 is not scored yet', blocked[0])
        self.assertIn('BLOCKED', fx.report_text(tree, f'ov1/ov1_prevailing_{GAME}.txt'))
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        fx.run_job(twin)
        self.assertEqual([line['content'] for line in fx.ledger_lines(tree)],
                         [line['content'] for line in fx.ledger_lines(twin)])
        self.assertEqual([line['content']['draw'] for line in fx.ledger_lines(tree)], [1161, 1162])

    def test_a_later_variant_counts_from_its_own_eligibility_draw_and_not_before(self):
        tree = self.counted_tree(variants=('TOY_A_V1', 'TOY_B_V1'), arrived=2)
        self.add_variant(tree, 'TOY_LATE_V1', {'rotate': 11})
        self.source(LAST_AT_START + 4, version=3)
        self.assertEqual(fx.run_job(tree)[0], 0)
        self.assertEqual(self.status(tree, 'TOY_LATE_V1').eligible_from, LAST_AT_START + 5)
        self.source(LAST_AT_START + 5, version=4)
        self.assertEqual(fx.run_job(tree)[0], 0)
        sizes = {line['content']['draw']: len(line['content']['cohort']) for line in fx.ledger_lines(tree)}
        self.assertEqual(sizes, {1161: 2, 1162: 2, 1163: 2, 1164: 2, 1165: 3})

    def test_the_stored_ledger_equals_its_rebuild(self):
        tree = self.counted_tree()
        code, said = fx.run_job(tree)                                   # its start recomputes every line and compares
        self.assertEqual(code, 0, said)
        self.assertIsNone(cutoff_record(tree))
        self.assertFalse(any('not current' in line for line in said), said)
        self.assertEqual(len(fx.ledger_lines(tree)), 3)


class TheLedgersArithmetic(unittest.TestCase):
    """ov1_ledger.draw_line on states made by hand."""

    @staticmethod
    def state(identity: str, top, worst, top_matches: int, worst_matches: int, held: bool = False):
        """A stand-in for one variant's records at draw 1200: its two sets and its score line's matches."""
        facts = TargetFacts(status='FORECAST', reason=None, content_digest='d' * 64,
                            sets={'MAIN': {'top': tuple(top), 'worst': tuple(worst)}}, view_digest='v' * 64,
                            result_on_file=False, rerun=None, role='PROD')
        return types.SimpleNamespace(variant=types.SimpleNamespace(identity=identity), held=held, targets={1200: facts},
                                     score_contents={1200: {'matches': {'MAIN': {'top': top_matches, 'worst': worst_matches}}}})

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

    def test_a_held_member_and_a_member_without_a_line_block(self):
        held = self.state('E_901/A', range(1, 8), range(8, 15), 7, 0, held=True)
        with self.assertRaisesRegex(ov1_ledger.Blocked, 'E_901/A is held'):
            ov1_ledger.draw_line(GAME, 1200, [held], [1, 2, 3, 4, 5, 6, 7], [0] * 6)
        absent = self.state('E_901/A', range(1, 8), range(8, 15), 7, 0)
        absent.targets = {}
        with self.assertRaisesRegex(ov1_ledger.Blocked, 'E_901/A has no line for it yet'):
            ov1_ledger.draw_line(GAME, 1200, [absent], [1, 2, 3, 4, 5, 6, 7], [0] * 6)


class TheFixedTexts(WithALedger):
    """Specification 10.5 and 10.6: the words are the specification's own."""

    @staticmethod
    def quoted_after(heading: str) -> str:
        """The block quotation that follows a heading of the specification, as one line of text."""
        lines = SPECIFICATION.read_text(encoding='utf-8').splitlines()
        start = next(index for index, line in enumerate(lines) if line.startswith(heading))
        quoted = []
        for line in lines[start:]:
            if line.startswith('> '):
                quoted.append(line[2:].strip())
            elif quoted:
                break
        return ' '.join(quoted).strip('"')

    @unittest.skipUnless(SPECIFICATION.is_file(), 'the specification is kept in DEV only')
    def test_the_claim_and_the_exploratory_heading_are_the_specifications_words(self):
        self.assertEqual(reports.PREVAILING_CLAIM, self.quoted_after('**10.6 The claim'))
        text = SPECIFICATION.read_text(encoding='utf-8')
        heading = re.search(r'Every file is headed: "([^"]+)"', text.replace('\n', ' ')).group(1)
        self.assertEqual(reports.EXPLORATORY_HEADLINE, heading)
        self.assertIn(f'"{reports.NOT_STARTED_TEXT}"', text.replace('\n', ' '))

    def test_the_prevailing_report_prints_the_claim_and_the_counts_and_the_exploratory_one_its_heading(self):
        tree = self.counted_tree()
        prevailing = fx.report_text(tree, f'ov1/ov1_prevailing_{GAME}.txt')
        self.assertIn(reports.PREVAILING_CLAIM, ' '.join(prevailing.split()), 'every word, in order')
        for wanted in (f'The tree that made this report: QA at {tree}', 'Draws counted: 3',
                       'Counted forecasts made before the result was on file: 3; after: 6',
                       'Draws whose lines were written by a historical walk-forward rerun: 0',
                       'Where the counted forecasts were computed: QA 9', 'Lines with a "no pair" member: 0'):
            self.assertIn(wanted, prevailing)
        self.assertNotRegex(prevailing, 'SUPPORTED|QUALIFIED|sandbox')
        exploratory = fx.report_text(tree, f'ov1/ov1_exploratory_{GAME}.txt')
        self.assertTrue(exploratory.startswith(reports.EXPLORATORY_HEADLINE + '\n'))
        self.assertNotIn('at most 2.5%', exploratory)
        rows = [row for row in csv.reader(io.StringIO(fx.report_text(tree, f'ov1/ov1_exploratory_{GAME}.csv')))
                if row and row[0].isdigit()]
        self.assertEqual([int(row[0]) for row in rows], list(range(fx.FIRST_TOY_TARGET, 1164)),
                         'every draw that has any scored pair')


class TheDerivedCheck(WithALedger):
    """Specification 5.8 (R6-F02, R7-F01 as far as it needs no rerun)."""

    def score_file(self, tree: Path, name: str = 'TOY_A_V1') -> Path:
        """A variant's score list."""
        return tree / 'results/research' / GAME / 'variants/E_901' / name / 'scores.jsonl'

    def test_one_stored_score_altered_is_found_at_its_draw_and_nothing_is_written_from_it(self):
        tree = self.counted_tree()

        def one_more_hit(line):
            """Claim one more TOP hit than the forecast had."""
            line['content']['matches']['MAIN']['top'] += 1

        fx.alter_list_line(self.score_file(tree), 1156 - fx.FIRST_TOY_TARGET, one_more_hit)
        before = fx.files_under(tree)
        self.source(LAST_AT_START + 4, version=3)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        warned = [line for line in said if 'results not current from draw 1156' in line]
        self.assertEqual(len(warned), 2, 'said at the start and again at the end')
        self.assertTrue(warned[1].startswith('WARNING (said again)'))
        self.assertIn(f'Rerun_Walk_Forward.bat --game {GAME} --from 1156 --derived-only', warned[0])
        self.assertIn('the score of E_901/TOY_A_V1 for draw 1156', warned[0])
        self.assertEqual((cutoff_record(tree)['not_current_from_draw'], cutoff_record(tree)['reason']), (1156, 'MISMATCH'))
        after = fx.files_under(tree)
        for name in ('TOY_A_V1', 'TOY_B_V1', 'TOY_C_V1'):
            self.assertEqual(fx.list_lines(tree, 'E_901', name)[-1]['content']['target'], LAST_AT_START + 5,
                             'forecasts go on and the next draw is forecast')
            scores = f'results/research/{GAME}/variants/E_901/{name}/scores.jsonl'
            self.assertEqual(after[scores], before[scores], 'no score is written, and nothing stored is altered')
            forecasts = f'results/research/{GAME}/variants/E_901/{name}/forecasts.jsonl'
            self.assertTrue(after[forecasts].startswith(before[forecasts]))
        ledger = f'results/research/{GAME}/ov1/prevailing.jsonl'
        self.assertEqual(after[ledger], before[ledger])
        self.assertEqual(active_reports(tree, 'league')[-1], f'league_{GAME}_d01155.txt')
        self.assertEqual(active_reports(tree, 'ov1'), [f'ov1_exploratory_{GAME}.csv', f'ov1_exploratory_{GAME}.txt'])
        self.assertIn('Runs to draw: 1155', fx.report_text(tree, f'ov1/ov1_exploratory_{GAME}.txt'))
        self.assertIn('RESULTS NOT CURRENT FROM DRAW 1156 (MISMATCH)', fx.report_text(tree, f'ov1/ov1_exploratory_{GAME}.txt'))
        set_aside = tree / 'results/research' / GAME / 'reports/not_current'
        self.assertTrue((set_aside / 'league' / f'league_{GAME}_d01156.csv').is_file())
        self.assertTrue((set_aside / 'ov1' / f'ov1_prevailing_{GAME}.txt').is_file())
        self.assertEqual([name for name in active_reports(tree, 'next') if name > f'next_draw_{GAME}_d01156'], [])
        code, said = fx.run_job(tree)                                   # no job clears a mismatch
        self.assertEqual(code, 0)
        self.assertEqual(cutoff_record(tree)['not_current_from_draw'], 1156)

    def test_one_ledger_line_altered_is_found_at_its_draw(self):
        tree = self.counted_tree()

        def another_x(line):
            """Store another X than the weights give."""
            line['content']['x'] += 1

        fx.alter_list_line(ov1_ledger.ledger_path(tree, GAME), 1, another_x)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(cutoff_record(tree)['not_current_from_draw'], 1162)
        self.assertIn('the prevailing line for draw 1162 is not what the installed code computes',
                      cutoff_record(tree)['detail'])
        self.assertEqual(active_reports(tree, 'league')[-1], f'league_{GAME}_d01161.txt')

    def test_a_planted_change_to_the_scoring_code_is_found_at_the_draw_it_changes(self):
        tree = self.counted_tree()
        real = derived_check.score_content

        def changed(forecast_content, digest, outcome):
            """The scoring function with another answer from draw 1158 on."""
            content = real(forecast_content, digest, outcome)
            if content['target'] >= 1158:
                content['divisions']['top'] = 9
            return content

        with mock.patch.object(derived_check, 'score_content', changed), \
                mock.patch.object(research_job, 'score_content', changed):
            code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(cutoff_record(tree)['not_current_from_draw'], 1158)

    def test_scoring_rewritten_with_the_same_answers_quoted_digests_and_a_grown_results_file_raise_nothing(self):
        tree = self.counted_tree()
        real = derived_check.score_content

        def other_digest(line):
            """Quote another code digest and results file than the installed ones."""
            line['envelope'].update(scoring_code_digest='0' * 64, results_sha256='1' * 64, results_version=99)

        for position in range(5):
            fx.alter_list_line(self.score_file(tree), position, other_digest)
        self.source(LAST_AT_START + 5, version=3)
        with mock.patch.object(derived_check, 'score_content', lambda *a: copy.deepcopy(real(*a))):
            code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertIsNone(cutoff_record(tree))
        self.assertEqual(fx.ledger_lines(tree)[-1]['content']['draw'], LAST_AT_START + 5)

    def test_a_variant_whose_list_became_foreign_is_held_and_what_was_built_with_it_is_set_aside(self):
        tree = self.counted_tree()
        method = tree / 'src/methods/E_901/TOY_B_V1/method.py'
        method.write_text(method.read_text(encoding='ascii') + '# edited after its lists were made\n', encoding='ascii')
        fx.as_installed(tree)              # as the command that changed the software would leave the tree
        before = fx.files_under(tree)
        self.source(LAST_AT_START + 4, version=3)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        held = [line for line in said if 'a list is foreign and is ignored: E_901/TOY_B_V1' in line]
        self.assertEqual(len(held), 2, 'said at the start and again at the end')
        self.assertIn('HELD', held[0])
        self.assertIn(f'Rerun_Walk_Forward.bat --game {GAME} --only E_901/TOY_B_V1', held[0])
        self.assertEqual(cutoff_record(tree)['not_current_from_draw'], fx.FIRST_TOY_TARGET,
                         'not current from the held variant\'s first draw')
        after = fx.files_under(tree)
        for which in ('forecasts', 'scores'):
            name = f'results/research/{GAME}/variants/E_901/TOY_B_V1/{which}.jsonl'
            self.assertEqual(after[name], before[name], 'a foreign list is never appended to')
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1')[-1]['content']['target'], LAST_AT_START + 5)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores')[-1]['content']['target'], LAST_AT_START + 3)
        self.assertEqual(fx.ledger_lines(tree)[-1]['content']['draw'], LAST_AT_START + 3, 'a held member blocks')
        self.assertEqual(active_reports(tree, 'league'), [], 'no league file naming the foreign variant stays in view')
        self.assertTrue((tree / 'results/research' / GAME / 'reports/not_current/league'
                         / f'league_{GAME}_d01150.csv').is_file())

    def test_lists_made_under_other_shared_forecasting_code_are_all_foreign(self):
        tree = self.counted_tree()
        (tree / 'src/toy_forecast_code.py').write_text('# the forecasting code was corrected\n', encoding='ascii')
        fx.as_installed(tree)              # as the command that changed the software would leave the tree
        before = fx.files_under(tree, f'results/research/{GAME}/variants')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(len([line for line in said if line.startswith('WARNING: ') and 'HELD' in line
                              and 'other shared forecasting code' in line]), 3)
        self.assertEqual(fx.files_under(tree, f'results/research/{GAME}/variants'), before)

    def test_the_list_of_a_variant_no_longer_installed_is_named_and_counts_nowhere(self):
        tree = self.counted_tree()
        shutil.rmtree(tree / 'src/methods/E_901/TOY_C_V1')
        fx.as_installed(tree)              # as the command that changed the software would leave the tree
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('a list is foreign and is ignored: E_901/TOY_C_V1 (the variant is not installed here)' in line
                            for line in said), said)
        self.assertEqual(cutoff_record(tree)['not_current_from_draw'], 1161,
                         'the ledger was built with it in the cohort: not current from the first such line')
        league = fx.report_text(tree, f'league/league_{GAME}_d01160.txt')
        self.assertNotIn('TOY_C_V1  ', league.split('\n\n', 1)[1])
        self.assertIn('Foreign lists ignored: E_901/TOY_C_V1 (not installed here)', league)

    def test_a_marker_that_cannot_be_read_refuses_the_game(self):
        tree = self.counted_tree()
        derived_check.cutoff_path(tree, GAME).write_text('{"not_current_from_draw": "soon"}', encoding='ascii')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 1)
        self.assertTrue(any('REFUSED' in line and 'NOT_CURRENT_FROM.json' in line for line in said), said)


class CatchUpAfterAStoppedRerun(fx.JobCase):
    """Specification 5.8, the reason AWAITING_CATCH_UP (R7-F01): the ordinary job's half."""

    def stopped_at_1160(self, name: str = 'tree', marker: bool = True) -> Path:
        """A tree as a rerun stopped at draw 1160 leaves it: everything right through 1160, results on file
        through 1164, and the marker saying the rest is awaited."""
        tree = self.tree(with_source=False, name=name)
        for variant in ('TOY_A_V1', 'TOY_B_V1'):
            write_status(fx.status_path(tree, 'E_901', variant), 'E_901', variant,
                         {GAME: GameStatus(eligible_from=1150, eligibility_recorded='planted for the test')})
        self.assertEqual(fx.run_job(tree, no_update=True)[0], 0)
        fx.write_results(tree, GAME, LAST_AT_START + 4, version=2)
        if marker:
            derived_check.write_cutoff(tree, GAME, LAST_AT_START + 1, derived_check.AWAITING_CATCH_UP, 'a rerun --to 1160')
        return tree

    def test_the_job_catches_up_as_for_new_draws_and_removes_the_marker_only_after_a_clean_full_check(self):
        tree = self.stopped_at_1160()
        twin = self.stopped_at_1160(name='twin', marker=False)
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('catches up from draw 1161' in line for line in said), said)
        self.assertTrue(any('the full check found nothing: the derived results are current again' in line for line in said))
        self.assertIsNone(cutoff_record(tree))
        fx.run_job(twin, no_update=True)
        self.assertEqual([line['content'] for line in fx.ledger_lines(tree)], [line['content'] for line in fx.ledger_lines(twin)])
        self.assertEqual(fx.ledger_lines(tree)[-1]['content']['draw'], LAST_AT_START + 4)
        self.assertEqual(active_reports(tree, 'league'), active_reports(twin, 'league'))

    def test_the_marker_stays_while_a_draw_is_still_to_do(self):
        tree = self.stopped_at_1160()
        code, said = fx.run_job(tree, no_update=True, only=['E_901/TOY_A_V1'])
        self.assertEqual(code, 0, said)
        self.assertEqual(cutoff_record(tree)['reason'], 'AWAITING_CATCH_UP')

    def test_a_catch_up_never_clears_a_real_mismatch(self):
        tree = self.stopped_at_1160()
        derived_check.write_cutoff(tree, GAME, 1158, derived_check.AWAITING_CATCH_UP, 'a rerun --to 1157')

        def one_more_hit(line):
            """Claim one more TOP hit than the forecast had."""
            line['content']['matches']['MAIN']['top'] += 1

        scores = tree / 'results/research' / GAME / 'variants/E_901/TOY_A_V1/scores.jsonl'
        fx.alter_list_line(scores, 1159 - fx.FIRST_TOY_TARGET, one_more_hit)
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        self.assertEqual((cutoff_record(tree)['not_current_from_draw'], cutoff_record(tree)['reason']), (1159, 'MISMATCH'))
        self.assertTrue(any('results not current from draw 1159' in line for line in said), said)
        self.assertEqual(active_reports(tree, 'league')[-1], f'league_{GAME}_d01158.txt')

    def test_with_a_held_variant_the_marker_becomes_a_mismatch_and_the_hold_is_not_cleared(self):
        tree = self.stopped_at_1160()
        method = tree / 'src/methods/E_901/TOY_B_V1/method.py'
        method.write_text(method.read_text(encoding='ascii') + '# edited\n', encoding='ascii')
        fx.as_installed(tree)              # as the command that changed the software would leave the tree
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        self.assertEqual((cutoff_record(tree)['not_current_from_draw'], cutoff_record(tree)['reason']),
                         (fx.FIRST_TOY_TARGET, 'MISMATCH'))
        self.assertTrue(any('HELD' in line for line in said))


class Withdrawal(fx.JobCase):
    """Specification 11 (F02, R5-F01, R6-F07)."""

    def withdraw(self, tree: Path, names=(('E_901', 'TOY_B_V1'),), games=(GAME,), reason: str = 'the table was built from the wrong column',
                 answer='WITHDRAW') -> tuple:
        """Run the withdrawal with a typed answer (or a function that gives one). Returns (exit code, lines said)."""
        said = []
        ask = answer if callable(answer) else (lambda question: answer)
        code = withdraw.withdraw(tree, list(names), games, reason, ask=ask, say=said.append, now=lambda: fx.FIXED_TIME)
        return code, said

    def counting_tree(self, role: str = 'QA', name: str = 'tree') -> Path:
        """A tree of the given role whose two variants count from draw 1150 (as status files that came with
        installed software say), worked through 1160 with draw 1161 forecast and pending."""
        tree = self.tree(role=role, with_source=False, name=name)
        for variant in ('TOY_A_V1', 'TOY_B_V1'):
            write_status(fx.status_path(tree, 'E_901', variant), 'E_901', variant,
                         {GAME: GameStatus(eligible_from=1150, eligibility_recorded='planted for the test')})
        self.assertEqual(fx.run_job(tree, no_update=True)[0], 0)
        return tree

    def test_the_planted_late_result_is_never_scored_in_every_kind_of_tree_alike(self):
        contents = {}
        for role in ('PROD', 'QA', 'DEV'):
            with self.subTest(role=role):
                tree = self.counting_tree(role, name=f'tree_{role}')
                self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1')[-1]['content']['target'], 1161)
                before = fx.files_under(tree)
                code, said = self.withdraw(tree)
                self.assertEqual(code, withdraw.EXIT_DONE, said)
                self.assertTrue(any('last draw on file 1160' in line and 'takes effect from draw 1161' in line for line in said))
                fx.write_results(tree, GAME, 1161, version=2)           # the result of 1161 is then accepted
                code, said = fx.run_job(tree, no_update=True)
                self.assertEqual(code, 0, said)
                after = fx.files_under(tree)
                for which in ('forecasts', 'scores'):
                    name = f'results/research/{GAME}/variants/E_901/TOY_B_V1/{which}.jsonl'
                    self.assertEqual(after[name], before[name], 'no score for 1161, no line for 1162, earlier lines byte-identical')
                self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores')[-1]['content']['target'], 1161)
                ledger = fx.ledger_lines(tree)
                self.assertEqual(ledger[-1]['content']['cohort'], [{'variant': 'E_901/TOY_A_V1', 'state': 'counted'}])
                self.assertEqual(len(ledger[-2]['content']['cohort']), 2, 'the lines already written stay as they were')
                self.assertTrue(after[f'results/research/{GAME}/ov1/prevailing.jsonl'].startswith(
                    before[f'results/research/{GAME}/ov1/prevailing.jsonl']))
                rows = list(csv.reader(io.StringIO(fx.report_text(tree, f'league/league_{GAME}_d01161.csv'))))
                header = next(row for row in rows if row and row[0] == 'order_top')
                row = dict(zip(header, next(row for row in rows if len(row) > 1 and row[1] == 'E_901/TOY_B_V1')))
                self.assertEqual(row['draws_scored'], str(1160 - fx.FIRST_TOY_TARGET + 1), 'no league scoring at 1161')
                self.assertEqual(row['note'], 'WITHDRAWN from draw 1161: the table was built from the wrong column '
                                              '(its forecast for draw 1161: not scored: withdrawn)')
                exploratory = [row for row in csv.reader(io.StringIO(fx.report_text(tree, f'ov1/ov1_exploratory_{GAME}.csv')))
                               if row and row[0] == '1161']
                self.assertEqual(exploratory[0][1], '1', 'no contribution to the exploratory score at 1161')
                contents[role] = ([line['content'] for line in ledger],
                                  [line['content'] for line in fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores')])
        self.assertEqual(contents['QA'], contents['PROD'])
        self.assertEqual(contents['DEV'], contents['PROD'])

    def test_the_same_in_a_catch_up_of_six_draws(self):
        tree = self.counting_tree()
        self.withdraw(tree)
        fx.write_results(tree, GAME, 1166, version=2)
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1')[-1]['content']['target'], 1161)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1', 'scores')[-1]['content']['target'], 1160)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores')[-1]['content']['target'], 1166)
        for line in fx.ledger_lines(tree)[-6:]:
            self.assertEqual([member['variant'] for member in line['content']['cohort']], ['E_901/TOY_A_V1'])
        self.assertIn('WITHDRAWN from draw 1161', fx.report_text(tree, f'next/next_draw_{GAME}_d01167.txt'))

    def test_a_withdrawal_changes_the_status_file_and_no_scientific_byte(self):
        tree = self.counting_tree()
        before = fx.files_under(tree)
        fingerprint = read_variant(tree / 'src/methods', 'E_901', 'TOY_B_V1').fingerprint
        other_status = fx.status_path(tree, 'E_901', 'TOY_A_V1').read_bytes()
        code, said = self.withdraw(tree)
        self.assertEqual(code, withdraw.EXIT_DONE, said)
        self.assertEqual(fx.files_under(tree), before)
        self.assertEqual(read_variant(tree / 'src/methods', 'E_901', 'TOY_B_V1').fingerprint, fingerprint)
        self.assertEqual(fx.status_path(tree, 'E_901', 'TOY_A_V1').read_bytes(), other_status)
        status = self.status(tree, 'TOY_B_V1')
        self.assertEqual((status.withdrawn_from, status.withdrawn_reason, status.eligible_from),
                         (1161, 'the table was built from the wrong column', 1150))
        self.assertIn('results on file through 1160', status.withdrawn_recorded)
        text = fx.status_path(tree, 'E_901', 'TOY_B_V1').read_text(encoding='ascii')
        self.assertIn('status = WITHDRAWN\nwithdrawn_from_draw = 1161\n', text)
        log = [json.loads(line) for line in (tree / 'records' / withdraw.TREE_LOG_NAME).read_text(encoding='ascii').splitlines()]
        self.assertEqual(len(log), 1)
        self.assertEqual((log[0]['operation'], log[0]['variants']),
                         ('WITHDRAWAL', [{'variant': 'E_901/TOY_B_V1', 'withdrawn_from_draw': {GAME: 1161}}]))

    def test_several_variants_are_withdrawn_under_one_confirmation(self):
        tree = self.counting_tree()
        asked = []
        code, said = self.withdraw(tree, names=(('E_901', 'TOY_A_V1'), ('E_901', 'TOY_B_V1')),
                                   answer=lambda question: asked.append(question) or 'WITHDRAW')
        self.assertEqual((code, len(asked)), (withdraw.EXIT_DONE, 1))
        self.assertEqual((self.status(tree, 'TOY_A_V1').withdrawn_from, self.status(tree, 'TOY_B_V1').withdrawn_from), (1161, 1161))

    def test_without_the_typed_word_or_when_refused_nothing_is_written(self):
        tree = self.counting_tree()
        status_file = fx.status_path(tree, 'E_901', 'TOY_B_V1')
        before = status_file.read_bytes()
        asked = []
        cases = (({'answer': 'yes'}, 'not confirmed'), ({'reason': '  '}, '--reason is empty'),
                 ({'reason': 'wrong \u2013 see notes', 'answer': lambda question: asked.append(question) or 'WITHDRAW'},
                  'must be one line of plain printable text'),
                 ({'names': (('E_901', 'NO_SUCH_V1'),)}, 'REFUSED'), ({'games': ('OZLOTTO',)}, 'REFUSED'))
        for arguments, wanted in cases:
            with self.subTest(arguments=arguments):
                code, said = self.withdraw(tree, **arguments)
                self.assertEqual(code, withdraw.EXIT_NOTHING_WRITTEN, said)
                self.assertTrue(any(wanted in line for line in said), said)
                self.assertEqual(status_file.read_bytes(), before)
                self.assertFalse((tree / 'records' / withdraw.TREE_LOG_NAME).exists())
        self.assertEqual(asked, [], 'a reason that cannot be written is refused before the owner is asked anything')

    def test_it_is_one_way_a_second_withdrawal_refuses_and_no_command_reinstates(self):
        tree = self.counting_tree()
        self.withdraw(tree)
        before = fx.status_path(tree, 'E_901', 'TOY_B_V1').read_bytes()
        code, said = self.withdraw(tree, reason='another reason')
        self.assertEqual(code, withdraw.EXIT_NOTHING_WRITTEN)
        self.assertTrue(any('already withdrawn in POWERBALL, from draw 1161' in line for line in said), said)
        self.assertEqual(fx.status_path(tree, 'E_901', 'TOY_B_V1').read_bytes(), before)
        offered = [name for name in dir(withdraw) + dir(research_job) if re.search('reinstat|unwithdraw|reactivat', name, re.I)]
        self.assertEqual(offered, [])

    def test_from_before_the_draw_is_shown_until_the_file_is_written_both_locks_are_held(self):
        tree = self.tree()
        fx.run_job(tree)
        self.source(LAST_IN_SOURCE, version=2)
        seen = {}

        def while_the_owner_decides(question):
            """What a job and a results step find while the confirmation is awaited."""
            seen['job lock'] = (tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME).is_file()
            seen['updater lock'] = (tree / job_lock.UPDATER_LOCK).is_file()
            seen['job'] = fx.run_job(tree)
            try:
                results_step.copy_results(read_settings(tree), GAME, 'now')
            except job_lock.LaunchRefused as refusal:
                seen['results step'] = str(refusal)
            return 'WITHDRAW'

        code, said = self.withdraw(tree, answer=while_the_owner_decides)
        self.assertEqual(code, withdraw.EXIT_DONE, said)
        self.assertTrue(seen['job lock'] and seen['updater lock'])
        self.assertEqual(seen['job'][0], research_job.EXIT_REFUSED)
        self.assertTrue(any('a process of this tree is running' in line for line in seen['job'][1]))
        self.assertIn('.results_master.lock exists', seen['results step'])
        self.assertEqual(self.status(tree, 'TOY_B_V1').withdrawn_from, LAST_AT_START + 1,
                         'the draw shown is the draw written: nothing could move the results in between')
        self.assertFalse((tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME).exists())
        self.assertFalse((tree / job_lock.UPDATER_LOCK).exists())

    def test_a_withdrawal_refuses_while_a_job_holds_the_tree(self):
        tree = self.counting_tree()
        lock = tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME
        lock.write_text('research job\n', encoding='ascii')
        before = fx.status_path(tree, 'E_901', 'TOY_B_V1').read_bytes()
        code, said = self.withdraw(tree)
        self.assertEqual(code, withdraw.EXIT_NOTHING_WRITTEN)
        self.assertTrue(any('a process of this tree is running' in line for line in said), said)
        self.assertEqual(fx.status_path(tree, 'E_901', 'TOY_B_V1').read_bytes(), before)

    def test_a_restore_to_before_the_withdrawal_runs_the_variant_again(self):
        tree = self.counting_tree()
        backup = self.root / 'backup'
        shutil.copytree(tree / 'results', backup / 'results')
        saved_status = fx.status_path(tree, 'E_901', 'TOY_B_V1').read_bytes()
        self.withdraw(tree)
        fx.write_results(tree, GAME, 1161, version=2)
        fx.run_job(tree, no_update=True)
        shutil.rmtree(tree / 'results')                                 # the restore: the backup's lists and status
        shutil.copytree(backup / 'results', tree / 'results')
        fx.status_path(tree, 'E_901', 'TOY_B_V1').write_bytes(saved_status)
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1', 'scores')[-1]['content']['target'], 1161)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1')[-1]['content']['target'], 1162)
        self.assertEqual(len(fx.ledger_lines(tree)[-1]['content']['cohort']), 2)
        self.assertIsNone(cutoff_record(tree))

    def test_a_status_file_taken_from_a_backup_is_accepted(self):
        tree = self.counting_tree()
        path = fx.status_path(tree, 'E_901', 'TOY_B_V1')
        saved = path.read_bytes()
        path.write_bytes(saved.replace(b'1150', b'1140'))
        self.assertEqual(fx.run_job(tree, no_update=True)[0], 1)
        path.write_bytes(saved)
        self.assertEqual(fx.run_job(tree, no_update=True)[0], 0)

    def test_the_command_line_takes_each_variant_as_two_words(self):
        tree = self.counting_tree()
        with mock.patch.object(withdraw, 'withdraw', return_value=0) as called:
            withdraw.main(['E_901', 'TOY_A_V1', 'E_901', 'TOY_B_V1', '--game', 'BOTH', '--reason', 'wrong'], tree)
        self.assertEqual(called.call_args[0], (tree, [('E_901', 'TOY_A_V1'), ('E_901', 'TOY_B_V1')],
                                               ('POWERBALL', 'OZLOTTO'), 'wrong'))
        with self.assertRaises(SystemExit), mock.patch('sys.stderr', io.StringIO()):
            withdraw.main(['E_901', '--game', GAME, '--reason', 'wrong'], tree)


if __name__ == '__main__':
    unittest.main()
