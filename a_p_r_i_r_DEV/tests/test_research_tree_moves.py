"""Tests of Retire, Copy_From_PROD and Restore, and of the command program that starts DEV's cross-tree commands.

Each test is named for the rule it proves and plants the fault that rule must catch. Everything runs on invented
draws and toy methods, in three invented trees under a temporary folder.
(The simple scheme v0.2 sections 3.1 rule 3, 4, 6 and 7.)
"""
import os
import shutil
import zipfile
from pathlib import Path
from unittest import mock

import research_fixtures as fx
import tree_fixtures as tf
from _common.game_profiles import get_profile

import dev_command                                          # noqa: E402  (tree_fixtures put deploy on the path)
import install_tools                                        # noqa: E402
import tree_parts                                           # noqa: E402
import tree_tools                                           # noqa: E402
from research import backup, method_flags, settings, tree_lock    # noqa: E402
from test_research_tree_commands import run_program        # noqa: E402
from tree_parts import CommandFailed, CommandRefused       # noqa: E402

GAME = fx.GAME
LAST = fx.LAST_AT_START
OTHER_GAME = 'OZLOTTO'
OTHER_LAST = get_profile(OTHER_GAME).first_draw + 16
B = 'E_901/TOY_B_V1'
METHOD_A = 'src/methods/E_901/TOY_A_V1/method.py'
ENGINE = 'src/' + fx.ENGINE_FILE


def no_room(read, why, moment):
    """A backup that cannot be made."""
    raise backup.BackupFailed(f'the backup of the {read.role} tree into T:\\x was not made: OSError: the disk is full')


class ThreeTrees(tf.TreesCase):
    """DEV, and QA and PROD created from it, each with its first job run."""

    def three(self, roles=('QA', 'PROD')) -> tuple:
        """Make the trees. Returns (dev, qa, prod); a tree not asked for is not made (its place is returned)."""
        dev = self.dev()
        fx.run_job(dev)
        for role in roles:
            fx.run_job(self.create(role))
        self.said.clear()
        return dev, self.place('QA'), self.place('PROD')

    def retired_file(self, role: str, name: str = 'TOY_B_V1') -> Path:
        """Where a method's I_AM_RETIRED lies in a tree."""
        return fx.method_folder(self.place(role), 'E_901', name) / method_flags.RETIRED_NAME


