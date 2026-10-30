"""Build the E_3/E_4 installation package (Claude, 30 Oct 2026). New files plus one whole-file replacement.

Usage: python3 -I build_e34_install.py DEV_TREE BASE_TREE OUTDIR BASE_COMMIT REGISTER
DEV_TREE: the base checkout plus the E_3/E_4 files; BASE_TREE: a checkout of BASE_COMMIT, which is the commit
that installed the E_6 package. Every file in DEV_TREE that differs from BASE_TREE must be one of the expected
new files or the one allowed replacement (the contract runner's ADAPTERS list).
BASE_COMMIT is the E_6 installation commit 7c93320. REGISTER is register v0.16 (candidate or final), installed
with the package as doc/RATIFICATION_REGISTER_v0_16.md, together with the LF copy of the EX_053 review.
"""
import ast, difflib, hashlib, shutil, sys
from pathlib import Path

dev, base, outdir = map(Path, sys.argv[1:4])
BASE = sys.argv[4]
reg = Path(sys.argv[5])
HERE = Path(__file__).resolve().parent
PKG = 'E34_Install_v1'
VARIANTS = ('POLY_LS_W52_D2_V1', 'POLY_LS_W52_D3_V1', 'POLY_LS_W104_D3_V1', 'POLY_INTERP_W52_D4_H4_V1',
            'POLY_MINIMAX_W52_D2_H4_V1', 'POLY_MINIMAX_W52_D3_H4_V1')
