# MHUP-B deployment design note - DRAFT v0.2

**Status:** DRAFT v0.2 for the reviewer's R-3 RECHECK. Not ratified. It authorises nothing. It answers EX_248 (RECHECK;
findings B01 to B06) and carries the nine choices the owner confirmed on 20 November 2026 (decision log entry 110).
Section 18 says where each finding landed. v0.1 (sent as EX_247) is kept beside it; `NOTE_v0_1_TO_v0_2.diff` is exact.
**Written:** 20 November 2026, 02:46 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's
go of 19 November 2026, 23:50 (decision log entry 107) and his go for this revision (entry 110). Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH (it replaces part of a ratified install procedure, design Appendix J; it touches gates, installs
and the formal OV-1 claim). **Base:** `main` at `9350196`; staged slices as passed (EX_231, EX_237, EX_242).

## Work-item card

| Item | |
|---|---|
| Work item | MHUP-B deployment layer: design note |
| Binds it | Owner decisions D1 to D12 (EX_243; decision log 92 to 98); EX_244 (restore and replay; governs); decision log 100 (how a restore is done), 103 (Python 3.15 only), 104 (no monthly restore test), 105 (no replay comparison), 107 (the go), 110 (the nine confirmed choices; EX_248 section 1, the owner's scientific clarification); H-1 v7r1 section 12.11 (the checklist); the working principle of 18 November 2026 |
| Replaces | The Git-based steps of design v0.1r7 Appendix J, for production; the backup paragraph of the direction document v0.3r1 section 9 |
| Not in scope | Any code, package, task file, Windows step, install, restore or run. Slices 1 to 3 are not reopened |
| Evidence state | DESIGNED. Nothing implemented or tested, except a probe and a trace on invented files (section 14) |

## 0. The whole thing in plain English

1. **Two folders.** Development stays in the Git clone on E:. Production is a plain folder on G: with no Git in it. It
   holds the code, the data and records, its own Python environment, and a small folder of deployment records.
2. **One tool, kept in the development clone, never copied to production.** It has five modes: `check` (look, change
   nothing), `init` (make production the first time), `update` (bring in a new reviewed release), `export` (copy
   records back to the clone so they can be committed and pushed) and `restore` (your method: rename the old tree
   aside, unpack a snapshot into a fresh tree). Every mode can be run again after a fault and picks up where it was.
3. **A release is a named commit of `main`, proved by file hashes.** The reviewed package states the hash list's
   digest; the tool recomputes it from the commit and refuses if they differ; production's files are then checked
   against the same list. Git is used only on the E: side.
4. **`update` keeps Appendix J's safety, without Git:** the same process check, the same two barriers (the updater's
   lock and the install-in-progress file), the test suite before release, the same install and release records with
   the same meaning. What Git used to prove ("committed and clean") is proved by hashing every file instead.
5. **A snapshot is one ordinary `.zip`** of the whole production folder except its Python environment, written by
   Python's own `zipfile`, checked twice before it counts (the archive read back; the files read again), named with
   the date and time, in `T:\a_p_r_i_r_backups`. Every production job ends with one. A "snapshot due" file, written
   before a job's first write, makes the next job take a missed one first. If it cannot be made (T: missing), every
   job goes on with a loud warning that stays until one is made: your decision, with its risk stated in section 7.
6. **Restore** works even when production is damaged: it needs only a verified snapshot, a clean process check and
   your go. It renames the old tree aside (kept), unpacks the snapshot into a fresh tree at `G:\a_p_r_i_r`, rebuilds
   the Python environment from that release's own locked wheels and writes a restore record. After that you work
   normally: the updater, then the weekly session, replay the missing draws one at a time from the draws before each.
   That is the same chronological process and valid research (EX_244; EX_248 section 1). Nothing is compared with the
   old tree, no timestamp proof is asked for, nothing stops.
7. **The formal OV-1 claim is kept apart, with no human choice.** A trace of the passed code (section 9) shows the one
   thing a restore changes: a draw that was counted before the restore can come back as "missed". The fix is one
   objective check in the recorder, fed by a small restore notice: such a draw makes the *registered formal claim*
   read "not established from draw T". Forecasting, scoring, league tables and the descriptive OV-1 view never wait
   for it and are never changed by it.
