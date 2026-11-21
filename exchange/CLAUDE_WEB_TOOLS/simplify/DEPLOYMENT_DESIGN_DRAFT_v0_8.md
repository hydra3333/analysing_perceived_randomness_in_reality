# Deployment design - DRAFT v0.8 (DEV, QA and PROD; local-file installs; backups; exact restore)

**Status:** DRAFT v0.8 for independent review (v0.7 with the owner's decision of 21 November 2026, 13:18: sections 0, 1,
2 to 8, 11, 12, 14 to 16; `DEPLOY_v0_7_TO_v0_8.diff` is exact). Not ratified. It authorises nothing. It is the companion of the system
specification DRAFT v0.2 and says how that document's sections 2, 4 and 12 to 14 are carried out.
**Written:** 21 November 2026, 13:22 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's
directions in EX_261 and EX_262 and his decisions of 21 November 2026 on installing (decision log entries 124 and 126). Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review. **Risk tier:** HIGH.
**It is a complete document, not a diff** (EX_261 F05; EX_262 section 3): the release rule of the earlier notes ("a named
Git commit proved by a hash list") is gone, so every install step is written afresh. The backup, recovery-kit and
restore rules are the ones the reviewer accepted in the note v0.6 (EX_261 P06), restated here for three roles; v0.6
keeps their reasoning and alternatives. Section 16 lists what is withdrawn and what is carried.

## 0. In plain English

1. One small settings file in each tree says what the tree is and where its backups go. The tools check it every time.
2. Installs copy named files from the DEV folder on this PC. No Git, no network.
3. **The marker is the whole of readiness.** A variant, or the infrastructure, is installable when its marker in DEV
   matches its files. QA is an optional test bed with the same commands; nothing links it to PROD. Each install
   checks itself in the tree it installs into.
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

**How the settings files come to exist, and why nothing overwrites them** (the owner's question of 21 November 2026).
- **DEV's file is made once, by the owner:** he copies the tracked `ENVIRONMENT.example.ini` to `ENVIRONMENT.ini` and types
  his paths. Git ignores the real file, so no checkout or pull can replace it. `Check_Tree.bat` prints how the tools
  read it and what each check finds, and changes nothing.
- **A QA or PROD tree's file is written exactly once, by `Init_Tree.bat`,** from DEV's entry for that role. It is opened
  create-only: if a file of that name already exists the write fails and the tool refuses.
- **After that no program writes it.** It is not on the infrastructure manifest, so `Reinstall_Infra.bat` cannot touch
  it; it is not part of any variant; every launcher and tool opens it for reading only. A test searches the code for
  any other write and plants an attempt. The one exception is a restore, which writes the backup's own copy into a
  fresh, empty tree (section 12).
- **To change a setting later** (a new backup drive, say) the owner edits the tree's own file by hand, and DEV's entry
  to match. The checks below run at the next command; if the two disagree it refuses and prints both values.
- Every backup holds its tree's file, so a restore brings the settings back with everything else.

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

## 3. What can be installed, and what an install checks (the owner's decision of 21 November 2026, 13:18)

**3.1 What can be installed, and only this.**
- *Variants:* the folders of ready variants (specification section 4), without their markers, and the helper files
  their declarations name.
- *Infrastructure:* the files listed in DEV's `deploy\INFRA_MANIFEST.txt`, one path a line, when
  `deploy\INFRA_IS_INSTALLABLE.json` matches them. `Make_Installable.bat INFRA` writes that marker: every manifest file
  and every file of the install tool, with SHA-256.
- Nothing else in DEV is ever read for copying. A file under `src\` in a target that is neither is a refusal.

**3.2 The markers are the whole of readiness (owner).** DRAFT v0.7 had a QA pass record and five comparisons of PROD
with QA before every PROD installation. The owner has withdrawn that: PROD is installed on the DEV markers alone.
There is no pass record, and no tool reads one tree in order to decide about another. QA and PROD are each installed
from DEV, in any order, or QA not at all.

**3.3 What every install checks in its own target,** and stops on:
1. the markers match DEV's files now (so a file edited after marking is named and refused);
2. add-only: no installed variant or helper would change; no unexpected file under `src\`;
3. after copying, every installed file equals the plan;
4. the whole suite, with the target's Python, on a temporary copy;
5. the regression of what was already installed: a fixed sample after variants, everything after infrastructure.

## 4. Creating a tree: `Init_Tree.bat QA|PROD`

| Step | What happens |
|---|---|
| 1 | Settings checked (section 1). The target root does not exist, or is empty, or holds this same unfinished creation |
| 2 | The plan: the infrastructure manifest's files (its marker must match) and every ready variant with its helpers, all hashed. It is shown; for PROD the owner types the confirmation |
| 3 | The process check (section 9). The folder is created; `ENVIRONMENT.ini` (create-only) and the barrier `records\INSTALL_IN_PROGRESS.json`, holding the plan, are written |
| 4 | Every planned file is copied from DEV: to a temporary name, hashed, renamed into place |
| 5 | The accepted results are copied (QA: from PROD, or from DEV while no PROD exists; PROD: from DEV), each file hashed on both sides; the list is kept as `INIT_RECORD.json`. No result, score, report or record is copied |
| 6 | **It stops and asks the owner to build `.venv`** with `create_venv.bat` and `install_upgrade_dependencies_into_venv.bat` in the new tree. The same command typed again goes on |
| 7 | The whole tree's software is checked against the plan. The suite is run with the new tree's Python on a temporary copy (the planned software and DEV's tests), which is then removed. On success `ENVIRONMENT_VERIFIED.json` is written |
| 8 | `INSTALLED_FILES.json`; the log line; the recovery kit, written and checked (PROD: a failure here stops); the barrier removed, last |
| 9 | The `INIT` backup. The owner then runs the research job |

## 5. Adding variants: `Install.bat PROD` (or `QA`)

| Step | What happens |
|---|---|
| 1 | Settings and role checked. The plan: ready variants the target lacks (narrowed by `--only`), their folders, and helper files the target lacks. A helper the target holds with other bytes refuses. Shown: to add; left out, each with its reason (not marked; marker does not match its files; already installed; already installed with different bytes). Nothing to add: end, target untouched |
| 2 | **PROD: one typed confirmation** of the batch shown |
| 3 | The process check; no job lock, updater lock, orphan marker or other unfinished install |
| 4 | The recovery kit for the new software state (PROD: a failure stops; QA: a failure warns) |
| 5 | The `PRE_INSTALL` backup, always attempted; if it cannot be made: NO ROLLBACK POINT WAS CREATED, and it goes on |
| 6 | The barrier, holding the plan; the updater's own lock is taken; `SNAPSHOT_DUE` |
| 7 | Each new file: temporary name, hash, rename. No existing file is opened for writing |
| 8 | The whole tree's software against the old list plus the plan; nothing unexpected under `src\` |
| 9 | The suite with the target's Python on a temporary copy; the sample regression |
| 10 | `INSTALLED_FILES.json`; the log line; the updater's lock released; the barrier removed, last |
| 11 | The `POST_INSTALL` backup. Installation is release: the owner's next `Run_Research.bat` fills the new variants' history |

## 6. Updating infrastructure: `Reinstall_Infra.bat PROD` (or `QA`)

The same eleven steps with these differences.
- **Step 1:** the infrastructure marker must match. The plan is the difference between DEV's manifest files and the
  target's infrastructure: files to add, to overwrite and to remove, each with both hashes; the text differences are
  shown. No path under a family folder or `_shared\` can be in it. No difference: end.
- **Step 7:** overwritten files are replaced by rename; removals come after all copies.
- **Step 9:** the **full** regression: every forecast and every score of every installed variant is recomputed from the
  permitted views and must equal the canonical files in content. One difference stops the install with the barrier
  in place: it is reported as a scientific change, and the way back is the `PRE_INFRA` backup.
- Backups are named `PRE_INFRA` and `POST_INFRA`.

## 7. Verifying a tree: `Verify_Tree.bat` (run in the tree, after its environment is rebuilt)

Process check; a backup; the suite with the tree's Python on a temporary copy of the installed software and DEV's
tests; the sample regression, whose differences after an environment change are **reported** for the W-23 review and
do not by themselves refuse; `ENVIRONMENT_VERIFIED.json`; a backup. A failed suite writes no marker and removes an
older one. The owner's install script removes the marker before it changes anything.

## 8. When an operation stops half-way

| State found | Meaning | What the same command does | The other way out |
|---|---|---|---|
| The barrier exists and its plan equals the plan now | this operation was interrupted, or a check failed and the cause is now corrected | continues: files already in place with the right hash are skipped; the checks run again | restore the backup taken at step 5 |
| The barrier exists with another plan | a different operation is unfinished, or DEV changed meanwhile | refuses and shows both plans | finish that one, or restore |
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
`KIT_MANIFEST.json`. It is built from DEV's install tool files, as the infrastructure marker lists them. The tool checks its own files against
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
   job, which catches up with what the backup held. Anything further is a new decision by the owner.

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

## 14. Worked examples (invented names; EX_262 section 4, adjusted to the owner's decision)

1. **Two ready, one unfinished.** DEV holds `E_002\RECUR_MEAN_ALL_V2` and `E_017\HAZARD_BINS_C100_V2`, both marked, and
   `E_002\RECUR_MEDIAN_ALL_V3` with no marker. `Install.bat QA` (the owner chooses to look first) shows "to add: 2
   variants, 1 helper (`_shared\recurrence_gaps_v2.py`); left out: `RECUR_MEDIAN_ALL_V3` (not marked)". It installs and
   checks. The owner runs QA's research job and reads its league reports.
2. **One changes afterwards.** The owner edits `HAZARD_BINS_C100_V2\method.py` in DEV. `Install.bat PROD` shows "to add:
   `RECUR_MEAN_ALL_V2`; left out: `HAZARD_BINS_C100_V2` (marker does not match its files)". When he has finished and
   marked it again, the next `Install.bat PROD` adds it. QA still holds the earlier bytes under that name:
   `Check_Tree.bat QA` says so, and `Install.bat QA` leaves it alone ("already installed with different bytes"). QA is
   a test bed: it can be restored to an earlier backup or created again; PROD is not affected either way.
3. **Infrastructure.** `src\evaluation\reports.py` is improved and `Make_Installable.bat INFRA` run.
   `Reinstall_Infra.bat PROD` shows one file to overwrite and no variant; one confirmation; `PRE_INFRA`; the file
   replaced; the suite; the full regression finds no difference; `POST_INFRA`. Had the change altered one old
   forecast, the install would have stopped there with no job able to run, and `PRE_INFRA` would be restored. Trying
   it in QA first would have shown the same without touching PROD.
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
a fault planted after every step, then the command again; the three states of section 8; the two kinds of marker (matching; one file
edited afterwards; made by hand with a wrong hash); a settings file never written after its creation; add-only (a changed, a removed and an added
helper); the manifest (a listed file missing; an imported module not listed); unexpected files under `src\`; the
guard in each role; the updater launcher refusing outside PROD; backups (a member changed in the archive; a file
changed, added or removed during the backup; not quiet; a link; a full disk; the due flag across jobs of different
kinds); the kit's self-check; restore (from a kit by a bare Python with DEV and QA out of reach; the exact allowed
set; old tree absent or damaged; a Python process present; stopped half-way; READY and NOT READY; the orphan
condition; the hand unzip and its reconciliation; **nothing installed afterwards**); the cold copy's dry run and its
refusal to leave DEV's root.

**The rehearsal on the owner's PC** (one task file, its own go, scratch folders, invented data only): three scratch
roots set in a scratch settings file; `Init_Tree` for a scratch QA and a scratch PROD; an `Install` into each; a
`Reinstall_Infra`; an install with a fault planted and the command typed again; jobs ending in backups; one backup
of a tree of the real size opened in **File Explorer by the owner**; one restore from the kit with a stale orphan
marker and a restart; the Windows process table and start time read by the standard library. No step changes the
PC's date, time or zone; nothing is terminated; no real data is read; no lottery site is contacted.

## 16. Withdrawn from the earlier notes, and carried

**Withdrawn:** a release as a named Git commit, its hash list and `deploy\RELEASE.json`, and bytes read from Git
objects; the install record, the release record and the barrier under `src\`; the `export` mode and
`export --after-restore` (specification choice E); `PRODUCTION_ROOT.json` and the settings JSON (replaced by
`ENVIRONMENT.ini`); the modes `check`, `init`, `update` under those names; the weekly and development sequencers; the
note v0.6's reading table (its section 0A); the QA pass record and the five checks of DRAFT v0.7 (the owner's decision of 13:18); every OV-1 restore rule; "later releases first" after a restore, in every
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
  needs, so that the temporary copy is complete; that list sits beside the infrastructure manifest. Tests that served
  only the old system are not part of the new suite.
- The run sheets (creation of QA and PROD; an environment change; a withdrawal; a restore) are written and reviewed
  with the code packages.

End of the deployment design, DRAFT v0.8.
