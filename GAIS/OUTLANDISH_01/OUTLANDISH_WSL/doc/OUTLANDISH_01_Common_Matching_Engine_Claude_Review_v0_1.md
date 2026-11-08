# OUTLANDISH_01 — Powerball and Oz Lotto Common Matching Engine and Assessment/Reporting Design

**Claude independent architecture/scientific review request — v0.1 (DRAFT, NOT RATIFIED)**  
**Prepared:** 8 November 2026, Australia/Adelaide  
**For:** A separate Claude conversation acting as an independent reviewer; the owner will relay this document.  
**From:** ChatGPT, proposing an architecture for independent challenge, not asserting that it is implemented.  
**Scope:** The standalone `GAIS/OUTLANDISH_01` mathematical-constant digit-search research, which may eventually provide candidate methods to `hydra3333/analysing_perceived_randomness_in_reality`. **No changes to the parent project's scientific/governance contracts are authorised by this draft.**

> **REQUEST TO CLAUDE:** Please read the whole document, especially **Part A (established facts, decisions, current workflow, uncertainties)** before reviewing **Part B (my recommendation and draft design)**. For every material proposal, respond **AGREE / DISAGREE / MODIFY / ALTERNATIVE**, with technical and scientific reasoning, concrete counterexamples where relevant, and the smallest viable revised architecture. Challenge my assumptions. Identify defects in baseline matching, order semantics, result attribution, null-model logic, safety, implementation complexity and the proposed tests. **Do not write/install code, run large jobs or change any project data without separate owner authorisation.** This is a review and design consultation, not an implementation handoff.

## Read-me-first: what is factual, what is proposed

This document deliberately distinguishes:

- **[OWNER-REPORTED]** Terminal outputs and owner decisions during the active production conversation on 8 Nov 2026. These are not claims that this reviewer or ChatGPT independently accessed the owner's drives.
- **[AS-INSPECTED]** Behaviour of scripts and historical project records in the available uploaded ZIPs and handovers. The checked ZIP snapshots may differ from the latest live Git checkout; examine the current checkout before changing source.
- **[OFFICIAL]** Public game descriptions from `https://www.lotterywest.wa.gov.au/` (Lotterywest-GOV) checked 8 Nov 2026. Prize divisions are listed to orient the experimental labels; the project *does not simulate actual purchased ticket payouts*.
- **[PROPOSED]** The matching-engine architecture, output schema, interpretations requiring owner decision, analytical methods and qualification design in **Part B**. Nothing proposed is implicitly ratified.

The owner deliberately welcomes unconventional exploratory hypotheses about randomness while expecting that conventional chance may explain all findings. We should **not automatically dismiss** unusual correlations, but must distinguish accurately recorded descriptive phenomena, appropriately calibrated statistical evidence, and executable next-draw predictive algorithms. Scientific correctness and practical simplicity outrank gratuitous paperwork and wholesale restructuring.

---

# Part A — Established project context and experimental requirements

## A1. Research purpose, relationship to the parent project, and present stage

The user wants to generate exceptionally long decimal expansions of six mathematical constants and look for patterns corresponding to **historical Australian Powerball and Oz Lotto draw results** in their continuous decimal digits. The central data include **every matching offset and its owning draw(s)**; subsequent research concerns whether the positions of historical draw `W` and successive draw `W+1` show interesting relationships, including relationships across matching categories. A later, separately specified candidate method could potentially map *past-only* data to a next-draw forecast. A list of coincidences alone is **not** a predictive method.

This is a standalone side investigation physically located under the parent research checkout. The separate parent repository uses protected historical development/holdout separation, independent methods and review, forecast scoring, and its own approval processes. `OUTLANDISH_01` cannot silently alter the parent's method registry, source policy, holdout, methods, rankings, TOP/WORST, or real-outcome workflows. Powerball and Oz Lotto must remain distinct experiments, with **compound `(game_id, draw_number)` draw identities** and independent source data and cutoff rules.

**Owner sequencing decision (8 Nov):** Finish generating, verifying and publishing **all six final 10^10-digit packed binaries**, then independently qualify the scientific match engine; **do not start further production scientific matching** before the source audit, deliberate synthetic-known-hit tests and prefix-result reconciliation have passed. The earlier one complete 10^10-digit phi scan has *integrity* evidence, but its *scientific hit counts are unqualified*.

## A2. Official Australian game mechanics and divisions (context, NOT the exact search rules)

**Authoritative public game-rules context [OFFICIAL]:**

- Powerball: `https://www.lotterywest.wa.gov.au/games/powerball`; Lotterywest-GOV FAQ `https://www.lotterywest.wa.gov.au/frequently-asked-questions`.
- Oz Lotto: `https://www.lotterywest.wa.gov.au/games/oz-lotto`.
- Critical historical Oz Lotto rule transition: Lotterywest-GOV 7 Apr 2022 announcement, `https://www.lotterywest.wa.gov.au/lotterywest/media-centre/bigger-prizes-and-more-winners-with-oz-lotto-game-change`, identifying a **scheduled 17 May 2022** launch of seven mains and three supplementaries from 47 numbers, replacing a 45-number / two-supplementary version, conditional on regulatory approval. Independently verify the **first effective draw number and actual historical dataset era**, rather than deducing a cutoff from this announcement alone.

### A2.1 Powerball — official draw mechanics

- Draws normally Thursday; **seven distinct main (winning) numbers from 1–35** in one barrel, and **one Powerball from 1–20** in a separate barrel.
- The PB number **can numerically equal a main number**, because it is from an independent barrel; it has a different *role* and must not be treated as an eighth distinct main.
- Official ticket prize categories do **not** require the seven winning numbers to occur in their operator-drawn order. The project's ordered decimal patterns are additional exploratory constructs.

**Lotterywest-GOV current Powerball prize descriptions:**

| Official division | Number-match criterion shown on official game page |
|---|---|
| 1 | 7 winning main numbers + the Powerball |
| 2 | 7 winning main numbers (without matching Powerball for a separate Div 2 award) |
| 3 | 6 winning main numbers + the Powerball |
| 4 | 6 winning main numbers |
| 5 | 5 winning main numbers + the Powerball |
| 6 | 4 winning main numbers + the Powerball |
| 7 | 5 winning main numbers |
| 8 | 3 winning main numbers + the Powerball |
| 9 | 2 winning main numbers + the Powerball |

