# OUTLANDISH_01 — Shared Matching, Classification and Reporting Specification

**Version:** v0.2 — post-review consolidated specification for **owner ratification**  
**Prepared:** 9 November 2026 (Australia/Adelaide)  
**Author:** ChatGPT, consolidating owner decisions, two Claude/ChatGPT architecture exchanges and Claude's single final review  
**Review disposition:** Claude `OUTLANDISH_01_Claude_Single_Review_of_Consolidated_Spec_v0_1.md`: **PASS WITH SPECIFIC CORRECTIONS**; C1–C20 reconciled in this revision; no unresolved design blocker identified.  
**Status:** **PROPOSED FOR OWNER RATIFICATION — NOT YET RATIFIED; NO CODING, SCANNING OR DATA MODIFICATION AUTHORISED**  
**Review policy:** The planned single Claude review is complete. No additional review round is requested or required on the issues identified. A further focused review would be considered only if later evidence reveals a genuine consequential flaw; that would be raised explicitly with the owner.

---

## 0. Read this first: objective, authority and review boundaries

OUTLANDISH_01 is a local, owner-operated Windows 11 / Debian WSL2 numerical research project associated with, but operationally distinct from, `hydra3333/analysing_perceived_randomness_in_reality`. Six long decimal expansions of mathematical constants are being produced, verified and stored as compact packed binary files. The next research phase will search their decimal digits for sequences corresponding to historical Australian **Powerball** and **Oz Lotto** draws, then examine counts and *positions* of matches, including relationships between consecutive historical draws. The owner welcomes exploratory and unconventional hypotheses but requires technically correct matches and appropriately qualified statistical interpretation. Nothing in OUTLANDISH_01 changes the parent project's forecasting, holdout or evaluation rules.

**Four non-negotiable boundaries:**

1. **Finish six verified production binaries first.** Do not implement or run scanner qualification, reconcile scientific results or launch new scientific production scans until the sixth constant has been verified and published. Design review can occur now.
2. **Preserve the agreed experimental categories.** Powerball P1/P2/P3 and Oz Lotto O1/O2/O3 plus their explicitly approved order refinements; no ascending-numeric-order class, no six-Powerball-mains-without-PB/P4, and no additional categories by default.
3. **Never contaminate real results with artificial data.** Synthetic fixtures, synthetic *decoy drawsets* and optional synthetic-digit null experiments must remain out of REAL draw histories, REAL event files, REAL reports and the parent project's prediction paths. Use simple structural separation with tests, not an elaborate operator approval system.
4. **Keep administration proportionate.** This is operated by one owner. Existing verified packed files and receipts, known drawsets and ordinary run metadata are enough. **No new registry, owner approval workflow, cryptographic ceremony, complex rule language, or extra authorisation/allowlist layer.** Scientific correctness and reproducibility matter; unnecessary process does not.

### Evidence and document status

- **OWNER-DECIDED:** explicitly recorded user choices in the two previous reconciliation exchanges and recent conversation. These are fixed for this review.
- **ESTABLISHED/REPORTED:** production outcomes and historical scanner behaviour from owner-supplied logs, uploaded source snapshots and previous review documents. The current live scanner revision must still be inspected in the qualification phase.
- **PROPOSED SPEC:** the technical design below, for Claude's **single independent review** and subsequent owner ratification. Agreement between reviewers is not implementation permission.
- Historical draw-source credibility and original operator-drawn-order verification **have already been completed by the owner/project**. **Do not reopen them.** Testing that *new software preserves* the existing stored column order and roles is appropriate.

### Sources to consult if available

1. `OUTLANDISH_01_Common_Matching_Engine_Claude_Review_v0_1.md` — original long context and design.
2. `OUTLANDISH_01_Common_Matching_Engine_Claude_Review_Response_v0_1.md` — Claude's first review.
3. `OUTLANDISH_01_ChatGPT_to_Claude_Focused_Reconciliation_v0_2.md` — owner decisions and negotiation.
4. `OUTLANDISH_01_Claude_to_ChatGPT_Focused_Reconciliation_Response_v0_1.md` — Claude's second review, the primary source for this consolidation.
5. `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md` — deferred historical proposal (not an authority to reopen owner choices).
6. Current `wsl_scan_packed_powerball.py`, `wsl_format.py`, legacy `outlandish_powerball_stage_a.py`, preholdout draw CSV and saved scan results, **when the post-six qualification stage starts**.

The reviewing Claude conversation has **not** directly inspected the current source code, result CSVs or drawset; it acknowledged that limitation. Its single-review corrections were accepted following a source-based plausibility check; qualification remains a post-six task. ChatGPT's inspection of supplied snapshots found the original PB-equals-main, all-seven-P3-omissions, and P2-main-above-20 behaviours apparently correct; treat these as **regression traps to prove**, not as confirmed existing defects. Cite specific code evidence if a later live-source inspection changes that conclusion.

---

# PART A — Established game, data and research requirements

## A1. Official draws and winning divisions versus our experimental pattern categories

The official winning-division selection rules are *context*. Our P and O categories define **digit-string matches**, not purchases or ticket prize allocations. One digit offset may legitimately yield more than one experimental category; official ticket divisions do not imply our experimental categories must be mutually exclusive.

**Official Lotterywest-GOV references (context, not draw-data source changes):**  
Powerball `https://www.lotterywest.wa.gov.au/games/powerball`  
Oz Lotto `https://www.lotterywest.wa.gov.au/games/oz-lotto`  
Oz Lotto 2022 rule change `https://www.lotterywest.wa.gov.au/lotterywest/media-centre/bigger-prizes-and-more-winners-with-oz-lotto-game-change`.

### A1.1 Powerball

- **Draw mechanics:** seven distinct main numbers from **1–35** in their actual operator-drawn order; one Powerball from a **separate 1–20** barrel.
- **Critical role rule:** the Powerball may have the same numeric value as one of the seven main numbers. Main-ball uniqueness must **not** extend to the Powerball field.
- **Top three official division *selections*:** Div 1 = 7 mains + PB; Div 2 = 7 mains; Div 3 = 6 mains + PB. Remaining official divisions, although not searched, are Div 4 = 6 mains; Div 5 = 5 mains + PB; Div 6 = 4 mains + PB; Div 7 = 5 mains; Div 8 = 3 mains + PB; Div 9 = 2 mains + PB.
- Official wins are not dependent on chronological drawn order. The project additionally tests drawn-order sequences as an explicit *experimental* constraint.
- The modern research drawset is the pre-existing isolated **433 historical draws**, `1144..1576` inclusive, exclusive cutoff `1577`; stored as `POWERBALL_preholdout_only.csv`, with `Draw_Number,Date,Drawn_1,...,Drawn_7,Powerball` in the approved order. **Never read a broader/master future-outcome source as a substitute.**

