# Predictive Randomness — Software Architecture Discussion and Open Questions

**Draft version:** v0.3  
**Date:** 22 October 2026  
**Status:** DISCUSSION DRAFT — not ratified; no implementation authorised by this document  
**Suggested repository path:** `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_3.md`  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Working environment:** Windows 11, standard CPython 3.14, VS Code, project-local `.venv`, AMD Ryzen 9 3900X (12 physical cores/24 logical threads), 32 GB RAM

> **Executive proposal:** Continue with **Architecture 2**, refined by the owner's preferred **single wrapper launch path (Option F)**: every `E_x` is a standalone `.py`; both the human operator and coordinator may invoke `Run_Experiment.bat`; shared utility modules prevent duplication. The wrapper explicitly checks/activates the project `.venv`, preserves the calling environment, and forwards arguments. The coordinator uses ordinary `subprocess.Popen`, up to **six concurrent experiments by default and in the initial implementation**, with modest `psutil` supervision rather than project-owned Windows Job Objects. All external Python package names and upgrade commands belong in a single, self-contained **`install_upgrade_dependencies_into_venv.bat`**. All these are **design proposals or owner directions**, not executable or Windows-validated code in this document.

## Cross-document review response — v0.2 to v0.3

**Claude review dated 22 October 2026** considered Architecture v0.2 + R3 v0.1 against ratified Proposal v0.3, R1 v0.4 and R2 v0.3. This v0.3 remains a **discussion draft**, not a claim of Windows proof-of-concept completion. **Final review corrections (22 October 2026)**: updated all references to owner-approved R2 erratum v0.2 while preserving provisional ERR-R2-02; updated stale R3/architecture version labels; extended environment snapshots to holdout and conclusion-bearing historical evaluations.

1. **A-1 — `cmd /D /C` quoting:** Withdraw the untested recommendation to construct a direct `cmd.exe /D /C` command merely to suppress AutoRun. Microsoft documents that `/C` quote preservation is conditional; a quoted batch path plus other quoted arguments can be mangled. **Proposed initial approach:** launch the `.bat` using normal tested `Popen` invocation, and have a preflight check inspect both HKCU/HKLM `Software\Microsoft\Command Processor\AutoRun`; if an AutoRun setting could affect execution, fail clearly or escalate for a separately designed and proven explicit command invocation. Do not silently change the user's registry. If `/D` suppression is ultimately wanted, test a correctly formed `/D /S /C` *outer-quoted* command on actual Windows with tricky paths before approving it. Tests W-19 and W-24 include quotes and AutoRun.
2. **A-2 — active `.venv` normalization:** Wrapper recognises its own project `.venv` whether `VIRTUAL_ENV` is written with different slash/case/trailing separators or a normalized absolute path. It must not reject normal coordinated children that inherited the project's activated environment. Validate effective child `sys.prefix` against the project environment as the definitive check, rather than trusting a string variable alone. Expand W-04.
3. **R2 capacity note and APPROVED erratum:** The ratified 1–12 allowance **includes six**. `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` now **APPROVES** the narrow operational interpretation of literal 1-vs-12 acceptance/benchmark wording, fit/readout seed identities and the single `.bat` dependency authority. **ERR-R2-02 / Option F remains provisionally approved, pending actual Windows tests and review**. The original ratified R2 v0.3 file remains unchanged.
4. **R3 interface:** R3 v0.2 independently addresses deterministic, label-neutral tied readout and updates the runtime/dependency references. No prediction tie breaker should be implemented in this architecture draft.

> **Important distinction:** Independent executable programs do **not** require each program to duplicate input validation, argument parsing, probability selection, output formatting, or numerical utilities. Imported common modules are reusable source code, **not a shared Python process, shared mutable memory, or a compulsory central experiment runner**.

## Earlier revision overview — v0.1 to v0.2

This is a **full replacement discussion draft**, not a ratification. All original architectural/scientific safeguards and open design questions remain, unless a later explicit owner direction modifies the *proposed implementation*.

1. Incorporated Claude's independent Windows subprocess research, version **v3 (22 October 2026)**, identifying CPython's Windows venv redirector as an **implementation detail**, recommending process self-reporting, process-tree cleanup and a post-upgrade test gate.
2. Added **Option F**: coordinator invokes the same `Run_Experiment.bat` used for manual execution; this is the owner's preferred provisional common launch path, conditional on real Windows testing. `cmd.exe` is an additional process; it does not abolish PID/termination concerns.
3. Preserved the owner's explicit **environment checking + temporary activation + restoration** in both human-facing launch wrappers. Claude's suggestion to remove activation was **not accepted**. The explicit project `.venv` interpreter is still used.
4. Added a third root-level batch utility, **`install_upgrade_dependencies_into_venv.bat`**, with the **authoritative package list and pip operations INSIDE the `.bat`**. Do **not** impose a separately maintained `requirements.txt`; optional version snapshots are generated artifacts only.
5. Changed the **first-implementation default and initial maximum concurrent experiments to six (6)**; revised memory-pressure and concurrency proof-of-concept tests accordingly. Ratified R2 v0.3 permits 1–12; its literal 1-vs-12 test/benchmark examples are now governed by the owner-approved narrow R2 erratum v0.2. The historical R2 file itself remains unchanged; ERR-R2-02 launcher implementation remains conditional on Windows tests and review.
6. Added lightweight `psutil` monitoring/termination (preferred; `taskkill /T /F` fallback), child self-reported runtime metrics, and an explicit ban on method-created subprocesses/pools **for the first implementation unless separately approved**. No project-created Windows Job Objects.
7. Expanded tests for CMD batch exit codes, quoting, Ctrl+C, redirection, CMD AutoRun behaviour, venv activation, six-worker ~2-GB-per-worker staged memory load, and Python/venv/dependency upgrade compatibility. **The v0.3 review corrected the previously unproven `/D /C` quote-handling proposal.**
8. **R3 v0.2 remains a separate review candidate, not yet owner-ratified.** Its `TIE_SHA256_V1` rule governs prediction-time tie resolution; the architecture does not introduce a competing tie-breaking rule.


---

## 0. Document purpose, authority and controls

### 0.1 Purpose

This document records the current software-architecture discussion, compares the approaches considered, proposes a manageable initial implementation, and identifies **explicit open questions** for further research, prototyping, and owner decisions. It is **not** an attempt to freeze all method mathematics, author the predictor now, or replace the project charter.

The design objective is to make an evolving catalogue of 62 current E-methods (eventually potentially 106 or more total methods) manageable by one maintainer, without compromising historical forecasting boundaries, prospective evidence, reproducibility, or openness to unconventional hypotheses.

### 0.2 Governing and supporting documents

| Document | Status | This draft's relationship |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_3.md` | RATIFIED | Scientific purpose and project-wide rules prevail |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | RATIFIED | Permanent E-method identity, names and research hypotheses prevail |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` | RATIFIED | Input/output, N−1, ranking, TOP/WORST, reproducibility and execution requirements prevail |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_2.md` | **REVIEW CANDIDATE** | Candidate evaluation/reporting rules; **not** treated as already ratified |
| `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` | **OWNER-APPROVED**; ERR-R2-02 provisionally accepted | Narrow operational reconciliation to ratified R2 v0.3; original R2 file unchanged |
| **This architecture discussion v0.3** | **DISCUSSION DRAFT** | Proposes how to implement the above, and identifies conflicts requiring a controlled decision |

The proposal in R2 §9.1 mentions `ProcessPoolExecutor **or an equivalent spawn-safe process worker pool**`. Independently launched Python subprocesses are intended as that equivalent, subject to acceptance tests. R2 §12.2 shows a **provisional** module/package layout, not a mandate to abandon independently executable scripts. If any final architectural selection requires changing binding R2 meaning, raise it for explicit user approval and issue a controlled revision; do not silently treat this discussion as overriding R2.

**Not decided in this draft:** final CLI option names, directory manifest, persistence schema, supported method-specific dependencies, exact per-method mathematical fitting rules, or R3 scoring policies.

### 0.3 Vocabulary

- **Experiment / method**: one permanent `E_x` scientific hypothesis, potentially with separately named revisions/variants.
- **Experiment program**: a standalone executable Python source file implementing one E-method; runnable without the coordinator.
- **Coordinator**: an optional umbrella program that launches multiple experiment programs, supervises their execution, and gathers results. It should **not** perform their method-specific mathematical fits.
- **Common utilities**: imported Python modules providing consistent input, interfaces, validation and reporting.
- **Worker**: one operating-system Python child process running an experiment program; default proposal is one active method per process.
- **Result**: a machine-readable, fully validated prediction artifact; **different** from transient console messages.
- **FINAL**: a genuine future-draw forecast frozen before the actual next draw; different from historical walk-forward evaluation and computational benchmarking.
- **Owner decisions**: explicit ratifications by the project owner; the language **proposed** below does not imply ratification.

---

## 1. Project-specific architectural requirements

An acceptable design must preserve the following already agreed requirements; choosing independent executables must not weaken them.

1. **Scientific neutrality.** All methods, including expensive, poorly performing, highly correlated, speculative and seemingly implausible methods, remain recorded and eligible for further experimentation and combinations. Speed is never a scientific veto.
2. **Same eligible game format.** Real training observations start at draw 1144 and contain seven distinct main numbers from 1–35 plus one Powerball from 1–20. Never silently import draws under earlier barrel rules.
3. **Draw-number chronology.** For historical target N, fit on admissible results through N−1. For a genuine future target, find L as the maximum validated completed draw, allow the full eligible training history 1144..L, and forecast L+1. Dates remain metadata and optional scientific features; the core engine needs no timestamps for normal draw-history prediction.
4. **Preserve the ten-draw historical holdout.** Draws 1578–1587 are held out for controlled historical testing, not withheld from a genuine next-draw FINAL fit.
5. **Separate main and Powerball results.** One method can incorporate cross-barrel past-history hypotheses but must respect each target's legal output requirements.
6. **Native TOP and WORST side by side.** For ranking-capable methods, derive and freeze both from the same fitted model and ranking, without feedback from post-draw ranking metrics. Retain a method's lawful native joint-set TOP when applicable; do not fabricate marginals or WORST for methods that cannot produce them.
7. **Rank-position is post-draw evaluation only.** A separate evaluator computes it after actual results are known. It cannot change pre-draw picks.
8. **Prospective integrity.** Keep a complete, immutable pre-draw batch of runnable experiments, variants and explicit unavailable/failure statuses. Record later outcomes separately. Nothing may be backfilled after the draw and passed off as prospective.
9. **Synthetic research separation.** Synthetic fixtures, null-world and planted-effect studies remain separately identified; their observations and fitted states do not become real forecasts. Disclosed learnings may inform later method design and interpretation.
10. **Stable prediction identity.** Random seeds and canonical prediction content depend only on the permitted training view, method/configuration and target, **not** on later source rows, the whole-source file hash, execution order, or number of workers.
11. **Reproducibility.** Equivalent standalone/coordinated execution and 1-versus-6-worker execution in the *initial implementation* shall aim for bit-identical canonical predictions on the same controlled system. **Ratified R2 v0.3 still additionally mandates 1-versus-12-worker evidence**; that requirement remains binding until the owner approves an explicit controlled change. Deviations require the specific technical justification/approval required by R2.
12. **Computational execution.** Owner's newer direction is a configurable **1–6 process** pool initially, with six the default and initial maximum, one method per process, and single-thread numerical libraries. R2's earlier 1–12 and optional 24-SMT trials are **not silently deleted**: see the reconciliation item O-POL-03. Future increases require explicit decision and separate capacity tests.
13. **Benchmark separation.** B1/B10 and differing training lengths measure timing and reliability without reporting predictive scores or merits.
14. **Project environment isolation.** All dependencies installed inside this project's `.venv`; no global package installs.
15. **Direct maintenance.** Each E-method must be executable, testable and debugged individually from ordinary Windows CMD or VS Code.
16. **Reuse without implicit fitted-state sharing.** Shared source code and immutable inputs are acceptable; another experiment's transient fit is not implicitly reused. Explicitly authorised combination methods may consume frozen versioned forecasts.

