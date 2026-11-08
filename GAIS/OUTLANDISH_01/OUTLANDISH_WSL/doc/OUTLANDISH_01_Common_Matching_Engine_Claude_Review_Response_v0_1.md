# OUTLANDISH_01 - Common Matching Engine: Independent Claude Review Response v0.1

**Responds to:** `OUTLANDISH_01_Common_Matching_Engine_Claude_Review_v0_1.md` (ChatGPT draft, 8 Nov 2026)
**Prepared:** 8 November 2026, Australia/Adelaide
**Reviewer:** Claude, acting as independent technical and scientific design reviewer; relayed by the GitHub project owner
**Status:** REVIEW OPINION ONLY. Nothing here is ratified. No code was written, no repository or data was touched.

---

## 0. Evidence base and limits of this review

- Read in full: the review request (Parts A, B, C).
- NOT available to this reviewer: any scanner source (`outlandish_powerball_stage_a.py`, `wsl_scan_packed_powerball.py`, `wsl_format.py`), the deferred order-matching record, the original scope text, `POWERBALL_preholdout_only.csv`, and the three result sets (1e8 packed rehearsal, 1e9 legacy, 1e10 packed phi).
- Consequences:
  - Everything labelled [AS-INSPECTED] in Part A is taken as ChatGPT's reading. I cannot confirm it to file:line. Where this review says "check that the code ...", that is a verification item, not a finding.
  - Question B8.2 (does the code match Part A?) is answered as a ranked list of specific traps to test for, not as a verdict.
- I did not re-open the Lotterywest-GOV pages. The official-division tables in A2 agree with my own understanding of both games' current formats; I found no error in them.

---

## 1. Executive verdict

**Shared engine: AGREE, with one significant simplification (MODIFY).**

ChatGPT is right that the dangerous code is the BCD reading, odd-offset field extraction, chunk lookahead and EOF handling, and that this must exist exactly once. It is also right to keep Powerball and Oz Lotto as separate scans, separate drawsets and separate result sets.

Where I disagree is the shape of the matching layer. Part B proposes a library of named strategies (`EXACT_ORDERED_7`, `UNORDERED_7`, `UNORDERED_6_OF_7`, `RELATIVE_ORDER_6_OF_7`, `SPECIAL_ANY_SLOT`) selected per category. That is more machinery than the problem needs. Every category in both games, including all proposed drawn-order / any-order / reordered-only classes, reduces to two things:

1. **One kind of lookup at scan time:** a numerically sorted canonical key of the ball fields in a window (with the special ball as a separate trailing component where the category has one), looked up in a tiny index built from the drawset(s).
2. **One kind of classification after the scan:** pure functions of (matched digits, historical draw record) that set flags - `drawn_order`, `drawn_subsequence_order`, special slot, selected/omitted mains, and so on.

Ordering is never part of the lookup. The existing exact-drawn-order P1 and P2 categories become `any-order hit AND drawn_order flag`. The engine then has a single code path (one extraction, one filter, one index lookup, one event writer), and every rule-definition question moves into a small post-processor that runs over hundreds to tens of thousands of rows in seconds, never over 5 GB. Baseline P1/P2/P3 semantics are reproduced exactly as filters on the event table and are regression-testable against the old scanner's outputs.

Two additions matter more than the architecture debate:

- **Decoy drawsets as the null model.** The index lookup is the cheap part and the digit pass is the expensive part, so the engine should accept several drawsets per run: the real one plus K synthetic, clearly labelled random drawsets with identical structure. They ride along in the same index at near-zero extra cost and yield an empirical distribution of "how many hits does a random drawset get in THESE digits". No assumption that the constant's digits are i.i.d. uniform is needed. This is the single most useful safeguard against a misleading conclusion that the project can buy.
- **The narrow-order classes are expected to be empty.** Under the uniform null, across all six constants, the project should expect about 0.003 P1-drawn hits, 0.26 P2-drawn hits and 1.8 P3-drawn-subsequence hits in total (Appendix A). One or two narrow-order hits somewhere in the project is the expected outcome, not an anomaly. Every count must be printed beside its expectation so this cannot be misread later. The classes are still worth computing (they are free flags) but they cannot support W->W+1 analysis; only the any-order classes have enough events for that.

