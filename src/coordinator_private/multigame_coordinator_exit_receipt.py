"""Package 2 REVIEW CANDIDATE v2: coordinator-owned exit receipt and consumer firewall.

This module has NO subprocess, network, kill or timeout capabilities. The issuer
MUST be called only from the coordinator after its own Popen exit observation,
its full v0.6 post-exit orphan checks, group PASS decision and reviewed console
verification. This is NOT an authorisation to run any E-method under the POC.

Threat model: reject buggy/accidental worker self-certification, stale writes,
misbound artifacts and failing/orphan groups. It is not a signature, ACL or
protection against a malicious local actor sharing filesystem privileges.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
from collections.abc import Sequence
import re
from typing import Any

_SCHEMA = 'MULTIGAME_COORDINATOR_EXIT_RECEIPT_V2_REVIEW'
_RUN = re.compile(r'mg-[a-z0-9][a-z0-9_-]{7,95}\Z', re.ASCII)
_GAME = re.compile(r'[A-Z][A-Z0-9]*\Z', re.ASCII)
_METHOD = re.compile(r'E_[1-9][0-9]*\Z', re.ASCII)
_VARIANT = re.compile(r'[A-Z0-9_]{3,96}\Z', re.ASCII)
_SHA = re.compile(r'[a-f0-9]{64}\Z', re.ASCII)
_FILES = ('status.json', 'manifest.json', 'canonical_result.json')
_CONTRACT_MODULE_NAMES = ('multigame_result_registry.py', 'multigame_console_protocol.py')


def _contract_hashes() -> dict[str,str]:
    directory = Path(__file__).resolve().parents[1] / 'methods' / '_common'
    return {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in _CONTRACT_MODULE_NAMES}

_MAX_FILE = 2_000_000


def _hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical(obj: dict) -> bytes:
    return (json.dumps(obj, sort_keys=True, ensure_ascii=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('ascii')


def _read(path: Path, *, limit: int = _MAX_FILE) -> tuple[dict, bytes]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise ValueError('missing, unsafe or oversize record: ' + path.name)
    raw = path.read_bytes()
    try:
        obj = json.loads(raw)
        if type(obj) is not dict or raw != _canonical(obj):
            raise ValueError('noncanonical record: ' + path.name)
    except (UnicodeError, json.JSONDecodeError, OverflowError) as ex:
        raise ValueError('invalid JSON: ' + path.name) from ex
    return obj, raw


def _identity(identity: dict) -> None:
    if (type(identity) is not dict or
            set(identity) != {'group_id', 'worker_sequence', 'run_id', 'game_id',
                              'draw_number', 'method_id', 'variant_id'} or
            type(identity['group_id']) is not str or not re.fullmatch(r'[A-Za-z0-9_-]{1,85}', identity['group_id']) or
            type(identity['worker_sequence']) is not int or identity['worker_sequence'] < 1 or
            type(identity['run_id']) is not str or not _RUN.fullmatch(identity['run_id']) or
            type(identity['game_id']) is not str or not _GAME.fullmatch(identity['game_id']) or
            type(identity['draw_number']) is not int or identity['draw_number'] < 1 or
            type(identity['method_id']) is not str or not _METHOD.fullmatch(identity['method_id']) or
            type(identity['variant_id']) is not str or not _VARIANT.fullmatch(identity['variant_id'])):
        raise ValueError('invalid coordinator receipt identity')


def _check_artifact_identities(identity: dict, status: dict, manifest: dict, result: dict) -> str:
    required = {k: v for k, v in identity.items() if k not in ('group_id', 'worker_sequence')}
    for name, item in (('status', status), ('manifest', manifest), ('result', result)):
        if any(item.get(key) != value for key, value in required.items()):
            raise ValueError(name + ' identity mismatch')
    from _common.multigame_result_registry import (
        SYNTHETIC_MODE, SYNTHETIC_SCHEMA, SCIENTIFIC_MODES,
        require_synthetic_variant, require_scientific_contract,
    )
    mode = status.get('mode')
    if (status.get('state') != 'SUCCESS' or
            manifest.get('state') != 'PASS' or
            manifest.get('orphan_suspected') is not False or
            manifest.get('marker_write_failed') is not False or
            mode not in SCIENTIFIC_MODES | {SYNTHETIC_MODE} or
            mode != manifest.get('mode') or mode != result.get('mode')):
        raise ValueError('worker outcome is not a valid coordinated success')
    if (type(status.get('pid')) is not int or status['pid'] <= 0 or
            type(status.get('process_create_time_epoch')) not in (int, float) or
            not math.isfinite(status['process_create_time_epoch']) or
            status['process_create_time_epoch'] <= 0):
        raise ValueError('status lacks valid process identity')
    if mode == SYNTHETIC_MODE:
        require_synthetic_variant(identity['game_id'], identity['method_id'], identity['variant_id'])
        if (result.get('schema') != SYNTHETIC_SCHEMA or
                result.get('data_kind') != SYNTHETIC_MODE or
                manifest.get('synthetic_only') is not True):
            raise ValueError('invalid synthetic-only receipt artifact classification')
    else:
        if (manifest.get('synthetic_only') is not False or
                result.get('not_a_forecast') is True or
                result.get('synthetic_only') is True):
            raise ValueError('non-scientific record cannot claim scientific mode')
        require_scientific_contract(game_id=identity['game_id'],
                                    method_id=identity['method_id'],
                                    variant_id=identity['variant_id'],
                                    mode=mode, result=result)
    return mode


def issue_coordinator_receipt(*, group_dir: Path, run_dir: Path, identity: dict,
                              coordinator_sha256: str, root_pid: int,
                              root_create_time_epoch: float,
                              wrapper_exit_code: int, exit_observed_utc: str,
                              console_publication_records: Sequence[str]) -> Path:
    """Issue ONLY after verified coordinator observations; NEVER pass to a method.

    The coordinator verifies Popen exit, root identity, ancestry, no-orphan
    and full-group PASS before calling. This function independently validates
    the console protocol against the one canonical-result read it hashes.
    """
    _identity(identity)
    if (group_dir.name != identity['group_id'] or
            run_dir.name != identity['run_id'] or
            run_dir == group_dir or group_dir in run_dir.parents or
            (group_dir / 'receipts').is_symlink()):
        raise ValueError('unsafe coordinator receipt folder')
    if (type(coordinator_sha256) is not str or not _SHA.fullmatch(coordinator_sha256) or
            type(root_pid) is not int or root_pid <= 0 or
            type(root_create_time_epoch) not in (int, float) or
            not math.isfinite(root_create_time_epoch) or root_create_time_epoch <= 0 or
            type(wrapper_exit_code) is not int or wrapper_exit_code != 0):
        raise ValueError('coordinator exit or console evidence not clean')
    try:
        when = datetime.fromisoformat(exit_observed_utc)
        if when.tzinfo is None or when.utcoffset().total_seconds() != 0:
            raise ValueError('time not UTC')
    except (ValueError, TypeError, AttributeError) as ex:
        raise ValueError('invalid coordinator-observed exit UTC') from ex
    files = {name: _read(run_dir / name) for name in _FILES}
    trusted_mode = _check_artifact_identities(identity, *(files[k][0] for k in _FILES))
    # C1: verify the complete console protocol AGAINST THE EXACT result bytes
    # in this one read. The same in-memory bytes are then SHA-256-bound below.
    # No second read of canonical_result.json and no unproven boolean from
    # the caller can certify the digest. The old v0.5 two-read seam is retired.
    from _common.multigame_console_protocol import verify_success_records
    verify_success_records(console_publication_records,
        game_id=identity['game_id'], method_id=identity['method_id'],
        run_id=identity['run_id'], target=identity['draw_number'],
        canonical_result=files['canonical_result.json'][1])
    status = files['status.json'][0]
    record = {'schema': _SCHEMA, **identity, 'mode': trusted_mode,
              'coordinator_sha256': coordinator_sha256,
              'root_pid': root_pid, 'root_create_time_epoch': root_create_time_epoch,
              'wrapper_exit_code': wrapper_exit_code,
              'coordinator_exit_observed_utc': exit_observed_utc,
              'console_result_digest_match': True,  # derived from exact read

              'status_pid': status['pid'],
              'status_create_time_epoch': status['process_create_time_epoch'],
              'artifact_sha256': {name: _hash(files[name][1]) for name in _FILES},
              'contract_modules_sha256': _contract_hashes()}
    directory = group_dir / 'receipts'
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('coordinator-owned receipts directory missing')
    destination = directory / (identity['run_id'] + '.json')
    # Create-only. A collision is an error and never overwrites a possible spoof.
    with destination.open('xb') as fh:
        fh.write(_canonical(record))
        fh.flush()
        os.fsync(fh.fileno())
    return destination


def verify_receipt_before_consume(*, group_dir: Path, run_dir: Path,
                                  identity: dict, coordinator_sha256: str,
                                  global_orphan_marker: Path) -> dict:
    """Only admit coordinated/FINAL result after complete receipt/group firewall.

    Result bytes are opened LAST. A caller must not access outcomes or model
    data before this function succeeds. Synthetic review interface only.
    """
    _identity(identity)
    if os.path.lexists(global_orphan_marker):
        raise ValueError('global unresolved-orphan safety stop')
    if (group_dir.name != identity['group_id'] or run_dir.name != identity['run_id'] or
            (group_dir / 'receipts').is_symlink() or
            type(coordinator_sha256) is not str or not _SHA.fullmatch(coordinator_sha256)):
        raise ValueError('group/run/coordinator identity mismatch')
    aggregate, _ = _read(group_dir / 'manifest.json')
    if (aggregate.get('group_id') != identity['group_id'] or
            aggregate.get('success') is not True or aggregate.get('status') != 'PASS' or
            aggregate.get('orphan_suspected') is not False or
            aggregate.get('marker_write_failed') is not False):
        raise ValueError('group is not eligible for consumption')
    members = aggregate.get('workers')
    if (type(members) is not list or
            len([w for w in members if type(w) is dict and
                 w.get('run_id') == identity['run_id'] and
                 w.get('sequence') == identity['worker_sequence'] and
                 w.get('state') == 'SUCCESS']) != 1):
        raise ValueError('worker missing from PASS group')
    receipt, _ = _read(group_dir / 'receipts' / (identity['run_id'] + '.json'))
    if (receipt.get('schema') != _SCHEMA or
            any(receipt.get(k) != v for k, v in identity.items()) or
            receipt.get('coordinator_sha256') != coordinator_sha256 or
            receipt.get('wrapper_exit_code') != 0 or
            receipt.get('console_result_digest_match') is not True or
            type(receipt.get('root_pid')) is not int or receipt['root_pid'] <= 0 or
            type(receipt.get('root_create_time_epoch')) not in (float, int) or
            not math.isfinite(receipt['root_create_time_epoch']) or
            receipt['root_create_time_epoch'] <= 0):
        raise ValueError('missing or mismatched trusted coordinator receipt')
    try:
        exit_time = datetime.fromisoformat(receipt['coordinator_exit_observed_utc'])
        if exit_time.tzinfo is None or exit_time.utcoffset().total_seconds() != 0:
            raise ValueError('receipt exit time not UTC')
    except (KeyError, ValueError, TypeError, AttributeError) as ex:
        raise ValueError('invalid coordinator exit timestamp') from ex
    if (type(receipt.get('status_pid')) is not int or receipt['status_pid'] <= 0 or
            type(receipt.get('status_create_time_epoch')) not in (int,float) or
            not math.isfinite(receipt['status_create_time_epoch']) or
            receipt['status_create_time_epoch'] <= 0):
        raise ValueError('invalid worker status identity in receipt')
    from _common.multigame_result_registry import SYNTHETIC_MODE, SCIENTIFIC_MODES
    receipt_mode = receipt.get('mode')
    if receipt_mode == SYNTHETIC_MODE:
        # No result-file read is ever allowed for a synthetic plumbing probe
        # through a coordinated/FINAL scientific consumer, even with a
        # valid-looking coordinator receipt and PASS group.
        raise ValueError('synthetic contract test is not a scientific result')
    if receipt_mode not in SCIENTIFIC_MODES:
        raise ValueError('unregistered coordinated/FINAL receipt mode')
    from _common.multigame_result_registry import registered_scientific_binding
    # Classify by a reviewed registry BEFORE even opening the result file.
    # Package 2 has no live scientific coordinated/FINAL registrations.
    registered_scientific_binding(game_id=identity['game_id'],
        method_id=identity['method_id'], variant_id=identity['variant_id'],
        mode=receipt_mode)
    if receipt.get('contract_modules_sha256') != _contract_hashes():
        raise ValueError('receipt contract module hash mismatch')
    digests = receipt.get('artifact_sha256')
    if (type(digests) is not dict or set(digests) != set(_FILES) or
            any(type(value) is not str or not _SHA.fullmatch(value)
                for value in digests.values())):
        raise ValueError('invalid bound artifact digests')
    # Status and worker manifest FIRST, both verified before opening a result.
    status, status_raw = _read(run_dir / 'status.json')
    manifest, manifest_raw = _read(run_dir / 'manifest.json')
    if (status.get('mode') != receipt_mode or
            manifest.get('mode') != receipt_mode or
            _hash(status_raw) != digests['status.json'] or
            _hash(manifest_raw) != digests['manifest.json'] or
            status.get('pid') != receipt.get('status_pid') or
            status.get('process_create_time_epoch') != receipt.get('status_create_time_epoch')):
        raise ValueError('frozen status/manifest tampered')
    # Result can only be read once all gates above are satisfied.
    result, raw = _read(run_dir / 'canonical_result.json')
    if _hash(raw) != digests['canonical_result.json']:
        raise ValueError('frozen result bytes changed')
    _check_artifact_identities(identity, status, manifest, result)
    # This checks an explicit (game, method, registered variant, mode,
    # result schema, data_kind) allowlist, NOT just absence of denial flags.
    # A legacy standalone forecast is not automatically a coordinated one.
    if (result.get('not_a_forecast') is True or
            result.get('synthetic_only') is True or
            manifest.get('synthetic_only') is True):
        raise ValueError('non-scientific plumbing record is not consumable')
    if (manifest.get('canonical_result_sha256') != digests['canonical_result.json'] or
            status.get('canonical_result_sha256') != digests['canonical_result.json']):
        raise ValueError('worker reported wrong canonical result hash')
    return result
