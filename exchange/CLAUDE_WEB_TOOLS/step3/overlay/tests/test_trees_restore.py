"""Tests of the recovery kit and of the restore, on invented trees and invented process tables.

What this file is for
    It proves what the deployment design's sections 11 and 12 say: a kit that checks itself; a backup verified
    in full before anything is touched; no other Python program on the PC, before the old tree is renamed and
    after; the old tree set aside by one rename; the fresh tree exactly the backup's payload, plus one record;
    the settings file last; the same command again after a stop; the reconciliation after an unzip by hand; and
    the one exception for a stale orphan marker, no part of it waived. The reader of Windows' own process table
    cannot run in the cloud: every table here is invented, and that reader meets Windows in the joined rehearsal.

Which of the project's own modules it uses
    deploy/restore_tool.py, deploy/recovery_kit.py, research.snapshot, research.launch_guard; the fixtures.
"""
import ast
import hashlib
import json
import os
import shutil
import sys
import time
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import recovery_kit                                          # noqa: E402  (after the path line above)
import restore_tool                                          # noqa: E402
import research_fixtures as fx                               # noqa: E402
from research import launch_guard, snapshot                  # noqa: E402
from research.settings import read_settings                  # noqa: E402

BACKED_UP_AT = datetime(2026, 12, 1, 9, 40, 12, tzinfo=timezone.utc)
RESTORED_AT = datetime(2026, 12, 3, 18, 5, 0, tzinfo=timezone.utc)
ORPHAN = restore_tool.ORPHAN_MARKER
# An invented process table in which only this test's own Python runs, started by a command window.
ME = os.getpid()
QUIET_TABLE = [(4, 0, 'System', 1), (900, 4, 'cmd.exe', 50), (ME, 900, 'python.exe', 60)]


def tree_as_hashes(folder: Path) -> dict:
    """Every file under a folder with the SHA-256 of its bytes: {path: sha256}."""
    return {path.relative_to(folder).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(folder.rglob('*')) if path.is_file()}


class ABackedUpTreeAndItsKit(fx.JobCase):
    """An invented QA tree, one verified backup of it, an invented DEV whose infrastructure is marked ready, and
    a recovery kit built from that DEV and unpacked, as the owner would have them on the day of a restore."""

    def setUp(self):
        super().setUp()
        self.qa = self.tree(with_source=False)
        self.settings = read_settings(self.qa)
        self.make_backup()
        self.dev = self.root / 'invented_dev'
        marked = []
        for source, _kit_name in recovery_kit.KIT_FILES:
            (self.dev / source).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPOSITORY_ROOT / source, self.dev / source)
            marked.append({'path': source, 'sha256': hashlib.sha256((self.dev / source).read_bytes()).hexdigest()})
        (self.dev / recovery_kit.INFRA_MARKER_PATH).write_text(json.dumps({'install_tool': marked}), encoding='ascii')
        self.kit_result = recovery_kit.build_kit(self.dev, self.settings.backup_root, 'ab12' * 16,
                                                 now=lambda: BACKED_UP_AT)
        self.kit = self.root / 'unpacked_kit'
        with zipfile.ZipFile(self.kit_result.path) as archive:
            archive.extractall(self.kit)
        self.said = []

    def make_backup(self) -> None:
        """Make the one backup of the tree as it stands, and remember what the tree held."""
        result = snapshot.attempt_snapshot(self.settings, 'MANUAL', now=lambda: BACKED_UP_AT)
        self.assertTrue(result.made, result.reason)
        self.backup = result.path
        self.backed_up = tree_as_hashes(self.qa)             # with the backup log's line, written after the ZIP
        with zipfile.ZipFile(self.backup) as archive:
            manifest = json.loads(archive.read(snapshot.MANIFEST_NAME))
        self.payload = {entry['path']: entry['sha256'] for entry in manifest['files']}

    def change_the_tree(self) -> None:
        """What happens to a tree after its backup: a file changed, one added, one removed."""
        with open(self.qa / 'src' / 'toy_other.py', 'ab') as handle:
            handle.write(b'# changed after the backup\r\n')
        (self.qa / 'records' / 'later.txt').write_bytes(b'written after the backup\r\n')
        (self.qa / 'src' / 'toy_derived_code.py').unlink()

    def restore(self, table=QUIET_TABLE, ready=True, **options) -> int:
        """Run the restore of the backup from the unpacked kit with an invented process table."""
        options.setdefault('read_processes', lambda: table)
        options.setdefault('now', lambda: RESTORED_AT)
        return restore_tool.restore(self.backup, kit_folder=self.kit, environment=lambda tree: ready,
                                    say=self.said.append, **options)

    def text(self) -> str:
        return '\n'.join(self.said)

    def set_aside(self) -> list:
        """The folders beside the tree that a restore set aside."""
        return sorted(self.qa.parent.glob(self.qa.name + '_SET_ASIDE_*'))

    def assert_nothing_was_touched(self, before: dict) -> None:
        self.assertEqual(tree_as_hashes(self.qa), before)
        self.assertEqual(self.set_aside(), [])
        self.assertIn('nothing was touched', self.said[-1])


