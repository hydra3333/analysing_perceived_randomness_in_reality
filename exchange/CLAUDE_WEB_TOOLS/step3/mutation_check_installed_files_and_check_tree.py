"""Workspace helper (not project code): plant one fault at a time in a disposable copy of the dev tree and show
that the step 2 tests fail. A fault no test catches is printed as SURVIVED."""
import subprocess, sys
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
FAULTS = [
 ('src/research/installed_files.py', "elif hashlib.sha256(file.read_bytes()).hexdigest() != installed_digest:", "elif False:", 'a changed file is not noticed'),
 ('src/research/installed_files.py', "if not file.is_file():\r\n            found.append(f'{path}: it is on the list", "if False:\r\n            found.append(f'{path}: it is on the list", 'a missing listed file is not noticed'),
 ('src/research/installed_files.py', "if not (root / path).is_file():\r\n            found.append(f'{path}: the status file", "if False:\r\n            found.append(f'{path}: the status file", 'a missing status file is not noticed'),
 ('src/research/installed_files.py', "if path not in listed and path not in status_files:", "if False:", 'an unlisted file under src is not noticed'),
 ('src/research/installed_files.py', "elif name == CACHE_FOLDER_NAME:", "elif False:", 'the cache folder is entered, file by file'),
 ('src/research/installed_files.py', "if is_link(Path(current) / name):\r\n                others.append(f'{from_root(name)}: a link or a junction", "if False:\r\n                others.append(f'{from_root(name)}: a link or a junction", 'a folder link is entered'),
 ('src/research/installed_files.py', "'status_files': [f'{METHODS_FOLDER}/{variant.family}/{variant.variant}/{variant_folders.STATUS_FILE_NAME}'\r\n                             for variant in variants]}", "'status_files': []}", 'status files are left off the list'),
 ('src/research/installed_files.py', "    if refused:\r\n        raise InstalledFilesRefused(f'{len(refused)} variant", "    if False:\r\n        raise InstalledFilesRefused(f'{len(refused)} variant", 'a broken variant folder is listed anyway'),
 ('src/research/installed_files.py', "content.get('kind') == LIST_KIND", "True", 'a file of another kind is taken for the list'),
 ('src/research/installed_files.py', "    os.replace(temporary, target)", "    __import__('shutil').copyfile(temporary, target)", 'the temporary file is left behind'),
 ('src/research/code_identity.py', "if section == FILES_SECTION and not (Path(tree_root) / path).is_file():", "if not (Path(tree_root) / path).is_file():", 'the manifest of an installed tree refuses for a DEV-only tool'),
 ('src/research/code_identity.py', "    for path in tool_files:\r\n        if not (Path(tree_root) / path).is_file():", "    for path in tool_files:\r\n        if False:", 'a missing install tool is not refused in DEV'),
 ('deploy/check_tree.py', "            findings.extend(drift)", "            pass", 'drift is counted but not found'),
 ('deploy/check_tree.py', "            tree = settings.tree_as_dev_names_it(view, role)", "            tree = settings.read_settings(entry.tree_root)", 'a tree whose own file says another role is looked at'),
 ('deploy/check_tree.py', "if not entry.tree_root.exists() or not any(entry.tree_root.iterdir()):", "if False:", 'a tree not yet created is not said as such'),
 ('deploy/check_tree.py', "            findings.append(str(refusal))\r\n    return variants, findings", "            pass\r\n    return variants, findings", 'a status file failing its own check is not found'),
 ('deploy/check_tree.py', "        findings.extend(f'{fault.path}: {fault.what}' for fault in faults)", "        pass", 'a file in the wrong form is not found'),
 ('deploy/check_tree.py', "    paths.add(SETTINGS_FILE)", "    pass", 'the settings file is not checked for its form'),
 ('deploy/check_tree.py', "if entry.is_file() and not entry.name.startswith(RETIRED_OPENING_RECORD_PREFIX))", "if entry.is_file())", 'the retired opening record is checked'),
 ('deploy/check_tree.py', "paths.update(f'{RESULTS_FOLDER}/{entry.name}' for entry in results_folder.iterdir()", "paths.update(file_form.files_under(tree_root, (RESULTS_FOLDER,), False) if False else (f'{RESULTS_FOLDER}/{entry.name}' for entry in ()) if False else (f'{RESULTS_FOLDER}/{p.relative_to(results_folder).as_posix()}' for p in results_folder.rglob('*') if p.is_file()) for entry in [0]", None),
 ('deploy/check_tree.py', "if entry.is_file() and entry.name.lower().endswith(BACKUP_SUFFIX))", "if entry.is_file())", 'a .partial is listed as a backup'),
 ('deploy/check_tree.py', "elif found.fingerprint != installed[name]:", "elif False:", 'a variant installed with other bytes is not said'),
 ('deploy/check_tree.py', "    return EXIT_FOUND if findings else EXIT_NOTHING_FOUND", "    return EXIT_NOTHING_FOUND", 'the exit code never says that something was found'),
 ('deploy/check_tree.py', "(job_lock.ORPHAN_MARKER, 'THE ORPHAN MARKER", "('no/such/file', 'THE ORPHAN MARKER", 'the orphan marker is not shown'),
]
survived = 0
for relative, old, new, what in FAULTS:
    if what is None:
        continue
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    run = subprocess.run([PY, '-B', '-m', 'unittest', 'test_trees_installed_files', 'test_trees_check_tree'], cwd=MUT,
                         env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
    path.write_bytes(kept)
    caught = run.returncode != 0
    survived += not caught
    print(('caught  ' if caught else 'SURVIVED'), '|', what)
print(f'{len([f for f in FAULTS if f[3]])} faults planted; {survived} survived')
