"""Package 2 review: method-side self-report for synthetic coordinated contracts.

The worker CANNOT attest wrapper exit, ancestry or group PASS. The manifest
is self-reported and is not consumable without the coordinator's separate,
create-only exit receipt and frozen PASS group manifest. No subprocess/network.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from _common.multigame_console_protocol_v1 import prepare_success_records
from _common.multigame_standalone_contract_v1 import json_bytes
from _common.multigame_result_registry_v1 import (
    require_synthetic_variant, SYNTHETIC_MODE, SYNTHETIC_SCHEMA
)


def _new(path: Path, raw: bytes) -> None:
    if path.is_symlink():
        raise ValueError('symlink output forbidden')
    with path.open('xb') as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())


def publish_coordinated_success(*, run_dir: Path, identity: dict,
                                status: dict, result: dict) -> tuple[str, ...]:
    """Freeze worker output in create-only files; return console records to print.

    Caller must have published STARTED status durably before heavy processing;
    `status` here is the terminal status intended for a separate mutable
    status file already created at STARTED. No group success implied.
    """
    # Method code cannot import the coordinator-only receipt issuer, even
    # for validation. This is merely a local schema check; ownership is
    # independently revalidated inside the coordinator.
    import re
    if (type(identity) is not dict or set(identity) !=
            {'group_id', 'worker_sequence', 'run_id', 'game_id',
             'draw_number', 'method_id', 'variant_id'} or
            not re.fullmatch(r'[A-Za-z0-9_-]{1,85}', str(identity['group_id']), re.ASCII) or
            type(identity['worker_sequence']) is not int or identity['worker_sequence'] < 1 or
            not re.fullmatch(r'mg-[a-z0-9][a-z0-9_-]{7,95}', str(identity['run_id']), re.ASCII) or
            not re.fullmatch(r'[A-Z][A-Z0-9]*', str(identity['game_id']), re.ASCII) or
            type(identity['draw_number']) is not int or identity['draw_number'] < 1 or
            not re.fullmatch(r'E_[1-9][0-9]*', str(identity['method_id']), re.ASCII) or
            not re.fullmatch(r'[A-Z0-9_]{3,96}', str(identity['variant_id']), re.ASCII)):
        raise ValueError('invalid worker identity')
    if (run_dir.name != identity['run_id'] or not run_dir.is_dir() or
            run_dir.is_symlink() or (run_dir / 'status.json').is_symlink()):
        raise ValueError('unsafe or missing run folder')
    keys = {k: v for k, v in identity.items() if k not in ('group_id', 'worker_sequence')}
    if any(status.get(k) != v or result.get(k) != v for k, v in keys.items()):
        raise ValueError('worker status/result identity mismatch')
    require_synthetic_variant(identity['game_id'], identity['method_id'], identity['variant_id'])
    if (status.get('mode') != SYNTHETIC_MODE or status.get('state') != 'SUCCESS' or
            result.get('mode') != SYNTHETIC_MODE or
            result.get('schema') != SYNTHETIC_SCHEMA or
            result.get('data_kind') != SYNTHETIC_MODE or
            type(status.get('pid')) is not int or status['pid'] <= 0 or
            type(status.get('process_create_time_epoch')) not in (int, float) or
            status['process_create_time_epoch'] <= 0):
        raise ValueError('not a valid synthetic worker terminal state')
    if (not (run_dir / 'status.json').is_file() or
            (run_dir / 'canonical_result.json').exists() or
            (run_dir / 'manifest.json').exists()):
        raise ValueError('worker output missing or pre-existing')
    # The terminal status is published by the worker using the existing
    # durable status updater. Match those exact bytes before creating outputs.
    status_bytes = (run_dir / 'status.json').read_bytes()
    if status_bytes != json_bytes(status):
        raise ValueError('terminal status file is not the supplied status')
    raw = json_bytes(result)
    hash_value = hashlib.sha256(raw).hexdigest()
    if status.get('canonical_result_sha256') != hash_value:
        raise ValueError('worker status digest disagreement')
    markers = prepare_success_records(game_id=identity['game_id'],
                method_id=identity['method_id'], run_id=identity['run_id'],
                target=identity['draw_number'], result=result)
    manifest = {**keys, 'schema':'MULTIGAME_COORDINATED_WORKER_MANIFEST_V1_REVIEW',
                'mode':SYNTHETIC_MODE, 'state':'PASS', 'synthetic_only': True,
                'orphan_suspected':False, 'marker_write_failed':False,
                'canonical_result_sha256':hash_value,
                'worker_exit_certified':False,
                'coordinator_receipt_required':True}
    # No error path may promote a failure to PASS. Partial publication is
    # treated as FAILED and retained for inspection, never overwritten.
    _new(run_dir / 'canonical_result.json', raw)
    _new(run_dir / 'manifest.json', json_bytes(manifest))
    return markers
