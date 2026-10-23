# Predictive Randomness — Windows Architecture Proof-of-Concept and Implementation Task Specification

**Edition:** v0.2 OWNER-RATIFIED (23 October 2026). v0.1 remains historical and unchanged. This version supersedes stale v0.1 operational instructions as explicitly stated in §10.

**Document version:** v0.2 — OWNER-RATIFIED  
**Date:** 22 October 2026  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Repository path:** `doc/Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_2.md`  
**Status:** OWNER-RATIFIED document; non-destructive Windows results identified as OWNER-REPORTED only; destructive gates remain NOT_RUN / NOT_AUTHORISED  
**Authoring basis:** inspected GitHub repository ZIP `analysing_perceived_randomness_in_reality-main(3).zip`, supplied 22 October 2026; ZIP SHA-256 `645824d2647bb2a0877e5dad9a16a2298743fed5a03db15c25ecd0e7aabf2a63`  
**Operator's local checkout:** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`  
**Target machine:** Windows 11; Python 3.14.8 project `.venv` (as reported); AMD Ryzen 9 3900X; 32 GB RAM; VS Code and CMD.

> **Purpose.** Authorise *a small, auditable engineering proof-of-concept* for the ratified Architecture 2, particularly **Option F** (coordinator launches an independent experiment through the same `Run_Experiment.bat` wrapper a person uses). Demonstrate correctness on the **actual Windows machine** before accepting that launch mechanism for production. No lottery research result, new physical hypothesis, or prospective prediction is produced during P0–P2.

> **Status distinction.** The **architectural design is ratified**; ERR-R2-02's **production acceptance is still conditional** on Windows evidence and subsequent owner review. A ratified design is not evidence that any wrapper, Python process tree, or numerical library has been tested.

---

## 0. Authority, precedence and scope

### 0.1 Controlling documents (already ratified/approved)

1. `doc/Predictive_Randomness_Research_Project_Proposal_v0_3.md` — scientific purpose, original holdout and prospective forecasting controls.
2. `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` — permanent E_1–E_62 method catalogue and hypotheses.
3. `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` — historical N−1 data rule, actual L+1 predictions, fit/readout separation, reproducibility and benchmarks.
4. `doc/Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` — owner-approved adjustments: worker tests against the configured maximum (currently **six**), Option F **conditional**, authoritative dependency `.bat`, and separation of fit/readout version identities.
5. `doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_2.md` — score/readout rules, including `TIE_SHA256_V1`, TOP/WORST and evaluation isolation.
6. `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_3.md` — independently executable E-programs, batch wrappers, `subprocess.Popen`, six-worker cap, proposed monitoring and P0–P4 phases.

In the repository archive the headings of R3/Architecture may still contain *pre-ratification* labels. The **project owner ratified the corrected R3 v0.2 and Architecture v0.3 on 22 October 2026**. Ratification is established by that decision, not inferred from the documents' old template status labels. This task does **not** edit those originals.

### 0.2 Implementation boundaries

**In scope now:** create small Windows batch wrappers, dependency maintenance, a **non-scientific engineering probe**, common test/runtime helpers, a miniature coordinator and automatic/manual Windows tests. All changes are reviewable, independently testable, source-controlled and reversible.

**Not in P0–P2:** implementing any E_1–E_62 mathematics; selecting algorithms by performance; reading holdout 1578–1587 for method evaluation; genuine FINAL forecasts; implementing R3 evaluator/scoring, ensembles, adaptive optimisation, fitted-model checkpointing or a general plugin/service framework. Do not start a background daemon or install a Windows service.

**No code has yet been implemented as part of this task document**. The proposed filenames, CLI spelling and JSON schema below are design targets for review and the first coding iteration, not evidence of existing programs.

### 0.3 Phase names — align exactly with ratified Architecture §16

| Phase | Meaning and gate |
|---|---|
| **P0** | Engineering probe + wrapper/venv/argument/pipe fundamentals; **no mathematical model**. |
| **P1** | Direct versus coordinated **canonical-content equivalence**, paths and output validation. |
| **P2** | Six-worker scheduler, failures, timeout/cleanup, `Ctrl+C`, memory and compatibility suite; **no mathematical model**. |
| **P2 closure** | Owner reviews the Windows evidence; decides acceptance, remediation or rejection of provisional **ERR-R2-02 / Option F**. This is a *review gate*, not a newly renumbered P3. |
| **P3** | **Later and separately authorised:** minimal actual E-method (probably E_1), using permitted data boundaries and R3 readouts. Not part of this first POC implementation or acceptance. |
| **P4** | Later, formal incremental implementation planning after the accepted architecture and minimal actual-method demonstration. |

### 0.4 Design preferences that are **not** reopened here

- **Independent executable `.py` experiments**, optional reusable `_common` modules and filename discovery rather than a compulsory imported-method runner.
- One human-facing `Run_Experiment.bat` launch contract for standalone and coordinator use (**Option F**, pending test acceptance); fallback direct-Python launch only after owner review if Option F is inadequate.
- **Explicit .venv checks, temporary `CALL` activation if inactive, and restoration of the caller's environment**, even though an explicit venv `python.exe` does not technically require shell activation.
- **`install_upgrade_dependencies_into_venv.bat` is self-contained:** the authoritative list of named PyPI dependencies and install/upgrade commands is in that `.bat`, not in a second human-maintained manifest.
- Default and initial maximum of **six** experiment subprocesses; one external numerical-library thread per experiment initially; no project-managed Windows Job Objects.
- Human-readable console, live coordinator relay and **one authoritative structured result file** per experiment; independent post-draw evaluator in the later scientific framework.

---

## 1. Exact repository baseline and non-destructive installation

### 1.1 Items verified in the supplied ZIP

