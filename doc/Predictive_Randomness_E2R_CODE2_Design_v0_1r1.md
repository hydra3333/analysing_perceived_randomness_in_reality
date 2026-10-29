# Predictive Randomness - E2R-CODE-2: wiring the contract library in, design note v0.1r1

**Document:** the design note that the owner-approved scope (S-1) requires before E2R-CODE-2's code. It states exactly which files and functions change, and answers the reviewer's E2RC-C04, the EX_036 gate watchpoint, and the reviewer's design-stage findings on v0.1 (EX_039: E2RC2-B01, B02, C01, C02, C03 and O01; Appendix A).
**Version:** v0.1r1 DRAFT for the reviewer's focused design RECHECK, 29 October 2026. Author: Claude. Ratifier: the project owner. It supersedes v0.1 (EX_038).
**Status:**
- **Authority:** this note authorises no code installation, run, data access, switch or allowlist change. The ratified design is E2R-1 v0.3r3 (`0a73c92d...a954`); nothing here changes it.
- **Speculative code:** at the owner's request, Claude has also written the code this note describes, as a candidate held in Claude's workspace (section 9).
- **Base:** commit `b846519` (register v0.12 installed). `src/` and `tests/` are unchanged since `205ae73` (E2R-CODE-1 v2 installed).

## 1. What CODE-2 does, in plain English

CODE-1 installed the contract library, but nothing uses it yet. CODE-2 makes it usable for one standalone method run at a time:

1. **A single release rule, applied before any data is read.** It checks:
   - that the method variant is released: an active `SUPPORTED` registry entry, which a run request must pin exactly;
   - that the revision and declaration match the entry;
   - that the method's folder has no `IN_DEVELOPMENT.txt`.

   Three launch points use it, with the same refusal text:
   - the new standalone contract runner;
   - the coordinator side;
   - **E_1's legacy standalone runner**, which is gated too (owner decision D2-3, 29 October 2026; E2RC2-B01).
2. **A standalone contract runner.** Every admitted run ends in a terminal record. The files are published in the specification's order:
   - the output record (C1 and/or C2), then
   - its freeze receipt, then
   - the terminal record.

   Each file is published by an atomic no-clobber primitive. Run IDs are `mg-...`, and run folders are game-namespaced.
3. **A consumption check that establishes every gate itself** (E2RC2-B02). No caller can vouch for a gate.
4. **E_1 through the contract,** by a wrapper outside E_1's folder. E_1's scientific code is untouched.
5. **One record of method status:** Package 2's per-method roster reads the installed contract registry. It is a roll-up and never an admission (E2RC2-C03).

It does **not** add any coordinated method run, real-data contract run, FINAL, IS, scoring or retirement tooling.

## 2. Exactly what changes

**New files (10):**

| File | What it holds |
|---|---|
| `src/methods/_common/contract_dispatch.py` | `dispatch_gate(request)`, `legacy_gate(game, method, variant, revision)`, `variant_released(...)`, `DispatchRefused`, the refusal text, `method_folder()` (E_2 -> E_002), `active_pins()` |
| `src/methods/_common/contract_publication.py` | `create_only()` (atomic no-clobber), `RunPublication` (C1 -> D1, C2 -> diagnostic receipt, then D2), `read_run()` (consumption), `run_disposition()`, `environment_identity()`, `new_run_id()` |
| `src/methods/_common/contract_runner.py` | `run_contract_method()`: refusals, gate, run folder, reader, task, compute, assembly, verify, publication; the new switch `ENABLE_CONTRACT_REAL_DEVELOPMENT = False`; `check_synthetic_workspace()` |
| `src/methods/Method_Contract_Runner.py` | the command-line entry, launched by the existing `Run_Experiment.bat`: `pins` and `run` |
| `src/methods/contract_adapters/__init__.py`, `e_001.py` | the method wrappers; E_1's only (section 5) |
| `src/coordinator_private/contract_coordinated_gate.py` | the coordinator side of the gate (section 6) |
| `tests/e2r_code2_fixtures.py`, `tests/test_e2r_dispatch.py`, `tests/test_e2r_runner.py` | E2R-T14, E2R-T16 at run level, and the rest of section 8 |

