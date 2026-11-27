"""DEV's commands that put software into another tree: "create tree" and "install".

What this file is for
    Create_Tree.bat QA|PROD
        makes a new tree in a folder that is absent or empty: copies DEV's flagged software (the infrastructure
        and every method that is flagged and not retired) and DEV's accepted results, and writes the new tree's
        settings file last, so that a half-made folder is not a tree and runs nothing. The owner then builds
        the new tree's Python environment and runs its research job.
    Install.bat QA|PROD [--show]
        works out what differs between DEV's flagged software and the destination's (the plan), backs the
        destination up, replaces the infrastructure if it is flagged and differs, replaces or adds every flagged
        method that differs or is missing, and then runs the destination's own research job (results updater
        left out) under the lock it already holds; that job makes again whatever the new software changes.
        A method the destination has and DEV does not is left alone. --show prints the plan and changes nothing.

    A flag (I_AM_INSTALLABLE) that is missing or older than its files installs nothing: the part is named and
    left alone. A helper file several methods share is brought only if every method of the destination that
    uses it is installed with it; otherwise the methods that need the changed file are named and not installed,
    so that no method ever ends up as a mix of files that was never flagged (a method folder of the destination
    that fails its checks there is looked at too, by its declaration). None of the three small files
    beside a method is copied: the destination's own stay, and its job writes its own IN_PLACE_SINCE.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md sections 3, 3.1 rule 3, 4 and 6 (Create_Tree, Install).

Which of the project's own modules it uses
    tree_parts                 files, copying, the other tree's identity, locks, the backup first, the job
    dev_tools                  infrastructure_fingerprints: what the infrastructure's flag vouches for
    research.variant_folders   find_variants: methods, their declarations and fingerprints
    research.method_flags      the flags' state; the names of the three small files
    research.code_identity     the engine's and the updater's files and fingerprints
    research.settings          settings_text, read_settings
    research.windows_text      windows_lines: the settings file is written with CRLF line ends

What uses it
    deploy/dev_command.py (the program behind Create_Tree.bat and Install.bat), and the tests.
"""
from __future__ import annotations

import contextlib
import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import tree_parts
from dev_tools import infrastructure_fingerprints
from research import backup as backups
from research import code_identity, method_flags
from research.settings import SETTINGS_FILE_NAME, read_settings, settings_text
from research.variant_folders import DECLARATION_NAME, VariantRefused, find_variants
from research.windows_text import windows_lines
from tree_parts import (EXIT_DONE, EXIT_NOT_CLEAN, METHODS_FOLDER, SOURCE_DATA, CommandFailed, CommandRefused,
                        copy_file, differing, files_under, infrastructure_paths, method_paths)

# The roles a tree made by Create_Tree, or installed into, can have. (DEV is where they are made from.)
OTHER_ROLES = ('QA', 'PROD')
# What a method step does in the destination.
ADD, REPLACE = 'add', 'replace'


@dataclass(frozen=True)
class MethodStep:
    """One method the install adds or replaces.  identity: 'E_002/RECUR_MEAN_ALL_V1'.  kind: ADD or REPLACE.
    variant: DEV's Variant of it (its files and fingerprint)."""
    identity: str
    kind: str
    variant: object


@dataclass
class Plan:
    """What an install would do, worked out from the two trees as they are.

    infrastructure: infrastructure files to copy (paths from the tree root).  infrastructure_gone: files of the
    destination's infrastructure that DEV no longer has, to remove.  engine_differs: the engine's fingerprint
    changes, so the destination's job makes everything again.  infrastructure_note: None, or why an
    infrastructure that differs is left alone.  steps: the methods added or replaced.
    passed_over: (identity, why) for each method that differs or is missing but is not installed.
    left_alone: methods the destination has and DEV does not.
    """
    infrastructure: list = field(default_factory=list)
    infrastructure_gone: list = field(default_factory=list)
    engine_differs: bool = False
    infrastructure_note: str | None = None
    steps: list = field(default_factory=list)
    passed_over: list = field(default_factory=list)
    left_alone: list = field(default_factory=list)

    @property
    def anything(self) -> bool:
        """True if the install would change the destination at all."""
        return bool(self.infrastructure or self.infrastructure_gone or self.steps)


