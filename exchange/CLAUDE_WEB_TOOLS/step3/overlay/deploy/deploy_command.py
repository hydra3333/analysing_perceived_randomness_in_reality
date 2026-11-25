"""The one program behind DEV's install launchers. In this slice: Make_Installable.bat and Check_Tree.bat.

What this file is for
    A launcher in DEV's folder starts this file with DEV's own Python and the name of a command. It puts DEV's
    code folders at the front of Python's import path, checks that this tree is DEV and that the Python running
    is DEV's own environment, prints any warning the settings give, and hands over to the command's program.
    Which tree it works in is the tree this file lies in; no path is typed or stored.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 16 (the owner's commands);
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 2 ("the install tools live in DEV and are run
    from DEV") and section 1 (the settings checks every tool makes).

Which of the project's own modules it uses
    research.settings    read_dev_view: DEV's settings and its entries for QA and PROD, every check made
    make_installable     main: the command Make_Installable
    check_tree           main: the command Check_Tree
    init_tree            main: the command Init_Tree (build step 3, slice C)
    install              main: the command Install (build step 3, slice C)
    reinstall_infra      main: the command Reinstall_Infra (build step 3, slice C)

What uses it
    Make_Installable.bat and Check_Tree.bat. The launchers of the later slices of build step 3 are added to COMMANDS as they arrive.
"""
import os
import sys
from pathlib import Path

# The tree this program lies in: <tree>/deploy/deploy_command.py.
TREE_ROOT = Path(__file__).resolve().parents[1]
# The folders Python imports the project's code from: the engine, the variants, and the install tools.
IMPORT_FOLDERS = (TREE_ROOT / 'src', TREE_ROOT / 'src' / 'methods', TREE_ROOT / 'deploy')
# The commands, by the word the launcher gives.
COMMANDS = ('make-installable', 'check-tree', 'init-tree', 'install', 'reinstall-infra')
# The exit code when the program refuses before a command runs: an unknown command, bad settings, a foreign Python.
EXIT_BAD_COMMAND = 2


def run_command(arguments) -> int:
    """Run the command a launcher named.

    arguments: the command word and what the owner typed after the launcher's name, for example
    ['make-installable', 'E_002', 'RECUR_MEAN_ALL_V1'].  Returns the command's exit code; 2 if it refused before
    the command ran (an unknown command word; a settings file the checks refuse; a tree that is not DEV; a Python
    that is not DEV's own environment).
    """
    if not arguments or arguments[0] not in COMMANDS:
        print(f'deploy_command.py: the first word must be one of: {", ".join(COMMANDS)}. Use the launchers in '
              f'DEV\'s folder, for example Make_Installable.bat.')
        return EXIT_BAD_COMMAND
    sys.path[:0] = [str(folder) for folder in IMPORT_FOLDERS]
    from research.settings import SettingsRefused, read_dev_view
    try:
        view = read_dev_view(TREE_ROOT)
    except SettingsRefused as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    if os.path.normcase(os.path.realpath(sys.prefix)) != os.path.normcase(os.path.realpath(view.own.venv_dir)):
        print(f'REFUSED: the Python running is {sys.prefix}, but DEV\'s settings name {view.own.venv_dir} as its '
              f'environment. Start the command with the launcher in DEV\'s own folder.')
        return EXIT_BAD_COMMAND
    for warning in view.warnings:
        print(warning)
    if arguments[0] == 'check-tree':
        from check_tree import main as check_tree
        return check_tree(arguments[1:], view)
    if arguments[0] == 'init-tree':
        from init_tree import main as init_tree
        return init_tree(arguments[1:], view)
    if arguments[0] == 'install':
        from install import main as install
        return install(arguments[1:], view)
    if arguments[0] == 'reinstall-infra':
        from reinstall_infra import main as reinstall_infra
        return reinstall_infra(arguments[1:], view)
    from make_installable import main
    return main(arguments[1:], TREE_ROOT)


if __name__ == '__main__':
    sys.exit(run_command(sys.argv[1:]))
