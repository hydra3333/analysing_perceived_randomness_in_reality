"""Tests of the project's standard for the form of its text files (line endings), and the suite's own check that
DEV's files keep it.

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; doc/FILE_FORM_STANDARD_v0_2.md sections 3, 3A, 3B, 4 and 6).

Which of the project's own modules it uses
    file_form (deploy/)     the code under test

What uses it
    The project's test suite. Its last class checks the real files of the tree the suite runs in: it fails until
    that tree has been converted to the standard, and afterwards whenever a file arrives in the wrong form.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# The checker is imported from deploy/, as the tools that use it import it.
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import file_form                                            # noqa: E402  (after the path line above)
from file_form import BINARY, CRLF, LF                      # noqa: E402

# The suite's scope in DEV (standard section 6): everything under these folders, and the root's own files.
SUITE_FOLDERS = ('src', 'deploy', 'tests')
# Where the project's programs lie, for the search of section 4. What a test writes in a temporary folder is not
# the project's own (standard section 2), so the tests' own code is not searched.
PROGRAM_FOLDERS = ('src', 'deploy', 'CLAUDE_CODE_WORKING_FOLDER_TREE/tools')


class TheListOfKinds(unittest.TestCase):
    """Standard section 3: each kind of file has exactly one form, decided from its name."""

    def test_every_text_kind_of_the_table_is_crlf(self):
        for name in ('a.py', 'Run_Research.bat', 'x.cmd', 'ENVIRONMENT.ini', 'VARIANT.json', 'master.csv',
                     'README.txt', 'job.log', 'notes.md', 'JOB.lock', '.gitattributes', '.gitignore', 'LICENSE',
                     'SNAPSHOT_DUE', 'records/SNAPSHOT_IN_PROGRESS.lock', 'src\\research\\reader.py'):
            self.assertEqual(file_form.form_of(name), CRLF, name)

    def test_a_line_record_file_is_the_one_exception_and_is_lf(self):
        self.assertEqual(file_form.form_of('results/research/POWERBALL/E_001/V1/FORECASTS.jsonl'), LF)
        self.assertEqual(file_form.form_of('helper.sh'), LF)

    def test_binary_kinds_are_binary_by_their_kind_alone(self):
        for name in ('backup.zip', 'paper.pdf', 'a.png', 'b.jpg', 'c.gif', 'd.ico', 'm.pyc'):
            self.assertEqual(file_form.form_of(name), BINARY, name)

    def test_upper_case_in_the_end_of_a_name_changes_nothing(self):
        self.assertEqual(file_form.form_of('OLD.BAT'), CRLF)
        self.assertEqual(file_form.form_of('LIST.JSONL'), LF)

    def test_a_kind_the_table_does_not_name_has_no_form(self):
        for name in ('notes.docx', 'data.xml', 'Makefile', 'settings.toml', 'license'):
            self.assertIsNone(file_form.form_of(name), name)

    def test_exactly_the_six_files_of_the_retired_machinery_are_left_out_by_name(self):
        self.assertEqual(len(file_form.LEFT_OUT_BY_NAME), 6)
        for path in file_form.LEFT_OUT_BY_NAME:
            self.assertTrue(file_form.is_left_out_by_name(path), path)
            self.assertTrue(file_form.is_left_out_by_name(path.replace('/', '\\').upper()), path)
        self.assertFalse(file_form.is_left_out_by_name('src/results_master_v0_3.py'))
        self.assertFalse(file_form.is_left_out_by_name('src/package_tools/process_check.py.txt'))


class WhatConformsMeans(unittest.TestCase):
    """Standard section 3B, rule by rule."""

    def test_a_crlf_file_with_every_line_ending_crlf_conforms(self):
        self.assertEqual(file_form.faults_in_bytes(b'one\r\ntwo\r\n', CRLF), [])

    def test_an_empty_file_conforms_in_either_form(self):
        self.assertEqual(file_form.faults_in_bytes(b'', CRLF), [])
        self.assertEqual(file_form.faults_in_bytes(b'', LF), [])

    def test_a_last_line_with_no_line_ending_is_allowed(self):
        self.assertEqual(file_form.faults_in_bytes(b'one\r\ntwo', CRLF), [])
        self.assertEqual(file_form.faults_in_bytes(b'{"a":1}\n{"b":2}', LF), [])

    def test_a_crlf_file_with_one_line_ending_lf_alone_is_a_fault_and_the_line_is_named(self):
        faults = file_form.faults_in_bytes(b'one\r\ntwo\r\nthree\nfour\r\n', CRLF)
        self.assertEqual(len(faults), 1)
        self.assertIn('1 line(s) end LF alone, the first at line 3', faults[0])

    def test_a_crlf_file_with_a_carriage_return_no_line_feed_follows_is_a_fault(self):
        faults = file_form.faults_in_bytes(b'one\r\ntwo\rthree\r\n', CRLF)
        self.assertEqual(len(faults), 1)
        self.assertIn('1 carriage return(s) that no line feed follows, the first at line 2', faults[0])

    def test_two_carriage_returns_before_a_line_feed_is_a_fault(self):
        faults = file_form.faults_in_bytes(b'one\r\r\ntwo\r\n', CRLF)
        self.assertEqual(len(faults), 1)
        self.assertIn('no line feed follows', faults[0])

    def test_an_lf_file_with_any_carriage_return_is_a_fault(self):
        self.assertEqual(file_form.faults_in_bytes(b'{"a":1}\n{"b":2}\n', LF), [])
        faults = file_form.faults_in_bytes(b'{"a":1}\n{"b":2}\r\n', LF)
        self.assertEqual(len(faults), 1)
        self.assertIn('must be LF but holds 1 carriage return(s), the first at line 2', faults[0])

    def test_a_text_kind_holding_a_zero_byte_is_refused_not_passed_over_as_binary(self):
        faults = file_form.faults_in_bytes(b'one\r\n\x00two\r\n', CRLF)
        self.assertTrue(any('zero byte' in fault and 'byte 6' in fault for fault in faults), faults)

    def test_a_text_kind_that_does_not_read_as_utf8_is_refused(self):
        faults = file_form.faults_in_bytes(b'caf\xe9\r\n', CRLF)
        self.assertEqual(len(faults), 1)
        self.assertIn('does not read as UTF-8 at byte 4', faults[0])

    def test_a_form_that_is_not_text_is_refused_by_the_byte_check(self):
        with self.assertRaises(file_form.FileFormRefused):
            file_form.faults_in_bytes(b'', BINARY)


class CheckingFilesOfATree(unittest.TestCase):
    """Standard section 6: the checker reads the disk, names each file and skips nothing silently."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)

    def put(self, relative_path: str, data: bytes) -> str:
        """Write one file of the invented tree, in binary so that its bytes are exactly those given."""
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return relative_path

    def test_a_conforming_tree_has_no_fault(self):
        paths = [self.put('src/a.py', b'x = 1\r\n'), self.put('results/L.jsonl', b'{"a":1}\n'),
                 self.put('LICENSE', b'text\r\n'), self.put('tests/empty.json', b'')]
        self.assertEqual(file_form.faults_of_files(self.root, paths), [])

    def test_a_file_in_the_wrong_form_is_named_with_its_path(self):
        paths = [self.put('src/a.py', b'x = 1\r\n'), self.put('src/b.py', b'y = 2\n')]
        faults = file_form.faults_of_files(self.root, paths)
        self.assertEqual([fault.path for fault in faults], ['src/b.py'])
        self.assertIn('must be CRLF', faults[0].what)

    def test_a_line_record_file_with_crlf_is_named(self):
        faults = file_form.faults_of_files(self.root, [self.put('results/L.jsonl', b'{"a":1}\r\n')])
        self.assertEqual(len(faults), 1)
        self.assertIn('must be LF', faults[0].what)

    def test_a_file_of_a_kind_the_table_does_not_name_is_refused_and_named(self):
        faults = file_form.faults_of_files(self.root, [self.put('src/notes.docx', b'anything')])
        self.assertEqual(len(faults), 1)
        self.assertIn('a kind the standard does not name', faults[0].what)

    def test_a_binary_kind_is_never_read(self):
        self.assertEqual(file_form.faults_of_files(self.root, [self.put('tests/x.zip', b'PK\x00\x01\n')]), [])

    def test_a_file_left_out_by_name_is_not_checked_whatever_it_holds(self):
        path = self.put('src/results_master_v0_2.py', b'x = 1\n')
        self.assertEqual(file_form.faults_of_files(self.root, [path]), [])
        other = self.put('src/results_master_v0_3.py', b'x = 1\n')
        self.assertEqual(len(file_form.faults_of_files(self.root, [other])), 1)

    def test_a_file_that_cannot_be_read_is_a_fault_not_a_pass(self):
        faults = file_form.faults_of_files(self.root, ['src/not_there.py'])
        self.assertEqual(len(faults), 1)
        self.assertIn('could not be read', faults[0].what)

    def test_the_walk_finds_every_file_under_the_named_folders_and_leaves_pythons_cache_out(self):
        self.put('src/a.py', b''), self.put('src/deep/er/b.json', b''), self.put('src/__pycache__/a.pyc', b'')
        self.put('src/deep/__pycache__/c.pyc', b''), self.put('tests/t.py', b''), self.put('LICENSE', b'')
        self.put('.venv/Lib/site-packages/other_peoples.py', b'x\n'), self.put('exchange/EX_001.md', b'x\n')
        self.assertEqual(file_form.files_under(self.root, ('src', 'tests', 'deploy'), with_root_files=True),
                         ['LICENSE', 'src/a.py', 'src/deep/er/b.json', 'tests/t.py'])
        self.assertEqual(file_form.files_under(self.root, ('src',), with_root_files=False),
                         ['src/a.py', 'src/deep/er/b.json'])

    def test_what_the_checker_prints_always_says_the_one_exception(self):
        clean = file_form.describe([])
        self.assertIn('Every file checked is in the form', clean)
        self.assertIn('.jsonl', clean)
        faulty = file_form.describe(file_form.faults_of_files(self.root, [self.put('src/b.py', b'y = 2\n')]))
        self.assertIn('1 fault(s)', faulty)
        self.assertIn('src/b.py: must be CRLF', faulty)
        self.assertIn('.jsonl', faulty)
        self.assertIn('VS Code', faulty)