### A1.2 Oz Lotto

- **Modern draw mechanics only:** seven distinct main numbers and three distinct supplementary numbers from the **same 1–47 barrel**, ten distinct values total. The first seven drawn are mains, the last three supplementary, and their operator order/role is already verified by the project.
- **Top three official division *selections*:** Div 1 = 7 mains; Div 2 = 6 mains + 1 supplementary; Div 3 = 6 mains. Remaining official divisions are Div 4 = 5 mains + 1 supplementary; Div 5 = 5 mains; Div 6 = 4 mains; Div 7 = 3 mains + 1 supplementary.
- **Era restriction decided by owner:** use **only historical draws from the actual first draw using today's 7-main + 3-supplementary, 1–47 configuration**. The game changed in May 2022; use the project-established effective draw boundary, not a guessed draw number or retroactive interpretation of older formats. Older historical eras are excluded from this research scope.
- Oz uses its **own validated isolated drawset and its own holdout**, per applicable parent-project policy, not Powerball's draw-number cutoff. A new software adapter must preserve existing main/supplementary role and actual column order without re-sorting; **this is an adapter-fidelity test, not a repeat of draw-source verification**.

## A2. Decimal constants and packed format

**Six intended production constants, 10,000,000,000 decimal digits each including integer digit:**

| ID | Constant | Production state known when drafting |
|---|---|---|
| `phi` | Golden ratio | **DONE:** generated/verified, 5 GB binary independently whole-file hash-checked via the old scan's digest comparison, published, decimal intermediate deleted |
| `e` | Euler's number | **DONE:** generated/verified, 5 GB binary independently SHA-256 checked with `sha256sum`, published, decimal intermediate deleted |
| `pi` | π | **DONE:** verified generation, 5 GB binary independently SHA-256 checked with `sha256sum`, published, decimal intermediate deleted; publication and cleanup PASS reported |
| `log2` | Natural logarithm of 2 | Preflight PASS; production generation completion not reported |
| `gamma` | Euler–Mascheroni constant | Not reported generated |
| `lemniscate` | Agreed y-cruncher lemniscate selection | Not reported generated; use verified generator/receipt identity rather than assuming a name/prefix |

The source decimal file contains **10,000,000,001 bytes**: 10 billion ASCII decimal digits plus the decimal point. Packed final files are **5,000,000,000 bytes** without header or decimal point, using `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1` — two decimal digits per byte, first digit high nibble and second low nibble. The **integer digit is logical zero-based digit offset 0**, and every offset (including odd offsets) is a potential match start. For fixture streams with an odd number of digits, the final unused low nibble is padding, not a real digit. The real N is obtained from the verified format metadata/receipt, not assumed to equal twice the byte count for every fixture.

Existing final directory (no replacement directory):

