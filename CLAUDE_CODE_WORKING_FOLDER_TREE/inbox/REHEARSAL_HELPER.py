"""The small steps the rehearsal tasks T029 to T031 share, in the scratch folder on D: only.

What this file is for
    The local runner rehearses the simple scheme's commands on the owner's PC, in scratch trees under
    D:\\DELETE_ME\\ (rulebook v0.8 section 2A). A few steps around those commands are not commands of the system:
    checking that the scratch folder is an ordinary folder, copying DEV's software into a scratch tree, writing a
    scratch tree's settings file, writing invented results, running the test suite with its temporary folders
    inside the scratch folder, planting a small change in a file, and naming a backup file. They are here, once,
    so that each task file can name them in one line. This program never runs a command of the system, never
    touches the network, and writes only under D:\\DELETE_ME\\ (it refuses any other place it is given).

    Commands (the first word after the program's name):
      check-scratch <task folder>            the scratch folder is an ordinary folder on D:; the task folder is new
      copy-dev <repository> <list> <tree> [--families E_001,E_002]
                                             copy the files the list names (git ls-files of a_p_r_i_r_DEV) into a
                                             new scratch tree, keeping only the method families named, if any
      settings <tree> <role>                 write a scratch tree's ENVIRONMENT.ini: the three trees and their
                                             backup folders all beside it in its scratch folder
      invented <tree> <draws>                write invented results for both games (run with the tree's Python)
      run-tests <tree> <temporary folder>    run the tree's test suite, temporary files inside the scratch folder
                                             (run with the tree's Python)
      plant-edit <file>                      add one comment line to a file of a scratch tree
      one-backup <folder> <ending>           print the name of the one backup file in a folder with that ending
      comparison-trees <repository> <real DEV tree> <list> <folder>
                                             for TASK_T031: a new-engine tree (DEV's software from the list, and
                                             the real DEV tree's source_data and results\\research, copied by
                                             reading) and a frozen-engine tree (the repository's top level, and the
                                             same source_data), each with its settings file; then check that the
                                             results copied were made by the engine copied (run with DEV's Python)

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 12 (the rehearsal), under the runner's rulebook
    v0.8 section 2A; decision log entries 365 and 366.

Which of the project's own modules it uses
    research_fixtures (from the scratch tree's tests folder)  write_results: invented results, for "invented"
    _common.game_profiles (from the scratch tree)              get_profile: each game's first draw
    research.code_identity (from the scratch tree)             the engine's fingerprint, for "comparison-trees"

What uses it
    CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T029.md, TASK_T030.md and TASK_T031.md.
"""
import argparse
import hashlib
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# The one folder this program writes in, and its drive.
SCRATCH_ROOT = Path(r'D:\DELETE_ME')
# The folder of the living system inside the repository, as `git ls-files` names its files.
DEV_PREFIX = 'a_p_r_i_r_DEV/'
# The three roles, and the folder under a task folder where every scratch tree's backups go.
ROLES = ('DEV', 'QA', 'PROD')
BACKUPS_FOLDER = 'backups'
# The pattern of the test files of the living system.
TEST_PATTERN = 'test_research_*.py'
# What a frozen-engine tree needs of the repository's top level (as deploy/compare_with_frozen.py FROZEN_PARTS),
# and the two folders of the real DEV tree a comparison copies by reading.
FROZEN_PARTS = ('src/research', 'src/evaluation', 'src/methods', 'src/research_command.py',
                'deploy/INFRA_MANIFEST.ini', 'Run_Research.bat', 'Withdraw_Variant.bat')
DEV_DATA = ('source_data', 'results/research')


class Refused(Exception):
    """A step that would leave the scratch folder, or find what it should not. The message says which."""


def inside_scratch(path: Path) -> Path:
    """The path made absolute, refused (Refused) unless it lies under D:\\DELETE_ME\\, for example
    inside_scratch(Path(r'D:\\DELETE_ME\\a_p_r_i_r\\T029\\s_DEV')) returns that path."""
    path = Path(os.path.abspath(path))
    root = os.path.normcase(str(SCRATCH_ROOT)) + os.sep
    if not os.path.normcase(str(path)).startswith(root):
        raise Refused(f'{path} is not under {SCRATCH_ROOT}: this program writes nowhere else.')
    return path


