"""MHUP-B: the forecasting half of the weekly session (design v0.1r7 section 6). Launched as:
Run_Experiment.bat Method_Weekly_Forecast.py ...   (normally by the weekly sequencer, Run_Weekly_Session.bat)

  status        --game G                 Print the status block. Read-only.
  open-session  --game G [--resume]      Open a new session (the session record, then the lock), or reopen the session
                                         the lock names (needs a fresh resume token from the process check).
  next          --game G --session S     One step of the session: catch up the lowest unclosed accepted draw, or
                                         freeze the next draw's forecast, or report OPEN, NONE or STALE.
  close-session --game G --session S     Remove the lock at a clean end.

It forecasts and freezes. It never scores, reads no outcome and imports nothing from the evaluator. Every run goes
through the unchanged contract runner and its dispatch gate, ticketed and bound to the session. No subprocess, timer or
termination is involved.

The last line printed is machine-readable, for sequencing only (the evidence is the records):
  [WEEKLY-FORECAST] RESULT state=<STATE> target=<N or -> session=<id or ->
Exit codes: 0 the command did its work (see the state); 1 stopped part-way (records kept; rerun to resume);
2 refused before anything was written, or invalid arguments.
"""
from __future__ import annotations

import argparse
import sys

from Method_Contract_Runner import ADAPTERS


def _result(state: str, target, session) -> None:
    print(f'[WEEKLY-FORECAST] RESULT state={state} target={"-" if target is None else target} '
          f'session={session or "-"}', flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-B weekly forecasting half')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status').add_argument('--game', required=True)
    op = sub.add_parser('open-session')
    op.add_argument('--game', required=True)
    op.add_argument('--resume', action='store_true')
    for name in ('next', 'close-session'):
        p = sub.add_parser(name)
        p.add_argument('--game', required=True)
        p.add_argument('--session', required=True)
    args = parser.parse_args(argv)

    import _common.weekly_session as WS
    echo = lambda s: print(s, flush=True)
    try:
        if args.command == 'status':
            for line in WS.status_lines(WS.status(args.game)):
                echo(line)
            _result('STATUS', None, None)
            return 0
        if args.command == 'open-session':
            rec = WS.open_session(args.game, ADAPTERS, resume=args.resume)
            echo(f"[WEEKLY-FORECAST] session {rec['session_id']} {'resumed' if args.resume else 'opened'}: {args.game}, "
                 f"master version {rec['ledger_version']} (last draw {rec['last_draw']}), {len(rec['roster'])} variants")
            _result('RESUMED' if args.resume else 'OPENED', None, rec['session_id'])
            return 0
        if args.command == 'next':
            state, target = WS.next_step(args.game, args.session, ADAPTERS, echo=echo)
            _result(state, target, args.session)
            return 0
        end = WS.close_session(args.game, args.session)
        echo(f'[WEEKLY-FORECAST] session {args.session} closed at a clean end ({end}); the lock is removed')
        _result('CLOSED', None, args.session)
        return 0
    except WS.SessionStopped as exc:
        print(f'[WEEKLY-FORECAST] STOP: {exc}. The records written so far stand; rerun the weekly session to resume.',
              file=sys.stderr, flush=True)
        _result('STOPPED', None, getattr(args, 'session', None))
        return 1
    except (WS.SessionRefused, ValueError) as exc:
        print(f'[WEEKLY-FORECAST] REFUSED: {exc}. Nothing was written by this command.', file=sys.stderr, flush=True)
        _result('REFUSED', None, getattr(args, 'session', None))
        return 2


if __name__ == '__main__':
    sys.exit(main())
