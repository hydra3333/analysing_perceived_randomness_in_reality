#!/usr/bin/env python3
"""OUTLANDISH_01 Q3 v0.4 shared Powerball/Oz matcher + streaming events.

This is a SYNTHETIC-TEST ENGINE SLICE, NOT a REAL/NULL entry point.
Its public function accepts explicit in-memory fixture draw records and a
packed file; no lottery history, G: paths, receipts or result roots are selected
or consulted here. Q4 must implement the published input/profile checks before
REAL use. The corresponding fixture-only test harness is the only supplied CLI.

The per-family effective-prefix cutoff is independent from file/chunk lookahead.
All physical source bytes are hashed once, even for an effective prefix scan.
Prefix scans still hash the WHOLE physical file for integrity. Streaming mode
writes events as discovered, in canonical order, without an all-events list.
Default is a fixed 4,000,000 packed-byte chunk; caller may override it.
"""
from __future__ import annotations

from collections import defaultdict, Counter
import csv
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
from typing import Iterable, Callable

import numpy as np

HEADER = ('draw_number', 'family', 'start_digit_offset', 'matched_digits')
FAMILY_LENGTHS = {'K7S': 16, 'K7': 14, 'K6S': 14, 'K7mix': 14, 'K6': 12}
GAME_FAMILIES = {'powerball': ('K7S', 'K7', 'K6S'), 'oz': ('K7', 'K7mix', 'K6')}
MAX_CHUNK_BYTES = 64_000_000

# Owner decision after Ryzen 4-vs-8 MB benchmark (15 Nov 2026):
# 4 MB always, even on 32 GiB systems. 8 MB remains a simple override.
DEFAULT_CHUNK_BYTES = 4_000_000
OPTIONAL_8MB_CHUNK_BYTES = 8_000_000


@dataclass(frozen=True)
class PBRecord:
    draw_number: int
    mains_drawn: tuple[int, ...]
    powerball: int


@dataclass(frozen=True)
class OzRecord:
    draw_number: int
    mains_drawn: tuple[int, ...]
    supplementaries_drawn: tuple[int, ...]


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


@dataclass(frozen=True)
class StreamScanResult:
    event_csv: Path
    event_sha256: str
    event_count: int
    family_counts: dict[str, int]
    effective_digits: int
    physical_digits: int
    sha256_full_packed: str
    bytes_hashed: int
    chunks: int
    chunk_bytes: int


def resolve_chunk_bytes(chunk_bytes: int | None = None) -> int:
    """Stable 4 MB default; caller may explicitly select any valid chunk size.

    No memory probe or hidden adaptive choice: parent scheduler controls workers.
    """
    chosen = DEFAULT_CHUNK_BYTES if chunk_bytes is None else chunk_bytes
    if type(chosen) is not int or not 1 <= chosen <= MAX_CHUNK_BYTES:
        raise ValueError('invalid byte chunk size')
    return chosen


class _HashingCsvTextSink:
    """csv.writer-compatible write method: SHA follows exact emitted UTF-8."""
    def __init__(self, destination):
        self.destination = destination
        self.digest = hashlib.sha256()

    def write(self, text: str) -> int:
        payload = text.encode('utf-8')
        self.destination.write(payload)
        self.digest.update(payload)
        return len(text)


def _stream_to_csv(path: Path, *, game: str, physical_digits: int,
                   effective_digits: int, draws, output_csv: Path,
                   chunk_bytes: int | None, expected_full_sha256: str | None,
                   ) -> StreamScanResult:
    """Fixture-stage create-only CSV; on failure unlink this new incomplete file.

    NO REAL or NULL profile selection, receipt provenance, or completion manifest.
    Q4 entry points must establish those invariants before production use.
    """
    resolved = resolve_chunk_bytes(chunk_bytes)
    output_csv = Path(output_csv).absolute()
    if not output_csv.parent.is_dir() or output_csv.parent.is_symlink():
        raise ValueError('ordinary pre-existing output directory required')
    if output_csv.exists() or output_csv.is_symlink():
        raise FileExistsError(f'create-only output already exists: {output_csv}')
    created = False
    try:
        with output_csv.open('xb') as handle:
            created = True
            sink = _HashingCsvTextSink(handle)
            writer = csv.writer(sink, lineterminator='\n')
            writer.writerow(HEADER)
            counts: Counter[str] = Counter()
            event_count = 0
            def emit(e: RawEvent) -> None:
                nonlocal event_count
                writer.writerow((e.draw_number, e.family, e.start_digit_offset,
                                 e.matched_digits))
                event_count += 1
                counts[e.family] += 1
            scan = _scan_core(path, game=game, physical_digits=physical_digits,
                              effective_digits=effective_digits, draws=draws,
                              chunk_bytes=resolved, expected_full_sha256=expected_full_sha256,
                              event_sink=emit)
            handle.flush()
            os.fsync(handle.fileno())
        return StreamScanResult(output_csv, sink.digest.hexdigest(), event_count,
                                dict(sorted(counts.items())), effective_digits,
                                physical_digits, scan.sha256_full_packed,
                                scan.bytes_hashed, scan.chunks, resolved)
    except BaseException:
        if created:
            output_csv.unlink(missing_ok=True)
        raise


