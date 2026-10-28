"""E1-ALIGN design evidence (v0.2): exact-allowlist equality and mutation checks.
Usage: python3 -I e1align_checks.py NAMES1_TREE E1ALIGN_TREE ALLOWLIST_JSON WORK_DIR
NAMES1_TREE: 38fc60e with the NAMES-1 renames; E1ALIGN_TREE: the same after apply_e1align.py plus
tests/test_e1_align.py. Both are read-only here; mutations run in copies under WORK_DIR.
The exact check (E1A-T01/T02) rebuilds every new file from its predecessor using ONLY the frozen
allowlist's (old block -> new block) edits, each of which must occur exactly once, and requires byte
equality. Added files must match their listed SHA-256; everything else must be byte-identical."""
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

a, b, allow_path, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4]).resolve()
allow = json.load(open(allow_path))
fails = 0
def check(ok, what):
    global fails
    print(('PASS ' if ok else 'FAIL ') + what); fails += not ok

def files(t):
    return {p.relative_to(t).as_posix() for p in t.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def exact_check(base, tree, report=True):
    """Return a list of problems; empty means the tree is exactly base + allowlist."""
    problems = []
    moves = allow['moves']; inv = {v: k for k, v in moves.items()}
    fa, fb = files(base), files(tree)
    want_b = (fa - set(moves)) | set(moves.values()) | set(allow['added'])
    if fb != want_b:
        problems.append(f'file set differs: extra {sorted(fb - want_b)} missing {sorted(want_b - fb)}')
    for p, h in allow['added'].items():
        if p in fb and hashlib.sha256((tree / p).read_bytes()).hexdigest() != h:
            problems.append(f'added file bytes differ: {p}')
    edited = {e['new_path']: e for e in allow['edited']}
    for new in sorted(fb & want_b):
        if new in allow['added']:
            continue
        old = inv.get(new, new)
        ob = (base / old).read_bytes()
        if new in edited:
            text = ob.decode('utf-8')
            for ed in edited[new]['edits']:
                if text.count(ed['old']) != 1:
                    problems.append(f'{new}: an allowlisted old block does not occur exactly once'); break
                text = text.replace(ed['old'], ed['new'])
            ob = text.encode('utf-8')
        if (tree / new).read_bytes() != ob:
            problems.append(f'{new}: differs from predecessor + allowlist')
    return problems

probs = exact_check(a, b)
check(not probs, f'E1A-T01/T02 exact: {len(allow["edited"])} edited files, '
      f'{sum(len(e["edits"]) for e in allow["edited"])} allowlisted blocks, {len(allow["moves"])} moves, '
      f'{len(allow["added"])} added files; nothing else differs {probs[:2]}')

core_old = (a / 'src/methods/_common/e1_historical_appearance_frequency.py').read_text('utf-8')
shared = (b / 'src/methods/_common/canonical_encoding.py').read_text('utf-8')
cb = core_old[core_old.index('def canonical_bytes('):core_old.index('def _integer(')].rstrip('\n')
lt = core_old[core_old.index('def _length32_tuple('):core_old.index('def tie_digest(')].rstrip('\n')
check(cb in shared and lt.replace('def _length32_tuple(', 'def length32_tuple(', 1) in shared,
      'E1A-T02 moved bodies: both definitions byte-for-byte in canonical_encoding.py (tuple helper def name only)')
check((a / 'src/methods/_common/e1_standalone_contract.py').read_bytes() ==
      (b / 'src/methods/E_001/e1_standalone_contract.py').read_bytes(), 'e1_standalone_contract moved byte-identical')

def mutant(name, edits=(), new_files=()):
    d = work / name
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(b, d, ignore=shutil.ignore_patterns('__pycache__'))
    for rel, old, new in edits:
        p = d / rel; s = p.read_text('utf-8'); assert s.count(old) == 1, (rel, old); p.write_text(s.replace(old, new), 'utf-8')
    for rel, text in new_files:
        (d / rel).parent.mkdir(parents=True, exist_ok=True); (d / rel).write_text(text, 'utf-8')
    return d

# The exact checker itself rejects unlisted edits (C01).
check(bool(exact_check(a, mutant('x1', edits=[('src/methods/_common/game_draws_reader.py',
      'from _common.canonical_encoding import canonical_bytes', 'from _common.canonical_encoding import canonical_bytes  # x')]))),
      'checker negative: an extra edit on an allowlisted import line is rejected')
check(bool(exact_check(a, mutant('x2', edits=[('src/methods/E_001/e1_training_view.py',
      'from E_001.e1_historical_appearance_frequency import canonical_bytes',
      'from E_001.e1_historical_appearance_frequency import canonical_bytes, rank_counts')]))),
      'checker negative: a different import that still "looks like an import" is rejected')
check(bool(exact_check(a, mutant('x3', new_files=[('src/methods/E_001/extra.py', 'X = 1\n')]))),
      'checker negative: an unlisted new file is rejected')

env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
def run(tree, test):
    e = dict(env, PYTHONPATH=os.pathsep.join(str(tree / p) for p in ('src', 'src/methods', 'tests')))
    return subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q', test], cwd=tree, env=e,
                          capture_output=True, text=True).returncode
