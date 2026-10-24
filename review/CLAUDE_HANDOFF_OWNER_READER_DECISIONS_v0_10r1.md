# ChatGPT → Claude: Owner decisions and Package 2 v0.10-r1 independent review

**Date:** 25 October 2026, Adelaide. **Status:** CODE/DOCUMENT REVIEW ONLY. No code installed; no owner-authorised live collection, Windows run, holdout access, or scientific run.

**Authoritative baseline:** Your `Claude_Review_Package2_Consolidated_v0_9_v2.md` (SHA-256 prefix `bd5665e0`), v0.9 candidate ZIP (`a14af81b...68ead46a`), ratified Package 1 documents and committed coordinator v0.6 (`2e23d550...`). This revised v0.10-r1 review ZIP **replaces** ChatGPT's initial v0.10 review ZIP (`8994cddc...487d32869`) for review purposes. It incorporates *only* the owner's subsequent view-policy/provenance clarifications in addition to the prior v0.10 scope; please preserve earlier v0.9 and v0.10 evidence for historical comparison.

## OWNER-DECIDED: general-purpose common reader; no duplicate view-permission table

The owner originally requested that **the common reader return sorted, drawn-order, or both representations at caller request**, with an experiment responsible for choosing and rigorously testing what it uses. They specifically reject maintaining a separate, duplicative per-(game, method, variant) view-entitlement registry: this would be another mutable source of scientific knowledge, potentially out of sync with the method. Their preferred safeguards are normal engineering discipline: method source review, tests, explicit diagnostics/log lines, immutable model configuration, forecast manifest and correct input-view digests.

Implement R2-C08 exact names `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC`. The reader offers all three on request; the caller selects. The paired representation is ONE object over the SAME events, not doubled independent draws. R2's no-double-likelihood principle remains binding, and predictive joint usage would need an explicit scientifically reviewed model. Reader need not prohibit a future legitimate joint algorithm. Remove `_VIEW_ENTITLEMENTS` and reader dependency on `permitted_view_kinds`; do NOT remove the separate scientific result-schema/data-kind/variant allowlist in the consumer. Scientific method support and registration remain governed for execution, but reader view selection does not mirror those permissions.

Preserve original `E_1` `FULL_HISTORY_RAW_COUNTS_V1` `UNORDERED_SET` Powerball view canonical schema/payload `E1_REAL_U_TRAINING_VIEW_V1`, golden digest `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339` and canonical result hash `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e`. New view/variant schemas and digests MUST differ; exact real golden remains post-DEV_BUILD gate. R2/Architecture amendment drafts are separate and require owner ratification if they change binding language.

**Order evidence:** The source includes sequences, but an unsorted sequence is not proof of true operator order. Powerball's order field must be established using the *pre-holdout* 434/434 comparison against historical Git CSVs; Oz order verification currently has only the early draw-1474 comparison, not a full-era proof. The revised reader currently labels source order `SOURCE_ORDER_UNVERIFIED` by default and never automatically upgrades it. Please recommend a provenance-bound, defensible promotion rule before order-dependent science is allowed, without reintroducing per-method entitlement tables. If you believe source order should be inaccessible pending such proof, explicitly report that as a design recommendation, not a silently enforced restriction.

## OWNER REQUEST: scrutinise complete-table N−1 isolation (ChatGPT recommendation A)

The common reader currently loads an entire pre-holdout development base into one immutable NumPy table and then returns an N−1 prefix for a target. This is efficient and supports repeatedly requesting views, but **immutability does not prevent a method from seeing future development rows if it can access the whole table or underlying CSV**. Please independently assess a trusted read-service/runner boundary where experiments receive only *prefix-only DrawView* objects (and perhaps a separate process), not `DevelopmentDrawTable`, its full arrays or full source paths. Consider performance, strict prior "loader never parses row N" rule, any scientific/method wrappers' actual access and suffix-poison tests. Propose the smallest defensible mechanism; do not relax N−1 silently. This remains an OPEN REVIEW ITEM, not a passed safety assertion.

## OWNER-DECIDED: old Powerball CSVs may be removed from active working tree (B)

They are recoverable from historical Git commits and should be removed *during the approved installation phase* before DEV_BUILD. DO NOT rewrite history or delete them in this review workspace. Their verified headers are:

- `australian_powerball_history_20261021.csv`: `Draw_Number,Date,Ball_1..Ball_7,Powerball` (main numbers sorted).
- `australian_powerball_draw_order_20261021.csv`: `Draw_Number,Date,Drawn_1..Drawn_7,Powerball,Official_Source_URL` (original Lotterywest sequence).

After owner-operated build, compare new Powerball development rows 1144–1577, **434/434**, for date, sorted seven-number set, Powerball, and exact drawn sequence. Do NOT compare/open quarantined draws >=1578 or calculate any metrics from them. The **new common reader uses the same drawn-order rows for both outputs**, sorting in memory for UNORDERED_SET; no second sorted CSV. The development source cap is 2026-08-07, Powerball 1577 / Oz 1694; later draws are quarantined.

## OWNER-ACCEPTED: factual holdout exposure record only (C)

Owner accepts making a factual, **value-free** note that reviewer chat displayed Powerball draws 1585–1587 and 1588. Do not include, reprint, compute with, statistically examine or design/select experiments using the exposed numbers. Do not assert "no effect" on any person's thinking without evidence. Retain the proposed exposure record as a draft pending accurate wording/review and any required ratification. No new holdout access is authorised.

## OWNER PREFERENCE: datetime if source can reliably substantiate it

Please assess whether Lotterywest's API or other already-identified provenance yields a meaningful **actual/official draw timestamp WITH a known timezone/UTC offset**. We prefer a timezone-aware datetime for future date/time-dependent experiments, and UTC storage with local display, **if verified**. Do not infer that a webpage's displayed 8:00 pm or 8:30 pm is the physical draw time, and do not invent a timezone or synthesize midnight. If source provides only a date, preserve a date-only field and label missing time explicitly. Distinguish scheduled/nominal draw, actual event, publication, and draw closing time. Keep draw-number sequence as the key; record raw source timestamp as provenance where available. If timestamps enter a method view, its own digest must bind exactly what was consumed; DO NOT alter legacy E_1 U digest. Please advise whether optional datetime belongs in canonical CSV, metadata sidecar or new view schema, and whether this needs a ratified amendment.

## Independent-review requests

1. Review revised v0.10-r1 delta and proposed R2/Architecture changes vs your v0.9-v2 direction; distinguish OWNER-DECIDED deviations from accidental gaps.
2. Review N−1 full-table isolation and minimal trusted boundary.
3. Review source-order proof binding without per-method entitlements; keep scientific result allowlist intact.
4. Verify old/new Powerball 434/434 *design*, exact E_1 golden identity preservation, and that no holdout reads occur in any proposed review procedure.
5. Assess optional verified datetime versus date-only, including provenance and digest consequences.
6. Keep all process-termination switches False; do not execute any live API/MHTML, Windows, or outcome-bearing test.
7. Identify any changes requiring owner ratification, especially R2/Architecture.

Return numbered BLOCKER/CORRECTION/OPTIONAL findings. The old Powerball CSVs are not modified in this package. No claims of a real DEV_BUILD or Windows pass are made.
