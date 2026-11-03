# Cold read of design v0.1r3 DRAFT against EX_127

Reader: a fresh helper with no prior context. Inputs: EX_127_ChatGPT.md, design v0.1r2 (comparison only), design v0.1r3 DRAFT. Git anchors checked at `3a9f6ac` with `git show` / `git rev-parse` (code files only; no data folder opened). The draft is pure ASCII (0 non-ASCII bytes) and names no person other than the project owner, Claude and ChatGPT; but see P18 for a rule that would put a person's name into a tracked file.

Section numbers below are the draft's. "Line" numbers for the draft are physical lines of the draft file.

## Findings

### P1 - BLOCKER - Records of a closed or stale session for a target with no freeze line are re-forecast, not continued (B01(c), B02)

Quoted text:
- Terms, Ticket: "the dispatch gate admits an official real-mode run only with an open ticket and never a second one for a pair with a DONE ticket".
- 3.4(b), session binding: "the run id must have an open ticket in the session's attempts ledger and the (variant, target) no DONE ticket" (per-session ledger).
- 6.3, The loop: "for each variant in **this session's roster** without a ticketed DONE record for N (from this session, or from the interrupted session this one resumed)".
- 6.4, third bullet: "a set interrupted and resumed with less than an hour left stays partial until M's result is accepted, after which the missing variants get `CATCH_UP` records and the freeze line marks them `MISSING_BATCH`".
- Appendix I, row "Restart midway with less than an hour left": "after N's result is accepted the missing variants get `CATCH_UP` records".
- Appendix I, row "The master grows during a session": "a new session completes N's set as `CATCH_UP` ... under its own roster, and N's line is written by that session".
- 6.3, The loop: "`STALE` ... the owner starts a new one, which continues from the same records".
- Appendix F, lock transitions: after `clear-session-lock` "the next session ... completes any incomplete set only as a new set under its own roster ... its DONE records stay as unnamed ticketed records of the old session ... never scored".
- B.2 B01 row: "completes only where a set is incomplete (then under the resumed id, never a new one)".

What is wrong: three ordinary paths end a session cleanly (lock removed) while target M or N has ticketed DONE records but no freeze line: (i) a resumed `FINAL_NEXT_DRAW` set with under an hour left ends `NONE` (close-session removes the lock on `NONE`); (ii) `STALE`; (iii) `clear-session-lock`. The next session has a new id, so by 6.3 it does not count the earlier session's DONE records, and by 3.4(b) the gate (which checks only the current session's attempts ledger) admits a second official run for the same (variant, target). Result: the earlier records, including genuinely PROSPECTIVE `FINAL_NEXT_DRAW` records frozen before the deadline, are silently orphaned and every variant is re-forecast as `CATCH_UP`. This contradicts 6.4 and Appendix I ("the missing variants get CATCH_UP"), contradicts "continues from the same records", contradicts the Terms ticket rule ("never a second one"), and is exactly EX_127 B01's "must not silently adopt or discard the first session's accepted records". It also lets an owner obtain a second forecast for a target by clearing a lock. Separately, "judged once, at the start of the set" (6.4) cannot be re-derived from the records unless the set's start is itself persisted: on resume `next` evaluates the hour rule afresh (Appendix F: "elif >= 1 h before M's deadline (judged once, here)").

Smallest fix: (1) make the DONE-ticket check game-wide: the gate and `next` refuse an official run for a (variant, target) that has a DONE ticket in any session's attempts ledger of the game; (2) define that a freeze line may name ticketed DONE records from earlier sessions of the same game, each keeping its own session binding (the line records the set of session ids), so a later session completes a partial set by adding only the missing variants; (3) persist a value-free `SET_STARTED` ticket (target, mode, time) so "judged once" is a record, not a recomputation; (4) correct Appendix F's lock-transition paragraph and B.2 B01(c) to match. Add L-W tests: partial FINAL set ended by `NONE`, by `STALE`, by `clear-session-lock`, each completed by a new session with zero re-forecast of an existing pair.

### P2 - BLOCKER - The install preflight runs a tool that is not installed until step 6 (B05)

Quoted text: 6.1 "`src/package_tools/process_check.py` (MHUP-A, because the install preflight needs it first; Appendix J)"; Appendix J step 2 "**Preflight:** `process_check.py check-no-runs` must print `CLEAN`"; step 6 "Copy the rest of the overlay (... `process_check.py` ...)".

What is wrong: at steps 2 and 4 the repository does not contain `process_check.py`; for MHUP-A the tool exists only in the package folder. The text never says where it is run from, how its bytes are verified before use (PRE at step 1 does not mention it), or that its own tests have passed. The B05 preflight therefore cannot run as written.

Smallest fix: state that for MHUP-A steps 2 and 4 run `process_check.py` from the package staging folder, after PRE has verified its SHA-256 against the package manifest, with the venv's Python and `-I`; from MHUP-B onward the installed copy is used. Add a rehearsal check (T016) that runs it from the package folder.

### P3 - BLOCKER - The byte-code guarantee is not delivered by the stated launchers, and excluding `*.pyc` by name opens a hole (B04)

