"""The reader: the accepted results on file, and the permitted view (the draws before a target, nothing else).

What this file is for
    It reads a tree's accepted results file for a game and checks that the file is whole and is the one its
    version ledger names. For a target draw T it then builds the permitted view: the draws before T and nothing
    else. A method receives only that view. Nothing from draw T or later, and nothing about the file as a whole,
    is in the view or in its digest.

    The view class (DrawView), the prefix parser and the safe file read are the old reader's code, copied
    character for character by exchange/CLAUDE_WEB_TOOLS/step2/make_reader.py from
    src/methods/_common/game_draws_reader.py; a test compares the two. They are between the two marked lines
    below and keep the old file's own comments. The old loader's version, owner-record and Mode H opening-record
    checks are not here: the new system has no holdout, and every draw on file is an ordinary target.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 6 (earlier draws only), section 5.4 (the
    permitted view's digest; the results file's version and SHA-256 for the envelope) and section 7.1 (the
    results on file).

Which of the project's own modules it uses
    _common.game_profiles        get_profile: each game's first draw, barrels and draw dates
    _common.canonical_encoding   canonical_bytes: the encoding the view digest is taken over

What uses it
    research/forecast_engine.py (the view), research/scoring.py and research/research_job.py (the results on
    file), research/results_step.py, and the engine's tests.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
import hashlib
import io
import os
from pathlib import Path
import re
from types import MappingProxyType

import numpy as np
from _common.game_profiles import get_profile

# ---------------------------------------------------------------- copied from the old reader, unchanged (begin)
# @@COPIED_FROM_THE_OLD_READER@@
# ---------------------------------------------------------------- copied from the old reader, unchanged (end)

# Where a tree keeps its accepted results, and the two files of one game.
SOURCE_FOLDER = 'source_data'
MASTER_NAME = '{game_id}_results_master.csv'
LEDGER_NAME = '{game_id}_results_master_ledger.csv'
# The first columns of the version ledger that this reader uses (the updater writes more after them).
LEDGER_FIRST_COLUMNS = ('version', 'utc', 'action', 'master_sha256', 'first_draw', 'last_draw')


class ResultsRefused(ValueError):
    """The accepted results on file cannot be used. The message names the file, says what was found and what to
    do."""


@dataclass(frozen=True)
class ResultsOnFile:
    """A game's accepted results as read from one tree.

    game_id: 'POWERBALL' or 'OZLOTTO'.  raw: the file's bytes.  sha256: their SHA-256.
    first_draw, last_draw: the first and the last draw on file, for example 1144 and 1591.
    version: the version the ledger's last row gives this file, for example 2.
    """
    game_id: str
    raw: bytes
    sha256: str
    first_draw: int
    last_draw: int
    version: int


def results_paths(tree_root: Path, game_id: str) -> tuple:
    """The results file and its version ledger of one game in a tree, for example
    (<tree>/source_data/POWERBALL_results_master.csv, <tree>/source_data/POWERBALL_results_master_ledger.csv)."""
    folder = Path(tree_root) / SOURCE_FOLDER
    return folder / MASTER_NAME.format(game_id=game_id), folder / LEDGER_NAME.format(game_id=game_id)


def check_results_bytes(raw: bytes, game_id: str, where: str) -> int:
    """Check that results bytes are a whole file for the game and return the last draw number.

    raw: the file's bytes.  game_id: the game.  where: the file's name, for messages.
    Returns the last draw on file, for example 1591.
    Refuses (ResultsRefused) a wrong header, an empty file, a blank line, or draw numbers that do not run upward
    by one from the game's first draw. Only each row's first field is read here; a row's numbers are checked by
    the parser when a view or an outcome needs that row.
    """
    profile = get_profile(game_id)
    lines = raw.split(b'\n')
    if lines and lines[-1] == b'':
        lines.pop()
    if not lines or lines[0].rstrip(b'\r').decode('ascii', errors='replace') != ','.join(header_for(game_id)):
        raise ResultsRefused(f'{where}: the first line is not the {game_id} results header. The file is not the '
                             f'accepted results file; restore it from a backup.')
    if len(lines) < 2:
        raise ResultsRefused(f'{where}: it holds no draw.')
    for index, line in enumerate(lines[1:]):
        first_field = line.split(b',', 1)[0]
        if not _DIGIT.fullmatch(first_field) or int(first_field) != profile.first_draw + index:
            raise ResultsRefused(f'{where}: line {index + 2} should be draw {profile.first_draw + index} but begins '
                                 f'"{first_field[:20].decode("ascii", errors="replace")}". The draws must run '
                                 f'upward by one; restore the file from a backup.')
    return profile.first_draw + len(lines) - 2


def results_on_file(tree_root: Path, game_id: str) -> ResultsOnFile:
    """Read a game's accepted results from a tree, with the version its ledger gives them.

    tree_root: the tree's folder.  game_id: the game.
    Returns the ResultsOnFile, for example ResultsOnFile('POWERBALL', b'...', 'e4f2...', 1144, 1591, 2).
    Refuses (ResultsRefused): a missing, linked or changing file; a file that fails check_results_bytes; a ledger
    that cannot be read; or a ledger whose last row does not name this file's SHA-256 and last draw (the results
    file was changed by something other than the updater or the checked copy).
    """
    master_path, ledger_path = results_paths(tree_root, game_id)
    try:
        raw = _trusted_file_bytes(master_path)
        ledger_raw = _trusted_file_bytes(ledger_path)
    except ValueError as error:
        raise ResultsRefused(f'{master_path} or its ledger {ledger_path.name}: {error}. Both files must be ordinary '
                             f'files in this tree; restore them from a backup.') from None
    last_draw = check_results_bytes(raw, game_id, str(master_path))
    digest = hashlib.sha256(raw).hexdigest()
    try:
        rows = list(csv.reader(io.StringIO(ledger_raw.decode('utf-8'), newline=''), strict=True))
        columns, last_row = tuple(rows[0][:len(LEDGER_FIRST_COLUMNS)]), dict(zip(rows[0], rows[-1]))
        if columns != LEDGER_FIRST_COLUMNS or len(rows) < 2:
            raise ValueError('its columns are not the version ledger\'s, or it has no row')
        version, ledger_sha, ledger_last = int(last_row['version']), last_row['master_sha256'], int(last_row['last_draw'])
    except (ValueError, IndexError, KeyError, csv.Error, UnicodeDecodeError) as error:
        raise ResultsRefused(f'{ledger_path}: the version ledger cannot be read ({error}). Restore it from a '
                             f'backup.') from None
    if ledger_sha != digest or ledger_last != last_draw:
        raise ResultsRefused(f'{master_path}: the file on disk (SHA-256 {digest[:12]}..., last draw {last_draw}) is '
                             f'not the one its ledger\'s last row names ({ledger_sha[:12]}..., last draw '
                             f'{ledger_last}). The results were changed outside the updater or the checked copy; '
                             f'restore both files from a backup.')
    return ResultsOnFile(game_id=game_id, raw=raw, sha256=digest, first_draw=get_profile(game_id).first_draw,
                         last_draw=last_draw, version=version)


def first_target(game_id: str, minimum_earlier_draws: int) -> int:
    """The first draw a variant can be asked to forecast: the first with enough earlier draws.

    For example first_target('POWERBALL', 104) is 1248: draws 1144 to 1247 are the 104 earlier draws.
    """
    return get_profile(game_id).first_draw + minimum_earlier_draws


def permitted_view(results: ResultsOnFile, *, method_id: str, variant_id: str, target: int,
                   observation_view: str, include_dates: bool = False) -> DrawView:
    """Build the permitted view for one target: the draws before it, and nothing else.

    results: the game's results on file.  method_id, variant_id: the method's identity as the view digest and the
    tie rule use it, for example 'E_2' and 'RECUR_MEAN_ALL_V1'.  target: the draw to be forecast.
    observation_view: 'UNORDERED_SET', 'OPERATOR_DRAWN_ORDER' or 'PAIRED_DIAGNOSTIC'.  include_dates: whether the
    view carries draw dates.
    Returns the DrawView. Its arrays own copies of the earlier draws only; rows at or after the target are never
    decoded.
    Refuses (ResultsRefused) a target that is not after the first draw and at most one past the last draw on
    file, or an unknown view; a malformed earlier row raises the parser's own ValueError.
    """
    if observation_view not in VIEW_KINDS or type(include_dates) is not bool:
        raise ResultsRefused(f'{variant_id}: "{observation_view}" is not an observation view '
                             f'({", ".join(sorted(VIEW_KINDS))}).')
    if type(target) is not int or not results.first_draw < target <= results.last_draw + 1:
        raise ResultsRefused(f'{results.game_id} target {target}: a target must be after draw {results.first_draw} '
                             f'and at most {results.last_draw + 1}, one past the last draw on file.')
    numbers, dates, drawn, sorted_main, powerball = _parse_prefix(results.raw, results.game_id, target,
                                                                  include_dates=include_dates)
    order_evidence = {'record': f'{results.game_id}_results_master_init_verification.json', 'status': _ORDER_STATUS}
    return DrawView(game_id=results.game_id, method_id=method_id, variant_id=variant_id, target=target,
                    kind=observation_view, numbers=numbers, dates=dates,
                    main=(drawn if observation_view == 'OPERATOR_DRAWN_ORDER' else sorted_main),
                    powerball=powerball, drawn_main=(drawn if observation_view == 'PAIRED_DIAGNOSTIC' else None),
                    order_status=_ORDER_STATUS,
                    order_evidence=(order_evidence if observation_view != 'UNORDERED_SET' else None))
