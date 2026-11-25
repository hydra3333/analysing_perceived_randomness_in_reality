"""Tests of Verify_Tree.bat and of the `checks` command (build step 3, slice C, part C1).

What this file is for
    It shows that research/tree_verify.py carries out deployment design section 7 in its order (process check;
    a backup attempted; the structure; every installed variant's smoke case; the suite; the forecast sample,
    reported; the derived results; the marker; a backup attempted), that only a failed smoke case or a failed
    suite withholds the marker and removes an older one, and that a refusal changes nothing; and that the
    `checks` command of src/tree_checks_command.py writes what it found for the install tool that started it.
    Every tree here is invented and lies in a temporary folder.

Which of the project's own modules it uses
    research.tree_verify, research.tree_checks, research.environment_marker, research.job_lock,
    research.process_rule, research.snapshot; src/tree_checks_command.py; and the fixtures.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import unittest
from datetime import timedelta
from pathlib import Path
from unittest import mock

import research_fixtures as fx
from research import environment_marker, job_lock, process_rule, snapshot, tree_checks, tree_verify

GAME = fx.GAME
FAMILY = 'E_901'
REPOSITORY_ROOT = Path(tree_verify.__file__).resolve().parents[2]
PROGRAM = REPOSITORY_ROOT / 'src' / 'tree_checks_command.py'


def whole_tree(tree: Path) -> dict:
    """Every file of a tree with the SHA-256 of its bytes, Python's own cache files left out."""
    return {path.relative_to(tree).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(tree.rglob('*')) if path.is_file() and '__pycache__' not in path.parts}


def a_clock_that_runs():
    """A clock that is a minute later each time it is read, so that the backup before and the backup after get
    two names."""
    read = iter(range(10 ** 6))
    return lambda: fx.FIXED_TIME + timedelta(minutes=next(read))


def suite_that(outcome: str, calls: list | None = None):
    """A stand-in for the suite: it answers `outcome` and notes that it was asked."""
    def suite(tool, settings, say):
        """Answer as told."""
        if calls is not None:
            calls.append(tool)
        return outcome, f'the suite: {outcome}'
    return suite


class VerifyCase(fx.JobCase):
    """An invented QA tree whose environment has just been rebuilt: it has no marker."""

    def rebuilt(self, **options) -> Path:
        """A tree as installed, its environment's marker removed as the owner's install script removes it."""
        tree = self.tree(**options)
        self.marker(tree).unlink()
        return tree

    def worked(self) -> Path:
        """A tree that holds forecasts, scores and a prevailing ledger, then had its environment rebuilt."""
        tree = self.tree()
        self.assertEqual(fx.run_job(tree)[0], 0)
        self.source(fx.LAST_AT_START + 3, version=2)
        self.assertEqual(fx.run_job(tree)[0], 0)
        self.marker(tree).unlink()
        return tree

    @staticmethod
    def marker(tree: Path) -> Path:
        """The path of the tree's environment marker."""
        return tree / '.venv' / environment_marker.MARKER_NAME

    @staticmethod
    def backups(tree: Path) -> list:
        """The names of the backup ZIPs of the tree, oldest first."""
        return sorted(path.name for path in (tree.parent / (tree.name + '_backups')).glob('*.zip'))

    @staticmethod
    def log(tree: Path) -> list:
        """The verification lines of the tree's log."""
        path = tree / 'records' / tree_verify.TREE_LOG_NAME
        lines = [json.loads(line) for line in path.read_text(encoding='ascii').splitlines()] if path.exists() else []
        return [line for line in lines if line['operation'] == 'VERIFICATION']

    def verify(self, tree: Path, dev: Path | None = None, suite=None) -> tuple:
        """Run the verification; return (the exit code, the lines said)."""
        said = []
        with fx.ImportPath(tree):
            code = tree_verify.verify_tree(tree, dev, now=a_clock_that_runs(), say=said.append,
                                           suite=suite or tree_verify.suite_from_dev)
        return code, said


