# MHUP-B deployment design note - DRAFT v0.1

**Status:** DRAFT for the reviewer's design-stage review (R-3). Not ratified. It authorises nothing.
**Written:** 20 November 2026, 00:09 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's go
of 19 November 2026, 23:50 (decision log entry 107: the design note only; Fable (High)).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH (it replaces part of a ratified install procedure, design Appendix J; it touches gates, installs
and the formal OV-1 claim). **Base:** `main` at `dd5788d`; staged slices as passed (EX_231, EX_237, EX_242).

## Work-item card

| Item | |
|---|---|
| Work item | MHUP-B deployment layer: design note |
| Binds it | Owner decisions D1 to D12 (EX_243; decision log 92 to 98); EX_244 (restore and replay; governs); decision log 100 (how a restore is done), 103 (Python 3.15 only), 104 (no monthly restore test), 105 (no replay comparison), 107 (this go); H-1 v7r1 section 12.11 (the checklist); the working principle of 18 November 2026 |
| Replaces | The Git-based steps of design v0.1r7 Appendix J, for production; the backup paragraph of the direction document v0.3r1 section 9 |
| Not in scope | Any code, package, task file, Windows step, install, restore or run. Slices 1 to 3 are not reopened |
| Evidence state | DESIGNED. Nothing implemented or tested, except one small probe on invented files (section 14) |

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
   Python's own `zipfile`, read back and hash-checked before it counts, named with the date and time, in your backup
   folder on T:. Every production job ends with one. A small "snapshot due" file makes the next job take it first if
   it was missed.
6. **Restore** renames the old tree aside (kept), unpacks the snapshot into a fresh tree at the same path, rebuilds the
   Python environment and writes a short restore record. After that you work normally: the updater, then the weekly
   session, replay the missing draws one at a time from the draws before each. That is valid research (EX_244). Nothing
   is compared with the old tree, no timestamp proof is asked for, nothing stops.
7. **The formal OV-1 claim is kept apart.** A restore never blocks forecasting, scoring, league tables or the
   descriptive OV-1 view. Whether a game's *registered formal stream* goes on is settled by one short rule fixed now
   (section 9), from a list of line kinds the restore tool prints. No records are carried forward.
8. **A marker file** at the production root. Every launcher refuses without it, so a weekly session or a registration
   typed in the E: clone does nothing.

Seven choices are yours (section 15), each with the alternatives and my recommendation.

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
- **Not verified (carried to the code stage or T017):** that no reader of an existing record compares an absolute path
  stored in a record with the current root (records made on E: must read correctly on G:); File Explorer opening a
  ZIP64 archive; snapshot time on the owner's drives; that G: and T: are NTFS and distinct physical drives; how Windows
  refuses a folder rename while a file inside is open.

## 2. The production folder

    G:\<production>\                 (the owner names it; a short path, section 15 item 8)
      PRODUCTION_ROOT.json           the marker: schema, this folder's absolute path, the time it was made, the
                                     release it was made from. Written once, last, by init or restore.
      PRODUCTION_SETTINGS.json       the owner's settings: the backup folder (T:...), the wheel folder (section 6).
                                     Plain JSON the owner may edit.
      Run_*.bat                      the launchers (release)
      src\                           the code (release), with the install records and the barrier P where they are today
      source_data\  results\  transitory_data\      data and records, exactly as on E: today
      production_records\            written only by the deploy tool and the snapshot code:
                                     RELEASE_<commit>.json (the hash list of each release deployed; create-only),
                                     DEPLOYMENT_LOG.jsonl (its last line names the current release),
                                     SNAPSHOT_LOG.jsonl, INIT_RECORD.json, RESTORE_<date>_<time>.json,
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
both; the longest path. Every other mode starts with the same checks and stops on a refusal.

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
marker guard keeps real-data jobs from running there; `export` keeps the tracked ones current.

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
- **After a restore** production's records legitimately differ from the clone's. `export --after-restore` is allowed
  only when production holds a restore record the clone does not; it then copies production's files over the clone's
  working files. Git's history keeps every earlier version, so nothing is lost. It never deletes: files the clone has
  and production lacks are listed and left.
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
| 9. The marker guard; every mode re-runnable | Sections 10 and 4 |
| 10. The snapshot | Section 7 |
| Appendix J's two stated residual risks (D3: three programs no barrier stops; a run straddling the gate copy) | Smaller: with the marker guard every launcher refuses outside production, and P is in place before any file changes. A project program started by hand between two checks remains the stated residual |

