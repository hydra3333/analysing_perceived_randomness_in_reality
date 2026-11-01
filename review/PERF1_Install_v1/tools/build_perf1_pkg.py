"""Build the PERF-1 installation package (Claude, 1 Nov 2026): the faster exact binomial sum and Clopper-Pearson
interval (identical results) and the report tool's progress lines.

Usage: python3 -I build_perf1_pkg.py DEV_TREE BASE_TREE OUTDIR BASE_COMMIT
DEV_TREE = BASE_TREE + PERF-1. Every file in DEV_TREE that differs from BASE_TREE must be an expected new file or an
allowed replacement. Evidence and tools come from this folder.
"""
import ast, difflib, hashlib, shutil, subprocess, sys
from pathlib import Path

dev, base, outdir, BASE = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
HERE = Path(__file__).resolve().parent
WH = Path('/home/claude/work/wf1code')
REPO = '/home/claude/analysing_perceived_randomness_in_reality'
PKG, TITLE = 'PERF1_Install_v1', 'PERF-1 package (faster exact Clopper-Pearson intervals with identical results; report progress lines)'
REPLACED = {'src/evaluation/numerics.py', 'src/evaluation/report.py', 'src/evaluation/Method_Rankings_Report.py'}
EVAL_TESTS = ('test_wf1b_numerics', 'test_wf1b_n1_generator', 'test_wf1b_divisions', 'test_wf1b_measures',
              'test_wf1b_outcome_reader', 'test_wf1b_report', 'test_wf1b_static', 'test_wf1b_crossplatform',
              'test_wf1b_seed_policy', 'test_wf1b_n1_replay', 'test_perf1_numerics')
NEW_TESTS = ('test_perf1_numerics',)
CRLF_OK = set()
WHAT = ('Makes the exact Clopper-Pearson interval fast (the same float64 results) and adds the ranking report '
        "tool's progress lines; adds one test module.")
COMMIT = ('PERF-1: faster exact binomial sums and Clopper-Pearson intervals (identical results) and progress lines '
          'for the ranking report tool')
GIT_ADD = 'git add review src tests'
GUARDED_PATHS = [
    'src/evaluation/n1.py', 'src/evaluation/n1_generator.py', 'src/evaluation/measures.py',
    'src/evaluation/divisions.py', 'src/evaluation/collect.py', 'src/evaluation/outcome_reader.py',
    'src/evaluation/report_writer.py', 'src/evaluation/seed_policies.py',
    'src/evaluation/registry/MEASURE_REGISTRY_V1.json', 'src/evaluation/registry/FAMILY_REGISTRY_V1.json',
    'src/evaluation/seed_policies/N1_ROOT_NIST_C2_20261031T1030Z_V1.json',
    'src/evaluation/seed_policies/N1_ROOT_NIST_C2_20261106T0000Z_V1.json',
    'src/methods/_common/walk_forward.py', 'src/methods/_common/contract_runner.py',
    'src/methods/_common/game_draws_reader.py', 'src/methods/_common/game_profiles.py',
    'src/methods/_common/contract_publication.py', 'src/methods/_common/contract_records.py',
    'src/Powerball_Experiment_Coordinator.py', 'Run_Method_Rankings.bat', 'Run_Experiment.bat', 'Run_Coordinator.bat',
    '.gitignore', 'doc/Predictive_Randomness_WF1B_Supplement_Design_v0_1r1.md',
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def lf(b):
    return b.replace(b'\r\n', b'\n')


def tracked(t):
    return {p.relative_to(t).as_posix(): p for p in t.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}


d, b = tracked(dev), tracked(base)
for p in b:
    assert p in d, f'missing in dev tree: {p}'
    if p not in REPLACED:
        assert d[p].read_bytes() == b[p].read_bytes(), f'existing file changed: {p}'
new = set(d) - set(b)
expected_new = {f'tests/{m}.py' for m in NEW_TESTS}
assert new == expected_new, sorted(new ^ expected_new)
for p in REPLACED:
    assert d[p].read_bytes() != b[p].read_bytes(), f'replacement not changed: {p}'
files = {p: d[p].read_bytes() for p in sorted(new)}
overlay_bytes = dict(files)
diffs = ''.join(''.join(difflib.unified_diff(b[p].read_text().splitlines(True), d[p].read_text().splitlines(True),
                                             f'a/{p}', f'b/{p}')) for p in sorted(REPLACED))
extra = {f'review/{PKG}/replaced_files_base_to_perf1.diff': diffs.encode('ascii')}
for f in sorted((HERE / 'ev').glob('*.txt')):
    extra[f'review/{PKG}/{f.name}'] = f.read_bytes()
for f in sorted((HERE / 'tools').glob('*.py')):
    extra[f'review/{PKG}/tools/{f.name}'] = f.read_bytes()
extra[f'review/{PKG}/tools/build_perf1_pkg.py'] = Path(__file__).read_bytes()
for f in sorted((HERE / 'docs').glob('*.md')):
    extra[f'doc/{f.name}'] = f.read_bytes()
for f in sorted((HERE / 'docs' / 'review').glob('*.md')):
    extra[f'review/{f.name}'] = f.read_bytes()
files.update(extra)
overlay_bytes.update(extra)
replaced = {p: d[p].read_bytes() for p in REPLACED}
for p, raw in [*files.items(), *replaced.items()]:
    if p in CRLF_OK:
        assert raw.isascii() and b'\r\n' in raw, p
        files[p] = lf(raw)                         # the Git blob (.gitattributes: *.bat text eol=crlf)
        continue
    assert b'\r' not in raw, p
    assert raw.isascii(), p
for p in files:
    assert p not in b, f'not a new path: {p}'
    r = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', f'{BASE}:{p}'], capture_output=True)
    assert r.returncode != 0, f'already in the base commit: {p}'

if outdir.exists():
    shutil.rmtree(outdir)
ov = outdir / 'repo_overlay'
for p, raw in [*overlay_bytes.items(), *replaced.items()]:
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(raw)
mp = f'review/{PKG}/INSTALL_MANIFEST_SHA256.txt'
man = (f'# {PKG} installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file\n' +
       ''.join(f'A {sha(raw)}  {p}\n' for p, raw in sorted(files.items())) +
       ''.join(f'M {sha(raw)}  {p}  (base {sha(b[p].read_bytes())})\n' for p, raw in sorted(replaced.items())))
(ov / mp).write_bytes(man.encode('ascii'))
files[mp] = man.encode('ascii')
NEW = {p: sha(raw) for p, raw in files.items()}
MOD = {p: (sha(b[p].read_bytes()), sha(raw)) for p, raw in replaced.items()}
guarded = {p: sha(subprocess.run(['git', '-C', REPO, 'show', f'{BASE}:{p}'], capture_output=True, check=True).stdout)
           for p in GUARDED_PATHS}
VERIFIER, RUNNER = 'VERIFY_PERF1_INSTALL.py', 'RUN_PERF1_SUITE.py'
v = (WH / 'verifier_template.py').read_text()
v = (v.replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEW.items())))
      .replace('@@MODIFIED@@', '\n'.join(f"    '{p}': ('{o}', '{n}')," for p, (o, n) in sorted(MOD.items())))
      .replace('@@DELETED@@', '').replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in guarded.items()))
      .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEW))).replace('@@M@@', str(len(MOD)))
      .replace('@@D@@', '0').replace('@@TITLE@@', TITLE).replace('@@VERIFIER@@', VERIFIER))
