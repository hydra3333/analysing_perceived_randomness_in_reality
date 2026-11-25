# Build step 3, slice A: the corrections after EX_319, for the focused recheck - v0.1

**Date:** 25 November 2026. **Author:** the Claude web chat. **Reviewer:** the ChatGPT reviewer chat.
**Status:** for the focused recheck EX_319 asks for. Not reviewed, not ratified, nothing installed. It authorises
nothing. It is read with the slice's package note (`SLICE_A_PACKAGE_NOTE_v0_1.md`, the note EX_319 reviewed), which
is left as it was reviewed; where the two differ, this note is the later one.

## 1. What this is

EX_319 (`exchange/EX_319_ChatGPT.md`, decision log entry 278) accepted the slice's architecture and asked for five
corrections: two blockers (A-B01, A-B02) and three corrections (A-C01, A-C02, A-C03). Claude read each against the
submitted files and found each one true. This note says, for each, what was changed, where, and which test and
which planted fault show it. Nothing else in the slice was changed, and nothing was redesigned.

The files are the overlay, `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, laid out as they go into the tree. The exact
differences from the files the reviewer read are in `SLICE_A_CORRECTIONS_AFTER_EX_319_DIFFERENCE.txt` beside this
note (11 files, 35 hunks):

| File | Lines added | Lines removed | Hunks |
|---|---|---|---|
| `deploy/check_tree.py` | 10 | 6 | 2 |
| `deploy/install_import_check.py` | 8 | 3 | 2 |
| `deploy/make_installable.py` | 15 | 2 | 4 |
| `src/research/environment_marker.py` | 50 | 20 | 4 |
| `src/research/launch_guard.py` | 34 | 17 | 4 |
| `src/research/process_rule.py` | 19 | 3 | 2 |
| `src/research/withdraw.py` | 7 | 0 | 4 |
| `tests/research_fixtures.py` | 20 | 2 | 2 |
| `tests/test_trees_check_tree.py` | 12 | 5 | 2 |
| `tests/test_trees_launch_guard.py` | 177 | 3 | 6 |
| `tests/test_trees_readiness.py` | 24 | 2 | 3 |

`src/research/withdraw.py` is new to the overlay: it is main's file with the four small changes of A-B02, so the
slice now changes ten files of main (it changed nine) and adds sixteen, as before. The manifest is not changed:
`withdraw.py` is already in it, and no file was added.

## 2. The five corrections

### A-B01. The environment's digest is now the full one

`src/research/environment_marker.py`.

- **The base Python's program file enters by its bytes.** The last line of what is hashed was
  `base python<TAB>version<TAB>path`; it is now `base python<TAB>version<TAB>path<TAB>sha256 of the file's bytes`.
  The file is read once. A new small function, `base_python()`, gives the version and the path, so that a test can
  put an invented program file in their place without touching a real one.
- **A program file that cannot be read refuses** (`EnvironmentRefused`), as any file of the inventory does.
- **A folder that cannot be listed refuses.** `os.walk` is given an error callback that passes the error on; before,
  such a folder was silently left out.
- **The three parts must be there:** `pyvenv.cfg`, `Scripts` and `Lib\site-packages`. An environment that lacks one
  is refused, each missing part named. Before, a missing part contributed nothing.
- **The count is of the files whose bytes were hashed,** the base program file among them (so one more than the
  files of the inventory).
- Nothing wider was added: no other file of the base Python, no DLL, no second pass, no second digest.

Tests (`tests/test_trees_launch_guard.py`, class `TheEnvironmentsDigest`): the base program's bytes change the
digest with its path and version held fixed, and putting the bytes back gives the old digest; another version at
the same path and bytes changes it; a base program that cannot be read refuses; each of the three parts, taken
away in turn, refuses and is named, and no marker is written; a folder that cannot be listed refuses. The earlier
tests of the stable digest and of the marker lying outside what is hashed are kept.

