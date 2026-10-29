"""Build the E2R-CODE-2 installation package (Claude, 29 Oct 2026). New files plus one whole-file replacement.

Usage (v2, after EX_039): python3 -I build_e2r_code2_install.py DEV_TREE BASE_TREE OUTDIR [REGISTER]
DEV_TREE: the base checkout plus CODE-2's files; BASE_TREE: a checkout of BASE. Every file in DEV_TREE that
differs from BASE_TREE must be a new file under the CODE-2 paths, or the one allowed replacement.
REGISTER (optional): the register edition installed with CODE-2, when there is one.
"""
import hashlib, shutil, sys
from pathlib import Path

dev, base, outdir = map(Path, sys.argv[1:4])
reg = Path(sys.argv[4]) if len(sys.argv) > 4 else None
HERE = Path(__file__).resolve().parent
BASE = 'b846519bce7463cc7a7a57095d438b9223dd8bb9'
PKG = 'E2R_CODE2_Install_v2'
NEW_CODE = {
    'src/methods/_common/contract_dispatch.py', 'src/methods/_common/contract_publication.py',
    'src/methods/_common/contract_runner.py', 'src/methods/Method_Contract_Runner.py',
    'src/methods/contract_adapters/__init__.py', 'src/methods/contract_adapters/e_001.py',
    'src/coordinator_private/contract_coordinated_gate.py',
    'tests/e2r_code2_fixtures.py', 'tests/test_e2r_dispatch.py', 'tests/test_e2r_runner.py',
}
REPLACED = {'src/methods/_common/multigame_method_registry.py', 'src/methods/_common/multigame_standalone_contract.py',
            'src/methods/E_001_Historical_Appearance_Frequency.py'}
GUARDED_PATHS = [
    'doc/RATIFICATION_REGISTER_v0_12.md',
    'doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md',
    'src/Powerball_Experiment_Coordinator.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/game_profiles.py', 'src/methods/_common/canonical_encoding.py',
    'src/methods/E_001/multigame_e1.py', 'src/methods/E_001/e1_historical_appearance_frequency.py',
    'src/methods/E_001/e1_training_view.py', 'src/methods/E_001/e1_standalone_contract.py',
    'src/methods/_common/contract_vocab.py', 'src/methods/_common/contract_records.py',
    'src/methods/_common/contract_task.py', 'src/methods/_common/contract_forecast.py',
    'src/methods/_common/contract_receipts.py', 'src/methods/_common/contract_registry.py',
    'src/methods/_common/multigame_result_registry.py', 'src/coordinator_private/multigame_launch_spec.py',
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tracked(t):
    return {p.relative_to(t).as_posix(): p for p in t.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}


d, b = tracked(dev), tracked(base)
for p in b:
    assert p in d, f'missing in dev tree: {p}'
    if p not in REPLACED:
        assert d[p].read_bytes() == b[p].read_bytes(), f'existing file changed: {p}'
new = set(d) - set(b)
assert new == NEW_CODE, sorted(new ^ NEW_CODE)
for p in REPLACED:
    assert d[p].read_bytes() != b[p].read_bytes(), f'replacement not changed: {p}'
files = {p: d[p].read_bytes() for p in sorted(new)}
files['doc/Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md'] = (HERE / 'Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md').read_bytes()
files['review/Independent_ChatGPT_E2R_CODE2_R3_Design_and_Register_v12_Review_v0_1.md'] = (
    (HERE / 'Independent_ChatGPT_E2R_CODE2_R3_Design_and_Register_v12_Review_v0_1.md').read_bytes().replace(b'\r\n', b'\n'))
if reg is not None:
    files[f'doc/{reg.name}'] = reg.read_bytes()
for name in ('suite_e2r_code2_linux_py313.txt', 'suite_e2r_code2_linux_py315b4.txt', 'e2r_code2_mutation_checks_linux.txt'):
    files[f'review/{PKG}/{name}'] = (HERE / 'ev' / name).read_bytes()
files[f'review/{PKG}/tools/e2r_code2_mutations.py'] = (HERE / 'tools' / 'e2r_code2_mutations.py').read_bytes()
replaced = {p: d[p].read_bytes() for p in REPLACED}
for p, raw in [*files.items(), *replaced.items()]:
    assert b'\r' not in raw, p
for p in files:
    assert p not in b, f'not a new path: {p}'

out = outdir
if out.exists():
    shutil.rmtree(out)
ov = out / 'repo_overlay'
for p, raw in [*files.items(), *replaced.items()]:
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(raw)
mp = f'review/{PKG}/INSTALL_MANIFEST_SHA256.txt'
man = ('# E2R-CODE-2 installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file\n' +
       ''.join(f'A {sha(raw)}  {p}\n' for p, raw in sorted(files.items())) +
       ''.join(f'M {sha(raw)}  {p}  (base {sha(b[p].read_bytes())})\n' for p, raw in sorted(replaced.items())))
(ov / mp).write_bytes(man.encode('ascii'))
files[mp] = man.encode('ascii')
NEW = {p: sha(raw) for p, raw in files.items()}
MOD = {p: (sha(b[p].read_bytes()), sha(raw)) for p, raw in replaced.items()}
guarded = {p: sha(b[p].read_bytes()) for p in GUARDED_PATHS}

v = (HERE / 'verifier_template.py').read_text()
v = (v.replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEW.items())))
      .replace('@@MODIFIED@@', '\n'.join(f"    '{p}': ('{o}', '{n}')," for p, (o, n) in sorted(MOD.items())))
      .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in guarded.items()))
      .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEW))).replace('@@M@@', str(len(MOD))))
