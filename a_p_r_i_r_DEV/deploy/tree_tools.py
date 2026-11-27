"""DEV's other commands that touch another tree: "retire", "copy from PROD" and "restore".

What this file is for
    Retire.bat <family>/<variant> <reason>
        retires a method in every tree that has it: backs each such tree up, then writes I_AM_RETIRED beside the
        method there, from that tree's own next draw. The tree's next research job drops what the method had
        from that draw on and makes no more for it; its earlier results stay. Deleting the file brings it back.
    Copy_From_PROD.bat software|data|both QA   and   Copy_From_PROD.bat data DEV
        makes QA's software, or its data (source_data and results\research), or both, the same as PROD's, after
        a backup of QA; into DEV, data only (DEV's software is Git's). Before anything is touched, PROD must
        hold what is to be copied and its accepted results must pass the engine's reader; what PROD holds is
        listed before anything of the destination is removed. Then the destination's own research job
        runs (results updater left out), which makes again whatever no longer fits. With the software go PROD's
        I_AM_RETIRED and IN_PLACE_SINCE files, so that QA retires and counts exactly as PROD does.
    Restore.bat QA|PROD <backup zip>
        puts a tree back from one of its backups: the settings file inside the ZIP must name the tree being
        restored; the ZIP is unpacked into a fresh folder; the tree as it was is renamed aside (its new name no
        longer ends with its role, so nothing can run in it) and the fresh folder takes its name. Restored files
        are never mixed with newer ones. The owner then builds the tree's Python environment again.

    Every one of them first reads the other tree's own settings (rule 3), takes the lock of every tree it
    touches, and makes a backup before it replaces anything; if that backup cannot be made, nothing is replaced.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md sections 4 (I_AM_RETIRED), 6 and 7.

Which of the project's own modules it uses
    tree_parts               files, copying, the other tree's identity, locks, the backup first, the job
    research.settings        the settings; settings_from_text for the settings file inside a backup
    research.method_flags    write_retired; the names of the three small files
    research.reader          results_on_file: the last draw a tree holds, for the retirement draw
    research.research_job    GAMES
    research.code_identity   fingerprints, to check a copy of the software
    research.variant_folders find_variants, to check a copy of the software
    research.backup          make_backup
    research.tree_lock       LOCK_NAME, RECORDS_FOLDER

What uses it
    deploy/dev_command.py (the program behind Retire.bat, Copy_From_PROD.bat and Restore.bat), and the tests.
"""
from __future__ import annotations

import contextlib
import os
import re
import shutil
import zipfile
import zlib
from pathlib import Path, PurePosixPath

import tree_parts
from research import backup as backups
from research import code_identity, method_flags
from research.reader import ResultsRefused, results_on_file
from research.research_job import GAMES
from research.settings import ROLES, SETTINGS_FILE_NAME, SettingsRefused, same_folder, settings_from_text
from research.tree_lock import LOCK_NAME, RECORDS_FOLDER
from research.variant_folders import find_variants
from tree_parts import (EXIT_DONE, EXIT_NOT_CLEAN, METHODS_FOLDER, RESEARCH_RESULTS, ROOT_FILES, SOURCE_DATA,
                        CommandFailed, CommandRefused, copy_file, replace_folder)

# A method's identity as typed: family/variant, for example E_002/RECUR_MEAN_ALL_V1.
IDENTITY_PATTERN = re.compile(r'E_\d{3}/[A-Z0-9_]{3,96}\Z')
# What reading a ZIP raises when the file is not one, is cut short or holds damaged data.
UNREADABLE_ZIP = (OSError, zipfile.BadZipFile, zlib.error, EOFError)
# What Copy_From_PROD can copy, and where to.
SOFTWARE, DATA, BOTH = 'software', 'data', 'both'
COPY_DESTINATIONS = ('QA', 'DEV')


