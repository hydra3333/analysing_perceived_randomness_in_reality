# Slice 1 working notes (Claude; survives compaction). Started 17 Nov 2026 20:10 on the owner's code go (entry 75).

Layout (MHUP-A convention, see exchange/CLAUDE_WEB_TOOLS/mhupa/): under exchange/CLAUDE_WEB_TOOLS/mhupb/:
  slice1_new/src/...  slice1_new/tests/...   new files (copied into a dev tree)
  apply_slice1.py TREE      counted edits to installed modules (every old string exactly once)
  edit_tests_slice1.py TREE counted edits to existing tests
  build_dev_slice1.sh BASE DEV TOOLS   makes the dev tree
Workspace: /home/claude/work/slice1/{base (git clone of main), dev (built tree)}; venv315 at /home/claude/work/venv315.
Suite: one module per process, python -B -m unittest -v tests.<mod>, skip class T12Determinism (see mhupa/run_all_but_t12.py).
Baseline: 3 known failures (2 in test_multigame_reader_contracts V011ReaderTests; test_mhupa_launchers test_gitignore_lines).

Decisions made while coding (tell the reviewer in the slice EX message):
- S1-D1 run root: installed contract_runner._run_root_for sends EVERY session-bound run to results/real/weekly/contract_runs;
  Des 6.4 says session-bound REAL_DEVELOPMENT goes to the development root. Kept installed behaviour (no gate change); ASK reviewer.
- S1-D2 closure: a target is closed when every record its freeze line names has a routine score line; failure records get a
  score line too (record_kind PREDICTION_FAILED, no match fields), so "scored or a failure record" (Des 6.3) holds either way.
- S1-D3 only the forecast ledger is digest-chained (Des 6.5); score and witness ledgers are append-only, same write discipline.
- S1-D4 freeze line carries set_kind (CATCH_UP_SET | NEXT_DRAW_SET) (Sup v0.8 6.8 needs "freeze line of a next-draw set").
- S1-D5 diagnostic-score in slice 1 serves prefix targets and weekly-frozen targets only; sealed-holdout targets wait for
  slice 2's post-seal development release rule (CF-4).
- S1-D6 STOP-class run outcome in the forecasting half: no DONE ticket, non-zero exit, lock stays; resume marks it
  FAILED_TO_START and reruns under a new run id (as Mode H). CONTINUE-class failures are DONE + PREDICTION_FAILED.
- S1-D7 outcome reader: new read_outcome_rows() also returns the master's draw date (score line: draw_date_is_derived);
  read_outcomes() unchanged for existing callers.
- Mode rule (Des 6.4): result accepted & release_date < draw date -> CATCH_UP; accepted & not before -> REAL_DEVELOPMENT
  (session-bound); M = last_draw+1 and >= 60 min before deadline at SET_STARTED -> FINAL_NEXT_DRAW.
- mode-to-pin rule in contract_runner after the reader: FINAL_NEXT_DRAW only target == last_draw(v)+1; CATCH_UP,
  session-bound REAL_DEVELOPMENT, OWNER_DIAGNOSTIC only target <= last_draw(v).

Files planned for slice 1:
 new src/methods/_common: jsonl_ledger.py weekly_records.py score_identities.py weekly_session.py; src/methods/Method_Weekly_Forecast.py
 new src/evaluation: weekly_score.py Method_Weekly_Score.py
 edited: contract_vocab.py contract_runner.py contract_task.py outcome_reader.py .gitignore
 tests: test_mhupb_l1_gates.py test_mhupb_weekly_forecast.py test_mhupb_weekly_score.py mhupb_fixtures.py;
        edits: test_multigame_reader_contracts.py test_mhupa_launchers.py test_mhupa_gates.py test_e2r_contract.py test_wf1b_static.py
Progress log (append below):
- 20:30 L1 + baseline fixes built: apply_slice1.py, edit_tests_slice1.py, tests/test_mhupb_l1_gates.py; full suite on 3.13 was 571 run, only the expected gates assertion failing before its edit.
- 20:35 L2 modules written (jsonl_ledger, weekly_records, score_identities, weekly_session, Method_Weekly_Forecast); imports ok; tests next.
- 20:47 checkpoint committed to exchange/CLAUDE_WEB_TOOLS/mhupb/slice1 (WIP). L3 modules written (weekly_score, Method_Weekly_Score, outcome_reader edits). NEXT: tests/mhupb_fixtures.py, test_mhupb_weekly.py (flows), then full suite both Pythons, mutants, EX message.
