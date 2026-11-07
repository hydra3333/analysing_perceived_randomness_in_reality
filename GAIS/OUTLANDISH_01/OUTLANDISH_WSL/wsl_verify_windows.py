#!/usr/bin/env python3
"""Read-only packed BCD receipt/sample and optional legacy-prefix spot-check.

Runs under the owner's existing Windows project .venv. Standard-library only;
never invokes the legacy byte-per-digit verifier, importer, or registry.
This is intentionally SAMPLED verification, NOT full SHA verification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from wsl_format import (FORMAT, PREFIXES, packed_bytes, sample_plan,
                        safe_regular, receipt_path)


def read_receipt(binary: Path, receipt: Path | None = None) -> dict:
    candidate = safe_regular(binary)
    data = json.loads(safe_regular(receipt or receipt_path(candidate)).read_text(encoding='utf-8'))
    if data.get('format') != FORMAT or data.get('format_version') != 1:
        raise ValueError('unexpected packed format/version; legacy numeric-byte files are incompatible')
    if data.get('scope') != 'PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY':
        raise ValueError('receipt is not an isolated packed staging record')
    const = data.get('constant')
    digits = data.get('digits_including_integer')
    if const not in PREFIXES or type(digits) is not int or digits < 32:
        raise ValueError('invalid constant/digit identity')
    size = packed_bytes(digits)
    if (candidate.stat().st_size != size or data.get('packed_bytes') != size
            or data.get('binary_name') != candidate.name):
        raise ValueError('staged binary length/name differs from receipt')
    digest = data.get('binary_sha256_streamed')
    if not isinstance(digest,str) or not re.fullmatch(r'[0-9a-f]{64}',digest):
        raise ValueError('malformed source-streamed digest in receipt')
    expected = sample_plan(size)
    samples = data.get('samples')
    if not isinstance(samples,list) or len(samples)!=len(expected):
        raise ValueError('wrong sample plan')
    for sample,(offset,length) in zip(samples,expected):
        if (not isinstance(sample,dict) or sample.get('offset_bytes')!=offset
                or sample.get('size')!=length or not isinstance(sample.get('sha256'),str)
                or not re.fullmatch(r'[0-9a-f]{64}',sample['sha256'])):
            raise ValueError('bad sample metadata')
    return data


def decimal_slice(packed: bytes, offset_digits: int, count: int) -> bytes:
    """Return BCD as legacy NUMERIC digit bytes from small sampled blocks only."""
    out=bytearray(count)
    for i in range(count):
        n = offset_digits + i
        b = packed[n//2]
        digit = (b>>4) if not n%2 else (b&15)
        if digit>9: raise ValueError(f'non-decimal nibble at sampled position {n}')
        out[i]=digit
    return bytes(out)


def verify_packed(binary: Path, receipt: Path | None = None,
                  reference: Path | None = None) -> dict:
    binary = safe_regular(binary)
    record = read_receipt(binary,receipt)
    digits=record['digits_including_integer']
    size=packed_bytes(digits)
    with binary.open('rb') as stream:
        for s in record['samples']:
            stream.seek(s['offset_bytes'])
            block=stream.read(s['size'])
            if hashlib.sha256(block).hexdigest()!=s['sha256']:
                raise ValueError(f"sample mismatch at packed byte {s['offset_bytes']}")
        stream.seek(0)
        prefix=decimal_slice(stream.read(16),0,32)
        if prefix!=bytes(x-48 for x in PREFIXES[record['constant']]):
            raise ValueError('known constant prefix differs')
        if digits&1:
            stream.seek(size-1)
            if stream.read(1)[0]&15:
                raise ValueError('invalid low nibble padding')
    checked_reference=0
    if reference is not None:
        ref=safe_regular(reference)
        if ref == binary: raise ValueError('reference aliases packed input')
        refsize=ref.stat().st_size
        checked_reference=min(digits,refsize)
        if checked_reference < 32: raise ValueError('reference is too short')
        # Sample the entire overlapping numeric-prefix range; not a full comparison.
        plans=sample_plan(packed_bytes(checked_reference))
        with binary.open('rb') as b, ref.open('rb') as r:
            for off,length in plans:
                n=off*2
                qty=min(length*2,checked_reference-n)
                b.seek(off); r.seek(n)
                numeric=decimal_slice(b.read(length),0,qty)
                if r.read(qty)!=numeric:
                    raise ValueError(f'sampled legacy prefix mismatch near digit {n:,}')
    return {'constant':record['constant'],'digits':digits,'packed_bytes':size,
            'samples_checked':len(record['samples']),
            'legacy_reference_prefix_digits_eligible':checked_reference,
            'full_file_sha_independently_recomputed':False,
            'no_registration':True}


def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--constant',required=True,choices=tuple(PREFIXES))
    p.add_argument('--digits',type=int,required=True)
    p.add_argument('--receipt',type=Path)
    p.add_argument('--reference',type=Path,
                   help='existing legacy 1-byte/digit reference; sampled only')
    a=p.parse_args(argv)
    try:
        result=verify_packed(a.input,a.receipt,a.reference)
        if result['constant']!=a.constant or result['digits']!=a.digits:
            raise ValueError('CLI and receipt identity mismatch')
        print('PACKED STAGING SAMPLE VERIFICATION PASS')
        print(json.dumps(result,indent=2))
        print('IMPORTANT: sampled check only; no full reread, registry update or deletion.')
        return 0
    except (OSError,ValueError,KeyError,TypeError,IndexError,json.JSONDecodeError) as exc:
        print(f'PACKED VERIFY STOP: {exc}',file=sys.stderr)
        return 2

if __name__=='__main__':raise SystemExit(main())
