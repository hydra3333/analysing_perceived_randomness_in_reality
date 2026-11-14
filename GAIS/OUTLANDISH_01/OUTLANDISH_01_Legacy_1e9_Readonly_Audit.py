#!/usr/bin/env python3
"""Read-only audit before possible OUTLANDISH_01 legacy 10^9 retirement.

Inspects exactly six byte-per-digit legacy binaries, and checks that current
outlandish.local.toml still references them. No writes, moves or deletions.
Optional --full-hash reads about 6 GB. Do not retire until Q1 is resolved.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import tomllib
from pathlib import Path

EXPECTED = {
    'pi': ('digits_pi_10_to_9.bin', '2e633867ad0ed7d866bcc0b3defc29b7704d0808cf62bba1dee1935fc357316e'),
    'phi': ('digits_golden_ratio_10_to_9.bin', '6be7059e971a6c710074682bfac76d415d1eff32c310bdb32c3c91283238d6d8'),
    'e': ('digits_e_10_to_9.bin', '7371fbff9ebde7fc7eb6009ce1137c8ab865d4fcf03d8231d3a22a74afd56b29'),
    'log2': ('digits_log2_10_to_9.bin', 'a9e86102914d564077c6fefcafc90dc27e9cad11af2bbc3159afebe1e4574f35'),
    'gamma': ('digits_gamma_10_to_9.bin', '82a1ed270f9494fb01d214b1e34156d29f0b1d62b3c586d87740ea80302d919a'),
    'lemniscate': ('digits_lemniscate_10_to_9.bin', 'a2482f77c7eccd54e9878317e88e4d9177f20b1e91eb07c377d36668a3973be6'),
}
SIZE = 1_000_000_000


def full_digest(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            buf = f.read(8 * 1024 * 1024)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--digits-dir', type=Path, default=Path(r'G:\OUTLANDISH_01\large_artifacts\digits'))
    parser.add_argument('--toml', type=Path, required=True,
                        help='actual checked-out GAIS/OUTLANDISH_01/outlandish.local.toml')
    parser.add_argument('--full-hash', action='store_true', help='read and hash all six 1GB files')
    a = parser.parse_args()
    try:
        raw = a.toml.read_bytes()
        cfg = tomllib.loads(raw.decode('utf-8-sig'))
        state = cfg['state']['active']
    except (OSError, ValueError, KeyError, UnicodeError) as exc:
        print('REGISTRY ERROR:', exc)
        return 2
    report = {
        'read_only': True,
        'physical_deletion_authorised': False,
        'toml_path': str(a.toml),
        'toml_sha256': hashlib.sha256(raw).hexdigest(),
        'digits_dir': str(a.digits_dir),
        'full_hash_requested': a.full_hash,
        'entries': [],
    }
    errors = []
    for constant, (filename, expected_sha) in EXPECTED.items():
        path = a.digits_dir / filename
        rec = {'constant': constant, 'filename': filename, 'expected_size': SIZE,
               'expected_sha256_from_legacy_registry': expected_sha}
        active = state.get(constant)
        rec['registry_still_active'] = (
            isinstance(active, dict) and active.get('file') == filename
            and active.get('digits') == SIZE and active.get('sha256') == expected_sha
        )
        if not rec['registry_still_active']:
            errors.append(f'legacy TOML state differs: {constant}')
        try:
            if path.is_symlink() or not path.is_file():
                raise ValueError('not an ordinary non-symlink file')
            rec['actual_size'] = path.stat().st_size
            if rec['actual_size'] != SIZE:
                raise ValueError('wrong file size')
            if a.full_hash:
                rec['actual_sha256'] = full_digest(path)
                if rec['actual_sha256'].lower() != expected_sha:
                    raise ValueError('hash mismatch')
            rec['file_check'] = 'PASS' if a.full_hash else 'SIZE_ONLY'
        except (OSError, ValueError) as exc:
            rec['file_check'] = 'FAIL: ' + str(exc)
            errors.append(f'{constant}: {exc}')
        report['entries'].append(rec)
    report['status'] = 'FAIL' if errors else ('HASHED_PASS' if a.full_hash else 'INVENTORY_PASS_HASH_PENDING')
    report['errors'] = errors
    print(json.dumps(report, indent=2))
    print('\nNO FILES OR REGISTRY STATE WERE MODIFIED.')
    print('Physical cleanup remains gated by saved-event Q1 reconciliation and a separate reviewed registry migration.')
    return 2 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