class AGoodTreeIsVerified(VerifyCase):
    """Deployment design section 7, when nothing is wrong."""

    def test_the_marker_is_written_with_a_backup_before_and_after_and_a_line_in_the_log(self):
        tree = self.rebuilt()
        code, said = self.verify(tree, suite=suite_that(tree_verify.PASSED))
        self.assertEqual(code, tree_verify.EXIT_VERIFIED, said)
        digest = environment_marker.read_marker(tree / '.venv')['digest']
        self.assertEqual(said[-1], f'VERIFIED: {self.marker(tree)} written; the environment\'s digest is {digest}.')
        self.assertEqual([name.split('_', 3)[3] for name in self.backups(tree)],
                         ['PRE_VERIFY.zip', 'POST_VERIFY.zip'])
        self.assertEqual(len([line for line in said if line.startswith('BACKUP MADE AND VERIFIED: ')]), 2)
        (line,) = self.log(tree)
        self.assertEqual((line['outcome'], line['environment_digest'], line['role'], line['suite']),
                         ('VERIFIED', digest, 'QA', 'PASSED'))
        self.assertEqual((line['smoke_cases_failed'], line['sample_compared'], line['derived_not_current']),
                         (0, 0, []))
        self.assertEqual(list((tree / tree_checks.SCRATCH_FOLDER).iterdir()), [])
        self.assertFalse((tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME).exists())

    def test_the_research_job_starts_in_the_tree_afterwards(self):
        tree = self.rebuilt()
        self.assertEqual(fx.run_job(tree)[0], 2, 'without the marker the job refuses')
        self.assertEqual(self.verify(tree)[0], tree_verify.EXIT_VERIFIED)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)

    def test_the_steps_come_in_the_designs_order(self):
        tree = self.worked()
        events = []
        real_rule, real_snapshot = process_rule.check_no_other_process_of_tree, snapshot.attempt_snapshot

        def rule(tree_root):
            """Note the process check, then make it."""
            events.append('process check')
            return real_rule(tree_root)

        def backup(settings, job, now=None):
            """Note the backup, then attempt it."""
            events.append(job)
            return real_snapshot(settings, job, now)

        def said(line):
            """Note the line of each step."""
            for word in ('The structure', '  smoke case', '  forecast sample', '  derived results', 'VERIFIED'):
                if line.startswith(word):
                    events.append(word.strip())

        def suite(tool, settings, say):
            """Note the suite."""
            events.append('suite')
            return tree_verify.PASSED, 'passed'

        with mock.patch.object(process_rule, 'check_no_other_process_of_tree', rule), \
                mock.patch.object(tree_verify, 'attempt_snapshot', backup), fx.ImportPath(tree):
            code = tree_verify.verify_tree(tree, now=a_clock_that_runs(), say=said, suite=suite)
        self.assertEqual(code, tree_verify.EXIT_VERIFIED)
        wanted = ['process check', 'PRE_VERIFY', 'The structure', 'smoke case', 'suite', 'forecast sample',
                  'derived results', 'POST_VERIFY', 'VERIFIED']
        self.assertEqual([event for event in dict.fromkeys(events) if event in wanted], wanted)
        self.assertEqual(events[0], 'process check', 'before the first backup')
        self.assertTrue(self.marker(tree).exists())

    def test_without_dev_named_the_suite_is_not_run_and_the_summary_says_so_in_capitals(self):
        tree = self.rebuilt()
        code, said = self.verify(tree)
        self.assertEqual(code, tree_verify.EXIT_VERIFIED)
        self.assertTrue(said[-2].startswith('THE TEST SUITE WAS NOT RUN: DEV\'s folder was not named.'), said[-2])
        self.assertEqual(self.log(tree)[0]['suite'], 'NOT RUN')

    def test_a_backup_that_cannot_be_made_is_said_and_does_not_stop_the_verification(self):
        tree = self.rebuilt()
        refusal = snapshot.SnapshotResult(False, reason='the backup root cannot be written.')
        with mock.patch.object(tree_verify, 'attempt_snapshot', return_value=refusal):
            code, said = self.verify(tree)
        self.assertEqual(code, tree_verify.EXIT_VERIFIED)
        self.assertEqual(said.count('BACKUP NOT MADE: the backup root cannot be written.'), 2)
        self.assertTrue(snapshot.is_due(tree), 'the tree was written to, so a backup is still owed')


