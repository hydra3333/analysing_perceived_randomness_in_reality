"""The research job: what Run_Research.bat runs, for one game or both, in any tree.

What this file is for
    One job does everything routine, and the same in every tree. For each game it reads what the tree holds,
    deletes what is out of date (and only that), forecasts every draw a method has no line for, the next draw
    included, scores every forecast whose result is on file, and makes the league, the reports and both OV-1
    series again. What to do is always read from the files, never remembered, so an interrupted job is continued
    by running the same command again. Nothing is refused because it differs: a difference means "make that part
    again". The games are worked one after the other and never mixed.

    What is out of date:
      the engine changed (the infrastructure's fingerprint is not the one kept beside the results), or
      --rebuild-all was given: every method's results, in both games;
      a method's files changed (its fingerprint is not the one in the first line of its stored lists), its lists
      cannot be read, or --rebuild names it: that method's results;
      a draw's result was corrected at the source: that draw's scores, and every forecast that was computed
      from it (found from the permitted-view digest each forecast holds), with their scores.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 5. Arriving with later steps of the work order:
    the results updater at the job's start (step 3); the new settings file, the lock and the backup at the job's
    end (step 4).

Which of the project's own modules it uses
    research.settings          read_settings: the tree's role and paths
    research.job_lock          the job lock
    research.code_identity     the infrastructure's fingerprint
    research.variant_folders   find_variants, load_method: the methods in the tree
    research.method_flags      the small files beside a method: retired, in place since
    research.game_state        the game's records in memory
    research.forecast_engine   compute_target: one forecast; view_digest_for: what it was computed from
    research.scoring           score_content: one score
    research.ov1_ledger        both OV-1 series
    research.reports           the saved reports
    research.variant_lists     the list files

What uses it
    src/research_command.py (the program behind Run_Research.bat), and the tests.
"""
from __future__ import annotations

import argparse
import platform
import shutil
import traceback
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

from research import code_identity, method_flags, ov1_ledger, reports
from research import variant_lists as lists
from research.forecast_engine import FORECAST, compute_target, content_digest, view_digest_for
from research.game_state import (MAIN_BARREL, GameRecords, VariantState, lists_of_variants_not_installed,
                                 load_variant_state, summarise_target_line)
from research.job_lock import LaunchRefused, check_no_orphan_marker, check_working_folders, job_lock
from research.reader import ResultsRefused, results_on_file
from research.scoring import score_content
from research.settings import SettingsRefused, TreeSettings, read_settings
from research.variant_folders import VariantRefused, find_variants, load_method

# The games, in the order a job for BOTH works them. They are never pooled.
GAMES = ('POWERBALL', 'OZLOTTO')
# Where a tree keeps its methods, from the tree root.
METHODS_FOLDER = 'src/methods'
# The job log: one line a job, under the tree's records folder.
JOB_LOG = 'records/JOB_LOG.jsonl'
# During a long fill the job says how far it has got after every so many draws in which it wrote something.
PROGRESS_EVERY_DRAWS = 25
# The job's exit codes: finished; a game stopped or a method failed; the job itself refused before any game.
EXIT_FINISHED, EXIT_GAME_STOPPED, EXIT_REFUSED = 0, 1, 2
# The stops of one game that are understood: said in one line, with no traceback.
GAME_REFUSALS = (ResultsRefused, LaunchRefused)


def no_checkpoint(label: str) -> None:
    """The checkpoint of an ordinary job: nothing. A test passes its own, to stop the job between two writes."""


