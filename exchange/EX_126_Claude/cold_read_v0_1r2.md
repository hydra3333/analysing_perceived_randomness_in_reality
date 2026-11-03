# Cold read of the draft of design v0.1r2 (MHUP-1) before the EX_127 recheck (3 November 2026)

A fresh helper (a separate agent with no knowledge of the Claude chat) was given the repository, the v0.1r2 draft, the v0.1r1 edition, EX_125 and the owner's decisions, and asked to check each EX_125 finding's resolution, the eight acceptance items, the citation anchors, internal consistency, process safety and plain English. Its report follows, unchanged except for ASCII normalisation ("section" for the section sign; ">=" and "->" for the symbols). Every N, P and E item is applied in the final v0.1r2; `design_v0_1r2_draft_to_final.diff` shows the changes.

Read: the v0.1r2 draft (622 lines) against v0.1r1, `exchange/EX_125_ChatGPT.md`, `exchange/OWNER_ROADMAP.md` item 10c, H-1 v1r7 (1.6, 5.1, 5.4, 6, 7.3, 10), register v0.23 (ER-2r1 line 1200; HX-1/HX-2/MH-1/OFF-1/EFF-1 lines 1311-1333), R3 v0.5 (6, 6.2, 6.3, 10.1-10.5, 11.5, 17.3.5 line 1130), E2R-1 v0.3r3 (R13, R14A, R39, R40C, R41 lines 500-503, R44, R52, R54, R56, R58), Architecture v0.9 section 5C, and the code at `3a9f6ac` via `git show`/`git rev-parse`. No data folder opened; no draw outcome displayed.

Every finding is numbered. N-items are internal contradictions (section 4); P-items process safety (section 5); E-items plain English (section 6).

## 1. EX_125 resolution check

| Finding | Verdict | Where / what is missing |
|---|---|---|
| B01 real-mode bypass | PARTLY | 3.4 (a)/(b)/(c) and Appendix E deliver the three-way split, the binding, the sealed-batch refusal and the "opening record authorises no run" sentence (4.2). Holes: (1) N1: 6.3 declares the weekly scope to include the holdout targets "so that a method released later gets development-tier forecasts for them", but 3.4(a) and Appendix E row 4 refuse `REAL_DEVELOPMENT` on any holdout target at every stage; so for any variant released after Mode H, `next` picks N = `holdout_first` (not closed, result accepted), the run is refused at the structural gate, and the session can never advance. Not a bypass, but the matrix's one-sentence treatment of "a newly released variant" hides a dead loop. (2) N5: 3.4(c) says a record is scored only if it is "the first DONE attempt of its pair in ... the session's freeze line", but 6.3 ("scores every record of N that has no score line yet"), 6.6 (keyed by `run_id`) and Appendix F contain no first-attempt rule, and 6.3's roster construction does not say which record goes into the freeze line when two bound DONE records exist for one (variant, N). E2R-R40C requires the official designation to be fixed by a predeclared rule. (3) N6: 3.4(b) has the dispatch gate decide "the batch must not be sealed (no COMPLETE score record for it)". `contract_dispatch.py` "never reads a master, ledger or any draw data" (E2R-R23A), and the score ledgers hold drawn numbers. The seal must be a value-free marker beside `MODE_H_BATCH_ID.json`, written by the scorer; the design has none. (4) The hand-typed `--binding` path (3.4 last paragraph; Appendix E row 9) is exactly the "alternative" EX_125 says "needs a deliberate owner decision and a documented safety argument"; it is not in section 9's DECIDED or RECOMMENDED lists. |
| B02 MH-1 order | RESOLVED (one wording note) | 6.1, 6.3, Appendix F: `next`/`score` alternate per target; the forecasting half enforces the order; resume per persisted step; open forecast handled first; never past an unaccepted draw. Note N9: MH-1's enumerated steps put "the scoring of any open prospective forecast" after the catch-up; the design scores it first (Appendix F property iv), which is the reviewer's B02 wording and the natural reading of "in draw order", but the design claims "implemented exactly" without recording that reading. Resume is safe for the cases stated; see P3 for the case not stated. |
| B03 witness status | RESOLVED | 6.5, 6.6, Appendix G. No publication status in any frozen record, freeze line or score line. `WITNESS_RECORDED` vs `WITNESS_VERIFIED` separated; status derived at report time; worked cases 1-4; no network. Observation: 6.5 names "the commit's push time as GitHub shows it" as the received instant; GitHub's ordinary commit view shows the committer timestamp (a local clock), not the push time. |
| B04 study freeze | PARTLY | 4.1, 4.4, 5.1, Appendix H: closure, environment, `v_f`/`v_a`, re-check, exclusions. One defect, N7: "every file under `src/`" includes `__pycache__/*.pyc`, which the interpreter creates and rewrites under `src/`; the first import after the manifest produces a mismatch, or a stale `.pyc` is digested as "code". |
| B05 straddling tier | PARTLY | 6.4 and Appendix I give the per-record rule and name `LATE_PRE_DRAW`. But the table is not total over its own inputs (N2): no row for `FINAL_NEXT_DRAW` with the result accepted before the record; no row for `CATCH_UP` whose variant's release date is on/after the draw date; no row for `REAL_DEVELOPMENT` above `holdout_last` whose release date is before the draw date. 3.4(a) checks mode-to-target range only, not release-date-to-mode. Also N3/N4. |
| C01 | RESOLVED | Section 2 and Appendix J. Minor N12: 4.3 fixes the release date as the POST PASS date (step 4), while E_1 r3 becomes runnable at step 7. |
| C02 | RESOLVED | 3.2 rule 1 is a closed grammar matching `LEDGER_COLUMNS` and the writer at 629-647. Nit N10b: the `note` column is unconstrained. |
| C03 | RESOLVED | 7 (A6); Appendix K row. |
| C04 | RESOLVED (see N5) | 6.6 key; failure records distinguished; primary statement amended. N5: a key with `run_id` permits two scored attempts per pair unless the first-attempt rule is carried into 6.3/6.6. |
| C05 | RESOLVED | 5.3 and 1. |
| C06 | RESOLVED | 3.3 and 2 (verified: `permitted_view_digest` routes through `view_data_kind`, contract_task.py lines 45-50). |
| C07 | RESOLVED | All 69 Appendix D anchors verified (section 3). |
| C08 | RESOLVED | 6.4, 6.5, Appendix I rows 5 and 7. |
| C09 | RESOLVED | 5.4, 6.6. |
| O01, O02, O03 | RESOLVED (noted) | 1, 4.5; 6.7, 6.4, 4.3, 5.4; 4.2, 4.4 step 2, 9 Q7. |

