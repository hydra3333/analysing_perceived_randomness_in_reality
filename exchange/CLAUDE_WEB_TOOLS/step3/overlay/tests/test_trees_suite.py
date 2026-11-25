"""Tests of deploy/suite_on_copy.py: the suite run on a temporary copy with the Python it is given (build step 3,
slice C, part C2).

What this file is for
    It shows that the list of the suite's tests is read strictly; that the copy holds what the project's own walk
    finds and never the settings file, and that DEV is only read; that every listed module is run with the
    Python named, in the copy and not in DEV; that one failing module, or one that ran no test, fails the suite
    and leaves the copy with its reports, and that a passing suite leaves nothing; and that the real list names
    every test module of the new system that exists. The suites run here are invented and tiny.

Which of the project's own modules it uses
    deploy/suite_on_copy.py and deploy/file_form.py.
"""
from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import file_form                                             # noqa: E402  (after the path line above)
import suite_on_copy                                         # noqa: E402

PASSING = ('import unittest\n\n\nclass T(unittest.TestCase):\n    def test_one(self):\n        self.assertTrue(True)\n'
           '\n    def test_two(self):\n        self.assertTrue(True)\n')
FAILING = 'import unittest\n\n\nclass T(unittest.TestCase):\n    def test_one(self):\n        self.fail("invented")\n'
# A module that ends its process with exit code 0 before any test is run.
SILENT = 'import sys\nsys.exit(0)\n'
# A test that writes down where it ran, which Python ran it, and whether it could import the copy's own code.
TELLING = ('import os\nimport sys\nimport unittest\nimport toy_code\nimport toy_method\nimport toy_fixture\n\n\n'
           'class T(unittest.TestCase):\n    def test_one(self):\n'
           '        with open(os.environ["TOLD"], "w", encoding="utf-8", newline="\\n") as stream:\n'
           '            stream.write("|".join([os.getcwd(), sys.executable, toy_code.__file__, '
           'str(sys.dont_write_bytecode)]))\n')


def whole_tree(tree: Path) -> dict:
    """Every file of a folder with the SHA-256 of its bytes."""
    return {path.relative_to(tree).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(tree.rglob('*')) if path.is_file()}


class SuiteCase(unittest.TestCase):
    """An invented DEV tree with a tiny suite of its own, and a folder for the temporary copies."""

    def setUp(self):
        """Make the invented DEV."""
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name).resolve()
        self.dev, self.copies = self.root / 'dev', self.root / 'copies'
        self.copies.mkdir()
        for relative, text in (('src/toy_code.py', 'VALUE = 1\n'), ('src/methods/toy_method.py', 'VALUE = 2\n'),
                               ('tests/toy_fixture.py', 'VALUE = 3\n'), ('deploy/toy_tool.py', 'VALUE = 4\n'),
                               ('README.txt', 'an invented project\n'), ('ENVIRONMENT.ini', '[environment]\n'),
                               ('doc/not_needed.md', 'never copied\n'), ('source_data/results.csv', 'never copied\n')):
            (self.dev / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.dev / relative).write_text(text, encoding='ascii')
        self.suite(test_toy_pass=PASSING)

    def tearDown(self):
        """Remove everything."""
        self._temporary.cleanup()

    def suite(self, listed=None, **modules) -> None:
        """Give the invented DEV its test modules and its list (`listed`, or every module given)."""
        for name, text in modules.items():
            (self.dev / 'tests' / f'{name}.py').write_text(text, encoding='ascii')
        lines = '# an invented list\n[tests]\n' + ''.join(f'{name}\n' for name in (listed or modules))
        (self.dev / suite_on_copy.SUITE_LIST).write_text(lines, encoding='ascii')

    def run_suite(self, python: Path | None = None) -> tuple:
        """Run the invented suite; return (the result, the lines said)."""
        said = []
        result = suite_on_copy.run_suite(self.dev, python or Path(sys.executable), say=said.append,
                                         parent=self.copies)
        return result, said


