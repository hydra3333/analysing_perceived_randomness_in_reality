"""Tests of Reinstall_Infra.bat (deploy/reinstall_infra.py): bringing a tree's infrastructure to DEV's (build step 3,
slice C, part C5).

What this file is for
    It shows, on invented trees in temporary folders, the eleven steps of deployment design section 6 and
    specification 12.4: the plan with each file's class, hashes and differences; that a plan touching code that
    makes forecasts is refused; the two statements, each from a planted change, found before anything is
    overwritten; the warning and the one question; that an accepted change of derived results leaves the tree
    marked not current, with no report of agreement; that the print-outs are made again when their code changes;
    that a failure in place leaves the barrier; and the three ways on: the same command, `--replace-unfinished`,
    or (the owner's own) a restore.
    The start of the tree's own Python is stood in for here (the checks are made in this process).

Which of the project's own modules it uses
    deploy/reinstall_infra.py, deploy/install_common.py, deploy/recovery_kit.py; research.derived_check,
    research.installed_files, research.job_lock, research.launch_guard, research.settings, research.tree_checks;
    the fixtures, and the created tree of tests/test_trees_install.py.
"""
from __future__ import annotations

import contextlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import install_common as common                              # noqa: E402  (after the path line above)
import install_readiness                                     # noqa: E402
import recovery_kit                                          # noqa: E402
import reinstall_infra as reinstall                          # noqa: E402
import research_fixtures as fixtures                         # noqa: E402
from research import derived_check, installed_files, job_lock, launch_guard, settings, tree_checks    # noqa: E402
from test_trees_init import KIT, checks_in_this_process      # noqa: E402
from test_trees_install import InstallCase                   # noqa: E402
from test_trees_install_common import FAMILY, sha, whole_tree    # noqa: E402

GAME = 'POWERBALL'
OTHER, DERIVED, FORECAST = 'src/toy_other.py', 'src/toy_derived_code.py', 'src/toy_forecast_code.py'
FORETOLD = 1158


def reports_in_this_process(python, tree_root, say=print, run=None) -> None:
    """A stand-in for the start of the tree's own Python on the reports command: the same work, done here."""
    with fixtures.ImportPath(Path(tree_root)):
        assert tree_checks.reports_main(['--data', str(tree_root)], Path(tree_root), say=say) == 0


def changed_from(draw: int, at_call: int = 1):
    """A stand-in for the comparison of the derived results: from its `at_call`-th call on it finds that the
    test game's stored results are not what the software computes from `draw`, known if the tree marks it."""
    calls = []

    def derived(stored, say=print):
        """Answer as told."""
        calls.append(True)
        answers = {game_id: None for game_id in stored}
        if len(calls) >= at_call and GAME in stored:
            marked = stored[GAME].cutoff
            known = marked is not None and marked[1] == derived_check.MISMATCH and marked[0] <= draw
            answers[GAME] = (draw, 'an invented difference in a score', known)
        return answers
    return derived


