"""MHUP-B: OV-1, the one confirmatory forward test, per game (design supplement v0.8 section 6). Launched as:
Run_Evaluation.bat Method_OV1.py ...   (record normally by the weekly sequencer, Run_Weekly_Session.bat)

  register --game G --statement "<the fixed sentence>"   The owner registers the test for G, once, before its first
                                                         eligible draw. There is no second registration.
  record   --game G                                      Append every OV-1 line that is due. Safe to run at any time.
  stop     --game G --statement "<the fixed sentence>"   The owner stops G's stream. It stays stopped.
  status   --game G                                      Print the stream's state. Writes nothing.
  verify   --game G                                      Rebuild every line and compare bytes. Writes nothing.

It runs no method, makes no forecast, reads no master's draws and uses no network.

The last line printed is machine-readable, for sequencing only (the evidence is the records):
  [OV1] RESULT state=<STATE> game=<G> next=<N or ->
States: REGISTERED, RECORDED (lines appended), NOTHING_DUE, STOPPED, VERIFIED, STATUS, BLOCKED, REFUSED.
Exit codes: 0 done (a stopped stream is a recorded state, reported by the state); 1 blocked (an input is not there yet
or does not verify; nothing was written for that draw; rerun later); 2 refused before anything was written, or invalid
arguments.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent / 'methods'), str(HERE.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _result(state: str, game: str, nxt) -> None:
    print(f'[OV1] RESULT state={state} game={game} next={"-" if nxt is None else nxt}', flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-B OV-1')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('register', 'record', 'stop', 'status', 'verify'):
        sp = sub.add_parser(name)
        sp.add_argument('--game', required=True, choices=('POWERBALL', 'OZLOTTO'))
        if name in ('register', 'stop'):
            sp.add_argument('--statement', required=True)
    args = parser.parse_args(argv)

    from evaluation import ov1 as OV
    echo = lambda s: print(s, flush=True)
    try:
        if args.command == 'register':
            rec = OV.register(args.game, args.statement)
            echo(f'[OV1] registered for {args.game}: the first eligible draw is {rec["first_target"]}; bar {OV.NUM.BAR}')
            _result('REGISTERED', args.game, rec['first_target'])
        elif args.command == 'record':
            out = OV.record(args.game, echo=echo)
            for line in OV.status_lines(args.game):
                echo('[OV1] ' + line)
            state = 'STOPPED' if out['state']['stopped'] else ('RECORDED' if out['written'] else 'NOTHING_DUE')
            _result(state, args.game, out['state']['next_target'])
        elif args.command == 'stop':
            line = OV.stop(args.game, args.statement)
            echo(f'[OV1] the stream of {args.game} is stopped at draw {line["target_draw_number"]}. It stays stopped.')
            _result('STOPPED', args.game, line['target_draw_number'])
        elif args.command == 'status':
            for line in OV.status_lines(args.game):
                echo('[OV1] ' + line)
            _result('STATUS', args.game, OV.status(args.game)['next_target'])
        else:
            out = OV.verify(args.game)
            echo(f'[OV1] verified: {out["lines"]} line(s) rebuilt and equal ({out["eligibility"]} eligibility, '
                 f'{out["factor"]} factor, {out["missed"]} missed, {out["stop"]} stop)')
            _result('VERIFIED', args.game, None)
        return 0
    except OV.OV1Blocked as exc:
        echo(f'[OV1] BLOCKED: {exc}')
        echo('[OV1] nothing was written for that draw or any later one; forecasting and scoring are not affected; '
             'run record again once the input is there')
        _result('BLOCKED', args.game, None)
        return 1
    except OV.OV1Refused as exc:
        echo(f'[OV1] REFUSED: {exc}')
        _result('REFUSED', args.game, None)
        return 2


if __name__ == '__main__':
    sys.exit(main())
