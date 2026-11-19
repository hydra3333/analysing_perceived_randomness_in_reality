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

