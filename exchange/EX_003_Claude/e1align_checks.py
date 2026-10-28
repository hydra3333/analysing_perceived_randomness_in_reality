"""E1-ALIGN design evidence: moved-code equality and mutation checks.
Usage: python3 -I e1align_checks.py NAMES1_TREE E1ALIGN_TREE WORK_DIR
NAMES1_TREE: 38fc60e with the NAMES-1 renames; E1ALIGN_TREE: the same after apply_e1align.py plus
tests/test_e1_align.py. Both are read-only here; mutations run in copies under WORK_DIR."""
import difflib, os, re, shutil, subprocess, sys
from pathlib import Path

a, b, work = (Path(x).resolve() for x in sys.argv[1:4])
fails = 0
def check(ok, what):
    global fails
    print(('PASS ' if ok else 'FAIL ') + what); fails += not ok

E1 = ['e1_historical_appearance_frequency', 'e1_training_view', 'e1_standalone_contract',
      'e1_common_reader_bridge', 'multigame_e1']
moved = {f'src/methods/_common/{n}.py': f'src/methods/E_001/{n}.py' for n in E1}
added = {'src/methods/_common/canonical_encoding.py', 'src/methods/E_001/__init__.py', 'tests/test_e1_align.py'}
IMPORT = re.compile(r'\s*(from\s+\S+\s+import\b|import\s+\S+)')

def files(t):
    return {p.relative_to(t).as_posix() for p in t.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
fa, fb = files(a), files(b)
inv = {v: k for k, v in moved.items()}
check(fb - fa == set(moved.values()) | added and fa - fb == set(moved), 'file set: exactly 5 moves and 3 additions')
changed = sorted(p for p in fb & fa if (a / p).read_bytes() != (b / p).read_bytes())
changed += sorted(v for k, v in moved.items() if (a / k).read_bytes() != (b / v).read_bytes())
expect = {'src/methods/E_001/e1_historical_appearance_frequency.py', 'src/methods/E_001/e1_training_view.py',
          'src/methods/E_001/multigame_e1.py', 'src/methods/E_001/e1_common_reader_bridge.py',
          'src/methods/E_001_Historical_Appearance_Frequency.py', 'src/methods/_common/game_draws_reader.py',
          'tests/test_e1_standalone.py', 'tests/test_multigame_console_and_synthetic_scorer.py',
          'tests/test_multigame_reader_contracts.py', 'tests/test_multigame_static_and_timing.py'}
check(set(changed) == expect, f'changed files exactly as expected ({len(changed)}); e1_standalone_contract moved unchanged')

core_old = (a / 'src/methods/_common/e1_historical_appearance_frequency.py').read_text('utf-8')
shared = (b / 'src/methods/_common/canonical_encoding.py').read_text('utf-8')
cb = core_old[core_old.index('def canonical_bytes('):core_old.index('def _integer(')].rstrip('\n')
lt = core_old[core_old.index('def _length32_tuple('):core_old.index('def tie_digest(')].rstrip('\n')
check(cb in shared and lt.replace('def _length32_tuple(', 'def length32_tuple(', 1) in shared,
      'shared module holds both functions byte-for-byte (tuple helper renamed only in its def line)')
moved_block = set(cb.splitlines()) | set(lt.splitlines()) | {''}
for new in changed:
    old = inv.get(new, new)
    ol = (a / old).read_text('utf-8').splitlines(); nl = (b / new).read_text('utf-8').splitlines()
    rem = [l for l in difflib.ndiff(ol, nl) if l[:2] in ('- ', '+ ')]
    if new.endswith('test_multigame_static_and_timing.py'):
        body = [l for l in rem if not IMPORT.match(l[2:])]
        check(all('firewall' in l or l[2:].startswith(' ' * 8) or l[2:].strip() == '' or
                  l[2:].startswith('    def test_method_loader_import_firewall') for l in body),
              f'{new}: only the firewall test body changes ({len(rem)} lines)')
        continue
    def allowed(l):
        if IMPORT.match(l[2:]) or l[2:].strip() == '':
            return True  # import lines, and blank lines around them
        if l[:2] == '- ' and l[2:] in moved_block:
            return True  # lines of the two definitions moved to the shared module
        return new == 'tests/test_e1_standalone.py' and ("patch('_common.e1_training_view." in l or
                                                         "patch('E_001.e1_training_view." in l)
    bad = [l for l in rem if not allowed(l)]
    check(not bad, f'{new}: {len(rem)} changed lines, all import / moved-definition / patch-target lines {bad[:2]}')

env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
def run(tree, test):
    e = dict(env, PYTHONPATH=os.pathsep.join(str(tree / p) for p in ('src', 'src/methods', 'tests')))
    return subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q', test], cwd=tree, env=e,
                          capture_output=True, text=True).returncode
FW = 'test_multigame_static_and_timing.StaticSafetyTests.test_method_loader_import_firewall_except_accepted_legacy_e1'
GUARD = 'test_e1_align'
def mutant(name, edits=(), new_files=()):
    d = work / name
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(b, d, ignore=shutil.ignore_patterns('__pycache__'))
    for rel, old, new in edits:
        p = d / rel; s = p.read_text('utf-8'); assert s.count(old) == 1, (rel, old); p.write_text(s.replace(old, new), 'utf-8')
    for rel, text in new_files:
        (d / rel).parent.mkdir(parents=True, exist_ok=True); (d / rel).write_text(text, 'utf-8')
    return d
check(run(mutant('c0'), FW) == 0 and run(mutant('c0g'), GUARD) == 0, 'control: firewall and guard tests pass')
check(run(mutant('m1', new_files=[('src/methods/E_001/e1_probe.py', 'from _common.game_draws_reader import DrawView\n')]), FW) != 0,
      'mutation: new E_001 file importing the reader is rejected (allowance is per file, not per folder)')
check(run(mutant('m2', new_files=[('src/methods/E_002/probe.py', 'import _common.game_draws_reader as r\n')]), FW) != 0,
      'mutation: another method folder importing the reader is rejected')
check(run(mutant('m3', new_files=[('src/methods/E_002/probe.py', "P = 'source_data'\n")]), FW) != 0,
      'mutation: another method folder naming source_data is rejected')
check(run(mutant('m4', edits=[('src/methods/E_001/e1_training_view.py', 'from __future__ import annotations\n',
                               "from __future__ import annotations\n# source_data\n")]), FW) != 0,
      'mutation: a second source_data reference in an allowed E_1 file is rejected (counted)')
check(run(mutant('m5', edits=[('src/methods/E_001/e1_common_reader_bridge.py', 'from _common.game_draws_reader import DrawView',
                               'DrawView = object')]), FW) != 0,
      'mutation: an unused allowance is rejected (every allowance must be used)')
check(run(mutant('m6', edits=[('src/methods/_common/game_draws_reader.py', 'from _common.canonical_encoding import canonical_bytes',
                               'from E_001.e1_historical_appearance_frequency import canonical_bytes')]), GUARD) != 0,
      'mutation: the shared reader importing E_1 code again is rejected')
check(run(mutant('m7', edits=[('src/methods/_common/canonical_encoding.py', "separators=(',', ':')", "separators=(', ', ':')")]), GUARD) != 0,
      'mutation: a changed shared encoder is caught by the three-encoder alarm')
check(run(mutant('m8', edits=[('src/methods/E_001/e1_standalone_contract.py', '.parents[3] /', '.parents[2] /')]), GUARD) != 0,
      'mutation: a moved orphan-marker path is caught (no marker is created)')
print('RESULT', 'PASS' if not fails else f'FAIL ({fails})'); sys.exit(1 if fails else 0)
