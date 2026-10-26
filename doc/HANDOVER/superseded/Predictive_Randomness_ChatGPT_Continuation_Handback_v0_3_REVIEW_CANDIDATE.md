# Predictive Randomness — ChatGPT Project Continuation and Recovery Handback

**Version:** v0.3 — **IMMEDIATE SAFETY CHECKPOINT / REVIEW CANDIDATE, NOT YET OWNER-RATIFIED**  
**Prepared:** 23 October 2026, Australia/Adelaide; **checkpoint occurs BEFORE manual clearance** of a real unresolved-orphan marker.  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Proposed repository path:** `doc/HANDOVER/Predictive_Randomness_ChatGPT_Continuation_Handback_v0_3.md`  
**Predecessor:** `doc/HANDOVER/Predictive_Randomness_ChatGPT_Continuation_Handback_v0_2.md` — **owner-ratified historical handback; preserve unchanged**.  
**Snapshot/installation status:** Owner's Windows console verified coordinator v0.6; source SHA-256 `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`. Claude independently accepted v0.6 for **non-destructive** Windows installation/testing. This handback is a new documentation candidate, not an independently ratified source release. **Do not claim it has been committed or pushed.**

> # CRITICAL — ACTIVE SAFETY INTERLOCK: DO NOT START A NEW COORDINATOR RUN
>
> At this handover checkpoint the owner has **NOT YET CLEARED** the real `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json` marker. The experiment's original processes have been independently confirmed gone and evidence was successfully archived, but the active marker was deliberately retained awaiting a final read-only clearance check and explicit operator action. **Do not delete, rename, overwrite, ignore, or bypass the marker merely because the archive passed.**
>
> **One incident only:** group `coord-2a42fac2c24549b5b216ffa691f225a7`, run `coord-2a42fac2c24549b5b216ffa691f225a7_w001`; original marker SHA-256 `2d8269eb3845cf17ce7124254f1f9397ae52a1dd5603a0aeb67bdda05453a2aa`.
>
> **Immediate next safe step:** preserve this handback; then, only when owner elects to continue, run the incident-specific clearance utility's **read-only `--check`**. Review output before its separately authorised `--clear-confirmed`. A successful check is **not** itself a clearance. The script writes a clearance record and deletes the exact pinned marker only in the latter mode. No destructive/process-termination action is permitted.

---

## 1. Emergency restart instructions — current incident comes first

This section **supersedes all stale “next step” paragraphs** in v0.2 and all earlier orphan-interlock review-candidate handbacks. If a replacement assistant starts here, **first determine the actual present state**; the last observed state is recorded below, not a claim about the disk at some future moment.

1. Confirm repository root `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` and current coordinator SHA-256. The owner verified v0.6 hash `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`; check current contents again before proceeding. Global top-level `ENABLE_PROCESS_TERMINATION = False` is required, with no command-line override.
2. **Check whether `transitory_data\poc_runs\UNRESOLVED_ORPHAN.json` still exists**. At this document's checkpoint it **does**. If its bytes/hash/group differ, stop; do not apply the incident-specific utility to a different marker. Do not assume a missing marker means safe clearance occurred: request/inspect the corresponding audit evidence.
3. Archive already completed successfully, at `results\architecture_poc\20261023_timeout_no_kill_coord-2a42fac2`. Its seven archived original evidence files and `archive_record.json` were generated and validated on Windows; **the console transcript itself was not demonstrated to be in the archive**. Preserve the owner's chat/console transcript separately where appropriate. The archive was verified, but do not mistake successful archiving for a successful experiment.
4. Owner received ZIP `P1P2_Clear_Archived_Real_Orphan_v0_1.zip`, containing incident-specific `P1P2_Clear_Archived_Real_Orphan_v0_1.py`; there is **NO evidence yet that either mode of this script has been run**. The earlier proposed commands were:

   ```cmd
   .venv\Scripts\python.exe -B transitory_data\P1P2_Clear_Archived_Real_Orphan_v0_1.py --check
   echo CHECK_EXIT_CODE=%ERRORLEVEL%
   ```

   **Read-only checkpoint:** expected `CHECK PASS`, exit `0`, active marker unchanged. If anything differs, **leave marker in place** and investigate. The exact script and its archive layout must be checked against current files before execution.
