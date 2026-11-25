"""Init_Tree.bat QA|PROD: create a QA or PROD tree from DEV (run from DEV).

What this file is for
    A QA or PROD tree does not exist until this command makes it. It works out the plan (DEV's infrastructure,
    whose marker must match, and every variant of DEV that is marked ready), shows it and asks once. Then it
    creates the folder, writes the tree's own settings file (create-only, from DEV's entry for the role) and the
    barrier, copies every planned file, gives each variant its status file, and copies the accepted results.
    There it stops and asks the owner to build the tree's Python environment with his two scripts, which are
    now in the tree. The same command typed again goes on: it checks the tree's software against the plan, runs
    the suite and every variant's smoke case with the tree's own Python, has that Python write the environment's
    marker, writes the recovery kit, the list of installed files and the log line, removes the barrier, and
    attempts the first backup.

    A creation that stopped anywhere is finished by the same command. A folder that is not empty and is not
    this same unfinished creation is refused.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 4 (its nine steps) and sections 1 and 8;
    doc/Predictive_Randomness_System_Specification_v0_6.md section 12.5.

Which of the project's own modules it uses
    install_common (deploy/)      the plan, the barrier, the copying, the checks, the ending
    recovery_kit (deploy/)        build_kit
    research.installed_files      LIST_PATH, InstalledFilesRefused
    research.job_lock             RECORDS_FOLDER, UPDATER_LOCK, LaunchRefused, is_link
    research.process_rule         check_no_other_process_of_tree
    research.reader               LEDGER_NAME, MASTER_NAME, SOURCE_FOLDER, ResultsRefused, results_on_file
    research.research_job         GAMES
    research.settings             SETTINGS_FILE_NAME, SettingsRefused, TreeSettings, entry_for,
                                  tree_as_dev_names_it
    research.snapshot             attempt_snapshot
    research.windows_text         windows_lines

What uses it
    deploy/deploy_command.py (Init_Tree.bat), and the tests.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import install_common as common
import recovery_kit
from research import installed_files, process_rule, snapshot
from research.job_lock import RECORDS_FOLDER, UPDATER_LOCK, LaunchRefused, is_link
from research.reader import LEDGER_NAME, MASTER_NAME, SOURCE_FOLDER, ResultsRefused, results_on_file
from research.research_job import GAMES
from research.settings import SETTINGS_FILE_NAME, SettingsRefused, TreeSettings, entry_for, tree_as_dev_names_it
from research.status_file import StatusRefused
from research.windows_text import windows_lines

USAGE = 'Usage:  Init_Tree.bat QA\n        Init_Tree.bat PROD'
# The record of what a creation copied into the tree's source_data (deployment design section 4, step 5).
INIT_RECORD_PATH = f'{RECORDS_FOLDER}/INIT_RECORD.json'
INIT_RECORD_KIND = 'INIT_RECORD_V1'
# The accepted results of one game: the results, their version ledger and their verification record.
RESULTS_FILE_NAMES = (MASTER_NAME, LEDGER_NAME, '{game_id}_results_master_init_verification.json')
# What a target folder may hold besides nothing and still be a creation that has not begun.
SETTINGS_ONLY = (SETTINGS_FILE_NAME, RECORDS_FOLDER)
# The exit codes: the tree is created; a check failed or a fault stopped it, with the barrier in place; the
# command refused before it changed anything; it paused for the owner to build the tree's Python environment.
EXIT_CREATED, EXIT_STOPPED, EXIT_REFUSED, EXIT_BUILD_THE_ENVIRONMENT = 0, 1, 2, 3
# The states a target is found in.
NEW, CONTINUED = 'NEW', 'CONTINUED'


def settings_bytes(entry, copy_from: Path | None) -> bytes:
    """The exact bytes of a new tree's own settings file, from DEV's entry for it (deployment design section 1).

    entry: DEV's OtherTreeEntry for the role.  copy_from: the tree a QA tree's jobs copy results from (PROD's
    folder as DEV's file names it), or None: PROD has no [results] section, and neither has a QA tree while
    DEV's file names no PROD.
    """
    lines = ['[environment]', f'role = {entry.role}', f'tree_root = {entry.tree_root}',
             f'backup_root = {entry.backup_root}', f'venv_dir = {entry.venv_dir}']
    if copy_from is not None:
        lines += ['[results]', f'copy_from = {copy_from}']
    return windows_lines('\n'.join(lines) + '\n').encode('utf-8')


def target_state(entry, plan: dict, wanted_settings: bytes) -> str:
    """What lies where the tree is to be (deployment design section 4, step 1).

    Returns NEW for a folder that does not exist, is empty, or holds only this creation's own settings file (a
    creation that stopped before its barrier was written); CONTINUED for a folder that holds this same
    unfinished creation: its settings file and a barrier with this same plan.
    Refuses (InstallRefused): a link; a file; a settings file that is not the one this creation writes; a
    barrier with another plan (both shown); a tree that is already created; any other folder that is not empty.
    """
    root = entry.tree_root
    if is_link(root) or (root.exists() and not root.is_dir()):
        raise common.InstallRefused(f'{root} is a link or a file. A tree is created in a folder that does not '
                                    f'exist or is empty. Nothing was changed.')
    names = sorted(os.listdir(root)) if root.exists() else []
    if not names:
        return NEW
    settings_file = root / SETTINGS_FILE_NAME
    if not settings_file.is_file():
        raise common.InstallRefused(f'{root} is not empty and is not a tree this command began (it holds '
                                    f'{", ".join(names[:5])}{" ..." if len(names) > 5 else ""}). A tree is created '
                                    f'in a folder that does not exist or is empty. Nothing was changed.')
    if settings_file.read_bytes() != wanted_settings:
        raise common.InstallRefused(f'{settings_file} exists and is not the settings file this creation writes '
                                    f'from DEV\'s entry [{entry.role}]: another tree lies there, or DEV\'s entry '
                                    f'changed since a creation began. Nothing was changed.')
    if common.read_barrier(root) is not None:
        try:
            common.check_barrier(root, plan)
        except common.InstallRefused as refusal:
            raise common.InstallRefused(
                f'{refusal}\nIf it is this creation, begun when DEV held other files, it cannot be continued with '
                f'DEV as it is now. To abandon it, delete the folder {root} yourself (it holds only what this '
                f'command copied, and the environment if you built it) and create the tree anew.') from None
        return CONTINUED
    if (root / installed_files.LIST_PATH).exists():
        raise common.InstallRefused(f'{root} is already a created {entry.role} tree. To add variants use '
                                    f'Install.bat {entry.role}; to update its infrastructure use Reinstall_Infra.bat '
                                    f'{entry.role}. Nothing was changed.')
    records = root / RECORDS_FOLDER
    if set(names) - set(SETTINGS_ONLY) or (records.exists() and (not records.is_dir() or os.listdir(records))):
        raise common.InstallRefused(f'{root} holds this creation\'s settings file and no barrier, and other things '
                                    f'besides. It is not a creation this command can continue. Look at the folder; '
                                    f'if nothing in it is wanted, empty it and run the command again.')
    return NEW


def results_source(view, role: str) -> tuple:
    """The tree a new tree's accepted results are copied from (specification 12.5): for PROD, DEV; for QA, PROD
    if a PROD tree exists, and DEV while none does.

    Returns (the source tree's folder, 'DEV' or 'PROD'). It is chosen once, when a creation begins, shown before
    the question and kept in the creation's plan, so that a creation continued later copies from the tree the
    owner was shown.
    """
    dev_root = view.own.tree_root
    if role == 'PROD' or 'PROD' not in view.entries:
        return dev_root, 'DEV'
    prod_root = view.entries['PROD'].tree_root
    if not (prod_root / SETTINGS_FILE_NAME).is_file():
        return dev_root, 'DEV'
    return prod_root, 'PROD'


def check_source_may_be_read(view, source_root: Path, source_role: str) -> None:
    """Refuse to read a PROD tree's results while they may be changing, or if it is not the tree DEV's file names.

    Refuses a PROD tree that is not what DEV's file says (SettingsRefused); one that is not the folder the
    creation was begun with, or in which an install is unfinished or a results update holds its lock
    (InstallRefused). Nothing is ever written to PROD to mark or lock it. DEV as the source asks nothing here.
    """
    if source_role != 'PROD':
        return
    named = tree_as_dev_names_it(view, 'PROD').tree_root
    if os.path.normcase(os.path.realpath(named)) != os.path.normcase(os.path.realpath(source_root)):
        raise common.InstallRefused(f'this creation was begun with the PROD tree at {source_root} as the source of '
                                    f'its results, and DEV\'s file now names {named} as PROD. Nothing was copied.')
    for held, what in ((common.BARRIER_PATH, 'an install is unfinished there'),
                       (UPDATER_LOCK, 'a results update holds its lock there')):
        if (Path(source_root) / held).exists():
            raise common.InstallRefused(f'the PROD tree at {source_root} cannot be read for its results now: {what} '
                                        f'({Path(source_root) / held}). Let it finish, then run this command again.')


def results_files(source_root: Path) -> list:
    """The accepted results of every game in a tree, checked: each game's results are read whole as the engine
    reads them (they pass their check and their ledger names them), and each of the three files is an ordinary
    file.

    Returns the files as paths from the tree root, for example ['source_data/POWERBALL_results_master.csv', ...].
    Refuses (InstallRefused), naming the game or the file.
    """
    found = []
    for game_id in GAMES:
        try:
            results_on_file(source_root, game_id)
        except ResultsRefused as refusal:
            raise common.InstallRefused(f'the results of {game_id} in {source_root} cannot be copied: '
                                        f'{refusal}') from None
        for name in RESULTS_FILE_NAMES:
            relative = f'{SOURCE_FOLDER}/{name.format(game_id=game_id)}'
            source = Path(source_root) / relative
            if is_link(source) or not source.is_file():
                raise common.InstallRefused(f'{source} is missing or is not an ordinary file. The accepted results '
                                            f'of a game are its results, their ledger and their verification record.')
            found.append(relative)
    return found


def record_bytes(record: dict) -> bytes:
    """The exact bytes of INIT_RECORD.json: ASCII JSON, keys sorted, two spaces of indent, CRLF."""
    return windows_lines(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')


def _sha256(path: Path) -> str:
    """The SHA-256 of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_copied_pairs(target_root: Path) -> None:
    """Check that each game's results as they now lie in the new tree are a results file with the ledger that
    names it, by the engine's own reading: what the tree's first research job will ask of them.
    Refuses (InstallRefused), naming the game."""
    for game_id in GAMES:
        try:
            results_on_file(target_root, game_id)
        except ResultsRefused as refusal:
            raise common.InstallRefused(
                f'the results of {game_id} as they lie in {target_root} are not a results file with the ledger that '
                f'names it ({refusal}). The source was probably being updated while it was read. No record of the '
                f'copy stands on them: type the same command again and they are copied afresh.') from None


def copy_results(view, source_root: Path, source_role: str, plan: dict, now, say=print) -> None:
    """Copy the accepted results of each game into the new tree as ONE set, and keep the list as
    records/INIT_RECORD.json (deployment design section 4, step 5; EX_329 C-B02).

    view: DEV's settings.  source_root, source_role: the source kept in the creation's plan.
    plan: the creation's plan (its tree_root is the target).
    A creation that already has its record reads no source: the six files in the tree are checked against the
    record, and each game's pair by the engine's reading. Otherwise: the source is checked (results_files); all
    six files are hashed (the first reading); each is copied and its copy must have that hash; all six are
    hashed again (the second reading) and must be unchanged; each game's copied pair must pass the engine's
    reading; only then is the record written. Until the record is written the copied files are this creation's
    own and a retry replaces them. No forecast, score, report or OV-1 record is read or copied, and nothing is
    written to the source.
    Refuses (InstallRefused): what results_files and check_source_may_be_read refuse; a source file that changed
    between the two readings; a copied pair that fails the engine's reading; with a record, a file that is no
    longer what the record says.
    """
    target_root = Path(plan['tree_root'])
    record_path = target_root / INIT_RECORD_PATH
    wanted = [f'{SOURCE_FOLDER}/{name.format(game_id=game_id)}' for game_id in GAMES for name in RESULTS_FILE_NAMES]
    if record_path.exists():
        try:
            record = json.loads(record_path.read_bytes().decode('ascii'))
            listed = [entry['path'] for entry in record['results']]
            changed = [entry['path'] for entry in record['results']
                       if not (target_root / entry['path']).is_file()
                       or _sha256(target_root / entry['path']) != entry['sha256']]
        except (OSError, ValueError, KeyError, TypeError) as fault:
            raise common.InstallRefused(f'{record_path} cannot be read as this creation\'s record '
                                        f'({fault}).') from None
        if listed != wanted or changed:
            raise common.InstallRefused(f'the results copied when this creation began are no longer what its record '
                                        f'{record_path} says: {", ".join(changed) or "it does not list the six files"}. '
                                        f'Nothing was copied again.')
        check_copied_pairs(target_root)
        say(f'The accepted results: already copied from {record["results_copied_from"]} '
            f'({len(record["results"])} files, as the record says; each game\'s pair read as the engine reads it).')
        return
    check_source_may_be_read(view, source_root, source_role)
    files = results_files(source_root)
    first = {relative: _sha256(Path(source_root) / relative) for relative in files}
    try:
        for relative in files:
            common.copy_into_place(Path(source_root) / relative, target_root, relative, first[relative],
                                   replace=True)
    except common.InstallRefused as refusal:
        raise common.InstallRefused(f'the accepted results could not be copied from {source_root} as they were first '
                                    f'read; they were probably being updated. ({refusal}) Type the same command '
                                    f'again when nothing is updating the results there.') from None
    moved = [relative for relative in files if _sha256(Path(source_root) / relative) != first[relative]]
    if moved:
        raise common.InstallRefused(f'the accepted results in {source_root} changed while they were being copied '
                                    f'({", ".join(moved)}). No record of the copy was written. Type the same command '
                                    f'again when nothing is updating the results there; they are copied afresh.')
    check_copied_pairs(target_root)
    record = {'kind': INIT_RECORD_KIND, 'role': plan['role'], 'tree_root': plan['tree_root'],
              'time': now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'results_copied_from': str(source_root), 'results_copied_from_role': source_role,
              'results': [{'path': relative, 'sha256': first[relative]} for relative in files]}
    temporary = record_path.with_name(record_path.name + common.INSTALLING_SUFFIX)
    with open(temporary, 'wb') as handle:
        handle.write(record_bytes(record))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, record_path)
    say(f'The accepted results: {len(files)} files copied from the {source_role} tree at {source_root} as one set '
        f'(hashed before and after; each game\'s pair read as the engine reads it); the list is {record_path}.')