def check_scratch(task_folder: Path) -> None:
    """Check that D:\\DELETE_ME is an ordinary folder on drive D:, that no folder between it and the task folder is
    a link or a junction, that the task folder would lie where its name says, and that it does not exist yet."""
    task_folder = inside_scratch(task_folder)
    real = Path(os.path.realpath(SCRATCH_ROOT))
    print(f'real path of the scratch folder: {real}')
    if os.path.normcase(str(real)) != os.path.normcase(str(SCRATCH_ROOT)) or not SCRATCH_ROOT.is_dir():
        raise Refused(f'{SCRATCH_ROOT} is not an ordinary folder on drive D: (its real path is {real}).')
    odd = [str(folder) for folder in [task_folder, *task_folder.parents]
           if folder.exists() and (folder.is_symlink() or os.path.realpath(folder) != str(folder))]
    print(f'folders on the way that are links or junctions: {odd}')
    if odd:
        raise Refused(f'these folders are not ordinary folders: {odd}')
    if task_folder.exists():
        raise Refused(f'{task_folder} exists already. This task makes it new: nothing was written.')
    print(f'task folder: {task_folder} (not there yet)')
    print('SCRATCH CHECK PASS')


def copy_dev(repository: Path, file_list: Path, tree: Path, families: str | None) -> None:
    """Copy the files of a_p_r_i_r_DEV that the list names (one path a line, as `git ls-files a_p_r_i_r_DEV`
    prints them) from the repository into a new scratch tree, then read every copy back against its source.
    families: None, or the method families to keep, for example 'E_001,E_002' (the others are not copied)."""
    tree = inside_scratch(tree)
    keep = set(families.split(',')) if families else None
    names = [line.strip() for line in file_list.read_text(encoding='utf-8').splitlines() if line.strip()]
    if not names or not all(name.startswith(DEV_PREFIX) for name in names):
        raise Refused(f'{file_list} does not list files of {DEV_PREFIX} only.')
    copied = 0
    for name in names:
        relative = name[len(DEV_PREFIX):]
        parts = relative.split('/')
        if keep is not None and parts[:2] == ['src', 'methods'] and parts[2].startswith('E_') and parts[2] not in keep:
            continue
        source, target = repository / name, tree / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if target.read_bytes() != source.read_bytes():
            raise Refused(f'{target} does not read back as {source}.')
        copied += 1
    print(f'files listed: {len(names)}; copied and read back: {copied}; families kept: '
          f'{sorted(keep) if keep else "all"}')
    print('COPY PASS')


def write_settings(tree: Path, role: str) -> None:
    """Write a scratch tree's ENVIRONMENT.ini (CRLF): its role, and for each role a tree folder named
    <stem>_<ROLE> and a backup folder <task folder>\\backups\\<ROLE>, all in the scratch tree's own folder.
    For example the tree D:\\DELETE_ME\\a_p_r_i_r\\T030\\s_DEV gives s_QA and s_PROD beside it."""
    tree = inside_scratch(tree)
    if role not in ROLES or not tree.name.endswith('_' + role):
        raise Refused(f'{tree} and the role {role}: a scratch tree\'s folder name ends with _ and its role.')
    stem, folder = tree.name[:-len(role) - 1], tree.parent
    lines = ['[environment]', f'role = {role}']
    for name in ROLES:
        lines += [f'[{name}]', f'tree_root = {inside_scratch(folder / f"{stem}_{name}")}',
                  f'backup_root = {inside_scratch(folder / BACKUPS_FOLDER / name)}']
    (tree / 'ENVIRONMENT.ini').write_bytes(('\r\n'.join(lines) + '\r\n').encode('ascii'))
    print('\n'.join(lines))
    print('every path above lies under ' + str(SCRATCH_ROOT))
    print('SETTINGS PASS')


