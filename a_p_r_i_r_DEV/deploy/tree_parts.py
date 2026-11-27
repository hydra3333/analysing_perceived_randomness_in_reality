"""What a tree's software and data are as files, and the steps DEV's cross-tree commands share.

What this file is for
    DEV has five commands that touch another tree: Create_Tree, Install, Retire, Copy_From_PROD and Restore
    (deploy/install_tools.py and deploy/tree_tools.py). They all need the same few things, which are here:
      - which files are a tree's infrastructure (the engine, the updater and the launchers at the tree's root)
        and which files are one method (its own files and the helper files it lists);
      - copying a file so that it is whole or absent, and telling which files differ between two trees;
      - reading another tree's own settings before touching it (rule 3), taking the locks of every tree a
        command touches, the backup made before a replacement, and starting a tree's own research job under the
        lock the command already holds.
    Nothing here decides anything about methods or results.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 3.1 rule 3, section 6 (the last paragraph: every
    command that touches another tree takes that tree's lock and checks its identity; the destination's job
    works under that same lock) and section 7 (a backup before every replacement; if it fails, nothing is
    replaced).

Which of the project's own modules it uses
    research.settings       the settings of this tree and of the others; same_places
    research.tree_lock      enter_tree, tree_lock
    research.backup         make_backup, BackupFailed
    research.code_identity  the engine's and the updater's files

What uses it
    deploy/install_tools.py, deploy/tree_tools.py and the tests.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from research import backup as backups
from research import code_identity
from research.settings import ROLES, SETTINGS_FILE_NAME, SettingsRefused, TreeSettings, same_places
from research.tree_lock import enter_tree, tree_lock

# The launchers and environment scripts every tree has at its root. They go with the infrastructure. (DEV's own
# launchers, deploy\ and tests\ stay in DEV.)
ROOT_FILES = ('Run_Research.bat', 'Run_Results_Updater.bat', 'Backup.bat', 'create_venv.bat',
              'install_upgrade_dependencies_into_venv.bat', 'activate_venv.bat', 'deactivate_venv.bat')
# Where a tree keeps its methods, its accepted results and what it computes, from the tree root.
METHODS_FOLDER = 'src/methods'
SOURCE_DATA = 'source_data'
RESEARCH_RESULTS = 'results/research'
# What a file is called while it is being copied; it is renamed to its own name when it is whole.
UNFINISHED_SUFFIX = '.writing'
# The exit codes of the cross-tree commands: done; done, but the destination's job did not finish cleanly;
# refused or failed (the message says which, and what state things are in).
EXIT_DONE, EXIT_NOT_CLEAN, EXIT_REFUSED = 0, 1, 2


class CommandRefused(Exception):
    """A cross-tree command stops before it has changed anything. The message says why and what to do."""


class CommandFailed(Exception):
    """A cross-tree command failed after it began to change things. The message says what state the tree is in
    and how to put it right."""


def files_under(folder: Path) -> list:
    """Every file under a folder, as paths from that folder with forward slashes, in order, Python's caches left
    out; [] if the folder does not exist. For example ['POWERBALL_results_master.csv', 'grabs/a.html'].
    Raises OSError if a folder under it cannot be listed, so that a copy never silently lacks part of it."""
    folder = Path(folder)
    if not folder.is_dir():
        return []

    def not_listed(fault: OSError):
        """os.walk passes over a folder it cannot list unless told otherwise: raise the fault instead."""
        raise fault

    found = []
    for current, folders, names in os.walk(folder, onerror=not_listed):
        folders[:] = sorted(name for name in folders if name != '__pycache__')
        found += [(Path(current) / name).relative_to(folder).as_posix() for name in names
                  if not name.endswith(('.pyc', '.pyo'))]
    return sorted(found)


def copy_file(source_root: Path, target_root: Path, relative: str) -> None:
    """Copy one file from a tree to the same place in another, making its folders. It is written under another
    name and renamed when whole, so that the place never holds half a file.
    For example copy_file(dev, qa, 'src/research/scoring.py')."""
    target = Path(target_root) / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    unfinished = target.with_name(target.name + UNFINISHED_SUFFIX)
    shutil.copyfile(Path(source_root) / relative, unfinished)
    os.replace(unfinished, target)


def differing(source_root: Path, target_root: Path, paths) -> list:
    """Those of the given paths (from the tree root) whose file in the target tree is missing or has other
    bytes than the source tree's file; for example ['src/research/scoring.py']."""
    found = []
    for relative in paths:
        target = Path(target_root) / relative
        if not target.is_file() or target.read_bytes() != (Path(source_root) / relative).read_bytes():
            found.append(relative)
    return found


def infrastructure_paths(tree_root: Path) -> list:
    """Every file of a tree's infrastructure, as paths from the tree root: the engine (what its fingerprint
    covers), the updater, and those of the root launchers that are there."""
    tree_root = Path(tree_root)
    return (code_identity.infrastructure_files(tree_root) + code_identity.updater_files(tree_root)
            + [name for name in ROOT_FILES if (tree_root / name).is_file()])


