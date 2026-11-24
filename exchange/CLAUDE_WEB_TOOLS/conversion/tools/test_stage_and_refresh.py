"""Tests of the program that stages the converted files and refreshes the working copy, on an invented
repository whose Git converts line endings as the owner's does (core.autocrlf true).

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; doc/FILE_FORM_STANDARD_v0_2.md section 5).

Which of the project's own modules it uses
    stage_and_refresh, convert_to_file_form (beside this file)     the program under test and what it shares
    file_form (../overlay/deploy/)                                 the standard's rule

What uses it
    Claude, in the cloud workspace, and the rehearsal:  python -B -m unittest test_stage_and_refresh
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
RULE_SOURCE = HERE.parent / 'overlay' / 'deploy' / 'file_form.py'
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RULE_SOURCE.parent))

import convert_to_file_form as conversion                  # noqa: E402  (after the path lines above)
import file_form                                            # noqa: E402
import stage_and_refresh as staging                         # noqa: E402

# The attribute files of the invented repository: before (as the project's root file is today, in short) and
# after (Git converts nothing, and the other project's folder keeps the behaviour it had).
OLD_ATTRIBUTES = b'*.bat text eol=crlf\nsource_data/** -text\n'
NEW_ATTRIBUTES = b'* -text\r\nGAIS/** !text\r\nGAIS/**/*.bat text eol=crlf\r\n'
# Every file of the invented repository as Git stores it before the conversion: {path: bytes}.
COMMITTED = {
    'src/a.py': b'x = 1\ny = 2\n',                       # listed; on disk LF, as a package's copy left it
    'src/b.py': b'z = 3\n',                              # listed; on disk CRLF, as Git's checkout left it
    'Run.bat': b'@echo off\necho hi\n',                  # listed; on disk CRLF by the old attribute line
    'exchange/EX_001.md': b'# history\nsecond line\n',   # frozen history; on disk CRLF, as checkout left it
    'exchange/helper.sh': b'#!/bin/bash\necho hi\n',     # frozen history, executable
    'doc/already_crlf.md': b'kept\r\nas committed\r\n',  # frozen history that Git stores CRLF
    'source_data/master.csv': b'Draw,Date\r\n1,x\r\n',   # stored byte for byte before and after
    'GAIS/notes.txt': b'another project\nits own\n',     # the other project: left exactly as it is
}
LISTED = ('src/a.py', 'src/b.py', 'Run.bat', '.gitattributes', 'deploy/file_form.py')


def sha(data: bytes) -> str:
    """SHA-256 of some bytes."""
    return hashlib.sha256(data).hexdigest()


class RepositoryCase(unittest.TestCase):
    """An invented repository in the state the owner's is in after the conversion program has finished: the
    listed files are in their form on disk, the new attribute file is in place, nothing is staged."""

    # Whether the checkout is left to grow older than a second before Git's index is next written. Git then
    # trusts what it remembers of each file's size and time, as it does on the owner's PC; without the wait it
    # reads again every file written in the same second as its index, which hides the fault this is here for.
    LET_GIT_SETTLE = False

    def git(self, *arguments: str, given: bytes | None = None) -> bytes:
        """Run one Git command in the invented repository; return what it printed."""
        return subprocess.run(['git', '-C', str(self.tree), *arguments], input=given, capture_output=True,
                              check=True).stdout

    def setUp(self):
        if shutil.which('git') is None:
            self.skipTest('Git is not available here')
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name).resolve()
        self.tree = self.root / 'tree'
        self.tree.mkdir()
        self.git('init', '-q')
        # The first commit is made with no conversion, so that Git stores exactly the bytes of COMMITTED.
        for key, value in (('core.autocrlf', 'false'), ('user.name', 'test'), ('user.email', 'test@example.invalid')):
            self.git('config', key, value)
        for path, data in {**COMMITTED, '.gitattributes': OLD_ATTRIBUTES}.items():
            self.put(path, data)
        (self.tree / 'exchange/helper.sh').chmod(0o755)
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'as it was')
        # The working copy as a checkout on the owner's PC leaves it: Git writes CRLF where it stores LF.
        self.git('config', 'core.autocrlf', 'true')
        for path in COMMITTED:
            (self.tree / path).unlink()
        self.git('checkout', '--', '.')
        if self.LET_GIT_SETTLE:
            time.sleep(1.2)
        # src/a.py as a package's copy left it (Git's own bytes), and Git told so.
        self.put('src/a.py', COMMITTED['src/a.py'])
        self.git('add', 'src/a.py')
        self.assertEqual(self.git('status', '--porcelain'), b'')
        self.head = self.git('rev-parse', 'HEAD')
        # The conversion: the package's files, and every listed file brought to its form.
        self.rule_bytes = file_form.to_form(RULE_SOURCE.read_bytes(), file_form.CRLF)
        self.put('.gitattributes', NEW_ATTRIBUTES)
        self.put('deploy/file_form.py', self.rule_bytes)
        for path in ('src/a.py', 'src/b.py', 'Run.bat'):
            in_its_form = file_form.to_form(COMMITTED[path], file_form.CRLF)
            if self.disk(path) != in_its_form:          # a file already in its form is not written again
                self.put(path, in_its_form)
        entries = [{'path': path, 'form': 'CRLF', 'sha256_before': 'not used here',
                    'sha256_after': sha((self.tree / path).read_bytes())} for path in LISTED]
        self.list_path = self.root / 'CONVERSION_LIST.json'
        self.list_path.write_bytes(json.dumps({'kind': conversion.LIST_KIND, 'files': entries}).encode('ascii'))
        self.rule_path = self.root / 'package' / conversion.RULE_FILE_NAME
        self.rule_path.parent.mkdir()
        self.rule_path.write_bytes(self.rule_bytes)
        self.said = []

    def put(self, path: str, data: bytes) -> None:
        """Write one file of the invented repository, in binary."""
        full = self.tree / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(data)

    def run_it(self, *words, look_only=False, checkpoint=lambda path: None) -> int:
        """Run the program. words: what the owner types. Returns the exit code; self.said holds the lines."""
        words = list(words)
        self.questions = []

        def ask(question):
            self.questions.append(question)
            return words.pop(0) if words else ''
        return staging.run(self.tree, self.list_path, look_only=look_only, ask=ask, say=self.said.append,
                           checkpoint=checkpoint, rule_path=self.rule_path)

    def staged(self, path: str) -> bytes:
        """The bytes Git's index holds for a path."""
        return self.git('show', f':{path}')

    def disk(self, path: str) -> bytes:
        return (self.tree / path).read_bytes()

    def text_said(self) -> str:
        return '\n'.join(self.said)

    def whole_state(self) -> tuple:
        """Everything a run could change: the index's tree and every working file's bytes."""
        files = {path.relative_to(self.tree).as_posix(): path.read_bytes() for path in sorted(self.tree.rglob('*'))
                 if path.is_file() and '.git/' not in path.relative_to(self.tree).as_posix() + '/'}
        return self.git('write-tree'), files


