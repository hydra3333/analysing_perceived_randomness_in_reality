"""WF-1B: the outcome reader, evaluator only (releases and WF-1 design v0.1r1 section 6.3; R3 17.12).

Orchestration-only. No method file may import it (a static check, MRT-05), and it imports no method code. It is
called only by the report tool, and only after the search-log row and the scoring plan are written (design 6.1).

Checks first, before any row is decoded (the same checks as the installed reader, `game_draws_reader`, whose file
helper is reused without editing the reader):
- every requested target is a whole number in [E(G) + 1, holdout_first - 1] (the development prefix); otherwise
  the whole request is refused and nothing is read;
- the ledger passes the version-2 chain and prefix rules (MHUP-A, _common.master_versions), and the plan's pin
  (ledger_version, master_sha256) is one of its rows; the INIT verification record matches row 1;
- every file is a trusted single-link regular file.

Then it reads the master line by line, from the first draw, and stops after the last requested target. Each line's
draw number is taken from its RAW FIRST FIELD only; a line is decoded only when its number is a requested target.
No line at or after the holdout's first draw is ever decoded (it stops before it, and refuses targets there).

Outcomes are returned only for the requested targets. For Oz Lotto, the three supplementary numbers are returned
only so that the caller can compute `supplementary_matches` and the division (R2 2.5; R3 17.8); the caller never
stores them (design 6.3).
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

from _common.game_draws_reader import _trusted_file_bytes, header_for
from _common.game_profiles import get_profile
import _common.master_versions as MV

_DIGIT = re.compile(rb'(0|[1-9][0-9]*)\Z', re.ASCII)
_SHA = re.compile(r'[a-f0-9]{64}\Z', re.ASCII)


class OutcomeRefused(Exception):
    """The request or the source failed a check; nothing was returned."""


def _check_targets(game_id: str, targets) -> list[int]:
    p = get_profile(game_id)
    out = sorted(set(targets))
    if not out:
        raise OutcomeRefused('no target requested')
    for t in out:
        if type(t) is not int or not (p.first_draw + 1 <= t <= p.holdout_first - 1):
            raise OutcomeRefused(f'target {t!r} is outside the development prefix '
                                 f'[{p.first_draw + 1}, {p.holdout_first - 1}]')
    return out


def _verify_source(repo_root: Path, game_id: str, master_sha256: str, ledger_version: int = 1) -> bytes:
    """MHUP-A (design 3.2 rule 5): the same chain and pin rules as the reader. The pinned version's bytes are an
    exact prefix of the current master, so the outcome of a draw at or below last_draw(v) is read from that prefix.
    Until the Mode H scorer's freeze-before-outcome rule (design 5.3) is installed, every target at or above the
    holdout's first draw is still refused by _check_targets, whatever the version."""
    if type(master_sha256) is not str or not _SHA.fullmatch(master_sha256):
        raise OutcomeRefused('invalid master pin')
    ledger_path, master_path, evidence_path = MV.source_paths(repo_root, game_id)
    try:
        ledger_raw = _trusted_file_bytes(ledger_path)
        raw = _trusted_file_bytes(master_path)
        rows = MV.check_source(ledger_raw, raw, _trusted_file_bytes(evidence_path), game_id)
        row = MV.resolve_pin(rows, ledger_version, master_sha256)
    except (ValueError, UnicodeDecodeError) as exc:
        raise OutcomeRefused(f'the ledger does not bind the pinned master: {exc}') from None
    # Serve only the pinned version's own rows: the prefix that hashes to the pin.
    return MV.prefix_bytes(raw, row)


def _number(text: str, high: int, what: str) -> int:
    if not text.isascii() or not text.isdecimal() or text.startswith('0'):
        raise OutcomeRefused(f'invalid {what}')
    v = int(text)
    if not 1 <= v <= high:
        raise OutcomeRefused(f'invalid {what}')
    return v


def read_outcomes(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1) -> dict:
    """{target: (drawn_main, drawn_powerball)} for Powerball, or {target: (drawn_main, drawn_supplementaries)} for
    Oz Lotto, both as ascending tuples, for exactly the requested targets. Refuses (OutcomeRefused) before
    decoding any row if a target or a source check fails. `ledger_version` is the pinned version (MHUP-A)."""
    if not isinstance(repo_root, Path):
        raise OutcomeRefused('invalid repository root')
    p = get_profile(game_id)
    wanted = _check_targets(game_id, targets)
    raw = _verify_source(repo_root, game_id, master_sha256, ledger_version)
    want = set(wanted)
    last = wanted[-1]                               # < holdout_first, by _check_targets
    high = 35 if game_id == 'POWERBALL' else 47
    width = len(header_for(game_id))
    stream = io.BytesIO(raw)
    if stream.readline().rstrip(b'\r\n').decode('ascii', errors='strict') != ','.join(header_for(game_id)):
        raise OutcomeRefused('wrong master header')
    out = {}
    for i in range(last - p.first_draw + 1):
        line = stream.readline()
        first = line.split(b',', 1)[0]              # the raw first field only, before any decoding
        if not _DIGIT.fullmatch(first) or int(first) != p.first_draw + i:
            raise OutcomeRefused('missing or nonconsecutive draw in the master')
        number = p.first_draw + i
        if number not in want:
            continue                                 # never decoded
        if number >= p.holdout_first:                # unreachable by construction; kept as a second guard
            raise OutcomeRefused('holdout row reached')
        try:
            row = next(csv.reader([line.decode('ascii', errors='strict')], strict=True))
        except (UnicodeDecodeError, csv.Error, StopIteration):
            raise OutcomeRefused(f'undecodable row for draw {number}') from None
        if len(row) != width:
            raise OutcomeRefused(f'malformed row for draw {number}')
        main = tuple(sorted(_number(x, high, 'main number') for x in row[2:9]))
        if len(set(main)) != 7:
            raise OutcomeRefused(f'repeated main number in draw {number}')
        if game_id == 'POWERBALL':
            out[number] = (main, _number(row[9], 20, 'Powerball'))
        else:
            supps = tuple(sorted(_number(x, 47, 'supplementary number') for x in row[9:12]))
            if len(set(supps)) != 3 or set(supps) & set(main):
                raise OutcomeRefused(f'invalid supplementary numbers in draw {number}')
            out[number] = (main, supps)
    if set(out) != want:                             # every requested target must be present
        raise OutcomeRefused('not every requested target was found')
    return out
