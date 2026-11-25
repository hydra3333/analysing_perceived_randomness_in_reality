"""Tests of a tree's backup: the verified ZIP, the note that a backup is owed, and the research job's two backups.

What this file is for
    It proves, on invented trees, what the deployment design's section 10 and the specification's section 14.1
    say of a backup: everything under the tree but two control files; checked twice; quiet throughout; given its
    name only when verified; always an attempt whose result is said as it is, never a stop of the work.

Which of the project's own modules it uses
    research.snapshot, research.research_job, research.job_lock, research.process_rule; tests/research_fixtures.py.
"""
import hashlib
import json
import os
import unittest
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import research_fixtures as fx
from research import job_lock, process_rule, research_job, snapshot, status_file
from research.settings import read_settings

A_TIME = datetime(2026, 12, 1, 9, 40, 12, tzinfo=timezone.utc)


def everything_under(folder: Path) -> tuple:
    """Every file under a folder with its bytes, and every empty folder: ({path: bytes}, [paths])."""
    files = {path.relative_to(folder).as_posix(): path.read_bytes() for path in sorted(folder.rglob('*'))
             if path.is_file()}
    empty = sorted(path.relative_to(folder).as_posix() for path in folder.rglob('*')
                   if path.is_dir() and not any(path.iterdir()))
    return files, empty


class InventedQaTree(fx.JobCase):
    """An invented QA tree as the project's commands leave one, with its backup root beside it."""

    def setUp(self):
        super().setUp()
        self.qa = self.tree(with_source=False)
        self.settings = read_settings(self.qa)
        self.backups = self.settings.backup_root

    def attempt(self, job: str = 'MANUAL', when: datetime = A_TIME) -> snapshot.SnapshotResult:
        """One attempt at a backup of the tree at a fixed time."""
        return snapshot.attempt_snapshot(self.settings, job, now=lambda: when)

    def assert_nothing_was_left(self) -> None:
        """No ZIP, no ".partial" and no lock: an attempt that failed left no trace but its result."""
        self.assertEqual([entry.name for entry in self.backups.iterdir()] if self.backups.is_dir() else [], [])
        self.assertFalse((self.qa / snapshot.LOCK_PATH).exists())


