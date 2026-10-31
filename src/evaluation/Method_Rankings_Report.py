"""WF-1B ranking report tool (R3 stage 2). Launched as: Run_Method_Rankings.bat --game G --batch ID --first S --last L

Reads the frozen forecasts of one walk-forward batch, then (only after its search-log row and scoring plan are
written) the actual development results of the grid's targets, and writes one report (text, CSV and JSON) in
results/method_rankings/<GAME>/. It runs no method, imports no method code, and never reads a holdout draw.
Exit codes: 0 report written; 1 failed after the search-log row was written (the attempt stays counted);
2 refused before anything was written.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent / 'methods'), str(HERE.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='WF-1B method rankings report')
    parser.add_argument('--game', required=True, choices=('POWERBALL', 'OZLOTTO'))
    parser.add_argument('--batch', required=True)
    parser.add_argument('--first', type=int, required=True)
    parser.add_argument('--last', type=int, required=True)
    args = parser.parse_args(argv)

    import _common.contract_publication as CP
    from evaluation import n1 as N1
    from evaluation import report as RP
    from evaluation import report_writer as RW
    from evaluation import seed_policies as SP

    try:
        policy, on_file = SP.approved_policy(), SP.count_policies()
    except ValueError as exc:
        print(f'[RANKINGS] REFUSED: seed policy records are invalid: {exc}. Nothing was written.', file=sys.stderr)
        return 2
    seed_line = (f"policy {policy['policy_id']}, R = {N1.R}" if policy else 'N1_NOT_RUN: seed policy not approved')
    try:
        res = RP.run_report(args.game, args.batch, args.first, args.last,
                            n1_runner=(N1.runner(policy) if policy else None))
    except RP.ReportRefused as exc:
        print(f'[RANKINGS] REFUSED: {exc}. Nothing was read or written.', file=sys.stderr, flush=True)
        return 2
    except Exception as exc:                                     # after the search-log row: the attempt stays counted
        print(f'[RANKINGS] FAILED: {type(exc).__name__}: {exc}. The search-log row for this attempt stays.',
              file=sys.stderr, flush=True)
        return 1
    now = CP.utc_now()
    stamp = now[:19].replace('-', '').replace(':', '') + 'Z'
    env = {k: v for k, v in CP.environment_identity().items() if k in ('python_version', 'numpy_version', 'os_name')}
    try:
        contents = RW.build(res, generated_utc=now, seed_line=seed_line, n1_policies_on_file=on_file, environment=env)
        paths = RW.write(res, contents, stamp)
    except Exception as exc:
        print(f'[RANKINGS] FAILED writing the report: {type(exc).__name__}: {exc}. The search-log row stays.',
              file=sys.stderr, flush=True)
        return 1
    print(f"[RANKINGS] COMPLETE: attempt {res['attempt_id']}, search-log row {res['search_log_row']}", flush=True)
    for p in paths:
        print(f'[RANKINGS] wrote {p}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
