"""Build the wave 2 installation package (E_2, E_17, E_18, E_19; Claude, 30 Oct 2026). New files plus three whole-file
replacements (the runner's ADAPTERS list and two template files, which become draft 3).

Usage: python3 -I build_w1_install.py DEV_TREE BASE_TREE OUTDIR BASE_COMMIT REGISTER
DEV_TREE: the base checkout plus the wave 2 files; BASE_TREE: a checkout of BASE_COMMIT (main after the wave 1
installation 947c370 and the exchange records up to EX_073). Every file in DEV_TREE that differs from BASE_TREE must
be one of the expected new files or one of the three allowed replacements. REGISTER is register v0.19 (candidate or
final), installed with the package as doc/RATIFICATION_REGISTER_v0_19.md, together with the LF copies of the EX_066,
EX_069, EX_071 and EX_073 reviews.
"""
import ast, difflib, hashlib, shutil, sys
from pathlib import Path

dev, base, outdir = map(Path, sys.argv[1:4])
BASE = sys.argv[4]
reg = Path(sys.argv[5])
HERE = Path(__file__).resolve().parent
PKG = 'W2_Install_v1'
VARIANTS = {'E_2': ('RECUR_MEAN_ALL_V1', 'RECUR_MEDIAN_ALL_V1', 'RECUR_MEAN_LAST8_V1'),
            'E_17': ('HAZARD_BINS_C100_V1', 'HAZARD_BINS_W208_C100_V1', 'HAZARD_LOGAGE_SIGN_V1'),
            'E_18': ('MIX4_ALL_C10_V1', 'MIX4_W208_C10_V1', 'MIX4_W104_C10_V1'),
            'E_19': ('PERIODIC_T2_V1', 'PERIODIC_T3_V1', 'PERIODIC_T4_V1')}
CD = 'src/methods/_common/contract_data/'
DESIGN = 'doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md'
NEW_EXPECTED = {
    'src/methods/_common/recurrence_gaps.py', 'tests/test_recurrence_gaps.py', 'tests/test_wave2_recurrence.py', DESIGN,
    *(f'src/methods/{f}/{n}' for f in ('E_002', 'E_017', 'E_018', 'E_019')
      for n in ('__init__.py', 'variants.py', 'contract.py', 'IN_DEVELOPMENT.txt')),
    *(f'{CD}{kind}/{g}/{m}/{v}/{leaf}' for kind, leaf in (('declarations', 'r1.json'), ('registry', 'entry_0001.json'))
      for g in ('POWERBALL', 'OZLOTTO') for m in VARIANTS for v in VARIANTS[m]),
}
REPLACED = {'src/methods/Method_Contract_Runner.py', 'doc/METHOD_TEMPLATE/README.md',
            'doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md'}
