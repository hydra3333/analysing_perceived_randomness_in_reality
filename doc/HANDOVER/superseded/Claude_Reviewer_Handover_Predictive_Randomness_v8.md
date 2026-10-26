# Claude reviewer handover - Predictive Randomness project

**Handover version:** v8 (v8 adds: Package 2 v0.9 and v0.10-r1 reviews; the owner's timing decisions (human-speed polling); the source change to Lotterywest's own results-search page read by honest headless Selenium, with The Lott as a private hand-saved verifier only; Claude-written owner-run tools `two_site_results_check_v0_7.py` and `results_master_v0_1.py` with `Run_Results_Updater.bat`; the verified development history for both games; the one-master-per-game design with ledger, backups and grabs; the proposed month-aligned holdout boundary (Powerball >= 1577, Oz >= 1694, dates >= 2026-08-01). Earlier versions: see v7 in `doc/HANDOVER/`.)
**As at:** 25 October 2026, afternoon, Adelaide time (UTC+10:30). First action in a new chat: pull GitHub, then ask the owner whether the masters were initialised and committed, and where ChatGPT is with Package 2 v0.11.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality` (public GitHub; https://github.com/hydra3333/analysing_perceived_randomness_in_reality). Claude clones it directly to verify commits. Last seen HEAD `995920d` (25 Oct, commits `src/two_site_results_check_v0_7.py`). Coordinator still v0.6 `2e23d550...`. Git stores `.md`/`.py` as LF; `.bat` is `text eol=crlf`; old CSVs are stored with CRLF. Claude in Chrome is installed on the owner's PC.
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
  - **Claude's own authority (owner, 23 Oct):** the same rule applies to Claude. Claude settles routine review matters itself and labels them reviewer-DECIDED: deferrability, document packaging/versioning, wording, whether a re-review is needed, test-policy choices, and confirmations the owner has already relayed (do not re-ask). Only consequential items go to the owner: new rules or scope, anything that weakens safety, switch-on/destructive tests, ratifications, real-data gates, anything irreversible.

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

Australian Powerball (current format since **Draw 1144, 19 April 2018**: 7 distinct main numbers from 1-35, plus 1 Powerball from 1-20) and, since the 24 Oct multi-game ratification, Oz Lotto (current era since **Draw 1474, 17 May 2022**: 7 of 1-47; supplementaries not used in science). Games are never pooled; each run is one game. The project builds a Python 3.14 research system on Windows 11 to test whether past draws contain any predictive structure, using 62 permanently registered experimental methods (E_1-E_62, room up to E_106). Every method produces full rankings; for each target it publishes a TOP prediction and a WORST (inverse) prediction side by side. After each real draw, each forecast is scored by TOP matches, WORST matches and an additional rank-position measure. Real weekly forecasts start only after modelling is complete: train on 1144..L, predict L+1, freeze and push before the draw, compare afterwards, append the draw, repeat.

---

## 4. Ratified and approved documents (all in `doc/`; see `doc/RATIFICATION_REGISTER_v0_2.md` for hashes)

**Current governing set (multi-game ratified 24 Oct at 057fd8c):**

| Document | Status | Key content |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_4.md` | Ratified 24 Oct (supersedes v0.3 for scope) | Charter; section 0A: two games POWERBALL / OZLOTTO, one game per run, Oz current era from 1474 (17 May 2022) 7-of-47, supplementaries excluded from science but archived raw |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | Ratified | 62 methods E_1-E_62 (unchanged; per-game applicability lives in registries) |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` + `..._R2_v0_3_Erratum_Record_v0_3.md` | Ratified / approved | Erratum record keeps ERR-R2-01..04 (ERR-R2-02 Option F still provisional) and adds ERR-R2-05 (per-game contracts: (game_id, draw_number) identity, per-game views/registry, Oz holdout rule, derived-date views, development targets < holdout_first) |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_3.md` | Ratified 24 Oct | Section 0A: per-barrel scoring, Oz PB channel ABSENT, per-game chance figures (Oz 49/47, mid-rank 24), no pooling, per-game freeze/timing |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_6.md` | Ratified 24 Oct (self-contained) | Section 0A: profiles as frozen Python module, identity, prefix-only loaders, bounded structural auditor, derived weekly dates, Run_Scraper.bat, method-generic runtime, console protocol + coordinator exit receipt, global orphan marker; section 5C safety unchanged |
| `Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_1.md` | Ratified 24 Oct | Packages 1-3 and invariants M-INV-01..07; workstreams W1-W6 |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_2.md` | Ratified (P0-P2) | POC; unchanged |
| `doc/contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md` | Ratified | Encoding unchanged; applies to every game, game identity via the view digest |
| `doc/RATIFICATION_REGISTER_v0_2.md` | Register | Hashes and dates of all governing documents |