class TheWholeOfIt(RepositoryCase):
    """Standard section 5: what is on disk is what is committed."""

    def test_every_listed_file_is_staged_with_exactly_the_bytes_on_disk(self):
        self.assertEqual(self.run_it('STAGE'), staging.EXIT_DONE, self.text_said())
        for path in LISTED:
            self.assertEqual(self.staged(path), self.disk(path), path)
            self.assertEqual(file_form.faults_in_bytes(self.staged(path), file_form.CRLF), [], path)

    def test_a_listed_file_that_was_in_its_form_on_disk_all_along_is_staged_all_the_same(self):
        # Run.bat and src/b.py were CRLF on disk before the conversion and were not written by it: Git has no
        # reason of its own to look at them again, and its index holds them with LF.
        self.assertEqual(self.staged('Run.bat'), COMMITTED['Run.bat'])
        self.run_it('STAGE')
        self.assertEqual(self.staged('Run.bat'), b'@echo off\r\necho hi\r\n')
        self.assertEqual(self.staged('src/b.py'), b'z = 3\r\n')

    def test_frozen_history_goes_back_on_disk_to_gits_own_bytes_and_nothing_of_it_is_staged(self):
        self.assertEqual(self.disk('exchange/EX_001.md'), b'# history\r\nsecond line\r\n')
        self.run_it('STAGE')
        self.assertEqual(self.disk('exchange/EX_001.md'), COMMITTED['exchange/EX_001.md'])
        self.assertEqual(self.disk('doc/already_crlf.md'), COMMITTED['doc/already_crlf.md'])
        staged = self.git('diff', '--cached', '--name-only').decode().split()
        self.assertEqual(sorted(staged), sorted(LISTED))

    def test_git_sees_no_change_on_disk_that_is_not_staged_and_nothing_is_committed(self):
        self.run_it('STAGE')
        self.assertEqual(self.git('diff-files', '--name-only'), b'')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.head)
        self.assertIn('Nothing was committed or pushed', self.said[-1])

    def test_the_other_projects_folder_is_left_exactly_as_it_is(self):
        before = self.disk('GAIS/notes.txt')
        self.assertEqual(before, b'another project\r\nits own\r\n')
        self.run_it('STAGE')
        self.assertEqual(self.disk('GAIS/notes.txt'), before)
        self.assertEqual(self.staged('GAIS/notes.txt'), COMMITTED['GAIS/notes.txt'])

    def test_a_file_stored_byte_for_byte_and_an_executable_keep_what_git_records_of_them(self):
        modes_before = self.git('ls-files', '-s', '--', 'exchange', 'source_data')
        self.run_it('STAGE')
        self.assertEqual(self.git('ls-files', '-s', '--', 'exchange', 'source_data'), modes_before)
        self.assertEqual(self.disk('source_data/master.csv'), COMMITTED['source_data/master.csv'])

    def test_after_the_commit_a_fresh_clone_gives_the_working_copy_byte_for_byte(self):
        self.run_it('STAGE')
        self.git('commit', '-q', '-m', 'the conversion')
        clone = self.root / 'clone'
        subprocess.run(['git', 'clone', '-q', '-c', 'core.autocrlf=true', str(self.tree), str(clone)], check=True,
                       capture_output=True)
        for path in list(COMMITTED) + list(LISTED):
            if not path.startswith('GAIS/'):
                self.assertEqual((clone / path).read_bytes(), self.disk(path), path)

    def test_a_second_run_finds_nothing_to_do_and_asks_nothing(self):
        self.run_it('STAGE')
        state = self.whole_state()
        self.said.clear()
        self.assertEqual(self.run_it(), staging.EXIT_DONE, self.text_said())
        self.assertEqual(self.questions, [])
        self.assertEqual(self.whole_state(), state)

    def test_a_refresh_interrupted_part_way_is_finished_by_the_next_run(self):
        def fail_at_the_second(path, seen=[]):
            seen.append(path)
            if len(seen) == 2:
                raise PermissionError(13, 'The process cannot access the file', path)
        self.assertEqual(self.run_it('STAGE', checkpoint=fail_at_the_second), staging.EXIT_STOPPED)
        self.assertIn('Do not commit', self.said[-1])
        self.assertEqual(self.run_it('STAGE'), staging.EXIT_DONE, self.text_said())
        self.assertEqual(self.git('diff-files', '--name-only'), b'')


