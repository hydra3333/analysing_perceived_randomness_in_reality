#!/usr/bin/env python3
"""OUTLANDISH_01 Stage A: independent, single-threaded Powerball digit search.

Uses only an owner-prepared, pre-holdout CSV. Never imports project code,
contacts lottery sites, or opens a master unless explicitly invoked with `prepare`.
Input constant files: one *decimal digit* per unsigned byte, numeric value 0..9.
Current ball format: FIXED2, e.g. ball 3 -> digit bytes [0,3]; 12 -> [1,2].
"""
from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import os
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from itertools import combinations
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

try:
    import numpy as np
except ImportError as exc:
    raise SystemExit("NumPy is required. In your project .venv: python -m pip install numpy") from exc

CUTOFF = 1577          # Restricted: this draw and everything after it.
EXPECTED_HEADER = ('Draw_Number', 'Date', *(f'Drawn_{i}' for i in range(1, 8)), 'Powerball')
DEFAULT_DRAWS = 'POWERBALL_preholdout_only.csv'
DEFAULT_DIGITS = ('digits_pi_10_to_6.bin', 'digits_golden_ratio_10_to_6.bin')
P1, P2, P3 = 1, 2, 3
PATTERN_DIGITS = {P1: 16, P2: 14, P3: 14}
FORMAT = 'FIXED2: every ball is exactly two decimal digits (03, 12, ...); each digit = one byte 0..9'
KNOWN_PREFIXES = {
    'digits_pi_': '31415926535897932384626433832795',
    'digits_golden_ratio_': '16180339887498948482045868343656',
    'digits_e_': '27182818284590452353602874713526',
    'digits_log2_': '06931471805599453094172321214581',
    'digits_gamma_': '05772156649015328606065120900824',
    'digits_lemniscate_': '26220575542921198104648395898911',
}


@dataclass(frozen=True)
class Draw:
    number: int
    drawn: tuple[int, int, int, int, int, int, int]
    powerball: int


