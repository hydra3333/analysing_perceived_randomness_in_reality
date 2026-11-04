"""Run every test module under tests/ (discovery), leaving out T12Determinism; print per-module counts and the total.
Usage: python -B run_all_but_t12.py <repo>"""
import sys, unittest
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
for p in ('src', 'src/methods', 'tests'):
    sys.path.insert(0, str(repo / p))
import os; os.chdir(repo)
loader = unittest.TestLoader()
suite = loader.discover('tests', pattern='test_*.py', top_level_dir=str(repo))
def flatten(s):
    for t in s:
        if isinstance(t, unittest.TestSuite):
            yield from flatten(t)
        else:
            yield t
tests = [t for t in flatten(suite) if type(t).__name__ != 'T12Determinism']
bad = [t for t in tests if 'ModuleImportFailure' in type(t).__name__ or '_FailedTest' in type(t).__name__]
counts = {}
for t in tests:
    counts[type(t).__module__] = counts.get(type(t).__module__, 0) + 1
for m in sorted(counts):
    print(f'{counts[m]:4d}  {m}')
print('modules', len(counts), 'tests', len(tests), 'load failures', len(bad))
r = unittest.TextTestRunner(verbosity=1, stream=sys.stdout).run(unittest.TestSuite(tests))
print('RESULT', 'PASS' if r.wasSuccessful() else 'STOP', 'ran', r.testsRun, 'failures', len(r.failures), 'errors', len(r.errors), 'skipped', len(r.skipped))
for t, _ in r.skipped: print('SKIPPED', t.id())
for t, tb in r.failures + r.errors: print('PROBLEM', t.id()); print(tb[-1500:])
