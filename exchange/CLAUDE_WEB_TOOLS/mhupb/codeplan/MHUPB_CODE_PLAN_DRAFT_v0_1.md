# MHUP-B code plan - DRAFT v0.1 (for the reviewer's review before any implementation code)

**Status: DRAFT, by the Claude web chat, 17 November 2026 (Adelaide). A plan only. It authorises nothing: no code, package,
task file, run, registration, re-forecast or install. No implementation code exists.** The owner authorised this plan on
17 November 2026 at 16:01 (decision log entry 64) on the condition that it is reviewed before any implementation code is
written.

**Authorities it stands on:** the ratified design `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`
("Des") sections 6 and 7 and Appendices E to L; the ratified supplement
`doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md` ("Sup"; RAT-33); register v0.31; H-1 v4; the approach of
16 November 2026 with EX_206's conditions; EX_213's code-round gates; EX_219's cautions C1 and C2. Where this plan and
those documents differ, they govern, and the difference is a fault in this plan.

**Base:** `main` at `b30919d`. No file under `src/`, `tests/`, no root `.bat` and no `requirements.txt` has changed since
`cc0ab73` (checked with `git diff`). **Risk tier:** HIGH (always-review subjects: N-1 boundaries, holdout access, freezing
and publication, TOP/WORST readout, the evaluator and scorer, launchers).

**Evidence with this plan** (folder `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/`): the baseline suite summaries; the OV-1
numerical probe `ov1_lower_bound_probe.py` and its output. The probe is a plan-stage feasibility tool on invented data,
not project code.

## 0. In plain English

- **What gets built.** One package, in the supplement's eight layers. Layers 1 to 3 are the weekly live path (catch up
  missed draws, freeze the next forecast, score). Layers 4 to 7 are reporting (the league table, the one formal test
  OV-1, back-history, the full report). Layer 8 is the one weekly command, the install and the documents.
- **A lot is already there.** MHUP-A installed most of the gates and record rules the weekly session needs. Section 2
  lists exactly what exists and what is missing. This makes layer 1 small.
- **Four things the installed code cannot yet do, which the plan must change with care** (section 2): it never checks that
  a next-draw forecast is really for the next draw; it refuses every development run and report on a holdout draw or
  later; it never releases a result after the holdout to any scorer; and a report over exactly the ten holdout draws
  would pick up the Mode H test families by accident.
- **The formal test's arithmetic can be made provably safe.** A probe shows the program can keep every figure as a whole
  number and always round against a crossing. The loss is about one part in 10^30 per draw. It also checks, for every
  draw, that the stored factors themselves average at most 1 under fair draws, so the guarantee holds for what is
  actually stored (section 6).
- **The test baseline is now measured, not assumed.** On current `main`, 570 of the 571 tests were run on Linux (one is
  left out because it starts worker processes). Exactly two tests fail, both in one file, both the expected ones tied
  to the old results files. The fix keeps what they test and never just updates a stored hash (section 3).
- **Six decisions are needed before code** (section 12): four for the owner, and several questions for the reviewer. The
  most important: what happens to the formal test if a week is missed, and whether a new method's back-history may run
  for that method alone (the owner declined that on 31 October in a different setting; the supplement now needs it).

## 1. Scope

**In scope** (Sup 2; Des 6, 7, 8): L1 `CATCH_UP` and `FINAL_NEXT_DRAW`; L2 the forecasting half, sessions, tickets, the
freeze line, the forecast and witness ledgers; L3 the scoring half and the score ledger; L4 the league table, its
sources, archive, `current` folder, history and reconstruction; L5 OV-1; L6 the window contract and back-history; L7 the
consolidated report and the retired-revision index; L8 the orchestrator, `Run_Weekly_Session.bat`, the owner's checklist
(with the A7 recovery procedure), the rulebook edition, the document amendments, the package and its rehearsal. Also: the
tests-only fix for the tests tied to the version-1 masters (readiness finding F-2), and the newest-first and shuffled
page cases for the updater's tests (register v0.31, future action 4; tests only).

**Not in scope:** any change to a released method, to the updater's code, to Mode H's sealed records or their writers; a
corrective-scoring writer (only the reader side of corrections: Sup 4 rule 2); result corrections (R3 10.3); WF-1C; the
coordinated path; a joint two-game figure (Sup 6.3: never computed); any new dependency.

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
  Decision log entry 58 also records the answer "only the new or changed variants are computed". This conflict is put
  to the owner as OD-1 (section 12).
- **CF-7. The development and Mode H score ledgers are git-ignored** (`.gitignore` lines for
  `results/real/development/scores/` and `results/real/holdout/scores/`): they exist only on the owner's PC. So "the
  adapters against the actual schemas" (EX_213) cannot be shown on real records from the repository. Section 8 says how.
