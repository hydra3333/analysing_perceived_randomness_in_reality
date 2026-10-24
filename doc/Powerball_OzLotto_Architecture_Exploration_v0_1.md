# Predictive Randomness - Powerball / Oz Lotto Architecture Exploration v0.1

**Date:** 24 October 2026 (Adelaide)
**Status:** DISCUSSION ONLY - NOT A SPECIFICATION, NOT RATIFIED, NO CODE AUTHORISED
**Purpose:** Evaluate whether to generalise the existing Powerball research architecture now, before E_2-E_62 are broadly implemented, to allow separate Australian Powerball and Oz Lotto runs with as much shared experimental machinery as practical.
**Development pause:** In force. No implementation, scraper execution, real historical scoring, holdout access, FINAL runs or coordinator safety changes are authorised by this document. Resume development only after the owner explicitly agrees.
**Authority:** Existing ratified repository documents prevail. Options below are questions for owner/Claude review, NOT silently adopted decisions.

## 1. Current state and scope

- First real Powerball E_1 historical-development prediction (target 1577, trained through 1576) is completed and verified through `verify_and_consume()`. Its forecast, training-view and canonical-result identities are preserved. The scoring/walk-forward v0.1 package awaits its own review/ratification; **no draw-1577 outcome was scored as part of this architectural exploration**.
- Powerball has two prediction barrels: MAIN (select 7 distinct numbers from 1..35) and POWERBALL (select 1 from 1..20). Eligible current-rule era begins draw 1144, 19 April 2018. Development holdout 1578..1587 is sealed.
- Oz Lotto currently has one physical barrel of 47 distinct labels. First 7 drawn numbers are its winning numbers; the next 3 are supplementary. **The owner's proposed research rule excludes the supplementary numbers entirely from model inputs, predictions and scoring.** This is a proposed scope rule, not an assertion that supplementary numbers do not exist.
- Oz Lotto's present 7-of-47 plus 3-supplementary matrix began **17 May 2022, draw 1474**, replacing the earlier 7-of-45 / 2-supplementary matrix. Older observations cannot silently enter the present-era dataset.
- Runs are envisioned as **one game per invocation**, even if one game's methods run with several workers. Simultaneous Powerball and Oz Lotto coordinator runs are outside the proposed scope.

Sources for external game facts:
- The Lott, How do I play the Oz Lotto game: https://help.thelott.com/hc/en-us/articles/4416863329689-How-do-I-play-the-Oz-Lotto-game
- Lotterywest, 7 April 2022 announcement (17 May 2022 launch): https://www.lotterywest.wa.gov.au/lotterywest/media-centre/bigger-prizes-and-more-winners-with-oz-lotto-game-change
- Official Oz Lotto game-rule schedule (2024): https://www.thelott.com/content/dam/projects/the-lott/game-rules/nt/Tatts-NT_Rules-of-Authorised-Lotteries_6-May-2024.pdf

## 2. Answers to the immediate questions

### 2.1 Is there an on-demand scraper .bat?

**Evidence from the supplied repository ZIP and the identified scraper at pinned GitHub revision fbb66ef:** A Python scraper exists, `src/scrape_australian_powerball_history_from_2018_04_19_v0_3.py`, but a dedicated scraper `.bat` was not found among the repository's root launchers (which include `Run_Experiment.bat` and `Run_Coordinator.bat`). This is an audit of the supplied snapshot/root listing, not a claim about uninspected future commits.

The Python scraper has an ordinary command-line entry point, with optional `--official-order`; it can be launched manually using the project venv. It currently writes its date-stamped CSVs **beside itself in `src/`** (`Path(__file__).with_name(...)`), not automatically to `source_data/`. Existing validated snapshots under `source_data/` must not be assumed to have been placed there automatically by this scraper. It atomically publishes its output after validation, subject to its documented limits; optional independent order verification makes many extra page requests.

**Possible future improvement (not decided):** add `Run_Scraper.bat <game>` to select the proper game-specific scraper, check the venv, validate/capture a new immutable source snapshot, report hashes and provenance, and never silently replace the currently selected training source. Concurrent scraping while a prediction is running is operationally the owner's responsibility as proposed; immutable snapshots and content identities nevertheless protect reproducibility.

