# Focused recheck of design v0.1r1 against the cold read (3 November 2026)

The same fresh helper was given the revised design, the draft it had read, the diff and its own first report, and asked whether each finding was applied, whether the new code citations hold, and what the revision had newly introduced. Its report follows, unchanged except for ASCII normalisation ("section" for the section sign). Every item N1-N18 is applied in the final v0.1r1; the one imprecise line range (`roots()`, 66-70) is corrected.

Base: the clone is still `3a9f6ac`, working tree clean. All new line citations were checked against the files on disk.

## 1. Disposition of the cold-read findings

**B (code citations)**
- B1 APPLIED: section 1 now cites `walk_forward.py` lines 45 and 143-144.
- B2 APPLIED: section 1 C rewritten; the "label only" claim withdrawn, tie keys cited (`multigame_e1.py` 23, 50; `contract_records.py` 405-409; `game_draws_reader.py` 125); section 2 cites `e_001.py` 27 only for the run-mode pass-through.
- B3, B4, B6, B8, B9, B10, B12, B14, B15, B16, B17, B18, B19, B21, B23 APPLIED (kept as cited; still correct). B4's `game_profiles.py` 72-76 citation was dropped, harmlessly.
- B5 APPLIED: section 3.1 table cites 98-109.
- B7 APPLIED: section 3.1 table cites 49-51, 64-69, 120-121.
- B11 APPLIED: section 3.1 cites 629 (version), 633-637 (NO_CHANGE), 643-647 (UPDATE).
- B13 APPLIED: section 3.1 cites line 446.
- B20 APPLIED: the `Method_Contract_Runner.py` 89-90 citation is replaced by `roots()` at "lines 64-70" in section 5.1, which is itself IMPRECISE (see part 2).
- B22 APPLIED: section 5.1 cites 118-122. B24 APPLIED: section 7 cites 616-617 and 653-672.

**C (conflicts)**
- C1 APPLIED: section 1 C carries the corrected reason and both new citations. One caveat: it says the reason "is corrected here, in the roadmap and in the stock-take record"; at `3a9f6ac` the roadmap (10c, line 149) and stock-take v0.7 still carry the wrong sentence (N15).
- C2 APPLIED: section 5.1 unreserves E2R-R41's rows as written (`WF_FORECAST`), no new product kind; E2R-R44 named; section 6.4 marks `CATCH_UP` as an E2R-1 9.1/E2R-R41/R3 17.3.9 amendment; section 9 lists the amendments.
- C3 APPLIED: section 5.4 families are mode `WF` with an `evidence_tier` field.
- C4 APPLIED: section 6.5 adopts R3 10.5's two timing statuses and E2R-R40C; the supersession list now includes R3 1.5, 10.2's paragraph, 17.3.9. It introduces a logical flaw (N6) and leaves four 10.5 statuses unaddressed (N7).
- C5 ANSWERED in part: section 3.2 rule 3 separates the development-prefix definition from the run-time target gate and lists E2R-R52 and R3 6 as register amendments; the caller-based wording remains (N10).
- C6 APPLIED: Terms and section 6.6 (score ledger = R3 11.5 item 6; outcome record = the master row).
- C7 APPLIED: section 4.4 step 1 (MHUP-A only; B before the first weekly session); but see N9.
- C8 APPLIED: section 5.4 one flag naming the record and the decision.
- C9 APPLIED: sections 5.1 and 6.1 run under `Run_Experiment.bat` (Option F); this collides with the MRT-05 static firewall (N5).
- C10 APPLIED: section 6.1 step 3 and section 7 (weekly backup, monthly restore test).