- **CF-8. OV-1's X needs no outcome read.** X equals the sum, over the eligible variants, of TOP main matches minus
  WORST main matches, and those are in the score lines. So L5 reads the forecast ledger, the frozen tickets and the
  score ledger, and never the master (Sup 6.2 says X "needs only the scores already kept").
- **CF-9. `next` must know which records are scored** (Des 6.3 "closed"; Appendix F). The forecasting half is under
  `src/methods/`, and the score ledger holds match counts. Planned: one reader function in a shared record module that
  returns identities only (target, record digest, policy id), and a static test that the forecasting half reaches the
  score ledger through that function alone. Method code never sees it. Question CP-Q5.

## 3. The baseline on current `main` (EX_219 C2)

Run in the cloud workspace only, in a full disposable clone of `b30919d`, each module in its own process
(`python -B -m unittest -v`), without class `T12Determinism` (E2R-T12 starts worker processes; that run context was not
requested). Nothing was fixed, skipped or relabelled.

| Python | Modules | Tests run | Modules failing | Failing tests |
|---|---|---|---|---|
| 3.13.18 (Linux) | 45 | 570 | 1 | 2 |
| 3.15.0b4 (Linux, venv with the project's direct packages) | 45 | 570 | 1 | 2 (the same two) |

- **The two failures, both in `tests/test_multigame_reader_contracts.py`** (class `V011ReaderTests`):
  1. `test_master_source_and_ledger_file_hashes`: the two masters' SHA-256 values are compared with the version-1
     values written in the test; the masters are now version 2.
  2. `test_only_legacy_e1_allowed_at_boundary`: requests at the first holdout target that the test expects to be
     refused are no longer refused (five assertions), because the opening record now exists and the master holds
     that draw.
  Both are the failures H-1 v4 section 6 names (readiness finding F-2). **No unexpected failure.**
- **What this means for earlier evidence.** T024's "571 pass with 4 symlink skips" (14 November 2026, Windows, masters at
  version 1) stays as dated, owner-reported history. It is not the state of `main` today. A Windows baseline at the
  current state does not exist yet; T017 takes it (section 10).
- **The fix (tests only; in the package; never a refreshed hash).** Both tests keep what they prove, on fixtures they
  build themselves: (1) a synthetic INIT master with its own ledger and INIT record, whose hash the test computes
  from the bytes it wrote, plus a check with no pinned value that the real masters pass the installed version-2 chain
  and prefix rules (`master_versions.load_verified_source`), which stays true after every update; (2) the boundary
  refusals on a synthetic unopened game, and a new positive test that an opened game admits them only under the gates.
  A mutation check plants "accept any hash" and "admit before opening" and shows the rewritten tests catch both.
- **In the package's suite runner** the expected count per module comes from the tools; the two tests are never listed as
  allowed failures or skips. T017 records the before state (exactly these two failures) and the after state (none).

## 4. The package: files, by layer

New files are marked N; edited files E. Names are proposals. Every new program is run only by the owner through its
launcher, and joins the rulebook's rule 7 and the owner's deny patterns (section 11).

