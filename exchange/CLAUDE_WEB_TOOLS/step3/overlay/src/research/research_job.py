"""The research job: what Run_Research.bat runs, for one game or both, in any tree.

What this file is for
    One job does everything routine. For each game it reads what the tree already holds, forecasts every draw a
    variant has no line for, scores every forecast whose result is on file, writes the prevailing OV-1 line of
    each draw, saves the reports, fetches or copies new results, catches up draw by draw, and forecasts the next
    draw. What to do next is always read from the files, never remembered, so an interrupted job is continued by
    running the same command again. The games are worked one after the other and never mixed.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 7.1 and 7.2 (the job and its examples), 5.3
    (what writes no line and stops the game), 5.6A (foreign lists and held variants), 5.7 (crash resume and the
    write order of a draw), 5.8 (the derived check is honoured), 10.2 (the eligibility draw) and 10.4 (the
    prevailing line). The tree's own checks at the start of a job (its environment, its installed files, the
    process rule) are the launch guard's. Not yet here, arriving with build step 3: the "backup due" flag, the
    end-of-job backup and the updater's launch in PROD.

Which of the project's own modules it uses
    research.settings          read_settings: the tree's role and paths
    research.job_lock          the job lock and the orphan-marker check
    research.code_identity     the code identities quoted in every line
    research.launch_guard      check_at_job_start: the tree's own checks, and the environment's digest
    research.snapshot          the note that a backup is owed, and the backup at the job's end (QA and PROD)
    research.variant_folders   find_variants, load_method: the installed variants
    research.status_file       the variants' status files (read; created in DEV; the eligibility draw written)
    research.game_state        the game's records in memory
    research.forecast_engine   compute_target: one forecast
    research.scoring           score_content: one score
    research.ov1_ledger        draw_line: one prevailing line
    research.derived_check     the full check and the not-current marker
    research.results_step      the checked copy of the results
    research.reports           the saved reports
    research.variant_lists     the list files

What uses it
    src/research_command.py (the program behind Run_Research.bat), and the engine's tests.
"""
from __future__ import annotations

import argparse
import traceback
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from research import derived_check, ov1_ledger, reports
from research import variant_lists as lists
from research.code_identity import ManifestRefused, derived_code_digest, forecasting_code_identity, read_manifest
from research.forecast_engine import FORECAST, compute_target, content_digest, view_digest_for
from research.game_state import (MAIN_BARREL, GameRecords, VariantState, lists_of_variants_not_installed,
                                 load_variant_state, summarise_target_line)
from research.launch_guard import check_at_job_start
from research.snapshot import backup_for_a_job, mark_due
from research.job_lock import LaunchRefused, check_no_orphan_marker, check_working_folders, job_lock
from research.reader import ResultsRefused, results_on_file
from research.results_step import copy_results, finish_interrupted_copy
from research.scoring import score_content
from research.settings import SettingsRefused, TreeSettings, read_settings
from research.status_file import (STATUS_FILE_NAME, StatusRefused, create_active, discard_unfinished_writes,
                                  read_status, with_eligibility, write_status)
from research.variant_folders import VariantRefused, find_variants, load_method

# The games, in the order a job for BOTH works them. They are never pooled.
GAMES = ('POWERBALL', 'OZLOTTO')
# Where a tree keeps its variants, from the tree root.
METHODS_FOLDER = 'src/methods'
# During a long fill the job says how far it has got after every so many draws in which it wrote something.
PROGRESS_EVERY_DRAWS = 25
# The job's exit codes: finished; a game refused or stopped; the job itself refused before any game.
EXIT_FINISHED, EXIT_GAME_STOPPED, EXIT_REFUSED = 0, 1, 2
# The refusals of one game that are understood: said in one line, with no traceback.
GAME_REFUSALS = (lists.ListFault, ResultsRefused, StatusRefused, derived_check.CutoffRefused, VariantRefused,
                 LaunchRefused)


def no_checkpoint(label: str) -> None:
    """The checkpoint of an ordinary job: nothing. A test passes its own, to stop the job between two writes."""


