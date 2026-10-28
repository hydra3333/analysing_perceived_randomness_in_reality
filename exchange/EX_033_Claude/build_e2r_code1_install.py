"""Build the E2R-CODE-1 installation package (Claude, 28 Oct 2026). New files only.

Usage: python3 -I build_e2r_code1_install.py DEV_TREE BASE_TREE REGISTER EX028_DIR EX032_DIR OUTDIR
DEV_TREE: the base checkout plus CODE-1's new files; BASE_TREE: a checkout of BASE. Every file in DEV_TREE
that differs from BASE_TREE must be a new file under the CODE-1 paths; nothing existing may change.
"""
import hashlib, shutil, sys
from pathlib import Path

dev, base, reg, ex28, ex32, outdir = map(Path, sys.argv[1:7])
HERE = Path(__file__).resolve().parent
BASE = '2f4e84e1d8454e847fdfd7d8e832adb0d0187460'
PKG = 'E2R_CODE1_Install_v1'
GUARDED_PATHS = [
    'doc/RATIFICATION_REGISTER_v0_10.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r3.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md',
    'doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md',
    'src/Powerball_Experiment_Coordinator.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/game_profiles.py', 'src/methods/_common/canonical_encoding.py',
    'src/methods/_common/multigame_method_registry.py', 'src/methods/E_001_Historical_Appearance_Frequency.py',
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tracked(t):
    return {p.relative_to(t).as_posix(): p for p in t.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}


d, b = tracked(dev), tracked(base)
for p in b:
    assert p in d and d[p].read_bytes() == b[p].read_bytes(), f'existing file changed or missing: {p}'
code = {p: d[p].read_bytes() for p in sorted(set(d) - set(b))}
allowed = lambda p: (p.startswith('src/methods/_common/contract_') or
                     p in ('tests/e2r_fixtures.py', 'tests/test_e2r_contract.py', 'tests/test_e2r_prefix.py'))
assert all(allowed(p) for p in code), sorted(p for p in code if not allowed(p))
lf = lambda raw: raw.replace(b'\r\n', b'\n')
files = dict(code)
files['doc/Predictive_Randomness_E2R_Code_Scope_v0_1.md'] = (HERE / 'Predictive_Randomness_E2R_Code_Scope_v0_1.md').read_bytes()
files['doc/RATIFICATION_REGISTER_v0_11.md'] = reg.read_bytes()
files['review/E2R_CODE1_Implementation_Notes_v0_1.md'] = (HERE / 'E2R_CODE1_Implementation_Notes_v0_1.md').read_bytes()
for name in ('Independent_ChatGPT_E1ALIGN_Code_RECHECK_v0_1.md', 'Independent_ChatGPT_Register_v0_10_Review_v0_1.md'):
    files[f'review/{name}'] = lf((ex28 / name).read_bytes())
for name in ('Independent_ChatGPT_E2R_Code_Scope_Review_v0_1.md', 'Independent_E2R_T05_Oracle_Plan_v0_1.md',
             'Independent_E2R_T05_Oracle_v0_1.py'):
    files[f'review/{name}'] = lf((ex32 / name).read_bytes())
for name in ('e2r_mutation_checks_linux.txt', 'suite_e2r_linux_py313.txt', 'suite_e2r_linux_py315b4.txt',
             'r4_oracle_agreement_linux.txt'):
    files[f'review/{PKG}/{name}'] = (HERE / 'ev' / name).read_bytes()
for name in ('build_contract_data.py', 'e2r_mutations.py', 'e2r_oracle_export.py', 'make_register_v11.py',
             'r2_method_names.json'):
    files[f'review/{PKG}/tools/{name}'] = (HERE / 'tools' / name).read_bytes()
for p, raw in files.items():
    assert b'\r' not in raw, p
    assert p not in b, f'not a new path: {p}'

out = outdir
if out.exists():
    shutil.rmtree(out)
ov = out / 'repo_overlay'
for p, raw in files.items():
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(raw)
mp = f'review/{PKG}/INSTALL_MANIFEST_SHA256.txt'
man = '# E2R-CODE-1 installation manifest (Git-content SHA-256, LF); every path is new\n' + ''.join(
    f'{sha(raw)}  {p}\n' for p, raw in sorted(files.items()))
(ov / mp).write_bytes(man.encode('ascii'))
files[mp] = man.encode('ascii')
NEW = {p: sha(raw) for p, raw in files.items()}
guarded = {p: sha(b[p].read_bytes()) for p in GUARDED_PATHS}

v = (HERE / 'verifier_template.py').read_text()
v = (v.replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEW.items())))
      .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in guarded.items()))
      .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEW))))
assert '@@' not in v
(out / 'VERIFY_E2R_CODE1_INSTALL.py').write_bytes(v.encode('ascii'))
shutil.copy(HERE / 'RUN_E2R_SUITE.py', out / 'RUN_E2R_SUITE.py')
P = rf'E:\TEMP\{PKG}'
instr = f"""# E2R-CODE-1 - the E_2-readiness contract library (only after the reviewer's RECHECK PASS and the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\E2R_CODE1_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files and changes no existing file.

## 1. Update, check, copy, check

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_E2R_CODE1_INSTALL.py" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_E2R_CODE1_INSTALL.py" --repo . --phase post
```

Expected: `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{len(NEW)} File(s) copied`; `POST PASS`.

## 2. Tests (offline; nothing in the repository is changed)

```bat
.venv\\Scripts\\python.exe "{P}\\RUN_E2R_SUITE.py" --repo .
```

Expected: `SUITE PASS` (132 tests; the only allowed skips are the two symlink tests). The determinism test (E2R-T12) starts up to six ordinary Python worker processes and lets them finish normally; nothing is killed. **Send Claude the output whatever it says.** If anything in steps 1 or 2 prints `STOP` or `FAILED`, do not commit: send Claude the output (nothing is committed; the copied files are only new files).

## 3. Stage, commit, check, and only then push

```bat
git add doc review src tests
git status --short
git commit -m "E2R-CODE-1: E_2-readiness contract library (new files only) and register v0.11"
python "{P}\\VERIFY_E2R_CODE1_INSTALL.py" --repo . --phase committed
```

Expected: `git status --short` lists {len(NEW)} lines starting with `A` and nothing else; then `COMMITTED PASS`.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub. Claude pushes nothing to the repository while you install.
"""
(out / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(len(NEW), 'new files:', len(code), 'code/data/tests', len(NEW) - len(code), 'documents and evidence')