### 2.2 Can a Python experiment have a custom process name in Task Manager?

Not in the ordinary Windows **Image name** field just by assigning `multiprocessing.Process.name`, setting an environment variable or changing a console title. The interpreter processes will normally display as `python.exe` (and the existing Windows batch/venv hierarchy may also show `cmd.exe` and Python redirectors). Renaming or copying interpreters into separate `Powerball_E_001.exe`/`OzLotto_E_001.exe` executables is possible in principle but materially changes executable provenance, process allow-lists and the already-reviewed ownership/termination model. **Do not adopt this merely for cosmetics.**

Practical choices for review:
1. **Low-risk default:** expose the Task Manager **Details > Command line** column and include `--game Powerball` / `--game OzLotto`, the E-method filename and run ID in the process command line. Retain `python.exe` as the executable image.
2. Log/display `GAME / E_NUMBER / TARGET / RUN_ID / PID` in STARTED status and coordinator console. Optionally build a lightweight project-side status view later.
3. Give a dedicated console/window a descriptive title only if separately verified to work with the existing piped, multiworker console design; a console title is **not** a process image name and may be shared among workers.
4. Investigate dedicated executables/process-title APIs only on a specific, justified request and after a fresh safety review. Not recommended now.

The no-status/no-kill and PID + creation-time + captured-ancestry safety rules remain binding regardless of any display names. A display label is NEVER ownership proof.

## 3. Why examine the multi-game extension now?

**Recommendation for discussion, NOT an owner decision:** now is preferable to after implementing most methods, because present logic still contains Powerball-specific assumptions in data validation, the E_1 loader, output representations, scoring, tie identities, coordinator entry points and reports. A controlled generalisation of the **contracts** now may avoid large-scale copying/editing later. But do not block the completed E_1 baseline or demand an unlimited abstract lottery framework.

The correct goal is **two supported game profiles with common infrastructure**, rather than a universal lottery modelling engine. Preserve the proven Powerball single-game path as an exact regression baseline.

## 4. Candidate separation of responsibilities (all OPEN)

| Component | Candidate direction | Important boundary / unknown |
|---|---|---|
| Acquisition/scraper | Separate game-specific scraper implementations | Different websites, formats, page layouts and change histories; do not force one parser |
| Game metadata | One validated, versioned game configuration | `game_id`, game-era ID, start draw/date, schedule, barrels and legal readouts; not untrusted free-form CLI controls |
| Source archive | Game-specific, immutable source snapshots | Timestamp, source, SHA-256, game/era; raw supplementary fields may be archived for provenance but cannot flow into Oz Lotto model views |
| Observation loader | Common, typed game-specific *permitted training view* API | No target or later-row leakage, correct prefixes and game-era; provenance excludes irrelevant columns when required |
| Experiment methods | Reuse E-number / scientific formula where legitimately general | Method may be unsupported for a game or need a governed game-specific variant; never fabricate a second barrel |
| Coordinator/worker | Shared launcher and scheduling, with one game selected per run | Preserve Option F (`Run_Experiment.bat`), safe process ancestry, venv rules, and global unresolved-orphan interlock |
| Results/status | Common schema with explicit game/era identity | All display text, folders, manifests, hashes and freeze/score records identify the game and draw |
| Scorer | Generic barrel-aware evaluation of actual legal predictions | TOP/WORST per available barrel; native-score mid-ranks; correct game-specific reference figures |
| FINAL/weekly loop | Shared orchestration, one separately identified game per invocation | Separate draw schedules, freeze identities, outcomes, report histories and publication timing |

Illustrative logical boundary (NOT a file-layout prescription):

```text
Powerball scraper -----\
                       -> validated game-specific snapshot -> permitted generic draw view
Oz Lotto scraper ------/                                    |
                                                            v
                                      game-scoped runner + compatible E-methods
                                                            |
                                                            v
                                      game-scoped forecast -> post-draw evaluation
```

## 5. Candidate game/barrel declaration

This is a **conceptual** data contract, not JSON approved for implementation.

