"""Tests that the research engine writes each of its files in the form the project gives it: every text file
with each line ending CRLF, the line-record files (.jsonl) and the small files beside a method included.

Each test is named for the rule it proves and plants the fault that rule must catch
(the simple scheme v0.2: everything CRLF; doc/FILE_FORM_STANDARD_v0_2.md sections 3B and 4).

Which of the project's own modules it uses
    research_fixtures       invented trees, toy variants and the research job run in them
    file_form (deploy/)     the project's one checker of the form of a file
    research.windows_text, reporting.printouts, research.tree_lock, research.method_flags   the writers under test

What uses it
    The project's test suite.
"""
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# The checker is imported from deploy/, as the tools that use it import it.
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import file_form                                            # noqa: E402  (after the path line above)
import research_fixtures as fx                              # noqa: E402
from reporting import printouts as reports                 # noqa: E402
from research import method_flags, tree_lock               # noqa: E402
from research.windows_text import LINE_ENDING, windows_lines                       # noqa: E402

GAME = fx.GAME
FAMILY, VARIANT = 'E_901', 'TOY_A_V1'
# The folders of a tree in which the engine writes (standard section 6, the row for a tree).
WRITTEN_FOLDERS = ('results/research', 'records')


def crlf_faults(data: bytes) -> list:
    """How some bytes fail to be a CRLF file, by the project's one checker; [] when they conform."""
    return file_form.faults_in_bytes(data, file_form.CRLF)


class TheOnePlaceThatMakesWindowsLines(unittest.TestCase):
    """research/windows_text.py: the engine's texts are turned to the standard's form in one place, once."""

    def test_every_line_feed_becomes_crlf_and_no_line_ending_is_added(self):
        self.assertEqual(LINE_ENDING, '\r\n')
        self.assertEqual(windows_lines('one\ntwo\n'), 'one\r\ntwo\r\n')
        self.assertEqual(windows_lines('one\ntwo'), 'one\r\ntwo')
        self.assertEqual(windows_lines(''), '')

    def test_text_that_already_holds_a_carriage_return_is_refused_not_converted_twice(self):
        with self.assertRaises(ValueError):
            windows_lines(windows_lines('one\ntwo\n'))


class TheReportFiles(unittest.TestCase):
    """Reports, read-me files and the side file of making times are text files: CRLF."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.tree = Path(self.folder.name)
        self.writer = reports.ReportWriter(self.tree, GAME, '2026-12-01 20:10')
        self.side_file = self.writer.root / reports.MADE_TIMES_NAME

    def test_a_report_built_with_line_feeds_is_written_crlf(self):
        self.assertTrue(self.writer.write('league/table.txt', 'first line\nsecond line\n'))
        self.assertEqual((self.writer.root / 'league/table.txt').read_bytes(), b'first line\r\nsecond line\r\n')

    def test_a_report_whose_bytes_would_not_change_is_not_written_again(self):
        self.writer.write('README.txt', 'one\n')
        self.assertFalse(self.writer.write('README.txt', 'one\n'))

    def test_a_report_left_in_lf_form_is_written_again_in_crlf(self):
        path = self.writer.root / 'README.txt'
        path.parent.mkdir(parents=True)
        path.write_bytes(b'one\n')
        self.assertTrue(self.writer.write('README.txt', 'one\n'))
        self.assertEqual(path.read_bytes(), b'one\r\n')

    def test_the_side_file_of_making_times_is_crlf_as_it_grows_and_after_it_is_tidied(self):
        self.writer.write('b.txt', 'b\n')
        self.writer.write('a.csv', 'x,y\n1,2\n')
        self.assertEqual(crlf_faults(self.side_file.read_bytes()), [])
        self.assertEqual(self.side_file.read_bytes().count(b'\r\n'), 2)
        self.writer.tidy_times()
        self.assertEqual(self.side_file.read_bytes(),
                         b'file,made\r\na.csv,2026-12-01 20:10\r\nb.txt,2026-12-01 20:10\r\n')

    def test_a_side_file_in_lf_form_but_already_in_order_is_still_put_right(self):
        self.writer.write('a.csv', 'x\n')
        self.writer.tidy_times()
        tidy = self.side_file.read_bytes()
        self.side_file.write_bytes(tidy.replace(b'\r\n', b'\n'))
        self.writer.tidy_times()
        self.assertEqual(self.side_file.read_bytes(), tidy)


class TheSmallFiles(unittest.TestCase):
    """A lock file and the small files beside a method are text files too: CRLF."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.tree = Path(self.folder.name)

    def test_a_retired_file_and_an_in_place_file_are_crlf_and_read_back(self):
        method_flags.write_retired(self.tree, {GAME: 1601}, 'a test of the file forms')
        method_flags.settle_in_place(self.tree, 'ab12', GAME, 1600)
        for name in (method_flags.RETIRED_NAME, method_flags.IN_PLACE_NAME):
            data = (self.tree / name).read_bytes()
            self.assertEqual(crlf_faults(data), [], name)
            self.assertGreater(data.count(b'\r\n'), 2, name)
        self.assertEqual(method_flags.status_of(self.tree, GAME),
                         method_flags.MethodStatus(1601, 'a test of the file forms', 1601))

    def test_a_lock_file_is_one_line_ending_crlf(self):
        path = self.tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME
        with tree_lock.FileLock(path, 'research job', '2026-12-01 20:10'):
            data = path.read_bytes()
        self.assertEqual(crlf_faults(data), [])
        self.assertEqual(data.count(b'\r\n'), 1)
        self.assertTrue(data.startswith(b'research job; started 2026-12-01 20:10; process '))