class LinksAreNeverFollowed(unittest.TestCase):
    """Standard section 6 with the reviewer's EX_308 LOOK-C02: the walk reads the tree's own files only. A link,
    a junction or any other reparse point is set apart, never entered and never read."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name) / 'tree'
        self.elsewhere = Path(self.folder.name) / 'elsewhere'
        for path in ('tree/src/a.py', 'tree/LICENSE', 'elsewhere/secret.py', 'elsewhere/deep/more.py'):
            full = Path(self.folder.name) / path
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_bytes(b'x = 1\r\n')

    def link(self, link: Path, target: Path) -> None:
        """Make a link to a folder or a file; a junction where Windows allows no symbolic link. Skips the test
        where neither can be made."""
        link.parent.mkdir(parents=True, exist_ok=True)
        remove = link.unlink
        try:
            os.symlink(target, link, target_is_directory=target.is_dir())
        except (OSError, NotImplementedError):
            if os.name != 'nt' or not target.is_dir():
                self.skipTest('this account cannot make a symbolic link here')
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
            remove = lambda: os.rmdir(link)                 # a junction is removed as a folder is
        # The link itself is removed before the temporary folder is, never what it points to.
        self.addCleanup(remove)

    def walk(self, folders=('src',), with_root_files=True):
        return file_form.files_and_links_under(self.root, folders, with_root_files)

    def test_a_linked_folder_met_in_the_walk_is_set_apart_and_not_entered(self):
        self.link(self.root / 'src' / 'linked', self.elsewhere)
        self.assertEqual(self.walk(), (['LICENSE', 'src/a.py'], ['src/linked']))

    def test_a_linked_file_is_set_apart_and_not_listed_as_a_file(self):
        self.link(self.root / 'src' / 'b.py', self.elsewhere / 'secret.py')
        self.assertEqual(self.walk(), (['LICENSE', 'src/a.py'], ['src/b.py']))

    def test_a_named_folder_that_is_a_link_is_not_walked(self):
        self.link(self.root / 'records', self.elsewhere)
        self.assertEqual(self.walk(folders=('src', 'records')), (['LICENSE', 'src/a.py'], ['records']))

    def test_a_named_folder_that_lies_under_a_link_is_not_walked_and_the_link_is_named(self):
        self.link(self.root / 'results', self.elsewhere)
        self.assertEqual(self.walk(folders=('src', 'results/deep')), (['LICENSE', 'src/a.py'], ['results']))

    def test_a_link_in_the_root_where_a_file_would_stand_is_set_apart(self):
        self.link(self.root / 'NOTES.txt', self.elsewhere / 'secret.py')
        self.assertEqual(self.walk(), (['LICENSE', 'src/a.py'], ['NOTES.txt']))

    def test_a_linked_folder_in_the_root_that_is_not_walked_is_none_of_the_walks_business(self):
        self.link(self.root / 'other_place', self.elsewhere)
        self.assertEqual(self.walk(), (['LICENSE', 'src/a.py'], []))

    def test_the_plain_walk_refuses_when_it_meets_a_link(self):
        self.assertEqual(file_form.files_under(self.root, ('src',), with_root_files=True), ['LICENSE', 'src/a.py'])
        self.link(self.root / 'src' / 'linked', self.elsewhere)
        with self.assertRaises(file_form.FileFormRefused) as refusal:
            file_form.files_under(self.root, ('src',), with_root_files=True)
        self.assertIn('src/linked', str(refusal.exception))

    def test_the_mark_windows_puts_on_a_junction_or_any_reparse_point_counts_as_a_link(self):
        ordinary = os.lstat(self.root / 'src' / 'a.py')

        class Marked:
            """An ordinary file's status with the reparse-point mark set, as Windows reports a junction."""
            st_mode = ordinary.st_mode
            st_file_attributes = file_form.REPARSE_POINT_ATTRIBUTE | 0x10

        self.assertFalse(file_form.is_link(self.root / 'src' / 'a.py'))
        with mock.patch.object(file_form.os, 'lstat', return_value=Marked()):
            self.assertTrue(file_form.is_link(self.root / 'src' / 'a.py'))
        self.assertFalse(file_form.is_link(self.root / 'not_there'))