**Three modified files (whole-file replacements):**

| File | The change |
|---|---|
| `src/methods/E_001_Historical_Appearance_Frequency.py` | 8 inserted lines, after its orphan-marker check and before anything is created or read: `legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '1')`, refusing with the gate's text (section 5). Nothing else changes. |
| `src/methods/_common/multigame_method_registry.py` | statuses read from the installed contract registry (section 7); interface unchanged |
| `src/methods/_common/multigame_standalone_contract.py` | 4 inserted lines in `begin_synthetic`: the exact variant must be released (`variant_released`), as well as the method (section 7) |

**Unchanged:**
- **The coordinator:** `src/Powerball_Experiment_Coordinator.py` is byte-identical, including all **11 protected functions** and `coordinator_main`. **No protected function changes.**
- **E_1's scientific code:** every file in E_1's folder `src/methods/E_001/`, including `multigame_e1.py`, `e1_historical_appearance_frequency.py`, `e1_training_view.py` and `e1_standalone_contract.py`.
- **The reader and the rest of the code:** the reader; every CODE-1 module and all contract data; Package 2's other modules; `coordinator_private`'s existing modules; both `.bat` wrappers.
- **Safety settings:** the three coordinator switches (False), E_1's legacy `ENABLE_REAL_HISTORICAL_DEVELOPMENT` (unchanged), and the empty coordinated science allowlist.

## 3. The release rule (E2R-R57, E2R-T14)

**`dispatch_gate(request)`** admits a `RUN_REQUEST_V1`, or raises `DispatchRefused`. It checks, in this order:

1. The request is a valid stage-1 request (CODE-1's `validate_run_request`). This refuses reserved modes, benchmarks, targets outside the development prefix, and the `NOT_YET_SPECIFIED` placeholders.
2. The installed registry loads. The gate **loads it afresh on every call**. It never uses a cached registry or a copy a caller holds (EX_036 watchpoint).
3. A chain exists for the request's exact (game, method, variant).
4. The chain's active entry is `SUPPORTED`.
5. The request pins exactly that active entry's digest. Anything else is stale.
6. The entry's revision equals the request's: an approval for revision 1 is not an approval for revision 2.
7. The entry's declaration digest equals the request's.
8. `src/methods/E_<nnn>/IN_DEVELOPMENT.txt` does not exist (a symlink counts as present).

On admission it returns fresh, caller-owned copies of the active entry and its declaration.

**`legacy_gate(game, method, variant, revision)`** applies the same rule for E_1's legacy runner, which has no run request and so no pins: steps 2, 3, 4, 6 and 8, with the same codes and text.

**`variant_released(game, method, variant)`** is a true or false form of steps 2, 3, 4 and 8. It is for synthetic-only checks; it is not an admission.

**What the gates read:** only the installed contract data and the existence of the flag file, never draw data. When refused, nothing is created.

**The refusal text,** identical from every launch point:
`DISPATCH REFUSED: <game> <method> <variant> revision <r>: <CODE>: <detail>. No data was read.`

The codes are `INVALID_RUN_REQUEST`, `REGISTRY_INVALID`, `NO_REGISTRY_ENTRY`, `NOT_SUPPORTED`, `STALE_REGISTRY_ENTRY`, `REVISION_MISMATCH`, `DECLARATION_MISMATCH` and `IN_DEVELOPMENT_FLAG_PRESENT`.

**What admission is not:** it does not authorise a scientific run. Every other gate stays separate (E2R-R57 item 3).

## 4. The standalone contract run (E2R-R36, R38, R38A, R52)

`run_contract_method(request, compute, verify, repo_root, run_root)` does this, in order:

1. **Refusals that read no data:**
   - the unresolved-orphan marker;
   - then the new code-level switch: a `REAL_DEVELOPMENT` request is refused while `ENABLE_CONTRACT_REAL_DEVELOPMENT` is False;
   - then the dispatch gate.

   A refusal raises, creates no folder and reads nothing.
2. **The run folder:** `<run_root>/<game_id>/<method_id>/<variant_id>/<run_id>/` is created exclusively, and its parent directory is fsynced. From here on, every outcome ends in a D2 terminal record.
3. **The data:** the reader loads the pinned prefix-only `DrawView`; it verifies the pin, the ledger and INIT. The receipt provenance (`ledger_sha256`, `init_record_sha256`) is then hashed from those files, with the reader's plain-file rule. Any failure gives D2 `VALIDATION_FAILURE` (`DATA_ADMISSION_REFUSED`).
4. **The computation:** CODE-1 builds the frozen `MethodTask`, and `compute(task, view)` runs once. An exception gives `RUNTIME_FAILURE`, or `NUMERIC_INVALID` for a non-finite or out-of-range number.
5. **Assembly and verification:** CODE-1 assembles C1 when the request's product is the forecast product, and C2 when the declaration has a diagnostic schema. Then the method's `verify()` checks them.
   - An invalid output gives `VALIDATION_FAILURE` (`CONTRACT_REFUSED_OUTPUT`), or `NUMERIC_INVALID`.
   - The empty-target rule is below (E2RC2-C02).
6. **Publication:** C1 is written, read back and validated; then D1. C2 and its diagnostic receipt follow the same pattern. Last, D2 `SUCCESS` names the receipts.
   - A publication failure or an interruption gives D2 `RUNTIME_FAILURE`, naming **no** receipt. Receipts already issued stay on disk, unnamed and never consumable.
   - If even D2 cannot be written, the exception propagates. There is then no D2, so nothing is consumable.

**Atomic no-clobber publication (E2RC2-C01).** `create_only(path, bytes)`:
1. writes the bytes to a new temporary file owned by this call (`.<name>.part-<uuid>`, exclusive create), then flushes and fsyncs it;
2. publishes it with **`os.link(temporary, path)`**. Creating a hard link is atomic, and it fails with `FileExistsError` if anything already has the name, on POSIX and on NTFS. So a published file is never replaced, a reader never sees a partial file, and of several concurrent writers exactly one wins;
3. removes only its own temporary file, then fsyncs the directory on POSIX. Windows has no directory fsync; NTFS journals the link.

There is no `exists()` pre-check and no rename anywhere. A filesystem that cannot make hard links refuses publication (`RuntimeError`, nothing published, fail closed); nothing falls back to a rename. Nothing else is ever deleted, moved, retried or recovered.

**The empty target (E2RC2-C02).** `assemble_forecast` returns no record only for a **valid** output with no available TOP or WORST and sufficient history. Any invalid output raises instead. So, for a request whose product is the forecast product:
- **No ticket, and no diagnostic declared:** this is the legitimate empty target of section 7.4. Nothing is published but D2. The frozen D2 vocabulary has no outcome for it (no `SUCCESS` without receipts), so D2 records `VALIDATION_FAILURE` with the fixed reason prefix `NO_TICKET_NO_DIAGNOSTIC:`. **`run_disposition(terminal)` classifies such a run as `DIAGNOSTIC_ONLY`:** unscored and valid, never a failure. Reports must count it with that function, never as a scientific invalidity. Every other non-SUCCESS run is `FAILED`. No change to the D2 vocabulary is made or implied; a later schema version could add an explicit outcome.
- **No ticket, and a diagnostic declared:** C2 is published with its receipt and D2 `SUCCESS` ("PUBLISHED: DIAGNOSTIC_ONLY").
- **A declared diagnostic missing (and no ticket):** the method owed its C2, so this is an invalid output, `VALIDATION_FAILURE` (`CONTRACT_REFUSED_OUTPUT`), `FAILED`.
- **Insufficient history:** the C1 records `INSUFFICIENT_HISTORY`, with every TOP and WORST unavailable. It is published with D1 and D2 `SUCCESS` ("PUBLISHED: INSUFFICIENT_HISTORY"). It is unscored, because it has no ticket, and never conflated with `PREDICTION_AVAILABLE`. The D2 outcome `INSUFFICIENT_HISTORY` is not used in stage 1.

**Consumption (E2RC2-B02).** `read_run(folder)` is the consumption check for a standalone run folder. It has no gate or declaration parameter: it establishes every gate itself, from current evidence, and fails closed. For each output found, it requires:
- **No orphan marker:** the global unresolved-orphan marker is absent, checked on every call.
- **A valid SUCCESS terminal record** that names the output's receipt (CODE-1's `consumable()`).
- **A standalone run:** a `COORDINATED` run's group and exit-receipt gates have no evidence path in CODE-2, so it is **never** consumable here (`COORDINATED_EVIDENCE_NOT_AVAILABLE`). The future coordinated package brings its own evidence check.
- **A matching folder:** the folder is `<game>/<method>/<variant>/<run_id>` of the records it holds.
- **The installed declaration:** the one with the record's declaration digest, fetched afresh. It is never supplied by the caller.
- **The installed admitting entry:** the receipt's registry entry is in that variant's installed chain, is `SUPPORTED`, and names the same revision and declaration.