@dataclass
class Job:
    """What one run of the job knows that is the same for every game.

    settings: the tree's settings.  variants: the installed variants.  statuses: {identity: {game: GameStatus}}.
    status_refusals: {identity: why its status file was refused}.
    forecasting_code_identity, derived_code_digest, environment_digest: the identities quoted in lines.
    only: None, or the identities the job is limited to (--only).  no_update: True to leave the results step out.
    now: gives the present time (UTC); a test passes a fixed one.  say: prints one line for the owner.
    checkpoint: called with a label after each kind of write; see no_checkpoint.
    warnings: every warning said so far, to be said again at the end.  counts: {game: Counter of what was written}.
    """
    settings: TreeSettings
    variants: tuple
    statuses: dict
    status_refusals: dict
    forecasting_code_identity: str
    derived_code_digest: str
    environment_digest: str
    only: frozenset | None
    no_update: bool
    now: object
    say: object
    checkpoint: object = no_checkpoint
    warnings: list = field(default_factory=list)
    counts: dict = field(default_factory=dict)
    methods: dict = field(default_factory=dict)

    def warn(self, text: str) -> None:
        """Say a warning now and keep it to be said again at the end of the job."""
        self.warnings.append(text)
        self.say(f'WARNING: {text}')

    def local_time(self) -> str:
        """The present time on the PC's clock, for the notes people read, for example '2026-12-01 20:10'."""
        return self.now().astimezone().strftime('%Y-%m-%d %H:%M')

    def utc_time(self) -> str:
        """The present time in UTC, for a line's envelope, for example '2026-12-01T09:40:12Z'."""
        return self.now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    def computed_in(self) -> dict:
        """Where a line is computed, for its envelope, for example {'role': 'PROD', 'tree_root': 'G:\\\\a_p_r_i_r'}."""
        return {'role': self.settings.role, 'tree_root': str(self.settings.tree_root)}

    def method_of(self, variant):
        """A variant's imported method.py, imported once in a job."""
        if variant.identity not in self.methods:
            self.methods[variant.identity] = load_method(variant)
        return self.methods[variant.identity]

    def in_scope(self, records: GameRecords) -> list:
        """The variants of a game this job computes for: not held, and named by --only if that was given."""
        return [state for state in records.workable if self.only is None or state.variant.identity in self.only]


def read_statuses(settings: TreeSettings, variants) -> tuple:
    """Read every installed variant's status file.

    Returns (statuses, refusals): {identity: {game: GameStatus}} and {identity: the refusal's text}. In DEV, where
    nothing is installed, a missing file is created as ACTIVE; in QA and PROD a missing file is a refusal
    (specification 3.5).
    """
    statuses, refusals = {}, {}
    for variant in variants:
        path = variant.folder / STATUS_FILE_NAME
        games = [game_id for game_id in GAMES if variant.supports(game_id)]
        try:
            if settings.role == 'DEV' and not path.exists():
                statuses[variant.identity] = create_active(path, variant.family, variant.variant, games)
            else:
                statuses[variant.identity] = read_status(path, games)
        except StatusRefused as refusal:
            refusals[variant.identity] = str(refusal)
    return statuses, refusals


def check_results_only_grew(records: GameRecords) -> None:
    """Refuse the game if the results on file changed other than by growing since its lists were written.

    Every TARGET line holds the digest of the draws before its target. The newest line of the variant that
    reaches furthest (one for each kind of view in use) is compared with the same digest taken from the results
    on file now. Refuses (ResultsRefused), naming the draw: results that end before a stored line's target, or
    an earlier draw whose row is no longer what a stored forecast was computed from.
    """
    furthest = {}
    for state in records.workable:
        view_kind = state.variant.declaration['observation_view']
        if state.targets and (view_kind not in furthest or state.next_target > furthest[view_kind].next_target):
            furthest[view_kind] = state
    results = records.results
    for state in furthest.values():
        newest = state.next_target - 1
        if newest > results.last_draw + 1:
            raise ResultsRefused(
                f'{records.game_id}: results changed other than by growing: {state.variant.identity} holds a line '
                f'for draw {newest}, but the results on file end at draw {results.last_draw}. Restore the results '
                f'from a backup; what to recompute otherwise is a reviewed decision.')
        if view_digest_for(state.variant, results, newest) == state.targets[newest].view_digest:
            continue
        low, high = state.first_target, newest          # the lowest target whose view no longer matches
        while low < high:
            middle = (low + high) // 2
            if view_digest_for(state.variant, results, middle) == state.targets[middle].view_digest:
                low = middle + 1
            else:
                high = middle
        raise ResultsRefused(
            f'{records.game_id}: results changed other than by growing: draw {low - 1}'
            f'{" or an earlier one" if low == state.first_target else ""} is no longer what the stored forecasts '
            f'were computed from (found from the lines of {state.variant.identity}). Restore the results from a '
            f'backup; what to recompute otherwise is a reviewed decision.')