| Path | Observation | POC treatment |
|---|---|---|
| `activate_venv.bat` | Exists; uses `CALL ...\.venv\Scripts\activate.bat`; checks `VIRTUAL_ENV` existence; current ZIP contains **LF** line endings. | Preserve existing operator interface; include in CRLF normalization/test. No unsupported in-place fix or replacement without review. |
| `deactivate_venv.bat` | Exists; current ZIP contains **LF** line endings; checks `VIRTUAL_ENV` existence. | Same. Do not assume `VIRTUAL_ENV` alone proves environment identity. |
| `.vscode/settings.json` | Configures `${workspaceFolder}/.venv/Scripts/python.exe`, and a CMD terminal profile that calls venv activation at startup. | Preserve; test both normal CMD and VS Code paths. |
| `.gitignore` | Excludes `.venv`; **does not currently exclude `transitory_data/`**. | Add a narrow ignore rule for POC scratch outputs; do not hide needed committed evidence. |
| `.gitattributes` | **Absent.** | Add `*.bat text eol=crlf`; test checkout conversion on Windows. Do not indiscriminately convert Markdown or CSV line endings. |
| `requirements.txt` | Exists; currently contains eight pinned packages (including `requests`, `beautifulsoup4` and their dependencies). | Historical file; **not** the new authoritative dependency policy. Decide its retirement/generated status explicitly; no independently maintained duplicate list. Do not silently delete during POC. |
| `src/scrape_australian_powerball_history_from_2018_04_19_v0_3.py` | Only Python source file presently under `src/` in ZIP. | Leave unchanged. It is the data-acquisition utility, not an experiment. |
| `source_data/australian_powerball_history_20261021.csv` | Present. | Preserve byte-for-byte; do not feed to P0–P2 fixtures. |
| `source_data/australian_powerball_draw_order_20261021.csv` | Present. | Preserve byte-for-byte; do not feed to P0–P2 fixtures. |
| `results/dummy.txt` and `transitory_data/dummy.txt` | Empty placeholders present. | Keep unless a separate cleanup is authorised; do not use as experiment outputs. |
| `doc/` | Contains ratified/approved docs plus superseded R3 v0.1 and Architecture v0.2. | Do not silently delete, rename or rewrite the ratified set; doc cleanup is a separate Git action. |

**Archive identity caveat:** GitHub's downloaded source ZIP does not include `.git` history. Do **not** invent a base commit SHA; ask the operator to record local `git rev-parse HEAD` at installation and in test evidence. The archive SHA-256 above identifies the reviewed ZIP, not the checkout commit.

### 1.2 Installation policy

- Add new source and tests to a *copy of, or properly checked-out instance of,* the existing repository; **never replace the whole `src/`, `source_data/` or `doc/` directories**.
- Keep existing ratified specifications unchanged. The new task spec and POC files should be separate Git additions with reviewable diffs.
- If delivering files as a ZIP, package repository-relative paths only; unpack deliberately at the repository root. Do not embed absolute `E:\...` paths into runtime Python or wrappers.
- Do not commit `.venv`, personal Windows paths, raw crash dumps, unmanaged huge memory-test logs, transient status files or automatically downloaded packages.
- Keep `.bat` **CRLF** in the delivery and Git checkout; Markdown/Python may remain UTF-8 LF.

---

## 2. Proposed POC file manifest

The initial POC should be small; a proposed manifest is:

```text
[repository root]
    Run_Coordinator.bat
    Run_Experiment.bat
    install_upgrade_dependencies_into_venv.bat
    .gitattributes                         [add]
    .gitignore                             [narrow change]
    activate_venv.bat                      [existing; CRLF validation]
    deactivate_venv.bat                    [existing; CRLF validation]
    requirements.txt                       [existing; not authoritative]
    src/
        Powerball_Experiment_Coordinator.py
        methods/
            POC_Architecture_Probe.py     [ENGINEERING ONLY; not E_000 / E_001]
            _common/
                __init__.py
                project_paths_and_output_locations.py
                experiment_runtime_status_and_resources.py
                runtime_environment_verification.py
                experiment_console_and_file_output.py
    tests/
        windows_architecture_poc_suite.py  [test launcher/reporting driver]
        fixtures/                          [small synthetic engineering inputs]
    doc/
        Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_1.md
```

The above `_common` helper boundaries can be combined if doing so visibly reduces complexity. Do **not** create a general RPC layer, method-fitting framework, scientific evaluator or empty placeholder for every E-method during the POC. Names must be descriptive; source files must not be mislabelled with scientific `E_` identities.

**Important probe discovery rule:** `POC_Architecture_Probe.py` does **not** match the production `E_???_*.py` discovery pattern. The POC coordinator may explicitly run that **one whitelisted probe** only under a declared `--poc`/test mode. This bypass is *only* for the engineering tests, not a new auto-discovery rule admitting arbitrary `.py` files. Zero implemented science methods must still be a normal, accurately reported state.

**Scratch/evidence separation:** write volatile probe files under a unique directory within `transitory_data/poc_runs/` (ignored by Git). Archive **small, sanitized, independently verified** pass/fail summaries to `results/architecture_poc/` only after operator approval. An aborted POC cannot leave an apparently valid FINAL lottery forecast.

---

## 3. P0 — wrapper, environment and dependency-maintenance contract

### 3.1 Common wrapper requirements

Both human-facing launch wrappers (`Run_Coordinator.bat`, `Run_Experiment.bat`) shall:

