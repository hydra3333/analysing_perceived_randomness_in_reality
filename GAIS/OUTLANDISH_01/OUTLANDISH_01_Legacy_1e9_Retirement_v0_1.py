#!/usr/bin/env python3
"""Strict, two-phase retirement of six known OUTLANDISH_01 legacy 1e9 byte binaries.

Run from the Ryzen repository with the project's Python, not on the i5.
DEFAULT is read-only PREVIEW. --deactivate archives the exact old registry and
verification record then atomically clears only legacy generated state.
--delete, separately, removes ONLY the six old 1GB paths once the registry is
empty, archive verified, and each surviving old binary rehashed.

The v0.2 byte-per-digit registry MUST NOT be pointed at new packed BCD files.
Author: ChatGPT implementation aid, NOT a replacement for owner-ratified v0.2.
No wildcard deletion; no modification of new packed binaries, receipts, CSVs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

import outlandish_config as cfgmod
from OUTLANDISH_01_Q1_Reconcile_Saved_Phi_Events import parse_evidence, compare

LEGACY = {
    'pi': ('digits_pi_10_to_9.bin', '2e633867ad0ed7d866bcc0b3defc29b7704d0808cf62bba1dee1935fc357316e'),
    'phi': ('digits_golden_ratio_10_to_9.bin', '6be7059e971a6c710074682bfac76d415d1eff32c310bdb32c3c91283238d6d8'),
    'e': ('digits_e_10_to_9.bin', '7371fbff9ebde7fc7eb6009ce1137c8ab865d4fcf03d8231d3a22a74afd56b29'),
    'log2': ('digits_log2_10_to_9.bin', 'a9e86102914d564077c6fefcafc90dc27e9cad11af2bbc3159afebe1e4574f35'),
    'gamma': ('digits_gamma_10_to_9.bin', '82a1ed270f9494fb01d214b1e34156d29f0b1d62b3c586d87740ea80302d919a'),
    'lemniscate': ('digits_lemniscate_10_to_9.bin', 'a2482f77c7eccd54e9878317e88e4d9177f20b1e91eb07c377d36668a3973be6'),
}
PACKED = {
    'pi': ('digits_pi_10_to_10.packed.bin', '62ab5b9a511eb0fcf5d09717df9ee51f8bd29ea09acf379e6f1045c537ababe2'),
    'phi': ('digits_golden_ratio_10_to_10.packed.bin', 'dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d'),
    'e': ('digits_e_10_to_10.packed.bin', '522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f'),
    'log2': ('digits_log2_10_to_10.packed.bin', '6993b8b6c6f46ae13b5e213aae0d46e784c8acae510f10e6862aecde83a15694'),
    'gamma': ('digits_gamma_10_to_10.packed.bin', '68e4a47d27759632dd8c608af973fa5bd22fb2aa7290d5e92f59e485ceb85e6a'),
    'lemniscate': ('digits_lemniscate_10_to_10.packed.bin', '958210dcda823fd1951b8487fbfe3cb98aeda9748c2b0dea4db9684608d21369'),
}
LEGACY_SIZE = 1_000_000_000
PACKED_SIZE = 5_000_000_000
CONFIG_SHA_BEFORE = '1718ab895a0479d437ac1f376585a3aea6cb864b722d96d2487ad21ac4236fe5'
PHI_CSV_OLD_SHA = 'c067b95d7171ca4669724985842e153e747c18adf255cafbe76d5512d564b580'
PHI_CSV_NEW_SHA = '7a4315d66b028a2664413f0b3017714c10653110a1d79af7102d8ea09bbb5c83'
OLD_CSV_REL = Path('OUTLANDISH_01_results/run_20261105_231343/digits_golden_ratio_10_to_9_matches.csv')
NEW_CSV_ABS = Path(r'G:\OUTLANDISH_01\large_artifacts\results\packed_run_20261108T012705Z_43564c3c\matches.csv')


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            chunk = f.read(8 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def regular_file(path: Path, size: int | None = None) -> None:
    cfgmod._validate_ancestors(path)  # rejects symlink/junction in the tree
    if not path.is_file() or cfgmod._unsafe_link(path):
        raise ValueError(f'NOT a safe ordinary file: {path}')
    if size is not None and path.stat().st_size != size:
        raise ValueError(f'wrong size: {path}, got {path.stat().st_size}, expected {size}')


def environment() -> tuple[cfgmod.Config, Path]:
    if os.name != 'nt':
        raise ValueError('Windows host required for production action')
    c = cfgmod.load_config()
    if str(c.root).casefold().rstrip('\\/') != r'G:\OUTLANDISH_01'.casefold():
        raise ValueError(f'unexpected configured workspace root: {c.root}')
    expected = Path(r'G:\OUTLANDISH_01\large_artifacts\digits')
    if str(c.path('digits')).casefold() != str(expected).casefold():
        raise ValueError(f'unexpected digits directory: {c.path("digits")}')
    if c.pending:
        raise ValueError(f'pending retirement records exist: {sorted(c.pending)}; manual review required')
    return c, expected


def q1_gate() -> dict:
    old = parse_evidence(cfgmod.WORKSPACE / OLD_CSV_REL)
    new = parse_evidence(NEW_CSV_ABS)
    if old.sha256 != PHI_CSV_OLD_SHA or new.sha256 != PHI_CSV_NEW_SHA:
        raise ValueError('Q1 saved CSV hash has changed since PASS; refuse')
    result = compare(old, new)
    if result['status'] != 'PASS' or any(x['status'] != 'PASS' for x in result['comparisons']):
        raise ValueError('Q1 exact comparison has failed or is incomplete; refuse')
    return {'status': 'PASS', 'legacy_csv_sha256': old.sha256, 'packed_csv_sha256': new.sha256,
            'comparisons': len(result['comparisons'])}


def verify_packed(digits: Path) -> None:
    for const, (name, expected_sha) in PACKED.items():
        p = digits / name
        regular_file(p, PACKED_SIZE)
        receipt = p.with_name(name + '.wsl-receipt.json')
        regular_file(receipt)
        doc = json.loads(receipt.read_text(encoding='utf-8-sig'))
        checks = (
            doc.get('format') == 'OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1',
            doc.get('format_version') == 1,
            doc.get('scope') == 'PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY',
            doc.get('constant') in (const, 'golden_ratio' if const == 'phi' else const),
            doc.get('digits_including_integer') == 10_000_000_000,
            doc.get('packed_bytes') == PACKED_SIZE,
            doc.get('binary_name') == name,
            doc.get('binary_sha256_streamed') == expected_sha,
        )
        if not all(checks):
            raise ValueError(f'packed receipt identity mismatch for {p}')
        print(f'PACKED REFERENCE PASS {const}: {name} ({expected_sha})')
    print('Packed sizes/receipts matched known identity; not rehashed during cleanup.')


def verify_legacy(digits: Path, *, hash_all: bool) -> dict:
    output = {}
    for const, (name, expected_sha) in LEGACY.items():
        p = digits / name
        regular_file(p, LEGACY_SIZE)
        if hash_all:
            actual = sha_file(p)
            if actual != expected_sha:
                raise ValueError(f'LEGACY HASH MISMATCH: {p}: {actual}')
            print(f'LEGACY SHA PASS {const}: {name}')
        else:
            print(f'LEGACY PRESENT {const}: {name} (1,000,000,000 bytes; not rehashed in preview)')
        output[const] = {'file': name, 'bytes': LEGACY_SIZE, 'sha256': expected_sha}
    return output


def check_old_state(c: cfgmod.Config) -> None:
    if set(c.active) != set(LEGACY):
        raise ValueError('registry active keys differ from six expected old entries')
    for const, (name, expected_sha) in LEGACY.items():
        v = c.active[const]
        if (v.get('file'), v.get('digits'), v.get('sha256')) != (name, LEGACY_SIZE, expected_sha):
            raise ValueError(f'unexpected registry record: {const}')
    if sha_bytes(cfgmod.CONFIG_FILE.read_bytes()) != CONFIG_SHA_BEFORE:
        raise ValueError('TOML differs from the 14 Nov full-hash audit; rerun review')


def write_new(path: Path, data: bytes) -> None:
    with path.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def archive_and_deactivate(c: cfgmod.Config, digits: Path) -> None:
    if not c.retention.get('delete_superseded'):
        raise ValueError('settings.retention.delete_superseded is disabled')
    with cfgmod.exclusive_lock():
        c, digits = environment()
        check_old_state(c)
        q1 = q1_gate()
        verify_packed(digits)
        verified = verify_legacy(digits, hash_all=True)
        previous = cfgmod.CONFIG_FILE.read_bytes()
        folder = c.path('logs', create=True) / ('legacy_1e9_retirement_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        folder.mkdir(exist_ok=False)
        write_new(folder / 'old_registry_exact.toml', previous)
        report = {'format': 'OUTLANDISH_LEGACY_1E9_RETIREMENT_V1',
                  'archived_config_sha256': sha_bytes(previous), 'old_files': verified,
                  'packed_files': PACKED, 'q1': q1, 'deactivation_planned': True}
        write_new(folder / 'retirement_evidence.json', (json.dumps(report, indent=2, sort_keys=True) + '\n').encode())
        cfgmod.save_generated_state({}, {})  # backed up as outlandish.local.toml.bak, atomic
        new_c = cfgmod.load_config()
        if new_c.active or new_c.pending:
            raise ValueError('post-deactivation registry unexpectedly not empty')
        print(f'DEACTIVATED: six legacy active records. Old 6GB files remain.')
        print(f'ARCHIVE: {folder}')
        print('NEXT (after checking archive and empty legacy registry):')
        print(f'"{sys.executable}" "{Path(__file__).resolve()}" --delete --manifest "{folder / "retirement_evidence.json"}" --confirm-idle')


def validate_manifest(manifest: Path, c: cfgmod.Config) -> dict:
    expected_logs = c.path('logs')
    cfgmod._validate_ancestors(manifest)
    if manifest.name != 'retirement_evidence.json' or not manifest.parent.name.startswith('legacy_1e9_retirement_'):
        raise ValueError('unexpected manifest basename')
    if manifest.parent.parent != expected_logs:
        raise ValueError(f'manifest is not under the configured logs root: {manifest}')
    regular_file(manifest)
    evidence = json.loads(manifest.read_text(encoding='utf-8'))
    if (evidence.get('format') != 'OUTLANDISH_LEGACY_1E9_RETIREMENT_V1'
            or evidence.get('archived_config_sha256') != CONFIG_SHA_BEFORE):
        raise ValueError('manifest does not match the previously approved registry')
    backup = manifest.parent / 'old_registry_exact.toml'
    regular_file(backup)
    if sha_file(backup) != CONFIG_SHA_BEFORE:
        raise ValueError('archived original registry hash invalid')
    if {k: (v['file'],v['sha256']) for k,v in evidence['old_files'].items()} != LEGACY:
        raise ValueError('manifest old filenames or hashes differ')
    if evidence.get('q1',{}).get('status') != 'PASS':
        raise ValueError('manifest Q1 evidence did not pass')
    return evidence


def delete_legacy(c: cfgmod.Config, digits: Path, manifest: Path) -> None:
    with cfgmod.exclusive_lock():
        c, digits = environment()
        if c.active or c.pending:
            raise ValueError('registry still has active/pending records; refuse physical deletion')
        validate_manifest(manifest, c)
        # All still-present sources are verified BEFORE the first unlink. An already
        # missing name is accepted only for recovery after a partly completed delete.
        existing=[]
        for const,(name,expected_sha) in LEGACY.items():
            path=digits/name
            if not path.exists() and not cfgmod._unsafe_link(path):
                print(f'ALREADY ABSENT (possible prior partial cleanup): {path}')
                continue
            regular_file(path,LEGACY_SIZE)
            digest=sha_file(path)
            if digest!=expected_sha:
                raise ValueError(f'aborting ALL deletion; old binary digest mismatch: {path}')
            existing.append((const,path))
            print(f'RECHECK PASS {const}: {path}')
        verify_packed(digits)
        for const,path in existing:
            path.unlink()
            print(f'DELETED {const}: {path}')
        print('DELETE COMPLETE: six known numeric-byte legacy files absent. Packed files untouched.')


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument('--deactivate', action='store_true', help='archive+atomically clear legacy active registry; does not delete binaries')
    mode.add_argument('--delete', action='store_true', help='delete exactly six legacy files after deactivation')
    p.add_argument('--manifest', type=Path, help='evidence JSON printed by --deactivate; required for --delete')
    p.add_argument('--confirm-idle', action='store_true', help='assert no scanner/generator is using old files')
    a = p.parse_args()
    if a.deactivate or a.delete:
        if not a.confirm_idle:
            p.error('--confirm-idle required for any mutation')
    if a.delete and a.manifest is None:
        p.error('--manifest required for --delete')
    if a.manifest and not a.delete:
        p.error('--manifest only applies to --delete')
    try:
        c, digits = environment()
        if a.delete:
            delete_legacy(c, digits, a.manifest)
        elif a.deactivate:
            archive_and_deactivate(c, digits)
        else:
            check_old_state(c)
            print('PREVIEW ONLY; no state or files will change.')
            q1 = q1_gate()
            print('Q1 saved-event matching:', q1['status'])
            verify_packed(digits)
            verify_legacy(digits, hash_all=False)
            print('PREVIEW PASS: archive+deactivate registry, THEN separate hash-checked deletion.')
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'REFUSED: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