## 6. Production's Python environment (D6)

- **Made fresh**, never copied: `python -m venv` from the same base installation the development environment uses,
  then `pip install --no-index --find-links <wheel folder> --require-hashes -r <lock file>`. No network.
- **The lock file** (`deploy/PRODUCTION_REQUIREMENTS_LOCK.txt`, reviewed, in the clone) pins the exact version and
  SHA-256 of every wheel. It lists only what the installed code imports and what those need (fact 7), at the versions
  of the development environment the suite passed on. Other work's packages stay out, so they can no longer change
  production's environment.
- **The wheel folder** holds the wheel files. It is not evidence (every wheel is hash-checked against the lock when
  installed), so it lives outside Git and outside the snapshots; recommended place: beside the snapshots on T:.
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
  its SHA-256 goes into a list stored as the last member (`SNAPSHOT_MANIFEST.json`). Then the archive is **read back**:
  every member's bytes are hashed and compared with the list, and each file's size and time are compared with what was
  seen before it was read (a file that changed meanwhile fails the snapshot). Only then is it renamed to `<name>.zip`
  (never over an existing name), a line is appended to `SNAPSHOT_LOG.jsonl`, and `SNAPSHOT_DUE` is removed. A
  `.partial` file is never a snapshot.
- **Name:** `PRODUCTION_<YYYYMMDD>_<HHMMSS>_<JOB>.zip`, local time, for example `..._WEEKLY_OZLOTTO.zip`; the UTC time is
  inside.
- **Where the code lives:** one module in the release, `src/package_tools/production_snapshot.py` (standard library
  only; it imports no method or evaluator code), started as a child process with production's Python, like the
  process tool. A launcher `Run_Production_Snapshot.bat` lets the owner take one by hand.
- **Which jobs end with one:** the weekly session and the development batch (their two sequencers), and the deploy
  tool's `init` and `update`. **Not** hooked: the updater (it keeps its own backups, and its change is in the next
  job's snapshot) and single owner commands such as `declare-developed` and OV-1's registration; their run sheets end
  with `Run_Production_Snapshot.bat`. (A registration is the one record a restore must not lose: section 9.)
- **`SNAPSHOT_DUE`:** written just before a job's first write (the weekly session: before `open-session`), removed
  only by a verified snapshot. It means "production may have changed since the last verified snapshot". A job that
  finds it takes that snapshot before anything else (D8), whatever kind of job left it and however long ago. A job
  that was refused before it started writes nothing and leaves no flag.
- **If the end-of-job snapshot fails** (T: unplugged, disk full): the job's own work stands and nothing is undone; the
  flag stays; the job's exit status says so (a new status "complete, snapshot not made" when everything else was
  complete; otherwise the job's own status, with the snapshot line printed as well). The live path comes first, as for
  the league table.
- **If an overdue snapshot cannot be made at a job's start:** section 15 item 3.
- **Nothing prunes the backup folder.** The owner deletes old snapshots when he chooses; `check` prints their number
  and total size.
- **More than 65,535 entries** needs the ZIP64 form, which `zipfile` writes by itself (section 14). Whether File
  Explorer opens it is to be shown on the owner's PC. **Fallback if it does not:** several ordinary zips per snapshot,
  each under 65,535 entries, under one manifest. Not designed unless needed.

## 8. Restore (D10; decision log entry 100; EX_244)

`restore --snapshot <zip>`, on the owner's own go each time:

