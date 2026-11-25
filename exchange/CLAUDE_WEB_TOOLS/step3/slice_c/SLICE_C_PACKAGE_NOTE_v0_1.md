# Build step 3, slice C: package note for the reviewer (v0.1)

**Date:** 25 November 2026. **Author:** the Claude web chat. **For:** the ChatGPT reviewer chat, through the project owner.
**Status:** working files, written and tested in the cloud only. Not installed. Nothing was run on Windows. This note
authorises nothing.

## 1. What slice C is

The four commands of the ratified deployment design v0.12 that create and change a QA or PROD tree, and the machinery
they share: `Init_Tree.bat QA|PROD` (design section 4), `Install.bat QA|PROD [--only ...]` (section 5),
`Reinstall_Infra.bat QA|PROD [--replace-unfinished]` (section 6), `Verify_Tree.bat` (section 7), with the checks of
section 3.3 and the states of section 8. Out of the slice, recognised and refused where met: `Correct_Shared_Code`, the
QA software replacement, the reseeding and the rerun (build step 4), and the updater (slice D).

## 2. The files

`slice_c/SLICE_C_FILES_AND_HASHES.txt` lists them with their SHA-256: **20 new files and 3 changed files** in
`exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, which now holds 54 files, every one CRLF. The three changed files are ones
slices A and B reviewed; their exact differences are `slice_c/SLICE_C_DIFFERENCES_OF_REVIEWED_FILES.txt`:

- `src/research/research_job.py`: the reading half of `open_game` is now its own function `read_game` (a pure
  extraction; `open_game` calls it), so that the checks read exactly what the job reads and write nothing.
- `deploy/deploy_command.py`: three command words (`init-tree`, `install`, `reinstall-infra`).
- `deploy/INFRA_MANIFEST.ini`: the new infrastructure and tool files; and the owner's four environment scripts under
  `[files]`, class `other`, so that a new tree holds them (design 2 lists them among a tree's files).

New, by part:

| Part | Files | What it is |
|---|---|---|
| C1 | `src/research/tree_checks.py`, `src/research/tree_verify.py`, `src/tree_checks_command.py`, `Verify_Tree.bat` | the smoke case, the forecast sample, the derived results in full; `Verify_Tree`; the program an install tool starts with the target's Python (`checks`, `reports`) |
| C2 | `deploy/install_common.py`, `deploy/suite_on_copy.py`, `deploy/SUITE_MANIFEST.ini` | what DEV offers; the plan; the barrier; copying; the tree's software against the plan; reserving the target; the kit, the backup and the one question; the ending; the suite of an install on a temporary copy |
| C3 | `deploy/init_tree.py`, `Init_Tree.bat` | creating a tree |
| C4 | `deploy/install.py`, `Install.bat` | adding ready variants |
| C5 | `deploy/reinstall_infra.py`, `Reinstall_Infra.bat` | bringing a tree's infrastructure to DEV's |
| tests | `tests/test_trees_checks.py`, `test_trees_verify.py`, `test_trees_suite.py`, `test_trees_install_common.py`, `test_trees_init.py`, `test_trees_install.py`, `test_trees_reinstall.py` | 246 tests |

## 3. One owner decision that needs an amendment of ratified text (decision log entry 305)

**`Verify_Tree.bat` does not run the test suite.** The tests live only in DEV; a QA or PROD tree's settings do not say
where DEV is; and the project's own rule is that the installed engine starts no program
(`tests/test_research_job.py`, `test_the_engine_starts_no_program_and_opens_no_connection`). My first writing started
DEV's tool from the tree and the whole suite refused it; the code was corrected, not the rule. `Verify_Tree` rests on
every installed variant's smoke case, the forecast sample and the derived results in full, and says in capitals every
time that the suite is not run by it. The suite is run with a tree's own Python at `Init_Tree` and at every
`Reinstall_Infra`. The owner's reasons: the same software then does the same thing in QA and in PROD, and a tree can
be verified with no DEV on the PC. **Proposed wording, for your view; the owner ratifies it (RAT-59) only after it:**

- *Deployment design section 7, first paragraph, to read:* "Process check; a backup attempted; the structure; every
  installed variant's smoke case; the fixed forecast sample, whose differences after an environment change are
  **reported** for the W-23 review and do not by themselves refuse; the derived results in full, reported likewise;
  `ENVIRONMENT_VERIFIED.json`; a backup attempted. **The test suite is not run by `Verify_Tree`:** the tests live in
  DEV and the installed software starts no program; the command says so every time. A failed smoke case writes no
  marker and removes an older one." (The rest of the paragraph unchanged.)
- *Specification section 13, "Verified before use", to read:* "`Verify_Tree.bat`, run in the tree, makes the checks of
  12.3 that travel with the installed software (items 1, 4 and 5, and every installed variant's smoke case) with that
  tree's Python and, on success, writes ..." (the rest unchanged); and item 3 of 12.3 gains: "The suite is run by the
  install tools in DEV (at a tree's creation and at an infrastructure reinstall), never by `Verify_Tree`."

## 4. One conflict between a ratified text and a reviewed one (reading C-R9)

Design section 6 has `Reinstall_Infra` take the target's job lock at step 2 and hold it "to the end", and attempt its
`PRE_INFRA` backup at step 4. Slice B, as reviewed, never makes a backup while a job lock lies in the tree (the lock
file would be inside the ZIP, and a restored tree would refuse every job). **Reading taken:** the lock is held for
step 3, let go for the kit, the backup and the question, and taken again by an exclusive create with a fresh process
check before anything is overwritten, as an ordinary install does at its step 6; a job that began meanwhile refuses
the reinstall there, nothing overwritten, nothing ended. Step 9's full comparison is made under the second hold. The
other way (a backup that leaves out a lock its caller holds) changes reviewed slice B code and the restore's exact set.

## 5. The readings taken (in full in `SLICE_C_PLAN_AND_NOTES.md`, section 3)

- **C-R1** the smoke case's table ends at the first draw the variant declares it can forecast, and that draw is the
  target; any answer but a complete FORECAST fails, and so does any error.
- **C-R2** the fixed sample: of each variant's stored FORECAST lines in each game, the first, the middle and the last.
- **C-R3** the derived results are read as the job reads them and nothing is written; a difference the tree already
  marks is reported as known.
- **C-R4** software and data may lie in two folders; status files are read where the software lies and never created.
- **C-R5** at `Verify_Tree` only a failed smoke case withholds the marker and removes an older one; a difference in the
  sample or in the derived results is said in capitals and does not withhold it, because the tree's own remedy (the
  research job marks it not current; the owner runs the rerun) cannot start without a verified environment.
- **C-R6** a refusal of `Verify_Tree` leaves the marker as it was; one log line for either verdict.
- **C-R7** the `checks` command only finds and tells; what stops an install is the tool's to decide.
- **C-R8** the suite of an install is the test modules whose subject is on the infrastructure manifest
  (`deploy/SUITE_MANIFEST.ini`, 23 modules; a test holds the list to exactly those that exist); its temporary copy is
  what the project's own walk calls the project (`src/`, `deploy/`, `tests/`, root files), never `ENVIRONMENT.ini`.
- **C-R10** the ending: the list, the log line, the updater's lock released, the barrier removed last.
- **C-R11** only `YES` in capitals proceeds.
- **C-R12** what stops an ordinary install after copying: a failed smoke case, unreadable stored records, a sample
  difference, an unexpected derived difference; a program that ended otherwise than with 0 means nothing passes.
- **C-R13** `Init_Tree`: the marker is written by the tree's own Python (`checks --write-marker`, only after every
  smoke case, in the tree itself); the accepted results of a game are three files; QA's results come from PROD once a
  PROD tree exists and from DEV until then; the kit is attempted before the list and the log line; a continued
  creation asks nothing; the pause ends with exit code 3.
- **C-R14** `Install`: a helper the target holds with other bytes refuses the whole command before any backup; step 2
  is a look and step 6 the reservation; a continued install attempts no new backup and asks nothing; if the stop came
  after the list was written, the list as it was before is worked out from the barrier's plan.
- **C-R15** `Reinstall_Infra`: "any forecast-class file" covers a file added, overwritten or removed **and a file moved
  into or out of the forecast class with its bytes unchanged** (the identity of the forecasting code is taken over
  exactly that class); the software as it would be is DEV's infrastructure with the tree's variants; where a change
  from draw X was accepted the cutoff is written, the stale reports moved out and both checked, and nothing is
  recomputed; the print-outs are made again when a `derived`-class file changed; `--replace-unfinished` works its plan
  out from the files as they lie in the tree.

## 6. Evidence (cloud: Linux, Python 3.15.0b4, numpy, scipy, psutil), in `slice_c/evidence/`

- **The whole suite on the slice's final files:** 68 modules, 1334 tests; the three known failing tests and no other
  (`whole_suite_MODULES.txt`). Compared with `main` and with slice B's run: no test changed or disappeared beyond what
  slices A and B already explained (`whole_suite_compared_with_main.txt`, `..._with_slice_b.txt`).
- **The suite of an install, run by the tool itself** (`suite_on_copy.run_suite`) with the workspace's Python on a
  temporary copy of 770 files: 23 modules, 763 tests, passed; the copy removed (`suite_of_an_install_on_a_copy.txt`).
- **Planted faults,** one at a time, in every new source file (`mutation_check_slice_c1.py`, `_c2a`, `_c2b`, `_c3`,
  `_c4`, `_c5`, beside the notes): 250 in all; all caught, 11 of them only after a test was added for the fault.
- **A creation on the project's real software** (`cloud_creation_*`): all 40 real variants marked ready and planned;
  168 files copied, 40 status files, the six results files; the same command again passing over all of it. Then,
  with a real Python environment built inside that tree, `install_common.checks_with_target_python` started the
  `checks` program for real: **all 40 real variants gave a complete forecast for both games on the invented table
  with exactly their declared minimum history (80 smoke cases);** the same call with another Python was refused.
  None of these files holds a draw value.

## 7. Not proved in the cloud; kept for the joined Windows rehearsal

The second half of a creation with a real Windows environment (the marker's digest takes the Windows layout); the
launchers; `python.exe` by its Windows path; the suite run by the tool with a tree's Windows Python; the times a
backup, the suite and the derived check take on the owner's PC; `Reinstall_Infra` and `Install` end to end with a real
target Python (their unit tests stand in for its start, and the stand-in imports the variants from the folder the
software lies in, as the program does).

## 8. Carried, not part of this slice

For the joined package of build step 3, as agreed at EX_327: tests that make a link must skip where Windows refuses
(the new tests of this slice that make one already skip); the early refusal's line "no research was written"; and one
docstring in `src/research/environment_marker.py` that holds a single backslash before "s" (a SyntaxWarning on Python
3.15).

## 9. What is asked of the reviewer

A review of slice C against deployment design v0.12 sections 3 to 9 and specification v0.6 sections 12 and 13: the
files of section 2; the amendment of section 3; the reading of section 4; the readings of section 5. As for slices A
and B: findings narrow and direct; no install, run or PC operation is authorised by a PASS.