| Layer | File | | What it holds |
|---|---|---|---|
| L1 | `src/methods/_common/contract_vocab.py` | E | `CATCH_UP` run mode and tier; `FINAL_NEXT_DRAW` unreserved; two `producible` rows; binding kind `DEV_BATCH` (L6) |
| L1 | `src/methods/_common/contract_records.py`, `contract_task.py`, `contract_runner.py`, `Method_Contract_Runner.py` | E | the mode, target and binding table with `DEV_BATCH`; the mode-to-pin rule (CF-2); the three `'CATCH_UP'` special cases folded into the vocabulary |
| L1, L6 | `src/methods/_common/contract_dispatch.py` | E | the `DEV_BATCH` branch (section 5, L6); the session branch re-read against Appendix E, changed only if a matrix cell fails |
| L2 | `src/methods/_common/jsonl_ledger.py` | N | the one append discipline (Des 6.5): whole line, flush, fsync; torn last line kept as a side file; the digest chain |
| L2 | `src/methods/_common/weekly_records.py` | N | full validators for `SESSION_V1` and `FREEZE_LINE_V1`; the deadline; the effective class (Appendix I) as one pure function; `scored_identities` (CF-9) |
| L2 | `src/methods/_common/weekly_session.py`, `src/methods/Method_Weekly_Forecast.py` | N | `status`, `open-session` (and `--resume`), `next`, `close-session`; the state machine of Appendix F |
| L3 | `src/evaluation/weekly_score.py`, `src/evaluation/Method_Weekly_Score.py` | N | `score`, `witness`, `verify`, `diagnostic-score`; the score and witness ledgers |
| L3, L6 | `src/evaluation/outcome_reader.py` | E | the weekly freeze-line release rule and the post-seal development rule (CF-4) |
| L4 | `src/evaluation/league_sources.py` | N | the three read-only adapters, `LEAGUE_SOURCES`, the one-score rule, correction chains |
| L4 | `src/evaluation/league_table.py` | N | rows, columns, order, labels: pure functions from adapter output to the `.txt` and `.csv` bytes |
| L4 | `src/evaluation/league_publish.py`, `src/evaluation/Method_League_Table.py` | N | the one writer: archive (create-only), `current` (whole sets), the `WEEKLY_TABLE` row; `publish`, `history`, `reconstruction`, `repair-current`, `sources-add`, `sources-check` |
| L5 | `src/evaluation/ov1_numeric.py` | N | the integer kernel: directed fixed-point arithmetic, `exp` and `log` enclosures (section 6) |
| L5 | `src/evaluation/ov1.py`, `src/evaluation/Method_OV1.py` | N | weights, exact distribution (two routes), factor table and certificate, the registration, the ledger lines, the stream state; `register`, `record`, `status`, `verify` |
| L6 | `src/methods/_common/walk_forward.py`, `src/methods/Method_Walk_Forward.py` | E | plan schema `WF_BATCH_PLAN_V2` (explicit targets, named cohort, tickets, the `DEV_BATCH` binding); version-1 plans untouched |
| L6 | `src/evaluation/report.py`, `Method_Rankings_Report.py`, `report_writer.py` | E | the window contract; the tier filter on families (CF-5); V2 batches; the comparison with the sealed forecasts (Sup 7.2 rule 7) |
| L6 | `src/evaluation/reforecast_compare.py` | N | named forecast content compared, preconditions stated per pair |
| L7 | `src/evaluation/consolidated_report.py`, `src/evaluation/Method_Weekly_Report.py` | N | the full report from named sources; the retired-revision index |
| L5, L7 | `src/evaluation/registry/MEASURE_REGISTRY_V1.json` | E | OV-1's entry and its label; the `CATCH_UP` tier (as MHUP-A added the Mode H families to the family registry) |
| L8 | `src/Weekly_Session_Orchestrator.py`, `Run_Weekly_Session.bat`, `.gitignore` | N, E | the sequencer (Des 6.1); the ignore lines for the weekly run folders and session attempts ledgers |
| L8 | `tests/test_mhupb_*.py` (about fourteen modules), `tests/test_multigame_reader_contracts.py`, `tests/test_wf1b_static.py`, `tests/test_mhupa_updater_v0_2.py` | N, E | section 5's tests; the F-2 fix; the static allowances; the page-order cases |
| L8 | the package: manifest, verifier, copy tool, suite runner, install instructions, mutation tools, `TASK_T017.md` | N | Appendix J without barrier E; two commits; a release record with an empty entry list |

**The order of building, and review slices (RECOMMENDED; the reviewer and the owner may prefer fewer or more).** MHUP-A
was reviewed in two slices and then as one integrated package, and that worked. Proposed: slice 1 = the F-2 fix, L1, L2,
L3 (the live path); slice 2 = L5 and L6; slice 3 = L4, L7, L8; then the integrated package, reviewed as a whole, then
T017. Each slice is reviewable and tested on its own; nothing is installed before the integrated package passes.

## 5. Layer by layer

### L1. Modes and gates

- `CATCH_UP / FORECAST -> (WF_FORECAST, CATCH_UP)`; `FINAL_NEXT_DRAW / FORECAST -> (WF_FORECAST, PROSPECTIVE)`. Both
  stay refused unless ticketed, session-bound and under the developed record: the dispatch gate decides, as now.
- The mode-to-pin rule, in `contract_runner` after the reader has resolved the pin: `FINAL_NEXT_DRAW` only for
  `last_draw(v) + 1`; `CATCH_UP`, a session-bound `REAL_DEVELOPMENT` and a `DEV_BATCH` run only for targets at most
  `last_draw(v)`; the diagnostic route at most `last_draw(v)` (Des 3.4(b)).
- **Gate:** a table-driven test that walks every row of Appendix E across stages S0 to S5 and X on a synthetic project
  and asserts each cell (published, or refused with its code, with no byte written). The table in the test is typed in
  from Appendix E and cross-checked by a second, independently written "what should happen" function (R-4).
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
  environment digest; the previous line's digest. No witness or publication status.
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
  `frozen_at_utc`; effective class; exposure flag (`EXPOSED_DRAWS`; Powerball 1587 and 1588 carry HX-2).
- **Corrections:** the line format carries `amendment_of`. This package writes no corrective score (no corrected scorer
  exists); it only reads them correctly (L4).
