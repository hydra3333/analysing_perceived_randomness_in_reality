# Claude review - Powerball / Oz Lotto multi-game architecture (v2)

**Reviewer:** Claude (independent reviewer)
**Date:** 24 October 2026 (Adelaide)
**Version note:** v2 supersedes v1. Section 7 has changed: the owner withdrew the "assume 7 days apart" direction in favour of actual recorded draw dates and times where the source provides them.
**Reviews:** ChatGPT `Powerball_OzLotto_Architecture_Exploration_v0_1.md`, plus the owner's follow-up points made in discussion on 24 Oct (draw identity, dates).
**Repository inspected:** GitHub HEAD `34b23ad5bfb07f0a45c1bbba329396e8d9235dd4`.
**Status:** DISCUSSION / RECOMMENDATIONS ONLY. Development remains PAUSED. No code, ratification, scraping, test execution or holdout access is authorised by this document. The owner's points below are recorded as proposed conventions, for later ratification.

---

## 1. Timing - do it now, contract-first

The Powerball-specific code is still small. Literal 35 / 20 / 1144, the 1577-1587 holdout range and the two-barrel result shape sit almost entirely in:

- the E_1 maths module (`_common/e1_historical_appearance_frequency_v0_3.py`);
- the E_1 loader (`_common/e1_training_view_v0_1.py`);
- the standalone contract (`_common/e1_standalone_contract_v0_1.py`, target cap 1145..1577);
- the Powerball scraper;
- tests.

The coordinator is game-neutral apart from its file name. The scorer and walk-forward are not yet built, and E_2-E_6 are next. Each method written against a fixed two-barrel shape raises the later cost. So generalise now, together with the scorer/walk-forward work, and before E_2-E_6.

## 2. Recommended approach (revised after the owner's concern)

A synthetic second profile proves the code is portable, but it cannot confirm the assumptions about **real** Oz Lotto data:

- official data layout;
- that draw 1474 is 17 May 2022;
- cadence and any moved or delayed draws;
- whether drawn order is published;
- how the supplementaries are presented.

Getting these wrong late would be expensive. So build and test the real Oz Lotto profile now, and **stop before any science**:

1. **Before any scraping:** fix the `OZLOTTO` profile, define and seal its holdout, and fix its scope: current era from 17 May 2022, winning numbers only.
2. **Build the Oz Lotto scraper and `Run_Scraper.bat <game>`.** Use the same venv checks as the other wrappers. It writes dated, never-overwritten snapshots and prints their SHA-256. It produces two files:
   - a winning-numbers CSV, the only file the loader accepts;
   - a separate raw provenance CSV that keeps the supplementaries.
   
   Choosing which snapshot to train on stays a separate, deliberate step. Also fix the existing Powerball scraper, which writes its CSVs beside itself in `src/`.
3. **Structural validation only, on the real Oz Lotto data:**
   - exactly 7 distinct numbers in 1..47 per draw;
   - consecutive draw numbers from the era start;
   - the era start confirmed;
   - dates parseable and increasing (see section 7);
   - file hashes recorded.
   
   No frequencies, scoring or forecasts. This is the same position as Powerball's CSV, which already holds sealed holdout rows that are never parsed for science.
4. **Make the loader, scorer, result schema and target caps profile-driven.** Powerball must reproduce **exactly** (regression gate in section 4).
5. **Also keep a synthetic second profile in the tests** (one barrel, 7 of 47, no Powerball barrel). It is cheap and catches hard-coded literals.
6. **STOP POINT:** no Oz Lotto method run, real or development, until its own separately reviewed and owner-authorised gate.

## 3. Shape - two narrow game profiles, not a generic engine

- **One versioned, validated game profile, bound into every run's identity.** It holds:
  - `game_id`;
  - era;
  - first draw number;
  - a list of barrels `{barrel_id, lowest label, highest label, count selected}`;
  - development target cap;
  - holdout definition;
  - game closing time, in UTC (allowing for daylight saving).
  
  `--game` selects an approved profile. Barrel parameters are never free-form command-line values.
- **Methods declare the view and barrels they need.** Each game's registry lists **every** E-number (R2-C13) as one of:
  - `SUPPORTED`;
  - `UNSUPPORTED_FOR_GAME`, with a reason;
  - `FORMULA_OPEN`.
  
  Most methods rank each barrel independently, so they run on Oz Lotto's single MAIN barrel. Methods that use both barrels together become UNSUPPORTED for Oz Lotto. A second barrel is never invented.
- **Results per barrel.** The scorer is barrel-aware. Oz Lotto has one TOP seven, one WORST seven and one MAIN mean mid-rank. Its Powerball channel is **ABSENT** (not zero, not a disguised N/A).

## 4. Compatibility - Powerball must not change

- **Do not change `TIE_SHA256_V1` or any Powerball identity.** Game identity enters through the **training-view digest**, which is already field 2 of the tie tuple.
  - Powerball keeps `E1_REAL_U_TRAINING_VIEW_V1`.
  - Every new game's view schema must name the game and era. Reusing barrel ID `MAIN` across games is then safe, because the digests differ.
  - No new tie version is needed.
