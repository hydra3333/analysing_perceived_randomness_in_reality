#!/usr/bin/env python3
"""NAMES-1 N1-T05 / N1-T05A: fresh-interpreter import-origin, refusal and firewall-mutation checks.

Claude, 28 October 2026. Owner-run on Windows, after the overlay is copied and before committing.
- Each import check runs in its own new `python -I -B` process with an explicit sys.path (src,
  src/methods, tests) and no PYTHONPATH, so nothing already imported or left on a path can help.
  Importing a module runs only its definitions: no data is read, no process is started.
- The firewall mutations run in a temporary copy of src/ and tests/ only, which is deleted after.
  The repository itself is not changed, and no bytecode is written to it.
Usage (repository root):  .venv\\Scripts\\python.exe CHECK_NAMES1_IMPORTS.py --repo .
"""
import argparse, ast, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

MODULES = json.loads(r'''{
 "_common.e1_common_reader_bridge_v1": [
  "_common.e1_common_reader_bridge",
  "src/methods/_common/e1_common_reader_bridge.py"
 ],
 "_common.e1_historical_appearance_frequency_v0_3": [
  "_common.e1_historical_appearance_frequency",
  "src/methods/_common/e1_historical_appearance_frequency.py"
 ],
 "_common.e1_standalone_contract_v0_1": [
  "_common.e1_standalone_contract",
  "src/methods/_common/e1_standalone_contract.py"
 ],
 "_common.e1_training_view_v0_1": [
  "_common.e1_training_view",
  "src/methods/_common/e1_training_view.py"
 ],
 "_common.game_draws_reader_v1": [
  "_common.game_draws_reader",
  "src/methods/_common/game_draws_reader.py"
 ],
 "_common.game_profiles_v1": [
  "_common.game_profiles",
  "src/methods/_common/game_profiles.py"
 ],
 "_common.multigame_ancestry_release_v1": [
  "_common.multigame_ancestry_release",
  "src/methods/_common/multigame_ancestry_release.py"
 ],
 "_common.multigame_console_protocol_v1": [
  "_common.multigame_console_protocol",
  "src/methods/_common/multigame_console_protocol.py"
 ],
 "_common.multigame_coordinated_manifest_v1": [
  "_common.multigame_coordinated_manifest",
  "src/methods/_common/multigame_coordinated_manifest.py"
 ],
 "_common.multigame_e1_v1": [
  "_common.multigame_e1",
  "src/methods/_common/multigame_e1.py"
 ],
 "_common.multigame_method_registry_v1": [
  "_common.multigame_method_registry",
  "src/methods/_common/multigame_method_registry.py"
 ],
 "_common.multigame_result_registry_v1": [
  "_common.multigame_result_registry",
  "src/methods/_common/multigame_result_registry.py"
 ],
 "_common.multigame_standalone_contract_v1": [
  "_common.multigame_standalone_contract",
  "src/methods/_common/multigame_standalone_contract.py"
 ],
 "_common.multigame_synthetic_scorer_v1": [
  "_common.multigame_synthetic_scorer",
  "src/methods/_common/multigame_synthetic_scorer.py"
 ],
 "_common.multigame_worker_launch_handshake_v1": [
  "_common.multigame_worker_launch_handshake",
  "src/methods/_common/multigame_worker_launch_handshake.py"
 ],
 "coordinator_private.multigame_coordinator_exit_receipt_v2": [
  "coordinator_private.multigame_coordinator_exit_receipt",
  "src/coordinator_private/multigame_coordinator_exit_receipt.py"
 ],
 "coordinator_private.multigame_launch_spec_v1": [
  "coordinator_private.multigame_launch_spec",
  "src/coordinator_private/multigame_launch_spec.py"
 ],
 "coordinator_private.multigame_windows_lifecycle_v1": [
  "coordinator_private.multigame_windows_lifecycle",
  "src/coordinator_private/multigame_windows_lifecycle.py"
 ],
 "test_multigame_console_and_synthetic_scorer_v0_4": [
  "test_multigame_console_and_synthetic_scorer",
  "tests/test_multigame_console_and_synthetic_scorer.py"
 ],
 "test_multigame_exit_receipt_v0_8": [
  "test_multigame_exit_receipt",
  "tests/test_multigame_exit_receipt.py"
 ],
 "test_multigame_launch_and_manifest_v0_8": [
  "test_multigame_launch_and_manifest",
  "tests/test_multigame_launch_and_manifest.py"
 ],
 "test_multigame_science_allowlist_v0_8": [
  "test_multigame_science_allowlist",
  "tests/test_multigame_science_allowlist.py"
 ],
 "test_multigame_v011_reader_contracts": [
  "test_multigame_reader_contracts",
  "tests/test_multigame_reader_contracts.py"
 ],
 "test_multigame_v011_static_and_timing": [
  "test_multigame_static_and_timing",
  "tests/test_multigame_static_and_timing.py"
 ],
 "test_multigame_windows_lifecycle_review_v0_9": [
  "test_multigame_windows_lifecycle_review",
  "tests/test_multigame_windows_lifecycle_review.py"
 ],
 "test_p2_r1_t05_hardening_v1": [
  "test_t05_hardening",
  "tests/test_t05_hardening.py"
 ],
 "test_p3_e1_standalone_v0_1": [
  "test_e1_standalone",
  "tests/test_e1_standalone.py"
 ]
}''')   # old dotted name -> [new dotted name, new path]
fails = 0


