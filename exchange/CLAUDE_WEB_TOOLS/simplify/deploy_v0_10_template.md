# Deployment design - DRAFT v0.10 (DEV, QA and PROD; local-file installs; the copies from PROD; backups; exact restore)

**Status:** DRAFT v0.10 for independent review (EX_266). It replaces DRAFT v0.9 and answers EX_264 (R5-F02 to R5-F05, N03),
EX_265 and the project owner's decisions in decision log entries 128 to 137. Sections 11 and 12 are byte-identical to
v0.9; sections 1, 10 and 14 are v0.9's with the counted changes the diff shows; the rest is rewritten.
`DEPLOY_v0_9_TO_v0_10.diff` is exact. Not ratified. It authorises nothing. It is the companion of the system
specification DRAFT v0.4 and says how that document's sections 2 to 4 and 12 to 14 are carried out.
**Written:** 21 November 2026, by the Claude web chat (primary designer and coder), on the project owner's go of 22:39
(decision log entry 137). Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review. **Risk tier:** HIGH.
**It is a complete document.** Section 16 lists what is withdrawn and what is carried.

## 0. In plain English

1. One small settings file in each tree says what the tree is and where its backups go. The tools check it every time.
2. Installs copy named files from the DEV folder on this PC. No Git, no network.
3. **The marker is the whole of readiness.** A variant, or the infrastructure, is installable when its marker in DEV
   matches its files. QA is never required. Each install checks itself in the tree it installs into, and makes every
   new variant forecast once before it is finished.
4. An operation that stops half-way leaves a barrier that keeps every job out until the same command finishes it or
   the owner restores a backup of his choosing.
5. **Before files are overwritten the usual backup is attempted and its result told truthfully; then one warning and
   one question whose default answer is NO.** No backup is a condition of anything.
6. Two copies read PROD and never write it: QA's installed software can be replaced by PROD's, and QA's or DEV's
   research data by PROD's. They are separate commands and neither starts the other.
7. Backups, the recovery kit and the exact restore are as already reviewed.

@@KEEP 1@@
## 2. What a QA or PROD tree holds

    <tree_root>\
        ENVIRONMENT.ini
        Run_Research.bat  Rerun_Walk_Forward.bat  Check_Forecasts.bat  Withdraw_Variant.bat
        Run_Results_Updater.bat  Run_Snapshot.bat  Verify_Tree.bat
        create_venv.bat  install_upgrade_dependencies_into_venv.bat  activate_venv.bat  deactivate_venv.bat
        src\                       exactly the files of the infrastructure manifest, and the installed variants and helpers;
                                   in each variant folder its VARIANT_STATUS.ini (specification 3.5)
        source_data\               the accepted results, their version ledgers and verification records
        results\research\          the lists, the OV-1 ledger and the reports (specification sections 5, 9, 10)
        results\research_set_aside\   what historical walk-forward reruns set aside (specification 7A.4); never read again
        scratch\                   smoke cases and Check_Forecasts reports; normally empty
        records\
            INSTALLED_FILES.json   every installed software file with its SHA-256, each variant's fingerprint, and each
                                   status file by name only
            INSTALL_LOG.jsonl      one line per finished install, reinstall, replacement, creation, verification, withdrawal
            SNAPSHOT_LOG.jsonl  INIT_RECORD.json  RESTORE_<date>_<time>.json
            INSTALL_IN_PROGRESS.json  RERUN_IN_PROGRESS.json  RESEED_IN_PROGRESS.json
            JOB.lock  SNAPSHOT_DUE  SNAPSHOT_IN_PROGRESS.lock                                    control files
        .venv\                     built by the owner; holds ENVIRONMENT_VERIFIED.json

    <backup_root>\
        <ROLE>_<YYYYMMDD>_<HHMMSS>_<JOB>.zip  and  .sha256        backups (section 10)
        KIT_<YYYYMMDD>_<HHMMSS>_<software fingerprint>.zip  and  .sha256      recovery kits (section 11)

