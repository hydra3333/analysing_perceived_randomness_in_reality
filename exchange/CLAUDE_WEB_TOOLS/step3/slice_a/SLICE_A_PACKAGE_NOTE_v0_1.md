# Build step 3, slice A (foundations): the package note for review - v0.1

**Date:** 25 November 2026. **Author:** the Claude web chat (the four parts written on 25 November on Fable; the
earlier parts by the previous Claude chat, entries 222 to 266). **Reviewer:** the ChatGPT reviewer chat.
**Status:** for independent review. Not reviewed, not ratified, nothing installed. It authorises nothing.

## 0. The work-item card

| | |
|---|---|
| Item | Build step 3, slice A: foundations (build plan v0.1r1 section 4) |
| Author; reviewer | Claude; ChatGPT |
| Base commit | `main` at `77fec1299dd21df88361ea0d9af7ce655ecb9b01` (the files are `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, laid out as they go into the tree) |
| Scope | the three trees' settings; the readiness markers and `Make_Installable`; the static import check; the list of installed files; the environment's digest and marker; `Check_Tree`; the launch guard with the process rule, wired into the installed research job and its launcher |
| Risk tier | HIGH: the process rule and the orphan-marker's company in the guard, the job's start, the manifest's reader, the digest written into every envelope |
| Owner gate | the owner's go for build step 3's design and cloud coding (entry 217) and for these parts (entries 266, 275). **No install, run, tree or runner task is authorised.** |
| Evidence state | IMPLEMENTED and TESTED in the cloud (Claude's evidence). Not REVIEWED. Nothing on Windows. |

**What this is not.** It is not an install package. By the owner's decision (entry 219) nothing of build step 3 is
installed into DEV until slices A to D have each passed and the joined software has been rehearsed; the one
cumulative package, with its verifier and sheet, is built then. So this slice travels as files at their
repository paths, named by path and SHA-256 in EX_318, with no ZIP.

## 1. The files

| File | New or changed | What it is |
|---|---|---|
| `ENVIRONMENT.example.ini` | changed | the rewritten example (entry 211) |
| `Make_Installable.bat`, `Check_Tree.bat` | new | the two launchers of this slice, in DEV |
| `deploy/INFRA_MANIFEST.ini` | changed | `[files]` gains `deploy/file_form.py` (`other`) and four `derived` files of `src/research`: `installed_files.py`, `environment_marker.py`, `process_rule.py`, `launch_guard.py`; the new `[install_tool]` section has seven files |
| `deploy/deploy_command.py` | new | the one program behind DEV's install launchers (two commands so far) |
| `deploy/install_import_check.py`, `deploy/install_readiness.py`, `deploy/make_installable.py` | new | the static import check; the two readiness markers; the command |
| `deploy/check_tree.py` | new | `Check_Tree`: the owner's read-only look at one tree |
| `src/research/settings.py` | changed | DEV's entries for QA and PROD and the cross-tree checks |
| `src/research/code_identity.py` | changed | the `[install_tool]` list (reading 2); the quick environment digest is removed (reading 7) |
| `src/research/installed_files.py` | new | the list of installed files: made, written, read, compared with the tree |
| `src/research/environment_marker.py` | new | the environment's digest over the fixed inventory; the marker `ENVIRONMENT_VERIFIED.json` written, read and compared |
| `src/research/process_rule.py` | new | which Python processes are of a tree (psutil); it never acts on a process |
| `src/research/launch_guard.py` | new | the checks of every launch and of the start of a job |
| `src/research/research_job.py` | changed | the job calls the guard under its lock and writes the guard's digest into every envelope (8 edits; no calculation touched) |
| `src/research_command.py` | changed | the launcher makes the guard's checks of every launch |
| `tests/research_fixtures.py` | changed | an invented QA or PROD tree is left "as installed" (its list and its marker) when it is made and when a variant is added |
| `tests/test_research_identity.py` | changed | the removed quick digest's one test is removed |
| `tests/test_research_ov1_and_checks.py` | changed | four tests that change an invented tree's software by hand gain one line each (reading 12) |
| `tests/test_trees_settings.py` (32), `test_trees_readiness.py` (40), `test_trees_installed_files.py` (22), `test_trees_check_tree.py` (24), `test_trees_launch_guard.py` (37) | new | 155 tests |

**The nine changed files, by lines added and removed** (the exact difference is
`SLICE_A_CHANGED_FILES_FROM_MAIN_DIFFERENCE.txt` beside this note):

| File | Lines added | Lines removed |
|---|---|---|
| `ENVIRONMENT.example.ini` | 54 | 18 |
| `deploy/INFRA_MANIFEST.ini` | 17 | 0 |
| `src/research/code_identity.py` | 43 | 28 |
| `src/research/research_job.py` | 17 | 11 |
| `src/research/settings.py` | 198 | 21 |
| `src/research_command.py` | 8 | 5 |
| `tests/research_fixtures.py` | 20 | 2 |
| `tests/test_research_identity.py` | 0 | 4 |
| `tests/test_research_ov1_and_checks.py` | 4 | 0 |

## 2. Where each ratified clause is carried out, and what proves it

| Clause | File | Tests |
|---|---|---|
| Deployment design 1: the settings of the three trees and their checks | `src/research/settings.py`, `ENVIRONMENT.example.ini` | `test_trees_settings` (32) |
| Specification 4 and 12.2; design 3.1, 3.2: the two readiness markers | `deploy/install_readiness.py`, `deploy/make_installable.py`, `Make_Installable.bat` | `test_trees_readiness` (40) |
| Specification 3.4: imports checked statically | `deploy/install_import_check.py` | `test_trees_readiness` |
| Specification 12.4: the manifest's `[install_tool]` list | `src/research/code_identity.py` | `test_trees_readiness`, `test_trees_installed_files` |
| Specification 4; design 2, 8, 9: the list of installed files; nothing else under `src` | `src/research/installed_files.py` | `test_trees_installed_files` (22) |
| Specification 16, 14.1; design 1, 10: `Check_Tree` | `deploy/check_tree.py`, `Check_Tree.bat` | `test_trees_check_tree` (24) |
| The file-form standard section 6: the checker in `Make_Installable` and in `Check_Tree` | `deploy/install_readiness.py`, `deploy/check_tree.py` | `test_trees_readiness`, `test_trees_check_tree` |
| Specification 13; design 9: the environment's digest and its marker | `src/research/environment_marker.py` | `test_trees_launch_guard`: `TheEnvironmentsDigest`, `TheEnvironmentsMarker` |
| Design 9, specification 15: the process rule; no program ends a process | `src/research/process_rule.py` | `test_trees_launch_guard`: `TheProcessRuleOnInventedTables`, `TheProcessRuleOnThisPc` |
| Design 8 and 9: the checks of every launch and of a job's start | `src/research/launch_guard.py`, `src/research/research_job.py`, `src/research_command.py` | `test_trees_launch_guard`: `EveryLaunch`, `TheStartOfAJob` |

## 3. Readings and choices put to the reviewer (each RECOMMENDED unless marked; none decided by Claude alone)

1. **A variant may import its own listed files as well as its helpers; the tool itself refuses a variant that
   imports an infrastructure file not classed `forecast`** (entry 225; H-1 v13 section 0E item 14).
2. **The manifest in an installed tree.** A QA or PROD tree holds the manifest as DEV has it, and the manifest
   names the install tool's files, which are never installed there. So the manifest's reader requires a `[files]`
   path to exist in every tree, and an `[install_tool]` path to exist only where that list is asked for, which is
   DEV (`read_install_tool_list`). Specification 12.4 says "a path that does not exist ... refuses"; this is how it
   is kept without making every job in QA and PROD refuse.
3. **The list of installed files** is `records/INSTALLED_FILES.json`: `kind`; `files` (the manifest, every
   `[files]` file, every variant's declaration, declared files and helpers, each once, with its SHA-256);
   `variants` (family, variant, fingerprint); `status_files` (names only). Its code is infrastructure in every
   tree (its class: reading 11). It is made from the tree as it stands; a variant folder that fails its checks refuses the
   making. DEV keeps no list.
4. **Nothing else lies under `src`** (deployment design 9), as the reviewer recommended at the takeover (entry
   270): anything under `src` that is neither a listed file nor a listed status file is a difference, Python's
   cache folder included (named once, not entered) and a link (named, not read). Inside a variant folder the
   fingerprint still passes over caches, as specification 3.4 says. No command removes anything.
5. **`Check_Tree`** takes `DEV`, `QA` or `PROD`, is run from DEV with DEV's Python and DEV's code, and runs no code
   of the tree it looks at. It writes nothing anywhere and takes no lock. What it calls found (exit code 1): the
   tree differing from its list; a variant folder or a status file failing its checks; a file not in its form.
   What it only reports: what is ready in DEV, how the tree compares with DEV (an install is the owner's act),
   the backup ZIPs (listed with full path, size and date; none verified), the locks. A tree not created yet is
   said as such, with `Init_Tree.bat <role>`.
6. **The form check's files in `Check_Tree`** (standard section 6): the tree's list of installed files (in DEV,
   which keeps none, the manifest's two lists and each variant's hashed files); `ENVIRONMENT.ini`; every status
   file; every file under `results/research` and `records`; and under `source_data` the files lying directly in
   it. Left as they are: the two opening records of the retired first study (standard 3A) and the updater's kept
   copies in `source_data`'s sub-folders (standard 7 lists them as untouched). The concrete reason: a walk of all
   of `source_data` would report, in DEV, files that the standard itself says are never converted.
7. **One environment digest: DECIDED by the owner, option A (entry 275).** The full digest of specification 13,
   of the tree's own `.venv` (`pyvenv.cfg`; every file under `Scripts`; every file under `Lib/site-packages` but
   caches and compiled files; one line for the base Python: its version and its program file's path), computed
   once at the start of every job in every tree, compared in QA and PROD with the tree's own marker, and written
   into every new envelope. The quick digest of build step 2 (the Python and the package names and versions) is
   removed; the marker keeps a list of the installed packages only for the cheap first gate of every launch
   (deployment design 9). Lines already written keep the digest they have; no rule compares an envelope's.
   *For the reviewer:* "the base Python's version and executable" is read as the version text and the program
   file's path.
8. **What a QA or PROD tree gains outside `src`:** `deploy/INFRA_MANIFEST.ini` (the engine reads it in every
   tree) and `deploy/file_form.py` (the owner, entry 265). The deployment design's section 2 picture shows no
   `deploy` folder; the two files are on the list of installed files.
9. **The unratified narrow amendment** of the deployment design's section 2 ("standard library only" for the
   install tools, except the process rule, which uses psutil; entry 222) goes with the launch guard.

10. **The process rule is applied at the start of a job in every tree, DEV included.** Deployment design 9 writes
    its list of job-start checks under "in QA and PROD"; the marker and the list of installed files exist only
    there, but the rule's own row in the table names no role, and the owner's rule is that DEV does not act
    differently from PROD. The cost, said to the owner: a DEV job refuses while another Python of the DEV tree is
    running (its `.venv`'s Python, a working folder in the tree, or a command line naming the tree), for example a
    Claude Code task or a debugging session; the refusal lists each process.
11. **The guard, the process rule, the environment's marker and the list of installed files are classed
    `derived`,** not `other` as specification 12.4's examples class "the guard". The job (`research_job.py`) is one
    of the class test's derived entry points and calls the guard under its lock, and that test requires
    everything it imports to be `forecast` or `derived`. `derived` is the more careful of the two labels; the
    forecasting-code identity is untouched.
12. **A status file's presence stays the job's own check, game by game** (specification 3.5; build step 2's
    reviewed behaviour and tests). The list holds each status file by name so that it is known to belong under
    `src`; `Check_Tree` names a missing one. **Four tests of build step 2** that change an invented QA tree's
    software by hand (to stand for a correction, a software replacement or a removal) gain one line,
    `fx.as_installed(tree)`: the command that changes software also rewrites the list.
13. **The checks of every launch** (settings; no unfinished operation; in QA and PROD the marker lists the packages
    installed now) are made by `research_command.py` before a command is handed to; the five unfinished-operation
    files are named in one place (`launch_guard.UNFINISHED_OPERATIONS`), with the one command that finishes each
    let through by name. Nothing writes those files yet (slices B and C, and build step 4).
14. **The process rule's reader** uses psutil (the owner, entry 222); its own chain is taken from psutil's
    `parents()`, and the walk upward for rule (c) from the table. An unreadable Python process refuses. The
    restore's own standard-library reader is slice B's.

## 4. The narrow amendment put forward for ratification (the owner's direction, entry 222; not yet ratified)

Deployment design v0.12, section 2, says: "**The install tools live in DEV** (`deploy\`, standard library only) and
are run from DEV". Its section 9 gives those tools a process rule that needs each process's working folder and
command line, which the standard library does not read. **Proposed wording:** "(`deploy\`, standard library
only, except the process rule of section 9, which uses psutil from the Python that runs the tool)". The restore
stays standard library only, with its own small reader (slice B); TASK_T028 showed the two readings agree on the
owner's PC (entry 240). In this slice the only code that reads the process table is `src/research/process_rule.py`,
which is infrastructure in every tree and runs with the tree's own Python, where psutil is installed; no file under
`deploy/` imports psutil yet. The amendment is put now, as agreed, so that slice C can rely on it.

## 5. The evidence (the cloud's: Claude's, not Windows' and not the reviewer's)

- `main` at `1e9ad25`: 54 modules, 830 tests, the three known failing tests (entry 273).
- With the twenty-five files, in a fresh clone of `main` at `4a3a55e`: **59 modules, 984 tests. Of the 830 earlier
  tests 829 have the same result and one is removed with the quick digest it tested
  (`test_the_environment_digest_is_stable_within_a_process`); the 155 new tests are OK; the three known failing
  tests fail as before and no other.**
- Planted faults, one at a time, each caught, on the final files: 22 in the list of installed files, `Check_Tree`
  and the manifest's reader (`mutation_check_installed_files_and_check_tree.py`; a twenty-third, planted against
  the list naming a missing status file, went with that check: reading 12); 31 in
  the process rule, the environment's marker, the guard and its wiring (`mutation_check_launch_guard.py`). One of
  the 31 first survived (a file that is not compiled, inside a cache folder, entered the digest unnoticed by the
  tests); the test was strengthened and it is caught.
- `Check_Tree DEV` on the real files of a disposable clone, read-only: 40 variants, 169 files checked for form,
  nothing found.
- The mechanical parts of the coding practices (a header with its four parts, a comment on every function, no
  unused import, no write that names no line ending, ASCII) scanned on the eight newest files: nothing found.
- **Not shown anywhere yet:** anything on Windows (the launchers; psutil's reading there; the time of the digest
  on G: and T:); a real QA or PROD tree. The cloud's workspace restarted once during the work; nothing was lost
  and the suite was run again from a clean clone.

**To reproduce** (any Linux with Python 3.15 and the packages of `install_upgrade_dependencies_into_venv.bat`): clone
`main` twice; in the second run `bash exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh <clone> <python>`; run
`exchange/CLAUDE_WEB_TOOLS/step1/run_suite.py <clone> <report folder>` on each and
`exchange/CLAUDE_WEB_TOOLS/step1/compare_suite_reports.py <before> <after>`. The comparison's last line is
`RESULT: DIFFERENCES FOUND - each needs an explanation`: the 155 new tests, the one removed test, the changed count
of `test_research_identity` (25 to 24), and `test_gitignore_lines`, which fails in both runs with a set printed in
another order each time. The files are in `evidence/` beside this note.

## 6. Not tested, and limits

- **Nothing has run on Windows:** the two launchers; psutil's reading of the process table there and the two
  processes of one program in practice; a junction under `src`; the time of the digest on the owner's drives; the
  whole suite. The tests are written to be Windows-safe (the link test skips where a link cannot be made; the
  process test's second Python is told to end and ends by itself; no test ends a process).
- **The cloud's Python is 3.15.0b4;** the owner's is 3.15.2.
- **No real QA or PROD tree exists.** The list of installed files and the marker are written here only into
  invented trees; `Init_Tree`, `Install` and `Verify_Tree`, which write them for real, are slice C's.
- **`src/research_command.py` cannot be run by the suite** (the tree it works in is the repository itself); its
  wiring is covered by one test of the order of its text, and by the guard's own tests.
- **The process rule's "cannot be read" branch** is tried on invented tables only.
- **Nothing yet writes an unfinished-operation file;** the guard's refusal on each is tried with a planted file.
- **When this slice is one day installed in DEV:** the forecasting-code identity is unchanged (no `forecast`-class
  file is touched), so no list becomes foreign and no forecast is made again; the derived-code digest changes;
  every new forecast's envelope carries the new digest of the environment; and a DEV job applies the process rule
  (reading 10).

## 7. Coding practices, and draw values

Coding practices met (`doc/CODING_PRACTICES_v0_1.md`), with the standing exceptions of build step 2's note and no new
one. Every new text file is CRLF and every write names its line ending or is binary (the file-form standard v0.2).
No draw value appears in any file of this slice; its tests use invented results only, and `Check_Tree` and the
guard read no result.

## 8. How the process went

What worked: the previous chat's working files and the handover's exact list of what was left; putting each open
reading to the owner or the reviewer before coding it (the one digest; the process readers); a test with a planted
fault for each rule, which found one weak test. What was friction: workspace helpers that edited the same file
and undid each other; a first fixture design that hid a change from four tests; one restart of the cloud's
workspace. What I would change: one helper for one file, rebuilt from `main`'s bytes each time (done), and work
committed before every long run (done since). Uncertain: whether applying the process rule in DEV will be a
nuisance in the owner's daily use; the rehearsal on Windows will show it.