def method_paths(variant) -> list:
    """The files one method consists of, as paths from the tree root: its declaration, its own files and the
    helper files it lists (exactly what its fingerprint covers). For example
    ['src/methods/E_002/RECUR_MEAN_ALL_V1/VARIANT.json', ..., 'src/methods/_shared/recurrence_gaps_v1.py']."""
    return [f'{METHODS_FOLDER}/{path}' for path, _ in variant.fingerprint_lines]


def has_tree(settings: TreeSettings, role: str) -> bool:
    """True if a tree of this role exists where the settings say: its folder holds a settings file."""
    return (settings.places[role].tree_root / SETTINGS_FILE_NAME).is_file()


def other_tree(settings: TreeSettings, role: str) -> TreeSettings:
    """Before a command reads from or writes into another tree (rule 3): read that tree's own settings, require
    the role meant, check its working folders, and require that its file names the same places as this tree's.

    settings: this tree's settings.  role: the other tree's role, for example 'QA'.
    Returns the other tree's settings. Refuses (SettingsRefused, LaunchRefused) if there is no tree there, it is
    not the tree meant, or the two settings files disagree about where the trees and their backups are.
    """
    theirs = enter_tree(settings.places[role].tree_root, must_be=role)
    if not same_places(settings, theirs):
        raise SettingsRefused(
            f'{theirs.tree_root / SETTINGS_FILE_NAME} and {settings.tree_root / SETTINGS_FILE_NAME} do not name '
            f'the same folders for the three trees and their backups. Nothing is done. Correct one of them by '
            f'hand, so that both say the same.')
    return theirs


def lock_trees(stack, trees, purpose: str, when: str) -> dict:
    """Take the lock of every tree a command touches, in the order DEV, QA, PROD; they are released when the
    stack closes.

    stack: a contextlib.ExitStack.  trees: the TreeSettings of the trees.  purpose, when: for the lock files.
    Returns {role: the lock}. Refuses (LaunchRefused) if one is held; those already taken are released.
    """
    return {tree.role: stack.enter_context(tree_lock(tree.tree_root, purpose, when))
            for tree in sorted(trees, key=lambda tree: ROLES.index(tree.role))}


def back_up_first(settings: TreeSettings, why: str, moment, say, backup=backups.make_backup) -> Path:
    """The backup made before a replacement. If it cannot be made the command stops before it replaces anything
    (scheme section 7).  settings: the tree to back up.  why: for the file's name, for example 'before install'.
    Returns the backup's path. Refuses (CommandRefused) if it could not be made."""
    try:
        path = backup(settings, why, moment)
    except backups.BackupFailed as fault:
        raise CommandRefused(f'{fault}. Nothing was replaced: a replacement is made only after a backup.') from None
    say(f'Backup made of the {settings.role} tree: {path}')
    return path


def require_python(settings: TreeSettings) -> None:
    """Refuse (CommandRefused) before anything is changed if a tree's own Python is not there: its research job
    could not be run afterwards."""
    if not settings.python.is_file():
        raise CommandRefused(
            f'the {settings.role} tree has no Python environment of its own ({settings.python} was not found), so '
            f'its research job could not be run afterwards. Nothing was changed. Build it first: in '
            f'{settings.tree_root} run create_venv.bat, then install_upgrade_dependencies_into_venv.bat.')


def run_job_of(settings: TreeSettings, key: str, say) -> int:
    """Run a tree's own research job, with its own Python and its own software, leaving the results updater out,
    under the lock this command holds there.

    settings: the tree.  key: the key of the lock held on it (research/tree_lock.py).  say: prints one line.
    What the job prints appears as it runs. Returns the job's exit code (0 finished, 1 not cleanly, 2 refused).
    """
    command = [str(settings.python), '-I', '-B', '-u', str(settings.tree_root / 'src' / 'research_command.py'),
               'research', '--no-update', '--under-lock', key]
    say(f'Now the {settings.role} tree\'s own research job (results updater left out), under the lock held:')
    return subprocess.run(command, cwd=settings.tree_root).returncode


def replace_folder(source_root: Path, target_root: Path, relative: str, leave_out=()) -> int:
    """Make a folder of the target tree the same as the source tree's: what the target holds there is removed,
    then every file of the source's folder is copied.

    relative: the folder from the tree root, for example 'source_data'.
    leave_out: file names never copied, for example ('I_AM_INSTALLABLE',).
    Returns the number of files copied (0 if the source tree has no such folder: the target then has none).
    """
    target = Path(target_root) / relative
    if target.exists():
        shutil.rmtree(target)
    names = [name for name in files_under(Path(source_root) / relative) if Path(name).name not in leave_out]
    for name in names:
        copy_file(source_root, target_root, f'{relative}/{name}')
    return len(names)
