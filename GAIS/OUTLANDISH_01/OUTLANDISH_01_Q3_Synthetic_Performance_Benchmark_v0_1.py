#!/usr/bin/env python3
"""OUTLANDISH_01: SYNTHETIC-ONLY Q3 v0.3 4MB vs 8MB performance check.

Each measured invocation runs in a fresh subprocess so Windows' peak working-set
high-water mark is not contaminated by a previous chunk size. Both games use
made-up draw histories and one temporary, random-looking FIXED2 BCD file.
Absolutely no REAL histories, G:/T: production constants, published receipts,
or REAL/NULL result roots are opened.

Examples (Windows CMD, project venv, from repository root):
  ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\OUTLANDISH_01_Q3_Synthetic_Performance_Benchmark_v0_1.py" --self-test
  ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\OUTLANDISH_01_Q3_Synthetic_Performance_Benchmark_v0_1.py" --run

--run defaults to 32 decimal MB of packed input and 433 SYNTHETIC draws per
chosen game. --size-mb 16 and --game powerball shorten the measurement.
This is a microbenchmark, not scientific qualification or a Q5 scan.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time

import OUTLANDISH_01_Q3_Packed_Matcher_v0_3 as m

CHUNKS = (4_000_000, 8_000_000)
BYTES_PER_MB = 1_000_000
FIXTURE_NAME = 'Q3_SYNTHETIC_BENCH_ONLY.packed.bin'
SYNTHETIC_DIR_PREFIX = 'OUTLANDISH_Q3_BENCH_SYNTHETIC_ONLY_'


def make_draws(game: str, total: int):
    """Independent, fixed-seed fabricated histories: never real lottery rows."""
    if not 1 <= total <= 10000:
        raise ValueError('synthetic draw count must be 1..10000')
    rng = random.Random(311_2026 if game == 'powerball' else 120_2026)
    if game == 'powerball':
        draws = [m.PBRecord(1, (3, 7, 11, 15, 19, 23, 35), 7)]
        for n in range(2, total + 1):
            draws.append(m.PBRecord(n, tuple(rng.sample(range(1, 36), 7)), rng.randint(1, 20)))
    elif game == 'oz':
        draws = [m.OzRecord(1, (1, 5, 9, 13, 17, 21, 47), (2, 4, 6))]
        for n in range(2, total + 1):
            balls = rng.sample(range(1, 48), 10)
            draws.append(m.OzRecord(n, tuple(balls[:7]), tuple(balls[7:])))
    else:
        raise ValueError('unknown game')
    return draws


def patch_decimals(path: Path, digit_start: int, digits: str, total_digits: int):
    """Patch a known hit at an arbitrary zero-based nibble position."""
    if not digits or not all(c in '0123456789' for c in digits):
        raise ValueError('nondecimal planted fixture')
    if digit_start < 0 or digit_start + len(digits) > total_digits:
        raise ValueError('planted fixture outside synthetic file')
    start_byte = digit_start // 2
    end_byte = (digit_start + len(digits) + 1) // 2
    with path.open('r+b') as f:
        f.seek(start_byte)
        old = bytearray(f.read(end_byte - start_byte))
        if len(old) != end_byte-start_byte:
            raise AssertionError('short synthetic fixture patch')
        for i, c in enumerate(digits):
            pos = digit_start + i
            idx = pos//2-start_byte
            v = ord(c)-48
            old[idx] = ((old[idx] & 0x0F) | (v << 4)) if pos % 2 == 0 else ((old[idx] & 0xF0) | v)
        f.seek(start_byte)
        f.write(old)


def create_fixture(path: Path, size_mb: int) -> str:
    """Uniform-ish random decimal pairs; fully synthetic, streaming creation."""
    if not 16 <= size_mb <= 128:
        raise ValueError('benchmark size must be 16..128 decimal MB')
    rng = random.Random(20261115)
    # Map each arbitrary byte to a valid two-decimal-digit BCD byte.
    conversion = bytes(((((v % 100)//10)<<4) | ((v % 100)%10)) for v in range(256))
    total_bytes = size_mb * BYTES_PER_MB
    with path.open('xb') as f:
        for amount in [BYTES_PER_MB] * size_mb:
            f.write(rng.randbytes(amount).translate(conversion))
    total_digits = total_bytes * 2
    plants = [
        (8_000_000 - 7, '0307111519233507'),          # PB P1, crosses 4 MB byte boundary
        (16_000_000 - 5, '0105091317214702'),         # Oz O2, crosses 8 MB byte boundary
        (24_000_000 - 9, '01050913172147'),           # Oz O1, another chunk edge
    ]
    for start,pattern in plants:
        patch_decimals(path,start,pattern,total_digits)
    digest=hashlib.sha256()
    with path.open('rb') as f:
        for segment in iter(lambda:f.read(2*BYTES_PER_MB),b''):
            digest.update(segment)
    return digest.hexdigest()


def peak_working_set_mib() -> tuple[float, str]:
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        class ProcessMemoryCounters(ctypes.Structure):
            _fields_ = [
                ('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD),
                ('PeakWorkingSetSize', ctypes.c_size_t),
                ('WorkingSetSize', ctypes.c_size_t),
                ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
                ('QuotaPagedPoolUsage', ctypes.c_size_t),
                ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                ('PagefileUsage', ctypes.c_size_t),
                ('PeakPagefileUsage', ctypes.c_size_t),
            ]
        counter=ProcessMemoryCounters()
        counter.cb=ctypes.sizeof(counter)
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        psapi=ctypes.WinDLL('psapi',use_last_error=True)
        kernel.GetCurrentProcess.argtypes=[]
        kernel.GetCurrentProcess.restype=wintypes.HANDLE
        psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE, ctypes.POINTER(ProcessMemoryCounters), wintypes.DWORD]
        psapi.GetProcessMemoryInfo.restype=wintypes.BOOL
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(counter),counter.cb):
            raise OSError('GetProcessMemoryInfo failed; refusing to invent peak RAM')
        return counter.PeakWorkingSetSize/(1024**2), 'Windows peak working set'
    import resource
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == 'darwin':
        return peak/(1024**2), 'macOS peak RSS'
    return peak/1024, 'Linux peak RSS'


def worker(inp: Path, out: Path, game: str, bytes_per_chunk: int, physical_digits: int,
           sha256: str, total_draws: int):
    # This is a deliberately internal-only entry point, not a production scanner CLI.
    if (inp.name != FIXTURE_NAME or not inp.parent.name.startswith(SYNTHETIC_DIR_PREFIX)
            or not inp.is_file() or inp.is_symlink()):
        raise ValueError('refusing non-synthetic benchmark path')
    if bytes_per_chunk not in CHUNKS:
        raise ValueError('benchmark uses only 4MB or 8MB chunks')
    draws=make_draws(game,total_draws)
    scan=m.scan_packed_stream if game == 'powerball' else m.scan_packed_oz_stream
    began=time.perf_counter()
    result=scan(inp, physical_digits=physical_digits, effective_digits=physical_digits,
                draws=draws, output_csv=out, chunk_bytes=bytes_per_chunk,
                expected_full_sha256=sha256)
    seconds=time.perf_counter()-began
    peak,metric=peak_working_set_mib()
    response=dict(game=game,chunk_mb=bytes_per_chunk//BYTES_PER_MB,
                  elapsed_seconds=round(seconds,4),
                  throughput_mb_per_s=round(physical_digits/2/BYTES_PER_MB/seconds,3),
                  peak_process_mib=round(peak,2),peak_metric=metric,
                  event_sha256=result.event_sha256,event_count=result.event_count,
                  family_counts=result.family_counts,source_sha256=result.sha256_full_packed,
                  bytes_hashed=result.bytes_hashed,chunks=result.chunks)
    print('Q3_BENCH_JSON '+json.dumps(response,sort_keys=True),flush=True)


def self_test():
    if not __debug__:
        raise RuntimeError('Do not run with -O')
    assert m.resolve_chunk_bytes(CHUNKS[0]) == CHUNKS[0]
    assert m.resolve_chunk_bytes(CHUNKS[1]) == CHUNKS[1]
    assert len(make_draws('powerball',433)) == 433
    assert len(make_draws('oz',433)) == 433
    for game in ('powerball','oz'):
        assert type(make_draws(game,1)[0].draw_number) is int
    with tempfile.TemporaryDirectory(prefix=SYNTHETIC_DIR_PREFIX) as t:
        p=Path(t)/FIXTURE_NAME
        sample=bytes([0x99]*34)
        p.write_bytes(sample)
        patch_decimals(p,13,'0307111519233507',len(sample)*2)
        with p.open('rb') as f:
            packed=f.read()
        digits=''.join(f'{x>>4}{x&15}' for x in packed)
        assert digits[13:29]=='0307111519233507'
    print('Q3 SYNTHETIC BENCH SELF-TEST PASS: fabricated draws, nibble patch, chunk override; no REAL files')


def run(size_mb: int, game: str, draw_count: int):
    self_test()
    games = ('powerball','oz') if game == 'both' else (game,)
    with tempfile.TemporaryDirectory(prefix=SYNTHETIC_DIR_PREFIX) as td:
        root=Path(td)
        inp=root/FIXTURE_NAME
        print(f'Creating {size_mb} MB of SYNTHETIC FIXED2 packed BCD in temporary directory',flush=True)
        digest=create_fixture(inp,size_mb)
        results=[]
        for idx,g in enumerate(games):
            # Reverse one game's order to reduce (not eliminate) cache/order bias.
            choices = CHUNKS if idx%2 == 0 else CHUNKS[::-1]
            for chunk in choices:
                out=root/f'{g}.{chunk//BYTES_PER_MB}MB.raw_events.csv'
                cmd=[sys.executable,str(Path(__file__).resolve()),'--_worker',
                     '--fixture',str(inp),'--output',str(out),'--game',g,
                     '--chunk-bytes',str(chunk),'--physical-digits',str(size_mb*BYTES_PER_MB*2),
                     '--expected-sha',digest,'--draw-count',str(draw_count)]
                finished=subprocess.run(cmd,capture_output=True,text=True,check=False)
                if finished.returncode:
                    raise RuntimeError(f'SYNTHETIC benchmark worker {g} chunk={chunk} failed '
                        f'(code {finished.returncode}):\n{finished.stdout}\n{finished.stderr}')
                line=next((l[len('Q3_BENCH_JSON '):] for l in finished.stdout.splitlines()
                           if l.startswith('Q3_BENCH_JSON ')),None)
                if line is None:
                    raise RuntimeError('worker did not provide valid benchmark result: '+finished.stdout)
                x=json.loads(line)
                if (x['source_sha256']!=digest or x['bytes_hashed']!=size_mb*BYTES_PER_MB):
                    raise AssertionError('worker source digest/byte coverage mismatch')
                results.append(x)
                print(f'BENCH {g:9s} {x["chunk_mb"]} MB: {x["elapsed_seconds"]:8.3f} s; '
                      f'{x["throughput_mb_per_s"]:7.2f} packed MB/s; '
                      f'peak process {x["peak_process_mib"]:7.1f} MiB; '
                      f'events={x["event_count"]}',flush=True)
        for g in games:
            a,b=sorted((x for x in results if x['game']==g),key=lambda x:x['chunk_mb'])
            if any(a[k]!=b[k] for k in ('event_sha256','event_count','family_counts','source_sha256')):
                raise AssertionError(f'{g}: 4MB/8MB benchmark changed scientific output or digest')
            print(f'EQUAL CSV SHA {g}: {a["event_sha256"]}',flush=True)
        print('Q3 SYNTHETIC BENCHMARK PASS: 4MB/8MB output-identical; '
              f'games={len(games)} synthetic-size={size_mb}MB '
              f'fabricated-draws/game={draw_count}; peak process includes interpreter/NumPy. '
              'NO REAL INPUTS OR Q5 AUTHORISATION',flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--self-test',action='store_true')
    group.add_argument('--run',action='store_true')
    group.add_argument('--_worker',action='store_true',help=argparse.SUPPRESS)
    p.add_argument('--size-mb',type=int,default=32,help='synthetic packed decimal MB, 16..128; default 32')
    p.add_argument('--game',choices=('powerball','oz','both'),default='both')
    p.add_argument('--draw-count',type=int,default=433,help='fabricated draws per game')
    p.add_argument('--fixture',type=Path,help=argparse.SUPPRESS)
    p.add_argument('--output',type=Path,help=argparse.SUPPRESS)
    p.add_argument('--chunk-bytes',type=int,help=argparse.SUPPRESS)
    p.add_argument('--physical-digits',type=int,help=argparse.SUPPRESS)
    p.add_argument('--expected-sha',help=argparse.SUPPRESS)
    a=p.parse_args()
    if a.self_test:
        self_test()
    elif a.run:
        run(a.size_mb,a.game,a.draw_count)
    else:
        if (not a.fixture or not a.output or a.chunk_bytes is None
                or a.physical_digits is None or a.expected_sha is None or a.game=='both'):
            p.error('incomplete synthetic worker arguments')
        worker(a.fixture,a.output,a.game,a.chunk_bytes,a.physical_digits,a.expected_sha,a.draw_count)

if __name__=='__main__':
    main()