1. **The snapshot is verified in full** (every member against its list) before anything is touched.
2. **Checks on the tree to be set aside:** no project process (the process check, run from the clone's hash-verified
   copy, because production's own Python may be what is broken; an unreadable process is a refusal; nothing is
   terminated; an uncertain process is treated as alive and the restore waits). **The orphan marker:** section 15
   item 4. A session lock, the updater's lock or P left in the old tree by the job that broke do **not** block the
   restore: they are files that go aside with the tree, and the restore record lists them.
3. **The formal OV-1 listing** (section 9) is printed and kept for the restore record.
4. **Rename** the production folder to `<name>_SET_ASIDE_<YYYYMMDD>_<HHMMSS>`: one rename, nothing copied, nothing
   deleted. Windows refuses it while any file inside is open; then nothing has changed and the tool says what to
   close. The marker inside the set-aside tree is then renamed too, so no launcher runs there.
5. **A fresh, empty folder at the standard path;** every member unpacked, each file hashed against the list as it is
   written; the marker last.
6. **The environment** rebuilt from the lock and wheel folder and verified; production checked against its own stored
   hash list (the code in a snapshot is the code that was deployed then).
7. **The restore record**, create-only, `production_records\RESTORE_<date>_<time>.json`: the snapshot's name and
   SHA-256, the set-aside tree's name, what was found in the old tree (locks, the formal OV-1 listing), the times.
8. No snapshot is taken: the restored tree is the snapshot just read.

A fault part-way: the same command again. A fresh tree that was not finished is itself renamed aside
(`..._PARTIAL_RESTORE_...`) and the unpacking starts again; the first set-aside tree is never touched again.

**After a restore, ordinary work, each step on its usual go:** the updater brings the results forward; the weekly
session catches up one target at a time, each from the draws before it; development jobs, league tables and reports
as normal. Per EX_244 this is valid research. Records made in the replay carry their real times and their truthful
labels: a forecast made after its draw is catch-up or development evidence, not prospective. **One plain consequence,
stated so that nobody is surprised:** forecasts that were genuinely made before their draws, after the snapshot, are
in the set-aside tree (and in Git's history if they were exported), not in production; the replayed ones for the same
draws are labelled catch-up. That is truthful labelling. Nothing is merged back, compared (entry 105) or recovered.

**By hand, if the tool or the clone is unavailable:** because a snapshot is an ordinary zip, the owner can rename the
folder and extract the zip in File Explorer. The run sheet will say what the tool would have checked.

**No monthly restore test** (entry 104). T017 rehearses one restore in a scratch folder.

## 9. The formal OV-1 claim after a restore

**What is and is not at stake.** Nothing ordinary: the staged code already goes on when a formal stream is stopped.
Only this: may a game's *registered* stream still carry its 2.5% claim? Its missed rule rests on the assumption that no
eligible freeze line is ever removed after the fact (supplement 6.8). A restore removes from production every line
written after the snapshot. If the recorder simply ran on, a draw that had been genuinely frozen before its cut-off
and counted would be recorded as MISSED (factor 1), because its replayed freeze line is later than the cut-off. A
restore decided after results are known could then erase counted draws, and the claim would not hold. So the claim
needs a rule; the research does not.

**The restore tool's part** is small and holds no draw value. For each game with a registration in the set-aside
tree it lists the lines that the set-aside tree's OV-1 ledger and forecast ledger hold beyond the snapshot's copies:
line number, kind, target draw number, written time. It prints the list and stores it in the restore record.

**The rule, fixed now so that it is never chosen after the event.** The owner applies it with Claude from that list,
before the first weekly session after the restore, and it is recorded in the decision log; if in doubt, F-C. No step of
it is needed before any calculation, and no program waits for it:

- **F-A. Nothing beyond the snapshot.** The stream is the same stream. It continues.
- **F-B. Only lines the recorder writes again by itself, identically or before any outcome exists.** It continues.
  These are exactly: (i) a FACTOR line for a target whose eligibility line and its confirmation are in the snapshot
  (the factor is looked up in the table sealed before the outcome; a different result would be the recorder's own
  contradiction STOP); (ii) a MISSED line (it is missed again); (iii) the freeze, eligibility and confirmation lines
  of a target whose cut-off has not passed when the first session after the restore runs (they are made again before
  the cut-off; if that session in fact runs after the cut-off, this is F-C); (iv) catch-up freeze lines, which play no
  part in the formal stream.
- **F-C. Anything else,** for example: a next-draw freeze line frozen before its cut-off, for a target whose cut-off
  has passed, that the snapshot lacks; a STOP line; or the registration itself. The formal claim for that game is
  **not established** from there on:
  - a lost counted or countable draw, or a lost STOP: the owner records the stop with the existing command
    (`Method_OV1.py stop`) before the first session. Every report then shows the stream as stopped, by code that has
    already passed review. The stop lands at the stream's open target, so at most one re-derivable factor is given up;
  - a lost registration (the snapshot is older than the registration): the game is **not registered again** unless
    the owner separately decides it with the reviewer's assessment (no second registration: OD-4; EX_219 C1; EX_244
    section 1 D). The restore record says so in words.
  In every case forecasting, scoring, the league table and the retrospective OV-1 view go on over every draw. If a
  session is run before the rule was applied, nothing ordinary is harmed: under F-B the recorder has only written the
  same lines again; under F-C the stop is recorded late, and the restore record's list shows which lines in between
  are outside the claim.

