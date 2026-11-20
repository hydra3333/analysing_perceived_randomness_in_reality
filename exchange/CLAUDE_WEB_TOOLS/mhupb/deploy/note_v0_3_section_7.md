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