| Property | Powerball current era | Oz Lotto current era |
|---|---|---|
| Stable `game_id` suggestion | `Powerball` | `OzLotto` |
| Game-format/era | Draw 1144 onward, 19-Apr-2018 | Draw 1474 onward, 17-May-2022 |
| Effective prediction barrel #1 | `MAIN`: labels 1..35; select 7 | `MAIN`: labels 1..47; select 7 |
| Effective prediction barrel #2 | `POWERBALL`: labels 1..20; select 1 | **Absent** |
| Supplementary balls | None in studied main/PB targets | Physically drawn 3; **excluded from all research views and scoring under proposed owner scope** |
| Draw cadence | Thursday | Tuesday |
| Development holdout | 1578..1587, already ratified | To be independently specified and sealed **before outcome-aware Oz Lotto experiments** |

A list of barrels such as `[{id, lower_label, upper_label, selected_count}, ...]` is more robust than four unrelated parameters such as number-of-barrels/max-label/draw-count. It permits different barrel sizes and selection counts, and prevents nonexistent `POWERBALL` fields on Oz Lotto. Distinguish **physical drawing procedure** from **effective prediction targets**; do not implicitly include supplementary balls in eligible model inputs.

Configuration must be **versioned and validated** (and included or bound in run identities), not merely user-supplied numbers that bypass an era gate. A `--game` selector could choose an approved profile; an experimental alternate ruleset is a separate, explicitly marked research mode.

## 6. Non-obvious impact inventory

### 6.1 Method applicability

- E_1 frequency on MAIN should transfer conceptually (7/35 vs 7/47), but its current canonical encoding and historical Powerball E_1 results must remain stable. Do not quietly mutate or overwrite existing outputs.
- Some methods examine cross-barrel relationships, Powerball-only behaviour, or order-sensitive inputs. A one-barrel Oz Lotto run should declare `SUPPORTED`, `UNSUPPORTED` or a governed Oz Lotto variant for each method. It must not invent a pseudo-Powerball or silently omit a registered experiment.
- R1's method inventory and E-number governance persist across games. Game-specific formula changes may justify new variants, and genuinely different hypotheses may justify new E-numbers; decisions remain governed. E_63 registration remains a separate outstanding matter.
- Method formulas with `35`, `20`, `7`, uniform-reference terms, tie boundaries, readout counts or training start hardcoded need per-method audits. Some model families may not generalise automatically. If Oz Lotto drawn order is needed by an order-sensitive method, the order of **only the first seven winning balls** must be separately sourced and proven; ascending numerical order is not physical draw order, and supplementary positions remain outside the proposed permitted view.

### 6.2 Identity, hash compatibility, and isolation

At minimum each run should unambiguously identify `(game_id, game_format_version, target_draw, method, variant, barrel_id, training_view_digest, run_id)`. A source-file SHA-256 and immutable snapshot provenance can be tracked separately from permitted-view hashes. **Game ID and format must domain-separate new multi-game canonical identities** to prevent two games with the same draw number or a coincidentally identical source view from sharing forecast identities.

Important compatibility question: the ratified existing Powerball `TIE_SHA256_V1` key order/encoding and E_1 golden vectors **must not silently change**. Options include (A) preserve old Powerball identity scheme and introduce a new game-scoped contract version for multi-game work, or (B) explicitly approve a migration with old outputs immutable and fully distinguishable. Claude should advise the minimal safe path.

Use game-qualified paths or prefixes for source, run, forecast, report and evidence artifacts. Whole-tree renames are **not** intrinsically required. Two plausible layouts:
- Directory scope: `source_data/Powerball/...`, `source_data/OzLotto/...`, `results/Powerball/...`, `results/OzLotto/...`.
- Filename prefix: `Powerball_...`, `OzLotto_...` in current directories.

Directory scoping plus explicit `game_id` in **every saved record** is a likely better long-term default; keep original historical paths and manifests read-only and backward-compatible. File/directory names alone are insufficient as an integrity identifier.

### 6.3 Global process/orphan safety

