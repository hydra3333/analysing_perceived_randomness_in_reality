# Claude reviewer handover - Predictive Randomness project

**Handover version:** v10. Self-contained: it replaces v9 and the interim note for continuity. v2-v9 stay in `doc/HANDOVER/` as history.

v10 adds to v9:
- the speculative discussion on **method ranking measures** (league tables), which ran through proposal v0.1-v0.5 with three ChatGPT reviews and ended in ratification (section 12A);
- the owner's foundational points about the project's nature (section 2A);
- exposure item 6 (exposure record v0.2);
- the GAIS deletion and the handover snapshot, both verified;
- the agreed plan for integrating the ranking proposal, and the next handovers;
- lessons from Claude's own errors in that work (section 9A).

**As at:** 26 October 2026, evening, Adelaide time (UTC+10:30).

**Repository:** `hydra3333/analysing_perceived_randomness_in_reality` (public GitHub, branch `main`). Claude clones it directly to verify commits.

Verified commits on 26 Oct:

| Commit | What it contains |
|---|---|
| `2db2554` | Governing documents installed |
| `a52ffd8` | GAIS script removed |
| `6726963` | Handover snapshot (v9 and coder handover v1.0r1) |
| `ac01678` | Ranking proposal v0.5 and exposure record v0.2, ratified |
| `cf81f51` | Interim handover note |

The next commit should contain this file (`doc/HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v10.md`) and ChatGPT coder handover v1.1, committed together.

**First actions in a new chat:**
1. Pull GitHub. Verify that this file and coder handover v1.1 are committed, and that the hashes in section 4 still match.
2. Ask the owner where things stand on:
   - (a) integrating the ratified ranking proposal into new governing editions. **Claude drafts this** (section 12, item 1);
   - (b) Package 2 v0.11 in ChatGPT's fresh coding chat.

**Purpose:** continuity for a follow-on Claude chat acting as **independent reviewer**. It records:
- the rules and decisions, including undocumented ones;
- the current status and verified facts;
- the review method that has worked;
- the open items.

**Authority:** the repository's ratified documents prevail over this handover wherever they conflict. This is a summary that points to them.

**Holdout discipline for the reader of this file:** nothing here contains a winning, Powerball or supplementary number. The only number lists are the frozen E_1 *forecast* outputs (section 7). Never display, paste or compute with any outcome for Powerball >= 1577 or Oz Lotto >= 1694.

---

## 1. Roles and workflow

- **Project owner** (GitHub `hydra3333`): sole decision-maker, ratifier and committer. Runs every Windows test and every data tool on their own PC.
  - Never name the owner in anything that may be committed. Write "the project owner" or "hydra3333".
- **ChatGPT:** primary coder and author of specifications and code. Produces versioned documents, repository-relative ZIP overlays and handback notes.
  - From 26 Oct, coding moves to a **fresh ChatGPT chat** seeded with its accepted coder handover.
- **Claude (you):** independent reviewer. Reviews documents and code for substantive errors, conformance with the ratified set, safety and scientific integrity.
  - Claude does not implement project code unless asked. Exception: Claude wrote the owner-run data tools in section 7.
- **Roles were re-decided by the owner on 26 Oct: unchanged.**
- **Flow:** ChatGPT drafts -> owner relays to Claude -> Claude reviews -> owner relays the findings back -> ChatGPT revises -> owner ratifies and commits. Relay is by copy-paste and file upload.
- **Fallback (owner, 25 Oct):** if ChatGPT cannot get a document right, the owner may ask Claude to fix it and supply a blurb, and ChatGPT then reviews Claude's fix.
- **Claude as drafter (owner, 26 Oct):** for the ranking proposal, Claude was the author and ChatGPT the reviewer. Claude will also draft the integration of that proposal into the governing documents, with ChatGPT reviewing. Otherwise the roles are unchanged.
- **Chat limits:** when either AI chat may run out of room, write an interim note first (as on 26 Oct), then full handovers. Do long mechanical drafting afterwards, in fresh chats. Committed documents are safe; unwritten knowledge is what is lost.

**Standing procedure (agreed 23 Oct 2026):**
- ChatGPT makes routine implementation decisions within the ratified specifications. It labels them:
  - DECIDED (within its authority);
  - RECOMMENDED (consequential, awaiting the owner);
  - OPEN (needs evidence or review).
- Claude reviews are bundled at milestones, **except** that these areas always get independent Claude review before consequential execution or acceptance:
  - process termination (kill logic, ownership verification, the safety switch);
  - N-1 training boundaries and leakage;
  - fit seeds and canonical forecast identity;
  - TOP/WORST readout, ties and selection rules;
  - holdout access and unsealing;
  - FINAL freezing, persistence and publication;
  - the synthetic/real firewall;
  - dependency upgrades (W-23 gate).
- For termination changes, static and synthetic checks may proceed with termination disabled. Review plus owner approval are needed before enabling or exercising real termination.
- **Review packages contain:**
  - the exact diff against an identified committed baseline;
  - the SHA-256 of new or changed files;
  - a short handback with test evidence;
  - the DECIDED / RECOMMENDED / OPEN record.
- **Claude's added duty:** check ChatGPT's DECIDED list and flag anything that should have been RECOMMENDED to the owner.
- **Claude's own authority (owner, 23 Oct):** Claude settles routine review matters itself and labels them REVIEWER-DECIDED. Examples:
  - deferrability;
  - packaging and versioning;
  - wording;
  - whether a re-review is needed;
  - test-policy choices;
  - confirmations the owner has already relayed (do not re-ask).

  Only consequential items go to the owner: new rules or scope, anything that weakens safety, switch-on or destructive tests, ratifications, real-data gates, anything irreversible.
- **Claude may flag issues beyond the requested diff** when they are material. Example: the GAIS script, found during the handover review.

---

## 2. How the owner wants work presented (follow strictly)

