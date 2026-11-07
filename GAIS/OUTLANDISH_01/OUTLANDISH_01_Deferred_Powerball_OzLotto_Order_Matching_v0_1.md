# OUTLANDISH_01 — Deferred Powerball and Oz Lotto order-matching extension

**Date:** 2026-11-07 (Australia/Adelaide)  
**Version:** v0.1 (proposal/decision record, **not** an implementation specification)  
**Status:** **RECORDED — DEFERRED**, following the owner's request on 7 November 2026.  
**Applies to:** `GAIS/OUTLANDISH_01` scientific digit scanner and its future Oz Lotto companion, **not** the independent main predictive-randomness programme.  
**Priority:** After the primary `OUTLANDISH_WSL` generation → isolated Windows conversion/verification → controlled registration workflow is implemented and rehearsed. Do not delay the WSL data pipeline for this enhancement.

## 1. Decision

Extend both **Powerball (P)** and **Oz Lotto (O)** constant-digit search reporting to distinguish **operator-drawn-order** from **any-order** matches, retaining the original category semantics and results for comparison. Record overlapping classifications without silently aggregating or double-counting them. The extension is exploratory, not evidence of predictive power or a redefinition of official prize divisions.

**Do not change code, current reports, data sources, format, or production experiments yet.** This note preserves a design direction and explicit unresolved issues for later specification, review and owner approval.

## 2. Grounded current Powerball scanner (as inspected in the supplied `OUTLANDISH_01.zip`)

The active `outlandish_powerball_stage_a.py` uses `FIXED2`: each ball is exactly two decimal digits; the constant file is one **numeric byte 0–9** per digit, not ASCII. It scans at *every* digit-byte offset, including odd offsets and chunk boundaries.

| Existing category | Existing semantics | Implementation approach |
|---|---|---|
| **P1** | All 7 main balls **in operator-drawn order**, followed by the Powerball number | Exact ordered key, including PB (`build_index`, `scan_one`) |
| **P2** | All 7 main balls **in operator-drawn order**, with no PB requirement | Exact ordered key |
| **P3** | **Any 6 distinct** of the 7 drawn main balls, in **any order**, followed by that draw's Powerball | Sorted 6-ball canonical lookup key, with PB; no explicit permutation enumeration |

Specifically: `build_index` establishes exact P1/P2 keys and sorted 6-ball P3 keys (around lines 220–234); `scan_one` canonicalizes candidate six balls for P3 but uses exact sequences for P1/P2 (around lines 303–326). The code does **not** currently do a sorted-number prefilter then check drawn order for P1/P2. Powerball Stage A already has consecutive-draw transition reports keyed by existing categories.

### Proposed Powerball classifications

| Experimental category | Keep existing | Proposed additional reporting |
|---|---|---|
| **P1** — 7 mains + PB | `P1_drawn_order` (current P1) | `P1_any_order`: the same **7 main-ball values in any order**, followed by the **same PB**. `P1_reordered_only` = any-order excluding drawn-order. PB is not permuted among main balls. |
| **P2** — 7 mains | `P2_drawn_order` (current P2) | `P2_any_order`: all 7 main-ball values in any order; `P2_reordered_only` likewise. |
| **P3** — 6 mains + PB | `P3_any_order` (current P3) | `P3_drawn_subsequence_order`: the six selected mains appear in the same **relative drawn order** as they appeared among the original seven, followed by PB; `P3_reordered_only` = any-order excluding this subset. |

**Proposed subset-order convention:** For a six-ball subset, delete one ball from the seven-ball draw sequence without rearranging the remaining six. This is *not* numeric ascending order and is not yet a ratified rule.

These classes are **nested** within each original category: e.g. `P1_drawn_order` is also `P1_any_order`. Existing P1/P2/P3 historical counts should remain reproducible unchanged, and new reports must make the intersection/exclusion semantics explicit. Across categories, hits may overlap (e.g., same prefix may qualify as P2 and P1); do not imply cross-category mutually exclusive totals.

## 3. Original Oz Lotto proposal (NOT implemented)

The historical 5 November 2026 standalone handover/scope proposed *seven main* numbers and *three supplementary* numbers, each from 1 to 47, and categories:

- **O1:** all seven main numbers in operator-drawn order.
- **O2:** any six main numbers plus any one supplementary number.
- **O3:** any six main numbers.

The historical spec specifically did **not** settle the precise ordering/permutation semantics of O2/O3, and the current OUTLANDISH source does **not** implement the Oz Lotto scanner. These are owner-defined exploratory pattern labels, **not** assertions about official Oz Lotto prize-division rules.

