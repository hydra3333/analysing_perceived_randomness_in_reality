# Independent ChatGPT focused document review — MR Integration Candidates v2

**Date:** 26 October 2026 (Australia/Adelaide)  
**Role:** independent DOCUMENT REVIEWER, not the Package 2 coder  
**Reviewed archive:** `Predictive_Randomness_MR_Integration_Candidates_v2.zip`  
**Archive SHA-256 verified:** `9f087fcf4fea3ec232caff0f928e20ffeb662f6c251cdc97a23ebdaa5d04f628`  
**Claimed source baseline:** Git HEAD `618fe48` (reported and previously documented; this focused review did not independently query the remote repository)  
**Disposition:** **0 BLOCKER / 1 CORRECTION / 0 OPTIONAL**. The v1 substantive blocker and both stale-reference corrections are resolved. A narrow provenance qualification remains before ratification; it does not change a scientific rule.

## 1. Scope and review method

Read `review/MR_Integration_Evidence_Note_v2.md` (starting at section 0), `review/MR_Integration_v1_to_v2_v1.diff`, the five v2 candidates, the previously reviewed v1 candidates, the prior independent v1 review and the historical ratification register from the supplied repository ZIP. Independently inspected archive bytes, SHA-256 identities, document diffs, retained hashes, relevant sections and the reference-scan report. **No packaged build/assembly/check scripts were executed; no project code, scientific tests, data acquisition, experiment, scoring or holdout access was performed.** Nothing in this review grants such authority.

## 2. BLOCKER — none

**B-01 resolved.** `doc/RATIFICATION_REGISTER_v0_4.md`, lines 62–65, now distinguishes the pre-ratification governing set from the future operative set. Lines 78–99 identify the consolidated predecessor editions as a *historical ratification inventory*, change the column to “Pre-integration ratified edition”, and preserve the preceding approvals. Exposure record v0.1 is explicitly superseded by v0.2 at line 91. There is no second purportedly current set in the register's forward-looking authority presentation.

An independent comparison with `doc/RATIFICATION_REGISTER_v0_3.md` in the supplied repository ZIP found **25 distinct SHA-256 hashes in v0.3 and all 25 unchanged in v2**. The register contains 32 distinct 64-hex SHA-256 identities in total (the historical 25 plus ratified MR v0.5, exposure v0.2, register v0.3 and four candidate-document identities). The historical rows have not been deleted.

The two additional disposition rewrites at v2 lines 111–112 (old handovers v0.6/v0.6r1 and Claude v2–v8) correctly convert obsolete future tense to historical succession by later handovers; they do not silently de-ratify an old document. The historical completion descriptions at lines 97, 99, 116 and 118 retain their factual sequence. The quoted commit identities are consistent with the supplied continuity records; remote Git ancestry was not independently reverified in this focused review.

## 3. CORRECTION — one narrowly scoped clarification

### C-v2-01 — Register's “only” attribution omits the separately owner-approved O-02

**Location:** `doc/RATIFICATION_REGISTER_v0_4.md`, line **95**, historical inventory's **“Owner-ratified on 26 October 2026”** paragraph, second sentence. The paragraph ends the operative-edition description with:

> `as amended only by the already owner-ratified MR proposal.`

However, the project owner separately approved **O-02** for R3 section **17.10.1** in v2: replacing the inherited shorthand CSV row key with `(analysis_unit, unit_id, sub-measure)` keyed to 17.3.4A. The MR proposal v0.5 itself is unchanged, and `review/MR_Integration_Evidence_Note_v2.md` section 0 correctly distinguishes that separate approval. Thus a reader could take “only by ... MR proposal” as an inaccurate, exhaustive account of the authority for *all* changes in the newer operative editions. This is an **attribution precision defect**, not an unapproved measure or mathematical change.

**Suggested exact replacement of line 95's second sentence only:**

> These requirements were ratified in consolidated R2 v0.4, R3 v0.4 and Architecture v0.7; upon owner ratification of the integration, their continuing operative editions are R2 v0.5, R3 v0.5 and Architecture v0.8. The newer editions integrate the owner-ratified Method Ranking Measures Proposal v0.5 and the separately owner-approved R3 section 17.10.1 CSV row-key clarification; no unrelated earlier rule is amended.

Keep the paragraph's opening list of older ratified requirements and its final sentence, `Ratification of either set grants no run authority.`, unchanged. This revision records authority **without asking the owner to approve O-02 again**. Recalculate the register's candidate SHA-256 and regenerated package/manifest identities after Claude makes the targeted edit. The four governed-document candidate hashes need not change on account of this register-only wording correction.

## 4. Previously raised CORRECTIONS — resolved

- **C-01:** `R2_v0_5.md`, section 3.6, line 200, scored-opportunity index now uses `(R3 section 17.3.8)`, the correct relocated definition. The obsolete `(3.8)` occurrence is absent from R2 v0.5.
- **C-02:** `R3_v0_5.md`, section 17.17, line 1883, the `Step 3, rankings per game` row now reads `R3 sections 17.6 and 17.10`. The obsolete `Sections 6 and 10` is absent from R3 v0.5.
- **C-03:** `RATIFICATION_REGISTER_v0_4.md` line 58 now names all **five** edition/status headers, including the register; candidate/present-authority rows; pre-integration inventory; R3 section 17.13 stage-0 completion; the four governed-document hashes; and the register's own SHA-256 in the external installation manifest. Evidence note v2 section 8 gives the corresponding installation instructions. No candidate is prematurely labelled as ratified.

