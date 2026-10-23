# Predictive Randomness — ChatGPT Project Continuation and Recovery Handback

**Version:** v0.1 — **REVIEW CANDIDATE; not yet owner-ratified**  
**Prepared:** 23 October 2026 (Australia/Adelaide)  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Intended repository destination:** `doc/HANDOVER/Predictive_Randomness_ChatGPT_Continuation_Handback_v0_1.md` *after review/ratification*  
**Snapshot source:** the owner's newly supplied, post-commit/push GitHub ZIP `analysing_perceived_randomness_in_reality-main(4).zip`  
**Status at transfer:** P0 standalone engineering demonstrations pass; P1 one-worker coordinator test passes; P1/P2 process-ownership safety patch v0.2 has passed a **one-worker non-destructive Windows ancestry preview**. Destructive cleanup, six-worker Windows acceptance, and production approval are **NOT** complete.

> **Start here in a new ChatGPT conversation.** This file is a factual orientation and current-state ledger, **not** an amendment to the project's ratified specifications. Read the attached **whole repository ZIP** alongside this handback. Confirm the source identity and inspect the named ratified documents and implementation before changing code. Do **not** assume that a ratified architectural requirement has passed its Windows implementation tests. Do not activate the process-termination safety switch. Do not start scientific E-method implementation without a separately approved P3 task.

---

## 1. Opening procedure for the replacement ChatGPT

1. Read this handback in full. Then read the **current** ratified project documents named in §3, with particular attention to Architecture v0.4 §5C, the approved R2 erratum, and the POC task specification. The ZIP has the complete files; this handback is not a substitute for their detailed scientific contracts.
2. Inspect the repository ZIP's relevant `.bat`, Python, safety-review and test files. The actual source, not a speculative reconstructed implementation, governs any code review. Check the safety switch in `src/Powerball_Experiment_Coordinator.py` remains `False`.
3. Confirm whether the user has supplied a **newer** repository ZIP or commit since this handback. If so, first reconcile the changed files and do not apply older patches blindly.
4. Distinguish four states: **RATIFIED design**; **IMPLEMENTED source**; **PASSED Windows evidence**; and **PENDING tests/decisions**. Do not silently promote one to another.
5. Acknowledge the current stage, open safety gates and source identity. The owner has requested a pause to establish a sound handover before additional P2 tests. The **next technical test** after owner/Claude review is the six-worker **non-destructive** process-tree preview, not termination.
6. Continue the established collaborative process: ChatGPT drafts/implements; Claude independently reviews important design/safety changes; the owner resolves and ratifies. Do not claim a Git commit, a production acceptance, or completed Windows test without corresponding evidence.

**Not permitted as an unprompted new-chat action:** enabling `ENABLE_PROCESS_TERMINATION`, invoking the timeout/forced-termination/interrupt/memory-stress tests, executing a lottery predictor, opening the sealed holdout, upgrading Python/PyPI dependencies, rewriting ratified specifications, or replacing the repository wholesale.

---

## 2. Source provenance and machine environment

### 2.1 Attached repository snapshot — independently inspected for this handback

- Input: `analysing_perceived_randomness_in_reality-main(4).zip`, supplied by the owner after reporting a Git commit/push; its extracted top directory is `analysing_perceived_randomness_in_reality-main/`.
- **ZIP SHA-256:** `77cfd287e5d444c3eae426392c8dccc4e5cc188d1e1e5faa2e7b4ce067105b06`.
- GitHub ZIP archive comment: `6b527627f7f98fd5cd88f4bea76e16b9cb56d372` (40 hex characters). This is **archive metadata** and may be the exported commit identifier; it was **not verified using `.git`**. Do not assert that it equals the owner's local `HEAD` without checking.
- ZIP inventory: 57 directory/file archive entries; 45 regular files. It contains the ratified v0.4 architecture, P1/P2 safety patch v0.2 implementation and tests, Claude safety review v2, project datasets and older history files.
- The source ZIP does **not** contain `.git`. The user reported that the snapshot followed a commit/push, but the local checkout `HEAD`, Git status and remote commit signature were not independently retrieved. Ask for or inspect these **only when needed**:

```cmd
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git rev-parse HEAD
git status --short
git log -1 --format="%h %s %ci"
```

**Important:** If this handback is added and committed later, its new commit will necessarily differ from the source ZIP snapshot. Preserve both identities; never pretend the snapshot includes its own subsequent handback commit.

### 2.2 Owner-reported development platform and practice

