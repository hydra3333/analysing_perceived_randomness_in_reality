# Build step 3 (trees, installs, backups and restore; then the transition check and PROD's first job) - build plan v0.1r1

**Date:** 24 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status:** a working plan, not a design
and not a rule. The authority is the specification v0.6 (sections 12.1 to 12.6, 13, 14.1, 17.3, 17.4), the deployment
design v0.12 and the coding practices (RAT-40). The owner's go: decision log entry 217. Nothing here authorises any
operation on the owner's PC.
**Why it exists:** so that the build can be followed, redirected early, and resumed by another chat. Each choice the
ratified documents leave open is marked RECOMMENDED, with the alternative. Section 7 lists what the owner decided.
**v0.1r1 (24 November 2026):** the reviewer's four focused corrections of EX_299, as narrowed by EX_300, are made
(S3P-C01: section 5; S3P-C02: sections 4 and 4A; S3P-C03: section 6; S3P-C04: section 6A), and the owner's four
decisions are recorded in section 7 (decision log entry 219). Nothing else is changed; v0.1 stays in the
repository as it was, and `STEP3_BUILD_PLAN_v0_1_TO_v0_1r1.diff` beside this file is the exact difference.

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
| **A. Foundations** (DEV only) | the LF pin; the rewritten settings example and the reader for `[QA]`, `[PROD]`, `[results]` with every check of design section 1; the two markers and `Make_Installable.bat`; the static import check and the manifest's `[install_tool]` list; `INSTALLED_FILES.json`; the environment digest; `Check_Tree.bat`; the launch guard with the process rule (the rule and the refusals of the reviewed process tool are kept; the file itself is not reused: section 4A) | everything later reads these; none of it creates or changes a tree |
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
- **A short probe task first** (TASK_T028, scratch only, about a quarter of an hour; the owner agreed, entry 219):
  on the owner's PC, what the standard library reads from Windows' process table and what psutil reads, side by
  side; how a rename, a replacement and a removal behave when a file is open or another program sits in the
  folder; how long a ZIP of a whole tree with its `.venv` takes and how large it is. These are the three things
  the cloud cannot tell, and the state machines are designed around them. The task file is written
  (`CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` and its probe); it runs only after the reviewer has read
  it and on the owner's own go.

## 4A. Reading Windows' processes: what is kept, what is not reused, and one question (EX_299 S3P-C02; EX_300)

- **The fact (the reviewer is right).** `src\package_tools\process_check.py` reads the process table through psutil
  and also holds the old system's lock clearances and Mode H figures. It cannot be installed as the new system's
  process check. v0.1 said it was "reused"; what is kept is **its rule and its refusals**: a Python process whose
  details cannot be read is a refusal, never a pass; ancestors are examined; no program ever ends a process.
- **Two different questions are asked of the process table** (deployment design section 9):
  (1) *the restore:* "is any Python program at all running on this PC, other than this restore?" This needs each
  process's program name, its parent and its start time, and nothing more. The standard library reads those from
  Windows directly, in a few dozen lines.
  (2) *every other rule:* "is another Python process **of this tree** running?" (its program file is the tree's,
  or its working folder is under the tree, or its command line or an ancestor's names the tree). The working
  folder and the command line of another process are **not** readable with the standard library except by
  hand-written reading of that process's memory, which is exactly the fragile part psutil exists to do.
- **Where psutil is available:** in every tree's own environment (it is one of the 39 packages the owner's
  environment script installs) and in DEV's. **Where it may not be:** in whatever Python runs a restore from an
  unpacked kit when every tree is unusable.
