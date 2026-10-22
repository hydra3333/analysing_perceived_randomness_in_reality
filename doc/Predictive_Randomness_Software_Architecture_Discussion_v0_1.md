# Predictive Randomness — Software Architecture Discussion and Open Questions

**Draft version:** v0.1  
**Date:** 22 October 2026  
**Status:** DISCUSSION DRAFT — not ratified; no implementation authorised by this document  
**Suggested repository path:** `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_1.md`  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Working environment:** Windows 11, standard CPython 3.14, VS Code, project-local `.venv`, AMD Ryzen 9 3900X (12 physical cores/24 logical threads), 32 GB RAM

> **Executive proposal:** Prefer **Architecture 2**: each `E_x` experiment is an independently executable Python `.py` program; a lightweight coordinator discovers and launches selected programs with `subprocess`; all programs may import shared, descriptive common Python modules; the coordinator performs scheduling, supervision, and consolidated output. An experiment can run **unchanged** directly from a Windows Command Prompt/VS Code or as a coordinator child. This is an architectural *proposal*, not a modification of the ratified research contracts.

> **Important distinction:** Independent executable programs do **not** require each program to duplicate input validation, argument parsing, probability selection, output formatting, or numerical utilities. Imported common modules are reusable source code, **not a shared Python process, shared mutable memory, or a compulsory central experiment runner**.

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
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_1.md` | **REVIEW CANDIDATE** | Candidate evaluation/reporting rules; **not** treated as already ratified |
| **This architecture discussion v0.1** | **DISCUSSION DRAFT** | Proposes how to implement the above, and identifies conflicts requiring a controlled decision |

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
11. **Reproducibility.** Equivalent standalone/coordinated execution and 1-versus-12-worker execution aim for bit-identical canonical predictions on the same controlled system. Deviations need specific technical explanation and owner approval under R2.
12. **Computational execution.** Begin with a configurable pool of 1–12 independent processes (optional 24-process SMT benchmark); limit numerical-library internal threads and preserve resources on a 32 GB machine.
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

One Python program per scientific experiment, with its own callable `main()` and normal command-line options. Each can import descriptive common utility modules. The optional coordinator finds or selects matching program files, launches them as children of the project Python interpreter, relays their console output, supervises failures/timeouts and reads their completed result artifacts.

**Advantages:** straightforward standalone invocation; clean process/memory isolation; explicit subprocess environment and numerical thread limits; easier method-specific debugging; no compulsory central runner; a crash need not take other methods down; dependencies and program output can be inspected independently; natural fit to 12-core execution; minor startup overhead is irrelevant for our computations.

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
    activate_venv.bat                       # if retained locally/committed
    deactivate_venv.bat                     # if retained locally/committed
    doc/
        Predictive_Randomness_Research_Project_Proposal_v0_3.md
        Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md
        Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md
        Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_1.md
        Predictive_Randomness_Software_Architecture_Discussion_v0_1.md
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
    requirements.txt
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

An experiment program must not require `Powerball_Experiment_Coordinator.py` to be running, or a service/daemon/remote API to be available. The coordinator is a convenience for multiple methods, not a scientific dependency of a method.

### 4.2 The coordinator's job

The coordinator should do only the tasks that benefit from centralisation:

- Discover candidate `.py` files by a fixed filename convention or select requested E-identifiers.
- Validate unique filenames/identities and manage declared unavailable or not-yet-implemented catalogue entries.
- Parse shared invocation settings and determine the requested target/mode/snapshot policy.
- Select the **same project-local Python interpreter** for children.
- Launch at most the configured number of active child processes and manage a queue.
- Set child environment variables for numerical thread control and standard output behaviour.
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

### 5.2 Proposed child-interpreter rule

**Proposed D-A03:** The coordinator should *explicitly validate* that its own interpreter is the repository's intended `.venv\Scripts\python.exe` (with normal Windows case/path handling). The simplest initial coordinator then launches each child with **its own `sys.executable`**, rather than the bare string `python`, `py`, a `.bat` activation command, or a file association.

Conceptual launch only, not the full production implementation:

```python
import os
import subprocess
import sys

child_environment = os.environ.copy()
child_environment.update({
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "PYTHONUNBUFFERED": "1",
    "PYTHONIOENCODING": "utf-8",
})

