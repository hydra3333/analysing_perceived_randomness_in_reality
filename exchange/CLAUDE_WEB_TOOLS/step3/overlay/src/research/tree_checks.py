"""The checks that travel with the installed software: the smoke case, the forecast sample, the derived results.

What this file is for
    An install, an infrastructure reinstall and Verify_Tree.bat each ask three things of a tree's software with
    the tree's own Python: can every variant still compute one legal forecast here (the smoke case, on an
    invented results table, never a real draw); does a fixed sample of the stored forecasts come out the same
    when it is computed again; and is every stored score and prevailing OV-1 line what this software computes
    from the stored forecasts and the results on file. This file holds those three checks. They read; the only
    thing written is a smoke case's own small folder under the tree's scratch folder, which is removed when the
    smoke case passes and left, and named, when it fails.

    The software and the data may lie in two folders: an infrastructure reinstall asks these questions of the
    software as it would be (assembled in a temporary folder) against the data of the tree, before anything in
    the tree is overwritten. Everywhere else the two are the same tree.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 12.3 items 2, 4 and 5 (and 5.8 for what is
    compared); doc/Predictive_Randomness_Deployment_Design_v0_12.md section 3.3 items 4, 6 and 7, and section 6
    step 3.

Which of the project's own modules it uses
    _common.game_profiles     get_profile: a game's first draw and barrels, for the invented table
    research.code_identity    the identities of the software being asked
    research.derived_check    first_mismatch: the full comparison of the derived results
    research.environment_marker  MARKER_NAME, write_marker: at a tree's creation only
    research.forecast_engine  compute_target, content_digest: the ordinary engine
    research.job_lock         is_link: the scratch folder must be a real folder
    research.reader           ResultsOnFile, check_results_bytes, first_target, header_for
    research.reports          ReportWriter: the print-outs made again after an infrastructure reinstall
    research.research_job     GAMES, GAME_REFUSALS, METHODS_FOLDER, Job, check_results_only_grew, finish_reports,
                              read_game: a game's records as the job reads them, its own check that the
                              results on file only grew, and its own making of the reports
    research.settings         TreeSettings, read_settings
    research.status_file      read_status: a status file is read here and never created
    research.variant_folders  find_variants, load_method
    research.windows_text     LINE_ENDING

What uses it
    src/tree_checks_command.py (Verify_Tree.bat, and the install tools in DEV, which start that program with the
    target tree's Python), and the tests.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import shutil
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from _common.game_profiles import get_profile
from research import derived_check, environment_marker
from research.code_identity import ManifestRefused, derived_code_digest, forecasting_code_identity, read_manifest
from research.forecast_engine import FORECAST, compute_target, content_digest
from research.job_lock import LaunchRefused, is_link
from research.reader import ResultsOnFile, check_results_bytes, first_target, header_for
from research.reports import ReportWriter
from research.research_job import (GAME_REFUSALS, GAMES, METHODS_FOLDER, Job, check_results_only_grew, finish_reports,
                                   read_game)
from research.settings import SettingsRefused, TreeSettings, read_settings
from research.status_file import STATUS_FILE_NAME, StatusRefused, read_status
from research.variant_folders import find_variants, load_method
from research.windows_text import LINE_ENDING

# The tree's folder for smoke cases (deployment design section 2: "normally empty").
SCRATCH_FOLDER = 'scratch'
# The fixed seed of the invented table: the same table on every run, in every tree.
SMOKE_SEED = 'SMOKE_CASE_V1'
# The two files of a smoke case's folder: the invented table, and (only when it failed) what failed.
SMOKE_TABLE_NAME = 'invented_results.csv'
SMOKE_NOTE_NAME = 'WHAT_FAILED.txt'
# How many stored forecasts of one variant in one game are computed again: the first, the middle and the last.
SAMPLE_SIZE = 3
# The kind of the result file the `checks` command writes for the install tool that started it.
RESULT_KIND = 'TREE_CHECKS_V1'
# The word that asks for every variant's smoke case, and the word that asks for none.
ALL_VARIANTS, NO_VARIANT = 'ALL', 'NONE'
# The exit codes of the `checks` command: it ran to its end and wrote its result (whatever it found); it refused.
EXIT_RAN, EXIT_REFUSED = 0, 2


class ChecksRefused(ValueError):
    """The software or the data cannot be read well enough to be checked at all. The message says what was found
    and what to do."""


@dataclass
class Software:
    """The software being asked, read once.

    root: the folder its src/ and deploy/ lie in.  variants: its valid Variants.
    forecasting_code_identity, derived_code_digest: its two code identities.
    methods: {identity: the imported method.py}, filled as variants are first used.
    """
    root: Path
    variants: tuple
    forecasting_code_identity: str
    derived_code_digest: str
    methods: dict = field(default_factory=dict)

    def method_of(self, variant):
        """A variant's imported method.py, imported once."""
        if variant.identity not in self.methods:
            self.methods[variant.identity] = load_method(variant)
        return self.methods[variant.identity]


