# Claude reviewer handover - Predictive Randomness project

**Handover version:** v2 (v2 adds: ChatGPT handback v0.2 and its review outcome, the snapshot identity, the one-worker live preview result, the smoke-suite watchdog finding)
**As at:** 23 October 2026, 14:45 Adelaide time (UTC+10:30)
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality` (public GitHub); last inspected via the owner's snapshot `analysing_perceived_randomness_in_reality-main(4).zip` (SHA-256 `77cfd287e5d444c3eae426392c8dccc4e5cc188d1e1e5faa2e7b4ce067105b06`; GitHub archive comment `6b527627f7f98fd5cd88f4bea76e16b9cb56d372`; 45 regular files; no `.git`)
**Purpose:** continuity document for a follow-on Claude chat acting as **independent reviewer**. It records the current rules, decisions (including undocumented ones), status, verified technical facts, the review method that has worked, and open items, so the next chat only has to work out what has changed since this date.
**Authority:** the repository documents prevail over this handover wherever they conflict. This is a summary that points to them; it never replaces them.

---

## 1. Roles and workflow

- **Project owner** (GitHub `hydra3333`): sole decision-maker and committer; runs all Windows tests on their own PC; ratifies documents. Never name the owner in anything that may be committed to GitHub; write "the project owner" or "hydra3333".
- **ChatGPT:** principal author of specifications and code. Produces versioned documents, source packages (repository-relative ZIP overlays) and handback notes.
- **Claude (you):** independent reviewer. Reviews documents and code for substantive errors, conformance with the ratified set, safety and scientific integrity. Claude does not implement code unless asked. Earlier chats also produced research responses and some review documents that the owner committed to the repository.
- **Flow:** ChatGPT drafts -> owner relays to Claude -> Claude reviews -> owner relays Claude's findings to ChatGPT -> ChatGPT revises -> owner ratifies. The owner relays Claude's output by copy-paste.

---

## 2. How the owner wants work presented (follow strictly)

- **End every review with a short paste-ready block** (a ```text fenced block) summarising findings for ChatGPT. The owner likes these small pastes.
- **Separate blockers from optional improvements.** Concentrate on substantive errors, not cosmetic wording. Do not reopen settled decisions without a substantive technical reason.
- **Decisions:** present as plain-English question / why / recommendation / options, with document references on a trailing line only.
- **Verify, don't assert.** The owner distrusts assertion: check claims against the actual files, line numbers, library source or official documentation. Label evidence where useful (documented / source / observed / to be tested).
- **Plain English** rather than acronym-dense wording.
- **Files Claude produces:** strict US-ASCII and CRLF line endings, mechanically verified after writing. Filenames carry their version (`..._v1.md`, `..._v2.md`). A mention of a versioned document means "that version or later", except in records of past events.
- **Superseded versions** are kept in the repository, not overwritten. The owner dislikes make-work revisions done only to update version mentions.
- **Process discipline:** propose before transforming; the owner ratifies.
- **Owner's philosophy (binding on the project):** the experiment deliberately challenges "perceived reality". No method may be excluded or ranked down because conventional statistics says it cannot work. The fair-draw reference model is a measuring ruler, never a veto. Real prospective predictions against actual draws are what count. Claude has honoured this by giving reference figures as context only, never as dismissals.

---

## 3. Project in one paragraph

Australian Powerball (current format since **Draw 1144, 19 April 2018**: 7 distinct main numbers from 1-35, plus 1 Powerball from 1-20). The project builds a Python 3.14 research system on Windows 11 to test whether past draws contain any predictive structure, using 62 permanently registered experimental methods (E_1-E_62, room up to E_106). Every method produces full rankings; for each target it publishes a TOP prediction and a WORST (inverse) prediction side by side. After each real draw, each forecast is scored by TOP matches, WORST matches and an additional rank-position measure. Real weekly forecasts start only after modelling is complete: train on 1144..L, predict L+1, freeze and push before the draw, compare afterwards, append the draw, repeat.

---

## 4. Ratified and approved documents (all in `doc/`)