8. **A marker file** at the production root, checked with its path at every real-data launch, so nothing real starts
   in the E: clone or in a copied or set-aside folder. The proof-of-concept suite still runs where it does today.
9. **A stale orphan marker never blocks a restore for ever and is never copied back as a live block:** restart the PC
   (recommended and checked), a fresh clean process check, and your typed acknowledgement (section 8).

The nine choices you confirmed are recorded in section 15, with five smaller ones still yours.

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

## 2. The production folder

    G:\a_p_r_i_r\                    (the owner's choice; backups in T:\a_p_r_i_r_backups\)
      PRODUCTION_ROOT.json           the marker: schema, this folder's absolute path, the time it was made, the
                                     release it was made from. Written once, last, by init or restore.
      PRODUCTION_SETTINGS.json       the owner's settings: the backup folder, the wheel folder (section 6).
                                     Plain JSON the owner may edit.
      Run_*.bat                      the launchers (release)
      src\                           the code (release), with the install records and the barrier P where they are today
      source_data\  results\  transitory_data\      data and records, exactly as on E: today
      production_records\            written only by the deploy tool and the snapshot code:
                                     RELEASE_<commit>.json (the hash list of each release deployed; create-only),
                                     DEPLOYMENT_LOG.jsonl (its last line names the current release),
                                     LOCK_<digest>.txt (the Python lock of each release deployed; section 6),
                                     SNAPSHOT_LOG.jsonl, INIT_RECORD.json, RESTORE_<date>_<time>.json (and, beside
                                     it, the bytes of any orphan marker a restore set aside as evidence),
                                     and two working files that are never put in a snapshot: SNAPSHOT_DUE and
                                     SNAPSHOT_IN_PROGRESS.lock
      .venv\                         production's own Python environment (not in snapshots; section 6)

Not in production: `.git`, `tests/`, `doc/`, `exchange/`, `review/`, `archive/`, `GAIS/`, the runner's folder, the
venv helper `.bat` files and the dependency installer. No installed program reads any of them (CODE-3's static rule
already forbids `src/` to refer to `archive/`).

**Alternative considered:** putting the settings in the marker (one file). Rejected: the marker is identity and is
never edited; the backup folder is a setting the owner may change (D9).

## 3. The release, and how production is proved equal to it

- **The release set** is every file Git tracks under `src/` at the release commit, plus every tracked root file named
  `Run_*.bat` (today 487 and 5). Bytes: the commit's own stored bytes, except that `.bat` files are written with CRLF,
  as `.gitattributes` requires. The tool reads them from Git's objects, never from working files, so the clone's mix
  of LF and CRLF working files and any uncommitted edit cannot reach production.
- **The release description** is one small reviewed file in the package, `deploy/RELEASE.json`, outside the release
  set: the package name; the fields `process_check.py` and `install_records.py` already read from a package manifest
  (`release_entries`, `retires`, `registry_entries_added`); the expected digest of the release hash list; the name and
  digest of the Python lock file (section 6).
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
starts three kinds of child process: `git` (on the E: side only), `pip` (section 6) and the project's own reviewed
tools. It is reviewed code, installed into `main` by the package, and is not part of the release set. Every mode names
the production folder explicitly (`--production G:\...`).

**The process check** is always the reviewed `process_check.py`, verified by hash before it is run: with production's
Python when production's environment exists and is verified, otherwise with the development environment's.

**Re-running.** Each mode is a list of small durable steps. Each step first looks at what is already there: finished
(skip it), or half done by the same run (finish it), or something this run did not make (stop and say what). So the
same command typed again after a power cut, a full disk or a refusal goes on from where it stopped, and typed again
after success changes nothing. The tests plant a fault after every step and run the command again (section 12).

### 4.1 `check` (reads only; safe at any time)

It prints, and changes nothing: the clone's commit and the release description; production's recorded release;
whether every production file equals its release (all hashed); unexpected or missing files; the marker and settings;
the environment against the lock; locks and barriers present; whether the orphan marker exists; `SNAPSHOT_DUE`; the
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
2. Create the folder. Copy `source_data/`, `results/` and `transitory_data/` whole, the git-ignored run folders
   included, each file hashed on both sides; the list is kept as `INIT_RECORD.json`. Nothing on E: is changed.
3. From here it is `update`'s steps 4 to 13 into an empty code tree: the barriers, the code, the check against the
   hash list, the environment, the suite, the install record, the release record (MHUP-B's has an empty entry list:
   no roster change).
4. Write the settings, then the marker, **last**: until the whole of `init` has passed, no launcher runs there.
5. Take the first snapshot.

After `init` the E: clone still holds its old copies of the data. They are left alone (nothing is deleted); the
production guard (section 10) keeps real-data jobs from running there; `export` keeps the tracked ones current.

### 4.3 `update` (a new reviewed release into production)

| Step | What happens | Appendix J step it keeps or replaces |
|---|---|---|
| 1 | `check`: production equals its recorded release (no drift); the named commit's hash list equals the package's expected digest; the new release descends from the deployed one (an older one is refused: going back is a restore) | 0, 1 (PRE; "replaced files at base bytes") |
| 2 | The install check: no project process; no session lock; no updater lock; for a roster-changing package, no unfinished weekly set | 2 (unchanged rule) |
| 3 | If `SNAPSHOT_DUE` exists: the overdue snapshot first (section 7) | new (D8) |
| 4 | Take the updater's lock U (`take-install-lock`); write `SNAPSHOT_DUE` | 3 |
| 5 | Create the barrier P; the install check again | 4, 5 |
| 6 | Copy the changed and new release files (each to a temporary name, then replaced); remove only files that the old hash list held and the new one does not | 6, 8. One copy, not two: Appendix J copied the gate files first because MHUP-A's old gate did not know P; the installed gate has honoured P since MHUP-A |
| 7 | The install check after the copy | 7 |
| 8 | Every production file against the new hash list; nothing unexpected under `src/` | 9 (POST) |
| 9 | The environment: built or rebuilt only if the lock changed, then verified (section 6) | new (D6) |
| 10 | The suite, in a temporary export of the whole release commit (so the tests find the repository files they read), run with **production's** Python; the temporary folder is then removed, and one that cannot be removed is a STOP. Production gains no file | 10 (J-1's shadow run; the barriers stay in production throughout) |
| 11 | The install check; the install record (the installed tool; P must be present, as now) | 11, 12 |
| 12 | Production against the hash list once more, with the install record; a line in `DEPLOYMENT_LOG.jsonl` | 13 (COMMITTED), replaced: see section 5 |
| 13 | The install check; remove P; the release record (it refuses while P exists, without U held by this package, with a session lock, or, for a roster change, with an unfinished weekly set: all as now; its two Git tests are replaced by "production equals its hash list and the install record validates"); validate the records; release U **last** | 14 to 18 |
| 14 | The end-of-job snapshot, verified; `SNAPSHOT_DUE` removed. Then the owner runs `export` and commits the two records in the clone | new (D8); 17, 19 (the two commits and the push become one export and one commit) |

