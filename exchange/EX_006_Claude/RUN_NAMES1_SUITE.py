#!/usr/bin/env python3
"""NAMES-1 N1-T09: run all 79 current tests, module by module, and compare with the expected counts.

Claude, 28 October 2026. Owner-run on Windows, after the overlay is copied and before committing.
Offline: these are the existing accepted test modules under their new names. They read no holdout,
start no Windows process, and make no network access; this script only runs them and reports.
Each module runs in its own `python -B -m unittest -v` process (no bytecode written).
A skip is allowed only where the existing tests skip because Windows cannot create a symlink (the
reader-contracts symlink subtest and the exit-receipt symlink test). Anything else stops.
Usage (repository root):  .venv\\Scripts\\python.exe RUN_NAMES1_SUITE.py --repo .
"""
import argparse, os, platform, re, subprocess, sys
from pathlib import Path

EXPECTED = [  # module, tests; first the 60-test standard suite, then the other 19
    ('tests.test_multigame_reader_contracts', 10), ('tests.test_multigame_static_and_timing', 6),
    ('tests.test_multigame_launch_and_manifest', 11), ('tests.test_multigame_exit_receipt', 18),
    ('tests.test_multigame_science_allowlist', 6), ('tests.test_multigame_console_and_synthetic_scorer', 7),
    ('tests.test_t05_hardening', 2), ('tests.test_e1_standalone', 13),
    ('tests.test_multigame_windows_lifecycle_review', 6),
]
SYMLINK_SKIP_OK = {'tests.test_multigame_reader_contracts', 'tests.test_multigame_exit_receipt'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    repo = ap.parse_args().repo.resolve()
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(repo / p) for p in ('src', os.path.join('src', 'methods'), 'tests'))
    print('environment:', platform.system(), platform.release(), 'Python', platform.python_version(), sys.executable)
    bad, total, skipped = [], 0, 0
    for mod, want in EXPECTED:
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', mod], cwd=repo, env=env,
                           capture_output=True, text=True)
        err = r.stderr
        m = re.search(r'^Ran (\d+) tests?', err, re.M)
        ran = int(m.group(1)) if m else -1
        last = err.strip().splitlines()[-1] if err.strip() else '(no output)'
        skips = [ln.strip() for ln in err.splitlines() if re.search(r"\.\.\. skipped|\) \.\.\. skipped|skipped '", ln)]
        total += max(ran, 0); skipped += len(skips)
        print(f'{mod:<52} ran {ran:3d} (expected {want:2d})  skipped {len(skips)}  {last}')
        for s in skips:
            print('    skip:', s[:200])
        if r.returncode != 0 or ran != want or not last.startswith('OK'):
            bad.append(f'{mod}: exit {r.returncode}, ran {ran} expected {want}, "{last}"')
        for s in skips:
            if mod not in SYMLINK_SKIP_OK or 'symlink' not in s.lower():
                bad.append(f'{mod}: unexpected skip: {s[:120]}')
    print(f'total ran {total} (expected 79); skips {skipped}')
    if bad:
        print('SUITE STOP:'); [print('  ' + b) for b in bad]; sys.exit(1)
    print('SUITE PASS: all 79 tests ran and passed; only the allowed symlink skips, if any.')


if __name__ == '__main__':
    main()