5. **Only after successful `--check` and the owner's deliberate decision** may the incident-specific `--clear-confirmed` action be run. Its source verifies coordinator SHA, pinned marker bytes/identity, archived bytes/checksums, original process PID **plus creation times** and stored FAILED status. It writes `manual_clearance_record.json` with `xb`/flush/fsync before unlinking the exact marker. It neither kills processes nor modifies the experiment files. If a partial attempt created a clearance record but left the marker, **do not retry automatically**; inspect it first.

   ```cmd
   .venv\Scripts\python.exe -B transitory_data\P1P2_Clear_Archived_Real_Orphan_v0_1.py --clear-confirmed
   echo CLEARANCE_EXIT_CODE=%ERRORLEVEL%
   ```

6. After an actual PASS, independently confirm marker absence, the saved original marker/hash and the new clearance record; only then resume ordinary non-destructive coordinator tests. If marker still exists, stop. **Never run a new experiment while the marker is unresolved.**
7. **Never manually kill a listed PID merely from a warning.** If any recorded identity remains alive or uncertain, retain the marker and escalate. Every identity check must compare PID **and original process creation time**. Status-reported PID is evidence for safety blocking, **never kill authority**.

### Exact real incident identities and preserved evidence

| Recorded identity | PID | Creation time (epoch seconds) | Last observed, twice on Windows |
|---|---:|---:|---|
| Root wrapper `cmd.exe` | `31720` | `1792749106.972062` | **Original gone**, PID absent |
| Captured Python child #1 | `17432` | `1792749107.0698512` | **Original gone**, PID absent |
| Captured Python child #2 / experiment | `25212` | `1792749107.0771797` | **Original gone**, PID absent |
| Status-reported experiment (not additional process) | `25212` | `1792749107.0771797` | **Original gone**, PID absent |

