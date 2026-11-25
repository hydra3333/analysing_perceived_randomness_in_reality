"""Reinstall_Infra.bat QA|PROD [--replace-unfinished]: bring a tree's infrastructure to DEV's (run from DEV).

What this file is for
    Infrastructure is the files on DEV's manifest. This command overwrites installed files, so before the owner
    answers it tells him what it would change in the science. It works out the plan (files to add, to overwrite
    and to remove, each with its class, both hashes and the text differences); refuses any plan that touches a
    file that can change a forecast; assembles the software as it would be in a temporary folder and, with the
    target's own Python and the target's own data, read only, runs the suite, compares every stored score and
    prevailing line, and recomputes the fixed sample of stored forecasts; says one of two plain statements;
    attempts a recovery kit and a backup; gives the warning and asks once. Then it reserves the target, writes
    its barrier, carries the plan out, checks the whole tree's software, makes every installed variant forecast
    once, runs the suite in place and compares the derived results again; where a change from a draw was
    foretold and accepted it marks that game's results not current from that draw and moves the stale reports
    out; if report or scoring code changed and the results agree it makes every print-out again; it writes the
    list and the log line, removes its barrier last, attempts a backup again, and names any rerun now owed.

    It never changes code that makes forecasts, never recomputes history and never starts a rerun.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 6 (its eleven steps) and sections 3 and 8;
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 12.4 and 5.8.

Which of the project's own modules it uses
    install_common (deploy/)      the plan, the barrier, the copying, the rollback point, the checks, the ending
    research.code_identity        MANIFEST_PATH
    research.derived_check        MISMATCH, read_cutoff, write_cutoff
    research.environment_marker   MARKER_NAME
    research.installed_files      InstalledFilesRefused, differences, read_list
    research.job_lock             LaunchRefused
    research.reports              set_aside_from
    research.settings             SettingsRefused, tree_as_dev_names_it
    research.snapshot             attempt_snapshot
    research.status_file          StatusRefused

What uses it
    deploy/deploy_command.py (Reinstall_Infra.bat), and the tests.
"""
from __future__ import annotations

import argparse
import configparser
import difflib
import hashlib
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import install_common as common
from research import code_identity, derived_check, installed_files, reports, snapshot
from research.environment_marker import MARKER_NAME
from research.job_lock import LaunchRefused
from research.settings import SettingsRefused, tree_as_dev_names_it
from research.status_file import StatusRefused

# The exit codes: the infrastructure is DEV's (reinstalled, or it was already); a check failed or a fault stopped
# it, with the barrier in place; the command refused, or the owner answered NO, and nothing was overwritten.
EXIT_REINSTALLED, EXIT_STOPPED, EXIT_REFUSED = 0, 1, 2
# A path that belongs to variants and their helpers: under a family folder, or under _shared. No such path is
# ever in an infrastructure plan (deployment design section 6, step 1).
VARIANTS_PATH = re.compile(r'src/methods/(E_\d{3}|_shared)/')
# The three classes of the manifest, and the word used here for the manifest file itself.
FORECAST, DERIVED, OTHER, MANIFEST_ITSELF = 'forecast', 'derived', 'other', 'the manifest'
# The first of the two statements of step 3.
NO_CHANGE = 'No stored result changes.'
# What the statement of step 3 rests on in the tree, besides four named files: these folders, without Python's
# caches and without the reports folders (print-outs, made again from the lists).
WATCHED_FOLDERS = ('src', 'source_data', 'results/research')
NOT_WATCHED = ('__pycache__', 'reports')
# The start of the name of the temporary folder the software as it would be is assembled in.
ASSEMBLY_PREFIX = 'a_p_r_i_r_as_it_would_be_'
# The warning of specification 12.4, said before the one question.
WARNING = ('This overwrites installed system files in {role} {root}. Make sure you hold a valid backup. If the '
           'overwrite fails, the way back is a manual restore of the whole tree from a backup you choose: there is no '
           'automatic rollback. A restore puts back exactly that backup: its software, variants, status files, '
           'results and Python environment. Anything installed, withdrawn or upgraded after it is not put back; you '
           'then run the research job to catch up. If Python, the environment or its packages have changed since '
           'that backup, the restored tree may not run, or may not give identical results. With no valid backup, '
           'recovery may not be possible.')


