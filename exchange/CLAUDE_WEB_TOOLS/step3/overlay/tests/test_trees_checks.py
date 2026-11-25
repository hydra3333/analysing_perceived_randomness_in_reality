"""Tests of the checks that travel with the installed software (build step 3, slice C, part C1).

What this file is for
    It shows that research/tree_checks.py does what specification v0.6 section 12.3 items 2, 4 and 5 ask: a
    smoke case passes only on a complete forecast, reads no real draw and writes only under the tree's scratch
    folder; the fixed sample of stored forecasts is computed again and a difference is named; every stored score
    and prevailing line is compared and the first difference is named; and none of the three changes the tree.
    Every tree here is invented and lies in a temporary folder.

Which of the project's own modules it uses
    research.tree_checks, research.derived_check, research.ov1_ledger, research.settings, and the fixtures.
"""
from __future__ import annotations

import hashlib
import shutil
import unittest
from pathlib import Path
from unittest import mock

import research_fixtures as fx
from research import derived_check, ov1_ledger, tree_checks
from research.settings import read_settings
from research.status_file import StatusRefused

GAME = fx.GAME
FAMILY = 'E_901'
# How many draws arrive after a worked tree's first job (its prevailing ledger begins with them).
ARRIVED = 3


def whole_tree(tree: Path) -> dict:
    """Every file of a tree with the SHA-256 of its bytes, Python's own cache files left out."""
    return {path.relative_to(tree).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(tree.rglob('*')) if path.is_file() and '__pycache__' not in path.parts}


class ChecksCase(fx.JobCase):
    """An invented QA tree, with what the checks need at hand."""

    def software(self, tree: Path) -> tree_checks.Software:
        """The software of a tree, read as the checks read it."""
        return tree_checks.read_software(tree)

    def smoke(self, tree: Path, name: str = 'TOY_A_V1', only=None) -> tuple:
        """Run the tree's smoke cases; return (the failures, the lines said)."""
        said = []
        with fx.ImportPath(tree):
            software = self.software(tree)
            failures = tree_checks.smoke_cases(software, tree, only=only, say=said.append)
        return failures, said

    def worked_tree(self, **options) -> Path:
        """A tree whose research job has run, and run again after three more draws arrived, so that it holds
        forecasts, scores and a prevailing ledger."""
        tree = self.tree(**options)
        self.assertEqual(fx.run_job(tree)[0], 0)
        self.source(fx.LAST_AT_START + ARRIVED, version=2)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        return tree

    def stored(self, tree: Path, software_root: Path | None = None) -> tuple:
        """(the software, the stored records) of a tree; the software read from another folder if one is named."""
        software = self.software(software_root or tree)
        return software, tree_checks.read_stored(software, read_settings(tree), say=lambda line: None)