- **End every review with a short paste-ready block** (a ```text fenced block) for ChatGPT.
- **Separate BLOCKER / CORRECTION / OPTIONAL.** Concentrate on substance, not cosmetic wording. Do not reopen settled decisions without a substantive technical reason.
- **Decisions:** present as plain-English question / why / recommendation / options. When there are several, lead the owner through them one by one with a recommendation each. Put document references on a trailing line.
- **Verify, don't assert.** The owner distrusts assertion. Check claims against the actual files, line numbers, library source or official documentation. Label evidence VERIFIED / OWNER-REPORTED / UNVERIFIED (or documented / source / observed / to be tested).
- **Plain English**, not acronym-dense wording.
- **Files Claude produces:**
  - strict US-ASCII with CRLF line endings, mechanically verified after writing;
  - the version in the file name (`..._v1.md`);
  - no owner name;
  - send them as files, and give a one-line summary plus the paste block in chat.

  A mention of a versioned document means "that version or later", except in records of past events.
- **Superseded versions are kept**, not overwritten. The owner dislikes make-work revisions done only to update version mentions.
- **Process discipline:** propose before transforming; the owner ratifies.
- **Owner's philosophy (binding on the project):**
  - The experiment deliberately challenges "perceived reality".
  - No method may be excluded or ranked down because conventional statistics says it cannot work.
  - The fair-draw reference model is a measuring ruler, never a veto.
  - Real prospective predictions against actual draws are what count.
  - Claude gives reference figures as context only, never as dismissals.

---

## 2A. The owner's foundational points about this project (26 Oct; binding)

1. The project is **deliberately and extremely speculative**. It looks for patterns in reality that conventional statistics may have missed. No idea, method or measure is excluded because conventional statistics says it cannot work.
2. The owner **expects the most likely outcome to be that no method works** as hoped. A carefully measured null result is a valid, useful outcome.
3. **"Mark, never suppress":** every number the owner asks for is computed and shown. Where it is not a calibrated probability, it carries a plain label saying so. Example: the owner knowingly accepts in-sample bias.
4. **Statistics is an instrument for telling kinds of pattern apart, never a gate** on what may be investigated. The four pattern origins:
   - PO-1, an unavoidable consequence of the method;
   - PO-2, an effect of fitting;
   - PO-3, chance, multiplicity or selection;
   - PO-4, a pattern that persists on genuinely new draws.

   Strict N-1, the sealed holdout and the WF/IS separation are kept precisely so that any surprise can be tested honestly.
5. **Openness with discipline:** any idea may be explored, but a claim needs a definable, testable form before results can say anything about it.
6. **Claude's review test for any suggestion:** does it make a number more honest without making any idea, method or measure ineligible? If yes, adopt it. If it would act as a veto, flag it against this philosophy.
7. **Plain language in outputs:** generic-sounding technical terms (for example "walk-forward", "in-sample") are always printed with their exact meaning in this project.

---

## 3. Project in one paragraph

Two games, never pooled, one game per run:
- **Powerball**: current format since **Draw 1144, 19 April 2018**; 7 distinct main numbers from 1-35 plus 1 Powerball from 1-20.
- **Oz Lotto**: current era since **Draw 1474, 17 May 2022**; 7 from 1-47; the 3 supplementaries are archived as provenance only and never enter science.

The project builds a Python 3.14 research system on Windows 11. It tests whether past draws contain any predictive structure, using 62 permanently registered methods (E_1-E_62, with room up to E_106 and no quota). E_1 is "historical appearance frequency", not the pilot-wave family (E_57-E_62); the owner asked.

Each method produces full rankings. For each target it publishes TOP and WORST (inverse) predictions side by side. After each real draw, a forecast is scored by TOP matches, WORST matches and an additional rank-position measure.

Real weekly forecasting starts only after modelling is complete:
1. Train on all eligible draws before the target.
2. Predict the next draw.
3. Freeze and push the forecast before the draw.
4. Score it afterwards.
5. Append the draw and repeat.

---

## 4. Governing documents (ratified 26 Oct 2026, installed and verified at `2db2554`)

All files are in `doc/`. The SHA-256 values are of the Git blobs (LF), checked by Claude with `git show HEAD:<path> | sha256sum`.

| Document | SHA-256 | Role |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_5.md` | `834c0a8e738979ae5bed3527fd946d4f9b0f6a4d77dcbf6d087f1437db731d58` | Charter and philosophy; A-01..A-37, D1-D5; E_1-E_6 definitions |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_4.md` | `1a1853570197a4a62a7d5695417848aac2de65b5fc83c25a931d936c84e05ef4` | Data, views, N-1, method contracts; I-, R2-C, R2-D, T-01..T-39; section 5.5 E_1 goldens; absorbed ERR-R2-01..06 |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_4.md` | `78e2818ab71f6fce68cf1b39b24f5d0f2ad5563f7143b4358a3bcf5b6d49c752` | Evaluation, TOP/WORST, rank position, holdout, freeze-to-score |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_7.md` | `6c7ba2bc1da0d7b1f81e6e2e62e7c1e69448122bdf149399ae560f0c361b7218` | Wrappers, coordinator, 5A.2 installer, **5C process safety (protected)**, W-01..W-25, A-01..A-26, O-register, 20A |
| `Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_2.md` | `2f3ac0e82dfd159025c3933ba41e812a4af0254da13e56664ed36dd5c5dcb61c` | Package 2 v0.11 work W1-W6; invariants M-INV-01..07 |
| `HOLDOUT_EXPOSURE_RECORD_v0_2.md` (ratified 26 Oct, at `ac01678`; supersedes v0.1 `a9806449...`) | `aec833fe031b6d1d73e6acbb81757b50b193425a6899c84d438431d9df4433e2` | Factual, value-free exposure record (6 items, section 5) |
| `Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_5.md` (ratified 26 Oct, at `ac01678`) | `c6ca2cb2174ee2963a6fe33347820c80b92e6dd1eda518a1f0c8e3254d67ab19` | Method ranking measures. **Ratified, pending integration** into R3/R2/Architecture/Proposal (section 12A). It is the approved record until then. |
| `NUMERICAL_INTEGRITY_AND_RETRAINING_REFERENCE_v0_1.md` | `51bcc84bc2ce4c2eda9c99008e75817f85e3f17ef12fc6639c1be6fd0ac3108d` | Non-normative guidance; R2/R3/Architecture prevail |
| `RATIFICATION_REGISTER_v0_3.md` | `99e75fbe1bc5cea34a7d2b1c456633815b88e340c4a05aab5fb671d624c7ec37` | Lineage and status; its own hash lives outside it; 17 historical hashes retained |

**Unchanged and still governing:**
- `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` (`19809ae8a1aca716c6c6a4de71a37b705129304894a2b382036d51b76575b99f`);
- `contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md` (`045b784d16a4611ac4ba5e8af063733e957b0b9359882d52b7143b912a65a0b6`);
- `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_2.md` (POC P0-P2 history, subject to Architecture 5C).

Proposal versions v0.2-v0.4 are in `doc/` as history (v0.1 was never committed). ChatGPT's reviews of the ranking proposal are in `review/`:
- `MR_v0_2_ChatGPT_Independent_Review_v0_1.md`;
- `MR_v0_3_ChatGPT_Focused_Spotcheck_v0_1.md`;
- `ChatGPT_Focused_Review_Method_Ranking_Measures_v0_4_v1.md`.

Claude's response `Claude_Response_ChatGPT_MR_v0_2_Review_v1.md` (`45c7b352...ca3b`) was delivered to the owner, and may not be committed.

The interim note `doc/Interim_Handover_Note_for_both_claude_and_chatgpt_v1.md` (`a46866ca...a1e5`) is superseded by v10 and coder handover v1.1.

**Installation ZIP:** `review/Predictive_Randomness_Governing_Documents_v0_4_OWNER_RATIFIED_INSTALL_CLAUDE_RECHECK_r1.zip`, SHA `178208c6fef7fcb5685cc1572d64f809dae34a6936d6f61ab721ab17623ec2d3`. A byte-identical copy is `review/Ratified_Governing_Documents_Install_r1.zip`.

**Precedence details:**
- **R3 ratification wording (Claude's recommendation, accepted):** provisions labelled `[R3-PROPOSED]` are ratified as written, and OPEN items remain undecided. The first install package said R3-PROPOSED stayed unapproved, which would have de-ratified R3; Claude caught it and r1 fixed it.
- **R2 statuses:** R2 `[PROPOSED]` / `[RECOMMENDED]` items keep their labels unless they are owner-decided elsewhere. An omission or a software default is not a decision.
- **Historical files** (kept, not operative):
  - Proposal v0.3/v0.4;
  - R2 v0.3 plus `..._R2_v0_3_Approved_Erratum_v0_2.md` and `..._R2_v0_3_Erratum_Record_v0_3.md`;
  - R3 v0.1-v0.3;
  - Architecture v0.2-v0.6;
  - P3 v0.1;
  - Register v0.2;
  - TIE v0.1;
  - `doc/experiments/P3_E1_..._REVIEW_CANDIDATE.md`.
- **Byte-identical through consolidation (protected; never edit casually):**
  - Architecture 5C;
  - R2 section 7 (method inventory) and 4.1;
  - R3 0.4, 2.4 and 3;
  - Proposal E_1-E_6.

**R1 method families:**
- E_1-E_6: the originals;
- E_7-E_16: frequency/Bayesian/regime;
- E_17-E_22: recurrence;
- E_23-E_32: within-draw/drawn order;
- E_33-E_40: spectral/curve;
- E_41-E_48: information/nonlinear;
- E_49-E_54: ML/external (E_54 uses date covariates);
- E_55-E_56: ensembles;
- E_57-E_62: pilot-wave.

E_14 and E_54 use dates. The proposed E_63 (Chebyshev/minimax, the owner's idea) is NOT registered; it needs an owner decision (an R1 addition or an E_37 variant).

---

## 5. Settled decisions - do not reopen without substantive cause

### Data
- **Boundary (P1, ratified):** quarantine from **2026-08-01**. Powerball >= 1577 and Oz Lotto >= 1694 are quarantined.
  - Development is Powerball 1144-1576 (433 draws) and Oz Lotto 1474-1693 (220).
  - The derived dates of the first quarantined draws are 2026-08-06 and 2026-08-04.
  - Development targets never exceed 1576 / 1693.
  - The walk-forward target windows (Powerball 1145-1576, Oz 1475-1693) are maxima pending preregistration (OPEN).
- **FINAL_HOLDOUT_10 (P2, ratified):** Powerball 1577-1586 and Oz Lotto 1694-1703.
  - The old ratified Powerball 1578-1587, `DEV_TO_DATE = 2026-08-07` and the Oz "ten highest in first snapshot" rule are withdrawn.
- **E_1 exception (P3, ratified):** the target-1577 regression is forecast-only.
  - It trains on 1144-1576, and the 1577 outcome is never read.
  - No score is computed, and it is not a holdout result.
- **Drawn order (P4, ratified):** the published sequence is treated as the operator's drawn order.
  - Status label: `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`. Reports say "published drawn order (assumed operator order)".
  - The owner recalls seeing the order on TV. It is not a verified physical order, and the set and order views of the same rows are not independent samples (R2 I-09).
- **Source:** Lotterywest's own results-search page on `www.lotterywest.wa.gov.au` (accepted as official), read by an honest, unmodified headless browser, pausing >= 2 s between page loads.
  - **No API of any site.**
  - `oz.lotterywest.com` blocks automation (Cloudflare) and is never contacted.
  - **No browser impersonation and no bot-protection bypass.**
- **Oz Lotto supplementaries (changed by the ranking proposal, ratified 26 Oct; integration pending):**
  - They may be read **by the evaluator only**, after a target is opened and its forecast is frozen, solely to classify prize divisions.
  - They stay out of every method view, fit, seed, digest and prediction. Methods never forecast supplementaries.
  - Until integration, the older governing text ("provenance only") still stands in R2/Architecture/Proposal. The ratified proposal records the change.
- **The Lott:** honest automation gets "0 draws found", so The Lott is used only through pages the owner saves by hand outside the repository (`*.mhtml` git-ignored), as a private verifier.
  - Nothing derived from it is committed. Lottery Corporation terms: browser-only personal use, no reproduction.
  - There is no manual Lott check in production (owner-decided).
- **One master per game:** `source_data/<GAME>_results_master.csv`.
  - Headers: Powerball `Draw_Number,Date,Drawn_1..Drawn_7,Powerball`; Oz Lotto `Draw_Number,Date,Drawn_1..Drawn_7,Supp_1..Supp_3`; the numbers are in drawn order.
  - Alongside it: `<GAME>_results_master_ledger.csv` (append-only), `<GAME>_results_master_init_verification.json` (value-free), and create-only `source_data/backups/` and `grabs/`. Everything is committed.
  - The master is a versioned, mutable-current file with immutable evidence. Every run pins the master version and SHA from the ledger.
  - Updater defaults: the current month plus the previous 5; `--months-back` up to 60.
- **The owner will NOT run `results_master update`, even to test.** It is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised.
- **Masters committed** at `d30fb03`; the old `*_20261021.csv` files were removed at `dadf8e4`.
  - The old files are still in history: `git show 06f6e0f:...` gives a pre-boundary E_1 fixture, but **only through a raw first-field filter (draw < 1577) before any CSV parsing**.
  - `.gitattributes` contains `source_data/** -text`. This is needed because the owner's git converts line endings; never change it.
- **Dates only.** Lotterywest's live-draw page says draws are "approximately 8:30pm AEST (9:30pm AEDT)", which is 10:30 UTC.
  - Masters record ISO dates; there are no invented times or time zones.
  - An optional timing sidecar is deferred.
- **No pre-April-2018 draws**, including for a Powerball-only analysis (Proposal 3.1; D4 rejected). A future rule change stops the programme pending new policy.
- **Exposure record (6 items, value-free; v0.2):**
  1. Powerball 1585-1588 were shown in the reviewer chat on 25 Oct.
  2. The old CSVs contain quarantined rows.
  3. Commit `9b78b8f` contained a saved page showing recent quarantined draws.
  4. The owner's saved Lott pages showed the latest-draw panel.
  5. R1 v0.4 and Proposal v0.3/v0.4 quote the Draw 1587 results, and Claude's consolidation diffs displayed that paragraph more than once.
  6. On 26 Oct, during ChatGPT's review of ranking proposal v0.2, a web search for game rules returned an unsolicited preview containing quarantined values. ChatGPT reported not opening the page or using the values. Claude's own searches that day showed no quarantined values; only Lotterywest game pages were opened.

  Item 5 covers every such display. **Never repeat those values.** Disclose rather than re-seal; make no claim about influence either way.

### Scientific contract
- **Strict N-1:** target N sees only eligible draws with `draw_number < N`.
- **Seeds and content identity** come from the permitted training-view digest, never the whole-file hash. The mandatory perturbation test is **T-05**: change N and every later row, and the forecast for N must stay byte-identical.
- **Views:** `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC`.
  - The caller declares which; there is no entitlement registry.
  - Paired views never double-count.
  - The scientific result-consumer allowlist exists and is **empty**.
- **New view schemas** for any game bind `game_id`, era and profile version. The sole exception is the legacy `E1_REAL_U_TRAINING_VIEW_V1`.
- **Dates are opt-in** (`include_dates=False` by default). Using them creates a new schema and digest; the E_1 digest stays frozen.
- **Numerics (owner decision, 25 Oct):**
  - `int64` for every integer field, in the reader's internal table and in every returned DrawView; `float64` for floats.
  - Views are byte-backed, own their prefix-only copies and are read-only, with no `.base` path to later rows. Test: `47*47 == 2209`.
  - Python `int` for exact counts beyond int64; higher precision where the evidence warrants.
  - A wide dtype alone is not proof of correctness.
- **Fresh fit for every target** on the eligible prefix.
  - An incremental cache or warm start needs a reviewed byte-identical comparison with from-scratch fitting.
  - A past target is never refitted with later draws.
- **TOP and WORST from one frozen ranking.** WORST = the last seven / last one positions of that ranking.
  - Native joint-set TOP is preserved; its WORST comes from marginals (`INVERSE_FROM_MARGINALS`), otherwise `INVERSE_UNAVAILABLE`, never fabricated.
- **Ties at prediction time:** `TIE_SHA256_V1`, a hash of (training-view digest, target, method, variant, barrel, readout version, label).
  - Encoding: a 4-byte unsigned little-endian length plus UTF-8; integers in base-10 ASCII; digests 64 lowercase hex.
  - Measured: E_1 count ties decide the 7th/8th place in 63% of targets and the Powerball top place in 14%. So an ascending-label rule would have biased results.
- **Rank position** (evaluation only; never affects predictions) = the mean mid-rank of the 7 drawn numbers and the Powerball's mid-rank.
  - Chance values: Powerball 18.0 (SD about 3.46) and 10.5 (SD about 5.77); Oz Lotto 24.0, with the PB channel ABSENT.
  - Tied scores get mid-ranks, which never alter a frozen forecast. It is reported in addition to TOP/WORST at the owner's request.
- **Status vocabularies are separate:**
  - benchmark (R2-C20): `SUCCESS`, `TIMEOUT`, `ERROR`, `INSUFFICIENT_HISTORY`, `BLOCKED_DEPENDENCY`, `NUMERIC_INVALID`;
  - evaluation (R3): `RUNTIME_FAILURE`, `INSUFFICIENT_HISTORY`, `DIAGNOSTIC_ONLY`, `NOT_IMPLEMENTED`, `INVERSE_UNAVAILABLE`, `PREDICTION_AVAILABLE`, never collapsed;
  - per-game registry: `SUPPORTED` / `FORMULA_OPEN` / `UNSUPPORTED_FOR_GAME`, with a structural reason. Oz has no Powerball barrel; never zero-pad one.
- **Weekly FINAL batch:** every runnable method and variant, TOP and WORST, with statuses, committed and pushed before the draw. Nothing is added afterwards. A reported hit is shown with its reference chance rate as context only.
- Real forecasting starts after modelling is finished (owner's choice). The scoring measures are fixed before the first real forecast (T-39).
- **Synthetic firewall:** synthetic studies may inform disclosed design. Synthetic data, states and scores never enter real fits, predictions or scores, and never exclude a method.
- **Evaluation windows (R3):** `DEV_ALL_ELIGIBLE`, `DEV_LAST_100/50/10`, `FINAL_HOLDOUT_10`, `PROSPECTIVE_ALL` / `PROSPECTIVE_LAST_K` (not yet authorised).

### Multi-game rules (ratified 24 Oct; carried into the 26 Oct set)
- Two games, one per run, selected by `--game`. Profiles are a frozen Python module, with no free-form barrel parameters (M-INV-06) and no generic engine.
- Identity = the pair (`game_id`, `draw_number`). `draw_key` (e.g. `POWERBALL_1576`) is display-only, and `game_id` matches `[A-Z][A-Z0-9]*`.
  - Legacy Powerball records without `game_id` are read through a versioned compatibility rule and never rewritten.
- Time axis = `draw_number`. Derived weekly date = era start + 7 x (N - first draw).
  - A source/derived date mismatch gives a value-free warning and **halts E_14/E_54 (and date-using equivalents) for that game only**, pending an owner decision.
  - The N-1 loaders never parse future rows to audit dates.
- Separate namespaces per game for results, synthetic runs, masters, ledgers and holdouts. No cross-game pooling or covariates without a preregistered, owner-approved design.
- A method-generic runtime contract must replace the E_1-specific conventions **before E_2** (Architecture 20A; P3 W5).
- **Not authorised:** any Oz Lotto method execution; modifying any frozen Powerball result.
  - OPEN: the E_54 feed contract, the first real Oz experiment, the start of each game's FINAL track, cross-game features, and walk-forward preregistration.

### Ratified 23 Oct 2026
- **Process safety:**
  - strict no-status/no-kill;
  - a persistent orphan interlock with manual clearance (no CLI bypass);
  - the status PID is block-only;
  - failed-group result firewall: results of FAIL or orphan-suspected groups are never consumed, even if `canonical_result.json` exists.
- **E_1 D1:** the first variant is `FULL_HISTORY_RAW_COUNTS_V1`. **D2:** `TIE_SHA256_V1` as above.
- **D3:** real historical development may run in parallel with unfinished P2, standalone via `Run_Experiment.bat` only, with the holdout sealed, no FINAL and no termination. Each real gate is separately authorised.

### Engineering
- **Architecture 2:** one standalone `.py` per method (`src/methods/E_###_name.py`), shared reviewed `_common/` source modules (no shared process or mutable state), and a small coordinator.
- **Option F is the single launch interface:**
  - coordinated: `Run_Coordinator.bat` -> Python coordinator -> **`Run_Experiment.bat` per experiment** -> method `.py`;
  - manual: `Run_Experiment.bat` -> method.

  There is no second production launcher. ERR-R2-02 / Option F has **provisional** production acceptance until the owner-run P1/P2 gates pass.
- **Wrappers:** explicit venv checks; scoped `CALL` activation when inactive; `SETLOCAL`/`ENDLOCAL`; the explicit `.venv\Scripts\python.exe`; forwarding via `%*`, never rebuilt from `%1..%9`; AutoRun checked in the registry (no `/D /C`); the `SAFE_ARG` restriction.
  - The coordinator refuses to start unless `VIRTUAL_ENV` and `sys.prefix` both match the project `.venv`.
- **Concurrency:** 1-6 workers, default 6; one numerical/BLAS thread per worker; no nested pools. The old 12-worker condition was withdrawn.
  - Benchmarks (all Powerball, never crossing the quarantine):
    - B1: target 1576, trained on 1144-1575;
    - B10: 1567-1576;
    - B1-short and B10-short: W=100 (B1-short trains on 1476-1575).
- **Dependencies:** `install_upgrade_dependencies_into_venv.bat` is the sole human-maintained package list. The default is **INSTALL+UPGRADE** (the owner's explicit choice); VERIFY, INSTALL and UPGRADE are also supported.
  - Its Architecture 5A.2 requirements 1-7 cover:
    - `SETLOCAL`;
    - `.venv\Scripts\python.exe -m pip`;
    - the full list shown;
    - `pip check` with a nonzero exit on failure;
    - a generated snapshot;
    - a numerical-change notice;
    - environment and exit status preserved;
    - CRLF.
  - `requirements.txt` is historical.
  - **After EVERY upgrade, STOP** until the offline suites, numerical boundary and N-1 tests, the W-suite including W-23, and all E_1 goldens pass. Goldens are never "recalibrated".
  - **No upgrade between freezing and scoring a forecast, or within Mode H** (R3-T50).
  - Owner-reported environment (baseline for the first post-upgrade comparison): Python 3.14.8, psutil 7.2.2, NumPy 2.5.4, SciPy 1.18.1, threadpoolctl 3.7.0, selenium 4.51.0.
- **Timing (OWNER-DECIDED 24 Oct; human speed):**
  - `POLL_SECONDS_DEFAULT/MIN/MAX` = 1.0/0.5/5.0 (`--poll-seconds`);
  - `PIPE_EOF_WAIT_SECONDS` = 5.0;
  - `RELEASE_POLL_SECONDS` = 0.5 (must equal `POLL_SECONDS_MIN`; tested);
  - `RELEASE_WAIT_SECONDS` = 15;
  - one shared blocking `messages.get(timeout=...)` helper;
  - capture throttle = the poll interval;
  - line-buffered logs.
- **Process termination (Architecture 5C, protected):**
  - psutil only. **No Windows Job Objects** (the owner objects) and **no `taskkill`**.
  - Ownership is proved by ancestry captured while the wrapper root is alive (PID plus creation time). Kill only retained `psutil.Process` members, and the root only via its `Popen` handle.
  - The status file is evidence that can only block. When uncertain, leave the process running and report `UNVERIFIED` / `ORPHAN_SUSPECTED`.
  - If anything is unconfirmed, publish the no-overwrite, fsynced `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json`. **Any entry at that path blocks all launches for both games**, and only the reviewed manual clearance procedure removes it.
  - Experiments may not start child processes in the first release.
- **The three switches stay False:**
  - `ENABLE_PROCESS_TERMINATION`;
  - `ENABLE_SCIENTIFIC_COORDINATION`;
  - `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`.

  No CLI override. Only the owner flips them, after non-destructive tests.
- **Testing order:** non-destructive tests first (decoys, plan-only, forged status). Destructive tests one at a time afterwards, each separately approved.
- **No-clobber publishing:** `os.rename` (raises `FileExistsError` on Windows). Never `os.replace` for frozen results.
- **Batched implementation plan (planning only):**
  - pilot E_1-E_6 (earlier notes differ between one at a time and E_2-E_6 as one batch; settle this when E_2 is scheduled);
  - then batch by R1 family, with a lead method verified first;
  - an automatic contract-test harness, whose verifiers derive expected results from the specification, not the code;
  - heavy methods (E_12, E_38, E_52, E_53, E_57-E_62) individually;
  - ensembles last.

---

## 6. Verified technical facts (sources were checked; reuse rather than re-derive)

- **The Windows venv `python.exe` is a redirector** (CPython `PC/venvlauncher.c`).
  - It starts the real interpreter as a second process, inherits stdio, returns the exit code, uses a kill-on-close job with silent breakaway and ignores Ctrl+C.
  - So `Popen.pid` is not the interpreter's PID. This is never relied on.
- **Windows does not kill children when the parent dies** (Microsoft, "Terminating a Process"), and `TerminateProcess` is asynchronous.
- **A `.bat` launched via `Popen`** runs under `cmd.exe`, and arguments are parsed by CMD without Python escaping (gh-114539). Hence `SAFE_ARG`.
- **`cmd /C` quote stripping** (Microsoft docs) is why `/D /C` was withdrawn and AutoRun is checked in the registry. CMD `%1` splits at `= , ;`, so use `%*`.
- **CPython 3.14 `activate.bat`** runs `chcp.com`. Under the coordinator, children inherit `VIRTUAL_ENV`, so there is no activation and no `chcp`.
- **The `Run_Experiment.bat` process tree:**
  - root `cmd.exe`;
  - a pipe gives a child `cmd.exe` plus `findstr.exe`;
  - a pre-check `"%PY%" -c` (redirector plus interpreter);
  - then the experiment's redirector and interpreter.

  The allow-list is `cmd.exe`, `findstr.exe` and `python.exe`.
- **psutil 7.2.2 (source read):**
  - `children(recursive=True)` filters by creation time against the root only, hence the per-edge check;
  - `kill()` / `terminate()` call `_raise_if_pid_reused()` (PID plus creation time);
  - `Process.wait()` on Windows waits by PID with no reuse check;
  - `wait_procs` returns (gone, alive);
  - the peak-memory field is `peak_wset` in 7.x and `peak_rss` in 8.0.
- **Lotterywest results search:**
  - `https://www.lotterywest.wa.gov.au/results/<powerball|oz-lotto>?fromDate=Ddd+Mmm+DD+YYYY&toDate=...&filterByGame=<5132|5130>`;
  - at most 100 draws per search;
  - per draw: `Draw N`, the date, `Winning numbers:` 7, then `Powerball:` 1 or `Supplementary numbers:` 3;
  - robots.txt allows all; it works under honest headless Selenium.
- **The Lott saved pages:** read only `section.results-search default-results`. The Drawn toggle (`.ball-order button`) is active when it has `disabled`. The latest-draw panel shows quarantined draws and must never be read.
- **Line endings:** Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text` (byte-exact). Hash governing documents via `git show HEAD:` blobs, because the owner's working tree may be CRLF.

**Reference figures (fair-draw model, context only):**
- Powerball main matches: mean 1.4, SD 0.9604; P(>=4) = 0.01826 (about 1 in 55); P(>=5) = 0.00121 (about 1 in 827). Powerball: 0.05 per draw.
- Oz Lotto main-match mean: 49/47 (about 1.0426).
- Chance hits per weekly Powerball batch (independence assumed, an overestimate where methods are correlated):

| Batch | Some 4+ main hit | Some 5+ main hit | Powerball hits per week |
|---|---|---|---|
| 62 forecasts | about 68% of weeks | about 1 week in 14 | about 3.1 |
| 124 forecasts (TOP + WORST) | about 90% of weeks | about 1 week in 7 | about 6.2 |

---

## 7. Current implementation status (verified at `2db2554` unless marked)

**Phase:** Phase 1 (development). Package 2 v0.11 is next (ChatGPT, fresh chat); it has not been written or started. Science is paused until the reader is accepted: the Powerball walk-forward, E_2-E_6, and any Oz work.

**Powerball E_1 (accepted; frozen):**
- `src/methods/E_001_Historical_Appearance_Frequency.py` (`9ce866e4...`; standalone since commit `fbb66efe`) with these `_common` modules:
  - `e1_historical_appearance_frequency_v0_3.py`;
  - `e1_training_view_v0_1.py`;
  - `e1_standalone_contract_v0_1.py`.
- Tests: `tests/test_p3_e1_standalone_v0_1.py` and `tests/p3_e1_synthetic_v0_3.json`.
- Goldens (R2 5.5):
  - synthetic training view: `df21871f8067e5405b4fdb1eec50c65dddbaa35958872bad3230d3c10a791fd4`;
  - synthetic MAIN label-3 tie: `7ce5ab1bae014adf61f1f02dd152d4b500cb405b65cb3886cdcee8dd9e2c9932`;
  - synthetic canonical forecast: `7b43d659d611791deb14d106a72984f153d9f79cc63b3d25000365de4c811d1e`;
  - real target 1577 (forecast-only), view: `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339`;
  - real target 1577, legacy canonical result: `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e`.
- Frozen **forecast** outputs (not outcomes): TOP `[9,17,7,11,18,30,12]` with PB 2; WORST `[31,13,8,29,26,33,35]` with PB 12.
- Claude reproduced the real hashes and has deliberately never computed a 1577 score.

**Coordinator:** `src/Powerball_Experiment_Coordinator.py`, v0.6, `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`, with the switches False.
- Eleven protected functions must stay AST-identical:
  - `accept_ancestry_candidate`;
  - `check_exited_worker_for_orphan`;
  - `departed_members_check`;
  - `read_status`;
  - `record_unresolved_orphan`;
  - `register_root`;
  - `require_no_unresolved_orphan`;
  - `save_new`;
  - `status_and_result`;
  - `status_orphan_evidence`;
  - `terminate_owned_tree`.

  This list comes from ChatGPT's v0.10 evidence. v0.10 changed `capture_owned_tree`, `read_lines`, `arguments` and `coordinator_main`, and added `receive_messages`.
- The 3 s termination-path waits stay.

**Package 2:**
- v0.9 was reviewed (review v2 committed).
- v0.10-r1, `review/Predictive_Randomness_MultiGame_Package2_v0_10r1_OWNER_VIEW_DECISIONS_CLAUDE_REVIEW.zip` (`f1db9629f4735f25de357a991a98748abffe0f53ed58efb03e11991b972cf45b`), was reviewed in `review/Claude_Review_Package2_v0_10_r1_and_Direction_v3.md` (it supersedes v1/v2). Findings:
  - **C1:** an N-1 leak via a NumPy slice `.base`. Fix with owned byte-backed prefix copies, int64/float64, poisoned-suffix tests.
  - **C2:** the method boundary. Methods get views only; the per-run parse is prefix-only, bound to the ledger version and SHA; reject links; static import checks; value-free errors.
  - **C3:** dates exposed but not digested. Make them opt-in with a new schema.
  - **C4:** the "exact" coordinator diff does not reproduce the shipped file. Regenerate it mechanically from `2e23d550` and rerun the AST proof.
  - **C5:** a pre-build 1577 forecast-only regression from master v1 or `06f6e0f`, with a raw first-field filter.
  - **C6:** name the 0.12/0.05 literals in `read_lines`, the `coordinator_main` `finally` and `multigame_windows_lifecycle_v1.py`; add the `RELEASE_POLL == POLL_MIN` test.
  - **O1:** a raw filter before `DictReader`. It is in `multigame_results_build_v1.py`, so it is closed by retirement.
  - **O2:** owner-supplied pre-boundary current-era Lotterywest page fixtures; optional and deferred.
  - **O3:** `requirements.txt` is historical.
- **Retire from the v0.11 overlay:**
  - `lotterywest_api_client_v1.py`;
  - `lotterywest_results_v1.py`;
  - `lotterywest_saved_pages_v1.py`;
  - `multigame_results_build_v1.py`;
  - `multigame_results_tool_v1.py`;
  - `Run_Scraper.bat` (not at HEAD; only in the overlay);
  - `multigame_source_policy_v1.py`, unless still imported;
  - tests unique to these.

  Keep the old Powerball scraper `src/scrape_australian_powerball_history_from_2018_04_19_v0_3.py` as history.
- The reader sets `order_verification_status = OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`, citing the init record's file name and the master SHA. It does not decide this itself.

**Claude-written, owner-run tools (do not let ChatGPT rewrite or invoke them):**
- `src/two_site_results_check_v0_7.py` (`69cb1decb1a1fed4077ccb41b91607405805721795992f57f302ae6618759aed`; self-test 14/14). Modes: `--build-history`, `--offline-dir --against-run`, `--pick-lott-sample`, `--diagnose-lotterywest`.
  - A hard quarantine STOP comes before any numbers are read; reports are value-free; runs go to the git-ignored `private_results_checks/`.
  - v0_2-v0_6 are historical.
- `src/results_master_v0_1.py` (`3436da9f560172606f4b9e010cd85a806b58e55597685f2ab7f65c3e17523619`; self-test 9/9; fake-browser scenarios 9/9) with `Run_Results_Updater.bat`.
  - `init` (offline, done) re-verified the build and Lott runs and every row, re-ran the old-file comparison 433/433, wrote create-only and re-read.
  - `update` is gated by `HOLDOUT_OPENED_<GAME>.json`, a lock file, a ledger-hash check, overlap matching, backup, atomic replace and a ledger append. It has never been run.
- **Masters at HEAD:**
  - Powerball `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8` (last row 1576);
  - Oz Lotto `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f` (last row 1693);
  - ledgers: Powerball `5499a9e1...`, Oz `47d479ac...`, each holding only INIT version 1;
  - init records: Powerball `bc3cf72c...`, Oz `3a8decb4...`.
- **Owner's private runs (git-ignored, OWNER-REPORTED):**
  - build `run_20261025T020840Z_5a7fbb`: Powerball 433/433, Oz 220/220, 0 missing/extra/off-date;
  - Lott check `run_20261025T021022Z_714ecd`: Powerball 52/52, Oz 31/31 on every field, including main order.

**Reviewed orphan utilities (`transitory_data/`, committed; do not modify):**
- inspection `606f5e22...`;
- archive `ca42d264...`;
- clearance `08000be1...`.

The 23 Oct real orphan was archived and cleared manually, and a later one-worker P2 fixture passed. That is history, not proof that no marker exists on the owner's PC now.

**Removed 26 Oct:** `src/GAIS/GAIS_results_fetcher_comparer.py`, an unreviewed Selenium scraper of thelott.com and oz.lotterywest.com, committed in `172f221`. The owner deleted it after Claude's handover review (commit `a52ffd8`, verified absent). It stays in Git history and must never be revived.

**Handovers committed at `6726963` (verified):**
- `doc/HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v9.md` (`1c4544ee...dacb`);
- `doc/HANDOVER/Predictive_Randomness_ChatGPT_Coder_Handover_v1_0r1.md` (`07e37284...9a`).

These are replaced by v10 and coder handover v1.1.

**Not done / not authorised:** the updater run; Mode H; FINAL; holdout access; destructive tests; P2 closure; any Oz science; any switch change; Package 2 acceptance.

---

## 8. Coordinator review history (still relevant)

- **v0.3 fixed** two defects:
  - departed members are retired, and newcomers are re-verified; an alive or unverifiable old identity gives `MEMBER_PID_IDENTITY_CONFLICT`;
  - a bounded 3 s `wait_procs` on processes told to stop.
- **Open optional notes:**
  - (a) the logged `alive=` count can overstate because psutil's Windows `wait()` has no reuse check; log identity-checked survivors instead;
  - (b) build the verified-parent list from `_member_alive(m) is True`.
- **The owner retained the stricter rule** (no termination unless identity is positively verified against both status and ancestry). The owner also approved manual marker clearance. Do not reopen either.
- **Still relevant:**
  - transient anomalies permanently block termination; consider separating hard from benign anomalies;
  - the smoke suite's `subprocess.run(timeout=120)` can kill the coordinator's `cmd.exe` by handle, bypassing the switch, so the default suite is not strictly kill-free;
  - with the switch False, a console Ctrl+C is a near-non-destructive test of W-10/W-18.
- Orphan interlock v0.4-v0.6 and the clearance utility were reviewed on 23 Oct. Quirk: `--check` returns HOLD after a successful clearance (marker absent), as expected.

---

## 9. Document consolidation (25-26 Oct) - lessons

- **v0.1** kept contradictory old layers (3 blockers).
- **v0.2** over-condensed and lost ratified substance (3 blockers).
- **v0.3** edited in place, which worked, but lost the multi-game rules that had no IDs (1 blocker).
- **v0.4** passed. The install package needed one correction (the R3 line 37 wording); r1 passed. The documents were verified at `2db2554`.
- **Lessons for future document reviews:**
  - Check IDs mechanically **and** search separately for rules without IDs.
  - Diff ratified against candidate line by line.
  - Confirm that protected blocks are byte-identical.
  - Check that ratification wording does not de-ratify anything.
- **Claude's own misses, to avoid repeating:**
  - Claude passed P3 v0.1 in the v0.1 review but missed that its M-INV-01..07 invariants had been dropped (caught in the v0.2 review).
  - A count of 108 R2 IDs wrongly included "N-1"; the correct count is 107.

---

## 9A. Lessons from the ranking-proposal review rounds (26 Oct) - Claude's own errors

ChatGPT's reviews caught real errors in Claude's drafts. Each was checked independently before being accepted.
- **Global sigma (v0.1-v0.2):** Claude used the Sidak formula, which assumes independent tests. It can be anti-conservative: two mutually exclusive events of 0.05 have a true family error of 0.10, but Sidak gives 0.0975. **Bonferroni over valid p-values is the safe default.**
- **Simulator claim (v0.3):** Claude claimed that replaying fair draws against stored adaptive forecasts calibrates everything. It does not.
  - For cross-track maxima: a 4-draw exhaustive toy gives a true probability of 1/16 but a replay of 15/128.
  - For forecast-weighted measures: also wrong.
  - Claude's own salvage, verified: the replay **is exact for single-track statistics built only from the track's hit codes**, because the fair law of match counts is the same for any ticket.
- **Scored-set selection (v0.4):** even that holds only on an **opportunity grid fixed independently of the outcomes**. A stopping rule at a nominal 5% boundary over at most 20 draws is crossed under pure chance with probability 6467/65536 = 0.0987 (reproduced).
- **Smaller errors:**
  - overgeneralising one E_1 simulation into a rule for all methods;
  - calling a threshold ratio a "detectable effect";
  - a redundant tie-break;
  - one wrongly rounded odds entry (Lotterywest rounds its published odds **up**);
  - "0 wins = 0 sigma" needing "excess".
- **Lessons:**
  - Verify every counterexample and every number by exhaustive enumeration or exact computation, both ways.
  - State the exact conditions under which any "exact" or "calibrated" claim holds.
  - Prefer marking over suppressing.
  - When ChatGPT leans towards suppression, propose labelling instead (it agreed each time).

---

## 10. ChatGPT coder handover (26 Oct)

- **ChatGPT Coder Handover v1.0** (`1f4db07e...`; package `c6c0ad9c...`) was reviewed in `Claude_Review_ChatGPT_Coder_Handover_v1_0_v1.md` (`d50b147c8f87176eb3b34dd21d1805098582cc0ca7b4cf5f9027cd4304908e0b`). Verdict: **accept after corrections; no blockers.**
- **C1-C8:**
  - **C1:** state the verified HEAD.
  - **C2:** the GAIS script (now deleted by the owner), and that `oz.lotterywest.com` is never contacted.
  - **C3:** the timing constants are OWNER-DECIDED, plus the C6 wording.
  - **C4:** tie-breaking vs mid-ranks; separate the status vocabularies; add the WORST inverse rule.
  - **C5:** other eras are excluded, not OPEN; O2 is pre-boundary current-era.
  - **C6:** reviewer handovers v2-v8 are historical.
  - **C7:** the verified inventory.
  - **C8:** the O1/O3 dispositions.
- Optional items O1-O8 were also listed.
- **Outcome:** v1.0r1 passed Claude's focused spot-check (own diff; ChatGPT's diff reproduces it). The owner accepted it, and it was committed at `6726963`. ChatGPT is now writing **v1.1**, a full document built from v1.0r1 plus the ranking work and section 2A.
- **Adopted from ChatGPT's handover:**
  - **Evidence classes:** keep these apart in every review:
    - ratified rule;
    - later owner decision;
    - Claude recommendation;
    - committed code;
    - review candidate;
    - owner-reported run;
    - locally repeated verification;
    - OPEN.
  - **Questions to answer in every v0.11 code review:**
    - Did the reader ever decode row N?
    - Can `.base` or method imports reach forbidden data?
    - Can a bad hash or an alternate link bypass the pinned ledger?
    - Does any numeric field narrow below int64/float64?
    - Are the E_1 goldens unchanged without the outcome?
    - Are the wrappers and the protected kill functions unchanged?
    - Can a failed or orphan group feed a downstream result?
    - Can a synthetic result pass as science?
    - Is any of the three switches non-False?
    - Do the owner tools and the retired acquisition code stay separate?
    - What was actually executed, by whom, on which OS, at which HEAD?
  - **Mode H storage stays OPEN:** a separate outcome store released one by one, or a versioned master isolated by the parser. Claude's earlier suggestion (update the master after opening) is a proposal only.

---

## 12A. Method ranking measures - ratified proposal v0.5 (summary; the proposal itself governs)

**Origin:** the owner's speculative-discussion starter: rank methods by measured success, separately per game, independently of production runs, with prize divisions, periodicity, "due" alignment and sigma, plus up to five further statistical/quantum-linked measures.

**Rounds:**
- v0.1: Claude drafted.
- v0.2: owner decisions on supplementaries and MR1-T.
- ChatGPT full review: 4 blockers and 10 corrections, plus MR6-MR10 proposed.
- v0.3: Claude's response, then all applied.
- ChatGPT spot-check: N1 adaptive blocker.
- v0.4: two-class N1, MR16, side-by-side display, plain mode meanings.
- ChatGPT focused review: the scored-set selection blocker.
- v0.5: applied; **ratified at `ac01678`** without a further round (owner's call, given ChatGPT's chat limit).

**Owner decisions** recorded in the proposal (MRD-01..24); key ones:
- all divisions (Powerball 9, Oz Lotto 7);
- supplementaries for scoring only;
- current-format draws only (the Oz window starts no earlier than 1474);
- rankings never feed forecasts; selection is a registered meta-method (RK-1..6, decided by Claude under delegation);
- the sigma scale with "0 wins = 0 excess sigma";
- the explanation-text rule for every measure, method, status and mode;
- MR1-T (90/7/3) kept;
- MR6-MR10 and MR10.BOTTOM adopted; MR16 adopted;
- N1 kept (R = 10,000);
- Bonferroni over predeclared families, plus a search log;
- defaults: MR13 prior 0.5 (also 0.25 and 1.0), LOW_N below 30, extra Oz measures main-only;
- WF/IS side by side with separate ranks;
- plain-English mode definitions printed word for word.

**Core design (for orientation):**
- **Modes:**
  - **WF**, "honest test: trained on earlier draws only";
  - **IS**, "hindsight fit: trained on all draws, including the ones scored", labelled `IS_NOT_CALIBRATED`, with all numbers shown.
  - They are never ranked together, but are shown side by side on the paired target set, with a comparable quantity per measure (or `NOT_COMPARABLE`) and a "hindsight advantage" column.
- **Numbering:** official draw numbers only; ranks 1 = best; the training set for N is the era's first draw through N-1.
- **Measures:**
  - MR0 division profile;
  - MR1 surprisal score and MR1-T;
  - MR2 recurrence period and MR3 "due" alignment, both on scored-opportunity gaps;
  - MR4 division sigma;
  - MR5 rank position;
  - MR6 log score;
  - MR7 total matches (exact);
  - MR8 streak (exact DP);
  - MR9 early/late change;
  - MR10 top-rank gain and MR10.BOTTOM;
  - MR11 TOP versus WORST (exact sign test);
  - MR12 surprisal;
  - MR13 Bayes factors;
  - MR14 fidelity (exact order-4 variance in draw size K);
  - MR15 Lomb-Scargle;
  - MR16 hit-rate with Clopper-Pearson interval and "observed hit-rate threshold for local 3 sigma".
  - New measures take MR17 onward.
- **Calibration labels:** `EXACT_LOCAL`, `APPROX_UNCALIBRATED`, `N1_CALIBRATED` (hit-sequence class on a fixed grid only), `N1_FIXED_FORECAST_REFERENCE`, `SELECTION_UNVERIFIED`, `BONFERRONI_REFERENCE_UNCALIBRATED`, `IS_NOT_CALIBRATED`, `NOT_A_P_VALUE`.
- **Evidence tiers:** development WF exploratory; holdout (Mode H); prospective; IS descriptive.
- **Analysis units:** readout track; method/variant ranking; probability vector; TOP/WORST pair. Each hypothesis is counted once.
- **Contract fields** (proposal section 13, stage 1), needed before E_2:
  - per-channel probability kinds;
  - IS capability;
  - registry texts;
  - independent readout states;
  - the evaluator-only outcome record with Oz supplementaries.
- **Phasing:**
  - stage 1: the E_2-readiness package (after v0.11 is accepted; not in v0.11);
  - stage 2: with the E_1 walk-forward runs and the scorer (MR0/1/4/5/7/16, N1, reports, search log);
  - stage 3: after E_2-E_6;
  - stage 4: meta-methods, only if proposed.
- **Small samples** (Phase 1 windows Powerball 1286-1576 = 291 draws, Oz Lotto 1474-1693 = 220):
  - 3+ main matches needs about 1.5x the chance rate for local 3 sigma;
  - division counts need about 2.4-3x;
  - top divisions are essentially never expected.
- **Illustration, not a test value:** E_1 in-sample on fair draws gains about 3.3 sigma from hindsight alone.

**Integration plan (owner, 26 Oct):**
- **What:** new clean editions R3 v0.5 (largest), R2 v0.5, Architecture v0.8 (5C untouched), Proposal v0.6 and register v0.4. They replace the "provenance only" supplementary wording and carry the proposal's sections as listed in its section 15.
- **Who:** Claude drafts in a new chat; ChatGPT's next chat reviews; the owner ratifies.
- **When:** during Package 2 v0.11, completed **before the E_2-readiness task spec**.
- **Unchanged:** P3 v0.2 and v0.11.
- **Watch for:** keep every ratified ID and rule (the consolidation lessons in section 9 apply), run the stale-phrase and ID checks, and preserve the protected blocks byte for byte.

---

## 11. Review method that has worked

- Unpack every ZIP into its own fresh scratch directory, and run Python on it with `-I`.
- Diff new versions against old ones (`diff <(sed 's/\r$//' old) <(sed 's/\r$//' new)`).
- Check every claim in a handback against the actual files: hashes (`git show HEAD:path | sha256sum`), line endings, file lists, `.gitignore`, and commit existence.
- Extract every 64-hex hash in a document and look each one up in the repository.
- List the whole tree at HEAD and compare it with the claimed inventory. That is how the GAIS script was found.
- Cross-check against the ratified set and quote line numbers.
- Recompute statistics and dates with a short script.
- Read library source when behaviour matters. Use official Microsoft and Python documentation for Windows behaviour, and cite sources.
- For Windows-only behaviour, label the expectation TO-TEST and map it to a W-, A- or T-series test.
- Never let a tool output print a quarantined row or the 1587 paragraph. When diffing documents that contain it, filter that paragraph out first.
- For any statistical claim (calibration, exactness, independence), build the smallest exhaustive toy that could break it, and enumerate it exactly with `fractions.Fraction` (section 9A).
- When reading master data for a non-outcome fact (for example a draw date), print only the fields needed (`cut -d, -f1-2`), never the number columns.

---

## 12. Likely next items

1. **Integration drafting (Claude, new chat):** new editions R3 v0.5, R2 v0.5, Architecture v0.8, Proposal v0.6 and register v0.4, from ratified proposal v0.5 (its section 15). Then:
   - ChatGPT reviews;
   - the owner ratifies;
   - Claude verifies the install.

   Edit in place from the ratified texts (the method that worked in consolidation v0.3/v0.4); check IDs and rules without IDs.
2. **Review Package 2 v0.11** (ChatGPT's fresh chat) against the direction v3 document, P3 W1-W6 and the section 10 questions. Above all:
   - C1/C2 (N-1);
   - the reader bound to the ledger;
   - int64/float64;
   - the E_1 goldens without the outcome;
   - the eleven-function AST proof against `2e23d550`;
   - the retirements.
3. **E_2-readiness task spec,** after v0.11 is accepted: the method-generic contract plus the ranking stage-1 fields. The owner ratifies the field schema.
4. **Resume science:**
   - preregister the walk-forward windows;
   - Powerball walk-forward to 1576, with the scorer and the stage-2 ranking core;
   - then E_2-E_6 (stage 3);
   - then families;
   - Oz Lotto only after a separate owner gate.
5. **P2:** coordinator v0.7 plus a destructive-gate plan; owner-authorised destructive tests one at a time; P2 closure; ERR-R2-02 / Option F final acceptance.
6. **Later:** a Mode H package (frozen study manifest R3-T50, the `HOLDOUT_OPENED` record, sequential release); the production weekly loop (updater -> score the frozen forecast -> retrain -> freeze -> push); rankings over the holdout only after Mode H scoring (RK-6).

*End of handover.*
