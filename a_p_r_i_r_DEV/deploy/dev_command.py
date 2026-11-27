"""The one program behind DEV's own launchers: Make_Installable.bat and Who_Uses.bat.

What this file is for
    A launcher starts this file with the tree's own Python and the name of a command. It puts this tree's code
    folders, and no other project folder, at the front of Python's import path, makes the tree's first step
    (the folder is the tree its settings say; its working folders are its own), requires that the tree is DEV,
    and hands over to the command. Which tree it works in is the tree this file lies in.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 3.1 rule 1 and section 6 (the commands that
    exist in DEV only; those that touch another tree arrive with the second part of step 4).

Which of the project's own modules it uses
    research.tree_lock    enter_tree: the first step
    dev_tools             the commands themselves

What uses it
    Make_Installable.bat and Who_Uses.bat.
"""
import os
import sys
from datetime import datetime
from pathlib import Path

# The tree this program lies in: <tree>/deploy/dev_command.py.
TREE_ROOT = Path(__file__).resolve().parents[1]
# The folders Python imports the project's code from: the engine, the methods, and DEV's tools.
IMPORT_FOLDERS = (TREE_ROOT / 'src', TREE_ROOT / 'src' / 'methods', TREE_ROOT / 'deploy')
# The commands, by the word the launcher gives.
COMMANDS = ('make_installable', 'who_uses')
# The exit code when the program refuses before a command runs.
EXIT_BAD_COMMAND = 2


def run_command(arguments) -> int:
    """Run the command a launcher named.

    arguments: the command word and what the owner typed after the launcher's name, for example
    ['make_installable', 'ALL', 'INFRA'].  Returns the command's exit code, or EXIT_BAD_COMMAND.
    """
    if not arguments or arguments[0] not in COMMANDS:
        print(f'dev_command.py: the first word must be one of: {", ".join(COMMANDS)}. Use the launchers in the '
              f'tree\'s folder, for example Make_Installable.bat.')
        return EXIT_BAD_COMMAND
    sys.path[:0] = [str(folder) for folder in IMPORT_FOLDERS]
    from research.settings import SettingsRefused
    from research.tree_lock import LaunchRefused, enter_tree
    try:
        settings = enter_tree(TREE_ROOT, must_be='DEV')
    except (SettingsRefused, LaunchRefused) as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    if os.path.normcase(os.path.realpath(sys.prefix)) != os.path.normcase(os.path.realpath(settings.venv_dir)):
        print(f'REFUSED: the Python running is {sys.prefix}, but this tree\'s own environment is '
              f'{settings.venv_dir}. Start the command with the launcher in the tree\'s own folder.')
        return EXIT_BAD_COMMAND
    import dev_tools
    if arguments[0] == 'who_uses':
        if len(arguments) != 2:
            print('Give one helper file, for example: Who_Uses.bat _shared\\recurrence_gaps_v1.py')
            return EXIT_BAD_COMMAND
        return dev_tools.who_uses(settings, arguments[1])
    try:
        return dev_tools.make_installable(settings, arguments[1:], datetime.now().astimezone())
    except LaunchRefused as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND


if __name__ == '__main__':
    sys.exit(run_command(sys.argv[1:]))