---

## 2. The three architectures considered

### 2.1 Architecture 1 — Monolithic coordinator with imported methods

One large Python process (or one large entry-point package) owns the main workflow and imports each method's functions. Some versions use in-process threads; a more capable version could dispatch imported functions to a process executor. Most control flows through shared in-memory structures.

**Advantages:** straightforward in-process function calls, central parameter parsing, little process communication, easy shared data access, tight control of workflows, and convenient reuse of common services.

**Disadvantages for this project:** a genuinely single source file would become unwieldy; individual-method command-line use is not automatic; in-process native-library crashes and shared mutable state can affect multiple methods; working around conflicting library thread pools is more difficult; a process pool brings subprocess-related concerns back anyway.

**Assessment:** viable but not preferred. A monolithic **source file** is particularly unattractive as method count grows. A module-based architecture with spawned processes remains technically possible but is closer to Architecture 3.

### 2.2 Architecture 2 — Independent executable experiment programs plus coordinator

One Python program per scientific experiment, with its own callable `main()` and normal command-line options. Each can import descriptive common utility modules. The optional coordinator finds or selects matching program files, provisionally launches each through the common `Run_Experiment.bat` and project interpreter, relays their console output, supervises failures/timeouts and reads their completed result artifacts.

**Advantages:** straightforward standalone invocation; clean process/memory isolation; explicit subprocess environment and numerical thread limits; easier method-specific debugging; no compulsory central runner; a crash need not take other methods down; dependencies and program output can be inspected independently; natural fit to the 12-physical-core host while using six initial workers; minor startup overhead is irrelevant for our computations.

**Disadvantages:** subprocess launch and lifecycle supervision; output-pipe handling; filesystem result protocol; possibility of inconsistent per-method implementations if common utilities are not used; method discovery/identity discipline; explicit coordination of dependent combination methods.

**Assessment:** **preferred discussion candidate**, using common imports and a deliberately small coordinator. **Independent program** does not mean duplicating validation, forecast schemas or output routines.

### 2.3 Architecture 3 — Coordinator plus centrally executed method modules

A main coordinator invokes a *common experiment runner*, which imports method modules that provide a standard function/class interface. Individual execution usually goes through a generic `run_method.py`, possibly inside separately spawned processes. Each scientific method is not independently responsible for its lifecycle or CLI.

**Advantages:** highly consistent lifecycle and output handling; fewer opportunities for experiment authors to bypass shared validation; easy interface introspection; changes to common behaviour can be centralised.

**Disadvantages:** direct invocation of `python methods\E_001.py` is not naturally supported without wrappers; more coupling to shared runner interfaces; more framework code up front; sometimes unnecessary complexity for a single-developer experimental repository.

**Assessment:** defensible but less aligned with the owner's preferred maintenance workflow.

### 2.4 Comparison and provisional selection

| Criterion | Arch. 1 | **Arch. 2** | Arch. 3 |
|---|---|---|---|
| Experiment directly executable by its own `.py` file | Only if engineered | **Native** | Usually wrapper/runner |
| Separate OS process per active experiment | Optional | **Native in coordinator** | Possible with process pool |
| Standalone VS Code debugging | Possible | **Simple** | Requires runner configuration |
| Shared validated input and output functions | Yes | **Yes, by imports** | Yes |
| Zero method-specific process protocol code | Possible | **Possible with common library** | Yes |
| Auto-discovery by filename | Possible | **Simple** | Usually module/registry based |
| Fault isolation | Weak if in process | **Good process isolation** | Good if spawn-based |
| Central method lifecycle enforcement | Strong | Shared utility plus validation | Strongest |
| Risk of complex framework | Medium | **Low if kept modest** | Medium–high initially |
| Per-experiment startup overhead | Lowest | Higher; immaterial | Higher if spawned |
| Directly addresses user preferences | Partial | **Strongly** | Partial |

**Working recommendation D-A01:** Adopt Architecture 2 for a limited architecture proof-of-concept. The selection is **not ratified** until the owner accepts the open points and any R2 interface implications are resolved.

---

## 3. Suggested repository layout — deliberately descriptive filenames

This structure is **illustrative**. It does not instruct anyone to reorganise existing tracked files yet.

```text
analysing_perceived_randomness_in_reality/
    .vscode/
    .venv/                                  # local; Git-ignored
    activate_venv.bat                       # existing operator convenience
    deactivate_venv.bat                     # existing operator convenience
    Run_Coordinator.bat                     # proposed operator launcher, checks venv
    Run_Experiment.bat                      # proposed operator + coordinator launcher
    install_upgrade_dependencies_into_venv.bat  # authoritative PyPI packages and maintenance
    .gitattributes                          # proposed: *.bat text eol=crlf
    doc/
        Predictive_Randomness_Research_Project_Proposal_v0_3.md
        Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md
        Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md
        Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_1.md
        Predictive_Randomness_Software_Architecture_Discussion_v0_2.md
    src/
        Powerball_Experiment_Coordinator.py
        scrape_australian_powerball_history_from_2018_04_19_v0_3.py
        methods/
            E_001_historical_occurrence_frequency.py
            E_002_expected_recurrence_interval.py
            E_003_curve_fitted_endpoint.py
            E_004_curve_fitted_gradient.py
            ...                                     # other E-method scripts
            _common/
                __init__.py
                data_input_and_validation.py
                experiment_command_line_parameters.py
                historical_training_view_and_digest.py
                prediction_ranking_and_selection.py
                experiment_console_and_file_output.py
                experiment_logging_and_progress.py
                experiment_runtime_status_and_resources.py
                runtime_environment_verification.py
                method_identity_and_result_validation.py
                project_paths_and_output_locations.py
    source_data/                                     # authoritative observational inputs
    transitory_data/                                # optional disposable scratch, ignored
    results/
        real/development/
        real/holdout/
        real/prospective/
        synthetic/
        benchmark/
    tests/
    # requirements.txt already exists in project history; not authoritative
    # No second hand-maintained package manifest is required by this design.
    .gitignore
    README.md
```

**Important filename caveat:** The above E-method filenames are *examples only*. Before writing files, copy the exact method names and E-numbers from ratified R1; do **not** rename, reassign or infer method identity from these illustrative examples. The desired convention is `E_001_descriptive_name.py` for E_1, continuing monotonically, with zero-padded filename numbers only for sorting. The scientific identifiers remain `E_1`, `E_2`, etc.

**Why put `_common` under `src/methods/`?** When Python executes `python src\methods\E_001_....py`, it normally places the script's containing directory (`src/methods`) on its import search path. The script can then import from `_common` without requiring `pip install -e .` or a hand-maintained `PYTHONPATH`. This needs a direct-run test in the actual Windows/VS Code environment. If a broader common package later becomes useful to the coordinator and evaluator, reconsider placement deliberately rather than adding arbitrary `sys.path` manipulations to every experiment.

**No hidden root-folder dependence:** Resolve the project root and default input/output destinations from a shared, verified path utility, **not** from the user's current working directory. This avoids different results when an experiment is run from the repository root, `src/`, inside VS Code or from a `.bat` file elsewhere.

**Filename policy:** Prefer unambiguous descriptive names to terse names such as `data.py`, but do not make names so long that Windows paths become unwieldy. Common file names are not method-number identities.

---

## 4. Standalone execution and coordinator execution

### 4.1 Direct execution from Windows CMD or VS Code

The owner wants to be able to invoke an individual experiment as an ordinary executable program:

```cmd
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
call .venv\Scripts\activate.bat
python src\methods\E_001_historical_occurrence_frequency.py --mode final
```

Or (proposed historical example):

```cmd
python src\methods\E_001_historical_occurrence_frequency.py --mode historical --target-draw 1500
```

These are **future illustrative commands**, not claims that E_001 exists or that its CLI is frozen. Equivalent direct-run debugging must work in VS Code using the selected environment.

**Preferred normal manual invocation:** `Run_Experiment.bat E_001_historical_occurrence_frequency.py --mode final`. For multiple methods use `Run_Coordinator.bat --mode final --workers 6`. The `.bat` wrappers are conveniences rather than scientific requirements: executing the `.py` directly under the correct venv remains supported for debugging. Both root-level wrappers must protect/restore their caller's environment; see §5A.

An experiment program must not require `Powerball_Experiment_Coordinator.py` to be running, or a service/daemon/remote API to be available. The coordinator is a convenience for multiple methods, not a scientific dependency of a method.

### 4.2 The coordinator's job

The coordinator should do only the tasks that benefit from centralisation:

- Discover candidate `.py` files by a fixed filename convention or select requested E-identifiers.
- Validate unique filenames/identities and manage declared unavailable or not-yet-implemented catalogue entries.
- Parse shared invocation settings and determine the requested target/mode/snapshot policy.
- Use the **same proposed `Run_Experiment.bat` launch pathway** for coordinated and ordinary runs, with explicit project-vEnv verification in the child; direct interpreter subprocess launch is the fallback if batch acceptance tests fail.
- Launch at most the configured number of active child processes and manage a queue.
- Apply/verify equivalent numerical thread limits and standard-output behaviour through shared wrapper/common setup, with test evidence for manual and coordinated equivalence.
- Prefix/relay console output, report aggregate progress and preserve exit status.
- Enforce timeouts, interruption and resource-aware scheduling; do not mislabel failures as zero-second successful runs.
- Locate and **independently validate** completed machine-readable prediction files.
- Coordinate required dependency ordering for combination methods; do not silently feed another method's temporary fit state into a child.
- Create a complete per-target run/batch manifest including failures and unavailable methods.
- Invoke a **separate evaluator** only when authorised and when actual outcomes are legitimately available; never let the evaluator choose or rewrite TOP/WORST.

The coordinator **should not** contain the mathematics of E_1–E_62, assign alternative E-numbers, or derive a different prediction merely because it is coordinating the run.

### 4.3 The experiment program's job

- Parse standard flags (possibly through a common utility) plus any declared method-specific flags.
- Resolve validated input and mode, construct its permitted training view, and verify N−1 or FINAL boundaries.
- Execute its method-specific mathematics in a process-local state.
- Freeze its full supported rankings and native predictions; use the common readout utilities for lawful TOP/WORST where applicable.
- Emit sensible human-readable console progress/results.
- Write the **same authoritative structured result** regardless of standalone or coordinated invocation.
- Report a suitable status/exit code; never report success if required result validation failed.

**Proposed D-A02:** Direct and coordinated execution are equivalent ways of launching the *same experiment program*. No duplicate mathematical implementations or alternate coordinator-only fit path.

---

## 5. The virtual environment question: what actually happens to subprocesses?

