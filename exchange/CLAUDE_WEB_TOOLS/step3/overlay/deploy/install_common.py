"""What every install into a QA or PROD tree shares: the plan, the barrier, copying, and the list of installed files.

What this file is for
    Init_Tree.bat, Install.bat and Reinstall_Infra.bat each do the same few things to a target tree. They work out
    a PLAN: every file to add, to overwrite or to remove, each with its SHA-256, and the variants that arrive.
    They write the plan into the BARRIER file records/INSTALL_IN_PROGRESS.json before the first change, so that
    no launcher of the tree works until the install is finished, and so that the same command typed again can
    tell whether it is finishing its own work or meeting another's. They COPY each file to a temporary name,
    hash what was written, and rename it into place; no existing file is ever opened for writing. They check the
    whole tree's software against what the plan says it must now be. And at the end they write the tree's LIST
    of installed files, add one line to its log, and remove the barrier, last. This file holds those steps; the
    three commands put them in their order.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md sections 3 (what can be installed, and what an install
    checks), 4, 5 and 6 (the steps the three commands share) and 8 (an operation stopped half-way);
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 12.1 to 12.4.

Which of the project's own modules it uses
    install_readiness (deploy/)   infrastructure_readiness, variant_readiness: the two markers
    research.code_identity        MANIFEST_PATH, read_manifest
    research.installed_files      LIST_PATH, METHODS_FOLDER, differences, read_list, software_now, write_list
    research.job_lock             RECORDS_FOLDER, is_link
    research.status_file          STATUS_FILE_NAME, create_active, read_status
    research.variant_folders      find_variants, sha256_of_file
    research.windows_text         windows_lines

What uses it
    deploy/init_tree.py, deploy/install.py and deploy/reinstall_infra.py (the three commands), and the tests.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import timezone
from pathlib import Path

import install_readiness
from research import code_identity, installed_files, variant_folders
from research.job_lock import RECORDS_FOLDER, is_link
from research.status_file import STATUS_FILE_NAME, StatusRefused, create_active, read_status
from research.windows_text import windows_lines

# The barrier: while this file lies in a tree, an install into it is unfinished and no launcher works there.
BARRIER_PATH = f'{RECORDS_FOLDER}/INSTALL_IN_PROGRESS.json'
BARRIER_KIND = 'INSTALL_IN_PROGRESS_V1'
PLAN_KIND = 'INSTALL_PLAN_V1'
# The tree's log: one line for each finished install, reinstall, creation, verification and withdrawal.
TREE_LOG_PATH = f'{RECORDS_FOLDER}/INSTALL_LOG.jsonl'
# The operations this file's commands carry out, as a plan names them.
INIT, INSTALL, REINSTALL_INFRA = 'INIT', 'INSTALL', 'REINSTALL_INFRA'
OPERATIONS = (INIT, INSTALL, REINSTALL_INFRA)
# The ending of a file that is being copied. A file with this ending is never installed software.
INSTALLING_SUFFIX = '.installing'
# How much of a file is read at a time, in bytes.
CHUNK = 1024 * 1024


class InstallRefused(ValueError):
    """The install cannot go on. The message says what was found, where, and what to do. What had been done
    before it stays as it is: the barrier, if written, is still in place."""


# --------------------------------------------------------------------------------------------- what DEV offers

def dev_infrastructure(dev_root: Path) -> dict:
    """The infrastructure DEV offers for installing, if its marker matches its files now.

    dev_root: DEV's folder.
    Returns {'fingerprint': the marker's fingerprint, 'files': {path: sha256}, 'classes': {path: class}}: the
    manifest itself and every file under its [files], with paths from the tree root; for example
        {'fingerprint': 'ab12...', 'files': {'deploy/INFRA_MANIFEST.ini': '...', 'src/research/reader.py': '...'},
         'classes': {'src/research/reader.py': 'forecast', ...}}
    The [install_tool] files are part of the fingerprint and are never installed.
    Refuses (InstallRefused) if the infrastructure is not ready, with the marker's own reason.
    """
    readiness = install_readiness.infrastructure_readiness(dev_root)
    if not readiness.ready:
        raise InstallRefused(readiness.reason)
    classes = code_identity.read_manifest(Path(dev_root))
    marked = dict(readiness.files)
    files = {path: marked[path] for path in classes}
    files[code_identity.MANIFEST_PATH] = variant_folders.sha256_of_file(Path(dev_root) / code_identity.MANIFEST_PATH)
    return {'fingerprint': readiness.fingerprint, 'files': files, 'classes': dict(classes)}


def dev_variants(dev_root: Path) -> tuple:
    """Every variant folder of DEV: those ready to be installed, and those that are not, each with its reason.

    dev_root: DEV's folder.
    Returns (ready, not_ready). ready: {identity: entry}, an entry being what a plan holds of a variant:
        {'family': 'E_002', 'variant': 'RECUR_MEAN_ALL_V1', 'fingerprint': 'ef56...', 'games': ['POWERBALL'],
         'files': {'src/methods/E_002/RECUR_MEAN_ALL_V1/VARIANT.json': '...', 'src/methods/_shared/x.py': '...'}}
    (its declaration, the files it declares and its helpers; never its marker, its status file or a cache).
    not_ready: {identity: one sentence}, for example 'E_002/X_V1: it is not marked. ...'.
    """
    methods_root = Path(dev_root) / installed_files.METHODS_FOLDER
    variants, refused = variant_folders.find_variants(methods_root)
    ready, not_ready = {}, {identity: str(reason).splitlines()[0] for identity, reason in refused}
    for variant in variants:
        readiness = install_readiness.variant_readiness(dev_root, variant.family, variant.variant)
        if not readiness.ready:
            not_ready[variant.identity] = readiness.reason.splitlines()[0]
            continue
        ready[variant.identity] = {
            'family': variant.family, 'variant': variant.variant, 'fingerprint': readiness.fingerprint,
            'games': list(variant.declaration['games']),
            'files': {f'{installed_files.METHODS_FOLDER}/{path}': digest for path, digest in readiness.files}}
    return ready, not_ready


# ---------------------------------------------------------------------------------------------------- the plan

def make_plan(operation: str, role: str, tree_root: Path, add: dict, overwrite: dict | None = None,
              remove: dict | None = None, variants=(), infrastructure_fingerprint: str | None = None,
              statement: str | None = None) -> dict:
    """Put a plan into its one form, so that the same intent always gives the same plan.

    operation: one of OPERATIONS.  role, tree_root: the target.
    add: {path: sha256} of files the target lacks.  overwrite: {path: (sha256 now in the target, sha256 to be)}.
    remove: {path: sha256 now in the target}.  variants: the entries of dev_variants for the variants that arrive.
    infrastructure_fingerprint: DEV's, when the plan carries infrastructure.  statement: what an infrastructure
    reinstall found it would change in the stored results (deployment design 6, step 3).
    Returns the plan, every list sorted, for example
        {'kind': 'INSTALL_PLAN_V1', 'operation': 'INSTALL', 'role': 'PROD', 'tree_root': 'G:\\\\a_p_r_i_r',
         'add': [{'path': 'src/methods/E_002/X_V1/method.py', 'sha256': '...'}], 'overwrite': [], 'remove': [],
         'variants': [{'family': 'E_002', 'variant': 'X_V1', 'fingerprint': '...', 'games': ['POWERBALL']}],
         'infrastructure_fingerprint': None, 'statement': None}
    """
    assert operation in OPERATIONS, operation
    return {'kind': PLAN_KIND, 'operation': operation, 'role': role, 'tree_root': str(tree_root),
            'add': [{'path': path, 'sha256': add[path]} for path in sorted(add)],
            'overwrite': [{'path': path, 'was': was, 'sha256': to_be}
                          for path, (was, to_be) in sorted((overwrite or {}).items())],
            'remove': [{'path': path, 'was': was} for path, was in sorted((remove or {}).items())],
            'variants': sorted(({'family': entry['family'], 'variant': entry['variant'],
                                 'fingerprint': entry['fingerprint'], 'games': list(entry['games'])}
                                for entry in variants), key=lambda entry: (entry['family'], entry['variant'])),
            'infrastructure_fingerprint': infrastructure_fingerprint, 'statement': statement}


def plan_lines(plan: dict) -> list:
    """The plan in lines for the owner; for example
        ['The plan (INSTALL into the PROD tree at G:\\a_p_r_i_r): 3 file(s) to add, 0 to overwrite, 0 to remove.',
         '  variant to add: E_002/X_V1 (POWERBALL)', '  add: src/methods/E_002/X_V1/VARIANT.json', ...]"""
    lines = [f'The plan ({plan["operation"]} into the {plan["role"]} tree at {plan["tree_root"]}): '
             f'{len(plan["add"])} file(s) to add, {len(plan["overwrite"])} to overwrite, {len(plan["remove"])} to '
             f'remove.']
    lines += [f'  variant to add: {entry["family"]}/{entry["variant"]} ({", ".join(entry["games"])})'
              for entry in plan['variants']]
    for word in ('add', 'overwrite', 'remove'):
        lines += [f'  {word}: {entry["path"]}' for entry in plan[word]]
    return lines


# ------------------------------------------------------------------------------------------------- the barrier

def barrier_bytes(plan: dict, started: str) -> bytes:
    """The exact bytes of the barrier file for a plan: ASCII JSON, keys sorted, two spaces of indent, CRLF."""
    content = {'kind': BARRIER_KIND, 'started': started, 'plan': plan}
    return windows_lines(json.dumps(content, indent=2, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')


def read_barrier(tree_root: Path) -> dict | None:
    """The plan in a tree's barrier file, or None if the tree has no barrier.

    Refuses (InstallRefused) a barrier that cannot be read as one: nothing is assumed about an install whose
    plan is unknown.
    """
    path = Path(tree_root) / BARRIER_PATH
    if not path.exists() and not is_link(path):
        return None
    try:
        content = json.loads(path.read_bytes().decode('ascii'))
        if content['kind'] != BARRIER_KIND or not isinstance(content['plan'], dict):
            raise ValueError('it is not a barrier file')
        return content['plan']
    except (OSError, ValueError, KeyError, TypeError) as fault:
        raise InstallRefused(f'{path} exists and cannot be read as the record of an unfinished install ({fault}). '
                             f'What was being installed is not known, so nothing is continued. Restore the tree '
                             f'from a backup you choose.') from None


def check_barrier(tree_root: Path, plan: dict, replace_unfinished: bool = False) -> bool:
    """Compare the barrier a tree holds, if any, with the plan now (deployment design section 8).

    Returns False if the tree has no barrier (a new install), True if it holds this same plan (this install is
    being continued), and also True if it holds another plan of an infrastructure reinstall and
    replace_unfinished was asked (the caller asks its question again before going on).
    Refuses (InstallRefused), showing both plans: a barrier with another plan; a barrier of an operation this
    command does not carry out.
    """
    found = read_barrier(tree_root)
    if found is None:
        return False
    if found == plan:
        return True
    if (replace_unfinished and plan['operation'] == REINSTALL_INFRA
            and found.get('operation') == REINSTALL_INFRA):
        return True
    mine = '\n'.join(plan_lines(plan))
    theirs = ('\n'.join(plan_lines(found)) if found.get('kind') == PLAN_KIND and found.get('operation') in OPERATIONS
              else f'an operation named {found.get("operation")!r}, which this command does not carry out')
    raise InstallRefused(f'{Path(tree_root) / BARRIER_PATH} exists and holds another plan than the plan now: a '
                         f'different operation is unfinished in this tree, or DEV changed since it began.\n'
                         f'THE UNFINISHED PLAN:\n{theirs}\nTHE PLAN NOW:\n{mine}\n'
                         f'Finish that operation with its own command (with DEV as it was), or restore the tree '
                         f'from a backup you choose. Nothing was changed.')


def write_barrier(tree_root: Path, plan: dict, started: str) -> None:
    """Write the barrier for a plan: the whole file under a temporary name, then one rename. A barrier that
    already holds this same plan is left as it is, byte for byte. The caller has compared any barrier found with
    the plan (check_barrier) and holds the tree's job lock; another plan found there is replaced only for an
    infrastructure reinstall whose replacement the owner has just agreed to.

    Refuses (InstallRefused) if the records folder is a link.
    """
    path = Path(tree_root) / BARRIER_PATH
    if is_link(path.parent) or is_link(path):
        raise InstallRefused(f'{path.parent}: the records folder of the target must be an ordinary folder; nothing '
                             f'was changed.')
    found = read_barrier(tree_root)
    if found == plan:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + INSTALLING_SUFFIX)
    with open(temporary, 'wb') as handle:
        handle.write(barrier_bytes(plan, started))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)                      # the whole barrier or none: never a half-written one


def remove_barrier(tree_root: Path) -> None:
    """Remove the barrier: the last act of an install."""
    (Path(tree_root) / BARRIER_PATH).unlink()


# -------------------------------------------------------------------------------------------------- the copying

def _hash_of(path: Path) -> str:
    """The SHA-256 of a file's bytes, read a part at a time."""
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for part in iter(lambda: handle.read(CHUNK), b''):
            digest.update(part)
    return digest.hexdigest()


def _check_no_link_on_the_way(tree_root: Path, relative: str) -> None:
    """Refuse if any folder between the tree's root and a file's place is a link: an install writes into the
    tree's own folders and nowhere else."""
    place = Path(tree_root)
    for part in Path(relative).parts[:-1]:
        place = place / part
        if is_link(place):
            raise InstallRefused(f'{place} is a link, a junction or another reparse point. An install writes only '
                                 f'into the tree\'s own folders. Remove the link (never what it points to).')


def copy_into_place(source: Path, tree_root: Path, relative: str, sha256: str, replace: bool = False) -> bool:
    """Put one file of the plan into the target: to a temporary name beside its place, hashed, renamed.

    source: the file in DEV.  tree_root, relative: the target and the file's path in it.
    sha256: the plan's hash for the file.  replace: True only for a file the plan overwrites.
    Returns True if the file was copied, False if it already lay there with the plan's bytes (the install is
    being continued). No existing file is opened for writing.
    Refuses (InstallRefused): a file there with other bytes that the plan does not overwrite; a link on the
    way; a source whose bytes are not the plan's (DEV changed after the plan was made).
    """
    target = Path(tree_root) / relative
    _check_no_link_on_the_way(tree_root, relative)
    if is_link(target) or (target.exists() and not target.is_file()):
        raise InstallRefused(f'{target}: something that is not an ordinary file lies where a file is to be '
                             f'installed. Nothing was written there.')
    if target.exists():
        if _hash_of(target) == sha256:
            return False
        if not replace:
            raise InstallRefused(f'{target}: already installed with different bytes. An install never changes an '
                                 f'installed file; changed work needs a new variant name. Nothing was written there.')
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + INSTALLING_SUFFIX)
    with open(source, 'rb') as reading, open(temporary, 'wb') as writing:
        for part in iter(lambda: reading.read(CHUNK), b''):
            writing.write(part)
        writing.flush()
        os.fsync(writing.fileno())
    if _hash_of(temporary) != sha256:
        temporary.unlink()
        raise InstallRefused(f'{source}: its bytes are not the bytes of the plan: DEV changed after the plan was '
                             f'made, or its marker no longer matches. Nothing was put in place of {target}. Run '
                             f'the command again; it makes its plan anew.')
    os.replace(temporary, target)
    return True