def retirement_draws(tree_root: Path) -> dict:
    """For each game whose accepted results a tree holds, the tree's own next draw: the one after the last on
    file. For example {'POWERBALL': 1592, 'OZLOTTO': 1709}. A game whose results are absent or unusable is left
    out; the tree's job gives it a draw when it first works that game."""
    draws = {}
    for game_id in GAMES:
        try:
            draws[game_id] = results_on_file(tree_root, game_id).last_draw + 1
        except ResultsRefused:
            continue
    return draws


def retire(settings, identity: str, reason: str, *, moment, say=print, backup=backups.make_backup) -> int:
    """Retire.bat: retire a method in every tree that has it.

    settings: DEV's settings.  identity: 'family/variant'.  reason: one line of plain text.
    moment: the present time on the PC's clock.  say: prints one line.  backup: a test passes its own.
    Returns EXIT_DONE. Refuses (CommandRefused, SettingsRefused, LaunchRefused) before anything is written:
    a bad name or reason, no tree that has the method, a tree whose lock is held, a backup that failed.
    """
    reason = ' '.join(reason.split())
    if not IDENTITY_PATTERN.match(identity):
        raise CommandRefused(f'"{identity}" is not a method\'s name. Give it as family/variant and then the reason, '
                             f'for example: Retire.bat E_002/RECUR_MEAN_ALL_V1 superseded by RECUR_MEAN_ALL_V2')
    if not reason or not reason.isascii() or not reason.isprintable():
        raise CommandRefused('Give the reason after the method\'s name, as one line of plain text, for example: '
                             'Retire.bat E_002/RECUR_MEAN_ALL_V1 superseded by RECUR_MEAN_ALL_V2')
    trees = [settings]
    for role in ROLES[1:]:
        if tree_parts.has_tree(settings, role):
            trees.append(tree_parts.other_tree(settings, role))
        else:
            say(f'  {role}: there is no tree at {settings.places[role].tree_root}; passed over.')
    with contextlib.ExitStack() as stack:
        tree_parts.lock_trees(stack, trees, 'retire', moment.strftime('%Y-%m-%d %H:%M'))
        to_retire = []
        for tree in trees:
            folder = tree.tree_root / METHODS_FOLDER / identity
            if not folder.is_dir():
                say(f'  {tree.role}: this tree does not have {identity}.')
            elif (folder / method_flags.RETIRED_NAME).exists():
                say(f'  {tree.role}: {identity} is already retired there; its file is left as it is.')
            else:
                to_retire.append((tree, folder))
        if not to_retire:
            if any((tree.tree_root / METHODS_FOLDER / identity).is_dir() for tree in trees):
                say('Nothing to do.')
                return EXIT_DONE
            raise CommandRefused(f'no tree has a method {identity}. Nothing was written. Who_Uses.bat method.py '
                                 f'lists the methods of DEV.')
        for tree, _ in to_retire:
            tree_parts.back_up_first(tree, 'before retire', moment, say, backup)
        for tree, folder in to_retire:
            draws = retirement_draws(tree.tree_root)
            method_flags.write_retired(folder, draws, reason)
            say(f'  {tree.role}: {identity} is retired from '
                + (', '.join(f'{game_id} draw {draw}' for game_id, draw in draws.items())
                   or 'the next draw of each game (its job writes the draws when it works them)')
                + '. That tree\'s next research job drops what it had from there on and remakes the reports.')
    say(f'Retired: {identity} ({reason}). In DEV the file {method_flags.RETIRED_NAME} beside the method is kept '
        f'in Git: commit it. Deleting the file in a tree brings the method back there.')
    return EXIT_DONE