class ReinstallCase(InstallCase):
    """A created QA tree whose job has run, so that it holds forecasts, scores, a ledger and reports."""

    def setUp(self):
        """Create the tree and run its job."""
        super().setUp()
        code, said = fixtures.run_job(self.target, games=(GAME,))
        self.assertEqual(code, 0, said)

    def change_in_dev(self, relative: str, text: str = '# changed in DEV\n') -> None:
        """Change one infrastructure file of DEV and mark the infrastructure ready again."""
        (self.dev / relative).write_bytes(text.replace('\n', '\r\n').encode('ascii'))
        install_readiness.mark_infrastructure(self.dev)

    def manifest_in_dev(self, change) -> None:
        """Rewrite DEV's manifest through `change` (text to text) and mark the infrastructure ready again."""
        path = self.dev / 'deploy' / 'INFRA_MANIFEST.ini'
        path.write_bytes(change(path.read_bytes().decode('ascii').replace('\r\n', '\n')).replace('\n', '\r\n')
                         .encode('ascii'))
        install_readiness.mark_infrastructure(self.dev)

    def reinstall(self, *words, answers=(), suites=(True, True), kit=KIT, derived=None) -> tuple:
        """Run the command for the QA tree; return (the exit code, the lines said).

        answers: what the owner types, in order.  suites: what the suite answers at each time it is run.
        derived: a stand-in for the comparison of the derived results, or None for the real one.
        """
        said, left, verdicts = [], list(answers), list(suites)

        def answer(prompt):
            """Give the next answer."""
            if not left:
                raise AssertionError(f'an unexpected question: {said[-3:]}')
            return left.pop(0)

        def suite(dev_root, dev_files, installed, python, say=print):
            """Answer the next verdict, for software whose infrastructure is DEV's."""
            assert common.infrastructure_differences(dev_files, installed) == []
            passed = verdicts.pop(0)
            return passed, f'THE TEST SUITE {"PASSED" if passed else "FAILED"}: an invented suite.'

        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(common, 'checks_with_target_python', checks_in_this_process))
            stack.enter_context(mock.patch.object(common, 'reports_with_target_python', reports_in_this_process))
            stack.enter_context(mock.patch.object(common, 'suite_if_it_is_the_trees', suite))
            stack.enter_context(mock.patch.object(recovery_kit, 'build_kit', return_value=kit))
            if derived is not None:
                stack.enter_context(mock.patch.object(tree_checks, 'derived_results', derived))
            code = reinstall.main(['QA', *words], settings.read_dev_view(self.dev), say=said.append, ask=answer,
                                  now=self.running)
        self.assertEqual(left, [], 'every answer given was asked for')
        return code, said

    def infrastructure_is_devs(self) -> None:
        """Assert that the tree is whole and its infrastructure is file for file DEV's."""
        content = installed_files.read_list(self.target)
        self.assertEqual(installed_files.differences(self.target, content), [])
        self.assertEqual(content, installed_files.software_now(self.target))
        self.assertEqual(common.infrastructure_differences(common.dev_infrastructure(self.dev)['files'], content), [])
        self.assertIsNone(common.read_barrier(self.target))
        for lock in (self.target / 'records' / job_lock.JOB_LOCK_NAME, self.target / job_lock.UPDATER_LOCK):
            self.assertFalse(lock.exists())

    def last_log(self) -> dict:
        """The last line of the tree's log."""
        return json.loads((self.target / common.TREE_LOG_PATH).read_text(encoding='ascii').splitlines()[-1])