def check(ok, what):
    global fails
    print(('PASS ' if ok else 'FAIL ') + what)
    fails += not ok


def fresh(code, root, cwd):
    pre = ('import sys; sys.path[:0] = [%r, %r, %r]\n'
           % (str(root / 'src'), str(root / 'src' / 'methods'), str(root / 'tests')))
    r = subprocess.run([sys.executable, '-I', '-B', '-c', pre + code], cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def firewall(root):
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(root / p) for p in ('src', os.path.join('src', 'methods'), 'tests'))
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q',
                        'test_multigame_static_and_timing.StaticSafetyTests.'
                        'test_method_loader_import_firewall_except_accepted_legacy_e1'],
                       cwd=root, env=env, capture_output=True, text=True)
    return r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    repo = ap.parse_args().repo.resolve()
    with tempfile.TemporaryDirectory(prefix='names1_check_') as tmp:
        tmp = Path(tmp)
        for old, (new, rel) in MODULES.items():
            rc, out = fresh(f'import importlib.util as u; print(u.find_spec({old!r}))', repo, tmp)
            check(rc == 0 and out == 'None', f'old name not importable: {old}')
        for old, (new, rel) in MODULES.items():
            rc, out = fresh(f'import importlib, pathlib; m = importlib.import_module({new!r}); '
                            f'print(m.__name__, pathlib.Path(m.__file__).resolve())', repo, tmp)
            check(rc == 0 and out == f'{new} {(repo / rel).resolve()}', f'new name origin: {new}')
        coord = (repo / 'src' / 'Powerball_Experiment_Coordinator.py').read_text(encoding='utf-8')
        consts = {n.value for n in ast.walk(ast.parse(coord)) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        check('multigame_coordinator_exit_receipt.py' in consts and 'multigame_coordinator_exit_receipt_v2.py' not in consts,
              'coordinator issuer literal names the new file only')
        check(coord.count('if actual_issuer != expected_issuer:') == 1 and
              coord.count("raise ValueError('untrusted coordinator receipt issuer location')") == 1,
              'coordinator issuer comparison and refusal unchanged')
        rc, out = fresh("import pathlib; import coordinator_private.multigame_coordinator_exit_receipt as m; "
                        f"e = (pathlib.Path({str(repo)!r}) / 'src' / 'coordinator_private' / "
                        "'multigame_coordinator_exit_receipt.py').resolve(strict=True); "
                        "print(pathlib.Path(m.__file__).resolve(strict=True) == e)", repo, tmp)
        check((rc, out) == (0, 'True'), 'receipt module origin equals the coordinator expected issuer')
        rc, out = fresh(f"import pathlib; (pathlib.Path({str(repo)!r}) / 'src' / 'coordinator_private' / "
                        "'multigame_coordinator_exit_receipt_v2.py').resolve(strict=True)", repo, tmp)
        check(rc != 0 and 'FileNotFoundError' in out, 'a stale old issuer literal would fail closed')
        rc, out = fresh("import coordinator_private.multigame_coordinator_exit_receipt as m; "
                        "print(sorted(m._contract_hashes()))", repo, tmp)
        check((rc, out) == (0, "['multigame_console_protocol.py', 'multigame_result_registry.py']"),
              'receipt contract-file hashes computed from the renamed files')

        def copy(name, probe=None, old_literal=False):
            d = tmp / name
            for part in ('src', 'tests'):
                shutil.copytree(repo / part, d / part, ignore=shutil.ignore_patterns('__pycache__'))
            if probe:
                (d / 'src' / 'methods' / 'E_999_Firewall_Probe.py').write_text(probe, encoding='utf-8')
            if old_literal:
                t = d / 'tests' / 'test_multigame_static_and_timing.py'
                s = t.read_text(encoding='utf-8')
                assert s.count("assertNotIn('game_draws_reader',") == 2
                t.write_text(s.replace("assertNotIn('game_draws_reader',", "assertNotIn('game_draws_reader_v1',"),
                             encoding='utf-8')
            return d
        check(firewall(copy('c0')) == 0, 'firewall control: the installed tree passes')
        check(firewall(copy('m1', 'from _common.game_draws_reader import DrawView\n')) != 0,
              'firewall: a method doing "from _common.game_draws_reader import ..." is rejected')
        check(firewall(copy('m2', 'import _common.game_draws_reader as r\n')) != 0,
              'firewall: a method doing "import _common.game_draws_reader" is rejected')
        check(firewall(copy('m3', 'from _common.game_draws_reader import DrawView\n', old_literal=True)) == 0,
              'why the literal had to change: with the old literal, the same import would pass')
    print('RESULT', 'PASS' if not fails else f'STOP ({fails} failed)')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
