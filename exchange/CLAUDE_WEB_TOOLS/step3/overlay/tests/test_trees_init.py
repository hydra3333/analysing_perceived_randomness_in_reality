"""Tests of Init_Tree.bat (deploy/init_tree.py): creating a QA or PROD tree from DEV (build step 3, slice C, part C3).

What this file is for
    It shows, on invented trees in temporary folders, the nine steps of deployment design section 4: the plan
    and the one question; the folder, the settings file written once, the barrier; every planned file and a
    status file for each variant; the accepted results copied and recorded; the pause for the owner to build the
    environment; the checks with the tree's own Python and the marker; the kit, the list, the log line and the
    barrier removed last; the first backup. And that the same command typed again finishes a creation that
    stopped anywhere, that a folder which is not this creation is refused, and that a failed check leaves the
    barrier in place.
    The start of the tree's own Python is stood in for here (the checks are made in this process); the suite is
    stood in for by one that passes or fails as the test says.

Which of the project's own modules it uses
    deploy/init_tree.py, deploy/install_common.py, deploy/recovery_kit.py, deploy/deploy_command.py;
    research.environment_marker, research.installed_files, research.job_lock, research.launch_guard,
    research.settings, research.tree_checks; the fixtures, and the invented DEV of tests/test_trees_install_common.py.
"""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import init_tree                                             # noqa: E402  (after the path line above)
import install_common as common                              # noqa: E402
import install_readiness                                     # noqa: E402
import recovery_kit                                          # noqa: E402
import research_fixtures as fixtures                         # noqa: E402
from _common.game_profiles import get_profile                # noqa: E402
from research import environment_marker, installed_files, job_lock, launch_guard, settings, tree_checks    # noqa: E402
from test_trees_install_common import FAMILY, FIRST, GAMES, METHODS, SECOND, InventedDevAndTarget, whole_tree    # noqa: E402

KIT = recovery_kit.KitResult(True, path=Path('an invented kit.zip'))
NO_KIT = recovery_kit.KitResult(False, reason='the backup root cannot be written.')
RESULT_NAMES = [name.format(game_id=game_id) for game_id in GAMES for name in init_tree.RESULTS_FILE_NAMES]


def never_asked(prompt):
    """The answer of a run in which no question may be asked."""
    raise AssertionError('no question is asked here')


def checks_in_this_process(python, software_root, tree_root, smoke, sample, derived, say=print, run=None,
                           write_marker=False) -> dict:
    """A stand-in for the start of the tree's own Python: the same checks, made here. (The word for "no smoke
    case" is turned into what the program's own command line turns it into; and, as the program does, the
    variants are imported from the folder the software lies in.)"""
    with fixtures.ImportPath(Path(software_root)):
        return tree_checks.run_checks(Path(software_root), settings.read_settings(Path(tree_root)),
                                      None if smoke == common.NO_VARIANT else smoke, sample, derived, say,
                                      write_marker)


def suite_that(passes: bool):
    """A stand-in for the suite: it requires what the real one requires and then passes or fails as told."""
    def suite(dev_root, dev_files, installed, python, say=print):
        """Answer as told, for a tree whose infrastructure is DEV's."""
        assert common.infrastructure_differences(dev_files, installed) == [], 'at a creation it is DEV\'s'
        assert Path(python).parts[-3:] == ('.venv', 'Scripts', 'python.exe'), python
        return passes, f'THE TEST SUITE {"PASSED" if passes else "FAILED"}: an invented suite.'
    return suite


