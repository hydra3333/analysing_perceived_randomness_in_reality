"""Tests of Create_Tree and Install, and of a job that works under the lock the installing command holds.

Each test is named for the rule it proves and plants the fault that rule must catch. Everything runs on invented
draws and toy methods; the destination's job is the real job run inside the test's process, except in the last
test, which starts it as the commands do: a separate process with the destination's own Python.
(The simple scheme v0.2 sections 3, 3.1 rule 3, 4, 6 and 7.)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import sysconfig
import venv
from pathlib import Path
from unittest import mock

import research_fixtures as fx
import tree_fixtures as tf
from _common.game_profiles import get_profile

import install_tools                                        # noqa: E402  (tree_fixtures put deploy on the path)
import tree_parts                                           # noqa: E402
from research import backup, method_flags, settings, tree_lock    # noqa: E402
from tree_parts import CommandFailed, CommandRefused       # noqa: E402

GAME = fx.GAME
A, B = 'E_901/TOY_A_V1', 'E_901/TOY_B_V1'
METHOD_A = 'src/methods/E_901/TOY_A_V1/method.py'


def fail_at_the(count: int, real=tree_parts.copy_file):
    """A copy_file that raises OSError at its count-th call (and every later one): a disk that fills up."""
    calls = []

    def copy(source_root, target_root, relative):
        """Copy as the real one does until the planted call."""
        calls.append(relative)
        if len(calls) >= count:
            raise OSError(28, 'No space left on device', relative)
        return real(source_root, target_root, relative)
    return copy


class CreateTree(tf.TreesCase):
    """Scheme sections 3 and 6: a new tree, from DEV's flagged software and accepted results."""

    def test_a_new_tree_holds_the_flagged_software_and_the_results_and_its_own_settings_and_nothing_else(self):
        dev = self.dev()
        fx.run_job(dev)                                     # DEV now has results, records and IN_PLACE_SINCE files
        qa = self.create('QA')
        held = self.snapshot('QA')
        software = ['Backup.bat', 'Run_Research.bat', 'src/methods/E_901/TOY_A_V1/VARIANT.json', METHOD_A,
                    'src/methods/E_901/TOY_B_V1/VARIANT.json', 'src/methods/E_901/TOY_B_V1/method.py',
                    'src/toy_engine.py', 'src/updater/results_updater.py']
        data = [f'source_data/{GAME}_results_master.csv', f'source_data/{GAME}_results_master_ledger.csv']
        self.assertEqual(sorted(held), sorted(software + data + ['.venv/Scripts/python.exe', 'ENVIRONMENT.ini']))
        for name in software + data:
            self.assertEqual(held[name], (dev / name).read_bytes(), name)
        mine = settings.read_settings(qa, must_be='QA')
        self.assertTrue(settings.same_places(mine, self.settings()))
        self.assertEqual(held['ENVIRONMENT.ini'].count(b'\r\n'), held['ENVIRONMENT.ini'].count(b'\n'))
        self.assertTrue(self.no_lock_is_left())
        code, said = fx.run_job(qa)
        self.assertEqual(code, 0, said)
        for name in ('TOY_A_V1', 'TOY_B_V1'):
            self.assertEqual([line['content'] for line in fx.list_lines(qa, 'E_901', name)],
                             [line['content'] for line in fx.list_lines(dev, 'E_901', name)],
                             'the same software on the same results forecasts the same')

    def test_only_what_is_flagged_as_it_now_stands_and_not_retired_goes_into_a_new_tree(self):
        dev = self.dev(variants=('TOY_A_V1', 'TOY_B_V1', 'TOY_C_V1', 'TOY_D_V1', 'TOY_E_V1'), flag=())
        self.flag('E_901/TOY_A_V1', 'E_901/TOY_B_V1', 'E_901/TOY_C_V1', 'E_901/TOY_E_V1', 'INFRA')
        tf.edit(dev / 'src/methods/E_901/TOY_B_V1/method.py', '# changed after it was flagged')
        method_flags.write_retired(fx.method_folder(dev, 'E_901', 'TOY_C_V1'), {GAME: 1161}, 'superseded')
        (fx.method_folder(dev, 'E_901', 'TOY_E_V1') / 'notes.txt').write_text('x', encoding='ascii')
        qa = self.create('QA')
        self.assertEqual(sorted(path.name for path in (qa / 'src/methods/E_901').iterdir()), ['TOY_A_V1'])
        text = self.said_text()
        for name, why in (('TOY_B_V1', 'its flag is older than its files'), ('TOY_C_V1', 'it is retired in DEV'),
                          ('TOY_D_V1', 'it is not flagged in DEV'), ('TOY_E_V1', 'its folder in DEV fails its checks')):
            self.assertRegex(text, rf'not copied: E_901/{name}: .*{why}')
        self.assertIn('the infrastructure and 1 methods', text)

    def test_without_a_flagged_engine_or_a_flagged_method_or_results_no_tree_is_made(self):
        dev = self.dev(flag=())
        for flags, removed, why in (((), None, 'the infrastructure is not flagged in DEV'),
                                    (('INFRA',), None, 'no method is flagged in DEV'),
                                    (('ALL', 'INFRA'), 'source_data', 'DEV holds no accepted results')):
            if flags:
                self.flag(*flags)
            if removed:
                shutil.rmtree(dev / removed)
            with self.assertRaisesRegex(CommandRefused, why):
                self.command(install_tools.create_tree, 'QA')
            self.assertFalse(self.place('QA').exists(), why)
        tf.edit(dev / 'src' / fx.ENGINE_FILE, '# changed after it was flagged')
        with self.assertRaisesRegex(CommandRefused, 'the infrastructure is its flag is older than its files in DEV'):
            self.command(install_tools.create_tree, 'QA')
        self.assertTrue(self.no_lock_is_left())

    def test_a_tree_is_created_only_into_a_folder_that_is_absent_or_empty(self):
        self.dev()
        qa = self.place('QA')
        qa.mkdir()
        (qa / 'something.txt').write_text('mine', encoding='ascii')
        with self.assertRaisesRegex(CommandRefused, 'already holds something'):
            self.command(install_tools.create_tree, 'QA')
        self.assertEqual(sorted(path.name for path in qa.iterdir()), ['something.txt'])
        (qa / 'something.txt').unlink()
        self.assertEqual(self.command(install_tools.create_tree, 'QA'), 0, 'an empty folder is as good as none')
        with self.assertRaisesRegex(CommandRefused, 'already holds something.*use Install.bat'):
            self.command(install_tools.create_tree, 'QA')
        for role in ('DEV', 'qa', 'TEST'):
            with self.assertRaisesRegex(CommandRefused, 'makes a QA or a PROD tree'):
                self.command(install_tools.create_tree, role)

    def test_a_new_tree_is_not_made_in_a_folder_whose_parent_does_not_exist(self):
        self.places['PROD'] = (self.root / 'no_such_drive' / 'three_PROD', self.places['PROD'][1])
        self.dev()
        with self.assertRaisesRegex(CommandRefused, 'no_such_drive does not exist'):
            self.command(install_tools.create_tree, 'PROD')
        self.assertFalse((self.root / 'no_such_drive').exists())

    def test_a_creation_that_fails_part_way_leaves_a_folder_that_is_not_a_tree(self):
        self.dev()
        with mock.patch.object(install_tools, 'copy_file', fail_at_the(5)):
            with self.assertRaisesRegex(CommandFailed, 'THE TREE WAS NOT CREATED .*No space left.*Delete that folder'):
                self.command(install_tools.create_tree, 'QA')
        qa = self.place('QA')
        self.assertTrue(any(qa.iterdir()), 'part of a copy')
        self.assertFalse((qa / 'ENVIRONMENT.ini').exists())
        with self.assertRaisesRegex(settings.SettingsRefused, 'this folder is not a tree'):
            settings.read_settings(qa)
        with self.assertRaisesRegex(CommandRefused, r'the rest of a\s+creation that did not finish, delete it by hand'):
            self.command(install_tools.create_tree, 'QA')
        self.assertTrue(self.no_lock_is_left())

    def test_a_copy_that_does_not_read_back_as_devs_makes_no_tree(self):
        self.dev()
        real = tree_parts.copy_file

        def one_file_spoiled(source_root, target_root, relative):
            """Copy, but spoil the copy of one method file."""
            real(source_root, target_root, relative)
            if relative == METHOD_A:
                tf.edit(Path(target_root) / relative, '# not what DEV holds')

        with mock.patch.object(install_tools, 'copy_file', one_file_spoiled):
            with self.assertRaisesRegex(CommandFailed, 'THE TREE WAS NOT CREATED .*does not match DEV when read back'):
                self.command(install_tools.create_tree, 'QA')
        self.assertFalse((self.place('QA') / 'ENVIRONMENT.ini').exists())

    def test_while_another_command_works_in_dev_no_tree_is_created(self):
        self.dev()
        with tree_lock.tree_lock(self.place('DEV'), 'research job', 'earlier'):
            with self.assertRaisesRegex(tree_lock.LaunchRefused, 'a process of this tree is running'):
                self.command(install_tools.create_tree, 'QA')
        self.assertFalse(self.place('QA').exists())


