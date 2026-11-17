"""MHUP-B: the scoring half of the weekly session (design v0.1r7 section 6). Launched as:
Run_Evaluation.bat Method_Weekly_Score.py ...   (score normally by the weekly sequencer, Run_Weekly_Session.bat)

  score            --game G --session S --target N   Score the records N's freeze line names that have no score line.
  witness          --game G --target N --kind github|email --ref <commit id or message id>
                                                     Record that N's freeze line digest was pushed or emailed.
  verify           --game G --target N --verified-by project-owner|reviewer --received-utc <UTC instant>
                   --evidence "<the service's own receipt, quoted; it must contain the reference>"
  diagnostic-score --game G --run <run id>           Print one diagnostic record's quantities. Writes nothing.

It scores and records witnesses. It runs no method, makes no forecast and uses no network. The outcome of a draw is
read only under the freeze-before-outcome rule.

The last line printed is machine-readable, for sequencing only (the evidence is the records):
  [WEEKLY-SCORE] RESULT state=<STATE> target=<N or -> session=<id or ->
Exit codes: 0 done; 1 stopped part-way (the lines written stand; rerun to resume); 2 refused before anything was
written, or invalid arguments.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent / 'methods'), str(HERE.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _result(state: str, target, session) -> None:
    print(f'[WEEKLY-SCORE] RESULT state={state} target={"-" if target is None else target} '
          f'session={session or "-"}', flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-B weekly scoring half')
    sub = parser.add_subparsers(dest='command', required=True)
    games = ('POWERBALL', 'OZLOTTO')
    sc = sub.add_parser('score')
    sc.add_argument('--game', required=True, choices=games)
    sc.add_argument('--session', required=True)
    sc.add_argument('--target', required=True, type=int)
    wi = sub.add_parser('witness')
    wi.add_argument('--game', required=True, choices=games)
    wi.add_argument('--target', required=True, type=int)
    wi.add_argument('--kind', required=True)
    wi.add_argument('--ref', required=True)
    ve = sub.add_parser('verify')
    ve.add_argument('--game', required=True, choices=games)
    ve.add_argument('--target', required=True, type=int)
    ve.add_argument('--verified-by', required=True)
    ve.add_argument('--received-utc', required=True)
    ve.add_argument('--evidence', required=True)
    ds = sub.add_parser('diagnostic-score')
    ds.add_argument('--game', required=True, choices=games)
    ds.add_argument('--run', required=True)
    args = parser.parse_args(argv)

    from evaluation import weekly_score as WS
    echo = lambda s: print(s, flush=True)
    target, session = getattr(args, 'target', None), getattr(args, 'session', None)
    try:
        if args.command == 'score':
            WS.score(args.game, args.session, args.target, echo=echo)
            _result('SCORED', target, session)
        elif args.command == 'witness':
            w = WS.witness(args.game, args.target, args.kind, args.ref)
            echo(f'[WEEKLY-SCORE] witness recorded for draw {args.target}: {w["witness_kind"]} {w["ref"]} (a claim, not proof)')
            _result('WITNESS_RECORDED', target, None)
        elif args.command == 'verify':
            WS.verify(args.game, args.target, args.verified_by, args.received_utc, args.evidence)
            echo(f'[WEEKLY-SCORE] witness verification recorded for draw {args.target} (digest binding: human-checked)')
            _result('WITNESS_VERIFIED', target, None)
        else:
            out = WS.diagnostic_score(args.game, args.run)
            echo('[WEEKLY-SCORE] DIAGNOSTIC (unofficial; nothing was written to any ledger):')
            echo(json.dumps(out, indent=1, sort_keys=True))
            _result('DIAGNOSTIC', out['target_draw_number'], None)
        return 0
    except WS.ScoreStopped as exc:
        print(f'[WEEKLY-SCORE] STOP: {exc}. Rerun the weekly session to resume.', file=sys.stderr, flush=True)
        _result('STOPPED', target, session)
        return 1
    except (WS.ScoreRefused, ValueError) as exc:
        print(f'[WEEKLY-SCORE] REFUSED: {exc}. Nothing was written by this command.', file=sys.stderr, flush=True)
        _result('REFUSED', target, session)
        return 2


if __name__ == '__main__':
    sys.exit(main())