**D (gaps)**
- D1 APPLIED: section 2 E_1 revision 3 inside MHUP-A; cohort stays 40; baseline record 39; labels follow r3's install date. New problems in the detail: N1, N2, N3, N13.
- D2 APPLIED: section 3.1 inventory table, including the coordinated-path lines marked unchanged.
- D3 APPLIED: section 3.3 one data kind, with a test.
- D4 APPLIED: section 6.3 target-outer, four steps (one residual criterion mismatch, N11).
- D5 APPLIED: section 6.4 one-hour margin; a straddling set labelled by its line (`deadline_met`); residual tier mismatch N12.
- D6 APPLIED: section 5.2 defines DONE and COMPLETE; section 5.3 uses COMPLETE.
- D7 APPLIED: section 6.3 "finished" = DONE Mode H pair or score record; section 5.4 "whose Mode H pair is DONE".
- D8 APPLIED for MHUP-A: section 5.1 kind-aware `roots()`, `wf-` IDs kept, `load_plan` root, `.gitignore` members; MHUP-B's folders not covered (N14).
- D9 APPLIED: section 4.2 exposure paragraph, `.gitignore` for backups/grabs/lock, owner records tracked; section 9 Q7 document list.
- D10 APPLIED: section 3.2 own copy of `LEDGER_COLUMNS` with an equality test; the tool is not imported.
- D11 APPLIED: row types `MODE_H_STUDY_MANIFEST`, `HOLDOUT_OPENED`, `MODE_H_REPORT`, `WEEKLY_REPORT`; the Mode H plan row's type still unnamed (N16).
- D12 APPLIED: section 4.1 enumerable file set.
- D13 APPLIED: section 6.4 invariant as a postcondition.
- D14 APPLIED: section 7 (restore test, orphan grab kept, message attributed to the updater).
- D15 APPLIED: section 5.2 (first DONE attempt; all attempts precede any outcome read).
- D16 APPLIED: section 5.4 flag in score records, ledgers and reports only.
- D17 APPLIED: section 2 last sentence; see the observation N17.
- D18 APPLIED: section 4.3 (no commit ID; release day; duplicates refuse).
- D19 ANSWERED: section 5.1 no new switch, record-gated, H-1 5.4 amended; where the gate is enforced is still unsaid (N10).
- D20 APPLIED: section 5.4 tier-aware texts, line 422 named.
- D21 APPLIED: section 4.4 step 3 acceptance rule.
- D22 APPLIED: section 9 Q1-Q9 table.
- D23 APPLIED: section 4.5 comparison.
- D24 APPLIED: section 3.2 rule 2.

**E (terms)**
- E1 APPLIED (card summarises the three notes; Appendix A). E2 APPLIED (section 9 table). E3 ANSWERED (section 3.2 rule 3 and section 6.4 explain the two senses; still two senses). E4, E5, E7, E8 APPLIED (Terms). E6 APPLIED (section 5.2). E9 APPLIED (section 1). E10 APPLIED (section 5.4). E11 APPLIED (section 5.1 "owner-reported, H-1 7.5"). E12 APPLIED (section 8 table).

**F notes** APPLIED: rate marked owner-reported and estimated, understatement noted; half-day and one-day estimates marked. One new date inconsistency: N1.

## 2. New code citations in the revised design