- Preserve **one** coordinator's ownership model and the owner-ratified no-status/no-kill rule. Selecting another game must not create an escape hatch around an existing unresolved-orphan marker.
- A global admission check / interlock must block all game starts while any unresolved orphan exists (unless a deliberately reviewed stronger interlock is ratified). Per-game run directories may coexist for evidence, but per-game markers alone risk bypass.
- If the owner requires **no simultaneous games**, enforce the one-active-game policy in orchestration or an operator gate; do not rely solely on goodwill or assume the orphan marker is a general concurrency lock.
- Do not rename executables without reviewing allow-lists, interpreter redirectors, PID/process-creation-time matching, retained ancestry and the termination safety switch.

### 6.4 Evaluation and holdouts

- R3 metrics must be parameterised by actual barrels. Oz Lotto would have one TOP seven-set, one WORST seven-set and one MAIN mean native-score mid-rank; it would have **no Powerball score**, rather than zero or N/A disguised as a result.
- Reference distributions differ with number of labels and selected set sizes (e.g., expected main intersection `selected^2 / barrel_size` for a uniform fixed set). Label reference-model results as contextual only, never as exclusions of methods.
- Each game has independent holdout boundaries, epochs, timestamps, weekly freeze/score history and experimental disclosure. **Do not apply Powerball's 1578..1587 holdout draw IDs to Oz Lotto.** Oz Lotto's holdout must be proposed, approved and sealed before its outcome-aware modelling begins.
- Keep synthetic/real separation, N-1 prefix rules, outcome loader restrictions and the failed-group/orphan result firewall at all games and all output consumers.
- Forecast publication must identify the selected game and its authoritative draw closing/publication timing. The Lott says Oz Lotto ticket sales close at 7:30 p.m. AEST on Tuesdays; that is a **closing time**, not proof the winning draw results are available at that moment.

### 6.5 Data freshness and operator workflow

Consider a simple game-selected user path:
1. Scrape/retrieve chosen game's new results and validate a fresh **immutable** snapshot; log date/source/rule era/hash.
2. Separately verify/score the last frozen forecast against the newly available actual result, with no retrospective refit.
3. Fit/refresh all eligible methods only on the permitted prefix and freeze forecasts for the next target.
4. Produce a game-qualified operator report: actual last draw, per-method previous forecast vs actual, and separately next-draw TOP/WORST; explicit missing/failed/unsupported statuses.

The owner may opt to run scrapers at will, including during predictions, but immutable snapshots ensure a run is unaffected if live upstream files change. No code here schedules or automates a scraper.

### 6.6 Repository and documentation effects

Likely affected: scraper entry points and source layout; ratified Architecture 5C and discovery conventions; R2 input/status/variant and N-1 contracts; R3 scoring/reference/prospective mode; coordinator launch arguments and safety checks; E_1 loader/runner and future methods; CLI wrappers; results and archival manifests; test fixtures; method game-support roster; documentation/handback.

A new **independent multi-game architecture proposal** could enumerate all changed contracts before editing ratified documents. Then, after owner decision and Claude review, publish a self-contained replacement Architecture version; do not leave hidden operative errata. R1/R2/R3 changes should be minimal and explicitly governed, preserving their existing Powerball requirements until ratification.

## 7. Architectural options for Claude to assess

| Option | Description | Indicative trade-off |
|---|---|---|
| A - Defer | Complete Powerball, then clone/edit for Oz Lotto | Easiest immediately; highest divergence, duplicate bugs and expensive later reconciliation |
| B - Two narrow game profiles now | Separate scrapers + versioned two-profile loader; shared coordinator/results/evaluator where possible; compatibility-gated methods | Preferred **discussion hypothesis**: modest near-term cost, prevents hardcoded assumptions spreading |
| C - Comprehensive generic engine now | Broad arbitrary multi-game framework, user-supplied rule topology, generalised all experiments | Most abstraction, highest risk of scope expansion and delay to real experiments |
| D - Isolated Oz Lotto runner with shared library | Separate front-end/CLI/coordinator for each game, reuse only stable library contracts | May isolate risk but doubles orchestration and safety maintenance |

A staged version of B is worth considering: first freeze a profile/identity/view API and Powerball compatibility tests; then add the Oz Lotto scraper/profile and a single adapted E_1, before extending other methods. **No option is selected here.**

## 8. Open decisions / questions (all OPEN)

