"""Mutation checks for REL-1 and WF-1A (Claude-side evidence; disposable copies only; Claude, 31 October 2026).

Usage: python3 -I wf1_mutations.py rel1 TREE      (TREE: a tree with REL-1 applied)
       python3 -I wf1_mutations.py wf1a TREE      (TREE: a tree with REL-1 and WF-1A applied)
For each planted defect, a temporary copy of src/, tests/ and .gitignore is changed and the named test must FAIL;
the unchanged copy (control) must pass. The tree itself is never changed and no bytecode is written to it.
A mutant's `old` of None with a `new` of None deletes the file; an `old` of None with text creates the file.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

which, tree = sys.argv[1], Path(sys.argv[2]).resolve()
REG = 'src/methods/_common/contract_data/registry/'
WF = 'src/methods/_common/walk_forward.py'
TR = 'tests.test_rel1_release.'
TW = 'tests.test_wf1a_walk_forward.'
E6F = REG + 'POWERBALL/E_6/BETA_BERNOULLI_FULL_MEMORY_V1/entry_0002.json'

REL1 = [
    ('a released variant without its entry_0002', E6F, None, None, TR + 'InstalledChains'),
    ('a development flag left in place', 'src/methods/E_006/IN_DEVELOPMENT.txt', None, 'left behind\n',
     TR + 'InstalledChains.test_no_development_flag_remains'),
    ('an entry_0002 with another reason', REG + 'OZLOTTO/E_19/PERIODIC_T4_V1/entry_0002.json',
     'Released by package REL-1', 'Released by package REL-0', TR + 'InstalledChains'),
    ('an entry_0002 with another date', REG + 'POWERBALL/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0002.json',
     '"effective_date":"2026-10-31"', '"effective_date":"2026-10-30"', TR + 'InstalledChains'),
]
WF1A = [
    ('the switch left off', 'src/methods/_common/contract_runner.py', 'ENABLE_CONTRACT_REAL_DEVELOPMENT = True',
     'ENABLE_CONTRACT_REAL_DEVELOPMENT = False', TW + 'StaticAndInstalled'),
    ('the real run root back in transitory_data', 'src/methods/Method_Contract_Runner.py',
     "run_root = CR.PROJECT_ROOT / 'results' / 'real' / 'development' / 'contract_runs'",
     "run_root = CR.PROJECT_ROOT / 'transitory_data' / 'contract_runs'", TW + 'StaticAndInstalled'),
    ('the gitignore line missing', '.gitignore', '\nresults/real/development/contract_runs/\n', '\n',
     TW + 'StaticAndInstalled'),
    ('DATA_ADMISSION_REFUSED classified CONTINUE', WF, "                      ('VALIDATION_FAILURE', CP.NO_TICKET_NO_DIAGNOSTIC)})",
     "                      ('VALIDATION_FAILURE', CP.NO_TICKET_NO_DIAGNOSTIC),\n"
     "                      ('VALIDATION_FAILURE', 'DATA_ADMISSION_REFUSED')})",
     TW + 'ResumeAndStop.test_changed_master_stops_with_zero_later_runs'),
    ('an unknown reason classified CONTINUE', WF,
     "    if isinstance(reason, str) and ':' in reason and (outcome, reason_prefix(reason)) in CONTINUE:",
     "    if isinstance(reason, str) and ':' in reason:", TW + 'Classification'),
    ('a runner refusal does not stop the batch', WF, "            return f'{ident}: REFUSED: {exc.text}'",
     "            continue", TW + 'ResumeAndStop.test_marker_between_targets_stops'),
    ('an escaping exception does not stop the batch', WF,
     "            return f'{ident}: {type(exc).__name__} escaped the runner: {exc}'", "            continue",
     TW + 'ResumeAndStop.test_escaping_exception_and_unknown_reason_stop'),
    ('a holdout target admitted at plan', WF, '    if last >= p.holdout_first:', '    if last > p.holdout_first:',
     TW + 'PlanRefusals'),
    ("the era's first draw admitted at plan", WF, '    if first < p.first_draw + 1:', '    if first < p.first_draw:',
     TW + 'PlanRefusals'),
    ('resume re-runs finished pairs', WF,
     "            if states[(mem['method_id'], mem['variant_id'], t)] != 'DONE']",
     "            if True]", TW + 'TheBatch.test_runs_in_order_and_every_run_is_consumable'),
    ('attempt lines of another batch accepted (B01)', WF, "a['batch_id'] == plan['batch_id'] and", "True and",
     TW + 'AttemptBinding.test_another_batch_with_the_same_pins_is_not_reused'),
    ("an attempt line's request digest not checked (B01)", WF,
     "                  a['request_digest'] == record_digest(request_for(plan, mem, a['target_draw_number'], a['run_id'])))",
     "                  True)", TW + 'AttemptBinding.test_an_attempt_without_a_folder_and_junk_lines'),
    ("the receipt's master pin not checked (B01)", WF,
     "    for k in ('master_sha256', 'run_mode', 'product_kind', 'registry_entry_digest', 'run_id'):",
     "    for k in ('run_mode', 'product_kind', 'registry_entry_digest', 'run_id'):",
     TW + 'AttemptBinding.test_corrupt_or_mismatched_records_make_the_pair_run_again'),
    ('a SUCCESS counted without the consumable check (B01)', WF, "    if not ok:\n        return 'NOT_DONE', f'forecast not consumable: {why}'",
     "    if False:\n        return 'NOT_DONE', f'forecast not consumable: {why}'",
     TW + 'AttemptBinding.test_corrupt_or_mismatched_records_make_the_pair_run_again'),
    ('a forged terminal counted without its records (B01)', WF,
     "    if forecast is None or receipt is None:\n        return 'NOT_DONE', 'SUCCESS without a valid forecast and receipt'",
     "    if forecast is None or receipt is None:\n        return 'DONE', 'forged'",
     TW + 'AttemptBinding.test_forged_terminal_without_an_attempt_is_not_done'),
    ('the attempt not bound before the run (B01)', WF, "        _append_attempt(plan, req)                          # bound to this batch before the run (EX_083 B01)\n",
     "", TW + 'TheBatch.test_runs_in_order_and_every_run_is_consumable'),
    ('an altered plan accepted', WF, '    if record_digest(plan) not in _logged_plan_digests(batch_id):',
     '    if False:', TW + 'TheBatch.test_plan_is_frozen_and_checked'),
    ('the start checks skip the flag', WF, "        if _flag(mem['method_id']).exists():\n            raise BatchRefused(f'{ident}: an IN_DEVELOPMENT flag is present')",
     "        if False:\n            raise BatchRefused(f'{ident}: an IN_DEVELOPMENT flag is present')",
     TW + 'ResumeAndStop.test_start_checks_refuse_a_changed_registry_or_a_new_flag'),
    ('the registry read from its import-time default', WF, '    return InstalledRegistry(Path(REG.DATA_ROOT))',
     '    return InstalledRegistry()', TW + 'ResumeAndStop.test_start_checks_refuse_a_changed_registry_or_a_new_flag'),
    ('E_1 revision 1 put in the cohort', WF, "NOT_REAL_CAPABLE = {'E_1': (", "NOT_REAL_CAPABLE = {'E_X': (",
     TW + 'TheBatch.test_runs_in_order_and_every_run_is_consumable'),
    ('no WF_BATCH search-log row', WF, "    _append_search_row({'row_type': 'WF_BATCH',", "    (lambda r: None)({'row_type': 'WF_BATCH',",
     TW + 'TheBatch.test_runs_in_order_and_every_run_is_consumable'),
    ('a flagged SUPPORTED member silently skipped at plan', WF,
     "    if inconsistent:\n        raise BatchRefused(", "    if False:\n        raise BatchRefused(",
     TW + 'PlanRefusals.test_supported_but_flagged_is_refused_by_name'),
]
MUTANTS = {'rel1': REL1, 'wf1a': WF1A}[which]


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
    shutil.copy(tree / '.gitignore', d / '.gitignore')
    return d


fails = 0
with tempfile.TemporaryDirectory(prefix='wf1_mut_') as t:
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
print(f'RESULT {which}:', 'PASS' if not fails else f'FAIL ({fails})', f'({len(MUTANTS)} mutants)')
sys.exit(1 if fails else 0)
