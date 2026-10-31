# Predictive Randomness - WF-1B supplement: the report's order, the batch progress line, and more workers (WORKERS-1), design note v0.1

**Document:** a supplement to the ratified releases and WF-1 design (`Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md`, LF `03f95fbe...12ee`, OWNER-RATIFIED 31 October 2026). That design's sections 6 to 8 (the scorer, the report, N1 and the seed) stay the design of WF-1B, unchanged. This note adds only what the owner decided since, and what coding needs settled first.
**Version:** v0.1 DRAFT for the reviewer's R-3 review, 31 October 2026. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule. Where it proposes a change or a reading, the owner decision is listed in section 9.
- **No code yet:** the code follows only after this note passes.
- **Base:** `main` at `0eb39cb` (register v0.22 installed at `2b1e7e3`; EX_099 and EX_101 at `0b067f1` and `80b7e31`; the seed announcement EX_103 at `92a6cef`).
- **Inputs:** the owner's directions recorded in register v0.22 ("The owner's directions for WF-1B": the report's order, the progress line, WORKERS-1); EX_101's four obligations for WORKERS-1; Architecture v0.8 (5A.4, 10.1, O-CPU-01, O-POL-03, ERR-R2-01, A-04, A-25); R3 v0.5 sections 7.2, 17.6, 17.9 and 17.10.

## 1. In plain English

**Three additions to the work already designed:**
1. **The report shows the real results first.** Each league table that ranks methods by what they actually achieved against the real draws (prizes won, numbers matched) comes first. The tables that measure how surprising those results would be under fair random draws come after, under their own heading, "adjusted against fair random draws". Nothing is computed differently; only the order and headings change.
2. **The walk-forward batch shows its progress** as it runs: runs done out of the total, the percentage, the elapsed time and an estimate of the time left.
3. **More workers (WORKERS-1).** The coordinator's limit of 6 workers becomes "1 up to the computer's logical processor count" (24 on your PC), with a default of half that (12). The walk-forward driver gets the same `--workers` option, so a batch uses many cores instead of one. With 12 workers the Powerball batch should take minutes, not 80.

**What does not change:** the scorer, the measures, N1, the seed procedure, the families and their labels, the holdout and every gate. A batch run with several workers produces the same predictions as one run with one worker; section 5.4 says exactly what "the same" means, and there is a command to check it.

**The packaging proposal (decision WB-0):** the scorer and report are the main road to your first real forecasts, so they go first as **WF-1B**. The workers change and the progress line go as a separate small package, **WF-1C**, reviewed with this note but coded and installed after WF-1B, so that it cannot delay the scorer.

## 2. What stays as ratified

- **The scorer and report:** design v0.1r1 sections 6.1 to 6.9 (the order of a report run, the fixed grids, the downgrade rules, the outcome reader, the records, the measures, the numerics, the families with M = 80, the search log, the report files with no drawn numbers).
- **N1 and its seed:** sections 7 and 8. Until SEED-1's approved policy is installed, the report runs with N1 off and says so (`N1_NOT_RUN`, 7.6).
- **The driver's rules:** section 5.3 (the STOP table, the start-of-run checks, resume, segment records, exit codes) and the WF-1A install's attempt binding (EX_083 WF1A-R2-B01). Section 5 below keeps each rule and says how it holds with several workers.
- **The cohort:** since E_1 revision 2, each game's batch holds 40 variants, so each family has M = 80 (register v0.22, "Out-of-date statements").

## 3. The report's order (the owner's direction; decision WB-1)

R3 already asks for this. R3 7.2: "Every evaluation report begins with what was actually forecast, what was actually observed, the evaluation formula, and its denominator. ... reference p-values, synthetic calibration ... are separate clearly labelled layers." R3 17.6: "Two ranking tables where relevant: a descriptive table (by the raw score) and a significance table (by local Z_plus, with global figures). They are never conflated."