def read_game(job: Job, game_id: str) -> GameRecords:
    """Read one game's records into memory, changing nothing: the results on file, each installed variant's
    lists with its status, the prevailing ledger and the marker NOT_CURRENT_FROM.json.

    Returns the game's records. Refuses with one of GAME_REFUSALS if they cannot be read: see the functions it
    calls. The job's Start step (open_game) reads through here, and so do the checks of an install and of
    Verify_Tree.bat (research/tree_checks.py), which must read exactly what the job reads and write nothing.
    """
    tree_root = job.settings.tree_root
    results = results_on_file(tree_root, game_id)
    states = []
    for variant in job.variants:
        if not variant.supports(game_id):
            continue
        if variant.identity in job.status_refusals:
            raise StatusRefused(f'a status file fails its check: {job.status_refusals[variant.identity]}')
        states.append(load_variant_state(tree_root, game_id, variant, job.statuses[variant.identity][game_id],
                                         job.forecasting_code_identity))
    ledger, ledger_lines = ov1_ledger.read_ledger(tree_root, game_id)
    return GameRecords(
        game_id=game_id, tree_root=tree_root, role=job.settings.role, results=results, states=states,
        foreign=lists_of_variants_not_installed(tree_root, game_id, {state.variant.identity for state in states}),
        forecasting_code_identity=job.forecasting_code_identity, derived_code_digest=job.derived_code_digest,
        environment_digest=job.environment_digest, ledger=ledger, ledger_lines=ledger_lines,
        cutoff=derived_check.read_cutoff(tree_root, game_id))


def open_game(job: Job, game_id: str) -> GameRecords:
    """The Start step for one game: finish or discard an interrupted copy of the results; read the game's
    records (read_game); name what is foreign; make the derived check.

    Returns the game's records in memory. Refuses with one of GAME_REFUSALS if the game cannot be worked: see
    the functions it calls.
    """
    unfinished = finish_interrupted_copy(job.settings.tree_root, game_id)
    if unfinished:
        job.say(unfinished)
    records = read_game(job, game_id)
    states = records.states
    for state in states:
        if state.held:
            job.warn(f'{game_id}: a list is foreign and is ignored: {state.variant.identity} '
                     f'({state.foreign_reason}). The variant is HELD: nothing is computed for it in {game_id}. '
                     f'To settle it: Rerun_Walk_Forward.bat --game {game_id} --only {state.variant.identity} '
                     f'(or reseed the research data; in QA, replace the software from PROD).')
    for identity in records.foreign:
        job.warn(f'{game_id}: a list is foreign and is ignored: {identity} (the variant is not installed here). '
                 f'It counts in no report and in neither OV-1.')
    check_results_only_grew(records)
    awaiting = records.cutoff is not None and records.cutoff[1] == derived_check.AWAITING_CATCH_UP
    derived_check.settle(records, derived_check.first_mismatch(records, records.cutoff[0] if awaiting else None))
    say_cutoff(job, records)
    return records


def say_cutoff(job: Job, records: GameRecords) -> None:
    """Say plainly what the not-current marker means for this game, and move stale reports out of view."""
    if records.cutoff is None:
        return
    draw, reason, detail = records.cutoff
    if reason == derived_check.MISMATCH:
        moved = reports.set_aside_from(records.tree_root, records.game_id, draw)
        job.warn(f'{records.game_id}: results not current from draw {draw}: {detail}. No score, prevailing line '
                 f'or report is written for draw {draw} or a later one; forecasts go on'
                 + (f'; {moved} stale report files were moved to reports/not_current' if moved else '')
                 + f'. To settle it: Rerun_Walk_Forward.bat --game {records.game_id} --from {draw} --derived-only '
                   f'(after a correction of shared code: the rerun for the variants it names).')
    else:
        job.say(f'{records.game_id}: a rerun was stopped before draw {draw}: this job catches up from draw {draw} '
                f'as for newly arrived draws.')