class AVerifiedBackup(InventedQaTree):
    """Deployment design section 10: what a backup holds, how it is named, and what is written when it passes."""

    def test_it_is_named_for_the_role_the_time_and_the_work_and_says_what_it_made(self):
        result = self.attempt('PRE_INSTALL')
        self.assertTrue(result.made, result.reason)
        stamp = A_TIME.astimezone().strftime('%Y%m%d_%H%M%S')
        self.assertEqual(result.path, self.backups / f'QA_{stamp}_PRE_INSTALL.zip')
        self.assertRegex(result.line(), r'^BACKUP MADE AND VERIFIED: .*QA_\d{8}_\d{6}_PRE_INSTALL\.zip \(\d+ files; ')
        self.assertEqual(sorted(entry.name for entry in self.backups.iterdir()),
                         [result.path.name, result.path.name + '.sha256'])

    def test_unpacked_it_is_the_tree_byte_for_byte_but_for_the_two_control_files(self):
        (self.qa / 'scratch' / 'an empty folder').mkdir(parents=True)
        (self.qa / 'records' / 'a name with spaces.txt').write_bytes(b'kept\r\n')
        snapshot.mark_due(self.settings)
        before = everything_under(self.qa)
        result = self.attempt()
        self.assertTrue(result.made, result.reason)
        unpacked = self.root / 'unpacked'
        with zipfile.ZipFile(result.path) as archive:
            self.assertEqual(archive.namelist()[-1], snapshot.MANIFEST_NAME)
            archive.extractall(unpacked)
        (unpacked / snapshot.MANIFEST_NAME).unlink()
        files, empty = everything_under(unpacked)
        expected = {path: data for path, data in before[0].items() if path != snapshot.DUE_PATH}
        self.assertEqual(files, expected)
        self.assertEqual(empty, before[1])
        self.assertIn('.venv/pyvenv.cfg', files)
        self.assertIn('ENVIRONMENT.ini', files)
        self.assertNotIn(snapshot.LOCK_PATH, files)

    def test_its_manifest_lists_every_file_with_its_hash_and_says_whose_tree_it_was(self):
        result = self.attempt()
        with zipfile.ZipFile(result.path) as archive:
            raw = archive.read(snapshot.MANIFEST_NAME)
        self.assertEqual(raw.count(b'\n'), raw.count(b'\r\n'))
        manifest = json.loads(raw)
        self.assertEqual((manifest['kind'], manifest['role'], manifest['tree_root'], manifest['job']),
                         (snapshot.MANIFEST_KIND, 'QA', str(self.qa), 'MANUAL'))
        self.assertEqual(manifest['made_utc'], '2026-12-01T09:40:12Z')
        self.assertEqual(manifest['software_fingerprint'],
                         hashlib.sha256((self.qa / 'records' / 'INSTALLED_FILES.json').read_bytes()).hexdigest())
        self.assertIsNone(manifest['recovery_kit'])
        listed = {entry['path']: entry['sha256'] for entry in manifest['files']}
        self.assertEqual(listed, {path: hashlib.sha256(data).hexdigest()
                                  for path, data in everything_under(self.qa)[0].items()
                                  if path != snapshot.LOG_PATH})          # the log's line is written afterwards

    def test_the_sha256_file_the_log_line_and_the_removal_of_the_note_follow_a_verified_backup(self):
        snapshot.mark_due(self.settings)
        self.assertTrue(snapshot.is_due(self.qa))
        result = self.attempt()
        digest = hashlib.sha256(result.path.read_bytes()).hexdigest()
        self.assertEqual(Path(str(result.path) + '.sha256').read_bytes(),
                         f'{digest} *{result.path.name}\r\n'.encode('ascii'))
        lines = (self.qa / snapshot.LOG_PATH).read_bytes()
        self.assertNotIn(b'\r', lines)
        record = json.loads(lines)
        self.assertEqual((record['backup'], record['sha256'], record['job']), (result.path.name, digest, 'MANUAL'))
        self.assertFalse(snapshot.is_due(self.qa))
        self.assertFalse((self.qa / snapshot.LOCK_PATH).exists())

    def invented_kit(self, name: str, fingerprint: str, sidecar: str = 'right') -> None:
        """Write an invented recovery kit into the backup root: a ZIP whose manifest names a software fingerprint,
        with its ".sha256" beside it ('right'), with one that does not agree ('wrong'), or with none ('none')."""
        self.backups.mkdir(exist_ok=True)
        with zipfile.ZipFile(self.backups / name, 'w') as kit:
            kit.writestr('KIT_MANIFEST.json', json.dumps({'software_fingerprint': fingerprint}))
        digest = hashlib.sha256((self.backups / name).read_bytes()).hexdigest()
        if sidecar != 'none':
            (self.backups / (name + '.sha256')).write_bytes(
                f'{digest if sidecar == "right" else "0" * 64} *{name}\r\n'.encode('ascii'))

    def kit_named_by_a_backup(self):
        with zipfile.ZipFile(self.attempt().path) as archive:
            return json.loads(archive.read(snapshot.MANIFEST_NAME))['recovery_kit']

    def test_it_names_the_newest_finished_recovery_kit_of_the_trees_software_state(self):
        fingerprint = snapshot.software_fingerprint(self.qa)
        short = fingerprint[:12]
        self.invented_kit(f'KIT_20261101_080000_{short}.zip', fingerprint)
        self.invented_kit(f'KIT_20261120_080000_{short}.zip', fingerprint)
        self.invented_kit(f'KIT_20261121_080000_{short}.zip', fingerprint, sidecar='none')      # never finished
        self.invented_kit(f'KIT_20261122_080000_{short}.zip', fingerprint, sidecar='wrong')     # damaged since
        self.invented_kit(f'KIT_20261123_080000_{short}.zip', short + 'f' * 52)     # another state, same 12 letters
        (self.backups / f'KIT_20261124_080000_{short}.zip').write_bytes(b'PK not a kit at all')
        (self.backups / f'KIT_20261124_080000_{short}.zip.sha256').write_bytes(
            hashlib.sha256(b'PK not a kit at all').hexdigest().encode('ascii') + b' *x\r\n')
        self.invented_kit('KIT_20261125_080000_000000000000.zip', '0' * 64)
        self.assertEqual(self.kit_named_by_a_backup(), f'KIT_20261120_080000_{short}.zip')

    def test_with_no_finished_kit_of_its_state_a_backup_is_made_all_the_same_and_names_none(self):
        fingerprint = snapshot.software_fingerprint(self.qa)
        self.invented_kit(f'KIT_20261121_080000_{fingerprint[:12]}.zip', fingerprint, sidecar='none')
        self.assertIsNone(self.kit_named_by_a_backup())

    def test_the_command_says_how_often_the_tree_is_read(self):
        said = []
        snapshot.main([], self.qa, say=said.append)
        self.assertIn('Every file is read three times (hashed, written into the ZIP, hashed again) and the ZIP is '
                      'read back', said[0])