child = subprocess.Popen(
    [sys.executable, "-u", str(method_script), "--mode", "final"],
    cwd=str(repository_root),
    env=child_environment,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    shell=False,
)
```

The snippet is **illustrative**. A real supervisor must concurrently drain output, check exit status, enforce cancellation/timeout, verify result files and report failures. On Windows, using an absolute executable path and argument **list** with `shell=False` avoids avoidable CMD quoting and PATH resolution problems.

**Alternative requiring an owner decision:** Rather than fail if the coordinator started under global Python, it could explicitly relaunch itself under the project interpreter. I favour a clear error initially; automatic relaunch adds path and process-lifecycle complexity that we do not yet need.

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

The coordinator accepts additional selection options such as `--methods E_1,E_2,...`, `--all-ready`, `--workers 12`, `--timeout-seconds ...`. A method should accept the common arguments where applicable and can declare its own mathematical options; undocumented options must not become hidden defaults.

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

For immediate line visibility, run child Python with `-u` / `PYTHONUNBUFFERED=1` or flush progress explicitly. On Windows, when capturing through a pipe with `encoding="utf-8"`, explicitly request `PYTHONIOENCODING=utf-8` in the child to prevent a mismatch with legacy redirected-output encodings. The coordinator should avoid treating every unstructured line as a protocol event. A child can print traceback or diagnostic text without causing loss of result identity.

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

### 10.1 First release: simplest viable scheduler

- A configurable pool of **1–12 active Python child processes**, each normally executing one E-method program.
- The coordinator fills available slots from its queue; finished children free slots.
- Each method program owns sequential historical targets when warm starts depend on previous fits.
- A long method does not block unrelated methods except through process slots or memory reservations.
- Optional **24-process** throughput test is separately labelled as an SMT experiment; no automatic assumption that it is faster.
- **Avoid nested parallelism initially.** Do not allow 12 active workers each to spawn another unmanaged 12-child pool.
- Set numerical-library threading controls to one *before* importing the relevant libraries in each child. Capture actual settings/backends in benchmark output.

### 10.2 Internal numerical libraries and environment

Environment candidates include `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS` and, where warranted, `threadpoolctl`. **Which are relevant depends on installed packages and NumPy's BLAS backend;** do not assume every variable controls every library. A method may later need explicitly approved exceptions for internal threads or GPU/accelerator use.

The coordinator can set limits independently for its child by supplying `env=os.environ.copy()` with named overrides. A standalone experiment should use equivalent defaults through its own startup bootstrap where possible **before importing heavy numerical libraries**. The two launch routes must produce equivalent effective numerical settings for the bit-identical test.

### 10.3 RAM and oversubscription

The 32 GB system does not imply that exactly 12 expensive methods may always coexist. A few methods may require several gigabytes each, especially optimisers or particle filters. Make the active limit configurable, measure child resident memory where possible, and allow conservative memory-aware admission/scheduling. A hard, enforceable per-process memory limit on Windows is a separate implementation question; observing working-set memory is not equivalent to enforcing a ceiling.

**Open question O-CPU-01:** Should default worker count be 12 or a lower number such as 8 to preserve desktop responsiveness? **Recommendation:** retain ratified configurable 1–12; test 1 and 12 first; choose operational default only from measured resource behaviour and owner's preference. It is acceptable to run fewer than 12 processes when required for memory safety.

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

Default repeat count could be three for cheap tests, with a recorded smaller count for expensive methods. Compare one coordinator worker with twelve, and optionally 24 in a separately documented trial. **Same input + same method configuration** should give the same canonical predictions irrespective of the number of coordinator workers.

Use Windows/NumPy diagnostics to verify the actual BLAS library and internal thread count. Recording an environment variable without checking whether the library respects it is not sufficient proof of thread pinning. `psutil` is a candidate future venv dependency for process CPU/memory observation and must be approved before installation; Python's `tracemalloc` alone cannot see all native NumPy allocations.

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

### 14.2 Cancellation and child trees on Windows

`Popen.terminate()` on Windows calls Windows process termination for the process; it does not generally guarantee cleanup of grandchildren or all files. The first architecture proof-of-concept should keep experiment programs from spawning children themselves. If method-internal subprocesses become necessary, define a Windows process-tree cleanup strategy (possibly job objects) before claiming reliable timeouts or Ctrl+C cancellation for nested process trees.

**Open question O-OPS-01:** Should Ctrl+C request graceful cleanup first and force termination after a bounded delay? **Recommendation:** yes, with console feedback, explicit stopped status and no successful result artifact from an interrupted process. Windows console control behaviour should be tested rather than assumed.

### 14.3 Trusted source-code boundary

Scanning a folder and executing Python programs is the execution of code with the user's Windows account permissions. **It is not a secure plugin sandbox.** The project should run only trusted tracked E-method scripts, reject paths escaping the authorised `src/methods/` directory, and use no `shell=True` or concatenated command strings. Good manual repository practice remains essential.

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
| A-04 | One versus twelve coordinator children | Predictions/complete rankings bit-identical for matching jobs; no result mixing |
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
| A-25 | 12-worker memory stress | System remains responsive within declared resource policy; limited when necessary |
| A-26 | Dependent combination with unavailable source | Explicit dependency status, not a fabricated forecast |

Bit-identical testing refers to the **canonical prediction-content bytes**—not timestamps, execution log ordering, different run IDs or full-source provenance fields. Those operational fields may legitimately differ. Any exception to the R2 bit-identity acceptance standard still requires a documented justification and owner approval.

---

## 16. Proposed stepwise architecture proof-of-concept (before predictor implementation)

The objective is to test the architecture cheaply, **not** perform the real research or create an early unratified method result.

### P0 — No mathematical model yet

Prepare an illustrative tiny standalone `.py` program that reads a small **synthetic engineering fixture**, prints BEGIN/progress/FINISH, writes a structured non-forecast test artifact and returns an exit code. The coordinator discovers and launches it. Verify the `.venv` in both processes. Mark it clearly as an **engineering fixture**, not E_1 or a Powerball forecast; do not place it in the permanent scientific E-method roster.

### P1 — Standalone/coordinated equivalence

Run the same engineering fixture directly and via coordinator using identical input and seed; compare canonical output bytes. Demonstrate a readable console and identical JSON, strict identity checking and default paths. Test both activated CMD and VS Code.

### P2 — Process supervision

Test 1, 2 and up to 12 concurrent small fixtures; deliberate failure, sleep/timeout, invalid result, verbose output and interruption. Verify that a worker failure cannot corrupt successful outputs or suppress an unavailable method record.

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
| **O-ENV-02** | Which interpreter to launch | Parent `sys.executable` vs hard-coded project `.venv` | Validated `sys.executable` |
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
| **O-CPU-01** | Default workers | Up to 12, lower operational default, optional 24 test | Configurable; benchmark before choosing default |
| **O-CPU-02** | Internal threads | One per child vs method-specific exceptions | One initially, verified |
| **O-OPS-01** | Ctrl+C and timeout | Graceful then forced termination; child-tree handling | Test Windows semantics in prototype |
| **O-OPS-02** | Memory limit | Observe vs enforce per-process | Observe initially; enforce only if needed |
| **O-CHK-01** | Long-run restart/checkpoints | First release vs deferred | Defer until needed; never implicit reuse |
| **O-BENCH-01** | Timing detail | Whole-process vs separated startup/fit/predict | Start simple in POC; formal reports later |
| **O-DEP-01** | Methods depending on other forecasts | Explicit dependency ordering and versioning | Necessary before ensembles run |
| **O-POL-01** | Ratified R2 layout reconciliation | Adopt Architecture 2 as conforming `equivalent process pool` vs controlled R2 revision | Seek explicit architecture decision; amend R2 only if needed |
| **O-POL-02** | R3 interface reconciliation | Adopt R3 scoring schema when ratified | Await R3 review/ratification; do not hard-code provisional scores |

The owner can resolve the highest-leverage items first: **O-ARCH-01**, **O-ENV-01/02**, **O-DISC-01/02**, **O-OUT-01**, **O-SCHEMA-01** and **O-POL-01**. Most remaining points can be resolved during a small prototype, with results brought back for ratification where they change the contract.

---

## 18. Potential risks, mitigations and tradeoffs

| Risk | Why it matters | Initial mitigation |
|---|---|---|
| Launcher uses global Python | Packages/config differ, misleading result | Validate `.venv` at startup; pass `sys.executable`; test wrong-interpreter case |
| Child launch changes result | Coordinated versus standalone paths differ | Same script, same common utility, canonical prediction equality test |
| Many verbose children deadlock | OS pipes fill | Always drain streams concurrently; start with merged stream |
| Hidden NumPy/OpenBLAS threads | 12 workers oversubscribe CPU | Pre-import numerical thread limit; inspect actual backend |
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

I recommend that the owner and assistant discuss and **provisionally ratify only the architectural foundation** first:

1. **Architecture 2**: fully executable per-method `.py` programs plus lightweight subprocess coordinator; allow shared imported utility modules without forcing a common runner.
2. **venv rule**: coordinator and experiment processes must execute the project's intended venv Python, with a fail-fast check; child processes use validated `sys.executable`, not shell activation.
3. **discoverability and roster**: filename scan for runnable scripts, backed by a minimal explicit list of all permanent E-methods/statuses. No complex plugin service.
4. **dual output**: human-readable standalone/relayed console presentation, especially TOP and WORST side by side, plus one canonical validated machine-readable JSON forecast file. No predictive parsing from console text.
5. **scheduler**: up to 12 independent Python child processes, BLAS threads limited to one initially, with queueing and explicit failure accounting.
6. **preserve safeguards**: N−1, FINAL L+1 all-data use, holdout, canonical seed identity, separate post-draw evaluation, synthetic segregation, immutable pre-draw batches and non-exclusion of slow/poor/correlated methods.
7. **build only a small engineering proof-of-concept next**: verify venv, direct versus coordinated identity, pipes, failure, timeouts and concurrency; do not undertake scientific modelling solely to validate the architecture.

Once those choices are agreed, produce a short **architecture decision record / implementation interface** with precisely versioned CLI and result schema; incorporate its conclusions into R3 or a controlled software-design supplement. **Do not silently rewrite ratified Proposal v0.3, R1 v0.4 or R2 v0.3.** R3 v0.1 remains a review candidate until the owner ratifies it.

---

## 20. Supporting technical references and verification state

### 20.1 Official Python documentation consulted

- Python 3.14, [Virtual Environments (`venv`)](https://docs.python.org/3.14/library/venv.html): environment activation versus explicitly executing `.venv` Python; venv detection by `sys.prefix != sys.base_prefix`; `.venv` non-portability.
- Python 3.14, [Subprocess management](https://docs.python.org/3.14/library/subprocess.html): `Popen`, `args` list, `sys.executable`, `cwd`, `env`, `shell=False`, standard streams and pipe deadlock caution.
- Python 3.14, [Python CLI options](https://docs.python.org/3.14/using/cmdline.html): `-u` unbuffered standard streams and `-m` module invocation.
- Python 3.14, [`sys` module](https://docs.python.org/3.14/library/sys.html): `sys.executable`, `sys.prefix` and `sys.base_prefix`.
- Python, [`os` module](https://docs.python.org/3.14/library/os.html): environment-variable inheritance and `os.environ`.

These establish the broad interpreter/environment mechanics. They do **not** prove that the proposed repository scripts work: none of those scripts or the proposed architecture has been implemented or run for this document.

### 20.2 Project documents consulted

- Ratified Proposal v0.3 for philosophy, allowed historical era, method retention, synthetic separation and real-world evidence.
- Ratified R1 v0.4 for 62 method identities and mathematical research context.
- Ratified R2 v0.3 for N−1, FINAL, holdout, ranks, TOP/WORST, subprocess-compatible process execution, seeds, validation, benchmarking and safe persistence.
- R3 v0.1 (**candidate**) for scoring/evaluator separation, source identities and prospective comparison/ensemble interface considerations.

### 20.3 What is established versus proposed

**Established/documented by Python:** a child can use the same project-local venv by invoking its interpreter; subprocess environmental variables and stdout/stderr redirection are controllable; activation scripts are not inherently required for a Python child.

**Established by project decisions:** Windows/VS Code/CMD setup, research philosophy, method retention, 62 E-identities, historical/FINAL distinction, TOP/WORST, holdout, 1–12 independent worker processes and bit-identical expectations.

**Still proposed / needs prototype:** file naming, scripts under `src/methods/`, coordinator subprocess supervisor implementation, manifest form, console formatting, schema and output-file path policies, exact numerical worker control and timeout cleanup.

**Not claimed:** that this architecture already works on the user's PC; that every E-method is implemented; that any method has predictive power; that the dataset was just updated; that the R3 review candidate is ratified.

---

**End of Software Architecture Discussion v0.1**