- **Gates:** a second routine score for the same scientific identity under another score run id refuses (L-S1); a
  fixture amendment stands beside the old line, which stays byte-identical (L-S2); an S1 line scored by S2 at a grown
  master records both pins (L-W2); a crash mid-score resumes with the unscored records only; no freeze line, no score;
  `diagnostic-score` writes no ledger byte (L-G3); the witness cases L-V1 to L-V3; a static test that no routine command
  touches the network.

### L4. The league table

- **Sources** (Sup 4), each through its own read-only adapter that returns the same small row shape (key, hits, class,
  source identity): (a) the weekly score ledger; (b) the development score ledgers of the report attempts listed in
  `LEAGUE_SOURCES`; (c) the sealed Mode H ledger, shown and never summed, read only if its SHA-256 equals the one in
  its `SCORE_COMPLETE` record.
- **`LEAGUE_SOURCES_<GAME>`** is kept as numbered, create-only versions under
  `results/method_rankings/<GAME>/league/sources/`, each naming the digest of the one before; the highest valid
  version is current. Each entry names an attempt, its window and, where the batch was restricted, its variants; a
  named selection for a corrected score is an entry too. `sources-add` is an owner command with a typed statement
  (the pattern of the owner records): the "reviewed step on the owner's go" of Sup 4 rule 5. Nothing is overwritten,
  and Claude never writes there.
- **The one-score rule:** key (game, method, revision, variant, target, barrel, TOP or WORST); the scoring policy is not
  in the key. Two sources or two listed attempts with the same key and no named selection: refuse, naming the key. A
  correction chain that branches, cycles or has two heads: refuse. A listed source absent or failing its identity:
  "not available: <source>" for the affected variants, never a partial total shown as a total.
- **The table** (Sup 3): every released variant; `NO_SCORES`; `LOW_N` under 30; all scored draws (no P value); forward
  only with the witness-verified count beside it; last 10; the second table by kind with "Mode H as sealed"; WORST;
  the Powerball barrel; divisions; revision, release date, first and last scored target, missing and failed counts;
  the order by hits above chance per draw as an exact fraction, ties by identity; the fixed header sentences.
- **Publishing** (Sup 5.1): the set's bytes are built and checked in memory; the `WEEKLY_TABLE` row is appended (version,
  both digests); the two archive files are created create-only; then `current` is refreshed: the new copies are
  written under temporary names, verified against the archive, a `CURRENT_COPY_INCOMPLETE` notice is placed, the old
  copies are replaced, and the notice is removed last. `repair-current` repeats the copy from the archive. An archive
  set missing one member is completed only with bytes that rebuild identically (the pattern of the Mode H report).
- **Who writes** (Sup 4 rule 4): `league_sources.py` and `league_table.py` open nothing for writing (a static test);
  `league_publish.py` is the only writer of table files and of the `WEEKLY_TABLE` row. See CP-Q3 on the supplement's
  words "the orchestrator, and only it".
- **Gates:** each refusal and each degraded case of Sup 4 once; the adapters against the writers' real output (section
  8); an interrupted copy at every step leaves the notice and an intact archive; the history report recomputes nothing;
  every reconstruction row carries its label and the "released at that date" column.

### L5. OV-1 (section 6 has the arithmetic)

- **The registration** (`register --game G --statement "..."`, owner-run, create-only, one per game, a search-log row):
  the game; the first eligible target T0 = `last_draw + 1` at that moment, which must have no freeze line and a
  deadline still ahead; the formula; the six lambdas as exact fractions with equal weights; the bar 40; the pair rule
  and the V = 0 rule; the eligibility-time rule (OD-3); the missed-week rule (OD-2); the recovery rule (OD-4); the
  error budget (this game's 2.5% of the programme's 5%, and RC-1); the kernel's precision, margin and version. It
  refuses without the developed record. **There is no command that makes a second registration for a game.**
- **The ledger** (`OV1_LEDGER_<GAME>_V1.jsonl`, tracked, chained from the registration's digest):
  - the *eligibility line* for target T: the registration's identity, the freeze line's digest, the eligible variants
    (count and digest), **the weight of every number**, V as an exact fraction, whether the draw is a skip, the time,
    and the master pin then in force;
  - the *factor line*: the eligibility line's digest, the outcome pin copied from the score lines, X (from the score
    lines, CF-8, cross-checked against the weights), Z to a fixed number of digits for display, the six stored
    log-factors as exact fixed-point integers, the six running sums, the proved lower bound of the score, and
    `crossed`;
  - a *stop line*, written when the recorder first sees that the stream has stopped.
- **One idempotent command, `record --game G`,** called by the orchestrator after every `score` and after the loop.
  It writes whatever is due, in strict target order, and nothing twice: the eligibility line of a frozen prospective
  target whose cut-off has not passed; each factor line whose eligibility line and score lines are complete; the stop
  line. It needs only the frozen tickets and the ledgers. A failure of `record` never changes the live path's exit.
