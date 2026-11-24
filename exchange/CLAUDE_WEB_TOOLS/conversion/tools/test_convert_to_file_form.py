"""Tests of the conversion program of the file-form standard, on an invented tree.

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; doc/FILE_FORM_STANDARD_v0_2.md section 7; the reviewer's watchpoint of
EX_305 on a resumed run).

Which of the project's own modules it uses
    convert_to_file_form (beside this file)     the program under test
    file_form (../overlay/deploy/)              the standard's rule, copied into each invented tree
    research.job_lock, research.status_file (the repository's src/, when this file is run inside it)
                                                the names the program must share with the engine

What uses it
    Claude, in the cloud workspace, and the rehearsal:  python -B -m unittest test_convert_to_file_form
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULE_SOURCE = HERE.parent / 'overlay' / 'deploy' / 'file_form.py'
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RULE_SOURCE.parent))

import convert_to_file_form as conversion                  # noqa: E402  (after the path lines above)
import file_form                                            # noqa: E402

# The repository this file lies in, when it does: its src/ holds the engine whose names the program shares.
REPOSITORY_SRC = HERE.parents[3] / 'src'

OLD_STATUS = (b'; E_901 / TOY_A_V1 - operating status in THIS tree.\n[POWERBALL]\nstatus = ACTIVE\n'
              b'[check]\nsha256 = 00\n')
# The invented tree: {path: bytes}. LISTED names the files the conversion list holds.
LISTED = {
    'deploy/file_form.py': None,                                    # filled with the rule itself, in its form
    'src/research_command.py': b'"""the program"""\nVALUE = 1\n',
    'src/a.py': b'x = 1\ny = 2\n',
    'src/b.json': b'{\n "a": 1\n}\n',
    'src/empty.py': b'',
    'src/no_last_ending.py': b'x = 1\ny = 2',
    'tests/test_a.py': b'import a\n',
    'Run_Research.bat': b'@echo off\r\necho hello\r\n',            # in its form already
    'source_data/POWERBALL_results_master_init_verification.json': b'{\n "ok": true\n}\n',
}
OTHER = {
    'ENVIRONMENT.ini': b'[tree]\nrole = DEV\n',
    'src/methods/E_901/TOY_A_V1/VARIANT_STATUS.ini': OLD_STATUS,
    'results/research/POWERBALL/variants/E_901/TOY_A_V1/forecasts.jsonl': b'{"a":1}\n{"b":2}\n',
    'results/research/POWERBALL/reports/README.txt': b'old report\n',
    'records/INSTALL_LOG.jsonl': b'{"operation":"X"}\n',
    'source_data/POWERBALL_results_master.csv': b'Draw,Date\r\n1,2026-01-01\r\n',
    'source_data/POWERBALL_results_master_ledger.csv': b'version,sha256\r\n1,ab\r\n',
    'source_data/HOLDOUT_OPENED_POWERBALL.json': b'{\n "opened": true\n}\n',
    'source_data/grabs/page.mhtml': b'anything\nat all\n',
    'src/results_master_v0_2.py': b'# left out by name\nx = 1\n',
    '.venv/Lib/site-packages/other_peoples.py': b'x = 1\n',
    'exchange/EX_001.md': b'# frozen history\n',
    'results/real/development/old_run/record.json': b'{\n "old": 1\n}\n',
    'transitory_data/anything.txt': b'x\n',
}
UNTOUCHED = [path for path in OTHER if not path.startswith(('ENVIRONMENT', 'src/methods/', 'results/research/',
                                                              'records/'))]


def sha(data: bytes) -> str:
    """SHA-256 of some bytes."""
    return hashlib.sha256(data).hexdigest()


def tree_bytes(tree: Path) -> dict:
    """Every file of a tree with its bytes: {path with forward slashes: bytes}."""
    return {path.relative_to(tree).as_posix(): path.read_bytes() for path in sorted(tree.rglob('*')) if path.is_file()}


class Asker:
    """Stands for the owner at the keyboard: answers each question with the next of the given words, and
    remembers the questions."""

    def __init__(self, *words):
        self.words, self.questions = list(words), []

    def __call__(self, question: str) -> str:
        self.questions.append(question)
        return self.words.pop(0) if self.words else ''


class ConversionCase(unittest.TestCase):
    """An invented DEV tree, its conversion list, and the owner's copy of it, each in a temporary folder."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name).resolve()
        self.tree, self.copy = self.root / 'tree', self.root / 'copy'
        self.list_path, self.record_path = self.root / 'CONVERSION_LIST.json', self.root / 'evidence' / 'RECORD.json'
        listed = dict(LISTED)
        listed['deploy/file_form.py'] = file_form.to_form(RULE_SOURCE.read_bytes(), file_form.CRLF)
        # The rule the program uses lies in the package, beside the program; here, in a folder of its own.
        self.rule_path = self.root / 'package' / conversion.RULE_FILE_NAME
        self.rule_path.parent.mkdir()
        self.rule_path.write_bytes(listed['deploy/file_form.py'])
        for path, data in {**listed, **OTHER}.items():
            self.put(path, data)
        entries = []
        for path, data in sorted(listed.items()):
            after = file_form.to_form(data, file_form.CRLF)
            entry = {'path': path, 'form': 'CRLF', 'sha256_before': sha(data), 'sha256_after': sha(after)}
            if path == 'deploy/file_form.py':
                entry['delivered_by_package'] = True
            entries.append(entry)
        self.list_path.write_bytes(json.dumps({'kind': conversion.LIST_KIND, 'files': entries}).encode('ascii'))
        shutil.copytree(self.tree, self.copy)
        self.said = []

    def put(self, path: str, data: bytes) -> None:
        """Write one file of the invented tree, in binary."""
        full = self.tree / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(data)

    def run_it(self, *words, copy=None, look_only=False, checkpoint=lambda path: None):
        """Run the program on the invented tree. words: what the owner types, in order. Returns the exit code;
        self.said holds the lines printed and self.asker the questions asked."""
        self.asker = Asker(*words)
        return conversion.run(self.tree, self.list_path, copy or self.copy, self.record_path, look_only=look_only,
                              ask=self.asker, say=self.said.append, checkpoint=checkpoint, rule_path=self.rule_path)

    def text_said(self) -> str:
        """Everything printed so far, as one text."""
        return '\n'.join(self.said)