Superseded but retained: Proposal v0.3, R2 Erratum v0.2, R3 v0.1-v0.2, Architecture v0.2-v0.5, POC Task Spec v0.1. Reviews in `doc/`: `Claude_Research_Historical_Results_Sources_v2.md` (v1 superseded). Claude's multi-game review v3 (`Claude_Review_MultiGame_Architecture_v3.md`, SHA `1efdaf0a...`) was given to the owner.

R1 method families: E_1-E_6 originals; E_7-E_16 frequency/Bayesian/regime; E_17-E_22 recurrence; E_23-E_32 within-draw/drawn order; E_33-E_40 spectral/curve; E_41-E_48 information/nonlinear; E_49-E_54 ML/external (E_54 uses date covariates); E_55-E_56 ensembles; E_57-E_62 pilot-wave. E_14 and E_54 use dates. Proposed E_63 Chebyshev/minimax (owner idea) is NOT yet registered (governed R1 addition or E_37 variant - owner decision).

---

## 5. Settled decisions - do not reopen without substantive cause

**Data (updated 25 Oct; see `Claude_Review_Package2_v0_10_r1_and_Direction_v1.md`)**
- **Source [OWNER-DECIDED]:** Lotterywest's own results-search page on `www.lotterywest.wa.gov.au` (accepted as official), read by an honest headless browser. No API of any site. `oz.lotterywest.com` blocks automation (Cloudflare) and is never contacted. The Lott: honest automation gets "0 draws found", so it is used only through pages the owner saves by hand outside the repo (`*.mhtml` git-ignored), as a private verifier; nothing derived from it is committed. **No browser impersonation and no bot-protection bypass** (owner agreed).
- **One master per game [OWNER-DECIDED]:** `source_data/<GAME>_results_master.csv` (drawn order; Powerball `Draw_Number,Date,Drawn_1..7,Powerball`; Oz `...,Supp_1..3`), append-only ledger, create-only `backups/` and `grabs/`, value-free init verification JSON. Everything is committed (full offline backup). Updater default = current month plus the previous 5; `--months-back` up to 60. The owner will NOT run the updater, even to test, until after the experiments.
- **Holdout [PENDING-OWNER, tools already use it]:** month-aligned boundary, quarantine from 2026-08-01: Powerball >= 1577, Oz >= 1694. Development = Powerball 1144-1576 (433 draws), Oz 1474-1693 (220). Proposed FINAL_HOLDOUT_10 = Powerball 1577-1586 (changes the ratified 1578-1587), Oz 1694-1703. Proposed narrow exception: the E_1 target-1577 regression (forecast from <= 1576 only; outcome never read).
- The old Powerball files `*_20261021.csv` (444 draws, 1144-1587, unordered and drawn order) contain quarantined rows; read only through a raw first-field filter (draw < 1577), from the working tree or `git show 06f6e0f:`. To be removed from the working tree (`git rm`) after the masters are committed.
- Exposure (value-free record accepted in principle): Powerball 1585-1588 were displayed in the reviewer chat on 25 Oct; commit `9b78b8f` contained a saved page showing recent quarantined draws (removed later, still in history).
- Dates only; no authoritative draw time or timezone exists in the sources checked (owner decided date-only; timing sidecar optional later).
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

**Ratified 24 Oct 2026 - multi-game (do not reopen)**
- Two games, one per run: `POWERBALL` (1144 / 2018-04-19; MAIN 7/35 + PB 1/20; holdout ratified as 1578-1587, now proposed 1577-1586) and `OZLOTTO` (1474 / 2022-05-17; MAIN 7/47; 3 supplementaries archived raw only). No generic engine; profiles are a frozen Python module; `--game` selects one; no free-form barrel parameters.
- Identity = structured pair (`game_id`, `draw_number`); `draw_key` (e.g. `POWERBALL_1577`) display only; `game_id` `[A-Z][A-Z0-9]*`. Legacy v0.1 records without game_id read as POWERBALL via a versioned rule. All Powerball identities and `TIE_SHA256_V1` unchanged; new view schemas name game/era/profile.
- Time axis = draw_number. Dates: DERIVED weekly date (era start + 7 x offset), verified against every snapshot (Powerball 444/444 exact; Oz 1474-1705 exact in the data checked); mismatch blocks only E_14/E_54 for that game. Dates are never keys; date-using views bind the profile version.
- Oz holdout (ratified rule, now proposed to be replaced by the fixed month boundary) = the 10 highest draw numbers of the first structurally accepted winning snapshot, rule fixed before scraping; "structurally accepted" excludes date checks; bounded auditor never emits values. Development targets stay below each game's holdout permanently.
- Results of FAILED/orphan-suspected groups never consumed. Owner regards published draw results as public information (repo may hold source CSVs), but no Lott-sourced data and no Lott scraping (Lottery Corporation terms: browser-only personal use, no reproduction).