class TheListOfTheSuitesTests(SuiteCase):
    """Deployment design section 17: the list sits beside the infrastructure manifest and is read strictly."""

    def refused(self, pattern: str) -> None:
        """Expect the list to be refused, and no copy to have been made."""
        with self.assertRaisesRegex(suite_on_copy.SuiteRefused, pattern):
            self.run_suite()
        self.assertEqual(list(self.copies.iterdir()), [])

    def test_the_names_are_read_in_the_lists_order(self):
        self.suite(listed=('test_toy_b', 'test_toy_a'), test_toy_a=PASSING, test_toy_b=PASSING)
        self.assertEqual(suite_on_copy.read_suite_list(self.dev), ('test_toy_b', 'test_toy_a'))

    def test_a_missing_list_is_refused(self):
        (self.dev / suite_on_copy.SUITE_LIST).unlink()
        self.refused('the list of the suite\'s tests is missing or cannot be read')

    def test_a_name_given_twice_is_refused(self):
        self.suite(listed=('test_toy_pass', 'test_toy_pass'))
        self.refused('missing or cannot be read')

    def test_a_list_that_names_no_test_is_refused(self):
        (self.dev / suite_on_copy.SUITE_LIST).write_text('[tests]\n', encoding='ascii')
        self.refused(r'no \[tests\] section, or it names no test')

    def test_a_module_that_does_not_exist_is_refused(self):
        self.suite(listed=('test_toy_pass', 'test_not_there'))
        self.refused(r'test_not_there is listed, but tests/test_not_there.py does not exist')

    def test_a_path_or_a_value_in_place_of_a_name_is_refused(self):
        for line in ('../test_toy_pass', 'test_toy_pass = yes', 'toy_fixture'):
            (self.dev / suite_on_copy.SUITE_LIST).write_text(f'[tests]\n{line}\n', encoding='ascii')
            self.refused('is not the plain name of a test module')

    def test_the_real_list_names_every_test_module_of_the_new_system_and_nothing_that_is_not_there(self):
        listed = suite_on_copy.read_suite_list(REPOSITORY_ROOT)
        new_system = sorted(path.stem for path in (REPOSITORY_ROOT / 'tests').glob('test_*.py')
                            if path.stem.startswith(('test_research_', 'test_trees_')) or path.stem == 'test_file_form')
        self.assertEqual(sorted(listed), new_system)
        self.assertIn('test_trees_suite', listed, 'this module is itself part of the suite')


class TheTemporaryCopy(SuiteCase):
    """What the copy holds, and that DEV is only read."""

    def test_it_holds_what_the_projects_own_walk_finds_except_the_settings_file(self):
        target = self.root / 'copy'
        target.mkdir()
        before = whole_tree(self.dev)
        copied = suite_on_copy.copy_project(self.dev, target)
        walked = file_form.files_under(self.dev, suite_on_copy.COPIED_FOLDERS, with_root_files=True)
        self.assertEqual(sorted(whole_tree(target)), sorted(set(walked) - {'ENVIRONMENT.ini'}))
        self.assertEqual(copied, len(walked) - 1)
        self.assertEqual({path: digest for path, digest in before.items() if path in whole_tree(target)},
                         whole_tree(target), 'each file is copied byte for byte')
        for never in ('ENVIRONMENT.ini', 'doc/not_needed.md', 'source_data/results.csv'):
            self.assertFalse((target / never).exists(), never)
        self.assertEqual(whole_tree(self.dev), before, 'DEV is only read')

    def test_a_link_in_dev_refuses_and_nothing_behind_it_is_copied(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'secret.py').write_text('SECRET = 1\n', encoding='ascii')
        try:
            os.symlink(outside, self.dev / 'src' / 'linked', target_is_directory=True)
        except OSError as refusal:
            self.skipTest(f'this account may not make a link ({refusal})')
        with self.assertRaises(file_form.FileFormRefused):
            self.run_suite()


