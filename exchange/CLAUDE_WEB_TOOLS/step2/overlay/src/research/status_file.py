"""A variant's operating status in this tree: the small file VARIANT_STATUS.ini beside its software.

What this file is for
    Each variant folder holds one readable file that says, for each game the variant supports, two facts, each
    set at most once: whether the variant is withdrawn (from which draw and why), and the first draw at which it
    counts in the prevailing OV-1. The research engine reads this file, in every tree, to decide whether a
    variant is forecast and scored at a draw and whether it is in the prevailing cohort. This file reads it,
    checks it, and writes it: the whole file under a temporary name, then one rename. The temporary file is made
    in the tree's control folder, never in the variant folder, so that a write that was interrupted can never
    leave an undeclared file among a variant's software (EX_283 F283-B01). The last lines hold the SHA-256 of
    every byte above them: a check against accidents and hand edits, not a signature.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 3.5, with 10.2 (the eligibility draw is set
    once) and 11 (withdrawal is one-way).

Which of the project's own modules it uses
    None.

What uses it
    research/research_job.py (reads; creates a missing file in DEV; writes the eligibility draw),
    research/withdraw.py (writes a withdrawal), research/ov1_ledger.py and research/reports.py (read), and the
    engine's tests.
"""
from __future__ import annotations

import configparser
import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

# Where a status file is written before it is renamed into place: a folder of the tree's control folder, on the
# same volume as the variant folders, so that the rename is one step. From the tree root.
STAGING_FOLDER = 'records/status_staging'
# The ending of a file in the staging folder.
STAGING_SUFFIX = '.writing'
# Where the variant folders lie in a tree, as the last parts of a status file's path before family and variant.
METHODS_PARTS = ('src', 'methods')
# The file's name, in every variant folder of every tree.
STATUS_FILE_NAME = 'VARIANT_STATUS.ini'
# The section whose one key holds the SHA-256 of every byte above the section's own line.
CHECK_SECTION = 'check'
CHECK_LINE = b'[check]\n'
# The two values of "status".
ACTIVE = 'ACTIVE'
WITHDRAWN = 'WITHDRAWN'


class StatusRefused(ValueError):
    """A status file is missing, damaged or edited by hand, or a fact would be set a second time. The message
    names the file, says what was found and what to do."""


@dataclass(frozen=True)
class GameStatus:
    """A variant's status in one game.

    withdrawn_from: the draw the withdrawal takes effect from, or None while the variant is active.
    withdrawn_reason, withdrawn_recorded: the owner's reason and a note of when it was recorded (for the reader).
    eligible_from: prevailing_ov1_first_eligible_draw, or None if not yet set.  eligibility_recorded: its note.
    """
    withdrawn_from: int | None = None
    withdrawn_reason: str | None = None
    withdrawn_recorded: str | None = None
    eligible_from: int | None = None
    eligibility_recorded: str | None = None

    def is_withdrawn_at(self, draw: int) -> bool:
        """True if the variant is withdrawn from a draw at or below `draw`: it is then neither forecast nor
        scored at `draw`. For example withdrawn from 1601: is_withdrawn_at(1601) is True, (1600) False."""
        return self.withdrawn_from is not None and draw >= self.withdrawn_from

    def in_prevailing_cohort_at(self, draw: int) -> bool:
        """True if the variant counts in the prevailing OV-1 at `draw`: eligible at or below it and not
        withdrawn from a draw at or below it (specification 10.4)."""
        return self.eligible_from is not None and self.eligible_from <= draw and not self.is_withdrawn_at(draw)


def _one_line(text: str, what: str) -> str:
    """Refuse text that would not be one plain line in the file; return it trimmed."""
    text = text.strip()
    if not text or not text.isascii() or not text.isprintable():
        raise StatusRefused(f'{what} must be one line of plain printable text; found {text!r}.')
    return text


