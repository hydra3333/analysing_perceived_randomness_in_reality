"""MHUP-B: the consolidated (weekly) report (design v0.1r7 section 6.6; design supplement v0.8 section 8). Launched as:
Run_Evaluation.bat Method_Weekly_Report.py --game G [--ov1-cohort current|all|M:R:V,M:R:V,...]
                                                    [--ov1-first S --ov1-last L]

One report of one game, on request (or monthly): the latest published league table (quoted), the registered formal OV-1
test's state, the RETROSPECTIVE OV-1 view (descriptive; not the formal test; no P value), the forward and catch-up
tables (secondary, EXPLORATORY_COHORT), the matched-target view, the development and Mode H reports quoted by identity,
and the retired-revision index. Nothing is pooled into a P value; the games are never combined.

  --ov1-cohort   the variants of the retrospective OV-1 ensemble: `current` (default: the released, unretired
                 variants), `all` (every scored identity, each revision its own member), or a named list of
                 METHOD:REVISION:VARIANT. The choice is printed with the view and is part of its identity.
  --ov1-first, --ov1-last   limit the retrospective view to a window of draws (default: every scored draw).

It reads accepted scores and frozen forecasts. It runs no method, scores nothing, reads no draw's result from a master,
publishes no league table, writes nothing to the OV-1 ledger and uses no network.

The last line printed is machine-readable, for sequencing only:
  [WEEKLY-REPORT] RESULT state=<STATE> game=<G> attempt=<id or ->
Exit codes: 0 report written; 1 failed after the search-log row was written (the attempt stays counted); 2 refused
before anything was written, or invalid arguments.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent / 'methods'), str(HERE.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _result(state: str, game: str, attempt=None) -> None:
    print(f'[WEEKLY-REPORT] RESULT state={state} game={game} attempt={attempt or "-"}', flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-B consolidated weekly report')
    parser.add_argument('--game', required=True, choices=('POWERBALL', 'OZLOTTO'))
    parser.add_argument('--ov1-cohort', default='current')
    parser.add_argument('--ov1-first', type=int)
    parser.add_argument('--ov1-last', type=int)
    args = parser.parse_args(argv)
    if args.ov1_cohort.lower() in ('current', 'all'):
        cohort = args.ov1_cohort.upper()
    else:
        cohort = [x.split(':') for x in args.ov1_cohort.split(',')]
        if any(len(c) != 3 or not all(c) for c in cohort):
            parser.error('--ov1-cohort is current, all, or a list of METHOD:REVISION:VARIANT separated by commas')

    import _common.contract_publication as CP
    from evaluation import consolidated_report as CRP
    from evaluation import n1 as N1
    from evaluation import seed_policies as SP
    try:
        policy = SP.approved_policy()
    except ValueError as exc:
        print(f'[WEEKLY-REPORT] REFUSED: seed policy records are invalid: {exc}. Nothing was written.', file=sys.stderr)
        _result('REFUSED', args.game)
        return 2
    try:
        res = CRP.run_report(args.game, cohort=cohort, ov1_first=args.ov1_first, ov1_last=args.ov1_last,
                             n1_runner=(N1.runner(policy) if policy else None),
                             echo=lambda text: print(f'[WEEKLY-REPORT] {text}', flush=True))
    except CRP.ReportRefused as exc:
        print(f'[WEEKLY-REPORT] REFUSED: {exc}. Nothing was written.', file=sys.stderr, flush=True)
        _result('REFUSED', args.game)
        return 2
    except Exception as exc:                                  # after the search-log row: the attempt stays counted
        print(f'[WEEKLY-REPORT] FAILED: {type(exc).__name__}: {exc}. The search-log row for this attempt stays; nothing '
              f'else was changed.', file=sys.stderr, flush=True)
        _result('FAILED', args.game)
        return 1
    now = CP.utc_now()
    try:
        paths = CRP.write(res, CRP.build(res, now), now[:19].replace('-', '').replace(':', '') + 'Z')
    except Exception as exc:
        print(f'[WEEKLY-REPORT] FAILED writing the report: {type(exc).__name__}: {exc}. The search-log row stays.',
              file=sys.stderr, flush=True)
        _result('FAILED', args.game, res['attempt_id'])
        return 1
    for p in paths:
        print(f'[WEEKLY-REPORT] wrote {p.name}', flush=True)
    _result('WRITTEN', args.game, res['attempt_id'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
