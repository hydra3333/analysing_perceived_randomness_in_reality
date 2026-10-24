# Predictive Randomness - Powerball / Oz Lotto Multi-Game Architecture
## Consolidated discussion v0.2 - Claude v2 review and owner feedback

**Date:** 24 October 2026 (Adelaide)

**Status:** DISCUSSION / REVIEW ONLY. **DEVELOPMENT REMAINS PAUSED** until the project owner explicitly authorises resumption. No code, scraper run, experimental run, scoring, holdout access, process-termination change, or FINAL publication is authorised by this document.

**Inputs:** ChatGPT's `Powerball_OzLotto_Architecture_Exploration_v0_1.md`; Claude's **`Claude_Review_MultiGame_Architecture_v2.md`** (v2 supersedes v1; do not use v1); the owner's clarifications on nonunique draw numbers, actual recorded draw dates, and keeping Task Manager display-name work simple. Claude inspected GitHub HEAD `34b23ad5bfb07f0a45c1bbba329396e8d9235dd4` for its v2 review. This document consolidates the discussion, **not** an acceptance of all reviewer recommendations.

**Authority:** Existing owner-ratified Proposal/R1/R2/R3, Architecture v0.5, Task Specification v0.2 and subsequent owner-ratified contracts remain authoritative until a separately reviewed replacement is ratified. Preserve all existing E_1 golden results and identities. Any apparent conflict is an issue for explicit resolution, not permission to override those documents.

### Status vocabulary

- **OWNER DIRECTION:** Stated by the owner in this discussion; may still need a precise specification and ratification where it changes architecture.
- **REVIEWER RECOMMENDATION:** Proposed by Claude, supported for consideration, **not automatically ratified**.
- **OPEN:** Decision or technical uncertainty to resolve before implementation.

## 1. Why assess this now?

The current Powerball proof is real: E_1 has run a permitted historical development forecast for draw 1577, trained through 1576, and its canonical result was validated by `verify_and_consume()` and independently recomputed by Claude. The historical scorer/walk-forward v0.1 is still a review candidate; no draw-1577 actual-result score was computed as part of this exploration.

Powerball assumptions (35/20 labels, two barrels, Powerball-specific draw limits, fixed schemas) remain concentrated in a few E_1/common modules, the scraper and tests. The generic scoring and walk-forward machinery, and E_2-E_6, are not yet finished. **REVIEWER RECOMMENDATION:** make the narrow contract extension now, alongside the scorer/walk-forward work, rather than copy/edit dozens of later methods.

The objective is **two explicitly validated game profiles with shared machinery where scientifically and technically appropriate**. It is *not* a generic any-lottery engine, and it is *not* two simultaneously selected games in one scientific run.

## 2. Owner's scope and operational preferences

1. **One game selected per invocation:** `POWERBALL` or `OZLOTTO`; a run's selected profile is fixed and recorded. This is not a demand for a new global hard concurrency lock. Operationally the owner intends not to run two games at once.
2. **Oz Lotto winning numbers only:** the first seven winning numbers are modelled and scored; the three supplementary balls are *not* model inputs, predicted labels or scored outcomes. **REVIEWER RECOMMENDATION:** preserve supplementaries in a separate raw/provenance archive to allow audit without making them accessible to current method views.
3. **Draw number is not a globally unique key.** The canonical identity is (`game_id`, `draw_number`), with a display `draw_key` such as `POWERBALL_1577` or `OZLOTTO_1577`.
4. **Use actual recorded draw dates.** The earlier suggestion to assume exactly seven calendar days between draw dates was **withdrawn**. Dates are metadata, not the draw identity or sequence key. When source data contains dates, preserve the actual dates, including unusual gaps.
5. **Task Manager naming: keep it simple.** The owner accepts ordinary `python.exe`/`cmd.exe` image names. Do **not** introduce renamed executables, embedding, custom launcher binaries or a dedicated monitoring program for display names. Existing command lines and status/log messages can identify `game_id`, E-number, draw key, run ID and PID. Display strings never prove process ownership.
6. **On-demand scrapers desired:** preferably a simple game-selected `.bat` launcher, with separate underlying scraper code. The user accepts responsibility for avoiding inappropriate overlapping operations, but snapshots must remain immutable and content-addressed.