| Document | Status | Key content |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_3.md` | Ratified | Charter, philosophy, rules A-01..A-37 |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | Ratified | 62 methods E_1-E_62 (families below); drawn-order provenance |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` | Ratified | N-1 rule, FINAL L+1, holdout, TOP/WORST, seeds, 1-12 workers (see erratum), tests T-01..T-39 |
| `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` | Owner-approved | ERR-R2-01: 1-vs-configured-maximum (6) worker identity; ERR-R2-02: Option F **provisional pending Windows tests**; ERR-R2-03: dependency `.bat` sole authority plus generated snapshots; ERR-R2-04: `selection_model_version` = fitting model only |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_2.md` | Ratified | TOP/WORST/rank-position scoring; `TIE_SHA256_V1` label-neutral tie order; reference figures; prospective batch protocol |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_4.md` | Ratified 23 Oct 2026 | Architecture 2 + Option F; section 5C: mandatory launch interfaces and verified process ownership |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_1.md` | Ratified for P0-P2 | POC phases, W-01..W-25, A-01..A-26 mapping, evidence package |

Superseded but retained: R3 v0.1; Architecture v0.2 and v0.3.

R1 method families: E_1-E_6 originals; E_7-E_16 frequency/Bayesian/regime; E_17-E_22 recurrence; E_23-E_32 within-draw and drawn order; E_33-E_40 spectral/curve; E_41-E_48 information/nonlinear; E_49-E_54 machine learning/external; E_55-E_56 ensembles; E_57-E_62 pilot-wave-inspired (E_57 DPP; E_58/E_59 latent wave; E_60 relaxation; E_61/E_62 guided-particle circulation).

---

## 5. Settled decisions - do not reopen without substantive cause

**Data**
- Dataset: 444 draws (1144-1587) in two CSVs, an unordered set and the **operator-labelled drawn order**. The order was confirmed by The Lott's "Drawn | Numerical" toggle (Draw 1587) and the operator's 2021 "Winning Numbers (drawn order)" PDF (Draw 1297). Both are views of the same draws, never counted as independent.
- Holdout: Draws **1578-1587**, sealed for development and benchmarks; it is not withheld from FINAL forecasts.
- No pre-2018 draws, including for Powerball-only analysis (owner rejected the earlier suggestion).

**Scientific contract**
- Strict N-1 history for historical targets.
- Seeds and content identity derive from the **permitted training-view digest**, never the whole-file hash. The mandatory perturbation test (change draw N and everything after it; the forecast for N must stay byte-identical) is T-05.
- **TOP and WORST from one frozen ranking.** WORST = the last seven / last one positions of the frozen ranking (equivalently, the first of its exact reversal). Native joint-set TOP (for example MAP) is preserved; its WORST comes from marginals (`INVERSE_FROM_MARGINALS`); otherwise `INVERSE_UNAVAILABLE`, never fabricated.
- **Rank position** = mean mid-rank of the 7 drawn numbers (chance 18.0, standard deviation about 3.46) and the Powerball's rank (chance 10.5, standard deviation about 5.77). It is evaluation only and never influences predictions. It is reported **in addition to** TOP and WORST, at the owner's explicit request.
- **Ties:** `TIE_SHA256_V1`, a hash of (training-view digest, target, method, variant, barrel, readout version, label). Measured on training data: E_1 count ties decide 7th/8th place in 63% of targets and the Powerball top place in 14%, so an ascending-label rule would have biased TOP towards low numbers and WORST towards high ones.
- **Weekly FINAL batch:** every runnable method and variant (TOP and WORST), with statuses, committed and pushed before the draw. Nothing may be added afterwards. Each method and selection rule has its own track. Any reported hit is shown with its reference chance rate as context only, never as a dismissal.
- Real forecasting starts after modelling is finished (the owner's choice). The scoring measures must be fixed before the first real forecast (T-39).
- **Synthetic firewall:** synthetic null and planted-effect studies may inform disclosed design. Synthetic data, states and scores never enter real fits, predictions or scores, and a synthetic diagnostic never excludes a method.

**Engineering**
- **Architecture 2:** one standalone `.py` per E-method in `src/methods/` (`E_###_name.py`), shared `_common/` helpers, and a small coordinator.
- **Option F is the single launch interface.** Coordinated runs go `Run_Coordinator.bat` -> Python coordinator -> **`Run_Experiment.bat` for every experiment** -> method `.py`. Manual runs go `Run_Experiment.bat` -> method. There is no second production launcher, and direct `sys.executable` launch is only an architecture-change proposal requiring an owner decision.
- **Wrappers:** the owner insisted they keep explicit venv checks, scoped `CALL` activation when inactive, `SETLOCAL`/`ENDLOCAL` restoration, the explicit `.venv\Scripts\python.exe`, and forwarding via `%*`. The coordinator refuses to start unless both `VIRTUAL_ENV` and `sys.prefix` match the project `.venv`, so child wrappers verify rather than activate.
- **Concurrency:** 1-6 workers, default 6; one numerical thread per worker; no nested parallelism.
- **Dependencies:** `install_upgrade_dependencies_into_venv.bat` is the sole human-maintained package list (modes VERIFY default / INSTALL / UPGRADE); `requirements.txt` is historical and non-authoritative. Installed on the owner's PC: psutil 7.2.2, NumPy 2.5.4, SciPy 1.18.1, threadpoolctl 3.7.0; Python 3.14.8.
- **Process termination (Architecture v0.4 section 5C):** psutil only; **no Windows Job Objects** (the owner objects to extra Windows machinery); **no `taskkill` fallback**. Ownership is proved by ancestry captured while the wrapper root is alive. Kill only retained `psutil.Process` members, and the root via its `Popen` handle. The status file is evidence only. When uncertain, leave the process running and report `UNVERIFIED` / `ORPHAN_SUSPECTED`. Experiments may not start child processes in the first release.
- **Owner's safety switch:** `ENABLE_PROCESS_TERMINATION = False` in the coordinator source, with no command-line override. Only the owner flips it, after non-destructive tests.
- **Testing order:** non-destructive tests first (decoy processes, plan-only mode, forged status); destructive tests one at a time afterwards.
- **Batched implementation (agreed in principle; held until verifications finish):** pilot E_1-E_6 one at a time, then batch by R1 family with one "lead method" verified first; an automatic contract-test harness; verifiers derive expected results from the specification, not the code; heavy methods (E_12, E_38, E_52, E_53, E_57-E_62) individually; ensembles last.

