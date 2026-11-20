# MHUP-B deployment design note - DRAFT v0.3

**Status:** DRAFT v0.3 for the reviewer's focused R-3 recheck. Not ratified. It authorises nothing. It answers EX_250
(a narrow RECHECK: R3-C01, R3-C02) and carries the owner's decisions of 20 November 2026 on full backups, the
recovery kit and the environment (decision log entries 112 and 113). Section 18 says where each finding landed.
v0.1 (EX_247) and v0.2 (EX_249) are kept beside it; `NOTE_v0_2_TO_v0_3.diff` is exact.
**Written:** 20 November 2026, 16:40 Australia/Adelaide, by the Claude web chat (primary designer and coder), under the project
owner's go of 19 November 2026 for the design note (decision log entry 107; entries 110 and 113). Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH (it replaces part of a ratified install procedure, design Appendix J; it touches gates, installs
and the formal OV-1 claim). **Base:** `main` at `4a72269`; staged slices as passed (EX_231, EX_237, EX_242).

## Work-item card

| Item | |
|---|---|
| Work item | MHUP-B deployment layer: design note |
| Binds it | Owner decisions D1 to D12 (EX_243; decision log 92 to 98); EX_244 (restore and replay; governs); decision log 100 (how a restore is done), 103 (Python 3.15 only), 104 (no monthly restore test), 105 (no replay comparison), 107 (the go), 110 (the nine confirmed choices; EX_248 section 1, the owner's scientific clarification), 112 and 113 (EX_250: full snapshots with `.venv`, a plain restore, before-and-after deployment snapshots, the recovery kit, A to G, H1, no Python at a restore); H-1 v7r1 section 12.11 (the checklist); the working principle of 18 November 2026 |
| Replaces | The Git-based steps of design v0.1r7 Appendix J, for production; the backup paragraph of the direction document v0.3r1 section 9 |
| Not in scope | Any code, package, task file, Windows step, install, restore or run. Slices 1 to 3 are not reopened |
| Evidence state | DESIGNED. Nothing implemented or tested, except a probe and a trace on invented files (section 14) |

## 0. The whole thing in plain English

1. **Two folders.** Development stays in the Git clone on E:. Production is a plain folder on G: with no Git in it. It
   holds the code, the data and records, its own Python environment, and a small folder of deployment records.
2. **One tool, kept in the development clone and in each recovery kit, never copied into production.** It has five modes: `check` (look, change
   nothing), `init` (make production the first time), `update` (bring in a new reviewed release), `export` (copy
   records back to the clone so they can be committed and pushed) and `restore` (your method: rename the old tree
   aside, unpack a snapshot into a fresh tree). Every mode can be run again after a fault and picks up where it was.
3. **A release is a named commit of `main`, proved by file hashes.** The reviewed package states the hash list's
   digest; the tool recomputes it from the commit and refuses if they differ; production's files are then checked
   against the same list. Git is used only on the E: side.
4. **`update` keeps Appendix J's safety, without Git:** the same process check, the same two barriers (the updater's
   lock and the install-in-progress file), the test suite before release, the same install and release records with
   the same meaning. What Git used to prove ("committed and clean") is proved by hashing every file instead.
5. **A snapshot is one ordinary `.zip` of the COMPLETE production folder,** its Python environment included; only two
   temporary control files are left out. It is written by Python's own `zipfile`, taken only when production is quiet,
   and checked twice before it counts (the archive read back; the files read again). It goes to
   `T:\a_p_r_i_r_backups`, named with the date and time. Every production job ends with one, `update` also takes one
   before it changes anything, and `Run_Production_Snapshot.bat` takes one whenever you like. A "snapshot due" file,
   written before a job's first write, makes the next job take a missed one first. If one cannot be made, every job
   goes on with a loud warning that stays until one is made (your decision; the risk is stated in section 7).
6. **A recovery kit** for each release: a small, separate, dated, hash-checked `.zip` on T: holding the restore tool,
   the release's hash list and plain instructions. An emergency restore runs from the kit with whatever Python is
   installed; it needs neither the E: clone nor a working production folder. `update` and `init` stop if the kit
   cannot be written to T:.
7. **Restore** is plain: verify the snapshot, check that no Python program is running on the PC, rename the old tree
   aside (kept), unpack the whole snapshot at `G:\a_p_r_i_r`, verify every file, and it is ready to run, environment
   and all. Then you work normally: the updater, then the weekly session, replay the missing draws one at a time from
   the draws before each. That is the same chronological process and valid research (EX_244; EX_248 section 1).
   Nothing is compared with the old tree, no timestamp proof is asked for, nothing stops. As the very last resort you
   can unzip a snapshot by hand; the kit's instructions say what to run afterwards.
8. **The formal OV-1 claim is kept apart, with no human choice.** A trace of the passed code (section 9) shows the one
   thing a restore changes: a draw that was counted before the restore can come back as "missed". The fix is one
   objective check in the recorder, fed by a small restore notice: such a draw makes the *registered formal claim*
   read "not established from draw T". Forecasting, scoring, league tables and the descriptive OV-1 view never wait
   for it and are never changed by it.
9. **A marker file** at the production root, checked with its path at every real-data launch, so nothing real starts
   in the E: clone or in a copied or set-aside folder. The proof-of-concept suite still runs where it does today.
10. **A stale orphan marker never blocks a restore for ever and is never copied back as a live block:** restart the PC
    (checked), a clean process check, and your typed acknowledgement (section 8).
