"""MHUP-B slice 1: mutation checks (design Appendix L: one planted defect per rule, each caught by a named test).

For each mutant: one counted edit to one file of a built dev TREE, the named test is run in its own process and must
FAIL; the file is then restored byte for byte. A mutant that survives is reported and the tool exits 1.
Usage: python3 -I mutations_slice1.py TREE [name-substring ...]
"""
import os
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
only = sys.argv[2:]
C = 'src/methods/_common/'
E = 'src/evaluation/'
L1, FC, SC_ = 'tests.test_mhupb_l1_gates', 'tests.test_mhupb_weekly_forecast', 'tests.test_mhupb_weekly_score'

MUTANTS = [
    # ---- the baseline fixes (code plan section 3)
    ('accept any hash', C + 'master_versions.py',
     "    if hashlib.sha256(raw_master).hexdigest() != rows[-1].master_sha256:\n",
     "    if False:\n", 'tests.test_multigame_reader_contracts.V011ReaderTests.test_master_source_and_ledger_file_hashes'),
    ('admit before opening', C + 'game_draws_reader.py',
     "                if OR.opening_record(repo_root, game_id) is None:\n",
     "                if False:\n", 'tests.test_multigame_reader_contracts.V011ReaderTests.test_only_legacy_e1_allowed_at_boundary'),
    ('ignore the scores again', '.gitignore',
     "results/real/weekly/contract_runs/\n",
     "results/real/weekly/contract_runs/\nresults/real/development/scores/\n",
     'tests.test_mhupa_launchers.LauncherStatics.test_gitignore_lines'),
    # ---- L1
    ('catch-up given the prospective tier', C + 'contract_vocab.py',
     "            return 'WF_FORECAST', 'CATCH_UP'                 # the new row",
     "            return 'WF_FORECAST', 'PROSPECTIVE'              # the new row", L1 + '.Vocabulary'),
    ('final for a draw the master holds', C + 'contract_runner.py',
     "        if target != last + 1:\n", "        if False:\n", L1 + '.ModeToPin.test_each_mode_at_the_last_draw_the_next_and_beyond'),
    ('catch-up for the next draw', C + 'contract_runner.py',
     "    elif target > last:\n", "    elif False:\n", L1 + '.ModeToPin.test_each_mode_at_the_last_draw_the_next_and_beyond'),
    ('weekly record naming a prefix draw', C + 'contract_forecast.py',
     "        if target <= p.holdout_last:\n            raise ValueError(f'{where}: a {mode} record must name a draw after the holdout')\n",
     "        pass\n", L1 + '.ModeToPin.test_one_data_kind_for_every_real_mode'),
    ('weekly modes without the developed record', C + 'contract_dispatch.py',
     "            if OR.developed_record(root, game) is None:\n", "            if False:\n",
     L1 + '.GateMatrix'),
    ('catch-up without the release rule', C + 'contract_dispatch.py',
     "            if mode == 'CATCH_UP' and not released_before:\n", "            if False:\n", L1 + '.GateMatrix'),
    # ---- L2
    ('the hour rule', C + 'weekly_session.py',
     "        if now + WR.HOUR_RULE > deadline_utc:\n", "        if now > deadline_utc:\n", FC + '.Deadline.test_the_hour_rule'),
    ('a frozen target treated as closed', C + 'weekly_session.py',
     "if t not in closed), None)", "if t not in by_target), None)",
     FC + '.WholeSession.test_next_never_passes_a_frozen_target_that_is_not_scored'),
    ('a completed run never ticketed DONE', C + 'weekly_session.py',
     "                        kind, tclass = 'DONE', ev['terminal_class']\n",
     "                        kind, tclass = 'FAILED_TO_START', None\n",
     FC + '.Interruptions.test_every_step_resumed_and_continued_by_a_successor'),
    ('a pair with a DONE ticket run again', C + 'weekly_session.py',
     "        if key in done:\n            continue\n        if accepted:\n",
     "        if accepted:\n", FC + '.Interruptions.test_every_step_resumed_and_continued_by_a_successor'),
    ('every record prospective', C + 'weekly_records.py',
     "        return 'PROSPECTIVE' if frozen_at_utc < deadline_utc else 'LATE_PRE_DRAW'\n",
     "        return 'PROSPECTIVE'\n", FC + '.Deadline.test_a_straddling_set_is_classified_record_by_record'),
    ('the chain digest unchecked', C + 'jsonl_ledger.py',
     "        if r.get('previous_line_digest') != prev:\n", "        if False:\n",
     FC + '.LedgerRules.test_the_chain_broken_by_an_edit_a_removal_and_a_reorder'),
    ('a torn fragment left in place', C + 'jsonl_ledger.py',
     "    repair_torn_tail(path)\n    if path.is_symlink()", "    if path.is_symlink()",
     FC + '.LedgerRules.test_a_torn_last_line_is_ignored_reported_and_completed'),
    ('a freeze time earlier than the last', C + 'weekly_session.py',
     "    if lines and now < WR.parse_utc(lines[-1]['frozen_utc']):\n", "    if False:\n",
     FC + '.Deadline.test_the_clock_behind_the_last_freeze_line_refuses'),
    ('a duplicated score identity accepted', C + 'score_identities.py',
     "        if ident in seen:\n", "        if False:\n", FC + '.ReadingScored.test_identities_only_and_refusals'),
    ('development back-history run as catch-up', C + 'weekly_session.py',
     "            mode = 'CATCH_UP' if OR.release_date_of(mem) < draw_date else 'REAL_DEVELOPMENT'\n",
     "            mode = 'CATCH_UP'\n",
     FC + '.StaleAndRoster.test_released_on_or_after_the_draw_date_is_development_never_missing_batch'),
    ('an old resume token', C + 'weekly_session.py',
     "    if age > WR.RESUME_TOKEN_MAX_AGE or age.total_seconds() < -60:\n", "    if False:\n",
     FC + '.Interruptions.test_resume_tokens_and_changed_code'),
    ('a resume token used twice', C + 'weekly_session.py',
     "    if any(t['kind'] == 'RESUMED' and t.get('resume_token') == newest.name for t in rows):\n", "    if False:\n",
     FC + '.Interruptions.test_resume_tokens_and_changed_code'),
    ('changed code under a session', C + 'weekly_session.py',
     "    if _digests() != (session['closure_digest'], session['environment_digest']):\n        raise SessionRefused('CODE_CHANGED: the closure or environment digest differs from the session record\\'s')\n",
     "", FC + '.Interruptions.test_resume_tokens_and_changed_code'),
    ('stale pin not noticed', C + 'weekly_session.py',
     "    if (row.version, row.master_sha256) != OR.pin_of(session, 'session record'):\n        return 'STALE', None\n",
     "", FC + '.StaleAndRoster.test_stale_when_the_master_grows_and_the_next_session_continues'),
    ('a second session while one is locked', C + 'weekly_session.py',
     "    if locked is not None:\n        raise SessionRefused(f'a session lock exists", "    if False:\n        raise SessionRefused(f'a session lock exists",
     FC + '.Interruptions.test_open_session_refusals'),
    ('the lock removed at an unclean end', C + 'weekly_session.py',
     "        if st['lowest_unclosed'] is not None:\n            raise SessionRefused(f'target {st[\"lowest_unclosed\"]} has an accepted result",
     "        if False:\n            raise SessionRefused(f'target {st[\"lowest_unclosed\"]} has an accepted result",
     FC + '.Interruptions.test_open_session_refusals'),
    # ---- found on re-reading with EX_229's principle: the developed record is tied to the sealed study (design 6.7)
    ('an arbitrary developed record believed', C + 'weekly_records.py',
     "    if (rec['mode_h_score_digest'] != seal['score_ledger_sha256'] or rec.get('mode_h_batch_id') != batch['batch_id'] or\n            rec['owner_statement'] != OR.DEVELOPED_STATEMENT):\n",
     "    if False:\n", FC + '.Interruptions.test_open_session_refusals'),
    ('a developed record believed without the seal', C + 'weekly_records.py',
     "    if batch is None or not OR.mode_h_sealed(root, game_id):\n", "    if False:\n",
     FC + '.Interruptions.test_open_session_refusals'),
    # ---- EX_229 F-229-1: the run root follows the run mode (design 6.4)
    ('a session development run sent to the weekly root', C + 'owner_records.py',
     "    return development_runs_root(root) if run_mode == 'REAL_DEVELOPMENT' else weekly_runs_root(root)\n",
     "    return weekly_runs_root(root)\n", L1 + '.ModeToPin.test_each_session_run_mode_publishes_under_its_one_root'),
    ('the runner accepts any root for a session run', C + 'contract_runner.py',
     "        return OR.session_runs_root(PROJECT_ROOT, request.get('run_mode'))\n", "        return None\n",
     L1 + '.ModeToPin.test_each_session_run_mode_publishes_under_its_one_root'),
    ('evidence looked for under the weekly root only', C + 'weekly_records.py',
     "    return (OR.session_runs_root(root, request['run_mode']) / request['game_id']",
     "    return (OR.weekly_runs_root(root) / request['game_id']", SC_ + '.RunRoots'),
    ('the forecasting half publishes every run in the weekly root', C + 'weekly_session.py',
     "run_root=OR.session_runs_root(root, mode))", "run_root=OR.weekly_runs_root(root))", SC_ + '.RunRoots'),
    # ---- EX_229 F-229-2: only valid, canonical, linked score lines count
    ('score lines not fully validated', C + 'weekly_records.py',
     "    for s in rows:\n        validate_score_line(s)\n", "    for s in rows:\n",
     FC + '.ReadingScored.test_identity_shaped_fragments_cannot_close_a_target'),
    ('score lines not canonical', C + 'weekly_records.py',
     "    rows, _torn = JL.read_lines(score_ledger_path(root, game_id))\n",
     "    rows, _torn = OR.read_jsonl(score_ledger_path(root, game_id))\n",
     FC + '.ReadingScored.test_identities_only_and_refusals'),
    ('a score not tied to its freeze line', C + 'score_identities.py',
     "        WR.check_score_linkage(s, line)\n", "", FC + '.ReadingScored.test_identities_only_and_refusals'),
    ('a readout out of range accepted', C + 'weekly_records.py',
     "            _check_readout(s['readouts'][name], s['game_id'], f'{what}: readout {name}')\n", "            pass\n",
     FC + '.ReadingScored.test_identities_only_and_refusals'),
    ('a drawn Powerball outside 1 to 20 accepted', C + 'weekly_records.py',
     "        if type(s['drawn_powerball']) is not int or not 1 <= s['drawn_powerball'] <= PB_POOL:\n",
     "        if type(s['drawn_powerball']) is not int:\n", FC + '.ReadingScored.test_identities_only_and_refusals'),
    ('an amendment that names nothing', C + 'score_identities.py',
     "        if s['amendment_of'] is not None and earlier.get(s['amendment_of']) != ident[:6]:\n", "        if False:\n",
     FC + '.ReadingScored.test_identities_only_and_refusals'),
    # ---- EX_229 F-229-3: only complete, linked witness lines count
    ('an unlinked verification promotes', C + 'weekly_records.py',
     "        elif link not in recorded:\n", "        elif False:\n", SC_ + '.Witness'),
    ('an incomplete witness line accepted', C + 'weekly_records.py',
     "    _need(w, WITNESS_RECORDED_FIELDS if kind == 'WITNESS_RECORDED' else WITNESS_VERIFIED_FIELDS, what)\n", "",
     SC_ + '.Witness'),
    ('a verification by a name read as valid', C + 'weekly_records.py',
     "        if w['verified_by'] not in VERIFIER_ROLES:\n            raise RecordRefused(f'{what}: verified_by is a role",
     "        if False:\n            raise RecordRefused(f'{what}: verified_by is a role", SC_ + '.Witness'),
    ('evidence without the reference read as valid', C + 'weekly_records.py',
     "                w['ref'] not in w['evidence']:\n", "                False:\n", SC_ + '.Witness'),
    # ---- EX_229 F-229-4: a next-draw set is believed only with its genuine SET_STARTED ticket
    ('a SET_STARTED ticket inside the hour', C + 'weekly_records.py',
     "    if started + HOUR_RULE > parse_utc(want, f'{what} deadline') or started < parse_utc(owner['started_utc']):\n",
     "    if False:\n", SC_ + '.SetProvenance'),
    ('a SET_STARTED ticket from a session that holds the draw', C + 'weekly_records.py',
     "    if owner['last_draw'] != target - 1:\n        raise RecordRefused(f'{what} was written",
     "    if False:\n        raise RecordRefused(f'{what} was written", SC_ + '.SetProvenance'),
    ('two SET_STARTED tickets', C + 'weekly_records.py',
     "    if len(found) != 1:\n        raise RecordRefused(f'{what} is not exactly one",
     "    if False:\n        raise RecordRefused(f'{what} is not exactly one", SC_ + '.SetProvenance'),
    ('a SET_STARTED ticket of another mode or deadline', C + 'weekly_records.py',
     "    if t.get('run_mode') != 'FINAL_NEXT_DRAW' or t.get('deadline_utc') != want:\n", "    if False:\n",
     SC_ + '.SetProvenance'),
    ('a next-draw set believed from its label', C + 'weekly_records.py',
     "        if found_start is None:\n            raise RecordRefused(f'target {target}: a next-draw record or set with no SET_STARTED ticket')\n",
     "        if found_start is None:\n            found_start = (None, {'utc': '2000-01-01T00:00:00Z'})\n", SC_ + '.SetProvenance'),
    ('the forecasting half believes a late SET_STARTED ticket', C + 'weekly_session.py',
     "    return _guard(WR.set_started_ticket, _root(), game_id, target, tickets) is not None\n",
     "    return any(t['kind'] == 'SET_STARTED' and t['target_draw_number'] == target for rows in tickets.values() for t in rows)\n",
     FC + '.Deadline.test_a_set_started_ticket_that_breaks_the_hour_rule_is_not_believed'),
    # Not listed, because each has a second guard (tried 17 November 2026): the SET_STARTED ticket later than its records
    # (also later than the freeze line); a CATCH_UP record from a session whose master lacks the draw (its session
    # record's digest and the runner's mode-to-pin rule refuse first).
    # ---- L3
    ('outcome released without verifying the records', E + 'outcome_reader.py',
     "        WR.verify_named_records(repo_root, game_id, line)\n", "",
     SC_ + '.ReleaseRule.test_evidence_that_does_not_verify_serves_no_outcome'),
    ('outcome released without a freeze line', E + 'outcome_reader.py',
     "        if line is None:\n            return False\n        WR.verify_named_records", "        if line is None:\n            return True\n        WR.verify_named_records",
     SC_ + '.ReleaseRule.test_no_freeze_line_no_outcome_and_the_other_refusals'),
    ('outcome released without the developed record', E + 'outcome_reader.py',
     "        WR.developed(repo_root, game_id)                   # the declaration of this game's sealed study, or a refusal\n", "",
     SC_ + '.ReleaseRule.test_no_freeze_line_no_outcome_and_the_other_refusals'),
    ('a second routine score', E + 'weekly_score.py',
     "            if SI.routine_identity(game_id, target, ev['named']) not in identities}\n", "            }\n",
     SC_ + '.ScoringGuards'),
    ('the training pin recorded as the outcome pin', E + 'weekly_score.py',
     "'outcome_ledger_version': scoring['ledger_version'],", "'outcome_ledger_version': r['ledger_version'],",
     SC_ + '.AcrossWeeks'),
    ('TOP scored from the WORST entry', E + 'weekly_score.py',
     "        entry, why = COL._entry(forecast, ro, game_id)\n", "        entry, why = COL._entry(forecast, 'WORST', game_id)\n",
     SC_ + '.Quantities'),
    ('the exposure flag dropped', E + 'weekly_score.py',
     "             'exposure_flag': OR.exposure_flag(game_id, target),\n", "             'exposure_flag': None,\n",
     SC_ + '.Quantities'),
    ('the date flag always true', E + 'weekly_score.py',
     "             'draw_date_is_derived': date_text == p.derived_date(target).isoformat()}\n",
     "             'draw_date_is_derived': True}\n", SC_ + '.Quantities.test_a_date_off_the_weekly_rule_is_flagged'),
    # Not listed since EX_229's corrections, because it now has a second guard: the scorer's own "reference in the
    # evidence" test in verify() is repeated by the witness line's validator ('evidence without the reference read as
    # valid', above, is the listed one).
    ('a late verification promotes', C + 'weekly_records.py',
     "        if w['kind'] == 'WITNESS_VERIFIED' and parse_utc(w['received_utc'], 'witness received_utc') < limit:\n",
     "        if w['kind'] == 'WITNESS_VERIFIED':\n", SC_ + '.Witness'),
    ('diagnostic-score without the release rule', E + 'weekly_score.py',
     "    if target >= p.holdout_first and not RD.outcome_release_allowed(root, game_id, target):\n", "    if False:\n",
     SC_ + '.DiagnosticScore'),
    # Not listed, because it is equivalent: with _check_targets' release test removed, the reader's second guard in its
    # read loop ("holdout or later row reached without release") refuses the same request (tried 17 November 2026).
    ('scoring a target the session\'s master does not hold', E + 'weekly_score.py',
     "    if target > outcome_row.last_draw:\n", "    if False:\n",
     SC_ + '.ReleaseRule.test_no_freeze_line_no_outcome_and_the_other_refusals'),
    ('the scorer skips the cross-session check', E + 'weekly_score.py',
     "    evidence = _guard(WR.verify_named_records, root, game_id, line)        # the cross-session check, every record\n",
     "    evidence = _guard(WR.verify_named_records, root, game_id, line)\n    _plant = None\n",
     None),                                                              # a marker edit: proves the edit machinery only
]

env = dict(os.environ)
env['PYTHONPATH'] = os.pathsep.join(str(tree / d) for d in ('src', 'src/methods', 'tests'))
env['PYTHONDONTWRITEBYTECODE'] = '1'
survived = caught = 0
for name, rel, old, new, test in MUTANTS:
    if test is None or (only and not any(o in name for o in only)):
        continue
    path = tree / rel
    raw = path.read_bytes()
    text = raw.decode('ascii')
    if text.count(old) != 1:
        print(f'NOT APPLIED  {name}: the old text occurs {text.count(old)} times in {rel}')
        survived += 1
        continue
    try:
        path.write_bytes(text.replace(old, new).encode('ascii'))
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', test], cwd=tree, env=env, capture_output=True, text=True)
    finally:
        path.write_bytes(raw)
    if r.returncode != 0 and ('FAILED' in r.stderr):
        caught += 1
        print(f'CAUGHT       {name}  [{test}]')
    else:
        survived += 1
        print(f'SURVIVED     {name}  [{test}]  exit {r.returncode}: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""}')
print(f'mutants caught {caught}; survived or not applied {survived}')
sys.exit(1 if survived else 0)