class AReinstallFromStartToEnd(ReinstallCase):
    """Deployment design section 6, in its order."""

    def test_no_difference_ends_without_a_question_and_nothing_is_done(self):
        before = whole_tree(self.target)
        code, said = self.reinstall(suites=())
        self.assertEqual(code, reinstall.EXIT_REINSTALLED)
        self.assertIn('REINSTALL INFRA - END - no difference', said[-1])
        self.assertEqual(whole_tree(self.target), before)

    def test_a_changed_file_that_can_change_no_result_is_overwritten_and_nothing_else_is_touched(self):
        self.change_in_dev(OTHER)
        before = whole_tree(self.target)
        with mock.patch.object(common, 'reports_with_target_python', side_effect=AssertionError('no report code changed')):
            code, said = self.reinstall(answers=['YES'])
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        after = whole_tree(self.target)
        changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
        self.assertEqual(changed, ['records/INSTALLED_FILES.json', 'records/INSTALL_LOG.jsonl',
                                   'records/SNAPSHOT_LOG.jsonl', OTHER],
                         'the one file of the plan and the tree\'s own records; no variant, list or result')
        self.assertEqual(after[OTHER], sha(self.dev / OTHER))
        self.infrastructure_is_devs()
        record = self.last_log()
        self.assertEqual((record['operation'], record['overwritten'], record['statement']['text'], record['suite']),
                         ('REINSTALL_INFRA', 1, reinstall.NO_CHANGE, 'PASSED'))
        self.assertEqual(self.backups_made()[-2:], ['PRE_INFRA', 'POST_INFRA'])
        self.assertIn(f'REINSTALL INFRA - END - the QA tree\'s infrastructure is DEV\'s. {reinstall.NO_CHANGE}', said[-1])
        self.assertEqual(fixtures.run_job(self.target, games=(GAME,))[0], 0, 'and the job runs afterwards')

    def test_the_plan_shows_class_both_hashes_and_the_differences_and_comes_before_the_statement_and_the_question(self):
        old = sha(self.target / OTHER)
        self.change_in_dev(OTHER)
        _, said = self.reinstall(answers=['YES'])
        plan = said.index(f'The plan (REINSTALL_INFRA into the QA tree at {self.target}): 0 file(s) to add, 1 to '
                          f'overwrite, 0 to remove.')
        self.assertEqual(said[plan + 1], f'  overwrite: {OTHER} (class other; now {old}; to be {sha(self.dev / OTHER)})')
        self.assertIn('      -# a launcher', said)
        self.assertIn('      +# changed in DEV', said)
        statement = said.index(f'THE STATEMENT: {reinstall.NO_CHANGE}')
        question = said.index('Type YES to proceed. Anything else, Enter included, is NO.')
        warning = next(i for i, line in enumerate(said) if line.startswith('This overwrites installed system files in '
                                                                           f'QA {self.target}. Make sure you hold'))
        self.assertTrue(plan < statement < warning < question)
        self.assertIn('there is no automatic rollback', said[warning])
        self.assertTrue(said[warning + 1].startswith('The backup taken just now: BACKUP MADE AND VERIFIED: '))
        self.assertIn('_PRE_INFRA.zip', said[warning + 1])

    def test_the_updaters_lock_is_let_go_before_the_barrier_is_removed_and_the_job_lock_after_it(self):
        self.change_in_dev(OTHER)
        seen, real = {}, common.remove_barrier

        def look_then_remove(tree_root):
            """Note what is still held at the moment the barrier is removed."""
            seen['updater lock'] = (self.target / job_lock.UPDATER_LOCK).exists()
            seen['job lock'] = (self.target / 'records' / job_lock.JOB_LOCK_NAME).exists()
            real(tree_root)

        with mock.patch.object(common, 'remove_barrier', look_then_remove):
            self.assertEqual(self.reinstall(answers=['YES'])[0], reinstall.EXIT_REINSTALLED)
        self.assertEqual(seen, {'updater lock': False, 'job lock': True})

    def test_no_or_enter_overwrites_nothing(self):
        self.change_in_dev(OTHER)
        before = self.software()
        for answer in ('', 'NO', 'yes'):
            code, said = self.reinstall(answers=[answer], suites=(True,))
            self.assertEqual(code, reinstall.EXIT_REFUSED)
            self.assertEqual(self.software(), before)
            self.assertIn('REINSTALL INFRA - END - NO: nothing was overwritten.', said[-1])

    def test_a_file_is_added_and_another_removed_and_removals_come_last(self):
        (self.dev / 'src' / 'toy_new.py').write_bytes(b'# a new infrastructure file\r\n')
        (self.dev / OTHER).unlink()
        self.manifest_in_dev(lambda text: text.replace('src/toy_other.py = other\n', 'src/toy_new.py = other\n'))
        code, said = self.reinstall(answers=['YES'])
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        self.assertTrue((self.target / 'src' / 'toy_new.py').is_file())
        self.assertFalse((self.target / OTHER).exists())
        self.infrastructure_is_devs()
        text = '\n'.join(said)
        self.assertIn('  add: src/toy_new.py (class other; ', text)
        self.assertIn(f'  remove: {OTHER} (class other; now ', text)
        self.assertIn('  overwrite: deploy/INFRA_MANIFEST.ini (class the manifest; ', text)


class CodeThatMakesForecastsIsNeverChanged(ReinstallCase):
    """Specification 12.4 (EX_267 R6-F01): a plan holding any forecast-class file is refused."""

    def refused(self, pattern: str) -> None:
        """Expect the refusal, before any backup, with the tree as it was."""
        before, backups = whole_tree(self.target), self.backups_made()
        code, said = self.reinstall(suites=())
        self.assertEqual(code, reinstall.EXIT_REFUSED, said)
        self.assertRegex('\n'.join(said), pattern)
        self.assertEqual((whole_tree(self.target), self.backups_made()), (before, backups))

    def test_a_changed_forecast_file(self):
        self.change_in_dev(FORECAST)
        self.refused('REFUSED: this changes code that makes forecasts; that is a correction of shared code: '
                     f'Correct_Shared_Code.bat. .*1 file\\(s\\) of class forecast: {FORECAST}')

    def test_a_forecast_file_added_or_removed(self):
        (self.dev / 'src' / 'toy_more.py').write_bytes(b'# more forecasting code\r\n')
        self.manifest_in_dev(lambda text: text + 'src/toy_more.py = forecast\n')
        self.refused('of class forecast: src/toy_more.py')
        (self.dev / 'src' / 'toy_more.py').unlink()
        (self.dev / FORECAST).unlink()
        self.manifest_in_dev(lambda text: text.replace('src/toy_more.py = forecast\n', '')
                             .replace('src/toy_forecast_code.py = forecast\n', ''))
        self.refused(f'of class forecast: {FORECAST}')

    def test_a_file_moved_into_or_out_of_the_forecast_class_with_its_bytes_unchanged(self):
        self.manifest_in_dev(lambda text: text.replace('src/toy_other.py = other', 'src/toy_other.py = forecast'))
        self.refused(f'do not class the same files as forecast \\(they differ on {OTHER}\\)')

    def test_a_path_under_a_family_folder_is_never_infrastructure(self):
        self.manifest_in_dev(lambda text: text + f'src/methods/{FAMILY}/__init__.py = other\n')
        self.refused(f'under a family folder or _shared, which belong to variants.*src/methods/{FAMILY}/__init__.py')