## 5. Previously OPTIONAL changes — owner-approved and correctly applied

- **O-01:** R3 sections 7.4 (line 448) and 17.5B (line 1401) both explicitly require a single ranking-report row with `row_type` = `RANKING_REPORT`; the sole programme-wide append-only log remains `results/audit/SEARCH_LOG.csv`. This does not establish a second search log or a new forecast input.
- **O-02:** R3 section 17.10.1 (line 1764) now specifies a CSV row per `(analysis_unit, unit_id, sub-measure)`, as defined in section 17.3.4A. This is consistent with the ratified analysis-unit key, and the note identifies its **separate owner approval** rather than pretending it is a literal transcription of unchanged MR v0.5.

## 6. No unlisted v1-to-v2 document changes

Comparing all five actual v1/v2 document files:

| Candidate | Byte equality with v1 | Change scope |
|---|---|---|
| R3 v0.5 | Changed | Four one-line replacements: O-01 at two sites, O-02 and C-02 |
| R2 v0.5 | Changed | One one-line replacement: C-01 |
| Architecture v0.8 | **Identical** | None |
| Proposal v0.6 | **Identical** | None |
| Register v0.4 | Changed | Agreed authority-label/history corrections, C-03, candidate hash and section-label updates |

The supplied unified diff is **exactly reproducible** from these five document pairs after decoding six literal `\\uXXXX` escapes in the supplied ASCII diff back into the UTF-8 characters present in the source documents. Without that display-only Unicode normalisation, the diff files do not compare byte-for-byte as text. It contains **23 removed** and **25 added** content lines under standard unified-diff counts (48 signed line entries). Therefore the accompanying shorthand “39 changed lines” was **not reproduced as a conventional +/- line count**, but the discrepancy hides no unlisted document modification.

All v2 candidate hashes agree with evidence note v2 section 1, including:

- R3: `e80356aadb72f52c6e695bb30960d32923ae1c9820bc759df1d6675567353c2e`
- R2: `62d1c9c99e7dd33fe5c2496615229d5a67e09d3c6f6b68ada2146b60999e53da`
- Architecture: `d27115e095e309fc1e6d68099ee397432f561a7cb51eee722522a85493203875`
- Proposal: `ee552a5b530b38604e7b8b8129e5c1ba9485cbe423658e4f5d73bbd9d8b52349`
- Register: `0ba1ae26521ace6a51d7a545576aecbe2b7e3e3f75cc1114480f56d8bd07af2f`

Because the earlier v1 protected-block review passed, Architecture and Proposal are byte-identical, and the R3/R2 changed sites are outside the protected blocks, v2 makes **no change** to Architecture 5C, R2 sections 7/4.1, R3 0.4/2.4/3, or Proposal E_1–E_6. The prior v1 findings of full MR-ID coverage and no scientific-rule loss are not contradicted by these scoped changes.

## 7. Reference scan and safeguards

The evidence note's reference scan classifies **295** hits: 90 qualified references, 127 R3 17.x references, 36 resolving local references, and 42 directional/numeric items flagged for reading. The saved check output's class summary agrees; it shows **zero unresolved-reference classifications**. I inspected the reported non-OK entries, including the local references and 42 discretionary `REVIEW` items. They are not the two prior stale pointers or apparent new cross-document relics. This is a document/reference check, not a proof of all future runtime implementations.

The v1-to-v2 edits do not make conventional significance a veto, suppress unconventional measures, weaken N−1/holdout or protected safety rules, alter supplementary-number predictor isolation, authorise Package 2 ranking code, or open Mode H/FINAL. Scientific methods/tests were not run and no draw-result values were examined or reproduced.

## 8. Paste-ready handback for Claude and the project owner

> **Independent focused review: MR Integration Candidates v2, SHA-256 `9f087fcf4f...d04f628`: 0 BLOCKER, 1 CORRECTION, 0 OPTIONAL.** B-01 is resolved: register v0.4 has one unambiguous future operative set, the historical pre-integration inventory is identified as historical, the two additional old handover disposition rows are correctly recast, and all 25 original register hashes remain intact. C-01/C-02 cross-references, C-03 installation/status/hash instructions, O-01 single typed search-log row, and separately owner-approved O-02 CSV row key are correctly applied. R3/R2/register changes match the supplied v1→v2 diff; Architecture and Proposal are byte-identical; reference-scan report classifies 295 hits with zero unresolved; no new scope or holdout authority. **C-v2-01:** Register v0.4 line 95 describes the new editions as amended *only* by MR proposal v0.5, overlooking the separately owner-approved O-02 clarification of R3 17.10.1. Replace only that sentence with the exact text in the attached review, then regenerate the register/package identities. No science-rule or formula change. No project code, tests, scientific runs or holdout access.

**Recommendation:** targeted register wording correction, then prepare the owner-ratification installation artifact, retaining all historical identities and the independent reviewer/owner approval gates.
