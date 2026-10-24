# Predictive Randomness — Multi-Game Infrastructure and P3 Transition Task Specification

**Version:** v0.1 — OWNER-RATIFIED, 24 October 2026  
**Status:** **OWNER-RATIFIED SPECIFICATION / NO CODE, SCRAPING OR DATA EXECUTION AUTHORISED**. Development remains paused pending an explicit separate owner go-ahead.  
**Repository path:** `doc/Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_1.md`  
**Baseline:** existing ratified Powerball Architecture v0.5 and POC Task Spec v0.2; the independent Claude Multi-Game Architecture review v3 (24 October 2026).  
**Ratified governing prerequisites:** Proposal v0.4, ERR-R2-05, R3 v0.3 and Architecture v0.6, without changing their historical ratified predecessor files.  
**Purpose:** a bounded implementation plan to support two approved lotteries **without changing** current Powerball scientific identities or weakening Windows process-safety requirements.

## 1. Boundaries, authority and ordering

This is not a continuation of the original P0/P2 destructive-test specification; that remains governed by POC Task Spec v0.2. This task is the *new* P3/shared-infrastructure work needed **before** E_2–E_6 and the postponed scoring/walk-forward implementation. Only document drafting has presently been authorised. All production implementation, scraping, method execution and holdout opening remain on PAUSE until the owner's explicit stop/go decisions.

- **Package 1 (DOCS ONLY)**: this multi-game charter, R2/R3, Architecture and task candidate review **together**. Claude independently reviews scientific identity, process safety and synthetic/real, N−1, holdout boundaries. Owner ratifies each consequential document, in order beginning with the charter. **No production changes.**
- **Package 2 (CODE)**: after separate authorisation, implement profile modules, shared method-generic runtime/result contract, game-aware source/reader/scorer APIs, per-game scrapers and launcher, bounded structural audit, complete synthetic fixtures and exact Powerball golden regressions. One consolidated, hashed, diff-based code review by Claude, then owner-operated synthetic Windows tests. **No Oz Lotto science.**
- **Package 3 (FIRST OZ DATA)**: after owner go-ahead, one controlled Oz Lotto scrape and structural validation under the pre-sealed holdout rule, archive raw and winning snapshots, record content digests and actual sealed draw boundaries. **STOP after audit:** no Oz development scoring, fitting, holdout display or FINAL without a later independent review and owner authorisation.
- After that STOP, the pending E_1 development scorer / walk-forward and E_2–E_6 resume using the common contracts. This task does not authorise their implementation now, nor modify the prospective freeze/start policy.

## 2. Invariants to preserve throughout

**M-INV-01 — Legacy reproducibility.** No changes to existing Powerball CSV bytes, E_1 v0.3 source-as-reference, permitted real-U digest `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339`, result hash `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e`, TOP `[9,17,7,11,18,30,12]`, PB TOP 2, WORST `[31,13,8,29,26,33,35]`, PB WORST 12; synthetic goldens and `TIE_SHA256_V1` unchanged. A new wrapper hash must have a new schema name and be labelled as such.

**M-INV-02 — Per-game identity.** Unique key `(game_id, draw_number)`; never draw number alone. Numeric collisions permitted; cross-game lookup forbidden unless separately authorised as an explicit covariate view. All new records require both structured fields.

**M-INV-03 — N−1 and holdout.** Scientific loaders never read target N or later. Structural auditors use an independent bounded interface for all rows, including held-out rows, and **never return raw values**. The Powerball holdout 1578–1587 remains sealed; Oz holdout follows the first-structurally-accepted-snapshot 10-highest rule before scraping. **Historical development/backtesting targets alone are limited below the first held-out draw** (`POWERBALL` maximum 1577; `OZLOTTO` maximum `holdout_first − 1`), even after later unsealed draws arrive. This restriction is NOT a permanent draw ceiling for ordinary operation or maintenance: separately authorised prospective FINAL predictions, eligible retraining and scoring can progress to later draws under N−1, freeze and holdout protections. Retrospective development beyond the seal needs a separately approved protocol. No outcome-aware design decisions precede the seal.

**M-INV-04 — Real/synthetic firewall and failure policy.** Synthetic and real source/fit/output namespaces stay separate. Only validated successful manifests may be consumed. FAILED or orphan-suspected results cannot be consumed even if a result file exists. No published record is overwritten.

**M-INV-05 — Process safety.** Current global orphan marker blocks either game. Ownership requires positively verified PID + creation time, status and captured process ancestry; a status PID can block but never authorize a kill. No `taskkill` fallback, CLI bypass or manual clearance shortcut. `ENABLE_PROCESS_TERMINATION` stays disabled absent its distinct reviewed, explicit owner gate.

