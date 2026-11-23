"""The results step in QA and DEV: the checked copy of the accepted results from the tree the settings name.

What this file is for
    QA and DEV never contact the lottery site. Their accepted results are copied from another tree (PROD) and
    checked to be the same file grown longer: the results already here must be the beginning, byte for byte, of
    the results there. The source tree is only read. The copy is written beside the old files first and then
    renamed into place, so that a crash leaves either the old pair or a state this file can finish.
    In PROD the step runs the one reviewed updater through its own launcher; that arrives with build step 3,
    and until then the step is left out there.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 7.1 (the Results step; "the results step
    succeeded" is one rule in every tree; results changed other than by growing refuse).

Which of the project's own modules it uses
    _common.game_profiles  get_profile: the game's first draw
    research.job_lock    updater_lock: no results update may run while the copy is put in place
    research.reader      results_on_file, results_paths, check_results_bytes, ResultsRefused
    research.settings    TreeSettings

What uses it
    research/research_job.py, and the engine's tests.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from _common.game_profiles import get_profile
from research.job_lock import updater_lock
from research.reader import ResultsRefused, check_results_bytes, results_on_file, results_paths
from research.settings import TreeSettings

# The ending of the two files a copy writes before it renames them into place.
INCOMING_SUFFIX = '.incoming'


@dataclass(frozen=True)
class ResultsStep:
    """What a results step did.

    succeeded: True if the step ran and the results on file are now those of the source (new draws or none).
    message: one line for the owner, for example 'results copied from G:\\a_p_r_i_r: draws 1601 to 1606 are new'.
    """
    succeeded: bool
    message: str


def first_draw_that_differs(old: bytes, new: bytes, game_id: str) -> int:
    """The first draw whose row differs between two results files, for the refusal's message.

    old: the results here.  new: the results they should be the beginning of.
    Returns the draw number, for example 1590; the game's first draw if the header line itself differs.
    """
    first = get_profile(game_id).first_draw
    new_rows = new.split(b'\n')
    for index, row in enumerate(old.split(b'\n')):
        if index >= len(new_rows) or new_rows[index] != row:
            return max(first, first + index - 1)
    return first


def finish_interrupted_copy(tree_root: Path, game_id: str) -> str | None:
    """Finish or discard a copy that a crash interrupted, before the results are read.

    Returns None if nothing was pending; otherwise one line saying what was done. A copy that had not yet
    replaced the results file is discarded (the next results step copies again); one that had replaced the
    results file but not yet its ledger is completed.
    """
    master, ledger = results_paths(tree_root, game_id)
    incoming_master = master.with_name(master.name + INCOMING_SUFFIX)
    incoming_ledger = ledger.with_name(ledger.name + INCOMING_SUFFIX)
    if incoming_master.exists():
        incoming_master.unlink()
        if incoming_ledger.exists():
            incoming_ledger.unlink()
        return f'{game_id}: an interrupted copy of the results had changed nothing and was discarded'
    if incoming_ledger.exists():
        os.replace(incoming_ledger, ledger)
        return f'{game_id}: an interrupted copy of the results was completed (its ledger was put in place)'
    return None


def copy_results(settings: TreeSettings, game_id: str, when: str) -> ResultsStep:
    """Run the results step of a QA or DEV tree for one game.

    settings: the tree's settings.  game_id: the game.  when: the time, as text, for the updater's lock file.
    Returns the ResultsStep. The step is "left out" or "failed" (not succeeded, nothing changed) when the
    settings name no tree to copy from, when the tree is PROD (the updater's launch arrives with build step 3),
    or when the source's results cannot be read whole and named by their ledger.
    Refuses (ResultsRefused) results here that are not the beginning of the source's ("results changed other
    than by growing"), naming the draw; and (LaunchRefused) if a results update holds the updater's lock here.
    """
    if settings.role == 'PROD':
        return ResultsStep(False, f'{game_id}: the results step was left out: in PROD it runs the reviewed updater '
                                  f'through its own launcher, which arrives with build step 3')
    source_root = settings.results_copy_from
    if source_root is None:
        return ResultsStep(False, f'{game_id}: the results step was left out: the settings file names no tree to '
                                  f'copy results from ([results] copy_from)')
    try:
        source = results_on_file(source_root, game_id)
        source_ledger = results_paths(source_root, game_id)[1].read_bytes()
    except (ResultsRefused, OSError) as failure:
        return ResultsStep(False, f'{game_id}: the results step failed: nothing new was read ({failure}). Run the '
                                  f'job again later; --no-update works without it')
    master, ledger = results_paths(settings.tree_root, game_id)
    here, here_ledger = master.read_bytes(), ledger.read_bytes()
    if not source.raw.startswith(here):
        raise ResultsRefused(f'{game_id}: results changed other than by growing: the results here are not the '
                             f'beginning of those in {source_root} (first difference at draw '
                             f'{first_draw_that_differs(here, source.raw, game_id)}). What to recompute is a '
                             f'reviewed decision; nothing was copied.')
    if source.raw == here and source_ledger == here_ledger:
        return ResultsStep(True, f'{game_id}: results checked against {source_root}: nothing new (through draw '
                                 f'{source.last_draw})')
    last_here = check_results_bytes(here, game_id, str(master))
    incoming_master = master.with_name(master.name + INCOMING_SUFFIX)
    incoming_ledger = ledger.with_name(ledger.name + INCOMING_SUFFIX)
    with updater_lock(settings.tree_root, 'checked copy of the results', when):
        # The ledger's copy is written first and the results file is renamed first, so that a crash leaves a
        # state finish_interrupted_copy can tell: both waiting (nothing changed) or only the ledger waiting.
        for path, data in ((incoming_ledger, source_ledger), (incoming_master, source.raw)):
            with open(path, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        os.replace(incoming_master, master)
        os.replace(incoming_ledger, ledger)
    if source.last_draw == last_here:
        return ResultsStep(True, f'{game_id}: results copied from {source_root}: no new draw (the ledger grew)')
    return ResultsStep(True, f'{game_id}: results copied from {source_root}: draws {last_here + 1} to '
                             f'{source.last_draw} are new')
