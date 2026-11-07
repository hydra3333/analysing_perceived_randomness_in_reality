#!/usr/bin/env python3
"""NumPy chunk scanner for packed BCD mathematical digits, Powerball P1/P2/P3.

Preserves legacy FIXED2/P1/P2/P3 definitions, offsets and pre-holdout cutoff.
Checks the streamed SHA-256 IN THE SCANNING PASS when scanning a whole file,
not via an additional verification pass. New any-order and Oz Lotto rules
are deliberately deferred as separately versioned changes.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date,datetime,timezone
from itertools import combinations
import csv
import hashlib
import json
from pathlib import Path
import sys
import time
import uuid

try:
    import numpy as np
except ImportError as exc:
    raise SystemExit('NumPy is required in the existing Windows project venv') from exc

from wsl_format import PREFIXES, packed_bytes, safe_regular
from wsl_verify_windows import read_receipt, verify_packed

CUTOFF=1577
EXPECTED_HEADER=('Draw_Number','Date',*(f'Drawn_{n}' for n in range(1,8)),'Powerball')

@dataclass(frozen=True)
class Draw:
    number:int
    drawn:tuple[int,...]
    powerball:int


def load_draws(path:Path)->list[Draw]:
    """Reject at/after cutoff BEFORE reading any restricted outcome fields."""
    inp=safe_regular(path)
    draws=[]
    with inp.open('rb') as f:
        header=f.readline().rstrip(b'\r\n').decode('utf-8-sig')
        if header!=','.join(EXPECTED_HEADER):
            raise ValueError('wrong pre-holdout Powerball CSV header')
        while True:
            initial=f.tell()
            number=bytearray()
            while True:
                c=f.read(1)
                if not c:
                    if number: raise ValueError('truncated Draw_Number')
                    break
                if c==b',':break
                if len(number)>=9 or not 48<=c[0]<=57:
                    raise ValueError('invalid draw ID field')
                number.extend(c)
            if not c:break
            if not number or (len(number)>1 and number[0]==48):
                raise ValueError('noncanonical draw number')
            draw_no=int(number)
            if draw_no >= CUTOFF:
                raise ValueError(f'draw {draw_no} violates pre-holdout cutoff {CUTOFF}')
            if draws and draw_no!=draws[-1].number+1:
                raise ValueError('draws must be strictly consecutive')
            f.seek(initial)
            fields=next(csv.reader([f.readline().decode('utf-8',errors='strict')],strict=True))
            if len(fields)!=10:raise ValueError('wrong draw field count')
            if date.fromisoformat(fields[1]).isoformat()!=fields[1]:
                raise ValueError('invalid draw date')
            values=fields[2:]
            if not all(v.isascii() and v.isdecimal() and v.isdigit() and not v.startswith('0') for v in values):
                raise ValueError('noncanonical ball values')
            main=tuple(map(int,values[:7])); powerball=int(values[7])
            if len(set(main))!=7 or not all(1<=n<=35 for n in main) or not 1<=powerball<=20:
                raise ValueError('invalid ball values')
            draws.append(Draw(draw_no,main,powerball))
    if not draws:raise ValueError('empty pre-holdout CSV')
    return draws


def build_index(draws:list[Draw]):
    p1=defaultdict(list);p2=defaultdict(list);p3=defaultdict(list)
    for d in draws:
        p1[(*d.drawn,d.powerball)].append(d.number)
        p2[d.drawn].append(d.number)
        for six in combinations(d.drawn,6):
            p3[(tuple(sorted(six)),d.powerball)].append(d.number)
    return p1,p2,p3


def unpack_numpy(packed:bytes, digit_limit:int)->np.ndarray:
    """Bounded vectorized nibble decoding, not whole-file expansion."""
    ar=np.frombuffer(packed,dtype=np.uint8)
    digits=np.empty(len(ar)*2,dtype=np.uint8)
    digits[0::2]=ar>>4
    digits[1::2]=ar&15
    if digit_limit>len(digits):raise ValueError('short packed read')
    digits=digits[:digit_limit]
    if np.any(digits>9):raise ValueError('invalid BCD nibble')
    return digits


def closest_pair(a:list[int],b:list[int]):
    if not a or not b:return None
    i=j=0;best=None
    while i<len(a) and j<len(b):
        delta=b[j]-a[i]
        if best is None or (abs(delta),delta)<(abs(best),best):best=delta
        if a[i]<b[j]:i+=1
        else:j+=1
    return best


def scan_file(inp:Path,record:dict,draws:list[Draw],output_root:Path,
              *,chunk_digits:int=4_000_000,max_digits:int|None=None,
              progress_seconds:float=5.0)->dict:
    inp=safe_regular(inp)
    output_root=output_root.absolute()
    if not output_root.is_dir() or output_root.is_symlink():
        raise ValueError('pre-existing ordinary report root required')
    if chunk_digits<32 or chunk_digits>64_000_000 or chunk_digits%2:
        raise ValueError('chunk_digits must be even, 32..64 million')
    if progress_seconds<=0:raise ValueError('positive progress interval required')
    total=record['digits_including_integer']
    n=total if max_digits is None else min(total,max_digits)
    if n<14:raise ValueError('minimum 14 decimal digits')
    expected_size=packed_bytes(total)
    if inp.stat().st_size!=expected_size:raise ValueError('candidate changed size')
    indexes=build_index(draws)
    p1,p2,p3=indexes
    run_dir=output_root/f'packed_run_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{uuid.uuid4().hex[:8]}'
    run_dir.mkdir(exist_ok=False)
    matches=run_dir/'matches.csv';transitions=run_dir/'transitions.csv'
    positions=defaultdict(list);hits=Counter();candidates=0
    start_time=time.perf_counter();next_update=start_time+progress_seconds
    sha=hashlib.sha256()
    with inp.open('rb') as stream, matches.open('x',encoding='utf-8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(('packed_file','draw_number','category','start_digit_offset_0_based',
                         'end_digit_offset_exclusive','matched_decimal_digits'))
        for start in range(0,n,chunk_digits):
            span=min(chunk_digits,n-start)
            # Chunk boundaries are even digit offsets, with 15-digit lookahead.
            look=min(total-start,span+15)
            stream.seek(start//2)
            raw=stream.read(packed_bytes(look))
            if len(raw)!=packed_bytes(look):raise ValueError('truncated packed digit file')
            digits=unpack_numpy(raw,look)
            # Hash each physical packed byte exactly once, without lookahead.
            sha.update(raw[:packed_bytes(span)])
            valid=min(span,max(0,len(digits)-13))
            if valid:
                balls=[digits[2*j:2*j+valid].astype(np.uint16)*10 +
                       digits[2*j+1:2*j+1+valid] for j in range(7)]
                six_ok=np.ones(valid,dtype=np.bool_)
                for ball in balls[:6]:six_ok &= (ball>=1)&(ball<=35)
                p3_ok=six_ok&(balls[6]>=1)&(balls[6]<=20)
                p2_ok=six_ok&(balls[6]>=1)&(balls[6]<=35)
                indices=np.flatnonzero(p2_ok|p3_ok)
                candidates+=len(indices)
                for ii in indices:
                    i=int(ii)
                    six=tuple(int(b[i]) for b in balls[:6])
                    if len(set(six))!=6:continue
                    seventh=int(balls[6][i]);pos=start+i
                    text=lambda count:bytes(digits[i:i+count]+48).decode('ascii')
                    if bool(p3_ok[i]):
                        for d in p3.get((tuple(sorted(six)),seventh),()):
                            positions[(d,3)].append(pos);hits[3]+=1
                            writer.writerow((inp.name,d,'P3',pos,pos+14,text(14)))
                    if bool(p2_ok[i]) and seventh not in six:
                        seven=(*six,seventh)
                        for d in p2.get(seven,()):
                            positions[(d,2)].append(pos);hits[2]+=1
                            writer.writerow((inp.name,d,'P2',pos,pos+14,text(14)))
                        if i+15<len(digits):
                            pb=int(digits[i+14])*10+int(digits[i+15])
                            if 1<=pb<=20:
                                for d in p1.get((*seven,pb),()):
                                    positions[(d,1)].append(pos);hits[1]+=1
                                    writer.writerow((inp.name,d,'P1',pos,pos+16,text(16)))
            done=start+span;now=time.perf_counter()
            if now>=next_update or done==n:
                print(f'SCAN {done:,}/{n:,} digits; matches P1/P2/P3 '
                      f'{hits[1]}/{hits[2]}/{hits[3]}',flush=True)
                next_update=now+progress_seconds
    # Comparing digest is available at zero extra I/O during an entire scan.
    full=(n==total)
    if full and sha.hexdigest()!=record['binary_sha256_streamed']:
        raise ValueError('FULL SCAN SHA DIFFERS from converter streamed SHA; report incomplete, no approval')
    with transitions.open('x',encoding='utf-8',newline='') as out:
        w=csv.writer(out)
        w.writerow(('draw_W','draw_W_plus_1','W_P1','W_P2','W_P3',
                    'next_P1','next_P2','next_P3','min_signed_delta_W_P1_to_next_P1',
                    'min_signed_delta_W_P1_to_next_P2','min_signed_delta_W_P1_to_next_P3'))
        for prev,nxt in zip(draws,draws[1:]):
            x=[len(positions[prev.number,k]) for k in (1,2,3)]
            y=[len(positions[nxt.number,k]) for k in (1,2,3)]
            if sum(x) and sum(y):
                diffs=[closest_pair(positions[prev.number,1],positions[nxt.number,k]) for k in (1,2,3)]
                w.writerow((prev.number,nxt.number,*x,*y,*('' if d is None else d for d in diffs)))
    summary={'format':record['format'],'constant':record['constant'],
             'category_definition':{'P1':'7 main drawn order + PB',
                                    'P2':'7 main drawn order',
                                    'P3':'any six distinct main, any order + PB'},
             'holdout_cutoff_exclusive':CUTOFF,
             'draw_count':len(draws),'scanned_digits':n,'scanned_full':full,
             'scanned_packed_sha256':sha.hexdigest(),
             'digest_compared_to_conversion_receipt':full,
             'candidate_offsets_examined':candidates,
             'match_counts':{f'P{k}':hits[k] for k in (1,2,3)},
             'scan_wall_seconds':round(time.perf_counter()-start_time,3),
             'input':str(inp),'matches':str(matches),'transitions':str(transitions)}
    (run_dir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print('SCAN PASS; results',run_dir)
    return summary


def main(argv=None)->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--draws',type=Path,required=True,help='pre-holdout-only fixed2 CSV')
    parser.add_argument('--output-root',type=Path,required=True,help='existing results folder')
    parser.add_argument('--chunk-digits',type=int,default=4_000_000)
    parser.add_argument('--prefix-digits',type=int)
    parser.add_argument('--progress-seconds',type=float,default=5.0)
    parser.add_argument('--run',action='store_true',help='without this, print preview only')
    a=parser.parse_args(argv)
    try:
        record=read_receipt(a.input)
        load_draws(a.draws) # safety check also in preview
        if not a.run:
            print('PREVIEW ONLY: packed Powerball P1/P2/P3 scan; no outputs written')
            print('INPUT:',a.input,'DIGITS:',record['digits_including_integer'])
            print('OUTPUT:',a.output_root);return 0
        verify_packed(a.input)
        scan_file(a.input,record,load_draws(a.draws),a.output_root,
                  chunk_digits=a.chunk_digits,max_digits=a.prefix_digits,
                  progress_seconds=a.progress_seconds)
        return 0
    except (OSError,ValueError,TypeError,json.JSONDecodeError,csv.Error) as exc:
        print(f'PACKED SCAN STOP: {exc}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
