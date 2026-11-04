#!/usr/bin/env python3
"""MHUPA_Slice2 (review slice 2 of the MHUP-A package): run all 561 current tests, module by module, and compare with the expected counts.

Claude, 5 November 2026 (from the slice 1 runner). Slice 2 adds six test modules: the updater v0.2 (syntax-tree identity and its offline
self-test), the launchers and the byte-code-cache rule, the Mode H study end to end on a temporary project with an invented master
and an invented Python environment (about two minutes: a 60-run synthetic batch and its score, twice), the process tool on mocked
tables, the install and release records on a temporary Git repository, and the Method_Mode_H command. Owner-run on Windows, after the overlay is
copied and before committing. The tests are offline: temporary registries, method folders, invented masters and
run folders, and the project's accepted tests, some of which read the development masters through the project's
reader (as before). They read no holdout, start no Windows process beyond E2R-T12's ordinary local workers, and
make no network access; this script only runs them.
Each module runs in its own `python -B -m unittest -v` process (no bytecode written).
A skip is allowed only where a test skips because Windows cannot create a symlink (the reader-contracts
symlink subtest, the exit-receipt symlink test, CODE-2's dangling-symlink publication test and WF-1B's
symlinked-master test). Anything else stops. A module that fails has its failing tests and tracebacks printed.
Usage (repository root):  .venv\\Scripts\\python.exe RUN_MHUPA_SLICE2_SUITE.py --repo .
"""
import argparse, os, platform, re, subprocess, sys, time
from pathlib import Path

EXPECTED = [
    ('tests.test_multigame_reader_contracts', 10), ('tests.test_multigame_static_and_timing', 6),
    ('tests.test_multigame_launch_and_manifest', 11), ('tests.test_multigame_exit_receipt', 18),
    ('tests.test_multigame_science_allowlist', 6), ('tests.test_multigame_console_and_synthetic_scorer', 7),
    ('tests.test_t05_hardening', 2), ('tests.test_e1_align', 5), ('tests.test_e1_standalone', 13),
    ('tests.test_multigame_windows_lifecycle_review', 6),
    ('tests.test_e2r_contract', 53), ('tests.test_e2r_prefix', 1),
    ('tests.test_e2r_dispatch', 18), ('tests.test_e2r_runner', 34),
    ('tests.test_e6_beta_bernoulli', 20), ('tests.test_polynomial_fits', 19),
    ('tests.test_e3_e4_polynomial', 13), ('tests.test_occurrence_counts', 8),
    ('tests.test_wave1_frequency', 18), ('tests.test_recurrence_gaps', 12),
    ('tests.test_wave2_recurrence', 19), ('tests.test_rel1_release', 5),
    ('tests.test_wf1a_walk_forward', 22), ('tests.test_code3_retirement', 12), ('tests.test_e1r2_revision2', 13),
    ('tests.test_wf1b_numerics', 21),
    ('tests.test_wf1b_n1_generator', 8),
    ('tests.test_wf1b_divisions', 17),
    ('tests.test_wf1b_measures', 33),
    ('tests.test_wf1b_outcome_reader', 6),
    ('tests.test_wf1b_report', 10),
    ('tests.test_wf1b_static', 4),
    ('tests.test_wf1b_crossplatform', 1),
    ('tests.test_wf1b_seed_policy', 11),
    ('tests.test_wf1b_n1_replay', 3),
    ('tests.test_perf1_numerics', 7),
    ('tests.test_mhupa_master_versions', 15),
    ('tests.test_mhupa_gates', 12),
    ('tests.test_e1r3_revision3', 8),
    ('tests.test_mhupa_updater_v0_2', 15),
    ('tests.test_mhupa_launchers', 10),
    ('tests.test_mhupa_mode_h', 14),
    ('tests.test_mhupa_process_check', 7),
    ('tests.test_mhupa_install_records', 6),
    ('tests.test_mhupa_method_mode_h_cli', 2),
]
TOTAL = sum(n for _m, n in EXPECTED)
SYMLINK_SKIP_OK = {'tests.test_multigame_reader_contracts', 'tests.test_multigame_exit_receipt',
                   'tests.test_e2r_runner', 'tests.test_wf1b_outcome_reader'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    repo = ap.parse_args().repo.resolve()
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(repo / p) for p in ('src', os.path.join('src', 'methods'), 'tests'))
    print('environment:', platform.system(), platform.release(), 'Python', platform.python_version(), sys.executable)
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
        print(f'{mod:<52} ran {ran:3d} (expected {want:2d})  skipped {len(skips)}  {last}  ({secs:.1f} s)')
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
    print(f'total ran {total} (expected {TOTAL}); skips {skipped}')
    if bad:
        print('SUITE STOP:'); [print('  ' + b) for b in bad]; sys.exit(1)
    print(f'SUITE PASS: all {TOTAL} tests ran and passed; only the allowed symlink skips, if any.')


if __name__ == '__main__':
    main()