**M-INV-06 — One selected game.** The intended operating workflow processes a single explicitly selected profile, not concurrently mixing experiments or datasets. No free-form ball/barrel CLI parameters. A resource-overcommit warning is advisory; no second hard interlock added in this work.

**M-INV-07 — Method openness.** Register all permanent E-numbers for each game, with support status based on structure and available scientific views, not on conventional probability judgments or cost. No method silently removed or fictitious second barrel supplied for Oz.

## 3. Proposed implementation workstreams (Package 2; not authorised by drafting)

### W1. Frozen game profiles and scientific identity

- Create a versioned source-code constant registry for `POWERBALL`, `OZLOTTO` only. Fields: profile ID/version, era start draw/date, permitted view schema names, actual ordered barrel descriptors, support registry location, caps/holdout rule + seal record reference, nominal local draw and closure time with IANA timezone and draw-specific UTC conversion. Validate constants at module import/test, not on an editable runtime configuration file.
- `POWERBALL`: 1144/2018-04-19, MAIN labels 1..35 choose 7, PB labels 1..20 choose 1, development cap `≤1577` and sealed holdout `1578..1587`. `OZLOTTO`: 1474/2022-05-17, MAIN 1..47 choose 7, current-era only, raw supplementary count 3 *outside science*; development cap fixed as `holdout_first − 1` after sealing. Operator confirmation of Oz current-era start remains a check, not a claim that the scraper has already passed.
- CLI chooses `--game`, no numeric profile overrides. `game_id` regex `[A-Z][A-Z0-9]*`; display `draw_key` formed from `game_id` + `_` + draw number. Never derive source authorization from display label alone.
- Date = era-start + 7-day draw offset, verified against every recorded source date. Date-dependent methods must stop on mismatch; non-date methods continue only if all other validity rules pass. Target row N is never parsed by method loader. Derived-date view identity binds game/profile/schema without modifying the frozen Powerball U view.

**Acceptance:** game/cap boundary tests; same-number different-game collision; immutable profile version; schema-domain disjointness; Powerball real E_1 digest identical; synthetic Oz independent golden vectors; nominal timezone/DST test when official times are established. No date-time values invented to pass tests.

### W2. Separate scrapers, immutable snapshots and `Run_Scraper.bat`

- Human command `Run_Scraper.bat POWERBALL|OZLOTTO` with same venv checks/temporary activation and restoration as existing wrappers. No scraping implicitly triggered by E-methods/coordinator; no package upgrade at runtime.
- Keep separate scraper implementations. Powerball scraper is refactored so its output location is approved source namespace rather than implicit `src/`, without silently changing existing archived CSVs. Oz scraper fetches operator results and emits **two create-only, dated snapshot files**: a winning-only U CSV and an independent raw/provenance CSV preserving supplementaries and dates. Print/export SHA-256 for each file and the source/origin revision; enforce basename/path safety and no overwrites on repeated invocation.
- Choosing an accepted data snapshot is an **operator-controlled step**, not automatic latest-file adoption. Preserve old historical source names/hashes and a durable snapshot acceptance ledger. Output is not itself authorised real training data.

**Acceptance:** synthetic scraper-data fixture, output shape, two-file separation, create-only collision, `.venv` restoration, malformed source refusal, path injection/traversal refusal, full hash match and no unexpected global state mutation. Later first live operator scrape occurs **only at Package 3**.

### W3. Bounded structural auditor and Oz holdout seal

- Freeze rule before first live scrape: ten highest draw numbers in the **first structurally accepted** Oz current-era winning snapshot. Do not choose the range using outcomes. Structural acceptance requires draw range/current era, uniqueness/1..47/count 7, supplementary provenance structure/count where available, no duplicate rows, consecutive unique draw numbering from 1474, strict two-file winning/raw separation and recorded hashes. **Derived-date equality is checked and logged as an independent audit signal, NOT a condition for snapshot structural acceptance or holdout sealing.** A date mismatch is recorded against the affected draw/field in audit and seal records and halts date-dependent methods E_14/E_54; non-date U-view methods remain eligible if all other structural conditions pass.
- Auditor may parse sealed rows in an internal isolated buffer solely to perform structural checks. It emits `game_id`, profile/schema, snapshot hash, row counts, overall pass/fail and bounded anomalies by `draw_number` and `field/rule` **without ball values**. Do not print a CSV excerpt, frequency, histogram, actual numbers or a trace of offending contents. Errors in a holdout row are anonymised to field name/draw number, as expressly permitted; raw and winning file paths are not conflated.
- The seal record binds first structurally accepted snapshot SHA-256, exact held-out draw range, rule version, accepted game/profile, timestamp and audit record identity, **plus a bounded summary of any date anomalies without any held-out values**. New later snapshots cannot silently move the holdout. If the first scrape fails **the structural acceptance criteria** (as distinguished from date anomalies alone), **no seal is established** and further actions require explicit operator response; never adjust the rule based on drawn balls.

