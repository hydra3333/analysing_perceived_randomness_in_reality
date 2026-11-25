"""Install.bat QA|PROD [--only <family>/<variant> ...]: add ready variants to a tree (run from DEV).

What this file is for
    Installing is adding: every variant of DEV that is marked ready and that the target does not hold, with the
    helper files the target lacks. Nothing installed is ever changed by it. The command shows what it would add
    and what it leaves out, each with its reason; attempts a recovery kit and a backup; asks once, telling both
    results exactly; reserves the target; copies; checks the whole tree's software against the old list and the
    plan; makes each new variant forecast once with the tree's own Python, recomputes the fixed sample of stored
    forecasts and compares every stored score and prevailing line; writes the list of installed files and the
    log line; removes its barrier last; and attempts a backup again. It is the same code for QA and for PROD.

    An install that stopped after its barrier was written is finished by the same command typed again, with DEV
    as it was. Installation is release: the owner's next research job in the tree fills the new variants'
    history.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 5 (its eleven steps) and sections 3 and 8;
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 12.1 to 12.3 and 12.6.

Which of the project's own modules it uses
    install_common (deploy/)      the plan, the barrier, the copying, the rollback point, the checks, the ending
    research.installed_files      InstalledFilesRefused, differences, read_list
    research.job_lock             LaunchRefused
    research.settings             SettingsRefused, tree_as_dev_names_it
    research.snapshot             attempt_snapshot
    research.status_file          StatusRefused

What uses it
    deploy/deploy_command.py (Install.bat), and the tests.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import install_common as common
from research import installed_files, snapshot
from research.job_lock import LaunchRefused
from research.settings import SettingsRefused, tree_as_dev_names_it
from research.status_file import StatusRefused

# The exit codes: installed, or nothing to add; a check failed or a fault stopped it, with the barrier in place;
# the command refused, or the owner answered NO, and the target's software is as it was.
EXIT_INSTALLED, EXIT_STOPPED, EXIT_REFUSED = 0, 1, 2
ALREADY, ALREADY_OTHER = 'already installed', ('already installed with different bytes (an install leaves it alone: '
                                              'changed work needs a new variant name)')


def list_before(current: dict, unfinished: dict | None) -> dict:
    """The target's list of installed files as it was before an unfinished install began.

    current: the list on file.  unfinished: the plan in the target's barrier, or None.
    An install writes the list just before it removes its barrier; if it stopped between the two, the list on
    file already holds what the barrier's plan added. Those entries are taken out again here, so that the plan
    worked out now is the plan in the barrier and the install can be finished.
    """
    if unfinished is None or unfinished.get('operation') != common.INSTALL:
        return current
    added = {(entry['path'], entry['sha256']) for entry in unfinished['add']}
    arrived = {(entry['family'], entry['variant'], entry['fingerprint']) for entry in unfinished['variants']}
    names = {f'{installed_files.METHODS_FOLDER}/{family}/{variant}/{common.STATUS_FILE_NAME}'
             for family, variant, _ in arrived}
    return {'kind': current['kind'],
            'files': [entry for entry in current['files'] if (entry['path'], entry['sha256']) not in added],
            'variants': [entry for entry in current['variants']
                         if (entry['family'], entry['variant'], entry['fingerprint']) not in arrived],
            'status_files': [path for path in current['status_files'] if path not in names]}


def make_install_plan(dev_root: Path, settings, before: dict, only, say=print) -> dict | None:
    """The plan of an install (deployment design section 5, step 1), shown as it is worked out.

    before: the target's list of installed files.  only: None, or the identities the owner named.
    Returns the plan, or None when there is nothing to add.
    Refuses (InstallRefused): a name after --only that is no variant folder of DEV; a helper that a variant to
    add lists and that the target holds with other bytes.
    """
    ready, not_ready = common.dev_variants(dev_root)
    unknown = sorted(set(only or ()) - set(ready) - set(not_ready))
    if unknown:
        raise common.InstallRefused(f'--only names {", ".join(unknown)}, which is no variant folder of DEV. Give '
                                    f'each as <family>/<variant>, for example E_002/RECUR_MEAN_ALL_V1.')
    installed = {f'{entry["family"]}/{entry["variant"]}': entry['fingerprint'] for entry in before['variants']}
    held = {entry['path']: entry['sha256'] for entry in before['files']}
    wanted = [identity for identity in sorted(set(ready) | set(not_ready)) if only is None or identity in only]
    to_add, left_out = [], {}
    for identity in wanted:
        if identity in installed and identity in ready:
            left_out[identity] = ALREADY if installed[identity] == ready[identity]['fingerprint'] else ALREADY_OTHER
        elif identity in ready:
            to_add.append(ready[identity])
        else:
            left_out[identity] = not_ready[identity]
    add, conflicts = {}, {}
    for entry in to_add:
        for path, digest in entry['files'].items():
            if path not in held:
                add[path] = digest
            elif held[path] != digest:
                conflicts.setdefault(path, []).append(f'{entry["family"]}/{entry["variant"]}')
    if conflicts:
        lines = '\n  '.join(f'{path} (listed by {", ".join(names)})' for path, names in sorted(conflicts.items()))
        raise common.InstallRefused(
            f'the {settings.role} tree holds {len(conflicts)} helper file(s) with other bytes than DEV\'s, and no '
            f'install overwrites a helper:\n  {lines}\nA changed idea needs successor variants that list a new '
            f'helper file (Who_Uses.bat, Make_Successors.bat); a defect in a helper is corrected by '
            f'Correct_Shared_Code.bat. The other variants can be installed now by naming them after --only. '
            f'Nothing was changed.')
    if only is not None:
        say(f'Narrowed by --only to {len(wanted)} variant(s).')
    for identity, reason in sorted(left_out.items()):
        say(f'  left out: {identity}: {reason}' if reason in (ALREADY, ALREADY_OTHER) else f'  left out: {reason}')
    if not to_add:
        return None
    plan = common.make_plan(common.INSTALL, settings.role, settings.tree_root, add, variants=to_add)
    for line in common.plan_lines(plan):
        say(line)
    return plan


def check_and_finish(view, settings, plan: dict, expected: dict, release, now, say) -> int:
    """Steps 8 to 10 of an install, made while the target is reserved and its barrier is in place.

    Returns EXIT_INSTALLED, or EXIT_STOPPED with the barrier left in place and the reason said.
    """
    dev_root, root = view.own.tree_root, settings.tree_root
    faults = common.software_differences(root, expected) + common.status_file_faults(root)
    if faults:
        say(f'STOPPED: the tree\'s software is not the old list and the plan together ({len(faults)} finding(s)):')
        for fault in faults:
            say(f'  {fault}')
        return EXIT_STOPPED
    say(f'The tree\'s software is exactly the old list and the plan: {len(expected["files"])} files, '
        f'{len(expected["variants"])} variant(s), each with its status file, and nothing else under src.')
    python = common.target_python(settings)
    dev_files = common.dev_infrastructure_bytes(dev_root)
    if dev_files is None:
        suite, line = None, ('The test suite: not run. DEV\'s infrastructure manifest cannot be read as one, so its '
                             'tests cannot be said to be the tests of this tree\'s software.')
    else:
        suite, line = common.suite_if_it_is_the_trees(dev_root, dev_files, expected, python, say)
    say(line)
    if suite is False:
        say('STOPPED: the suite failed with the tree\'s own Python.')
        return EXIT_STOPPED
    new = [f'{entry["family"]}/{entry["variant"]}' for entry in plan['variants']]
    say(f'The checks with the tree\'s own Python: the smoke case of each of the {len(new)} new variant(s); the fixed '
        f'sample of stored forecasts; every stored score and prevailing line.')
    found = common.checks_with_target_python(python, root, root, new, True, True, say)
    stopping = common.faults_that_stop(found)
    if stopping:
        say(f'STOPPED: {len(stopping)} finding(s) of the checks stop the install:')
        for fault in stopping:
            say(f'  {fault}')
        return EXIT_STOPPED
    fingerprint = common.finish(root, plan, expected, now, release=release,
                                extra={'suite': {True: 'PASSED', None: 'NOT RUN'}[suite],
                                       'sample_compared': found['sample']['compared']})
    say(f'The list of installed files and the log line are written (software fingerprint {fingerprint}); the '
        f'barrier is removed.')
    return EXIT_INSTALLED


def main(arguments, view, say=print, ask=input, now=None) -> int:
    """The command line of Install.bat.

    arguments: for example ['PROD'] or ['QA', '--only', 'E_002/RECUR_MEAN_ALL_V1', 'E_002/RECUR_MEDIAN_ALL_V1'].
    view: DEV's settings (research.settings.read_dev_view).  say, ask: print a line, read the owner's answer.
    now: gives the present time (UTC).  Returns the exit code (see the constants).
    """
    now = now or (lambda: datetime.now(timezone.utc))
    parser = argparse.ArgumentParser(prog='Install.bat', description='Add ready variants to the QA or PROD tree '
                                                                     '(specification 12; deployment design 5).')
    parser.add_argument('role', metavar='QA|PROD')
    parser.add_argument('--only', nargs='+', metavar='<family>/<variant>',
                        help='install only these of the ready variants')
    chosen = parser.parse_args(arguments)
    began = False
    try:
        settings = tree_as_dev_names_it(view, chosen.role)
        role, root, dev_root = settings.role, settings.tree_root, view.own.tree_root
        say(f'INSTALL - START - into the {role} tree at {root}, from DEV at {dev_root}')
        unfinished = common.read_barrier(root)
        current = installed_files.read_list(root)
        before = list_before(current, unfinished)
        plan = make_install_plan(dev_root, settings, before, chosen.only, say)
        if plan is None and unfinished is None:
            say('INSTALL - END - nothing to add: every ready variant named is installed already. The target was '
                'not touched.')
            return EXIT_INSTALLED
        if plan is None:
            plan = common.make_plan(common.INSTALL, role, root, {})
        continuing = common.check_barrier(root, plan)
        expected = common.expected_list(before, plan)
        started = now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        if continuing:
            say('This same install was begun before and is being continued; files already in place are passed '
                'over, and every check is made again. No new backup is attempted and nothing is asked again.')
        else:
            drift = installed_files.differences(root, current)
            if drift:
                raise common.InstallRefused(
                    f'the {role} tree\'s software does not match its own list of installed files '
                    f'({len(drift)} difference(s)):\n  ' + '\n  '.join(drift) + f'\n{installed_files.WHAT_TO_DO}')
            with common.reserved(settings, f'Install {role}: a look before the backup', started, say):
                pass
            kit, backup = common.attempt_rollback_point(dev_root, settings, 'PRE_INSTALL', expected, now, say)
            if not common.owner_says_yes(common.question_lines(kit, backup), ask, say):
                say('INSTALL - END - NO: the target\'s software was not touched. (A backup, a recovery kit and their '
                    'log lines may have been written, as said above.)')
                return EXIT_REFUSED
        with common.reserved(settings, f'Install {role}', started, say):
            if common.check_barrier(root, plan) != continuing or (not continuing and (
                    installed_files.read_list(root) != current or installed_files.differences(root, current))):
                raise common.InstallRefused(
                    f'the {role} tree\'s installed software, or its record of an unfinished install, changed while '
                    f'the backup was being made or the question stood (another install began or finished, or a '
                    f'file was changed). Nothing was copied. Run the command again: it makes its plan anew.')
            with common.changing(settings, plan, started) as release:
                began = True
                common.carry_out(dev_root, root, plan, say)
                created = common.create_status_files(root, plan)
                say(f'Status files: {created} created as ACTIVE; {len(plan["variants"]) - created} already there.')
                exit_code = check_and_finish(view, settings, plan, expected, release, now, say)
        if exit_code != EXIT_INSTALLED:
            say(f'INSTALL - END - not finished. {root / common.BARRIER_PATH} stays in place, so no job runs in that '
                f'tree. Correct the cause and type the same command again, or restore the tree from a backup you '
                f'choose.')
            return exit_code
        say('A backup is attempted again, now that the install is finished.')
        say(snapshot.attempt_snapshot(settings, 'POST_INSTALL', now).line())
        names = ', '.join(f'{entry["family"]}/{entry["variant"]}' for entry in plan['variants'])
        say(f'INSTALL - END - installed into the {role} tree: {names}. Installation is release: the next '
            f'Run_Research.bat in that tree fills their history.')
        return EXIT_INSTALLED
    except (SettingsRefused, LaunchRefused, common.InstallRefused, installed_files.InstalledFilesRefused,
            StatusRefused, OSError) as refusal:
        say(f'{"STOPPED" if began else "REFUSED"}: {refusal}')
        if began:
            say('INSTALL - END - not finished. The barrier stays in place, so no job runs in that tree. Correct the '
                'cause and type the same command again, or restore the tree from a backup you choose.')
            return EXIT_STOPPED
        say('INSTALL - END - refused. The target\'s software was not touched.')
        return EXIT_REFUSED