class ABackupIsOnlyOfAQuietTree(InventedQaTree):
    """Deployment design sections 9 and 10: the lock, the process rule before and after, and the second reading.
    Every failure is a result, and leaves no ZIP that could be taken for a backup."""

    def not_made(self, *words) -> str:
        """Attempt a backup, expect none, and return the reason; the note that one is owed is left as it was."""
        due = snapshot.is_due(self.qa)
        result = self.attempt()
        self.assertFalse(result.made)
        for word in words:
            self.assertIn(word, result.reason)
        self.assertTrue(result.line().startswith('BACKUP NOT MADE: '))
        self.assertEqual(snapshot.is_due(self.qa), due)
        return result.reason

    def test_dev_has_no_backup_root_and_nothing_is_written(self):
        dev = self.tree(role='DEV', with_source=False, name='dev')
        before = everything_under(dev)
        result = snapshot.attempt_snapshot(read_settings(dev), 'MANUAL')
        self.assertFalse(result.made)
        self.assertIn('DEV has no backup root', result.reason)
        self.assertEqual(everything_under(dev), before)

    def test_a_job_or_a_results_update_holding_its_lock_means_no_backup(self):
        for lock, word in ((job_lock.job_lock, 'a job of this tree holds its lock'),
                           (job_lock.updater_lock, 'a results update holds its lock')):
            with self.subTest(word=word):
                with lock(self.qa, 'a test', 'now'):
                    self.not_made(word)
                self.assert_nothing_was_left()

    def test_a_backup_already_in_progress_means_no_second_one_and_its_lock_is_left_alone(self):
        (self.qa / snapshot.LOCK_PATH).write_bytes(b'backup of another process\r\n')
        self.not_made('SNAPSHOT_IN_PROGRESS.lock exists')
        self.assertEqual((self.qa / snapshot.LOCK_PATH).read_bytes(), b'backup of another process\r\n')

    def test_another_python_of_the_tree_before_the_first_reading_or_after_the_second_means_no_backup(self):
        for calls_that_pass in (0, 1):
            with self.subTest(calls_that_pass=calls_that_pass):
                seen = []

                def rule(tree_root):
                    seen.append(tree_root)
                    if len(seen) > calls_that_pass:
                        raise process_rule.ProcessRuleRefused('1 other Python process(es) of the tree are running')
                    return 1

                with mock.patch.object(process_rule, 'check_no_other_process_of_tree', rule):
                    self.not_made('other Python process(es) of the tree')
                self.assertEqual(len(seen), calls_that_pass + 1)
                self.assert_nothing_was_left()

    def test_the_process_rule_is_asked_twice_of_this_tree_for_a_backup_that_is_made(self):
        with mock.patch.object(process_rule, 'check_no_other_process_of_tree', return_value=1) as rule:
            self.assertTrue(self.attempt().made)
        self.assertEqual([call.args for call in rule.call_args_list], [(self.qa,), (self.qa,)])

    def test_a_file_changed_added_or_removed_while_the_backup_is_made_means_no_backup(self):
        changes = {'changed': lambda: (self.qa / 'ENVIRONMENT.ini').write_bytes(
                       (self.qa / 'ENVIRONMENT.ini').read_bytes() + b'\r\n'),
                   'added': lambda: (self.qa / 'records' / 'new.txt').write_bytes(b'new\r\n'),
                   'removed': lambda: (self.qa / 'src' / 'toy_other.py').unlink()}
        check = snapshot._check_archive
        for what, change in changes.items():
            with self.subTest(what=what):
                kept = everything_under(self.qa)

                def check_then_change(*arguments):
                    check(*arguments)                    # the archive is good; then the tree moves
                    change()

                with mock.patch.object(snapshot, '_check_archive', check_then_change):
                    self.not_made('the tree changed while it was being backed up', 'only of a quiet tree')
                self.assert_nothing_was_left()
                for path, data in kept[0].items():       # put the invented tree back for the next case
                    (self.qa / path).write_bytes(data)
                for path in set(everything_under(self.qa)[0]) - set(kept[0]):
                    (self.qa / path).unlink()

    def test_an_archive_that_does_not_read_back_as_it_was_written_means_no_backup(self):
        write = snapshot._write_archive

        def write_then_misremember(*arguments):
            hashes, manifest_bytes = write(*arguments)
            hashes['ENVIRONMENT.ini'] = '0' * 64
            return hashes, manifest_bytes

        with mock.patch.object(snapshot, '_write_archive', write_then_misremember):
            self.not_made('ENVIRONMENT.ini read back from the archive is not the file that was read')
        self.assert_nothing_was_left()

    def rewritten(self, partial: Path, change) -> None:
        """Write a ZIP again member by member, as a valid ZIP, with change(name, data) giving each member's bytes."""
        with zipfile.ZipFile(partial) as old:
            members = [(name, old.read(name)) for name in old.namelist()]
        partial.unlink()
        with zipfile.ZipFile(partial, 'x', compression=zipfile.ZIP_DEFLATED) as new:
            for name, data in members:
                new.writestr(name, change(name, data))

    def test_a_manifest_that_reads_back_as_other_bytes_means_no_backup_though_every_file_is_right(self):
        (self.qa / 'scratch' / 'empty').mkdir(parents=True)
        write = snapshot._write_archive
        other_root = lambda name, data: (data.replace(str(self.qa).encode(), str(self.qa.parent / 'elsewhere').encode())
                                         if name == snapshot.MANIFEST_NAME else data)
        other_hash = lambda name, data: (data.replace(b'"sha256": "', b'"sha256": "0', 1)
                                         if name == snapshot.MANIFEST_NAME else data)
        folder_not_empty = lambda name, data: b'x' if name == 'scratch/empty/' else data
        for what, change, word in (('another tree root', other_root, 'the manifest read back'),
                                   ('another hash', other_hash, 'the manifest read back'),
                                   ('an empty folder that is not empty', folder_not_empty, 'scratch/empty read back')):
            with self.subTest(what=what):
                snapshot.mark_due(self.settings)

                def write_then_alter(tree_root, partial, *rest):
                    result = write(tree_root, partial, *rest)
                    self.rewritten(partial, change)          # a valid ZIP; every file's bytes as they were read
                    return result

                with mock.patch.object(snapshot, '_write_archive', write_then_alter):
                    self.not_made(word)
                self.assert_nothing_was_left()
                self.assertTrue(snapshot.is_due(self.qa))

    def test_an_archive_that_does_not_decompress_is_a_backup_not_made_and_never_an_exception(self):
        import zlib
        for error in (zlib.error('Error -3 while decompressing data'), EOFError('compressed file ended early'),
                      zipfile.BadZipFile('Bad CRC-32')):
            with self.subTest(error=type(error).__name__):
                with mock.patch.object(snapshot, '_check_archive', side_effect=error):
                    self.not_made()
                self.assert_nothing_was_left()

    def test_a_partial_that_lay_there_before_the_attempt_is_another_attempts_and_is_not_removed(self):
        stamp = A_TIME.astimezone().strftime('%Y%m%d_%H%M%S')
        self.backups.mkdir(exist_ok=True)
        earlier = self.backups / f'QA_{stamp}_MANUAL.zip.partial'
        earlier.write_bytes(b'left by a backup that was ended')
        self.not_made('exists already', 'Nothing was removed')
        self.assertEqual(earlier.read_bytes(), b'left by a backup that was ended')
        self.assertEqual([entry.name for entry in self.backups.iterdir()], [earlier.name])

    def test_a_link_in_the_tree_means_no_backup_and_what_it_points_to_is_not_read(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'private.txt').write_bytes(b'not the tree\'s\r\n')
        os.symlink(outside, self.qa / 'records' / 'a_link', target_is_directory=True)
        self.not_made('records/a_link is a link or a junction')
        self.assert_nothing_was_left()

    def test_a_backup_root_that_cannot_be_written_means_no_backup_and_no_exception(self):
        if self.backups.exists():
            self.backups.rmdir()
        self.backups.write_bytes(b'a file where the backup root should be')
        self.not_made()
        self.assertFalse((self.qa / snapshot.LOCK_PATH).exists())

    def test_a_backup_of_the_same_name_is_never_written_over(self):
        first = self.attempt()
        kept = first.path.read_bytes()
        self.not_made('exists already')
        self.assertEqual(first.path.read_bytes(), kept)