def append_forecasts(job: Job, records: GameRecords, draw: int) -> None:
    """Write the TARGET line for a draw for every variant in scope that is due one (specification 5.7).

    A variant is due one when the draw is its next target and it is not withdrawn from a draw at or below it.
    The lines are made durable before this returns. An exception from a method that is not its declared failure
    passes through: no line is written for that variant and the game stops.
    """
    game_id, results, touched = records.game_id, records.results, []
    for state in job.in_scope(records):
        if state.next_target != draw or state.status.is_withdrawn_at(draw):
            continue
        variant = state.variant
        content, detail = compute_target(variant, job.method_of(variant), results, draw)
        if state.forecasts is None:
            path = lists.variant_list_paths(records.tree_root, game_id, variant.family, variant.variant)[0]
            state.forecasts = lists.create_list(path, lists.make_header(
                lists.FORECASTS_KIND, game_id, variant.family, variant.variant, variant.fingerprint,
                job.forecasting_code_identity, state.first_target))
        lists.cut_torn_tail(state.forecasts)
        envelope = {'results_version': results.version, 'results_sha256': results.sha256,
                    'forecasting_code_identity': job.forecasting_code_identity,
                    'environment_digest': job.environment_digest, 'computed_in': job.computed_in(),
                    'target_result_on_file': draw <= results.last_draw, 'rerun': None, 'time': job.utc_time()}
        if detail is not None:
            envelope['detail'] = detail
        line = lists.append_line(state.forecasts, {'line': lists.TARGET_LINE, 'content': content,
                                                   'content_digest': content_digest(content), 'envelope': envelope})
        state.targets[draw] = summarise_target_line(line)
        state.forecasts.lines = []
        touched.append(state.forecasts)
        job.counts[game_id]['forecasts'] += 1
        job.checkpoint('forecast line written')
    for listed in touched:
        lists.sync_list(listed)


def append_scores(job: Job, records: GameRecords, draw: int) -> None:
    """Write the score line for a draw for every variant in scope whose FORECAST for it is not scored
    (specification 5.7, 8): never for a variant withdrawn from a draw at or below it. The lines are made durable
    before this returns."""
    game_id, results, touched = records.game_id, records.results, []
    for state in job.in_scope(records):
        facts = state.targets.get(draw)
        if (facts is None or facts.status != FORECAST or draw in state.score_contents
                or state.status.is_withdrawn_at(draw)):
            continue
        variant = state.variant
        content = score_content(state.forecast_content(game_id, draw), facts.content_digest,
                                derived_check.outcome_of(records, draw))
        if state.scores is None:
            path = lists.variant_list_paths(records.tree_root, game_id, variant.family, variant.variant)[1]
            state.scores = lists.create_list(path, lists.make_header(
                lists.SCORES_KIND, game_id, variant.family, variant.variant, variant.fingerprint,
                job.forecasting_code_identity))
        lists.cut_torn_tail(state.scores)
        envelope = {'results_version': results.version, 'results_sha256': results.sha256,
                    'scoring_code_digest': job.derived_code_digest, 'computed_in': job.computed_in(),
                    'rerun': None, 'time': job.utc_time()}
        lists.append_line(state.scores, {'line': lists.SCORE_LINE, 'content': content, 'envelope': envelope})
        state.score_contents[draw] = content
        state.scores.lines = []
        touched.append(state.scores)
        job.counts[game_id]['scores'] += 1
        job.checkpoint('score line written')
    for listed in touched:
        lists.sync_list(listed)


