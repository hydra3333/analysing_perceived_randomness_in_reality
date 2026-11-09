# OUTLANDISH_01 - Claude Single Review of the Consolidated Matching, Classification and Reporting Specification

**Version:** v0.1
**Date:** 2026-11-09 (Australia/Adelaide)
**Reviewer:** Claude, independent technical/scientific reviewer
**Reviews:** `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_Candidate_v0_1.md` (ChatGPT, 9 Nov 2026)
**Status:** The single requested review. Design only. No code, scan, data or repository change.

**Basis:** the full candidate, checked against my two earlier responses. I have still not seen the scanner source, result CSVs or drawset files. Statements about existing code rely on ChatGPT's snapshot inspection.

---

## 1. Verdict

**PASS WITH SPECIFIC CORRECTIONS.** No blocker.

The candidate faithfully consolidates the owner decisions and both review rounds. The matching semantics, family table, role rules, EOF rule, conditional order model, analytical expectations and REAL/NULL separation are correct in substance. The corrections below fall into four groups:

- **(a)** A missing class of same-draw overlaps (shifted windows), which would make overlap reporting incomplete.
- **(b)** Three small code-level rules that make the REAL/NULL boundary concrete without any allowlist or registry.
- **(c)** Under-specified details of the W->W+1 primary test.
- **(d)** A contamination hazard specific to running fixtures through the OLD scanner.

All can be folded in by ChatGPT without another review round.

---

## 2. Corrections table

Priority: **MUST** = fold in before ratification; **SHOULD** = recommended; **OPT** = optional.