Confidence: high on the matching and null-model reasoning (elementary combinatorics); moderate on the architecture because the existing NumPy scanner has not been seen; none on the state of the code.

Sequencing: build the independent oracle and fixtures and run them against the EXISTING packed scanner first; reconcile the existing 1e8/1e9/1e10 result CSVs (no scanning required); then refactor into the shared engine with that harness in place. Refactoring before qualifying would make it impossible to tell whether a discrepancy came from the old code or the new.

---

## 2. Part A - errors and material omissions

**Hard errors found: none** in the game rules, the pattern-space arithmetic, the packed-format description or the null-model estimate. The figures 5,040 / 15,120 / 105,840 / 218.23 and the `0x16 0x18 0x03` example are all correct.

**Material omissions / traps** (not errors in the document, but things the design must handle explicitly):

**2A. Powerball equal to a main.** Roughly 1 draw in 5 has its Powerball numerically equal to one of its seven mains (on average 4 of 7 mains lie in 1-20, so P ~ 4/20). If the candidate distinctness check is applied across ALL fields of a P1 or P3 window (8 or 7 fields) instead of across the main fields only, those draws silently lose P1/P3 eligibility. Part A states the rule correctly; whether the code does is the single most likely semantic defect and needs a named fixture (a draw with PB == a main, planted as both P1 and P3).

**2B. Order provenance is testable and has not been tested.** If a source lists mains in ascending order, "drawn order" categories silently become "ascending order" categories. Under true drawn order only about 1 draw in 5,040 is ascending by chance. So: count rows of `POWERBALL_preholdout_only.csv` whose `Drawn_1..7` are ascending. Expected about 0.09 of 433. If it is 433, the file is sorted and every drawn-order statement to date is mislabelled. The same one-line test decides whether any Oz Lotto source actually carries drawn order. Do this before anything else.

**2C. Within one draw, a matching window has exactly one interpretation.** For P3, a window of six distinct mains determines the omitted main uniquely. For O2 under either convention, because mains and supplementaries are disjoint within a draw, the window's six mains and one supplementary are uniquely determined. Part B's concern about "multiple eligible interpretations at the same slice" therefore arises only ACROSS draws (two draws sharing a key), which the existing attribution-list index already handles. No tie or dedup policy is needed beyond "one event per (drawset, draw, category, start offset)".

**2D. Supplementary-last is ChatGPT's narrowing, not the owner's original definition.** A5 quotes the original intent as "any six of seven main numbers and any one of the three supplementary numbers", with no position stated. The deferred record then proposes supp-last. This is a genuine owner decision (section 5), and the difference is a factor of 7 in expected hits.

**2E. Expected-zero classes.** Parts A and B present the drawn-order classes as hypotheses on an equal footing with the any-order classes. Statistically they are not (Appendix A), and the reporting must say so on the same line as the count.

**2F. A unifying definition for Oz drawn-subsequence order.** Define it as: the seven selected values appear in the window in the same relative order as in the full ten-ball drawn sequence. Because supplementaries are drawn 8th-10th this automatically forces the supplementary last and the six mains in relative drawn order, and it is meaningful under the any-slot convention too. Expected ~0.002 x D per constant, i.e. empty, but it is the only Oz order class needed.

**2G. Minor.** N = 10^10 is even, so production files have no pad nibble; pad handling matters only for fixtures and must still be tested.

---

## 3. Review table - Part B design decisions

