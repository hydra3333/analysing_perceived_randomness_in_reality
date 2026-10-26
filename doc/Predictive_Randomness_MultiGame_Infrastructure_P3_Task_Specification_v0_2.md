# Predictive Randomness — Multi-Game Infrastructure P3 Task Specification

**Version:** v0.2 CONSOLIDATED, OWNER-RATIFIED 26 October 2026  
**Stage:** Package 2 v0.11, independent Claude review required; no code execution authorisation  
**Source lineage:** ratified P3 v0.1, reviewed v0.2 update, owner decisions 25 October 2026, Claude v3 direction.  
**Purpose:** current implementation plan only; scientific and safety authority remains with Proposal, R2, R3 and Architecture.

## 1. Completed prerequisites and current boundary

- [OWNER-DECIDED / DONE, owner-run] Version-1 development masters exist: POWERBALL 1144–1576 (433) and OZLOTTO 1474–1693 (220); verify their SHA-256 and INIT ledgers as specified in Architecture. Historic Powerball 433/433 and The Lott private historical samples were reported passed; no new scraping is required from ChatGPT.
- [DONE / OWNER-DECIDED] Owner-maintained `src/two_site_results_check_v0_7.py`, `src/results_master_v0_1.py` and `Run_Results_Updater.bat` are authoritative. Do not duplicate, rewrite or invoke them in Package 2. Their owner-run INIT results are accepted; `update` remains explicitly unauthorised.
- [OWNER-DECIDED] Quarantine starts 2026-08-01: Powerball first sealed 1577, holdout ten 1577–1586; Oz first sealed 1694, holdout ten 1694–1703. No held-out values are read. E_1 target 1577 is regression forecast-only from 1144–1576.
- [REVIEWED CANDIDATE] Package 2 v0.10-r1 provided method-generic contracts and coordinator prototype. Claude identified C1–C6 requiring v0.11 corrections. No coordinated scientific result schema is enabled.

## 2. Package 2 v0.11 mandatory implementation work

### W1 — Ledger-pinned scientific reader (C1, C2, C3; critical no-go gate)

- Consume `<GAME>_results_master.csv` pinned to exact approved ledger version + master SHA. Hash complete master bytes only as integrity/provenance; parse only lines whose first `Draw_Number` is strictly below target N. Never convert any other field of row N or later. The target outcome remains unseen. Reject symlinks and `st_nlink > 1` paths; test poisoned suffix and links.
- Methods receive only a safe, readonly, byte-backed owned-prefix `DrawView` or plain Python integer lists, never an unrestricted table or source path. For every array, `.base` is `bytes` of exactly prefix-length × row item size, with no path to later rows.
- Internal numeric table **and exported scientific views** use NumPy `int64` integer and `float64` floating dtypes. Typed ISO dates remain dates; date access opt-in under new schema and digest. Test `47 * 47 == 2209` with view arrays. Preserve legacy E_1 date-free digests and tie encoding exactly.
- `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC` are caller choices and **do not** require a duplicate per-method entitlement registry. An experiment must declare which it actually consumes, and the separate scientific-result consumer allowlist remains strict and empty until independently approved. The assumed order label and evidence citation travel with every order-consuming view.

### W2 — Prebuild golden and source-history comparison (C5, optional O1)

- Reconstruct old Powerball source rows only through a raw first-field draw-number filter from historical commit `06f6e0f`, reading only rows with draw < 1577; do not DictReader-parse quarantined rows before filtering. Test the accepted E_1 draw-1577 **forecast only**, training-view SHA `d47fbbd6…4339` and canonical-result SHA `7f113087…164e`; never read/score target result.
- Check accepted synthetic E_1 vectors, new master/ledger identity, missing/poisoned suffix, negative game/era/holdout cases, and frozen scientific-result allowlist. No real Oz method run or real-scored experiment.

### W3 — Coordinator timing and receipt correctness (C4, C6)

