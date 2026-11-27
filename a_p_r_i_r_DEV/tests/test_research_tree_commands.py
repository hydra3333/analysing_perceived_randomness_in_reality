"""Tests of what every command does first in a tree, of the backup, and of DEV's two own-tree commands.

Each test is named for the rule it proves and plants the fault that rule must catch. Everything runs on invented
draws and toy methods.
(The simple scheme v0.2 sections 3.1, 4, 5 steps 1, 2 and 8, 6 and 7.)
"""
import contextlib
import io
import json
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from unittest import mock

TREE_OF_THIS_FILE = Path(__file__).resolve().parents[1]
if str(TREE_OF_THIS_FILE / 'deploy') not in sys.path:
    sys.path.insert(0, str(TREE_OF_THIS_FILE / 'deploy'))

import dev_command                                          # noqa: E402  (after the path line above)
import dev_tools                                            # noqa: E402
import research_command                                     # noqa: E402
import research_fixtures as fx                              # noqa: E402
from research import backup, code_identity, method_flags, research_job, settings, tree_lock    # noqa: E402

GAME = fx.GAME
MOMENT = datetime(2026, 12, 1, 20, 10, 12)


def run_program(program, tree: Path, *arguments) -> tuple:
    """Run a command program (research_command or dev_command) as its launcher does, but in this process and as
    if it lay in the given tree and that tree's own Python were running. Returns (exit code, what it printed)."""
    path_before, printed = list(sys.path), io.StringIO()
    folders = (tree / 'src', tree / 'src' / 'methods') + ((TREE_OF_THIS_FILE / 'deploy',) if program is dev_command
                                                           else ())
    try:
        with mock.patch.object(program, 'TREE_ROOT', tree), mock.patch.object(program, 'IMPORT_FOLDERS', folders), \
                mock.patch.object(sys, 'prefix', str(tree / '.venv')), contextlib.redirect_stdout(printed):
            code = program.run_command(list(arguments))
    finally:
        sys.path[:] = path_before
        fx.ImportPath._forget()
    return code, printed.getvalue()


class TheFirstStepOfEveryCommand(fx.JobCase):
    """enter_tree: the folder is the tree its settings say, and its working folders are its own; then the lock."""

    def linked_results(self, tree: Path) -> Path | None:
        """Make the tree's results folder a link to a folder outside it. Returns that folder, or None if this
        machine allows no link."""
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        return elsewhere if fx.make_folder_link(tree / 'results', elsewhere) else None

    def test_a_working_folder_linked_to_another_place_refuses_the_job_and_the_other_place_is_untouched(self):
        tree = self.tree()
        elsewhere = self.linked_results(tree)
        if elsewhere is None:
            self.skipTest('this machine allows neither a symbolic link nor a junction')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 2)
        self.assertTrue(any('is a link or a junction to another place, not a real folder of this tree' in line
                            for line in said), said)
        self.assertEqual(list(elsewhere.iterdir()), [])
        self.assertFalse((tree / 'records').exists(), 'refused before even the lock was made')

    def test_the_updater_and_the_backup_started_by_themselves_make_the_same_first_step(self):
        tree = self.tree()
        elsewhere = self.linked_results(tree)
        if elsewhere is None:
            self.skipTest('this machine allows neither a symbolic link nor a junction')
        with mock.patch('updater.results_updater.main') as updater_main:
            for command in ('update', 'backup'):
                code, printed = run_program(research_command, tree, command)
                self.assertEqual(code, research_command.EXIT_BAD_COMMAND, command)
                self.assertIn('REFUSED:', printed)
                self.assertIn('is a link or a junction', printed)
        self.assertFalse(updater_main.called)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_a_folder_that_is_not_the_tree_its_file_says_runs_no_command_at_all(self):
        tree = self.tree()
        (tree / 'ENVIRONMENT.ini').write_text(fx.settings_text('PROD', fx.places_around(tree, 'DEV')), encoding='utf-8')
        with mock.patch('updater.results_updater.main') as updater_main:
            for program, command in ((research_command, 'research'), (research_command, 'update'),
                                     (research_command, 'backup'), (dev_command, 'make_installable'),
                                     (dev_command, 'who_uses')):
                code, printed = run_program(program, tree, command, 'x')
                self.assertEqual(code, 2, command)
                self.assertIn('does not end with PROD', printed, command)
        self.assertFalse(updater_main.called)
        self.assertEqual(sorted(path.name for path in tree.iterdir()), ['.venv', 'ENVIRONMENT.ini', 'source_data', 'src'])

    def test_every_command_holds_the_one_lock_and_refuses_while_another_holds_it(self):
        tree = self.tree()
        lock = tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME
        lock.parent.mkdir()
        lock.write_bytes(b'research job; started earlier\r\n')
        with mock.patch('updater.results_updater.main') as updater_main:
            for program, arguments in ((research_command, ('research', '--no-update')), (research_command, ('update',)),
                                       (research_command, ('backup',)), (dev_command, ('make_installable', 'ALL'))):
                code, printed = run_program(program, tree, *arguments)
                self.assertEqual(code, 2, arguments)
                self.assertIn('REFUSED: a process of this tree is running', printed, arguments)
        self.assertFalse(updater_main.called)
        self.assertTrue(lock.is_file(), 'never removed by another command')
        self.assertFalse(any(name.endswith(method_flags.INSTALLABLE_NAME) for name in fx.files_under(tree, 'src')))
        self.assertFalse((tree / 'results').exists())

    def test_the_first_systems_orphan_marker_means_nothing_in_a_tree_of_this_scheme(self):
        tree = self.tree()
        marker = tree / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        marker.parent.mkdir(parents=True)
        marker.write_text('{}', encoding='ascii')
        self.assertEqual(fx.run_job(tree)[0], 0)
        self.assertTrue(marker.is_file(), 'and nothing here touches it')