**Ratified 23 Oct 2026 (do not reopen)**
- Strict no-status/no-kill rule; persistent orphan interlock with manual clearance (no CLI bypass); status PID block-only; failed-group result firewall (results of FAIL/orphan-suspected groups are never consumed, even if `canonical_result.json` exists).
- E_1 D1: first variant `FULL_HISTORY_RAW_COUNTS_V1` (other frequency variants stay registered). D2: `TIE_SHA256_V1` = R3 tuple, 4-byte unsigned little-endian length + UTF-8; ints base-10 ASCII; digests 64 lowercase hex; barrels MAIN/POWERBALL. D3: P3 real historical *development* may run in parallel with unfinished P2, standalone via `Run_Experiment.bat` only, holdout sealed, no FINAL, no termination, each real gate separately authorised.
- Development order: E_1 alone as lead (done), then E_2-E_6 as one batch, then families.

**Engineering**
- **Architecture 2:** one standalone `.py` per E-method in `src/methods/` (`E_###_name.py`), shared `_common/` helpers, and a small coordinator.
- **Option F is the single launch interface.** Coordinated runs go `Run_Coordinator.bat` -> Python coordinator -> **`Run_Experiment.bat` for every experiment** -> method `.py`. Manual runs go `Run_Experiment.bat` -> method. There is no second production launcher, and direct `sys.executable` launch is only an architecture-change proposal requiring an owner decision.
- **Wrappers:** the owner insisted they keep explicit venv checks, scoped `CALL` activation when inactive, `SETLOCAL`/`ENDLOCAL` restoration, the explicit `.venv\Scripts\python.exe`, and forwarding via `%*`. The coordinator refuses to start unless both `VIRTUAL_ENV` and `sys.prefix` match the project `.venv`, so child wrappers verify rather than activate.
- **Concurrency:** 1-6 workers, default 6; one numerical thread per worker; no nested parallelism.
- **Dependencies:** `install_upgrade_dependencies_into_venv.bat` is the sole human-maintained package list (now default INSTALL_UPGRADE; also INSTALL, UPGRADE, VERIFY; before/after `pip freeze` snapshots and changed-version lines; adds selenium; departs from Architecture 5A.2, amendment pending); `requirements.txt` is historical and non-authoritative. Installed on the owner's PC: psutil 7.2.2, NumPy 2.5.4, SciPy 1.18.1, threadpoolctl 3.7.0, selenium 4.51.0; Python 3.14.8.
- **Timing [OWNER-DECIDED 24 Oct]:** human-speed. `POLL_SECONDS_DEFAULT/MIN/MAX` 1.0/0.5/5.0 (`--poll-seconds`), `PIPE_EOF_WAIT_SECONDS` 5.0, `RELEASE_POLL_SECONDS` 0.5, `RELEASE_WAIT_SECONDS` 15; one shared blocking `messages.get(timeout=...)` helper; capture throttle = poll interval; line-buffered logs. Web tools pause >= 2 s between page loads.
- **Reader [OWNER-DECIDED]:** one common reader; views `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC`; no per-method view-entitlement registry; the scientific result allowlist stays (empty).
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
- **Lotterywest results search:** `https://www.lotterywest.wa.gov.au/results/<powerball|oz-lotto>?fromDate=Ddd+Mmm+DD+YYYY&toDate=...&filterByGame=<5132|5130>`; the path selects the game (a saved page keeps the selected game in `filterByGame`); at most 100 draws per search; per draw: `Draw N`, date, `Winning numbers:` 7, `Powerball:` 1 or `Supplementary numbers:` 3, `View prizes`; robots.txt allows all; works under honest headless Selenium.
- **The Lott saved pages:** read only `section.results-search default-results`; the Drawn toggle (`.ball-order button`) is active when it has the `disabled` attribute; the latest-draw panel ("Draw No. ...", "Jackpotted to draw") shows quarantined draws and must never be read.
- **Line endings for hashed data:** proposed `.gitattributes` line `source_data/** -text` keeps masters byte-exact under any `core.autocrlf` (tested).
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