@dataclass
class Job:
    """What one run of the job knows that is the same for every game.

    settings: the tree's settings.  variants: the methods in the tree.
    rebuild: the identities --rebuild names (empty if none).  no_update: True to leave the updater out.
    now: gives the present time (UTC); a test passes a fixed one.  say: prints one line for the owner.
    checkpoint: called with a label after each kind of write; see no_checkpoint.
    warnings: every warning said so far, to be said again at the end.  counts: {game: Counter of what was written}.
    rebuilt: what was deleted to be made again, and why, one text each.  failed: each method whose calculation
    failed in this job, and why, one text each.  methods: the imported method programs.
    """
    settings: TreeSettings
    variants: tuple
    rebuild: frozenset
    no_update: bool
    now: object
    say: object
    checkpoint: object = no_checkpoint
    warnings: list = field(default_factory=list)
    counts: dict = field(default_factory=dict)
    rebuilt: list = field(default_factory=list)
    failed: list = field(default_factory=list)
    methods: dict = field(default_factory=dict)

    def warn(self, text: str) -> None:
        """Say a warning now and keep it to be said again at the end of the job."""
        self.warnings.append(text)
        self.say(f'WARNING: {text}')

    def note_rebuild(self, text: str) -> None:
        """Say what is being made again and why, and keep it for the job log."""
        self.rebuilt.append(text)
        self.say(f'REBUILD: {text}')

    def local_time(self) -> str:
        """The present time on the PC's clock, for the notes people read, for example '2026-12-01 20:10'."""
        return self.now().astimezone().strftime('%Y-%m-%d %H:%M')

    def utc_time(self) -> str:
        """The present time in UTC, for a line's envelope, for example '2026-12-01T09:40:12Z'."""
        return self.now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    def computed_in(self) -> dict:
        """Where a line is computed, for its envelope, for example {'role': 'PROD', 'tree_root': 'G:\\...'}."""
        return {'role': self.settings.role, 'tree_root': str(self.settings.tree_root)}

    def method_of(self, variant):
        """A method's imported method.py, imported once in a job."""
        if variant.identity not in self.methods:
            self.methods[variant.identity] = load_method(variant)
        return self.methods[variant.identity]

    def in_scope(self, records: GameRecords) -> list:
        """The methods of a game this job still computes for: those whose calculation has not failed in it."""
        return [state for state in records.workable if state.failed is None]


def delete_method_results(job: Job, game_id: str, variant, why: str) -> None:
    """Delete one method's stored results for a game, to be filled again from its starting draw."""
    folder = lists.variant_folder(job.settings.tree_root, game_id, variant.family, variant.variant)
    if folder.is_dir():
        shutil.rmtree(folder)
    job.note_rebuild(f'{game_id}: {variant.identity}: {why}')


def settle_infrastructure(job: Job, rebuild_all: bool) -> None:
    """Compare the engine in the tree with the one the tree's results were made with, and delete every method's
    results, in both games, if they differ or --rebuild-all was given. The fingerprint of the engine now in the
    tree is then kept beside the results. Results of methods that have no software in this tree are left alone.
    """
    tree_root = job.settings.tree_root
    current = code_identity.infrastructure_fingerprint(tree_root)
    stored = code_identity.stored_fingerprint(tree_root)
    research = tree_root / lists.RESEARCH_FOLDER
    with_results = [(game_id, variant) for game_id in GAMES for variant in job.variants
                    if lists.variant_folder(tree_root, game_id, variant.family, variant.variant).is_dir()]
    why = ('--rebuild-all was given' if rebuild_all
           else None if stored == current
           else 'the engine is not the one these results were made with' if stored is not None
           else 'nothing says which engine made these results' if with_results else None)
    if why is not None:
        for game_id, variant in with_results:
            shutil.rmtree(lists.variant_folder(tree_root, game_id, variant.family, variant.variant))
        for game_id in GAMES:
            for folder in ('ov1', reports.REPORTS_FOLDER):
                if (research / game_id / folder).is_dir():
                    shutil.rmtree(research / game_id / folder)
        job.note_rebuild(f'everything, in both games ({len(with_results)} stored method results deleted): {why}. '
                         f'A game this job does not work is filled again by the next job that works it.')
    if stored != current:
        code_identity.store_fingerprint(tree_root, current)


