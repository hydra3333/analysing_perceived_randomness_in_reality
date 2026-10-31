# Predictive Randomness - WF-1B supplement: the report's order and the seed (with WORKERS-1 deferred to WF-1C), design note v0.1r1

**Document:** a supplement to the ratified releases and WF-1 design (`Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md`, LF `03f95fbe...12ee`, OWNER-RATIFIED 31 October 2026). That design's sections 6 to 8 (the scorer, the report, N1 and the seed) stay the design of WF-1B, unchanged. This note adds only what the owner decided since, and what coding needs settled first.
**Version:** v0.1r1 DRAFT for the reviewer's focused RECHECK, 31 October 2026. It resolves EX_105 (`exchange/EX_105_ChatGPT.md`; RECHECK: 1 BLOCKER, 5 CORRECTION, 2 OPTIONAL) by the owner's decision WB-0 (31 October 2026, after EX_105): WF-1B goes ahead with the report's order (section 3, now with C01's RK-4 disclosure) and the seed (section 6); everything about more workers, the progress line and `compare` moves to WF-1C's own design round, which carries B01, C02 to C05, O01 and O02 as its obligations (section 4). Appendix A maps every finding. v0.1 (`ce4c0249...33d3`) is superseded. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule. Where it proposes a change or a reading, the owner decision is listed in section 9.
- **No code yet:** the code follows only after this note passes.
- **Base:** `main` at `63f4a57` (register v0.22 installed at `2b1e7e3`; the seed announcement EX_103 at `92a6cef`; v0.1 as EX_104 at `b37022c`; EX_105 at `63f4a57`).
- **Inputs:** the owner's directions recorded in register v0.22 ("The owner's directions for WF-1B": the report's order, the progress line, WORKERS-1); EX_101's four obligations for WORKERS-1; Architecture v0.8 (5A.4, 10.1, O-CPU-01, O-POL-03, ERR-R2-01, A-04, A-25); R3 v0.5 sections 7.2, 17.6, 17.9 and 17.10.

## 1. In plain English

**What this note settles for WF-1B:**
1. **The report shows the real results first.** Each league table that ranks methods by what they actually achieved against the real draws (prizes won, numbers matched) comes first. The tables that measure how surprising those results would be under fair random draws come after, under their own heading, "adjusted against fair random draws". Nothing is computed differently; only the order and headings change.
2. **The seed travels with WF-1B** if tonight's NIST pulse passes its checks (section 6).

**What does not change:** the scorer, the measures, N1, the seed procedure, the families and their labels, the holdout and every gate.