A STOP at any step leaves U and P in place (fail closed) and prints what to send. Nothing is terminated by any tool.
Typing the same command again continues when the state is this update's own; otherwise it stops. An update that cannot
be completed is abandoned by restoring the last verified snapshot (D10), on the owner's go, with steps written for
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

While `update`, `restore`, `init` or a session resume runs its process check: no Claude Code task and no other Python
job started from the same Python installation (fact 4). An ordinary weekly session with no leftover lock does not run
that check.

## 5. Appendix J's safety properties: kept, or consciously replaced

| Property (H-1 v7r1 12.11 checklist) | Here |
|---|---|
| 1. Code identity | Kept, stronger: every file hashed against a reviewed digest (section 3). **Replaced:** `git status` clean, `git pull`, the committed-at-HEAD test |
| 2. No evidence overwritten | Kept: `update` writes only release files under `src/`, the root launchers and `production_records/`; under `source_data/`, `results/` and `transitory_data/` it writes nothing except taking and releasing the updater's lock; the orphan marker is never touched |
| 3. The install check and the barriers U and P | Kept unchanged (the installed tools). E is E_1's alone and is not used |
| 4. No roster change under an unfinished weekly set | Kept unchanged (install check and release-record tool) |
| 5. The meaning of the install and release records | Kept: code arrival after POST and the suite; the release date is the local date of the step that writes the record; never while P or a session lock exists. **Replaced:** the two Git tests, by the hash check of step 13 |
| 6. The suite before release; the restore rule on a STOP | Kept: step 10 with production's Python. **Replaced:** `git checkout --` and `git revert` as the way back, by restoring the last verified snapshot (D10) |
| 7. A reproducible environment | New, section 6 |
| 8. `export` one way and non-destructive | Section 4.4 |
| 9. The production guard; every mode re-runnable | Sections 10 and 4 |
| 10. The snapshot | Section 7 |
| Appendix J's two stated residual risks (D3: three programs no barrier stops; a run straddling the gate copy) | Smaller: with the production guard every real-data launcher refuses outside production, and P is in place before any file changes. A project program started by hand between two checks remains the stated residual |