**The test fixture.** The common invented tree had an empty `.venv`; it now has a small invented environment in the
Windows layout (`tests/research_fixtures.py`, `make_invented_environment`: `pyvenv.cfg`, `Scripts/python.exe`,
`Lib/site-packages/invented_package/__init__.py`, none of it a Python that could run).

**What the cloud evidence is, and is not.** Every digest in the tests is of invented files in the Windows layout.
The base program file read in the job's tests is the cloud's own Python, read and never changed. A real Linux
environment (its folders are `bin` and `lib/python3.x/site-packages`) is now refused as lacking the three parts,
which is intended: the project runs on Windows. Nothing here is evidence about a real Windows environment; that
stays with the joined rehearsal.

### A-B02. The commands that write can no longer escape the refusal

- **The shared check.** `src/research/launch_guard.py` gains `check_software_is_as_installed(settings)`: the
  comparison of a QA or PROD tree with its list of installed files, taken out of `check_at_job_start` unchanged, so
  that the job and the withdrawal use the same lines. In DEV it asks nothing.
- **(a) The withdrawal.** `src/research/withdraw.py`: holding its two existing locks, and before it tidies the
  staging folder, plans, shows or writes anything, it calls `check_no_unfinished_operation` and
  `check_software_is_as_installed`. A refusal ends as its other refusals do: `REFUSED: ...`, exit code 2, nothing
  written. It does not take the environment's digest and does not read the process table. Its own orphan-marker
  check is where it was. No new lock.
- **(b) Make_Installable.** `deploy/make_installable.py`, in `main`, after the typed words are understood and
  before any marker is made or removed: `check_no_unfinished_operation` and `check_no_orphan_marker`. A refusal
  says `REFUSED: ... No readiness marker was made or removed.` and gives exit code 2, the code the command already
  gives when nothing was done. The checks are in `main` and not in the dispatcher so that the tests go through
  the route that writes.
- **The job, under its lock.** `check_at_job_start` now begins with `check_no_unfinished_operation`, before the
  environment is read. It is a look for five file names.
- **Check_Tree is not changed by this:** it still reports these states and is never refused by them.

Tests: class `AWithdrawalInAnInstalledTree` (nine tests, each through `withdraw.withdraw`, the command's own
route): written and logged in a tree as installed; a helper changed by hand, an unlisted file under `src`, and a
tree without its list each refuse with the software, the status files, the tree's log and the staging folder
byte for byte as before; the refusal comes before an interrupted status write is tidied away; an unfinished
operation refuses in QA and in DEV; the orphan marker still refuses; in DEV no list is asked; and a withdrawal
passes with the digest and the process table replaced by functions that fail if called. Class `TheStartOfAJob`:
an unfinished operation refuses the job itself, run without its launcher, before the environment is read. Class
`TheCommandMakeInstallable` (`tests/test_trees_readiness.py`): with an unfinished operation's file, and with the
orphan marker, marking, unmarking and several at once each refuse and every file of the tree is as before; with
the file gone the command works. `tests/test_trees_check_tree.py` already shows Check_Tree reporting both.

### A-C01. The process rule: a path must end where the tree's path ends

`src/research/process_rule.py`, `_names_the_folder`. The tree's path is taken as named in a command line only when
the character after it does not continue a folder's name. A letter, a digit and the four marks `_ - . ~` continue a
name; the end of the text, a separator, a quote, a blank and any other mark end it. So `T:\a_p_r_i_r_backups\QA`
does not name `T:\a_p_r_i_r`, and `T:\a_p_r_i_r\Run_Research.bat`, `"T:\a_p_r_i_r"` and
`cd /d T:\a_p_r_i_r&& Run_Research.bat` do. Every place the path stands in an argument is looked at, not only the
first. **The reading taken:** EX_319 asks for "end or actual path separator, with ordinary quoting/argument syntax
accommodated". The rule is written from the other side (what continues a name) so that an unforeseen mark after
the path lists the process rather than passes it: the rule may only list too much. No command-line parser.