No finding is MADE WORSE. B01's over-closure (N1) is the price of fixing r1's under-closure and must be reconciled.

## 2. Acceptance items 1-8

| Item | Verdict | Appendix / gap |
|---|---|---|
| 1 Gate matrix | PARTLY | Appendix E. Missing row: `REAL_DEVELOPMENT` above `holdout_last` unbound. Row 3 says "validate; publish refused" at S0 but bare "refuse" at S1-S4 for the same request (N13). "Newly released / retired" is one preamble sentence and conceals N1. |
| 2 Event-order diagram | DELIVERED | Appendix F. |
| 3 Witness lifecycle | DELIVERED | Appendix G. |
| 4 Digest inventory | PARTLY | Appendix H; N7. |
| 5 Classification table | PARTLY | Appendix I; N2, N3, N4. |
| 6 Install safety table | DELIVERED | Appendix J. |
| 7 Citations, Lotterywest, retained/superseded, names | DELIVERED | Appendix D, section 7, Appendix K. |
| 8 Oracles and tests | DELIVERED | Appendix L. Add the test for N1's case and `test_wf1b_static.py` line 60 (N11). |

## 3. New citations and anchors

- D1. 69 of 69 anchors: blob id correct, quoted first-line text correct; ranges spot-read, not just first lines, for every citation in sections 2, 3.1, 6.1 and the code the body cites. All say what the body says they say.
- D2. Body citations without an anchor: none for code. Document-line citations (R3 line 1130; register lines 1200, 1183, 1189, 1215; E2R-1 lines 500-503) verified correct.
- D3. Anchors with no corresponding line citation in the body (harmless): `Method_Contract_Runner.py` 89-90, `contract_vocab.py` 69-73 and 113, `results_master_v0_1.py` 226-233 and 592, `game_profiles.py` 72-76, `test_code3_retirement.py` 94-99.
- D4. EX_125's examples (refusals at 27-31, `roots()` at 57-61, `tie_identity_for` at 368-372) are consistent with a view that strips blank/comment lines or a different base; the Git objects at `3a9f6ac` support the design's numbers. C07's "rebutted with evidence" stands.

## 4. Internal consistency