1. Determine the **repository root using `%~dp0`**, not the caller's working directory; test calling from another directory and a location containing spaces.
2. Use `SETLOCAL` to scope environmental changes, restore the caller's original environment at all *normal* exits, and return the launched Python program's exit code (or a distinct failure code if launch could not occur).
3. Check existence/identity of `root\.venv\Scripts\python.exe` and `root\.venv\Scripts\activate.bat`. If no environment is active, `CALL` the project activation **inside the scoped batch environment**. If the active `.venv` is the same project path after Windows-style normalisation, do not falsely reject it; if another venv is active, fail clearly rather than silently switching. For diagnostic consistency, the *actual Python child's* `sys.prefix` is the final authority.
4. Execute the **explicit project interpreter** after checking, regardless of `PATH`. Do not use global Python or implicitly create/rebuild `.venv` during an experiment launch.
5. Preserve raw command arguments through the agreed `%*` forwarding interface. Do not reconstruct arguments by `SHIFT` plus `%*`, which leaves the first argument present; do not round-trip through `%1..%9` for forwarding.
6. Configure pre-import numerical-thread environmental limits consistently for manual/coordinated runs (at least `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`; expand only when a known backend requires it). Verify observed limits where a relevant library is installed; do not silently override user-approved method-specific exceptions in later stages.
7. Keep printed wrapper diagnostics short; never include credentials/secrets in log lines. Do not swallow child standard output or error output.
8. Remain **CRLF** batch files; no custom PowerShell runner is required.

**No assumption about `cmd.exe` launch parsing:** The wrapper is executed under CMD. The POC must prove real argument handling. Do **not** standardise an untested `cmd.exe /D /C` invocation: nested quote handling can change the meaning of a path or argument. Read `Software\Microsoft\Command Processor\AutoRun` from both HKCU/HKLM as part of the test preflight; if it interferes with reliability, **fail with a diagnostic**, do not edit the user's registry. If an explicit `/D /S /C` path is later justified, implement only after a separately tested correctly quoted form is reviewed.