**Proposed layout of the text report** (R3 17.10.2's six parts, with part 4 split and moved up):
1. **Header,** as in 17.10.2.
2. **Part A, "League tables: results against the real draws".** Every descriptive table, measure by measure in R3's order: MR0 (divisions won, best first), MR1 and MR1-T, MR4, MR5, MR7 and MR16. Each is ranked by its descriptive key as R3 17.6 defines it (for example MR7 by S - n x mean0, the matches above the fair-draw average, so that tracks with different n compare fairly). These keys use only the real results and fixed fair-draw averages: no simulated draws and no p-values.
3. **Glossary,** as in 17.10.2.
4. **Fair-draw reference,** as in 17.10.2.
5. **Part B, "League tables: adjusted against fair random draws".** Every significance table: local Z_plus and its label, the exact tails, N1's figures, and the families' global figures.
6. **Per-track detail and notes,** as in 17.10.2.

**RK-4 still holds in Part A:** R3 17.9 RK-4 says any report highlighting a top-ranked track shows the number of tracks and tests compared, the global figures and the search-log count. So Part A opens with one line giving them: the number of tracks, the number of tests, the search-log count for the game, and each family's global result with its label (or "N1 not run"). It also points to Part B.

**The CSV and JSON** carry the same rows as now; each row gains a `table_kind` field (`DESCRIPTIVE` or `SIGNIFICANCE`). The text report is the only file whose order changes.

**Why a decision is needed:** R3 17.10.2 lists the glossary and fair-draw reference before the league tables. Moving Part A up is a departure from that order (the content is unchanged), so the register records it. The option is to keep 17.10.2's order exactly and split part 4 into A then B in place.

## 4. The batch progress line (WF-1C)

- **While a batch runs,** the driver prints one line at most every 10 seconds and whenever a variant finishes:
  `[WALK-FORWARD] PROGRESS 4120/17280 runs (23.8%); variants finished 9/40; workers 12; elapsed 0:03:41; estimated left 0:11:48`
- **The estimate** is the elapsed time divided by the runs done this invocation, times the runs left. It is shown only after 20 runs, and is labelled an estimate.
- **It is console output only.** It writes nothing, and nothing depends on it. The read-only `status` command is unchanged.

## 5. More workers (WORKERS-1; WF-1C)

### 5.1 The limits (EX_101 obligation 4)

- **The upper limit** is the computer's logical processor count, read when the program starts: Python's `os.process_cpu_count()` (the processors this process may use), falling back to `os.cpu_count()`. It is capped at 60 (Windows' wait functions take at most 64 handles; 60 leaves room).
- **If neither function gives a number,** the limit is 1.
- **The default** is half the limit, rounded down, and at least 1: 24 gives 12; 23 gives 11; 1 gives 1.
- **`--workers N`** accepts 1 to the limit; anything else is refused before anything runs, with the limit named.
- **One function,** `worker_limits()`, in `src/methods/_common/`, serves both the coordinator and the driver. Tests patch both processor-count functions and check the limit and default for None, 1, 2, 23, 24 and 64.
- **The memory guard** (5.6) is separate: it can stop dispatching at any worker count, and it never changes the limit or the default.

### 5.2 The coordinator

- `--workers` keeps its meaning, with the limits of 5.1 in place of "1..6" (default 12 on your PC instead of 6).
- **Nothing else changes:** its memory floors (`--min-available-gb` 4.0, `--critical-available-gb` 2.0), its owner safety switch, its orphan rules and its status evidence.
- **The coordinator still runs no science:** no coordinated run exists (D2-1), and its Windows lifecycle tests are still not authorised. This change only prepares it.
- **Test edits (HIGH, listed):** the static check `p1p2_static_checks.py` asserts the text `workers <= 6`; it will assert the call to `worker_limits()` instead. E2R-T12's identity test compares 1 and 6 workers in a spawn pool; it will compare 1, 6 and 12 (the default on the owner's machine). The Windows proof-of-concept suite (`windows_architecture_poc_suite.py`, owner-run only, not authorised) is left as it is.
- **The Architecture amendment:** O-CPU-01's "configurable 1-6, default and maximum 6" and A-04's and A-25's six-worker wording are read as amended by WORKERS-1 once WF-1C is ratified (register). The Architecture's text is not edited.

### 5.3 The driver with several workers

- **`run --game G --batch ID --workers N`.** Without `--workers`, the default of 5.1 applies. `--workers 1` behaves exactly as today, one run at a time in one process.
- **Structure:** one parent process (the driver) and N worker processes, started one at a time (Python `multiprocessing`, the `spawn` method, the same on Windows and Linux). The parent is the only process that:
  - decides what runs next;
  - writes `attempts.jsonl` (one line per attempt, before the run starts, exactly as today);
  - classifies results by the STOP table;
  - writes the segment record and prints the progress.

  A worker only runs what it is given: one ordinary `run_contract_method` call through the unchanged runner, which writes the run folder as it does today. Its result (outcome, reason, run ID) goes back to the parent.
- **Order:** each worker takes the next variant in cohort order and runs that variant's pending targets in ascending order, one at a time; the parent hands it each next target only after the previous result has come back. Variants run side by side, but each variant's targets are in order, as the owner asked.
- **Every rule of design 5.3 that concerns one run holds unchanged,** because each run is the same call as today: the runner's refusals, the dispatch gate, the reader's development-prefix rule, the pins, create-only folders, and attempt binding.

### 5.4 What must be the same at any worker count (EX_101 obligation 2)

**The canonical scientific content:** for every (variant, target) pair of a plan, a batch run with N workers gives, for each pair proven done:
- the same terminal outcome and reason prefix; and
- for a `SUCCESS`, a forecast with the same `canonical_content_digest` (the field the scorer already compares, design 6.1 step 3).

**What legitimately differs,** and is never compared: run IDs, run-folder names, the attempt order in `attempts.jsonl`, times in records, segment records, and the order of console lines. Whole folders are therefore never compared byte for byte.

**The check:** a new read-only command, `compare --game G --batch A --batch B`, compares two batches with the same game, window and cohort digest. For every pair it prints whether both are done, and whether the outcome, reason prefix and content digest agree. It ends with `IDENTICAL: all <n> pairs` or `DIFFERENT: <k> of <n> pairs`, then lists each difference. It reads only plans, attempt lines and run folders (forecast records, not outcomes), as `status` does, and appends no search-log row.

**This holds by construction, and the tests confirm it:** each run is a pure function of its request and the pinned master (the installed methods are deterministic, and every run's thread limits are pinned by `Run_Experiment.bat`). Nothing a worker does depends on another worker.

### 5.5 Stops, interrupts and failures with several workers (EX_101 obligation 3)

**A STOP is a STOP, with one difference that cannot be avoided without killing processes:**
- When a run ends in the STOP class, the parent hands out no further work: no new run starts anywhere. Runs already under way in other workers (at most N - 1) are not interrupted, because the project never kills a process. Each finishes on its own, and the parent records and classifies it as usual. Then the workers exit, the parent waits for each one to end, writes the segment record and stops with exit code 1.
- **The segment record** lists every run of the invocation, including those that finished after the STOP, and every STOP class result. Its `stop_reason` names the earliest STOP in plan order (cohort order, then target) among those observed, so that the reason given does not depend on timing when several occur. All of them are listed.
- **With `--workers 1`,** no run ever starts after a STOP, as today.

**Resume, with the cause still present (keeping design 5.3's "at most one failed attempt"):**
- every `run` invocation first runs **one** pending pair alone (the first in plan order), in one worker;
- only if that run is in the CONTINUE class are the other workers started;
- so a resume whose cause persists (a changed master, say) makes exactly one failed attempt and stops, at any worker count.

**Refusals before any run:** the plan load, the start-of-run registry and flag checks, and the `--workers` range check, all before any worker starts: exit code 2, as today.

**The orphan marker:**
- the parent checks it before handing out each run, and stops handing out work if it appears;
- the runner also refuses any run while it is present (a STOP);
- the driver never writes, reads beyond its presence, or clears it, and it writes no status or PID files.

**Ctrl-C:**
- In a Windows console, Ctrl-C reaches every process of the console, the workers included. A worker's run under way ends with its own `INTERRUPTED` terminal record (the runner's existing behaviour), which is a STOP, and the worker exits. A worker between runs exits without starting another.
- The parent stops handing out work, waits for every worker to end (it never terminates one), writes the segment record and exits with code 1.
- A second Ctrl-C does not hurry anything. The parent prints that it is waiting for N workers to finish their current run, and that nothing is killed.

**If the parent ends unexpectedly** (the window is closed, say): each worker's channel to the parent breaks, so the worker exits after its current run, without starting another. A run cut off by the window closing is left without a terminal record, which resume already treats as not done. A resumed batch may find a duplicate of a pair that a departing worker completed; duplicates are expected and already handled by the scorer (equal digests pass; unequal ones are `REPRODUCIBILITY_FAIL`, design 6.1 step 3).

**What is not added:** no timer, no kill, no termination path, no status PIDs, and no coordinator involvement. The driver stays outside Architecture section 10's coordinator lifecycle, as WF-1A is.

### 5.6 Memory (EX_101 obligation 1)

- **Measured:** a synthetic walk-forward over all 40 Powerball variants in one Linux process (the WF-1 timing probe, 3 targets each, through `probe_wf_memory.py`; output `ev_wf1b_memory_powerball.txt`) peaked at about **46 MB** of resident memory (45.4 and 45.9 MB in two runs; Python 3.13, NumPy 2.5). Twelve workers would use about 0.6 GB, plus the parent: far below the Architecture's planning figure of about 2 GB per worker, which predates the methods. This is Linux planning evidence; Windows will differ somewhat.
- **The guard,** the same idea and defaults as the coordinator's (Architecture 10.1):
  - before handing out each run, the parent reads the available memory (`psutil`, already a project dependency used by the coordinator);
  - **below 4 GiB available:** no new run is handed out, and the batch stops cleanly (a STOP, "MEMORY_ADMISSION_FLOOR"), once the runs under way end;
  - the floor is a constant in the driver, with no command-line override, so changing it is a reviewed change.
- **Nothing is ever killed for memory.** The coordinator's own critical floor, which can stop a running worker, has no counterpart in the driver.
- **The owner's first batch at 12 workers:** watch Task Manager's memory graph; heavy paging means using fewer workers.

### 5.7 Windows evidence (decision WB-3)

- **In the package's suite,** on Linux in Claude's runs and on the owner's Windows machine at install: a synthetic batch run with 1 and with 12 workers, compared with `compare`: `IDENTICAL`. The suite also runs the STOP, resume, orphan-marker and refusal tests with 3 workers, and the limit tests.
- **Ctrl-C with several workers on Windows** is a lifecycle test, which is not authorised. The suite tests it on Linux, by raising the interrupt inside the runner. On Windows, the first real proof is the owner's own use.
- **Proposed real-data check, read-only for outcomes:** after WF-1C's install, you run each game's batch again at the default 12 workers (new batch IDs, each counted in the search log), then `compare` each new batch with its single-worker original. `IDENTICAL` on 17,280 and 8,760 pairs is strong evidence that the parallel driver changes nothing. It reads no outcome, so it is safe at any time.

## 6. SEED-1 and the first reports (decision WB-2)

- **The pulse is brought forward (EX_103, committed and pushed at `92a6cef`, 31 October 2026, 09:30 UTC):** the owner replaced the announced 6 November pulse with the pulse of `2026-10-31T10:30:00.000Z`, under WF1-9 and D-10, an hour before it existed. The new policy is `N1_ROOT_NIST_C2_20261031T1030Z_V1`. The replaced policy was never fetched and stays on file, counted (design 8.4).
- **If that pulse passes design 8.2's checks,** its `APPROVED` `SEED_POLICY_V1` record (design 8.3) travels in WF-1B under `src/evaluation/seed_policies/`, with both earlier records (the replaced and the provisional) as history. Each game's report then runs once, with N1.
- **If it fails a check,** the policy is `REFUSED` and a new pulse is announced the same way (design 8.1). WF-1B then installs without an approved policy, and the reports run with N1's figures labelled `N1_NOT_RUN` and every other figure complete; they are run again once a policy is approved. Every report attempt is a `RANKING_REPORT` row in the search log, and is counted.

## 7. Documentary items

- **EX_080 O03 (non-gating), qualified here:** design v0.1r1's statements that NIST's chain links "hold on two public chain 1 pulses" (sections 8.2 and 9.5) are illustrative, not independently verified. In the probe, the next pulse's `previous` value was set equal to the earlier `outputValue` before being compared, so that comparison is tautological. The SHA-512 relation was really computed, but on values whose archive provenance the probe did not establish. Nothing depends on either: the chain-link check is not part of SEED-1's approval (WF1-12).
- **R3 finding R3-5 (for the next register):** R3 17.10.2's order places the glossary and fair-draw reference before the league tables. WB-1 moves the descriptive tables (Part A) first, as R3 7.2 asks.

## 8. Tests

**WF-1B:** design v0.1r1 section 10's WF-1B list, plus the order of section 3:
- Part A comes before the glossary and Part B after the fair-draw reference, in the text report;
- every descriptive table precedes every significance table;
- Part A's RK-4 line is present, with the counts and each family's global label;
- the CSV and JSON `table_kind` field;
- no significance figure appears in Part A, and no table appears in both parts.

**WF-1C:**
- **the limits:** `worker_limits()` with patched processor counts (None, 1, 2, 23, 24, 64); `--workers` 0, the limit plus 1 and a non-number are refused before any worker starts; the coordinator uses the same function;
- **identity:** a synthetic batch with 1 and 12 workers gives `IDENTICAL` under `compare`; a planted difference in one forecast gives `DIFFERENT` and names the pair;
- **order:** each variant's targets run in ascending order in its worker (from the attempt lines); only the parent writes `attempts.jsonl`; an attempt line precedes each run;
- **STOP with 3 workers:** no run starts after the parent receives a STOP; runs under way finish and are recorded; `stop_reason` is the earliest in plan order; exit code 1;
- **resume:** with a persisting data-admission failure, exactly one attempt is made, by one worker, and nothing else starts;
- **orphan marker** created mid-batch: no run is handed out after it;
- **interrupt:** a `KeyboardInterrupt` raised inside a worker's run ends that run `INTERRUPTED`, no new run starts, every worker ends, and nothing is terminated (a test double for `Process.terminate` and `kill` fails the test if called);
- **parent loss:** a worker whose channel closes exits after its current run;
- **memory guard:** a patched available-memory reading below 4 GiB hands out no new run and stops with `MEMORY_ADMISSION_FLOOR`;
- **progress line:** its format, its throttling and the estimate's 20-run minimum;
- **`--workers 1`:** today's WF-1A tests pass unchanged;
- **static checks:** the driver still imports no evaluation code and opens no data file; no `terminate`, `kill` or `os.kill` appears in the driver;
- **mutation checks:** a run handed out after a STOP; the canary skipped on resume; a worker writing `attempts.jsonl`; `stop_reason` by arrival instead of plan order; the memory floor ignored; the limit not capped.

## 9. Owner decisions

- **WB-0 (RECOMMENDED): two packages.**
  - Why: the scorer is the main road to your first real forecasts; the workers change touches the driver and the coordinator, and should not hold the scorer up.
  - Recommended: WF-1B (scorer and report, with section 3's order) first; WF-1C (workers, progress line, `compare`) reviewed now with this note, coded and installed after WF-1B.
  - Option: one package, as WORKERS-1 first said ("WF-1B also replaces ..."), installed once both are ready.
- **WB-1 (RECOMMENDED): Part A first** (section 3).
  - Why: you asked for the real-outcome rankings first, and R3 7.2 says the same.
  - Recommended: header, Part A (real draws), glossary, fair-draw reference, Part B (adjusted against fair random draws), detail and notes.
  - Option: R3 17.10.2's order exactly, with the league tables split into A then B in their usual place.
- **WB-2 (RECOMMENDED): the approved seed policy travels in WF-1B** (section 6), if tonight's pulse passes its checks, and each report runs once with N1. If it fails, WF-1B installs without one and the reports run with `N1_NOT_RUN`, then again after approval.
  - Why: no separate SEED-1 package or second report run is needed.
  - Option: a separate tiny SEED-1 package after WF-1B (design section 3).
- **WB-3 (RECOMMENDED): Windows evidence for WF-1C** (section 5.7): the suite's synthetic identity and stop tests at install, Ctrl-C tested on Linux only, and your two real re-runs at 12 workers compared with the originals.
  - Why: the re-runs are the strongest evidence and read no outcome; a Windows Ctrl-C test with several workers is a lifecycle test, which is not authorised.
  - Option: skip the real re-runs (the suite's synthetic evidence only).
- **WB-4 (RECOMMENDED): the limits and the guard as in 5.1 and 5.6:** limit = logical processors (cap 60), default half rounded down (at least 1), the driver's memory floor 4 GiB with no override.
  - Option: a different default (for example the full count) or floor.

## 10. What the reviewer is asked to check (R-3)

1. **The report's order:** that Part A holds only descriptive figures and Part B every significance figure; that RK-4 holds in Part A; that nothing is hidden or relabelled.
2. **EX_101's four obligations:** memory (5.6), the identity definition and `compare` (5.4), the stop, interrupt and failure rules (5.5), and the limits (5.1).
3. **A STOP is a STOP:** whether letting runs already under way finish (at most N - 1), with no new run started and everything recorded, is an acceptable reading for several workers, given that nothing may be killed.
4. **The resume canary:** that it keeps design 5.3's "at most one failed attempt" when the cause persists.
5. **No new process-management risk:** no kill, no timer, no status PIDs; the parent waits for every worker; a lost parent leaves only states that resume and the scorer already handle.
6. **The coordinator change:** that it changes only the limit, and that the test edits are correct.
7. **Mark, never suppress:** that nothing here hides a run, a method or a number.

## 11. Not in scope

- Everything design v0.1r1 sections 6.9 and 14 exclude.
- **Mode H** (scoring the holdout draws) and **prospective forecasts** (forecasting a draw that has not yet happened). They come next, in their own design, which Claude drafts while this one is reviewed.
- Running anything through the coordinator; Windows lifecycle tests.
- Any change to a method, to the runner, or to the gates.
