"""The one ledger writer the synthetic fixtures share (MHUP-A, EX_142 B03): a master ledger of exactly the updater's
grammar (design v0.1r5 section 3.2 rule 1), so that the production rules apply to every fixture in full. A one-row
INIT ledger here has the exact LEDGER_COLUMNS header, a UTC instant, a tool version and digest, the added fields and
an ASCII note; grown ledgers (tests/mhupa_fixtures.py) add UPDATE and NO_CHANGE rows with the same writer.

Fixture values only: the tool digest is a fixed string, the instants are invented. No real draw is written."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

LEDGER_COLUMNS = ('version', 'utc', 'action', 'master_sha256', 'first_draw', 'last_draw', 'draw_count',
                  'added_count', 'added_first', 'added_last', 'grab_file', 'grab_sha256',
                  'backup_file', 'backup_sha256', 'tool_version', 'tool_sha256', 'note')
T0 = datetime(2026, 10, 21, 3, 0, 0, tzinfo=timezone.utc)
FIXTURE_TOOL_SHA = '0' * 64


def utc_at(i: int) -> str:
    """An invented UTC instant, i hours after T0, in the updater's isoformat (+00:00)."""
    return (T0 + timedelta(hours=i)).isoformat()


def init_row(profile, master_sha256: str, *, note: str = 'fixture INIT') -> dict:
    """The INIT row of a synthetic master that covers exactly the development prefix."""
    count = profile.holdout_first - profile.first_draw
    return {'version': 1, 'utc': utc_at(0), 'action': 'INIT', 'master_sha256': master_sha256,
            'first_draw': profile.first_draw, 'last_draw': profile.holdout_first - 1, 'draw_count': count,
            'added_count': count, 'added_first': profile.first_draw, 'added_last': profile.holdout_first - 1,
            'tool_version': '0.1', 'tool_sha256': FIXTURE_TOOL_SHA, 'note': note}


def ledger_bytes(rows: list[dict], *, eol: str = '\r\n') -> bytes:
    """The ledger file: the exact header, one record per physical line, every column, CRLF as the updater writes."""
    lines = [','.join(LEDGER_COLUMNS)]
    for r in rows:
        fields = [str(r.get(c, '')) for c in LEDGER_COLUMNS]
        assert all(',' not in f and '"' not in f and '\n' not in f for f in fields), 'fixture fields are plain'
        lines.append(','.join(fields))
    return (eol.join(lines) + eol).encode('ascii')


def write_ledger(path: Path, rows: list[dict], *, eol: str = '\r\n') -> None:
    Path(path).write_bytes(ledger_bytes(rows, eol=eol))


def write_init_ledger(path: Path, profile, master_sha256: str) -> None:
    """A one-row INIT ledger for a synthetic full-prefix master whose whole-file SHA-256 is `master_sha256`."""
    write_ledger(path, [init_row(profile, master_sha256)])
