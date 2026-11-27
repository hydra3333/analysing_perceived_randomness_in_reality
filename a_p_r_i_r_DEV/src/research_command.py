"""The one program behind the launchers every tree has: Run_Research.bat, Run_Results_Updater.bat and Backup.bat.

What this file is for
    A launcher starts this file with the tree's own Python and the name of a command. It puts this tree's two
    code folders, and no other project folder, at the front of Python's import path, and hands over to the
    command's own program. Which tree it works in is the tree this file lies in; no path is typed or stored.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 3.1 rule 1 (a command works on the folder its
    own launcher lies in) and section 6 (the commands; the others arrive with step 4 of the work order).

    Before any command it makes the tree's first step (the folder is the tree its settings say; its working
    folders are its own) and checks that the Python running it is the tree's own environment.

Which of the project's own modules it uses
    research.tree_lock         enter_tree: the first step; the tree's lock, for an update or a backup by itself
    research.research_job      main: the research job
    research.backup            make_backup: a backup now
    updater.results_updater    main: the results updater

What uses it
    Run_Research.bat, Run_Results_Updater.bat and Backup.bat.
"""
import os
import sys
from datetime import datetime
from pathlib import Path

# The tree this program lies in: <tree>/src/research_command.py.
TREE_ROOT = Path(__file__).resolve().parents[1]
# The two folders Python imports the project's code from: the engine (research, evaluation) and the methods.
IMPORT_FOLDERS = (TREE_ROOT / 'src', TREE_ROOT / 'src' / 'methods')
# The commands, by the word the launcher gives.
COMMANDS = ('research', 'update', 'backup')
# The exit code when the program refuses before a command runs: an unknown command, bad settings, a foreign Python.
EXIT_BAD_COMMAND = 2


def run_command(arguments) -> int:
    """Run the command a launcher named.

    arguments: the command word and what the owner typed after the launcher's name, for example
    ['research', '--no-update'].  Returns the command's exit code.
    """
    if not arguments or arguments[0] not in COMMANDS:
        print(f'research_command.py: the first word must be one of: {", ".join(COMMANDS)}. Use the launchers in the '
              f'tree\'s folder, for example Run_Research.bat.')
        return EXIT_BAD_COMMAND
    sys.path[:0] = [str(folder) for folder in IMPORT_FOLDERS]
    from research.settings import SettingsRefused
    from research.tree_lock import LaunchRefused, enter_tree
    try:
        settings = enter_tree(TREE_ROOT)
    except (SettingsRefused, LaunchRefused) as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    if os.path.normcase(os.path.realpath(sys.prefix)) != os.path.normcase(os.path.realpath(settings.venv_dir)):
        print(f'REFUSED: the Python running is {sys.prefix}, but this tree\'s own environment is '
              f'{settings.venv_dir}. Start the command with the launcher in the tree\'s own folder.')
        return EXIT_BAD_COMMAND
    if arguments[0] == 'update':
        return update_alone(settings, arguments[1:])
    if arguments[0] == 'backup':
        return backup_alone(settings)
    from research.research_job import main
    return main(arguments[1:], TREE_ROOT)


def backup_alone(settings) -> int:
    """Make a backup of this tree now, holding the tree's lock, so that it is never taken while something is
    being written. settings: the tree's settings. Returns 0, or EXIT_BAD_COMMAND if the lock is held or the
    backup could not be made (the reason is printed)."""
    from research.backup import BackupFailed, make_backup
    from research.tree_lock import LaunchRefused, tree_lock
    moment = datetime.now().astimezone()
    try:
        with tree_lock(settings.tree_root, 'backup', moment.strftime('%Y-%m-%d %H:%M')):
            path = make_backup(settings, 'on demand', moment)
    except (LaunchRefused, BackupFailed) as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    print(f'Backup made of the {settings.role} tree at {settings.tree_root}: {path}')
    return 0


def update_alone(settings, arguments) -> int:
    """Run the results updater by itself in this tree, holding the tree's lock, so that it never changes the
    results while a research job reads them.

    settings: the tree's settings.
    arguments: what the owner typed after Run_Results_Updater.bat, for example ['--months-back', '11'].
    Returns the updater's exit code (0 done or nothing new, 1 a check failed, 2 STOP, 3 refused), or
    EXIT_BAD_COMMAND if the tree's lock is held.
    """
    from research.tree_lock import LaunchRefused, tree_lock
    from updater.results_updater import main as update
    started = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')
    print(f'RESULTS UPDATER - START - {started} - the {settings.role} tree at {settings.tree_root}')
    try:
        with tree_lock(settings.tree_root, 'results updater', started):
            code = update(arguments, settings.tree_root)
    except LaunchRefused as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    print('RESULTS UPDATER - END - ' + ('done.' if code == 0 else f'it did not finish (exit code {code}); see above. '
                                        f'The results file is as it was unless an update was reported.'))
    return code


if __name__ == '__main__':
    sys.exit(run_command(sys.argv[1:]))