CD = 'src/methods/_common/contract_data/'
DESIGN = 'doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md'
NEW_EXPECTED = {
    'src/methods/_common/polynomial_fits.py', 'tests/test_polynomial_fits.py', 'tests/test_e3_e4_polynomial.py', DESIGN,
    *(f'src/methods/{f}/{n}' for f in ('E_003', 'E_004')
      for n in ('__init__.py', 'variants.py', 'contract.py', 'IN_DEVELOPMENT.txt')),
    *(f'{CD}{kind}/{g}/{m}/{v}/{leaf}' for kind, leaf in (('declarations', 'r1.json'), ('registry', 'entry_0001.json'))
      for g in ('POWERBALL', 'OZLOTTO') for m in ('E_3', 'E_4') for v in VARIANTS),
}
REPLACED = {'src/methods/Method_Contract_Runner.py'}
GUARDED_PATHS = [
    'doc/RATIFICATION_REGISTER_v0_15.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r4.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r5.md',
    'doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md',
    'doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md',
    'src/Powerball_Experiment_Coordinator.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/game_profiles.py', 'src/methods/_common/canonical_encoding.py',
    'src/methods/E_001/multigame_e1.py', 'src/methods/E_001/e1_standalone_contract.py',
    'src/methods/_common/contract_vocab.py', 'src/methods/_common/contract_records.py',
    'src/methods/_common/contract_task.py', 'src/methods/_common/contract_forecast.py',
    'src/methods/_common/contract_receipts.py', 'src/methods/_common/contract_registry.py',
    'src/methods/_common/contract_dispatch.py', 'src/methods/_common/contract_publication.py',
    'src/methods/_common/contract_runner.py', 'src/methods/contract_adapters/e_001.py',
    'src/coordinator_private/contract_coordinated_gate.py', 'src/coordinator_private/multigame_launch_spec.py',
    'src/methods/_common/multigame_method_registry.py',
    'src/methods/E_006/beta_bernoulli.py', 'src/methods/E_006/contract.py', 'src/methods/E_006/IN_DEVELOPMENT.txt',
    'tests/e2r_fixtures.py', 'tests/e2r_code2_fixtures.py', 'tests/test_e2r_runner.py', 'tests/test_e2r_contract.py',
    'tests/test_e2r_dispatch.py', 'tests/test_e6_beta_bernoulli.py', 'doc/METHOD_TEMPLATE/README.md',
    f'{CD}registry/POWERBALL/E_3/NOT_YET_SPECIFIED/entry_0001.json',
    f'{CD}registry/OZLOTTO/E_4/NOT_YET_SPECIFIED/entry_0001.json',
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
for p in GUARDED_PATHS:
    assert p in b, f'guarded path not in base: {p}'
files = {p: d[p].read_bytes() for p in sorted(new)}
diffs = ''.join(''.join(difflib.unified_diff(b[p].read_text().splitlines(True), d[p].read_text().splitlines(True),
                                             f'a/{p}', f'b/{p}')) for p in sorted(REPLACED))
files[f'review/{PKG}/replaced_file_base_to_v1.diff'] = diffs.encode('ascii')
for name in ('suite_py313.txt', 'suite_py315.txt', 'mutations_py313.txt'):
    files[f'review/{PKG}/{name}'] = (HERE / 'ev' / name).read_bytes()
for name in ('e34_mutations.py', 'make_e3e4_contract_data.py'):
    files[f'review/{PKG}/tools/{name}'] = (HERE / 'tools' / name).read_bytes()
files['doc/RATIFICATION_REGISTER_v0_16.md'] = reg.read_bytes()
files['review/Independent_ChatGPT_EX052_Three_Part_Review_v0_1.md'] = (
    Path('/home/claude/work/reg16/Independent_ChatGPT_EX052_Three_Part_Review_v0_1.md').read_bytes())
assert hashlib.sha256(files['review/Independent_ChatGPT_EX052_Three_Part_Review_v0_1.md']).hexdigest() == (
    '8cb7519e72c01751d8a88e211517e65daf8ea63d88fef3fbafd35fc21a1b6491')
replaced = {p: d[p].read_bytes() for p in REPLACED}
for p, raw in [*files.items(), *replaced.items()]:
    assert b'\r' not in raw, p
    assert raw.isascii() or p.startswith('doc/RATIFICATION_REGISTER_'), p   # the register keeps its UTF-8 title
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
man = ('# E_3/E_4 package installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file\n' +
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
(out / 'VERIFY_E34_INSTALL.py').write_bytes(v.encode('ascii'))
shutil.copy(HERE / 'RUN_E34_SUITE.py', out / 'RUN_E34_SUITE.py')
_expected = next(n.value for n in ast.parse((HERE / 'RUN_E34_SUITE.py').read_text()).body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED')
SUITE_N = sum(c for _m, c in ast.literal_eval(_expected))
TOTAL = len(NEW) + len(MOD)
P = rf'E:\TEMP\{PKG}'
instr = f"""# E_3/E_4 package v1 - E_3 and E_4 revision 1 and their shared helper, installed non-runnable, and register v0.16 (only after the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Install the E_6 package first; this package checks that it is there.** **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\E34_Install_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files and replaces 1 existing file (`{"`, `".join(sorted(MOD))}`); nothing else changes. E_3 and E_4 are installed **non-runnable**: every E_3 or E_4 request is refused until a separate release package.

## 1. Update, check, copy, check

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_E34_INSTALL.py" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_E34_INSTALL.py" --repo . --phase post
```

Expected: `git status --short` prints nothing (if it prints anything, stop and send Claude the output); the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; `POST PASS`.

## 2. Tests, before committing (offline; nothing in the repository is changed)

```bat
.venv\\Scripts\\python.exe "{P}\\RUN_E34_SUITE.py" --repo .
```

Expected: `SUITE PASS` ({SUITE_N} tests; the only allowed skips are symlink tests: on Windows without symlink rights, up to 3). E2R-T12 starts up to six ordinary Python worker processes and lets them finish normally. **Do not skip this step.** If anything in steps 1 or 2 prints `STOP` or `FAILED`, do not commit: send Claude the output.

## 3. Stage, commit, check, and only then push

```bat
git add doc review src tests
git status --short
git commit -m "E_3 and E_4 revision 1 with the shared polynomial helper (installed non-runnable) and register v0.16"
python "{P}\\VERIFY_E34_INSTALL.py" --repo . --phase committed
```

Expected: `git status --short` lists {len(NEW)} lines starting with `A` and 1 starting with `M`, and nothing else; then `COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings while staging are normal.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub. Claude pushes nothing to the repository while you install.
"""
(out / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(len(NEW), 'new files and', len(MOD), 'replaced; suite', SUITE_N, '; base', BASE)
