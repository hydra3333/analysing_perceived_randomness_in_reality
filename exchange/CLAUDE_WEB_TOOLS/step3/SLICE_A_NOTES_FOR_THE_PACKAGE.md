# Slice A of build step 3: notes for the package (a working file; not a design, not a rule)

Kept by the Claude web chat while slice A is written, so that the package's note can be made from it and so that
another chat can go on. The authority is the specification v0.6, the deployment design v0.12, the coding practices
and the file-form standard v0.2. Decision log entries 264 to 266 and 270 to 276 are the record. Everything in
`overlay/` is working files: not a package, not reviewed, nothing installed.

## 1. What the overlay holds (25 November 2026: every part of slice A is written)

Twenty-five files, all CRLF, laid out as they go into the tree. "Changed" means a file that is on `main` today.

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

## 2. Still to do before the slice goes to the reviewer

The package's note (from this file), the exact difference of every changed file from `main`, and the EX message, on
the owner's word. No part of the code is left to write. The marker `ENVIRONMENT_VERIFIED.json` has its writer here;
the commands that call it (`Verify_Tree`, `Init_Tree`) are slice C's, and so is the first writing of a real tree's
list of installed files.

## 3. Readings and choices to put to the reviewer with the slice (each RECOMMENDED, none decided by Claude alone)

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

## 4. The cloud's evidence (Claude's, not Windows'; Python 3.15.0b4 on Linux)

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

## After EX_319 (25 November 2026)

The reviewer's five findings (A-B01, A-B02, A-C01, A-C02, A-C03) are corrected in the overlay. What changed, the
tests and the evidence are in `slice_a/SLICE_A_CORRECTIONS_AFTER_EX_319_v0_1.md`; where these notes and that note
differ, that note is the later one. The slice now changes ten files of main (`src/research/withdraw.py` is the
tenth) and adds sixteen.