- **Results:** adding `game_id` to the result wrapper needs a new result-schema version. Old results stay valid under the v0.1 schemas.
- **Keep the accepted E_1 maths module as it is.** The parameterised code is a new module version.
- **Regression gate:** under profile-driven code, the following must reproduce exactly:
  - the Powerball synthetic goldens: training view `df21871f...`, tie digest for label 3 `7ce5ab1b...`, forecast `7b43d659...`;
  - the real 1577 forecast: training view `d47fbbd6...4339`, same ranking, TOP [9,17,7,11,18,30,12] PB 2, WORST [31,13,8,29,26,33,35] PB 12. The result-wrapper hash may change only through the new schema version, and only with an explicit label.

## 5. Draw identity (owner convention, endorsed)

| Field | Meaning | Example |
|---|---|---|
| `game_id` | The lottery | `POWERBALL`, `OZLOTTO` |
| `draw_number` | The operator's draw number | `1577` |
| `draw_key` | Human-readable form for display and filenames | `POWERBALL_1577` |

- **The authoritative identity is the pair (`game_id`, `draw_number`).** Carry it as two structured fields in every record, manifest, status file, log and score. Draw numbers are not unique across games; the same number in two games is legitimate.
- **`game_id` must match `[A-Z][A-Z0-9]*`, with no underscore**, so `draw_key` splits unambiguously at its last underscore.
- **The era is a property of a draw, not part of its key.** Oz Lotto's numbering continued through its 2022 change. The profile decides a draw's era, and loaders refuse draws outside the selected era.
- **Legacy records:** v0.1-schema records that lack `game_id` are defined once as meaning `POWERBALL`. New schemas **require** `game_id`; it is never inferred. The existing Powerball CSVs are left unmodified, because their verified hashes must stay valid. New snapshots may carry a `game_id` column, which the loader checks.
- **Scoring** looks up outcomes by the pair and refuses any mismatch. Run folders carry a game segment, and random run IDs are unchanged.

## 6. Time axis (owner convention, endorsed with one exception)

- **Within each game the time axis and sequence key is `draw_number`.** Intervals, lags, recurrence and walk-forward steps are counted in draws. Dates never enter keys, digests or ordering.
- **Exception: do not drop dates.** Ratified R1 includes two date-based methods:
  - **E_14 Calendar-Phase Conditional Patterns**, which uses date-derived phases (month, week of year, astronomical calendar);
  - **E_54 External-Date Covariate Synchrony** (view `U+X`), which uses weather, geomagnetic, lunar, solar or astronomical covariates known before a draw. R1 also lists "other game outputs" as a possible covariate.
  
  Removing dates would silently disable these, contrary to the no-exclusion rule. The owner's caveat about spacetime (Earth's position, relativity) is essentially the hypothesis E_54 tests.

## 7. Dates for E_14 / E_54 (owner decision, 24 Oct: use the actual recorded dates)

The owner's earlier "assume 7 days apart" suggestion is **withdrawn**. It was made only because it was unclear whether both games' sources record dates. The rule is now:

- **Use the actual draw date (and time, where the source records it) taken from the validated source snapshot.** It is per-draw metadata, never a key: identity remains (`game_id`, `draw_number`).
  - Powerball: the existing history CSV has a `Date` column for every draw.
  - Oz Lotto: official results show the draw date; the scraper's structural check must confirm it.
  - Both current CSVs record **dates only, not times of day**.
- **Where only a date is recorded,** the profile declares the game's nominal draw time and its timezone. This is needed for E_54's "known before the draw" test against external covariates. The declared time is labelled nominal, never presented as observed.
- **Fallback only if a game's source has no dates at all** (not currently expected for either game): nominal date = era-start date + 7 x (`draw_number` - the era's first draw number), explicitly labelled `NOMINAL_7_DAY` in the method's view and its results.
- **Dates enter only the views of methods that use them** (E_14, E_54 and later governed variants). They are excluded from the default U view, as E_1 already does, and never enter keys, digests or ordering.
- **Validation is a sanity check, not a gate:** dates must parse and strictly increase with `draw_number`. A non-weekly gap (a moved or delayed draw) is logged as a WARNING with its size, not refused, and is kept in the record, because to E_14 / E_54 it is real information. Powerball is exactly weekly across all 444 draws (1144-1587, checked by Claude on draw numbers and dates only). For Oz Lotto this is to be confirmed by the scraper.
- **The existing E_1 loader's strict weekly check** passes for Powerball. When the loader becomes profile-driven, make the cadence check a warning and keep `Date` out of the U view. The date is not part of the digest, so no Powerball identity changes.

## 8. Oz Lotto facts and scope

