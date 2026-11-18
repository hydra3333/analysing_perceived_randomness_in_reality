"""MHUP-B layer L8: the weekly session's sequencer (design v0.1r7 section 6.1 and Appendix F; code plan v0.3 L8).
Started by the owner as:  Run_Weekly_Session.bat --game G

A sequencer, not a coordinator: it imports neither the method code nor the evaluator, starts each child through its
launcher (sequencer_children), reads the child's output to the end, and holds no state of its own. Rerunning the
command continues from the records alone.

  1. the status block;
  2. open a session, or (a session lock exists) the process check and then resume;
  3. the loop: `next`; on FROZE N, `score` N and then OV-1's `record`; at the loop's end (FROZE_NEXT, OPEN, NONE or
     STALE) OV-1's `record` at once, so a frozen forecast's pre-draw entry is made, or made up, before its cut-off;
  4. `close-session` (on FROZE_NEXT, OPEN, NONE or STALE);
  5. then, and only then, the league table's `publish` (which first finishes any unfinished publication);
  6. the status block again, and what happened.

THE LIVE PATH COMES FIRST. A stop of the forecasting or scoring half stops the sequence and leaves the lock (rerun to
resume). The reporting steps (OV-1's recorder, the league table) never stop, undo or delay the live path: if one
fails, the session still closes and the exit status says which reporting step to rerun.

Exit statuses: 0 complete; 20 frozen and scored, the league table not written; 21 frozen and scored, OV-1's recorder
failed or was blocked; 22 both; 30 a stop of the live path (the child is named); 2 refused before any child started.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import sequencer_children as SC

EXIT_COMPLETE, EXIT_TABLE, EXIT_OV1, EXIT_BOTH, EXIT_LIVE_STOP, EXIT_REFUSED = 0, 20, 21, 22, 30, 2
CLEAN_ENDS = ('FROZE_NEXT', 'OPEN', 'NONE', 'STALE')
OV1_FINE = ('RECORDED', 'NOTHING_DUE', 'NOT_REGISTERED', 'STOPPED')


def say(text: str) -> None:
    print(f'[WEEKLY-SESSION] {text}', flush=True)


def live_stop(child: str, code: int) -> int:
    say(f'STOPPED at {child} (exit {code}). The records written so far stand and the session lock is left in place.')
    say('What to do: read the message above; when its cause is dealt with, run the same command again to resume.')
    return EXIT_LIVE_STOP


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-B weekly session')
    parser.add_argument('--game', required=True, choices=SC.GAMES)
    args = parser.parse_args(argv)
    g = args.game
    try:
        SC.check_environment()
        forecast = lambda *a: SC.run_child(SC.command('experiment', 'Method_Weekly_Forecast.py', *a))
        evaluate = lambda tool, *a: SC.run_child(SC.command('evaluation', tool, *a))
        code, _f = forecast('status', '--game', g)
        if code != 0:
            return live_stop('status', code)
        if (SC.ROOT / 'results' / 'real' / 'weekly' / g / 'ACTIVE_SESSION.lock').exists():
            say('a session lock exists: checking that no run is in progress, then resuming that session')
            code, _f = SC.run_child(SC.command('process', 'check-no-runs', '--game', g))
            if code != 0:
                return live_stop('the process check', code)
            code, f = forecast('open-session', '--game', g, '--resume')
        else:
            code, f = forecast('open-session', '--game', g)
        session = f.get('session', '-')
        if code != 0 or session == '-':
            return live_stop('open-session', code)
    except SC.SequencerRefused as exc:
        say(f'REFUSED: {exc}. Nothing was started.')
        return EXIT_REFUSED

    ov1_trouble, ov1_stopped, last_scored, end = [], False, None, None

    def record_ov1(after: str) -> None:
        nonlocal ov1_stopped
        code, f = evaluate('Method_OV1.py', 'record', '--game', g)
        state = f.get('state')
        if code != 0 or state not in OV1_FINE:              # the state line is read, not only the exit code
            ov1_trouble.append(f'{after}: exit {code}, state {state or "none"}')
        ov1_stopped = ov1_stopped or state == 'STOPPED'

    while end is None:
        code, f = forecast('next', '--game', g, '--session', session)
        state, target = f.get('state'), f.get('target', '-')
        if code != 0 or state is None:
            return live_stop('next', code)
        if state == 'FROZE':
            if target == last_scored:
                say(f'draw {target} came back for scoring a second time: no progress')
                return live_stop('next (no progress)', code)
            code, f = evaluate('Method_Weekly_Score.py', 'score', '--game', g, '--session', session, '--target', target)
            if code != 0 or f.get('state') != 'SCORED':
                return live_stop(f'score (draw {target})', code)
            last_scored = target
            record_ov1(f'after the score of draw {target}')
        elif state in CLEAN_ENDS:
            record_ov1(f'at the end of the loop ({state}' + (f', draw {target})' if target != '-' else ')'))
            end = (state, target)
        else:
            return live_stop(f'next (state {state})', code)

    code, _f = forecast('close-session', '--game', g, '--session', session)
    if code != 0:
        return live_stop('close-session', code)
    # ---- the live path is complete and closed. Reporting follows; it cannot change anything above.
    code, f = evaluate('Method_League_Table.py', 'publish', '--game', g)
    table_ok = code == 0 and f.get('state') in ('PUBLISHED', 'UP_TO_DATE')
    forecast('status', '--game', g)

    say(f'session {session} closed at a clean end: {end[0]}' + (f' (draw {end[1]})' if end[1] != '-' else ''))
    if end[0] == 'STALE':
        say('the results master changed during the session: run the weekly session again to continue from the records')
    if ov1_stopped:
        say('*' * 80)
        say('OV-1: THE FORMAL STREAM OF THIS GAME IS STOPPED AND STAYS STOPPED. Forecasting, scoring and the league')
        say('table go on as normal. Tell Claude and the reviewer (the reason is printed above by the OV-1 tool).')
        say('*' * 80)
    if table_ok and not ov1_trouble:
        say('complete: forecasts frozen, scores written, OV-1 recorded, league table ' +
            ('published' if f.get('state') == 'PUBLISHED' else 'already up to date'))
        return EXIT_COMPLETE
    if ov1_trouble:
        say('OV-1\'s recorder did not finish (' + '; '.join(ov1_trouble) + '). The forecasts and scores are safe.')
        say('What to do: run  Run_Evaluation.bat Method_OV1.py record --game ' + g + '  (before the next draw\'s cut-off '
            'if a forecast was frozen today); if it is blocked again, tell Claude.')
    if not table_ok:
        say('the league table was not written. The forecasts and scores are safe.')
        say('What to do: run  Run_Evaluation.bat Method_League_Table.py publish --game ' + g + '  (it finishes or marks '
            'anything unfinished first).')
    return EXIT_BOTH if ov1_trouble and not table_ok else EXIT_OV1 if ov1_trouble else EXIT_TABLE


if __name__ == '__main__':
    sys.exit(main())
