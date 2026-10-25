# Claude review of the Document Tree Refresh v0.2 candidates, v1

**Reviewer:** Claude (independent reviewer)
**Date:** 25 October 2026 (Adelaide)
**Reviewed:** `Predictive_Randomness_Document_Tree_Refresh_v0_2_CLAUDE_REVIEW.zip`, SHA-256 `4508268d5de9d822fb14e05f27cd9cbab102205cdc2462d296a55bb64de87324`, including `ChatGPT_Continuation_Handback_v0_6r1`.
**Checked against:** GitHub HEAD `3ddb8a6`, and `Claude_Review_Package2_v0_10_r1_and_Direction_v3.md`.
**Status:** review only. Nothing here ratifies a document or authorises any run.

No winning, Powerball or supplementary numbers appear in this document.

---

## 1. Verdict

**No BLOCKERS.** Five corrections (R1-R5) should be made before ratification. There are four discretionary items (D1-D4). The candidates faithfully carry the 25 October owner decisions and the v3 direction.

## 2. What was verified

| Item | Result |
|---|---|
| Manifest | 19/19 files match; nothing unlisted or missing |
| (a) HEAD and `doc/` inventory | HEAD `3ddb8a6`. All 17 SHA-256 values in the register's ratified table match the files at HEAD. Each candidate's body is identical to its ratified predecessor at HEAD, except the header/status lines and the new section (`0B`, or `ERR-R2-06` for R2). Line counts: Proposal +35/-5, R2 erratum +17/-3, R3 +18/-4, Architecture +38/-5, P3 +17/-3, register +24/-1. |
| (b) Protected rules | Architecture section 5C is byte-identical to v0.6 (the diff touches only the header and inserts 0B). R1 v0.4, the R2 v0.3 body and TIE_SHA256_V1 v0.2 are untouched. The E_1 digest `d47fbbd6...4339` and result `7f113087...164e` are stated as frozen everywhere. |
| (c) Boundary and exception | 2026-08-01; Powerball 1577 / Oz 1694; FINAL_HOLDOUT_10 1577-1586 / 1694-1703; development 1144-1576 / 1474-1693; E_1 1577 forecast-only, never read or scored, not a holdout result. Consistent in all five documents and the handback. |
| (d) Masters, order and views | File names and header columns are correct. The pinned ledger version and SHA are required. The order status `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`, with its citation, is stated as "assumed", never "verified". No entitlement registry; the result allowlist stays and is empty. The added rule that the whole-master SHA is never a seed, feature or readout input is correct and welcome. |
| (e) Dates | Opt-in, with a new schema and digest; the legacy E_1 digest is unchanged; masters hold the ISO date only. |
| (f) Installer | The install-and-upgrade default is retained. After every upgrade: STOP until the offline suites, boundary tests and E_1 goldens PASS. No upgrade between freezing and scoring, or within Mode H (R3-T50). |
| (g) No implied authority | Every candidate states it is unratified and authorises no run, Mode H, FINAL, update or holdout access. The Mode H storage design is correctly left as "proposed, to be reviewed". |
| Numeric width, owner rule | `int64` for the internal table and every view, `float64` for floats, typed dates, Python ints beyond 64 bits, `47*47 == 2209`, exact `.base` byte length. No surviving operative text permits `int8`/`int32` (the old v0.10-r1 code is described as uncorrected, which is accurate). |
| Fresh fit and caching | Every target N is fitted afresh on eligible draws < N. A cache is allowed only after a reviewed byte-identical test. Selective retention of intermediate states. Consistent. |

## 3. Corrections before ratification