There is no Git folder, test, document or exchange file in a QA or PROD tree. **The only files under `src\` that are
written after installation are the status files,** by the two commands the specification names. `Run_Results_Updater.bat`
runs in PROD only; in QA its guard refuses. DEV has the same `records\` and `scratch\` folders for its own jobs, ignored
by Git.

**The install tools live in DEV** (`deploy\`, standard library only) and are run from DEV: `Make_Installable.bat`,
`Install.bat`, `Reinstall_Infra.bat`, `Init_Tree.bat`, `Check_Tree.bat`, `Replace_QA_Software_From_PROD.bat`,
`Reseed_Research_Data_From_PROD.bat`, and the DEV conveniences `Who_Uses.bat` and `Make_Successors.bat`.

## 3. What can be installed, and what an install checks (owner, entry 126; EX_264 R5-F02, R5-F03)

**3.1 What can be installed from DEV, and only this.**
- *Variants:* for each ready variant, exactly the files its marker lists: `VARIANT.json`, the files that declaration
  lists, and the helpers it lists (specification 3.4, 4). The marker itself, DEV's own status file and any cache are
  never copied. The target's status file is created by the installer.
- *Infrastructure:* the files listed under `[files]` in DEV's `deploy\INFRA_MANIFEST.ini`, when
  `deploy\INFRA_IS_INSTALLABLE.json` matches. `Make_Installable.bat INFRA` writes that marker: the SHA-256 of the
  manifest itself, of every file under `[files]` and of every file under `[install_tool]`, and one fingerprint over
  them, computed as for a variant. **The marker is not on the manifest, so it is not in its own hash.** A listed file
  that does not exist refuses. The manifest's exact syntax and its three classes are in specification 12.4.
- Nothing else in DEV is ever read for copying. A file under `src\` in a target that is neither is a refusal.

**3.2 The markers are the whole of readiness (owner).** PROD is installed on the DEV markers alone. There is no pass
record, and **no install reads QA in order to decide about PROD, or PROD in order to decide about QA.** QA and PROD are
each installed from DEV, in any order, or QA not at all. (The two copies of sections 6A and 6B read PROD in order to
write QA or DEV. They are not installs into PROD and decide nothing about it.)

**3.3 What every install checks in its own target,** and stops on (specification 12.3 has the reasons):
1. the markers match DEV's files now; no undeclared file in a variant folder;
2. add-only: no installed scientific file would change; no unexpected file under `src\`; every status file passes its
   own check;
3. after copying, every installed file equals the plan;
4. **each new variant's smoke case, for each game it supports,** with the target's Python, writing only under
   `scratch\`: a complete forecast, or the install stops;
5. the suite, with the target's Python on a temporary copy, when the target's infrastructure is file for file DEV's;
   otherwise it is not run and the tool says why;
6. the fixed sample of stored forecasts, recomputed and compared;
7. the derived results in full: every score and the prevailing ledger, recomputed and compared.

**3.4 Helpers are never updated in place (owner).** No command overwrites an installed helper, proved harmless or not.
A wrong helper is handled in DEV: `Who_Uses.bat` finds the variants that declare it; `Make_Successors.bat` prepares
a successor folder for each, pointing at the corrected file (it refuses an existing name, changes no existing folder,
copies no marker and no status file, and withdraws nothing); the owner reviews, marks the batch, and installs it in
the ordinary way. Whether and when he withdraws each old variant is his own separate act (example 7).

## 4. Creating a tree: `Init_Tree.bat QA|PROD`

| Step | What happens |
|---|---|
| 1 | Settings checked (section 1). The target root does not exist, or is empty, or holds this same unfinished creation |
| 2 | The plan: the infrastructure manifest's files (its marker must match) and every ready variant with its helpers, all hashed. It is shown; the owner types the confirmation |
| 3 | The process check (section 9). The folder is created; `ENVIRONMENT.ini` (create-only) and the barrier `records\INSTALL_IN_PROGRESS.json`, holding the plan, are written |
| 4 | Every planned file is copied from DEV: to a temporary name, hashed, renamed into place. Each variant's status file is created as `ACTIVE` |
| 5 | The accepted results are copied (QA: from PROD, or from DEV while no PROD exists; PROD: from DEV), each file hashed on both sides; the list is kept as `INIT_RECORD.json`. No forecast, score, report or OV-1 record is copied |
| 6 | **It stops and asks the owner to build `.venv`** with `create_venv.bat` and `install_upgrade_dependencies_into_venv.bat` in the new tree. The same command typed again goes on |
| 7 | The whole tree's software is checked against the plan. The checks of 3.3 that apply to an empty tree: the suite (the infrastructure is DEV's), and every variant's smoke case. On success `ENVIRONMENT_VERIFIED.json` is written |
| 8 | `INSTALLED_FILES.json`; the log line; the recovery kit, written and checked (a failure is reported and asked about, default NO); the barrier removed, last |
| 9 | The `INIT` backup is attempted and its result reported. The owner then runs the research job |

## 5. Adding variants: `Install.bat PROD` (or `QA`)

The same steps, texts and question in QA as in PROD: it is the same code.

| Step | What happens |
|---|---|
| 1 | Settings and role checked. The plan: ready variants the target lacks (narrowed by `--only`), their files, and helper files the target lacks. A helper the target holds with other bytes refuses. Shown: to add; left out, each with its reason (not marked; marker does not match its files; an undeclared file in its folder; already installed; already installed with different bytes). Nothing to add: end, target untouched |
| 2 | The process check; no job lock, updater lock, orphan marker or other unfinished operation |
| 3 | The recovery kit for the new software state is written. A failure is noted for step 5; it does not stop the install (owner, entry 136) |
| 4 | The `PRE_INSTALL` backup is attempted. Its result is noted for step 5 exactly as it is: made and verified, with its name; or not made, with the reason |
| 5 | **One question for the whole batch:** the batch; "the backup taken just now: <result>"; "the recovery kit: <result>"; if either failed, "NO ROLLBACK POINT WAS CREATED BY THIS INSTALL" or "THE RESTORE TOOL COULD NOT BE WRITTEN: an existing kit in your backup folder still works for older backups". "Type YES to proceed. Anything else, Enter included, is NO." NO leaves the target's software untouched |
| 6 | The barrier, holding the plan; the updater's own lock is taken; `SNAPSHOT_DUE` |
| 7 | Each new file: temporary name, hash, rename. Each new variant's status file is created as `ACTIVE`. No existing file is opened for writing |
| 8 | The whole tree's software against the old list plus the plan; nothing unexpected under `src\` |
| 9 | The checks of 3.3, items 4 to 7. A failure stops here with the barrier in place |
| 10 | `INSTALLED_FILES.json`; the log line; the updater's lock released; the barrier removed, last |
| 11 | The `POST_INSTALL` backup is attempted and its result reported. Installation is release: the owner's next `Run_Research.bat` fills the new variants' history |

## 6. Updating infrastructure: `Reinstall_Infra.bat PROD` (or `QA`) (EX_264 R5-F04, R5-F05; owner, entries 135, 136)

It overwrites files, so it tells the owner what it will change in the science before he answers, and it asks the
question of specification 12.4. **It never recomputes history and never starts a rerun.**

| Step | What happens |
|---|---|
| 1 | Settings and role checked. The infrastructure marker must match. The plan is the difference between DEV's manifest files and the target's infrastructure: files to add, to overwrite and to remove, each with both hashes and its class (`forecast`, `derived`, `other`); the text differences are shown. No path under a family folder or `_shared\` can be in it. No difference: end |
| 2 | The process check; no job lock, updater lock, orphan marker or other unfinished operation |
| 3 | **What it would change, found before anything is overwritten.** The software as it would be is assembled in a temporary folder. With the target's Python, reading the target's data and writing nothing in the tree: the suite; every score and the whole prevailing ledger recomputed and compared with what is stored (exhaustive); the fixed sample of stored forecasts recomputed and compared. One of the three statements of specification 12.4 is produced |
| 4 | The recovery kit for the new software state is written; the `PRE_INFRA` backup is attempted. Each result is noted exactly as it is. **No earlier backup is looked for, counted or verified** |
| 5 | **The warning and the one question** (specification 12.4, in full): the plan; step 3's statement; the warning text; "the backup just attempted: <result>"; "the recovery kit: <result>"; "Type YES to proceed. Anything else, Enter included, is NO." NO changes nothing in the tree's software |
| 6 | The barrier, holding the plan; the updater's own lock; `SNAPSHOT_DUE` |
| 7 | New files: temporary name, hash, rename. Overwritten files are replaced by rename. Removals come after all copies |
| 8 | The whole tree's software against the old list changed by the plan |
| 9 | In place, with the target's Python: the structure; every installed variant's smoke case (an infrastructure change can break a variant that was fine); the suite |
| 10 | `INSTALLED_FILES.json`; the log line; the updater's lock released; the barrier removed, last |
| 11 | The `POST_INFRA` backup is attempted and its result reported. If step 3 found that stored scores or OV-1 lines change, the tool ends by naming the command the owner now owes that game: `Rerun_Walk_Forward.bat --game <game> --from <X> --derived-only`. Until he runs it the job withholds (specification 5.8) |

- **If step 9 fails** the barrier stays and no job runs. The ways out, said as they are: correct the cause in DEV, mark
  the infrastructure again, and run `Reinstall_Infra.bat <role> --replace-unfinished`, which shows the unfinished plan
  and the new one and asks the same question; or a manual restore of the whole tree from a backup the owner chooses.
  **`PRE_INFRA` is named as a way back only if step 4 made and verified it.**
- Backups are named `PRE_INFRA` and `POST_INFRA`.

## 6A. The QA software replacement from PROD: `Replace_QA_Software_From_PROD.bat` (owner, entries 135, 136)

Run from DEV. The destination is QA and nothing else. What it is for and what it leaves alone: specification 12.7.

| Step | What happens |
|---|---|
| 1 | Settings checked (section 1). QA's own file says `role = QA` and PROD's own says `role = PROD`; the two roots and DEV's are three different folders. Anything else refuses: there is no option to name another destination |
| 2 | **PROD is read, and found still.** No control file in PROD's `records\` (a job, an install, a rerun, a reseeding, a backup or a restore in progress); no Python process of the PROD tree in the process table. PROD's `INSTALLED_FILES.json` is read and every file it lists is hashed and must equal it, with nothing unexpected under PROD's `src\`. A PROD that does not match its own list is not copied |
| 3 | The plan, shown: what leaves QA (variants, helpers and infrastructure files QA holds that PROD does not, or holds with other bytes); what arrives; "each variant's status file arrives as PROD holds it: <the withdrawals and eligibility draws>"; and "QA's research data is not touched. After this, <n> of QA's lists will not match the software and will be ignored until you reseed QA's research data from PROD or rerun those variants" (worked out from the list headers) |
| 4 | The process check for QA; no QA job lock, orphan marker or unfinished operation |
| 5 | The recovery kit for the software state QA will have; the `PRE_REPLACE` backup of QA is attempted. Each result noted exactly as it is |
| 6 | **The warning and the one question:** "This REMOVES the software installed in QA <root> and puts PROD's in its place. QA's settings, Python environment and research data are kept." Then the backup's and the kit's results and the same YES-or-NO rule as section 5 |
| 7 | The barrier in QA (`records\INSTALL_IN_PROGRESS.json`), naming this operation and PROD's software fingerprint; `SNAPSHOT_DUE` |
| 8 | Every file on PROD's list is copied into `src.incoming\` and `launchers.incoming\` inside QA's root: temporary name, hashed against PROD's list. PROD's files are opened for reading only |
| 9 | **PROD is read again:** the same control-file and process check, the list, and every file's hash. Any difference: the incoming folders are removed, QA's software is as it was, and the tool refuses ("PROD changed while it was being read") |
| 10 | The swap: QA's `src\` is renamed to `src.outgoing\`; `src.incoming\` is renamed to `src\`; each root launcher is replaced by rename; `src.outgoing\` is deleted. QA's `ENVIRONMENT.ini`, `.venv\`, `source_data\`, `results\`, `records\` and `scratch\` are never opened for writing by this step |
| 11 | QA's software is read again and must equal the plan. QA's own `INSTALLED_FILES.json` is written from QA's bytes; the log line. Nothing of PROD's `records\` was copied |
| 12 | With QA's Python: the structure; every status file's own check; every variant's smoke case. The suite is run only if this software's infrastructure is file for file DEV's. **If any smoke case fails, QA's `ENVIRONMENT_VERIFIED.json` is removed:** the replacement is complete, but every QA launcher refuses until the owner rebuilds QA's environment and runs `Verify_Tree.bat QA` |
| 13 | The barrier removed, last. The `POST_REPLACE` backup is attempted. The tool ends by repeating which of QA's lists are now foreign and whether QA's derived results will be withheld, and the two commands that settle it |

Stopped before step 10: QA's software is untouched; the same command starts again. Stopped during or after step 10:
the barrier keeps every QA launcher out; the same command does the whole replacement again from PROD. A half-replaced
QA is never runnable.

## 6B. The research-data reseeding from PROD: `Reseed_Research_Data_From_PROD.bat QA` (or `DEV`) (owner; EX_265; entry 135)

Run from DEV. What it copies and what it never copies: specification 14.2.

| Step | What happens |
|---|---|
| 1 | Settings checked. The destination is QA or DEV as its own settings file says; PROD's own file says `role = PROD`. A destination that is, or is another name for, PROD, PROD's backup root or anything inside either refuses |
| 2 | **PROD is found still, by reading:** as 6A step 2, first sentence. Then the inventory of PROD's research data: the accepted-results set in `source_data\` (the results files, their version ledgers, verification records and the updater's own kept copies) and everything under `results\research\`, each path with its size |
| 3 | The destination is quiet: the process check; no job lock or unfinished operation |
| 4 | **The summary and the one question:** what will be removed from the destination (how many lists, reports and ledgers; its last draw on file); what will arrive (the same counts for PROD); "these <n> lists from PROD will be ignored here, because the variant is not installed here or is installed with other bytes: <names>"; "the destination's software, status files, settings and environment are not changed". "This DELETES the research data now in <role> <root>. Type YES to proceed. Anything else, Enter included, is NO." No backup is taken first (owner) |
| 5 | Every inventoried file is copied into `reseed.incoming\` inside the destination's root, hashed as it is read. PROD's files are opened for reading only |
| 6 | **PROD is read again:** the control-file and process check; the same set of files; every file hashed again and equal. Any difference: `reseed.incoming\` is removed, the destination is unchanged, and the tool refuses |
| 7 | The barrier `records\RESEED_IN_PROGRESS.json` in the destination |
| 8 | The destination's `results\research\` and its accepted-results set are removed; the incoming folders are renamed into their places |
| 9 | The destination's research data is read again and must equal PROD's hashes. The barrier removed; `SNAPSHOT_DUE`. The tool reports the counts, the lists that are foreign here, and that the next `Run_Research.bat` will show what is withheld, if anything |

- Stopped before step 7: the destination is unchanged (an `reseed.incoming\` left behind is removed by the next run).
  Stopped after: every launcher of the destination refuses until the same command is run again, which copies afresh.
- In DEV the accepted-results files are tracked by Git, which will show them as changed. That is expected; whether to
  commit them is the owner's choice and nothing depends on it. No other file of DEV's `source_data\` is touched.
- A set-aside folder (specification 7A.4) is not research data in use: it is neither copied from PROD nor removed
  from the destination.

## 7. Verifying a tree: `Verify_Tree.bat` (run in the tree, after its environment is rebuilt)

Process check; a backup attempted; the structure; every installed variant's smoke case; the suite, if the tree's
infrastructure is file for file DEV's; the fixed forecast sample, whose differences after an environment change are
**reported** for the W-23 review and do not by themselves refuse; the derived results in full;
`ENVIRONMENT_VERIFIED.json`; a backup attempted. A failed smoke case or suite writes no marker and removes an older
one. The owner's install script removes the marker before it changes anything. The environment's digest is taken
over the fixed inventory of specification 13, which does not contain the marker.

## 8. When an operation stops half-way

| State found | Meaning | What the same command does | The other way out |
|---|---|---|---|
| `INSTALL_IN_PROGRESS.json` exists and its plan equals the plan now | this operation was interrupted, or a check failed and the cause is now corrected | continues: files already in place with the right hash are skipped; the checks run again | a manual restore from a backup the owner chooses |
| It exists with another plan | a different operation is unfinished, or DEV changed meanwhile | refuses and shows both plans. For an infrastructure reinstall, `--replace-unfinished` goes on with the new plan after the same question | finish that one, or a manual restore |
| It names a QA software replacement | the replacement was interrupted | does the whole replacement again from PROD | a manual restore of QA |
| `RESEED_IN_PROGRESS.json` exists | a reseeding was interrupted after the old data was removed | copies afresh from PROD and finishes | a manual restore of the destination |
| `RERUN_IN_PROGRESS.json` exists | a historical walk-forward rerun was interrupted | the same rerun command with the same scope continues | a manual restore |
| `INSTALLED_FILES.json` and the tree differ, no barrier | something changed a file outside the tools | every launcher and tool refuses, naming the file | a manual restore; in QA, the software replacement |

While any of these files exists every launcher in that tree refuses, except the command that finishes it. A file not
on `INSTALLED_FILES.json` is never run. **No tool names a particular backup as the way back unless it made and
verified that backup itself, in that run** (R5-F04). Every restore is the owner's own act, from the backup he chooses.

## 9. The guard and the process rules (kept; no program ever ends a process)

**At every launch,** inside the Python pre-check each launcher already makes: the settings file is present and names
this folder and a role this launcher may run in; none of `INSTALL_IN_PROGRESS.json`, `RERUN_IN_PROGRESS.json`,
`RESEED_IN_PROGRESS.json`, `RESTORE_IN_PROGRESS.json` or `SNAPSHOT_IN_PROGRESS.lock` (the command that finishes one of
them excepted); in QA and PROD, `ENVIRONMENT_VERIFIED.json` is present and lists the installed distributions (a cheap
first gate only).
**At the start of a research job or a rerun, in QA and PROD:** the environment's digest equals the marker's; every
installed software file equals `INSTALLED_FILES.json`, every status file is present and passes its own check, and
nothing else lies under `src\`; no orphan marker (`transitory_data\poc_runs\UNRESOLVED_ORPHAN.json`; nothing installed
outside DEV writes one, and the check stays); the job lock is taken; no other Python process of this tree is running.

| Operation | Process rule |
|---|---|
| Research job; rerun; `Check_Forecasts`; a backup (before and after) | no other Python process **of this tree**: its executable is the tree's own, or its working folder is under the tree, or its command line or an ancestor's names the tree. Unrelated Python work on the PC does not count |
| `Init_Tree`, `Install`, `Reinstall_Infra`, `Verify_Tree`, and the QA software replacement as it applies to QA | the existing rule of design 6.1, unchanged, applied to the target tree, the tool's own chain excepted. As today, another Python job from the same Python installation (a Claude Code task, say) is listed and must be finished first |
| The reseeding, as it applies to its destination | no other Python process of the destination tree |
| **PROD, when it is only read** (6A, 6B) | no Python process of the PROD tree, and no control file in PROD's `records\`, checked by reading, before the copy and after it. Nothing is written to PROD to mark or lock it |
| Restore | **no Python program at all on the PC** but the restore tool, read from Windows' process table with the standard library; checked before the old tree is renamed and again after; a table that cannot be read refuses |

The tools of the process and records kind that write refuse while a backup is in progress; the read-only quiet check
does not.

@@KEEP 10@@
@@KEEP 11@@
@@KEEP 12@@
## 13. Preserving the old project folder: the owner's own ZIP (owner, entries 130, 131)

There is no tool for this. Before phase 1 moves any source file in DEV, the owner himself makes one full ZIP of the
whole project folder on E:, with the old run folders that Git ignores and `.git` included, and keeps it off E:. Claude
tells him when it is time. Advice given to him, not a rule: nothing of the project running while he makes it; open the
ZIP once to see that it reads; the old `.venv` is his choice. Specification 17.2 says what that ZIP is for.

@@KEEP 14@@
8. **QA's software replaced from PROD.** PROD holds V1 and V2 with infrastructure I1; V1 is withdrawn from 1601. QA holds
   V1 (active), an experimental V3 and infrastructure I2. `Replace_QA_Software_From_PROD.bat` shows: "leaves QA: V3, 4
   files of I2; arrives: V2, 4 files of I1; V1's status file arrives as PROD holds it: withdrawn from 1601; QA's
   research data is not touched: 2 of QA's lists (V1, V3) will not match and will be ignored". The owner types YES.
   Afterwards QA's software is V1, V2 and I1; its settings, `.venv` and backup folder are its own; PROD is unchanged to
   the byte. QA's next job warns that V1's list (it has scores after 1600) and V3's list are foreign and ignored.
9. **QA's research data reseeded from PROD, software left alone.** QA holds I2 and V3. `Reseed_Research_Data_From_PROD.bat
   QA` shows what goes and what arrives and that no list for V3 exists in PROD. YES. QA's lists, reports and ledgers
   are PROD's; QA's software and status files are as they were. QA's job then fills V3's history, and, because I2's
   scoring differs from I1's, says "derived results withheld from draw X" (the first draw that differs) until the
   owner runs the derived-only rerun in QA. Stopped during the copy: QA is unchanged. PROD is unchanged to the byte either way.
10. **A full mirror, on demand.** The owner runs example 8's command and then example 9's. QA now has PROD's software,
   status files and research data, with its own settings and environment. QA's job finds nothing foreign and nothing
   withheld, and its prevailing score is PROD's, line for line. No claim is made that the two environments compute
   identically until the job has shown it.
11. **A rerun of a range.** In QA: `Rerun_Walk_Forward.bat --game POWERBALL --from 1550 --to 1650`. The scope is shown,
   with "draws after 1650 are left for the next Run_Research.bat"; the owner types `QA`. The old lines from 1550 on go
   to a set-aside folder; 1550 to 1650 are computed; reports and both OV-1 records for those draws are rebuilt. The
   next ordinary job catches up from 1651.
12. **An infrastructure overwrite with no backup.** T: is unplugged. `Reinstall_Infra.bat PROD` shows the plan and "No
   stored result changes"; the kit cannot be written; the `PRE_INFRA` backup cannot be made. The warning says both,
   in those words, and asks. Enter: nothing is overwritten. On a second run the owner types YES: the files are
   replaced and checked; nothing at any point says a backup exists.
13. **A corrected scoring file.** `Reinstall_Infra.bat QA` shows: "This changes stored scores or OV-1 lines, for POWERBALL
   from draw 1612." YES. QA's job forecasts as usual and withholds scores, reports and the prevailing line from 1612.
   `Rerun_Walk_Forward.bat --game POWERBALL --from 1612 --derived-only` settles it. Satisfied, the owner installs the
   same correction into PROD and, when he chooses, runs the same rerun there, typing `PROD`.

## 15. Tests and the rehearsal

**Tests** (invented trees in temporary folders): each check of section 1 with one wrong setting; each step table with
a fault planted after every step, then the command again; every state of section 8; the two kinds of marker
(matching; one file edited afterwards; made by hand with a wrong hash; made twice, identical; never listing itself);
a settings file never written after its creation; add-only (a changed, a removed and an added helper); the manifest
(a malformed line; a duplicate; a listed file missing; an unknown class; an imported module not listed; a wrong
class caught by the import test); unexpected files under `src\`; the guard in each role; the updater launcher
refusing outside PROD; **the smoke case** (a broken new variant stops the install behind its barrier; an
insufficient-history answer fails; only `scratch\` is written); **the backup and kit questions** (each failing alone
and together; the result told exactly; Enter and NO change nothing; YES proceeds; no text ever names a backup that
was not made); **the three statements of an infrastructure reinstall,** each from a planted change; no rerun ever
started by an install; `--replace-unfinished`; **the QA software replacement** (the example of 8; PROD hashed whole
before and after; PROD changed during the read; a destination that is PROD or DEV by any name; a failing smoke case
leaves QA refusing; stopped at every step); **the reseeding** (PROD hashed whole before and after a successful, a
failed and an interrupted copy; PROD changed during the copy; a busy destination; stopped before and after the
barrier; into QA and into DEV; the foreign-list count foretold equals the count found); backups (a member changed in
the archive; a file changed, added or removed during the backup; not quiet; a link; a full disk; the due flag across
jobs of different kinds); the kit's self-check; restore (from a kit by a bare Python with DEV and QA out of reach;
the exact allowed set, status files included; old tree absent or damaged; a Python process present; stopped
half-way; READY and NOT READY; the orphan condition; the hand unzip and its reconciliation; **nothing installed
afterwards**).

**The rehearsal on the owner's PC** (one task file, its own go, scratch folders, invented data only): three scratch
roots set in a scratch settings file; `Init_Tree` for a scratch QA and a scratch PROD; an `Install` into each; a
`Reinstall_Infra`; an install with a fault planted and the command typed again; jobs ending in backups; a withdrawal
and the status file read in Notepad; the QA software replacement and the reseeding between the two scratch trees,
with the scratch PROD hashed before and after; a rerun of a range; one backup of a tree of the real size opened in
**File Explorer by the owner**; one restore from the kit with a stale orphan marker and a restart; the Windows process
table and start time read by the standard library; **the time the derived check, a backup and a `Check_Forecasts
--all` take.** No step changes the PC's date, time or zone; nothing is terminated; no real data is read; no lottery
site is contacted.

## 16. Withdrawn from the earlier notes and drafts, and carried

**Withdrawn:** a release as a named Git commit, its hash list and `deploy\RELEASE.json`, and bytes read from Git
objects; the install record, the release record and the barrier under `src\`; the old `export` mode to the clone and
Git, and `export --after-restore`; `PRODUCTION_ROOT.json` and the settings JSON (replaced by `ENVIRONMENT.ini`); the
modes `check`, `init`, `update` under those names; the weekly and development sequencers; the note v0.6's reading
table; the QA pass record and the five checks of DRAFT v0.7; every OV-1 restore rule; "later releases first" after a
restore, in every form. **From DRAFT v0.9:** `Cold_Copy.bat` and its settings section (the owner makes his own ZIP);
the recomputation of every forecast and score at an infrastructure reinstall; "the way back is the `PRE_INFRA` backup"
said of a backup that might not exist; a PROD install stopping for want of a recovery kit; any difference between
QA's and PROD's steps or questions.
**Added in v0.10:** the smoke case; the backup and kit results told before one default-NO question; the three
statements of an infrastructure reinstall; the QA software replacement from PROD; the research-data reseeding from
PROD (the owner's choice E; it copies to QA or DEV and never to Git).
**Carried, as reviewed:** complete-tree ZIP backups, their two verifications and the quiet rule; the due flag and
"work goes on"; `PRE_` and `POST_` backups, now attempts whose results are reported; the recovery kit; the exact
restore with its payload check, its process rule, the hand unzip and the orphan-marker exception; the environment
built by the owner and verified before use; W-23; the guard inside each launcher's own pre-check; no program ends a
process.

## 17. Not designed here, and uncertainties

- Nothing here has run. Unmeasured: a backup of a whole tree with its environment; the derived check; a
  `Check_Forecasts --all`; File Explorer on an archive of that size (the fallback of several smaller ZIPs under one
  manifest is not designed unless needed).
- **The tests live in DEV and belong to DEV's infrastructure.** A target whose infrastructure is older than DEV's
  (PROD between reinstalls; QA after a replacement from PROD) cannot be given the suite honestly, so there the smoke
  cases, the forecast sample and the full derived check stand in for it, and the tool says so. Keeping the matching
  tests with each installed software state would close that gap; the owner has ruled tests out of QA and PROD, so it
  is not proposed.
- Reading PROD "found still" rests on PROD's control files and the process table at two moments, and on every file's
  hash being the same at both. A change made and undone exactly between the two readings would not be seen; no such
  writer exists in the design.
- Windows may update last-access times when PROD's files are read. The tests compare content, names, sizes and
  modification times.
- Reading Windows' process table and start time with the standard library is to be shown in the rehearsal.
- A restored environment may not start if the PC's base Python has changed since the backup; the restore says so.
- The design 6.1 process rule lists unrelated Python work from the same installation during an install; with three
  environments sharing one Python this will be met. I recommend living with it.
- DEV's settings file holds the paths of all three trees. If it is lost it is typed again from the example; each
  tree's own file is what actually protects a tree.
- The code round lists exactly what the suite needs from the repository, so that the temporary copy is complete;
  that list sits beside the infrastructure manifest. Tests that served only the old system are not part of the new
  suite.
- The run sheets (creation of QA and PROD; an environment change; a withdrawal; a QA mirror; a rerun; a restore) are
  written and reviewed with the code packages.

End of the deployment design, DRAFT v0.10.
