# Claude full review of the consolidated governing documents v0.3, v1

**Reviewer:** Claude (independent reviewer)
**Date:** 25 October 2026 (Adelaide)
**Reviewed:** `Predictive_Randomness_Governing_Documents_CONSOLIDATED_v0_3_CLAUDE_FULL_REVIEW.zip`, SHA-256 `0cc30ae97b759c65e01f3c2135a0c3a09b0893ef555e4894af8e4842d1586d9e`
**Baseline:** GitHub HEAD `ce462be`. Its `doc/`, `source_data/` and `src/` are identical to `cf00999`, so the ratified sources used are the ones I hold.

**Method:** independent.
- Re-ran the package verifier (PASS).
- Ran my own ID inventory: all A-, D-, I-, R2-C, R2-D, T-, W-, O-, M-INV- and ERR- identifiers present. The only exceptions are A-1/A-2, which were labels in the old revision history; their substance is in 5A.1, W-04 and W-19.
- Ran my own stale-phrase scan: no operative stale hits beyond those listed in section 3.
- Read every removed and added line, ratified to candidate, for the Proposal, R2, Architecture and R3, plus the P3 changes.
- Searched for each multi-game rule from the ratified Proposal 0A, Architecture 0A, R3 0A and ERR-R2-05 that does not carry an ID.

**Status:** review only; nothing here authorises any run. No winning, Powerball or supplementary numbers appear in this document.

---

## 1. Verdict

**Close. One BLOCKER (a short, specific list), plus corrections.**

Editing in place worked. The documents are back to near-ratified size, every ratified ID is present, and the diffs read as targeted changes. These now retain their full meaning:
- the philosophy, central premise and title;
- the A-01..A-37 and D1-D5 tables, with superseded rows such as A-08, A-33, A-34 and A-36 correctly restated;
- the I-, R2-C, R2-D and T- contracts;
- the W-01..W-25 and A-01..A-26 test tables, with W-23 extended to package upgrades;
- the wrapper rules (`SETLOCAL`/`ENDLOCAL`, `%*`, never rebuilding from `%1..%9`, the AutoRun check);
- the O-register, with O-POL-03 and O-PKG-02 correctly marked RESOLVED;
- 5C byte-identical;
- the M-INV-01..07 invariants, restored and updated;
- benchmarks at 1576 (Proposal 12.8; Architecture apart from C2);
- the R2 section 5.5 goldens;
- R3.

The remaining problem is the opposite edge of the v0.2 issue. Some ratified multi-game rules existed only inside the deleted 0A layers and the ERR-R2-05 table, with no ID. v0.2 had integrated them. Restoring the old bodies dropped them again, and the ID check cannot see them.

---

## 2. BLOCKER

### B1. Ratified multi-game rules without an ID are missing from every normative document

| # | Ratified rule (source) | Where it is now | Required home |
|---|---|---|---|
| 1 | Derived weekly date = era-start date + 7 x (N - first draw), a profile constant. A source/derived date discrepancy is a value-free warning that **halts date-dependent methods (E_14, E_54, governed equivalents) for that game pending owner decision**, and does not block unrelated U-view methods. (Proposal 0A.3; Architecture 0A.3; R3 0A.4; ERR-R2-05 "Date-using views") | **Nowhere.** No candidate contains a date-anomaly rule. | R2 section 3 (data) and R3 section 1.5 (evaluation) |
| 2 | Every **new** view schema for **any** game (including Powerball E_2+, ordered, X and date views) binds `game_id`, era and profile version into its schema/digest. **Only** the legacy `E1_REAL_U_TRAINING_VIEW_V1` keeps its legacy domain. (ERR-R2-05 "Seeds and tie identity"; Architecture 0A.2) | Only in P3 M-INV-01 and the non-normative numerical reference. R3 says only "appropriate training-view identity". | R2 section 4 or 5.4 |
| 3 | Per-game registry status `SUPPORTED` / `FORMULA_OPEN` / `UNSUPPORTED_FOR_GAME`, with a structural reason. (ERR-R2-05 "R2-C13"; Proposal 0A.1; Architecture 0A.1) | `UNSUPPORTED_FOR_GAME` appears in no document. The R2 status list at line 288 lacks it. P3 M-INV-07 says "support status" generically. | R2 R2-C13 and the status enumeration |
| 4 | Machine identity is the pair `(game_id, draw_number)`; `draw_key` is display-only and never a substitute. (ERR-R2-05 "Target identity"; Architecture 0A.2) | The pair is in R3 and P3 M-INV-02. `draw_key` display-only is in no document. | R2 section 2 |
| 5 | ERR-R2-05 **OPEN list** and **no-authorisation clause**. OPEN: E_54 feed contract, first Oz Lotto real experiment, start of each game's FINAL track, cross-game features, walk-forward pre-registration (Powerball 1145-1576, Oz Lotto 1475-1693). No authorisation: Oz method execution, modifying a frozen Powerball result. | R2 has neither. Parts are in P3 and R3 only. | R2 section 13 or 15 |
| 6 | Before E_2, replace the E_1-specific runtime conventions with a method-generic contract (Architecture 0A.4). | P3 only, as a work item. | Architecture section 20A, as a requirement |

