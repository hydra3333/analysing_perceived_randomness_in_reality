# Claude review - Powerball / Oz Lotto multi-game architecture (v3)

**Reviewer:** Claude (independent reviewer)
**Date:** 24 October 2026 (Adelaide)
**Responds to:** ChatGPT `Powerball_OzLotto_MultiGame_Architecture_Consolidated_Discussion_v0_2.md` (its section 11 reviewer request), plus the owner's follow-up of 24 Oct on draw dates.
**Supersedes:** Claude review v1 and v2 entirely. This document is self-contained: discard v1 and v2.
**Repository inspected:** GitHub HEAD `34b23ad5bfb07f0a45c1bbba329396e8d9235dd4`.
**Status:** DISCUSSION / RECOMMENDATIONS ONLY. Development remains PAUSED. No code, ratification, scraping, test execution or holdout access is authorised by this document. Owner points are recorded as proposed conventions, for later ratification.

ChatGPT's consolidation v0.2 is an accurate and fair summary. It also correctly identified an inconsistency in Claude v2 about dates in digests; section 6 below corrects it. The date question itself has since been settled by evidence (section 7).

---

## 1. Timing - do it now, contract-first

The Powerball-specific code is still small. Literal 35 / 20 / 1144, the 1577-1587 holdout range and the two-barrel result shape sit almost entirely in:

- the E_1 maths module (`_common/e1_historical_appearance_frequency_v0_3.py`);
- the E_1 loader (`_common/e1_training_view_v0_1.py`);
- the standalone contract (`_common/e1_standalone_contract_v0_1.py`, target cap 1145..1577);
- the Powerball scraper;
- tests.

The coordinator is game-neutral apart from its file name. The scorer and walk-forward are not yet built, and E_2-E_6 are next. Each method written against a fixed two-barrel shape raises the later cost. So generalise now, together with the scorer/walk-forward work, and before E_2-E_6. Two narrow profiles remain the best route (consolidation Q1); a generic any-lottery engine is not wanted.

## 2. Approach - build and test the real Oz Lotto profile, stop before science

A synthetic second profile proves the code is portable, but it cannot confirm the assumptions about **real** Oz Lotto data (layout, era start, cadence, supplementary presentation). So:

1. **Before any scraping:**
   - ratify the `OZLOTTO` profile;
   - fix its scope: current era from draw 1474 (17 May 2022), winning numbers only;
   - fix its holdout **rule** (section 8).
2. **Build `Run_Scraper.bat <game>` and an Oz Lotto scraper.** Use the same venv checks as the other wrappers. Snapshots are dated, never overwritten, and print their SHA-256. Each scrape produces two files:
   - a winning-numbers CSV, the only file a loader accepts;
   - a separate raw provenance CSV that keeps the supplementaries.
   
   Choosing which snapshot to train on stays a separate, deliberate step. Also fix the existing Powerball scraper, which writes its CSVs beside itself in `src/`.
3. **Structural validation only, through a bounded audit interface** (section 8):
   - 7 distinct labels in 1..47 per draw;
   - consecutive draw numbers from the era start;
   - era start confirmed;
   - every date equal to the derived weekly date (section 7);
   - raw and winning files kept separate;
   - hashes recorded.
   
   No frequencies, scoring or forecasts.
4. **Profile-driven loader, scorer, result schema and target caps,** with an exact Powerball regression gate (section 4).
5. **Keep a synthetic second profile in the tests** (one barrel, 7 of 47, no Powerball barrel). It is cheap and catches hard-coded literals.
6. **STOP POINT:** no Oz Lotto method run, real or development, until its own separately reviewed and owner-authorised gate.

## 3. Shape - two narrow game profiles