def copy_software(prod: Path, target: Path) -> None:
    """Make a tree's software the same as PROD's: its src folder (PROD's I_AM_RETIRED and IN_PLACE_SINCE files
    with it; never an I_AM_INSTALLABLE, which means something in DEV only) and the root launchers. Then check
    the copy by the fingerprints. Raises OSError or CommandFailed."""
    replace_folder(prod, target, 'src', leave_out=(method_flags.INSTALLABLE_NAME,))
    for name in ROOT_FILES:
        if (prod / name).is_file():
            copy_file(prod, target, name)
        elif (target / name).exists():
            (target / name).unlink()
    ours, ours_refused = find_variants(prod / METHODS_FOLDER)
    theirs, theirs_refused = find_variants(target / METHODS_FOLDER)
    if ({variant.identity: variant.fingerprint for variant in ours}
            != {variant.identity: variant.fingerprint for variant in theirs}
            or sorted(name for name, _ in ours_refused) != sorted(name for name, _ in theirs_refused)
            or code_identity.infrastructure_fingerprint(prod) != code_identity.infrastructure_fingerprint(target)
            or code_identity.updater_fingerprint(prod) != code_identity.updater_fingerprint(target)):
        raise CommandFailed('the software copied does not match PROD\'s when read back')


def check_prod_holds(prod: Path, what: str) -> None:
    """Before anything of the destination is touched: PROD holds what is to be copied, and what is to be copied
    is usable. For the data, the accepted results of both games must pass the engine's own reader (each file
    whole, in draw order, and the one its ledger names), and PROD must hold computed results.
    Refuses (CommandRefused) otherwise; nothing has been changed."""
    if what in (SOFTWARE, BOTH) and not tree_parts.files_under(prod / 'src'):
        raise CommandRefused(f'the PROD tree holds no software ({prod / "src"} is absent or empty). Nothing was '
                             f'changed.')
    if what in (DATA, BOTH):
        for game_id in GAMES:
            try:
                results_on_file(prod, game_id)
            except ResultsRefused as refusal:
                raise CommandRefused(f'the PROD tree\'s accepted results for {game_id} cannot be used, so they are '
                                     f'not copied over another tree\'s: {refusal} Nothing was changed.') from None
        if not tree_parts.files_under(prod / RESEARCH_RESULTS):
            raise CommandRefused(f'the PROD tree holds no computed results ({prod / RESEARCH_RESULTS} is absent or '
                                 f'empty). Nothing was changed. Run its research job first.')


def copy_from_prod(settings, what: str, role: str, *, moment, say=print, run_job=tree_parts.run_job_of,
                   backup=backups.make_backup) -> int:
    """Copy_From_PROD.bat: make QA's software, data or both the same as PROD's, or DEV's data; then run the
    destination's own job.

    settings: DEV's settings.  what: SOFTWARE, DATA or BOTH.  role: the destination, 'QA' or 'DEV'.
    moment: the present time on the PC's clock.  say: prints one line.  run_job, backup: a test passes its own.
    Returns EXIT_DONE; EXIT_NOT_CLEAN if the copy was made but the destination's job did not finish cleanly.
    Refuses (CommandRefused, SettingsRefused, LaunchRefused) before anything is changed; raises CommandFailed
    if the copy itself did not finish.
    """
    usage = 'For example: Copy_From_PROD.bat both QA   or   Copy_From_PROD.bat data DEV'
    if what not in (SOFTWARE, DATA, BOTH) or role not in COPY_DESTINATIONS:
        raise CommandRefused(f'Give what to copy (software, data or both) and where to (QA or DEV). {usage}')
    if role == 'DEV' and what != DATA:
        raise CommandRefused(f'Into DEV only PROD\'s data is copied: DEV\'s software is what Git holds. {usage}')
    prod = tree_parts.other_tree(settings, 'PROD')
    theirs = settings if role == 'DEV' else tree_parts.other_tree(settings, role)
    target = theirs.tree_root
    with contextlib.ExitStack() as stack:
        locks = tree_parts.lock_trees(stack, {tree.role: tree for tree in (settings, prod, theirs)}.values(),
                                      'copy from PROD', moment.strftime('%Y-%m-%d %H:%M'))
        say(f'COPY FROM PROD ({prod.tree_root}) into the {role} tree ({target}): {what}.')
        check_prod_holds(prod.tree_root, what)
        tree_parts.require_python(theirs)
        made = tree_parts.back_up_first(theirs, 'before copy from PROD', moment, say, backup)
        try:
            if what in (SOFTWARE, BOTH):
                copy_software(prod.tree_root, target)
                say(f'  software: the {role} tree\'s src folder and launchers are now PROD\'s.')
            if what in (DATA, BOTH):
                counts = [replace_folder(prod.tree_root, target, folder) for folder in (SOURCE_DATA, RESEARCH_RESULTS)]
                say(f'  data: {counts[0]} files of accepted results and {counts[1]} files of computed results are '
                    f'now PROD\'s.')
        except (OSError, CommandFailed) as fault:
            raise CommandFailed(
                f'THE COPY DID NOT FINISH ({type(fault).__name__}: {fault}). The {role} tree may hold part of '
                f'PROD\'s files and part of its own, and its job was not run. When the cause is put right, run the '
                f'same command again: it replaces everything it copies. '
                + (f'Or put the tree back as it was: Restore.bat {role} {made.name}' if role != 'DEV'
                   else f'The backup made just before is {made}.')) from None
        code = run_job(theirs, locks[role].key, say)
    if code != 0:
        say(f'The copy was made, but the {role} tree\'s job did not finish cleanly (exit code {code}): see what it '
            f'printed above. When the cause is put right, run Run_Research.bat --no-update in {target}.')
        return EXIT_NOT_CLEAN
    say(f'Copy finished: the {role} tree\'s results are up to date with what it now holds.')
    return EXIT_DONE