## 6. Production's Python environment (D6)

- **Made fresh**, never copied: `python -m venv` from the same base installation the development environment uses,
  then `pip install --no-index --find-links <wheel folder> --require-hashes -r <lock file>`. No network.
- **The lock file** (`deploy/PRODUCTION_REQUIREMENTS_LOCK.txt`, reviewed, in the clone) pins the exact version and
  SHA-256 of every wheel. It lists only what the installed code imports and what those need (fact 7), at the versions
  of the development environment the suite passed on. Other work's packages stay out, so they can no longer change
  production's environment.
- **Each release has its own lock.** `update` and `init` copy the release's lock file into
  `production_records/LOCK_<digest>.txt`, so **every snapshot carries the exact lock of the release it holds**.
- **The wheel folder** (recommended: `T:\a_p_r_i_r_backups\wheels`, a setting) holds the wheel files of every lock
  ever deployed. Nothing prunes it. It is not evidence (every wheel is hash-checked against the lock when installed),
  so it lives outside Git and outside the snapshots.
- **A restore rebuilds the environment from the snapshot's own lock,** not from whatever lock is newest on E:. If a
  wheel that lock names is missing or has another hash, the tool lists exactly which, writes no marker (so nothing
  runs in the fresh tree) and reports RESTORE NOT COMPLETE: ENVIRONMENT NOT BUILT. The owner puts the wheels back (the
  same pinned versions fetched again, on a dependency go; they are hash-checked) and types the command again. An old
  lock also needs the Python version it was made for; the tool says so if the base Python no longer matches.
- **Making the lock and the wheel folder** needs the internet once per dependency change (`pip download`). It is a
  dependency step: its own short reviewed procedure and its own owner go, as D6 says. Not designed further here.
- **Verified after every build:** the installed distributions equal the lock; the existing environment inventory
  refuses an orphan file; the digest goes into the deployment log. Step 10 then runs the suite with this environment.
- **A changed base Python** (say 3.15.3) changes both environments. The existing rule holds: stop until the suite
  passes; here, an `update` run rebuilds and re-verifies.

## 7. Snapshots (D7 to D9)

