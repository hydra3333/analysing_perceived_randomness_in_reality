"""Mutation checks for the CODE-3 and E_1 revision 2 package (Claude-side evidence; disposable copies only;
Claude, 31 October 2026; design v0.1r2 section 6).

Usage: python3 -I e1r2_mutations.py TREE      (TREE: a tree with the package applied)
For each planted defect, a temporary copy of src/, tests/, archive/ and .gitignore is changed and the named test must
FAIL; the unchanged copy (control) must pass. The tree itself is never changed and no bytecode is written to it.
A mutant's `old` of None with a `new` of None deletes the file; an `old` of None with text creates the file.
The install-time mutants (the barrier flag left out or removed early; the verifier's `code` phase accepting an
entry) concern the package's verifier, not the repository, and are checked by the end-to-end rehearsal instead.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
MG = 'src/methods/E_001/multigame_e1.py'
LEG = 'src/methods/E_001_Historical_Appearance_Frequency.py'
AR = 'archive/methods/E_001/r1/'
CD = 'src/methods/_common/contract_data/'
MR = 'src/package_tools/method_retirement.py'
T3 = 'tests.test_code3_retirement.'
T2 = 'tests.test_e1r2_revision2.'

MUTANTS = [
    ("r2's data-kind line admitting REAL_HOLDOUT", MG, "('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT')",
     "('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT', 'REAL_HOLDOUT')", T2 + 'DataKinds'),
    ('the legacy gate left at revision 1', LEG, "'FULL_HISTORY_RAW_COUNTS_V1', '2')", "'FULL_HISTORY_RAW_COUNTS_V1', '1')",
     T2 + 'LegacyRunner'),
    ('an archived file with one byte changed', AR + 'E_001/e1_training_view.py', 'import csv\n', 'import csv \n',
     T3 + 'InstalledArchive.test_archive_holds_revision_1_complete'),
    ('a README without its helper list', AR + 'README.md', '## Shared helpers used', '## Helpers',
     T3 + 'InstalledArchive.test_archive_holds_revision_1_complete'),
    ('the archive missing one file', AR + 'E_001/__init__.py', None, None,
     T3 + 'InstalledArchive.test_archive_holds_revision_1_complete'),
    ('an import from archive in src/', 'src/methods/_common/zz_mutant_probe.py', None,
     'import archive.methods.E_001  # noqa\n', T3 + 'ArchiveIsNeverExecuted.test_static'),
    ('a test loading an archived file with importlib', 'tests/test_zz_mutant_probe.py', None,
     'import importlib\n\ndef load():\n    return importlib.import_module("archive.methods.E_001.r1")\n',
     T3 + 'ArchiveIsNeverExecuted.test_static'),
    ('the static check blind to import_module', MR, "frozenset({'import_module', ", "frozenset({",
     T3 + 'ArchiveIsNeverExecuted.test_static_check_catches_loading'),
    ('the static check blind to Path(...) / parts (EX_093 B01)', MR,
     "    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):\n        return _parts(node.left) + _parts(node.right)\n",
     "    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):\n        return [UNKNOWN]\n",
     T3 + 'ArchiveIsNeverExecuted.test_static_check_catches_constructed_paths'),
    ("the static check not folding Path('archive', 'methods') (EX_093 B01)", MR,
     "        if name in PATH_CALLS or ast.unparse(fn).endswith('path.join') or name == 'join':",
     "        if ast.unparse(fn).endswith('path.join') or name == 'join':",
     T3 + 'ArchiveIsNeverExecuted.test_static_check_catches_constructed_paths'),
    ('the path-construction rule removed (EX_095 O02)', MR,
     "        if _is_path_construction(n) and _spells_archive(_parts(n), strict=True):\n",
     "        if False:\n", T3 + 'ArchiveIsNeverExecuted.test_static_check_catches_constructed_paths'),
    ('retire writing before checking every input (EX_093 O01)', MR,
     "            raise ValueError(f'not a regular file: {src}')\n    if len(set(files)) != len(files):\n        raise ValueError('a file is listed twice')\n",
     "            pass\n",
     T3 + 'RetirementT15.test_retire_checks_every_input_before_writing'),
    ('retirement not removing a dropped path', MR, "    for f in drop:\n        (repo / 'src' / 'methods' / f).unlink()\n",
     "    for f in drop:\n        pass\n", T3 + 'RetirementT15.test_without_git_history'),
    ('the archive check ignoring changed bytes', MR, '        if exp is None or got != exp:', '        if exp is None:',
     T3 + 'RetirementT15.test_without_git_history'),
    ('E_1 left in NOT_REAL_CAPABLE', 'src/methods/_common/walk_forward.py', 'NOT_REAL_CAPABLE: dict[str, str] = {}',
     "NOT_REAL_CAPABLE: dict[str, str] = {'E_1': 'left in'}", T2 + 'Driver'),
    ("r2's declaration differing in another field", CD + 'declarations/OZLOTTO/E_1/FULL_HISTORY_RAW_COUNTS_V1/r2.json',
     '"minimum_history_draws":1', '"minimum_history_draws":2', T2 + 'Registry'),
    ("E_1's counting changed", MG, '                counts[value] += 1\n',
     '                counts[value] += 2 if value == 1 else 1\n', T2 + 'IdentityWithRevision1.test_r2_equals_r1_label_for_label'),
    ("E_1's Oz Lotto tie order changed", MG,
     'ranking = sorted(counts, key=lambda n:(-counts[n], _digest(digest,target,desc.barrel_id,n),n))',
     "ranking = sorted(counts, key=lambda n:(-counts[n], (str(n) if profile.game_id == 'OZLOTTO' else "
     '_digest(digest,target,desc.barrel_id,n)),n))', T2 + 'RealNamespaceOzLotto'),
    ('the r1 reference file edited by one value', 'tests/fixtures/e1_r1_reference_v1.json',
     '"training_last_draw_number":1145', '"training_last_draw_number":1144',
     T2 + 'IdentityWithRevision1.test_r2_equals_r1_label_for_label'),
    ("the gate's flag check moved before the pin check", 'src/methods/_common/contract_dispatch.py',
     "    if entry['registry_status'] != 'SUPPORTED':\n",
     "    if (methods_root / method_folder(method) / FLAG_NAME).exists():\n"
     "        refuse('IN_DEVELOPMENT_FLAG_PRESENT', 'moved')\n"
     "    if entry['registry_status'] != 'SUPPORTED':\n", T2 + 'InstallBarrier'),
]


def run(root, test):
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(root / p) for p in ('src', 'src/methods', 'tests'))
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q', test], cwd=root, env=env,
                          capture_output=True, text=True).returncode


def copy(tmp, name):
    d = tmp / name
    for part in ('src', 'tests', 'archive'):
        shutil.copytree(tree / part, d / part, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy(tree / '.gitignore', d / '.gitignore')
    return d


fails = 0
with tempfile.TemporaryDirectory(prefix='e1r2_mut_') as t:
    tmp = Path(t)
    c = copy(tmp, 'control')
    for test in sorted({m[4] for m in MUTANTS}):
        ok = run(c, test) == 0
        print(('PASS' if ok else 'FAIL'), 'control passes', test)
        fails += not ok
    for i, (what, rel, old, new, test) in enumerate(MUTANTS):
        d = copy(tmp, f'm{i}')
        p = d / rel
        if old is None and new is None:
            p.unlink()
        elif old is None:
            assert not p.exists(), rel
            p.write_text(new, encoding='utf-8')
        else:
            s = p.read_text(encoding='utf-8')
            assert s.count(old) == 1, (what, old[:40])
            p.write_text(s.replace(old, new), encoding='utf-8')
        failed = run(d, test) != 0
        print(('PASS' if failed else 'FAIL'), f'mutation: {what} -> {test} fails')
        fails += not failed
print('RESULT e1r2:', 'PASS' if not fails else f'FAIL ({fails})', f'({len(MUTANTS)} mutants)')
sys.exit(1 if fails else 0)
