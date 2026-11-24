"""Workspace helper (not project code): plant one fault at a time in a disposable copy of the dev tree and show
that the tests of the launch guard, the process rule, the environment's marker and the job's wiring fail. A fault
no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_launch_guard', 'test_trees_installed_files', 'test_trees_check_tree']
R, E, G, J = 'src/research/process_rule.py', 'src/research/environment_marker.py', 'src/research/launch_guard.py', 'src/research/research_job.py'
FAULTS = [
 (R, "        if _is_inside(process.program, tree_root):", "        if False:", 'a Python that is the tree\'s own program is not listed'),
 (R, "        elif _is_inside(process.working_folder, tree_root):", "        elif False:", 'a Python working in the tree is not listed'),
 (R, "                if _names_the_folder(above.command_line, tree_root):", "                if above is process and _names_the_folder(above.command_line, tree_root):", 'the processes above are not looked at (the pair, the launcher window)'),
 (R, "                above = by_number.get(above.parent_id) if above.parent_id is not None else None", "                above = by_number.get(above.parent_id) if above.parent_id is not None else None\r\n                walked.clear()", 'a ring of parents is walked for ever'),
 (R, "        if process.unreadable:\r\n            listed.append(", "        if False:\r\n            listed.append(", 'an unreadable Python process is passed'),
 (R, "        if process.process_id in left_out or not is_python_name(process.name):", "        if not is_python_name(process.name):", 'the asking program lists itself'),
 (R, "        if process.process_id in left_out or not is_python_name(process.name):", "        if process.process_id in left_out:", 'a program that is not Python is listed'),
 (R, "    return inner == outer or inner.startswith(outer.rstrip('\\\\/') + os.sep)", "    return inner.startswith(outer)", 'a folder whose name begins with the tree\'s counts as inside it'),
 (R, "    if listed:\r\n        lines = ", "    if False:\r\n        lines = ", 'a listed process does not refuse'),
 (E, "            found.extend(_files_below(venv_dir, entry, leave_out_caches=False))", "            pass", 'Scripts is left out of the digest'),
 (E, "        if lowered == SETTINGS_FILE_OF_AN_ENVIRONMENT and (venv_dir / entry).is_file():\r\n            found.append(entry)", "        if False:\r\n            found.append(entry)", 'pyvenv.cfg is left out of the digest'),
 (E, "                    found.extend(_files_below(venv_dir, f'{entry}/{inner}', leave_out_caches=True))", "                    pass", 'the packages are left out of the digest'),
 (E, "            folders[:] = [name for name in folders if name != CACHE_FOLDER_NAME]", "            pass", 'cache folders enter the digest'),
 (E, "            if leave_out_caches and name.lower().endswith(COMPILED_SUFFIX):\r\n                continue", "            if False:\r\n                continue", 'compiled files enter the digest'),
 (E, "            lines.append(f'{path}\\t{hashlib.sha256((venv_dir / path).read_bytes()).hexdigest()}\\n')", "            lines.append(f'{path}\\n')", 'the digest is of names, not of bytes'),
 (E, "    if then != now:", "    if False:", 'a changed package list passes the first gate'),
 (E, "    if marker['digest'] != digest:", "    if False:", 'a changed environment passes the job\'s check'),
 (E, "    if not path.is_file():\r\n        raise EnvironmentRefused(f'{path}: environment not verified.", "    if False:\r\n        raise EnvironmentRefused(f'{path}: environment not verified.", 'a missing marker is not "environment not verified"'),
 (E, "            and content['kind'] == MARKER_KIND and", "            and", 'a file of another kind is taken for the marker'),
 (E, "    os.replace(temporary, target)", "    __import__('shutil').copyfile(temporary, target)", 'the marker\'s temporary file is left in the environment folder'),
 (G, "        if relative != finishing and (Path(tree_root) / relative).exists():", "        if relative != finishing and False:", 'an unfinished operation does not refuse a launch'),
 (G, "        if relative != finishing and (Path(tree_root) / relative).exists():", "        if finishing is None and (Path(tree_root) / relative).exists():", 'a finishing command passes every unfinished operation'),
 (G, "    check_no_unfinished_operation(settings.tree_root, finishing)\r\n    if settings.role in INSTALLED_ROLES:", "    check_no_unfinished_operation(settings.tree_root, finishing)\r\n    if False:", 'QA launches without its environment\'s marker'),
 (G, "        environment_marker.check_digest_is_the_markers(settings.venv_dir, digest)", "        pass", 'the job does not compare the digest with the marker'),
 (G, "        if differences:\r\n            raise GuardRefused(", "        if False:\r\n            raise GuardRefused(", 'software that differs from its list does not refuse the job'),
 (G, "        except installed_files.InstalledFilesRefused as refusal:\r\n            raise GuardRefused(str(refusal)) from None", "        except installed_files.InstalledFilesRefused as refusal:\r\n            differences = []", 'a tree without its list is run'),
 (G, "    looked_at = process_rule.check_no_other_process_of_tree(settings.tree_root)", "    looked_at = 0", 'the job does not apply the process rule'),
 (G, "INSTALLED_ROLES = ('QA', 'PROD')", "INSTALLED_ROLES = ('QA', 'PROD', 'DEV')", 'DEV is asked for a marker and a list it does not have'),
 (J, "            environment_digest = check_at_job_start(settings, say)", "            environment_digest = 'x' * 64", 'the job skips the guard'),
 (J, "environment_digest=environment_digest,\r\n", "environment_digest='0' * 64,\r\n", 'the envelope does not carry the environment\'s digest'),
 ('src/research_command.py', "        environment_folder = check_at_launch(TREE_ROOT).venv_dir", "        from research.settings import read_settings\r\n        environment_folder = read_settings(TREE_ROOT).venv_dir", 'the launcher skips the guard'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', *MODULES], cwd=MUT, timeout=120,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught = run.returncode != 0
    except subprocess.TimeoutExpired:
        caught = True                                  # the tests did not end: the fault was not passed
    path.write_bytes(kept)
    survived += not caught
    print(('caught  ' if caught else 'SURVIVED'), '|', what)
print(f'{len(FAULTS)} faults planted; {survived} survived')