### Proposed Oz Lotto extensions (requiring explicit specification)

| Experimental category | Drawn-order variant (proposal) | Any-order variant (proposal) |
|---|---|---|
| **O1** — 7 mains | All seven main numbers in original drawn order | Same seven main numbers in any order |
| **O2** — 6 mains + 1 supplementary | Six main numbers in their relative order within the seven drawn mains, **followed by** a selected supplementary number (provisional placement rule) | Any order of the same six mains, **followed by** the chosen supplementary number (provisional placement rule) |
| **O3** — 6 mains | Six selected main numbers in relative drawn order | Same six main numbers in any order |

For each category, consider `drawn_order`, `any_order`, and `reordered_only`; do not add their counts together because drawn-order is a subset of any-order.

**O2 unresolved issues before coding:** Must supplementary numbers be the last encoded two digits, or can they occupy any position among the seven? Does the order of the three supplementary balls matter in selection or reporting? How will multiple eligible supplementary numbers for the same main subset/offset be attributed and deduplicated? These are *not* settled by this note and must be owner-ratified. Also confirm the actual authoritative Oz Lotto source's drawn-order fields and the isolated pre-holdout dataset schema before designing any production reader; do not invent them.

## 4. Implementation/research requirements, deferred

1. **Keep original semantics and baselines.** Existing Powerball P1/P2/P3 results and their historic counts remain reproducible; add versioned output fields/report IDs rather than silently redefining their meanings. Oz Lotto, not yet implemented, must have a separately versioned specification.
2. **Do not enumerate permutations unnecessarily.** Generalize the existing canonical sorted-key technique to filter candidate 7- or 6-main-number sets efficiently, then separately test whether the candidate satisfies drawn-order or relative-subsequence order. Preserve match multiplicities and draw-number identity.
3. **Separate matches by game.** Dedicated Powerball/Oz Lotto datasets, schemas, validation, indices, counts and reports. Never pool outcomes or mix game number ranges, prize definitions or holdout boundaries. All actual historical development outcomes must be from the respective approved isolated pre-holdout data.
4. **Preserve exact byte-offset semantics.** Continue scanning all positions, including odd offsets, chunk boundaries and EOF. Keep the integer digit of the constant at offset zero. Record the exact `FIXED2` matched digit sequence, draw identity, category and order classification, including PB/supplementary selection provenance when applicable.
5. **Be careful with overlap and duplicate attribution.** Report nested order classes (`drawn_order` ⊆ `any_order`), disjoint `reordered_only`, per-category counts, and distinct occurrence/draw counts where meaningful. Same constant offset may be valid for more than one category/draw; represent that deliberately.
6. **Version consecutive-draw positional analyses** (W to W+1) so original P-category comparisons are preserved and optional order-stratified comparisons can be evaluated separately. Specify how to handle zero matches and multiple matches before generating transition tables.
7. **Test before full scans.** Use synthetic planted exact-order, reversed/reordered, six-of-seven subsequence, supplementary-selection, duplicate-key, invalid/duplicate ball, odd-offset, chunk-boundary and EOF cases. Verify classification inclusion/exclusion, deduplication, report provenance, and performance/memory impacts. Compare original Powerball counts bit-for-bit where practicable.
8. **No implied statistical conclusion.** Large any-order match spaces can produce many more coincidences by construction. Compare appropriate chance/null baselines; label any observed positional clustering as exploratory until separately validated.
9. **No implementation authorisation here.** Return to this design only after the WSL2 generation/import/verification path is validated. Propose a focused specification and independent test plan, resolve Oz Lotto open questions with the owner, then implement under separate approval.

## 5. Source and handover context

- Current Powerball scanner: uploaded `OUTLANDISH_01.zip`, `outlandish_powerball_stage_a.py`, especially `build_index`, `scan_one` and `build_transition_report`.
- Historical Oz Lotto definitions: `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md`, especially the original experiment scope and unresolved O2/O3 semantics.
- Primary current workstream: `OUTLANDISH_01_2026-11-07_Project_Status_and_WSL2_Primary_Design_v3.md`.
- This note is **one deferred feature record for both games**, not a replacement for the v3 handover, the live code, the original owner scope or the established production registry.

**Next action now:** Continue the thin, isolated WSL2-to-Windows numeric-output conversion/verification integration. No scanning changes or Oz Lotto data retrieval are requested at this checkpoint.
