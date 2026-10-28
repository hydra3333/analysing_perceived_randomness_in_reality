"""Run the E2R-CODE-1 suite exactly as the package's RUN_E2R_SUITE.py does, but without E2R-T12.

Written by the Claude web chat, 29 October 2026, for task clones. E2R-T12 (class T12Determinism, one
test) starts up to six Python worker processes; the project owner has not yet approved that, so it is
left out unless the owner says otherwise. Every other test runs, with the same expected counts and the
same skip rule (only the two symlink skips). Offline; it reads no source_data, results or transitory_data.
Usage: <venv python> -I run_e2r_suite_without_t12.py --repo <task clone>
Prints SUITE PASS (132 of 133 tests; T12 not run) or SUITE STOP.
"""
import argparse, ast, os, platform, re, subprocess, sys
from pathlib import Path

EXPECTED = [
    ('tests.test_multigame_reader_contracts', 10), ('tests.test_multigame_static_and_timing', 6),
    ('tests.test_multigame_launch_and_manifest', 11), ('tests.test_multigame_exit_receipt', 18),
    ('tests.test_multigame_science_allowlist', 6), ('tests.test_multigame_console_and_synthetic_scorer', 7),
    ('tests.test_t05_hardening', 2), ('tests.test_e1_align', 5), ('tests.test_e1_standalone', 13),
    ('tests.test_multigame_windows_lifecycle_review', 6),
    ('tests.test_e2r_contract', 48), ('tests.test_e2r_prefix', 1),
]
SYMLINK_SKIP_OK = {'tests.test_multigame_reader_contracts', 'tests.test_multigame_exit_receipt'}
LEFT_OUT = ('tests.test_e2r_contract', 'T12Determinism')


def test_classes(path):
    """Test classes of a module and their test counts, read with ast (nothing imported)."""
    tree = ast.parse(path.read_text(encoding='utf-8'))
    return {n.name: sum(1 for f in n.body if isinstance(f, ast.FunctionDef) and f.name.startswith('test'))
            for n in tree.body if isinstance(n, ast.ClassDef)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    repo = ap.parse_args().repo.resolve()
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(repo / p) for p in ('src', os.path.join('src', 'methods'), 'tests'))
    print('environment:', platform.system(), platform.release(), 'Python', platform.python_version(), sys.executable)
    classes = {k: v for k, v in test_classes(repo / 'tests' / 'test_e2r_contract.py').items() if v}
    n_left_out = classes.pop(LEFT_OUT[1], 0)
    if n_left_out != 1 or sum(classes.values()) + n_left_out != 48:
        print(f'SUITE STOP: expected T12Determinism with 1 test and 48 tests in all; found {n_left_out} and '
              f'{sum(classes.values()) + n_left_out}')
        sys.exit(1)
    bad, total, skipped = [], 0, 0
    for mod, want in EXPECTED:
        targets = [mod]
        if mod == LEFT_OUT[0]:
            targets = [f'{mod}.{c}' for c in sorted(classes)]
            want -= n_left_out
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', *targets], cwd=repo, env=env,
                           capture_output=True, text=True)
        err = r.stderr
        m = re.search(r'^Ran (\d+) tests?', err, re.M)
        ran = int(m.group(1)) if m else -1
        last = err.strip().splitlines()[-1] if err.strip() else '(no output)'
        skips = [ln.strip() for ln in err.splitlines() if re.search(r"\.\.\. skipped|\) \.\.\. skipped|skipped '", ln)]
        total += max(ran, 0); skipped += len(skips)
        note = '  (T12Determinism left out)' if mod == LEFT_OUT[0] else ''
        print(f'{mod:<52} ran {ran:3d} (expected {want:2d})  skipped {len(skips)}  {last}{note}')
        for s in skips:
            print('    skip:', s[:200])
        if r.returncode != 0 or ran != want or not last.startswith('OK'):
            bad.append(f'{mod}: exit {r.returncode}, ran {ran} expected {want}, "{last}"')
            print('\n'.join(err.strip().splitlines()[-40:]))
        for s in skips:
            if mod not in SYMLINK_SKIP_OK or 'symlink' not in s.lower():
                bad.append(f'{mod}: unexpected skip: {s[:120]}')
    print(f'total ran {total} (expected 132 = 133 less T12); skips {skipped}')
    if bad:
        print('SUITE STOP:')
        for b in bad:
            print('  ' + b)
        sys.exit(1)
    print('SUITE PASS: 132 of the 133 tests ran and passed (E2R-T12 not run); only the allowed symlink skips, if any.')


if __name__ == '__main__':
    main()
