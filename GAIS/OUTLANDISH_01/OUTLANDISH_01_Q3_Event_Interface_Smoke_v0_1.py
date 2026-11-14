#!/usr/bin/env python3
"""OUTLANDISH_01 Q3 event-interface smoke: stdlib, fixture-only, no file I/O.

A test aid for the ratified v0.2 event CSV interface and a future *proposed*
forecast view. This is not a production event reader, scanner, source selector,
forecast implementation, or formal Q3/Q4 qualification. No REAL data touched.
Run: python OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1.py --self-test
"""
from __future__ import annotations
import argparse
import csv
from dataclasses import dataclass
import hashlib
from io import StringIO

HEADER = ('draw_number', 'family', 'start_digit_offset', 'matched_digits')
FAMILIES = {
    'powerball': {'K7S': 16, 'K7': 14, 'K6S': 14},
    'oz': {'K7': 14, 'K7mix': 14, 'K6': 12},
}


@dataclass(frozen=True)
class Event:
    draw_number: int
    family: str
    start_digit_offset: int
    matched_digits: str


def encoded(events: list[Event]) -> bytes:
    """Production-style column order; values remain *literal strings*."""
    stream = StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(HEADER)
    for e in events:
        writer.writerow((e.draw_number, e.family, e.start_digit_offset,
                         e.matched_digits))
    return stream.getvalue().encode('utf-8')


def read_events(raw: bytes, *, game: str, logical_N: int, allowed_draws: set[int],
                recorded_sha256: str) -> list[Event]:
    """Strict *example* event loader, not an authorised REAL/NULL run reader."""
    if game not in FAMILIES:
        raise ValueError('unknown game')
    if type(logical_N) is not int or logical_N < 1:
        raise ValueError('invalid effective logical digit count')
    if not allowed_draws or any(type(x) is not int for x in allowed_draws):
        raise ValueError('invalid synthetic allowed-draw IDs')
    if hashlib.sha256(raw).hexdigest() != recorded_sha256:
        raise ValueError('raw event digest mismatch')
    if b'\x00' in raw:
        raise ValueError('NUL in event file')
    try:
        stream = StringIO(raw.decode('utf-8'), newline='')
    except UnicodeDecodeError as e:
        raise ValueError('event file not UTF-8') from e
    rows = csv.reader(stream, strict=True)
    if tuple(next(rows, ())) != HEADER:
        raise ValueError('wrong four-column event header')
    output: list[Event] = []
    seen: set[tuple[int, str, int]] = set()
    prior_key: tuple[int, str, int] | None = None
    for cells in rows:
        if len(cells) != 4:
            raise ValueError('wrong event column count')
        d, family, start, matched = cells
        if not d.isascii() or not d.isdecimal() or str(int(d)) != d:
            raise ValueError('noncanonical draw ID')
        if not start.isascii() or not start.isdecimal() or str(int(start)) != start:
            raise ValueError('noncanonical start offset')
        draw, offset = int(d), int(start)
        if draw not in allowed_draws:
            raise ValueError('draw not in allowed drawset')
        length = FAMILIES[game].get(family)
        if length is None:
            raise ValueError('family incompatible with game')
        if len(matched) != length or any(ch not in '0123456789' for ch in matched):
            raise ValueError('nondecimal or incorrect FIXED2 matched_digits')
        if offset + length > logical_N:
            raise ValueError('event end beyond effective logical prefix')
        identity = (draw, family, offset)
        if identity in seen:
            raise ValueError('duplicate event identity')
        seen.add(identity)
        ordering = (offset, family, draw)
        if prior_key is not None and ordering < prior_key:
            raise ValueError('out-of-order event')
        prior_key = ordering
        output.append(Event(draw, family, offset, matched))
    return output


def events_visible_at_origin(events: list[Event], origin_W: int) -> tuple[Event, ...]:
    """Only the permitted past. Full-table counts/ranks are NOT exposed."""
    if type(origin_W) is not int:
        raise ValueError('origin must be an integer draw ID')
    return tuple(e for e in events if e.draw_number <= origin_W)


def expect_refusal(label: str, raw: bytes, *, game: str = 'powerball',
                   N: int = 80, allowed: set[int] | None = None):
    digest = hashlib.sha256(raw).hexdigest()
    try:
        read_events(raw, game=game, logical_N=N,
                    allowed_draws={1, 2, 3} if allowed is None else allowed,
                    recorded_sha256=digest)
    except (ValueError, csv.Error):
        return
    raise AssertionError(f'negative canary was incorrectly accepted: {label}')


