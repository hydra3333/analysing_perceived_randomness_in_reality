r"""A tree's settings file, ENVIRONMENT.ini: reading it, and how a tree knows which tree it is.

What this file is for
    Every tree (DEV, QA, PROD) has one small settings file at its root, of the same form in all three: the
    tree's own role, and for each of the three roles where that tree lies and where its backups go.

        [environment]
        role = QA
        [DEV]
        tree_root = E:\...\a_p_r_i_r_DEV
        backup_root = T:\a_p_r_i_r_backups\DEV
        [QA]
        tree_root = T:\a_p_r_i_r_QA
        backup_root = T:\a_p_r_i_r_backups\QA
        [PROD]
        tree_root = G:\a_p_r_i_r_PROD
        backup_root = T:\a_p_r_i_r_backups\PROD

    No path and no role is written in any program: programs read them here. A command works on the folder its
    own launcher lies in, and this file checks that folder before anything else is done there: the role must be
    the ending of the folder's name, and that role's tree_root must be that folder. So a tree that was copied or
    renamed, or a settings file put into the wrong tree, runs nothing. The one time a settings file is written
    is when DEV creates a new QA or PROD tree: settings_text gives its text.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 3.1 (the four rules of identity).

Which of the project's own modules it uses
    none.

What uses it
    src/research_command.py and research/research_job.py (every command, first), research/backup.py, the tools of
    deploy/, and the tests.
"""
from __future__ import annotations

import configparser
import os
from dataclasses import dataclass
from pathlib import Path

# The settings file's name, at the root of every tree, and the tracked example it is made from in DEV.
SETTINGS_FILE_NAME = 'ENVIRONMENT.ini'
EXAMPLE_FILE_NAME = 'ENVIRONMENT.example.ini'
# The three roles a tree can have.
ROLES = ('DEV', 'QA', 'PROD')
# A tree's own Python environment, a folder at its root (built by the owner's two scripts; left out of backups).
ENVIRONMENT_FOLDER = '.venv'


class SettingsRefused(ValueError):
    """The settings file is missing or wrong, or the folder is not the tree the file says. The message names the
    file, the section and the key, says what was found and what to do."""


@dataclass(frozen=True)
class TreePlace:
    """Where one role's tree lies and where its backups go, as the settings file says."""
    tree_root: Path
    backup_root: Path


@dataclass(frozen=True)
class TreeSettings:
    """What a tree's settings file says.

    role: this tree's own role, 'DEV', 'QA' or 'PROD'.  places: {role: TreePlace} for all three roles.
    """
    role: str
    places: dict

    @property
    def tree_root(self) -> Path:
        """This tree's own folder."""
        return self.places[self.role].tree_root

    @property
    def backup_root(self) -> Path:
        """Where this tree's backups go."""
        return self.places[self.role].backup_root

    @property
    def venv_dir(self) -> Path:
        """This tree's own Python environment folder."""
        return self.tree_root / ENVIRONMENT_FOLDER

    @property
    def python(self) -> Path:
        """This tree's own Python program, for example T:\\a_p_r_i_r_QA\\.venv\\Scripts\\python.exe."""
        return self.venv_dir / 'Scripts' / 'python.exe'


def same_folder(a: Path, b: Path) -> bool:
    """True if two paths name the same folder, compared as the operating system compares names (Windows ignores
    letter case). For example same_folder(Path('E:/a'), Path('e:/A')) is True on Windows."""
    return os.path.normcase(str(a)) == os.path.normcase(str(b))


def inside(inner: Path, outer: Path) -> bool:
    """True if `inner` is `outer` itself or lies under it, for example inside(Path('/t/.venv'), Path('/t'))."""
    inner_text, outer_text = os.path.normcase(str(inner)), os.path.normcase(str(outer))
    return inner_text == outer_text or inner_text.startswith(outer_text.rstrip('\\/') + os.sep)


def _real_absolute_path(text: str, where: str) -> Path:
    """Turn one path of the settings file into a Path, refusing a relative path or one that passes through a link.

    text: the value as written, for example 'T:\\a_p_r_i_r_QA'.  where: 'file [section] key', for the message.
    Returns the Path. Refuses (SettingsRefused) a path that is not absolute, or that is not its own real path
    (a junction, a link or a substituted drive lies in it), saying which.
    """
    path = Path(text)
    if not text or not path.is_absolute():
        raise SettingsRefused(f'{where}: "{text}" is not an absolute path. Type the full path of the folder.')
    real = Path(os.path.realpath(path))
    if not same_folder(real, path):
        raise SettingsRefused(f'{where}: "{text}" is not its own real path (it resolves to "{real}"): a link, a '
                              f'junction or a substituted drive lies in it. Type the real path.')
    return path