| # | Part B item | Disposition | Reasoning / alternative | Priority |
|---|---|---|---|---|
| B1 | Shared core (reader, extraction, candidate filter) + per-game profiles + shared event representation | AGREE | The bug-prone code is digit handling; it must exist once. Profiles are data (ranges, roles, lengths, enabled families), not code. | High |
| B1 | Separate physical scans per game | AGREE | Simpler to audit; 12 scans in total is cheap. Never merge games into one pass or one index. | High |
| B1 | Reject (A) duplicated scanners and (B) a rule DSL | AGREE | Both bad for the stated reasons. | - |
| B1 | Hybrid: keep existing Powerball scanner behind a common output layer | ALTERNATIVE | Keep the existing scanner untouched as the regression reference, not as a production component. Once the new engine reproduces its events on the 1e8/1e9 prefixes, retire it to the scientific-reference archive. | Medium |
| B2 | Library of five named strategies | MODIFY - one mechanism | Every lookup is "sorted canonical key of ball fields -> attribution list". Order, relative order and slot are post-hoc flags on events. `RELATIVE_ORDER_6_OF_7` and `EXACT_ORDERED_7` cease to exist as strategies; `SPECIAL_ANY_SLOT` becomes one more key family (sorted 7 of {6 mains + 1 supp}). | High |
| B2 | Profile must not be runtime-evaluated Python | AGREE | Frozen JSON per game, hashed into the run manifest. | High |
| B2 | Do not pre-generate 5,040 / 15,120 / 105,840 strings per draw | AGREE | Canonical keys: 1 to 21 per draw per family. | High |
| B3 | One event per distinct (..., draw, category, start offset) with nested flags; no duplicate rows per class | AGREE | Per 2C, no further dedup policy is needed. | High |
| B3 | P1 and its P2 prefix as separate linked events | AGREE | Different lengths and categories; link by (draw, offset). | - |
| B3 | Three distinct totals (events / distinct positions / distinct draws) | AGREE | Always report all three with the denominator named. | Medium |
| B3 | Wide ~25-column event CSV | MODIFY | Run-level constants go in `run_manifest.json`. The event CSV carries the irreducible fields (drawset_id, draw_number, family/category, start_offset, matched_digits) plus derived flags marked as derived and re-computable by the classifier. Width is irrelevant for size (thousands of rows); it matters for what counts as primary evidence. | Medium |
| B4 | any_order contains the narrow class; reordered_only is a difference; never add nested totals | AGREE | Also print expected count per class beside each observed count. | High |
| B4 | Preserve baseline P1/P2/P3 exact meaning in versioned reports | AGREE | Implement as explicit filters: `P1_baseline = K7S hit AND drawn_order`; `P2_baseline = K7 hit AND drawn_order`; `P3_baseline = K6S hit`. Test these against the old scanner's outputs. | High |
| B4 | Reporting layers 1-6 | AGREE with MODIFY | Layers 2-5 are derived from layer 1 by a separate tool that never opens the packed file. Transitions: do not anchor on P1 (expected 0); make P3any->P3any and P2any->P2any the predeclared primary pairs. | Medium |
| B4 | Tie convention min(abs(delta), delta) | AGREE | Keep, version it, test with an equal-distance fixture. | Low |
| B5 | One scan per (constant, game, drawset, ruleset) | MODIFY | One scan per (constant, game) with ALL drawsets for that game (real + decoys) in the index and all key families in one pass. Ruleset is a post-processor concern and does not trigger rescans. | High |
| B5 | Implementation invariants (nibble decode, lookahead, hash each byte once, bounded memory, determinism) | AGREE | Add: range-check first on all offsets, compact to candidates, then distinctness and sort on candidates only (candidate density ~6e-4 for seven 1-35 fields, ~5e-3 for seven 1-47 fields, ~1e-2 for six 1-47 fields). | High |
| B5 | Numba/Cython only after profiling | AGREE | NumPy should be adequate: order of an hour per constant per game, dominated by field extraction and range masks. | - |
| B6 | E ~ D x S x (N-L+1) / 10^L | AGREE | Correct for draw-attributed events under i.i.d. uniform digits; Poisson is a good approximation for these rare, effectively non-overlapping patterns. But do not rely on it: use decoy drawsets (empirical null in the actual digits) and a draw-label permutation test for W->W+1 (section 6.6). | High |
| B6 | Null-world artificial-digit trials | ALTERNATIVE | Decoy drawsets against the real digits are cheaper, assumption-free, and answer the question actually asked. Synthetic digit streams remain useful only as test fixtures. | High |
| B7 | Gate order 0-6 | MODIFY | Gates 2 and 3 need no 10^10 scanning and negligible CPU; they may start before all six constants finish if the owner revises his sequencing (section 8). Engine refactor (Gate 4) only after Gates 2-3 pass against the existing scanner. | Medium |
| B7 | Gate 6: do not rerun six scans for report changes | AGREE | Guaranteed by the event-table / post-processor split. | - |

