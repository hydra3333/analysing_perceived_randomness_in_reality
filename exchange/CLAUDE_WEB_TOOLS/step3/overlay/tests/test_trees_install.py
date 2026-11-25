"""Tests of Install.bat (deploy/install.py): adding ready variants to a tree (build step 3, slice C, part C4).

What this file is for
    It shows, on invented trees in temporary folders, the eleven steps of deployment design section 5: what is
    added and what is left out, each with its reason; that nothing installed is changed; the one question with
    the backup's and the kit's results; the target reserved before anything is copied, also when a job began
    while the owner was deciding; the checks that stop an install behind its barrier; the ending; and that the
    same command typed again finishes an install that stopped anywhere.
    The start of the tree's own Python is stood in for here (the checks are made in this process).

Which of the project's own modules it uses
    deploy/install.py, deploy/install_common.py, deploy/recovery_kit.py, deploy/suite_on_copy.py;
    research.installed_files, research.job_lock, research.launch_guard, research.settings, research.status_file,
    research.tree_checks; the fixtures, and the invented DEV and creation of tests/test_trees_init.py.
"""
from __future__ import annotations

import contextlib
import json
import sys
import unittest
from datetime import timedelta
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import install                                               # noqa: E402  (after the path line above)
import install_common as common                              # noqa: E402
import install_readiness                                     # noqa: E402
import recovery_kit                                          # noqa: E402
import research_fixtures as fixtures                         # noqa: E402
import suite_on_copy                                         # noqa: E402
from research import installed_files, job_lock, launch_guard, settings, status_file, tree_checks    # noqa: E402
from test_trees_init import KIT, NO_KIT, CreationCase, checks_in_this_process, suite_that    # noqa: E402
from test_trees_install_common import FAMILY, FIRST, GAMES, METHODS, SECOND, sha, whole_tree    # noqa: E402
from test_trees_readiness import bring_to_form, write_crlf   # noqa: E402

THIRD = 'TOY_COUNTS_V3'


class InstallCase(CreationCase):
    """A created QA tree that holds DEV's first variant; DEV then gains more."""

    def setUp(self):
        """Create the QA tree."""
        super().setUp()
        self.created()
        read = iter(range(1, 10 ** 6))
        self.running = lambda: fixtures.FIXED_TIME + timedelta(minutes=next(read))

    def install(self, *words, answers=(), suite='passes', kit=KIT, ask=None) -> tuple:
        """Run the command for the QA tree; return (the exit code, the lines said).

        answers: what the owner types, in order; a question beyond them fails the test.  suite: 'passes' or
        'fails' for a stand-in, 'real' for the real decision whether the suite belongs to the tree.
        ask: a function to answer with in place of `answers`.
        """
        said, left = [], list(answers)

        def answer(prompt):
            """Give the next answer."""
            if not left:
                raise AssertionError(f'an unexpected question: {said[-3:]}')
            return left.pop(0)

        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(common, 'checks_with_target_python', checks_in_this_process))
            stack.enter_context(mock.patch.object(recovery_kit, 'build_kit', return_value=kit))
            if suite != 'real':
                stack.enter_context(mock.patch.object(common, 'suite_if_it_is_the_trees', suite_that(suite == 'passes')))
            code = install.main(['QA', *words], settings.read_dev_view(self.dev), say=said.append,
                                ask=ask or answer, now=self.running)
        self.assertEqual(left, [], 'every answer given was asked for')
        return code, said

    def software(self) -> dict:
        """The target's software and control files, without its backups' log."""
        return {path: digest for path, digest in whole_tree(self.target).items()
                if not path.startswith(('.venv/', 'records/SNAPSHOT'))}

    def variants_installed(self) -> list:
        """The names of the variants on the target's list of installed files."""
        return [entry['variant'] for entry in installed_files.read_list(self.target)['variants']]

    def backups_made(self) -> list:
        """The jobs of the backups in the target's backup root, oldest first."""
        return [path.name.split('_', 3)[3][:-4] for path in sorted(self.backups.glob('*.zip'))]