def infrastructure_on_list(current: dict) -> dict:
    """The infrastructure a tree's list of installed files holds: every listed file that is not under a family
    folder or _shared, as {path: sha256}."""
    return {entry['path']: entry['sha256'] for entry in current['files'] if not VARIANTS_PATH.match(entry['path'])}


def expected_after(current: dict, dev_files: dict) -> dict:
    """The list of installed files a tree must have once its infrastructure is DEV's: its variants, helpers and
    status files as they are listed now, and DEV's infrastructure files.

    current: the tree's list.  dev_files: install_common.dev_infrastructure()['files'].
    It does not depend on the plan, so it is the same whether the reinstall is new, continued or replaces an
    unfinished one.
    """
    files = {entry['path']: entry['sha256'] for entry in current['files'] if VARIANTS_PATH.match(entry['path'])}
    files.update(dev_files)
    return {'kind': current['kind'], 'files': [{'path': path, 'sha256': files[path]} for path in sorted(files)],
            'variants': current['variants'], 'status_files': current['status_files']}


def classes_in_tree(tree_root: Path) -> dict:
    """The class each file has on the manifest that lies in the tree now, as {path: class}; read leniently (the
    files it lists need not all exist while a reinstall is unfinished). Empty if there is no readable manifest."""
    parser = configparser.ConfigParser(delimiters=('=',), interpolation=None, strict=False)
    parser.optionxform = str
    try:
        parser.read_string((Path(tree_root) / code_identity.MANIFEST_PATH).read_text(encoding='ascii'))
        return {path: parser.get('files', path).strip() for path in parser.options('files')}
    except (OSError, UnicodeError, configparser.Error):
        return {}


