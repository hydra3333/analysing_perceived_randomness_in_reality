# MHUP-A integrated package - item 3 follow-up: N5, N4, release-record guard, recovery, F2 rows 8-9 (11 November 2026)

By the Claude web chat (Opus 5.5), after the owner's yes to N5 option A in principle and to N4 (11 November 2026, 08:21) and
the reviewer's item 3 review (`exchange/HO2_2026_11_10/MHUPA_Item3_N5_F2_ChatGPT_Review_2026_11_11.md`). Not an EX message.
US-ASCII, CRLF. Everything is **PRELIMINARY, on a DRAFT package**; nothing frozen, reviewed, installed or run on real data.
Base `main` `c48ac3c`; working date 2026-11-10. Draft manifest SHA-256: see `evidence_2026_11_11b/PRELIMINARY_BUILD_REPORT.txt`.

## 1. What changed

| Change | Where | Kind |
|---|---|---|
| **N5 option A:** step 10 runs the suite on a barrier-free byte copy; the live tree stays barred | the package's suite runner, `--shadow` (install-time tool only) | no production code, no reviewed test changed |
| **N4:** `-text` for `src/package_tools/process_check.py` and `tests/fixtures/results_master_v0_1_reference.py.txt` | `.gitattributes` (already a package file since N1) | owner-approved |
| **N4b (owner-approved, 11 November 2026, 09:32):** `-text` for `src/results_master_v0_2.py` | `.gitattributes` | the same updater test has a third raw-bytes assertion (no CR in the new updater), hidden until the first two were fixed; a search of every test finds no other |
| **Reviewer's point A:** the release-record tool refuses, before writing the permanent record, unless U is held by this package and no released method still has its IN_DEVELOPMENT flag (E) | `src/package_tools/install_records.py`; one new test in `tests/test_mhupa_install_records.py` (suite 570 -> 571) | a change to reviewed code, for the reviewer |

All are made by counted edits in `apply_item3_changes.py`, which `build_dev_integrated.sh` runs last. The package shape is
unchanged: 37 new, 34 modified, 1 deleted.

## 2. The step 10 runner (N5) against the reviewer's five requirements

1. **Starts only after POST PASS, with the live barriers intact.** It runs the verifier's POST phase on the live tree first
   (U held by this package; E and P present and this package's; exactly the package's changes), and again after the suite,
   also after any failure. It never touches a barrier.
2. **An ordinary byte copy, isolated.**
   - The copy goes into a new temporary folder outside the live tree.
   - It is made of plain file copies, never links, of every tracked code and test file plus the package's new files (minus
     the deleted file and the barriers).
   - Each copied file is compared byte for byte with the live file, and each package file also with the manifest.
   - An escape check runs under the suite's own environment: ten key modules must import from the copy, and nothing on the
     import path may be in the live tree.
3. **Data: only what the tests need.** I ran the whole suite on a copy with no data at all. Exactly one module
   (`test_multigame_reader_contracts`) needed data: the development masters, ledgers and INIT records. So the copy
   receives exactly those six files and nothing from `results/` or `transitory_data/`. At an install before Approval 2
   they hold development draws only. The ad hoc full-copy script was evidence of feasibility only and is not used.
4. **Any failure is a step 10 STOP.**
   - It prints `SUITE STOP ... do not run step 11`.
   - E, P and U stay in place.
   - The temporary folder, and only that folder, is removed after a name and location check, also on a STOP.
5. **Evidence** (`evidence_2026_11_11b/`):
   - The full positive path, steps 0 to 18 with step 10 and with N4, on a full LF clone (Python 3.13) and a full
     `core.autocrlf=true` clone (Python 3.15).
   - Step 10 negatives, 9 checks, 0 failed:
     - live P missing, live P foreign and live U foreign: each refused before copying;
     - a changed file in the copy: refused before the suite;
     - the import path reaching into the live tree: refused;
     - a failing suite: STOP, then the live tree is checked again and is still barred;
     - a test writing an untracked file into the live tree: STOP (POST sees it);
     - a test writing into a Git-ignored path of the live tree: STOP (the before/after listing sees it);
     - a test changing a file in the copy: STOP.
     In each case U, E and P were checked afterwards and no temporary copy was left.
   - The full suite in a fresh `core.autocrlf=true` clone of the installed tree (N4).

**The Appendix J amendment, for ratification with the package (proposed wording):**
- **Step 10, Action:** "The suite, run by the package's suite runner in `--shadow` mode: after a fresh POST PASS on the live
  tree, it copies the installed files byte for byte into a new temporary folder without the barrier files and runs the
  suite there; the live tree keeps U, E and P throughout and is checked again afterwards."
