"""Workspace helper (not project code): the planted faults for slice C part C4 (deploy/install.py). One fault at a
time in a disposable copy of the dev tree that holds the overlay; tests/test_trees_install.py must fail. A fault no
test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
N = 'deploy/install.py'
FAULTS = [
 (N, "    if unfinished is None or unfinished.get('operation') != common.INSTALL:\r\n        return current", "    if unfinished is None:\r\n        return current", 'list before: another operation\'s barrier is undone too'),
 (N, "            'files': [entry for entry in current['files'] if (entry['path'], entry['sha256']) not in added],", "            'files': list(current['files']),", 'list before: the files a finished copy added stay on it'),
 (N, "            'variants': [entry for entry in current['variants']\r\n                         if (entry['family'], entry['variant'], entry['fingerprint']) not in arrived],", "            'variants': list(current['variants']),", 'list before: the variants that arrived stay on it'),
 (N, "    if unknown:\r\n        raise common.InstallRefused(f'--only names", "    if False:\r\n        raise common.InstallRefused(f'--only names", 'plan: a name after --only that is no variant is ignored'),
 (N, "    wanted = [identity for identity in sorted(set(ready) | set(not_ready)) if only is None or identity in only]", "    wanted = [identity for identity in sorted(set(ready) | set(not_ready))]", 'plan: --only does not narrow'),
 (N, "        if identity in installed and identity in ready:", "        if False:", 'plan: an installed variant is installed again'),
 (N, "            left_out[identity] = ALREADY if installed[identity] == ready[identity]['fingerprint'] else ALREADY_OTHER", "            left_out[identity] = ALREADY", 'plan: different bytes are called already installed'),
 (N, "        elif identity in ready:\r\n            to_add.append(ready[identity])\r\n        else:\r\n            left_out[identity] = not_ready[identity]", "        else:\r\n            to_add.append((ready | {identity: None})[identity]) if identity in ready else left_out.update({identity: ''})", 'plan: the reason a variant is not ready is lost'),
 (N, "            if path not in held:\r\n                add[path] = digest", "            if True:\r\n                add[path] = digest", 'plan: a helper the target holds is planned again'),
 (N, "            elif held[path] != digest:\r\n                conflicts.setdefault(path, []).append(f'{entry[\"family\"]}/{entry[\"variant\"]}')", "            elif False:\r\n                conflicts.setdefault(path, []).append(f'{entry[\"family\"]}/{entry[\"variant\"]}')", 'plan: a helper with other bytes is not a conflict'),
 (N, "    if not to_add:\r\n        return None", "    if False:\r\n        return None", 'plan: nothing to add still makes a plan'),
 (N, "        if plan is None and unfinished is None:", "        if False:", 'nothing to add does not end the command'),
 (N, "            drift = installed_files.differences(root, current)\r\n            if drift:", "            drift = installed_files.differences(root, current)\r\n            if False:", 'software changed outside the tools is not refused'),
 (N, "            with common.reserved(settings, f'Install {role}: a look before the backup', started, say):\r\n                pass\r\n", "", 'no look at the tree before the backup'),
 (N, "            kit, backup = common.attempt_rollback_point(dev_root, settings, 'PRE_INSTALL', expected, now, say)", "            kit, backup = common.attempt_rollback_point(dev_root, settings, 'MANUAL', expected, now, say)", 'the backup before is not named PRE_INSTALL'),
 (N, "            if not common.owner_says_yes(common.question_lines(kit, backup), ask, say):", "            if False:", 'the install goes on without the question'),
 (N, "        if continuing:\r\n            say('This same install", "        if True:\r\n            say('This same install", 'a new install attempts no backup and asks nothing'),
 (N, "        with common.reserved(settings, f'Install {role}', started, say):\r\n            common.check_barrier(root, plan)", "        if True:\r\n            common.check_barrier(root, plan)", 'the target is not reserved before the copying'),
 (N, "                common.carry_out(dev_root, root, plan, say)\r\n", "", 'no file is copied'),
 (N, "                created = common.create_status_files(root, plan)", "                created = 0", 'no status file is created'),
 (N, "    faults = common.software_differences(root, expected) + common.status_file_faults(root)", "    faults = []", 'the tree\'s software is not checked against the old list and the plan'),
 (N, "    if suite is False:", "    if False:", 'a failed suite does not stop the install'),
 (N, "        suite, line = common.suite_if_it_is_the_trees(dev_root, dev_files, expected, python, say)", "        suite, line = None, 'not run'", 'the suite is never run'),
 (N, "    found = common.checks_with_target_python(python, root, root, new, True, True, say)", "    found = common.checks_with_target_python(python, root, root, common.ALL_VARIANTS, True, True, say)", 'every variant is made to forecast, not the new ones'),
 (N, "    found = common.checks_with_target_python(python, root, root, new, True, True, say)", "    found = common.checks_with_target_python(python, root, root, new, False, True, say)", 'the forecast sample is not asked'),
 (N, "    found = common.checks_with_target_python(python, root, root, new, True, True, say)", "    found = common.checks_with_target_python(python, root, root, new, True, False, say)", 'the derived results are not asked'),
 (N, "    if stopping:\r\n        say(f'STOPPED: {len(stopping)} finding(s) of the checks", "    if False:\r\n        say(f'STOPPED: {len(stopping)} finding(s) of the checks", 'a finding of the checks does not stop the install'),
 (N, "    fingerprint = common.finish(root, plan, expected, now, release=release,", "    fingerprint = common.finish(root, plan, expected, now, release=None,", 'the updater\'s lock is not released before the barrier goes'),
 (N, "        say(snapshot.attempt_snapshot(settings, 'POST_INSTALL', now).line())", "        say('no backup')", 'no backup is attempted after'),
 (N, "        if exit_code != EXIT_INSTALLED:\r\n", "        if False:\r\n", 'a stopped install is said to be installed'),
 (N, "                return EXIT_REFUSED\r\n        with common.reserved", "                return EXIT_INSTALLED\r\n        with common.reserved", 'NO is reported as installed'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', 'test_trees_install'], cwd=MUT, timeout=300,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught, how = run.returncode != 0, 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what, flush=True)
print(f'{len(FAULTS)} faults planted; {survived} survived')