def _sha256(path: Path) -> str | None:
    """The SHA-256 of a file, or None if no ordinary file lies there."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def changes_between(held: dict, dev_files: dict) -> tuple:
    """What brings a set of infrastructure files to DEV's: (add, overwrite, remove) as install_common.make_plan
    takes them. held: {path: sha256, or None for a path with no file}."""
    add = {path: digest for path, digest in dev_files.items() if held.get(path) is None}
    overwrite = {path: (held[path], digest) for path, digest in dev_files.items()
                 if held.get(path) is not None and held[path] != digest}
    remove = {path: digest for path, digest in held.items() if digest is not None and path not in dev_files}
    return add, overwrite, remove


def check_plan_may_be_carried_out(plan: dict, classes: dict, in_tree: dict, in_dev: dict) -> None:
    """Refuse a plan this command never carries out (deployment design section 6, step 1).

    classes: {path: class} for every path of the plan, from DEV's manifest and the tree's.
    in_tree, in_dev: {path: class} of the manifest that lies in the tree and of DEV's.
    Refuses (InstallRefused): a path under a family folder or _shared; any file of class forecast, added,
    overwritten or removed; a path whose class is not known; and two manifests that do not class the same files
    as forecast (the identity of the forecasting code is taken over exactly those files, so a file moved into or
    out of that class changes it although no such file's bytes change).
    """
    paths = [entry['path'] for word in ('add', 'overwrite', 'remove') for entry in plan[word]]
    belonging = [path for path in paths if VARIANTS_PATH.match(path)]
    if belonging:
        raise common.InstallRefused(f'the plan holds {len(belonging)} path(s) under a family folder or _shared, which '
                                    f'belong to variants and are never infrastructure: {", ".join(belonging)}. '
                                    f'Correct DEV\'s manifest. Nothing was changed.')
    unknown = [path for path in paths if path not in classes]
    if unknown:
        raise common.InstallRefused(f'the class of {", ".join(unknown)} is not known (it is on neither DEV\'s manifest '
                                    f'nor the tree\'s). Nothing was changed.')
    forecasting = [path for path in paths if classes[path] == FORECAST]
    if forecasting:
        raise common.InstallRefused(
            f'this changes code that makes forecasts; that is a correction of shared code: Correct_Shared_Code.bat. '
            f'The plan would add, overwrite or remove {len(forecasting)} file(s) of class forecast: '
            f'{", ".join(forecasting)}. Reinstall_Infra never changes forecasting code. Nothing was changed.')
    reclassed = sorted({path for path, kind in in_tree.items() if kind == FORECAST}
                       ^ {path for path, kind in in_dev.items() if kind == FORECAST})
    if reclassed:
        raise common.InstallRefused(
            f'this changes code that makes forecasts; that is a correction of shared code: Correct_Shared_Code.bat. '
            f'DEV\'s manifest and the tree\'s do not class the same files as forecast (they differ on '
            f'{", ".join(reclassed)}), and the identity of the forecasting code is taken over exactly those files. '
            f'Nothing was changed.')


def show_plan(plan: dict, classes: dict, dev_root: Path, tree_root: Path, say=print) -> None:
    """Show every file the plan would add, overwrite or remove, with its class, both hashes and, for a text file
    that is overwritten, the differences (specification 12.4)."""
    say(f'The plan (REINSTALL_INFRA into the {plan["role"]} tree at {plan["tree_root"]}): {len(plan["add"])} '
        f'file(s) to add, {len(plan["overwrite"])} to overwrite, {len(plan["remove"])} to remove.')
    for entry in plan['add']:
        say(f'  add: {entry["path"]} (class {classes[entry["path"]]}; {entry["sha256"]})')
    for entry in plan['remove']:
        say(f'  remove: {entry["path"]} (class {classes[entry["path"]]}; now {entry["was"]})')
    for entry in plan['overwrite']:
        say(f'  overwrite: {entry["path"]} (class {classes[entry["path"]]}; now {entry["was"]}; to be '
            f'{entry["sha256"]})')
        try:
            old = (Path(tree_root) / entry['path']).read_bytes().decode('utf-8').splitlines()
            new = (Path(dev_root) / entry['path']).read_bytes().decode('utf-8').splitlines()
        except (OSError, UnicodeError):
            say('      (not a text file that can be read: its differences are not shown)')
            continue
        for line in difflib.unified_diff(old, new, 'installed', 'DEV', lineterm='', n=1):
            say(f'      {line}')


def assemble(dev_root: Path, tree_root: Path, expected: dict, dev_files: dict, folder: Path) -> None:
    """Assemble the software as it would be in an empty folder: DEV's infrastructure, and the tree's own variants,
    helpers and status files, each file checked against the hash expected of it. Nothing in the tree is written."""
    for entry in expected['files']:
        source_root = dev_root if entry['path'] in dev_files else tree_root
        common.copy_into_place(Path(source_root) / entry['path'], folder, entry['path'], entry['sha256'])
    for path in expected['status_files']:
        (Path(folder) / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(tree_root) / path, Path(folder) / path)


def statement_of(found: dict) -> dict:
    """The statement of step 3, from what the comparison of the derived results found.

    found: the result of the checks (research.tree_checks.run_checks).
    Returns {'text': one of the two plain statements, 'not_current_from': {game: X}, 'detail': {game: what was
    found}}, for example
        {'text': 'This changes stored scores or OV-1 lines, for POWERBALL from draw 1601. It is a scientific ...',
         'not_current_from': {'POWERBALL': 1601}, 'detail': {'POWERBALL': 'the score of ... for draw 1601 ...'}}
    A game the tree already marks not current from that draw or an earlier one is not a change of this
    reinstall; it is named so in the text.
    """
    new = {game: answer for game, answer in sorted(found['derived'].items()) if answer and not answer['known']}
    old = {game: answer for game, answer in sorted(found['derived'].items()) if answer and answer['known']}
    if new:
        where = '; and for '.join(f'{game} from draw {answer["from_draw"]}' for game, answer in new.items())
        text = (f'This changes stored scores or OV-1 lines, for {where}. It is a scientific correction to derived '
                f'results. Stored forecasts are not affected. If you install it, those scores, reports and the '
                f'prevailing line will be not current from that draw until you run the derived-only rerun.')
    else:
        text = NO_CHANGE
    for game in old:
        text += f' ({game}\'s results are already marked not current in this tree; that stands.)'
    return {'text': text, 'not_current_from': {game: answer['from_draw'] for game, answer in new.items()},
            'detail': {game: answer['detail'] for game, answer in new.items()}}


def what_it_would_change(view, settings, expected: dict, dev: dict, say=print) -> dict:
    """Step 3: what the reinstall would change, found before anything is overwritten, with the target's Python,
    reading the target's data and writing nothing in the tree.

    Returns the statement (statement_of). Refuses (InstallRefused), nothing having been overwritten: a suite
    that fails; stored records that cannot be read; a difference in the forecast sample (no forecasting code is
    in the plan, so a file is wrongly classed).
    """
    dev_root, root = view.own.tree_root, settings.tree_root
    python = common.target_python(settings)
    say('What it would change, found before anything is overwritten:')
    passed, line = common.suite_if_it_is_the_trees(dev_root, dev['files'], expected, python, say)
    say(line)
    if passed is not True:
        raise common.InstallRefused('the suite does not pass with the target\'s Python on the software as it would '
                                    'be. Nothing was overwritten.')
    folder = Path(tempfile.mkdtemp(prefix=ASSEMBLY_PREFIX)).resolve()
    try:
        assemble(dev_root, root, expected, dev['files'], folder)
        say(f'The software as it would be is assembled in {folder}; every stored score and prevailing line is '
            f'compared, and the fixed sample of stored forecasts is computed again.')
        found = common.checks_with_target_python(python, folder, root, common.NO_VARIANT, True, True, say)
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    if found['unreadable']:
        raise common.InstallRefused('stored records could not be read, so what the reinstall would change is not '
                                    'known: ' + '; '.join(f'{game}: {why}' for game, why in
                                                          sorted(found['unreadable'].items()))
                                    + '. Nothing was overwritten.')
    if found['sample']['differences']:
        raise common.InstallRefused(
            'the fixed sample of stored forecasts does not come out the same with the software as it would be. No '
            'forecasting code is in the plan, so a file is wrongly classed on the manifest. The forecasts that '
            'differ:\n  ' + '\n  '.join(found['sample']['differences']) + '\nNothing was overwritten.')
    return statement_of(found)


def what_the_statement_rests_on(settings, dev_fingerprint: str) -> str:
    """One SHA-256 over everything the statement of step 3, and so the owner's answer, rests on.

    settings: the target's settings.  dev_fingerprint: the fingerprint of DEV's infrastructure, read now.
    It covers DEV's fingerprint and, in the tree: every file under src (the status files among them); the
    manifest; the list of installed files; the barrier, if one lies there; the accepted results; the stored
    research (every list, the prevailing ledger, the not-current markers; the reports are print-outs and are
    left out); and the marker of the verified environment. Taken while the lock is held for step 3, and again
    under the second hold before anything is written (design section 6, step 6; EX_329 C-B01): equal values mean
    that no job, install, withdrawal, results update or change of environment came between.
    """
    root = settings.tree_root
    paths = [root / code_identity.MANIFEST_PATH, root / installed_files.LIST_PATH, root / common.BARRIER_PATH,
             settings.venv_dir / MARKER_NAME]

    def stop(error: OSError) -> None:
        raise common.InstallRefused(f'a folder of the tree could not be listed ({error}). Nothing was overwritten.')

    for folder in WATCHED_FOLDERS:
        for current, folders, names in os.walk(root / folder, onerror=stop):
            folders[:] = [name for name in folders if name not in NOT_WATCHED]
            paths += [Path(current) / name for name in names]
    digest = hashlib.sha256(f'DEV\t{dev_fingerprint}\n'.encode('ascii'))
    for path in sorted(paths):
        line = f'{path.relative_to(root).as_posix()}\t{_sha256(path) or "no file"}\n'
        digest.update(line.encode('utf-8'))
    return digest.hexdigest()


def mark_not_current(tree_root: Path, statement: dict, say=print) -> list:
    """Step 9, where a change from a draw was foretold and accepted: write the game's cutoff file for that draw,
    move the stale reports out, and check that both were done (specification 5.8).

    Returns the faults found by the check; empty when each game is marked from its draw (or an earlier one, if
    the tree already marked one) and no report for that draw or a later one is left in view.
    """
    faults = []
    for game_id, draw in sorted(statement['not_current_from'].items()):
        marked = derived_check.read_cutoff(tree_root, game_id)
        if not (marked is not None and marked[1] == derived_check.MISMATCH and marked[0] <= draw):
            derived_check.write_cutoff(tree_root, game_id, draw, derived_check.MISMATCH, statement['detail'][game_id])
        moved = reports.set_aside_from(tree_root, game_id, draw)
        marked = derived_check.read_cutoff(tree_root, game_id)
        if marked is None or marked[1] != derived_check.MISMATCH or marked[0] > draw:
            faults.append(f'{game_id}: its results are not marked not current from draw {draw}')
        if reports.set_aside_from(tree_root, game_id, draw):
            faults.append(f'{game_id}: a report for draw {draw} or a later one was still in view')
        say(f'  {game_id}: marked not current from draw {draw}, as was foretold and accepted; {moved} stale report '
            f'file(s) moved to reports/not_current.')
    return faults


def check_in_place_and_finish(view, settings, plan: dict, expected: dict, dev: dict, release, now, say) -> int:
    """Steps 8 to 10, made while the target is reserved and its barrier is in place.

    Returns EXIT_REINSTALLED, or EXIT_STOPPED with the barrier left in place and the reason said.
    """
    dev_root, root = view.own.tree_root, settings.tree_root
    faults = common.software_differences(root, expected) + common.status_file_faults(root)
    if faults:
        say(f'STOPPED: the tree\'s software is not the old list changed by the plan ({len(faults)} finding(s)):')
        for fault in faults:
            say(f'  {fault}')
        return EXIT_STOPPED
    say(f'The tree\'s software is exactly the old list changed by the plan: {len(expected["files"])} files.')
    faults = mark_not_current(root, plan['statement'], say)
    if faults:
        say('STOPPED: ' + '; '.join(faults) + '.')
        return EXIT_STOPPED
    python = common.target_python(settings)
    passed, line = common.suite_if_it_is_the_trees(dev_root, dev['files'], expected, python, say)
    say(line)
    if passed is not True:
        say('STOPPED: the suite does not pass in place with the tree\'s own Python.')
        return EXIT_STOPPED
    say('In place, with the tree\'s own Python: every installed variant\'s smoke case; the fixed sample of stored '
        'forecasts; every stored score and prevailing line.')
    found = common.checks_with_target_python(python, root, root, common.ALL_VARIANTS, True, True, say)
    stopping = common.faults_that_stop(found)
    if stopping:
        say(f'STOPPED: {len(stopping)} finding(s) in place. Nothing is reported as agreeing that does not agree:')
        for fault in stopping:
            say(f'  {fault}')
        return EXIT_STOPPED
    if plan.get('reports_owed', True):
        say('Report or scoring code changed: every league report, next-draw report and OV-1 print-out is made '
            'again with the new code.')
        common.reports_with_target_python(python, root, say)
    fingerprint = common.finish(root, plan, expected, now, release=release, extra={'suite': 'PASSED'})
    say(f'The list of installed files and the log line are written (software fingerprint {fingerprint}); the '
        f'barrier is removed.')
    return EXIT_REINSTALLED


def main(arguments, view, say=print, ask=input, now=None) -> int:
    """The command line of Reinstall_Infra.bat.

    arguments: ['PROD'], ['QA'] or ['PROD', '--replace-unfinished'].  view: DEV's settings.
    say, ask: print a line, read the owner's answer.  now: gives the present time (UTC).
    Returns the exit code (see the constants).
    """
    now = now or (lambda: datetime.now(timezone.utc))
    parser = argparse.ArgumentParser(prog='Reinstall_Infra.bat',
                                     description='Bring the infrastructure of the QA or PROD tree to DEV\'s '
                                                 '(specification 12.4; deployment design 6).')
    parser.add_argument('role', metavar='QA|PROD')
    parser.add_argument('--replace-unfinished', action='store_true',
                        help='go on from an unfinished infrastructure reinstall with the plan as DEV is now')
    chosen = parser.parse_args(arguments)
    began = False
    try:
        settings = tree_as_dev_names_it(view, chosen.role)
        role, root, dev_root = settings.role, settings.tree_root, view.own.tree_root
        say(f'REINSTALL INFRA - START - the {role} tree at {root}, from DEV at {dev_root}')
        dev = common.dev_infrastructure(dev_root)
        current = installed_files.read_list(root)
        unfinished = common.read_barrier(root)
        expected = expected_after(current, dev['files'])
        started = now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        # The same command again (design section 8): the barrier holds a reinstall of this tree that was accepted
        # from DEV exactly as DEV is now. Its plan is carried on as it was accepted, whatever of it has already
        # been copied or removed; it was checked when it was accepted, and nothing of DEV has changed since.
        continuing = (unfinished is not None and unfinished.get('operation') == common.REINSTALL_INFRA
                      and unfinished.get('tree_root') == str(root)
                      and unfinished.get('infrastructure_fingerprint') == dev['fingerprint'])
        if continuing:
            plan = unfinished
            say('This same reinstall was begun before and is being continued; files already in place are passed '
                'over and every check is made again. Its statement, accepted then, was: '
                + plan['statement']['text'])
        else:
            replaced = unfinished if (unfinished or {}).get('operation') == common.REINSTALL_INFRA else None
            in_tree = classes_in_tree(root)
            # A class is known from DEV's manifest, from the manifest that lies in the tree, or, for a file an
            # unfinished reinstall was removing, from that reinstall's accepted plan. Any other path is refused.
            classes = {**(replaced or {}).get('classes', {}), **in_tree, **dev['classes'],
                       code_identity.MANIFEST_PATH: MANIFEST_ITSELF}
            by_the_list = common.make_plan(common.REINSTALL_INFRA, role, root,
                                           *changes_between(infrastructure_on_list(current), dev['files']),
                                           infrastructure_fingerprint=dev['fingerprint'])
            if unfinished is None:
                plan = by_the_list
                check_plan_may_be_carried_out(plan, classes, in_tree, dev['classes'])
                if not (plan['add'] or plan['overwrite'] or plan['remove']):
                    say(f'REINSTALL INFRA - END - no difference: the {role} tree\'s infrastructure is file for file '
                        f'DEV\'s. Nothing was done.')
                    return EXIT_REINSTALLED
                drift = installed_files.differences(root, current)
                if drift:
                    raise common.InstallRefused(
                        f'the {role} tree\'s software does not match its own list of installed files '
                        f'({len(drift)} difference(s)):\n  ' + '\n  '.join(drift) + f'\n{installed_files.WHAT_TO_DO}')
            else:
                if not (chosen.replace_unfinished and replaced is not None):
                    try:
                        common.check_barrier(root, by_the_list)
                    except common.InstallRefused as refusal:
                        raise common.InstallRefused(
                            f'{refusal}\nIf the unfinished operation is an infrastructure reinstall whose cause '
                            f'you have corrected in DEV and marked again, Reinstall_Infra.bat {role} '
                            f'--replace-unfinished goes on with the plan now, after the same question.') from None
                    raise common.InstallRefused(f'{root / common.BARRIER_PATH} holds an unfinished operation.')
                paths = set(infrastructure_on_list(current)) | set(dev['files']) | {
                    entry['path'] for word in ('add', 'overwrite', 'remove') for entry in replaced[word]}
                plan = common.make_plan(common.REINSTALL_INFRA, role, root,
                                        *changes_between({path: _sha256(root / path) for path in paths}, dev['files']),
                                        infrastructure_fingerprint=dev['fingerprint'])
                check_plan_may_be_carried_out(plan, classes, in_tree, dev['classes'])
                say('AN UNFINISHED REINSTALL IS BEING REPLACED (--replace-unfinished). THE UNFINISHED PLAN:')
                for line in common.plan_lines(replaced):
                    say(f'  {line}')
                say('THE PLAN NOW, worked out from the files as they lie in the tree:')
            show_plan(plan, classes, dev_root, root, say)
            with common.reserved(settings, f'Reinstall_Infra {role}: what it would change', started, say):
                rested_on = what_the_statement_rests_on(settings, dev['fingerprint'])
                statement = what_it_would_change(view, settings, expected, dev, say)
            changed = [entry['path'] for word in ('add', 'overwrite', 'remove') for entry in plan[word]]
            # Kept in the plan, and so in the barrier, for the command that finishes or replaces this reinstall:
            # the class of each file of the plan, and whether the print-outs are owed a remaking (a file of class
            # derived is in this plan, or was in an unfinished plan this one replaces).
            plan = dict(plan, statement=statement, classes={path: classes[path] for path in changed},
                        reports_owed=bool(any(classes[path] == DERIVED for path in changed)
                                          or (replaced or {}).get('reports_owed', replaced is not None)))
            say(f'THE STATEMENT: {statement["text"]}')
            kit, backup = common.attempt_rollback_point(dev_root, settings, 'PRE_INFRA', expected, now, say)
            lines = [WARNING.format(role=role, root=root)] + common.question_lines(kit, backup)
            if not common.owner_says_yes(lines, ask, say):
                say('REINSTALL INFRA - END - NO: nothing was overwritten. (A backup, a recovery kit and their log '
                    'lines may have been written, as said above.)')
                return EXIT_REFUSED
        with common.reserved(settings, f'Reinstall_Infra {role}', started, say):
            # The target is reserved again (design section 6, step 6). Before anything is written under this hold,
            # what the owner's answer rested on must still be so (EX_329 C-B01).
            if continuing:
                if common.read_barrier(root) != plan:
                    raise common.InstallRefused(f'{root / common.BARRIER_PATH} is no longer the record of the '
                                                f'unfinished reinstall this command read. Nothing was done. Run '
                                                f'the command again.')
            elif what_the_statement_rests_on(settings, common.dev_infrastructure(dev_root)['fingerprint']) != rested_on:
                raise common.InstallRefused(
                    f'something the statement rested on changed while the backup was being made or the question '
                    f'stood: a job ran or results arrived in the {role} tree, an install or a withdrawal was made '
                    f'there, its environment changed, or DEV changed. Nothing was overwritten. Run the command '
                    f'again: it says afresh what it would change.')
            with common.changing(settings, plan, started) as release:
                began = True
                common.carry_out(dev_root, root, plan, say)
                exit_code = check_in_place_and_finish(view, settings, plan, expected, dev, release, now, say)
        if exit_code != EXIT_REINSTALLED:
            say(f'REINSTALL INFRA - END - not finished. {root / common.BARRIER_PATH} stays in place, so no job runs '
                f'in that tree. The ways out: correct the cause in DEV, run Make_Installable.bat INFRA, and run '
                f'Reinstall_Infra.bat {role} --replace-unfinished; or restore the whole tree from a backup you '
                f'choose.')
            return exit_code
        say('A backup is attempted again, now that the reinstall is finished.')
        say(snapshot.attempt_snapshot(settings, 'POST_INFRA', now).line())
        for game_id, draw in sorted(plan['statement']['not_current_from'].items()):
            say(f'YOU NOW OWE {game_id} A RERUN: Rerun_Walk_Forward.bat --game {game_id} --from {draw} '
                f'--derived-only. Until it has run, {game_id}\'s scores, reports and prevailing line are not '
                f'current from draw {draw}; forecasts go on.')
        say(f'REINSTALL INFRA - END - the {role} tree\'s infrastructure is DEV\'s. {plan["statement"]["text"]}')
        return EXIT_REINSTALLED
    except (SettingsRefused, LaunchRefused, common.InstallRefused, installed_files.InstalledFilesRefused,
            StatusRefused, derived_check.CutoffRefused, OSError) as refusal:
        say(f'{"STOPPED" if began else "REFUSED"}: {refusal}')
        if began:
            say('REINSTALL INFRA - END - not finished. The barrier stays in place, so no job runs in that tree. The '
                'ways out: correct the cause in DEV, run Make_Installable.bat INFRA, and run Reinstall_Infra.bat '
                'with --replace-unfinished; or restore the whole tree from a backup you choose.')
            return EXIT_STOPPED
        say('REINSTALL INFRA - END - refused. Nothing was overwritten.')
        return EXIT_REFUSED