def self_test() -> None:
    # Fictional IDs 1..3 deliberately below real preholdout era; fixtures only.
    events = [
        Event(1, 'K7', 0, '01020304050607'),
        Event(2, 'K7', 0, '01020304050607'),  # legitimate second attribution
        Event(1, 'K7S', 0, '0102030405060708'),
        Event(1, 'K6S', 2, '02030405060708'),  # shifted window, odd/even starts legal
        Event(3, 'K6S', 41, '01020304050607'),
    ]
    data = encoded(events)
    digest = hashlib.sha256(data).hexdigest()
    loaded = read_events(data, game='powerball', logical_N=80,
                         allowed_draws={1, 2, 3}, recorded_sha256=digest)
    assert loaded == events, 'event tuple roundtrip failed'
    assert loaded[0].matched_digits.startswith('0'), 'leading zero lost'
    assert len([e for e in loaded if e.start_digit_offset == 0]) == 3

    past = events_visible_at_origin(loaded, 2)
    assert all(e.draw_number <= 2 for e in past) and len(past) == 4
    # Future-scramble canary: future-labeled events change, permitted view does not.
    changed = events[:-1] + [Event(3, 'K6S', 43, '09080706050403')]
    scrambled = read_events(encoded(changed), game='powerball', logical_N=80,
        allowed_draws={1, 2, 3}, recorded_sha256=hashlib.sha256(encoded(changed)).hexdigest())
    assert events_visible_at_origin(scrambled, 2) == past
    # Also ensure *adding* future events never changes past-view selection.
    changed2 = sorted(events + [Event(3, 'K7', 60, '01020304050607')],
                      key=lambda x: (x.start_digit_offset, x.family, x.draw_number))
    changed2_raw = encoded(changed2)
    changed2_read = read_events(changed2_raw, game='powerball', logical_N=80,
        allowed_draws={1, 2, 3}, recorded_sha256=hashlib.sha256(changed2_raw).hexdigest())
    assert events_visible_at_origin(changed2_read, 2) == past
    assert len(changed2_read) != len(loaded), 'global counts should NOT be exposed as past'

    # Strict digest is checked before interpreting any row.
    try:
        read_events(data, game='powerball', logical_N=80,
                    allowed_draws={1,2,3}, recorded_sha256='0'*64)
    except ValueError:
        pass
    else:
        raise AssertionError('changed event digest was accepted')

    expect_refusal('missing column', b'draw_number,family,start_digit_offset\n')
    expect_refusal('duplicate identity', encoded([events[0], events[0]]))
    expect_refusal('out-of-order', encoded([events[3], events[0]]))
    expect_refusal('unknown draw', encoded([Event(4, 'K7', 0, events[0].matched_digits)]))
    expect_refusal('wrong family', encoded([Event(1, 'K6', 0, '010203040506')]))
    expect_refusal('wrong length', encoded([Event(1, 'K7', 0, '010203')]))
    expect_refusal('non-ascii digit', encoded([Event(1, 'K7', 0, '０1020304050607')]))
    expect_refusal('effective EOF', encoded([Event(1, 'K7S', 70, events[2].matched_digits)]))
    expect_refusal('negative offset', b'draw_number,family,start_digit_offset,matched_digits\n1,K7,-1,01020304050607\n')
    # Oz has a separate family namespace and legal distinct 12-digit window.
    oz = [Event(7, 'K6', 0, '010203040506'), Event(7, 'K7mix', 2, '02030405060708')]
    oz_raw = encoded(oz)
    assert read_events(oz_raw, game='oz', logical_N=40,
                      allowed_draws={7}, recorded_sha256=hashlib.sha256(oz_raw).hexdigest()) == oz
    expect_refusal('PB family in Oz', encoded([Event(7, 'K6S', 0, '01020304050607')]),
                   game='oz', N=40, allowed={7})
    print('Q3 INTERFACE SMOKE PASS: exact four-column text events, provenance digest,')
    print('  family-specific lengths, sorted unique identities, multi-draw attribution,')
    print('  effective EOF, invalid-input refusals, and past-only origin view/future canary.')
    print('  FIXTURE-ONLY; no REAL drawsets, packed files, histories, results or registry read.')
    print('  NOT A Q3 ENGINE IMPLEMENTATION OR FORECAST APPROVAL.')


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test', action='store_true', required=True)
    p.parse_args()
    self_test()


if __name__ == '__main__':
    main()
