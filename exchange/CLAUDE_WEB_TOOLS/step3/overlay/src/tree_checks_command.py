"""The program behind Verify_Tree.bat, and the one an install tool starts to have a tree's software checked.

What this file is for
    Three commands, each run with a tree's own Python:
      verify   Verify_Tree.bat, in a QA or PROD tree after its Python environment was built or rebuilt
               (research/tree_verify.py).
      checks   started by the install tools in DEV, never by a launcher: the smoke cases, the forecast sample
               and the derived results of the software this program lies in, asked of a tree's data, the result
               written to a file the tool names (research/tree_checks.py).
      reports  started by an infrastructure reinstall in DEV, never by a launcher: the tree's league reports,
               next-draw reports and OV-1 print-outs made again from its lists with its own installed software.
    It is not research_command.py because that program refuses a tree whose environment has no marker, and
    writing the marker is what `verify` is for; and because `checks` may be asked of software that lies in a
    temporary folder, beside no settings file of its own.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 12.3 and 13;
    doc/Predictive_Randomness_Deployment_Design_v0_12.md sections 3.3, 6 (step 3) and 7.

Which of the project's own modules it uses
    research.settings, research.tree_checks, research.tree_verify (imported after the import folders are set).

What uses it
    Verify_Tree.bat; the install tools under deploy/ in DEV.
"""
import os
import sys
from pathlib import Path

# The folder this program's software lies in: <software>/src/tree_checks_command.py. For `verify` it is the tree.
SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
# The two folders Python imports the project's code from: the engine and the variants.
IMPORT_FOLDERS = (SOFTWARE_ROOT / 'src', SOFTWARE_ROOT / 'src' / 'methods')
# The commands, by the word that names them.
COMMANDS = ('verify', 'checks', 'reports')
# The exit code when the program refuses before a command runs.
EXIT_BAD_COMMAND = 2


def data_root_of(arguments) -> Path:
    """The tree whose Python must be the one running: for `verify` the tree this program lies in; for `checks`
    and `reports` the tree named after --data (the command itself refuses if none is named)."""
    if arguments[0] in ('checks', 'reports'):
        for position, word in enumerate(arguments[:-1]):
            if word == '--data':
                return Path(arguments[position + 1])
    return SOFTWARE_ROOT


def run_command(arguments, running_prefix: str | None = None) -> int:
    """Run the command named.

    arguments: the command word and what follows it, for example ['verify'] or ['checks', '--data', ...].
    running_prefix: the environment of the Python that is running (sys.prefix); a test passes its own.
    Returns the command's exit code.
    """
    if not arguments or arguments[0] not in COMMANDS:
        print(f'tree_checks_command.py: the first word must be one of: {", ".join(COMMANDS)}. In a tree, use '
              f'Verify_Tree.bat.')
        return EXIT_BAD_COMMAND
    sys.path[:0] = [str(folder) for folder in IMPORT_FOLDERS]
    from research.settings import SettingsRefused, read_settings
    try:
        environment_folder = read_settings(data_root_of(arguments)).venv_dir
    except SettingsRefused as refusal:
        print(f'REFUSED: {refusal}')
        return EXIT_BAD_COMMAND
    running = sys.prefix if running_prefix is None else running_prefix
    if os.path.normcase(os.path.realpath(running)) != os.path.normcase(os.path.realpath(environment_folder)):
        print(f'REFUSED: the Python running is {running}, but the tree\'s settings name {environment_folder} as its '
              f'environment. These checks are made with the tree\'s own Python and no other.')
        return EXIT_BAD_COMMAND
    if arguments[0] == 'verify':
        from research.tree_verify import main
    elif arguments[0] == 'checks':
        from research.tree_checks import main
    else:
        from research.tree_checks import reports_main as main
    return main(arguments[1:], SOFTWARE_ROOT)


if __name__ == '__main__':
    sys.exit(run_command(sys.argv[1:]))