11. **Production's Python environment is built your way,** with your own scripts, as on E:. After any build or change,
    one command verifies it (the whole test suite with production's own Python); until then no launcher runs.

Every choice put to you so far is confirmed and listed in section 15.

## 1. What I read and verified first

- **Read in full for this note:** `src/package_tools/install_records.py` and `process_check.py`;
  `src/methods/_common/closure.py` (its contract and the closure listing); design v0.1r7 sections 4.3, 6.1 and
  Appendix J; supplement v0.8 section 6.8; the staged `sequencer_children.py`, `Weekly_Session_Orchestrator.py`,
  `Run_Weekly_Session.bat`, `ov1.py` (the recorder, its reconciliation and the owner stop), `league_publish.py` (what it
  replaces in place); `.gitignore`; `.gitattributes`; the dependency installer's package list.
- **Facts verified with a tool (each bears on the design):**
  1. The install and release records live under `src/` (`src/methods/_common/contract_data/install_records/`), and the
     release record's time is read from the PC clock when it is written. So production will hold records under `src/`
     that the release commit cannot contain. Section 3 deals with it.
  2. `install_records.py` uses Git in exactly two helpers (`_committed`, `_tracked_changes`) and one root test (`.git`
     must exist); `process_check.py` in one root test. The only other places under `src/` that start Git are the
     updater's one-time INIT (done; it refuses on existing files) and the retired two-site checkers (never run, TSC-1).
  3. The closure module already lists every file under `src/` and every root `.bat` with its SHA-256, and it tolerates a
     root without `requirements.txt` or the dependency installer. The session record pins that digest and the
     environment's; a resumed session refuses if either changed.
  4. The process rule lists any Python process started from the same base Python installation. Development and
     production will share that installation, so a Claude Code task or an OUTLANDISH job running on E: makes
     production's process check refuse. That is the existing, safe false positive ("the owner closes it"); the note
     keeps the rule unchanged and states the consequence in section 4.6.
  5. Tests read repository files outside `src/` and `tests/` (`.gitignore`, `.gitattributes`, evidence files under
     `exchange/`). So the suite cannot run from a folder that holds only the release; section 4.3 runs it from a
     temporary export of the whole release commit, with production's Python.
  6. Files a production program legitimately replaces in place, among the kinds Git tracks: the league table's
     `current/` copies and `LEAGUE_SOURCES_<GAME>.json`, nothing else. The masters and their ledgers have grown only
     by appending: each game's first committed version is a byte prefix of today's (checked from Git).
  7. The third-party modules the code and tests import are `numpy`, `psutil`, `requests`, `bs4` and `selenium`. The
     development environment holds 39 direct packages (90 distributions), most of them for other work.
  8. The staged weekly sequencer already treats a stopped formal OV-1 stream as an expected state and goes on; the
     recorder's owner stop (`Method_OV1.py stop`) exists and lands at the stream's open target.
  9. **The trace of section 9** (the passed slice 3 tree run on the invented weekly project; section 14): after a
     restore the recorder re-derives a lost FACTOR line with all 17 fields equal; it records a formerly counted draw as
     MISSED when its pre-cut-off freeze line is not in the snapshot and its cut-off has passed; its own `verify` then
     passes; and in a tree whose snapshot predates the registration a second `register` is accepted.
  10. The owner's existing orphan-clearance utility (`transitory_data/P1P2_Clear_Archived_Real_Orphan_v0_1.py`) is
     written for one incident: it is pinned to that marker's SHA-256 and that incident's process identities. A new
     marker needs a new reviewed procedure. Section 8 does not change that route; it adds one other.
- **Not verified (carried to the code stage or T017):** that no reader of an existing record compares an absolute path
  stored in a record with the current root (records made on E: must read correctly on G:); File Explorer opening a
  ZIP64 archive; snapshot time on the owner's drives; that G: and T: are NTFS and distinct physical drives; how Windows
  refuses a folder rename while a file inside is open.

## 2. The production folder and the backup folder

    G:\a_p_r_i_r\                    PRODUCTION. Everything here is in every snapshot, except the two files marked *.
      PRODUCTION_ROOT.json           the marker: schema, this folder's absolute path, the time it was made, the
                                     release it was made from. Written once, last, by init or restore.
      PRODUCTION_SETTINGS.json       the owner's settings: the backup folder. Plain JSON the owner may edit.
      Run_*.bat                      the launchers (release)
      create_venv.bat, install_upgrade_dependencies_into_venv.bat, activate_venv.bat, deactivate_venv.bat
                                     the owner's own environment scripts (release), used as on E: (section 6)
      src\                           the code (release), with the install records and the barrier P where they are today
      source_data\  results\  transitory_data\      data and records, exactly as on E: today
      production_records\            written only by the deploy tool and the snapshot code:
                                     RELEASE_<commit>.json (the hash list of each release deployed; create-only),
                                     DEPLOYMENT_LOG.jsonl (its last line names the current release),
                                     SNAPSHOT_LOG.jsonl, INIT_RECORD.json, RESTORE_<date>_<time>.json (and, beside
                                     it, the bytes of any orphan marker a restore set aside as evidence),
                                     * SNAPSHOT_DUE and * SNAPSHOT_IN_PROGRESS.lock (never in a snapshot)
      .venv\                         production's own Python environment, with ENVIRONMENT_VERIFIED.json (section 6)

    T:\a_p_r_i_r_backups\            BACKUPS. Nothing here is pruned by any tool. The owner copies this whole folder
                                     to his USB3 drives and the cloud himself; no tool does that.
      PRODUCTION_<date>_<time>_<JOB>.zip          a verified snapshot, with <same name>.zip.sha256 beside it
      DEPLOY_KIT_<date>_<time>_<release>.zip      a recovery kit (section 4.7), with its .sha256 beside it
      <anything>.partial             an unfinished file: NOT a backup
      the Python installer file      kept there by the owner (one file), in case Python itself must be put back

Not in production: `.git`, `tests/`, `doc/`, `exchange/`, `review/`, `archive/`, `GAIS/`, the runner's folder. No
installed program reads any of them (CODE-3's static rule already forbids `src/` to refer to `archive/`).

**What is where, in one line each.** Inside a snapshot: all of `G:\a_p_r_i_r`, the environment, the settings, the
marker and every record included. Separate on T:, never inside a snapshot: the recovery kits and the `.sha256`
files. For a restore the owner needs one snapshot, its matching kit and a Python installation; nothing from E: and
nothing from the internet.

**Alternative considered:** putting the settings in the marker (one file). Rejected: the marker is identity and is
never edited; the backup folder is a setting the owner may change (D9).

## 3. The release, and how production is proved equal to it

- **The release set** is every file Git tracks under `src/` at the release commit, plus every tracked root file named
  `Run_*.bat`, and the owner's four environment scripts (`create_venv.bat`,
  `install_upgrade_dependencies_into_venv.bat`, `activate_venv.bat`, `deactivate_venv.bat`), as they are (today 487, 5
  and 4). Bytes: the commit's own stored bytes, except that `.bat` files are written with CRLF,
  as `.gitattributes` requires. The tool reads them from Git's objects, never from working files, so the clone's mix
  of LF and CRLF working files and any uncommitted edit cannot reach production.
- **The release description** is one small reviewed file in the package, `deploy/RELEASE.json`, outside the release
  set: the package name; the fields `process_check.py` and `install_records.py` already read from a package manifest
  (`release_entries`, `retires`, `registry_entries_added`); the expected digest of the release hash list.
- **The proof, in three links.** (1) Reviewed bytes to commit: the integrated package is applied to the clone and
  checked there by its verifier (PRE, POST, the suite, COMMITTED), as every package so far; Git lives there, so those
  steps stay. (2) Commit to hash list: the tool computes the hash list of the release set at the commit the owner
  names and refuses unless its digest equals the one in that commit's `deploy/RELEASE.json`. (3) Hash list to
  production: after copying, every production file in the release set is hashed and must equal the list; no other
  file may exist under `src/` or as a root `.bat`, except those of the next bullet.
- **Records born in production.** The install record and the release record of each package are written in production
  (the release time is production's clock), under `src/` where the one reader expects them. They are the only files
  under production's `src/` that the release commit lacks. The tool accepts exactly: records under `install_records/`
  that the records tool validates and the deployment log lists; and the barrier file P while an update is running.
  `export` copies the records back to the clone; the owner commits them; a later release contains them, and from then
  on their bytes are checked like any other file. Anything else unexpected under `src/` is drift and a refusal.
- **The commit ID is a label.** The proof is the file hashes (E2R-R54: Git history is never relied on).

**Alternatives considered.** (a) Moving the install and release records out of `src/`: cleaner, but it changes a
ratified location (design 4.3), the one reader and three installed records; rejected as disproportionate. (b) Copying
from the clone's working files: simpler, but then production's bytes would depend on the clone's line-ending state and
on uncommitted edits; rejected. (c) Deploying `tests/` and running the suite inside production: fact 5 rules it out.

## 4. The deploy tool

One program in the development clone, `deploy/Deploy_Production.py` with a small launcher, standard library only. It
starts two kinds of child process: `git` (on the E: side only, and never in `restore`) and the project's own reviewed
tools. It is reviewed code, installed into `main` by the package, and is not part of the release set; a copy travels
in every recovery kit (section 4.7). Every mode names
the production folder explicitly (`--production G:\...`).

**The process check** of `init` and `update` is the reviewed `process_check.py`, verified by hash before it is run, with
production's Python (for `init`, before production's environment exists, the development environment's). `restore`
uses its own stricter check, which needs neither (section 8).

**Re-running.** Each mode is a list of small durable steps. Each step first looks at what is already there: finished
(skip it), or half done by the same run (finish it), or something this run did not make (stop and say what). So the
same command typed again after a power cut, a full disk or a refusal goes on from where it stopped, and typed again
after success changes nothing. The tests plant a fault after every step and run the command again (section 12).

### 4.1 `check` (reads only; safe at any time)

It prints, and changes nothing: the clone's commit and the release description; production's recorded release;
whether every production file equals its release (all hashed); unexpected or missing files; the marker and settings;
the environment against `ENVIRONMENT_VERIFIED.json`; locks and barriers present; whether the orphan marker exists; `SNAPSHOT_DUE`; the
last verified snapshot; the backup folder, its free space, and whether it is on the same volume as production (a
warning: the tool cannot prove two drive letters are different physical disks, and says so); the file systems of
both; the longest path. `init`, `update` and `export` start with the checks that concern them and stop on a
refusal. **`restore` does not:** it has its own short list (section 8), because it must work when production is the
thing that is broken.

### 4.2 `init` (the first deployment; once)

1. Preconditions on the E: tree: no project process (the process check); no session lock, updater lock or orphan
   marker; `git status` shows no change under `source_data/` or `results/` (so every tracked record equals what Git
   holds, which also catches a record rewritten with CRLF). The destination does not exist, or holds an unfinished
   `init` of the same release.
2. Write and verify the recovery kit on T: (section 4.7); stop if it cannot be written. Create the folder. Copy `source_data/`, `results/` and `transitory_data/` whole, the git-ignored run folders
   included, each file hashed on both sides; the list is kept as `INIT_RECORD.json`. Nothing on E: is changed.
3. From here it is `update`'s steps 4 to 13 into an empty code tree: the barriers, the code, the check against the
   hash list, the environment, the suite, the install record, the release record (MHUP-B's has an empty entry list:
   no roster change). At the environment step `init` stops and asks the owner to build `.venv` with his two scripts;
   the same command typed again goes on (section 6).
4. Write the settings, then the marker, **last**: until the whole of `init` has passed, no launcher runs there.
5. Take the first snapshot (`INIT_<release>`). There is no earlier G: tree, so there is none before.

After `init` the E: clone still holds its old copies of the data. They are left alone (nothing is deleted); the
production guard (section 10) keeps real-data jobs from running there; `export` keeps the tracked ones current.

### 4.3 `update` (a new reviewed release into production)

| Step | What happens | Appendix J step it keeps or replaces |
|---|---|---|
| 1 | The recovery kit for this release is written and verified on T:, or the update stops there (section 4.7). `check`: production equals its recorded release (no drift); the named commit's hash list equals the package's expected digest; the new release descends from the deployed one (an older one is refused: going back is a restore) | 0, 1 (PRE; "replaced files at base bytes") |
| 2 | The install check: no project process; no session lock; no updater lock; for a roster-changing package, no unfinished weekly set | 2 (unchanged rule) |
| 3 | The `PRE_DEPLOY` snapshot of the whole tree, always attempted, while the old release is whole and quiet (section 7). If it cannot be made the update goes on with the warning NO ROLLBACK POINT WAS CREATED FOR THIS UPDATE | new (D8; EX_250 R3-C02) |
| 4 | Take the updater's lock U (`take-install-lock`); write `SNAPSHOT_DUE` | 3 |
| 5 | Create the barrier P; the install check again | 4, 5 |
| 6 | Copy the changed and new release files (each to a temporary name, then replaced); remove only files that the old hash list held and the new one does not | 6, 8. One copy, not two: Appendix J copied the gate files first because MHUP-A's old gate did not know P; the installed gate has honoured P since MHUP-A |
| 7 | The install check after the copy | 7 |
| 8 | Every production file against the new hash list; nothing unexpected under `src/` | 9 (POST) |
| 9 | The environment: never built by the tool. If it is not the verified one, the environment inventory is run here and, after step 10 passes, `ENVIRONMENT_VERIFIED.json` is written (section 6) | new (D6; H1) |
| 10 | The suite, in a temporary export of the whole release commit (so the tests find the repository files they read), run with **production's** Python; the temporary folder is then removed, and one that cannot be removed is a STOP. Production gains no file | 10 (J-1's shadow run; the barriers stay in production throughout) |
| 11 | The install check; the install record (the installed tool; P must be present, as now) | 11, 12 |
| 12 | Production against the hash list once more, with the install record; a line in `DEPLOYMENT_LOG.jsonl` | 13 (COMMITTED), replaced: see section 5 |
| 13 | The install check; remove P; the release record (it refuses while P exists, without U held by this package, with a session lock, or, for a roster change, with an unfinished weekly set: all as now; its two Git tests are replaced by "production equals its hash list and the install record validates"); validate the records; release U **last** | 14 to 18 |
| 14 | The `POST_DEPLOY` snapshot of the whole tree, verified; `SNAPSHOT_DUE` removed. Then the owner runs `export` and commits the two records in the clone | new (D8); 17, 19 (the two commits and the push become one export and one commit) |

A STOP at any step leaves U and P in place (fail closed) and prints what to send. Nothing is terminated by any tool.
Typing the same command again continues when the state is this update's own; otherwise it stops. An update that cannot
be completed is abandoned by restoring the `PRE_DEPLOY` snapshot, or the last verified one (D10), on the owner's go, with steps written for
that case, as J-3 required: no fix forward in place by hand.

**One rule about the two records.** `update` never writes an install or release record for a package whose record the
clone already holds (exported and committed after an earlier deployment). It then requires the named commit to contain
that record, and production receives the original, with its original date. This matters after a restore to a snapshot
older than an update: running `update` again brings back the original records, not second ones (section 17).

### 4.4 `export` (records back to the clone; production is only read)

- **What:** every file under production's `source_data/`, `results/`, `production_records/` (to a folder of the same
  name in the clone) and
  `src/.../install_records/` that Git in the clone would track (the tool asks `git check-ignore`, so `.gitignore` stays
  the one list; run folders, attempts ledgers, backups, grabs and locks stay out, as today).