class TheTwoStatements(ReinstallCase):
    """Specification 12.4 and 5.8: what it would change is found and said before anything is overwritten."""

    def reports_folder(self) -> Path:
        """The test game's active reports folder."""
        return self.target / 'results' / 'research' / GAME / 'reports'

    def test_no_stored_result_changes_is_said_when_nothing_differs_and_the_tree_is_not_marked(self):
        self.change_in_dev(DERIVED)
        code, said = self.reinstall(answers=['YES'])
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        self.assertIn(f'THE STATEMENT: {reinstall.NO_CHANGE}', said)
        self.assertIsNone(derived_check.read_cutoff(self.target, GAME))
        self.assertNotIn('YOU NOW OWE', '\n'.join(said))

    def test_a_change_from_a_draw_is_foretold_before_the_question_and_nothing_is_marked_on_no(self):
        self.change_in_dev(DERIVED)
        before = self.software()
        code, said = self.reinstall(answers=['NO'], suites=(True,), derived=changed_from(FORETOLD))
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        statement = next(line for line in said if line.startswith('THE STATEMENT: '))
        self.assertEqual(statement, f'THE STATEMENT: This changes stored scores or OV-1 lines, for {GAME} from draw '
                                    f'{FORETOLD}. It is a scientific correction to derived results. Stored forecasts '
                                    f'are not affected. If you install it, those scores, reports and the prevailing '
                                    f'line will be not current from that draw until you run the derived-only rerun.')
        self.assertLess(said.index(statement), said.index('Type YES to proceed. Anything else, Enter included, is NO.'))
        self.assertEqual(self.software(), before)
        self.assertIsNone(derived_check.read_cutoff(self.target, GAME))

    def test_an_accepted_change_leaves_the_tree_marked_not_current_and_names_the_rerun_owed(self):
        self.change_in_dev(DERIVED)
        lists = {path: digest for path, digest in whole_tree(self.target).items()
                 if '/variants/' in path or path.endswith('ov1_prevailing.jsonl')}
        code, said = self.reinstall(answers=['YES'], derived=changed_from(FORETOLD))
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        draw, reason, detail = derived_check.read_cutoff(self.target, GAME)
        self.assertEqual((draw, reason, detail), (FORETOLD, derived_check.MISMATCH, 'an invented difference in a score'))
        active = sorted(path.name for path in self.reports_folder().rglob('*')
                        if path.is_file() and 'not_current' not in path.parts)
        self.assertFalse([name for name in active if f'd0{FORETOLD}' in name or f'd0{FORETOLD + 1}' in name], active)
        self.assertTrue(any(f'd0{FORETOLD - 1}' in name for name in active), 'the draws before it are still in view')
        self.assertTrue(any(f'd0{FORETOLD}' in path.name
                            for path in (self.reports_folder() / 'not_current').rglob('*')))
        text = '\n'.join(said)
        self.assertIn(f'  {GAME}: marked not current from draw {FORETOLD}, as was foretold and accepted;', text)
        self.assertIn(f'YOU NOW OWE {GAME} A RERUN: Rerun_Walk_Forward.bat --game {GAME} --from {FORETOLD} '
                      f'--derived-only.', text)
        self.assertNotIn(reinstall.NO_CHANGE, text, 'it never reports agreement that does not exist')
        self.assertEqual(self.last_log()['statement']['not_current_from'], {GAME: FORETOLD})
        self.assertEqual({path: digest for path, digest in whole_tree(self.target).items()
                          if '/variants/' in path or path.endswith('ov1_prevailing.jsonl')}, lists,
                         'no stored forecast, score or prevailing line was altered: nothing is recomputed')
        self.infrastructure_is_devs()

    def test_a_tree_that_already_marks_the_game_is_told_so_and_is_not_marked_again(self):
        derived_check.write_cutoff(self.target, GAME, FORETOLD - 2, derived_check.MISMATCH, 'marked earlier')
        self.change_in_dev(DERIVED)
        code, said = self.reinstall(answers=['YES'], derived=changed_from(FORETOLD))
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        self.assertIn(f'THE STATEMENT: {reinstall.NO_CHANGE} ({GAME}\'s results are already marked not current in '
                      f'this tree; that stands.)', said)
        self.assertEqual(derived_check.read_cutoff(self.target, GAME)[:2], (FORETOLD - 2, derived_check.MISMATCH))

    def test_a_difference_in_the_forecast_sample_is_a_wrongly_classed_file_and_stops_before_any_backup(self):
        self.change_in_dev(OTHER)
        before, backups = self.software(), self.backups_made()
        with mock.patch.object(tree_checks, 'forecast_sample',
                               return_value=(3, ['E_901/TOY_COUNTS_V1 for POWERBALL, draw 1150: not the same'])):
            code, said = self.reinstall(suites=(True,))
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        text = '\n'.join(said)
        self.assertIn('No forecasting code is in the plan, so a file is wrongly classed on the manifest.', text)
        self.assertIn('draw 1150: not the same', text)
        self.assertEqual((self.software(), self.backups_made()), (before, backups))

    def test_the_software_as_it_would_be_is_asked_about_the_trees_data_and_the_tree_is_not_written(self):
        self.change_in_dev(DERIVED)
        asked = []
        real = tree_checks.run_checks

        def noting(software_root, tree_settings, smoke, sample, derived, *rest):
            """Note what was asked of which software, and whether it was DEV's file that was asked."""
            asked.append((Path(software_root) == self.target, smoke, sample, derived,
                          (Path(software_root) / DERIVED).read_bytes() == (self.dev / DERIVED).read_bytes()))
            return real(software_root, tree_settings, smoke, sample, derived, *rest)

        with mock.patch.object(tree_checks, 'run_checks', noting):
            code, _ = self.reinstall(answers=['NO'], suites=(True,))
        self.assertEqual(asked, [(False, None, True, True, True)],
                         'a folder that is not the tree; no smoke case; the sample and the derived results; DEV\'s code')
        self.assertFalse((self.target / 'scratch').exists() and list((self.target / 'scratch').iterdir()))

    def test_the_folder_the_software_was_assembled_in_is_gone_afterwards_whatever_the_answer(self):
        import tempfile
        self.change_in_dev(OTHER)
        made, real = [], tempfile.mkdtemp

        def noting(*arguments, **options):
            """Note every temporary folder that is made."""
            made.append(Path(real(*arguments, **options)))
            return str(made[-1])

        with mock.patch.object(reinstall.tempfile, 'mkdtemp', noting):
            self.reinstall(answers=['NO'], suites=(True,))
            self.reinstall(answers=['YES'])
        assembled = [folder for folder in made if folder.name.startswith(reinstall.ASSEMBLY_PREFIX)]
        self.assertEqual(len(assembled), 2)
        self.assertEqual([folder for folder in assembled if folder.exists()], [])
        self.assertNotIn(self.target, [parent for folder in assembled for parent in folder.parents],
                         'and it never lay in the tree')

    def test_a_mark_the_tree_already_holds_from_an_earlier_draw_is_never_moved_to_a_later_one(self):
        derived_check.write_cutoff(self.target, GAME, FORETOLD - 2, derived_check.MISMATCH, 'marked earlier')
        statement = {'text': 'x', 'not_current_from': {GAME: FORETOLD}, 'detail': {GAME: 'foretold'}}
        self.assertEqual(reinstall.mark_not_current(self.target, statement, say=lambda line: None), [])
        self.assertEqual(derived_check.read_cutoff(self.target, GAME),
                         (FORETOLD - 2, derived_check.MISMATCH, 'marked earlier'))
        derived_check.write_cutoff(self.target, GAME, FORETOLD + 1, derived_check.MISMATCH, 'marked later')
        reinstall.mark_not_current(self.target, statement, say=lambda line: None)
        self.assertEqual(derived_check.read_cutoff(self.target, GAME)[:2], (FORETOLD, derived_check.MISMATCH),
                         'a later mark is brought down to the draw foretold')

    def test_a_suite_that_fails_on_the_software_as_it_would_be_stops_before_any_backup(self):
        self.change_in_dev(OTHER)
        before, backups = self.software(), self.backups_made()
        code, said = self.reinstall(suites=(False,))
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        self.assertIn('REFUSED: the suite does not pass with the target\'s Python on the software as it would be.',
                      '\n'.join(said))
        self.assertEqual((self.software(), self.backups_made()), (before, backups))