**Why F-B is sound:** under it the restored stream ends up with the same counted draws and the same factors as the
lost one, whichever snapshot was chosen and whenever; the choice cannot favour any outcome. **Why not more:** a restore
to the latest snapshot soon after a job broke, before the next cut-off, is F-A or F-B, which is the common case; only
a restore that reaches back past counted draws costs the formal claim, and it costs nothing else.

**Alternatives.** (1) Stop the formal stream on any difference: simplest, but it would end a game's one confirmatory
test for a fault that lost nothing of substance. (2) The rule above: recommended. (3) Carry the formal ledger and its
evidence forward from the set-aside tree: recovery machinery, which the owner ruled out and which would bring back
records from a tree judged unusable. (4) Do nothing and let the recorder run: rejected, because it would silently
turn counted draws into missed ones under a claim that forbids exactly that.

## 10. The marker guard (D5)

- **Rule:** every root launcher (`Run_Coordinator`, `Run_Experiment`, `Run_Evaluation`, `Run_Method_Rankings`,
  `Run_Results_Updater`, `Run_Weekly_Session`, `Run_Development_Batch`) refuses, before starting Python, unless
  `PRODUCTION_ROOT.json` exists beside it. Two lines in each `.bat`, no extra process per run.
- The two sequencers and `check` also compare the path recorded in the marker with where they are, so a production
  tree copied elsewhere by hand is noticed.
- **Effect:** in the E: clone no launcher runs. The offline suite is not affected (it starts Python directly);
  rehearsals run in a scratch production folder that `init` makes. **One existing thing changes:** the owner-run
  Windows proof-of-concept suite (`tests/windows_architecture_poc_suite.py`) starts the real launchers in the tree it
  is run from, so from now on it is run in a marker-holding folder (a scratch production folder, or production). This
  is the cost of the uniform rule; section 15 item 6 has the alternative.
- **Limits, stated:** it is a wrong-folder guard, not security: Python typed by hand bypasses it, as it bypasses the
  launchers' other checks today.

## 11. Edits to code that is installed or has passed review

Counted edits, each old text asserted to occur once, with a line-level diff, as for the slices:

