"""Run the project's existing test suite, one test module per process, and keep the ordinary reports.

What this file is for
    Build step 1 needs one run of the existing suite before the layout move and the same run after it, so that
    the two can be compared test by test. This is a workspace tool for Claude's cloud workspace; it is not
    project code and nothing imports it. It runs every test module, the worker-process test E2R-T12 included.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3, phase 1: "the existing suite".

Which of the project's own modules it uses
    None. It starts `python -B -m unittest -v <module>` for each tests/test_*.py of the tree it is given.

Usage:  python run_suite.py <tree root> <report folder>
        (the tests run with the same Python that runs this file)
Writes: <report folder>/<module>.txt (the unittest -v output of each module) and <report folder>/MODULES.txt
        (the one line per module that is also printed).
"""
import os
import pathlib
import re
import subprocess
import sys

# One module may take this long before it is reported as TIMEOUT. The whole suite takes about ten minutes
# in the cloud workspace; the limit is generous so that a slow module is never cut short.
PER_MODULE_TIMEOUT_SECONDS = 3600

# The folders of the tree that must be on Python's search path for the tests (H-1 v8 section 12.3).
SEARCH_PATH_FOLDERS = ('src', 'src/methods', 'tests')


def main() -> int:
    """Run every test module of the tree and return 0 (the modules' own results are in the reports)."""
    tree, reports = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    python = sys.executable
    reports.mkdir(parents=True, exist_ok=True)
    module_lines = []
    environment = dict(os.environ, PYTHONPATH=os.pathsep.join(str(tree / folder) for folder in SEARCH_PATH_FOLDERS))
    for test_file in sorted((tree / 'tests').glob('test_*.py')):
        module = test_file.stem
        try:
            finished = subprocess.run([python, '-B', '-m', 'unittest', '-v', module], cwd=tree, env=environment,
                                      capture_output=True, text=True, timeout=PER_MODULE_TIMEOUT_SECONDS)
            output, exit_code = finished.stderr + finished.stdout, finished.returncode
        except subprocess.TimeoutExpired:
            output, exit_code = 'TIMEOUT', -1
        (reports / f'{module}.txt').write_text(output, encoding='utf-8')
        ran = re.search(r'^Ran (\d+) tests?', output, re.M)
        verdict = re.search(r'^(OK|FAILED)[^\n]*$', output, re.M)
        module_lines.append(f'{module}\texit={exit_code}\tran={ran.group(1) if ran else "?"}\t'
                            f'{verdict.group(0) if verdict else "?"}')
        print(module_lines[-1], flush=True)
    total = sum(int(line.split('ran=')[1].split('\t')[0]) for line in module_lines if 'ran=?' not in line)
    module_lines.append(f'DONE: {len(module_lines)} modules, {total} tests ran')
    print(module_lines[-1], flush=True)
    (reports / 'MODULES.txt').write_text('\n'.join(module_lines) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
