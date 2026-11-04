"""WF-1B: the outcome reader, evaluator only (releases and WF-1 design v0.1r1 section 6.3; R3 17.12).

Orchestration-only. No method file may import it (a static check, MRT-05), and it imports no method code. It is
called only by the report tool, and only after the search-log row and the scoring plan are written (design 6.1).

Checks first, before any row is decoded (the same checks as the installed reader, `game_draws_reader`, whose file
helper is reused without editing the reader):
- every requested target is a whole number in [E(G) + 1, holdout_first - 1] (the development prefix), or a
  holdout draw the freeze-before-outcome rule releases to the Mode H scorer (MHUP-A, design 5.3:
  `outcome_release_allowed`); otherwise the whole request is refused and nothing is read;
- the ledger passes the version-2 chain and prefix rules (MHUP-A, _common.master_versions), and the plan's pin
  (ledger_version, master_sha256) is one of its rows; the INIT verification record matches row 1;
- every file is a trusted single-link regular file.

Then it reads the master line by line, from the first draw, and stops after the last requested target. Each line's
draw number is taken from its RAW FIRST FIELD only; a line is decoded only when its number is a requested target.
No line at or after the holdout's first draw is ever decoded unless the freeze-before-outcome rule released that
draw (then only the released, requested holdout draws are decoded); a draw after the holdout is never decoded in
this package (the weekly freeze-line rule arrives with MHUP-B).

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


def outcome_release_allowed(repo_root: Path, game_id: str, target: int) -> bool:
    """The freeze-before-outcome rule (design 5.3; an always-review subject). Orchestration-only, fixed evidence paths
    under the project root, no caller-chosen inputs beyond the root the report already fixes (E2RC2-B01, B02).
    Decides whether the outcome of `target` may be served to the Mode H scorer; says nothing about its existence.
    For a holdout draw: only when the game's one Mode H batch has its BATCH_COMPLETE and SCORING_STARTED markers,
    SCORING_STARTED's roster digest equals the exact roster of the plan (every planned pair with its DONE ticket, by
    identity, computed here from the records), the target is one of the plan's, and SCORE_COMPLETE does not yet
    exist (after it, no outcome is re-read, 5.2). For a draw after the holdout: never in this package (the weekly
    freeze-line rule is MHUP-B's). Anything invalid or absent refuses (False)."""
    import _common.owner_records as OR
    p = get_profile(game_id)
    if type(target) is not int or target > p.holdout_last or target < p.holdout_first:
        return False
    try:
        rec = OR.batch_id_record(repo_root, game_id)
        if rec is None:
            return False
        plan = OR.mode_h_plan(repo_root, game_id, rec['batch_id'])
        if target not in plan['targets']:
            return False
        present = OR.lifecycle_markers_present(repo_root, game_id, rec['batch_id'])
        if 'BATCH_COMPLETE' not in present or 'SCORING_STARTED' not in present or 'SCORE_COMPLETE' in present:
            return False
        started = OR.marker(repo_root, game_id, rec['batch_id'], 'SCORING_STARTED')
        return started['roster_digest'] == OR.roster_digest(repo_root, game_id, plan)
    except OR.RecordRefused:
        return False


def _check_targets(game_id: str, targets, repo_root: Path | None = None) -> list[int]:
    p = get_profile(game_id)
    out = sorted(set(targets))
    if not out:
        raise OutcomeRefused('no target requested')
    for t in out:
        if type(t) is not int or t < p.first_draw + 1 or t > p.holdout_last:
            raise OutcomeRefused(f'target {t!r} is outside [{p.first_draw + 1}, {p.holdout_last}]')
        if t >= p.holdout_first and (repo_root is None or not outcome_release_allowed(repo_root, game_id, t)):
            raise OutcomeRefused(f'target {t} is a holdout draw not released by the freeze-before-outcome rule '
                                 f'(design 5.3)')
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
    wanted = _check_targets(game_id, targets, repo_root)
    raw = _verify_source(repo_root, game_id, master_sha256, ledger_version)
    want = set(wanted)
    last = wanted[-1]                               # <= holdout_last; in the holdout only if released (5.3)
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
        if number >= p.holdout_first and not outcome_release_allowed(repo_root, game_id, number):
            raise OutcomeRefused('holdout row reached without release')     # a second guard; unreachable by construction
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
