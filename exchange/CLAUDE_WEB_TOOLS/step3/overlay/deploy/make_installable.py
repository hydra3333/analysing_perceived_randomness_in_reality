"""Make_Installable: the owner's command that marks finished variants, or the infrastructure, ready in DEV.

What this file is for
    It reads what the owner typed after Make_Installable.bat, makes (or with --unmark removes) the readiness
    marker of each thing named, says what it did for each on a line of its own, and ends with one line of
    counts. One thing that is refused does not stop the others; the exit code then says that something was
    refused. It works in DEV only and changes nothing but markers.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 4 (Make_Installable.bat <family> <variant>;
    several variants at once; --unmark) and 12.2 (Make_Installable.bat INFRA).

Which of the project's own modules it uses
    install_readiness          the markers themselves
    research.variant_folders   the patterns a family's and a variant's folder name must match

What uses it
    deploy/deploy_command.py, for Make_Installable.bat; and its tests.
"""
from __future__ import annotations

from pathlib import Path

from research import variant_folders

import install_readiness

# The word that names the infrastructure where a variant would be named.
INFRA_WORD = 'INFRA'
# The option that removes markers where the command would make them.
UNMARK_OPTION = '--unmark'
# Exit codes: every named thing was done; at least one was refused; what was typed could not be understood.
EXIT_DONE, EXIT_REFUSED, EXIT_USAGE = 0, 1, 2
USAGE = ('Usage:  Make_Installable.bat INFRA\n'
         '        Make_Installable.bat <family> <variant>              for example  E_002 RECUR_MEAN_ALL_V1\n'
         '        Make_Installable.bat <family>/<variant> [...]        several at once, each as family/variant\n'
         '        add --unmark to remove the markers instead of making them')


def things_named(arguments) -> list:
    """Turn what the owner typed into the list of things to mark.

    arguments: the words after the launcher's name, without --unmark, for example ['E_002', 'RECUR_MEAN_ALL_V1']
    or ['E_002/RECUR_MEAN_ALL_V1', 'E_003/GAP_V1', 'INFRA'].
    Returns a list of 'INFRA' and (family, variant) pairs in the order typed, each once, for example
    [('E_002', 'RECUR_MEAN_ALL_V1')]. Raises ValueError, with a sentence for the owner, for nothing named, or a
    word that is neither INFRA nor a family and a variant whose names have the form of folder names.
    """
    if not arguments:
        raise ValueError('nothing was named.')
    if (len(arguments) == 2 and '/' not in arguments[0] and '/' not in arguments[1]
            and INFRA_WORD not in arguments):
        arguments = [f'{arguments[0]}/{arguments[1]}']
    named = []
    for word in arguments:
        if word == INFRA_WORD:
            thing = INFRA_WORD
        else:
            family, separator, variant_name = word.partition('/')
            if (not separator or not variant_folders.FAMILY_FOLDER_PATTERN.match(family)
                    or not variant_folders.VARIANT_FOLDER_PATTERN.match(variant_name)):
                raise ValueError(f'"{word}" is neither INFRA nor a variant written as family/variant '
                                 f'(for example E_002/RECUR_MEAN_ALL_V1).')
            thing = (family, variant_name)
        if thing not in named:
            named.append(thing)
    return named


def main(arguments, tree_root: Path, say=print) -> int:
    """Run the command.

    arguments: the words the owner typed after Make_Installable.bat.  tree_root: DEV's folder (the caller has
    checked that this tree is DEV).  say: where the lines for the owner go.
    Returns the exit code: 0 everything named was marked (or unmarked, or was so already); 1 at least one thing
    was refused, the others having been done; 2 what was typed could not be understood, and nothing was done.
    """
    unmark = UNMARK_OPTION in arguments
    try:
        named = things_named([word for word in arguments if word != UNMARK_OPTION])
    except ValueError as problem:
        say(f'REFUSED: {problem} Nothing was done.\n{USAGE}')
        return EXIT_USAGE
    names = ', '.join(thing if thing == INFRA_WORD else '/'.join(thing) for thing in named)
    doing = 'to remove the readiness marker of' if unmark else 'to mark ready'
    say(f'MAKE INSTALLABLE - START - tree DEV {tree_root} - {doing}: {names}')
    done = refused = 0
    for thing in named:
        try:
            if thing == INFRA_WORD:
                line = (install_readiness.unmark_infrastructure if unmark
                        else install_readiness.mark_infrastructure)(tree_root)
            else:
                line = (install_readiness.unmark_variant if unmark
                        else install_readiness.mark_variant)(tree_root, *thing)
        except install_readiness.ReadinessRefused as refusal:
            refused += 1
            say(f'REFUSED: {refusal}')
            continue
        done += 1
        say(line)
    say(f'MAKE INSTALLABLE - END - {done} done, {refused} REFUSED' + ('' if not refused else
        '. What was refused is not ready: correct what its line says and run the command again for it.'))
    return EXIT_REFUSED if refused else EXIT_DONE
