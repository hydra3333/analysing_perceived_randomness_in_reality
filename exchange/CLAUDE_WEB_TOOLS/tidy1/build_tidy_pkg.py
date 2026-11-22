"""The light tidy-up of the existing method files: the builder of the install package for the owner's clone.

What this file is for
    It makes the package the owner installs: the overlay of the tidied method files, the read-only verifier
    (from the project's reviewed template, exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py), the four tools
    the run sheet uses, the manifest, and the install and run sheet. Everything is derived from one fresh clone
    at the base commit, changed by make_tidy_up.py: nothing is typed by hand, and every count in the
    instructions comes from the files.

Which part of the specification it carries out
    The owner's note of ratification RAT-40, item 3 (decision log entry 147); the install order is
    doc/HANDOVER/Claude_Primary_Handover_H1_v8.md section 1.6 ("Code packages").

Which of the project's own modules it uses
    None. It runs make_tidy_up.py (beside this file) and reads the verifier template as text.

What uses it
    Claude, in the cloud workspace. Usage:  python build_tidy_pkg.py <repository clone> <base commit> <out folder>
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- constants

HERE = Path(__file__).resolve().parent                              # exchange/CLAUDE_WEB_TOOLS/tidy1
STEP1_TOOLS = HERE.parent / 'step1'                                 # the tools reviewed with build step 1
VERIFIER_TEMPLATE = HERE.parent / 'wf1' / 'verifier_template.py'    # the reviewed read-only verifier

PACKAGE_NAME = 'TIDY1_Method_Comments_v1'
PACKAGE_TITLE = 'light tidy-up package (headers and comments of the existing method files; RAT-40 note 3)'
VERIFIER_NAME = 'VERIFY_TIDY1_INSTALL.py'
SHEET_NAME = 'INSTALL_AND_RUN_SHEET.md'
MANIFEST_NAME = 'INSTALL_MANIFEST_SHA256.txt'

# The tools the run sheet uses, copied into the package so that their bytes are fixed with it: {name: its folder}.
# The first three are the tools of build step 1, byte for byte; the fourth is new with this package.
TOOLS = {'run_suite.py': STEP1_TOOLS, 'compare_suite_reports.py': STEP1_TOOLS,
         'check_layout_equivalence.py': STEP1_TOOLS, 'check_comments_only.py': HERE}

# Where the owner extracts the package and keeps the evidence: his download folder, never the repository.
OWNER_PACKAGE_FOLDER = rf'E:\TEMP\{PACKAGE_NAME}'
OWNER_EVIDENCE_FOLDER = r'E:\TEMP\TIDY1_evidence'

COMMIT_MESSAGE = ('LIGHT TIDY-UP (RAT-40 note 3): headers, dependency lists and missing comments in the existing '
                  'method files; no calculation change')

# Files that the package must leave byte-identical in Git: the data, the code every forecast passes through, and
# the six E_1 files that the old archive tests pin (the tidy-up leaves them alone).
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
    'src/methods/_common/closure.py', 'src/methods/_common/method_table.py',
    'src/methods/E_001/__init__.py', 'src/methods/E_001/e1_common_reader_bridge.py',
    'src/methods/E_001/e1_historical_appearance_frequency.py', 'src/methods/E_001/e1_standalone_contract.py',
    'src/methods/E_001/e1_training_view.py', 'src/methods/E_001/multigame_e1.py',
    'src/Powerball_Experiment_Coordinator.py', 'src/results_master_v0_2.py', '.gitattributes', '.gitignore',
)


def sha256_of(data: bytes) -> str:
    """Return the SHA-256 of some bytes as 64 hexadecimal characters, for example 'e3b0c442...b855'."""
    return hashlib.sha256(data).hexdigest()


def git(tree: Path, *arguments: str) -> bytes:
    """Run one Git command in a tree and return its output bytes. Refuses (an exception) if Git fails."""
    return subprocess.run(['git', '-C', str(tree), *arguments], check=True, capture_output=True).stdout


def sheet_text(base: str, modified_count: int) -> str:
    """Write the owner's install and run sheet.

    base: the base commit's full ID.  modified_count: how many files the package replaces (from its own list).
    Returns the sheet as text with LF line endings (the caller converts to CRLF), for example beginning
    '# TIDY1_Method_Comments_v1 - light tidy-up package ...'.
    """
    p, ev = OWNER_PACKAGE_FOLDER, OWNER_EVIDENCE_FOLDER
    py = r'.venv\Scripts\python.exe'
    return f"""# {PACKAGE_NAME} - {PACKAGE_TITLE}: install and run sheet