---

## 6. Verified technical facts (sources were checked; reuse rather than re-derive)

- **Windows venv `python.exe` is a redirector** (CPython `PC/venvlauncher.c`). It starts the real interpreter as a second process, passes the command line, inherits stdio, returns the exit code, places the child in a kill-on-close job with silent breakaway, and ignores Ctrl+C. Consequently `Popen.pid` is not the interpreter's PID. This is an implementation detail, never relied on.
- **Windows does not kill children when the parent dies** (Microsoft, "Terminating a Process"), and `TerminateProcess` is asynchronous.
- **Python on batch files:** a `.bat` launched via `Popen` (even with `shell=False`) runs under `cmd.exe`, and arguments are parsed by CMD without Python escaping (subprocess docs; gh-114539). The coordinator therefore restricts argument characters (`SAFE_ARG` regex).
- **`cmd /C` quote stripping:** quotes are kept only in narrow cases; otherwise the first and last quote are stripped (Microsoft `cmd` docs). That is why `/D /C` was withdrawn and AutoRun is checked in the registry instead.
- **CMD `%1` parsing splits at `= , ;`.** Never rebuild arguments from `%1..%9`; `%*` keeps the raw text.
- **CPython 3.14 `activate.bat`** runs `chcp.com`, via `for /f` (a child `cmd.exe`) and directly. Under the coordinator, children inherit `VIRTUAL_ENV`, so no activation and no `chcp`.
- **Current `Run_Experiment.bat` tree:** root `cmd.exe`; `set SCRIPT_NAME | findstr.exe ...`, where a pipe makes a child `cmd.exe` plus `findstr.exe`; a pre-check `"%PY%" -c ...` (transient redirector plus interpreter `python.exe`); then the experiment's redirector and interpreter `python.exe`. Coordinator allow-list: `cmd.exe`, `findstr.exe`, `python.exe`.
- **psutil 7.2.2 (source read):** `children(recursive=True)` filters by creation time against the **root only** (lines 995-1029), hence the project's per-edge check. `kill()` / `terminate()` on Windows call `_raise_if_pid_reused()`, which compares PID + creation time, so stored objects refuse reused PIDs. `wait_procs` returns (gone, alive). The peak-memory field is `peak_wset` in 7.x and `peak_rss` in the 8.0 docs (the helper handles both).
- **`os.rename` on Windows** raises `FileExistsError` if the destination exists; the project uses it for no-clobber publishing. `os.replace` overwrites and must not be used for frozen results.

