"""The settings file of a tree, ENVIRONMENT.ini: reading it and checking it.

What this file is for
    Every tree (DEV, QA, PROD) has one small settings file at its root that says what the tree is: its role, its
    own folder, where its backups go, and (in QA and DEV) where the accepted results are copied from. DEV's file
    also says where the QA and PROD trees are, in sections named [QA] and [PROD], so that DEV's tools can find
    them. No path and no role is written in any program: programs read them here. This file reads the settings
    and makes every check of the deployment design's section 1: those that concern one tree (read_settings), and
    those that concern the three trees together, as DEV's file names them (read_dev_view, tree_as_dev_names_it).
    It never writes a settings file.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 2;
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 1, checks 1 to 5.

Which of the project's own modules it uses
    None. (It uses the standard library only, so that the install tools and the recovery kit can use it too.)

What uses it
    research/research_job.py and research/withdraw.py (through the launchers); the install tools under deploy/
    (build step 3); and the tests.
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
# The two roles DEV's file can describe in a section of their own; the section's name is the role.
OTHER_TREE_ROLES = ('QA', 'PROD')


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


@dataclass(frozen=True)
class OtherTreeEntry:
    """What DEV's settings file says of the QA tree or the PROD tree, in the section named for it.

    role: 'QA' or 'PROD' (the section's name).  tree_root: that tree's folder.  venv_dir: its Python environment
    folder.  backup_root: where its backups go.  The tree need not exist yet: Init_Tree creates it from this.
    """
    role: str
    tree_root: Path
    venv_dir: Path
    backup_root: Path


@dataclass(frozen=True)
class DevView:
    """DEV's settings file as DEV's tools read it: DEV itself, and the other trees it names.

    own: DEV's own settings.  entries: {'QA': OtherTreeEntry, 'PROD': OtherTreeEntry}, holding only the roles DEV's
    file has a section for.  warnings: lines to print, each a full sentence (for example that a backup root lies
    on the same disk volume as its tree); empty when there is nothing to warn of.
    """
    own: TreeSettings
    entries: dict
    warnings: tuple


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


def _open_settings_file(tree_root: Path):
    """Read the settings file at a tree's root, without judging what it says.

    tree_root: the tree's folder.
    Returns (the file's path, the parsed file), for example (Path('E:/.../ENVIRONMENT.ini'), <ConfigParser>).
    Refuses (SettingsRefused): no file there; a file Python's INI reader rejects.
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
    return file_path, parser


def _value(parser, file_path: Path, section: str, key: str) -> str:
    """One value of a parsed settings file.

    parser, file_path: as _open_settings_file returned them.  section, key: for example 'QA', 'backup_root'.
    Returns the value without surrounding blanks, for example 'T:\\a_p_r_i_r_backups\\QA'.
    Refuses (SettingsRefused) a missing section or key, naming the file, the section and the key.
    """
    if not parser.has_section(section) or not parser.has_option(section, key):
        raise SettingsRefused(f'{file_path} [{section}] {key}: this setting is missing. Add it to the file '
                              f'(see {EXAMPLE_FILE_NAME}).')
    return parser.get(section, key).strip()


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
    file_path, parser = _open_settings_file(Path(tree_root))

    def value(section: str, key: str) -> str:
        """One value of the file, refusing a missing section or key by name."""
        return _value(parser, file_path, section, key)

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


def _volume_of(path: Path) -> str:
    """Name the disk volume a path lies on, so that two paths can be compared.

    path: an absolute, real path; it need not exist yet.
    Returns a text that is equal for two paths exactly when they lie on the same volume: on Windows the drive, for
    example 'T:' (the settings checks have already refused a link, a junction and a substituted drive, so a drive
    letter is a volume); elsewhere the device number of the nearest folder that exists, for example 'device 2049'.
    """
    drive = os.path.splitdrive(str(path))[0]
    if drive:
        return os.path.normcase(drive)
    nearest = Path(path)
    while not nearest.exists() and nearest != nearest.parent:
        nearest = nearest.parent
    return f'device {os.stat(nearest).st_dev}'


def read_dev_view(dev_root: Path) -> DevView:
    """Read DEV's settings file as DEV's tools need it: DEV's own settings, and its entries for QA and PROD, with
    every check of the deployment design's section 1 that concerns the three trees together (checks 1, 2, 3, 5).

    dev_root: DEV's folder (the folder the tool is in).
    Returns the DevView, for example DevView(own=TreeSettings(role='DEV', ...), entries={'QA': OtherTreeEntry(
    role='QA', tree_root=Path('T:/a_p_r_i_r'), venv_dir=Path('T:/a_p_r_i_r/.venv'),
    backup_root=Path('T:/a_p_r_i_r_backups/QA'))}, warnings=('[QA] backup_root ... lies on the same disk volume
    ...',)). A role with no section in the file is simply not in `entries`.
    Refuses (SettingsRefused): whatever read_settings refuses for DEV's own section; a file whose role is not DEV;
    in a [QA] or [PROD] section a missing key, or a path that is relative or not real; an environment folder that
    is not inside its own tree; two tree roots that are the same folder or lie one inside the other; a backup root
    and any tree root that lie one inside the other; the same backup root for QA and for PROD.
    """
    own = read_settings(dev_root)
    file_path, parser = _open_settings_file(Path(dev_root))
    if own.role != 'DEV':
        raise SettingsRefused(f'{file_path} [environment] role: this tree is {own.role}, not DEV. The install tools '
                              f'run from DEV only; run this command in the DEV tree.')
    entries = {}
    for role in OTHER_TREE_ROLES:
        if not parser.has_section(role):
            continue
        root = _real_absolute_path(_value(parser, file_path, role, 'tree_root'), f'{file_path} [{role}] tree_root')
        venv = _real_absolute_path(_value(parser, file_path, role, 'venv_dir'), f'{file_path} [{role}] venv_dir')
        backup = _real_absolute_path(_value(parser, file_path, role, 'backup_root'),
                                     f'{file_path} [{role}] backup_root')
        if not _inside(venv, root) or _same_folder(venv, root):
            raise SettingsRefused(f'{file_path} [{role}] venv_dir: "{venv}" is not inside that tree, "{root}". The '
                                  f'environment folder must lie inside its own tree, so that every backup holds it.')
        entries[role] = OtherTreeEntry(role=role, tree_root=root, venv_dir=venv, backup_root=backup)

    # Check 2: three different tree roots, none inside another; no backup root and tree root one inside the other.
    roots = [('[environment] tree_root', own.tree_root)]
    roots += [(f'[{role}] tree_root', entry.tree_root) for role, entry in entries.items()]
    for first in range(len(roots)):
        for second in range(first + 1, len(roots)):
            (first_name, first_root), (second_name, second_root) = roots[first], roots[second]
            if _inside(first_root, second_root) or _inside(second_root, first_root):
                raise SettingsRefused(f'{file_path}: {first_name} "{first_root}" and {second_name} "{second_root}" '
                                      f'are the same folder, or one lies inside the other. DEV, QA and PROD must be '
                                      f'three separate folders. Correct the file.')
    for role, entry in entries.items():
        for root_name, root in roots:
            if _inside(entry.backup_root, root) or _inside(root, entry.backup_root):
                raise SettingsRefused(f'{file_path}: [{role}] backup_root "{entry.backup_root}" and {root_name} '
                                      f'"{root}" lie one inside the other. A backup root must be outside every '
                                      f'tree, and no tree inside a backup root. Correct the file.')
    if len(entries) == 2 and _same_folder(entries['QA'].backup_root, entries['PROD'].backup_root):
        raise SettingsRefused(f'{file_path}: [QA] backup_root and [PROD] backup_root are the same folder, '
                              f'"{entries["QA"].backup_root}". Each tree needs a backup root of its own. Correct '
                              f'the file.')

    # Check 5: allowed, with a warning the tools print.
    warnings = tuple(
        f'WARNING: {file_path} [{role}] backup_root "{entry.backup_root}" lies on the same disk volume as that '
        f'tree, "{entry.tree_root}". It is allowed; a failure of that one disk would take the tree and its backups '
        f'together, so keep copies of the backup root on other media.'
        for role, entry in entries.items() if _volume_of(entry.backup_root) == _volume_of(entry.tree_root))
    return DevView(own=own, entries=entries, warnings=warnings)


def entry_for(view: DevView, role: str) -> OtherTreeEntry:
    """DEV's entry for the QA or the PROD tree, for a tool that is asked to work on that tree.

    view: read_dev_view's result.  role: 'QA' or 'PROD', as the owner typed it.
    Returns the OtherTreeEntry. Refuses (SettingsRefused) a role that is not QA or PROD, and a role DEV's file has
    no section for, saying which sections it does have.
    """
    file_path = view.own.tree_root / SETTINGS_FILE_NAME
    if role not in OTHER_TREE_ROLES:
        raise SettingsRefused(f'"{role}" is not a tree this command can work on. Type QA or PROD.')
    if role not in view.entries:
        has = ', '.join(f'[{name}]' for name in view.entries) or 'neither [QA] nor [PROD]'
        raise SettingsRefused(f'{file_path} [{role}]: DEV\'s settings file has no section for the {role} tree (it '
                              f'has: {has}). Add the section with tree_root, backup_root and venv_dir '
                              f'(see {EXAMPLE_FILE_NAME}).')
    return view.entries[role]


def tree_as_dev_names_it(view: DevView, role: str) -> TreeSettings:
    """The settings of an existing QA or PROD tree, checked against what DEV's file says of it (deployment design
    section 1, check 4: "a tree is what its own file says").

    view: read_dev_view's result.  role: 'QA' or 'PROD'.
    Returns that tree's own TreeSettings, read from the file in its own folder.
    Refuses (SettingsRefused): whatever entry_for refuses; no settings file in that folder, or one that
    read_settings refuses (a file naming another folder among them); a file that says another role; a backup root
    or an environment folder that differs from DEV's entry, printing both values.
    """
    entry = entry_for(view, role)
    dev_file = view.own.tree_root / SETTINGS_FILE_NAME
    found = read_settings(entry.tree_root)
    tree_file = entry.tree_root / SETTINGS_FILE_NAME
    if found.role != role:
        raise SettingsRefused(f'{tree_file} [environment] role: that tree\'s own file says it is {found.role}, but '
                              f'{dev_file} names that folder as [{role}]. A tree is what its own file says; nothing '
                              f'was done. Correct DEV\'s entry, or use the tree that is {role}.')
    for key, in_dev, in_tree in (('backup_root', entry.backup_root, found.backup_root),
                                 ('venv_dir', entry.venv_dir, found.venv_dir)):
        if in_tree is None or not _same_folder(in_dev, in_tree):
            raise SettingsRefused(f'{key} disagrees for the {role} tree: {dev_file} [{role}] says "{in_dev}"; '
                                  f'{tree_file} [environment] says "{in_tree}". The two files must agree. Edit both '
                                  f'by hand to the same value (deployment design section 1); nothing was done.')
    return found