- Human-speed helper: one `--poll-seconds` default 1.0, bounds 0.5–5.0; pipe EOF cap 5.0; ancestry release poll 0.5 / wait 15.0; line-buffered per-worker logs. Wake on queue output or configured interval, no fast-loop scans. Define remaining timing literals only in functions approved for editing.
- Atomic create-only ancestry release: status-derived PID/create time and run match, never a method-originated coordinator receipt. Receipt issuer reads and hashes exactly the canonical bytes it verifies, correct exit-observed UTC, known-good source import path. Consumers only use verifier-returned result; a synthetic probe can never enter scientific scoring.
- Regenerate exact v0.6 coordinator diff mechanically against SHA `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`. Show AST match of all protected safety functions, both review gates and all safety flags `False`; no destructive run.

### W4 — Retire superseded ChatGPT acquisition code; retain owner tools

- Remove from the reviewed v0.11 overlay (with an explicit retirement list) ChatGPT's Lotterywest API adapter, saved-page client, results build/publisher, `Run_Scraper.bat` and related policy/fixture tests that no longer serve the approved owner-run master. Preserve the old Powerball scraper as historical evidence only.
- Reference Claude-side `results_master_v0_1.py`, `two_site_results_check_v0_7.py` and `Run_Results_Updater.bat` by their actual repository paths and SHA when available. Do not rewrite or silently call them. Reconcile `requirements.txt` with the single authoritative dependency-maintenance `.bat` (or label requirements historical).

### W5 — E-method/coordinator-scoring gates (not auto-enabled)

- One approved game-qualified E-method runtime and console BEGIN/FINISH/RESULT/DIGEST contract, method/wrapper manifest, and coordinator-only run/exit receipt are required *before* any coordinated science. Never infer scientific permission from synthetic worker tests. Failure/orphan-suspected group results are never consumed, even if a canonical file exists.
- Scorer works per actual profile barrel: Powerball MAIN/PB and Oz MAIN only; rank-position mid-ranks from native scores, unaffected by readout ties. The outcome provider is evaluator-only and not called before verified frozen forecast. Preserve per-game evidence and no pooled scores without prior owner approval.

### W6 — Offline evidence and review deliverable

