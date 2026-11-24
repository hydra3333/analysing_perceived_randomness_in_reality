"""Withdrawing a defective variant: what Withdraw_Variant.bat runs.

What this file is for
    A withdrawal is the owner's explicit decision that a variant is wrong and stops. This program shows the
    variant, the last draw on file and the draw the withdrawal will take effect from (the last draw on file
    plus one), asks for one typed confirmation, and then rewrites the variant's status file. That is the whole
    mechanism: nothing is written into any list, nothing is removed, and no command reverses it. From before the
    draw is shown until the status file is written it holds the tree's job lock and the updater's own lock.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 11 (and 3.5: who writes the status file).

Which of the project's own modules it uses
    research.settings          read_settings: the tree's role and root
    research.job_lock          the job lock, the updater's lock, the orphan-marker check
    research.variant_folders   read_variant: the variant and the games it supports
    research.status_file       read_status, with_withdrawal, write_status, discard_unfinished_writes
    research.reader            results_on_file, results_paths: the last draw on file

What uses it
    src/research_command.py (the program behind Withdraw_Variant.bat), and the engine's tests.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path

from research.job_lock import (RECORDS_FOLDER, LaunchRefused, check_no_orphan_marker, check_working_folders,
                               job_lock, updater_lock)
from research.reader import ResultsRefused, results_on_file, results_paths
from research.settings import SettingsRefused, read_settings
from research.status_file import (STATUS_FILE_NAME, StatusRefused, discard_unfinished_writes, read_status,
                                  with_withdrawal, write_status)
from research.variant_folders import VariantRefused, read_variant

# The games a withdrawal can name; BOTH means each of them.
GAMES = ('POWERBALL', 'OZLOTTO')
# Where a tree keeps its variants, from the tree root.
METHODS_FOLDER = 'src/methods'
# The word the owner types to confirm. A withdrawal is one-way, so a plain "y" is not enough.
CONFIRMATION_WORD = 'WITHDRAW'
# The tree's log of installs, replacements and withdrawals (deployment design section 2).
TREE_LOG_NAME = 'INSTALL_LOG.jsonl'
# The exit codes: done; stopped by a fault part-way (each status file is whole, old or new); refused or not
# confirmed (nothing written).
EXIT_DONE, EXIT_STOPPED, EXIT_NOTHING_WRITTEN = 0, 1, 2


class WithdrawalRefused(ValueError):
    """The withdrawal cannot be made. The message says what was found; nothing was written."""


def results_last_checked(tree_root: Path, game_id: str) -> str:
    """When a game's results were last checked or updated, from the last row of their version ledger, for
    example '2026-12-01T09:40:12Z (UPDATE)'. For the owner's eye only; no rule reads it."""
    rows = list(csv.reader(io.StringIO(results_paths(tree_root, game_id)[1].read_text(encoding='utf-8'))))
    last = dict(zip(rows[0], rows[-1]))
    return f'{last.get("utc", "?")} ({last.get("action", "?")})'


def plan_withdrawal(tree_root: Path, names, games, reason: str, stamp: str) -> list:
    """Work out exactly what a withdrawal would write, and refuse if any part of it cannot be made.

    names: (family, variant) pairs.  games: the games named.  reason: the owner's reason.  stamp: the time, as
    text, for the status file's note.
    Returns one entry for each variant: {'variant': the Variant, 'new_statuses': its {game: GameStatus} as they
    will be written, 'effective': {game: the draw the withdrawal takes effect from}, 'last_on_file': {game: the
    last draw}}.
    Refuses (WithdrawalRefused, or the status file's or the results' own refusal), before anything is shown or
    written: no reason, or one that is not a line of plain text; an unknown variant; a variant that does not
    support a named game; a variant already withdrawn in a named game.
    """
    if not reason.strip():
        raise WithdrawalRefused('--reason is empty. Say in a few words why the variant is wrong.')
    last_on_file = {game_id: results_on_file(tree_root, game_id).last_draw for game_id in games}
    plan = []
    for family, name in names:
        variant = read_variant(Path(tree_root) / METHODS_FOLDER, family, name)
        supported = [game_id for game_id in GAMES if variant.supports(game_id)]
        statuses = read_status(variant.folder / STATUS_FILE_NAME, supported)
        for game_id in games:
            if game_id not in supported:
                raise WithdrawalRefused(f'{variant.identity} does not support {game_id}. Name the game it runs in.')
            if statuses[game_id].withdrawn_from is not None:
                raise WithdrawalRefused(f'{variant.identity} is already withdrawn in {game_id}, from draw '
                                        f'{statuses[game_id].withdrawn_from}. A withdrawal is set once. (If an '
                                        f'earlier command for several variants was interrupted, run it again '
                                        f'without this one.)')
            statuses[game_id] = with_withdrawal(statuses[game_id], last_on_file[game_id] + 1, reason,
                                                f'{stamp}; results on file through {last_on_file[game_id]}')
        plan.append({'variant': variant, 'new_statuses': statuses,
                     'effective': {game_id: last_on_file[game_id] + 1 for game_id in games},
                     'last_on_file': dict(last_on_file)})
    return plan