- **Profiles as a small, versioned Python module of frozen constants** (for example `_common/game_profiles_v1.py`), not a configuration file. They are reviewed and hashed like code, there is nothing to parse, nothing editable by users, and the profile version string is bound into every run's identity.
- **Each profile holds:**
  - `game_id`;
  - era;
  - era-start date;
  - era first draw number;
  - a list of barrels `{barrel_id, lowest label, highest label, count selected}`;
  - development target cap;
  - holdout rule and record;
  - nominal draw time and timezone;
  - closing time in UTC.
  
  `--game` selects an approved profile. Barrel counts and label ranges are never accepted as command-line values.
- **Each game's registry lists every E-number** (R2-C13) as `SUPPORTED`, `UNSUPPORTED_FOR_GAME` (with a structural reason) or `FORMULA_OPEN`.
  - Methods that rank each barrel independently run on Oz Lotto's single `MAIN` barrel.
  - Methods that use both barrels together are UNSUPPORTED for Oz Lotto.
  - A second barrel is never invented, and no method is excluded because standard theory predicts no signal.
- **Results and scoring are per actual barrel.** Oz Lotto has one TOP seven, one WORST seven and one MAIN mean mid-rank. Its Powerball channel is **ABSENT** (not zero, not a disguised N/A).
- **Missed hard-coding (consolidation Q4).** `_common/e1_standalone_contract_v0_1.py` is E_1-specific: it fixes `e1-` run IDs, method `E_1`, the variant and the schema names. Make it method-generic in the same work, **before E_2**, or every method will copy it. Also clear:
  - the loader's Powerball-only filename pattern (`SAFE_NAME`) and its `FIRST_DATE` cadence check;
  - the 1577 cap, which appears in both the loader and `begin()`;
  - the barrel sizes inside the E_1 maths;
  - the git-ignore paths.
  
  Keep the tests that pin hashes; they are the regression baseline.

## 4. Compatibility - Powerball must not change

- **Do not change `TIE_SHA256_V1` or any Powerball identity.** Game identity enters through the training-view digest, which is already field 2 of the tie tuple.
  - Powerball keeps `E1_REAL_U_TRAINING_VIEW_V1`.
  - Every new game's view schema must name its game, era and profile version. Barrel ID `MAIN` is then safely reused across games.
  - No new tie version is needed.
- **Results:** adding `game_id` to the result wrapper needs a new result-schema version. Old results stay valid under the v0.1 schemas.
- **Keep the accepted E_1 maths module as it is.** The parameterised code is a new module version.
- **Regression gate** - under profile-driven code, these must reproduce exactly:
  - the Powerball synthetic goldens: training view `df21871f...`, tie digest for label 3 `7ce5ab1b...`, forecast `7b43d659...`;
  - the real 1577 forecast: training view `d47fbbd6...4339`, same ranking, TOP [9,17,7,11,18,30,12] PB 2, WORST [31,13,8,29,26,33,35] PB 12.
  
  A new result wrapper's hash may differ only through the new schema version, and only with an explicit label.
- **Legacy rule:** v0.1-schema records that lack `game_id` are defined once, by a versioned compatibility rule, as meaning `POWERBALL`. New schemas **require** `game_id`. Existing Powerball CSVs are left unmodified, because their hashes must stay valid.

## 5. Draw identity (owner convention, endorsed)

| Field | Meaning | Example |
|---|---|---|
| `game_id` | The lottery | `POWERBALL`, `OZLOTTO` |
| `draw_number` | The operator's draw number | `1577` |
| `draw_key` | Human-readable form for display and filenames | `POWERBALL_1577` |

- **The authoritative identity is the pair (`game_id`, `draw_number`),** carried as two structured fields in every record, manifest, status file, log and score. The same draw number in two games is legitimate.
- **`game_id` matches `[A-Z][A-Z0-9]*` (no underscore),** so `draw_key` splits unambiguously at its last underscore.
- **The era is a property of a draw, not part of its key** (Oz Lotto numbering continued through 2022). Loaders refuse draws outside the selected era.
- **Scoring** looks up outcomes by the pair in that game's own snapshot and refuses any mismatch. Run folders carry a game segment; random run IDs are unchanged.

