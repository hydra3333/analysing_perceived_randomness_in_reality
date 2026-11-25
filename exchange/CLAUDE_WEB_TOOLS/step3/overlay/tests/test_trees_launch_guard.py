"""Tests of the launch guard: the process rule, the environment's digest and marker, and the checks at every launch
and at the start of a job.

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; deployment design v0.12 sections 8 and 9; specification v0.6 sections 13
and 15). The process rule is tried on invented process tables, and once on a real one: a second Python that these
tests start, which waits for a line and then ends by itself. No test ends a process.

Which of the project's own modules it uses
    research_fixtures           invented trees, toy variants, and the job run in them
    research.process_rule, research.environment_marker, research.launch_guard     the code under test
    research.installed_files, research.research_job, research.settings

What uses it
    The project's test suite.
"""
import ast
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import research_fixtures as fx
from research import (environment_marker, installed_files, job_lock, launch_guard, process_rule, research_job,
                      settings, withdraw)
from research.process_rule import ProcessSeen

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_NAME = 'python.exe' if os.name == 'nt' else 'python3'


class TheProcessRuleOnInventedTables(unittest.TestCase):
    """Deployment design section 9: a Python process is of the tree by its program file, its working folder, or a
    command line (its own or one above it) that names the tree. Unrelated Python does not count."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.tree = Path(self.folder.name).resolve() / 'a_p_r_i_r'
        self.elsewhere = Path(self.folder.name).resolve() / 'other_work'
        self.tree.mkdir()
        self.elsewhere.mkdir()

    def tearDown(self):
        self.folder.cleanup()

    def python(self, number: int, parent: int = 1, **details) -> ProcessSeen:
        """An invented Python process that belongs nowhere unless a detail says so."""
        values = {'program': str(self.elsewhere / PYTHON_NAME), 'working_folder': str(self.elsewhere),
                  'command_line': (PYTHON_NAME, 'something.py')}
        values.update(details)
        return ProcessSeen(process_id=number, parent_id=parent, name=PYTHON_NAME, **values)

    def listed(self, *table, left_out=()) -> list:
        """The numbers of the processes the rule lists, with each reason."""
        return [(process.process_id, reason)
                for process, reason in process_rule.processes_of_tree(table, self.tree, frozenset(left_out))]

    def test_unrelated_python_work_on_the_pc_does_not_count(self):
        self.assertEqual(self.listed(self.python(10), self.python(11, working_folder=str(self.tree) + '_backups')), [])

    def test_a_command_line_naming_a_folder_whose_name_only_begins_like_the_trees_does_not_count(self):
        sibling = str(self.tree) + '_backups'                # as T:\\a_p_r_i_r_backups lies beside T:\\a_p_r_i_r
        for number, argument in enumerate((sibling, os.path.join(sibling, 'QA'), f'--to="{sibling}"',
                                           str(self.tree) + '.old', str(self.tree) + '2')):
            with self.subTest(argument=argument):
                self.assertEqual(self.listed(self.python(10 + number, command_line=(PYTHON_NAME, 'copy.py', argument))),
                                 [])
        window = ProcessSeen(process_id=5, parent_id=1, name='cmd.exe', command_line=('cmd.exe', '/c', f'dir {sibling}'))
        self.assertEqual(self.listed(window, self.python(30, parent=5)), [])

    def test_the_trees_path_is_named_wherever_a_path_ends_after_it(self):
        for number, argument in enumerate((str(self.tree), str(self.tree) + os.sep, f'"{self.tree}"',
                                           f'cd /d {self.tree}&& Run_Research.bat', f'--tree={self.tree};later',
                                           f'{self.tree}_backups {self.tree / "x.py"}')):
            with self.subTest(argument=argument):
                self.assertEqual(self.listed(self.python(10 + number, command_line=(PYTHON_NAME, argument))),
                                 [(10 + number, 'its command line names the tree')])

    def test_a_python_whose_program_file_is_the_trees_own_is_listed(self):
        found = self.listed(self.python(10, program=str(self.tree / '.venv' / 'Scripts' / PYTHON_NAME)))
        self.assertEqual(found, [(10, "its program file is the tree's own Python")])

    def test_a_python_whose_working_folder_is_the_tree_or_lies_in_it_is_listed(self):
        for folder in (self.tree, self.tree / 'src'):
            with self.subTest(folder=folder):
                self.assertEqual(self.listed(self.python(10, working_folder=str(folder))),
                                 [(10, 'its working folder lies in the tree')])

    def test_a_python_whose_command_line_names_the_tree_is_listed(self):
        found = self.listed(self.python(10, command_line=(PYTHON_NAME, str(self.tree / 'src' / 'research_command.py'))))
        self.assertEqual(found, [(10, 'its command line names the tree')])

    def test_the_base_python_under_the_trees_own_python_is_listed_through_its_parent(self):
        # Every program started from an environment is two processes on Windows (TASK_T028): the second has its
        # program file outside the tree and is found through the command line of the first.
        first = self.python(10, program=str(self.tree / '.venv' / 'Scripts' / PYTHON_NAME),
                            command_line=(str(self.tree / '.venv' / 'Scripts' / PYTHON_NAME), '-I', 'job.py'))
        second = self.python(11, parent=10, command_line=(PYTHON_NAME, '-I', 'job.py'))
        self.assertEqual([number for number, _ in self.listed(first, second)], [10, 11])
        self.assertIn('process 10 above it names the tree', self.listed(first, second)[1][1])

    def test_a_python_started_by_a_launcher_window_that_names_the_tree_is_listed(self):
        window = ProcessSeen(process_id=5, parent_id=1, name='cmd.exe',
                             command_line=('cmd.exe', '/c', str(self.tree / 'Run_Research.bat')))
        self.assertEqual(self.listed(window, self.python(10, parent=5)),
                         [(10, 'the command line of process 5 above it names the tree')])

    def test_a_program_that_is_not_python_is_never_listed_even_inside_the_tree(self):
        editor = ProcessSeen(process_id=7, parent_id=1, name='notepad.exe', program=str(self.tree / 'notepad.exe'),
                             working_folder=str(self.tree), command_line=('notepad.exe', str(self.tree / 'x.txt')))
        self.assertEqual(self.listed(editor), [])

    def test_a_python_process_that_cannot_be_read_is_listed_never_passed(self):
        unreadable = ProcessSeen(process_id=10, parent_id=1, name=PYTHON_NAME, unreadable='its command line could '
                                                                                         'not be read (AccessDenied)')
        found = self.listed(unreadable)
        self.assertEqual([number for number, _ in found], [10])
        self.assertIn('cannot be shown not to belong', found[0][1])

    def test_the_asking_programs_own_pair_and_its_window_are_left_out(self):
        mine = self.python(20, parent=19, working_folder=str(self.tree))
        my_first = self.python(19, parent=5, program=str(self.tree / '.venv' / 'Scripts' / PYTHON_NAME))
        another = self.python(30, working_folder=str(self.tree))
        self.assertEqual([number for number, _ in self.listed(mine, my_first, another, left_out=(20, 19, 5))], [30])

    def test_a_table_whose_parents_form_a_ring_is_walked_once_and_ends(self):
        self.assertEqual(self.listed(self.python(10, parent=11), self.python(11, parent=10)), [])


class TheProcessRuleOnThisPc(unittest.TestCase):
    """The table is read through psutil, and nothing is ever ended."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.tree = Path(self.folder.name).resolve() / 'tree'
        self.tree.mkdir()

    def tearDown(self):
        self.folder.cleanup()

    def test_the_table_holds_this_process_with_its_details_and_the_own_chain_holds_it(self):
        mine = [process for process in process_rule.read_process_table() if process.process_id == os.getpid()]
        self.assertEqual(len(mine), 1)
        self.assertTrue(process_rule.is_python_name(mine[0].name), mine[0].name)
        self.assertIsNone(mine[0].unreadable)
        self.assertTrue(mine[0].program and mine[0].working_folder and mine[0].command_line)
        self.assertIn(os.getpid(), process_rule.own_chain())

    def test_with_no_other_python_of_the_tree_the_check_passes_and_counts_what_it_looked_at(self):
        self.assertGreater(process_rule.check_no_other_process_of_tree(self.tree), 0)

    def test_a_second_python_working_in_the_tree_is_refused_and_listed_and_passes_once_it_has_ended_by_itself(self):
        waiting = subprocess.Popen([sys.executable, '-c', 'import sys; print("ready", flush=True); sys.stdin.readline()'],
                                   cwd=self.tree, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            self.assertEqual(waiting.stdout.readline().strip(), 'ready')
            with self.assertRaises(process_rule.ProcessRuleRefused) as refused:
                process_rule.check_no_other_process_of_tree(self.tree)
            message = str(refused.exception)
            self.assertIn('other Python process(es) of the tree', message)
            self.assertIn('nothing was started', message)
            self.assertIn('no program of this project ends a process', message)
        finally:
            waiting.stdin.write('end\n')         # it is told to finish, and finishes by itself
            waiting.stdin.close()
            waiting.wait()
            waiting.stdout.close()
        self.assertGreater(process_rule.check_no_other_process_of_tree(self.tree), 0)

    def test_the_rules_file_and_the_guards_hold_no_call_that_could_end_or_signal_a_process(self):
        for name in ('process_rule.py', 'launch_guard.py', 'environment_marker.py', 'installed_files.py'):
            tree = ast.parse((REPOSITORY_ROOT / 'src' / 'research' / name).read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    self.assertNotIn(node.attr, ('terminate', 'kill', 'send_signal', 'suspend', 'resume', 'system',
                                                 'popen', 'Popen'), f'{name} uses .{node.attr}')
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    names = [alias.name for alias in node.names] + [getattr(node, 'module', None) or '']
                    self.assertFalse({'subprocess', 'signal'} & {text.split('.')[0] for text in names}, name)


class InventedEnvironment(unittest.TestCase):
    """An invented environment folder in the Windows layout: pyvenv.cfg, Scripts and Lib/site-packages."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.venv = Path(self.folder.name).resolve() / '.venv'
        for relative, data in (('pyvenv.cfg', b'home = C:\\Python315\r\n'), ('Scripts/python.exe', b'MZ invented'),
                               ('Lib/site-packages/toy/__init__.py', b'VALUE = 1\r\n'),
                               ('Lib/site-packages/toy-1.0.dist-info/METADATA', b'Name: toy\r\n')):
            (self.venv / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.venv / relative).write_bytes(data)

    def tearDown(self):
        self.folder.cleanup()

    def digest(self) -> str:
        """The environment's digest now."""
        return environment_marker.environment_digest(self.venv)[0]


class TheEnvironmentsDigest(InventedEnvironment):
    """Specification section 13: the digest is taken over a fixed inventory and does not include its own marker."""

    def test_it_counts_the_files_of_the_inventory_and_is_the_same_when_nothing_changed(self):
        digest, files_read = environment_marker.environment_digest(self.venv)
        self.assertEqual(files_read, 5)                      # the four files of the inventory and the base program
        self.assertRegex(digest, r'^[0-9a-f]{64}$')
        self.assertEqual(self.digest(), digest)

    def test_a_change_in_any_part_of_the_inventory_changes_it(self):
        before = self.digest()
        for relative in ('pyvenv.cfg', 'Scripts/python.exe', 'Lib/site-packages/toy/__init__.py'):
            with self.subTest(relative=relative):
                kept = (self.venv / relative).read_bytes()
                (self.venv / relative).write_bytes(kept + b'changed')
                self.assertNotEqual(self.digest(), before)
                (self.venv / relative).write_bytes(kept)
                self.assertEqual(self.digest(), before)
        (self.venv / 'Scripts' / 'added.exe').write_bytes(b'MZ')
        self.assertNotEqual(self.digest(), before)

    def test_pythons_caches_compiled_files_and_files_outside_the_inventory_do_not_change_it(self):
        before = self.digest()
        cache = self.venv / 'Lib' / 'site-packages' / 'toy' / '__pycache__'
        cache.mkdir()
        (cache / '__init__.cpython-315.pyc').write_bytes(b'\x00')
        (cache / 'a_file_that_is_not_compiled.txt').write_bytes(b'still inside a cache folder\r\n')
        (self.venv / 'Lib' / 'site-packages' / 'toy' / 'stray.pyc').write_bytes(b'\x00')
        (self.venv / 'Include').mkdir()
        (self.venv / 'Include' / 'note.txt').write_bytes(b'not in the inventory\r\n')
        self.assertEqual(self.digest(), before)

    def test_the_base_pythons_program_file_enters_by_its_bytes_and_not_only_by_its_path_and_version(self):
        program = Path(self.folder.name).resolve() / 'base' / 'python.exe'       # an invented base program file
        program.parent.mkdir()
        program.write_bytes(b'MZ the base Python as it was when the environment was verified')
        with mock.patch.object(environment_marker, 'base_python', lambda: ('3.15.0 invented', str(program))):
            before = self.digest()
            self.assertEqual(self.digest(), before)
            program.write_bytes(b'MZ another program put at the same path, saying the same version')
            self.assertNotEqual(self.digest(), before)
            program.write_bytes(b'MZ the base Python as it was when the environment was verified')
            self.assertEqual(self.digest(), before)
            program.unlink()
            with self.assertRaisesRegex(environment_marker.EnvironmentRefused, 'base Python\'s program file, could '
                                                                               'not be read'):
                self.digest()
            program.write_bytes(b'MZ the base Python as it was when the environment was verified')
        with mock.patch.object(environment_marker, 'base_python', lambda: ('3.15.1 invented', str(program))):
            self.assertNotEqual(self.digest(), before)       # another version at the same path, the same bytes

    def test_an_environment_that_lacks_a_part_of_the_inventory_refuses_and_names_the_part(self):
        aside = self.venv.parent / 'kept_aside'
        for part in ('pyvenv.cfg', 'Scripts', 'Lib/site-packages'):
            with self.subTest(part=part):
                os.rename(self.venv / part, aside)
                with self.assertRaisesRegex(environment_marker.EnvironmentRefused,
                                            f'it has no {part.replace(".", chr(92) + ".")}' + r'\. Nothing was started'):
                    self.digest()
                with self.assertRaises(environment_marker.EnvironmentRefused):
                    environment_marker.write_marker(self.venv)
                self.assertFalse((self.venv / 'ENVIRONMENT_VERIFIED.json').exists())
                os.rename(aside, self.venv / part)
        self.assertRegex(self.digest(), r'^[0-9a-f]{64}$')

    def test_a_folder_of_the_inventory_that_cannot_be_listed_refuses_and_is_not_left_out(self):
        closed = str(self.venv / 'Lib' / 'site-packages' / 'toy')
        listing = os.scandir

        def scandir(path='.'):
            """As os.scandir, but the one folder cannot be listed, as a folder held or forbidden on Windows."""
            if os.fspath(path) == closed:
                raise PermissionError(13, 'Access is denied', closed)
            return listing(path)

        with mock.patch('os.scandir', scandir):
            with self.assertRaisesRegex(environment_marker.EnvironmentRefused, 'could not be read'):
                self.digest()
        self.assertRegex(self.digest(), r'^[0-9a-f]{64}$')

    def test_writing_the_marker_changes_nothing_that_is_hashed(self):
        before = self.digest()
        self.assertEqual(environment_marker.write_marker(self.venv), before)
        self.assertEqual(self.digest(), before)
        self.assertEqual(sorted(path.name for path in self.venv.iterdir() if path.is_file()),
                         ['ENVIRONMENT_VERIFIED.json', 'pyvenv.cfg'])

    def test_an_environment_folder_that_does_not_exist_refuses(self):
        with self.assertRaisesRegex(environment_marker.EnvironmentRefused, 'does not exist'):
            environment_marker.environment_digest(self.venv.parent / 'no_such_venv')


class TheEnvironmentsMarker(InventedEnvironment):
    """Specification section 13 and deployment design section 9: launchers refuse without the marker; a job
    compares the digest at its start."""

    def test_the_marker_is_a_text_file_with_every_line_ending_crlf_and_the_same_bytes_twice(self):
        environment_marker.write_marker(self.venv)
        first = (self.venv / 'ENVIRONMENT_VERIFIED.json').read_bytes()
        environment_marker.write_marker(self.venv)
        self.assertEqual((self.venv / 'ENVIRONMENT_VERIFIED.json').read_bytes(), first)
        self.assertEqual(first.count(b'\n'), first.count(b'\r\n'))
        self.assertGreater(first.count(b'\r\n'), 4)

    def test_no_marker_is_environment_not_verified_and_names_verify_tree(self):
        with self.assertRaisesRegex(environment_marker.EnvironmentRefused, 'environment not verified.*Verify_Tree.bat'):
            environment_marker.read_marker(self.venv)

    def test_a_marker_that_is_not_json_or_not_of_its_kind_refuses(self):
        for data in (b'{ not json\r\n', b'{"kind": "SOMETHING_ELSE", "digest": "x", "distributions": []}\r\n'):
            with self.subTest(data=data):
                (self.venv / 'ENVIRONMENT_VERIFIED.json').write_bytes(data)
                with self.assertRaises(environment_marker.EnvironmentRefused):
                    environment_marker.read_marker(self.venv)

    def test_the_first_gate_passes_when_the_marker_lists_what_is_installed_and_names_a_package_that_changed(self):
        environment_marker.write_marker(self.venv)
        environment_marker.check_marker_lists_what_is_installed(self.venv)
        installed = environment_marker.installed_distributions()
        (self.venv / 'ENVIRONMENT_VERIFIED.json').write_bytes(
            environment_marker.marker_bytes(self.digest(), installed[1:] + ['invented_package 9.9']))
        with self.assertRaises(environment_marker.EnvironmentRefused) as refused:
            environment_marker.check_marker_lists_what_is_installed(self.venv)
        self.assertIn(f'installed since: {installed[0]}', str(refused.exception))
        self.assertIn('no longer installed: invented_package 9.9', str(refused.exception))

    def test_a_file_changed_after_verification_is_environment_not_verified(self):
        environment_marker.write_marker(self.venv)
        environment_marker.check_digest_is_the_markers(self.venv, self.digest())
        with open(self.venv / 'Lib' / 'site-packages' / 'toy' / '__init__.py', 'ab') as handle:
            handle.write(b'VALUE = 2\r\n')
        with self.assertRaisesRegex(environment_marker.EnvironmentRefused, 'environment not verified'):
            environment_marker.check_digest_is_the_markers(self.venv, self.digest())


class EveryLaunch(fx.JobCase):
    """Deployment design sections 8 and 9: at every launch, no unfinished operation; in QA and PROD the marker."""

    def test_each_unfinished_operations_file_refuses_every_launch_and_is_named_with_the_way_on(self):
        tree = self.tree(role='DEV', with_source=False)
        launch_guard.check_at_launch(tree)
        (tree / 'records').mkdir(exist_ok=True)
        self.assertEqual(len(launch_guard.UNFINISHED_OPERATIONS), 5)
        for relative, meaning, way_on in launch_guard.UNFINISHED_OPERATIONS:
            with self.subTest(relative=relative):
                (tree / relative).write_bytes(b'{}\r\n')
                with self.assertRaises(launch_guard.GuardRefused) as refused:
                    launch_guard.check_at_launch(tree)
                self.assertIn(str(tree / relative), str(refused.exception))
                self.assertIn(way_on, str(refused.exception))
                (tree / relative).unlink()

    def test_only_the_command_that_finishes_an_operation_passes_that_operations_file(self):
        tree = self.tree(role='DEV', with_source=False)
        (tree / 'records').mkdir(exist_ok=True)
        install, rerun = (launch_guard.UNFINISHED_OPERATIONS[0][0], launch_guard.UNFINISHED_OPERATIONS[1][0])
        (tree / install).write_bytes(b'{}\r\n')
        launch_guard.check_at_launch(tree, finishing=install)
        with self.assertRaises(launch_guard.GuardRefused):
            launch_guard.check_at_launch(tree, finishing=rerun)

    def test_in_qa_a_launch_refuses_without_the_environments_marker_and_dev_is_asked_for_none(self):
        qa = self.tree(with_source=False)
        (qa / '.venv' / 'ENVIRONMENT_VERIFIED.json').unlink()
        with self.assertRaisesRegex(environment_marker.EnvironmentRefused, 'environment not verified'):
            launch_guard.check_at_launch(qa)
        environment_marker.write_marker(qa / '.venv')
        self.assertEqual(launch_guard.check_at_launch(qa).role, 'QA')
        self.assertEqual(launch_guard.check_at_launch(self.tree(role='DEV', with_source=False, name='dev')).role, 'DEV')

    def test_the_launcher_makes_the_guards_checks_before_it_hands_over_to_a_command(self):
        text = (REPOSITORY_ROOT / 'src' / 'research_command.py').read_text(encoding='utf-8')
        self.assertLess(text.index('check_at_launch(TREE_ROOT)'), text.index('from research.research_job import main'))
        self.assertLess(text.index('check_at_launch(TREE_ROOT)'), text.index('from research.withdraw import main'))


class TheStartOfAJob(fx.JobCase):
    """Deployment design section 9: at the start of a job the environment's digest is computed; in QA and PROD it
    equals the marker's and the software matches its list; in every tree no other Python of the tree runs."""

    def installed(self, **options) -> Path:
        """A QA tree as the project's commands would leave it: its list and its environment's marker made."""
        return self.tree(with_source=False, **options)       # the fixture leaves a QA tree as installed

    def job(self, tree: Path) -> tuple:
        """Run the job itself, with nothing made ready for it; return (exit code, what it said as one text)."""
        said = []
        with fx.ImportPath(tree):
            code = research_job.run(tree, (fx.GAME,), now=lambda: fx.FIXED_TIME, say=said.append, no_update=True)
        return code, '\n'.join(said)

    def test_a_job_in_an_installed_tree_says_what_it_checked_and_every_forecast_carries_the_environments_digest(self):
        tree = self.installed()
        code, text = self.job(tree)
        self.assertEqual(code, 0, text)
        self.assertIn('Reading this tree\'s own Python environment', text)
        self.assertIn('The environment is the one that was verified, and the software matches its list', text)
        self.assertIn('No other Python process of this tree is running', text)
        digest = environment_marker.environment_digest(tree / '.venv')[0]
        forecasts = fx.list_lines(tree, 'E_901', 'TOY_A_V1')
        self.assertGreater(len(forecasts), 3)
        self.assertEqual({line['envelope']['environment_digest'] for line in forecasts}, {digest})

    def test_in_dev_neither_a_marker_nor_a_list_is_asked_and_the_digest_is_still_taken(self):
        tree = self.tree(role='DEV', with_source=False)
        code, text = self.job(tree)
        self.assertEqual(code, 0, text)
        self.assertIn('The environment: ', text)
        self.assertNotIn('the one that was verified', text)
        self.assertIn('No other Python process of this tree is running', text)

    def refused(self, tree: Path, *words) -> str:
        """Run the job, expect it to refuse before any game with nothing written, and return what it said."""
        code, text = self.job(tree)
        self.assertEqual(code, research_job.EXIT_REFUSED, text)
        for word in words:
            self.assertIn(word, text)
        self.assertIn('refused before any game was worked; nothing was written', text)
        self.assertFalse((tree / 'results' / 'research').exists())
        return text

    def test_a_helper_or_any_installed_file_changed_outside_the_tools_refuses_the_job_and_is_named(self):
        tree = self.installed()
        with open(tree / 'src' / 'toy_forecast_code.py', 'ab') as handle:
            handle.write(b'# changed by hand\r\n')
        self.refused(tree, 'src/toy_forecast_code.py: its bytes are not the bytes that were installed',
                     'restore from a backup you choose')

    def test_an_unlisted_python_file_under_src_refuses_the_job_and_is_named(self):
        tree = self.installed()
        (tree / 'src' / 'stray.py').write_bytes(b'# not installed\r\n')
        self.refused(tree, 'src/stray.py: it lies under src and is not on the list of installed files')

    def test_a_tree_without_its_list_refuses_the_job(self):
        tree = self.installed()
        (tree / installed_files.LIST_PATH).unlink()
        self.refused(tree, 'this tree has no list of installed files')

    def test_an_environment_file_changed_after_verification_refuses_the_job(self):
        tree = self.installed()
        (tree / '.venv' / 'Scripts' / 'added.exe').write_bytes(b'MZ')
        self.refused(tree, 'environment not verified')

    def test_an_operation_left_unfinished_refuses_the_job_itself_under_its_lock_and_not_only_the_launcher(self):
        tree = self.tree(role='DEV', with_source=False)      # the job is run here without its launcher
        (tree / 'records').mkdir(exist_ok=True)
        (tree / launch_guard.UNFINISHED_OPERATIONS[1][0]).write_bytes(b'{}\r\n')
        text = self.refused(tree, 'a historical walk-forward rerun did not finish in this tree')
        self.assertNotIn('Reading this tree\'s own Python environment', text)

    def test_an_environment_with_no_marker_refuses_the_job(self):
        tree = self.installed()
        (tree / '.venv' / 'ENVIRONMENT_VERIFIED.json').unlink()
        self.refused(tree, 'environment not verified', 'Verify_Tree.bat')

    def test_another_python_process_working_in_the_tree_refuses_the_job_in_dev_as_in_any_tree(self):
        tree = self.tree(role='DEV', with_source=False)
        waiting = subprocess.Popen([sys.executable, '-c', 'import sys; print("ready", flush=True); sys.stdin.readline()'],
                                   cwd=tree, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            self.assertEqual(waiting.stdout.readline().strip(), 'ready')
            self.refused(tree, 'other Python process(es) of the tree', 'no program of this project ends a process')
        finally:
            waiting.stdin.write('end\n')         # it is told to finish, and finishes by itself
            waiting.stdin.close()
            waiting.wait()
            waiting.stdout.close()
        self.assertEqual(self.job(tree)[0], 0)

    def test_a_trees_settings_role_is_what_decides_and_no_caller_can_switch_a_check_off(self):
        # The guard's two functions take the tree and nothing that could point a check elsewhere.
        tree = ast.parse((REPOSITORY_ROOT / 'src' / 'research' / 'launch_guard.py').read_text(encoding='utf-8'))
        arguments = {node.name: [argument.arg for argument in node.args.args] for node in ast.walk(tree)
                     if isinstance(node, ast.FunctionDef)}
        self.assertEqual(arguments['check_at_job_start'], ['settings', 'say'])
        self.assertEqual(arguments['check_at_launch'], ['tree_root', 'finishing'])
        self.assertEqual(settings.ROLES, ('DEV', 'QA', 'PROD'))


class AWithdrawalInAnInstalledTree(fx.JobCase):
    """Deployment design section 8 (last row) and specification 11: a withdrawal is one-way, so it is not written
    in a QA or PROD tree whose software is not the software that was installed, nor in any tree while an operation
    is unfinished. It checks while it holds its two locks, before it reads, tidies or writes anything; it reads no
    file of the environment and no process table (deployment design section 9 gives it its own rule)."""

    REASON = 'a test of the guard'

    def withdrawal(self, tree: Path) -> tuple:
        """Try to withdraw TOY_B_V1 by the command's own route, confirming when asked; return (exit code, what it
        said as one text)."""
        said = []
        code = withdraw.withdraw(tree, [('E_901', 'TOY_B_V1')], (fx.GAME,), self.REASON,
                                 ask=lambda question: 'WITHDRAW', say=said.append, now=lambda: fx.FIXED_TIME)
        return code, '\n'.join(said)

    def everything_the_withdrawal_could_change(self, tree: Path) -> dict:
        """The software with its status files, and the records with the tree's log and the staging folder."""
        return {**fx.files_under(tree, 'src'), **fx.files_under(tree, 'records')}

    def refused_with_nothing_changed(self, tree: Path, *words) -> None:
        """The withdrawal refuses naming each of `words`; no status, no log line and no staged file changes."""
        before = self.everything_the_withdrawal_could_change(tree)
        code, text = self.withdrawal(tree)
        self.assertEqual(code, withdraw.EXIT_NOTHING_WRITTEN, text)
        for word in words:
            self.assertIn(word, text)
        self.assertIn('refused; no status file was changed by this command', text)
        self.assertEqual(self.everything_the_withdrawal_could_change(tree), before)
        self.assertIsNone(self.status(tree, 'TOY_B_V1').withdrawn_from)

    def test_in_a_tree_as_installed_the_withdrawal_is_written_and_logged(self):
        tree = self.tree()
        code, text = self.withdrawal(tree)
        self.assertEqual(code, withdraw.EXIT_DONE, text)
        self.assertEqual(self.status(tree, 'TOY_B_V1').withdrawn_from, fx.LAST_AT_START + 1)
        self.assertIn('"operation": "WITHDRAWAL"', (tree / 'records' / withdraw.TREE_LOG_NAME).read_text('ascii'))

    def test_a_helper_changed_outside_the_tools_refuses_the_withdrawal_before_any_status_or_log_change(self):
        tree = self.tree()
        with open(tree / 'src' / 'toy_forecast_code.py', 'ab') as handle:
            handle.write(b'# changed by hand\r\n')
        self.refused_with_nothing_changed(tree, 'src/toy_forecast_code.py: its bytes are not the bytes that were '
                                                'installed', 'restore from a backup you choose')

    def test_an_unlisted_python_file_under_src_refuses_the_withdrawal(self):
        tree = self.tree()
        (tree / 'src' / 'stray.py').write_bytes(b'# not installed\r\n')
        self.refused_with_nothing_changed(tree, 'src/stray.py: it lies under src and is not on the list of '
                                                'installed files')

    def test_a_tree_without_its_list_refuses_the_withdrawal(self):
        tree = self.tree()
        (tree / installed_files.LIST_PATH).unlink()
        self.refused_with_nothing_changed(tree, 'this tree has no list of installed files')

    def test_the_refusal_comes_before_an_interrupted_status_write_is_tidied_away(self):
        tree = self.tree()
        staged = tree / 'records' / 'status_staging' / 'E_901__TOY_B_V1__VARIANT_STATUS.ini.writing'
        staged.parent.mkdir(parents=True, exist_ok=True)
        staged.write_bytes(b'left by an interrupted status write\r\n')
        (tree / 'src' / 'stray.py').write_bytes(b'# not installed\r\n')
        self.refused_with_nothing_changed(tree, 'src/stray.py')
        self.assertTrue(staged.exists())

    def test_an_operation_left_unfinished_refuses_the_withdrawal_in_every_tree(self):
        for role in ('QA', 'DEV'):
            with self.subTest(role=role):
                tree = self.tree(role=role, name=f'tree_{role}')
                barrier = tree / launch_guard.UNFINISHED_OPERATIONS[0][0]
                barrier.parent.mkdir(exist_ok=True)
                barrier.write_bytes(b'{}\r\n')
                self.refused_with_nothing_changed(tree, f'{barrier} exists', 'did not finish in this tree')

    def test_the_orphan_marker_still_refuses_the_withdrawal(self):
        tree = self.tree()
        marker = tree / job_lock.ORPHAN_MARKER
        marker.parent.mkdir(parents=True)
        marker.write_bytes(b'[]\r\n')
        code, text = self.withdrawal(tree)
        self.assertEqual(code, withdraw.EXIT_NOTHING_WRITTEN, text)
        self.assertIn('orphan marker present', text)
        self.assertIsNone(self.status(tree, 'TOY_B_V1').withdrawn_from)

    def test_in_dev_no_list_is_asked_of_a_withdrawal(self):
        tree = self.tree(role='DEV')
        self.assertFalse((tree / installed_files.LIST_PATH).exists())
        self.assertEqual(self.withdrawal(tree)[0], withdraw.EXIT_DONE)

    def test_a_withdrawal_reads_no_file_of_the_environment_and_no_process_table(self):
        tree = self.tree()

        def never(*arguments):
            raise AssertionError('a withdrawal must not take the environment\'s digest or read the process table')

        with mock.patch.object(environment_marker, 'environment_digest', never), \
                mock.patch.object(process_rule, 'read_process_table', never):
            self.assertEqual(self.withdrawal(tree)[0], withdraw.EXIT_DONE)


if __name__ == '__main__':
    unittest.main()
