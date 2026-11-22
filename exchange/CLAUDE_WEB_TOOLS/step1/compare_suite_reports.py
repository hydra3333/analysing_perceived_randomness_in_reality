"""Compare two runs of the test suite, test by test: before the layout move and after it.

What this file is for
    It reads the ordinary `unittest -v` reports of two runs made by run_suite.py and says, for every test, whether
    its result is the same. A test that passed before and fails now, a test that has disappeared, a new test, and
    a test that failed both times (with each run's own failure line, so that the cause can be compared by eye)
    are listed. It is a workspace tool; it is not project code.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3, phase 1: "the existing suite".

Which of the project's own modules it uses
    None.

Usage:  python compare_suite_reports.py <report folder before> <report folder after>
Exit code 0 when no test changed its result, disappeared or appeared; 1 otherwise.
"""
import pathlib
import re
import sys

# One line of `unittest -v`: "test_name (module.Class.test_name) ... ok". A docstring line may sit between the
# name and the result; a sub-test adds text after the bracket.
RESULT_LINE = re.compile(r'^(\w+) \(([\w.]+)\)[^\n]*?(?:\n[^\n]*?)? \.\.\. (ok|FAIL|ERROR|skipped|expected failure)', re.M)

# In the failure section: "FAIL: test_name (module.Class.test_name) ..." down to the last line of its traceback.
FAILURE_BLOCK = re.compile(r'^(?:FAIL|ERROR): (\w+) \(([\w.]+)\)[^\n]*\n-+\n(.*?)(?=\n\n(?:=|-){20,}|\Z)', re.M | re.S)


def read_reports(folder: pathlib.Path) -> tuple:
    """Read one run's reports.

    folder: a report folder written by run_suite.py.
    Returns (results, causes): results is {test id: result}, for example
        {'test_e2r_prefix.PrefixTests.test_prefix': 'ok', ...}; causes is {test id: [last line of each failure
        of that test]}, for example {'test_x.C.test_y': ['AssertionError: 1 != 2']}.
    """
    results, causes = {}, {}
    for report in sorted(folder.glob('test_*.txt')):
        text = report.read_text(encoding='utf-8')
        for _name, test_id, result in RESULT_LINE.findall(text):
            results[test_id] = result
        for _name, test_id, traceback_text in FAILURE_BLOCK.findall(text):
            causes.setdefault(test_id, []).append(traceback_text.strip().splitlines()[-1][:200])
            results[test_id] = 'FAIL' if results.get(test_id) in (None, 'ok') else results[test_id]
    return results, causes


def main() -> int:
    """Print the comparison and return 0 only if no test changed its result, disappeared or appeared."""
    before, causes_before = read_reports(pathlib.Path(sys.argv[1]))
    after, causes_after = read_reports(pathlib.Path(sys.argv[2]))
    disappeared = sorted(set(before) - set(after))
    appeared = sorted(set(after) - set(before))
    changed = sorted(t for t in set(before) & set(after) if before[t] != after[t])
    failing_both = sorted(t for t in set(before) & set(after) if before[t] == after[t] and before[t] in ('FAIL', 'ERROR'))
    print(f'tests before: {len(before)}; after: {len(after)}; same result: {len(set(before) & set(after)) - len(changed)}')
    for title, tests in (('DISAPPEARED', disappeared), ('NEW', appeared)):
        for test_id in tests:
            print(f'{title}: {test_id}')
    for test_id in changed:
        print(f'CHANGED: {test_id}: {before[test_id]} -> {after[test_id]}')
    for test_id in failing_both:
        same_cause = causes_before.get(test_id) == causes_after.get(test_id)
        print(f'FAILS IN BOTH RUNS ({"same failure lines" if same_cause else "FAILURE LINES DIFFER"}): {test_id}')
        if not same_cause:
            print(f'    before: {causes_before.get(test_id)}\n    after:  {causes_after.get(test_id)}')
    different = bool(disappeared or appeared or changed)
    print('RESULT: ' + ('DIFFERENCES FOUND - each needs an explanation' if different
                        else 'no test changed its result, disappeared or appeared'))
    return 1 if different else 0


if __name__ == '__main__':
    sys.exit(main())
