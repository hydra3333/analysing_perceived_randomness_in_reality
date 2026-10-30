"""Build the wave 1 installation package (E_7, E_8, E_9, E_10; Claude, 30 Oct 2026). New files plus four whole-file
replacements (the runner's ADAPTERS list and three template files, which become draft 2).

Usage: python3 -I build_w1_install.py DEV_TREE BASE_TREE OUTDIR BASE_COMMIT REGISTER
DEV_TREE: the base checkout plus the wave 1 files; BASE_TREE: a checkout of BASE_COMMIT (main after the handover
installation 8defe9d). Every file in DEV_TREE that differs from BASE_TREE must be one of the expected new files or
one of the four allowed replacements. REGISTER is register v0.18 (candidate or final), installed with the package
as doc/RATIFICATION_REGISTER_v0_18.md, together with the LF copies of the EX_062 and EX_064 reviews.
"""
import ast, difflib, hashlib, shutil, sys
from pathlib import Path

dev, base, outdir = map(Path, sys.argv[1:4])
BASE = sys.argv[4]
reg = Path(sys.argv[5])
HERE = Path(__file__).resolve().parent
PKG = 'W1_Install_v1'
VARIANTS = {'E_7': ('BETA_SHRINK_W52_C52_V1', 'BETA_SHRINK_W104_C52_V1', 'BETA_SHRINK_FULL_C52_V1'),
            'E_8': ('HIER_PERIODS_P13_V1', 'HIER_PERIODS_P26_V1', 'HIER_PERIODS_P52_V1'),
            'E_9': ('EXP_DECAY_5_6_V1', 'EXP_DECAY_18_19_V1', 'EXP_DECAY_37_38_V1'),
            'E_10': ('CONTRAST_S13_L104_V1', 'CONTRAST_S26_L208_V1', 'CONTRAST_S52_FULL_V1')}
CD = 'src/methods/_common/contract_data/'
DESIGN = 'doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md'
NEW_EXPECTED = {
    'src/methods/_common/occurrence_counts.py', 'tests/test_occurrence_counts.py', 'tests/test_wave1_frequency.py', DESIGN,
    *(f'src/methods/{f}/{n}' for f in ('E_007', 'E_008', 'E_009', 'E_010')
      for n in ('__init__.py', 'variants.py', 'contract.py', 'IN_DEVELOPMENT.txt')),
    *(f'{CD}{kind}/{g}/{m}/{v}/{leaf}' for kind, leaf in (('declarations', 'r1.json'), ('registry', 'entry_0001.json'))
      for g in ('POWERBALL', 'OZLOTTO') for m in VARIANTS for v in VARIANTS[m]),
}
REPLACED = {'src/methods/Method_Contract_Runner.py', 'doc/METHOD_TEMPLATE/README.md',
            'doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md', 'doc/METHOD_TEMPLATE/method_folder/contract.py.txt'}
GUARDED_PATHS = [
    'doc/RATIFICATION_REGISTER_v0_17.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r5.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md',
    'doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md', 'src/methods/_common/polynomial_fits.py',
    'src/methods/E_003/contract.py', 'src/methods/E_004/contract.py', 'tests/test_e3_e4_polynomial.py',
    'doc/METHOD_TEMPLATE/method_folder/model.py.txt', 'doc/METHOD_TEMPLATE/test_template.py.txt',
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
    'tests/test_e2r_dispatch.py', 'tests/test_e6_beta_bernoulli.py',
    f'{CD}registry/POWERBALL/E_7/NOT_YET_SPECIFIED/entry_0001.json',
    f'{CD}registry/OZLOTTO/E_10/NOT_YET_SPECIFIED/entry_0001.json',
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
files[f'review/{PKG}/replaced_files_base_to_v1.diff'] = diffs.encode('ascii')
for name in ('suite_py313.txt', 'suite_py315.txt', 'mutations_py313.txt', 'template_trial_v2.txt'):
    files[f'review/{PKG}/{name}'] = (HERE / 'ev' / name).read_bytes()
for name in ('w1_mutations.py', 'make_wave1_contract_data.py', 'write_wave1_methods.py', 'template_trial_v2.py'):
    files[f'review/{PKG}/tools/{name}'] = (HERE / 'tools' / name).read_bytes()
for name in ('reference_wave1_examples.py', 'make_template_draft2.py', 'make_template_draft2_code.py'):
    files[f'review/{PKG}/tools/{name}'] = (HERE / name).read_bytes()
files['doc/RATIFICATION_REGISTER_v0_18.md'] = reg.read_bytes()
for name, h in (('Independent_ChatGPT_Wave1_R3_and_Template_Draft2_Review_v0_1.md', '76818fab4d16988ea89a0e52b55c42ada46163e5d10da288a4b558285aad1a21'),
                ('Independent_ChatGPT_Wave1_v0_1r1_Focused_RECHECK_v0_1.md', '780513e0b1f36ac1981f5b2e6476b985bec266a8ee01fa0fd2fb49b70d81763a')):
    files[f'review/{name}'] = Path(f'/home/claude/work/reg18/{name}').read_bytes()
    assert hashlib.sha256(files[f'review/{name}']).hexdigest() == h, name
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
man = ('# Wave 1 package installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file\n' +
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
(out / 'VERIFY_W1_INSTALL.py').write_bytes(v.encode('ascii'))
shutil.copy(HERE / 'RUN_W1_SUITE.py', out / 'RUN_W1_SUITE.py')
_expected = next(n.value for n in ast.parse((HERE / 'RUN_W1_SUITE.py').read_text()).body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED')
SUITE_N = sum(c for _m, c in ast.literal_eval(_expected))
TOTAL = len(NEW) + len(MOD)
P = rf'E:\TEMP\{PKG}'
instr = f"""# Wave 1 package v1 - E_7, E_8, E_9 and E_10 revision 1 with their shared helper, installed non-runnable; the template's draft 2; register v0.18 (only after the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\W1_Install_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files and replaces {len(MOD)} existing files (`{"`, `".join(sorted(MOD))}`); nothing else changes. The four methods are installed **non-runnable**: every request is refused until a separate release package.

## 1. Update, check, copy, check, and the tests (one block; do not skip the last command)

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_W1_INSTALL.py" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_W1_INSTALL.py" --repo . --phase post
.venv\\Scripts\\python.exe "{P}\\RUN_W1_SUITE.py" --repo .
```

Expected: `git status --short` prints nothing (if it prints anything, stop and send Claude the output); the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; `POST PASS`; then `SUITE PASS` ({SUITE_N} tests; the only allowed skips are symlink tests: on Windows without symlink rights, up to 3). E2R-T12 starts up to six ordinary Python worker processes and lets them finish normally. The tests change nothing in the repository. If anything prints `STOP` or `FAILED`, do not commit: send Claude the output.

## 2. Stage, commit, check, and only then push

```bat
git add doc review src tests
git status --short
git commit -m "Wave 1: E_7, E_8, E_9 and E_10 revision 1 with the shared counting helper (installed non-runnable), the template's draft 2 and register v0.18"
python "{P}\\VERIFY_W1_INSTALL.py" --repo . --phase committed
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
print(len(NEW), 'new files and', len(MOD), 'replaced; suite', SUITE_N, '; base', BASE)