Tests (class `TheProcessRuleOnInventedTables`): five command lines that name only a folder whose name begins like
the tree's, and a window above with such a line, list nothing; six forms that do name the tree are listed. The
earlier examples (program file, working folder, the pair, the launcher window) are kept.

### A-C02. Check_Tree says what it looked at

`deploy/check_tree.py`. With a marker: `Environment: verification marker present (<path>; it lists N package(s)).
This command did not check the environment's files or packages against it; each launch and each job in the tree
does.` Without one: `Environment: NOT VERIFIED; ...`, as before. The closing line, when nothing was found:
`Nothing was found by the checks this command makes. It starts nothing and does not check the tree's Python
environment, so it does not say that the tree is ready to run.` Nothing is hashed or compared that was not
before. The existing marker test was changed, not a new one added: it also changes the environment after the
marker was written and shows that the line still says only that the marker is present.

### A-C03. The static import check sees `import sys as s`

`deploy/install_import_check.py`, `forbidden_constructs`: the names a file imports `sys` by are collected first
(`sys`, and any `import sys as <name>`), and `<name>.path` is found under each. Two more cases in the existing
test of forbidden constructs (`tests/test_trees_readiness.py`): `import sys as s` then `s.path.insert(...)`, and
`import os, sys as system` then `system.path`. It is a check against accidents, as EX_319 says; it does not try to
defeat a file written to deceive it.

## 3. The evidence (the cloud: Linux, Python 3.15.0b4; Claude's own, not Windows' and not the reviewer's)

All in `evidence/` beside this note.

- **The whole suite** in a fresh clone of `main` with the corrected overlay copied in: 59 modules, 1000 tests
  (`SUITE_WITH_SLICE_A_AFTER_EX_319_MODULES.txt`).
- **Compared with the slice as reviewed** (`SUITE_COMPARISON_REVIEWED_SLICE_TO_CORRECTED_SLICE.txt`): 983 tests in
  both runs, every one with the same result; one test renamed (the Check_Tree marker test, A-C02); 16 new, all OK.
  The comparison tool says "DIFFERENCES FOUND" because tests were added and one was renamed; no test changed its
  result.
- **Compared with `main`** (`SUITE_COMPARISON_MAIN_TO_SLICE_A_AFTER_EX_319.txt`): 829 of main's 830 tests with the
  same result, one removed (the old quick digest's test, as before), 171 new. The three known failing tests of
  main, and no other.
- **Planted faults for the corrections** (`PLANTED_FAULTS_EX_319_CORRECTIONS.txt`): 22 planted, one at a time, 22
  caught. Seven for A-B01, eight for A-B02, four for A-C01, two for A-C02, one for A-C03. The script is
  `exchange/CLAUDE_WEB_TOOLS/step3/mutation_check_ex319_corrections.py`.
- **The two earlier planted-fault runs, made again on the corrected files:** 31 of 31 and 22 of 22 caught
  (`..._AFTER_EX_319.txt`). Two faults of the first script were re-pointed at the lines where the comparison now
  lies.
- **Check_Tree DEV** on the real files of a disposable clone with the corrected overlay: 172 files checked for
  form, nothing found.

## 4. What is not tested, and what a reader should know

- Nothing ran on Windows. The base program file on Windows (`sys._base_executable`), a folder Windows will not
  list, and psutil's view of a real command line are for the joined rehearsal, as agreed.
- The launcher's text is not end-to-end evidence (EX_319 section 5); the real launch path is in the joined
  rehearsal.
- The digest a job writes into its envelopes differs from what the slice as first submitted would have written (one
  more field in its last line). Nothing was ever produced with either: nothing of the slice is installed, and no
  earlier envelope is touched.
- One cost on the owner's PC, small: each job and each `Verify_Tree` reads the base Python's program file once.
- Slices B to D, the order of installation and the owner's gates are unchanged.
