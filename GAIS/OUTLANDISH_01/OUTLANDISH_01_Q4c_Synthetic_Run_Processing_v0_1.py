#!/usr/bin/env python3
"""Q4c synthetic-only streaming integration, TEST_REAL/TEST_NULL.

No production runner, no production path access, no Q5. Uses the Q4b
published-format verifier in *marked test* mode and the existing Q3 v0.4
streaming matcher. Separate per-type inputs/outputs; NULL bytes and seed kept.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import random
import re

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G

HEADER = ('draw_number', 'family', 'start_digit_offset', 'matched_digits')
DECOY_HEADER = ('decoy_id', *(f'Drawn_{i}' for i in range(1, 8)))
DECOY_VERSION = 'OUTLANDISH_NULL_PY_RANDOM_SAMPLE_V1'  # bytes saved; never depend on future RNG
RUN_SCHEMA = 'Q4C_SYNTHETIC_ONLY_V1'
SCOPED = 'SYNTHETIC_Q4C_NOT_AUTHORISATION_FOR_Q5'
SYNTHETIC_ERA = {'powerball': 11, 'oz': 21}
RUN_ID = re.compile(r'TEST_(?:REAL|NULL)_[A-Za-z0-9_-]{1,48}\Z')


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _new_bytes(path: Path, data: bytes) -> None:
    with path.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def _new_json(path: Path, record: dict) -> None:
    _new_bytes(path, (json.dumps(record, indent=2, sort_keys=True)+'\n').encode('utf-8'))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def _check_test_root(roots: G.FixedRoots) -> None:
    if not isinstance(roots, G.FixedRoots) or not roots.synthetic:
        raise ValueError('Q4c runner is SYNTHETIC ONLY')
    # Revalidate marker and directories for each operation; no paths supplied by a caller.
    G.FixedRoots.test_sandbox(roots.base)
    for name in ('digits', 'histories', 'results', 'results_null'):
        target = G._inside(roots.base, roots.base/name)
        if not target.is_dir():
            raise ValueError(f'missing synthetic {name} directory')


def _historical_profile(roots: G.FixedRoots, game: str) -> G.HistoryProfile:
    if game not in SYNTHETIC_ERA:
        raise ValueError('unknown fixture game')
    first = SYNTHETIC_ERA[game]
    header = G.PB_HEADER if game == 'powerball' else G.SYNTHETIC_OZ_HEADER
    return G.HistoryProfile(game, roots.base/'histories'/f'{game}_synthetic.csv',
                            first, first + 3, header, True)


def _draw_records(game: str, numbered):
    from OUTLANDISH_01_Q3_Packed_Matcher_v0_4 import PBRecord, OzRecord
    if game == 'powerball':
        return tuple(PBRecord(i, values[:7], values[7]) for i, values in numbered)
    return tuple(OzRecord(i, values[:7], values[7:]) for i, values in numbered)


def generate_decoy_draws(game: str, *, seed: int, k: int, positions: int = 3):
    """Unambiguous text IDs and independent valid histories; return bytes + indexed rows.

    RNG algorithm/version need not be reproducible years later: original generated
    bytes are persisted in each NULL run and take precedence on every replay.
    """
    if game not in SYNTHETIC_ERA or type(seed) is not int or not 0 <= seed < 2**64:
        raise ValueError('invalid synthetic decoy game/seed')
    if type(k) is not int or not 1 <= k <= 8 or type(positions) is not int or positions != 3:
        raise ValueError('bounded K=1..8 / exactly 3 synthetic positions required')
    rng = random.Random(seed)
    text = io.StringIO(newline='')
    writer = csv.writer(text, lineterminator='\n')
    extra = ('Powerball',) if game == 'powerball' else ('Supplementary_1', 'Supplementary_2', 'Supplementary_3')
    writer.writerow((*DECOY_HEADER, *extra))
    index = []
    for history in range(1, k + 1):
        for pos in range(1, positions + 1):
            label = f'DECOY-{history:04d}-{pos:04d}'
            if game == 'powerball':
                balls = tuple(rng.sample(range(1, 36), 7)) + (rng.randrange(1, 21),)
            else:
                balls = tuple(rng.sample(range(1, 48), 10))
            ordinal = (history-1)*positions + pos
            writer.writerow((label, *balls))
            index.append((ordinal, label, balls))
    return text.getvalue().encode('utf-8'), tuple(index)


def _read_decoys(raw: bytes, *, game: str, k: int):
    if game not in SYNTHETIC_ERA or type(k) is not int or not 1 <= k <= 8:
        raise ValueError('invalid decoy identity')
    try:
        rows = list(csv.reader(io.StringIO(raw.decode('utf-8'), newline=''), strict=True))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('invalid decoy CSV') from exc
    extra = ('Powerball',) if game == 'powerball' else ('Supplementary_1', 'Supplementary_2', 'Supplementary_3')
    if not rows or tuple(rows[0]) != (*DECOY_HEADER, *extra) or len(rows) != k*3+1:
        raise ValueError('missing/mislabelled decoy rows')
    result = []
    for n, fields in enumerate(rows[1:], 1):
        expected = f'DECOY-{(n-1)//3 + 1:04d}-{(n-1)%3 + 1:04d}'
        if len(fields) != len(rows[0]) or fields[0] != expected:
            raise ValueError('decoy type/order/count mismatch')
        values=[]
        for field in fields[1:]:
            if G.INTEGER.fullmatch(field) is None:
                raise ValueError('noncanonical decoy outcome')
            values.append(int(field))
        nums=tuple(values)
        if game == 'powerball':
            if any(not 1 <= v <= 35 for v in nums[:7]) or len(set(nums[:7])) != 7 \
                    or not 1 <= nums[7] <= 20:
                raise ValueError('invalid PB decoy roles')
        else:
            if any(not 1 <= v <= 47 for v in nums) or len(set(nums)) != 10:
                raise ValueError('invalid Oz decoy roles')
        result.append((n, expected, nums))
    return tuple(result)


def _rewrite_null(internal_csv: Path, external_csv: Path, mapping: dict[int,str]):
    with internal_csv.open('r', encoding='utf-8', newline='') as src, \
            external_csv.open('x', encoding='utf-8', newline='') as out:
        reader = csv.reader(src, strict=True)
        writer = csv.writer(out, lineterminator='\n')
        if tuple(next(reader, ())) != HEADER:
            raise ValueError('wrong internal event header')
        writer.writerow(HEADER)
        for cells in reader:
            if len(cells) != 4 or G.INTEGER.fullmatch(cells[0]) is None:
                raise ValueError('invalid internal event row')
            ordinal=int(cells[0])
            if ordinal not in mapping:
                raise ValueError('NULL event references unknown decoy')
            writer.writerow((mapping[ordinal], *cells[1:]))
        out.flush()
        os.fsync(out.fileno())
    internal_csv.unlink()  # only newly created file under this new TEST run


def _verified_events(raw: bytes, *, game: str, n: int, numbered, digest: str,
                     labels: dict[str,int] | None):
    """Strict numeric event oracle reused for typed NULL labels; no packed reads."""
    from OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1 import read_events
    from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import (
        classify_events, PBRecord as CPB, OzRecord as COz, RawEvent as CEvent)
    if _sha(raw) != digest:
        raise ValueError('event CSV SHA mismatch')
    if labels is not None:
        try:
            rows=list(csv.reader(io.StringIO(raw.decode('utf-8'), newline=''), strict=True))
        except (UnicodeError, csv.Error) as exc:
            raise ValueError('invalid NULL event CSV') from exc
        if not rows or tuple(rows[0]) != HEADER:
            raise ValueError('wrong NULL event header')
        buffer=io.StringIO(newline='')
        writer=csv.writer(buffer, lineterminator='\n')
        writer.writerow(HEADER)
        for row in rows[1:]:
            if len(row) != 4 or row[0] not in labels:
                raise ValueError('NULL event must have a known text decoy ID')
            writer.writerow((labels[row[0]], *row[1:]))
        numeric=buffer.getvalue().encode('utf-8')
    else:
        numeric=raw
    loaded=read_events(numeric, game=game, logical_N=n,
                       allowed_draws={i for i,_ in numbered}, recorded_sha256=_sha(numeric))
    if game=='powerball':
        classified_draws=tuple(CPB(i, values[:7], values[7]) for i,values in numbered)
    else:
        classified_draws=tuple(COz(i, values[:7], values[7:]) for i,values in numbered)
    classified_events=tuple(CEvent(e.draw_number,e.family,e.start_digit_offset,e.matched_digits)
                            for e in loaded)
    classify_events(game, classified_events, classified_draws, effective_digits=n)
    return tuple(loaded)


def _receipt_replay(roots: G.FixedRoots, constant: str, meta: dict) -> None:
    """Inspect only receipt bytes, not source BCD (may have been removed)."""
    receipt=G._inside(roots.base,roots.receipt(constant))
    raw=receipt.read_bytes()
    if _sha(raw) != meta.get('receipt_sha256'):
        raise ValueError('receipt changed since run')
    record=json.loads(raw.decode('utf-8'))
    if not isinstance(record,dict) or record.get('format')!=G.FORMAT \
            or record.get('scope')!=G.SCOPE or record.get('constant')!=constant \
            or record.get('binary_name')!=roots.published_binary(constant).name \
            or record.get('digits_including_integer')!=meta.get('physical_digits') \
            or record.get('binary_sha256_streamed')!=meta.get('input_sha256_actual'):
        raise ValueError('receipt identity not preserved')


def _verify_run(roots: G.FixedRoots, game: str, constant: str, kind: str,
                run_id: str, *, precomplete: dict | None = None):
    _check_test_root(roots)
    if game not in SYNTHETIC_ERA or kind not in ('TEST_REAL','TEST_NULL'):
        raise ValueError('unknown Q4c run type')
    folder=roots.run_location(kind,run_id)
    # Unlike the create-only location check, replay MUST target an existing directory.
    if not folder.is_dir():
        raise ValueError('run missing')
    G._inside(roots.base, folder)
    manifest=G._inside(roots.base,folder/'run_manifest.json')
    meta=json.loads(manifest.read_bytes().decode('utf-8'))
    if not isinstance(meta,dict) or meta.get('status')!=('INCOMPLETE' if precomplete is not None else 'COMPLETE'):
        raise ValueError('run is not in the required verified state')
    if precomplete is not None:
        # Before COMPLETE: check candidate metadata in memory, but require the
        # persisted manifest to remain INCOMPLETE throughout verification.
        if precomplete.get('status') != 'INCOMPLETE':
            raise ValueError('candidate manifest not INCOMPLETE')
        meta=precomplete
    fixed={'schema':RUN_SCHEMA,'scope':SCOPED,'run_id':run_id,'run_type':kind,
           'game':game,'constant':constant,'packed_filename':roots.published_binary(constant).name,
           'event_filename':'raw_events.csv',
           'scanner':'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py'}
    if any(meta.get(key)!=value for key,value in fixed.items()):
        raise ValueError('wrong run identity or provenance')
    n=meta.get('physical_digits')
    if type(n) is not int or n<32 or meta.get('effective_digits')!=n:
        raise ValueError('invalid scan dimensions')
    if meta.get('input_sha256_actual')!=meta.get('packed_sha256_recorded'):
        raise ValueError('full source SHA not matched to receipt')
    if meta.get('bytes_hashed')!=(n+1)//2:
        raise ValueError('source was not completely hashed')
    _receipt_replay(roots,constant,meta)
    if kind=='TEST_REAL':
        profile=_historical_profile(roots,game)
        checked=G.validate_drawset(profile,expected_sha256=meta.get('drawset_sha256'))
        numbered=checked.draw_rows
        labels=None
        if 'decoy_sha256' in meta or 'seed' in meta:
            raise ValueError('REAL cannot have NULL provenance')
    else:
        if 'drawset_sha256' in meta:
            raise ValueError('NULL cannot have REAL drawset provenance')
        path=G._inside(roots.base,folder/'decoy_histories.csv')
        raw_decoys=path.read_bytes()
        if _sha(raw_decoys)!=meta.get('decoy_sha256') or meta.get('generator')!=DECOY_VERSION:
            raise ValueError('NULL decoy provenance mismatch')
        if type(meta.get('seed')) is not int or not 0<=meta['seed']<2**64:
            raise ValueError('invalid recorded NULL seed')
        decoys=_read_decoys(raw_decoys,game=game,k=meta.get('k'))
        numbered=tuple((i,v) for i,_,v in decoys)
        labels={label:i for i,label,_ in decoys}
    event_path=G._inside(roots.base,folder/'raw_events.csv')
    raw_events=event_path.read_bytes()
    loaded=_verified_events(raw_events,game=game,n=n,numbered=numbered,
                            digest=meta.get('event_sha256'),labels=labels)
    if type(meta.get('event_count')) is not int or len(loaded)!=meta['event_count']:
        raise ValueError('event count inconsistent with manifest')
    counts={family:sum(e.family==family for e in loaded) for family in sorted({e.family for e in loaded})}
    if counts!=meta.get('family_counts'):
        raise ValueError('family counts inconsistent with manifest')
    return loaded


def load_verified_synthetic_run(roots: G.FixedRoots, game: str, constant: str,
                                kind: str, run_id: str):
    """Read-only event replay: never opens or hashes the packed BCD file."""
    return _verify_run(roots,game,constant,kind,run_id)


def run_synthetic(roots: G.FixedRoots, game: str, constant: str, kind: str,
                  run_id: str, *, fixture_digits: int, seed: int | None = None,
                  k: int = 1, chunk_bytes: int | None = None,
                  fail_after_scan: bool = False) -> Path:
    """Execute one tiny new TEST run, no production paths or entry point."""
    _check_test_root(roots)
    if game not in SYNTHETIC_ERA or kind not in ('TEST_REAL','TEST_NULL') or \
            not isinstance(run_id,str) or RUN_ID.fullmatch(run_id) is None or \
            not run_id.startswith(kind+'_'):
        raise ValueError('invalid synthetic run identity')
    if kind=='TEST_REAL' and (seed is not None or k!=1):
        raise ValueError('REAL-like test cannot accept NULL parameters')
    if kind=='TEST_NULL' and (type(seed) is not int or not 0<=seed<2**64):
        raise ValueError('NULL-like test requires explicit reproducible seed')
    source=G.validate_published_source(roots,constant,fixture_digits=fixture_digits)
    result_dir=roots.validate_run_location(kind,run_id,roots.run_location(kind,run_id))
    if kind=='TEST_REAL':
        history=G.validate_drawset(_historical_profile(roots,game))
        numbered=history.draw_rows
        decoy_bytes=None
    else:
        decoy_bytes,decoys=generate_decoy_draws(game,seed=seed,k=k)
        numbered=tuple((i,balls) for i,_,balls in decoys)
    from OUTLANDISH_01_Q3_Packed_Matcher_v0_4 import (
        scan_packed_stream,scan_packed_oz_stream)
    # Imports and all source/profile checks are complete before create-only run folder.
    result_dir.mkdir(exist_ok=False)
    basic={'schema':RUN_SCHEMA,'scope':SCOPED,'status':'INCOMPLETE','run_id':run_id,
           'run_type':kind,'game':game,'constant':constant,
           'event_filename':'raw_events.csv','scanner':'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
           'physical_digits':source.digits,'effective_digits':source.digits,
           'packed_filename':source.path.name,'receipt_sha256':source.receipt_sha256,
           'packed_sha256_recorded':source.packed_sha256,'started_utc':_now()}
    if kind=='TEST_REAL':
        basic['drawset_sha256']=history.sha256
    else:
        basic.update(seed=seed,k=k,generator=DECOY_VERSION,
                     decoy_sha256=_sha(decoy_bytes))
    manifest=result_dir/'run_manifest.json'
    _new_json(manifest,basic)
    if decoy_bytes is not None:
        _new_bytes(result_dir/'decoy_histories.csv',decoy_bytes)
    output=result_dir/('raw_events.csv' if kind=='TEST_REAL' else 'events_internal.csv')
    scan=scan_packed_stream if game=='powerball' else scan_packed_oz_stream
    result=scan(source.path,physical_digits=source.digits,effective_digits=source.digits,
                draws=_draw_records(game,numbered),output_csv=output,
                chunk_bytes=chunk_bytes,expected_full_sha256=source.packed_sha256)
    source.check_completed_stream(result.sha256_full_packed,result.bytes_hashed)
    if (result.event_csv != output or result.physical_digits != source.digits
            or result.effective_digits != source.digits or
            result.event_sha256 != G._sha(output)):
        raise ValueError('scanner stream result/event digest mismatch')
    if fail_after_scan:
        raise RuntimeError('injected synthetic failure: run remains INCOMPLETE')
    if kind=='TEST_NULL':
        _rewrite_null(output,result_dir/'raw_events.csv',
                      {i:label for i,label,_ in decoys})
    raw=(result_dir/'raw_events.csv').read_bytes()
    complete={**basic,'event_sha256':_sha(raw),'event_count':result.event_count,
              'family_counts':result.family_counts,'bytes_hashed':result.bytes_hashed,
              'input_sha256_actual':result.sha256_full_packed,
              'chunk_bytes':result.chunk_bytes,'finished_utc':_now()}
    # Validate semantic/event/source/NULL identity before publishing COMPLETE.
    _verify_run(roots,game,constant,kind,run_id,precomplete=complete)
    complete['status']='COMPLETE'
    temp_manifest=result_dir/'run_manifest.next.json'
    _new_json(temp_manifest,complete)
    os.replace(temp_manifest,manifest)
    return result_dir


if __name__=='__main__':
    raise SystemExit('No Q4c CLI: synthetic harness only; Q5 forbidden')