| ID | Finding | Change |
|---|---|---|
| R1 | **Withdraw the old holdout rules by name.** The 0B / ERR-R2-06 sections supersede "conflicting" text only in general terms, while the ratified text still stands verbatim inside the candidates: Proposal section 0A (Oz rule "ten highest draw numbers in the first ... snapshot", sealed before the first scrape), ERR-R2-05 ("Powerball 1578-1587 remains sealed"; the Oz seal rule), and R3 section 0A.3. For a sealed-holdout matter, leave no room for argument. | In Proposal 0B.1, ERR-R2-06 item 1 and R3 0B, add one line that names what is withdrawn: Powerball holdout 1578-1587 and development cap 1577; the Oz "ten highest ... first accepted snapshot" rule and its seal step; `DEV_TO_DATE = 2026-08-07`. |
| R2 | **Hashing versus "never parse row N".** ERR-R2-06 item 2 and Architecture 0B.2 require the master SHA to be checked before parsing, and parsing to stop before row N. Hashing necessarily reads every byte, including the suffix. As written, the two rules can look contradictory. | Add: "Computing the SHA-256 reads all bytes without decoding them; the prohibition is on parsing or converting any field of a row whose first field is >= N." |
| R3 | **Oz master hash and HEAD.** P3 0B item 4, the handback and the impact assessment still say the Oz SHA is "read from its ledger" or give only a prefix. | Use the full value `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f`. Claude verified at HEAD `3ddb8a6` that, for both games, the master's SHA-256 equals both its ledger `INIT` row and its init record: version 1, Powerball 433 rows, Oz 220 rows, tool SHA `3436da9f...`. Update the handback's HEAD reference to `3ddb8a6`. |
| R4 | **Proposal header, line 8.** It now reads "now verified in owner-run masters" but still ends "subject to operator-source confirmation before data acceptance", which contradicts it. "As reported by Claude" undersells the evidence: the ledgers and init records are committed. | Replace with: "data accepted 25 October 2026 as master version 1; evidence in the committed ledgers and init records (hashes verified by Claude at HEAD `3ddb8a6`)". |
| R5 | **Exposure record completeness.** One factual item is missing. | Add item 4: "Results pages saved by the owner from The Lott in October 2026, for the cross-checks, also carried that site's latest-draw panel, which showed then-recent draws of both games in the quarantined range. The pages were kept outside the repository, and some were attached to the reviewer chat as files. The Claude-side tools never parse that panel; apart from item 1, no values were displayed." |

## 4. Discretionary

- **D1 (question h) [REVIEWER-DECIDED]:** make the numerical policy a **technical reference**, not a sixth normative copy.
  - The same rules now appear in five documents with slightly different wording. For example: "full applicable offline suites, boundary tests" versus "applicable complete offline test suites, mathematical boundary/precision checks". Duplicates drift over time.
  - One normative home per rule:
    - data, views, N-1 and width: ERR-R2-06;
    - evaluation, the freeze-to-score rule and Mode H pinning: R3 0B;
    - installer and implementation: Architecture 0B.
  - Proposal 0B summarises and points to those homes.
  - The policy document keeps its guidance (numerical stability, log-domain calculation, higher-precision reference checks), plus one precedence line: "where wording differs, ERR-R2-06, R3 0B and Architecture 0B prevail."
- **D2: Mode H storage.** ChatGPT's caution is right. Section 6A step 3 of my v3 is a proposal only. The Mode H package should weigh it against a separate quarantine store that the runner releases one draw at a time. No document change is needed now.
- **D3:** in Proposal 0B.3, use the exact name `PAIRED_DIAGNOSTIC` instead of "paired representations".
- **D4:** the candidates are UTF-8 with LF line endings, the same as the ratified set. No change.

## 5. Recommended order (unchanged from the impact assessment)

1. Make R1-R5 and D1/D3 as a v0.3 documentation refresh.
2. Claude spot-checks the diff.
3. The owner ratifies in this order: Proposal v0.5, then the R2 erratum v0.4 and R3 v0.4, then Architecture v0.7 and P3 v0.2, then the exposure record and the numerical reference, then register v0.3.

Package 2 v0.11 code remains a separate review.

*End of document.*
