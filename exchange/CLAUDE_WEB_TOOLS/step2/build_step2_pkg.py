"""Build step 2 (the research engine, in DEV): the builder of the install package for the owner's clone.

What this file is for
    It makes the package the owner installs: the overlay of the engine's new files and of the two existing files
    it changes, the read-only verifier (from the project's reviewed template,
    exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py), the tools the run sheet uses, the manifest, and the
    install and run sheet. Everything is derived from one fresh clone at the base commit, with this folder's
    overlay copied in and apply_edits.py run on it: nothing is typed by hand, and every count in the
    instructions comes from the files.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.4 (build step 2: the research engine, in
    DEV); the install order is doc/HANDOVER/Claude_Primary_Handover_H1_v9.md section 1.6 ("Code packages").

Which of the project's own modules it uses
    None. It runs apply_edits.py (beside this file) and reads the verifier template as text.

What uses it
    Claude, in the cloud workspace. Usage:  python build_step2_pkg.py <repository clone> <base commit> <out folder>
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- constants

HERE = Path(__file__).resolve().parent                              # exchange/CLAUDE_WEB_TOOLS/step2
STEP1_TOOLS = HERE.parent / 'step1'                                 # the tools reviewed with build step 1
VERIFIER_TEMPLATE = HERE.parent / 'wf1' / 'verifier_template.py'    # the reviewed read-only verifier
OVERLAY = HERE / 'overlay'                                          # the engine's new files, as they go into the tree

PACKAGE_NAME = 'STEP2_Research_Engine_v1'
PACKAGE_TITLE = 'build step 2 package (the research engine, in DEV; specification v0.6 sections 3 to 11)'
VERIFIER_NAME = 'VERIFY_STEP2_INSTALL.py'
SHEET_NAME = 'INSTALL_AND_RUN_SHEET.md'
MANIFEST_NAME = 'INSTALL_MANIFEST_SHA256.txt'

# The tools the run sheet uses, copied into the package so that their bytes are fixed with it: {name: its folder}.
# The first two are the tools of build step 1, byte for byte; the third is new with this package.
TOOLS = {'run_suite.py': STEP1_TOOLS, 'compare_suite_reports.py': STEP1_TOOLS,
         'compare_fill_with_old_records.py': HERE}

# The two existing files the package replaces (apply_edits.py makes their new versions from the base versions).
EDITED_PATHS = ('.gitignore', 'tests/test_mhupa_master_versions.py')

# Where the owner extracts the package and keeps the evidence: his download folder, never the repository.
OWNER_PACKAGE_FOLDER = rf'E:\TEMP\{PACKAGE_NAME}'
OWNER_EVIDENCE_FOLDER = r'E:\TEMP\STEP2_evidence'
# The suite reports the owner made this morning on exactly today's src and tests (the tidy-up's "after" run).
OWNER_EARLIER_SUITE = r'E:\TEMP\TIDY1_evidence\suite_after'
TIDY_UP_COMMIT = 'c7e6ed8'

COMMIT_MESSAGE = ('BUILD STEP 2: the research engine in DEV (src/research, the two launchers, the manifest, '
                  'its tests); the old system is not changed')

# Files that the package must leave byte-identical in Git: the data, the old system's code that every old
# forecast passed through, the shared code the new engine imports, and the line-ending rules.
GUARDED_PATHS = (
    'source_data/POWERBALL_results_master.csv', 'source_data/POWERBALL_results_master_ledger.csv',
    'source_data/POWERBALL_results_master_init_verification.json', 'source_data/HOLDOUT_OPENED_POWERBALL.json',
    'source_data/OZLOTTO_results_master.csv', 'source_data/OZLOTTO_results_master_ledger.csv',
    'source_data/OZLOTTO_results_master_init_verification.json', 'source_data/HOLDOUT_OPENED_OZLOTTO.json',
    'src/methods/_common/__init__.py', 'src/methods/_common/canonical_encoding.py',
    'src/methods/_common/contract_vocab.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/game_profiles.py', 'src/methods/_common/contract_forecast.py',
    'src/methods/_common/contract_records.py', 'src/methods/_common/contract_task.py',
    'src/methods/_common/contract_runner.py', 'src/methods/_common/contract_dispatch.py',
    'src/methods/_common/contract_registry.py', 'src/methods/_common/walk_forward.py',
    'src/methods/_common/master_versions.py', 'src/methods/_common/closure.py',
    'src/methods/_common/method_table.py', 'src/evaluation/__init__.py', 'src/evaluation/divisions.py',
    'src/Powerball_Experiment_Coordinator.py', 'src/results_master_v0_2.py', '.gitattributes',
)


def sha256_of(data: bytes) -> str:
    """Return the SHA-256 of some bytes as 64 hexadecimal characters, for example 'e3b0c442...b855'."""
    return hashlib.sha256(data).hexdigest()


def git_content(data: bytes) -> bytes:
    """A file's bytes as Git stores them for a text file: CRLF line endings become LF."""
    return data.replace(b'\r\n', b'\n')


