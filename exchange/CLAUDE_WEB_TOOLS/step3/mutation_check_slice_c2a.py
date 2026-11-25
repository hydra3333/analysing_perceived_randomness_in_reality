"""Workspace helper (not project code): the planted faults for slice C part C2, first piece (deploy/suite_on_copy.py,
the suite run on a temporary copy). One fault at a time in a disposable copy of the dev tree that holds the overlay;
tests/test_trees_suite.py must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_suite']
S = 'deploy/suite_on_copy.py'
FAULTS = [
 (S, "        if relative in NEVER_COPIED:", "        if False:", 'the settings file is copied'),
 (S, "COPIED_FOLDERS = ('src', 'deploy', 'tests')", "COPIED_FOLDERS = ('src', 'deploy', 'tests', 'doc')", 'a folder the suite does not need is copied'),
 (S, "file_form.files_under(dev_root, COPIED_FOLDERS, with_root_files=True)", "file_form.files_under(dev_root, COPIED_FOLDERS, with_root_files=False)", 'the root files are not copied'),
 (S, "        if parser.get(TESTS_SECTION, name) is not None or not re.fullmatch(r'test_[A-Za-z0-9_]+', name):", "        if False:", 'a path or a value in place of a name is accepted'),
 (S, "        if not (Path(dev_root) / 'tests' / f'{name}.py').is_file():", "        if False:", 'a listed module that does not exist is accepted'),
 (S, "    if not parser.has_section(TESTS_SECTION) or not parser.options(TESTS_SECTION):", "    if not parser.has_section(TESTS_SECTION):", 'a list that names no test is accepted'),
 (S, "    if not Path(python).is_file():", "    if False:", 'a Python that is not there is not refused before the copy'),
 (S, "[str(python), '-B', '-m', 'unittest', name], cwd=folder,", "[str(python), '-B', '-m', 'unittest', name], cwd=dev_root,", 'the tests run in DEV, not in the copy'),
 (S, "[str(python), '-B', '-m', 'unittest', name]", "[str(python), '-m', 'unittest', name]", 'the tests may write cache files'),
 (S, "PYTHONPATH=os.pathsep.join(str(folder / part) for part in SEARCH_PATH_FOLDERS)", "PYTHONPATH=os.pathsep.join(str(Path(dev_root) / part) for part in SEARCH_PATH_FOLDERS)", 'the tests import DEV\'s code, not the copy\'s'),
 (S, "        good = ended == 0 and ran > 0", "        good = ended == 0", 'a module that ran no test passes'),
 (S, "        good = ended == 0 and ran > 0", "        good = ran > 0", 'a failing module passes'),
 (S, "        result.passed = result.passed and good", "        result.passed = good", 'only the last module decides'),
 (S, "    if result.passed:\r\n        shutil.rmtree(folder)", "    if True:\r\n        shutil.rmtree(folder)", 'the copy of a failed suite is removed'),
 (S, "        shutil.rmtree(folder)\r\n        result.folder = None", "        result.folder = None", 'the copy of a passed suite is left behind'),
 (S, "    return int(found[-1]) if found else 0", "    return int(found[-1]) if found else 1", 'output without a count is taken for one test'),
 (S, "    names = tuple(parser.options(TESTS_SECTION))", "    names = tuple(sorted(parser.options(TESTS_SECTION)))", 'the list\'s order is not kept'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', *MODULES], cwd=MUT, timeout=300,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught, how = run.returncode != 0, 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what, flush=True)
print(f'{len(FAULTS)} faults planted; {survived} survived')