class TheRecoveryKit(ABackedUpTreeAndItsKit):
    """Deployment design section 11."""

    def test_it_is_named_for_its_time_and_software_state_and_holds_the_tool_with_its_own_list(self):
        self.assertTrue(self.kit_result.made, self.kit_result.reason)
        self.assertRegex(self.kit_result.path.name, r'^KIT_\d{8}_\d{6}_ab12ab12ab12\.zip$')
        self.assertTrue(self.kit_result.line().startswith('RECOVERY KIT WRITTEN AND CHECKED: '))
        with zipfile.ZipFile(self.kit_result.path) as archive:
            self.assertEqual(sorted(archive.namelist()),
                             ['HOW_TO_RESTORE.txt', 'KIT_MANIFEST.json', 'Restore.bat', 'restore_tool.py'])
        digest = hashlib.sha256(self.kit_result.path.read_bytes()).hexdigest()
        self.assertEqual(Path(str(self.kit_result.path) + '.sha256').read_bytes(),
                         f'{digest} *{self.kit_result.path.name}\r\n'.encode('ascii'))
        self.assertEqual(restore_tool.check_kit(self.kit)['software_fingerprint'], 'ab12' * 16)
        self.assertEqual((self.kit / 'restore_tool.py').read_bytes(),
                         (REPOSITORY_ROOT / 'deploy' / 'restore_tool.py').read_bytes())

    def test_a_kit_file_that_is_not_the_one_the_infrastructure_marker_lists_means_no_kit(self):
        with open(self.dev / 'deploy' / 'restore_tool.py', 'ab') as handle:
            handle.write(b'# changed after it was marked\r\n')
        before = sorted(entry.name for entry in self.settings.backup_root.iterdir())
        result = recovery_kit.build_kit(self.dev, self.settings.backup_root, 'cd34' * 16, now=lambda: RESTORED_AT)
        self.assertFalse(result.made)
        self.assertIn('deploy/restore_tool.py in DEV is not the file', result.line())
        (self.dev / recovery_kit.INFRA_MARKER_PATH).unlink()
        self.assertIn('not marked ready', recovery_kit.build_kit(self.dev, self.settings.backup_root, 'cd34' * 16).reason)
        self.assertEqual(sorted(entry.name for entry in self.settings.backup_root.iterdir()), before)

    def test_a_kit_that_cannot_be_written_is_a_result_and_never_an_exception(self):
        blocked = self.root / 'a_file_not_a_folder'
        blocked.write_bytes(b'x')
        result = recovery_kit.build_kit(self.dev, blocked, 'cd34' * 16)
        self.assertFalse(result.made)
        self.assertTrue(result.line().startswith('RECOVERY KIT NOT WRITTEN: '))

    def test_a_kit_that_does_not_read_back_as_it_was_written_is_not_a_kit(self):
        before = sorted(entry.name for entry in self.settings.backup_root.iterdir())
        with mock.patch.object(zipfile.ZipFile, 'read', return_value=b'not what was written'):
            result = recovery_kit.build_kit(self.dev, self.settings.backup_root, 'cd34' * 16, now=lambda: RESTORED_AT)
        self.assertFalse(result.made)
        self.assertIn('the kit read back is not what was written', result.reason)
        self.assertEqual(sorted(entry.name for entry in self.settings.backup_root.iterdir()), before)

    def test_a_backup_names_the_kit_of_its_software_state(self):
        fingerprint = snapshot.software_fingerprint(self.qa)
        kit = recovery_kit.build_kit(self.dev, self.settings.backup_root, fingerprint, now=lambda: RESTORED_AT)
        later = snapshot.attempt_snapshot(self.settings, 'MANUAL', now=lambda: RESTORED_AT)
        with zipfile.ZipFile(later.path) as archive:
            self.assertEqual(json.loads(archive.read(snapshot.MANIFEST_NAME))['recovery_kit'], kit.path.name)

    def test_the_restore_tool_is_one_file_of_the_standard_library_and_ends_no_process(self):
        source = (REPOSITORY_ROOT / 'deploy' / 'restore_tool.py').read_text(encoding='ascii')
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.add(node.module.split('.')[0])
        self.assertLessEqual(imported, set(sys.stdlib_module_names) | {'__future__'})
        for word in ('.kill(', '.terminate(', 'taskkill', 'TerminateProcess', 'signal'):
            self.assertNotIn(word, source)

    def test_a_kit_whose_own_list_does_not_name_exactly_its_three_files_refuses(self):
        whole = json.loads((self.kit / 'KIT_MANIFEST.json').read_bytes())
        before = tree_as_hashes(self.qa)
        for what, files in (('none', []), ('two of three', whole['files'][:2]),
                            ('one twice', whole['files'] + whole['files'][:1])):
            with self.subTest(what=what):
                self.said.clear()
                (self.kit / 'KIT_MANIFEST.json').write_text(json.dumps(dict(whole, files=files)), encoding='ascii')
                (self.kit / 'restore_tool.py').write_bytes(b'# not the tool: and the short list does not notice\r\n')
                self.assertEqual(self.restore(), restore_tool.EXIT_REFUSED)
                self.assertIn('it does not list exactly HOW_TO_RESTORE.txt, Restore.bat, restore_tool.py', self.text())
                self.assert_nothing_was_touched(before)

    def test_a_kit_that_cannot_be_given_its_name_leaves_nothing_that_looks_like_one(self):
        before = sorted(entry.name for entry in self.settings.backup_root.iterdir())
        with mock.patch.object(recovery_kit.os, 'replace', side_effect=OSError('invented: the rename failed')):
            result = recovery_kit.build_kit(self.dev, self.settings.backup_root, 'cd34' * 16, now=lambda: RESTORED_AT)
        self.assertFalse(result.made)
        self.assertIn('the rename failed', result.line())
        self.assertEqual(sorted(entry.name for entry in self.settings.backup_root.iterdir()), before)
        beside = self.settings.backup_root / 'KIT_20261203_000000_cd34cd34cd34.zip.sha256'
        stamp = RESTORED_AT.astimezone().strftime('%Y%m%d_%H%M%S')
        earlier = self.settings.backup_root / f'KIT_{stamp}_cd34cd34cd34.zip.sha256'
        earlier.write_bytes(b'left by another attempt')
        result = recovery_kit.build_kit(self.dev, self.settings.backup_root, 'cd34' * 16, now=lambda: RESTORED_AT)
        self.assertFalse(result.made)
        self.assertIn('Nothing was removed', result.reason)
        self.assertEqual(earlier.read_bytes(), b'left by another attempt')
        self.assertFalse(beside.exists())

    def test_a_kit_is_never_left_with_its_name_and_without_its_sha256(self):
        opening = open

        def sha256_cannot_be_written(path, *rest, **more):
            if str(path).endswith('.sha256'):
                raise OSError('invented: the ".sha256" could not be written')
            return opening(path, *rest, **more)

        before = sorted(entry.name for entry in self.settings.backup_root.iterdir())
        with mock.patch('builtins.open', sha256_cannot_be_written):
            result = recovery_kit.build_kit(self.dev, self.settings.backup_root, 'cd34' * 16, now=lambda: RESTORED_AT)
        self.assertFalse(result.made)
        self.assertEqual(sorted(entry.name for entry in self.settings.backup_root.iterdir()), before)

    def test_the_tool_sets_no_time_limit_that_would_end_the_python_it_starts(self):
        source = (REPOSITORY_ROOT / 'deploy' / 'restore_tool.py').read_text(encoding='ascii')
        calls = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                 and node.func.value.id == 'subprocess']
        self.assertEqual([call.func.attr for call in calls], ['run'])
        self.assertEqual([keyword.arg for keyword in calls[0].keywords], ['capture_output'])
        for word in ('timeout=', 'Popen', 'check_output', 'wait('):
            self.assertNotIn(word, source)

    def test_a_kit_whose_file_was_damaged_refuses_before_anything_else(self):
        before = tree_as_hashes(self.qa)
        with open(self.kit / 'HOW_TO_RESTORE.txt', 'ab') as handle:
            handle.write(b'damaged')
        self.assertEqual(self.restore(), restore_tool.EXIT_REFUSED)
        self.assertIn('is missing or is not the file the kit was made with', self.text())
        self.assert_nothing_was_touched(before)