FW = 'test_multigame_static_and_timing.StaticSafetyTests.test_method_loader_import_firewall_except_accepted_legacy_e1'
GUARD = 'test_e1_align'
SHARED = 'test_e1_align.E1AlignGuards.test_shared_code_imports_no_method_code'
BR = 'src/methods/E_001/e1_common_reader_bridge.py'
BRL = 'from _common.game_draws_reader import DrawView'
check(run(mutant('c0'), FW) == 0 and run(mutant('c0g'), GUARD) == 0 and run(mutant('c0s'), SHARED) == 0, 'control: firewall, guard and shared-import tests pass')
M = [
 ('m1', 'new E_001 file importing the reader', [], [('src/methods/E_001/e1_probe.py', BRL + '\n')], FW),
 ('m2', 'E_002 file: import _common.game_draws_reader', [], [('src/methods/E_002/probe.py', 'import _common.game_draws_reader as r\n')], FW),
 ('m3', 'E_002 file naming source_data', [], [('src/methods/E_002/probe.py', "P = 'source_data'\n")], FW),
 ('m4', 'second source_data in an allowed E_1 file', [('src/methods/E_001/e1_training_view.py', 'from __future__ import annotations\n', 'from __future__ import annotations\n# source_data\n')], [], FW),
 ('m5', 'unused allowance (bridge import removed)', [(BR, BRL, 'DrawView = object')], [], FW),
 ('m6', 'shared reader importing E_1 code again', [('src/methods/_common/game_draws_reader.py', 'from _common.canonical_encoding import canonical_bytes', 'from E_001.e1_historical_appearance_frequency import canonical_bytes')], [], GUARD),
 ('m7', 'changed shared encoder', [('src/methods/_common/canonical_encoding.py', "separators=(',', ':')", "separators=(', ', ':')")], [], GUARD),
 ('m8', 'moved orphan-marker path (no marker created)', [('src/methods/E_001/e1_standalone_contract.py', '.parents[3] /', '.parents[2] /')], [], GUARD),
 # v0.2, reviewer's E1A-B01:
 ('m9', 'E_002 file: from _common import game_draws_reader', [], [('src/methods/E_002/probe.py', 'from _common import game_draws_reader\n')], FW),
 ('m10', 'bridge imports load_pinned_draw_view instead of DrawView', [(BR, BRL, 'from _common.game_draws_reader import load_pinned_draw_view as DrawView')], [], FW),
 ('m11', 'bridge adds an extra reader symbol', [(BR, BRL, 'from _common.game_draws_reader import DrawView, load_pinned_draw_view')], [], FW),
 ('m12', 'bridge aliases DrawView', [(BR, BRL, 'from _common.game_draws_reader import DrawView as DV\nDrawView = DV')], [], FW),
 ('m13', 'bridge star import', [(BR, BRL, 'from _common.game_draws_reader import *')], [], FW),
 ('m14', 'E_002 file: dynamic import by string', [], [('src/methods/E_002/probe.py', "import importlib\nr = importlib.import_module('_common.game_draws_reader')\n")], FW),
 ('m15', 'E_001 file: from _common import game_draws_reader', [], [('src/methods/E_001/e1_probe.py', 'from _common import game_draws_reader\n')], FW),
 # v0.2r1, reviewer's E1A2-C01 (shared code importing method code by imported name):
 ('m16', 'shared module: from methods import E_001', [('src/methods/_common/game_profiles.py', 'from __future__ import annotations\n', 'from __future__ import annotations\nfrom methods import E_001\n')], [], SHARED),
 ('m17', 'shared module: from _common import e1_training_view', [('src/methods/_common/game_profiles.py', 'from __future__ import annotations\n', 'from __future__ import annotations\nfrom _common import e1_training_view\n')], [], SHARED),
 ('m18', 'coordinator_private module: from methods.E_001 import x (module path)', [('src/coordinator_private/multigame_launch_spec.py', 'from __future__ import annotations\n', 'from __future__ import annotations\nfrom methods.E_001 import e1_training_view\n')], [], SHARED),
]
for name, what, edits, new_files, test in M:
    check(run(mutant(name, edits, new_files), test) != 0, f'mutation {name}: {what} is rejected')
print('RESULT', 'PASS' if not fails else f'FAIL ({fails})'); sys.exit(1 if fails else 0)