def append_prevailing_line(job: Job, records: GameRecords, draw: int) -> None:
    """Write the prevailing OV-1 line for a draw if it is the next one due (specification 10.4).

    Nothing is written before the prevailing score's start, out of order, or while a cohort member is not
    complete for the draw or is held: the line is then blocked, which is said once, naming the variant.
    """
    game_id = records.game_id
    start = ov1_ledger.prevailing_start(records.states)
    if start is None or draw != start + len(records.ledger_lines):
        return
    try:
        made = ov1_ledger.draw_line(game_id, draw, ov1_ledger.prevailing_cohort(records.states, draw),
                                    derived_check.outcome_of(records, draw)[MAIN_BARREL],
                                    ov1_ledger.running_logs_of(records.ledger_contents[-1]
                                                               if records.ledger_lines else None))
    except ov1_ledger.Blocked as blocked:
        if records.blocked is None:
            records.blocked = str(blocked)
            job.warn(f'{game_id}: the prevailing OV-1 line is blocked, not skipped: {blocked}. It is written by '
                     f'the first job that finds every counted variant complete for that draw.')
        return
    if records.ledger is None:
        records.ledger = lists.create_list(ov1_ledger.ledger_path(records.tree_root, game_id),
                                           ov1_ledger.ledger_header(game_id))
    lists.cut_torn_tail(records.ledger)
    envelope = {'results_version': records.results.version, 'results_sha256': records.results.sha256,
                'ov1_code_digest': job.derived_code_digest, 'computed_in': job.computed_in(), 'rerun': None,
                'time': job.utc_time()}
    line = lists.append_line(records.ledger, {'line': lists.PREVAILING_LINE, 'content': made['content'],
                                              'audit': made['audit'], 'envelope': envelope})
    lists.sync_list(records.ledger)
    records.ledger.lines = []
    records.ledger_lines.append(line)
    records.blocked = None
    job.counts[game_id]['prevailing lines'] += 1
    job.checkpoint('prevailing line written')


def complete_draw(job: Job, records: GameRecords, draw: int, league: reports.LeagueTable,
                  writer: reports.ReportWriter) -> None:
    """Do everything that is due for one draw, in the write order of specification 5.7: forecast lines, score
    lines, the prevailing OV-1 line, the league report. Each part is skipped if already done.

    This one function is the fill and the catch-up. For a draw whose result is not on file only the forecasts
    are made. Scores, the prevailing line and the report are left unwritten at a draw the derived results are
    withheld from (specification 5.8).
    """
    append_forecasts(job, records, draw)
    if draw > records.results.last_draw:
        return
    withheld = records.withheld(draw)
    if not withheld:
        append_scores(job, records, draw)
        append_prevailing_line(job, records, draw)
    if league.add_draw(draw) and not withheld:
        text, table = league.render(draw)
        for name, content in zip(reports.league_names(records.game_id, draw), (text, table)):
            job.counts[records.game_id]['report files'] += writer.write(name, content)
        job.checkpoint('league report written')


def history_complete(state: VariantState, last_draw: int) -> bool:
    """True if a variant has a line for every draw from its first target to the last on file and every FORECAST
    among them is scored (specification 10.2: "has its history complete")."""
    if state.held or state.first_target > last_draw + 1 or state.next_target <= last_draw:
        return False
    return all(target in state.score_contents for target, facts in state.targets.items()
               if facts.status == FORECAST and target <= last_draw)


def write_eligibility_draws(job: Job, records: GameRecords) -> None:
    """After a results step that succeeded: give every variant that has none, is not withdrawn and has its
    history complete its eligibility draw, the last draw on file plus one (specification 10.2). Written once;
    a value already in a status file is never changed."""
    last_draw = records.results.last_draw
    for state in records.states:
        if (state.status.eligible_from is not None or state.status.withdrawn_from is not None
                or not history_complete(state, last_draw)):
            continue
        variant = state.variant
        statuses = job.statuses[variant.identity]
        statuses[records.game_id] = with_eligibility(
            state.status, last_draw + 1,
            f'{job.local_time()}; results on file through {last_draw} after a successful results step')
        write_status(variant.folder / STATUS_FILE_NAME, variant.family, variant.variant, statuses)
        state.status = statuses[records.game_id]
        job.counts[records.game_id]['eligibility draws'] += 1
        job.checkpoint('eligibility draw written')


def everything_done(records: GameRecords) -> bool:
    """True if nothing is left to compute for any draw on file: every variant that is not held has its lines
    and scores through the last draw (or is withdrawn), and the prevailing ledger reaches it."""
    last_draw = records.results.last_draw
    for state in records.states:
        if state.held:
            return False
        stop = min(last_draw, state.status.withdrawn_from - 1) if state.status.withdrawn_from else last_draw
        if state.first_target <= stop and state.next_target <= stop:
            return False
        if any(facts.status == FORECAST and target <= stop and target not in state.score_contents
               for target, facts in state.targets.items()):
            return False
    start = ov1_ledger.prevailing_start(records.states)
    return start is None or start + len(records.ledger_lines) > last_draw


