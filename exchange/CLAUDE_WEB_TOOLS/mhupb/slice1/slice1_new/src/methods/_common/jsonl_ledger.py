"""MHUP-B: the one write discipline of every JSONL ledger (design v0.1r7 section 6.5) and the forecast ledger's digest
chain.

Orchestration-only, value-agnostic: it never interprets a line beyond its JSON shape.

Writing (`append`): the whole line, with its newline, in one write, then flush and fsync. Before appending, a final
fragment without its newline (a crash in the middle of an earlier append) is copied, as it is, to a side file beside
the ledger and the ledger is cut back to the end of its last complete line; nothing else is ever changed, and nothing
is edited by hand. A reader (`owner_records.read_jsonl`) ignores such a fragment and reports it.

Reading strictly (`read_lines`): every complete line must be exactly the canonical bytes of its record; anything else
refuses. A path that exists but is not a plain file refuses; a ledger never created reads as empty.

The chain (`chained`, `verify_chain`): a chained line carries its 1-based `line_number` and `previous_line_digest`, the
SHA-256 of the canonical bytes of the line before it (None on the first line). What the chain proves (design 6.5): that
the lines agree with each other; compared with an earlier trusted digest, kept separately, it reveals later changes;
by itself it proves neither when the lines were written nor that the whole ledger was never replaced.
"""
from __future__ import annotations

from collections.abc import Mapping
import os
from pathlib import Path
import uuid

from _common.contract_records import canonical, record_digest
from _common import owner_records as OR

LedgerRefused = OR.RecordRefused


def _fsync_dir(folder: Path) -> None:
    try:
        fd = os.open(folder, os.O_RDONLY)
    except OSError:
        return                                            # a platform that cannot open a folder (Windows)
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


def repair_torn_tail(path: Path) -> Path | None:
    """If the ledger ends in a fragment without its newline: copy the fragment to a side file (create-only), cut the
    ledger back to the end of its last complete line, and return the side file; otherwise None."""
    path = Path(path)
    if OR.absent(path):
        return None
    if path.is_symlink() or not path.is_file():
        raise LedgerRefused(f'{path.name}: exists but is not a plain file')
    raw = path.read_bytes()
    if not raw or raw.endswith(b'\n'):
        return None
    keep = raw.rfind(b'\n') + 1
    side = path.with_name(f'{path.name}.torn_{uuid.uuid4().hex}')
    with side.open('xb') as fh:
        fh.write(raw[keep:])
        fh.flush()
        os.fsync(fh.fileno())
    with path.open('r+b') as fh:
        fh.truncate(keep)
        fh.flush()
        os.fsync(fh.fileno())
    _fsync_dir(path.parent)
    return side


def append(path: Path, record: Mapping) -> bytes:
    """Append one record as its canonical line under the write discipline. Returns the bytes written."""
    path = Path(path)
    line = canonical(record)
    if not line.endswith(b'\n') or line.count(b'\n') != 1:
        raise ValueError('a ledger line is one canonical line')
    path.parent.mkdir(parents=True, exist_ok=True)
    repair_torn_tail(path)
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise LedgerRefused(f'{path.name}: exists but is not a plain file')
    with path.open('ab') as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())
    _fsync_dir(path.parent)
    return line


def read_lines(path: Path) -> tuple[list[dict], bool]:
    """(records, torn) of a ledger whose every complete line must be exactly its record's canonical bytes."""
    rows, torn = OR.read_jsonl(path)
    if rows:
        raw = Path(path).read_bytes()
        complete = raw[:raw.rfind(b'\n') + 1]
        if b''.join(canonical(r) for r in rows) != complete:
            raise LedgerRefused(f'{Path(path).name}: a line is not the canonical bytes of its record (altered?)')
    return rows, torn


def chained(record: Mapping, previous_rows) -> dict:
    """`record` with the chain fields for appending after `previous_rows` (the verified lines already there)."""
    out = dict(record)
    out['line_number'] = len(previous_rows) + 1
    out['previous_line_digest'] = record_digest(previous_rows[-1]) if previous_rows else None
    return out


def verify_chain(rows, what: str = 'ledger') -> None:
    """Every line's number and previous-line digest must follow from the lines before it."""
    prev = None
    for i, r in enumerate(rows, start=1):
        if r.get('line_number') != i:
            raise LedgerRefused(f'{what}: line {i} does not carry its number (a line removed, added or reordered)')
        if r.get('previous_line_digest') != prev:
            raise LedgerRefused(f'{what}: line {i} does not name the digest of the line before it (the chain is broken)')
        prev = record_digest(r)


def extent(rows) -> dict:
    """The verified extent of a chained ledger: how many lines, and the digest of the last (None when empty). A later
    reader can check that this extent is still there, unchanged, at the same position (`extent_still_there`)."""
    return {'lines': len(rows), 'last_line_digest': record_digest(rows[-1]) if rows else None}


def extent_still_there(rows, ext: Mapping) -> bool:
    n = ext.get('lines')
    if type(n) is not int or n < 0 or n > len(rows):
        return False
    return ext.get('last_line_digest') == (record_digest(rows[n - 1]) if n else None)
