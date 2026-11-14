#!/usr/bin/env python3
r"""OUTLANDISH_01 Q2: unchanged old packed Powerball scanner vs independent oracle.

Only small SYNTHETIC digit files/drawsets and disposable TEST results under the
Windows temporary directory. Never opens published packed data or REAL CSVs.
Read-only listing fingerprint of the REAL results directory checks isolation.

Run from the Ryzen repository root with the existing .venv Python:
  .venv\Scripts\python.exe GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1.py --self-test
  .venv\Scripts\python.exe GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1.py --run

The fixture purposefully reproduces an observed *potential* prefix-boundary
risk in the old scanner. A mismatch is a Q2 FINDING, not an excuse to alter
that historical scanner. A new engine must meet ratified per-family EOF rules.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from OUTLANDISH_01_Q2_Independent_Oracle_v0_1 import (
    PowerballDraw, encoded, oracle, pack_independent, plant,
)

HERE = Path(__file__).resolve().parent
OLD_SCANNER = HERE / 'OUTLANDISH_WSL' / 'wsl_scan_packed_powerball.py'
OLD_SCANNER_GIT_BLOB_SHA1 = '675d0f1592d417483c051605d77093a3e716ac03'
ORACLE_FILE = HERE / 'OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py'
ORACLE_GIT_BLOB_SHA1 = '6ea5562ed681c854f8c552e9600af5d8f9d3be00'
REAL_RESULTS_ROOT = Path(r'G:\OUTLANDISH_01\large_artifacts\results')
PHI_KNOWN_FIRST_32 = '16180339887498948482045868343656'

D1 = PowerballDraw(1, (3, 7, 11, 15, 19, 23, 35), 7)
D2 = PowerballDraw(2, (1, 5, 9, 13, 17, 21, 25), 4)
D3 = PowerballDraw(3, (2, 4, 6, 8, 10, 12, 14), 18)
D4 = PowerballDraw(4, (5, 9, 13, 17, 21, 25, 29), 1)
D5 = PowerballDraw(5, (1, 5, 9, 13, 17, 21, 4), 12)  # K7/K6S role collision
D6 = PowerballDraw(6, D1.mains, 16)                   # repeated K7 key, distinct PB
DRAWS = [D1, D2, D3, D4, D5, D6]


@dataclass(frozen=True)
class Scenario:
    name: str
    digits: str
    prefix_digits: int | None = None


def git_blob_sha(data: bytes) -> str:
    # Only normalise CRLF for a Git-core.autocrlf checkout of canonical LF blobs.
    canonical = data.replace(b'\r\n', b'\n')
    return hashlib.sha1(f'blob {len(canonical)}\0'.encode() + canonical).hexdigest()


def sources_preflight() -> None:
    for path, expected in ((OLD_SCANNER, OLD_SCANNER_GIT_BLOB_SHA1),
                           (ORACLE_FILE, ORACLE_GIT_BLOB_SHA1)):
        if not path.is_file() or path.is_symlink():
            raise ValueError(f'required ordinary source file missing/linked: {path}')
        actual = git_blob_sha(path.read_bytes())
        if actual != expected:
            raise ValueError(f'historical code identity changed: {path.name}; '
                             f'Git blob expected {expected}, observed {actual}. '
                             'Do not modify the unchanged reference scanner.')


def scenario_set() -> list[Scenario]:
    # All patches start after the 32-digit prefix mandated by the old scanner's
    # mathematical-prefix verifier. The remaining digits are explicitly synthetic.
    basic = plant(340, [(64, encoded(*D1.mains, D1.pb)),
                        (109, encoded(*D2.mains)),
                        (170, encoded(2, 4, 6, 8, 12, 14, 18)),
                        (230, encoded(*D3.mains, D3.pb)),
                        (300, encoded(3, 7, 11, 15, 19, 23, 7))])
    cross = plant(341, [
        (55, encoded(*D1.mains, D1.pb)),    # odd, crosses chunk 64; d1/d6 P2 at same start
        (94, encoded(*D2.mains)),           # even, crosses chunk 96
        (127, encoded(2, 4, 6, 8, 12, 14, 18)),  # odd, crosses chunk 128
        (159, encoded(*D3.mains, D3.pb)),   # odd, crosses chunk 160
        (207, encoded(1, 5, 9, 13, 17, 21, 4)), # d2 K6S + d5 K7
        (255, encoded(3, 7, 11, 15, 19, 23, 7)),# PB equals selected main
        (325, encoded(*D1.mains, D1.pb)),   # final valid 16-digit start, odd N
    ])
    cases = [
        Scenario('planted_baseline_340', PHI_KNOWN_FIRST_32 + basic[32:]),
        Scenario('chunk_crossings_duplicate_keys_odd_N', PHI_KNOWN_FIRST_32 + cross[32:]),
        Scenario('EOF_K7S_odd_N', PHI_KNOWN_FIRST_32 + plant(95, [(79, encoded(*D1.mains, D1.pb))])[32:]),
        Scenario('EOF_K7_even_N', PHI_KNOWN_FIRST_32 + plant(94, [(80, encoded(*D2.mains))])[32:]),
        Scenario('EOF_K6S_odd_N', PHI_KNOWN_FIRST_32 + plant(95, [(81, encoded(2, 4, 6, 8, 12, 14, 18))])[32:]),
        Scenario('PREFIX_END_EOF_ELIGIBILITY', PHI_KNOWN_FIRST_32 + cross[32:], prefix_digits=332),
    ]
    assert all(len(x.digits) <= 2000 and x.digits.startswith(PHI_KNOWN_FIRST_32) for x in cases)
    assert all(32 <= (x.prefix_digits or len(x.digits)) <= len(x.digits) for x in cases)
    return cases


def result_root_fingerprint() -> tuple:
    if not REAL_RESULTS_ROOT.exists():
        return ('NO_REAL_RESULTS_DIRECTORY',)
    if not REAL_RESULTS_ROOT.is_dir() or REAL_RESULTS_ROOT.is_symlink():
        raise ValueError('REAL results root is not an ordinary directory')
    listing = []
    for root, dirs, files in os.walk(REAL_RESULTS_ROOT, followlinks=False):
        parent = Path(root)
        for item in sorted(dirs + files):
            p = parent / item
            st = p.lstat()
            listing.append((str(p.relative_to(REAL_RESULTS_ROOT)), p.is_dir(), st.st_size, st.st_mtime_ns))
            if p.is_symlink():
                raise ValueError(f'linked entry in REAL results root: {p}')
    return tuple(listing)


def write_draws(path: Path, *, forbidden_id: bool = False) -> None:
    with path.open('x', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(('Draw_Number', 'Date', *(f'Drawn_{i}' for i in range(1, 8)), 'Powerball'))
        start = date(2025, 1, 2)
        for i, d in enumerate(DRAWS):
            w.writerow((d.number, (start + timedelta(days=7*i)).isoformat(), *d.mains, d.pb))
        if forbidden_id:
            # The old reader MUST reject the restricted ID before parsing the
            # deliberately invalid (and non-outcome) remainder of the row.
            f.write('1577,RESTRICTED_FIELDS_MUST_NOT_BE_PARSED\r\n')


def write_synthetic(path: Path, digits: str, *, corrupt_nibble: bool = False,
                    corrupt_digest: bool = False) -> None:
    if not digits.startswith(PHI_KNOWN_FIRST_32) or len(digits) >= 8192:
        raise ValueError('synthetic fixture violates bounded known-prefix rules')
    raw = bytearray(pack_independent(digits))
    if corrupt_nibble:
        raw[25] = 0xFA  # beyond the required first 32 digits
    data = bytes(raw)
    path.write_bytes(data)
    # len(data)<4096 makes the legacy readback plan exactly one full-file sample.
    assert len(data) <= 4096
    digest = hashlib.sha256(data).hexdigest()
    if corrupt_digest:
        digest = '0' * 64
    receipt = {
        'format': 'OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1', 'format_version': 1,
        'scope': 'PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY',
        'constant': 'phi', 'digits_including_integer': len(digits),
        'packed_bytes': len(data), 'binary_name': path.name,
        'binary_sha256_streamed': digest,
        'sample_block_length': len(data),
        'samples': [{'offset_bytes': 0, 'size': len(data),
                     'sha256': hashlib.sha256(data).hexdigest()}],
        'fixture_warning': 'SYNTHETIC_Q2_ONLY; NOT A MATHEMATICAL CONSTANT OR REAL INPUT',
    }
    rp = path.with_name(path.name + '.wsl-receipt.json')
    rp.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')


def expected_rows(s: Scenario) -> set[tuple[int, str, int, str]]:
    effective = s.digits[:s.prefix_digits] if s.prefix_digits is not None else s.digits
    rows = set()
    for hit in oracle('powerball', effective, DRAWS):
        if hit.family == 'K7S' and 'P1_drawn_order' in hit.flags:
            label = 'P1'
        elif hit.family == 'K7' and 'P2_drawn_order' in hit.flags:
            label = 'P2'
        elif hit.family == 'K6S':
            label = 'P3'
        else:
            continue
        row = (hit.draw, label, hit.start, hit.digits)
        if row in rows:
            raise ValueError(f'independent oracle produced duplicate baseline identity: {row}')
        rows.add(row)
    return rows


def read_actual_rows(csv_path: Path, effective_N: int) -> set[tuple[int, str, int, str]]:
    if not csv_path.is_file():
        raise ValueError('old scanner did not produce a matches.csv')
    with csv_path.open('r', encoding='utf-8-sig', newline='') as f:
        rd = csv.DictReader(f)
        required = {'packed_file', 'draw_number', 'category', 'start_digit_offset_0_based',
                    'end_digit_offset_exclusive', 'matched_decimal_digits'}
        if set(rd.fieldnames or ()) != required:
            raise ValueError(f'unexpected old-scanner CSV schema: {rd.fieldnames}')
        result = set()
        for row in rd:
            label = row['category']
            if label not in ('P1', 'P2', 'P3'):
                raise ValueError(f'unknown category: {label}')
            draw = int(row['draw_number'])
            start = int(row['start_digit_offset_0_based'])
            end = int(row['end_digit_offset_exclusive'])
            text = row['matched_decimal_digits']
            length = 16 if label == 'P1' else 14
            if (start < 0 or end != start + length or len(text) != length
                    or not text.isascii() or not text.isdecimal()):
                raise ValueError(f'malformed old scanner row: {row}')
            # Include the row in comparison even if beyond cutoff, so a scanner
            # error is conspicuous rather than being silently filtered away.
            item = (draw, label, start, text)
            if item in result:
                raise ValueError(f'duplicate old scanner event identity: {item}')
            result.add(item)
    return result


def call_scanner(binary: Path, draws: Path, output_root: Path,
                 *, prefix_digits: int | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(OLD_SCANNER), '--input', str(binary),
           '--draws', str(draws), '--output-root', str(output_root),
           '--chunk-digits', '32', '--progress-seconds', '999', '--run']
    if prefix_digits is not None:
        cmd.extend(['--prefix-digits', str(prefix_digits)])
    return subprocess.run(cmd, cwd=output_root.parent, text=True,
                          encoding='utf-8', errors='replace',
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=45, check=False)


def check_one(case: Scenario, root: Path) -> tuple[bool, str]:
    folder = root / case.name
    folder.mkdir()
    data = folder / 'Q2_SYNTHETIC_ONLY_phi.packed.bin'
    draws = folder / 'fixture_draws_PB_NOT_REAL.csv'
    out = folder / 'test_results_not_real'
    out.mkdir()
    write_synthetic(data, case.digits)
    write_draws(draws)
    expected = expected_rows(case)
    result = call_scanner(data, draws, out, prefix_digits=case.prefix_digits)
    if result.returncode != 0:
        return False, f'exit {result.returncode}; {result.stderr.strip()[-480:]}'
    created = list(out.glob('packed_run_*'))
    if len(created) != 1:
        return False, f'expected one isolated TEST run, observed {len(created)}'
    actual = read_actual_rows(created[0] / 'matches.csv', case.prefix_digits or len(case.digits))
    observed = json.loads((created[0] / 'summary.json').read_text(encoding='utf-8'))
    if not observed.get('scanned_full') and case.prefix_digits is None:
        return False, 'old scanner did not report a complete fixture scan'
    exp_counts = {cat: sum(row[1] == cat for row in expected) for cat in ('P1', 'P2', 'P3')}
    if observed.get('match_counts') != exp_counts:
        # Mismatching counts are diagnosed together with exact row differences.
        pass
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    over_end = sorted((row for row in actual if row[2] + (16 if row[1] == 'P1' else 14) > (case.prefix_digits or len(case.digits))))
    if missing or extra or over_end or observed.get('match_counts') != exp_counts:
        return False, (f'expected P1/P2/P3 {exp_counts}; observed {observed.get("match_counts")}; '
                       f'missing={missing[:5]}; extra={extra[:5]}; '
                       f'events_beyond_effective_EOF={over_end[:5]}')
    return True, f'{len(actual)} exact event tuples; P1/P2/P3={exp_counts["P1"]}/{exp_counts["P2"]}/{exp_counts["P3"]}'


def negative_canary(kind: str, root: Path) -> tuple[bool, str]:
    folder = root / ('canary_' + kind)
    folder.mkdir()
    data = folder / 'Q2_SYNTHETIC_ONLY_phi.packed.bin'
    draws = folder / 'fixture_draws_PB_NOT_REAL.csv'
    out = folder / 'test_results_not_real'
    out.mkdir()
    digits = scenario_set()[0].digits
    write_synthetic(data, digits, corrupt_nibble=(kind == 'invalid_bcd'),
                    corrupt_digest=(kind == 'wrong_full_sha'))
    write_draws(draws, forbidden_id=(kind == 'cutoff_draw_refusal'))
    r = call_scanner(data, draws, out)
    if r.returncode == 0 or 'SCAN PASS' in r.stdout:
        return False, 'incorrectly accepted invalid synthetic input'
    diagnostic = (r.stderr + '\n' + r.stdout).strip()
    needles = {'invalid_bcd': 'invalid BCD nibble',
               'wrong_full_sha': 'FULL SCAN SHA DIFFERS',
               'cutoff_draw_refusal': 'violates pre-holdout cutoff'}
    if needles[kind] not in diagnostic:
        return False, f'refused for unexpected reason: {diagnostic[-400:]}'
    return True, 'refused as intended: ' + needles[kind]


def self_test() -> None:
    sources_preflight()
    cases = scenario_set()
    assert len(cases) >= 6
    for s in cases:
        data = pack_independent(s.digits)
        assert len(data) == (len(s.digits) + 1) // 2
        assert 0 < len(expected_rows(s)) < 100
    # The prefix fixture is meaningful because the full stream has a planted
    # final P1 while the 332-digit prefix does not contain that entire event.
    full = cases[1]
    prefix = cases[-1]
    assert full.digits == prefix.digits
    assert any(x[1] == 'P1' and x[2] == 325 for x in expected_rows(full))
    assert not any(x[1] == 'P1' and x[2] == 325 for x in expected_rows(prefix))
    print('Q2 HARNESS SELF-TEST PASS: source code identity, fixture construction, '
          'oracle baseline projection, EOF cutoff and known-prefix packaging. '
          'No file created; no historical scanner executed.')


def run_all() -> int:
    if os.name != 'nt':
        raise ValueError('production Q2 comparison is intended for the owner\'s Windows Ryzen host')
    self_test()
    before = result_root_fingerprint()
    failures = []
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q2_ONLY_') as tmp:
        root = Path(tmp)
        # System temp must never be a child of either the REAL output root or
        # the published digits root. No input is read from either data root.
        if str(root).casefold().startswith(str(REAL_RESULTS_ROOT.parent).casefold()):
            raise ValueError('Windows TEMP unexpectedly points inside OUTLANDISH large_artifacts')
        for case in scenario_set():
            ok, details = check_one(case, root)
            print(f'{"PASS" if ok else "Q2 FINDING"}: {case.name}: {details}', flush=True)
            if not ok:
                failures.append(case.name)
        for name in ('invalid_bcd', 'wrong_full_sha', 'cutoff_draw_refusal'):
            ok, details = negative_canary(name, root)
            print(f'{"PASS" if ok else "Q2 FINDING"}: canary_{name}: {details}', flush=True)
            if not ok:
                failures.append('canary_' + name)
    after = result_root_fingerprint()
    if after != before:
        print('Q2 FAIL: REAL result directory contents/metadata changed; investigate immediately')
        return 2
    print('REAL RESULTS ISOLATION PASS: directory listing/metadata unchanged')
    if failures:
        print(f'Q2 FINDINGS ({len(failures)}): {", ".join(failures)}')
        print('The unchanged historical scanner is NOT qualified. Retain its source and '
              'old scientific outputs; review each discrepancy before Q3.')
        return 1
    print('Q2 LEGACY COMPARISON PASS: synthetic exact event tuples, EOF and refusal canaries')
    print('This is not a full Q2 PASS until other required mutations/fixtures are reviewed.')
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--self-test', action='store_true', help='small read-only harness/fixture checks')
    mode.add_argument('--run', action='store_true', help='run unchanged old scanner only on disposable test inputs')
    a = p.parse_args()
    try:
        if a.self_test:
            self_test()
            return 0
        return run_all()
    except (OSError, ValueError, AssertionError, subprocess.TimeoutExpired,
            json.JSONDecodeError, csv.Error) as exc:
        print(f'Q2 HARNESS STOP: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
