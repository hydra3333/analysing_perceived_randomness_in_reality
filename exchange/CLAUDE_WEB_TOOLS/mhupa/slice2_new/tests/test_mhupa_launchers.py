"""MHUP-A (design v0.1r5 sections 4.1, 6.1, 7; EX_129 C02): the launchers and the byte-code-cache rule.

Static: Run_Experiment.bat carries exactly the four changes (a)-(d) of 4.1 against its MHUP-A base (the base is
reconstructed here line by line, so the test states the whole permitted difference); Run_Evaluation.bat is the
mirror of the edited Run_Experiment.bat for src\\evaluation\\; Run_Results_Updater.bat names v0_2; every .bat is
ASCII with CRLF line endings; .gitignore carries the MHUP-A lines.

Behavioural (Linux, in the suite): with PYTHONPYCACHEPREFIX set to an absent folder and -B, a planted
__pycache__ sentinel is not imported and the folder is not created, including the nested case where the variables
are already set by a parent and the venv probe (line 31's command) runs first without -B; without the rule the
same planted sentinel IS imported (the control), which is why the rule exists.
"""
from __future__ import annotations

import os
import py_compile
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRLF = b'\r\n'

ADDED_A = b'set "PYTHONDONTWRITEBYTECODE=1"'
ADDED_B = [b'set "PYTHONPYCACHEPREFIX=%ROOT%transitory_data\\no_pycache_ever"',
           b'if exist "%PYTHONPYCACHEPREFIX%" goto :pycache_present']
RUN_OLD, RUN_NEW = b'"%PY%" -u %*', b'"%PY%" -B -u %*'
ADDED_D = [b':pycache_present',
           b'echo [RUN-EXPERIMENT] ERROR: transitory_data\\no_pycache_ever exists; refusing to run. >&2',
           b'set "RC=10"',
           b'goto :finish']
MIRROR = [(b'rem Human-facing AND provisional coordinator-facing experiment runner (Option F).',
           b'rem Evaluator launcher (MHUP-A design 6.1): the mirror of Run_Experiment.bat for src\\evaluation\\.'),
          (b'[RUN-EXPERIMENT]', b'[RUN-EVALUATION]'),
          (b'if not exist "%ROOT%src\\methods\\%SCRIPT_NAME%" goto :missing_script',
           b'if not exist "%ROOT%src\\evaluation\\%SCRIPT_NAME%" goto :missing_script'),
          (b'pushd "%ROOT%src\\methods"', b'pushd "%ROOT%src\\evaluation"'),
          (b'echo Usage: %~nx0 POC_Architecture_Probe.py --poc --case=echo-argv [options] >&2',
           b'echo Usage: %~nx0 Method_Mode_H.py statements [options] >&2'),
          (b'First argument must be a filename like POC_Architecture_Probe.py',
           b'First argument must be a filename like Method_Mode_H.py'),
          (b'ERROR: Experiment Python file does not exist in src\\methods:',
           b'ERROR: Evaluation Python file does not exist in src\\evaluation:'),
          (b'ERROR: Could not enter src\\methods.', b'ERROR: Could not enter src\\evaluation.'),
          (b'rem Pin numerical library threads before the experiment imports NumPy / SciPy.',
           b'rem Pin numerical library threads before the evaluator imports NumPy / SciPy.')]
GITIGNORE_LINES = ['source_data/backups/', 'source_data/grabs/', 'source_data/.results_master.lock',
                   'src/methods/E_001/IN_DEVELOPMENT.txt', 'src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt',
                   'results/real/holdout/contract_runs/', 'results/real/holdout/wf_batches/**/attempts.jsonl',
                   'results/real/holdout/scores/', 'transitory_data/lock_clearances/', 'transitory_data/no_pycache_ever']
PROBE = ('import sys,pathlib;sys.exit(0 if pathlib.Path(sys.prefix).resolve()==pathlib.Path(sys.argv[1]).resolve() else 12)')


def lines_of(path: Path) -> list[bytes]:
    data = path.read_bytes()
    data.decode('ascii')
    assert data.count(b'\n') == data.count(CRLF) and data.endswith(CRLF), path.name
    return data.split(CRLF)[:-1]