class ThePrintOutsAreMadeAgainWhenTheirCodeChanges(ReinstallCase):
    """Specification 12.4 (EX_269 R7-F02)."""

    def test_after_a_derived_class_change_no_file_made_by_old_report_code_is_left_in_view(self):
        league = sorted((self.target / 'results' / 'research' / GAME / 'reports' / 'league').glob('*.txt'))[0]
        wanted = league.read_bytes()
        league.write_bytes(b'a report as old report code made it\r\n')
        self.change_in_dev(DERIVED)
        code, said = self.reinstall(answers=['YES'])
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        self.assertEqual(league.read_bytes(), wanted)
        self.assertIn('Report or scoring code changed: every league report, next-draw report and OV-1 print-out is '
                      'made again with the new code.', said)

    def test_it_is_done_before_the_barrier_is_removed(self):
        self.change_in_dev(DERIVED)
        seen = []

        def reports(python, tree_root, say=print, run=None):
            """Note whether the barrier is still in place when the reports are made."""
            seen.append(common.read_barrier(tree_root) is not None)

        said = []
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(common, 'checks_with_target_python', checks_in_this_process))
            stack.enter_context(mock.patch.object(common, 'reports_with_target_python', reports))
            stack.enter_context(mock.patch.object(common, 'suite_if_it_is_the_trees',
                                                  lambda *a, **k: (True, 'THE TEST SUITE PASSED: invented.')))
            stack.enter_context(mock.patch.object(recovery_kit, 'build_kit', return_value=KIT))
            code = reinstall.main(['QA'], settings.read_dev_view(self.dev), say=said.append,
                                  ask=lambda prompt: 'YES', now=self.running)
        self.assertEqual((code, seen), (reinstall.EXIT_REINSTALLED, [True]), said)


