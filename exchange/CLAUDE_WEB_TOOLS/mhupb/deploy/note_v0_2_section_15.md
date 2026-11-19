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

