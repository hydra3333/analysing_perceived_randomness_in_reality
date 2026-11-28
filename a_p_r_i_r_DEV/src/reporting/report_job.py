"""The reporting part's work for one game, and Run_Reports.bat.

What this file is for
    make_reports makes every report of a game from its records: the league report of every scored draw, the
    next-draw report of every draw some forecast was made for before its result was on file, the two OV-1
    print-outs and the README. A file is written only if its bytes would change, and every report file the
    records no longer give is removed. The research job calls it at the end of each game's work, with the
    records it holds. Run_Reports.bat calls it without a research job: the tree's lock is taken, each game's
    stored science is read and checked (report_inputs.py), and the reports are made from it. Nothing here
    computes a forecast, a score or an OV-1 line, or writes outside the game's reports folder.

    In this slice (S1 of the code plan) the reports are exactly those the engine made before; the ranking
    reports, the settings and LAST, DRAW and ALL come in slice S3.

Which part of the design it carries out
    doc/Predictive_Randomness_Reporting_Design_And_Specification_Amendment_A1_v0_5.md (RAT-74) A2 (the reporting
    part, its lock, its exit codes) and Part B section 1, 9.1 and 9.9.

Which of the project's own modules it uses
    reporting.printouts       the report files themselves
    reporting.report_inputs   load_game: a game's stored science, read and checked
    research.tree_lock        enter_tree, tree_lock: the tree's identity and its lock

What uses it
    research/research_job.py (at the end of each game), src/research_command.py (Run_Reports.bat), and the tests.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from reporting import printouts
from reporting.report_inputs import InputsRefused, load_game
from research.settings import SettingsRefused
from research.tree_lock import LaunchRefused, enter_tree, tree_lock

# The games, in the order a run for BOTH works them. They are never pooled.
GAMES = ('POWERBALL', 'OZLOTTO')
# The folders of a game's reports folder whose every file is made again (the README and the side file of making
# times lie beside them).
REPORT_FOLDERS = ('league', 'next', 'ov1')
# The exit codes of Run_Reports.bat: every report asked for is made; reports were made but at least one game was
# refused or did not finish; nothing was made (the tree, its lock, or every game asked for refused).
EXIT_DONE, EXIT_INCOMPLETE, EXIT_REFUSED = 0, 1, 2


def remove_reports_no_longer_made(reports_folder: Path, made: set) -> int:
    """Delete every file of the league, next-draw and OV-1 report folders that this run did not make: a report
    for a draw the results no longer hold, a next-draw report of a forecast that has since been made again, a
    file left half written. What stays is exactly what the records now give.

    reports_folder: the game's reports folder.  made: the names this run made (written or found unchanged), from
    that folder with forward slashes, for example {'league/league_POWERBALL_d01601.txt', ...}.
    Returns how many files were deleted.
    """
    removed = 0
    for folder in REPORT_FOLDERS:
        for path in sorted((reports_folder / folder).glob('*')) if (reports_folder / folder).is_dir() else []:
            if path.is_file() and f'{folder}/{path.name}' not in made:
                path.unlink()
                removed += 1
    return removed


def make_reports(records, exploratory: list, made_at: str) -> Counter:
    """Make every report of one game again from its records; write each file whose bytes differ; delete each
    report no longer made.

    records: the game's GameRecords, with its second OV-1 series (ledger_lines, blocked).
    exploratory: the lines of the exploratory series.  made_at: the local time of making, for the side file,
    for example '2026-12-01 20:10'.
    Returns the counts {'report files': written, 'reports removed': removed}.
    """
    game_id, last_draw = records.game_id, records.results.last_draw
    counts = Counter()
    writer = printouts.ReportWriter(records.tree_root, game_id, made_at)
    made = set()

    def write(name: str, content: str) -> None:
        """Write one report if its bytes differ, and note that this run made it."""
        made.add(name)
        counts['report files'] += writer.write(name, content)

    league = printouts.LeagueTable(records)
    lowest = min((state.first_target for state in records.workable), default=last_draw + 1)
    for draw in range(lowest, last_draw + 1):
        if league.add_draw(draw):
            for name, content in zip(printouts.league_names(game_id, draw), league.render(draw)):
                write(name, content)
    made_before_result = sorted({target for state in records.workable for target, facts in state.targets.items()
                                 if not facts.result_on_file})
    for draw in made_before_result:
        for name, content in zip(printouts.next_draw_names(game_id, draw),
                                 printouts.next_draw_report(records, draw)):
            write(name, content)
    for name, content in zip(printouts.ov1_names(game_id, 'exploratory'),
                             printouts.exploratory_report(records, exploratory)):
        write(name, content)
    for name, content in zip(printouts.ov1_names(game_id, 'prevailing'), printouts.prevailing_report(records)):
        write(name, content)
    writer.write(printouts.README_NAME, printouts.readme_text(game_id))
    counts['reports removed'] = remove_reports_no_longer_made(writer.root, made)
    writer.tidy_times()
    return counts


def run_reports(tree_root: Path, games, *, now=None, say=print) -> int:
    """Run_Reports.bat: make the reports of each game asked for from its stored science, without a research job.

    tree_root: the tree's folder.  games: for example ('POWERBALL', 'OZLOTTO').
    now: the clock (a test passes its own).  say: prints one line.
    Returns EXIT_DONE, EXIT_INCOMPLETE or EXIT_REFUSED (see above). A refused game is named with the reason and
    what to do; the other games are still made.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    started = now().astimezone().strftime('%Y-%m-%d %H:%M')
    try:
        settings = enter_tree(Path(tree_root))
        say(f'REPORTS - START - {started} - the {settings.role} tree at {settings.tree_root}')
        with tree_lock(settings.tree_root, 'reports', started):
            made, refused = 0, 0
            for game_id in games:
                try:
                    records, exploratory = load_game(settings.tree_root, game_id)
                except InputsRefused as refusal:
                    refused += 1
                    say(f'{game_id}: REFUSED: {refusal}')
                    continue
                records.role = settings.role
                counts = make_reports(records, exploratory, started)
                made += 1
                say(f'{game_id}: reports made through draw {records.results.last_draw}: '
                    f'{counts["report files"]} report files written, {counts["reports removed"]} removed')
    except (SettingsRefused, LaunchRefused) as refusal:
        say(f'REFUSED: {refusal}')
        say('REPORTS - END - refused; nothing was written.')
        return EXIT_REFUSED
    say(f'REPORTS - END - {now().astimezone().strftime("%Y-%m-%d %H:%M")} - '
        + ('every game asked for is reported.' if not refused
           else f'{refused} of {len(games)} games refused; see above.'))
    return EXIT_DONE if not refused else EXIT_INCOMPLETE if made else EXIT_REFUSED


def main(arguments, tree_root: Path) -> int:
    """The command line of Run_Reports.bat.

    arguments: what the owner typed after the command, for example ['--game', 'OZLOTTO'].
    tree_root: the tree the launcher lies in.  Returns the exit code of run_reports().
    """
    parser = argparse.ArgumentParser(prog='Run_Reports.bat', description='Make the reports from the stored science.')
    parser.add_argument('--game', default='BOTH', choices=GAMES + ('BOTH',),
                        help='the game to report (default: BOTH)')
    chosen = parser.parse_args(arguments)
    return run_reports(tree_root, GAMES if chosen.game == 'BOTH' else (chosen.game,))
