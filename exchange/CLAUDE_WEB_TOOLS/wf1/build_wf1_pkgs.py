"""Build the REL-1 or the WF-1A installation package (Claude, 31 Oct 2026; releases and WF-1 design v0.1r1).

Usage: python3 -I build_wf1_pkgs.py rel1|wf1a DEV_TREE BASE_TREE OUTDIR BASE_COMMIT
  rel1: DEV_TREE = BASE_TREE + REL-1; BASE_TREE = main at BASE_COMMIT.
  wf1a: DEV_TREE = REL-1 + WF-1A; BASE_TREE = the REL-1 tree; BASE_COMMIT = REL-1's install commit.
Every file in DEV_TREE that differs from BASE_TREE must be an expected new file, an allowed replacement or an
expected deletion. The register, design and review copies (rel1) and the evidence and tools come from this folder.
"""
import ast, difflib, hashlib, shutil, sys
from pathlib import Path

which, dev, base, outdir, BASE = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5]
HERE = Path(__file__).resolve().parent
CD = 'src/methods/_common/contract_data/'
RELEASED = {'E_2': ('RECUR_MEAN_ALL_V1', 'RECUR_MEDIAN_ALL_V1', 'RECUR_MEAN_LAST8_V1'),
            'E_3': None, 'E_4': None, 'E_6': None, 'E_7': None, 'E_8': None, 'E_9': None, 'E_10': None,
            'E_17': None, 'E_18': None, 'E_19': None}
FLAGS = {f'src/methods/E_{int(m[2:]):03d}/IN_DEVELOPMENT.txt' for m in RELEASED}

if which == 'rel1':
    PKG, TITLE = 'REL1_Install_v2', 'REL-1 package (release of the 39 variants of the 11 installed methods, both games)'
    entries = {p.relative_to(dev).as_posix() for p in (dev / CD / 'registry').rglob('entry_0002.json')}
    NEW_EXPECTED = entries | {'tests/test_rel1_release.py'}
    REPLACED = {f'tests/{n}.py' for n in ('test_e6_beta_bernoulli', 'test_e3_e4_polynomial', 'test_wave1_frequency',
                                          'test_wave2_recurrence', 'test_e2r_dispatch')}
    DELETED = FLAGS
    assert len(entries) == 78
    EXTRA_RUNNER = ''
    WHAT = 'Adds tests/test_rel1_release.py (5 tests) and edits five test files\' status expectations.'
    REG = HERE / 'reg'
    extra = {'doc/Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md': REG / 'Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md',
             'doc/RATIFICATION_REGISTER_v0_21.md': REG / 'RATIFICATION_REGISTER_v0_21.md',
             'review/Independent_ChatGPT_WF1_Design_R3_Review_EX078.md': REG / 'Independent_ChatGPT_WF1_Design_R3_Review_EX078.md',
             'review/Independent_ChatGPT_WF1_Design_Focused_RECHECK_EX080.md': REG / 'Independent_ChatGPT_WF1_Design_Focused_RECHECK_EX080.md'}
    ev = ('suite_rel1_py313.txt', 'suite_rel1_py315.txt', 'mutations_rel1_py313.txt')
    tools = ('make_rel1_release.py', 'edit_tests_rel1.py', 'wf1_mutations.py')
    tools_here = ('make_register_v21.py',)
    COMMIT = 'REL-1: release the 39 variants of E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19 (both games); WF-1 design v0.1r1 and register v0.21'
    GIT_ADD = 'git add doc review src tests'
else:
    PKG, TITLE = 'WF1A_Install_v2', 'WF-1A package (the walk-forward driver; the real-development switch turned on)'
    NEW_EXPECTED = {'src/methods/_common/walk_forward.py', 'src/methods/Method_Walk_Forward.py',
                    'tests/test_wf1a_walk_forward.py'}
    REPLACED = {'src/methods/_common/contract_runner.py', 'src/methods/Method_Contract_Runner.py', '.gitignore',
                'tests/test_e2r_runner.py', 'tests/test_e2r_dispatch.py'}
    DELETED = set()
    EXTRA_RUNNER = "    ('tests.test_wf1a_walk_forward', 22),\n"
    WHAT = ('Adds tests/test_wf1a_walk_forward.py (22 tests: synthetic batches in a temporary project folder) and edits '
            'two tests that pinned the real-development switch.')
    extra = {}
    ev = ('suite_wf1a_py313.txt', 'suite_wf1a_py315.txt', 'mutations_wf1a_py313.txt')
    tools = ('edit_tests_wf1a.py', 'wf1_mutations.py')
    tools_here = ()
    COMMIT = 'WF-1A: the walk-forward driver; ENABLE_CONTRACT_REAL_DEVELOPMENT turned on (owner decision WF1-3); real-development runs under results/real/development/'
    GIT_ADD = 'git add .gitignore review src tests'

