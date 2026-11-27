"""DEV's own commands that touch only DEV: "make installable" and "who uses".

What this file is for
    DEV is where methods and the engine are written and installed from. Two small commands help with that:
      Make_Installable.bat <family>/<variant> ... | ALL | INFRA
          writes the flag I_AM_INSTALLABLE beside each named method (ALL: every method), holding the method's
          fingerprint; INFRA writes the same kind of flag once, in src, holding the engine's fingerprint and the
          updater's. A flag says "this version may be installed". It is out of date as soon as a file it
          vouches for changes, and the install commands then report it and leave that part alone until the
          flag is made again.
      Who_Uses.bat <helper file>
          lists every method that uses a helper file, so that the owner sees what a change to it would touch.
          It changes nothing.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md sections 4 and 6.

Which of the project's own modules it uses
    research.variant_folders   find_variants: the methods, their declarations and fingerprints
    research.code_identity     the engine's and the updater's fingerprints
    research.method_flags      the flag files
    research.tree_lock         the tree's lock, held while flags are written

What uses it
    deploy/dev_command.py (the program behind Make_Installable.bat and Who_Uses.bat), and the tests.
"""
from __future__ import annotations

from pathlib import Path

from research import code_identity, method_flags
from research.tree_lock import tree_lock
from research.variant_folders import find_variants

# Where a tree keeps its methods, from the tree root; and the two words that stand for "every method" and "the
# infrastructure" on Make_Installable's command line.
METHODS_FOLDER = 'src/methods'
ALL_METHODS, INFRASTRUCTURE = 'ALL', 'INFRA'
# The exit codes: done; something named could not be flagged (or was not found).
EXIT_DONE, EXIT_NOT_ALL = 0, 1


def infrastructure_fingerprints(tree_root: Path) -> dict:
    """What the infrastructure's flag vouches for, computed from the files now: the engine's fingerprint and the
    updater's, for example {'fingerprint': 'ab12...', 'updater_fingerprint': 'cd34...'}."""
    return {'fingerprint': code_identity.infrastructure_fingerprint(tree_root),
            'updater_fingerprint': code_identity.updater_fingerprint(tree_root)}


def make_installable(settings, names, moment, say=print) -> int:
    """Write the I_AM_INSTALLABLE flags that were asked for, under the tree's lock.

    settings: DEV's settings.  names: what the owner typed: method identities ('E_002/RECUR_MEAN_ALL_V1'), and/or
    ALL (every method), and/or INFRA (the infrastructure).  moment: the present time on the PC's clock.
    say: prints one line.
    Says one line for each flag: written, or already as it should be. A named method that does not exist, and a
    method folder that fails its checks, is said and not flagged; the others are still flagged.
    Returns EXIT_DONE, or EXIT_NOT_ALL if anything named could not be flagged or nothing was named.
    """
    tree_root, made = settings.tree_root, moment.strftime('%Y-%m-%d %H:%M')
    if not names:
        say('Nothing was named. Give method identities (family/variant), or ALL for every method, or INFRA for the '
            'infrastructure; for example: Make_Installable.bat ALL INFRA')
        return EXIT_NOT_ALL
    variants, refused = find_variants(tree_root / METHODS_FOLDER)
    by_identity = {variant.identity: variant for variant in variants}
    wanted_methods = sorted(by_identity) if ALL_METHODS in names else [name for name in names
                                                                     if name not in (ALL_METHODS, INFRASTRUCTURE)]
    not_all = False
    with tree_lock(tree_root, 'make installable', made):
        for identity in wanted_methods:
            if identity not in by_identity:
                why = dict(refused).get(identity, 'there is no such method in this tree (give it as family/variant)')
                say(f'NOT FLAGGED: {identity}: {why}')
                not_all = True
                continue
            variant = by_identity[identity]
            written = method_flags.write_installable(variant.folder, {'fingerprint': variant.fingerprint}, made)
            say(f'{"flagged" if written else "already flagged, unchanged"}: {identity} (fingerprint '
                f'{variant.fingerprint[:12]}...)')
        if ALL_METHODS in names:
            for name, why in refused:
                say(f'NOT FLAGGED: {name}: the method folder fails its checks: {why}')
                not_all = True
        if INFRASTRUCTURE in names:
            fingerprints = infrastructure_fingerprints(tree_root)
            written = method_flags.write_installable(tree_root / 'src', fingerprints, made)
            say(f'{"flagged" if written else "already flagged, unchanged"}: the infrastructure (engine '
                f'{fingerprints["fingerprint"][:12]}..., updater {fingerprints["updater_fingerprint"][:12]}...)')
    say('Done, but not everything named was flagged: see NOT FLAGGED above.' if not_all else 'Done.')
    return EXIT_NOT_ALL if not_all else EXIT_DONE


def who_uses(settings, helper: str, say=print) -> int:
    """List every method that uses a helper file. Changes nothing.

    settings: DEV's settings.  helper: the file, as a declaration lists it ('_shared/recurrence_gaps_v1.py',
    'E_002/core_v1.py') or by its name alone ('core_v1.py'), in either spelling of the slashes.
    A method uses a file if its declaration lists it among its helpers or its own files. Method folders that
    fail their checks are named, because their declarations could not be read.
    Returns EXIT_DONE if at least one method uses it, EXIT_NOT_ALL if none does.
    """
    wanted = helper.replace('\\', '/').strip('/')
    variants, refused = find_variants(settings.tree_root / METHODS_FOLDER)
    users = {}
    for variant in variants:
        listed = list(variant.declaration['helpers']) + [f'{variant.identity}/{name}'
                                                         for name in variant.declaration['files']]
        matching = sorted(path for path in listed if path == wanted or path.endswith('/' + wanted))
        if matching:
            users[variant.identity] = matching
    for identity, matching in sorted(users.items()):
        say(f'{identity}    uses {", ".join(matching)}')
    for name, why in refused:
        say(f'NOT READ: {name}: the method folder fails its checks ({why})')
    different = sorted({path for matching in users.values() for path in matching})
    say(f'{len(users)} of {len(variants)} methods use "{wanted}"'
        + (f', which matches {len(different)} different files: {", ".join(different)}' if len(different) > 1 else '')
        + '. A change to a helper changes the fingerprint of every method that uses it: each is rebuilt.')
    return EXIT_DONE if users else EXIT_NOT_ALL
