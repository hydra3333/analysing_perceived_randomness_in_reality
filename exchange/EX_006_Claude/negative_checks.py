"""NAMES-1 v0.2 design evidence: fresh-interpreter origin, refusal and mutation checks (N1-C01, N1-C03).

Usage: python3 -I negative_checks.py BASE_TREE RENAMED_TREE WORK_DIR
BASE_TREE is an export of 38fc60e; RENAMED_TREE is the same export after apply_trial.py; WORK_DIR is an
empty scratch folder for mutation copies. Read-only for both trees. Prints one line per check and
exits non-zero if any check fails. Every import check runs in its own fresh `python -I` process with an
explicit sys.path (src, src/methods, tests), so nothing cached in sys.modules or PYTHONPATH can help.
"""
import ast, os, re, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rename_map as R

base, tree, work = (Path(a).resolve() for a in sys.argv[1:4])
fails = 0


def check(ok, what):
    global fails
    print(('PASS ' if ok else 'FAIL ') + what)
    fails += not ok


def fresh(code, root):
    pre = ('import sys; sys.path[:0] = [%r, %r, %r]\n'
           % (str(root / 'src'), str(root / 'src' / 'methods'), str(root / 'tests')))
    r = subprocess.run([sys.executable, '-I', '-B', '-c', pre + code], cwd=work, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def run_firewall_test(root):
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(root / p) for p in ('src', 'src/methods', 'tests'))
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q',
                        'test_multigame_static_and_timing.StaticSafetyTests.'
                        'test_method_loader_import_firewall_except_accepted_legacy_e1'],
                       cwd=root, env=env, capture_output=True, text=True)
    return r.returncode


fmap, bare = R.files(), R.bare()
old_mods = {**{o: n for o, n in R.MODULES.items()}, **{o: n for o, n in R.TESTS.items()}}

# 1. Paths: every old path absent, every new path present; no stray old-name source or bytecode.
for old, new in fmap.items():
    check(not (tree / old).exists() and (tree / new).is_file(), f'path {old} -> {new}')
stray = [p for p in tree.rglob('*') if p.suffix in ('.py', '.pyc') and p.stem.split('.')[0] in bare
         and '__pycache__' not in p.parts and p.relative_to(tree).parts[0] in ('src', 'tests')]
check(not stray, f'no old-name .py/.pyc outside __pycache__ under src/ or tests/ ({len(stray)} found)')

# 2. Fresh interpreter: every old module name is refused; every new module imports from its new path.
for old, new in old_mods.items():
    rc, out = fresh(f'import importlib.util as u; print(u.find_spec({old!r}))', tree)
    check(rc == 0 and out == 'None', f'old name not importable: {old}')
for old, new in old_mods.items():
    rel = [n for o, n in fmap.items() if Path(n).stem == new.split('.')[-1]][0]
    code = (f'import importlib, pathlib; m = importlib.import_module({new!r}); '
            f'print(m.__name__, pathlib.Path(m.__file__).resolve())')
    rc, out = fresh(code, tree)
    check(rc == 0 and out == f'{new} {(tree / rel).resolve()}', f'new name origin: {new} -> {rel}')

