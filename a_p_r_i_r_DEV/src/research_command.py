"""The one program behind the research system's launchers in a tree (today: Run_Research.bat).

What this file is for
    A launcher starts this file with the tree's own Python and the name of a command. It puts this tree's two
    code folders, and no other project folder, at the front of Python's import path, and hands over to the
    command's own program. Which tree it works in is the tree this file lies in; no path is typed or stored.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 3.1 rule 1 (a command works on the folder its
    own launcher lies in) and section 6 (the commands; the others arrive with step 4 of the work order).

    It also checks that the Python running it is the tree's own environment, the one the settings file names.

Which of the project's own modules it uses
    research.settings       read_settings: the tree's environment folder
    research.research_job   main: the research job

What uses it
    Run_Research.bat.
"""
import os
import sys
from pathlib import Path

# The tree this program lies in: <tree>/src/research_command.py.
TREE_ROOT = Path(__file__).resolve().parents[1]
# The two folders Python imports the project's code from: the engine (research, evaluation) and the methods.
IMPORT_FOLDERS = (TREE_ROOT / 'src', TREE_ROOT / 'src' / 'methods')
# The commands, by the word the launcher gives.
COMMANDS = ('research',)
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
    from research.settings import SettingsRefused, read_settings
    try:
        environment_folder = read_settings(TREE_ROOT).venv_dir
    except SettingsRefused as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    if os.path.normcase(os.path.realpath(sys.prefix)) != os.path.normcase(os.path.realpath(environment_folder)):
        print(f'REFUSED: the Python running is {sys.prefix}, but this tree\'s settings name {environment_folder} '
              f'as its environment. Start the command with the launcher in the tree\'s own folder.')
        return EXIT_BAD_COMMAND
    from research.research_job import main
    return main(arguments[1:], TREE_ROOT)


if __name__ == '__main__':
    sys.exit(run_command(sys.argv[1:]))