def write_invented(tree: Path, draws: int) -> None:
    """Write invented results (a seeded generator; never a real draw) for both games into a scratch tree: from
    each game's first draw to `draws` draws after it, with their version ledgers. Run with the tree's Python."""
    tree = inside_scratch(tree)
    sys.path[:0] = [str(tree / 'src'), str(tree / 'src' / 'methods'), str(tree / 'tests')]
    import research_fixtures
    from _common.game_profiles import get_profile
    for game_id in ('POWERBALL', 'OZLOTTO'):
        last = get_profile(game_id).first_draw + draws
        research_fixtures.write_results(tree, game_id, last)
        print(f'{game_id}: invented results through draw {last}')
    print('INVENTED RESULTS WRITTEN')


def run_tests(tree: Path, temporary: Path) -> int:
    """Run a scratch tree's whole test suite, with every temporary file the tests make inside the given folder
    of the scratch folder. Run with the tree's Python. Returns 0 if every test passed, else 1."""
    tree, temporary = inside_scratch(tree), inside_scratch(temporary)
    temporary.mkdir(parents=True, exist_ok=True)
    os.environ['TMP'] = os.environ['TEMP'] = str(temporary)
    tempfile.tempdir = str(temporary)
    sys.path[:0] = [str(tree / 'src'), str(tree / 'src' / 'methods'), str(tree / 'tests')]
    os.chdir(temporary)
    print(f'Python: {sys.executable}; temporary folder: {tempfile.gettempdir()}')
    tests = str(tree / 'tests')
    suite = unittest.defaultTestLoader.discover(tests, pattern=TEST_PATTERN, top_level_dir=tests)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
    print(f'TESTS RUN {result.testsRun}; FAILURES {len(result.failures)}; ERRORS {len(result.errors)}; '
          f'SKIPPED {len(result.skipped)}')
    for test, why in result.skipped:
        print(f'SKIPPED: {test.id()}: {why}')
    return 0 if result.wasSuccessful() else 1


def plant_edit(path: Path) -> None:
    """Add one comment line (CRLF) to a Python file of a scratch tree, so that its bytes change; print its SHA-256
    before and after."""
    path = inside_scratch(path)
    before = path.read_bytes()
    path.write_bytes(before + b'# changed for the rehearsal\r\n')
    print(f'{path}: SHA-256 {hashlib.sha256(before).hexdigest()[:16]}... -> '
          f'{hashlib.sha256(path.read_bytes()).hexdigest()[:16]}...')
    print('EDIT PLANTED')


def one_backup(folder: Path, ending: str) -> int:
    """Print the name of the one file in a backup folder whose name ends as given (for example '_on_demand.zip').
    Returns 0, or 1 (printing what was found) if there is not exactly one."""
    folder = inside_scratch(folder)
    found = sorted(path.name for path in folder.iterdir() if path.name.endswith(ending))
    if len(found) != 1:
        print(f'NOT EXACTLY ONE: {found}', file=sys.stderr)
        return 1
    print(found[0])
    return 0


def copy_folder(source: Path, target: Path) -> int:
    """Copy a folder by reading (Python's caches left out) into the scratch folder, reading every copy back
    against its source; return the files copied. Refuses (Refused) a source that is absent or empty, a copy that
    does not read back as its source, or a target outside the scratch folder."""
    target = inside_scratch(target)
    names = [path for path in sorted(source.rglob('*')) if path.is_file() and '__pycache__' not in path.parts]
    if not names:
        raise Refused(f'{source} is absent or empty: there is nothing to copy.')
    for path in names:
        copy = target / path.relative_to(source)
        copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, copy)
        if copy.read_bytes() != path.read_bytes():
            raise Refused(f'{copy} does not read back as {path}.')
    return len(names)