def write_league_reports(job: Job, records: GameRecords, writer: reports.ReportWriter, through: int) -> None:
    """Make every league report up to a draw again from the records as they now stand, and write those whose
    bytes differ. The reports written draw by draw during the job were made before the job's last changes (an
    eligibility draw written at its end shows in every league report), so this pass is what leaves the folder
    a function of the lists, the results and the status files alone."""
    league = reports.LeagueTable(records)
    lowest = min((state.first_target for state in records.workable), default=through + 1)
    for draw in range(lowest, through + 1):
        if league.add_draw(draw):
            for name, content in zip(reports.league_names(records.game_id, draw), league.render(draw)):
                job.counts[records.game_id]['report files'] += writer.write(name, content)


def finish_reports(job: Job, records: GameRecords, writer: reports.ReportWriter) -> None:
    """The End step's reports: every league report once more, the next-draw reports, the two OV-1 print-outs,
    the README and the side file of making times. Under a MISMATCH marker nothing is made for the marked draw or
    a later one, and the prevailing print-out is not made at all."""
    game_id, last_draw = records.game_id, records.results.last_draw
    mismatch_from = records.cutoff[0] if records.cutoff and records.cutoff[1] == derived_check.MISMATCH else None
    reported_through = last_draw if mismatch_from is None else min(last_draw, mismatch_from - 1)
    write_league_reports(job, records, writer, reported_through)
    made_before_result = sorted({target for state in records.workable for target, facts in state.targets.items()
                                 if not facts.result_on_file})
    for draw in made_before_result:
        if mismatch_from is None or draw < mismatch_from:
            for name, content in zip(reports.next_draw_names(game_id, draw), reports.next_draw_report(records, draw)):
                job.counts[game_id]['report files'] += writer.write(name, content)
    through = reported_through
    outcomes = {draw: derived_check.outcome_of(records, draw)[MAIN_BARREL]
                for state in records.workable for draw in state.score_contents if draw <= through}
    series = ov1_ledger.exploratory_series(game_id, records.states, outcomes, through)
    for name, content in zip(reports.ov1_names(game_id, 'exploratory'), reports.exploratory_report(records, series)):
        job.counts[game_id]['report files'] += writer.write(name, content)
    if mismatch_from is None:
        for name, content in zip(reports.ov1_names(game_id, 'prevailing'), reports.prevailing_report(records)):
            job.counts[game_id]['report files'] += writer.write(name, content)
    writer.write(reports.README_NAME, reports.readme_text(game_id))
    writer.tidy_times()


def run_game(job: Job, game_id: str) -> str:
    """The whole job for one game: Start, Fill, Results, Catch-up, End (specification 7.1).

    Returns the one line that says how the game finished. A refusal or a fault passes through as an exception;
    whatever was written before it stays, and the same command continues from there.
    """
    job.counts[game_id] = Counter()
    records = open_game(job, game_id)
    writer = reports.ReportWriter(records.tree_root, game_id, job.local_time())
    league = reports.LeagueTable(records)
    held = sum(1 for state in records.states if state.held)
    first_on_file = records.results.last_draw
    job.say(f'{game_id}: results on file through draw {first_on_file}; {len(records.states)} variants installed'
            + (f', {held} of them held' if held else '')
            + (f'; this job is limited to {len(job.in_scope(records))} of them (--only)' if job.only else ''))
    lowest = min((state.first_target for state in records.workable), default=first_on_file + 1)
    written, said_at = job.counts[game_id], 0
    for draw in range(lowest, first_on_file + 2):                       # the fill, and the next draw's forecast
        complete_draw(job, records, draw, league, writer)
        if (draw - lowest + 1) % PROGRESS_EVERY_DRAWS == 0 and written['forecasts'] + written['scores'] > said_at:
            said_at = written['forecasts'] + written['scores']
            job.say(f'{game_id}: worked through draw {draw} of {first_on_file}; so far {written["forecasts"]} '
                    f'forecasts and {written["scores"]} scores written')
    succeeded = False
    if job.no_update:
        job.say(f'{game_id}: the results step was left out (--no-update)')
    else:
        step = copy_results(job.settings, game_id, job.local_time())
        succeeded = step.succeeded
        if succeeded:
            job.say(step.message)
            records.results = results_on_file(records.tree_root, game_id)
        else:
            job.warn(step.message)
    last_draw = records.results.last_draw
    for draw in range(first_on_file + 1, last_draw + 1):                # the catch-up, one draw at a time
        complete_draw(job, records, draw, league, writer)
    if succeeded:
        write_eligibility_draws(job, records)
    complete_draw(job, records, last_draw + 1, league, writer)
    if (records.cutoff is not None and records.cutoff[1] == derived_check.AWAITING_CATCH_UP
            and everything_done(records)):
        message = derived_check.finish_catch_up(records)
        if records.cutoff is None:
            job.say(message)
        else:
            say_cutoff(job, records)
    finish_reports(job, records, writer)
    summary = ', '.join(f'{written[what]} {what}' for what in ('forecasts', 'scores', 'prevailing lines',
                                                               'eligibility draws', 'report files'))
    return (f'{game_id}: finished. Results on file through draw {last_draw}; written: {summary}. '
            + reports.prevailing_status_line(records))