class TheBackup(fx.JobCase):
    """Scheme section 7: one plain ZIP, without the environment and the lock file."""

    def test_a_backup_is_one_plain_zip_of_the_whole_tree_but_the_environment_the_lock_and_pythons_caches(self):
        tree = self.tree()
        fx.run_job(tree)
        read = settings.read_settings(tree)
        (tree / '.venv' / 'python.exe').write_bytes(b'the environment')
        (tree / 'src' / '__pycache__').mkdir()
        (tree / 'src' / '__pycache__' / 'x.pyc').write_bytes(b'cache')
        (tree / 'results' / '.venv').mkdir()
        (tree / 'results' / '.venv' / 'kept.txt').write_bytes(b'only the environment at the tree\'s root is left out')
        lock = tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME
        with tree_lock.tree_lock(tree, 'backup', 'now'):
            path = backup.make_backup(read, 'after job', MOMENT)
            self.assertTrue(lock.exists())
        self.assertEqual(path, read.backup_root / 'DEV_20261201_201012_after_job.zip')
        self.assertEqual([entry.name for entry in read.backup_root.iterdir()], [path.name], 'nothing unfinished is left')
        with zipfile.ZipFile(path) as archive:
            self.assertIsNone(archive.testzip())
            held = {info.filename: archive.read(info) for info in archive.infolist()}
            self.assertEqual({info.compress_type for info in archive.infolist()}, {zipfile.ZIP_DEFLATED})
        on_disk = {name: data for name, data in fx.files_under(tree, '.', leave_out=()).items()
                   if not name.startswith('.venv/') and '__pycache__' not in name}
        self.assertEqual(held, on_disk)
        for wanted in ('ENVIRONMENT.ini', 'source_data/POWERBALL_results_master.csv', 'records/JOB_LOG.jsonl',
                       'src/methods/E_901/TOY_A_V1/IN_PLACE_SINCE', 'results/.venv/kept.txt',
                       f'results/research/{GAME}/variants/E_901/TOY_A_V1/forecasts.jsonl'):
            self.assertIn(wanted, held)
        self.assertNotIn('records/TREE.lock', held)

    def test_a_backup_is_never_written_over_and_its_name_says_why_it_was_made(self):
        tree = self.tree()
        read = settings.read_settings(tree)
        names = [backup.make_backup(read, why, MOMENT).name for why in ('before install', 'before install', 'on demand')]
        self.assertEqual(names, ['DEV_20261201_201012_before_install.zip', 'DEV_20261201_201012_before_install_2.zip',
                                 'DEV_20261201_201012_on_demand.zip'])
        self.assertEqual(backup.backup_name('PROD', MOMENT, '../odd: reason!'), 'PROD_20261201_201012_odd_reason.zip')

    def test_a_backup_that_cannot_be_made_says_where_and_why_and_leaves_no_half_backup(self):
        tree = self.tree()
        read = settings.read_settings(tree)
        read.backup_root.parent.mkdir(parents=True)
        read.backup_root.write_bytes(b'a file where the backup folder should be')
        with self.assertRaisesRegex(backup.BackupFailed, 'the backup of the DEV tree into .* was not made'):
            backup.make_backup(read, 'after job', MOMENT)
        read.backup_root.unlink()
        with mock.patch.object(zipfile.ZipFile, 'write', side_effect=OSError('the disk is full')):
            with self.assertRaisesRegex(backup.BackupFailed, 'OSError: the disk is full'):
                backup.make_backup(read, 'after job', MOMENT)
        self.assertEqual(list(read.backup_root.iterdir()), [], 'what was begun is removed')

    def test_every_job_ends_with_a_backup_that_holds_what_the_job_made_and_its_line_of_the_job_log(self):
        tree = self.tree()
        code, said = fx.run_job(tree, backup=backup.make_backup)
        self.assertEqual(code, 0, said)
        made = [line for line in said if line.startswith('Backup made: ')]
        self.assertEqual(len(made), 1, said)
        path = Path(made[0].split(': ', 1)[1])
        self.assertEqual(path.parent, settings.read_settings(tree).backup_root)
        self.assertRegex(path.name, r'^DEV_\d{8}_\d{6}_after_job\.zip$')
        with zipfile.ZipFile(path) as archive:
            log = [json.loads(line) for line in archive.read('records/JOB_LOG.jsonl').decode('ascii').splitlines()]
            self.assertEqual((len(log), log[0]['how']), (1, 'finished'))
            self.assertEqual(archive.read(f'results/research/{GAME}/variants/E_901/TOY_A_V1/scores.jsonl'),
                             (tree / 'results/research' / GAME / 'variants/E_901/TOY_A_V1/scores.jsonl').read_bytes())
        self.assertFalse((tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME).exists())
        self.assertIs(research_job.run.__kwdefaults__['backup'], backup.make_backup, 'a real job always makes one')

    def test_if_the_backup_cannot_be_made_the_job_says_so_loudly_and_what_it_computed_stands(self):
        tree = self.tree()

        def no_room(read, why, moment):
            """A backup that fails."""
            raise backup.BackupFailed('the backup of the DEV tree into T:\\x was not made: OSError: the disk is full')

        code, said = fx.run_job(tree, backup=no_room)
        self.assertEqual(code, 1)
        loud = [line for line in said if 'THE BACKUP AFTER THIS JOB WAS NOT MADE' in line]
        self.assertEqual(len(loud), 2, 'said when it happens and again at the end')
        self.assertIn('What the job computed stands', loud[0])
        self.assertEqual(said[-1], 'The job finished, but not cleanly: the results updater, a method or the backup did '
                                   'not finish. See the warnings above.')
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1')[-1]['content']['target'], fx.LAST_AT_START + 1)
        log = [json.loads(line) for line in (tree / research_job.JOB_LOG).read_text(encoding='ascii').splitlines()]
        self.assertEqual(len(log), 2)
        self.assertIn('the backup after the job was not made', log[1]['note'])
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, 'the next job is an ordinary one')

    def test_backup_bat_makes_one_now_under_the_lock(self):
        tree = self.tree()
        lock, seen = tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME, []
        real = backup.make_backup

        def watched(read, why, moment):
            """Note whether the lock is held while the backup is made."""
            seen.append((why, lock.exists()))
            return real(read, why, moment)

        with mock.patch.object(backup, 'make_backup', watched):
            code, printed = run_program(research_command, tree, 'backup')
        self.assertEqual((code, seen), (0, [('on demand', True)]))
        self.assertIn('Backup made of the DEV tree', printed)
        made = list(settings.read_settings(tree).backup_root.iterdir())
        self.assertEqual(len(made), 1)
        self.assertRegex(made[0].name, r'^DEV_\d{8}_\d{6}_on_demand\.zip$')
        self.assertFalse(lock.exists())