**Acceptance:** synthetic date-discrepancy fixture remains seal-eligible if all structural requirements pass, records non-value date anomaly and blocks only date-dependent methods; invalid winning counts/ranges, era, numbering, file separation or unrecorded hashes block acceptance; invented sealed rows with deliberate invalid values; auditor reports only allowed error metadata; memory/intermediate files outside method-readable paths; no raw values in logs/exceptions; invariant that no scorer/trainer receives audit output or a held-out row. No actual Oz holdout outcomes inspected by developers or reviewers.

### W4. Method-generic runtime, one executable per E-number and result consumer

- Convert the E_1-only `e1_standalone_contract_v0_1` assumptions (hard-coded `e1-` IDs, `E_1` method, variant/schema, cap and output location) to a separately versioned, method-generic contract; retain the reviewed E_1 module and historical outputs unchanged. Same shared `ENGINEERING_POC_STATUS_V1` fields as required by ratified Architecture until a separately reviewed schema migration.
- One executable `src/methods/E_NNN_descriptive.py` per registered E-method, with game-qualified `--game`, target and method identity, immutable run root/ID handshake, validated profile and method-registry support. Produce canonical forecast bytes and status/manifest under game-qualified namespaces, with create-only publishing and no failure-to-PASS promotion.
- **Coordinated console protocol compatibility is a mandatory pre-run gate:** the existing coordinator v0.6 `status_and_result` validator expects a method's `BEGIN` and `FINISH` console lines and `RESULT`/`DIGEST` statements consistent with the published canonical result (current coordinator around lines 704–710). E_001 currently prints only STARTED and a prepared-result message, so launching it as a coordinated method **would be `INVALID_RESULT`**, even if its own manifest reports PASS. Define and implement **one reviewed, method-generic console protocol** (or explicitly and safely generalise coordinator validation), covering identity, target, BEGIN/FINISH, RESULT path and DIGEST binding, **before ANY coordinated method run**. A handoff must test console/schema byte identity, failed/partial output, mismatches and validation refusal. The coordinator source must not be relaxed implicitly.
- For future coordinated and FINAL consumers, require a **coordinator-created `exit_receipt.json`** after root wrapper exit. Its identity/exit/status binds to the run and root PID/create time, and it cannot be faked by a method. The existing narrow standalone historical self-report rule applies only where already approved. Never infer safety from Task Manager process names.
- Consumer `verify_and_consume` first validates selected game, target, profile, allowed view, global marker, status and success/failure/orphan flags, hashes and (for coordinated/FINAL) exit receipt, and only then opens the result. No bytes from FAILED/orphan-suspected groups are passed to downstream code.

**Acceptance:** coordinator v0.6 synthetic fake-method handshake refuses missing BEGIN/FINISH/RESULT/DIGEST and mismatched result hash; reviewed new console protocol or validator update accepted before coordinated E-method launch; Powerball E_1 true 1577 legacy forecast identity unchanged; new wrapper schema labelled; simulated one-barrel Oz fields with PB ABSENT; fake PASS/mismatched game/target/status hash rejected; failure without result safe; run-ID collision refused; no future data read; spoofed PID/ctime cannot become kill target; `exit_receipt` handback separately reviewed.

### W5. Barrel-aware scoring, evaluation and reporting APIs (no real Oz scoring now)

- Build scorer interface driven by actual profile barrels; rank only eligible labels, TOP and WORST from same frozen ordering, mean mid-rank from *native scores prior to SHA tie resolution*. Reference figures per actual barrel (Powerball 7-of-35 + 1-of-20, Oz 7-of-47) are context only. A missing Oz PB channel is truly absent, not zero.
- Evaluation first consumes and validates the frozen success result before loading **exactly the game-qualified target outcome** through a separately authorised evaluator-only interface; no N or future outcome available to the predictor. Include game/target/profile in every score row, and never pool game performance implicitly.
- The previously drafted E_1 walk-forward window (Powerball 1145–1577, zero burn-in, all targets reported) remains **RECOMMENDED and unratified**, and implementation stays PAUSED. This shared infrastructure can be implemented with synthetic outcomes first, but no Oz scores or Powerball holdout scores under this package.

**Acceptance:** synthetic 7/35+PB and 7/47-only mathematical goldens; exact native-score tie/mid-rank; qualified same-number collision; fail/group firewall; mandatory frozen artifact and source-view identity; all target statuses retained with no silent exclusions; no real outcomes accessed during package-2 tests.

