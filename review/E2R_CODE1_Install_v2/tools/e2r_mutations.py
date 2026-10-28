"""E2R-1 section 13 mutation checks for CODE-1 (Claude-side evidence; disposable copies only).

Usage: python3 -I e2r_mutations.py TREE
For each of E2R-T01, T03, T04, T06, T10 and T16, and the EX_034 fixes B01 and C01, plants a defect in a temporary copy of src/ and tests/
and requires the named test to FAIL; the unchanged copy (control) must pass. The tree itself is never
changed and no bytecode is written to it.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
C = 'src/methods/_common/'
T = 'tests.test_e2r_contract.'
P = 'tests.test_e2r_prefix'
MUTANTS = [
    ('T01', 'validator trusts ranked_groups instead of recomputing them from the scores',
     C + 'contract_forecast.py', "            if groups != score_groups(scores, barrel.low):", "            if False:", T + 'T01ShapeAndNumericContracts'),
    ('T01', 'negative zero accepted', C + 'contract_records.py',
     "        if value == 0.0 and math.copysign(1.0, value) < 0:", "        if False:", T + 'T01ShapeAndNumericContracts'),
    ('T01', 'probability sum not checked', C + 'contract_records.py',
     "    if abs(math.fsum(vec) - V.PROBABILITY_SUM[kind]) > tolerance:", "    if False:", T + 'T01ShapeAndNumericContracts'),
    ('T03', 'the master SHA reaches the method task', C + 'contract_task.py',
     "               'target_draw_number', 'observation_view', 'include_dates', 'run_mode', 'product_kind')",
     "               'target_draw_number', 'observation_view', 'include_dates', 'run_mode', 'product_kind', 'master_sha256')", None),
    ('T04', 'ties ordered by label instead of TIE_SHA256_V1', C + 'contract_records.py',
     "            ranking.extend(sorted(g, key=lambda lab: (tie_digest(tie_identity, lab), lab)))",
     "            ranking.extend(sorted(g))", T + 'T04TieAndWorst'),
    ('T04', 'WORST taken as the last k instead of the reversal', C + 'contract_forecast.py',
     "                        'labels': list(reversed(ranking))[:k]}", "                        'labels': ranking[-k:]}", T + 'T04TieAndWorst'),
    ('T06', 'REAL_HOLDOUT made producible (unreserved AND mapped onto the development row)', C + 'contract_vocab.py',
     ["RESERVED_MODES = frozenset(('REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC'))",
      "        if run_mode == 'REAL_DEVELOPMENT':\n            return 'WF_FORECAST', 'DEVELOPMENT_WF_EXPLORATORY'"],
     ["RESERVED_MODES = frozenset(('FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC'))",
      "        if run_mode in ('REAL_DEVELOPMENT', 'REAL_HOLDOUT'):\n            return 'WF_FORECAST', 'DEVELOPMENT_WF_EXPLORATORY'"],
     T + 'T06ModeFirewall'),
    ('T06', 'benchmarks may produce a forecast', C + 'contract_vocab.py',
     "    if run_mode in BENCHMARK_MODES:\n        raise ValueError('benchmarks produce no method output record (E2R-R41A)')",
     "    if run_mode in BENCHMARK_MODES:\n        return 'BENCHMARK_TIMING', 'NOT_EVIDENCE'", T + 'T06ModeFirewall'),
    ('T10', 'the run ID reaches the forecast warnings', C + 'contract_forecast.py',
     "    warnings = list(output.warnings)", "    warnings = list(output.warnings) + ['mg-synthetic-contract-0001']", P),
    ('T16', 'consumption ignores the group and firewall gates', C + 'contract_receipts.py',
     "    if gates_pass is not True:", "    if False:", T + 'T16ReceiptsAndTerminalRecords'),
    ('T16', 'consumption accepts an interrupted run with no terminal record', C + 'contract_receipts.py',
     "    if terminal is None:\n        return False, 'NO_TERMINAL_RECORD'",
     "    if terminal is None:\n        return True, 'NO_TERMINAL_RECORD'", T + 'T16ReceiptsAndTerminalRecords'),
    ('T16', 'consumption accepts a non-SUCCESS terminal record (both guards removed)', C + 'contract_receipts.py',
     "    if terminal['outcome'] != 'SUCCESS':\n        return False, f'TERMINAL_{terminal[\"outcome\"]}'",
     "    if terminal['outcome'] != 'SUCCESS':\n        return True, 'CONSUMABLE'", T + 'T16ReceiptsAndTerminalRecords'),
    ('B01', 'registry accessors hand every caller the same shared object', C + 'contract_registry.py',
     "def _thaw(digest: str, raw: bytes) -> dict:", "@__import__('functools').lru_cache(maxsize=None)\ndef _thaw(digest: str, raw: bytes) -> dict:",
     T + 'RegistryImmutability'),
    ('B01', 'registry attributes can be replaced', C + 'contract_registry.py',
     "        raise AttributeError('InstalledRegistry is read-only')\n\n    def __delattr__",
     "        object.__setattr__(self, name, value)\n\n    def __delattr__", T + 'RegistryImmutability'),
    ('B01', 'registry chain store is an ordinary mutable dict', C + 'contract_registry.py',
     "        object.__setattr__(self, '_chains', MappingProxyType(chains))",
     "        object.__setattr__(self, '_chains', chains)", T + 'RegistryImmutability'),
    ('C01', 'the old ends-with-Z timestamp check', C + 'contract_receipts.py',
     ["    if type(v) is not str or _UTC_TIMESTAMP.fullmatch(v) is None:",
      "        datetime.strptime(v[:19], '%Y-%m-%dT%H:%M:%S')   # rejects impossible dates and times"],
     ["    if type(v) is not str or not v.endswith('Z'):", "        datetime.fromisoformat(v[:-1])"],
     T + 'ReceiptTimestamps'),
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