def flag_state(variant) -> str:
    """How a method's I_AM_INSTALLABLE flag in DEV stands against its files now (research/method_flags.py)."""
    return method_flags.installable_state(variant.folder, {'fingerprint': variant.fingerprint})


def plan_infrastructure(plan: Plan, dev: Path, target: Path) -> None:
    """Fill in the plan's infrastructure part: what differs, and whether DEV's flag lets it be installed."""
    wanted = infrastructure_paths(dev)
    to_copy = differing(dev, target, wanted)
    gone = sorted(set(code_identity.infrastructure_files(target) + code_identity.updater_files(target))
                  - set(wanted))
    if not to_copy and not gone:
        return
    state = method_flags.installable_state(dev / 'src', infrastructure_fingerprints(dev))
    if state != method_flags.FLAGGED:
        plan.infrastructure_note = (f'the infrastructure differs ({len(to_copy) + len(gone)} files), and in DEV it is '
                                    f'{state}; Make_Installable.bat INFRA makes the flag')
        return
    plan.infrastructure, plan.infrastructure_gone = to_copy, gone
    plan.engine_differs = (code_identity.infrastructure_fingerprint(dev)
                           != code_identity.infrastructure_fingerprint(target))


def files_of_destination_methods(target: Path, theirs, theirs_refused) -> list:
    """For every method folder of the destination, the files it uses with what the destination holds of each:
    [(identity, ((path from src/methods, sha256 or None if the file is missing), ...)), ...].

    A valid method gives the files its fingerprint covers. A folder that fails its checks there gives the
    helpers its declaration lists, if the declaration can be read: such a method must be looked at too, because
    bringing a helper it lacks would let it run again as a mix nobody flagged. One whose declaration cannot be
    read gives nothing; nothing brought can make it run.
    """
    found = [(variant.identity, variant.fingerprint_lines) for variant in theirs]
    methods_root = Path(target) / METHODS_FOLDER
    for identity, _ in theirs_refused:
        try:
            declared = json.loads((methods_root / identity / DECLARATION_NAME).read_text(encoding='utf-8'))
            helpers = [helper for helper in declared['helpers'] if isinstance(helper, str)]
        except (OSError, ValueError, KeyError, TypeError):
            continue
        held = {helper: (code_identity.sha256_of_file(methods_root / helper)
                         if (methods_root / helper).is_file() else None) for helper in helpers}
        found.append((identity, tuple(held.items())))
    return found


def hold_back_shared_helper_mixes(candidates: list, destination_files: list, dev_identities,
                                  passed_over: list) -> list:
    """Take out of the install every method that would change another method of the destination behind its back.

    A method brings its helper files with it. If a helper it brings differs from the destination's (or is
    missing there), every method of the destination that lists that helper changes too. That is right only when
    those methods are installed in the same run (they are then DEV's flagged versions). Otherwise the method
    bringing the file is held back and named, and the question is asked again without it, until nothing more
    changes.

    candidates: the MethodSteps that are flagged and differ.
    destination_files: what files_of_destination_methods gives for the destination.
    dev_identities: the identities of DEV's methods.  passed_over: (identity, why) is added for each held back.
    Returns the steps that remain.
    """
    remaining = list(candidates)
    while True:
        brought = {path: sha for step in remaining for path, sha in step.variant.fingerprint_lines}
        installing = {step.identity for step in remaining}
        mixed = [(identity, sorted(path for path, sha in lines if brought.get(path, sha) != sha))
                 for identity, lines in destination_files if identity not in installing]
        mixed = [(identity, changed) for identity, changed in mixed if changed]
        if not mixed:
            return remaining
        identity, changed = mixed[0]
        why_not = ('DEV has no such method' if identity not in dev_identities
                   else 'it is not flagged as it now stands in DEV, or is itself held back')
        bringing = [step for step in remaining
                    if set(changed) & {path for path, _ in step.variant.fingerprint_lines}]
        for step in bringing:
            remaining.remove(step)
            passed_over.append((
                step.identity,
                f'it brings a changed helper file ({", ".join(changed)}) that {identity} in the destination also '
                f'uses, and that method is not installed with it ({why_not}). Flag every method that uses the '
                f'file (Make_Installable.bat ALL), then install again'))


