"""Build step 1 (the folder layout): the builder of the install package for the owner's clone.

What this file is for
    It makes the package the owner installs: the overlay of new and changed files, the list of files to delete,
    the read-only verifier (from the project's reviewed template, exchange/CLAUDE_WEB_TOOLS/wf1/
    verifier_template.py), the three tools the run sheet uses, the manifest, and the install and run sheet.
    Everything is derived from one fresh clone at the base commit, changed by make_step1_layout.py: nothing is
    typed by hand, and every count in the instructions comes from the files.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3, phase 1; the install order is
    doc/HANDOVER/Claude_Primary_Handover_H1_v8.md section 1.6 ("Code packages").

Which of the project's own modules it uses
    None. It runs make_step1_layout.py (beside this file) and reads the verifier template as text.

What uses it
    Claude, in the cloud workspace. Usage:  python build_step1_pkg.py <repository clone> <base commit> <out folder>
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- constants

HERE = Path(__file__).resolve().parent                       # exchange/CLAUDE_WEB_TOOLS/step1
VERIFIER_TEMPLATE = HERE.parent / 'wf1' / 'verifier_template.py'   # the reviewed read-only verifier

PACKAGE_NAME = 'STEP1_Layout_Install_v1'
PACKAGE_TITLE = 'build step 1 package (the folder layout; specification 17.3 phase 1)'
VERIFIER_NAME = 'VERIFY_STEP1_INSTALL.py'
SHEET_NAME = 'INSTALL_AND_RUN_SHEET.md'
DELETE_LIST_NAME = 'DELETE_PATHS.txt'
MANIFEST_NAME = 'INSTALL_MANIFEST_SHA256.txt'

# The tools the run sheet uses, copied into the package so that their bytes are fixed with it.
TOOLS = ('run_suite.py', 'compare_suite_reports.py', 'check_layout_equivalence.py')

# Where the owner extracts the package and keeps the evidence: his download folder, never the repository.
OWNER_PACKAGE_FOLDER = rf'E:\TEMP\{PACKAGE_NAME}'
OWNER_EVIDENCE_FOLDER = r'E:\TEMP\STEP1_evidence'

COMMIT_MESSAGE = ('BUILD STEP 1: the folder layout (specification 17.3 phase 1): method files to the family and '
                  'variant layout, shared helpers to _shared, the runner table built from the folder tree')

# Files that the package must leave byte-identical in Git: the data, and the code every forecast passes through.
GUARDED_PATHS = (
    'source_data/POWERBALL_results_master.csv', 'source_data/POWERBALL_results_master_ledger.csv',
    'source_data/POWERBALL_results_master_init_verification.json', 'source_data/HOLDOUT_OPENED_POWERBALL.json',
    'source_data/OZLOTTO_results_master.csv', 'source_data/OZLOTTO_results_master_ledger.csv',
    'source_data/OZLOTTO_results_master_init_verification.json', 'source_data/HOLDOUT_OPENED_OZLOTTO.json',
    'src/methods/_common/game_draws_reader.py', 'src/methods/_common/game_profiles.py',
    'src/methods/_common/contract_forecast.py', 'src/methods/_common/contract_records.py',
    'src/methods/_common/contract_task.py', 'src/methods/_common/contract_runner.py',
    'src/methods/_common/contract_dispatch.py', 'src/methods/_common/contract_registry.py',
    'src/methods/_common/walk_forward.py', 'src/methods/_common/master_versions.py',
    'src/methods/_common/closure.py', 'src/methods/E_006/beta_bernoulli.py', 'src/methods/E_001/multigame_e1.py',
    'src/Powerball_Experiment_Coordinator.py', 'src/results_master_v0_2.py', '.gitattributes', '.gitignore',
)


def sha256_of(data: bytes) -> str:
    """Return the SHA-256 of some bytes as 64 hexadecimal characters, for example 'e3b0c442...b855'."""
    return hashlib.sha256(data).hexdigest()


def git(tree: Path, *arguments: str) -> bytes:
    """Run one Git command in a tree and return its output bytes. Refuses (an exception) if Git fails."""
    return subprocess.run(['git', '-C', str(tree), *arguments], check=True, capture_output=True).stdout


def sheet_text(base: str, new_count: int, modified_count: int, deleted_count: int, moved_count: int) -> str:
    """Write the owner's install and run sheet.

    base: the base commit's full ID.  The four counts come from the package's own lists.
    Returns the sheet as text with LF line endings (the caller converts to CRLF), for example beginning
    '# STEP1_Layout_Install_v1 - build step 1 package ...'.
    """
    p, ev = OWNER_PACKAGE_FOLDER, OWNER_EVIDENCE_FOLDER
    py = r'.venv\Scripts\python.exe'
    added_lines = new_count - moved_count
    return f"""# {PACKAGE_NAME} - {PACKAGE_TITLE}: install and run sheet

