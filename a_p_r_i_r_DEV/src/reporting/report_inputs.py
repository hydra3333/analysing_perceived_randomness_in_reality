"""The reporting part's reading: a game's stored science, read without changing anything, and checked.

What this file is for
    The reporting part makes reports only from stored science that still follows from the accepted results. It
    reads a game's results, its methods' lists and small files and both OV-1 series through the engine's own
    reading code, never through the research job's opening of a game (which deletes what is out of date and
    writes small files). It then works out the game's science identity from those files as they are now and
    compares it with the one the job wrote at the end of its work. If they differ, or there is none, or a
    method's lists would have to be made again, the game is refused and nothing is made for it: the owner runs
    Run_Research.bat first. Nothing here scores, fetches or writes.

Which part of the design it carries out
    doc/Predictive_Randomness_Reporting_Design_And_Specification_Amendment_A1_v0_5.md (RAT-74) A2 (what the
    reporting part reads, what it refuses and that it never changes a scientific record); the code plan v0.2
    section 3 with the reviewer's C03 (decision log entries 426 and 428).

Which of the project's own modules it uses
    research.reader            results_on_file: the accepted results
    research.variant_folders   find_variants: the methods in the tree
    research.method_flags      status_of: a method's status, read only
    research.game_state        GameRecords, load_variant_state, lists_of_variants_not_installed
    research.variant_lists     read_list: the two OV-1 series as stored
    research.ov1_ledger        where the series are kept
    research.code_identity     the engine's fingerprint, now and as kept with the results
    research.science_identity  the identity, worked out now and as stored

What uses it
    reporting/report_job.py, and the tests.
"""
from __future__ import annotations

from pathlib import Path

from research import code_identity, method_flags, ov1_ledger, science_identity
from research import variant_lists as lists
from research.game_state import GameRecords, lists_of_variants_not_installed, load_variant_state
from research.reader import results_on_file
from research.variant_folders import find_variants

# Where a tree keeps its methods, from the tree root.
METHODS_FOLDER = 'src/methods'
# What every refusal ends with: what the owner does about it.
PUT_RIGHT = 'Run Run_Research.bat in this tree first; it brings the stored science up to date, then the reports.'


class InputsRefused(Exception):
    """A game's stored science is not what the reports may be made from. The message says why and what to do."""


def read_series(tree_root: Path, game_id: str, which: str, kind: str) -> list:
    """The lines of one stored OV-1 series, each {'line', 'content', 'audit'}; [] if the file holds none.
    Refuses (InputsRefused) a series file that cannot be read."""
    try:
        listed = lists.read_list(ov1_ledger.ledger_path(tree_root, game_id, which), kind)
    except lists.ListFault as fault:
        raise InputsRefused(f'{game_id}: the {kind.lower()} OV-1 series cannot be read ({fault}). {PUT_RIGHT}')
    return listed.lines if listed is not None else []


def load_game(tree_root: Path, game_id: str) -> tuple:
    """Read a game's stored science for the reports, and check it.

    tree_root: the tree.  game_id: 'POWERBALL' or 'OZLOTTO'.
    Returns (records, exploratory): the game's GameRecords, as the research job holds them at the end of its
    work (the second series' lines and its blocked reason included), and the lines of the exploratory series.
    Refuses (InputsRefused), having changed nothing: the accepted results cannot be read; the engine in the tree
    is not the one the stored results were made with; a method's lists would have to be made again; a series
    file cannot be read; the game has no science identity, or it no longer matches the files.
    """
    tree_root = Path(tree_root)
    try:
        results = results_on_file(tree_root, game_id)
    except Exception as fault:              # the reader's refusals name the file and what to do
        raise InputsRefused(f'{game_id}: the accepted results cannot be read ({fault}).') from None
    engine_now = code_identity.infrastructure_fingerprint(tree_root)
    if code_identity.stored_fingerprint(tree_root) != engine_now:
        raise InputsRefused(f'{game_id}: the engine in this tree is not the one its stored results were made with. '
                            f'{PUT_RIGHT}')
    records = GameRecords(game_id=game_id, tree_root=tree_root, role='', results=results, states=[], foreign=[])
    variants, _ = find_variants(tree_root / METHODS_FOLDER)
    in_tree = set()
    for variant in variants:
        if not variant.supports(game_id):
            continue
        in_tree.add(variant.identity)
        try:
            status = method_flags.status_of(variant.folder, game_id)
        except method_flags.FlagFault:
            continue                        # the job passes such a method over too, and says why
        state, stale = load_variant_state(tree_root, game_id, variant, status)
        if stale:
            raise InputsRefused(f'{game_id}: {variant.identity}: its stored results must be made again ({stale}). '
                                f'{PUT_RIGHT}')
        records.states.append(state)
    records.foreign = lists_of_variants_not_installed(tree_root, game_id, in_tree)
    stored = science_identity.read_identity(tree_root, game_id)
    if stored is None:
        raise InputsRefused(f'{game_id}: there is no record of what its stored science was made from (the last '
                            f'research job did not finish this game, or none has run since the reports moved out '
                            f'of the engine). {PUT_RIGHT}')
    unlike = science_identity.differences(stored, science_identity.identity_of(records, engine_now))
    if unlike:
        raise InputsRefused(f'{game_id}: the stored science has changed since the research job last finished this '
                            f'game ({"; ".join(unlike)}). {PUT_RIGHT}')
    records.ledger_lines = read_series(tree_root, game_id, ov1_ledger.PREVAILING_LEDGER, lists.PREVAILING_KIND)
    records.blocked = stored[science_identity.BLOCKED_KEY]
    exploratory = read_series(tree_root, game_id, ov1_ledger.EXPLORATORY_LEDGER, lists.EXPLORATORY_KIND)
    return records, exploratory