class ARestore(ABackedUpTreeAndItsKit):
    """Deployment design section 12: the steps, and what the tree is afterwards."""

    def test_the_tree_is_put_back_exactly_with_one_record_and_the_old_tree_is_set_aside_whole(self):
        self.change_the_tree()
        changed = tree_as_hashes(self.qa)
        self.assertEqual(self.restore(), restore_tool.EXIT_RESTORED, self.text())
        stamp = RESTORED_AT.astimezone().strftime('%Y%m%d_%H%M%S')
        record_name = f'records/RESTORE_{stamp}.json'
        now = tree_as_hashes(self.qa)
        record = json.loads((self.qa / record_name).read_bytes())
        self.assertEqual({path: digest for path, digest in now.items() if path != record_name}, self.payload)
        self.assertEqual((self.qa / record_name).read_bytes().count(b'\n'), (self.qa / record_name).read_bytes().count(b'\r\n'))
        [aside] = self.set_aside()
        self.assertEqual(aside.name, f'{self.qa.name}_SET_ASIDE_{stamp}')
        was = tree_as_hashes(aside)
        was['ENVIRONMENT.ini'] = was.pop('ENVIRONMENT.ini.SET_ASIDE')        # renamed so that no launcher runs there
        self.assertEqual(was, changed)
        self.assertEqual((record['backup'], record['backup_sha256'], record['set_aside_as'], record['tree_root']),
                         (self.backup.name, hashlib.sha256(self.backup.read_bytes()).hexdigest(), str(aside), str(self.qa)))
        self.assertFalse((self.qa / restore_tool.PROGRESS_FILE).exists())
        self.assertIn('RESTORE - END - RESTORED AND READY TO RUN.', self.text())
        self.assertIn('Nothing else was done', self.said[-1])
        launch_guard.check_no_unfinished_operation(self.qa)
        self.assertEqual(read_settings(self.qa).role, 'QA')

    def test_it_never_says_ready_when_the_restored_environment_does_not_start(self):
        self.assertEqual(self.restore(ready=False), restore_tool.EXIT_RESTORED)
        self.assertIn('RESTORED; ENVIRONMENT NOT READY.', self.text())
        self.assertNotIn('READY TO RUN', self.text())
        self.assertFalse(restore_tool.environment_starts(self.qa))       # the invented environment is no Python

    def test_a_tree_that_is_gone_is_put_back_with_nothing_set_aside(self):
        shutil.rmtree(self.qa)
        self.assertEqual(self.restore(), restore_tool.EXIT_RESTORED, self.text())
        self.assertEqual(self.set_aside(), [])
        self.assertIn(f'there was no folder at {self.qa}', self.text())
        self.assertTrue(self.payload.items() <= tree_as_hashes(self.qa).items())

    def test_the_progress_file_is_written_first_and_the_settings_file_last(self):
        written, write = [], restore_tool._write_whole

        def note_then_write(path, data):
            written.append(Path(path).relative_to(self.qa).as_posix())
            self.assertEqual((self.qa / 'ENVIRONMENT.ini').exists(), False)
            write(path, data)

        with mock.patch.object(restore_tool, '_write_whole', note_then_write):
            self.assertEqual(self.restore(), restore_tool.EXIT_RESTORED, self.text())
        self.assertEqual(written[0], restore_tool.PROGRESS_FILE)
        self.assertEqual(written[-1], 'ENVIRONMENT.ini')
        self.assertRegex(written[1], r'^records/RESTORE_\d{8}_\d{6}\.json$')

    def test_empty_folders_and_file_times_come_back_as_the_backup_kept_them(self):
        (self.qa / 'scratch' / 'empty').mkdir(parents=True)
        os.utime(self.qa / 'src' / 'toy_other.py', (1_700_000_000, 1_700_000_000))
        self.make_backup_again()
        self.assertEqual(self.restore(), restore_tool.EXIT_RESTORED, self.text())
        self.assertTrue((self.qa / 'scratch' / 'empty').is_dir())
        self.assertLess(abs((self.qa / 'src' / 'toy_other.py').stat().st_mtime - 1_700_000_000), 2.5)

    def test_the_settings_file_comes_back_with_its_time_and_its_checked_bytes(self):
        os.utime(self.qa / 'ENVIRONMENT.ini', (1_700_000_000, 1_700_000_000))
        self.make_backup_again()
        self.assertEqual(self.restore(), restore_tool.EXIT_RESTORED, self.text())
        self.assertLess(abs((self.qa / 'ENVIRONMENT.ini').stat().st_mtime - 1_700_000_000), 2.5)
        self.assertEqual(hashlib.sha256((self.qa / 'ENVIRONMENT.ini').read_bytes()).hexdigest(),
                         self.payload['ENVIRONMENT.ini'])

    def test_a_settings_file_that_reads_from_the_backup_as_other_bytes_the_second_time_is_not_written(self):
        read, reads = zipfile.ZipFile.read, []

        def second_reading_differs(archive, name, *rest):
            data = read(archive, name, *rest)
            if name == 'ENVIRONMENT.ini':
                reads.append(name)
                if len(reads) == 2:                          # the first is the check before anything is touched
                    return data + b'# other bytes\r\n'
            return data

        with mock.patch.object(zipfile.ZipFile, 'read', second_reading_differs):
            self.assertEqual(self.restore(), restore_tool.EXIT_STOPPED, self.text())
        self.assertIn('read from the backup a second time is not the file its manifest lists', self.text())
        self.assertFalse((self.qa / 'ENVIRONMENT.ini').exists())
        self.assertTrue((self.qa / restore_tool.PROGRESS_FILE).is_file())

    def make_backup_again(self) -> None:
        """A second backup, a minute after the first, of the tree as it stands now."""
        result = snapshot.attempt_snapshot(self.settings, 'MANUAL', now=lambda: BACKED_UP_AT.replace(minute=41))
        self.assertTrue(result.made, result.reason)
        self.backup = result.path