class AFailureInPlaceLeavesTheBarrier(ReinstallCase):
    """Deployment design section 6, after its table, and section 8."""

    def stopped(self, pattern: str, **options) -> list:
        """Reinstall with YES and expect a stop with the barrier in place, the old list kept and no lock left."""
        old = installed_files.read_list(self.target)
        code, said = self.reinstall(answers=['YES'], **options)
        self.assertEqual(code, reinstall.EXIT_STOPPED, said)
        self.assertRegex('\n'.join(said), pattern)
        self.assertEqual(common.read_barrier(self.target)['operation'], 'REINSTALL_INFRA')
        self.assertEqual(installed_files.read_list(self.target), old)
        for lock in (self.target / 'records' / job_lock.JOB_LOCK_NAME, self.target / job_lock.UPDATER_LOCK):
            self.assertFalse(lock.exists())
        with self.assertRaises(launch_guard.GuardRefused):
            launch_guard.check_no_unfinished_operation(self.target)
        self.assertIn('--replace-unfinished; or restore the whole tree from a backup you choose.', said[-1])
        self.assertNotIn('POST_INFRA', self.backups_made())
        return said

    def test_a_suite_that_fails_in_place(self):
        self.change_in_dev(OTHER)
        self.stopped('STOPPED: the suite does not pass in place with the tree\'s own Python.', suites=(True, False))

    def test_a_derived_difference_in_place_that_was_not_foretold_is_never_reported_as_agreement(self):
        self.change_in_dev(DERIVED)
        said = self.stopped('STOPPED: 1 finding\\(s\\) in place. Nothing is reported as agreeing that does not agree:',
                            derived=changed_from(FORETOLD, at_call=2))
        self.assertIn(f'THE STATEMENT: {reinstall.NO_CHANGE}', said, 'what was foretold')
        self.assertIsNone(derived_check.read_cutoff(self.target, GAME), 'and the reinstall marks nothing by itself')

    def test_the_same_command_again_finishes_it_with_no_question_once_the_cause_is_gone(self):
        self.change_in_dev(OTHER)
        self.stopped('the suite does not pass in place', suites=(True, False))
        backups = self.backups_made()
        code, said = self.reinstall(suites=(True,))
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        self.assertIn('This same reinstall was begun before and is being continued', '\n'.join(said))
        self.assertIn(f'Its statement, accepted then, was: {reinstall.NO_CHANGE}', '\n'.join(said))
        self.assertEqual(self.backups_made(), backups + ['POST_INFRA'])
        self.infrastructure_is_devs()

    def test_dev_corrected_since_is_another_plan_refused_with_both_shown_and_the_way_on_named(self):
        self.change_in_dev(OTHER)
        self.stopped('the suite does not pass in place', suites=(True, False))
        self.change_in_dev(OTHER, '# corrected in DEV\n')
        before = self.software()
        code, said = self.reinstall(suites=())
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        text = '\n'.join(said)
        self.assertIn('holds another plan than the plan now', text)
        self.assertIn('Reinstall_Infra.bat QA --replace-unfinished goes on with the plan now, after the same question.',
                      text)
        self.assertEqual(self.software(), before)

    def test_replace_unfinished_shows_both_plans_asks_again_and_brings_the_tree_to_dev_as_it_is_now(self):
        (self.dev / 'src' / 'toy_new.py').write_bytes(b'# a new infrastructure file\r\n')
        self.manifest_in_dev(lambda text: text + 'src/toy_new.py = other\n')
        self.change_in_dev(OTHER)
        self.stopped('the suite does not pass in place', suites=(True, False))
        self.assertTrue((self.target / 'src' / 'toy_new.py').is_file(), 'the first plan was carried out')
        (self.dev / 'src' / 'toy_new.py').unlink()
        self.manifest_in_dev(lambda text: text.replace('src/toy_new.py = other\n', ''))
        self.change_in_dev(OTHER, '# corrected in DEV\n')
        code, said = self.reinstall('--replace-unfinished', answers=['YES'])
        self.assertEqual(code, reinstall.EXIT_REINSTALLED, said)
        text = '\n'.join(said)
        self.assertIn('AN UNFINISHED REINSTALL IS BEING REPLACED (--replace-unfinished). THE UNFINISHED PLAN:', text)
        self.assertIn('THE PLAN NOW, worked out from the files as they lie in the tree:', text)
        self.assertIn('  remove: src/toy_new.py (class other; now ', text)
        self.assertIn('Type YES to proceed. Anything else, Enter included, is NO.', said)
        self.assertFalse((self.target / 'src' / 'toy_new.py').exists(), 'what the replaced plan added is gone')
        self.assertEqual((self.target / OTHER).read_bytes(), b'# corrected in DEV\r\n')
        self.infrastructure_is_devs()

    def test_replace_unfinished_answered_no_leaves_the_unfinished_reinstall_as_it_was(self):
        self.change_in_dev(OTHER)
        self.stopped('the suite does not pass in place', suites=(True, False))
        unfinished = common.read_barrier(self.target)
        self.change_in_dev(OTHER, '# corrected in DEV\n')
        before = self.software()
        code, _ = self.reinstall('--replace-unfinished', answers=['NO'], suites=(True,))
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        self.assertEqual((self.software(), common.read_barrier(self.target)), (before, unfinished))

    def test_a_fault_at_each_place_is_followed_by_the_same_command_finishing_the_reinstall(self):
        places = ((common, 'carry_out'), (common, 'software_differences'), (reinstall, 'mark_not_current'),
                  (common, 'finish'), (common, 'remove_barrier'))
        for number, (module, name) in enumerate(places):
            self.change_in_dev(OTHER, f'# change number {number}\n')
            with mock.patch.object(module, name, side_effect=OSError(f'an invented fault in {name}')):
                code, said = self.reinstall(answers=['YES'], suites=(True, True)[:1 if name in (
                    'carry_out', 'software_differences', 'mark_not_current') else 2])
            self.assertEqual(code, reinstall.EXIT_STOPPED, (name, said))
            self.assertIn(f'STOPPED: an invented fault in {name}', said)
            self.assertIsNotNone(common.read_barrier(self.target), name)
            code, said = self.reinstall(suites=(True,))
            self.assertEqual(code, reinstall.EXIT_REINSTALLED, (name, said))
            self.assertIn('This same reinstall was begun before and is being continued', '\n'.join(said))
            self.infrastructure_is_devs()