def drop_what_results_no_longer_support(job: Job, records: GameRecords, state: VariantState) -> bool:
    """Drop the lines of one method that the results on file no longer support, so that they are made again.

    Every forecast holds the digest of the draws it was computed from. If the newest one no longer matches the
    results, the first one that does not is found, and it and every later forecast are dropped with their
    scores. Every stored score is worked out again from its forecast and the result on file now; the first one
    that comes out otherwise is dropped, with every later score. Lines beyond the results on file (results that
    became shorter) are dropped the same way.
    Returns True if anything was dropped from the files (the caller then reads the method's lists again).
    """
    if not state.targets:
        return False
    results, game_id = records.results, records.game_id
    newest = state.next_target - 1
    first_bad_forecast = None
    if newest > results.last_draw + 1:
        first_bad_forecast, newest = results.last_draw + 2, results.last_draw + 1
    if (newest >= state.first_target
            and view_digest_for(state.variant, results, newest) != state.targets[newest].view_digest):
        low, high = state.first_target, newest              # the lowest target whose view no longer matches
        while low < high:
            middle = (low + high) // 2
            if view_digest_for(state.variant, results, middle) == state.targets[middle].view_digest:
                low = middle + 1
            else:
                high = middle
        first_bad_forecast = low
    first_bad_score = first_bad_forecast
    for target in sorted(state.score_contents):
        if first_bad_score is not None and target >= first_bad_score:
            break
        if target > results.last_draw or state.score_contents[target] != score_content(
                state.forecast_content(game_id, target), state.targets[target].content_digest,
                records.outcome_of(target)):
            first_bad_score = target
            break
    if first_bad_forecast is None and first_bad_score is None:
        return False
    variant = state.variant
    forecasts_path, scores_path = lists.variant_list_paths(records.tree_root, game_id, variant.family,
                                                           variant.variant)
    dropped = Counter()
    if first_bad_forecast is not None:
        dropped['forecasts'] = lists.keep_below(forecasts_path, lists.FORECASTS_KIND, first_bad_forecast)
    if first_bad_score is not None:
        dropped['scores'] = lists.keep_below(scores_path, lists.SCORES_KIND, first_bad_score)
    job.note_rebuild(f'{game_id}: {variant.identity}: the results on file are no longer what its lines were made '
                     f'from: {dropped["forecasts"]} forecasts (from draw {first_bad_forecast}) and '
                     f'{dropped["scores"]} scores (from draw {first_bad_score}) dropped')
    return True


def drop_beyond_retirement(job: Job, records: GameRecords, state: VariantState) -> bool:
    """Drop what a retired method holds past its retirement draw: forecasts for later draws, and scores for the
    retirement draw or later (its forecast for the retirement draw itself stays, unscored, as it was made).
    Returns True if anything was dropped."""
    retired_from = state.status.withdrawn_from
    if retired_from is None or not state.targets:
        return False
    if state.next_target - 1 <= retired_from and all(target < retired_from for target in state.score_contents):
        return False
    variant = state.variant
    forecasts_path, scores_path = lists.variant_list_paths(records.tree_root, records.game_id, variant.family,
                                                           variant.variant)
    forecasts = lists.keep_below(forecasts_path, lists.FORECASTS_KIND, retired_from + 1)
    scores = lists.keep_below(scores_path, lists.SCORES_KIND, retired_from)
    job.note_rebuild(f'{records.game_id}: {variant.identity}: retired from draw {retired_from}: {forecasts} later '
                     f'forecasts and {scores} scores dropped')
    return True