def settings_from_text(text: str, file_path) -> TreeSettings:
    """What a settings file's text says, checked by rule 4, wherever the text came from: a tree's own file, or
    the settings file inside a backup that is about to be restored.

    text: the file's text.  file_path: where it came from, for the messages.
    Returns the TreeSettings. Refuses (SettingsRefused), in this order: a text Python's INI reader rejects; a
    missing section or key; a role that is not DEV, QA or PROD; a path that is relative or not real; two roles
    with one tree_root, or one tree inside another; a backup folder that is one of the trees or lies inside one.
    """
    parser = configparser.ConfigParser(interpolation=None, delimiters=('=',), strict=True)
    parser.optionxform = str
    try:
        parser.read_string(text, source=str(file_path))
    except configparser.Error as error:
        raise SettingsRefused(f'{file_path}: not a readable settings file ({error}). Correct the file by '
                              f'hand.') from None

    def value(section: str, key: str) -> str:
        """One value of the file, refusing a missing section or key by name."""
        if not parser.has_section(section) or not parser.has_option(section, key):
            raise SettingsRefused(f'{file_path} [{section}] {key}: this setting is missing. Add it to the file '
                                  f'(see {EXAMPLE_FILE_NAME}).')
        return parser.get(section, key).strip()

    role = value('environment', 'role')
    if role not in ROLES:
        raise SettingsRefused(f'{file_path} [environment] role: "{role}" is not one of {", ".join(ROLES)}.')
    places = {name: TreePlace(_real_absolute_path(value(name, 'tree_root'), f'{file_path} [{name}] tree_root'),
                              _real_absolute_path(value(name, 'backup_root'), f'{file_path} [{name}] backup_root'))
              for name in ROLES}
    for index, first in enumerate(ROLES):
        for second in ROLES[index + 1:]:
            a, b = places[first].tree_root, places[second].tree_root
            if inside(a, b) or inside(b, a):
                raise SettingsRefused(f'{file_path}: the {first} tree "{a}" and the {second} tree "{b}" are the same '
                                      f'folder, or one lies inside the other. Each tree has a folder of its own.')
    for name in ROLES:
        for tree in ROLES:
            if inside(places[name].backup_root, places[tree].tree_root):
                raise SettingsRefused(f'{file_path} [{name}] backup_root: "{places[name].backup_root}" is the {tree} '
                                      f'tree "{places[tree].tree_root}" or lies inside it. A backup folder lies '
                                      f'outside all three trees.')
    return TreeSettings(role=role, places=places)


def read_settings(tree_folder: Path, must_be: str | None = None) -> TreeSettings:
    """Read the settings file of the tree in a folder, and check that the folder is the tree the file says.

    tree_folder: the folder the launcher lies in (or, for a command that touches another tree, that tree's
    folder).  must_be: None, or the role the tree must have (rule 3: a command that reads from or writes into
    another tree says which role it means).
    Returns the TreeSettings, for example TreeSettings(role='QA', places={'DEV': TreePlace(...), 'QA': ..., ...}).
    Refuses (SettingsRefused), in this order: no file ("not a tree"); whatever settings_from_text refuses (rule
    4); a role that is not the ending of the folder's name, or whose tree_root is not this folder (rule 2); a
    role other than must_be (rule 3).
    """
    folder = Path(tree_folder)
    file_path = folder / SETTINGS_FILE_NAME
    if not file_path.is_file():
        raise SettingsRefused(f'{file_path}: there is no settings file here, so this folder is not a tree. In DEV, '
                              f'copy {EXAMPLE_FILE_NAME} to {SETTINGS_FILE_NAME} beside it and check its paths; a QA '
                              f'or PROD tree is made only by Create_Tree.bat.')
    try:
        text = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as error:
        raise SettingsRefused(f'{file_path}: not a readable settings file ({error}). Correct the file by '
                              f'hand.') from None
    read = settings_from_text(text, file_path)
    role, places = read.role, read.places
    real_folder = Path(os.path.realpath(folder))
    if not real_folder.name.endswith(role):
        raise SettingsRefused(f'{file_path} [environment] role: the file says {role}, but the folder it lies in is '
                              f'named "{real_folder.name}", which does not end with {role}. This folder is not the '
                              f'tree its file says: nothing is done here. (A tree that was copied or renamed, or a '
                              f'settings file from another tree, is refused.)')
    if not same_folder(places[role].tree_root, real_folder):
        raise SettingsRefused(f'{file_path} [{role}] tree_root: the file says the {role} tree is '
                              f'"{places[role].tree_root}", but the file lies in "{real_folder}". This folder is not '
                              f'the tree its file says: nothing is done here. Correct the file, or use the tree where '
                              f'it was created.')
    if must_be is not None and role != must_be:
        raise SettingsRefused(f'{file_path} [environment] role: this tree is {role}, but the command means the '
                              f'{must_be} tree. Nothing is done.')
    return read


def same_places(first: TreeSettings, second: TreeSettings) -> bool:
    """True if two settings files name the same three trees and the same three backup folders (their roles may
    differ). A command that touches another tree requires it, so that both files mean the same places."""
    return all(same_folder(first.places[name].tree_root, second.places[name].tree_root)
               and same_folder(first.places[name].backup_root, second.places[name].backup_root) for name in ROLES)


def settings_text(role: str, places: dict) -> str:
    """The text of a settings file, for the one command that writes one (Create_Tree, into a new tree).

    role: the new tree's role.  places: {role: TreePlace} for all three roles, as the creating tree's own file has
    them.  Returns the text with LF line ends, for example '[environment]\nrole = QA\n[DEV]\ntree_root = ...'.
    """
    lines = ['; The settings of this tree (the simple scheme v0.2, section 3.1). Written by Create_Tree.bat in DEV.',
             '; The same form in every tree; only the role differs. Never copy this file into another tree.',
             '[environment]', f'role = {role}']
    for name in ROLES:
        lines += [f'[{name}]', f'tree_root = {places[name].tree_root}', f'backup_root = {places[name].backup_root}']
    return '\n'.join(lines) + '\n'