- **Current format:** 7 winning numbers from 47, plus 3 supplementaries, since **17 May 2022**. Previously 7 of 45 with 2 supplementaries.
- **Draw 1474 = 17 May 2022 is consistent but not yet confirmed.** It matches draw 1678 on 14 April 2026 at one draw per week, but that date was itself inferred from a news report. Confirm from official data.
- **About 230 current-era draws as of October 2026**, against Powerball's 444. A 10-draw holdout takes proportionally more, and data-hungry methods have less to work with. That is context, never a reason to exclude.
- **Supplementaries:** excluded from all model views, predictions and scoring (owner scope), but **archived raw** in the provenance CSV. They are 3 of the 10 balls of each physical draw. Within-draw order and physical-process hypotheses (for example E_23-E_32 and E_57-E_62) lose them under this scope. Archiving keeps a later, governed variant possible.
- **Holdout:** define and seal it **before** the first scrape lands in `source_data`, for example "the 10 most recent draws as of the first snapshot". Never reuse Powerball's 1578-1587. The development target cap comes from the profile.
- **Era changes:** if either game changes its rules in future, profiles must refuse cross-era data, so the pipeline stops rather than silently mixing eras.

## 9. Safety and operations

- **Single global orphan marker** (it already is global). Choosing another game must never get around it.
- **No hard "one game at a time" lock.** Each coordinator kills only its own captured, verified processes, so two runs cannot harm each other's processes. The real risk is overloading the PC (6 + 6 workers). An advisory check plus the owner's operating rule is enough. A hard lock would add a second interlock with its own stale-lock clearance procedure.
- **Keep the coordinator's file name** (`Powerball_Experiment_Coordinator.py`). Renaming changes its hash and the test pins with no safety gain. If wanted, rename it with v0.7.
- **Coordinated method runs still need:**
  - the coordinator-written `exit_receipt.json` (Claude decision);
  - a run-folder / run-ID handshake (E_001 currently requires `e1-` IDs and uses its own run root);
  - `--game` passed to each method, checked against that method's support status for the game.
- **Task Manager:** the Image name stays `python.exe`. Use the **Details > Command line** column, which shows the method file, `--game` and the run ID. Show game, E-number, `draw_key`, run ID and PID in STARTED status and the coordinator console.
  - **Do not rename executables.** That would break the `python.exe` allow-list, the venv redirector and the reviewed ownership model.
  - A console title is not a process name, and coordinator workers share one console.
  - A display label is never proof of ownership.

## 10. Other points the exploration missed

- **Per-game reference figures,** as context only:
  - Oz Lotto: expected TOP matches 7 x 7 / 47 = about 1.04; chance mean mid-rank 24.0; no Powerball channel.
  - Powerball: 1.4 TOP matches; Powerball hit 1/20; mid-ranks 18.0 and 10.5.
- **No pooling of scores across games** unless that is decided in advance. Each game keeps its own tracks, holdout, freeze and score history, and publication timing.
- **The development target cap 1577 is hard-coded in two places** (the loader and the contract's `begin()`). Move both into the profile.
- **Cross-game hypotheses** are deliberately excluded by "one game per run". E_54's "other game outputs" implies a possible future, governed variant, for example using the Tuesday Oz Lotto result as a covariate for Thursday Powerball. That is allowed in principle, because the Tuesday draw is known first. It would need a strictly time-ordered, read-only view of the other game. Do not design it out of the profile/view API.
- **E_63 (Chebyshev / minimax):** either a governed new R1 entry or an E_37 variant; the owner decides. It is independent of this review.

## 11. Decisions for the owner

1. Approve the approach in section 2: profile API, real Oz Lotto profile + scraper + structural validation, synthetic second profile, Powerball exact regression, then STOP before Oz Lotto science.
2. Oz Lotto scope: current era only, from 17 May 2022. Supplementaries excluded from views and scoring, but archived raw.
3. Oz Lotto holdout definition, fixed before the first scrape.
4. Layout: game-named filename prefixes (Powerball's are already `australian_powerball_...`) plus `game_id` in every record. New run folders carry a game segment. Existing Powerball paths and files are unchanged.
5. Record as proposed conventions, to be ratified with the next Architecture version:
   - the draw-identity convention (section 5);
   - the draw-number time axis (section 6);
   - date-using methods use the actual recorded draw dates; a nominal draw time is declared per profile; a 7-day nominal date is a labelled fallback only if a source lacks dates (section 7, owner direction).

## Sources (Oz Lotto facts)

- Oz Lotto - Wikipedia: https://en.wikipedia.org/wiki/Oz_Lotto
- Lotterywest, 16 May 2022 (changes from Tuesday 17 May): https://lotterywest.wa.gov.au/lotterywest/media-centre/oz-lotto-10-million-jackpot-could-ease-the-rainy-day-blues
- Lotterywest, 7 April 2022 game-change announcement: https://lotterywest.wa.gov.au/lotterywest/media-centre/bigger-prizes-and-more-winners-with-oz-lotto-game-change
- Oz Lotto draw 1678 report (Bendigo Times): https://www.bdtimes.com.au/news/lotto/oz-lotto-results-draw-1678-one-lucky-winner-scoops-incredible-15-million-prize-on-tuesday--c-22141260.amp

*End of review.*