class TheSmokeCase(ChecksCase):
    """Specification 12.3 item 2: each variant is made to forecast once, on an invented table."""

    def test_a_variant_that_forecasts_passes_and_leaves_nothing_behind(self):
        tree = self.tree()
        before = whole_tree(tree)
        failures, said = self.smoke(tree)
        self.assertEqual(failures, [])
        self.assertEqual(said, [f'  smoke case: {FAMILY}/TOY_A_V1 for {GAME}: a complete forecast',
                                f'  smoke case: {FAMILY}/TOY_B_V1 for {GAME}: a complete forecast'])
        self.assertEqual(whole_tree(tree), before)
        self.assertEqual(list((tree / tree_checks.SCRATCH_FOLDER).iterdir()), [])

    def test_it_reads_no_results_file_of_the_tree(self):
        tree = self.tree()
        shutil.rmtree(tree / 'source_data')
        failures, _ = self.smoke(tree)
        self.assertEqual(failures, [])

    def test_the_invented_table_is_the_same_every_time_and_ends_at_the_first_draw_the_variant_can_forecast(self):
        first = tree_checks.invented_results(GAME, fx.FIRST_TOY_TARGET)
        again = tree_checks.invented_results(GAME, fx.FIRST_TOY_TARGET)
        self.assertEqual(first.raw, again.raw)
        self.assertEqual((first.first_draw, first.last_draw), (1144, fx.FIRST_TOY_TARGET))
        self.assertEqual(len(first.raw.splitlines()), 1 + fx.FIRST_TOY_TARGET - 1144 + 1)
        self.assertNotEqual(first.raw, fx.results_bytes(GAME, fx.FIRST_TOY_TARGET), 'not the tests\' own table')
        other_game = tree_checks.invented_results('OZLOTTO', 1480)
        self.assertEqual(len(other_game.raw.splitlines()[1].split(b',')), 2 + 7 + 3)

    def failing(self, behaviour: dict, *words) -> tuple:
        """A tree with one variant that behaves as planted; its smoke case must fail. Returns (tree, line)."""
        tree = self.tree(variants=(('TOY_A_V1', behaviour),))
        before = whole_tree(tree)
        failures, said = self.smoke(tree)
        self.assertEqual(len(failures), 1, said)
        self.assertEqual(said, [f'  smoke case: {FAMILY}/TOY_A_V1 for {GAME}: FAILED'])
        for word in words:
            self.assertIn(word, failures[0])
        folder = tree / tree_checks.SCRATCH_FOLDER / f'SMOKE_{FAMILY}_TOY_A_V1_{GAME}'
        self.assertIn(str(folder), failures[0], 'the folder left behind is named')
        self.assertEqual(sorted(entry.name for entry in folder.iterdir()),
                         sorted([tree_checks.SMOKE_TABLE_NAME, tree_checks.SMOKE_NOTE_NAME]))
        self.assertEqual((folder / tree_checks.SMOKE_TABLE_NAME).read_bytes(),
                         tree_checks.invented_results(GAME, fx.FIRST_TOY_TARGET).raw)
        note = (folder / tree_checks.SMOKE_NOTE_NAME).read_bytes()
        self.assertEqual(note.count(b'\n'), note.count(b'\r\n'), 'the note is a Windows text file')
        after = {name: digest for name, digest in whole_tree(tree).items()
                 if not name.startswith(tree_checks.SCRATCH_FOLDER + '/')}
        self.assertEqual(after, before, 'nothing outside the scratch folder was written')
        return tree, failures[0]

    def test_insufficient_history_at_the_declared_minimum_fails(self):
        self.failing({'short_below': 5}, 'NO_FORECAST', 'INSUFFICIENT_HISTORY')

    def test_a_method_failure_fails_and_its_reason_is_kept(self):
        self.failing({'fail_at': [fx.FIRST_TOY_TARGET]}, 'METHOD_FAILED', 'no fit can be made')

    def test_an_output_the_readout_refuses_fails(self):
        self.failing({'bad_output_at': [fx.FIRST_TOY_TARGET]}, 'METHOD_FAILED')

    def test_an_error_inside_the_method_fails_and_its_trace_is_in_the_note(self):
        tree, line = self.failing({'crash_at': [fx.FIRST_TOY_TARGET]}, 'RuntimeError', 'an environmental fault')
        note = (tree / tree_checks.SCRATCH_FOLDER / f'SMOKE_{FAMILY}_TOY_A_V1_{GAME}'
                / tree_checks.SMOKE_NOTE_NAME).read_text(encoding='utf-8')
        self.assertIn('Traceback', note)

    def test_a_method_that_can_no_longer_be_imported_fails(self):
        tree = self.tree(variants=('TOY_A_V1',))
        method = tree / 'src' / 'methods' / FAMILY / 'TOY_A_V1' / 'method.py'
        method.write_text('import a_package_this_environment_does_not_have\n' + method.read_text(encoding='ascii'),
                          encoding='ascii')
        failures, _ = self.smoke(tree)
        self.assertEqual(len(failures), 1)
        self.assertIn('ModuleNotFoundError', failures[0])

    def test_a_forecast_that_lacks_a_barrel_of_the_game_is_not_complete(self):
        tree = self.tree(variants=('TOY_A_V1',))
        real = tree_checks.compute_target

        def without_the_second_barrel(*arguments):
            """The engine's answer with the POWERBALL barrel taken out."""
            content, detail = real(*arguments)
            content['barrels'].pop('POWERBALL')
            return content, detail

        with mock.patch.object(tree_checks, 'compute_target', without_the_second_barrel):
            failures, _ = self.smoke(tree)
        self.assertEqual(len(failures), 1)
        self.assertIn('not for every barrel of the game', failures[0])

    def test_the_folder_of_an_earlier_failure_is_gone_once_the_smoke_case_passes(self):
        tree = self.tree(variants=('TOY_A_V1',))
        folder = tree / tree_checks.SCRATCH_FOLDER / f'SMOKE_{FAMILY}_TOY_A_V1_{GAME}'
        folder.mkdir(parents=True)
        (folder / tree_checks.SMOKE_NOTE_NAME).write_bytes(b'an earlier failure\r\n')
        failures, _ = self.smoke(tree)
        self.assertEqual(failures, [])
        self.assertFalse(folder.exists())

    def test_only_the_variants_named_are_tried(self):
        tree = self.tree(variants=(('TOY_A_V1', {'crash_at': [fx.FIRST_TOY_TARGET]}), 'TOY_B_V1'))
        failures, said = self.smoke(tree, only={f'{FAMILY}/TOY_B_V1'})
        self.assertEqual(failures, [])
        self.assertEqual(len(said), 1)

    def test_a_variant_is_tried_for_each_game_it_supports(self):
        tree = self.tree(variants=())
        self.add_variant(tree, 'TOY_TWO_V1', games=('POWERBALL', 'OZLOTTO'))
        failures, said = self.smoke(tree)
        self.assertEqual(failures, [])
        self.assertEqual([line.split(' for ')[1].split(':')[0] for line in said], ['POWERBALL', 'OZLOTTO'])

    def test_a_scratch_folder_that_is_a_link_is_refused_and_nothing_is_written_through_it(self):
        tree = self.tree(variants=('TOY_A_V1',))
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        kind = fx.make_folder_link(tree / tree_checks.SCRATCH_FOLDER, elsewhere)
        if kind is None:
            self.skipTest('this machine lets the test make neither a symbolic link nor a junction')
        with self.assertRaises(tree_checks.ChecksRefused) as refused:
            self.smoke(tree)
        self.assertIn('ordinary folder', str(refused.exception))
        self.assertEqual(list(elsewhere.iterdir()), [])