def scan_packed_stream(path: Path, *, physical_digits: int, effective_digits: int,
                       draws: Iterable[PBRecord], output_csv: Path,
                       chunk_bytes: int | None = None,
                       expected_full_sha256: str | None = None) -> StreamScanResult:
    """Powerball fixture-stage streaming CSV, never a production REAL API."""
    return _stream_to_csv(path, game='powerball', physical_digits=physical_digits,
                          effective_digits=effective_digits, draws=draws,
                          output_csv=output_csv, chunk_bytes=chunk_bytes,
                          expected_full_sha256=expected_full_sha256)


def scan_packed_oz_stream(path: Path, *, physical_digits: int, effective_digits: int,
                          draws: Iterable[OzRecord], output_csv: Path,
                          chunk_bytes: int | None = None,
                          expected_full_sha256: str | None = None) -> StreamScanResult:
    """Oz Lotto fixture-stage streaming CSV, never a production REAL API."""
    return _stream_to_csv(path, game='oz', physical_digits=physical_digits,
                          effective_digits=effective_digits, draws=draws,
                          output_csv=output_csv, chunk_bytes=chunk_bytes,
                          expected_full_sha256=expected_full_sha256)


def _index_pb(draws: Iterable[PBRecord]):
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


def _index_oz(draws: Iterable[OzRecord]):
    """Independent per-family sorted keys; preserve all draw attributions.

    K7mix indexes each choice of six mains and one supplementary; the slot of
    the actual supplementary is NOT decided from the digit string here. The
    classifier subsequently uses the draw's distinct mains/supplementaries.
    """
    k7, k7mix, k6 = defaultdict(list), defaultdict(list), defaultdict(list)
    seen = set()
    draws = tuple(draws)
    if not draws:
        raise ValueError('empty fixture drawset')
    for d in draws:
        if not isinstance(d, OzRecord):
            raise ValueError('Oz draw must be OzRecord')
        if type(d.draw_number) is not int or d.draw_number <= 0 or d.draw_number in seen:
            raise ValueError('invalid or duplicate draw number')
        seen.add(d.draw_number)
        m, s = d.mains_drawn, d.supplementaries_drawn
        if (not isinstance(m, tuple) or len(m) != 7 or not isinstance(s, tuple)
                or len(s) != 3 or any(type(v) is not int or not 1 <= v <= 47
                                     for v in m+s) or len(set(m+s)) != 10):
            raise ValueError(f'wrong Oz draw roles/values: {d.draw_number}')
        k7[tuple(sorted(m))].append(d.draw_number)
        for omission in m:
            six = tuple(sorted(x for x in m if x != omission))
            k6[six].append(d.draw_number)
            for supplementary in s:
                k7mix[tuple(sorted((*six, supplementary)))].append(d.draw_number)
    return k7, k7mix, k6


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
                draws: Iterable[PBRecord], chunk_bytes: int | None = None,
                expected_full_sha256: str | None = None) -> ScanResult:
    """Backward-compatible Powerball wrapper for the shared read-only engine."""
    return _scan_core(path, game='powerball', physical_digits=physical_digits,
                      effective_digits=effective_digits, draws=draws,
                      chunk_bytes=resolve_chunk_bytes(chunk_bytes), expected_full_sha256=expected_full_sha256)


def scan_packed_oz(path: Path, *, physical_digits: int, effective_digits: int,
                   draws: Iterable[OzRecord], chunk_bytes: int | None = None,
                   expected_full_sha256: str | None = None) -> ScanResult:
    """Fixture-only Oz wrapper; no REAL drawset or output-root selection."""
    return _scan_core(path, game='oz', physical_digits=physical_digits,
                      effective_digits=effective_digits, draws=draws,
                      chunk_bytes=resolve_chunk_bytes(chunk_bytes), expected_full_sha256=expected_full_sha256)