class Install(tf.TreesCase):
    """Scheme sections 4 and 6: what differs and is flagged is installed, after a backup; then the tree's job."""

    def two_trees(self, **options) -> tuple:
        """DEV and a QA tree created from it whose first job has run. Returns (dev, qa)."""
        dev = self.dev(**options)
        qa = self.create('QA')
        self.assertEqual(fx.run_job(qa)[0], 0)
        self.said.clear()
        return dev, qa

    def install(self, **options) -> int:
        """Install into QA with the stand-ins."""
        return self.command(install_tools.install, 'QA', **{'show': False, **options})

    def test_when_nothing_differs_nothing_is_done_not_even_a_backup(self):
        self.two_trees()
        before = self.snapshot('QA')
        self.assertEqual(self.install(), 0)
        self.assertIn('Nothing to install', self.said_text())
        self.assertEqual((self.backups, self.jobs), ([], []))
        self.assertEqual(self.snapshot('QA'), before)
        self.assertTrue(self.no_lock_is_left())

    def test_a_changed_method_is_replaced_and_a_new_one_added_after_a_backup_and_the_trees_job_makes_them_again(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# a better calculation')
        self.add_variant(dev, 'TOY_NEW_V1')
        self.flag('ALL')
        folder = fx.method_folder(qa, 'E_901', 'TOY_A_V1')
        method_flags.write_retired(fx.method_folder(qa, 'E_901', 'TOY_B_V1'), {GAME: 1161}, 'retired in QA only')
        (folder / '__pycache__').mkdir()
        in_place_before = (folder / 'IN_PLACE_SINCE').read_bytes()
        old, seen = (qa / METHOD_A).read_bytes(), []

        def backup_watched(read, why, moment):
            """Note what the destination held when the backup was made, and that both locks were held."""
            seen.append((read.role, why, (qa / METHOD_A).read_bytes() == old, self.lock_of('DEV').exists(),
                         self.lock_of('QA').exists()))
            return Path('QA_before.zip')

        self.assertEqual(self.install(backup=backup_watched), 0, self.said_text())
        self.assertEqual(seen, [('QA', 'before install', True, True, True)])
        text = self.said_text()
        self.assertIn(f'  replace: {A} (its results in the QA tree are made again)', text)
        self.assertIn('  add: E_901/TOY_NEW_V1', text)
        self.assertIn('Installed into the QA tree: 0 infrastructure files, 2 methods.', text)
        for name in (METHOD_A, 'src/methods/E_901/TOY_NEW_V1/method.py', 'src/methods/E_901/TOY_NEW_V1/VARIANT.json'):
            self.assertEqual((qa / name).read_bytes(), (dev / name).read_bytes(), name)
        self.assertEqual(len(self.jobs), 1)
        self.assertTrue(any('REBUILT' in line and A in line for line in self.job_said), self.job_said)
        self.assertEqual(len(fx.list_lines(qa, 'E_901', 'TOY_NEW_V1')), len(fx.list_lines(qa, 'E_901', 'TOY_A_V1')))
        flags = sorted(path.relative_to(qa).as_posix() for path in qa.rglob('I_AM_*'))
        self.assertEqual(flags, ['src/methods/E_901/TOY_B_V1/I_AM_RETIRED'], 'no flag of DEV is copied; QA\'s own stay')
        self.assertNotEqual((folder / 'IN_PLACE_SINCE').read_bytes(), in_place_before, 'written afresh by QA\'s own job')
        self.assertTrue(self.no_lock_is_left())
        self.said.clear()
        self.assertEqual(self.install(), 0)
        self.assertIn('Nothing to install', self.said_text())

    def test_the_trees_job_works_under_the_lock_the_install_holds_and_is_given_its_key(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        seen = []

        def job_watched(read, key, say):
            """Note the lock as the job finds it, then run the job under it."""
            seen.append((read.role, self.lock_of('QA').read_text(encoding='ascii').split()[-2:] == ['key', key],
                         self.lock_of('DEV').exists()))
            return self.job_in_process(read, key, say)

        self.assertEqual(self.install(run_job=job_watched), 0)
        self.assertEqual(seen, [('QA', True, True)])
        self.assertTrue(self.no_lock_is_left())

    def test_a_method_whose_flag_is_missing_or_older_than_its_files_is_named_and_left_alone(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed, and not flagged again')
        self.add_variant(dev, 'TOY_NEW_V1')
        (fx.method_folder(dev, 'E_901', 'TOY_B_V1') / 'notes.txt').write_text('x', encoding='ascii')
        before = self.snapshot('QA')
        self.assertEqual(self.install(), 0)
        text = self.said_text()
        self.assertIn(f'NOT INSTALLED: {A}: it is its flag is older than its files in DEV', text)
        self.assertIn('NOT INSTALLED: E_901/TOY_NEW_V1: it is not flagged in DEV', text)
        self.assertIn(f'NOT INSTALLED: {B}: its folder in DEV fails its checks', text)
        self.assertIn('Nothing to install', text)
        self.assertEqual((self.snapshot('QA'), self.backups, self.jobs), (before, [], []))

    def test_the_infrastructure_is_installed_only_when_flagged_as_it_now_stands_and_says_what_is_made_again(self):
        dev, qa = self.two_trees()
        tf.edit(dev / 'src' / fx.ENGINE_FILE, '# the engine, changed')
        (dev / 'src' / 'new_engine_file.py').write_text('# new\n', encoding='ascii')
        self.assertEqual(self.install(), 0)
        self.assertIn('NOT INSTALLED: the infrastructure differs (2 files) but is its flag is older than its files',
                      self.said_text())
        self.assertEqual((self.backups, self.jobs), ([], []))
        self.flag('INFRA')
        self.said.clear()
        self.assertEqual(self.install(), 0, self.said_text())
        self.assertIn('  infrastructure: 2 files added or replaced, 0 removed. The engine differs, so the QA tree\'s job '
                      'makes everything again, in both games.', self.said_text())
        self.assertTrue(any('REBUILD: everything' in line for line in self.job_said), self.job_said)
        self.assertEqual(tree_parts.infrastructure_paths(qa), tree_parts.infrastructure_paths(dev))
        self.assertEqual(tree_parts.differing(dev, qa, tree_parts.infrastructure_paths(dev)), [])

    def test_a_change_to_the_updater_or_a_launcher_alone_is_installed_and_makes_nothing_again(self):
        dev, qa = self.two_trees()
        tf.edit(dev / tf.TOY_UPDATER, '# the updater, changed')
        tf.edit(dev / 'Backup.bat', 'rem changed')
        (dev / 'src' / 'updater' / 'old_part.py').write_text('# to be removed later\n', encoding='ascii')
        self.flag('INFRA')
        self.assertEqual(self.install(), 0)
        self.assertIn('3 files added or replaced, 0 removed. The engine\'s fingerprint is the same', self.said_text())
        self.assertFalse(any('REBUILD' in line for line in self.job_said), self.job_said)
        (dev / 'src' / 'updater' / 'old_part.py').unlink()
        self.flag('INFRA')
        self.said.clear()
        self.assertEqual(self.install(), 0)
        self.assertIn('0 files added or replaced, 1 removed.', self.said_text())
        self.assertFalse((qa / 'src' / 'updater' / 'old_part.py').exists())
        self.assertEqual((qa / 'Backup.bat').read_bytes(), (dev / 'Backup.bat').read_bytes())

    def test_show_prints_the_plan_and_changes_nothing(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        tf.edit(dev / 'src' / fx.ENGINE_FILE, '# changed')
        self.flag('ALL', 'INFRA')
        before = self.snapshot('QA')
        self.assertEqual(self.install(show=True), 0)
        text = self.said_text()
        self.assertIn('  infrastructure: 1 files added or replaced', text)
        self.assertIn(f'  replace: {A}', text)
        self.assertIn('--show: nothing was changed.', text)
        self.assertEqual((self.snapshot('QA'), self.backups, self.jobs), (before, [], []))
        self.assertTrue(self.no_lock_is_left())

    def test_a_method_the_destination_has_and_dev_does_not_is_left_alone(self):
        dev, qa = self.two_trees()
        self.add_variant(qa, 'TOY_ONLY_IN_QA_V1')
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        self.assertEqual(self.install(), 0)
        self.assertIn('  left alone: E_901/TOY_ONLY_IN_QA_V1 (the QA tree has it; DEV does not)', self.said_text())
        self.assertTrue((fx.method_folder(qa, 'E_901', 'TOY_ONLY_IN_QA_V1') / 'method.py').is_file())

    def test_a_retired_method_is_never_added_but_one_the_destination_has_is_kept_in_step(self):
        dev, qa = self.two_trees()
        self.add_variant(dev, 'TOY_GONE_V1')
        method_flags.write_retired(fx.method_folder(dev, 'E_901', 'TOY_GONE_V1'), {GAME: 1161}, 'never installed')
        method_flags.write_retired(fx.method_folder(dev, 'E_901', 'TOY_A_V1'), {GAME: 1161}, 'superseded')
        tf.edit(dev / METHOD_A, '# a correction to a retired method')
        self.flag('ALL')
        self.assertEqual(self.install(), 0)
        text = self.said_text()
        self.assertIn('NOT INSTALLED: E_901/TOY_GONE_V1: it is retired in DEV, and a retired method is not added', text)
        self.assertIn(f'  replace: {A}', text)
        self.assertFalse(fx.method_folder(qa, 'E_901', 'TOY_GONE_V1').exists())
        self.assertFalse((fx.method_folder(qa, 'E_901', 'TOY_A_V1') / 'I_AM_RETIRED').exists(), 'retiring is Retire\'s job')

    def test_nothing_is_replaced_unless_the_backup_before_it_was_made(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        before = self.snapshot('QA')

        def no_room(read, why, moment):
            """A backup that fails."""
            raise backup.BackupFailed('the backup of the QA tree into T:\\x was not made: OSError: the disk is full')

        with self.assertRaisesRegex(CommandRefused, 'the disk is full. Nothing was replaced'):
            self.install(backup=no_room)
        self.assertEqual((self.snapshot('QA'), self.jobs), (before, []))
        self.assertTrue(self.no_lock_is_left())

    def test_a_destination_without_its_own_python_is_refused_before_anything_is_changed(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        (qa / '.venv' / 'Scripts' / 'python.exe').unlink()
        before = self.snapshot('QA')
        with self.assertRaisesRegex(CommandRefused, 'has no Python environment of its own.*create_venv.bat'):
            self.install()
        self.assertEqual((self.snapshot('QA'), self.backups, self.jobs), (before, [], []))

    def test_an_install_that_fails_part_way_says_so_runs_no_job_and_is_finished_by_running_it_again(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        tf.edit(dev / 'src/methods/E_901/TOY_B_V1/method.py', '# changed')
        self.flag('ALL')
        with mock.patch.object(install_tools, 'copy_file', fail_at_the(2)):
            with self.assertRaisesRegex(CommandFailed, 'THE INSTALL DID NOT FINISH .*No space left.*run Install.bat '
                                                       'QA again.*Restore.bat QA QA_20261201_201012_before_install.zip'):
                self.install()
        self.assertEqual(self.jobs, [])
        self.assertEqual((qa / METHOD_A).read_bytes(), (dev / METHOD_A).read_bytes(), 'the first file went in')
        self.assertTrue(self.no_lock_is_left())
        self.said.clear()
        self.assertEqual(self.install(), 0)
        self.assertIn(f'  replace: {B}', self.said_text())
        self.assertNotIn(f'  replace: {A}', self.said_text())

    def test_what_is_in_the_destination_after_the_copy_is_checked_against_dev(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        real = tree_parts.copy_file

        def spoiled(source_root, target_root, relative):
            """Copy, but spoil the copy."""
            real(source_root, target_root, relative)
            tf.edit(Path(target_root) / relative, '# not what DEV holds')

        with mock.patch.object(install_tools, 'copy_file', spoiled):
            with self.assertRaisesRegex(CommandFailed, 'THE INSTALL DID NOT FINISH .*the destination still differs'):
                self.install()
        self.assertEqual(self.jobs, [])

    def test_a_job_that_does_not_finish_cleanly_is_said_and_the_exit_code_shows_it(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        self.job_code = 1
        self.assertEqual(self.install(), tree_parts.EXIT_NOT_CLEAN)
        self.assertIn('The software is installed, but the QA tree\'s job did not finish cleanly (exit code 1)',
                      self.said_text())

    def test_while_a_command_works_in_either_tree_nothing_is_installed_and_no_lock_is_left_behind(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        before = self.snapshot('QA')
        for role in ('DEV', 'QA'):
            with tree_lock.tree_lock(self.place(role), 'research job', 'earlier'):
                for show in (False, True):
                    with self.assertRaisesRegex(tree_lock.LaunchRefused, 'a process of this tree is running'):
                        self.install(show=show)
            self.assertTrue(self.no_lock_is_left(), role)
        self.assertEqual((self.snapshot('QA'), self.backups, self.jobs), (before, [], []))

    def test_the_destination_must_be_the_tree_meant_by_its_own_settings_file(self):
        dev, qa = self.two_trees()
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        own = (qa / 'ENVIRONMENT.ini').read_text(encoding='utf-8')
        for planted, why in ((own.replace('role = QA', 'role = PROD'), 'does not end with PROD'),
                             (own.replace(str(self.places['PROD'][1]), str(self.root / 'elsewhere')),
                              r'do not name\s+the same folders'),
                             (None, 'there is no settings file here, so this folder is not a tree')):
            if planted is None:
                (qa / 'ENVIRONMENT.ini').unlink()
            else:
                (qa / 'ENVIRONMENT.ini').write_text(planted, encoding='utf-8')
            with self.assertRaisesRegex(settings.SettingsRefused, why):
                self.install()
        with self.assertRaisesRegex(settings.SettingsRefused, 'not a tree'):
            self.command(install_tools.install, 'PROD', show=False)
        with self.assertRaisesRegex(CommandRefused, 'installs into QA or PROD'):
            self.command(install_tools.install, 'DEV', show=False)
        self.assertEqual((qa / METHOD_A).read_bytes().count(b'# changed'), 0)
        self.assertEqual((self.backups, self.jobs), ([], []))
        self.assertTrue(self.no_lock_is_left())


class ASharedHelper(tf.TreesCase):
    """A helper file several methods use is brought only if every method of the destination that uses it is
    installed with it: no method ever becomes a mix of files that was never flagged."""

    HELPER = 'E_901/core_v1.py'

    def two_trees(self) -> tuple:
        """DEV with methods A and B that share a family helper and C that does not; QA created from it."""
        dev = self.dev(variants=(), flag=())
        (dev / 'src/methods/E_901').mkdir()
        (dev / 'src/methods' / self.HELPER).write_text('# the family\'s calculation\n', encoding='ascii')
        for name, helpers in (('TOY_A_V1', (self.HELPER,)), ('TOY_B_V1', (self.HELPER,)), ('TOY_C_V1', ())):
            fx.add_toy_variant(dev, 'E_901', name, games=(GAME,), helpers=helpers)
        self.flag('ALL', 'INFRA')
        qa = self.create('QA')
        self.said.clear()
        return dev, qa

    def install(self) -> int:
        """Install into QA with the stand-ins; the job's exit code is planted, since no job is needed here."""
        self.job_code = 0
        return self.command(install_tools.install, 'QA', show=False)

    def test_a_changed_helper_goes_in_only_with_every_method_that_uses_it(self):
        dev, qa = self.two_trees()
        tf.edit(dev / 'src/methods' / self.HELPER, '# changed')
        tf.edit(dev / 'src/methods/E_901/TOY_C_V1/method.py', '# changed')
        self.flag(A, 'E_901/TOY_C_V1')                     # B, which uses the helper too, is not flagged again
        before = (qa / 'src/methods' / self.HELPER).read_bytes()
        self.assertEqual(self.install(), 0)
        text = self.said_text()
        self.assertRegex(text, rf'NOT INSTALLED: {A}: it brings a changed helper file \({self.HELPER}\) that {B} in the '
                               rf'destination also uses, and that method is not installed with it')
        self.assertIn(f'NOT INSTALLED: {B}: it is its flag is older than its files in DEV', text)
        self.assertIn('  replace: E_901/TOY_C_V1', text)
        self.assertEqual((qa / 'src/methods' / self.HELPER).read_bytes(), before, 'the helper did not go in')
        self.flag('ALL')
        self.said.clear()
        self.assertEqual(self.install(), 0)
        self.assertIn(f'  replace: {A}', self.said_text())
        self.assertIn(f'  replace: {B}', self.said_text())
        self.assertEqual((qa / 'src/methods' / self.HELPER).read_bytes(), (dev / 'src/methods' / self.HELPER).read_bytes())

    def test_a_method_only_the_destination_has_also_holds_a_changed_helper_back(self):
        dev, qa = self.two_trees()
        fx.add_toy_variant(qa, 'E_901', 'TOY_ONLY_IN_QA_V1', games=(GAME,), helpers=(self.HELPER,))
        tf.edit(dev / 'src/methods' / self.HELPER, '# changed')
        self.flag('ALL')
        before = self.snapshot('QA')
        self.assertEqual(self.install(), 0)
        text = self.said_text()
        for name in (A, B):
            self.assertRegex(text, rf'NOT INSTALLED: {name}: it brings a changed helper file .* that '
                                   rf'E_901/TOY_ONLY_IN_QA_V1 in the destination also uses.*DEV has no such method')
        self.assertEqual((self.snapshot('QA'), self.backups), (before, []))

    def test_a_new_method_that_brings_a_new_helper_changes_no_other_and_is_added(self):
        dev, qa = self.two_trees()
        (dev / 'src/methods/E_901/core_v2.py').write_text('# a second calculation\n', encoding='ascii')
        fx.add_toy_variant(dev, 'E_901', 'TOY_NEW_V1', games=(GAME,), helpers=('E_901/core_v2.py',))
        self.flag('E_901/TOY_NEW_V1')
        self.assertEqual(self.install(), 0)
        self.assertIn('  add: E_901/TOY_NEW_V1', self.said_text())
        self.assertTrue((qa / 'src/methods/E_901/core_v2.py').is_file())


class AJobUnderAnotherCommandsLock(fx.JobCase):
    """Scheme section 6, last paragraph: the destination's job works under the lock the command already holds."""

    def test_a_job_given_the_locks_key_works_under_it_and_leaves_it_in_place(self):
        tree = self.tree()
        lock_file = tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME
        with tree_lock.tree_lock(tree, 'install', 'now') as lock:
            held = lock_file.read_bytes()
            self.assertRegex(held.decode('ascii'), r'^install; started now; process \d+; key [0-9a-f]{16}\r\n$')
            code, said = fx.run_job(tree, under_lock=lock.key)
            self.assertEqual(code, 0, said)
            self.assertEqual(lock_file.read_bytes(), held, 'neither removed nor rewritten by the job')
        self.assertFalse(lock_file.exists())
        self.assertEqual(len(fx.list_lines(tree, 'E_901', 'TOY_A_V1')), fx.LAST_AT_START + 1 - fx.FIRST_TOY_TARGET + 1)

    def test_a_job_given_a_key_that_is_not_the_locks_or_no_lock_at_all_does_nothing(self):
        tree = self.tree()
        lock_file = tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME
        with tree_lock.tree_lock(tree, 'research job', 'now') as lock:
            for key in ('0' * 16, lock.key[:-1], '', 'key'):
                code, said = fx.run_job(tree, under_lock=key)
                self.assertEqual(code, 2, key)
                self.assertTrue(any('is not there or is not that command\'s lock' in line for line in said), said)
            code, said = fx.run_job(tree)
            self.assertEqual(code, 2, 'and an ordinary job is refused as ever')
            self.assertTrue(lock_file.exists())
        code, said = fx.run_job(tree, under_lock='0' * 16)
        self.assertEqual(code, 2)
        self.assertFalse(lock_file.exists(), 'a job told to work under a lock never makes one')
        self.assertFalse((tree / 'results').exists())


@mock.patch.object(settings.TreeSettings, 'python',
                   settings.TreeSettings.python if os.name == 'nt'
                   else property(lambda self: self.venv_dir / 'bin' / 'python'))
class TheDestinationsOwnJobInItsOwnProcess(tf.TreesCase):
    """The one test that starts the destination's job as the commands do: another process, the destination's own
    Python and its own copy of the software. (Off Windows a Python environment keeps its program in bin, not in
    Scripts: the test says where; nothing else differs.)"""

    def real_dev(self) -> Path:
        """A DEV tree that holds this project's real engine, with toy methods and invented results of both
        games, all flagged."""
        tree = fx.make_tree(self.place('DEV'), 'DEV', places=self.places)
        (tree / 'src' / fx.ENGINE_FILE).unlink()
        families = re.compile(r'E_\d{3}\Z')
        shutil.copytree(tf.TREE_OF_THIS_FILE / 'src', tree / 'src', dirs_exist_ok=True,
                        ignore=lambda folder, names: [n for n in names if n == '__pycache__' or families.match(n)])
        for name in tree_parts.ROOT_FILES:
            shutil.copyfile(tf.TREE_OF_THIS_FILE / name, tree / name)
        for game_id in ('POWERBALL', 'OZLOTTO'):
            fx.write_results(tree, game_id, get_profile(game_id).first_draw + 16)
        fx.add_toy_variant(tree, 'E_901', 'TOY_A_V1')
        fx.add_toy_variant(tree, 'E_901', 'TOY_B_V1', behaviour={'reverse': True})
        self.flag('ALL', 'INFRA')
        return tree

    @staticmethod
    def real_python(tree: Path) -> None:
        """Give a tree a Python environment of its own that can see the packages the tests run with."""
        venv.create(tree / '.venv', with_pip=False, symlinks=os.name != 'nt')
        site = next(path for path in (tree / '.venv').rglob('site-packages') if path.is_dir())
        (site / 'borrowed_for_the_test.pth').write_text(sysconfig.get_paths()['purelib'] + '\n', encoding='utf-8')

    def test_an_install_runs_the_destinations_own_job_in_its_own_process_under_the_lock_it_holds(self):
        dev = self.real_dev()
        self.assertEqual(install_tools.create_tree(self.settings(), 'QA', moment=tf.MOMENT, say=self.said.append), 0)
        qa = self.place('QA')
        self.real_python(qa)
        tf.edit(dev / METHOD_A, '# changed')
        self.flag('ALL')
        real_run, children = subprocess.run, []

        def captured(command, cwd):
            """Start the child as the command does, but keep what it prints for the test."""
            children.append((command, real_run(command, cwd=cwd, capture_output=True, text=True)))
            return children[-1][1]

        with mock.patch.object(tree_parts.subprocess, 'run', captured):
            code = install_tools.install(self.settings(), 'QA', show=False, moment=tf.MOMENT, say=self.said.append)
        command, child = children[0]
        self.assertEqual((code, child.returncode), (0, 0), child.stdout + child.stderr)
        self.assertEqual(command[:4] + command[5:7], [str(self.settings('QA').python), '-I', '-B', '-u', 'research',
                                                      '--no-update'])
        self.assertEqual(Path(command[4]), qa / 'src' / 'research_command.py', 'the destination\'s own copy')
        self.assertIn('RESEARCH JOB - START', child.stdout)
        self.assertIn(f'the QA tree at {qa}', child.stdout)
        self.assertEqual(child.stdout.strip().splitlines()[-1], 'The job finished.')
        for game_id in ('POWERBALL', 'OZLOTTO'):
            self.assertEqual(len(fx.list_lines(qa, 'E_901', 'TOY_A_V1', game_id=game_id)), 15, game_id)
        log = [json.loads(line) for line in (qa / 'records' / 'JOB_LOG.jsonl').read_text(encoding='ascii').splitlines()]
        self.assertEqual([line['how'] for line in log], ['finished'])
        made = sorted(path.name for path in self.places['QA'][1].iterdir())
        self.assertEqual(len(made), 2, made)
        self.assertRegex(made[0], r'^QA_\d{8}_\d{6}_after_job\.zip$')
        self.assertEqual(made[1], 'QA_20261201_201012_before_install.zip')
        self.assertTrue(self.no_lock_is_left())
        wrong = real_run(command[:-1] + ['0' * 16], cwd=qa, capture_output=True, text=True)
        self.assertEqual(wrong.returncode, 2, wrong.stdout + wrong.stderr)
        self.assertIn('is not there or is not that command\'s lock', wrong.stdout)
        self.assertEqual(sys.executable != command[0], True, 'another Python program than the one running the tests')


if __name__ == '__main__':
    import unittest
    unittest.main()