class Retire(ThreeTrees):
    """Scheme sections 4 and 6: I_AM_RETIRED in every tree that has the method, from that tree's own next draw."""

    def test_a_method_is_retired_in_every_tree_that_has_it_from_that_trees_own_next_draw_after_a_backup_of_each(self):
        dev, qa, prod = self.three(roles=('QA',))
        fx.write_results(qa, GAME, LAST + 2)                # QA holds two more draws than DEV
        fx.run_job(qa)
        seen = []

        def backup_watched(read, why, moment):
            """Note that nothing is written anywhere before every backup is made, and that the locks are held."""
            seen.append((read.role, why, self.retired_file('DEV').exists() or self.retired_file('QA').exists(),
                         self.lock_of('DEV').exists() and self.lock_of('QA').exists()))
            return Path('x.zip')

        code = self.command(tree_tools.retire, B, '  superseded   by TOY_B_V2 ', backup=backup_watched)
        self.assertEqual(code, 0, self.said_text())
        self.assertEqual(seen, [('DEV', 'before retire', False, True), ('QA', 'before retire', False, True)])
        self.assertEqual(method_flags.read_flag(self.retired_file('DEV')),
                         {f'retired_from_{GAME}': str(LAST + 1), 'reason': 'superseded by TOY_B_V2'})
        self.assertEqual(method_flags.read_flag(self.retired_file('QA')),
                         {f'retired_from_{GAME}': str(LAST + 3), 'reason': 'superseded by TOY_B_V2'})
        text = self.said_text()
        self.assertIn(f'  PROD: there is no tree at {prod}; passed over.', text)
        self.assertIn(f'  QA: {B} is retired from {GAME} draw {LAST + 3}.', text)
        self.assertIn('kept in Git: commit it', text)
        self.assertTrue(self.no_lock_is_left())
        self.assertEqual(fx.list_lines(qa, 'E_901', 'TOY_B_V1')[-1]['content']['target'], LAST + 3)
        self.assertEqual(fx.run_job(qa)[0], 0)
        self.assertEqual(fx.list_lines(qa, 'E_901', 'TOY_B_V1')[-1]['content']['target'], LAST + 2,
                         'QA\'s next job drops the forecast it had made for the retirement draw')
        self.assertEqual(fx.list_lines(qa, 'E_901', 'TOY_A_V1')[-1]['content']['target'], LAST + 3)

    def test_a_tree_where_it_is_already_retired_or_that_lacks_it_is_left_as_it_is(self):
        dev, qa, prod = self.three()
        method_flags.write_retired(self.retired_file('QA').parent, {GAME: 1150}, 'retired here long ago')
        held = self.retired_file('QA').read_bytes()
        shutil.rmtree(fx.method_folder(prod, 'E_901', 'TOY_B_V1'))
        self.assertEqual(self.command(tree_tools.retire, B, 'not wanted'), 0)
        self.assertEqual(self.backups, [('DEV', 'before retire')])
        self.assertTrue(self.retired_file('DEV').is_file())
        self.assertEqual(self.retired_file('QA').read_bytes(), held)
        self.assertIn(f'  QA: {B} is already retired there; its file is left as it is.', self.said_text())
        self.assertIn(f'  PROD: this tree does not have {B}.', self.said_text())
        self.said.clear()
        self.backups.clear()
        self.assertEqual(self.command(tree_tools.retire, B, 'not wanted'), 0)
        self.assertEqual((self.said[-1], self.backups), ('Nothing to do.', []))

    def test_a_name_no_tree_has_or_a_bad_name_or_no_plain_reason_writes_nothing(self):
        self.three()
        before = {role: self.snapshot(role) for role in self.places}
        for identity, reason, why in (('E_901/NO_SUCH_V1', 'not wanted', 'no tree has a method E_901/NO_SUCH_V1'),
                                      ('TOY_B_V1', 'not wanted', 'is not a method\'s name'),
                                      ('E_901/../TOY_B_V1', 'not wanted', 'is not a method\'s name'),
                                      (B, '   ', 'Give the reason'), (B, 'caf' + chr(233), 'Give the reason')):
            with self.assertRaisesRegex(CommandRefused, why):
                self.command(tree_tools.retire, identity, reason)
        self.assertEqual(({role: self.snapshot(role) for role in self.places}, self.backups), (before, []))
        self.assertTrue(self.no_lock_is_left())

    def test_if_one_trees_backup_cannot_be_made_no_tree_is_written(self):
        self.three()

        def second_fails(read, why, moment):
            """The backup of DEV is made; QA's fails."""
            return no_room(read, why, moment) if read.role == 'QA' else Path('x.zip')

        with self.assertRaisesRegex(CommandRefused, 'the backup of the QA tree .* was not made'):
            self.command(tree_tools.retire, B, 'not wanted', backup=second_fails)
        self.assertFalse(any(self.retired_file(role).exists() for role in self.places))
        self.assertTrue(self.no_lock_is_left())

    def test_while_a_command_works_in_one_of_the_trees_no_tree_is_written(self):
        self.three()
        with tree_lock.tree_lock(self.place('PROD'), 'research job', 'earlier'):
            with self.assertRaisesRegex(tree_lock.LaunchRefused, 'a process of this tree is running'):
                self.command(tree_tools.retire, B, 'not wanted')
        self.assertFalse(any(self.retired_file(role).exists() for role in self.places))
        self.assertEqual(self.backups, [])
        self.assertTrue(self.no_lock_is_left())