| # | Section | Disposition | Replacement rule / text | Reason | Priority |
|---|---|---|---|---|---|
| C1 | A3.3 | MODIFY | Add **shifted same-draw nestings**. For one draw, a window at start k contains the windows at k+2 field by field. Deterministic consequences: **P1_any@k implies P3_any@k+2** (fields 1-6 are six of the draw's mains, field 7 its PB; omitted main = field 0). **O1_any@k implies O3_any@k AND O3_any@k+2.** **O2 with supplementary in slot 0 @k implies O3_any@k+2** (the existing rule covers supp-last implies O3@k). Order flags follow: P1_drawn@k implies P3_drawn_subsequence@k+2; O1_drawn@k implies O3_drawn_subsequence@k and @k+2. | These are real, structural overlaps. They are not duplicates, but reports that list only same-start nestings will misdescribe overlap and invite double-counting of one physical substring. | MUST |
| C2 | A3.3 | MODIFY | Add the **PB-equals-main coincidence**: when a draw's PB equals one of its mains and that main sits in field 6 of a P2_any window, the same 14 digits are also a P3_any event for the same draw at the same start (two events, families K7 and K6S). Expected about 218 x 0.2 / 7 = **about 6 per constant**. Similarly, P1_any@k with PB equal to the field-0 main also gives P2_any@k+2. | Not rare: about 1 draw in 5 has PB equal to a main. The old scanner presumably emits both events too; baseline reproduction must expect them. | MUST |
| C3 | A3.3 / B6 | MODIFY | Replace any fixed nesting list in the reporter with one rule: **same-draw overlaps are computed physically**, as events of the same draw whose digit intervals `[start, start+L)` intersect. C1 and C2 become named fixtures, not reporter logic. | Robust to cases nobody listed; simpler code. | MUST |
| C4 | B5.1 | AGREE + note | Add one sentence: C1/C2 overlaps do **not** change any analytical expectation (expectations are additive per class); they affect only overlap tables and the independence caveat in B5.2. | Prevents someone "correcting" E for overlaps. | SHOULD |
| C5 | B3 | MODIFY | `matched_digits` is **text and must never be parsed as a number**. Leading zeros are common (balls 1-9 encode as `01`..`09`; any window starting with such a ball begins with `0`). Readers must specify string type and assert `len(matched_digits) == family length` and all characters are 0-9. `raw_events.csv` is never opened and re-saved in a spreadsheet; its SHA-256 in the manifest detects any edit. | A default CSV reader (pandas, Excel) silently drops the leading zero, so the classifier would mis-parse the fields. | MUST |
| C6 | B3 | MODIFY | "If the same identity would be emitted twice, treat it as a scanner defect" becomes an **enforced check**: after the deterministic sort, the writer verifies no two adjacent rows share `(draw_number, family, start_digit_offset)` and aborts the run (FAILED) if any do. | Cheap; turns a stated rule into a fail-closed guard against chunk double-emission. | SHOULD |
| C7 | B4 (REAL packed input) | MODIFY | State the concrete rule. A REAL run accepts a packed file only if (i) it lies in the hard-coded published `digits` root; (ii) its same-name `.wsl-receipt.json` exists; (iii) file size equals the receipt's declared size and N/2 **before** scanning; (iv) the streamed SHA-256 equals the receipt's SHA-256 **before** the run directory is marked complete; otherwise FAILED. | Uses only the existing receipts, so no new registry. B4 currently says "verified published packed constant" without saying how it is enforced. | MUST |
| C8 | B4 (REAL drawset) | MODIFY | Concrete rule without any SHA allowlist. (i) The REAL drawset path is fixed in the game profile, not a run argument. (ii) The REAL adapter requires integer draw numbers and requires **every draw number in [era_first_draw, cutoff_exclusive) present exactly once and nothing else** (Powerball: 1144..1576). (iii) Any gap, extra row or out-of-range ID is refused with a precise message. The profile already needs both bounds (era start for Oz; cutoff for both). | A fixture or decoy file cannot satisfy (ii) by accident. Decoys fail the integer rule; fixtures fail the range rule (see C9). No catalogue to maintain. | MUST |
| C9 | Q2 / B4 | MODIFY (corrects my own v0.1) | **Synthetic fixture draw IDs are small integers below every game's first real draw (for example 1-999; confirm against Oz era_first_draw at integration).** My v0.1 suggested 9,000,001 and up; that is **withdrawn**, because the existing scanner refuses IDs at or above 1577 before parsing, so such fixtures could not be run through it in Q2. IDs of 1-999 pass the old scanner's upper cutoff and are refused by the new REAL adapter's lower bound (C8). Decoys keep text IDs. | Makes Q2 possible against the old scanner while keeping REAL refusal automatic. | MUST |
| C10 | B5.3 / B3 | MODIFY | The REAL classifier and reporter verify that the drawset file they load has the SHA-256 recorded in the run manifest, and refuse otherwise. | Reproducibility, not authorisation: reclassifying old events against a later-edited drawset would silently change results. | MUST |
| C11 | Q2 | MODIFY | When fixtures are run through the **existing** scanner, its output must go to an explicit test location, and the test must confirm the REAL results root is unchanged (directory listing before and after). If the old scanner cannot be pointed elsewhere, run it on a copy in a scratch tree. | The old scanner predates the REAL/NULL separation and may default to the production results root. This is the one realistic contamination route in the current plan. | MUST |
| C12 | Q2 | ADD | If the old scanner's chunk size is not a parameter, chunk-boundary fixtures must be generated large enough to span its actual chunk boundary (still a temporary test file). **Do not modify the old scanner just to make it testable.** | Preserves it as an unmodified reference. | SHOULD |
| C13 | B5.4 | MODIFY | Fix the tie rule rather than leaving it open: choose the pair minimising `(abs(b-a), b-a)`, i.e. smallest absolute gap, then the negative signed gap. This is the legacy `closest_pair` convention. | One fewer open choice; continuity with legacy reports. | SHOULD |
| C14 | B5.4 | MODIFY | Define the permutation precisely. Permute the per-draw offset sets across **all D draws, including draws with no events**. The number of evaluable pairs then varies by permutation and is recorded. Use 10,000 permutations, p = (1 + b) / (R + 1). The primary test is **two-sided** (owner's hypothesis states no direction): b = permutations whose median is at least as far from the permutation median as the observed one. Report both one-sided tails as descriptive. | As written, the null and the tail are unspecified; different reasonable readings give different p-values. | MUST |
| C15 | B5.4 | MODIFY | A primary statistic per game applied to six constants is **six tests per game**. Predeclare **Holm correction across the six constants within each game**; report raw and Holm-adjusted p. | Without this, "predeclared primary" still leaves six chances per game. | MUST |
| C16 | B5.4 | ADD | Adjacency means consecutive draw numbers. A pair spanning a missing draw number is not adjacent; it is excluded and counted. With C8 enforcing completeness this should never occur for REAL data, but the rule must exist. A gap of zero arising from one physical window attributed to both W and W+1 (shared key) is recorded and flagged, not dropped. | Edge rules otherwise left to the implementer. | SHOULD |
| C17 | B5.3 | MODIFY | Each NULL run writes its generated decoy drawsets (text IDs) into its own NULL run directory and records seed and generator version in the NULL manifest. | Reproducibility should not depend on the random-number library's distribution methods staying identical across NumPy versions (they are not guaranteed to). Also lets NULL events be reclassified, as REAL ones can. | SHOULD |
| C18 | B5.3 | MODIFY | Fix the empirical tail convention: upper p = (1 + #{decoy count >= real count}) / (K + 1); lower tail analogous. State K beside every value. | Removes an open convention. | SHOULD |
| C19 | B5.2 | ADD | Optional extra row: O2 any-slot -> drawn subsequence, q = 1/5040. Note that C1 creates deterministic links between classes (for example, P1_drawn implies P3_drawn_subsequence@k+2), so conditional tests in different classes are not independent of each other. Each class's own test is unaffected. | Completeness of the order table; honest caveat. | OPT |
| C20 | B2 | ADD | Chunk boundaries fall on whole bytes (chunk size set in bytes), so every chunk starts at an even digit offset; odd starts are always interior to a chunk or in its lookahead. In odd-length fixtures, require the pad nibble to be 0 and never count it as a digit. | Removes a class of off-by-one designs at little cost. | OPT |

Everything not listed is **AGREED as written**. This includes: A1-A2; A3.1/A3.2 semantics and role rules; the O2 nesting `drawn_subsequence (subset of) supplementary_last (subset of) any_slot` and its reordered labels; the B2 family table and all eight invariants; the B3 four-column schema; B4's structure and its "no new administrative machinery" stance; B5.1 figures (verified: 0.000433 / 2.18 / 0.0433 / 218.23 / 0.3031 / 218.23; Oz S values 5,040 / 105,840 / 15,120 / 21 / 5,040 / 7); the B5.2 q values; B5.3 decoy sampling and K = 19 / 99 as benchmark defaults; B6 outputs; the Q1-Q5 order; and B8 exclusions.

---

## 3. Consequential edge cases, as tests

Each becomes a Q2 fixture or reporter fixture. **Blocker** means the corresponding MUST correction must be in the spec; the fixture itself is built later.

| Test | Expected result | Status |
|---|---|---|
| Plant one P1 any-order window for draw X at k | Events: K7S@k, K7@k, K6S@k+2 (all draw X); reporter shows them as one same-draw overlap group | Blocker (C1, C3) |
| Plant an Oz O1 window for draw Y at k | K7@k, K6@k, K6@k+2 | Blocker (C1), when Oz is in scope |
| Plant an O2 window with supplementary in slot 0 | K7mix@k and K6@k+2 | Blocker (C1), when Oz is in scope |
| Draw with PB equal to main m; plant six other mains then m | K7@k and K6S@k for the same draw | Blocker (C2) |
| Window whose first ball is 01..09 | `matched_digits` round-trips with its leading zero through write, read and classify | Blocker (C5) |
| Old scanner run on fixtures | REAL results root listing identical before and after | Blocker (C11) |
| Fixture drawset (IDs 1-999) given to the new REAL entry point | Refused (range / completeness) | Blocker (C8, C9) |
| Drawset edited after a REAL run, then reclassified | Refused (digest mismatch) | Blocker (C10) |
| Duplicate emission injected | Run FAILED by the writer check | Optional (C6) |
| Tie fixture with gaps of -5 and +5 | Signed gap reported as -5 | Optional (C13) |

---

## 4. The five requested review points

**4.1 Family index, role and EOF rules: correct.** The K6S/K7 collision rule, PB-equals-main legality, the seventh-main 1-35 rule for P2, Oz K7mix identification after lookup against the draw's disjoint role sets, and per-family `k + L_F <= N` with explicit masks are all right. The only omission is the overlap consequence of these rules (C1, C2), which affects reporting, not matching.

**4.2 REAL/NULL boundary without an allowlist: adequate once C7-C11 are added.** The boundary then rests on rules the project already needs: existing receipts; the profile's era start and cutoff, enforced as a complete range; integer versus text IDs; fixed output roots; and digest consistency between manifest, events and drawset. None of it is an owner-maintained catalogue. The one realistic leak is the old scanner during Q2 (C11). Residual risk after this: deliberate manual file placement only.

**4.3 Conditional order model and expectations: correct.** All q values and expectations check. Events versus distinct offsets versus distinct draws are correctly separated. Add C4 (overlaps do not alter E) and the optional C19.

**4.4 Four-column raw record: sufficient.** `draw_number`, `family` and `matched_digits`, plus the drawset (verified by digest, C10), determine every classification: stream order of fields, the omitted main, PB or supplementary identity and slot, drawn and relative order, and all nested memberships. **No extra field is needed**, provided `matched_digits` is handled as text (C5).

**4.5 W->W+1 primary statistic: coherent once C14 and C15 specify it.** Median of per-pair minimum absolute gaps, with a draw-label permutation null preserving each draw's whole offset set, tests adjacency conditional on the observed event sets. It says nothing about forecasting, and the spec rightly labels it exploratory. Expect about 67 evaluable Powerball pairs per constant (about 0.5 P3 events per draw), so Powerball power is limited. Oz O3 (about 50 events per draw) is much better powered.

---

## 5. Consensus ledger

| Item | Status |
|---|---|
| Owner decisions (section 0, Part A) | AGREED, fixed |
| Family table, role rules, EOF rule, arithmetic, compact keys | AGREED |
| Overlap rules | AGREED WITH A SPECIFIC REVISION (C1-C3) |
| Expectations and conditional order model | AGREED (C4 note, C19 optional) |
| Four-column raw events + manifest | AGREED WITH A SPECIFIC REVISION (C5, C6) |
| REAL/NULL separation, no allowlist | AGREED WITH A SPECIFIC REVISION (C7-C11) |
| Decoy design, K defaults | AGREED WITH A SPECIFIC REVISION (C17, C18) |
| W->W+1 primary statistic | AGREED WITH A SPECIFIC REVISION (C13-C16) |
| Qualification order Q1-Q5 | AGREED WITH A SPECIFIC REVISION (C9, C11, C12) |
| Exclusions (B8) | AGREED |

**Residual disagreement:** none.

**Items for the owner to note, not decide:**
1. The predeclared primary W->W+1 test as specified by C14/C15: two-sided, 10,000 draw-label permutations, Holm across the six constants per game. The owner may veto it before any real scan.
2. B4 introduces one new folder, the NULL results root (for example `G:\OUTLANDISH_01\large_artifacts\results_null\`), as a sibling of the existing `results\`. It is the only addition to the established G: layout.

**Suitability:** once ChatGPT folds in the MUST items (C1-C3, C5, C7-C11, C14, C15), this candidate is suitable for owner ratification **without another review round**. SHOULD and OPT items may be accepted or declined by ChatGPT with a one-line reason each.

**End of review.**