def open_game(job: Job, game_id: str) -> GameRecords:
    """Read one game: the results, the methods' small files and lists; delete what is out of date.

    Returns the game's records in memory. Stops the game (ResultsRefused) only if the results on file cannot be
    read. A method whose small files cannot be read is reported and passed over.
    """
    tree_root = job.settings.tree_root
    results = results_on_file(tree_root, game_id)
    records = GameRecords(game_id=game_id, tree_root=tree_root, role=job.settings.role, results=results,
                          states=[], foreign=[])
    in_tree = set()
    for variant in job.variants:
        if not variant.supports(game_id):
            continue
        in_tree.add(variant.identity)
        try:
            method_flags.settle_retired(variant.folder, game_id, results.last_draw)
            status = method_flags.status_of(variant.folder, game_id)
        except method_flags.FlagFault as fault:
            job.warn(f'{game_id}: {variant.identity} is passed over: {fault}')
            job.failed.append(f'{game_id}: {variant.identity}: passed over: {fault}')
            continue
        state, stale = load_variant_state(tree_root, game_id, variant, status)
        if variant.identity in job.rebuild and (state.targets or stale):
            stale = '--rebuild names it'
        if stale:
            delete_method_results(job, game_id, variant, stale)
            state, _ = load_variant_state(tree_root, game_id, variant, status)
        if method_flags.settle_in_place(variant.folder, variant.fingerprint, game_id, results.last_draw):
            state.status = method_flags.status_of(variant.folder, game_id)
        dropped = drop_what_results_no_longer_support(job, records, state)
        dropped = drop_beyond_retirement(job, records, state) or dropped
        if dropped:
            status = state.status
            state, _ = load_variant_state(tree_root, game_id, variant, status)
        records.states.append(state)
    records.foreign = lists_of_variants_not_installed(tree_root, game_id, in_tree)
    for identity in records.foreign:
        job.warn(f'{game_id}: stored results of {identity} are left alone: this tree has no software for it. They '
                 f'count in no report and in neither OV-1 series.')
    return records


def append_forecasts(job: Job, records: GameRecords, draw: int) -> None:
    """Write the TARGET line for a draw for every method that is due one.

    A method is due one when the draw is its next target and it is not retired from a draw at or below it. The
    lines are made durable before this returns. A method whose calculation raises anything but its declared
    failure writes no line: it is reported, and passed over for the rest of this job in this game.
    """
    game_id, results, touched = records.game_id, records.results, []
    for state in job.in_scope(records):
        if state.next_target != draw or state.status.is_withdrawn_at(draw):
            continue
        variant = state.variant
        try:
            content, detail = compute_target(variant, job.method_of(variant), results, draw)
        except Exception as fault:              # a failed calculation is never recorded as a result
            state.failed = f'{type(fault).__name__}: {fault}'
            job.failed.append(f'{game_id}: {variant.identity}: its forecast for draw {draw} failed: {state.failed}')
            job.warn(f'{game_id}: {variant.identity}: its forecast for draw {draw} failed and no line was written '
                     f'({state.failed}). It is passed over for the rest of this job; the next job tries again.')
            job.say(traceback.format_exc())
            continue
        if state.forecasts is None:
            path = lists.variant_list_paths(records.tree_root, game_id, variant.family, variant.variant)[0]
            state.forecasts = lists.create_list(path, lists.make_header(
                lists.FORECASTS_KIND, game_id, variant.family, variant.variant, variant.fingerprint,
                state.first_target))
        lists.cut_torn_tail(state.forecasts)
        envelope = {'results_version': results.version, 'results_sha256': results.sha256,
                    'computed_in': job.computed_in(), 'target_result_on_file': draw <= results.last_draw,
                    'time': job.utc_time()}
        if detail is not None:
            envelope['detail'] = detail
        # The content's digest is kept because a score names the forecast it scored by it. Nothing checks it.
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
    """Write the score line for a draw for every method whose FORECAST for it is not scored: never for a method
    retired from a draw at or below it. The lines are made durable before this returns."""
    game_id, results, touched = records.game_id, records.results, []
    for state in job.in_scope(records):
        facts = state.targets.get(draw)
        if (facts is None or facts.status != FORECAST or draw in state.score_contents
                or state.status.is_withdrawn_at(draw)):
            continue
        variant = state.variant
        content = score_content(state.forecast_content(game_id, draw), facts.content_digest,
                                records.outcome_of(draw))
        if state.scores is None:
            path = lists.variant_list_paths(records.tree_root, game_id, variant.family, variant.variant)[1]
            state.scores = lists.create_list(path, lists.make_header(
                lists.SCORES_KIND, game_id, variant.family, variant.variant, variant.fingerprint))
        lists.cut_torn_tail(state.scores)
        envelope = {'results_version': results.version, 'results_sha256': results.sha256,
                    'computed_in': job.computed_in(), 'time': job.utc_time()}
        lists.append_line(state.scores, {'line': lists.SCORE_LINE, 'content': content, 'envelope': envelope})
        state.score_contents[draw] = content
        state.scores.lines = []
        touched.append(state.scores)
        job.counts[game_id]['scores'] += 1
        job.checkpoint('score line written')
    for listed in touched:
        lists.sync_list(listed)