- **`verify`** rebuilds every line from the eligibility lines and the score ledger and compares bytes. A later kernel
  version must reproduce a frozen fixture ledger byte for byte, or it is a reviewed amendment.
- **Gates** (Sup 2 row L5): section 6's; incomplete pairs excluded; changing rosters and history-dependent weights; an
  interruption exactly between the freeze line and the eligibility line; the stop path; restart giving the same bytes;
  no OV-1 figure for a holdout, catch-up or development draw in the formal stream (Sup 6.7).

### L6. The window contract and back-history (always-review: holdout access, N-1)

- **A second plan schema, `WF_BATCH_PLAN_V2`,** beside the first, which is left exactly as it is: explicit targets, a
  named cohort, tickets (`TICKET_V1`, scope `DEV_BATCH`) and a `DEV_BATCH` binding on every request. Its runs publish
  under the development run root only.
- **The `DEV_BATCH` branch of the dispatch gate** (value-free records, fixed roots): the plan exists with that digest
  and its search-log row and lists the pair; the request pins the plan's pin; an open ticket, and no DONE ticket for
  the pair in the batch; for a target at or above `holdout_first`, the opening record and the game's `MODE_H_SEALED`
  (Sup 7.2 rules 1 and 2); for a target above `holdout_last` (rule 2A), the variant's release date is after the
  target's draw date, the target has a freeze line that does not name the variant, and no session ledger holds a
  ticket for the pair.
- **The report tool:** the window may reach `holdout_last` once the seal exists, and 2A targets for a V2 batch; the
  outcome reader releases those draws to a development report only under the same conditions, after the search-log
  row and the scoring plan are written (the existing order, unchanged); families are loaded by window **and tier**.
- **The comparison with the sealed forecasts** (Sup 7.2 rule 7), as a section of the batch's report: for each pair, the
  preconditions and whether each holds; the ranking with scores and ties, and the TOP and WORST sets, compared; every
  difference listed with the inputs' identities. It reads the sealed run folders and writes nothing under any sealed
  path.
- **Gates:** no write under any sealed Mode H path and no freeze line touched (a test snapshots every such file's bytes
  before and after each L6 command); every refused window refuses, including a holdout target before the seal, a 2A
  target with a weekly ticket, and a 2A target dated on or after the release; every forecast's tier is development;
  T-05 on the extended windows.

### L7. The consolidated report and the retired index

- Parts, each from named sources by identity, none pooled into a P value (Sup 8): the league table; OV-1; the forward and
  catch-up family tables; the matched-target view (R3 17.3.7); the development and Mode H results quoted from their own
  reports, not recomputed; each with a `WEEKLY_REPORT` search-log row.
- **Labels for the forward and catch-up family tables (RECOMMENDED; CP-Q4).** Their window and roster grow from report to
  report, so they are not a family fixed in advance. Use R3's existing labels and invent none: `EXPLORATORY_COHORT`,
  and `BONFERRONI_REFERENCE_UNCALIBRATED` on any Bonferroni arithmetic, under the heading "secondary".
- **Gates:** every figure traceable to a source identity; a test that searches the report's text, CSV and JSON for any
  pooled or joint figure and finds none; the retired index lists each retired revision once.

### L8. The orchestrator, the launcher and the rest