def read_software(software_root: Path) -> Software:
    """Read the variants and the code identities of the software in a folder.

    software_root: the tree, or the temporary folder holding the software as it would be.
    Refuses (ChecksRefused) if any variant folder fails its own checks: software with a broken variant folder
    is not installed software. (ManifestRefused is passed on: the manifest is missing or wrong.)
    """
    software_root = Path(software_root)
    variants, refused = find_variants(software_root / METHODS_FOLDER)
    if refused:
        raise ChecksRefused('a variant folder fails its checks: '
                            + '; '.join(f'{name}: {why}' for name, why in refused))
    manifest = read_manifest(software_root)
    return Software(root=software_root, variants=variants,
                    forecasting_code_identity=forecasting_code_identity(software_root, manifest),
                    derived_code_digest=derived_code_digest(software_root, manifest))


# ------------------------------------------------------------------------------------------- the smoke case

def invented_results(game_id: str, last_draw: int) -> ResultsOnFile:
    """An invented results table for a game, from the game's first draw to last_draw, held in memory.

    Every row comes from the fixed seed, the game and the draw number and from nothing else, so the table is the
    same on every run; no real draw is read. For example invented_results('POWERBALL', 1150) holds draws 1144 to
    1150, each with seven invented main numbers and one invented Powerball.
    """
    profile = get_profile(game_id)
    main = profile.barrels[0]
    rows = [','.join(header_for(game_id))]
    for draw in range(profile.first_draw, last_draw + 1):
        generator = random.Random(f'{SMOKE_SEED}:{game_id}:{draw}')
        drawn = generator.sample(range(main.low, main.high + 1), main.selected)
        if len(profile.barrels) > 1:
            second = profile.barrels[1]
            extra = [generator.randint(second.low, second.high)]
        else:
            extra = generator.sample([n for n in range(main.low, main.high + 1) if n not in drawn],
                                     profile.raw_supplementary_count)
        rows.append(','.join([str(draw), profile.derived_date(draw).isoformat()] + [str(n) for n in drawn + extra]))
    raw = ('\n'.join(rows) + '\n').encode('ascii')
    check_results_bytes(raw, game_id, 'the smoke case\'s invented table')
    return ResultsOnFile(game_id=game_id, raw=raw, sha256=hashlib.sha256(raw).hexdigest(),
                         first_draw=profile.first_draw, last_draw=last_draw, version=1)


def smoke_folder(data_root: Path, variant, game_id: str) -> Path:
    """The folder of one smoke case, for example <tree>/scratch/SMOKE_E_002_RECUR_MEAN_ALL_V1_POWERBALL."""
    return Path(data_root) / SCRATCH_FOLDER / f'SMOKE_{variant.family}_{variant.variant}_{game_id}'


