"""The list files: a method's forecasts and scores for a game, and the two OV-1 series, as plain line records.

What this file is for
    Everything the research job computes is kept as lists of records, one record a line, in plain text (JSON,
    CRLF). The first line of a list is its header: what the list is, and the fingerprint of the software that
    made it. A method has two lists for each game: its forecasts (one TARGET line a draw, upward by one from its
    first target) and its scores. Nothing in a list is sealed or chained: a list that cannot be read, or that
    was made by other software than is in the tree now, is simply made again by the job.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 5 ("The records").

Which of the project's own modules it uses
    _common.canonical_encoding   canonical_bytes: one record as text, its keys in order

What uses it
    research/game_state.py, research/research_job.py, research/ov1_ledger.py, and the tests.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from _common.canonical_encoding import canonical_bytes

# Where a tree keeps what the job computes; under it, for each game, the folder of the methods' results; and the
# two list files of a method.
RESEARCH_FOLDER = 'results/research'
VARIANTS_FOLDER = 'variants'
FORECASTS_NAME = 'forecasts.jsonl'
SCORES_NAME = 'scores.jsonl'
# The format name every header carries, and the kinds of list.
LIST_FORMAT = 'RESEARCH_LIST_V2'
FORECASTS_KIND = 'FORECASTS'
SCORES_KIND = 'SCORES'
PREVAILING_KIND = 'PREVAILING'
EXPLORATORY_KIND = 'EXPLORATORY'
# The kinds of line: a header, and the one kind of line each kind of list holds after it.
HEADER_LINE = 'HEADER'
TARGET_LINE = 'TARGET'
SCORE_LINE = 'SCORE'
PREVAILING_LINE = 'PREVAILING'
EXPLORATORY_LINE = 'EXPLORATORY'
LINE_OF_LIST = {FORECASTS_KIND: TARGET_LINE, SCORES_KIND: SCORE_LINE, PREVAILING_KIND: PREVAILING_LINE,
                EXPLORATORY_KIND: EXPLORATORY_LINE}
# The line ending of every file this project writes.
LINE_ENDING = b'\r\n'


class ListFault(ValueError):
    """A list cannot be read, or its lines do not follow one another as they must. The message names the file
    and the line. The job makes the method's results again."""


@dataclass
class ListOnFile:
    """A list as read from disk.

    path: the file.  header: the first line.  lines: the lines after the header, in order.
    torn_bytes: how many bytes of an unfinished last line follow the last complete line (0 if none).
    """
    path: Path
    header: dict
    lines: list = field(default_factory=list)
    torn_bytes: int = 0


def record_bytes(record: dict) -> bytes:
    """One record as the line a list holds: its keys in order, no spaces, CRLF at the end."""
    return canonical_bytes(record)[:-1] + LINE_ENDING


def variant_folder(tree_root: Path, game_id: str, family: str, variant: str) -> Path:
    """The folder of a method's results for a game, for example
    <tree>/results/research/POWERBALL/variants/E_002/RECUR_MEAN_ALL_V1."""
    return Path(tree_root) / RESEARCH_FOLDER / game_id / VARIANTS_FOLDER / family / variant


def variant_list_paths(tree_root: Path, game_id: str, family: str, variant: str) -> tuple:
    """The two list files of a method for a game: (.../forecasts.jsonl, .../scores.jsonl)."""
    folder = variant_folder(tree_root, game_id, family, variant)
    return folder / FORECASTS_NAME, folder / SCORES_NAME


def make_header(kind: str, game_id: str, family: str, variant: str, variant_fingerprint: str,
                first_target: int | None = None) -> dict:
    """The header line of a method's new list.

    kind: FORECASTS_KIND or SCORES_KIND.  first_target: the first draw with enough earlier draws (forecast list
    only).  variant_fingerprint: the fingerprint of the method's software that makes the list.
    Returns for example {'line': 'HEADER', 'format': 'RESEARCH_LIST_V2', 'list': 'FORECASTS', 'game':
    'POWERBALL', 'family': 'E_002', 'variant': 'RECUR_MEAN_ALL_V1', 'variant_fingerprint': 'ab12...',
    'first_target': 1248}.
    """
    header = {'line': HEADER_LINE, 'format': LIST_FORMAT, 'list': kind, 'game': game_id, 'family': family,
              'variant': variant, 'variant_fingerprint': variant_fingerprint}
    if kind == FORECASTS_KIND:
        header['first_target'] = first_target
    return header


def read_list(path: Path, kind: str) -> ListOnFile | None:
    """Read a list file.

    path: the file.  kind: the kind of list the header must name.
    Returns None if the file does not exist or holds no complete line. Otherwise the ListOnFile; a last line
    without its line ending is unfinished (the job was stopped while writing it): it is not among the lines and
    its length is in torn_bytes.
    Refuses (ListFault): a complete line that is not a JSON record; a first line that is not this kind's
    header; a line of the wrong kind for the list.
    """
    if not path.is_file():
        return None
    pieces = path.read_bytes().split(b'\n')
    torn = pieces.pop()                       # b'' when the file ends with a line ending
    if not pieces:
        return None
    wanted_line = LINE_OF_LIST[kind]
    listed = ListOnFile(path=path, header={}, torn_bytes=len(torn))
    for number, piece in enumerate(pieces, start=1):
        try:
            line = json.loads(piece.decode('ascii'))
            if type(line) is not dict:
                raise ValueError('not a record')
        except (ValueError, UnicodeDecodeError) as error:
            raise ListFault(f'{path} line {number}: not a readable record ({error}).') from None
        if number == 1:
            if line.get('line') != HEADER_LINE or line.get('format') != LIST_FORMAT or line.get('list') != kind:
                raise ListFault(f'{path} line 1: not the header of a {kind} list of format {LIST_FORMAT}.')
            listed.header = line
        elif line.get('line') != wanted_line:
            raise ListFault(f'{path} line {number}: a {line.get("line")} line in a {kind} list.')
        else:
            listed.lines.append(line)
    return listed