Only the **top three selection patterns** are in the present constant-search research. The labels P1/P2/P3 are *pattern categories*, **not an assertion that a matching 14- or 16-digit substring constitutes a prize-winning ticket**. For example, a P1 hit also has the seven-main P2 prefix; project reporting permits this overlap, whereas a physical ticket belongs to the applicable winning division. There is no automatic disjoint official-prize classification of decimal substrings.

### A2.2 Oz Lotto — official draw mechanics

- Currently drawn Tuesdays; **ten distinct numbers from a common 1–47 barrel**: the **first seven** are main winning numbers, the **last three** are supplementary numbers. All three supplementaries are distinct and do not repeat the main seven within that draw.
- Unlike Powerball, Oz Lotto's supplementary balls are **not a separate independent 1–20 barrel**. A shared matcher must not conflate the two role systems.
- Ordering of the main and supplementary draws is important as input provenance for this experiment; official lottery-prize eligibility is by selected values, not by reproduced chronological draw order.

**Lotterywest-GOV current Oz Lotto prize descriptions:**

| Official division | Number-match criterion shown on official game page |
|---|---|
| 1 | 7 winning main numbers |
| 2 | 6 winning main numbers + 1 supplementary |
| 3 | 6 winning main numbers |
| 4 | 5 winning main numbers + 1 supplementary |
| 5 | 5 winning main numbers |
| 6 | 4 winning main numbers |
| 7 | 3 winning main numbers + 1 supplementary |

The proposed O1/O2/O3 pattern classes target the **top three selections only**; they do not attempt official ticket prize classification. The exact exploratory O2/O3 order semantics are *not yet settled*. Older Oz Lotto results **must not** be processed as 7+3-from-47 merely because the current game has that format. Separate versioned rule eras or a modern-era-only approved dataset are options for owner/Claude review.

### A2.3 Draw-source and isolation constraints

- The owner established **Lotterywest-GOV**, exactly `https://www.lotterywest.wa.gov.au/` results-search pages, as the sole approved production source for newly acquired draw outcomes. Do not silently use `oz.lotterywest.com`, The Lott, aggregators, other branded sites or unofficial APIs as production-result substitutes. Official game descriptions above are context, not authorisation to change data acquisition.
- Use the isolated, previously prepared Powerball CSV `POWERBALL_preholdout_only.csv`; **433 consecutive draws, 1144–1576 inclusive**, exclusive cutoff `1577`. Its schema is `Draw_Number,Date,Drawn_1,...,Drawn_7,Powerball`, and numbers `Drawn_1..7` preserve operator-labelled order. The current scanner refuses draws >=1577 **before parsing their other fields**. It must not read the parent master as a shortcut.
- Oz Lotto does **not** yet have a demonstrated authorised reader, isolated pre-holdout CSV or validated schema in the supplied snapshot. Before an implementation: confirm the source actually retains trustworthy **operator-drawn order**, document the modern-rule-era draw range, agree an Oz-specific holdout cutoff and provenance, and create a game-specific adapter. Never import Powerball's numeric cutoff as Oz Lotto's.
- In development and real next-draw workflows, follow the parent project's applicable no-leakage and information-cutoff rules. Do not interpret full historical all-draw matching as a permission to use future outcomes to design/evaluate a past forecast.

## A3. Constant-file production — six agreed 10^10-digit datasets

**[OWNER DECISION]** The final data size is **ten billion digits per constant**, not one hundred billion. Producing the latter was judged disproportionate in time/disk costs. The six sources are:

| ID used by WSL generator | Constant | Leading decimal digits (including integer digit) |
|---|---|---|
| `phi` | Golden ratio, phi | `1.6180339887...` |
| `pi` | Pi | `3.1415926535...` |
| `e` | Euler's number | `2.7182818284...` |
| `log2` | Natural logarithm of 2 | `0.6931471805...` |
| `gamma` | Euler–Mascheroni constant | `0.5772156649...` |
| `lemniscate` | Lemniscate constant / selected y-cruncher half-perimeter output | Identify actual y-cruncher selection and verified prefix from production receipt; do not infer a prefix from this label |

The production stream retains the **leading integer digit** at logical digit offset zero and omits the decimal point. A declared `N=10,000,000,000` has **exactly N real decimal digits**, with `-dec:9999999999` passed to y-cruncher (9,999,999,999 digits after the decimal plus one before it). During generation, y-cruncher's text file is 10,000,000,001 bytes including the decimal point.

**[OWNER-REPORTED current progress, 8 Nov 2026]:**

| Constant | Verified generation | Final packed publication | Exact final SHA-256 | Cleanup |
|---|---|---|---|---|
| `phi` | PASS, y-cruncher `-verify:1`, exit 0; ~83m start-end | **PUBLISHED** `G:\OUTLANDISH_01\large_artifacts\digits\digits_golden_ratio_10_to_10.packed.bin` (5,000,000,000 B) | `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d` | Decimal source deleted; report/log preserved; full-file SHA compared during complete scan; scientific results *unqualified* |
| `e` | PASS, `-verify:1`, exit 0; ~136m36s shell | **PUBLISHED** `G:\OUTLANDISH_01\large_artifacts\digits\digits_e_10_to_10.packed.bin` (5,000,000,000 B) | `522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f` | Independent **standalone `sha256sum --check`** read whole 5 GB on G: and passed; final hard-link publication + source deletion + empty swap cleanup PASS; report/log preserved |
| `pi` | **In progress / waiting**, according to owner's current description; no completed run log supplied here | NOT CLAIMED | — | Not yet final |
| `log2` | Not reported complete | NOT CLAIMED | — | — |
| `gamma` | Not reported complete | NOT CLAIMED | — | — |
| `lemniscate` | Not reported complete | NOT CLAIMED | — | — |

The order of pending constants may change; do not infer that a preview created files or that π completed. The project is **two of six final packed binaries complete** at this checkpoint, with π underway per the owner. Even completed `phi` and `e` are **filesystem-published but not entered into a newly implemented packed-format registry**; their conversion receipts retain `PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY` scope. Do not mistake file presence for registry release.