class WhatIsRefusedBeforeAnythingIsOverwritten(ReinstallCase):
    """Steps 1 and 2."""

    def test_infrastructure_that_is_not_marked_ready(self):
        (self.dev / OTHER).write_bytes(b'# changed and not marked\r\n')
        code, said = self.reinstall(suites=())
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        self.assertIn('Make_Installable.bat INFRA', '\n'.join(said))

    def test_software_changed_outside_the_tools(self):
        self.change_in_dev(OTHER)
        (self.target / DERIVED).write_bytes(b'# edited by hand\r\n')
        backups = self.backups_made()
        code, said = self.reinstall(suites=())
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        self.assertIn('does not match its own list of installed files (1 difference(s))', '\n'.join(said))
        self.assertEqual(self.backups_made(), backups)

    def test_a_job_that_holds_the_lock_refuses_before_the_checks_and_any_backup(self):
        self.change_in_dev(OTHER)
        backups = self.backups_made()
        with job_lock.job_lock(self.target, 'a research job', 'now'):
            code, said = self.reinstall(suites=())
        self.assertEqual(code, reinstall.EXIT_REFUSED)
        self.assertIn('REFUSED: a process of this tree is running', '\n'.join(said))
        self.assertEqual(self.backups_made(), backups)

    def test_a_job_that_began_while_the_owner_was_deciding_refuses_at_the_second_reservation(self):
        self.change_in_dev(OTHER)
        before = self.software()
        lock = self.target / 'records' / job_lock.JOB_LOCK_NAME
        said = []

        def a_job_starts_then_yes(prompt):
            """While the owner reads the warning, a research job takes the tree's lock."""
            lock.write_bytes(b'research job; started later; process 4242\r\n')
            return 'YES'

        with mock.patch.object(common, 'checks_with_target_python', checks_in_this_process), \
                mock.patch.object(common, 'suite_if_it_is_the_trees', lambda *a, **k: (True, 'passed')), \
                mock.patch.object(recovery_kit, 'build_kit', return_value=KIT):
            code = reinstall.main(['QA'], settings.read_dev_view(self.dev), say=said.append,
                                  ask=a_job_starts_then_yes, now=self.running)
        self.assertEqual(code, reinstall.EXIT_REFUSED, said)
        self.assertEqual(lock.read_bytes(), b'research job; started later; process 4242\r\n')
        lock.unlink()
        self.assertEqual(self.software(), before, 'nothing was overwritten and no barrier was written')