## 6. Time axis and digests (corrects Claude v2 section 6)

- **Within each game the time axis and sequence key is `draw_number`.** Intervals, lags, recurrence and walk-forward steps are counted in draws.
- **Correction:** v2 said dates "never enter keys, digests or ordering". That was too strong. The correct rule:
  - Dates never enter **keys** or the **sequence order**.
  - Dates never enter the **U-view digest**, so E_1 and every Powerball identity are unchanged.
  - A view that consumes dates includes what it consumes in **that view's** digest, and through it the method's seed and tie identity. This follows R2's permitted-view rule.
- **With the derived-date rule in section 7, this becomes trivial.** The derived date is a pure function of `draw_number` and the profile's constants. A date-using view therefore only needs its schema to name the profile version: no separate date field enters the digest, and no extra date-mutation machinery is needed beyond the normal suffix-poison test.
- **Do not drop dates.** Ratified R1 includes two date-using methods, and removing dates would silently disable them, contrary to the no-exclusion rule:
  - **E_14** Calendar-Phase Conditional Patterns;
  - **E_54** External-Date Covariate Synchrony (view `U+X`; R1 also lists "other game outputs" as a covariate).

## 7. Draw dates - findings and rule

**Findings (24 Oct, draw numbers and dates only; no ball values read or collected):**

- **Powerball** (repository CSVs `australian_powerball_history_20261021.csv` and `australian_powerball_draw_order_20261021.csv`):
  - 444 draws, 1144..1587, from 2018-04-19 to 2026-10-15;
  - **every step exactly +7 days and +1 draw**, all on Thursdays;
  - both CSVs carry identical dates;
  - zero deviations.
- **Oz Lotto** (lottodraw.com.au yearly archives 2022-2026; a secondary site, with pairs extracted by an automated page reader, and no winning or supplementary numbers collected):
  - current era 1474 (Tue 2022-05-17) to 1703 (Tue 2026-10-06): 230 draws over exactly 229 weeks;
  - **every step +7 days and +1 draw**, all on Tuesdays, including the Christmas/New Year weeks;
  - anchors 1474, 1506/1507, 1558/1559, 1611/1612, 1663/1664, 1678 and 1703 match the derived date exactly;
  - the archive stopped at 1703; by the same rule 1704 = 13 Oct and 1705 = 20 Oct 2026.
- **Draw 1474 = 17 May 2022** is corroborated by this full sequence and by other independent results sites. It is still secondary evidence until confirmed from operator data (consolidation Q5).

