# Cold read of the draft of design v0.1r1 (3 November 2026)

A fresh helper (a separate agent with no knowledge of the Claude chat) was given the repository at `3a9f6ac` and the draft `Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r1_DRAFT_before_cold_read.md`, and asked to explain the design back, check every code citation, and list conflicts with the authorities, gaps, unexplained terms, numbers and dates, the five things the independent reviewer would most likely send back, and a verdict. Its report follows, unchanged except for ASCII normalisation. Claude verified its critical claims (D1, C1, D2, D3, C2, C3, D20) against the code before revising; all held. The revised v0.1r1 applies or answers every finding; `design_v0_1r1_draft_to_final.diff` shows the changes.

Base checked: the clone's `HEAD` is `3a9f6ac` (matches the design's stated base). The clone is shallow (17 commits), so `3fce327` could not be checked directly; register v0.23 line 1303 records it as the PERF-1 install. Working tree clean.

## A. The design in ten plain-English lines

1. Today every reader of the results file insists the file is still the original (version 1); the first job is a shared module that accepts the updater's later versions by checking the ledger chain and proving each older version's bytes are a prefix of the current file, so old pins stay valid and new runs can pin new versions.
2. A pinned run may forecast any draw up to the pinned version's last draw plus one; a holdout or later target additionally needs the game's opening record.
3. Before the holdout is opened, the owner freezes a study manifest (cohort, ten targets, measures, N1 seed, code digests, installed packages) and writes `HOLDOUT_OPENED_<GAME>.json`; only then is the updater run for the first time, which adds the holdout and every later draw in one version.
4. Mode H (option A) is one batch of 40 variants x 10 holdout targets per game, each forecast from the draws before its target, all frozen create-only, then scored once by the WF-1B scorer; it is described as a precommitted holdout evaluation, not pre-draw forecasting; option B (one reveal at a time) is kept for the reviewer; option C is withdrawn.
5. No scorer may read a holdout outcome until the whole Mode H batch is complete; for later draws, not until the forecast ledger holds that draw's freeze line (the freeze-before-outcome function, fixed paths, no caller inputs).
6. Install records (one per package from package A on, plus a one-off baseline record for the 40 variants dated 31 October 2026) decide whether a catch-up forecast is CATCH-UP (variant installed before the draw's derived date) or development evidence.
7. The weekly session per game is one offline command after the owner's updater: a status block, then every outstanding draw strictly in order (score an existing forecast, or make-freeze-score a catch-up one), then freeze the next draw's forecast before its deadline (00:00 local on draw day).
8. Timing proof is a local digest-chained forecast ledger per game; a GitHub push or emailed digest is an optional witness; R3's push clauses are superseded for this project on ratification.
9. Scores go to an append-only score ledger; league tables are built from it with PROSPECTIVE, CATCH-UP, development and Mode H kept apart; nothing is scored twice; the "developed" record is R3's FINAL opening.
10. Two HIGH packages (A: reader, opening, install records, Mode H; B: weekly session and checklist), planning target 13-15 November, first prospective forecasts Oz Lotto 1709 (17 Nov) and Powerball 1592 (19 Nov).

The design is understandable. Its weak points are not clarity but premises checked against the code (B and C below).

## B. Code citations checked

| # | Design section / citation | Verdict | What the lines hold |
|---|---|---|---|
| B1 | S1 C: `walk_forward.py` line 45 ("the driver runs unordered, date-free views") | IMPRECISE | Line 45 is the constant `VIEW = 'UNORDERED_SET'`; the enforcement and the quoted phrase are at `cohort()` lines 143-144. |
| B2 | S1 C: `contract_adapters/e_001.py` line 27 ("E_1 alone carries the target in its forecast record as a label") | WRONG (claim) | Line 27 does pass `task.target_draw_number` to E_1, but not as a label only: `E_001/multigame_e1.py` line 50 sorts ties by `_digest(digest, target, ...)`, and line 23 hashes `str(target)` into the tie key. Moreover every method's tie-break uses the target: `_common/contract_records.py` lines 405-409 (`tie_identity_for` includes `target_draw_number`), and every non-legacy permitted-view digest includes `'target': self.target` (`game_draws_reader.py` line 125). |
| B3 | S2.1: `game_draws_reader.py` lines 241-254 | CORRECT | 241-244 `ledger_version != 1` refused; 249-254 single INIT row with `last_draw == holdout_first - 1`. |
| B4 | S2.1: `game_draws_reader.py` line 237; lines 234-236; `game_profiles.py` lines 72-76 | CORRECT | 237 target gate; 234-236 the E_1 1577 exception; 72-76 `historical_development_target_allowed`. |
| B5 | S2.1: `walk_forward.py` lines 100-109 | IMPRECISE | `ledger_pin` is lines 98-109; the single-INIT-row checks are 104-108. |
| B6 | S2.1: `walk_forward.py` lines 184-195 | CORRECT | 184-185 refuse `last >= holdout_first`; 189 pin; 195 `'ledger_version': 1`. |
| B7 | S2.1: `outcome_reader.py` lines 49-51 and 55-80 | CORRECT | 49-51 the target range; 64-69 the single INIT row (the function `_verify_source` runs to 83; the INIT-record check is 78-82). |
| B8 | S2.1 and S4.4: `report.py` lines 125-126 | CORRECT | `last > p.holdout_first - 1` refused. |
| B9 | S2.1: `results_master_v0_1.py` lines 185-189 (`to_csv_bytes`) | CORRECT | Header, one CRLF line per draw. |
| B10 | S2.1: lines 640-647 (append new draws, rewrite, ledger row) | CORRECT | 640 merge, 642 `replace_atomically`, 643-647 UPDATE row and append. |
| B11 | S2.1: lines 633-636 ("UPDATE, or NO_CHANGE ... new version number") | IMPRECISE | 633-637 is the NO_CHANGE branch only; the UPDATE row is 643-647; the version increment is line 629. |
| B12 | S2.1: line 639 (backup), line 613 (grab) | CORRECT | `write_new(backup, master_bytes)` at 639; `write_new(grab_path, ...)` at 613. |
| B13 | S2.1: `cmd_init` uses `to_csv_bytes` | CORRECT | Line 446. |
| B14 | S2.1: `Run_Results_Updater.bat` lines 4 and 33 | CORRECT | Comment at 4; bare `update` at 33. |
| B15 | S2.2 rule 4: `_parse_prefix` lines 161-209 | CORRECT | 161 def to 209 return; reads `target - first_draw` rows only. |
| B16 | S2.2 rule 2: `load_verified_master` lines 298-300 | CORRECT | The "does not match the last ledger entry" check. |
| B17 | S3.2: `results_master_v0_1.py` lines 135-150 | CORRECT | `holdout_opened`: schema, game, 64-hex `study_manifest_sha256`, `opened_utc`, `owner_statement`. |
| B18 | S3.3: register v0.23 lines 1183, 1189, 1215 | CORRECT | `6a1bed9`, `0d98706`, `86d12ea`, all 31 October 2026. |
| B19 | S3.4: the updater's `--self-test` is offline | CORRECT | `self_test()` at 704 uses `FakeFetcher`. |
| B20 | S4.1: `Method_Contract_Runner.py` lines 89-90 | CORRECT | Fixed `run_root` under `results/real/development/contract_runs/`. |
| B21 | S4.1: `contract_vocab.py` lines 69-100 | CORRECT | 69-73 modes and `RESERVED_MODES`; 75-79 product kinds and tiers (`HOLDOUT_MODE_H`, `PROSPECTIVE` exist; `HOLDOUT_FORECAST` does not); 83-100 `producible` refuses reserved rows. |
| B22 | S4.1: `contract_runner.py` lines 118-121 | CORRECT | 118-122: REAL_DEVELOPMENT must read the project root; everything else goes to `check_synthetic_workspace`. |
| B23 | S4.4: `n1_generator.py` lines 48-50 | CORRECT | `stream_key` keyed by domain, policy, root, game, replicate, target. |
| B24 | S6: `.results_master.lock` lines 653-672; line 617 | CORRECT | `Lock` class 653-672; the no-overlap refusal at 616-617. |

Not cited but load-bearing (see D2): `contract_records.py` 335-336 and 354, `contract_forecast.py` 275-277, `contract_receipts.py` 68, `contract_dispatch.py` 96, `Method_Contract_Runner.py` 50, `E_001/multigame_e1.py` 30-34, `contract_task.py` 45-51.

## C. Conflicts with the authorities

- **C1. S1 option C, "Checked at the base: no released method uses its target's draw number in its calculation".** False at the base. E_1's tie key hashes the target (`multigame_e1.py` 23, 50); the contract's `TIE_SHA256_V1` identity includes `target_draw_number` for every method (`contract_records.py` 405-409); every non-legacy view digest includes the target (`game_draws_reader.py` 125). Under C the ten forecasts from one prefix would have identical scores but could differ in tie order, hence in TOP/WORST where ties straddle the boundary. The conclusion (C is a fixed-origin test of one forecast, not of retraining) survives; the stated check and both citations do not. The same sentence is in Response 3 S2(c), Response 4 S3.2 and roadmap 10c line 149, so the error is inherited and now on the owner's roadmap. Reviewer's Response 2 S7(c) asked exactly this question.
- **C2. S4.1 and S5.4 vocabulary vs E2R-1 9.1/9.2 and R3 17.3.9.** E2R-1 9.1 marks every field "Values (closed)"; E2R-R41's reserved table (E2R-1 lines 500-503) already fixes `REAL_HOLDOUT -> WF_FORECAST / HOLDOUT_MODE_H` and `FINAL_NEXT_DRAW -> WF_FORECAST / PROSPECTIVE`. The design invents `HOLDOUT_FORECAST`, `PROSPECTIVE_FORECAST`, `CATCH_UP_FORECAST`, a new run mode `CATCH_UP` and a new tier `CATCH_UP` (also absent from R3 17.3.9's tier list), without saying why it departs from the reserved rows, and flags only one row ("an E2R-1 vocabulary addition") as an amendment. E2R-R44 (DECIDED: "Every code path that would act on them stays refused. Mode H and FINAL stay shut") is being amended by S4.1 and S5.4 and is not named.
- **C3. S4.4 family `mode: "H"` vs E2R-R39 (DECIDED: a track's mode is `WF` or `IS`), R3 17.3.5 and 17.3.5A (two modes, each printed with its plain meaning; `TRACK_MODES` in `contract_vocab.py` line 113).** Mode H forecasts are walk-forward records scored at the `HOLDOUT_MODE_H` tier; a third mode value conflicts with the ratified two-mode vocabulary and the display rule.
- **C4. S5.5 "without one the label stays PROSPECTIVE" vs R3 10.2 (a saved local prediction "must not be mislabelled 'verified prospective' unless the required timing evidence exists"), R3 10.5 (`PUBLISHED_BEFORE_DRAW` / `TIMELINESS_UNVERIFIED`), R3 17.3.9 ("PROSPECTIVE: forecasts frozen and published before their draws"), R3 1.5, R3 6.1 `PROSPECTIVE_ALL` ("archived-before-draw"), and E2R-R40C ("Publications without independent publication evidence are labelled unverified and counted").** OFF-1 (register line 1329) makes the witness optional; it does not say an unwitnessed forecast carries the bare PROSPECTIVE label. Appendix B item 5 calls the S5.5 supersession list "complete"; it omits all of the above and R3 10.2's post-diagram paragraph.
- **C5. S5.4 bullet 2 (run mode `REAL_DEVELOPMENT`, tier `DEVELOPMENT_WF_EXPLORATORY`, for post-holdout targets) vs R3 6 ("Development caps remain 1576/1693"), E2R-R52 ("hard-coded target ceilings (now the profile's `historical_development_target_allowed`)") and `game_profiles.py` line 73 ("ONLY retrospective development, never an ongoing FINAL ceiling").** MH-1 ratifies the *label* "development evidence"; the design's *mechanism* reuses the REAL_DEVELOPMENT run mode above the development cap, which means loosening the one code guard that separates development from holdout for every REAL_DEVELOPMENT run. The design does not say how the guard changes or that E2R-R52 and R3 6's cap are amended.
- **C6. S5.6 "This is R3 7.6's and 11.5's 'outcome ledger' (finding A11)".** R3 11.5 item 5 `OutcomeRecord` holds the verified actual draw; the design's score ledger holds scores, which is item 6 `EvaluationRecord`. A11 is answered only by implication (the outcome record is the master row at (version, SHA)); the design should say so instead of renaming the score ledger.
- **C7. S3.4 step 1 ("Packages A and B installed and verified") vs S7 ("two code packages, so Mode H is never held up by the weekly work") and direction v0.2r1 S10 (reader, then open and first update, then batch, then scoring).** If B must precede Approval 1, Mode H is held up by B.
- **C8. S4.4/S5.4 flag names `HOLDOUT_EXPOSED_HX1` and `HOLDOUT_EXPOSED_HX2` vs HX-2 (register line 1313: 1587 and 1588 "carry the same exposure flag as Powerball 1585 and 1586 in Mode H").** Two names where the decision says one flag. Minor.
- **C9. S5.1 `Run_Weekly_Session.bat`, a wrapper that itself runs contract method code, vs H-1 5.4 Option F ("the single launch interface ... No second production launcher").** The walk-forward driver runs under `Run_Experiment.bat`; the design should say the weekly command does too, or state the exception.
- **C10. Direction v0.2r1 S5 step 5 and S9 (backup `source_data/` and `results/` after every session and before every install, with one restore test; agreed 2 Nov) are absent from S5.1 and S6**, although Appendix A says they land in "6 checklist (package B)".

## D. Gaps

- **D1 (critical). E_1 revision 2 cannot take part in Mode H, CATCH-UP or PROSPECTIVE as the code stands.** `E_001/multigame_e1.py` line 30 refuses any `data_kind` other than `SYNTHETIC_CONTRACT_TEST` / `REAL_DEVELOPMENT` (the adapter passes `data_kind=task.run_mode`, `e_001.py` line 27), and line 33 refuses any target not in `historical_development_target_allowed`. So every E_1 Mode H run would end `RUNTIME_FAILURE METHOD_FAILED`. Fixing it is a code change to a released method, i.e. E_1 revision 3 (E2R-R14A; R3 6.3) with its own code and release packages (E2R-R58). Consequences the design must state: the Mode H cohort (40 or 39), the baseline install record (E_1 r3's install date is not 31 October, so its Oz Lotto 1707 and Powerball 1590 forecasts are development evidence, not CATCH-UP, under S3.3's rule), the study manifest, and the S7 schedule. Fix: add E_1 r3 (same formula; admits the new modes and targets) before or inside package A, and recompute the labels in S0 and S7.
- **D2 (critical). S2.1's inventory of version-1 pins and target ceilings is incomplete**, so "runs each (variant, target) exactly as today" (S4.1) cannot hold. Missing: `contract_records.validate_run_request` lines 335-336 (target ceiling, E2R-R52; reached first through `dispatch_gate`, `contract_dispatch.py` 96, and `reader_pin`) and line 354 (`ledger_version` 1..1); `contract_forecast._validate_header` 275-277 (every forecast and diagnostic record with a holdout target is invalid, so no Mode H record is consumable); `contract_receipts._common_receipt` line 68 (`ledger_version` 1..1); `Method_Contract_Runner.py` line 50 (`'ledger_version': 1` hard-coded in the CLI request); `outcome_reader.py` 120-121 (second guard); `multigame_standalone_contract.py` 43 and 120, `multigame_worker_launch_handshake.py` 27, `coordinator_private/multigame_launch_spec.py` 63 (coordinated path; say they stay as they are). Fix: list each, state its new rule and its test.
- **D3. The permitted-view digest depends on the run mode.** `contract_task.view_data_kind` (lines 45-46) maps `REAL_DEVELOPMENT` to `REAL_HISTORICAL_DEVELOPMENT` and every other mode to its own name, and the digest feeds `TIE_SHA256_V1`. A REAL_HOLDOUT, CATCH_UP or FINAL_NEXT_DRAW run therefore has a different view digest, and possibly a different tie order, from a REAL_DEVELOPMENT run on the same prefix. S2.2 rule 4 ("View schemas and digests are unchanged") is true only for existing modes. Fix: say whether all real modes share one `data_kind` (a change to `view_data_kind`) or accept and state the mode-dependence (direction S3's "same arithmetic for all" is then not literal).
- **D4. Loop order in S5.3 contradicts S4.3/S5.5.** S5.3 is variant-outer ("For each active variant ... for each target N: ... run one contract run, freeze it, then score it"); but the outcome for N is released only when the ledger line for N exists, which needs every active variant frozen (S5.5). Fix: state target-outer: for each outstanding N, run and freeze every variant, append the line, then score every variant, then move on.
- **D5. The deadline and a set that straddles it.** If the 40 FINAL_NEXT_DRAW runs span 00:00, some freeze receipts predate the deadline and the ledger line does not. Fix: the label is decided per target by the line's freeze time, all-or-nothing; say what the early runs become, and whether the command refuses to start a set it cannot finish before the deadline.
- **D6. S4.3 "every (variant, target) ... with a terminal, consumable record (the batch COMPLETE)".** A `RUNTIME_FAILURE` terminal record is terminal but not consumable; the driver's COMPLETE is "every pair DONE in a CONTINUE class" (`walk_forward.py` 56-59, 330-370). As worded, one failed run (E_1, D1) blocks scoring for ever. Fix the wording.
- **D7. S5.3 "except the draws that variant already has Mode H records for".** Undefined when the Mode H record is a failure. Fix: any CONTINUE-class Mode H terminal record counts; the weekly session never revisits a Mode H target.
- **D8. New roots and Git.** `.gitignore` ignores only `results/real/development/contract_runs/`, `.../attempts.jsonl` and `.../scores/`; `results/real/holdout/contract_runs/`, `results/real/weekly/contract_runs/`, their `attempts.jsonl` and score folders would be untracked-but-not-ignored (800+ run folders). `load_plan` also requires `wf-<32 hex>` IDs and the development root (`walk_forward.py` 66-70, 208-214), which the fixed `MODE_H_BATCH/plan.json` path does not satisfy. Fix: name the `.gitignore` lines as package members (as WF-1B did) and say how `roots()` becomes mode-dependent.
- **D9. Exposure after Approval 2.** The six `source_data` records are tracked by Git. After the first update the masters hold the holdout and every later outcome, and when the owner pushes, every clone (the Claude web chat's, the reviewer's, Claude Code's) contains them. The design says nothing about this, nor whether grabs, backups, `HOLDOUT_OPENED_*` and `DEVELOPED_*` are tracked. Fix: state it; decide what is pushed; and add the documents Q7 would amend (rulebook rules 4-5, H-1 5.1, H-2, the exposure record) to S8.
- **D10. `master_versions.py` and `LEDGER_COLUMNS`.** "The header equals the updater's `LEDGER_COLUMNS` exactly" - imported from `src/results_master_v0_1.py` (the owner's tool, outside `_common`, under the static import firewall) or a copied constant with an equality test? Say which.
- **D11. Search-log row types** for the study manifest, the opening, the Mode H batch and score, the after-draw note and the full report are not named (R3 7.4: rows of their own types, "defined when the tools that write them are specified").
- **D12. S3.1 "the SHA-256 of every file under `src/` that the batch and the scorer import"** is not a deterministic set; S4.1's R3-T50 equality check is untestable until it is (for example every `.py` under `_common`, `E_*`, `contract_adapters`, `evaluation`, plus the registries and seed records).
- **D13. S5.4 invariant "exactly one whenever the next target is still before its deadline"** is false of the stored state before the week's first session. Reword as a postcondition of a completed session.
- **D14. S6 checklist** omits backups and the restore test (C10), the orphaned grab file of a refused or interrupted run (H-1 12.8 A7 names "grabs from refused runs"), and says "every tool refuses with 'does not match the last ledger entry'" although that is the updater's message only (line 299).
- **D15. S4.2 "never retried silently".** Today a pair not proven DONE is run again on the next `run` (`walk_forward.py` 264-271, 387-391). Say which attempt is the Mode H forecast after a STOP (the first CONTINUE-class attempt bound to the batch) and that all attempts precede any outcome read.
- **D16. S4.4 flags "in every per-target record".** `METHOD_FORECAST_V1` is a closed schema (E2R-R13); say the flag lives in score and ledger records and the report, not in the frozen forecast.
- **D17. S2.2 rule 3 "The E_1 1577 exception is unchanged" vs R3 6 ("the narrow E_1 draw-1577 regression is forecast-only ... never Mode H").** Say that the Mode H E_1 forecast for 1577 is a separate contract record that is scored, and the legacy forecast-only record stays unscored.
- **D18. S3.3 install record.** Say whether it stores commit IDs (E2R-R54's "Git history is not relied on"), which date counts for the current cohort (release day 31 October, not the earlier code installs of 29-30 October), and what happens when a variant has two records.
- **D19. Switches.** `ENABLE_CONTRACT_REAL_DEVELOPMENT` gates `REAL_DEVELOPMENT` only (`contract_runner.py` 114-116). Say whether the new real modes get a code-level switch (H-1 5.4 lists the switches) or why not.
- **D20. S4.4 "reused unchanged in ... layout".** `report_writer.py` line 422 prints a fixed sentence that no holdout draw was used; the WF display texts (R3 17.3.5A) and the family `mode` need Mode H wording.
- **D21. S3.4 step 3's `--self-test`** has no acceptance rule (who reads it, STOP on any failure) in the approvals list.
- **D22. Q2 and Q3 are never stated as questions** (direction S11 lists Q1 and Q4-Q9 only). Add a Q1-Q9 table with each question's text and where it is answered.
- **D23. R3 6.2 asks the study to "compare" the combined master with a separate release store.** S3.5 is one sentence; put the comparison (risks of outcomes being in the file the reader opens; mitigations: prefix parse, T-05, B1, create-only records) in one place, since the reviewer's Response 2 S4 leaned to B "where safely feasible".
- **D24. The owner's pin per session.** Say explicitly that every run of a session pins the current last ledger row, and that the scorer uses the forecast's own pin through the prefix check.

## E. Unexplained or inconsistent terms

- **E1.** "the three takeover notes (1 November)" (work-item card): a reviewer chat message, not on disk (EX_123 cover note line 5 says "a chat message, not an EX file"); never summarised.
- **E2.** Q2, Q3, Q9 used without their question text (D22); "Q5 detail" vs "Q5" (mechanism decided, format open) is explained only in S3.3.
- **E3.** "development" in two senses: the pre-holdout development prefix (R3 6, E2R-R52) and the post-holdout "development evidence" label of MH-1 (S5.4 bullet 2 gives the latter the former's run mode and tier).
- **E4.** "freeze": the study-plan/code freeze (S1), the forecast freeze receipt (`FORECAST_FREEZE_RECEIPT_V1`), and the ledger "freeze line" (S5.5) are three different things.
- **E5.** Three "ledgers": the updater's master ledger, the forecast ledger (S5.5) and the score ledger (S5.6), plus R3's "outcome ledger" (C6); one glossary line each would help.
- **E6.** "COMPLETE" (the driver's batch state) and "complete" (S4.3) side by side.
- **E7.** "MHUP-1", "MHUP-A", "MHUP-B": MHUP is never expanded; "R-4 oracles" (S2.2 Tests) is a tier name used without its meaning.
- **E8.** "version-2 reader / version-2 reading rules" means "accepts versions 2 and later", not "reads version 2"; define once.
- **E9.** "label" for the evidence label and for a ranking label ("carries the target ... as a label", S1).
- **E10.** `HOLDOUT_EXPOSED_HX1` / `HX2` vs the register's single "exposure flag" (C8).
- **E11.** "measured rate" (S4.1) for an owner-reported "about 80 minutes" (H-1 7.5).
- **E12.** "EX_124" in the S7 table is the reviewer's reply number asked for in EX_123; the design's own transmission is a Claude EX.

## F. Numbers and dates

Derived with `game_profiles.derived_date` (run from the code; no result file touched):

| Design statement | `derived_date` | Verdict |
|---|---|---|
| Oz Lotto 1709, Tuesday 17 November | 2026-11-17 Tuesday | correct |
| Powerball 1592, Thursday 19 November | 2026-11-19 Thursday | correct |
| Week of 9 November: Oz Lotto 1708, Powerball 1591 | 2026-11-10 Tue; 2026-11-12 Thu | correct |
| Oz Lotto 1704-1706 predate 31 October installs | 13, 20, 27 Oct 2026 | correct |
| Powerball 1587-1589 predate 31 October installs | 15, 22, 29 Oct 2026 | correct |
| Oz Lotto 1707 onward CATCH-UP (install 31 Oct before draw date) | 1707 = 3 Nov 2026 | correct |
| Powerball 1590 onward CATCH-UP | 1590 = 5 Nov 2026 | correct |
| Deadlines 00:00 Tue 17 Nov / 00:00 Thu 19 Nov (S7) | consistent with S5.4 and the draw days | correct |
| "Oz Lotto from Wednesday to Monday night, Powerball from Friday to Wednesday night" | consistent with Tue/Thu draws and 00:00 draw-day deadlines | correct |
| Holdout 1577-1586 / 1694-1703 | profiles lines 83, 88 | correct |

Counts: 40 variants (H-1 5.3; register 1184 + E_1 r2) correct; 400 = 40 x 10 correct; 17,280 = 40 x 432 targets 1145-1576 and 8,760 = 40 x 219 targets 1475-1693 (register lines 1224-1225) correct; 471 tests (register 1303) correct; R = 10,000 correct.

Time statements: "17,280 runs in about 80 minutes" is owner-reported in H-1 7.5 ("about"), called "measured" in S4.1; "about two minutes per game" is marked estimated (note the Mode H prefixes are the longest, so the average rate understates); "about half a day" per recheck round and "the snapshot took four rounds" are unmarked estimates (the snapshot: candidates 1-4, EX_117 and EX_119 RECHECK, EX_121 PASS - four is fair); "adds at least a day" for a fresh pulse is an unmarked estimate. Dates of commits `c01717d` (2 Nov) and the three installs (31 Oct) are correct; `3fce327` not verifiable in the shallow clone, consistent with the register.

## G. What the independent reviewer would most likely send back

1. **E_1 r2 cannot run in any new mode or on any holdout target (D1), and the "checked at the base" claim behind withdrawing option C is wrong (C1)** - the reviewer asked exactly question (c) in Response 2 S7 and will look at E_1 first.
2. **The pin/ceiling inventory is incomplete (D2) and the vocabulary changes amend DECIDED rules without saying so (C2, C5, E2R-R41/R44/R52)** - "runs exactly as today" is not true until `validate_run_request`, `_validate_header` and the receipt validator are in the design.
3. **PROSPECTIVE without a witness contradicts R3 10.2/10.5, 17.3.9 and E2R-R40C, and the "complete" supersession list is not complete (C4)** - the reviewer wrote the "witness must verifiably receive the digest before the draw" wording and will check the label that follows from it.
4. **The weekly loop as written cannot satisfy its own freeze-before-outcome rule (D4), the deadline has no rule for a straddling set (D5), and the "exactly one open" invariant is overstated (D13)** - the reviewer's Response 2 S2(d.2) cautions precisely here.
5. **Mode-dependent view digests (D3), post-holdout targets under the REAL_DEVELOPMENT mode above the ratified development cap (C5), and a third track mode "H" (C3)** - each quietly changes a ratified identity or vocabulary.

## H. Verdict

**NOT READY** - a released method (E_1 revision 2) cannot produce any Mode H, CATCH-UP or PROSPECTIVE forecast as the code stands, the design's checked claim about target use is wrong at the base, and the list of code that pins version 1 or the development ceiling is incomplete, so the cohort, labels and schedule rest on unverified premises; the rest is fixable in one revision.

**Confirmation.** I opened no file under any `source_data`, `results` or `transitory_data` folder and read no data value. For transparency: `ls -la` of the repository root showed those folder names, and `git ls-files source_data` / `git ls-files results` printed tracked path names from the Git index (names only, no contents) to check what is pushed to GitHub (D8, D9); nothing inside those folders was opened. No draw outcome of Powerball 1577 or later or Oz Lotto 1694 or later was displayed, quoted or computed with; draw numbers and derived dates only. No web access; no `.bat`, experiment, coordinator, updater or report tool was run; only read-only `git` commands and one Python snippet importing `game_profiles`. No repository file was modified.

**For the main session (not from memory; all from the repository):** the inherited factual error about "no released method uses its target's draw number" is also in `exchange/OWNER_ROADMAP.md` item 10c (line 149) and in stock-take v0.7 Responses 3 and 4, so correcting the design alone leaves the roadmap wrong.

*End of the cold read.*