def make_creation_plan(dev_root: Path, entry, say=print) -> tuple:
    """The plan of a creation (deployment design section 4, step 2): DEV's infrastructure and every ready
    variant with its helpers, all hashed. Variants that are not ready are named with their reasons and left out.

    Returns (the plan, DEV's infrastructure as install_common.dev_infrastructure gives it).
    Refuses (InstallRefused) if the infrastructure's marker does not match.
    """
    infrastructure = common.dev_infrastructure(dev_root)
    ready, not_ready = common.dev_variants(dev_root)
    add = dict(infrastructure['files'])
    for variant in ready.values():
        add.update(variant['files'])
    plan = common.make_plan(common.INIT, entry.role, entry.tree_root, add, variants=ready.values(),
                            infrastructure_fingerprint=infrastructure['fingerprint'])
    for line in common.plan_lines(plan):
        say(line)
    for identity, reason in sorted(not_ready.items()):
        say(f'  left out, not ready: {reason}')
    return plan, infrastructure


def verify_and_finish(view, settings, plan: dict, infrastructure: dict, release, now, say, ask) -> int:
    """Steps 7 and 8 of a creation, made while the target is reserved and its barrier is in place.

    Returns EXIT_CREATED, or EXIT_STOPPED with the barrier left in place and the reason said.
    """
    dev_root, root = view.own.tree_root, settings.tree_root
    expected = common.expected_list(None, plan)
    faults = common.software_differences(root, expected) + common.status_file_faults(root)
    if faults:
        say(f'STOPPED: the tree\'s software is not what the plan says ({len(faults)} finding(s)):')
        for fault in faults:
            say(f'  {fault}')
        return EXIT_STOPPED
    say(f'The tree\'s software is exactly the plan: {len(expected["files"])} files, {len(expected["variants"])} '
        f'variant(s), each with its status file, and nothing else under src.')
    python = common.target_python(settings)
    passed, line = common.suite_if_it_is_the_trees(dev_root, infrastructure['files'], expected, python, say)
    say(line)
    if passed is not True:
        say('STOPPED: at a creation the tree\'s infrastructure is DEV\'s, and the suite must pass with the tree\'s '
            'own Python.')
        return EXIT_STOPPED
    say('The smoke cases: every variant is made to forecast once with the tree\'s own Python, on an invented table.')
    found = common.checks_with_target_python(python, root, root, common.ALL_VARIANTS, False, False, say,
                                             write_marker=True)
    stopping = common.faults_that_stop(found)
    if stopping or not found.get('marker'):
        say(f'STOPPED: {len(stopping)} smoke case(s) failed; the environment\'s marker was not written.')
        for fault in stopping:
            say(f'  {fault}')
        return EXIT_STOPPED
    say(f'The environment is verified; its digest is {found["marker"]}.')
    kit = recovery_kit.build_kit(dev_root, settings.backup_root, common.software_fingerprint_of(expected), now)
    if not kit.made:
        lines = [kit.line(), 'THE RESTORE TOOL COULD NOT BE WRITTEN: without a recovery kit in the backup folder, a '
                             'backup of this tree cannot be restored by the kit\'s own tool.',
                 f'Type {common.YES} to finish the creation without a recovery kit. Anything else, Enter included, '
                 f'is NO, and the same command typed again tries again.']
        if not common.owner_says_yes(lines, ask, say):
            say('STOPPED: the creation is not finished; nothing more was written.')
            return EXIT_STOPPED
    else:
        say(kit.line())
    fingerprint = common.finish(root, plan, expected, now, release=release,
                                extra={'suite': 'PASSED', 'smoke_cases_failed': 0,
                                       'environment_digest': found['marker'], 'recovery_kit': kit.made})
    say(f'The list of installed files and the log line are written (software fingerprint {fingerprint}); the '
        f'barrier is removed.')
    return EXIT_CREATED