class AFirstRun(ConversionCase):
    """Standard section 7 item 2, an uninterrupted run."""

    def test_every_listed_file_is_brought_to_its_form_and_the_run_finishes(self):
        self.assertEqual(self.run_it('CONVERT', 'REMOVE'), conversion.EXIT_DONE, self.text_said())
        for path, data in LISTED.items():
            if data is not None:
                self.assertEqual((self.tree / path).read_bytes(), file_form.to_form(data, file_form.CRLF), path)
        self.assertEqual((self.tree / 'src/no_last_ending.py').read_bytes(), b'x = 1\r\ny = 2')
        self.assertIn('FILE-FORM CONVERSION - END - FINISHED', self.said[-1])
        self.assertIn('.jsonl', self.text_said())

    def test_what_it_found_is_printed_by_class_before_the_first_question(self):
        self.run_it('no')
        before_question = self.text_said()
        for words in ('LISTED, to be converted now ............ 6 file(s) of the 9 listed',
                      'LISTED, in their form already .......... 3 file(s)', 'ENVIRONMENT.ini: to be converted',
                      '4 file(s): research results, status files, control-folder leftovers',
                      'UNTOUCHED, AND PROVED UNTOUCHED ........ 2 results file(s)',
                      'IN NO CLASS, OR NOT AS EXPECTED ........ 0'):
            self.assertIn(words, before_question)
        self.assertEqual(len(self.asker.questions), 1)

    def test_the_trees_own_settings_file_is_converted_by_rule(self):
        self.run_it('CONVERT', 'REMOVE')
        self.assertEqual((self.tree / 'ENVIRONMENT.ini').read_bytes(), b'[tree]\r\nrole = DEV\r\n')

    def test_what_is_made_again_is_removed_and_not_converted(self):
        self.run_it('CONVERT', 'REMOVE')
        self.assertFalse((self.tree / 'results/research').exists())
        self.assertFalse((self.tree / 'src/methods/E_901/TOY_A_V1/VARIANT_STATUS.ini').exists())
        self.assertEqual(list((self.tree / 'records').iterdir()), [])
        self.assertTrue((self.tree / 'src/methods/E_901/TOY_A_V1').is_dir())

    def test_everything_outside_the_classes_is_byte_for_byte_as_it_was(self):
        self.run_it('CONVERT', 'REMOVE')
        for path in UNTOUCHED:
            self.assertEqual((self.tree / path).read_bytes(), OTHER[path], path)

    def test_both_locks_are_held_while_it_works_and_gone_afterwards(self):
        seen = []
        self.run_it('CONVERT', 'REMOVE', checkpoint=lambda path: seen.append(
            ((self.tree / conversion.JOB_LOCK).is_file(), (self.tree / conversion.UPDATER_LOCK).is_file())))
        self.assertTrue(seen and all(both == (True, True) for both in seen))
        self.assertFalse((self.tree / conversion.JOB_LOCK).exists())
        self.assertFalse((self.tree / conversion.UPDATER_LOCK).exists())

    def test_the_record_keeps_the_hash_before_of_every_file_changed_or_removed_and_is_in_the_standards_form(self):
        self.run_it('CONVERT', 'REMOVE')
        data = self.record_path.read_bytes()
        self.assertEqual(file_form.faults_in_bytes(data, file_form.CRLF), [])
        record = json.loads(data)
        self.assertEqual(record['originals_converted']['src/a.py'], sha(LISTED['src/a.py']))
        self.assertEqual(record['originals_converted']['ENVIRONMENT.ini'], sha(OTHER['ENVIRONMENT.ini']))
        self.assertEqual(record['originals_removed']['records/INSTALL_LOG.jsonl'], sha(OTHER['records/INSTALL_LOG.jsonl']))
        self.assertEqual(record['proved_untouched']['source_data/POWERBALL_results_master.csv'],
                         sha(OTHER['source_data/POWERBALL_results_master.csv']))
        self.assertIsNotNone(record['finished'])

    def test_a_zip_of_the_project_folder_with_its_own_top_folder_serves_as_the_copy(self):
        archive = self.root / 'copy.zip'
        with zipfile.ZipFile(archive, 'w') as packed:
            for path, data in tree_bytes(self.copy).items():
                packed.writestr('project_folder/' + path, data)
        self.assertEqual(self.run_it('CONVERT', 'REMOVE', copy=archive), conversion.EXIT_DONE, self.text_said())