def _scan_core(path: Path, *, game: str, physical_digits: int, effective_digits: int,
               draws: Iterable[PBRecord] | Iterable[OzRecord],
               chunk_bytes: int, expected_full_sha256: str | None,
               event_sink: Callable[[RawEvent], None] | None = None) -> ScanResult:
    """Shared read-once packed scanner, exact per-family effective-prefix bounds.

    Every *physical* byte is hashed once. Read-only lookahead supplies windows
    across byte-chunk boundaries, without creating another owner for a start.
    Never call this fixture-level API on real production inputs: Q4 must enforce
    receipt/drawset/profile/REAL-NULL output separation first.
    """
    if game not in GAME_FAMILIES:
        raise ValueError('invalid game')
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
    indexes = _index_pb(draws) if game == 'powerball' else _index_oz(draws)
    events: list[RawEvent] | None = [] if event_sink is None else None
    last_sort_key: tuple[int, str, int] | None = None
    def emit(e: RawEvent) -> None:
        nonlocal last_sort_key
        key = (e.start_digit_offset, e.family, e.draw_number)
        if last_sort_key is not None and key <= last_sort_key:
            raise ValueError('duplicate or unsorted raw event identity')
        if e.start_digit_offset + FAMILY_LENGTHS[e.family] > effective_digits:
            raise ValueError('internal family-specific effective-prefix EOF violation')
        last_sort_key = key
        if events is None:
            assert event_sink is not None
            event_sink(e)
        else:
            events.append(e)
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
            owned_starts = min(2 * span, max(0, effective_digits - own_digit_start))

            # Each family has its own end-bound. The lookup may READ beyond the
            # active prefix in a physical chunk but may not REPORT such hits.
            def valid_starts(length: int) -> int:
                return max(0, min(owned_starts,
                    effective_digits - own_digit_start - length + 1,
                    len(digits) - length + 1))

            limit12 = valid_starts(12) if game == 'oz' else 0
            limit14 = valid_starts(14)
            limit16 = valid_starts(16) if game == 'powerball' else 0
            core_len = limit14 if game == 'powerball' else limit12
            if not core_len:
                continue
            field_count = 7 if game == 'powerball' else 6
            fields = [digits[2*j:2*j+core_len].astype(np.uint16) * 10 +
                      digits[2*j+1:2*j+1+core_len]
                      for j in range(field_count)]
            upper = 35 if game == 'powerball' else 47
            six_ok = np.ones(core_len, dtype=np.bool_)
            for val in fields[:6]:
                six_ok &= (val >= 1) & (val <= upper)
            for i in range(6):
                for j in range(i+1, 6):
                    six_ok &= fields[i] != fields[j]

            if game == 'powerball':
                k7s, k7, k6s = indexes
                seventh = fields[6]
                mask6s = six_ok & (seventh >= 1) & (seventh <= 20)
                mask7 = six_ok & (seventh >= 1) & (seventh <= 35)
                for j in range(6):
                    mask7 &= seventh != fields[j]
                for vi in np.flatnonzero(mask6s | mask7):
                    rel = int(vi)
                    start = own_digit_start + rel
                    local_events: list[RawEvent] = []
                    six = tuple(int(f[rel]) for f in fields[:6])
                    seventh_val = int(seventh[rel])
                    if bool(mask6s[rel]):
                        for draw_num in k6s.get((tuple(sorted(six)), seventh_val), ()):
                            local_events.append(RawEvent(draw_num, 'K6S', start,
                                _fixed2_text(digits, rel, 14)))
                    if bool(mask7[rel]):
                        seven = (*six, seventh_val)
                        key7 = tuple(sorted(seven))
                        for draw_num in k7.get(key7, ()):
                            local_events.append(RawEvent(draw_num, 'K7', start,
                                _fixed2_text(digits, rel, 14)))
                        if rel < limit16:
                            pb = int(digits[rel+14]) * 10 + int(digits[rel+15])
                            if 1 <= pb <= 20:
                                for draw_num in k7s.get((key7, pb), ()):
                                    local_events.append(RawEvent(draw_num, 'K7S', start,
                                        _fixed2_text(digits, rel, 16)))
                    for ev in sorted(local_events, key=lambda e: (e.family,e.draw_number)):
                        emit(ev)
            else:
                k7, k7mix, k6 = indexes
                # K6 is eligible even where no complete seventh field exists.
                # Build the seventh field only for eligible 14-digit starts.
                for vi in np.flatnonzero(six_ok):
                    rel = int(vi)
                    start = own_digit_start + rel
                    local_events: list[RawEvent] = []
                    six = tuple(int(f[rel]) for f in fields[:6])
                    for draw_num in k6.get(tuple(sorted(six)), ()):
                        local_events.append(RawEvent(draw_num, 'K6', start,
                            _fixed2_text(digits, rel, 12)))
                    if rel >= limit14:
                        for ev in sorted(local_events, key=lambda e: (e.family,e.draw_number)):
                            emit(ev)
                        continue
                    seventh = int(digits[rel+12]) * 10 + int(digits[rel+13])
                    if not 1 <= seventh <= 47 or seventh in six:
                        for ev in sorted(local_events, key=lambda e: (e.family,e.draw_number)):
                            emit(ev)
                        continue
                    key7 = tuple(sorted((*six, seventh)))
                    for draw_num in k7.get(key7, ()):
                        local_events.append(RawEvent(draw_num, 'K7', start,
                            _fixed2_text(digits, rel, 14)))
                    for draw_num in k7mix.get(key7, ()):
                        local_events.append(RawEvent(draw_num, 'K7mix', start,
                            _fixed2_text(digits, rel, 14)))
                    for ev in sorted(local_events, key=lambda e: (e.family,e.draw_number)):
                        emit(ev)
    if path.stat().st_size != total_bytes:
        raise ValueError('input size changed during scan')
    if bytes_hashed != total_bytes:
        raise ValueError('full-byte hashing did not cover physical file')
    digest = sha.hexdigest()
    if expected_full_sha256 is not None and digest != expected_full_sha256:
        raise ValueError('full packed SHA-256 mismatch')
    return ScanResult(tuple(events) if events is not None else (), effective_digits, physical_digits,
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
