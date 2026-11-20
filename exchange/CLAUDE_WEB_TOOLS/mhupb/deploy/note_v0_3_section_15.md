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