def complete_draw(job: Job, records: GameRecords, draw: int) -> None:
    """Do everything that is due for one draw: forecast lines, then score lines. Each part is skipped if already
    done. For a draw whose result is not on file only the forecasts are made."""
    append_forecasts(job, records, draw)
    if draw <= records.results.last_draw:
        append_scores(job, records, draw)


def make_series_and_reports(job: Job, records: GameRecords) -> None:
    """Make both OV-1 series, the league report of every draw, the next-draw reports and the README again from
    the records as they now stand, and write each file whose bytes differ."""
    game_id, last_draw = records.game_id, records.results.last_draw
    written = job.counts[game_id]
    writer = reports.ReportWriter(records.tree_root, game_id, job.local_time())
    main_drawn = {draw: records.outcome_of(draw)[MAIN_BARREL]
                  for state in records.states for draw in state.score_contents if draw <= last_draw}
    exploratory = ov1_ledger.exploratory_series(game_id, records.states, main_drawn, last_draw)
    records.ledger_lines, records.blocked = ov1_ledger.prevailing_series(
        game_id, records.states, lambda draw: records.outcome_of(draw)[MAIN_BARREL], last_draw)
    if records.blocked:
        job.warn(f'{game_id}: the second OV-1 series stops early: {records.blocked}')
    written['series files'] += ov1_ledger.write_series(records.tree_root, game_id, records.ledger_lines, exploratory)
    league = reports.LeagueTable(records)
    lowest = min((state.first_target for state in records.workable), default=last_draw + 1)
    for draw in range(lowest, last_draw + 1):
        if league.add_draw(draw):
            for name, content in zip(reports.league_names(game_id, draw), league.render(draw)):
                written['report files'] += writer.write(name, content)
    made_before_result = sorted({target for state in records.workable for target, facts in state.targets.items()
                                 if not facts.result_on_file})
    for draw in made_before_result:
        for name, content in zip(reports.next_draw_names(game_id, draw), reports.next_draw_report(records, draw)):
            written['report files'] += writer.write(name, content)
    for name, content in zip(reports.ov1_names(game_id, 'exploratory'),
                             reports.exploratory_report(records, exploratory)):
        written['report files'] += writer.write(name, content)
    for name, content in zip(reports.ov1_names(game_id, 'prevailing'), reports.prevailing_report(records)):
        written['report files'] += writer.write(name, content)
    writer.write(reports.README_NAME, reports.readme_text(game_id))
    writer.tidy_times()


