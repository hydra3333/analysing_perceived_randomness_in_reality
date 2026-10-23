# E_1 U-view standalone development contract v0.2 - REVIEW CANDIDATE

Date: 23 October 2026. Status: synthetic-reviewed candidate only; owner may separately enable real historical development after Claude review and Windows testing. Governing documents: ratified Architecture v0.5 section 5C and section 6.1, R2/R3, owner-ratified D1/D2/D3 and failed-group firewall.

## Status contract resolution (Claude blocker)

The standalone method uses **the same** shared `ProbeStatus` in `_common/experiment_runtime_status_and_resources.py` that the coordinated POC uses. Identical schema `ENGINEERING_POC_STATUS_V1`. The helper now optionally accepts `identity` for STARTED and `terminal_fields` for completion; the POC's existing constructor and finish calls remain compatible. STARTED includes actual os.getpid, psutil process creation time, actual sys.prefix, started_utc, run ID, case, target, mode, method and variant. Missing creation identity raises after recording STARTED; no PASS. Terminal SUCCESS/FAILED includes elapsed_seconds from perf_counter, cpu_time_seconds from process_time, peak_working_set_bytes with peak_field (`peak_wset`/`peak_rss`/UNAVAILABLE), finished_utc and canonical/training SHA-256 if successful. Durable status write uses the existing shared publication utility. Status hash is committed to the standalone manifest.

## Single executable per E-number

`src/methods/E_001_Historical_Appearance_Frequency.py` is the only executable for E_1. Previously named `E_1_Historical_Appearance_Frequency_Run.py` and `E_1_Historical_Appearance_Frequency.py` must NOT be installed as second executables. The latter's accepted v0.3 pure mathematics is copied byte-identically to `_common/e1_historical_appearance_frequency_v0_3.py`. `method_id` remains E_1 inside scientific results as previously ratified; executable identity is E_001 for Architecture 6.1. No changes to E_1 ranking mathematics.

## Modes, files, firewall

The real-mode switch remains hard False; the proposed one-line True change is a separate review-only diff. Real mode must read only the approved nonsymlink U CSV below source_data, use strict N-1 target 1145..1577 (holdout sealed) and never call coordinator or rely on timeouts. Synthetic data and development output use transitory_data, with separate digest domains. `canonical_result.json` is xb+fsync; last publication is a PASS manifest only after SUCCESS status with binding hashes. No result from FAIL/orphan-suspected groups may be consumed. For real consumers, the canonical unresolved-orphan marker is ALWAYS checked irrespective of arguments. Failure including KeyboardInterrupt -> FAILED with `failure_reason=INTERRUPTED` and non-PASS manifest if possible; STARTED-only remains fail-closed after abnormal hard exit.

Standalone's PASS is a worker declaration; unlike a coordinator or FINAL publication, it does **not** claim verified wrapper exit. Claude accepted this residual only for standalone historical development. For coordinator and FINAL acceptance, an independently authored post-wrapper-exit receipt with observed exit code, exit time and root identity remains required, is outside this scope, and may not be inferred from this manifest.

## Review gates

1. Claude independently verifies status schema and fields, POC helper backwards compatibility, final identities and CPU/peak measurement; checks no alternate E_001 method executable.
2. Claude reviews the one-line real gate switch change separately and the Windows synthetic procedure through `Run_Experiment.bat` (no wrapper modification). No real run is implied.
3. Owner separately authorises first real U-data standalone historical run (source snapshot and target), after Windows synthetic PASS. The holdout, FINAL, termination and destructive tests remain forbidden.

**DECIDED:** reusable identity/terminal-fields extension, one E_001 launcher, early durable STARTED, failure and result firewall; names and locations of ignored dev outputs.
**RECOMMENDED for owner:** the exact first real historical target and source snapshot, and the one-line real gate after independent review. **OPEN:** independently observed coordinator/FINAL exit receipts; Windows acceptance; final scorer integration; P2 coordinator v0.7.
