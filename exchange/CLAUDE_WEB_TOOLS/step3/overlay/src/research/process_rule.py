"""The process rule: which Python processes on this PC belong to a tree. It reads the process table; it never acts
on a process.

What this file is for
    Before a research job works in a tree, no other Python process of that tree may be running: a second job, a
    backup, an install's tool, or a process left over from a job that was ended. This file reads the PC's process
    table through psutil and lists every Python process that belongs to the tree by the rule below. It ends,
    signals and suspends nothing: a process that should not be there is for the owner to let finish or to close.
    A Python process whose details cannot be read is a refusal, never a pass.

    The rule (deployment design section 9, first row of its table): a process whose program is named python.exe
    or pythonw.exe (any name beginning "python" outside Windows), other than the asking process and its own
    parents, is of the tree when (a) its program file lies in the tree, or (b) its working folder is the tree or
    lies in it, or (c) its command line, or the command line of any process above it, names the tree's folder.
    Unrelated Python work on the PC does not count.

    Every program started from a tree's own environment is two processes on Windows: the environment's python.exe
    and, under it, the base Python (TASK_T028). The second has its program file outside the tree; it is found by
    (c), through its parent. The asking program's own pair is left out because both are in its own chain.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 15 ("No program ends another process");
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 9 (the process rules). The rule and the refusals
    are those of the reviewed process tool of the first system (src/package_tools/process_check.py, its rule
    6.1); that file is not reused.

Which of the project's own modules it uses
    research.job_lock    LaunchRefused: a refusal of this file stops a launch like any other

What uses it
    research/launch_guard.py, and its tests.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from research.job_lock import LaunchRefused

# The names of a Python program on Windows. Elsewhere (the cloud's tests) any program name beginning "python".
WINDOWS_PYTHON_NAMES = ('python.exe', 'pythonw.exe')
# The marks that, like a letter or a digit, can continue a folder's name: after the tree's path in a command line
# they mean that another, longer-named folder is spoken of (T:\a_p_r_i_r_backups is not T:\a_p_r_i_r).
NAME_CONTINUES = '_-.~'
# What the owner is told to do about a process that is listed. No program of the project ends a process.
WHAT_TO_DO = ('Let it finish, or close it yourself in its own window; no program of this project ends a process. '
              'Then run the command again.')


class ProcessRuleRefused(LaunchRefused):
    """A Python process of the tree is running, or the process table could not be read. The message lists each
    process and says what to do."""


@dataclass(frozen=True)
class ProcessSeen:
    """One process, as the table was read.

    process_id, parent_id: its number and its parent's (None if not given).  name: its program's name, for example
    'python.exe'.  program: its program file's full path.  working_folder: its current folder.  command_line: its
    arguments, for example ('G:\\\\a_p_r_i_r\\\\.venv\\\\Scripts\\\\python.exe', '-I', 'src\\\\research_command.py').
    unreadable: None, or what could not be read of a Python process (it is then a refusal). For a process that is
    not Python only name, parent and command line are read, and an unreadable command line is simply None.
    """
    process_id: int
    parent_id: int | None
    name: str
    program: str | None = None
    working_folder: str | None = None
    command_line: tuple | None = None
    unreadable: str | None = None


def is_python_name(name: str) -> bool:
    """True if a program name is Python's: 'python.exe' or 'pythonw.exe' in any case; outside Windows also any name
    beginning 'python' (for example 'python3.15')."""
    lowered = (name or '').lower()
    return lowered in WINDOWS_PYTHON_NAMES or (os.name != 'nt' and lowered.startswith('python'))


def read_process_table() -> tuple:
    """Read every process of the PC, changing nothing.

    Returns a tuple of ProcessSeen. A Python process gets all its details; one of them that cannot be read is
    recorded in `unreadable`. Any other process gets its name, parent and, where readable, its command line, so
    that rule (c) sees a parent such as the cmd.exe that runs a launcher.
    Refuses (ProcessRuleRefused) when psutil is not installed in the Python that runs this, or the table itself
    cannot be read.
    """
    try:
        import psutil
    except ImportError:
        raise ProcessRuleRefused('the package psutil is not installed in the Python environment that runs this '
                                 'command, so the process table cannot be read and nothing was started. It is one of '
                                 'the packages install_upgrade_dependencies_into_venv.bat installs: build the '
                                 'tree\'s environment with it.') from None
    seen = []
    try:
        for process in psutil.process_iter(['pid', 'ppid', 'name']):
            name = process.info.get('name') or ''
            details = {'program': None, 'working_folder': None, 'command_line': None, 'unreadable': None}
            if is_python_name(name):
                for detail, read in (('program', process.exe), ('working_folder', process.cwd),
                                     ('command_line', process.cmdline)):
                    try:
                        value = read()
                        details[detail] = tuple(value) if detail == 'command_line' else value
                    except psutil.NoSuchProcess:
                        details['unreadable'] = 'it ended while it was being read'
                    except (psutil.AccessDenied, psutil.ZombieProcess, OSError) as error:
                        details['unreadable'] = f'its {detail.replace("_", " ")} could not be read ({type(error).__name__})'
            else:
                try:
                    details['command_line'] = tuple(process.cmdline())
                except (psutil.Error, OSError):
                    pass                         # not a Python process: it can neither list nor clear anything
            seen.append(ProcessSeen(process_id=process.info['pid'], parent_id=process.info.get('ppid'), name=name,
                                    **details))
    except (psutil.Error, OSError) as error:
        raise ProcessRuleRefused(f'the process table of this PC could not be read ({type(error).__name__}: {error}); '
                                 f'nothing was started. Run the command again; if it refuses again, say so.') from None
    return tuple(seen)


def own_chain() -> frozenset:
    """This process and every process above it, by number: they are the asking program itself (on Windows the
    environment's python.exe is the parent of the base Python that runs this) and the windows it was started
    from. Returns, for example, frozenset({4120, 4096, 1532}); only this process's own number if its parents
    cannot be read."""
    chain = {os.getpid()}
    try:
        import psutil
        chain.update(parent.pid for parent in psutil.Process().parents())
    except Exception:                            # psutil missing or a parent unreadable: fewer are left out,
        pass                                     # never more, so the rule can only list too much
    return frozenset(chain)


def _is_inside(path: str | None, folder: Path) -> bool:
    """True if a path is the folder or lies in it, comparing as Windows does (case and slashes set aside)."""
    if not path:
        return False
    inner = os.path.normcase(os.path.abspath(path))
    outer = os.path.normcase(os.path.abspath(str(folder)))
    return inner == outer or inner.startswith(outer.rstrip('\\/') + os.sep)


def _names_the_folder(command_line, folder: Path) -> bool:
    """True if any argument of a command line holds the folder's path as text (case set aside), ending where a
    path ends. T:\\a_p_r_i_r is named by 'T:\\a_p_r_i_r', 'T:\\a_p_r_i_r\\Run_Research.bat' and
    'cd /d "T:\\a_p_r_i_r"&& ...'; it is not named by 'T:\\a_p_r_i_r_backups\\QA', which is another folder whose
    name only begins the same way. The text is taken as the folder's path unless the character after it could
    continue a folder's name (a letter, a digit, or one of _ - . ~): a separator, a quote, a blank or any other
    mark ends it."""
    wanted = os.path.normcase(os.path.abspath(str(folder))).lower().rstrip('\\/')
    for argument in command_line or ():
        text = os.path.normcase(argument).lower()
        at = text.find(wanted)
        while at >= 0:
            after = text[at + len(wanted):at + len(wanted) + 1]
            if not after or not (after.isalnum() or after in NAME_CONTINUES):
                return True
            at = text.find(wanted, at + 1)
    return False


def processes_of_tree(table, tree_root: Path, left_out) -> list:
    """Apply the rule to a process table.

    table: ProcessSeen values, as read_process_table gives them.  tree_root: the tree's folder.
    left_out: the numbers of the asking program's own chain.
    Returns (process, reason) pairs, in the table's order, for every Python process that is of the tree or could
    not be read; for example [(ProcessSeen(4200, 4188, 'python.exe', ...), 'its working folder lies in the tree')].
    Empty when no other Python process of the tree is running.
    """
    by_number = {process.process_id: process for process in table}
    listed = []
    for process in table:
        if process.process_id in left_out or not is_python_name(process.name):
            continue
        if process.unreadable:
            listed.append((process, f'it is a Python process and {process.unreadable}: it cannot be shown not to '
                                    f'belong to the tree'))
            continue
        reason = None
        if _is_inside(process.program, tree_root):
            reason = 'its program file is the tree\'s own Python'
        elif _is_inside(process.working_folder, tree_root):
            reason = 'its working folder lies in the tree'
        else:
            above, walked = process, set()
            while above is not None and above.process_id not in walked:
                walked.add(above.process_id)
                if _names_the_folder(above.command_line, tree_root):
                    reason = ('its command line names the tree' if above is process
                              else f'the command line of process {above.process_id} above it names the tree')
                    break
                above = by_number.get(above.parent_id) if above.parent_id is not None else None
        if reason:
            listed.append((process, reason))
    return listed


def check_no_other_process_of_tree(tree_root: Path) -> int:
    """Refuse unless no other Python process of the tree is running.

    tree_root: the tree's folder.  Returns how many processes the table held (for the line the job prints).
    Refuses (ProcessRuleRefused), listing every process found with its number, its program, its working folder,
    its command line and the reason; or because the table could not be read.
    """
    table = read_process_table()
    listed = processes_of_tree(table, Path(tree_root), own_chain())
    if listed:
        lines = '\n  '.join(f'process {process.process_id} ({process.name}; program {process.program}; working '
                            f'folder {process.working_folder}; command line {" ".join(process.command_line or ())}): '
                            f'{reason}' for process, reason in listed)
        raise ProcessRuleRefused(f'{len(listed)} other Python process(es) of the tree {tree_root} are running; '
                                 f'nothing was started:\n  {lines}\n{WHAT_TO_DO}')
    return len(table)