def find_backup(settings, role: str, name: str) -> Path:
    """The backup ZIP the owner named: a full path, or a file name in that role's backup folder.
    Refuses (CommandRefused) if there is no such file."""
    typed = Path(name)
    for path in ((typed,) if typed.is_absolute() else (settings.places[role].backup_root / typed, typed.resolve())):
        if path.is_file():
            return path
    raise CommandRefused(f'the backup "{name}" was not found (looked in {settings.places[role].backup_root}). '
                         f'Give a file name from that folder, or a full path. Nothing was changed.')


def check_backup(path: Path, settings, role: str) -> list:
    """Check a backup before anything is touched: it is a readable ZIP whose every file reads back whole, every
    name in it stays inside the tree, and its own settings file names the tree being restored (its role, and
    that role's tree_root).  Returns the names of the files in it. Refuses (CommandRefused) otherwise."""
    try:
        with zipfile.ZipFile(path) as archive:
            names = [info.filename for info in archive.infolist() if not info.is_dir()]
            damaged = archive.testzip()
            text = archive.read(SETTINGS_FILE_NAME).decode('utf-8') if SETTINGS_FILE_NAME in names else None
    except (*UNREADABLE_ZIP, UnicodeDecodeError) as fault:
        raise CommandRefused(f'{path} cannot be read as a backup ({type(fault).__name__}: {fault}). Nothing was '
                             f'changed. Use another backup.') from None
    if damaged:
        raise CommandRefused(f'{path} is damaged: "{damaged}" in it does not read back whole. Nothing was changed. '
                             f'Use another backup.')
    outside = [name for name in names if name.startswith('/') or '\\' in name or ':' in name
               or '..' in PurePosixPath(name).parts]
    if outside:
        raise CommandRefused(f'{path} holds a name that does not stay inside a tree ("{outside[0]}"): it is not '
                             f'one of this project\'s backups. Nothing was changed.')
    if text is None:
        raise CommandRefused(f'{path} holds no {SETTINGS_FILE_NAME}, so it is not the backup of a tree. Nothing '
                             f'was changed.')
    try:
        inside = settings_from_text(text, f'{path} / {SETTINGS_FILE_NAME}')
    except SettingsRefused as refusal:
        raise CommandRefused(f'{refusal} Nothing was changed.') from None
    if inside.role != role or not same_folder(inside.tree_root, settings.places[role].tree_root):
        raise CommandRefused(
            f'{path} is the backup of the {inside.role} tree at {inside.tree_root}, not of the {role} tree at '
            f'{settings.places[role].tree_root}. A backup is restored only into the tree it was made of. Nothing '
            f'was changed.')
    return names


