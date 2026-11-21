# Deployment design - DRAFT v0.7 (DEV, QA and PROD; local-file installs; backups; exact restore)

**Status:** DRAFT v0.7 for independent review. Not ratified. It authorises nothing. It is the companion of the system
specification DRAFT v0.1 and says how that document's sections 2, 4 and 12 to 14 are carried out.
**Written:** 21 November 2026, 13:07 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's
directions in EX_261 and EX_262 and his decision of 21 November 2026 on QA (decision log entry 124). Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review. **Risk tier:** HIGH.
**It is a complete document, not a diff** (EX_261 F05; EX_262 section 3): the release rule of the earlier notes ("a named
Git commit proved by a hash list") is gone, so every install step is written afresh. The backup, recovery-kit and
restore rules are the ones the reviewer accepted in the note v0.6 (EX_261 P06), restated here for three roles; v0.6
keeps their reasoning and alternatives. Section 16 lists what is withdrawn and what is carried.

## 0. In plain English

1. One small settings file in each tree says what the tree is and where its backups go. The tools check it every time.
2. Installs copy named files from the DEV folder on this PC. No Git, no network.
3. **QA proves, PROD copies the proof.** A QA operation ends by testing QA as a whole and writing a pass that lists
   every installed file with its hash. A PROD operation compares itself with that pass, file by file, before it
   touches anything, and no option skips the comparison.
4. An install that stops half-way leaves a barrier that keeps every job out until the same command finishes it or
   the backup taken just before is restored.
5. Backups, the recovery kit and the exact restore are as already reviewed, now for QA as well as PROD.

## 1. Settings: `ENVIRONMENT.ini` (EX_262 F09)

**DEV's file** (not tracked by Git, since it holds this PC's paths; a tracked example sits beside it):

    [environment]
    role = DEV
    tree_root = E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
    venv_dir = E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
    [QA]
    tree_root = D:\TEST_BED
    backup_root = D:\TEST_BED_backups
    venv_dir = D:\TEST_BED\.venv
    [PROD]
    tree_root = G:\a_p_r_i_r
    backup_root = T:\a_p_r_i_r_backups
    venv_dir = G:\a_p_r_i_r\.venv
    [results]
    copy_from = G:\a_p_r_i_r
    [cold_backup]
    root = T:\a_p_r_i_r_cold

**A QA or PROD tree's own file,** written by `Init_Tree.bat` from DEV's entry and never edited by a tool afterwards:

    [environment]
    role = QA
    tree_root = D:\TEST_BED
    backup_root = D:\TEST_BED_backups
    venv_dir = D:\TEST_BED\.venv
    [results]
    copy_from = G:\a_p_r_i_r

