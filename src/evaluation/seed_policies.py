"""N1's seed policy records (releases and WF-1 design v0.1r1 sections 7.6 and 8; decisions WF1-9, WF1-12; D-9..D-11).

Records live in src/evaluation/seed_policies/, are reviewed and immutable, and are all kept (provisional, refused,
replaced and approved), so that every root tried is counted (D-10; design 8.4). The report tool uses N1 only with
exactly one APPROVED record; there is no default, test or fallback root in production code (7.6).

Binding (EX_109 WF1B-R2-B01): every record must name a policy in ANNOUNCED below, the review-pinned list of the
pulses announced in exchange/ before they existed. An APPROVED record must describe exactly that announced pulse
(chain, exact UTC time stamp, version), with a well-typed pulse index, NIST's canonical URI for it, and the two
HTTPS reads of design 8.2 at their exact official addresses (the time lookup the owner opened and the permanent
pulse address Claude read). Anything else fails closed: the record is refused and N1 does not run.
No live fetch and no signature check is made (WF1-12).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

FOLDER = Path(__file__).resolve().parent / 'seed_policies'
SCHEMA = 'SEED_POLICY_V1'
STATUSES = ('PROVISIONAL', 'APPROVED', 'REFUSED', 'REPLACED_BEFORE_PULSE')
BEACON = 'https://beacon.nist.gov/beacon/2.0'

# The pulses announced before they existed (review-pinned; a new announcement is a reviewed change to this table).
ANNOUNCED = {
    'N1_ROOT_NIST_C2_20261106T0000Z_V1': {'time_stamp': '2026-11-06T00:00:00.000Z', 'epoch_ms': 1793923200000,
                                          'chain_index': 2, 'version': '2.0',
                                          'announced_in': 'design v0.1r1 section 8.1 (EX_077, EX_079)'},
    'N1_ROOT_NIST_C2_20261031T1030Z_V1': {'time_stamp': '2026-10-31T10:30:00.000Z', 'epoch_ms': 1793442600000,
                                          'chain_index': 2, 'version': '2.0',
                                          'announced_in': 'EX_103 (commit 92a6cef)'},
}

_HEX128_UPPER = re.compile(r'[0-9A-F]{128}\Z', re.ASCII)
_HEX128_LOWER = re.compile(r'[0-9a-f]{128}\Z', re.ASCII)
_SHA256 = re.compile(r'[0-9a-f]{64}\Z', re.ASCII)
_APPROVED_FIELDS = ('output_value', 'uri', 'pulse_index', 'time_stamp', 'status_code', 'certificate_id', 'chain_index',
                    'version', 'sources', 'owner_file_sha256', 'fetched_by', 'fetched_utc', 'verified_by',
                    'verified_utc', 'signature_verification', 'trust_basis', 'nist_notice', 'approved_by',
                    'approved_utc')


def _int(v) -> bool:
    return type(v) is int


def _text(v) -> bool:
    return type(v) is str and bool(v) and v.isascii()


def validate(rec) -> dict:
    """Fail closed unless the record is a SEED_POLICY_V1 of an announced policy and, if APPROVED, describes exactly
    the announced pulse and its two official reads."""
    if type(rec) is not dict or rec.get('schema') != SCHEMA or rec.get('status') not in STATUSES:
        raise ValueError('not a SEED_POLICY_V1 record with a known status')
    pid = rec.get('policy_id')
    if pid not in ANNOUNCED:
        raise ValueError(f'policy {pid!r} was not announced before its pulse (not in the pinned ANNOUNCED table)')
    ann = ANNOUNCED[pid]
    if rec['status'] != 'APPROVED':
        if 'output_value' in rec:
            raise ValueError(f'{pid}: a {rec["status"]} record carries no root')
        return rec
    missing = [k for k in _APPROVED_FIELDS if k not in rec]
    if missing:
        raise ValueError(f'{pid}: APPROVED record lacks {missing}')
    if rec['time_stamp'] != ann['time_stamp']:
        raise ValueError(f'{pid}: time stamp {rec["time_stamp"]!r} is not the announced {ann["time_stamp"]}')
    if not _int(rec['chain_index']) or rec['chain_index'] != ann['chain_index']:
        raise ValueError(f'{pid}: chain must be {ann["chain_index"]}')
    if rec['version'] != ann['version']:
        raise ValueError(f'{pid}: version must be {ann["version"]}')
    if not _int(rec['pulse_index']) or rec['pulse_index'] < 1:
        raise ValueError(f'{pid}: pulse_index must be a positive integer')
    canonical_uri = f"{BEACON}/chain/{ann['chain_index']}/pulse/{rec['pulse_index']}"
    if rec['uri'] != canonical_uri:
        raise ValueError(f'{pid}: uri must be {canonical_uri}')
    if not _int(rec['status_code']) or rec['status_code'] != 0:
        raise ValueError(f'{pid}: statusCode must be 0')
    if type(rec['output_value']) is not str or not _HEX128_UPPER.fullmatch(rec['output_value']):
        raise ValueError(f'{pid}: outputValue must be 128 upper-case hexadecimal characters, as published')
    if type(rec['certificate_id']) is not str or not _HEX128_LOWER.fullmatch(rec['certificate_id']):
        raise ValueError(f'{pid}: certificateId must be 128 lower-case hexadecimal characters, as published')
    expected_sources = [f"{BEACON}/pulse/time/{ann['epoch_ms']}", canonical_uri]
    srcs = rec['sources']
    if (type(srcs) is not list or len(srcs) != 2 or any(type(s) is not dict for s in srcs) or
            [s.get('url') for s in srcs] != expected_sources or not all(_text(s.get('read_by')) for s in srcs) or
            srcs[0]['read_by'] == srcs[1]['read_by']):
        raise ValueError(f'{pid}: sources must be the two official reads, by two different people: '
                         f'{expected_sources}')
    if type(rec['owner_file_sha256']) is not str or not _SHA256.fullmatch(rec['owner_file_sha256']):
        raise ValueError(f'{pid}: owner_file_sha256 must be a SHA-256')
    if rec['signature_verification'] != 'NOT_PERFORMED':
        raise ValueError(f'{pid}: signature_verification must be NOT_PERFORMED (WF1-12)')
    for k in ('fetched_by', 'fetched_utc', 'verified_by', 'verified_utc', 'trust_basis', 'nist_notice', 'approved_by',
              'approved_utc'):
        if not _text(rec[k]):
            raise ValueError(f'{pid}: {k} must be non-empty ASCII text')
    if rec['fetched_by'] == rec['verified_by']:
        raise ValueError(f'{pid}: the pulse must be verified by someone other than the person who fetched it (D-9)')
    return rec


def _records() -> list[dict]:
    out = []
    if not FOLDER.is_dir():
        return out
    for p in sorted(FOLDER.glob('*.json')):
        rec = json.loads(p.read_bytes().decode('ascii'))
        validate(rec)
        if p.stem != rec['policy_id']:
            raise ValueError(f'{p.name}: the file name must be the policy ID')
        out.append(rec)
    ids = [r['policy_id'] for r in out]
    if len(ids) != len(set(ids)):
        raise ValueError('two records for one policy')
    return out


def count_policies() -> int:
    return len(_records())


def approved_policy() -> dict | None:
    """The one APPROVED policy, or None. More than one APPROVED record is refused (a replacement must be explicit)."""
    approved = [r for r in _records() if r['status'] == 'APPROVED']
    if len(approved) > 1:
        raise ValueError('more than one APPROVED N1 seed policy')
    return approved[0] if approved else None