def carry_out(dev_root: Path, tree_root: Path, plan: dict, say=print) -> None:
    """Carry out a plan's file changes: every addition and overwrite, then the removals (design 6, step 7).

    A file already as the plan wants it is passed over, so the same command typed again goes on where it
    stopped. Refuses what copy_into_place refuses, and a file to be removed that holds neither the bytes the
    plan expects nor nothing.
    """
    copied = passed = 0
    for entry, replace in ([(entry, False) for entry in plan['add']] + [(entry, True) for entry in plan['overwrite']]):
        if copy_into_place(Path(dev_root) / entry['path'], tree_root, entry['path'], entry['sha256'], replace):
            copied += 1
        else:
            passed += 1
    removed = 0
    for entry in plan['remove']:
        target = Path(tree_root) / entry['path']
        _check_no_link_on_the_way(tree_root, entry['path'])
        if not target.exists():
            continue
        if _hash_of(target) != entry['was']:
            raise InstallRefused(f'{target}: it is to be removed, and its bytes are not the bytes the plan found '
                                 f'there. Nothing was removed.')
        target.unlink()
        removed += 1
    say(f'Files: {copied} copied (each to a temporary name, hashed, renamed); {passed} already in place; '
        f'{removed} removed.')


def create_status_files(tree_root: Path, plan: dict) -> int:
    """Create the status file of each variant that arrives, as ACTIVE in each of its games.

    Returns how many were created. One that already exists (the install is being continued) is read, and left
    if it passes its own check. Refuses (InstallRefused) one that exists and fails it.
    """
    created = 0
    for entry in plan['variants']:
        path = (Path(tree_root) / installed_files.METHODS_FOLDER / entry['family'] / entry['variant']
                / STATUS_FILE_NAME)
        try:
            if path.exists():
                read_status(path, entry['games'])
            else:
                create_active(path, entry['family'], entry['variant'], entry['games'])
                created += 1
        except StatusRefused as refusal:
            raise InstallRefused(f'the status file of {entry["family"]}/{entry["variant"]} fails its own check: '
                                 f'{refusal}') from None
    return created