def run_game(job: Job, game_id: str) -> str:
    """The whole job for one game: read, delete what is out of date, fill and catch up, make the reports.

    Returns the one line that says how the game finished. A fault passes through as an exception; whatever was
    written before it stays, and the same command continues from there.
    """
    job.counts[game_id] = Counter()
    records = open_game(job, game_id)
    last_draw = records.results.last_draw
    job.say(f'{game_id}: results on file through draw {last_draw}; {len(records.states)} methods in the tree')
    lowest = min((state.first_target for state in records.workable), default=last_draw + 1)
    written, said_at = job.counts[game_id], 0
    for draw in range(lowest, last_draw + 2):               # every draw on file, and the next draw's forecast
        complete_draw(job, records, draw)
        if (draw - lowest + 1) % PROGRESS_EVERY_DRAWS == 0 and written['forecasts'] + written['scores'] > said_at:
            said_at = written['forecasts'] + written['scores']
            job.say(f'{game_id}: worked through draw {draw} of {last_draw}; so far {written["forecasts"]} '
                    f'forecasts and {written["scores"]} scores written')
    make_series_and_reports(job, records)
    summary = ', '.join(f'{written[what]} {what}' for what in ('forecasts', 'scores', 'series files',
                                                               'report files'))
    failed = sum(1 for state in records.states if state.failed)
    return (f'{game_id}: finished{f" with {failed} methods failed" if failed else ""}. Results on file through '
            f'draw {last_draw}; written: {summary}. ' + reports.prevailing_status_line(records))


def environment_versions() -> dict:
    """The Python version and the version of every package in the environment, for the job log; for example
    {'python': '3.14.0', 'packages': {'numpy': '2.3.1', ...}}."""
    packages = {}
    for distribution in metadata.distributions():
        name = distribution.metadata['Name'] if distribution.metadata else None
        if name:
            packages[name] = distribution.version
    return {'python': platform.python_version(), 'packages': dict(sorted(packages.items()))}


def write_job_log(job: Job, games, started: str, endings: list, how: str) -> None:
    """Add this job's one line to the job log: the time, the Python and package versions, what was rebuilt and
    why, any method that failed with the reason, and how each game ended."""
    line = {'started': started, 'ended': job.local_time(), 'time_utc': job.utc_time(), 'how': how,
            'computed_in': job.computed_in(), 'games': list(games), 'no_update': job.no_update,
            'infrastructure_fingerprint': code_identity.stored_fingerprint(job.settings.tree_root),
            'rebuilt': job.rebuilt, 'failed': job.failed, 'warnings': job.warnings, 'endings': endings,
            'written': {game_id: dict(counts) for game_id, counts in job.counts.items()},
            **environment_versions()}
    path = job.settings.tree_root / JOB_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'ab') as stream:
        stream.write(lists.record_bytes(line))


def run(tree_root: Path, games, *, no_update: bool = False, rebuild=(), rebuild_all: bool = False, now=None,
        say=print, checkpoint=no_checkpoint) -> int:
    """Run the research job in a tree.

    tree_root: the tree's folder.  games: the games to work, for example ('POWERBALL', 'OZLOTTO').
    no_update: leave the results updater out.  rebuild: method identities ('E_002/RECUR_MEAN_ALL_V1') whose
    results are deleted and made again.  rebuild_all: delete and make again everything.
    now, say, checkpoint: see Job (a test passes its own).
    Returns the exit code: 0 finished; 1 a game stopped or a method's calculation failed (the rest is still
    worked); 2 the job itself refused before any game (the settings, a working folder that is not the tree's
    own, the job lock, an unknown --rebuild name).
    """
    now = now or (lambda: datetime.now(timezone.utc))
    tree_root = Path(tree_root)
    started = now().astimezone().strftime('%Y-%m-%d %H:%M')
    try:
        settings = read_settings(tree_root)
        say(f'RESEARCH JOB - START - {started} - the {settings.role} tree at {settings.tree_root}')
        say(f'About to work: {", ".join(games)}' + (' (results updater left out: --no-update)' if no_update else '')
            + (f'; rebuilding {", ".join(sorted(rebuild))} (--rebuild)' if rebuild else '')
            + ('; rebuilding everything (--rebuild-all)' if rebuild_all else ''))
        check_no_orphan_marker(settings.tree_root)
        check_working_folders(settings.tree_root)
        with job_lock(settings.tree_root, 'research job', started):
            return run_locked(settings, games, no_update, rebuild, rebuild_all, now, say, checkpoint, started)
    except (SettingsRefused, LaunchRefused, VariantRefused) as refusal:
        say(f'REFUSED: {refusal}')
        say('RESEARCH JOB - END - refused before any game was worked; nothing was written.')
        return EXIT_REFUSED