| File | Edit |
|---|---|
| `Run_Experiment.bat`, `Run_Evaluation.bat`, `Run_Method_Rankings.bat`, `Run_Results_Updater.bat`, `Run_Coordinator.bat` (installed); `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` (slice 3) | the marker test |
| `src/sequencer_children.py` (slice 3) | a `snapshot` child kind; the marker's path check; "overdue snapshot first" and "end-of-job snapshot" in one place |
| `Weekly_Session_Orchestrator.py`, `Development_Batch_Orchestrator.py` (slice 3) | `main` wrapped: guard and overdue snapshot before, snapshot and exit status after; `SNAPSHOT_DUE` written before the first writing child. The sequence itself is untouched |
| `src/package_tools/process_check.py` (installed) | the root test no longer requires `.git` |
| `src/package_tools/install_records.py` (installed) | the root test likewise; `_committed` and `_tracked_changes` replaced by the hash check of section 4.3 step 13 |
| New | `deploy/Deploy_Production.py` and its launcher; `deploy/RELEASE.json`; the lock file; `src/package_tools/production_snapshot.py`; `Run_Production_Snapshot.bat` |

Also in the integrated package, already decided: the removal of the two installed Mode H archive checks (D1).
Not edited: the OV-1 kernel and recorder, the forecasting and scoring halves, the league table, the report.

## 12. Tests the code round must show

- **Each mode, interrupted after every durable step, then run again:** the end state equals an uninterrupted run's
  (the harness slice 3 used for the publication).
- **Identity:** a wrong byte, a missing file and an extra file under `src/` each refuse; a commit whose hash list is not
  the package's digest refuses; an older release refuses; `.bat` bytes are CRLF whatever the clone's settings.
- **`update`:** every refusal Appendix J's negative tests list that still applies (a live process, an unreadable one, a
  session lock, a foreign updater lock, an unfinished set for a roster change, P present at the release record); U and
  P left in place by a fault at each step; the release record across midnight.
- **Snapshot:** a round trip gives back every byte and every empty folder; more than 65,535 files; a flipped byte in
  the archive, a file changed during the snapshot, a full or missing backup folder each leave no snapshot and leave
  the flag; an existing name is never overwritten; the overdue snapshot is taken first.
- **Restore:** onto an invented production tree; the set-aside tree is byte-identical to the tree before; a launcher
  refuses in it; a process listed, or an orphan marker, refuses as decided; the formal OV-1 listing for each of F-A,
  F-B and F-C on invented ledgers; after a restore the weekly sequence on invented data runs to a clean end.
- **`export`:** new, grown and identical files; a changed create-only record refuses and writes nothing; the two
  exempt kinds; `--after-restore` refused without a new restore record; production's bytes never change.
- **Static:** the snapshot module and the deploy tool contain no terminate, kill or signal call and import no method or
  evaluator code; nothing in the release set starts `git`, other than the two historical places named in section 1.
- One Python 3.15 build in the cloud (entry 103); planted defects for each rule above.

## 13. What T017 rehearses (one task file, its own go, a reviewed rulebook allowance)

In scratch folders only, on invented masters and records, through the real launchers: `check` and `init` from a task
clone into a scratch production folder (with the offline environment build); a launcher refusing in the clone and
running in the scratch folder; weekly sessions and a development batch, each ending in a snapshot; one snapshot
opened in **File Explorer by the owner** (the only step the runner cannot do) and its size and time recorded; an
`update` with a fault planted and the command typed again; an overdue snapshot taken first; one `restore`, then a
catch-up over the lost draws; an `export` and what it prints; records made in one folder read in another (the open
check of section 1); the whole suite before and after, as the owner decided on 13 November 2026. No step changes the
PC's date, time or zone; nothing is terminated; no real data is read or written.

## 14. The probe (invented files; cloud, Linux; an indication only)

`zip_probe.py` beside this note, output in `zip_probe_output.txt`: 81,500 invented JSON files, 215 MB, zipped by
`zipfile` (Deflate, level 9) on Python 3.15.0b4: the ZIP64 end records are written without being asked for; 81,502
entries; the read-back check found 0 mismatches; an empty folder came back; the extracted tree equalled the list.
About 9 seconds to write, 3 to check, 5 to extract. The archive was 140 MB, but the invented content is mostly random
digits and compresses poorly; real records should do better. None of this says anything about the owner's drives or
File Explorer.

## 15. Choices for the owner (each: the question, the options, my recommendation and why)