def withdraw(tree_root: Path, names, games, reason: str, *, ask=input, say=print, now=None) -> int:
    """Withdraw one or more variants in a tree, after one typed confirmation.

    tree_root: the tree.  names: (family, variant) pairs.  games: the games.  reason: the owner's reason.
    ask: asks the owner a question and returns what he typed (a test passes its own).  say: prints one line.
    now: gives the present time (UTC); a test passes a fixed one.
    Returns EXIT_DONE if the status files were written; EXIT_NOTHING_WRITTEN if it was refused or not confirmed;
    EXIT_STOPPED if a file operation failed part-way (each status file is then the old one or the new one).
    """
    now = now or (lambda: datetime.now(timezone.utc))
    stamp = now().astimezone().strftime('%Y-%m-%d %H:%M')
    try:
        settings = read_settings(Path(tree_root))
        tree_root = settings.tree_root
        say(f'WITHDRAW A VARIANT - START - {stamp} - the {settings.role} tree at {tree_root}')
        check_no_orphan_marker(tree_root)
        check_working_folders(tree_root)
        with job_lock(tree_root, 'withdrawal', stamp), updater_lock(tree_root, 'withdrawal', stamp):
            for leftover in discard_unfinished_writes(tree_root):
                say(f'  An earlier status write was interrupted before it changed anything; its unfinished copy was '
                    f'removed ({leftover}).')
            plan = plan_withdrawal(tree_root, names, games, reason, stamp)
            for entry in plan:
                for game_id in games:
                    say(f'  {entry["variant"].identity} in {game_id}: last draw on file '
                        f'{entry["last_on_file"][game_id]} (results last checked '
                        f'{results_last_checked(tree_root, game_id)}); the withdrawal takes effect from draw '
                        f'{entry["effective"][game_id]}.')
            say(f'  Reason: {reason}')
            say('  The effective draw is fixed from the results on file, not from the calendar. If a draw has been '
                'made but its result is not yet on file, the withdrawal takes effect at that draw: consider '
                'running Run_Research.bat first.')
            say('  From that draw the variant is not forecast, never scored (also not for a forecast it already '
                'holds for that draw) and not in the prevailing OV-1. Nothing is removed. No command reverses it.')
            if ask(f'  Type {CONFIRMATION_WORD} to confirm, anything else to leave everything as it is: ') \
                    != CONFIRMATION_WORD:
                say('WITHDRAW A VARIANT - END - not confirmed; nothing was written.')
                return EXIT_NOTHING_WRITTEN
            for game_id in games:
                if results_on_file(tree_root, game_id).last_draw != plan[0]['last_on_file'][game_id]:
                    raise WithdrawalRefused(f'the last {game_id} draw on file is no longer the one shown. Nothing '
                                            f'was written; run the command again.')
            for entry in plan:
                variant = entry['variant']
                write_status(variant.folder / STATUS_FILE_NAME, variant.family, variant.variant,
                             entry['new_statuses'])
                say(f'  written: {variant.folder / STATUS_FILE_NAME}')
            log_withdrawal(tree_root, settings.role, plan, games, reason, now)
    except (SettingsRefused, LaunchRefused, VariantRefused, StatusRefused, ResultsRefused,
            WithdrawalRefused) as refusal:
        say(f'REFUSED: {refusal}')
        say('WITHDRAW A VARIANT - END - refused; no status file was changed by this command.')
        return EXIT_NOTHING_WRITTEN
    except OSError as failure:
        say(f'STOPPED: a file could not be written or read: {failure}')
        say('WITHDRAW A VARIANT - END - stopped by a fault. No status file is half-written: each is the old one or '
            'the new one, whole. Run the command again; it names any variant that is already withdrawn.')
        return EXIT_STOPPED
    say(f'WITHDRAW A VARIANT - END - {len(plan)} variant(s) withdrawn. The next Run_Research.bat honours it.')
    return EXIT_DONE


def log_withdrawal(tree_root: Path, role: str, plan: list, games, reason: str, now) -> None:
    """Add one line to the tree's log saying what was withdrawn, from which draws, why and when."""
    record = {'operation': 'WITHDRAWAL', 'time': now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'role': role, 'tree_root': str(tree_root), 'reason': reason,
              'variants': [{'variant': entry['variant'].identity,
                            'withdrawn_from_draw': {game_id: entry['effective'][game_id] for game_id in games}}
                           for entry in plan]}
    path = Path(tree_root) / RECORDS_FOLDER / TREE_LOG_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a', encoding='ascii', newline='\n') as stream:
        stream.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + '\n')


def main(arguments, tree_root: Path) -> int:
    """The command line of Withdraw_Variant.bat.

    arguments: for example ['E_002', 'RECUR_MEAN_ALL_V1', '--game', 'POWERBALL', '--reason', 'the gap table was
    built from the wrong column'].  tree_root: the tree the launcher lies in.  Returns the exit code.
    """
    parser = argparse.ArgumentParser(prog='Withdraw_Variant.bat',
                                     description='Withdraw a defective variant (specification 11).')
    parser.add_argument('names', nargs='+', metavar='<family> <variant>',
                        help='the variant, as two words; several variants may follow one another')
    parser.add_argument('--game', required=True, choices=GAMES + ('BOTH',))
    parser.add_argument('--reason', required=True, help='why the variant is wrong, in a few words')
    chosen = parser.parse_args(arguments)
    if len(chosen.names) % 2:
        parser.error('give each variant as two words: <family> <variant>, for example E_002 RECUR_MEAN_ALL_V1')
    pairs = list(zip(chosen.names[0::2], chosen.names[1::2]))
    return withdraw(tree_root, pairs, GAMES if chosen.game == 'BOTH' else (chosen.game,), chosen.reason)
