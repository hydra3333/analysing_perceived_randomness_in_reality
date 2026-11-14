#!/usr/bin/env python3
"""OUTLANDISH_01 Q3 initial matcher: Powerball FIXED2 packed BCD, read-only source.

This is a FIRST ENGINE SLICE, NOT a production REAL/NULL entry point.
Its public function accepts explicit in-memory fixture draw records and a
packed file; no lottery history, G: paths, receipts or result roots are selected
or consulted here. Q4 must implement the published input/profile checks before
REAL use. The corresponding fixture-only test harness is the only supplied CLI.

The per-family effective-prefix cutoff is independent from file/chunk lookahead.
All physical source bytes are hashed once, even for an effective prefix scan.
This is deliberate for correctness in the first slice (prefix runs still incur
whole-file I/O); performance/partial-scan policy can be reviewed later.
"""
from __future__ import annotations

from collections import defaultdict
import csv
from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Iterable

import numpy as np

HEADER = ('draw_number', 'family', 'start_digit_offset', 'matched_digits')
FAMILY_LENGTHS = {'K7S': 16, 'K7': 14, 'K6S': 14}
MAX_CHUNK_BYTES = 64_000_000


@dataclass(frozen=True)
class PBRecord:
    draw_number: int
    mains_drawn: tuple[int, ...]
    powerball: int


@dataclass(frozen=True)
class RawEvent:
    draw_number: int
    family: str
    start_digit_offset: int
    matched_digits: str


@dataclass(frozen=True)
class ScanResult:
    events: tuple[RawEvent, ...]
    effective_digits: int
    physical_digits: int
    sha256_full_packed: str
    bytes_hashed: int
    chunks: int


def _index(draws: Iterable[PBRecord]):
    """Independent canonical-key lookups: retain every matching attribution."""
    k7s, k7, k6s = defaultdict(list), defaultdict(list), defaultdict(list)
    seen = set()
    draws = tuple(draws)
    if not draws:
        raise ValueError('empty fixture drawset')
    for d in draws:
        if not isinstance(d, PBRecord):
            raise ValueError('Powerball draw must be PBRecord')
        if type(d.draw_number) is not int or d.draw_number <= 0 or d.draw_number in seen:
            raise ValueError('invalid or duplicate draw number')
        seen.add(d.draw_number)
        m = d.mains_drawn
        if (not isinstance(m, tuple) or len(m) != 7
                or any(type(x) is not int or not 1 <= x <= 35 for x in m)
                or len(set(m)) != 7 or type(d.powerball) is not int
                or not 1 <= d.powerball <= 20):
            raise ValueError(f'wrong Powerball draw roles/values: {d.draw_number}')
        key7 = tuple(sorted(m))
        k7s[(key7, d.powerball)].append(d.draw_number)
        k7[key7].append(d.draw_number)
        for omitted in m:
            six = tuple(sorted(x for x in m if x != omitted))
            k6s[(six, d.powerball)].append(d.draw_number)
    return k7s, k7, k6s


def _unpack_window(raw: bytes) -> np.ndarray:
    """Decode physical bytes with uint8 digits; validate BOTH nibbles."""
    buf = np.frombuffer(raw, dtype=np.uint8)
    high = buf >> 4
    low = buf & 15
    if bool(np.any(high > 9)) or bool(np.any(low > 9)):
        raise ValueError('nondecimal packed BCD nibble')
    digits = np.empty(buf.size * 2, dtype=np.uint8)
    digits[0::2] = high
    digits[1::2] = low
    return digits


def _fixed2_text(digits: np.ndarray, relative_start: int, length: int) -> str:
    # BYTE conversion (not numeric formatting) preserves the leading zero.
    return bytes(digits[relative_start:relative_start + length] + 48).decode('ascii')