# --------------------------------------------------------------------- what the tree's software must now be

def expected_list(before: dict | None, plan: dict) -> dict:
    """The list of installed files the target must have once the plan is carried out.

    before: the target's list before the install (installed_files.read_list), or None for a tree being created.
    Returns a list's content in the form installed_files.software_now gives, so that the two can be compared
    whole: the old list, with the plan's additions and overwrites, without its removals, and with the variants
    that arrive and their status files.
    """
    files = {entry['path']: entry['sha256'] for entry in (before or {'files': []})['files']}
    for entry in plan['add'] + plan['overwrite']:
        files[entry['path']] = entry['sha256']
    for entry in plan['remove']:
        files.pop(entry['path'], None)
    variants = {(entry['family'], entry['variant']): entry['fingerprint']
                for entry in (before or {'variants': []})['variants'] + plan['variants']}
    ordered = sorted(variants)
    return {'kind': installed_files.LIST_KIND,
            'files': [{'path': path, 'sha256': files[path]} for path in sorted(files)],
            'variants': [{'family': family, 'variant': variant, 'fingerprint': variants[family, variant]}
                         for family, variant in ordered],
            'status_files': [f'{installed_files.METHODS_FOLDER}/{family}/{variant}/{STATUS_FILE_NAME}'
                             for family, variant in ordered]}


