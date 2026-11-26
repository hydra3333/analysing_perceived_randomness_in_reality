"""Tests of deploy/compare_with_frozen.py: that "SAME" means the same, by planting one difference of each kind.

The comparison itself is made on the real methods by the tool's own commands; here two invented trees are made
with this tree's engine, which the tool must find the same, and then one thing at a time is changed in one of them.
(The simple scheme v0.2 section 9.)
"""
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

    def test_comments_and_docstrings_are_left_out_and_any_other_change_is_seen(self):
        first = b'"""About."""\nimport os\n\n\ndef f(a):\n    """Old words."""\n    return a + 1  # one more\n'
        second = b'"""About, reworded."""\nimport os\n\n\ndef f(a):\n    """New words."""\n    return a + 1\n'
        third = second.replace(b'a + 1', b'a + 2')
        self.assertEqual(compare.without_comments(first), compare.without_comments(second))
        self.assertNotEqual(compare.without_comments(second), compare.without_comments(third))
        self.assertNotEqual(compare.without_comments(b'X = "text"\n'), compare.without_comments(b'X = "other"\n'))


if __name__ == '__main__':
    unittest.main()
