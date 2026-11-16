#!/usr/bin/env python3
"""OUTLANDISH_01 reviewer's full-size synthetic rehearsal, v0.1 (Claude, review point C).

Purpose
    Evidence behind OUTLANDISH_REVIEW_004_Claude_to_ChatGPT.md, and a way to
    MEASURE scan time and memory on the machine that will run Q5, instead of
    estimating them. It pushes one FABRICATED constant of production size
    (9,999,999,999 digits, 5,000,000,000 packed bytes) through the committed
    Q4i path in SYNTHETIC mode, against 433 FABRICATED draws.

What it checks
    1. The scan completes at production size with the default 4,000,000-byte
       chunks (1,250 chunks) and the in-scan full-file digest matches.
    2. Five planted hits at awkward positions are found: an odd start at the
       beginning, a window straddling 2^32, a window straddling a chunk
       boundary, a start at 2^33 - 1, and the last valid 16-digit start.
       The shifted P1 -> P3 event at the very last valid 14-digit start too.
    3. Soundness: every reported event is re-read from the file and checked
       against the literal rule by the reviewer's own code.
    4. Counts of chance events on random digits are close to the analytical
       expectation (about 218 P3_any, 218 P2_any, 2 P1_any).
    5. One report with 10,000 permutations is created, loaded and audited.

What it does NOT do
    No REAL data. It never opens the published packed constants, receipts,
    POWERBALL_preholdout_only.csv, any results folder or any parent path.
    It does not use, need or change the Q5 switch. It runs only in the
    marked synthetic mode and refuses a work folder under the production
    root. A PASS is not Q4 production qualification and not Q5 authorisation.

Needs
    About 6 GB free in the work folder (the 5 GB file is deleted at the end
    unless --keep is given), the project venv (NumPy), and roughly 5 to 15
    minutes. The reviewer's Linux run took about 4.5 minutes in total.

Usage (Windows CMD, from the repository root; choose any scratch folder)
    ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\REVIEW\\OUTLANDISH_REVIEW_Claude_FullSize_Rehearsal_v0_1.py" --run --work-dir "T:\\some_scratch_folder"

Expected final line
    REVIEWER FULL-SIZE REHEARSAL PASS: digits=9999999999 bytes=5000000000 chunks=1250 ...

Reviewer's own result at commit 3a07e8aba15cb159e7e0cfc35e41a46bd5558833
(Linux, Python 3.13.18, NumPy 2.5.3, 2 cores): scan 222 s (22.6 packed MB/s),
peak memory 352 MiB, events 453 (K6S 226, K7 224, K7S 3), report 1.8 s.
Event counts may differ slightly with another NumPy version, because the
random background may differ; the planted checks are exact everywhere.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import random
import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
PROJECT = Path(__file__).absolute().parent.parent   # GAIS/OUTLANDISH_01
sys.path.insert(0, str(PROJECT))

DIGITS = 9_999_999_999        # odd on purpose: exercises the pad nibble at full size
BYTES = 5_000_000_000
FIRST_DRAW, DRAWS = 11, 433   # fixture identifiers; fabricated values
CONSTANT = 'pi'               # only a fixture file name; the content is random
RUN_ID = 'TEST_REAL_fullsize_rehearsal'
PRODUCTION_ROOT = r'G:\OUTLANDISH_01'


def say(*parts) -> None:
    print(time.strftime('%H:%M:%S'), *parts, flush=True)


def fixed2(values) -> str:
    return ''.join(f'{v:02d}' for v in values)


def peak_memory_mib():
    """Peak process memory in MiB, or None if it cannot be measured here."""
    try:
        if os.name == 'nt':
            import ctypes
            from ctypes import wintypes

            class Counters(ctypes.Structure):
                _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD),
                            ('PeakWorkingSetSize', ctypes.c_size_t),
                            ('WorkingSetSize', ctypes.c_size_t),
                            ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
                            ('QuotaPagedPoolUsage', ctypes.c_size_t),
                            ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                            ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                            ('PagefileUsage', ctypes.c_size_t),
                            ('PeakPagefileUsage', ctypes.c_size_t)]
            counters = Counters()
            counters.cb = ctypes.sizeof(Counters)
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            psapi = ctypes.WinDLL('psapi', use_last_error=True)
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters),
                                                   wintypes.DWORD]
            if not psapi.GetProcessMemoryInfo(kernel32.GetCurrentProcess(),
                                              ctypes.byref(counters), counters.cb):
                return None
            return counters.PeakWorkingSetSize / 2**20
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return peak / 2**20 if sys.platform == 'darwin' else peak / 1024
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--run', action='store_true', required=True)
    parser.add_argument('--work-dir', required=True,
                        help='existing scratch folder with about 6 GB free; never under G:\\OUTLANDISH_01')
    parser.add_argument('--keep', action='store_true', help='keep the 5 GB fixture afterwards')
    args = parser.parse_args()

    work = Path(args.work_dir).absolute()
    if not work.is_dir():
        raise SystemExit('work folder does not exist: ' + str(work))
    if os.path.normcase(str(work)).startswith(os.path.normcase(PRODUCTION_ROOT)):
        raise SystemExit('REFUSED: the work folder must not be under ' + PRODUCTION_ROOT)
    free = shutil.disk_usage(work).free
    if free < 6 * 10**9:
        raise SystemExit(f'not enough free space in work folder: {free / 1e9:.1f} GB, need about 6 GB')

    import numpy as np
    import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
    import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
    import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
    import OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 as R
    import OUTLANDISH_01_Q4i_Mode_v0_1 as M

    base = work / ('OUTLANDISH_Q4_SOURCE_SYNTHETIC_ONLY_fullsize_' + time.strftime('%Y%m%d_%H%M%S'))
    base.mkdir()
    say('PROJECT', PROJECT)
    say('SANDBOX', base)
    try:
        (base / 'SYNTHETIC_MARKER').write_bytes(G.MAGIC)
        for name in ('digits', 'histories', 'results'):
            (base / name).mkdir()
        roots = G.FixedRoots.test_sandbox(base)

        rng = random.Random(4242)
        draws = [(FIRST_DRAW + i, rng.sample(range(1, 36), 7), rng.randint(1, 20))
                 for i in range(DRAWS)]
        text = io.StringIO(newline='')
        writer = csv.writer(text, lineterminator='\n')
        writer.writerow(G.PB_HEADER)
        for number, mains, pb in draws:
            writer.writerow((number, '2000-01-01', *mains, pb))
        history = base / 'histories' / 'powerball_synthetic.csv'
        history.write_bytes(text.getvalue().encode('utf-8'))
        profile = G.HistoryProfile('powerball', history, FIRST_DRAW, FIRST_DRAW + DRAWS,
                                   G.PB_HEADER, True)

        # ---- fabricate the 5,000,000,000-byte packed file: random decimal digits
        source = roots.published_binary(CONSTANT)
        say('generating 5,000,000,000 random packed bytes')
        table = np.array([((v // 10) << 4) | (v % 10) for v in range(100)], dtype=np.uint8)
        generator = np.random.default_rng(20261116)
        with source.open('wb') as stream:
            for _ in range(50):
                stream.write(table[generator.integers(0, 100, size=100_000_000,
                                                      dtype=np.uint8)].tobytes())

        def plant(offset: int, digits: str) -> None:
            first, last = offset // 2, (offset + len(digits) + 1) // 2
            with source.open('r+b') as stream:
                stream.seek(first)
                window = stream.read(last - first).hex()
                at = offset - 2 * first
                window = window[:at] + digits + window[at + len(digits):]
                stream.seek(first)
                stream.write(bytes.fromhex(window))

        with source.open('r+b') as stream:     # odd digit count: final low nibble is padding
            stream.seek(BYTES - 1)
            final = stream.read(1)[0]
            stream.seek(BYTES - 1)
            stream.write(bytes([final & 0xF0]))

        planted = []

        def add(index: int, family: str, offset: int) -> None:
            number, mains, pb = draws[index]
            order = random.Random(index).sample(mains, 7)
            digits = {'K6S': fixed2(order[:6] + [pb]), 'K7': fixed2(order),
                      'K7S': fixed2(mains + [pb])}[family]
            plant(offset, digits)
            planted.append((number, family, offset, digits))

        add(5, 'K6S', 1)                    # odd start at the very beginning
        add(50, 'K7', 4_294_967_289)        # window straddles 2^32
        add(120, 'K7S', 4_799_999_993)      # odd start; window straddles a 4,000,000-byte chunk boundary
        add(200, 'K6S', 8_589_934_591)      # 2^33 - 1
        add(300, 'K7S', DIGITS - 16)        # last valid 16-digit start

        say('hashing the fixture and writing its receipt')
        digest = hashlib.sha256()
        with source.open('rb') as stream:
            for block in iter(lambda: stream.read(1 << 24), b''):
                digest.update(block)
        plan = G.sample_plan(BYTES)
        samples = []
        with source.open('rb') as stream:
            for offset, length in plan:
                stream.seek(offset)
                samples.append({'offset_bytes': offset, 'size': length,
                                'sha256': hashlib.sha256(stream.read(length)).hexdigest()})
        roots.receipt(CONSTANT).write_text(json.dumps({
            'format': G.FORMAT, 'format_version': 1, 'scope': G.SCOPE, 'constant': CONSTANT,
            'binary_name': source.name, 'digits_including_integer': DIGITS, 'packed_bytes': BYTES,
            'binary_sha256_streamed': digest.hexdigest(), 'sample_block_length': plan[0][1],
            'samples': samples}, indent=2) + '\n', encoding='utf-8')

        # ---- the committed path, synthetic mode, default chunk size
        mode = M.PowerballMode.synthetic(roots, profile, DIGITS)
        say('scan start (default chunk size)')
        started = time.perf_counter()
        P.run_powerball(mode, CONSTANT, RUN_ID)
        scan_seconds = time.perf_counter() - started
        peak = peak_memory_mib()
        rate = BYTES / 1e6 / scan_seconds
        say(f'scan done: {scan_seconds:.0f} s, {rate:.1f} packed MB/s, peak memory '
            + (f'{peak:.0f} MiB' if peak is not None else 'not measured'))

        meta, _raw, _hist, events, _cls = P.load_run(mode, CONSTANT, RUN_ID)
        got = [(e.draw_number, e.family, e.start_digit_offset, e.matched_digits) for e in events]
        chunks = -(-BYTES // meta['chunk_bytes'])
        if meta['bytes_hashed'] != BYTES or meta['digits'] != DIGITS:
            raise AssertionError('run manifest does not cover the full file')

        # ---- soundness: re-read each reported window and apply the literal rule
        by_number = {number: (mains, pb) for number, mains, pb in draws}
        with source.open('rb') as stream:
            for number, family, offset, digits in got:
                length = S.FAMILY_LENGTHS[family]
                first = offset // 2
                stream.seek(first)
                window = stream.read((offset + length + 1) // 2 - first).hex()
                at = offset - 2 * first
                if window[at:at + length] != digits or offset + length > DIGITS:
                    raise AssertionError(f'event text differs from the file at offset {offset}')
                v = [int(digits[k:k + 2]) for k in range(0, length, 2)]
                mains, pb = by_number[number]
                if family == 'K7':
                    ok = len(set(v)) == 7 and set(v) == set(mains)
                elif family == 'K6S':
                    ok = len(set(v[:6])) == 6 and set(v[:6]) <= set(mains) and v[6] == pb
                else:
                    ok = len(set(v[:7])) == 7 and set(v[:7]) == set(mains) and v[7] == pb
                if not ok:
                    raise AssertionError(f'event violates its family rule: {number} {family} {offset}')
        say(f'PASS soundness: all {len(got)} reported events re-read from the file and rule-checked')

        found = set(got)
        for item in planted:
            if item not in found:
                raise AssertionError(f'planted event not found: {item}')
        for index, start in ((120, 4_799_999_995), (300, DIGITS - 14)):   # P1@k => P3@k+2
            number, mains, pb = draws[index]
            if (number, 'K6S', start, fixed2(mains[1:] + [pb])) not in found:
                raise AssertionError(f'shifted P3 event missing at {start}')
        if max(o + S.FAMILY_LENGTHS[f] for _, f, o, _ in got) != DIGITS:
            raise AssertionError('no event ends exactly at the last digit')
        say('PASS planted: odd start, 2^32 straddle, chunk-boundary straddle, 2^33-1, '
            'last valid 16-digit and 14-digit starts')

        counts = meta['family_counts']
        expected14 = DRAWS * 5040 * (DIGITS - 13) / 1e14
        expected16 = DRAWS * 5040 * (DIGITS - 15) / 1e16
        chance = {'K6S': counts.get('K6S', 0) - 4, 'K7': counts.get('K7', 0) - 3,
                  'K7S': counts.get('K7S', 0) - 2}     # remove the planted and implied events
        for family in ('K6S', 'K7'):
            if abs(chance[family] - expected14) > 5 * expected14 ** 0.5:
                raise AssertionError(f'{family} chance count {chance[family]} is far from {expected14:.1f}')
        if chance['K7S'] > 15:
            raise AssertionError('implausibly many chance K7S events')
        odd = sum(o & 1 for _, _, o, _ in got)
        say(f'PASS counts: chance events K6S={chance["K6S"]} K7={chance["K7"]} K7S={chance["K7S"]}; '
            f'expected about {expected14:.1f}, {expected14:.1f}, {expected16:.2f}; '
            f'odd-offset events {odd} of {len(got)}')
        same = counts == {'K6S': 226, 'K7': 224, 'K7S': 3}
        say('counts identical to the reviewer\'s run (226/224/3): ' + ('yes' if same else
            'no - a different NumPy random stream; not a failure'))

        started = time.perf_counter()
        R.create_report(mode, CONSTANT, RUN_ID)
        report_seconds = time.perf_counter() - started
        report = R.load_report(mode, CONSTANT, RUN_ID)['report']
        perm = report['permutation']
        if perm['iterations_requested'] != 10_000 or not R.audit_report(mode, CONSTANT, RUN_ID)['science_matches']:
            raise AssertionError('report permutation count or audit failed')
        summary = report['transitions_summary']
        say(f'PASS report: {report_seconds:.1f} s, 10,000 permutations, evaluable pairs '
            f'{summary["evaluable_pairs"]} of {summary["total_adjacent_pairs"]}, '
            f'p={perm["centered_two_sided_p"]:.4f}; audit reproduced it')

        six = 6 * scan_seconds / 60
        print(f'REVIEWER FULL-SIZE REHEARSAL PASS: digits={DIGITS} bytes={BYTES} chunks={chunks} '
              f'events={len(got)} scan_seconds={scan_seconds:.0f} packed_MB_per_s={rate:.1f} '
              f'peak_MiB={"%.0f" % peak if peak is not None else "n/a"} '
              f'report_seconds={report_seconds:.1f} six_constant_scan_estimate_minutes={six:.0f}')
        print('  SYNTHETIC ONLY: fabricated digits and draws; Q5 switch not used or changed.')
        print('  Not Q4 production qualification; not Q5 authorisation.')
    finally:
        if args.keep:
            say('kept sandbox:', base)
        else:
            shutil.rmtree(base, ignore_errors=True)
            say('sandbox removed' if not base.exists() else f'could not fully remove {base}')


if __name__ == '__main__':
    main()