Only then does it call `consumable()`. The `gates_pass` argument of that low-level CODE-1 function is set to True by `read_run` alone, after the checks above; it is never exposed. Nothing is repaired, moved or deleted.

**Receipt fields:**
- `environment_identity`: Python, NumPy and psutil versions, OS name and build, and a digest of the installed package list;
- `execution_path`: `STANDALONE`;
- `window` and `cohort_id`: null;
- `frozen_at_utc`: the local clock in CODE-1's strict UTC form (informational only).

**The command line:** `Run_Experiment.bat Method_Contract_Runner.py pins|run ...`.
- **Synthetic runs:** need `--workspace DIR` of invented masters. The folder must not be the project root, or inside its data, results, code or record folders. Runs publish under `DIR/contract_runs/`.
- **Real development runs:** refused by the switch.
- **Exit codes:** 0 SUCCESS, 1 other terminal outcome, 2 refused.
- **What it prints:** status lines only.

**Diagnostic-only requests (E2RC2-O01).** The command line always requests the forecast product of the run mode. This is a **launcher capability limit of CODE-2, not a limit of the contract**: the shared runner supports `DIAGNOSTIC_OUTPUT` requests, which publish C2 only, and a test proves it. The command-line option comes with the first owner-scoped method package that declares a diagnostic record.

## 5. E_1 (reviewer's E2RC-C04, option (a); E2RC2-B01, owner decision D2-3)

**Through the contract.**
- **Where the wrapper lives:** `src/methods/contract_adapters/e_001.py`, outside E_1's folder. It calls E_1's own reviewed `E_001.multigame_e1.forecast` unchanged.
- **Proof of identity at run time:** before anything is published, `verify()` recomputes E_1's own result and requires the contract record to equal it **label for label** (scores, ranking, TOP and WORST, per barrel). A difference stops the run.
- **What E_1 can run on:** E_1's multi-game function accepts only `SYNTHETIC_CONTRACT_TEST` data, so E_1 contract runs are synthetic-only, independently of the new switch.