def digit_bytes_for_ball(n: int, encoding: str = 'fixed2') -> bytes:
    """Central representation adapter. Natural-width support needs a different scanner."""
    if encoding == 'fixed2':
        return bytes((n // 10, n % 10))
    if encoding == 'natural':
        return bytes((n,)) if n < 10 else bytes((n // 10, n % 10))
    raise ValueError(f'unknown ball encoding {encoding!r}')


def encode_balls(numbers, encoding: str = 'fixed2') -> bytes:
    return b''.join(digit_bytes_for_ball(n, encoding) for n in numbers)


def display_pattern(values: bytes) -> str:
    return ''.join(chr(48 + x) for x in values)


def safe_header(row) -> bool:
    return tuple(row) == EXPECTED_HEADER


def prepare_preholdout(source: Path, destination: Path) -> None:
    """Owner-only explicit command. Do not read any restricted outcome field.

    Source rows are ordered by draw number (as the project master requires).
    At first draw >= CUTOFF, read ONLY its leading Draw_Number, then stop.
    Output is independent of the authoritative project data and is not committed.
    """
    if source.resolve() == destination.resolve():
        raise ValueError('source and destination must differ')
    if source.is_symlink() or not source.is_file():
        raise ValueError('source must be an existing ordinary file, not a symlink')
    if destination.exists():
        raise FileExistsError(f'refusing to overwrite existing draw copy: {destination}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    count = first = last = None
    try:
        with source.open('rb') as src, NamedTemporaryFile('wb', delete=False, dir=destination.parent,
                                                          prefix='.preholdout_', suffix='.tmp') as dst:
            temp_path = Path(dst.name)
            header = src.readline()
            if header.rstrip(b'\r\n').decode('utf-8-sig') != ','.join(EXPECTED_HEADER):
                raise ValueError('source header differs from verified project CSV schema')
            dst.write(header)
            count = 0
            while True:
                beginning = src.tell()
                # Peek only at Draw_Number, stopping before the next field.
                num = bytearray()
                while True:
                    c = src.read(1)
                    if not c:
                        if num:
                            raise ValueError('truncated source row')
                        break
                    if c == b',':
                        break
                    if len(num) >= 9 or not (48 <= c[0] <= 57):
                        raise ValueError('noncanonical draw-number field in master')
                    num.extend(c)
                if not c:
                    break
                draw_no = int(num)
                if draw_no >= CUTOFF:
                    # Deliberately NEVER read the restricted number/date fields.
                    break
                if last is not None and draw_no != last + 1:
                    raise ValueError('nonconsecutive or unordered source draw numbers')
                if first is None:
                    first = draw_no
                last = draw_no
                src.seek(beginning)
                whole_line = src.readline()  # Only an eligible, pre-holdout row.
                if not whole_line.endswith((b'\r', b'\n')):
                    # Last line without newline is also valid, but never combine lines.
                    pass
                dst.write(whole_line)
                count += 1
            if not count:
                raise ValueError('no eligible pre-holdout draws in source')
        # CSV validation happens only against eligible, newly prepared copy.
        parsed = load_draws(temp_path)
        if len(parsed) != count:
            raise ValueError('extracted draw count does not validate')
        os.replace(temp_path, destination)
        temp_path = None
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
    print(f'PREPARED {destination}: {count:,} eligible draws, {first}..{last}; cutoff < {CUTOFF}')
    print('Only pre-holdout rows were copied. No held-out winning-number fields were read.')


def load_draws(path: Path) -> list[Draw]:
    """Read only a development-only, canonical CSV; refuse restricted rows
    *before* decoding their outcome fields, even when given the wrong file.
    """
    if not path.is_file() or path.is_symlink():
        raise ValueError('draw CSV is missing or is a symlink')
    draws: list[Draw] = []
    with path.open('rb') as inp:
        header = inp.readline().rstrip(b'\r\n').decode('utf-8-sig')
        if header != ','.join(EXPECTED_HEADER):
            raise ValueError(f'draw header must be exactly: {",".join(EXPECTED_HEADER)}')
        while True:
            beginning = inp.tell()
            prefix = bytearray()
            while True:
                ch = inp.read(1)
                if not ch:
                    if prefix:
                        raise ValueError('truncated Draw_Number field')
                    break
                if ch == b',':
                    break
                if len(prefix) >= 9 or not (48 <= ch[0] <= 57):
                    raise ValueError('invalid Draw_Number field')
                prefix.extend(ch)
            if not ch:
                break
            if len(prefix) > 1 and prefix[0] == 48:
                raise ValueError('leading zero in Draw_Number')
            draw_no = int(prefix)
            if draw_no >= CUTOFF:
                # Do not read, parse or display anything after this field.
                raise ValueError(f'draw CSV includes Draw_Number >= {CUTOFF}; '
                                 'run prepare to create a pre-holdout-only copy')
            if draws and draw_no != draws[-1].number + 1:
                raise ValueError('draw numbers must be strictly consecutive')
            inp.seek(beginning)
            line = inp.readline()  # Now known to be an eligible row.
            fields = next(csv.reader([line.decode('utf-8', errors='strict')], strict=True))
            if len(fields) != len(EXPECTED_HEADER):
                raise ValueError('malformed CSV row')
            stamp = fields[1]
            if date.fromisoformat(stamp).isoformat() != stamp:
                raise ValueError('noncanonical draw date')
            vals = fields[2:10]
            if not all(v.isascii() and v.isdecimal() and not v.startswith('0') for v in vals):
                raise ValueError('invalid noncanonical ball text')
            main = tuple(map(int, vals[:7]))
            pb = int(vals[7])
            if len(set(main)) != 7 or not all(1 <= x <= 35 for x in main) or not 1 <= pb <= 20:
                raise ValueError('invalid Powerball numbers in pre-holdout CSV')
            draws.append(Draw(draw_no, main, pb))
    if not draws:
        raise ValueError('empty draw CSV')
    return draws


def build_index(draws: list[Draw]):
    """P3 is indexed by sorted six-ball combinations, NOT by 5040 permutations/draw.

    We still match all 5040 possible *orders* through the canonical sorted key.
    This reduces index size and compilation time by ~720x for P3.
    """
    p1 = defaultdict(list)
    p2 = defaultdict(list)
    p3 = defaultdict(list)
    for d in draws:
        p1[(*d.drawn, d.powerball)].append(d.number)
        p2[d.drawn].append(d.number)
        for six in combinations(d.drawn, 6):
            p3[(tuple(sorted(six)), d.powerball)].append(d.number)
    return p1, p2, p3


def scan_one(path: Path, draws: list[Draw], indexes, dest: Path, chunk_size: int,
             status_seconds: float, echo_chunks: bool, max_bytes: int | None,
             draw_copy: str = DEFAULT_DRAWS, index_prep_seconds: float = 0):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'digit stream is absent or is a symlink: {path}')
    actual_size = path.stat().st_size
    total = actual_size if max_bytes is None else min(max_bytes, actual_size)
    if total < 14:
        raise ValueError('digit file must have at least 14 digits')
    label = path.stem
    dest.mkdir(parents=True, exist_ok=True)
    matches_path = dest / f'{label}_matches.csv'
    transitions_path = dest / f'{label}_transitions.csv'
    summary_path = dest / f'{label}_summary.json'
    # One record for each draw and category; match positions always increase.
    positions = defaultdict(list)
    hits = Counter()
    p1, p2, p3 = indexes
    t0 = time.perf_counter()
    next_update = t0 + status_seconds
    chunks = candidates = 0
    scanned_hasher = hashlib.sha256()
    print(f'[{label}] Input: {total:,} numeric digit bytes. Encoding: {FORMAT}', flush=True)
    with path.open('rb') as src, matches_path.open('w', encoding='utf-8', newline='') as out:
        for prefix_name, expected in KNOWN_PREFIXES.items():
            if path.name.startswith(prefix_name):
                seen = src.read(len(expected))
                if seen != bytes(ord(c) - 48 for c in expected):
                    raise ValueError(f'{label} fails known 32-digit constant-prefix check')
                print(f'[{label}] Known {prefix_name} prefix: PASS ({len(expected)} digits).', flush=True)
                break
        writer = csv.writer(out)
        writer.writerow(('constant_file', 'draw_number', 'category', 'start_digit_offset_0_based',
                         'end_digit_offset_exclusive', 'matched_decimal_digits'))
        # Seek for every chunk, adding 15 look-ahead bytes. This is an intentionally
        # bounded-memory alternative to mapping a whole 1 TB file into an address space.
        for start in range(0, total, chunk_size):
            span = min(chunk_size, total - start)
            src.seek(start)
            block = src.read(min(span + 15, total - start))
            if len(block) < span:
                raise IOError('digit file was shortened during the scan')
            scanned_hasher.update(block[:span])  # Exactly once, without the 15-byte lookahead.
            digits = np.frombuffer(block, dtype=np.uint8)
            invalid = np.flatnonzero(digits > 9)
            if invalid.size:
                raise ValueError(f'non-digit binary byte at file offset {start + int(invalid[0])}')
            # A candidate 14-digit pattern starts only when all 14 bytes exist.
            n = min(span, max(0, len(block) - 13))
            if n:
                # Every position, including odd offsets, is examined.
                # int16 avoids 8-bit multiplication overflow.
                balls = [(digits[2*j:2*j+n].astype(np.uint16) * 10 +
                          digits[2*j+1:2*j+1+n]) for j in range(7)]
                six_ok = np.ones(n, dtype=np.bool_)
                for b in balls[:6]:
                    six_ok &= (b >= 1) & (b <= 35)
                p3_ok = six_ok & (balls[6] >= 1) & (balls[6] <= 20)
                p2_ok = six_ok & (balls[6] >= 1) & (balls[6] <= 35)
                idxs = np.flatnonzero(p3_ok | p2_ok)
                candidates += len(idxs)
                for i_ in idxs:
                    i = int(i_)
                    six = tuple(int(b[i]) for b in balls[:6])
                    if len(set(six)) != 6:
                        continue
                    seventh = int(balls[6][i])
                    location = start + i
                    if bool(p3_ok[i]):
                        for draw_no in p3.get((tuple(sorted(six)), seventh), ()):
                            positions[(draw_no, P3)].append(location)
                            hits[P3] += 1
                            writer.writerow((label, draw_no, P3, location, location + 14,
                                             display_pattern(block[i:i+14])))
                    if bool(p2_ok[i]) and seventh not in six:
                        seven = (*six, seventh)
                        for draw_no in p2.get(seven, ()):
                            positions[(draw_no, P2)].append(location)
                            hits[P2] += 1
                            writer.writerow((label, draw_no, P2, location, location + 14,
                                             display_pattern(block[i:i+14])))
                        # A P1 match needs two additional bytes after the P2 prefix.
                        if i + 15 < len(block):
                            pb = block[i + 14] * 10 + block[i + 15]
                            if 1 <= pb <= 20:
                                for draw_no in p1.get((*seven, pb), ()):
                                    positions[(draw_no, P1)].append(location)
                                    hits[P1] += 1
                                    writer.writerow((label, draw_no, P1, location, location + 16,
                                                     display_pattern(block[i:i+16])))
            chunks += 1
            now = time.perf_counter()
            done = start + span
            if echo_chunks or now >= next_update or done == total:
                elapsed = now - t0
                speed = done / elapsed / 1e6 if elapsed else 0
                print(f'[{label}] {done:,}/{total:,} bytes ({done/total:.1%}), '
                      f'{speed:.2f} MB/s, {candidates:,} valid candidate starts, '
                      f'matches P1/P2/P3={hits[P1]}/{hits[P2]}/{hits[P3]}', flush=True)
                next_update = now + status_seconds
    scan_elapsed = time.perf_counter() - t0
    analysis_start = time.perf_counter()
    transition_summary = build_transition_report(draws, positions, transitions_path)
    analysis_elapsed = time.perf_counter() - analysis_start
    speed = total / scan_elapsed
    summary = {
        'experiment': 'OUTLANDISH_01_STAGE_A_POWERBALL',
        'category_definition': {'P1': '7 drawn-order main numbers + Powerball',
                                'P2': '7 drawn-order main numbers',
                                'P3': 'any 6 distinct main numbers, any order + Powerball'},
        'ball_encoding': FORMAT,
        'constant_file': str(path), 'input_bytes': total,
        'file_actual_bytes': actual_size,
        'draw_copy': draw_copy,
        'draws_and_index_prep_seconds': round(index_prep_seconds, 6),
        'scanned_prefix_sha256': scanned_hasher.hexdigest(),
        'draw_count': len(draws), 'first_draw': draws[0].number, 'last_draw': draws[-1].number,
        'holdout_cutoff_exclusive': CUTOFF,
        'implementation': 'one-threaded NumPy vectorized chunk scan (all byte offsets)',
        'chunk_bytes': chunk_size,
        'chunks': chunks, 'candidate_starts_examined': candidates,
        'match_counts': {'P1': hits[P1], 'P2': hits[P2], 'P3': hits[P3]},
        'scan_elapsed_seconds': round(scan_elapsed, 6),
        'analysis_elapsed_seconds': round(analysis_elapsed, 6),
        'scan_MB_per_second': round(speed / 1e6, 3),
        'projected_scan_1e9_seconds': round(1e9 / speed, 2),
        'projected_scan_1e12_seconds': round(1e12 / speed, 2),
        'projections_are': 'rough linear scan-only estimates; not generation, disk capacity, or real large-file measurements',
        **transition_summary,
    }
    summary_path.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(f'[{label}] SCAN FINISHED in {scan_elapsed:.3f}s, analysis {analysis_elapsed:.3f}s. '
          f'Matches: {dict(hits)}', flush=True)
    if total >= 100_000:
        print(f'[{label}] Linear scan-only projection: 1e9 = {1e9/speed/60:.2f} min; '
              f'1e12 = {1e12/speed/3600:.2f} h (very uncertain).', flush=True)
    else:
        print(f'[{label}] Tiny self-test file: do not extrapolate scan time.', flush=True)
    print(f'[{label}] Evidence: {matches_path}, {transitions_path}, {summary_path}', flush=True)
    return summary, positions


def closest_pair(a: list[int], b: list[int]):
    """For increasing position lists, return closest signed delta (B - A)."""
    if not a or not b:
        return None
    best = None
    for x in a:
        j = bisect.bisect_left(b, x)
        for k in (j-1, j):
            if 0 <= k < len(b):
                delta = b[k] - x
                if best is None or abs(delta) < abs(best):
                    best = delta
    return best


def build_transition_report(draws: list[Draw], positions, destination: Path):
    counts = {'pairs': max(0, len(draws)-1), 'pairs_both_have_any_match': 0,
              'pairs_W_P1_and_next_any_match': 0}
    with destination.open('w', encoding='utf-8', newline='') as out:
        w = csv.writer(out)
        w.writerow(('draw_W', 'draw_W_plus_1', 'W_P1', 'W_P2', 'W_P3',
                    'next_P1', 'next_P2', 'next_P3', 'min_signed_offset_delta_W_P1_to_next_P1',
                    'min_signed_offset_delta_W_P1_to_next_P2',
                    'min_signed_offset_delta_W_P1_to_next_P3'))
        for prev, nxt in zip(draws, draws[1:]):
            prev_count = [len(positions[(prev.number, d)]) for d in (1,2,3)]
            nxt_count = [len(positions[(nxt.number, d)]) for d in (1,2,3)]
            if sum(prev_count) and sum(nxt_count):
                counts['pairs_both_have_any_match'] += 1
                if prev_count[0]:
                    counts['pairs_W_P1_and_next_any_match'] += 1
                deltas = [closest_pair(positions[(prev.number, 1)],
                                       positions[(nxt.number, d)]) for d in (1,2,3)]
                w.writerow((prev.number, nxt.number, *prev_count, *nxt_count,
                            *('' if d is None else d for d in deltas)))
    return {'transition_statistics': counts}


def self_test():
    """Invented examples only. Includes planted matches and cross-chunk boundaries."""
    d = Draw(1500, (3,14,25,7,31,8,22), 12)
    indexes = build_index([d])
    p1 = encode_balls((*d.drawn, d.powerball))
    p2 = encode_balls(d.drawn)
    p3 = encode_balls((25,3,31,8,22,14,12))
    assert len(p1) == 16 and len(p2) == 14 and len(p3) == 14
    assert encode_balls((3, 12)) == bytes((0,3,1,2))
    with TemporaryDirectory() as td:
        f = Path(td) / 'invented_digits.bin'
        prefix = bytes([9]) * 19
        stream = prefix + p1 + bytes([9])*23 + p2 + bytes([9])*25 + p3 + bytes([9])*9
        f.write_bytes(stream)
        r, pos = scan_one(f, [d], indexes, Path(td)/'reports', chunk_size=17,
                          status_seconds=9999, echo_chunks=False, max_bytes=None)
        assert 19 in pos[(1500, 1)], (pos, 19)
        assert 19 in pos[(1500, 2)], (pos, 19)
        assert len(pos[(1500, 3)]) >= 1 and 19+16+23+14+25 in pos[(1500, 3)]
        assert r['match_counts']['P1'] >= 1
        # Last valid P2 pattern at EOF, without room for P1's final 2 digits.
        end = Path(td) / 'end_digits.bin'
        end.write_bytes(bytes([9])*7 + p2)
        _, p = scan_one(end, [d], indexes, Path(td)/'reports2', chunk_size=8,
                        status_seconds=9999, echo_chunks=False, max_bytes=None)
        assert p[(1500,2)] == [7]
        # Invalid byte must refuse, not be interpreted as a digit.
        bad = Path(td) / 'bad.bin'
        bad.write_bytes(bytes([9])*15 + bytes([49]) + bytes([9])*15)
        try:
            scan_one(bad, [d], indexes, Path(td)/'reports3', 8, 9999, False, None)
        except ValueError:
            pass
        else:
            raise AssertionError('non-digit byte accepted')
    print('SELF-TEST PASS: invented P1/P2/P3, overlapping and chunk-boundary positions, EOF, invalid byte.')


def format_sizes():
    for n in (10**6, 10**9, 10**12):
        print(f'One constant, {n:,} digits = {n:,} bytes = {n/(1024**3):,.3f} GiB '
              f'({n/1e9:,.3f} decimal GB)')
    print('Two 1e12 constant files require 2,000,000,000,000 bytes before temporary output files.')


def main(argv=None):
    parser = argparse.ArgumentParser(description='OUTLANDISH_01: independent pre-holdout Powerball digit scanner')
    sub = parser.add_subparsers(dest='cmd', required=True)
    prep = sub.add_parser('prepare', help='owner-only: extract safe development CSV; stop before holdout')
    prep.add_argument('--source', required=True, type=Path,
                      help='authoritative master location, on owner PC only')
    prep.add_argument('--output', type=Path, default=Path(DEFAULT_DRAWS))
    scan = sub.add_parser('scan', help='scan pi and golden-ratio digit files')
    scan.add_argument('--draws', type=Path, default=Path(DEFAULT_DRAWS))
    scan.add_argument('--digits', nargs='+', type=Path, default=[Path(x) for x in DEFAULT_DIGITS])
    scan.add_argument('--output-dir', type=Path, default=Path('OUTLANDISH_01_results'))
    scan.add_argument('--chunk-bytes', type=int, default=100_000)
    scan.add_argument('--progress-seconds', type=float, default=5)
    scan.add_argument('--max-bytes', type=int, default=None,
                      help='optional shorter benchmark; default entire provided file')
    sub.add_parser('self-test', help='invented data only; never accesses project data')
    sub.add_parser('sizes', help='print exact binary file sizes and storage costs')
    args = parser.parse_args(argv)
    if args.cmd == 'prepare':
        prepare_preholdout(args.source, args.output)
    elif args.cmd == 'self-test':
        self_test()
    elif args.cmd == 'sizes':
        format_sizes()
    elif args.cmd == 'scan':
        if args.chunk_bytes < 32 or args.chunk_bytes > 64_000_000:
            parser.error('--chunk-bytes must be in range 32..64,000,000')
        if args.progress_seconds <= 0:
            parser.error('--progress-seconds must be positive')
        if args.max_bytes is not None and args.max_bytes < 14:
            parser.error('--max-bytes must be >= 14')
        load_start = time.perf_counter()
        draws = load_draws(args.draws)
        load_seconds = time.perf_counter() - load_start
        build_start = time.perf_counter()
        indexes = build_index(draws)
        build_seconds = time.perf_counter() - build_start
        prep_seconds = load_seconds + build_seconds
        print(f'DRAWS: {len(draws):,} eligible pre-holdout draws, '
              f'{draws[0].number}..{draws[-1].number}. No sample records.')
        print(f'CSV LOAD: {load_seconds:.4f}s; INDEX BUILD: {build_seconds:.4f}s; '
              f'unique P1/P2/P3 keys {len(indexes[0]):,}/{len(indexes[1]):,}/{len(indexes[2]):,}.')
        # Separate output folder per invocation: never overwrite earlier reports.
        run_stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        run_dir = args.output_dir / f'run_{run_stamp}'
        suffix = 2
        while run_dir.exists():
            run_dir = args.output_dir / f'run_{run_stamp}_{suffix}'
            suffix += 1
        run_dir.mkdir(parents=True)
        print(f'Results directory: {run_dir}')
        all_results = []
        for file in args.digits:
            if not file.is_file():
                raise FileNotFoundError(file)
            # Lots of diagnostic lines for the 1e6 trial; time-gated for larger files.
            show_every = (file.stat().st_size <= 2_000_000)
            report, _ = scan_one(file, draws, indexes, run_dir,
                                 args.chunk_bytes, args.progress_seconds,
                                 show_every, args.max_bytes, str(args.draws), prep_seconds)
            all_results.append(report)
        (run_dir / 'run_summary.json').write_text(json.dumps({
            'draw_copy': str(args.draws),
            'draws_and_index_prep_seconds': round(prep_seconds, 6),
            'scans': all_results,
        }, indent=2) + '\n', encoding='utf-8')
        print('\nSUMMARY')
        for r in all_results:
            c = r['match_counts']
            print(f"{r['constant_file']}: P1={c['P1']}, P2={c['P2']}, P3={c['P3']}; "
                  f"scan={r['scan_elapsed_seconds']:.3f}s; "
                  f"project 1e9={r['projected_scan_1e9_seconds']:.1f}s; "
                  f"1e12={r['projected_scan_1e12_seconds']/3600:.1f}h (illustrative)")
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, OSError, csv.Error) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(2)