def render(family: str, variant: str, statuses: dict) -> bytes:
    """The bytes of a status file.

    family, variant: the variant's identity, for the comment lines.  statuses: {game: GameStatus}, in the order
    the sections are to appear.
    Returns the whole file, ending with the [check] section, for example beginning
        b'; E_002 / RECUR_MEAN_ALL_V1 - operating status in THIS tree.\\n; Written only by ...'.
    """
    lines = [f'; {family} / {variant} - operating status in THIS tree.',
             '; Written only by the project\'s commands. Do not edit by hand: a hand edit is detected and the game '
             'refuses.']
    for game_id, status in statuses.items():
        lines.append(f'[{game_id}]')
        lines.append(f'status = {WITHDRAWN if status.withdrawn_from is not None else ACTIVE}')
        if status.withdrawn_from is not None:
            lines += [f'withdrawn_from_draw = {status.withdrawn_from}',
                      f'withdrawn_reason = {status.withdrawn_reason}',
                      f'withdrawn_recorded = {status.withdrawn_recorded}']
        if status.eligible_from is not None:
            lines += [f'prevailing_ov1_first_eligible_draw = {status.eligible_from}',
                      f'prevailing_ov1_eligibility_recorded = {status.eligibility_recorded}']
    body = ('\n'.join(lines) + '\n').encode('ascii')
    return body + CHECK_LINE + f'sha256 = {hashlib.sha256(body).hexdigest()}\n'.encode('ascii')


def read_status(path: Path, games) -> dict:
    """Read a status file and check it.

    path: the file.  games: the games the variant supports; the file must hold exactly a section for each.
    Returns {game: GameStatus}, for example {'POWERBALL': GameStatus(withdrawn_from=1601, withdrawn_reason='the
    gap table was built from the wrong column', ..., eligible_from=1596, ...), 'OZLOTTO': GameStatus(...)}.
    Refuses (StatusRefused): a missing file; a file without its [check] section or whose check does not match
    the bytes above it (a hand edit); a file Python's INI reader rejects; sections other than the variant's
    games; a status that is not ACTIVE or WITHDRAWN; a withdrawal or an eligibility draw that is not complete.
    The way out is to take the file from the newest backup.
    """
    def refuse(found: str) -> StatusRefused:
        """The refusal for this file, with the one remedy."""
        return StatusRefused(f'{path}: {found} Take this file from your newest backup ZIP (or restore; in QA, '
                             f'replace the software from PROD).')

    if not path.is_file():
        raise refuse('the status file is missing.')
    raw = path.read_bytes()
    body, mark, tail = raw.rpartition(CHECK_LINE)
    if not mark or (body and not body.endswith(b'\n')):
        raise refuse('it has no [check] section.')
    parser = configparser.ConfigParser(interpolation=None, delimiters=('=',), strict=True, comment_prefixes=(';',))
    parser.optionxform = str
    try:
        parser.read_string(raw.decode('ascii'), source=str(path))
        recorded = parser.get(CHECK_SECTION, 'sha256').strip()
    except (configparser.Error, UnicodeDecodeError) as error:
        raise refuse(f'it is not a readable status file ({error}).') from None
    if recorded != hashlib.sha256(body).hexdigest() or tail != f'sha256 = {recorded}\n'.encode('ascii'):
        raise refuse('its check does not match its contents: it was edited by hand or damaged.')
    if set(parser.sections()) - {CHECK_SECTION} != set(games):
        raise refuse(f'its sections {sorted(set(parser.sections()) - {CHECK_SECTION})} are not the variant\'s '
                     f'games {sorted(games)}.')
    statuses = {}
    for game_id in games:
        section = parser[game_id]
        try:
            if section.get('status') == WITHDRAWN:
                withdrawn = (int(section['withdrawn_from_draw']), section['withdrawn_reason'],
                             section['withdrawn_recorded'])
            elif section.get('status') == ACTIVE and 'withdrawn_from_draw' not in section:
                withdrawn = (None, None, None)
            else:
                raise ValueError('status must be ACTIVE, or WITHDRAWN with its draw, reason and note')
            eligible = (int(section['prevailing_ov1_first_eligible_draw']),
                        section['prevailing_ov1_eligibility_recorded']) \
                if 'prevailing_ov1_first_eligible_draw' in section else (None, None)
        except (KeyError, ValueError) as error:
            raise refuse(f'section [{game_id}] is not complete ({error}).') from None
        statuses[game_id] = GameStatus(*withdrawn, *eligible)
    return statuses


def staging_folder_for(path: Path) -> Path:
    """The staging folder of the tree a status file lies in.

    path: a status file, <tree>/src/methods/<family>/<variant>/VARIANT_STATUS.ini.
    Returns <tree>/records/status_staging. Refuses (StatusRefused) a path that is not a status file in a variant
    folder of a tree: the writer must never guess where a tree's control folder is.
    """
    path = Path(path)
    if path.name != STATUS_FILE_NAME or len(path.parts) < 6 or path.parts[-5:-3] != METHODS_PARTS:
        raise StatusRefused(f'{path}: a status file is written only as <tree>/src/methods/<family>/<variant>/'
                            f'{STATUS_FILE_NAME}.')
    return path.parents[4] / STAGING_FOLDER