---

## 4. Answers to B8 questions 1-15

**1. Architecture.** Shared: reader, extraction, candidate filter, key index, raw event writer, classifier, reporter. Per game: a profile (main range, special range, families enabled with their field counts, cutoff draw number, era identity) and a drawset adapter (CSV reader with cutoff refusal before parsing, order-provenance test, era check). Minimum interface: `scan(packed_path, profile, drawsets) -> raw_events` and `classify(raw_events, profile, draw_records) -> classified_events`. Nothing else crosses the boundary.

**2. Scientific equivalence.** No verdict possible without source. Traps to test, in order of likelihood: (a) distinctness applied across the PB field (2A); (b) P3 index missing one of the seven omissions, or a six-subset not re-sorted after omission; (c) off-by-one between legacy and packed offset conventions (integer digit at 0, 1-based, or decimal point skipped); (d) matches straddling a chunk boundary missed or duplicated; (e) odd-offset starts near chunk ends; (f) a PB range check (1-20) applied to the seventh field of the 14-digit window when testing P2 - a P2 window has no PB, and this would wrongly exclude P2 hits whose seventh drawn main exceeds 20.

**3. Prefix anomaly diagnostic.** Step 1, no code and no scanning: take the 1e10 phi event CSV (227 rows). Filter to `end_offset <= 1e8`; the result must be exactly the three rehearsal rows (starts 20,048,101; 71,806,090; 95,105,831) with identical matched digits. Filter to `end_offset <= 1e9`; the result must be exactly the 25 legacy phi rows (allow a documented constant shift if the legacy convention differed; try shifts of -1, 0, +1). Step 2: any row in one set and absent from the other is a concrete counterexample; read the digits at that offset from the packed file with a ten-line independent reader and decide which run is right. Step 3: only if Step 1 agrees, dismiss the progress-message observation as a chunk-timing artefact. Preserve: the three result directories, the drawset CSV with SHA-256, the exact scanner source used for each run (SHA-256 of each `.py`), console logs and receipts. Do not rescan anything to diagnose this.

**4. Oz O2.** Section 5, decision 1. Implement the any-slot key family and record `special_stream_slot`; supp-last is then a flag/filter. The owner chooses which is the PRIMARY predeclared class.

**5. Oz history.** Section 5, decisions 2-4. Modern era only, with the first modern draw derived from the data (count of numbers per draw, maximum value) and cross-checked against the announcement. Older eras out of scope.

**6. Event identity.** AGREE: one event per (drawset, draw, category, start offset) with flags. Cross-draw sharing produces several events at one offset, each attributed. Per 2C no other multiplicity exists.

**7. Data contract.** Essential at source: `drawset_id, draw_number, family, start_offset, matched_digits`. Everything else is derivable; store derived flags for convenience but require a test showing the classifier reproduces them from the essentials. `special_stream_slot` is a nullable column, not a rule class; the rule class is the key family.