- **Source coordinator:** v0.6 `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`; owner verified using `certutil` immediately before rehearsal.
- **Marker location:** `transitory_data\poc_runs\UNRESOLVED_ORPHAN.json`.
- **Marker hash:** `2d8269eb3845cf17ce7124254f1f9397ae52a1dd5603a0aeb67bdda05453a2aa` (owner's `certutil` output; also verified by separate read-only inspector and archive utility).
- **Marker group:** `coord-2a42fac2c24549b5b216ffa691f225a7`; **schema:** `ENGINEERING_UNRESOLVED_ORPHAN_V1`.
- **Archive destination:** `results\architecture_poc\20261023_timeout_no_kill_coord-2a42fac2`; owner obtained `ARCHIVE PASS` and exit `0` from archive utility, which explicitly reported **original marker still active**.
- **Archived original file inventory:** `UNRESOLVED_ORPHAN.original.json`, `manifest.json`, `worker_001.stdout.log` (empty), `runtime_environment.json`, `pip_freeze.txt`, `status.json`, `canonical_result.json`; plus `archive_record.json` containing per-file hashes and lengths. **No proof yet that `manual_clearance_record.json` exists.**
- **Probe status:** `FAILED`, `error = "OSError: [Errno 22] Invalid argument"`, `elapsed_seconds = 60.005447...`, `finished_utc = 2026-10-23T09:52:47.190050+00:00`. `canonical_result.json` exists. The coordinator ended after approximately 10 seconds, so a later probe stdout write to a closed/broken pipe is the **likely** explanation, corroborated by source ordering (result published before final print); there is **no traceback proving the exact failing line**. **Do not relabel this experiment SUCCESS.** The failure is not evidence of a remaining live process.
- **Operator UX:** two flushed `SAFETY STOP` banners appeared: first on timeout; second when reader pipes remained open. Later launch refusal repeated the original incident and required steps, returned exit `2` without launching a worker. The duplicate banner is an acknowledged cosmetic/semantic issue; preserve real evidence.

### Incident chronology (owner-reported Windows console, 23 October 2026)

1. Preflight: coordinator SHA matches reviewed v0.6; **no** pre-existing marker.
2. Command `call Run_Coordinator.bat --poc --case=sleep-timeout --count=1 --workers=1 --sleep-seconds=60 --timeout-seconds=10`: root/2 descendants positively captured; `[SAFETY PROOF] experiment_matched=True unmatched_status=none ownership_anomalies=none` and `[SAFETY AFTER] ... TERMINATION_DISABLED ... no signals issued`; marker published durably, `FAIL successes=0/1`, coordinator exit `1`. Subsequent reader-pipe warning did not overwrite existing marker.
3. Command `call Run_Coordinator.bat --poc --case=canonical-fixture --count=1 --workers=1` while marker active: `SAFETY STOP` explained original incident, **no worker launched**, exit `2`.
4. Read-only inspection script: all recorded original identities gone, marker unchanged; returned exit `2` **because it also required successful probe completion** (`status=FAILED`). That is a stricter completion check than the ratified safety-clearance rule, **not** an observation that any process survived.
5. Reviewed probe status/source: sleep completed ~60 seconds, result file exists, console write failed with `OSError [Errno 22]`. Worker stdout log empty. Cause likely lost pipe; preserve as FAILED.
6. Incident-specific archive-only script: checked gone identities before and after creating hash-verified evidence copies; returned `ARCHIVE PASS`/exit `0`, explicitly **did not clear the marker**.
7. Owner paused **before** running the clearance utility, expressly requesting this updated handback.

---

## 2. Authority, scientific boundaries, and collaboration rules

### 2.1 Ratified project documents

Always consult current actual repository copies (not old proposals with similar names):

| Repo document under `doc/` | Authority |
|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_3.md` | Owner-ratified research goals, governance, holdout |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | Owner-ratified E_1–E_62 catalogue |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` | Owner-ratified experiment/ranking/seed contracts |
| `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` | Owner-approved narrow operational changes, including 1–6 worker cap |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_2.md` | Owner-ratified scoring, prospectively frozen outputs |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_4.md` | Owner-ratified Architecture 2 / Option F, **§5C process safety** |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_1.md` | Owner-ratified P0–P2 engineering tasks; P3 separately authorised |

Owner and Claude reported that their respective v0.2/Claude v2 handovers had been committed/pushed prior to subsequent v0.3–v0.6 coordinator changes; do **not** assume the old handovers describe current safety code. The original owner-ratified ChatGPT handback v0.2 is preserved as history, not replaced in place. More recent owner decisions below prevail over stale statements in its old source/testing ledger. A user-provided fresh repository ZIP, exact committed HEAD and file hashes always take precedence over guesses from a previous archive.

### 2.2 Owner-approved safety decisions — already resolved; do NOT reopen by default

- **RATIFIED strict no-status/no-kill:** do not request coordinator termination until the experiment's identity (PID **and** creation time) is positively matched to its own status and verified owned process ancestry; missing, stale, ambiguous or unmatched status -> **no kill**. Status PID does not add members to a termination list. Even known-looking Python names or correct venv paths alone grant no authority. Global `ENABLE_PROCESS_TERMINATION = False` remains mandatory until a *separate, explicitly owner-approved destructive-testing gate*. No CLI bypass.
- **OWNER-APPROVED manual orphan clearance:** persist unresolved safety marker, fail closed at start, display clear flushed `SAFETY STOP` banner (group/worker/reason/path/instructions), stop new scheduling; if any identity remains alive/uncertain, **leave interlock active and escalate, never kill a PID by guesswork**. When every original identity is confirmed gone, archive original bytes/hash and logs, then deliberately remove exact active marker by manual, verified operation. **No automatic `--acknowledge-orphans`/bypass.**
- **Review authority:** ChatGPT makes routine low-risk engineering decisions; material process ownership/switch/kill, historical visibility/seeds/readouts, holdout, FINAL publication and dependency W-23 changes need independent Claude review and owner authorization where applicable. Bundle review by safety milestone rather than demanding repeated owner decisions on minor issues. Present clear DECIDED/RECOMMENDED/OPEN labels.
- **Process ownership:** capture under specific launched `Run_Experiment.bat` root while alive; preserve PID + creation time, positively observed ancestry, strict executable sanity checks, root only via Popen handle. No `taskkill /T /F`, name-wide `taskkill`, process-name guessing, or Windows Job Objects in current design. Prefer suspected orphan + visible warning to killing unrelated applications. Ctrl+C in a shared Windows console can independently send signals to children even with coordinator kill switch off.
- **EARLY status:** future real methods should durably publish `STARTED` as first practical operation, before heavyweight imports, to minimise uncaptured/pre-status uncertainty. Safety-critical JSON state uses temp write, flush/fsync and atomic/no-clobber publish as appropriate; safety console BEFORE/AFTER/BLOCK messages are immediately flushed. No indiscriminate fsync for bulk logging.

### 2.3 Experimental-science invariants — NOT YET IMPLEMENTED as E-methods

- Australian Powerball: 7 distinct main numbers in 1–35, plus Powerball 1–20. Historical 444-draw source CSVs from #1144 through #1587, last draw 2026-10-15, with final ten #1578–#1587 **SEALED HOLDOUT**. History CSV and drawn-order CSV are not engineering POC fixtures. Preserve allowed training horizon **strictly N−1**; no out-of-sample leakage, no testing on known holdout outcomes for tuning.
- Keep independent E_1–E_62 research methods and their negative/inconclusive results; no method is implemented or scientifically accepted merely because P0–P2 synthetic coordinator succeeds. Deterministic complete ranking; frozen TOP seven and exact WORST seven of same ranking; `TIE_SHA256_V1` readout/tie seed separate from stochastic fitted-model seed; freeze FINAL forecasts before outcome.
- `Run_Experiment.bat` is compulsory for both individual experiments and each coordinator-launched method; normal coordination begins via `Run_Coordinator.bat`. Direct Python is allowed for isolated unit/debug operations, **not an alternate normal experiment/coordinator launcher**.
- Each program can independently read immutable checksum-identified source CSV snapshots. Ordinary Python shared reads and module imports suffice; no `multiprocessing.shared_memory` or special file-locking scheme at this stage. Do not edit datasets, packages or shared Python modules mid-run. Consider shared memory only following measured performance need. The **1–6 workers** limit is the owner's currently approved coordinator cap, not a Windows/Python read limit or six-method-per-family requirement.
- `install_upgrade_dependencies_into_venv.bat` is the **sole user-maintained direct PyPI package list**; no implicit upgrade, no second active `requirements.txt`. W-23 real upgrade gate remains **NOT TESTED**.

---

## 3. Source provenance and local environment

- **Repository:** `hydra3333/analysing_perceived_randomness_in_reality`; local Win11 root `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`.
- VS Code editing/Git; Windows CMD launch; Python 3.14.8 project `.venv`; Ryzen 9 3900X and 32 GB RAM. Owner installs from assistant's repository-relative ZIP overlays deliberately; assistant has no direct access to local checkout/`.git`.
- Earliest supplied source snapshot `(4).zip`: SHA-256 `77cfd287e5d444c3eae426392c8dccc4e5cc188d1e1e5faa2e7b4ce067105b06`; ZIP archive comment `6b527627f7f98fd5cd88f4bea76e16b9cb56d372` is **not verified current Git HEAD**. That ZIP holds v0.2 coordinator `26c471e183d073db6e258a51c5b363f90d3024bc497ebebeba804a25ab187cf4`.
- Owner's later **v0.3 committed baseline**: `a2402175eaf22bf9d0293b49a6d1c91b48fe20d26866cf5d096dcfae6a95a58b`. In Claude's v0.6 review, GitHub HEAD reported `7254fc9` with v0.3 coordinator. This is **reviewer's reported point-in-time Git HEAD**, not current owner local HEAD; v0.6 was installed on the Windows working tree, and no commit/push of v0.6 is evidenced yet.
- **v0.6 installed/tested on Windows**, SHA-256 `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`; owner's `certutil` printed this hash before all v0.6 tests and timeout rehearsal. v0.6 was supplied as `Predictive_Randomness_P1P2_Orphan_Interlock_v0_6_REVIEW_CANDIDATE.zip` (one replacement coordinator, three new fake-only test scripts, handback). The ZIP's old handback correctly described its **pre-review** status and must not be treated as current acceptance ledger.
- Other key implementation files unchanged by v0.6: `Run_Experiment.bat`, `Run_Coordinator.bat`, engineering probes, imports under `src/methods/_common`, original static tests. v0.6 adds `tests/p1p2_orphan_interlock_v0_4.py`, `_v0_5.py`, `_v0_6.py`; original six-worker decoy utility is still pinned to v0.3 and **must NOT** be rerun against v0.6 until exact hash guard is re-pinned and independently reviewed.
- Source names: `src/Powerball_Experiment_Coordinator.py`, `src/methods/POC_Architecture_Probe.py`, `src/methods/POC_Coordinator_Probe.py`, `tests/p0_static_checks.py`, `tests/p1p2_static_checks.py`, `tests/p1p2_non_destructive_safety_checks.py`, `tests/p1p2_safety_regression_v0_3.py`, three orphan-interlock suites, and `tests/windows_architecture_poc_suite.py` (see watchdog warning).
- `transitory_data/poc_runs/` contains ephemeral local actual evidence and safety marker; treat ignored status cautiously. `results/architecture_poc/20261023_timeout_no_kill_coord-2a42fac2/` holds seven archived incident originals and integrity record; do not claim it was committed. `.gitattributes` pins `*.bat` CRLF.

---

## 4. Coordinator v0.6 safety contract and independent review

**Architecture:** human/CMD/VS Code -> `Run_Coordinator.bat` -> Python coordinator -> separate `Run_Experiment.bat` for EACH worker -> standalone Python engineering probe/method. Batch wrappers guard `.venv` and restore caller CMD environment; coordinator rejects direct invocation with missing/wrong `VIRTUAL_ENV`.

**v0.3:** fixed captured-member PID-reuse retirement (`departed_members`) and bounded wait for signalled descendants (fake tests; **real killing NOT tested**). v0.3's only two original `kill` invocations remain under protected disabled switch.

**v0.4/v0.5/v0.6 review history:**

- v0.4 introduced fail-closed persistent `UNRESOLVED_ORPHAN.json`, a start interlock, no-clobber durability, and stricter live member ancestry (`_member_alive(m) is True`); Claude **rejected v0.4** because exit-time orphan discovery missed survivors not handled by `stop()` (B1).
- v0.5 fixed B1 for **captured** members, emitted informative prominent console warnings and recorded marker-write failures in manifest; Claude **rejected v0.5** because uncaptured experiment PID in matching status could survive a nonzero wrapper exit (B2).
- v0.6 fixed B2: at every observed root exit, examine both captured retained members and **run-ID-matched status PID evidence**. If status PID is still live or uncertain (including missing creation time), stop launches, persist marker, display warning, mark orphan suspected; a confirmed gone/reused status PID alone is not an orphan. Status is **evidence to block, never a termination target**. Post-loop recheck catches late status. Retains existing marker; malformed/unknown marker blocks; marker-write failure flagged `marker_write_failed` and emits CRITICAL warning; no kill path added.
- **Claude v0.6 verdict:** `ACCEPT for NON-DESTRUCTIVE Windows install/testing; no switch-on or destructive test authorised`. Verified manifests/diffs, kill function identity vs v0.3, only two original kill calls, switch False, seven fake/static checks. Reviewer-reported HEAD `7254fc9`/coordinator v0.3 at review time.
- **Residual accepted:** with no captured descendant **and** no usable matching status, coordinator has insufficient evidence to detect orphan. Must not manufacture ownership or kill authority. No absolute guarantee every descendant was captured, especially without Job Objects.

**Additional improvements OPEN (not acceptance blockers for the non-destructive tests already completed):**

1. **O1:** post-loop orphan re-check may overwrite `issue` / `final_state` for a worker previously `TIMEOUT`, `INTERRUPTED` or `TERMINATION_DISABLED`, and print a second banner. Preserve original cause and suppress redundant banner after marker exists.
2. **O2:** malformed status with huge-integer create time can cause `OverflowError` during `math.isfinite`; may escape post-loop without a complete manifest. Wrap conversion, treat unknown identity conservatively as BLOCK.
3. **O3:** pre-review v0.6 handback inaccurately says `capture_owned_tree` identical to v0.3; v0.4's `is True` hardening changed it. **This v0.3 handback records that difference correctly.**
4. **O4:** add fake main-loop test verifying `stop_launches`, `orphan_suspected`, and `marker_write_failed` manifest flags.
5. **O5:** v0.6 source ZIP placed handback Markdown at repository root; consider tidying only during a planned commit, without overwriting ratified docs.

**Risk gates:** All O1/O2 process-safety changes require narrow source diff + Claude review before destructive testing. Only owner may authorise an exact test copy with `ENABLE_PROCESS_TERMINATION=True` for a separately designed destructive test; subsequently verify hash restored to unchanged reviewed v0.6 (or its independently reviewed successor). **No destructive test has been authorised or run.**

---

## 5. Evidence ledger — actual Windows observations through this checkpoint

Distinguish **owner's console observations** from fresh independent execution by this handback's author. The owner reported tests from Windows 11. No access to owner's full `.git`, runtime tree or machine was available.

| Stage | Windows observations | Status |
|---|---|---|
| P0 standalone batch/venv | Individual `Run_Experiment.bat` from active and inactive `.venv`; conflicts rejected, argument/filename guards, no-clobber sentinel, intentional exit3/abrupt exit7, synthetic fixture SHA `a853ac3545213c8f9be9355e312bf220a74fa89f240e4123aed308d983350937`. | PASS for listed cases; W-23 **NOT** done |
| v0.3 safety fix fake/static | Four suites covering P0, P1/P2 static, N2/N3/N4/N5 and v0.3 PID reuse/wait | PASS synthetic/static; no actual kill |
| v0.3 one worker and six workers plan-only | Six separate verified `cmd.exe`->`python.exe`->`python.exe` ancestry trees; all match; six-worker digest `234dab5ff151e4aa58cc77a1198cf69a50b5e63745e4a9464e5b6d42692b1b34`; no kills | PASS on v0.3 |
| v0.3 automated unrelated decoys | Three independent decoys (global Python, `.venv` Python, CMD), six-worker preview, all identities unchanged and none in SAFETY TARGET; cooperative decoy exit; utility hash pinned to v0.3. | PASS on v0.3 **only**, not yet re-pinned to v0.6 |
| v0.6 seven checks | `p0_static_checks.py`, `p1p2_static_checks.py`, `p1p2_non_destructive_safety_checks.py`, `p1p2_safety_regression_v0_3.py`, `p1p2_orphan_interlock_v0_4.py`, `_v0_5.py`, `_v0_6.py` | **PASS on owner Windows**, synthetic/fake tests only; v0.4 banner test temporary synthetic marker, not real interlock |
| v0.6 one-worker plan-only | Group `coord-a9ea0b92cd874848b0a27ef92daa5340`; match, no anomalies, `PASS successes=1/1`, digest `234dab...`, no marker, exit0 | PASS |
| v0.6 six-worker plan-only | Group `coord-d109282904f0442c93529dd588eb5c7e`; 6/6 unique roots, expected depth2 Python ancestry, matched status, no errors, same digest `234dab...`, **no marker**, exit0 | PASS |
| v0.6 batch inactive `.venv` and code page | In new ordinary CMD, direct `.venv\Scripts\python.exe src\Powerball_Experiment_Coordinator.py ...` rejected missing `VIRTUAL_ENV` with exit2; `Run_Coordinator.bat` fixture success exit0; before and after `chcp` **65001**; caller `VIRTUAL_ENV` undefined before/after | PASS for missing-env direct Python and inactive-CMD restoration; mismatched-env direct Python test not separately evidenced here |
| v0.6 manual dummy marker | Created using exclusive `xb`; new launch blocked with clear SAFETY STOP, no worker, exit2; original dummy bytes archived with SHA `665ed6c460973f92803d2af6ffc265f8b066bf6524db9f2060ae2244f4a3046a`; verified dummy cleared | PASS, deliberate dummy only |
| v0.6 real-marker rehearsal | 60-sec sleeping worker; coordinator timeout10 with switch False; verified group ancestry and no signals; **real marker created**; later launch refused exit2; process identities later all gone; status `FAILED` from late `OSError`; archive-only PASS | **PASS for safety/interlock behaviour**, **manual clearance PENDING** |
| v0.6 real process termination | None. | **NOT TESTED / NOT AUTHORISED** |

**Synthetic vs real:** The canonical-fixture digest is not a lottery forecast; v0.6 `--poc` remains engineering-only. One-vs-six equivalence under the complete scientific R2 method contract and all W-suite cases are **NOT** thereby accepted. A process ancestry **preview** is not an actual termination safety proof.

**Watchdog caveat:** `tests/windows_architecture_poc_suite.py` uses `subprocess.run(...,timeout=120)` and can kill its own launched CMD wrapper on watchdog timeout even with coordinator switch False, potentially leaving children. Do **not** run it casually or treat absence of `--with-timeout` as kill-free; review it separately. Same warning for Ctrl+C shared-console signal propagation and unreviewed short external watchdogs.

---

## 6. Next work after this emergency handback (safe order)

**IMMEDIATE:** At document creation, active real marker remains. **Do not run new experiments.** The owner asked to create/update this handback **before** using the incident-specific clearance script; that pause is intentional.

1. **Preserve this v0.3 candidate.** It is a recovery artifact written from owner transcripts and actual source files in the ChatGPT working environment. Retain owner-ratified v0.2 unchanged. Seek owner's approval for v0.3 before claiming it ratified; obtain Claude consistency review when prudent. If installed, use `doc/HANDOVER/` and commit/push by owner; **no commit implied yet**. A newer future checkout must be reconciled against this checkpoint.
2. **Preserve original operator console transcript.** Seven-file archive holds the empty worker stdout log, not necessarily full coordinator CMD output. Archive the pasted console transcript separately (or note it is held in chat) and its checksum before final project evidence closure; do not silently invent its presence in `results/`.
3. **Perform incident-specific read-only `--check`** from §1 only after the owner proceeds. Require exit0 and a clear `CHECK PASS`; if HOLD, no clearance.
4. **Deliberate `--clear-confirmed` only after approval and successful check**, retaining the archive and created clearance record; verify marker absence. Do not modify source or flip termination switch as part of this. If any original identity reappears or evidence hash differs, halt and escalate.
5. **Optional verification after clearance:** run one ordinary non-destructive canonical fixture through batch, with normal exit0, no orphan marker; do not conduct another timeout rehearsal inadvertently.
6. **Complete remaining non-destructive evidence:** re-pin/review automated three-decoy utility to v0.6 for Windows rerun; assess malformed/folder marker variants on Windows if needed (synthetic v0.4 test already covers them, actual dummy marker proven); test direct Python **mismatched** `VIRTUAL_ENV` if required; review comprehensive W-suite without risking watchdog kill. No automatic dependency upgrade.
7. **Next safety patch, separately reviewed:** resolve O1/O2, tighten main-loop fake regressions O4, properly document capture hardening; do not mix these changes into an evidence-only commit silently. Then prepare the independent destructive gate: exact source/test copy and one-line-only switch diff, before/after source hashes, kill target inventories, identity-checked independent decoys, one-worker timeout, archived console+manifest+decoy+environment+pip freeze+HEAD/source hash, and forced revert. OWNER must explicitly authorise the destructive test first; this handback gives **no permission**.
8. When non-destructive P1/P2 milestone closes, synchronise Claude's handover, exact committed source identity, and test/evidence ledger. Production acceptance/ERR-R2-02 remains conditional. P3 actual scientific E-method implementation requires separate scope and authorisation; holdout stays sealed.

### The next ChatGPT must NOT do, even if eager to help

- Do not reinterpret archive PASS as marker already cleared; do not assume original `FAILED` status is a real orphan or valid finished experiment `SUCCESS`.
- Do not call the safety script with `--clear-confirmed` without preceding `--check` and actual owner decision. Never add automatic CLI marker bypass.
- Do not run further coordinator experiments while marker remains, apart from separately approved controlled refusal demonstrations; do not delete marker to make a test pass.
- Do not set `ENABLE_PROCESS_TERMINATION=True`, use `taskkill /T /F`, kill by name/PID, run Ctrl+C tests, or force-terminate a worker without reviewed detailed plan and owner authorisation.
- Do not use a status PID as authority to kill; do not mistake a Python `.venv` path for ancestry proof.
- Do not confuse old v0.2 GitHub snapshot with installed v0.6 working tree; do not re-extract old ZIP overlays.
- Do not modify data, unseal #1578–#1587 holdout, upgrade package dependencies, claim successful predictions or run scientific E-methods.

---

## 7. Precise verification commands for future recovery (read-only unless identified)

Run from owner repository root; **do not run the actual clearance command as part of a read-only audit**:

```cmd
certutil -hashfile src\Powerball_Experiment_Coordinator.py SHA256
if exist "transitory_data\poc_runs\UNRESOLVED_ORPHAN.json" (echo SAFETY HOLD: marker exists) else (echo No active marker - VERIFY prior clearance evidence)
if exist "transitory_data\poc_runs\UNRESOLVED_ORPHAN.json" certutil -hashfile "transitory_data\poc_runs\UNRESOLVED_ORPHAN.json" SHA256
git rev-parse HEAD
git status --short
```

**Incident-specific tool hashes verified from assistant's file artifacts:**

| Utility | SHA-256 of source `.py` | Purpose/status |
|---|---|---|
| `P1P2_Read_Only_Real_Orphan_Inspection_v0_1.py` | `606f5e222a724fb2d9413ca953d770fc053e97afe20fdbe40c64b755451d554e` | Ran on owner Windows; all originals gone; HOLD only because `status=FAILED` |
| `P1P2_Archive_Real_Orphan_Evidence_v0_1.py` | `ca42d26403d139c0fcb15db504dcb39e03f735c065304bdffda4a5b897fd4681` | Ran on owner Windows, `ARCHIVE PASS` exit0; marker deliberately active |
| `P1P2_Clear_Archived_Real_Orphan_v0_1.py` | `08000be1a35c079bd4fed8ed40e17d03165466a2cf81dd0fc1bebae82ee1f0ea` | Supplied in ZIP; syntax/local simulation tested by assistant; **NOT YET RUN on owner Windows** |

These utility hashes are of the assistant's verified source artifacts. Verify extracted Windows files independently when it matters; ZIP and local tool path are not evidence of successful installation. The clearance utility is **one-incident-only**, with hardcoded group, expected archive, original marker hash and PID/creation-time identities. It is not a generic orphan-cleanup mechanism or future incident-handling tool.

**Known remaining provenance gap:** the Git revision of the owner's working tree **after** v0.6 overlay installation and the later handover commit is not independently known. Ask the owner to report `git rev-parse HEAD` at the next Git checkpoint; do not invent it.

---

## 8. Review/ratification and restart status

**This v0.3 document is a self-contained emergency recovery checkpoint.** It was prepared because the owner explicitly requested updated handover **before** manual marker clearance. Its facts are sourced from (a) the full prior ratified v0.2 Markdown; (b) assistant-accessible v0.6 exact source and handback, local tested scripts; (c) Claude's v0.4–v0.6 review messages supplied by owner; and (d) the owner's verbatim Windows console outputs through `ARCHIVE PASS`. It does **not** independently inspect the owner's current Windows filesystem or git state. It changes no coordinator code or operating-system process state.

**Open review/owner action:** Owner to inspect/ratify v0.3 (and optionally Claude to independently check scope and state). Any later clearance should result in a dated post-checkpoint status addendum or v0.4 handover stating the exact clearance observation, not an untraceable silent edit to this frozen record. Protect evidence and preserve the old handover version.

**END — v0.3 REVIEW CANDIDATE; REAL MARKER STILL ACTIVE AT HANDOVER CHECKPOINT; NO DESTRUCTIVE TEST AUTHORISED.**
