"""Workspace helper (not project code): the planted faults for slice C part C2, second piece (deploy/install_common.py:
the plan, the barrier, the copying, the list of installed files). One fault at a time in a disposable copy of the dev
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