(PROD's file has no `[results]` section: its results come from the updater.) Every path above is an example.

**Checks, made by every tool and launcher that reads a settings file; any failure refuses:**
1. Every path is absolute and is its own real path: no junction, link or substituted drive in any part of it.
2. The tree roots of DEV, QA and PROD are three different folders, none inside another. No backup root lies inside
   any tree root, and no tree root inside a backup root. QA's and PROD's backup roots differ.
3. `venv_dir` lies inside its own tree root, so that every backup holds the environment.
4. **A tree is what its own file says.** For an operation on role R: DEV's entry for R names a folder; that folder's
   own file must say `role = R` and name that same folder as `tree_root`. A launcher run inside a tree requires the
   file's `tree_root` to be the folder the launcher is in.
5. A backup root on the same disk volume as its tree is allowed with a printed warning (the owner's choice for QA).

## 2. What a QA or PROD tree holds

    <tree_root>\
        ENVIRONMENT.ini
        Run_Research.bat  Run_Results_Updater.bat  Run_Snapshot.bat  Verify_Tree.bat  Withdraw_Variant.bat
        create_venv.bat  install_upgrade_dependencies_into_venv.bat  activate_venv.bat  deactivate_venv.bat
        src\                       exactly the files of the infrastructure manifest, and the installed variants and helpers
        source_data\               the accepted results, their version ledgers and verification records
        results\research\          the canonical files, the OV-1 ledger and the reports (specification sections 5, 9, 10)
        records\
            INSTALLED_FILES.json   every installed software file with its SHA-256, and each variant's fingerprint
            INSTALL_LOG.jsonl      one line per finished install, reinstall, creation or verification
            QA_PASS_<number>.json  QA only (section 3)
            SNAPSHOT_LOG.jsonl  INIT_RECORD.json  RESTORE_<date>_<time>.json
            INSTALL_IN_PROGRESS.json  JOB.lock  SNAPSHOT_DUE  SNAPSHOT_IN_PROGRESS.lock      control files
        .venv\                     built by the owner; holds ENVIRONMENT_VERIFIED.json

    <backup_root>\
        <ROLE>_<YYYYMMDD>_<HHMMSS>_<JOB>.zip  and  .sha256        backups (section 10)
        KIT_<YYYYMMDD>_<HHMMSS>_<software fingerprint>.zip  and  .sha256      recovery kits (section 11)

There is no Git folder, test, document or exchange file in a QA or PROD tree, and nothing born in the tree lies under
`src\`. `Run_Results_Updater.bat` runs in PROD only; in QA its guard refuses.

**The install tools live in DEV** (`deploy\`, standard library only) and are run from DEV: `Make_Installable.bat`,
`Install.bat`, `Reinstall_Infra.bat`, `Init_Tree.bat`, `Check_Tree.bat`, `Cold_Copy.bat`.

## 3. The candidate, the QA pass and the five checks (the owner's decision of 21 November 2026)

**3.1 What can be installed, and only this.**
- *Variants:* the folders of ready variants (specification section 4), without their markers, and the helper files
  their declarations name.
- *Infrastructure:* the files listed in DEV's `deploy\INFRA_MANIFEST.txt`, one path a line.
- Nothing else in DEV is ever read for copying. A file under `src\` in a target that is neither is a refusal.

**3.2 The QA pass record,** `records\QA_PASS_<number>.json` in the QA tree, written only at the end of a QA operation
whose tests all succeeded:
- `software`: QA's complete installed list (every infrastructure, variant and helper file, with SHA-256);
- `infrastructure`: the manifest's paths as tested;
- `test_material` and `tool_material`: every file of DEV's tests and of the install tool that was used, with SHA-256;
- the evidence: the suite's counts and output digest; the regression (sample or full; pairs compared; differences,
  which must be none for a pass after a software change); the research job's summary for each game, with the
  `NO_FORECAST` counts of each new variant; QA's environment digest; the operation; the time.

**3.3 The five checks of every PROD operation** (`Install.bat PROD`, `Reinstall_Infra.bat PROD`, `Init_Tree.bat PROD`).
Let PASS be QA's highest-numbered pass, and AFTER the complete installed list PROD would have when the operation ends.
1. QA's `INSTALLED_FILES.json` and QA's files, hashed now, equal PASS's `software`.
2. For every file the operation would write: SHA-256 of DEV's file equals PASS's entry for that path.
3. The infrastructure paths of AFTER are exactly PASS's `infrastructure`, with PASS's hashes.
4. Every other path of AFTER (variants, helpers) is in PASS's `software` with the same hash.
5. DEV's tests and install tool, and the files of the tool now running, equal PASS's `test_material` and
   `tool_material`.
Any difference refuses before anything is touched and names the first file. **There is no flag, setting, prompt or
environment variable that skips a check,** and a test asserts that no command line makes a PROD operation proceed
without a pass. What the refusals lead to: check 1, `Verify_Tree.bat QA`; checks 2 and 5, the QA operation again;
check 3 on a variant install, `Reinstall_Infra.bat PROD` first; check 4, DEV has drifted from what PROD holds, or QA
lacks something PROD has: bring QA up to date and verify it.

## 4. Creating a tree: `Init_Tree.bat QA|PROD`

| Step | What happens |
|---|---|
| 1 | Settings checked (section 1). The target root does not exist, or is empty, or holds this same unfinished creation |
| 2 | The plan: the infrastructure manifest's files and every ready variant with its helpers, all hashed. **PROD:** the five checks; the batch and the pass are shown; the owner types the confirmation |
| 3 | The process check (section 9). The folder is created; `ENVIRONMENT.ini` and the barrier `records\INSTALL_IN_PROGRESS.json` (holding the plan) are written |
| 4 | Every planned file is copied from DEV: to a temporary name, hashed, renamed into place |
| 5 | The accepted results are copied (QA: from PROD, or from DEV while no PROD exists; PROD: from DEV), each file hashed on both sides; the list is kept as `INIT_RECORD.json`. No result, score, report or record is copied |
| 6 | **It stops and asks the owner to build `.venv`** with `create_venv.bat` and `install_upgrade_dependencies_into_venv.bat` in the new tree. The same command typed again goes on |
| 7 | The whole tree's software is checked against the plan. The suite is run with the new tree's Python on a temporary copy (the planned software and DEV's tests), which is then removed. On success `ENVIRONMENT_VERIFIED.json` is written |
| 8 | `INSTALLED_FILES.json`; the log line; the recovery kit, written and checked (PROD: a failure here stops); the barrier removed, last |
| 9 | **QA:** the research job to its end, then `QA_PASS_1.json`, then a backup. **PROD:** the `INIT` backup; the owner then runs the research job |

## 5. Adding variants: `Install.bat QA|PROD`

| Step | QA | PROD |
|---|---|---|
| 1 | Settings and role checked. The plan: ready variants the target lacks (narrowed by `--only`), their folders, and helper files the target lacks. A helper the target holds with other bytes refuses. Shown: to add; left out, each with its reason (not marked; marker does not match; already installed; already installed with different bytes). Nothing to add: end, target untouched | the same |
| 2 | | The five checks. The batch and the pass (its number, time and evidence) are shown; **one typed confirmation** |
| 3 | The process check; no job lock, updater lock, orphan marker or other unfinished install | the same |
| 4 | The recovery kit for the new software state (a failure warns) | the same (**a failure stops**) |
| 5 | The `PRE_INSTALL` backup, always attempted; if it cannot be made: NO ROLLBACK POINT WAS CREATED, and it goes on | the same |
| 6 | The barrier, holding the plan; the updater's own lock is taken; `SNAPSHOT_DUE` | the same |
| 7 | Each new file: temporary name, hash, rename. No existing file is opened for writing | the same |
| 8 | The whole tree's software against the old list plus the plan; nothing unexpected under `src\` | the same |
| 9 | The suite with QA's Python on a temporary copy | the suite with PROD's Python on a temporary copy; the sample regression, reported |
| 10 | `INSTALLED_FILES.json`; the log line; the updater's lock released; the barrier removed | the same |
| 11 | The sample regression; the research job to its end; **the new QA pass** | |
| 12 | The `POST_INSTALL` backup | the same. Installation is release: the owner's next `Run_Research.bat` fills the new variants' history |

## 6. Updating infrastructure: `Reinstall_Infra.bat QA|PROD`

The same twelve steps with these differences.
- **Step 1:** the plan is the difference between DEV's manifest files and the target's infrastructure: files to add, to
  overwrite and to remove, each with both hashes; the text differences are shown. No path under a family folder or
  `_shared\` can be in it. No difference: end. **QA:** it refuses if QA's environment digest is not that of QA's last
  pass (one kind of change at a time: `Verify_Tree.bat QA` first).
- **Step 7:** overwritten files are replaced by rename; removals come after all copies.
- **Step 11, QA:** the **full** regression: every forecast and every score of every installed variant is recomputed from
  the permitted views and must equal the canonical files in content. One difference: no pass, the reinstall is
  reported as a scientific change, and the way back is the `PRE_INFRA` backup. Then the research job; then the pass.
- Backups are named `PRE_INFRA` and `POST_INFRA`.

## 7. Verifying a tree: `Verify_Tree.bat` (run in the tree)

- **QA:** process check; backup; the suite with QA's Python; the full regression; the research job; a new pass;
  `ENVIRONMENT_VERIFIED.json`; backup. After an environment change the regression's differences are recorded in the
  pass as environment differences for the W-23 review and do not withhold it; after no change there must be none.
- **PROD:** process check; backup; the suite with PROD's Python on a temporary copy of the installed software and DEV's
  tests (which must be the pass's: check 5); the sample regression, reported; `ENVIRONMENT_VERIFIED.json`; backup.
- A failed verification writes no marker and removes an older one. The owner's install script removes the marker
  before it changes anything.

## 8. When an operation stops half-way

| State found | Meaning | What the same command does | The other way out |
|---|---|---|---|
| The barrier exists and its plan equals the plan now | this operation was interrupted | continues: files already in place with the right hash are skipped | restore the backup taken at step 5 |
| The barrier exists with another plan | a different operation is unfinished, or DEV changed meanwhile | refuses and shows both plans | finish that one, or restore |
| No barrier; QA's software has no pass | QA's tests did not finish or failed | `Verify_Tree.bat QA` | return QA to its `PRE_` backup, correct DEV, install again |
| `INSTALLED_FILES.json` and the tree differ, no barrier | something changed a file outside the tools | every launcher and tool refuses, naming the file | restore |

While the barrier exists every launcher in that tree refuses. A file not on `INSTALLED_FILES.json` is never run: a
variant folder that is present but not listed is an unexpected file, which refuses the job.

## 9. The guard and the process rules (kept; no program ever ends a process)

**At every launch,** inside the Python pre-check each launcher already makes: the settings file is present and names
this folder and a role this launcher may run in; no `INSTALL_IN_PROGRESS.json`, `RESTORE_IN_PROGRESS.json` or
`SNAPSHOT_IN_PROGRESS.lock`; in QA and PROD, `ENVIRONMENT_VERIFIED.json` is present and lists the installed
distributions (a cheap first gate only).
**At the start of a research job, in QA and PROD:** the environment's full digest equals the marker's; every installed
software file equals `INSTALLED_FILES.json` and nothing else lies under `src\`; no orphan marker
(`transitory_data\poc_runs\UNRESOLVED_ORPHAN.json`; nothing installed outside DEV writes one, and the check stays); the
job lock is taken; no other Python process of this tree is running.

| Operation | Process rule |
|---|---|
| Research job; a backup (before and after) | no other Python process **of this tree**: its executable is the tree's own, or its working folder is under the tree, or its command line or an ancestor's names the tree. Unrelated Python work on the PC does not count |
| `Init_Tree`, `Install`, `Reinstall_Infra`, `Verify_Tree` | the existing rule of design 6.1, unchanged, applied to the target tree, the tool's own chain excepted. As today, another Python job from the same Python installation (a Claude Code task, say) is listed and must be finished first |
| Restore | **no Python program at all on the PC** but the restore tool, read from Windows' process table with the standard library; checked before the old tree is renamed and again after; a table that cannot be read refuses |

The tools of the process and records kind that write refuse while a backup is in progress; the read-only quiet check
does not.

## 10. Backups (as reviewed in the note v0.6 section 7, for any role)

- **Everything under the tree root,** `.venv` included; only `SNAPSHOT_DUE` and `SNAPSHOT_IN_PROGRESS.lock` are left out.
  No other exclusion of any kind.
- **How:** Python's `zipfile`, Deflate level 9, to `<name>.zip.partial` in the tree's own backup root; each file's
  SHA-256 goes into `SNAPSHOT_MANIFEST.json`, the last member, with the time, the role, the tree root, the software
  fingerprint and the name of the matching recovery kit. ZIP64 is written automatically when needed.
- **What a ZIP keeps:** every byte, name, folder and empty folder, and times to two seconds. **Not:** permissions,
  alternate streams, or hard links as links. A link to another place makes the backup fail.
- **Quiet, by three things together:** the lock makes every launcher refuse; the process rule of section 9 before the
  first reading and after the second; and the second reading itself.
- **Verified means both:** the archive read back, every member against the list; and every source file read and
  hashed again, the set of files unchanged. Only then is it renamed to `<name>.zip`, its `.sha256` written, a line
  added to `SNAPSHOT_LOG.jsonl` and `SNAPSHOT_DUE` removed. A `.partial` is never a backup.
- **Names:** `<ROLE>_<YYYYMMDD>_<HHMMSS>_<JOB>.zip`; `<JOB>` is `RESEARCH`, `MANUAL`, `INIT`, `PRE_INSTALL`, `POST_INSTALL`,
  `PRE_INFRA`, `POST_INFRA`, `PRE_VERIFY` or `POST_VERIFY`. Every one is complete.
- **`SNAPSHOT_DUE`** is written before a job's first write and removed only by a verified backup. A job that finds it
  tries that backup first. **If a backup cannot be made the job goes on,** with a warning in capitals at its start
  and end, repeated by every job until a verified backup exists (owner).
- `Run_Snapshot.bat` asks for a backup at any time; it is made only if the tree is quiet.
- Nothing prunes a backup root. The owner copies PROD's backup root to other media himself.

## 11. The recovery kit (as reviewed in the note v0.6 section 4.7)

A small ZIP with its `.sha256` in the backup root, written at every creation, install and reinstall, for the software
state that results. It holds the restore tool (standard library only), `Restore.bat`, `HOW_TO_RESTORE.txt` and
`KIT_MANIFEST.json`. It is built from the tool files that passed in QA (check 5). The tool checks its own files against
the manifest before doing anything. A digest is a check against damage, not a signature. Each backup's manifest names
its kit. A restore needs the kit, the backup and any installed Python: not DEV, not QA, not a working tree.

## 12. Restore (as reviewed in the note v0.6 section 8; EX_258; EX_259 section 7)

`Restore.bat --snapshot <zip>`, from an unpacked kit, on the owner's own go. The destination is the tree root named
inside the backup; no other place is accepted.

**It requires:** the kit's self-check; the backup verified in full before anything is touched; no Python program on
the PC (section 9); and, only if an orphan marker is found, the condition below.

**Its steps:**
1. The old tree is looked at, for the record only (locks, a barrier, an orphan marker); whatever cannot be read is
   noted as such.
2. The old folder is renamed to `<tree_root>_SET_ASIDE_<date>_<time>`: one rename, nothing copied or deleted. Its
   settings file is renamed too, so no launcher runs there. The second process check.
3. A fresh empty folder; `RESTORE_IN_PROGRESS.json` first; then every member of the **payload** (every member except
   the manifest) is unpacked and hashed, except the settings file and an orphan marker if the backup holds one.
4. The fresh tree is read again and must be exactly the payload, less those two, plus the progress file.
5. Added, by name, and nothing else: the restore record `records\RESTORE_<date>_<time>.json`; and the orphan marker's
   bytes as `records\RESTORE_<date>_<time>_ORPHAN_MARKER.json`, if there was one.
6. The settings file is written last, from the backup's own bytes; the progress file is removed. The tree is now
   exactly: the payload, plus the restore record, plus the orphan evidence if any, less a live orphan marker.
7. The restored environment's Python is started once and imports the project's third-party modules. **RESTORED AND
   READY TO RUN,** or **RESTORED; ENVIRONMENT NOT READY.** It never says "ready" otherwise.
8. **Nothing else is done.** No release, variant or infrastructure file is installed; no withdrawal is applied; the
   environment is not rebuilt; nothing is read from DEV, QA or the set-aside tree. The owner then runs the research
   job, which catches up with what the backup held. Anything further is a new decision, through QA.

Stopped half-way: the same command again; an unfinished fresh tree is itself renamed aside first.

**By hand, as the last resort** (owner): close everything that uses Python; rename the old folder; make an empty
folder at the same path; extract the backup into it. Nothing was checked. The manifest now lies at the tree's root
and no new backup is made while it is there. If the backup held an orphan marker it is live and blocks every launch
as always. `Restore.bat --after-hand-unzip --snapshot <zip>` then checks every file, writes the restore record with
the time labelled "reconciliation recorded at", and moves the manifest beside it.

**A stale orphan marker: one exception, proposed for ratification** (Architecture 5C is amended by ratification, not
edited; unchanged from the notes v0.2 to v0.6):

> At a restore, a stale orphan marker is set aside as evidence instead of being cleared in place, when all of these
> hold: (a) the tool has shown the marker and a prominent warning that recommends restarting the PC; (b) the PC was
> started after the marker was written; (c) a fresh process check, made after that, is CLEAN; (d) the owner types the
> fixed acknowledgement sentence. No part can be waived, and (d) never stands in for (b) or (c).

Without a restart since the marker, the restore refuses and names the two ways forward: restart the PC, or the
existing reviewed clearance. Outside a restore the rule stands as it is.

## 13. The cold copy of the old project clone (EX_261 F04; its own go)

`Cold_Copy.bat --dry-run`, then `Cold_Copy.bat --make`, in DEV. It reads DEV's own root from DEV's settings file, and
the destination from `[cold_backup]`. **It never looks outside that one folder.** The dry run prints the file count and
size of each top-level folder and what would be left out (by default only `.venv`; `--with-venv` includes it), and
writes nothing. `--make` uses the backup core of section 10: one ZIP64 archive `COLD_<date>_<time>.zip`, a manifest of
hashes, the archive read back and the source read again, a `.sha256`. Nothing of it ever goes to QA or PROD. It is
delivered and reviewed as a small script before phase 1.

## 14. Worked examples (invented names; EX_262 section 4)

1. **Two ready, one unfinished.** DEV holds `E_002\RECUR_MEAN_ALL_V2` and `E_017\HAZARD_BINS_C100_V2`, both marked, and
   `E_002\RECUR_MEDIAN_ALL_V3` with no marker. `Install.bat QA` shows "to add: 2 variants, 1 helper
   (`_shared\recurrence_gaps_v2.py`); left out: `RECUR_MEDIAN_ALL_V3` (not marked)". It installs, tests, runs QA's job,
   writes `QA_PASS_7.json` and a backup.
2. **One changes after QA.** The owner edits `HAZARD_BINS_C100_V2\method.py` in DEV. `Install.bat PROD` shows "to add:
   `RECUR_MEAN_ALL_V2`; left out: `HAZARD_BINS_C100_V2` (marker does not match its files)". If he makes the marker
   again, it is ready, and PROD refuses the batch at check 2: "not the QA-tested bytes:
   `E_017\HAZARD_BINS_C100_V2\method.py`". `Install.bat QA` reports it "already installed with different bytes". Ways
   forward: give the changed work a new variant name; or restore QA to its `PRE_INSTALL` backup and install again.
3. **Infrastructure.** `src\evaluation\reports.py` is improved. `Reinstall_Infra.bat QA` shows one file to overwrite and
   no variant; the full regression finds no difference; `QA_PASS_8.json`. `Reinstall_Infra.bat PROD`: the five checks,
   one confirmation, `PRE_INFRA`, the file replaced, the suite, `POST_INFRA`. Had the change altered one old
   forecast, QA would have written no pass and PROD could not have been touched.
4. **A wrong setting.** DEV's `[QA]` entry is mistyped as `G:\a_p_r_i_r`. `Install.bat QA` refuses at once: QA's and
   PROD's roots are the same folder. Had only the folder been reused, its own file says `role = PROD`: refused.
5. **Separate backups.** QA's job ends with `D:\TEST_BED_backups\QA_20270105_101500_RESEARCH.zip` (with the same-volume
   warning); PROD's with `T:\a_p_r_i_r_backups\PROD_20270105_193000_RESEARCH.zip`.
6. **A restore installs nothing.** PROD is restored to a backup made before `RECUR_MEAN_ALL_V2` was installed. The tree
   holds forty variants; the job catches up with forty. `Check_Tree.bat PROD` lists the variant as "ready in DEV, not
   installed", as information. If the owner later runs `Install.bat PROD`, it is a new installation: new files, and
   a new `FORWARD_FROM`.

## 15. Tests and the rehearsal

**Tests** (invented trees in temporary folders): each check of section 1 with one wrong setting; each step table with
a fault planted after every step, then the command again; the four states of section 8; each of the five checks
with one planted difference, and no command line that avoids them; add-only (a changed, a removed and an added
helper); the manifest (a listed file missing; an imported module not listed); unexpected files under `src\`; the
guard in each role; the updater launcher refusing outside PROD; backups (a member changed in the archive; a file
changed, added or removed during the backup; not quiet; a link; a full disk; the due flag across jobs of different
kinds); the kit's self-check; restore (from a kit by a bare Python with DEV and QA out of reach; the exact allowed
set; old tree absent or damaged; a Python process present; stopped half-way; READY and NOT READY; the orphan
condition; the hand unzip and its reconciliation; **nothing installed afterwards**); the cold copy's dry run and its
refusal to leave DEV's root.

**The rehearsal on the owner's PC** (one task file, its own go, scratch folders, invented data only): three scratch
roots set in a scratch settings file; `Init_Tree` for a scratch QA and a scratch PROD; an `Install` through both; a
`Reinstall_Infra`; an install with a fault planted and the command typed again; jobs ending in backups; one backup
of a tree of the real size opened in **File Explorer by the owner**; one restore from the kit with a stale orphan
marker and a restart; the Windows process table and start time read by the standard library. No step changes the
PC's date, time or zone; nothing is terminated; no real data is read; no lottery site is contacted.

## 16. Withdrawn from the earlier notes, and carried

**Withdrawn:** a release as a named Git commit, its hash list and `deploy\RELEASE.json`, and bytes read from Git
objects; the install record, the release record and the barrier under `src\`; the `export` mode and
`export --after-restore` (specification choice E); `PRODUCTION_ROOT.json` and the settings JSON (replaced by
`ENVIRONMENT.ini`); the modes `check`, `init`, `update` under those names; the weekly and development sequencers; the
note v0.6's reading table (its section 0A); every OV-1 restore rule; "later releases first" after a restore, in every
form (the remaining cell of v0.6 section 18 that said so is superseded: EX_261 F05).
**Carried, as reviewed:** complete-tree ZIP backups, their two verifications and the quiet rule; the due flag and
"jobs go on"; `PRE_` and `POST_` backups; the recovery kit; the exact restore with its payload check, its process
rule, the hand unzip and the orphan-marker exception; the environment built by the owner and verified before use;
W-23; the guard inside each launcher's own pre-check; no program ends a process.

## 17. Not designed here, and uncertainties

- Nothing here has run. Unmeasured: a backup of a whole tree with its environment; the full regression in QA; File
  Explorer on an archive of that size (the fallback of several smaller ZIPs under one manifest is not designed
  unless needed).
- Reading Windows' process table and start time with the standard library is to be shown in the rehearsal.
- A restored environment may not start if the PC's base Python has changed since the backup; the restore says so.
- The design 6.1 process rule lists unrelated Python work from the same installation during an install; with three
  environments sharing one Python this will be met. I recommend living with it.
- DEV's settings file holds the paths of all three trees. If it is lost it is typed again from the example; each
  tree's own file is what actually protects a tree.
- Some existing tests read repository files outside `src\` and `tests\`. The code round lists exactly what the suite
  needs, so that the temporary copy is complete; that list is part of the pass's `test_material`. Tests that served
  only the old system are not part of the new suite.
- The run sheets (creation of QA and PROD; an environment change; a withdrawal; a restore) are written and reviewed
  with the code packages.

End of the deployment design, DRAFT v0.7.