def create_list(path: Path, header: dict) -> ListOnFile:
    """Create a list file holding its header line; a file already there is replaced.

    path: the file (its folder is made if needed).  header: make_header's result.  Returns the new ListOnFile.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as stream:
        stream.write(record_bytes(header))
        stream.flush()
        os.fsync(stream.fileno())
    return ListOnFile(path=path, header=header)


def cut_torn_tail(listed: ListOnFile) -> int:
    """Cut an unfinished last line off the file, before the next line is added.

    listed: the list as read.  Returns how many bytes were cut (0 if there was no unfinished line).
    """
    cut = listed.torn_bytes
    if cut:
        os.truncate(listed.path, listed.path.stat().st_size - cut)
        listed.torn_bytes = 0
    return cut


def append_line(listed: ListOnFile, body: dict) -> dict:
    """Add one line to the end of a list.

    listed: the list (an unfinished last line, if any, must have been cut).  body: the line.
    Returns the line as written. The bytes are handed to the operating system before this returns; sync_list
    makes them durable.
    """
    if listed.torn_bytes:
        raise ListFault(f'{listed.path}: an unfinished last line must be cut before a line is added.')
    with open(listed.path, 'ab') as stream:
        stream.write(record_bytes(body))
        stream.flush()
    listed.lines.append(body)
    return body


def sync_list(listed: ListOnFile) -> None:
    """Make every added line of a list durable (flushed to the disk)."""
    with open(listed.path, 'ab') as stream:
        os.fsync(stream.fileno())


def write_whole(path: Path, header: dict, lines: list) -> bool:
    """Write a whole list afresh (the two OV-1 series are made again by every job), unless the file already
    holds exactly these bytes.

    path: the file.  header: its header line.  lines: the lines after it.
    The file is written beside itself under another name and then put in place. Returns True if it was written.
    """
    data = b''.join(record_bytes(record) for record in [header, *lines])
    if path.is_file() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.with_name(path.name + '.writing')
    staged.write_bytes(data)
    os.replace(staged, path)
    return True


def keep_below(path: Path, kind: str, target: int) -> int:
    """Rewrite a method's list so that it keeps only the lines for draws below `target` (used when a draw's
    result was corrected at the source, and when a method is retired).

    path: the list file.  kind: FORECASTS_KIND or SCORES_KIND.  target: the first draw whose line is dropped.
    Returns how many lines were dropped (0 if the file does not exist or nothing is at or above `target`).
    """
    listed = read_list(path, kind)
    if listed is None:
        return 0
    kept = [line for line in listed.lines if line['content']['target'] < target]
    dropped = len(listed.lines) - len(kept)
    if dropped or listed.torn_bytes:
        staged = path.with_name(path.name + '.writing')
        staged.write_bytes(b''.join(record_bytes(record) for record in [listed.header, *kept]))
        os.replace(staged, path)
    return dropped


def check_lists(forecasts: ListOnFile, scores: ListOnFile | None) -> dict:
    """Check that a method's two lists follow on as they must, and summarise them.

    forecasts: the forecast list.  scores: the score list, or None if it does not exist yet.
    Returns {'first_target': the header's first target; 'next_target': the first draw with no TARGET line;
    'scored': the set of scored targets}, for example {'first_target': 1248, 'next_target': 1593, 'scored':
    {1248, ...}}.
    Refuses (ListFault), naming the line: a TARGET line whose target is not the next one (a gap or a repeat); a
    TARGET line that is neither a FORECAST nor a NO_FORECAST with a reason; a score line for a draw that has no
    FORECAST line; score lines whose draws do not rise; a draw scored although an earlier forecast is not (the
    job scores in draw order, so a gap means a line was lost).
    """
    first_target = forecasts.header.get('first_target')
    if type(first_target) is not int:
        raise ListFault(f'{forecasts.path} line 1: the header has no first target.')
    forecast_targets = set()
    for offset, line in enumerate(forecasts.lines):
        content, expected = line.get('content') or {}, first_target + offset
        if content.get('target') != expected:
            raise ListFault(f'{forecasts.path} line {offset + 2}: the target is {content.get("target")} where '
                            f'{expected} is due. TARGET lines run upward by one with no gap and no repeat.')
        if content.get('status') == 'FORECAST':
            forecast_targets.add(expected)
        elif not (content.get('status') == 'NO_FORECAST' and content.get('reason')):
            raise ListFault(f'{forecasts.path} line {offset + 2}: a TARGET line is a FORECAST or a NO_FORECAST '
                            f'with a reason.')
    scored, last_scored = set(), None
    for number, line in enumerate(scores.lines if scores is not None else [], start=2):
        target = (line.get('content') or {}).get('target')
        if target not in forecast_targets:
            raise ListFault(f'{scores.path} line {number}: the score for draw {target} has no FORECAST line.')
        if last_scored is not None and target <= last_scored:
            raise ListFault(f'{scores.path} line {number}: draw {target} follows draw {last_scored}. Score lines '
                            f'rise, and no draw is scored twice.')
        scored.add(target)
        last_scored = target
    unscored = sorted(forecast_targets - scored)
    if unscored and last_scored is not None and last_scored > unscored[0]:
        raise ListFault(f'{scores.path}: draw {last_scored} is scored although the forecast for draw {unscored[0]} '
                        f'is not. Scoring is in draw order and complete.')
    return {'first_target': first_target, 'next_target': first_target + len(forecasts.lines), 'scored': scored}
