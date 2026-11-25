"""Verify_Tree.bat: is this tree's Python environment one in which this tree's software forecasts?

What this file is for
    A QA or PROD tree's launchers refuse until its Python environment has been verified, and each job compares
    the environment with the one that was verified. After the owner builds or rebuilds a tree's .venv he runs
    Verify_Tree.bat in that tree. It attempts a backup, checks that the software is what was installed, makes
    every installed variant forecast once on an invented table (the smoke case), computes the fixed sample of
    stored forecasts again, compares every stored score and prevailing line, writes the marker
    .venv\\ENVIRONMENT_VERIFIED.json, and attempts a backup again.

    The test suite is not run here (the owner, decision log entry 305): the tests live in DEV, and no file of
    the installed software starts a program. The closing lines say so in capitals every time. The suite is run
    with a tree's own Python by the install tools in DEV, when a tree is created and at every infrastructure
    reinstall.

    One thing withholds the marker and removes an older one: a failed smoke case. A difference in the forecast
    sample or in the derived results is reported in plain words and does not withhold it: after a change of the
    environment such a difference is what the owner's review is for, and the tree's own research job and its
    rerun, which need a verified environment to start at all, are what act on a derived result that is no
    longer current.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 13 ("Verified before use") and 12.3;
    doc/Predictive_Randomness_Deployment_Design_v0_12.md sections 7 and 9; both as the owner decided on 25
    November 2026 that Verify_Tree does not run the suite (an amendment of those two clauses is to be reviewed
    and ratified with build step 3, slice C).

Which of the project's own modules it uses
    research.code_identity       ManifestRefused
    research.environment_marker  MARKER_NAME, write_marker
    research.job_lock            RECORDS_FOLDER, LaunchRefused, check_no_orphan_marker, check_working_folders,
                                 job_lock
    research.launch_guard        INSTALLED_ROLES, check_no_unfinished_operation, check_software_is_as_installed
    research.process_rule        check_no_other_process_of_tree
    research.settings            SettingsRefused, read_settings
    research.snapshot            attempt_snapshot, mark_due
    research.tree_checks         the smoke cases, the forecast sample, the derived results

What uses it
    src/tree_checks_command.py (Verify_Tree.bat), and the tests.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from research import process_rule, tree_checks
from research.code_identity import ManifestRefused
from research.environment_marker import MARKER_NAME, write_marker
from research.job_lock import (RECORDS_FOLDER, LaunchRefused, check_no_orphan_marker, check_working_folders,
                               job_lock)
from research.launch_guard import INSTALLED_ROLES, check_no_unfinished_operation, check_software_is_as_installed
from research.settings import SettingsRefused, read_settings
from research.snapshot import attempt_snapshot, mark_due

# The tree's log of installs, verifications and withdrawals (deployment design section 2).
TREE_LOG_NAME = 'INSTALL_LOG.jsonl'
# What the closing lines say of the test suite, every time.
SUITE_LINE = ('THE TEST SUITE IS NOT RUN BY THIS COMMAND: the tests live in DEV. This verification rests on the smoke '
              'cases, the forecast sample and the derived results. The suite is run with a tree\'s own Python when '
              'the tree is created and at every infrastructure reinstall.')
# The exit codes of Verify_Tree.bat: the marker was written; a smoke case failed and there is no marker; the
# command refused and changed nothing.
EXIT_VERIFIED, EXIT_NOT_VERIFIED, EXIT_REFUSED = 0, 1, 2


def log_verification(settings, outcome: str, digest: str | None, summary: dict, now) -> None:
    """Add one line to the tree's log: that a verification ended, how, and with which environment digest."""
    record = {'operation': 'VERIFICATION', 'time': now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'role': settings.role, 'tree_root': str(settings.tree_root), 'outcome': outcome,
              'environment_digest': digest, **summary}
    path = settings.tree_root / RECORDS_FOLDER / TREE_LOG_NAME
    with open(path, 'a', encoding='ascii', newline='\n') as stream:
        stream.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + '\n')


