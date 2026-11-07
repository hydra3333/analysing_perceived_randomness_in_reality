#!/usr/bin/env python3
"""OUTLANDISH packed-decimal format v1. Shared pure-Python format contract.

Byte i stores digit 2*i in high nibble, digit 2*i+1 in low nibble.
For odd digit counts the final LOW nibble MUST be zero padding; digit_count
is authoritative (length alone cannot determine it). This is NOT the legacy
one-byte-per-digit format. There is no in-place compatibility.
"""
from __future__ import annotations
import hashlib
from pathlib import Path

FORMAT = 'OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1'
PREFIXES = {
    'pi': b'31415926535897932384626433832795',
    'phi': b'16180339887498948482045868343656',
    'e': b'27182818284590452353602874713526',
    'log2': b'06931471805599453094172321214581',
    'gamma': b'05772156649015328606065120900824',
    'lemniscate': b'26220575542921198104648395898911',
}
FULL_LEMNISCATE = b'52441151085842396209296791797822'
STEMS = {'pi':'pi','phi':'golden_ratio','e':'e','log2':'log2',
         'gamma':'gamma','lemniscate':'lemniscate'}
REPORT_NAMES = {'pi':'Pi','phi':'Golden Ratio','e':'e','log2':'Log(2)',
                'gamma':'Euler-Mascheroni Constant','lemniscate':'Lemniscate'}


def packed_bytes(digits: int) -> int:
    if type(digits) is not int or digits < 1:
        raise ValueError('digits must be a positive integer')
    return (digits + 1) // 2


def pack_ascii(digits: bytes) -> bytes:
    """Fast strict ASCII decimal packing, using CPython's native fromhex."""
    if digits.translate(None, b'0123456789'):
        raise ValueError('non-ASCII-decimal digit')
    if len(digits) % 2:
        digits += b'0'   # canonical LOW nibble pad; not a real digit
    return bytes.fromhex(digits.decode('ascii'))


def unpack_numeric(packed: bytes, digits: int) -> bytes:
    """Unpack to LEGACY numeric bytes for bounded cross-format comparisons."""
    if digits < 0 or digits > len(packed)*2:
        raise ValueError('invalid digit count for packed data')
    out = bytearray(len(packed)*2)
    out[0::2] = bytes(x >> 4 for x in packed)
    out[1::2] = bytes(x & 15 for x in packed)
    if max(out[:digits], default=0) > 9:
        raise ValueError('invalid BCD nibble')
    if digits & 1 and (packed[(digits-1)//2] & 15):
        raise ValueError('nonzero trailing pad nibble')
    return bytes(out[:digits])


def sample_plan(total_bytes: int, *, sample_len: int = 4096, count: int = 12) -> list[tuple[int,int]]:
    """Deterministic reproducible block positions; not random authenticity proof."""
    if total_bytes < 1: raise ValueError('empty file')
    length = min(sample_len, total_bytes)
    hi = total_bytes - length
    offsets = {0, hi, hi//2, hi//4, (3*hi)//4}
    n = 0
    while len(offsets) < min(count, hi+1):
        value = hashlib.sha256(f'{total_bytes}:{n}:OUTLANDISH_SAMPLES_V1'.encode()).digest()
        offsets.add(int.from_bytes(value[:8], 'big') % (hi+1))
        n += 1
    return [(o, length) for o in sorted(offsets)]


def safe_regular(path: Path, *, must_exist: bool = True) -> Path:
    """No symlink/junction components; regular existing file required by default."""
    p = Path(path).absolute()
    for node in (p, *p.parents):
        junction = getattr(node, 'is_junction', None)
        if node.is_symlink() or (junction is not None and junction()):
            raise ValueError(f'linked path prohibited: {node}')
    if must_exist and not p.is_file():
        raise ValueError(f'ordinary file required: {p}')
    return p


def receipt_path(binary: Path) -> Path:
    return binary.with_name(binary.name + '.wsl-receipt.json')