def smoke_case(software: Software, data_root: Path, variant, game_id: str) -> str | None:
    """Make one variant forecast once for one game, on an invented table, through the ordinary engine.

    software: the software being asked.  data_root: the tree whose scratch folder is used.
    variant: the Variant.  game_id: a game it supports.
    The table runs from the game's first draw to the first draw the variant declares it can forecast, and that
    draw is the target: the declared minimum history, and not one draw more, must be enough.
    Returns None if the engine returned a complete FORECAST (a ranking and valid TOP and WORST sets for every
    barrel of the game: the engine's own readout has validated them). Otherwise one line saying what failed and
    naming the folder left behind, for example
        'E_002/X_V1 for POWERBALL: the smoke case failed: NO_FORECAST, INSUFFICIENT_HISTORY. Its invented table
         and a note are left in G:\\a_p_r_i_r\\scratch\\SMOKE_E_002_X_V1_POWERBALL.'
    A failure is any other answer, and any error at all while the method is imported or run: after a change of
    the Python environment a method that can no longer be imported fails here.
    Refuses (ChecksRefused) if the tree's scratch folder is a link or cannot be made.
    """
    scratch = Path(data_root) / SCRATCH_FOLDER
    if is_link(scratch) or (scratch.exists() and not scratch.is_dir()):
        raise ChecksRefused(f'{scratch}: the scratch folder must be an ordinary folder of this tree. Remove what '
                            f'lies there; the smoke case makes the folder again.')
    folder = smoke_folder(data_root, variant, game_id)
    if folder.exists():                              # a smoke case that failed before: its folder is its own
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    target = first_target(game_id, variant.minimum_earlier_draws(game_id))
    results = invented_results(game_id, target)
    # The table the engine reads is the bytes in memory. The copy kept beside a failure's note is a file of the
    # tree's scratch folder, and the file-form standard gives a scratch CSV file CRLF line endings.
    (folder / SMOKE_TABLE_NAME).write_bytes(results.raw.replace(b'\n', LINE_ENDING.encode('ascii')))
    profile = get_profile(game_id)
    try:
        content, detail = compute_target(variant, software.method_of(variant), results, target)
        if content['status'] == FORECAST and set(content['barrels']) == {b.barrel_id for b in profile.barrels}:
            found = None
        elif content['status'] == FORECAST:
            found = f'a forecast for the barrels {sorted(content["barrels"])}, not for every barrel of the game'
        else:
            found = f'{content["status"]}, {content.get("reason")}' + (f' ({detail})' if detail else '')
    except Exception as fault:                       # whatever stops a method here would stop it in a job
        found = f'{type(fault).__name__}: {fault}'
        detail = traceback.format_exc()
    if found is None:
        shutil.rmtree(folder)
        return None
    note = (f'The smoke case of {variant.identity} for {game_id} failed.\n'
            f'Target: draw {target}, on the invented table beside this note (draws {results.first_draw} to '
            f'{results.last_draw}; seed {SMOKE_SEED}; no real draw).\n'
            f'Found: {found}\n' + (f'\n{detail}\n' if detail else ''))
    with open(folder / SMOKE_NOTE_NAME, 'w', encoding='utf-8', newline=LINE_ENDING) as stream:
        stream.write(note)
    return (f'{variant.identity} for {game_id}: the smoke case failed: {found}. Its invented table and a note are '
            f'left in {folder}.')


def smoke_cases(software: Software, data_root: Path, only=None, say=print) -> list:
    """The smoke case of every variant of the software, for each game it supports.

    only: None for every variant, or the identities to try (an install tries its new variants).
    say: prints one line a smoke case.  Returns the failures' lines; empty if every one passed.
    """
    failures = []
    for variant in software.variants:
        if only is not None and variant.identity not in only:
            continue
        for game_id in GAMES:
            if not variant.supports(game_id):
                continue
            failure = smoke_case(software, data_root, variant, game_id)
            say(f'  smoke case: {variant.identity} for {game_id}: '
                + ('a complete forecast' if failure is None else 'FAILED'))
            if failure is not None:
                failures.append(failure)
    return failures