class TheSoftwareIsReadAndNothingIsMade(ChecksCase):
    """The checks read the software where it lies; a broken variant folder or a missing status file is said,
    never mended."""

    def test_a_broken_variant_folder_refuses(self):
        tree = self.tree()
        (tree / 'src' / 'methods' / FAMILY / 'TOY_A_V1' / 'left_by_an_editor.bak').write_bytes(b'x')
        with self.assertRaises(tree_checks.ChecksRefused) as refused:
            self.software(tree)
        self.assertIn(f'{FAMILY}/TOY_A_V1', str(refused.exception))

    def test_a_missing_status_file_is_a_refusal_and_is_not_created_even_in_dev(self):
        for role in ('DEV', 'QA'):
            with self.subTest(role=role):
                tree = self.worked_tree(role=role, name=f'tree_{role}')
                fx.status_path(tree, FAMILY, 'TOY_A_V1').unlink()
                with fx.ImportPath(tree), self.assertRaises(StatusRefused):
                    self.stored(tree)
                self.assertFalse(fx.status_path(tree, FAMILY, 'TOY_A_V1').exists())


class TheForecastSample(ChecksCase):
    """Specification 12.3 item 4: a fixed sample of stored forecasts, computed again and compared by content."""

    def sample(self, tree: Path) -> tuple:
        """(how many were compared, the differences, the lines said)."""
        said = []
        with fx.ImportPath(tree):
            software, stored = self.stored(tree)
            compared, differences = tree_checks.forecast_sample(software, stored, say=said.append)
        return compared, differences, said

    def test_the_sample_is_the_first_the_middle_and_the_last_stored_forecast_of_each_variant(self):
        tree = self.worked_tree()
        with fx.ImportPath(tree):
            _, stored = self.stored(tree)
        state = stored[GAME].states[0]
        targets = sorted(state.targets)
        self.assertEqual(targets[0], fx.FIRST_TOY_TARGET)
        self.assertEqual(tree_checks.sample_targets(state), [targets[0], targets[len(targets) // 2], targets[-1]])

    def test_lines_without_a_forecast_are_not_in_the_sample(self):
        tree = self.worked_tree(variants=(('TOY_A_V1', {'fail_at': [fx.FIRST_TOY_TARGET, fx.LAST_AT_START + ARRIVED + 1]}),))
        with fx.ImportPath(tree):
            _, stored = self.stored(tree)
        sample = tree_checks.sample_targets(stored[GAME].states[0])
        self.assertEqual((sample[0], sample[-1]), (fx.FIRST_TOY_TARGET + 1, fx.LAST_AT_START + ARRIVED))

    def test_unchanged_software_computes_the_same_forecasts_and_changes_nothing(self):
        tree = self.worked_tree()
        before = whole_tree(tree)
        compared, differences, said = self.sample(tree)
        self.assertEqual((compared, differences), (2 * tree_checks.SAMPLE_SIZE, []))
        self.assertEqual(said, ['  forecast sample: 6 stored forecast(s) computed again; 0 differ'])
        self.assertEqual(whole_tree(tree), before)

    def test_a_forecast_that_comes_out_otherwise_is_named_by_variant_game_and_draw(self):
        tree = self.worked_tree()
        real = tree_checks.compute_target

        def another_order_at_one_draw(variant, method, results, target):
            """The engine's answer, with one variant's ranking turned round at one draw."""
            content, detail = real(variant, method, results, target)
            if (variant.variant, target) == ('TOY_B_V1', fx.FIRST_TOY_TARGET):
                content['barrels']['MAIN']['ranking'] = content['barrels']['MAIN']['ranking'][::-1]
            return content, detail

        with mock.patch.object(tree_checks, 'compute_target', another_order_at_one_draw):
            compared, differences, _ = self.sample(tree)
        self.assertEqual(compared, 6)
        self.assertEqual(differences, [f'{FAMILY}/TOY_B_V1 for {GAME}, draw {fx.FIRST_TOY_TARGET}: the stored '
                                       f'forecast is not what this software computes here'])

    def test_a_forecast_that_cannot_be_computed_again_is_a_difference_with_its_error(self):
        tree = self.worked_tree(variants=('TOY_A_V1',))

        def broken(*arguments):
            """An environment in which the method no longer runs."""
            raise ImportError('numpy.core.multiarray failed to import')

        with mock.patch.object(tree_checks, 'compute_target', broken):
            compared, differences, _ = self.sample(tree)
        self.assertEqual((compared, len(differences)), (3, 3))
        self.assertIn('could not be computed again (ImportError: numpy.core.multiarray failed to import)',
                      differences[0])


class TheDerivedResultsInFull(ChecksCase):
    """Specification 12.3 item 5 and 5.8: every score and the whole prevailing ledger, compared by content."""

    def derived(self, tree: Path, software_root: Path | None = None) -> tuple:
        """(the answers by game, the lines said)."""
        said = []
        with fx.ImportPath(software_root or tree):
            _, stored = self.stored(tree, software_root)
            answers = tree_checks.derived_results(stored, say=said.append)
        return answers, said

    def score_file(self, tree: Path, name: str = 'TOY_A_V1') -> Path:
        """A variant's score list in the test game."""
        return tree / 'results' / 'research' / GAME / 'variants' / FAMILY / name / 'scores.jsonl'

    @staticmethod
    def one_more_hit(line: dict) -> None:
        """Claim one more TOP hit than the forecast had."""
        line['content']['matches']['MAIN']['top'] += 1

    def test_what_the_job_wrote_is_what_the_software_computes_and_nothing_is_changed(self):
        tree = self.worked_tree()
        self.assertTrue(fx.ledger_lines(tree), 'the tree has a prevailing ledger to compare')
        before = whole_tree(tree)
        answers, said = self.derived(tree)
        self.assertEqual(answers, {GAME: None})
        self.assertEqual(said, [f'  derived results: {GAME}: every stored score and prevailing line compared is '
                                f'what this software computes'])
        self.assertEqual(whole_tree(tree), before)

    def test_one_stored_score_altered_is_found_at_its_draw_and_no_marker_is_written(self):
        tree = self.worked_tree()
        fx.alter_list_line(self.score_file(tree), 1156 - fx.FIRST_TOY_TARGET, self.one_more_hit)
        before = whole_tree(tree)
        answers, said = self.derived(tree)
        draw, detail, known = answers[GAME]
        self.assertEqual((draw, known), (1156, False))
        self.assertIn(f'the score of {FAMILY}/TOY_A_V1 for draw 1156 is not what the installed code computes', detail)
        self.assertIn('NOT what this software computes, from draw 1156', said[0])
        self.assertEqual(whole_tree(tree), before, 'the check writes nothing')
        self.assertIsNone(derived_check.read_cutoff(tree, GAME), 'and never the marker')

    def test_one_prevailing_line_altered_is_found_at_its_draw(self):
        tree = self.worked_tree()
        first = fx.ledger_lines(tree)[0]['content']['draw']

        def another_x(line):
            """Store another X than the weights give."""
            line['content']['x'] += 1

        fx.alter_list_line(ov1_ledger.ledger_path(tree, GAME), 1, another_x)
        answers, _ = self.derived(tree)
        self.assertEqual(answers[GAME][0], first + 1)
        self.assertIn('the prevailing line for draw', answers[GAME][1])

    def test_a_difference_the_tree_already_marks_is_known_and_an_earlier_one_is_not(self):
        tree = self.worked_tree()
        fx.alter_list_line(self.score_file(tree), 1156 - fx.FIRST_TOY_TARGET, self.one_more_hit)
        for marked_from, known in ((1150, True), (1156, True), (1157, False)):
            with self.subTest(marked_from=marked_from):
                derived_check.write_cutoff(tree, GAME, marked_from, derived_check.MISMATCH, 'found by a job')
                answers, said = self.derived(tree)
                self.assertEqual(answers[GAME][::2], (1156, known))
                self.assertEqual('already marks them not current' in said[0], known)

    def test_where_a_catch_up_is_awaited_only_the_draws_before_it_are_compared(self):
        tree = self.worked_tree()
        fx.alter_list_line(self.score_file(tree), 1158 - fx.FIRST_TOY_TARGET, self.one_more_hit)
        derived_check.write_cutoff(tree, GAME, 1157, derived_check.AWAITING_CATCH_UP, 'a rerun --to 1156')
        answers, said = self.derived(tree)
        self.assertEqual(answers, {GAME: None})
        self.assertIn('(before draw 1157; a catch-up is awaited from there)', said[0])
        fx.alter_list_line(self.score_file(tree), 1150 - fx.FIRST_TOY_TARGET, self.one_more_hit)
        answers, _ = self.derived(tree)
        self.assertEqual(answers[GAME][::2], (1150, False))

    def test_software_in_another_folder_is_asked_about_the_trees_data_and_the_tree_is_not_touched(self):
        tree = self.worked_tree()
        as_it_would_be = self.root / 'as_it_would_be'
        shutil.copytree(tree / 'src', as_it_would_be / 'src')
        shutil.copytree(tree / 'deploy', as_it_would_be / 'deploy')
        before = whole_tree(tree)
        answers, _ = self.derived(tree, software_root=as_it_would_be)
        self.assertEqual(answers, {GAME: None})
        with fx.ImportPath(as_it_would_be):
            software, stored = self.stored(tree, as_it_would_be)
            self.assertEqual(tree_checks.forecast_sample(software, stored, say=lambda line: None), (6, []))
            self.assertEqual(tree_checks.smoke_cases(software, as_it_would_be, say=lambda line: None), [])
        self.assertEqual(whole_tree(tree), before)

    def test_changed_scoring_code_in_the_other_folder_is_found_from_the_draw_it_changes(self):
        tree = self.worked_tree()
        real = derived_check.score_content

        def new_scoring(forecast, digest, outcome):
            """Scoring code as it would be: it counts one more TOP hit from draw 1152 on."""
            content = real(forecast, digest, outcome)
            if content['target'] >= 1152:
                content['matches']['MAIN']['top'] += 1
            return content

        with mock.patch.object(derived_check, 'score_content', new_scoring):
            answers, _ = self.derived(tree)
        self.assertEqual(answers[GAME][::2], (1152, False))


if __name__ == '__main__':
    unittest.main()
