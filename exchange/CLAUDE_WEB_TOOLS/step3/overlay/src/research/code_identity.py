"""The infrastructure manifest, the identity of the forecasting code, and the digests quoted in every line.

What this file is for
    deploy/INFRA_MANIFEST.ini lists every infrastructure file with a class that says what the file can change:
    `forecast` (it can change a forecast), `derived` (it can change a score, a report or an OV-1 line, never a
    forecast) or `other`. This file reads that list and computes: the identity of the forecasting code (one
    SHA-256 over the `forecast` files), which every list's header records; the digest of the code behind derived
    results (the `forecast` and `derived` files), which score and OV-1 lines quote. (The digest of the tree's
    Python environment, which every forecast's envelope quotes, is research/environment_marker.py's.)

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 12.4 (the manifest's syntax, the classes, the
    identity of the forecasting code) and 5.4 (the envelope's code digests).

Which of the project's own modules it uses
    None.

What uses it
    research/research_job.py, research/scoring.py, research/ov1_ledger.py, and the engine's tests.
"""
from __future__ import annotations

import configparser
import hashlib
from pathlib import Path

# The manifest's place in a tree, and its two sections (specification 12.4).
MANIFEST_PATH = 'deploy/INFRA_MANIFEST.ini'
FILES_SECTION = 'files'
INSTALL_TOOL_SECTION = 'install_tool'
# The three classes a file can have.
CLASSES = ('forecast', 'derived', 'other')


class ManifestRefused(ValueError):
    """The infrastructure manifest is missing or wrong. The message names the file and the line's path, says
    what was found and what to do."""


def _read_manifest_sections(tree_root: Path) -> dict:
    """Read the manifest of the tree and check every line of both its sections.

    tree_root: the tree's folder.
    Returns {section name: {path from the tree root, forward slashes: class}}, always with both sections, for
    example {'files': {'src/research/reader.py': 'forecast'}, 'install_tool': {'deploy/deploy_command.py': 'other'}}
    (an [install_tool] section that is not in the file is given as empty).
    Refuses (ManifestRefused): no manifest; a file Python's INI reader rejects (a malformed line and a path given
    twice among them); a section other than the two allowed; a path with a space or a backslash; a class that is
    not one of the three; a [files] path that does not exist in the tree. (Whether an [install_tool] file exists
    is checked by read_install_tool_list alone: those files lie in DEV and are never installed in a QA or PROD
    tree, whose manifest still names them.)
    """
    manifest_file = Path(tree_root) / MANIFEST_PATH
    if not manifest_file.is_file():
        raise ManifestRefused(f'{manifest_file}: the infrastructure manifest is missing. It arrives with the '
                              f'software; restore it from the package or from Git.')
    parser = configparser.ConfigParser(interpolation=None, delimiters=('=',), strict=True)
    parser.optionxform = str
    try:
        parser.read_string(manifest_file.read_text(encoding='utf-8'), source=str(manifest_file))
    except (configparser.Error, UnicodeDecodeError) as error:
        raise ManifestRefused(f'{manifest_file}: not a readable manifest ({error}). Each line is '
                              f'"<path> = <class>"; a path may appear once.') from None
    unknown = set(parser.sections()) - {FILES_SECTION, INSTALL_TOOL_SECTION}
    if unknown or not parser.has_section(FILES_SECTION):
        raise ManifestRefused(f'{manifest_file}: it must hold a [{FILES_SECTION}] section and may hold '
                              f'[{INSTALL_TOOL_SECTION}]; found {sorted(parser.sections())}.')
    sections = {FILES_SECTION: {}, INSTALL_TOOL_SECTION: {}}
    for section in parser.sections():
        for path, file_class in parser.items(section):
            file_class = file_class.strip()
            if ' ' in path or '\\' in path or path.startswith('/') or '..' in path.split('/'):
                raise ManifestRefused(f'{manifest_file}: "{path}" must be a path from the tree root with forward '
                                      f'slashes and no spaces.')
            if file_class not in CLASSES:
                raise ManifestRefused(f'{manifest_file}: "{path}" has the class "{file_class}"; it must be one of '
                                      f'{", ".join(CLASSES)}.')
            if section == FILES_SECTION and not (Path(tree_root) / path).is_file():
                raise ManifestRefused(f'{manifest_file}: "{path}" is listed but does not exist in {tree_root}. '
                                      f'Remove the line or restore the file.')
            sections[section][path] = file_class
    return sections


def read_manifest(tree_root: Path) -> dict:
    """The infrastructure of the tree: the manifest's [files] section, every line checked.

    tree_root: the tree's folder.
    Returns {path from the tree root, forward slashes: class}, for example
        {'src/research/reader.py': 'forecast', 'src/research/scoring.py': 'derived'}.
    Refuses (ManifestRefused) whatever _read_manifest_sections refuses, in either section.
    """
    return _read_manifest_sections(tree_root)[FILES_SECTION]


def read_install_tool_list(tree_root: Path) -> tuple:
    """The DEV-side install tool's own files: the manifest's [install_tool] section (specification 12.4).

    They are not infrastructure and are never installed into a QA or PROD tree; the infrastructure's readiness
    marker hashes them, and the recovery kit is built from them. tree_root: the tree's folder.
    Returns the paths from the tree root, sorted, for example ('Make_Installable.bat', 'deploy/deploy_command.py');
    empty if the manifest has no such section. Refuses (ManifestRefused) as read_manifest does, and a listed
    install tool file that does not exist: this is asked in DEV only, where every one of them lies.
    """
    tool_files = sorted(_read_manifest_sections(tree_root)[INSTALL_TOOL_SECTION])
    for path in tool_files:
        if not (Path(tree_root) / path).is_file():
            raise ManifestRefused(f'{Path(tree_root) / MANIFEST_PATH}: "{path}" is listed but does not exist in '
                                  f'{tree_root}. Remove the line or restore the file.')
    return tuple(tool_files)


def _digest_of_files(tree_root: Path, paths) -> str:
    """One SHA-256 over files, computed as a variant's fingerprint is (specification 3.4, 12.4): the SHA-256 of
    the lines '<path><TAB><sha256 of the file's bytes on disk><LF>', sorted by path."""
    text = ''.join(f'{path}\t{hashlib.sha256((Path(tree_root) / path).read_bytes()).hexdigest()}\n'
                   for path in sorted(paths))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def forecasting_code_identity(tree_root: Path, manifest: dict | None = None) -> str:
    """The identity of the tree's shared forecasting code: one SHA-256 over its `forecast`-class files.

    tree_root: the tree's folder.  manifest: read_manifest's result, if the caller already has it.
    Returns 64 hexadecimal characters. It identifies this project's source code and nothing more.
    """
    manifest = read_manifest(tree_root) if manifest is None else manifest
    return _digest_of_files(tree_root, [p for p, c in manifest.items() if c == 'forecast'])


def derived_code_digest(tree_root: Path, manifest: dict | None = None) -> str:
    """The digest of the code that makes derived results: one SHA-256 over the `forecast` and `derived` files.

    Score lines quote it as the scoring code's digest and prevailing lines as the OV-1 code's digest: both are
    made by this same set of files. tree_root, manifest: as for forecasting_code_identity.
    Returns 64 hexadecimal characters.
    """
    manifest = read_manifest(tree_root) if manifest is None else manifest
    return _digest_of_files(tree_root, [p for p, c in manifest.items() if c in ('forecast', 'derived')])