| Citation | Verdict | Note |
|---|---|---|
| `multigame_e1.py` 23 | CORRECT | `str(target)` in the tie-key tuple. |
| `multigame_e1.py` 30-34 (section 2 splits 30-32 / 33-34) | CORRECT | `data_kind` refusal 30-32; target refusal 33-34. |
| `multigame_e1.py` 50 | CORRECT | Ties sorted by `_digest(digest, target, ...)`. |
| `contract_records.py` 335-336 | CORRECT | `validate_run_request` target ceiling (E2R-R52 in the message). |
| `contract_records.py` 354 | CORRECT | `ledger_version` 1..1. |
| `contract_records.py` 405-409 | CORRECT | `tie_identity_for` with `target_draw_number`. |
| `contract_forecast.py` 275-277 | CORRECT | `_validate_header`, used for forecast and diagnostic records. |
| `contract_receipts.py` 68 | CORRECT | `ledger_version` 1..1 in receipts. |
| `contract_task.py` 45-46 | CORRECT | `view_data_kind`. |
| `Method_Contract_Runner.py` 50 | CORRECT | `'ledger_version': 1` in `build_request`. |
| `walk_forward.py` 45 and 143-144 | CORRECT | Constant; enforcement and the quoted phrase. |
| `walk_forward.py` 56-59 | CORRECT | The `CONTINUE` table (the classifier is 86-90). |
| `walk_forward.py` 64-70 | IMPRECISE | `roots()` is lines 66-70; 64-65 are blank. |
| `walk_forward.py` 98-109 | CORRECT | `ledger_pin`. |
| `walk_forward.py` 208-214 | CORRECT | `load_plan` head; the root path at 212. |
| `walk_forward.py` 264-271 | CORRECT | The attempts comment block. |
| `walk_forward.py` 331-352 | CORRECT | The claim is the docstring (331-332) and the non-SUCCESS DONE rule (349-352); the function runs 330-370. |
| `walk_forward.py` 387-391 | CORRECT | `pending()`. |
| `outcome_reader.py` 64-69, 120-121 | CORRECT | Single INIT row; second guard. |
| `contract_runner.py` 114-116, 118-122 | CORRECT | Switch check; data-source rule. |
| `report_writer.py` 422 | CORRECT | The sentence spans 422-423 ("no holdout draw is read or scored"). |
| `game_draws_reader.py` 125 | CORRECT | `'target': self.target` in the view digest. |
| `results_master_v0_1.py` 299, 446, 616-617, 629, 633-637, 643-647 | CORRECT | Message text; INIT via `to_csv_bytes`; overlap refusal; version increment; NO_CHANGE; UPDATE. |
| `multigame_standalone_contract.py` 43, 120; `multigame_worker_launch_handshake.py` 27; `coordinator_private/multigame_launch_spec.py` 63 | CORRECT | All four are `historical_development_target_allowed` checks; 43 and 120 are the legacy (Package 2) standalone path, the other two the coordinated path, as the table says. |
| E2R-1 lines 500-503 | CORRECT | Reserved table header and the two rows. |
| Register lines 1183, 1189, 1215 | CORRECT | Unchanged. |
| `game_profiles.py` 72-76 | not cited in the final text | The draft's citation was correct. |
| `.claude/settings.json` "deny those reads" (section 4.2) | CORRECT | `Read(**/source_data/**)`, `Read(**/results/**)`, `Read(**/transitory_data/**)` are denied. |
| R3 17.3.5 quotation (section 1), R3 3.6 (section 5.2), E2R-R40C (section 6.5), H-1 1.4 for R-4 (Terms) | CORRECT | Lines 1130, 245, 466; H-1 1.4 lists R-4 as "independent reference oracles where justified". |

## 3. New conflicts, gaps and inconsistencies introduced by the revision