class CreationCase(InventedDevAndTarget):
    """The invented DEV, with accepted results of both games and an entry for a QA tree that does not exist."""

    def setUp(self):
        """Give DEV its results and its entry for QA; the target folder does not exist."""
        super().setUp()
        self.target.rmdir()
        self.backups = self.target.parent / 'target_backups'
        self.write_results()
        self.add_entry('QA', self.target)

    def write_results(self) -> None:
        """Give DEV the accepted results of both games: results, ledger and verification record."""
        for game_id in GAMES:
            fixtures.write_results(self.dev, game_id, get_profile(game_id).first_draw + 16)
            (self.dev / 'source_data' / f'{game_id}_results_master_init_verification.json').write_bytes(
                b'{"invented": "a verification record"}\r\n')

    def add_variant(self, name: str, mark: bool = True) -> Path:
        """Add a toy variant to DEV as the base class does, then write the results again: the base's helper
        brings every file of the invented DEV to a text file's form, which results are not."""
        folder = super().add_variant(name, mark)
        if (self.dev / 'source_data').exists():
            self.write_results()
        return folder

    def add_entry(self, role: str, root: Path) -> None:
        """Add DEV's entry for a tree."""
        with open(self.dev / 'ENVIRONMENT.ini', 'a', encoding='utf-8', newline='\r\n') as handle:
            handle.write(f'[{role}]\ntree_root = {root}\nbackup_root = {root.parent / (root.name + "_backups")}\n'
                         f'venv_dir = {root / ".venv"}\n')

    def init(self, role: str = 'QA', answers=(), suite: bool = True, kit=KIT) -> tuple:
        """Run the command; return (the exit code, the lines said). answers: what the owner types, in order; a
        question beyond them fails the test."""
        said, left = [], list(answers)

        def ask(prompt):
            """Give the next answer."""
            if not left:
                raise AssertionError(f'an unexpected question: {said[-1]}')
            return left.pop(0)

        with mock.patch.object(common, 'checks_with_target_python', checks_in_this_process), \
                mock.patch.object(common, 'suite_if_it_is_the_trees', suite_that(suite)), \
                mock.patch.object(recovery_kit, 'build_kit', return_value=kit):
            code = init_tree.main([role], settings.read_dev_view(self.dev), say=said.append, ask=ask, now=self.clock)
        self.assertEqual(left, [], 'every answer given was asked for')
        return code, said

    def build_environment(self, root: Path | None = None) -> None:
        """What the owner does at the pause: build the tree's .venv (here an invented one)."""
        fixtures.make_invented_environment((root or self.target) / '.venv')

    def created(self, role: str = 'QA', root: Path | None = None) -> None:
        """Create a tree whole: the first run, the environment, the second run."""
        self.assertEqual(self.init(role, answers=['YES'])[0], init_tree.EXIT_BUILD_THE_ENVIRONMENT)
        self.build_environment(root)
        code, said = self.init(role)
        self.assertEqual(code, init_tree.EXIT_CREATED, said)