This is not wholly an open scientific question; the basic Python/Windows mechanism is documented. The **integration behaviour in our eventual scripts must still be demonstrated on the actual PC**.

### 5.1 What is already known

1. A project `.venv` contains its own Python executable at `.venv\Scripts\python.exe` and separate installed packages.
2. Activating the environment from CMD mainly changes the shell's `PATH` and environment variables so unqualified `python` uses that executable. Activation **is not necessary** if Python is invoked by its absolute path.
3. `subprocess.Popen` normally inherits a copy of the launching process's environment when `env` is not supplied. When `env` is supplied, that mapping is used **instead**; it must preserve necessary Windows variables.
4. A subprocess **does not run `activate.bat` automatically** simply because the parent process used a venv.
5. The recommended way for a Python program to re-launch its interpreter is `sys.executable`. If the coordinator is running inside the project's `.venv`, `sys.executable` should resolve to that environment's interpreter. The child then imports packages from the same environment.
6. `VIRTUAL_ENV` is an activation marker, **not a reliable proof** that a process is using the venv: a program can directly invoke the venv's Python even when `VIRTUAL_ENV` is unset.
7. A coordinator accidentally launched under the **global** Python would yield a global `sys.executable`. Blindly passing it to children would break our isolation requirement. This is an explicit startup validation/failure case, not an obscure exception.