class AnInstallFromStartToEnd(InstallCase):
    """Deployment design section 5, in its order."""

    def test_nothing_to_add_ends_without_a_question_and_the_target_is_not_touched(self):
        before = whole_tree(self.target)
        code, said = self.install()
        self.assertEqual(code, install.EXIT_INSTALLED)
        self.assertIn(f'  left out: {FAMILY}/{FIRST}: already installed', said)
        self.assertIn('INSTALL - END - nothing to add', said[-1])
        self.assertEqual(whole_tree(self.target), before)
        self.assertEqual(self.backups_made(), ['INIT'])

    def test_a_new_variant_is_added_and_nothing_installed_is_changed(self):
        self.assertEqual(fixtures.run_job(self.target, games=('POWERBALL',))[0], 0)
        self.add_variant(SECOND)
        before = whole_tree(self.target)
        code, said = self.install(answers=['YES'])
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        after = whole_tree(self.target)
        new = f'{METHODS}/{FAMILY}/{SECOND}'
        added = sorted(path for path in after if path not in before and not path.startswith('records/'))
        self.assertEqual(added, [f'{new}/VARIANT.json', f'{new}/VARIANT_STATUS.ini', f'{new}/method.py'])
        for name in ('VARIANT.json', 'method.py'):
            self.assertEqual(after[f'{new}/{name}'], sha(self.dev / new / name))
        changed = sorted(path for path in before if after.get(path) != before[path])
        self.assertEqual(changed, ['records/INSTALLED_FILES.json', 'records/INSTALL_LOG.jsonl',
                                   'records/SNAPSHOT_LOG.jsonl'], 'no installed file and no result was changed')
        self.assertEqual(status_file.read_status(self.target / new / 'VARIANT_STATUS.ini', GAMES),
                         {game: status_file.GameStatus() for game in GAMES})
        self.assertEqual(self.variants_installed(), [FIRST, SECOND])
        content = installed_files.read_list(self.target)
        self.assertEqual(installed_files.differences(self.target, content), [])
        record = json.loads((self.target / common.TREE_LOG_PATH).read_text(encoding='ascii').splitlines()[-1])
        self.assertEqual((record['operation'], record['variants'], record['added'], record['suite']),
                         ('INSTALL', [f'{FAMILY}/{SECOND}'], 2, 'PASSED'))
        self.assertGreater(record['sample_compared'], 0, 'the stored forecasts of the first variant were sampled')
        self.assertIsNone(common.read_barrier(self.target))
        for lock in (self.target / 'records' / job_lock.JOB_LOCK_NAME, self.target / job_lock.UPDATER_LOCK):
            self.assertFalse(lock.exists())
        self.assertEqual(self.backups_made()[-2:], ['PRE_INSTALL', 'POST_INSTALL'])
        self.assertIn(f'INSTALL - END - installed into the QA tree: {FAMILY}/{SECOND}. Installation is release', said[-1])
        code, lines = fixtures.run_job(self.target, games=('POWERBALL',))
        self.assertEqual(code, 0, lines)
        self.assertGreater(len(fixtures.list_lines(self.target, FAMILY, SECOND)), 0,
                           'installation is release: the next job fills the new variant\'s history')

    def test_the_question_tells_the_backups_and_the_kits_results_and_comes_after_the_plan(self):
        self.add_variant(SECOND)
        code, said = self.install(answers=['YES'])
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        ask = said.index('Type YES to proceed. Anything else, Enter included, is NO.')
        self.assertTrue(said[ask - 2].startswith('The backup taken just now: BACKUP MADE AND VERIFIED: '))
        self.assertIn('_PRE_INSTALL.zip', said[ask - 2])
        self.assertEqual(said[ask - 1], f'The recovery kit: {KIT.line()}')
        plan = next(i for i, line in enumerate(said) if line.startswith('The plan (INSTALL into the QA tree'))
        self.assertLess(plan, ask)
        self.assertIn(f'  variant to add: {FAMILY}/{SECOND} (POWERBALL, OZLOTTO)', said[plan + 1])

    def test_no_or_enter_leaves_the_software_untouched_and_says_what_may_have_been_written(self):
        self.add_variant(SECOND)
        before = self.software()
        for answer in ('', 'NO', 'yes'):
            code, said = self.install(answers=[answer])
            self.assertEqual(code, install.EXIT_REFUSED)
            self.assertEqual(self.software(), before)
            self.assertIn('INSTALL - END - NO: the target\'s software was not touched.', said[-1])
        self.assertEqual(self.backups_made().count('PRE_INSTALL'), 3)

    def test_a_failed_backup_and_kit_are_said_in_capitals_and_yes_still_proceeds(self):
        self.add_variant(SECOND)
        refusal = common.snapshot.SnapshotResult(False, reason='the backup root cannot be written.')
        with mock.patch.object(common.snapshot, 'attempt_snapshot', return_value=refusal):
            code, said = self.install(answers=['YES'], kit=NO_KIT)
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        text = '\n'.join(said)
        self.assertIn('NO ROLLBACK POINT WAS CREATED BY THIS INSTALL.', text)
        self.assertIn('THE RESTORE TOOL COULD NOT BE WRITTEN', text)
        self.assertNotIn('PRE_INSTALL.zip', text, 'no text names a backup that was not made')