**Reference figures (fair-draw model, context only):**
- Main matches: mean 1.4, standard deviation 0.9604. P(at least 4) = 0.01826 (about 1 in 55); P(at least 5) = 0.00121 (about 1 in 827).
- Powerball: 0.05 per draw.
- Chance hits per weekly batch (independence assumed, an overestimate where methods are correlated):

| Batch | Some 4+ main hit | Some 5+ main hit | Powerball hits per week |
|---|---|---|---|
| 62 forecasts | about 68% of weeks | about 1 week in 14 | about 3.1 |
| 124 forecasts (TOP + WORST) | about 90% of weeks | about 1 week in 7 | about 6.2 |

---

## 7. Current implementation status (as at this handover)

**P0 (standalone), passed on Windows:**
- venv activation; Python 3.14.8 verified;
- static checks;
- dependency installer INSTALL and VERIFY;
- `Run_Experiment.bat` argument forwarding (including quoted parameters) and venv thread settings;
- canonical fixture digest;
- exit code 3 propagation;
- **W-11** (hard exit 7 through the wrapper, standalone half only; the coordinator half is pending in P2);
- **A-17/A-18 / POC-Q08 single-run collision** (`FileExistsError`; original file's hash unchanged). This was originally mislabelled W-23. **W-23 (upgrade gate) has not been run.** Concurrent collision is untested.

**P1:** one-worker coordinator run through `Run_Experiment.bat` passed (canonical digest matched the standalone run).

**P1/P2 one-worker live ownership preview (patch v0.2, switch False): PASS (non-destructive only).** `--case=sleep-timeout --count=1 --workers=1 --sleep-seconds=12 --timeout-seconds=45 --plan-termination` gave:
- root `cmd.exe` (PID 26116);
- descendants `python.exe` at depth 1 (PID 27848) and depth 2 (PID 26768), i.e. the redirector and the interpreter;
- `experiment_matched=True`, no anomalies, no signals sent, worker SUCCESS, exit 0.

The transient `findstr.exe` and pre-check `python.exe` were not captured (expected at a 0.5 s capture interval). This certifies no kill behaviour.

**P1/P2 coordinator ownership-safety patch v0.2:** committed, switch False. Static and synthetic checks passed, plus the one-worker live preview above. **Pending:** the six-worker preview, the decoy and forged-status tests, and then (after owner review and the switch flip) the destructive tests D-1..D-6.

**Option F / ERR-R2-02:** still provisional. **P3** (first real E-method, probably E_1) is not authorised yet.

No E-method has been implemented. No real-data predictions have been made. The holdout is sealed.

---

## 8. Open review findings at handover (patch v0.2, `src/Powerball_Experiment_Coordinator.py`)

Raised in the 23 October Claude review of the patch. Check whether later versions resolved them.

1. **PID reuse within one experiment's own tree causes a false refusal** (`capture_owned_tree`, lines 254-258). Windows reuses PIDs quickly. If the wrapper's transient pre-check `python.exe` exits and its PID is reused by the experiment's redirector or interpreter, the code records `MEMBER_PID_REUSED`. Any ownership error then blocks termination of the whole worker, and the experiment is never matched. Fix: when the stored member is confirmed gone, treat the new process as a fresh candidate (move the old record to a "departed" list). Flag an error only if the old member was still believed alive.
2. **No wait for killed members before the survivor check** (`terminate_owned_tree`, lines 357-364). `TerminateProcess` is asynchronous, and v0.2 waits only on the root. Add `psutil.wait_procs` over the killed members, with a bounded timeout, before computing survivors. Otherwise false `ORPHAN_SUSPECTED` results are likely in the destructive tests.
3. **Owner decision: a hung experiment with no status file is never terminated** (lines 322-334 refuse unless the experiment was matched through status). A process with verified ancestry is owned even without a status match. Recommendation: allow the kill of verified members and report `UNVERIFIED` rather than `STOPPED_CONFIRMED`. The owner may prefer the current stricter rule.
4. **Transient anomalies permanently block termination.** Any entry in `ownership_errors` refuses the kill. Consider separating hard anomalies (unexpected executable, child older than parent) from benign vanished-process races. This is lower priority because the analysis found few realistic races in the current tree.
5. **The smoke suite has its own kill path.** `tests/windows_architecture_poc_suite.py`'s `run()` (lines 24-28) uses `subprocess.run(..., timeout=120)`. On expiry, Python kills the launched `Run_Coordinator.bat` `cmd.exe` by handle, bypassing `ENABLE_PROCESS_TERMINATION`. It can't reach unrelated processes, but it can orphan the coordinator and its workers. So the default run (without `--with-timeout`) is not strictly kill-free.
6. **A useful near-non-destructive test:** with the switch False, a console Ctrl+C reaches only that console's processes (coordinator and its children; decoys run in separate windows). It therefore shows W-10/W-18 behaviour, including any hanging "Terminate batch job (Y/N)?" prompt, without the coordinator killing anything.

**Handback status:** ChatGPT's own continuation handback was reviewed. v0.1 had three corrections, C1-C3:
- C1 = item 3 above (the current code refuses all kills unless the experiment is matched);
- C2 = items 1-2 (the two defects), plus a note that a `MEMBER_PID_REUSED` anomaly in the six-worker preview most likely reflects defect 1, and that group PASS ignores ownership anomalies;
- C3 = item 5 (the smoke-suite watchdog).

`Predictive_Randomness_ChatGPT_Continuation_Handback_v0_2_REVIEW_CANDIDATE.md` incorporates all three accurately (Claude checked its diff against v0.1 and the cited line numbers). It awaits owner ratification, then is to be committed under `doc/HANDOVER/`. **Item 3 is an open owner decision.** The handback records it as unresolved, to be decided after the handback is ratified.

Housekeeping (not blockers): the patch ZIP and handback documents were committed at the repository root. The owner may want them under `review/` or similar.

---

## 9. Review method that has worked

- Unpack every ZIP into its own fresh scratch directory. Diff new versions against old ones (`diff <(sed 's/\r$//' old) <(sed 's/\r$//' new)`).
- Check the claims in handback documents against the actual files: line endings (CRLF), hashes, file lists, `.gitignore` contents.
- Cross-check against the ratified set, and quote line numbers.
- Recompute any statistics with a short Python script rather than trusting them.
- Read library source (for example via `pip download --no-binary`) when behaviour matters. Use official Microsoft and Python documentation for Windows behaviour. Cite sources at the end.
- For the owner's Windows-only behaviour, label the expectation **TO-TEST** and map it to a W-, A- or N-series test.
- Produce longer reviews as versioned `.md` files (ASCII, CRLF; verify mechanically), send them, and give a short summary plus the paste block in chat.

---

## 10. Likely next items

1. Review the Windows evidence from the six-worker plan-only preview and the decoy tests. Review the patch fixing the two section 8 defects, and the owner's decision on item 3, before any switch flip.
2. Review the destructive-test evidence (D-1..D-6, Ctrl+C, memory guard), then the P2 closure and ERR-R2-02 disposition.
3. Review the P3 task (E_1 first real method): contract harness, N-1 perturbation test, `TIE_SHA256_V1`, TOP/WORST, canonical forecast schema, fixture with expected values from the specification.
4. Review the batched family plans and the `FORMULA_OPEN` mathematics specifications as they arrive.

*End of handover.*
