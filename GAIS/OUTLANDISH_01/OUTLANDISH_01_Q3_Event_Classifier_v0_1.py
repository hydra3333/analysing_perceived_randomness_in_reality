#!/usr/bin/env python3
"""OUTLANDISH_01 Q3 synthetic-stage event classifier and overlap summarizer.

No packed-input I/O, receipt/drawset reading, source selector or REAL/NULL CLI.
Classify already validated raw FIXED2 events against *explicit* draw records.
Raw events remain authoritative; multiple/nested classes do NOT create new rows.

Q4 must implement source-profile/manifest/hash gates before using this on REAL.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import heapq
from typing import Iterable

from OUTLANDISH_01_Q3_Packed_Matcher_v0_2 import (
    PBRecord, OzRecord, RawEvent, FAMILY_LENGTHS, GAME_FAMILIES,
)


@dataclass(frozen=True)
class Classified:
    event: RawEvent
    category: str                     # P1/P2/P3 or O1/O2/O3, not extra event row
    historical_pb_baseline: bool | None
    drawn_order: bool | None
    drawn_subsequence_order: bool | None
    reordered_only: bool | None
    selected_mains: tuple[int, ...]    # order as literally encoded in matched_digits
    omitted_main: int | None
    matched_powerball: int | None
    selected_supplementary: int | None
    supplementary_slot: int | None  # zero-based slot within seven matched fields
    supplementary_drawn_index: int | None  # 0..2 in actual Oz supplementary chronology
    supplementary_last: bool | None
    supplementary_last_reordered_only: bool | None
    any_slot_non_drawn: bool | None


@dataclass(frozen=True)
class OverlapSummary:
    events: int
    direct_same_draw_pairs: int
    same_start_pairs: int
    shifted_start_pairs: int
    family_pair_counts: dict[tuple[str, str], int]


def _validated_draws(game: str, draws: Iterable[PBRecord] | Iterable[OzRecord]):
    if game not in GAME_FAMILIES:
        raise ValueError('unknown game')
    lookup = {}
    for d in draws:
        if game == 'powerball':
            if not isinstance(d, PBRecord):
                raise ValueError('incorrect Powerball draw record class')
            mains, supp = d.mains_drawn, None
            if (type(d.powerball) is not int or not 1 <= d.powerball <= 20):
                raise ValueError('invalid PB special value')
            main_hi = 35
        else:
            if not isinstance(d, OzRecord):
                raise ValueError('incorrect Oz draw record class')
            mains, supp = d.mains_drawn, d.supplementaries_drawn
            main_hi = 47
            if (not isinstance(supp, tuple) or len(supp) != 3
                    or any(type(v) is not int or not 1 <= v <= 47 for v in supp)
                    or len(set(supp)) != 3):
                raise ValueError('invalid Oz supplementary record')
        if (type(d.draw_number) is not int or d.draw_number <= 0
                or d.draw_number in lookup):
            raise ValueError('invalid/duplicated draw identity')
        if (not isinstance(mains, tuple) or len(mains) != 7
                or any(type(v) is not int or not 1 <= v <= main_hi for v in mains)
                or len(set(mains)) != 7):
            raise ValueError('invalid seven-main draw record')
        if supp is not None and set(mains) & set(supp):
            raise ValueError('Oz main/supplementary overlap within one barrel')
        lookup[d.draw_number] = d
    if not lookup:
        raise ValueError('empty drawset')
    return lookup


def _ordered_six_subsequence(six: tuple[int, ...], seven: tuple[int, ...]) -> bool:
    return len(six) == 6 and any(six == seven[:j] + seven[j+1:] for j in range(7))


def _one(event: RawEvent, d: PBRecord | OzRecord, game: str) -> Classified:
    values = tuple(int(event.matched_digits[i:i+2]) for i in range(0, len(event.matched_digits), 2))
    m = d.mains_drawn
    mset = set(m)
    family = event.family
    cat = ''
    historical: bool | None = None
    ordered: bool | None = None
    subseq: bool | None = None
    reordered: bool | None = None
    omitted = None
    pb = None
    special = None
    special_slot = None
    special_chronology = None
    special_last = None
    special_last_reordered = None
    any_non_drawn = None

    if game == 'powerball':
        assert isinstance(d, PBRecord)
        if family == 'K7S':
            selected, pb = values[:7], values[7]
            cat = 'P1'
            if len(set(selected)) != 7 or set(selected) != mset or pb != d.powerball:
                raise ValueError('K7S event fails Powerball draw attribution')
            ordered = selected == m
            historical = ordered
            reordered = not ordered
        elif family == 'K7':
            selected = values
            cat = 'P2'
            if len(set(selected)) != 7 or set(selected) != mset:
                raise ValueError('K7 event fails Powerball draw attribution')
            ordered = selected == m
            historical = ordered
            reordered = not ordered
        elif family == 'K6S':
            selected, pb = values[:6], values[6]
            cat = 'P3'
            if (len(set(selected)) != 6 or not set(selected) <= mset
                    or pb != d.powerball):
                raise ValueError('K6S event fails Powerball draw attribution')
            omitted = next(v for v in m if v not in selected)
            subseq = _ordered_six_subsequence(selected, m)
            historical = True  # original P3 = any six mains plus actual PB
            reordered = not subseq
        else:
            raise ValueError('Powerball event family unsupported')
    else:
        assert isinstance(d, OzRecord)
        supp_set = set(d.supplementaries_drawn)
        if family == 'K7':
            cat = 'O1'
            selected = values
            if len(set(selected)) != 7 or set(selected) != mset:
                raise ValueError('Oz K7 event fails actual main draw')
            ordered = selected == m
            reordered = not ordered
        elif family == 'K6':
            cat = 'O3'
            selected = values
            if len(set(selected)) != 6 or not set(selected) <= mset:
                raise ValueError('Oz K6 event fails six-main draw subset')
            omitted = next(v for v in m if v not in selected)
            subseq = _ordered_six_subsequence(selected, m)
            reordered = not subseq
        elif family == 'K7mix':
            cat = 'O2'
            if len(set(values)) != 7:
                raise ValueError('Oz K7mix duplicate matched values')
            special_slots = [i for i, v in enumerate(values) if v in supp_set]
            if len(special_slots) != 1:
                raise ValueError('Oz K7mix expected precisely one supplementary')
            special_slot = special_slots[0]
            special = values[special_slot]
            selected = values[:special_slot] + values[special_slot+1:]
            if len(selected) != 6 or not set(selected) <= mset:
                raise ValueError('Oz K7mix must contain six drawn mains')
            omitted = next(v for v in m if v not in selected)
            special_chronology = d.supplementaries_drawn.index(special)
            special_last = special_slot == 6
            subseq = special_last and _ordered_six_subsequence(selected, m)
            special_last_reordered = special_last and not subseq
            any_non_drawn = not subseq
        else:
            raise ValueError('Oz event family unsupported')

    return Classified(event, cat, historical, ordered, subseq, reordered,
                      tuple(selected), omitted, pb, special, special_slot,
                      special_chronology, special_last, special_last_reordered,
                      any_non_drawn)


def classify_events(game: str, events: Iterable[RawEvent],
                    draws: Iterable[PBRecord] | Iterable[OzRecord],
                    *, effective_digits: int) -> tuple[Classified, ...]:
    """Pure/replayable attribution, not an authorisation to read REAL inputs.

    Validate exact event order, identity, text and effective-N bounds, then
    independently verify each event against its actual draw. No packed reread.
    """
    draw_lookup = _validated_draws(game, draws)
    if type(effective_digits) is not int or effective_digits < 1:
        raise ValueError('invalid effective digit count')
    result = []
    seen = set()
    prior_order = None
    for e in events:
        if not isinstance(e, RawEvent):
            raise ValueError('event not a RawEvent')
        if type(e.draw_number) is not int or e.draw_number not in draw_lookup:
            raise ValueError('event draw absent from fixture drawset')
        if e.family not in GAME_FAMILIES[game]:
            raise ValueError('event family unsupported for game')
        L = FAMILY_LENGTHS[e.family]
        if (not isinstance(e.matched_digits, str) or len(e.matched_digits) != L
                or not e.matched_digits.isascii() or not e.matched_digits.isdecimal()):
            raise ValueError('event matched_digits must be exact FIXED2 ASCII text')
        if (type(e.start_digit_offset) is not int or e.start_digit_offset < 0
                or e.start_digit_offset + L > effective_digits):
            raise ValueError('event outside effective prefix')
        identity = (e.draw_number, e.family, e.start_digit_offset)
        if identity in seen:
            raise ValueError('duplicate event identity')
        seen.add(identity)
        order = (e.start_digit_offset, e.family, e.draw_number)
        if prior_order is not None and order < prior_order:
            raise ValueError('event input out of required order')
        prior_order = order
        result.append(_one(e, draw_lookup[e.draw_number], game))
    return tuple(result)


def summarize_same_draw_overlaps(events: Iterable[RawEvent], *, game: str) -> OverlapSummary:
    """Count *direct* physical interval intersections, by draw, in a sweep.

    [start,end) with family length. Excludes different-draw pairs; no physical
    event is discarded, no pair-list allocation, not a connected-component count.
    Typical complexity O(E log E + E * number_of_active_families).
    """
    if game not in GAME_FAMILIES:
        raise ValueError('unknown game')
    by_draw: dict[int, list[RawEvent]] = defaultdict(list)
    total_events = 0
    for e in events:
        if not isinstance(e, RawEvent) or e.family not in GAME_FAMILIES[game]:
            raise ValueError('bad event or game family for overlap calculation')
        if type(e.draw_number) is not int or type(e.start_digit_offset) is not int or e.start_digit_offset < 0:
            raise ValueError('invalid physical event identity')
        by_draw[e.draw_number].append(e)
        total_events += 1
    count_pairs = same_start_pairs = 0
    pair_counts: Counter[tuple[str, str]] = Counter()
    for rows in by_draw.values():
        rows.sort(key=lambda e: (e.start_digit_offset,e.family))
        heap: list[tuple[int,int,str,int]] = []
        active_families: Counter[str] = Counter()
        active_by_start: Counter[tuple[int,str]] = Counter()
        seq = 0
        for e in rows:
            s = e.start_digit_offset
            while heap and heap[0][0] <= s:
                _,_,f,oldstart = heapq.heappop(heap)
                active_families[f] -= 1
                if active_families[f] == 0: del active_families[f]
                active_by_start[oldstart,f] -= 1
                if active_by_start[oldstart,f] == 0: del active_by_start[oldstart,f]
            for f,n in active_families.items():
                pair_counts[tuple(sorted((f,e.family)))] += n
                count_pairs += n
                same_start_pairs += active_by_start[s,f]
            heapq.heappush(heap,(s+FAMILY_LENGTHS[e.family],seq,e.family,s))
            seq += 1
            active_families[e.family] += 1
            active_by_start[s,e.family] += 1
    return OverlapSummary(total_events, count_pairs, same_start_pairs,
                          count_pairs-same_start_pairs, dict(sorted(pair_counts.items())))