- **N1 (section 2 vs section 8).** Section 2 says E_1 revision 3's forecasts for "Powerball 1590-1591" are development evidence. Section 8 installs MHUP-A by Sun 8 Nov; under section 4.3's rule (release date before the draw's date) Powerball 1591 (Thu 12 Nov) and Oz Lotto 1708 (Tue 10 Nov) would then be CATCH-UP for E_1 r3. Fix: "every draw dated on or before MHUP-A's install date", no draw numbers.
- **N2 (section 2 vs E2R-R58 and ER-2r1).** "a new declaration and a `SUPPORTED` entry released by the same package (E2R-R58, as REL-1 did)": E2R-R58 makes release a separate small package and new code arrives non-runnable (H-1 5.3); REL-1 *was* that separate package. The one-package precedent for E_1 is ER-2r1, an owner exception with five named steps behind E_1's own `IN_DEVELOPMENT.txt` barrier, copied first and deleted last, never committed (register lines 1200, 1214; EX_087 B01 on fail-closed interim states). Fix: a separate REL-2 package, or ask the owner for an ER-2r1-style exception and name the barrier and the interim refusal codes.
- **N3 (section 2 vs E2R-R56 / E1R2-T07).** Section 2's identity test runs "the archived revision 2 code". `tests/test_code3_retirement.py` 94-99 (`ArchiveIsNeverExecuted`, "no test-only exception") scans `src/**/*.py` and `tests/*.py` for archive references; E1R2-T01 proved r2 = r1 with a frozen reference fixture computed outside the repository (`tests/fixtures/e1_r1_reference_v1.json`; `test_e1r2_revision2.py` lines 3-9, 85-97). Fix: an `e1_r2_reference_v1.json` fixture computed at the base, outside the repository.
- **N4 (section 3.3 "the existing 471 tests unchanged" vs sections 2, 3, 6).** Existing tests that must change: `test_code3_retirement.test_the_archive_is_no_package_and_only_r1_exists` (line 91 asserts only `r1` under `archive/methods/E_001`); `test_e1r2_revision2.test_admitted_and_refused` (223-239 asserts E_1 *refuses* `REAL_HOLDOUT`, `FINAL_NEXT_DRAW` and targets at or above `holdout_first`) and `test_r2_equals_r1_label_for_label` (dispatches revision 2, refused once r3 holds the active `SUPPORTED` entry); `test_wf1b_static.test_the_evaluator_imports_no_method_code` (`ALLOWED_COMMON`, lines 12-14, lacks `_common.master_versions`) and `test_only_the_outcome_reader_touches_the_masters` (line 63: only `report.py` may import the outcome reader). Fix: scope the sentence and list each change.
- **N5 (sections 6.1 and 4.1 Option F vs MRT-05).** `Run_Experiment.bat` launches only `src\methods\<file>` (its lines 13, 20, 38). `test_wf1b_static.test_no_method_file_imports_the_evaluator` (34-38; Architecture 12.5; MRT-05) forbids every file under `src/methods/` from importing `evaluation` or naming `outcome_reader`. `Method_Weekly_Session.py` must score (section 6.3 step 3, section 6.6) and `Method_Mode_H.py manifest` must read the family registry, measures and scorer version (section 4.1): both breach the firewall. The evaluator's precedent is `src/evaluation/Method_Rankings_Report.py` with its own `Run_Method_Rankings.bat` (WF-1B). Fix: choose and name the bent rule: one evaluator-side command with its own launcher (against H-1 5.4's "no second production launcher", already bent once), or a forecasting half under `src/methods/` and a scoring half under `src/evaluation/` (against MH-1's "one wrapper command per game").
- **N6 (section 6.5, logical).** The freeze line is create-only and digest-chained, yet lists "the publication status" as a field, and `PUBLISHED_BEFORE_DRAW` depends on a witness receiving *that line's digest* after the line exists. The status cannot live in the line. Fix: a separate witness record (its writer, the receipt evidence and how it is verified offline under OFF-1 are unspecified) or the score-ledger line, which section 6.6 already lists as carrying it.
- **N7 (section 6.5 "R3 10.5 ... applied as written").** Only two of 10.5's six statuses are used. A missed deadline (section 6.4 last bullet) produces no `MISSING_BATCH` record ("Report missing weeks rather than silently skipping them"); a failed variant has no `PREDICTION_FAILED` in the weekly path (section 5.2 covers Mode H only); `OUTCOME_PENDING`/`OUTCOME_AVAILABLE` are implicit. Fix: say which statuses the ledgers and the status block carry, and that a missed prospective set is recorded as `MISSING_BATCH` on the later catch-up line.
- **N8 (section 5.4 vs the three-way split).** "Scored once ... a second [attempt] is refused unless the first ended in a STOP before any outcome read" leaves no room for the ratified exception (2 Nov; section 6.3 step 3; direction section 2): a separately identified scoring run beside the first for a scorer fault or a new measure. Fix: carve it out for Mode H too.
- **N9 (section 4.4 step 1 vs section 5.1 R3-T50 check).** MHUP-B "may follow" any time before the first weekly session; installed after Approval 1 and before Approval 3 it changes the code digests of section 4.1's set (new files under `src/methods/` and `src/evaluation/`), so the batch's digest check refuses. Section 8's plan avoids it; the rule does not. Fix: MHUP-B before Approval 1 or after Approval 4, never between.
- **N10 (sections 5.1, 6.7, 3.2 rule 3: where the record gates bind).** Nothing stated stops `REAL_HOLDOUT` on a development target (a `HOLDOUT_MODE_H`-tier record for a development draw), `CATCH_UP` or `FINAL_NEXT_DRAW` on a holdout target, or a hand-made `Method_Contract_Runner.py run --mode CATCH_UP` bypassing the weekly command's developed-record check; and "keeps gating `REAL_DEVELOPMENT` runs made by the walk-forward driver's development batches" is a caller-based rule the validators cannot see (E2RC2-B01/B02). Fix: request-level rules in the validators: `REAL_HOLDOUT` only for targets in `[holdout_first, holdout_last]` with the opening record; `CATCH_UP` and `FINAL_NEXT_DRAW` only above `holdout_last` with the developed record; `REAL_DEVELOPMENT` above the cap only with the opening record (and say that a hand-made request is then admitted too, or refuse it).
- **N11 (section 6.3 step 1 vs step 2 and section 5.2).** Step 1 runs "every active variant without a frozen forecast for N"; step 2 waits for "a DONE record". A variant whose run ended `RUNTIME_FAILURE` (DONE, no forecast) is re-run on every pass. Fix: step 1's criterion is "without a DONE record for N".
- **N12 (section 6.4 last bullet).** A straddling `FINAL_NEXT_DRAW` set's frozen records and receipts carry tier `PROSPECTIVE` (E2R-R41 fixes the tier per run mode) while the line says `deadline_met: false` and "never counted as prospective evidence". Fix: say the line's `deadline_met` governs every report and the record's tier is read with it.
- **N13 (section 2 vs section 4.3).** Section 2: the baseline record "lists 39 variants"; section 4.3: it also lists "E_1 revision 2's release ... for the record" (40 entries); and "every entry it names must exist in the installed registry" is undefined for a revision whose entry is superseded after MHUP-A. Fix: 40 entries, one marked superseded; "exist" = a chain entry exists, active or not.
- **N14 (sections 6.4, 8).** MHUP-B's `results/real/weekly/contract_runs/`, its attempts and score folders have no `.gitignore` line (section 5.1's are MHUP-A's), and whether `FORECAST_LEDGER_V1.jsonl` / `SCORE_LEDGER_V1.jsonl` are tracked (pushable as a witness, direction section 9) is not said. Fix: list MHUP-B's lines; ledgers tracked, run folders ignored.
- **N15 (section 1).** "corrected here, in the roadmap and in the stock-take record" claims corrections the design cannot make; at `3a9f6ac` roadmap 10c (line 149) and stock-take v0.7 still carry the wrong sentence. Fix: "to be corrected in the roadmap and recorded in register v0.24", with the roadmap commit alongside EX_124.
- **N16 (section 5.1).** `load_plan` requires a `WF_BATCH` search-log row with the plan digest (`walk_forward.py` 220-230); the Mode H plan's row type is not named (the manifest's and report's are).
- **N17 (sections 2, 3.3; observation).** Under one data kind, E_1 r3's Mode H forecast for Powerball 1577 (prefix 1144-1576, the legacy view schema, E_1's own tie rule) coincides label for label with the legacy forecast-only 1577 regression that R3 6 says is "never scored". The design scores the Mode H record and keeps the legacy one unscored; the numbers are the same. Say so (a free R-4 oracle; R3 6 protects the legacy record's status, not the numbers), or the reviewer will raise it.
- **N18 (section 5.2, minor).** "a second plan for the game is refused" is not enforced by `wf-<32 hex>` paths; say what marks a game's Mode H plan as existing (for example the study manifest records the batch id, create-only).

## 4. Verdict

**READY WITH FIXES.** Every cold-read finding is applied or answered and the critical premises now hold against the code. Before sending, fix: N1 (the 1591 label), N2 (E2R-R58 / ER-2r1), N3 (reference fixture, not archived code), N4 (the tests sentence), N5 (the firewall versus Option F: decide which rule bends), N6 (publication status out of the chained line), N7 (R3 10.5 statuses), N8 (the corrective-scoring exception), N9 (when MHUP-B may install), N10 (request-level mode gates), N11 (step 1's criterion), N13 (39 or 40 entries), N15 (what is corrected where), and the `roots()` line range (66-70). N12, N14, N16, N17, N18 are small and can go in the same pass.

**Confirmation.** In this recheck I opened no file under any `source_data`, `results` or `transitory_data` folder, listed none of them, and read no data value; the files read were the three scratch files, `src/` and `tests/` sources, `.claude/settings.json`, `Run_Experiment.bat` (grep only) and the cited documents. No draw outcome of Powerball 1577 or later or Oz Lotto 1694 or later was displayed, quoted or computed with. No web access; nothing run except read-only `grep`/`sed` and `git log`/`git status`; no repository file was modified.

*End of the recheck.*