GUARDED_PATHS = [
    'doc/RATIFICATION_REGISTER_v0_18.md', 'doc/RATIFICATION_REGISTER_v0_17.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r5.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md',
    'doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md', 'src/methods/_common/polynomial_fits.py',
    'src/methods/E_003/contract.py', 'src/methods/E_004/contract.py', 'tests/test_e3_e4_polynomial.py',
    'doc/METHOD_TEMPLATE/method_folder/model.py.txt', 'doc/METHOD_TEMPLATE/test_template.py.txt',
    'doc/METHOD_TEMPLATE/method_folder/contract.py.txt', 'doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md',
    'src/methods/_common/occurrence_counts.py', 'src/methods/E_007/contract.py', 'src/methods/E_008/contract.py',
    'src/methods/E_009/contract.py', 'src/methods/E_010/contract.py', 'src/methods/E_010/IN_DEVELOPMENT.txt',
    'tests/test_occurrence_counts.py', 'tests/test_wave1_frequency.py',
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
    f'{CD}registry/POWERBALL/E_2/NOT_YET_SPECIFIED/entry_0001.json',
    f'{CD}registry/OZLOTTO/E_19/NOT_YET_SPECIFIED/entry_0001.json',
    f'{CD}registry/POWERBALL/E_7/BETA_SHRINK_W52_C52_V1/entry_0001.json',
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
for name in ('suite_py313.txt', 'suite_py315.txt', 'mutations_py313.txt', 'template_trial_v3.txt'):
    files[f'review/{PKG}/{name}'] = (HERE / 'ev' / name).read_bytes()
for name in ('w2_mutations.py', 'make_wave2_contract_data.py', 'write_wave2_methods.py', 'edit_runner.py', 'template_trial_v3.py'):
    files[f'review/{PKG}/tools/{name}'] = (HERE / 'tools' / name).read_bytes()
for name in ('reference_wave2.py', 'make_template_draft3.py'):
    files[f'review/{PKG}/tools/{name}'] = (HERE / name).read_bytes()
files[f'review/{PKG}/design_probes_v0_1r2.txt'] = (HERE / 'ev' / 'design_probes_v0_1r2.txt').read_bytes()
files['doc/RATIFICATION_REGISTER_v0_19.md'] = reg.read_bytes()
EXCH = Path('/home/claude/analysing_perceived_randomness_in_reality/exchange')
for ex, name, h in (('EX_066_ChatGPT', 'Independent_ChatGPT_Wave1_R2_and_Register_v18_Review_v0_1.md', 'baf0914044f88ef5162ed6d71d7f5f0dc5d93f6f7e33f1dfa8af5541c38ffa90'),
                    ('EX_069_ChatGPT', 'Independent_ChatGPT_Wave2_R3_Review_v0_1.md', '75ec652caf27c1db5594625bbc0ad4b0f587ffc233e59c68bc25695841913c51'),
                    ('EX_071_ChatGPT', 'Independent_ChatGPT_Wave2_v0_1r1_R3_RECHECK_v0_1.md', '64a48a8cb91633fad3027860fd6ff2ca770d35a88040f936404294dbc2ade56a'),
                    ('EX_073_ChatGPT', 'Independent_ChatGPT_Wave2_v0_1r2_Focused_RECHECK_v0_1.md', 'e5b5116be5448601d82eba27fb4efcd86fa3c6400a762a9ea275ece474ef2305')):
    files[f'review/{name}'] = (EXCH / ex / name).read_bytes().replace(b'\r\n', b'\n')
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
man = ('# Wave 2 package installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file\n' +
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
(out / 'VERIFY_W2_INSTALL.py').write_bytes(v.encode('ascii'))
shutil.copy(HERE / 'RUN_W2_SUITE.py', out / 'RUN_W2_SUITE.py')
_expected = next(n.value for n in ast.parse((HERE / 'RUN_W2_SUITE.py').read_text()).body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED')
SUITE_N = sum(c for _m, c in ast.literal_eval(_expected))
TOTAL = len(NEW) + len(MOD)
P = rf'E:\TEMP\{PKG}'
instr = f"""# Wave 2 package v1 - E_2, E_17, E_18 and E_19 revision 1 with their shared helper, installed non-runnable; the template's draft 3; register v0.19 (only after the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\W2_Install_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files and replaces {len(MOD)} existing files (`{"`, `".join(sorted(MOD))}`); nothing else changes. The four methods are installed **non-runnable**: every request is refused until a separate release package.

## 1. Update, check, copy, check, and the tests (one block; do not skip the last command)

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_W2_INSTALL.py" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_W2_INSTALL.py" --repo . --phase post
.venv\\Scripts\\python.exe "{P}\\RUN_W2_SUITE.py" --repo .
```

Expected: `git status --short` prints nothing (if it prints anything, stop and send Claude the output); the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; `POST PASS`; then `SUITE PASS` ({SUITE_N} tests; the only allowed skips are symlink tests: on Windows without symlink rights, up to 3). E2R-T12 starts up to six ordinary Python worker processes and lets them finish normally. The tests change nothing in the repository. If anything prints `STOP` or `FAILED`, do not commit: send Claude the output.

## 2. Stage, commit, check, and only then push

```bat
git add doc review src tests
git status --short
git commit -m "Wave 2: E_2, E_17 (Method A), E_18 and E_19 revision 1 with the shared gaps helper (installed non-runnable), the template's draft 3 and register v0.19"
python "{P}\\VERIFY_W2_INSTALL.py" --repo . --phase committed
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