def git(tree: Path, *arguments: str) -> bytes:
    """Run one Git command in a tree and return its output bytes. Refuses (an exception) if Git fails."""
    return subprocess.run(['git', '-C', str(tree), *arguments], check=True, capture_output=True).stdout


def sheet_text(base: str, new_count: int, test_modules: list, engine_tests: int) -> str:
    """Write the owner's install and run sheet.

    base: the base commit's full ID.  new_count: how many files the package adds.  test_modules: the names of
    the test modules it adds.  engine_tests: how many tests those modules hold in all.
    Returns the sheet as text with LF line endings (the caller converts to CRLF), for example beginning
    '# STEP2_Research_Engine_v1 - build step 2 package ...'.
    """
    p, ev = OWNER_PACKAGE_FOLDER, OWNER_EVIDENCE_FOLDER
    py = r'.venv\Scripts\python.exe'
    after_modules = 45 + len(test_modules)
    return f"""# {PACKAGE_NAME} - {PACKAGE_TITLE}: install and run sheet

**Only after the owner's own go for each part.** Windows CMD, in the repository root
(`E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality`). Nothing of the project running.
**Save the ZIP to `E:\\TEMP`, not into the repository,** delete any earlier `{p}` folder, and extract it
**to `E:\\TEMP`** (the ZIP holds its own top folder), so that `{p}\\{VERIFIER_NAME}` exists. Base commit: `{base}`.

**What this package does.** It adds the new research engine beside the old system: {new_count} new files
(`src\\research\\`, the program `src\\research_command.py`, the launchers `Run_Research.bat` and
`Withdraw_Variant.bat`, `deploy\\INFRA_MANIFEST.ini`, `ENVIRONMENT.example.ini` and {len(test_modules)} test modules with their
fixtures). It replaces two existing files: `.gitignore` (six lines added, so that Git ignores this PC's settings
file, DEV's research results, the status files and the `records` and `scratch` folders) and one old test,
`tests\\test_mhupa_master_versions.py` (its list of the files allowed to name the results files gains the new
reader). **No file of the old system's code or of any method is changed,** and nothing is deleted.

**A STOP is a STOP.** If any step prints `STOP`, `FAIL`, `REFUSED`, an error, or anything other than what is
expected: do not go on, do not retry, do not reset or undo anything. Send Claude the whole output.
**The one exception** is the test suite's own report of the failures that exist today: the word `FAILED` on a
module's line in parts 1 and 3, and the lines `FAILS IN BOTH RUNS` in part 3, are expected for as long as part 3's
comparison ends as part 3 says.

Nothing here contacts a lottery website, changes the PC's date or time, or ends a process. Parts 1 to 5 read the
results masters and write only under `{ev}` (the suite's reports) and Python's own temporary folders. Part 6, on
its own go, is the first run of the new engine on the real results: it writes DEV's own research results under
`results\\research\\`, the status file in each variant folder, `records\\` and nothing else; Git ignores all of
them. Your ZIP of the project folder made before build step 1 remains the way back to the old system.

## Part 1. Update, and the suite as it is today (the baseline; about 25 minutes, or none)

```bat
git status --short
git pull --ff-only
git diff --stat {TIDY_UP_COMMIT} HEAD -- src tests
```

Expected: `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; the third
command prints nothing (`src` and `tests` are exactly as the tidy-up left them this morning).

**If the folder `{OWNER_EARLIER_SUITE}` still exists** (this morning's "after" run of the tidy-up, made on
exactly these files), it is the baseline: skip the next command and use that folder as the "before" in part 3.
**Otherwise** make the baseline now:

```bat
{py} -B "{p}\\tools\\run_suite.py" . "{ev}\\suite_before"
git status --short
```

Expected: one line for each test module, some of them `FAILED` (two modules are known to fail today; that is the
baseline, not a STOP); a last line `DONE: 45 modules, 571 tests ran`; and `git status --short` prints nothing.

## Part 2. Check, copy, check (about a minute)

```bat
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase pre
xcopy "{p}\\repo_overlay\\*" . /E /Y /H
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase post
```

Expected: `PRE PASS`; `{new_count + len(EDITED_PATHS)} File(s) copied`; `POST PASS` ({new_count} new paths, {len(EDITED_PATHS)} modified files, 0 staged
deletions). (`/H` is needed because `.gitignore` is among the files copied.)

## Part 3. The suite again, and the comparison (about 30 minutes)

```bat
{py} -B "{p}\\tools\\run_suite.py" . "{ev}\\suite_after"
```

Expected: a last line `DONE: {after_modules} modules, {571 + engine_tests} tests ran`, and the {len(test_modules)} new modules
({', '.join(f'`{name}`' for name in test_modules)}) each ending `OK`.

@@COMPARISON_EXPECTED@@

```bat
git status --short
```

Expected: only the files of part 2: {len(EDITED_PATHS)} lines starting ` M` and the new paths starting `??`. The suite has left
nothing else behind.

## Part 4. Stage, commit, check, and only then push

```bat
git add .gitignore deploy src tests Run_Research.bat Withdraw_Variant.bat ENVIRONMENT.example.ini
git status --short
git commit -m "{COMMIT_MESSAGE}"
{py} "{p}\\{VERIFIER_NAME}" --repo . --phase committed
```

Expected: `git status --short` lists {new_count} lines starting with `A` and {len(EDITED_PATHS)} starting with `M`, and nothing else; then
`COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings are harmless.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

## Part 5. This PC's settings file (a minute)

```bat
copy ENVIRONMENT.example.ini ENVIRONMENT.ini
notepad ENVIRONMENT.ini
git status --short
```

In Notepad, check that `tree_root` is this folder and `venv_dir` is its `.venv`; the example already holds this
PC's paths, so there should be nothing to change. Leave the commented lines as they are (they belong to build
step 3). Save and close. `git status --short` prints nothing: Git ignores `ENVIRONMENT.ini`.

**Parts 1 to 5 install the engine and prove the install. They run nothing on real results. Stop here if you wish.**

## Part 6. DEV's first fill - only on your own separate go (about an hour; leave the window alone)

```bat
Run_Research.bat --game BOTH --no-update
```

What it does: for each game it gives every variant a status file (`ACTIVE`), computes every variant's forecast for
every draw it has enough earlier draws for, scores each against the result on file, saves the reports, and
forecasts the next draw. It says how far it has got every 25 draws. `--no-update` because DEV has no other tree
to copy results from yet; the results in DEV are still brought up to date by `Run_Results_Updater.bat`, as today.

Expected, at the end: for each game a line beginning
`POWERBALL: finished. Results on file through draw` (and the same for `OZLOTTO`), each ending
`prevailing OV-1: not started; waiting for a successful results step`; no line beginning `WARNING`; and the last
line **`The job finished.`** A line with `REFUSED` or `STOPPED`, or the last line `A STOP is a STOP: ...`, is a STOP:
change nothing and send Claude the whole output. (If the window is closed or the PC restarts part-way, the same
command continues where it stopped; if it then says `a process of this tree is running`, read what it says and
ask Claude before deleting anything.)

Then the same command once more, into a file (a few minutes; this second job has nothing new to compute, and its
time is the time of an ordinary week's job without new draws):

```bat
echo %TIME%
Run_Research.bat --game BOTH --no-update > "{ev}\\second_job.txt" 2>&1
echo %TIME%
type "{ev}\\second_job.txt"
git status --short
```

Expected: for each game `written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files`;
the last line `The job finished.`; and `git status --short` prints nothing (everything the job wrote is ignored
by Git).

## Part 7. The early comparison with the old development records (reads only; a few minutes)

```bat
{py} -B "{p}\\tools\\compare_fill_with_old_records.py" --tree .
```

It reads every development forecast the old system kept in its run folders and requires DEV's new lists to hold
the same view digest, scores, ranking, TOP and WORST for the same variant and draw. It computes nothing and
writes nothing.
Expected: one line for each variant of each game, `n of n equal`; two summary lines for each game with
`DIFFERENT: 0` and `of those not among the old forecasts compared: 0`; and the last line
**`RESULT: PASS - COMPLETE - both games; all N old development forecasts ...`**
Anything else is a STOP: a line beginning `DIFFERENT`, `RESULT: STOP`, `RESULT: PARTIAL` or `RESULT: REFUSED`.

## Part 8. What to send Claude

The commit ID of part 4; the comparison's text (part 3); the last twenty lines of the first job's window and the
two times and the file `{ev}\\second_job.txt` (part 6); the text of part 7; roughly how long the first job took;
and, if anything was unexpected, the folder `{ev}`. Claude then verifies the commit from GitHub.
The reports to look at, if you wish: `results\\research\\POWERBALL\\reports\\` (start with `README.txt`).
"""