class BringingAFileToItsForm(unittest.TestCase):
    """Standard section 7: the conversion changes line endings and nothing else, and never guesses."""

    def test_lf_becomes_crlf_and_a_second_time_changes_nothing(self):
        once = file_form.to_form(b'one\ntwo\n', CRLF)
        self.assertEqual(once, b'one\r\ntwo\r\n')
        self.assertEqual(file_form.to_form(once, CRLF), once)

    def test_a_file_of_mixed_endings_becomes_crlf_throughout(self):
        self.assertEqual(file_form.to_form(b'one\r\ntwo\nthree\r\n', CRLF), b'one\r\ntwo\r\nthree\r\n')

    def test_no_line_ending_is_added_to_a_last_line_that_has_none(self):
        self.assertEqual(file_form.to_form(b'one\ntwo', CRLF), b'one\r\ntwo')
        self.assertEqual(file_form.to_form(b'', CRLF), b'')

    def test_a_line_record_file_becomes_lf(self):
        self.assertEqual(file_form.to_form(b'{"a":1}\r\n{"b":2}\n', LF), b'{"a":1}\n{"b":2}\n')

    def test_a_carriage_return_that_ends_no_crlf_is_refused_not_guessed(self):
        for data in (b'one\rtwo\n', b'one\r\r\ntwo\n', b'one\r'):
            with self.assertRaises(file_form.FileFormRefused, msg=data):
                file_form.to_form(data, CRLF)
            with self.assertRaises(file_form.FileFormRefused, msg=data):
                file_form.to_form(data, LF)

    def test_a_zero_byte_or_bytes_that_are_not_utf8_are_refused(self):
        with self.assertRaises(file_form.FileFormRefused):
            file_form.to_form(b'one\n\x00', CRLF)
        with self.assertRaises(file_form.FileFormRefused):
            file_form.to_form(b'caf\xe9\n', CRLF)

    def test_the_proof_of_line_endings_only_passes_a_conversion_and_fails_any_other_change(self):
        old = b'one\ntwo\r\nthree'
        self.assertTrue(file_form.differ_in_line_endings_only(old, file_form.to_form(old, CRLF)))
        self.assertFalse(file_form.differ_in_line_endings_only(old, b'one\r\ntwo\r\nthree\r\n'))
        self.assertFalse(file_form.differ_in_line_endings_only(old, b'one\r\ntwo\r\nthreE'))
        self.assertFalse(file_form.differ_in_line_endings_only(b'one two', b'one\r\ntwo'))