**Rule (owner direction 24 Oct; supersedes all earlier date proposals, including Claude's draw-calendar idea and the v2 "actual date + nominal time" scheme):**

- **Derived date** = profile era-start date + 7 x (`draw_number` - era first draw), with:
  - `POWERBALL`: 2018-04-19 at draw 1144;
  - `OZLOTTO`: 2022-05-17 at draw 1474.
  
  The target draw's date is the last training date + 7. There is **no user input**, no draw-calendar file, and no loader ever parses row N, in historical and FINAL modes alike.
- **Verified, not assumed.** Structural validation of every snapshot checks that each scraped date equals the derived date: Powerball passes 444/444 now, and Oz Lotto is checked at its first scrape from operator data. On any deviation the validator flags it, and date-using methods (E_14, E_54 and later variants) STOP for that game pending an owner decision. Nothing else is affected.
- **Scraped dates are kept as provenance only.** They are never keys, digests or model inputs.
- **E_54 "known before the draw":** judged against the derived date plus the profile's nominal draw time and timezone, labelled nominal. The exact availability semantics stay OPEN until E_54's own data contract is written.

## 8. Oz Lotto holdout and pre-seal inspection (consolidation Q3)

- **Fix the holdout RULE before the first scrape.** The last draw number is not known in advance, so state a rule, not a range. Example: "the holdout is the 10 highest draw numbers present in the first accepted winning-numbers snapshot". The draw numbers are selected without reference to any values. After the scrape, record the resulting draw numbers and the snapshot hash in an Oz Lotto holdout record. Never reuse Powerball's 1578-1587.
- **Bounded audit interface.** Structural validation may read holdout rows only through a bounded audit function. It returns pass/fail, counts, and error lists by draw number and field name, **never values**. Nothing prints or reports holdout numbers.
- The raw provenance CSV (which holds supplementaries and holdout outcomes) gets the same treatment.
- Opening the CSVs by hand cannot be prevented by code; that is the owner's discipline, as for Powerball now.
- About 230 current-era draws exist (to 1703), against Powerball's 444. A 10-draw holdout takes proportionally more. That is context, never a reason to exclude.

## 9. Oz Lotto scope

- **Current format:** 7 winning numbers from 47, plus 3 supplementaries, since 17 May 2022 (previously 7 of 45 with 2 supplementaries). Profiles refuse cross-era data. If either game changes its rules in future, the pipeline stops rather than mixing eras.
- **Supplementaries:** excluded from all model views, predictions and scoring (owner scope), but archived raw. They are 3 of the 10 balls of each physical draw. Within-draw order and physical-process hypotheses (for example E_23-E_32 and E_57-E_62) lose them under this scope, and archiving keeps a governed variant possible later.

## 10. Safety and operations

- **Single global orphan marker** (already global); choosing another game never bypasses it.
- **No hard one-game lock.** Each coordinator kills only its own captured, verified processes. The real risk is CPU and memory overload, so an advisory warning plus the owner's operating rule is enough.
- **Keep the coordinator's file name;** rename it with v0.7 if wanted.
- **Coordinated method runs still need:**
  - `exit_receipt.json`;
  - the run-folder / run-ID handshake;
  - `--game` checked against the method's support status for that game.
- **Task Manager (owner de-scope accepted):** keep `python.exe` / `cmd.exe`. Put game, method, `draw_key` and run ID in arguments and existing logs. Display labels never prove ownership.

## 11. Other points

- **Per-game chance figures,** as context only:
  - Oz Lotto: expected TOP matches 7 x 7 / 47 = about 1.04; chance mean mid-rank 24.0; Powerball channel ABSENT.
  - Powerball: 1.4 TOP matches; Powerball hit 1/20; mid-ranks 18.0 and 10.5.
- **No pooling of scores across games** unless that is decided in advance.
- **Per-game freeze and publication timing,** with closing time in UTC.
- **Cross-game hypotheses** (for example a known Tuesday Oz Lotto result as an input for the Thursday Powerball draw, under E_54) are out of scope now. Do not design them out of the view API.
- **E_63 (Chebyshev / minimax):** a governed new R1 entry or an E_37 variant; the owner decides. It is independent of this work.

## 12. Who decides what (consolidation Q7)

**Owner ratifies:**

- the scope extension to Oz Lotto (a charter change);
- the Oz Lotto era, supplementary policy and holdout rule;
- the draw-identity convention;
- the derived, verified weekly-date rule and the date-view digest rule;
- the Proposal, R2, R3 and Architecture amendments.

**ChatGPT decides as routine (DECIDED):**

- profile module format;
- file and folder names;
- the `game_id` pattern;
- the advisory concurrency warning;
- arguments and log lines;
- scraper internals.

**Minimal stop/go packages:**

1. **DOCS ONLY:** the amendments in section 13, the Oz Lotto holdout rule and the profile specification. One Claude review, then owner ratification.
2. **CODE:**
   - the profile module;
   - the method-generic contract and consumer;
   - `Run_Scraper.bat` and the Oz Lotto scraper;
   - the bounded structural validator, including the derived-date check;
   - the exact Powerball regression.
   
   One Claude review, then Windows synthetic tests.
3. **Owner's first Oz Lotto scrape and structural validation, then STOP.**

After that, the paused scorer/walk-forward and E_2-E_6 resume on the new contracts.

## 13. Documents to update

| Document | Change needed | How |
|---|---|---|
| Proposal v0.3 (charter) | **Yes. Adding Oz Lotto is a scope change.** A second game, per-game datasets, eras and holdouts, the supplementaries policy, and the data, holdout and no-pooling rules applied per game. | Proposal v0.4 or a referenced scope addendum; ratify **first**. |
| R1 v0.4 | No change. The hypotheses do not depend on the game; per-game applicability lives in each game's registry. E_63 is separate. | None now. |
| R2 v0.3 + Erratum v0.2 | Yes: I-05/I-06 per game plus the Oz Lotto holdout record; per-game U/X views; the date-view digest rule and the derived, verified weekly-date rule; per-game R2-C13 registry; supplementaries excluded. | R2 Erratum v0.3 (ERR-R2-05), following R2's existing practice and recorded in the ratification register, or R2 v0.4. Owner's call; Claude leans erratum. |
| R3 v0.2 | Yes: per-barrel scoring; per-game chance figures from the profile; Powerball channel ABSENT for Oz Lotto; per-game reporting, with no pooling unless decided in advance; per-game freeze and publication timing (closing time in UTC). | R3 v0.3 or an erratum, handled the same way as R2. |
| Architecture v0.5 | Yes, the main one: profiles (code module); the (`game_id`, `draw_number`) identity; view and digest rules, including date-using views; derived dates and their verification; snapshots and `Run_Scraper.bat`; the barrel-aware scorer; the per-game registry and section 6.1 discovery; `--game`; the global marker unchanged; exit receipt and run-ID handshake; Task Manager note. | Self-contained Architecture v0.6. |
| POC Task Spec v0.2 | Little or nothing; it is P0-P2 and Powerball-specific by design. | Leave it; write a **new** multi-game/P3 infrastructure task spec. |
| TIE_SHA256_V1 contract note | One sentence: it applies to every game, with game identity carried through the view digest. | Minor revision. |
| E_1 design documents | Revise when E_1 is parameterised, keeping v0.3 as history. | With package 2. |
| New | Oz Lotto holdout record (rule, resulting draw numbers, snapshot hash); `doc/RATIFICATION_REGISTER.md` (also fixes the stale DRAFT headers on Proposal, R1, R2 and R3). | In package 1. |
| Handovers | ChatGPT's handback and Claude's handover. | Refresh at the end. |

**Order:** Proposal, then R2/R3, then Architecture v0.6, then the task spec, then code. All the documents go in **one** review package (package 1). They touch identity, holdout, synthetic/real separation and N-1 rules, which always get independent review.

## Sources

- Oz Lotto - Wikipedia: https://en.wikipedia.org/wiki/Oz_Lotto
- Lotterywest, 16 May 2022 (changes from Tuesday 17 May): https://lotterywest.wa.gov.au/lotterywest/media-centre/oz-lotto-10-million-jackpot-could-ease-the-rainy-day-blues
- Lotterywest, 7 April 2022 announcement: https://lotterywest.wa.gov.au/lotterywest/media-centre/bigger-prizes-and-more-winners-with-oz-lotto-game-change
- lottodraw.com.au Oz Lotto archive: https://lottodraw.com.au/oz-lotto/archive (yearly pages 2022-2026), and draw 1474: https://www.lottodraw.com.au/oz-lotto/draw-1474
- powerball.us.org draw 1474 (17 May 2022): https://powerball.us.org/news/oz-lotto-draw-1474-results-17-may-2022-10-000-000-jackpot-6083
- Mirage News draw 1474: https://www.miragenews.com/oz-lotto-results-winning-numbers-in-draw-1474-783592/

*End of review v3.*
