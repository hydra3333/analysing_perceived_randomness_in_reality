# Build step 3 (trees, installs, backups and restore; then the transition check and PROD's first job) - build plan v0.1

**Date:** 24 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status:** a working plan, not a design
and not a rule. The authority is the specification v0.6 (sections 12.1 to 12.6, 13, 14.1, 17.3, 17.4), the deployment
design v0.12 and the coding practices (RAT-40). The owner's go: decision log entry 217. Nothing here authorises any
operation on the owner's PC.
**Why it exists:** so that the build can be followed, redirected early, and resumed by another chat. Each choice the
ratified documents leave open is marked RECOMMENDED, with the alternative. Section 7 lists what the owner decides.

## 1. The work item

- **Item:** build step 3 of specification 17.4: `Init_Tree`, `Install`, `Reinstall_Infra`, the checks, backups, the
  recovery kit and the restore; then the transition check and PROD's first job. **After it PROD exists and forecasts
  every week, the prevailing OV-1 begins, and new methods can be added.**
- **Risk tier:** HIGH for the state machines (the install and its barrier, the backup, the restore), for the
  results updater and for the launch guard. They decide whether a tree can be trusted and recovered.
- **Author:** Claude. **Reviewer:** the ChatGPT reviewer chat (H-2 v6).
- **Not in step 3 (step 4):** the QA software replacement from PROD, the research-data reseeding, the historical
  walk-forward rerun, `Correct_Shared_Code`, `Check_Forecasts`, `Who_Uses` and `Make_Successors`. Step 3 is built so
  that step 4 adds to it and does not change it (specification 17.4).

## 2. What step 3 delivers

| Command or part | Where it runs | What it does | Authority |
|---|---|---|---|
| `Make_Installable.bat` | DEV | writes a variant's readiness marker, or the infrastructure's (`deploy\INFRA_IS_INSTALLABLE.json`); the marker is the whole of readiness | spec 12.2; design 3.1, 3.2 |
| `Check_Tree.bat <role>` | DEV | read-only: how the settings are read and what each check finds; lists a tree's backup ZIPs | design 1, 10 |
| `Init_Tree.bat QA\|PROD` | DEV | creates a tree: settings file written once, infrastructure and ready variants copied, accepted results copied, then stops for the owner to build `.venv`; typed again it verifies and finishes | spec 12.5; design 4 |
| `Install.bat PROD\|QA` | DEV | adds ready variants a tree lacks; add-only; one question for the batch; the smoke case of each new variant | spec 12.3; design 5 |
| `Reinstall_Infra.bat PROD\|QA` | DEV | replaces infrastructure of the `derived` and `other` classes; says before the question what it would change in stored results; refuses any `forecast`-class file | spec 12.4; design 6 |
| `Verify_Tree.bat` | in the tree | checks the tree with its own Python and writes `.venv\ENVIRONMENT_VERIFIED.json` | spec 13; design 7 |
| The launch guard | in every tree | settings, no unfinished operation, the environment's digest, every installed file equal to `INSTALLED_FILES.json`, the process rule | design 9 |
| `Run_Snapshot.bat`, and a backup at each job's end | in the tree | one ZIP of the whole tree, checked twice, only when the tree is quiet; `SNAPSHOT_DUE` | spec 14.1; design 10 |
| The recovery kit and `Restore.bat` | from an unpacked kit | puts back exactly one chosen backup at the path it came from; the old tree renamed aside | spec 14.1; design 11, 12 |
| `Run_Results_Updater.bat` with `results_master_v0_3.py` | PROD only | the owner's reviewed source of results, as a clean-sheet edition (section 5) | spec 7.1; entry 181 |
| The results step in each role | in the tree | PROD: the updater; QA and DEV: a copy of PROD's accepted results (`[results] copy_from`) | spec 7.1; design 1 |
| The transition check | once, in QA | every forecast the old system kept, against the new lists made in QA | spec 17.3 |
| The half-finished states | everywhere | the barrier; the same command finishes; nothing names a backup it did not make | design 8 |

## 3. Decided already by the owner (not reopened here)

