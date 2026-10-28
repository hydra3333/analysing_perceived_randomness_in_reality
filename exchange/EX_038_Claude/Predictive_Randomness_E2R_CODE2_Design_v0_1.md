# Predictive Randomness - E2R-CODE-2: wiring the contract library in, design note v0.1

**Document:** the design note that the owner-approved scope (S-1) requires before E2R-CODE-2's code. It states exactly which files and functions change, and answers the reviewer's E2RC-C04 and the EX_036 gate watchpoint.
**Version:** v0.1 DRAFT for the reviewer's design-stage review, 29 October 2026. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** this note authorises no code installation, run, data access, switch or allowlist change. The ratified design is E2R-1 v0.3r3 (`0a73c92d...a954`); nothing here changes it.
- **Speculative code:** at the owner's request, Claude has also written the code this note describes, as a candidate held in Claude's workspace (section 9).
- **Base:** commit `205ae73` (E2R-CODE-1 v2 installed and verified).

## 1. What CODE-2 does, in plain English

CODE-1 installed the contract library, but nothing uses it yet. CODE-2 makes it usable for one standalone method run at a time:

1. **A single dispatch gate.** Both the standalone runner and the coordinator side use it. Before any data is read, it checks:
   - that the method variant is released: an active `SUPPORTED` registry entry that the request pins exactly;
   - that the revision and declaration match the entry;
   - that the method's folder has no `IN_DEVELOPMENT.txt`.
2. **A standalone contract runner.** It runs an admitted method, and every run ends in a terminal record. The files are published in the specification's order:
   - the output record (C1 and/or C2), then
   - its freeze receipt, then
   - the terminal record.

   Run IDs are `mg-...`, and run folders are game-namespaced.
3. **E_1 through the contract,** by a wrapper outside E_1's folder. E_1's own code is untouched.
4. **One record of method status:** Package 2's per-method roster now reads the installed contract registry.

It does **not** add any coordinated method run, real-data run, FINAL, IS, scoring or retirement tooling.

## 2. Exactly what changes

**New files (10):**

| File | What it holds |
|---|---|
| `src/methods/_common/contract_dispatch.py` | `dispatch_gate(request)`, `DispatchRefused`, the refusal text, `method_folder()` (E_2 -> E_002), `active_pins()` |
| `src/methods/_common/contract_publication.py` | create-only writes, `RunPublication` (C1 -> D1, C2 -> diagnostic receipt, then D2), `environment_identity()`, `new_run_id()`, `read_run()` (consumption) |
| `src/methods/_common/contract_runner.py` | `run_contract_method()`: refusals, gate, run folder, reader, task, compute, assembly, verify, publication; the new switch `ENABLE_CONTRACT_REAL_DEVELOPMENT = False`; `check_synthetic_workspace()` |
| `src/methods/Method_Contract_Runner.py` | the command-line entry, launched by the existing `Run_Experiment.bat`: `pins` and `run` |
| `src/methods/contract_adapters/__init__.py`, `e_001.py` | the method wrappers; E_1's only (section 5) |
| `src/coordinator_private/contract_coordinated_gate.py` | the coordinator side of the gate (section 6) |
| `tests/e2r_code2_fixtures.py`, `tests/test_e2r_dispatch.py`, `tests/test_e2r_runner.py` | E2R-T14 and E2R-T16 at run level, and the rest of section 8 |

**One modified file:** `src/methods/_common/multigame_method_registry.py`, a whole-file replacement (section 7). Its interface (`method_status`, `all_statuses`, the three status constants) is unchanged.

**Unchanged:**
- **The coordinator:** `src/Powerball_Experiment_Coordinator.py` is byte-identical, including all **11 protected functions** and `coordinator_main`. **No protected function changes, so no owner decision on them is needed.**
- **The reader and E_1:** the reader; E_1's folder `src/methods/E_001/` and its entry file `E_001_Historical_Appearance_Frequency.py`.
- **The rest of the code:** every CODE-1 module and all contract data; Package 2's other modules; `coordinator_private`'s existing modules; both `.bat` wrappers.
- **Safety settings:** the three coordinator switches (False) and the empty coordinated science allowlist.

## 3. The dispatch gate (E2R-R57, E2R-T14)

`dispatch_gate(request)` admits a `RUN_REQUEST_V1`, or raises `DispatchRefused`. It checks, in this order:

1. The request is a valid stage-1 request (CODE-1's `validate_run_request`). This refuses, among other things, reserved modes, benchmarks, targets outside the development prefix, and the `NOT_YET_SPECIFIED` placeholders.
2. The installed registry loads. The gate **loads it afresh on every call**. It never uses a cached registry or a copy a caller holds (the reviewer's EX_036 watchpoint).
3. A chain exists for the request's (game, method, variant).
4. The chain's active entry is `SUPPORTED`.
5. The request pins exactly that active entry's digest. A pin to an earlier or later entry is stale.
6. The entry's revision equals the request's: an approval for revision 1 is not an approval for revision 2.
7. The entry's declaration digest equals the request's.
8. `src/methods/E_<nnn>/IN_DEVELOPMENT.txt` does not exist (a symlink counts as present).

On admission it returns fresh, caller-owned copies of the active entry and its declaration, taken from the registry it just loaded. What it reads:
- **What it reads:** only the installed contract data and the existence of that flag file. It never reads a master, ledger or any draw data.
- **When refused:** nothing is created.
- **The refusal text,** identical from both launchers:
  `DISPATCH REFUSED: <game> <method> <variant> revision <r>: <CODE>: <detail>. No data was read.`

  The code is one of `INVALID_RUN_REQUEST`, `REGISTRY_INVALID`, `NO_REGISTRY_ENTRY`, `NOT_SUPPORTED`, `STALE_REGISTRY_ENTRY`, `REVISION_MISMATCH`, `DECLARATION_MISMATCH` or `IN_DEVELOPMENT_FLAG_PRESENT`.
- **What admission is not:** it does not authorise a scientific run. Every other gate stays separate (E2R-R57 item 3).

## 4. The standalone contract run (E2R-R38, R38A, R52)

`run_contract_method(request, compute, verify, repo_root, run_root)` does this, in order:

1. **Refusals that read no data:**
   - the unresolved-orphan marker (the same path as E_1's standalone runner);
   - then the new code-level switch: a `REAL_DEVELOPMENT` request is refused while `ENABLE_CONTRACT_REAL_DEVELOPMENT` is False;
   - then the dispatch gate.

   A refusal raises, creates no folder and reads nothing.
2. **The run folder:** `<run_root>/<game_id>/<method_id>/<variant_id>/<run_id>/` is created **exclusively**. From here on, every outcome ends in a D2 terminal record.
3. **The data:** the reader loads the pinned prefix-only `DrawView` (it verifies the pin, the ledger and INIT, as today). The receipt's provenance (`ledger_sha256`, `init_record_sha256`) is then hashed from those same files, with the reader's plain-file rule. Any failure here gives D2 `VALIDATION_FAILURE` (`DATA_ADMISSION_REFUSED`).
4. **The computation:** CODE-1 builds the frozen `MethodTask`, and the method's `compute(task, view)` runs once.
   - An exception gives `RUNTIME_FAILURE`, or `NUMERIC_INVALID` when the error is a non-finite or out-of-range number.
5. **Assembly and verification:** CODE-1 assembles C1 when the request's product is the forecast product, and C2 when the declaration has a diagnostic schema. Then the method's `verify(task, view, c1, c2)` checks them.
   - A refusal by either gives `VALIDATION_FAILURE`, or `NUMERIC_INVALID` for a number error.
   - No record at all (no available TOP or WORST, and no C2) gives `VALIDATION_FAILURE` (`NO_RECORD`).
6. **Publication:**
   - C1 is written create-only, read back and validated; then D1 is written. C2 and its diagnostic receipt follow the same pattern.
   - Last, D2 `SUCCESS` names the receipts.
   - If publication fails, or the run is interrupted (`KeyboardInterrupt`), D2 says `RUNTIME_FAILURE` and names **no** receipt. Receipts already issued stay on disk, unnamed, and are never consumable.
   - If even D2 cannot be written, the exception propagates and the output is not consumable, because there is no D2.

**How files are written:** create-only, like the coordinator's `save_new`. Each file goes to a new `.part-` name, is flushed and fsynced, then renamed onto a name that must not exist; it is never replaced. Nothing anywhere deletes, moves, quarantines, retries, kills or recovers.

**Receipt fields:**
- `environment_identity`: Python, NumPy and psutil versions, OS name and build, and a digest of the installed package list;
- `execution_path`: `STANDALONE`;
- `window` and `cohort_id`: null;
- `frozen_at_utc`: the local clock in CODE-1's strict UTC form (informational only).

**Consumption:** `read_run(folder, declaration, gates_pass)` applies CODE-1's `consumable()` to each output found. `gates_pass` is the caller's result for every existing group and firewall gate.

**The command line:** `Run_Experiment.bat Method_Contract_Runner.py pins|run ...`.
- **Synthetic runs:** need `--workspace DIR`, a folder of invented masters that is neither the project root nor inside its data, results, code or record folders. They publish under `DIR/contract_runs/`.
- **Real development runs:** would publish under `transitory_data/contract_runs/`, but they are refused by the switch.
- **Exit codes:** 0 SUCCESS, 1 other terminal outcome, 2 refused.
- **What it prints:** status lines only, never data.

**Choices made within E2R-1, for the reviewer:**
- **(a) Insufficient history:** an `INSUFFICIENT_HISTORY` C1 (sufficient-history rules decided by the contract) is published with D1, and D2 is `SUCCESS` ("PUBLISHED: INSUFFICIENT_HISTORY"). The record itself carries its status, and consumers read it. The D2 outcome `INSUFFICIENT_HISTORY` is therefore not used in stage 1.
- **(b) No record:** "no record" is recorded as `VALIDATION_FAILURE`, so that the run is visibly not a success.
- **(c) Product kind:** the runner always requests the forecast product of the run mode. A diagnostic-only request (`DIAGNOSTIC_OUTPUT`) is supported by the library but has no command-line option yet.

## 5. E_1 through the contract (reviewer's E2RC-C04): option (a)

- **Where the wrapper lives:** `src/methods/contract_adapters/e_001.py`, **outside** E_1's folder. It calls E_1's own reviewed multi-game function, `E_001.multigame_e1.forecast`, unchanged, and turns its counts into a contract `MethodOutput` (`ScoredRanking` per barrel).
- **Proof of identity at run time:** before anything is published, `verify()` recomputes E_1's own result and requires the contract record to equal it **label for label**: the scores, the ranking, TOP and WORST, per barrel. A difference stops the run with `VALIDATION_FAILURE`. So a published contract record can never differ from what E_1 itself computes.
- **The goldens:** E_1's legacy goldens and CODE-1's E2R-T09 equality test still pass.
- **E_1's revision:** no E_1 byte changes, so **E_1 stays revision 1 with no exception needed**. NAMES-1's and E1-ALIGN's structural exceptions are not used.
- **What E_1 can run on:** E_1's own multi-game function accepts only `SYNTHETIC_CONTRACT_TEST` data. So E_1 contract runs are synthetic-only until a reviewed E_1 change says otherwise. That is a second, independent block on real runs.
- **The legacy runner:** E_1's legacy standalone runner (`E_001_Historical_Appearance_Frequency.py`, `e1-` run IDs and `E1_*` schemas) is unchanged. It remains the frozen legacy path that E2R-R50 and R52 keep for the legacy goldens and the 1577 forecast-only regression. New work uses the contract runner. Gating the legacy runner as well would change E_1's entry file; that is owner decision D2-3.

## 6. The coordinator side

- **There is no coordinated contract-method dispatch today.** Scientific coordination is switched off, the coordinated science allowlist is empty, and coordinated publication needs the exit-receipt joins that a future package must design.
- **What CODE-2 adds:** `coordinator_private.contract_coordinated_gate.gate_coordinated_contract_request(request)`, the single entry point any future coordinated contract dispatch must use.
  - It applies **exactly** the standalone gate, so a request the gate refuses gets the same rule and the same text from both launchers (E2R-T14).
  - A request the gate admits is then refused with `COORDINATED_CONTRACT_DISPATCH_NOT_ENABLED`.
  - It reads no data, starts nothing and writes nothing.
- **What does not change:** the coordinator file and its protected functions.
- **What comes later:** replacing that final refusal with a real coordinated run is a separate, reviewed package (owner decision D2-1).

## 7. One record of method status (Package 2's roster)

`multigame_method_registry.method_status(game, method)` now derives each method's status from the installed contract registry, loaded on every call. The rule:
- **SUPPORTED:** one of the method's variants has an active `SUPPORTED` entry for that game, and the method has no `IN_DEVELOPMENT.txt`;
- **UNSUPPORTED_FOR_GAME:** every active entry says so;
- **FORMULA_OPEN:** otherwise.

With today's data, this gives exactly the earlier fixed roster: E_1 SUPPORTED, and E_2..E_62 FORMULA_OPEN, in both games (tested). Package 2's synthetic plumbing paths, which use it, behave as before.

What it changes is that a future release (a SUPPORTED entry appended, the flag removed) shows up in one place, not two. The roster stays per method; normal dispatch uses the variant-exact gate (owner decision D2-4).

## 8. Tests and proof

**New tests (28):**
- **`tests/test_e2r_dispatch.py` (13): E2R-T14.**
  - **The truth table:** status (SUPPORTED, FORMULA_OPEN, UNSUPPORTED_FOR_GAME) times flag (absent, present), through both launchers, with identical refusal texts.
  - **Entries:** missing, stale and mismatched entries; a revision-1 approval against revision-2 code; the placeholders; installed E_1 admitted and E_2..E_62 refused.
  - **The watchpoint:** the gate fetches afresh each call, and caller-mutated copies change nothing.
  - **Reading and creating nothing:** a refusal reads no data (the reader is patched to fail if called, and no file under the workspace is opened) and creates no folder.
  - **The launcher:** the command-line launcher prints only the refusal and exits 2.
  - **The release transition:** D and entry 1 `FORMULA_OPEN` installed with the flag; entry 2 `SUPPORTED` appended, still refused while the flag exists; the flag removed, then admitted and run. Entry 1 and D are byte-unchanged, the record validates under D, and stale or mismatched pins are refused.
  - **The roster:** it equals the old table, and a flag makes it `FORMULA_OPEN`.
  - **Static checks:** the switch is closed, and the wrappers read no data and name no receipt or publication module.
- **`tests/test_e2r_runner.py` (15): E2R-T16 at run level.**
  - **E_1 through the contract:** in both games and at three targets each, the record equals E_1's own result, is consumable with the gates passed, and is not consumable with them failed. A planted difference is refused by the identity check. E_1's function refuses non-synthetic data.
  - **Publication:** publication order, create-only writes, and one folder per run ID.
  - **An interrupted run:** stopped after D1 and before D2, its files stay and it is not consumable.
  - **A failure after a receipt:** D2 `RUNTIME_FAILURE` names no receipt.
  - **Both records:** C1 and C2 are both published and consumable.
  - **Failures:** a method exception, a NaN score and a verify refusal each end in D2 alone. A bad pin is a data-admission failure.
  - **Refusals:** the orphan marker and the real-development switch refuse before anything is created.
  - **The workspace rule.**
  - **Run-level E2R-T03:** two masters differing only at and after the target give byte-identical `forecast.json` and different receipt master SHAs.
  - **Hygiene:** no run ID, path, master SHA, execution path or entry digest in the forecast bytes.
  - **The command line, end to end.**

**The whole suite:** 166 tests (84 earlier, 54 CODE-1 and 28 CODE-2) pass on Linux, Python 3.13.17 and 3.15.0b4.

**Mutation checks (E2R-1 13, for T14 and T16): 12 planted defects, each caught.**
- **The gate:** it ignores the flag, admits FORMULA_OPEN, accepts a stale pin, or ignores a declaration mismatch.
- **Reading and the coordinator:** the runner reads data before the gate; the coordinator side skips the shared gate.
- **Caching:** the gate trusts a cached registry.
- **Terminal records:** a failed run names its receipts; a failure after a receipt is recorded as SUCCESS.
- **Publication:** publication overwrites (with both existence guards removed: one first-draft mutation was equivalent); a run folder can be reused; consumption ignores the gates.

**Proposed review:** HIGH tier with RECHECK. The always-review subjects touched are dispatch and orchestration, publication and consumption, and orchestration-only provenance. No reader, coordinator, protected function, switch or allowlist is touched.

**Install:** the usual code discipline. PRE checks that the one modified file equals its base blob; POST checks that it equals the reviewed bytes and that every new file is exact; then COMMITTED; the owner's Windows suite runs before the commit.

## 9. The speculative candidate

At the owner's request, Claude has already written the code this note describes, with its tests, mutation checks, and an install package built and run end to end on Linux. It is held in Claude's workspace, not installed. If the reviewer passes this design as written, the same candidate goes to the HIGH-tier code RECHECK. If the design changes, the code changes with it.

## 10. Decisions for the owner

- **D2-1:** CODE-2 covers the standalone contract path. The coordinator side gets only the shared gate, and refuses every coordinated contract request. A real coordinated contract run is a later, separately reviewed package, which also needs scientific coordination enabled by you. **Recommendation: yes.**
- **D2-2:** a new code-level switch, `ENABLE_CONTRACT_REAL_DEVELOPMENT = False`, in the shared contract runner. Contract runs on the real development masters stay off until a separately reviewed, owner-authorised patch. It becomes a fourth switch that stays False, with a test. **Recommendation: yes.**
- **D2-3:** E_1's legacy standalone runner stays unchanged and is not gated. It is the frozen legacy path; new work uses the gated contract runner. Gating it too would change E_1's entry file. **Recommendation: leave it unchanged.**
- **D2-4:** Package 2's roster reads the installed contract registry, so there is one record of status, with identical results today. **Recommendation: yes.**

Out of scope, and unchanged: coordinated method runs, real-data runs, FINAL, IS, scoring, retirement (CODE-3), any E_1 code change, and any change to a protected function, switch or allowlist.