class EverythingAJobWrites(fx.JobCase):
    """The whole of it at once: after two research jobs in an invented tree, one of them with a method retired,
    the project's own checker finds every file the engine wrote in its form."""

    def written_files(self, tree: Path) -> list:
        """Every file under the folders the engine writes in, and every small file beside a method, from the
        tree root."""
        paths = file_form.files_under(tree, WRITTEN_FOLDERS, with_root_files=False)
        paths += [path.relative_to(tree).as_posix() for name in method_flags.FLAG_NAMES
                  for path in sorted(tree.rglob(name))]
        return paths

    def after_two_jobs(self) -> Path:
        """A tree after a job, a retirement written by hand as an empty file, and a second job."""
        tree = self.tree()
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        (tree / 'src' / 'methods' / FAMILY / 'TOY_B_V1' / method_flags.RETIRED_NAME).write_bytes(b'')
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        return tree

    def test_every_file_two_jobs_write_is_in_its_form(self):
        tree = self.after_two_jobs()
        paths = self.written_files(tree)
        names = {Path(path).suffix or Path(path).name for path in paths}
        self.assertLessEqual({'.txt', '.csv', '.jsonl', 'INFRASTRUCTURE', 'IN_PLACE_SINCE', 'I_AM_RETIRED'}, names,
                             paths)
        faults = file_form.faults_of_files(tree, paths)
        self.assertEqual(faults, [], '\n' + file_form.describe(faults))

    def test_the_lists_and_the_reports_are_crlf(self):
        tree = self.after_two_jobs()
        paths = self.written_files(tree)
        self.assertTrue(any(path.endswith('.jsonl') for path in paths) and any(path.endswith('.txt') for path in paths))
        for path in paths:
            data = (tree / path).read_bytes()
            self.assertEqual(data.count(b'\n'), data.count(b'\r\n'), path)
            self.assertGreater(data.count(b'\r\n'), 0, path)

    def test_a_planted_lf_report_and_a_planted_lf_list_are_each_named_by_the_checker(self):
        tree = self.after_two_jobs()
        paths = self.written_files(tree)
        report = next(path for path in paths if path.endswith('.txt'))
        listed = next(path for path in paths if path.endswith('.jsonl'))
        for path in (report, listed):
            (tree / path).write_bytes((tree / path).read_bytes().replace(b'\r\n', b'\n'))
        named = {fault.path for fault in file_form.faults_of_files(tree, paths)}
        self.assertEqual(named, {report, listed})


if __name__ == '__main__':
    unittest.main()