- **The negative-test sentence**, which replaces "the suite fails if P is absent at step 10 in the rehearsal": "the step 10
  runner STOPs before copying if the live P (or E, or U) is missing or foreign, STOPs if the copy differs from the live tree
  or the import path reaches the live tree, and STOPs if the live tree gains any file during the suite; P's own refusals are
  tested in `test_mhupa_gates` and `test_e2r_dispatch`."

## 3. Reviewer's point B: a fix after step 13 or step 17 (proposal)

- The verifier proves only the two-commit shape, on purpose. If COMMITTED (step 13) or RELEASED (step 17) STOPs after a
  commit exists, the install is not fixed forward in place.
- The proposed recovery is abandon and rebuild:
  1. E, P and U stay.
  2. Nothing is pushed.
  3. Claude writes reviewed restore steps for that case: one `git revert --no-edit` per install commit, newest first, which
     keeps every commit and its identity (no reset, no history rewrite); then E and P are removed after a fresh CLEAN; U is
     released last.
  4. A new package candidate, with a new name and its own records, is built on the resulting HEAD and goes through its own
     review and evidence.
- Nothing is pushed at any point before step 19, so the owner can alternatively keep the unpushed local commits for Claude
  to inspect first.
- The instructions' STOP texts for steps 13 and 17 will say "send the output; Claude writes the reviewed recovery; do not
  continue". No recovery is authorised by the ordinary procedure.

## 4. F2 rows 8 and 9, corrected

**Row 8: CLEAN at the real project root, the ordinary desktop (Claude Code and a console open there).**
- **Who:** the owner, in his own CMD window. Claude Code may not run the tool at the real root.
- **Command:** `process_check.py check-no-runs --root REAL --install MANIFEST`, run from the staging folder.
- **What it reads:**
  - the process table: name, parent and command line of every process; executable, folder, command line and start time of
    Python processes;
  - `.venv\pyvenv.cfg`;
  - whether `src`, `source_data`, `results` and `.git` exist;
  - whether each game's `results\real\weekly\<GAME>\ACTIVE_SESSION.lock` exists;
  - if `source_data\.results_master.lock` exists, its one line of lock text;
  - because MHUP-A changes the roster, the weekly ledgers `results\real\weekly\<GAME>\sessions\SESSION_*_attempts.jsonl`
    and `FORECAST_LEDGER_V1.jsonl`. These do not exist before MHUP-B, so in practice nothing is read; if they existed, it
    would read their ticket lines and print only the target draw numbers of an unfinished set.
- **What it writes:** nothing (without `--game` it writes no resume token).
- **What it prints:** `CLEAN`, or one line per listed process (PID, start time, parent chain, executable, folder, command
  line) and `REFUSED`. No draw value is printed.
- **Expect:** `CLEAN`.
- **Known false positive:** a VS Code Python helper process started at the root is listed. The owner closes it and reruns;
  nothing is terminated by the tool.

**Row 9: a live `Run_Experiment.bat` child is listed.**
- **Who:** the owner, in two CMD windows at the real root. Claude Code may not launch anything (rule 7).
- **Precondition:** no orphan marker. `dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json` must print "File Not Found";
  otherwise do not run this row.
- **Window A:** `Run_Experiment.bat POC_Coordinator_Probe.py --poc --case=sleep-timeout --sleep-seconds 120 --run-id
  poc-T016-row9-YYYYMMDDHHMM` (a fresh id each time, made from the date and time).
  - This is the existing engineering-only probe: no lottery data, no coordinator.
  - It sleeps 120 s, then ends by itself with `FINISH POC_Coordinator_Probe SUCCESS`.
  - It writes only `transitory_data\poc_runs\<id>\status.json` and `canonical_result.json`. That folder is ignored by Git,
    so it never shows in `git status` or affects a later clean-tree check. The files can stay; they are harmless.
- **Window B, within those 120 s:** the row 8 command. Expect `REFUSED`, listing the probe's processes, each with its PID and
  start time: the venv's `python.exe` (rule (a)), with its folder `src\methods` under the root (rule (b)) and the root on its
  command line (rule (c)).
- **Window B again, after window A shows `FINISH ... SUCCESS`:** expect `CLEAN`.
- **Nothing is terminated.** If the probe does not end by itself, the owner waits, or closes window A himself; the check's
  output is sent to Claude either way.
- **If not approved:** the oracle is reported unmet. A bare sleeping Python is not offered as an equivalent.

**What rows 2 and 3 now prove (N5):**
- **Row 2** (the suite in a normal task clone) is evidence for the installed bytes on Windows.
- **Row 3** (steps 1 to 18 in the synthetic, data-free clone) cannot run the step 10 suite, because there the copy would have
  no masters. So T016 runs step 10's `--shadow` mode in a full task clone instead: either as its own step, or by running the
  whole of row 3 in a full clone, where the tools read nothing but the masters the tests need.
- The cleaner choice for T016 is to run steps 0 to 18 in a **full** task clone, with the suite in `--shadow` mode. The live
  install itself then needs no additional owner rehearsal beyond T016.