def plan_install(dev: Path, target: Path) -> Plan:
    """Work out what an install from DEV into another tree would do. Reads both trees; changes nothing.

    dev, target: the two trees' folders.  Returns the Plan.
    """
    dev, target, plan = Path(dev), Path(target), Plan()
    plan_infrastructure(plan, dev, target)
    ours, ours_refused = find_variants(dev / METHODS_FOLDER)
    theirs, theirs_refused = (find_variants(target / METHODS_FOLDER) if (target / METHODS_FOLDER).is_dir()
                              else ((), []))
    there = {variant.identity: variant for variant in theirs}
    there_but_refused = dict(theirs_refused)
    plan.passed_over += [(name, f'its folder in DEV fails its checks: {why}') for name, why in ours_refused]
    candidates = []
    for variant in ours:
        if variant.identity in there and there[variant.identity].fingerprint == variant.fingerprint:
            continue
        missing = variant.identity not in there and variant.identity not in there_but_refused
        state = flag_state(variant)
        if state != method_flags.FLAGGED:
            plan.passed_over.append((variant.identity, f'in DEV it is {state}; Make_Installable.bat makes the flag'))
        elif missing and (variant.folder / method_flags.RETIRED_NAME).exists():
            plan.passed_over.append((variant.identity, 'it is retired in DEV, and a retired method is not added to '
                                                       'a tree that lacks it'))
        else:
            candidates.append(MethodStep(variant.identity, ADD if missing else REPLACE, variant))
    known = {variant.identity for variant in ours} | {name for name, _ in ours_refused}
    plan.steps = hold_back_shared_helper_mixes(
        candidates, files_of_destination_methods(target, theirs, theirs_refused), known, plan.passed_over)
    plan.passed_over.sort()
    plan.left_alone = sorted((set(there) | set(there_but_refused)) - known)
    return plan


def describe(plan: Plan, role: str) -> list:
    """The plan as lines for the owner, for example '  replace: E_002/RECUR_MEAN_ALL_V1 (...)'."""
    lines = []
    if plan.infrastructure or plan.infrastructure_gone:
        lines.append(f'  infrastructure: {len(plan.infrastructure)} files added or replaced, '
                     f'{len(plan.infrastructure_gone)} removed. '
                     + (f'The engine differs, so the {role} tree\'s job makes everything again, in both games.'
                        if plan.engine_differs else 'The engine\'s fingerprint is the same (only the updater or the '
                                                    'launchers differ): nothing is made again on its account.'))
    if plan.infrastructure_note:
        lines.append(f'  NOT INSTALLED: {plan.infrastructure_note}.')
    for step in plan.steps:
        lines.append(f'  {step.kind}: {step.identity}'
                     + (f' (its results in the {role} tree are made again)' if step.kind == REPLACE else ''))
    lines += [f'  NOT INSTALLED: {identity}: {why}.' for identity, why in plan.passed_over]
    lines += [f'  left alone: {identity} (the {role} tree has it; DEV does not)' for identity in plan.left_alone]
    if not plan.anything:
        lines.append(f'  Nothing to install: the {role} tree already has every part that is flagged in DEV.')
    return lines


def apply_plan(dev: Path, target: Path, plan: Plan) -> None:
    """Carry the plan out in the destination: remove, copy, and for each method clear what its declaration no
    longer lists (the three small files stay). Raises OSError if a file cannot be removed or copied."""
    for relative in plan.infrastructure_gone:
        (target / relative).unlink()
    for relative in plan.infrastructure:
        copy_file(dev, target, relative)
    for step in plan.steps:
        folder = target / METHODS_FOLDER / step.identity
        listed = {DECLARATION_NAME, *step.variant.declaration['files']}
        for item in (sorted(folder.iterdir()) if folder.is_dir() else ()):
            if item.is_dir() and item.name != '__pycache__':
                shutil.rmtree(item)
            elif item.is_file() and item.name not in listed and item.name not in method_flags.PASSED_OVER_NAMES:
                item.unlink()
        for relative in differing(dev, target, method_paths(step.variant)):
            copy_file(dev, target, relative)


