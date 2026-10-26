"""PACKAGE 2 REVIEW — pure synthetic coordinator plumbing probe for E_1 identity.

NOT a real E_1 forecast, not eligible for statistical scoring. No real CSV,
no outcomes, no scrape, no child processes and no access to either holdout.
Current coordinator cannot launch this script (scientific gate disabled).
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import sys

from _common.multigame_standalone_contract_v1 import json_bytes
from _common.experiment_runtime_status_and_resources import ProbeStatus
from _common.multigame_coordinated_manifest_v1 import publish_coordinated_success
from _common.multigame_result_registry_v1 import SYNTHETIC_MODE, SYNTHETIC_VARIANT, SYNTHETIC_SCHEMA

METHOD = 'E_1'


def main(argv: list[str] | None = None, *, test_synthetic_root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description='Synthetic E_1 coordinator plumbing probe ONLY')
    parser.add_argument('--synthetic-contract-probe', action='store_true', required=True)
    parser.add_argument('--await-coordinator-release', action='store_true', default=False)
    parser.add_argument('--game', choices=('POWERBALL','OZLOTTO'), required=True)
    parser.add_argument('--target', type=int, required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--group-id', required=True)
    parser.add_argument('--worker-sequence', type=int, required=True)
    parser.add_argument('--variant', required=True, choices=(SYNTHETIC_VARIANT,))
    args = parser.parse_args(argv)
    # Launch specification has no dynamic source paths or arbitrary barrel values.
    project = Path(__file__).resolve().parents[2]
    root = test_synthetic_root if test_synthetic_root is not None else (project / 'transitory_data' / 'multigame_synthetic_runs')
    marker = project / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
    if os.path.lexists(marker):
        parser.error('global unresolved orphan safety stop')
    from _common.multigame_worker_launch_handshake_v1 import verify_synthetic_worker_request
    identity,run_dir,profile_version=verify_synthetic_worker_request(
            group_id=args.group_id,worker_sequence=args.worker_sequence,
            run_id=args.run_id,game_id=args.game,draw_number=args.target,
            method_id=METHOD,variant_id=args.variant,root=root)
    if run_dir.exists() or run_dir.is_symlink():
        parser.error('run directory exists: create-only identity collision')
    run_dir.mkdir(parents=True,exist_ok=False)
    status = ProbeStatus(run_dir / 'status.json',args.run_id,METHOD,
            identity={**{k:v for k,v in identity.items() if k!='run_id'},
                      'mode':SYNTHETIC_MODE, 'profile_version':profile_version})
    print(f'BEGIN {METHOD} game={args.game} draw={args.target} run={args.run_id}',flush=True)
    try:
        if args.await_coordinator_release:
            from _common.multigame_ancestry_release_v1 import await_release
            born = status.value.get('process_create_time_epoch')
            if type(born) not in (float, int) or born <= 0:
                raise ValueError('worker process creation time not available')
            await_release(run_dir=run_dir, identity=identity, pid=os.getpid(),
                          create_time_epoch=born, orphan_marker=marker)
        # Deliberately NOT model science: a static plumbing payload is used
        # to prove statuses/manifest/hash/console binding only.
        result={**identity, 'schema':SYNTHETIC_SCHEMA, 'mode':SYNTHETIC_MODE,
                'data_kind':SYNTHETIC_MODE,
                'profile_version':profile_version,
                'draw_key':f'{args.game}_{args.target}',
                'not_a_forecast':True,'payload':{'plumbing_probe':'NON_SCIENTIFIC'}}
        result_digest=hashlib.sha256(json_bytes(result)).hexdigest()
        status.finish('SUCCESS',terminal_fields={'canonical_result_sha256':result_digest})
        records=publish_coordinated_success(run_dir=run_dir,
                    identity=identity,status=status.value,result=result)
        for line in records[1:]:
            print(line,flush=True)
        return 0
    except (Exception,KeyboardInterrupt) as exc:
        try:
            if status.value.get('state') == 'STARTED':
                status.finish('FAILED',error=f'{type(exc).__name__}')
        except Exception:
            pass
        print(f'FINISH {METHOD} game={args.game} draw={args.target} run={args.run_id} FAILED',flush=True)
        print(f'[SYNTHETIC WORKER] FAILED {type(exc).__name__}',file=sys.stderr,flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
