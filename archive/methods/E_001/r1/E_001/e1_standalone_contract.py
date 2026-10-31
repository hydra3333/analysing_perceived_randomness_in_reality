"""Review-candidate standalone E_1 status/manifest integrity contract.

Never infers coordinator PASS from an experiment's result file. No process
termination, PID targeting, network, or background work. Verified consumer
checks manifest and terminal status BEFORE opening canonical_result.json.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from _common.experiment_runtime_status_and_resources import ProbeStatus

RUN_ID_RE = re.compile(r'e1-[a-z0-9][a-z0-9_-]{7,95}\Z', re.ASCII)
HEX_RE = re.compile(r'[0-9a-f]{64}\Z', re.ASCII)


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
            separators=(',', ':'), allow_nan=False) + '\n').encode('ascii')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def create_only(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def begin(run_dir: Path, run_id: str, mode: str, target: int) -> ProbeStatus:
    """One shared runtime schema for standalone and coordinated methods.

    The shared helper writes STARTED with real PID, creation time, sys.prefix
    and monotonic start origin. No CSV/model imports occur before this step.
    """
    if not RUN_ID_RE.fullmatch(run_id):
        raise ValueError('run_id must be a safe e1- prefixed identifier')
    if mode not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT'):
        raise ValueError('mode not supported')
    if type(target) is not int or not 1145 <= target <= 1577:
        raise ValueError('invalid target')
    run_dir.mkdir(parents=True, exist_ok=False)
    status = ProbeStatus(run_dir / 'status.json', run_id,
                         'E_001_Historical_Appearance_Frequency',
                         identity={'mode': mode, 'target_draw': target,
                                   'method_id': 'E_1',
                                   'variant_id': 'FULL_HISTORY_RAW_COUNTS_V1'})
    # psutil is an installed project dependency; never claim identity if absent.
    if status.value.get('process_create_time_epoch') is None:
        raise RuntimeError('process creation time unavailable; no valid STARTED identity')
    return status


def finish(run_dir: Path, status: ProbeStatus, state: str, *,
           error: str | None = None, training_digest: str | None = None,
           result_digest: str | None = None,
           failure_reason: str | None = None) -> dict:
    if state not in ('SUCCESS', 'FAILED'):
        raise ValueError('terminal state not recognised')
    if status.value['state'] != 'STARTED':
        raise ValueError('status can only finish once')
    additions = {}
    if training_digest is not None:
        additions['training_view_sha256'] = training_digest
    if result_digest is not None:
        additions['canonical_result_sha256'] = result_digest
    if failure_reason is not None:
        additions['failure_reason'] = failure_reason
    status.finish(state, error=error[:320] if error else None,
                  terminal_fields=additions)
    return dict(status.value)


def publish_success_manifest(run_dir: Path, status: dict, result_digest: str,
                             training_digest: str) -> None:
    # Called as LAST substantive instruction before Python return.
    if status.get('state') != 'SUCCESS':
        raise ValueError('cannot report success without completed status')
    if status.get('canonical_result_sha256') != result_digest or status.get('training_view_sha256') != training_digest:
        raise ValueError('status digest mismatch')
    manifest = {'schema': 'E1_STANDALONE_MANIFEST_V0_1_REVIEW',
                'run_id': status['run_id'], 'mode': status['mode'],
                'method_id': status['method_id'], 'variant_id': status['variant_id'],
                'target_draw': status['target_draw'], 'state': 'PASS',
                'orphan_suspected': False, 'marker_write_failed': False,
                'status_sha256': sha(canonical_json(status)),
                'canonical_result_sha256': result_digest,
                'training_view_sha256': training_digest,
                'self_reported_completion': True,
                'external_exit_code_verified': False}
    create_only(run_dir / 'standalone_manifest.json', canonical_json(manifest))


def publish_failed_manifest(run_dir: Path, status: dict) -> None:
    # It is legal to have a FAILED manifest and even a late canonical_result;
    # consumers still refuse to inspect that result.
    manifest = {'schema': 'E1_STANDALONE_MANIFEST_V0_1_REVIEW',
                'run_id': status['run_id'], 'mode': status['mode'],
                'target_draw': status['target_draw'], 'state': 'FAIL',
                'status_sha256': sha(canonical_json(status)),
                'orphan_suspected': False, 'marker_write_failed': False}
    create_only(run_dir / 'standalone_manifest.json', canonical_json(manifest))


def _strict_json_bytes(path: Path) -> tuple[dict, bytes]:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'{path.name}: expected regular nonsymlink JSON file')
    raw = path.read_bytes()
    obj = json.loads(raw)
    if not isinstance(obj, dict) or raw != canonical_json(obj):
        raise ValueError(f'{path.name} not canonical JSON object')
    return obj, raw


def verify_and_consume(run_dir: Path, *, run_id: str, target: int, mode: str,
                       unresolved_orphan_marker: Path | None = None) -> dict:
    """Fail closed before consuming any result. No coordinator-manifest fallback.

    This validates the *worker's own* claimed success, NOT external Windows
    exit-code proof. Such external proof remains an independently reviewed gate.
    """
    # Real-data consumers ALWAYS check the canonical project marker; a caller
    # cannot pass None or a decoy path to bypass the protective check.
    if mode == 'REAL_HISTORICAL_DEVELOPMENT':
        canonical_marker = Path(__file__).resolve().parents[3] / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        if canonical_marker.exists() or canonical_marker.is_symlink():
            raise ValueError('unresolved coordinator orphan marker: refuse real consumption')
    if unresolved_orphan_marker is not None and (unresolved_orphan_marker.exists() or unresolved_orphan_marker.is_symlink()):
        raise ValueError('unresolved coordinator orphan marker: refuse consumption')
    if run_dir.is_symlink():
        raise ValueError('symlink run directory forbidden')
    manifest, _ = _strict_json_bytes(run_dir / 'standalone_manifest.json')
    if manifest.get('schema') != 'E1_STANDALONE_MANIFEST_V0_1_REVIEW':
        raise ValueError('unknown manifest schema')
    if manifest.get('state') != 'PASS':
        raise ValueError('non-PASS run is forbidden')
    if manifest.get('orphan_suspected') is not False or manifest.get('marker_write_failed') is not False:
        raise ValueError('orphan/marker uncertainty: forbidden')
    if manifest.get('self_reported_completion') is not True or manifest.get('external_exit_code_verified') is not False:
        raise ValueError('unsupported standalone exit proof declaration')
    if (manifest.get('run_id'), manifest.get('target_draw'), manifest.get('mode'),
        manifest.get('method_id'), manifest.get('variant_id')) != (run_id, target, mode, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1'):
        raise ValueError('run identity mismatch')
    status, raw_status = _strict_json_bytes(run_dir / 'status.json')
    if sha(raw_status) != manifest.get('status_sha256') or status.get('schema') != 'ENGINEERING_POC_STATUS_V1':
        raise ValueError('status hash or schema mismatch')
    if status.get('state') != 'SUCCESS':
        raise ValueError('terminal status not SUCCESS')
    # Require full shared runtime contract, not an E1-only lookalike.
    if (type(status.get('pid')) is not int or status['pid'] <= 0 or
        not isinstance(status.get('process_create_time_epoch'), (int, float)) or
        status['process_create_time_epoch'] <= 0 or
        not isinstance(status.get('sys_prefix'), str) or not status['sys_prefix'] or
        not isinstance(status.get('case'), str) or
        status['case'] != 'E_001_Historical_Appearance_Frequency'):
        raise ValueError('runtime identity invalid')
    for key in ('elapsed_seconds', 'cpu_time_seconds'):
        if not isinstance(status.get(key), (int, float)) or status[key] < 0:
            raise ValueError(f'{key} missing or invalid')
    if status.get('peak_field') not in ('peak_wset', 'peak_rss', 'UNAVAILABLE'):
        raise ValueError('memory metric label missing or unexpected')
    peak = status.get('peak_working_set_bytes')
    if not (peak is None and status['peak_field'] == 'UNAVAILABLE' or
            type(peak) is int and peak >= 0 and status['peak_field'] != 'UNAVAILABLE'):
        raise ValueError('memory peak invalid')
    for name in ('run_id', 'target_draw', 'mode', 'method_id', 'variant_id'):
        if status.get(name) != manifest.get(name):
            raise ValueError(f'{name} inconsistent')
    for name in ('canonical_result_sha256', 'training_view_sha256'):
        if not isinstance(manifest.get(name), str) or HEX_RE.fullmatch(manifest[name]) is None:
            raise ValueError(f'{name} malformed')
        if status.get(name) != manifest.get(name):
            raise ValueError(f'{name} status disagreement')
    # Only now may a consumer open and examine the canonical result.
    result, raw = _strict_json_bytes(run_dir / 'canonical_result.json')
    if sha(raw) != manifest['canonical_result_sha256']:
        raise ValueError('canonical result hash mismatch')
    if (result.get('method_id'), result.get('variant_id'), result.get('target_draw'),
        result.get('data_kind'), result.get('training_view_sha256')) != (
            'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', target, mode,
            manifest['training_view_sha256']):
        raise ValueError('canonical result identity mismatch')
    if result.get('schema') != 'E1_HISTORICAL_DEVELOPMENT_FORECAST_V0_1_REVIEW':
        raise ValueError('unsupported result schema')
    if result.get('ranking_tie_readout_version') != 'TIE_SHA256_V1':
        raise ValueError('unrecognised readout identity')
    return result