class LauncherStatics(unittest.TestCase):

    def test_run_experiment_carries_exactly_the_four_changes(self):
        new = lines_of(ROOT / 'Run_Experiment.bat')
        self.assertEqual(len(new), 84)
        # reconstruct the base by removing exactly the added lines and reverting (c); the result must be the
        # 77-line launcher of the MHUP-A base in every other respect
        self.assertEqual(new[29], b':verify_python')
        self.assertEqual(new[30], ADDED_A)                                   # (a) right after :verify_python
        self.assertIn(b'sys.prefix', new[31])                                # the probe runs after (a)
        self.assertEqual(new[32], b'if errorlevel 1 goto :prefix_failed')
        self.assertEqual(new[33:35], ADDED_B)                                # (b) right after the prefix check
        self.assertEqual(new[43], RUN_NEW)                                   # (c)
        self.assertEqual(new[71], b':prefix_failed')
        self.assertEqual(new[74], b'goto :finish')
        self.assertEqual(new[75:79], ADDED_D)                                # (d) after the :prefix_failed block
        self.assertEqual(new[79], b':pushd_failed')
        base = new[:30] + new[31:33] + new[35:43] + [RUN_OLD] + new[44:75] + new[79:]
        self.assertEqual(len(base), 77)
        for token in (b'PYTHONDONTWRITEBYTECODE', b'PYCACHEPREFIX', b'pycache', b'-B'):
            self.assertFalse(any(token in l for l in base), token)
        self.assertEqual(base[40], RUN_OLD)
        self.assertEqual(base[0], b'@echo off')
        self.assertEqual(base[-1], b'endlocal & exit /b %RC%')
        # exit code 10 is new and unique
        codes = [l for l in new if l.startswith(b'set "RC=')]
        for n in range(2, 11):
            self.assertEqual(codes.count(b'set "RC=%d"' % n), 1, n)
        # the -B run and the refusal both sit inside SETLOCAL, so nothing leaks to the caller
        self.assertEqual(new[1], b'setlocal DisableDelayedExpansion')

    def test_run_evaluation_is_the_mirror(self):
        exp = (ROOT / 'Run_Experiment.bat').read_bytes()
        mirrored = exp
        for old, new in MIRROR:
            self.assertIn(old, mirrored, old)
            mirrored = mirrored.replace(old, new)
        self.assertEqual(mirrored, (ROOT / 'Run_Evaluation.bat').read_bytes())
        ev = lines_of(ROOT / 'Run_Evaluation.bat')
        self.assertEqual(len(ev), 84)
        self.assertFalse(any(b'methods' in l or b'EXPERIMENT' in l for l in ev))
        self.assertIn(ADDED_A, ev)
        self.assertEqual(ev[43], RUN_NEW)

    def test_results_updater_launcher_names_v0_2_only(self):
        up = lines_of(ROOT / 'Run_Results_Updater.bat')
        self.assertEqual(up[12], b'set "TOOL=%ROOT%src\\results_master_v0_2.py"')
        self.assertEqual(up[46], b'echo [RUN-RESULTS-UPDATER] ERROR: src\\results_master_v0_2.py not found. >&2')
        self.assertFalse(any(b'v0_1' in l for l in up))
        self.assertEqual(len(up), 66)

    def test_every_root_bat_is_ascii_crlf(self):
        names = sorted(p.name for p in ROOT.glob('*.bat'))
        self.assertIn('Run_Evaluation.bat', names)
        for name in names:
            lines_of(ROOT / name)

    def test_gitignore_lines(self):
        text = (ROOT / '.gitignore').read_text(encoding='ascii')
        self.assertNotIn('\r', text)
        present = {l.strip() for l in text.splitlines()}
        for line in GITIGNORE_LINES:
            self.assertIn(line, present, line)


def plant(tmp: Path) -> tuple[Path, Path]:
    """A package folder with mod.py (prints REAL) and a live __pycache__ entry compiled from a sentinel (prints
    SENTINEL) whose header matches mod.py's size and mtime, so a cache-trusting import picks the sentinel."""
    pkg = tmp / 'pkg'
    pkg.mkdir()
    real = "print('REAL')\n#" + 'x' * 10 + '\n'
    sentinel = "print('SENTINEL')\n" + '#' * (len(real) - len("print('SENTINEL')\n") - 1) + '\n'
    assert len(real) == len(sentinel)
    src = pkg / 'mod.py'
    src.write_text(sentinel)
    cache = pkg / '__pycache__' / f'mod.cpython-{sys.version_info.major}{sys.version_info.minor}.pyc'
    py_compile.compile(str(src), cfile=str(cache), doraise=True)
    st = src.stat()
    src.write_text(real)
    os.utime(src, ns=(st.st_atime_ns, st.st_mtime_ns))
    return pkg, cache