class MakeInstallableAndWhoUses(fx.JobCase):
    """Scheme sections 4 and 6: DEV's two commands that touch only DEV."""

    def said_by(self, function, *arguments) -> tuple:
        """(exit code, the lines said) of one of dev_tools' commands."""
        said = []
        with fx.ImportPath(arguments[0].tree_root):
            code = function(*arguments, say=said.append)
        return code, said

    def test_all_flags_every_method_with_its_fingerprint_and_infra_flags_the_engine_and_the_updater(self):
        tree = self.tree()
        (tree / 'src' / 'updater').mkdir()
        (tree / 'src' / 'updater' / 'results_updater.py').write_text('# the updater\n', encoding='ascii')
        read = settings.read_settings(tree)
        engine_before = code_identity.infrastructure_fingerprint(tree)
        code, said = self.said_by(dev_tools.make_installable, read, ['ALL', 'INFRA'], MOMENT)
        self.assertEqual(code, 0, said)
        self.assertEqual(len([line for line in said if line.startswith('flagged: ')]), 3, said)
        for name in ('TOY_A_V1', 'TOY_B_V1'):
            folder = fx.method_folder(tree, 'E_901', name)
            flag = method_flags.read_flag(folder / method_flags.INSTALLABLE_NAME)
            with fx.ImportPath(tree):
                from research.variant_folders import read_variant
                fingerprint = read_variant(tree / 'src' / 'methods', 'E_901', name).fingerprint
            self.assertEqual(flag, {'fingerprint': fingerprint, 'made': '2026-12-01 20:10'})
            self.assertEqual(method_flags.installable_state(folder, {'fingerprint': fingerprint}), method_flags.FLAGGED)
        flag = method_flags.read_flag(tree / 'src' / method_flags.INSTALLABLE_NAME)
        self.assertEqual((flag['fingerprint'], flag['updater_fingerprint']),
                         (engine_before, code_identity.updater_fingerprint(tree)))
        self.assertEqual(code_identity.infrastructure_fingerprint(tree), engine_before, 'a flag changes no fingerprint')
        self.assertFalse((tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME).exists())

    def test_a_flag_that_already_says_the_same_is_left_as_it_is(self):
        tree = self.tree()
        read = settings.read_settings(tree)
        self.said_by(dev_tools.make_installable, read, ['ALL', 'INFRA'], MOMENT)
        before = {**fx.files_under(tree, 'src')}
        code, said = self.said_by(dev_tools.make_installable, read, ['ALL', 'INFRA'], MOMENT.replace(year=2027))
        self.assertEqual(code, 0)
        self.assertEqual(len([line for line in said if line.startswith('already flagged, unchanged: ')]), 3, said)
        self.assertEqual(fx.files_under(tree, 'src'), before)

    def test_a_flag_is_out_of_date_as_soon_as_a_file_it_vouches_for_changes_and_is_put_right_by_making_it_again(self):
        tree = self.tree()
        read = settings.read_settings(tree)
        self.said_by(dev_tools.make_installable, read, ['ALL', 'INFRA'], MOMENT)
        folder = fx.method_folder(tree, 'E_901', 'TOY_A_V1')
        (folder / 'method.py').write_text((folder / 'method.py').read_text(encoding='ascii') + '# changed\n',
                                          encoding='ascii')
        (tree / 'src' / fx.ENGINE_FILE).write_text('# the engine, changed\n', encoding='ascii')
        with fx.ImportPath(tree):
            from research.variant_folders import read_variant
            now = {'fingerprint': read_variant(tree / 'src' / 'methods', 'E_901', 'TOY_A_V1').fingerprint}
        self.assertEqual(method_flags.installable_state(folder, now), method_flags.FLAG_OUT_OF_DATE)
        self.assertEqual(method_flags.installable_state(tree / 'src', dev_tools.infrastructure_fingerprints(tree)),
                         method_flags.FLAG_OUT_OF_DATE)
        self.assertEqual(method_flags.installable_state(fx.method_folder(tree, 'E_901', 'TOY_B_V1') / 'nowhere', now),
                         method_flags.NOT_FLAGGED)
        code, said = self.said_by(dev_tools.make_installable, read, ['E_901/TOY_A_V1', 'INFRA'], MOMENT)
        self.assertEqual((code, [line.split(':')[0] for line in said]), (0, ['flagged', 'flagged', 'Done.']), said)
        self.assertEqual(method_flags.installable_state(folder, now), method_flags.FLAGGED)

    def test_what_cannot_be_flagged_is_said_and_the_rest_is_still_flagged(self):
        tree = self.tree()
        read = settings.read_settings(tree)
        (fx.method_folder(tree, 'E_901', 'TOY_B_V1') / 'method.py.bak').write_text('x', encoding='ascii')
        code, said = self.said_by(dev_tools.make_installable, read, ['ALL'], MOMENT)
        self.assertEqual(code, 1)
        self.assertTrue(any(line.startswith('flagged: E_901/TOY_A_V1') for line in said), said)
        self.assertTrue(any(line.startswith('NOT FLAGGED: ') and 'TOY_B_V1' in line and 'fails its checks' in line
                            for line in said), said)
        self.assertFalse((fx.method_folder(tree, 'E_901', 'TOY_B_V1') / method_flags.INSTALLABLE_NAME).exists())
        code, said = self.said_by(dev_tools.make_installable, read, ['E_901/NO_SUCH_V1'], MOMENT)
        self.assertEqual(code, 1)
        self.assertIn('NOT FLAGGED: E_901/NO_SUCH_V1: there is no such method in this tree', said[0])
        code, said = self.said_by(dev_tools.make_installable, read, [], MOMENT)
        self.assertEqual((code, said[0].startswith('Nothing was named')), (1, True))

    def test_who_uses_lists_every_method_that_lists_the_helper_and_changes_nothing(self):
        tree = self.tree(variants=())
        helpers = tree / 'src' / 'methods' / '_shared'
        helpers.mkdir()
        (helpers / 'counts_v1.py').write_text('# a shared helper\n', encoding='ascii')
        (tree / 'src' / 'methods' / 'E_901').mkdir()
        (tree / 'src' / 'methods' / 'E_901' / 'core_v1.py').write_text('# the family\'s calculation\n', encoding='ascii')
        fx.add_toy_variant(tree, 'E_901', 'TOY_A_V1', helpers=('E_901/core_v1.py', '_shared/counts_v1.py'))
        fx.add_toy_variant(tree, 'E_901', 'TOY_B_V1', helpers=('E_901/core_v1.py',))
        fx.add_toy_variant(tree, 'E_902', 'TOY_C_V1')
        read = settings.read_settings(tree)
        before = fx.files_under(tree, '.', leave_out=())
        for helper, users in (('_shared\\counts_v1.py', ['E_901/TOY_A_V1']), ('counts_v1.py', ['E_901/TOY_A_V1']),
                              ('E_901/core_v1.py', ['E_901/TOY_A_V1', 'E_901/TOY_B_V1']),
                              ('method.py', ['E_901/TOY_A_V1', 'E_901/TOY_B_V1', 'E_902/TOY_C_V1'])):
            code, said = self.said_by(dev_tools.who_uses, read, helper)
            self.assertEqual((code, [line.split()[0] for line in said[:-1]]), (0, users), helper)
            self.assertIn(f'{len(users)} of 3 methods use', said[-1])
        code, said = self.said_by(dev_tools.who_uses, read, 'no_such_helper.py')
        self.assertEqual((code, said), (1, [said[-1]]))
        self.assertIn('0 of 3 methods use "no_such_helper.py"', said[0])
        self.assertEqual(fx.files_under(tree, '.', leave_out=()), before)

    def test_these_commands_are_devs_and_a_tree_of_another_role_refuses_them(self):
        tree = self.tree(role='QA')
        for arguments in (('make_installable', 'ALL'), ('who_uses', 'method.py')):
            code, printed = run_program(dev_command, tree, *arguments)
            self.assertEqual(code, dev_command.EXIT_BAD_COMMAND, arguments)
            self.assertIn('this tree is QA, but the command means the DEV tree', printed)
        self.assertFalse(any(name.endswith(method_flags.INSTALLABLE_NAME) for name in fx.files_under(tree, 'src')))

    def test_the_command_program_runs_both_commands_in_the_tree_it_lies_in(self):
        tree = self.tree()
        code, printed = run_program(dev_command, tree, 'make_installable', 'ALL', 'INFRA')
        self.assertEqual(code, 0, printed)
        self.assertEqual(printed.count('flagged: '), 3, printed)
        code, printed = run_program(dev_command, tree, 'who_uses', 'method.py')
        self.assertEqual(code, 0, printed)
        self.assertIn('2 of 2 methods use "method.py"', printed)
        code, printed = run_program(dev_command, tree, 'who_uses')
        self.assertEqual(code, dev_command.EXIT_BAD_COMMAND)
        code, printed = run_program(dev_command, tree, 'tidy')
        self.assertEqual((code, 'the first word must be one of' in printed), (dev_command.EXIT_BAD_COMMAND, True))

    def test_each_launcher_names_its_command_and_its_program_and_runs_python_isolated_without_a_cache(self):
        for name, program, word in (('Backup.bat', 'src\\research_command.py', 'backup'),
                                    ('Make_Installable.bat', 'deploy\\dev_command.py', 'make_installable'),
                                    ('Who_Uses.bat', 'deploy\\dev_command.py', 'who_uses')):
            text = (TREE_OF_THIS_FILE / name).read_bytes().decode('ascii')
            self.assertIn(f'set "TOOL=%ROOT%{program}"\r\n', text, name)
            self.assertIn(f'"%PY%" -I -B -u "%TOOL%" {word} %*\r\n', text, name)
            self.assertEqual(text.count('\r\n'), text.count('\n'), name)


if __name__ == '__main__':
    import unittest
    unittest.main()