class NothingIsTouchedUnless(ABackedUpTreeAndItsKit):
    """Deployment design sections 9 and 12: what a restore requires before the old tree is renamed."""

    def refused_untouched(self, *words, **options) -> None:
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.restore(**options), restore_tool.EXIT_REFUSED, self.text())
        for word in words:
            self.assertIn(word, self.text())
        self.assert_nothing_was_touched(before)

    def test_any_other_python_program_on_the_pc_refuses_and_is_named_whatever_tree_it_is_of(self):
        for name in ('python.exe', 'pythonw.exe', 'Python3.15.exe', 'py.exe'):
            with self.subTest(name=name):
                self.said.clear()
                self.refused_untouched('1 other Python program(s) are running on this PC', f'process 5000 ({name})',
                                       'no program of this project ends a process',
                                       table=QUIET_TABLE + [(5000, 4, name, 70)])

    def test_programs_that_are_not_python_do_not_count(self):
        table = QUIET_TABLE + [(5000, 4, 'pythonista.exe', 70), (5001, 4, 'notepad.exe', 71), (5002, 4, 'cmd.exe', 72)]
        self.assertEqual(self.restore(table=table), restore_tool.EXIT_RESTORED, self.text())

    def test_the_tools_own_python_and_the_pythons_above_it_are_left_out_and_no_other(self):
        launcher_pair = [(4, 0, 'System', 1), (800, 4, 'python.exe', 40), (ME, 800, 'python.exe', 60)]
        self.assertEqual(restore_tool.other_python_programs(launcher_pair, ME), [])
        reused_number = [(4, 0, 'System', 1), (800, 4, 'python.exe', 90), (ME, 800, 'python.exe', 60)]
        self.assertEqual([entry[0] for entry in restore_tool.other_python_programs(reused_number, ME)], [800])
        unreadable_start = [(800, 4, 'python.exe', None), (ME, 800, 'python.exe', 60)]
        self.assertEqual([entry[0] for entry in restore_tool.other_python_programs(unreadable_start, ME)], [800])

    def test_a_process_table_that_cannot_be_read_refuses(self):
        def unreadable():
            raise restore_tool.RestoreRefused('Windows would not give its process table (error 5).')

        self.refused_untouched('Windows would not give its process table', read_processes=unreadable)

    def test_where_windows_own_table_cannot_be_read_at_all_the_tool_refuses(self):
        if os.name == 'nt':
            self.skipTest('this is Windows: its own table is read in the joined rehearsal')
        before = tree_as_hashes(self.qa)
        code = restore_tool.restore(self.backup, kit_folder=self.kit, say=self.said.append, now=lambda: RESTORED_AT)
        self.assertEqual(code, restore_tool.EXIT_REFUSED)
        self.assertIn('this is not Windows', self.text())
        self.assert_nothing_was_touched(before)

    def test_a_backup_that_is_damaged_or_is_not_one_refuses(self):
        good = self.backup.read_bytes()
        cases = {'a byte changed inside': good[:200] + bytes([good[200] ^ 0xFF]) + good[201:],
                 'cut short': good[:len(good) // 2], 'not a ZIP': b'not a ZIP at all'}
        for what, data in cases.items():
            with self.subTest(what=what):
                self.said.clear()
                self.backup.write_bytes(data)
                self.refused_untouched()
                self.backup.write_bytes(good)
        partial = self.backup.with_name(self.backup.name + '.partial')
        shutil.copyfile(self.backup, partial)
        self.said.clear()
        self.backup = partial
        self.refused_untouched('A file ending ".partial" is never a backup')

    def test_a_backup_whose_members_are_not_what_its_manifest_lists_refuses(self):
        other = self.backup.with_name('QA_20261201_101010_MANUAL.zip')
        with zipfile.ZipFile(self.backup) as old, zipfile.ZipFile(other, 'w') as new:
            for name in old.namelist():
                new.writestr(name, old.read(name) + (b'x' if name == 'src/toy_other.py' else b''))
        self.backup = other
        self.refused_untouched('"src/toy_other.py" is not the file that was backed up')

    def test_a_backup_that_holds_a_member_its_manifest_does_not_list_refuses(self):
        other = self.backup.with_name('QA_20261201_101012_MANUAL.zip')
        with zipfile.ZipFile(self.backup) as old, zipfile.ZipFile(other, 'w') as new:
            new.writestr('src/slipped_in.py', b'# not on the list\r\n')
            for name in old.namelist():
                new.writestr(name, old.read(name))
        self.backup = other
        self.refused_untouched('it does not hold exactly the files its manifest lists')

    def copy_of_the_backup(self, name: str, change_manifest, leave_out=(), other_bytes=None) -> None:
        """Make a second, valid ZIP from the backup: every member's bytes as they are, the manifest changed by
        change_manifest(dict), the members named in leave_out dropped from the ZIP and from the manifest's list,
        and the members in other_bytes ({name: bytes}) given those bytes, with their hashes in the list to match."""
        other, other_bytes = self.backup.with_name(name), other_bytes or {}
        with zipfile.ZipFile(self.backup) as old, zipfile.ZipFile(other, 'w', compression=zipfile.ZIP_DEFLATED) as new:
            manifest = json.loads(old.read(restore_tool.SNAPSHOT_MANIFEST_NAME))
            manifest['files'] = [entry if entry['path'] not in other_bytes else
                                 {'path': entry['path'], 'sha256': hashlib.sha256(other_bytes[entry['path']]).hexdigest()}
                                 for entry in manifest['files'] if entry['path'] not in leave_out]
            change_manifest(manifest)
            for member in old.namelist()[:-1]:
                if member not in leave_out:
                    new.writestr(member, other_bytes.get(member, old.read(member)))
            new.writestr(restore_tool.SNAPSHOT_MANIFEST_NAME, json.dumps(manifest))
        self.backup = other

    def test_a_backup_whose_manifest_names_another_folder_than_its_own_settings_is_put_back_nowhere(self):
        elsewhere = self.root / 'another_invented_tree'
        elsewhere.mkdir()
        (elsewhere / 'precious.txt').write_bytes(b'not this backup\'s to rename\r\n')
        self.copy_of_the_backup('QA_20261201_101013_MANUAL.zip', lambda manifest: manifest.update(tree_root=str(elsewhere)))
        self.refused_untouched('A backup is put back only at the path its own settings name')
        self.assertEqual(sorted(entry.name for entry in self.root.iterdir() if 'another_invented_tree' in entry.name),
                         ['another_invented_tree'])          # not renamed, nothing set aside beside it
        self.assertEqual((elsewhere / 'precious.txt').read_bytes(), b'not this backup\'s to rename\r\n')

    def test_a_backup_whose_root_is_not_a_full_path_or_whose_role_is_not_its_settings_refuses(self):
        the_backup = self.backup
        for number, change in enumerate((lambda manifest: manifest.update(tree_root='a_p_r_i_r'),
                                         lambda manifest: manifest.update(tree_root=''),
                                         lambda manifest: manifest.update(role='PROD'))):
            with self.subTest(case=number):
                self.said.clear()
                self.backup = the_backup
                self.copy_of_the_backup(f'QA_20261201_10102{number}_MANUAL.zip', change)
                self.refused_untouched('A backup is put back only at the path its own settings name')

    def test_a_root_that_is_not_a_full_path_refuses_even_when_the_settings_inside_say_the_same(self):
        settings = ('[environment]\r\nrole = QA\r\ntree_root = a_p_r_i_r\r\nvenv_dir = a_p_r_i_r/.venv\r\n'
                    'backup_root = a_p_r_i_r_backups\r\n').encode('ascii')
        self.copy_of_the_backup('QA_20261201_101015_MANUAL.zip', lambda manifest: manifest.update(tree_root='a_p_r_i_r'),
                                other_bytes={'ENVIRONMENT.ini': settings})
        self.refused_untouched('A backup is put back only at the path its own settings name')
        self.assertFalse(Path('a_p_r_i_r').exists())

    def test_settings_inside_a_backup_that_do_not_describe_a_tree_of_the_project_refuse(self):
        for number, lines in enumerate((f'venv_dir = {self.qa.parent / "elsewhere" / ".venv"}\r\nbackup_root = {self.settings.backup_root}',
                                        f'venv_dir = {self.qa / ".venv"}\r\nbackup_root = {self.qa / "backups"}')):
            with self.subTest(case=number):
                self.said.clear()
                the_backup = self.backup
                settings = f'[environment]\r\nrole = QA\r\ntree_root = {self.qa}\r\n{lines}\r\n'.encode('utf-8')
                self.copy_of_the_backup(f'QA_20261201_10103{number}_MANUAL.zip', lambda manifest: None,
                                        other_bytes={'ENVIRONMENT.ini': settings})
                self.refused_untouched('does not describe a tree of this project')
                self.backup = the_backup

    def test_a_backup_that_holds_no_settings_file_is_not_a_trees_backup(self):
        self.copy_of_the_backup('QA_20261201_101014_MANUAL.zip', lambda manifest: None, leave_out=('ENVIRONMENT.ini',))
        self.refused_untouched('it holds no ENVIRONMENT.ini')

    def test_a_process_table_that_was_not_read_whole_refuses(self):
        without_this_tool = [entry for entry in QUIET_TABLE if entry[0] != ME]
        for table in (without_this_tool, []):
            with self.subTest(entries=len(table)):
                self.said.clear()
                self.refused_untouched('does not hold this tool\'s own process: it was not read whole', table=table)
        restore_tool.check_table_was_read_to_its_end(restore_tool.ERROR_NO_MORE_FILES)
        for error in (0, 5, 299):                            # no error reported; access denied; a partial copy
            with self.assertRaisesRegex(restore_tool.RestoreRefused, 'could not be read to its end'):
                restore_tool.check_table_was_read_to_its_end(error)

    def test_a_member_whose_name_would_leave_the_tree_refuses(self):
        other = self.backup.with_name('QA_20261201_101011_MANUAL.zip')
        manifest = {'kind': restore_tool.SNAPSHOT_MANIFEST_KIND, 'tree_root': str(self.qa), 'empty_folders': [],
                    'role': 'QA', 'files': [{'path': '../outside.txt', 'sha256': hashlib.sha256(b'x').hexdigest()}]}
        with zipfile.ZipFile(other, 'w') as new:
            new.writestr('../outside.txt', b'x')
            new.writestr(restore_tool.SNAPSHOT_MANIFEST_NAME, json.dumps(manifest))
        self.backup = other
        self.refused_untouched('is not a path inside a tree')
        self.assertFalse((self.qa.parent / 'outside.txt').exists())


class StoppedPartWay(ABackedUpTreeAndItsKit):
    """Deployment design section 12: stopped half-way, the same command again; and section 9: the second check."""

    def test_a_python_program_that_appears_after_the_rename_stops_it_and_the_same_command_again_finishes(self):
        tables = iter([QUIET_TABLE, QUIET_TABLE + [(5000, 4, 'python.exe', 70)]])
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.restore(read_processes=lambda: next(tables)), restore_tool.EXIT_STOPPED, self.text())
        self.assertIn('after the old tree was renamed', self.text())
        self.assertIn('STOPPED PART-WAY', self.said[-1])
        [aside] = self.set_aside()
        was = tree_as_hashes(aside)
        was['ENVIRONMENT.ini'] = was.pop('ENVIRONMENT.ini.SET_ASIDE')
        self.assertEqual(was, before)
        self.assertFalse(self.qa.exists())
        self.assertEqual(restore_tool.restore(self.backup, kit_folder=self.kit, read_processes=lambda: QUIET_TABLE,
                                              environment=lambda tree: True, say=self.said.append,
                                              now=lambda: RESTORED_AT.replace(minute=6)), restore_tool.EXIT_RESTORED)
        self.assertTrue(self.payload.items() <= tree_as_hashes(self.qa).items())

    def test_a_fresh_tree_that_is_not_the_payload_stays_marked_unfinished_and_is_set_aside_by_the_next_attempt(self):
        read_back = restore_tool._tree_now

        def one_file_lost(tree_root):
            files, empty = read_back(tree_root)
            del files['src/toy_other.py']
            return files, empty

        with mock.patch.object(restore_tool, '_tree_now', one_file_lost):
            self.assertEqual(self.restore(), restore_tool.EXIT_STOPPED, self.text())
        self.assertIn('is not exactly what the backup holds', self.text())
        self.assertTrue((self.qa / restore_tool.PROGRESS_FILE).is_file())
        self.assertFalse((self.qa / 'ENVIRONMENT.ini').exists())                 # so no launcher runs in it
        with self.assertRaises(launch_guard.GuardRefused):
            launch_guard.check_no_unfinished_operation(self.qa)
        self.said.clear()
        self.assertEqual(restore_tool.restore(self.backup, kit_folder=self.kit, read_processes=lambda: QUIET_TABLE,
                                              environment=lambda tree: True, say=self.said.append,
                                              now=lambda: RESTORED_AT.replace(minute=6)), restore_tool.EXIT_RESTORED)
        self.assertIn('an unfinished restore', self.text())
        self.assertEqual(len(self.set_aside()), 2)
        self.assertFalse((self.qa / restore_tool.PROGRESS_FILE).exists())

    def test_a_fresh_tree_with_a_folder_the_backup_does_not_hold_or_without_one_it_holds_is_not_the_payload(self):
        read_back = restore_tool._tree_now
        for what, change in (('one more', lambda folders: folders | {'src/slipped_in'}),
                             ('one fewer', lambda folders: folders - {'src/methods'})):
            with self.subTest(what=what):
                self.said.clear()

                def folders_differ(tree_root):
                    files, folders = read_back(tree_root)
                    return files, change(folders)

                with mock.patch.object(restore_tool, '_tree_now', folders_differ):
                    self.assertEqual(self.restore(now=lambda: RESTORED_AT.replace(second=len(what))),
                                     restore_tool.EXIT_STOPPED, self.text())
                self.assertIn('its folders are not the backup\'s', self.text())
                self.assertTrue((self.qa / restore_tool.PROGRESS_FILE).is_file())

    def test_a_folder_that_cannot_be_listed_stops_the_restore_and_is_never_read_as_absent(self):
        listing = os.scandir

        def scandir(path='.'):
            if os.fspath(path) == str(self.qa / 'src' / 'methods'):
                raise PermissionError(13, 'Access is denied', os.fspath(path))
            return listing(path)

        real_tree_now = restore_tool._tree_now

        def read_with_one_folder_closed(tree_root):
            with mock.patch('os.scandir', scandir):
                return real_tree_now(tree_root)

        with mock.patch.object(restore_tool, '_tree_now', read_with_one_folder_closed):
            self.assertEqual(self.restore(), restore_tool.EXIT_STOPPED, self.text())
        self.assertIn('STOPPED: a file or a folder could not be read', self.text())
        self.assertTrue((self.qa / restore_tool.PROGRESS_FILE).is_file())


class AStaleOrphanMarker(ABackedUpTreeAndItsKit):
    """Deployment design section 12, the one exception: shown with its warning; the PC started after the marker
    was written; a fresh process check clean; the fixed sentence typed. No part can be waived."""

    def setUp(self):
        super().setUp()
        (self.qa / ORPHAN).parent.mkdir(parents=True)
        (self.qa / ORPHAN).write_bytes(b'[{"an": "invented orphan entry"}]\r\n')
        result = snapshot.attempt_snapshot(self.settings, 'MANUAL', now=lambda: BACKED_UP_AT.replace(minute=45))
        self.assertTrue(result.made, result.reason)
        self.backup = result.path
        self.marker_written = (self.qa / ORPHAN).stat().st_mtime

    def with_marker(self, typed: str, started_after: float, table=QUIET_TABLE) -> int:
        tables = iter([QUIET_TABLE, table, QUIET_TABLE, QUIET_TABLE])
        return self.restore(read_processes=lambda: next(tables), ask=lambda question: typed,
                            started_at=lambda: self.marker_written + started_after)

    def test_with_all_four_parts_the_marker_is_kept_as_evidence_and_is_not_live(self):
        self.assertEqual(self.with_marker(restore_tool.ORPHAN_ACKNOWLEDGEMENT, 3600), restore_tool.EXIT_RESTORED,
                         self.text())
        self.assertIn('WARNING: AN ORPHAN MARKER WAS FOUND', self.text())
        self.assertIn('RESTART THE PC', self.text())
        self.assertFalse((self.qa / ORPHAN).exists())
        [evidence] = sorted((self.qa / 'records').glob('RESTORE_*_ORPHAN_MARKER.json'))
        self.assertEqual(evidence.read_bytes(), b'[{"an": "invented orphan entry"}]\r\n')
        [aside] = self.set_aside()
        self.assertTrue((aside / ORPHAN).is_file())
        self.assertEqual(self.orphan_record(), {
            'in_the_backup': True, 'in_the_old_tree': True, 'old_tree_marker_now_at': str(aside / ORPHAN),
            'old_tree_marker_note': None, 'evidence_is_the_marker_of': 'the backup',
            'evidence_file': f'records/{evidence.name}'})
        self.assertIn('are kept as evidence in', self.text())

    def orphan_record(self) -> dict:
        """What the restore record says of orphan markers."""
        [record] = [path for path in (self.qa / 'records').glob('RESTORE_*.json') if 'ORPHAN' not in path.name]
        return json.loads(record.read_bytes())['orphan_marker']

    def test_without_a_restart_since_the_marker_it_refuses_and_typing_the_sentence_does_not_stand_in(self):
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.with_marker(restore_tool.ORPHAN_ACKNOWLEDGEMENT, -60), restore_tool.EXIT_REFUSED)
        self.assertIn('has not been restarted since the orphan marker was written', self.text())
        self.assertIn('the existing reviewed clearance', self.text())
        self.assert_nothing_was_touched(before)

    def test_a_python_program_at_the_fresh_check_refuses_whatever_is_typed(self):
        before = tree_as_hashes(self.qa)
        code = self.with_marker(restore_tool.ORPHAN_ACKNOWLEDGEMENT, 3600, QUIET_TABLE + [(5000, 4, 'python.exe', 70)])
        self.assertEqual(code, restore_tool.EXIT_REFUSED)
        self.assertIn('the fresh check that the orphan marker asks for', self.text())
        self.assert_nothing_was_touched(before)

    def test_anything_but_the_fixed_sentence_refuses(self):
        for typed in ('', 'YES', restore_tool.ORPHAN_ACKNOWLEDGEMENT.lower()):
            with self.subTest(typed=typed):
                self.said.clear()
                before = tree_as_hashes(self.qa)
                self.assertEqual(self.with_marker(typed, 3600), restore_tool.EXIT_REFUSED)
                self.assert_nothing_was_touched(before)

    def test_a_marker_only_in_the_old_tree_asks_the_same(self):
        self.backup = sorted(self.settings.backup_root.glob('QA_*_MANUAL.zip'))[0]    # made before the marker was
        with zipfile.ZipFile(self.backup) as archive:
            self.assertNotIn(ORPHAN, archive.namelist())
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.with_marker('YES', 3600), restore_tool.EXIT_REFUSED)
        self.assertIn(str(self.qa / ORPHAN), self.text())
        self.assert_nothing_was_touched(before)
        self.said.clear()
        self.assertEqual(self.with_marker(restore_tool.ORPHAN_ACKNOWLEDGEMENT, 3600), restore_tool.EXIT_RESTORED,
                         self.text())
        self.assertFalse((self.qa / ORPHAN).exists())
        [evidence] = sorted((self.qa / 'records').glob('RESTORE_*_ORPHAN_MARKER.json'))     # read before the rename
        self.assertEqual(evidence.read_bytes(), b'[{"an": "invented orphan entry"}]\r\n')
        [aside] = self.set_aside()
        self.assertEqual((aside / ORPHAN).read_bytes(), b'[{"an": "invented orphan entry"}]\r\n')
        self.assertEqual(self.orphan_record(), {
            'in_the_backup': False, 'in_the_old_tree': True, 'old_tree_marker_now_at': str(aside / ORPHAN),
            'old_tree_marker_note': None, 'evidence_is_the_marker_of': 'the old tree',
            'evidence_file': f'records/{evidence.name}'})

    def test_an_old_tree_marker_that_cannot_be_read_is_not_said_to_be_kept(self):
        self.backup = sorted(self.settings.backup_root.glob('QA_*_MANUAL.zip'))[0]
        (self.qa / ORPHAN).unlink()
        (self.qa / ORPHAN).mkdir()                           # it is there and its bytes cannot be read
        self.assertEqual(self.with_marker(restore_tool.ORPHAN_ACKNOWLEDGEMENT, 3600), restore_tool.EXIT_RESTORED,
                         self.text())
        self.assertEqual(sorted((self.qa / 'records').glob('RESTORE_*_ORPHAN_MARKER.json')), [])
        record = self.orphan_record()
        self.assertEqual((record['evidence_file'], record['evidence_is_the_marker_of']), (None, None))
        self.assertIn('could not be read', record['old_tree_marker_note'])
        self.assertIn('ARE NOT KEPT BESIDE THE RECORD', self.text())

    def test_a_restart_within_the_two_seconds_a_zip_cannot_tell_apart_is_not_proof_of_a_later_restart(self):
        (self.qa / ORPHAN).unlink()                          # the marker is only in the backup: its time is the ZIP's
        kept = restore_tool.read_backup(self.backup)['orphan_marker_time']
        for after, expected in ((0, restore_tool.EXIT_REFUSED), (restore_tool.ZIP_TIME_STEP, restore_tool.EXIT_REFUSED),
                                (restore_tool.ZIP_TIME_STEP + 1, restore_tool.EXIT_RESTORED)):
            with self.subTest(seconds_after_the_zips_time=after):
                self.said.clear()
                tables = iter([QUIET_TABLE] * 4)
                code = self.restore(read_processes=lambda: next(tables), started_at=lambda: kept + after,
                                    ask=lambda question: restore_tool.ORPHAN_ACKNOWLEDGEMENT)
                self.assertEqual(code, expected, self.text())

    def test_a_marker_only_in_the_backup_asks_the_same(self):
        (self.qa / ORPHAN).unlink()
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.with_marker('YES', 3600), restore_tool.EXIT_REFUSED)
        self.assertIn(f'{ORPHAN} inside the backup', self.text())
        self.assert_nothing_was_touched(before)