class WhatIsAddedAndWhatIsLeftOut(InstallCase):
    """Step 1: to add; left out, each with its reason; a helper with other bytes refuses."""

    def test_each_reason_for_leaving_a_variant_out_is_said(self):
        self.add_variant(SECOND, mark=False)
        third = self.add_variant(THIRD)
        (third / 'method.py').write_bytes((third / 'method.py').read_bytes() + b'# changed after marking\r\n')
        first = self.dev / METHODS / FAMILY / FIRST / 'method.py'
        first.write_bytes(first.read_bytes() + b'# changed in DEV after it was installed\r\n')
        install_readiness.mark_variant(self.dev, FAMILY, FIRST)
        before = whole_tree(self.target)
        code, said = self.install()
        self.assertEqual(code, install.EXIT_INSTALLED)
        text = '\n'.join(said)
        self.assertIn(f'  left out: {FAMILY}/{FIRST}: already installed with different bytes (an install leaves it '
                      f'alone: changed work needs a new variant name)', text)
        self.assertIn(f'  left out: {FAMILY}/{SECOND}: it is not marked.', text)
        self.assertIn(f'  left out: {FAMILY}/{THIRD}: its marker does not match its files', text)
        self.assertEqual(whole_tree(self.target), before)

    def test_only_narrows_the_install_to_the_variants_named(self):
        self.add_variant(SECOND)
        self.add_variant(THIRD)
        code, said = self.install('--only', f'{FAMILY}/{THIRD}', answers=['YES'])
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        self.assertEqual(self.variants_installed(), [FIRST, THIRD])
        self.assertIn('Narrowed by --only to 1 variant(s).', said)
        code, said = self.install('--only', f'{FAMILY}/{THIRD}', f'{FAMILY}/{FIRST}')
        self.assertEqual(code, install.EXIT_INSTALLED)
        self.assertIn('INSTALL - END - nothing to add', said[-1])

    def test_a_name_after_only_that_is_no_variant_of_dev_is_refused(self):
        code, said = self.install('--only', f'{FAMILY}/NOT_THERE_V1')
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertIn(f'REFUSED: --only names {FAMILY}/NOT_THERE_V1, which is no variant folder of DEV.', said[1])

    def test_a_helper_the_target_holds_with_other_bytes_refuses_and_names_the_way_on(self):
        helper = self.dev / METHODS / FAMILY / 'toy_helper_v1.py'
        self.add_variant(SECOND, mark=False)
        write_crlf(helper, '"""An invented helper, its idea changed."""\nLIMIT = 4\n')
        install_readiness.mark_variant(self.dev, FAMILY, SECOND)
        before, backups = whole_tree(self.target), self.backups_made()
        code, said = self.install()
        self.assertEqual(code, install.EXIT_REFUSED)
        text = '\n'.join(said)
        self.assertIn('holds 1 helper file(s) with other bytes than DEV\'s, and no install overwrites a helper', text)
        self.assertIn(f'{METHODS}/{FAMILY}/toy_helper_v1.py (listed by {FAMILY}/{SECOND})', text)
        self.assertIn('Correct_Shared_Code.bat', text)
        self.assertEqual((whole_tree(self.target), self.backups_made()), (before, backups))

    def test_a_helper_the_target_lacks_arrives_with_the_variant_that_lists_it(self):
        folder = fixtures.add_toy_variant(self.dev, FAMILY, SECOND, games=GAMES,
                                          helpers=(f'{FAMILY}/__init__.py', f'{FAMILY}/toy_helper_v2.py'))
        write_crlf(self.dev / METHODS / FAMILY / 'toy_helper_v2.py', '"""A second invented helper."""\nLIMIT = 5\n')
        bring_to_form(self.dev)
        self.write_results()
        install_readiness.mark_variant(self.dev, FAMILY, SECOND)
        self.assertTrue(folder.is_dir())
        code, said = self.install(answers=['YES'])
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        self.assertEqual((self.target / METHODS / FAMILY / 'toy_helper_v2.py').read_bytes(),
                         (self.dev / METHODS / FAMILY / 'toy_helper_v2.py').read_bytes())
        self.assertIn(f'  add: {METHODS}/{FAMILY}/toy_helper_v2.py', said)