class ASecondRun(ConversionCase):
    """Standard section 7: the rule that makes a second run safe, and the watchpoint of EX_305."""

    def interrupt_at(self, count: int):
        """A checkpoint that lets `count` files be changed and then fails as Windows does when a file is open."""
        calls = []

        def checkpoint(path):
            calls.append(path)
            if len(calls) > count:
                raise PermissionError(13, 'The process cannot access the file', path)
        return checkpoint

    def test_a_finished_tree_run_again_changes_nothing_and_asks_nothing(self):
        self.run_it('CONVERT', 'REMOVE')
        after_first = tree_bytes(self.tree)
        self.said.clear()
        self.assertEqual(self.run_it(), conversion.EXIT_DONE, self.text_said())
        self.assertEqual(self.asker.questions, [])
        self.assertEqual(tree_bytes(self.tree), after_first)
        self.assertIn('Nothing is left to convert', self.text_said())

    def test_a_run_interrupted_part_way_is_simply_run_again_and_ends_as_an_uninterrupted_run_does(self):
        self.assertEqual(self.run_it('CONVERT', 'REMOVE', checkpoint=self.interrupt_at(3)), conversion.EXIT_STOPPED)
        self.assertIn('goes on from where it stopped', self.text_said())
        self.assertEqual((self.tree / 'src/a.py').read_bytes().count(b'\r\n')
                         + (self.tree / 'tests/test_a.py').read_bytes().count(b'\r\n') > 0, True)
        self.assertFalse((self.tree / conversion.JOB_LOCK).exists())
        self.assertEqual(self.run_it('CONVERT', 'REMOVE'), conversion.EXIT_DONE, self.text_said())
        interrupted = tree_bytes(self.tree)
        other = ConversionCase('run_it')
        other.setUp()
        self.addCleanup(other.doCleanups)
        other.run_it('CONVERT', 'REMOVE')
        self.assertEqual(interrupted, tree_bytes(other.tree))

    def test_on_a_second_run_the_copy_is_checked_against_the_first_runs_hashes_not_the_converted_files(self):
        self.run_it('CONVERT', 'REMOVE', checkpoint=self.interrupt_at(3))
        # A copy made NOW, from the half-converted tree, matches every live file but is not the way back.
        late_copy = self.root / 'late_copy'
        shutil.copytree(self.tree, late_copy)
        half_converted = tree_bytes(self.tree)
        self.said.clear()
        self.assertEqual(self.run_it('CONVERT', 'REMOVE', copy=late_copy), conversion.EXIT_STOPPED)
        self.assertIn('your copy holds other bytes', self.text_said())
        self.assertEqual(tree_bytes(self.tree), half_converted)
        self.assertEqual(self.asker.questions, [])
        self.assertEqual(self.run_it('CONVERT', 'REMOVE'), conversion.EXIT_DONE, self.text_said())

    def test_a_file_that_appeared_since_the_first_run_stops_the_second_before_anything_is_changed(self):
        self.run_it('CONVERT', 'REMOVE', checkpoint=self.interrupt_at(3))
        self.put('results/research/POWERBALL/reports/made_since.txt', b'not in the copy, not in the record\n')
        (self.copy / 'results/research/POWERBALL/reports/made_since.txt').write_bytes(b'not in the copy, not in the record\n')
        half_converted = tree_bytes(self.tree)
        self.said.clear()
        self.assertEqual(self.run_it('CONVERT', 'REMOVE'), conversion.EXIT_STOPPED)
        self.assertIn('were not there, or not to be changed, at the first run', self.text_said())
        self.assertEqual(tree_bytes(self.tree), half_converted)
        self.assertEqual(self.asker.questions, [])

    def test_a_removal_interrupted_part_way_is_finished_by_the_next_run(self):
        self.assertEqual(self.run_it('CONVERT', 'REMOVE', checkpoint=self.interrupt_at(9)), conversion.EXIT_STOPPED)
        self.assertTrue(any((self.tree / path).exists() for path in OTHER if path.startswith('results/research/')))
        self.assertEqual(self.run_it('REMOVE'), conversion.EXIT_DONE, self.text_said())
        self.assertFalse((self.tree / 'results/research').exists())

    def test_the_removal_not_confirmed_leaves_the_results_and_the_next_run_asks_only_for_it(self):
        self.assertEqual(self.run_it('CONVERT', 'no'), conversion.EXIT_NOT_CONFIRMED)
        self.assertTrue((self.tree / 'records/INSTALL_LOG.jsonl').is_file())
        self.assertEqual((self.tree / 'src/a.py').read_bytes(), b'x = 1\r\ny = 2\r\n')
        self.assertEqual(self.run_it('REMOVE'), conversion.EXIT_DONE, self.text_said())
        self.assertEqual(len(self.asker.questions), 1)

    def test_a_record_of_another_conversion_list_is_refused(self):
        self.run_it('CONVERT', 'REMOVE')
        document = json.loads(self.list_path.read_bytes())
        self.list_path.write_bytes(json.dumps(document, indent=2).encode('ascii'))
        self.said.clear()
        self.assertEqual(self.run_it(), conversion.EXIT_STOPPED)
        self.assertIn('of another tree or another conversion list', self.text_said())


