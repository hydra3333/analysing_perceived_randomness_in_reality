# Deferred Performance Engineering: Profiling, Numerical Libraries, and Selective Native Acceleration

**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Document version:** v0.1 — discussion proposal / future-stage placeholder  
**Prepared:** 2026-10-31 (Australia/Adelaide)  
**Proposed stage:** After the project's scientific and operational implementation is complete  
**Status:** Owner-requested record of discussion; **not** an authorization to implement, change experiments, change safety controls, or access hold-outs  
**Intended use:** Commit to the repository, link from the project plan/register, and schedule a future review and implementation decision

> **Scope and authority.** This records the agreed *direction* and the alternatives and preferences discussed, rather than silently promoting them to ratified technical requirements. Existing ratified project governance, experiment contracts, source-of-truth documentation, process-safety rules, method-revision rules, and hold-out protections take precedence. The owner will decide when to activate the stage and what, if anything, to implement.

## 1. Executive proposal

After the randomness project is fully implemented, perform a **profiling-first, evidence-driven performance-engineering study**. Establish where real elapsed time, active CPU time, memory, waiting, and concurrency overhead are incurred across the complete experiment pipeline, including Python methods and imported compiled numerical libraries such as NumPy and SciPy. Only *then* decide whether optimization is worthwhile and which techniques suit each measured bottleneck.

The leading possibilities for selectively accelerating custom numerical code are **Numba** (first to investigate where its supported subset applies) and **Cython** (strong alternative, particularly with explicit native types and typed array access). Improvements to existing NumPy/SciPy usage, batching, data representation, memory allocation, and native-library threading are at least as important to test. Compiling the entire project or producing a single Windows `.exe` is a **separate, lower-priority deployment question**, not the performance strategy.

The intended outcome is not necessarily one compiler for all methods. Different experimental methods may benefit from different approaches; some may already spend nearly all their execution time in efficient compiled libraries and should remain ordinary Python.

**Primary goal:** maximize *scientifically reproducible, safe, end-to-end experiment throughput* and/or reduce elapsed time for genuinely expensive workloads, without changing the scientific question, ranking/forecast semantics, safety behavior, or evidence integrity.

## 2. What has been agreed, what is merely preferred, and what remains undecided

The labels below distinguish discussion-level alignment from formal repository ratification.

| Topic | Discussion status | Meaning |
| --- | --- | --- |
| Defer performance engineering until after full project implementation | **Owner-agreed direction** | Add a future stage now; no premature optimization project. |
| Profile first, including NumPy/SciPy and multi-process execution | **Owner-agreed direction** | Measured bottlenecks, not guesses, drive follow-on work. |
| Measure elapsed/wall and CPU times separately | **Agreed analytical principle** | Aggregate CPU-seconds of parallel workers must not be mistaken for elapsed seconds. |
| Preserve existing Python experiment architecture initially | **Strong preference** | Leave coordination, dynamic method imports, and existing scientific dependencies intact unless evidence justifies changes. |
| Test ordinary Python/NumPy/SciPy improvements and native-thread settings | **Proposed candidate** | Could produce gains without compilation. |
| Numba as an early candidate for custom numerical loops | **Provisional first investigation preference** | Not chosen as project-wide implementation technology. |
| Cython as another leading candidate | **Provisional strong preference** | May be better for kernels requiring explicit typing or where Numba is unsuitable. |
| Mixed implementation technologies across methods | **Acceptable in principle** | Selection by measured method/kernel, not by a universal rule. |
| Full-project compilation / single-file Windows EXE | **Separate, lower-priority possibility** | Packaging is not evidence of speed; dependencies complicate deployment. |
| Numerical equivalence, provenance, and governance | **Non-negotiable project constraint** | Optimizations must pass the applicable existing scientific and safety review gates. |
| Which benchmarks, profilers, compiler versions, speed thresholds, deployment format, and exact stage ID | **Deferred decisions** | Decide on activation after current project implementation is complete. |

No speedup percentage is promised. Illustrative Cython/Numba speedups reported for some tight loops are *not* a forecast for this repository.

## 3. Why this investigation is worthwhile