These directions still require detailed compatibility/safety contracts before modifying ratified implementation architecture.

## 3. Candidate supported games and data era

| Field | `POWERBALL` | `OZLOTTO` |
|---|---|---|
| Intended era | Draw 1144 onward, 19 Apr 2018 | Current 7-of-47 format from 17 May 2022 |
| First draw ID for current era | 1144 | **Candidate 1474; must be checked against primary source** |
| Predictive barrels | `MAIN` 7 distinct of 1..35; `POWERBALL` 1 of 1..20 | `MAIN` 7 distinct of 1..47 |
| Supplementaries | Not in current targets | Three physically drawn; excluded from current modelling/scoring; raw provenance retained |
| Draw data view | Validated current unordered seven numbers + PB; optional separate drawn-order provenance | Validated seven winning numbers only; optional raw provenance includes supplementaries |
| Holdout | Existing sealed 1578..1587 | **OPEN:** independent period, sealed before any outcome-aware work |
| Dates | Actual `Date` value present in current history CSV | Validate actual dates in proposed scraper output |
| Nominal time | Profile's declared time and time zone, explicitly nominal | Same requirement; independently configured |

**Evidence boundary:** Claude describes Oz Lotto's 17 May 2022 rule change as established, but calls the specific **draw 1474** starting number *consistent but not independently confirmed*. Do not turn that candidate ID into a hard-coded rule before official verification. Earlier 7-of-45 observations must not silently cross into the current era.

## 4. Architecture under consideration - two narrow profiles

**REVIEWER RECOMMENDATION; not yet ratified:**

- Maintain a **versioned validated profile** with `game_id`, era, first draw, barrel descriptors (IDs, permitted labels and selected counts), holdout and development limits, nominal draw time/time zone, and applicable snapshot/input rules. Never accept arbitrary command-line barrel counts or label ranges in place of selecting a reviewed profile.
- Permit `--game` to select one approved profile. All runs, statuses, manifests, canonical results, output folders, reports and human-readable messages include unambiguous game/draw identity. New run directories may have a game segment; **legacy Powerball locations and hash identities must remain valid**.
- Use **separate scrapers**, a shared versioned permitted-view interface, a game-aware scorer, compatible shared E-method code and one safety-reviewed coordinator/launcher pathway (Option F). Preserve the global unresolved-orphan marker regardless of game.
- A game's E-method roster records every registered E-number as `SUPPORTED`, `UNSUPPORTED_FOR_GAME` (with an actual structural reason) or `FORMULA_OPEN`. Never invent an Oz Lotto `POWERBALL` barrel or exclude methods merely because standard theory predicts no predictive signal.
- Represent TOP/WORST, native-score rank statistics and chance-reference context **per actual barrel**. For Oz Lotto, no Powerball channel exists (not zero, fake data or a misleading N/A statistic).
- Treat source archives as **immutable snapshots**. Scraping and selecting a snapshot for training are separate acts. The existing Powerball source files and hashes are not overwritten.

### Scraping and initial Oz Lotto data boundary

Proposed `Run_Scraper.bat <game>` with the established venv checks. Produce a dated no-overwrite **winning-number CSV** (the only file allowed in a current Oz Lotto training view) and a **separate raw provenance CSV** retaining supplementaries. Emit source/provenance hashes. Fix the existing Powerball scraper's default output location beside `src/` without silently rewriting or replacing already accepted `source_data` files.

**Important sequencing proposed by Claude:** ratify the Oz Lotto era/profile and independent holdout first; then scrape, perform **structural validation only** (7 distinct winning labels in 1..47, draw continuity, date validity, source hashes, raw/winning segregation), and **STOP before any Oz Lotto predictions, counts, evaluation or tuning**. A structural validation may have to inspect sealed rows to validate their shape; it must not analyse, score or report their values and needs a clearly bounded audit interface.