def run_locked(settings: TreeSettings, games, no_update: bool, rebuild, rebuild_all: bool, now, say, checkpoint,
               started: str) -> int:
    """The job once it holds the job lock: read the methods, settle the engine's fingerprint, then work each
    game. Arguments and result as for run()."""
    tree_root = settings.tree_root
    variants, refused = find_variants(tree_root / METHODS_FOLDER)
    unknown = sorted(set(rebuild) - {variant.identity for variant in variants})
    if unknown:
        raise VariantRefused(f'--rebuild names no method of this tree: {", ".join(unknown)}. Give each as '
                             f'<family>/<variant>, for example E_002/RECUR_MEAN_ALL_V1.')
    job = Job(settings=settings, variants=variants, rebuild=frozenset(rebuild), no_update=no_update, now=now,
              say=say, checkpoint=checkpoint)
    for name, why in refused:
        job.warn(f'the method folder {name} fails its checks and is passed over: {why}')
        job.failed.append(f'{name}: passed over: {why}')
    if not no_update:
        job.say('The results updater is not part of the job yet (it arrives with step 3 of the work order): this '
                'job works on the results on file.')
    settle_infrastructure(job, rebuild_all)
    endings, stopped = [], False
    for game_id in games:
        try:
            endings.append(run_game(job, game_id))
        except GAME_REFUSALS as refusal:
            stopped = True
            endings.append(f'{game_id}: STOPPED: {refusal}')
        except Exception as fault:              # anything else: a fault; no line was written for what failed
            stopped = True
            endings.append(f'{game_id}: STOPPED by a fault; no line was written for the step that failed. '
                           f'{type(fault).__name__}: {fault}. Running the job again tries again.')
            say(traceback.format_exc())
        say(endings[-1])
    say(f'RESEARCH JOB - END - {job.local_time()} - the {settings.role} tree at {settings.tree_root}')
    for ending in endings:
        say(ending)
    for text in job.rebuilt:
        say(f'REBUILT (said again): {text}')
    for warning in job.warnings:
        say(f'WARNING (said again): {warning}')
    not_clean = stopped or bool(job.failed)
    how = ('at least one game did not finish' if stopped
           else 'finished, but at least one method failed or was passed over' if job.failed else 'finished')
    write_job_log(job, games, started, endings, how)
    say('A STOP is a STOP: at least one game did not finish; nothing retries by itself.' if stopped
        else 'The job finished, but at least one method failed or was passed over: see the warnings above.'
        if job.failed else 'The job finished.')
    return EXIT_GAME_STOPPED if not_clean else EXIT_FINISHED


def main(arguments, tree_root: Path) -> int:
    """The command line of Run_Research.bat.

    arguments: what the owner typed after the command, for example ['--no-update'].
    tree_root: the tree the launcher lies in.  Returns the exit code of run().
    """
    parser = argparse.ArgumentParser(prog='Run_Research.bat', description='The research job.')
    parser.add_argument('--game', default='BOTH', choices=GAMES + ('BOTH',),
                        help='the game to work (default: BOTH)')
    parser.add_argument('--no-update', action='store_true', help='leave the results updater out')
    parser.add_argument('--rebuild', nargs='+', default=(), metavar='<family>/<variant>',
                        help='delete these methods\' results and make them again')
    parser.add_argument('--rebuild-all', action='store_true', help='delete every result and make it again')
    chosen = parser.parse_args(arguments)
    return run(tree_root, GAMES if chosen.game == 'BOTH' else (chosen.game,), no_update=chosen.no_update,
               rebuild=tuple(chosen.rebuild), rebuild_all=chosen.rebuild_all)