class ACreationFromStartToEnd(CreationCase):
    """Deployment design section 4, in its order."""

    def test_the_first_run_puts_software_settings_and_results_in_place_and_pauses_behind_its_barrier(self):
        dev_before = whole_tree(self.dev)
        code, said = self.init(answers=['YES'])
        self.assertEqual(code, init_tree.EXIT_BUILD_THE_ENVIRONMENT, said)
        plan = common.read_barrier(self.target)
        self.assertEqual((plan['operation'], plan['role'], plan['tree_root']), ('INIT', 'QA', str(self.target)))
        tree = whole_tree(self.target)
        for entry in plan['add']:
            self.assertEqual(tree[entry['path']], entry['sha256'])
        self.assertEqual((self.target / 'ENVIRONMENT.ini').read_bytes().decode('utf-8'),
                         f'[environment]\r\nrole = QA\r\ntree_root = {self.target}\r\nbackup_root = {self.backups}\r\n'
                         f'venv_dir = {self.target / ".venv"}\r\n')
        self.assertIn(f'{METHODS}/{FAMILY}/{FIRST}/VARIANT_STATUS.ini', tree)
        for name in RESULT_NAMES:
            self.assertEqual(tree[f'source_data/{name}'], dev_before[f'source_data/{name}'])
        record = json.loads((self.target / init_tree.INIT_RECORD_PATH).read_bytes())
        self.assertEqual((record['kind'], record['results_copied_from'], record['results_copied_from_role']),
                         ('INIT_RECORD_V1', str(self.dev), 'DEV'))
        self.assertEqual([entry['path'] for entry in record['results']], [f'source_data/{n}' for n in RESULT_NAMES])
        self.assertEqual(sorted(set(tree) - {e['path'] for e in plan['add']} - {f'source_data/{n}' for n in RESULT_NAMES}),
                         ['ENVIRONMENT.ini', 'records/INIT_RECORD.json', 'records/INSTALL_IN_PROGRESS.json',
                          'records/SNAPSHOT_DUE', f'{METHODS}/{FAMILY}/{FIRST}/VARIANT_STATUS.ini'],
                         'nothing else: no lock is left, no forecast, score or report was copied')
        self.assertEqual(whole_tree(self.dev), dev_before, 'DEV is only read')
        self.assertIn('INIT TREE - PAUSED - ', said[-1])
        self.assertIn('create_venv.bat, then install_upgrade_dependencies_into_venv.bat', said[-1])
        with self.assertRaisesRegex(launch_guard.GuardRefused, 'INSTALL_IN_PROGRESS.json exists'):
            launch_guard.check_no_unfinished_operation(self.target)

    def test_the_same_command_again_verifies_finishes_and_backs_up_and_asks_nothing(self):
        self.init(answers=['YES'])
        self.build_environment()
        code, said = self.init()
        self.assertEqual(code, init_tree.EXIT_CREATED, said)
        text = '\n'.join(said)
        self.assertIn('This same creation was begun before and is being continued', text)
        self.assertIn('Files: 0 copied (each to a temporary name, hashed, renamed); 8 already in place; 0 removed.',
                      text)
        self.assertIn('already copied from', text)
        digest = environment_marker.read_marker(self.target / '.venv')['digest']
        self.assertIn(f'The environment is verified; its digest is {digest}.', text)
        content = installed_files.read_list(self.target)
        self.assertEqual(installed_files.differences(self.target, content), [])
        self.assertEqual(content, installed_files.software_now(self.target))
        (line,) = (self.target / common.TREE_LOG_PATH).read_text(encoding='ascii').splitlines()
        record = json.loads(line)
        self.assertEqual((record['operation'], record['suite'], record['environment_digest'], record['recovery_kit']),
                         ('INIT', 'PASSED', digest, True))
        records = sorted(path.name for path in (self.target / 'records').iterdir())
        self.assertEqual(records, ['INIT_RECORD.json', 'INSTALLED_FILES.json', 'INSTALL_LOG.jsonl',
                                   'SNAPSHOT_LOG.jsonl', 'status_staging'], 'no barrier, no lock, no backup owed')
        self.assertEqual(list((self.target / 'records' / 'status_staging').iterdir()), [])
        self.assertEqual([path.name.split('_', 3)[3] for path in self.backups.glob('*.zip')], ['INIT.zip'])
        self.assertTrue(said[-2].startswith('BACKUP MADE AND VERIFIED: '))
        self.assertIn('is created. Its first research job', said[-1])

    def test_the_order_of_the_second_run_is_the_designs(self):
        self.init(answers=['YES'])
        self.build_environment()
        _, said = self.init()
        marks = ('The tree\'s software is exactly the plan', 'THE TEST SUITE PASSED', 'The smoke cases:',
                 'The environment is verified', 'RECOVERY KIT WRITTEN AND CHECKED',
                 'The list of installed files and the log line are written', 'The first backup is attempted',
                 'BACKUP MADE AND VERIFIED')
        positions = [next(i for i, line in enumerate(said) if line.startswith(mark)) for mark in marks]
        self.assertEqual(positions, sorted(positions), said)

    def test_the_updaters_lock_is_let_go_before_the_barrier_is_removed_and_the_job_lock_after_it(self):
        self.init(answers=['YES'])
        self.build_environment()
        seen, real = {}, common.remove_barrier

        def look_then_remove(tree_root):
            """Note what is still held at the moment the barrier is removed."""
            seen['updater lock'] = (self.target / job_lock.UPDATER_LOCK).exists()
            seen['job lock'] = (self.target / 'records' / job_lock.JOB_LOCK_NAME).exists()
            seen['list'] = (self.target / installed_files.LIST_PATH).is_file()
            real(tree_root)

        with mock.patch.object(common, 'remove_barrier', look_then_remove):
            self.assertEqual(self.init()[0], init_tree.EXIT_CREATED)
        self.assertEqual(seen, {'updater lock': False, 'job lock': True, 'list': True})

    def test_the_research_job_runs_in_the_new_tree(self):
        self.created()
        code, said = fixtures.run_job(self.target, games=('POWERBALL',))
        self.assertEqual(code, 0, said)

    def test_a_prod_tree_is_created_with_no_results_section_and_its_results_come_from_dev(self):
        prod = self.target.parent / 'prod'
        self.add_entry('PROD', prod)
        self.assertEqual(self.init('PROD', answers=['YES'])[0], init_tree.EXIT_BUILD_THE_ENVIRONMENT)
        self.assertNotIn(b'[results]', (prod / 'ENVIRONMENT.ini').read_bytes())
        self.assertIn(b'role = PROD\r\n', (prod / 'ENVIRONMENT.ini').read_bytes())
        self.assertEqual(json.loads((prod / init_tree.INIT_RECORD_PATH).read_bytes())['results_copied_from_role'], 'DEV')
        self.assertFalse(self.target.exists(), 'the QA tree was not touched')