def main() -> int:
    """Build the package in the out folder; print its counts; return 0."""
    repository, base, out_folder = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    base = git(repository, 'rev-parse', base).decode().strip()
    with tempfile.TemporaryDirectory() as temporary:
        dev = Path(temporary) / 'dev'
        subprocess.run(['git', 'clone', '-q', str(repository), str(dev)], check=True)
        git(dev, 'checkout', '-q', base)
        shutil.copytree(OVERLAY, dev, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
        subprocess.run([sys.executable, '-B', '-I', str(HERE / 'apply_edits.py'), str(dev)], check=True,
                       stdout=subprocess.DEVNULL)
        new, modified = {}, {}
        for line in git(dev, 'status', '--porcelain=v1', '--untracked-files=all').decode().splitlines():
            status, path = line[:2], line[3:]
            content = (dev / path).read_bytes()
            if status == '??':
                assert (OVERLAY / path).is_file() and (OVERLAY / path).read_bytes() == content, f'not from the overlay: {path}'
                new[path] = content
            else:
                assert status == ' M' and path in EDITED_PATHS, f'an unexpected change: {line}'
                assert b'\r' not in content, f'CR in {path}'
                modified[path] = (sha256_of(git(dev, 'show', f'{base}:{path}')), content)
        assert sorted(modified) == sorted(EDITED_PATHS), f'the edited files are not the two expected: {sorted(modified)}'
        for path, content in new.items():
            assert (b'\r' in content) == path.endswith('.bat'), f'line endings: only a .bat file holds CRLF: {path}'

    assert not (set(new) | set(modified)) & set(GUARDED_PATHS), 'a guarded file is among the package\'s files'
    if out_folder.exists():
        shutil.rmtree(out_folder)
    overlay = out_folder / 'repo_overlay'
    for path, content in list(new.items()) + [(p, c) for p, (_old, c) in modified.items()]:
        (overlay / path).parent.mkdir(parents=True, exist_ok=True)
        (overlay / path).write_bytes(content)
    (out_folder / 'tools').mkdir()
    for tool, folder in TOOLS.items():
        (out_folder / 'tools' / tool).write_bytes((folder / tool).read_bytes())

    manifest = (f'# {PACKAGE_NAME} installation manifest (Git-content SHA-256, LF); base {base}\n'
                '# "N" new file; "M" modified file (with its base hash); the package deletes nothing\n'
                + ''.join(f'N {sha256_of(git_content(c))}  {p}\n' for p, c in sorted(new.items()))
                + ''.join(f'M {sha256_of(c)}  {p}  (base {old})\n' for p, (old, c) in sorted(modified.items())))
    (out_folder / MANIFEST_NAME).write_bytes(manifest.encode('ascii'))

    guarded = {p: sha256_of(git(repository, 'show', f'{base}:{p}')) for p in GUARDED_PATHS}
    verifier = VERIFIER_TEMPLATE.read_text(encoding='ascii')
    for mark, text in (
            ('@@NEW@@', '\n'.join(f"    '{p}': '{sha256_of(git_content(c))}'," for p, c in sorted(new.items()))),
            ('@@DELETED@@', ''),
            ('@@MODIFIED@@', '\n'.join(f"    '{p}': ('{old}', '{sha256_of(c)}')," for p, (old, c) in sorted(modified.items()))),
            ('@@GUARDED@@', '\n'.join(f"    '{p}': '{h}'," for p, h in guarded.items())),
            ('@@BASE@@', base), ('@@N@@', str(len(new))), ('@@M@@', str(len(modified))), ('@@D@@', '0'),
            ('@@TITLE@@', PACKAGE_TITLE), ('@@VERIFIER@@', VERIFIER_NAME)):
        verifier = verifier.replace(mark, text)
    assert '@@' not in verifier
    (out_folder / VERIFIER_NAME).write_bytes(verifier.encode('ascii'))

    test_modules = sorted(Path(p).stem for p in new if p.startswith('tests/test_'))
    engine_tests = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    sheet = sheet_text(base, len(new), test_modules, engine_tests)
    expected = (HERE / 'comparison_expected.md').read_text(encoding='ascii').strip() \
        if (HERE / 'comparison_expected.md').is_file() else 'COMPARISON EXPECTATIONS NOT YET WRITTEN'
    sheet = sheet.replace('@@COMPARISON_EXPECTED@@', expected)
    (out_folder / SHEET_NAME).write_bytes(sheet.replace('\n', '\r\n').encode('ascii'))
    print(f'{PACKAGE_NAME}: {len(new)} new files, {len(modified)} modified files, nothing deleted; '
          f'{len(guarded)} guarded files; {len(test_modules)} new test modules; base {base}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