---

## 3. CORRECTIONS

| ID | Finding | Change |
|---|---|---|
| C1 | **Architecture line 66** (requirement 11) says "the **6-worker** condition was withdrawn under ERR-R2-01". This is wrong: the **12-worker** condition was withdrawn, and six is current. | Change to "12-worker". |
| C2 | **Architecture benchmark presets (lines 608-611).** The B10 row is duplicated and B10-short is missing. | Replace the second row with "B10-short / 10 / 100 / Draws 1567..1576; each has 100 preceding observations". |
| C3 | **Architecture line 460:** "authorised logical observation view (`UNORDERED_SET`, `DRAWN_ORDER`, or an approved combination)", and "Both CSV views". These are the old names, wording that implies entitlement, and the old two-file source. | Use the three R2-C08 names, "caller-declared", and "both representations of the same master rows". |
| C4 | **Proposal section 20.1 (line ~1102)** still calls R1 the "separate current R1 research review candidate" and says "proceed to R2 ... rather than writing predictor code prematurely". **Line 1104:** "The R2 draft should address ... the simple 1-12 process / 32 GB baseline". | Restate as the current next step: ratify, install, then the coder handover. Mark 1104 historical, or change it to 1-6. |
| C5 | **Proposal D2:** "Order is now supported as operator-labelled drawn order". This conflicts with the updated A-33. | "Published order, owner-assumed operator order (`OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`)". |
| C6 | **R2 lost its own change-control rules** (old section 0.3): never edit a ratified file in place; a substantive algorithm change creates a new method-specification version; keep inactive/blocked methods in the registry; "an omission or a default in software is not a decision". Its binding philosophy quote (old line 14) is also shortened to one sentence. | Restore both verbatim. |
| C7 | **R2-C08 and R2-C09 are still labelled [PROPOSED]** although ERR-R2-06 made the view names, caller choice and manifest recording an owner decision. | Label them DECIDED (ERR-R2-06), keeping their text. |
| C8 | **The R2 erratum index maps ERR-R2-06 to "Architecture sections 5B, 5C".** 5C is protected and contains none of it; the content is in Architecture section 20A. | Correct the mapping. Also check that ERR-R2-05's "sections 12-16" mapping holds once B1 is fixed. |
| C9 | **Architecture 5A.2 installer requirements were condensed.** The ratified numbered list is gone: SETLOCAL scope, explicit `.venv\Scripts\python.exe -m pip`, show the complete list, `pip check` with a nonzero return on failure, a generated snapshot as evidence, notice that upgrades can change floating-point results, preserved environment and exit status, CRLF. | Restore the numbered list, changing only the default to INSTALL + UPGRADE and adding the post-upgrade STOP. |

---

## 4. OPTIONAL

- **O1:** restore the Architecture "Important distinction" note: independent executables share reviewed source modules, not a shared process, shared mutable memory or a compulsory central runner.
- **O2:** extend the "must be present" check with the six B1 terms (`UNSUPPORTED_FOR_GAME`, `draw_key`, a date-anomaly / E_14 rule, `E1_REAL_U_TRAINING_VIEW_V1` in R2, the ERR-R2-05 OPEN items, method-generic). That covers rules without IDs as well as IDs.
- **Exposure note:** while comparing the old and new Proposal, my diff display again showed part of the old Proposal's Draw 1587 paragraph. Exposure record item 5 already covers this, so no change is needed.

---

## 5. Next step

Apply B1 (six insertions) and C1-C9 as v0.4. These are local edits, so a focused spot-check of the diff is enough; no further full review is needed. Ratification can follow.

*End of document.*
