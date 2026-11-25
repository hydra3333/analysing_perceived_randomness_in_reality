"""Workspace helper (not project code): the planted faults for slice C part C2, second and third pieces
(deploy/install_common.py: the plan, the barrier, the copying, the list of installed files; reserving the target,
the rollback point and the one question, the checks with the target's Python). One fault at a time in a disposable copy of the dev
tree that holds the overlay; tests/test_trees_install_common.py must fail. A fault no test catches is SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_install_common']
C = 'deploy/install_common.py'
FAULTS = [
 (C, "    if not readiness.ready:\r\n        raise InstallRefused(readiness.reason)", "    if False:\r\n        raise InstallRefused(readiness.reason)", 'infrastructure that is not ready is offered'),
 (C, "    files = {path: marked[path] for path in classes}", "    files = dict(marked)", 'the install tools are offered for installing'),
 (C, "    files[code_identity.MANIFEST_PATH] = variant_folders.sha256_of_file(", "    marked[code_identity.MANIFEST_PATH] = variant_folders.sha256_of_file(", 'the manifest itself is not offered'),
 (C, "        if not readiness.ready:\r\n            not_ready[variant.identity] = readiness.reason.splitlines()[0]\r\n            continue", "        if not readiness.ready:\r\n            not_ready[variant.identity] = readiness.reason.splitlines()[0]", 'a variant that is not ready is offered'),
 (C, "    ready, not_ready = {}, {identity: str(reason).splitlines()[0] for identity, reason in refused}", "    ready, not_ready = {}, {}", 'a broken variant folder is not reported'),
 (C, "            'add': [{'path': path, 'sha256': add[path]} for path in sorted(add)],", "            'add': [{'path': path, 'sha256': add[path]} for path in add],", 'the plan depends on the order given'),
 (C, "    if found == plan:\r\n        return True\r\n", "    if found == plan:\r\n        return False\r\n", 'the same plan found is taken for a new install'),
 (C, "    if (replace_unfinished and plan['operation'] == REINSTALL_INFRA\r\n            and found.get('operation') == REINSTALL_INFRA):", "    if (replace_unfinished and plan['operation'] == REINSTALL_INFRA):", 'replace-unfinished replaces the barrier of another operation'),
 (C, "    if (replace_unfinished and plan['operation'] == REINSTALL_INFRA\r\n            and found.get('operation') == REINSTALL_INFRA):", "    if (plan['operation'] == REINSTALL_INFRA\r\n            and found.get('operation') == REINSTALL_INFRA):", 'another reinstall plan is replaced without being asked'),
 (C, "    if (replace_unfinished and plan['operation'] == REINSTALL_INFRA\r\n            and found.get('operation') == REINSTALL_INFRA):", "    if (replace_unfinished\r\n            and found.get('operation') == REINSTALL_INFRA):", 'an install replaces an unfinished reinstall'),
 (C, "        if content['kind'] != BARRIER_KIND or not isinstance(content['plan'], dict):", "        if False:", 'a file of another kind is read as a barrier'),
 (C, "    if not path.exists() and not is_link(path):\r\n        return None\r\n    try:", "    if True:\r\n        return None\r\n    try:", 'a barrier is never seen'),
 (C, "    if found == plan:\r\n        return\r\n", "", 'the same plan is written again'),
 (C, "    if is_link(path.parent) or is_link(path):", "    if False:", 'a records folder that is a link is written through'),
 (C, "        if _hash_of(target) == sha256:\r\n            return False\r\n", "", 'a file already in place is copied again or refused'),
 (C, "        if not replace:\r\n            raise InstallRefused(f'{target}: already installed with different bytes.", "        if False:\r\n            raise InstallRefused(f'{target}: already installed with different bytes.", 'an installed file is changed by an addition'),
 (C, "    if _hash_of(temporary) != sha256:", "    if False:", 'a source that is not the plan\'s bytes is put in place'),
 (C, "    if _hash_of(temporary) != sha256:\r\n        temporary.unlink()", "    if _hash_of(temporary) != sha256:", 'a refused copy leaves its temporary file'),
 (C, "    _check_no_link_on_the_way(tree_root, relative)\r\n    if is_link(target)", "    if is_link(target)", 'a link on the way is written through'),
 (C, "    if is_link(target) or (target.exists() and not target.is_file()):", "    if is_link(target):", 'a folder where a file belongs is not refused'),
 (C, "    for entry, replace in ([(entry, False) for entry in plan['add']] + [(entry, True) for entry in plan['overwrite']]):", "    for entry, replace in ([(entry, False) for entry in plan['add']]):", 'the overwrites are not made'),
 (C, "    for entry, replace in ([(entry, False) for entry in plan['add']] + [(entry, True) for entry in plan['overwrite']]):", "    for entry, replace in ([(entry, True) for entry in plan['add']] + [(entry, True) for entry in plan['overwrite']]):", 'an addition may replace an installed file'),
 (C, "        if _hash_of(target) != entry['was']:", "        if False:", 'a file with other bytes than the plan found is removed'),
 (C, "        target.unlink()\r\n        removed += 1", "        removed += 1", 'the removals are not made'),
 (C, "        if not target.exists():\r\n            continue\r\n", "", 'a removal already made stops the same command'),
 (C, "            if path.exists():\r\n                read_status(path, entry['games'])", "            if path.exists():\r\n                pass", 'a broken status file found there is accepted'),
 (C, "                create_active(path, entry['family'], entry['variant'], entry['games'])\r\n                created += 1", "                created += 1", 'no status file is created'),
 (C, "    for entry in plan['add'] + plan['overwrite']:\r\n        files[entry['path']] = entry['sha256']", "    for entry in plan['add']:\r\n        files[entry['path']] = entry['sha256']", 'an overwrite is not in what is expected'),
 (C, "    for entry in plan['remove']:\r\n        files.pop(entry['path'], None)", "    for entry in ():\r\n        files.pop(entry['path'], None)", 'a removal is still expected'),
 (C, "                for entry in (before or {'variants': []})['variants'] + plan['variants']}", "                for entry in plan['variants']}", 'the variants installed before are forgotten'),
 (C, "    found = installed_files.differences(tree_root, expected)\r\n    if found:\r\n        return found", "    found = []", 'the files are not compared with the plan'),
 (C, "    if now != expected:", "    if False:", 'the tree\'s own reading is not compared'),
 (C, "            faults.append(f'{variant.identity}: {refusal}')", "            pass", 'a status file that fails its check is not a fault'),
 (C, "    installed_files.write_list(tree_root, expected)\r\n", "", 'the list of installed files is not written'),
 (C, "    remove_barrier(tree_root)\r\n    return fingerprint", "    return fingerprint", 'the barrier is not removed'),
 (C, "    installed_files.write_list(tree_root, expected)\r\n    fingerprint", "    remove_barrier(tree_root)\r\n    installed_files.write_list(tree_root, expected)\r\n    fingerprint", 'the barrier is removed first'),
 (C, "'software_fingerprint': fingerprint},", "'software_fingerprint': None},", 'the log does not hold the software fingerprint'),
 (C, "    with job_lock(root, purpose, started):\r\n        looked_at", "    if True:\r\n        looked_at", 'reserve: the job lock is not taken'),
 (C, "        looked_at = process_rule.check_no_other_process_of_tree(root)", "        looked_at = 0", 'reserve: no process check under the lock'),
 (C, "        check_no_orphan_marker(root)\r\n        check_no_unfinished_operation(root, finishing=BARRIER_PATH)", "        check_no_unfinished_operation(root, finishing=BARRIER_PATH)", 'reserve: the orphan marker does not refuse'),
 (C, "        check_no_unfinished_operation(root, finishing=BARRIER_PATH)", "        pass", 'reserve: another unfinished operation does not refuse'),
 (C, "        check_no_unfinished_operation(root, finishing=BARRIER_PATH)", "        check_no_unfinished_operation(root)", 'reserve: an unfinished install can never be continued'),
 (C, "        if (root / UPDATER_LOCK).exists():", "        if False:", 'reserve: a results update that holds its lock does not refuse'),
 (C, "    write_barrier(settings.tree_root, plan, started)\r\n    lock = updater_lock(", "    lock = updater_lock(", 'changing: no barrier is written'),
 (C, "    lock.__enter__()\r\n    released = []", "    released = []", 'changing: the updater\'s lock is not taken'),
 (C, "        snapshot.mark_due(settings)\r\n        yield release", "        yield release", 'changing: the note that a backup is owed is not written'),
 (C, "    finally:\r\n        release()", "    finally:\r\n        pass", 'changing: a fault leaves the updater\'s lock held'),
 (C, "    if release is not None:\r\n        release()\r\n    remove_barrier(tree_root)", "    remove_barrier(tree_root)\r\n    if release is not None:\r\n        release()", 'finish: the barrier is removed before the updater\'s lock is released'),
 (C, "    kit = recovery_kit.build_kit(dev_root, settings.backup_root, software_fingerprint_of(expected), now)", "    kit = recovery_kit.build_kit(dev_root, settings.backup_root, 'x' * 64, now)", 'rollback: the kit is not for the software state to come'),
 (C, "    backup = snapshot.attempt_snapshot(settings, backup_job, now)", "    backup = snapshot.attempt_snapshot(settings, 'MANUAL', now)", 'rollback: the backup does not carry its name'),
 (C, "    if not backup.made:\r\n        lines.append('NO ROLLBACK POINT", "    if False:\r\n        lines.append('NO ROLLBACK POINT", 'question: a backup that was not made is not warned of'),
 (C, "    if not kit.made:\r\n        lines.append('THE RESTORE TOOL", "    if False:\r\n        lines.append('THE RESTORE TOOL", 'question: a kit that was not written is not warned of'),
 (C, "    if not backup.made:\r\n        lines.append('NO ROLLBACK POINT", "    if True:\r\n        lines.append('NO ROLLBACK POINT", 'question: a warning of no rollback point when there is one'),
 (C, "    return answer.strip() == YES", "    return answer.strip().upper() == YES", 'question: yes in small letters is taken for YES'),
 (C, "    return answer.strip() == YES", "    return answer.strip().startswith(YES)", 'question: YES with more on the line is taken for YES'),
 (C, "    except EOFError:\r\n        answer = ''", "    except EOFError:\r\n        answer = YES", 'question: an input that has ended is taken for YES'),
 (C, "    if not python.is_file():", "    if False:", 'checks: a tree without its Python is not refused'),
 (C, "    return sorted(path for path, digest in dev_files.items() if held.get(path) != digest)", "    return sorted(path for path, digest in dev_files.items() if path in held and held[path] != digest)", 'suite: a tree that lacks an infrastructure file counts as DEV\'s'),
 (C, "    if differing:\r\n        return None,", "    if False:\r\n        return None,", 'suite: it is run for a tree whose infrastructure is not DEV\'s'),
 (C, "        result = suite_on_copy.run_suite(dev_root, python, say)", "        result = suite_on_copy.run_suite(dev_root, Path(__import__('sys').executable), say)", 'suite: it is run with DEV\'s Python, not the target\'s'),
 (C, "    return result.passed, result.line()", "    return True, result.line()", 'suite: a failed suite is reported as passed'),
 (C, "    words = [str(python), '-I', '-B', '-u',", "    words = [str(python), '-B', '-u',", 'checks: the program is not started in isolated mode'),
 (C, "             '--data', str(tree_root), '--result', str(result),", "             '--data', str(software_root), '--result', str(result),", 'checks: the data read is the software folder\'s, not the tree\'s'),
 (C, "    words += ['--sample'] if sample else []", "    words += ['--sample']", 'checks: the sample is asked when it was not wanted'),
 (C, "    words += ['--derived'] if derived else []", "    words += []", 'checks: the derived results are never asked'),
 (C, "            found = json.loads(result.read_bytes().decode('ascii')) if ended == 0 else None", "            found = json.loads(result.read_bytes().decode('ascii'))", 'checks: a result left by a program that refused is believed'),
 (C, "    if not isinstance(found, dict) or found.get('kind') != CHECKS_RESULT_KIND:", "    if not isinstance(found, dict):", 'checks: a result of another kind is believed'),
 (C, "    finally:\r\n        shutil.rmtree(folder, ignore_errors=True)", "    finally:\r\n        pass", 'checks: the temporary folder is left behind'),
 (C, "    faults = list((found['smoke'] or {'failures': []})['failures'])", "    faults = []", 'verdict: a failed smoke case does not stop the install'),
 (C, "               for game_id, why in sorted((found['unreadable'] or {}).items())]", "               for game_id, why in ()]", 'verdict: an unreadable game does not stop the install'),
 (C, "    faults += list((found['sample'] or {'differences': []})['differences'])", "    faults += []", 'verdict: a sample difference does not stop the install'),
 (C, "        if answer is not None and not answer['known']:", "        if False:", 'verdict: an unexpected derived difference does not stop the install'),
 (C, "        if answer is not None and not answer['known']:", "        if answer is not None:", 'verdict: a difference the tree already marks stops the install'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', *MODULES], cwd=MUT, timeout=300,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught, how = run.returncode != 0, 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what, flush=True)
print(f'{len(FAULTS)} faults planted; {survived} survived')