class WhenGitTrustsWhatItRemembers(RepositoryCase):
    """The owner's case: Git's index is older than the files, so Git goes by each file's remembered size and time
    and does not read it again."""

    LET_GIT_SETTLE = True

    def test_plain_git_passes_over_a_listed_file_it_believes_unchanged_and_the_program_does_not(self):
        self.git('add', '--', 'Run.bat', 'src/b.py')
        self.assertEqual(self.staged('Run.bat'), COMMITTED['Run.bat'], 'plain "git add" staged it after all')
        self.assertEqual(self.run_it('STAGE'), staging.EXIT_DONE, self.text_said())
        self.assertEqual(self.staged('Run.bat'), b'@echo off\r\necho hi\r\n')
        self.assertEqual(self.staged('src/b.py'), b'z = 3\r\n')

    def test_git_is_told_of_every_rewritten_working_copy_so_that_it_reports_none_as_changed(self):
        self.assertEqual(self.run_it('STAGE'), staging.EXIT_DONE, self.text_said())
        self.assertEqual(self.git('diff-files', '--name-only'), b'')
        unstaged = [line for line in self.git('status', '--porcelain').decode().splitlines() if line[1] != ' ']
        self.assertEqual(unstaged, [])


    def test_the_proof_asks_git_itself_and_stops_if_git_still_sees_an_unstaged_change(self):
        with mock.patch.object(staging, 'note_refreshed', lambda tree, paths: None):
            self.assertEqual(self.run_it('STAGE'), staging.EXIT_STOPPED)
        self.assertIn('Git still sees a change on disk that is not staged', self.text_said())
        self.assertIn('Do not commit', self.said[-1])


class WhatStopsItBeforeAnythingIsChanged(RepositoryCase):
    """Each of these is named, and neither the index nor any working file is changed."""

    def assert_stops_unchanged(self, expected: str, *words):
        state = self.whole_state()
        self.assertEqual(self.run_it(*(words or ('STAGE',))), staging.EXIT_STOPPED, self.text_said())
        self.assertIn(expected, self.text_said())
        self.assertEqual(self.questions, [])
        self.assertEqual(self.whole_state(), state)

    def test_a_listed_file_that_is_not_at_the_lists_after(self):
        self.put('src/a.py', COMMITTED['src/a.py'])
        self.assert_stops_unchanged('src/a.py: on the conversion list but not at the list\'s "after" on disk')

    def test_frozen_history_changed_here_in_more_than_line_endings_is_not_touched(self):
        self.put('exchange/EX_001.md', b'# history\r\nan uncommitted change\r\n')
        self.assert_stops_unchanged('exchange/EX_001.md: its bytes on disk differ from Git\'s in more than line endings')

    def test_a_tracked_file_that_is_missing(self):
        (self.tree / 'doc/already_crlf.md').unlink()
        self.assert_stops_unchanged('doc/already_crlf.md: tracked by Git but not on disk')

    def test_the_word_not_typed(self):
        state = self.whole_state()
        self.assertEqual(self.run_it('stage'), staging.EXIT_NOT_CONFIRMED)
        self.assertEqual(self.whole_state(), state)

    def test_a_look_changes_nothing_and_says_what_would_be_done(self):
        state = self.whole_state()
        self.assertEqual(self.run_it(look_only=True), staging.EXIT_DONE, self.text_said())
        self.assertEqual(self.whole_state(), state)
        self.assertIn('TO BE STAGED, exactly as on disk ....... 5 of the 5 listed file(s)', self.text_said())
        self.assertIn('2 file(s): exchange 2', self.text_said())
        self.assertIn('LOOKED ONLY; nothing was changed', self.said[-1])


if __name__ == '__main__':
    unittest.main()