class TheOneQuestion(CreationCase):
    """Step 2: the plan is shown and the owner types the confirmation."""

    def test_anything_but_yes_creates_nothing(self):
        for answer in ('', 'NO', 'yes', 'y'):
            code, said = self.init(answers=[answer])
            self.assertEqual(code, init_tree.EXIT_REFUSED)
            self.assertFalse(self.target.exists())
            self.assertEqual(said[-1], 'INIT TREE - END - NO: nothing was created.')

    def test_the_plan_the_variants_left_out_and_the_source_of_the_results_are_shown_before_it(self):
        self.add_variant(SECOND, mark=False)
        _, said = self.init(answers=['NO'])
        question = next(i for i, line in enumerate(said) if line.startswith('Type YES to create the QA tree at'))
        before = '\n'.join(said[:question])
        self.assertIn(f'The plan (INIT into the QA tree at {self.target}): 8 file(s) to add', before)
        self.assertIn(f'  variant to add: {FAMILY}/{FIRST} (POWERBALL, OZLOTTO)', before)
        self.assertIn(f'  left out, not ready: {FAMILY}/{SECOND}: it is not marked.', before)
        self.assertIn(f'The accepted results will be copied from the DEV tree at {self.dev}.', before)

    def test_a_variant_that_is_not_ready_is_not_in_the_tree(self):
        self.add_variant(SECOND, mark=False)
        self.created()
        self.assertFalse((self.target / METHODS / FAMILY / SECOND).exists())
        self.assertEqual([entry['variant'] for entry in installed_files.read_list(self.target)['variants']], [FIRST])


