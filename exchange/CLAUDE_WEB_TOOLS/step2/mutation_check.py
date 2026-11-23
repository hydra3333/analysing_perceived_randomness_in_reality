"""Build step 2, proof tool: plant one fault at a time in the engine and require a named test to fail.

Usage: mutation_check.py <dev tree with the step 2 files in place> <python>
It works only in the tree it is given (use a disposable copy). For each planted fault it alters one file of
src/research/, runs the test module that should catch it, requires that module to FAIL, and puts the file back.
It prints one line a fault and ends with RESULT: PASS only if every planted fault was caught and every file was
put back byte for byte. The coding practices ask that each rule have a test with a planted fault; this shows it
for the rules of the job, OV-1, the derived check and the withdrawal.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

# (what the fault is, the file, the text to find exactly once, what replaces it, the test that must fail)
FAULTS = [
    ('a withdrawn variant is still scored', 'research_job.py',
     "                or state.status.is_withdrawn_at(draw)):\n            continue\n        variant = state.variant\n        content = score_content(",
     "                or False):\n            continue\n        variant = state.variant\n        content = score_content(",
     'test_research_ov1_and_checks.Withdrawal.test_the_planted_late_result_is_never_scored_in_every_kind_of_tree_alike'),
    ('a withdrawn variant is still forecast', 'research_job.py',
     "        if state.next_target != draw or state.status.is_withdrawn_at(draw):",
     "        if state.next_target != draw:",
     'test_research_ov1_and_checks.Withdrawal.test_the_same_in_a_catch_up_of_six_draws'),
    ('a withdrawn variant stays in the prevailing cohort', 'status_file.py',
     "        return self.eligible_from is not None and self.eligible_from <= draw and not self.is_withdrawn_at(draw)",
     "        return self.eligible_from is not None and self.eligible_from <= draw",
     'test_research_ov1_and_checks.Withdrawal.test_the_planted_late_result_is_never_scored_in_every_kind_of_tree_alike'),
    ('an eligibility draw is written without a successful results step', 'research_job.py',
     "    if succeeded:\n        write_eligibility_draws(job, records)",
     "    write_eligibility_draws(job, records)",
     'test_research_job.TheExamplesOfSection72.test_the_first_job_with_the_results_step_failing_absent_or_left_out'),
    ('an eligibility draw already present is rewritten', 'research_job.py',
     "        if (state.status.eligible_from is not None or state.status.withdrawn_from is not None\n                or not history_complete(state, last_draw)):\n            continue\n        variant = state.variant\n        statuses = job.statuses[variant.identity]\n        statuses[records.game_id] = with_eligibility(\n            state.status, last_draw + 1,",
     "        if (state.status.withdrawn_from is not None\n                or not history_complete(state, last_draw)):\n            continue\n        variant = state.variant\n        statuses = job.statuses[variant.identity]\n        statuses[records.game_id] = with_eligibility(\n            type(state.status)(), last_draw + 1,",
     'test_research_job.TheExamplesOfSection72.test_qa_as_prods_mirror_keeps_a_copied_eligibility_draw_however_many_draws_arrive'),
    ('scores are written at a draw the results are withheld from', 'research_job.py',
     "    withheld = records.withheld(draw)\n",
     "    withheld = False\n",
     'test_research_ov1_and_checks.TheDerivedCheck.test_one_stored_score_altered_is_found_at_its_draw_and_nothing_is_written_from_it'),
    ('stale reports are left in the active folder', 'research_job.py',
     "        moved = reports.set_aside_from(records.tree_root, records.game_id, draw)",
     "        moved = 0",
     'test_research_ov1_and_checks.TheDerivedCheck.test_one_ledger_line_altered_is_found_at_its_draw'),
    ('the derived check does not compare the scores', 'derived_check.py',
     "            if rebuilt != state.score_contents[target]:",
     "            if False:",
     'test_research_ov1_and_checks.TheDerivedCheck.test_a_planted_change_to_the_scoring_code_is_found_at_the_draw_it_changes'),
    ('the derived check does not compare the ledger', 'derived_check.py',
     "        if rebuilt != stored:\n            note(draw, f'the prevailing line for draw {draw} is not what",
     "        if False:\n            note(draw, f'the prevailing line for draw {draw} is not what",
     'test_research_ov1_and_checks.TheDerivedCheck.test_one_ledger_line_altered_is_found_at_its_draw'),
    ('a held variant does not mark the derived results', 'derived_check.py',
     "        if state.held:\n            note(state.first_target,",
     "        if state.held:\n            continue\n            note(state.first_target,",
     'test_research_ov1_and_checks.TheDerivedCheck.test_a_variant_whose_list_became_foreign_is_held_and_what_was_built_with_it_is_set_aside'),
    ('a catch-up clears the marker without the full check', 'derived_check.py',
     "    found = first_mismatch(records)\n    if found is None:\n        remove_cutoff(",
     "    found = None\n    if found is None:\n        remove_cutoff(",
     'test_research_ov1_and_checks.CatchUpAfterAStoppedRerun.test_a_catch_up_never_clears_a_real_mismatch'),
    ('a list made by other variant files is not found foreign', 'game_state.py',
     "        if listed.header.get('variant_fingerprint') != variant.fingerprint:",
     "        if False:",
     'test_research_ov1_and_checks.TheDerivedCheck.test_a_variant_whose_list_became_foreign_is_held_and_what_was_built_with_it_is_set_aside'),
    ('a list made under other forecasting code is not found foreign', 'game_state.py',
     "        elif listed.header.get('forecasting_code_identity') != forecasting_code_identity:",
     "        elif False:",
     'test_research_ov1_and_checks.TheDerivedCheck.test_lists_made_under_other_shared_forecasting_code_are_all_foreign'),
    ('a blocked prevailing line is skipped', 'ov1_ledger.py',
     "        if score is None:\n            raise Blocked(f'draw {draw}: the forecast of {identity} is not scored yet')",
     "        if score is None:\n            continue",
     'test_research_ov1_and_checks.PrevailingLines.test_a_missing_member_blocks_the_line_which_is_never_skipped'),
    ('the WORST sets are left out of the weights', 'ov1_ledger.py',
     "            weights[number - barrel.low] -= 1",
     "            weights[number - barrel.low] -= 0",
     'test_research_ov1_and_checks.PrevailingLines.test_each_line_holds_the_weights_x_and_factors_of_its_counted_pairs_as_the_kernel_gives_them'),
    ('a NO_FORECAST member is dropped from the cohort record', 'ov1_ledger.py',
     "            members.append({'variant': identity, 'state': NO_PAIR, 'reason': facts.reason})\n            continue",
     "            continue",
     'test_research_ov1_and_checks.PrevailingLines.test_a_cohort_member_with_no_forecast_is_recorded_as_no_pair_with_its_reason'),
    ('results changed other than by growing are not looked for', 'research_job.py',
     "    check_results_only_grew(records)\n",
     "",
     'test_research_job.TheResultsStep.test_results_changed_other_than_by_growing_refuse_the_game_and_name_the_draw'),
    ('the copy accepts results that are not these grown longer', 'results_step.py',
     "    if not source.raw.startswith(here):",
     "    if False:",
     'test_research_job.TheResultsStep.test_a_source_that_is_not_these_results_grown_longer_is_refused_and_nothing_is_copied'),
    ('an environmental fault is recorded as a method failure', 'forecast_engine.py',
     "    except MethodFailed as failure:",
     "    except Exception as failure:",
     'test_research_job.Records.test_any_other_exception_writes_no_line_and_stops_the_game'),
    ('a torn last line is not cut before the next append', 'research_job.py',
     "        lists.cut_torn_tail(state.forecasts)\n",
     "",
     'test_research_job.Records.test_a_torn_last_line_in_each_file_is_cut_and_redone'),
    ('the orphan marker is not looked for', 'research_job.py',
     "        check_no_orphan_marker(settings.tree_root)\n",
     "",
     'test_research_job.StartingAndStopping.test_an_orphan_marker_blocks_the_launch'),
    ('the withdrawal does not hold the updater\'s lock', 'withdraw.py',
     "        with job_lock(tree_root, 'withdrawal', stamp), updater_lock(tree_root, 'withdrawal', stamp):",
     "        with job_lock(tree_root, 'withdrawal', stamp):",
     'test_research_ov1_and_checks.Withdrawal.test_from_before_the_draw_is_shown_until_the_file_is_written_both_locks_are_held'),
    ('the withdrawal writes without the typed word', 'withdraw.py',
     "                    != CONFIRMATION_WORD:",
     "                    == 'never':",
     'test_research_ov1_and_checks.Withdrawal.test_without_the_typed_word_or_when_refused_nothing_is_written'),
    ('the league report counts a draw twice', 'reports.py',
     "            row['draws'] += 1\n",
     "            row['draws'] += 2\n",
     'test_research_job.Reports.test_the_league_figures_are_those_of_the_score_list'),
    ('a report file is rewritten though nothing changed', 'reports.py',
     "        if path.is_file() and path.read_bytes() == data:\n            return False",
     "        if False:\n            return False",
     'test_research_job.Reports.test_the_same_records_give_the_same_report_bytes'),
    ('the claim\'s words are altered', 'reports.py',
     "is at most 2.5%. '", "is at most 5%. '",
     'test_research_ov1_and_checks.TheFixedTexts.test_the_claim_and_the_exploratory_heading_are_the_specifications_words'),
    ('the status file is written under a temporary name inside the variant folder (EX_283 F283-B01)', 'status_file.py',
     "    temporary = staging_folder_for(path) / staged_name(family, variant)     # checked again now that it exists",
     "    temporary = path.with_name(path.name + STAGING_SUFFIX)",
     'test_research_job.InterruptedStatusWrite.test_an_eligibility_write_interrupted_by_a_kill_a_failure_or_a_half_written_copy_is_continued'),
    ('an unfinished status copy is not removed at the next job', 'research_job.py',
     "    for leftover in discard_unfinished_writes(tree_root):",
     "    for leftover in []:",
     'test_research_job.InterruptedStatusWrite.test_an_eligibility_write_interrupted_by_a_kill_a_failure_or_a_half_written_copy_is_continued'),
    ('a staged ledger is put in place without checking that it names the results on file (EX_283 F283-B02)',
     'results_step.py',
     "    if ledger_names_results(incoming_ledger.read_bytes(), master.read_bytes()):",
     "    if True:",
     'test_research_job.InterruptedResultsCopy.test_every_state_a_crash_can_leave_is_finished_or_discarded_to_a_consistent_pair'),
    ('a staged results file is taken as proof that the copy went through', 'results_step.py',
     "    if incoming_master.exists():\n        if incoming_ledger.exists():\n            incoming_ledger.unlink()\n        incoming_master.unlink()",
     "    if incoming_master.exists():\n        if incoming_ledger.exists():\n            _put_in_place(incoming_ledger, ledger)\n        _put_in_place(incoming_master, master)\n        return None\n    if False:\n        incoming_master.unlink()",
     'test_research_job.InterruptedResultsCopy.test_a_kill_or_a_failure_at_every_step_of_the_copy_never_leaves_a_mixed_pair'),
    ('the league reports are not made again after the job\'s last changes', 'research_job.py',
     "    write_league_reports(job, records, writer, reported_through)\n",
     "",
     'test_research_job.Reports.test_an_eligibility_draw_written_at_the_end_of_a_job_shows_in_that_jobs_league_reports'),
    ('the cleanup removes whatever it finds in the staging folder (EX_285 F285-B01)', 'status_file.py',
     "    strangers = [entry.name for entry in entries if not is_staged_write(tree_root, entry)]",
     "    strangers = []",
     'test_research_job.TheStagingFolderIsTheTreesOwn.test_anything_else_in_the_staging_folder_survives_and_refuses_both_commands'),
    ('a staged name for a variant this tree does not hold is taken for the writer\'s own', 'status_file.py',
     "                and Path(tree_root).joinpath(*METHODS_PARTS, family, variant).is_dir())",
     "                and True)",
     'test_research_job.TheStagingFolderIsTheTreesOwn.test_anything_else_in_the_staging_folder_survives_and_refuses_both_commands'),
    ('a link or a junction is followed as if it were a folder of the tree (EX_285 F285-B01)', 'job_lock.py',
     "        if is_link(step):",
     "        if False:",
     'test_research_job.TheStagingFolderIsTheTreesOwn.test_a_staging_or_working_folder_linked_to_another_place_refuses_and_the_other_place_is_untouched'),
    ('the working folders are not checked before a job starts', 'research_job.py',
     "        check_working_folders(settings.tree_root)\n",
     "",
     'test_research_job.TheStagingFolderIsTheTreesOwn.test_a_results_folder_linked_to_another_place_refuses_before_anything_is_written_there'),
    ('the writer does not look at whether its staged name is a link', 'status_file.py',
     "    if is_link(temporary):",
     "    if False:",
     'test_research_job.TheStagingFolderIsTheTreesOwn.test_the_writer_refuses_a_staged_name_that_is_a_link_to_a_file_elsewhere'),
]


def sha256_of(path: Path) -> str:
    """The SHA-256 of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(tree: Path, python: str) -> int:
    """Plant each fault in turn in `tree` and report; returns 0 only if every one was caught."""
    engine = tree / 'src' / 'research'
    before = {path.name: sha256_of(path) for path in sorted(engine.glob('*.py'))}
    environment = dict(os.environ, PYTHONPATH=os.pathsep.join(['src', 'src/methods', 'tests']))
    caught = 0
    for number, (what, name, old, new, test) in enumerate(FAULTS, start=1):
        path = engine / name
        original = path.read_bytes()
        text = original.decode('utf-8')
        if text.count(old) != 1:
            print(f'{number:2d}  NOT PLANTED ({text.count(old)} places)  {what}  [{name}]')
            continue
        path.write_bytes(text.replace(old, new).encode('utf-8'))
        try:
            done = subprocess.run([python, '-B', '-m', 'unittest', test], cwd=tree, env=environment,
                                  capture_output=True, text=True)
        finally:
            path.write_bytes(original)
        verdict = 'CAUGHT' if done.returncode != 0 and ('FAILED' in done.stderr) else 'MISSED'
        caught += verdict == 'CAUGHT'
        print(f'{number:2d}  {verdict}  {what}  [{name}; {test.split(".")[-1]}]')
    restored = before == {path.name: sha256_of(path) for path in sorted(engine.glob('*.py'))}
    print(f'{caught} of {len(FAULTS)} planted faults caught; every file put back: {"yes" if restored else "NO"}')
    print('RESULT: PASS' if caught == len(FAULTS) and restored else 'RESULT: FAIL')
    return 0 if caught == len(FAULTS) and restored else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve(), sys.argv[2]))