class WhatWithholdsTheMarker(VerifyCase):
    """Design 7: "A failed smoke case or suite writes no marker and removes an older one." """

    def test_a_failed_smoke_case_writes_no_marker_removes_an_older_one_and_leaves_its_folder(self):
        tree = self.tree(variants=('TOY_A_V1', ('TOY_BAD_V1', {'fail_at': [fx.FIRST_TOY_TARGET]})))
        self.assertTrue(self.marker(tree).exists(), 'an older marker')
        asked = []
        code, said = self.verify(tree, suite=suite_that(tree_verify.PASSED, asked))
        self.assertEqual(code, tree_verify.EXIT_NOT_VERIFIED)
        self.assertFalse(self.marker(tree).exists())
        self.assertEqual(asked, [], 'the suite is not run after a failed smoke case')
        self.assertIn(f'{FAMILY}/TOY_BAD_V1 for {GAME}: the smoke case failed', said[-3])
        self.assertEqual(said[-2], 'The test suite was not run: a smoke case had failed.')
        self.assertTrue(said[-1].startswith(f'NOT VERIFIED: {self.marker(tree)} was not written, and an older one '
                                            f'was removed.'))
        self.assertTrue(tree_checks.smoke_folder(tree, mock.Mock(family=FAMILY, variant='TOY_BAD_V1'), GAME).is_dir())
        (line,) = self.log(tree)
        self.assertEqual((line['outcome'], line['environment_digest'], line['smoke_cases_failed']),
                         ('NOT_VERIFIED', None, 1))
        self.assertEqual(self.backups(tree)[-1].split('_', 3)[3], 'POST_VERIFY.zip', 'a backup is still attempted')
        self.assertEqual(fx.run_job(tree)[0], 2, 'and no job starts')

    def test_a_failed_suite_writes_no_marker_and_removes_an_older_one(self):
        tree = self.tree()
        code, said = self.verify(tree, suite=suite_that(tree_verify.FAILED))
        self.assertEqual(code, tree_verify.EXIT_NOT_VERIFIED)
        self.assertFalse(self.marker(tree).exists())
        self.assertEqual(said[-2], 'the suite: FAILED')
        self.assertEqual(self.log(tree)[0]['suite'], 'FAILED')

    def test_a_suite_that_was_not_run_does_not_withhold_it(self):
        tree = self.rebuilt()
        code, _ = self.verify(tree, suite=suite_that(tree_verify.NOT_RUN))
        self.assertEqual(code, tree_verify.EXIT_VERIFIED)
        self.assertTrue(self.marker(tree).exists())