class WhatIsRefusedBeforeAnythingIsChanged(CreationCase):
    """Step 1, and what must be so in DEV."""

    def refused(self, pattern: str, role: str = 'QA') -> list:
        """Expect a refusal matching `pattern`, with no question asked and the target as it was."""
        before = whole_tree(self.target) if self.target.exists() else None
        code, said = self.init(role)
        self.assertEqual(code, init_tree.EXIT_REFUSED, said)
        self.assertRegex('\n'.join(said), pattern)
        self.assertEqual(whole_tree(self.target) if self.target.exists() else None, before)
        return said

    def test_no_word_or_a_word_that_is_no_role(self):
        said = []
        self.assertEqual(init_tree.main([], settings.read_dev_view(self.dev), say=said.append), 2)
        self.assertEqual(said, [init_tree.USAGE])
        self.refused('"DEV" is not a tree this command can work on', role='DEV')
        self.refused(r'has no section for the PROD tree', role='PROD')

    def test_infrastructure_that_is_not_ready(self):
        install_readiness.unmark_infrastructure(self.dev)
        self.refused('Make_Installable.bat INFRA')
        self.assertFalse(self.target.exists())

    def test_a_folder_that_holds_something_else(self):
        self.target.mkdir()
        (self.target / 'holiday.jpg').write_bytes(b'not a tree')
        self.refused('is not empty and is not a tree this command began')

    def test_an_empty_folder_is_a_place_for_a_tree(self):
        self.target.mkdir()
        self.assertEqual(self.init(answers=['YES'])[0], init_tree.EXIT_BUILD_THE_ENVIRONMENT)

    def test_a_tree_that_is_already_created(self):
        self.created()
        self.refused('is already a created QA tree. To add variants use Install.bat QA')

    def test_a_settings_file_there_that_is_not_this_creations(self):
        self.target.mkdir()
        (self.target / 'ENVIRONMENT.ini').write_bytes(b'[environment]\r\nrole = PROD\r\n')
        self.refused('is not the settings file this creation writes')

    def test_dev_changed_since_the_creation_began_shows_both_plans_and_says_how_to_abandon_it(self):
        self.init(answers=['YES'])
        self.add_variant(SECOND)
        said = self.refused('holds another plan than the plan now')
        text = '\n'.join(said)
        self.assertIn('THE UNFINISHED PLAN:', text)
        self.assertIn(f'  variant to add: {FAMILY}/{SECOND} (POWERBALL, OZLOTTO)', text.split('THE PLAN NOW:')[1])
        self.assertIn(f'To abandon it, delete the folder {self.target} yourself', text)

    def test_results_in_the_source_that_are_not_whole_refuse_before_the_question(self):
        (self.dev / 'source_data' / 'OZLOTTO_results_master_init_verification.json').unlink()
        self.refused('OZLOTTO_results_master_init_verification.json is missing or is not an ordinary file')
        self.assertFalse(self.target.exists())

    def test_another_python_process_of_the_tree_to_be(self):
        from research import process_rule
        error = process_rule.ProcessRuleRefused('1 other Python process(es) of the tree are running')
        with mock.patch.object(process_rule, 'check_no_other_process_of_tree', side_effect=error):
            code, said = self.init(answers=['YES'])
        self.assertEqual(code, init_tree.EXIT_REFUSED)
        self.assertFalse(self.target.exists(), 'the folder is not even created')


class TheSettingsFileIsWrittenOnce(CreationCase):
    """Deployment design section 1: written exactly once, create-only, and never by a tool afterwards."""

    def test_the_second_run_does_not_write_it_again(self):
        self.init(answers=['YES'])
        path = self.target / 'ENVIRONMENT.ini'
        data = path.read_bytes()
        self.build_environment()
        real_open, opened = open, []

        def watching(file, mode='r', *arguments, **options):
            """Note every opening of the settings file for writing."""
            if Path(str(file)).name == 'ENVIRONMENT.ini' and any(letter in mode for letter in 'wax+'):
                opened.append(mode)
            return real_open(file, mode, *arguments, **options)

        with mock.patch('builtins.open', watching):
            self.assertEqual(self.init()[0], init_tree.EXIT_CREATED)
        self.assertEqual((opened, path.read_bytes()), ([], data))

    def test_it_is_read_back_and_a_file_that_does_not_give_devs_entry_stops_before_any_software_is_copied(self):
        real = init_tree.settings_bytes

        def naming_another_backup_root(entry, copy_from):
            """The file as it would be if it were written wrongly."""
            return real(entry, copy_from).replace(str(self.backups).encode(), str(self.backups).encode() + b'_x')

        with mock.patch.object(init_tree, 'settings_bytes', naming_another_backup_root):
            code, said = self.init(answers=['YES'])
        self.assertEqual(code, init_tree.EXIT_REFUSED, said)
        self.assertIn('backup_root disagrees for the QA tree', '\n'.join(said))
        self.assertIsNone(common.read_barrier(self.target))
        self.assertFalse((self.target / 'src').exists())
        self.assertFalse((self.target / 'records' / job_lock.JOB_LOCK_NAME).exists())

    def test_the_command_opens_it_for_writing_in_one_place_and_only_to_create_it(self):
        source = (REPOSITORY_ROOT / 'deploy' / 'init_tree.py').read_text(encoding='utf-8')
        self.assertEqual(source.count('open(settings_file'), 1)
        self.assertIn("with open(settings_file, 'xb') as handle:", source)

    def test_a_qa_tree_names_prod_as_the_tree_its_jobs_copy_results_from_when_dev_names_a_prod(self):
        prod = self.target.parent / 'prod'
        self.add_entry('PROD', prod)
        self.init(answers=['YES'])
        self.assertIn(f'[results]\r\ncopy_from = {prod}\r\n', (self.target / 'ENVIRONMENT.ini').read_bytes().decode())
        self.assertEqual(settings.read_settings(self.target).results_copy_from, prod)
        self.assertEqual(json.loads((self.target / init_tree.INIT_RECORD_PATH).read_bytes())['results_copied_from_role'],
                         'DEV', 'no PROD tree exists yet, so the results themselves come from DEV')