class AfterAnUnzipByHand(ABackedUpTreeAndItsKit):
    def make_backup(self) -> None:
        (self.qa / 'scratch' / 'empty').mkdir(parents=True, exist_ok=True)       # so that the backup holds one
        super().make_backup()

    """Deployment design section 12, the last resort: nothing was checked by the unzip; the reconciliation checks
    every file, writes the record and moves the manifest; until then no new backup is made."""

    def setUp(self):
        super().setUp()
        shutil.rmtree(self.qa)
        with zipfile.ZipFile(self.backup) as archive:
            archive.extractall(self.qa)

    def reconcile(self) -> int:
        return restore_tool.reconcile_after_hand_unzip(self.backup, kit_folder=self.kit, say=self.said.append,
                                                       read_processes=lambda: QUIET_TABLE, now=lambda: RESTORED_AT)

    def test_no_new_backup_is_made_while_the_manifest_lies_at_the_trees_root(self):
        result = snapshot.attempt_snapshot(self.settings, 'MANUAL', now=lambda: RESTORED_AT)
        self.assertFalse(result.made)
        self.assertIn('Restore.bat --after-hand-unzip', result.reason)

    def test_it_checks_every_file_writes_the_record_and_moves_the_manifest_beside_it(self):
        self.assertEqual(self.reconcile(), restore_tool.EXIT_RESTORED, self.text())
        stamp = RESTORED_AT.astimezone().strftime('%Y%m%d_%H%M%S')
        record = json.loads((self.qa / 'records' / f'RESTORE_{stamp}.json').read_bytes())
        self.assertEqual(record['reconciliation_recorded_at'], stamp)
        self.assertNotIn('restored_at', record)
        self.assertTrue(record['unzipped_by_hand'])
        self.assertFalse((self.qa / snapshot.MANIFEST_NAME).exists())
        self.assertTrue((self.qa / 'records' / f'RESTORE_{stamp}_{snapshot.MANIFEST_NAME}').is_file())
        self.assertTrue(snapshot.attempt_snapshot(self.settings, 'MANUAL', now=lambda: RESTORED_AT).made)

    def test_a_missing_empty_folder_or_another_manifest_at_the_root_is_not_this_backup_unzipped(self):
        empty = [path for path in self.qa.rglob('*') if path.is_dir() and not any(path.iterdir())]
        self.assertTrue(empty, 'the invented tree holds no empty folder to lose')
        empty[0].rmdir()
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.reconcile(), restore_tool.EXIT_REFUSED)
        self.assertIn('its folders are not the backup\'s', self.text())
        self.assertEqual(tree_as_hashes(self.qa), before)
        empty[0].mkdir()
        self.said.clear()
        manifest_at_root = self.qa / snapshot.MANIFEST_NAME
        kept = manifest_at_root.read_bytes()
        manifest_at_root.write_bytes(kept.replace(b'"job": "MANUAL"', b'"job": "RESEARCH"'))
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.reconcile(), restore_tool.EXIT_REFUSED)
        self.assertIn('at its root is missing or is not this backup\'s', self.text())
        self.assertEqual(tree_as_hashes(self.qa), before)
        manifest_at_root.write_bytes(kept)
        self.said.clear()
        self.assertEqual(self.reconcile(), restore_tool.EXIT_RESTORED, self.text())

    def test_a_tree_that_is_not_the_backup_unzipped_is_refused_and_nothing_is_changed(self):
        with open(self.qa / 'src' / 'toy_other.py', 'ab') as handle:
            handle.write(b'# not the backup\'s\r\n')
        before = tree_as_hashes(self.qa)
        self.assertEqual(self.reconcile(), restore_tool.EXIT_REFUSED)
        self.assertIn('is not exactly this backup unzipped', self.text())
        self.assertEqual(tree_as_hashes(self.qa), before)


if __name__ == '__main__':
    unittest.main()