Quoted text: 4.1 "every Mode H and weekly command runs Python with `-B` and with `PYTHONPYCACHEPREFIX` set by the launcher to a fresh, empty scratch folder, so that no pre-existing `.pyc` anywhere (under `src/` or under `site-packages/`) is ever read"; 4.1 closure "except byte-code caches (`__pycache__/`, `*.pyc`, `*.pyo`)"; Appendix H Method row "excluding `__pycache__/` and `*.py[co]` by name"; 6.1 lists `-B`/`PYTHONPYCACHEPREFIX` only for `Run_Evaluation.bat`.

What is wrong: (a) the Mode H batch (`Run_Experiment.bat Method_Walk_Forward.py plan --mode H`, 5.1) and the forecasting half (`Run_Experiment.bat Method_Weekly_Forecast.py`, 6.1) run through `Run_Experiment.bat`, which at `3a9f6ac` line 41 is `"%PY%" -u %*`: no `-B`, no `PYTHONPYCACHEPREFIX`. No section, package list (8) or Appendix L entry says `Run_Experiment.bat` (a launcher shared with the coordinator's POC path) changes. (b) `-B` plus `PYTHONPYCACHEPREFIX` only redirect the cache of modules that have a `.py` source. A *sourceless* `.pyc` placed directly in a directory on `sys.path` (not in `__pycache__`) is still imported by the sourceless loader. Because `Run_Experiment.bat` runs scripts from `src\methods` without `-I`, `sys.path[0]` is `src\methods`; a stray `json.pyc` there would shadow the standard library, and the closure deliberately does not enumerate it ("`*.pyc` ... by name"). The planted-`.pyc` test (L-U3) as described plants into caches and would not catch this.

Smallest fix: (a) name `Run_Experiment.bat` (and `Run_Weekly_Session.bat`) as changed MHUP-A/MHUP-B members that add `-B` and `PYTHONPYCACHEPREFIX`, with the Appendix L test; (b) exclude only `__pycache__/` directories from the closure and treat any `*.pyc`/`*.pyo` outside `__pycache__` (under `src/` and `site-packages/`) as a closure file, i.e. a refusal; add a test that plants a sourceless `json.pyc` in `src/methods/` and expects refusal.

### P4 - CORRECTION - The updater's redirect refusal cannot be built on the existing fetcher, and "byte-for-byte unchanged" and "three additions only" cannot both hold (C03, B04)

Quoted text: 7 A6 "v0.2 adds: the request refuses any redirect (no automatic following; a `3xx` answer is a refusal naming the `Location` host without fetching it)"; 7 "Its fetch, parse, overlap ... logic is byte-for-byte unchanged, and the identity test is a diff of the two files showing only those three additions"; Appendix L L-U6 "the v0.1 -> v0.2 diff contains only the three additions (a test over the two files' ASTs)"; 7 "`Run_Results_Updater.bat` lines 4 and 33 renamed to match".

What is wrong: at `3a9f6ac` the updater fetches with Selenium (`BrowserFetcher.fetch`, `self.driver.get(url)`, headless Chrome or Firefox). A browser follows redirects itself and WebDriver exposes no status code or `Location`; "no automatic following" and "a `3xx` answer is a refusal" are not implementable without replacing the fetch, which contradicts "fetch logic byte-for-byte unchanged". What is implementable is a check of `driver.current_url` after load (and of every navigation the page makes, if wanted). Also: `TOOL_VERSION = "0.1"` (line 54) and the module docstring must change in v0.2 or every new ledger row will say tool version 0.1, so "only those three additions" is false; "diff" (section 7) and "AST" (L-U6) name different identity tests; and in `Run_Results_Updater.bat` the tool path is on line 13 (`set "TOOL=%ROOT%src\results_master_v0_1.py"`), not lines 4 and 33.

Smallest fix: replace the redirect sentence with "after `driver.get`, refuse unless `driver.current_url` has scheme `https` and host exactly `www.lotterywest.wa.gov.au`; a redirect to another host is therefore refused after the browser followed it, before any parse or write"; state the honest limit (the browser may load sub-resources from other hosts); list the permitted diff as the three additions plus `TOOL_VERSION`, the docstring and the file name; pick one identity test; correct the `.bat` line to 13 (and line 4 only if its comment is edited). L-U6's "a `3xx` answer" becomes "a fetcher whose final URL host differs".

### P5 - CORRECTION - "A hand-typed run has no ticket and can never be official" is an overclaim; stale open tickets stay admissible (C01, B03)

Quoted text: 3.4 first paragraph "A hand-typed run has no ticket and can never be official (Q11)"; 3.4(b) "the run id must have an **open ticket** for that pair ... and the pair must have **no DONE ticket**"; 5.2 "a pair whose ticket is open but not DONE is attempted again on the next `run` under the same ticket or a new ticket after the old one is marked FAILED_TO_START".

What is wrong: a ticket is a readable value-free line naming a run id; nothing binds it to the process that wrote it. A hand-typed request that reuses the run id of an existing open ticket passes the gate. After any crash the open ticket stays open indefinitely (only Mode H mentions `FAILED_TO_START`, and only as one of two options; the weekly half says nothing), so the admission window is not just the seconds of a live run. On resume, 5.2's DONE rule ("its ticketed attempt's run folder proves the planned run happened") would then adopt the hand-typed run as official. "Under the same ticket" also reuses a run id whose create-only run folder may already exist.

Smallest fix: (1) on every resume (driver and forecasting half), before writing any new ticket, mark every open ticket whose run folder does not prove a completed run as `FAILED_TO_START` (value-free), and drop "under the same ticket"; (2) reword 3.4 to "cannot become official by mistake: it would have to copy the run id of a live open ticket"; (3) add a test: hand-typed request reusing a stale open ticket's run id after a crash is refused.

### P6 - CORRECTION - Appendix E says the gate refuses a second set for a frozen target; 3.4(b) has no such check

Quoted text: Appendix E row "`FINAL_NEXT_DRAW` for a target that already has a freeze line | refuse (publication / pin gate; `OPEN M`)"; Appendix I row "refused by the pin gate (3.4(a)) or `OPEN M` (6.3)"; 3.4(b) session binding lists no freeze-line check.

What is wrong: only `next` (the forecasting half) refuses; the dispatch gate would admit a ticketed request from another session (the case of P1). The matrix overstates what the gate enforces.

Smallest fix: add to 3.4(b) session binding "and the game's forecast ledger has no freeze line for the target" (value-free), or change the Appendix E/I cells to "refused by `next` (6.3); the gate does not check this".

### P7 - CORRECTION - Diagnostic runs above `holdout_last` before the seal: 3.4(b) admits, Appendix E refuses

Quoted text: 3.4(b) "admitted for `REAL_DEVELOPMENT` only, for any target the pin allows (`<= last_draw(v)`), with the opening record for a target at or above `holdout_first` and, for a holdout target, the game's `MODE_H_SEALED` marker as well"; Appendix E diagnostic row S1 "above `holdout_last` refused (no seal)".

What is wrong: under 3.4(b) a target above `holdout_last` needs only the opening record, so after Approval 2 it is admitted in S1-S3; Appendix E refuses it. Such a run trains on the unsealed holdout draws, and its record would be displayable before the study is sealed.

Smallest fix: in 3.4(b) write "for any target at or above `holdout_first`, the game's `MODE_H_SEALED` marker as well", matching Appendix E.

### P8 - CORRECTION - The two recovery paths for an unexpected ledger row cannot be executed under the stated rules (B04)

Quoted text: 4.1 "continue at the newer version by an owner-approved **study version advance** record ... or abandon the batch ... and re-plan under a new study manifest"; 4.1 manifest is written "create-only, `results/real/holdout/<GAME>/MODE_H_STUDY_MANIFEST_V1.json`"; 4.2 opening record is create-only, permanent and names one `study_manifest_sha256`; 5.1 `MODE_H_BATCH_ID.json` "is what makes a second plan for the game refuse"; Appendix H "any row beyond `v_a` before the seal: refuse".

What is wrong: re-planning needs a second manifest (fixed name V1, create-only), a second opening record (permanent, names the first manifest) and a second plan (refused by the batch-id record). None is possible, and nothing says which gate honours a study version advance record (the plan, `run`, the scorer and the updater all compare against `v_a` / `v_f`). Without a seal the updater refuses for that game forever (4.1 refusal (1)) and the weekly session can never start (6.7 needs the seal), so a single hand-made row is an unrecoverable deadlock, not "two reviewed paths".

Smallest fix: either define the advance record (fields; which checks read it; it replaces `v_a` for every later Mode H step and for the updater's refusal) and drop "re-plan", or state plainly that both paths need a separately reviewed design and that the game is blocked until then.

### P9 - CORRECTION - The baseline release record contradicts the "date of writing" rule (C05)

Quoted text: 4.3 "no record ever manufactures retroactive standing (a release record's date can only be the day it was written)"; 4.3 "The baseline record, `RELEASE_BASELINE_20261031_V1.json`, travels in MHUP-A ... the dates are the days the variants became released".

What is wrong: the baseline is written with MHUP-A (planned 5-9 November) yet carries 31 October dates. Also the rule depends on the PC clock (the record tool reads the local date), which is not stated.

Smallest fix: "a release record's date is the local date of the step that writes it, by the PC clock; the one exception is the owner-confirmed baseline record, whose entries carry the release dates the owner confirmed (EX_127 C05), validated against register v0.23 lines 1183, 1189 and 1215".

### P10 - CORRECTION - Wrong cross-references and stale citations

- 4.3 "after COMMITTED PASS and after the barriers are removed (Appendix J step 11)": step 11 is COMMITTED; barriers go at step 12; the release record is step 13. Fix: "(Appendix J step 13)".
- B.2 C05 row "Appendix J steps 6, 9, 11": step 6 is the overlay. Fix: "steps 9, 11, 13, 14".
- 3.2 "a test asserting equality with `src/results_master_v0_1.py`": that file is removed by MHUP-A (7: "the old file removed"). Fix: `results_master_v0_2.py`.
- 6.1 "`tests/test_wf1b_static.py` lines 34-38 and 60-63: ... and the evaluator imports no method code": at `3a9f6ac` that test is lines 40-53; lines 60-63 are the `_trusted_file_bytes`/`ledger_pin` checks and the outcome-reader users list. Fix: "lines 34-38 and 40-53".
- 6.1 and Appendix L "`test_wf1b_static.py` line 60 gains it" (`Method_Mode_H.py` may name `source_data`): the `source_data` assertion is line 59 (`self.assertNotIn('source_data', text, p.name)`); line 60 is `_trusted_file_bytes`. Fix: "line 59".
- 6.1 "the evaluator's import allowance (lines 12-16: `_common` modules on the list and the standard library only; no `subprocess`, no process tool)": `STDLIB_OK` (lines 15-16) also admits `numpy` and `evaluation`; the `subprocess` ban is a text check at lines 52-53; there is no "process tool" rule in the test (psutil is simply absent from the list). Fix the wording to that.
- 7 "`Run_Results_Updater.bat` lines 4 and 33 renamed": see P4 (line 13).

### P11 - CORRECTION - The 6.4 invariant contradicts the line-roster rule (B02)

Quoted text: 6.4 "**Invariant ...** exactly one for every roster variant when the session ended `FROZE_NEXT` or `OPEN`".

What is wrong: when a session ends `OPEN M` and a variant joined the session roster after M's line was written, that variant has no open forecast (6.3: "a variant released after N was frozen does not make N unclosed"). The invariant is false in the case L-R2 tests.

Smallest fix: "exactly one for every variant of the open line's line roster; none for a session-roster variant absent from that line".

### P12 - CORRECTION - `WAIT` and `NONE` overlap and `WAIT` names a case that does not exist

Quoted text: 6.3 "**Otherwise:** `WAIT` (the last accepted draw's successor is not yet due, or a result is pending) or `NONE` (the deadline rule forbids a forecast now)"; 6.4 "less than one hour remains, or the deadline has passed: ... (`NONE`)"; Appendix F "WAIT (result pending) or NONE (deadline rule)".

What is wrong: "the successor is not yet due" falls under `FROZE_NEXT` (no rule forbids an early forecast). After the deadline with M's result not yet in the master, both "a result is pending" (`WAIT`) and "the deadline has passed" (`NONE`) apply. There is no single answer.

Smallest fix: define `NONE` = M has no freeze line and fewer than 60 minutes remain before M's deadline, or the deadline has passed; drop `WAIT`, or define it only as "M has no freeze line, M's set was started (P1 `SET_STARTED`) and could not be completed in time". State the exit words in Terms once.

### P13 - CORRECTION - Locks are not cross-checked: install vs session, session vs updater; resume does not check the environment (B01, B05)

Quoted text: Appendix J step 2 preflight checks processes only; 4.1 updater refusal (2) "for a game whose `ACTIVE_SESSION.lock` exists"; 6.1 `open-session` "refuses while a lock exists" (its own lock only); 6.1 session record holds "the environment digest"; Appendix I "The master grows during a session (a result arrives mid-set)".

What is wrong: (a) an install can proceed while a crashed session's lock exists (no process alive), after which `open-session --resume` continues the old session with its old roster (perhaps including a now-superseded revision) on new code; nothing compares the session record's environment digest with the installed tree. (b) `open-session` does not refuse while the updater's lock `source_data/.results_master.lock` exists, so an updater started first can append a row mid-session; this is the only ordinary way to reach `STALE`, yet Appendix I presents a mid-session result as normal. (c) The lock's path is never given, although the updater v0.2 must read it.

Smallest fix: the preflight also refuses while any `ACTIVE_SESSION.lock` or the updater lock exists; `open-session` (new or `--resume`) refuses while the updater lock exists; `--resume` and every `next` refuse if the closure/environment digest differs from the session record's; give the full path of `ACTIVE_SESSION.lock`; reword the Appendix I row to "possible only if the updater was already running when the session opened, or by a hand edit".

### P14 - CORRECTION - The resume token is not "fresh" by any stated rule, and `check-no-runs` has two signatures

Quoted text: 6.1 "provided a fresh **resume token** ... requires a token for the lock's session that no earlier resume has used"; 6.1 "`process_check.py check-no-runs --game G`"; Appendix J step 2 "`process_check.py check-no-runs`" (no game); 6.1 "the one **read-only process tool**" which "writes, create-only, a resume token" and "a value-free clearance record".

What is wrong: "fresh" means only "unused"; a token written by a check whose resume never happened (e.g. the orchestrator died between the two children, or the owner typed `open-session --resume` by hand days later) remains usable after new processes may have started. It is undefined whether `check-no-runs` without `--game` (the install preflight) writes a token, and where. "Read-only" is true of processes but the tool writes files.

Smallest fix: `open-session --resume` accepts only a token whose check time is within a stated limit (e.g. 5 minutes, by the PC clock, stated as clock-dependent) and that is the newest token for the session; `check-no-runs` writes a token only when `--game G` is given and that game's lock exists; describe the tool as "never acts on a process; writes only its own value-free records".

### P15 - CORRECTION - "A Python process whose command line names the project root" may miss the real interpreter (B05)

Quoted text: 6.1 "lists, read-only through psutil, every Python process whose command line names the project root, other than itself and its own parent chain".

What is wrong: `Run_Experiment.bat` runs `"%PY%" -u %*` after `pushd "%ROOT%src\methods"`, so the script argument is a bare file name. `%PY%` is the venv's `Scripts\python.exe` redirector, which on Windows starts the base interpreter as a child; that child's command line need not contain the project root. Detection then depends on the redirector parent still being visible. The criterion is a heuristic, not the "positive identity" B.2 claims. Separately, the "zombie" negative test (Appendix J, L-I4) has no Windows meaning.

Smallest fix: select processes whose executable is the venv redirector or the base interpreter named in `pyvenv.cfg`, or whose `cwd` or any ancestor's command line is under the project root; record the rule as a heuristic with its known limits; make T016 show a live `Run_Experiment.bat` child is detected on Windows; replace "zombie" with "a process whose details cannot be read (access denied)".

### P16 - CORRECTION - "Everything refuses (P)" overstates the barrier; some STOP cells leave recovery undefined (B05, C05)

Quoted text: Appendix J steps 5-11 "everything refuses (P)"; Appendix E X column for the updater "runs (... the install barrier is honoured by the dispatch gate, not the updater ...)"; step 5 STOP "`git checkout --` of the listed paths, then remove E and P"; step 10 STOP "stop"; step 11 STOP "P stays"; steps 13-14 STOP "re-create P"; Appendix J "the record tool refuses to write a release record while P exists".

What is wrong: P is honoured only by the new dispatch gate. The updater, the WF-1B report tool (`Run_Method_Rankings.bat`, which would read mixed-version evaluator modules during steps 6-9), the coordinator's POC path and any path that does not call `contract_dispatch` are not refused; Appendix E itself says so for the updater. `git checkout --` restores changed files but leaves newly added files (new modules, the install record) in place. Steps 10 and 11-14 give no route forward: after "P stays" or "re-create P", the release record cannot be written (the tool refuses while P exists) and no step says when or how P is removed and step 13 retried, nor which date the record then carries.

Smallest fix: write "every dispatch-gated run refuses (P); the updater, the report tool and the coordinator are not gated and the checklist forbids them until step 12"; the restore steps also delete the package's added paths (listed by the manifest); for STOP at 10-14 state the resume path: fix, rerun the failed step, then (for 11) steps 12-15; the release record's date is the date of the step that finally writes it.

### P17 - CORRECTION - The orchestrator's child handling can deadlock, and it launches a third program directly

Quoted text: 6.1 "launches each half through its launcher with `subprocess.Popen(..., cwd=ROOT, shell=False, stdin=DEVNULL)` and blocks on `wait()` with no timeout ... on a child's non-zero exit it stops and prints the child's output ... It learns the session id and the target from ... one machine-readable last line"; Appendix F step 2 "`python -I src\package_tools\process_check.py check-no-runs`"; Appendix K "the orchestrator is named as a sequencer of the two launchers".

What is wrong: to read the child's output and last line the child's stdout must be a pipe; `wait()` with a pipe that fills deadlocks (Python documents this). The coordinator precedent cited (lines 943-945) uses `stdout=PIPE` with line buffering and reads the stream. The orchestrator also starts `process_check.py` directly, not through either launcher, and Appendix F writes bare `python` where 6.1 says `.venv\Scripts\python.exe`.

Smallest fix: "reads the child's stdout line by line to end of file, echoing it, then calls `wait()`"; name `process_check.py` as the orchestrator's third child (venv Python, `-I`, full path) in 6.1 and in the 5C.1 amendment.

### P18 - CORRECTION - The witness evidence rule either rejects real GitHub evidence or is trivially met, and it records a person's name (C04)

Quoted text: 6.5 "`--verified-by <name>` ... a `verify` line without an evidence text, or whose evidence text does not contain the freeze line's digest or the reference, is refused"; Appendix G "refused unless the evidence text contains d and the reference"; 6.5 "the `created_at` of the `PushEvent` from GitHub's public events API".

What is wrong: a `PushEvent` carries the commit id, not the freeze line's digest `d` (that is inside the pushed ledger file). Either a genuine GitHub quote is refused, or the verifier pastes `d` into the text, at which point the check proves nothing; it is a string-containment test on owner-typed text, which is what EX_127 C04 warned against. 6.5 says "digest or the reference" and Appendix G "d and the reference": these differ. `--verified-by <name>` writes a person's name into `WITNESS_LEDGER_V1.jsonl`, which 6.4 says is tracked and pushed (the rulebook forbids the owner's personal name in files). The public events API lists events only for public repositories, and GitHub documents a delay of up to hours.

Smallest fix: evidence = (for GitHub) the quoted event with the commit id, plus the verifier's statement that the commit's ledger file contains `d`; the tool checks the reference only, and the line says the digest binding is a human check; one rule ("reference" required, digest binding stated as human); `--verified-by` takes a role (`project-owner`, `reviewer`), never a name; note the public-repository and delay limits.

### P19 - CORRECTION - The installed-file freeze is self-contradictory on `.pyc` and will refuse spuriously (B04)

Quoted text: 4.1 "a file a `RECORD` lists without a hash (pip hashes everything except `RECORD` itself) is hashed at manifest time"; Appendix H "a `RECORD` entry without a hash, which pip writes only for `RECORD` itself and `.pyc` entries"; Appendix H Interpreter "every file under its `DLLs/` and `Lib/` trees"; Appendix H Byte-code "the claim is 'never read', not 'never present'".

What is wrong: the two parenthetical statements disagree. Hashing `.pyc` files under `site-packages/__pycache__/` and the base `Lib/` tree (including `Lib/__pycache__/`) freezes bytes that the design says are never read, and they can be rewritten by any Python run without `-B`; Approval 2's updater run (`Run_Results_Updater.bat`, no `-B`) happens between the manifest and the plan. A new `.pyc` for a module first imported then is an "unlisted file under `site-packages/`", which Appendix H makes a refusal.

Smallest fix: one statement (pip leaves `RECORD` and compiled `.pyc` entries unhashed); exclude `__pycache__/` directories from the `site-packages/` and base `Lib/` digests and from the orphan check, consistent with the "never read" claim (sourceless `.pyc` outside `__pycache__` still refuses, P3); or give `Run_Results_Updater.bat` `-B` and `PYTHONPYCACHEPREFIX` too.

### P20 - CORRECTION - Finalisation after a crash between the report and the seal is not idempotent (B03)

Quoted text: 5.2 "`MODE_H_SEALED` (the scorer, after the report ...)"; "if it stops after `SCORE_COMPLETE`, rerunning it reads no outcome at all and only produces the report and the seal".

What is wrong: if the crash falls after the report was written (create-only, with its search-log row) and before the seal, the rerun "produces the report" again and collides with the existing file, or writes a second report and a second `MODE_H_REPORT` row. L-H2 also claims "byte-identical final report" without saying the report carries no run time.

Smallest fix: "if a report for this attempt already exists, the rerun verifies its digest against the accepted lines and writes only the seal; otherwise it writes the report then the seal"; state that the report contains no wall-clock field, or drop "byte-identical".

### P21 - CORRECTION - No rule for a torn last line in the append-only JSONL ledgers

Quoted text: 6.5 forecast ledger "create-only, digest-chained"; 6.6 score ledger "append-only"; 5.2 "one score line per planned pair (create-only, in the Mode H score ledger)"; attempts ledgers (3.4).

What is wrong: a crash during an append can leave a partial last line. Every reader then refuses (chain or grammar error) and no recovery is defined, which contradicts "a crash anywhere resumes by rerunning the command" (6.3). "Create-only line" inside an appended file is also not a defined operation.

Smallest fix: state the write discipline (one `write` of the full line plus newline, then `fsync`, as the updater's ledger does at lines 280-288) and the rule: a final line without its newline is ignored and reported on the next run, then completed by appending the same event again; never edited by hand.

### P22 - CORRECTION - "Retired" is used everywhere but no record defines it (B02)

Quoted text: 6.1 "**session roster** (every released, unretired variant ...)"; Terms "Roster: the released, unretired variants"; 4.3 baseline "E_1 revision 2 marked `superseded_by: revision 3`".

What is wrong: 4.3 defines release records only. Nothing says what makes a variant retired (a registry status, a record, a package), whether "superseded" counts as retired, or when a retirement takes effect relative to a session. The roster is therefore not computable from the stated records.

Smallest fix: one sentence in 4.3: a variant is retired when its registry chain entry is superseded or marked retired by an installed package; the session roster is computed at `open-session` from the release records minus those entries.

### P23 - WORDING - `LATE_PRE_DRAW` is decided by acceptance, not by the draw

Quoted text: Appendix I "Late before the draw: `FINAL_NEXT_DRAW`, `frozen_at_utc` >= deadline, result not yet accepted when made".

What is wrong: the criterion is "before the result was accepted", not "before the draw". A run still going after the evening draw is labelled "pre draw". Smallest fix: say so in 6.4 ("frozen after the deadline and before the result was accepted; whether before the draw itself is not established").

### P24 - WORDING - Overclaims

- Section 1: "provided B01, B04 and C05 are met (they are, in sections 3.4, 4.1 and 5.3)": an assertion awaiting this review. Fix: "(addressed in ...)".
- Appendix I: "Every combination of the inputs falls in exactly one row above": the restart, roster and master-grows rows are scenarios, not input combinations, and overlap the tier rows. Fix: "every record falls in exactly one of the tier rows; the remaining rows show scenarios".
- Appendix I row "or no release record" -> development: unreachable, because an unreleased variant is not in any session roster (4.3, 6.1). Fix: delete or say "cannot occur".
- Terms, Lifecycle markers: "the updater refuses until the seal exists": omits the one permitted first update at `v_f` (4.1). Fix: "refuses, after the first update, until ...".
- Section 2 and ER-2r1 "copied first and deleted last": in Appendix J the release record is written and committed after E and P are deleted. Fix: "deleted last of the install's files; the release record follows".
- Appendix C: "its findings are applied in this text": true only after this read is applied. Fix when shipping.

## Section C - state-machine traces

1. Rerun the same week after `FROZE_NEXT M`, before M's result: the previous session closed cleanly; a new session opens with the same pin; no unclosed accepted target; M has a line, so `OPEN M`, nothing made (6.3, F, 6.4 example). ONE ANSWER.
2. S1 freezes N at v; the updater admits N at v+1; S2 scores N: 6.3 "Across weeks" plus Appendix F's score step: the score binds to S1's line, training pin v, outcome pin v+1, provenance S2. ONE ANSWER. (The equal-pin rule applies to new publications only, 3.4(a).)
3. Crash after the freeze line, before scoring; rerun: the lock remains; the orchestrator runs `check-no-runs`, then `--resume`; `next` returns `FROZE N`; `score` runs. ONE ANSWER, subject to P14 (token freshness) and P15 (detection).
4. Crash during the runs for N; rerun: resumed under the same id; the variants without a DONE ticket rerun. AMBIGUOUS on the crashed run's open ticket: 5.2 "same ticket or a new ticket after ... FAILED_TO_START" (Mode H only); the weekly half is silent (P5). If N is M and fewer than 60 minutes remain on resume, P1/P12 apply: 6.4 says the set "stays partial", Appendix F re-judges the hour rule, and the session ends `NONE` with the lock removed, after which a new session re-forecasts every variant.
5. New variant released after three post-holdout targets were scored: those lines stay closed under their line rosters; it joins at the next session (6.3, E preamble, F (vii), L-R1). ONE ANSWER; it also receives development-tier records for backlog targets that predate its release and have no line yet (6.4 bullet 2), which 6.3's "first weekly target is the first target frozen after its release" covers only implicitly.
6. Variant retired with an open forecast: it stays in that line and is scored; no new forecast (6.3, F (vii), I). ONE ANSWER, but "retired" is undefined (P22) and the 6.4 invariant is wrong for newcomers (P11).
7. The master grows during a session: `next` exits `STALE`; every further publication refuses. CONFLICT on what follows: 6.3 says the new session "continues from the same records"; Appendix I says it "completes N's set as `CATCH_UP` under its own roster"; 6.3's loop and 3.4(b) make it re-run every variant (P1). Also reachable only when the updater was already running at `open-session` (P13).
8. `clear-session-lock` on a session whose set for N was incomplete, then a new session: Appendix F re-forecasts N under the new roster and leaves the old DONE records unscored; B.2 B01(c) says completion happens only "under the resumed id, never a new one"; L-W3 says "no record adopted, discarded or rewritten". CONFLICT (P1).
9. Mode H scorer crashes after `SCORE_COMPLETE`, before the seal: the rerun reads no outcome and writes the report and the seal (5.2, 5.4, L-H3). ONE ANSWER, except when the report was already written (P20).
10. Hand-typed run with a valid Mode H binding while the batch is in progress: refused for lack of a ticket (3.4, E, L-G1). ONE ANSWER unless the run id of an open ticket is reused, which the gate admits (P5).

## Section D - updater v0.2 and the environment freeze

- The three additions are listed the same way in 7, 8 and B.2: two refusals, the exact-host rule and self-test cases. Nothing still says the updater is unchanged; Appendix K records the amendment, and 3.1's "Binding until MHUP-A is installed: the updater is not run in any form" is consistent. Stale points: 3.2's equality test against `results_master_v0_1.py` (P10), the unimplementable redirect clause, the version string and the `.bat` line (P4).
- The environment freeze is checkable in principle: `RECORD` hashes, an orphan-file check, and interpreter files from `pyvenv.cfg`'s home. It is not consistent as written (P19). `PYTHONPYCACHEPREFIX` is promised by launchers that do not set it (P3, `Run_Experiment.bat`). The sourceless `.pyc` gap is real (P3).

## Section E - Appendix J

- Order: preflight (2), barriers (3), preflight again (4), gate files first (5), overlay (6), POST (7), suite (8), install record (9), package commit (10), COMMITTED (11), remove E then P (12), release record (13), release commit (14), push (15). This matches the order EX_127 asks for.
- Gate closed until COMMITTED: yes for dispatch-gated runs through step 11; in steps 5-9 STOP the restore removes P only after the old code is back. Gaps: the tool for steps 2 and 4 is not yet installed (P2); "everything refuses" overstates (P16); no forward path after STOP at steps 10-14 (P16).

## Section F - Appendix D anchors (git at 3a9f6ac)

| Anchor | Blob (rev-parse) | Actual first line | Verdict |
|---|---|---|---|
| `src/methods/_common/game_draws_reader.py` 161-209 | `dcd425b9e143` | `def _parse_prefix(raw: bytes, game_id: str, target: int, *, include_dates: bool):` (209 is the function's `return`) | VERIFIED |
| `src/Powerball_Experiment_Coordinator.py` 29 | `ca5d3a374efa` | `    import psutil` (indented, inside `try:` at 28; `except ImportError` exits at 30-31) | VERIFIED (indent stripped, as in the other anchors) |
| same, 35 | `ca5d3a374efa` | `WRAPPER = ROOT / "Run_Experiment.bat"` | VERIFIED |
| same, 793 | `ca5d3a374efa` | `    output = [str(WRAPPER), name, "--poc", "--case=" + args.case, "--run-id=" + run_id]` | VERIFIED |
| same, 943-945 | `ca5d3a374efa` | `proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,` ... `cwd=ROOT, shell=False)` | VERIFIED |
| `src/results_master_v0_1.py` 533-537 | `7e3e67ba2061` | `def gov_url(game: str, a: date, b: date) -> str:` (536 builds `https://www.lotterywest.wa.gov.au/results/...`) | VERIFIED |
| `tests/test_wf1b_static.py` 16 | `9e359c9a260b` | `             'json', 'math', 'pathlib', 'platform', 're', 'struct', 'sys', 'uuid', 'numpy', 'evaluation'}` (second line of `STDLIB_OK`, which starts at 15) | VERIFIED |

Spot-checks:
- Evaluator import confinement: lines 12-14 `ALLOWED_COMMON` and 15-16 `STDLIB_OK` define the allowance; the enforcing test is lines 40-53 (non-recursive `EVAL.glob('*.py')`; text bans on `subprocess`, `os.kill`, `E_0` and others at 52-53). Lines 34-38 are the *methods-side* ban on importing the evaluator or naming `outcome_reader`. So the design's "lines 12-16" for the allowance is right; "standard library only" is not (numpy and `evaluation` are allowed), and "60-63" for "the evaluator imports no method code" is wrong (P10).
- The coordinator imports psutil at line 29: yes, guarded by `try/except ImportError`. psutil is installed by `install_upgrade_dependencies_into_venv.bat` (`DIRECT_PACKAGES`, line 8), not by `requirements.txt`; "already the coordinator's dependency" holds.

## EX_127 coverage

- B01: PARTIAL. (a) `OPEN M` and (b) cross-session scoring are resolved with concrete rules (6.3 "Across weeks", "The next-draw cases"). (c) Same-session resume is specified, but sets left without a line by `NONE`, `STALE` or `clear-session-lock` are re-forecast and their records orphaned, and the gate's DONE check is per session (P1, P6). (d) Lock transitions are given, with gaps in token freshness and lock cross-checks (P13, P14), and `WAIT`/`NONE` are ambiguous (P12).
- B02: PARTIAL. The line roster versus session roster and the closed-under-line-roster rule are concrete and resolve the deadlock. The invariant contradicts the rule (P11), and "retired" is undefined (P22).
- B03: PARTIAL (narrow). Ticket plus no-DONE plus lifecycle markers in the gate, value-free; the marker order and same-attempt resume are concrete. Gaps: report-then-seal idempotence (P20) and reuse of a stale open ticket (P5).
- B04: PARTIAL. The updater v0.2 refusals are concrete and fail closed. Byte-code closure is not delivered by `Run_Experiment.bat`, sourceless `.pyc` is a hole (P3), the `.pyc` handling is inconsistent (P19), and the recovery paths are unexecutable (P8).
- B05: PARTIAL. The order and "barriers removed only after COMMITTED" are resolved; the session lock is cleared only by the tool, nothing is terminated and the orphan marker is untouched. But the preflight tool is absent at steps 2 and 4 (P2), identity detection is heuristic (P15), "everything refuses" overstates (P16), and the post-COMMITTED STOP path is undefined (P16).
- C01: PARTIAL. Q11 is decided, tickets and the diagnostic root are concrete, and the trust boundary is stated honestly. "Can never be official" overclaims while stale open tickets are reusable (P5).
- C02: RESOLVED. 6.6 separates the scientific identity from execution provenance, with the L-S1 negative test.
- C03: PARTIAL. The exact host, no fallback and the limits of the checks are stated, but the redirect clause cannot be built on the Selenium fetcher and conflicts with "fetch logic unchanged" (P4).
- C04: PARTIAL. Commit timestamps are rejected and the concrete receipt sources are named, but the containment rule is unworkable or trivial for GitHub evidence, and the verifier's name goes into a pushed file (P18).
- C05: PARTIAL. The install record and release record are distinguished, the release date comes from the release record, and there is no CATCH_UP without one. The baseline date rule contradicts itself (P9), the cross-references are wrong (P10), and there is no forward path after a STOP at steps 11-14 (P16).
- O01: RESOLVED. Section 1, 5.4 and 6.6 keep Mode H as a separate retrospective family, and Q7 stays open.
- O02: RESOLVED. The 6.2 status block gives the last accepted version, OPEN/PENDING targets and the lock interlock; the out-of-scope items are listed in section 9.