**Production platform and workflow [AS-INSPECTED / OWNER-REPORTED]:** Windows 11 / AMD Ryzen 9 3900X / 32 GiB RAM; Debian 13 WSL2, y-cruncher static v0.8.7 build 9547, Linux ext4 working filesystem in dynamic VHDX physically on host T:, G: for final files; WSL ~15.6 GiB available, 4 GiB unused OS swap at preflights, `-M:12g -TD:4 -PF:taskqueue -mode:swap`, y-cruncher `-verify:1`, no independently recomputed mathematical constant (risk explicitly accepted). `-verify:0` is **benchmark-only, not production**. The intended `taskset -c 0,2,4,6` physical-core confinement was **not maintained by Kagari** (actual child thread affinity observed all 24 logical CPUs in phi); this remains a separate performance/safety concern and no reason to alter scan semantics. Older unverified data and byte-per-digit binaries must not be silently promoted as packed production data.

Per constant: verified generation on T: ext4 -> `wsl_convert.py` streams/validates decimal source and writes **exactly 5,000,000,000 bytes** directly into pre-existing G: `large_artifacts/staging` -> create-only `*.wsl-receipt.json` with source and packed hashes -> optional Windows 12-sample verifier -> independent **entire persisted packed file** SHA-256 comparison (`sha256sum --check` for e; the phi full scanner provided digest evidence, even though its *matching* is not qualified) -> create-only, same-G-volume hard-link publication of binary and receipt into established `large_artifacts/digits` -> unlink staged names -> **mandatory exact-path deletion of 10,000,000,001-byte decimal source** only on success; preserve small report/log and provenance. No unqualified scanner is needed to perform hash verification. Preserve existing G: `digits/`, `staging/`, `results/`, `logs/`, `scratch/` layout; do not invent a new `packed_v1` subtree. An intentional replacement workflow for existing published files remains to be designed safely (never delete the old good output first).

