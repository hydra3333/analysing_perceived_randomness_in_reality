#!/usr/bin/env python3
"""RUN_MHUP_A_SUITE.py - the suite runner of the MHUP-A install package (design Appendix J step 10).

DRAFT (item 2 of the integrated package work list). Claude web chat, 10 November 2026, from the slice 2 runner.
Runs every test module of the installed tree, each in its own `python -B -m unittest -v` process (no byte-code
written), and compares each module's count with the count the package builder took from the unittest loader.
The tests are offline: temporary registries, method folders, invented masters and run folders, and the project's
accepted tests, some of which read the development masters through the project's reader. They read no holdout,
start no Windows process beyond E2R-T12's ordinary local workers (it needs the owner's approval for each run context),
and make no network access; this script only runs them. A skip is allowed only where a test skips because Windows
cannot create a symlink (four modules). Anything else stops. A failing module's output is printed: test failure
output; inspect before sharing (R-010).
Usage: python -I RUN_MHUP_A_SUITE.py --repo REPO
"""
import argparse, os, platform, re, subprocess, sys, time
from pathlib import Path

EXPECTED = [
@@EXPECTED@@
]
TOTAL = sum(n for _m, n in EXPECTED)
SYMLINK_SKIP_OK = {'tests.test_multigame_reader_contracts', 'tests.test_multigame_exit_receipt',
                   'tests.test_e2r_runner', 'tests.test_wf1b_outcome_reader'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    repo = ap.parse_args().repo.resolve()
    present = sorted(p.stem for p in (repo / 'tests').glob('test_*.py'))
    listed = sorted(m.split('.', 1)[1] for m, _ in EXPECTED)
    if present != listed:
        print('SUITE STOP: the test modules on disk are not the package\'s list:',
              sorted(set(present) ^ set(listed)))
        sys.exit(1)
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(repo / p) for p in ('src', os.path.join('src', 'methods'), 'tests'))
    print('environment:', platform.system(), platform.release(), 'Python', platform.python_version(), sys.executable, flush=True)
    t_all = time.perf_counter()
    bad, total, skipped = [], 0, 0
    for mod, want in EXPECTED:
        t0 = time.perf_counter()
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', mod], cwd=repo, env=env,
                           capture_output=True, text=True)
        secs = time.perf_counter() - t0
        err = r.stderr
        m = re.search(r'^Ran (\d+) tests?', err, re.M)
        ran = int(m.group(1)) if m else -1
        last = err.strip().splitlines()[-1] if err.strip() else '(no output)'
        skips = [ln.strip() for ln in err.splitlines() if re.search(r"\.\.\. skipped|\) \.\.\. skipped|skipped '", ln)]
        total += max(ran, 0); skipped += len(skips)
        print(f'{mod:<52} ran {ran:3d} (expected {want:2d})  skipped {len(skips)}  {last}  ({secs:.1f} s)', flush=True)
        for s in skips:
            print('    skip:', s[:200])
        if r.returncode != 0 or ran != want or not last.startswith('OK'):
            bad.append(f'{mod}: exit {r.returncode}, ran {ran} expected {want}, "{last}"')
            detail = [ln for ln in (err + r.stdout).splitlines() if ln.strip()]
            start = next((i for i, ln in enumerate(detail) if ln.startswith(('ERROR:', 'FAIL:'))), max(len(detail) - 40, 0))
            print('    detail (test failure output; inspect before sharing):')
            for ln in detail[start:start + 60]:
                print('    | ' + ln[:200])
        for s in skips:
            if mod not in SYMLINK_SKIP_OK or 'symlink' not in s.lower():
                bad.append(f'{mod}: unexpected skip: {s[:120]}')
    print(f'total ran {total} (expected {TOTAL}); skips {skipped}; elapsed {time.perf_counter() - t_all:.0f} s')
    if bad:
        print('SUITE STOP:'); [print('  ' + b) for b in bad]; sys.exit(1)
    print(f'SUITE PASS: all {TOTAL} tests ran and passed; only the allowed symlink skips, if any.')


if __name__ == '__main__':
    main()
