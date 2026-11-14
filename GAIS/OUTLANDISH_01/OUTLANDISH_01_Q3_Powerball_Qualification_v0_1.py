#!/usr/bin/env python3
"""Fixture-only qualification of new Q3 packed Powerball engine vs Q2 oracle.

Run (Windows project .venv, repository root):
    ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\OUTLANDISH_01_Q3_Powerball_Qualification_v0_1.py" --run

No REAL drawset, published binary, G: result root, registry or source receipt is
opened. All tiny input/output files are generated under TemporaryDirectory.
This does NOT approve Q3 or production/Q5; it qualifies just this first slice.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import random
import tempfile

from OUTLANDISH_01_Q2_Independent_Oracle_v0_1 import (
    PowerballDraw, oracle, encoded, pack_independent, plant,
)
from OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1 import (
    DRAWS, D1, D2, D3, scenario_set, expected_rows,
)
from OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1 import (
    read_events, Event as InterfaceEvent,
)
from OUTLANDISH_01_Q3_Packed_Matcher_v0_1 import (
    PBRecord, RawEvent, scan_packed, write_fixture_events_create_only,
)


def pb_fixture_records(draws):
    return [PBRecord(d.number, d.mains, d.pb) for d in draws]


def expected_all(digits: str, draws) -> set[tuple[int, str, int, str]]:
    expected = {(h.draw, h.family, h.start, h.digits) for h in oracle('powerball', digits, draws)}
    if len(expected) != len(oracle('powerball', digits, draws)):
        raise AssertionError('independent reference emitted duplicate identities')
    return expected


def as_tuples(events) -> set[tuple[int, str, int, str]]:
    out = {(e.draw_number, e.family, e.start_digit_offset, e.matched_digits) for e in events}
    if len(out) != len(events):
        raise AssertionError('engine emitted duplicate identities')
    return out


def check_case(label: str, digits: str, draws, effective_N: int,
               root: Path, chunk_choices=(1, 3, 7, 16, 32, 64, 256),
               expected_baseline: set | None = None) -> int:
    if not 1 <= len(digits) <= 3000 or not 1 <= effective_N <= len(digits):
        raise ValueError('fixture out of bounds')
    file = root / (label + '.SYNTHETIC_TEST_ONLY.packed.bin')
    blob = pack_independent(digits)
    file.write_bytes(blob)
    digest = hashlib.sha256(blob).hexdigest()
    all_expected = expected_all(digits[:effective_N], draws)
    reference = pb_fixture_records(draws)
    checked = 0
    for chunk in chunk_choices:
        result = scan_packed(file, physical_digits=len(digits),
            effective_digits=effective_N, draws=reference, chunk_bytes=chunk,
            expected_full_sha256=digest)
        actual = as_tuples(result.events)
        if actual != all_expected:
            raise AssertionError(f'{label} chunk_bytes={chunk}: '
                f'missing={sorted(all_expected-actual)[:6]} extra={sorted(actual-all_expected)[:6]}')
        if result.bytes_hashed != len(blob) or result.sha256_full_packed != digest:
            raise AssertionError(f'{label} chunk_bytes={chunk}: physical byte hashing mismatch')
        # Output CSV is create-only, exact four-column schema, strict-read back.
        out = root / (label + f'.chunk{chunk}.raw_events.csv')
        csv_digest = write_fixture_events_create_only(out, result.events)
        loaded = read_events(out.read_bytes(), game='powerball', logical_N=effective_N,
            allowed_draws={d.number for d in draws}, recorded_sha256=csv_digest)
        if set((e.draw_number,e.family,e.start_digit_offset,e.matched_digits) for e in loaded) != actual:
            raise AssertionError(f'{label} chunk_bytes={chunk}: event CSV roundtrip mismatch')
        try:
            write_fixture_events_create_only(out, result.events)
        except FileExistsError:
            pass
        else:
            raise AssertionError('create-only event writer overwrote prior file')
        checked += 1
        if expected_baseline is not None:
            by_id = {d.number: d for d in draws}
            baseline = set()
            for e in result.events:
                d = by_id[e.draw_number]
                if e.family == 'K7S' and e.matched_digits == encoded(*d.mains,d.pb):
                    cat = 'P1'
                elif e.family == 'K7' and e.matched_digits == encoded(*d.mains):
                    cat = 'P2'
                elif e.family == 'K6S':
                    cat = 'P3'
                else:
                    continue
                baseline.add((e.draw_number,cat,e.start_digit_offset,e.matched_digits))
            if baseline != expected_baseline:
                raise AssertionError(f'{label}: legacy baseline P1/P2/P3 subset mismatch')
    print(f'PASS: {label}: {len(all_expected)} exact independent oracle events, '
          f'{checked} chunk sizes, full-byte SHA, strict CSV roundtrip')
    return checked


def expect_error(label, thunk, substring: str):
    try:
        thunk()
    except (ValueError, FileExistsError) as exc:
        if substring not in str(exc):
            raise AssertionError(f'{label}: wrong refusal: {exc}') from exc
    else:
        raise AssertionError(f'{label}: expected refusal absent')
    print(f'PASS: negative_{label}: deliberate error refused')


def self_test() -> None:
    oracle_file = Path(__file__).resolve().parent / 'OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py'
    src = oracle_file.read_bytes().replace(b'\r\n', b'\n')
    sha1 = hashlib.sha1(f'blob {len(src)}\0'.encode() + src).hexdigest()
    if sha1 != '6ea5562ed681c854f8c552e9600af5d8f9d3be00':
        raise ValueError('Independent Q2 oracle has changed; refuse comparison')
    if __debug__ is False:
        raise RuntimeError('run without Python -O')
    scenarios = scenario_set()
    if len(scenarios) < 6:
        raise RuntimeError('Q2 fixtures missing')
    # The exact old regression: 341 physical digits, only first 332 eligible.
    pref = next(s for s in scenarios if s.name == 'PREFIX_END_EOF_ELIGIBILITY')
    assert len(pref.digits) == 341 and pref.prefix_digits == 332
    assert len(expected_rows(pref)) == 12
    assert len(expected_rows(next(s for s in scenarios
          if s.name == 'chunk_crossings_duplicate_keys_odd_N'))) == 16
    print('Q3 PB SELF-TEST PASS: pinned Q2 oracle/fixtures, known 341-to-332 '
          'prefix regression, no files created or REAL inputs accessed')


def run_all() -> int:
    self_test()
    suite_count = chunk_count = 0
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q3_PB_SYNTHETIC_ONLY_') as td:
        root = Path(td)
        for s in scenario_set():
            name = 'q2_' + s.name
            n = s.prefix_digits if s.prefix_digits is not None else len(s.digits)
            chunk_count += check_case(name, s.digits, DRAWS, n, root,
                                      expected_baseline=expected_rows(s))
            suite_count += 1
        # Explicit per-family last-valid-start, and both nibble phases at 0/1.
        fixture_cases = [
            ('zero_start_P1', plant(57, [(0, encoded(*D1.mains, D1.pb))]), [D1], 57),
            ('odd_start_P1', plant(57, [(1, encoded(*D1.mains, D1.pb))]), [D1], 57),
            ('last_valid_P1', plant(57, [(41, encoded(*D1.mains,D1.pb))]), [D1], 57),
            ('last_valid_P2', plant(57, [(43, encoded(*D2.mains))]), [D2], 57),
            ('last_valid_P3', plant(57, [(43, encoded(2,4,6,8,12,14,18))]), [D3], 57),
            ('P1_outside_prefix', plant(57, [(41, encoded(*D1.mains,D1.pb))]), [D1], 55),
        ]
        for name, digits, draws, n in fixture_cases:
            chunk_count += check_case(name, digits, draws, n, root)
            suite_count += 1
        # Seeded synthetic corruption/noise with explicit source offsets.
        # Never use saved REAL drawsets in this qualification stage.
        rng = random.Random(20261114)
        patterns = [encoded(*D1.mains,D1.pb), encoded(*D2.mains),
                    encoded(2,4,6,8,12,14,18)]
        for j in range(10):
            n = 189 + j*37
            data = [str(rng.randrange(10)) for _ in range(n)]
            start = 30 + (j * 17) % 65
            pat = patterns[j % 3]
            data[start:start+len(pat)] = pat
            effective = n - (j % 5)
            chunk_count += check_case(f'seeded_{j:02d}', ''.join(data), DRAWS,
                                      effective, root, chunk_choices=(3,17,64))
            suite_count += 1
        # Negative cases — corruption, size, digest, pad, draw validity.
        good_digits = plant(101, [(45, encoded(*D1.mains,D1.pb))])
        good = root / 'negative_good.SYNTHETIC_TEST_ONLY.packed.bin'
        good_blob = pack_independent(good_digits)
        good.write_bytes(good_blob)
        args = dict(physical_digits=101, effective_digits=101,
                    draws=pb_fixture_records([D1]), chunk_bytes=7)
        corrupt = root / 'negative_corrupt.SYNTHETIC_TEST_ONLY.packed.bin'
        bad_blob = bytearray(good_blob); bad_blob[20] = 0xBA
        corrupt.write_bytes(bad_blob)
        expect_error('bad_BCD', lambda: scan_packed(corrupt,**args), 'nondecimal packed BCD')
        pad = root / 'negative_pad.SYNTHETIC_TEST_ONLY.packed.bin'
        bad_blob = bytearray(good_blob);bad_blob[-1] |= 0x07
        pad.write_bytes(bad_blob)
        expect_error('nonzero_pad',lambda:scan_packed(pad,**args), 'padding')
        truncated = root / 'negative_truncated.SYNTHETIC_TEST_ONLY.packed.bin'
        truncated.write_bytes(good_blob[:-1])
        expect_error('truncated_file',lambda:scan_packed(truncated,**args), 'size disagree')
        expect_error('bad_sha',lambda:scan_packed(good,**args,
            expected_full_sha256='0'*64), 'SHA-256 mismatch')
        expect_error('effective_N_larger',lambda:scan_packed(good,**(args | {'effective_digits':102})),
            'effective digit count')
        expect_error('duplicate_draw_id',lambda:scan_packed(good,**(args | {
            'draws':pb_fixture_records([D1,D1])})), 'duplicate draw')
        expect_error('PB_out_of_range',lambda:scan_packed(good,**(args | {
            'draws':[PBRecord(1,D1.mains,35)]})),
            'wrong Powerball draw')
    print(f'Q3 POWERBALL SLICE PASS: fixtures={suite_count} chunk-configurations={chunk_count} '
          'negative-refusals=7; exact independent-oracle tuple equality, '
          'effective-prefix EOF regression FIXED in new engine, source SHA and '
          'create-only event CSV; synthetic-only, no REAL scan or Q5 approval')
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--self-test', action='store_true')
    g.add_argument('--run', action='store_true')
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    return run_all()


if __name__ == '__main__':
    raise SystemExit(main())