GUARDED_PATHS = [
    'src/methods/E_001/multigame_e1.py', 'src/methods/E_001/e1_historical_appearance_frequency.py',
    'src/methods/E_001_Historical_Appearance_Frequency.py', 'src/methods/contract_adapters/e_001.py',
    'src/methods/_common/game_draws_reader.py', 'src/methods/_common/game_profiles.py',
    'src/methods/_common/contract_dispatch.py', 'src/methods/_common/contract_registry.py',
    'src/methods/_common/contract_publication.py', 'src/methods/_common/contract_receipts.py',
    'src/methods/_common/contract_records.py', 'src/methods/_common/contract_forecast.py',
    'src/methods/_common/contract_task.py', 'src/methods/_common/contract_vocab.py',
    'src/coordinator_private/contract_coordinated_gate.py', 'src/Powerball_Experiment_Coordinator.py',
    'Run_Experiment.bat', 'Run_Coordinator.bat',
    f'{CD}registry/POWERBALL/E_1/FULL_HISTORY_RAW_COUNTS_V1/entry_0001.json',
    f'{CD}registry/OZLOTTO/E_2/NOT_YET_SPECIFIED/entry_0001.json',
    f'{CD}registry/POWERBALL/E_6/BETA_BERNOULLI_FULL_MEMORY_V1/entry_0001.json',
    'doc/RATIFICATION_REGISTER_v0_20.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r6.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md',
    'doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md',
]
if which == 'rel1':
    GUARDED_PATHS += ['src/methods/_common/contract_runner.py', 'src/methods/Method_Contract_Runner.py', '.gitignore']


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tracked(t):
    return {p.relative_to(t).as_posix(): p for p in t.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}


d, b = tracked(dev), tracked(base)
for p in b:
    if p in DELETED:
        assert p not in d, f'not deleted: {p}'
        continue
    assert p in d, f'missing in dev tree: {p}'
    if p not in REPLACED:
        assert d[p].read_bytes() == b[p].read_bytes(), f'existing file changed: {p}'
new = set(d) - set(b)
assert new == NEW_EXPECTED, sorted(new ^ NEW_EXPECTED)
for p in REPLACED:
    assert d[p].read_bytes() != b[p].read_bytes(), f'replacement not changed: {p}'
for p in [*GUARDED_PATHS, *DELETED]:
    assert p in b, f'guarded or deleted path not in base: {p}'
files = {p: d[p].read_bytes() for p in sorted(new)}
diffs = ''.join(''.join(difflib.unified_diff(b[p].read_text().splitlines(True), d[p].read_text().splitlines(True),
                                             f'a/{p}', f'b/{p}')) for p in sorted(REPLACED))
files[f'review/{PKG}/replaced_files_base_to_v1.diff'] = diffs.encode('ascii')
for name in ev:
    files[f'review/{PKG}/{name}'] = (HERE / 'ev' / name).read_bytes()
for name in tools:
    files[f'review/{PKG}/tools/{name}'] = (HERE / 'tools' / name).read_bytes()
for name in tools_here:
    files[f'review/{PKG}/tools/{name}'] = (HERE / name).read_bytes()
for p, src in extra.items():
    files[p] = src.read_bytes()
replaced = {p: d[p].read_bytes() for p in REPLACED}
for p, raw in [*files.items(), *replaced.items()]:
    assert b'\r' not in raw, p
    assert raw.isascii() or p.startswith('doc/RATIFICATION_REGISTER_'), p
for p in files:
    assert p not in b, f'not a new path: {p}'

if outdir.exists():
    shutil.rmtree(outdir)
ov = outdir / 'repo_overlay'
for p, raw in [*files.items(), *replaced.items()]:
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(raw)
mp = f'review/{PKG}/INSTALL_MANIFEST_SHA256.txt'
man = (f'# {PKG} installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file, "D" deleted file\n' +
       ''.join(f'A {sha(raw)}  {p}\n' for p, raw in sorted(files.items())) +
       ''.join(f'M {sha(raw)}  {p}  (base {sha(b[p].read_bytes())})\n' for p, raw in sorted(replaced.items())) +
       ''.join(f'D {sha(b[p].read_bytes())}  {p}\n' for p in sorted(DELETED)))