### Regression obligations

- The accepted E_1 mathematical module and the accepted Powerball input/view schema remain preserved as history. Parameterised modules/results get **new** versions where representation changes.
- Keep existing `TIE_SHA256_V1` byte encoding and tie tuple unchanged. The existing Powerball training view remains `E1_REAL_U_TRAINING_VIEW_V1`; the game/era must be bound into **new-game** training-view schema/identity, avoiding cross-game collisions without perturbing accepted Powerball digests.
- Powerball synthetic golden view `df21871f...`, label-3 tie digest `7ce5ab1b...`, forecast `7b43d659...` must remain identical in the legacy path.
- Powerball real draw 1577 view `d47fbbd6...`, forecast result `7f113087...` and selected TOP/WORST must be reproducible. If a **new** result wrapper/schema embeds `game_id`, its new content hash must be explained and labelled; it does not retroactively invalidate the old result.
- v0.1-schema legacy records lacking `game_id` are interpreted as `POWERBALL` by an explicit **versioned compatibility rule**, not a general inference for new records. New schemas must explicitly carry `game_id`.

## 5. Draw identifiers, dates and scientifically valid view digests

### 5.1 Identity and indexing

**Owner direction:** authoritative key = (`game_id`, `draw_number`). Claude proposes `[A-Z][A-Z0-9]*` for `game_id` to support unambiguous parsing of optional `draw_key = GAME_1234` labels. Era is a validated attribute/rule, *not* part of the draw key. Run and output identifiers must not collide across games.

For training and recurrence, `draw_number` is the **within-game sequence index**. Draw dates do not replace that index and must not be assumed to be spaced by seven days. If a source contains dates, validate they parse and strictly increase with draw sequence. **Non-weekly gaps are preserved with warnings, not treated as automatic errors.**

### 5.2 Date-dependent methods

R1's E_14 (calendar-phase) and E_54 (external date covariates, view `U+X`) legitimately use dates; later governed variants may do so too. Those methods use the **actual recorded date**, not a synthetic weekly date when one is present. When only a date is recorded, a versioned profile supplies a **nominal** local time/time zone for pre-draw availability assessment; nominal is labelled, not passed off as an observed draw timestamp. If a future game's source contains no date at all, Claude documents a possible explicitly labelled `NOMINAL_7_DAY` fallback based on era start and draw-number offset. This exception remains for further scrutiny, not a reason to replace actual dates.

**OPEN - scientific-contract clarification needed:** Claude v2 section 6 says dates should never enter keys, digests or ordering, but section 7 correctly requires date-derived inputs in E_14/E_54 views. Under the ratified N-1 / training-view identity rule, **the date fields actually consumed by a date-dependent method should normally contribute to that method's permitted training-view digest** (and thus its fit seed/identity where specified); otherwise changing a meaningful date input could change the prediction without changing the view identity. This **does not** mean putting dates into E_1's `U` digest or altering accepted Powerball hashes. Request Claude's explicit reconciliation and a date-mutation / suffix-poison test for date-dependent views.

**OPEN - availability semantics:** E_54's known-before-draw condition must distinguish external observations actually available by the time of the forecast from nominal clock metadata, taking time zone and daylight saving into account. A nominal scheduled time is not independently verified historical publication timing. Resolve only when preparing E_54's specific formula/data contract.

## 6. Experimental scope and future results