class TheResearchJobsBackups(InventedQaTree):
    """Specification 14.1: a backup at the end of every research job; the note that one is owed, written before
    the job's first write; if a backup cannot be made the work goes on, with a standing warning."""

    def job(self, tree: Path, clock=None) -> tuple:
        """Run the research job; return (exit code, what it said as one text). clock: gives the time; the fixed
        time of the fixtures if none is given."""
        said = []
        with fx.ImportPath(tree):
            code = research_job.run(tree, (fx.GAME,), now=clock or (lambda: fx.FIXED_TIME), say=said.append,
                                    no_update=True)
        return code, '\n'.join(said)

    @staticmethod
    def a_clock_that_runs():
        """A clock that is a minute later each time it is read, as a real job's is later at its end than at its
        start: a job that makes a backup at its start and another at its end gives them two names."""
        read = iter(range(10 ** 6))
        return lambda: fx.FIXED_TIME + timedelta(minutes=next(read))

    def test_a_job_ends_with_a_verified_backup_that_holds_what_the_job_wrote_and_no_lock(self):
        code, text = self.job(self.qa)
        self.assertEqual(code, 0, text)
        self.assertIn('BACKUP MADE AND VERIFIED: ', text)
        self.assertNotIn('WARNING', text)
        self.assertNotIn('A backup is owed from earlier work', text)
        self.assertFalse(snapshot.is_due(self.qa))
        [archive_path] = [entry for entry in self.backups.iterdir() if entry.name.endswith('_RESEARCH.zip')]
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
        self.assertTrue(any(name.startswith('results/research/') and name.endswith('forecasts.jsonl') for name in names))
        self.assertNotIn('records/JOB.lock', names)
        self.assertNotIn(snapshot.DUE_PATH, names)
        self.assertNotIn(snapshot.LOCK_PATH, names)

    def staged_leftover(self) -> Path:
        """What an interrupted status write leaves: an unfinished copy in the staging folder."""
        leftover = self.qa / status_file.STAGING_FOLDER / f'E_901__TOY_B_V1__{status_file.STATUS_FILE_NAME}.writing'
        leftover.parent.mkdir(parents=True, exist_ok=True)
        leftover.write_bytes(b'left by an interrupted status write\r\n')
        return leftover

    def test_the_note_is_the_jobs_first_write_before_it_tidies_or_writes_anything_else(self):
        leftover, seen = self.staged_leftover(), []
        tidy = research_job.discard_unfinished_writes

        def look_then_tidy(tree_root):
            seen.append((snapshot.is_due(tree_root), leftover.exists(), (tree_root / 'results' / 'research').exists()))
            return tidy(tree_root)

        with mock.patch.object(research_job, 'discard_unfinished_writes', look_then_tidy):
            self.assertEqual(self.job(self.qa)[0], 0)
        self.assertEqual(seen, [(True, True, False)])
        self.assertFalse(leftover.exists())

    def test_an_ordinary_refusal_after_the_guard_comes_before_any_write_and_says_so_truthfully(self):
        leftover, said = self.staged_leftover(), []
        with fx.ImportPath(self.qa):
            code = research_job.run(self.qa, (fx.GAME,), now=lambda: fx.FIXED_TIME, say=said.append, no_update=True,
                                    only=('E_901/NO_SUCH_VARIANT',))
        self.assertEqual(code, research_job.EXIT_REFUSED, said)
        self.assertIn('--only names no variant of this tree', '\n'.join(said))
        self.assertEqual(said[-1], 'RESEARCH JOB - END - refused before any game was worked; nothing was written.')
        self.assertFalse(snapshot.is_due(self.qa))                       # no note: nothing was written
        self.assertEqual(leftover.read_bytes(), b'left by an interrupted status write\r\n')    # nor tidied
        self.assertNotIn('BACKUP', '\n'.join(said))

    def test_a_refusal_that_follows_the_note_is_said_as_it_is_and_the_owed_backup_is_tried(self):
        refuse = mock.Mock(side_effect=status_file.StatusRefused('an invented refusal after the first write'))
        with mock.patch.object(research_job, 'read_statuses', refuse):
            code, text = self.job(self.qa)
        self.assertEqual(code, research_job.EXIT_REFUSED, text)
        self.assertNotIn('nothing was written', text)
        self.assertIn('BACKUP MADE AND VERIFIED: ', text)
        self.assertTrue(text.endswith('the tree\'s note that a backup is owed had been written, so that backup was '
                                      'tried (above).'))
        self.assertFalse(snapshot.is_due(self.qa))
        self.assertFalse((self.qa / 'records' / 'JOB.lock').exists())

    def test_a_note_that_cannot_be_written_refuses_the_job_before_it_writes_research(self):
        (self.qa / snapshot.DUE_PATH).mkdir(parents=True)                # a folder where the note should be
        with self.assertRaisesRegex(job_lock.LaunchRefused, 'the note that a backup is owed could not be written'):
            snapshot.mark_due(self.settings)

    def test_the_jobs_end_line_gives_the_time_after_its_backup(self):
        code, text = self.job(self.qa, clock=self.a_clock_that_runs())
        self.assertEqual(code, 0, text)
        lines = text.split('\n')
        start = next(line for line in lines if line.startswith('RESEARCH JOB - START - '))
        end = next(line for line in lines if line.startswith('RESEARCH JOB - END - '))
        self.assertLess(lines.index(next(line for line in lines if line.startswith('BACKUP MADE'))), lines.index(end))
        self.assertGreater(end[len('RESEARCH JOB - END - '):][:16], start[len('RESEARCH JOB - START - '):][:16])
        self.assertEqual(lines[-1], 'The job finished.')

    def test_if_no_backup_can_be_made_the_job_goes_on_and_every_job_says_so_until_one_is_made(self):
        if self.backups.exists():
            self.backups.rmdir()
        self.backups.write_bytes(b'a file where the backup root should be')
        code, text = self.job(self.qa)
        self.assertEqual(code, 0, text)
        self.assertIn('BACKUP NOT MADE: ', text)
        self.assertLess(text.index(snapshot.STANDING_WARNING), text.index('RESEARCH JOB - END - '))
        self.assertTrue(text.endswith('The job finished.'))           # the job's verdict is still said last
        self.assertTrue(snapshot.is_due(self.qa))
        code, text = self.job(self.qa)                           # the next job: it tries first, and says so twice
        self.assertEqual(code, 0, text)
        self.assertIn('A backup is owed from earlier work in this tree; it is tried first.', text)
        self.assertEqual(text.count(snapshot.STANDING_WARNING), 2)
        self.assertLess(text.index(snapshot.STANDING_WARNING), text.index('Reading this tree\'s own Python environment'))
        self.backups.unlink()                                    # the owner puts the backup root right
        code, text = self.job(self.qa, clock=self.a_clock_that_runs())
        self.assertEqual(code, 0, text)
        self.assertIn('A backup is owed from earlier work in this tree; it is tried first.', text)
        self.assertIn('BACKUP MADE AND VERIFIED: ', text)
        self.assertFalse(snapshot.is_due(self.qa))

    def test_in_dev_a_job_makes_no_backup_writes_no_note_and_says_nothing_of_one(self):
        dev = self.tree(role='DEV', with_source=False, name='dev')
        code, text = self.job(dev)
        self.assertEqual(code, 0, text)
        self.assertNotIn('BACKUP', text)
        self.assertFalse(snapshot.is_due(dev))
        self.assertFalse((dev / snapshot.LOG_PATH).exists())

    def test_a_job_that_is_refused_before_it_writes_leaves_no_note_and_makes_no_backup(self):
        (self.qa / 'src' / 'stray.py').write_bytes(b'# not installed\r\n')
        code, text = self.job(self.qa)
        self.assertEqual(code, research_job.EXIT_REFUSED, text)
        self.assertFalse(snapshot.is_due(self.qa))
        self.assertNotIn('BACKUP', text)