# 3. Exit-receipt issuer origin (coordinator lines 1103-1105): exact literal, same resolution, no relaxing.
coord = (tree / 'src' / 'Powerball_Experiment_Coordinator.py').read_text(encoding='utf-8')
consts = {n.value for n in ast.walk(ast.parse(coord)) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
check('multigame_coordinator_exit_receipt.py' in consts and 'multigame_coordinator_exit_receipt_v2.py' not in consts,
      'coordinator issuer literal is the new file name only')
check(coord.count('if actual_issuer != expected_issuer:') == 1 and
      coord.count("raise ValueError('untrusted coordinator receipt issuer location')") == 1,
      'coordinator issuer comparison and refusal unchanged')
code = ("import pathlib; import coordinator_private.multigame_coordinator_exit_receipt as m; "
        f"root = pathlib.Path({str(tree)!r}); "
        "e = (root / 'src' / 'coordinator_private' / 'multigame_coordinator_exit_receipt.py').resolve(strict=True); "
        "print(pathlib.Path(m.__file__).resolve(strict=True) == e)")
check(fresh(code, tree) == (0, 'True'), 'fresh interpreter: receipt module origin equals the coordinator expected issuer')
code = (f"import pathlib; (pathlib.Path({str(tree)!r}) / 'src' / 'coordinator_private' / "
        "'multigame_coordinator_exit_receipt_v2.py').resolve(strict=True)")
rc, out = fresh(code, tree)
check(rc != 0 and 'FileNotFoundError' in out, 'mutation: a stale old issuer literal fails closed (FileNotFoundError)')

# 4. Exit-receipt contract-module file names (receipt line 31): the hashed files exist under their new names.
code = ("import coordinator_private.multigame_coordinator_exit_receipt as m; "
        "print(sorted(m._contract_hashes()))")
check(fresh(code, tree) == (0, "['multigame_console_protocol.py', 'multigame_result_registry.py']"),
      'receipt contract-module hashes computed from the renamed files')

# 5. Firewall (static test lines 99 and 102): mutation and control cases.
def mutant(name, edit_test_back=False, probe=None):
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(tree, d, ignore=shutil.ignore_patterns('__pycache__'))
    if probe is not None:
        (d / 'src' / 'methods' / 'E_999_Firewall_Probe.py').write_text(probe, encoding='utf-8')
    if edit_test_back:
        t = d / 'tests' / 'test_multigame_static_and_timing.py'
        s = t.read_text(encoding='utf-8')
        assert s.count("assertNotIn('game_draws_reader',") == 2
        t.write_text(s.replace("assertNotIn('game_draws_reader',", "assertNotIn('game_draws_reader_v1',"), encoding='utf-8')
    return d

check(run_firewall_test(mutant('m0_control')) == 0, 'control: renamed tree, no probe: firewall test passes')
check(run_firewall_test(mutant('m1_from', probe='from _common.game_draws_reader import DrawView\n')) != 0,
      'mutation: a method doing "from _common.game_draws_reader import ..." is rejected')
check(run_firewall_test(mutant('m2_import', probe='import _common.game_draws_reader as r\n')) != 0,
      'mutation: a method doing "import _common.game_draws_reader" is rejected')
check(run_firewall_test(mutant('m3_oldliteral', edit_test_back=True,
                               probe='from _common.game_draws_reader import DrawView\n')) == 0,
      'why the literal must change: with the old literal kept, the same new-name import would be accepted')
d = work / 'm4_base'
if d.exists():
    shutil.rmtree(d)
shutil.copytree(base, d, ignore=shutil.ignore_patterns('__pycache__'))
(d / 'tests' / 'test_multigame_v011_static_and_timing.py').rename(d / 'tests' / 'test_multigame_static_and_timing.py')
check(run_firewall_test(d) == 0, 'base tree (test file name only aliased): firewall test passes before the rename')

# 6. Non-Python live files: no old name anywhere outside review/, doc/ and transitory_data/ (history).
pat = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, bare), key=len, reverse=True)) + r')\b')
hits = []
for p in tree.rglob('*'):
    rel = p.relative_to(tree)
    if not p.is_file() or rel.parts[0] in ('review', 'doc', 'transitory_data', 'exchange', 'source_data', 'results') or '__pycache__' in rel.parts:
        continue
    try:
        txt = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    if pat.search(txt):
        hits.append(rel.as_posix())
check(not hits, f'no old name in any live file outside review/, doc/, transitory_data/, exchange/ (source_data/ and results/ not opened) ({hits})')
bats = sorted(p.relative_to(base).as_posix() for p in base.rglob('*.bat'))
check(all((base / b).read_bytes() == (tree / b).read_bytes() for b in bats) and bats ==
      sorted(p.relative_to(tree).as_posix() for p in tree.rglob('*.bat')), f'{len(bats)} .bat files byte-identical: {bats}')

print('RESULT', 'PASS' if fails == 0 else f'FAIL ({fails})')
sys.exit(1 if fails else 0)
