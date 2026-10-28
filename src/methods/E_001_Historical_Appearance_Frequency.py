"""P3 E_001 single executable review candidate; SYNTHETIC CONTRACT MODE ONLY for now.

The real-data code path is deliberately hard-disabled until independent review.
No subprocess launches, timers, termination or coordinator invocation.
"""
from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

# Code-level gate cannot be set by a CLI flag or environment variable.
# Flip only in a separately accepted, reviewed, owner-authorised patch.
ENABLE_REAL_HISTORICAL_DEVELOPMENT = True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='E_1 standalone review-candidate runner')
    parser.add_argument('--mode', choices=('synthetic-contract', 'historical-development'), required=True)
    parser.add_argument('--target', type=int, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--run-id', default='e1-' + uuid.uuid4().hex)
    parser.add_argument('--synthetic-run-root', type=Path, default=None,
                        help='synthetic mode only; isolated test artifact directory')
    args = parser.parse_args(argv)
    if args.mode == 'historical-development' and not ENABLE_REAL_HISTORICAL_DEVELOPMENT:
        parser.error('REAL HISTORICAL DEVELOPMENT DISABLED pending loader/status review and owner gate')
    if args.mode == 'historical-development' and args.synthetic_run_root is not None:
        parser.error('synthetic-run-root is not a real-mode option')
    project = Path(__file__).resolve().parents[2]
    trusted_real_source = project / 'source_data'
    marker = project / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
    if marker.exists() or marker.is_symlink():
        parser.error('unresolved orphan marker: no standalone experiment permitted')
    mode = ('SYNTHETIC_CONTRACT_TEST' if args.mode == 'synthetic-contract'
            else 'REAL_HISTORICAL_DEVELOPMENT')
    if mode == 'SYNTHETIC_CONTRACT_TEST':
        if args.synthetic_run_root is None:
            parser.error('synthetic mode requires --synthetic-run-root')
        root = args.synthetic_run_root.resolve()
        if root.is_relative_to((project / 'results').resolve()) or root.is_relative_to(trusted_real_source.resolve()):
            parser.error('synthetic output cannot be placed in real results/source namespaces')
        if args.source.resolve().is_relative_to(trusted_real_source.resolve()):
            parser.error('synthetic mode may not read the real source_data directory')
    else:
        root = project / 'transitory_data' / 'p3_standalone_runs'
    from E_001.e1_standalone_contract import (
        begin, canonical_json, create_only, finish, publish_failed_manifest,
        publish_success_manifest, sha)
    # Durable STARTED happens before CSV/model/numerics imports or source reads.
    run_dir = root / args.run_id
    try:
        status = begin(run_dir, args.run_id, mode, args.target)
    except Exception as exc:
        print(f'[E_1] REFUSED before STARTED: {type(exc).__name__}: {exc}', file=sys.stderr, flush=True)
        return 2
    print(f'[E_001] STARTED run={args.run_id} mode={mode} target={args.target}', flush=True)
    try:
        from E_001.e1_training_view import load_permitted_u_view, build_e1_forecast
        rows, digest = load_permitted_u_view(args.source, args.target, source_kind=mode,
                                           trusted_source_dir=(trusted_real_source if mode == 'REAL_HISTORICAL_DEVELOPMENT' else None))
        result = build_e1_forecast(rows, digest, args.target, source_kind=mode)
        raw = canonical_json(result)
        result_digest = sha(raw)
        create_only(run_dir / 'canonical_result.json', raw)
        # Any printing must be BEFORE terminal SUCCESS and PASS manifest.
        print(f'[E_1] synthetic/development result prepared; target={args.target}; '
              f'canonical_sha256={result_digest}', flush=True)
        finished = finish(run_dir, status, 'SUCCESS', training_digest=digest,
                          result_digest=result_digest)
        publish_success_manifest(run_dir, finished, result_digest, digest)
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        interrupted = isinstance(exc, KeyboardInterrupt)
        try:
            failed = finish(run_dir, status, 'FAILED',
                            error=f'{type(exc).__name__}: {exc}',
                            failure_reason='INTERRUPTED' if interrupted else None)
            publish_failed_manifest(run_dir, failed)
        except Exception as secondary:
            # If recording failure also fails, no valid PASS manifest may be
            # assumed; test harness will refuse, and an operator must inspect.
            print(f'[E_1] CRITICAL failure recording status: {secondary}',
                  file=sys.stderr, flush=True)
        print(f'[E_1] FAILED: {type(exc).__name__}: {exc}', file=sys.stderr, flush=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
