#!/usr/bin/env python3
"""OUTLANDISH_01 Q2 — deliberately simple, independently written FIXED2 oracle.

No project matcher, packed-reader, index, classifier or current draw-data imports.
Only small synthetic test inputs; no REAL scans and no output files.
Use --self-test to exercise Powerball P1/P2/P3 and Oz Lotto O1/O2/O3
matching/classification plus format, offset, EOF and overlap invariants.
This is an initial Q2 oracle, NOT the full Q2 old-scanner qualification.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class PowerballDraw:
    number: int
    mains: tuple[int, ...]       # operator drawn order
    pb: int


@dataclass(frozen=True)
class OzDraw:
    number: int
    mains: tuple[int, ...]       # first seven in operator order
    supp: tuple[int, ...]        # following three, operator order


@dataclass(frozen=True, order=True)
class Hit:
    draw: int
    family: str
    start: int
    digits: str
    flags: tuple[str, ...] = ()


def fields(text: str) -> tuple[int, ...]:
    if len(text) % 2:
        raise ValueError('FIXED2 field sequence has odd length')
    return tuple(int(text[i:i+2]) for i in range(0, len(text), 2))


def six_is_drawn_subsequence(six: tuple[int, ...], seven: tuple[int, ...]) -> bool:
    return any(six == seven[:i] + seven[i+1:] for i in range(7))


def check_draws(game: str, draws: list[PowerballDraw | OzDraw]):
    if not draws or len(set(d.number for d in draws)) != len(draws):
        raise ValueError('missing/duplicate fixture draw IDs')
    for d in draws:
        if game == 'powerball':
            if not isinstance(d, PowerballDraw) or len(d.mains) != 7 or len(set(d.mains)) != 7:
                raise ValueError('bad Powerball fixture mains')
            if not all(1 <= b <= 35 for b in d.mains) or not 1 <= d.pb <= 20:
                raise ValueError('Powerball fixture ball out of range')
        elif game == 'oz':
            if not isinstance(d, OzDraw) or len(d.mains) != 7 or len(d.supp) != 3:
                raise ValueError('bad Oz fixture roles')
            if len(set(d.mains+d.supp)) != 10 or not all(1 <= b <= 47 for b in d.mains+d.supp):
                raise ValueError('Oz fixture barrel validity failure')
        else:
            raise ValueError('unknown game')


def oracle(game: str, digits: str, draws: list[PowerballDraw | OzDraw]) -> list[Hit]:
    """Reference: test every legal digit offset against every draw, literally.

    Permissible only for TINY fixtures. Deliberately NO family index, NumPy,
    chunking or optimised production helpers. Returns all raw families with
    independently derived narrow-order flags.
    """
    if any(c not in '0123456789' for c in digits):
        raise ValueError('non-decimal string')
    check_draws(game, draws)
    out = []
    lens = [('K7S', 16), ('K7', 14), ('K6S', 14)] if game == 'powerball' else [
        ('K7', 14), ('K7mix', 14), ('K6', 12)]
    for start in range(len(digits)):
        for family, length in lens:
            if start+length > len(digits):
                continue  # EACH family has its own EOF eligibility
            raw = digits[start:start+length]
            values = fields(raw)
            for d in draws:
                flags: tuple[str, ...] | None = None
                if game == 'powerball':
                    mains = d.mains
                    if family == 'K7S':
                        seven, special = values[:7], values[7]
                        if (len(set(seven)) == 7 and all(1 <= b <= 35 for b in seven)
                                and 1 <= special <= 20 and special == d.pb
                                and set(seven) == set(mains)):
                            flags = ('P1_any_order',) + (('P1_drawn_order',) if seven == mains else ('P1_reordered_only',))
                    elif family == 'K7':
                        seven = values
                        if (len(set(seven)) == 7 and all(1 <= b <= 35 for b in seven)
                                and set(seven) == set(mains)):
                            flags = ('P2_any_order',) + (('P2_drawn_order',) if seven == mains else ('P2_reordered_only',))
                    else:  # K6S
                        six, special = values[:6], values[6]
                        if (len(set(six)) == 6 and all(1 <= b <= 35 for b in six)
                                and 1 <= special <= 20 and special == d.pb
                                and set(six).issubset(set(mains))):
                            flags = ('P3_any_order',) + (( 'P3_drawn_subsequence_order',)
                                        if six_is_drawn_subsequence(six, mains) else ('P3_reordered_only',))
                else:
                    mains, supplementaries = d.mains, d.supp
                    if family == 'K7':
                        if len(set(values)) == 7 and set(values) == set(mains):
                            flags = ('O1_any_order',) + (('O1_drawn_order',) if values == mains else ('O1_reordered_only',))
                    elif family == 'K6':
                        if len(set(values)) == 6 and set(values).issubset(set(mains)):
                            flags = ('O3_any_order',) + (('O3_drawn_subsequence_order',)
                                        if six_is_drawn_subsequence(values,mains) else ('O3_reordered_only',))
                    else:  # K7mix
                        if len(set(values)) == 7 and all(1 <= b <= 47 for b in values):
                            selected_supp = [b for b in values if b in supplementaries]
                            selected_main = [b for b in values if b in mains]
                            if (len(selected_supp) == 1 and len(selected_main) == 6
                                    and set(selected_main).issubset(set(mains))):
                                slot = values.index(selected_supp[0])
                                flags_list = ['O2_any_slot', f'O2_supp_slot_{slot}']
                                if slot == 6:
                                    flags_list.append('O2_supplementary_last')
                                if slot == 6 and six_is_drawn_subsequence(tuple(values[:6]), mains):
                                    flags_list.append('O2_drawn_subsequence_order')
                                else:
                                    flags_list.append('O2_any_slot_non_drawn')
                                    if slot == 6:
                                        flags_list.append('O2_supplementary_last_reordered_only')
                                flags = tuple(flags_list)
                if flags is not None:
                    out.append(Hit(d.number, family, start, raw, flags))
    return sorted(out)


def pack_independent(digits: str) -> bytes:
    if not digits or any(c not in '0123456789' for c in digits):
        raise ValueError('not decimal')
    answer = bytearray()
    for i in range(0, len(digits), 2):
        high = ord(digits[i]) - 48
        low = ord(digits[i+1]) - 48 if i+1 < len(digits) else 0
        answer.append(high*16+low)
    return bytes(answer)


def unpack_independent(packed: bytes, logical_digits: int) -> str:
    if logical_digits < 0 or len(packed) != (logical_digits+1)//2:
        raise ValueError('packed size inconsistent with declared logical count')
    chars = []
    for byte in packed:
        hi = byte // 16
        lo = byte % 16
        if hi > 9 or lo > 9:
            raise ValueError('non-BCD nibble')
        chars.extend((str(hi), str(lo)))
    if logical_digits % 2 and packed[-1] % 16 != 0:
        raise ValueError('nonzero odd-length pad nibble')
    return ''.join(chars[:logical_digits])


def encoded(*numbers: int) -> str:
    return ''.join(f'{b:02d}' for b in numbers)


def plant(total: int, patches: list[tuple[int, str]]) -> str:
    data = ['9']*total
    occupied = set()
    for off, pat in patches:
        if off < 0 or off+len(pat) > total:
            raise ValueError('bad planted range')
        for i, ch in enumerate(pat,off):
            if i in occupied:
                raise ValueError('accidental planted overlap')
            occupied.add(i)
            data[i]=ch
    return ''.join(data)


def self_test() -> None:
    if not __debug__:
        raise RuntimeError('Q2 self-test requires ordinary Python (assertions enabled; no -O)')
    d1=PowerballDraw(1,(3,7,11,15,19,23,35),7) # PB = a main; seventh main >20
    d2=PowerballDraw(2,(1,5,9,13,17,21,25),4)
    d3=PowerballDraw(3,(2,4,6,8,10,12,14),18)
    d4=PowerballDraw(4,(5,9,13,17,21,25,29),1) # PB < all mains
    p1a=encoded(*d1.mains,d1.pb)
    p2b=encoded(*d2.mains)
    p3c=encoded(2,4,6,8,12,14,18)
    p1c=encoded(*d3.mains,d3.pb)
    p3_same_pb=encoded(3,7,11,15,19,23,7) # repeats a main in PB field
    source=plant(340,[(64,p1a),(109,p2b),(170,p3c),(230,p1c),(300,p3_same_pb)])
    hits=oracle('powerball',source,[d1,d2,d3,d4])
    ids={(x.draw,x.family,x.start) for x in hits}
    assert len(ids)==len(hits),'duplicate raw family attributions'
    expect = {(1,'K7S',64),(1,'K7',64),(1,'K6S',66),
              (2,'K7',109),(3,'K6S',170),
              (3,'K7S',230),(3,'K7',230),(3,'K6S',232),
              (1,'K6S',300)}
    assert expect.issubset(ids),('missing required planted/inclusion hits',sorted(expect-ids))
    assert (1,'K7',300) not in ids,'P2 incorrectly permitted duplicate seventh MAIN'
    assert any(x.draw==1 and x.family=='K6S' and x.start==300 for x in hits),'PB-repeat incorrectly rejected'
    assert any(x.draw==2 and x.family=='K7' and x.start==109 and 'P2_drawn_order' in x.flags for x in hits)
    assert any(x.draw==3 and x.family=='K6S' and x.start==170 and 'P3_drawn_subsequence_order' in x.flags for x in hits)
    # At exact final eligible P3 start, no 16-digit P1 is eligible there.
    eof=plant(57, [(57-len(p3c),p3c)])
    ends=oracle('powerball',eof,[d3])
    assert any(x.family=='K6S' and x.start==43 for x in ends)
    assert all(not (x.family=='K7S' and x.start>41) for x in ends)
    # At zero (even) and 1 (odd) digit offset, both start positions are examined.
    assert any(x.family=='K7S' and x.start==0 for x in oracle('powerball',p1a+'9'*18,[d1]))
    assert any(x.family=='K7S' and x.start==1 for x in oracle('powerball','9'+p1a+'9'*18,[d1]))
    # Correct odd count, zero final pad, leading-zero fields, corrupt nibbles.
    for original in ('012345678', source+'7', p1a):
        packed=pack_independent(original)
        assert unpack_independent(packed,len(original))==original
    try:
        unpack_independent(pack_independent('123')[:-1]+b'\x4a',3)
        raise AssertionError('bad nibble not rejected')
    except ValueError: pass
    try:
        unpack_independent(pack_independent('123')[:-1]+b'\x48',3)
        raise AssertionError('odd pad not rejected')
    except ValueError: pass
    try:
        unpack_independent(pack_independent('123'),5)
        raise AssertionError('wrong declared digit count not rejected')
    except ValueError: pass
    # Oz supports selected supplementary at ANY of seven positions,
    # not merely supplementary last; order/subsequence flags are distinct.
    o=OzDraw(7,(1,5,9,13,17,21,47),(2,4,6))
    o1=encoded(*o.mains)
    o2last=encoded(1,5,9,13,17,21,2)
    o2first=encoded(2,1,5,9,13,17,21)
    oz=plant(156,[(19,o1),(61,o2last),(109,o2first)])
    oh=oracle('oz',oz,[o])
    oi={(x.draw,x.family,x.start) for x in oh}
    assert {(7,'K7',19),(7,'K6',19),(7,'K6',21),
            (7,'K7mix',61),(7,'K6',61),
            (7,'K7mix',109),(7,'K6',111)}.issubset(oi),sorted(oi)
    assert any(x.family=='K7mix' and x.start==61 and 'O2_drawn_subsequence_order' in x.flags for x in oh)
    assert any(x.family=='K7mix' and x.start==109 and 'O2_supp_slot_0' in x.flags
               and 'O2_supplementary_last' not in x.flags for x in oh)
    assert not any(x.family=='K7mix' and x.start==109 and 'O2_drawn_subsequence_order' in x.flags for x in oh)
    for bad in (OzDraw(9,(1,5,9,13,17,21,47),(2,4,1)),):
        try: oracle('oz','9'*50,[bad]);raise AssertionError('Oz duplicate across roles not rejected')
        except ValueError: pass
    print('Q2 ORACLE SELF-TEST PASS: PB P1/P2/P3 and Oz O1/O2/O3, explicit planted')
    print('  even/odd/zero/EOF, PB equals main, main >20, supplementary slots,')
    print('  shifted same-draw implications, order/subsequence flags, BCD padding')
    print(f'  planted Powerball fixture produced {len(hits)} attributed raw events; Oz {len(oh)}')
    print('  NO REAL files, receipts, registry, scanned data or results modified.')


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test',action='store_true',required=True,
                   help='run small independent synthetic fixtures only')
    a=p.parse_args()
    if a.self_test:self_test()
    return 0


if __name__=='__main__':raise SystemExit(main())