- R3 TOP/WORST and native-score rank-position measures apply per genuine barrel, with score reference figures calibrated to its labels/selection count and shown as **context**, never as a veto on methods.
- Report per-game performance separately; do not pool Powerball and Oz Lotto results without a specifically pre-registered rule. Separate holdouts, development caps, freeze/publication deadlines and FINAL track identities are required.
- The synthetic/real firewall and FAILED/orphan-suspected result rejection apply unchanged, including to cross-game snapshots and future scorers.
- One-game-at-a-time scientific runs do not preclude a **future separately governed cross-game covariate** (e.g. known Tuesday Oz Lotto output in a later Thursday Powerball E_54 input). Design the view API so such a strictly time-ordered read-only input is not inherently impossible, but **do not implement cross-game modelling now**.
- Proposed E_63 Chebyshev/minimax is **not yet ratified into R1**. Its registration as a new E-number versus a governed E_37 variant remains a separate owner decision; it is not a dependency of the multi-game work.

## 7. Windows operations and process naming - deliberately minimal

**Owner direction:** accept ordinary `cmd.exe`/`python.exe` in Task Manager. Do not add executable-name wrappers, embedded Python, binary launchers, custom process monitors, or a new observability subsystem.

Low-cost candidate conventions only:

- Pass the approved `--game` when doing so fits the existing Option F interface and source review; Task Manager **Details > Command line** can show the Python script, game argument and run ID.
- Print and record `game_id`, E-number, `draw_key`, run ID and PID in the existing STARTED/status/console paths. Where a process hierarchy has several wrappers, not every CMD process will display a readable custom name; that is accepted.
- **No display label is process ownership proof.** The ratified PID + creation time + verified ancestry + status rules remain unchanged. Do not change the `python.exe` allow-list merely for presentation.

This is a minor part of the ordinary multi-game interface design, **not a standalone engineering project or review gate**.

## 8. Safety and workflow

- The **global** `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json` remains authoritative, for either selected game. A game switch cannot bypass it.
- No new hard simultaneous-game lock is proposed. Operational instruction: one selected game per run and avoid overlapping independent coordinators; optionally produce a non-authoritative/advisory warning if a second invocation is observed. The orphan marker is **not** a general busy lock.
- Future coordinated real methods still need Claude's previously identified `exit_receipt.json` and run-directory/run-ID handshake. Coordinator termination remains subject to separately reviewed changes and explicit owner approval; `ENABLE_PROCESS_TERMINATION` stays disabled while those gates are outstanding.
- Desired future user loop per selected game: scrape immutable snapshot -> independently validate the previous frozen forecast and score against the subsequently available result -> train on strictly permitted history -> freeze TOP/WORST for the next target before draw -> later compare outcomes. The game, draw, method and run identities are always visible. Scraping alone never silently changes the training snapshot in a running experiment.
- The E_1 scoring/walk-forward review and coordinator v0.7 safety work are **paused**, not cancelled. No new actual-result scoring or Oz Lotto method execution under this discussion authority.

## 9. Smallest candidate implementation sequence (only after ratification and explicit resume)

1. **Contract/identity design + golden gate:** Ratify narrowly scoped two-profile Architecture revision, draw/view IDs, era handling, holdout, and preservation of existing Powerball E_1 identities. No destructive or FINAL changes.
2. **Profiles and scraping:** Implement reviewed Powerball/Oz Lotto profiles, `Run_Scraper.bat <game>`, immutable game-specific snapshots, separate Oz Lotto winning/raw provenance and structural-only real-data validation. Confirm the actual Oz Lotto era-start draw ID from primary evidence. STOP before Oz Lotto science.
3. **Common permitted views + barrel-aware scorer:** Parameterise the existing Powerball scorer/walk-forward before broad method implementation; retain exact legacy Powerball regression results and introduce synthetic one-barrel 7-of-47 tests.
4. **Runner/coordinator compatibility:** Add game selection and output identities without weakening Option F, the orphan interlock, status verification, or retained-process rules; coordinate this with the existing v0.7 safety review rather than mixing it into an unreviewed change.
5. **Explicit gates:** Claude reviews scientific/identity/safety boundaries; owner authorises real Oz Lotto experimental work separately. E_2-E_6 and further method-family work resume when the owner releases the pause.

The ordering of steps 2-4 is still **OPEN** if evidence or change isolation suggests a safer or faster split.