**Only after the owner's own go for each part.** Windows CMD, in the repository root
(`E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality`). Nothing of the project running.
**Save the ZIP to `E:\\TEMP`, not into the repository,** delete any earlier `{p}` folder, and extract it so that
`{p}\\{VERIFIER_NAME}` exists. Base commit: `{base}`.

**A STOP is a STOP.** If any step prints `STOP`, `FAIL`, an error, or anything other than what is expected: do not
go on, do not retry, do not reset or undo anything. Send Claude the whole output.

Nothing here contacts a lottery website, changes the PC's date or time, or ends a process. The suite and the
equivalence check read the results masters and the old records; they write only under `{ev}`
(the suite's reports) and Python's own temporary folders.

## Part 0. Your own ZIP of the project folder (before anything else)

Make one full ZIP of the whole project folder on E: by hand, with `.git` and the old run folders included
(`.venv` is your choice). Keep it off E:. Open it once to see that it reads. **It is the only other copy of the
old forecast records that Git does not track, and it is the way back to the old system** (specification 17.2).

## Part 1. Update, and the suite as it is today (the baseline; about 25 minutes)

```bat
git status --short
git pull --ff-only
{py} -B "{p}\\tools\\run_suite.py" . "{ev}\\suite_before"
git status --short
```

Expected: the first `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; one
line for each test module, some of them `FAILED` (two modules are known to fail today; that is the baseline, not a
STOP); a last line `DONE: 45 modules, ... tests ran`; and the second `git status --short` prints nothing.

## Part 2. Check, copy, delete, check

```bat
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase pre
xcopy "{p}\\repo_overlay\\*" . /E /Y
git rm -q --pathspec-from-file="{p}\\{DELETE_LIST_NAME}"
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase post
```

Expected: `PRE PASS`; `{new_count + modified_count} File(s) copied`; the `git rm` prints nothing; `POST PASS`.
(The {moved_count} moved files arrive at their new paths in the overlay and leave their old paths in the `git rm`.)

## Part 3. The same suite again, and the comparison (about 25 minutes)

```bat
{py} -B "{p}\\tools\\run_suite.py" . "{ev}\\suite_after"
{py} -B "{p}\\tools\\compare_suite_reports.py" "{ev}\\suite_before" "{ev}\\suite_after"
```

Expected, from the comparison: `tests before: N; after: N; same result: N` with one number three times; perhaps
some lines `FAILS IN BOTH RUNS` (the known failures; the words `FAILURE LINES DIFFER` on `test_gitignore_lines` are
expected, because that test prints a set in a different order each run); **no line beginning `CHANGED`,
`DISAPPEARED` or `NEW`;** and
the last line `RESULT: no test changed its result, disappeared or appeared`. Any other result is a STOP.

## Part 4. The equivalence check (reads only; about 30 to 60 minutes; leave the window alone)

```bat
{py} -B "{p}\\tools\\check_layout_equivalence.py" --tree .
```

It computes every old development forecast again with the moved code, in memory, and compares content digests.
Expected: for each game a line `old development forecasts found: ...` (on this PC the count "in old run folders"
should be well above zero); one line for each variant, `n of n equal`; and the last line
**`RESULT: PASS - every old development forecast found was computed again ... the same content digest.`**
A line beginning `DIFFERENT` or `FAILED`, or `RESULT: STOP`, is a STOP: change nothing and send Claude the output.
(Optional, to save time: four CMD windows, each with the same command and one of `--part 1/4`, `--part 2/4`,
`--part 3/4`, `--part 4/4`. Each then ends `RESULT: PARTIAL`; all four must end so, with no `DIFFERENT` or `FAILED`.)

## Part 5. Stage, commit, check, and only then push

```bat
git add src tests
git status --short
git commit -m "{COMMIT_MESSAGE}"
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase committed
```

Expected: `git status --short` lists {moved_count} lines starting with `R` (moved), {added_lines} starting with `A`,
{modified_count} starting with `M` and {deleted_count - moved_count} starting with `D`, and nothing else; then
`COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings are harmless.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

## Part 6. What to send Claude

The commit ID; the text of the comparison (part 3) and of the equivalence check (part 4), copied from the
window; and, if anything was unexpected, the folder `{ev}`. Claude then verifies the commit from GitHub.
"""


def main() -> int:
    """Build the package in the out folder; print its counts; return 0."""
    repository, base, out_folder = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    base = git(repository, 'rev-parse', base).decode().strip()
    with tempfile.TemporaryDirectory() as temporary:
        dev = Path(temporary) / 'dev'
        subprocess.run(['git', 'clone', '-q', str(repository), str(dev)], check=True)
        git(dev, 'checkout', '-q', base)
        subprocess.run([sys.executable, '-B', '-I', str(HERE / 'make_step1_layout.py'), str(dev)], check=True)
        new, modified, deleted = {}, {}, {}
        for line in git(dev, 'diff', '--cached', '--no-renames', '--name-status').decode().splitlines():
            status, path = line.split('\t')
            assert path.startswith(('src/', 'tests/')), f'a change outside src/ and tests/: {path}'
            if status == 'D':
                deleted[path] = sha256_of(git(dev, 'show', f'{base}:{path}'))
                continue
            content = (dev / path).read_bytes()
            assert b'\r' not in content, f'CR in {path}'
            if status == 'A':
                new[path] = content
            else:
                assert status == 'M', line
                modified[path] = (sha256_of(git(dev, 'show', f'{base}:{path}')), content)
        moved_count = sum(1 for line in git(dev, 'diff', '--cached', '-M', '--name-status').decode().splitlines()
                          if line.startswith('R'))

    if out_folder.exists():
        shutil.rmtree(out_folder)
    overlay = out_folder / 'repo_overlay'
    for path, content in list(new.items()) + [(p, c) for p, (_old, c) in modified.items()]:
        (overlay / path).parent.mkdir(parents=True, exist_ok=True)
        (overlay / path).write_bytes(content)
    (out_folder / DELETE_LIST_NAME).write_bytes(('\n'.join(sorted(deleted)) + '\n').encode('ascii'))
    (out_folder / 'tools').mkdir()
    for tool in TOOLS:
        (out_folder / 'tools' / tool).write_bytes((HERE / tool).read_bytes())

    manifest = (f'# {PACKAGE_NAME} installation manifest (Git-content SHA-256, LF); base {base}\n'
                '# "A" new path, "M" modified file (with its base hash), "D" deleted path (its base hash)\n'
                + ''.join(f'A {sha256_of(c)}  {p}\n' for p, c in sorted(new.items()))
                + ''.join(f'M {sha256_of(c)}  {p}  (base {old})\n' for p, (old, c) in sorted(modified.items()))
                + ''.join(f'D {old}  {p}\n' for p, old in sorted(deleted.items())))
    (out_folder / MANIFEST_NAME).write_bytes(manifest.encode('ascii'))

    guarded = {p: sha256_of(git(repository, 'show', f'{base}:{p}')) for p in GUARDED_PATHS}
    verifier = VERIFIER_TEMPLATE.read_text(encoding='ascii')
    for mark, text in (
            ('@@NEW@@', '\n'.join(f"    '{p}': '{sha256_of(c)}'," for p, c in sorted(new.items()))),
            ('@@MODIFIED@@', '\n'.join(f"    '{p}': ('{old}', '{sha256_of(c)}')," for p, (old, c) in sorted(modified.items()))),
            ('@@DELETED@@', '\n'.join(f"    '{p}': '{old}'," for p, old in sorted(deleted.items()))),
            ('@@GUARDED@@', '\n'.join(f"    '{p}': '{h}'," for p, h in guarded.items())),
            ('@@BASE@@', base), ('@@N@@', str(len(new))), ('@@M@@', str(len(modified))), ('@@D@@', str(len(deleted))),
            ('@@TITLE@@', PACKAGE_TITLE), ('@@VERIFIER@@', VERIFIER_NAME)):
        verifier = verifier.replace(mark, text)
    assert '@@' not in verifier
    (out_folder / VERIFIER_NAME).write_bytes(verifier.encode('ascii'))

    sheet = sheet_text(base, len(new), len(modified), len(deleted), moved_count)
    (out_folder / SHEET_NAME).write_bytes(sheet.replace('\n', '\r\n').encode('ascii'))
    print(f'{PACKAGE_NAME}: {len(new)} new paths, {len(modified)} modified, {len(deleted)} deleted '
          f'({moved_count} of them moves); base {base}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
