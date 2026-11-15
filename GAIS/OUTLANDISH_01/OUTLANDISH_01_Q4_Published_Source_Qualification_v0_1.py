#!/usr/bin/env python3
"""Q4 published-format receipt/profile/root guards, SYNTHETIC-only tests.

A marked TemporaryDirectory is the only source for test digits/draws. The
future production scan API does not exist here. No real input or history reads.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G


def refuse(label: str, action, error: str | None = None):
    try:
        action()
    except (ValueError, FileExistsError, TypeError) as exc:
        if error and error not in str(exc):
            raise AssertionError(f'{label}: wrong refusal: {exc}') from exc
        return 1
    raise AssertionError(f'{label}: invalid input was accepted')


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2)+'\n', encoding='utf-8')


def serialize_csv(header, rows) -> bytes:
    text=io.StringIO(newline='')
    writer=csv.writer(text,lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)
    return text.getvalue().encode('utf-8')


def history_rows(game: str, first: int):
    if game=='powerball':
        return [(first, '2026-01-01', 1,2,3,4,5,6,7, 1),
                (first+1, '2026-01-08', 8,9,10,11,12,13,14, 20),
                (first+2, '2026-01-15', 15,16,17,18,19,20,21, 3)]
    return [(first, '2026-01-01', 1,2,3,4,5,6,7, 8,9,10),
            (first+1,'2026-01-08', 11,12,13,14,15,16,17, 18,19,20),
            (first+2,'2026-01-15', 21,22,23,24,25,26,27, 28,29,30)]


def prepare(work: Path):
    root=work/'OUTLANDISH_Q4_SOURCE_SYNTHETIC_ONLY_v01'
    root.mkdir()
    (root/'SYNTHETIC_MARKER').write_bytes(G.MAGIC)
    for sub in ('digits','histories','results','results_null'):
        (root/sub).mkdir()
    roots=G.FixedRoots.test_sandbox(root)
    # 10,001 logical digits -> odd low-nibble padding. The binary is >4096
    # bytes, so its REAL converter-style deterministic multi-block plan applies.
    text=(b'31415926535897932384626433832795' * 313)[:10_001]
    text=text.ljust(10_001,b'9')
    packed=bytes.fromhex((text+b'0').decode('ascii'))
    path=roots.published_binary('phi')
    path.write_bytes(packed)
    digest=hashlib.sha256(packed).hexdigest()
    plan=G.sample_plan(len(packed))
    receipt={'format': G.FORMAT,'format_version':1,'scope':G.SCOPE,
             'verification_policy':'STREAM_ALL_SOURCE_VALIDATE;SHA256_WHILE_WRITE;SAMPLED_OUTPUT_READBACK',
             'constant':'phi', 'binary_name':path.name,
             'digits_including_integer':len(text), 'packed_bytes':len(packed),
             'binary_sha256_streamed':digest,
             'sample_block_length':plan[0][1],
             'samples':[{'offset_bytes':s,'size':n,
                         'sha256':hashlib.sha256(packed[s:s+n]).hexdigest()} for s,n in plan]}
    write_json(roots.receipt('phi'),receipt)
    return roots, receipt, text


def mutate_json(path, original, change, action, label):
    variant=json.loads(json.dumps(original))
    change(variant)
    if json.dumps(variant,sort_keys=True)==json.dumps(original,sort_keys=True):
        raise AssertionError(f'{label}: mutation made no change')
    try:
        write_json(path,variant)
        return refuse(label,action)
    finally:
        write_json(path,original)


def test_receipt(roots,receipt,text):
    misses=0
    checked=G.validate_published_source(roots,'phi',fixture_digits=len(text))
    assert checked.packed_bytes==5001 and checked.digits==10001
    actual=G._sha(checked.path)
    checked.check_completed_stream(actual,5001)
    misses+=refuse('whole-file SHA tamper',lambda:checked.check_completed_stream('0'*64,5001))
    misses+=refuse('incomplete byte count',lambda:checked.check_completed_stream(actual,5000))
    misses+=refuse('bool byte count',lambda:checked.check_completed_stream(actual,True))
    misses+=refuse('full hex not canonical',lambda:checked.check_completed_stream(actual.upper(),5001))
    misses+=refuse('wrong fixture logical N',lambda:G.validate_published_source(roots,'phi',fixture_digits=10000))
    misses+=refuse('boolean N',lambda:G.validate_published_source(roots,'phi',fixture_digits=True))
    misses+=refuse('unknown constant',lambda:G.validate_published_source(roots,'alien',fixture_digits=len(text)))
    original=roots.receipt('phi')
    def validate():
        return G.validate_published_source(roots,'phi',fixture_digits=len(text))
    mutations=[
        ('format', lambda x:x.update(format='BAD')),
        ('format version',lambda x:x.update(format_version=True)),
        ('converter scope',lambda x:x.update(scope='REAL')),
        ('constant ID',lambda x:x.update(constant='pi')),
        ('binary name',lambda x:x.update(binary_name='../x.bin')),
        ('declared digit length',lambda x:x.update(digits_including_integer=10000)),
        ('declared packed size',lambda x:x.update(packed_bytes=5000)),
        ('missing SHA',lambda x:x.pop('binary_sha256_streamed')),
        ('non-lowercase SHA',lambda x:x.update(binary_sha256_streamed='A'*64)),
        ('sample length',lambda x:x.update(sample_block_length=4095)),
        ('missing sample',lambda x:x['samples'].pop()),
        ('reversed sample order',lambda x:x['samples'].reverse()),
        ('sample offset',lambda x:x['samples'][0].update(offset_bytes=1)),
        ('sample offset as bool',lambda x:x['samples'][0].update(offset_bytes=True)),
        ('sample byte length',lambda x:x['samples'][0].update(size=1)),
        ('sample SHA',lambda x:x['samples'][0].update(sha256='0'*64)),
        ('sample SHA omitted',lambda x:x['samples'][0].pop('sha256')),
    ]
    for label,change in mutations:
        misses+=mutate_json(original,receipt,change,validate,label)
    content=checked.path.read_bytes()
    try:
        checked.path.write_bytes(content[:-1])
        misses+=refuse('physical truncation',validate)
    finally:
        checked.path.write_bytes(content)
    try:
        changed=bytearray(content); changed[0]^=1
        checked.path.write_bytes(changed)
        misses+=refuse('source sample corruption',validate)
    finally:
        checked.path.write_bytes(content)
    # Refuse path tricks without requiring admin ability to create links.
    try:
        alias=roots.digit_root/'alias'
        alias.symlink_to(checked.path)
    except (OSError,NotImplementedError):
        pass
    else:
        try:
            misses+=refuse('binary symlink',lambda:G._inside(roots.base,alias))
        finally:
            alias.unlink()
    assert len(G.sample_plan(5001))==12
    # This independently fixed oracle anchors deterministic converter positions.
    assert tuple(start for start,_ in G.sample_plan(5001)) == (
        0, 181, 202, 226, 452, 511, 554, 603, 678, 790, 813, 905
    ), 'converter sampling algorithm drift'
    assert G.sample_plan(9)==((0,9),)
    return misses



def test_unsampled_full_hash(roots):
    """Receipt sample verification alone must NOT authorise COMPLETE.

    Use a large-enough artificial file with genuinely UNSAMPLED physical bytes.
    Change one valid BCD digit outside every readback sample: the receipt and
    its sampled hashes still pass, but the full streamed SHA check MUST fail.
    """
    digits = b'1234567890' * 12_001
    packed = bytes.fromhex(digits.decode('ascii'))
    binary = roots.published_binary('e')
    binary.write_bytes(packed)
    plan = G.sample_plan(len(packed))
    uncovered = next((i for i in range(len(packed))
                      if all(not start <= i < start + length
                             for start, length in plan)), None)
    if uncovered is None:
        raise AssertionError('fixture did not contain an unsampled byte')
    receipt = {
        'format': G.FORMAT, 'format_version': 1, 'scope': G.SCOPE,
        'constant': 'e', 'binary_name': binary.name,
        'digits_including_integer': len(digits), 'packed_bytes': len(packed),
        'binary_sha256_streamed': hashlib.sha256(packed).hexdigest(),
        'sample_block_length': plan[0][1],
        'samples': [{'offset_bytes': start, 'size': length,
                     'sha256': hashlib.sha256(packed[start:start+length]).hexdigest()}
                    for start, length in plan],
    }
    write_json(roots.receipt('e'), receipt)
    checked = G.validate_published_source(roots, 'e', fixture_digits=len(digits))
    changed = bytearray(packed)
    changed[uncovered] ^= 1  # preserves both high/low decimal-nibble validity
    binary.write_bytes(changed)
    try:
        # A sampled-only validator cannot detect this; do not assert that it can.
        again = G.validate_published_source(roots, 'e', fixture_digits=len(digits))
        assert again.packed_sha256 == checked.packed_sha256
        actual = hashlib.sha256(changed).hexdigest()
        return refuse('unsampled tampering requires full streamed digest',
                      lambda: again.check_completed_stream(actual, len(changed)))
    finally:
        binary.write_bytes(packed)


def test_roots(roots):
    misses=0
    assert roots.output_parent('TEST_REAL')==roots.base/'results'
    assert roots.output_parent('TEST_NULL')==roots.base/'results_null'
    expect=roots.base/'results'/'TEST_REAL_one'
    assert roots.validate_run_location('TEST_REAL','TEST_REAL_one',expect)==expect
    misses+=refuse('NULL/REAL parent substitution',lambda:roots.validate_run_location(
        'TEST_REAL','TEST_REAL_one',roots.base/'results_null'/'TEST_REAL_one'))
    misses+=refuse('wrong run type',lambda:roots.output_parent('REAL'))
    misses+=refuse('type spoof',lambda:roots.output_parent('NULL'))
    misses+=refuse('cross-type name',lambda:roots.run_location('TEST_REAL','TEST_NULL_one'))
    misses+=refuse('path traversal',lambda:roots.run_location('TEST_REAL','TEST_REAL_../bad'))
    misses+=refuse('same-name wrong path',lambda:roots.validate_run_location(
        'TEST_REAL','TEST_REAL_one',roots.base/'results'/'TEST_REAL_other'))
    misses+=refuse('unknown production base',lambda:G.FixedRoots(roots.base,False))
    misses+=refuse('unmarked fixture',lambda:G.FixedRoots.test_sandbox(roots.base/'digits'))
    expect.mkdir()
    try:
        misses+=refuse('create-only collision',lambda:roots.validate_run_location(
            'TEST_REAL','TEST_REAL_one',expect))
    finally:
        expect.rmdir()
    return misses


def test_game(roots,game,first):
    misses=0
    header=G.PB_HEADER if game=='powerball' else G.SYNTHETIC_OZ_HEADER
    source=roots.base/'histories'/(game+'_synthetic.csv')
    original=history_rows(game,first)
    source.write_bytes(serialize_csv(header,original))
    profile=G.HistoryProfile(game,source,first,first+3,header,True)
    checked=G.validate_drawset(profile)
    assert checked.draw_count==3
    assert checked.draw_rows[0][0]==first
    assert checked.draw_rows[0][1][:7]==tuple(original[0][2:9])
    G.validate_drawset(profile,expected_sha256=checked.sha256)
    misses+=refuse('bad manifest digest',lambda:G.validate_drawset(profile,expected_sha256='0'*64))
    misses+=refuse('noncanonical manifest digest',lambda:G.validate_drawset(profile,expected_sha256='F'*64))
    variants=[
        ('wrong columns',tuple(reversed(header)),original),
        ('extra cutoff draw',header,original+[tuple([first+3,*original[-1][1:]])]),
        ('short era',header,original[:-1]),
        ('duplicate draw',header,[(first,*original[0][1:]),(first,*original[1][1:]),original[2]]),
        ('shuffled rows',header,[original[1],original[0],original[2]]),
        ('out-of-era future draw',header,[original[0],original[1],(first+3,*original[2][1:])]),
        ('date missing',header,[(first,'',*original[0][2:]),*original[1:]]),
        ('bad width',header,[original[0][:-1],*original[1:]]),
        ('main duplicated',header,[(first,*original[0][:3],original[0][2],*original[0][4:]),*original[1:]]),
        ('main out of range',header,[(first,*original[0][1:2],0,*original[0][3:]),*original[1:]]),
        ('leading-zero main',header,[(first,original[0][1],'01',*original[0][3:]),*original[1:]]),
    ]
    # Type of one variant is intentionally a string (leading zero) to test CSV parsing.
    for label,h,rows in variants:
        mutated=serialize_csv(h,rows)
        if mutated==source.read_bytes():
            raise AssertionError(f'{label} mutation no-op')
        source.write_bytes(mutated)
        misses+=refuse(label,lambda:G.validate_drawset(profile))
        source.write_bytes(serialize_csv(header,original))
    if game=='oz':
        mutated=list(original)
        row=list(mutated[0]);row[9]=row[2] # supplementary repeats main
        mutated[0]=tuple(row)
        source.write_bytes(serialize_csv(header,mutated))
        misses+=refuse('Oz supplement overlaps main',lambda:G.validate_drawset(profile))
    else:
        # PB legitimately equals a main, accepted in original fixture.
        assert checked.draw_rows[0][1][7] == checked.draw_rows[0][1][0]
        mutated=list(original)
        row=list(mutated[0]);row[9]=21 # invalid PB
        mutated[0]=tuple(row)
        source.write_bytes(serialize_csv(header,mutated))
        misses+=refuse('PB exceeds 20',lambda:G.validate_drawset(profile))
    source.write_bytes(serialize_csv(header,original))
    # Alter values but keep exact era: manifest hash still catches it on replay.
    tampered=list(original)
    row=list(tampered[0]); row[2],row[3]=row[3],row[2]
    tampered[0]=tuple(row)
    source.write_bytes(serialize_csv(header,tampered))
    misses+=refuse('same-era changed history',lambda:G.validate_drawset(
        profile,expected_sha256=checked.sha256))
    source.write_bytes(serialize_csv(header,original))
    return misses


def main():
    parser=argparse.ArgumentParser(description='Synthetic-only Q4 published format guard tests')
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--run',action='store_true')
    args=parser.parse_args()
    if args.self_test==args.run:
        parser.error('select exactly one of --self-test or --run')
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4_SOURCE_SANDBOX_') as parent:
        roots,record,text=prepare(Path(parent))
        # No code here reads a published source or existing REAL history.
        n=test_receipt(roots,record,text)
        n+=test_unsampled_full_hash(roots)
        n+=test_roots(roots)
        n+=test_game(roots,'powerball',11)
        n+=test_game(roots,'oz',21)
        n+=refuse('unconfirmed Oz REAL profile',lambda:G.installed_history_profile('oz'))
        n+=refuse('synthetic PB cannot become REAL profile',lambda:G.HistoryProfile(
            'powerball',roots.base/'histories'/'powerball_synthetic.csv',1144,1577,G.PB_HEADER))
        n+=refuse('synthetic Oz cannot become REAL profile',lambda:G.HistoryProfile(
            'oz',roots.base/'histories'/'oz_synthetic.csv',21,24,G.SYNTHETIC_OZ_HEADER))
        installed=G.installed_history_profile('powerball')
        assert installed.era_first_draw==1144 and installed.cutoff_exclusive==1577
        assert installed.source.name=='POWERBALL_preholdout_only.csv'
    print(f'Q4 PUBLISHED-SOURCE ADAPTER SYNTHETIC PASS: refusals={n} '
          'real-production-scans=0 real-history-reads=0')


if __name__=='__main__':
    main()