def install(settings, role: str, *, show: bool, moment, say=print, run_job=tree_parts.run_job_of,
            backup=backups.make_backup) -> int:
    """Install.bat: install DEV's flagged software into another tree, then run that tree's own job.

    settings: DEV's settings.  role: 'QA' or 'PROD'.  show: print the plan and change nothing.
    moment: the present time on the PC's clock.  say: prints one line.
    run_job, backup: the destination's job and the backup before the install (a test passes its own).
    Returns EXIT_DONE; EXIT_NOT_CLEAN if the software was installed but the destination's job did not finish
    cleanly. Refuses (CommandRefused, SettingsRefused, LaunchRefused) before anything is changed; raises
    CommandFailed if the copy itself did not finish.
    """
    if role not in OTHER_ROLES:
        raise CommandRefused(f'Install.bat installs into QA or PROD; "{role}" is neither. For example: Install.bat QA')
    theirs = tree_parts.other_tree(settings, role)
    dev, target = settings.tree_root, theirs.tree_root
    with contextlib.ExitStack() as stack:
        locks = tree_parts.lock_trees(stack, (settings, theirs), 'install --show' if show else 'install',
                                      moment.strftime('%Y-%m-%d %H:%M'))
        plan = plan_install(dev, target)
        say(f'INSTALL from DEV ({dev}) into the {role} tree ({target}):')
        for line in describe(plan, role):
            say(line)
        if show:
            say('--show: nothing was changed.')
            return EXIT_DONE
        if not plan.anything:
            return EXIT_DONE
        tree_parts.require_python(theirs)
        made = tree_parts.back_up_first(theirs, 'before install', moment, say, backup)
        try:
            apply_plan(dev, target, plan)
            if plan_install(dev, target).anything:
                raise CommandFailed('after the copy the destination still differs from what was to be installed')
        except (OSError, CommandFailed) as fault:
            raise CommandFailed(
                f'THE INSTALL DID NOT FINISH ({type(fault).__name__}: {fault}). The {role} tree may hold some new '
                f'files and some old ones, and its job was not run. When the cause is put right, run Install.bat '
                f'{role} again: it copies whatever still differs. Or put the tree back as it was: Restore.bat '
                f'{role} {made.name}') from None
        say(f'Installed into the {role} tree: {len(plan.infrastructure)} infrastructure files, '
            f'{len(plan.steps)} methods.')
        code = run_job(theirs, locks[role].key, say)
    if code != 0:
        say(f'The software is installed, but the {role} tree\'s job did not finish cleanly (exit code {code}): see '
            f'what it printed above. When the cause is put right, run Run_Research.bat --no-update in {target}.')
        return EXIT_NOT_CLEAN
    say(f'Install finished: the {role} tree has the software and its results are up to date with it.')
    return EXIT_DONE


def check_place_for_a_new_tree(target: Path, role: str) -> None:
    """Refuse (CommandRefused) unless the folder for a new tree is absent (its parent being a folder) or is an
    empty folder: a tree is created nowhere else (rule 3)."""
    if target.exists():
        if not target.is_dir() or any(target.iterdir()):
            raise CommandRefused(
                f'{target} already holds something. A tree is created only into a folder that is absent or empty; '
                f'nothing was changed. If that folder is a {role} tree, use Install.bat; if it is the rest of a '
                f'creation that did not finish, delete it by hand and run Create_Tree.bat {role} again.')
    elif not target.parent.is_dir():
        raise CommandRefused(f'{target.parent} does not exist, so {target} cannot be made in it. Nothing was '
                             f'changed. Make that folder (or correct the {role} tree_root in the settings file).')


def choose_for_a_new_tree(dev: Path, say) -> list:
    """Which of DEV's methods go into a new tree: those flagged as they now stand and not retired. Every other
    method is named with the reason. Returns their Variants. Refuses (CommandRefused) if the infrastructure is
    not flagged as it now stands, no method is, or DEV holds no accepted results."""
    state = method_flags.installable_state(dev / 'src', infrastructure_fingerprints(dev))
    if state != method_flags.FLAGGED:
        raise CommandRefused(f'in DEV the infrastructure is {state}, so there is no engine to give the new tree. '
                             f'Nothing was changed. Run Make_Installable.bat ALL INFRA first.')
    variants, refused = find_variants(dev / METHODS_FOLDER)
    chosen = []
    for variant in variants:
        state = flag_state(variant)
        if (variant.folder / method_flags.RETIRED_NAME).exists():
            say(f'  not copied: {variant.identity}: it is retired in DEV.')
        elif state != method_flags.FLAGGED:
            say(f'  not copied: {variant.identity}: in DEV it is {state}; Make_Installable.bat makes the flag.')
        else:
            chosen.append(variant)
    for name, why in refused:
        say(f'  not copied: {name}: its folder in DEV fails its checks: {why}')
    if not chosen:
        raise CommandRefused('no method is flagged in DEV, so the new tree would have nothing to run. Nothing was '
                             'changed. Run Make_Installable.bat ALL INFRA first.')
    if not files_under(dev / SOURCE_DATA):
        raise CommandRefused(f'DEV holds no accepted results ({dev / SOURCE_DATA} is absent or empty), so there '
                             f'are none to give the new tree. Nothing was changed.')
    return chosen