**Physical format:** `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, **two decimal digits per byte**: logical digits at offsets `2i` and `2i+1` are the **high** and **low** nibble of byte `i`. Every real nibble is 0–9; for odd-length streams a final low zero nibble is *padding*, not a real digit. Exactly `ceil(N/2)` bytes; **no decimal point, header, separators, or leading-digit discard**. Example phi `1.61803...` -> bytes `0x16 0x18 0x03 ...`. The scanner works at *every logical decimal-digit start offset*, both even and odd (odd starts cross physical byte boundaries). Ball encoding `FIXED2`: `3 -> "03"`, `35 -> "35"`; the packed storage is **not** ASCII and is **not** the old one-numeric-byte-per-digit format. Any future natural-width/other encoding must be separately versioned, specified and tested.

The completed 6 packed files will consume **30,000,000,000 bytes total (~27.94 GiB)** without copies; source originals and unverified temporary files are not retained. The old six 10^9-digit, one-byte-per-digit binaries and their historical registry can be retired through a separate controlled reconciliation; the owner waived mandatory full prefix-comparison against those originals. Historical code, small-scan outputs and documents should still be retained as scientific references.

## A4. Baseline experimental matching rules — Powerball, exactly as currently implemented

The **legacy numeric-byte** Powerball implementation is `outlandish_powerball_stage_a.py`; the newer **packed** Powerball implementation is `wsl_scan_packed_powerball.py`. Both use `FIXED2` and a fixed source/draw mapping; neither implements additional any-order variants for P1/P2. The packed scanner in supplied `OUTLANDISH_WSL.zip` has been inspected for this review.

For a single historical draw `D` with main drawn order `[a,b,c,d,e,f,g]`, Powerball `p`:

| Existing category | Existing *experimental* rule | Length | Present implementation |
|---|---|---:|---|
| **P1** | Exactly seven mains **in operator-drawn order**, followed immediately by exact `p` | 16 digit characters | Exact ordered tuple + PB lookup |
| **P2** | Exactly seven mains **in operator-drawn order**, with no requirement to examine the next PB | 14 | Exact ordered tuple lookup |
| **P3** | **Any six distinct** of seven drawn mains, **in any order**, followed immediately by `p` | 14 | Sorted six-main canonical lookup plus PB; all 7 possible omissions and 6! permutations logically accepted |

Conventions: each ball is 2 decimal digits with leading zero if needed; look for substrings at **every digit offset, not only even byte/nibble positions**. `P1` has a `P2` prefix; one offset may represent both categories. The `P3` PB occupies the **last** two-digit field; it is never freely permuted into the first six mains. Multiple draws can match the same sequence and must all retain attribution. `P3` deliberately does **not** require the six mains to be in drawn relative order.

**Current data indexing:** `build_index()` uses an exact 7-main order for P2, ordered 7+PB for P1, and **canonical sorted six-main subsets plus PB** for P3. Do **not** enumerate 5,040 P3 strings per draw in a new design merely because permutations are logically eligible. The old code's index consolidates shared keys while retaining all matching draw identities.

**Original experimental order extension, deferred owner record (`OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md`):**

| Category | Narrow drawn-order-type class | Any-order class | Disjoint difference class |
|---|---|---|---|
| P1 | `P1_drawn_order`: exact 7 drawn mains + PB (current P1) | `P1_any_order`: same seven main values any permutation, **PB fixed last** | `P1_reordered_only = P1_any_order AND NOT P1_drawn_order` |
| P2 | `P2_drawn_order`: exact 7 drawn mains (current P2) | `P2_any_order`: same seven main values any permutation | `P2_reordered_only = P2_any_order AND NOT P2_drawn_order` |
| P3 | `P3_drawn_subsequence_order`: six mains retain their relative order in the 7 drawn mains **after deleting one**; PB fixed last | `P3_any_order`: current P3 | `P3_reordered_only = P3_any_order AND NOT P3_drawn_subsequence_order` |

For P3, **seven** possible six-main drawn subsequences per draw, as distinct selections, versus **7 × 6! = 5,040** eligible six-main orders per draw. For P1/P2, one exact drawn order versus **7! = 5,040** distinct arrangements for each draw. These are **proposals to add**, not existing scanner capabilities. `any_order` includes the narrow drawn-order class: counts must never be added as though independent. A numerically sorted canonical lookup key is an implementation mechanism, **not** a rule requiring digits to be numerically sorted.

## A5. Oz Lotto experimental rules: initial intent and intentionally open questions

No actual Oz Lotto scanner or isolated historical reader is demonstrated in the supplied installed-source snapshot. Original owner concept:

| Experimental category | Basic selection intent | Length in FIXED2 |
|---|---|---:|
| **O1** | Seven main numbers in **operator-drawn order** | 14 digits |
| **O2** | Any six of seven main numbers and any **one of the three** supplementary numbers | 14 digits |
| **O3** | Any six of seven main numbers | 12 digits |

The owner wants Oz Lotto's additional **drawn-order vs any-order vs reordered-only** classifications analogously, but without suppressing genuine differences. The deferred proposal tentatively says:

- `O1_drawn_order` = seven mains exactly in their draw order; `O1_any_order` = any permutation of those seven; `O1_reordered_only` = any minus drawn.
- `O3_drawn_subsequence_order` = one of the seven relative-order six-main subsequences; `O3_any_order` = any six main values in any order; reordered-only as difference.
- `O2_drawn_subsequence_order` = six mains in original relative order followed by one selected supplementary; `O2_any_order` = any order of six mains **with the selected supplementary last**; reordered-only as difference. **This supplemental-last placement is a provisional proposal, not an owner-ratified fact**.

**Open O2 specification decisions for Claude to evaluate, then owner to settle:** Can the selected supplementary appear anywhere among the seven encoded ball slots, or only last? Is the operator order of the three supplementaries relevant to any specific classification? If two or three supplementaries can create distinct hits at the same offset/selection, should each selection produce a distinct identity-linked match record, and how are distinct positions/draws counted? Which six of the seven main balls were selected/omitted must be explicit. Is a seven-field O2 pattern semantically distinct from a seven-field O1 pattern at the same position for the same historical draw (given disjoint Oz Lotto main and supplemental pools)? What exact input provenance establishes true draw order? Do not silently decide these in the implementation.

For each selected six-main subset, there are 7 omission choices; O2 offers 3 supplemental choices; O3 offers 7 × 6! = 5,040 distinct sequences/draw; O2 **supplementary-last** offers 7 × 3 × 6! = 15,120 distinct sequences/draw, ignoring duplication across historical draws. If the supplementary can occupy any of seven positions, the O2 pattern space becomes **7 × 15,120 = 105,840** distinct strings/draw. These differences drastically change expected chance coincidences and performance; a choice is scientific, not cosmetic.

## A6. Existing reporting, measured evidence and the scientific-scanner qualification blocker

### A6.1 Established outputs

Both the original and packed Powerball scanners write match CSV records with: constant/file, historical draw number, P category, **zero-based start digit offset**, **exclusive end offset**, and exact matched decimal digits. The packed scanner writes:

- `matches.csv` for each attributed hit;
- `transitions.csv` per adjacent draw pair `W -> W+1` **only when both draws have at least one match in any category**, including counts per P category for W and W+1, and minimal signed positional deltas **anchored only on W's P1** to W+1's P1/P2/P3;
- `summary.json` with digest, counts, candidate filter count, cutoff, draw count, scan time, version-limited definitions and referenced output paths.

`candidate_offsets_examined` is the **number passing a prefilter**; it is **not** the number of all scanned digit offsets, a denominator for pattern probability, or match count. `transitions.csv` **does not presently calculate P3->P3** positional deltas. Historical adjacent P3/P3 examples were derived separately from saved matches. If W has no P1, P1-anchored deltas are empty; no scientific inference follows.

### A6.2 Previously observed results (not all formats are directly comparable)

| Source / scan | Observed P1 / P2 / P3 | Evidence / caveat |
|---|---|---|
| Legacy numeric-byte pi, 10^9 digits, 433 draws | `0 / 0 / 29` | Historical full scan, original algorithm |
| Legacy numeric-byte phi, 10^9 digits, 433 draws | `0 / 0 / 25` | Historical full scan, original algorithm |
| 100-million-digit **packed phi rehearsal**, same 433 draws | `0 / 0 / 3` | 3 reported P3 starting positions: `20,048,101`, `71,806,090`, `95,105,831`; full digest matched rehearsal receipt |
| 10-billion-digit **packed phi full scan**, 433 draws | `0 / 0 / 227` | **Unqualified scientific output**; complete G: file SHA matched receipt, but owner observed a possible early shared-prefix mismatch |

Owner-reported anomaly: at the beginning of the 10^10-digit phi scan, the progress/counts **looked different** from smaller-file results for what should be the same leading digits. Exact differing offsets/counterexamples and precise comparison conditions have **not** yet been supplied. This is a **scientific qualification blocker, not a demonstrated defect**. Compare by the **same logical prefix length**, constant identity, encoding, exact drawset hash, effective rule version, **match-start eligibility near prefix ends** and output-count definition; compare exact hit tuples, not just time-gated progress messages. A longer file can contain a match whose start lies just inside a shorter prefix but whose 14/16-digit pattern extends beyond its end: the shorter-file EOF rule and the longer-file scan differ unless the comparison bounds are made equivalent. Explicitly test this edge before concluding the code is wrong. The full phi scanner result cannot be endorsed merely because its SHA-256 passed; **integrity and scientific semantics are independent gates**.

Illustrative uniform-i.i.d.-decimal-digit null, **not** a proven property of constants: `433 draws × (7 × 6! = 5040 P3 sequences/draw) × ~10^10 starts / 10^14` ≈ **218.23 P3 matches** in a ten-billion-digit stream, before collision/finite-length corrections. Therefore 227 provisional P3 matches is broadly plausible **but not proof of correctness or predictive power**. Any-order expansions multiply the number of eligible patterns, and expectations must be normalised accordingly.

### A6.3 Owner-ratified qualification gate, before the next real scientific scan

After **all six** production binaries are complete:

1. Re-read the actual **current live** legacy and packed scanner source, input/format conventions and output definitions; determine whether and where behaviour differs.
2. Implement/execute **independently constructed** small truth-set reference matching (prefer simple, obvious code or manually audited fixed strings) and packed synthetic fixtures with **at least TWO known hits in each P1/P2/P3 category** plus comparable O1/O2/O3 tests **once Oz definitions are approved**; include intentional overlap P1/P2, different draws sharing keys, duplicate/reversed/order cases, negative examples.
3. Test **both BCD nibble phases**, all start-digit offsets, zero-based mapping, 12/14/16-digit lengths, P3 subset omission, fixed last PB, odd/even chunk boundaries, multi-chunk overlap, EOF/truncated/invalid nibble, exact 5 GB file metadata vs small test fixtures, duplicates/role validation and deterministic output ordering.
4. Reconcile **every qualifying hit** in the known 100m and common-prefix 10^9 comparisons, not merely total counts; confirm identical drawset digest and comparable prefix-end conditions. Do not run full six real scans before this passes.
5. Compare the optimised code and independent oracle; include deliberate mutations (reversed nibble order, byte-only alignment, omitted lookahead, wrong subset sorting) that MUST fail. Avoid circular tests that call the same decoding or matching helper in both reference and production paths.
6. Confirm reporter calculations and pair transitions against hand-worked tiny cases; verify no history leakage, missing draw attribution or double-counting. Quantify performance/memory only after correctness.

**No authorisation is given here** for immediate scanner modification or further real full-file runs while π / remaining constants are being generated.

---

# Part B — ChatGPT's assessment and proposed design for Claude to challenge

## B1. Recommendation, alternatives and the design boundary

**RECOMMENDATION [PROPOSED]:** **One shared, small core engine** to read high-first BCD digits and test configurable *selections/ordering*, **separate game/era rules and draw-data adapters**, then **one common match-event representation and shared analysis/reporting toolkit** that always partitions outputs by game and rule version. Start with **separate physical scans per game** for inspectability; combine scans only after evidence of a worthwhile speedup.

This is preferable to (A) two largely duplicated monolithic scanners, which risk divergent nibble decoding/chunk/EOF fixes, or (B) a fully general declarative matching-rule DSL, which could hide the science behind unnecessary abstraction. **A few explicit tested rule strategies** are the preferred middle ground. Reuse tested chunks of the working NumPy packed scanner; do not write a fresh large engine for elegance alone.

Claude should critically compare these alternatives, including a **hybrid adapter** that leaves the existing Powerball scan intact behind a common output interface. It may prove safer to refactor *after* qualification rather than before; this is a real design question, not an imposed refactor.

### B1.1 Logical topology

```text
Verified .packed.bin + receipt + manifest
             |
     Shared bounded BCD digit reader
     (high nibble first; every digit offset)
             |
     Shared candidate extraction/filtering
     (FIXED2; 6/7/7+special windows)
             |
     Matching strategy/index core
     (exact-order lookup; canonical unordered-set lookup;
      six-of-seven subset; relative-order predicate;
      special-ball role and fixed/variable placement)
             ^
             |
   +---------+--------------------+
   |                              |
