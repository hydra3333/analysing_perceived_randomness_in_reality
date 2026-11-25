"""Workspace helper (not project code): the planted faults for the corrections EX_329 asked for in slice C. One fault
at a time is planted in a disposable copy of the dev tree that holds the overlay; the named test module must fail. A
fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
R, I, N, T, V = ('deploy/reinstall_infra.py', 'deploy/init_tree.py', 'deploy/install.py', 'src/research/tree_checks.py',
                 'src/research/tree_verify.py')
MODULES = {R: ['test_trees_reinstall'], I: ['test_trees_init'], N: ['test_trees_install'],
           T: ['test_trees_checks', 'test_trees_verify'], V: ['test_trees_verify']}
FAULTS = [
 (R, "            elif what_the_statement_rests_on(settings, common.dev_infrastructure(dev_root)['fingerprint']) != rested_on:", "            elif False:", 'C-B01: the answer is acted on although what it rested on changed'),
 (R, "WATCHED_FOLDERS = ('src', 'source_data', 'results/research')", "WATCHED_FOLDERS = ('source_data', 'results/research')", 'C-B01: a change of the software or of a status file is not seen'),
 (R, "WATCHED_FOLDERS = ('src', 'source_data', 'results/research')", "WATCHED_FOLDERS = ('src', 'source_data')", 'C-B01: a change of the stored research is not seen'),
 (R, "WATCHED_FOLDERS = ('src', 'source_data', 'results/research')", "WATCHED_FOLDERS = ('src', 'results/research')", 'C-B01: a change of the accepted results is not seen'),
 (R, "    paths = [root / code_identity.MANIFEST_PATH, root / installed_files.LIST_PATH, root / common.BARRIER_PATH,\r\n", "    paths = [root / code_identity.MANIFEST_PATH, root / installed_files.LIST_PATH,\r\n", 'C-B01: a barrier that appeared or changed is not seen'),
 (R, "             settings.venv_dir / MARKER_NAME]", "             ]", 'C-B01: a change of the verified environment is not seen'),
 (R, "    digest = hashlib.sha256(f'DEV\\t{dev_fingerprint}\\n'.encode('ascii'))", "    digest = hashlib.sha256(b'DEV')", 'C-B01: a change of DEV is not seen'),
 (R, "NOT_WATCHED = ('__pycache__', 'reports')", "NOT_WATCHED = ('__pycache__',)", 'C-B01: a print-out moves what the statement rests on'),
 (R, "                if common.read_barrier(root) != plan:", "                if False:", 'C-B01: a continued reinstall whose record changed is carried on'),
 (R, "                      and unfinished.get('infrastructure_fingerprint') == dev['fingerprint'])", "                      and unfinished.get('infrastructure_fingerprint') == dev['fingerprint'] and not unfinished['remove'])", 'C-B03: a plan that removes a file cannot be continued'),
 (R, "                      and unfinished.get('infrastructure_fingerprint') == dev['fingerprint'])", "                      )", 'C-B03: a reinstall accepted from another DEV is continued'),
 (R, "            classes = {**(replaced or {}).get('classes', {}), **in_tree, **dev['classes'],", "            classes = {**in_tree, **dev['classes'],", 'C-B03: the class of a file an unfinished plan was removing is forgotten'),
 (R, "                    entry['path'] for word in ('add', 'overwrite', 'remove') for entry in replaced[word]}", "                    entry['path'] for word in () for entry in replaced[word]}", 'C-B03: a replacement forgets what the unfinished plan had added'),
 (R, "                                          or (replaced or {}).get('reports_owed', replaced is not None)))", "                                          ))", 'C-B04: a replacement forgets the print-outs owed'),
 (R, "    if plan.get('reports_owed', True):", "    if False:", 'C-B04: the print-outs owed are not made again'),
 (I, "    moved = [relative for relative in files if _sha256(Path(source_root) / relative) != first[relative]]", "    moved = []", 'C-B02: no second reading of the source'),
 (I, "    check_copied_pairs(target_root)\r\n    record = {", "    record = {", 'C-B02: the copied pairs are not read before the record'),
 (I, "                                   replace=True)", "                                   replace=False)", 'C-B02: a retry cannot replace its own unrecorded results'),
 (I, "            source = begun['statement']                  # a creation being continued: the source it was begun with", "            source = dict(zip(('results_copied_from', 'results_copied_from_role'), map(str, results_source(view, role))))", 'C-B02: a continued creation chooses its source anew'),
 (I, "        if not (root / INIT_RECORD_PATH).exists():           # with its record, a creation reads no source again", "        if True:", 'C-B02: a recorded creation still reads its former source'),
 (I, "    if source_role != 'PROD':\r\n        return\r\n", "    return\r\n", 'C-B02: a busy PROD is read'),
 (N, "            if common.check_barrier(root, plan) != continuing or (not continuing and (\r\n                    installed_files.read_list(root) != current or installed_files.differences(root, current))):", "            if common.check_barrier(root, plan) != continuing:", 'C-B01: an install acts on a base that changed'),
 (N, "    dev_files = common.dev_infrastructure_bytes(dev_root)", "    dev_files = common.dev_infrastructure(dev_root)['files'] if install_readiness_ready(dev_root) else None", 'C-C02: the suite depends on DEV\'s readiness marker'),
 (T, "            records = read_game(job, game_id)\r\n            check_results_only_grew(records)\r\n            stored[game_id] = records", "            records = read_game(job, game_id)\r\n            stored[game_id] = records", 'C-C01: the checks compare a game whose results the job refuses'),
 (T, "            records = read_game(job, game_id)\r\n            check_results_only_grew(records)\r\n        except GAME_REFUSALS as refusal:", "            records = read_game(job, game_id)\r\n        except GAME_REFUSALS as refusal:", 'C-C01: reports are made again for a game whose results the job refuses'),
 (T, "    (folder / SMOKE_TABLE_NAME).write_bytes(results.raw.replace(b'\\n', LINE_ENDING.encode('ascii')))", "    (folder / SMOKE_TABLE_NAME).write_bytes(results.raw)", 'C-C04: the kept table is not CRLF'),
 (V, "    check_no_unfinished_operation(settings.tree_root)\r\n    check_no_orphan_marker(settings.tree_root)\r\n    looked_at", "    check_no_orphan_marker(settings.tree_root)\r\n    looked_at", 'C-C03: an operation begun meanwhile is not seen under the lock'),
 (V, "    check_no_unfinished_operation(settings.tree_root)\r\n    check_no_orphan_marker(settings.tree_root)\r\n    looked_at", "    check_no_unfinished_operation(settings.tree_root)\r\n    looked_at", 'C-C03: an orphan marker written meanwhile is not seen under the lock'),
 (V, "        return EXIT_NOT_VERIFIED, smoke_failures + [SUITE_LINE] + [", "        return EXIT_NOT_VERIFIED, smoke_failures + [", 'C-C04: the suite line is missing from the failed verdict'),
]
PRELUDE = {N: ("import install_common as common\r\n", "import install_common as common\r\nimport install_readiness\r\ninstall_readiness_ready = lambda root: install_readiness.infrastructure_readiness(root).ready\r\n")}
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    data = kept.replace(old.encode(), new.encode())
    if relative in PRELUDE and 'readiness marker' in what:
        data = data.replace(PRELUDE[relative][0].encode(), PRELUDE[relative][1].encode(), 1)
    path.write_bytes(data)
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', *MODULES[relative]], cwd=MUT, timeout=600,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught, how = run.returncode != 0, 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what, flush=True)
print(f'{len(FAULTS)} faults planted; {survived} survived')