def verify_locked(settings, now, say) -> tuple:
    """The part of a verification made while the tree's job lock is held.

    Returns (the exit code, the closing lines). Refuses with what the checks it calls refuse; a refusal leaves
    the marker as it was.
    """
    looked_at = process_rule.check_no_other_process_of_tree(settings.tree_root)
    say(f'No other Python process of this tree is running ({looked_at} processes of this PC looked at).')
    check_software_is_as_installed(settings)
    software = tree_checks.read_software(settings.tree_root)
    _, status_refusals = tree_checks.read_statuses(software)
    if status_refusals:
        raise tree_checks.ChecksRefused('a status file fails its own check: ' + '; '.join(
            f'{identity}: {why}' for identity, why in sorted(status_refusals.items())))
    say(f'The structure: the software matches the tree\'s list of installed files; {len(software.variants)} '
        f'variant(s), each with a valid declaration and status file.')
    mark_due(settings)
    marker = settings.venv_dir / MARKER_NAME
    say('The smoke cases: every installed variant is made to forecast once, on an invented table.')
    smoke_failures = tree_checks.smoke_cases(software, settings.tree_root, say=say)
    summary = {'smoke_cases_failed': len(smoke_failures)}
    if smoke_failures:
        marker.unlink(missing_ok=True)
        log_verification(settings, 'NOT_VERIFIED', None, summary, now)
        return EXIT_NOT_VERIFIED, smoke_failures + [
            f'NOT VERIFIED: {marker} was not written, and an older one was removed. No job starts in this tree '
            f'until Verify_Tree.bat passes. Nothing of the research was changed.']
    say('The stored results: read as the research job reads them; nothing is written.')
    stored, unreadable = tree_checks.read_stored_game_by_game(software, settings, say)
    compared, differences = tree_checks.forecast_sample(software, stored, say)
    derived = tree_checks.derived_results(stored, say)
    digest = write_marker(settings.venv_dir)
    changed = sorted(game_id for game_id, answer in derived.items() if answer is not None)
    summary.update(sample_compared=compared, sample_differences=len(differences),
                   derived_not_current=changed, unreadable=sorted(unreadable))
    log_verification(settings, 'VERIFIED', digest, summary, now)
    closing = [SUITE_LINE]
    if differences:
        closing.append(f'THE FORECAST SAMPLE: {len(differences)} of {compared} stored forecast(s) are NOT what this '
                       f'software computes in this environment. This does not withhold the marker; it is for '
                       f'your review of the environment change before any job is run:')
        closing += [f'  {line}' for line in differences]
    for game_id in changed:
        draw, detail, known = derived[game_id]
        closing.append(f'THE DERIVED RESULTS of {game_id} are NOT what this software computes here, from draw '
                       f'{draw}: {detail}. ' + ('The tree already marks them not current.' if known else
                                                'The next research job will mark them not current from that draw '
                                                'and say which rerun is owed.'))
    for game_id, why in sorted(unreadable.items()):
        closing.append(f'{game_id}: its stored records could not be read, so nothing of it was compared; the '
                       f'research job will refuse that game for the same reason: {why}')
    closing.append(f'VERIFIED: {marker} written; the environment\'s digest is {digest}.')
    return EXIT_VERIFIED, closing


def verify_tree(tree_root: Path, now=None, say=print) -> int:
    """Verify the tree's Python environment (deployment design section 7), in its order.

    tree_root: the tree the launcher lies in.  now: gives the present time (UTC); a test passes a fixed one.
    Returns EXIT_VERIFIED, EXIT_NOT_VERIFIED or EXIT_REFUSED.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    try:
        settings = read_settings(Path(tree_root))
        if settings.role not in INSTALLED_ROLES:
            raise LaunchRefused('this is the DEV tree. DEV has no verified-environment marker and its launchers '
                                'ask for none; there is nothing to verify here.')
        check_no_unfinished_operation(settings.tree_root)
        check_no_orphan_marker(settings.tree_root)
        check_working_folders(settings.tree_root)
        process_rule.check_no_other_process_of_tree(settings.tree_root)
    except (SettingsRefused, LaunchRefused) as refusal:
        say(f'REFUSED: {refusal}')
        say('VERIFY TREE - END - refused; nothing was changed.')
        return EXIT_REFUSED
    started = now().astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    say(f'VERIFY TREE - START - the {settings.role} tree at {settings.tree_root}, its environment {settings.venv_dir}')
    say('A backup is attempted first (every file is read three times; it can take several minutes).')
    say(attempt_snapshot(settings, 'PRE_VERIFY', now).line())
    try:
        with job_lock(settings.tree_root, 'verify tree', started):
            exit_code, closing = verify_locked(settings, now, say)
    except (SettingsRefused, LaunchRefused, tree_checks.ChecksRefused, ManifestRefused) as refusal:
        say(f'REFUSED: {refusal}')
        say('VERIFY TREE - END - refused; the environment\'s marker is as it was.')
        return EXIT_REFUSED
    say('A backup is attempted again, now that the tree is verified or not.')
    say(attempt_snapshot(settings, 'POST_VERIFY', now).line())
    say(f'VERIFY TREE - END - the {settings.role} tree at {settings.tree_root}')
    for line in closing:
        say(line)
    return exit_code


def main(arguments, tree_root: Path, say=print) -> int:
    """The command line of Verify_Tree.bat.

    arguments: none.  tree_root: the tree the launcher lies in.  Returns the exit code.
    """
    argparse.ArgumentParser(prog='Verify_Tree.bat', description='Verify this tree\'s Python environment '
                                                                '(specification 13).').parse_args(arguments)
    return verify_tree(Path(tree_root), say=say)