- No parallel or multi-threaded runner now (entry 180).
- **The updater is a clean-sheet new edition,** `results_master_v0_3.py`: every Mode H state removed; every genuine
  source, parse, overlap, chronology, ledger and lock check kept and proved unchanged; `v0_2` left untouched in DEV
  (entry 181). The reviewer's stated preference was a narrower correction; it is put to the reviewer as the owner's
  decision, with section 5's proof.
- Line endings pinned to LF for the project's code in `.gitattributes`, before the first tree is made (entry 181).
- **The places:** PROD `G:\a_p_r_i_r`; QA `T:\a_p_r_i_r`; backups `T:\a_p_r_i_r_backups\PROD` and `\QA` (entry 181). QA's
  backups share QA's drive: allowed, with the printed warning of design section 1 item 5.
- Rehearsals as Claude chooses; the runner in scratch trees under `D:\DELETE_ME\` (rulebook v0.7 section 2A).
- `ENVIRONMENT.example.ini` is rewritten (entry 211). A tree's `.venv` is built by the owner from a plain CMD window
  (entry 202): `Init_Tree.bat` says so when it stops for it.

## 4. RECOMMENDED: four code slices, each reviewed by itself, and one install into DEV at the end

Build step 2 went to the reviewer whole and needed four rounds. Step 3 is larger and its parts depend on each other
in one direction, so it is cut where a reviewer can judge a part by itself.

| Slice | Holds | Why here |
|---|---|---|
| **A. Foundations** (DEV only) | the LF pin; the rewritten settings example and the reader for `[QA]`, `[PROD]`, `[results]` with every check of design section 1; the two markers and `Make_Installable.bat`; the static import check and the manifest's `[install_tool]` list; `INSTALLED_FILES.json`; the environment digest; `Check_Tree.bat`; the launch guard with the process rule (the reviewed `src\package_tools\process_check.py` is reused) | everything later reads these; none of it creates or changes a tree |
| **B. Backups, the kit, restore** | `Run_Snapshot.bat`, the job's backup at its end, `SNAPSHOT_DUE`; the recovery kit; `Restore.bat` with the hand-unzip reconciliation and the orphan-marker exception | an install must be able to attempt a backup; restore is the way out of everything else |
| **C. Trees and installs** | `Init_Tree`, `Install`, `Reinstall_Infra`, `Verify_Tree`; the barrier and every state of design section 8; the smoke case; the results step in each role | uses A and B |
| **D. The updater** | `results_master_v0_3.py` and its launcher, PROD only | independent of B and C; can be reviewed beside them |
| **E. The transition** (sheets and one tool) | the transition check; the owner's sheets for `Init_Tree QA`, the check, `Init_Tree PROD` and PROD's first job | last |

- **Each slice goes to the reviewer as its own EX package** (a code package with its evidence), on the owner's word.
- **RECOMMENDED: nothing is installed into DEV until slices A to D have each passed and been rehearsed.** The runner
  rehearses each slice in a task clone and scratch trees, which needs no install in DEV. Then one cumulative package
  is installed in DEV from one sheet (about an hour of the owner's time, once). *The alternative:* install each
  slice in DEV as it passes: four sheets, four pairs of suite runs, and earlier use of `Check_Tree` and
  `Make_Installable` in the real DEV. It is safer against a late surprise and costs the owner three more hours.
- **RECOMMENDED: a short probe task first** (TASK_T028, scratch only, a few minutes), before slices B and C are
  coded: on the owner's PC, what the standard library reads from Windows' process table; how a rename behaves when
  the old file is open; how long a ZIP of a whole tree with its `.venv` takes and how large it is. These are the
  three things the cloud cannot tell, and the state machines are designed around them.

## 5. The clean-sheet updater: what is promised, and how it is proved

- **Kept, each with a test that maps to a test of `v0_2`:** the one source and its exact host; the parse; the
  overlap with the draws on file; chronology; the version ledger and the verification records; the lock; the
  refusal outside PROD (new: by the settings file's role).
- **Removed:** every Mode H state: the opening record `HOLDOUT_OPENED_<GAME>.json` as a precondition, the holdout
  boundary, and anything that reads or writes a seal.
- **Proof:** `v0_2` and `v0_3` run on the same invented source pages (the cases of `v0_2`'s own offline self-test, and
  more invented pages) and on the same starting masters give byte-identical masters and ledgers; a table lists
  every check of `v0_2` and where it is in `v0_3`, or why it is gone; planted faults in each kept check. `v0_2` is
  1,270 lines and its tests compare it with `v0_1` by syntax tree: the same method is used for `v0_3`.
- **Never by Claude:** a live run. Claude contacts no lottery website. The owner's first real update with `v0_3` is
  his own go, in PROD.
- The old checks of `contract_dispatch.py` and `master_versions.py` that consult the opening record belong to the
  old runner, which is not installed in any tree; the new reader of step 2 does not consult it.

## 6. How it is proved (the lessons of step 2 applied)

- **Invented trees in temporary folders,** three roots each: every check of design section 1 with one wrong setting;
  every step table with a fault planted after every step, then the command again; every state of section 8; the
  test list of design section 15 is the checklist, item by item, and the package note says which test covers which.
- **Made-up records in the real form before the first package,** for every tool that reads something only the
  owner's PC holds (the lesson of TASK_T026).
- **The whole suite before and after,** test by test; planted faults for every check a package relies on; the install
  rehearsed in an LF clone and a CRLF clone.
- **Every sheet's builder checks every path and says what must exist before the sheet starts** (entries 209, 210).
- **The Windows rehearsal by the runner,** in scratch trees with the roles DEV, QA and PROD under `D:\DELETE_ME\`,
  following design section 15's list: both `Init_Tree`s, an install into each, a reinstall, an install with a fault
  planted and the command typed again, jobs ending in backups, a withdrawal, a backup of a tree of the real size, a
  restore from the kit. The design's list says "invented data only"; rulebook v0.7 (later, entry 184) allows real
  results in the scratch folder, and the first fill needs them to be of the real size. **Two things the runner
  cannot do** and the owner does himself, from a sheet, in scratch: build each scratch tree's `.venv` (a plain CMD
  window), and the restore's restart of the PC. The runner also cannot delete: the owner clears the scratch folder.
- **Then the real sequence, each step the owner's own go** (specification 17.3): `Init_Tree.bat QA`; the transition
  check in QA; `Init_Tree.bat PROD`; PROD's first job.

## 7. What the owner decides now

1. **Slices and installs** (section 4): four reviewed slices and one install into DEV at the end (recommended), or
   an install per slice.
2. **The probe task first** (section 4): yes (recommended) or no.
3. **QA before PROD** (specification 17.3 recommends it and does not require it): `Init_Tree QA` and the transition
   check there before PROD exists (recommended), or PROD directly. The early comparison in DEV already found all
   20,436 old forecasts equal, so the check in QA is expected to pass; it is still the one made by an installed tree.
4. **Whether this plan goes to the reviewer before slice A is coded** (recommended: yes, for its slice boundaries
   and section 5), or only with slice A.

## 8. Known unknowns

- What the standard library can read of another process on this Windows (its executable, working folder, command
  line, start time): the process rule and the restore depend on it. The probe answers it.
- The size and time of a backup that holds a whole `.venv`. If it is long, the job's backup at its end is still made
  (the design leaves no option), and the time is told to the owner before PROD is created.
- Whether `T:` and `G:` are ordinary local volumes with no substituted drive or junction in the paths: the settings
  check refuses otherwise. `Check_Tree.bat` will say; the owner's `U:` is a substituted drive and is not used.
- Each week before PROD's first job is one draw of each game that cannot count in the prevailing OV-1, which begins
  at the first draw after PROD's first successful results step. That is a reason not to dawdle, and no reason to
  cut a check.

## 9. Models

Fable (High) for slices B and C (the state machines) and for slice D's proof design. Opus for slice A's plainer
parts, the sheets, the task files and the records. The owner switches; Claude says when a Fable task is finished.
