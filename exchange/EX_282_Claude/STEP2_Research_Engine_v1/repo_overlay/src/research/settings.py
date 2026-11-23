"""A tree's own settings file, ENVIRONMENT.ini: reading it and checking it.

What this file is for
    Every tree (DEV, QA, PROD) has one small settings file at its root that says what the tree is: its role, its
    own folder, where its backups go, and (in QA and DEV) where the accepted results are copied from. No path and
    no role is written in any program: programs read them here. This file reads the settings and makes the
    checks that concern one tree. It never writes a settings file.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 2;
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 1 (the checks 1 to 4 as they apply to one tree).

Which of the project's own modules it uses
    None.

What uses it
    research/research_job.py and research/withdraw.py (through the launchers), and the engine's tests.
"""
from __future__ import annotations

import configparser
import os
from dataclasses import dataclass
from pathlib import Path

# The settings file's name, at the root of every tree.
SETTINGS_FILE_NAME = 'ENVIRONMENT.ini'
# The tracked example the owner copies to make DEV's file (deployment design section 1).
EXAMPLE_FILE_NAME = 'ENVIRONMENT.example.ini'
# The three roles a tree can have.
ROLES = ('DEV', 'QA', 'PROD')


class SettingsRefused(ValueError):
    """The settings file is missing or wrong. The message names the file, the section and the key, says what was
    found and what to do."""


@dataclass(frozen=True)
class TreeSettings:
    """What a tree's settings file says.

    role: 'DEV', 'QA' or 'PROD'.  tree_root: the tree's own folder.  venv_dir: its Python environment folder.
    backup_root: where its backups go (None in DEV, which has none).
    results_copy_from: the tree whose accepted results this tree copies (None in PROD, and in a DEV or QA tree
    whose file names none yet).
    """
    role: str
    tree_root: Path
    venv_dir: Path
    backup_root: Path | None
    results_copy_from: Path | None


def _same_folder(a: Path, b: Path) -> bool:
    """True if two paths name the same folder, compared as the operating system compares names (Windows ignores
    letter case). For example _same_folder(Path('E:/a'), Path('e:/A')) is True on Windows."""
    return os.path.normcase(str(a)) == os.path.normcase(str(b))


def _inside(inner: Path, outer: Path) -> bool:
    """True if `inner` is `outer` itself or lies under it, for example _inside(Path('/t/.venv'), Path('/t'))."""
    inner_text, outer_text = os.path.normcase(str(inner)), os.path.normcase(str(outer))
    return inner_text == outer_text or inner_text.startswith(outer_text.rstrip('\\/') + os.sep)


def _real_absolute_path(text: str, where: str) -> Path:
    """Turn one path of the settings file into a Path, refusing a relative path or one that passes through a link.

    text: the value as written, for example 'D:\\TEST_BED'.  where: 'file [section] key', for the message.
    Returns the Path. Refuses (SettingsRefused) a path that is not absolute, or that is not its own real path
    (a junction, a link or a substituted drive lies in it), saying which.
    """
    path = Path(text)
    if not text or not path.is_absolute():
        raise SettingsRefused(f'{where}: "{text}" is not an absolute path. Type the full path of the folder.')
    real = Path(os.path.realpath(path))
    if not _same_folder(real, path):
        raise SettingsRefused(f'{where}: "{text}" is not its own real path (it resolves to "{real}"): a link, a '
                              f'junction or a substituted drive lies in it. Type the real path.')
    return path


def read_settings(tree_root: Path) -> TreeSettings:
    """Read and check the settings file of the tree at `tree_root`.

    tree_root: the folder the launcher is in.
    Returns the TreeSettings, for example TreeSettings(role='DEV', tree_root=Path('E:/.../project'), venv_dir=...,
    backup_root=None, results_copy_from=None).
    Refuses (SettingsRefused): no file; a file Python's INI reader rejects; a missing section or key; a role that
    is not DEV, QA or PROD; a path that is relative or not real; a tree_root that is not this folder ("this tree
    is not what its file says"); an environment folder outside the tree; a backup root inside the tree; a
    [results] section in PROD; a copy_from that is this tree itself.
    """
    file_path = Path(tree_root) / SETTINGS_FILE_NAME
    if not file_path.is_file():
        raise SettingsRefused(f'{file_path}: the settings file is missing. In DEV, copy {EXAMPLE_FILE_NAME} to '
                              f'{SETTINGS_FILE_NAME} beside it and type this PC\'s paths; in QA and PROD only '
                              f'Init_Tree creates it.')
    parser = configparser.ConfigParser(interpolation=None, delimiters=('=',), strict=True)
    parser.optionxform = str
    try:
        parser.read_string(file_path.read_text(encoding='utf-8'), source=str(file_path))
    except (configparser.Error, UnicodeDecodeError) as error:
        raise SettingsRefused(f'{file_path}: not a readable settings file ({error}). Correct the file by hand.') from None

    def value(section: str, key: str) -> str:
        """One value of the file, refusing a missing section or key by name."""
        if not parser.has_section(section) or not parser.has_option(section, key):
            raise SettingsRefused(f'{file_path} [{section}] {key}: this setting is missing. Add it to the file '
                                  f'(see {EXAMPLE_FILE_NAME}).')
        return parser.get(section, key).strip()

    role = value('environment', 'role')
    if role not in ROLES:
        raise SettingsRefused(f'{file_path} [environment] role: "{role}" is not one of {", ".join(ROLES)}.')
    root = _real_absolute_path(value('environment', 'tree_root'), f'{file_path} [environment] tree_root')
    if not _same_folder(root, Path(os.path.realpath(tree_root))):
        raise SettingsRefused(f'{file_path} [environment] tree_root: the file says "{root}" but it lies in '
                              f'"{tree_root}". This tree is not what its file says: a copied or moved tree is '
                              f'refused. Correct the file, or use the tree where it was created.')
    venv = _real_absolute_path(value('environment', 'venv_dir'), f'{file_path} [environment] venv_dir')
    if not _inside(venv, root) or _same_folder(venv, root):
        raise SettingsRefused(f'{file_path} [environment] venv_dir: "{venv}" is not inside the tree "{root}". The '
                              f'environment folder must lie inside its own tree, so that every backup holds it.')
    backup = None
    if role != 'DEV':
        backup = _real_absolute_path(value('environment', 'backup_root'), f'{file_path} [environment] backup_root')
        if _inside(backup, root) or _inside(root, backup):
            raise SettingsRefused(f'{file_path} [environment] backup_root: "{backup}" and the tree "{root}" lie '
                                  f'one inside the other. The backup root must be outside the tree.')
    copy_from = None
    if parser.has_section('results'):
        if role == 'PROD':
            raise SettingsRefused(f'{file_path} [results]: PROD has no [results] section; its results come from '
                                  f'the updater. Remove the section.')
        copy_from = _real_absolute_path(value('results', 'copy_from'), f'{file_path} [results] copy_from')
        if _inside(copy_from, root) or _inside(root, copy_from):
            raise SettingsRefused(f'{file_path} [results] copy_from: "{copy_from}" is this tree, or lies inside '
                                  f'or around it. It must name the other tree whose results are copied.')
    return TreeSettings(role=role, tree_root=root, venv_dir=venv, backup_root=backup, results_copy_from=copy_from)