class EveryProgramSaysWhatItWrites(unittest.TestCase):
    """Standard section 4: a write that leaves the line ending to the platform is found by reading the code."""

    def found(self, source: str) -> list[str]:
        """What the search finds in some source, without the line numbers."""
        return [what for _line, what in file_form.writes_without_a_named_line_ending(source)]

    def test_open_for_writing_text_without_newline_is_found_with_its_line(self):
        source = "import os\n\nwith open('a.txt', 'w', encoding='utf-8') as handle:\n    handle.write('x')\n"
        self.assertEqual(file_form.writes_without_a_named_line_ending(source),
                         [(3, "open() in mode 'w' without newline=")])

    def test_every_writing_text_mode_is_found(self):
        for mode in ('w', 'a', 'x', 'r+', 'w+', 'wt', 'at'):
            self.assertEqual(len(self.found(f"open('a.txt', '{mode}')")), 1, mode)
            self.assertEqual(len(self.found(f"open('a.txt', mode='{mode}')")), 1, mode)

    def test_a_write_that_names_its_line_ending_is_not_found(self):
        self.assertEqual(self.found("open('a.txt', 'w', newline='\\r\\n')"), [])
        self.assertEqual(self.found("path.write_text('x', encoding='utf-8', newline='\\r\\n')"), [])
        self.assertEqual(self.found("path.open('w', newline='')"), [])

    def test_a_binary_write_and_a_read_are_not_found(self):
        for source in ("open('a.bin', 'wb')", "open('a.bin', 'ab')", "open('a.txt')", "open('a.txt', 'r')",
                       "path.open('rb')", "path.open()", "path.read_text()", "path.write_bytes(b'x')"):
            self.assertEqual(self.found(source), [], source)

    def test_write_text_without_newline_is_found(self):
        self.assertEqual(self.found("path.write_text('x', encoding='utf-8')"), ['write_text() without newline='])

    def test_a_paths_open_and_the_modules_own_open_are_each_read_correctly(self):
        self.assertEqual(self.found("path.open('w')"), ["open() in mode 'w' without newline="])
        self.assertEqual(self.found("io.open('a.txt', 'w')"), ["open() in mode 'w' without newline="])
        self.assertEqual(self.found("os.fdopen(descriptor, 'w')"), ["fdopen() in mode 'w' without newline="])
        self.assertEqual(self.found("os.fdopen(descriptor, 'wb')"), [])

    def test_the_low_level_os_open_is_not_a_text_write(self):
        self.assertEqual(self.found("os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)"), [])

    def test_a_mode_that_is_not_written_out_is_found_to_be_safe(self):
        self.assertEqual(self.found("open('a.txt', chosen_mode)"),
                         ['open() with a mode that is not written out, without newline='])

    def test_a_temporary_file_in_a_writing_text_mode_is_found_and_its_binary_default_is_not(self):
        self.assertEqual(len(self.found("tempfile.NamedTemporaryFile(mode='w')")), 1)
        self.assertEqual(self.found("tempfile.NamedTemporaryFile()"), [])
        self.assertEqual(self.found("tempfile.NamedTemporaryFile(mode='w', newline='\\r\\n')"), [])

    def test_a_logging_file_handler_is_found_because_it_cannot_name_one(self):
        self.assertEqual(len(self.found("logging.FileHandler('job.log')")), 1)