### 3.1 Normal Python execution

Standard CPython compiles `.py` source to Python bytecode and executes that bytecode. Cached `.pyc` files can reduce repeat import/parse overhead but generally **do not accelerate the steady-state computations**. This is distinct from C/C++ native compilation.

### 3.2 Where speed may actually be lost

Likely categories to *measure*, not assume, include:

1. Pure-Python numerical loops, repeated scalar operations, branches, array-element indexing, object allocation, and Python call overhead.
2. NumPy operations involving small arrays or many repeated calls where dispatch, allocation, or data copying dominates useful calculation.
3. Large NumPy/SciPy operations already running mostly in optimized native code (potentially little to gain from compiling their Python callers).
4. Expensive optimization, linear algebra, transforms, probability calculations, or other numerical kernels; any bottleneck *inside* native libraries may require deeper profiling.
5. Python-to-native call boundaries and callbacks from native solvers back into Python functions.
6. Experiment orchestration: method initialization, import time, loading/parsing datasets, serialization, process startup, IPC, writing results, and logging.
7. Disk or network waits (if present in a particular workflow), locks, idle workers, process scheduling, memory pressure, paging, and contention.
8. Oversubscription caused by multiple experiment processes, each using their own BLAS/OpenMP/native thread pools.
9. Cold-start effects, compilation/JIT warm-up, repeated dynamic imports, and short-lived experiment tasks.

The purpose of profiling is to rank these by their **measured contribution to end-to-end time** and their realistic potential for improvement.

## 4. The first stage must be a trustworthy, unoptimized baseline

Before changing source code or execution policy, establish **unprofiled** baselines on a documented machine and environment. Keep normal execution and measurement separate from instrumented runs because even profiling can distort performance.

Record for each representative workload:

- Game identifier, experiment/method identifier, method revision, workload type, source-data identity/hash, experiment parameters, and deterministic seeds where applicable; preserve the established compound `(game ID, draw number)` identity.
- The exact interpreter **used by the project's virtual environment**, not just the user's separately installed Python version; Python implementation/build, architecture, package versions, numerical-library builds, CPU architecture, physical/logical cores, memory, OS, and relevant thread settings.
- Git/source or immutable artifact provenance under the *currently ratified* project conventions; do not reintroduce commit-ID requirements into method-retirement records where the project explicitly uses revision-labelled, commit-independent provenance.
- Elapsed time for the full requested job or batch, time per method/worker and per relevant phase, total CPU-seconds (with correct process/thread aggregation), peak resident/private memory, I/O and paging indicators where useful.
- Startup/import/preparation costs separately from actual numerical kernel execution, result processing and final artifact publication.
- Actual worker concurrency, each worker's process CPU usage, active native-library thread counts, and CPU/memory contention.
- Exact success/failure and canonical output identities, sufficient to confirm that the benchmark ran the intended workload and reached the expected completion state.

**Measurement principles:** run repeat trials; use a planned representative workload matrix; distinguish cold and warm runs; avoid comparing runs with different data, method revisions or environment conditions; use medians and variability rather than one flattering timing. Measure both *single-worker efficiency* and *normal project throughput*. Keep an untouched, original baseline for comparison.

Initial expected environment characteristics from project discussions include a Windows x64 system with approximately 32 GiB RAM and a default of six concurrent experiment workers, with a prior planning estimate of about 2 GiB per worker. These are **historical planning context, not a verified current benchmark specification**; re-check at activation.

## 5. Profiling strategy — Python first, native analysis as needed

### 5.1 Python 3.15 profiling facilities

As of **Python 3.15.2 (released 2026-10-25)**, Python includes two directly relevant profiling facilities:

- **`profiling.sampling` / Tachyon:** low-overhead statistical stack sampling, suitable for discovering real hotspots. Offers wall-clock, CPU, and GIL modes; flame graphs and heatmaps; subprocess tracking; all-Python-thread sampling; and synthetic `<native>` frames. Sampling percentages and durations are *estimates*, not exact function timings.
- **`profiling.tracing` / `cProfile`:** deterministic call and return profiling, useful for precise Python call counts and caller/callee relationships. Tracing generally imposes more overhead. In Python 3.15, `cProfile` remains the compatible spelling of `profiling.tracing`.

