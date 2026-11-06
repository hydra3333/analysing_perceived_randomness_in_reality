#!/usr/bin/env python3
"""OUTLANDISH_01 v0.2 storage policy, audits and verified active-digit registry.

Does not import/inspect the primary project's source_data or holdout. Scans
workspace filenames and metadata only; only an EXPLICIT registration operation
reads full numeric digit data. Never automatically deletes arbitrary files.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
from typing import Callable, TypeVar

from outlandish_config import (
    WORKSPACE, CONFIG_FILE, CONSTANTS, ConfigError, load_config, exclusive_lock,
    save_generated_state, now_utc, _unsafe_link, _validate_ancestors,
)

THRESHOLD = 10 * 1024 * 1024
THIRD_PARTY_EXCEPTION = 'y-cruncher v0.8.7.9547b'
_T = TypeVar('_T')
PREFIXES = {
    'pi': '31415926535897932384626433832795',
    'phi': '16180339887498948482045868343656',
    'e': '27182818284590452353602874713526',
    'log2': '06931471805599453094172321214581',
    'gamma': '05772156649015328606065120900824',
    'lemniscate': '26220575542921198104648395898911',
}
_DIGIT_NAME = re.compile(r'^(?:digits_(?:pi|golden_ratio|e|log2|gamma|lemniscate)_.+|(?:pi|phi|e|log2|gamma|lemniscate)_.+)\.bin$', re.I)


class ArtifactPolicyError(ConfigError):
    pass


@dataclass(frozen=True)
class Violation:
    path: Path
    size: int
    reason: str

    def describe(self) -> str:
        return f'{self.reason}: {self.path} ({self.size:,} bytes)'


def is_inside(path: Path, parent: Path) -> bool:
    try:
        Path(os.path.abspath(path)).relative_to(Path(os.path.abspath(parent)))
        return True
    except ValueError:
        return False


def require_artifact_path(path: Path) -> Path:
    cfg = load_config()
    root = cfg.path('artifacts')
    p = Path(os.path.abspath(os.fspath(path)))
    if not is_inside(p, root) or p == root:
        raise ArtifactPolicyError(f'generated file must be beneath {root}: {path}')
    _validate_ancestors(p)
    return p


def artifact_directory(kind: str, *, create: bool = False) -> Path:
    return load_config().path(kind, create=create)


def new_artifact_directory(kind: str) -> Path:
    return artifact_directory(kind, create=True)


def digit_path(name: str) -> Path:
    cfg = load_config()
    return cfg.digit_file(name)


def resolve_digit_argument(path: Path) -> Path:
    if path.parent == Path('.'):
        return require_artifact_path(digit_path(path.name))
    return require_artifact_path(path)


def active_digit_file(constant: str, min_digits: int = 0) -> tuple[Path, dict]:
    cfg = load_config()
    if constant not in cfg.active:
        raise ArtifactPolicyError(f'no verified active binary for {constant}; explicitly register one')
    record = cfg.active[constant]
    if record['digits'] < min_digits:
        raise ArtifactPolicyError(f'{constant} has only {record["digits"]:,} verified digits; requested {min_digits:,}')
    path = cfg.digit_file(record['file'], require_existing=True)
    if path.stat().st_size != record['digits']:
        raise ArtifactPolicyError(f'{constant} active binary length no longer matches TOML: {path}')
    return path, record


def _reason(path: Path, rel: Path, size: int) -> str | None:
    if rel.parts == ('Pi - Dec - Chudnovsky.txt',) and size <= 2_000_000:
        return None  # The tracked historical fixture is intentionally retained.
    if path.suffix.lower() == '.bin':
        return 'generated/retained .bin outside configured artifact root'
    if path.name.startswith(('.outlandish_build_', '.preholdout_', '.outlandish_migrate_')) and path.suffix == '.tmp':
        return 'abandoned temporary output'
    if rel.parts and rel.parts[0] == 'ycruncher_digits':
        if path.suffix.lower() in ('.ycd', '.dat', '.swap', '.tmp'):
            return 'legacy calculation scratch'
        if (path.suffix.lower() == '.txt' and
                any(re.match(r'.+_\d+_digits$', ancestor.name) and
                    size == int(ancestor.name.split('_')[-2]) + 1 for ancestor in rel.parents)):
            return 'legacy decimal digit text'
    if size >= THRESHOLD:
        return f'file >= {THRESHOLD:,} bytes outside artifact root'
    return None


def _scan_tree(base: Path, *, artifact_skip: Path | None = None, workspace: bool = False) -> list[Violation]:
    found: list[Violation] = []
    if not base.exists():
        return found
    if not base.is_dir() or _unsafe_link(base):
        return [Violation(base, 0, 'invalid root or link/junction')]
    for parent, dirs, files in os.walk(base, topdown=True, followlinks=False):
        folder = Path(parent)
        kept = []
        for name in dirs:
            candidate = folder / name
            if artifact_skip is not None and candidate == artifact_skip:
                if _unsafe_link(candidate):
                    found.append(Violation(candidate, 0, 'artifact root is a link/junction'))
                continue
            if workspace and folder == WORKSPACE and name == THIRD_PARTY_EXCEPTION:
                continue
            if _unsafe_link(candidate):
                found.append(Violation(candidate, 0, 'directory link/junction'))
            else:
                kept.append(name)
        dirs[:] = kept
        for name in files:
            candidate = folder / name
            if _unsafe_link(candidate):
                found.append(Violation(candidate, 0, 'file link/junction'))
                continue
            try:
                info = candidate.lstat()
            except FileNotFoundError:
                found.append(Violation(candidate, 0, 'vanished during metadata scan'))
                continue
            if not stat.S_ISREG(info.st_mode):
                found.append(Violation(candidate, 0, 'nonregular file'))
                continue
            why = _reason(candidate, candidate.relative_to(base), info.st_size)
            if why:
                found.append(Violation(candidate, info.st_size, why))
    return found


def audit_workspace() -> list[Violation]:
    cfg = load_config()
    root = cfg.path('main')
    artifacts = cfg.path('artifacts')
    if not root.anchor or not Path(root.anchor).exists():
        raise ArtifactPolicyError(f'configured drive is unavailable: {root.anchor}')
    if is_inside(root, WORKSPACE) or is_inside(WORKSPACE, root):
        raise ArtifactPolicyError('configured external storage must not overlap repository workspace')
    failures = _scan_tree(WORKSPACE, workspace=True)
    failures += _scan_tree(root, artifact_skip=artifacts)
    if artifacts.exists() and (_unsafe_link(artifacts) or not artifacts.is_dir()):
        failures.append(Violation(artifacts, 0, 'artifact root invalid/link/junction'))
    elif artifacts.is_dir():
        # Do not read file contents or classify sizes within allowed storage,
        # but do reject links/junctions and non-regular files anywhere inside.
        for parent, dirs, files in os.walk(artifacts, topdown=True, followlinks=False):
            folder = Path(parent)
            safe_dirs = []
            for name in dirs:
                candidate = folder / name
                if _unsafe_link(candidate):
                    failures.append(Violation(candidate, 0, 'link/junction in artifact area'))
                else:
                    safe_dirs.append(name)
            dirs[:] = safe_dirs
            for name in files:
                candidate = folder / name
                if _unsafe_link(candidate) or not candidate.is_file():
                    failures.append(Violation(candidate, 0, 'linked or non-regular artifact file'))
    for kind in ('digits', 'scratch', 'staging', 'results', 'logs'):
        sub = cfg.path(kind)
        if sub.exists() and (_unsafe_link(sub) or not sub.is_dir()):
            failures.append(Violation(sub, 0, 'configured subdirectory invalid/link/junction'))
    return sorted(failures, key=lambda item: str(item.path).casefold())


def _report(failures: list[Violation], phase: str) -> None:
    if failures:
        print(f'ARTIFACT SAFETY STOP ({phase}): {len(failures)} misplaced/unsafe entries', file=sys.stderr)
        for item in failures:
            print('  ' + item.describe(), file=sys.stderr)
    else:
        print(f'ARTIFACT AUDIT PASS ({phase}): no misplaced generated/large files', flush=True)


def require_clean(phase: str) -> None:
    findings = audit_workspace()
    _report(findings, phase)
    if findings:
        raise ArtifactPolicyError('workspace artifact audit failed')


def guarded_call(call: Callable[[], _T], *, hold_lock: bool = False) -> _T:
    """For scanning, hold the registry lock throughout so retire cannot unlink inputs."""
    if hold_lock:
        with exclusive_lock():
            return guarded_call(call)
    require_clean('preflight')
    try:
        return call()
    finally:
        failed = sys.exc_info()[0] is not None
        findings = audit_workspace()
        _report(findings, 'post-run / error-path' if failed else 'post-run')
        if findings and not failed:
            raise ArtifactPolicyError('post-run artifact audit failed')


def inventory_sources() -> int:
    known = {'outlandish_config.py', 'outlandish_artifacts.py', 'outlandish_big_constants.py',
             'outlandish_powerball_stage_a.py', 'generate_1e10.cmd', 'scan_1e10.cmd',
             'scan_1e9.cmd', 'test_artifact_safeguards.py', 'test_outlandish_v02.py'}
    ext = {'.py', '.cmd', '.bat', '.sh', '.ps1'}
    found = archival = unknown = 0
    for base, dirs, files in os.walk(WORKSPACE, topdown=True, followlinks=False):
        folder = Path(base)
        dirs[:] = [d for d in dirs if not _unsafe_link(folder / d)
                   and not (folder == WORKSPACE and d == THIRD_PARTY_EXCEPTION)
                   and d != '__pycache__']
        for name in sorted(files):
            rel = (folder / name).relative_to(WORKSPACE)
            if rel.suffix.lower() not in ext:
                continue
            found += 1
            if len(rel.parts) > 1 and rel.parts[0].casefold() == 'archive':
                archival += 1
                print(f'ARCHIVED-ENTRY {rel} -- historical, do not execute')
            elif len(rel.parts) == 1 and name in known:
                print(f'EXPECTED-ENTRY-NAME {rel} (source hash must match package manifest)')
            else:
                unknown += 1
                print(f'UNREVIEWED-ENTRY {rel} -- review before treating installation as complete')
    print(f'PROGRAM INVENTORY: {found} entries; {archival} archived; {unknown} unreviewed.')
    return 2 if unknown else 0


def _digest(path: Path, prefix: bytes | None = None) -> str:
    sha = hashlib.sha256()
    n = 0
    with path.open('rb') as f:
        while part := f.read(4 * 1024 * 1024):
            if prefix is not None:
                if n < len(prefix) and part[:len(prefix)-n] != prefix[n:n+len(part)]:
                    raise ArtifactPolicyError(f'known constant prefix mismatch: {path}')
                if max(part, default=0) > 9:
                    raise ArtifactPolicyError(f'non-digit numeric byte near offset {n:,}: {path}')
            sha.update(part)
            n += len(part)
    return sha.hexdigest()


def _compare_prefix(longer: Path, shorter: Path) -> None:
    with longer.open('rb') as a, shorter.open('rb') as b:
        while small := b.read(4 * 1024 * 1024):
            if a.read(len(small)) != small:
                raise ArtifactPolicyError(f'new file differs from existing verified active prefix: {shorter}')


def _candidate_valid(path: Path, constant: str, digits: int) -> str:
    if not path.is_file() or _unsafe_link(path) or path.stat().st_size != digits:
        raise ArtifactPolicyError(f'invalid/missing binary or length mismatch: {path}')
    if digits < 32:
        raise ArtifactPolicyError('at least 32 digits required for known-prefix check')
    _validate_ancestors(path)
    return _digest(path, bytes(int(ch) for ch in PREFIXES[constant]))


def promote_verified(constant: str, file: Path, digits: int, sha256: str) -> None:
    """Verify and publish a larger active file, then optionally retire its predecessor.

    Promotion occurs under the shared lock. When retention enables automatic
    deletion, the *already fully verified* former active file is unlinked only
    AFTER the new registry state has been atomically published. The active file
    is never a deletion target. An auto-retirement failure is nonfatal to an
    otherwise successful promotion; the pending record is retained for manual
    retirement/recovery. This protects a complete candidate from being treated
    as a failed generation merely because predecessor cleanup had an issue.
    """
    with exclusive_lock():
        cfg = load_config()
        if constant not in CONSTANTS:
            raise ArtifactPolicyError(f'unknown constant: {constant}')
        if cfg.pending.get(constant):
            raise ArtifactPolicyError(f'{constant} has unresolved pending retirement; resolve it first')
        candidate = cfg.digit_file(file.name, require_existing=True)
        if Path(os.path.abspath(file)) != Path(os.path.abspath(candidate)):
            raise ArtifactPolicyError(f'candidate must be in configured digits directory: {file}')
        verified_hash = _candidate_valid(candidate, constant, digits)
        if verified_hash != sha256:
            raise ArtifactPolicyError('candidate SHA-256 changed before promotion')
        prior = cfg.active.get(constant)
        old = None
        if prior is not None:
            if digits <= prior['digits']:
                raise ArtifactPolicyError('replacement must be strictly longer than current verified active')
            old = cfg.digit_file(prior['file'], require_existing=True)
            if old == candidate:
                raise ArtifactPolicyError('candidate is the previously active file')
            if _candidate_valid(old, constant, prior['digits']) != prior['sha256']:
                raise ArtifactPolicyError('existing active binary fails independent re-verification')
            _compare_prefix(candidate, old)
        active = dict(cfg.active)
        pending = dict(cfg.pending)
        active[constant] = {'file': file.name, 'digits': digits, 'sha256': sha256,
                            'verified_utc': now_utc()}
        if prior:
            pending[constant] = prior
        save_generated_state(active, pending)
        print(f'PROMOTED {constant}: {digits:,} digits, {file.name}, SHA-256 {sha256}', flush=True)
        if prior:
            if not cfg.retention['delete_superseded']:
                print(f'PENDING RETIREMENT {constant}: {prior["file"]}; '
                      'automatic deletion disabled in TOML', flush=True)
            else:
                # All candidate/prior content checks above ran with the same
                # exclusive lock held. Reconfirm the published identity and
                # path safety without re-reading enormous already-verified files.
                try:
                    current = load_config()
                    if (current.active.get(constant) != active[constant] or
                            current.pending.get(constant) != prior):
                        raise ArtifactPolicyError('registry changed after publication')
                    if (old is None or _unsafe_link(old) or not old.is_file() or
                            old.stat().st_size != prior['digits'] or
                            _unsafe_link(candidate) or not candidate.is_file() or
                            candidate.stat().st_size != digits):
                        raise ArtifactPolicyError('predecessor/successor path changed after verification')
                    # Crash here leaves pending_retirement referring to the
                    # missing file. The existing recover-retirement command
                    # safely clears that marker after checking active SHA.
                    old.unlink()
                    remaining = dict(current.pending)
                    del remaining[constant]
                    save_generated_state(dict(current.active), remaining)
                except Exception as exc:
                    print(f'WARNING: {constant} promoted, but AUTO-RETIRE incomplete '
                          f'for {prior["file"]}: {exc}. Check status; if the old '
                          'file still exists use retire, otherwise preview '
                          'recover-retirement. The new active binary is retained.',
                          file=sys.stderr, flush=True)
                else:
                    print(f'AUTO-RETIRED {constant}: removed superseded '
                          f'{old.name} ({prior["digits"]:,} bytes); '
                          'active successor preserved', flush=True)


def import_verified(constant: str, source: Path, digits: int, expected_sha256: str, apply: bool,
                    confirm_idle: bool, delete_source: bool) -> None:
    if constant not in CONSTANTS:
        raise ArtifactPolicyError('unknown constant')
    cfg = load_config()
    src = Path(os.path.abspath(source))
    if (not is_inside(src, WORKSPACE) and not is_inside(src, cfg.path('artifacts'))):
        raise ArtifactPolicyError('import source must be inside OUTLANDISH workspace or configured artifact root')
    _validate_ancestors(src)
    if not src.is_file() or _unsafe_link(src) or not src.name.endswith('.bin'):
        raise ArtifactPolicyError(f'invalid input binary: {src}')
    if src.stat().st_size != digits:
        raise ArtifactPolicyError('provided digit count differs from source size')
    dest = cfg.digit_file(src.name)
    if not apply:
        print(f'IMPORT PREVIEW: {constant}, {digits:,} bytes, {src} -> {dest}')
        print('No content read, copied, registered or deleted during preview.')
        return
    if not confirm_idle:
        raise ArtifactPolicyError('--apply requires --confirm-idle')
    # Check content and an independently supplied, prior verified SHA receipt.
    if not re.fullmatch(r'[0-9a-f]{64}', expected_sha256):
        raise ArtifactPolicyError('expected SHA-256 must be 64 lowercase hexadecimal digits')
    sha = _candidate_valid(src, constant, digits)
    if sha != expected_sha256:
        raise ArtifactPolicyError('source does not match the independent expected SHA-256 receipt')
    if src != dest:
        cfg.path('digits', create=True)
        cfg.path('staging', create=True)
        if dest.exists() or _unsafe_link(dest):
            # Recovery from an interrupted copy/promotion: reuse only a fully
            # reverified, byte-identical existing destination; never overwrite.
            if _candidate_valid(dest, constant, digits) != sha:
                raise FileExistsError(f'existing destination differs, non-overwrite: {dest}')
            print(f'REUSE VERIFIED EXISTING DESTINATION (recovery): {dest}')
        else:
            staged = None
            try:
                with tempfile.NamedTemporaryFile(dir=cfg.path('staging'), prefix='.import_', suffix='.tmp', delete=False) as f:
                    staged = Path(f.name)
                    with src.open('rb') as input_file:
                        shutil.copyfileobj(input_file, f, 4 * 1024 * 1024)
                    f.flush()
                    os.fsync(f.fileno())
                if _candidate_valid(staged, constant, digits) != sha or _candidate_valid(src, constant, digits) != sha:
                    raise ArtifactPolicyError('source/copy mismatch or source changed during import')
                # Same-volume create-only, atomic publication; never overwrite.
                os.link(staged, dest)
            finally:
                if staged is not None and staged.exists():
                    staged.unlink()
    existing = load_config().active.get(constant)
    if existing is not None and (existing['file'], existing['digits'], existing['sha256']) == (dest.name, digits, sha):
        # Crash/retry after the active registry was already safely published,
        # but before an old E: source could be deleted.
        if _candidate_valid(dest, constant, digits) != sha:
            raise ArtifactPolicyError('previously active destination changed; cannot resume source cleanup')
        print(f'REGISTRY ALREADY PROMOTED (idempotent import recovery): {dest}')
    else:
        try:
            promote_verified(constant, dest, digits, sha)
        except Exception:
            # An unregistered complete dest is safe to retain for investigation/retry.
            print(f'PROMOTION REFUSED: input and copied candidate preserved at {dest}', file=sys.stderr)
            raise
    if src != dest and delete_source:
        # Recheck source after durable state publication, never before.
        if _candidate_valid(src, constant, digits) != sha:
            raise ArtifactPolicyError(f'source changed, refusing deletion: {src}')
        src.unlink()
        print(f'REMOVED VERIFIED IMPORT SOURCE {src}')
    elif src != dest:
        print(f'SOURCE RETAINED {src}; if it is a misplaced workspace .bin, the next audit will report it')


def retire(constant: str, apply: bool, confirm_idle: bool) -> None:
    if constant not in CONSTANTS:
        raise ArtifactPolicyError('unknown constant')
    if apply and not confirm_idle:
        raise ArtifactPolicyError('retirement requires --confirm-idle and --apply')
    with exclusive_lock():
        cfg = load_config()
        old = cfg.pending.get(constant)
        if not old:
            print(f'No pending retirement for {constant}')
            return
        if not cfg.retention['delete_superseded']:
            raise ArtifactPolicyError('retirement disabled in TOML settings')
        active_path, active = active_digit_file(constant)
        old_path = cfg.digit_file(old['file'], require_existing=True)
        if old_path == active_path:
            raise ArtifactPolicyError('refusing to retire active file')
        print(f'RETIRE {constant}: {old_path} ({old["digits"]:,} bytes)')
        if not apply:
            print('PREVIEW: no file or registry modified')
            return
        # Hash both active and prior and compare prefix before unlinking.
        if _candidate_valid(active_path, constant, active['digits']) != active['sha256']:
            raise ArtifactPolicyError('active verification failed; preserving predecessor')
        if _candidate_valid(old_path, constant, old['digits']) != old['sha256']:
            raise ArtifactPolicyError('old verification failed; preserving predecessor')
        _compare_prefix(active_path, old_path)
        # Persist retirement completion first: if power fails before unlink,
        # orphan stays on disk rather than losing the last active file.
        # To avoid unrecorded orphan on interrupted unlink, remove old first;
        # pending state still names missing old after crash and recovery can
        # clear it with inspect/clear-missing, not by guessing a replacement.
        old_path.unlink()
        pending = dict(cfg.pending)
        del pending[constant]
        save_generated_state(dict(cfg.active), pending)
        print(f'RETIRED {old_path}; active {active_path} intact')


def recover_missing_retirement(constant: str, apply: bool, confirm_idle: bool) -> None:
    # Recovery for power loss after unlink, before TOML state write. Never
    # invent a replacement; require the active file's complete verification.
    if apply and not confirm_idle:
        raise ArtifactPolicyError('recovery requires --confirm-idle')
    with exclusive_lock():
        cfg = load_config()
        old = cfg.pending.get(constant)
        if old is None:
            print(f'No pending retirement for {constant}')
            return
        old_path = cfg.digit_file(old['file'])
        if old_path.exists() or _unsafe_link(old_path):
            raise ArtifactPolicyError('old binary is still present; use retire, not recover-retirement')
        active = cfg.active[constant]
        active_path = cfg.digit_file(active['file'], require_existing=True)
        if _candidate_valid(active_path, constant, active['digits']) != active['sha256']:
            raise ArtifactPolicyError('active verification failed; cannot clear interrupted retirement')
        print(f'RECOVERY: {old_path.name} already missing; {active_path.name} independently verified')
        if not apply:
            print('PREVIEW: registry unchanged')
            return
        pending = dict(cfg.pending)
        del pending[constant]
        save_generated_state(dict(cfg.active), pending)
        print('RECOVERED: missing old file retirement marker cleared')


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest='command', required=True)
    for cmd in ('audit', 'inventory', 'status', 'validate', 'paths'):
        subs.add_parser(cmd)
    imp = subs.add_parser('register', help='explicit verified import and promote of a completed .bin')
    imp.add_argument('--constant', choices=CONSTANTS, required=True)
    imp.add_argument('--source', required=True, type=Path)
    imp.add_argument('--digits', type=int, required=True)
    imp.add_argument('--expected-sha256', required=True,
                     help='independently recorded digest from a prior verified run; mandatory')
    imp.add_argument('--apply', action='store_true')
    imp.add_argument('--confirm-idle', action='store_true')
    imp.add_argument('--delete-source', action='store_true', help='delete original only after verified durable promotion')
    ret = subs.add_parser('retire', help='review/delete an exclusively recorded superseded active binary')
    ret.add_argument('--constant', choices=CONSTANTS, required=True)
    ret.add_argument('--apply', action='store_true')
    ret.add_argument('--confirm-idle', action='store_true')
    recover = subs.add_parser('recover-retirement', help='recover after power loss following predecessor unlink')
    recover.add_argument('--constant', choices=CONSTANTS, required=True)
    recover.add_argument('--apply', action='store_true')
    recover.add_argument('--confirm-idle', action='store_true')
    args = p.parse_args(argv)
    if args.command == 'inventory':
        return inventory_sources()
    if args.command == 'validate':
        c = load_config()
        print(f'CONFIG PASS: {CONFIG_FILE}, main_root={c.root}; {len(c.active)} active constants')
        return 0
    if args.command == 'paths':
        c = load_config()
        for kind in ('main', 'artifacts', 'digits', 'scratch', 'staging', 'results', 'logs'):
            print(f'{kind}: {c.path(kind)}')
        return 0
    if args.command == 'audit':
        found = audit_workspace()
        _report(found, 'standalone audit')
        return 2 if found else 0
    if args.command == 'status':
        c = load_config()
        print(f'CONFIG {CONFIG_FILE} root={c.root}')
        for constant in CONSTANTS:
            a = c.active.get(constant)
            x = c.pending.get(constant)
            print(f'{constant}: active={a["file"] if a else "NONE"} '
                  f'digits={a["digits"] if a else "-"} '
                  f'pending_retire={x["file"] if x else "NONE"}')
        print('Status is metadata only; use register/retire for full binary verification.')
        return 0
    if args.command == 'register':
        if args.delete_source and not args.apply:
            p.error('--delete-source requires --apply')
        import_verified(args.constant, args.source, args.digits, args.expected_sha256, args.apply,
                        args.confirm_idle, args.delete_source)
        if args.apply:
            found = audit_workspace()
            _report(found, 'post-registration')
            return 2 if found else 0
        return 0
    if args.command == 'retire':
        retire(args.constant, args.apply, args.confirm_idle)
        if args.apply:
            found = audit_workspace()
            _report(found, 'post-retirement')
            return 2 if found else 0
        return 0
    if args.command == 'recover-retirement':
        recover_missing_retirement(args.constant, args.apply, args.confirm_idle)
        if args.apply:
            found = audit_workspace()
            _report(found, 'post-recovery')
            return 2 if found else 0
        return 0
    raise AssertionError(args.command)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(2)