def comparison_trees(repository: Path, dev: Path, file_list: Path, folder: Path) -> None:
    """Make the two trees of TASK_T031 in a new folder of the scratch folder: new_DEV (DEV's software from the list,
    and the real DEV tree's source_data and results\\research, copied by reading) and frozen_DEV (the repository's
    top level parts the frozen engine needs, and the same source_data), each with its own settings file. Then
    check, with the new tree's own engine code, that the results copied were made by the engine copied. Nothing of
    the real DEV tree is written; its ENVIRONMENT.ini is not read."""
    folder = inside_scratch(folder)
    new, frozen = folder / 'new_DEV', folder / 'frozen_DEV'
    copy_dev(repository, file_list, new, None)
    for part in DEV_DATA:
        print(f'{part}: {copy_folder(dev / part, new / part)} files copied by reading from the real DEV tree')
    for part in FROZEN_PARTS:
        source = repository / part
        if source.is_dir():
            copy_folder(source, frozen / part)
        else:
            (frozen / part).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, inside_scratch(frozen / part))
            if (frozen / part).read_bytes() != source.read_bytes():
                raise Refused(f'{frozen / part} does not read back as {source}.')
    print(f'source_data: {copy_folder(dev / "source_data", frozen / "source_data")} files copied into the frozen tree')
    (frozen / 'ENVIRONMENT.ini').write_bytes((f'[environment]\r\nrole = DEV\r\ntree_root = {frozen}\r\n'
                                              f'venv_dir = {frozen / ".venv"}\r\n').encode('ascii'))
    lines = ['[environment]', 'role = DEV']
    for name, place in (('DEV', new), ('QA', folder / 'none_QA'), ('PROD', folder / 'none_PROD')):
        lines += [f'[{name}]', f'tree_root = {inside_scratch(place)}',
                  f'backup_root = {inside_scratch(folder / BACKUPS_FOLDER / name)}']
    (new / 'ENVIRONMENT.ini').write_bytes(('\r\n'.join(lines) + '\r\n').encode('ascii'))
    sys.path[:0] = [str(new / 'src'), str(new / 'src' / 'methods')]
    from research import code_identity
    engine, stored = code_identity.infrastructure_fingerprint(new), code_identity.stored_fingerprint(new)
    print(f'engine copied: {engine[:16]}...; engine the copied results were made with: {(stored or "none")[:16]}...')
    if engine != stored:
        raise Refused('the results copied from the real DEV tree were not made by the engine of this commit.')
    print('COMPARISON TREES PASS')


def main(arguments) -> int:
    """The command line. Returns the exit code: 0 done, 1 not as expected, 2 refused."""
    parser = argparse.ArgumentParser(prog='REHEARSAL_HELPER.py', description=__doc__.split('\n')[0])
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check-scratch').add_argument('task_folder', type=Path)
    copy = commands.add_parser('copy-dev')
    for name in ('repository', 'file_list', 'tree'):
        copy.add_argument(name, type=Path)
    copy.add_argument('--families', default=None)
    settings = commands.add_parser('settings')
    settings.add_argument('tree', type=Path)
    settings.add_argument('role')
    invented = commands.add_parser('invented')
    invented.add_argument('tree', type=Path)
    invented.add_argument('draws', type=int)
    tests = commands.add_parser('run-tests')
    tests.add_argument('tree', type=Path)
    tests.add_argument('temporary', type=Path)
    commands.add_parser('plant-edit').add_argument('file', type=Path)
    backup = commands.add_parser('one-backup')
    backup.add_argument('folder', type=Path)
    backup.add_argument('ending')
    trees = commands.add_parser('comparison-trees')
    for name in ('repository', 'dev', 'file_list', 'folder'):
        trees.add_argument(name, type=Path)
    chosen = parser.parse_args(arguments)
    try:
        if chosen.command == 'check-scratch':
            check_scratch(chosen.task_folder)
        elif chosen.command == 'copy-dev':
            copy_dev(chosen.repository, chosen.file_list, chosen.tree, chosen.families)
        elif chosen.command == 'settings':
            write_settings(chosen.tree, chosen.role)
        elif chosen.command == 'invented':
            write_invented(chosen.tree, chosen.draws)
        elif chosen.command == 'run-tests':
            return run_tests(chosen.tree, chosen.temporary)
        elif chosen.command == 'plant-edit':
            plant_edit(chosen.file)
        elif chosen.command == 'comparison-trees':
            comparison_trees(chosen.repository, chosen.dev, chosen.file_list, chosen.folder)
        else:
            return one_backup(chosen.folder, chosen.ending)
    except Refused as refusal:
        print(f'STOP: {refusal}')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