class WhatIsReportedAndDoesNotWithholdIt(VerifyCase):
    """Design 7 and specification 13: the forecast sample's differences are reported for the owner's review; a
    derived result that is no longer current is the research job's to mark."""

    def test_a_difference_in_the_forecast_sample_is_listed_and_the_marker_is_written(self):
        tree = self.worked()
        real = tree_checks.compute_target

        def another_order_at_one_draw(variant, method, results, target):
            """The engine's answer, with one stored variant's ranking turned round at one draw; the smoke
            case's own table (which ends at its target) is left alone."""
            content, detail = real(variant, method, results, target)
            if (variant.variant, target) == ('TOY_B_V1', fx.FIRST_TOY_TARGET) and results.last_draw > target:
                content['barrels']['MAIN']['ranking'] = content['barrels']['MAIN']['ranking'][::-1]
            return content, detail

        with mock.patch.object(tree_checks, 'compute_target', another_order_at_one_draw):
            code, said = self.verify(tree)
        self.assertEqual(code, tree_verify.EXIT_VERIFIED)
        self.assertTrue(self.marker(tree).exists())
        text = '\n'.join(said[said.index(f'VERIFY TREE - END - the QA tree at {tree}'):])
        self.assertIn('THE FORECAST SAMPLE: 1 of 6 stored forecast(s) are NOT what this software computes in this '
                      'environment. This does not withhold the marker', text)
        self.assertIn(f'  {FAMILY}/TOY_B_V1 for {GAME}, draw {fx.FIRST_TOY_TARGET}: the stored forecast is not what',
                      text)
        self.assertEqual(self.log(tree)[0]['sample_differences'], 1)

    def test_a_stored_score_that_is_not_what_the_software_computes_is_said_and_nothing_of_it_is_marked(self):
        tree = self.worked()
        scores = tree / 'results' / 'research' / GAME / 'variants' / FAMILY / 'TOY_A_V1' / 'scores.jsonl'

        def one_more_hit(line: dict) -> None:
            """Claim one more TOP hit than the forecast had."""
            line['content']['matches']['MAIN']['top'] += 1

        fx.alter_list_line(scores, 1156 - fx.FIRST_TOY_TARGET, one_more_hit)
        code, said = self.verify(tree)
        self.assertEqual(code, tree_verify.EXIT_VERIFIED)
        (line,) = [line for line in said if line.startswith('THE DERIVED RESULTS of')]
        self.assertIn(f'THE DERIVED RESULTS of {GAME} are NOT what this software computes here, from draw 1156', line)
        self.assertTrue(line.endswith('The next research job will mark them not current from that draw and say '
                                      'which rerun is owed.'))
        self.assertFalse((tree / 'results' / 'research' / GAME / 'NOT_CURRENT_FROM.json').exists())
        self.assertEqual(self.log(tree)[0]['derived_not_current'], [GAME])

    def test_a_game_whose_records_cannot_be_read_is_said_and_the_marker_is_written(self):
        tree = self.worked()
        scores = tree / 'results' / 'research' / GAME / 'variants' / FAMILY / 'TOY_A_V1' / 'scores.jsonl'
        scores.write_bytes(b'not a line of a list\n' + scores.read_bytes())
        code, said = self.verify(tree)
        self.assertEqual(code, tree_verify.EXIT_VERIFIED, said)
        self.assertIn(f'{GAME}: its stored records could not be read, so nothing of it was compared; the research '
                      f'job will refuse that game for the same reason: ', '\n'.join(said))
        self.assertEqual(self.log(tree)[0]['unreadable'], [GAME])


class WhatIsRefused(VerifyCase):
    """A refusal changes nothing in the tree and leaves the marker as it was."""

    def refused(self, tree: Path, pattern: str, backups: int = 0, **options) -> list:
        """Expect a refusal matching `pattern`, the tree unchanged but for `backups` attempted before it."""
        before, held = whole_tree(tree), self.backups(tree)
        code, said = self.verify(tree, **options)
        self.assertEqual(code, tree_verify.EXIT_REFUSED, said)
        self.assertRegex('\n'.join(said), pattern)
        after = whole_tree(tree)
        for name in ('records/SNAPSHOT_LOG.jsonl',):
            if backups:
                before.pop(name, None), after.pop(name, None)
        self.assertEqual(after, before)
        self.assertEqual(len(self.backups(tree)) - len(held), backups)
        self.assertEqual(self.log(tree), [])
        return said

    def test_dev_has_nothing_to_verify(self):
        tree = self.tree(role='DEV')
        self.refused(tree, r'REFUSED: this is the DEV tree\.')

    def test_an_unfinished_operation(self):
        tree = self.tree()
        (tree / 'records').mkdir(exist_ok=True)
        (tree / 'records' / 'INSTALL_IN_PROGRESS.json').write_text('{}', encoding='ascii')
        self.refused(tree, r'INSTALL_IN_PROGRESS\.json exists')

    def test_the_orphan_marker(self):
        tree = self.tree()
        orphan = tree / job_lock.ORPHAN_MARKER
        orphan.parent.mkdir(parents=True)
        orphan.write_text('[{"run": "invented"}]', encoding='ascii')
        self.refused(tree, r'UNRESOLVED_ORPHAN\.json')

    def test_another_python_process_of_the_tree_refuses_before_any_backup(self):
        tree = self.tree()
        error = process_rule.ProcessRuleRefused('1 other Python process(es) of the tree are running')
        with mock.patch.object(process_rule, 'check_no_other_process_of_tree', side_effect=error):
            said = self.refused(tree, r'REFUSED: 1 other Python process')
        self.assertEqual(said[-1], 'VERIFY TREE - END - refused; nothing was changed.')

    def test_a_job_that_holds_the_lock(self):
        tree = self.tree()
        with job_lock.job_lock(tree, 'a test', 'now'):
            code, said = self.verify(tree)
        self.assertEqual(code, tree_verify.EXIT_REFUSED)
        self.assertIn('BACKUP NOT MADE: a job of this tree holds its lock', '\n'.join(said))
        self.assertEqual(said[-1], 'VERIFY TREE - END - refused; the environment\'s marker is as it was.')
        self.assertTrue(self.marker(tree).exists())

    def test_software_that_is_not_what_was_installed(self):
        tree = self.tree()
        (tree / 'src' / 'stray.py').write_text('# not installed\n', encoding='ascii')
        self.refused(tree, r'does not match its list of installed files', backups=1)
        self.assertTrue(self.marker(tree).exists(), 'the marker is as it was')

    def test_a_status_file_that_fails_its_own_check(self):
        tree = self.tree()
        fx.status_path(tree, FAMILY, 'TOY_A_V1').write_text('not a status file\n', encoding='ascii')
        self.refused(tree, r'REFUSED: a status file fails its own check: E_901/TOY_A_V1: ', backups=1)