class WhereTheResultsComeFrom(CreationCase):
    """Specification 12.5: QA from PROD, or from DEV while no PROD exists; PROD from DEV."""

    def setUp(self):
        """A PROD tree, created; then DEV's results grow, so the two sources differ."""
        super().setUp()
        self.prod = self.target.parent / 'prod'
        self.add_entry('PROD', self.prod)
        self.created('PROD', self.prod)
        fixtures.write_results(self.dev, 'POWERBALL', get_profile('POWERBALL').first_draw + 20, version=2)

    def test_qa_takes_its_results_from_the_prod_tree_once_one_exists_and_prod_is_only_read(self):
        prod_before = whole_tree(self.prod)
        code, said = self.init(answers=['YES'])
        self.assertEqual(code, init_tree.EXIT_BUILD_THE_ENVIRONMENT, said)
        self.assertIn(f'The accepted results will be copied from the PROD tree at {self.prod}.', said)
        for name in RESULT_NAMES:
            self.assertEqual((self.target / 'source_data' / name).read_bytes(),
                             (self.prod / 'source_data' / name).read_bytes())
        self.assertNotEqual((self.target / 'source_data' / RESULT_NAMES[0]).read_bytes(),
                            (self.dev / 'source_data' / RESULT_NAMES[0]).read_bytes())
        self.assertEqual(whole_tree(self.prod), prod_before)

    def test_a_prod_tree_with_an_unfinished_install_or_a_results_update_is_not_read(self):
        for held, words in ((common.BARRIER_PATH, 'an install is unfinished there'),
                            (job_lock.UPDATER_LOCK, 'a results update holds its lock there')):
            (self.prod / held).parent.mkdir(exist_ok=True)
            (self.prod / held).write_bytes(b'{}')
            code, said = self.init()
            self.assertEqual(code, init_tree.EXIT_REFUSED)
            self.assertIn(words, '\n'.join(said))
            self.assertFalse(self.target.exists())
            (self.prod / held).unlink()

    def test_a_continued_creation_keeps_the_results_it_copied_and_checks_them_against_its_record(self):
        self.init(answers=['YES'])
        copied = (self.target / 'source_data' / RESULT_NAMES[0]).read_bytes()
        fixtures.write_results(self.prod, 'POWERBALL', get_profile('POWERBALL').first_draw + 25, version=3)
        self.build_environment()
        code, said = self.init()
        self.assertEqual(code, init_tree.EXIT_CREATED, said)
        self.assertEqual((self.target / 'source_data' / RESULT_NAMES[0]).read_bytes(), copied)

    def test_a_copied_results_file_changed_before_the_second_run_stops_the_creation(self):
        self.init(answers=['YES'])
        path = self.target / 'source_data' / RESULT_NAMES[0]
        path.write_bytes(path.read_bytes() + b'9999,2099-01-01,1,2,3,4,5,6,7,8\n')
        self.build_environment()
        code, said = self.init()
        self.assertEqual(code, init_tree.EXIT_STOPPED)
        self.assertIn('are no longer what its record', '\n'.join(said))
        self.assertIsNotNone(common.read_barrier(self.target))