## 5. For you to decide

1. **N4b:** the third `-text` line, for `src/results_master_v0_2.py` (recommended: yes; same reason as N4).
2. **Point B:** the abandon-and-rebuild recovery (recommended), reviewer first.
3. **F2 rows 8 and 9:** your view on running them yourself at T016 time; reviewer first.
Then, on Opus: rulebook v0.5 and the T016 task for their focused review (Route A).

## 6. After the reviewer's follow-up on fadd2b9 (11 November 2026, owner away; Opus 5.5)

Review: `exchange/HO2_2026_11_10/MHUPA_ChatGPT_N4b_N5_F2_Followup_2026_11_11.md`. Evidence: `evidence_2026_11_11c/`.

**N5-C01 (done): a temporary copy that cannot be removed is a STOP.**
- The step 10 runner now ends with `SUITE STOP: the temporary copy could not be removed completely` (or "failed the removal
  check"), and step 10 has not passed. U, E and P stay.
- It removes only the one folder it made, after the name and location check.
- New negative (step 10 negatives now 10 checks, 0 failed): the removal is made to leave the folder in place, as a locked
  file would on Windows; the runner STOPs, the barriers are intact, and the harness removes the leftover.

**N5-C02 (confirmed): exactly six data files, and no reach into the live tree.**
- Each of the six files is needed: removing any one of them makes `test_multigame_reader_contracts` fail
  (`N5_C02_each_data_file_needed.txt`). The whole suite with no data at all fails only that module.
- Imports: the escape check stays. Writes: the before/after listing of the live tree, ignored files included, stays.
- **A Windows defect found and fixed here.** On the owner's PC the venv is `.venv` inside the repository, so Python's own
  import path includes the venv's `site-packages`. The escape check refused anything on the import path inside the live
  tree, so it would have STOPped every time on Windows (it passed here only because the test venv sat outside the clone).
  Now the project's own `.venv` is allowed: it holds the interpreter and installed packages, not project code. Proven by
  running the step 10 runner with a venv inside the tree (`N5_C02_venv_inside_tree_shadow_py315.txt`).

**REC-C01 (done in the draft instructions): a fix after step 13 or 17.**
- Step 13's and step 17's STOP texts now say: do not push and do not continue; the recovery is proposed by Claude for that
  exact state, checked by the reviewer and approved by the owner.
- The normal route: a fresh install check showing `CLEAN` before any change; reviewed `git revert` commits (nothing reset,
  rewritten or deleted; every commit and record, including a release record already committed, stays in the history); E and
  P removed after another `CLEAN`; U released last; a new package built and reviewed on the resulting commit.
- Before the release commit exists, step 17 keeps its ordinary fix-and-rerun.

**F2-C04 (noted, for the rulebook v0.5 and T016 round).** Running T016 in a full clone means the runner reaches the six master
files through two programs, not only through the accepted tests: the package's suite runner copies them (bytes only, not
parsed or displayed) for step 10, and `process_check.py` tests whether lock files exist and reads the lock text.
Rulebook v0.5 and the T016 task must say so exactly. Nothing is drafted yet.

**Where the draft instructions differ from the ratified Appendix J** (each needs the reviewer and the owner's ratification
before it supersedes the table):

| Step | Ratified table | Draft | Kind |
|---|---|---|---|
| 10 | the suite with P present | the suite on a barrier-free copy; the live tree barred throughout | N5: needs the amendment in section 2 |
| 10 (negative tests) | "the suite fails if P is absent at step 10" | the step 10 runner's own STOPs (section 2) | N5: amendment |
| 13 STOP | "Claude writes the fix (a further small package commit, or a reviewed revert commit), COMMITTED is rerun, then steps 14-19" | abandon and rebuild, approved for the exact state | REC-C01: amendment |
| 17 STOP after the release commit | "after the fix, delete P and rerun from step 17" | abandon and rebuild | REC-C01: amendment |
| 12 and 17 | stage; `git status`; commit | stage; the verifier's `staged` check; commit only if it passes | stricter, added |
| 15 | delete E, then P | removing E refuses unless COMMITTED passes at that moment | stricter, added |
| 16 | the record tool's refusals as listed | also refuses unless U is held by this package and E is gone | stricter (reviewer's A) |
| 18 | release U | release U only if RELEASED passes at that moment | stricter, added |
| 0 | `git status`; `git pull` | 0a (names for the window, repeatable), then status, then pull | presentation |

Two wording points in design 4.3, also for the amendment: the baseline holds "40 entries" per game (80 in all); and
`post_pass_utc` in the install record is the time of step 12, not of the POST check.

**Evidence (PRELIMINARY; all on the rebuilt draft):** listed in `evidence_2026_11_11c/`; results in the report to the owner.

