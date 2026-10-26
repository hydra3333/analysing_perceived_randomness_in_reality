# Claude reviewer handover - Predictive Randomness project

**Handover version:** v5 (v5 adds: coordinator v0.5 and v0.6 reviews (v0.6 accepted for non-destructive Windows testing); the owner-reported Windows v0.6 results; the real timeout/orphan incident, its archive and the pending marker clearance; Claude's review of ChatGPT handback v0.3 and of the incident utilities; the strict rule and manual clearance recorded as owner-ratified. v4 added: the strict no-status/no-kill rule now DECIDED; the inactive-CMD activation and decoy-test passes; the readiness review; the coordinator v0.4 orphan-interlock review and its blocker B1. v3 added: the standing review procedure agreed on 23 Oct; coordinator v0.3 review; the six-worker preview result. v2 added: ChatGPT handback v0.2, the snapshot identity, the one-worker preview, the smoke-suite watchdog)
**As at:** 23 October 2026, 21:10 Adelaide time (UTC+10:30). **First action in a new chat: ask the owner whether the real orphan marker (section 7) has since been cleared.**
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality` (public GitHub); last inspected by Claude by cloning GitHub HEAD `7254fc9c8351be1255981df987f2605ff7565f90` (23 Oct 16:05; coordinator still v0.3 `a2402175...`; contains Claude handovers v2 and v3 under `doc/HANDOVER/`). Earlier snapshot `analysing_perceived_randomness_in_reality-main(4).zip` (SHA-256 `77cfd287...5b06`) held coordinator v0.2. The owner's Windows working tree now runs v0.6 (not yet committed, as far as Claude knows)
**Purpose:** continuity document for a follow-on Claude chat acting as **independent reviewer**. It records the current rules, decisions (including undocumented ones), status, verified technical facts, the review method that has worked, and open items, so the next chat only has to work out what has changed since this date.
**Authority:** the repository documents prevail over this handover wherever they conflict. This is a summary that points to them; it never replaces them.

---

## 1. Roles and workflow

- **Project owner** (GitHub `hydra3333`): sole decision-maker and committer; runs all Windows tests on their own PC; ratifies documents. Never name the owner in anything that may be committed to GitHub; write "the project owner" or "hydra3333".
- **ChatGPT:** principal author of specifications and code. Produces versioned documents, source packages (repository-relative ZIP overlays) and handback notes.
- **Claude (you):** independent reviewer. Reviews documents and code for substantive errors, conformance with the ratified set, safety and scientific integrity. Claude does not implement code unless asked. Earlier chats also produced research responses and some review documents that the owner committed to the repository.
- **Flow:** ChatGPT drafts -> owner relays to Claude -> Claude reviews -> owner relays Claude's findings to ChatGPT -> ChatGPT revises -> owner ratifies. The owner relays Claude's output by copy-paste.
- **Standing procedure (agreed 23 Oct 2026, to reduce administration):**
  - ChatGPT makes routine implementation decisions itself within the ratified specifications. It labels items DECIDED (made within its authority), RECOMMENDED (consequential; awaiting owner approval) or OPEN (needs evidence or review).
  - Claude reviews are bundled at meaningful milestones, **except** that these areas always get independent Claude review before consequential execution or acceptance:
    - process termination (kill logic, ownership verification, safety switch);
    - N-1 training boundaries and leakage;
    - fit seeds and canonical forecast identity;
    - TOP/WORST readout, ties and selection rules;
    - holdout access and unsealing;
    - FINAL freezing, persistence and publication;
    - the synthetic/real firewall;
    - dependency upgrades (W-23 gate).
  - For termination changes, static and synthetic checks may proceed with termination disabled. Review plus owner approval are needed before enabling or exercising real termination.
  - **Review packages contain:** the exact diff against an identified committed baseline; SHA-256 of new or changed files; a short handback with test evidence; and the DECIDED / RECOMMENDED / OPEN record.
  - **Claude's added duty:** check the DECIDED list and flag anything that should have been RECOMMENDED to the owner instead.

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

**Coordinator lineage** (all with `ENABLE_PROCESS_TERMINATION = False`; the kill path `terminate_owned_tree` is code-identical from v0.3 to v0.6; only the two original kill calls exist):

| Version | SHA-256 | Claude verdict |
|---|---|---|
| v0.2 | `26c471e1...` | superseded (two defects, section 8) |
| v0.3 | `a2402175eaf22bf9d0293b49a6d1c91b48fe20d26866cf5d096dcfae6a95a58b` | approved for non-destructive checks; committed baseline (GitHub HEAD 7254fc9) |
| v0.4 | `b3a15a15...25d1c7` | NOT APPROVED - B1: no marker when an orphan is seen at natural/failed wrapper exit |
| v0.5 | `a05a32d7...6bf1` | NOT APPROVED - B2: status-file PID checked only on fully successful runs, and only after the scheduling loop |
| **v0.6** | **`2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`** | **ACCEPTED for non-destructive Windows install and testing only** (23 Oct). Installed on the owner's Windows tree. |

**v0.6 interlock design (what a reviewer must preserve):**
- Marker `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json` (schema `ENGINEERING_UNRESOLVED_ORPHAN_V1`), written once with fsync and no overwrite (Windows `os.rename` no-clobber). Any existing entry - file, folder, symlink, garbled - blocks every later coordinator start with a flushed `[SAFETY STOP]` banner and exit 2. No CLI bypass, no automatic acknowledgement.
- On every observed wrapper exit (any exit code), before further launches: check every captured member with `_member_alive`, and check the run-ID-matched status-file PID with `same_process(pid, create_time)`. Alive or unknown (including a missing creation time) -> ORPHAN_SUSPECTED, marker, `stop_launches`; remaining workers finish naturally. A post-loop re-check catches late status files. **Status-file PIDs only ever block; they are never kill targets.**
- Marker-write failure -> CRITICAL banner and `marker_write_failed` in the manifest (accepted residual: then future starts are not blocked).
- With the switch False, every timeout or Ctrl+C writes a marker (expected).
- Accepted residual: wrapper exits before anything is captured AND no usable status file -> no evidence.
- **Open optional items (to go in the next reviewed safety patch, before the destructive gate):** O1 post-loop re-check overwrites the issue/state of already-stopped workers and repeats the banner; O2 a huge-integer creation time in a corrupt status file raises `OverflowError` in `math.isfinite` (main loop: caught, marker written; post-loop: escapes, no manifest); O3 handback wording (capture_owned_tree has the v0.4 `is True` change); O4 fake-driven main-loop test of stop_launches and manifest flags; O5 handback .md lands at repo root.

**Windows evidence (owner-reported via ChatGPT; Claude has not seen the transcripts):**
- P0 standalone batch/venv cases PASS (W-23 not run). v0.3: one- and six-worker plan-only previews PASS; automated 3-decoy test PASS (utility pinned to v0.3).
- v0.6: the seven check scripts PASS; one-worker (group `coord-a9ea0b92...`) and six-worker (`coord-d1092829...`) plan-only previews PASS with **no marker** (false-positive check passed); direct `python` coordinator launch with VIRTUAL_ENV unset refused (exit 2); `Run_Coordinator.bat` from an inactive CMD PASS and environment restored; `chcp` 65001 before and after; dummy-marker gate test PASS (refusal, banner, exit 2; dummy archived, SHA `665ed6c4...`, then removed). Not yet evidenced: direct `python` with a *mismatched* VIRTUAL_ENV.
- **Real-marker rehearsal (owner-chosen, non-destructive):** `--case=sleep-timeout --sleep-seconds=60 --timeout-seconds=10`, switch False. Ancestry matched, no signals sent, real marker written, coordinator exit 1; a second banner came from the stuck-reader path (the orphaned experiment still held the pipe) - expected, not O1. A later launch was refused (exit 2). The experiment ran on, finished its sleep, published `canonical_result.json`, then failed its final console write with `OSError: [Errno 22] Invalid argument` (writing to the closed pipe, most likely) - status FAILED, must stay FAILED.

**REAL INCIDENT - marker ACTIVE at this handover (check current state first):**
- Group `coord-2a42fac2c24549b5b216ffa691f225a7`, run `..._w001`; marker SHA-256 `2d8269eb3845cf17ce7124254f1f9397ae52a1dd5603a0aeb67bdda05453a2aa`.
- Identities (PID / creation time): root `cmd.exe` 31720 / 1792749106.972062; `python.exe` 17432 / 1792749107.0698512; experiment `python.exe` 25212 / 1792749107.0771797 (also the status PID). Owner reports all gone, checked twice.
- Evidence archived to `results/architecture_poc/20261023_timeout_no_kill_coord-2a42fac2/` (7 files plus `archive_record.json`; ARCHIVE PASS, exit 0). The coordinator console transcript is not in the archive; the owner should save it separately.
- Incident utilities (one-incident only, hard-pinned; never reuse for another incident): read-only inspector `606f5e22...` (ran; HOLD only because it also demanded probe SUCCESS); archiver `ca42d264...` (ran; copies with `xb`, never touches the marker); **clearance utility `P1P2_Clear_Archived_Real_Orphan_v0_1.py` `08000be1...` - NOT YET RUN.** Claude reviewed it and simulated it on Linux: `--check` is read-only; `--clear-confirmed` re-runs every pinned check (coordinator v0.6 hash, marker hash and contents, archive hashes, byte-identical archived marker, FAILED status, all four identities gone by PID + creation time; any uncertainty -> HOLD), writes `manual_clearance_record.json` with `xb` + fsync, then unlinks only that exact marker. No kill calls anywhere. A tampered archive gave HOLD with the marker intact. After clearance, `--check` returns HOLD (marker absent) - expected, not an alarm.
- Owner's next steps: `--check` (expect CHECK PASS, exit 0) -> owner decision -> `--clear-confirmed` -> confirm marker absent and record present -> one ordinary canonical-fixture run with no marker.

**Not done / not authorised:** any real termination (switch on), Ctrl+C test, memory stress, W-23, decoy test on v0.6 (utility must be re-pinned to `2e23d550...` and reviewed first). P3 (first real E-method) not authorised. No E-method implemented, no real-data predictions, holdout sealed.

**ChatGPT handback v0.3 (emergency checkpoint, reviewed by Claude 23 Oct; awaiting owner ratification, then `doc/HANDOVER/` without `_REVIEW_CANDIDATE`):** accurate and safe - no implied clearance, no invitation to run experiments before clearance, FAILED status kept FAILED. Claude's corrections (not blockers): C1 Claude handover v3 is already committed (not only v2); C2 the always-independent-review list should include the synthetic/real firewall and canonical forecast identity explicitly, matching section 1; C3 the second banner in the rehearsal was the stuck-reader path, not O1; C4 v0.3 drops v0.2's P3 roadmap (E_1-E_6 one by one, family batches, FORMULA_OPEN ratified per family, extra-review list, automatic method contracts) - state that v0.2's roadmap remains current or copy it in; C5 note that `--check` after a successful clearance returns HOLD. Safe to defer: a timed-out run published a late `canonical_result.json` - later tooling must never consume results from a group whose manifest is FAIL or orphan-suspected.

---

## 8. Review findings on the coordinator (v0.2, and their v0.3 resolution)

**v0.3 status:** items 1 and 2 are **FIXED in v0.3** and verified by Claude.
- **Item 1:** confirmed-gone members are retired to `departed_members`, and the newcomer is re-verified from scratch; an alive or unverifiable old identity gives `MEMBER_PID_IDENTITY_CONFLICT` (fail closed).
- **Item 2:** a bounded 3 s `wait_procs` on processes actually told to stop; any wait error fails closed.

Open notes from the v0.3 review (optional, not blockers):
- (a) psutil 7.2.2 `Process.wait()` on Windows waits by PID with no reuse check, so the logged `alive=` count can overstate. The confirmed/orphan decision correctly uses identity-checked survivors; better to log the survivors.
- (b) Build the verified-parent list from members with `_member_alive(m) is True` rather than "is not False". This was pre-existing, and the refusal gate prevents any kill impact.

Items 3-6 below remain as written, except item 3: **RATIFIED - the owner retained the stricter rule** (no termination unless the experiment's identity is positively verified against its status file and verified ancestry). Recorded as owner-ratified on 23 Oct in ChatGPT handbacks relayed by the owner, together with the **owner-approved manual marker clearance** (inspect PID + creation time; never kill by hand; escalate anything alive or uncertain; archive original bytes, SHA-256 and logs; then remove the exact marker; no CLI bypass). Do not reopen either.

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

`Predictive_Randomness_ChatGPT_Continuation_Handback_v0_2_REVIEW_CANDIDATE.md` incorporates all three accurately (Claude checked its diff against v0.1 and the cited line numbers). v0.2 was later owner-ratified (SHA-256 `53b33b6d...8140`) and is kept as history; the current ChatGPT handback is the v0.3 candidate (section 7). Item 3 has since been ratified (see above).

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

1. Confirm the real marker's state (section 7). If the owner ran the clearance utility, check its console output and the clearance record against the pinned values.
2. Review the next reviewed safety patch (v0.7?): O1, O2, O4, and the decoy-utility re-pin to the v0.6 (or successor) hash. Then the destructive-gate package: the written switch-on procedure on an exact test copy (one-line switch diff, before/after hashes, forced revert), kill-target inventories, decoys, archived console + manifest + environment + pip freeze + HEAD. **Never authorise destructive tests in a review; that is the owner's step.**
3. Review the destructive-test evidence (D-1..D-6, Ctrl+C, memory guard), then the P2 closure and ERR-R2-02 disposition.
4. Review the P3 task (E_1 first real method): contract harness, N-1 perturbation test, `TIE_SHA256_V1`, TOP/WORST, canonical forecast schema, fixture with expected values from the specification. Real methods should publish STARTED status as early as possible.
5. Review the batched family plans and the `FORMULA_OPEN` mathematics specifications as they arrive.

*End of handover.*
