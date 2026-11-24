"""The two readiness markers of DEV: a variant's I_AM_INSTALLABLE.json and the infrastructure's
INFRA_IS_INSTALLABLE.json. Making them, removing them, and deciding whether a thing is ready.

What this file is for
    Nothing is installed from DEV into a QA or PROD tree unless it is marked ready, and the marker is the whole
    of readiness: there is no pass record and no approval file. A marker is an ordinary list of the files it
    covers with their SHA-256 and one fingerprint over them. It is bound to content: if any listed file changes
    afterwards the marker no longer matches and the thing is not ready until the marker is made again. Making a
    marker again on unchanged files writes the same bytes. A marker never lists itself. A marker made by hand
    counts only if it holds exactly what this file would write. A marker nominates; it proves nothing about
    correctness and is not the owner's approval.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 4 (readiness in DEV), 3.4 (the fingerprint
    and the import check) and 12.2 (the infrastructure's marker);
    doc/Predictive_Randomness_Deployment_Design_v0_12.md sections 3.1 and 3.2.

Which of the project's own modules it uses
    research.variant_folders   read_variant: the declaration's checks and the variant's fingerprint;
                               fingerprint_of, sha256_of_file: the same hashing for the infrastructure
    research.code_identity     read_manifest, read_install_tool_list: the infrastructure's two lists
    research.job_lock          check_real_folder: the staging folder must be a real folder of the tree
    install_import_check       the static import check of a variant and of the infrastructure

What uses it
    deploy/deploy_command.py (Make_Installable.bat), the install tools of build step 3 that ask "is it ready?",
    and its tests.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from research import code_identity, variant_folders
from research.job_lock import check_real_folder

import file_form
import install_import_check

# The marker of the infrastructure, from the tree root (deployment design 3.1). It is not on the manifest, so it
# is never part of what it hashes.
INFRA_MARKER_PATH = 'deploy/INFRA_IS_INSTALLABLE.json'
# What each marker says it is, so that a file of another kind is never taken for one.
VARIANT_MARKER_KIND = 'I_AM_INSTALLABLE_V1'
INFRA_MARKER_KIND = 'INFRA_IS_INSTALLABLE_V1'
# Where a marker is written whole before one rename puts it in place, from the tree root: outside every variant
# folder, so that an interrupted write never leaves an undeclared file among a variant's software.
STAGING_FOLDER = 'records/marker_staging'
# The folder of the variants and helpers, from the tree root: a marker's paths are given from here, as a
# variant's fingerprint gives them (specification 3.4).
METHODS_FOLDER = 'src/methods'
# The end of every line of a marker file: the Windows form the project's standard gives a text file.
LINE_ENDING = '\r\n'


class ReadinessRefused(ValueError):
    """A marker cannot be made, or a thing is not as readiness requires. The message says what was found, where,
    and what to do."""


@dataclass(frozen=True)
class Readiness:
    """Whether one variant, or the infrastructure, is ready to be installed.

    name: what it is, for example 'E_002/RECUR_MEAN_ALL_V1' or 'INFRA'.  ready: True or False.
    reason: when not ready, one full sentence saying why and what to do; '' when ready.
    fingerprint: the fingerprint computed now from the files (None if they could not be read).
    files: the hashed list computed now, as (path, sha256) pairs (empty if they could not be read).
    """
    name: str
    ready: bool
    reason: str
    fingerprint: str | None
    files: tuple


def marker_bytes(content: dict) -> bytes:
    """The exact bytes of a marker file: the same content always gives the same bytes.

    content: the marker as a dictionary.  Returns ASCII JSON, keys sorted, two spaces of indent, every line ending
    CRLF (the project's file-form standard: a marker is a text file), for example
    b'{\\r\\n  "files": [...],\\r\\n  "fingerprint": "ab12...",\\r\\n  "kind": "..."\\r\\n}\\r\\n'.
    """
    text = json.dumps(content, indent=2, sort_keys=True, ensure_ascii=True) + '\n'
    return text.replace('\n', LINE_ENDING).encode('ascii')


def _write_whole(tree_root: Path, target: Path, data: bytes) -> None:
    """Write a marker: the whole file under a temporary name in the tree's staging folder, then one rename.

    tree_root: the tree's folder.  target: the marker's place.  data: its bytes.
    Before the rename the old marker (or none) is in place; after it the new one: never a mixture.
    Refuses (ReadinessRefused) a staging folder that is not a real folder of this tree.
    """
    try:
        staging = check_real_folder(tree_root, STAGING_FOLDER)
    except Exception as refusal:
        raise ReadinessRefused(f'{refusal} No marker was written.') from None
    staging.mkdir(parents=True, exist_ok=True)
    temporary = staging / (target.relative_to(tree_root).as_posix().replace('/', '__') + '.tmp')
    with open(temporary, 'wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)


def _read_marker(path: Path):
    """Read a marker file as JSON, without judging it.

    Returns the parsed content (any JSON value), or None if there is no file. A file that is not JSON is returned
    as the text 'NOT JSON', which equals no marker this file would write.
    """
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeDecodeError):
        return 'NOT JSON'


def _refuse_files_not_in_their_form(tree_root: Path, what: str, paths) -> None:
    """Refuse to mark anything ready while one of its files is not in the project's file-form standard.

    tree_root: DEV's folder.  what: what is being marked, for the message ('E_002/RECUR_MEAN_ALL_V1', 'INFRA').
    paths: exactly the files the marker about to be written lists, from the tree root (standard section 6).
    Refuses (ReadinessRefused), naming each file and what is wrong with it. Nothing in the wrong form can be
    marked ready, so nothing in the wrong form can be installed.
    """
    faults = file_form.faults_of_files(Path(tree_root), sorted(paths))
    if faults:
        raise ReadinessRefused(f'{what}: {len(faults)} file(s) are not in the form the project\'s standard gives '
                               f'them:\n  ' + '\n  '.join(f'{fault.path}: {fault.what}' for fault in faults)
                               + f'\n  {file_form.RULE_IN_SHORT}')


# ------------------------------------------------------------------------------------------------- a variant

def _variant_now(tree_root: Path, family: str, variant_name: str):
    """Read one variant folder of DEV and make every check readiness asks of its files.

    Returns (the Variant, the marker content that matches its files now). Refuses (ReadinessRefused): a
    declaration or folder that read_variant refuses (an undeclared file among them), or a failing import check,
    each fault on its own line.
    """
    methods_root = Path(tree_root) / METHODS_FOLDER
    try:
        variant = variant_folders.read_variant(methods_root, family, variant_name)
        manifest = code_identity.read_manifest(tree_root)
        own_prefix = f'{family}/{variant_name}/'
        own_files = [f'{METHODS_FOLDER}/{path}' for path, _ in variant.fingerprint_lines if path.startswith(own_prefix)]
        helper_files = [f'{METHODS_FOLDER}/{helper}' for helper in variant.declaration['helpers']]
        faults = install_import_check.variant_import_faults(tree_root, own_files, helper_files, manifest)
    except (variant_folders.VariantRefused, code_identity.ManifestRefused,
            install_import_check.ImportCheckRefused) as refusal:
        raise ReadinessRefused(str(refusal)) from None
    if faults:
        raise ReadinessRefused(f'{family}/{variant_name}: the import check found {len(faults)} fault(s):\n  '
                               + '\n  '.join(faults))
    _refuse_files_not_in_their_form(tree_root, f'{family}/{variant_name}',
                                    [f'{METHODS_FOLDER}/{path}' for path, _ in variant.fingerprint_lines])
    content = {'kind': VARIANT_MARKER_KIND, 'family': family, 'variant': variant_name,
               'fingerprint': variant.fingerprint,
               'files': [{'path': path, 'sha256': digest} for path, digest in variant.fingerprint_lines]}
    return variant, content


def variant_marker_path(tree_root: Path, family: str, variant_name: str) -> Path:
    """The place of a variant's marker, for example <tree>/src/methods/E_002/RECUR_MEAN_ALL_V1/I_AM_INSTALLABLE.json."""
    return Path(tree_root) / METHODS_FOLDER / family / variant_name / variant_folders.MARKER_FILE_NAME


def mark_variant(tree_root: Path, family: str, variant_name: str) -> str:
    """Make a variant's readiness marker (Make_Installable.bat <family> <variant>).

    tree_root: DEV's folder.  family, variant_name: the folder names, for example 'E_002', 'RECUR_MEAN_ALL_V1'.
    Returns one line for the owner, for example 'E_002/RECUR_MEAN_ALL_V1: marked ready; fingerprint ab12...; 5
    files' or '...: already marked, and the marker matches its files; nothing was written'.
    Refuses (ReadinessRefused), having written nothing: an invalid declaration; an undeclared file in the folder;
    a missing listed file or helper; a failing import check.
    """
    _variant, content = _variant_now(tree_root, family, variant_name)
    path = variant_marker_path(tree_root, family, variant_name)
    name = f'{family}/{variant_name}'
    if _read_marker(path) == content and path.read_bytes() == marker_bytes(content):
        return f'{name}: already marked, and the marker matches its files; nothing was written'
    _write_whole(Path(tree_root), path, marker_bytes(content))
    return f'{name}: marked ready; fingerprint {content["fingerprint"]}; {len(content["files"])} files'


def unmark_variant(tree_root: Path, family: str, variant_name: str) -> str:
    """Remove a variant's readiness marker (Make_Installable.bat --unmark), so that no later install takes it.

    Returns one line for the owner. A variant with no marker is said to have none; that is not a refusal.
    Refuses (ReadinessRefused) a variant folder that does not exist.
    """
    path = variant_marker_path(tree_root, family, variant_name)
    if not path.parent.is_dir():
        raise ReadinessRefused(f'{path.parent}: there is no such variant folder. Check the family and the variant.')
    if not path.exists():
        return f'{family}/{variant_name}: it has no marker; nothing was removed'
    path.unlink()
    return f'{family}/{variant_name}: the marker was removed; it is no longer ready'


def variant_readiness(tree_root: Path, family: str, variant_name: str) -> Readiness:
    """Whether a variant of DEV is ready: a valid declaration, the import check passing, and a marker that holds
    exactly what its files give now (specification section 4).

    Returns the Readiness. It never refuses: whatever is wrong is the reason of a not-ready answer.
    """
    name = f'{family}/{variant_name}'
    try:
        variant, content = _variant_now(tree_root, family, variant_name)
    except ReadinessRefused as refusal:
        return Readiness(name, False, f'{refusal} Correct it, then run Make_Installable.bat {family} {variant_name}.',
                         None, ())
    found = _read_marker(variant_marker_path(tree_root, family, variant_name))
    if found is None:
        reason = f'{name}: it is not marked. If it is finished, run Make_Installable.bat {family} {variant_name}.'
    elif found != content:
        reason = (f'{name}: its marker does not match its files (a file changed after it was marked, or the marker '
                  f'was not made by Make_Installable). Finish the work and run Make_Installable.bat {family} '
                  f'{variant_name} again.')
    else:
        reason = ''
    return Readiness(name, not reason, reason, variant.fingerprint, variant.fingerprint_lines)


# ------------------------------------------------------------------------------------------- the infrastructure

def _infrastructure_now(tree_root: Path) -> dict:
    """Read the infrastructure of DEV as the manifest lists it and make every check readiness asks of it.

    Returns the marker content that matches the files now, for example {'kind': 'INFRA_IS_INSTALLABLE_V1',
    'fingerprint': 'ab12...', 'manifest': {'path': 'deploy/INFRA_MANIFEST.ini', 'sha256': '...'},
    'files': [{'path': 'src/research/reader.py', 'class': 'forecast', 'sha256': '...'}, ...],
    'install_tool': [{'path': 'deploy/deploy_command.py', 'sha256': '...'}, ...]}. The fingerprint is computed as
    a variant's is, over the manifest, every [files] file and every [install_tool] file, with paths from the tree
    root.
    Refuses (ReadinessRefused): a manifest the reader refuses (a listed file that does not exist among them); the
    marker itself on the manifest; a file on both lists; a project file the infrastructure imports that is not on
    the manifest.
    """
    root = Path(tree_root)
    try:
        manifest = code_identity.read_manifest(root)
        tool_files = code_identity.read_install_tool_list(root)
        faults = install_import_check.infrastructure_import_faults(root, manifest)
    except (code_identity.ManifestRefused, install_import_check.ImportCheckRefused) as refusal:
        raise ReadinessRefused(str(refusal)) from None
    manifest_path = code_identity.MANIFEST_PATH
    listed = list(manifest) + list(tool_files)
    if INFRA_MARKER_PATH in listed or manifest_path in listed:
        raise ReadinessRefused(f'{root / manifest_path}: it lists the manifest or the marker itself. Neither is '
                               f'listed: the marker hashes the manifest by itself and never itself. Remove the line.')
    twice = sorted(set(manifest) & set(tool_files))
    if twice:
        raise ReadinessRefused(f'{root / manifest_path}: listed under both [files] and [install_tool]: '
                               f'{", ".join(twice)}. List each file once.')
    if faults:
        raise ReadinessRefused(f'the infrastructure imports {len(faults)} project file(s) that are not on the '
                               f'manifest:\n  ' + '\n  '.join(faults))
    _refuse_files_not_in_their_form(root, 'INFRA', [manifest_path] + listed)
    digest = {path: variant_folders.sha256_of_file(root / path) for path in [manifest_path] + listed}
    return {'kind': INFRA_MARKER_KIND,
            'fingerprint': variant_folders.fingerprint_of(digest.items()),
            'manifest': {'path': manifest_path, 'sha256': digest[manifest_path]},
            'files': [{'path': path, 'class': manifest[path], 'sha256': digest[path]} for path in sorted(manifest)],
            'install_tool': [{'path': path, 'sha256': digest[path]} for path in tool_files]}


def mark_infrastructure(tree_root: Path) -> str:
    """Make the infrastructure's readiness marker (Make_Installable.bat INFRA).

    tree_root: DEV's folder.  Returns one line for the owner. Refuses (ReadinessRefused), having written
    nothing, whatever _infrastructure_now refuses.
    """
    content = _infrastructure_now(tree_root)
    path = Path(tree_root) / INFRA_MARKER_PATH
    if _read_marker(path) == content and path.read_bytes() == marker_bytes(content):
        return 'INFRA: already marked, and the marker matches the files; nothing was written'
    _write_whole(Path(tree_root), path, marker_bytes(content))
    return (f'INFRA: marked ready; fingerprint {content["fingerprint"]}; {len(content["files"])} infrastructure '
            f'files, {len(content["install_tool"])} install tool files, and the manifest')


def unmark_infrastructure(tree_root: Path) -> str:
    """Remove the infrastructure's marker (Make_Installable.bat --unmark INFRA). Returns one line for the owner;
    no marker is said as such and is not a refusal."""
    path = Path(tree_root) / INFRA_MARKER_PATH
    if not path.exists():
        return 'INFRA: it has no marker; nothing was removed'
    path.unlink()
    return 'INFRA: the marker was removed; the infrastructure is no longer ready'


def infrastructure_readiness(tree_root: Path) -> Readiness:
    """Whether DEV's infrastructure is ready: the manifest and every listed file as the marker says, and nothing
    it imports missing from the manifest. Returns the Readiness; it never refuses."""
    try:
        content = _infrastructure_now(tree_root)
    except ReadinessRefused as refusal:
        return Readiness('INFRA', False, f'{refusal} Correct it, then run Make_Installable.bat INFRA.', None, ())
    found = _read_marker(Path(tree_root) / INFRA_MARKER_PATH)
    files = tuple((entry['path'], entry['sha256']) for entry in content['files'] + content['install_tool'])
    if found is None:
        reason = 'INFRA: the infrastructure is not marked. If it is finished, run Make_Installable.bat INFRA.'
    elif found != content:
        reason = ('INFRA: the marker does not match the files (the manifest or a listed file changed after it was '
                  'marked, or the marker was not made by Make_Installable). Run Make_Installable.bat INFRA again.')
    else:
        reason = ''
    return Readiness('INFRA', not reason, reason, content['fingerprint'], files)