1. **Is `.venv` inside each snapshot?** (a) No: rebuilt at a restore from the wheel folder (recommended: the
   environment is as large as the data, changes rarely and can always be rebuilt and verified; snapshots stay about
   half the size and time). (b) Yes: a restore is "unzip and go", at roughly double the size and time of every
   snapshot (my estimate, not measured), and it still depends on the base Python being where it was.
2. **When is `SNAPSHOT_DUE` written?** (a) Just before a job's first write (recommended: it then also covers a job cut
   off by a power failure; cost: a couple of minutes at the rerun). (b) When the job finishes, the wording of
   entry 97: a job that dies midway leaves no flag, and the next snapshot comes at the end of the rerun.
3. **A job finds an overdue snapshot and cannot make it** (T: missing). (a) It stops before starting, except the
   weekly session, which goes ahead with a loud warning because a forecast must be frozen before its deadline
   (recommended). (b) Every job goes ahead with the warning. (c) Every job stops.
4. **The orphan marker at a restore.** (a) The restore refuses while the tree to be set aside holds one; the owner's
   approved clearance procedure comes first (recommended: the marker means a process may still be alive, which is
   exactly when a tree must not be moved). (b) The restore carries the marker across into the fresh tree unchanged.
   Either way a restore is never a way round the marker.
5. **The formal OV-1 claim after a restore:** the rule of section 9 (recommended), or "any difference stops it".
6. **Where the marker guard sits:** (a) every launcher (recommended: one uniform rule, nothing real can start in the
   clone; cost: the Windows proof-of-concept suite moves to a marker-holding folder, section 10). (b) Only the two
   sequencers, the updater's launcher and the irreversible owner commands: the proof-of-concept suite stays where it
   is, but the rule has a list to keep right.
7. **`restore` as a fifth mode of the one tool** (recommended: the checks of section 8 are the point), or a hand
   procedure in File Explorer only. D4 named four modes; this adds one to the same tool, not a second tool.
8. **Two names, when convenient:** the production folder on G: and the backup folder on T: (short paths, please: the
   set-aside name adds 26 characters to every path in the old tree).
9. **Optional, early, on its own go:** running the probe of section 14 once on your PC and opening its zip in File
   Explorer (about five minutes, invented files only). If Explorer cannot open it, the fallback of section 7 changes
   the snapshot format, and it is cheaper to know before the code is written.

## 16. Documents to amend with the integrated package (each reviewed and ratified in the ordinary way)

- **Design v0.1r7 Appendix J:** the development-clone part (the verifier's PRE, POST, suite, COMMITTED, push) and the
  production part (`update`, section 4.3), with the table of section 5. Sections 4.3 (where and when the two records
  are written), 6.1 (the launchers' marker test; the snapshot at a session's end) and 7 (the checklist).
- **Direction document v0.3r1 section 9:** the backup paragraph replaced by D7 to D10 and the restore method; no
  monthly restore test; and one sentence that settles the wording difference between EX_243 ("OFF-1 read strictly")
  and H-2 v3r6 ("a new, stricter owner rule"): proposed, "The owner decided on 18 November 2026 that production holds
  no Git at all; this goes further than OFF-1's words and is binding."
- **Architecture** (the launch interfaces: the marker test, the new launcher); **code plan v0.3 section 10** (T017 and
  the install); **the runner's rulebook v0.6** and the owner's deny lines for the new programs; **the owner's
  checklist**; register v0.32; the next H-1.

## 17. Not designed here, uncertainties, and what could be wrong

- The dependency procedure (lock and wheel folder): its own reviewed step.
- The run sheets for the first deployment, `declare-developed` and the registrations.
- The multi-zip fallback, unless File Explorer needs it.
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
- Rule F-B (iii) depends on a human reading of "has the cut-off passed" from the printed list. The cut-off is a fixed
  instant (01:30 UTC on the draw date); the run sheet will give it for the draw in question.
- Size: about a small slice (one tool, one module, counted edits to twelve files, their tests).

*End of the draft.*