- **How, per file:** not in the clone: copied. Identical: nothing. The clone's bytes are the beginning of production's
  (a ledger that grew): copied. **Anything else is a changed record:** the tool stops before writing anything and lists
  them. Two kinds are replaced whole by design and are exempt: the league's `current/` copies and
  `LEAGUE_SOURCES_<GAME>.json` (fact 6).
- **Every export is planned before it writes.** The tool first classifies every file on both sides (new, identical,
  grown, changed, and in the clone only), and requires the clone's `source_data/`, `results/` and
  `production_records/` to have no uncommitted change. If anything is refused it prints the whole list and writes
  nothing.
- **After a restore** production's records legitimately differ from the clone's, and the clone holds later records
  that no longer belong to production's state. An ordinary `export` then refuses (changed records). The owner runs
  `export --after-restore`, allowed only when production holds a restore record the clone does not. It makes the
  clone's active folders **exactly** production's tracked records, and nothing is deleted:
  1. every clone file that is changed, or is in the clone only, is first **moved** to
     `superseded_by_restore/<the restore's date and time>/<its same path>` in the clone (bytes checked);
  2. then production's files are copied in.
  So after it, `source_data/` and `results/` in the clone are one coherent state (production's), and everything that
  was there before the restore is in one dated folder, visibly not current, and in Git's history. An interrupted run
  is finished by typing the command again (a file already moved with the same bytes is skipped). **Active** therefore
  has one meaning: what is under `source_data/` and `results/`; a reader of GitHub is never shown a mixture.
- **A worked example (invented names).** Before the restore the clone holds the forecast ledger with freeze lines
  for draws 1 to 5, session files S4 and S5, and OV-1's ledger through draw 5. Production is restored to a snapshot
  taken after draw 3 and replays draws 4 and 5 (new session R4). Ordinary `export`: REFUSED, listing the forecast
  ledger and OV-1's ledger as changed and S4, S5 as in the clone only; nothing written. `export --after-restore`:
  the four old files go to `superseded_by_restore/20261203_101500/results/...`; the clone then holds production's
  ledgers and R4 only. The commit shows four moves and the new files.
- The tool never stages, commits or pushes. It prints the paths; the owner runs `git add` on them, commits and pushes.
  A pre-draw witness push (design 6.5) is this export followed by the push, and stays optional.

### 4.5 `restore` (section 8)

### 4.6 What the owner must not have running

While `update`, `init` or a session resume runs its process check: no Claude Code task and no other Python
job started from the same Python installation (fact 4). An ordinary weekly session with no leftover lock does not run
that check.

### 4.7 The recovery kit (EX_250 R3-C01; decision log entry 112, item F)

- **Why.** The E: clone is a working place: its files may be edited, its environment broken, or the drive gone, at
  exactly the moment a restore is needed. So the restore must not need it.
- **What it is.** `T:\a_p_r_i_r_backups\DEPLOY_KIT_<YYYYMMDD>_<HHMMSS>_<release>.zip`, made by `init` and by every
  `update` **from the release commit's own bytes** (Git's objects, as for the release itself; never working files).
  A few small files:
  - the deploy tool itself (the same reviewed file; in a kit only `restore` and `check` are of use, because the
    others need Git);
  - `Restore_Production.bat`, which starts it with whatever Python is installed for the user (the `py` launcher, or
    `python`);
  - `HOW_TO_RESTORE.txt`: the steps in plain English, the last-resort unzip by hand included;
  - the release's hash list (`RELEASE_<commit>.json`) and the release description;
  - `KIT_MANIFEST.json`: the kit's own identity (release, time, the tool's version) and the SHA-256 of every file in it.
  Beside the zip, `<name>.zip.sha256` holds the zip's own SHA-256.
- **Nothing in it needs installing.** The tool uses the standard library only. In particular its restore-time process
  check uses no third-party package (section 8), so any Python 3 the user has will run it.
- **How it is trusted.** Before doing anything, the tool run from an unpacked kit checks its own files against
  `KIT_MANIFEST.json`, and the kit zip against its `.sha256` when the zip is at hand, and prints the kit's identity.
  A digest shows accidental change or a wrong file; it is not a signature and proves nothing against a deliberate
  attacker. That is stated, not hidden.
- **Which kit for which snapshot.** Every snapshot's manifest names the release it holds and the kit made for that
  release. The matching kit is the recommended one. Because a restore is "verify, rename, unpack, verify", a newer
  kit can restore an older snapshot; the tool says when the two do not match and goes on only if the snapshot's
  format version is one it knows.
- **`update` and `init` stop if the kit cannot be written and verified on T:** (the owner: "T: must be available").
  This is checked first, before anything in production changes. It is separate from the rule for a snapshot that
  cannot be made, where jobs go on.
- **If something is missing at a restore** (no kit, no Python at all, a kit that fails its own check): the tool does
  not start, or stops before touching anything, and says what is missing. The owner's copies of T: on USB3 and in the
  cloud hold every kit and snapshot; the Python installer kept on T: puts Python back. Beyond that, the last resort
  is the unzip by hand (section 8).
- **Not a second tool.** One program, shipped twice: in the clone for `init`, `update` and `export`; in the kit for
  `restore`.

## 5. Appendix J's safety properties: kept, or consciously replaced

| Property (H-1 v7r1 12.11 checklist) | Here |
|---|---|
| 1. Code identity | Kept, stronger: every file hashed against a reviewed digest (section 3). **Replaced:** `git status` clean, `git pull`, the committed-at-HEAD test |
| 2. No evidence overwritten | Kept: `update` writes only release files under `src/`, the root launchers and `production_records/`; under `source_data/`, `results/` and `transitory_data/` it writes nothing except taking and releasing the updater's lock; the orphan marker is never touched |
| 3. The install check and the barriers U and P | Kept unchanged (the installed tools). E is E_1's alone and is not used |
| 4. No roster change under an unfinished weekly set | Kept unchanged (install check and release-record tool) |
| 5. The meaning of the install and release records | Kept: code arrival after POST and the suite; the release date is the local date of the step that writes the record; never while P or a session lock exists. **Replaced:** the two Git tests, by the hash check of step 13 |
| 6. The suite before release; the restore rule on a STOP | Kept: step 10 with production's Python. **Replaced:** `git checkout --` and `git revert` as the way back, by restoring the last verified snapshot (D10) |
| 7. A verified environment | Section 6: built the owner's way; verified by the suite with production's own Python before any launcher runs; the exact environment is inside every snapshot. v0.2's pinned lock is withdrawn (H1) |
| 8. `export` one way and non-destructive | Section 4.4 |
| 9. The production guard; every mode re-runnable | Sections 10 and 4 |
| 10. The snapshot | Section 7 |
| Appendix J's two stated residual risks (D3: three programs no barrier stops; a run straddling the gate copy) | Smaller: with the production guard every real-data launcher refuses outside production, and P is in place before any file changes. A project program started by hand between two checks remains the stated residual |

