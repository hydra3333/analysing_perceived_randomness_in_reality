"""Run the research system's test suite on a temporary copy of DEV's files, with the Python it is given.

What this file is for
    The tests live in DEV. An install asks whether they pass with the TARGET tree's own Python (a tree's creation,
    an infrastructure reinstall, and an ordinary install when the target's infrastructure is file for file
    DEV's). The tests must not run in DEV's own folder with a foreign Python, and nothing of them is ever put in
    a QA or PROD tree. So this file copies what the suite needs into a new temporary folder outside every tree,
    runs each listed test module there with the Python named, one module a process, and says what each did. The
    folder is removed when every module passed, and is left and named when one did not, with each module's own
    output in it.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 12.3 item 3;
    doc/Predictive_Randomness_Deployment_Design_v0_12.md sections 3.3 (item 5), 4 (step 7), 6 (steps 3 and 9) and
    17 ("the code round lists exactly what the suite needs").

Which of the project's own modules it uses
    file_form (deploy/file_form.py): files_under, the project's one walk of its own files.

What uses it
    The install tools in DEV (deploy/), and the tests. It is standard library only and starts only the Python it
    is given, on the copy it made.
"""
from __future__ import annotations

import configparser
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import file_form

# The list of the suite's test modules, from DEV's root.
SUITE_LIST = 'deploy/SUITE_MANIFEST.ini'
TESTS_SECTION = 'tests'
# What the temporary copy holds: these folders whole, and the files lying directly in the root.
COPIED_FOLDERS = ('src', 'deploy', 'tests')
# Root files that are never copied: the settings file holds this PC's paths, and no tool writes one.
NEVER_COPIED = ('ENVIRONMENT.ini',)
# The folders of the copy that Python imports the tests and the code from.
SEARCH_PATH_FOLDERS = ('src', 'src/methods', 'tests')
# The folder of the copy that holds each module's own output.
REPORTS_FOLDER = 'SUITE_REPORTS'
# The start of the temporary folder's name.
FOLDER_PREFIX = 'a_p_r_i_r_suite_'


class SuiteRefused(ValueError):
    """The suite cannot be run at all. The message says what was found and what to do. No test was started."""


@dataclass
class SuiteResult:
    """What a run of the suite found.

    passed: True only if every listed module ran at least one test and ended with exit code 0.
    modules: [(module, exit code, tests run)] in the order run.
    folder: None when the copy was removed (every module passed); otherwise the folder left behind.
    """
    passed: bool
    modules: list = field(default_factory=list)
    folder: Path | None = None

    def line(self) -> str:
        """One line for the owner; for example 'THE TEST SUITE PASSED: 19 modules, 569 tests.' or 'THE TEST SUITE
        FAILED: 2 of 19 modules (test_research_job, test_trees_snapshot). Each module's output is in C:\\...'."""
        tests = sum(ran for _, _, ran in self.modules)
        if self.passed:
            return f'THE TEST SUITE PASSED: {len(self.modules)} modules, {tests} tests.'
        failed = [module for module, exit_code, ran in self.modules if exit_code != 0 or ran == 0]
        return (f'THE TEST SUITE FAILED: {len(failed)} of {len(self.modules)} modules ({", ".join(failed)}). Each '
                f'module\'s output is in {self.folder / REPORTS_FOLDER}.')