class TheDevTreeNamedForTheSuite(VerifyCase):
    """The suite belongs to DEV: the folder named must be the DEV tree that names this tree."""

    def dev_for(self, tree: Path, names: Path | None = None, with_tool: str | None = 'import sys\nsys.exit(0)\n'):
        """An invented DEV tree whose settings name `names` (default: the tree) as its QA tree."""
        dev = self.root / 'dev'
        dev.mkdir()
        fx.make_tree(dev)
        named = names or tree
        with open(dev / 'ENVIRONMENT.ini', 'a', encoding='utf-8', newline='\n') as stream:
            stream.write(f'[QA]\ntree_root = {named}\nbackup_root = {named.parent / (named.name + "_backups")}\n'
                         f'venv_dir = {named / ".venv"}\n')
        if with_tool is not None:
            (dev / 'deploy' / 'suite_for_tree.py').write_text(with_tool, encoding='ascii')
        return dev

    def settings(self, tree: Path):
        """The tree's settings."""
        from research.settings import read_settings
        return read_settings(tree)

    def test_the_dev_tree_that_names_this_tree_gives_its_tool(self):
        tree = self.tree()
        dev = self.dev_for(tree)
        self.assertEqual(tree_verify.check_dev_folder(dev, self.settings(tree)), dev / 'deploy' / 'suite_for_tree.py')

    def test_a_folder_that_is_not_a_dev_tree_refuses_before_anything_is_done(self):
        tree = self.tree()
        other = self.tree(name='other')
        before = whole_tree(tree)
        code, said = self.verify(tree, dev=other)
        self.assertEqual(code, tree_verify.EXIT_REFUSED)
        self.assertRegex(said[0], r'^REFUSED: .*ENVIRONMENT\.ini')
        self.assertEqual(whole_tree(tree), before)
        self.assertEqual(self.backups(tree), [])

    def test_a_dev_tree_that_names_another_folder_as_this_role_refuses(self):
        tree = self.tree()
        other = self.tree(name='other')
        dev = self.dev_for(tree, names=other)
        from research.settings import SettingsRefused
        with self.assertRaisesRegex(SettingsRefused, 'names .*other as its QA tree, and this tree is'):
            tree_verify.check_dev_folder(dev, self.settings(tree))

    def test_a_dev_tree_without_the_tool_refuses(self):
        tree = self.tree()
        dev = self.dev_for(tree, with_tool=None)
        from research.settings import SettingsRefused
        with self.assertRaisesRegex(SettingsRefused, 'suite_for_tree.py is missing'):
            tree_verify.check_dev_folder(dev, self.settings(tree))

    def test_the_tools_exit_code_decides_and_it_is_started_with_the_python_that_is_running(self):
        tree = self.tree()
        tool = self.root / 'tool.py'
        proof = self.root / 'started_with.txt'
        for exit_code, outcome, words in ((0, tree_verify.PASSED, 'The test suite passed'),
                                          (1, tree_verify.FAILED, 'THE TEST SUITE FAILED or could not be run'),
                                          (3, tree_verify.NOT_RUN, 'the tests in DEV are for other code'),
                                          (2, tree_verify.FAILED, 'exit code 2')):
            tool.write_text(f'import sys\nopen({str(proof)!r}, "w").write(sys.executable + "|" + "|".join(sys.argv[1:])'
                            f' + "|" + str(sys.flags.isolated))\nsys.exit({exit_code})\n', encoding='ascii')
            found, line = tree_verify.suite_from_dev(tool, self.settings(tree), lambda said: None)
            self.assertEqual(found, outcome)
            self.assertIn(words, line)
            started_with, *rest = proof.read_text().split('|')
            self.assertEqual(os.path.normpath(started_with), os.path.normpath(sys.executable))
            self.assertEqual(rest, ['--tree', str(tree), '1'], 'the tree named; Python in isolated mode')