class WhatIsRefusedBeforeAnythingIsCopied(InstallCase):
    """Steps 1, 2 and 6."""

    def test_a_tree_that_does_not_exist_or_is_not_what_dev_says(self):
        said = []
        code = install.main(['PROD'], settings.read_dev_view(self.dev), say=said.append, ask=None)
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertIn('has no section for the PROD tree', said[0])

    def test_software_changed_outside_the_tools_is_refused_before_any_backup(self):
        self.add_variant(SECOND)
        (self.target / 'src' / 'toy_other.py').write_bytes(b'# edited by hand\r\n')
        backups = self.backups_made()
        code, said = self.install()
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertIn('does not match its own list of installed files (1 difference(s))', '\n'.join(said))
        self.assertEqual(self.backups_made(), backups)

    def test_a_job_that_holds_the_lock_refuses_before_any_backup(self):
        self.add_variant(SECOND)
        before = self.software()
        with job_lock.job_lock(self.target, 'a research job', 'now'):
            code, said = self.install()
            self.assertEqual(code, install.EXIT_REFUSED)
            self.assertIn('REFUSED: a process of this tree is running', '\n'.join(said))
            self.assertEqual(self.backups_made(), ['INIT'])
        self.assertEqual(self.software(), before)

    def test_a_job_that_began_while_the_owner_was_deciding_refuses_at_the_reservation_and_nothing_was_copied(self):
        self.add_variant(SECOND)
        before = self.software()
        lock = self.target / 'records' / job_lock.JOB_LOCK_NAME

        def a_job_starts_then_yes(prompt):
            """While the owner reads the question, a research job takes the tree's lock."""
            lock.write_bytes(b'research job; started later; process 4242\r\n')
            return 'YES'

        code, said = self.install(ask=a_job_starts_then_yes)
        self.assertEqual(code, install.EXIT_REFUSED, said)
        self.assertIn('REFUSED: a process of this tree is running', '\n'.join(said))
        self.assertEqual(lock.read_bytes(), b'research job; started later; process 4242\r\n', 'nothing ends the job')
        lock.unlink()
        self.assertEqual(self.software(), before, 'no file was copied and no barrier was written')
        code, said = self.install(answers=['YES'])
        self.assertEqual(code, install.EXIT_INSTALLED, 'a second run on a quiet tree succeeds')

    def test_dev_changed_since_an_install_began_is_another_plan_and_both_are_shown(self):
        self.add_variant(SECOND)
        with mock.patch.object(common, 'software_differences', side_effect=OSError('an invented fault')):
            self.assertEqual(self.install(answers=['YES'])[0], install.EXIT_STOPPED)
        self.add_variant(THIRD)
        code, said = self.install()
        self.assertEqual(code, install.EXIT_REFUSED)
        text = '\n'.join(said)
        self.assertIn('holds another plan than the plan now', text)
        self.assertIn(f'  variant to add: {FAMILY}/{THIRD} (POWERBALL, OZLOTTO)', text.split('THE PLAN NOW:')[1])
        self.assertIsNotNone(common.read_barrier(self.target))