def _rename_into_place(temporary: Path, path: Path) -> None:
    """The one rename that puts a written status file in place (its own function so that a test can plant a
    failure exactly here)."""
    os.replace(temporary, path)


def write_status(path: Path, family: str, variant: str, statuses: dict) -> None:
    """Write a status file: the whole file under a temporary name in the tree's staging folder, then one rename.

    path: the status file, in its variant folder.  family, variant: its variant.  statuses: {game: GameStatus}.
    A crash or a failure before the rename leaves the old file (or none) exactly as it was, and nothing new in
    the variant folder; after it, the new file: never a mixture. What an interrupted write leaves in the staging
    folder is removed by discard_unfinished_writes at the next job or withdrawal.
    """
    staging = staging_folder_for(path)
    staging.mkdir(parents=True, exist_ok=True)
    temporary = staging / f'{family}__{variant}__{STATUS_FILE_NAME}{STAGING_SUFFIX}'
    with open(temporary, 'wb') as stream:
        stream.write(render(family, variant, statuses))
        stream.flush()
        os.fsync(stream.fileno())
    _rename_into_place(temporary, path)


def discard_unfinished_writes(tree_root: Path) -> list:
    """Remove what an interrupted status write left in a tree's staging folder.

    tree_root: the tree.  Call it only while holding the tree's job lock, so that no write is in progress.
    Returns the names removed, for example ['E_901__TOY_A_V1__VARIANT_STATUS.ini.writing']; [] if there was
    nothing. A staged file was never a status: the status file it was meant for is still the old one, whole,
    and whatever was being recorded is simply recorded again by the command that runs next.
    """
    staging = Path(tree_root) / STAGING_FOLDER
    removed = []
    if staging.is_dir():
        for leftover in sorted(staging.iterdir()):
            if leftover.is_file():
                leftover.unlink()
                removed.append(leftover.name)
    return removed


def create_active(path: Path, family: str, variant: str, games) -> dict:
    """Create a variant's status file as ACTIVE in every game, with nothing else set.

    Returns the new {game: GameStatus}. Refuses (StatusRefused) if the file already exists: creating never
    replaces a status.
    """
    if path.exists():
        raise StatusRefused(f'{path}: the status file already exists; it is never created twice.')
    statuses = {game_id: GameStatus() for game_id in games}
    write_status(path, family, variant, statuses)
    return statuses


def with_withdrawal(status: GameStatus, from_draw: int, reason: str, recorded: str) -> GameStatus:
    """A game's status with a withdrawal added.

    from_draw: the draw it takes effect from.  reason: the owner's reason.  recorded: the note for the reader,
    for example '2027-01-05 19:42; results on file through 1600'.
    Returns the new GameStatus. Refuses (StatusRefused) if the variant is already withdrawn in that game:
    a withdrawal is set once and is one-way.
    """
    if status.withdrawn_from is not None:
        raise StatusRefused(f'already withdrawn from draw {status.withdrawn_from}: a withdrawal is set once and '
                            f'no command changes or removes it.')
    return GameStatus(withdrawn_from=from_draw, withdrawn_reason=_one_line(reason, 'The reason'),
                      withdrawn_recorded=_one_line(recorded, 'The note'), eligible_from=status.eligible_from,
                      eligibility_recorded=status.eligibility_recorded)


def with_eligibility(status: GameStatus, first_eligible_draw: int, recorded: str) -> GameStatus:
    """A game's status with its prevailing-OV-1 eligibility draw added.

    first_eligible_draw: the first draw not on file after a successful results step.  recorded: the note, for
    example '2026-12-01 20:10; results on file through 1595 after a successful results step'.
    Returns the new GameStatus. Refuses (StatusRefused) if one is already set: it is set once and never changed.
    """
    if status.eligible_from is not None:
        raise StatusRefused(f'the eligibility draw is already {status.eligible_from}: it is set once and never '
                            f'changed.')
    return GameStatus(withdrawn_from=status.withdrawn_from, withdrawn_reason=status.withdrawn_reason,
                      withdrawn_recorded=status.withdrawn_recorded, eligible_from=first_eligible_draw,
                      eligibility_recorded=_one_line(recorded, 'The note'))