**Security boundary:** Program filenames supplied to `Run_Experiment.bat` must resolve **only to approved `.py` files within `src\methods`**; do not accept `..\`, absolute arbitrary executables or shell-control characters just because `%*` is convenient. CMD metacharacters and percent expansion require an explicitly tested supported/unsupported parameter policy. Ordinary known arguments, including `--history=100`, must survive unchanged; approved quoted paths must also be tested.

### 3.2 `Run_Experiment.bat` interface

Illustrative use (not yet functioning):

```cmd
Run_Experiment.bat POC_Architecture_Probe.py --case=echo-argv --case-id=example
Run_Experiment.bat E_001_historical_occurrence_frequency.py --mode=historical --target-draw=1500
```

- The **first argument is the `.py` basename**; subsequent arguments belong to that program.
- `PUSHD`/`POPD` to `root\src\methods` is allowed for simple `%*` forwarding, but common path utilities must derive repository-relative defaults from `__file__` rather than the accidental CMD working directory.
- Avoid using the experimental probe's `E_` identity or the real Powerball CSV in P0. The E_001 command above is only future documentation.
- A wrapper exit code of zero is **not** by itself proof that a valid scientific result exists; coordinated runs must later validate result files.

### 3.3 `Run_Coordinator.bat` interface

Illustrative test use:

```cmd
Run_Coordinator.bat --poc --workers=1 --case=echo-argv
Run_Coordinator.bat --poc --workers=6 --case=canonical-fixture
```

- Perform the same `.venv` checks, scoped activation and explicit-interpreter launch as the experiment wrapper.
- Launch `src\Powerball_Experiment_Coordinator.py` and forward all coordinator arguments intact.
- The Python coordinator is responsible for child lifecycle and pipes; wrappers contain no prediction mathematics or stateful method registry.

### 3.4 `install_upgrade_dependencies_into_venv.bat` — sole authoritative package list

**Operator requirement:** a maintainer opens **one self-contained `.bat`**, sees the actual named PyPI packages and their version policies, and runs that `.bat` when installation/maintenance is intended. No dependency declaration is separately maintained in `requirements.txt` or `pyproject.toml`.

**First draft behaviour to prove:**

- Explicit `INSTALL` (ensure specified dependencies), `UPGRADE` (deliberate eligible upgrade) and `VERIFY` (read-only checks), or equivalent clearly documented switches; invalid switches fail nonzero. Decide the default no-argument operation before implementation, but **never silently upgrade on a forecast launch**.
- Clearly identify a single editable section **inside the batch file**, listing all direct PyPI packages actually selected: existing `requests` and `beautifulsoup4`; `psutil` for process supervision; proposed scientific dependencies such as `numpy` and `scipy` when approved/needed; and `threadpoolctl` only if used to check effective numerical threading. Do not copy/transcribe all transitive packages into a second human-maintained authority by mistake.
- Verify/create policy for `.venv`: first implementation should **require** a usable project `.venv`, not silently create one with the global Python or overwrite a known environment. If `pip` is missing, report the recovery path rather than using a global `pip` unnoticed.
- Use `root\.venv\Scripts\python.exe -m pip ...` explicitly; run `pip check`; display interpreter/pip/package versions and meaningful nonzero failures; preserve CMD caller environment.
- Print resolved environment details and allow generation of a **machine-produced snapshot** (`pip freeze`, Python identity and script digest); such a snapshot is provenance, not another package list for manual editing. Snapshots must eventually accompany benchmarks, genuine FINAL batches, the once-only holdout opening and conclusion-bearing historical evaluations.
- Never upgrade automatically inside coordinator or experiment. After an explicit upgrade/rebuild, block consequential research until the **relevant Windows compatibility suite** and scientific reproducibility gates have passed.

**Existing tracked `requirements.txt`:** the ZIP contains a pinned eight-line file. This POC shall record that fact and explicitly recommend its eventual retirement or automatic derivation if external tools need it. Do not silently discard it before validating the replacement workflow. If retained, it must be labelled non-authoritative and not manually edited independently.

### 3.5 New `.gitattributes` / ignore policy

Proposed minimum:

```gitattributes
*.bat text eol=crlf
```

Add a **narrow** `.gitignore` rule for ephemeral `transitory_data/poc_runs/` (or the entire transitory-data contents if separately approved), leaving scientific evidence under `results/` eligible for deliberate commits. Perform a clean-checkout or `git add --renormalize` **dry review** for existing batch files and confirm the Windows working files actually contain CRLF. Note: `.gitattributes` influences checkout representation; it does not automatically repair already checked-out LF files until a checkout/renormalisation operation or explicit conversion. Do not mass-rewrite unrelated tracked files.

---

## 4. P0/P1 — engineering probe and deterministic-output contract

### 4.1 POC probe operations

The standalone `POC_Architecture_Probe.py` is an **engineering fixture**, deliberately unrelated to Powerball data and outside the E_1–E_62 catalogue. Proposed, test-specific operations:

| Probe case | Action | Why |
|---|---|---|
| `echo-argv` | Record `sys.argv`, root resolution, interpreter, `sys.prefix`, process PID and selected non-secret environment variables. | Wrapper argument/venv/path integrity. |
| `canonical-fixture` | Read a tiny fixed synthetic input from `tests/fixtures/`; write reproducible JSON with fixed values and an independently checked digest. | Manual versus coordinator, 1 vs 6, output files. |
| `verbose` | Print a configured large number of labelled lines with flushing. | Pipes, concurrency, attribution and deadlocks. |
| `sleep-timeout` | Sleep beyond a small test-specific timeout, after atomic STARTED status. | Tree cleanup; no valid result on timeout. |
| `exit-code` | Exit with selected `0`, `3`, an unhandled exception, or `os._exit(7)` only in controlled tests. | Exit propagation, partial status and failure accounting. |
| `cpu-load` | Bounded pure-Python CPU loop using monotonic stopping/iteration bounds. | Process-owned CPU time and coordinator elapsed time. |
| `memory-load` | Allocate measured, bounded memory in staged increments; release on normal exit. | Six-worker RAM headroom and accurate self-reporting. |
| `status-only` | Emit STARTED then deliberately omit valid JSON or write invalid/mismatched JSON under test control. | Exit-zero is not success; validation rejects incomplete output. |

**Safety:** Dangerous cases require an explicit `--poc` or an equivalent test flag, a bounded duration/allocation and a disposable run directory. Cleanup is permitted only at the separately reviewed and owner-authorised destructive gate, performed by the coordinator using its retained, identity-verified processes and original wrapper handle; never by a test driver, never manually, and never via taskkill. No POC probe can create a genuine `FINAL_NEXT_DRAW` result or score against the real CSV.

### 4.2 Runtime status file (machine-readable, separate from the authoritative result)

The shared helper should write a per-invocation atomic status file into its unique scratch directory. Minimum fields at start: test identity, status=`STARTED`, experiment `os.getpid()`, process-creation identity/time adequate to detect PID reuse, `sys.prefix`, a non-guessable or safely unique run key, and start timestamp. At normal end: terminal status (`SUCCESS`/`FAILED`), wall elapsed via `time.perf_counter`, CPU time via `time.process_time`, and peak working-set memory (with explicit semantics and unit; `psutil` preferred).

If `os._exit()` or the interpreter crashes, STARTED-only is legitimate evidence of an abnormal termination, **not** a successful result. Do not require a status file to claim a hard crash was neatly recorded by a dead child.

### 4.3 Console and result file — distinct responsibilities

- A readable `BEGIN / DESCRIPTION / PROGRESS / RESULT / FINISH` presentation may be emitted by the probe; this is **operator-facing text**, not a custom RPC protocol or sole scientific data source.
- Coordinator continuously drains stdout/stderr for **each active child**. One reader thread per process with a thread-safe queue is a simple candidate; implement the smallest reliable mechanism. `stderr=STDOUT` is acceptable initially if exception diagnostics are preserved.
- Every child writes its **authoritative result JSON atomically**: temporary file in the same directory, flush/close as needed, then replace/rename after validating completion. A run identity that already corresponds to a frozen authoritative result **must not be overwritten**; use a preflight no-clobber policy for collisions. A plain `os.replace` can overwrite, so it must not by itself be treated as an immutability guarantee.
- JSON canonical bytes: explicitly define UTF-8, key ordering, separators, integer/float representation (fixture can use integers only), newline policy and hashed-content boundary. Exclude timestamps, worker count, wall/CPU/memory figures, transient paths and log interleaving from **canonical prediction-content equality**. These belong in separate provenance/status fields.
- Compare canonical **output bytes**, not merely parsed JSON equality, for A-03/A-04/W-25. The probe uses a constant synthetic fixture, not a fake claimed lottery forecast.
- A nonzero child exit, missing JSON, malformed JSON, wrong method/probe ID, wrong target, digest mismatch, or a status disagreement is a **failed run**. Every queued worker must have a final manifest status; failures cannot silently disappear.

### 4.4 Path resolution

Root detection must work when run from repository root, a different drive/folder, a VS Code terminal and inside `src\methods`. Source/output defaults are derived from a common verified path utility, **not** `os.getcwd()`. If a user passes a relative project path, the documented policy should resolve it against the project root even if the wrapper temporarily changes CMD directory. Make this observable in `echo-argv` and W-24.

---

## 5. P2 — six-worker supervision, timeouts and Windows compatibility

### 5.1 Coordinator scheduling and resource policy

- `workers` is configurable **1–6**, with initial default **6** and rejection (or explicit, well-documented clamp decision) of `0`, negatives and `>6`; do not silently spawn 12.
- For each probe, construct one child launch through the **shared `Run_Experiment.bat`** via `subprocess.Popen`; exact Windows command-line quoting remains an observed W-suite question. Direct child Python launch is a separately recorded contingency, not silent fallback after a wrapper failure.
- Give each worker a unique ID, scratch path, provenance, timeout and output expectation; preserve the correlation between stdout labels, process exit code, status file and result JSON.
- No POC probe starts its own subprocess or process pool. Existing Windows venv launcher internals are not counted as method-created process pools.
- Verify `sys.prefix` from the **actual executing probe**. Do not depend on `Popen.pid` identifying the computation or a stable number of CPython processes.
- Keep numerical-library thread controls identical under manual/coordinator execution. Initial limit is **one computational thread per library per experiment**; let tests establish actual backend behaviour when NumPy is installed.
- CPU and memory benchmarks require **the experiment's own self-reported values** plus separate coordinator wall-clock and system-available-memory sampling. Do not interpret CMD/redirector CPU usage as the experiment's resources.

### 5.2 Timeout and process-tree protocol

1. On start, record the `Popen` root PID (usually CMD with Option F) and an independent probe process identity. Publish durable STARTED status as early as practicable before expensive imports; absence of matched status blocks termination regardless of observed ancestry. Verify both are recorded before treating a process as fully supervised.
2. During ordinary running, capture and retain verified wrapper descendants **while the wrapper root is alive**, using `psutil`, before any timeout/cancellation. Distinguish this process list from an assumption about CPython's venv redirector.
3. Only when switch-on has separately been reviewed and expressly owner-authorised, apply bounded shutdown to retained identity-verified members and original root handle, wait, and confirm the probe's recorded PID/creation identity is gone. Until then `ENABLE_PROCESS_TERMINATION = False`; a timed-out worker must remain unterminated and creates an unresolved-orphan marker. PID checks must defend against reuse; compare recorded process creation time where applicable. The implementation must not accidentally kill an unrelated process whose PID was recycled.
4. If a descendant persists, its identity is uncertain, or confirmation fails, record `ORPHAN_SUSPECTED`, alert the operator, **stop all further launches**, and create a persistent no-overwrite, fsynced `UNRESOLVED_ORPHAN.json` interlock. Existing workers may finish naturally. Future starts must refuse while **any** marker entry exists; there is no CLI bypass or automatic clearance. The marker is cleared only after separately verified manual incident-specific recovery and evidence archiving; **do not free/reassign that worker slot as if cleanup succeeded**. Do not assume `Popen.kill()` alone stops descendants on Windows.
4a. **Complete launch-stop / marker trigger (OWNER-RATIFIED):** on **any condition where the coordinator cannot positively confirm that every captured process AND the run-matched status-reported experiment have exited**, refuse further launches and preserve a persistent no-overwrite/fsynced unresolved-orphan marker. A live/unknown run-ID-matched status PID at wrapper exit triggers the marker **even with no captured descendants**; likewise a stuck reader pipe, timeout/interrupt with termination disabled, or any unconfirmed stop. Status evidence may block, never add kill targets. An existing marker entry blocks startup with no CLI bypass. Manually inspect PID plus creation time, archive original bytes/hash/logs, and clear only through a reviewed narrowly scoped procedure after all listed processes are confirmed gone. Marker-write failure = CRITICAL. See proposed Architecture v0.5 §5C.2.
5. `taskkill /PID ... /T /F` is **NOT an authorised coordinator fallback** (ratified Architecture v0.4 §5C.2); neither status-file PIDs nor freshly reconstructed trees authorise killing. W-09/W-16 are diagnostic observations only, and must not initiate unsafe cleanup. Process termination requires the strict verified ancestry **and** positively matched experiment status identity rule; otherwise leave uncertain processes untouched.
6. Ctrl+C through **six CMD wrappers** must be verified with redirected stdin and real CMD/VS Code console conditions. Avoid a stranded `Terminate batch job (Y/N)?` prompt and preserve `INTERRUPTED` status.
7. No project-managed Windows Job Objects in P0–P2. They may be reconsidered **only** if evidence demonstrates simpler approaches inadequate and the owner approves the change.

**Operational qualification:** No mechanism that merely *tries* to kill a process tree can provide absolute guarantees against detached grandchildren or races. The ratified first-release restriction against experiment-created child processes makes a bounded, verified `psutil` approach a plausible **testable** minimum. Never promise that a direct subprocess kill always cleans up every future Python implementation.

### 5.3 Memory stress test (risk-managed; DESTRUCTIVE-GATE ONLY)

- Machine: 32 GB RAM, six active worker ceiling; a nominal 6 × 2 GB = **12 GB**, **excluding** Python/library overhead, coordinator, OS and other processes.
- Stage workers progressively (e.g. 1 → 2 → 4 → 6), while sampling **available physical memory** and observing operator responsiveness.
- Explicitly define an operator-approved safety floor before the test; stop admitting new allocations or terminate the test deliberately if approaching the floor. **Do not require 12 GB actual allocation if the PC lacks adequate headroom that day**.
- Release allocated memory and verify the workers exit; never write multi-gigabyte scratch files or commit logs containing huge memory dumps.
- The stress case measures process management and system capacity, **not** scientific performance or an E-method's predictive value.

### 5.4 Upgrade regression gate

Rerun appropriate Windows W-tests whenever the operator updates Python, rebuilds `.venv`, upgrades `psutil`/numerics or materially edits wrappers. No assumption that CPython continues to use the same redirector PID arrangement or internal Job Object. A *new* Python version is accepted for research only after the observable contract has passed. Save interpreter/installed dependency versions and relevant code digests with evidence.

---

## 6. Mandatory test register (existing identifiers preserved)

### 6.1 Mapping the ratified architecture A-suite into the POC

| Tests | POC phase / intent |
|---|---|
| **A-01–A-06** | P0/P1: direct CMD/VS Code, coordinator equivalence, 1 vs 6, global-python rejection, `env` override integrity. |
| **A-07–A-10** | P1/P2 discovery/roster accounting; test probe is separately whitelisted and not mistaken for a scientific E-method. A complete E_1–E_62 implementation roster belongs to the later framework, so a POC may test roster status with synthetic inventory fixtures only. |
| **A-11–A-17** | P1/P2 pipes, exceptions, absent/invalid JSON, timeout/interrupt, collision. |
| **A-18–A-24** | Contract-level negative tests where meaningful: immutable results, source cutoffs, fit/readout independence, JSON/console agreement, actual-outcome/evaluator separation, paths and namespaces. **Real-draw leakage / actual-score tests are deferred to P3; P0–P2 may use only isolated synthetic dummy analogues.** |
| **A-25** | P2 staged six-worker memory stress. |
| **A-26** | Later scientific ensemble dependency contract; in P2 only test synthetic `UNAVAILABLE` accounting. |

Do not label scientific acceptance tests involving genuine prediction/evaluation as PASSED merely because a dummy analogue passed. The POC report must clearly separate **fully verified / engineering analogue / deferred** per test ID.

### 6.2 Windows W-01–W-25 — authoritative acceptance mapping

| ID | Phase | Required evidence / criterion |
|---|---|---|
| W-01 | P0 | Child `sys.argv` exact for supported `=`, comma, semicolon, quotes, spaces. Mark unsupported CMD metacharacters explicitly; never silently rewrite. |
| W-02 | P2 | Six verbose children; complete line counts, method/worker labels and no pipe deadlock. |
| W-03 | P0/P2 | Exit 0 / exit 3 / Python exception; wrapper and coordinator preserve codes. |
| W-04 | P0 | Inactive, project-active and different-active venv; path normalisation, environment restoration; probe `sys.prefix` verified. |
| W-05 | P0 | Record `Popen.pid` and probe `os.getpid()`; do not require equality. |
| W-06 | P2 | Controlled ~1-GB memory allocation; in-process peak memory reports with units. |
| W-07 | P2 | Bounded CPU task; in-process CPU and coordinator wall time sensible. |
| W-08 | P2 | Switch-False timeout: NO termination; marker and interlock expected, FAILED manifest retained. Destructive termination/verification deferred to separate reviewed gate. |
| W-09 | P2 diagnostic | Kill wrapper root only, observe and **then observe survivors; cleanup is destructive-gate-only via the coordinator using retained identity-verified processes, never manual, never taskkill**; not a mandatory everyday upgrade diagnostic. |
| W-10 | P2 | Six-worker Ctrl+C only at separately reviewed/authorised gate. With switch False, timeout or Ctrl+C creates a persistent interlock; no claim of no orphans or ordinary completion is allowed. |
| W-11 | P2 | Hard exit 7; incomplete status not misrepresented as successful. |
| W-12 | P0 | Global-Python start or missing venv fails clearly without running science or installing packages. |
| W-13 | P2 | Progressive 1/2/4/6 worker ~2-GB stress **only while adequate memory headroom exists**; any stop is destructive-gate-only under independent review and explicit owner authorisation; coordinator may stop only retained identity-verified processes. |
| W-14 | P0 | Coordinator-through-wrapper `argv` exact within approved set; invalid chars rejected; path with quotes/spaces test. |
| W-15 | P0 | Exit 0/3/exception/7 propagated via wrapper to coordinator. |
| W-16 | P2 diagnostic | Killing CMD alone does not constitute success; measure survivors; any cleanup is destructive-gate-only via retained identity-verified coordinator processes, never manual or taskkill. |
| W-17 | P2 | Capture/verify descendant ancestry and status identity; simulated kill-target plan with switch False; actual terminate/wait only after reviewed destructive gate. |
| W-18 | P2 | Ctrl+C console behaviour requires separately reviewed test; with switch False an unresolved marker is expected, and no guaranteed cleanup claim. |
| W-19 | P0/P1 | Manual versus coordinated: same effective venv, numerical settings and canonical bytes; inspect HKCU/HKLM `AutoRun`, no untested `/D /C` quoting. |
| W-20 | P0 | Dependency `.bat` contains actual direct package list, runs deliberate operation, `pip check` and reports versions; caller state restored. |
| W-21 | P0 | Deliberately invalid dependency/constraint in **isolated dry fixture**, not destructive modification of real venv; nonzero and clear message. |
| W-22 | P0 | Committed/checked-out `.bat` CRLF verified with byte check and actual CMD launch. |
| W-23 | P2/maintenance | Demonstrate gating logic by a simulated environment-change marker or safe verification; **do not forcibly upgrade/recreate the user's live venv** just to test it. A real post-upgrade run occurs after actual upgrades. |
| W-24 | P0 | Start from elsewhere / project path with spaces / quoted parameter; exact args, project-root-relative path and exit code, no nested `/C` mangling. |
| W-25 | P1/P2 | Same fixed fixture with 1 and 6 simultaneous invocations; byte-identical canonical payload; distinct per-run metadata. |

**Test designation:** `PASS` (performed with exact expected evidence), `FAIL` (performed, violated contract), `INCONCLUSIVE` (performed but evidence insufficient), `NOT_RUN` (not performed), `DEFERRED` (only later scientific code can exercise), and `N/A` (documented reason). The test-driver summary must not turn NOT_RUN into PASS.

### 6.3 Acceptance thresholds and negative tests

- **P0 gate:** both wrappers start correct interpreter from different working directories, exit codes/args/CRLF/venv identity are verified, dependency-maintenance script is controlled, and no unexplained CMD AutoRun/quoting behaviour remains.
- **P1 gate:** standalone and coordinated probe have exactly equal canonical bytes; JSON/console agree; no file clobber; no production E-roster contamination.
- **P2 gate:** six-worker scheduling, stdout drains, deliberate failure and timeout cleanup, Ctrl+C, memory guard, and applicable W-tests all pass or have explicitly approved qualified exceptions. Failures or unresolved `ORPHAN_SUSPECTED` prevent Option F production acceptance.
- **P3 gate:** **not part of POC closure**; requires owner's explicit approval to proceed with first genuine method after P0–P2 evidence review.

---

## 7. Evidence package and handback to owner / independent reviewer

### 7.1 Required per-machine test record

One versioned report (e.g. `results/architecture_poc/Windows_Architecture_POC_Report_v0_1.md`) should contain:

1. Test date/time in Adelaide local time with timezone offset and a UTC timestamp where convenient; machine OS build, CPU, RAM, CMD/VS Code context.
2. Git base commit, dirty/clean state, modified tracked/untracked file list; Python, `.venv` path, pip and installed relevant package versions; dependency-maintenance `.bat` hash.
3. SHA-256 for all submitted `.bat`/`.py` implementations and important synthetic probe fixtures; no assumption that ZIP source hash is the Git commit.
4. Clear table for **every W-01–W-25 and A-01–A-26**: observed status, exact invoking command/case, expected, actual, log/status/JSON evidence path, deviations, and known limitations.
5. Comparative direct/manual/coordinated canonical-output hashes for the same synthetic fixture; one vs six, with separate operational metadata.
6. PID/tree observations including wrapper PID and probe PID **without assuming CPython internal redirector arrangement**; recovered tree on test failures; exact timeout/cancellation semantics.
7. Resource/accounting comparison: child self-reported CPU/working set; coordinator elapsed time; observed available RAM; progressive memory-test stopping decision and operator headroom.
8. A concise inventory of **remaining issues and required owner decisions**, in particular whether ERR-R2-02 / Option F passes, needs corrective patch/retest, or should be replaced by direct Python subprocess launching.
9. Clear statement that P0–P2 contained **no Powerball predictions, real dataset fitting, holdout scoring or FINAL batch publication**.

### 7.2 POC delivery/handover layout

Deliver code as a small reviewable source patch or ZIP rooted at repository-relative paths; include a separate **test-run procedure in CMD** with actual commands, expected return codes and explicitly labelled commands that allocate memory, kill processes or upgrade packages. No implicit changes to `source_data/`, `doc/` ratified text or the existing scraper.

Retain manageable logs and status traces for failures; summarise high-volume line-count tests instead of committing hundreds of thousands of output lines. Remove unsafe test scratch only after confirming no children remain; never delete source data or legitimate pre-existing experiment results as cleanup.

### 7.3 Ratification/approval procedure

1. Reviewer checks this POC task specification against the ratified six documents and owner preferences; changes are decided by the owner.
2. Implement **P0 first**; run the safe non-destructive tests on the owner's Windows machine; review any launch surprises before adding process supervision.
3. Implement/test **P1** canonical-output equivalence.
4. Implement/test **P2** concurrency and deliberately hazardous cases in controlled stages; preserve evidence.
5. Owner, optionally after Claude independent review, explicitly closes the POC and decides **ERR-R2-02 Option F**. **No claim of acceptance from passing only Linux/container tests.**
6. Only then obtain approval for P3 first actual E-method or develop a further method-specific task plan; the fixed original ten-draw holdout remains sealed from developmental scoring.

---

## 8. Questions to settle before or during P0 (not reasons to redesign architecture)

| ID | Question | Recommended starting position / evidence needed |
|---|---|---|
| **POC-Q01** | Exact CMD argument-escaping contract and supported quoted values? | Support ordinary names, `--option=value`, spaces/quoted paths; test comma/semicolon and deliberately reject unsupported metacharacters. W-01/W-14/W-24 provide evidence. |
| **POC-Q02** | `cmd.exe` AutoRun registry present? | Query HKCU/HKLM read-only. If configured, block/log until a specific safe launch solution is tested; never modify registry without separate owner approval. |
| **POC-Q03** | Wrapper working-directory choice? | `PUSHD` to `src\methods` for `%*`; common utilities resolve project paths from file locations; W-24 checks. |
| **POC-Q04** | What to do with a different venv already active? | Clear refusal, preserve shell; project-active normalised comparison passes. |
| **POC-Q05** | Dependency script default and package pins? | Default should **not upgrade silently**; keep script legible and direct package names inside; record installed versions. Confirm exact mode switches before code. |
| **POC-Q06** | How to treat tracked `requirements.txt`? | Preserve until self-contained installer and provenance scheme pass; later retire/archive or make generated-only, not another manually maintained authority. |
| **POC-Q07** | Ownership/identity races and timeout orphan handling | No fallback termination path. Capture and verify while wrapper alive; status PID block-only. Unverified exits trigger durable interlock, manual review, and no subsequent launches. Any destructive case requires its separately reviewed owner-approved gate. |
| **POC-Q08** | Status/result no-clobber and canonical serializer details? | Use unique per-run scratch, fixed JSON serializer and exact hash scope; atomic *create without overwrite* or equivalent preflight. Test failures/collisions. |
| **POC-Q09** | How much buffer/log output? | One reader per worker or equivalent, bounded memory, buffered-to-file rather than accumulating unbounded stdout in RAM. |
| **POC-Q10** | POC/production discovery separation? | Explicit whitelisted engineering probe; future roster `E_???_*.py` only, with identity checks and NOT_IMPLEMENTED accounting. |
| **POC-Q11** | Memory safety floor and test schedule on owner's PC? | Decide threshold before the staged 6 × ~2-GB test; abort safely if headroom or responsiveness is poor. |
| **POC-Q12** | Should dependency-snapshot generation be mandatory for all POC runs? | Minimum POC provenance is package versions and maintenance-script digest; add full `pip freeze` for P2 acceptance and all later consequential runs. |

---

## 9. Explicit nonclaims, safeguards and decision request

- The supplied repository ZIP was **inspected**, not installed or run on the owner's Windows machine; it establishes file contents, not runtime reliability.
- The file manifest and examples **do not claim any E-method Python files, coordinator or wrapper already exist**.
- The six-worker limit is a new **owner-approved** operational setting under the approved R2 erratum; the original R2 v0.3 document retains historical 1–12 wording.
- The first-release no-method-created-subprocess rule is an engineering capacity constraint **not permission to discard any scientific E-method**.
- Synthetic POC fixtures are engineering-only and must not cross into scientific synthetic null-world/planted-effect research or real-data fitting by accident.
- The POC must never expose the reserved holdout as a development benchmark or let an evaluator supply a future draw outcome to a predictor.
- No package upgrades, registry edits, Python environment rebuilds, Windows Job Objects, or changes to `.venv` are performed merely by reading or ratifying this task document.
- The operator retains approval of new code, Windows test stages, any revised scientific contract, and the eventual disposition of **ERR-R2-02**.

**Decision requested:** approve this v0.2 as a bounded implementation task for P0–P2 (including necessary tests and evidence), with P3 still withheld pending the POC review. Claude may independently review it against the ratified source files before any Windows installation.

**End of original v0.1 section; ratified v0.2 additions follow.**


## 10. v0.2 supplemental accepted-design and evidence register — OWNER-RATIFIED

**Authority:** This proposed v0.2 updates the task specification to match ratified Architecture v0.4 §5C and proposed Architecture v0.5 §5C (candidate) and owner decisions. It does **not** itself authorise a destructive run, live marker clearance, or acceptance of Option F. Where an older table contradicts the ratified §5C safety baseline, the more restrictive safety contract prevails.

### 10.1 Current implementation and baseline (supersedes historical §1.1 observations only)

- The initial source-ZIP inventory in §1.1 is a **historical v0.1-era baseline**, not today's file inventory; do not use its old `.gitignore` / `.gitattributes` assertions to overwrite current files. Claude independently verified GitHub HEAD `5eea9bd` by direct clone at 21:11 Adelaide; the supplied source ZIP is consistent with coordinator v0.6 hash `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`, but contains no `.git` metadata independently proving the owner's local checkout HEAD.
- Coordinator v0.6 was accepted by Claude for **non-destructive Windows testing only**. `ENABLE_PROCESS_TERMINATION = False` remains mandatory. No destructive testing, P3 method, or holdout access is authorised.
- The real incident marker is ignored by Git: owner-reported locally ACTIVE at 23 Oct 2026 21:18 Adelaide, SHA-256 `2d8269eb3845cf17ce7124254f1f9397ae52a1dd5603a0aeb67bdda05453a2aa`; the one-incident clearance utility has not been run.

### 10.2 P1/P2 acceptance additions and requalification

- **Interlock:** dummy-marker startup refusal PASS (owner-reported); real timeout with switch False produced a persistent marker and stopped subsequent launches PASS (owner-reported). Both are limited evidence, not a destructive safety validation. Test corrupt/file/directory marker refusal and repeated starts without bypass using reviewed non-destructive fixtures.
- **Timeout evidence:** root and experiment ancestry matched; **no termination signals sent**; group FAILED remains FAILED despite a late `canonical_result.json`. The rehearsal's second banner was from the stuck-reader path, **not** O1.
- **Direct Python env:** refusal with `VIRTUAL_ENV` absent observed. Direct Python with **mismatched** `VIRTUAL_ENV` remains NOT_RUN.
- **Decoys:** the three-decoy utility proved its originally pinned source; re-pin and independently review before using it as evidence for v0.6 or a later coordinator.
- **Ctrl+C, memory and W-23:** NOT_RUN/NOT_AUTHORISED at this checkpoint; never infer PASS. Any test harness watchdog that can kill `Run_Coordinator.bat` is **not** truly kill-free.
- **Patch candidates before destructive gate:** O1 post-loop status/banner behaviour; O2 malformed huge-integer creation time; O4 main-loop fake-driven stop-launch/manifest test; independently review source changes and updated decoy harness.

### 10.3 Evidence layout and destructive gate requirements

- Durable authorised evidence archive path: `results/architecture_poc/<date>_<test>/`; preserve archive record, exact marker bytes/SHA-256, statuses/manifests, relevant worker stdout including `.log` files, test output and coordinator console transcript (separately when necessary). One archived `worker_001.stdout.log` is omitted from the supplied Git ZIP due to `*.log`; rectify by narrowly scoped reviewed `git add -f` after confirming file bytes, not by silently changing global ignore rules.
- Before any **destructive** testing: obtain independent Claude review and explicit owner authorisation of an exact copied test source; demonstrate the only intentional activation delta is a one-line safety-switch change; record before/after SHA-256, process inventory and decoy identities, environment, package versions, exact Git HEAD, expected safety bounds, and the **forced switch-off/revert verification**. Execute destructive cases one at a time only under a reviewed plan.
- The read-only incident utility `--check` must PASS before owner-initiated `--clear-confirmed`. Do not bypass/rewrite the marker; any live/uncertain identity remains a hard safety stop. Following successful clearance, repeat `--check` returns HOLD due to marker absence as expected.
- **OWNER-RATIFIED 23 October 2026 — failed-group result firewall:** any run/group marked FAIL or orphan-suspected must not contribute `canonical_result.json` to training, evaluation, fixtures accepted as successful, or scientific reports, even when a late result file exists.

### 10.4 Change-status register

- **DECIDED (documentation within existing authority):** remove taskkill fallback, record interlock/status rule, distinguish owner-reported non-destructive evidence and NOT_RUN gates, preserve original v0.1 as history.
- **RECOMMENDED (owner ratification):** approve this task-spec v0.2 and the single self-contained Architecture v0.5 (no erratum); precise housekeeping operations require separate owner approval.
- **OPEN:** live clearance result; independent v0.6 decoy rerun; O1/O2/O4 patch; destructive gate and P2 closure.
