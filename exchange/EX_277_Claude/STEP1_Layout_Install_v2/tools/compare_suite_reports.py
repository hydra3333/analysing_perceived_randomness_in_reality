"""Compare two runs of the test suite, module by module and test by test: before the layout move and after it.

What this file is for
    It reads the ordinary `unittest -v` reports of two runs made by run_suite.py and says whether anything
    changed. It compares, for every module, the number of tests unittest says it ran and unittest's own verdict
    line; and, for every test, its result. It lists a test that passed before and fails now, a test that has
    disappeared, a new test, and a test that fails in both runs (with how many failures each run reports for it,
    and each run's failure lines where they differ, so that the cause can be compared by eye). It refuses to say
    "nothing changed" unless it has identified every test that unittest says ran. It is a workspace tool; it is
    not project code.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3, phase 1: "the existing suite".

Which of the project's own modules it uses
    None.

Usage:  python compare_suite_reports.py <report folder before> <report folder after>
Exit code 0 only when every test of both runs was identified and no module or test differs; 1 otherwise.
"""
import pathlib
import re
import sys

# A test's first line in `unittest -v`: "test_name (module.Class.test_name)" at the start of a line. Whatever the
# test prints, a docstring line, and the lines of its sub-tests (which are indented) follow until the next test.
TEST_START = re.compile(r'^(\w+) \(([\w.]+)\)', re.M)

# The end of a test's own text: its result word, either after " ... " or alone on a line when the test printed
# something in between.
RESULT_WORD = re.compile(r'(?:\.\.\. |^)(ok|FAIL|ERROR|skipped .*|expected failure|unexpected success)$', re.M)

# The progress part of a report ends at the first ruled line (a row of = or -), where the failures or the summary begin.
PROGRESS_END = re.compile(r'^(?:={60,}|-{60,})$', re.M)

# unittest's two summary lines: how many tests ran, and its verdict ("OK", "OK (skipped=1)", "FAILED (failures=7)").
RAN_LINE = re.compile(r'^Ran (\d+) tests? in', re.M)
VERDICT_LINE = re.compile(r'^(OK|FAILED)(?: \(([^)]*)\))?$', re.M)

# In the failure section: "FAIL: test_name (module.Class.test_name) ..." and its traceback, down to the next ruled line.
FAILURE_BLOCK = re.compile(r'^(?:FAIL|ERROR): (\w+) \(([\w.]+)\)[^\n]*\n-+\n(.*?)(?=\n\n(?:=|-){20,}|\Z)', re.M | re.S)

# How much of a failure's last line is shown.
FAILURE_LINE_WIDTH = 200


def read_reports(folder: pathlib.Path) -> dict:
    """Read one run's reports.

    folder: a report folder written by run_suite.py (one <module>.txt for each test module).
    Returns {module: {'ran': count or None, 'verdict': text or None, 'results': {test id: result word},
                      'causes': {test id: [last line of each of its failures]}}}, for example
        {'test_e2r_prefix': {'ran': 1, 'verdict': 'OK', 'results': {'test_e2r_prefix.T.test_prefix': 'ok'},
                             'causes': {}}, ...}.
    A sub-test's failure belongs to its test: the test's result is then FAIL or ERROR.
    """
    modules = {}
    for report in sorted(folder.glob('test_*.txt')):
        text = report.read_text(encoding='utf-8')
        ran = RAN_LINE.search(text)
        verdicts = VERDICT_LINE.findall(text)
        progress_end = PROGRESS_END.search(text)
        progress = text[:progress_end.start()] if progress_end else text
        starts = list(TEST_START.finditer(progress))
        results = {}
        for position, start in enumerate(starts):
            end = starts[position + 1].start() if position + 1 < len(starts) else len(progress)
            words = RESULT_WORD.findall(progress[start.start():end])
            if any(word in ('FAIL', 'ERROR') for word in words):
                result = 'ERROR' if 'ERROR' in words else 'FAIL'
            else:
                result = words[-1].split(' ')[0] if words else 'NO RESULT FOUND'
            results[start.group(2)] = result
        causes = {}
        for _name, test_id, traceback_text in FAILURE_BLOCK.findall(text):
            causes.setdefault(test_id, []).append(traceback_text.strip().splitlines()[-1][:FAILURE_LINE_WIDTH])
        modules[report.stem] = {'ran': int(ran.group(1)) if ran else None,
                                'verdict': (verdicts[-1][0] + (f' ({verdicts[-1][1]})' if verdicts[-1][1] else ''))
                                if verdicts else None,
                                'results': results, 'causes': causes}
    return modules