- **RECOMMENDED (for the owner; see section 7 item 5):** the restore keeps its ratified contract (the kit, the
  backup and any installed Python; standard library only), with its own small reader for question (1); every
  other check uses **one** new psutil reader written for the new system. That is two readers, but for two
  different questions, and the second is the one already proved in use. It needs one narrow amendment, for
  ratification: the deployment design section 2 says the install tools in `deploy\` are "standard library
  only", and the same design's section 9 gives them the process rule that needs psutil; the amendment would say
  "standard library only, except the process rule, which uses psutil from the Python that runs the tool".
  *The alternatives:* (a) psutil for the restore too: one reader, but a restore then needs a Python that has
  psutil, checked before anything is touched, and the kit's promise "any installed Python" is weakened;
  (b) the standard library for everything: hand-written memory reading, which Claude advises against.
- **Nothing is relaxed either way:** the scopes of section 9 stay as they are, an unreadable process refuses, and
  the restore is tested from an unpacked kit with no tree's environment in reach.
- TASK_T028 shows both readings on the owner's PC before any of this is coded.

## 5. The clean-sheet updater: what is promised, and how it is proved

- **Kept, each mapped and tested** (the reviewer's inventory, EX_299 S3P-C01, to be confirmed line by line
  against `v0_2` when slice D begins): the exact official HTTPS host and the final address after every redirect;
  no fallback source; refusal of a block or challenge page; the browser's pacing; the date windows and the era
  and number validation; the completeness of a source page; chronological, contiguous updates; the overlap with
  the draws on file; the integrity of master and ledger; create-only grabs and backups; a correct `NO_CHANGE`;
  the verification records; the updater's lock; and the refusal outside PROD (new: by the settings file's role).
- **Removed:** every Mode H state: the opening record `HOLDOUT_OPENED_<GAME>.json` as a precondition, the holdout
  boundary, and anything that reads or writes a seal.
- **Proof (corrected, EX_299 S3P-C01; v0.1 wrongly promised byte-identical ledgers and a syntax-tree comparison).**
  `v0_2` and `v0_3` are run on the same invented source pages (the cases of `v0_2`'s own offline self-test, and
  more) and the same starting masters, `v0_2` in a made-up opened state so that its Mode H precondition is not
  what refuses. Then:
  - **Equal byte for byte:** the master CSV; and so the accepted draws, in order. **Equal case by case:** whether
    each case was accepted or refused.
  - **The version ledger and the verification records are compared field by field,** not as bytes: the version
    progression, `UPDATE` or `NO_CHANGE`, the master's hash, the range and the counts, the added range, the
    content hashes of grabs and backups, and that history is only ever appended to. **The only differences
    allowed are a written list of truthful provenance fields** (the tool's version and its own SHA-256; times
    and the names made from them). Nothing is normalised away beyond that list, and no tool identity is faked.
  - **A refused case leaves master and ledger untouched;** a diagnostic grab it is allowed to keep is recorded
    correctly.
  - **Old ledger rows stay as they are:** a made-up ledger with rows written by `v0_2`, then an `UPDATE` and a
    `NO_CHANGE` by `v0_3`: the old rows are byte for byte unchanged and keep their own tool's name; the new rows
    name `v0_3`.
  - **No Mode H:** `v0_3` runs with no opening, freeze, holdout, seal or session record present, and a test shows
    it neither reads, writes nor asks for one.
  - **A table lists every check of `v0_2`** and where it is in `v0_3`, or why it is gone; each kept check has
    normal, edge and planted-fault cases on invented data. A syntax-tree comparison is used only for a helper
    that really is unchanged; it does not certify the rewrite.
- **Never by Claude, the reviewer or the runner:** a live run. Claude contacts no lottery website, and the
  runner's rulebook forbids the updater in every version, in scratch trees too (v0.7 section 2A item 6). Its
  tests use offline, injected pages; on Windows they run only inside the suite. The owner's first real update
  with `v0_3` is his own go, in PROD.
- **The launcher:** `Run_Results_Updater.bat` today starts `v0_2`. The package of slice D says exactly how it
  becomes the PROD-only launcher of `v0_3` behind the new guard, while `src\results_master_v0_2.py` stays in
  DEV unchanged.
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
- **Then the real sequence, each step the owner's own go** (specification 17.3; corrected, EX_299 S3P-C03: v0.1
  left out QA's first fill, without which QA holds no forecast to compare):
  1. `Init_Tree.bat QA`: it copies the software and the accepted results, no forecast, score, report or OV-1
     record, and stops for the environment.
  2. The owner builds QA's `.venv` from a plain CMD window; `Init_Tree.bat QA` again verifies, writes the kit and
     attempts the `INIT` backup.
  3. **QA's first fill:** `Run_Research.bat --game BOTH --no-update` in QA. `--no-update` because QA's results
     come from PROD, which does not exist yet. The fill is retrospective: it starts no prevailing OV-1.
  4. **The transition check,** read-only, against the old records kept in DEV: the 20,436 old forecasts compared
     on their scientific content (the score of every number, the ranking, TOP and WORST), never on whole-record
     digests; the 5,604 old `INSUFFICIENT_HISTORY` records counted apart, each before its variant's first target,
     where the new list rightly has no line; old scores, if compared, reported under their own heading. Any
     unexpected difference stops the transition for review.
  5. `Init_Tree.bat PROD`, its `.venv`, `Init_Tree.bat PROD` again.
  6. PROD's first job.
  QA first is the recommended order for the transition (and the owner's choice, entry 219); it is not a standing
  condition for PROD.

## 6A. Before the one install into DEV: the slices joined and proved together (EX_299 S3P-C04)

A PASS of each slice does not show that the joined software is safe. Before the cumulative package is put to the
owner for DEV, the exact joined files are rehearsed in scratch trees, and the package note answers each of these:

- **A with the installed step 2:** every launcher that writes (research, withdrawal, updater) calls the new guard
  before its first write: tree and settings, markers, the file inventory, status, the environment's digest, the
  job lock and the process rule, and a refusal at every unfinished barrier. The manifest's `[install_tool]` list
  and its classes cover every real import, and no forecast-class file is listed as anything else.
- **B with the job and with C:** `SNAPSHOT_DUE`, the backup at a job's end and the standing warning at its start
  and end are joined to the installed research job. Every attempt of specification 14.1 is covered: a job's
  end, the first tree, before and after an install and a reinstall, before and after `Verify_Tree`, and
  `Run_Snapshot`. Shown: the whole tree with its `.venv` in the ZIP; every member read back; every source file
  read a second time; the quiet checks; a failed `.partial`; no backup named that was not made and verified; the
  due flag kept until a verified backup. The kit is not a backup of the tree.
- **C with A and B:** an install stays add-only with its one question; a helper mismatch refuses; "nothing to
  do" is said as such; no QA pass is a gate. A new variant's smoke case must end in a complete forecast for each
  game, not merely in a call. The fixed forecast sample and the full check of derived results are two checks.
  The suite runs with the target's Python only where the tree's infrastructure is file for file DEV's, and the
  tool says so when it is not run; the package says which tests are the new system's, and the three old known
  failing tests are named as such, neither passed over nor copied to PROD. The digest's inventory and the
  marker's exclusion are those of specification 13; forecast-sample differences after an environment change
  are reported for the W-23 review and are not a failed smoke case.
- **The infrastructure reinstall:** it refuses any forecast-class file added, changed or removed; it never
  overwrites a variant's or a helper's scientific bytes; it shows the full difference in scores and OV-1 before
  its question; cutoffs and stale reports are told truthfully when derived content changes; print-outs are made
  again when only their presentation changes; and it names no rerun command that step 4 has yet to build. A
  half-finished operation stays barred until the same command finishes it, its approved replacement, or the
  owner's own restore.
- **D with A, C and the results step:** the new updater stands behind the same role, path and guard, its lock
  and the `source_data` boundary; it is never started in QA or DEV.
- **Also reviewed then:** the joined manifest and exact file inventory, and one same-command way on for every
  half-finished state of slice C.

## 7. What the owner decided (24 November 2026, 16:03; decision log entry 219), and one question that is open

1. **Slices and installs** (section 4): four reviewed slices and one install into DEV at the end (recommended), or
   an install per slice. **DECIDED: "one at the end."** (The reviewer adds, and Claude agrees: only after section
   6A's joined rehearsal, and on the owner's separate go.)
2. **The probe task first** (section 4): yes (recommended) or no. **DECIDED: yes.** Its run is his own go.
3. **QA before PROD** (specification 17.3 recommends it and does not require it): `Init_Tree QA` and the transition
   check there before PROD exists (recommended), or PROD directly. The early comparison in DEV already found all
   20,436 old forecasts equal, so the check in QA is expected to pass; it is still the one made by an installed tree.
   **DECIDED: yes, QA first.**
4. **Whether this plan goes to the reviewer before slice A is coded** (recommended: yes, for its slice boundaries
   and section 5), or only with slice A. **DECIDED: yes.** Done: EX_299 and EX_300, answered by this v0.1r1.
5. **OPEN, for the owner, after TASK_T028's report:** how Windows' processes are read (section 4A).
   Recommended: the restore stays standard library only; every other check uses psutil; one narrow amendment of
   the deployment design section 2 for ratification. It is needed before slice A's guard is put to the reviewer.

## 8. Known unknowns

- What the standard library can read of another process on this Windows (its program file, parent and start
  time), and what psutil can (also its working folder and command line): the process rule and the restore
  depend on it (section 4A). The probe shows both.
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
