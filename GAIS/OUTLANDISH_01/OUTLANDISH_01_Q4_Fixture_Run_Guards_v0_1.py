#!/usr/bin/env python3
"""OUTLANDISH_01 Q4, synthetic-only REAL/NULL *analogues* and run validation.

This has NO production entry point, no published profile, no command-line
arguments, no discovery of production files and no unrestricted path selection.
Every call requires a purpose-built temporary sandbox with a magic marker.
TEST_REAL and TEST_NULL are deliberately not the ratified REAL/NULL statuses.

Shows a simple eventual design: sealed source receipt and complete drawset,
streaming output in a new incomplete run folder, atomic manifest completion,
then event/drawset SHA verification and classify WITHOUT rereading packed BCD.
The real production adapter, exact game profiles and NULL decoy machinery must
be independently qualified later. This is a fixture qualification tool only.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re

from OUTLANDISH_01_Q3_Packed_Matcher_v0_4 import (
    PBRecord, OzRecord, RawEvent, scan_packed_stream, scan_packed_oz_stream,
)
from OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1 import read_events
from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import (
    classify_events, PBRecord as ClassifiedPBRecord,
    OzRecord as ClassifiedOzRecord, RawEvent as ClassifiedRawEvent,
)

MAGIC = b'OUTLANDISH_Q4_SYNTHETIC_SANDBOX_V1\n'
FORMAT = 'OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1'
SCOPE = 'PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY'
TEST_SCOPE = 'SYNTHETIC_Q4_ONLY_NOT_REAL_OR_NULL_PRODUCTION'
SHA = re.compile(r'[0-9a-f]{64}\Z')
DECIMAL = re.compile(r'(?:0|[1-9][0-9]*)\Z')
TEST_HEADER_PB = ('draw_number', *(f'Drawn_{i}' for i in range(1, 8)), 'Powerball')
TEST_HEADER_OZ = ('draw_number', *(f'Drawn_{i}' for i in range(1, 8)),
                  'Supplementary_1', 'Supplementary_2', 'Supplementary_3')
EVENT_HEADER = ('draw_number', 'family', 'start_digit_offset', 'matched_digits')


def _sha_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for piece in iter(lambda: f.read(1_048_576), b''):
            h.update(piece)
    return h.hexdigest()


def _same_digest(actual: str, recorded: object, what: str) -> None:
    if not isinstance(recorded, str) or not SHA.fullmatch(recorded) or actual != recorded:
        raise ValueError(f'{what} SHA-256 mismatch or invalid digest')


def _no_link_component(root: Path, p: Path) -> Path:
    """Resolve only paths under a named TEST sandbox; refuse link/junction chains."""
    root = Path(root).absolute()
    p = Path(p).absolute()
    try:
        parts = p.relative_to(root).parts
    except ValueError as e:
        raise ValueError('path outside synthetic sandbox') from e
    for check in (root, *(root.joinpath(*parts[:i]) for i in range(1, len(parts)+1))):
        if check.is_symlink() or bool(getattr(check, 'is_junction', lambda: False)()):
            raise ValueError('symlink/junction in protected synthetic path')
    if not p.resolve(strict=False).is_relative_to(root.resolve(strict=True)):
        raise ValueError('resolved path outside synthetic sandbox')
    return p


def _fixture_root(root: Path) -> Path:
    root = Path(root).absolute()
    if not root.name.startswith('OUTLANDISH_Q4_SYNTHETIC_ONLY_'):
        raise ValueError('fixture root must have synthetic-only name')
    if not root.is_dir() or root.is_symlink():
        raise ValueError('invalid fixture root')
    marker = _no_link_component(root, root / 'SYNTHETIC_FIXTURE_MARKER')
    if not marker.is_file() or marker.read_bytes() != MAGIC:
        raise ValueError('missing synthetic-only sandbox marker')
    return root


def _file(root: Path, path: Path) -> Path:
    checked = _no_link_component(root, path)
    if not checked.is_file() or checked.stat().st_nlink < 1:
        raise ValueError('missing ordinary sandbox file')
    return checked


def _stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


@dataclass(frozen=True)
class FixtureProfile:
    root: Path
    game: str
    run_type: str                       # TEST_REAL or TEST_NULL only
    constant: str
    first_draw: int
    cutoff_exclusive: int

    def checked(self) -> 'FixtureProfile':
        _fixture_root(self.root)
        if self.game not in ('powerball', 'oz') or self.constant != 'phi':
            raise ValueError('fixture identity does not match fixed simulated profile')
        if self.run_type not in ('TEST_REAL', 'TEST_NULL'):
            raise ValueError('only TEST_REAL or TEST_NULL permitted')
        if type(self.first_draw) is not int or type(self.cutoff_exclusive) is not int:
            raise ValueError('invalid fixture era types')
        if not (1 <= self.first_draw < self.cutoff_exclusive <= 20
                and self.cutoff_exclusive - self.first_draw == 3):
            raise ValueError('fixture profile permits exactly three synthetic draw positions')
        # No real Powerball history number can be admitted by this profile.
        return self

    @property
    def stem(self) -> str:
        return f'{self.game}_{self.run_type}_SYNTHETIC_NOT_REAL'

    @property
    def packed(self) -> Path:
        return Path(self.root) / 'fixture_digits' / (self.stem + '.packed.bin')

    @property
    def receipt(self) -> Path:
        return self.packed.with_name(self.packed.name + '.wsl-receipt.json')

    @property
    def draws_file(self) -> Path:
        return Path(self.root) / 'fixture_histories' / (self.stem + '.csv')

    @property
    def result_root(self) -> Path:
        directory = 'fixture_results_real' if self.run_type == 'TEST_REAL' else 'fixture_results_null'
        return Path(self.root) / directory


def _receipt(profile: FixtureProfile) -> tuple[dict, str]:
    path = _file(profile.root, profile.packed)
    receipt = _file(profile.root, profile.receipt)
    record = json.loads(receipt.read_text(encoding='utf-8'))
    if not isinstance(record, dict):
        raise ValueError('receipt is not an object')
    if record.get('format') != FORMAT or type(record.get('format_version')) is not int \
            or record['format_version'] != 1 or record.get('scope') != SCOPE:
        raise ValueError('invalid BCD format/version/receipt scope')
    n = record.get('digits_including_integer')
    if (record.get('constant') != profile.constant or type(n) is not int
            or not 32 <= n <= 4000 or record.get('binary_name') != path.name
            or type(record.get('packed_bytes')) is not int
            or record['packed_bytes'] != (n+1)//2
            or path.stat().st_size != (n+1)//2):
        raise ValueError('incorrect source identity/size/receipt')
    digest = record.get('binary_sha256_streamed')
    if not isinstance(digest, str) or not SHA.fullmatch(digest):
        raise ValueError('invalid source SHA in receipt')
    # This tiny fixture specifically has one full-size sample. Do not assume
    # that production receipts have this layout; production uses sample_plan.
    samples = record.get('samples')
    if not isinstance(samples, list) or len(samples) != 1 or not isinstance(samples[0], dict):
        raise ValueError('invalid synthetic receipt sample plan')
    s = samples[0]
    if (type(s.get('offset_bytes')) is not int or s['offset_bytes'] != 0
            or type(s.get('size')) is not int or s['size'] != path.stat().st_size):
        raise ValueError('synthetic receipt sample offset/length mismatch')
    _same_digest(_sha_file(path), s.get('sha256'), 'sampled packed input')
    _same_digest(s['sha256'], digest, 'packed receipt sample/full')
    return record, _sha_file(receipt)


def _draws(profile: FixtureProfile):
    path = _file(profile.root, profile.draws_file)
    expected_header = TEST_HEADER_PB if profile.game == 'powerball' else TEST_HEADER_OZ
    with path.open('r', encoding='utf-8', newline='') as handle:
        parser = csv.reader(handle, strict=True)
        if tuple(next(parser, ())) != expected_header:
            raise ValueError('incorrect fixture game draw header')
        rows = list(parser)
    if len(rows) != profile.cutoff_exclusive-profile.first_draw:
        raise ValueError('missing/extra fixture historical draws')
    result=[]
    for index, row in enumerate(rows):
        if len(row) != len(expected_header):
            raise ValueError('incorrect game draw field count')
        identifier = row[0]
        if profile.run_type == 'TEST_REAL':
            if not DECIMAL.fullmatch(identifier) or int(identifier) != profile.first_draw+index:
                raise ValueError('out-of-era/nonconsecutive/duplicate REAL-like draw IDs')
            internal = int(identifier)
        else:
            expected_id = f'DECOY-{index+1:04d}'
            if identifier != expected_id:
                raise ValueError('NULL-like history must have unique text DECOY identifiers')
            internal = profile.first_draw+index  # private, not published
        try:
            values = tuple(int(s) if DECIMAL.fullmatch(s) else -1 for s in row[1:])
        except (ValueError, TypeError):
            raise ValueError('noncanonical two-digit outcome value') from None
        if any(str(v) != s or v == -1 for v, s in zip(values, row[1:])):
            raise ValueError('noncanonical outcome field')
        if profile.game == 'powerball':
            rec = PBRecord(internal, values[:7], values[7])
        else:
            rec = OzRecord(internal, values[:7], values[7:])
        result.append(rec)
    return tuple(result), _sha_file(path)


def _json_create(path: Path, body: dict) -> None:
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, indent=2, sort_keys=True)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def _json_atomic_complete(path: Path, body: dict) -> None:
    staging = path.with_name('run_manifest.next.json')
    _json_create(staging, body)
    os.replace(staging, path)  # replaces only this new run's STARTED manifest


def _map_null_to_decoys(intermediate: Path, final_csv: Path, profile: FixtureProfile) -> str:
    """Small, streaming second pass over *event CSV*, never over digit file."""
    with intermediate.open('r',encoding='utf-8',newline='') as r, \
            final_csv.open('x',encoding='utf-8',newline='') as w:
        source=csv.reader(r,strict=True)
        dest=csv.writer(w,lineterminator='\n')
        if tuple(next(source,())) != EVENT_HEADER:
            raise ValueError('wrong internal NULL event header')
        dest.writerow(EVENT_HEADER)
        for cells in source:
            if len(cells)!=4 or not DECIMAL.fullmatch(cells[0]):
                raise ValueError('incorrect NULL internal event row')
            index=int(cells[0])-profile.first_draw
            if not 0<=index<3:
                raise ValueError('NULL internal event unknown draw')
            dest.writerow((f'DECOY-{index+1:04d}', *cells[1:]))
    intermediate.unlink()
    return _sha_file(final_csv)


def _validate_test_events(raw: bytes, *, profile: FixtureProfile, n: int,
                          drawset: tuple, expected_sha: str) -> tuple[RawEvent, ...]:
    _same_digest(_sha_bytes(raw), expected_sha, 'event file')
    if profile.run_type == 'TEST_REAL':
        loaded=read_events(raw,game=profile.game,logical_N=n,
                           allowed_draws={x.draw_number for x in drawset},
                           recorded_sha256=expected_sha)
        return tuple(RawEvent(x.draw_number,x.family,x.start_digit_offset,x.matched_digits)
                     for x in loaded)
    # NULL's external typed labels cannot be passed to REAL's integer loader.
    try:
        rows=list(csv.reader(raw.decode('utf-8').splitlines(),strict=True))
    except UnicodeDecodeError as e:
        raise ValueError('invalid NULL event encoding') from e
    if not rows or tuple(rows[0]) != EVENT_HEADER:
        raise ValueError('wrong NULL event header')
    numeric=[]
    for cells in rows[1:]:
        if len(cells)!=4 or not re.fullmatch(r'DECOY-000[123]',cells[0]):
            raise ValueError('invalid NULL event text ID')
        pos=int(cells[0][-1])-1
        numeric.append((str(profile.first_draw+pos), *cells[1:]))
    # Apply same strict order, identity, end and family checks as REAL.
    import io
    dest=io.StringIO(newline='')
    writer=csv.writer(dest,lineterminator='\n')
    writer.writerow(EVENT_HEADER)
    writer.writerows(numeric)
    numeric_raw=dest.getvalue().encode('utf-8')
    loaded=read_events(numeric_raw,game=profile.game,logical_N=n,
                      allowed_draws={x.draw_number for x in drawset},
                      recorded_sha256=_sha_bytes(numeric_raw))
    return tuple(RawEvent(x.draw_number,x.family,x.start_digit_offset,x.matched_digits)
                 for x in loaded)


def run_fixture(profile: FixtureProfile, run_id: str, *,
                effective_digits: int | None = None,
                chunk_bytes: int | None = None,
                inject_failure_after_scan: bool = False) -> Path:
    """One NEW synthetic run: fixed paths from profile, never a production API."""
    profile.checked()
    if not re.fullmatch(r'TEST_[A-Za-z0-9_]{1,40}',run_id):
        raise ValueError('only TEST run IDs accepted')
    receipt, receipt_sha=_receipt(profile)
    draws,draw_sha=_draws(profile)
    size=receipt['digits_including_integer']
    n=size if effective_digits is None else effective_digits
    if type(n) is not int or not 1 <= n <= size:
        raise ValueError('invalid effective digit prefix')
    root=_no_link_component(profile.root,profile.result_root)
    if not root.is_dir():
        raise ValueError('fixed result root missing')
    directory=_no_link_component(profile.root,root/run_id)
    directory.mkdir(exist_ok=False)
    manifest=directory/'run_manifest.json'
    basic=dict(schema='Q4_SYNTHETIC_FIXTURE_V1', execution_scope=TEST_SCOPE,
               run_id=run_id, run_type=profile.run_type, game=profile.game,
               constant=profile.constant, packed_filename=profile.packed.name,
               receipt_sha256=receipt_sha,
               packed_sha256_recorded=receipt['binary_sha256_streamed'],
               physical_digits=size, effective_digits=n,
               drawset_filename=profile.draws_file.name,drawset_sha256=draw_sha,
               first_draw=profile.first_draw,cutoff_exclusive=profile.cutoff_exclusive,
               scanner='OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
               event_filename='raw_events.csv',status='INCOMPLETE',
               started_utc=_stamp())
    _json_create(manifest,basic)
    # Failure must leave a conspicuous INCOMPLETE manifest, not an accepted file.
    engine_file=directory/('events_internal.csv' if profile.run_type=='TEST_NULL' else 'raw_events.csv')
    scan=(scan_packed_stream if profile.game=='powerball' else scan_packed_oz_stream)
    result=scan(profile.packed,physical_digits=size,effective_digits=n,
                draws=draws,output_csv=engine_file,chunk_bytes=chunk_bytes,
                expected_full_sha256=receipt['binary_sha256_streamed'])
    if inject_failure_after_scan:
        raise RuntimeError('deliberate fixture failure before completion')
    if profile.run_type=='TEST_NULL':
        event_sha=_map_null_to_decoys(engine_file,directory/'raw_events.csv',profile)
    else:
        event_sha=result.event_sha256
    completed=basic | dict(status='COMPLETE',finished_utc=_stamp(),
                           input_sha256_actual=result.sha256_full_packed,
                           bytes_hashed=result.bytes_hashed,
                           chunk_bytes=result.chunk_bytes,
                           event_sha256=event_sha,event_count=result.event_count,
                           family_counts=result.family_counts)
    _json_atomic_complete(manifest,completed)
    return directory


def load_verified_fixture(profile: FixtureProfile, run_id: str,
                          *, require_type: str = 'TEST_REAL') -> tuple[RawEvent,...]:
    """Fail-closed fixture reader/classification source; NEVER opens packed BCD."""
    profile.checked()
    if require_type not in ('TEST_REAL','TEST_NULL') or profile.run_type != require_type:
        raise ValueError('REAL/NULL type mismatch; fail closed')
    if not re.fullmatch(r'TEST_[A-Za-z0-9_]{1,40}',run_id):
        raise ValueError('invalid TEST run identity')
    folder=_no_link_component(profile.root,profile.result_root/run_id)
    if not folder.is_dir():
        raise ValueError('requested run absent')
    raw_manifest=_file(profile.root,folder/'run_manifest.json').read_text(encoding='utf-8')
    meta=json.loads(raw_manifest)
    if not isinstance(meta,dict) or meta.get('status')!='COMPLETE':
        raise ValueError('run incomplete or malformed; no publish')
    fixed={'schema':'Q4_SYNTHETIC_FIXTURE_V1','execution_scope':TEST_SCOPE,
           'run_id':run_id,'run_type':require_type,'game':profile.game,
           'constant':profile.constant,'packed_filename':profile.packed.name,
           'drawset_filename':profile.draws_file.name,'first_draw':profile.first_draw,
           'cutoff_exclusive':profile.cutoff_exclusive,'event_filename':'raw_events.csv',
           'scanner':'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py'}
    if any(meta.get(key)!=value for key,value in fixed.items()):
        raise ValueError('manifest identity/type/scope/profile mismatch')
    receipt,receipt_sha=_receipt_metadata_only(profile)
    _same_digest(receipt_sha,meta.get('receipt_sha256'),'receipt file')
    if receipt['digits_including_integer']!=meta.get('physical_digits') or \
            receipt['binary_sha256_streamed']!=meta.get('packed_sha256_recorded') or \
            receipt['binary_sha256_streamed']!=meta.get('input_sha256_actual'):
        raise ValueError('receipt and scanner digest identity mismatch')
    n=meta.get('effective_digits')
    if type(n) is not int or not 1<=n<=receipt['digits_including_integer']:
        raise ValueError('invalid scan prefix in manifest')
    draws,draw_sha=_draws(profile)
    _same_digest(draw_sha,meta.get('drawset_sha256'),'drawset file')
    raw=_file(profile.root,folder/'raw_events.csv').read_bytes()
    events=_validate_test_events(raw,profile=profile,n=n,drawset=draws,
                                 expected_sha=meta.get('event_sha256'))
    if type(meta.get('event_count')) is not int or meta['event_count']!=len(events):
        raise ValueError('manifest event count mismatch')
    counts={f:sum(e.family==f for e in events) for f in set(e.family for e in events)}
    if counts != meta.get('family_counts'):
        raise ValueError('manifest family-count mismatch')
    # Pure draw+event classifier: NO packed source read from this point onward.
    # The already-qualified classifier imports the frozen v0.2 dataclasses.
    # Convert at this IO boundary without changing the classifier or scanner.
    if profile.game == 'powerball':
        class_draws = tuple(ClassifiedPBRecord(d.draw_number, d.mains_drawn, d.powerball)
                            for d in draws)
    else:
        class_draws = tuple(ClassifiedOzRecord(d.draw_number, d.mains_drawn,
                                               d.supplementaries_drawn) for d in draws)
    class_events = tuple(ClassifiedRawEvent(e.draw_number, e.family,
                                           e.start_digit_offset, e.matched_digits)
                         for e in events)
    classify_events(profile.game,class_events,class_draws,effective_digits=n)
    return events


def _receipt_metadata_only(profile: FixtureProfile) -> tuple[dict,str]:
    """Reader checks receipt metadata + digest, but never rehashes packed bytes."""
    rp=_file(profile.root,profile.receipt)
    record=json.loads(rp.read_text(encoding='utf-8'))
    if not isinstance(record,dict) or record.get('format')!=FORMAT or \
            record.get('scope')!=SCOPE or record.get('format_version')!=1:
        raise ValueError('invalid receipt on replay')
    n=record.get('digits_including_integer')
    if type(n) is not int or n<32 or n>4000 or \
            record.get('binary_name')!=profile.packed.name or \
            record.get('constant')!=profile.constant or \
            record.get('packed_bytes')!=(n+1)//2:
        raise ValueError('invalid receipt identity on replay')
    return record,_sha_file(rp)