### W6. Provenance, tests, documentation and code review

- Ship a review ZIP containing identified Git baseline, repository-relative overlay (excluding any real activation switch), exact diffs, SHA-256 of all changed files, synthetic test transcripts, DECIDED/RECOMMENDED/OPEN register and plain-English risk list. Expose the existing ratified source bytes unchanged wherever practical; establish method/package provenance without forcing future source rehashes unrelated to methods.
- Tests must cover independent Powerball 1577 golden recomputation, original synthetic goldens, a synthetic Oz one-barrel profile, prefix-only U loaders, suffix poison/target mutation, drawn-order/supplementary exclusion, date discrepancy behaviour, sealed-bound audit no-value output, create-only snapshot collision, group-failure firewall, game-scoped names and no fake PB, and unchanged orphan gate. Perform separate review of anything affecting termination ownership.
- Installation is a separate **owner action**, never implied by creating a review package. No destructive tests, Ctrl+C cleanup, first Oz scrape, real Oz method run or FINAL publication from Package 2.

## 4. Package 3 — first real Oz Lotto data intake, structural only

**Precondition:** owner has ratified Profile / holdout rule / charter/R2/R3/Architecture and independently reviewed the code package with satisfactory synthetic Windows results. Owner then explicitly authorises the first scrape **separately**. Confirm source endpoint and current era operator facts. Preserve command transcript, hashes, source provenance, errors and process/environment evidence.

Run one approved scraper, obtain winning-only and raw provenance snapshots, validate dates/draw numbers/number-range/supplementary structure using bounded auditor. If accepted, seal ten latest current-era draws from the first accepted winning snapshot and archive the seal record. **STOP** immediately afterward. Report metadata only: validated draw-number bounds, date bounds, seal range, counts, source file SHA-256, validation PASS/FAIL and anomaly field names. Never inspect/display held-out outcomes. A later owner decision is necessary for any scientific Oz trial.

## 5. Continuity: existing P2, E_1 and later development

- The P2 coordinator v0.7 ownership safety patch and destructive-gate plan remain in their separate review/owner decision track. Existing safety rule, global marker and `ENABLE_PROCESS_TERMINATION = False` remain binding. Multi-game development neither closes P2 nor grants process-kill authority.
- Powerball E_1 historical draw 1577 already has independent prediction-verification evidence; keep it unaltered. Its scoring and proposed zero-burn-in walk-forward window are **pending scientific review/ratification**, currently paused, and may resume only following the owner's explicit restart after the new contracts are accepted.
- After Package 3's STOP and any follow-up review/approval, the programme can progress E_2–E_6, then family batches with mathematical fixtures and per-family FORMULA_OPEN decisions. The Oz-specific method run needs its own gate; no cross-game science is introduced by mere infrastructure support.
- E_63 Chebyshev/minimax remains a separate proposed E-number, needing governed R1 addition or the owner's alternative placement decision, not settled here.

## 6. Decisions and reviewer questions

**OWNER-RATIFIED scope, 24 October 2026 (implementation still separately gated):** (1) add Oz Lotto as second scoped game; (2) current-era, seven-winning-only/supplementaries-raw rule; (3) holdout selection rule before scrape; (4) compound draw identity and legacy-compatibility scheme; (5) derived-date rule and profile-bound date views; (6) per-game score/freeze isolation; (7) self-contained Architecture v0.6/initial code-package gates. All remain unratified in this review candidate.

**DECIDED for drafting only:** propose two frozen profile constants, one selected game per run, game-prefixed new outputs, method-generic common runtime, a bounded structural-audit API, separate provenance CSVs and simple Task Manager visibility; these are implementation proposals within existing owner direction, not source changes.

**OPEN / evidence required:** Oz first operator snapshot/official draw 1474 confirmation; draw/close nominal clock and reliable UTC-deadline rules; exact first snapshot/holdout range/hash; exact new JSON schemas; reader implementation; E_54 covariate timing; any future new game/rules era; experimental method formulas for Oz and E_63 placement. No guesses shall be frozen as facts.

**Claude review focus:** Does any clause weaken Powerball immutable identities, R2 N−1, failure firewall, global orphan safety, or per-game holdout separation? Is the date mismatch policy correctly qualified? Are new result/status requirements sufficient and backwards compatible? Are the three stop/go packages minimal and correctly gated? Are any owner-reserved decisions mislabelled DECIDED? Review against the ratified predecessors and the *v3* reviewer document only; v1/v2 are superseded.

---

*End of owner-ratified v0.1 task specification — no implementation or run authority.*
