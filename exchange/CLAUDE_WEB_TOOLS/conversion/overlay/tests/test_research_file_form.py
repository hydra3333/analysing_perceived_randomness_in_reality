"""Tests that the research engine writes each of its files in the form the project's standard gives it: every
text file with each line ending CRLF, every line-record file (.jsonl) with LF.

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; doc/FILE_FORM_STANDARD_v0_1.md sections 1, 3, 3B and 4).

Which of the project's own modules it uses
    research_fixtures       invented trees, toy variants and the research job run in them
    file_form (deploy/)     the project's one checker of the form of a file
    research.windows_text, research.status_file, research.reports, research.derived_check, research.job_lock,
    research.withdraw       the writers under test

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
from research import derived_check, job_lock, reports, status_file, withdraw       # noqa: E402
from research.status_file import GameStatus                # noqa: E402
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


class TheStatusFile(unittest.TestCase):
    """VARIANT_STATUS.ini is a settings file: CRLF, with its check over the bytes as they are written."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.tree = fx.make_tree(Path(self.folder.name) / 'tree')
        variant_folder = fx.add_toy_variant(self.tree, FAMILY, VARIANT, games=(GAME,))
        self.path = variant_folder / status_file.STATUS_FILE_NAME
        self.statuses = {GAME: GameStatus()}

    def test_the_rendered_file_ends_every_line_crlf(self):
        data = status_file.render(FAMILY, VARIANT, self.statuses)
        self.assertEqual(crlf_faults(data), [])
        self.assertIn(b'[check]\r\nsha256 = ', data)
        self.assertTrue(data.endswith(b'\r\n'))

    def test_a_written_status_file_is_crlf_on_disk_and_reads_back(self):
        status_file.write_status(self.path, FAMILY, VARIANT, self.statuses)
        self.assertEqual(crlf_faults(self.path.read_bytes()), [])
        self.assertEqual(status_file.read_status(self.path, (GAME,)), self.statuses)

    def test_a_status_file_in_the_old_lf_form_is_refused(self):
        self.path.write_bytes(status_file.render(FAMILY, VARIANT, self.statuses).replace(b'\r\n', b'\n'))
        with self.assertRaises(status_file.StatusRefused) as refusal:
            status_file.read_status(self.path, (GAME,))
        self.assertIn('every line ending CRLF', str(refusal.exception))

    def test_one_line_of_a_status_file_changed_to_lf_is_caught_by_its_check(self):
        data = status_file.render(FAMILY, VARIANT, self.statuses)
        self.path.write_bytes(data.replace(b'status = ACTIVE\r\n', b'status = ACTIVE\n', 1))
        with self.assertRaises(status_file.StatusRefused):
            status_file.read_status(self.path, (GAME,))


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
    """The not-current marker and a lock file are text files too: CRLF."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.tree = Path(self.folder.name)

    def test_the_not_current_marker_is_crlf_and_reads_back(self):
        derived_check.write_cutoff(self.tree, GAME, 1601, 'MISMATCH', 'a score differs at draw 1601')
        data = derived_check.cutoff_path(self.tree, GAME).read_bytes()
        self.assertEqual(crlf_faults(data), [])
        self.assertGreater(data.count(b'\r\n'), 2)
        self.assertEqual(derived_check.read_cutoff(self.tree, GAME)[0], 1601)

    def test_a_lock_file_is_one_line_ending_crlf(self):
        path = self.tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME
        with job_lock.FileLock(path, 'research job', '2026-12-01 20:10'):
            data = path.read_bytes()
        self.assertEqual(crlf_faults(data), [])
        self.assertEqual(data.count(b'\r\n'), 1)
        self.assertTrue(data.startswith(b'research job; started 2026-12-01 20:10; process '))


class EverythingAJobWrites(fx.JobCase):
    """The whole of it at once: after a research job and a withdrawal in an invented tree, the project's own
    checker finds every file the engine wrote in its form, and the lists are the LF exception."""

    def written_files(self, tree: Path) -> list:
        """Every file under the folders the engine writes in, and every status file, from the tree root."""
        paths = file_form.files_under(tree, WRITTEN_FOLDERS, with_root_files=False)
        paths += [path.relative_to(tree).as_posix() for path in sorted(tree.rglob(status_file.STATUS_FILE_NAME))]
        return paths

    def test_every_file_a_job_and_a_withdrawal_write_is_in_its_form(self):
        tree = self.tree()
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        with fx.ImportPath(tree):
            withdrawn = withdraw.withdraw(tree, [(FAMILY, 'TOY_B_V1')], (GAME,), 'a test of the file forms',
                                          ask=lambda _question: 'WITHDRAW', say=lambda _line: None,
                                          now=lambda: fx.FIXED_TIME)
        self.assertEqual(withdrawn, withdraw.EXIT_DONE)
        paths = self.written_files(tree)
        endings = {Path(path).suffix for path in paths}
        self.assertLessEqual({'.txt', '.csv', '.jsonl', '.ini'}, endings, paths)
        faults = file_form.faults_of_files(tree, paths)
        self.assertEqual(faults, [], '\n' + file_form.describe(faults))

    def test_the_lists_are_lf_and_the_reports_are_crlf(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        paths = self.written_files(tree)
        lists = [path for path in paths if path.endswith('.jsonl')]
        texts = [path for path in paths if path.endswith(('.txt', '.csv', '.ini'))]
        self.assertTrue(lists and texts)
        for path in lists:
            self.assertNotIn(b'\r', (tree / path).read_bytes(), path)
        for path in texts:
            data = (tree / path).read_bytes()
            self.assertEqual(data.count(b'\n'), data.count(b'\r\n'), path)
            self.assertGreater(data.count(b'\r\n'), 0, path)

    def test_a_planted_lf_report_and_a_planted_crlf_list_are_each_named_by_the_checker(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        paths = self.written_files(tree)
        report = next(path for path in paths if path.endswith('.txt'))
        listed = next(path for path in paths if path.endswith('.jsonl'))
        (tree / report).write_bytes((tree / report).read_bytes().replace(b'\r\n', b'\n'))
        (tree / listed).write_bytes((tree / listed).read_bytes().replace(b'\n', b'\r\n'))
        named = {fault.path for fault in file_form.faults_of_files(tree, paths)}
        self.assertEqual(named, {report, listed})


if __name__ == '__main__':
    unittest.main()
