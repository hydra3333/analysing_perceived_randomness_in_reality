"""Workspace helper (not project code): the planted faults for slice C part C3 (deploy/init_tree.py, and the marker
written by the checks command at a tree's creation). One fault at a time in a disposable copy of the dev tree that
holds the overlay; the named test modules must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
I, T, C = 'deploy/init_tree.py', 'src/research/tree_checks.py', 'deploy/install_common.py'
MODULES = {I: ['test_trees_init'], T: ['test_trees_verify'], C: ['test_trees_install_common', 'test_trees_init']}
FAULTS = [
 (I, "    if copy_from is not None:\r\n        lines += ['[results]'", "    if False:\r\n        lines += ['[results]'", 'settings: a QA tree is never told where its jobs copy results from'),
 (I, "        copy_from = view.entries['PROD'].tree_root if role == 'QA' and 'PROD' in view.entries else None", "        copy_from = view.entries['PROD'].tree_root if 'PROD' in view.entries else None", 'settings: a PROD tree gets a results section'),
 (I, "    if not settings_file.is_file():\r\n        raise common.InstallRefused(f'{root} is not empty", "    if False:\r\n        raise common.InstallRefused(f'{root} is not empty", 'state: a folder that holds something else is taken'),
 (I, "    if settings_file.read_bytes() != wanted_settings:", "    if False:", 'state: another tree\'s settings file is accepted'),
 (I, "    if (root / installed_files.LIST_PATH).exists():", "    if False:", 'state: a created tree is created again'),
 (I, "            common.check_barrier(root, plan)\r\n        except", "            pass\r\n        except", 'state: a barrier with another plan is continued'),
 (I, "                f'DEV as it is now. To abandon it, delete the folder {root} yourself", "                f'DEV as it is now. Delete it; {root}", 'state: the way to abandon a creation is not said'),
 (I, "    if role == 'PROD' or 'PROD' not in view.entries:\r\n        return dev_root, 'DEV'", "    if True:\r\n        return dev_root, 'DEV'", 'results: QA never takes its results from PROD'),
 (I, "    if not (prod_root / SETTINGS_FILE_NAME).is_file():\r\n        return dev_root, 'DEV'", "    if not (prod_root / SETTINGS_FILE_NAME).is_file():\r\n        return prod_root, 'PROD'", 'results: a PROD that does not exist is the source'),
 (I, "        if (prod_root / held).exists():", "        if False:", 'results: a PROD with an unfinished install or a running update is read'),
 (I, "            if is_link(source) or not source.is_file():", "            if False:", 'results: a missing file of the accepted results is not noticed'),
 (I, "RESULTS_FILE_NAMES = (MASTER_NAME, LEDGER_NAME, '{game_id}_results_master_init_verification.json')", "RESULTS_FILE_NAMES = (MASTER_NAME, LEDGER_NAME)", 'results: the verification records are not copied'),
 (I, "        if changed:\r\n            raise common.InstallRefused(f'the results copied when", "        if False:\r\n            raise common.InstallRefused(f'the results copied when", 'results: a copied file changed since is accepted'),
 (I, "            f'({len(record[\"results\"])} files, as the record says).')\r\n        return\r\n", "            f'({len(record[\"results\"])} files, as the record says).')\r\n", 'results: a continued creation copies them again'),
 (I, "        if state == NEW or not (root / INIT_RECORD_PATH).exists():\r\n            results_files(source_root)", "        if False:\r\n            results_files(source_root)", 'results: the source is not checked before the question'),
 (I, "            if not common.owner_says_yes([f'Type {common.YES} to create the {role} tree", "            if False and not common.owner_says_yes([f'Type {common.YES} to create the {role} tree", 'question: the tree is created without being asked'),
 (I, "        process_rule.check_no_other_process_of_tree(root)\r\n        settings = TreeSettings(", "        settings = TreeSettings(", 'no process check before the folder is created'),
 (I, "                with open(settings_file, 'xb') as handle:", "                with open(settings_file, 'wb') as handle:", 'the settings file is not opened create-only'),
 (I, "            if not settings_file.exists():\r\n                with open", "            if True:\r\n                with open", 'the settings file is written again by a continued creation'),
 (I, "                common.carry_out(dev_root, root, plan, say)\r\n", "", 'no file is copied'),
 (I, "                created = common.create_status_files(root, plan)", "                created = 0", 'no status file is created'),
 (I, "                copy_results(source_root, source_role, plan, now, say)\r\n", "", 'no results are copied'),
 (I, "                if not (entry.venv_dir / common.PROGRAMS_FOLDER / 'python.exe').is_file():", "                if False:", 'no pause for the environment'),
 (I, "    faults = common.software_differences(root, expected) + common.status_file_faults(root)", "    faults = []", 'the tree\'s software is not checked against the plan'),
 (I, "    if passed is not True:", "    if False:", 'a failed suite does not stop the creation'),
 (I, "                                             write_marker=True)", "                                             write_marker=False)", 'the marker is not asked for'),
 (I, "    if stopping or not found.get('marker'):", "    if not found.get('marker') and False:", 'a failed smoke case does not stop the creation'),
 (I, "    if not kit.made:\r\n        lines = [kit.line()", "    if False:\r\n        lines = [kit.line()", 'a kit that could not be written is not asked about'),
 (I, "        if not common.owner_says_yes(lines, ask, say):\r\n            say('STOPPED: the creation is not finished", "        if False:\r\n            say('STOPPED: the creation is not finished", 'NO to finishing without a kit finishes anyway'),
 (I, "    fingerprint = common.finish(root, plan, expected, now, release=release,", "    fingerprint = common.finish(root, plan, expected, now, release=None,", 'the updater\'s lock is not released before the barrier goes'),
 (I, "        say(snapshot.attempt_snapshot(settings, 'INIT', now).line())", "        say('no backup')", 'the first backup is not attempted'),
 (I, "        if exit_code != EXIT_CREATED:\r\n", "        if False:\r\n", 'a stopped creation is said to be created'),
 (I, "            if tree_as_dev_names_it(view, role) != settings:", "            if False:", 'the settings file is not read back'),
 (T, "    if write_marker and (smoke != ALL_VARIANTS or Path(software_root).resolve() != settings.tree_root.resolve()):", "    if write_marker and (smoke != ALL_VARIANTS):", 'marker: written by software outside the tree'),
 (T, "    if write_marker and (smoke != ALL_VARIANTS or Path(software_root).resolve() != settings.tree_root.resolve()):", "    if write_marker and (Path(software_root).resolve() != settings.tree_root.resolve()):", 'marker: written without every smoke case'),
 (T, "        if found['smoke']['failures']:\r\n            (settings.venv_dir / environment_marker.MARKER_NAME).unlink(missing_ok=True)", "        if found['smoke']['failures']:\r\n            pass", 'marker: an older one is left after a failed smoke case'),
 (T, "        if found['smoke']['failures']:\r\n", "        if False:\r\n", 'marker: written although a smoke case failed'),
 (T, "    if write_marker:\r\n        if found", "    if True:\r\n        if found", 'marker: written without being asked'),
 (C, "    words += ['--write-marker'] if write_marker else []", "    words += []", 'marker: the install tool never asks the program for it'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', *MODULES[relative]], cwd=MUT, timeout=300,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught, how = run.returncode != 0, 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what, flush=True)
print(f'{len(FAULTS)} faults planted; {survived} survived')
