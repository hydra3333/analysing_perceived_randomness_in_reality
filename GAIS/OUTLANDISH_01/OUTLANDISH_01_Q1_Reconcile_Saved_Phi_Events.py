#!/usr/bin/env python3
"""OUTLANDISH_01 Q1: read-only saved-CSV comparison, NOT a digit scanner.

Compares legacy numeric-byte Powerball P1/P2/P3 matches with saved packed
scanner's P1/P2/P3 or v0.2 K6S (P3-any only) event records. No raw digit
binary opened, no new scan, no writes to scientific result directories.

See owner-ratified OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2
section B7 Q1. This utility is an implementation aid, not itself ratified.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

LENGTH = {'P1': 16, 'P2': 14, 'P3': 14}
EXPECTED_100M_DRAW_OFFSET = {
    (1244, 20_048_101), (1274, 71_806_090), (1373, 95_105_831)
}
PREFIXES = (100_000_000, 1_000_000_000)


class BadEvidence(ValueError):
    pass


@dataclass(frozen=True, order=True)
class Event:
    draw: int
    category: str
    offset: int
    digits: str

    @property
    def end(self) -> int:
        return self.offset + LENGTH[self.category]

    def dump(self):
        return [self.draw, self.category, self.offset, self.digits]


@dataclass
class Evidence:
    path: str
    sha256: str
    rows: int
    events: set[Event]
    available: frozenset[str]
    ignored_nonbaseline: int


def _category(row: dict[str, str]) -> str | None:
    if 'category' in row:
        val = row['category'].strip().upper()
        aliases = {'1': 'P1', '2': 'P2', '3': 'P3',
                   'P1': 'P1', 'P2': 'P2', 'P3': 'P3'}
        if val not in aliases:
            raise BadEvidence(f'unknown baseline category {val!r}')
        return aliases[val]
    fam = row['family'].strip()
    # Raw ratified v0.2 canonical families K7 and K7S are any-order;
    # they do not by themselves prove original P1/P2 drawn-order status.
    if fam == 'K6S':
        return 'P3'
    if fam in ('K7', 'K7S'):
        return None
    raise BadEvidence(f'unknown canonical family {fam!r}')


def parse_evidence(path: Path) -> Evidence:
    if not path.is_file():
        raise BadEvidence(f'not a regular file: {path}')
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    try:
        stream = io.StringIO(data.decode('utf-8-sig'), newline='')
        rdr = csv.DictReader(stream, strict=True)
        if not rdr.fieldnames or len(rdr.fieldnames) != len(set(rdr.fieldnames)):
            raise BadEvidence(f'absent or duplicate header: {path}')
        headers = set(rdr.fieldnames)
        for fields in (
            ('draw_number', 'category', 'start_digit_offset_0_based',
             'matched_decimal_digits'),
            ('draw_number', 'family', 'start_digit_offset', 'matched_digits'),
        ):
            if set(fields).issubset(headers):
                family_form = fields[1] == 'family'
                break
        else:
            raise BadEvidence(f'unsupported event schema {rdr.fieldnames}: {path}')
        events: set[Event] = set()
        seen: set[tuple[int, str, int]] = set()
        present = {'P3'} if family_form else {'P1', 'P2', 'P3'}
        ignored = 0
        count = 0
        for row in rdr:
            count += 1
            if None in row or None in row.values():
                raise BadEvidence(f'{path}:{count+1}: malformed CSV row')
            cat = _category(row)
            if cat is None:
                ignored += 1
                continue
            dtext = row['draw_number']
            stext = row['start_digit_offset' if family_form else 'start_digit_offset_0_based']
            digits = row['matched_digits' if family_form else 'matched_decimal_digits']
            if not dtext.isdecimal() or not stext.isdecimal():
                raise BadEvidence(f'{path}:{count+1}: non-integer draw/offset')
            draw = int(dtext)
            off = int(stext)
            if draw < 1 or not (0 <= off < 10_000_000_000):
                raise BadEvidence(f'{path}:{count+1}: draw/offset out of range')
            if (len(digits) != LENGTH[cat] or not digits.isascii() or
                    not digits.isdecimal()):
                raise BadEvidence(f'{path}:{count+1}: invalid FIXED2 digits: {digits!r}')
            ev = Event(draw, cat, off, digits)
            key = (draw, cat, off)
            if key in seen:
                raise BadEvidence(f'{path}:{count+1}: duplicate event identity {key}')
            seen.add(key)
            if not family_form and 'end_digit_offset_exclusive' in headers:
                t = row['end_digit_offset_exclusive']
                if not t.isdecimal() or int(t) != ev.end:
                    raise BadEvidence(f'{path}:{count+1}: end offset mismatch')
            events.add(ev)
    except (UnicodeDecodeError, csv.Error) as exc:
        raise BadEvidence(f'invalid UTF-8/CSV evidence: {path}: {exc}') from exc
    return Evidence(str(path), sha, count, events, frozenset(present), ignored)


def filtered(evidence: Evidence, prefix: int, category: str) -> set[Event]:
    # Per-family END eligibility: do not select a start merely < prefix.
    return {x for x in evidence.events if x.category == category and x.end <= prefix}


def compare(legacy: Evidence, packed: Evidence | None) -> dict:
    result = {
        'status': 'PARTIAL_NO_PACKED_CSV' if packed is None else 'PASS',
        'legacy': {'path': legacy.path, 'sha256': legacy.sha256,
                   'rows': legacy.rows, 'baseline_events': len(legacy.events)},
        'packed': (None if packed is None else {
            'path': packed.path, 'sha256': packed.sha256,
            'rows': packed.rows, 'baseline_events': len(packed.events),
            'ignored_nonbaseline_rows': packed.ignored_nonbaseline,
            'categories_comparable': sorted(packed.available),
        }),
        'comparisons': [],
    }
    first = filtered(legacy, 100_000_000, 'P3')
    actual = {(e.draw, e.offset) for e in first}
    known_ok = actual == EXPECTED_100M_DRAW_OFFSET
    result['known_100m_P3_draw_offset_check'] = {
        'status': 'PASS' if known_ok else 'FAIL',
        'legacy_count': len(first),
        'expected_count': len(EXPECTED_100M_DRAW_OFFSET),
        'missing': sorted([list(x) for x in EXPECTED_100M_DRAW_OFFSET - actual]),
        'extra': sorted([list(x) for x in actual - EXPECTED_100M_DRAW_OFFSET]),
    }
    if not known_ok:
        result['status'] = 'FAIL'
    for prefix in PREFIXES:
        for cat in ('P1', 'P2', 'P3'):
            left = filtered(legacy, prefix, cat)
            entry = {'prefix_logical_digits': prefix, 'category': cat,
                     'legacy_count': len(left)}
            if packed is None or cat not in packed.available:
                entry['status'] = 'NOT_COMPARED'
            else:
                right = filtered(packed, prefix, cat)
                missing = sorted(left - right)
                extra = sorted(right - left)
                entry.update({'status': 'PASS' if not missing and not extra else 'FAIL',
                              'packed_count': len(right),
                              'legacy_only_count': len(missing),
                              'packed_only_count': len(extra),
                              'legacy_only_first_10': [e.dump() for e in missing[:10]],
                              'packed_only_first_10': [e.dump() for e in extra[:10]]})
                if entry['status'] != 'PASS':
                    result['status'] = 'FAIL'
            result['comparisons'].append(entry)
    return result


def self_test():
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as td:
        a = Path(td) / 'old.csv'
        b = Path(td) / 'new.csv'
        header = ('constant_file,draw_number,category,start_digit_offset_0_based,'
                  'end_digit_offset_exclusive,matched_decimal_digits\n')
        old_rows = [
            'phi,1244,3,20048101,20048115,10112718012020',
            'phi,1274,3,71806090,71806104,32072715310907',
            'phi,1373,3,95105831,95105845,31232513152110',
            'phi,1169,3,999999990,1000000004,02110203040506',
        ]
        a.write_text(header + '\n'.join(old_rows) + '\n', encoding='utf-8')
        b.write_text('packed_file,draw_number,category,start_digit_offset_0_based,'
                     'end_digit_offset_exclusive,matched_decimal_digits\n' +
                     '\n'.join(old_rows) + '\n', encoding='utf-8')
        l, p = parse_evidence(a), parse_evidence(b)
        c = compare(l, p)
        assert c['status'] == 'PASS', c
        assert len(filtered(l, 1_000_000_000, 'P3')) == 3  # end not just start!
        assert len(filtered(l, 100_000_000, 'P3')) == 3
        b.write_text(b.read_text() + old_rows[0] + '\n')
        try:
            parse_evidence(b)
            raise AssertionError('duplicate event not rejected')
        except BadEvidence:
            pass
        b.write_text('draw_number,family,start_digit_offset,matched_digits\n'
                     '1244,K6S,20048101,10112718012020\n'
                     '1244,K7,20048101,10112718012020\n')
        p = parse_evidence(b)
        assert p.available == frozenset({'P3'}) and p.ignored_nonbaseline == 1
        assert filtered(p, 100_000_000, 'P3') == {Event(1244, 'P3', 20048101, '10112718012020')}
    print('SELF-TEST PASS: tuple equality, prefix END eligibility, duplicate refusal, K6S subset parsing')


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test', action='store_true')
    p.add_argument('--legacy-csv', type=Path, help='saved 1e9 numeric-byte phi matches.csv')
    p.add_argument('--packed-csv', type=Path, help='saved 1e10 packed phi matches.csv; do not rescan')
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.legacy_csv:
        p.error('--legacy-csv required except with --self-test')
    try:
        old = parse_evidence(args.legacy_csv)
        new = parse_evidence(args.packed_csv) if args.packed_csv else None
        result = compare(old, new)
    except (BadEvidence, OSError) as e:
        print('Q1 EVIDENCE ERROR:', e)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    print('Q1 STATUS:', result['status'])
    return 1 if result['status'] == 'FAIL' else 0


if __name__ == '__main__':
    raise SystemExit(main())
