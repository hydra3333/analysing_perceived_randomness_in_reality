"""Check_Tree: the owner's read-only look at one tree (DEV, QA or PROD), run from DEV.

What this file is for
    It prints, for the tree the owner names: how the settings are read; what is installed and whether the tree
    still matches its list of installed files; each variant's status; what is ready in DEV and how the tree
    compares with DEV; whether the tree's files are in the form the project's standard gives them; whether
    its Python environment is verified; the backup ZIPs in its backup folder; and the locks and
    unfinished-operation files that are present. It changes nothing in any tree: it opens files for
    reading only, takes no lock and writes no record. It is run from DEV with DEV's own Python and DEV's own
    code; it runs no code of the tree it looks at.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 16 ("read-only: what is installed, each
    variant's status, what is ready, any drift, the backup ZIPs, locks") and 14.1 (it lists the backup ZIPs and
    verifies none);
    doc/Predictive_Randomness_Deployment_Design_v0_12.md sections 1 (how the settings are read), 8 (the tree and
    its list differ) and 10; doc/FILE_FORM_STANDARD_v0_2.md section 6 (the checker's third place, and its files).

Which of the project's own modules it uses
    research.settings          entry_for, tree_as_dev_names_it: the tree DEV's file names, checked against its own
    research.installed_files   read_list, differences: the tree's list, and every way the tree differs from it
    research.variant_folders   find_variants: the variant folders of a tree, read as files
    research.status_file       read_status: a variant's operating status, with the file's own check
    research.code_identity     read_manifest, read_install_tool_list: the infrastructure's two lists
    research.job_lock          the names of the job lock, the updater's lock and the orphan marker
    research.launch_guard      the files that mean an operation did not finish; which trees have a marker
    research.environment_marker    read_marker: whether the tree's own Python environment is verified
    install_readiness          what is ready in DEV
    file_form                  the project's one rule for the form of a file

What uses it
    deploy/deploy_command.py, for Check_Tree.bat; and its tests.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import file_form
import install_readiness
from research import (code_identity, environment_marker, installed_files, job_lock, launch_guard, settings,
                      status_file, variant_folders)

# What the owner may type after Check_Tree.bat.
USAGE = ('Usage:  Check_Tree.bat DEV\n'
         '        Check_Tree.bat QA\n'
         '        Check_Tree.bat PROD\n'
         'It looks at that tree and changes nothing.')
# The exit codes: nothing wrong was found; something was found; the command could not look.
EXIT_NOTHING_FOUND, EXIT_FOUND, EXIT_COULD_NOT_LOOK = 0, 1, 2
# The folders of a tree in which the project's programs write, whose files are checked for their form
# (standard section 6). Under source_data only the files lying directly in it are checked: the results masters,
# their ledgers and their verification records. The updater's own kept copies in its sub-folders are left
# untouched by the standard (its section 7), and so are the two opening records of the retired first study
# (its section 3A), whose names begin with the words below.
WRITTEN_FOLDERS_WALKED = ('results/research', 'records')
RESULTS_FOLDER = 'source_data'
RETIRED_OPENING_RECORD_PREFIX = 'HOLDOUT_OPENED_'
# The tree's settings file, which the standard's section 6 names among the files Check_Tree checks.
SETTINGS_FILE = settings.SETTINGS_FILE_NAME
# The ending of a backup's file name (deployment design section 10).
BACKUP_SUFFIX = '.zip'


def _status_words(statuses: dict) -> str:
    """One variant's operating status in a few words, game by game.

    statuses: {game: GameStatus}, as read_status gives it.
    Returns, for example, 'POWERBALL: WITHDRAWN from draw 1601 (the gap table was wrong), prevailing OV-1 from
    draw 1596; OZLOTTO: ACTIVE, no eligibility draw yet'.
    """
    words = []
    for game, status in statuses.items():
        state = (f'WITHDRAWN from draw {status.withdrawn_from} ({status.withdrawn_reason})'
                 if status.withdrawn_from is not None else 'ACTIVE')
        counted = (f'prevailing OV-1 from draw {status.eligible_from}' if status.eligible_from is not None
                   else 'no eligibility draw yet')
        words.append(f'{game}: {state}, {counted}')
    return '; '.join(words)


def _variants_and_their_status(tree_root: Path, role: str, say) -> tuple:
    """Print every variant folder of the tree with its operating status.

    tree_root: the tree looked at.  role: its role.  say: the function that prints a line.
    Returns (variants, findings): the valid Variants, and one sentence for each thing found wrong (a variant
    folder that fails its checks; a status file that fails its own check; in QA and PROD a missing status file).
    """
    variants, refused = variant_folders.find_variants(tree_root / installed_files.METHODS_FOLDER)
    findings = [f'{identity}: {reason}' for identity, reason in refused]
    say(f'Variants: {len(variants)} variant folder(s) with a valid declaration.')
    for variant in variants:
        path = variant.folder / variant_folders.STATUS_FILE_NAME
        if not path.is_file():
            if role == 'DEV':
                say(f'  {variant.identity}: no status file yet (in DEV the research job creates it)')
            else:
                findings.append(f'{variant.identity}: its status file is missing ({path})')
            continue
        try:
            say(f'  {variant.identity}: {_status_words(status_file.read_status(path, variant.declaration["games"]))}')
        except status_file.StatusRefused as refusal:
            findings.append(str(refusal))
    return variants, findings


def _what_is_ready_in_dev(dev_root: Path, say) -> dict:
    """Print what is ready to be installed in DEV: the infrastructure, and each variant.

    dev_root: DEV's folder.  say: the function that prints a line.
    Returns {variant identity: Readiness} for every variant folder of DEV, for example
    {'E_002/RECUR_MEAN_ALL_V1': Readiness(name='E_002/RECUR_MEAN_ALL_V1', ready=True, ...)}.
    """
    infrastructure = install_readiness.infrastructure_readiness(dev_root)
    say('Ready in DEV: the infrastructure is ' + ('ready.' if infrastructure.ready
                                                    else f'NOT ready. {infrastructure.reason}'))
    variants, _refused = variant_folders.find_variants(dev_root / installed_files.METHODS_FOLDER)
    readiness = {variant.identity: install_readiness.variant_readiness(dev_root, variant.family, variant.variant)
                 for variant in variants}
    ready = sorted(name for name, found in readiness.items() if found.ready)
    say(f'Ready in DEV: {len(ready)} of {len(readiness)} variant(s) are marked ready and match their markers.')
    for name, found in sorted(readiness.items()):
        if not found.ready:
            say(f'  not ready: {found.reason.splitlines()[0]}')
    return readiness


def _compared_with_dev(dev_root: Path, content: dict, readiness: dict, say) -> None:
    """Print how an installed tree compares with DEV. This is information, never a finding: QA and PROD are each
    installed from DEV when the owner chooses, and may rightly be behind it.

    dev_root: DEV's folder.  content: the tree's list of installed files.  readiness: what is ready in DEV.
    say: the function that prints a line.
    """
    installed = {f'{entry["family"]}/{entry["variant"]}': entry['fingerprint'] for entry in content['variants']}
    for name, found in sorted(readiness.items()):
        if name not in installed:
            say(f'  {name}: ' + ('ready in DEV, not installed' if found.ready else 'in DEV, not ready, not installed'))
        elif found.fingerprint != installed[name]:
            say(f'  {name}: installed with different bytes than DEV now holds (an install leaves it alone: changed '
                f'work needs a new variant name)')
    for name in sorted(set(installed) - set(readiness)):
        say(f'  {name}: installed, and not a variant folder of DEV')
    listed = {entry['path']: entry['sha256'] for entry in content['files']}
    in_dev = [code_identity.MANIFEST_PATH, *code_identity.read_manifest(dev_root)]
    differing = sorted(path for path in in_dev
                       if listed.get(path) != variant_folders.sha256_of_file(dev_root / path))
    if differing:
        say(f'  the infrastructure differs from DEV\'s in {len(differing)} file(s): {", ".join(differing)}')
    else:
        say('  the infrastructure is file for file DEV\'s.')


def _files_checked_for_form(tree_root: Path, role: str, variants, content: dict | None) -> list:
    """The files of a tree whose form Check_Tree checks (standard section 6).

    tree_root: the tree.  role: its role.  variants: its valid Variants.  content: its list of installed files,
    or None in DEV, which keeps none: there the manifest's two lists and each variant's hashed files stand for it.
    Returns the paths from the tree root, sorted and each once: the software's files, the settings file, every
    status file that exists, and what the project's programs have written (the constants above say exactly where).
    """
    if content is not None:
        paths = {entry['path'] for entry in content['files']}
    else:
        paths = {code_identity.MANIFEST_PATH, *code_identity.read_manifest(tree_root),
                 *code_identity.read_install_tool_list(tree_root)}
        for variant in variants:
            paths.update(f'{installed_files.METHODS_FOLDER}/{path}' for path, _ in variant.fingerprint_lines)
    paths.add(SETTINGS_FILE)
    for variant in variants:
        status = variant.folder / variant_folders.STATUS_FILE_NAME
        if status.is_file():
            paths.add(status.relative_to(tree_root).as_posix())
    paths.update(file_form.files_under(tree_root, WRITTEN_FOLDERS_WALKED, with_root_files=False))
    results_folder = tree_root / RESULTS_FOLDER
    if results_folder.is_dir():
        paths.update(f'{RESULTS_FOLDER}/{entry.name}' for entry in results_folder.iterdir()
                     if entry.is_file() and not entry.name.startswith(RETIRED_OPENING_RECORD_PREFIX))
    return sorted(paths)


def _backups(backup_root: Path | None, say) -> None:
    """Print the full path, size and date of every backup ZIP in a tree's backup folder. None is verified.

    backup_root: the tree's backup folder, or None for DEV, which has none.  say: the function that prints a line.
    """
    if backup_root is None:
        say('Backups: DEV has no backup folder (its backups are Git and your own ZIP of the project folder).')
        return
    if not backup_root.is_dir():
        say(f'Backups: the backup folder {backup_root} does not exist yet.')
        return
    backups = sorted(entry for entry in backup_root.iterdir()
                     if entry.is_file() and entry.name.lower().endswith(BACKUP_SUFFIX))
    say(f'Backups: {len(backups)} ZIP file(s) in {backup_root}. This command lists them and verifies none.')
    for backup in backups:
        details = backup.stat()
        say(f'  {backup}  {details.st_size:,} bytes  {datetime.fromtimestamp(details.st_mtime):%Y-%m-%d %H:%M}')


def _environment(tree, say) -> None:
    """Print whether the tree's own Python environment has its verification marker. The marker is read; the
    environment's files and packages are not compared with it (this command runs with DEV's Python and cannot
    speak for another tree's), and the line printed says so: a marker that is present is not a finding that the
    environment is still the one that was verified. Each launch and each job in the tree checks that itself.

    tree: the settings of the tree looked at.  say: the function that prints a line.
    """
    if tree.role not in launch_guard.INSTALLED_ROLES:
        say('Environment: DEV\'s environment has no verification marker; none is asked of it.')
        return
    try:
        marker = environment_marker.read_marker(tree.venv_dir)
        say(f'Environment: verification marker present ({tree.venv_dir / environment_marker.MARKER_NAME}; it '
            f'lists {len(marker["distributions"])} package(s)). This command did not check the environment\'s '
            f'files or packages against it; each launch and each job in the tree does.')
    except environment_marker.EnvironmentRefused as refusal:
        say(f'Environment: NOT VERIFIED; every launcher of this tree refuses until it is. {refusal}')


def _locks(tree_root: Path, say) -> None:
    """Print which locks and unfinished-operation files are present in the tree. Each is a state to know of, not
    a fault of the tree.

    tree_root: the tree.  say: the function that prints a line.
    """
    present = [(name, what) for name, what in (
        (f'{job_lock.RECORDS_FOLDER}/{job_lock.JOB_LOCK_NAME}', 'the job lock: a job is running, or one was ended'),
        (job_lock.UPDATER_LOCK, 'the results updater\'s own lock'),
        (job_lock.ORPHAN_MARKER, 'THE ORPHAN MARKER: it blocks every launch until your approved clearance'),
        *((name, f'{meaning}. {way_on}') for name, meaning, way_on in launch_guard.UNFINISHED_OPERATIONS),
    ) if (tree_root / name).exists()]
    say(f'Locks and unfinished operations: {len(present)} present.')
    for name, what in present:
        say(f'  {tree_root / name}: {what}')


def main(arguments, view, say=print) -> int:
    """Run Check_Tree for the tree the owner named.

    arguments: what was typed after Check_Tree.bat, for example ['PROD'].  view: DEV's settings with its entries
    for QA and PROD, every check made (settings.read_dev_view's result).  say: the function that prints a line.
    Returns 0 when nothing wrong was found (a tree that is not created yet among them), 1 when something was
    found, 2 when the command could not look (a word that is not a role; a tree whose settings refuse).
    """
    role = arguments[0].upper() if len(arguments) == 1 else ''
    if role not in settings.ROLES:
        say(USAGE)
        return EXIT_COULD_NOT_LOOK
    dev_root = view.own.tree_root
    say(f'Check_Tree: looking at {role}, from DEV {dev_root}. It reads only; nothing is changed.')
    say(f'Settings: DEV\'s file {dev_root / SETTINGS_FILE} was read and passed every check. DEV: tree_root '
        f'{dev_root}; venv_dir {view.own.venv_dir}.')
    for name, entry in view.entries.items():
        say(f'Settings: DEV names {name} as tree_root {entry.tree_root}; backup_root {entry.backup_root}; venv_dir '
            f'{entry.venv_dir}.')
    try:
        if role == 'DEV':
            tree = view.own
        else:
            entry = settings.entry_for(view, role)
            if not entry.tree_root.exists() or not any(entry.tree_root.iterdir()):
                say(f'{role} is not created yet: {entry.tree_root} does not exist or is empty. Init_Tree.bat {role} '
                    f'creates it.')
                say('Check_Tree finished: there is no tree to look at.')
                return EXIT_NOTHING_FOUND
            tree = settings.tree_as_dev_names_it(view, role)
            say(f'Settings: {role}\'s own file {tree.tree_root / SETTINGS_FILE} says role {tree.role} and agrees '
                f'with DEV\'s entry.')
    except settings.SettingsRefused as refusal:
        say(f'REFUSED: {refusal}')
        return EXIT_COULD_NOT_LOOK
    tree_root = tree.tree_root
    findings, content = [], None
    if role == 'DEV':
        say('Installed: DEV keeps no list of installed files; its software is its working files.')
    else:
        try:
            content = installed_files.read_list(tree_root)
            say(f'Installed: {len(content["files"])} software file(s) and {len(content["variants"])} variant(s) '
                f'are on {tree_root / installed_files.LIST_PATH}.')
            drift = installed_files.differences(tree_root, content)
            say(f'Drift: {len(drift)} difference(s) between the tree and its list.'
                + (f' {installed_files.WHAT_TO_DO}' if drift else ''))
            findings.extend(drift)
        except installed_files.InstalledFilesRefused as refusal:
            findings.append(str(refusal))
    variants, status_findings = _variants_and_their_status(tree_root, role, say)
    findings.extend(status_findings)
    readiness = _what_is_ready_in_dev(dev_root, say)
    if content is not None:
        say(f'{role} compared with DEV (information; an install is your own act):')
        _compared_with_dev(dev_root, content, readiness, say)
    try:
        checked = _files_checked_for_form(tree_root, role, variants, content)
        faults = file_form.faults_of_files(tree_root, checked)
        say(f'File form: {len(checked)} file(s) checked; {len(faults)} not in the form the standard gives them.'
            + (f' {file_form.RULE_IN_SHORT}' if faults else ''))
        findings.extend(f'{fault.path}: {fault.what}' for fault in faults)
    except (file_form.FileFormRefused, code_identity.ManifestRefused) as refusal:
        findings.append(str(refusal))
    _environment(tree, say)
    _backups(tree.backup_root, say)
    _locks(tree_root, say)
    for finding in findings:
        say(f'FOUND: {finding}')
    say(f'Check_Tree finished: {len(findings)} thing(s) found in {role} {tree_root}.'
        + ('' if findings else ' Nothing was found by the checks this command makes. It starts nothing and does '
           'not check the tree\'s Python environment, so it does not say that the tree is ready to run.'))
    return EXIT_FOUND if findings else EXIT_NOTHING_FOUND