class CopyFromProd(ThreeTrees):
    """Scheme section 6: QA's software, data or both become PROD's; DEV's data; then the destination's job."""

    def diverged(self) -> tuple:
        """Three trees where PROD has moved on (more results, a retired method, a newer engine file) and QA has
        gone its own way (its own method, its own engine file)."""
        dev, qa, prod = self.three()
        fx.write_results(prod, GAME, LAST + 2)
        fx.write_results(prod, OTHER_GAME, OTHER_LAST)      # PROD holds both games' accepted results, as it must
        tf.edit(prod / ENGINE, '# PROD\'s engine')
        method_flags.write_retired(self.retired_file('PROD').parent, {GAME: LAST + 2}, 'retired in PROD')
        (prod / 'src' / method_flags.INSTALLABLE_NAME).write_text('fingerprint = planted\n', encoding='ascii')
        self.assertEqual(fx.run_job(prod)[0], 0)
        tf.edit(qa / ENGINE, '# QA\'s own engine')
        self.add_variant(qa, 'TOY_ONLY_IN_QA_V1')
        self.assertEqual(fx.run_job(qa)[0], 0)
        self.said.clear()
        return dev, qa, prod

    def test_both_makes_qa_the_twin_of_prod_after_a_backup_and_its_job_then_finds_nothing_to_make_again(self):
        dev, qa, prod = self.diverged()
        kept = {name: (qa / name).read_bytes() for name in ('ENVIRONMENT.ini', 'records/JOB_LOG.jsonl',
                                                             '.venv/Scripts/python.exe')}
        seen = []

        def backup_watched(read, why, moment):
            """Note that QA is still its old self when the backup is made, and that all three locks are held."""
            seen.append((read.role, why, (qa / ENGINE).read_bytes().endswith(b'# QA\'s own engine\n'),
                         all(self.lock_of(role).exists() for role in self.places)))
            return Path('QA_before.zip')

        self.assertEqual(self.command(tree_tools.copy_from_prod, 'both', 'QA', backup=backup_watched), 0,
                         self.said_text())
        self.assertEqual(seen, [('QA', 'before copy from PROD', True, True)])
        theirs = fx.files_under(prod, 'src')
        self.assertIn('src/methods/E_901/TOY_B_V1/I_AM_RETIRED', theirs)
        self.assertIn('src/methods/E_901/TOY_A_V1/IN_PLACE_SINCE', theirs)
        self.assertEqual(theirs.pop('src/I_AM_INSTALLABLE'), b'fingerprint = planted\n')
        self.assertEqual(fx.files_under(qa, 'src'), theirs, 'PROD\'s software, its retirements and establishments')
        self.assertEqual(fx.files_under(qa, 'source_data'), fx.files_under(prod, 'source_data'))
        log = kept.pop('records/JOB_LOG.jsonl')
        self.assertEqual({name: (qa / name).read_bytes() for name in kept}, kept, 'QA\'s own settings and Python')
        self.assertTrue((qa / 'records/JOB_LOG.jsonl').read_bytes().startswith(log), 'QA\'s own records, added to')
        self.assertEqual([role for role, _ in self.jobs], ['QA'])
        self.assertFalse(any('REBUIL' in line for line in self.job_said), self.job_said)
        self.assertTrue(any('written: 0 forecasts, 0 scores' in line for line in self.job_said), self.job_said)
        for name in ('TOY_A_V1', 'TOY_B_V1'):
            self.assertEqual(fx.list_lines(qa, 'E_901', name), fx.list_lines(prod, 'E_901', name))
        self.assertTrue(self.no_lock_is_left())

    def test_the_data_copied_is_prods_bytes_and_the_software_is_left_alone(self):
        dev, qa, prod = self.diverged()
        software = fx.files_under(qa, 'src')
        self.job_code = 0                                   # no job, so that the copy itself can be looked at
        self.assertEqual(self.command(tree_tools.copy_from_prod, 'data', 'QA'), 0)
        for folder in ('source_data', 'results/research'):
            self.assertEqual(fx.files_under(qa, folder, leave_out=()), fx.files_under(prod, folder, leave_out=()),
                             folder)
        self.assertEqual(fx.files_under(qa, 'src'), software)
        self.assertIn('4 files of accepted results', self.said_text())

    def test_the_software_copied_is_prods_and_the_data_is_left_alone_until_the_job(self):
        dev, qa, prod = self.diverged()
        data = fx.files_under(qa, 'source_data'), fx.files_under(qa, 'results/research', leave_out=())
        self.job_code = 0
        self.assertEqual(self.command(tree_tools.copy_from_prod, 'software', 'QA'), 0)
        self.assertEqual((fx.files_under(qa, 'source_data'), fx.files_under(qa, 'results/research', leave_out=())), data)
        self.assertFalse(fx.method_folder(qa, 'E_901', 'TOY_ONLY_IN_QA_V1').exists())
        self.assertEqual((qa / ENGINE).read_bytes(), (prod / ENGINE).read_bytes())
        self.assertEqual((qa / 'Backup.bat').read_bytes(), (prod / 'Backup.bat').read_bytes())

    def test_into_dev_only_data_is_copied_and_devs_software_stays_gits(self):
        dev, qa, prod = self.diverged()
        software = fx.files_under(dev, 'src')
        for what in ('software', 'both'):
            with self.assertRaisesRegex(CommandRefused, 'Into DEV only PROD\'s data is copied'):
                self.command(tree_tools.copy_from_prod, what, 'DEV')
        self.assertEqual(self.backups, [])
        self.assertEqual(self.command(tree_tools.copy_from_prod, 'data', 'DEV'), 0, self.said_text())
        self.assertEqual(self.backups, [('DEV', 'before copy from PROD')])
        self.assertEqual(fx.files_under(dev, 'src'), software)
        self.assertEqual(fx.files_under(dev, 'source_data'), fx.files_under(prod, 'source_data'))
        self.assertEqual([role for role, _ in self.jobs], ['DEV'])
        self.assertTrue(any('REBUILD: everything' in line for line in self.job_said),
                        'DEV\'s engine is not PROD\'s, so DEV\'s job makes the results again with its own')
        self.assertEqual(fx.read_last_draw(dev), LAST + 2)
        self.assertTrue(self.no_lock_is_left())

    def test_what_is_not_software_data_or_both_into_qa_or_dev_is_refused(self):
        self.three()
        for what, role in (('everything', 'QA'), ('data', 'PROD'), ('QA', 'data'), ('', '')):
            with self.assertRaisesRegex(CommandRefused, 'Give what to copy'):
                self.command(tree_tools.copy_from_prod, what, role)
        self.assertEqual((self.backups, self.jobs), ([], []))

    def test_nothing_is_copied_without_prod_a_backup_the_destinations_python_and_every_lock(self):
        dev, qa, prod = self.diverged()
        before = self.snapshot('QA')
        with self.assertRaisesRegex(CommandRefused, 'the disk is full. Nothing was replaced'):
            self.command(tree_tools.copy_from_prod, 'both', 'QA', backup=no_room)
        for role in self.places:
            with tree_lock.tree_lock(self.place(role), 'research job', 'earlier'):
                with self.assertRaisesRegex(tree_lock.LaunchRefused, 'a process of this tree is running'):
                    self.command(tree_tools.copy_from_prod, 'both', 'QA')
            self.assertTrue(self.no_lock_is_left())
        (qa / '.venv' / 'Scripts' / 'python.exe').unlink()
        with self.assertRaisesRegex(CommandRefused, 'has no Python environment of its own'):
            self.command(tree_tools.copy_from_prod, 'both', 'QA')
        tf.give_python(qa)
        (prod / 'ENVIRONMENT.ini').unlink()
        with self.assertRaisesRegex(settings.SettingsRefused, 'this folder is not a tree'):
            self.command(tree_tools.copy_from_prod, 'both', 'QA')
        self.assertEqual((self.snapshot('QA'), self.backups, self.jobs), (before, [], []))

    def test_prods_accepted_results_must_pass_the_reader_before_they_replace_another_trees(self):
        dev, qa, prod = self.diverged()
        before = self.snapshot('QA')
        master = prod / 'source_data' / f'{GAME}_results_master.csv'
        whole = master.read_bytes()
        master.write_bytes(whole[:-40])                     # cut short: no longer the file its ledger names
        for what, role in (('data', 'QA'), ('both', 'QA'), ('data', 'DEV')):
            with self.assertRaisesRegex(CommandRefused, f'the PROD tree\'s accepted results for {GAME} cannot be used'):
                self.command(tree_tools.copy_from_prod, what, role)
        master.write_bytes(whole)
        (prod / 'source_data' / f'{OTHER_GAME}_results_master.csv').unlink()
        with self.assertRaisesRegex(CommandRefused, f'accepted results for {OTHER_GAME} cannot be used'):
            self.command(tree_tools.copy_from_prod, 'data', 'QA')
        self.assertEqual((self.snapshot('QA'), self.backups, self.jobs), (before, [], []))
        self.assertEqual(self.command(tree_tools.copy_from_prod, 'software', 'QA'), 0, 'the software does not need them')
        self.assertTrue(self.no_lock_is_left())

    def test_a_prod_with_nothing_to_copy_never_empties_the_destination(self):
        dev, qa, prod = self.diverged()
        before = self.snapshot('QA')
        shutil.rmtree(prod / 'results' / 'research')
        with self.assertRaisesRegex(CommandRefused, 'the PROD tree holds no computed results'):
            self.command(tree_tools.copy_from_prod, 'data', 'QA')
        self.assertEqual((self.snapshot('QA'), self.backups, self.jobs), (before, [], []))
        for folder in ('results/research', 'no_such_folder'):
            with self.assertRaisesRegex(CommandFailed, 'is absent or holds nothing to copy; nothing was removed'):
                tree_parts.replace_folder(prod, qa, folder)
        (prod / 'only_flags').mkdir()
        (prod / 'only_flags' / 'I_AM_INSTALLABLE').write_text('x', encoding='ascii')
        with self.assertRaisesRegex(CommandFailed, 'holds nothing to copy'):
            tree_parts.replace_folder(prod, qa, 'only_flags', leave_out=('I_AM_INSTALLABLE',))
        self.assertEqual(self.snapshot('QA'), before, 'the source is listed before anything is removed')

    def test_a_copy_that_fails_part_way_says_so_runs_no_job_and_is_finished_by_running_it_again(self):
        dev, qa, prod = self.diverged()
        real, calls = tree_parts.copy_file, []

        def fails_at_the_fourth(source_root, target_root, relative):
            """Copy until the fourth file, then fail."""
            calls.append(relative)
            if len(calls) == 4:
                raise OSError(28, 'No space left on device', relative)
            return real(source_root, target_root, relative)

        with mock.patch.object(tree_parts, 'copy_file', fails_at_the_fourth):
            with self.assertRaisesRegex(CommandFailed, r'THE COPY DID NOT FINISH .*No space left.*run the\s+same command '
                                                       'again.*Restore.bat QA QA_20261201_201012_before_copy_from_PROD.zip'):
                self.command(tree_tools.copy_from_prod, 'both', 'QA')
        self.assertEqual(self.jobs, [])
        self.assertTrue(self.no_lock_is_left())
        self.assertEqual(self.command(tree_tools.copy_from_prod, 'both', 'QA'), 0, self.said_text())
        self.assertEqual(fx.files_under(qa, 'source_data'), fx.files_under(prod, 'source_data'))

    def test_the_software_copied_is_checked_against_prods(self):
        dev, qa, prod = self.diverged()
        real = tree_parts.copy_file

        def spoiled(source_root, target_root, relative):
            """Copy, but spoil the copy of one method file."""
            real(source_root, target_root, relative)
            if relative == METHOD_A:
                tf.edit(Path(target_root) / relative, '# not what PROD holds')

        with mock.patch.object(tree_parts, 'copy_file', spoiled):
            with self.assertRaisesRegex(CommandFailed, 'THE COPY DID NOT FINISH .*does not match PROD\'s when read back'):
                self.command(tree_tools.copy_from_prod, 'software', 'QA')
        self.assertEqual(self.jobs, [])


