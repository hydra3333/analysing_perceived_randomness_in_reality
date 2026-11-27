"""Tests of deploy/compare_with_frozen.py: that "SAME" means the same, by planting one difference of each kind.

The comparison itself is made on the real methods by the tool's own commands; here two invented trees are made
with this tree's engine, which the tool must find the same, and then one thing at a time is changed in one of them.
(The simple scheme v0.2 section 9.)
"""
import ast
import shutil
import sys
import unittest
from pathlib import Path

TREE_OF_THIS_FILE = Path(__file__).resolve().parents[1]
if str(TREE_OF_THIS_FILE / 'deploy') not in sys.path:
    sys.path.insert(0, str(TREE_OF_THIS_FILE / 'deploy'))

import compare_with_frozen as compare                       # noqa: E402  (after the path line above)
import research_fixtures as fx                              # noqa: E402

GAME = fx.GAME


class TwoTreesCompared(fx.JobCase):
    """compare_trees on two trees that hold the same science, and on one planted difference at a time."""

    def setUp(self):
        """Two trees with the same invented results and toy methods, each worked twice so that the second OV-1
        series has lines; and the other game's results, so that both games are compared."""
        super().setUp()
        self.trees = []
        for name in ('first_DEV', 'second_DEV'):
            tree = self.tree(variants=(), name=name)
            self.add_variant(tree, 'TOY_A_V1', games=('POWERBALL', 'OZLOTTO'))
            self.add_variant(tree, 'TOY_B_V1', {'reverse': True, 'fail_at': [1155]}, games=('POWERBALL', 'OZLOTTO'))
            fx.write_results(tree, 'OZLOTTO', 1482)
            self.assertEqual(fx.run_job(tree, games=compare.GAMES)[0], 0)
            fx.write_results(tree, GAME, fx.LAST_AFTER_NEW, version=2)
            self.assertEqual(fx.run_job(tree, games=compare.GAMES)[0], 0)
            self.trees.append(tree)

    def compared(self) -> tuple:
        """(whether the two trees came out the same, the lines that say DIFFERENT)."""
        said = []
        same = compare.compare_trees(*self.trees, say=said.append)
        self.assertEqual(said[-1].startswith('RESULT: SAME'), same)
        return same, [line for line in said if line.startswith('DIFFERENT')]

    def test_two_trees_with_the_same_science_are_the_same_whatever_their_paths_and_times(self):
        same, different = self.compared()
        self.assertTrue(same, different)

    def test_the_frozen_reports_are_given_exactly_the_declared_new_wording_and_no_other_change_is_forgiven(self):
        new_reports = compare.report_files(self.trees[1], GAME)
        frozen_reports, made = compare.frozen_report_files(self.trees[1], GAME)
        self.assertEqual((frozen_reports, made), (new_reports, 0), 'the new wording is left as it is')
        league = self.trees[0] / 'results/research' / GAME / f'reports/league/league_{GAME}_d01160.txt'
        text = league.read_bytes()
        old = text.replace(b'Methods: ', b'Variants: ').replace(b'  method  ', b'  variant ')
        self.assertNotEqual(old, text)
        league.write_bytes(old)
        same, different = self.compared()
        self.assertTrue(same, 'the frozen engine\'s words are given the new ones')
        league.write_bytes(old.replace(b'Variants: ', b'Entries: '))
        same, different = self.compared()
        self.assertEqual(len(different), 1, 'a wording that is not on the declared list is not forgiven')
        self.assertIn('every report file', different[0])
        self.assertIn(f'league/league_{GAME}_d01160.txt', different[0])

    def test_each_planted_difference_is_found_and_named(self):
        research = self.trees[1] / 'results/research' / GAME
        pristine = self.root / 'pristine'
        shutil.copytree(research, pristine)

        def change_top(record):
            """Swap two numbers between a forecast's TOP and WORST sets."""
            main = record['content']['barrels']['MAIN']
            main['top'][0], main['worst'][0] = main['worst'][0], main['top'][0]

        def change_matches(record):
            """Give a score one more TOP hit."""
            record['content']['matches']['MAIN']['top'] += 1

        def change_x(record):
            """Change one OV-1 line's X."""
            record['content']['x'] += 1

        def change_made_before(record):
            """Say that a forecast was made after its result was on file."""
            record['envelope']['target_result_on_file'] = not record['envelope']['target_result_on_file']

        plants = (
            ('variants/E_901/TOY_A_V1/forecasts.jsonl', change_top, 'every forecast and every score'),
            ('variants/E_901/TOY_A_V1/forecasts.jsonl', change_made_before, 'every forecast and every score'),
            ('variants/E_901/TOY_B_V1/scores.jsonl', change_matches, 'every forecast and every score'),
            ('ov1/prevailing.jsonl', change_x, 'the second OV-1 series'),
            ('ov1/exploratory.jsonl', change_x, 'the OV-1 series over all draws'),
        )
        for name, change, wanted in plants:
            fx.alter_list_line(research / name, 2, change)
            same, different = self.compared()
            self.assertFalse(same, name)
            self.assertEqual(len(different), 1, different)
            self.assertIn(f'{GAME}: {wanted}', different[0])
            shutil.rmtree(research)
            shutil.copytree(pristine, research)
        for name, wanted in ((f'reports/ov1/ov1_exploratory_{GAME}.csv', 'every report file'),
                             (f'reports/league/league_{GAME}_d01160.txt', 'every report file')):
            path = research / name
            path.write_bytes(path.read_bytes().replace(b'1', b'2', 1))
            same, different = self.compared()
            self.assertFalse(same, name)
            self.assertIn(f'{GAME}: {wanted}', different[0])
            self.assertIn(name.split('/', 1)[1], different[0])
            shutil.rmtree(research)
            shutil.copytree(pristine, research)
        shutil.rmtree(research / 'variants/E_901/TOY_B_V1')
        same, different = self.compared()
        self.assertIn(f'{GAME}: the methods that have results', different[0])
        (research / f'reports/next/next_draw_{GAME}_d01167.txt').unlink()
        same, different = self.compared()
        self.assertTrue(any('the names of the report files' in line for line in different), different)