class WhatStopsARunBeforeAnythingIsChanged(ConversionCase):
    """Standard section 7: each of these is named, and the tree is byte for byte as it was."""

    def assert_stops_unchanged(self, *expected_words, words=('CONVERT', 'REMOVE'), **options):
        """Run; assert that it stopped, said the expected words, asked nothing and changed no byte of the tree."""
        before = tree_bytes(self.tree)
        self.assertEqual(self.run_it(*words, **options), conversion.EXIT_STOPPED, self.text_said())
        for expected in expected_words:
            self.assertIn(expected, self.text_said())
        self.assertEqual(self.asker.questions, [])
        self.assertEqual(tree_bytes(self.tree), before)

    def test_a_listed_file_with_a_third_sha256(self):
        self.put('src/a.py', b'x = 1\ny = 3\n')
        self.assert_stops_unchanged('src/a.py: its SHA-256 is neither the list\'s "before" nor its "after"')

    def test_a_listed_file_that_is_missing(self):
        (self.tree / 'src/a.py').unlink()
        self.assert_stops_unchanged('src/a.py: on the conversion list but not in the tree')

    def test_the_packages_files_not_yet_copied_into_the_tree(self):
        self.put('deploy/file_form.py', b'# an older rule\n')
        self.assert_stops_unchanged("1 of the package's own files are not in this tree", "Copy the package's files")

    def test_a_file_the_package_delivers_that_is_missing_from_the_tree(self):
        (self.tree / 'deploy/file_form.py').unlink()
        self.assert_stops_unchanged("1 of the package's own files are not in this tree")

    def test_a_rule_beside_the_program_that_is_not_the_one_the_list_names(self):
        self.rule_path.write_bytes(b'# another rule\r\n')
        self.assert_stops_unchanged('is not the rule the conversion list expects')

    def test_a_text_file_that_is_in_no_class(self):
        self.put('src/my_notes.txt', b'something of mine\n')
        self.assert_stops_unchanged('src/my_notes.txt: a text file that is in no class')

    def test_a_file_of_a_kind_the_standard_does_not_name(self):
        self.put('scratch/thing.xml', b'<a/>\n')
        self.assert_stops_unchanged('scratch/thing.xml: a file of a kind the standard does not name')

    def test_a_status_file_that_holds_a_withdrawal(self):
        self.put('src/methods/E_901/TOY_A_V1/VARIANT_STATUS.ini', OLD_STATUS.replace(
            b'status = ACTIVE\n', b'status = WITHDRAWN\nwithdrawn_from_draw = 1601\n'))
        self.assert_stops_unchanged('VARIANT_STATUS.ini: it holds a status other than ACTIVE', 'your decision')
        for content in ('WITHDRAWN', '1601', 'withdrawn_from_draw'):
            self.assertNotIn(content, self.text_said())

    def test_a_status_file_that_holds_an_eligibility_draw(self):
        self.put('src/methods/E_901/TOY_A_V1/VARIANT_STATUS.ini', OLD_STATUS.replace(
            b'status = ACTIVE\n', b'status = ACTIVE\nprevailing_ov1_first_eligible_draw = 1596\n'))
        self.assert_stops_unchanged('VARIANT_STATUS.ini: it records a withdrawal or an eligibility draw')
        for content in ('1596', 'prevailing_ov1'):
            self.assertNotIn(content, self.text_said())

    def link(self, link: Path, target: Path) -> None:
        """Make a link to a folder; a junction where Windows allows no symbolic link. Skips the test where
        neither can be made."""
        remove = link.unlink
        try:
            os.symlink(target, link, target_is_directory=True)
        except (OSError, NotImplementedError):
            if os.name != 'nt':
                self.skipTest('this account cannot make a symbolic link here')
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
            remove = lambda: os.rmdir(link)                 # a junction is removed as a folder is
        # The link itself is removed before the temporary folder is, never what it points to.
        self.addCleanup(remove)

    def test_a_linked_folder_among_the_results_is_named_and_nothing_behind_it_is_read_or_removed(self):
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        (elsewhere / 'not_the_trees.txt').write_bytes(b'another place\n')
        self.link(self.tree / 'results/research/linked', elsewhere)
        self.assert_stops_unchanged('results/research/linked: a link, a junction or another reparse point')
        self.assertNotIn('not_the_trees.txt', self.text_said())
        self.assertEqual((elsewhere / 'not_the_trees.txt').read_bytes(), b'another place\n')

    def test_a_control_folder_that_is_a_link_stops_the_run_before_a_lock_is_written_through_it(self):
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        shutil.rmtree(self.tree / 'records')
        self.link(self.tree / 'records', elsewhere)
        self.assertEqual(self.run_it('CONVERT', 'REMOVE'), conversion.EXIT_STOPPED)
        self.assertIn('records is a link, a junction or another reparse point', self.text_said())
        self.assertEqual(list(elsewhere.iterdir()), [])
        self.assertEqual(self.asker.questions, [])

    def test_a_results_master_that_is_not_in_its_form_is_never_converted(self):
        self.put('source_data/POWERBALL_results_master.csv', b'Draw,Date\n1,2026-01-01\n')
        self.assert_stops_unchanged('POWERBALL_results_master.csv: must be CRLF', 'never converted')

    def test_a_settings_file_with_a_stray_carriage_return(self):
        self.put('ENVIRONMENT.ini', b'[tree]\rrole = DEV\n')
        self.assert_stops_unchanged('ENVIRONMENT.ini:', 'carriage return')

    def test_a_job_lock_left_by_another_job(self):
        self.put(conversion.JOB_LOCK, b'research job\n')
        self.assert_stops_unchanged('records/JOB.lock exists')

    def test_the_updaters_lock_left_by_an_update(self):
        self.put(conversion.UPDATER_LOCK, b'update\n')
        self.assert_stops_unchanged('.results_master.lock exists')
        self.assertFalse((self.tree / conversion.JOB_LOCK).exists())

    def test_a_copy_that_lacks_a_file_to_be_converted(self):
        (self.copy / 'src/a.py').unlink()
        self.assert_stops_unchanged('src/a.py: not in your copy')

    def test_a_copy_that_lacks_a_file_to_be_removed(self):
        (self.copy / 'records/INSTALL_LOG.jsonl').unlink()
        self.assert_stops_unchanged('records/INSTALL_LOG.jsonl: not in your copy')

    def test_a_copy_that_holds_other_bytes(self):
        (self.copy / 'ENVIRONMENT.ini').write_bytes(b'[tree]\nrole = QA\n')
        self.assert_stops_unchanged('ENVIRONMENT.ini: your copy holds other bytes')

    def test_a_copy_that_is_not_a_copy_of_the_project(self):
        self.assert_stops_unchanged('does not look like a copy of the project folder', copy=self.root)

    def test_a_list_that_is_not_a_conversion_list(self):
        self.list_path.write_bytes(b'{"kind": "SOMETHING_ELSE", "files": []}')
        self.assert_stops_unchanged('is not a conversion list')

    def test_the_word_not_typed(self):
        before = tree_bytes(self.tree)
        self.assertEqual(self.run_it('convert'), conversion.EXIT_NOT_CONFIRMED)
        self.assertEqual({path: data for path, data in tree_bytes(self.tree).items()}, before)

    def test_a_list_whose_after_hash_is_not_what_the_rule_gives_stops_at_that_file_untouched(self):
        document = json.loads(self.list_path.read_bytes())
        next(entry for entry in document['files'] if entry['path'] == 'src/a.py')['sha256_after'] = 'f' * 64
        self.list_path.write_bytes(json.dumps(document).encode('ascii'))
        self.assertEqual(self.run_it('CONVERT', 'REMOVE'), conversion.EXIT_STOPPED)
        self.assertIn('src/a.py: the converted bytes are not the ones the conversion list expects', self.text_said())
        self.assertEqual((self.tree / 'src/a.py').read_bytes(), LISTED['src/a.py'])


