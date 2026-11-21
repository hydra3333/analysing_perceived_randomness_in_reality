## 0A. What v0.6 changes, and how to read the rest (EX_258; EX_259 sections 7 and 8 G)

v0.6 is v0.5 with two kinds of change, shown exactly in `NOTE_v0_5_TO_v0_6.diff`.

**1. An error removed.** v0.5 said that after a restore `update` first puts back any later release, and gave an order
to "keep lines supported". The owner rejected that: "that isn't a restore it is a restore being mangled." **A restore
recreates exactly the selected verified snapshot: its code, variants, data, results, records and saved environment,
at the same path. Nothing is put back, retired, activated, upgraded or rebuilt automatically, from Git, from the
clone or from the set-aside tree.** The lost draws are then caught up by the ordinary job with the snapshot's own
variants. Any later software or method change is a separate owner decision, after he has looked at why the restore
was needed. Sections 0, 4.1, 4.3, 8, 9, 12, 15, 17 and 18 are corrected accordingly.

**2. The system this note deploys has been simplified** (the research system simplification design DRAFT v0.1, sent
with it). Where a passage of this note still uses the words of the left column, read the right column. The backup,
recovery-kit, restore, guard and environment sections do not depend on the difference.

| This note says | Read |
|---|---|
| the weekly session; the development batch; their sequencers and orchestrators; `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` | the one research job, `Run_Research.bat` (simplification design, section 5) |
| the install record and the release record, born in production under `src/`; "a roster change"; "an unfinished weekly set" | none of these exist. Installation is release. Each `update` writes one line in `production_records\DEPLOYMENT_LOG.jsonl` and `RELEASE_<commit>.json`; nothing is written under `src/` in production except the barrier file while an update runs |
| a session lock | the job lock |
| `declare-developed`; league `admit` and `repair`; a witness line | no such commands remain |
| catch-up, development and prospective "labels" | one fact on each forecast line: whether the result was on file when it was computed |

A full rewrite of this note in the simplified system's words belongs with the phase 2 package. It is not done here so
that the reviewer can see exactly what changed in a design already examined five times.