**8. Fast matching.** Yes, once, with no hidden branches. Decode each chunk to a uint8 digit array (two digits per byte, plus 15 digits of lookahead from the next chunk). Fields `F_j[k] = 10*d[k+2j] + d[k+2j+1]` for j = 0..7 via strided slices; odd and even k are handled identically, so there is no "nibble phase" logic anywhere. Range masks over all offsets; compact; distinctness and sort on candidates only; pack the sorted key into one int64; `np.searchsorted` against each family's sorted key array. The risk at N = 10^10 is wall-clock time, not memory or complexity. Keep chunk size a parameter (tens of MB) so fixtures can use tiny chunks.

**9. Reference tests.** Section 6.

**10. Transitions.** Section 6.6.

**11. Null models.** The per-draw sequence counts and the expectation formula are correct. Repeated keys across draws reduce the number of distinct strings slightly (negligible at 433 draws). The Poisson approximation is adequate for these rare patterns; confirm it empirically from the decoy counts. For positional claims use the draw-label permutation test (6.6). Multiplicity: predeclare ONE primary statistic per game; report everything else as exploratory with the number of comparisons stated.

**12. Versioning.** `profile_id` + hash, `drawset_id` + hash, `scanner_version` (source SHA-256), `classifier_version`. The raw event table depends only on the first three; the classifier re-runs freely. That is all the version machinery required.

**13. Safety.** Section 7.4. No proposed workflow reads restricted outcomes provided the Oz holdout is defined and split BEFORE any Oz scan, and the scanner verifies the drawset file's hash against the run manifest. Decoy drawsets must carry obviously synthetic draw numbers and live only in the run directory.

**14. Plan.** Section 7. Shared engine AFTER the oracle and fixtures have been run against the existing scanner and the CSV reconciliation is complete.

**15. Optional ideas.** (a) Decoy drawsets - recommended unconditionally. (b) An `ascending_order` flag: published order is one specific permutation, free to compute, a natural third order class; owner decides whether to report it. (c) A Powerball 12-digit family "six of seven mains, no PB" analogous to O3: about 22,000 events per constant and far richer W->W+1 statistics; it is a NEW hypothesis, so owner decision. (d) Aho-Corasick / automata: not needed - the canonical-key approach is equivalent and simpler in NumPy. (e) Role-labelled canonical tuples: this is exactly what the key families are.

---

## 5. Oz Lotto decisions requiring the owner

Each is presented as question / why it matters / recommendation / options.

**Decision 1 - Where may the selected supplementary sit in an O2 window?**
Why: a factor of 7 in expected hits (supp-last ~1.5 x D per constant; any-slot ~10.6 x D), and a different hypothesis. The original scope text fixes no position; supp-last is a later narrowing.
Recommendation: implement any-slot as the key family and record the slot; declare supp-last the PRIMARY class (closest analogue to P3) and any-slot a labelled secondary class. One pass computes both; nothing is lost.
Options: (1) supp-last only; (2) any-slot only; (3) both, supp-last primary [recommended]; (4) both, any-slot primary.

**Decision 2 - Which Oz Lotto era is in scope?**
Why: before the May 2022 change Oz Lotto was 7 + 2 from 45 (and earlier still, 6 from 45). Those draws cannot be O1/O2/O3 as defined.
Recommendation: modern 7 + 3 from 47 only. Determine the first modern draw from the data itself (first draw with ten numbers or any value above 45), cross-check against the announcement, and record the draw number in the profile. Older eras are a separate experiment if ever wanted.
Options: (1) modern only [recommended]; (2) modern now, a separately defined 45/2 ruleset later.

**Decision 3 - What if the approved Oz source does not carry drawn order?**
Why: if the source lists numbers ascending, drawn-order classes are impossible for Oz Lotto and must be marked not-applicable rather than computed on sorted data.
Recommendation: run the ascending-row test (2B) on the acquired Oz data. If it is sorted, Oz Lotto gets any-order classes only; do not substitute an unapproved source to obtain order.
Options: (1) proceed with any-order only if sorted [recommended]; (2) hold Oz Lotto until an approved ordered source exists.

**Decision 4 - Oz holdout size and cutoff.**
Why: the parent project's no-leakage rules apply, and the cutoff must exist before any scan.
Recommendation: same construction as Powerball (last N draws reserved; exclusive cutoff draw number recorded in the profile and refused by the adapter before parsing). N is the owner's call.

