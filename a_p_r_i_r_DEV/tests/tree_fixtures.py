"""Fixtures for the tests of DEV's commands that touch another tree: three invented trees that know of one another.

What this file is for
    The tests of Create_Tree, Install, Retire, Copy_From_PROD and Restore need a DEV tree and, made from it by
    the real Create_Tree, a QA and a PROD tree, all under one temporary folder, with stand-ins for the two things
    a test must not really do each time: the backup before a replacement (noted, not made, unless the test is
    about it) and the destination's own research job (run inside the test's process, under the lock the command
    holds, with the key it was given). Everything is invented: toy methods, invented draws.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 9 (tests on invented games and toy methods).

Which of the project's own modules it uses
    research_fixtures        the invented trees, results and toy methods
    dev_tools, install_tools the real "make installable" and "create tree"
    research.settings        read_settings

What uses it
    tests/test_research_install.py and tests/test_research_tree_moves.py.
"""
from __future__ import annotations

import inspect
import sys
from datetime import datetime
from pathlib import Path

TREE_OF_THIS_FILE = Path(__file__).resolve().parents[1]
if str(TREE_OF_THIS_FILE / 'deploy') not in sys.path:
    sys.path.insert(0, str(TREE_OF_THIS_FILE / 'deploy'))

import dev_tools                                            # noqa: E402  (after the path line above)
import install_tools                                        # noqa: E402
import research_fixtures as fx                              # noqa: E402
from research.settings import read_settings                 # noqa: E402

# The moment every command of a test is given as "now".
MOMENT = datetime(2026, 12, 1, 20, 10, 12)
# Invented launchers every invented DEV tree holds at its root (two of the real names).
TOY_ROOT_FILES = ('Run_Research.bat', 'Backup.bat')
# The invented updater's one file, from the tree root.
TOY_UPDATER = 'src/updater/results_updater.py'


def give_python(tree: Path) -> None:
    """Put a file where a tree's own Python would be, so that a command sees that the tree has an environment.
    (No test starts it: the destination's job is a stand-in, except in the one test that makes a real one.)"""
    (tree / '.venv' / 'Scripts').mkdir(parents=True, exist_ok=True)
    (tree / '.venv' / 'Scripts' / 'python.exe').write_bytes(b'not a real Python')


def edit(path: Path, text: str) -> None:
    """Add a line to a text file of a tree: the smallest change that makes its bytes other bytes. The line is
    written as bytes ending LF, so that a test sees the same bytes on Windows and elsewhere."""
    with open(path, 'ab') as stream:
        stream.write(text.encode('ascii') + b'\n')


class TreesCase(fx.JobCase):
    """Three invented trees under the test's temporary folder: DEV made here, QA and PROD by Create_Tree."""

    def setUp(self):
        """Lay out the three places; note what the stand-ins are asked."""
        super().setUp()
        self.places = fx.three_places(self.root)
        self.said, self.backups, self.jobs, self.job_code = [], [], [], None

    def place(self, role: str) -> Path:
        """Where the tree of a role lies (or would lie)."""
        return self.places[role][0]

    def settings(self, role: str = 'DEV'):
        """A tree's settings, read from its own file."""
        return read_settings(self.place(role))

    def dev(self, variants=('TOY_A_V1', 'TOY_B_V1'), flag=('ALL', 'INFRA')) -> Path:
        """Make the DEV tree: invented results, toy methods, an invented engine file, updater and launchers; and
        flag what is named (nothing if flag is empty)."""
        tree = fx.make_tree(self.place('DEV'), 'DEV', places=self.places)
        fx.write_results(tree, fx.GAME, fx.LAST_AT_START)
        for entry in variants:
            self.add_variant(tree, *((entry,) if isinstance(entry, str) else entry))
        (tree / TOY_UPDATER).parent.mkdir()
        (tree / TOY_UPDATER).write_text('# an invented updater\n', encoding='ascii')
        for name in TOY_ROOT_FILES:
            (tree / name).write_text(f'rem an invented {name}\n', encoding='ascii')
        give_python(tree)
        if flag:
            self.flag(*flag)
        return tree

    def flag(self, *names) -> None:
        """Run the real Make_Installable in DEV for the names given, for example self.flag('ALL', 'INFRA')."""
        code = dev_tools.make_installable(self.settings(), list(names), MOMENT, say=lambda line: None)
        self.assertEqual(code, 0, names)

    def create(self, role: str = 'QA') -> Path:
        """Make the QA or the PROD tree with the real Create_Tree and give it a place-holder Python."""
        code = install_tools.create_tree(self.settings(), role, moment=MOMENT, say=self.said.append)
        self.assertEqual(code, 0, self.said)
        give_python(self.place(role))
        return self.place(role)

    def backup_noted(self, settings, why, moment) -> Path:
        """The stand-in for the backup before a replacement: note which tree and why; make nothing."""
        self.backups.append((settings.role, why))
        return Path(f'{settings.role}_20261201_201012_{why.replace(" ", "_")}.zip')

    def job_in_process(self, settings, key: str, say) -> int:
        """The stand-in for a tree's own job: the real job, run inside the test's process in that tree, under
        the lock the command holds (it is given the key). A test may set self.job_code to plant its exit code."""
        self.jobs.append((settings.role, key))
        if self.job_code is not None:
            return self.job_code
        code, self.job_said = fx.run_job(settings.tree_root, under_lock=key)
        return code

    def command(self, function, *arguments, **options) -> int:
        """Run one cross-tree command with DEV's settings, the test's moment and the stand-ins; what it says
        goes to self.said. For example self.command(install_tools.install, 'QA', show=False)."""
        for name, stand_in in (('backup', self.backup_noted), ('run_job', self.job_in_process)):
            if name in inspect.signature(function).parameters:
                options.setdefault(name, stand_in)
        return function(self.settings(), *arguments, moment=MOMENT, say=self.said.append, **options)

    def snapshot(self, role: str) -> dict:
        """Every file of a tree with its bytes, to show afterwards that a refused command changed nothing."""
        return fx.files_under(self.place(role), '.', leave_out=())

    def said_text(self) -> str:
        """Everything the commands of the test said, as one text."""
        return '\n'.join(self.said)

    def lock_of(self, role: str) -> Path:
        """Where a tree's lock file is while a command holds it."""
        return self.place(role) / 'records' / 'TREE.lock'

    def no_lock_is_left(self) -> bool:
        """True if no tree of the test holds a lock file."""
        return not any(self.lock_of(role).exists() for role in self.places)