**The legacy standalone runner is gated (owner decision D2-3, 29 October 2026).**
- **What it is:** `E_001_Historical_Appearance_Frequency.py` stays the frozen legacy path for the legacy `e1-` runs, the `E1_*` schemas, the legacy goldens and the 1577 forecast-only regression (E2R-R50, R52).
- **The change:** it is no longer outside the release rule. Immediately after its existing orphan-marker check, and before it creates a run folder, imports E_1's loader or reads any source, it calls `legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '1')`. On refusal it exits with argparse's error code 2 and the gate's text.
- **What it applies to:** both its modes, synthetic-contract and historical-development.
- **While E_1 stays released** (today's registry), the runner behaves exactly as before: same arguments, same outputs, same goldens. So it can still read the real development masters under its existing, owner-accepted `ENABLE_REAL_HISTORICAL_DEVELOPMENT` gate (D3 boundary, holdout sealed) and write historical `E1_*` records.
- **If E_1's active entry stops being SUPPORTED, or `src/methods/E_001/IN_DEVELOPMENT.txt` appears,** it refuses before anything is created or read. Tests cover both, in both modes.
- **It is not an exception:** it uses the normal rule without pins, because it has no run request. It never writes contract records.
- **E_1's revision:** E_1's scientific modules are untouched, and its outputs are byte-identical whenever it runs, so Claude recommends that **E_1 stays revision 1**. The change is a refusal before any computation, not a behaviourally relevant change to what E_1 computes (E2R-R14A). Claude asks the reviewer to confirm. No structural exception is used or needed.

## 6. The coordinator side

- **There is no coordinated contract-method dispatch today.** Scientific coordination is switched off, and the coordinated science allowlist is empty.
- **What CODE-2 adds:** `coordinator_private.contract_coordinated_gate.gate_coordinated_contract_request(request)`, an **intentionally rejecting entry point** for future integration. It is not yet called from `coordinator_main`.
  - It applies **exactly** the standalone gate: same rule, same text for every gate refusal.
  - It then refuses every admitted request with `COORDINATED_CONTRACT_DISPATCH_NOT_ENABLED`.
  - It reads no data, starts nothing and writes nothing.
- **What does not change:** the coordinator file and its protected functions.
- **What comes later:** a real coordinated run, with its evidence-based consumption check, is a separate, reviewed package.

## 7. Method status: a roll-up, never an admission (E2RC2-C03)

`multigame_method_registry.method_status(game, method)` derives each method's status from the installed contract registry, read on every call. The rule:
- **SUPPORTED:** some variant has an active `SUPPORTED` entry for that game, and the method has no flag;
- **UNSUPPORTED_FOR_GAME:** every active entry says so;
- **FORMULA_OPEN:** otherwise.

Today this equals the earlier fixed roster: E_1 SUPPORTED, and E_2..E_62 FORMULA_OPEN.

**It is an informational roll-up. A SUPPORTED roll-up never by itself grants a run, never selects a variant, and never replaces the exact entry pin.**
- **Normal method dispatch** uses `dispatch_gate` (exact variant, revision, declaration and pinned entry).
- **Package 2's consumers** each add an exact check of their own:
  - **the launch specification and the worker handshake:** only E_1's registered synthetic probe variant;
  - **`begin_synthetic`:** now also requires the exact variant to be released (`variant_released`);
  - **`registered_scientific_binding`:** the coordinated science allowlist is empty, so it always refuses.

**Proof with mixed variants** (not only today's snapshot):
- **A new method:** E_2 with variant A `SUPPORTED` and variant B `FORMULA_OPEN`. The roll-up is SUPPORTED, but the gate refuses B. A's pin cannot admit B. Every Package 2 consumer refuses both variants of E_2.
- **An extra E_1 variant:** an unreleased E_1 variant is refused by the gate and by `begin_synthetic`.
- **A withdrawn E_1 variant:** E_1's `FULL_HISTORY_RAW_COUNTS_V1` is withdrawn (entry 2 `FORMULA_OPEN`) while another E_1 variant stays SUPPORTED. The roll-up still says SUPPORTED, yet `legacy_gate`, `dispatch_gate` and `begin_synthetic` all refuse the withdrawn variant.

## 8. Tests and proof

**New tests (47):**
- **`tests/test_e2r_dispatch.py` (18): E2R-T14.**
  - **The truth table:** status (SUPPORTED, FORMULA_OPEN, UNSUPPORTED_FOR_GAME) times flag, through both contract launch points, with identical texts.
  - **Entries:** missing, stale and mismatched entries; revision-1 approval against revision-2 code; the placeholders; installed E_1 admitted and E_2..E_62 refused.
  - **Fresh fetch:** the gate fetches afresh on every call.
  - **Refusal:** a refusal reads no data and creates no folder; the command-line launcher prints only the refusal.
  - **The release transition.**
  - **The roster:** it equals the old table, and a flag makes it FORMULA_OPEN.
  - **Static checks.**
  - **Mixed variants** (section 7; 2 tests).
  - **The legacy runner** (3 tests): withdrawn or flagged E_1 refused before anything, in both modes, with the loader and the run start patched to fail if reached; released E_1 admitted.
- **`tests/test_e2r_runner.py` (29): E2R-T16 at run level.**
  - **E_1 through the contract:** both games, three targets each; the identity check; E_1 refuses non-synthetic data.
  - **Publication and interruption:** publication order; create-only and one folder per run; interrupted after D1; failure after a receipt; C1 and C2 both published; method, NaN and verify failures; a bad pin; the orphan marker and the switch; the workspace rule.
  - **Run-level T03 and hygiene; the command line end to end.**
  - **Consumption (B02; 5 tests):** no caller-supplied gate or declaration parameter exists; an active orphan marker blocks consumption, and lifting it restores it; a COORDINATED run is never consumable; the declaration and admitting entry must be installed (a receipt naming an unknown entry is refused); the folder must match its records.
  - **The empty target (C02; 5 tests):** a valid empty target gives `DIAGNOSTIC_ONLY`, not failure; a missing declared diagnostic is `FAILED`; no ticket with a diagnostic publishes C2 only; insufficient history is published with no ticket; and the library's diagnostic-only product (O01).
  - **No-clobber publication (C01; 4 tests):** an existing target is refused and untouched; a dangling-symlink target is refused (skipped where the platform disallows symlinks); 12 concurrent writers, exactly one wins, and no temporary file is left; no hard links means no publication.

**The whole suite:** 185 tests (84 earlier, 54 CODE-1 and 47 CODE-2) pass on Linux, Python 3.13.17 and 3.15.0b4. The suite runner allows, besides the two existing symlink skips, CODE-2's one dangling-symlink skip, which is expected on Windows without symlink rights.

**Mutation checks (E2R-1 13, for T14 and T16, and each EX_039 correction): 18 planted defects, each caught.**
- **The gate:** it ignores the flag, admits FORMULA_OPEN, accepts a stale pin, or ignores a declaration mismatch.
- **Reading and the coordinator:** the runner reads data before the gate; the coordinator skips the shared gate.
- **Caching:** the gate trusts a cached registry.
- **Terminal records:** a failed run names its receipts; a failure after a receipt is recorded as SUCCESS.
- **Publication:** publication renames over an existing file; a run folder can be reused.
- **Consumption:** it ignores the orphan marker, accepts a coordinated run, or trusts any admitting entry.
- **The legacy runner:** it skips the gate.
- **The empty target:** a missing declared diagnostic counts as an empty target.
- **Package 2:** `begin_synthetic` trusts the roll-up.

**Review and install:**
- **Proposed review:** HIGH tier with RECHECK. The always-review subjects touched are dispatch and orchestration, publication and consumption, and orchestration-only provenance. No reader, coordinator, protected function, switch or allowlist is touched.
- **Install:** the usual code discipline.
  - PRE checks that each of the three replaced files equals its base blob.
  - POST checks that each equals its reviewed bytes, and that every new file is exact.
  - Then COMMITTED; the owner's Windows suite runs before the commit.

## 9. The speculative candidate

Claude has revised the candidate code to this note, with its tests, mutation checks and an install package built and run end to end on Linux. It is held in Claude's workspace, not installed. If the reviewer passes this design unchanged, the candidate goes to the HIGH-tier code RECHECK.

## 10. Owner decisions

- **D2-1 (coordinator scope):** CODE-2 covers the standalone path. The coordinator side gets only the rejecting entry point. Reviewer: supported in principle. **Awaiting the owner, after this recheck.**
- **D2-2 (the switch):** `ENABLE_CONTRACT_REAL_DEVELOPMENT = False`, a fourth switch that stays False. Reviewer: supported. **Awaiting the owner.**
- **D2-3 (the legacy runner): DECIDED by the owner, 29 October 2026.** The legacy runner gets the release check (section 5), not an exception. Open for the reviewer: confirmation that E_1 stays revision 1.
- **D2-4 (the roster):** it reads the installed registry, as a roll-up only (section 7). Reviewer: supported, subject to C03. **Awaiting the owner.**

Out of scope, and unchanged: coordinated method runs, real-data contract runs, FINAL, IS, scoring, retirement (CODE-3), any change to E_1's scientific code, and any change to a protected function, switch or allowlist.

## Appendix A. EX_039 findings and their resolution

| Finding | Class | Resolution in v0.1r1 | Where | Proof |
|---|---|---|---|---|
| E2RC2-B01 legacy runner outside the release rule | BLOCKER, RECHECK | Owner decision D2-3: the legacy runner calls `legacy_gate` before anything is created or read, in both modes; it is not an exception; E_1's scientific code is untouched | sections 2, 3, 5, 10 | 3 tests, 1 mutation |
| E2RC2-B02 caller-supplied `gates_pass` | BLOCKER, RECHECK | `read_run(folder)` has no gate or declaration parameter. It checks the orphan marker now, standalone-only, the folder, the installed declaration and the installed SUPPORTED admitting entry, then `consumable()`; COORDINATED is never consumable in CODE-2 | section 4 | 5 tests, 3 mutations |
| E2RC2-C01 rename is not no-clobber | CORRECTION, RECHECK | `create_only` publishes with `os.link` (atomic, fails on any existing name, POSIX and NTFS), with fsync of file and directory; only its own temporary file is removed; no rename, no `exists()` pre-check; fail closed without hard links | section 4 | 4 tests (including 12 concurrent writers), 1 mutation |
| E2RC2-C02 empty target versus invalid output | CORRECTION, RECHECK | A valid empty target (no ticket, no declared diagnostic) gets the reason `NO_TICKET_NO_DIAGNOSTIC:` and `run_disposition() = DIAGNOSTIC_ONLY`; a missing declared diagnostic is invalid; no-ticket-with-C2 is SUCCESS DIAGNOSTIC_ONLY; INSUFFICIENT_HISTORY is unscored; the D2 vocabulary is unchanged | section 4 | 5 tests, 1 mutation |
| E2RC2-C03 roll-up is not admission | CORRECTION, RECHECK | The roster is documented as a roll-up only; `begin_synthetic` now requires the exact variant (`variant_released`); a proof with mixed and withdrawn variants across every Package 2 consumer and both gates | sections 2, 7 | 2 tests, 1 mutation |
| E2RC2-O01 diagnostic-only CLI | OPTIONAL | Labelled as a CODE-2 launcher limit, not a contract limit; the shared runner's C2-only path is tested; the option comes with the first method declaring a C2 | section 4 | 1 test |

**Also changed from v0.1:**
- The base is now `b846519`.
- The gate's registry and method-folder roots are read at call time, so tests can point them at temporary copies.
- The test count is 47 (was 28), and the mutation count is 18 (was 12).
