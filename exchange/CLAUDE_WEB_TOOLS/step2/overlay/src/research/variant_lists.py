"""The canonical record: a variant's two list files for a game, and their invariants.

What this file is for
    Every result is one line in a list. Each variant has, for each game, a forecast list (a header, then one
    TARGET line for each draw from its first target, upward by one) and a score list (a header, then one line
    for each scored forecast). Every line carries the SHA-256 of the line before it, so a list cannot be changed
    in the middle without the change being seen. This file reads a list and checks the chain; checks the rules
    that tie the two lists together; creates a list; and appends a line. It never rewrites or shortens a list,
    except to cut off a torn last line (a line a crash left half-written), which is not a record.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 5.1 (two list files), 5.2 (the header and
    the lines), 5.6 (invariants 1 to 4; invariant 5 is checked with the status file by the job) and 5.7 (a torn
    last line).

Which of the project's own modules it uses
    _common.canonical_encoding   canonical_bytes: the one way a line is written (sorted keys, ASCII, one LF)
    _common.contract_records     record_digest: to check each TARGET line's content digest

What uses it
    research/research_job.py, research/derived_check.py, research/reports.py, and the engine's tests.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from _common.canonical_encoding import canonical_bytes
from _common.contract_records import record_digest

# Where a tree keeps its research results, and the two list files of a variant (specification 5.1).
RESEARCH_FOLDER = 'results/research'
FORECASTS_NAME = 'forecasts.jsonl'
SCORES_NAME = 'scores.jsonl'
# The format name every header carries, and the two kinds of list.
LIST_FORMAT = 'RESEARCH_LIST_V1'
FORECASTS_KIND = 'FORECASTS'
SCORES_KIND = 'SCORES'
# The three kinds of line.
HEADER_LINE = 'HEADER'
TARGET_LINE = 'TARGET'
SCORE_LINE = 'SCORE'


class ListFault(ValueError):
    """A list breaks one of its rules. The message names the file and the line, says which rule is broken and
    what to do. The game refuses until the owner settles it."""


@dataclass
class ListOnFile:
    """A list as read from disk.

    path: the file.  header: the first line.  lines: the lines after the header, in order.
    last_digest: the SHA-256 of the last complete line's bytes (the next line's "prev").
    torn_bytes: how many bytes of a torn last line follow the last complete line (0 if none).
    """
    path: Path
    header: dict
    lines: list = field(default_factory=list)
    last_digest: str = ''
    torn_bytes: int = 0


def variant_list_paths(tree_root: Path, game_id: str, family: str, variant: str) -> tuple:
    """The two list files of a variant for a game, for example
    (<tree>/results/research/POWERBALL/variants/E_002/RECUR_MEAN_ALL_V1/forecasts.jsonl, .../scores.jsonl)."""
    folder = Path(tree_root) / RESEARCH_FOLDER / game_id / 'variants' / family / variant
    return folder / FORECASTS_NAME, folder / SCORES_NAME


def make_header(kind: str, game_id: str, family: str, variant: str, variant_fingerprint: str,
                forecasting_code_identity: str, first_target: int | None = None) -> dict:
    """The header line of a new list (specification 5.2).

    kind: FORECASTS_KIND or SCORES_KIND.  first_target: the first draw with enough earlier draws (forecast list
    only).  The other arguments are the list's identity and the two identities it is begun under.
    Returns for example {'line': 'HEADER', 'format': 'RESEARCH_LIST_V1', 'list': 'FORECASTS', 'game': 'POWERBALL',
    'family': 'E_002', 'variant': 'RECUR_MEAN_ALL_V1', 'variant_fingerprint': 'ab12...',
    'forecasting_code_identity': 'cd34...', 'first_target': 1248, 'prev': None}.
    """
    header = {'line': HEADER_LINE, 'format': LIST_FORMAT, 'list': kind, 'game': game_id, 'family': family,
              'variant': variant, 'variant_fingerprint': variant_fingerprint,
              'forecasting_code_identity': forecasting_code_identity, 'prev': None}
    if kind == FORECASTS_KIND:
        header['first_target'] = first_target
    return header


def read_list(path: Path, kind: str) -> ListOnFile | None:
    """Read a list file and check its chain (invariant 1).

    path: the file.  kind: FORECASTS_KIND or SCORES_KIND, which the header must name.
    Returns None if the file does not exist or holds no complete line (a crash before the header was written;
    create_list then starts it afresh). Otherwise the ListOnFile; a last line without its line ending is a torn
    line: it is not among the lines and its length is in torn_bytes.
    Refuses (ListFault): a complete line that is not JSON; a first line that is not this kind's header; a line
    whose "prev" is not the SHA-256 of the line before it; a line of the wrong kind for the list.
    """
    if not path.is_file():
        return None
    raw = path.read_bytes()
    pieces = raw.split(b'\n')
    torn = pieces.pop()                       # b'' when the file ends with a line ending
    if not pieces:
        return None
    wanted_line = TARGET_LINE if kind == FORECASTS_KIND else SCORE_LINE
    listed = ListOnFile(path=path, header={}, torn_bytes=len(torn))
    previous_digest = None
    for number, piece in enumerate(pieces, start=1):
        try:
            line = json.loads(piece.decode('ascii'))
            if type(line) is not dict:
                raise ValueError('not an object')
        except (ValueError, UnicodeDecodeError) as error:
            raise ListFault(f'{path} line {number}: not a readable record ({error}). The list is damaged; restore '
                            f'it from a backup, or rerun the variant.') from None
        if line.get('prev') != previous_digest:
            raise ListFault(f'{path} line {number}: the chain is broken (its "prev" is not the digest of the line '
                            f'before it). The list was changed outside the job; restore it from a backup, or '
                            f'rerun the variant.')
        if number == 1:
            if line.get('line') != HEADER_LINE or line.get('format') != LIST_FORMAT or line.get('list') != kind:
                raise ListFault(f'{path} line 1: not the header of a {kind} list.')
            listed.header = line
        else:
            if line.get('line') != wanted_line:
                raise ListFault(f'{path} line {number}: a {line.get("line")} line in a {kind} list.')
            listed.lines.append(line)
        previous_digest = hashlib.sha256(piece + b'\n').hexdigest()
    listed.last_digest = previous_digest
    return listed


def create_list(path: Path, header: dict) -> ListOnFile:
    """Create a list file holding its header line.

    path: the file to create (its folder is made if needed).  header: make_header's result.
    Returns the new ListOnFile.
    Refuses (ListFault) if the file already holds a complete line: a list is never started twice. A file holding
    only the debris of a torn header is started afresh.
    """
    if read_list(path, header['list']) is not None:
        raise ListFault(f'{path}: the list already exists; a list is never created twice.')
    path.parent.mkdir(parents=True, exist_ok=True)
    line = canonical_bytes(header)
    with open(path, 'wb') as stream:
        stream.write(line)
        stream.flush()
        os.fsync(stream.fileno())
    return ListOnFile(path=path, header=header, last_digest=hashlib.sha256(line).hexdigest())


def cut_torn_tail(listed: ListOnFile) -> int:
    """Cut a torn last line off the file, before the next append (specification 5.7).

    listed: the list as read.  Returns how many bytes were cut (0 if the list had no torn line).
    This is the only removal of bytes from a list that the ordinary job ever makes.
    """
    cut = listed.torn_bytes
    if cut:
        os.truncate(listed.path, listed.path.stat().st_size - cut)
        listed.torn_bytes = 0
    return cut


def append_line(listed: ListOnFile, body: dict) -> dict:
    """Append one line to a list.

    listed: the list (its torn tail, if any, must have been cut).  body: the line without its "prev".
    Returns the line as written (with "prev"). The bytes are handed to the operating system before this
    returns; sync_list makes them durable.
    Refuses (ListFault) while a torn tail is still on the file.
    """
    if listed.torn_bytes:
        raise ListFault(f'{listed.path}: a torn last line must be cut before a line is appended.')
    line = dict(body, prev=listed.last_digest)
    raw = canonical_bytes(line)
    with open(listed.path, 'ab') as stream:
        stream.write(raw)
        stream.flush()
    listed.lines.append(line)
    listed.last_digest = hashlib.sha256(raw).hexdigest()
    return line


def sync_list(listed: ListOnFile) -> None:
    """Make every appended line of a list durable (flushed to the disk), before lines that depend on them are
    written elsewhere: forecast lines before their score lines, score lines before an OV-1 line."""
    with open(listed.path, 'ab') as stream:
        os.fsync(stream.fileno())


def check_lists(forecasts: ListOnFile, scores: ListOnFile | None) -> dict:
    """Check a variant's two lists against invariants 2, 3 and 4, and summarise them.

    forecasts: the forecast list.  scores: the score list, or None if it does not exist yet.
    Returns a summary: {'first_target': the header's first target; 'next_target': the first draw with no TARGET
    line; 'forecast_digests': {target: content digest} for each FORECAST line; 'no_forecast': {target: reason};
    'scored': the set of scored targets; 'first_unscored_forecast': the lowest FORECAST target with no score
    line, or None}, for example {'first_target': 1248, 'next_target': 1593, 'forecast_digests': {1248: 'ab..'},
    'no_forecast': {}, 'scored': {1248, ...}, 'first_unscored_forecast': 1592}.
    Refuses (ListFault), naming the line: a TARGET line whose target is not the next one (a gap or a repeat); a
    content digest that is not the digest of the content; a score line that names no FORECAST line by target and
    content digest (a score without a forecast, or for a NO_FORECAST); a score line whose target does not rise
    (a second score); a score beyond an unscored FORECAST.
    """
    first_target = forecasts.header.get('first_target')
    if type(first_target) is not int:
        raise ListFault(f'{forecasts.path} line 1: the header has no first target.')
    forecast_digests, no_forecast = {}, {}
    for offset, line in enumerate(forecasts.lines):
        content, expected = line.get('content', {}), first_target + offset
        if content.get('target') != expected:
            raise ListFault(f'{forecasts.path} line {offset + 2}: the target is {content.get("target")} where '
                            f'{expected} is due. TARGET lines run upward by one with no gap and no repeat.')
        if record_digest(content) != line.get('content_digest'):
            raise ListFault(f'{forecasts.path} line {offset + 2}: the content digest is not the digest of the '
                            f'content.')
        if content.get('status') == 'FORECAST':
            forecast_digests[expected] = line['content_digest']
        elif content.get('status') == 'NO_FORECAST' and content.get('reason'):
            no_forecast[expected] = content['reason']
        else:
            raise ListFault(f'{forecasts.path} line {offset + 2}: a TARGET line is a FORECAST or a NO_FORECAST with '
                            f'a reason.')
    scored, last_scored = set(), None
    for number, line in enumerate(scores.lines if scores is not None else [], start=2):
        content = line.get('content', {})
        target = content.get('target')
        if target not in forecast_digests or content.get('forecast_content_digest') != forecast_digests[target]:
            raise ListFault(f'{scores.path} line {number}: the score for draw {target} names no FORECAST line of '
                            f'{forecasts.path.name} by target and content digest.')
        if last_scored is not None and target <= last_scored:
            raise ListFault(f'{scores.path} line {number}: draw {target} follows draw {last_scored}. Score lines '
                            f'rise, and no target is scored twice.')
        scored.add(target)
        last_scored = target
    unscored = sorted(t for t in forecast_digests if t not in scored)
    first_unscored = unscored[0] if unscored else None
    if first_unscored is not None and last_scored is not None and last_scored > first_unscored:
        raise ListFault(f'{scores.path}: draw {last_scored} is scored although the forecast for draw '
                        f'{first_unscored} is not. Scoring is in order and complete.')
    return {'first_target': first_target, 'next_target': first_target + len(forecasts.lines),
            'forecast_digests': forecast_digests, 'no_forecast': no_forecast, 'scored': scored,
            'first_unscored_forecast': first_unscored}