Potential commands for **a separately approved, disposable profiling harness**, with the actual entrypoint and argument handling to be determined at implementation time:

```bat
REM Sampling: Python and native boundaries, process descendants, threads, elapsed-time view.
python -m profiling.sampling run --subprocesses --all-threads --native --mode=wall --flamegraph profiling_harness.py

REM Sampling: active CPU-time view; compare with wall view.
python -m profiling.sampling run --subprocesses --all-threads --native --mode=cpu --flamegraph profiling_harness.py

REM Deterministic Python call profiling on a chosen isolated workload.
python -m profiling.tracing -s cumulative profiling_harness.py
REM Equivalent compatibility form:
python -m cProfile -s cumulative profiling_harness.py
```

**These are examples, not approved repository commands.** In particular, `profiling_harness.py` does not presently denote an existing project file. Do not invoke these examples through the production coordinator without separate safety review.

Tachyon's `--subprocesses` can report separate profiles for descendants *discovered after the target starts*; verify that this covers the project's Windows BAT-wrapper/coordinator/worker ancestry, short-lived workers, and any separately launched jobs. The option does **not** promise to capture all existing unrelated processes or non-Python child programs.

**Windows privilege caution:** Profiling another process by memory-reading/attaching can require administrator privileges or `SeDebugPrivilege`; the profiler and target also need matching Python minor versions. Prefer an approved launch-and-profile harness over attaching to live coordinator-owned worker processes. Do not elevate permissions, attach to unknown processes, or change coordinator controls merely to obtain profiles. The stage must independently verify the exact requirements on the target machine.

### 5.2 What Python profilers can and cannot see in NumPy/SciPy

A Python profiler can attribute time to a Python call into NumPy/SciPy, and Tachyon's `--native` option marks time that has transitioned into native code. This answers questions such as *which Python call chain enters an expensive numerical operation* and *whether the time is spent in Python or native code*.

**Important limitation:** Python call-stack profiling does **not** necessarily resolve the individual C/C++/Fortran/BLAS/LAPACK functions, hardware instructions, or internal native worker threads responsible for that time. `--all-threads` is not a guarantee of visibility into every thread created entirely within a native library. A call that appears as one costly native segment might contain many different internal operations.

If native-library cost dominates, investigate a **second level of native-capable profiling** using an appropriate tool on the actual Windows hardware (e.g., Windows Performance Recorder/Analyzer or a compatible CPU performance profiler). Tool selection, symbols, privilege requirements, overhead, and thread visibility are **to be verified at that future stage**, not assumed. Library-specific timings/microbenchmarks can supplement these profiles.

### 5.3 Interpretation: wall time is not summed CPU time

Six simultaneous workers each consuming roughly 60 CPU-seconds may represent roughly 360 aggregate CPU-seconds but only around 60 seconds elapsed if executed concurrently without bottlenecks. Conversely, a method with low CPU usage but high wall time may be waiting on I/O, locks, other workers, memory, or native thread-pool contention.

Assess:

- End-to-end *wall-clock completion time* and throughput (primary operational objectives).
- Active CPU-seconds and CPU utilization (how much computation occurs and where).
- Per-worker waiting, start/finish skew, queueing, work imbalance, process startup and serialization.
- Per-process/per-thread memory use and total working-set pressure.
- Whether one optimized kernel improves the **normal concurrent workload**, rather than only a single isolated microbenchmark.

### 5.4 Experimental discipline for profiling

Use short, representative and longer steady-state cases; repeated controlled runs; consistent environments; an explicit distinction between profiled and unprofiled results; sufficient sampling for meaningful estimates; and deterministic correctness fixtures where applicable. Keep profiler output separate from canonical scientific result artifacts. Treat evidence from incomplete/failed/orphan-suspected runs according to the existing result-consumption firewall; do not borrow such results merely because profiling output exists.

## 6. Native-library concurrency deserves early examination