class AFailedCheckStopsBehindTheBarrier(InstallCase):
    """Steps 8 and 9: a failure stops here with the barrier in place, so no job runs."""

    def stopped(self, pattern: str, **options) -> list:
        """Install the second variant and expect a stop with the barrier in place and the old list kept."""
        code, said = self.install(answers=['YES'], **options)
        self.assertEqual(code, install.EXIT_STOPPED, said)
        self.assertRegex('\n'.join(said), pattern)
        self.assertIsNotNone(common.read_barrier(self.target))
        self.assertEqual(self.variants_installed(), [FIRST], 'the list is still the old one')
        for lock in (self.target / 'records' / job_lock.JOB_LOCK_NAME, self.target / job_lock.UPDATER_LOCK):
            self.assertFalse(lock.exists())
        with self.assertRaises(launch_guard.GuardRefused):
            launch_guard.check_no_unfinished_operation(self.target)
        self.assertIn('or restore the tree from a backup you choose.', said[-1])
        self.assertNotIn('POST_INSTALL', self.backups_made())
        return said

    def test_a_new_variant_that_cannot_forecast(self):
        fixtures.add_toy_variant(self.dev, FAMILY, 'TOY_BAD_V1', games=('POWERBALL',),
                                 behaviour={'fail_at': [fixtures.FIRST_TOY_TARGET]}, helpers=(f'{FAMILY}/__init__.py',))
        bring_to_form(self.dev)
        self.write_results()
        install_readiness.mark_variant(self.dev, FAMILY, 'TOY_BAD_V1')
        said = self.stopped(r'STOPPED: 1 finding\(s\) of the checks stop the install:')
        self.assertIn(f'  {FAMILY}/TOY_BAD_V1 for POWERBALL: the smoke case failed', '\n'.join(said))
        self.assertTrue((self.target / 'scratch' / f'SMOKE_{FAMILY}_TOY_BAD_V1_POWERBALL').is_dir())

    def test_only_the_new_variants_are_made_to_forecast(self):
        self.add_variant(SECOND)
        asked = []
        real = tree_checks.run_checks

        def noting(software_root, tree_settings, smoke, *rest):
            """Note which smoke cases were asked."""
            asked.append(smoke)
            return real(software_root, tree_settings, smoke, *rest)

        with mock.patch.object(tree_checks, 'run_checks', noting):
            self.assertEqual(self.install(answers=['YES'])[0], install.EXIT_INSTALLED)
        self.assertEqual(asked, [[f'{FAMILY}/{SECOND}']])

    def test_a_difference_in_the_forecast_sample(self):
        self.add_variant(SECOND)
        with mock.patch.object(tree_checks, 'forecast_sample',
                               return_value=(3, ['E_901/TOY_COUNTS_V1 for POWERBALL, draw 1150: not the same'])):
            said = self.stopped('draw 1150: not the same')
        self.assertIn('STOPPED: 1 finding(s) of the checks stop the install:', said)

    def test_an_unexpected_difference_in_the_derived_results_stops_and_a_known_one_does_not(self):
        self.add_variant(SECOND)
        answer = {'POWERBALL': (1160, 'the score of a variant is not what the installed code computes', False)}
        with mock.patch.object(tree_checks, 'derived_results', return_value=answer):
            self.stopped('POWERBALL: stored scores or OV-1 lines are not what the installed software computes, from '
                         'draw 1160')
        known = {'POWERBALL': (1160, 'the score of a variant is not what the installed code computes', True)}
        with mock.patch.object(tree_checks, 'derived_results', return_value=known):
            code, said = self.install()
        self.assertEqual(code, install.EXIT_INSTALLED, said)

    def test_a_suite_that_fails(self):
        self.add_variant(SECOND)
        self.stopped('STOPPED: the suite failed with the tree\'s own Python.', suite='fails')

    def test_a_file_under_src_that_is_neither_the_old_list_nor_the_plan(self):
        self.add_variant(SECOND)
        real = common.carry_out

        def copy_then_stray(dev_root, tree_root, plan, say=print):
            """Carry the plan out, then something else writes a file under src."""
            real(dev_root, tree_root, plan, say)
            (Path(tree_root) / 'src' / 'stray.py').write_bytes(b'#\r\n')

        with mock.patch.object(common, 'carry_out', copy_then_stray):
            self.stopped(r'STOPPED: the tree\'s software is not the old list and the plan together \(1 finding')