class TheCodeCompared(unittest.TestCase):
    """without_comments: a file that differs only in comments and docstrings is the same program."""

    def test_each_declared_change_turns_the_frozen_text_into_the_new_and_keeps_a_tables_columns(self):
        for frozen, new in compare.WORDING_CHANGES:
            data, made = compare.with_new_wording(frozen.encode('ascii'))
            self.assertEqual((data, made), (new.encode('ascii'), 1), frozen[:60])
        columns = [(frozen, new) for frozen, new in compare.WORDING_CHANGES if frozen.endswith('variant ')]
        self.assertEqual(len(columns), 2)
        for frozen, new in columns:
            self.assertEqual(len(frozen), len(new), 'a column name keeps its padded width')
        row = b'\r\nvariant                  line\r\nE_002/RECUR_MEAN_ALL_V1  FORECAST'
        self.assertEqual(compare.with_new_wording(row)[0],
                         b'\r\nmethod                   line\r\nE_002/RECUR_MEAN_ALL_V1  FORECAST')

    def test_the_declared_wording_is_that_of_the_two_engines(self):
        frozen_source = TREE_OF_THIS_FILE.parent / 'src/research/reports.py'
        if not frozen_source.is_file():
            self.skipTest('the frozen engine is not beside this tree')
        frozen_module = ast.parse(frozen_source.read_text(encoding='utf-8'))
        new_module = ast.parse((TREE_OF_THIS_FILE / 'src/research/reports.py').read_text(encoding='utf-8'))

        def constant(module, name):
            """The value of a module's top-level text constant."""
            for node in module.body:
                if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', None) == name:
                    return ast.literal_eval(node.value)
            raise AssertionError(name)

        NOT_STARTED = next(pair for pair in compare.WORDING_CHANGES if pair[0].startswith('prevailing OV-1: not'))
        for module, claim, not_started in ((frozen_module, compare.FROZEN_CLAIM, NOT_STARTED[0]),
                                           (new_module, compare.NEW_CLAIM, NOT_STARTED[1])):
            self.assertEqual(constant(module, 'PREVAILING_CLAIM'), claim)
            self.assertEqual(constant(module, 'NOT_STARTED_TEXT'), not_started)
            self.assertEqual(constant(module, 'CLAIM_LINE_WIDTH'), compare.CLAIM_WIDTH)

    def test_comments_and_docstrings_are_left_out_and_any_other_change_is_seen(self):
        first = b'"""About."""\nimport os\n\n\ndef f(a):\n    """Old words."""\n    return a + 1  # one more\n'
        second = b'"""About, reworded."""\nimport os\n\n\ndef f(a):\n    """New words."""\n    return a + 1\n'
        third = second.replace(b'a + 1', b'a + 2')
        self.assertEqual(compare.without_comments(first), compare.without_comments(second))
        self.assertNotEqual(compare.without_comments(second), compare.without_comments(third))
        self.assertNotEqual(compare.without_comments(b'X = "text"\n'), compare.without_comments(b'X = "other"\n'))


if __name__ == '__main__':
    unittest.main()
