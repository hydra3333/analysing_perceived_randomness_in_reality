"""MHUP-B layer L8: the development batch's sequencer (design supplement v0.8 sections 7.1A and 4 rule 2A; code plan
v0.3 L8 and section 12A; EX_223 C04). Started by the owner as one of:

  Run_Development_Batch.bat --game G --fill
        A new method gets its history: plan the pairs that have no canonical score, run them, report them, admit
        the attempt to the league's sources if nothing conflicts, publish the league table.
  Run_Development_Batch.bat --game G --rerun --first S --last L [--variants M:V,M:V,...]
        A voluntary rerun for research: plan, run, report. Never admitted; the league table does not change.
  Run_Development_Batch.bat --game G --batch wf-...
        Continue a batch this command planned earlier (it prints the batch): what is unfinished is run on, a batch
        without a report is reported, an unadmitted fill is admitted, an unpublished table is published.
  Run_Development_Batch.bat --game G --report --batch wf-... --first S --last L
        Score forecasts an existing batch already holds over S..L (no forecast is run), then admit and publish.

A sequencer, not a coordinator: it imports neither the method code nor the evaluator, starts each child through its
launcher (sequencer_children), reads its output to the end and holds no state. It opens no weekly record. Every step
reads the records, so rerunning continues from them: nothing is planned, run, reported or admitted twice.

Exit statuses: 0 complete; 30 a stop (the child is named; rerun with --batch to continue); 2 refused before any child
started, or invalid arguments.
"""
from __future__ import annotations

import argparse
import sys

import sequencer_children as SC

EXIT_COMPLETE, EXIT_STOP, EXIT_REFUSED = 0, 30, 2
ADMITTED_KINDS = ('ROUTINE_FILL', 'WF_BATCH_PLAN_V1')


def say(text: str) -> None:
    print(f'[DEVELOPMENT-BATCH] {text}', flush=True)


def stop(child: str, code: int, batch: str | None, game: str) -> int:
    say(f'STOPPED at {child} (exit {code}). Nothing already recorded is changed, and no league table was changed by '
        f'this step.')
    say('What to do: read the message above; then continue with  Run_Development_Batch.bat --game ' + game +
        (f' --batch {batch}' if batch else ' and the same options'))
    return EXIT_STOP


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-B development batch')
    parser.add_argument('--game', required=True, choices=SC.GAMES)
    parser.add_argument('--fill', action='store_true')
    parser.add_argument('--rerun', action='store_true')
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--batch')
    parser.add_argument('--first', type=int)
    parser.add_argument('--last', type=int)
    parser.add_argument('--variants')
    args = parser.parse_args(argv)
    g = args.game
    forms = [args.fill, args.rerun, args.report, args.batch is not None and not args.report]
    if sum(forms) != 1:
        parser.error('one of: --fill | --rerun --first S --last L | --batch wf-... | --report --batch wf-... --first S --last L')
    window = (args.first is not None, args.last is not None)
    if (args.rerun or args.report) and window != (True, True):
        parser.error('--rerun and --report need --first and --last')
    if (args.fill or forms[3]) and window != (False, False):
        parser.error('--first and --last belong to --rerun and --report')
    if args.report and args.batch is None:
        parser.error('--report needs --batch')
    if args.variants is not None and not args.rerun:
        parser.error('--variants belongs to --rerun')
    try:
        SC.check_environment()
        walk = lambda *a: SC.run_child(SC.command('experiment', 'Method_Walk_Forward.py', *a))
        league = lambda *a: SC.run_child(SC.command('evaluation', 'Method_League_Table.py', *a))
        batch, scope = args.batch, []
        if args.fill or args.rerun:
            plan = ['plan', '--game', g, '--fill'] if args.fill else \
                ['plan', '--game', g, '--rerun', '--first', args.first, '--last', args.last,
                 *(['--variants', args.variants] if args.variants else [])]
            code, f = walk(*plan)
            if code == 0 and f.get('state') == 'NOTHING_TO_FILL':
                say('nothing to fill: every eligible pair already has a canonical score. Publishing the table if it is due.')
                code, f = league('publish', '--game', g)
                return EXIT_COMPLETE if code == 0 and f.get('state') in ('PUBLISHED', 'UP_TO_DATE') else \
                    stop('publish', code, None, g)
            if code != 0 or f.get('state') != 'PLANNED':
                return stop('plan', code, None, g)
            batch = f['batch']
            say(f'batch {batch} planned. If anything stops, continue with  Run_Development_Batch.bat --game {g} --batch {batch}')
        if args.report:
            scope = ['--first', args.first, '--last', args.last]
        else:
            code, _f = walk('run', '--game', g, '--batch', batch)
            if code != 0:
                return stop('run', code, batch, g)
        code, f = league('batch-state', '--game', g, '--batch', batch, *scope)
        if code != 0 or f.get('state') != 'BATCH':
            return stop('batch-state', code, batch, g)
        kind, first, last = f['kind'], f['first'], f['last']
        if f['report'] == '-':
            code, _f = SC.run_child(SC.command('rankings', '--game', g, '--batch', batch, '--first', first, '--last', last))
            if code != 0:
                return stop('the report', code, batch, g)
        else:
            say(f'batch {batch} already has its report ({f["report"]}); not reported again')
        if kind not in ADMITTED_KINDS:
            say(f'complete: batch {batch} ({kind}) run and reported. An exploratory rerun is never admitted: the league '
                f'table and its totals are unchanged. Its report sets it beside the canonical figures.')
            return EXIT_COMPLETE
        code, f = league('admit', '--game', g, '--batch', batch, '--first', first, '--last', last)
        if code != 0 or f.get('state') not in ('ADMITTED', 'ALREADY_ADMITTED'):
            return stop('admit', code, batch, g)
        code, f = league('publish', '--game', g)
        if code != 0 or f.get('state') not in ('PUBLISHED', 'UP_TO_DATE'):
            return stop('publish', code, batch, g)
        say(f'complete: batch {batch} ({kind}) run, reported, admitted and the league table ' +
            ('published' if f['state'] == 'PUBLISHED' else 'already up to date'))
        return EXIT_COMPLETE
    except SC.SequencerRefused as exc:
        say(f'REFUSED: {exc}. Nothing further was started.')
        return EXIT_REFUSED


if __name__ == '__main__':
    sys.exit(main())
