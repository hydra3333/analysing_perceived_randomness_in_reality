"""MHUP-A: the version-2 master rules (Mode H, results update and prospective design v0.1r5, section 3.2).

Orchestration-only. Nothing here reaches a method: no output of this module ever enters a DrawView, a
permitted-view digest or a method task (the B1 rule holds). It reads the master ledger and the master file
of one game through the reader's trusted-file helper and checks, before any row is served:

1. The ledger chain (the closed grammar, design 3.2 rule 1). Row 1 is the INIT row with today's checks of
   its own fields; every later row is UPDATE or NO_CHANGE with the cross-row rules; versions are
   1, 2, 3, ... with no gap; anything else refuses.
2. Prefix-verified pins (rule 2). Because the owner's updater only appends and re-serialises with the same
   function, version v's bytes are an exact prefix of every later version: the SHA-256 of the first
   1 + draw_count(v) lines of the current master must equal row v's master_sha256, the first field of the
   last of those lines must be last_draw(v), and the whole file's SHA-256 must equal the last row's. A run
   pins (ledger_version v, master_sha256 s); the pin is accepted when row v exists with that SHA-256 and
   passed the prefix check. A corrected earlier row or an interrupted update (master replaced, ledger not
   appended) fails here, and every reader refuses.
3. The target gate (rule 3): for a pin to version v, targets up to last_draw(v) + 1; a target at or above
   the game's holdout_first additionally needs a valid opening record (design 4.2) and the mode gates of
   3.4, which are checked by the request validator, the dispatch gate and the runner, not here.

LEDGER_COLUMNS is the module's own copy of the updater's columns; a test asserts equality with the owner's
tool (the tool is never imported by project code). The grammar is applied in full whenever the ledger holds
more than one row; a single-row (INIT) ledger is checked exactly as every reader checked it before this
module (its fields and the INIT verification record), so every existing synthetic fixture and the committed
version-1 records stay valid without a byte changed.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import re

from _common.game_draws_reader import _trusted_file_bytes
from _common.game_profiles import get_profile

LEDGER_COLUMNS = ('version', 'utc', 'action', 'master_sha256', 'first_draw', 'last_draw', 'draw_count',
                  'added_count', 'added_first', 'added_last', 'grab_file', 'grab_sha256',
                  'backup_file', 'backup_sha256', 'tool_version', 'tool_sha256', 'note')
INIT_SOURCE = 'LOTTERYWEST_GOV_RESULTS_SEARCH'
_SHA = re.compile(r'[0-9a-f]{64}\Z', re.ASCII)
_DIGIT = re.compile(rb'(0|[1-9][0-9]*)\Z', re.ASCII)
_INT = re.compile(r'(0|[1-9][0-9]*)\Z', re.ASCII)


class LedgerRefused(ValueError):
    """The ledger, the master or a pin failed a check; nothing was served."""


@dataclass(frozen=True)
class LedgerRow:
    version: int
    action: str
    master_sha256: str
    first_draw: int
    last_draw: int
    draw_count: int


def _int_field(row: dict, name: str, where: str) -> int:
    v = row.get(name)
    if type(v) is not str or not _INT.fullmatch(v):
        raise LedgerRefused(f'{where}: {name} is not a whole number')
    return int(v)


def _sha_field(row: dict, name: str, where: str, *, required: bool) -> str | None:
    v = row.get(name)
    if v is None or v == '':
        if required:
            raise LedgerRefused(f'{where}: {name} is missing')
        return None
    if type(v) is not str or not _SHA.fullmatch(v):
        raise LedgerRefused(f'{where}: {name} is not 64 lower-case hex digits')
    return v


def _utc_instant(text: object, where: str) -> datetime:
    if type(text) is not str or not text:
        raise LedgerRefused(f'{where}: utc is missing')
    try:
        t = datetime.fromisoformat(text)
    except ValueError:
        raise LedgerRefused(f'{where}: utc is not an ISO-8601 instant') from None
    if t.tzinfo is None or t.utcoffset().total_seconds() != 0:
        raise LedgerRefused(f'{where}: utc is not a UTC instant')
    return t


def parse_ledger(raw: bytes, game_id: str) -> list[LedgerRow]:
    """The closed grammar (design 3.2 rule 1). Returns the rows, version 1 first. Refuses on any break."""
    p = get_profile(game_id)
    try:
        text = raw.decode('ascii')
    except UnicodeDecodeError:
        raise LedgerRefused('ledger is not ASCII') from None
    if not text.endswith('\n'):
        raise LedgerRefused('ledger does not end with a line ending (truncated?)')
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise LedgerRefused('ledger has no rows')
    header = tuple(rows[0].keys())
    if len(rows) > 1 and header != LEDGER_COLUMNS:
        raise LedgerRefused('ledger header is not the updater\'s LEDGER_COLUMNS')
    out: list[LedgerRow] = []
    previous_utc = None
    for i, row in enumerate(rows, start=1):
        where = f'ledger row {i}'
        if None in row or any(v is None for v in row.values()):
            raise LedgerRefused(f'{where}: wrong number of fields')
        version = _int_field(row, 'version', where)
        if version != i:
            raise LedgerRefused(f'{where}: version {version} out of order (expected {i})')
        action = row.get('action')
        sha = _sha_field(row, 'master_sha256', where, required=True)
        first = _int_field(row, 'first_draw', where)
        last = _int_field(row, 'last_draw', where)
        count = _int_field(row, 'draw_count', where)
        if first != p.first_draw:
            raise LedgerRefused(f'{where}: first_draw is not the era\'s first draw')
        if count != last - first + 1 or count < 1:
            raise LedgerRefused(f'{where}: draw_count disagrees with first_draw and last_draw')
        if i == 1:
            if action != 'INIT':
                raise LedgerRefused(f'{where}: the first row is not INIT')
            if last != p.holdout_first - 1 or count != p.holdout_first - p.first_draw:
                raise LedgerRefused(f'{where}: the INIT row does not cover exactly the development prefix')
            if len(rows) > 1:
                previous_utc = _utc_instant(row.get('utc'), where)
                added = _int_field(row, 'added_count', where)
                if added != count or _int_field(row, 'added_first', where) != first or \
                        _int_field(row, 'added_last', where) != last:
                    raise LedgerRefused(f'{where}: the INIT row\'s added fields disagree with its counts')
        else:
            prev = out[-1]
            t = _utc_instant(row.get('utc'), where)
            if t < previous_utc:
                raise LedgerRefused(f'{where}: utc decreases')
            previous_utc = t
            if not row.get('tool_version'):
                raise LedgerRefused(f'{where}: tool_version is empty')
            _sha_field(row, 'tool_sha256', where, required=True)
            _sha_field(row, 'grab_sha256', where, required=True)
            if not row.get('grab_file'):
                raise LedgerRefused(f'{where}: grab_file is missing')
            if not (row.get('note') or '').isascii():
                raise LedgerRefused(f'{where}: note is not ASCII')
            added = _int_field(row, 'added_count', where)
            if action == 'NO_CHANGE':
                if sha != prev.master_sha256 or last != prev.last_draw or count != prev.draw_count or added != 0:
                    raise LedgerRefused(f'{where}: NO_CHANGE row differs from the row before it')
                for f in ('added_first', 'added_last', 'backup_file', 'backup_sha256'):
                    if row.get(f) not in (None, ''):
                        raise LedgerRefused(f'{where}: NO_CHANGE row has {f}')
            elif action == 'UPDATE':
                a_first = _int_field(row, 'added_first', where)
                a_last = _int_field(row, 'added_last', where)
                if added < 1 or a_first != prev.last_draw + 1 or a_last != last or a_last != a_first + added - 1 \
                        or count != prev.draw_count + added:
                    raise LedgerRefused(f'{where}: UPDATE row\'s added range disagrees with the row before it')
                if _sha_field(row, 'backup_sha256', where, required=True) != prev.master_sha256:
                    raise LedgerRefused(f'{where}: backup_sha256 is not the previous master')
                if not row.get('backup_file'):
                    raise LedgerRefused(f'{where}: backup_file is missing')
                if sha == prev.master_sha256:
                    raise LedgerRefused(f'{where}: UPDATE row repeats the previous master_sha256')
            else:
                raise LedgerRefused(f'{where}: action {action!r} is not INIT, UPDATE or NO_CHANGE')
        out.append(LedgerRow(version, action, sha, first, last, count))
    return out


def _lines_with_endings(raw: bytes) -> list[bytes]:
    return raw.splitlines(keepends=True)


def verify_master_against_ledger(raw_master: bytes, rows: list[LedgerRow], game_id: str) -> None:
    """Prefix-verified pins (design 3.2 rule 2): every row's SHA-256 is the digest of the header plus that row's
    draws, as stored; the last of those lines starts with last_draw(row); the whole file equals the last row."""
    p = get_profile(game_id)
    lines = _lines_with_endings(raw_master)
    if not lines:
        raise LedgerRefused('master is empty')
    if hashlib.sha256(raw_master).hexdigest() != rows[-1].master_sha256:
        raise LedgerRefused('complete master bytes differ from the last ledger row\'s SHA-256 (edited outside the tool, or an '
                            'update was interrupted)')
    if len(rows) == 1:
        # A version-1-only ledger: the whole file IS the prefix, and the hash above has just bound it, exactly as
        # every reader did before this module. The line-count rules below bind each version's rows once the
        # ledger has grown (the updater verifies the counts itself at every run).
        return
    for row in rows:
        n = 1 + row.draw_count
        if len(lines) < n:
            raise LedgerRefused(f'master has fewer lines than ledger row {row.version} records')
        prefix = b''.join(lines[:n])
        if hashlib.sha256(prefix).hexdigest() != row.master_sha256:
            raise LedgerRefused(f'master prefix for ledger row {row.version} does not hash to its master_sha256 '
                                f'(an earlier version was changed?)')
        first_field = lines[n - 1].split(b',', 1)[0]
        if not _DIGIT.fullmatch(first_field) or int(first_field) != row.last_draw:
            raise LedgerRefused(f'the last draw of version {row.version} is not {row.last_draw}')
        if lines[n - 1][-1:] not in (b'\n',):
            raise LedgerRefused(f'version {row.version} does not end with a line ending')
    if len(lines) != 1 + rows[-1].draw_count:
        raise LedgerRefused('master has more lines than the last ledger row records')


def resolve_pin(rows: list[LedgerRow], ledger_version: object, master_sha256: object) -> LedgerRow:
    """The row a run pins: row `ledger_version` must exist and carry exactly `master_sha256`."""
    if type(ledger_version) is not int or not 1 <= ledger_version <= len(rows):
        raise LedgerRefused(f'pinned ledger version {ledger_version!r} does not exist (the ledger has {len(rows)} rows)')
    row = rows[ledger_version - 1]
    if type(master_sha256) is not str or master_sha256 != row.master_sha256:
        raise LedgerRefused(f'pinned master_sha256 is not ledger row {ledger_version}\'s')
    return row


def target_admissible(game_id: str, target: object, row: LedgerRow) -> bool:
    """Rule 3's first half: a target is readable from version v only up to last_draw(v) + 1 and only after the
    era's first draw. The holdout condition (opening record and mode gates) is checked by the callers named above."""
    p = get_profile(game_id)
    return type(target) is int and p.first_draw + 1 <= target <= row.last_draw + 1