- N1 (high). 6.3 scope ("every draw from `holdout_first` onward ...") and Appendix I row 5 vs 3.4(a) and Appendix E row 4. `next` dead-locks at N = `holdout_first` for the first variant released after Mode H. Fix: scope the weekly session at `holdout_last + 1` and say what a later-released variant gets for the holdout draws; add the test.
- N2 (high). Appendix I is not total: missing (`FINAL_NEXT_DRAW`, result accepted before the record), (`CATCH_UP`, release date >= draw date), (`REAL_DEVELOPMENT` above `holdout_last`, release date < draw date). Either the gates refuse the mismatch (then say so in 3.4 and Appendix E) or the table classifies them.
- N3 (medium). Appendix I row 10 vs 6.1 (a session pins the ledger's last row) and 3.2 rule 2. If the master grows mid-session the pins differ; the design should fail closed rather than switch modes, and no gate compares a run's pin with its session's pin.
- N4 (medium). Appendix I row 9 vs 6.4 bullet 4 (`NONE` once less than an hour remains). Say whether the hour rule is per run or per set; `LATE_PRE_DRAW` is reachable only under the per-set reading or a run longer than an hour.
- N5 (medium-high). 3.4(c) first-attempt rule vs 6.3/6.6/Appendix F. Carry 5.2's rule into 6.3: the freeze line names exactly one record per active variant.
- N6 (medium). 3.4(b) dispatch gate reading a score record vs `contract_dispatch.py`'s "never reads any draw data" (E2R-R23A). Define a value-free seal marker.
- N7 (medium). Appendix H vs `__pycache__/*.pyc` under `src/`.
- N8 (medium). 6.1 "waiting for each child; never polls" vs "a hung child ... reports `UNVERIFIED`". A blocking wait cannot observe a hang. Choose one; see P2.
- N9 (low). "MH-1's order implemented exactly" vs MH-1's step list; record the draw-order reading.
- N10 (low). 3.2 rule 1 "Row 1 ... today's exact checks (unchanged)" vs today's INIT check binding `master_sha256` to the run's pin. N10b: the `note` column.
- N11 (medium). Appendix L omits `tests/test_wf1b_static.py` line 60 (no evaluator file but `outcome_reader.py` may name `source_data`); `Method_Mode_H.py` writes two owner records into `source_data/`.
- N12 (low). 4.3 release date = POST PASS date vs Appendix J step 7.
- N13 (low). Appendix E row 3 wording.
- N14 (low). Appendix K names `verify`; the body never does.
- N15 (low). Section 0 "two separate programs" vs 6.1 "Three programs".
- N16 (low). Sections 0 and 8 "before 00:00" while 6.4's operative cut-off is 23:00.
- N17 (low). Terms: "real-mode request" vs 3.4(a).
- N18 (low). 3.1 table: say the ordinary `WF` batch kind keeps `last <= holdout_first - 1`.
- N19 (low). Section 8 puts the rulebook additions in MHUP-A while the files they name arrive in MHUP-B.
- N20 (consistent). E_1 r3 release-date consequences; 4.4 vs section 8; package contents; Appendix K vs the body except N6/N14 and P1.

## 5. Process safety (6.1 orchestrator)

- P1 (medium). Architecture 5C.1 names two launch interfaces and "no second production method launcher". The orchestrator is a third Python parent of `Run_Experiment.bat`. State either that 5C.1's list is amended by ratification, or that the orchestrator is not a coordinator under 5C and why.
- P2 (medium). Hung child: with "wait for each child" there is no hang detection (N8). Say: blocking `wait()` with no timeout; a hang is visible to the owner; nothing is killed; nothing is reported as `UNVERIFIED`.
- P3 (medium). H-1 section 6: Windows does not kill children when the parent dies. An interrupted orchestrator can leave the forecasting half running and publishing bound records while the owner starts a new session. No session-level interlock. Either a create-only session lock or an explicit statement plus the first-attempt rule.
- P4 (low). 5C.1's venv refusal applies to the orchestrator too; 6.1 gives it to the wrapper only.
- P5 (precedent). `Run_Experiment.bat` as a child of a Python process: `src/Powerball_Experiment_Coordinator.py` line 35, line 793, lines 943-945 (`subprocess.Popen(command, stdout=PIPE, stderr=STDOUT, stdin=DEVNULL, text=True, cwd=ROOT, shell=False)`); `multigame_windows_lifecycle.py` 137-139. Both precedents are POC/synthetic-only. The design should cite the precedent and its limits, and copy `cwd=ROOT`, `shell=False`, `stdin=DEVNULL` and the `SAFE_ARG` discipline.
- P6 (low). The orchestrator must learn the session id and N from the children (stdout or exit codes); unstated.

## 6. Plain English

- E1. Section 0 is plain except item 4's "N-1 isolation" and item 5's "two separate programs".
- E2. Section 1: the option C bullet is written for the reviewer; the owner needs only its last sentence.
- E3. 6.3: the `next` bullet is one 120-word sentence with four conditions; split it.
- E4. 6.4: the first bullet's vocabulary citation is jargon; the effective-class paragraph is not plain; a two-line example would carry it.
- E5. Appendix F readable; Appendix G plain; Appendix I plain apart from row 10 and the terse "Counted where" column.

## 7. Verdict

READY WITH FIXES. The structure answers all 17 EX_125 findings and the eight acceptance items; the citations are verified; the fixes are text-level. Ranked: 1. N1; 2. N2 + N3 + N4; 3. N5 + P3; 4. N6; 5. N7; 6. N8 + P1 + P2 + P4; 7. N11; 8. the B01 owner decision (the hand-typed `--binding` path) under RECOMMENDED/for the owner in section 9; 9. low items N9, N10, N12-N19, P5, P6, E1-E5.

Confirmation: nothing under any `source_data`, `results` or `transitory_data` folder was opened, listed or read; no drawn numbers of any draw were displayed or computed; draw numbers and dates appear only as identifiers.

*End of the cold read.*