`G:\OUTLANDISH_01\large_artifacts\digits\`

Each final `.packed.bin` has a same-name `.wsl-receipt.json`; the conversion stage uses `...\large_artifacts\staging\`, then the verified binary and receipt are published on G:. No scanner may modify these files. All run evidence is separate. Verified generation uses y-cruncher `-verify:1`; a temporary decimal intermediate is deleted **only after** packed publication and whole-file SHA verification, retaining the small y-cruncher validation report and log.

**Published known hashes:**

| Constant | Filename | Packed SHA-256 |
|---|---|---|
| φ | `digits_golden_ratio_10_to_10.packed.bin` | `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d` |
| e | `digits_e_10_to_10.packed.bin` | `522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f` |
| π | `digits_pi_10_to_10.packed.bin` | `62ab5b9a511eb0fcf5d09717df9ee51f8bd29ea09acf379e6f1045c537ababe2` |

There is no requirement for a newly implemented packed registry before scientific scanning. The receipts already exist. Don't modify the legacy byte-format registry to misrepresent these as byte-per-digit data. The unresolved Kagari/taskset CPU-affinity issue belongs to generation/performance, not this scanner design.

## A3. Established experimental matching rules (FIXED2)

Each ball value is represented by exactly **two decimal digits**, e.g., ball 7 = `07`, and the candidate can start at **any logical decimal-digit offset** of the constant. 'Any-order' means **any permutation of the eligible distinct selected main values**; a sorted canonical key is only a lookup technique. “Drawn order” is the recorded operator chronological order, not ascending numerical order.

### A3.1 Powerball P1/P2/P3 (preserve original baseline exactly)

| Category / family | Candidate length | Original baseline | New approved classifications |
|---|---:|---|---|
| **P1 / K7S** | 16 digits | Seven drawn mains **exactly in operator-drawn order**, followed by that draw's PB as eighth field | `P1_any_order` (seven mains any permutation, PB fixed last), `P1_drawn_order` (original P1), `P1_reordered_only` = any AND NOT drawn |
| **P2 / K7** | 14 digits | Seven drawn mains **exactly in operator-drawn order**, with no PB condition | `P2_any_order`, `P2_drawn_order` (original P2), `P2_reordered_only` |
| **P3 / K6S** | 14 digits | **Any six of the seven drawn mains in any order**, followed by that draw's PB | `P3_any_order` (**original P3**), `P3_drawn_subsequence_order` (delete one of original seven without reordering remaining six), `P3_reordered_only` |

Powerball role constraint: for K6S, fields 0..5 are **six unique mains 1–35**, and field 6 is PB **1–20**, which **may equal a main**. For K7S, fields 0..6 are seven unique mains and field 7 is PB, likewise allowed to equal a main. For P2, field 6 is a main **1–35**, not a PB restricted to 1–20.

### A3.2 Oz Lotto O1/O2/O3 (first proposed implementation)

| Category / family | Candidate length | Owner-approved views |
|---|---:|---|
| **O1 / K7** | 14 digits | All seven mains: `O1_any_order`; `O1_drawn_order` matches exact operator-drawn main sequence (the original O1 research intent); `O1_reordered_only` |
| **O2 / K7mix** | 14 digits | Any six of seven mains **and one of three supplementaries**, all seven fields unique 1–47. **Both** `O2_any_slot` and its subset `O2_supplementary_last` are required; **supplementary-last is the provisional primary headline**, any-slot secondary. Also `O2_drawn_subsequence_order` and suitable `reordered_only` are derived views. |
| **O3 / K6** | 12 digits | Any six of seven mains: `O3_any_order`, `O3_drawn_subsequence_order`, `O3_reordered_only` |

For O2, the engine must identify **which selected ball is supplementary and its 0-based slot**, using the corresponding actual draw's disjoint main/supplementary sets. A selected six-main/one-supplementary O2 hit in **full relative order of the ten-ball chronological draw** necessarily has the supplementary **last**, and is therefore nested:  
`O2_drawn_subsequence_order ⊆ O2_supplementary_last ⊆ O2_any_slot`.

For O2 `reordered_only`, **state the particular parent class**. Recommended initial labels: `O2_supplementary_last_reordered_only = O2_supplementary_last AND NOT O2_drawn_subsequence_order`, and, if reported, `O2_any_slot_non_drawn = O2_any_slot AND NOT O2_drawn_subsequence_order`. The latter includes both reordered supplementary-last hits and hits where the supplementary appears earlier; don't call it just `reordered_only` without that explanation. No new research rule regarding which of the three supplementary balls was drawn 8th/9th/10th; preserve chosen-ball provenance as metadata only.

### A3.3 Allowed overlaps, shifted windows and classification nesting

- **Same-start deterministic inclusions:** every Powerball `P1_any@k` yields `P2_any@k` for that draw (the first seven fields). Every Oz `O2_supplementary_last@k` yields `O3_any@k` for that draw (its first six fields). The narrower drawn-order class implies its corresponding narrower same-start class where applicable.
- **Shifted deterministic inclusions:** `P1_any@k` also yields `P3_any@(k+2)` for that draw: the six mains in fields 1–6 followed by the PB. `P1_drawn@k` consequently yields `P3_drawn_subsequence@(k+2)`. Oz `O1_any@k` yields `O3_any@k` **and** `O3_any@(k+2)`; `O1_drawn@k` implies the corresponding two O3 drawn-subsequence events. Oz `O2_any_slot@k` with its supplementary in the **first** field yields `O3_any@(k+2)`; O2 supplementary-last yields O3 at `k`.
- **PB/main value equality:** the PB is from a separate barrel and is allowed to equal a main. If an eligible `P2_any@k` ends with a main whose number equals that draw's PB, those same seven fields also form `P3_any@k` (first six mains + PB), provided they match that draw; the two family events are legitimate. If `P1_any@k` has PB equal to the main in field 0, the seven fields at `k+2` also yield `P2_any@(k+2)`. These are structural relationships, not duplicate-emission defects.
- **Order nesting:** a narrow-order event is included in its any-order parent; `reordered_only` is a *disjoint subset difference*, not another match event. Oz O2 `drawn_subsequence ⊆ supplementary_last ⊆ any_slot`. The same offset can legitimately belong to different categories or draw attributions.
- **Physical overlap reporting:** do **not** hard-code the above cases as the complete list. For **the same draw**, derive each event's half-open logical digit interval `[start, start + family_length)` and detect **actual interval intersections**, whether at the same start or shifted. Report event counts unchanged; include concise pairwise same-draw overlap summaries and, if grouping is used, clearly distinguish connected components from pairwise direct overlap. An efficient ordered sweep suffices; avoid quadratic all-pairs comparison over large event tables.
- **Units:** draw-attributed **events**, distinct starting **offsets**, distinct historical **draws**, and overlapping physical **intervals** answer different questions. Never sum nested categories as if independent and never suppress valid overlapping events. Overlap changes dependence/interpretation, **not** each category's analytical expected event count.

## A4. Existing evidence and unresolved scientific accuracy question

The legacy byte-per-digit Powerball scanner and the current packed-scanner snapshot produce match CSVs, adjacent-draw transition reports and summary information. The packed scanner's historical W→W+1 transition deltas are predominantly **anchored on P1**, so an all-zero P1 result leaves those comparisons uninformative; the agreed design must support P3→P3 (and Oz O3→O3) from the raw event table.

Known **unqualified/scientifically unresolved** Powerball observations:

| Data | Original categories P1/P2/P3 | Evidence status |
|---|---|---|
| 100-million-digit packed φ rehearsal | `0 / 0 / 3` | Three P3 starts: `20,048,101`; `71,806,090`; `95,105,831` |
| 1-billion-digit legacy numeric-byte φ | `0 / 0 / 25` | Historical baseline report, not yet row-reconciled against packed φ prefix |
| 1-billion-digit legacy numeric-byte π | `0 / 0 / 29` | Historical baseline report; not the current production π |
| 10-billion-digit packed φ | `0 / 0 / 227` | Full-file digest agreed with conversion receipt; **match logic not yet qualified** |

Owner saw suspicious differences in early progress counts between the long packed φ scan and earlier short-file results. **Do not assume a bug or dismiss the observation**. After the six constants are published, first compare the **saved CSVs**, with exact draw identities, matched strings, zero-based starts and the **derived** end offset `start + pattern_length <= prefix_N`. Compare P3 first and then all available baseline categories; inspect any discrepancy to a specific offset. Check old offset conventions ±1 only if evidence warrants; no automatic shift in production data. Check duplicate `(draw, category, offset)` records. Do not rerun 5 GB scans solely to diagnose a discrepancy resolvable from saved event rows.

---

# PART B — Consolidated technical specification candidate

## B1. Recommended minimalist architecture

**One shared matcher implementation. One game per REAL scan. Five small canonical key families, not five independent strategy classes and not a rule DSL.** Ordered vs unordered is classified after finding candidate *sets*, not encoded in the scanner's main lookup. Reporting is a separate phase that consumes event files rather than rereading the 5 GB constant.

Conceptual modules (names illustrative, not mandatory):

1. **BCD reader/extractor** — read-only stream, high-nibble-first decode, exact offset ownership, variable chunk size, optional final pad, streaming SHA-256 of underlying bytes.
2. **Game adapter/profile** — already-approved isolated historical data, main/special roles and ranges, era/cutoff, enabled key families and selection semantics. Keep as simple code/config, not executable rule expressions.
3. **Canonical family index and scanner** — for each family, an independent mapping from a compact sorted key to all eligible `(draw, draw-subset/selected-special)` attributions; candidate role checks and lookups; emit raw occurrences.
4. **Classifier** — pure, replayable event+draw-record calculation of exact/relative drawn order, omitted mains, selected supplementary, supplementary stream slot and nested class membership.
5. **Reporter** — counts, overlaps, expectations, carefully qualified null comparisons and W→W+1 spatial relationships derived exclusively from the qualified event dataset.
6. **Small independent reference oracle and fixtures** — different algorithm from production, written and reviewed independently, only for qualification.

One REAL scan is per `(constant, game, specific drawset/profile version)` and includes all approved families of that game. Do not combine Powerball and Oz Lotto in one pass, pool their histories, or re-scan the constants simply because report thresholds or class displays change.

## B2. Key families and candidate processing — correctness invariants

| Family | Game(s) | Candidate fields/roles | Length (logical digits) | Distinctness and key |
|---|---|---|---:|---|
| `K7` | Both | 7 mains | 14 | All 7 main fields distinct; sorted 7-main key; game-specific main range |
| `K7S` | PB | 7 mains + trailing PB | 16 | Seven main fields distinct; PB validated separately; sorted mains plus trailing PB in key |
| `K6S` | PB | 6 mains + trailing PB | 14 | Six main fields distinct; PB validated separately; sorted mains plus trailing PB in key |
| `K6` | Oz | 6 mains | 12 | Six distinct main fields; sorted key |
| `K7mix` | Oz | 6 mains + 1 supplementary at **any slot** | 14 | Seven distinct values from common 1–47 range; sorted seven-value key; matched draw identifies which is supplementary and its slot |

**Critical implementation invariants:**

- **Separate index by family** (or family-discriminated keys). A `K6S` key may numerically equal a `K7` key; mixing them would misattribute matches. Store all matching draw identities; never overwrite an attribution just because a second draw has the same canonical key.
- **Family-specific role checks.** A shared range mask may be reused as an intermediate, but never one common “all seven balls must be distinct 1–35 and seventh must be ≤20” predicate. In PB K6S the final field is PB and can repeat a main; in PB K7 it is a distinct main and can be 21–35; in Oz K7mix the selected special is identified **against a draw** after canonical lookup, not from a fixed field slot.
- **Family-specific EOF eligibility.** At zero-based start `k`, family F is eligible **iff `k + L_F <= N`**, where `N` is the number of real digits. The largest 16-digit family's needed lookahead must never exclude a valid final 12- or 14-digit hit. Never let the last pad nibble become a digit. Explicit per-family length masks; do not use sentinel padding as a substitute for end checks.
- **All logical starts.** Examine even and odd digit offsets. Exactly one chunk owns each start, including positions near chunk borders. Lookahead supplies data but must not create a second ownership of the same starting offset. Hash **each physical input byte once** independent of lookahead. Chunks start at whole-byte boundaries (thus even digit offsets); odd logical starts remain eligible. In odd-digit fixtures, require the final low pad nibble to be zero and never treat it as a digit.
- **Arithmetic.** Form 2-digit fields in `int16` or wider (not unchecked `uint8` arithmetic with potential sentinels); e.g. `F0[k] = 10*d[k] + d[k+1]` and `Fj[k] = F0[k+2*j]`. Shared field arrays, masks and candidate compaction are allowed optimisations only after they agree with the reference oracle. Sort/pack **only valid candidates**, not 10 billion rows of arbitrary numbers.
- **Compact keys.** Sorted FIXED2 values encoded as base-100/integer within signed int64 are acceptable for these lengths. Preserve the family identity and the original matched-digit text. Avoid generating literal factorial permutations for the index.
- **No false invariants.** Numerical equality of PB and a main is legal; Oz ten values all come from one barrel and cannot repeat within a draw. K7 (Oz O1) and K7mix (Oz O2) may share a precomputed candidate sorted key but have distinct indexes/attributions.
- **Input validation.** Reject corrupt nibble values, invalid receipt/declared size, missing or inconsistent actual draw fields, invalid duplicate main selections, out-of-range roles and contradictory data lengths. Do not silently skip a class or corrupt chunk; fail with a clear reason.

## B3. Minimal event dataset and classification contract

**REAL raw event CSV (four columns):**

```csv
draw_number,family,start_digit_offset,matched_digits
1274,K6S,71806090,32072715310907
```

*The row is illustrative only; it does not assert the example string is the observed scan result.*

- `draw_number` is an integer present in the approved isolated drawset. `family` is one of the enabled game families. `start_digit_offset` is an integer ≥0. **`matched_digits` is text, never a numerical quantity**: the exact FIXED2 string from that offset, containing only ASCII `0`–`9` with exact length equal to the family window (12/14/16). Explicitly force text/string dtype when loading; do not open-and-resave via Excel or a spreadsheet importer, which may strip leading zeroes. Event-file SHA-256 in the manifest detects modifications. **No arbitrary new per-row game ID, explicit end offset or duplicate count column:** game, constant ID, drawset reference and immutable scan settings are stored once in a small sibling `run_manifest.json`; end offset is derived as `start + family_length`.
- Row identity inside its specific run is `(draw_number, family, start_digit_offset)`. Sort deterministically by `(start_digit_offset, family, draw_number)`. Output **one row per valid draw attribution**, not one per order flag, and do not deduplicate legitimate different draws/families sharing an offset. **After sorting, the REAL/NULL event writer checks adjacent rows for duplicate identities and fails the run if found** (catching repeated chunk emission rather than hiding it).
- Raw CSV plus manifest plus the known historical drawset must suffice to **re-run the classifier without opening the packed binary**. The classifier and reporter must recheck the historical drawset file's SHA-256 against the digest recorded in that run manifest; refuse a mismatch rather than silently reclassify against modified outcomes. Derived fields: category label, selected/omitted mains, matched PB or supplementary and its slot, `drawn_order` / `drawn_subsequence_order` (as applicable), `reordered_only`, baseline membership; flags can be `true`, `false` or `N/A` if genuinely inapplicable. If a classified CSV is stored, recomputation must exactly reproduce it.
- Run-level metadata should be short and useful: REAL or NULL run type, constant ID, packed filename/receipt digest, game ID/modern era, drawset identity and digest, scanner code/version, start/end time, number of logical digits scanned, checks completed, count totals and output file identities. Use the existing receipt and ordinary SHA-256 provenance, **not a newly operated approval/whitelist database**.
- The event CSV and report never become inputs to the parent forecasting project automatically. Any later transfer is a separate scientific design decision.

## B4. REAL versus NULL separation — simple but enforceable

There are **two scientific run types**, not two sets of actual historical draws:

- **REAL:** only a verified published packed constant and the existing validated *real* isolated drawset for that game. Output under `G:\OUTLANDISH_01\large_artifacts\results\` (or the established REAL results root). `run_manifest.json` says `REAL`; draw numbers are genuine integer IDs. Real reporting refuses NULL files. **Exact built-in checks:** (i) packed file is a regular file under the existing published `digits/` root; same-name `.wsl-receipt.json` is present (its retained converter `PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY` scope label is historical and does not require rewriting the receipt after publication); size agrees with receipt and `(N+1)//2` before scanning (for production N = 10^10, size = 5,000,000,000 bytes); streaming SHA-256 of *the entire packed file* matches receipt before completed status; (ii) REAL drawset path comes from the installed game profile, not a caller-supplied alternative; (iii) it contains exactly one row per integer draw number from `era_first_draw` through `cutoff_exclusive-1` with no extra, missing or duplicate rows; Powerball = `1144..1576` inclusive. Refuse cutoff violations before reading restricted outcome fields. This is automatic software validation using files we already have, **not** a new catalogue or manual signoff.
- **NULL:** independently generated **synthetic decoy drawsets**, or an explicitly separate optional synthetic-digit experiment. Output under a fixed separate directory such as `G:\OUTLANDISH_01\large_artifacts\results_null\`, with unmistakable `NULL` manifest/type and text identifiers (`DECOY-...`). Never write, append or publish NULL events as REAL results.

**Agreed engineering compromise:** separate REAL and NULL executions, **not** one interleaved mixed index. For efficiency, one NULL run may contain **K synthetic draw histories in the same NULL-only index/pass** for a given `(constant, game)`. No common real/synthetic attribution list. Real and Null outputs must never share a completed run directory. This is a concrete computational compromise, not an operator approval workflow.

**Minimum built-in safeguards, automated:**

1. REAL and NULL index objects are constructed from different inputs and cannot be merged after creation. REAL uses exactly the profile-defined genuine drawset and its complete, era-bounded integer draw-number sequence; NULL IDs must be typed/non-integer text. A caller cannot flip the output type merely by renaming a file or passing a results path.
2. The REAL classifier/reporter accepts a REAL manifest and its REAL event file only; rejects NULL manifests, text decoy IDs, modified events or a historical drawset whose SHA-256 differs from the manifest. A comparator reads only **summary counts** (not synthetic raw rows) across the two run types.
3. REAL and NULL write to separate fixed parent locations (`results/` versus `results_null/`); files are produced in a new run-specific incomplete directory and marked complete only after success, **including the complete-file input digest comparison**. No append to older completed REAL results. A failed scan is not reported as successful.
4. No fixture or decoy generator writes into the production `digits/`, REAL drawset directory or REAL results directory. Synthetic-digit files are confined to their own test/null location; tests never mutate the actual packed source file.
5. Test the refusals: NULL events fed to REAL loader, real/null output-root substitution, synthetic fixture submitted as a REAL input, altered receipt/manifest and intentional duplicate identities. Each should produce a conspicuous refusal, not a quietly mixed result. Run tests in separate scratch directories and **prove existing REAL results are untouched**; deliberately disable each important guard in mutation tests and ensure the corresponding test fails.

**No extra administrative machinery:** don't introduce a frozen catalogue of approved constant SHA digests, special registry, manual signer/approver, additional owner checklist or permission ceremony. Already existing production receipts, the known game-specific real drawset and isolated output directories suffice. This is a one-person project; favour code-level guardrails and tiny targeted tests. No software can mathematically guarantee absence of all bugs, but the separation must be straightforward to audit and fail closed on foreseeable misuse.

## B5. Statistical and comparison analyses

**All interpretations are exploratory.** A larger eligible permutation space inevitably produces many more apparent coincidences; reports must show denominators and model-based expected counts beside observed counts. Do not infer predictive power from a matching string or interesting proximity alone.

### B5.1 Analytical expectation

For one class with `S` eligible digit sequences per draw, pattern length `L`, `D` historical draws, and an `N`-digit string, under the **idealised i.i.d. uniform decimal-digit null**:

`E[draw-attributed events] = D × S × max(0, N − L + 1) / 10^L`.

This is an **expectation for events attributed to historical draws**, not necessarily for distinct starting positions. Expected values depend on each class's length and permutations. For example Powerball with D=433, N=10^10:

| Class | S/draw | Expected events per constant |
|---|---:|---:|
| P1 drawn order | 1 | 0.00043 |
| P1 any order | 5,040 | 2.18 |
| P2 drawn order | 1 | 0.0433 |
| P2 any order | 5,040 | 218.23 |
| P3 drawn subsequence | 7 | 0.3031 |
| P3 any order | 5,040 | 218.23 |

The observed unqualified φ P3=227 is numerically near 218 expected, **but is not proof that scanner logic is right**. A very rare P1 drawn-order event should not be waved away as “some narrow class”; equally, one P3 drawn-subsequence event is quite ordinary. Interpretation must account for the particular class, the number of constants and analyses inspected, and other attempts at the same phenomenon.

For Oz, use its *actual modern-era D* and its own categories, not the illustrative old figure: O1 any 5,040 14-digit sequences/draw; O2 any-slot 105,840 14-digit sequences/draw; O2 supplementary-last 15,120; O2 drawn subsequence 21; O3 any 5,040 12-digit sequences/draw; O3 drawn subsequence 7. **Deterministic physical overlaps do not change any individual class's event expectation** (which remains additive in counted, draw-attributed patterns), but they make counts across classes dependent and should be noted in statistical interpretation.

### B5.2 Conditional order analysis

Condition on the observed any-order event count `n` within a class. Under **exchangeability of orderings within eligible matched windows**, an approximate binomial order baseline is `Binomial(n, q)` with:

| Given any-order parent | Narrow subset | q |
|---|---|---:|
| P1/P2/O1 any-order | exact drawn order | 1/5,040 |
| P3/O3 any-order | relative drawn subsequence | 1/720 |
| O2 any-slot | supplementary last | 1/7 |
| O2 supplementary-last | relative drawn subsequence | 1/720 |
| O2 any-slot | relative drawn subsequence (optional equivalent view) | 1/5,040 |

Show the conditional expected `n×q` next to narrow observed count, and label the corresponding p-value *approximate/conditional*, especially if shared positions, shared keys, overlapping draws or dependence of nearby windows undermine independence. The test is **not** proof of prediction. Conditional tests across categories may themselves be dependent because some matches deterministically imply other same-draw shifted or same-start events; interpret class-specific results individually and avoid counting their tests as independent discoveries.

### B5.3 Decoy drawsets and other null comparisons

- Keep **decoy drawsets** as a complementary empirical check: independently generate valid random draw histories using that game's current mechanics (PB seven distinct mains in a random draw order plus independent PB 1–20; Oz ten distinct numbers 1–47 in a random draw order, first seven main, last three supplementary). Each decoy history has the **same D and draw positions/count as REAL**, but **synthetic text IDs and separate NULL outputs**. Preserve repeated keys when they arise naturally.
- One reproducible seed per game can define the same decoy histories for all six constants of that game. Each NULL run also stores the **generated decoy drawset bytes** within its own NULL run directory and records the generation seed and generator version; future reclassification must not depend on a PRNG/library behaving identically years later. Suggested bounded **defaults to benchmark**: **K=19** in development/qualification and **K=99** in final comparisons. They are implementation defaults, **not a requirement to generate vast datasets**; measure elapsed time, output size and adequacy of resolution, and adjust with reason. A K=99 empirical tail probability cannot resolve better than approximately 0.01 without further simulation.
- Compare REAL counts with the distribution of **NULL counts by decoy**, for the same game, constant and class. Do not join NULL raw event rows into REAL reports. Nulls offer comparisons conditional on the observed constant digits; they are **not assumption-free**, because decoy sampling embodies a model of draw mechanics.
- Retain the analytical expectation as a separate baseline; do **not** replace it with decoys. **Synthetic random-digit/null-world experiments remain optional** for distinct questions concerning properties of constant digits; not routine or mandatory, and never intermixed with REAL inputs.
- For an empirical decoy-count comparison, use the simple finite-sample inclusive tails: `p_upper = (1 + number of decoy counts >= REAL count) / (K + 1)` and `p_lower = (1 + number of decoy counts <= REAL count) / (K + 1)`. State K beside each probability; avoid treating this as a definitive significance test without checking its exchangeability assumptions. Treat scanned categories chosen after examining the observed data as exploratory; predeclare a primary test before using p-values for substantive claims.

### B5.4 Consecutive-draw positional analysis

- Compute from classified **REAL** events **without rereading packed files**. An adjacent pair consists of genuine consecutive draw numbers `W` and `W+1` within the **same** complete game drawset. Never mix games or real and null event rows. Zero-match draws are still part of the chronological series.
- For each adjacent pair where both draws have one or more eligible events in the chosen class, compute `min_{a in offsets(W), b in offsets(W+1)} abs(b-a)` and record the chosen signed gap `b-a`, positions and corresponding events. **Deterministic tie:** choose the pair minimising `(abs(b-a), b-a, a, b)`; this favours the negative gap if absolute distances tie, continuing legacy behaviour, then a stable identity tie. Count *all* adjacent pairs and explicitly partition into evaluable and non-evaluable. If a gap is zero because one physical substring was attributed to two adjacent draws, **retain and flag** it, never drop it.
- **Proposed predeclared primary statistic per game, subject to owner ratification:** Powerball `P3_any -> P3_any`; Oz Lotto `O3_any -> O3_any`. For each constant, take the **median** of the minimum absolute gaps across evaluable adjacent pairs. This tests conditional positional adjacency, not prediction.
- **Primary permutation null:** perform **10,000** permutations of the *whole per-draw offset sets* across **all D eligible draws, including empty sets**, while the chronological draw-number positions remain fixed. Recompute the statistic and the **number of evaluable adjacent pairs** separately in every permutation. No artificial coupling or exclusion of zero-match draws. If the observed or a permutation statistic is undefined because no pairs are evaluable, report that explicitly as `N/A` and do not fabricate a numerical test; a predefined treatment of such cases must be validated on tiny fixtures before running real reporting.
- **Two-sided p-value:** let `m_obs` be the observed median and `m_perm` the median of valid permuted median values. Let `b` be the number of valid permuted medians for which `abs(m_i - m_perm) >= abs(m_obs - m_perm)` (including equality). The Monte Carlo p-value is `(1+b)/(R_valid+1)`; use all R=10,000 when all permutations are valid, and display the valid count and any exclusions. Also show upper and lower tails descriptively. Clearly label this a **centered permutation-distance convention**, conditional on the observed per-draw event sets, not a prediction test.
- **Multiplicity across constants:** the same predeclared primary statistic is tested on six constants **per game**. Report raw p-values and the **Holm family-wise multiplicity adjustment across the six constants within each game**; do not pool Powerball and Oz Lotto outcomes or silently enlarge/shrink the correction family.
- Other category pairs, directional gaps, window-threshold tests and cross-constant comparisons remain explicitly **exploratory**, with the number of comparisons stated. The owner may decline the proposed primary statistic before any real qualified research runs; no change to match definitions follows.

## B6. Minimum reporting outputs and example

Keep outputs useful for scientific review without generating a dashboard or excessive files.

1. **`raw_events.csv`** — immutable, minimal four-column actual matching facts; only REAL history in REAL runs.
2. **`run_manifest.json`** — compact game/constant/drawset/file identity, digest and engine version/status, scope REAL/NULL, counts and references. Not a registry.
3. **`classified_events.csv`** (optional to materialise, otherwise reproducibly derived) — one row per raw event with explicit nested classification, selected/omitted numbers and special slot/provenance.
4. **`category_summary.csv` and concise `summary.md`/JSON** — observed events, distinct offsets, distinct draws, relevant numerator/denominator, expectation and conditional-order result. Label any-order/narrow/reordered views and category overlaps; do not sum nested rows.
5. **`transitions.csv`** — per adjacent draw pair, eligible counts and minimum distance details, with a small overall summary and optional permutation/decoy aggregates from distinct NULL analysis.

Illustrative **fictional** Powerball report (D=433, N=10^10; these observed counts are NOT measured):

| Class | Observed draw-attributed events (fictional) | Analytical expectation |
|---|---:|---:|
| P1 drawn order | 0 | 0.00043 |
| P1 any order (contains P1 drawn) | 3 | 2.18 |
| P1 reordered-only | 3 | 2.18 minus drawn-order expectation |
| P2 drawn order | 0 | 0.0433 |
| P2 any order (contains P1 any at same draw/offset) | 215 | 218.23 |
| P3 drawn subsequence | 0 | 0.303 |
| P3 any order (contains P3 drawn subsequence) | 225 | 218.23 |

Reports shall also display **exact nesting and shifted same-draw inclusions**: `P1_any@k => P2_any@k AND P3_any@(k+2)`; `O1_any@k => O3_any@k AND O3_any@(k+2)`; `O2_supp_last@k => O3_any@k`; `O2_supp_slot0@k => O3_any@(k+2)`; plus the PB-equals-main coincidences in A3.3. Order-narrow ⊆ any, and `O2_drawn_subseq ⊆ O2_supp_last ⊆ O2_any_slot`. **The reporter finds all same-draw overlaps from actual interval intersections, not only from these named examples.** Distinct offsets, intervals and event counts remain separate, and optional pairwise summaries must not be confused with additive totals. Avoid turning summary rows into an exhaustive taxonomy.

**IMPORTANT:** An analytical expectation is for total draw-attributed events. Distinct offsets and distinct draws need different denominators and must not reuse that expectation unqualified. A report must make clear whether a class is unavailable (e.g., data missing) rather than silently treating it as zero. Given established owner-verified drawn-order datasets, it is anticipated that drawn-order classes are available for both games; adapters must not reorder them.

## B7. Correctness qualification and implementation order — only after all six published

### Q1. Desk reconciliation using saved evidence (no new full scan)

- Preserve the 100m rehearsal, 1e9 legacy and 1e10 unqualified φ results/CSV, drawset CSV, receipts, existing scanner versions and logs **without deleting or overwriting them**.
- Compare the 227-row φ P3 CSV filtered by **derived end ≤100,000,000** with the three known 100m events, and filtered by **end ≤1,000,000,000** with the 25 legacy 1e9 events. Compare exact `(draw, baseline-category, start, matched_digits)` sets. Check duplicates and normalise *only documented* format/offset differences. If disagreement, inspect individual digit bytes/windows with an independent tiny reader; don't interpret progress counts as definitive.
- Verify the observed installed Powerball CSV fields are passed through in operator-drawn order by the parser; **do not reopen historical source veracity**.

### Q2. Independent oracle and planted artificial fixtures against the EXISTING scanner

- Create a small **plain-Python decimal-string oracle** with straightforward offset iteration, FIXED2 parsing and literal rule comparisons, sharing **no decoder, match index or classifier functions** with production code. No need to process huge files or optimise the oracle.
- Use short all-`9` background strings, with independent trivial BCD packing. **Fixture draws use small integer IDs below the first real draw (provisionally 1–999; check the Oz modern era lower bound at integration)**: the old scanner rejects draw IDs at or above Powerball's cutoff, while the new REAL adapter refuses these out-of-era fixture IDs. Decoys instead use unmistakably **text** IDs. Construct **at least two deliberately planted hits per original P1, P2, P3**, and, once Oz is in scope, per O1, O2, O3. Include both nibble phases, offset 0, many offsets and chunk boundaries, final-valid start at exact EOF and invalid beyond EOF for **each family**; odd digit count with pad nibble; 6/7-omission variants; PB equal to main, PB less than all mains; seventh P2 main >20; `K7`/`K6S` key collision; candidate distinctness failures; special in wrong role/slot; multiple draws with shared key; overlapping P1/P2 and O2/O3; duplicate chunk emissions; abbreviated/truncated inputs.
- Verify **exact event tuple set and order flags**, not just total counts. Include fixtures for P1 shifted P3@k+2, Oz O1 shifted O3@k/k+2, Oz O2 special-slot-0 shifted O3@k+2, PB-equals-main cross-family `K7`/`K6S` same-start, leading-zero `matched_digits` roundtrip, duplicate writer identities, and direct interval-overlap counting. Add deliberate mutations of nibble order, odd start rejection, omitted lookahead, PB-inclusive distinctness, seventh-main PB-range confusion, incorrect family discrimination, shortened window exclusion near EOF and off-by-one offsets; each mutation must fail an appropriate fixture.
- Run these against the **existing** packed scanner first, with its output directed explicitly to a **temporary test result root outside production REAL `results/`**. Verify the production results directory listing/state is unchanged before and after each such run; if the old scanner cannot redirect its output, run an unchanged copy in a scratch tree. If its chunk size cannot be configured, construct a temporary fixture sufficiently long to straddle a genuine chunk boundary; do **not** modify the old reference scanner just to make the test easy. Any discrepancy becomes a specific, reproducible finding; don't refactor before identifying whether old behaviour is wrong or the definition needs clarification.

### Q3. Implement the minimal shared matching engine, then prove equivalence

- Implement the common packed reader and canonical family indexes with independent per-family eligibility; classify outside scanner. First support Powerball and prove the original **P1/P2/P3 baseline tuple sets** agree with the oracle, and with old outputs wherever the old outputs are qualified.
- Test prefix real-data equivalence against the three known φ rehearsal events (read just the necessary prefix); do not automatically equate event-set equality with statistical validity. Add Oz profile/adapter and fixtures after confirming the already-settled modern drawset/holdout file details at integration.
- Ensure reported per-family EOF behaviour, exact digit offset and round-trip matched digits are correct. Preserve the existing scanner as a reference/archive until equivalence is proven; no wholesale rewrite purely for architectural neatness.

### Q4. REAL/NULL separation and scientific reporting tests

- Implement real and null scan entry points/results roots with simple code-enforced separation; synthetic-decoy NULL runs may share one NULL index containing K decoys but never a REAL index. The **published-root/receipt/whole-file-SHA** and **profile-drawset exact-era-range** checks are part of the engine at this stage, not postponed to release. Ensure the real classifier and reporter refuse drawset SHA mismatch. Test attempted cross-type inputs, reporter refusals and fixed-path isolation; inject mutations to make sure the tests fail when a guard is removed.
- Build a tiny hand-computed fixture covering overlapping and shifted same-draw categories, zero-match draws, repeated offsets, W→W+1 ties, multi-hit pairs, signed deltas, permutation of **all** draws including empties, and expected counts. Test 10,000-draw-label-permutation p-value conventions, Holm adjustment, and an all-empty fixture that must produce `N/A`, not a manufactured p-value. Assert reporter and classifier equality without accessing the large constant.
- Run bounded performance checks and choose realistic chunk size and K, but don't optimise or extend scope before correctness. Implement and test independent full-file SHA verification/read-once behaviour; avoid accidental digest double-counting on lookahead.

### Q5. Qualified production scientific runs and release

- Only after Q1–Q4 PASS and owner ratifies the final implementation specification, perform **new create-only qualified REAL scans** of all six published constants for Powerball, then Oz Lotto independently when its already-approved modern isolated drawset/holdout is available. Optional separate NULL runs and reports follow, clearly labelled and contained.
- Keep the original 10^10 φ unqualified run as evidence, not as a replacement for qualified outputs. Each run has a distinct completed/failed state and cannot overwrite earlier evidence.
- No automatic transfer to the parent project; any new method/hypothesis requires that project's separately reviewed process and holdout rules.

## B8. Explicit exclusions, performance and change control

- **No new scientific categories** beyond approved P1/P2/P3/O1/O2/O3 and order refinements. No numeric-ascending classification and no six-main-no-PB family.
- **No extra data-source credibility audit** or manual signoff process. Preserve verified historical order and roles in new adapters. If a field needed by the rule is actually missing from a supplied integration file, report the precise incompatibility.
- **No new production registry**, frozen user-maintained SHA allowlist, two-person verification, signed evidence ledger or elaborate release workflow. The scanner uses existing receipts/known files and simple manifests; tests exercise foreseeable contamination hazards.
- **No refactor before oracle qualification**. No automatic rewrites of the six completed binaries. No generation-CPU affinity project under the scanner umbrella.
- **No compulsory synthetic-digit full-scale campaigns**, no per-category physical rescans for new reports, no combinatorial enumeration of all 5,040 sequences per draw, no arbitrary generic rule DSL and no new expensive framework without profiling.
- **No claim of prediction** based on observed matches. Record unexplained anomalies and statistically surprising results for proper subsequent analysis, neither suppressing them nor labelling them proof.

---


# PART C — Independent review outcome and proposed owner ratification

## C1. What happened in the one authorised review

Claude's `OUTLANDISH_01_Claude_Single_Review_of_Consolidated_Spec_v0_1.md` returned **PASS WITH SPECIFIC CORRECTIONS; no blocker**. The reviewed design was v0.1; this v0.2 folds those corrections into the normative sections. Claude's review is not a code-level audit of the live repository, which remains scheduled after the six constants.

**MUST corrections incorporated:** C1–C3 (shifted and PB-equality overlaps, physical interval-based reporting); C5 (exact textual `matched_digits`); C7–C8 (existing packed receipt verification and fixed complete REAL drawset range); C9 (fixture IDs); C10 (drawset digest on classification/reporting); C11 (legacy scanner tests outside REAL results); C14–C15 (specified permutation and Holm across six constants). All are embedded above, not deferred to an appendix.

**SHOULD/OPT disposition (ChatGPT):**

| Review item | Decision | Reason |
|---|---|---|
| C4 overlap does not alter E | **ACCEPT** | Prevents incorrect statistical adjustment for deterministic overlap. |
| C6 reject duplicate event identities | **ACCEPT** | Tiny, automatic integrity check that catches double-emission without adding owner work. |
| C12 preserve old scanner; adapt fixture size | **ACCEPT** | Maintains an unchanged regression reference. |
| C13 signed-gap tie convention | **ACCEPT** | Continuity with legacy reports and deterministic testability. |
| C16 adjacency/zero-gap edge rules | **ACCEPT** | Avoids silently excluding real correlations or missing draws. |
| C17 store generated decoy drawset | **ACCEPT** | Reproducible synthetic results without relying on a future PRNG implementation. |
| C18 empirical count-tail convention | **ACCEPT** | Removes avoidable reporting ambiguity. |
| C19 optional conditional O2 any-slot row | **ACCEPT as optional view** | It is a derived interpretation, not an extra match category; avoids new scans. |
| C20 byte/chunk and odd pad rules | **ACCEPT** | Simple explicit test constraints for nibble correctness. |

**No substantive reviewer disagreement remains known.** No second review is necessary to resolve Claude's comments, although the owner permitted one if a genuine blocker appeared. None has been identified. This specification still requires owner ratification.

## C2. Two items the owner should be aware of

1. The proposed **primary W→W+1 positional test** is one predeclared category per game (Powerball P3-any, Oz O3-any), 10,000 draw-label permutations of all draws, a two-sided centered test and Holm adjustment across six constants **within each game**. It is exploratory and does **not** demonstrate predictive ability. The owner may veto or change it **before scientific REAL scans**; changing it later must be labelled post-hoc.
2. A single new sibling directory `G:\OUTLANDISH_01\large_artifacts\results_null\` is proposed to keep all synthetic comparisons separate from the pre-existing `results\` REAL location. There is **no new owner-maintained registry or approval system**.

## C3. Owner decision requested

**Ratify v0.2 for the later matching/reporting implementation phase, or identify any substantive scientific disagreement.** Ratification fixes the *design*, not permission to begin scanner qualification immediately. The existing production sequence remains: **publish and verify all six constants first; then Q1–Q5**, with implementation and research runs undertaken only when separately scheduled/authorised by the owner. No code or data has been changed by preparing this document.

---

**End — OUTLANDISH_01 Shared Matching, Classification and Reporting Specification v0.2 (post-review proposed ratification text).**
