"""The full check of a game's derived results, and the file that marks them not current.

What this file is for
    A game's score lines and its prevailing OV-1 ledger are stored results. They must be what the installed code
    computes today from the stored forecasts, the results on file and the status files. At its start the job
    recomputes every one of them in memory and compares the scientific content. If the content differs from some
    draw X on, the game's derived results are not current from X: this file writes the one small marker
    NOT_CURRENT_FROM.json, and every part of the job that writes a score, a prevailing line or a report honours
    it. Nothing is recomputed on disk and no stored line is altered here.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 5.8 (and 5.6A: a held variant makes the
    derived results not current from its first draw).

Which of the project's own modules it uses
    research.game_state    GameRecords, MAIN_BARREL: the game's records in memory
    research.scoring       score_content, read_outcome
    research.ov1_ledger    draw_line, prevailing_start, prevailing_cohort, running_logs_of, Blocked
    research.variant_lists RESEARCH_FOLDER
    research.windows_text  LINE_ENDING: the marker is written in the standard's form, each line ending CRLF

What uses it
    research/research_job.py, and the engine's tests.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from research import ov1_ledger
from research.game_state import MAIN_BARREL, GameRecords
from research.scoring import read_outcome, score_content
from research.variant_lists import RESEARCH_FOLDER
from research.windows_text import LINE_ENDING

# The marker file of a game, under the tree's research folder, and its two reasons (specification 5.8).
CUTOFF_NAME = 'NOT_CURRENT_FROM.json'
MISMATCH = 'MISMATCH'
AWAITING_CATCH_UP = 'AWAITING_CATCH_UP'
REASONS = (MISMATCH, AWAITING_CATCH_UP)


class CutoffRefused(ValueError):
    """The marker file cannot be read as a draw and one of the two reasons. The game refuses and names it."""


def cutoff_path(tree_root: Path, game_id: str) -> Path:
    """The marker file of a game, for example <tree>/results/research/POWERBALL/NOT_CURRENT_FROM.json."""
    return Path(tree_root) / RESEARCH_FOLDER / game_id / CUTOFF_NAME


def read_cutoff(tree_root: Path, game_id: str) -> tuple | None:
    """Read a game's marker.

    Returns None if there is none; otherwise (draw, reason, detail), for example
    (1590, 'MISMATCH', 'the score of E_002/X_V1 for draw 1590 is not what the installed code computes').
    Refuses (CutoffRefused) a file that is not such a record.
    """
    path = cutoff_path(tree_root, game_id)
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding='ascii'))
        draw, reason = record['not_current_from_draw'], record['reason']
        if type(draw) is not int or reason not in REASONS:
            raise ValueError('not a draw number with one of the two reasons')
    except (ValueError, KeyError, TypeError, UnicodeDecodeError) as error:
        raise CutoffRefused(f'{path}: the marker cannot be read ({error}). Restore it from a backup; do not '
                            f'delete it, or stale results would look current.') from None
    return draw, reason, str(record.get('detail', ''))


def write_cutoff(tree_root: Path, game_id: str, draw: int, reason: str, detail: str) -> None:
    """Write a game's marker, each line ending CRLF: the whole file to a temporary name, then one rename.

    draw: the first draw whose derived results are not current.  reason: MISMATCH or AWAITING_CATCH_UP.
    detail: one line for the reader saying what was found.
    """
    path = cutoff_path(tree_root, game_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps({'not_current_from_draw': draw, 'reason': reason, 'detail': detail}, indent=1,
                      ensure_ascii=True) + '\n'
    temporary = path.with_name(path.name + '.writing')
    with open(temporary, 'w', encoding='ascii', newline=LINE_ENDING) as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def remove_cutoff(tree_root: Path, game_id: str) -> None:
    """Remove a game's marker (only after a catch-up whose full check found nothing)."""
    cutoff_path(tree_root, game_id).unlink()


def outcome_of(records: GameRecords, draw: int) -> dict:
    """The result of a draw on file, read once and kept (see scoring.read_outcome)."""
    if draw not in records.outcomes:
        records.outcomes[draw] = read_outcome(records.results, draw)
    return records.outcomes[draw]