def scan_packed(path: Path, *, physical_digits: int, effective_digits: int,
                draws: Iterable[PBRecord], chunk_bytes: int = 4_000_000,
                expected_full_sha256: str | None = None) -> ScanResult:
    """Read-only raw-event extraction for Powerball, ALL valid digit start offsets.

    No fixture flags or synthetic role restrictions are inferred from a filename:
    this is a low-level matcher, not a REAL input-selection/security boundary.
    Only the *separate* fixture-only test harness may invoke it for now.

    Chunk starts are byte-aligned; all starts in the owned byte span are visited
    exactly once. A read-only maximum 8-byte lookahead supplies up to 16 digits.
    Per-family eligible starts satisfy start + family_length <= effective_digits.
    The SHA is of the full PHYSICAL packed file, with each byte hashed exactly
    once (never hash the additional lookahead).
    """
    if type(physical_digits) is not int or physical_digits < 1:
        raise ValueError('invalid physical digit count')
    if (type(effective_digits) is not int or effective_digits < 1
            or effective_digits > physical_digits):
        raise ValueError('invalid effective digit count')
    if type(chunk_bytes) is not int or not 1 <= chunk_bytes <= MAX_CHUNK_BYTES:
        raise ValueError('invalid byte chunk size')
    if expected_full_sha256 is not None and (not isinstance(expected_full_sha256, str)
            or len(expected_full_sha256) != 64
            or any(ch not in '0123456789abcdef' for ch in expected_full_sha256)):
        raise ValueError('invalid required full-input SHA-256')
    path = Path(path).absolute()
    if not path.is_file() or path.is_symlink() or bool(getattr(path, 'is_junction', lambda: False)()):
        raise ValueError('source must be an ordinary regular packed file')
    total_bytes = (physical_digits + 1) // 2
    if path.stat().st_size != total_bytes:
        raise ValueError('packed physical digit count and file size disagree')
    k7s, k7, k6s = _index(draws)
    events = []
    sha = hashlib.sha256()
    bytes_hashed = chunks = 0

    with path.open('rb') as inp:
        for byte_start in range(0, total_bytes, chunk_bytes):
            span = min(chunk_bytes, total_bytes - byte_start)
            own_digit_start = 2 * byte_start
            inp.seek(byte_start)
            wanted = min(total_bytes - byte_start, span + 8)
            raw = inp.read(wanted)
            if len(raw) != wanted:
                raise ValueError('truncated packed stream during scan')
            sha.update(raw[:span])
            bytes_hashed += span
            chunks += 1
            if physical_digits & 1 and byte_start + wanted == total_bytes and raw[-1] & 15:
                raise ValueError('nonzero low-nibble padding for odd physical N')
            digits = _unpack_window(raw)

            # Independent limits. A 14-digit match may be legal where a
            # 16-digit match is not, even at the final chunk/physical EOF.
            owned_starts = min(2 * span, max(0, effective_digits - own_digit_start))
            limit14 = max(0, min(owned_starts,
                effective_digits - own_digit_start - 14 + 1,
                len(digits) - 14 + 1))
            limit16 = max(0, min(owned_starts,
                effective_digits - own_digit_start - 16 + 1,
                len(digits) - 16 + 1))
            if not limit14:
                continue
            fields = [digits[2*j:2*j+limit14].astype(np.uint16) * 10 +
                      digits[2*j+1:2*j+1+limit14]
                      for j in range(7)]
            six_ok = np.ones(limit14, dtype=np.bool_)
            for v in fields[:6]:
                six_ok &= (v >= 1) & (v <= 35)
            for i in range(6):
                for j in range(i + 1, 6):
                    six_ok &= fields[i] != fields[j]
            seventh = fields[6]
            # Both family lookups can be triggered at the same start, even
            # when K6S's PB equals a main and K7's final main is > 20.
            mask6s = six_ok & (seventh >= 1) & (seventh <= 20)
            mask7 = six_ok & (seventh >= 1) & (seventh <= 35)
            for j in range(6):
                mask7 &= seventh != fields[j]
            viable = np.flatnonzero(mask6s | mask7)
            # P1 needs a valid extra 2-digit PB field and is only eligible
            # for the independently bounded 16-digit starts.
            for vi in viable:
                rel = int(vi)
                start = own_digit_start + rel
                six = tuple(int(f[rel]) for f in fields[:6])
                seventh_value = int(seventh[rel])
                if bool(mask6s[rel]):
                    key = (tuple(sorted(six)), seventh_value)
                    for draw_num in k6s.get(key, ()):
                        events.append(RawEvent(draw_num, 'K6S', start,
                            _fixed2_text(digits, rel, 14)))
                if bool(mask7[rel]):
                    seven = (*six, seventh_value)
                    key7 = tuple(sorted(seven))
                    for draw_num in k7.get(key7, ()):
                        events.append(RawEvent(draw_num, 'K7', start,
                            _fixed2_text(digits, rel, 14)))
                    if rel < limit16:
                        powerball = int(digits[rel + 14]) * 10 + int(digits[rel + 15])
                        if 1 <= powerball <= 20:
                            for draw_num in k7s.get((key7, powerball), ()):
                                events.append(RawEvent(draw_num, 'K7S', start,
                                    _fixed2_text(digits, rel, 16)))
    if path.stat().st_size != total_bytes:
        raise ValueError('input size changed during scan')
    if bytes_hashed != total_bytes:
        raise ValueError('full-byte hashing did not cover physical file')
    digest = sha.hexdigest()
    if expected_full_sha256 is not None and digest != expected_full_sha256:
        raise ValueError('full packed SHA-256 mismatch')
    events.sort(key=lambda x: (x.start_digit_offset, x.family, x.draw_number))
    seen = set()
    for e in events:
        ident = (e.draw_number, e.family, e.start_digit_offset)
        if ident in seen:
            raise ValueError(f'duplicate raw event identity: {ident}')
        seen.add(ident)
        if e.start_digit_offset + FAMILY_LENGTHS[e.family] > effective_digits:
            raise ValueError('internal family-specific effective-prefix EOF violation')
    return ScanResult(tuple(events), effective_digits, physical_digits,
                      digest, bytes_hashed, chunks)


def write_fixture_events_create_only(path: Path, events: Iterable[RawEvent]) -> str:
    """Serialize precise ratified 4-column CSV into a NEW caller-owned TEST file.

    This helper is *not* a REAL writer: the fixture test harness owns the output
    path and confines it to its temporary directory. Q4 must introduce REAL/
    NULL source and output-root checks before any published use.
    """
    events = tuple(events)
    if list(events) != sorted(events, key=lambda x: (x.start_digit_offset,x.family,x.draw_number)):
        raise ValueError('events not sorted')
    identities = [(x.draw_number, x.family, x.start_digit_offset) for x in events]
    if len(set(identities)) != len(identities):
        raise ValueError('duplicate event identity')
    path = Path(path)
    with path.open('x', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(HEADER)
        for e in events:
            writer.writerow((e.draw_number, e.family, e.start_digit_offset, e.matched_digits))
    return hashlib.sha256(path.read_bytes()).hexdigest()