## 10. Decisions outstanding for the project owner

| Question | Working recommendation | Status |
|---|---|---|
| Do it now or defer? | Narrow two-profile contract work **now**, before E_2-E_6; no broad generic engine | OPEN |
| Profile + real Oz Lotto scraper / structural validation | Yes, but stop before science | OPEN |
| Oz Lotto supplementary policy | Winning-only permitted view; supplementaries held solely in raw provenance | Owner scope stated; detailed contract OPEN |
| Oz Lotto holdout | Choose fixed boundary by draw number before new real snapshot/outcome-aware work; 10 most recent in first snapshot is one option, **not selected** | OPEN |
| Game IDs and `draw_key` representation | `POWERBALL`, `OZLOTTO`; authoritative pair; new schemas require game | Owner identity principle stated; exact contract OPEN |
| Existing Powerball identity compatibility | Preserve exact legacy digests/readouts; version new wrappers | OPEN |
| Date metadata and method-specific digest | Actual source dates; method-consumed dates in relevant view identity; no dates in E_1 U digest | Owner actual-date direction; digest reconciliation OPEN |
| Timezone/nominal-time semantics | Profile time and zone labelled nominal, not observed | OPEN |
| Process display naming | Accept default image names; descriptive args/messages only | Owner preference established; no complex solution |
| Safety/concurrency | One game selected per run; global orphan marker; no extra hard busy lock | OPEN detailed architecture |
| New per-game method support roster | Explicit SUPPORTED/UNSUPPORTED_FOR_GAME/FORMULA_OPEN with reasons | OPEN |

**No decision in this table is silently implemented or deemed architecture-ratified by this document.**

## 11. Reviewer request - Claude v2 follow-up

Claude's v2 supersedes v1 and is the current reviewer baseline. Please review this consolidation **openly**, not merely as a proofreading exercise:

1. Is the two-narrow-profiles migration at this stage still the best route? What smaller or safer alternatives are overlooked?
2. Reconcile actual dates as model inputs for E_14/E_54 with the requirement that consumed permitted-view inputs determine digest/fit identity, without changing E_1's U-view digest or existing Powerball tie vectors.
3. Identify exactly when the Oz Lotto holdout must be fixed and what limited structural inspection of its rows is permissible before it is sealed.
4. Challenge the proposed minimal game-aware schema, historical compatibility, process-safety and scoring boundaries, including any unnoticed hard-coded assumptions.
5. Confirm or correct the proposed Oz Lotto first draw/era facts from primary evidence when available; do not silently promote the candidate draw ID to a verified fact.
6. The owner has **de-scoped Task Manager executable renaming**. Accept default `python.exe`/`cmd.exe`; use only low-cost game/method/run IDs in args and existing logs. Do not recommend a new monitoring system without a compelling operational reason.
7. Distinguish issues requiring owner ratification from routine implementation choices and identify a genuinely minimal stop/go package. No coding, real-data run, holdout unsealing or development resumption is requested.

## 12. Short paste-ready accompanying note

> **Multi-game architecture follow-up, 24 Oct 2026 - DISCUSSION ONLY.** Development remains PAUSED. Attached is ChatGPT's consolidated v0.2 discussion using your **Claude review v2** (v1 superseded), plus the owner's new instruction to avoid complex Task Manager process naming. The owner accepts ordinary `python.exe`/`cmd.exe` names; concise `--game`/method/run arguments and existing STARTED/log identities suffice. Actual recorded draw dates prevail; the prior seven-day assumption is withdrawn. Compound (`game_id`, `draw_number`) identity remains essential. Please independently assess the design and explicit open issues, especially whether date inputs in E_14/E_54 should enter their *own* training-view digest (without changing E_1's U view), the independent Oz Lotto holdout and pre-scrape inspection gate, and the smallest safe migration before E_2-E_6. No implementation or ratification is requested in this round.

---

**End of consolidated discussion v0.2.**