- **The sequence** (Des Appendix F, with the supplement's additions): status; open or resume; the loop of `next` and
  `score`, with `record` after each score; on `FROZE_NEXT`, `record` at once; `close-session`; then, and only then, the
  table; the status block.
- **Exit statuses, distinct:** 0 complete; one value for "frozen; table not written"; one for "frozen; OV-1 recorder
  failed"; another for a live-path stop, naming the child. A failure after `close-session` never reopens, undoes or
  delays anything before it.
- **Static tests:** the orchestrator imports neither `methods` nor `evaluation`, and has no `terminate`, `kill`,
  `taskkill`, psutil, signal, PID or timer; no module of L1 to L3 imports a module of L4 to L7 (the list of both sets
  is in the test, and a new file in `src/` that is in neither list fails the test).

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
small: the exact counts and one function, the upper end of `exp`. If the certificate fails, the program refuses and
writes no factor line.

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
- restart: the ledger rebuilt from its eligibility lines and the score ledger equals the stored bytes.

**6.6 Failure semantics and the error budget (EX_219 C1).**
- A frozen prospective target with no valid eligibility line at its cut-off: **PRIMARY STREAM STOP** for that game from
  that target (Sup 6.8, F01). No factor line for it or any later target. Forecasting, scoring, tables and every
  secondary measure continue. Every report says so.
- **After a stop the default is to stay stopped.** The package has no command to register again, and no recovery rule
  unless one is fixed in the registration before the first draw (OD-4). Nothing in the code spends, moves or reuses the
  stopped stream's 2.5%. A new confirmatory test would be a new owner-approved design amendment with a reviewed
  error-budget argument covering the whole programme; this plan proposes none.
- A V = 0 draw is a recorded skip with factor 1, decided on the eligibility line. It is not a stop.
- The other game's stream is unaffected. The two streams share no state.

## 7. Isolation of the live path (Sup 2; EX_213)

**Static:** the import test of L8. **Dynamic, by fault injection:** each test runs a whole session on a synthetic project
with one fault planted, then asserts that the session, attempts, forecast, witness and score ledgers and every run
record are byte-identical to the same session run without the fault, and that the orchestrator's exit status is the
distinct reporting status.

| Fault planted | Where | Expected |
|---|---|---|
| The table formatter raises | L4 | live records identical; "frozen; table not written"; a later `publish` writes the table as a new file |
| An adapter meets a duplicate key, a branching correction chain, a missing source | L4 | the table refuses or degrades as Sup 4 says; live records identical |
| The archive write fails after the search-log row; after the first of two files | L4 | no partial set is called current; live records identical; the next `publish` takes the next version |
| The `current` copy is interrupted at each step | L4 | `CURRENT_COPY_INCOMPLETE` present; archive intact; `repair-current` restores |
| `record` raises before the eligibility line; between eligibility and factor | L5 | the freeze line and scores identical; rerun before the cut-off writes the line; after it, the stop |
| The OV-1 ledger is unreadable or its chain is broken | L5 | `record` refuses; live records identical |
| The report tool fails on a V2 batch | L6 | no weekly record touched |
| The consolidated report fails | L7 | nothing else changes |
| Every child of the reporting steps exits non-zero | L8 | the session is already closed; the lock is gone; the exit status is the reporting one |

## 8. The source schemas (EX_213; CF-7)

- **The rule:** an adapter is tested against records made by the installed writer, never against a hand-written
  imitation. The tests run the real report tool (`report.run_report`) and the real Mode H scorer (`mode_h.score`) on
  invented masters, as the existing WF-1B and MHUP-A tests already do, and feed their ledgers to the adapters. The
  weekly score ledger is written by L3 in the same way.
- **The schemas the adapters rely on** are read from the writers and pinned in a test: `POST_OUTCOME_SCORE_RECORD_V1`
  (`contract_receipts.validate_score_record`: `track_id`, `draw_number`, `method_revision`, `main_matches`,
  `powerball_match`, `division`, the two digests, `evaluator_version`, optional `exposure_flag`); the rank record; the
  scoring plan (`attempt_id`, `batch_id`, window, `selected_forecasts`); the Mode H ledger's name
  (`mode_h_score_ledger.jsonl`, score lines then rank lines) and its `SCORE_COMPLETE` marker (`score_ledger_sha256`,
  `lines`).
- **What that cannot show:** that the real records on the owner's PC are what the writers would write today (they were
  written by the code as installed on 31 October, 1 November, 15 and 16 November). **RECOMMENDED, a separate owner go
  before the install (OD-5):** a small read-only census tool, run by the owner, that reads the real development and
  Mode H score ledgers through the adapters and prints only counts, field names, schema names and digests; it writes
  nothing. Its command is reviewed first. Until it has run, the league table's first real publication is itself the
  first meeting of the adapters with real records, and its refusal rules are what protect it.

## 9. Interruption and restart (EX_213)

A harness runs a command with a fault injected after its k-th durable write, for every k, then reruns the command and
compares the final bytes with an uninterrupted run. Durable writes are counted by wrapping the one ledger appender and
the one create-only writer, so no step can be missed.

| Command | Points | Must hold after the rerun |
|---|---|---|
| `open-session` | record; lock | one session; resume needs a token |
| `next`, catch-up set | each OPEN ticket, run record, DONE ticket; the freeze line | no pair run twice; the line names every record with its own session |
| `next`, next-draw set | `SET_STARTED`; each ticket and record; the freeze line | completed under the same ticket; classes by each record's own time |
| `score` | each score line | no line twice; unscored records only |
| `record` (OV-1) | eligibility line; each factor line; stop line | same bytes; never a second line for a draw |
| `publish` | search-log row; each archive file; each step of the `current` copy | archive never partial-as-current; next version on retry |
| V2 batch `run` | each ticket and record | as the Mode H batch today |
| the orchestrator | between every pair of children | the rerun continues from the records alone |

Also: the torn last line in each ledger (ignored, reported, kept as a side file, completed by the next writer); `STALE`
mid-session; a cleared lock and a successor session; a resume token older than five minutes or used twice.

## 10. Windows gates and the install