**Decision 5 - Does the supplementary's own drawn position (8th/9th/10th) create classes?**
Recommendation: record `special_draw_position` on every O2 event; create no classes from it. The ten-ball relative-order definition (2F) is the only Oz order class needed.

---

## 6. Qualification plan

### 6.1 Independent oracle
- Operates on a plain Python string of decimal digits and a list of draw records. For every offset i and category: take `s[i:i+L]`, split into two-character fields, `int()` them, and apply the written definition literally with sets, `sorted()` and sequence comparison. No index, no NumPy, no helper shared with production.
- Written by a different party from the engine. In the owner's workflow the reviewer side writes the oracle and the coder writes the engine. Target under 150 lines.
- Practical limit ~10^7 digits per run in pure Python. Larger comparisons are engine-vs-engine (new vs old), not engine-vs-oracle.

### 6.2 Fixtures
- Background digits: all `9`. A `99` field is invalid in every game, so the background can never contribute a hit; every hit is planted and known.
- Independent trivial packer for fixtures: `byte = (int(d[2i]) << 4) | int(d[2i+1])`, low nibble 0 in the last byte when the length is odd. Not `wsl_convert.py`.
- Synthetic drawset: draw numbers from 9,000,001, synthetic dates, valid structure. Include a draw with PB equal to a main; two draws sharing a six-of-seven subset and PB; a draw whose seventh drawn main exceeds 20.
- Plants, each at an even AND an odd offset: at least 2 P1 (each also yields a P2 at the same offset); at least 2 standalone P2; at least 2 P3 not in drawn order; at least 1 P3 in drawn-subsequence order; at least 1 P1 and 1 P3 using the PB-equals-main draw; one of each straddling a chunk boundary (chunk size set to about 1,000 digits in tests); one ending exactly at N; one starting at offset 0; one that would need digits beyond N (must NOT hit); near-misses (one field out of range, one duplicate main, PB in a middle slot); an odd-length fixture with a pad nibble. Oz fixtures mirror these once decisions 1-3 are made.
- Pass criterion: exact equality of the tuple set `(drawset_id, draw_number, category, start, matched_digits, flags)` between oracle and engine, and byte-identical output across two runs.

### 6.3 Mutation tests (each must fail at least one fixture)
Swapped nibble order; byte-aligned starts only; lookahead omitted; omission list missing one subset; distinctness applied across the PB field; PB range check applied to P2's seventh field; off-by-one offset.

### 6.4 Reconciliation (no new scans)
As in section 4, question 3. Pass = exact set equality after boundary normalisation, or every difference explained by a documented convention change.

### 6.5 Golden real-data test
Read the first 10^8 digits of the published phi packed file (the first 50,000,000 bytes) with the new engine; the events must equal the three rehearsal events. Real digits, no generation, seconds to run.