def software_differences(tree_root: Path, expected: dict) -> list:
    """Every way the target's software differs from what the plan says it must now be (design 5, step 8).

    expected: expected_list's result.
    Returns one sentence a difference, empty when the tree is exactly that: every listed file present with its
    bytes, nothing else under src, and the tree's own reading of its software (its manifest, its variants and
    their fingerprints) giving that same list.
    """
    found = installed_files.differences(tree_root, expected)
    if found:
        return found
    try:
        now = installed_files.software_now(tree_root)
    except installed_files.InstalledFilesRefused as refusal:
        return [f'the tree\'s software cannot be read as installed software: {refusal}']
    if now != expected:
        for key in ('files', 'variants', 'status_files'):
            if now[key] != expected[key]:
                extra = [entry for entry in now[key] if entry not in expected[key]]
                missing = [entry for entry in expected[key] if entry not in now[key]]
                found.append(f'the tree\'s own reading of its {key} is not the plan\'s: in the tree and not in '
                             f'the plan: {extra}; in the plan and not in the tree: {missing}')
    return found


def status_file_faults(tree_root: Path) -> list:
    """Every status file of the target that is missing or fails its own check (design 3.3, item 2), one
    sentence each; empty when every installed variant has a status file that passes."""
    variants, refused = variant_folders.find_variants(Path(tree_root) / installed_files.METHODS_FOLDER)
    faults = [f'{identity}: {reason}' for identity, reason in refused]
    for variant in variants:
        try:
            read_status(variant.folder / STATUS_FILE_NAME, list(variant.declaration['games']))
        except StatusRefused as refusal:
            faults.append(f'{variant.identity}: {refusal}')
    return faults