(ov / mp).write_bytes(man.encode('ascii'))
files[mp] = man.encode('ascii')
NEW = {p: sha(raw) for p, raw in files.items()}
MOD = {p: (sha(b[p].read_bytes()), sha(raw)) for p, raw in replaced.items()}
DEL = {p: sha(b[p].read_bytes()) for p in DELETED}
import subprocess
GIT_REF = 'd15183eccdc9e5d6b7d6322ef2bf57a6bf118b18'   # main before REL-1; guarded files are unchanged by both packages
guarded = {p: sha(subprocess.run(['git', '-C', '/home/claude/analysing_perceived_randomness_in_reality', 'show',
                                  f'{GIT_REF}:{p}'], capture_output=True, check=True).stdout) for p in GUARDED_PATHS}
VERIFIER, RUNNER = f'VERIFY_{PKG.split("_")[0]}_INSTALL.py', f'RUN_{PKG.split("_")[0]}_SUITE.py'

v = (HERE / 'verifier_template.py').read_text()
v = (v.replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEW.items())))
      .replace('@@MODIFIED@@', '\n'.join(f"    '{p}': ('{o}', '{n}')," for p, (o, n) in sorted(MOD.items())))
      .replace('@@DELETED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(DEL.items())))
      .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in guarded.items()))
      .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEW))).replace('@@M@@', str(len(MOD)))
      .replace('@@D@@', str(len(DEL))).replace('@@TITLE@@', TITLE).replace('@@VERIFIER@@', VERIFIER))
assert '@@' not in v
(outdir / VERIFIER).write_bytes(v.encode('ascii'))
r = (HERE / 'suite_template.py').read_text().replace('@@EXTRA@@', EXTRA_RUNNER)
_expected = next(n.value for n in ast.parse(r).body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED')
SUITE_N = sum(c for _m, c in ast.literal_eval(_expected))
r = r.replace('@@PKG@@', PKG).replace('@@TOTAL@@', str(SUITE_N)).replace('@@WHAT@@', WHAT).replace('@@RUNNER@@', RUNNER)
assert '@@' not in r
(outdir / RUNNER).write_bytes(r.encode('ascii'))
TOTAL = len(NEW) + len(MOD)
P = rf'E:\TEMP\{PKG}'
rm = ''
if DEL:
    rm = 'git rm -q -- ' + ' '.join(sorted(DEL)) + '\n'
instr = f"""# {PKG} - {TITLE} (only after the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\{PKG.split('_')[0]}_Install_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files, replaces {len(MOD)} existing files (`{"`, `".join(sorted(MOD))}`){f" and deletes {len(DEL)} files (the `IN_DEVELOPMENT.txt` flags)" if DEL else ""}; nothing else changes.

## 1. Update, check, copy, {"delete, " if DEL else ""}check, and the tests (one block; do not skip the last command)

```bat
git status --short
git pull --ff-only
python "{P}\\{VERIFIER}" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
{rm}python "{P}\\{VERIFIER}" --repo . --phase post
.venv\\Scripts\\python.exe "{P}\\{RUNNER}" --repo .
```

Expected: `git status --short` prints nothing (if it prints anything, stop and send Claude the output); the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; {"the `git rm` line prints nothing; " if DEL else ""}`POST PASS`; then `SUITE PASS` ({SUITE_N} tests; the only allowed skips are symlink tests: on Windows without symlink rights, up to 3). E2R-T12 starts up to six ordinary Python worker processes and lets them finish normally. The tests change nothing in the repository. If anything prints `STOP` or `FAILED`, do not commit: send Claude the output.

## 2. Stage, commit, check, and only then push

```bat
{GIT_ADD}
git status --short
git commit -m "{COMMIT}"
python "{P}\\{VERIFIER}" --repo . --phase committed
```

Expected: `git status --short` lists {len(NEW)} lines starting with `A`, {len(MOD)} starting with `M`{f" and {len(DEL)} starting with `D`" if DEL else ""}, and nothing else; then `COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings while staging are normal.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub. Claude pushes nothing to the repository while you install.
"""
(outdir / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(PKG, len(NEW), 'new,', len(MOD), 'replaced,', len(DEL), 'deleted; suite', SUITE_N, '; base', BASE)
