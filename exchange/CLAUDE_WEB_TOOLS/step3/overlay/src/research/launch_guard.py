"""The launch guard: what a tree checks of itself before a command works in it.

What this file is for
    Two moments, each one function. AT EVERY LAUNCH of a command in a tree: the settings file names this folder;
    no operation was left unfinished in this tree (an install, a rerun, a reseeding, a restore, a backup being
    made); and, in QA and PROD, the tree's own Python environment has its marker and the marker lists the
    packages installed now. AT THE START OF A JOB, under the job lock: the environment's digest is computed once
    (it goes into every forecast the job makes); in QA and PROD it must equal the marker's, and the tree's
    software must match its list of installed files with nothing else under src; and, in every tree, no other
    Python process of this tree may be running. Every refusal says what was found and what to do. The guard
    changes nothing, repairs nothing and ends no process. A tree checks only itself: its own folder, its own
    environment and its own records.

    DEV has no marker and no list of installed files (nothing is installed there), so those two checks are QA's
    and PROD's; everything else is the same in every tree.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 9 ("At every launch"; "At the start of a research
    job or a rerun") and section 8 (while an unfinished operation's file exists every launcher of the tree
    refuses, except the command that finishes it);
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 13 and 15.

Which of the project's own modules it uses
    research.settings            read_settings: the tree's role, folder and environment folder
    research.job_lock            LaunchRefused, RECORDS_FOLDER
    research.environment_marker  the environment's digest and its marker
    research.installed_files     the tree's list of installed files, and every way the tree differs from it
    research.process_rule        no other Python process of this tree

What uses it
    src/research_command.py (every launch); research/research_job.py (the start of a job); and its tests. The
    commands of the later slices of build step 3 call the same two functions.
"""
from __future__ import annotations

from pathlib import Path

from research import environment_marker, installed_files, process_rule
from research.job_lock import RECORDS_FOLDER, LaunchRefused
from research.settings import TreeSettings, read_settings

# The files that mean an operation did not finish in this tree (deployment design sections 2, 8 and 9): where each
# lies from the tree root, what it means, and the way on. While one exists every launcher of the tree refuses,
# except the command that finishes it.
UNFINISHED_OPERATIONS = (
    (f'{RECORDS_FOLDER}/INSTALL_IN_PROGRESS.json',
     'an install, an infrastructure reinstall, a correction of shared code or a QA software replacement did not '
     'finish in this tree',
     'Run that same command again from DEV, or restore from a backup you choose.'),
    (f'{RECORDS_FOLDER}/RERUN_IN_PROGRESS.json',
     'a historical walk-forward rerun did not finish in this tree',
     'Run the same rerun command again with the same scope, or restore from a backup you choose.'),
    (f'{RECORDS_FOLDER}/RESEED_IN_PROGRESS.json',
     'a research-data reseeding from PROD did not finish in this tree',
     'Run the same reseeding command again from DEV, or restore from a backup you choose.'),
    (f'{RECORDS_FOLDER}/RESTORE_IN_PROGRESS.json',
     'a restore from backup did not finish in this tree',
     'Run the same restore command again from the recovery kit.'),
    (f'{RECORDS_FOLDER}/SNAPSHOT_IN_PROGRESS.lock',
     'a backup of this tree is being made, or one was ended before it finished',
     'Wait for the backup to finish. If none is running, read what Run_Snapshot.bat says.'),
)
# The trees that have a verified-environment marker and a list of installed files. DEV has neither.
INSTALLED_ROLES = ('QA', 'PROD')


class GuardRefused(LaunchRefused):
    """The tree is not in a state in which the command may work. The message says what was found, where, and what
    to do. Nothing was started and nothing was changed."""


def check_no_unfinished_operation(tree_root: Path, finishing: str | None = None) -> None:
    """Refuse while a file of an unfinished operation lies in the tree.

    tree_root: the tree's folder.  finishing: None for an ordinary command; for the one command that finishes an
    operation, that operation's file as UNFINISHED_OPERATIONS names it, which alone is then passed over.
    Refuses (GuardRefused), naming the file, what it means and the way on.
    """
    for relative, meaning, way_on in UNFINISHED_OPERATIONS:
        if relative != finishing and (Path(tree_root) / relative).exists():
            raise GuardRefused(f'{Path(tree_root) / relative} exists: {meaning}. Until it is finished no command '
                               f'works in this tree. {way_on}')


def check_at_launch(tree_root: Path, finishing: str | None = None) -> TreeSettings:
    """The checks of every launch (deployment design section 9, first paragraph).

    tree_root: the folder the launcher is in.  finishing: see check_no_unfinished_operation.
    Returns the tree's settings, for example TreeSettings(role='PROD', tree_root=Path('G:/a_p_r_i_r'), ...).
    Refuses: a settings file the reader refuses (SettingsRefused); an unfinished operation (GuardRefused); in QA
    and PROD, an environment with no marker, or whose marker does not list the packages installed now
    (EnvironmentRefused: "environment not verified").
    """
    settings = read_settings(Path(tree_root))
    check_no_unfinished_operation(settings.tree_root, finishing)
    if settings.role in INSTALLED_ROLES:
        environment_marker.check_marker_lists_what_is_installed(settings.venv_dir)
    return settings


def check_at_job_start(settings: TreeSettings, say) -> str:
    """The checks at the start of a research job, made while the job holds the tree's job lock (deployment design
    section 9, second paragraph). The orphan marker and the lock itself are the job's own first steps.

    settings: the tree's settings.  say: the function that prints a line for the owner.
    Returns the environment's digest, which the job writes into the envelope of every forecast it makes; for
    example '9c1f...e07a'.
    Refuses: an environment that cannot be read, or in QA and PROD is not the one that was verified
    (EnvironmentRefused); in QA and PROD, software that differs from the tree's list of installed files, every
    difference named (GuardRefused); another Python process of this tree (ProcessRuleRefused).
    """
    say(f'Reading this tree\'s own Python environment at {settings.venv_dir}. It can take two or three minutes '
        f'when its files have not been read lately.')
    digest, files_read = environment_marker.environment_digest(settings.venv_dir)
    say(f'The environment: {files_read} file(s) read; digest {digest}.')
    if settings.role in INSTALLED_ROLES:
        environment_marker.check_digest_is_the_markers(settings.venv_dir, digest)
        try:
            differences = installed_files.differences(settings.tree_root,
                                                      installed_files.read_list(settings.tree_root))
        except installed_files.InstalledFilesRefused as refusal:
            raise GuardRefused(str(refusal)) from None
        if differences:
            raise GuardRefused(f'this tree\'s software does not match its list of installed files '
                               f'({settings.tree_root / installed_files.LIST_PATH}); {len(differences)} '
                               f'difference(s):\n  ' + '\n  '.join(differences) + f'\n{installed_files.WHAT_TO_DO}')
        say('The environment is the one that was verified, and the software matches its list of installed files.')
    looked_at = process_rule.check_no_other_process_of_tree(settings.tree_root)
    say(f'No other Python process of this tree is running ({looked_at} processes of this PC looked at).')
    return digest