**Deferred to WF-1C (decision WB-0, the owner's choice of 31 October 2026):** more workers (WORKERS-1), the batch progress line and the `compare` command. They get their own design round after WF-1B, carrying the review's findings (section 4). Until WF-1C is reviewed, ratified and installed, the coordinator's limit stays 1 to 6 and the walk-forward driver runs one run at a time.

## 2. What stays as ratified

- **The scorer and report:** design v0.1r1 sections 6.1 to 6.9 (the order of a report run, the fixed grids, the downgrade rules, the outcome reader, the records, the measures, the numerics, the families with M = 80, the search log, the report files with no drawn numbers).
- **N1 and its seed:** sections 7 and 8. Until SEED-1's approved policy is installed, the report runs with N1 off and says so (`N1_NOT_RUN`, 7.6).
- **The driver,** unchanged by WF-1B: design section 5.3 and the WF-1A install's attempt binding (EX_083 WF1A-R2-B01).
- **The cohort:** since E_1 revision 2, each game's batch holds 40 variants, so each family has M = 80 (register v0.22, "Out-of-date statements").

## 3. The report's order (the owner's direction; decision WB-1)

R3 already asks for this. R3 7.2: "Every evaluation report begins with what was actually forecast, what was actually observed, the evaluation formula, and its denominator. ... reference p-values, synthetic calibration ... are separate clearly labelled layers." R3 17.6: "Two ranking tables where relevant: a descriptive table (by the raw score) and a significance table (by local Z_plus, with global figures). They are never conflated."

**Proposed layout of the text report** (R3 17.10.2's six parts, with part 4 split and moved up):
1. **Header,** as in 17.10.2.
2. **Part A, "League tables: results against the real draws".** It opens with the RK-4 disclosure block (below), then every descriptive table, measure by measure in R3's order: MR0 (divisions won, best first), MR1 and MR1-T, MR4, MR5, MR7 and MR16. Each is ranked by its descriptive key as R3 17.6 defines it (for example MR7 by S - n x mean0, the matches above the fair-draw average, so that tracks with different n compare fairly). These keys use only the real results and fixed fair-draw averages: no simulated draws and no p-values.
3. **Glossary,** as in 17.10.2.
4. **Fair-draw reference,** as in 17.10.2.
5. **Part B, "League tables: adjusted against fair random draws".** Every significance table: local Z_plus and its label, the exact tails, N1's figures, and the families' global figures.
6. **Per-track detail and notes,** as in 17.10.2.

**RK-4 in Part A (EX_105 C01).** R3 17.9 RK-4 says any report highlighting a top-ranked track shows the number of tracks and tests compared, the global figures and the search-log count. Part A ranks tracks, so it must show them. They go in one boxed block at the top of Part A, titled exactly:

`RK-4 disclosure - global and significance context, not part of the descriptive rankings (full figures in Part B)`

It gives:
- the number of tracks in the cohort and the number of tests counted for the report;
- the search-log counts for the game: `RANKING_REPORT` rows, and how many of them have no completed report; `WF_BATCH` rows;
- for each registered family: its ID, M, its global result exactly as Part B shows it (the Bonferroni figure, shown as guaranteed when design 6.2A's conditions hold and otherwise labelled `BONFERRONI_REFERENCE_UNCALIBRATED`; the N1 maximum statistic with `N1_FIXED_FORECAST_REFERENCE`, or `N1_NOT_RUN`) and the count of tracks that broke the guarantee's conditions;
- the N1 seed policy used (or none) and the number of N1 policies on file.

**This is the one exception to "Part A holds only descriptive figures":** the RK-4 block is the only place in Part A where a p-value, sigma or global figure appears, and it is visibly separate from the tables. The descriptive tables themselves hold no p-value, sigma, calibration label or global figure, and their ranking keys use no significance figure. Nothing is suppressed: every figure in the block also appears in Part B, with the same value and label.

**The CSV and JSON** carry the same rows as now; each row gains a `table_kind` field (`DESCRIPTIVE`, `SIGNIFICANCE` or `RK4_DISCLOSURE`). The text report is the only file whose order changes.

**Why a decision is needed:** R3 17.10.2 lists the glossary and fair-draw reference before the league tables. Moving Part A up is a departure from that order (the content is unchanged), so the register records it. The option is to keep 17.10.2's order exactly and split part 4 into A then B in place.


## 4. Deferred to WF-1C: more workers, the progress line and `compare` (decision WB-0)

v0.1's sections 4 and 5 (the progress line; WORKERS-1's limits, coordinator change, parallel driver, identity definition and `compare`, stop and failure rules, memory and Windows evidence) are withdrawn from this note. They are the starting draft of WF-1C's own design note, which carries these obligations:
- **EX_101's four:** memory headroom; which canonical bytes must agree across worker counts; concurrency failure semantics; the default for odd or unavailable processor counts.
- **EX_105 B01 (BLOCKER):** an atomic admission boundary, no prefetch, at most one outstanding request per worker, a shared STOP and orphan recheck before each run starts, no claim of zero starts after a STOP unless a start protocol proves it, and fail-closed handling of a lost parent: no resume until the owner has established that the affected workers have exited, or an independently reviewed durable interlock gives the same assurance. No kill, no PID-based action, no automatic orphan clearance.
- **EX_105 C02:** `compare` checks the exact master SHA-256, game, targets, cohort, revisions and declarations first (`INCOMPARABLE` otherwise), and records or controls the effective numerical-thread settings.
- **EX_105 C03:** every real-data re-run, and the exact scope of any Windows multi-process test, is a separate owner approval; the Windows interrupt and crash behaviour is TO-TEST until authorised.
- **EX_105 C04:** the 46 MB figure is a limited synthetic Linux observation; the dispatch floor cannot cap peak memory; a staged, owner-authorised Windows check at increasing worker counts comes before 12 is treated as established; an unreadable memory figure stops dispatch.
- **EX_105 C05:** worker-limit tests that do not assume 24 processors (an injected 24-processor environment for the 1, 6 and 12 policy); the 60-worker cap as an explicit owner choice.
- **EX_105 O01 and O02:** the canary's guarantee stated for a persisting global cause only; the progress line counting distinct validated pairs, the 20-run threshold per invocation, and the variant-finished exception to the 10-second throttle.

Until WF-1C is ratified and installed: the coordinator's limit stays 1 to 6 (Architecture v0.8, O-CPU-01), and the driver runs one run at a time (`status` shows progress meanwhile).

## 5. (Removed in v0.1r1; see section 4.)

## 6. SEED-1 and the first reports (decision WB-2)

- **The pulse is brought forward (EX_103, committed and pushed at `92a6cef`, 31 October 2026, 09:30 UTC):** the owner replaced the announced 6 November pulse with the pulse of `2026-10-31T10:30:00.000Z`, under WF1-9 and D-10, an hour before it existed. The new policy is `N1_ROOT_NIST_C2_20261031T1030Z_V1`. The replaced policy was never fetched and stays on file, counted (design 8.4).
- **If that pulse passes design 8.2's checks,** its `APPROVED` `SEED_POLICY_V1` record (design 8.3) travels in WF-1B under `src/evaluation/seed_policies/`, with both earlier records (the replaced and the provisional) as history. Each game's report then runs once, with N1.
- **If it fails a check,** the policy is `REFUSED` and a new pulse is announced the same way (design 8.1). WF-1B then installs without an approved policy, and the reports run with N1's figures labelled `N1_NOT_RUN` and every other figure complete; they are run again once a policy is approved. Every report attempt is a `RANKING_REPORT` row in the search log, and is counted.

## 7. Documentary items

- **EX_080 O03 (non-gating), qualified here:** design v0.1r1's statements that NIST's chain links "hold on two public chain 1 pulses" (sections 8.2 and 9.5) are illustrative, not independently verified. In the probe, the next pulse's `previous` value was set equal to the earlier `outputValue` before being compared, so that comparison is tautological. The SHA-512 relation was really computed, but on values whose archive provenance the probe did not establish. Nothing depends on either: the chain-link check is not part of SEED-1's approval (WF1-12).
- **R3 finding R3-5 (for the next register):** R3 17.10.2's order places the glossary and fair-draw reference before the league tables. WB-1 moves the descriptive tables (Part A) first, as R3 7.2 asks, with RK-4's disclosure block at its top (section 3).

## 8. Tests

**WF-1B:** design v0.1r1 section 10's WF-1B list, plus the order of section 3:
- Part A comes before the glossary and Part B after the fair-draw reference, in the text report;
- every descriptive table precedes every significance table;
- Part A's RK-4 block is present, titled as in section 3, and holds the track and test counts, the search-log counts, every family's global result with its label (each equal to Part B's), and the N1 policy line; a synthetic family that is complete shows its Bonferroni figure as guaranteed there, and one with a failed cell shows it labelled `BONFERRONI_REFERENCE_UNCALIBRATED`;
- the CSV and JSON `table_kind` field, including `RK4_DISCLOSURE`;
- outside the RK-4 block, no p-value, sigma, calibration label or global figure appears in Part A (a scan of the text between the block's end and the glossary), and no table appears in both parts.

**WF-1C:** in its own design (section 4); v0.1's list is its starting draft.

## 9. Owner decisions

- **WB-0 (OWNER-DECIDED 31 October 2026, after EX_105): two packages.** WF-1B (the scorer and report, with section 3's order and section 6's seed) goes ahead now. WF-1C (workers, progress line, `compare`) gets its own design round afterwards, carrying the obligations of section 4. This departs from WORKERS-1's first placement ("WF-1B also replaces ..."; register v0.22), as the owner chose; the next register records it.
- **WB-1 (RECOMMENDED): Part A first** (section 3).
  - Why: you asked for the real-outcome rankings first, and R3 7.2 says the same.
  - Recommended: header, Part A (real draws), glossary, fair-draw reference, Part B (adjusted against fair random draws), detail and notes.
  - Option: R3 17.10.2's order exactly, with the league tables split into A then B in their usual place.
- **WB-2 (RECOMMENDED): the approved seed policy travels in WF-1B** (section 6), if tonight's pulse passes its checks, and each report runs once with N1. If it fails, WF-1B installs without one and the reports run with `N1_NOT_RUN`, then again after approval.
  - Why: no separate SEED-1 package or second report run is needed.
  - Option: a separate tiny SEED-1 package after WF-1B (design section 3).
- **WB-3 and WB-4** (v0.1: the Windows evidence and the limits) move to WF-1C's design (section 4).

## 10. What the reviewer is asked to check (R-3)

**For the focused RECHECK of v0.1r1:**
1. **C01:** that the RK-4 block (section 3) meets R3 17.9 RK-4, is visibly separate from the descriptive tables, matches Part B, and that the tests (section 8) check both the block and the absence of significance figures elsewhere in Part A.
2. **WB-0's deferral:** that section 4 carries every EX_101 and EX_105 obligation into WF-1C, and that nothing in WF-1B depends on WF-1C.
3. **Mark, never suppress:** unchanged from v0.1.

## 11. Not in scope

- Everything design v0.1r1 sections 6.9 and 14 exclude.
- **WF-1C** (section 4).
- **Mode H** (scoring the holdout draws) and **prospective forecasts** (forecasting a draw that has not yet happened). They come next, in their own design, which Claude drafts while this one is reviewed.
- Running anything through the coordinator; Windows lifecycle tests.
- Any change to a method, to the runner, or to the gates.

## Appendix A. Resolution of EX_105

| Finding | Class | Resolution in v0.1r1 |
|---|---|---|
| WF1BS-R3-B01 parallel STOP admission and parent loss | BLOCKER / RECHECK | Deferred with WF-1C (owner decision WB-0); carried in full as a WF-1C obligation (section 4). WF-1B changes no driver code |
| WF1BS-R3-C01 RK-4 disclosure versus "Part A only descriptive" | CORRECTION / RECHECK | Section 3: a titled RK-4 disclosure block at the top of Part A, the one stated exception, matching Part B; `table_kind` `RK4_DISCLOSURE`; tests in section 8 check the block and scan the rest of Part A |
| WF1BS-R3-C02 `compare` identities | CORRECTION / RECHECK | Deferred with WF-1C; carried (section 4) |
| WF1BS-R3-C03 evidence versus authorisation | CORRECTION / RECHECK | Deferred with WF-1C; carried (section 4). WB-3 withdrawn from this note |
| WF1BS-R3-C04 memory claims | CORRECTION / RECHECK | Deferred with WF-1C; carried (section 4). The 46 MB figure is no longer used in this note |
| WF1BS-R3-C05 portable limit tests and the 60 cap | CORRECTION / RECHECK | Deferred with WF-1C; carried (section 4). WB-4 withdrawn from this note |
| WF1BS-R3-O01 canary scope | OPTIONAL | Carried to WF-1C (section 4) |
| WF1BS-R3-O02 progress counts | OPTIONAL | Carried to WF-1C (section 4) |