class Restore(ThreeTrees):
    """Scheme section 7: a tree is put back whole from one of its own backups; what it was is renamed aside."""

    def backed_up_then_changed(self) -> tuple:
        """DEV and QA; a real backup of QA; then QA changes. Returns (qa, the ZIP, what the ZIP holds)."""
        dev, qa, prod = self.three(roles=('QA',))
        made = backup.make_backup(self.settings('QA'), 'after job', tf.MOMENT)
        with zipfile.ZipFile(made) as archive:
            held = {info.filename: archive.read(info) for info in archive.infolist()}
        tf.edit(qa / ENGINE, '# changed after the backup')
        (qa / 'results' / 'research' / 'newer.txt').write_text('made after the backup', encoding='ascii')
        self.said.clear()
        return qa, made, held

    def test_a_restore_puts_the_tree_back_exactly_as_its_backup_holds_it_and_keeps_what_it_was_aside(self):
        qa, made, held = self.backed_up_then_changed()
        as_it_was = self.snapshot('QA')
        self.assertEqual(self.command(tree_tools.restore, 'QA', made.name), 0, self.said_text())
        self.assertEqual(self.backups, [('QA', 'before restore')])
        self.assertEqual(self.snapshot('QA'), held, 'nothing newer is mixed in; no .venv, which is built again')
        self.assertEqual(settings.read_settings(qa, must_be='QA').tree_root, qa)
        aside = qa.with_name(qa.name + '_set_aside_20261201_201012')
        self.assertEqual(fx.files_under(aside, '.', leave_out=()), as_it_was, 'whole, its .venv too, and no lock')
        with self.assertRaisesRegex(settings.SettingsRefused, 'does not end with QA'):
            settings.read_settings(aside)
        self.assertEqual(sorted(path.name for path in self.root.iterdir()),
                         ['three_DEV', 'three_QA', 'three_QA_set_aside_20261201_201012', 'three_backups'])
        self.assertTrue(self.no_lock_is_left())
        self.assertIn(f'the tree as it was is kept at {aside}', self.said_text())
        self.assertIn('It has no Python environment', self.said_text())

    def test_a_tree_that_is_gone_is_restored_into_its_empty_place_from_a_backup_given_by_its_full_path(self):
        qa, made, held = self.backed_up_then_changed()
        elsewhere = self.root / 'kept_elsewhere.zip'
        shutil.copyfile(made, elsewhere)
        shutil.rmtree(qa)
        self.assertEqual(self.command(tree_tools.restore, 'QA', str(elsewhere)), 0, self.said_text())
        self.assertEqual((self.snapshot('QA'), self.backups), (held, []))
        self.assertFalse(any('set_aside' in path.name or 'being_restored' in path.name for path in self.root.iterdir()))

    def test_only_a_whole_backup_of_that_very_tree_is_restored(self):
        qa, made, held = self.backed_up_then_changed()
        self.create('PROD')
        folder = self.places['QA'][1]
        of_prod = backup.make_backup(self.settings('PROD'), 'on demand', tf.MOMENT)
        shutil.copyfile(of_prod, folder / 'of_prod.zip')

        def zip_with(name: str, entries: dict) -> None:
            """Write a ZIP into QA's backup folder."""
            with zipfile.ZipFile(folder / name, 'w') as archive:
                for entry, data in entries.items():
                    archive.writestr(entry, data)

        own = held['ENVIRONMENT.ini'].decode('utf-8')
        zip_with('moved.zip', {**held, 'ENVIRONMENT.ini': own.replace(f'{qa}\r\n', f'{self.root / "old_QA"}\r\n')})
        zip_with('no_settings.zip', {name: data for name, data in held.items() if name != 'ENVIRONMENT.ini'})
        zip_with('bad_settings.zip', {**held, 'ENVIRONMENT.ini': 'role = QA\n'})
        zip_with('escapes.zip', {**held, '../outside.txt': b'x'})
        (folder / 'not_a_zip.zip').write_bytes(b'this is not a ZIP file')
        raw = bytearray(made.read_bytes())
        at = raw.index(b'ENVIRONMENT.ini') + 60
        raw[at:at + 8] = b'\xff' * 8
        (folder / 'damaged.zip').write_bytes(bytes(raw))
        before = self.snapshot('QA')
        for name, why in (('of_prod.zip', 'is the backup of the PROD tree at .*not of the QA tree'),
                          ('moved.zip', 'is the backup of the QA tree at .*old_QA, not of the QA tree at'),
                          ('no_settings.zip', 'holds no ENVIRONMENT.ini, so it is not the backup of a tree'),
                          ('bad_settings.zip', 'not a readable settings file'),
                          ('escapes.zip', 'holds a name that does not stay inside a tree'),
                          ('not_a_zip.zip', 'cannot be read as a backup'),
                          ('damaged.zip', 'is damaged|cannot be read as a backup'),
                          ('no_such.zip', 'was not found')):
            with self.assertRaisesRegex(CommandRefused, why):
                self.command(tree_tools.restore, 'QA', name)
        with self.assertRaisesRegex(CommandRefused, 'DEV is not restored by this command'):
            self.command(tree_tools.restore, 'DEV', made.name)
        with self.assertRaisesRegex(CommandRefused, 'Give the tree'):
            self.command(tree_tools.restore, 'TEST', made.name)
        self.assertEqual((self.snapshot('QA'), self.backups), (before, []))
        self.assertFalse((self.root / 'outside.txt').exists())
        self.assertFalse(any('set_aside' in path.name or 'being_restored' in path.name for path in self.root.iterdir()))

    def test_a_folder_that_holds_files_but_is_not_a_tree_is_not_touched(self):
        qa, made, held = self.backed_up_then_changed()
        (qa / 'ENVIRONMENT.ini').unlink()
        before = self.snapshot('QA')
        with self.assertRaisesRegex(CommandRefused, 'holds files but no settings file.*Rename it away by hand'):
            self.command(tree_tools.restore, 'QA', made.name)
        self.assertEqual(self.snapshot('QA'), before)

    def test_the_tree_is_not_touched_while_a_command_works_in_it_or_if_the_backup_before_cannot_be_made(self):
        qa, made, held = self.backed_up_then_changed()
        before = self.snapshot('QA')
        with tree_lock.tree_lock(qa, 'research job', 'earlier'):
            with self.assertRaisesRegex(tree_lock.LaunchRefused, 'a process of this tree is running'):
                self.command(tree_tools.restore, 'QA', made.name)
        with self.assertRaisesRegex(CommandRefused, 'the disk is full. Nothing was replaced'):
            self.command(tree_tools.restore, 'QA', made.name, backup=no_room)
        self.assertEqual(self.snapshot('QA'), before)
        self.assertTrue(self.no_lock_is_left())
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ['three_DEV', 'three_QA', 'three_backups'])

    def test_a_backup_that_cannot_be_unpacked_leaves_the_tree_as_it_was_and_no_half_copy(self):
        qa, made, held = self.backed_up_then_changed()
        before = self.snapshot('QA')
        real = zipfile.ZipFile.extractall

        def half(archive, path=None, members=None, pwd=None):
            """Unpack three files, then fail."""
            real(archive, path, archive.namelist()[:3])
            raise OSError(28, 'No space left on device')

        with mock.patch.object(zipfile.ZipFile, 'extractall', half):
            with self.assertRaisesRegex(CommandRefused, r'could not be unpacked .*The QA\s+tree was not touched'):
                self.command(tree_tools.restore, 'QA', made.name)
        self.assertEqual(self.snapshot('QA'), before)
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ['three_DEV', 'three_QA', 'three_backups'])
        self.assertTrue(self.no_lock_is_left())

    def test_if_the_last_rename_fails_the_owner_is_told_where_everything_is(self):
        qa, made, held = self.backed_up_then_changed()
        as_it_was = self.snapshot('QA')
        real, calls = os.rename, []

        def second_fails(source, target):
            """Rename the tree aside; fail to give the fresh folder its name."""
            calls.append(Path(target).name)
            if len(calls) == 2:
                raise PermissionError(13, 'Access is denied', str(target))
            return real(source, target)

        with mock.patch.object(tree_tools.os, 'rename', second_fails):
            with self.assertRaisesRegex(CommandFailed, 'THE RESTORE DID NOT FINISH .*The restored copy is whole at '
                                                       '.*three_QA_being_restored_20261201_201012. The tree as it was is '
                                                       'at .*three_QA_set_aside_20261201_201012'):
                self.command(tree_tools.restore, 'QA', made.name)
        self.assertEqual(fx.files_under(self.root / 'three_QA_set_aside_20261201_201012', '.', leave_out=()), as_it_was)
        self.assertEqual(fx.files_under(self.root / 'three_QA_being_restored_20261201_201012', '.', leave_out=()), held)
        self.assertFalse(qa.exists())
        self.assertFalse(self.lock_of('DEV').exists())


