#!/usr/bin/env python3
"""OUTLANDISH_01 shared, metadata-only generated-artifact location policy.

The only workspace examined is the directory containing this module.  No data
contents, lottery draw fields, parent project files, or Git metadata are read.
Migration is explicitly opt-in and never overwrites; ordinary programs never
move/delete artifacts to satisfy the audit.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from typing import Callable, TypeVar

WORKSPACE = Path(__file__).resolve().parent
ARTIFACTS = WORKSPACE / 'large_artifacts'
THRESHOLD = 10 * 1024 * 1024  # 10 MiB; owner may revise in a subsequent reviewed change.
THIRD_PARTY_EXCEPTION = 'y-cruncher v0.8.7.9547b'
LEGACY_DIGITS = 'ycruncher_digits'
LEGACY_RESULTS = 'OUTLANDISH_01_results'
_DIGIT_RUN = re.compile(r'^(?:pi|phi|e|log2|gamma|lemniscate)_(\d+)_digits$')
_T = TypeVar('_T')


class ArtifactPolicyError(ValueError):
    """An output path or workspace file violates the OUTLANDISH policy."""


@dataclass(frozen=True)
class Violation:
    path: Path
    size: int
    reason: str
    movable: bool

    def describe(self) -> str:
        return f'{self.reason}: {self.path} ({self.size:,} bytes)'


def _junction(path: Path) -> bool:
    checker = getattr(path, 'is_junction', None)
    return bool(checker and checker())


def _unsafe_link(path: Path) -> bool:
    return path.is_symlink() or _junction(path)


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.absolute().relative_to(parent.absolute())
        return True
    except ValueError:
        return False


def require_artifact_path(path: Path) -> Path:
    """Forbid path traversal, symlinks and junctions along the artifact path."""
    # abspath normalises '..' and '.' before checking the containment boundary.
    actual = Path(os.path.abspath(os.fspath(path)))
    if not is_inside(actual, ARTIFACTS) or actual == ARTIFACTS:
        raise ArtifactPolicyError(f'generated artifact must be beneath {ARTIFACTS}: {path}')
    current = WORKSPACE
    for piece in actual.relative_to(WORKSPACE).parts:
        current = current / piece
        if _unsafe_link(current):
            raise ArtifactPolicyError(f'symlink/junction in artifact path: {current}')
    return actual


def new_artifact_directory(child: str) -> Path:
    destination = require_artifact_path(ARTIFACTS / child / '_probe_').parent
    destination.mkdir(parents=True, exist_ok=True)
    require_artifact_path(destination / '_probe_')
    return destination


def digit_path(name: str) -> Path:
    if Path(name).name != name or not name.lower().endswith('.bin'):
        raise ArtifactPolicyError(f'invalid digit binary file name: {name}')
    return require_artifact_path(ARTIFACTS / 'digits' / name)


def resolve_digit_argument(path: Path) -> Path:
    """Bare digit names default to digits/; explicit paths must already be in artifacts."""
    return require_artifact_path(digit_path(path.name) if path.parent == Path('.') else path)


def _reason(path: Path, rel: Path, size: int) -> str | None:
    # The one legacy tracked pi fixture is an intentional narrow exception.
    if rel.parts == ('Pi - Dec - Chudnovsky.txt',) and size <= 2_000_000:
        return None
    if path.suffix.lower() == '.bin':
        return 'generated/retained .bin outside artifact root'
    if (path.suffix.lower() == '.txt'
            and re.match(r'(?i)^(pi|golden ratio|euler|lemniscate|ln.*2|log.*2).* - dec - .*\.txt$', path.name)):
        return 'recognised calculator decimal-digit text outside artifact root'
    if path.name.startswith(('.outlandish_build_', '.preholdout_')) and path.suffix == '.tmp':
        return 'abandoned known temporary output'
    if rel.parts[0] == LEGACY_DIGITS:
        if path.suffix.lower() in ('.ycd', '.dat', '.swap', '.tmp'):
            return 'legacy calculation scratch/intermediate'
        for parent in rel.parents:
            match = _DIGIT_RUN.match(parent.name)
            if match and path.suffix.lower() == '.txt' and size == int(match.group(1)) + 1:
                return 'legacy uncompressed decimal digit text'
    if size >= THRESHOLD:
        return f'file at or above {THRESHOLD:,}-byte workspace threshold'
    return None


def audit_workspace() -> list[Violation]:
    """Metadata-only, no following directory links, no reading file contents."""
    failures: list[Violation] = []
    if _unsafe_link(ARTIFACTS):
        failures.append(Violation(ARTIFACTS, 0, 'artifact root is a link/junction', False))
    elif ARTIFACTS.exists() and not ARTIFACTS.is_dir():
        failures.append(Violation(ARTIFACTS, ARTIFACTS.stat().st_size,
                                  'artifact root exists but is not a directory', False))
    if not WORKSPACE.is_dir():
        raise ArtifactPolicyError(f'workspace is not a directory: {WORKSPACE}')
    for parent, dirs, files in os.walk(WORKSPACE, topdown=True, followlinks=False):
        folder = Path(parent)
        kept = []
        for name in dirs:
            candidate = folder / name
            if candidate == ARTIFACTS and not _unsafe_link(candidate):
                continue
            if folder == WORKSPACE and name == THIRD_PARTY_EXCEPTION:
                continue
            if _unsafe_link(candidate):
                failures.append(Violation(candidate, 0, 'directory link/junction outside artifact root', False))
            else:
                kept.append(name)
        dirs[:] = kept
        for name in files:
            candidate = folder / name
            if _unsafe_link(candidate):
                failures.append(Violation(candidate, 0, 'file link/junction outside artifact root', False))
                continue
            try:
                item = candidate.lstat()
            except FileNotFoundError:
                failures.append(Violation(candidate, 0, 'file vanished during audit; retry', False))
                continue
            if not stat.S_ISREG(item.st_mode):
                failures.append(Violation(candidate, 0, 'non-regular workspace entry', False))
                continue
            reason = _reason(candidate, candidate.relative_to(WORKSPACE), item.st_size)
            if reason:
                # Only recognised COMPLETE digit binaries/plaintexts are auto-movable.
                # Unknown oversized files, scratch and abandoned temps need human review.
                movable = reason in (
                    'generated/retained .bin outside artifact root',
                    'legacy uncompressed decimal digit text',
                    'recognised calculator decimal-digit text outside artifact root',
                )
                failures.append(Violation(candidate, item.st_size, reason, movable))
    return sorted(failures, key=lambda x: str(x.path).casefold())


def _report(failures: list[Violation], phase: str) -> None:
    if failures:
        print(f'ARTIFACT SAFETY STOP ({phase}): {len(failures)} misplaced/unsafe entries', file=sys.stderr)
        for failure in failures:
            print('  ' + failure.describe(), file=sys.stderr)
        print('Use: python outlandish_artifacts.py audit', file=sys.stderr)
        print('Migration is explicit and must not run while any writer is active.', file=sys.stderr)
    else:
        print(f'ARTIFACT AUDIT PASS ({phase}): no misplaced generated/large files', flush=True)


def require_clean(phase: str) -> None:
    failures = audit_workspace()
    _report(failures, phase)
    if failures:
        raise ArtifactPolicyError('artifact workspace audit failed; see paths above')


def guarded_call(call: Callable[[], _T]) -> _T:
    """Audit at start and normal/failing exits without masking an original exception."""
    require_clean('preflight')
    try:
        return call()
    finally:
        failed = sys.exc_info()[0] is not None
        findings = audit_workspace()
        _report(findings, 'post-run / error-path' if failed else 'post-run')
        if findings and not failed:
            raise ArtifactPolicyError('post-run artifact audit failed')


def destination_for(failure: Violation) -> Path:
    rel = failure.path.relative_to(WORKSPACE)
    if rel.parts[0] == LEGACY_DIGITS:
        return require_artifact_path(ARTIFACTS / 'intermediate' / 'legacy_ycruncher_digits' / Path(*rel.parts[1:]))
    if rel.parts[0] == LEGACY_RESULTS:
        return require_artifact_path(ARTIFACTS / 'large_results' / 'legacy_results' / Path(*rel.parts[1:]))
    if failure.path.suffix.lower() == '.bin':
        return digit_path(failure.path.name) if len(rel.parts) == 1 else require_artifact_path(ARTIFACTS / 'digits' / 'legacy' / rel)
    return require_artifact_path(ARTIFACTS / 'intermediate' / 'legacy_misc' / rel)


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as src:
        while chunk := src.read(4 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def migrate_one(v: Violation) -> Path:
    """Explicit move: copy -> full hash verify -> create-only publish -> unlink old.

    Requires same-filesystem hardlink support for atomic create-only publication.
    Refuses to alter source if it changed while copying or before removal.
    """
    if not v.movable or _unsafe_link(v.path) or not v.path.is_file():
        raise ArtifactPolicyError(f'cannot safely migrate {v.path}')
    dest = destination_for(v)
    dest.parent.mkdir(parents=True, exist_ok=True)
    require_artifact_path(dest)
    if dest.exists() or dest.is_symlink():
        raise FileExistsError(f'non-overwrite refusal: destination already exists {dest}')
    before = v.path.stat()
    if before.st_size != v.size:
        raise ArtifactPolicyError(f'source changed since audit: {v.path}')
    stage = None
    try:
        with tempfile.NamedTemporaryFile(mode='wb', dir=dest.parent,
                                         prefix='.outlandish_migrate_', suffix='.tmp', delete=False) as tgt:
            stage = Path(tgt.name)
            h = hashlib.sha256()
            with v.path.open('rb') as src:
                while chunk := src.read(4 * 1024 * 1024):
                    h.update(chunk)
                    tgt.write(chunk)
            tgt.flush()
            os.fsync(tgt.fileno())
        now = v.path.stat()
        if (now.st_size, now.st_mtime_ns, now.st_ino) != (before.st_size, before.st_mtime_ns, before.st_ino):
            raise ArtifactPolicyError(f'source changed during migration: {v.path}')
        if _hash_file(stage) != h.hexdigest() or _hash_file(v.path) != h.hexdigest():
            raise ArtifactPolicyError(f'copy/hash mismatch: {v.path}; source preserved')
        # os.link is atomic and create-only on a local NTFS volume.
        os.link(stage, dest)
        stage.unlink()
        stage = None
        final = v.path.stat()
        if (_unsafe_link(v.path) or (final.st_size, final.st_mtime_ns, final.st_ino)
                != (before.st_size, before.st_mtime_ns, before.st_ino)):
            raise ArtifactPolicyError(f'source changed before unlink, both copies retained: {v.path}')
        v.path.unlink()
        print(f'MIGRATED {v.path} -> {dest} SHA-256 {h.hexdigest()}')
        return dest
    finally:
        if stage is not None and stage.exists():
            stage.unlink()


def inventory_sources() -> int:
    """Read only program text inside this standalone workspace; not a code proof."""
    known = {
        'outlandish_artifacts.py', 'outlandish_big_constants.py',
        'outlandish_powerball_stage_a.py', 'generate_1e10.cmd',
        'scan_1e10.cmd', 'test_artifact_safeguards.py',
    }
    extensions = {'.py', '.bat', '.cmd', '.ps1', '.sh'}
    unreviewed = 0
    found = 0
    for base, dirs, files in os.walk(WORKSPACE, topdown=True, followlinks=False):
        folder = Path(base)
        dirs[:] = [d for d in dirs if not _unsafe_link(folder / d)
                   and (folder / d) != ARTIFACTS
                   and not (folder == WORKSPACE and d == THIRD_PARTY_EXCEPTION)
                   and d != '__pycache__']
        for name in sorted(files):
            path = folder / name
            if path.suffix.lower() not in extensions or _unsafe_link(path):
                continue
            found += 1
            rel = path.relative_to(WORKSPACE)
            if len(rel.parts) == 1 and name in known:
                print(f'EXPECTED-ENTRY-NAME {rel} (exact source version not verified)')
            else:
                unreviewed += 1
                print(f'UNREVIEWED-ENTRY {rel} -- inspect manually; do not assume guarded')
            try:
                with path.open('r', encoding='utf-8-sig', errors='replace') as source:
                    for line_no, line in enumerate(source, 1):
                        if name != 'outlandish_artifacts.py' and ('src/GAIS' in line or 'src\\GAIS' in line):
                            unreviewed += 1
                            print(f'  LEGACY-PATH line {line_no}: {line.strip()[:150]}')
            except OSError as exc:
                print(f'  SOURCE READ ERROR: {exc}')
                unreviewed += 1
    print(f'PROGRAM INVENTORY: {found} files; {unreviewed} unreviewed/read errors.')
    print('Archives and scripts outside OUTLANDISH_01 are not inspected.')
    return 2 if unreviewed else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('audit', help='metadata-only read-only scan, exit nonzero on violations')
    migrate = sub.add_parser('migrate', help='show migrations, or perform explicit safe copy/hash/move')
    sub.add_parser('inventory', help='list program entry points; highlight unreviewed scripts and legacy paths')
    migrate.add_argument('--apply', action='store_true', help='perform verified create-only moves')
    migrate.add_argument('--confirm-idle', action='store_true', help='confirm no OUTLANDISH generation or scan writers are active')
    args = parser.parse_args(argv)
    if args.command == 'inventory':
        return inventory_sources()
    findings = audit_workspace()
    if args.command == 'audit':
        _report(findings, 'standalone audit')
        return 2 if findings else 0
    if args.apply and not args.confirm_idle:
        parser.error('--apply requires --confirm-idle (manually confirm no active writers first)')
    if not findings:
        print('Nothing to migrate.')
        return 0
    for v in findings:
        if not v.movable:
            print(f'MANUAL REVIEW: {v.describe()}')
            continue
        try:
            destination = destination_for(v)
            print(f'{"MOVE" if args.apply else "PLAN"} {v.path} -> {destination} ({v.size:,} bytes)')
            if args.apply:
                migrate_one(v)
        except (OSError, ValueError) as exc:
            print(f'MIGRATION REFUSED: {exc}', file=sys.stderr)
    remaining = audit_workspace()
    _report(remaining, 'after migration' if args.apply else 'migration preview')
    # Preview is informational and intentionally nonzero if work remains.
    return 2 if remaining else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(2)
