#!/usr/bin/env python3
"""WSL-only verified y-cruncher text -> packed BCD .bin staging, preview default.

Single streaming source read, output SHA computed while writing, bounded
sample readback only. Deletes source text *after* published binary + receipt
are confirmed. No production registry operations. Python stdlib only.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
import uuid
from wsl_format import (FORMAT, PREFIXES, FULL_LEMNISCATE, STEMS, REPORT_NAMES,
                        packed_bytes, pack_ascii, sample_plan, safe_regular, receipt_path)

CHUNK = 8 * 1024 * 1024
WHITESPACE = b' \t\r\n'


def report_evidence(report: Path, constant: str, digits: int) -> dict:
    if report.stat().st_size > 256_000:
        raise ValueError('oversized report')
    data = report.read_bytes()
    body = data.decode('utf-8', errors='replace')
    if not re.search(r'^\s*Verify Output:\s*Enabled\s*$', body, re.M):
        raise ValueError('y-cruncher report must say Verify Output: Enabled')
    if not re.search(r'Spot Check:\s*Good through\s+[\d,]+', body):
        raise ValueError('missing positive y-cruncher spot-check evidence')
    if not re.search(r'^\s*Constant:\s*' + re.escape(REPORT_NAMES[constant]) + r'\s*$', body, re.M|re.I):
        raise ValueError('report constant mismatch')
    if not re.search(r'^\s*Decimal Digits:\s*' + re.escape(f'{digits-1:,}') + r'\s*$', body, re.M):
        raise ValueError('report digits mismatch')
    return {'report_name':report.name,'report_sha256':hashlib.sha256(data).hexdigest(),
            'ycruncher_verify_output':True,'ycruncher_spot_check_reported':True}


def half_decimal_ascii(chunk: bytes, carry: int) -> tuple[bytes,int]:
    """Exact streaming truncated decimal division of full lemniscate by two.
    This is a deliberately simple pure-Python per-digit implementation; no
    Debian NumPy dependency. Benchmark at 1e9 before a 1e11 commitment.
    """
    out = bytearray(len(chunk))
    for i, a in enumerate(chunk):
        d = a-48
        out[i] = 48 + (10*carry+d)//2
        carry = d&1
    return bytes(out), carry


def _inside(child: Path, parent: Path) -> bool:
    try: return bool(child.relative_to(parent).parts)
    except ValueError: return False


def _parse_and_run(a: argparse.Namespace) -> dict:
    srcroot = safe_regular(a.source_root, must_exist=False)
    outroot = safe_regular(a.output_root, must_exist=False)
    src = safe_regular(a.input)
    report = safe_regular(a.report)
    dst = safe_regular(a.output, must_exist=False)
    if not srcroot.is_dir() or not outroot.is_dir():
        raise ValueError('existing source and output roots required')
    if not _inside(src,srcroot) or not _inside(dst,outroot):
        raise ValueError('source/output outside declared roots')
    if report.parent != src.parent or not _inside(report,srcroot):
        raise ValueError('report must be beside the source text')
    if dst.parent != outroot/'staging' or not dst.parent.is_dir():
        raise ValueError('destination must be directly inside pre-existing output-root/staging')
    if not src.name.endswith('.txt') or not dst.name.startswith('digits_'+STEMS[a.constant]+'_') or not dst.name.endswith('.packed.bin'):
        raise ValueError('invalid source/output filename')
    if a.digits < 32:
        raise ValueError('digits must be >= 32')
    recpath = receipt_path(dst)
    for p in (dst, recpath):
        if p.exists() or p.is_symlink():
            raise FileExistsError(f'refuse to overwrite {p}')
    evidence = report_evidence(report,a.constant,a.digits)
    if not a.run:
        print(f'PREVIEW ONLY: {a.constant} {a.digits:,} digits -> {packed_bytes(a.digits):,} bytes')
        print(f'INPUT {src}\nREPORT {report}\nOUTPUT {dst}\nRECEIPT {recpath}')
        print('TEXT: ' + ('keep' if a.keep_text else 'delete only after staged sample checks and receipt'))
        print('No calculation, conversion, publication, registry update or deletion.')
        return {}
    if a.digits >= 1_000_000_000 and a.ack_large != a.digits:
        raise ValueError(f'large conversion requires --ack-large {a.digits}')
    size = packed_bytes(a.digits)
    if shutil.disk_usage(dst.parent).free < size + 64*1024*1024:
        raise ValueError('insufficient destination staging space')
    known = PREFIXES[a.constant]
    plans = sample_plan(size)
    expected = {offset:bytearray(length) for offset,length in plans}
    written = 0
    textdigits = 0
    rawbytes = 0
    dots = 0
    carry = 0
    pending = b''
    first_source = bytearray()
    first_result = bytearray()
    hsource = hashlib.sha256()
    hbin = hashlib.sha256()
    src_stat_before = src.stat()
    started = time.perf_counter()
    temporary = dst.with_name('.'+dst.name+'.'+uuid.uuid4().hex+'.part')
    published = False
    receipt_done = False
    try:
        with src.open('rb') as reader, temporary.open('xb') as writer:
            while chunk := reader.read(CHUNK):
                rawbytes += len(chunk)
                hsource.update(chunk)
                # One ASCII decimal point immediately after the integer digit.
                if chunk.count(b'.'):
                    if dots or chunk.count(b'.') != 1:
                        raise ValueError('multiple decimal points')
                    before = chunk.split(b'.',1)[0].translate(None, WHITESPACE)
                    if textdigits + len(before) != 1:
                        raise ValueError('decimal point not immediately after integer digit')
                    dots = 1
                stripped = chunk.translate(None, WHITESPACE + b'.')
                if stripped.translate(None, b'0123456789'):
                    raise ValueError('invalid source character (must be ASCII decimal)')
                if len(first_source)<len(FULL_LEMNISCATE):
                    n = min(len(stripped), len(FULL_LEMNISCATE)-len(first_source))
                    first_source.extend(stripped[:n])
                textdigits += len(stripped)
                if textdigits > a.digits: raise ValueError('too many source digits')
                if a.constant=='lemniscate':
                    stripped,carry = half_decimal_ascii(stripped,carry)
                if len(first_result)<len(known):
                    n = min(len(stripped),len(known)-len(first_result))
                    first_result.extend(stripped[:n])
                    if len(first_result)==len(known) and bytes(first_result)!=known:
                        raise ValueError('known 32-digit constant prefix mismatch')
                if a.constant=='lemniscate' and len(first_source)==len(FULL_LEMNISCATE) and bytes(first_source)!=FULL_LEMNISCATE:
                    raise ValueError('lemniscate source is not the full-perimeter constant')
                data = pending + stripped
                even = len(data) & ~1
                packed = pack_ascii(data[:even])
                pending = data[even:]
                # Sample expected bytes while producing the output: no reread.
                for offset,length in plans:
                    low = max(offset,written)
                    high = min(offset+length,written+len(packed))
                    if low<high:
                        expected[offset][low-offset:high-offset] = packed[low-written:high-written]
                writer.write(packed)
                hbin.update(packed)
                written += len(packed)
            if dots != 1 or textdigits != a.digits:
                raise ValueError(f'source digits {textdigits:,}, expected {a.digits:,}; dot count {dots}')
            if a.constant=='lemniscate' and bytes(first_source) != FULL_LEMNISCATE:
                raise ValueError('lemniscate source is not the full-perimeter constant')
            if bytes(first_result) != known:
                raise ValueError('known 32-digit constant prefix mismatch')
            if pending:
                packed = pack_ascii(pending) # pad low nibble zero
                for offset,length in plans:
                    low=max(offset,written); high=min(offset+length,written+1)
                    if low<high: expected[offset][low-offset:high-offset]=packed[low-written:high-written]
                writer.write(packed)
                hbin.update(packed)
                written+=1
            if written != size: raise ValueError('internal packed byte length mismatch')
            src_stat_after = src.stat()
            if (src_stat_after.st_dev,src_stat_after.st_ino,src_stat_after.st_size,src_stat_after.st_mtime_ns) != (src_stat_before.st_dev,src_stat_before.st_ino,src_stat_before.st_size,src_stat_before.st_mtime_ns):
                raise ValueError('source file changed during streaming conversion')
            writer.flush(); os.fsync(writer.fileno())
        # Create-only publish, no overwrite; fail closed on DrvFS without hard links.
        os.link(temporary,dst)
        published = True
        if dst.stat().st_size != size: raise ValueError('published size mismatch')
        with dst.open('rb') as inp:
            for offset,length in plans:
                inp.seek(offset)
                block=inp.read(length)
                if block != expected[offset]:
                    raise ValueError(f'sampled readback differs at byte {offset:,}')
        record = {
            'format': FORMAT, 'format_version': 1,
            'verification_policy': 'STREAM_ALL_SOURCE_VALIDATE;SHA256_WHILE_WRITE;SAMPLED_OUTPUT_READBACK',
            'constant': a.constant, 'digits_including_integer':a.digits,
            'packed_bytes':size, 'binary_name':dst.name,'binary_sha256_streamed':hbin.hexdigest(),
            'source_text_name':src.name,'source_text_bytes':rawbytes,
            'source_text_sha256':hsource.hexdigest(),
            'sample_block_length':plans[0][1],
            'samples':[{'offset_bytes':off,'size':length,
                        'sha256':hashlib.sha256(expected[off]).hexdigest()} for off,length in plans],
            'text_cleanup_requested': not a.keep_text,
            'conversion_wall_seconds': round(time.perf_counter()-started,3),
            'completed_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY', **evidence,
        }
        with recpath.open('x',encoding='utf-8') as out:
            json.dump(record,out,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
        receipt_done=True
        # Source deletion is the last step. Failure leaves source in place if possible.
        if not a.keep_text:
            now_stat = src.stat()
            if (now_stat.st_dev,now_stat.st_ino,now_stat.st_size,now_stat.st_mtime_ns) != (src_stat_before.st_dev,src_stat_before.st_ino,src_stat_before.st_size,src_stat_before.st_mtime_ns):
                raise ValueError('source changed after conversion; source preserved (receipt already created)')
            src.unlink()
            print(f'SOURCE TEXT DELETED: {src}',flush=True)
        print(f'PACKED CONVERSION PASS {a.constant} {a.digits:,} digits -> {size:,} bytes')
        print(f'STREAMED SHA256 {hbin.hexdigest()}\nOUTPUT {dst}\nRECEIPT {recpath}')
        print(f'TIME {time.perf_counter()-started:.3f}s; no full-file readback')
        return record
    finally:
        if temporary.exists():
            temporary.unlink()
        if published and not receipt_done:
            print('ATTENTION: published file without receipt; text retained; manual inspection needed.',file=sys.stderr)


def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--constant',choices=tuple(PREFIXES),required=True)
    p.add_argument('--digits',type=int,required=True)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--output-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--run',action='store_true')
    p.add_argument('--ack-large',type=int)
    p.add_argument('--keep-text',action='store_true')
    a=p.parse_args(argv)
    try: _parse_and_run(a); return 0
    except (OSError,ValueError,RuntimeError) as exc:
        print(f'WSL PACKED CONVERSION STOP: {exc}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
