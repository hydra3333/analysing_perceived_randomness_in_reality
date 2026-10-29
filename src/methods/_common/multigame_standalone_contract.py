"""Synthetic-only method-generic status/result/consumer prototype, Package 2.

NO coordinated runs and NO FINAL. In coordinated/FINAL mode, a trusted
coordinator-written exit_receipt.json, and its reviewed console/run-ID
handshake, must be implemented before this contract may be used.
No termination, no subprocesses, and no access to real game data.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from _common.experiment_runtime_status_and_resources import ProbeStatus
from _common.game_profiles import GameProfile
from _common.multigame_method_registry import method_status, SUPPORTED

_RUN = re.compile(r'mg-[a-z0-9][a-z0-9_-]{7,95}\Z',re.ASCII)
_HEX = re.compile(r'[0-9a-f]{64}\Z',re.ASCII)
_MODE = 'SYNTHETIC_CONTRACT_TEST'


def json_bytes(value: object) -> bytes:
    return (json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_new(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())


def begin_synthetic(run_root: Path, *, run_id: str, profile: GameProfile,
                    target: int, method_id: str, variant_id: str) -> tuple[Path, ProbeStatus]:
    if not _RUN.fullmatch(run_id):
        raise ValueError('invalid game-qualified run ID')
    if not profile.historical_development_target_allowed(target):
        raise ValueError('outside historical development boundary')
    if method_status(profile.game_id,method_id) != SUPPORTED:
        raise ValueError('method unsupported or FORMULA_OPEN')
    if not variant_id or not re.fullmatch(r'[A-Z0-9_]{3,96}',variant_id,re.ASCII):
        raise ValueError('invalid variant identifier')
    # E2R-CODE-2 (reviewer's E2RC2-C03): the per-method roll-up above never approves another variant.
    from _common.contract_dispatch import variant_released
    if not variant_released(profile.game_id, method_id, variant_id):
        raise ValueError('this method variant is not released (no active SUPPORTED entry, or flagged)')
    directory = run_root / profile.game_id / run_id
    directory.mkdir(parents=True,exist_ok=False)
    status=ProbeStatus(directory/'status.json',run_id,method_id,identity={
        'game_id':profile.game_id,'profile_version':profile.version,
        'draw_number':target,'draw_key':profile.draw_key(target),
        'method_id':method_id,'variant_id':variant_id,'mode':_MODE,
    })
    if status.value.get('process_create_time_epoch') is None:
        raise RuntimeError('cannot prove process creation time')
    return directory,status


def publish_synthetic_success(run_dir: Path,status: ProbeStatus, result: dict) -> dict:
    # NO real source, no FINAL and no external coordinator exit proof.
    before=dict(status.value)
    if (before.get('mode') != _MODE or result.get('data_kind') != _MODE or
            before.get('game_id') != result.get('game_id') or
            before.get('profile_version') != result.get('profile_version') or
            before.get('draw_number') != result.get('draw_number') or
            before.get('method_id') != result.get('method_id') or
            before.get('variant_id') != result.get('variant_id') or
            before.get('state') != 'STARTED'):
        raise ValueError('result identity mismatch')
    raw=json_bytes(result)
    result_hash=digest(raw)
    write_new(run_dir/'canonical_result.json',raw)
    status.finish('SUCCESS',terminal_fields={
        'canonical_result_sha256':result_hash,
        'training_view_sha256':result['training_view_sha256'],
    })
    final=dict(status.value)
    status_raw=json_bytes(final)
    manifest={
        'schema':'MULTIGAME_STANDALONE_MANIFEST_V1_REVIEW',
        'game_id':final['game_id'],'profile_version':final['profile_version'],
        'method_id':final['method_id'],'variant_id':final['variant_id'],
        'draw_number':final['draw_number'],'draw_key':final['draw_key'],
        'run_id':final['run_id'],'mode':_MODE,
        'state':'PASS','orphan_suspected':False,'marker_write_failed':False,
        'status_sha256':digest(status_raw),
        'canonical_result_sha256':result_hash,
        'training_view_sha256':final['training_view_sha256'],
        'external_exit_code_verified':False,'self_reported_completion':True,
    }
    write_new(run_dir/'standalone_manifest.json',json_bytes(manifest))
    return manifest


def _load_canonical(path: Path) -> tuple[dict,bytes]:
    if path.is_symlink() or not path.is_file():
        raise ValueError('required regular JSON record missing')
    raw=path.read_bytes()
    obj=json.loads(raw)
    if type(obj) is not dict or raw != json_bytes(obj):
        raise ValueError('not a canonical JSON object')
    return obj,raw


def verify_synthetic_and_consume(run_dir: Path, *, run_id: str,
                                 profile: GameProfile, method_id: str,
                                 variant_id: str, target: int,
                                 global_orphan_marker: Path) -> dict:
    """Manifest/status checked BEFORE result opening, never bypass firewall."""
    if os.path.lexists(global_orphan_marker):
        raise ValueError('global unresolved-orphan safety stop')
    if (not _RUN.fullmatch(run_id) or
            run_dir.name != run_id or run_dir.parent.name != profile.game_id or
            not profile.historical_development_target_allowed(target)):
        raise ValueError('run identity or boundary mismatch')
    manifest,_=_load_canonical(run_dir/'standalone_manifest.json')
    if (manifest.get('schema')!='MULTIGAME_STANDALONE_MANIFEST_V1_REVIEW' or
            manifest.get('state')!='PASS' or manifest.get('orphan_suspected') is not False or
            manifest.get('marker_write_failed') is not False or
            manifest.get('mode')!=_MODE or
            manifest.get('external_exit_code_verified') is not False or
            manifest.get('self_reported_completion') is not True):
        raise ValueError('manifest not eligible')
    expected={'game_id':profile.game_id,'profile_version':profile.version,
              'draw_number':target,'draw_key':profile.draw_key(target),
              'method_id':method_id,'variant_id':variant_id,'run_id':run_id}
    if any(manifest.get(k)!=v for k,v in expected.items()):
        raise ValueError('manifest identity mismatch')
    for fld in ('canonical_result_sha256','training_view_sha256','status_sha256'):
        if type(manifest.get(fld)) is not str or not _HEX.fullmatch(manifest[fld]):
            raise ValueError('manifest digest invalid')
    status,sraw=_load_canonical(run_dir/'status.json')
    if digest(sraw)!=manifest['status_sha256'] or status.get('state')!='SUCCESS' or status.get('schema')!='ENGINEERING_POC_STATUS_V1':
        raise ValueError('terminal status invalid')
    if any(status.get(k)!=v for k,v in expected.items()):
        raise ValueError('status identity mismatch')
    if (status.get('mode')!=_MODE or status.get('case')!=method_id or
            status.get('canonical_result_sha256')!=manifest['canonical_result_sha256'] or
            status.get('training_view_sha256')!=manifest['training_view_sha256']):
        raise ValueError('status/result digest mismatch')
    if (type(status.get('pid')) is not int or status['pid']<=0 or
            not isinstance(status.get('process_create_time_epoch'),(int,float)) or
            not isinstance(status.get('sys_prefix'),str) or not status['sys_prefix'] or
            not isinstance(status.get('elapsed_seconds'),(int,float)) or status['elapsed_seconds']<0 or
            not isinstance(status.get('cpu_time_seconds'),(int,float)) or status['cpu_time_seconds']<0 or
            status.get('peak_field') not in ('peak_wset','peak_rss','UNAVAILABLE')):
        raise ValueError('incomplete status identity/metrics')
    result,raw=_load_canonical(run_dir/'canonical_result.json')
    if digest(raw)!=manifest['canonical_result_sha256']:
        raise ValueError('result digest invalid')
    for k,v in expected.items():
        if k=='run_id':continue
        if k in result and result[k]!=v:
            raise ValueError('result identity mismatch')
    if (result.get('schema')!='MULTIGAME_E1_FORECAST_V1_REVIEW' or
            result.get('game_id')!=profile.game_id or
            result.get('training_view_sha256')!=manifest['training_view_sha256'] or
            result.get('data_kind')!=_MODE or
            set(result.get('barrels',{}))!={b.barrel_id for b in profile.barrels}):
        raise ValueError('wrong result identity or barrels')
    return result