class TheSuiteIsRunOnTheCopyWithThePythonNamed(SuiteCase):
    """Specification 12.3 item 3: "with the target's Python on a temporary copy"."""

    def test_a_passing_suite_passes_says_each_module_and_leaves_nothing_behind(self):
        self.suite(test_toy_a=PASSING, test_toy_b=PASSING)
        before = whole_tree(self.dev)
        result, said = self.run_suite()
        self.assertTrue(result.passed)
        self.assertEqual(result.modules, [('test_toy_a', 0, 2), ('test_toy_b', 0, 2)])
        self.assertIsNone(result.folder)
        self.assertEqual(result.line(), 'THE TEST SUITE PASSED: 2 modules, 4 tests.')
        self.assertEqual(said[1:], ['  suite: test_toy_a: 2 tests, OK', '  suite: test_toy_b: 2 tests, OK'])
        self.assertEqual(list(self.copies.iterdir()), [], 'the copy is removed')
        self.assertEqual(whole_tree(self.dev), before, 'nothing is written in DEV, not even a cache')

    def test_each_module_runs_in_the_copy_with_the_python_named_and_imports_the_copys_own_code(self):
        self.suite(test_toy_tell=TELLING)
        told = self.root / 'told.txt'
        os.environ['TOLD'] = str(told)
        try:
            result, _ = self.run_suite()
        finally:
            del os.environ['TOLD']
        self.assertTrue(result.passed)
        where, python, code, no_cache = told.read_text(encoding='utf-8').split('|')
        self.assertEqual(Path(where).parent, self.copies, 'it ran in the copy, not in DEV')
        self.assertEqual(os.path.normpath(python), os.path.normpath(sys.executable))
        self.assertEqual(Path(code).parent.parent, Path(where), 'and imported the copy\'s code')
        self.assertEqual(no_cache, 'True')

    def test_one_failing_module_fails_the_suite_and_the_copy_is_left_with_every_modules_output(self):
        self.suite(test_toy_a=PASSING, test_toy_bad=FAILING, test_toy_c=PASSING)
        result, said = self.run_suite()
        self.assertFalse(result.passed)
        self.assertEqual([(name, code != 0) for name, code, _ in result.modules],
                         [('test_toy_a', False), ('test_toy_bad', True), ('test_toy_c', False)],
                         'the modules after a failure are still run')
        (folder,) = self.copies.iterdir()
        self.assertEqual(result.folder, folder)
        self.assertIn(b'AssertionError: invented', (folder / 'SUITE_REPORTS' / 'test_toy_bad.txt').read_bytes())
        self.assertTrue((folder / 'SUITE_REPORTS' / 'test_toy_c.txt').is_file())
        self.assertEqual(result.line(), f'THE TEST SUITE FAILED: 1 of 3 modules (test_toy_bad). Each module\'s output '
                                        f'is in {folder / "SUITE_REPORTS"}.')
        self.assertIn('  suite: test_toy_bad: 1 tests, FAILED (exit code 1); see ', said[2])

    def test_a_module_that_ran_no_test_fails_the_suite(self):
        self.suite(test_toy_a=PASSING, test_toy_silent=SILENT)
        result, said = self.run_suite()
        self.assertEqual(result.modules[1], ('test_toy_silent', 0, 0), 'it ended with exit code 0 and ran nothing')
        self.assertFalse(result.passed)
        self.assertIn('(test_toy_silent)', result.line())

    def test_a_python_that_is_not_there_is_refused_before_any_copy_is_made(self):
        with self.assertRaisesRegex(suite_on_copy.SuiteRefused, 'the Python to run the tests with was not found'):
            self.run_suite(python=self.root / 'no_python.exe')
        self.assertEqual(list(self.copies.iterdir()), [])

    def test_the_number_of_tests_is_read_from_unittests_own_line(self):
        self.assertEqual(suite_on_copy.tests_run(b'..\r\n-----\r\nRan 48 tests in 61.204s\r\n\r\nOK\r\n'), 48)
        self.assertEqual(suite_on_copy.tests_run(b'Ran 1 test in 0.001s\n\nOK\n'), 1)
        self.assertEqual(suite_on_copy.tests_run(b'ImportError: no module\n'), 0)


if __name__ == '__main__':
    unittest.main()