## 6. Production's Python environment (D6; the owner's decision H1, decision log entry 113)

- **Built by the owner, his way, as on E:.** `create_venv.bat`, then `install_upgrade_dependencies_into_venv.bat`, run
  in `G:\a_p_r_i_r` (both are in the release, with the two activate scripts they call). That step needs the internet,
  as it does on E: today. **v0.2's lock file and wheel folder are withdrawn.**
- **It is in every snapshot** (section 7), so a restore brings back the very environment that was running. Nothing is
  rebuilt at a restore.
- **One rule: verified before use.** After any build or change the owner runs `update` (the same command; with no new
  release it changes no code). It sees that the environment is not the verified one and: (1) runs the existing
  environment inventory, which refuses an orphan file; (2) runs the whole suite in a temporary export of the release
  commit with production's Python; (3) on a pass writes `.venv\ENVIRONMENT_VERIFIED.json` (the environment's digest,
  the installed distributions and versions, the release, the time) and a deployment-log line, and takes the
  POST-deployment snapshot. **This is the "verification command".**
- **Until then no launcher runs.** The production guard (section 10) requires that file, and requires the installed
  distributions (names and versions, read from the folder names in `site-packages`: one directory listing) to equal
  its list. A deleted and rebuilt `.venv` has no such file; an upgrade in place changes the list. Either way every
  real-data launcher refuses and says: run `update` to verify the environment.
- **The owner's procedure for an environment change** (a new Python, say), each time on his own go as a dependency
  change (W-23): in the E: clone first (rebuild; the suite by a Claude Code task, as T024 did). Then in production:
  `Run_Production_Snapshot.bat` (the "before" snapshot); rebuild; `update` (the verification and the "after" snapshot).
- **At `init`:** after the data and the code are in place, `init` stops and asks the owner to build the environment
  with his two scripts; the same `init` command typed again goes on with the verification.
- **What this gives up, stated plainly.** Production's package versions are whatever `pip` resolves that day and may
  differ from E:'s. The evidence is the suite passing in production's own environment, and the snapshot holds the
  exact files. All of the installer's 39 packages are installed, not only the five this project imports.
- **An old snapshot after a major Python change** may hold an environment that no longer starts, because a Windows
  environment depends on the base Python being where it was. The restore says so and does not call it ready
  (section 8); the fix is the same rebuild and `update`.

**Alternatives.** (1) The pinned lock and wheel folder of v0.2: reproducible and offline, but machinery the owner
would work around; he chose H1. (2) No `ENVIRONMENT_VERIFIED.json`, the rule kept by procedure only: simpler by one
small file and one directory listing per launch, but a real job on an untested environment would go unnoticed. I
recommend keeping the file; the reviewer may judge it unnecessary.

## 7. Snapshots (D7 to D9; EX_250 R3-C02; decision log entries 110 and 112)

- **What is in one: everything.** Every file and every empty folder under `G:\a_p_r_i_r`, the `.venv` included. Only
  the two control files `SNAPSHOT_DUE` and `SNAPSHOT_IN_PROGRESS.lock` are left out. No other exclusion of any kind:
  not by file type, not by `.gitignore`, not by size.