class TheCommandRunSnapshot(InventedQaTree):
    """Deployment design section 10: Run_Snapshot.bat asks for a backup at any time; it is made only if the tree
    is quiet."""

    def run_command(self) -> tuple:
        """Run the command; return (exit code, lines said)."""
        said = []
        return snapshot.main([], self.qa, say=said.append), said

    def test_it_makes_a_backup_named_manual_and_says_so(self):
        code, said = self.run_command()
        self.assertEqual(code, snapshot.EXIT_MADE, said)
        self.assertRegex(said[0], r'^BACKUP - START - the QA tree at ')
        self.assertRegex(said[1], r'^BACKUP MADE AND VERIFIED: .*_MANUAL\.zip ')
        self.assertEqual(said[-1], 'BACKUP - END')

    def test_it_says_why_when_none_was_made_and_its_exit_code_says_so_too(self):
        with job_lock.job_lock(self.qa, 'a test', 'now'):
            code, said = self.run_command()
        self.assertEqual(code, snapshot.EXIT_NOT_MADE)
        self.assertIn('BACKUP NOT MADE: a job of this tree holds its lock', said[1])

    def test_the_launcher_lets_the_backup_command_past_a_backups_own_lock_and_no_other_command(self):
        text = (Path(research_job.__file__).resolve().parents[1] / 'research_command.py').read_text(encoding='utf-8')
        self.assertIn("finishing = LOCK_PATH if arguments[0] == 'snapshot' else None", text)
        self.assertIn('check_at_launch(TREE_ROOT, finishing)', text)


if __name__ == '__main__':
    unittest.main()
