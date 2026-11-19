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