- Single v0.10-r1 → v0.11 code delta with exact repository lineage and one SHA manifest. Full applicable offline suite transcript and explicit retired-test replacements. Include corrected N−1 and dtype/overflow tests, prebuild 1577 golden regression, static import/path checks, human-speed simulated queue tests, receipt/synthetic classification, and a precise coordinator diff against ratified v0.6.
- Owner-run Windows P1/P2 and lifecycle command lists are **instructions only** until separately reviewed/authorised. Preserve `ENABLE_PROCESS_TERMINATION = False`, `ENABLE_SCIENTIFIC_COORDINATION = False`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE = False`; no override.
- Every finding/decision is labelled DECIDED, RECOMMENDED or OPEN. Claude independently reviews the delta, the owner then decides whether to install and run separate Windows tests.

## 3. Phase and approval boundaries

**Phase 1 development:** use only the version-1 development masters; no `results_master update`, `HOLDOUT_FETCH`, Mode H, FINAL, Windows lifecycle or other real-data run by ChatGPT. Scientific use of the v0.10 reader is NO-GO until C1/C2 corrections pass Claude review.

**Phase 2 (Mode H):** NOT AUTHORIZED. New per-game study manifest/environment snapshot, owner-only opening record, safe stepwise freeze-before-outcome and append-only scoring; must independently review whether quarantine storage remains separate or a master is updated, and later quarantined draws. No silent implementation choice.

**Phase 3 production:** NOT AUTHORIZED. Following Mode H and explicit owner decision, routine owner-run results updater may append eligible new draws with overlap verification, backup/grab/ledger. Genuine next-draw FINAL refits on all then-eligible completed past draws under each method's registered window and freezes before the event; scoring later.

## 4. OPEN / deferred items

Before any walk-forward method run, preregister the selected per-game development target windows (Powerball 1145–1576, Oz Lotto 1475–1693, subject to each method's minimum-history requirements). Optional O2 owner-provided real pre-boundary page fixture remains OPEN, not an acceptance prerequisite.


**OPEN — pre-registration:** before any research walk-forward evaluation, separately register target windows (proposed POWERBALL 1145–1576 and OZLOTTO 1475–1693), burn-ins, exclusions, and source/fit/view identities. **O2** owner-supplied real pre-boundary page fixture is optional; do not treat it as a mandatory prerequisite or solicit quarantined values. No scientific run is authorised.

- Detailed Mode H runner, sequential outcome release, storage separation and treatment of quarantined draws after each game’s first ten.
- Draw time/timezone from reliable operator evidence; master currently stores ISO date only. Optional future timing sidecar.
- Individual `FORMULA_OPEN` methods, first authorised real Oz Lotto scientific trial, cross-game covariate contracts, and separately governed E_63.
- Windows lifecycle and process-termination safety tests pending independent review and explicit owner approval.


## 5. Preserved P3 M-INV invariant catalogue (owner-decided updates)

**M-INV-01 — Legacy reproducibility and current master-backed goldens.** Preserve E_1 `E1_REAL_U_TRAINING_VIEW_V1` digest `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339` and frozen result `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e`, its frozen TOP/WORST forecast, full synthetic goldens and `TIE_SHA256_V1` unchanged. The old sorted/order CSV bytes are preserved through Git source history, while the owner-accepted Powerball master reproduces the permitted 1144–1576 prefix. Any new wrapper hash requires a new schema and cannot overwrite these frozen identities.

**M-INV-02 — Per-game identity.** Unique key `(game_id, draw_number)`; never draw number alone. Numeric collisions permitted; cross-game lookup forbidden unless separately authorised as an explicit covariate view. All new records require both structured fields.

**M-INV-03 — N−1, quarantine and holdout.** Scientific loader scans a row’s raw `Draw_Number` first, parses/converts no row N or later, and returns prefix-only owned `int64`/`float64` views. The full master may be SHA-256 hashed as uninterpreted bytes for integrity. Structural auditors use bounded value-free reports, never held-out numbers. Fixed boundary 1 August 2026: development POWERBALL <=1576, OZLOTTO <=1693; `FINAL_HOLDOUT_10` Powerball 1577–1586 / Oz Lotto 1694–1703. E_1 1577 regression is forecast-only; no scoring/outcome access. Opening holdout or FINAL requires separate owner approval.

**M-INV-04 — Real/synthetic firewall and failure policy.** Synthetic and real source/fit/output namespaces stay separate. Only validated successful manifests may be consumed. FAILED or orphan-suspected results cannot be consumed even if a result file exists. No published record is overwritten.

**M-INV-05 — Process safety.** Current global orphan marker blocks either game. Ownership requires positively verified PID + creation time, status and captured process ancestry; a status PID can block but never authorize a kill. No `taskkill` fallback, CLI bypass or manual clearance shortcut. All three process-termination enable switches stay disabled absent its distinct reviewed, explicit owner gate.

**M-INV-06 — One selected game.** The intended operating workflow processes a single explicitly selected profile, not concurrently mixing experiments or datasets. No free-form ball/barrel CLI parameters. A resource-overcommit warning is advisory; no second hard interlock added in this work.

**M-INV-07 — Method openness.** Register all permanent E-numbers for each game, with support status based on structure and available scientific views, not on conventional probability judgments or cost. No method silently removed or fictitious second barrel supplied for Oz.

## Appendix S — Withdrawn P3 plan (historical only)

- Old W1–W3 two-game scraper/first-Oz-snapshot seal/DEV_BUILD and `Run_Scraper.bat` → completed owner-run master INIT and ledger-bound reader work (§§1–2).
- Former Powerball 1578–1587 and Oz “ten highest first accepted snapshot” seal → fixed August 2026 first ten (§1).
- Earlier `DEV_TO_DATE = 2026-08-07` → 1 August 2026 quarantine (§1).
- Old dated immutable snapshot-output scheme → versioned master, ledger, create-only backups and grabs (§1).
- Per-method input entitlement registry → experiment-declared view with strict result-consumer schema allowlist (§2 W1).

*This owner-ratified task specification does not install code or authorise a scientific, Windows, scraping, holdout or termination run.*
