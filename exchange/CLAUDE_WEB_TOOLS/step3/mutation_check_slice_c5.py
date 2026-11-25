"""Workspace helper (not project code): the planted faults for slice C part C5 (deploy/reinstall_infra.py, and the
reports command of the checks program). One fault at a time in a disposable copy of the dev tree that holds the
overlay; the named test module must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
R, T = 'deploy/reinstall_infra.py', 'src/research/tree_checks.py'
MODULES = {R: ['test_trees_reinstall'], T: ['test_trees_verify.TheReportsCommand']}
FAULTS = [
 (R, "    return {entry['path']: entry['sha256'] for entry in current['files'] if not VARIANTS_PATH.match(entry['path'])}", "    return {entry['path']: entry['sha256'] for entry in current['files']}", 'the variants\' files are taken for infrastructure'),
 (R, "    files.update(dev_files)\r\n", "", 'expected: DEV\'s infrastructure is not what the tree must hold'),
 (R, "    if belonging:\r\n", "    if False:\r\n", 'a path under a family folder is carried out'),
 (R, "    if forecasting:\r\n", "    if False:\r\n", 'a forecast-class file is changed'),
 (R, "    forecasting = [path for path in paths if classes[path] == FORECAST]", "    forecasting = [path for path in paths if classes[path] == FORECAST and path in in_dev]", 'a forecast-class file is removed'),
 (R, "    if reclassed:\r\n", "    if False:\r\n", 'a file is moved into the forecast class'),
 (R, "        for line in difflib.unified_diff(old, new, 'installed', 'DEV', lineterm='', n=1):\r\n            say(f'      {line}')", "        pass", 'the differences are not shown'),
 (R, "        say(f'  overwrite: {entry[\"path\"]} (class {classes[entry[\"path\"]]}; now {entry[\"was\"]}; to be '", "        say(f'  overwrite: {entry[\"path\"]} (now {entry[\"was\"]}; to be '", 'the class is not shown'),
 (R, "        source_root = dev_root if entry['path'] in dev_files else tree_root", "        source_root = tree_root", 'step 3 asks the installed software, not the software as it would be'),
 (R, "    new = {game: answer for game, answer in sorted(found['derived'].items()) if answer and not answer['known']}", "    new = {}", 'statement: a change is reported as no change'),
 (R, "    new = {game: answer for game, answer in sorted(found['derived'].items()) if answer and not answer['known']}", "    new = {game: answer for game, answer in sorted(found['derived'].items()) if answer}", 'statement: a difference the tree already marks is a change of this reinstall'),
 (R, "    for game in old:\r\n        text +=", "    for game in ():\r\n        text +=", 'statement: an already marked game is not mentioned'),
 (R, "    if passed is not True:\r\n        raise common.InstallRefused('the suite does not pass with the target\\'s Python on the software as it would '", "    if False:\r\n        raise common.InstallRefused('the suite does not pass with the target\\'s Python on the software as it would '", 'step 3: a failing suite does not stop'),
 (R, "        found = common.checks_with_target_python(python, folder, root, common.NO_VARIANT, True, True, say)", "        found = common.checks_with_target_python(python, root, root, common.NO_VARIANT, True, True, say)", 'step 3: the tree itself is asked'),
 (R, "    if found['sample']['differences']:", "    if False:", 'step 3: a sample difference does not stop'),
 (R, "    finally:\r\n        shutil.rmtree(folder, ignore_errors=True)", "    finally:\r\n        pass", 'step 3: the temporary folder is left behind'),
 (R, "            derived_check.write_cutoff(tree_root, game_id, draw, derived_check.MISMATCH, statement['detail'][game_id])", "            pass", 'step 9: the cutoff is not written'),
 (R, "        if not (marked is not None and marked[1] == derived_check.MISMATCH and marked[0] <= draw):", "        if True:", 'step 9: an earlier mark is replaced by a later draw'),
 (R, "        moved = reports.set_aside_from(tree_root, game_id, draw)", "        moved = 0", 'step 9: the stale reports are not moved out'),
 (R, "    faults = mark_not_current(root, plan['statement'], say)", "    faults = []", 'step 9: an accepted change is not marked'),
 (R, "    faults = common.software_differences(root, expected) + common.status_file_faults(root)", "    faults = []", 'step 8: the software is not checked against the plan'),
 (R, "    if passed is not True:\r\n        say('STOPPED: the suite does not pass in place", "    if False:\r\n        say('STOPPED: the suite does not pass in place", 'step 9: a failing suite in place does not stop'),
 (R, "    found = common.checks_with_target_python(python, root, root, common.ALL_VARIANTS, True, True, say)", "    found = common.checks_with_target_python(python, root, root, common.ALL_VARIANTS, True, False, say)", 'step 9: the derived results are not compared again'),
 (R, "    if stopping:\r\n        say(f'STOPPED: {len(stopping)} finding(s) in place.", "    if False:\r\n        say(f'STOPPED: {len(stopping)} finding(s) in place.", 'step 9: a finding in place does not stop'),
 (R, "    if any(classes.get(path) == DERIVED for path in changed):", "    if False:", 'the print-outs are not made again'),
 (R, "    if any(classes.get(path) == DERIVED for path in changed):", "    if True:", 'the print-outs are made again although no report code changed'),
 (R, "    fingerprint = common.finish(root, plan, expected, now, release=release, extra={'suite': 'PASSED'})", "    fingerprint = common.finish(root, plan, expected, now, release=None, extra={'suite': 'PASSED'})", 'the updater\'s lock is not released before the barrier goes'),
 (R, "        if unfinished is None and nothing_differs:", "        if False:", 'no difference does not end the command'),
 (R, "                if drift:\r\n", "                if False:\r\n", 'software changed outside the tools is not refused'),
 (R, "            with common.reserved(settings, f'Reinstall_Infra {role}: what it would change', started, say):\r\n                statement", "            if True:\r\n                statement", 'step 3 is made without the lock'),
 (R, "            kit, backup = common.attempt_rollback_point(dev_root, settings, 'PRE_INFRA', expected, now, say)", "            kit, backup = common.attempt_rollback_point(dev_root, settings, 'PRE_INSTALL', expected, now, say)", 'the backup before is not named PRE_INFRA'),
 (R, "            lines = [WARNING.format(role=role, root=root)] + common.question_lines(kit, backup)", "            lines = common.question_lines(kit, backup)", 'the warning is not given'),
 (R, "            if not common.owner_says_yes(lines, ask, say):", "            if False:", 'the reinstall goes on without the question'),
 (R, "        with common.reserved(settings, f'Reinstall_Infra {role}', started, say):\r\n            if not continuing:", "        if True:\r\n            if not continuing:", 'the target is not reserved before the overwriting'),
 (R, "                common.carry_out(dev_root, root, plan, say)\r\n", "", 'nothing is overwritten'),
 (R, "                if not (chosen.replace_unfinished and unfinished.get('operation') == common.REINSTALL_INFRA):", "                if not (unfinished.get('operation') == common.REINSTALL_INFRA):", 'another plan is replaced without the flag'),
 (R, "                                        *changes_between({path: _sha256(root / path) for path in paths}, dev['files']),", "                                        *changes_between(infrastructure_on_list(current), dev['files']),", 'replace: the plan is not worked out from the files as they lie'),
 (R, "        say(snapshot.attempt_snapshot(settings, 'POST_INFRA', now).line())", "        say('no backup')", 'no backup is attempted after'),
 (R, "            say(f'YOU NOW OWE {game_id} A RERUN: Rerun_Walk_Forward.bat --game {game_id} --from {draw} '", "            say(f'A rerun may be needed for {game_id} from {draw} '", 'the rerun owed is not named'),
 (R, "        if exit_code != EXIT_REINSTALLED:\r\n", "        if False:\r\n", 'a stopped reinstall is said to be finished'),
 (R, "            dict(unfinished, statement=None) == by_the_list\r\n", "            False\r\n", 'the same command again cannot continue'),
 (T, "        finish_reports(job, records, ReportWriter(records.tree_root, game_id, job.local_time()))", "        pass", 'reports: nothing is made again'),
 (T, "        if Path(software_root).resolve() != settings.tree_root.resolve():\r\n            raise ChecksRefused('a tree\\'s reports", "        if False:\r\n            raise ChecksRefused('a tree\\'s reports", 'reports: made by software outside the tree'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
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