# ------------------------------------------------------------------------- the stored results, read once

def read_statuses(software: Software) -> tuple:
    """Read every variant's status file where the software lies. Nothing is created: a missing file is a
    refusal like any other. Returns (statuses, refusals) as research_job.read_statuses does."""
    statuses, refusals = {}, {}
    for variant in software.variants:
        games = [game_id for game_id in GAMES if variant.supports(game_id)]
        try:
            statuses[variant.identity] = read_status(variant.folder / STATUS_FILE_NAME, games)
        except StatusRefused as refusal:
            refusals[variant.identity] = str(refusal)
    return statuses, refusals


def read_stored(software: Software, settings: TreeSettings, say=print) -> dict:
    """Read each game's stored records as the research job reads them, changing nothing.

    software: the software being asked.  settings: the settings of the tree whose data is read.
    Returns {game: GameRecords}. Refuses with what the job's own reading refuses (a list that breaks its
    invariants, results that fail their check, a status file that fails its check): the caller reports it.
    """
    stored, unreadable = read_stored_game_by_game(software, settings, say, pass_on=True)
    assert not unreadable
    return stored


def _job_that_only_reads(software: Software, settings: TreeSettings, say, now=None) -> Job:
    """The record the engine's own reading functions ask for, made for software that is being asked and not
    run as a job: no results step, no scope, and an empty environment digest (no line is written with it)."""
    statuses, refusals = read_statuses(software)
    return Job(settings=settings, variants=software.variants, statuses=statuses, status_refusals=refusals,
               forecasting_code_identity=software.forecasting_code_identity,
               derived_code_digest=software.derived_code_digest, environment_digest='', only=None, no_update=True,
               now=now, say=say)


def read_stored_game_by_game(software: Software, settings: TreeSettings, say=print, pass_on: bool = False) -> tuple:
    """As read_stored, but a game whose records the job itself would refuse does not stop the other game.

    pass_on: True to let such a refusal through unchanged (read_stored).
    Returns (stored, unreadable): {game: GameRecords} and {game: the refusal's own words}, for example
        ({'OZLOTTO': <GameRecords>}, {'POWERBALL': 'results/research/POWERBALL/...: line 7 is not ...'})
    A game's records count as read only if the job would work them: after reading, the job's own check that the
    results on file only grew since the lists were written is made (research_job.check_results_only_grew), so
    that these checks never call a game well whose results the job refuses.
    Only the refusals the job understands (research_job.GAME_REFUSALS) are caught; any other error is a fault
    and is passed on.
    """
    job = _job_that_only_reads(software, settings, say)
    stored, unreadable = {}, {}
    for game_id in GAMES:
        if not any(variant.supports(game_id) for variant in software.variants):
            continue
        try:
            records = read_game(job, game_id)
            check_results_only_grew(records)
            stored[game_id] = records
        except GAME_REFUSALS as refusal:
            if pass_on:
                raise
            unreadable[game_id] = str(refusal)
            say(f'  {game_id}: its stored records could not be read, so nothing of it was compared: {refusal}')
    return stored, unreadable


# ------------------------------------------------------------------------------------ the forecast sample