An ordinary NumPy/SciPy call may invoke a compiled BLAS/LAPACK library or OpenMP-backed implementation with its **own threads**. With multiple independent Python experiment workers, native thread pools can compete for cores, memory bandwidth and cache, resulting in poor total throughput despite high CPU utilization.

Investigate:

- Which BLAS/LAPACK/OpenMP implementations and versions are actually loaded for each relevant Python environment.
- Native-library thread counts and actual core utilization under **one worker** versus the normal **six-worker (if still current)** workload.
- Conservative, documented alternatives (for example, suitable controls through `threadpoolctl` and/or relevant `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `OMP_NUM_THREADS`, `BLIS_NUM_THREADS` settings), applied only in controlled benchmark configurations.
- Nested parallelism, competing threading runtimes, and the distinction between thread limits that are process-wide and thread-local on Windows.
- Whether improved throughput comes from lower thread counts, different worker concurrency, batching, or other resource scheduling rather than source compilation.

**No blanket rule such as "one BLAS thread per worker" is approved.** Whether such a configuration helps is workload-dependent. Any eventual worker/thread-control change is subject to the project's process-concurrency and safety governance, independent review, and scientific equivalence checks.

## 7. Candidate performance approaches (not final selections)

| Approach | Plausible benefit | Important limitations and provisional standing |
| --- | --- | --- |
| **Better use of NumPy/SciPy**: batching, vectorized operations where appropriate, fewer temporary arrays/copies, memory layout, better API selection | Can reduce dispatch/allocation overhead or leverage existing highly optimized kernels | First to test where profiler evidence points; maintain operation order and semantics where required. |
| **Native-thread and worker concurrency tuning** | Could improve whole-job throughput and memory efficiency without compiling methods | Benchmark carefully; can change floating-point reduction order and must not compromise coordinator safety. |
| **Numba**: LLVM-based just-in-time compilation of selected supported functions (e.g., `@njit(cache=True)`) | Promising for hot numerical loops on NumPy arrays with relatively small localized changes | Supports only a subset of Python/NumPy/SciPy behavior inside compiled functions; first-call compilation, cache and cold-start costs matter. Fast-math/parallel features can change results. **Provisional first candidate**, not mandated. |
| **Cython**: compile selected source modules/functions to C/C++-backed extension modules | Strong for explicitly typed tight loops, efficient typed memoryviews over NumPy buffers, and custom native-array kernels | Largest gains may require careful type declarations and code changes, compiler/build support and maintenance; normal Python calls into SciPy remain native/library calls. **Strong second candidate** (or first for kernels better suited to it). |
| **mypyc**: compiled extensions from suitably typed Python | May help some frequently invoked typed, object-oriented Python modules | Less obviously suited to heavy NumPy/SciPy kernels; exploratory only. |
| **Nuitka**: compile Python program through C/C++ toolchain | Potential runtime and distribution benefits for some code | No universal computational speedup; compiled NumPy/SciPy still dominate when already native; project-wide packaging complexity. Lower priority. |
| **PyInstaller** | Packages an application and dependencies into a deployable program | Primarily packaging; does not turn Python calculations into native optimized loops. Not a performance candidate. |
| **CPython bytecode (`compileall`, `.pyc`)** | May reduce repeat Python import/compilation overhead | Generally no steady-state numerical acceleration. No primary role. |
| **CPython experimental JIT / alternative interpreter builds** | Potential interpreter-wide improvement where supported and correctly configured | Experimental/build- and platform-dependent; must evaluate Python ABI/wheel/library compatibility, accuracy and actual gains. Later exploratory candidate only. |
| **Pure algorithmic/data-structure improvements** | Sometimes larger gains than compilation | May change mathematical semantics or method identity; requires stricter method-level scientific review. Distinguish transparent implementation efficiency from a new scientific method/revision. |

### 7.1 Why Numba leads the initial compiler investigation

Numba is particularly suited to contained numerical kernels and may let a function remain mostly recognizable as Python. The idea is to select **proven hot functions**, not decorate the entire project indiscriminately. For supported code, JIT compilation avoids Python-loop overhead during repeated execution; warm-up/first-call costs must be counted separately. Numba 0.68 introduced Python 3.15 support, and 0.68.1 has a Windows x64 CPython 3.15 wheel as of 2026-10-27. This demonstrates *availability at the date of this proposal*, not guaranteed compatibility with the project's final environment or every SciPy API.

### 7.2 Why Cython remains important

Cython can compile selected routines into `.pyd` extension modules on Windows, imported by the existing Python architecture. Explicit C types and typed memoryviews can remove much of Python's scalar-loop and array-element-access overhead. It may outperform a Numba attempt on some kernels or handle patterns Numba cannot. Simply compiling unmodified Python is not a guaranteed large speedup; assess the actual workload and required maintenance.

### 7.3 Heterogeneous optimization is acceptable

A method that delegates most work to a large SciPy solver may require no source compilation. Another may use a small Numba-accelerated kernel. Another may benefit most from Cython. Another might need an improved NumPy batching strategy. Keep these choices modular and independently benchmarked; **never exclude, retire, or change an experimental method merely because it is slower or strongly correlated with another**.

## 8. Scientific correctness and reproducibility safeguards

This project explores unconventional hypotheses about physical randomness. Performance engineering must not turn an experimental scientific method into a different experiment without saying so.

1. **No leakage or changed boundaries.** Preserve N-1/prefix isolation, approved data views, compound game/draw identities, and all hold-out restrictions. No profiling study authorizes opening a reserved hold-out.
2. **Forecast and ranking invariants.** When an optimization is presented as a transparent implementation change, compare its outputs with frozen baseline fixtures: canonical forecasts, TOP/WORST selection from the same ranking, tie-breaking, seeds, and all applicable provenance/digest fields. A change to float ordering, tie behavior or predictions is consequential.
3. **Numerical semantics.** Explicitly assess floating-point precision/rounding, reassociation, vectorized reduction order, BLAS threading, numerical tolerances, NaN/Inf behavior, RNG sequences, parallel ordering and deterministic initialization. Do **not** enable relaxed `fastmath` or parallel RNG/reduction options as if they were automatically equivalent.
4. **Version governance.** Preserve the currently ratified method-revision and archival scheme (including revision-labelled source preservation). A changed algorithm or consequential numerical behavior may require a **new method revision or new experiment ID**, decided under existing governance, not a silent overwrite.
5. **Baseline is immutable for evaluation.** Retain the original implementation and reference predictions/results; compare candidate variants in a separated, non-contaminating benchmark environment.
6. **Independent review.** Changes affecting seeds/forecasts, TOP/WORST, data views/leakage, hold-outs, coordinator/manifest/status, process termination, firewall/orphan safety or destructive switches remain in the project's **always-review** category and must not be expedited through a routine fix-and-proceed path.
7. **No false performance claim.** If a candidate gets faster by doing less work, skipping validation, bypassing safety steps, changing scientific work, reducing output, or using an unfair workload, that is not an equivalent speedup.

A successful candidate must demonstrate both performance benefit **and** scientifically defensible behavior. Where strict bitwise identity is not feasible, document numerical differences, decision impact and required method-revision treatment; the owner and independent reviewer decide whether to proceed.

## 9. Process-safety and operational boundaries

The existing coordinator's process lifecycle and orphan interlock are out of scope for casual optimization. In particular:

- No changes to process-termination enable switches or kill logic without the required independent review and owner approval.
- No termination or signaling to a process whose PID **and creation time**, status binding, and verified coordinator ancestry have not been positively established under the ratified rules.
- No profiler-induced manual killing, stale-PID attachment, unreviewed coordinator modification, or bypass of unresolved-orphan safety markers.
- Where profiles must be collected, favor **isolated, disposable, review-approved test harnesses**, not production coordinator-owned live work. External profiler attachment is a safety/permissions decision in its own right and should not be assumed harmless.
- Run result-consumption firewall and manifest/status-hash validation remain authoritative; profiler artifacts do not make a failed or orphan-suspected scientific result valid.
- Keep benchmarks' resource use within machine limits. A profiler, JIT compiler or build tool may itself consume memory and CPU; normal six-worker concurrency is not automatically appropriate during deep profiling.

No installation or execution of an experimental compiler is authorized by this document.

## 10. Proposed future workflow and review gates

### P0 — Activation and scope confirmation (owner decision)

Only after full project implementation: reconcile this document against the **then-current** ratified architecture, register, methods, safety agreements, hardware, Python/environment and dependencies. Assign the stage identifier, owner/reviewer roles, representative work matrix, safety review scope, acceptable precision and performance criteria. No implementation before this gate.

### P1 — Establish objective baselines

Run uninstrumented reference workloads. Record complete environment provenance and repeated wall/CPU/memory/concurrency metrics. Validate outputs and avoid consuming invalid scientific results. Separate method time from coordinator and startup overhead.

**Deliverable:** baseline benchmark inventory, protocol, timings and output hashes/identities.

### P2 — Profile the existing program, without optimizing it

Run approved sampling profiles in wall and CPU modes; compare worker and full-batch profiles; use deterministic tracing for exact call/caller counts. Map Python-to-NumPy/SciPy calls. Record native boundaries, worker imbalance, blocking and memory. Use a native profiler only when Python profiling leaves a consequential unresolved native hotspot.

**Deliverable:** evidence-based hotspot ranking with estimates and uncertainty, separated by workload/method/phase, with explicit limitations.

### P3 — Examine low-invasiveness improvements first

Evaluate batching, use of optimized existing NumPy/SciPy operations, avoidable allocations, data layout and the existing worker/native-thread interaction. Use separate experimental branches/harnesses and exact fairness controls. If the bottleneck is startup or I/O, pursue that rather than numerical compilation.

**Deliverable:** prioritized options and expected/observed throughput changes, with a statement on scientific equivalence risk.

### P4 — Evaluate selective compilers on measured hotspots

Choose **one or a few** representative expensive kernels and compare unchanged Python, a suitable Numba implementation, and a suitable Cython implementation. Include build/integration effort, dependencies, cold/warm execution, numerical identity, memory, diagnostics, concurrency behavior, and full-batch impact. Optionally explore mypyc, Nuitka or an experimental interpreter only if earlier profiling makes a credible case.

**Deliverable:** reproducible benchmark matrix and trade-off analysis, not a wholesale rewrite.

### P5 — Independent review and owner go/no-go

Independently review benchmarks, safety constraints, exact numerical results, artifact identities, reproducibility, maintenance, and any affected method-revision decisions. Owner chooses whether to adopt each candidate, retain Python, defer, or abandon optimization. Performance alone is insufficient.

**Deliverable:** explicit decision record with the reviewed scope, chosen candidates, exclusions, outstanding risks and rollback plan.

### P6 — Controlled integration, if approved

Only for approved candidates: implement/review/test via normal project controls, verify canonical scientific results and build reproducibility, benchmark again end-to-end, and document how to disable or revert acceleration. Preserve an ordinary-Python reference execution path where practical.

**Deliverable:** reviewed integration with before/after performance and correctness evidence.

### P7 — Optional deployment packaging (independent decision)

If a standalone Windows deliverable is genuinely useful, study Nuitka/PyInstaller and the complete dynamic-import and NumPy/SciPy dependency closure separately. Test Windows builds, DLLs, CPU compatibility, startup, size, extraction behavior, antivirus interactions and reproducible environments. Do not conflate one-file distribution with computational speed. The existing virtual environment / BAT-driven development workflow may remain preferable.

**Deliverable:** packaging decision, only if requested; not a prerequisite for performance success.

## 11. Benchmark design and selection criteria

Before work begins, define a **representative matrix**, for example:

- A compute-heavy Python-loop method; a NumPy-dominant method; a SciPy-solver-heavy method; a mixed method; a fast/short method where startup overhead could dominate; and a full typical cohort or batch.
- Cold process startup and warm steady state; modest and large workload sizes; single worker and normal concurrent workers.
- At least the current reference interpreter and any candidate optimized build on the same machine and matching data; confirm whether the working virtual environment is actually CPython 3.15.2.
- Controlled thread settings, repeated randomized/interleaved trial order if feasible, and observation of thermal/frequency throttling, memory and background load.

Proposed measures (to finalize at P0):

| Measure | Why it matters |
| --- | --- |
| End-to-end elapsed seconds and batch throughput | Primary practical outcome. |
| Per-method and per-phase elapsed seconds | Identify real bottlenecks. |
| Aggregate and per-process CPU seconds | Distinguish compute and waiting; account for parallelism. |
| Peak per-process and total memory | Avoid trading speed for swapping or worker failure. |
| CPU/core occupancy and native thread counts | Detect nested threading and oversubscription. |
| Cold-start/JIT compile and warm-run times | Fair comparisons for intermittent experiments. |
| Source, environment, inputs, seeds, output digests | Scientific and performance reproducibility. |
| Result/ranking/forecast equivalence and error budget | Ensure speed was not bought by changing the method. |
| Build, debugging and long-term maintenance cost | Decide whether gains justify complexity. |

**Decision principle:** Prefer the simplest approach with a *repeatable, material improvement in the normal end-to-end workload* and no unacceptable impact on scientific correctness, safety, transparency or maintainability. The threshold for “material” is intentionally not fixed in v0.1.

## 12. What is deliberately *not* decided now

- No selection of Numba, Cython, Nuitka, mypyc, an experimental JIT, or any profiling product as a permanent project dependency.
- No blanket compiler conversion of methods or the coordinator.
- No guarantee of a 5x, 10x or other speed increase; potential Cython benefits vary by workload and static typing.
- No automatic adoption of a one-file Windows executable.
- No changes to scientific method definitions, inclusion criteria, ranking, TOP/WORST production, data views, hold-out access, or seed management.
- No specific benchmark sample sizes, exact workload set, speedup threshold or machine hardware locked in until activation.
- No changes to default concurrency, process safety switches, timeout/kill ownership, or firewall/orphan rules.
- No immediate software installation, repository source-code changes or experiment runs.

## 13. Recommended scheduling instruction for the project plan/register

> **DEFERRED STAGE — Performance characterization and selective acceleration (proposal v0.1).** After full implementation of the randomness project, first establish reproducible unoptimized baselines; then profile Python execution and NumPy/SciPy/native-library boundaries using Python 3.15's sampling and deterministic profilers and deeper native tooling if justified. Measure wall-clock, CPU, memory and six-worker/native-thread interaction. Based on observed bottlenecks, evaluate non-invasive NumPy/SciPy/threading improvements followed by selective Numba and Cython acceleration where appropriate. Preserve method revisions, canonical outputs, N-1/hold-out restrictions, TOP/WORST semantics, and the coordinator/orphan/firewall safety contracts. All optimization and packaging choices remain subject to independent review and owner approval. Standalone Windows EXE packaging is a separate lower-priority decision. **Not authorized to execute until explicitly activated.**

## 14. Reference documentation (verified 2026-10-31; re-check on activation)

1. Python 3.15.2 release: https://www.python.org/downloads/release/python-3152/
2. Python 3.15 sampling profiler (Tachyon), CLI, native boundaries, subprocesses and Windows permissions: https://docs.python.org/3.15/library/profiling.sampling.html
3. Python 3.15 deterministic profiler (`profiling.tracing` / `cProfile`): https://docs.python.org/3.15/library/profiling.tracing.html
4. Numba 0.68 Python 3.15 release notes: https://numba.readthedocs.io/en/latest/release/0.68.0-notes.html
5. Numba supported Python/NumPy dependency versions: https://github.com/numba/numba/blob/main/docs/source/user/installing.rst
6. Cython typed memoryviews and efficient NumPy-buffer access: https://cython.readthedocs.io/en/latest/src/userguide/memoryviews.html
7. `threadpoolctl` native BLAS/OpenMP introspection and controls: https://github.com/joblib/threadpoolctl
8. Project source of truth (consult current ratified documents at activation): https://github.com/hydra3333/analysing_perceived_randomness_in_reality

---

**End of proposal v0.1.** The key commitment is to remember and schedule the **profiling-first** study after implementation, not to preselect a compiler before the evidence exists.
