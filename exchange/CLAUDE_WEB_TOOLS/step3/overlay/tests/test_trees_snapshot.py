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
from research import job_lock, process_rule, research_job, snapshot
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

    def test_it_names_the_newest_recovery_kit_of_the_trees_software_state(self):
        fingerprint = snapshot.software_fingerprint(self.qa)
        self.backups.mkdir(exist_ok=True)
        for name in (f'KIT_20261101_080000_{fingerprint[:12]}.zip', f'KIT_20261120_080000_{fingerprint[:12]}.zip',
                     'KIT_20261125_080000_000000000000.zip'):
            (self.backups / name).write_bytes(b'PK invented')
        with zipfile.ZipFile(self.attempt().path) as archive:
            manifest = json.loads(archive.read(snapshot.MANIFEST_NAME))
        self.assertEqual(manifest['recovery_kit'], f'KIT_20261120_080000_{fingerprint[:12]}.zip')


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
            hashes = write(*arguments)
            hashes['ENVIRONMENT.ini'] = '0' * 64
            return hashes

        with mock.patch.object(snapshot, '_write_archive', write_then_misremember):
            self.not_made('ENVIRONMENT.ini read back from the archive is not the file that was read')
        self.assert_nothing_was_left()

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

    def test_the_note_is_written_before_the_jobs_first_write(self):
        seen = []
        run_locked = research_job.run_locked

        def look_then_run(settings, *arguments):
            seen.append((snapshot.is_due(settings.tree_root), (settings.tree_root / 'results' / 'research').exists()))
            return run_locked(settings, *arguments)

        with mock.patch.object(research_job, 'run_locked', look_then_run):
            self.assertEqual(self.job(self.qa)[0], 0)
        self.assertEqual(seen, [(True, False)])

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