**Official references:** [Python `venv`](https://docs.python.org/3.14/library/venv.html) and [Python `subprocess`](https://docs.python.org/3.14/library/subprocess.html). Their documented behaviour establishes the main answer; we still need an actual project acceptance test.

### 5.2 Proposed launcher rule — revised for Option F

The owner's preferred **provisional** execution path is:

```text
Human CMD / VS Code --> Run_Experiment.bat --> project .venv Python --> E-method
Coordinator ---------> Run_Experiment.bat --> project .venv Python --> E-method
```

**Proposed D-A03 (revised):** The coordinator shall validate its own venv. It shall provisionally invoke the **same root-level `Run_Experiment.bat`** used by a person, with explicit arguments and `subprocess.Popen` pipes. The wrapper checks its environment, temporarily activates the project `.venv` when necessary, invokes the *explicit* `%~dp0.venv\Scripts\python.exe`, and preserves the method's exit code. Child self-reporting independently checks its actual `sys.prefix`. The initial coordinator does **not** use a bespoke Windows launcher, a project-managed Job Object, or a second experiment-runner program.

`sys.executable` remains a sound **direct-launch fallback**, not the normal Option F entry point. Calling a batch file through `Popen` can invoke `cmd.exe` even if `shell=False`. Argument parsing thus crosses a CMD boundary: actual quoting, special-character handling, path spaces, return codes and Ctrl+C **must be tested**, not presumed. The coordinator must not construct unquoted arbitrary shell command strings from user content.

The preferred simple solution uses `psutil` to supervise the wrapper-rooted process tree and **does not depend on `Popen.pid` being the actual computational Python PID**. This is essential because `Popen.pid` refers to `cmd.exe` in Option F; Windows venv Python may itself be a redirector. See §5B and §14.2.

If wrapper tests fail, the fallback is a direct `Popen([verified_venv_python, '-u', script, *args], ...)` using the same common utility library, with retained independent manual wrappers. This fallback is a consciously tracked alternative, **not** silently swapped in while comparing experiments.

### 5.3 Environment inheritance versus environment selection

A child inherits an **environment-variable map**, not the parent's current Python imports, memory, package objects, interpreter state or Python execution stack. It starts a fresh interpreter process. Therefore:

- Installing a package inside `.venv` makes it available to all children launched by that `.venv` interpreter.
- Packages installed **only globally** are not automatically available in the normal isolated venv.
- An activated CMD and an activated VS Code terminal should lead to equivalent `sys.executable` if both activate the same project environment.
- `PATH`, `VIRTUAL_ENV`, temporary-directory variables, BLAS thread limits and other values can be inherited or explicitly overridden; inspect what is actually used.
- Child execution should *not* depend on `VIRTUAL_ENV` being set, even though it may be set in ordinary activated sessions.
- The project `.venv` itself must be recreated after a repository move or reinstall as appropriate; it is not portable Git content.

**Open question O-ENV-01:** Should direct experiment scripts refuse global Python and demand this project's `.venv`, or merely warn? Recommendation: fail loudly for actual research/FINAL modes, rather than silently run using different dependencies. Test mode could be less strict if explicitly authorised.

### 5.4 Minimal proof-of-concept tests for `.venv`

| Test | Setup | Expected result |
|---|---|---|
| V-01 | Coordinator launched from activated CMD | Coordinator and child both use repository `.venv` Python |
| V-02 | Coordinator launched from VS Code terminal | Same as V-01 |
| V-03 | Experiment launched directly after activation | Same Python interpreter/package imports as coordinated invocation |
| V-04 | Coordinator intentionally launched using global Python | Controlled failure with clear corrective command; no misleading success |
| V-05 | Child receives `env=os.environ.copy()` plus thread limits | Still imports packages from `.venv`; thread limits applied |
| V-06 | `VIRTUAL_ENV` unset but absolute venv interpreter used | Child still operates inside venv; detector uses `sys.prefix`, not just environment marker |
| V-07 | Project path has spaces (test copy) | `shell=False` argument list and paths still work |
| V-08 | Child logs `sys.executable`, `sys.prefix`, `sys.base_prefix` | Values confirm environment isolation; mismatch reported |

**Suggested lightweight runtime check:** `sys.prefix != sys.base_prefix` confirms some virtual environment is active. Compare resolved `sys.prefix` to the **intended repository `.venv`** to confirm it is the *right* environment. `where python` and `VIRTUAL_ENV` are valuable CMD diagnostics but insufficient on their own.

---
## 5A. Three operator-maintained Windows batch utilities

### 5A.1 `Run_Coordinator.bat` and `Run_Experiment.bat`

**The owner's explicit choice:** do not remove the environment checks or activation/restoration because an absolute executable path happens to work today. Each wrapper:

1. Uses a scoped `SETLOCAL` context to preserve the user's original CMD environment; use `ENDLOCAL`/automatic scope restoration on exit and preserve the Python program's exit code.
2. Locates the repository root using its own `%~dp0` location; fails clearly if `.venv` or expected Python/activation script is absent.
3. Determines whether **the project's own `.venv` is active, none is active, or some other virtual environment is active**. If already correctly active, keep it. If none is active, `CALL` the project's activation script **inside** the local environment and check success. If a different environment appears active, fail clearly initially, rather than silently switching.
4. Verifies the actual Python environment used rather than trusting `VIRTUAL_ENV` alone. The program's shared Python startup utility checks `sys.prefix` against the project `.venv`, including when Python was invoked directly without shell activation.
5. Invokes the explicit project `.venv\Scripts\python.exe` rather than bare `python`. Activation and explicit interpreter selection serve complementary maintenance purposes; the actual child-interpreter identity, not the activation banner, is authoritative.
6. Establishes standard numerical thread-limit environment variables *before* Python imports NumPy/SciPy, so manual and coordinated method execution are equivalent. Exact settings/overrides are measured rather than assumed.
7. Relays normal console streams without inventing extra mandatory line protocols, and returns the Python exit code unchanged even after `POPD`/`ENDLOCAL`.
8. Does not globally install packages, start a project-owned Windows Job Object, or silently download anything when starting experiments.

**Experiment-wrapper parameter convention:** the wrapper receives the script filename as its **first** argument, with the remaining arguments for the experiment, for example:

```cmd
Run_Experiment.bat E_027_example.py --mode historical --target-draw=1577 --history-length=100
```

The simple candidate changes the current directory temporarily to `src\methods`, and invokes `"%PY%" %*` so Python treats the first argument as the script. **Do not rebuild `%*` via `%1`/`SHIFT`/`%2...`**, since that has tricky CMD parsing and may corrupt `--option=value` or quoted arguments. Preserve literal arguments from normal CMD use, while separately defining and testing safe arguments passed across the coordinator-to-CMD boundary.

**Caveat:** changing the current directory to `src\methods` changes how an experiment interprets relative path parameters. A common argument/path utility must resolve project-relative paths from the verified project root; the prototype must compare use from another current directory. If it proves too restrictive for legitimate external input paths, decide explicit absolute-path or `--project-root` semantics before implementation.

Batch files must be checked in with **CRLF** line endings. Proposed `.gitattributes` addition:

```gitattributes
*.bat text eol=crlf
```

`Run_Coordinator.bat` launches the coordinator under the verified project Python with forwarded coordinator options; it is separate from the *coordinator's own* repeated calls to `Run_Experiment.bat`. Neither wrapper should install/upgrade packages as a side effect.

### 5A.2 `install_upgrade_dependencies_into_venv.bat` — one self-contained authority

**Owner requirement, superseding the earlier `requirements.txt` proposal:** one human-runnable root-level batch file shall contain **all pip/PyPI dependency names, any approved version constraints, and their install/upgrade commands in an obvious editable section within that same `.bat`**. A maintainer runs one file from time to time and can inspect all required packages by opening that one file. Do **not** require a separate manually maintained `requirements.txt`, `pyproject.toml` dependency list or Python package manifest as a precondition for this functionality.

The maintenance script shall, when explicitly invoked:

1. Locate/verify the project-local `.venv`; manage activation inside a `SETLOCAL`-protected scope, preserve the user's original CMD environment, and use `.venv\Scripts\python.exe -m pip` **explicitly**. Do not use the global `pip` or pip invoked from a different venv.
2. Show its readable, **complete authoritative list** of named direct dependencies. The initial candidates include existing `requests` and `beautifulsoup4`, and anticipated `numpy`, `scipy`, `psutil` and any additional *actually required* PyPI packages. **Candidates are not assertions that they are already installed or that every method needs them.** Include `threadpoolctl` or other packages only when selected by the implementation.
3. Provide a deliberate **install/verify** operation and an explicit **upgrade** operation. The latter should update only packages permitted by the script's constraints. If constraints are exact pins, changing the version requires an intentional edit of the script; do not pretend a pinned install automatically upgrades to a new release.
4. Report interpreter and pip versions; run `python -m pip check`; display all required installed package versions, and stop/return nonzero on installation, conflict or verification failures.
5. Produce an optional, automatically generated package-environment snapshot (for example `pip freeze` + version/provenance record). The snapshot is **evidence**, not a second dependency list a human must maintain. Each consequential benchmark, immutable FINAL batch, once-only opening of the original ten-draw holdout, and historical evaluation supporting substantive conclusions archives the resolved Python/PyPI environment snapshot (and a reference digest); not just package names from this script.
6. Show clearly that a package upgrade can change floating-point behaviour or availability, potentially affecting canonical forecast bytes. Re-run the Windows subprocess/venv compatibility gate and scientific reproducibility checks **before accepting a changed environment for actual research/FINAL forecasting**; do not silently upgrade during a coordinator/experiment invocation.
7. Preserve the initial/return environment and meaningful exit status even on error. Keep `.bat` CRLF and subject it to CMD quoting/path/activation tests.

**Existing `requirements.txt`:** it may currently be a tracked project file. This discussion **does not delete or change it**. Before implementation, decide whether to retire it, retain it as historical information, or **generate** it for external tooling from the `.bat` package list; it must not become a second independently edited authoritative package list. No file-system mutation is authorised by this draft.

**Dependency lifecycle:** developers deliberately update the .bat list when a new E-method adds a direct PyPI requirement; review whether its version constraints need adjustment; invoke the maintenance script; verify; record version snapshot in experiments and commit the script revision. Distinguish *approved research environment* from merely *latest PyPI packages*.

**Open question O-PKG-01:** Exact default switch syntax (`/INSTALL`, `/UPGRADE`, or no-argument install/upgrade), initial package/version constraints, whether `pip` itself upgrades, and whether verification runs automatically after maintenance. Proposed answer: clearly printed modes, no silent upgrades, built-in verification; settle during P0/P2.

**Open question O-PKG-02:** How to treat the existing tracked `requirements.txt` without dual-maintenance. Proposed answer: `.bat` alone is authoritative; other manifests, if needed, are generated/read-only derivative artifacts.

### 5A.3 Wrapper-specific acceptance criteria

- Manual call from ordinary CMD with no active `.venv`, from a project-activated CMD, and from a shell with a **different** `.venv` active must behave exactly as documented, without changing the caller's environment.
- Arguments including `--history-length=100`, spaces, `=`, `,`, `;`, quotes and approved project paths must arrive intact **in the modes that promise support for those characters**. CMD `&`, `%`, `^`, `|`, `<` and `>` need explicit documented restrictions or correct tested escaping; do not label a string safe without testing the actual CMD boundary.
- **Do not assume `cmd.exe /D /C` preserves nested quotes.** Microsoft's `/C` quoting rules are conditional: the initial and final quote may be stripped if the command string contains multiple quoted segments. Default to a standard, individually tested `.bat` launch through `Popen`; check for relevant CMD `AutoRun` registry settings in HKCU and HKLM at startup and report/block unexpectedly configured AutoRun rather than silently editing registry keys. Explicit `/D /S /C` with an outer-quoted command is a possible later solution **only if tested**, particularly for spaces in the batch path and other quoted parameters.
- `CTRL+C` across several wrappers must not leave a `Terminate batch job (Y/N)?` prompt hanging or falsely record success.
- Batch CRLF, return codes, output pipes and process-tree termination must be tested on the user's actual Windows/venv installation.

---

## 5B. Python-release-independent subprocess accounting and supervision

### 5B.1 Documented interfaces versus current CPython implementation

Documented: Python `subprocess.Popen` supports command-line parameters, pipes, status codes and timeouts; a Windows `terminate()`/`kill()` applies to the **identified process**, not a promise to remove every descendant. A `Popen.wait(timeout)` expiration does not itself stop the program. When a batch file is involved, CMD parsing and process identity become additional considerations.

Claude's review of the **then-current CPython source** indicates Windows venv `python.exe` can be a redirector that launches the actual interpreter with inherited streams and returns its exit code. Current launcher code reportedly uses an **internal Job Object**; that is **not a Python-version-independent documented API contract** and must not be relied on for our termination semantics. Under Option F the `Popen.pid` is normally the CMD wrapper process, not the computation. Neither direct mode nor wrapper mode may assume a specific fixed number of Python processes in future releases.

### 5B.2 Proposed minimal monitoring contract

- Every experiment writes an atomic, uniquely named small **runtime status file** through a shared helper. At STARTED, report its actual `os.getpid()`, process creation identity/time (sufficient to guard against PID reuse), actual `sys.prefix`, launch mode/identity and start time. At normal completion report success/failure, `time.perf_counter()` elapsed duration, `time.process_time()` CPU time and actual **peak process working set or other accurately labelled memory measure**. A hard crash/kill may leave only STARTED; it must not be mistaken for zero CPU/memory or a successful run.
- The coordinator records its own per-worker elapsed wall time and samples **system-wide available RAM** for admission/safety, particularly with six processes on 32 GB RAM. Do not conflate system-wide memory pressure with precise per-experiment usage or confuse peak working set with memory allocation/commit.
- Use `psutil` initially for resource information and for enumerating/waiting on a process tree. `taskkill /PID ... /T /F` is a documented fallback if psutil is unavailable; it is a forced cleanup rather than a graceful shutdown. `psutil` API/field/version changes are checked as part of environment maintenance.
- A timeout/cancel first identifies the wrapper-rooted tree **while the parent is still alive**, kills/waits for the relevant processes, and verifies that the experiment's independently self-reported PID has exited. Guard against PID reuse using creation-time identity before terminating a process by PID. If a process is unaccounted for or survives, report `ORPHAN_SUSPECTED`, do not mark an ordinary success, and avoid prematurely reusing the worker slot.
- Only accept subprocess-running methods as an explicit, later-approved extension. For first implementation, **experiments must not spawn their own child processes/pools**. This is not an E-method exclusion: an affected E-method remains in the scientific catalogue with a visible unsupported/unavailable execution state pending an approved design.

**No project-owned Windows Job Objects** in the initial implementation. Their more comprehensive process-lifetime guarantees would add Windows-specific API machinery beyond our demonstrated need. If a later method needs nested process trees, reconsider the simplest adequate mechanism with fresh tests; do not permanently rule out a justified change.

### 5B.3 Compatibility as an observable contract

After upgrading Python, rebuilding `.venv`, upgrading psutil/numerical packages or materially editing the wrapper, rerun the P0/P2 Windows compatibility suite. The acceptance standard is **observable behaviour** (arguments, pipes, statuses, memory reports, effective interpreter, cleanup and deterministic results), **not** the continued presence of a venv redirector or any CPython-internal Job Object.

**Open question O-PROC-01:** Select `psutil` as the principal tree-control/monitoring helper with a tested `taskkill` fallback? **Recommendation:** yes, provisionally; verify creation-time/PID reuse logic and installation via authoritative dependency `.bat`.

**Open question O-PROC-02:** Any project-managed Job Object needed initially? **Recommendation:** **no**; defer until evidence from an approved nested-process method warrants it.

---

## 6. Experiment discovery and permanent method identity

### 6.1 Owner preference: filename discovery

The coordinator can scan the single controlled directory `src/methods/` for filenames matching a restrictive convention such as:

```text
E_001_descriptive_name.py
E_002_descriptive_name.py
...
E_062_descriptive_name.py
```

The scanner should **not recurse into** `_common`, `tests`, virtual environments or arbitrary folders. A mere `.py` extension is not sufficient. Discovery should be deterministic (e.g. sort numerically by parsed E-identifier) and report duplicate numeric identifiers, malformed names, unavailable scripts and invalid file locations.

The user reasonably prefers management discipline over an elaborate plugin-registration framework. **No Python import/registration ceremony should be necessary merely to discover a standalone executable.** It can announce its own name/identity in the generated result, and the coordinator can verify those against the parsed filename.

### 6.2 But discovery alone cannot establish the complete scientific roster

This is a subtle difference between *finding implemented programs* and *retaining every E-method*. Our ratified contracts require all E_1–E_62 to remain in the project catalogue, even when not implemented, failed or temporarily unavailable. A directory containing only implemented `.py` programs cannot, by itself, prove that the absent E_061 program is **not yet implemented** rather than accidentally forgotten.

**Minimal proposal, without an elaborate registry framework:** maintain one small, human-readable **method inventory** listing every permanent E-identifier and approved descriptive name. It may be a simple CSV/JSON file or another machine-readable format chosen by the owner. Each entry has a status such as `NOT_IMPLEMENTED`, `READY`, `DISABLED_BY_OWNER`, `UNSUPPORTED_INPUT`, or `FORMULA_OPEN`. File paths can be inferred from `E_###_*.py` rather than redundantly hard-coded.

The coordinator then compares *what exists on disk* against *what the approved catalogue says ought to exist*, while running only runnable programs. A FINAL batch includes explicit absence/failure status for catalogue entries not runnable for that target. This meets R2's roster requirements without forcing a Python plugin architecture.

**Open question O-DISC-01:** Which is the smallest acceptable source of permanent E-identities: a separately maintained manifest, a generated catalogue from ratified R1, or a manually maintained index verified in tests? **Recommendation:** a tiny explicit manifest; neither dynamic imports nor an enterprise-style registry service.

**Open question O-DISC-02:** Should experiments automatically enter a production FINAL batch merely because a validly named `.py` file appears? **Recommendation:** filename discovery makes them visible, but production readiness is confirmed by required tests/status in the tiny catalogue. This does not disqualify the method scientifically; it prevents a broken or work-in-progress program from being misrepresented as a valid frozen forecast. Keep its failure/unavailable status visible.

### 6.3 Script-reported identity is checked, not trusted blindly

A method should declare its permanent E-number, a descriptive name, implementation revision, mathematical variant and supported modes. The coordinator compares these with the filename/catalogue and **does not silently relabel discrepancies**. The method may expose these through a cheap `--describe` invocation or the result file; the former is an **open convenience**, not mandatory infrastructure yet.

Methods may use separate named *variants*. A scientific change requiring a new E-number is decided through the ratified governance; the filename convention never generates new scientific identifiers on its own.

---

## 7. Command-line options and mode contract

### 7.1 Shared, human-maintainable options

**Illustrative** options (actual spelling not ratified):

```text
--help
--describe
--mode final | historical | benchmark-real | benchmark-synthetic | synthetic
--target-draw N
--history-length all | integer
--source-data path
--draw-order-data path
--result-directory path
--run-id identifier
--seed identifier-or-integer
--progress-interval-seconds N
--verbose
--quiet
```

The coordinator accepts additional selection options such as `--methods E_1,E_2,...`, `--all-ready`, `--workers 6`, `--timeout-seconds ...`. A method should accept the common arguments where applicable and can declare its own mathematical options; undocumented options must not become hidden defaults.

In FINAL mode, `--target-draw` ordinarily should be **derived automatically as L+1**, not typed. If supplied, validate that it equals L+1 or deliberately reject it, rather than accidentally permit a stale future target. For historical mode, `--target-draw N` is explicit and the training view ends at N−1.

Default input locations should come from the verified project directory and a controlled latest-snapshot policy, not simply whichever file has the newest filesystem timestamp. Snapshot discovery, validation and pinning are common utilities.

### 7.2 Two competing ways to handle standalone/coordinator inputs

**Option A — Each experiment opens source data itself via common loader.**

- Simplest direct execution; very little data transfer.
- Common code validates source snapshots, determines cutoffs and enforces permitted training views.
- Requires adversarial tests to ensure the individual experiment does not bypass cutoff logic.

**Option B — Coordinator materialises a restricted input snapshot for each child.**

- Adds a second layer against accidental look-ahead and allows smaller read-only input files.
- Extra temporary-file life cycle, although source datasets are small.
- Standalone runs still require the common loader and equivalent restrictions.

**Recommendation for a first implementation:** use Option A, with a shared strict training-view utility, immutable source snapshot identity, and R2's mandatory leakage mutation tests. Add Option B as a defence-in-depth trial if helpful. **Important:** separate OS processes with the same Windows user permissions are **not security sandboxes**; a child can generally open repository files unless access is constrained separately. We should not claim that a cutoff argument makes unaudited code physically incapable of reading future outcomes.

### 7.3 Source arguments and full-view restrictions

Every method should receive an authorised logical observation view (`UNORDERED_SET`, `DRAWN_ORDER`, or an approved combination) and a pre-target cutoff. It should be impossible for a default to silently switch an order-aware method between sorted and operator-labelled draw-order data. Both CSV views refer to the **same** underlying draws, not independent observations.

Combination experiments receive **explicit frozen source-method forecasts** and dependency identities—not a shared directory of transient model fit states that happens to exist.

---

## 8. Human-readable console output and machine-readable files

### 8.1 Two representations of one authoritative forecast

The owner wants informative console output both when an experiment is run by hand and when it is launched through the coordinator. I agree.

**Proposal D-A04:** Every experiment emits:

1. **Readable console text**: BEGIN, identity/description, mode, target, train range, progress, method duration and TOP/WORST side by side, completion/failure.
2. **One authoritative validated structured result file**: complete frozen rankings where available, method/native TOP selection, WORST/inverse readout where lawful, identities, input digests, status and provenance.

The console should be a rendering of the same internally validated result object **after** selection is frozen, not a second independent prediction calculation. It may omit large arrays for readability; the result file is complete.

**Illustrative human console output — numbers invented; not a real forecast:**

```text
==========================================================================
BEGIN E_001 — Historical Occurrence Frequency
MODE:    FINAL_NEXT_DRAW
SOURCE:  validated eligible current-rule history
TRAIN:   Draws 1144..1587 (444 observations)
TARGET:  Draw 1588

TOP:     02  07  11  18  24  30  35       PB 09
WORST:   01  05  13  19  22  28  33       PB 17

RESULT:  results/real/prospective/.../E_001/...json
STATUS:  SUCCESS
FINISH E_001
==========================================================================
```

Use stable delimiters, descriptive labels and human-friendly formatting, but **do not attempt to parse the displayed numbers as the authoritative forecast**. Machine readers use the result file.

### 8.2 Console piping with the coordinator

The coordinator can launch a child with a **single merged output stream** (`stderr=subprocess.STDOUT`) initially. It relays complete lines to its own console, prefixing `[E_001]` if multiple children are active. It may simultaneously append lines to a per-method log. This avoids inventing a full binary or RPC protocol just to communicate status and text.

Python/Windows pipes have limited buffers. The coordinator **must continuously consume output for every active child**; otherwise a verbose process can block on a full pipe. If concurrent pipes are used, a dedicated reader thread per active **child output stream** is a reasonable implementation detail; these are I/O threads, **not computational workers**. Alternatively, a tested asynchronous supervisor is possible, but not required on day one.

For immediate line visibility through Option F, the wrapper should invoke the project Python with `-u` or set `PYTHONUNBUFFERED=1`, and the experiment should flush progress where appropriate. On Windows, when capturing through a pipe with `encoding="utf-8"`, explicitly request `PYTHONIOENCODING=utf-8` in the child to prevent a mismatch with legacy redirected-output encodings. The coordinator should avoid treating every unstructured line as a protocol event. A child can print traceback or diagnostic text without causing loss of result identity.

**Open question O-OUT-01:** Is merged stdout/stderr sufficient for the first release, or must the two remain separately recorded? **Recommendation:** merged for straightforward reliable relay initially, with status and errors also captured in structured logs; preserve separate streams later if a demonstrated need arises.

### 8.3 Progress reporting and heartbeats

The **coordinator** can show each process's wall-clock elapsed time even if that method emits no output. That does not require the experiment to print a line every five minutes. Each long method can optionally report fitting iteration, percentage or completed target count at a configurable interval. Avoid inventing progress percentages when the computational work has no meaningful bounded denominator.

**Proposed defaults:** sparse method-start messages; optional progress roughly every 5 minutes for lengthy experiments; coordinator status displayed at a user-chosen interval. These are convenience settings, not scientific controls or grounds for cancellation.

### 8.4 File names, destinations and immutability

- Default result paths should be derived from **mode, target, method ID, version/variant and unique run identity**, not merely an easily overwritten `result.json` in `src/methods`.
- Standalone and coordinated runs must resolve identical default **root folders and file conventions**, although separately initiated runs can have distinct `run_id`s.
- Write to a temporary file in the **same destination filesystem**, flush/close, validate, then replace/rename into a final result *only if this target/run is allowed to create it*.
- A failure must not leave an apparently successful complete result; distinguish `SUCCESS`, `FAILED`, `TIMEOUT`, `UNAVAILABLE`, `PARTIAL_DIAGNOSTIC`, etc.
- Do **not** silently overwrite a frozen genuine pre-draw result or retroactively edit a prior prospective batch. Repeating a command after a draw produces a separately labelled retrospective run.
- The coordinator should not declare a full FINAL batch complete solely because programs returned exit code 0: it also validates expected method files, matching input/target identities and the presence of validated final result payloads or explicit exception statuses.

**Proposed D-A05:** Final prediction files are authoritative; console output is human-readable, visible, and logged, but never a substitute for structured results.

---

## 9. Structured result schema — architecture-level sketch

Do not freeze precise JSON keys in this discussion. The required **conceptual fields** are:

| Category | Examples of required content |
|---|---|
| Experiment identity | `E_x`, exact ratified name, implementation revision, mathematical variant, data-view identity |
| Run identity | stable mode, target draw, run/batch identity, whether direct/coordinated |
| Input identity | admissible draw range, input view type, SHA-256 of permitted training view, source snapshot provenance separately |
| Seed and fit | root-seed/config scope, true fitting/sampling model revision, permitted warm-start lineage |
| Prediction | lawful native TOP main/PB outputs; WORST/inverse when genuine rankings exist; full ranked labels/scores/ties; optional joint/ordered data |
| Status | success, partial capability, abstention/unavailable reason, numerical failure, time limit, process crash |
| Runtime provenance | Python executable/version, package versions, platform/backend as appropriate |
| Integrity | canonical serialization/version, content digest, output schema revision |

**Two levels of identity must not be conflated:**

- **Prediction-content identity:** from *permitted* training-view digest, method model/configuration and target. It must remain unchanged if later draws are appended or modified.
- **Run/source provenance:** may record full-file snapshot hashes, actual execution date, operating system and other information that legitimately changes between executions. Such metadata cannot be fed backward into historical fitting or canonical prediction bytes.

Further split the stochastic identity into `fit_sampling_model_version` and a downstream `readout_selection_rule_version`. Changing how a frozen ranking is displayed/read as TOP or WORST must **not** perturb the model's fitting seed; an actually stochastic sampling readout can have a separately defined readout seed where needed.

The format of TOP/WORST console lines and machine output must preserve methods with native whole-set forecasts and methods for which no complete genuine ranking exists. A fabricated WORST or a post-draw rank-position-based alteration would violate R2.

**Open question O-SCHEMA-01:** Should canonical forecasts use JSON, JSON Lines, or a pair of machine-readable JSON and human-readable text/CSV? **Recommendation:** one complete, UTF-8 JSON result per method-target-run, plus text console/log. CSV can be an optional later aggregate export. JSON Lines is useful for streamed events, but is not necessary for complete forecast identity.

**Open question O-SCHEMA-02:** Freeze path and serialization details in a small interface spec before coding. R3 scoring implementations must read this stable schema and must never rewrite the original prediction file.

---

## 10. Parallel scheduling on the Ryzen 9 3900X

### 10.1 First release: simplest viable scheduler — six workers

- The owner's updated instruction is a configurable **1–6 active experiment processes, default = 6, initial maximum = 6**. Each normally executes one scientific E-method `.py` through its own batch wrapper (Option F). This replaces the previous proposed default of twelve, but **R2's separately ratified 1–12/1-versus-12 requirements must be reconciled in a narrow controlled decision** (O-POL-03).
- The coordinator fills available slots from its queue; a slot is freed only once the experiment and its relevant subprocess chain have been confirmed complete/terminated and its results/status validated.
- Each method program owns sequential historical targets when warm starts depend on previous fits.
- A long method does not block unrelated methods except through process slots or resource-admission rules.
- **No default 12-worker or 24-worker SMT stress runs.** Such scaling experiments are deferred until explicitly authorised and resources justify them; the ratified R2 historical wording and its approved operational erratum v0.2 remain traceable.
- **Avoid nested parallelism.** In the first implementation an experiment does not create its own subprocess/process pool; restrict numerical-library internal threads to one initially, with documented controlled exceptions if genuinely needed.

### 10.2 Internal numerical libraries and environment

Environment candidates include `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS` and, where warranted, `threadpoolctl`. **Which are relevant depends on installed packages and NumPy's BLAS backend;** do not assume every variable controls every library. A method may later need explicitly approved exceptions for internal threads or GPU/accelerator use.

Under Option F, put equivalent early numerical-thread environment settings in `Run_Experiment.bat`, so standalone and coordinated executions pass through the **same configuration**. The coordinator may supply inherited environment variables as well, but the wrapper's effective contract must be verified **before the experiment imports heavy numerical libraries**. Direct `.py` debugging must either reproduce that setup explicitly or disclose any environmental difference; do not silently claim bit-equivalence. Record and test the effective BLAS backend and thread count.

### 10.3 RAM and oversubscription

The initial six-worker limit creates **approximately 12 GB of nominal experiment allocations when six methods each allocate ~2 GB**. This is *not* a guaranteed 12-GB system working set: Python interpreters, native libraries, coordinator/CMD/venv helper processes, the OS and cache consume additional memory, and exact allocation/working-set behaviour varies. The 32-GB machine still requires staged admission and system-available-memory monitoring to avoid making Windows unresponsive. Capture per-experiment self-reported peak memory separately from system-level telemetry. Observing memory does not impose a hard Windows memory limit.

**Owner direction recorded under O-CPU-01:** six is the initial default and initial maximum for this proposed implementation, subject to 1–6 configurability; **not an open default-choice question**. Validate one versus six, and six simultaneous ~2-GB allocations *progressively* with headroom/abort criteria. Reference the approved R2 erratum v0.2 when interpreting earlier 1–12/1-vs-12 language; do not silently rewrite ratified R2 v0.3.

### 10.4 Dependency-aware combinations

Most methods are independent. A combination method may require forecasts from another method for the *same target* and admissible information boundary. When that occurs, record an explicit dependency graph and execute the combination only after its frozen dependencies are available, or report dependency unavailability.

The dependency graph must not have cycles, and should not allow a method to import a later actual result by querying another method's post-draw evaluation. E-methods retain identity and eligibility even when a dependent forecast cannot be computed for a particular target.

### 10.5 What is intentionally deferred

Do not initially implement method-internal distributed optimisation, subprocess trees, remote execution, GPU scheduling, Python's optional free-threaded runtime, or a sophisticated workload queue. They can be considered after measured benchmarks justify them.

---
## 11. Timing-only benchmarking: simple modes, no scoring

The benchmark is a **software engineering instrument**, not a method-selection instrument. It can inform which numerical implementation, process count and training-history size is practical; it must not display a method's winning numbers, compare with historical outcomes, or rank scientific merit.

### 11.1 Benchmark settings

Proposed user-friendly parameters:

- `X` = number of historical target draws being timed, ending immediately before the reserved 1578–1587 holdout.
- `W` = preceding training observations per target: `all` or an integer count.

Presets:

| Preset | X | W | Targets at current snapshot |
|---|---:|---|---|
| B1 | 1 | all | Draw 1577; training 1144..1576 (433 observations) |
| B10 | 10 | all | Draws 1568..1577; varying full-history counts 424..433 |
| B1-short | 1 | 100 | Draw 1577; training 1477..1576 |
| B10-short | 10 | 100 | Draws 1568..1577; each has 100 preceding observations |

A 10-draw *training* set may be useful as a smoke test, but timing it alone is not representative of costly full-history model fitting. Retain full-history and 100-history comparisons to assess scaling. Benchmark targets are **development draws**, not the final ten-draw holdout.

### 11.2 Benchmark metrics

Measure startup/import, fitted-model computation, prediction/readout and result-serialization time separately where the experiment can truthfully report them; include total elapsed and CPU time, peak process memory, success/failure/timeout and environment information. Record a short report without revealing actual predicted numbers or historical hit scores. Maintain full canonical forecast data only in controlled test evidence when needed for equality checking, not in a timing report.

Default repeat count could be three for cheap tests, with a recorded smaller count for expensive methods. Compare one coordinator worker with six in the initial implementation; any 12/24-worker extension remains deferred and must reconcile ratified R2 requirements. **Same input + same method configuration** should give the same canonical predictions irrespective of the number of coordinator workers.

Use Windows/NumPy diagnostics to verify the actual BLAS library and internal thread count. Recording an environment variable without checking whether the library respects it is not sufficient proof of thread pinning. `psutil` is a provisionally selected direct venv dependency, to be listed explicitly inside `install_upgrade_dependencies_into_venv.bat` and installed only when the owner runs it; Python's `tracemalloc` alone cannot see all native NumPy allocations.

### 11.3 Per-method timeouts

An exceeded time limit or crash is a **failure status**, not a measured successful duration. A run may record the actual elapsed time up to failure, but cannot treat it as the method's completion time. Performance warnings or poor scaling never cause scientific method deletion.

**Open question O-BENCH-01:** Do we need fine-grained timing events from every experiment on day one, or is a simple whole-process elapsed time enough for the initial prototype? **Recommendation:** the initial architecture prototype can use total elapsed and a child-reported fit/predict split when readily available; formal R2/R3 benchmarking adds the full required metric set before acceptance.

---

## 12. Historical, FINAL and evaluation lifecycles

### 12.1 Historical walk-forward predictions

For target `N`, all methods receive the same allowed cutoff ending at `N−1`. A method may use its declared 100-draw rolling window or another mathematically declared history length, but may not read `N` or later observations to select or fit the prediction. Its fitted result and ranking are frozen. **Only then** is a separate evaluation run allowed to load the known actual draw N.

The source snapshot can grow between runs; this must not alter the canonical historical prediction for an earlier N if its permitted pre-N view is unchanged. R2's adversarial mutation/append test applies to direct and coordinated execution.

### 12.2 FINAL real-world prediction and weekly continuation

1. Validate the newest real source data and identify `L` as the last completed draw number.
2. Permit eligible data 1144..L to each method (subject to its separately defined rolling-window mechanism); the historical final-ten holdout restriction does **not** apply here.
3. Construct a full target `L+1` batch roster from the permanent method inventory and selected approved variants.
4. Launch independent experiment programs within the worker limit, collecting original/native TOP plus WORST side by side where supported; preserve failures and unavailable outcomes.
5. Freeze each completed method result and the complete batch manifest **before** draw L+1; commit and push the batch with evidence of timely publication under the ratified requirements.
6. After L+1 actually occurs and its results are published, run the **separate post-draw evaluator**. It calculates TOP/WORST matches and rank-position summaries without changing frozen forecasts.
7. Append/verify newly published actual source data, producing a new source snapshot; predict new L+1 (the following draw).

A standalone experiment execution can make a technically valid pre-draw prediction, but it should **not automatically claim to be part of a complete prospective batch** unless it has been included and immutably published under the full FINAL procedure. This distinction prevents later improvised standalone reruns from masquerading as part of the original weekly set.

### 12.3 Full completion is not equivalent to suppressing unavailable methods

A method with an unresolved formula, missing approved dependency, numeric failure or unsupported required observation view remains in the **method inventory and batch status**. The coordinator does not fabricate its predictions or hide it. “Complete batch” means complete accounting for the ratified roster and declared variants, **not** that all 62 mathematical methods have miraculously become runnable.

### 12.4 Rank position and reporting boundaries

The post-draw evaluator sees the frozen ranking and actual draw. Its rank-position metric is *evaluation-only*. Neither standalone program nor coordinator may use actual rank positions to change already-produced TOP/WORST outputs; any later predictive idea based on historical rank-position scores requires a separately declared, pre-target, method/ensemble version and governance decision.

---

## 13. Scratch files, persistent results and controlled restarts

### 13.1 Data-folder roles

| Root directory | Contents | Reuse policy |
|---|---|---|
| `source_data/` | validated real observation snapshots | Authoritative, read through controlled input logic; not ordinary scratch |
| `transitory_data/` | temporary files if a method really needs disk-backed storage | Disposable, per run/method namespace; ignored by Git; **never automatically re-input** |
| `results/real/...` | archived actual-history predictions, held-out evaluations and genuine future forecasts | Versioned/immutable under the relevant mode; never silently overwritten |
| `results/synthetic/...` | labelled null/planted/identifiability experiments | Separate evidence; never silently treated as actual outcomes |
| `results/benchmark/...` | runtime/resource/failure reports | **Timing-only**, not predictive merit |
| `doc/` | versioned specifications/research/decision records | Documentation, not fitted state |

**`transitory_data/` is optional** and should not be created until genuinely needed. Add `/transitory_data/` to `.gitignore` when introduced. A temporary file should have a unique run/method path to prevent concurrent workers colliding; use in-memory data for ordinary 444-row input handling.

### 13.2 Checkpoints and warm starts

Some E-methods will eventually take many hours or days. Resuming may be valuable, but this is not the same thing as opportunistically reading yesterday's scratch file.

A future checkpoint design must explicitly define: data cutoff identity, method/version, fitting objective, optimiser state, random generator state, numerical environment, target sequence, whether a checkpoint came from real or synthetic work, and whether its use preserves bit-level prediction identity. Restarting from a checkpoint with future information is prohibited.

**Open question O-CHK-01:** Defer resumable checkpoints until a heavyweight method actually needs them, or build them into the framework immediately? **Recommendation:** defer; maintain safe, atomic final-file handling and explicit cancellation/status now. No automatic scratch reuse.

### 13.3 Single result file versus several exports

A readable console and a canonical JSON output already provide the necessary dual representation. Additional CSV exports or pretty text summary files may be generated **from** canonical JSON after completion, but must not become independent calculations or alternative sources of truth. If such exports are introduced, record their source forecast digest.

---

## 14. Error handling, timeouts, cancellation and security boundaries

### 14.1 Failures are first-class outcomes

A subprocess may fail to start, exit nonzero, hang, raise an exception, exceed a time limit, run out of memory, produce invalid JSON, omit an obligatory component or emit a result with the wrong method/target/digest. Each has a distinguishable status and diagnostic record; none silently converts into a success or disappears from the all-method roster.

An exit code of zero **alone** is not proof of forecast completion. Conversely, a valid partial diagnostic from a method that does not have a complete ranking is not to be fabricated into a failed full prediction.

### 14.2 Cancellation and child trees on Windows — Option F

Launching an experiment by `Run_Experiment.bat` adds `cmd.exe` ahead of the venv redirector/actual interpreter. Killing just the `Popen.pid` (CMD) is **not** reliable experiment termination: Windows does not automatically kill a parent's children when the parent terminates. Current CPython redirector cleanup is an implementation detail and is not the project's contract.

**Proposed minimal protocol:** on timeout/cancellation, enumerate the wrapper-rooted process tree while it is still present, attempt bounded graceful handling where workable, then forcibly terminate/wait for the tree using `psutil` (or a documented `taskkill /T /F` fallback). Confirm the experiment PID recorded in the status file is no longer alive, considering PID reuse/creation identity. Fail visibly if confirmation is impossible; do not overwrite a successful immutable result or claim success after forced termination.

Do **not** implement a custom Windows Job Object manager or `CREATE_NEW_PROCESS_GROUP` as part of the initial architecture. An experiment must not create child processes/pools initially; exceptions require explicit review. Ctrl+C through multiple CMD wrappers, particularly the batch prompt and redirected stdin, must be verified on Windows. A five-second timeout example is merely a test fixture, not a global compute cutoff.

**Open question O-OPS-01:** Which tested approach best handles Ctrl+C through six concurrent wrappers without blocking on `Terminate batch job (Y/N)?`? **Recommendation:** use recorded tree cleanup with bounded timeout; determine whether a graceful stage is safe/practical. Do not assert unconditional success until W-18 passes.

### 14.3 Trusted source-code boundary

Scanning a folder and executing Python programs is the execution of code with the user's Windows account permissions. **It is not a secure plugin sandbox.** The project should run only trusted tracked E-method scripts, reject paths escaping the authorised `src/methods/` directory, and never pass unchecked arbitrary content through a CMD command string; test the batch-file shell/quoting boundary. Good manual repository practice remains essential.

A strict filename pattern reduces accidental launches, but it does not ensure a matching file is safe or scientifically correct. Retaining simple catalogue/status checks is an engineering safety measure, not a challenge to the owner's preference for straightforward discovery.

### 14.4 Read-only observational inputs (logical, not OS-guaranteed)

The preferred initial implementation prevents unintentional alteration of source files by opening them read-only in the common data utility. A separate child process does **not** inherently prevent it from modifying repository files, nor from reading later draws if buggy code deliberately opens the wrong source. The N−1/no-leakage tests, source digests, and separation of prediction from evaluation remain essential.

---

## 15. Reproducibility and validation tests for Architecture 2

These are **architecture-specific additions** supporting—not replacing—the ratified R2 acceptance tests.

| ID | Test | Success criterion |
|---|---|---|
| A-01 | Direct experiment under activated CMD | Runs without coordinator, correct venv and output |
| A-02 | Direct experiment in VS Code | Same venv and method behaviour as CMD |
| A-03 | Coordinator launches the same experiment | Same canonical prediction bytes, given identical input/configuration |
| A-04 | One versus six coordinator children (initial contract; see R2 reconciliation) | Predictions/complete rankings bit-identical for matching jobs; no result mixing |
| A-05 | Coordinator accidentally launched globally | Controlled error; no unapproved global dependency run |
| A-06 | Child with overridden `env` | Retains needed Windows environment; correct venv and native thread limits |
| A-07 | No valid method files | Clear empty/none-runnable accounting, not fake complete batch |
| A-08 | Valid named method file and invalid filename | Valid one discovered; invalid one not silently executed |
| A-09 | Duplicate E-number filenames | Explicit duplicate error or quarantine; no double science track |
| A-10 | Catalogue E-number without `.py` implementation | Explicit NOT_IMPLEMENTED/FORMULA_OPEN row retained |
| A-11 | Two children print very verbose output | No pipe deadlock; lines relayed and attributed correctly |
| A-12 | Child prints exception and exits nonzero | Status captured; no false successful result |
| A-13 | Child exits zero but creates no result file | Validation failure, not completion |
| A-14 | Partial JSON or mismatched method/target | Rejected; no valid frozen prediction |
| A-15 | Child takes longer than declared timeout | Explicit timeout status; termination/cleanup tested |
| A-16 | Run interrupted from CMD/VS Code | No fabricated success, cleanup or documented residue |
| A-17 | Two simultaneous jobs with same basename | Unique output paths; no collisions or overwrites |
| A-18 | Re-run a prospective target after publication | Cannot overwrite original frozen batch; new retrospective identity |
| A-19 | Perturb draw N and later | Direct and coordinated historical prediction N unchanged canonically |
| A-20 | Change readout/report formatting | Fitted stochastic model and frozen rankings unchanged |
| A-21 | TOP/WORST displays compared to JSON | Console is faithful rendering of authoritative result |
| A-22 | Rank-position evaluator receives real outcome | Forecast files remain unchanged |
| A-23 | Coordinator launched from different `cwd` | Default source and output paths remain correct |
| A-24 | One real and one synthetic job queued | Output namespaces and fitted states cannot cross |
| A-25 | Six-worker staged ~2 GB each memory stress | System remains responsive within declared resource policy; limited when necessary |
| A-26 | Dependent combination with unavailable source | Explicit dependency status, not a fabricated forecast |

Bit-identical testing refers to the **canonical prediction-content bytes**—not timestamps, execution log ordering, different run IDs or full-source provenance fields. Those operational fields may legitimately differ. Any exception to the R2 bit-identity acceptance standard still requires a documented justification and owner approval.

---

### 15.1 Added Windows subprocess / wrapper / dependency validation suite (research-derived)

Claude's independent research v3 identified W-01–W-19. This v0.2 proposal **adapts** those checks to the owner's six-worker direction; these are **not evidence of any completed tests**. `W-13` is deliberately made progressive to limit risk to the owner's 32-GB machine. All induced crash/kill tests must have cleanup/final verification.

| Test | Setup / procedure | Intended passing observation |
|---|---|---|
| W-01 | Send filename/options with `=`, comma, semicolon, quotes and spaces within promised invocation contract | Exact child `sys.argv`; no silent CMD rewriting |
| W-02 | Six children each emit many lines quickly | No pipe deadlock; complete, attributed logging and readable console |
| W-03 | Child exit 0, nonzero and Python exception | Wrapper/coordinator preserve correct codes and failure status |
| W-04 | Start with project venv inactive, active and other venv active; vary path case, slash/trailing separator and normal inherited activation | Compare normalized absolute `VIRTUAL_ENV` paths; preserve/restores caller environment; child verifies actual `sys.prefix`, no false rejection of own project `.venv` |
| W-05 | Record wrapper `Popen.pid` and real `os.getpid()` | Values tracked without assuming equality or any fixed redirector structure |
| W-06 | Child allocates controlled ~1 GB and then exits | Self-reported peak memory accurately reflects allocation with stated units |
| W-07 | CPU-bound fixture for fixed interval | In-process CPU timing sensible; coordinator wall time independent |
| W-08 | Hang fixture, short forced timeout | Wrapper-rooted tree removed; real PID confirmed gone; no success result |
| W-09 | Diagnostic `Popen.kill()` on wrapper only | Observe difference; after diagnostic **always clean surviving tree** |
| W-10 | Ctrl+C with six active workers | No stranded prompt/process; all marked interrupted, outputs safe |
| W-11 | Child deliberately `os._exit(7)` | Actual code/status preserved; incomplete STARTED status is not SUCCESS |
| W-12 | Coordinator global Python or malformed/missing venv | Explicit failure, no global installs/research run |
| W-13 | **Gradual** ramp to six children each allocating roughly 2 GB | Memory headroom and responsiveness checked continuously; stop safely below resource-risk threshold; no precondition to fill 12 GB if unsafe |
| W-14 | Option F wrapper via coordinator, safe arguments and a tricky quoted path | Exact permitted `sys.argv`, disallowed unsafe command arguments rejected |
| W-15 | Option F 0/3/exception/forced-exit | Exact Python exit codes returned by CMD wrapper and `Popen` |
| W-16 | Diagnostic kill of only wrapper `cmd.exe` | Observe survival without assuming specifics; **terminate and confirm any survivors** |
| W-17 | Option F `psutil` tree enumeration before kill | Wrapper, redirector if present and computing Python all gone or loudly flagged |
| W-18 | Option F Ctrl+C, six active batch wrappers | No interactive batch termination prompt left unanswered; all stop |
| W-19 | Shared wrapper contract, manual versus coordinated, CMD AutoRun and quoted `.bat` path | Same venv, numerical limits and canonical fixture output; HKCU/HKLM CMD AutoRun checked and potential interference rejected/reported; do not rely on untested `/D /C` nested quoting |
| W-20 | Environment-maintenance `.bat` executed deliberately | Package list visibly embedded; `pip check`; versions printed; caller environment restored |
| W-21 | Simulated dependency-install failure / constraint mismatch | Nonzero exit and clear diagnostics, never false success |
| W-22 | `.bat` checked out after Git conversion | CRLF retained; test commands run in ordinary CMD |
| W-23 | Recreate `.venv` or upgrade Python/psutil | Required W-suite re-run; research blocked until compatible |
| W-24 | Wrapper from folder containing spaces, another quoted argument and different caller CWD | No `/C` quote corruption; exact `sys.argv`, project-root-relative path semantics and exit codes; optional `/D /S /C` outer-quote candidate assessed only if explicitly designed |
| W-25 | Same fixture once and at six-way concurrency | Canonical payload bytes identical; resource/time metadata compared separately |

**Upgrade gate:** before accepting a changed Python/venv/psutil/numerics/wrapper combination for research use, execute the applicable W-suite (especially W-01–W-08, W-10/W-11, W-14–W-25). Benchmarks and immutable FINAL predictions must not be run in a known-incompatible environment. Informational diagnostics W-09/W-16 are not required for every routine maintenance invocation if a previously proven safe cleanup mechanism remains valid.

**Memory safety:** a theoretical six-times-two-gigabyte total is only an illustrative workload; run in stages with explicit free-memory stop thresholds and other-process load consideration. This engineering stress test does not use live Powerball data.

---

## 16. Proposed stepwise architecture proof-of-concept (before predictor implementation)

The objective is to test the architecture cheaply, **not** perform the real research or create an early unratified method result.

### P0 — No mathematical model yet

Prepare an illustrative tiny standalone `.py` program that reads a small **synthetic engineering fixture**, prints BEGIN/progress/FINISH, writes a structured non-forecast test artifact and returns an exit code. The coordinator discovers and launches it through `Run_Experiment.bat` (Option F) using `Popen`. Verify `.venv`/argument/pipe behaviour in both processes, including a nonactivated CMD and a differently activated environment. Mark it clearly as an **engineering fixture**, not E_1 or a Powerball forecast; do not place it in the permanent scientific E-method roster.

### P1 — Standalone/coordinated equivalence

Run the same engineering fixture directly and via coordinator using identical input and seed; compare canonical output bytes. Demonstrate a readable console and identical JSON, strict identity checking and default paths. Test both activated CMD and VS Code.

### P2 — Process supervision

Test 1, 2 and up to 6 concurrent small fixtures; deliberate failure, sleep/timeout, invalid result, verbose output and interruption. Rehearse gradual per-worker memory allocation before six simultaneous ~2-GB workloads; exercise the post-upgrade W-suite and release-no-orphans checks. Verify that a worker failure cannot corrupt successful outputs or suppress an unavailable method record.

### P3 — Minimal actual-method demonstration, only after design approval

Implement the simplest agreed E-method (likely E_1) using shared utilities; prove historical cutoff, FINAL L+1, complete lawful rankings, TOP/WORST and post-draw evaluation separation. Use the existing 444 valid historical draws but do **not** run the reserved final holdout as a development benchmark. This is a **later** step, after the architecture and corresponding method-specific choices are authorised.

### P4 — Move to formal implementation plan

Use the tested architecture to write a small versioned build/task plan. Only then add more E-methods progressively, and measure whether subprocess overhead is actually material (we expect it not to be).

**Important:** This document itself creates no source files beyond this Markdown proposal and does not authorise any prospective lottery prediction.

---

## 17. Open questions requiring discussion or research

Below is a consolidated decision register. All entries remain **OPEN** until explicitly agreed. Recommendations are proposed defaults, not statements of prior ratification.

| ID | Topic | Options / investigation | Recommendation |
|---|---|---|---|
| **O-ARCH-01** | Final architecture | Independent `.py` programs with subprocess coordinator (2), vs common runner/module architecture (3), vs monolith (1) | **2** with shared imports |
| **O-ARCH-02** | Separate common library | `_common` within methods, `src/common`, or installed package | `_common` within methods initially; verify direct imports |
| **O-ENV-01** | Wrong Python interpreter | Fail clearly vs auto-relaunch into `.venv` | Fail clearly; parent and child both verify |
| **O-ENV-02** | Coordinator launch entry point | Common `Run_Experiment.bat` vs direct `sys.executable` fallback | **Option F**, dependent on W-14..W-19 |
| **O-ENV-03** | Standalone numeric thread limit | Shared bootstrap env setup vs require activated shell settings | Shared early bootstrap, validated before numerical imports |
| **O-DISC-01** | Permanent E-method roster | Tiny catalogue vs docs-only list vs dynamic registration | Tiny explicit human-readable catalogue |
| **O-DISC-02** | What becomes runnable | Filename alone vs catalogue READY state and tests | Discover by filename, READY gate for FINAL |
| **O-DISC-03** | Discovery recursion | Flat directory vs recursive folders | Flat `src/methods` scan initially |
| **O-CLI-01** | Exact argument spelling | Common flags plus method-specific options | Common parser utility; settle prior to code |
| **O-CLI-02** | Modes and defaults | FINAL/historical/benchmark/synthetic command design | Derive L+1 automatically; demand historical N |
| **O-DATA-01** | Input delivery | Child loads cutoff-limited view vs coordinator writes restricted snapshot | Shared loader first; add restricted snapshot if worthwhile |
| **O-DATA-02** | Latest input snapshot choice | Explicit manifest vs timestamp discovery | Validated explicit/latest-by-policy snapshot, never timestamp alone |
| **O-OUT-01** | Process output | Merged stdout/stderr vs separate logs | Merged relay initially; structured result authoritative |
| **O-OUT-02** | Progress and logging | Event protocol vs human lines plus result file | Human lines, optional progress, no custom RPC yet |
| **O-SCHEMA-01** | Machine result format | JSON vs JSON Lines vs CSV | Atomic canonical JSON, printable console |
| **O-SCHEMA-02** | Path/run identity format | Mode/target/method/run/version hierarchy | Define in interface spec; never overwrite FINAL |
| **O-CPU-01** | Initial worker setting | Owner directs default/max 6; configurable 1–6 | **6 from the start**; staged six-worker verification |
| **O-CPU-02** | Internal threads | One per child vs method-specific exceptions | One initially, verified |
| **O-OPS-01** | Ctrl+C and timeout | Graceful then forced termination; child-tree handling | Test Windows semantics in prototype |
| **O-OPS-02** | Memory limit | Six ~2-GB workers, OS headroom; observe vs enforce per-process | Progressive admission and monitored headroom initially |
| **O-CHK-01** | Long-run restart/checkpoints | First release vs deferred | Defer until needed; never implicit reuse |
| **O-BENCH-01** | Timing detail | Whole-process vs separated startup/fit/predict | Start simple in POC; formal reports later |
| **O-DEP-01** | Methods depending on other forecasts | Explicit dependency ordering and versioning | Necessary before ensembles run |
| **O-POL-01** | Ratified R2 layout reconciliation | Adopt Architecture 2 as conforming `equivalent process pool` vs controlled R2 revision | Seek explicit architecture decision; amend R2 only if needed |
| **O-POL-02** | R3 interface reconciliation | Adopt R3 scoring schema when ratified | Await R3 review/ratification; do not hard-code provisional scores |
| **O-POL-03** | **Six-worker R2 operational reconciliation** | R2 permits 1–12; historical I-12/T-13/T-37/S3/D09 and timing examples mention twelve; D07 describes a process pool | **RESOLVED BY OWNER-APPROVED `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md`**: one versus configured maximum (currently six), equivalent subprocess implementation; **ERR-R2-02 / Option F production acceptance still awaits Windows tests and review** |
| **O-WRAP-01** | Batch wrapper checks | Project venv active, inactive, other venv; normalize `VIRTUAL_ENV` path; activation+restore; wrong `sys.prefix` | **Retain explicit checks, temporary `CALL` activation, `SETLOCAL` restoration**, reject *other* venv, verify effective Python environment |
| **O-WRAP-02** | CMD args and working directory | `%*` passthrough from `src\methods`, project-relative paths, nested quotes, HKCU/HKLM CMD AutoRun | **Ordinary tested batch Popen initially**; do not assume `/D /C` quoting or add Python forwarding helper without evidence |
| **O-WRAP-03** | Shared launch route | Option F wrapper vs direct-Python fallback | Option F provisional; W-14–W-19 gate |
| **O-PKG-01** | Installer/upgrade `.bat` behaviour | Embedded dependency list, install vs upgrade switches, pins/version checks, pip check | One self-contained authoritative `.bat`; define switches and candidate packages at implementation |
| **O-PKG-02** | Existing `requirements.txt` status | Retire or generate/read-only derivative, or retain historical | **No separately hand-maintained authority** |
| **O-PROC-01** | Tree monitor and cancellation | `psutil` tree/wait; `taskkill /T /F` fallback | `psutil` provisional; verify status PID + creation identity |
| **O-PROC-02** | Custom Windows Job Objects | Implement now vs defer pending nested child processes | **Defer** project-managed Job Objects |
| **O-UPG-01** | Future upgrades | After Python, `.venv` or package upgrade rerun compatibility suite | Required gate before accepting environment for research |

The owner's latest preferences already provide direction for **O-ARCH-01**, **O-CPU-01**, **O-WRAP-01**, **O-WRAP-03** and **O-PKG-01**; the narrow **O-POL-03** reconciliation is now owner-approved, while the **Option F Windows tests and review** remain essential before accepting that launcher for production. Remaining high-leverage open items include **O-DISC-01/02**, **O-SCHEMA-01**, **O-WRAP-02** and the exact first-release package manifest. Most remaining points can be resolved during a small prototype, with results brought back for ratification where they change the contract.

---

## 18. Potential risks, mitigations and tradeoffs

| Risk | Why it matters | Initial mitigation |
|---|---|---|
| Launcher uses global Python | Packages/config differ, misleading result | Wrapper checks/activates expected `.venv`; explicit Python path; child verifies `sys.prefix` |
| Child launch changes result | Coordinated versus standalone paths differ | Same script, same common utility, canonical prediction equality test |
| Many verbose children deadlock | OS pipes fill | Always drain streams concurrently; start with merged stream |
| Hidden NumPy/OpenBLAS threads | Six workers can still oversubscribe CPU | Wrapper-set pre-import numerical thread limit; inspect actual backend |
| Child exceeds memory | 32 GB system may become unstable | Configurable worker limit, memory telemetry, staged admission |
| Accidentally new `.py` file runs | Filename discovery executes local code | Narrow flat pattern, trusted source, identity checks, manual review |
| Implemented methods omit unimplemented ones | Full roster/evidence completeness lost | Minimal permanent E-method inventory separate from file discovery |
| Bypassed training-view utility | Look-ahead / leakage into historical runs | Mandatory N-and-later perturbation test for each method |
| Stale scratch file read | Hidden state improperly carried to next run | Per-run scratch paths; no automatic restart/import |
| Predictor output differs from console | Maintainer sees one thing, evaluator another | Single frozen result object, rendered twice; compare on test |
| Duplicate result filenames | Overwritten forecast/evidence | Unique path identity, preflight collision, immutable FINAL batches |
| Unverified exit-code success | Missing/corrupt result counted as valid | Independent JSON/schema/identity validation after exit |
| Method's downstream selection changes seed | Stochastic fit changes unexpectedly | Split fit model identity from TOP/WORST selection/report identity |
| Coupled methods consume future outputs | Ensemble leakage | Versioned origin-matched dependency graph; post-draw evaluator isolated |
| Architecture becomes a framework project | Time diverted from 62 scientific methods | Small POC, no generic plugin/RPC service, progressive additions |

---

## 19. Recommendations for the next discussion

The **current preferred Architecture 2 foundation**, subject to owner ratification and Windows testing, is:

1. **Programs:** independent executable `.py` files (one E-method each), with small reusable descriptive common modules and discoverable filenames; no mandatory central mathematical runner.
2. **Shared launch path (Option F):** a person uses `Run_Experiment.bat`; the coordinator provisionally uses that **same** wrapper through `subprocess.Popen`. `Run_Coordinator.bat` starts the coordinator for a human. Direct `.py` execution with correct venv remains supported for development/debugging; direct subprocess launch remains a contingency if Option F fails.
3. **Deliberate wrappers:** explicit `.venv` checks, conditional scoped activation, caller-environment restoration, explicit project Python, forwarded `%*`, tested CMD quoting, CRLF `.bat` tracking and common pre-import thread settings.
4. **Single dependency-maintenance authority:** `install_upgrade_dependencies_into_venv.bat` with the complete *human-edited* package list and pip install/upgrade commands inside the batch file. No second independently maintained `requirements.txt` source. Install/upgrade operations are user-invoked, not automatic.
5. **Concurrency:** initial **six** active E-method processes maximum, configurable 1–6, with staged six-times-~2-GB RAM proof. This is the **owner-approved operational interpretation** under `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md`. The original R2 v0.3 text has not been rewritten; the Option F launcher remains conditional on successful Windows tests and review.
6. **Monitoring and cancellation:** process self-reporting plus coordinator elapsed/system-RAM observation; `psutil` tree cleanup/verification (with taskkill fallback) on timeout/Ctrl+C; no project-managed Job Objects in first implementation; no method-spawned child pools initially.
7. **Output and scientific safeguards:** authoritative canonical JSON per method and human-readable TOP/WORST console, live relayed logging, frozen FINAL batch, N−1/FINAL L+1 boundary, synthetic separation and evaluator independence; retain all E-method identities.
8. **Proof of concept before real method implementation:** exercise Option F W-14–W-19, P0/P2 cancellation, venv checking and protected wrapper exit codes, one-vs-six content equality and staged memory use on Windows 11. Re-run compatibility gate after upgrades.
9. **Separate R3 statistical matter:** adopt no label-neutral tie-break rule in this architecture draft; incorporate Claude's proposed deterministic label-neutral resolution in a reviewed **R3 v0.2** prior to coding/rating outcomes.

The owner may ratify the architecture design separately from accepting Option F as production-ready; **ERR-R2-02 remains conditional on Windows verification and review**. The narrow R2 operational adjustment is already approved in `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md`. **Do not silently rewrite ratified Proposal v0.3, R1 v0.4 or R2 v0.3; R3 v0.2 remains a separate unratified review candidate.**

---

## 20. Supporting technical references and verification state

### 20.1 Official Python documentation consulted

- Python 3.14, [Virtual Environments (`venv`)](https://docs.python.org/3.14/library/venv.html): environment activation versus explicitly executing `.venv` Python; venv detection by `sys.prefix != sys.base_prefix`; `.venv` non-portability.
- Python 3.14, [Subprocess management](https://docs.python.org/3.14/library/subprocess.html): `Popen`, `args` list, `sys.executable`, `cwd`, `env`, `shell=False`, standard streams and pipe deadlock caution.
- Python 3.14, [Python CLI options](https://docs.python.org/3.14/using/cmdline.html): `-u` unbuffered standard streams and `-m` module invocation.
- Python 3.14, [`sys` module](https://docs.python.org/3.14/library/sys.html): `sys.executable`, `sys.prefix` and `sys.base_prefix`.
- Python, [`os` module](https://docs.python.org/3.14/library/os.html): environment-variable inheritance and `os.environ`.

These establish the broad interpreter/environment mechanics. They do **not** prove that the proposed repository scripts work: none of those scripts or the proposed architecture has been implemented or run for this document.

### 20.1A Additional Windows/process/dependency references considered for v0.2

- Microsoft [`cmd` switches](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd) — `/D` disables AutoRun; `cmd.exe` invocation and quoting need real Windows validation.
- Microsoft [`setlocal`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setlocal) — scoped environment-variable changes for human-facing wrappers.
- Microsoft [`taskkill`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/taskkill) — `/T /F` is a documented process-tree termination fallback.
- Microsoft [`Terminating a Process`](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process) — child-process lifetimes are not implicitly bound to a terminated parent.
- Python [CPython venv launcher source](https://github.com/python/cpython/blob/main/PC/venvlauncher.c) and [Python issue 38905](https://bugs.python.org/issue38905) — evidence about historical/current Windows venv redirector implementation, **not** a version-independent API promise.
- [`psutil` documentation](https://psutil.io/) — process-tree enumeration, memory sampling and resource reporting; exact installed version is recorded during runs.
- **Claude research v3, 22 Oct 2026**, supplied by owner: source-level findings, Option F assessment and original W-01–W-19 test matrix; this draft adapts them, without claiming they were executed on Windows.



### 20.2 Project documents consulted

- Ratified Proposal v0.3 for philosophy, allowed historical era, method retention, synthetic separation and real-world evidence.
- Ratified R1 v0.4 for 62 method identities and mathematical research context.
- Ratified R2 v0.3 for N−1, FINAL, holdout, ranks, TOP/WORST, subprocess-compatible process execution, seeds, validation, benchmarking and safe persistence.
- R3 v0.2 (**candidate**) for scoring/evaluator separation, source identities, deterministic label-neutral tie ordering, and prospective comparison/ensemble interface considerations.

### 20.3 What is established versus proposed

**Established/documented by Python:** a child can use the same project-local venv by invoking its interpreter; subprocess environmental variables and stdout/stderr redirection are controllable; activation scripts are not inherently required for a Python child.

**Established project decisions, with recorded precedence:** Windows/VS Code/CMD, method retention, TOP/WORST, holdout and method catalogue; ratified R2 v0.3 still documents 1–12 concurrency and 1-versus-12 identity, while the owner's *subsequent* design direction is an initial **six-worker default/maximum**. The approved R2 erratum v0.2 reconciles the operational test/worker wording without rewriting R2 v0.3; Option F remains provisionally approved pending Windows tests and review. User preference for authoritative dependency `.bat` and explicit wrapper venv handling is unambiguous.

**Still proposed / needs prototype:** Option F Windows behaviour; exact batch quoting/activation/return-code flow; file naming, method inventory, supervisor and process tree; per-experiment peak memory collection; actual six-worker memory headroom; dependency package/version selection; schema and output paths; Python upgrade compatibility.

**Not claimed:** that this architecture already works on the user's PC; that every E-method is implemented; that any method has predictive power; that the dataset was just updated; that the R3 review candidate is ratified.

---

**End of Software Architecture Discussion v0.3 — DISCUSSION DRAFT, NOT RATIFIED**