class TheCommandProgram(ThreeTrees):
    """deploy/dev_command.py: what the owner types reaches the right command with the right words."""

    def typed(self, *arguments) -> tuple:
        """Run the command program in the DEV tree with stand-ins for the five commands. Returns (exit code,
        what was printed, [(the command, its arguments, its options)])."""
        reached = []

        def stand_in(name):
            """A command that notes how it was called."""
            return lambda read, *given, **options: reached.append((name, given, {
                key: value for key, value in options.items() if key != 'moment'})) or 0

        with mock.patch.multiple(install_tools, create_tree=stand_in('create_tree'), install=stand_in('install')), \
                mock.patch.multiple(tree_tools, retire=stand_in('retire'), copy_from_prod=stand_in('copy_from_prod'),
                                    restore=stand_in('restore')):
            code, printed = run_program(dev_command, self.place('DEV'), *arguments)
        return code, printed, reached

    def test_each_command_is_reached_with_the_words_typed(self):
        self.dev()
        for arguments, expected in (
                (('create_tree', 'qa'), ('create_tree', ('QA',), {})),
                (('install', 'QA'), ('install', ('QA',), {'show': False})),
                (('install', 'prod', '--show'), ('install', ('PROD',), {'show': True})),
                (('install', '--show', 'QA'), ('install', ('QA',), {'show': True})),
                (('retire', 'E_901\\TOY_B_V1', 'superseded', 'by', 'V2'), ('retire', (B, 'superseded by V2'), {})),
                (('copy_from_prod', 'BOTH', 'qa'), ('copy_from_prod', ('both', 'QA'), {})),
                (('copy_from_prod', 'data', 'dev'), ('copy_from_prod', ('data', 'DEV'), {})),
                (('restore', 'qa', 'QA_1.zip'), ('restore', ('QA', 'QA_1.zip'), {}))):
            code, printed, reached = self.typed(*arguments)
            self.assertEqual((code, reached), (0, [expected]), (arguments, printed))

    def test_a_command_typed_with_too_few_or_too_many_words_does_nothing_and_shows_how_it_is_typed(self):
        self.dev()
        for arguments, shown in ((('create_tree',), 'Create_Tree.bat QA'), (('create_tree', 'QA', 'PROD'), 'Create_Tree'),
                                 (('install',), 'Install.bat QA [--show]'), (('install', 'QA', 'PROD'), 'Install.bat'),
                                 (('install', '--show'), 'Install.bat'), (('retire', B), 'Retire.bat family/variant'),
                                 (('copy_from_prod', 'data'), 'Copy_From_PROD.bat software|data|both QA'),
                                 (('restore', 'QA'), 'Restore.bat QA|PROD backup_file.zip')):
            code, printed, reached = self.typed(*arguments)
            self.assertEqual((code, reached), (2, []), arguments)
            self.assertIn('REFUSED: the command was not typed as it must be. ' + shown, printed)

    def test_a_refusal_and_a_failure_are_printed_and_end_with_exit_code_2(self):
        self.dev(flag=())
        code, printed = run_program(dev_command, self.place('DEV'), 'create_tree', 'QA')
        self.assertEqual(code, 2)
        self.assertIn('REFUSED: the infrastructure is not flagged in DEV', printed)
        code, printed = run_program(dev_command, self.place('DEV'), 'install', 'QA')
        self.assertEqual(code, 2)
        self.assertIn('REFUSED: ', printed)
        self.assertIn('this folder is not a tree', printed)

        def fails(read, role, **options):
            """An install that fails after it began."""
            raise CommandFailed('THE INSTALL DID NOT FINISH (planted).')

        with mock.patch.object(install_tools, 'install', fails):
            code, printed = run_program(dev_command, self.place('DEV'), 'install', 'QA')
        self.assertEqual((code, printed.strip()), (2, 'THE INSTALL DID NOT FINISH (planted).'))

    def test_these_commands_run_from_dev_only(self):
        dev, qa, prod = self.three(roles=('QA',))
        for arguments in (('create_tree', 'PROD'), ('install', 'PROD'), ('retire', B, 'x'),
                          ('copy_from_prod', 'data', 'DEV'), ('restore', 'PROD', 'x.zip')):
            code, printed = run_program(dev_command, qa, *arguments)
            self.assertEqual(code, 2, arguments)
            self.assertIn('this tree is QA, but the command means the DEV tree', printed)
        self.assertFalse(prod.exists())

    def test_each_launcher_names_its_command_and_runs_devs_command_program(self):
        for name, word in (('Create_Tree.bat', 'create_tree'), ('Install.bat', 'install'), ('Retire.bat', 'retire'),
                           ('Copy_From_PROD.bat', 'copy_from_prod'), ('Restore.bat', 'restore')):
            text = (tf.TREE_OF_THIS_FILE / name).read_bytes().decode('ascii')
            self.assertIn('set "TOOL=%ROOT%deploy\\dev_command.py"\r\n', text, name)
            self.assertIn(f'"%PY%" -I -B -u "%TOOL%" {word} %*\r\n', text, name)
            self.assertEqual(text.count('\r\n'), text.count('\n'), name)
            self.assertNotIn(name, tree_parts.ROOT_FILES, 'a launcher of DEV only: never copied into another tree')


if __name__ == '__main__':
    import unittest
    unittest.main()