- **What is in one:** every file and every empty folder under the production root, except `.venv\` and the two
  working files `SNAPSHOT_DUE` and `SNAPSHOT_IN_PROGRESS.lock`. That includes the git-ignored run folders, the ledgers,
  the registries and release records, the sealed Mode H archive, `production_records\`, the marker and settings, and
  any lock or orphan marker present at that moment, as they are.
- **How:** Python's `zipfile`, Deflate at level 9, into `<backup folder>\<name>.zip.partial`. While each file is read
  its SHA-256 goes into a list stored as the last member (`SNAPSHOT_MANIFEST.json`), with the time the copying began.
- **Verified means two checks, both required.** (1) *The archive:* it is read back and every member's bytes are hashed
  and compared with the list. (2) *The source:* after the archive is complete, every file in production is read and
  hashed **again** and must equal the list, and the set of files must be the same. Production's records are created,
  grow, or are replaced by newer ones; none returns to earlier bytes. So files equal at both readings were the same
  in between: the snapshot is one state, the state at the moment between the two readings. A file that changed, appeared or vanished fails the snapshot. Only
  then is the file renamed to `<name>.zip` (never over an existing name), a line appended to `SNAPSHOT_LOG.jsonl`, and
  `SNAPSHOT_DUE` removed. A `.partial` file is never a snapshot. A lock file stops two snapshots running at once.
- **Name:** `PRODUCTION_<YYYYMMDD>_<HHMMSS>_<JOB>.zip`, local time, for example `..._WEEKLY_OZLOTTO.zip`; the UTC time is
  inside.
- **Where the code lives:** one module in the release, `src/package_tools/production_snapshot.py` (standard library
  only; it imports no method or evaluator code), started as a child process with production's Python, like the
  process tool. A launcher `Run_Production_Snapshot.bat` lets the owner take one by hand.
- **Which commands do it by themselves** (flag before the first write, snapshot at the end):

  | Command | Flag and snapshot |
  |---|---|
  | `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` | automatic, in their sequencers |
  | `Run_Results_Updater.bat update` | automatic, in the launcher: flag, the updater, then the snapshot. The updater's own file is not touched. So the first backup after a results update exists even if no weekly session follows |
  | the deploy tool's `init` and `update` | automatic |
  | `Run_Production_Snapshot.bat` | the snapshot, by hand, at any time |
  | single owner commands through the general launchers (`declare-developed`; OV-1's `register` and `stop`; a league `admit` or `repair` typed by hand; a witness line; an old-style walk-forward or report run typed by hand) | **not automatic.** Their run sheets end with `Run_Production_Snapshot.bat`. Until then their change is in no snapshot. This is an exception for the owner's explicit acceptance (section 15, item A) |
  | `restore`; `export`; `check`; any read-only command | none (nothing in production changes, or the tree is the snapshot just read) |

- **`SNAPSHOT_DUE`:** written just before a job's first write (the weekly session: before `open-session`), removed
  only by a verified snapshot. It means "production may have changed since the last verified snapshot". A job that
  finds it tries that snapshot before anything else, whatever kind of job left it and however long ago. A job that was
  refused before it started writes nothing and leaves no flag.
- **If a snapshot cannot be made** (T: unplugged, disk full, a check fails), at the start or at the end of a job:
  **every job goes on** (the owner's decision, entry 110, item 3). The flag stays. Nothing claims a snapshot was made.
  A warning in capitals is printed at the start and again as the last lines of the job, by every job, until a
  verified snapshot exists; the job's exit status says so (a new status "complete, snapshot not made" when everything
  else was complete; otherwise the job's own status, with the warning). The live path comes first.
  **The risk the owner accepts, stated plainly:** while the flag stands, the newest rollback point is the last
  verified snapshot; a restore then replays everything since. That costs time, never research validity. It can cost a
  game's formal OV-1 claim if a counted draw's records exist only in the unsnapshotted stretch (section 9). The
  exposure is largest before `update`, which changes the code with no fresh snapshot of the old state; `update` prints
  that sentence and the date of the last verified snapshot before it goes on.
- **Nothing prunes the backup folder.** The owner deletes old snapshots when he chooses; `check` prints their number
  and total size.
- **More than 65,535 entries** needs the ZIP64 form, which `zipfile` writes by itself (section 14). Whether File
  Explorer opens it is to be shown on the owner's PC. **Fallback if it does not:** several ordinary zips per snapshot,
  each under 65,535 entries, under one manifest. Not designed unless needed.

## 8. Restore (D10; decision log entries 100 and 110; EX_244; EX_248 B01 and B02)

`restore --snapshot <zip>`, on the owner's own go each time. **It asks nothing of the damaged tree.** It does not run
`check`, does not use production's Python, and does not need any file of the old tree to be readable.

**What it requires (all of these, and nothing else):**

1. The owner's go: the command typed by him, naming the snapshot.
2. The snapshot verified in full, every member against its list, before anything is touched.
3. Process safety, checked independently of production: the reviewed process tool, from the clone's hash-verified
   copy, run with the development environment's Python, applied to the production path whether or not the folder is
   whole. Any project Python process, or one whose details cannot be read, is a refusal. Nothing is terminated, and no
   acknowledgement overrides it: an uncertain process is treated as alive and the restore waits.
4. Only if an orphan marker is found: the condition under "A stale orphan marker" below.

**What it does, in order:**

1. **Looks at the old tree, best effort, for the record only:** locks and barriers left behind; an orphan marker;
   whether each game's weekly folder holds an OV-1 registration. Whatever cannot be read is recorded as "could not be
   read". Nothing found here stops the restore, except the orphan marker's condition.
2. **Renames the old folder** to `G:\a_p_r_i_r_SET_ASIDE_<YYYYMMDD>_<HHMMSS>`: one rename, nothing copied, nothing
   deleted. If the old folder is absent, this step is skipped. If Windows refuses (a file inside is open, or the
   disk is failing), nothing has changed and the tool says what it met. Then the production marker inside the
   set-aside tree, if there is one, is renamed, so no launcher runs there.
3. **Makes a fresh, empty `G:\a_p_r_i_r`,** writes `RESTORE_IN_PROGRESS.json` in it first, and unpacks every member,
   hashing each file against the list as it is written. An orphan marker inside the snapshot is not unpacked to its
   active place (below).
4. **Writes the restore record** `production_records\RESTORE_<date>_<time>.json` (create-only: the snapshot's name,
   SHA-256 and time; the set-aside tree's name; what step 1 found; the times) **and the two restore notices** of
   section 9.
5. **Rebuilds the environment from the snapshot's own lock** (section 6) and verifies it; checks the code against the
   snapshot's own hash list.
6. **Writes the production marker last** and removes `RESTORE_IN_PROGRESS.json`. Until then no launcher runs there, and
   the tool does not say the restore succeeded.
7. No snapshot is taken: the restored tree is the snapshot just read.

**If it stops half-way,** the same command again. A fresh tree still holding `RESTORE_IN_PROGRESS.json` whose
unpacking did not finish is itself renamed aside (`..._PARTIAL_RESTORE_...`) and the unpacking starts again. If only
the environment failed (a wheel missing), the command continues from step 5. The first set-aside tree is never touched
again by any run.

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
  shows the old processes are gone, not that nothing new was started since.
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
| `src/package_tools/process_check.py` (installed) | the root test no longer requires `.git`; for `restore` only, the listing rule is applied to the production path even when the folder is missing or damaged (the rule itself is unchanged) |
| `src/evaluation/ov1.py` (slice 2; the recorder, not the kernel) | reads the restore notices in its own weekly folder; one new stop cause where it would otherwise write MISSED; `register` refuses after a lost registration (section 9) |
| `src/evaluation/consolidated_report.py` (slice 3) | the formal view's wording when a registration was lost (section 9) |
| `src/package_tools/install_records.py` (installed) | the root test likewise; `_committed` and `_tracked_changes` replaced by the hash check of section 4.3 step 13 |
| New | `deploy/Deploy_Production.py` and its launcher; `deploy/RELEASE.json`; the lock file; `src/package_tools/production_snapshot.py`; `src/package_tools/production_guard.py` (the pre-check); `Run_Production_Snapshot.bat` |

Also in the integrated package, already decided: the removal of the two installed Mode H archive checks (D1).
Not edited: the OV-1 kernel (`ov1_numeric.py`), the forecasting and scoring halves, the league table, the updater.

## 12. Tests the code round must show

- **Each mode, interrupted after every durable step, then run again:** the end state equals an uninterrupted run's
  (the harness slice 3 used for the publication).
- **Identity:** a wrong byte, a missing file and an extra file under `src/` each refuse; a commit whose hash list is not
  the package's digest refuses; an older release refuses; `.bat` bytes are CRLF whatever the clone's settings.
- **`update`:** every refusal Appendix J's negative tests list that still applies (a live process, an unreadable one, a
  session lock, a foreign updater lock, an unfinished set for a roster change, P present at the release record); U and
  P left in place by a fault at each step; the release record across midnight.
- **Snapshot:** a round trip gives back every byte and every empty folder; more than 65,535 files; a flipped byte in
  the archive, a file changed, added or removed during the snapshot (a same-size rewrite included), a full or
  missing backup folder each leave no snapshot and leave the flag; an existing name is never overwritten; the overdue
  snapshot is tried first; when it cannot be made the job still runs, warns at its start and end, and exits with the
  stated status; the updater's launcher takes one after `update` and none after a read-only command.
- **Restore:** onto an invented production tree; the set-aside tree is byte-identical to the tree before, apart from
  its renamed marker; with the old tree absent, half missing, without a `.venv`, with an unreadable OV-1 ledger: the
  restore completes; a process listed refuses and no acknowledgement overrides it; extraction stopped half-way, then
  the command again; a wheel missing: no marker, RESTORE NOT COMPLETE, then complete after the wheel is put back.
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
clone into a scratch production folder (with the offline environment build); a launcher refusing in the clone and
running in the scratch folder; weekly sessions and a development batch, each ending in a snapshot; one snapshot
opened in **File Explorer by the owner** (the only step the runner cannot do) and its size and time recorded; an
`update` with a fault planted and the command typed again; an overdue snapshot taken first, and a job that goes
on with the warning when the backup folder is missing; one `restore`, with a stale orphan marker and a restart of the
PC by the owner, then a catch-up over the lost draws and the formal view's "not established" line; an `export` and what it prints; records made in one folder read in another (the open
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

## 15. The owner's choices

**Confirmed by the owner on 20 November 2026 (decision log entry 110; relayed in EX_248 section 4). Built into this
draft; listed so the ratification covers them:**

1. `.venv` is not in snapshots; it is rebuilt at a restore from the exact locked wheels of that release (section 6).
2. `SNAPSHOT_DUE` is written just before a job's first write (section 7).
3. When a snapshot that is due cannot be made, **all** jobs go on with a loud warning that stays until one is made.
   This relaxes D8's "the next job makes it first" (entry 97) for the case where it cannot be made; the risk is
   written in section 7 and printed by `update`.
4. An orphan marker neither refuses a restore outright nor is copied into the restored tree as a live block
   (section 8).
5. Formal OV-1: no difference for the research; the passed code traced; the registered claim reported truthfully
   (section 9).
6. The production guard checks the path, not only the marker's presence (section 10).
7. `restore` is a fifth mode of the one tool.
8. Production: `G:\a_p_r_i_r`. 9. Backups: `T:\a_p_r_i_r_backups`.

**Still yours, each with the options and my recommendation:**

- **A. Single owner commands and snapshots** (section 7's table). `declare-developed`, OV-1's `register` and `stop`,
  and the few other commands typed by hand through the general launchers do not take a snapshot by themselves. (a)
  Their run sheets end with `Run_Production_Snapshot.bat`, and you accept that until then their change is in no
  snapshot (recommended: these are rare, each already has a reviewed run sheet and its own go, and hooking the general
  launchers would touch every one of the thousands of runs inside a session). (b) A wrapper launcher for owner
  commands that sets the flag and takes the snapshot: one more launcher to keep right. The one that matters most is
  `register`: a registration lost by a restore cannot be made again (section 9).
- **B. The exact condition for a stale orphan marker at a restore** (section 8's boxed text). You confirmed the
  principle. The draft makes the restart a checked condition of this route, and leaves "identify and close the
  processes" to the existing per-incident clearance procedure. (a) As drafted (recommended: a restart is the one fact
  about old processes a tool can verify). (b) Also let the tool accept, without a restart, that every process
  identity recorded in the marker is gone: more code in an always-review area, and it cannot work on a marker that
  cannot be read.
- **C. The formal OV-1 check** (section 9.3). (a) One check in the recorder and one in `register`, fed by the restore
  notice (recommended). (b) A report label only. It is a small change to code that has passed review, and to
  supplement 6.8, so it needs your ratification with the reviewer's view.
- **D. The proof-of-concept suite and the guard** (section 10). (a) The two proof-of-concept probes stay unguarded, so
  the suite runs in the clone as today (recommended). (b) Guard everything and run that suite in a marked folder.
- **E. Optional, early, on its own go** (the reviewer recommends it, EX_248 section 3): run the probe of section 14
  once on your PC and open its zip in File Explorer (about five minutes, invented files only). If Explorer cannot
  open it, the fallback of section 7 changes the snapshot format, and it is cheaper to know before the code is
  written.

## 16. Documents to amend with the integrated package (each reviewed and ratified in the ordinary way)

- **Design v0.1r7 Appendix J:** the development-clone part (the verifier's PRE, POST, suite, COMMITTED, push) and the
  production part (`update`, section 4.3), with the table of section 5. Sections 4.3 (where and when the two records
  are written), 6.1 (the launchers' production guard; the snapshot at a session's end) and 7 (the checklist).
- **Direction document v0.3r1 section 9:** the backup paragraph replaced by D7 to D10 and the restore method; no
  monthly restore test; and one sentence that settles the wording difference between EX_243 ("OFF-1 read strictly")
  and H-2 v3r6 ("a new, stricter owner rule"): proposed, "The owner decided on 18 November 2026 that production holds
  no Git at all; this goes further than OFF-1's words and is binding."
- **Supplement v0.8 section 6.8** (and code plan v0.3 L5): the restore notice; one more stop cause; `register` after a
  lost registration (section 9). **The orphan-marker rule** (Architecture 5C, a protected block, amended by
  ratification and not edited; H-1 5.4): the one added exception of section 8.
- **Architecture** (the launch interfaces: the production guard in the pre-check, the new launcher); **code plan v0.3 section 10** (T017 and
  the install); **the runner's rulebook v0.6** and the owner's deny lines for the new programs; **the owner's
  checklist**; register v0.32; the next H-1.

## 17. Not designed here, uncertainties, and what could be wrong

- The dependency procedure (lock and wheel folder): its own reviewed step.
- The run sheets for the first deployment, `declare-developed` and the registrations.
- The multi-zip fallback, unless File Explorer needs it.
- **A restore by hand in File Explorer** is possible because a snapshot is an ordinary zip, but it writes no restore
  record and no restore notice, so the formal check of section 9 would not see it. It is therefore not a supported
  procedure: if the tool cannot be used, the steps are written and reviewed for that case.
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

## 18. Where each finding of EX_248 landed

| Finding | The scenario, in one line | The correction | Where |
|---|---|---|---|
| B01 emergency restore | Production is restored because its tree, environment or records are damaged, so it cannot pass a healthy-production check | `restore` has its own four requirements and never runs `check`, never uses production's Python and never needs the old tree readable; the old tree absent, half missing or unreadable is handled; a stop half-way is finished by the same command | 4.1, 8 |
| B02 the orphan marker | A marker left by a crash would block the very restore the crash calls for; copied back, it would block the fresh tree | One added exception to the owner-only rule: restart shown, fresh clean process check, typed acknowledgement; the bytes kept as evidence; never an active marker in the fresh tree; never an override of a running or uncertain process | 8, 16 |
| B03 formal OV-1 | The staged recorder turns a formerly counted draw into MISSED after a restore, and accepts a second registration | Traced on the passed code (five cases); an objective classification from three times and the snapshot's contents; one new stop cause at the earliest unverifiable draw; `register` refuses after a lost registration; v0.1's list applied by people withdrawn | 9, 14 |
| B04 export after a restore | The clone's active folders could mix production's restored state with later records | Every export is planned before it writes; after a restore, changed and clone-only files are moved to one dated folder and the active folders become exactly production's; a worked example; the tests | 4.4, 12 |
| B05 snapshots | Which commands snapshot; a coherent single state; the old release's own lock and wheels; the changed choice on an overdue snapshot | A table of commands, the updater's launcher included; a second reading of the source; each release's lock kept in production and so in every snapshot, wheels of every lock kept, and no "restored" before the environment is verified; all jobs go on with a standing warning, the risk stated | 6, 7 |
| B06 the guard | A hand-copied production folder carries the marker and would run | The path is checked at every real-data launch, inside the pre-check each launcher already makes; the proof-of-concept probes stay unguarded so safe synthetic work stays in the clone | 10 |
| Section 3, labels | A replayed forecast for a draw after an original release date | CATCH-UP, never PROSPECTIVE; revisions never pooled; a fixture | 4.3, 12 |

Not changed from v0.1: sections 3 (the release and its proof), 4.2, 4.3 and 5 (init, update, Appendix J's properties),
which EX_248 supported.

*End of the draft.*