def main(arguments, view, say=print, ask=input, now=None) -> int:
    """The command line of Init_Tree.bat.

    arguments: ['QA'] or ['PROD'].  view: DEV's settings (research.settings.read_dev_view).
    say, ask: print a line, read the owner's answer.  now: gives the present time (UTC).
    Returns the exit code (see the constants).
    """
    now = now or (lambda: datetime.now(timezone.utc))
    if len(arguments) != 1:
        say(USAGE)
        return EXIT_REFUSED
    began = False
    try:
        entry = entry_for(view, arguments[0])
        role, root, dev_root = entry.role, entry.tree_root, view.own.tree_root
        say(f'INIT TREE - START - the {role} tree at {root}, from DEV at {dev_root}')
        copy_from = view.entries['PROD'].tree_root if role == 'QA' and 'PROD' in view.entries else None
        wanted_settings = settings_bytes(entry, copy_from)
        plan, infrastructure = make_creation_plan(dev_root, entry, say)
        begun = common.read_barrier(root)
        if begun is not None and begun.get('operation') == common.INIT and begun.get('statement'):
            source = begun['statement']                  # a creation being continued: the source it was begun with
        else:
            chosen_root, chosen_role = results_source(view, role)
            source = {'results_copied_from': str(chosen_root), 'results_copied_from_role': chosen_role}
        plan = dict(plan, statement=source)
        source_root, source_role = Path(source['results_copied_from']), source['results_copied_from_role']
        state = target_state(entry, plan, wanted_settings)
        if not (root / INIT_RECORD_PATH).exists():           # with its record, a creation reads no source again
            check_source_may_be_read(view, source_root, source_role)
            results_files(source_root)
        if state == NEW:
            say(f'The accepted results will be copied from the {source_role} tree at {source_root}.')
            if not common.owner_says_yes([f'Type {common.YES} to create the {role} tree at {root} with this plan. '
                                          f'Anything else, Enter included, is NO.'], ask, say):
                say('INIT TREE - END - NO: nothing was created.')
                return EXIT_REFUSED
        else:
            say('This same creation was begun before and is being continued; files already in place are passed over.')
        process_rule.check_no_other_process_of_tree(root)
        settings = TreeSettings(role=role, tree_root=root, venv_dir=entry.venv_dir, backup_root=entry.backup_root,
                                results_copy_from=copy_from)
        started = now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        root.mkdir(parents=True, exist_ok=True)
        with common.reserved(settings, f'Init_Tree {role}', started, say):
            settings_file = root / SETTINGS_FILE_NAME
            if not settings_file.exists():
                with open(settings_file, 'xb') as handle:
                    handle.write(wanted_settings)
            if tree_as_dev_names_it(view, role) != settings:
                raise common.InstallRefused(f'{settings_file} does not read back as DEV\'s entry [{role}].')
            with common.changing(settings, plan, started) as release:
                began = True
                common.carry_out(dev_root, root, plan, say)
                created = common.create_status_files(root, plan)
                say(f'Status files: {created} created as ACTIVE; {len(plan["variants"]) - created} already there.')
                copy_results(view, source_root, source_role, plan, now, say)
                if not (entry.venv_dir / common.PROGRAMS_FOLDER / 'python.exe').is_file():
                    say(f'INIT TREE - PAUSED - the {role} tree\'s software and results are in place. NOW BUILD ITS '
                        f'PYTHON ENVIRONMENT: in {root} run create_venv.bat, then '
                        f'install_upgrade_dependencies_into_venv.bat. Then type this same command again: '
                        f'Init_Tree.bat {role}. Until it finishes, no command works in that tree.')
                    return EXIT_BUILD_THE_ENVIRONMENT
                exit_code = verify_and_finish(view, settings, plan, infrastructure, release, now, say, ask)
        if exit_code != EXIT_CREATED:
            say(f'INIT TREE - END - not finished. {root / common.BARRIER_PATH} stays in place, so no command works in '
                f'that tree. Correct what is named above and type the same command again.')
            return exit_code
        say('The first backup is attempted (every file is read three times; it can take several minutes).')
        say(snapshot.attempt_snapshot(settings, 'INIT', now).line())
        say(f'INIT TREE - END - the {role} tree at {root} is created. Its first research job, Run_Research.bat in '
            f'that tree, fills the history of its variants.')
        return EXIT_CREATED
    except (SettingsRefused, LaunchRefused, common.InstallRefused, installed_files.InstalledFilesRefused,
            StatusRefused, OSError) as refusal:
        say(f'{"STOPPED" if began else "REFUSED"}: {refusal}')
        if began:
            say('INIT TREE - END - not finished. The barrier stays in place, so no command works in that tree. '
                'Correct what is named above and type the same command again.')
            return EXIT_STOPPED
        say('INIT TREE - END - refused. No file of the tree\'s software was written.')
        return EXIT_REFUSED
