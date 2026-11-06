#!/usr/bin/env python3
"""OUTLANDISH_01 -- create/verify numeric-byte mathematical constant streams.

Standalone; no lottery data, no network, no project modules.  The optional
'generate' subcommand explicitly launches the owner's local y-cruncher.
Conversion input must be PLAIN ASCII decimal digits, optional decimal point
immediately after first integer digit, optional whitespace; no headers.
Output byte i is numeric decimal digit 0..9, INCLUDING the integer digit.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import hashlib
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from uuid import uuid4

from outlandish_config import load_config

from outlandish_artifacts import (
    WORKSPACE, require_artifact_path, guarded_call, artifact_directory,
    promote_verified, active_digit_file,
)

CHUNK = 4 * 1024 * 1024
# Limit retained diagnostic evidence for a failed, program-owned attempt.
FAILURE_LOG_LIMIT = 1 * 1024 * 1024
ATTEMPT_OWNER_MARKER = 'OUTLANDISH_01_owned_attempt.json'
WHITESPACE = b' \t\r\n'
TABLE = bytes((v - 48) if 48 <= v <= 57 else 255 for v in range(256))
PREFIXES = {
    'pi': b'31415926535897932384626433832795',
    'phi': b'16180339887498948482045868343656',
    'e': b'27182818284590452353602874713526',
    'log2': b'06931471805599453094172321214581',
    'gamma': b'05772156649015328606065120900824',
    'lemniscate': b'26220575542921198104648395898911',
}
YCRUNCHER_CONSTANT = {
    'pi': 'pi', 'phi': 'goldenratio', 'e': 'e',
    'log2': 'log:2', 'gamma': 'gamma', 'lemniscate': 'lemniscate',
}
FILE_STEMS = {
    'pi': 'digits_pi_', 'phi': 'digits_golden_ratio_',
    'e': 'digits_e_', 'log2': 'digits_log2_',
    'gamma': 'digits_gamma_', 'lemniscate': 'digits_lemniscate_',
}
CONSTANTS = tuple(PREFIXES)

# y-cruncher's built-in "lemniscate" computes the full unit-lemniscate
# perimeter (5.244115...), whereas OUTLANDISH_01 deliberately studies the
# half-perimeter constant (2.622057...). Both definitions are legitimate.
# The N-digit decimal source is halved in a streaming, exact long division.
LEMNISCATE_YCRUNCHER_SOURCE_PREFIX = bytes(
    c - 48 for c in b'52441151085842396209296791797822'
)


def halve_lemniscate_digits(digits: bytes, carry: int = 0, numpy_module=None) -> tuple[bytes, int]:
    """Divide an *unpunctuated numeric-byte decimal stream* by 2.

    All digits are 0..9, including the leading integer digit. `carry` is the
    decimal remainder (0 or 1) from the previous input block. One input digit
    always yields exactly one output digit, including at the final boundary;
    this is truncation to N digits, not rounding. The NumPy fast path is
    optional and has a pure-Python equivalent.
    """
    if carry not in (0, 1):
        raise ValueError('invalid decimal division remainder')
    if not digits:
        return b'', carry
    if numpy_module is None:
        out = bytearray(len(digits))
        for i, d in enumerate(digits):
            out[i] = (10 * carry + d) // 2
            carry = d & 1
        return bytes(out), carry
    np = numpy_module
    a = np.frombuffer(digits, dtype=np.uint8)
    out = a >> 1
    out[0] += 5 * carry
    if len(a) > 1:
        out[1:] += 5 * (a[:-1] & 1)
    return out.tobytes(), int(a[-1] & 1)



def display_cmd(args: list[str]) -> str:
    return subprocess.list2cmdline(args) if os.name == 'nt' else shlex.join(args)


def get_exe(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
    else:
        matches = sorted(WORKSPACE.glob('y-cruncher*/y-cruncher.exe'))
        if len(matches) != 1:
            raise ValueError('expected one y-cruncher*/y-cruncher.exe beneath current folder; use --exe')
        p = matches[0]
    if not p.is_file():
        raise FileNotFoundError(f'y-cruncher executable not found: {p}')
    return p.resolve()


def resolve_mode(mode: str, digits: int) -> str:
    # A conservative default: large jobs are not launched in RAM-only mode.
    return ('swap' if digits >= 5_000_000_000 else 'ram') if mode == 'auto' else mode


def ycmd(exe: Path, const: str, digits: int, threads: int,
         mode: str, memory_gib: int, scratch: Path | None,
         ycruncher_verify_output: bool = False) -> list[str]:
    # Verified Windows convention: -dec gives digits AFTER the integer digit.
    cmd = [str(exe), 'custom', YCRUNCHER_CONSTANT[const],
           f'-dec:{digits - 1}', '-hex:0', '-od:1',
           '-compress:0', '-verify:1' if ycruncher_verify_output else '-verify:0', f'-mode:{mode}',
           f'-TD:{threads}', '-PF:none' if threads == 1 else '-PF:taskqueue']
    if mode == 'swap':
        if scratch is None:
            raise ValueError('swap mode needs a dedicated scratch directory')
        cmd += [f'-M:{memory_gib}g', '-swap:raid0', str(scratch)]
    return cmd


def output_dir(root: Path, const: str, digits: int, attempt_id: str | None = None) -> Path:
    # Fresh, isolated attempt directories avoid manual renaming after failures.
    # Historical deterministic folders are never reused or silently deleted.
    name = f'{const}_{digits}_digits'
    if attempt_id is not None:
        name += f'__attempt_{attempt_id}'
    return root / name


def _unsafe_link(p: Path) -> bool:
    check_junction = getattr(p, 'is_junction', None)
    return p.is_symlink() or bool(check_junction and check_junction())


def _fresh_attempt_id() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid4().hex[:12]


def _attempt_marker(out: Path, const: str, digits: int, attempt_id: str) -> None:
    # Only a newly created directory with this marker is eligible for cleanup.
    marker = out / ATTEMPT_OWNER_MARKER
    with marker.open('x', encoding='utf-8') as handle:
        json.dump({'owner': 'OUTLANDISH_01_v0_2r3_pipeline', 'constant': const,
                   'digits': digits, 'attempt_id': attempt_id, 'folder': out.name}, handle)
        handle.write('\n')


def prune_owned_attempt_data(out: Path, const: str, digits: int, attempt_id: str) -> int:
    """Remove data, not diagnostics, from ONE explicitly marked fresh attempt.

    Fail closed if a path contains a symbolic link or NTFS junction. Neither
    previously existing attempt folders nor any registered binary is touched.
    """
    require_artifact_path(out)
    marker = out / ATTEMPT_OWNER_MARKER
    if (not out.is_dir() or _unsafe_link(out) or
            not marker.is_file() or _unsafe_link(marker)):
        raise RuntimeError('no verified owned-attempt marker')
    owner = json.loads(marker.read_text(encoding='utf-8'))
    if owner != {'owner': 'OUTLANDISH_01_v0_2r3_pipeline',
                 'constant': const, 'digits': digits, 'attempt_id': attempt_id,
                 'folder': out.name}:
        raise RuntimeError('owned-attempt marker differs from expected identity')
    entries = list(out.rglob('*'))
    if any(_unsafe_link(item) for item in entries):
        raise RuntimeError('symbolic link/junction inside attempt; automatic cleanup refused')
    # Keep only small root-level diagnostic reports. Uncompressed numeric
    # digits are deleted even for a 1e6 smoke (size == digits + 1).
    deleted = 0
    for item in entries:
        if not item.is_file() or item == marker:
            continue
        size = item.stat().st_size
        is_small_report = (item.parent == out and size <= FAILURE_LOG_LIMIT
                           and item.suffix.lower() in ('.txt', '.log', '.json')
                           and size != digits + 1)
        if not is_small_report:
            item.unlink()
            deleted += 1
    for directory in sorted((item for item in entries if item.is_dir()),
                            key=lambda item: len(item.parts), reverse=True):
        try:
            directory.rmdir()  # Only remove when already empty.
        except OSError:
            pass
    return deleted


def cleanup_failed_attempt(out: Path, const: str, digits: int, attempt_id: str,
                           reason: Exception, staged: Path | None = None,
                           published: Path | None = None) -> None:
    """Best-effort cleanup after a handled failure and a confirmed child exit."""
    try:
        deleted = prune_owned_attempt_data(out, const, digits, attempt_id)
        receipt = out / 'OUTLANDISH_01_failed_attempt.json'
        with receipt.open('x', encoding='utf-8') as handle:
            json.dump({'constant': const, 'digits': digits, 'attempt_id': attempt_id,
                       'error': str(reason), 'deleted_intermediates': deleted,
                       'status': 'FAILED'}, handle, indent=2)
            handle.write('\n')
        # The staging basename is unique to this attempt, so only that file
        # can be removed; NEVER touch a published/registered active binary.
        if staged is not None and staged.exists():
            require_artifact_path(staged)
            if _unsafe_link(staged) or not staged.is_file() or attempt_id not in staged.name:
                raise RuntimeError('unsafe/non-owned staged file; cannot automatically remove')
            staged.unlink()
        if published is not None and published.exists():
            # A failed promotion can leave a create-only link. Refuse to delete
            # if state has already been updated to identify it as the active file.
            from outlandish_config import load_config
            current = load_config().active.get(const)
            if current is not None and current['file'] == published.name:
                print(f'[{const}] ACTIVE BINARY PRESERVED after interrupted publication: '
                      f'{published}', flush=True)
            else:
                require_artifact_path(published)
                if _unsafe_link(published) or not published.is_file():
                    raise RuntimeError('published output not a safe regular file')
                published.unlink()
        print(f'[{const}] FAILURE CLEANUP: removed {deleted} failed-run data file(s); '
              f'kept small reports in {out}', flush=True)
    except Exception as cleanup_error:
        # Report cleanup errors without hiding the primary failure; do not
        # attempt broader directory deletion when identity is uncertain.
        print(f'[{const}] WARNING: cleanup incomplete: {cleanup_error}; '
              f'inspect {out} before manual deletion', file=sys.stderr, flush=True)


def target_binary(const: str, digits: int, root: Path) -> Path:
    exponent = len(str(digits)) - 1
    if digits != 10 ** exponent:
        name = f'{FILE_STEMS[const]}{digits}_digits.bin'
    else:
        name = f'{FILE_STEMS[const]}10_to_{exponent}.bin'
    return root / name


def expand_constants(const: str) -> tuple[str, ...]:
    return ('pi', 'phi') if const == 'both' else (const,)


def start_compute(args, const: str, attempt_id: str | None = None):
    exe = get_exe(args.exe)
    root = artifact_directory('scratch')
    attempt_id = attempt_id or _fresh_attempt_id()
    out = require_artifact_path(output_dir(root, const, args.digits, attempt_id))
    mode = resolve_mode(args.mode, args.digits)
    scratch = out / '_outlandish_owned_swap' if mode == 'swap' else None
    cmd = ycmd(exe, const, args.digits, args.threads, mode, args.memory_gib, scratch,
               args.ycruncher_verify_output)
    print(f'[{const}] TARGET: {args.digits:,} digits INCLUDING integer digit.', flush=True)
    print(f'[{const}] OUTPUT FOLDER: {out}', flush=True)
    print(f'[{const}] MODE={mode.upper()} THREADS_REQUESTED={args.threads} '
          f'(TD task decomposition, not a strict OS thread count)', flush=True)
    if mode == 'swap':
        print(f'[{const}] DISK SWAP MODE: {args.memory_gib} GiB working memory; '
              f'scratch={scratch}; Windows may require elevation.', flush=True)
    print(f'[{const}] Y-CRUNCHER OUTPUT VERIFICATION: '
          f'{"ON" if args.ycruncher_verify_output else "OFF"} '
          '(does not change independent Python pipeline checks)', flush=True)
    print(f'[{const}] COMMAND: {display_cmd(cmd)}', flush=True)
    if not args.run:
        print(f'[{const}] DRY RUN: nothing launched or modified.', flush=True)
        return None
    # Never reuse an old output folder or remove its contents during a retry.
    if out.exists() or out.is_symlink():
        raise FileExistsError(f'refusing existing output directory: {out}')
    root.mkdir(parents=True, exist_ok=True)
    require_artifact_path(out)
    free = shutil.disk_usage(root).free
    if free < args.digits * 2 + 2 * (1024 ** 3):
        raise ValueError(f'insufficient free space for text + binary + margin; '
                         f'free={free:,} bytes, minimum={args.digits * 2 + 2 * (1024 ** 3):,}')
    if mode == 'swap' and free < args.digits * 4:
        print('WARNING: swap computation may need significant additional scratch disk space.', flush=True)
    out.mkdir(parents=True, exist_ok=False)
    _attempt_marker(out, const, args.digits, attempt_id)
    if scratch:
        scratch.mkdir()
        (scratch / '_OUTLANDISH_OWNED.txt').write_text('Owned by this newly created pipeline run.\n', encoding='ascii')
    t0 = time.perf_counter()
    try:
        completed = subprocess.run(cmd, check=False, cwd=out)
    except OSError as exc:
        cleanup_failed_attempt(out, const, args.digits, attempt_id, exc)
        raise RuntimeError(f'y-cruncher launch failed: {exc}') from exc
    elapsed = time.perf_counter() - t0
    print(f'[{const}] y-cruncher exit code={completed.returncode}; wall={elapsed:.1f}s', flush=True)
    if completed.returncode != 0:
        failure = RuntimeError(f'y-cruncher exit {completed.returncode}')
        cleanup_failed_attempt(out, const, args.digits, attempt_id, failure)
        raise failure
    outputs = sorted(p for p in out.iterdir() if p.is_file())
    # The owned-attempt marker does not count as calculator output.
    outputs = [p for p in outputs if p.name != ATTEMPT_OWNER_MARKER]
    if not outputs:
        failure = RuntimeError('y-cruncher exit 0 but no output files')
        cleanup_failed_attempt(out, const, args.digits, attempt_id, failure)
        raise failure
    for item in outputs:
        print(f'  {item.name} ({item.stat().st_size:,} bytes)', flush=True)
    return out, elapsed, cmd, mode, scratch


def generate(args) -> None:
    for const in expand_constants(args.constant):
        start_compute(args, const)


def find_digit_text(out: Path, digits: int) -> Path:
    # Observed for this y-cruncher version: N digits and one decimal point.
    # Never guess from a filename, and never include the small stats/validation TXT.
    candidates = [p for p in out.iterdir()
                  if p.is_file() and not p.is_symlink() and p.suffix.lower() == '.txt'
                  and p.stat().st_size == digits + 1]
    if len(candidates) != 1:
        raise ValueError(f'expected exactly one uncompressed text file of {digits + 1:,} '
                         f'bytes in {out}; found {len(candidates)}; inspect files; '
                         'conversion and cleanup REFUSED')
    return candidates[0]


def pipeline(args) -> None:
    import json
    for const in expand_constants(args.constant):
        destination = require_artifact_path(target_binary(const, args.digits, artifact_directory('digits')))
        staged_output = None  # Unique, attempt-owned staging path allocated below.
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f'refusing to overwrite existing binary: {destination}')
        reference = require_artifact_path(args.reference) if args.reference is not None else None
        if reference is None:
            try:
                previous, record = active_digit_file(const)
            except ValueError as exc:
                if 'no verified active binary' not in str(exc):
                    raise
            else:
                if record['digits'] >= args.digits:
                    raise ValueError(f'new {const} file must have MORE digits than registered active')
                reference = previous
        if reference is None and args.digits >= 1_000_000_000:
            if args.run:
                raise ValueError(f'no prior verified active .bin reference for {const}; '
                                 'register/generate a verified smaller reference first. '
                                 'Large generation requires a complete previous-prefix check.')
            print(f'[{const}] DRY-RUN ONLY: no active reference yet; actual --run would refuse.', flush=True)
        if reference is not None:
            print(f'[{const}] REFERENCE (entire prefix checked): {reference}', flush=True)
        else:
            print(f'[{const}] SMALL SMOKE: verified against independent known 32-digit prefix.', flush=True)
        attempt_id = _fresh_attempt_id()
        staged_output = require_artifact_path(artifact_directory('staging') /
            f'.outlandish_{const}_{args.digits}_{attempt_id}.staged.bin')
        result = start_compute(args, const, attempt_id=attempt_id)
        if result is None:
            print(f'[{const}] DRY RUN: would convert, re-read/verify then delete temporary text '
                  '(keeping small y-cruncher reports).', flush=True)
            continue
        out, generation_seconds, cmd, mode, scratch = result
        published_here = False
        try:
            text_file = find_digit_text(out, args.digits)
            print(f'[{const}] Found digit text: {text_file.name}', flush=True)
            artifact_directory('staging', create=True)
            opts = argparse.Namespace(input=[text_file], output=staged_output, reference=reference,
                                      constant=const, digits=args.digits, progress_seconds=args.progress_seconds)
            conversion_sha = convert(opts)
            verification_sha = verify(argparse.Namespace(input_file=staged_output, reference=reference,
                                      constant=const, digits=args.digits, progress_seconds=args.progress_seconds))
            if conversion_sha != verification_sha:
                raise RuntimeError('conversion and re-read verification SHA-256 mismatch')
            from datetime import datetime, timezone
            record = {
                'format': 'OUTLANDISH_01_numeric_digit_0_to_9_one_byte',
                'constant': const, 'total_digits_including_integer': args.digits,
                'binary_filename': destination.name, 'binary_sha256': verification_sha,
                'reference_file': str(reference) if reference else None,
                'reference_bytes': reference.stat().st_size if reference else None,
                'generation_wall_seconds': round(generation_seconds, 3),
                'generated_text_filename': text_file.name,
                'generated_text_bytes': text_file.stat().st_size,
                'source_constant_convention': ('y-cruncher full lemniscate perimeter, 5.244115...'
                                               if const == 'lemniscate' else 'direct'),
                'output_normalization': ('decimal_stream_divided_by_2_to_half_perimeter'
                                         if const == 'lemniscate' else 'none'),
                'threads_requested': args.threads, 'ycruncher_mode': mode,
                'ycruncher_output_verification_enabled': args.ycruncher_verify_output,
                'ycruncher_command': cmd, 'verified_utc': datetime.now(timezone.utc).isoformat(),
                'cleanup_enabled': not args.keep_text,
                'attempt_id': attempt_id,
            }
            report = out / 'OUTLANDISH_01_verified.json'
            with report.open('x', encoding='utf-8') as h:
                json.dump(record, h, indent=2)
                h.write('\n')
            # Verified source is in staging; create-only publish into digits (same
            # configured volume). Promotion verifies the published file again and
            # updates TOML atomically. Preserve sources if this fails.
            artifact_directory('digits', create=True)
            os.link(staged_output, destination)
            published_here = True
            promote_verified(const, destination, args.digits, verification_sha)
            staged_output.unlink()
            if not args.keep_text:
                deleted = prune_owned_attempt_data(out, const, args.digits, attempt_id)
                print(f'[{const}] CLEANED {deleted} generated temporary data file(s); '
                      'kept small y-cruncher reports and verification manifest', flush=True)
            print(f'[{const}] PIPELINE PASS: {destination} ({args.digits:,} bytes); '
                  f'SHA-256 {verification_sha}', flush=True)
            print(f'[{const}] RETAINED: small y-cruncher reports and verification manifest: {out}', flush=True)

        except Exception as exc:
            cleanup_failed_attempt(out, const, args.digits, attempt_id, exc,
                                   staged=staged_output,
                                   published=destination if published_here else None)
            raise


def inspect_folder(folder: Path):
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    items = sorted(x for x in folder.rglob('*') if x.is_file())
    print(f'{len(items)} files under {folder}')
    for f in items:
        rel = f.relative_to(folder)
        print(f'{rel}: {f.stat().st_size:,} bytes')
        if f.suffix.lower() == '.txt':
            with f.open('rb') as h:
                b = h.read(90)
            print('  first 90 bytes:', repr(b))
    print('Only explicitly selected, PLAIN DIGIT text input files should be passed to convert.')


def validate_reference(ref: Path | None, target_digits: int):
    if ref is None:
        return None, 0
    if not ref.is_file() or ref.is_symlink():
        raise ValueError(f'reference is not an ordinary file: {ref}')
    n = ref.stat().st_size
    if not (32 <= n <= target_digits):
        raise ValueError(f'reference file length {n:,} must be 32..{target_digits:,} bytes')
    with ref.open('rb') as src:
        known_start = src.read(min(n, CHUNK))
        if max(known_start, default=0) > 9:
            raise ValueError('reference contains non-decimal-digit bytes')
    # Comparison is streamed; a prior 1e9 reference never loads into RAM.
    return ref, n

def check_filenames(ins: list[Path], destination: Path) -> None:
    if not ins:
        raise ValueError('provide at least one --input in explicit digit order')
    if len({x.resolve() for x in ins}) != len(ins):
        raise ValueError('duplicated input file')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'output already exists, refusing overwrite: {destination}')
    for f in ins:
        if not f.is_file() or f.is_symlink():
            raise ValueError(f'input is missing or a symlink: {f}')
        if f.resolve() == destination.resolve():
            raise ValueError('source and destination must differ')


def convert(args):
    ins: list[Path] = args.input
    out: Path = args.output
    check_filenames(ins, out)
    reference, ref_len = validate_reference(args.reference, args.digits)
    out.parent.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(out.parent).free
    if free < args.digits:
        raise ValueError(f'Insufficient free disk space: need {args.digits:,} bytes, have {free:,}')
    target_prefix = bytes(c - 48 for c in PREFIXES[args.constant])
    is_lemniscate = args.constant == 'lemniscate'
    numpy_module = None
    remainder = 0
    if is_lemniscate:
        # NumPy accelerates 10^9+ digit long division; it is NOT required to
        # run or verify the generator. The standard-library fallback remains.
        try:
            import numpy as numpy_module
        except ImportError:
            print('NOTE: NumPy unavailable; using slower exact Python lemniscate division.', flush=True)
        print('NORMALIZATION: y-cruncher full lemniscate perimeter (5.244115...) '
              'divided by 2 -> OUTLANDISH half-perimeter constant (2.622057...).', flush=True)
    seen = 0
    periods = 0
    digest = hashlib.sha256()
    t0 = time.perf_counter()
    next_report = t0 + args.progress_seconds
    tmp = None
    ref_reader = reference.open('rb') if reference else None
    try:
        with tempfile.NamedTemporaryFile(mode='wb', dir=out.parent,
                                         prefix='.outlandish_build_', suffix='.tmp',
                                         delete=False) as dest:
            tmp = Path(dest.name)
            for item in ins:
                print(f'INPUT {item} ({item.stat().st_size:,} bytes)', flush=True)
                with item.open('rb') as src:
                    while raw := src.read(CHUNK):
                        if b'.' in raw:
                            count = raw.count(b'.')
                            if count != 1 or periods:
                                raise ValueError('unexpected/multiple decimal points')
                            before = raw[:raw.index(b'.')].translate(None, WHITESPACE)
                            if seen + len(before) != 1:
                                raise ValueError('decimal point must immediately follow integer digit')
                            periods += 1
                        numeric = raw.translate(None, WHITESPACE + b'.').translate(TABLE)
                        if b'\xff' in numeric:
                            raise ValueError(f'non-digit/header/metadata in {item}')
                        if is_lemniscate:
                            if seen < len(LEMNISCATE_YCRUNCHER_SOURCE_PREFIX):
                                qty = min(len(numeric), len(LEMNISCATE_YCRUNCHER_SOURCE_PREFIX)-seen)
                                if numeric[:qty] != LEMNISCATE_YCRUNCHER_SOURCE_PREFIX[seen:seen+qty]:
                                    raise ValueError('expected y-cruncher FULL-perimeter lemniscate '
                                                     'source beginning 5.244115...; refusing to '
                                                     'halve an unexpected or already-normalized input')
                            numeric, remainder = halve_lemniscate_digits(
                                numeric, remainder, numpy_module)
                        if seen < len(target_prefix):
                            qty = min(len(numeric), len(target_prefix) - seen)
                            if numeric[:qty] != target_prefix[seen:seen+qty]:
                                raise ValueError(f'{args.constant} known prefix mismatch')
                        if seen + len(numeric) > args.digits:
                            raise ValueError(f'input has more than expected {args.digits:,} digits')
                        if ref_reader and seen < ref_len:
                            qty = min(len(numeric), ref_len - seen)
                            compare = ref_reader.read(qty)
                            if len(compare) != qty or numeric[:qty] != compare:
                                raise ValueError(f'new digits differ from reference near digit offset {seen:,}')
                        seen += len(numeric)
                        dest.write(numeric)
                        digest.update(numeric)
                        now = time.perf_counter()
                        if now >= next_report:
                            elapsed = max(now - t0, 1e-9)
                            print(f'CONVERT {seen:,}/{args.digits:,} digits ({seen/args.digits:.1%}); '
                                  f'{seen/elapsed/1e6:.1f} MB/s', flush=True)
                            next_report = now + args.progress_seconds
            if seen != args.digits:
                raise ValueError(f'input has {seen:,} digits; expected {args.digits:,}')
            dest.flush()
            os.fsync(dest.fileno())
        # A hard link in the same NTFS filesystem is create-only; it cannot
        # overwrite a file created by a concurrent operator after the initial check.
        try:
            os.link(tmp, out)
        except FileExistsError as exc:
            raise FileExistsError(f'binary appeared while conversion was running: {out}') from exc
        tmp.unlink()
        tmp = None
    finally:
        if ref_reader:
            ref_reader.close()
        if tmp is not None and tmp.exists():
            tmp.unlink()
    print(f'CONVERSION PASS: {args.constant} {seen:,} numeric digit bytes '
          f'({time.perf_counter()-t0:.1f}s)', flush=True)
    print(f'OUTPUT {out}; SHA-256 {digest.hexdigest()}', flush=True)
    if reference:
        print(f'PREVIOUS {ref_len:,}-digit reference prefix MATCHES: {reference}', flush=True)
    return digest.hexdigest()


def verify(args):
    inp: Path = args.input_file
    if not inp.is_file() or inp.is_symlink():
        raise ValueError('input binary must be a regular file, not a symlink')
    if inp.stat().st_size != args.digits:
        raise ValueError(f'file size {inp.stat().st_size:,} bytes, expected {args.digits:,}')
    reference, reflen = validate_reference(args.reference, args.digits)
    known = bytes(c - 48 for c in PREFIXES[args.constant])
    n = 0
    sha = hashlib.sha256()
    start = time.perf_counter()
    next_report = start + args.progress_seconds
    ref_reader = reference.open('rb') if reference else None
    try:
        with inp.open('rb') as src:
            while chunk := src.read(CHUNK):
                if n < len(known):
                    qty = min(len(chunk), len(known)-n)
                    if chunk[:qty] != known[n:n+qty]:
                        raise ValueError('known constant prefix mismatch')
                if ref_reader and n < reflen:
                    qty = min(len(chunk), reflen-n)
                    compare = ref_reader.read(qty)
                    if len(compare) != qty or chunk[:qty] != compare:
                        raise ValueError(f'prior reference differs near digit offset {n:,}')
                if max(chunk, default=0) > 9:
                    raise ValueError(f'invalid binary digit near offset {n:,}')
                sha.update(chunk)
                n += len(chunk)
                now = time.perf_counter()
                if now >= next_report:
                    print(f'VERIFY {n:,}/{args.digits:,} ({n/args.digits:.1%})', flush=True)
                    next_report = now + args.progress_seconds
    finally:
        if ref_reader:
            ref_reader.close()
    if n != args.digits:
        raise ValueError('file changed size during verification')
    print(f'VERIFY PASS {args.constant} {n:,} digits; SHA-256 {sha.hexdigest()}; '
          f'elapsed {time.perf_counter()-start:.1f}s', flush=True)
    if reference:
        print(f'PREVIOUS {reflen:,}-digit reference prefix MATCHES: {reference}', flush=True)
    return sha.hexdigest()


def self_test():
    with tempfile.TemporaryDirectory() as folder:
        p = Path(folder)
        for const in CONSTANTS:
            prefix = PREFIXES[const]
            n = len(prefix)
            expected = bytes(x-48 for x in prefix)
            (p/'reference.bin').write_bytes(expected)
            # Lemniscate test uses ACTUAL y-cruncher full-perimeter digits,
            # then checks division across the two file boundaries, including
            # an odd input digit at the end of the first file.
            source_prefix = (bytes(x+48 for x in LEMNISCATE_YCRUNCHER_SOURCE_PREFIX)
                             if const == 'lemniscate' else prefix)
            (p/'head.txt').write_bytes(source_prefix[:1] + b'. ' + source_prefix[1:11] + b'\n')
            (p/'tail.txt').write_bytes(source_prefix[11:])
            opts = argparse.Namespace(input=[p/'head.txt', p/'tail.txt'], output=p/f'{const}.bin',
                                      reference=p/'reference.bin', constant=const, digits=n,
                                      progress_seconds=999)
            convert(opts)
            verify(argparse.Namespace(input_file=opts.output, reference=opts.reference,
                                      constant=const, digits=n, progress_seconds=999))
            assert opts.output.read_bytes() == expected
            opts2 = argparse.Namespace(input=[p/'head.txt', p/'tail.txt'], output=p/f'{const}_error.bin',
                                       reference=None, constant=const, digits=n-1,
                                       progress_seconds=999)
            try:
                convert(opts2)
            except ValueError as exc:
                assert 'more than expected' in str(exc)
            else:
                raise AssertionError('extra digit should refuse')
            assert not opts2.output.exists()
            (p/'head_bad.txt').write_bytes(b'HEADER' + source_prefix[:1]+b'.'+source_prefix[1:11])
            opts3 = argparse.Namespace(input=[p/'head_bad.txt', p/'tail.txt'], output=p/f'{const}_bad.bin',
                                       reference=opts.reference, constant=const, digits=n,
                                       progress_seconds=999)
            try:
                convert(opts3)
            except ValueError:
                pass
            else:
                raise AssertionError('metadata should refuse')
            assert not opts3.output.exists()
            if const == 'lemniscate':
                # Guard against treating an already-halved source as raw input.
                (p/'head_bad.txt').write_bytes(prefix[:1] + b'.' + prefix[1:])
                opts4 = argparse.Namespace(input=[p/'head_bad.txt'],
                                           output=p/'lemniscate_double_half_refusal.bin',
                                           reference=None, constant=const,
                                           digits=n, progress_seconds=999)
                try:
                    convert(opts4)
                except ValueError as exc:
                    assert 'FULL-perimeter' in str(exc)
                else:
                    raise AssertionError('already-halved input must refuse')
                assert not opts4.output.exists()
                # Pure-Python and optional NumPy paths have identical results,
                # including at odd-remainder boundaries and empty chunks.
                source = bytes(x-48 for x in source_prefix)
                q1, rem = halve_lemniscate_digits(source[:11], 0)
                q2, rem = halve_lemniscate_digits(source[11:], rem)
                assert q1+q2 == expected and rem in (0, 1)
                assert halve_lemniscate_digits(b'', rem) == (b'', rem)
                try:
                    import numpy as np
                except ImportError:
                    pass
                else:
                    q1, rem = halve_lemniscate_digits(source[:11], 0, np)
                    q2, rem = halve_lemniscate_digits(source[11:], rem, np)
                    assert q1+q2 == expected and rem in (0, 1)
    print('SELF-TEST PASS: 6 constants, split text, decimal point, reference prefix, '
          'extra digits, metadata refusal, lemniscate x2 normalization and guard')


def main():
    cfg = load_config()
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    def add_generation_opts(g):
        g.add_argument('--digits', type=int, required=True,
                       help='total digits INCLUDING integer digit')
        g.add_argument('--constant', choices=CONSTANTS + ('both',), default='both')
        g.add_argument('--threads', type=int, default=cfg.generator['threads'],
                       help='requested y-cruncher task-decomposition parallelism; default 4')
        g.add_argument('--mode', choices=('auto', 'ram', 'swap'), default=cfg.generator['mode'],
                       help='auto uses disk swap for >=5e9 digits; RAM below that')
        g.add_argument('--memory-gib', type=int, default=cfg.generator['memory_gib'],
                       help='y-cruncher memory setting in swap mode; default 16 GiB')
        g.add_argument('--ycruncher-verify-output',
                       action=argparse.BooleanOptionalAction,
                       default=cfg.generator['ycruncher_verify_output'],
                       help='enable or disable y-cruncher base-conversion/output-digit '
                            'verification (default OFF); Python pipeline checks remain enabled')
        g.add_argument('--exe', help='path to local y-cruncher executable')
        g.add_argument('--run', action='store_true',
                       help='launch y-cruncher; without this flag only preview')
    g = sub.add_parser('generate', help='launch y-cruncher only (manual conversion)')
    add_generation_opts(g)
    run = sub.add_parser('pipeline', help='generate, convert, verify, then cleanup text')
    add_generation_opts(run)
    run.add_argument('--reference', type=Path,
                     help='trusted prefix binary; automatically use prior 1e9 then 1e6 if present')
    run.add_argument('--keep-text', action='store_true',
                     help='preserve intermediate digit text on SUCCESS; failure discards data')
    run.add_argument('--progress-seconds', type=float, default=5)
    i = sub.add_parser('inspect', help='list generated output files')
    i.add_argument('--folder', type=Path, required=True)
    c = sub.add_parser('convert', help='strict text-to-numeric-byte conversion')
    c.add_argument('--constant', choices=CONSTANTS, required=True)
    c.add_argument('--digits', type=int, required=True)
    c.add_argument('--input', nargs='+', type=Path, required=True)
    c.add_argument('--output', type=Path, required=True)
    c.add_argument('--reference', type=Path, help='streamed prefix check (up to full prior 1e9 file)')
    c.add_argument('--progress-seconds', type=float, default=5)
    v = sub.add_parser('verify', help='independently re-read and validate numeric byte file')
    v.add_argument('--constant', choices=CONSTANTS, required=True)
    v.add_argument('--digits', type=int, required=True)
    v.add_argument('--input-file', type=Path, required=True)
    v.add_argument('--reference', type=Path)
    v.add_argument('--progress-seconds', type=float, default=5)
    sub.add_parser('self-test', help='synthetic conversion and refusal checks')
    a = p.parse_args()
    if a.command in {'generate', 'pipeline', 'convert', 'verify'} and a.digits < 33:
        p.error('--digits must be >=33')
    if a.command in {'generate', 'pipeline'}:
        if not (1 <= a.threads <= 128):
            p.error('--threads must be between 1 and 128')
        if not (1 <= a.memory_gib <= 1024):
            p.error('--memory-gib must be between 1 and 1024')
        if a.mode == 'ram' and a.digits >= 5_000_000_000 and a.run:
            p.error('>=5e9 RAM-only calculation is blocked pending measured safe-memory review; '
                    'dry-run preview is allowed')
    if a.command in {'convert', 'verify', 'pipeline'} and a.progress_seconds <= 0:
        p.error('--progress-seconds must be positive')
    # Explicit output/large-input paths must be in the shared artifact area.
    if a.command == 'generate':
        generate(a)
    elif a.command == 'pipeline':
        pipeline(a)
    elif a.command == 'inspect':
        # Prevent accidentally inspecting the separate primary project's files.
        require_artifact_path(a.folder / '_unused_inspect_entry_')
        inspect_folder(a.folder)
    elif a.command == 'convert':
        a.input = [require_artifact_path(x) for x in a.input]
        a.output = require_artifact_path(a.output)
        if a.reference is not None:
            a.reference = require_artifact_path(a.reference)
        convert(a)
    elif a.command == 'verify':
        a.input_file = require_artifact_path(a.input_file)
        if a.reference is not None:
            a.reference = require_artifact_path(a.reference)
        verify(a)
    else:
        self_test()


if __name__ == '__main__':
    try:
        guarded_call(main, hold_lock=True)
    except (ValueError, FileNotFoundError, OSError, RuntimeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(2)