class TheSuiteBelongsToTheTreeOrIsNotRun(InstallCase):
    """Design 3.3 item 5 and specification 12.3 item 3."""

    def run_real_decision(self) -> tuple:
        """Install the second variant with the real decision, the suite itself replaced by one that must not run."""
        with mock.patch.object(suite_on_copy, 'run_suite', side_effect=AssertionError('it must not be run')):
            return self.install(answers=['YES'], suite='real')

    def test_when_devs_infrastructure_has_moved_on_the_suite_is_not_run_and_the_install_goes_on(self):
        self.add_variant(SECOND)
        (self.dev / 'src' / 'toy_other.py').write_bytes(b'# newer infrastructure in DEV\r\n')
        install_readiness.mark_infrastructure(self.dev)
        code, said = self.run_real_decision()
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        self.assertIn('The test suite: the tests in DEV are for newer code than this tree holds; not run (the tree '
                      'differs from DEV in: src/toy_other.py).', said)
        record = json.loads((self.target / common.TREE_LOG_PATH).read_text(encoding='ascii').splitlines()[-1])
        self.assertEqual(record['suite'], 'NOT RUN')

    def test_when_devs_infrastructure_is_not_marked_ready_the_suite_is_not_run_and_the_line_says_why(self):
        self.add_variant(SECOND)
        install_readiness.unmark_infrastructure(self.dev)
        code, said = self.run_real_decision()
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        self.assertIn('The test suite: not run. DEV\'s infrastructure is not marked ready', '\n'.join(said))

    def test_when_the_infrastructure_is_devs_the_suite_is_run_with_the_trees_python(self):
        self.add_variant(SECOND)
        result = suite_on_copy.SuiteResult(passed=True, modules=[('test_x', 0, 3)])
        with mock.patch.object(suite_on_copy, 'run_suite', return_value=result) as run:
            code, said = self.install(answers=['YES'], suite='real')
        self.assertEqual(code, install.EXIT_INSTALLED, said)
        self.assertEqual(run.call_args.args[:2], (self.dev, self.target / '.venv' / 'Scripts' / 'python.exe'))
        self.assertIn('THE TEST SUITE PASSED: 1 modules, 3 tests.', said)


