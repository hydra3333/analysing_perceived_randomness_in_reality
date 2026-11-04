"""MHUP-A (design v0.1r5 section 6.1, section 7 A7, Appendix J; Appendix L item L-I4 and the process-tool statics):
process_check.py on mocked process tables. OFFLINE; no process is started, examined or touched: every table here is
invented. The static tests show the tool imports nothing under src/methods/ or src/evaluation/ and contains no
terminating call.
"""
from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'src' / 'package_tools' / 'process_check.py'


def load():
    spec = importlib.util.spec_from_file_location('process_check', TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['process_check'] = mod                 # dataclasses resolve annotations through sys.modules
    spec.loader.exec_module(mod)
    return mod


PC = load()
PYEXE = 'python.exe' if os.name == 'nt' else 'python3'


def proc(pid, ppid, *, exe=None, cwd=None, cmdline=None, name=PYEXE, error=None, create_time=1.0):
    return PC.Proc(pid=pid, ppid=ppid, name=name, exe=exe, cwd=cwd, cmdline=cmdline, create_time=create_time, error=error)


class Harness(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name).resolve() / 'project'
        for sub in ('src', 'source_data', 'results', '.git', '.venv'):
            (self.root / sub).mkdir(parents=True)
        (self.root / '.venv' / 'pyvenv.cfg').write_text(f'home = {Path(self._td.name) / "base" / "bin"}\nversion = 3.99\n')
        self.venv_py = PC.venv_python(self.root)
        self.base_py = PC.base_python(self.root)
        self.elsewhere = Path(self._td.name).resolve() / 'elsewhere'
        self.elsewhere.mkdir()
        self.out = []

    def tearDown(self):
        self._td.cleanup()

    def run_tool(self, argv, table, exclude=frozenset()):
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            rc = PC.main(argv, table=list(table), exclude=set(exclude))
        finally:
            sys.stdout = real
        self.out = buf.getvalue().splitlines()
        return rc

    def check(self, table, *extra, exclude=frozenset()):
        return self.run_tool(['check-no-runs', '--root', str(self.root), *extra], table, exclude)


class MockedTables(Harness):

    def test_the_rule_of_6_1_on_each_kind_of_process(self):
        shell = proc(10, 1, exe='/bin/bash', cwd=str(self.elsewhere), cmdline=['bash'], name='bash')
        # (a) a live redirector child: its executable is the venv's Python
        redirector = proc(20, 10, exe=str(self.venv_py), cwd=str(self.elsewhere), cmdline=['python', 'x.py'])
        self.assertEqual(self.check([shell, redirector]), 1)
        self.assertIn('executable is the project venv or its base interpreter', '\n'.join(self.out))
        self.assertTrue(self.out[-1].startswith('REFUSED: 1 project Python process'))
        self.assertIn('never terminates anything', self.out[-1])
        # (a') the base interpreter named in pyvenv.cfg, started by the redirector: its own command line is silent,
        # its ancestor's names the root
        launcher = proc(30, 10, exe='/usr/bin/cmd', cwd=str(self.elsewhere), name='cmd.exe',
                        cmdline=['cmd', '/c', str(self.root / 'Run_Experiment.bat'), 'E.py'])
        base = proc(31, 30, exe=str(self.base_py), cwd=str(self.elsewhere), cmdline=['python', '-u', 'E.py'])
        self.assertEqual(self.check([shell, launcher, base]), 1)
        text = '\n'.join(self.out)
        self.assertIn('command line names the project root (ancestor 30)', text)
        self.assertIn('executable is the project venv or its base interpreter', text)
        # (b) a process whose current directory is under the project root
        cwd_proc = proc(40, 10, exe='/usr/bin/python3.12', cwd=str(self.root / 'src' / 'methods'), cmdline=['python3', '-c', 'pass'])
        self.assertEqual(self.check([shell, cwd_proc]), 1)
        self.assertIn('current directory under the project root', '\n'.join(self.out))
        # (c) a process whose own command line names the root, from elsewhere
        cmd_proc = proc(50, 10, exe='/usr/bin/python3.12', cwd=str(self.elsewhere), cmdline=['python3', str(self.root / 'src' / 'x.py')])
        self.assertEqual(self.check([shell, cmd_proc]), 1)
        self.assertIn('command line names the project root', '\n'.join(self.out))
        # (d) a Python process whose details cannot be read: a refusal, never CLEAN
        denied = proc(60, 10, error='exe: AccessDenied')
        self.assertEqual(self.check([shell, denied]), 1)
        self.assertIn('unreadable: exe: AccessDenied', '\n'.join(self.out))
        # an unrelated Python elsewhere, a non-Python process at the root, and an exited child (absent): CLEAN
        unrelated = proc(70, 10, exe='/usr/bin/python3.12', cwd=str(self.elsewhere), cmdline=['python3', 'other.py'])
        editor = proc(80, 10, exe='/usr/bin/code', cwd=str(self.root), cmdline=['code', str(self.root)], name='code')
        self.assertEqual(self.check([shell, unrelated, editor]), 0)
        self.assertEqual(self.out, ['CLEAN'])
        # this tool's own chain is never listed, even when it runs from the root
        me = proc(90, 10, exe=str(self.venv_py), cwd=str(self.root), cmdline=['python', 'process_check.py'])
        self.assertEqual(self.check([shell, me], exclude={90, 10}), 0)
        self.assertEqual(self.check([shell, me]), 1)
        # the description names PID, creation time, parent chain, executable and command line
        self.assertEqual(self.check([shell, redirector]), 1)
        line = next(l for l in self.out if l.strip().startswith('PID 20'))
        for frag in ('PID 20', 'created 1970-01-01T00:00:01', 'parents [10]', "exe '", "cmdline ['python', 'x.py']"):
            self.assertIn(frag, line)

    def test_root_argument_is_validated(self):
        self.assertEqual(self.run_tool(['check-no-runs', '--root', 'relative/path'], []), 1)
        self.assertIn('--root must be an absolute path', self.out[-1])
        self.assertEqual(self.run_tool(['check-no-runs', '--root', str(self.elsewhere)], []), 1)
        self.assertIn('does not look like the project root', self.out[-1])
        import contextlib
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                PC.main(['check-no-runs'], table=[], exclude=set())
            with self.assertRaises(SystemExit):
                PC.main(['clear-session-lock', '--root', str(self.root)], table=[], exclude=set())


class LocksAndRecords(Harness):

    def test_session_lock_resume_token_and_clearance(self):
        lock = PC.session_lock(self.root, 'POWERBALL')
        lock.parent.mkdir(parents=True)
        self.assertEqual(self.run_tool(['clear-session-lock', '--root', str(self.root), '--game', 'POWERBALL'], []), 1)
        self.assertIn('no session lock', self.out[-1])
        lock.write_text('0123456789abcdef0123456789abcdef 2026-11-20T10:00:00Z')
        live = proc(20, 1, exe=str(self.venv_py), cwd=str(self.root), cmdline=['python', 'Method_Weekly_Forecast.py'])
        # with a live process: refused, the lock stays, no token, no record
        self.assertEqual(self.check([live], '--game', 'POWERBALL'), 1)
        self.assertTrue(lock.exists())
        self.assertEqual(list((self.root / 'results' / 'real' / 'weekly' / 'POWERBALL').rglob('RESUME_*')), [])
        self.assertEqual(self.run_tool(['clear-session-lock', '--root', str(self.root), '--game', 'POWERBALL'], [live]), 1)
        self.assertTrue(lock.exists())
        self.assertFalse((self.root / 'transitory_data').exists())
        # CLEAN with --game and the lock present: a resume token is written, the lock stays
        self.assertEqual(self.check([], '--game', 'POWERBALL'), 0)
        self.assertIn('resume token written', self.out[-1])
        tokens = list((self.root / 'results' / 'real' / 'weekly' / 'POWERBALL' / 'sessions').glob('RESUME_0123456789abcdef0123456789abcdef_*.json'))
        self.assertEqual(len(tokens), 1)
        tok = json.loads(tokens[0].read_text())
        self.assertEqual((tok['schema'], tok['game_id'], tok['session_id']), ('RESUME_TOKEN_V1', 'POWERBALL', '0123456789abcdef0123456789abcdef'))
        self.assertEqual(tok['process_table_sha256'], PC.table_digest([]))
        self.assertTrue(lock.exists())
        # a lock that names no session id: refused, no token
        lock.write_text('garbage')
        self.assertEqual(self.check([], '--game', 'POWERBALL'), 1)
        self.assertIn('does not name a session id', self.out[-1])
        lock.write_text('0123456789abcdef0123456789abcdef 2026-11-20T10:00:00Z')
        # clear-session-lock on CLEAN: the lock goes, a clearance record stays
        self.assertEqual(self.run_tool(['clear-session-lock', '--root', str(self.root), '--game', 'POWERBALL'], []), 0)
        self.assertFalse(lock.exists())
        recs = list((self.root / 'transitory_data' / 'lock_clearances').glob('CLEARANCE_SESSION_LOCK_*.json'))
        self.assertEqual(len(recs), 1)
        rec = json.loads(recs[0].read_text())
        self.assertEqual((rec['schema'], rec['kind'], rec['game_id']), ('LOCK_CLEARANCE_V1', 'SESSION_LOCK', 'POWERBALL'))
        self.assertIn('0123456789abcdef0123456789abcdef', rec['lock_content'])
        # a lock that is a folder is refused as not a plain file
        lock.mkdir()
        self.assertEqual(self.run_tool(['clear-session-lock', '--root', str(self.root), '--game', 'POWERBALL'], []), 1)
        self.assertIn('not a plain file', self.out[-1])

    def test_updater_lock_rules(self):
        lock = PC.updater_lock(self.root)
        self.assertEqual(self.run_tool(['clear-updater-lock', '--root', str(self.root)], []), 1)
        self.assertIn('no updater lock', self.out[-1])
        lock.write_text('2026-11-20T10:00:00+00:00')                     # the updater's own content: a timestamp
        # a live updater process: refused; an unrelated project Python that is not the updater does not count here
        updater = proc(20, 1, exe=str(self.venv_py), cwd=str(self.root), cmdline=['python', '-u', 'src/results_master_v0_2.py', 'update'])
        other = proc(21, 1, exe=str(self.venv_py), cwd=str(self.root), cmdline=['python', 'Method_Walk_Forward.py'])
        self.assertEqual(self.run_tool(['clear-updater-lock', '--root', str(self.root)], [updater, other]), 1)
        self.assertIn('1 updater process(es) listed', self.out[-1])
        self.assertTrue(lock.exists())
        self.assertEqual(self.run_tool(['clear-updater-lock', '--root', str(self.root)], [other]), 0)
        self.assertFalse(lock.exists())
        recs = list((self.root / 'transitory_data' / 'lock_clearances').glob('CLEARANCE_UPDATER_LOCK_*.json'))
        self.assertEqual(len(recs), 1)
        self.assertEqual(json.loads(recs[0].read_text())['lock_content'], '2026-11-20T10:00:00+00:00')
        # an install's lock is never cleared by this command
        self.assertEqual(self.run_tool(['take-install-lock', '--root', str(self.root), '--package', 'MHUPA_V1'], []), 0)
        content = lock.read_text()
        self.assertTrue(PC.INSTALL_LOCK.fullmatch(content), content)
        self.assertEqual(self.run_tool(['clear-updater-lock', '--root', str(self.root)], []), 1)
        self.assertIn('names an install', self.out[-1])
        self.assertEqual(lock.read_text(), content)
        # a second install cannot take it; a wrong package cannot release it; the right one can, once
        self.assertEqual(self.run_tool(['take-install-lock', '--root', str(self.root), '--package', 'OTHER'], []), 1)
        self.assertIn('already names an install', self.out[-1])
        self.assertEqual(self.run_tool(['release-install-lock', '--root', str(self.root), '--package', 'OTHER'], []), 1)
        self.assertTrue(lock.exists())
        self.assertEqual(self.run_tool(['release-install-lock', '--root', str(self.root), '--package', 'MHUPA_V1'], []), 0)
        self.assertFalse(lock.exists())
        self.assertEqual(self.run_tool(['release-install-lock', '--root', str(self.root), '--package', 'MHUPA_V1'], []), 1)
        # an update's lock blocks an install from taking it (A7: the owner clears it with clear-updater-lock first)
        lock.write_text('2026-11-20T10:00:00+00:00')
        self.assertEqual(self.run_tool(['take-install-lock', '--root', str(self.root), '--package', 'MHUPA_V1'], []), 1)
        self.assertIn("an update's content", self.out[-1])
        self.assertEqual(self.run_tool(['take-install-lock', '--root', str(self.root), '--package', 'bad name'], []), 1)

    def test_install_check(self):
        manifest = Path(self._td.name) / 'PACKAGE_MANIFEST.json'
        manifest.write_text(json.dumps({'package': 'MHUPA_V1', 'release_entries': []}))
        self.assertEqual(self.check([], '--install', str(manifest)), 0)
        # a session lock refuses the install check
        slock = PC.session_lock(self.root, 'OZLOTTO')
        slock.parent.mkdir(parents=True)
        slock.write_text('x')
        self.assertEqual(self.check([], '--install', str(manifest)), 1)
        self.assertIn('OZLOTTO: a session lock exists', self.out[-1])
        slock.unlink()
        # the updater lock: an update's content refuses; this install's own content passes; another's refuses
        ulock = PC.updater_lock(self.root)
        ulock.write_text('2026-11-20T10:00:00+00:00')
        self.assertEqual(self.check([], '--install', str(manifest)), 1)
        self.assertIn("not an install's", self.out[-1])
        ulock.write_text('INSTALL MHUPA_V1 2026-11-20T10:00:00.000000Z')
        self.assertEqual(self.check([], '--install', str(manifest)), 0)
        ulock.write_text('INSTALL OTHER 2026-11-20T10:00:00.000000Z')
        self.assertEqual(self.check([], '--install', str(manifest)), 1)
        self.assertIn('names another install (OTHER)', self.out[-1])
        ulock.unlink()
        # a roster-changing install waits for an unfinished weekly set (EX_129 C01); Mode H tickets do not count
        weekly = self.root / 'results' / 'real' / 'weekly' / 'POWERBALL'
        (weekly / 'sessions').mkdir(parents=True)
        ticket = {'schema': 'TICKET_V1', 'kind': 'SET_STARTED', 'target_draw_number': 1590}
        (weekly / 'sessions' / ('SESSION_' + 'a' * 32 + '_attempts.jsonl')).write_text(json.dumps(ticket) + '\n')
        hold = self.root / 'results' / 'real' / 'holdout' / 'wf_batches' / 'POWERBALL' / ('wf-' + 'b' * 32)
        hold.mkdir(parents=True)
        (hold / 'attempts.jsonl').write_text(json.dumps({'schema': 'TICKET_V1', 'kind': 'OPEN', 'target_draw_number': 1577}) + '\n')
        self.assertEqual(self.check([], '--install', str(manifest)), 0)            # changes no roster: passes
        changing = Path(self._td.name) / 'PACKAGE_MANIFEST_2.json'
        changing.write_text(json.dumps({'package': 'MHUPA_V1', 'release_entries': [{'game_id': 'POWERBALL'}]}))
        self.assertEqual(self.check([], '--install', str(changing)), 1)
        self.assertIn('unfinished weekly set (targets [1590]', self.out[-1])
        (weekly / 'FORECAST_LEDGER_V1.jsonl').write_text(json.dumps({'schema': 'FREEZE_LINE_V1', 'target_draw_number': 1590}) + '\n')
        self.assertEqual(self.check([], '--install', str(changing)), 0)            # the set is finished
        self.assertEqual(PC.unfinished_weekly_set(self.root, 'OZLOTTO'), set())
        # a live process still refuses the install check
        live = proc(20, 1, exe=str(self.venv_py), cwd=str(self.root), cmdline=['python', 'x.py'])
        self.assertEqual(self.check([live], '--install', str(changing)), 1)
        bad = Path(self._td.name) / 'bad.json'
        bad.write_text(json.dumps({'release_entries': []}))
        self.assertEqual(self.check([], '--install', str(bad)), 1)
        self.assertIn('names no package', self.out[-1])


class Statics(unittest.TestCase):
    """The tool's code with every string constant blanked: identifiers and calls only, no docstring or message."""

    @staticmethod
    def code_only() -> tuple[ast.Module, str]:
        tree = ast.parse(TOOL.read_text(encoding='ascii'))

        class Blank(ast.NodeTransformer):
            def visit_Constant(self, node):
                return ast.copy_location(ast.Constant(value=''), node) if isinstance(node.value, str) else node
        stripped = ast.fix_missing_locations(Blank().visit(ast.parse(TOOL.read_text(encoding='ascii'))))
        return tree, ast.unparse(stripped)

    def test_imports_and_no_terminating_call(self):
        tree, code = self.code_only()
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names |= {a.name.split('.')[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                names.add((node.module or '').split('.')[0])
        self.assertTrue(names <= {'argparse', 'dataclasses', 'datetime', 'hashlib', 'json', 'os', 're', 'sys', 'pathlib',
                                  'psutil', '__future__'}, names)
        for bad in ('methods', 'evaluation', '_common', 'Method_', 'subprocess', 'terminate', 'kill', 'taskkill', 'signal',
                    'SIGTERM', 'suspend', 'resume(', 'wait('):
            self.assertNotIn(bad, code, bad)
        calls = {ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}
        self.assertFalse(any(c.endswith(('.terminate', '.kill', '.send_signal', '.suspend', '.resume', '.wait')) for c in calls), calls)
        psutil_calls = sorted(c for c in calls if c.startswith('psutil.'))
        self.assertEqual(psutil_calls, ['psutil.Process', 'psutil.process_iter'])
        self.assertNotIn(b'\r', TOOL.read_bytes())
        TOOL.read_bytes().decode('ascii')

    def test_writes_only_its_own_records(self):
        tree, code = self.code_only()
        # every write goes through write_record (create-only) or the install lock's create-exclusive open
        opens = [ast.unparse(n) for n in ast.walk(tree) if isinstance(n, ast.Call) and ast.unparse(n.func) in ('open', 'os.open')]
        self.assertEqual(len(opens), 2, opens)
        self.assertTrue(any('O_EXCL' in o for o in opens))
        unlinks = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and ast.unparse(n.func).endswith('.unlink')]
        self.assertEqual(len(unlinks), 3)                                   # the two lock clearances and the install release
        self.assertEqual(PC.HOLDOUT_LAST, {'POWERBALL': 1586, 'OZLOTTO': 1703})
        for bad in ('results_master.csv', 'ledger.csv', 'plan.json', 'forecast.json', 'score_ledger'):
            self.assertNotIn(bad, TOOL.read_text(encoding='ascii'), bad)


if __name__ == '__main__':
    unittest.main()