**Only after the owner's own go for each part.** Windows CMD, in the repository root
(`E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality`). Nothing of the project running.
**Save the ZIP to `E:\\TEMP`, not into the repository,** delete any earlier `{p}` folder, and extract it so that
`{p}\\{VERIFIER_NAME}` exists. Base commit: `{base}`.

**What this package does.** It replaces {modified_count} existing method files with the same files carrying fuller
headers and comments. No file is added, moved or deleted, and no line of code changes: part 2 proves that for
every file, and part 4 runs the equivalence check of build step 1 again.

**A STOP is a STOP.** If any step prints `STOP`, `FAIL`, an error, or anything other than what is expected: do not
go on, do not retry, do not reset or undo anything. Send Claude the whole output.
**The one exception** is the test suite's own report of the failures that exist today: the word `FAILED` on a
module's line in parts 1 and 3, and the lines `FAILS IN BOTH RUNS` in part 3, are expected for as long as part 3's
comparison ends with its `RESULT: every test that ran was identified; no module and no test changed ...` line.
A failure that is new, a `CHANGED` line, or any STOP from the verifier, the comments-only check or the
equivalence check still stops.

Nothing here contacts a lottery website, changes the PC's date or time, or ends a process. The suite and the
equivalence check read the results masters and the old records; they write only under `{ev}`
(the suite's reports) and Python's own temporary folders. Your ZIP of the project folder made before build
step 1 remains the way back to the old system; no new ZIP is needed, because this package touches no data and no
run folder.

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

## Part 2. Check, copy, check, and the proof that only comments changed (about a minute)

```bat
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase pre
xcopy "{p}\\repo_overlay\\*" . /E /Y
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase post
{py} -B "{p}\\tools\\check_comments_only.py" --tree .
```

Expected: `PRE PASS`; `{modified_count} File(s) copied`; `POST PASS` (0 new paths, {modified_count} modified files, 0 staged
deletions); then {modified_count} lines beginning `comments only:`, a line `compared with commit ...: N Python files
under src and tests; {modified_count} with changed text; 0 with a problem`, and the last line
**`RESULT: PASS - in all {modified_count} changed files only comments and docstrings differ; the code Python runs is identical.`**
A line beginning `CODE CHANGED`, `ADDED`, `REMOVED` or `NOT READABLE`, or `RESULT: STOP`, is a STOP.

## Part 3. The same suite again, and the comparison (about 25 minutes)

```bat
{py} -B "{p}\\tools\\run_suite.py" . "{ev}\\suite_after"
{py} -B "{p}\\tools\\compare_suite_reports.py" "{ev}\\suite_before" "{ev}\\suite_after"
```

Expected, from the comparison: two lines `before: 45 modules; unittest ran N tests; identified here: N` and
`after: ...` with the same N four times; `tests in both runs: N; with the same result: N`; some lines
`FAILS IN BOTH RUNS` (the failures that exist today; the words `FAILURE LINES DIFFER` on `test_gitignore_lines` are
expected, because that test prints a set in a different order each run); **no line beginning `CHANGED`,
`DISAPPEARED`, `NEW`, `MODULE`, `NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`;** and the last line
`RESULT: every test that ran was identified; no module and no test changed its result, disappeared or appeared`.
Any other result is a STOP.

## Part 4. The equivalence check again (reads only; about 40 minutes; leave the window alone)

```bat
{py} -B "{p}\\tools\\check_layout_equivalence.py" --tree .
```

It is the same check, byte for byte, that you ran for build step 1: it computes every old development forecast
again with the tidied code, in memory, and compares content digests.
Expected: for each game a line `coverage: the batch records list N published forecasts; an old digest was found
for N of them; MISSING: 0; ...`; one line for each variant, `n of n equal`; and the last line
**`RESULT: PASS - COMPLETE - both games; every forecast the batch records list was found, computed again ... the
same content digest.`**
Anything else is a STOP: a line beginning `DIFFERENT` or `FAILED`, `RESULT: STOP`, a `MISSING` count above 0, or
`RESULT: PARTIAL` (it names what was not covered). Change nothing and send Claude the output.
(Optional, to save time: four CMD windows, each with the same command and one of `--part 1/4`, `--part 2/4`,
`--part 3/4`, `--part 4/4`. Each then ends `RESULT: PARTIAL` giving `--part was used` as its only reason; all four
must end so, each with `MISSING: 0` for both games and no `DIFFERENT` or `FAILED`.)

## Part 5. Stage, commit, check, and only then push

```bat
git add src
git status --short
git commit -m "{COMMIT_MESSAGE}"
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase committed
```

Expected: `git status --short` lists {modified_count} lines starting with `M`, all under `src/methods/`, and nothing else;
then `COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings are harmless.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

## Part 6. What to send Claude

The commit ID; the text of part 2's comments-only check, of the comparison (part 3) and of the equivalence check
(part 4), copied from the window; and, if anything was unexpected, the folder `{ev}`. Claude then verifies the
commit from GitHub.
"""


def main() -> int:
    """Build the package in the out folder; print its counts; return 0."""
    repository, base, out_folder = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    base = git(repository, 'rev-parse', base).decode().strip()
    with tempfile.TemporaryDirectory() as temporary:
        dev = Path(temporary) / 'dev'
        subprocess.run(['git', 'clone', '-q', str(repository), str(dev)], check=True)
        git(dev, 'checkout', '-q', base)
        subprocess.run([sys.executable, '-B', '-I', str(HERE / 'make_tidy_up.py'), str(dev)], check=True)
        modified = {}
        for line in git(dev, 'status', '--porcelain=v1', '--untracked-files=all').decode().splitlines():
            status, path = line[:2], line[3:]
            assert status == ' M', f'the tidy-up may only modify files: {line}'
            assert path.startswith('src/methods/') and path.endswith('.py'), f'a change outside the method files: {path}'
            content = (dev / path).read_bytes()
            assert b'\r' not in content, f'CR in {path}'
            modified[path] = (sha256_of(git(dev, 'show', f'{base}:{path}')), content)

    assert not set(modified) & set(GUARDED_PATHS), 'a guarded file is among the modified files'
    if out_folder.exists():
        shutil.rmtree(out_folder)
    overlay = out_folder / 'repo_overlay'
    for path, (_old, content) in modified.items():
        (overlay / path).parent.mkdir(parents=True, exist_ok=True)
        (overlay / path).write_bytes(content)
    (out_folder / 'tools').mkdir()
    for tool, folder in TOOLS.items():
        (out_folder / 'tools' / tool).write_bytes((folder / tool).read_bytes())

    manifest = (f'# {PACKAGE_NAME} installation manifest (Git-content SHA-256, LF); base {base}\n'
                '# "M" modified file (with its base hash); the package adds and deletes nothing\n'
                + ''.join(f'M {sha256_of(c)}  {p}  (base {old})\n' for p, (old, c) in sorted(modified.items())))
    (out_folder / MANIFEST_NAME).write_bytes(manifest.encode('ascii'))

    guarded = {p: sha256_of(git(repository, 'show', f'{base}:{p}')) for p in GUARDED_PATHS}
    verifier = VERIFIER_TEMPLATE.read_text(encoding='ascii')
    for mark, text in (
            ('@@NEW@@', ''), ('@@DELETED@@', ''),
            ('@@MODIFIED@@', '\n'.join(f"    '{p}': ('{old}', '{sha256_of(c)}')," for p, (old, c) in sorted(modified.items()))),
            ('@@GUARDED@@', '\n'.join(f"    '{p}': '{h}'," for p, h in guarded.items())),
            ('@@BASE@@', base), ('@@N@@', '0'), ('@@M@@', str(len(modified))), ('@@D@@', '0'),
            ('@@TITLE@@', PACKAGE_TITLE), ('@@VERIFIER@@', VERIFIER_NAME)):
        verifier = verifier.replace(mark, text)
    assert '@@' not in verifier
    (out_folder / VERIFIER_NAME).write_bytes(verifier.encode('ascii'))

    sheet = sheet_text(base, len(modified))
    (out_folder / SHEET_NAME).write_bytes(sheet.replace('\n', '\r\n').encode('ascii'))
    print(f'{PACKAGE_NAME}: {len(modified)} modified files, nothing added or deleted; '
          f'{len(guarded)} guarded files; base {base}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