class TheChecksCommand(VerifyCase):
    """The `checks` command: what an install tool asks with the target tree's Python, and reads from a file."""

    def checks(self, tree: Path, *words, software: Path | None = None) -> tuple:
        """Run the command; return (the exit code, the result read from its file or None, the lines said)."""
        said, result = [], self.root / 'result.json'
        with fx.ImportPath(software or tree):
            code = tree_checks.main(['--data', str(tree), '--result', str(result), *words], software or tree,
                                    say=said.append)
        return code, json.loads(result.read_text(encoding='ascii')) if result.exists() else None, said

    def test_everything_asked_of_a_worked_tree_is_found_and_written_and_the_tree_is_not_changed(self):
        tree = self.worked()
        before = whole_tree(tree)
        code, found, _ = self.checks(tree, '--smoke', 'ALL', '--sample', '--derived')
        self.assertEqual(code, tree_checks.EXIT_RAN)
        self.assertEqual(found, {'kind': 'TREE_CHECKS_V1', 'software_root': str(tree), 'data_root': str(tree),
                                 'smoke': {'asked': 'ALL', 'failures': []}, 'unreadable': {},
                                 'sample': {'compared': 6, 'differences': []}, 'derived': {GAME: None}})
        self.assertEqual(whole_tree(tree), before)

    def test_what_was_not_asked_is_not_made(self):
        tree = self.worked()
        code, found, said = self.checks(tree, '--derived')
        self.assertEqual(code, tree_checks.EXIT_RAN)
        self.assertEqual((found['smoke'], found['sample'], found['derived']), (None, None, {GAME: None}))
        self.assertEqual(len(said), 1)

    def test_a_failure_is_written_for_the_tool_to_judge_and_the_command_still_ends_with_zero(self):
        tree = self.tree(variants=('TOY_A_V1', ('TOY_BAD_V1', {'fail_at': [fx.FIRST_TOY_TARGET]})))
        code, found, _ = self.checks(tree, '--smoke', f'{FAMILY}/TOY_BAD_V1')
        self.assertEqual(code, tree_checks.EXIT_RAN)
        self.assertEqual(found['smoke']['asked'], [f'{FAMILY}/TOY_BAD_V1'])
        (failure,) = found['smoke']['failures']
        self.assertIn('the smoke case failed: NO_FORECAST', failure)

    def test_a_derived_difference_is_written_with_its_draw_and_whether_the_tree_knows_it(self):
        tree = self.worked()
        scores = tree / 'results' / 'research' / GAME / 'variants' / FAMILY / 'TOY_A_V1' / 'scores.jsonl'

        def one_more_hit(line: dict) -> None:
            """Claim one more TOP hit than the forecast had."""
            line['content']['matches']['MAIN']['top'] += 1

        fx.alter_list_line(scores, 1156 - fx.FIRST_TOY_TARGET, one_more_hit)
        _, found, _ = self.checks(tree, '--derived')
        self.assertEqual((found['derived'][GAME]['from_draw'], found['derived'][GAME]['known']), (1156, False))

    def test_a_smoke_case_asked_for_a_variant_the_software_does_not_hold_is_refused(self):
        tree = self.tree()
        code, found, said = self.checks(tree, '--smoke', f'{FAMILY}/NOT_THERE_V1')
        self.assertEqual((code, found), (tree_checks.EXIT_REFUSED, None))
        self.assertIn(f'REFUSED: a smoke case was asked for {FAMILY}/NOT_THERE_V1', said[0])

    def test_a_result_file_that_exists_is_never_overwritten(self):
        tree = self.tree()
        (self.root / 'result.json').write_text('{"kept": true}', encoding='ascii')
        code, found, said = self.checks(tree, '--smoke', 'ALL')
        self.assertEqual((code, found), (tree_checks.EXIT_REFUSED, {'kept': True}))
        self.assertTrue(said[-1].startswith('REFUSED: '))

    def test_a_tree_whose_settings_are_refused_is_refused(self):
        tree = self.tree()
        (tree / 'ENVIRONMENT.ini').unlink()
        code, found, said = self.checks(tree, '--smoke', 'ALL')
        self.assertEqual((code, found), (tree_checks.EXIT_REFUSED, None))