assert '@@' not in v
(outdir / VERIFIER).write_bytes(v.encode('ascii'))
counts = {m: n for m, n in ast.literal_eval((HERE / 'test_counts.txt').read_text())}
extra_runner = ''.join(f"    ('tests.{m}', {counts[m]}),\n" for m in EVAL_TESTS)
r = (WH / 'suite_template.py').read_text().replace('@@EXTRA@@', "    ('tests.test_wf1a_walk_forward', 22), "
                                                    "('tests.test_code3_retirement', 11), ('tests.test_e1r2_revision2', 13),\n" + extra_runner)
_expected = next(n.value for n in ast.parse(r).body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED')
SUITE_N = sum(c for _m, c in ast.literal_eval(_expected))
r = r.replace('@@PKG@@', PKG).replace('@@TOTAL@@', str(SUITE_N)).replace('@@WHAT@@', WHAT).replace('@@RUNNER@@', RUNNER)
assert '@@' not in r
(outdir / RUNNER).write_bytes(r.encode('ascii'))
TOTAL = len(NEW) + len(MOD)
P = rf'E:\TEMP\{PKG}'
instr = f"""# {PKG} - {TITLE} (only after the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\PERF1_Install_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}_candidate.zip" -C E:\\TEMP`). This package adds {len(NEW)} new files and replaces {len(MOD)} existing files (`src/evaluation/numerics.py`, `report.py` and `Method_Rankings_Report.py`); nothing else changes. It runs no report. Your working tree must be clean first: commit or settle any report results before you start.

## 1. Update, check, copy, check, and the tests (one block; do not skip the last command)

```bat
git status --short
git pull --ff-only
python "{P}\\{VERIFIER}" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\{VERIFIER}" --repo . --phase post
.venv\\Scripts\\python.exe "{P}\\{RUNNER}" --repo .
```

Expected: `git status --short` prints nothing (if it prints anything, stop and send Claude the output); the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; `POST PASS`; then `SUITE PASS` ({SUITE_N} tests; the only allowed skips are symlink tests: on Windows without symlink rights, up to 4). E2R-T12 starts up to six ordinary Python worker processes and lets them finish normally. The WF-1B and PERF-1 tests run on invented data in temporary folders, with an invented N1 root. If anything prints `STOP` or `FAILED`, do not commit: send Claude the output.

## 2. Stage, commit, check, and only then push

```bat
{GIT_ADD}
git status --short
git commit -m "{COMMIT}"
python "{P}\\{VERIFIER}" --repo . --phase committed
```

Expected: `git status --short` lists {len(NEW)} lines starting with `A` and {len(MOD)} starting with `M`, and nothing else; then `COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings while staging are normal.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub.
"""
(outdir / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(PKG, len(NEW), 'A', len(MOD), 'M; suite', SUITE_N, '; base', BASE)