assert '@@' not in v
(out / 'VERIFY_E2R_CODE2_INSTALL.py').write_bytes(v.encode('ascii'))
shutil.copy(HERE / 'RUN_E2R_CODE2_SUITE.py', out / 'RUN_E2R_CODE2_SUITE.py')
import ast
_expected = next(n.value for n in ast.parse((HERE / 'RUN_E2R_CODE2_SUITE.py').read_text()).body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED')
SUITE_N = sum(c for _m, c in ast.literal_eval(_expected))
TOTAL = len(NEW) + len(MOD)
P = rf'E:\TEMP\{PKG}'
instr = f"""# E2R-CODE-2 - wiring the contract library in (only after the reviewer's RECHECK PASS and the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\E2R_CODE2_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files and replaces {len(MOD)} existing files (`{"`, `".join(sorted(MOD))}`); nothing else changes.

## 1. Update, check, copy, check

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_E2R_CODE2_INSTALL.py" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_E2R_CODE2_INSTALL.py" --repo . --phase post
```

Expected: `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; `POST PASS`.

## 2. Tests (offline; nothing in the repository is changed)

```bat
.venv\\Scripts\\python.exe "{P}\\RUN_E2R_CODE2_SUITE.py" --repo .
```

Expected: `SUITE PASS` ({SUITE_N} tests; the only allowed skips are the two symlink tests). E2R-T12 starts up to six ordinary Python worker processes and lets them finish normally. **Send Claude the output whatever it says.** If anything in steps 1 or 2 prints `STOP` or `FAILED`, do not commit: send Claude the output.

## 3. Stage, commit, check, and only then push

```bat
git add doc review src tests
git status --short
git commit -m "E2R-CODE-2: dispatch gate, standalone contract runner and E_1 wrapper"
python "{P}\\VERIFY_E2R_CODE2_INSTALL.py" --repo . --phase committed
```

Expected: `git status --short` lists {len(NEW)} lines starting with `A` and {len(MOD)} starting with `M`, and nothing else; then `COMMITTED PASS`.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub. Claude pushes nothing to the repository while you install.
"""
(out / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(len(NEW), 'new files and', len(MOD), 'replaced; suite', SUITE_N)