def read_suite_list(dev_root: Path) -> tuple:
    """Read the names of the suite's test modules from DEV's list.

    dev_root: DEV's folder.  Returns the names in the list's order, for example ('test_file_form', ...).
    Refuses (SuiteRefused): no list; a file Python's INI reader rejects (a name given twice among them); no
    [tests] section or an empty one; a name with a value or a path in it; a name with no file under tests/.
    """
    path = Path(dev_root) / SUITE_LIST
    parser = configparser.ConfigParser(allow_no_value=True, delimiters=('=',), interpolation=None)
    parser.optionxform = str
    try:
        with open(path, 'r', encoding='ascii', newline='') as stream:
            parser.read_file(stream)
    except (OSError, UnicodeError, configparser.Error) as fault:
        raise SuiteRefused(f'{path}: the list of the suite\'s tests is missing or cannot be read ({fault}). It '
                           f'arrives with the install tools; nothing was run.') from None
    if not parser.has_section(TESTS_SECTION) or not parser.options(TESTS_SECTION):
        raise SuiteRefused(f'{path}: the list has no [{TESTS_SECTION}] section, or it names no test. Nothing was run.')
    names = tuple(parser.options(TESTS_SECTION))
    for name in names:
        if parser.get(TESTS_SECTION, name) is not None or not re.fullmatch(r'test_[A-Za-z0-9_]+', name):
            raise SuiteRefused(f'{path} [{TESTS_SECTION}]: "{name}" is not the plain name of a test module (for '
                               f'example test_research_job). Nothing was run.')
        if not (Path(dev_root) / 'tests' / f'{name}.py').is_file():
            raise SuiteRefused(f'{path} [{TESTS_SECTION}]: {name} is listed, but tests/{name}.py does not exist in '
                               f'{dev_root}. Nothing was run.')
    return names


def copy_project(dev_root: Path, folder: Path) -> int:
    """Copy what the suite needs from DEV into an empty folder: every file under src/, deploy/ and tests/, and
    every file lying directly in DEV's root except the settings file.

    dev_root: DEV's folder, which is only read.  folder: the new, empty folder.  Returns how many files were
    copied. Refuses (file_form.FileFormRefused) if the walk meets a link: nothing behind a link is read.
    """
    copied = 0
    for relative in file_form.files_under(dev_root, COPIED_FOLDERS, with_root_files=True):
        if relative in NEVER_COPIED:
            continue
        target = Path(folder) / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(dev_root) / relative, target)
        copied += 1
    return copied


def tests_run(output: bytes) -> int:
    """How many tests a module's output says it ran: the number in unittest's own line 'Ran 48 tests in 61.2s';
    0 if there is no such line."""
    found = re.findall(rb'^Ran (\d+) tests? in ', output, re.M)
    return int(found[-1]) if found else 0


def run_suite(dev_root: Path, python: Path, say=print, parent: Path | None = None) -> SuiteResult:
    """Run the suite on a temporary copy of DEV's files with the Python named.

    dev_root: DEV's folder.  python: the program to run the tests with, for example
    Path('G:/a_p_r_i_r/.venv/Scripts/python.exe').  say: prints one line a module.
    parent: the folder the temporary folder is made in; None for the PC's own temporary folder.
    No time limit is put on a module: a limit would end the process, and no program of this project ends one.
    Returns a SuiteResult. Refuses (SuiteRefused) what read_suite_list refuses, and a Python that is not a file.
    """
    names = read_suite_list(dev_root)
    if not Path(python).is_file():
        raise SuiteRefused(f'{python}: the Python to run the tests with was not found. Nothing was run.')
    folder = Path(tempfile.mkdtemp(prefix=FOLDER_PREFIX, dir=parent)).resolve()
    copied = copy_project(dev_root, folder)
    reports = folder / REPORTS_FOLDER
    reports.mkdir()
    say(f'The test suite: {len(names)} modules, run with {python} on a copy of {copied} files in {folder}. It takes '
        f'several minutes.')
    environment = dict(os.environ, PYTHONPATH=os.pathsep.join(str(folder / part) for part in SEARCH_PATH_FOLDERS))
    result = SuiteResult(passed=True, folder=folder)
    for name in names:
        report = reports / f'{name}.txt'
        with open(report, 'wb') as output:
            ended = subprocess.run([str(python), '-B', '-m', 'unittest', name], cwd=folder, env=environment,
                                   stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT,
                                   check=False).returncode
        ran = tests_run(report.read_bytes())
        result.modules.append((name, ended, ran))
        good = ended == 0 and ran > 0
        result.passed = result.passed and good
        say(f'  suite: {name}: {ran} tests, ' + ('OK' if good else f'FAILED (exit code {ended}); see {report}'))
    if result.passed:
        shutil.rmtree(folder)
        result.folder = None
    return result