- **Cloud, before sending:** the suite on Python 3.13 and a 3.15 build; every mutant caught; the install rehearsed in LF
  and CRLF clones with every negative stopping; `check_task_commands.py` on the task file; every count from the tools.
- **T017 on the owner's PC (a task file; the owner's go; a rulebook allowance like section 2A, reviewed first):**
  1. the baseline at the base commit: the suite, expecting exactly the two failures of section 3;
  2. Appendix J steps 0 to 18 without barrier E, in a task clone, with the suite in `--shadow` mode at step 10;
  3. the whole suite again after step 18, in the post-release state (the owner's decision of 13 November 2026);
  4. the time taken by the closure and environment digests (L2's uncertainty);
  5. the launch chain from a Python parent on Windows: the orchestrator starting `Run_Experiment.bat` and
     `Run_Evaluation.bat` children and reading their output to the end (Des 6.1);
  6. **RECOMMENDED (CP-Q6):** in the same task clone, a full weekly dress rehearsal on invented masters and invented
     owner records, through the real launchers: two missed draws caught up, the next forecast frozen, the table
     written, the reporting layer made to fail once. It touches no real data and terminates nothing.
- **The install:** Appendix J as amended (J-1 to J-4), two commits, a release record with an empty entry list. The
  package changes no roster, so it may install while a weekly set is unfinished (none exists). It changes `src/`, so
  Mode H's frozen closure no longer matches afterwards; that is expected, the studies are sealed and never rerun, and
  reading their records needs no closure check (section 2).
- **Before the install:** the owner's deny lines for the new programs in `.claude/settings.json` (his edit), and the
  rulebook edition.

## 11. Documents that travel with the package (each reviewed and ratified before it goes into `doc/`)

- R3: 17.3.6 (the window contract); 17.3.9 (`CATCH_UP`; `LATE_PRE_DRAW`); 17.5.2 and the measure registry (OV-1, label
  "exact test martingale"); the league table and reconstruction as descriptive outputs.
- E2R-1: 9.1 and E2R-R41 (`CATCH_UP`); E2R-R44 (`FINAL_NEXT_DRAW`); the `DEV_BATCH` binding.
- The Architecture's next edition (the orchestrator as a sequencer; the new launcher).
- A short amendment to the design naming the supplement, and recording whatever is decided under section 12.
- The runner's rulebook v0.6 (Sup 10): rule 4 withdrawn; rule 5 as read-only wording; rule 7 with the new programs; the
  T017 allowance. The owner's checklist, with the A7 recovery procedure (Des 7).
- `exchange/README.md` v0.6 (the write rules after RAT-34; EX_216 D3).

## 12. Decisions and questions

**For the owner (each with a recommendation; one at a time when he is ready):**
- **OD-1. May a development batch name its variants?** On 31 October you declined that (ER-6) and chose full-cohort
  batches. The supplement's rule 2A needs a restricted batch (CF-6), and on 17 November you were told a new method
  computes only its own variants. RECOMMENDED: yes, for V2 batches: a new or revised method runs alone; the others'
  records are reused. *Why:* a full-cohort rerun repeats every earlier run each time a method arrives (the first
  Powerball batch took about 80 minutes for 40 variants, and that grows with every wave) and creates a second score
  for every old pair, which the league table must then be told to ignore. *Alternative:* keep full-cohort batches up to `holdout_last` and allow restricted
  batches only for rule 2A. *Cost of yes:* one more reviewed gate rule.
- **OD-2. A missed week and the formal test.** If no next-draw forecast was frozen for a draw (the PC was off, or the
  hour rule said `NONE`), the supplement does not say what OV-1 does. Options: (A) the stream stops, so one missed week
  ends that game's formal test for good; (B) the draw counts as a skip with factor 1, recorded at the next session
  from the forecast ledger alone, which shows that no next-draw set was frozen for it. RECOMMENDED: B. *Why it is
  sound:* not running a session is decided before the draw, so it cannot use the result; a frozen forecast, once it
  exists, is in the chained ledger and then needs its eligibility line or the stream stops. *Uncertainty:* B records a
  skip after the result is known, which the reviewer may judge to be against F01's wording; it is asked first (CP-Q1).
- **OD-3. The cut-off for the eligibility line.** Options: (A) the forecast deadline, 00:00 local on the draw date; (B)
  12:00 local on the draw date, and before the result is in the master. Only records frozen before the deadline count
  in either case. RECOMMENDED: B. *Why:* under A, a set that finishes five minutes after midnight, or a crash resumed
  the next morning, ends the formal test although the draw is still hours away. *Uncertainty:* B relies on the fact
  that both games are drawn in the evening; that is the owner's knowledge, fixed in the registration. If undecided, A.
- **OD-4. Recovery after a stop.** RECOMMENDED: none; the stream stays stopped (EX_219 C1's default).
  *Alternative for the reviewer to assess only if wanted:* a rule fixed in the registration that always rebuilds a
  missing eligibility line from the freeze line by the same function, marked as rebuilt, with no choice left to anyone.
- **OD-5.** The read-only census of section 8, on its own go later. **OD-6.** The slices of section 4.

**For the reviewer:**
- **CP-Q1.** OD-2 and OD-3: are options B consistent with Sup 6.5 and 6.8 (F01, RC-1), or do they need a supplement
  amendment? Is there a third option you prefer?
- **CP-Q2.** Is section 6's realisation (the lower end of a checked enclosure, less a fixed margin; exact integer sums;
  the per-draw certificate) an acceptable reading of Sup 6.5's numerical contract? Is the certificate wanted as a
  hard refusal, as planned?
- **CP-Q3.** Sup 4 rule 4 says "the orchestrator, and only it" appends the `WEEKLY_TABLE` row and the OV-1 lines. Des 6.1
  makes the orchestrator a sequencer that imports neither side and holds no state. This plan reads the supplement as
  "one named writer command per record, started by the orchestrator, and never the adapters or the formatter". The
  table can then also be published later by its own command and still be logged. Is that reading acceptable?
- **CP-Q4.** L7's labels for the forward and catch-up family tables.
- **CP-Q5.** CF-9: the forecasting half reading score identities through one function.
- **CP-Q6.** T017's dress rehearsal on invented data in the task clone, and the wording of its rulebook allowance.
- **CP-Q7.** Rule 2A says "dated before that variant's release". A target frozen before a release on the draw's own day is
  then covered by neither the weekly session nor 2A, and stays a typed gap for that variant (Des Appendix I already
  has that row). Planned as written. Is the gap acceptable, or should 2A read "frozen before"? (That would be an
  amendment.)
- **CP-Q8.** Exposure flags on development re-forecasts of Powerball 1585 and 1586: planned as "the flag prints wherever
  the draw is scored" (Sup 3.5), since the supplement does not say it for re-forecasts.
- **CP-Q9.** Anything in sections 5 to 10 that the code round's gates need and this plan lacks.

**DECIDED (cited, not reopened):** per game, bar 40, no joint figure (entry 55); the eight layers and the isolation rule
(RAT-33); the deadline (MHUP-R); tickets for official runs (Q11); two commits per install; the full suite after step 18.
**RECOMMENDED:** everything in sections 4 to 10 not listed as decided. **OPEN:** OD-1 to OD-6; CP-Q1 to CP-Q9.

## 13. Which gate belongs where

| Stage | What is judged | By whom |
|---|---|---|
| This plan's review | coverage of every gate; the kernel's method and proof plan; the release rules of CF-4; the `DEV_BATCH` gate; the fault and interruption matrices; the baseline method; OD-2 to OD-4's consistency with the supplement | the reviewer; then the owner's decisions and his go to start code |
| Implementation acceptance | the tests on both Pythons; mutants; the proofs written out; oracles reproduced (R-2, R-4); adapters on writer-made records; the cloud rehearsals; T017's report read step by step | the reviewer; Claude's evidence |
| Separate owner gos | starting code; each task file's run; the census; the E2R-T12 run context; the install; his settings lines; each document's ratification; `declare-developed` per game; OV-1's registration per game; the first weekly sessions; every re-forecast batch and report; `sources-add`; the Powerball 1145-1285 run | the owner |

## 14. Not tested, uncertainties, alternatives

- **Not tested:** everything. The only things run were the existing suite (section 3) and the probe (section 6.4).
- **Size:** seventeen new Python source files and one launcher, about twelve edited, about fourteen new test modules. Larger than MHUP-A's
  code. Building it is several working sessions, with a review round per slice.
- **Uncertainties:** the cost of the environment digest at every `next`; the local time of midnight around a
  daylight-saving change (tested with fixed zones; the owner's zone is the one that matters); whether real score
  records match the writers' present output (section 8); the answers to CP-Q1 to CP-Q3, which could change L5 and L8.
- **Alternatives considered:**
  - `decimal` at high precision for OV-1, with a margin: shorter code, but it leans on a library's rounding of `exp` and
    `ln`, and on two implementations of `decimal` giving the same digits. Kept as a cross-check only.
  - Exact fractions throughout: no rounding to argue about, but the denominators grow without limit.
  - Reading X from the master in L5: rejected; the score lines already hold it (CF-8), and L5 then needs no outcome
    access at all.
  - Extending the first plan schema in place: rejected; committed version-1 plans must stay verifiable byte for byte.
  - Writing the eligibility line inside the forecasting half, in the same step as the freeze line: it would close the
    gap between the two, but L2 would then import L5, against the isolation rule.
  - One big review instead of slices: fewer rounds, but faults in the live path would be found late.

End of draft v0.1.