def run(args, cwd, env):
    r = subprocess.run([sys.executable, *args], cwd=cwd, env=env, capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


class ByteCodeCacheRule(unittest.TestCase):

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.tmp = Path(self.td.name)
        self.pkg, self.cache = plant(self.tmp)
        self.prefix = self.tmp / 'transitory_data' / 'no_pycache_ever'
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
        self.env['PYTHONHASHSEED'] = '0'

    def tearDown(self):
        self.td.cleanup()

    def test_control_the_planted_sentinel_is_live_without_the_rule(self):
        rc, out, err = run(['-c', 'import mod'], self.pkg, self.env)
        self.assertEqual((rc, out), (0, 'SENTINEL'), err)

    def test_prefix_and_dash_b_bypass_the_sentinel_and_create_nothing(self):
        rc, out, err = run(['-B', '-X', f'pycache_prefix={self.prefix}', '-c', 'import mod'], self.pkg, self.env)
        self.assertEqual((rc, out), (0, 'REAL'), err)
        self.assertFalse(self.prefix.exists())
        self.assertFalse((self.tmp / 'transitory_data').exists())
        # the same through the environment variable, as the launcher sets it
        env = dict(self.env, PYTHONPYCACHEPREFIX=str(self.prefix))
        rc, out, err = run(['-B', '-c', 'import mod'], self.pkg, env)
        self.assertEqual((rc, out), (0, 'REAL'), err)
        self.assertFalse(self.prefix.exists())
        # the planted entry is untouched and still live: it was never consulted, not rewritten
        rc, out, _ = run(['-c', 'import mod'], self.pkg, self.env)
        self.assertEqual(out, 'SENTINEL')

    def test_nested_case_probe_without_dash_b_writes_nothing(self):
        # a parent launcher already set both variables; the child launcher's probe (line 31) runs WITHOUT -B, then
        # the run itself with -B: the folder is never created
        env = dict(self.env, PYTHONPYCACHEPREFIX=str(self.prefix), PYTHONDONTWRITEBYTECODE='1')
        rc, out, err = run(['-c', PROBE, sys.prefix], self.pkg, env)
        self.assertEqual(rc, 0, err)
        rc, out, err = run(['-c', 'import mod'], self.pkg, env)                # even without -B, the variable holds
        self.assertEqual((rc, out), (0, 'REAL'), err)
        self.assertFalse(self.prefix.exists())
        rc, out, err = run(['-B', '-u', '-c', 'import mod'], self.pkg, env)
        self.assertEqual((rc, out), (0, 'REAL'), err)
        self.assertFalse(self.prefix.exists())
        self.assertFalse((self.tmp / 'transitory_data').exists())

    def test_without_dontwritebytecode_the_prefix_folder_would_be_created(self):
        # the reason for (a): with only the prefix set, an import without -B writes the cache under the prefix
        env = dict(self.env, PYTHONPYCACHEPREFIX=str(self.prefix))
        rc, out, err = run(['-c', 'import mod'], self.pkg, env)
        self.assertEqual((rc, out), (0, 'REAL'), err)
        self.assertTrue(self.prefix.exists())

    def test_dash_i_ignores_the_variables_so_the_process_tool_needs_the_options(self):
        # 4.1: -I makes Python ignore both variables, so a -I program is given -B -X pycache_prefix directly
        env = dict(self.env, PYTHONPYCACHEPREFIX=str(self.prefix), PYTHONDONTWRITEBYTECODE='1')
        rc, out, err = run(['-I', '-c', 'import sys; print(sys.pycache_prefix, sys.dont_write_bytecode)'], self.pkg, env)
        self.assertEqual((rc, out), (0, 'None False'), err)
        rc, out, err = run(['-I', '-B', '-X', f'pycache_prefix={self.prefix}', '-c',
                            'import sys; print(sys.pycache_prefix, sys.dont_write_bytecode)'], self.pkg, env)
        self.assertEqual((rc, out), (0, f'{self.prefix} True'), err)
        self.assertFalse(self.prefix.exists())


if __name__ == '__main__':
    unittest.main()