Powerball game/era profile    Oz Lotto game/era profile
Powerball isolated adapter    Oz Lotto isolated adapter
   |                              |
   +--------------+---------------+
                  |
     Canonical attributed MATCH EVENTS
     (one scientific fact + versioned classifications)
                  |
       Shared derived assessments
     counts, overlaps, positions,
     W->W+1 relationships, null comparisons
                  |
       Distinct reports and exports:
       by constant x game x drawset x ruleset
```

**Isolation rule:** common *code* is not a licence to pool outcomes or train on one game while pretending to evaluate the other. Every artifact is keyed by constant SHA, `(game_id, draw_number)`, drawset SHA, encoding version, ruleset version and scanner source version.

## B2. The proposed call contract and rule-profile concepts

Illustrative API (not existing code):

```python
scan_constant(
    constant_id="phi",
    packed_path=".../digits/digits_golden_ratio_10_to_10.packed.bin",
    game_id="POWERBALL",
    drawset_id="POWERBALL_PREHOLDOUT_V1",
    ruleset_id="PB_FIXED2_ORDER_EXTENDED_V1",
    offset_start=0,
    offset_stop_exclusive=None,
)
```

A *validated* game/era profile should specify: valid main/special ranges and roles; distinctness within main and (where required) supplementary pools; official rule-era identity; exact supported draw fields/order provenance; experimental P1/P2/P3 or O1/O2/O3 selection rules; fixed two-digit encoding; special placement allowed in each category; ordered/subsequence/unordered predicates; classification nesting; drawset cutoff. It must not be an unreviewed user-supplied Python expression evaluated at runtime.

A small library of explicit strategies suffices initially:

1. `EXACT_ORDERED_7`: exact seven mains (and optionally a fixed terminal special).
2. `UNORDERED_7`: canonical sorted seven mains, with optional terminal special.
3. `UNORDERED_6_OF_7`: canonical sorted six-main subset, optionally followed by terminal special.
4. `RELATIVE_ORDER_6_OF_7`: membership match plus six-element relative order obtained by deleting exactly one element from the operator's drawn-seven sequence.
5. **Only if approved for Oz Lotto**: `SPECIAL_ANY_SLOT` with provenance of selected supplementary and its position; this is a separate semantic strategy, not an accidental side-effect of sorting all seven balls.

For P1/P2, `drawn_order` is checked after a seven-main set lookup (unless a direct exact-order lookup proves faster). For P3/O3/O2, the canonical six-main lookup identifies eligible draws and omissions; an explicit ordered-subsequence predicate classifies the qualifying subset. Never require the digit stream's numeric values to be sorted just because the index key is sorted. Preserve every matching draw association, including shared keys and cross-category overlaps. Avoid pre-generating 5,040/15,120/105,840 full strings per historical draw.

## B3. Separation of event identity, classification and selection provenance

**Recommendation [PROPOSED]:** Emit **one logical event per distinct** `(constant SHA, game, drawset/ruleset, draw_number, category, start_digit_offset, matched-length, eligible selected-main subset, selected special identity/role/slot)` **and attach nested classification flags**. Do not emit three duplicate event rows merely because the *same* event qualifies as `drawn_order`, `any_order` and `reordered_only`. Where categories actually differ (e.g., P1 and its P2 prefix) emit **separate category events linked by position**, not an artificial single official-division label.

Distinguish three different report totals:

- **Event count** (draw-specific category occurrences, can include more than one draw at the same location).
- **Distinct physical position count** (unique `(constant, start offset[, matched length])` per stated aggregation scope).
- **Distinct draw count / draw-position count** (not the same as matches, and historical draw identity includes game).

For O2 in particular, distinguish **number of distinct selected supplementary identities** from **number of physical substrings**. Require an explicit tie/dedup policy if the same slice supports multiple eligible interpretations; preserve a lossless child `selection_provenance` structure or an accompanying selection table, not silently collapse legitimate different draws/roles.

Suggested canonical `match_events.csv` fields (CSV + JSON manifest preferred to keep dependencies low):

| Column | Contract / note |
|---|---|
| `run_id`, `constant_id`, `packed_sha256`, `digits_total`, `format_id` | Verifiable binary identity; no assumption that filename alone suffices |
| `game_id`, `game_era_id`, `drawset_id`, `drawset_sha256`, `ruleset_id`, `scanner_version` | Exact inputs and definition provenance |
| `draw_number`, `draw_date` | Historical identity from isolated input; game ID retained |
| `category` | Original P1/P2/P3 or O1/O2/O3; never silently relabel |
| `start_digit_offset_0_based`, `end_digit_offset_exclusive` | Whole-file logical offsets, including integer digit at zero; `end-start` is 12, 14 or 16 |
| `matched_decimal_digits` | Exact FIXED2 substring for audit; preferably also parsed ball-role sequence |
| `selected_main_in_stream_order`, `main_drawn_order`, `omitted_main_id` | Distinguish actual substring from historical selection/relative-order test |
| `selected_special_value`, `special_role`, `special_draw_position`, `special_stream_slot` | PB vs supplementary provenance; null where absent |
| `any_order`, `drawn_order`, `drawn_subsequence_order`, `reordered_only` | Explicit applicability and nested Boolean semantics; nullable when a predicate is not meaningful |
| `classification_flags` / `selection_id` | If needed for extensions/multiplicity; avoid ambiguous repeated rows |

**Potential criticism Claude should assess:** These columns might be too verbose for first implementation. A smaller immutable core CSV plus a metadata manifest and optional detailed selection table may better preserve KISS and streaming performance. Report which fields are genuinely necessary at source, which can be derived without re-reading 5 GB, and how to avoid enormous per-event memory use.

Output should be streamable, deterministic in ordering, create-only in run-specific directories, and explicitly record partial/error state rather than silently publish success on an interrupted read. Never alter production constant binaries or registry merely to generate a scientific report.

## B4. Match classification and reporting rules

For every category `C`:

- `C_any_order` contains all members of `C_drawn_order` or `C_drawn_subsequence_order` where defined.
- `C_reordered_only = C_any_order - C_narrow_order`; this is a **disjoint subset**, not a third independent count to add.
- Preserve **baseline original P1/P2/P3** exact meaning and historical counts in versioned reports; extended classes do not retroactively redefine old P1/P2/P3.
- Overlap **across P/O categories** may be real, and P1 implies a P2 prefix for the same draw. Report intersections separately; do not add nested totals and call them unique hits.
- Record the **observed** two-digit values and role assignments as well as the sorted canonical keys used internally; never describe a sorted set index as proof of order.
- Offsets are always logical **digit** offsets, not BCD byte offsets; zero is the integer digit. Define end-exclusive boundaries consistently and require exact prefix-cutoff semantics.

Suggested reporting layers:

1. **`run_manifest.json` + immutable match events**: constant/hash, game, drawset/hash, versioned exact category definitions, digit window/coverage, source versions, output hashes, scan/verification status; one CSV per game/run (or files partitioned by category for convenience, not a redefinition).
2. **`counts_and_overlaps.csv`**: per-draw and all-draw event counts, distinct offsets, distinct draws, any-order/drawn/reordered partition, pairwise category intersections, named denominator and optional validation notes.
3. **`positions.csv`** (optional derived table): sorted occurrences by draw/category/order class to enable fast repeatable analysis without re-reading `.packed.bin`.
4. **`transitions.csv`**: for each consecutive historical draw W -> W+1, explicit category-pair and order-class pair, counts, nearest signed/absolute offset delta, tie convention, whether no matches (null), and total eligible pair count. Do not restrict to W P1 merely because the historical report did. Keep legacy P1-anchored output available under its existing version for regression.
5. **`summary.json`**: top-line audited counts, total/unique metrics, scanned range, time and memory/throughput, methodology ID, null-model assumptions, caveats and compatibility to legacy outputs. A visually rich later report should derive from these machine-readable artifacts, not be the only durable evidence.
6. **Cross-constant / cross-game research comparisons**: derived later from *separate* game datasets, with labelled multiple-comparison and null-model treatment. Never mash both games' draw numbers, winnings or rule descriptions into one untyped sequence.

**Transition caution:** A positional delta between arbitrary occurrences of W and W+1 does not predict either draw. The analysis must make the *direction* and position-order criteria explicit (closest-by-absolute-distance, forward-only nearest, all pairs, bounded window, etc.) and quantify how multiple matches per draw are handled. The current `closest_pair` uses minimum `(abs(delta), delta)` tie-break; any change should be versioned and tested with equal-distance ties. Zero matches should be represented explicitly in suitable summary statistics rather than disappearing from denominators just because a row was not written.

## B5. Proposed efficient scan algorithm

**One independent scan per `(constant, game, rule set, drawset)` initially**, using the established bounded NumPy packed reader. The engine can inspect **all** logical start offsets while cheaply rejecting invalid ranges/duplicates, then consult versioned indexes of eligible historical draw selections. It should recognise 12-digit six-main, 14-digit seven-main / six+special, and 16-digit seven+PB patterns in a **single scan** for a game if correctness and profiling justify it. An implementation may instead use a clear two-pass *small* derived analysis on an event dataset; no second read of the full 5 GB is required for new report types.

Important implementation invariants:

- Decode byte `b` into `(b >> 4, b & 0x0f)`; do **not** confuse byte index with start digit index. An odd start `k` spans a physical nibble boundary. Reject `A..F` nibble values in real digits.
- Read sufficient **lookahead** across chunks to support the longest 16-digit P1, including odd/even starts. Verify exact behavior when a pattern begins at the final 15/13/11 logical digits and when the finite input ends; never overread odd pad nibble as real data.
- For full-file digest verification, hash **each underlying packed byte exactly once**, not overlapping lookahead bytes. `sha256sum` can also be run independently. A correct digest says nothing about the correctness of candidate extraction.
- Keep at most bounded windows/candidate arrays/indexes in memory; do not expand the entire 10^10-digit input into a 10 GB NumPy array or enumerate huge permutation tables.
- Powerball special PB comes last for P1/P3; a numerically equal PB and main is *legal* due to separate barrels. Oz selected supplementary is distinct from its mains because the draw is from one 47-number barrel. Each game/role has its own validation.
- Validate actual game/era draw fields, historical order and unique main numbers before indexing. For Oz Lotto, explicit 47-number modern era + three supplementaries; reject unsuitable older-era data unless a separate historical ruleset exists.
- Avoid non-deterministic output order from hash table iteration; sort or specify stable write ordering; identity and duplicate policy must not depend on machine run order.
- Preserve the existing separate-scanning isolation and **do not** optimize by accidentally combining both games' matching index or incorrectly using one game's rule filter on another.

**Performance design question for Claude:** Is a single NumPy candidate extraction using both 6-main and 7-main windows appropriate, or is a high-level strategy dispatcher per category too slow? Propose benchmarks on small/medium **synthetic** and pre-authorised known files only *after qualification*, focusing on sustained throughput, candidate density, memory and I/O without overengineering Cython/Numba before profiling. Extra dependencies are undesirable unless measurements warrant them.

## B6. Null-model, scientific interpretation and optional assessment methods

At `N` independent uniform decimal digits, an eligible exact `L`-digit sequence at a given start has probability `10^-L`. For distinct balls and a fixed special placement, approximate eligible sequences per historical draw are:

| Category, proposal | Eligible sequences per draw | Length `L` | Comment |
|---|---:|---:|---|
| P1 drawn | 1 | 16 | Seven exact mains then PB |
| P1 any-order | `7! = 5,040` | 16 | PB fixed last |
| P2 drawn | 1 | 14 | Seven exact mains |
| P2 any-order | `7! = 5,040` | 14 | Seven mains permuted |
| P3 drawn-subsequence | `7` | 14 | Seven ways to omit one main; PB last |
| P3 any-order (baseline) | `7 * 6! = 5,040` | 14 | PB last |
| O1 drawn / any | `1 / 5,040` | 14 | Seven mains |
| O2 drawn-subsequence / any (special last) | `7*3=21 / 7*3*6!=15,120` | 14 | Provisional O2 convention |
| O3 drawn-subsequence / any | `7 / 5,040` | 12 | Six mains |

Expected event-count approximation for a fixed category on `D` historical draws with `S` distinct eligible sequence patterns per draw and `N-L+1` possible start positions: `E[count] ≈ D*S*(N-L+1)/10^L`. Exact counting/variance needs to address repeated patterns across draws, overlaps among correlated windows and category nesting; **do not** use the approximation as a calibration certificate or infer a Poisson distribution without checking. For illustration, `D=433`, `N=10^10`, P3 any-order: `433*5040*~10^10/10^14 ≈ 218.23` expected *draw-attributed events*, not necessarily distinct start positions. Compare the provisional phi 227 only as a rough sanity check, not validation.

Recommended assessment logic to debate:

- Clearly separate expected opportunity counts for different categories, order classes, patterns, per-draw and per-constant exposures. `reordered_only` expectations are differences of nested classes, not an independent test family.
- Build null-world/artificial-digit trials, seed and provenance recorded, **after matching correctness**. Consider both uniform-digit null and more structured reference processes if an observation motivates them. Multiple constants, categories, lookback choices and transition metrics introduce multiplicity and overfitting risk.
- Report descriptive distance distributions for W→W+1 at least under a baseline of independently placed matches with observed or simulated frequencies. Do not claim an excess of near-neighbours without a measurable, predeclared statistic and appropriate null.
- Exploratory patterns can be kept and examined even when non-significant; mark status and limitations. A method handed to the parent project requires a separate deterministic **past-only** forecast construction, immutable data/parameter decisions, controlled evaluation and appropriate negative results.

## B7. Qualification implementation and release sequence (proposed, subject to review)

**Gate 0 — Finish data production**: all six packed files generated with `-verify:1`; complete persisted-file SHA-256 check before publication; final file + receipt; exact 10 GB source deletion; logs retained; no further unqualified 10^10 scientific scans. Fix packed registry only by a small separately reviewed reconciliation, not by repurposing the legacy byte-format registry.

**Gate 1 — Audit existing baseline**: take fixed source snapshot/hashes of existing legacy and packed Powerball readers. Review each candidate predicate, exact key generation, nibble/chunk/EOF handling, drawset and cutoff, event-count semantics and output determinism. Identify exact benchmark cases with shared-prefix discrepancy. Correct only independently demonstrated defects in a small isolated patch, preserving baseline compatibility.

**Gate 2 — Build independent reference oracle and synthetic fixtures**: preferably a plain straightforward Python/hand-verified matcher that operates on tiny explicit digit strings rather than reusing the optimized BCD decoder or its indexes. Require **at least 2 known P1 hits, 2 P2 hits and 2 P3 hits** and, once approved, at least 2 per O category; additionally drawn vs reordered variants, explicit nonhits, repeated keys across draws, offset parity and all boundaries. Compare exact tuple sets (`draw ID, category, start, end, selected numbers, classification`) and reports. Do not invent real historical draws to satisfy this synthetic test; clearly mark synthetic identities.

**Gate 3 — Regression and reconciliation**: compare old numeric-byte and new packed Powerball scan on **identical verified logical digit substrings** where available (owner waived mandatory full old-binary prefix comparison, so tests must not *require* retaining legacy 1e9 binaries). Compare archived 100m/1e9 matches when evidence is available, boundary-normalised and with hashed drawset identity; don't confuse differing source files, partial scans, or boundary-crossing matches with a defect. Any real scanner discrepancy remains a blocker until explained.

**Gate 4 — Ruleset extension**: only now add P1/P2 any-order and P3 relative drawn-order flags. Keep baseline output and exact existing category semantics with versioned fields. Settle Oz Lotto era/source/O2 options with the owner, then implement its separate profile/adapter and acceptance tests against the same core (or present evidence a separate engine is safer).

**Gate 5 — Scientific reporting and assessment**: materialise event datasets, counts, nested-overlap summaries, category-pair positional transitions, null comparisons and audit provenance. Derive reports entirely from saved match datasets where feasible. Review accuracy, performance and file sizes.

**Gate 6 — Production scientific scans**: only once all gates pass, execute six constant scans for Powerball and optionally separate Oz Lotto scans when its reader and rules are approved. Use repeatable ruleset/drawset/manifests; preserve old unqualified phi diagnostic as a separate audit artifact, not as accepted output. Do not rerun all six merely because report rendering changes.

## B8. Specific review questions — require answers, not just a general endorsement

Please respond to each, with `AGREE / DISAGREE / MODIFY / ALTERNATIVE`, reasons, and a recommended action:

1. **Architecture choice:** shared core + per-game profiles vs separate scanners vs hybrid thin shared reader/output layer. Where is the best *minimum* interface boundary?
2. **Scientific equivalence:** do the actual original P1/P2/P3 implementations precisely match Part A? Identify counterexamples (especially P3 subsets, PB/main same value, nested P1/P2 and shared draw keys).
3. **Old-versus-new mismatch:** what is the most efficient rigorous *diagnostic* sequence for the reported prefix anomaly? Are prefix-end effects, compare-window mismatches, BCD odd offset or filtering plausible? What exact files and metadata should the owner preserve?
4. **Oz Lotto O2:** supplementary last vs any slot vs additional role-specific variants. Which is scientifically coherent with the original owner intent, feasible and simplest? Should both be tested as separately labelled hypotheses? How should selected supplementary identity, source order and multiple attributions be represented?
5. **Oz Lotto history:** what independent checks establish the effective first 47/3 draw, trustworthy chronological draw order, modern-era dataset and Oz-only cutoff? Should older 45/2-era results be out of scope initially?
6. **Event identity/dedup:** is one event with nested classification flags correct? How should multiple eligible draws/choices, overlapping categories, multiple selections and same-position matches be modelled without loss or double-counting?
7. **Data contract:** which event fields are truly essential? Would a compact event table plus run metadata/selection detail be better than the proposed wide CSV? Should `special_stream_slot` be nullable versus a distinct rule-id class?
8. **Fast matching:** can the canonical combination lookup, subset classification and odd-offset packed decode be implemented once without hidden branches/complexity? What is the algorithmic/CPU/I/O risk at N=10^10?
9. **Reference tests:** how to make synthetic oracles *genuinely independent*, with guaranteed ≥2 known hits per category, deliberate wrong-implementation cases, end-of-prefix/chunk/EOF tests, and stable comparison to existing baseline?
10. **Transition analysis:** which W→W+1 pair metrics are meaningful and tractable? How should zero-hit draws, multiple hits, tie-breaking, signed versus absolute deltas, reversed constant positions and adjacent-draw identity be handled? Which data should be stored vs derived?
11. **Null models:** are the listed expected counts mathematically sound for draw-attributed event counts, including role overlaps and repeated historical selections? What exact, simulation or permutation alternatives would you recommend for meaningful positional claims and multiple-testing control?
12. **Rules/versioning:** how to keep baseline P-category semantics and reports reproducible while extending any-order classes? How much explicit version machinery is appropriate without compromising KISS?
13. **Safety/governance:** does any proposed workflow risk reading restricted outcomes, confusing the standalone source policy, operating on unverified binaries, modifying original data, unsafe file replacement, or silently changing parent-project methods?
14. **Implementation plan:** provide the fewest safe increments, test/rollback points, estimated complexity and any tasks **not worth doing**. Identify whether shared engine should come **before** or **after** the original packed scanner is independently qualified.
15. **Optional ideas:** Are there alternative designs or experimental classifications the current proposal misses, such as role-labelled canonical tuples, automata, sparse direct-key lookups, generic event grammar, unique-count vs multiplicity analysis, or additional explicitly separate representation experiments? Recommend only those with a compelling scientific or implementation benefit.

### Requested response structure

1. **Executive verdict:** shared-engine recommendation `AGREE / DISAGREE / MODIFY`, short rationale and confidence/limitations.
2. **Blocking errors in Part A:** correct any factual/rule/source/code misunderstandings with references to current inspected source, distinguishing hard errors from material not available.
3. **Review table:** each major Part B design decision, disposition, justification, recommended alternative if any, impact/priority.
4. **Oz Lotto decisions requiring the owner:** numbered options with pros/cons, no unilateral pseudo-ratification.
5. **Concrete qualification plan:** synthetic fixture design, oracle independence, old/new reconciliation, pass criteria, source snapshots.
6. **Minimum viable architecture and staged implementation:** modules/interfaces/data records, how to reuse existing code, what is intentionally deferred, and straightforward rollback.
7. **Questions for the owner (only genuine blocking decisions)**, and a clear statement of what source/code is still missing from this review.

Please **challenge the proposed design as an independent reviewer**; do not treat ChatGPT's recommendation as an instruction to agree. If you identify a compelling reason *not* to share the scanner engine, say so and propose the smaller, safer solution.

---

# Part C — Source inventory, verification pointers and review limitations

**Project / installed-state sources to inspect, in order of relevance** (uploaded indicative archives and user's live repository may differ):

1. `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md` — owner-recorded deferred order extensions; **proposal/decision record, not an implementation specification**.
2. `0_outlandish_thought_experiment_01_scope.txt` — original owner idea, matching definitions, W→W+1 and Oz Lotto intent.
3. `outlandish_powerball_stage_a.py` — original numeric-byte Powerball FIXED2 scanner and original transitions.
4. `wsl_scan_packed_powerball.py` and `wsl_format.py` — packed high-nibble-first reader, fixed existing Powerball semantics, hash-in-scan, latest scanned source in supplied ZIP. `wsl_verify_windows.py` and `wsl_convert.py` — receipt and conversion identity, readback and validation assumptions.
5. `POWERBALL_preholdout_only.csv` — approved isolated Powerball development CSV (do not replace with master or current outcomes; verify hash and cutoff).
6. `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md` — early measured scan data and actual transition/report limitations.
7. `OUTLANDISH_01_Consolidated_Handover_v6.md` **plus** `OUTLANDISH_01_Living_Handover_Addendum.md` revision 0.6 — historical baseline and owner's later controlling changes. Rev0.6 documents completed phi; this review request additionally includes **subsequent owner-reported completed e** and apparent π-in-progress status as of its preparation.
8. `OUTLANDISH_WSL.zip` and `OUTLANDISH_01_indicative_original.zip` — indicative source snapshots; hashes/sizes in earlier handovers; **not** substitutes for inspecting the current live checkout before applying changes.
9. Existing `G:\OUTLANDISH_01\large_artifacts\results\packed_run_20261108T012705Z_43564c3c\` — **unqualified** complete phi scan event CSV and summary; 100m packed rehearsal results on T:; historical 1e9 numeric-byte match CSVs and summary, if still retained. Preserve them to reconcile actual shared-prefix hit identities.
10. Official game-rule/public context (not a new source policy for results):
    - Powerball: https://www.lotterywest.wa.gov.au/games/powerball
    - Oz Lotto: https://www.lotterywest.wa.gov.au/games/oz-lotto
    - Powerball two-barrel FAQ: https://www.lotterywest.wa.gov.au/frequently-asked-questions
    - Oz Lotto May-2022 rule-change announcement: https://www.lotterywest.wa.gov.au/lotterywest/media-centre/bigger-prizes-and-more-winners-with-oz-lotto-game-change

**Evidence limits:** This review document relies on the named source snapshots, historical artifacts, external official public pages, and pasted owner terminal output. It has **not** independently opened the owner's live G:/E:/T: storage, used his live Git HEAD, verified the Oz historical draw schema, proved the scientific correctness of the packed scanner, or observed π complete. Where these are required, the reviewer should request the smallest relevant artifact or read-only inspection, not guess.

**End of review request.**