def main() -> int:
    """Print the comparison and return 0 only if every test was identified and nothing differs."""
    before = read_reports(pathlib.Path(sys.argv[1]))
    after = read_reports(pathlib.Path(sys.argv[2]))
    problems = 0

    # 1. Every module of both runs: was every test identified, and do unittest's own two summary lines agree?
    for name, run in (('before', before), ('after', after)):
        ran_total = sum(m['ran'] or 0 for m in run.values())
        identified = sum(len(m['results']) for m in run.values())
        print(f'{name}: {len(run)} modules; unittest ran {ran_total} tests; identified here: {identified}')
        for module, m in run.items():
            if m['ran'] is None or m['verdict'] is None:
                print(f'NO SUMMARY ({name}): {module}: its report has no "Ran N tests" or verdict line')
                problems += 1
            elif len(m['results']) != m['ran'] or 'NO RESULT FOUND' in m['results'].values():
                print(f'NOT ALL TESTS IDENTIFIED ({name}): {module}: unittest ran {m["ran"]}, identified '
                      f'{len(m["results"])}; so this comparison cannot vouch for that module')
                problems += 1
    for module in sorted(set(before) | set(after)):
        if module not in before or module not in after:
            print(f'MODULE {"DISAPPEARED" if module in before else "NEW"}: {module}')
            problems += 1
        elif (before[module]['ran'], before[module]['verdict']) != (after[module]['ran'], after[module]['verdict']):
            print(f'MODULE CHANGED: {module}: ran {before[module]["ran"]}, {before[module]["verdict"]} -> '
                  f'ran {after[module]["ran"]}, {after[module]["verdict"]}')
            problems += 1

    # 2. Every test.
    results_before = {t: r for m in before.values() for t, r in m['results'].items()}
    results_after = {t: r for m in after.values() for t, r in m['results'].items()}
    causes_before = {t: c for m in before.values() for t, c in m['causes'].items()}
    causes_after = {t: c for m in after.values() for t, c in m['causes'].items()}
    for test_id in sorted(set(results_before) - set(results_after)):
        print(f'DISAPPEARED: {test_id}')
        problems += 1
    for test_id in sorted(set(results_after) - set(results_before)):
        print(f'NEW: {test_id}')
        problems += 1
    common = sorted(set(results_before) & set(results_after))
    same = 0
    for test_id in common:
        if results_before[test_id] != results_after[test_id]:
            print(f'CHANGED: {test_id}: {results_before[test_id]} -> {results_after[test_id]}')
            problems += 1
        else:
            same += 1
    print(f'tests in both runs: {len(common)}; with the same result: {same}')
    for test_id in common:
        if results_before[test_id] == results_after[test_id] and results_before[test_id] in ('FAIL', 'ERROR'):
            lines_before, lines_after = causes_before.get(test_id, []), causes_after.get(test_id, [])
            if len(lines_before) != len(lines_after):
                print(f'CHANGED: {test_id}: fails in both runs, but with {len(lines_before)} failure(s) before and '
                      f'{len(lines_after)} after')
                problems += 1
            elif lines_before == lines_after:
                print(f'FAILS IN BOTH RUNS ({len(lines_before)} failure(s), the same failure lines): {test_id}')
            else:
                print(f'FAILS IN BOTH RUNS ({len(lines_before)} failure(s); FAILURE LINES DIFFER, compare by eye): {test_id}')
                print(f'    before: {lines_before}\n    after:  {lines_after}')
    print('RESULT: ' + ('DIFFERENCES FOUND - each needs an explanation' if problems else
                        'every test that ran was identified; no module and no test changed its result, '
                        'disappeared or appeared'))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