def check_init_evidence(evidence: object, game_id: str, rows: list[LedgerRow]) -> dict:
    """The INIT verification record (already read), checked against row 1 exactly as every reader checked it before."""
    p = get_profile(game_id)
    name = f'{game_id}_results_master.csv'
    r1 = rows[0]
    if (type(evidence) is not dict or evidence.get('master_sha256') != r1.master_sha256 or
            evidence.get('master_file') != name or evidence.get('game') != game_id or
            evidence.get('first_draw') != p.first_draw or evidence.get('last_draw') != p.holdout_first - 1 or
            evidence.get('draw_count') != p.holdout_first - p.first_draw or evidence.get('source') != INIT_SOURCE):
        raise LedgerRefused('INIT verification does not match the pinned source')
    return evidence


def check_source(ledger_raw: bytes, master_raw: bytes, evidence_raw: bytes, game_id: str) -> list[LedgerRow]:
    """Rules 1 and 2 and the INIT record check, on bytes the caller has already read through the trusted-file
    helper. Returns the ledger rows. No file is opened here."""
    rows = parse_ledger(ledger_raw, game_id)
    verify_master_against_ledger(master_raw, rows, game_id)
    try:
        evidence = json.loads(evidence_raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise LedgerRefused(f'INIT verification record unreadable: {exc}') from None
    check_init_evidence(evidence, game_id, rows)
    return rows


def source_paths(repo_root: Path, game_id: str) -> tuple[Path, Path, Path]:
    """(ledger, master, INIT verification record) under the root's source_data/."""
    get_profile(game_id)
    folder = Path(repo_root) / 'source_data'
    return (folder / f'{game_id}_results_master_ledger.csv', folder / f'{game_id}_results_master.csv',
            folder / f'{game_id}_results_master_init_verification.json')


def load_verified_source(repo_root: Path, game_id: str) -> tuple[bytes, list[LedgerRow], dict]:
    """Read the ledger, the master and the INIT record of one game through the trusted-file helper, apply rules 1
    and 2, and return (master bytes, ledger rows, INIT evidence). The caller resolves its own pin and target."""
    ledger_path, master_path, evidence_path = source_paths(repo_root, game_id)
    try:
        ledger_raw = _trusted_file_bytes(ledger_path)
        master_raw = _trusted_file_bytes(master_path)
        evidence_raw = _trusted_file_bytes(evidence_path)
    except ValueError as exc:
        raise LedgerRefused(f'source file: {exc}') from None
    rows = check_source(ledger_raw, master_raw, evidence_raw, game_id)
    return master_raw, rows, json.loads(evidence_raw)


def current_pin(repo_root: Path, game_id: str) -> tuple[int, str]:
    """(version, master_sha256) of the ledger's current last row, after rules 1 and 2. Orchestration only."""
    _raw, rows, _ev = load_verified_source(repo_root, game_id)
    return rows[-1].version, rows[-1].master_sha256


def ledger_sha256(repo_root: Path, game_id: str) -> str:
    """The ledger file's own SHA-256 (receipt provenance), through the trusted-file helper."""
    return hashlib.sha256(_trusted_file_bytes(Path(repo_root) / 'source_data' / f'{game_id}_results_master_ledger.csv')).hexdigest()