def run(tree_root: Path, games, *, no_update: bool = False, only=None, now=None, say=print,
        checkpoint=no_checkpoint) -> int:
    """Run the research job in a tree.

    tree_root: the tree's folder.  games: the games to work, for example ('POWERBALL', 'OZLOTTO').
    no_update: leave the results step out.  only: None, or variant identities ('E_002/RECUR_MEAN_ALL_V1') the
    job is limited to.  now, say, checkpoint: see Job (a test passes its own).
    Returns the exit code: 0 finished; 1 a game refused or stopped (the other game is still worked); 2 the job
    itself refused before any game (the settings, the orphan marker, a working folder that is not the tree's
    own, the job lock, the launch guard's checks of the environment, the installed files and the process rule,
    the manifest, something foreign in the status staging folder, a variant folder, an
    unknown --only name).
    """
    now = now or (lambda: datetime.now(timezone.utc))
    tree_root = Path(tree_root)
    started = now().astimezone().strftime('%Y-%m-%d %H:%M')
    settings, reached = None, {'writing': False}         # how far THIS job got; never read from the tree
    try:
        settings = read_settings(tree_root)
        say(f'RESEARCH JOB - START - {started} - the {settings.role} tree at {settings.tree_root}')
        say(f'About to work: {", ".join(games)}' + (' (results step left out: --no-update)' if no_update else '')
            + (f'; limited to {", ".join(sorted(only))} (--only)' if only else ''))
        check_no_orphan_marker(settings.tree_root)
        check_working_folders(settings.tree_root)
        backup_for_a_job(settings, 'start', now, say)        # only if a backup is owed from earlier work
        with job_lock(settings.tree_root, 'research job', started):
            environment_digest = check_at_job_start(settings, say)
            exit_code, closing = run_locked(settings, games, no_update, only, now, say, checkpoint,
                                            environment_digest, reached)
        backup_for_a_job(settings, 'end', now, say)          # the job's lock is released: the tree is quiet
        say(f'RESEARCH JOB - END - {now().astimezone().strftime("%Y-%m-%d %H:%M")} - the {settings.role} tree at '
            f'{settings.tree_root}')                         # the time is read now, after the backup
        for line in closing:                                 # the job's own verdict stays the last thing said
            say(line)
        return exit_code
    except (SettingsRefused, LaunchRefused, ManifestRefused, VariantRefused, StatusRefused) as refusal:
        say(f'REFUSED: {refusal}')
        if not reached['writing']:                           # refused at a guard or a read-only check
            say('RESEARCH JOB - END - refused before any game was worked; nothing was written.')
        elif settings.backup_root is None:                   # DEV keeps no note and makes no backup
            say('RESEARCH JOB - END - refused before any game was worked. No research was written: no forecast, '
                'score or report. (If an interrupted status write was tidied away, a line above says so.)')
        else:
            # This job had written its note that a backup is owed before it was refused. Its lock is released:
            # the backup that is owed is tried, and if it cannot be made the standing warning is said.
            backup_for_a_job(settings, 'end', now, say)
            say('RESEARCH JOB - END - refused before any game was worked. No research was written: no forecast, '
                'score or report. This job had written the tree\'s note that a backup is owed, so the backup was '
                'tried (its result is above).')
        return EXIT_REFUSED