- **What an ordinary zip keeps, and what it does not.** It keeps every file's bytes exactly (CRLF and LF untouched),
  every name, the folder tree, empty folders, and modification times to two seconds. It does not keep: Windows
  permissions (restored files take the permissions of the folder they are unpacked into, which on the same PC and
  path is what they had by inheritance); alternate data streams; hard links as links (each comes back as an ordinary
  file; production's records have one link each); or links to other places. If the snapshot meets a link to another
  place (a symbolic link or junction) it fails rather than write something it cannot restore; an environment made by
  `python -m venv` on Windows has none. T017 shows a restored tree runs at the same path.
- **How:** Python's `zipfile`, Deflate at level 9, into `<backup folder>\<name>.zip.partial`. While each file is read
  its SHA-256 goes into a list stored as the last member (`SNAPSHOT_MANIFEST.json`), with the time the copying began,
  the release production holds and the name of that release's recovery kit.
- **Quiet, by three things together** (EX_250 R3-C02):
  1. *Nothing can start.* While `SNAPSHOT_IN_PROGRESS.lock` exists, the production guard refuses every launch.
  2. *Nothing is running, at the start and at the end.* Before the first reading and after the second, the process
     tool lists any Python process that belongs to this production folder (its executable is production's own, or
     its working folder is under `G:\a_p_r_i_r`, or its command line or an ancestor's names that folder), other than
     the snapshot's own chain. This is the rule of design 6.1 without its one clause about the shared base
     interpreter, so that unrelated Python work on the PC (an OUTLANDISH job, a Claude Code task on E:) does not stop
     routine snapshots; every launcher-run program of production is still listed, because the launchers start them
     inside the folder and name it. One new read-only command in the process tool. Any process listed, or one that
     cannot be read: not quiet, no snapshot.
  3. *No file differs.* The second reading below.
- **Verified means two checks, both required.** (1) *The archive:* it is read back and every member's bytes are hashed
  and compared with the list. (2) *The source:* after the archive is complete, every file in production is read and
  hashed **again** and must equal the list, and the set of files must be the same. Only then is the file renamed to
  `<name>.zip` (never over an existing name), its `.sha256` written beside it, a line appended to
  `SNAPSHOT_LOG.jsonl`, and `SNAPSHOT_DUE` removed. A `.partial` file is never a snapshot, and a snapshot that failed
  any check is never called verified.
- **Names.** `PRODUCTION_<YYYYMMDD>_<HHMMSS>_<JOB>.zip`, local time (the UTC time is inside). `<JOB>` is one of
  `WEEKLY_OZLOTTO`, `WEEKLY_POWERBALL`, `DEV_BATCH`, `RESULTS_UPDATE`, `MANUAL`, `INIT_<release>`,
  `PRE_DEPLOY_<release>`, `POST_DEPLOY_<release>`. Every one is a full snapshot; none is a difference from another.
- **Where the code lives:** one module in the release, `src/package_tools/production_snapshot.py` (standard library
  only; it imports no method or evaluator code), started as a child process with production's Python, like the
  process tool.
- **Which commands do it by themselves** (flag before the first write, snapshot at the end):

  | Command | Flag and snapshot |
  |---|---|
  | `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` | automatic, in their sequencers |
  | `Run_Results_Updater.bat update` | automatic, in the launcher: flag, the updater, then the snapshot. The updater's own file is not touched |
  | the deploy tool's `update` | **two:** `PRE_DEPLOY` before anything in production changes, while the old release is whole and quiet; `POST_DEPLOY` after the code, the two records and the environment check are complete and the barriers are gone. Both always attempted |
  | the deploy tool's `init` | one, `INIT`, at the end. There is no earlier G: tree, so there is nothing to snapshot before |
  | `Run_Production_Snapshot.bat` | **a snapshot by hand, at any time, by itself** (the owner's question of 20 November 2026). With `--mark-due` it only sets the flag |
  | single owner commands through the general launchers (`declare-developed`; OV-1's `register` and `stop`; a league `admit` or `repair` typed by hand; a witness line; an old-style walk-forward or report run typed by hand) | **not automatic** (the owner's decision A, entry 112). Their run sheets begin with `Run_Production_Snapshot.bat --mark-due` and end with `Run_Production_Snapshot.bat`. Between the command and that snapshot its change is in no snapshot; the one that matters most is `register`, which cannot be made again if lost (section 9) |
  | `restore`; `export`; `check`; any read-only command | none |

- **`SNAPSHOT_DUE`:** written just before a job's first write (the weekly session: before `open-session`), removed
  only by a verified snapshot. It means "production may have changed since the last verified snapshot". A job that
  finds it tries that snapshot before anything else, whatever kind of job left it and however long ago. A job that was
  refused before it started writes nothing and leaves no flag.
- **If a snapshot cannot be made** (T: unplugged, disk full, not quiet, a check fails), at the start or at the end of
  a job, or before or after an `update`: **every job goes on** (the owner's decision, entry 110, item 3). The flag
  stays. Nothing claims a snapshot was made. A warning in capitals is printed at the start and again as the last lines
  of the job, by every job, until a verified snapshot exists; the job's exit status says so (a new status "complete,
  snapshot not made" when everything else was complete; otherwise the job's own status, with the warning). The live
  path comes first. **For `update` the warning is: NO ROLLBACK POINT WAS CREATED FOR THIS UPDATE,** with the date of
  the last verified snapshot. (An `update` has already stopped if T: itself cannot be reached, because the recovery
  kit is written first, section 4.7; so this case is a snapshot that failed a check, not a missing drive.)
  **The risk the owner accepts, stated plainly:** while the flag stands, the newest rollback point is the last
  verified snapshot; a restore then replays everything since. That costs time, never research validity. It can cost a
  game's formal OV-1 claim if a counted draw's records exist only in the unsnapshotted stretch (section 9).
- **Nothing prunes the backup folder.** The owner deletes old snapshots when he chooses; `check` prints their number
  and total size.
- **Size and time.** With the environment inside, a snapshot has more entries and is larger than v0.2's. No estimate
  is given here; the owner has said storage is not the limit (decision log entry 112), and T017 measures it. More than
  65,535 entries needs the ZIP64 form, which `zipfile` writes by itself (section 14). Whether File Explorer opens it is
  to be shown on the owner's PC, on a tree of the real size. **Fallback if it does not:** several ordinary zips per
  snapshot, each under 65,535 entries, under one manifest. Not designed unless needed.

## 8. Restore (D10; decision log entries 100, 110, 112 and 113; EX_244; EX_248 B01, B02; EX_250 R3-C01, R3-C02)

`restore --snapshot <zip>`, run from an unpacked recovery kit (section 4.7) with whatever Python is installed, on the
owner's own go each time. **It asks nothing of the damaged tree and nothing of E:.** It does not run `check`, does not
use production's Python, reads no file of the E: clone, and does not need any file of the old tree to be readable.

**What it requires (all of these, and nothing else):**

1. The owner's go: the command typed by him, naming the snapshot.
2. The kit's own check (section 4.7), and the snapshot verified in full, every member against its list, before
   anything is touched.
3. **No Python program running on the PC, apart from the restore tool itself** (the owner's decision, entry 113).
   The tool reads Windows' own process table with the standard library and lists every process named `python*.exe`,
   `pythonw*.exe` or `py.exe` outside its own chain. Any one listed, or a table that cannot be read completely, is a
   refusal. It needs no path on G: or E: and no extra package, so it cannot be misled by a damaged tree. It is made
   twice: before the rename, and again straight after it, before anything is unpacked. Nothing is terminated, and no
   acknowledgement stands in for it: the owner closes what is listed, and the restore waits. (Windows' own refusal to
   rename a folder with a file open in it remains as a second barrier.)
4. Only if an orphan marker is found: the condition under "A stale orphan marker" below.

**What it does, in order:**

1. **Looks at the old tree, best effort, for the record only:** locks and barriers left behind; an orphan marker;
   whether each game's weekly folder holds an OV-1 registration. Whatever cannot be read is recorded as "could not be
   read". Nothing found here stops the restore, except the orphan marker's condition.
2. **Renames the old folder** to `G:\a_p_r_i_r_SET_ASIDE_<YYYYMMDD>_<HHMMSS>`: one rename, nothing copied, nothing
   deleted. If the old folder is absent, this step is skipped. If Windows refuses (a file inside is open, or the
   disk is failing), nothing has changed and the tool says what it met. Then the production marker inside the
   set-aside tree, if there is one, is renamed, so no launcher runs there. Then the second process check.
3. **Makes a fresh, empty `G:\a_p_r_i_r`,** writes `RESTORE_IN_PROGRESS.json` in it first, and unpacks **every**
   member, the environment included, hashing each file against the list as it is written. Nothing is merged,
   skipped or rebuilt. An orphan marker inside the snapshot is the one member not unpacked to its place (below).
4. **Writes the restore record** `production_records\RESTORE_<date>_<time>.json` (create-only: the snapshot's name,
   SHA-256 and time; the kit used; the set-aside tree's name; what step 1 found; the times) **and the two restore
   notices** of section 9.
5. **Verifies the whole fresh tree again:** every file against the list, nothing missing and nothing extra, and the
   code against the hash list of its release, which the snapshot itself carries.
6. **Writes the production marker last** and removes `RESTORE_IN_PROGRESS.json`.
7. **A short health check:** it starts the restored environment's own Python once, has it import the third-party
   modules the project uses, and compares the installed distributions with `ENVIRONMENT_VERIFIED.json`. Pass:
   **RESTORED AND READY TO RUN.** Fail: **RESTORED; ENVIRONMENT NOT READY** (the files are all back and verified, but
   this PC's Python is not what it was when the snapshot was taken): the launchers will refuse by themselves, and the
   way forward is the owner's rebuild and `update` (section 6). The tool never says "ready" in that case.
8. No snapshot is taken: the restored tree is the snapshot just read.

**If it stops half-way,** the same command again. A fresh tree still holding `RESTORE_IN_PROGRESS.json` is itself
renamed aside (`..._PARTIAL_RESTORE_...`) and the unpacking starts again. The first set-aside tree is never touched
again by any run.

**The last resort, in the owner's words: "a simple unzip by the human into the right place gets it done".** A
snapshot is an ordinary zip, so with no tool at all the owner can rename the old folder and extract the snapshot to
`G:\a_p_r_i_r` in File Explorer. That skips the process check, the verification, the restore record and the restore
notices. So `HOW_TO_RESTORE.txt` says: first close everything that uses Python; afterwards, as soon as a kit can be
run, `Restore_Production.bat --after-hand-unzip --snapshot <zip>`, which verifies the tree against that snapshot's
list and writes the restore record and the notices (with the time of that moment). Until that is done the formal
OV-1 check of section 9 cannot know a restore happened; ordinary work is unaffected either way.

### A stale orphan marker (EX_248 B02; the owner's decision, entry 110 item 4)

`transitory_data/poc_runs/UNRESOLVED_ORPHAN.json` is the coordinator's record that a process may have been left alive.
It is a different thing from the production marker `PRODUCTION_ROOT.json`, which is identity only and is restored
normally. An orphan marker can be met in two places: in the old tree, and inside the snapshot. Today's rule: any entry
blocks all launches for both games, and only the owner's approved manual clearance procedure clears it. **The smallest
change, proposed for ratification as one added exception** (Architecture 5C is a protected block: it is amended by
ratification, not edited):

> At a restore, a stale orphan marker is set aside as evidence instead of being cleared in place, when all of these
> hold: (a) the tool has shown the marker and a prominent warning that recommends restarting the PC; (b) the PC was
> started after the marker was written; (c) a fresh process check, made after that, is CLEAN; (d) the owner types the
> fixed acknowledgement sentence. No part can be waived, and (d) never stands in for (b) or (c).

- **Why (b), and how it is checked.** A restart ends every process the marker could name. That is a fact the tool can
  check (Windows' start time against the marker's own time, or its file time if the marker cannot be parsed); "I
  closed them" is not. So in this route the recommended restart is also verified. **Why (c) as well:** a restart
  shows the old processes are gone, not that nothing new was started since. Here (c) is the restore's own check: no Python program at all. The start
  time is read from Windows with the standard library.
- **No restart since the marker:** the restore refuses and names the two ways forward: restart the PC, or first clear
  the marker by the existing route, a clearance procedure written and reviewed for that incident (section 1, fact 10).
- **The old tree too damaged to show whether a marker exists:** treated as a marker of unknown time. The tool notes
  the time of this first attempt in the backup folder and asks for a restart; (b) is then judged against that time.
- **Where the bytes go.** The old tree's marker stays where it is, in the set-aside tree, untouched. A marker inside
  the snapshot is unpacked only to `production_records\RESTORE_<date>_<time>_ORPHAN_MARKER.json`. The restore record
  gives each one's SHA-256, the start time that satisfied (b) and the check that satisfied (c). **The fresh tree
  starts with no active orphan marker.**
- **Nothing else about the rule changes.** No chat clears a marker; no tool ends a process; no PID is acted on; and
  outside a restore the existing rule stands as it is.

### After a restore

Ordinary work, each step on its usual go: the updater brings the results forward; the weekly session catches up one
target at a time, each from the draws before it; development jobs, league tables and reports as normal. Every eligible
method and revision is run, impartially; rankings are outputs. This is the same chronological process as before and
valid research (EX_244; EX_248 section 1). Records made in the replay carry their real times and their truthful labels:
a forecast made after its draw is catch-up or development evidence, not prospective. **One plain consequence, stated
so that nobody is surprised:** forecasts that were genuinely made before their draws, after the snapshot, are in the
set-aside tree (and in Git's history if they were exported), not in production; the replayed ones for the same draws
are labelled catch-up. That is truthful labelling. Nothing is merged back, compared (entry 105) or recovered.

**No monthly restore test** (entry 104). T017 rehearses one restore in a scratch folder.

## 9. The formal OV-1 claim after a restore (EX_248 B03)

**Nothing ordinary is at stake** (EX_248 section 1). All eligible methods and revisions run impartially; a restore and
replay are the same chronological process; the ordinary forecasts, scores, rankings and the retrospective OV-1 X, Z,
factors and trajectory are valid research; no rule here guards against choosing methods to suit results, because the
system has no such mechanism. The one question is narrow: what can the restored tree still certify about the claim
labelled "REGISTERED FORMAL PROSPECTIVE OV-1, 2.5% per game", whose ratified rule requires, for every counted draw, a
freeze line and an eligibility line made before that draw's cut-off (supplement v0.8 section 6.8)?

### 9.1 The trace: what the passed code does today

The passed slice 3 tree, run on the invented weekly project of its own tests (section 14). M is the first registered
target. "Restore" means: the project folder renamed aside and an earlier copy put back, the clock left at the real,
later time.

| Case | Before the restore | The restore | What the recorder then appends | What the report's formal view shows |
|---|---|---|---|---|
| (a) nothing lost | M and M+1 counted; M+2 eligible | to the snapshot from the end of that job | Nothing differs: the ledger is byte-identical after the restore; the next week appends FACTOR M+2 and ELIGIBILITY M+3 (counted 3, score 0.979739214220) | RUNNING, as if no restore had happened |
| (b) only a factor line lost | M counted; M+1's factor written by the job that then broke | to the snapshot from the job before (it holds M+1's confirmed eligibility line), before M+2's cut-off | FACTOR M+1 again, 17 of 17 fields equal to the lost line's; then ELIGIBILITY M+2 (counted 2, score 0.988226352101, before and after) | RUNNING, the same figures |
| (c) a counted draw's pre-cut-off records lost | M, M+1 and M+2 counted (score 0.979739214220); M+3 eligible | to the snapshot from before M+2 was frozen, after M+2's cut-off | FACTOR M+1 again; **MISSED M+2** (reason `MISSED_NO_FREEZE`, label `RECORDED_AFTER_THE_CUTOFF_FROM_LOCAL_RECORDS`); ELIGIBILITY M+3 (counted 2, missed 1, score 0.988226352101). `verify` passes | RUNNING, one counted draw fewer and another score, with nothing to say it changed |
| (d) the registration lost | registered; M counted | to a snapshot older than the registration | Nothing: no registration, no ledger; `record` answers NOT_REGISTERED. A second `register` typed before the next session is ACCEPTED (after a session it is refused only because the next draw is already frozen) | "not registered yet" |
| (e) the old tree unreadable | as (c) | as (c) | Exactly as (c): the recorder never reads the old tree | as (c) |

In (c) the replay's ordinary scores for M+2 equal the old tree's for all three invented variants, classed CATCH_UP:
the research is the same. Only the formal bookkeeping moved.

**The code-level reason.** (c): in `ov1.py`, `_due`, when the forecast ledger holds no next-draw freeze line frozen
before C(T) and the clock is past C(T), the recorder calls `reconcile` and appends MISSED. After a restore the tree is
consistent with itself, so `reconcile` passes. The line is truthful about the tree it is in, but the registered
sequence of opportunities has changed, and the missed rule's own stated assumption (no eligible freeze line is removed
after the fact; supplement 6.8) no longer holds, with nothing in the tree to say so. (d): `register` can only check
the tree it is in.

### 9.2 The smallest objective classification

Two times are known in the restored tree without the old one: **S**, when the snapshot's copying began (in its
manifest), and **R**, when the restore finished. C(T) is a fixed instant (01:30 UTC on the draw's date). For a target T:

- **C(T) at or before S:** everything that existed before the cut-off is in the snapshot. Counted or missed, as the
  snapshot shows. Certifiable.
- **C(T) after R:** everything about T is made afresh, before any outcome exists. Certifiable.
- **S before C(T), and C(T) at or before R:** only what the snapshot holds is known.
  - It holds T's freeze line and its confirmed eligibility line: counted; the factor is looked up again in the table
    sealed before the outcome (case b). Certifiable.
  - It holds the freeze line without a confirmed eligibility line: the passed recorder already stops
    (`ELIGIBILITY_NOT_VERIFIED`).
  - **It holds no pre-cut-off freeze line for T:** the tree cannot tell "missed" from "counted, then lost". The honest
    status is **not established from T**. This is the one place where today's code states something it cannot know.

The classification uses three times and the snapshot's contents. No person decides it, no outcome enters it, and the
old tree is not read.

### 9.3 The mechanism (recommended)

1. **A restore notice.** `restore` writes, create-only, in each game's weekly folder,
   `RESTORE_NOTICE_<date>_<time>.json`: S, R, the snapshot's name and SHA-256, and `registration_before_restore`:
   `YES`, `NO` or `COULD_NOT_BE_READ` (whether the old tree's weekly folder held a registration that the snapshot
   lacks; from step 1 of the restore, best effort). For both games, at every restore, registered or not.
2. **One check in the recorder.** Where it is about to append MISSED for T: if a notice has S before C(T) and C(T) at
   or before R, it appends instead a STOP line with the new cause `NOT_ESTABLISHED_AFTER_RESTORE` and the detail
   "FORMAL CLAIM NOT ESTABLISHED FROM DRAW T: production was restored at R from a snapshot of S; whether draw T was
   frozen before its cut-off cannot be verified from this tree". Because targets are taken in order, the stop is at
   the **earliest** such draw, not at whatever target is open when someone notices. Every report then shows it by code
   that has already passed (state STOPPED, the cause, the detail). `verify` applies the same check.
3. **`register` after a lost registration.** With a notice that says `YES` or `COULD_NOT_BE_READ` for the game,
   `register` refuses: "a registration made before the restore of R is not in this tree (or could not be checked);
   there is no second registration (OD-4)". The report's formal view then reads "NOT ESTABLISHED: the registration was
   made before a restore and is not in this tree" instead of "not registered yet". A fresh formal test after that
   would be a new, separately reviewed decision of the owner (EX_219 C1); nothing here provides one.
4. **Nothing else changes.** No existing line is rewritten; no time is altered or invented; the kernel
   (`ov1_numeric.py`) is untouched; cases (a) and (b) behave exactly as traced.

**What never waits and never changes:** forecasting, scoring, the league table and the retrospective OV-1 view. The
weekly sequencer already treats a stopped formal stream as an expected state and goes on (it prints that forecasting,
scoring and the league table continue), and the retrospective view computes X, Z, the factors and the trajectory over
every draw, the replayed ones included, under its descriptive label. The tests show these outputs byte-identical with
and without the new check (section 12).

**Why this is sound, and not a new test.** The change can only stop a stream; it never adds a counted draw, changes a
factor or restarts anything. Stopping cannot raise the chance of ever reaching the bar. Whichever snapshot is restored
and whenever, the counted draws that remain have exactly their original factors (case b). The stop cause becomes part
of the rule each stream is registered under; no stream is registered yet, so none is changed after the event. It is
recorded as a short amendment to supplement 6.8, ratified with the package.

**Its cost.** It is conservative in one way: a draw that was genuinely missed, with its cut-off between S and R, also
reads "not established". And the stretch between S and R is longer whenever snapshots were not made (section 7).

**Alternatives.** (1) The mechanism above: recommended. (2) Leave the recorder alone and let the report print "not
established from draw T" beside a ledger that keeps counting: no edit to slice 2, but two voices about one stream,
and a later crossing would sit in a ledger the report disowns. (3) Do nothing: case (c) shows the silent change.
(4) v0.1's list applied by the owner and Claude after a restore: withdrawn (EX_248 B03: discretionary, and it needed
the old tree).

## 10. The production guard (D5; EX_248 B06)

- **Two different markers.** `PRODUCTION_ROOT.json` says "this folder is production, at this path". It has nothing to
  do with the orphan marker of section 8.
- **The rule.** Every real-data launcher already starts Python once, before the program, to confirm it is running in
  the project's own environment. That pre-check becomes one small reviewed module, `production_guard.py`, which makes
  the same test **and** requires that the marker exists, parses, and records exactly the folder the launcher is in
  (resolved, case ignored). Any failure refuses before the program starts. No extra process per run.
- **Two more things the same pre-check refuses on:** `SNAPSHOT_IN_PROGRESS.lock` present (a snapshot is being taken;
  section 7); `.venv\ENVIRONMENT_VERIFIED.json` missing, or its list not the installed distributions (section 6).
- **The two tools that run without a launcher** (`process_check.py`, `install_records.py`) change real files (locks,
  the two records). They apply the same marker-and-path test to the folder they are given, so they too refuse
  outside production (EX_250 section 4, B06); the tests' invented folders carry an invented marker.
- **Which launchers:** `Run_Experiment.bat`, `Run_Evaluation.bat`, `Run_Method_Rankings.bat`,
  `Run_Results_Updater.bat`, `Run_Weekly_Session.bat`, `Run_Development_Batch.bat`, `Run_Production_Snapshot.bat`.
- **Not guarded, so that safe synthetic work stays where it is:** `Run_Coordinator.bat`, and `Run_Experiment.bat` when
  the file it is asked to run is one of the two proof-of-concept probes the coordinator's own whitelist names
  (`POC_Architecture_Probe.py`, `POC_Coordinator_Probe.py`). They read no draw and write no project record, so the
  owner-run Windows proof-of-concept suite keeps running in the clone. A test pins the two names. **A condition
  recorded now:** if scientific coordination is ever switched on (its switch is False and has its own gate), the
  coordinator's launcher gets the guard in that same package.
- **What it stops:**

  | Folder | Why a real-data launcher refuses there |
  |---|---|
  | the E: clone | no marker |
  | a set-aside tree | its marker was renamed at the restore, and the path differs |
  | a production folder copied by hand to another place | the marker's recorded path is not that place |

- **Limits, stated:** Python typed by hand does not pass through a launcher, as today; the deploy tool and the process
  tool are given their folder explicitly and check it themselves.
- **Alternative:** guard the coordinator path too and move the proof-of-concept suite into a marked folder. Simpler to
  state, but it would forbid safe synthetic work in the clone for no gain today.

## 11. Edits to code that is installed or has passed review

Counted edits, each old text asserted to occur once, with a line-level diff, as for the slices:

| File | Edit |
|---|---|
| `Run_Experiment.bat`, `Run_Evaluation.bat`, `Run_Method_Rankings.bat`, `Run_Results_Updater.bat` (installed); `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` (slice 3) | the production guard, inside the Python pre-check each already makes (section 10). `Run_Experiment.bat`: not for the one proof-of-concept probe. `Run_Results_Updater.bat`: also the flag and the snapshot around `update` (section 7). `Run_Coordinator.bat` is not edited |
| `src/sequencer_children.py` (slice 3) | a `snapshot` child kind; the marker's path check; "overdue snapshot first" and "end-of-job snapshot" in one place |
| `Weekly_Session_Orchestrator.py`, `Development_Batch_Orchestrator.py` (slice 3) | `main` wrapped: guard and overdue snapshot before, snapshot and exit status after; `SNAPSHOT_DUE` written before the first writing child. The sequence itself is untouched |
| `src/package_tools/process_check.py` (installed) | the root test no longer requires `.git` and requires the production marker (section 10); one new read-only command, the quiet check of section 7 (design 6.1's rule without the shared-interpreter clause). `restore` does not use this tool |
| `src/evaluation/ov1.py` (slice 2; the recorder, not the kernel) | reads the restore notices in its own weekly folder; one new stop cause where it would otherwise write MISSED; `register` refuses after a lost registration (section 9) |
| `src/evaluation/consolidated_report.py` (slice 3) | the formal view's wording when a registration was lost (section 9) |
| `src/package_tools/install_records.py` (installed) | the root test likewise (no `.git`; the production marker); `_committed` and `_tracked_changes` replaced by the hash check of section 4.3 step 13 |
| New | `deploy/Deploy_Production.py` and its launcher; `deploy/RELEASE.json`; the kit's `Restore_Production.bat` and `HOW_TO_RESTORE.txt`; `src/package_tools/production_snapshot.py`; `src/package_tools/production_guard.py` (the pre-check); `Run_Production_Snapshot.bat` |

Also in the integrated package, already decided: the removal of the two installed Mode H archive checks (D1).
Not edited: the OV-1 kernel (`ov1_numeric.py`), the forecasting and scoring halves, the league table, the updater.

## 12. Tests the code round must show

- **Each mode, interrupted after every durable step, then run again:** the end state equals an uninterrupted run's
  (the harness slice 3 used for the publication).
- **Identity:** a wrong byte, a missing file and an extra file under `src/` each refuse; a commit whose hash list is not
  the package's digest refuses; an older release refuses; `.bat` bytes are CRLF whatever the clone's settings.
- **`update`:** a `PRE_DEPLOY` and a `POST_DEPLOY` snapshot, each full and each naming the release and its kit; the
  PRE one failing: the update goes on and prints that no rollback point was created; every refusal Appendix J's negative tests list that still applies (a live process, an unreadable one, a
  session lock, a foreign updater lock, an unfinished set for a roster change, P present at the release record); U and
  P left in place by a fault at each step; the release record across midnight.
- **Snapshot:** a round trip gives back every byte and every empty folder; more than 65,535 files; a flipped byte in
  the archive, a file changed, added or removed during the snapshot (a same-size rewrite included), a project
  process listed before or after (not quiet), a launch attempted during the snapshot (refused), a link to another
  place in the tree, a full or
  missing backup folder each leave no snapshot and leave the flag; an existing name is never overwritten; the overdue
  snapshot is tried first; when it cannot be made the job still runs, warns at its start and end, and exits with the
  stated status; the updater's launcher takes one after `update` and none after a read-only command.
- **The kit:** built from a commit's bytes whatever the working files hold; a changed, missing or extra file in an
  unpacked kit, and a zip that is not its `.sha256`, each refuse; `update` and `init` stop before touching production
  when the kit cannot be written.
- **Restore:** run from an unpacked kit by a bare Python with no third-party package, with no E: clone present, onto
  an invented production tree with an environment in it; the set-aside tree is byte-identical to the tree before,
  apart from its renamed marker; the fresh tree equals the snapshot file for file, environment included, with nothing
  extra; with the old tree absent, half missing, without a `.venv`, with an unreadable OV-1 ledger: the restore
  completes; any Python process in a stand-in process table refuses, an unreadable table refuses, and no
  acknowledgement overrides either; a process appearing between the two checks stops it after the rename with
  nothing unpacked; extraction stopped half-way, then the command again; the health check READY, and NOT READY when
  the environment cannot start (never "ready"); `--after-hand-unzip` on a tree unzipped by hand.
- **The environment:** a rebuilt `.venv` and an upgrade in place each make every real-data launcher refuse until
  `update` has verified it; a failing suite writes no `ENVIRONMENT_VERIFIED.json`.
- **The orphan marker at a restore:** in the old tree and in the snapshot; restart shown, clean check and the typed
  sentence: the restore proceeds, the fresh tree has no active marker, the evidence bytes are kept; no restart shown:
  refused; a wrong or missing sentence: refused; a marker written after the last restart: refused.
- **Formal OV-1 after a restore** (the five cases of section 9, on the invented weekly project): (a) and (b)
  unchanged ledgers and equal factors; (c) the new stop at the earliest unverifiable draw, never a MISSED line, with
  forecasting, scoring, the league table and the retrospective view identical to a run without the check; a draw
  whose cut-off is before the snapshot or after the restore still becomes MISSED as today; (d) the report's wording
  and `register` refusing; (e) the same as (c) with the old tree deleted. One planted defect per rule.
- **Labels after a restore** (EX_248 section 3): an original release record brought back by `update`; a replayed
  forecast for a draw after that release date is CATCH-UP, never PROSPECTIVE; revisions are not pooled.
- **The production guard:** the clone (no marker), a renamed-aside tree and a hand-copied marked folder each refuse
  every real-data launcher; the proof-of-concept probe still starts in the clone.
- **`export`:** new, grown and identical files; a changed create-only record refuses and writes nothing at all (the
  plan is complete before the first write); the two exempt kinds; an uncommitted change in the clone refuses;
  `--after-restore` refused without a new restore record; the worked example of section 4.4 end to end: afterwards
  the clone's active folders equal production's tracked records file for file, every earlier file is under the dated
  folder with its bytes, and an interruption at each step followed by the command again gives the same result;
  production's bytes never change.
- **Static:** the snapshot module and the deploy tool contain no terminate, kill or signal call and import no method or
  evaluator code; nothing in the release set starts `git`, other than the two historical places named in section 1.
- One Python 3.15 build in the cloud (entry 103); planted defects for each rule above.

## 13. What T017 rehearses (one task file, its own go, a reviewed rulebook allowance)

In scratch folders only, on invented masters and records, through the real launchers: `check` and `init` from a task
clone into a scratch production folder (its environment built by the owner with his two scripts: the runner never
runs `pip`); a launcher refusing in the clone and
running in the scratch folder; weekly sessions and a development batch, each ending in a snapshot; one snapshot
of a tree of the real size, environment included, opened in **File Explorer by the owner** (the only step the runner cannot do) and its size and time recorded; an
`update` with a fault planted and the command typed again; an overdue snapshot taken first, and a job that goes
on with the warning when the backup folder is missing; one `restore`, with a stale orphan marker and a restart of the
PC by the owner, run from an unpacked recovery kit with the task clone out of reach, the restored environment running at the same
path with nothing installed, then a catch-up over the lost draws and the formal view's "not established" line; an
environment rebuilt with the owner's two scripts, refused by a launcher until `update` verifies it; the restore's
process table and start time read on Windows; an `export` and what it prints; records made in one folder read in another (the open
check of section 1); the whole suite before and after, as the owner decided on 13 November 2026. No step changes the
PC's date, time or zone; nothing is terminated; no real data is read or written.

## 14. The probe and the trace (invented files; cloud, Linux)

`zip_probe.py` beside this note, output in `zip_probe_output.txt`: 81,500 invented JSON files, 215 MB, zipped by
`zipfile` (Deflate, level 9) on Python 3.15.0b4: the ZIP64 end records are written without being asked for; 81,502
entries; the read-back check found 0 mismatches; an empty folder came back; the extracted tree equalled the list.
About 9 seconds to write, 3 to check, 5 to extract. The archive was 140 MB, but the invented content is mostly random
digits and compresses poorly; real records should do better. None of this says anything about the owner's drives or
File Explorer.

**The trace** (`restore_ov1_trace.py`, output in `restore_ov1_trace_output.txt`): the passed slice 3 tree, built from
the repository copy (tree digest `ef2b67e0...1f50e9d13`), on the invented weekly project of the slice's own tests,
Python 3.15.0b4. A "restore" there is: the invented project folder renamed aside and an earlier copy put in its
place, with the clock left at the real later time. Section 9 quotes its five cases. It is a trace of existing code on
invented data: not a test, not a result, and it changes no file of the slices.

## 15. The owner's choices: all confirmed

Nothing in this draft waits on a choice. For the ratification, in one place (decision log entries 110, 112, 113):

| # | Decided | Where |
|---|---|---|
| 1 | Every snapshot is the complete `G:\a_p_r_i_r`, `.venv` included; only the two control files are left out (replaces the earlier "no `.venv`") | 7 |
| 2 | Restore is plain: verify, rename the old tree aside, unpack everything at the same path, verify; nothing rebuilt | 8 |
| 3 | `update` takes a snapshot before and after; `init` takes one at its end; ordinary end-of-job snapshots stay | 4.3, 7 |
| 4 | A recovery kit zip on T: for each release; an emergency restore needs neither E: nor a working production folder | 4.7, 8 |
| 5 | The owner copies the whole T: backup folder to USB3 drives and the cloud himself | 2 |
| 6 | `SNAPSHOT_DUE` is written just before a job's first write | 7 |
| 7 | When a snapshot cannot be made, all jobs go on with a standing warning; the risk is accepted | 7 |
| 8 | `restore` is a fifth mode of the one tool | 4 |
| 9 | Production `G:\a_p_r_i_r`; backups `T:\a_p_r_i_r_backups` | 2 |
| A | Single owner commands: the run sheet marks the snapshot as due first and ends with the snapshot command | 7 |
| B | A stale orphan marker at a restore: a checked restart, a clean process check, the typed acknowledgement; otherwise the existing per-incident clearance | 8 |
| C | Formal OV-1: the one objective check in the recorder; `register` refuses after a lost registration | 9 |
| D | Only the two named proof-of-concept probes stay unguarded; the guard checks the path | 10 |
| E | The early File Explorer check: yes, **on its own go, not yet given** | 14 |
| F | `update` and `init` stop if the recovery kit cannot be written to T: | 4.7 |
| G | An emergency restore runs on whatever Python is installed for the user | 4.7, 8 |
| H | Production's environment is built the owner's way and verified by the suite before use (H1) | 6 |
| - | For a restore: no Python program at all may be running on the PC | 8 |
| - | A snapshot by hand at any time; and, as the last resort, an unzip by hand | 7, 8 |

**Two small things I added that you have not been asked about; say if either is unwelcome.** (1) The file
`.venv\ENVIRONMENT_VERIFIED.json`, so that a launcher refuses on an environment that was rebuilt or upgraded and not
yet verified (section 6). (2) `Restore_Production.bat --after-hand-unzip`, so that a restore done by hand still gets
its restore record and notices (section 8).

**Still needing your word, later:** the ratification of this note after the reviewer's recheck; the go for E; and the
amendment to the orphan-marker rule (section 8's boxed text), which is part of what the ratification covers.

## 16. Documents to amend with the integrated package (each reviewed and ratified in the ordinary way)

- **Design v0.1r7 Appendix J:** the development-clone part (the verifier's PRE, POST, suite, COMMITTED, push) and the
  production part (`update`, section 4.3), with the table of section 5. Sections 4.3 (where and when the two records
  are written), 6.1 (the launchers' production guard; the snapshot at a session's end) and 7 (the checklist).
- **Direction document v0.3r1 section 9:** the backup paragraph replaced by D7 to D10, full snapshots, the recovery kit
  and the restore method; no
  monthly restore test; and one sentence that settles the wording difference between EX_243 ("OFF-1 read strictly")
  and H-2 v3r6 ("a new, stricter owner rule"): proposed, "The owner decided on 18 November 2026 that production holds
  no Git at all; this goes further than OFF-1's words and is binding."
- **Design 6.1** (the process rule): the quiet check of section 7 and the restore's own rule of section 8, each named
  beside the existing rule, which is not changed.
- **Supplement v0.8 section 6.8** (and code plan v0.3 L5): the restore notice; one more stop cause; `register` after a
  lost registration (section 9). **The orphan-marker rule** (Architecture 5C, a protected block, amended by
  ratification and not edited; H-1 5.4): the one added exception of section 8.
- **Architecture** (the launch interfaces: the production guard in the pre-check, the new launcher); **code plan v0.3 section 10** (T017 and
  the install); **the runner's rulebook v0.6** and the owner's deny lines for the new programs; **the owner's
  checklist**; register v0.32; the next H-1.

## 17. Not designed here, uncertainties, and what could be wrong

- The run sheet for an environment change (section 6): written and reviewed with the package.
- The run sheets for the first deployment, `declare-developed` and the registrations.
- The multi-zip fallback, unless File Explorer needs it.
- **Not shown anywhere yet (T017):** reading Windows' process table and start time with the standard library; an
  environment restored from a zip running at the same path; File Explorer on an archive of the real size; the time a
  full snapshot takes with the environment inside.
- **The quiet check narrows an always-review rule** for snapshots only (it drops the shared-interpreter clause). I
  believe every launcher-run program is still listed; the reviewer should judge that, and the alternative is to keep
  the full rule and accept that an unrelated Python job on the PC stops routine snapshots.
- **Section 9's check is conservative in one way:** a draw that was genuinely missed, whose cut-off lies between the
  snapshot and the restore, also reads "not established", because the restored tree cannot tell the two apart.
- **A point for the reviewer's judgement (labels):** after a restore to a snapshot older than an update, `update`
  brings back the original install and release records with their original dates (section 4.3). So a replayed
  catch-up forecast by that variant, for a draw after its original release date, is labelled CATCH-UP as it would
  have been. I think that is truthful (the variant was released then, and the record is the original, not a new one),
  and it manufactures no standing; say if you read design 4.3 differently.
- I have not traced every reader of old records for a stored absolute path (section 1). If one exists, `init`'s copy
  to G: would expose it; the fix would be in that reader, shown in T017.
- The process rule's false positive (section 4.6) will be met more often now that two environments share one Python.
  I recommend living with it rather than touching an always-review rule.
- The exempt list of `export` (two kinds) is from a search of the staged tree for in-place replacement; a future
  record kind replaced in place would be refused by `export` until added. That fails safe.
- Size: about a small slice (one tool, two small modules, counted edits to thirteen files, their tests).

## 18. Where each finding of EX_248 and EX_250 landed

| Finding | The scenario, in one line | The correction | Where |
|---|---|---|---|
| B01 emergency restore | Production is restored because its tree, environment or records are damaged, so it cannot pass a healthy-production check | `restore` has its own four requirements and never runs `check`, never uses production's Python and never needs the old tree readable; the old tree absent, half missing or unreadable is handled; a stop half-way is finished by the same command | 4.1, 8 |
| B02 the orphan marker | A marker left by a crash would block the very restore the crash calls for; copied back, it would block the fresh tree | One added exception to the owner-only rule: restart shown, fresh clean process check, typed acknowledgement; the bytes kept as evidence; never an active marker in the fresh tree; never an override of a running or uncertain process | 8, 16 |
| B03 formal OV-1 | The staged recorder turns a formerly counted draw into MISSED after a restore, and accepts a second registration | Traced on the passed code (five cases); an objective classification from three times and the snapshot's contents; one new stop cause at the earliest unverifiable draw; `register` refuses after a lost registration; v0.1's list applied by people withdrawn | 9, 14 |
| B04 export after a restore | The clone's active folders could mix production's restored state with later records | Every export is planned before it writes; after a restore, changed and clone-only files are moved to one dated folder and the active folders become exactly production's; a worked example; the tests | 4.4, 12 |
| B05 snapshots | Which commands snapshot; a coherent single state; the old release's own lock and wheels; the changed choice on an overdue snapshot | A table of commands, the updater's launcher included; a second reading of the source; each release's lock kept in production and so in every snapshot, wheels of every lock kept, and no "restored" before the environment is verified; all jobs go on with a standing warning, the risk stated | 6, 7 |
| B06 the guard | A hand-copied production folder carries the marker and would run | The path is checked at every real-data launch, inside the pre-check each launcher already makes; the proof-of-concept probes stay unguarded so safe synthetic work stays in the clone | 10 |
| Section 3, labels | A replayed forecast for a draw after an original release date | CATCH-UP, never PROSPECTIVE; revisions never pooled; a fixture | 4.3, 12 |
| EX_250 R3-C01 the E: dependency | The restore needed the E: clone's tool and Python at the moment E: may be broken; the process tool reads the damaged tree's `pyvenv.cfg` | A recovery kit zip per release on T:, built from release bytes, self-checking, standard library only; `restore` runs from it on any installed Python; its process check is "no Python program at all", read from Windows' process table, made before and after the rename | 4.7, 8 |
| EX_250 R3-C02 full-tree snapshots | `.venv` was left out and rebuilt; one snapshot around a deployment; a double scan alone as the quiet proof | Everything under the root, `.venv` included; what a zip keeps and does not; quiet by three things (no launch during a snapshot, a process check before and after, the second reading); `PRE_DEPLOY` and `POST_DEPLOY`; a plain same-path restore with a health check and no false "ready" | 6, 7, 8 |
| EX_250 section 1, the environment | Rebuilt from pinned wheels at every restore | Withdrawn. Built the owner's way (H1), verified by the suite before any launcher runs, and carried in every snapshot | 6 |
| EX_250 section 4, B06 note | Direct commands that change real files | The two tools run without a launcher apply the same marker-and-path test | 10 |

Unchanged in substance since v0.2, and accepted in principle in EX_250: sections 4.4 (export), 9 (formal OV-1) and the
orphan-marker rule of section 8. B05's wheel-and-lock part is superseded by section 6.

*End of the draft.*