def sample_targets(state) -> list:
    """The stored forecasts of one variant in one game that are computed again: of its lines that hold a
    FORECAST, the first, the middle and the last, for example [1248, 1420, 1591]. Fewer if it has fewer."""
    forecasts = sorted(target for target, facts in state.targets.items() if facts.status == FORECAST)
    if len(forecasts) <= SAMPLE_SIZE:
        return forecasts
    return [forecasts[0], forecasts[len(forecasts) // 2], forecasts[-1]]


def forecast_sample(software: Software, stored: dict, say=print) -> tuple:
    """Compute the fixed sample of stored forecasts again and compare each by its content's digest.

    stored: read_stored's result.  Returns (how many were compared, the differences' lines), for example
        (12, ['E_002/X_V1 for POWERBALL, draw 1420: the stored forecast is not what this software computes here'])
    A held variant has no list of its own here and is left out. An error while a forecast is computed is a
    difference, and its line says what the error was. It is a sample: it can show a fault, never that there is
    none.
    """
    compared, differences = 0, []
    for game_id, records in stored.items():
        for state in records.workable:
            for target in sample_targets(state):
                compared += 1
                where = f'{state.variant.identity} for {game_id}, draw {target}'
                try:
                    content, _ = compute_target(state.variant, software.method_of(state.variant), records.results,
                                                target)
                    same = content_digest(content) == state.targets[target].content_digest
                    why = 'the stored forecast is not what this software computes here'
                except Exception as fault:
                    same, why = False, f'it could not be computed again ({type(fault).__name__}: {fault})'
                if not same:
                    differences.append(f'{where}: {why}')
    say(f'  forecast sample: {compared} stored forecast(s) computed again; {len(differences)} differ')
    return compared, differences


# ---------------------------------------------------------------------------------- the derived results

def derived_results(stored: dict, say=print) -> dict:
    """Recompute every score and the whole prevailing ledger of each game and compare them with what is stored.

    stored: read_stored's result.
    Returns {game: None, or (X, detail, known)}: the lowest draw at which a stored score or prevailing line is
    not what the software computes, the one line saying what, and whether the tree already says so. `known` is
    True when the game's own marker NOT_CURRENT_FROM.json already names a mismatch at X or an earlier draw: then
    the difference is the one the owner has been told of and owes a rerun for, not a new one. Where the marker
    says a catch-up is awaited from a draw, only the draws before it are compared, as the job does.
    Nothing is written: this check never makes or changes the marker.
    """
    answers = {}
    for game_id, records in stored.items():
        cutoff = records.cutoff
        awaiting = cutoff is not None and cutoff[1] == derived_check.AWAITING_CATCH_UP
        found = derived_check.first_mismatch(records, cutoff[0] if awaiting else None)
        if found is None:
            answers[game_id] = None
            say(f'  derived results: {game_id}: every stored score and prevailing line compared is what this '
                f'software computes' + (f' (before draw {cutoff[0]}; a catch-up is awaited from there)'
                                        if awaiting else ''))
            continue
        known = cutoff is not None and cutoff[1] == derived_check.MISMATCH and cutoff[0] <= found[0]
        answers[game_id] = (found[0], found[1], known)
        say(f'  derived results: {game_id}: NOT what this software computes, from draw {found[0]}: {found[1]}'
            + (f' (the tree already marks them not current from draw {cutoff[0]})' if known else ''))
    return answers


# ------------------------------------------------- the checks, asked by an install tool with the tree's Python

def run_checks(software_root: Path, settings: TreeSettings, smoke=None, sample: bool = False, derived: bool = False,
               say=print, write_marker: bool = False) -> dict:
    """Make the checks an install tool asks for and return what was found, as plain values.

    software_root: the folder the software lies in (the tree, or the software as it would be).
    settings: the settings of the tree whose data is read and whose scratch folder is used.
    smoke: None for no smoke case; ALL_VARIANTS for every variant's; or the identities to try, for example
    ['E_002/RECUR_MEAN_ALL_V1'].  sample, derived: whether the forecast sample and the derived results are asked.
    write_marker: True only for a tree's creation, with ALL_VARIANTS: if every smoke case passed, the marker of
    the tree's environment is written by this Python, the tree's own (the marker lists what THIS Python has
    installed); if one failed, no marker is written and an older one is removed.
    Returns, for example,
        {'kind': 'TREE_CHECKS_V1', 'software_root': 'C:/Temp/as_it_would_be', 'data_root': 'G:/a_p_r_i_r',
         'smoke': {'asked': 'ALL', 'failures': []}, 'marker': None,
         'unreadable': {},
         'sample': {'compared': 12, 'differences': []},
         'derived': {'POWERBALL': None, 'OZLOTTO': {'from_draw': 1702, 'detail': '...', 'known': False}}}
    A check that was not asked is None; 'marker' is the digest written, or None. It only finds and tells: what
    stops an install is the tool's to decide.
    Refuses (ChecksRefused): the software cannot be read (read_software); an identity named for a smoke case
    that the software does not hold; the marker asked without every variant's smoke case, or of software that
    does not lie in the tree itself.
    """
    if write_marker and (smoke != ALL_VARIANTS or Path(software_root).resolve() != settings.tree_root.resolve()):
        raise ChecksRefused('the environment\'s marker is written only after every variant\'s smoke case, made by the '
                            'software that lies in the tree itself.')
    software = read_software(software_root)
    found = {'kind': RESULT_KIND, 'software_root': str(software_root), 'data_root': str(settings.tree_root),
             'smoke': None, 'marker': None, 'unreadable': None, 'sample': None, 'derived': None}
    if smoke is not None:
        only = None if smoke == ALL_VARIANTS else list(smoke)
        unknown = sorted(set(only or ()) - {variant.identity for variant in software.variants})
        if unknown:
            raise ChecksRefused(f'a smoke case was asked for {", ".join(unknown)}, which the software in '
                                f'{software_root} does not hold.')
        found['smoke'] = {'asked': smoke if only is None else only,
                          'failures': smoke_cases(software, settings.tree_root, only=only, say=say)}
    if write_marker:
        if found['smoke']['failures']:
            (settings.venv_dir / environment_marker.MARKER_NAME).unlink(missing_ok=True)
        else:
            found['marker'] = environment_marker.write_marker(settings.venv_dir)
            say(f'  the environment\'s marker is written: {settings.venv_dir / environment_marker.MARKER_NAME}')
    if sample or derived:
        stored, found['unreadable'] = read_stored_game_by_game(software, settings, say)
        if sample:
            compared, differences = forecast_sample(software, stored, say)
            found['sample'] = {'compared': compared, 'differences': differences}
        if derived:
            found['derived'] = {game_id: answer and {'from_draw': answer[0], 'detail': answer[1], 'known': answer[2]}
                                for game_id, answer in derived_results(stored, say).items()}
    return found


def main(arguments, software_root: Path, say=print) -> int:
    """The `checks` command of src/tree_checks_command.py. No launcher starts it: an install tool in DEV does,
    with the target tree's own Python, while it holds the target's job lock.

    arguments: for example ['--data', 'G:/a_p_r_i_r', '--result', 'C:/Temp/x/result.json', '--smoke', 'ALL',
    '--sample', '--derived'].  software_root: the folder this program's own src/ lies in.
    Writes the result of run_checks as one line of JSON to the file named, which must not exist yet.
    Returns EXIT_RAN when the result was written, whatever was found; EXIT_REFUSED, with one line saying why and
    no result file, when the settings, the software or the arguments are refused.
    """
    parser = argparse.ArgumentParser(prog='tree_checks_command.py checks',
                                     description='The checks of an install, made with the target tree\'s Python '
                                                 '(specification 12.3 items 2, 4 and 5).')
    parser.add_argument('--data', required=True, help='the tree whose data is read and whose scratch folder is used')
    parser.add_argument('--result', required=True, help='the file the result is written to; it must not exist')
    parser.add_argument('--smoke', default=NO_VARIANT,
                        help=f'{ALL_VARIANTS}, {NO_VARIANT}, or identities separated by commas, for example '
                             f'E_002/RECUR_MEAN_ALL_V1,E_002/RECUR_MEDIAN_ALL_V1')
    parser.add_argument('--sample', action='store_true', help='compute the fixed sample of stored forecasts again')
    parser.add_argument('--derived', action='store_true', help='compare every stored score and prevailing line')
    parser.add_argument('--write-marker', action='store_true',
                        help='with --smoke ALL, at a tree\'s creation: write the environment\'s marker if every '
                             'smoke case passed')
    chosen = parser.parse_args(arguments)
    smoke = {NO_VARIANT: None, ALL_VARIANTS: ALL_VARIANTS}.get(chosen.smoke, chosen.smoke.split(','))
    try:
        settings = read_settings(Path(chosen.data))
        found = run_checks(Path(software_root), settings, smoke, chosen.sample, chosen.derived, say,
                           chosen.write_marker)
        with open(chosen.result, 'x', encoding='ascii', newline='\n') as stream:
            stream.write(json.dumps(found, ensure_ascii=True, sort_keys=True) + '\n')
    except (SettingsRefused, ChecksRefused, ManifestRefused, FileExistsError, LaunchRefused) as refusal:
        say(f'REFUSED: {refusal}')
        return EXIT_REFUSED
    return EXIT_RAN


# ---------------------------------------------- the print-outs made again, after an infrastructure reinstall

def make_reports_again(software: Software, settings: TreeSettings, now=None, say=print) -> dict:
    """Make every league report, next-draw report and OV-1 print-out of each game again from the stored lists,
    with this software, exactly as the research job's End step makes them (specification 12.4: "the print-outs
    are made again when their code changes").

    software: the tree's own software.  settings: the tree's settings.  now: gives the present time (UTC).
    The reports are print-outs, a function of the lists, the results and the status files: no list, score or
    prevailing line is read for writing, and none is written. A file whose bytes would not change is not
    written. Where a game's results are marked not current from a draw, nothing is made for that draw or a
    later one, by the job's own rule. A game whose stored records the job itself would refuse is said and left.
    Returns {game: how many report files were written}.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    job = _job_that_only_reads(software, settings, say, now)
    written = {}
    for game_id in GAMES:
        if not any(variant.supports(game_id) for variant in software.variants):
            continue
        try:
            records = read_game(job, game_id)
            check_results_only_grew(records)
        except GAME_REFUSALS as refusal:
            say(f'  {game_id}: its stored records could not be read, so its reports were not made again: {refusal}')
            continue
        job.counts[game_id] = collections.Counter()
        finish_reports(job, records, ReportWriter(records.tree_root, game_id, job.local_time()))
        written[game_id] = job.counts[game_id]['report files']
        say(f'  reports: {game_id}: made again with this software; {written[game_id]} file(s) differed and were '
            f'written')
    return written


def reports_main(arguments, software_root: Path, say=print) -> int:
    """The `reports` command of src/tree_checks_command.py. No launcher starts it: an infrastructure reinstall
    does, with the target tree's own Python, while it holds the target's job lock.

    arguments: ['--data', 'G:/a_p_r_i_r'].  software_root: the folder this program's own src/ lies in, which
    must be that tree: a tree's reports are made by its own installed software.
    Returns EXIT_RAN when the reports were made; EXIT_REFUSED with one line saying why.
    """
    parser = argparse.ArgumentParser(prog='tree_checks_command.py reports',
                                     description='Make a tree\'s print-outs again with its installed software '
                                                 '(specification 12.4).')
    parser.add_argument('--data', required=True, help='the tree whose reports are made again')
    chosen = parser.parse_args(arguments)
    try:
        settings = read_settings(Path(chosen.data))
        if Path(software_root).resolve() != settings.tree_root.resolve():
            raise ChecksRefused('a tree\'s reports are made by the software that lies in the tree itself.')
        make_reports_again(read_software(software_root), settings, say=say)
    except (SettingsRefused, ChecksRefused, ManifestRefused, LaunchRefused) as refusal:
        say(f'REFUSED: {refusal}')
        return EXIT_REFUSED
    return EXIT_RAN