1. **Timing:** endorse an architecture review now (while coding is paused) or defer until the approved Powerball scoring evaluator is finished? Is there a smaller contract-first scope?
2. **Supplementary provenance:** exclude the three Oz Lotto supplements from all model views/scoring as proposed; may raw scraper archives store them solely for auditing, with explicit code-level exclusion from permitted views?
3. **Game identity:** choose exact stable identifiers `Powerball` / `OzLotto`, versioned era rules and canonical representation; use `--game` to select a preapproved profile?
4. **Data layout:** game-named subdirectories, filename prefixes, or both? How to preserve historical Powerball paths and reproducible hashes?
5. **Compatibility:** preserve the existing Powerball `TIE_SHA256_V1` identity unchanged and introduce a game-aware revision, or another scheme?
6. **Method roster:** shared E-number vs per-game applicability/variants; explicit unsupported outcomes for Powerball-only / two-barrel methods?
7. **Holdout:** how many Oz Lotto historical draws and what frozen period? Approval must precede evaluating outcomes.
8. **Coordinator safety:** exact one-active-game interlock design without touching the no-status/no-kill safety contract or permitting marker bypass?
9. **Operator view:** is Task Manager Command line plus logging adequate, or is a custom visible executable image name essential enough to justify an independent high-risk design review?
10. **Scraper UX:** one generic `Run_Scraper.bat --game ...` or separate `Run_Powerball_Scraper.bat` / `Run_OzLotto_Scraper.bat`, output into which immutable store and under whose controlled source selection?
11. **Scope:** what minimum engineering spike demonstrates portability without postponing E_1 scoring and the E_2-E_6 methods?
12. **Scientific integrity:** when may Oz Lotto outcomes first be inspected; how should its initial rules and holdout be frozen and evidenced?

## 9. Suggested reviewer investigation (deliberately non-prescriptive)

Request Claude to independently inspect the current GitHub commit and ratified Architecture/R2/R3, then assess:
- Whether it is **better now or later**, considering actual implementation state and concrete migration costs.
- Alternative architectures, including approaches not mentioned here; not to constrain review to options A-D.
- Differences between a reusable method and a game-specific hypothesis, without weakening the 62-method inventory and E-number governance.
- All locations where literal 35/20/7, Powerball naming, era starts, fixed two-barrel result shapes, holdouts, score chance references, result hashes, `source_data` trust paths and coordinator ownership identities are assumed.
- A backward-compatible minimal migration and test plan, with independent safety/scientific gates and an explicit stop point before broad method implementation.
- How to label experiments visibly in Task Manager **without** changing the process image, if practicable; when a distinct executable is justified, identify safety implications.
- Unanticipated vulnerabilities or omissions in this discussion.

**Owner decisions:** NONE taken in this exploration. Any owner decisions made in subsequent dialogue should be appended to a versioned revision rather than retroactively claimed here.

## 10. Paste-ready note to Claude

> **Powerball / Oz Lotto architecture exploration - DISCUSSION ONLY, development PAUSED.** The owner asks whether now, while E_1 is verified and before most methods are implemented, is the right time to support **one game per run** for Australian Powerball and Tuesday Oz Lotto without cloning the eventual large codebase. Powerball is 7/35 MAIN plus 1/20 PB; Oz Lotto current era starts draw 1474 (17 May 2022), 7 winning of 47, with 3 supplementary numbers which the owner proposes **excluding from model inputs/predictions/scoring**. The possible shape is game-specific scrapers, versioned game profiles, a generic permitted training-view API, shared methods/coordinator/scorer where scientifically applicable, explicit game/era identities in all data/results, per-game holdouts and no synthetic/real leakage. Preserve existing Powerball results/hashes, Option F, process ownership and the **global** unresolved-orphan interlock; do not fabricate a second Oz Lotto barrel. Practical questions: no dedicated scraper .bat was found in inspected snapshot; Python scraper currently writes dated CSV beside script in src; on Windows the Python process image name cannot normally be customised, but Task Manager Command line can identify game/method/run. Please independently challenge both **timing and design**, identify missed architecture contracts and safer/simpler alternatives, review Oz Lotto change-era and supplement handling, and propose a minimal path to a decision. **No code, architecture ratification, test execution, holdout access, or resumption of development is authorised.**

---

**End of v0.1 discussion draft.**