### 6.6 Transition analysis design
- Compute only from the event table.
- Predeclared primary statistic: for the category pair (P3_any, P3_any) and adjacent draws (W, W+1) that both have at least one event, the minimum absolute offset difference; report the signed value too.
- Null: permute the draw labels (randomly reassign each draw's set of event offsets to a draw index) 10^4 times and recompute the statistic (e.g. median of the minima, or the count of pairs within a predeclared distance). This exactly preserves per-draw event counts and the position distribution and destroys only the W->W+1 adjacency, which is the hypothesis under test. No assumption about the constant's digits is required.
- Denominators: report the number of adjacent pairs that were evaluable and the number that were not (one or both draws empty).
- Decoys provide an independent second check: the same statistic computed on each decoy drawset.

---

## 7. Minimum viable architecture and staged implementation

### 7.1 Modules (one file each; plain Python + NumPy)
1. `bcd_reader.py` - yields `(first_owned_offset, digit_array)` per chunk; the digit array includes 15 digits of lookahead; hashes each underlying byte exactly once; at EOF, offsets whose window would extend past N are owned by no chunk.
2. `extract.py` - fields `F_0..F_7` for owned offsets; range masks per profile; compaction to candidates; distinctness; sorted keys packed to int64.
3. `index.py` - per key family: a sorted int64 key array plus attribution lists of `(drawset_id, draw_number)`. Families: `K7` (sorted 7 mains), `K7S` (sorted 7 mains + special), `K6S` (sorted 6 mains + special), `K6` (sorted 6 mains), `K7mix` (sorted 7 of {6 mains + 1 supplementary}; Oz any-slot). Built from all drawsets in the run.
4. `scan.py` - the one pass; writes `raw_events.csv` (`drawset_id, draw_number, family, start_offset, matched_digits`) and `run_manifest.json`.
5. `classify.py` - pure: adds category, selected/omitted mains, special value/role/stream slot/draw position, `drawn_order`, `drawn_subsequence_order`, `ascending_order` (if adopted), `reordered_only`, baseline flags.
6. `report.py` - counts and overlaps beside expectations, decoy comparison, transitions with permutation test, summary.
7. `profiles/powerball.json`, `profiles/ozlotto.json`; `adapters/` CSV readers with cutoff refusal, order-provenance test, era check.
8. `oracle/` - independent, string-based (6.1).

Family to category mapping. Powerball: `K7 -> P2_any`, `K7S -> P1_any`, `K6S -> P3_any`. Oz Lotto: `K7 -> O1_any`, `K7mix -> O2_any` (slot recorded; supp-last subset by flag), `K6 -> O3_any`.

### 7.2 Reuse
Lift the chunked reader, nibble decode and existing candidate prefilter from `wsl_scan_packed_powerball.py` if they pass 6.1-6.5. Replace only the P-specific index with the family index. Move transitions out of the scanner into `report.py`.

### 7.3 Stages, each a rollback point (nothing earlier is modified or deleted)
- **S1 Desk checks (hours):** ascending-row test on the Powerball CSV; CSV reconciliation 1e8 / 1e9 / 1e10. Output: a short findings note.
- **S2 Oracle, fixtures and mutation suite run against the EXISTING packed scanner.** Output: pass/fail list. Patch the old scanner only for a demonstrated defect, as a minimal isolated change.
- **S3 New engine (modules 1-4, Powerball profile only)** until it passes the S2 suite, the golden real-data test, and reproduces the old scanner's 1e8/1e9 events.
- **S4 `classify.py` and `report.py`:** baseline-filter equality test against old outputs; decoys; permutation test on the existing phi events.
- **S5 Oz Lotto:** decisions 1-5 settled, data acquired and split, adapter + profile + Oz fixtures.
- **S6 Production:** six constants x Powerball, then six x Oz Lotto. Each run writes to a new create-only directory keyed by `run_id`; the old unqualified phi run stays as an audit artefact.

### 7.4 Safety points
- The scanner opens packed files read-only and verifies the manifest SHA-256; refuses any drawset file whose SHA-256 is not in the run manifest; refuses draw numbers at or beyond the cutoff before parsing other fields (existing behaviour, keep).
- No path under the parent project's data directories is accepted as a drawset.
- Decoy drawsets are generated with a recorded seed, written only into the run directory, and carry draw numbers of 9,000,001 and above.
- Replacing a published binary (if ever): write new, verify, rename the old to a `.superseded_<date>` name, then publish; never delete first.
- The Kagari/taskset affinity issue is a performance matter with no bearing on scan semantics; keep it off this workstream.

### 7.5 Not worth doing
A rule DSL; the five-strategy library; combining games in one pass; Numba/Cython before profiling; pre-generated permutation strings; per-category output files; the packed-format registry rework before scanning (a manifest with SHA-256 is sufficient provenance); mandatory comparison against the retired 1e9 byte-per-digit binaries (waived; the CSV comparison suffices); any rich visual report before the event tables exist.

---

## 8. Questions for the owner, and missing materials

Blocking decisions:
1. O2 supplementary position (section 5, decision 1).
2. Oz Lotto era, source order provenance and holdout size (decisions 2-4).
3. Whether the low-CPU qualification work (S1, S2) may begin while pi and the remaining constants generate, or must wait for all six per the 8 Nov sequencing decision. My view: S1/S2 use negligible CPU and touch no production file, so they can run in parallel; revising the sequencing is the owner's call.
4. Whether to adopt the two optional additions that are new hypotheses: the `ascending_order` flag and the Powerball 12-digit six-mains-no-PB family. (Decoy drawsets are not a new hypothesis; I recommend them unconditionally.)

Materials not seen, needed for any code-level review: `wsl_scan_packed_powerball.py`, `wsl_format.py`, `outlandish_powerball_stage_a.py` (the exact versions used for the 1e9 and 1e10 runs, with SHA-256), the three result CSV sets, the drawset CSV's SHA-256, and the deferred order-matching record.

---

## Appendix A - Expected draw-attributed event counts under the uniform-digit null, N = 10^10

Formula: `E = D x S x (N - L + 1) / 10^L`. Poisson standard deviation ~ sqrt(E).

**Powerball, D = 433**

| Class | S per draw | L | Expected per constant | Across six constants |
|---|---:|---:|---:|---:|
| P1 drawn order | 1 | 16 | 0.00043 | 0.0026 |
| P1 any order | 5,040 | 16 | 2.18 | 13.1 |
| P2 drawn order | 1 | 14 | 0.043 | 0.26 |
| P2 any order | 5,040 | 14 | 218 | 1,310 |
| P3 drawn-subsequence order | 7 | 14 | 0.30 | 1.8 |
| P3 any order (baseline) | 5,040 | 14 | 218 | 1,310 |
| (optional) six of seven mains, no PB, any order | 5,040 | 12 | 21,800 | 131,000 |

**Oz Lotto, D modern-era draws (D ~ 230 in brackets is illustrative only)**

| Class | S per draw | L | Expected per constant |
|---|---:|---:|---:|
| O1 drawn order | 1 | 14 | 0.0001 x D (0.02) |
| O1 any order | 5,040 | 14 | 0.50 x D (116) |
| O2 ten-ball relative order | 21 | 14 | 0.0021 x D (0.5) |
| O2 any order, supplementary last | 15,120 | 14 | 1.51 x D (348) |
| O2 any order, any slot | 105,840 | 14 | 10.6 x D (2,430) |
| O3 drawn-subsequence order | 7 | 12 | 0.07 x D (16) |
| O3 any order | 5,040 | 12 | 50.4 x D (11,600) |

Reading: the provisional phi result of 227 P3 against 218 expected is unremarkable (sd ~ 15). Any narrow-order hit must be reported on the same line as its project-wide expectation.

---

## Appendix B - The one pass, in brief

```text
for each chunk (digit array d with 15-digit lookahead; owned offsets k):
    F_j[k] = 10*d[k+2j] + d[k+2j+1]            for j in 0..7   (strided slices)
    mask6  = all F_0..F_5 in main range           -> compact -> distinct -> sort -> key6
    mask7  = mask6 and F_6 in main range          -> compact -> distinct -> sort -> key7
    maskS6 = mask6 and F_6 in special range       -> key6 + F_6         (K6S)
    maskS7 = mask7 and F_7 in special range       -> key7 + F_7         (K7S)
    (Oz)  mask7mix = all F_0..F_6 in 1..47        -> sort -> key7mix     (K7mix)
    for each family: idx = searchsorted(family_keys, keys); on hit, emit
        (drawset_id, draw_number, family, k, digits d[k : k+L]) for every attribution
    hash the chunk's own bytes (never the lookahead bytes)
post-pass (classify.py, seconds): flags from (matched digits, draw record)
post-pass (report.py):            counts beside expectations, decoys, transitions
```

**End of review response.**
