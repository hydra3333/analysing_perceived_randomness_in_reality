"""The one program behind DEV's own launchers: Make_Installable.bat, Who_Uses.bat, and the five that touch
another tree (Create_Tree.bat, Install.bat, Retire.bat, Copy_From_PROD.bat, Restore.bat).

What this file is for
    A launcher starts this file with the tree's own Python and the name of a command. It puts this tree's code
    folders, and no other project folder, at the front of Python's import path, makes the tree's first step
    (the folder is the tree its settings say; its working folders are its own), requires that the tree is DEV,
    and hands over to the command. Which tree it works in is the tree this file lies in.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 3.1 rule 1 and section 6 (the commands that
    exist in DEV only).

Which of the project's own modules it uses
    research.tree_lock    enter_tree: the first step
    dev_tools             "make installable" and "who uses"
    install_tools         "create tree" and "install"
    tree_tools            "retire", "copy from PROD" and "restore"

What uses it
    Make_Installable.bat, Who_Uses.bat, Create_Tree.bat, Install.bat, Retire.bat, Copy_From_PROD.bat and
    Restore.bat.
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
COMMANDS = ('make_installable', 'who_uses', 'create_tree', 'install', 'retire', 'copy_from_prod', 'restore')
# The exit code when the program refuses before a command runs, or a command refuses or fails.
EXIT_BAD_COMMAND = 2
# How each of the commands that touch another tree is typed.
USAGE = {'create_tree': 'Create_Tree.bat QA   or   Create_Tree.bat PROD',
         'install': 'Install.bat QA [--show]   or   Install.bat PROD [--show]',
         'retire': 'Retire.bat family/variant the reason in a few words',
         'copy_from_prod': 'Copy_From_PROD.bat software|data|both QA   or   Copy_From_PROD.bat data DEV',
         'restore': 'Restore.bat QA|PROD backup_file.zip'}


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
    if arguments[0] != 'make_installable':
        return across_trees(settings, arguments[0], arguments[1:])
    try:
        return dev_tools.make_installable(settings, arguments[1:], datetime.now().astimezone())
    except LaunchRefused as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND


def across_trees(settings, command: str, typed: list) -> int:
    """Run one of the five commands that touch another tree.

    settings: DEV's settings.  command: the command word.  typed: what the owner typed after the launcher's
    name, for example ['QA', '--show'].
    Returns the command's exit code; EXIT_BAD_COMMAND if it refused before changing anything (REFUSED: ...) or
    failed after it began (the message, in capitals, says what state things are in and what to do).
    """
    import install_tools
    import tree_tools
    from research.settings import SettingsRefused
    from research.tree_lock import LaunchRefused
    from tree_parts import CommandFailed, CommandRefused
    moment = datetime.now().astimezone()
    words = [word for word in typed if word != '--show']
    try:
        if command == 'create_tree' and len(typed) == 1:
            return install_tools.create_tree(settings, typed[0].upper(), moment=moment)
        if command == 'install' and len(words) == 1 and len(typed) <= 2:
            return install_tools.install(settings, words[0].upper(), show=len(typed) == 2, moment=moment)
        if command == 'retire' and len(typed) >= 2:
            return tree_tools.retire(settings, typed[0].replace('\\', '/'), ' '.join(typed[1:]), moment=moment)
        if command == 'copy_from_prod' and len(typed) == 2:
            return tree_tools.copy_from_prod(settings, typed[0].lower(), typed[1].upper(), moment=moment)
        if command == 'restore' and len(typed) == 2:
            return tree_tools.restore(settings, typed[0].upper(), typed[1], moment=moment)
    except (CommandRefused, SettingsRefused, LaunchRefused) as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    except CommandFailed as failure:
        print(str(failure))
        return EXIT_BAD_COMMAND
    print('REFUSED: the command was not typed as it must be. ' + USAGE[command])
    return EXIT_BAD_COMMAND


if __name__ == '__main__':
    sys.exit(run_command(sys.argv[1:]))