def first_mismatch(records: GameRecords, below: int | None = None) -> tuple | None:
    """Recompute every score and the whole prevailing ledger of a game and find the first draw that differs.

    records: the game's records in memory.  below: if given, only draws before it are compared (the catch-up
    after a rerun the owner stopped); a held variant counts whatever `below` is.
    Returns None if every stored content equals its recomputation; otherwise (X, detail): the lowest draw at
    which something differs and one line saying what, for example
        (1590, 'the score of E_002/X_V1 for draw 1590 is not what the installed code computes').
    Compared, and nothing else: each score line's content (target, the forecast content's digest, the numbers
    drawn, the matches, the divisions); each prevailing line's content (draw, cohort, weights, V, X, Z, the six
    log-factors and running sums, the score and the crossing). The envelopes are not compared.
    """
    found = None

    def note(draw: int, detail: str) -> None:
        """Keep the lowest draw found so far."""
        nonlocal found
        if found is None or draw < found[0]:
            found = (draw, detail)

    for state in records.states:
        identity = state.variant.identity
        if state.held:
            note(state.first_target, f'{identity} is held: its list is foreign ({state.foreign_reason}), and the '
                                     f'stored reports and OV-1 records were built with it')
            continue
        for target in sorted(state.score_contents):
            if (below is not None and target >= below) or (found is not None and target >= found[0]):
                break
            rebuilt = score_content(state.forecast_content(records.game_id, target),
                                    state.targets[target].content_digest, outcome_of(records, target))
            if rebuilt != state.score_contents[target]:
                note(target, f'the score of {identity} for draw {target} is not what the installed code computes '
                             f'from the stored forecast and the results on file')
    start = ov1_ledger.prevailing_start(records.states)
    running = ov1_ledger.running_logs_of(None)
    for index, stored in enumerate(records.ledger_contents):
        draw = stored['draw']
        if (below is not None and draw >= below) or (found is not None and draw >= found[0]):
            break
        if start is None or draw != start + index:
            note(draw, f'the prevailing ledger has a line for draw {draw}, but the status files '
                       + ('give no variant an eligibility draw' if start is None
                          else f'start the prevailing score at draw {start}'))
            break
        try:
            rebuilt = ov1_ledger.draw_line(records.game_id, draw, ov1_ledger.prevailing_cohort(records.states, draw),
                                           outcome_of(records, draw)[MAIN_BARREL], running)['content']
        except ov1_ledger.Blocked as blocked:
            note(draw, f'the prevailing line for draw {draw} cannot be rebuilt: {blocked}')
            break
        if rebuilt != stored:
            note(draw, f'the prevailing line for draw {draw} is not what the installed code computes from the '
                       f'lists, the results and the status files')
            break
        running = ov1_ledger.running_logs_of(rebuilt)
    return found


def settle(records: GameRecords, found: tuple | None) -> bool:
    """Bring the marker into line with what a check found, and set records.cutoff.

    records: the game's records (records.cutoff holds the marker as read, or None).
    found: first_mismatch's result.
    Returns True if the marker was written or changed. A mismatch writes MISMATCH at the lowest draw known (never
    a later draw than a marker already names). With nothing found the marker is left as it is: a MISMATCH is
    removed only by the owner's derived-only rerun, and an AWAITING_CATCH_UP only by finish_catch_up.
    """
    if found is None:
        return False
    draw, detail = found
    current = records.cutoff
    if current is not None and current[1] == MISMATCH and current[0] <= draw:
        return False
    write_cutoff(records.tree_root, records.game_id, draw, MISMATCH, detail)
    records.cutoff = (draw, MISMATCH, detail)
    return True


def finish_catch_up(records: GameRecords) -> str:
    """After a catch-up that has done every draw on file: the full comparison once more (specification 5.8).

    Returns one line for the owner. If the comparison finds nothing the AWAITING_CATCH_UP marker is removed; if it
    finds something the marker stays and its reason becomes MISMATCH at the draw concerned: a catch-up never
    clears a real mismatch.
    """
    found = first_mismatch(records)
    if found is None:
        remove_cutoff(records.tree_root, records.game_id)
        records.cutoff = None
        return (f'{records.game_id}: the catch-up is complete and the full check found nothing: the derived '
                f'results are current again')
    write_cutoff(records.tree_root, records.game_id, found[0], MISMATCH, found[1])
    records.cutoff = (found[0], MISMATCH, found[1])
    return (f'{records.game_id}: results not current from draw {found[0]}: the catch-up finished, but the full '
            f'check found: {found[1]}')
