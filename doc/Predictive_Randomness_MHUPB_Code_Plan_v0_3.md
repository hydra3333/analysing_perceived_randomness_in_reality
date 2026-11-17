# MHUP-B code plan - v0.3 (RATIFICATION CANDIDATE)

**Status: RATIFICATION CANDIDATE v0.3, by the Claude web chat, 17 November 2026 (Adelaide). A plan only. It authorises nothing: no code,
package, task file, run, registration, re-forecast or install. No implementation code exists.** By the owner's
instruction (decision log entry 67), no code is written until this plan is complete and owner-ratified and he has then
given a specific go for code.

**What changed from v0.1.** The reviewer's review (EX_223, which supersedes EX_221 and EX_222: PASS WITH REQUIRED
CORRECTIONS) and the owner's directions on OD-1 to OD-6 (decision log entries 69 and 70) are applied. Section 1A says
where each point landed. v0.1 stays beside this file, and `PLAN_v0_1_TO_v0_2.diff` shows every changed line. The design
amendments the plan needs are in the supplement's next full edition,
`exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_8_RATIFICATION_CANDIDATE.md` ("Sup v0.8"), which goes to the
same ratification.

**What changed from v0.2.** The reviewer's focused recheck (EX_225) passed v0.2 with two corrections, both applied here
and in Sup v0.8: RC-225-1, what local records can and cannot establish about a missed week (L5; 6.6); and RC-225-2, a
repeated admission of the same attempt changes nothing and no publication is made twice (L4; L8; 9). R-5's conditions
for the report-only form are added to L8, and section 12 records the answers. Nothing else changed.
`CANDIDATE_TO_RATIFICATION_CANDIDATE_PLAN.diff` shows every changed line; v0.2 stays beside this file.

**Authorities it stands on:** the ratified design `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`
("Des") sections 6 and 7 and Appendices E to L; the ratified supplement
`doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md` ("Sup"; RAT-33), which governs until v0.8 is ratified;
register v0.31; H-1 v4; the approach of 16 November 2026 with EX_206's conditions; the working approach P0-P6 (decision
log entry 1); EX_213's code-round gates; EX_219's cautions C1 and C2; EX_223. Where this plan and those documents
differ, they govern, and the difference is a fault in this plan. Where the plan relies on an amendment of Sup v0.8, it
says "Sup v0.8".

**Base:** `main` at `cc665ce` or later. No file under `src/`, `tests/`, no root `.bat` and no `requirements.txt` has
changed since `cc0ab73` (checked with `git diff`); `.gitignore` changed at `cc665ce` (section 3). **Risk tier:** HIGH
(always-review subjects: N-1 boundaries, holdout access, freezing and publication, TOP/WORST readout, the evaluator and
scorer, launchers).

**Evidence with this plan** (folder `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/`): the baseline suite summaries; the OV-1
numerical probe `ov1_lower_bound_probe.py` and its outputs; the census of the real score records (`score_census.py`
and its output). The probe is a plan-stage feasibility tool on invented data, not project code.

## 0. In plain English

- **What gets built.** One package, in the supplement's eight layers. Layers 1 to 3 are the weekly live path (catch up
  missed draws, freeze the next forecast, score). Layers 4 to 7 are reporting (the league table, the one formal test
  OV-1, runs over past draws, the full report). Layer 8 is the commands, the install and the documents.
- **Three everyday jobs, one command each** (section 12A). The weekly session. Giving a new method its history and
  refreshing the all-method league table. Re-running any method over past draws for research. The owner never edits a
  ledger, a hash, a source list or a version number, and one go from him covers the whole of one job.
- **A lot is already there.** MHUP-A installed most of the gates and record rules the weekly session needs. Section 2
  lists exactly what exists and what is missing.
- **Four things the installed code cannot yet do, which the plan changes with care** (section 2): it never checks that a
  next-draw forecast is really for the next draw; it refuses every development run and report on a holdout draw or
  later; it never releases a result after the holdout to any scorer; and a report over exactly the ten holdout draws
  would pick up the Mode H test families by accident.
- **The formal test's arithmetic can be made provably safe** (section 6). Every figure is a whole number, every rounding
  goes against a crossing, and the loss is about one part in 10^30 per draw. Each draw's factors are worked out and
  sealed before the draw, and the program checks that they average at most 1 under fair draws.
- **A missed week no longer ends the formal test** (Sup v0.8 6.8). A draw with no forecast set frozen in time counts as
  neutral, by a rule fixed in advance that cannot see the result. A frozen set whose pre-draw entry is missing still
  stops the test, and a stopped test stays stopped.
- **The test baseline is measured.** On `main`, three tests fail, all known: two tied to the old results files, and one
  that expects an ignore line the owner has since commented out. Each fix keeps what the test proves (section 3).
- **The real score records are checked.** The owner committed them; they are exactly what the installed programs
  define, and the sealed Mode H files match their seals (section 8).
- **Nothing is left for the owner to decide before ratification.** His six directions are in section 12.

## 1. Scope

**In scope** (Sup 2; Des 6, 7, 8): L1 `CATCH_UP` and `FINAL_NEXT_DRAW`; L2 the forecasting half, sessions, tickets, the
freeze line, the forecast and witness ledgers; L3 the scoring half and the score ledger; L4 the league table, its
sources, archive, `current` folder, history and reconstruction; L5 OV-1; L6 the window contract and the two kinds of
development run; L7 the consolidated report and the retired-revision index; L8 the two sequencers and their launchers,
the owner's checklist (with the A7 recovery procedure), the rulebook edition, the document amendments, the package and
its rehearsal. Also, tests only: the fix for the tests tied to the version-1 masters (readiness finding F-2); the
ignore-list test; the newest-first and shuffled page cases for the updater's tests (register v0.31, future action 4).

**Not in scope:** any change to a released method, to the updater's code, to Mode H's sealed records or their writers; a
corrective-scoring writer (only the reader side of corrections: Sup 4 rule 2); result corrections (R3 10.3); WF-1C; the
coordinated path; a joint two-game figure (Sup 6.3: never computed); a second OV-1 registration or any recovery after a
stop (OD-4); any new dependency.

## 1A. Where each point of EX_223 landed

| EX_223 | Point | In this plan | In Sup v0.8 |
|---|---|---|---|
| B01; OD-2, OD-3 | A missed week; the cut-off for the pre-draw entry | L5; 6.6 | 6.5, 6.8 |
| B02 | A table is logged only when its archive set is complete | L4 "Publishing"; 7; 9 | 5.1 |
| B03; CP-Q7 | Back-history by the release instant | L6 | 7.2 rule 2A |
| B04; OD-1 | Routine fill and exploratory rerun through one driver | L6; L4; 12A | 7.1A; 4 rule 2A |
| C01; CP-Q3 | Who starts a publication; one writer per ledger | L4; L5; L8 | 4 rule 4; 6.8 |
| C02 | OV-1's failure states; the table sealed before the outcome | L5; 6.3; 6.6 | 6.8 |
| C03 | One small tracked source file; no extra chain | L4 | 4 rule 5 |
| C04; Appendix A | Minimum administration | 0; 12A; 13 | - |
| CP-Q2 | The certificate as a hard refusal; proofs, not `decimal` checks | 6.3; 6.5 | - |
| CP-Q4 | Labels for the secondary family tables | L7 | - |
| CP-Q5 | Reading "scored" through one function, with a taint test | L2 | - |
| CP-Q6 | T017's dress rehearsal on invented data | 10 | - |
| CP-Q8 | Exposure flags wherever the draw is scored | L3; L4 | - |
| CP-Q9 | Negative mode-to-pin cases; X rebuilt two ways; the real-record census kept apart from fixtures | L1; 6.5; 8 | 14 |
| OD-4 | A stopped stream stays stopped | L5; 6.6 | 6.8 |
| OD-5 | The real score records checked before the install | 8 | - |
| OD-6 | Three technical review slices, one install | 4 | - |
| EX_225 RC-225-1 | What local records can and cannot show about a missed week; reconciliation with earlier records | L5; 6.6 | 6.8 |
| EX_225 RC-225-2 | A repeated admission of the same attempt is a no-op; one row per publication; resume after any crash | L4; L8; 9 | 4 rule 2A; 5.1 |
| EX_225 R-5 | The report-only form: a pinned, authorised batch; resumable; tested with both plan kinds | L8 | - |

## 2. What reading the installed code showed

Each item was read in the code at `b30919d`; file and function are named so the reviewer can check.

**Already installed by MHUP-A (reused, not rebuilt):**
- The record contract for sessions, tickets and freeze lines: `src/methods/_common/owner_records.py` (`SESSION_V1`,
  `TICKET_V1` with kinds `OPEN`, `DONE`, `FAILED_TO_START`, `SET_STARTED`, `RESUMED`; `FREEZE_LINE_V1`; the paths under
  `results/real/weekly/`; `read_jsonl` with the torn-last-line rule; `pair_done_in_any_session`; `freeze_line_exists`;
  the developed record; `EXPOSED_DRAWS`).
