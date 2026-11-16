#!/usr/bin/env python3
"""Minimal four-column shared Powerball/Oz event reader for Q4h.

The existing Q3 v0.4 scanner owns the writer. The reviewed Q3 classifier
owns semantic/ordering/duplicate checks. No REAL paths, source reads or CLI.
"""
from __future__ import annotations

import csv
import hashlib
import io

from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import PBRecord, OzRecord, RawEvent, classify_events

HEADER = ('draw_number', 'family', 'start_digit_offset', 'matched_digits')


def game_draws(checked_history, game: str):
    if checked_history.profile.game != game:
        raise ValueError('drawset/game mismatch')
    if game == 'powerball':
        return tuple(PBRecord(i, values[:7], values[7])
                     for i, values in checked_history.draw_rows)
    if game == 'oz':
        return tuple(OzRecord(i, values[:7], values[7:])
                     for i, values in checked_history.draw_rows)
    raise ValueError('unknown game')


def powerball_draws(checked_history):
    return game_draws(checked_history, 'powerball')


def read_and_classify(raw: bytes, *, recorded_sha256: str, history, digits: int,
                      game: str = 'powerball'):
    if not isinstance(raw, bytes) or hashlib.sha256(raw).hexdigest() != recorded_sha256:
        raise ValueError('raw event digest mismatch')
    if b'\x00' in raw:
        raise ValueError('NUL in event CSV')
    try:
        rows = csv.reader(io.StringIO(raw.decode('utf-8'), newline=''), strict=True)
        if tuple(next(rows, ())) != HEADER:
            raise ValueError('wrong four-column event header')
        events = []
        for cells in rows:
            if len(cells) != 4:
                raise ValueError('wrong event column count')
            d, family, start, matched = cells
            if any(not x.isascii() or not x.isdecimal() or str(int(x)) != x
                   for x in (d, start)):
                raise ValueError('noncanonical draw number or offset')
            events.append(RawEvent(int(d), family, int(start), matched))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('malformed event CSV') from exc
    cast = classify_events(game, events, game_draws(history, game),
                           effective_digits=digits)
    return tuple(events), cast