class ALookOnly(ConversionCase):
    """The look-only run reads and prints; it takes no lock, needs no copy and changes nothing."""

    def test_a_look_changes_no_byte_and_writes_no_record(self):
        before = tree_bytes(self.tree)
        code = conversion.run(self.tree, self.list_path, look_only=True, say=self.said.append,
                              rule_path=self.rule_path)
        self.assertEqual(code, conversion.EXIT_DONE, self.text_said())
        self.assertEqual(tree_bytes(self.tree), before)
        self.assertEqual(tree_bytes(self.rule_path.parent), {conversion.RULE_FILE_NAME: self.rule_path.read_bytes()})
        self.assertFalse(self.record_path.exists())
        self.assertIn('LOOKED ONLY; nothing was changed', self.said[-1])

    def test_a_look_before_the_packages_files_are_copied_says_so_and_is_not_stopped_by_it(self):
        (self.tree / 'deploy/file_form.py').unlink()
        before = tree_bytes(self.tree)
        code = conversion.run(self.tree, self.list_path, look_only=True, say=self.said.append,
                              rule_path=self.rule_path)
        self.assertEqual(code, conversion.EXIT_DONE, self.text_said())
        self.assertIn("THE PACKAGE'S OWN FILES, not yet here .. 1 file(s)", self.text_said())
        self.assertEqual(tree_bytes(self.tree), before)

    def test_a_look_reports_what_would_stop_a_real_run(self):
        self.put('src/my_notes.txt', b'mine\n')
        self.put(conversion.JOB_LOCK, b'research job\n')
        code = conversion.run(self.tree, self.list_path, look_only=True, say=self.said.append,
                              rule_path=self.rule_path)
        self.assertEqual(code, conversion.EXIT_STOPPED)
        self.assertIn('src/my_notes.txt', self.text_said())
        self.assertIn('records/JOB.lock: a lock file exists', self.text_said())
        self.assertIn('tell Claude', self.text_said())
        self.assertNotIn('by hand', self.text_said())