def run_locked(settings: TreeSettings, games, no_update: bool, only, now, say, checkpoint,
               environment_digest: str, reached: dict) -> tuple:
    """The job once it holds the job lock and the launch guard has passed: read the code's identities and the
    variants, then work each game. environment_digest: the digest of the tree's own Python environment, as the
    guard computed it for this job. The other arguments are as for run(). Returns (the exit code, the job's
    closing lines): run() says those lines, under its END line, after the job's lock is released and its backup
    has been attempted, so that the job's verdict is the last thing the owner reads. It reads and may refuse
    before it writes anything; its first write is the tree's note that a backup is owed.
    reached: the caller's own record of how far this job got; reached['writing'] is set True once the note is
    written (in DEV, where no note is kept, at the same point), before anything else is written or tidied."""
    tree_root = settings.tree_root
    manifest = read_manifest(tree_root)
    variants, refused = find_variants(tree_root / METHODS_FOLDER)
    if refused and settings.role != 'DEV':
        raise VariantRefused('a variant folder fails its checks: '
                             + '; '.join(f'{name}: {why}' for name, why in refused))
    installed = {variant.identity for variant in variants}
    unknown = sorted(set(only or ()) - installed)
    if unknown:
        raise VariantRefused(f'--only names no variant of this tree: {", ".join(unknown)}. Give each as '
                             f'<family>/<variant>, for example E_002/RECUR_MEAN_ALL_V1.')
    # Everything above only reads and may refuse: nothing has been written yet. From here the job writes: the
    # tree's note that a backup is owed comes first (QA and PROD), then the tidying of an interrupted status write.
    mark_due(settings)
    reached['writing'] = True
    for leftover in discard_unfinished_writes(tree_root):
        say(f'An earlier status write was interrupted before it changed anything; its unfinished copy was removed '
            f'({leftover}). The status file it was meant for is as it was.')
    statuses, status_refusals = read_statuses(settings, variants)
    job = Job(settings=settings, variants=variants, statuses=statuses, status_refusals=status_refusals,
              forecasting_code_identity=forecasting_code_identity(tree_root, manifest),
              derived_code_digest=derived_code_digest(tree_root, manifest), environment_digest=environment_digest,
              only=frozenset(only) if only else None, no_update=no_update, now=now, say=say, checkpoint=checkpoint)
    for name, why in refused:
        job.warn(f'the variant folder {name} fails its checks and is not run: {why}')
    endings, stopped = [], False
    for game_id in games:
        try:
            endings.append(run_game(job, game_id))
        except GAME_REFUSALS as refusal:
            stopped = True
            endings.append(f'{game_id}: REFUSED: {refusal}')
        except Exception as fault:              # anything else: an environmental fault; no line was written for it
            stopped = True
            endings.append(f'{game_id}: STOPPED by a fault; no line was written for the step that failed. '
                           f'{type(fault).__name__}: {fault}. Running the job again tries again.')
            say(traceback.format_exc())
        say(endings[-1])
    closing = [*endings, *(f'WARNING (said again): {warning}' for warning in job.warnings),
               'A STOP is a STOP: at least one game did not finish; nothing retries by itself.' if stopped
               else 'The job finished.']
    return (EXIT_GAME_STOPPED if stopped else EXIT_FINISHED), closing


def main(arguments, tree_root: Path) -> int:
    """The command line of Run_Research.bat.

    arguments: what the owner typed after the command, for example ['--game', 'BOTH', '--no-update'].
    tree_root: the tree the launcher lies in.  Returns the exit code of run().
    """
    parser = argparse.ArgumentParser(prog='Run_Research.bat', description='The research job (specification 7).')
    parser.add_argument('--game', required=True, choices=GAMES + ('BOTH',), help='the game to work, or BOTH')
    parser.add_argument('--no-update', action='store_true', help='leave the results step out')
    parser.add_argument('--only', nargs='+', metavar='<family>/<variant>', help='limit the job to these variants')
    chosen = parser.parse_args(arguments)
    return run(tree_root, GAMES if chosen.game == 'BOTH' else (chosen.game,), no_update=chosen.no_update,
               only=chosen.only)
