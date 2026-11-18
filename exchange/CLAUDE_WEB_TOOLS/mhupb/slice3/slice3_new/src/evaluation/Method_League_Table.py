"""MHUP-B: the league table tool (design supplement v0.8 sections 3 to 5). Launched as:
Run_Evaluation.bat Method_League_Table.py ...   (publish and admit normally by a sequencer; the owner may run any)

  publish        --game G                Publish the game's league table if its inputs changed since the last one
                                         (first finishing any unfinished publication). Up to date: nothing is written.
  repair         --game G                Finish or mark any unfinished publication; restore the current folder.
  admit          --game G --attempt rr-...   |   --game G --batch wf-... [--first S --last L]
                                         Add one COMPLETE routine-fill or first-kind report attempt to the game's
                                         source list, if none of its keys is already supplied. A repeat changes nothing.
  batch-state    --game G --batch wf-... [--first S --last L]
                                         Where a development batch's job stands, from the records. Read-only.
  sources-check  --game G                Read every source and every logged publication. Read-only.
  history        --game G                Join the published tables, newest first. Recomputes nothing.
  reconstruction --game G                The current-cohort historical reconstruction (a labelled CSV).

It reads scores; it never scores, forecasts, reads a draw's result or uses a network. The sealed Mode H ledger is shown
and never summed.

The last line printed is machine-readable, for sequencing only (the evidence is the records):
  [LEAGUE] RESULT state=<STATE> game=<G> name=<publication, attempt or ->
  [LEAGUE] RESULT state=BATCH game=<G> kind=<K> first=<S> last=<L> report=<attempt or -> admitted=<attempt or ->
Exit codes: 0 done; 1 failed part-way (rerun: an unfinished publication is finished or marked); 2 refused before
anything was written, or invalid arguments.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent / 'methods'), str(HERE.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _result(state: str, game: str, name=None) -> None:
    print(f'[LEAGUE] RESULT state={state} game={game} name={name or "-"}', flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-B league table')
    sub = parser.add_subparsers(dest='command', required=True)
    games = ('POWERBALL', 'OZLOTTO')
    for name in ('publish', 'repair', 'sources-check', 'history', 'reconstruction'):
        sub.add_parser(name).add_argument('--game', required=True, choices=games)
    for name in ('admit', 'batch-state'):
        p = sub.add_parser(name)
        p.add_argument('--game', required=True, choices=games)
        p.add_argument('--batch')
        p.add_argument('--first', type=int)
        p.add_argument('--last', type=int)
        if name == 'admit':
            p.add_argument('--attempt')
    args = parser.parse_args(argv)
    if args.command in ('admit', 'batch-state'):
        if args.command == 'admit' and (args.attempt is None) == (args.batch is None):
            parser.error('admit takes --attempt, or --batch (with --first and --last for a batch of the first kind)')
        if args.command == 'batch-state' and args.batch is None:
            parser.error('batch-state needs --batch')
        if (args.first is None) != (args.last is None):
            parser.error('--first and --last go together')

    from evaluation import league_publish as LP
    from evaluation import league_sources as LS
    echo = lambda s: print(s, flush=True)
    g = args.game
    try:
        if args.command == 'publish':
            res = LP.publish(g, echo=echo)
            echo(f'[LEAGUE] {g}: ' + (f'the table is up to date ({res["name"]}); nothing was written'
                                      if res['state'] == 'UP_TO_DATE' else f'new table {res["name"]}'))
            _result(res['state'], g, res['name'])
        elif args.command == 'repair':
            res = LP.repair(g, echo=echo)
            echo(f'[LEAGUE] {g}: {len(res["finished"])} finished, {len(res["incomplete"])} marked incomplete; current '
                 f'folder: {res["current"] or "no publication yet"}')
            _result('REPAIRED', g)
        elif args.command == 'admit':
            res = LP.admit(g, attempt_id=args.attempt, batch_id=args.batch, first=args.first, last=args.last)
            echo(f'[LEAGUE] {g}: attempt {res["attempt_id"]} ' +
                 ('is now a canonical source' if res['state'] == 'ADMITTED' else
                  'was already listed, identically; the source list was not rewritten'))
            _result(res['state'], g, res['attempt_id'])
        elif args.command == 'batch-state':
            st = LS.batch_state(LS.project_root(), g, args.batch, args.first, args.last)
            for why in st['incomplete_reasons']:
                echo(f'[LEAGUE] not a complete report: {why}')
            report = st['admitted'] or (st['complete'][0] if st['complete'] else None)
            print(f'[LEAGUE] RESULT state=BATCH game={g} kind={st["batch_kind"]} first={st["first"]} last={st["last"]} '
                  f'report={report or "-"} admitted={st["admitted"] or "-"}', flush=True)
        elif args.command == 'sources-check':
            res = LP.sources_check(g)
            echo(f'[LEAGUE] {g}: {res["sources"]} listed development attempts, {res["rows"]} summed score rows; Mode H as '
                 f'sealed: {res["mode_h"]}; {res["logged"]} published tables, {len(res["pending"])} unfinished, '
                 f'{len(res["incomplete"])} marked incomplete; current folder notice: '
                 f'{"PRESENT (run repair)" if res["current_notice"] else "none"}')
            for n in res['not_available']:
                echo(f'[LEAGUE] not available: {n["source"]}: {n["reason"]}')
            _result('CHECKED', g)
        else:
            res = LP.history(g) if args.command == 'history' else LP.reconstruction(g)
            echo(f'[LEAGUE] {g}: {res["path"].name} ({res["state"].lower()})')
            _result(res['state'], g, res['path'].name)
        return 0
    except LS.LeagueRefused as exc:
        print(f'[LEAGUE] REFUSED: {exc}.', file=sys.stderr, flush=True)
        _result('REFUSED', g)
        return 2
    except Exception as exc:                                  # part-way: the next publish or repair finishes or marks it
        print(f'[LEAGUE] FAILED: {type(exc).__name__}: {exc}. Nothing published is changed; rerun publish or repair.',
              file=sys.stderr, flush=True)
        _result('FAILED', g)
        return 1


if __name__ == '__main__':
    sys.exit(main())
