"""E2R-1 section 13 mutation checks for CODE-2: E2R-T14 and T16 (Claude-side evidence; disposable copies only).

Usage: python3 -I e2r_mutations.py TREE
For E2R-T14 (the dispatch gate), E2R-T16 at run level, the EX_039 corrections B01, B02 and C01..C03, and the EX_041 code fixes CODE-B01 and CODE-B02, plants a defect in a temporary copy of src/ and tests/
and requires the named test to FAIL; the unchanged copy (control) must pass. The tree itself is never
changed and no bytecode is written to it.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
C = 'src/methods/_common/'
T = 'tests.test_e2r_contract.'
D = 'tests.test_e2r_dispatch.'
R = 'tests.test_e2r_runner.'
P = None
MUTANTS = [
    ('T14', 'the gate ignores the IN_DEVELOPMENT flag', C + 'contract_dispatch.py',
     "    if flag.exists() or flag.is_symlink():\n        refuse('IN_DEVELOPMENT_FLAG_PRESENT'",
     "    if False:\n        refuse('IN_DEVELOPMENT_FLAG_PRESENT'", D + 'T14TruthTable'),
    ('T14', 'the gate admits a FORMULA_OPEN entry', C + 'contract_dispatch.py',
     "    if entry['registry_status'] != 'SUPPORTED':", "    if entry['registry_status'] == 'UNSUPPORTED_FOR_GAME':",
     D + 'T14TruthTable'),
    ('T14', 'the gate accepts a stale pinned entry', C + 'contract_dispatch.py',
     "    if pinned_entry is not None and pinned_entry != record_digest(entry):", "    if False:", D + 'T14ReleaseTransition'),
    ('T14', 'the gate ignores a declaration mismatch', C + 'contract_dispatch.py',
     "    if pinned_declaration is not None and entry['declaration_digest'] != pinned_declaration:", "    if False:",
     D + 'T14TruthTable'),
    ('T14', 'the runner reads data before the gate', C + 'contract_runner.py',
     "    entry, declaration = dispatch_gate(request)                   # reads no data",
     "    load_pinned_draw_view(repo_root=Path(repo_root), run_manifest=reader_pin(request))\n"
     "    entry, declaration = dispatch_gate(request)                   # reads no data",
     D + 'T14TruthTable'),
    ('T14', 'the coordinator side skips the shared gate', 'src/coordinator_private/contract_coordinated_gate.py',
     "    dispatch_gate(request)\n", "", D + 'T14TruthTable'),
    ('T14', 'the gate trusts a cached registry', C + 'contract_dispatch.py',
     "        registry = InstalledRegistry(data_root)      # fresh every call, never a cached or caller copy",
     "        cache = globals().setdefault('_CACHE', {})\n        registry = cache[str(data_root)] if str(data_root) in cache "
     "else cache.setdefault(str(data_root), InstalledRegistry(data_root))", D + 'T14TruthTable'),
    ('T16', 'a failed run still names its receipts', C + 'contract_publication.py',
     "             'receipt_digests': sorted(self.receipts) if outcome == 'SUCCESS' else []}",
     "             'receipt_digests': sorted(self.receipts)}", R + 'T16RunLevel'),
    ('T16', 'a failure after a receipt is recorded as SUCCESS', C + 'contract_runner.py',
     "        return end('RUNTIME_FAILURE', reason)", "        return end('SUCCESS', reason)", R + 'T16RunLevel'),
    ('C01', 'publication renames over an existing file instead of linking', C + 'contract_publication.py',
     "            os.link(tmp, path)", "            os.replace(tmp, path)", R + 'AtomicCreateOnly'),
    ('T16', 'a run folder can be reused', C + 'contract_publication.py',
     "        self.folder.mkdir(exist_ok=False)", "        self.folder.mkdir(exist_ok=True)", R + 'T16RunLevel'),
    ('B02', 'consumption ignores an active orphan marker', C + 'contract_publication.py',
     "    if marker.exists() or marker.is_symlink():\n        return False, 'UNRESOLVED_ORPHAN_MARKER'",
     "    if False:\n        return False, 'UNRESOLVED_ORPHAN_MARKER'", R + 'ConsumptionGates'),
    ('B02', 'consumption accepts a coordinated run without its evidence', C + 'contract_publication.py',
     "    if terminal.get('execution_path') != 'STANDALONE' or receipt.get('execution_path') != 'STANDALONE':",
     "    if False:", R + 'ConsumptionGates'),
    ('B02', 'consumption trusts any admitting entry', C + 'contract_publication.py',
     "    if (entry is None or entry['registry_status'] != 'SUPPORTED' or",
     "    if False and (entry is None or entry['registry_status'] != 'SUPPORTED' or", R + 'ConsumptionGates'),
    ('B01', 'the legacy E_1 runner skips the release gate', 'src/methods/E_001_Historical_Appearance_Frequency.py',
     "        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '1')",
     "        pass", D + 'LegacyRunnerGate'),
    ('C02', 'a missing declared diagnostic counts as a valid empty target', C + 'contract_runner.py',
     "                if task.product_kind == forecast_product and declaration['diagnostic_schema_id'] is None:",
     "                if task.product_kind == forecast_product:", R + 'NoTicketAndProducts'),
    ('CODE-B01', 'consumption accepts a caller-chosen orphan marker', C + 'contract_publication.py',
     ["def read_run(folder: Path) -> dict:", "    marker = Path(CRun.ORPHAN_MARKER)"],
     ["def read_run(folder: Path, orphan_marker=None) -> dict:",
      "    marker = Path(CRun.ORPHAN_MARKER if orphan_marker is None else orphan_marker)"], R + 'NoCallerChosenAuthority'),
    ('CODE-B01', 'the gate accepts a caller-chosen registry root', C + 'contract_dispatch.py',
     "def dispatch_gate(request: object) -> tuple[dict, dict]:",
     "def dispatch_gate(request: object, data_root=None) -> tuple[dict, dict]:", R + 'NoCallerChosenAuthority'),
    ('CODE-B02', 'the runner publishes a coordinated run', C + 'contract_publication.py',
     "        self.execution_path = 'STANDALONE'", "        self.execution_path = 'COORDINATED'", R + 'NoCallerChosenAuthority'),
    ('CODE-B01', 'a synthetic run may read the project itself', C + 'contract_runner.py',
     "            check_synthetic_workspace(repo_root)", "            pass", R + 'NoCallerChosenAuthority'),
    ('C03', "Package 2's synthetic prototype trusts the per-method roll-up", C + 'multigame_standalone_contract.py',
     "    if not variant_released(profile.game_id, method_id, variant_id):", "    if False:",
     D + 'RosterIsNotAdmission'),
]


def run(root, test):
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(root / p) for p in ('src', 'src/methods', 'tests'))
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q', test], cwd=root, env=env,
                          capture_output=True, text=True).returncode


def copy(tmp, name):
    d = tmp / name
    for part in ('src', 'tests'):
        shutil.copytree(tree / part, d / part, ignore=shutil.ignore_patterns('__pycache__'))
    return d


fails = 0
with tempfile.TemporaryDirectory(prefix='e2r_mut_') as t:
    tmp = Path(t)
    c = copy(tmp, 'control')
    for test in sorted({m[5] or P for m in MUTANTS}):
        ok = run(c, test) == 0
        print(('PASS' if ok else 'FAIL'), 'control passes', test)
        fails += not ok
    for i, (tid, what, rel, old, new, test) in enumerate(MUTANTS):
        d = copy(tmp, f'm{i}')
        p = d / rel
        s = p.read_text(encoding='utf-8')
        for o, n in zip(*((old, new) if isinstance(old, list) else ([old], [new]))):
            assert s.count(o) == 1, (tid, what, o[:40])
            s = s.replace(o, n)
        p.write_text(s, encoding='utf-8')
        failed = run(d, test or P) != 0
        print(('PASS' if failed else 'FAIL'), f'{tid} mutation: {what} -> {test or P} fails')
        fails += not failed
print('RESULT', 'PASS' if not fails else f'FAIL ({fails})')
sys.exit(1 if fails else 0)