class TheLivingProjectKeepsTheStandard(unittest.TestCase):
    """Standard section 6, first row: the suite's check of the tree it runs in, read from the disk."""

    def test_every_file_under_src_deploy_tests_and_the_root_is_in_its_form(self):
        paths = file_form.files_under(REPOSITORY_ROOT, SUITE_FOLDERS, with_root_files=True)
        self.assertGreater(len(paths), 500, 'the walk found too few files to be the project')
        faults = file_form.faults_of_files(REPOSITORY_ROOT, paths)
        self.assertEqual(faults, [], '\n' + file_form.describe(faults))

    def test_no_program_of_the_project_writes_a_text_file_without_naming_its_line_ending(self):
        found = []
        for path in file_form.files_under(REPOSITORY_ROOT, PROGRAM_FOLDERS, with_root_files=True):
            if not path.endswith('.py') or file_form.is_left_out_by_name(path):
                continue
            source = (REPOSITORY_ROOT / path).read_text(encoding='utf-8')
            found.extend(f'{path} line {line}: {what}'
                         for line, what in file_form.writes_without_a_named_line_ending(source))
        self.assertEqual(found, [], '\nEach of these writes CRLF on Windows and LF elsewhere; give it newline= '
                                    '(standard section 4):\n' + '\n'.join(found))


if __name__ == '__main__':
    unittest.main()