class AFailedCheckLeavesTheBarrier(CreationCase):
    """Steps 7 and 8: a failure stops the creation behind its barrier; the same command finishes it."""

    def stopped(self, pattern: str, **options) -> list:
        """Run the second run and expect it to stop with the barrier in place and nothing verified."""
        code, said = self.init(**options)
        self.assertEqual(code, init_tree.EXIT_STOPPED, said)
        self.assertRegex('\n'.join(said), pattern)
        self.assertIsNotNone(common.read_barrier(self.target))
        self.assertFalse((self.target / installed_files.LIST_PATH).exists())
        self.assertFalse((self.target / common.TREE_LOG_PATH).exists())
        self.assertFalse((self.target / 'records' / job_lock.JOB_LOCK_NAME).exists())
        self.assertFalse((self.target / job_lock.UPDATER_LOCK).exists())
        self.assertIn('stays in place, so no command works in that tree.', said[-1])
        return said

    def begun(self) -> None:
        """The first run and the environment."""
        self.assertEqual(self.init(answers=['YES'])[0], init_tree.EXIT_BUILD_THE_ENVIRONMENT)
        self.build_environment()

    def test_a_file_under_src_that_the_plan_does_not_hold(self):
        self.begun()
        stray = self.target / 'src' / 'stray.py'
        stray.write_bytes(b'# not installed\r\n')
        self.stopped(r'STOPPED: the tree\'s software is not what the plan says \(1 finding\(s\)\)')
        self.assertFalse((self.target / '.venv' / environment_marker.MARKER_NAME).exists())
        stray.unlink()
        self.assertEqual(self.init()[0], init_tree.EXIT_CREATED, 'the cause corrected, the same command finishes')

    def test_a_suite_that_fails(self):
        self.begun()
        with mock.patch.object(tree_checks, 'run_checks', side_effect=AssertionError('no check after a failed suite')):
            self.stopped('THE TEST SUITE FAILED: an invented suite.', suite=False)
        self.assertFalse((self.target / '.venv' / environment_marker.MARKER_NAME).exists())
        self.assertEqual(self.init()[0], init_tree.EXIT_CREATED)

    def test_a_variant_that_cannot_forecast_in_the_trees_environment(self):
        folder = fixtures.add_toy_variant(self.dev, FAMILY, 'TOY_BAD_V1', games=('POWERBALL',),
                                          behaviour={'fail_at': [fixtures.FIRST_TOY_TARGET]},
                                          helpers=(f'{FAMILY}/__init__.py',))
        from test_trees_readiness import bring_to_form
        bring_to_form(self.dev)
        self.write_results()
        install_readiness.mark_variant(self.dev, FAMILY, 'TOY_BAD_V1')
        self.assertTrue(folder.is_dir())
        self.begun()
        said = self.stopped(r'STOPPED: 1 smoke case\(s\) failed; the environment\'s marker was not written\.')
        self.assertIn(f'  {FAMILY}/TOY_BAD_V1 for POWERBALL: the smoke case failed', '\n'.join(said))
        self.assertFalse((self.target / '.venv' / environment_marker.MARKER_NAME).exists())
        self.assertTrue((self.target / 'scratch' / f'SMOKE_{FAMILY}_TOY_BAD_V1_POWERBALL').is_dir())

    def test_no_recovery_kit_is_asked_about_and_no_is_the_default(self):
        self.begun()
        said = self.stopped('THE RESTORE TOOL COULD NOT BE WRITTEN', kit=NO_KIT, answers=[''])
        self.assertIn('RECOVERY KIT NOT WRITTEN: the backup root cannot be written.', said)
        self.assertTrue((self.target / '.venv' / environment_marker.MARKER_NAME).exists(), 'the checks had passed')
        code, said = self.init(kit=NO_KIT, answers=['YES'])
        self.assertEqual(code, init_tree.EXIT_CREATED, said)
        record = json.loads((self.target / common.TREE_LOG_PATH).read_text(encoding='ascii'))
        self.assertFalse(record['recovery_kit'])

    def test_a_fault_at_each_place_is_followed_by_the_same_command_finishing_the_creation(self):
        early = ((common, 'carry_out'), (common, 'create_status_files'), (init_tree, 'copy_results'))
        late = ((common, 'software_differences'), (common, 'checks_with_target_python'), (common, 'finish'))
        for number, (module, name) in enumerate(early + late):
            root = self.target.parent / f'tree_{number}'
            self.add_entry_replacing('QA', root)
            self.target, self.backups = root, root.parent / (root.name + '_backups')
            fault = mock.patch.object(module, name, side_effect=OSError(f'an invented fault in {name}'))
            if (module, name) in early:
                with fault:
                    code, said = self.init(answers=['YES'])
            else:
                self.assertEqual(self.init(answers=['YES'])[0], init_tree.EXIT_BUILD_THE_ENVIRONMENT)
                self.build_environment(root)
                said = []
                with mock.patch.object(common, 'checks_with_target_python', checks_in_this_process), \
                        mock.patch.object(common, 'suite_if_it_is_the_trees', suite_that(True)), \
                        mock.patch.object(recovery_kit, 'build_kit', return_value=KIT), fault:
                    code = init_tree.main(['QA'], settings.read_dev_view(self.dev), say=said.append,
                                          ask=never_asked, now=self.clock)
            self.assertEqual(code, init_tree.EXIT_STOPPED, (name, said))
            self.assertIn(f'STOPPED: an invented fault in {name}', said)
            self.assertIsNotNone(common.read_barrier(root), name)
            self.assertFalse((root / 'records' / job_lock.JOB_LOCK_NAME).exists(), name)
            self.assertFalse((root / job_lock.UPDATER_LOCK).exists(), name)
            self.build_environment(root)
            code, said = self.init()
            self.assertEqual(code, init_tree.EXIT_CREATED, (name, said))
            self.assertEqual(installed_files.differences(root, installed_files.read_list(root)), [], name)

    def add_entry_replacing(self, role: str, root: Path) -> None:
        """Point DEV's entry for a role at another folder (as the owner would edit his file by hand)."""
        path = self.dev / 'ENVIRONMENT.ini'
        text = path.read_text(encoding='utf-8')
        path.write_text(text[:text.index(f'[{role}]')] if f'[{role}]' in text else text, encoding='utf-8')
        self.add_entry(role, root)