def restore(settings, role: str, name: str, *, moment, say=print, backup=backups.make_backup) -> int:
    """Restore.bat: put the QA or the PROD tree back from one of its backups.

    settings: DEV's settings.  role: 'QA' or 'PROD'.  name: the backup's file name or full path.
    moment: the present time on the PC's clock.  say: prints one line.  backup: a test passes its own.
    Returns EXIT_DONE. Refuses (CommandRefused, SettingsRefused, LaunchRefused) before the tree is touched;
    raises CommandFailed if the two renames at the end could not both be made (it says where everything is).
    """
    if role == 'DEV':
        raise CommandRefused('DEV is not restored by this command: its software is in Git. To put DEV\'s data back, '
                             'unpack the backup by hand into a fresh folder and move what you need.')
    if role not in ROLES:
        raise CommandRefused('Give the tree (QA or PROD) and the backup, for example: Restore.bat QA '
                             'QA_20261201_201012_after_job.zip')
    target = settings.places[role].tree_root
    path = find_backup(settings, role, name)
    names = check_backup(path, settings, role)
    stamp = moment.strftime('%Y%m%d_%H%M%S')
    fresh, aside = (target.with_name(f'{target.name}_being_restored_{stamp}'),
                    target.with_name(f'{target.name}_set_aside_{stamp}'))
    is_tree = tree_parts.has_tree(settings, role)
    if not is_tree and target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise CommandRefused(f'{target} holds files but no settings file, so it is not a tree and this command '
                             f'does not touch it. Rename it away by hand, then run Restore.bat again.')
    if fresh.exists() or aside.exists() or not target.parent.is_dir():
        raise CommandRefused(f'{fresh} or {aside} already exists, or {target.parent} does not. Nothing was changed.')
    trees = [settings] + ([tree_parts.other_tree(settings, role)] if is_tree else [])
    with contextlib.ExitStack() as stack:
        locks = tree_parts.lock_trees(stack, trees, 'restore', moment.strftime('%Y-%m-%d %H:%M'))
        say(f'RESTORE the {role} tree at {target} from {path}:')
        if is_tree:
            tree_parts.back_up_first(trees[1], 'before restore', moment, say, backup)
        try:
            with zipfile.ZipFile(path) as archive:
                archive.extractall(fresh)
            if tree_parts.files_under(fresh) != sorted(names):
                raise CommandFailed('what was unpacked is not what the backup lists')
        except (*UNREADABLE_ZIP, CommandFailed) as fault:
            shutil.rmtree(fresh, ignore_errors=True)
            raise CommandRefused(f'the backup could not be unpacked ({type(fault).__name__}: {fault}). The {role} '
                                 f'tree was not touched.') from None
        say(f'  unpacked: {len(names)} files into a fresh folder.')
        try:
            if is_tree:
                os.rename(target, aside)
                locks[role].path = aside / RECORDS_FOLDER / LOCK_NAME
            elif target.exists():
                target.rmdir()
            os.rename(fresh, target)
        except OSError as fault:
            raise CommandFailed(
                f'THE RESTORE DID NOT FINISH ({type(fault).__name__}: {fault}). The restored copy is whole at '
                f'{fresh}. The tree as it was is at {aside if aside.exists() else target}. Put the cause right, '
                f'then by hand rename {fresh} to {target} (first moving away whatever is at that name).') from None
    if is_tree:
        say(f'  the tree as it was is kept at {aside}. Nothing can run in it; delete it by hand when it is no '
            f'longer wanted.')
    say(f'Restored: the {role} tree at {target} is now as the backup holds it. It has no Python environment: in '
        f'that folder run create_venv.bat, then install_upgrade_dependencies_into_venv.bat, then Run_Research.bat '
        f'--no-update.')
    return EXIT_DONE