@unittest.skipUnless((REPOSITORY_SRC / 'research' / 'job_lock.py').is_file(), 'not run inside the repository')
class TheNamesSharedWithTheEngine(unittest.TestCase):
    """The program is standard library only, so it repeats four names of the engine; they must stay the same."""

    def test_the_locks_and_the_status_file_are_named_as_the_engine_names_them(self):
        sys.path.insert(0, str(REPOSITORY_SRC))
        sys.path.insert(0, str(REPOSITORY_SRC / 'methods'))
        from research import job_lock, status_file, variant_lists
        self.assertEqual(conversion.JOB_LOCK, f'{job_lock.RECORDS_FOLDER}/{job_lock.JOB_LOCK_NAME}')
        self.assertEqual(conversion.UPDATER_LOCK, job_lock.UPDATER_LOCK)
        self.assertEqual(conversion.STATUS_FILE_NAME, status_file.STATUS_FILE_NAME)
        self.assertEqual(conversion.METHODS_FOLDER, '/'.join(status_file.METHODS_PARTS) + '/')
        self.assertIn(variant_lists.RESEARCH_FOLDER + '/', conversion.REMOVED_FOLDERS)
        self.assertEqual(conversion.PLAIN_STATUS_LINE, f'status = {status_file.ACTIVE}')


if __name__ == '__main__':
    unittest.main()