class TheLauncherAndTheCommandWord(unittest.TestCase):
    """Init_Tree.bat and deploy/deploy_command.py."""

    def test_the_launcher_runs_init_tree_with_devs_own_python_isolated(self):
        text = (REPOSITORY_ROOT / 'Init_Tree.bat').read_bytes().decode('ascii')
        self.assertIn('"%PY%" -I -B -u "%TOOL%" init-tree %*\r\nexit /b %ERRORLEVEL%\r\n', text)
        self.assertIn('set "TOOL=%ROOT%deploy\\deploy_command.py"', text)
        self.assertEqual(text.count('\n'), text.count('\r\n'), 'every line ends CRLF')

    def test_the_command_word_is_known_and_leads_to_the_command(self):
        source = (REPOSITORY_ROOT / 'deploy' / 'deploy_command.py').read_text(encoding='utf-8')
        self.assertIn("'init-tree'", source)
        self.assertIn('from init_tree import main as init_tree', source)

    def test_the_owners_four_environment_scripts_are_infrastructure_so_that_a_new_tree_holds_them(self):
        from research import code_identity
        manifest = code_identity.read_manifest(REPOSITORY_ROOT)
        for name in ('create_venv.bat', 'install_upgrade_dependencies_into_venv.bat', 'activate_venv.bat',
                     'deactivate_venv.bat'):
            self.assertEqual(manifest.get(name), 'other', name)


if __name__ == '__main__':
    unittest.main()
