"""Shared canonical encodings, moved unchanged from E_1's module by E1-ALIGN.

canonical_bytes: the project canonical JSON encoding. length32_tuple: the ratified tuple encoding
(4-byte unsigned little-endian UTF-8 byte length, then the bytes). No method code may live here.
"""
from __future__ import annotations

import json
from collections.abc import Sequence


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('ascii')


def length32_tuple(values: Sequence[object]) -> bytes:
    """Ratified tuple encoding: 4-byte unsigned LE UTF-8 byte length + bytes."""
    parts = []
    for value in values:
        if type(value) is not str:
            raise ValueError('tie tuple field must be a canonical string')
        encoded = value.encode('utf-8')
        if len(encoded) > 0xffffffff:
            raise ValueError('tie tuple field exceeds uint32 byte length')
        parts.append(len(encoded).to_bytes(4, byteorder='little') + encoded)
    return b''.join(parts)
