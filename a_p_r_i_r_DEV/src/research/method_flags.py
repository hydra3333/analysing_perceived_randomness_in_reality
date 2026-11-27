"""The three small files beside a method: I_AM_INSTALLABLE, I_AM_RETIRED and IN_PLACE_SINCE.

What this file is for
    Each lies in the method's own folder, src/methods/<family>/<variant>/, where its software is, and is plain
    text: one "key = value" a line. None of them is part of any fingerprint.
      I_AM_INSTALLABLE  written by "make installable" in DEV: this version may be installed.
      I_AM_RETIRED      written by "retire": for each game, the draw from which the method makes no forecast.
                        Its results for earlier draws stay, marked retired; what it held for that draw or a
                        later one is dropped. Deleting the file brings the method back.
      IN_PLACE_SINCE    written by the research job in each tree: the method's fingerprint, and for each game
                        the last draw the tree held when this version of its code was first used there. It is
                        bookkeeping only: a report can then show how a method did on the draws since.
    This file reads and writes them, and gives the research job each method's status in a game.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 4.

Which of the project's own modules it uses
    none.

What uses it
    research/research_job.py, research/game_state.py, research/variant_folders.py (the names), the commands of
    deploy/ and the tests.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

INSTALLABLE_NAME = 'I_AM_INSTALLABLE'
RETIRED_NAME = 'I_AM_RETIRED'
IN_PLACE_NAME = 'IN_PLACE_SINCE'
# The three names: a method's folder may hold them besides its declared files, and no fingerprint includes them.
FLAG_NAMES = (INSTALLABLE_NAME, RETIRED_NAME, IN_PLACE_NAME)
# A small file is written under its name plus this ending and then put in place; a job that is stopped between
# the two leaves such a file behind, which is harmless and is passed over like the small files themselves.
STAGED_SUFFIX = '.writing'
PASSED_OVER_NAMES = FLAG_NAMES + tuple(name + STAGED_SUFFIX for name in FLAG_NAMES)
# The line ending of every file this project writes.
LINE_ENDING = '\r\n'
# How an I_AM_INSTALLABLE flag stands against the files it is for (what installable_state returns).
NOT_FLAGGED = 'not flagged'
FLAG_OUT_OF_DATE = 'its flag is older than its files'
FLAGGED = 'flagged'
# Why settle_in_place wrote a method's IN_PLACE_SINCE (what it returns).
WRITTEN_FIRST = 'it did not exist'
WRITTEN_CHANGED = 'the method\'s files changed'
WRITTEN_GAME = 'this game is worked for the first time with this version'
WRITTEN_UNREADABLE = 'it could not be read'
# The comment line a retired file begins with.
RETIRED_FIRST_LINE = ('This method is retired: it makes no forecast for these draws or later ones. Delete this '
                      'file to bring it back.')


class FlagFault(ValueError):
    """One of the small files cannot be read as "key = value" lines, or holds a value that is not what its key
    needs. The message names the file and the line. The job reports it and passes the method over."""


@dataclass(frozen=True)
class MethodStatus:
    """A method's status in one game, read from its small files.

    withdrawn_from: the draw it is retired from (it makes no forecast for that draw or a later one), or None.
    withdrawn_reason: the reason written when it was retired, or None.
    eligible_from: the first draw after its establishment draw (IN_PLACE_SINCE plus one), or None if not known:
    from this draw it counts in the second OV-1 series.
    (The names are those the reports and the OV-1 code have always used.)
    """
    withdrawn_from: int | None = None
    withdrawn_reason: str | None = None
    eligible_from: int | None = None

    def is_withdrawn_at(self, draw: int) -> bool:
        """True if the method is retired from a draw at or below `draw`: it is then neither forecast nor scored
        at `draw`. For example retired from 1601: is_withdrawn_at(1601) is True, (1600) False."""
        return self.withdrawn_from is not None and draw >= self.withdrawn_from

    def in_prevailing_cohort_at(self, draw: int) -> bool:
        """True if the method counts in the second OV-1 series at `draw`: in place before it and not retired
        from a draw at or below it."""
        return self.eligible_from is not None and self.eligible_from <= draw and not self.is_withdrawn_at(draw)


def read_flag(path: Path) -> dict:
    """Read one small file.

    Returns {key: value text} in the file's order, for example {'fingerprint': 'ab12...',
    'in_place_since_POWERBALL': '1591'}; {} if the file does not exist. Blank lines and lines that begin with a
    semicolon are passed over.
    Refuses (FlagFault) a file that is not plain text, or a line without " = ".
    """
    if not path.is_file():
        return {}
    try:
        text = path.read_bytes().decode('ascii')
    except UnicodeDecodeError:
        raise FlagFault(f'{path}: not plain text. Correct the file or delete it.') from None
    found = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith(';'):
            continue
        key, separator, value = line.partition(' = ')
        if not separator or not key.strip():
            raise FlagFault(f'{path} line {number}: not "key = value". Correct the file or delete it.')
        found[key.strip()] = value.strip()
    return found


def write_flag(path: Path, pairs: dict, first_line: str) -> None:
    """Write one small file whole: a comment line, then one "key = value" a line, CRLF.

    path: the file.  pairs: {key: value}, written in this order.  first_line: what the file is, in a few words.
    The file is written beside itself under another name and then put in place, so that a reader finds the old
    file or the new one and never half of one.
    """
    text = f'; {first_line}{LINE_ENDING}' + ''.join(f'{key} = {value}{LINE_ENDING}' for key, value in pairs.items())
    staged = path.with_name(path.name + STAGED_SUFFIX)
    staged.write_bytes(text.encode('ascii'))
    os.replace(staged, path)


def _draw(path: Path, pairs: dict, key: str) -> int | None:
    """The whole number a key holds, or None if the key is absent. Refuses (FlagFault) anything else."""
    if key not in pairs:
        return None
    if not pairs[key].isdigit():
        raise FlagFault(f'{path}: "{key}" must be a draw number; found "{pairs[key]}". Correct the file.')
    return int(pairs[key])


def status_of(folder: Path, game_id: str) -> MethodStatus:
    """A method's status in a game, from the two small files in its folder that bear on it.

    folder: the method's folder.  game_id: the game.
    Returns for example MethodStatus(withdrawn_from=None, withdrawn_reason=None, eligible_from=1592).
    The job calls settle_retired first, so that a retired file always names a draw for the game.
    Refuses (FlagFault) a retired file that cannot be read: whether a method is retired must be known. An
    IN_PLACE_SINCE that cannot be read never refuses: it is bookkeeping, and reads as "not known" (the job
    writes it afresh; see settle_in_place).
    """
    retired_path, in_place_path = folder / RETIRED_NAME, folder / IN_PLACE_NAME
    withdrawn_from = reason = None
    if retired_path.is_file():
        retired = read_flag(retired_path)
        withdrawn_from = _draw(retired_path, retired, f'retired_from_{game_id}')
        reason = retired.get('reason') or 'no reason was written'
    try:
        since = _draw(in_place_path, read_flag(in_place_path), f'in_place_since_{game_id}')
    except FlagFault:
        since = None
    return MethodStatus(withdrawn_from=withdrawn_from, withdrawn_reason=reason,
                        eligible_from=None if since is None else since + 1)


def settle_in_place(folder: Path, fingerprint: str, game_id: str, last_draw: int) -> str | None:
    """Bring a method's IN_PLACE_SINCE up to date for one game, as the research job does when it opens the game.

    folder: the method's folder.  fingerprint: the method's fingerprint now.  game_id: the game.
    last_draw: the last draw the tree holds for the game at this moment.
    If the file names another fingerprint (the code changed), or is missing or unreadable, it is written afresh
    with this game's draw alone: the other game's draw is written when that game is next worked. If it names
    this fingerprint and has no draw for the game, the draw is added. Otherwise nothing is written.
    Returns None if nothing was written, otherwise why the file was written: one of the WRITTEN_... texts
    below, for example WRITTEN_UNREADABLE. Refuses nothing; a file that cannot be written raises OSError.
    """
    path = folder / IN_PLACE_NAME
    key = f'in_place_since_{game_id}'
    why = WRITTEN_FIRST if not path.exists() else None
    try:
        pairs = read_flag(path)
        if any(not value.isdigit() for name, value in pairs.items() if name.startswith('in_place_since_')):
            raise FlagFault(f'{path}: a draw that is not a number')
    except FlagFault:
        pairs, why = {}, WRITTEN_UNREADABLE
    if pairs.get('fingerprint') != fingerprint:
        pairs, why = {'fingerprint': fingerprint}, why or WRITTEN_CHANGED
    if key in pairs:
        return None
    pairs[key] = str(last_draw)
    write_flag(path, pairs, 'Written by the research job: the last draw this tree held when this version of the '
                            'method was first used here. Bookkeeping only.')
    return why or WRITTEN_GAME


def settle_retired(folder: Path, game_id: str, last_draw: int) -> bool:
    """Give a method's I_AM_RETIRED a draw for one game if it has none, as the research job does when it opens
    the game: the method is then retired from the draw after the last one the tree holds. So a retired file made
    by hand, even an empty one, retires the method from now on and leaves its earlier results as they are.

    Returns True if the file was written. Does nothing if the method has no such file.
    Refuses (FlagFault) a file that cannot be read.
    """
    path = folder / RETIRED_NAME
    key = f'retired_from_{game_id}'
    if not path.is_file():
        return False
    pairs = read_flag(path)
    if key in pairs:
        return False
    reason = pairs.pop('reason', 'no reason was written')
    pairs[key] = str(last_draw + 1)
    pairs['reason'] = reason
    write_flag(path, pairs, RETIRED_FIRST_LINE)
    return True


def write_installable(folder: Path, fingerprints: dict, made: str) -> bool:
    """Write an I_AM_INSTALLABLE flag ("make installable", in DEV), unless the flag there already says the same.

    folder: the method's folder, or the tree's src folder for the infrastructure's flag.
    fingerprints: what the flag vouches for, for example {'fingerprint': 'ab12...'}; for the infrastructure also
    {'updater_fingerprint': 'cd34...'}.  made: when, as text, for the reader.
    Returns True if the file was written; False if it already held these fingerprints (it is then left as it is,
    with its earlier time).
    """
    path = folder / INSTALLABLE_NAME
    try:
        held = read_flag(path)
    except FlagFault:
        held = {}
    if {key: held.get(key) for key in fingerprints} == fingerprints:
        return False
    write_flag(path, {**fingerprints, 'made': made}, 'This version may be installed (written by Make_Installable.bat '
                                                    'in DEV). It is out of date once the files it names change.')
    return True


def installable_state(folder: Path, fingerprints: dict) -> str:
    """How a folder's I_AM_INSTALLABLE flag stands against what is in the folder now: NOT_FLAGGED (no flag, or one
    that cannot be read), FLAG_OUT_OF_DATE (the flag names other fingerprints: the files changed since) or
    FLAGGED.  fingerprints: as for write_installable, computed from the files now."""
    try:
        held = read_flag(folder / INSTALLABLE_NAME)
    except FlagFault:
        held = {}
    if not held:
        return NOT_FLAGGED
    return FLAGGED if {key: held.get(key) for key in fingerprints} == fingerprints else FLAG_OUT_OF_DATE


def write_retired(folder: Path, retired_from: dict, reason: str) -> None:
    """Write a method's I_AM_RETIRED.

    folder: the method's folder.  retired_from: {game: the draw from which it stops}, for example
    {'POWERBALL': 1601, 'OZLOTTO': 1712}.  reason: one line of plain text.
    Refuses (FlagFault) a reason that is not one line of plain printable text.
    """
    reason = reason.strip()
    if not reason or not reason.isascii() or not reason.isprintable():
        raise FlagFault(f'the reason must be one line of plain printable text; found {reason!r}.')
    pairs = {f'retired_from_{game_id}': str(draw) for game_id, draw in retired_from.items()}
    pairs['reason'] = reason
    write_flag(folder / RETIRED_NAME, pairs, RETIRED_FIRST_LINE)