def copy_and_check_new_tree(dev: Path, target: Path, chosen: list) -> tuple:
    """Copy the infrastructure, the chosen methods and the accepted results into the new tree's folder, then
    check the copy: the engine's and the updater's fingerprints and every method's are DEV's, and the results
    are the same bytes. Returns (number of software files, number of results files).
    Raises OSError or CommandFailed if anything could not be copied or the check fails."""
    software = sorted(set(infrastructure_paths(dev)) | {path for variant in chosen for path in method_paths(variant)})
    data = [f'{SOURCE_DATA}/{name}' for name in files_under(dev / SOURCE_DATA)]
    target.mkdir(exist_ok=True)
    for relative in software + data:
        copy_file(dev, target, relative)
    copied, refused = find_variants(target / METHODS_FOLDER)
    same_methods = ({variant.identity: variant.fingerprint for variant in copied}
                    == {variant.identity: variant.fingerprint for variant in chosen})
    if (refused or not same_methods or differing(dev, target, software + data)
            or code_identity.infrastructure_fingerprint(target) != code_identity.infrastructure_fingerprint(dev)
            or code_identity.updater_fingerprint(target) != code_identity.updater_fingerprint(dev)):
        raise CommandFailed('the copy does not match DEV when read back')
    return len(software), len(data)


def create_tree(settings, role: str, *, moment, say=print) -> int:
    """Create_Tree.bat: make a new QA or PROD tree from DEV's flagged software and accepted results.

    settings: DEV's settings.  role: 'QA' or 'PROD'.  moment: the present time on the PC's clock.
    say: prints one line.
    Returns EXIT_DONE. Refuses (CommandRefused, LaunchRefused) before anything is changed; raises CommandFailed
    if the copy did not finish (the folder then holds no settings file, so it is not a tree).
    """
    if role not in OTHER_ROLES:
        raise CommandRefused(f'Create_Tree.bat makes a QA or a PROD tree; "{role}" is neither. For example: '
                             f'Create_Tree.bat QA')
    dev, target = settings.tree_root, settings.places[role].tree_root
    check_place_for_a_new_tree(target, role)
    with contextlib.ExitStack() as stack:
        tree_parts.lock_trees(stack, (settings,), 'create tree', moment.strftime('%Y-%m-%d %H:%M'))
        say(f'CREATE the {role} tree at {target}, from DEV ({dev}):')
        chosen = choose_for_a_new_tree(dev, say)
        try:
            software, data = copy_and_check_new_tree(dev, target, chosen)
            unfinished = target / (SETTINGS_FILE_NAME + tree_parts.UNFINISHED_SUFFIX)
            unfinished.write_bytes(windows_lines(settings_text(role, settings.places)).encode('utf-8'))
            os.replace(unfinished, target / SETTINGS_FILE_NAME)
            read_settings(target, must_be=role)
        except (OSError, ValueError, CommandFailed, VariantRefused) as fault:
            raise CommandFailed(
                f'THE TREE WAS NOT CREATED ({type(fault).__name__}: {fault}). {target} may hold part of a copy; '
                f'unless it holds a settings file it is not a tree and nothing runs in it. Delete that folder by '
                f'hand, put the cause right, and run Create_Tree.bat {role} again.') from None
    say(f'  copied: the infrastructure and {len(chosen)} methods ({software} files), and DEV\'s accepted results '
        f'({data} files). The settings file was written last.')
    say(f'The {role} tree is created. It has no Python environment and no results of its own yet. Next, in '
        f'{target}: run create_venv.bat, then install_upgrade_dependencies_into_venv.bat, then Run_Research.bat '
        f'--no-update (its first job computes everything, which takes a while).')
    return EXIT_DONE