class TheProgramAndItsLauncher(VerifyCase):
    """src/tree_checks_command.py and Verify_Tree.bat."""

    def program(self):
        """The program, loaded as a module of its own."""
        spec = importlib.util.spec_from_file_location('tree_checks_command_under_test', PROGRAM)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_program(self, tree: Path, words, prefix: Path | None = None) -> tuple:
        """Run the program as if it lay in `tree`; return (the exit code, what it printed)."""
        program, printed = self.program(), []
        with mock.patch.object(program, 'SOFTWARE_ROOT', tree), mock.patch.object(program, 'IMPORT_FOLDERS', ()), \
                mock.patch('builtins.print', lambda *words: printed.append(' '.join(str(word) for word in words))), \
                fx.ImportPath(tree):
            code = program.run_command(list(words), running_prefix=str(prefix or tree / '.venv'))
        return code, '\n'.join(printed)

    def test_a_word_that_is_no_command_is_refused(self):
        code, printed = self.run_program(self.tree(), ['research'])
        self.assertEqual(code, 2)
        self.assertIn('the first word must be one of: verify, checks', printed)

    def test_a_python_that_is_not_the_trees_own_is_refused_for_both_commands(self):
        tree = self.tree()
        before = whole_tree(tree)
        for words in (['verify'], ['checks', '--data', str(tree), '--result', str(self.root / 'r.json')]):
            code, printed = self.run_program(tree, words, prefix=self.root / 'another_python')
            self.assertEqual(code, 2)
            self.assertIn('These checks are made with the tree\'s own Python and no other.', printed)
        self.assertEqual(whole_tree(tree), before)

    def test_checks_is_held_to_the_python_of_the_tree_whose_data_it_reads_not_of_the_folder_it_lies_in(self):
        tree = self.tree()
        elsewhere = self.root / 'software_as_it_would_be'
        elsewhere.mkdir()
        program = self.program()
        with mock.patch.object(program, 'SOFTWARE_ROOT', elsewhere):
            self.assertEqual(program.data_root_of(['checks', '--result', 'x', '--data', str(tree)]), tree)
            self.assertEqual(program.data_root_of(['verify']), elsewhere)

    def test_verify_without_a_marker_is_let_through_to_the_verification(self):
        tree = self.rebuilt()
        with mock.patch.object(tree_verify, 'main', return_value=0) as main:
            code, printed = self.run_program(tree, ['verify', '--dev', 'X'])
        self.assertEqual(code, 0, printed)
        main.assert_called_once_with(['--dev', 'X'], tree)

    def test_the_launcher_runs_verify_with_the_trees_own_python_isolated_and_passes_on_what_was_typed(self):
        text = (REPOSITORY_ROOT / 'Verify_Tree.bat').read_bytes().decode('ascii')
        self.assertIn('set "PY=%ROOT%.venv\\Scripts\\python.exe"', text)
        self.assertIn('"%PY%" -I -B -u "%TOOL%" verify %*\r\nexit /b %ERRORLEVEL%\r\n', text)
        self.assertEqual(text.count('\n'), text.count('\r\n'), 'every line ends CRLF')
        self.assertNotIn('<', text.replace('1>&2', ''))


if __name__ == '__main__':
    unittest.main()