# -------------------------------------------------------------------------------------------------- the ending

def log_line(tree_root: Path, record: dict, now) -> None:
    """Add one line to the tree's log. record: what happened, for example {'operation': 'INSTALL', 'role':
    'PROD', 'variants': ['E_002/X_V1'], 'software_fingerprint': '5d0c...'}; the time is added here."""
    line = dict(record, time=now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    path = Path(tree_root) / TREE_LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a', encoding='ascii', newline='\n') as stream:
        stream.write(json.dumps(line, ensure_ascii=True, sort_keys=True) + '\n')


def finish(tree_root: Path, plan: dict, expected: dict, now, extra: dict | None = None) -> str:
    """The ending every install shares (design 5, step 10): the list of installed files, the log line, and the
    barrier removed, last.

    expected: the list the tree's software was checked against.  extra: more for the log line.
    Returns the tree's new software fingerprint (the SHA-256 of its list of installed files).
    """
    installed_files.write_list(tree_root, expected)
    fingerprint = hashlib.sha256((Path(tree_root) / installed_files.LIST_PATH).read_bytes()).hexdigest()
    log_line(tree_root, dict({'operation': plan['operation'], 'role': plan['role'], 'tree_root': plan['tree_root'],
                              'added': len(plan['add']), 'overwritten': len(plan['overwrite']),
                              'removed': len(plan['remove']),
                              'variants': [f'{entry["family"]}/{entry["variant"]}' for entry in plan['variants']],
                              'infrastructure_fingerprint': plan['infrastructure_fingerprint'],
                              'statement': plan['statement'], 'software_fingerprint': fingerprint},
                             **(extra or {})), now)
    remove_barrier(tree_root)
    return fingerprint