class TheLauncherAndTheCommandWord(unittest.TestCase):
    """Reinstall_Infra.bat and deploy/deploy_command.py."""

    def test_the_launcher_runs_the_reinstall_with_devs_own_python_isolated(self):
        text = (REPOSITORY_ROOT / 'Reinstall_Infra.bat').read_bytes().decode('ascii')
        self.assertIn('"%PY%" -I -B -u "%TOOL%" reinstall-infra %*\r\nexit /b %ERRORLEVEL%\r\n', text)
        self.assertEqual(text.count('\n'), text.count('\r\n'), 'every line ends CRLF')
        self.assertIn('rem        Reinstall_Infra.bat PROD --replace-unfinished', text)

    def test_the_command_word_is_known_and_leads_to_the_command(self):
        source = (REPOSITORY_ROOT / 'deploy' / 'deploy_command.py').read_text(encoding='utf-8')
        self.assertIn("'reinstall-infra'", source)
        self.assertIn('from reinstall_infra import main as reinstall_infra', source)

    def test_the_warning_is_the_specifications(self):
        text = reinstall.WARNING.format(role='PROD', root='G:\\a_p_r_i_r')
        for words in ('This overwrites installed system files in PROD G:\\a_p_r_i_r.', 'there is no automatic rollback',
                      'A restore puts back exactly that backup', 'Anything installed, withdrawn or upgraded after it is '
                      'not put back', 'With no valid backup, recovery may not be possible.'):
            self.assertIn(words, text)


if __name__ == '__main__':
    unittest.main()
