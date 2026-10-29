"""Build the E_6 installation package (Claude, 30 Oct 2026). New files plus three whole-file replacements.

Usage: python3 -I build_e6_install.py DEV_TREE BASE_TREE OUTDIR
DEV_TREE: the base checkout plus the E_6 files; BASE_TREE: a checkout of BASE. Every file in DEV_TREE that
differs from BASE_TREE must be one of the expected new files or one of the three allowed replacements.
"""
import ast, difflib, hashlib, shutil, sys
from pathlib import Path

dev, base, outdir = map(Path, sys.argv[1:4])
HERE = Path(__file__).resolve().parent
BASE = 'f9de54ad4b877bf45a5e4d8bcca2e4b4b5e3f752'
PKG = 'E6_Install_v1'
VARIANTS = ('BETA_BERNOULLI_FULL_MEMORY_V1', 'BETA_BERNOULLI_DECAY_74_75_V1', 'BETA_BERNOULLI_DECAY_149_150_V1')
CD = 'src/methods/_common/contract_data/'
NEW_EXPECTED = {
    'src/methods/E_006/__init__.py', 'src/methods/E_006/beta_bernoulli.py', 'src/methods/E_006/contract.py',
    'src/methods/E_006/IN_DEVELOPMENT.txt', 'tests/test_e6_beta_bernoulli.py',
    'doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md',
    *(f'{CD}declarations/{g}/E_6/{v}/r1.json' for g in ('POWERBALL', 'OZLOTTO') for v in VARIANTS),
    *(f'{CD}registry/{g}/E_6/{v}/entry_0001.json' for g in ('POWERBALL', 'OZLOTTO') for v in VARIANTS),
    *(f'doc/METHOD_TEMPLATE/{n}' for n in (
        'README.md', 'METHOD_SPECIFICATION_TEMPLATE.md', 'declaration_example.json', 'registry_entry_example.json',
        'make_contract_data.py.txt', 'test_template.py.txt', 'method_folder/__init__.py.txt',
        'method_folder/model.py.txt', 'method_folder/contract.py.txt', 'method_folder/IN_DEVELOPMENT.txt')),
}
REPLACED = {'src/methods/Method_Contract_Runner.py', 'tests/test_e2r_contract.py', 'tests/test_e2r_dispatch.py'}
GUARDED_PATHS = [
    'doc/RATIFICATION_REGISTER_v0_14.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r4.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r5.md',
    'doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md',
    'doc/Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md',
    'src/Powerball_Experiment_Coordinator.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/game_profiles.py', 'src/methods/_common/canonical_encoding.py',
    'src/methods/E_001/multigame_e1.py', 'src/methods/E_001/e1_historical_appearance_frequency.py',
    'src/methods/E_001/e1_training_view.py', 'src/methods/E_001/e1_standalone_contract.py',
    'src/methods/E_001_Historical_Appearance_Frequency.py',
    'src/methods/_common/contract_vocab.py', 'src/methods/_common/contract_records.py',
    'src/methods/_common/contract_task.py', 'src/methods/_common/contract_forecast.py',
    'src/methods/_common/contract_receipts.py', 'src/methods/_common/contract_registry.py',
    'src/methods/_common/contract_dispatch.py', 'src/methods/_common/contract_publication.py',
    'src/methods/_common/contract_runner.py', 'src/methods/contract_adapters/e_001.py',
    'src/coordinator_private/contract_coordinated_gate.py', 'src/coordinator_private/multigame_launch_spec.py',
    'src/methods/_common/multigame_method_registry.py', 'src/methods/_common/multigame_result_registry.py',
    'src/methods/_common/multigame_standalone_contract.py',
    'tests/e2r_fixtures.py', 'tests/e2r_code2_fixtures.py', 'tests/test_e2r_runner.py',
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
assert new == NEW_EXPECTED, sorted(new ^ NEW_EXPECTED)
for p in REPLACED:
    assert d[p].read_bytes() != b[p].read_bytes(), f'replacement not changed: {p}'
files = {p: d[p].read_bytes() for p in sorted(new)}
diffs = ''.join(''.join(difflib.unified_diff(b[p].read_text().splitlines(True), d[p].read_text().splitlines(True),
                                             f'a/{p}', f'b/{p}')) for p in sorted(REPLACED))
files[f'review/{PKG}/replaced_files_base_to_v1.diff'] = diffs.encode('ascii')
for name in ('suite_e6_linux_py313.txt', 'suite_e6_linux_py315b4.txt', 'e6_mutation_checks_linux.txt',
             'template_trial_linux.txt'):
    files[f'review/{PKG}/{name}'] = (HERE / 'ev' / name).read_bytes()
for name in ('e6_mutations.py', 'make_e6_contract_data.py', 'template_trial.py'):
    files[f'review/{PKG}/tools/{name}'] = (HERE / 'tools' / name).read_bytes()
replaced = {p: d[p].read_bytes() for p in REPLACED}
for p, raw in [*files.items(), *replaced.items()]:
    assert b'\r' not in raw, p
    assert raw.isascii(), p
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
man = ('# E_6 package installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file\n' +
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
(out / 'VERIFY_E6_INSTALL.py').write_bytes(v.encode('ascii'))
shutil.copy(HERE / 'RUN_E6_SUITE.py', out / 'RUN_E6_SUITE.py')
_expected = next(n.value for n in ast.parse((HERE / 'RUN_E6_SUITE.py').read_text()).body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED')
SUITE_N = sum(c for _m, c in ast.literal_eval(_expected))
TOTAL = len(NEW) + len(MOD)
P = rf'E:\TEMP\{PKG}'
instr = f"""# E_6 package - E_6 revision 1 installed non-runnable, and the new-method template (only after the reviewer's PASS and the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\E6_Install_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files and replaces {len(MOD)} existing files (`{"`, `".join(sorted(MOD))}`); nothing else changes. E_6 is installed **non-runnable**: every E_6 request is refused until a separate release package.

## 1. Update, check, copy, check

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_E6_INSTALL.py" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_E6_INSTALL.py" --repo . --phase post
```

Expected: `git status --short` prints nothing (if it prints anything, stop and send Claude the output); the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; `POST PASS`.

## 2. Tests, before committing (offline; nothing in the repository is changed)

```bat
.venv\\Scripts\\python.exe "{P}\\RUN_E6_SUITE.py" --repo .
```

Expected: `SUITE PASS` ({SUITE_N} tests; the only allowed skips are symlink tests: on Windows without symlink rights, up to 3). E2R-T12 starts up to six ordinary Python worker processes and lets them finish normally. **Do not skip this step.** If anything in steps 1 or 2 prints `STOP` or `FAILED`, do not commit: send Claude the output.

## 3. Stage, commit, check, and only then push

```bat
git add doc review src tests
git status --short
git commit -m "E_6 revision 1 (installed non-runnable) and the new-method template draft 1"
python "{P}\\VERIFY_E6_INSTALL.py" --repo . --phase committed
```

Expected: `git status --short` lists {len(NEW)} lines starting with `A` and {len(MOD)} starting with `M`, and nothing else; then `COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings while staging are normal.

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