**Phase:** multi-game Package 2 (ChatGPT) awaiting v0.11; results data in place on the Claude side; science paused (Powerball scorer/walk-forward and E_2-E_6 resume after Package 2).

**Powerball E_1:** E_001 standalone at `fbb66efe`; first real run target 1577 reproduced by Claude: view `d47fbbd6...4339`, result `7f113087...164e`. Under the proposed month boundary 1577 is quarantined; the regression is kept as a forecast-only exception (pending). Claude has deliberately not computed any 1577 score.

**Package 2:** v0.9 reviewed (consolidated review v2, `bd5665e0...`, committed). v0.10-r1 (`f1db9629...cf45b`) reviewed: no blockers; C1 N-1 leak via numpy slice `.base` (views must own copies); C2 method boundary (methods get views only; prefix-only per-run parse bound to the ledger hash; poisoned-suffix, link and static checks); C3 dates exposed but not digested; C4 coordinator "exact" diff mismatch; C5 keep a pre-build 1577 regression from git history; C6 timing literals and the missing `RELEASE_POLL == POLL_MIN` test. Direction document `Claude_Review_Package2_v0_10_r1_and_Direction_v1.md` asks for v0.11: those fixes, reader consuming the master, the boundary behind named constants, retiring ChatGPT's results-acquisition modules (API client, saved-page parser, results tool, `Run_Scraper.bat`), and [RATIFY] amendments (installer 5A.2, masters vs immutability, source, boundary/FINAL_HOLDOUT_10, exposure record).

**Claude-side tools (owner-run):**
- `src/two_site_results_check_v0_7.py` (committed `995920d`, SHA `69cb1dec...9aed`, self-test 14/14): `--build-history`, `--offline-dir --against-run`, `--pick-lott-sample`, `--diagnose-lotterywest`; hard quarantine STOP before numbers are read; value-free reports; create-only git-ignored runs under `private_results_checks/`.
- `src/results_master_v0_1.py` + `Run_Results_Updater.bat` (delivered 25 Oct; self-test 9/9, fake-browser scenarios 9/9 in Claude's scratch, init tested on the real old Powerball rows). `init` (offline, once) re-verifies the build and Lott runs, re-validates every row, re-runs the Powerball 433/433 old-file comparison, writes create-only and re-reads. **Expected Powerball master SHA-256 `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8`** (computed by Claude from the old committed rows). `update` is gated by `source_data/HOLDOUT_OPENED_<GAME>.json` (no override), lock file, ledger-hash check, overlap must match exactly, backup -> atomic replace -> ledger.

**Owner's private runs (git-ignored, on the owner's PC):** build `run_20261025T020840Z_5a7fbb` (Powerball 433/433, Oz 220/220, 0 missing/extra/off-date; Powerball vs old files 433/433); Lott check `run_20261025T021022Z_714ecd` (seed 20261025; Powerball 52/52 over 12 months, Oz 31/31 over 7 months). Saved Lott pages contain the quarantined panel; Claude advised deleting them (their hashes are in provenance).

**Not done / not authorised:** the updater run; Mode H; FINAL; holdout access; destructive tests; P2 closure; any Oz science.

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

1. The owner's `init` run: check the console output (both games INIT, warnings 0, Powerball old files 433/433, Lott tallies, re-read identical) and the Powerball master SHA against `ce0ae7e7...66b8`. Then commit the masters, ledgers, init records and `.gitattributes`; then `git rm` the old `*_20261021.csv` files.
2. Owner decisions P1-P3 (August 2026 boundary; FINAL_HOLDOUT_10 = first ten; E_1 1577 forecast-only exception) and the order-status rule.
3. Review Package 2 v0.11 against the direction document (C1-C6 especially N-1; reader bound to the ledger; retirements; amendments).
4. Resume: Powerball walk-forward to 1576 and Oz to 1693, then E_2-E_6, then families.
5. P2 coordinator v0.7 + destructive-gate plan, then owner-authorised destructive tests, P2 closure, ERR-R2-02.
6. Later: Mode H package (runner, holdout loading, opening record); production weekly loop (updater -> score frozen forecast -> retrain -> freeze -> push).

*End of handover.*
