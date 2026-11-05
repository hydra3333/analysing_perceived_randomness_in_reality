#!/usr/bin/env python3
"""Streaming converter for verified, plain-text decimal constant digits.

Input must contain ONLY ASCII decimal digits, whitespace, and optionally ONE
period exactly after the initial integer digit. No metadata or headers.
Output is one numeric decimal digit (0..9) per byte, matching OUTLANDISH_01.
This program CONVERTS a supplied digit text file; it does NOT compute pi/phi.
"""
import argparse
import hashlib
import os
import shutil
import sys
import time
from pathlib import Path
from tempfile import NamedTemporaryFile

WHITESPACE = b' \t\r\n'
TRANS = bytes((n - 48) if 48 <= n <= 57 else 255 for n in range(256))
CHUNK = 4 * 1024 * 1024


def convert(source: Path, destination: Path, expected_digits: int, first_digit: int) -> None:
    if source.is_symlink() or not source.is_file():
        raise ValueError('input text must be an existing ordinary file')
    if source.resolve() == destination.resolve() or destination.exists():
        raise ValueError('refusing to overwrite either the source or existing output')
    destination.parent.mkdir(parents=True, exist_ok=True)
    available = shutil.disk_usage(destination.parent).free
    if available < expected_digits:
        raise ValueError(f'not enough destination disk space: need {expected_digits:,} bytes, '
                         f'available {available:,} bytes (before temporary files)')
    tmp = None
    digit_count = 0
    period_seen = False
    digest = hashlib.sha256()
    t0 = time.perf_counter()
    try:
        with source.open('rb') as incoming, NamedTemporaryFile('wb', dir=destination.parent,
                      prefix='.decimal_to_bin_', suffix='.tmp', delete=False) as outgoing:
            tmp = Path(outgoing.name)
            while chunk := incoming.read(CHUNK):
                if b'.' in chunk:
                    if period_seen or chunk.count(b'.') != 1:
                        raise ValueError('multiple decimal points in input')
                    before = chunk.split(b'.', 1)[0].translate(None, WHITESPACE)
                    if digit_count + len(before) != 1:
                        raise ValueError('decimal point is not immediately after the leading digit')
                    period_seen = True
                stripped = chunk.translate(None, WHITESPACE + b'.')
                converted = stripped.translate(TRANS)
                if b'\xff' in converted:
                    raise ValueError('input contains non-digit text or metadata: refuse rather than guess')
                if digit_count == 0 and converted and converted[0] != first_digit:
                    raise ValueError('leading digit does not match expected constant')
                digit_count += len(converted)
                if digit_count > expected_digits:
                    raise ValueError('input contains more digits than requested')
                outgoing.write(converted)
                digest.update(converted)
            if digit_count != expected_digits:
                raise ValueError(f'expected {expected_digits:,} digits but got {digit_count:,}')
        os.replace(tmp, destination)
        tmp = None
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
    dt = time.perf_counter()-t0
    print(f'CONVERTED {digit_count:,} digits in {dt:.3f}s -> {destination}')
    print(f'SHA256: {digest.hexdigest()}')
    print('Output is numeric bytes 0..9, exactly one per decimal digit.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True, help='ASCII digit text without headers or metadata')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--digits', type=int, required=True, help='number of digits INCLUDING integer leading digit')
    p.add_argument('--constant', choices=('pi', 'phi'), required=True)
    a = p.parse_args()
    if a.digits < 2:
        p.error('--digits must be at least 2')
    convert(a.input, a.output, a.digits, 3 if a.constant == 'pi' else 1)

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