class TheSameCommandAgainFinishesIt(InstallCase):
    """Deployment design section 8, first row."""

    def test_a_fault_at_each_place_is_followed_by_the_same_command_finishing_the_install(self):
        places = ((common, 'carry_out'), (common, 'create_status_files'), (common, 'software_differences'),
                  (common, 'checks_with_target_python'), (common, 'finish'), (common, 'remove_barrier'))
        for number, (module, name) in enumerate(places):
            variant = f'TOY_STEP_{number}_V1'
            self.add_variant(variant)
            said = []
            with mock.patch.object(common, 'checks_with_target_python', checks_in_this_process), \
                    mock.patch.object(common, 'suite_if_it_is_the_trees', suite_that(True)), \
                    mock.patch.object(recovery_kit, 'build_kit', return_value=KIT), \
                    mock.patch.object(module, name, side_effect=OSError(f'an invented fault in {name}')):
                code = install.main(['QA'], settings.read_dev_view(self.dev), say=said.append,
                                    ask=lambda prompt: 'YES', now=self.running)
            self.assertEqual(code, install.EXIT_STOPPED, (name, said))
            self.assertIn(f'STOPPED: an invented fault in {name}', said)
            self.assertIsNotNone(common.read_barrier(self.target), name)
            backups = self.backups_made()
            code, said = self.install()
            self.assertEqual(code, install.EXIT_INSTALLED, (name, said))
            self.assertIn('This same install was begun before and is being continued', '\n'.join(said))
            self.assertEqual(self.backups_made(), backups + ['POST_INSTALL'], 'no new backup before; one after')
            self.assertIn(variant, self.variants_installed(), name)
            self.assertIsNone(common.read_barrier(self.target), name)
            content = installed_files.read_list(self.target)
            self.assertEqual(installed_files.differences(self.target, content), [], name)
            self.assertEqual(content, installed_files.software_now(self.target), name)

    def test_the_list_as_it_was_before_is_worked_out_when_the_stop_came_after_the_list_was_written(self):
        current = installed_files.read_list(self.target)
        self.add_variant(SECOND)
        ready, _ = common.dev_variants(self.dev)
        entry = ready[f'{FAMILY}/{SECOND}']
        own = {path: digest for path, digest in entry['files'].items() if SECOND in path}
        plan = common.make_plan(common.INSTALL, 'QA', self.target, own, variants=[entry])
        after = common.expected_list(current, plan)
        self.assertEqual(install.list_before(after, plan), current)
        self.assertEqual(install.list_before(current, plan), current, 'and a list not yet written is left as it is')
        self.assertEqual(install.list_before(after, None), after)
        other = dict(plan, operation=common.REINSTALL_INFRA)
        self.assertEqual(install.list_before(after, other), after, 'only an install\'s own barrier is undone')


class TheLauncherAndTheCommandWord(unittest.TestCase):
    """Install.bat and deploy/deploy_command.py."""

    def test_the_launcher_runs_install_with_devs_own_python_isolated(self):
        text = (REPOSITORY_ROOT / 'Install.bat').read_bytes().decode('ascii')
        self.assertIn('"%PY%" -I -B -u "%TOOL%" install %*\r\nexit /b %ERRORLEVEL%\r\n', text)
        self.assertEqual(text.count('\n'), text.count('\r\n'), 'every line ends CRLF')
        self.assertIn('rem        Install.bat PROD --only E_002/RECUR_MEAN_ALL_V1 E_002/RECUR_MEDIAN_ALL_V1', text)

    def test_the_command_word_is_known_and_leads_to_the_command(self):
        source = (REPOSITORY_ROOT / 'deploy' / 'deploy_command.py').read_text(encoding='utf-8')
        self.assertIn("'install'", source)
        self.assertIn('from install import main as install', source)


if __name__ == '__main__':
    unittest.main()