- The session branch of the dispatch gate: `contract_dispatch._resolve_binding` (session record and digest, the pin, the
  roster entry, the developed record, no freeze line for the target, no DONE ticket in any session, an open ticket, and
  `CATCH_UP` against the release date).
- The weekly run root and the current-pin rule: `contract_runner._run_root_for`, `_check_pin_current` (`STALE_PIN`).
- The process tool, complete: `src/package_tools/process_check.py` (`check-no-runs`, resume tokens,
  `clear-session-lock`, `clear-updater-lock`, the install lock, `unfinished_weekly_set`).
- The updater's refusal while a session lock exists; the record tool's refusal while a weekly set is unfinished.
- `mode_h.declare_developed` (it needs only the seal; it does not re-check the closure, so it still works after an
  install changes `src/`).

**Missing or blocking (each is a planned change; CF = code finding):**
- **CF-1. The vocabulary still shuts the weekly modes.** `contract_vocab.RUN_MODES` has no `CATCH_UP`;
  `FINAL_NEXT_DRAW` is in `RESERVED_MODES`; `producible` has no row for either; `EVIDENCE_TIERS` has no `CATCH_UP`.
  Three places special-case the string `'CATCH_UP'` ahead of this (`contract_task.view_data_kind`,
  `contract_runner`, the runner's command line).
- **CF-2. The mode-to-pin rule of Des 3.4(a) is enforced nowhere.** The reader admits any target up to
  `last_draw(v) + 1` for any mode (`game_draws_reader.load_pinned_draw_view`, `master_versions.target_admissible`).
  Nothing checks that `FINAL_NEXT_DRAW` targets exactly `last_draw(v) + 1`, or that `CATCH_UP` and a bound
  `REAL_DEVELOPMENT` target is at most `last_draw(v)`. No test asserts it. It has had no effect so far, because those
  modes cannot yet be requested. L1 adds it in the runner, where the pin is read, with a test written to fail first.
- **CF-3. Development runs stop at the old cap in three places.** `walk_forward.make_plan` refuses
  `last >= holdout_first`; `contract_records._check_mode_target_binding` refuses a `REAL_DEVELOPMENT` target above the
  development prefix unless it is session-bound or diagnostic; `report.run_report` refuses `last > holdout_first - 1`.
  Sup 7.2 (the window contract) needs all three changed.
- **CF-4. No outcome after the cap is ever released, except to the Mode H scorer during its one score.**
  `outcome_reader.outcome_release_allowed` returns False for every target above `holdout_last`, and for a holdout
  target once `SCORE_COMPLETE` exists. The weekly scorer and the post-seal development report both need a reviewed
  release rule (an always-review subject).
- **CF-5. A development report over exactly 1577-1586 (or 1694-1703) would load the Mode H families.**
  `report.load_families` matches on game and window only; the Mode H families carry `evidence_tier` but it is not
  read. Unreachable today (CF-3); reachable once the cap moves. L6 filters by tier and tests it.
- **CF-6. The existing driver always plans the whole released cohort** (`walk_forward.cohort`), and the owner declined a
  method-restricted plan on 31 October 2026 (ER-6, `doc/Predictive_Randomness_CODE3_and_E1_Revision2_Design_v0_1r2.md`
  line 231). But Sup 7.2 rule 2A (back-history above the holdout for a variant released later) can only be a restricted
  plan: the other variants already hold weekly records for those targets, and Sup 4's one-score rule forbids a second.
  Decision log entry 58 also records the answer "only the new or changed variants are computed". **Decided (OD-1, entry
  69):** plans of the new kind may name their variants, in two kinds of run (L6; Sup v0.8 7.1A).
- **CF-7. The development and Mode H score ledgers were git-ignored.** The owner committed them on 17 November 2026
  (`cc665ce`; OD-5, entry 70), so both AIs can now read the real records. Claude's one-time census of them passed
  (section 8).
- **CF-8. OV-1's X needs no outcome read.** X equals the sum, over the eligible variants, of TOP main matches minus
  WORST main matches, and those are in the score lines. So L5 reads the forecast ledger, the frozen tickets and the
  score ledger, and never the master (Sup 6.2 says X "needs only the scores already kept").
- **CF-9. `next` must know which records are scored** (Des 6.3 "closed"; Appendix F). The forecasting half is under
  `src/methods/`, and the score ledger holds match counts. Planned: one reader function in a shared record module that
  returns identities only (target, record digest, policy id), and a static test that the forecasting half reaches the
  score ledger through that function alone. Method code never sees it. The reviewer accepts this with conditions
  (EX_223 CP-Q5), which are in L2.
- **CF-10. E_1's development scores are for its old revision.** The census (section 8) shows the development score
  records of E_1 carry revision 2, now superseded; revision 3 has scores only in the sealed Mode H ledgers, which are
  shown and never summed. So in the first league table E_1 revision 3 would read `NO_SCORES`. A routine fill for it,
  and for every variant's holdout targets, is among the first runs the package makes possible (L6; section 12A).

## 3. The baseline on current `main` (EX_219 C2)

Run in the cloud workspace only, in a full disposable clone, each module in its own process
(`python -B -m unittest -v`), without class `T12Determinism` (E2R-T12 starts worker processes; that run context was not
requested). Nothing was fixed, skipped or relabelled.

| At commit | Python | Modules | Tests run | Modules failing | Failing tests |
|---|---|---|---|---|---|
| `b30919d` | 3.13.18 (Linux) | 45 | 570 | 1 | 2 |
| `b30919d` | 3.15.0b4 (Linux, venv with the project's direct packages) | 45 | 570 | 1 | 2 (the same two) |
| `cc665ce` | 3.13.18, the one affected module only (`tests.test_mhupa_launchers`, 10 tests) | 1 | 10 | 1 | 1 |

- **The two failures at `b30919d`, both in `tests/test_multigame_reader_contracts.py`** (class `V011ReaderTests`):
  1. `test_master_source_and_ledger_file_hashes`: the two masters' SHA-256 values are compared with the version-1
     values written in the test; the masters are now version 2.
  2. `test_only_legacy_e1_allowed_at_boundary`: requests at the first holdout target that the test expects to be
     refused are no longer refused (five assertions), because the opening record now exists and the master holds
     that draw.
  Both are the failures H-1 v4 section 6 names (readiness finding F-2). **No unexpected failure.**
- **The third, from `cc665ce`:** `tests/test_mhupa_launchers.py`, `test_gitignore_lines`. It requires the line
  `results/real/holdout/scores/` in `.gitignore`. The owner commented that line out when he committed the score
  records (decision log entry 70). The whole suite was not rerun at `cc665ce`; no file under `src/` or `tests/` changed
  there, and the one module that reads `.gitignore` this way was rerun.
- **So the known baseline is three failing tests, each with its cause.** T024's "571 pass with 4 symlink skips" (14
  November 2026, Windows, masters at version 1) stays as dated, owner-reported history. A Windows baseline at the
  current state does not exist yet; T017 takes it (section 10).
- **The fixes (tests only, with one line-list change; in the package; never a refreshed hash, never an allowed skip).**
  - The two reader tests keep what they prove, on fixtures they build themselves: (1) a synthetic INIT master with its
    own ledger and INIT record, whose hash the test computes from the bytes it wrote, plus a check with no pinned
    value that the real masters pass the installed version-2 chain and prefix rules
    (`master_versions.load_verified_source`), which stays true after every update; (2) the boundary refusals on a
    synthetic unopened game, and a new positive test that an opened game admits them only under the gates.
  - The package's `.gitignore` drops the two commented-out `scores/` lines and their out-of-date comments, and adds the
    weekly lines; the test's list is changed to match, and gains a check that neither `scores/` folder is ignored.
  - Mutation checks plant "accept any hash", "admit before opening" and "ignore the scores again", and show the
    rewritten tests catch each.
- **In the package's suite runner** the expected count per module comes from the tools. T017 records the before state
  (exactly these three failures) and the after state (none).

## 4. The package: files, by layer

New files are marked N; edited files E. Names are proposals. Every new program is run only by the owner through its
launcher, and joins the rulebook's rule 7 and the owner's deny patterns (section 11).

| Layer | File | | What it holds |
|---|---|---|---|
| L1 | `src/methods/_common/contract_vocab.py` | E | `CATCH_UP` run mode and tier; `FINAL_NEXT_DRAW` unreserved; two `producible` rows; binding kind `DEV_BATCH` (L6) |
| L1 | `src/methods/_common/contract_records.py`, `contract_task.py`, `contract_runner.py`, `Method_Contract_Runner.py` | E | the mode, target and binding table with `DEV_BATCH`; the mode-to-pin rule (CF-2); the three `'CATCH_UP'` special cases folded into the vocabulary |
| L1, L6 | `src/methods/_common/contract_dispatch.py` | E | the `DEV_BATCH` branch (section 5, L6); the session branch re-read against Appendix E, changed only if a matrix cell fails |
| L2 | `src/methods/_common/jsonl_ledger.py` | N | the one append discipline (Des 6.5): whole line, flush, fsync; torn last line kept as a side file; the digest chain and its verifier |
| L2 | `src/methods/_common/weekly_records.py` | N | full validators for `SESSION_V1` and `FREEZE_LINE_V1`; the deadline; the effective class (Appendix I) as one pure function |
| L2, L6 | `src/methods/_common/score_identities.py` | N | identities-only readers of score records: which records are scored (CF-9), and which keys the league's canonical sources already cover (for a routine fill) |
| L2 | `src/methods/_common/weekly_session.py`, `src/methods/Method_Weekly_Forecast.py` | N | `status`, `open-session` (and `--resume`), `next`, `close-session`; the state machine of Appendix F |
| L3 | `src/evaluation/weekly_score.py`, `src/evaluation/Method_Weekly_Score.py` | N | `score`, `witness`, `verify`, `diagnostic-score`; the score and witness ledgers |
| L3, L6 | `src/evaluation/outcome_reader.py` | E | the weekly freeze-line release rule and the post-seal development rule (CF-4) |
| L4 | `src/evaluation/league_sources.py` | N | the three read-only adapters; the reader of `LEAGUE_SOURCES_<GAME>.json`; the one-score rule; correction chains |
| L4 | `src/evaluation/league_table.py` | N | rows, columns, order, labels: pure functions from adapter output to the `.txt` and `.csv` bytes |
| L4 | `src/evaluation/league_publish.py`, `src/evaluation/Method_League_Table.py` | N | the one league writer: the publication (manifest, archive, `WEEKLY_TABLE` row, `current`) and the admission of a source; `publish`, `repair`, `history`, `reconstruction`, `admit`, `sources-check` |
| L5 | `src/evaluation/ov1_numeric.py` | N | the integer kernel: directed fixed-point arithmetic, `exp` and `log` enclosures (section 6) |
| L5 | `src/evaluation/ov1.py`, `src/evaluation/Method_OV1.py` | N | weights, exact distribution (two routes), the sealed factor table and certificate, the registration, the ledger lines, the stream's state; `register`, `record`, `stop`, `status`, `verify` |
| L5, L7 | `src/evaluation/registry/MEASURE_REGISTRY_V1.json` | E | OV-1's entry and its label; the `CATCH_UP` tier (as MHUP-A added the Mode H families to the family registry) |
| L6 | `src/methods/_common/walk_forward.py`, `src/methods/Method_Walk_Forward.py` | E | plan schema `WF_BATCH_PLAN_V2`: its kind (`ROUTINE_FILL` or `EXPLORATORY_RERUN`), explicit pairs, tickets, the `DEV_BATCH` binding; version-1 plans untouched |
| L6 | `src/evaluation/report.py`, `Method_Rankings_Report.py`, `report_writer.py` | E | the window contract; the tier filter on families (CF-5); V2 batches reported on their own pairs |
| L6 | `src/evaluation/reforecast_compare.py` | N | named forecast content compared: a re-forecast with a sealed forecast (Sup 7.2 rule 7), and one attempt with another |
| L7 | `src/evaluation/consolidated_report.py`, `src/evaluation/Method_Weekly_Report.py` | N | the full report from named sources; the retired-revision index |
| L8 | `src/sequencer_children.py`, `src/Weekly_Session_Orchestrator.py`, `src/Development_Batch_Orchestrator.py` | N | the child launcher both sequencers share (Des 6.1's rules), and the two sequences |
| L8 | `Run_Weekly_Session.bat`, `Run_Development_Batch.bat`, `.gitignore` | N, E | the two owner commands; the ignore list (section 3) |
| L8 | `tests/test_mhupb_*.py` (about fifteen modules), `tests/test_multigame_reader_contracts.py`, `tests/test_mhupa_launchers.py`, `tests/test_wf1b_static.py`, `tests/test_mhupa_updater_v0_2.py` | N, E | section 5's tests; the three baseline fixes; the static allowances; the page-order cases |
| L8 | the package: manifest, verifier, copy tool, suite runner, install instructions, mutation tools, `TASK_T017.md` | N | Appendix J without barrier E; two commits; a release record with an empty entry list |

**The order of building, and the review slices (DECIDED: OD-6, entry 69).** Slice 1 = the baseline fixes, L1, L2, L3 (the
live path); slice 2 = L5 and L6; slice 3 = L4, L7, L8; then the integrated package, reviewed as a whole, then T017. The
slices are the reviewer's technical checks. They are not owner ratifications, and nothing is installed before the
integrated package passes. An ordinary fix inside the ratified plan goes back to the reviewer, not to the owner; a
change to a binding rule or gate still goes to him.

## 5. Layer by layer

### L1. Modes and gates

- `CATCH_UP / FORECAST -> (WF_FORECAST, CATCH_UP)`; `FINAL_NEXT_DRAW / FORECAST -> (WF_FORECAST, PROSPECTIVE)`. Both
  stay refused unless ticketed, session-bound and under the developed record: the dispatch gate decides, as now.
- The mode-to-pin rule, in `contract_runner` after the reader has resolved the pin: `FINAL_NEXT_DRAW` only for
  `last_draw(v) + 1`; `CATCH_UP`, a session-bound `REAL_DEVELOPMENT` and a `DEV_BATCH` run only for targets at most
  `last_draw(v)`; the diagnostic route at most `last_draw(v)` (Des 3.4(b)).
- **Gate:** a table-driven test that walks every row of Appendix E across stages S0 to S5 and X on a synthetic project
  and asserts each cell (published, or refused with its code, with no byte written). The table in the test is typed in
  from Appendix E and cross-checked by a second, independently written "what should happen" function (R-4). The
  mode-to-pin rule has its own negative cases for `REAL_DEVELOPMENT`, `CATCH_UP` and `FINAL_NEXT_DRAW` at
  `last_draw(v)`, at `last_draw(v) + 1` and beyond, and T-05 shows that no admitted combination changes a
  method-facing byte (EX_223 CP-Q9).
- **Unchanged and proved unchanged:** every existing digest and golden; a forecast made in each real mode on the same
  invented prefix has the same content digest, ranking and tie order (Des 3.3).

### L2. The forecasting half

- **Session:** `open-session` writes `SESSION_<id>.json` create-only (game, time, pin = the ledger's last row, the
  developed record's digest, the closure and environment digests, the roster from `release_records.released_variants`
  with each variant's release date) and takes the lock; refuses while the session lock or the updater lock exists.
  `--resume` needs a fresh, unused resume token and unchanged digests, and records a `RESUMED` ticket.
- **`next`:** exactly Appendix F: `STALE`; else the lowest unclosed accepted target N (complete its set, write its freeze
  line, `FROZE N`); else M = `last_draw + 1`: `OPEN M`, or complete a `SET_STARTED` set, or start one if at least an
  hour remains (the `SET_STARTED` ticket is the one persisted judgement), else `NONE`. The order is enforced inside
  `next`, so a faulty orchestrator cannot skip a step.
- **The freeze line** (Des 6.5): target and date; writing session; freeze time and local offset; deadline and
  `deadline_met`; per named record its identity, session and that session record's digest, run mode, DONE ticket,
  digest, training pin and `frozen_at_utc`; `PREDICTION_FAILED` and `MISSING_BATCH` marks; the non-runnable methods; the
  environment digest; the previous line's digest. No witness or publication status. A line's freeze time is never
  earlier than the line before it: the writer refuses to append if the clock is behind (Sup v0.8 6.8 relies on it).
- **Reading "scored" (CF-9; EX_223 CP-Q5).** `score_identities.scored_identities` gives the forecasting half only the
  target, the scored record's digest, the policy id and whether every record a freeze line names has its routine score
  line. A target is closed only by score lines that carry the digests of the records its own freeze line names: a
  foreign, malformed or duplicated score identity refuses, and never closes a target. It exposes no match count,
  ranking, score or outcome, imports nothing from the evaluator, and a static test shows the forecasting half reads
  the score ledger nowhere else. A taint test plants a marker in every outcome-derived field of a score ledger and
  shows it reaches no run request, task or view.
- **The deadline:** 00:00 local on the draw's date from the PC clock and time zone, stored as the UTC instant and the
  offset (Des 6.4; decided with MHUP-R). The clock is one module-level function, patched only by the test harness.
- **Uncertainty to measure, not assume:** Des 6.1 has every `next` re-check the closure and environment digests. The
  environment digest hashes the whole venv. T017 measures its cost on the owner's PC. If it is too slow for a
  catch-up of several draws, that is a design amendment to propose, not a quiet shortcut.
- **Gates:** Appendix F's states with an interruption injected after every write (ticket, run record, DONE ticket,
  freeze line), each resumed under the same session and, separately, by a successor session after a cleared lock;
  zero re-runs of a pair with a DONE ticket; the chain broken by an edit, a removal and a reorder; the hour rule and
  the deadline; a straddling set classified record by record; `MISSING_BATCH` only for eligible variants; the L-R
  roster cases (a variant added after three scored draws, added or retired while a forecast is open, E_1 revised).
  Oracles (R-4): an independently written chain checker, and an independently written roster-closure checker that,
  given lines, tickets and score identities, says which targets are closed (Des Appendix L).

### L3. The scoring half

- **`score --target N`:** the cross-session check of Des 6.3 for every named record; then the release rule; then the
  outcome read once; one score line per named record that has none.
- **The weekly release rule** (new text in `outcome_release_allowed`; fixed evidence paths; no caller-chosen input): a
  target above `holdout_last` is released only if the game's developed record exists, the forecast ledger holds a
  freeze line for it, every record that line names verifies (session record and digest, DONE ticket, digest), and the
  target is at most `last_draw` of the scoring session's pin. Anything absent or invalid refuses.
- **The score line** (Des 6.6): the scientific identity (game, method, revision, variant, target, scored record's
  digest, scoring policy id), which is the duplicate guard; the execution provenance (score run id, scorer version,
  scoring session, outcome pin); TOP and WORST matches, Powerball match, division, rank positions, computed by the
  installed WF-1B functions (`divisions.match_record`, `measures.mr5_target_fields`), unchanged; training pin; tier;
  `frozen_at_utc`; effective class; exposure flag (`EXPOSED_DRAWS`; Powerball 1587 and 1588 carry HX-2); the drawn
  numbers, as the WF-1B score record holds them; and whether the draw's date in the master is its derived date (OV-1
  stops on a draw that is off the weekly rule, Sup v0.8 6.8).
- **Corrections:** the line format carries `amendment_of`. This package writes no corrective score (no corrected scorer
  exists); it only reads them correctly (L4).
- **Gates:** a second routine score for the same scientific identity under another score run id refuses (L-S1); a
  fixture amendment stands beside the old line, which stays byte-identical (L-S2); an S1 line scored by S2 at a grown
  master records both pins (L-W2); a crash mid-score resumes with the unscored records only; no freeze line, no score;
  `diagnostic-score` writes no ledger byte (L-G3); the witness cases L-V1 to L-V3; a static test that no routine command
  touches the network.

### L4. The league table

- **Sources** (Sup 4), each through its own read-only adapter that returns the same small row shape (key, hits, class,
  source identity, exposure flag): (a) the weekly score ledger; (b) the development score ledgers of the canonical
  attempts listed in `LEAGUE_SOURCES_<GAME>.json`; (c) the sealed Mode H ledger, shown and never summed, read only if
  its SHA-256 equals the one in its `SCORE_COMPLETE` record.
- **`LEAGUE_SOURCES_<GAME>.json` is one small tracked file** (Sup v0.8 4 rule 5; EX_223 C03), at
  `results/method_rankings/<GAME>/league/`. It lists the canonical development attempts, each by attempt identity,
  batch, kind, the digest of its score ledger and the keys' scope. There is no chain of versions: Git keeps its
  history, and every published table names the file's digest and the exact sources it used. It is written only by
  the admission step below, by an atomic replace of the whole file. The owner never edits it.
- **Admission is deterministic and part of the job that made the attempt** (Sup v0.8 4 rule 2A). `admit` adds a
  routine-fill attempt, or a report attempt over a version-1 batch, only if its report completed and none of its keys
  is already supplied by a canonical source or by the weekly score ledger. Otherwise it refuses, names the first conflicting key, and changes nothing. A repeat for exactly the
  attempt already listed, with the same score-ledger digest, keys' scope and scoring policy, succeeds and changes nothing
  (the file is not rewritten), so the job goes on to publish; the same identity with any difference refuses (EX_225
  RC-225-2). An
  exploratory attempt is never admitted. So the canonical score of a key is the first one admitted, never the newest
  or the best. The two existing attempts (`rr-4be324ab...` for Oz Lotto, `rr-97bb4861...` for Powerball) are admitted
  the same way at the first use after the install. Replacing a canonical source is not provided: it would be a
  reviewed, named change on the owner's decision.
- **The one-score rule:** key (game, method, revision, variant, target, barrel, TOP or WORST); the scoring policy is not
  in the key. Two canonical sources with the same key and no named selection: refuse, naming the key. A correction
  chain that branches, cycles or has two heads: refuse. A listed source absent or failing its identity: "not
  available: <source>" for the affected variants, never a partial total shown as a total.
- **The table** (Sup 3): every released variant; `NO_SCORES`; `LOW_N` under 30; all scored draws (no P value); forward
  only with the witness-verified count beside it; last 10; the second table by kind with "Mode H as sealed"; WORST;
  the Powerball barrel; divisions; revision, release date, first and last scored target, missing and failed counts;
  the order by hits above chance per draw as an exact fraction, ties by identity; the fixed header sentences; the
  exposure flags HX-1 and HX-2 wherever a flagged draw is scored, from the recorded source, changing no figure
  (EX_223 CP-Q8).
- **Publishing, made crash-consistent** (Sup v0.8 5.1; EX_223 B02). One publication has one identity: game, version,
  latest draw and time stamp, which are its file names.
  1. Build both members' bytes in memory and check them.
  2. Create the publication's manifest in the archive, create-only: the identity; both members' digests; and every
     input pinned so the bytes can be rebuilt exactly (the source file's digest and entries, each ledger's verified
     length and digest, the forecast ledger's included, the roster with release dates).
  3. Create the two archive members, create-only.
  4. Append the `WEEKLY_TABLE` search-log row, naming the manifest. **The row is written last, so a row always points
     at a complete, verified set.**
  5. Refresh `current`: new copies under temporary names, verified against the archive; a `CURRENT_COPY_INCOMPLETE`
     notice placed; the old copies replaced; the notice removed last.
  Every `publish` and `repair` first looks for a manifest with no row. It rebuilds that publication from the manifest's
  pinned inputs; if the bytes equal the manifest's digests it creates whatever member is missing and appends the row
  (the same bytes, the same identity). If they cannot be rebuilt identically it writes a create-only
  `PUBLICATION_INCOMPLETE` note beside the manifest, reports it, and never logs that publication. Nothing in the
  archive is overwritten or deleted, no logged path ever lacks its files, and version numbers come from the manifests,
  so none is reused. A failed `current` copy is repaired from the archive. A `publish` whose pinned inputs equal those of
  the latest logged publication writes nothing and reports the table as up to date, so a rerun after a crash that
  followed the row never makes a second publication; and before appending a row the writer checks that no row already
  names the manifest (EX_225 RC-225-2).
- **Who starts and who writes** (Sup v0.8 4 rule 4; EX_223 C01). A publication is started only by `Method_League_Table.py
  publish`, which the weekly and development sequencers run and the owner may run on its own. Whoever starts it, the
  same writer runs the same five steps, so no publication can exist without its row. `league_sources.py` and
  `league_table.py` open nothing for writing (a static test); `league_publish.py` is the only writer of the table
  files, the manifest, the `WEEKLY_TABLE` row and the source file. A test drives both entry points.
- **Exploratory attempts** appear only in a separate, labelled comparison (by named attempt, beside the canonical
  figure for the same keys), never in a canonical column or total.
- **Gates:** each refusal and each degraded case of Sup 4 once; the adapters on writer-made records and on the real
  committed ones (section 8); an interruption before and after every durable step of a publication and of the
  `current` copy (section 9); a manifest whose inputs have changed is marked incomplete, not finished wrongly; a
  repeated `admit` of the same attempt changes no byte, and the same identity with different bytes or scope refuses;
  crashes before and after admission, between admission and publication, after the row and during the `current`
  repair, each ending with exactly one canonical score per key and one row per publication; a torn or duplicated
  search-log row;
  admission refused on an overlapping key, with the file byte-identical; a repeated attempt for a covered key never
  counted; the history report recomputes nothing; every reconstruction row carries its label and the "released at
  that date" column.

### L5. OV-1 (section 6 has the arithmetic; Sup v0.8 6.5 and 6.8 have the rules)

- **The registration** (`register --game G --statement "..."`, owner-run, create-only, one per game, a search-log row):
  the game; the first eligible target T0 = `last_draw + 1` at that moment, which must have no freeze line and a
  deadline still ahead; the formula; the six lambdas as exact fractions with equal weights; the bar 40; the pair rule
  and the V = 0 rule; the opportunity rule and the cut-off; the owner's statement that both games close at 7.30pm
  AEST; the scoring policy whose lines are read; the kernel's precision, margin and version; the error budget (this
  game's 2.5% of the programme's 5%, and RC-1). It refuses without the developed record. **No command makes a second
  registration for a game, and none recovers a stopped stream (OD-4).**
- **The cut-off** C(T) is 01:30 UTC on T's derived draw date: noon in Adelaide in daylight time, 11:00 in standard time,
  eight hours before 7.30pm AEST. It is a fixed instant, so the code has no time-zone rule to get wrong. A test checks,
  for every Tuesday and Thursday to the end of 2045, that it is 11:00 or 12:00 in Adelaide on the same date and never
  after noon. It moves no forecast deadline: a ticket counts only if frozen before midnight (Des 6.4).
- **The ledger** (`OV1_LEDGER_<GAME>_V1.jsonl`, tracked, chained from the registration's digest), four kinds of line:
  - *eligibility*, for a target with a pre-cut-off freeze line: the registration's identity, the freeze line's digest,
    the eligible variants (count and digest), the weight of every number, V as an exact fraction, whether the draw is
    a V = 0 skip, the digest of the sealed factor table with its certificate result, the time, and the master pin then
    in force;
  - *factor*: the eligibility line's digest, the outcome pin copied from the score lines, X, Z to a fixed number of
    digits for display, the six stored log-factors as exact fixed-point integers, the six running sums, the proved
    lower bound of the score, and `crossed`;
  - *missed* (`MISSED_NO_FREEZE`), for a target with no pre-cut-off freeze line: written after C(T), from the forecast
    ledger once its chain verifies and it reconciles with every earlier record (6.6), naming that ledger's length and
    digest as read, and labelled as recorded after the cut-off from local records;
  - *stop*: the target and the cause.
- **One idempotent command, `record --game G`,** run by the sequencer after every `score` and after the loop, and safe
  for the owner to run again at any time. It takes the targets from T0 in order and writes whatever is due, nothing
  twice and nothing out of order: an eligibility line (before C(T) only); a missed line (after C(T) only); a factor
  line once the eligibility line and the eligible variants' score lines are there; a stop line. It reads the frozen
  tickets, the forecast ledger and the score ledger, and never the master. A failure of `record` never changes the
  live path's exit. It is the one writer of this ledger (EX_223 C01).
- **`stop --game G --statement "..."`** records an owner stop (the operator's schedule changed). **`verify`** rebuilds
  every line from the eligibility lines, the forecast ledger and the score ledger and compares bytes. A later kernel
  version must reproduce a frozen fixture ledger byte for byte, or it is a reviewed amendment.
- **Gates** (Sup 2 row L5; Sup v0.8 14): section 6's; every target classified as counted, skipped, missed or a stop from
  the records alone, with the cut-off tested one second before, at, and one second after; a missed line refused, and
  the target blocked, when the forecast ledger is torn, truncated or replaced, its chain is broken, its times run
  backwards or lie after the recorder's clock, or it conflicts with an extent or freeze-line digest named earlier in
  the OV-1 ledger, the witness ledger or a publication manifest (EX_225 RC-225-1); a freeze line appended after the
  cut-off never
  counted; incomplete pairs excluded; changing rosters and history-dependent weights; an interruption exactly between
  the freeze line and the eligibility line, resumed before and after the cut-off; each stop cause of 6.6 planted
  once, with no factor line after it; restart giving the same bytes; no OV-1 figure for a holdout, catch-up or
  development draw in the formal stream (Sup 6.7).

### L6. The window contract and the two kinds of development run (always-review: holdout access, N-1)

- **A second plan schema, `WF_BATCH_PLAN_V2`,** beside the first, which is left exactly as it is. A V2 plan fixes its
  kind, its cohort and its explicit (variant, target) pairs; its runs carry tickets (`TICKET_V1`, scope `DEV_BATCH`)
  and a `DEV_BATCH` binding, and publish under the development run root only. Both kinds go through the same driver,
  the same gate, the same N-1 isolation and the same record contracts (Sup v0.8 7.1A; EX_223 B04).
  - **`ROUTINE_FILL`:** the driver works out the pairs itself: for every released variant, its eligible targets that no
    canonical source covers (`score_identities.canonical_coverage`, identities only). Eligible means the game's first
    target to `holdout_last` (after the seal), and, above the holdout, only the targets of rule 2A. The owner names
    nothing but the game.
  - **`EXPLORATORY_RERUN`:** the owner names the variants (or the whole released cohort) and the window. Any target up
    to `holdout_last` (after the seal) and any later accepted target that already has a weekly freeze line may be
    included, whether or not it was scored before.
- **The `DEV_BATCH` branch of the dispatch gate** (value-free records, fixed roots): the plan exists with that digest
  and its search-log row and lists the pair; the request pins the plan's pin; an open ticket, and no DONE ticket for
  the pair in the batch; for a target at or above `holdout_first`, the opening record and the game's `MODE_H_SEALED`
  (Sup 7.2 rules 1 and 2); for a target above `holdout_last`, a weekly freeze line for the target must exist, and
  - for a routine fill (rule 2A as amended, EX_223 B03): that freeze line's time is before the variant's release
    instant (`released_utc` of its release record), the line does not name the variant, and no session ledger holds a
    ticket for the pair;
  - for an exploratory rerun: nothing more.
  A target that is still open in the weekly session is never a batch's.
- **The report tool:** a V2 batch is reported on its own pairs; the window may reach `holdout_last` once the seal exists,
  and the targets above it that the plan lists; the outcome reader releases those draws to a development report only
  under the same conditions, after the search-log row and the scoring plan are written (the existing order,
  unchanged); families are loaded by window **and tier** (CF-5); every table of a V2 report is `EXPLORATORY_COHORT`.
- **After the report:** a routine fill's attempt is admitted (L4) and the league table is published. An exploratory
  rerun's report carries the comparison with the canonical figures for the same keys, and with any named earlier
  attempt, and changes nothing else.
- **The comparison with the sealed forecasts** (Sup 7.2 rule 7), as a section of the batch's report: for each pair, the
  preconditions and whether each holds; the ranking with scores and ties, and the TOP and WORST sets, compared; every
  difference listed with the inputs' identities. It reads the sealed run folders and writes nothing under any sealed
  path.
- **Gates:** no write under any sealed Mode H path and no freeze line or weekly ledger touched (a test snapshots every
  such file's bytes before and after each L6 command); every refused window refuses, including a holdout target
  before the seal, a routine-fill target with a weekly ticket, and the same-day cases of rule 2A (frozen before the
  release instant: admitted; frozen after it: refused; across a daylight-saving change); every forecast's tier is
  development; T-05 on the extended windows; a repeated run of a covered key is a separate attempt, is never summed,
  and never becomes canonical; a retired revision is not runnable; the two kinds give identical forecast content for
  the same pair, pin and revision.

### L7. The consolidated report and the retired index

- Parts, each from named sources by identity, none pooled into a P value (Sup 8): the league table; OV-1; the forward and
  catch-up family tables; the matched-target view (R3 17.3.7); the development and Mode H results quoted from their own
  reports, not recomputed; each with a `WEEKLY_REPORT` search-log row.
- **Labels for the forward and catch-up family tables (EX_223 CP-Q4: accepted, with this precision).** Their window and
  roster grow from report to report, so they are not a family fixed in advance: `EXPLORATORY_COHORT`, under the
  heading "secondary". `BONFERRONI_REFERENCE_UNCALIBRATED` is put only on Bonferroni arithmetic whose prerequisites
  actually fail (the family, the fixed grid or an input's validity). Local figures keep their own labels and `LOW_N`;
  catch-up stays apart from the prospective column; the sealed Mode H report's own calibration is quoted, not redone.
  No confirmatory family is made from a secondary table. No new label is invented.
- **Gates:** every figure traceable to a source identity; a test that searches the report's text, CSV and JSON for any
  pooled or joint figure and finds none; the retired index lists each retired revision once.

### L8. The two sequencers, their launchers and the rest

- **Both are sequencers in the sense of Des 6.1, not coordinators.** They import neither `methods` nor `evaluation`,
  start each child through its launcher, read its output to the end, stop on a non-zero exit, hold no state, and never
  terminate, poll or look up a process. They share one small child-launching module, so the rules are written once.
- **`Run_Weekly_Session.bat --game G`** (Des Appendix F, with the supplement's additions): status; open or resume; the
  loop of `next` and `score`, with OV-1's `record` after each score; on `FROZE_NEXT`, `record` at once; `close-session`;
  then, and only then, the league table's `publish` (which first repairs any unfinished publication); the status
  block.
- **`Run_Development_Batch.bat --game G --fill`**, or **`--rerun --variants ... --first S --last L`** (new; EX_223 C04):
  plan; run; report; then for a fill, `admit` and `publish`. A third form, `--report --batch B --first S --last L`,
  scores forecasts an existing batch already holds, then `admit` and `publish`: it is how the Powerball 1145-1285
  scores of O-4 are made, with no forecast run again. That form uses only an authorised batch at its own pin and the
  accepted outcome reader, never changes the batch's forecasts, refuses any key a canonical source already supplies,
  and is tested with a version-1 batch and a version-2 batch (EX_225 R-5); running it for O-4 still needs its own go.
  Rerunning the command with the batch it printed continues from the records alone: an unfinished batch is run on, a
  batch without a report is reported, an unadmitted attempt is admitted, an admitted one is not admitted again (L4),
  and an unpublished table is published. It opens no weekly record. It is a new launch interface, so the Architecture's next edition names it
  beside the weekly one.
- **Exit statuses, distinct:** 0 complete; one value for "frozen; table not written"; one for "frozen; OV-1 recorder
  failed"; another for a stop of the live path or of a batch, naming the child. A failure after `close-session` never
  reopens, undoes or delays anything before it. Every stop prints what to do next in plain words.
- **Static tests:** neither sequencer imports `methods` or `evaluation`, or has `terminate`, `kill`, `taskkill`, psutil,
  signal, PID or timer; no module of L1 to L3 imports a module of L4 to L7 (the list of both sets is in the test, and
  a new file in `src/` that is in neither list fails the test).

## 6. OV-1's numerical contract (Sup 6.5; EX_209 B02; EX_211 F02; EX_219 C1)

**6.1 What must be true.** The stored factor is never above the true factor; the six running components, the mixture
and the comparison with 40 are proved lower bounds; if a bound cannot be established the program refuses.

**6.2 The method: whole numbers only, rounding always against a crossing.**
- Every real number is an integer n meaning n / 10^50. Lower bounds round down and upper bounds round up; Python's
  integer `//` is an exact floor, so each rounding direction is exact. No float and no `decimal` call is on the path,
  so the bytes are the same on every platform and Python version.
- The fair-draw distribution of X is exact integer counts (a dynamic programme), divided by C(N, 7).
- `sqrt(V)`, `exp` and `log` are *enclosed*: each returns a lower and an upper end. `exp` uses a Taylor series on a
  reduced argument with its remainder term added to the upper end; `log` uses `2 atanh((m-1)/(m+1))` with its
  remainder. A proved bound keeps the arguments in range: for any weights that sum to zero,
  |Z| <= sqrt(N(N-1)/(N-K)), which is below 6.52 for Powerball and below 7.36 for Oz Lotto (Cauchy-Schwarz on the
  seven drawn weights), so |lambda Z| < 1.48 and the mean of exp(lambda Z) is between 1 and 4.4.
- For the observed X: `l_lo` = (lower end of lambda Z) - (upper end of log E0[exp(lambda Z)]). The stored log-factor is
  `l_lo - 10^-30`. The program checks that the enclosure is narrower than 10^-30 and refuses otherwise. So stored <=
  true, and true - stored < 2 x 10^-30. (This is Sup 6.5's "lowered by a fixed safety margin larger than the error
  bound", with the bound checked at run time.)
- **The running sums are exact integer sums of the stored log-factors.** Nothing is rounded when draws accumulate, so the
  guarantee does not weaken with the number of draws: after n draws each running log is below its true value by at
  most n x 2 x 10^-30.
- **The crossing rule in integers:** a crossing is declared only if the sum over the six lambdas of the lower end of
  exp(running log) is at least 240 x 10^50 (that is 6 x 40). There is no division and no rounding in the comparison.

**6.3 A second, independent guarantee, checked on every draw (the certificate).** For each lambda, the program adds up,
over every possible value x of X, count(x) times the *upper* end of exp(stored log-factor at x), and checks in exact
integers that the total is at most C(N, 7) x 10^50. In words: the stored factors themselves have a fair-draw mean of at
most 1. That makes the stored process a nonnegative supermartingale under fair draws in its own right, so Ville's
inequality applies to what the software stores, even if the derivation of 6.2 had an error. The trusted core is then
small: the exact counts and one function, the upper end of `exp`. The certificate is a hard refusal (EX_223 CP-Q2),
and it is separate from the pointwise claim of 6.2, which has its own proof.

**It is computed and sealed before the outcome (EX_223 C02).** The certificate depends on the weights alone, not on the
drawn numbers. So the whole factor table of a draw (every possible X, each lambda) is built and certified when the
eligibility line is written, and its digest goes into that line. If it cannot be built and certified then, no
eligibility line is written, and that is decided before the result exists. At scoring the table is rebuilt, must equal
the sealed digest, and the factor line only looks up the observed X.

**6.4 What the probe shows** (`ov1_lower_bound_probe.py`; invented weights and fair draws; its output is in the
evidence folder):
- the `exp` and `log` enclosures contain the 90-digit `decimal` value in 4,002 cases;
- the exact distribution by two independent algorithms agrees on eight full-size weight patterns, and with brute force
  over all 6,724,520 subsets (N = 35, two patterns) and all 62,891,499 subsets (N = 47, one pattern);
- for the reviewer's counterexample, a single variant, a heavily skewed roster, 40, 400 and 2,000 variants, in both
  games: the enclosure is about 10^-47 wide, the certificate holds, the stored value is below the 90-digit reference in
  every checked cell, and the largest true-minus-stored is 1.00 x 10^-30;
- one draw's six factor tables take 0.01 to 0.15 seconds for up to 40 variants and about 1.1 seconds for 400 or 2,000;
- over 300 fair draws with a different roster every draw, the exact running logs agree with a floating-point reference to
  2 x 10^-15 (the float's own rounding);
- at the bar: all six logs 10^-40 above log 40 cross, 10^-40 below do not; very negative logs give a lower bound of 0;
  exp(5000) is enclosed without overflow.

**6.5 What the code round must still prove** (the probe is not the implementation):
- the written proof of each enclosure's remainder bound, in the module's documentation, checked by the reviewer;
- an oracle for the kernel that shares no code with it: `fractions.Fraction` series with explicit remainders on a grid
  of arguments, and `decimal` at 90 digits as a third opinion;
- the exact distribution against brute force for both games at full size (evidence run), and against brute force on
  every small case in the unit tests; the variance formula as an exact identity;
- each factor's fair-draw mean: the certificate on adversarial weights (all zero; one variant; all variants identical;
  maximal skew; thousands of variants; weights at the proved |Z| bound);
- mutants, each caught by a named test: a rounding direction flipped in each primitive; the remainder term dropped; the
  margin dropped; the certificate skipped; the crossing compared on an upper bound; a float used anywhere (a static
  test bans `float`, `math.exp`, `math.log` and `decimal` in the kernel);
- restart: the ledger rebuilt from its eligibility lines and the score ledger equals the stored bytes;
- X rebuilt two ways from the fixed score identities (TOP minus WORST matches; the weights of the drawn numbers) and
  required to agree and to lie in the sealed table's support; a corrupt score line, a score line under another policy
  and an out-of-support X each planted once (EX_223 C02, CP-Q9);
- the probe's `decimal` checks are feasibility evidence only. The proofs are the written remainder bounds and the
  exact-fraction oracle (EX_223 CP-Q2).

**6.6 Failure semantics and the error budget (Sup v0.8 6.8; EX_219 C1; EX_223 B01, C02).**

| State | When | What the program does |
|---|---|---|
| Counted | a pre-cut-off freeze line and a valid eligibility line | applies the sealed factor at the observed X (1 if V = 0) |
| Missed | no pre-cut-off freeze line for the target | factor 1, a `MISSED_NO_FREEZE` line, written after the cut-off from the forecast ledger, verified and reconciled |
| Blocked | an input is not yet there or does not verify: the result not accepted; a score line not written; a ledger whose chain, times or reconciliation fail | writes nothing for that target or any later one; passes over nothing; resumes by itself when the input verifies |
| Stop | a pre-cut-off freeze line with no valid eligibility line at the cut-off (F01); an owner stop; or a contradiction about a counted target (below) | a stop line; no factor line for that target or any later one, ever |

- **The contradictions that stop the stream:** the factor table rebuilt at scoring is not the sealed one; X is outside
  the sealed table's support, or its two derivations disagree; an eligible variant's score line does not carry the
  frozen record's digest and the registered scoring policy; the draw's date in the master is not its derived date.
- **A failure is never a skip.** Only two things give a factor of 1: V = 0, decided on the eligibility line before the
  outcome, and `MISSED_NO_FREEZE`, fixed by what existed before the cut-off. A numerical refusal, a missing or
  corrupt score, a missing eligibility line or a broken ledger is never turned into either.
- **Why "missed" cannot see the result.** Whether a freeze line with a freeze time before C(T) exists is settled at
  C(T), eight hours before the result. A line appended later carries its own later time (the writer refuses a time
  earlier than the line before), so it can never become a pre-cut-off line. Skipping a draw by a rule that uses only
  information from before the draw keeps the score a fair-draw supermartingale, exactly as V = 0 does.
- **What that rests on (EX_225 RC-225-1; Sup v0.8 6.8).** Three operating assumptions, stated in the registration: the
  writers append as specified and nothing is later truncated, replaced or suppressed; the PC's clock and event order
  are trustworthy relative to the real cut-off (the trust the design already places in `PROSPECTIVE` and the deadline;
  the clock is no witness); no eligible freeze line is removed or hidden after the fact. A verified chain is local
  evidence that the lines agree; it does not prove when they were written or that the ledger was never replaced
  (design 6.5). So the recorder writes a missed line only after C(T), only from a ledger whose whole chain verifies,
  and only once the ledger reconciles with every earlier record that names part of it: each forecast-ledger extent
  and freeze-line digest named in the OV-1 ledger, the witness ledger or a publication manifest must be there
  unchanged, and no record may name a freeze line for T that the ledger lacks. Any failure, or a time after the
  recorder's clock, blocks the target; it is never turned into missed, because an absence of evidence is not
  evidence of absence. The missed line is labelled as recorded after the cut-off from local records, and is never
  presented as independent proof of absence or of timing. No owner step and no outside witness are needed.
- **Why a stop cannot manufacture a crossing.** A stop ends the stream at its last value and no later factor is ever
  applied, so every crossing the software can declare is a crossing of the whole registered process at that same
  draw. Stopping, for any reason and at any time, can only remove crossings. What would break the guarantee is
  passing over a draw and carrying on, and outside the missed rule the software never does that.
- **After a stop the stream stays stopped (OD-4).** No command registers again and none recovers. Nothing in the code
  spends, moves or reuses the stopped stream's 2.5%. A retry of `record` before the cut-off is ordinary operation, not
  a recovery. A new confirmatory test would be a new owner-approved design with a reviewed error-budget argument for
  the whole programme; this plan proposes none.
- **The two games** share no state. Each stored process is a nonnegative fair-draw supermartingale starting at 1, so
  each reaches 40 with chance at most 2.5%, and the two together at most 5% by the union bound.

## 7. Isolation of the live path (Sup 2; EX_213)

**Static:** the import test of L8. **Dynamic, by fault injection:** each test runs a whole session on a synthetic project
with one fault planted, then asserts that the session, attempts, forecast, witness and score ledgers and every run
record are byte-identical to the same session run without the fault, and that the sequencer's exit status is the
distinct reporting status.

| Fault planted | Where | Expected |
|---|---|---|
| The table formatter raises | L4 | live records identical; "frozen; table not written"; a later `publish` writes the table |
| An adapter meets a duplicate key, a branching correction chain, a missing source | L4 | the table refuses or degrades as Sup 4 says; live records identical |
| A crash after the manifest; after the first archive member; after both members and before the row | L4 | no row exists for that publication; the next `publish` or `repair` finishes it with the same bytes and identity, then appends the row |
| The same, with an input changed before the retry | L4 | `PUBLICATION_INCOMPLETE` beside the manifest; never logged; the next publication takes the next version |
| The `current` copy is interrupted at each step | L4 | `CURRENT_COPY_INCOMPLETE` present; archive intact; `repair` restores |
| `record` raises before the eligibility line; between eligibility and factor | L5 | the freeze line and scores identical; rerun before the cut-off writes the line; after it, the stop |
| The OV-1 ledger is unreadable or its chain is broken | L5 | `record` is blocked and writes nothing; live records identical |
| The report tool or `admit` fails on a V2 batch | L6 | no weekly record touched; the source file byte-identical |
| The consolidated report fails | L7 | nothing else changes |
| Every child of the reporting steps exits non-zero | L8 | the session is already closed; the lock is gone; the exit status is the reporting one |

## 8. The source schemas (EX_213; CF-7; OD-5)

- **The real records have been checked, once (OD-5, done).** The owner committed the development score records and the
  two Mode H score ledgers on 17 November 2026 (`cc665ce`). `score_census.py` read all ten files from the repository
  (its output is in the evidence folder):
  - every file is canonical JSON lines with no CR byte, and every (track, draw) key is unique;
  - both Mode H ledgers (1,200 lines each: 800 score, 400 rank) equal the SHA-256 in their `SCORE_COMPLETE` and
    `MODE_H_SEALED` markers;
  - every scoring plan's digest and attempt match its search-log row (rows 3, 4, 8 and 12);
  - the fields are exactly those the installed writers define: `POST_OUTCOME_SCORE_RECORD_V1` with one field set per
    game (and `exposure_flag` on the 160 Powerball Mode H lines for draws 1585 and 1586), and
    `RANK_POSITION_RECORD_V1`;
  - development coverage: Oz Lotto 1475-1693 (11,916 score lines), Powerball 1286-1576 (22,884); 80 tracks each;
    revisions 1 and 2 (CF-10).
  This need not be repeated. From now on both AIs can read the real records, so the adapters are tested on them.
- **The rule for the tests:** an adapter is tested against records made by the installed writer, never against a
  hand-written imitation: the tests run the real report tool (`report.run_report`) and the real Mode H scorer
  (`mode_h.score`) on invented masters and feed their ledgers to the adapters; and a second test reads the committed
  real ledgers through the adapters and checks counts and identities against the census. The two are kept apart:
  passing on writer-made fixtures is not the same claim as reading the real records (EX_223 CP-Q9).
- **The schemas the adapters rely on** are read from the writers and pinned in a test: the score record
  (`contract_receipts.validate_score_record`: `track_id`, `draw_number`, `method_revision`, `main_matches`,
  `powerball_match`, `division`, the two digests, `evaluator_version`, optional `exposure_flag`); the rank record; the
  scoring plan (`attempt_id`, `batch_id`, window, `selected_forecasts`); the Mode H ledger's name
  (`mode_h_score_ledger.jsonl`, score lines then rank lines) and its `SCORE_COMPLETE` marker (`score_ledger_sha256`,
  `lines`).

## 9. Interruption and restart (EX_213; EX_223 B02)

A harness runs a command with a fault injected after its k-th durable write, for every k, then reruns the command and
compares the final bytes with an uninterrupted run. Durable writes are counted by wrapping the one ledger appender and
the one create-only writer, so no step can be missed.

| Command | Points | Must hold after the rerun |
|---|---|---|
| `open-session` | record; lock | one session; resume needs a token |
| `next`, catch-up set | each OPEN ticket, run record, DONE ticket; the freeze line | no pair run twice; the line names every record with its own session |
| `next`, next-draw set | `SET_STARTED`; each ticket and record; the freeze line | completed under the same ticket; classes by each record's own time |
| `score` | each score line | no line twice; unscored records only |
| `record` (OV-1) | eligibility line; each factor line; missed line; stop line | same bytes; never a second line for a target; never out of order |
| `publish` | before and after: the manifest; each archive member; the `WEEKLY_TABLE` row; each step of the `current` copy | a row only for a complete set; the same publication finished with the same bytes, or marked incomplete; no version reused; a rerun after the row publishes nothing new and adds no row |
| `admit` | the source file's replacement | the old file or the new file, never a mixture; no key admitted twice; a repeat of the same attempt succeeds and changes no byte |
| V2 batch `run` | each ticket and record | as the Mode H batch today |
| either sequencer | between every pair of children | the rerun continues from the records alone |

Also: the torn last line in each ledger (ignored, reported, kept as a side file, completed by the next writer); `STALE`
mid-session; a cleared lock and a successor session; a resume token older than five minutes or used twice.

## 10. Windows gates and the install

- **Cloud, before sending:** the suite on Python 3.13 and a 3.15 build; every mutant caught; the install rehearsed in LF
  and CRLF clones with every negative stopping; `check_task_commands.py` on the task file; every count from the tools.
- **T017 on the owner's PC (one task file; one go; a tightly scoped rulebook allowance like section 2A, reviewed
  first):**
  1. the baseline at the base commit: the suite, expecting exactly the three failures of section 3;
  2. Appendix J steps 0 to 18 without barrier E, in a task clone, with the suite in `--shadow` mode at step 10;
  3. the whole suite again after step 18, in the post-release state (the owner's decision of 13 November 2026);
  4. the time taken by the closure and environment digests (L2's uncertainty);
  5. the launch chain from a Python parent on Windows: each sequencer starting `Run_Experiment.bat` and
     `Run_Evaluation.bat` children and reading their output to the end (Des 6.1);
  6. in the same task clone, a full dress rehearsal on invented masters and invented owner records, through the real
     launchers (EX_223 CP-Q6: accepted): two missed draws caught up; the next forecast frozen; OV-1's entry written;
     the table published; the reporting layer made to fail once and repaired; a routine fill and an exploratory
     rerun. It checks that no network is used and no process is terminated, that the lock is gone at the end, that the
     search log, archive and `current` recover, and that the live records are byte-identical with and without the
     reporting failure. It touches no real data and is not permission to run on real data.
- **The install:** Appendix J as amended (J-1 to J-4), two commits, a release record with an empty entry list. The
  package changes no roster, so it may install while a weekly set is unfinished (none exists). It changes `src/`, so
  Mode H's frozen closure no longer matches afterwards; that is expected, the studies are sealed and never rerun, and
  reading their records needs no closure check (section 2).
- **Before the install:** the owner's deny lines for the new programs in `.claude/settings.json` (his edit), and the
  rulebook edition.

## 11. Documents that travel with the package (each reviewed and ratified before it goes into `doc/`)

- **The supplement v0.8**, ratified with this plan, then committed into `doc/` beside v0.7.
- R3: 17.3.6 (the window contract); 17.3.9 (`CATCH_UP`; `LATE_PRE_DRAW`); 17.5.2 and the measure registry (OV-1, label
  "exact test martingale"); the league table and reconstruction as descriptive outputs.
- E2R-1: 9.1 and E2R-R41 (`CATCH_UP`); E2R-R44 (`FINAL_NEXT_DRAW`); the `DEV_BATCH` binding.
- The Architecture's next edition (the two sequencers and their launchers).
- A short amendment to the design naming the supplement; and a note beside the record of ER-6 that plans of the new
  kind may name their variants (Sup v0.8 7.1A).
- The runner's rulebook v0.6 (Sup 10): rule 4 withdrawn; rule 5 as read-only wording; rule 7 with the new programs; the
  T017 allowance. The owner's checklist, with the A7 recovery procedure (Des 7).
- `exchange/README.md` v0.6 (the write rules after RAT-34; EX_216 D3).

## 12. Decisions made, and what the recheck is asked

**The owner's directions (decision log entries 69 and 70). Their exact wording is Sup v0.8, for his ratification.**

| | Direction | Where |
|---|---|---|
| OD-1 | A: two kinds of development run, routine fill and exploratory rerun | L6; Sup v0.8 7.1A, 4 rule 2A |
| OD-2 | B, conditionally as the reviewer indicated: a missed week is a neutral factor fixed in advance; else stop | L5; 6.6; Sup v0.8 6.8 |
| OD-3 | B: noon Adelaide time as the last moment for OV-1's pre-draw entry; the owner states that both games close at 7.30pm AEST | L5; Sup v0.8 6.8 |
| OD-4 | A: a stopped stream stays stopped | 6.6; Sup v0.8 6.8 |
| OD-5 | The real score records checked before the install: done (`cc665ce`; section 8) | 8 |
| OD-6 | A: three technical review slices, one integrated review, one install | 4 |

**The reviewer's answers CP-Q1 to CP-Q9 are all adopted** (section 1A). CP-Q7's gap is closed by rule 2A as amended.

**Put to the focused recheck (the points where this plan went beyond the exact words of EX_223); EX_225's answers
follow the list:**
- **R-1. The cut-off as a fixed instant.** OD-3 says noon Adelaide time. Sup v0.8 6.8 fixes 01:30 UTC on the draw date,
  which is noon in daylight time and 11:00 in standard time: never later than Adelaide's noon, one hour stricter for
  about half the year, and free of any time-zone rule. Is that acceptable as the realisation of OD-3? The owner sees
  the same wording at ratification.
- **R-2. The opportunity rule and its two arguments** (Sup v0.8 6.8; plan 6.6): that "missed" is fixed before the
  outcome, with absence established only from a verified chain; and that a stop can only remove crossings.
- **R-3. The canonical rule:** the first admitted score of a key is the canonical one; routine fills are admitted by
  their own workflow when nothing conflicts; exploratory reruns never (Sup v0.8 4 rule 2A; plan L4).
- **R-4. The publication protocol** (plan L4): manifest first, the search-log row last, an unfinished publication
  finished with identical bytes or marked incomplete.
- **R-5. A second sequencer and launcher for development jobs** (plan L8), so that one go covers one bounded job. It is
  a new launch interface for the Architecture's next edition.
- **R-6. Anything in Sup v0.8's amended text that says more, or less, than EX_223 intended.**

**DECIDED (cited, not reopened):** per game, bar 40, no joint figure (entry 55); the eight layers and the isolation rule
(RAT-33); the deadline (MHUP-R); tickets for official runs (Q11); two commits per install; the full suite after step 18;
OD-1 to OD-6 as directions (entries 69, 70). **RECOMMENDED:** everything else in sections 4 to 10.

**EX_225's answers:** R-1 accepted, to be shown to the owner as a conservative choice, not an exact translation of
"noon Adelaide time" (Sup v0.8 13, O-5); R-2 the arithmetic and the stop argument passed, the evidence wording
corrected by RC-225-1; R-3 and R-4 accepted, with RC-225-2; R-5 accepted, with RC-225-2's restart behaviour and its
conditions (L8); R-6 passed, subject to the two corrections; the probe is never claimed to prove the production
software (6.5). **OPEN:** the reviewer's check of the two corrections; then the owner's ratification of this plan and
of Sup v0.8, together. Ratification authorises no code (entry 67).

## 12A. The three everyday jobs (EX_223 Appendix A, the operator experience test)

**1. A new method gets its history, and the all-method ranking is refreshed.** After the method's release package is
installed, the owner types one command per game, `Run_Development_Batch.bat --game G --fill`. The program works out which
(variant, draw) pairs have no canonical score, runs only those, scores them, admits them to the league's sources if
nothing conflicts, and publishes a new league table; the earlier table stays in the archive. One go covers all of it.
If something conflicts or fails, it stops, says what and why in plain words, and changes no table.

**2. A voluntary rerun of anything, for research.** The owner types
`Run_Development_Batch.bat --game G --rerun --variants ... --first S --last L` (or the whole cohort). The program runs
that as a new, separate attempt and writes a report that sets the rerun beside the canonical figures for the same
draws. The league table and its totals do not change. Draws that were once the Mode H holdout are allowed, as
development evidence; the sealed Mode H records are not touched.

**3. A weekly session after missed draws.** The owner runs the updater, then `Run_Weekly_Session.bat --game G`. It catches
up the missed draws oldest first (forecast, freeze, score), freezes the next draw's forecast if at least an hour
remains before midnight, makes OV-1's pre-draw entry, and publishes the league table. A missed week shows in the
formal test as "missed", not as a stop. If something genuinely fails, the status block says which typed stop it is and
what to do; the forecasts and scores already made are safe.

In none of the three does the owner edit a ledger, a hash, the source list or a version number.

| EX_223 Appendix A area | How this plan meets it |
|---|---|
| Historical walk-forward reruns | both kinds through one V2 driver; one canonical score per key (L6; L4) |
| Adding results to league tables | admission and publication are steps of the job; conflicts refuse (L4; L8) |
| Source-list versioning | one small tracked file, digest-bound to each publication; no extra chain (L4) |
| Owner approvals | one go per bounded job (section 13) |
| Three review slices | technical checks only (section 4) |
| OV-1 safeguards | kept and automated: the pre-draw entry, the sealed table, the certificate, the stop rules (L5; 6) |

## 13. Which gate belongs where

| Stage | What is judged | By whom |
|---|---|---|
| This plan's recheck | that B01-B04 and C01-C04 are met; R-1 to R-6; the kernel's method and proof plan; the release rules of CF-4; the `DEV_BATCH` gate; the fault and interruption matrices | the reviewer |
| Ratification | this plan and Sup v0.8, together | the owner |
| Implementation acceptance | the tests on both Pythons; mutants; the proofs written out; oracles reproduced (R-2, R-4); adapters on writer-made and on real records; the cloud rehearsals; T017's report read step by step | the reviewer, in three slices and one integrated review; Claude's evidence |

**The owner's gos, each covering one bounded job and all of its named steps (P1; EX_223 C04):**

| Go | Covers | How often |
|---|---|---|
| Start the code | the code round, to the integrated package | once |
| T017 | the baseline, the install rehearsal, both suites, the timings, the launch chain, the dress rehearsal | once (again only after a STOP) |
| The install | Appendix J's steps, both commits; his settings lines first | once |
| The documents | ratifying each amended document before it goes into `doc/` | once each |
| `declare-developed`; OV-1's registration | one per game | once each |
| A weekly session | the update, then for each game: catch-up, freeze, score, OV-1's entry, the table and any repair | his own deliberate weekly run is that week's go (R-018) |
| A development job | plan, run, report, and for a fill the admission and the new table | one per job he asks for |

A step outside a job's named scope, a retry after a STOP, and anything that changes a binding rule still need their
own go. The E2R-T12 run context is asked once for the cloud suite.

## 14. Not tested, uncertainties, alternatives

- **Not tested:** everything in the plan. The only things run were the existing suite (section 3), the probe (section
  6.4) and the census (section 8).
- **Size:** twenty new Python source files and two launchers, about twelve edited files, about fifteen new test
  modules. Larger than MHUP-A's code. v0.2 adds three source files to v0.1 (the identities reader, and the second
  sequencer with the shared child launcher) and removes the chain of source-list versions.
- **Uncertainties:** the cost of the environment digest at every `next`; the local time of midnight around a
  daylight-saving change for the forecast deadline (tested with fixed zones; the owner's zone is the one that
  matters; OV-1's cut-off no longer depends on it); the reviewer's view of R-1 to R-5.
- **Alternatives considered:**
  - `decimal` at high precision for OV-1, with a margin: shorter code, but it leans on a library's rounding of `exp` and
    `ln`, and on two implementations of `decimal` giving the same digits. Kept as a cross-check only.
  - Exact fractions throughout: no rounding to argue about, but the denominators grow without limit.
  - Reading X from the master in L5: rejected; the score lines already hold it (CF-8), and L5 then needs no outcome
    access at all.
  - Extending the first plan schema in place: rejected; committed version-1 plans must stay verifiable byte for byte.
  - Writing the eligibility line inside the forecasting half, in the same step as the freeze line: it would close the
    gap between the two, but L2 would then import L5, against the isolation rule.
  - A chain of numbered source-list versions (v0.1): dropped; Git and the publication manifests already give the
    history and the identity (EX_223 C03).
  - The search-log row before the archive files (v0.1): dropped; a crash could leave a permanent row with no files
    (EX_223 B02).
  - Noon by Adelaide's own clock: needs time-zone data and a rule for the daylight-saving change; the fixed instant is
    never later and has neither.
  - No second sequencer, the owner typing four commands per development job with identifiers copied by hand: fewer
    files, but exactly the administration the owner asked to avoid.
  - One big review instead of slices: fewer rounds, but faults in the live path would be found late.

End of v0.3.