- Windows 11; VS Code for editing and Git operations; standard CMD for running `.bat` launchers and tests.
- Python 3.14.8 in a project-local `.venv` (tested on the owner's Windows machine); Ryzen 9 3900X, 12 physical cores, 32 GB RAM.
- Local repository root: `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`.
- User downloads ChatGPT-delivered small **repository-relative ZIP overlays**, reviews preservation rules, extracts deliberately, tests in Windows, and commits/pushes himself. The assistant does **not** have write access to this local checkout.
- `.gitattributes` requires `*.bat text eol=crlf`. `transitory_data/poc_runs/` and `transitory_data/dependency_snapshots/` are `.gitignore`d. Preserve real `source_data`, ratified `doc`, scraper and unrelated files.

---

## 3. Authority and project decisions

### 3.1 Binding project documents: read current versions, not superseded drafts

| Repository path (under `doc/`) | Status established by subsequent owner decisions | Main authority |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_3.md` | **RATIFIED**, 22 Oct 2026 | Objectives, epistemic openness, scientific governance, datasets/holdout, retention. |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | **RATIFIED**, 22 Oct 2026 | Permanent E_1–E_62 research catalogue; hypotheses, sources, family definitions. |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` | **RATIFIED**, 22 Oct 2026 | Historical visibility, modes, I/O, ranking, TOP/WORST, seeds, reproducibility, method contracts. |
| `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` | **OWNER-APPROVED**; ERR-R2-02 **provisional pending Windows test/review** | Narrow operational precedence: 1-versus-configured-maximum (currently 6), Option F pilot, one dependency-list authority, fitted-model vs deterministic readout seeding. Historical R2 v0.3 remains untouched. |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_2.md` | **RATIFIED**, 22 Oct 2026 | Scoring/evaluation, immutable before-outcome outputs, worst-pick readout, reporting, sealed holdout. |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_4.md` | **RATIFIED**, 23 Oct 2026 | Architecture 2, compulsory Option F interface, `.venv` discipline, process ownership, safety acceptance gates (especially §5C). |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_1.md` | **RATIFIED** P0–P2 task specification | Staged Windows engineering tests and W-suite; P3 scientific method requires independent authorization. |

**Version-status warning:** Some historical sections and original headers still say “review draft” or “proposed” because those source drafts were ratified through **later owner messages** without rewriting every historical heading. Do not undo owner decisions merely because a retained historical heading says draft. Conversely, the approved R2 erratum's **ERR-R2-02** production acceptance remains conditional. Later ratified changes prevail over older provisional alternatives.

**Supporting, not binding:** `Claude_Safety_Review_POC_Coordinator_Termination_v2.md` at repository root (independent review; no source change by itself); `P0_INITIAL_SOURCE_PACKAGE_HANDOVER_v0_1.md`; `P1_P2_Coordinator_Ownership_Safety_Handback_v0_2.md`; earlier POC and architecture handbacks/diffs. Retain evidence, but the approved specifications and owner rulings prevail.

### 3.2 Scope and scientific protections

- Study whether apparently random physical results exhibit **testable, prospectively exploitable** structure, including unconventional candidate mechanisms. Neither presume predictability nor exclude methods solely because independent-draw theory predicts no advantage. Statistical rigor still governs conclusions.
- Australian Powerball rules for this era: **seven distinct main balls from 1–35** plus **one Powerball from 1–20**. The historical same-rule era begins at draw **#1144, 2018-04-19**.
- The attached files `source_data/australian_powerball_history_20261021.csv` and `source_data/australian_powerball_draw_order_20261021.csv` each contain **444 rows, draws #1144–#1587, through 2026-10-15**, verified directly from the ZIP. The date suffix in each **filename is not the last draw date**. The first is sorted/main-number history; the second retains reported drawn-position order, important for order-specific hypotheses. They are **not** POC inputs.
- The R1-era originally reserved **final ten draws #1578–#1587 as the holdout**. Treat the held-out outcomes as **sealed**, even though their rows physically exist in the source CSV. Development/evaluation eligibility must be enforced by the ratified split and any subsequently ratified controlled changes. Do not inspect holdout outcomes during method development or tune against them. Source updates/newer draws must not silently redefine this split.
- At forecast target N, fit only on permitted observations **strictly before N** (N−1 boundary). A genuine FINAL forecast after last permitted draw L targets **L+1** and must be frozen before the result. No post-outcome re-selection.
- Produce deterministic, label-neutral complete rankings/readout with **TOP seven and WORST seven** from the same frozen ranking. **WORST is the exact bottom seven** (or top seven of reversed ranking), not an after-draw “worst-performing” selection. Tied TOP/WORST readout uses independently versioned `TIE_SHA256_V1`; downstream tie/readout seed must not contaminate stochastic model-fitting seed. Post-draw rank-position analysis (including mid-ranks on tied scores) must not change pre-draw picks.
- Keep all 62 scientific E-method identities, unsuccessful methods, inconclusive and exploratory results; synthetic engineering fixtures have **no E_ identity** and must never masquerade as lottery predictions.
- Do not infer success from the fixture digest or a coordinator PASS. A scientific method must later meet independent maths review, training-cutoff test, reproducibility, benchmark and leakage checks.

### 3.3 Development batching decision (future, not part of current POC)

- First genuine methods **E_1–E_6 one by one** to validate common helpers (training view, ranking/ties, TOP/WORST, status/results).
- Then review and build **families** in ~6–10-method batches: validate *one lead method* and its independent, hand-checkable maths fixture before implementing siblings. Family groups discussed with Claude: E_7–16 frequency/Bayesian; E_17–22 recurrence; E_23–32 within-draw/order; E_33–40 spectral; E_41–48 information/nonlinear; E_49–54 ML/external; E_55–56 ensembles last; E_57–62 pilot-wave. Give E_12, E_38, E_52, E_53 and E_57–E_62 extra individual mathematics/performance review.
- `FORMULA_OPEN` choices must be specified and ratified family by family *before* cloning code across methods. Automatic contracts per method include N-and-later leakage perturbation, output/ranking legality, TOP/WORST reversal, one-vs-six identity and repeated-run determinism. Keep the reserved holdout sealed.
- **Six workers is an execution capacity limit, not a mandate for exactly six methods per development batch.** No production predictor is implemented yet; a separate P3 task and authorization are required.

---

## 4. Ratified launch and dependency architecture — Option F

**The same `Run_Experiment.bat` is mandatory for every normal individual engineering/prototype/scientific experiment invocation, irrespective of whether initiated manually or dispatched by the coordinator.** Direct `.py` invocation is allowed for isolated debugging/unit tests, **not** as an alternative operational/production route. The coordinator may not silently fall back to direct `sys.executable` on launcher failure; that requires a separately approved architecture change.

```text
INDIVIDUAL:
  User / CMD / VS Code -> Run_Experiment.bat -> standalone Python experiment

COORDINATED:
  User / CMD / VS Code -> Run_Coordinator.bat
     -> src/Powerball_Experiment_Coordinator.py
        -> Run_Experiment.bat (independently for EACH worker)
           -> standalone Python experiment
```

- `Run_Coordinator.bat` and `Run_Experiment.bat` are self-protecting Windows `.bat` entry points. They use `SETLOCAL` and project-relative `.venv`, check interpreter identity via `sys.prefix`, activate internally only when no venv is active, refuse a conflicting venv, set numerical threads initially to one, pass supported parameters and return exit codes.
- **The Python coordinator itself** insists that normalized `VIRTUAL_ENV` **and** `sys.prefix` match the project's `.venv`. Under the normal coordinated path the human-facing coordinator batch wrapper activates if necessary **before** Python coordinator execution; child `Run_Experiment.bat` wrappers inherit that active environment, so generally **verify** rather than activating again. Direct Python coordinator from an inactive environment is rejected. Manual standalone experiment wrapper activation/restoration is already Windows-tested; the coordinator wrapper's inactive-start/restoration is **still pending**.
- Initial concurrency configurable **1–6**, with **six default and maximum**. The normal option F mechanism is `subprocess.Popen` with stdout/stderr capture, independent method processes and per-worker status/result validation. Do not introduce custom Windows Job Objects, broad process termination, central shared-process prediction fitting or self-created method process pools without controlled owner review.
- All human-maintained direct pip package names and installs/upgrades belong **only** in `install_upgrade_dependencies_into_venv.bat` (current: `requests beautifulsoup4 psutil numpy scipy threadpoolctl`; `VERIFY`, `INSTALL`, `UPGRADE`; default `VERIFY`). `VERIFY` or normal run must **never** trigger implicit upgrades. Generated `transitory_data/dependency_snapshots/*` are evidence, not another dependency authority. The repository still tracks an **older `requirements.txt`** (eight pinned packages) — leave untouched pending an explicit retire/historical/generated-file decision; do **not** manually maintain it as a parallel source of authority.
- On the owner's Windows installation, previous dependency maintenance succeeded with Python 3.14.8 and reported `psutil 7.2.2`, `numpy 2.5.4`, `scipy 1.18.1`, `threadpoolctl 3.7.0`, `requests 2.34.2`, `beautifulsoup4 4.15.0`; these are historical observed versions, **not** independently fetched from the user's present `.venv` by reading a GitHub ZIP.

---

## 5. Current implementation in the attached ZIP

### 5.1 Active engineering files

```text
Run_Experiment.bat                              # individual and per-coordinator worker
Run_Coordinator.bat                             # human-coordinator launcher
install_upgrade_dependencies_into_venv.bat     # single owner-maintained package authority
src/Powerball_Experiment_Coordinator.py        # current P1/P2 coordinator, safety patch v0.2
src/methods/POC_Architecture_Probe.py          # synthetic argv/canonical/error tests
src/methods/POC_Coordinator_Probe.py           # synthetic sleep/CPU/memory engineering tests
src/methods/_common/                          # paths, runtime status, environment, JSON output
src/scrape_australian_powerball_history_from_2018_04_19_v0_3.py  # scraper, not an E-method
tests/p0_static_checks.py
tests/p1p2_static_checks.py
tests/p1p2_non_destructive_safety_checks.py
tests/windows_architecture_poc_suite.py       # optional timeout case; SEE SAFETY CAUTION BELOW
tests/fixtures/poc_canonical_fixture.json
P0_INITIAL_SOURCE_PACKAGE_HANDOVER_v0_1.md
P1_P2_Coordinator_Ownership_Safety_Handback_v0_2.md
Claude_Safety_Review_POC_Coordinator_Termination_v2.md
```

- `src/Powerball_Experiment_Coordinator.py` is **engineering-POC-only**: requires `--poc`, restricts available cases to whitelisted synthetic probes, limits workers to six and never discovers a production E-method. Do **not** claim production-method coordination is already implemented.
- Unique IDs isolate output under ignored `transitory_data/poc_runs/<id>/`. Typical per-probe files are `status.json`, `canonical_result.json`; coordinated groups additionally have `manifest.json`, `runtime_environment.json`, `pip_freeze.txt`, and per-worker stdout logs. Successful status and result digest must be checked, not merely a zero process exit.
- Current patch implements retained ancestry, owner kill switch, non-destructive plan output, narrow executable-name sanity checks, conservative failure handling and SIGINT flag handling. These are **source implementations pending extended Windows tests**, not proven production-safe termination.
- The original source ZIP retains `Predictive_Randomness_P1_P2_Coordinator_Ownership_Safety_Patch_v0_2.zip` as a historical patch payload. **Do not re-extract that ZIP over later checked-out source.** `src/Powerball_Experiment_Coordinator.py` from the current user-supplied snapshot is the operative code.

### 5.2 Source snapshot integrity anchors (SHA-256 of unmodified ZIP members)

The table below is **file-byte evidence** for detecting inadvertent changes, not a Git proof or license to overwrite a newer file:

| SHA-256 | Repository-relative file |
|---|---|
| `04e061d13b69e49c0dc227b7093570e96598d4c416952ac6092af4d3d14d4b64` | `doc/Predictive_Randomness_Research_Project_Proposal_v0_3.md` |
| `19809ae8a1aca716c6c6a4de71a37b705129304894a2b382036d51b76575b99f` | `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` |
| `7ec4bad9ab00a619a42cedc4abbe4bec393589563d3bc3061ab4737525259d71` | `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` |
| `a08b4e7620be8cb32142b23146c5f82c415a50e56cba0b2ea3bed6e1a4b80d5e` | `doc/Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` |
| `dd0b5243ad8f93a0de7c502e2e6ce54a99c5e427063ce7b3e49313fb18975800` | `doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_2.md` |
| `7526e381be93caa68ce8f8a6b90f135748925f1c0b080e171e1ef18cd771f257` | `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_4.md` |
| `26c471e183d073db6e258a51c5b363f90d3024bc497ebebeba804a25ab187cf4` | `src/Powerball_Experiment_Coordinator.py` |
| `a9056a336a2f243510522ed72e0d884611de46b07e4363d7f2f834a77410618e` | `Run_Experiment.bat` |
| `ba9719d42279e488ff079d1507eb11167a753307c31c5dc713e78da1f47b6d7b` | `Run_Coordinator.bat` |
| `d39f65ad5e4d40b6ba66daf05ced6aa066f6312228c17b39c1fa1ed92669ad24` | `P1_P2_Coordinator_Ownership_Safety_Handback_v0_2.md` |
| `fe9eaeb4984d94c89a8e011e4c90d95b99ae41fe43b9e9930a2b730b1048d790` | `Claude_Safety_Review_POC_Coordinator_Termination_v2.md` |

### 5.3 Process termination invariant — owner's critical safety requirement

At the **top of the coordinator's source**:

```python
ENABLE_PROCESS_TERMINATION = False
```

**Never change this to `True` without explicit owner authorization following independent review and completed non-destructive Windows gates.** No CLI option overrides this flag. A plan-only request is never destructive even if a future owner-approved revision enables the switch.

- **Before** every coordinator cleanup request, issue `[SAFETY BEFORE]` and per-target `[SAFETY TARGET]` information: root and children PID, executable name, creation time, reason, switch state, ancestry/proof. **After**, issue `[SAFETY AFTER]`: preview/no signals, refusal, actual attempted signals and survivors/outcome. Emit honest incomplete cleanup states; do not misreport “stopped” while the switch is `False`.
- Ownership must be established by capturing **actual descendants of the coordinator's launched `Run_Experiment.bat` root `cmd.exe` while that wrapper lives**; retain `psutil.Process` identity objects (PID plus creation time), validate each parent-child edge, and only then consider a process eligible for termination.
- The experiment `status.json` PID and creation time verify that the **right experiment** was observed; **never** construct an additional kill target from status-file PID alone (nor from any external name/PID). The root may be terminated through its original `Popen` handle only; owned descendants through retained, verified `psutil.Process` objects only.
- Root expected process name `cmd.exe`. In the **normal coordinated path** current source sanity-filter permits descendants named `cmd.exe`, `findstr.exe`, `python.exe`: the wrapper uses `findstr.exe` for filename validation and may spawn transient CMD processes. The two-Python process pattern observed on Windows is consistent with venv redirector plus interpreter, though transient pre-check processes may already have exited. `chcp.com` is **not expected** under normal coordinator-managed workers, because their venv is inherited and not reactivated.
- **Process names are not ownership proof**; they are a refusal/anomaly filter. Never use `taskkill /IM`, `taskkill /PID ... /T /F` as an automatic fallback, terminate other Python projects by process name, or reconstruct an uncaptured kill list. If ancestry/identity fails, **leave the process running, report `UNVERIFIED`/`ORPHAN_SUSPECTED`/`TERMINATION_DISABLED`, stop new scheduling and request human inspection**.
- Without operating-system containment there is no absolute guarantee that *all* descendants are captured or stopped. The design prioritizes **not terminating unrelated software** over guaranteed orphan cleanup. There are no project-managed Job Objects under the present ratification.
- Special caveat: pressing Ctrl+C in the shared console can send signals to child processes independently of the coordinator; the global Boolean controls only the coordinator's *own kill calls*. A disabled flag is **not** a universal OS process-protection barrier.

---

## 6. Windows evidence ledger — distinguish observation from acceptance

### 6.1 Passed or substantively demonstrated by the owner's console transcripts

| Stage / test | Actual Windows observation | Evidence status |
|---|---|---|
| P0 Python static check | `python tests\p0_static_checks.py` reported CRLF/import/canonical-fixture PASS. | PASS (static; not standalone proof of all Windows CMD behaviours). |
| Dependency maintenance | Explicit `INSTALL` and `VERIFY` succeeded; `pip check` clean. The batch installer was revised to concise direct-package output, then `VERIFY` passed. | PASS for those executions; no package upgrade/W-23 gate implied. |
| Individual wrapper activated `.venv` | `Run_Experiment.bat` with `.venv` already active successfully echoed argv, root/cwd, project interpreter, and four BLAS thread variables equal `1`. | PASS. |
| Individual wrapper from inactive `.venv` | On owner CMD, activated internally, ran echo-argv, returned `0`, and left parent `VIRTUAL_ENV` undefined. | PASS. |
| Conflicting venv | Simulated `VIRTUAL_ENV=E:\POC_FAKE_DIFFERENT_VENV` in separate `cmd /d`; wrapper refused and returned `6`; parent CMD environment unchanged. | PASS **for simulated conflict**, not every possible real second-venv activation. |
| Invalid/nonexistent filename | `..\POC_Architecture_Probe.py` and `.txt` refused with exit `4`; nonexistent `.py` refused with exit `5`. | PASS. |
| Synthetic canonical fixture | Standalone `canonical-fixture`: SHA-256 of canonical result `a853ac3545213c8f9be9355e312bf220a74fa89f240e4123aed308d983350937`. | PASS; **synthetic engineering data only**. |
| Failure/hard-exit | Explicit `--exit=3` returned `3` with FAILED status; W-11 `os._exit(7)` returned `7`, left STARTED-only status, no valid result. | PASS for standalone negative behaviour. |
| Existing-output protection | Same-run-ID sentinel `canonical_result.json` was preserved when a repeated probe failed with `FileExistsError`; SHA of preserved sentinel `69dbeb787edda70eac7bf7d1cbedebf7e5f8341ed7f625446eab6e54857cff3a`. | **Partial A-17/A-18 and POC-Q08**, **NOT W-23** (which is upgrade-gating and UNTESTED). Concurrent collisions remain untested. |
| P1 one-worker coordinator v0.1 | `Run_Coordinator.bat --poc --case=canonical-fixture --count=1 --workers=1`: worker BEGIN/RESULT/DIGEST/FINISH, matching canonical digest, `PASS successes=1/1`, exit `0`. | PASS; real Windows batch launch/pipe/result, **not** forced termination. |
| P1/P2 static and synthetic safety v0.2 | `p1p2_static_checks.py` PASS; `p1p2_non_destructive_safety_checks.py` PASS N2/N3 synthetic status, N4/N5 simulated per-edge/name, switch False, BEFORE/AFTER, no kill. | PASS **synthetic/static**; not proof of live unrelated-process protection. |
| **Latest P1/P2 one-worker live ownership preview v0.2** | On Windows: group `coord-04692b32b8ee4e6d97f0ac8dd5cb04a8`, `--case=sleep-timeout --count=1 --workers=1 --sleep-seconds=12 --timeout-seconds=45 --plan-termination`; root `cmd.exe` PID `26116`, descendants `python.exe` PID `27848` (depth 1) and PID `26768` (depth 2); `experiment_matched=True`, `unmatched_status=none`, `ownership_anomalies=none`, switch False, BEFORE/AFTER preview, no signals, worker normal SUCCESS, group `PASS successes=1/1`, exit `0`. | **PASS: one-worker LIVE NON-DESTRUCTIVE ownership preview**. This does **not** certify any kill. |

Earlier standalone W-11 run ID: `poc_W11_20261022_A`. The latest live preview group is under ignored `transitory_data/poc_runs/`, and its transient evidence is **not** included in the source GitHub ZIP. Its console transcript was supplied by the owner, not reconstructed from this archive. An earlier unsafe test instruction used interactive `setlocal` (which did not establish a protected local scope); corrected with separate CMD process; no demonstrated wrapper defect followed. Do not repeat that incorrect test pattern.

### 6.2 Explicitly NOT TESTED or NOT ACCEPTED — do not mark PASS

| Gate | State / warning |
|---|---|
| Six-worker concurrent execution and one-versus-six canonical-byte equality under real Windows | **PENDING**. A local non-Windows surrogate is not Windows acceptance. |
| Six-worker `--plan-termination` ownership inventory with real Windows processes | **PENDING**; next proposed safe test after handover review. |
| Live unrelated-process **decoys** (global Python, project-venv Python, other-venv Python, separate CMD) through safety previews | **PENDING**. No unrelated real process has yet been proved immune to a forced-kill path. |
| Coordinator launcher from initially inactive `.venv` and subsequent parent CMD restoration | **PENDING**, although the **individual** wrapper passed inactive activation/restoration. |
| W-23 package upgrade/compatibility gate | **UNTESTED**; do not confuse with sentinel no-clobber test. |
| Broader W-suite CMD quoting, registry AutoRun, redirected output, argument edge cases, abnormal processes/interrupts, resource guards | **PENDING** unless individually evidenced. |
| Process timeout/actual kill; Ctrl+C with active jobs; memory-guard forced cleanup; D-series destructive tests | **NOT AUTHORISED NOW** with switch False; do not run before N-series decoy tests, independent safety review and explicit owner decision. |
| Comprehensive `P0–P2` closure or scientific/production Option F acceptance | **NOT COMPLETE**. Architecture v0.4 itself is ratified, but code's Windows safety/worker acceptance remains conditional. |
| First real E-method (P3), valid ranking/results, holdout evaluation, predicted efficacy | **NOT IMPLEMENTED**, no inference of predictive power. |

**Additional test-suite warning:** `tests/windows_architecture_poc_suite.py` has an **optional `--with-timeout`** path that expects successful cleanup. Do **not** run it with the owner kill switch False; it may leave a sleeping process alive and cannot pass the asserted cleanup condition. Likewise do not run ad-hoc short timeout, Ctrl+C, or memory-stress commands as substitutes for a deliberate safe test plan.

---

## 7. Next work, in safe order

**First milestone: transfer and review the handback itself.** Deliver this handback and the source ZIP to Claude for independent check of file paths, decision hierarchy, owner commitments, latest safety source, statuses and next gates. Incorporate justified corrections; the owner then ratifies and commits it. Do not silently rewrite already-ratified architecture v0.4 as part of this handover.

**After that handover checkpoint, proposed engineering order:**

1. **Six-worker live ownership preview with kill switch remaining False.** First confirm the owner is using the current ZIP source and no unrelated changes; test six synthetic sleepers with a generous timeout and explicit `--plan-termination`. Record all six worker ancestry trees, BEFORE/AFTER, complete outcome, no anomalous target, no signal/kill, exit code, manifest. Review the output before proceeding. Example *for separately authorised use after review*:

   ```cmd
   call Run_Coordinator.bat --poc --case=sleep-timeout --count=6 --workers=6 --sleep-seconds=12 --timeout-seconds=45 --plan-termination
   echo %ERRORLEVEL%
   ```

   This command does **not request termination**; nevertheless monitor the console and stop/diagnose unexpected memory/admission problems. Do not conflate plan-only success with a later actual-kill test.
2. **Non-destructive real decoy testing (N-series).** Start identifiable unrelated Python/CMD processes in separate consoles; capture both PID **and creation time** before/after; demonstrate none appear on any kill-candidate plan. Independently review forged/missing/wrong-run-ID status and unexpected-name/ancestry tests (synthetic N2–N5 already pass; live decoy coverage is still pending).
3. **Coordinator inactive environment test.** Start from an ordinary inactive CMD using `Run_Coordinator.bat`, let its batch wrapper activate and restore, verify the parent environment unchanged; verify direct Python coordinator launch with inactive `VIRTUAL_ENV` is rejected (not a normal launch route).
4. **Non-destructive concurrency/reproducibility.** Perform the safe portion of `tests/windows_architecture_poc_suite.py` **without `--with-timeout`** only after verifying its current source and the user's environment; obtain 1-vs-6 canonical bytes, failure propagation and live-output evidence. Evaluate the risk of any unexpected cleanup before using additional cases.
5. **Independent safety code review and acceptance plan.** Address any ownership anomalies and the risk of uncaptured descendants; align with ratified §5C and Claude review; refine code through narrow versioned patches, not broad cleanup.
6. **Only upon explicit owner approval**, consider separately controlled destructive timeout, interrupt, and memory-guard tests, with the exact switch operation and target inventories reviewed. Never flip `ENABLE_PROCESS_TERMINATION` to True merely to make an assertion pass or remove an error. Anomalies require safe refusal, not broader kill authority.
7. **P0–P2/W-suite closure and ERR-R2-02 production gate review**; **then** seek distinct P3 method authorization, implementing the validated common method contracts before family batches.

**Do not prematurely update a PASS ledger when a source file merely adds code for the functionality.** Preserve an explicit test-input/expected/observed/status record, with source revision and actual Windows output.

---

## 8. Operational handoff rules and recurring pitfalls

1. **Source fidelity:** Before proposing code changes, read the exact current repository ZIP/working files. Compare SHA-256 and list proposed **ADD/REPLACE/UNCHANGED** paths. Never overwrite `source_data`, `.venv`, ratified `doc`, the history scraper, or user changes without consent and reconciliation. Deliver small ZIP overlays; the owner controls installation and Git commits.
2. **No silent architecture drift:** Launch through common `.bat` runners; direct coordinator Python is not an operational alternate; no backdoor direct `sys.executable` fallback, broad `taskkill`, or Job Object without owner-ratified change. POC case whitelist is not the future scientific E-method registry.
3. **Do not mix evidence domains:** engineering fixtures and checksums are not lottery forecasts; static/source-level tests are not real Windows proof; live plan-only ancestry is not a demonstration of safe actual termination; a stopped parent CMD is not proof the Python process exited.
4. **Safety priority:** owner kills disabled by default; always print BEFORE and AFTER including PID/name/creation time and action outcome; status file cannot appoint kill candidates; uncertain ownership means no kill and a clear suspect-orphan report. No unapproved stress/interrupt/kill experiments.
5. **No fake completeness:** W-23 is the package-upgrade gate and is NOT tested; the same-ID sentinel test belongs to A-17/A-18 and POC-Q08. Do not mark the six-worker Windows gate closed based on local Linux surrogate tests or the latest one-worker PASS.
6. **No dual package authorities:** `install_upgrade_dependencies_into_venv.bat` alone lists user-maintained direct PyPI dependencies. The tracked historical `requirements.txt` remains in source; do not edit/use it as the active dependency contract or delete without owner consent.
7. **Historical-document wording:** Architecture v0.4 contains inherited older “draft” or `taskkill`-fallback discussion; **ratified §5C expressly supersedes conflicting earlier proposals**. Some R1/R2/R3 original headers are still marked draft despite subsequent explicit owner ratification. Document precedence by **approved decision date**, not isolated header text.
8. **Test outputs and secrets:** `transitory_data/` contains generated local output and is generally ignored; do not invent its contents from a source ZIP. Evidence can be copied to a controlled tracked location only after owner selection/sanitization. No source repo ZIP provides a `.venv` binary or full external process tree.
9. **Environment diagnostics:** The pre-existing `deactivate_venv.bat` printed “virtual environment is not active” after deactivation even when it had just successfully removed the prompt; its wording reflects the **post-deactivation** state. It does not, by itself, imply a wrapper failure. Avoid interactive `SETLOCAL`/`ENDLOCAL` isolation advice; use a batch file or separate `cmd /d` process.
10. **Risky partial failures:** With kill switch False, if a timeout/interrupt/critical-memory stop is accidentally requested, some processes may continue running. The coordinator should report inability to confirm cleanup; inspect live PIDs (and creation times) before any manual action. Do not promise the switch controls Windows-originated Ctrl+C signals.

---

## 9. Independent review checklist for Claude and owner

Ask Claude to verify this handback against **both** this GitHub ZIP snapshot and the ratified documents; identify **specific file paths/sections** for corrections:

- Does the hierarchy correctly distinguish ratified documents from the conditional ERR-R2-02 implementation decision?
- Is Option F the single human/coordinated **common batch experiment interface**, with `.venv` activation/restoration assigned to the correct layers?
- Does the process-safety summary match **v0.2 source**, including the global switch, kill authority, live capture, status-only-as-evidence, allowed transient executables and fail-safe reporting?
- Are all **PASS** claims supported by the owner's Windows transcripts? Is anything wrongly marked PASS, particularly live decoys, 1-vs-6, P2, W-23, Ctrl+C or actual termination?
- Are source-data draw counts/ranges and the 10-draw holdout represented accurately? Is synthetic-vs-real separation uncompromised?
- Are the next proposed commands *strictly non-destructive* under the actual code and owner safety settings, with caveats for timeouts and external Ctrl+C?
- Are there any overlooked mismatches between **current source** and safety-review v2, or important unfinished gates that a new chat must know before touching the coordinator?

**Approval gate:** This is **v0.1 REVIEW CANDIDATE**. After Claude's review and the owner's ratification, install it at the intended repository path in the opening document metadata and commit it deliberately. The owner need not extract any source-code patch to review this handback. All existing project files remain unchanged by preparing this document.

---

## 10. Short restart checklist (for the next ChatGPT)

- [ ] Have the newest source ZIP **and** this handback; note actual ZIP hash and available Git commit.
- [ ] Read **ratified** Proposal v0.3, R1 v0.4, R2 v0.3 + approved erratum v0.2, R3 v0.2, Architecture v0.4 §5C, P0–P2 task spec.
- [ ] Inspect `Run_Experiment.bat`, `Run_Coordinator.bat`, `src/Powerball_Experiment_Coordinator.py`, owner-switch setting, probes and tests.
- [ ] Know **P0 wrapper PASS**, **P1 one-worker PASS**, **P1/P2 v0.2 one-worker ancestry preview PASS**, **six-worker/destructive/real-decoy gates PENDING**.
- [ ] Keep `ENABLE_PROCESS_TERMINATION = False` and never falsely report process cleanup as verified.
- [ ] Do not change source or start new tests until owner approves the immediate next step.
- [ ] Verify future code patches only against the user's current source, review with Claude when safety/scientific contracts are material, and require owner ratification for architectural changes.

**END — v0.1 REVIEW CANDIDATE; no P2/Option F production acceptance implied.**
