"""Workspace helper (not project code): the planted faults for the corrections EX_323 asked for in slice B (B-B01 to
B-B04, B-C01 to B-C03). One fault at a time is planted in a disposable copy of the dev tree that holds the overlay;
the slice's two test modules must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_snapshot', 'test_trees_restore']
S, R, K, J = 'src/research/snapshot.py', 'deploy/restore_tool.py', 'deploy/recovery_kit.py', 'src/research/research_job.py'
FAULTS = [
 (S, "        if archive.read(MANIFEST_NAME) != manifest_bytes:", "        if False:", 'B-B01: the manifest is not read back'),
 (S, "            if archive.read(folder + '/') != b'':", "            if False:", 'B-B01: an empty folder\'s member is not read back'),
 (S, "zipfile.LargeZipFile, zlib.error,\r\n            EOFError) as failure:", "zipfile.LargeZipFile) as failure:", 'B-B01: an archive that does not decompress is an exception, not a result'),
 (R, "            if SETTINGS_FILE not in listed:", "            if False and SETTINGS_FILE not in listed:", 'B-B02: a backup without its settings file is accepted'),
 (R, "    if (not os.path.isabs(named) or not os.path.isabs(root) or not _same_place(named, root)\r\n            or manifest.get('role') != role):", "    if False:", 'B-B02: the manifest\'s root and role are not checked against the settings'),
 (R, "not _same_place(named, root)\r\n            or manifest.get('role') != role):", "not _same_place(named, root)):", 'B-B02: another role than the settings\' passes'),
 (R, "    if (not os.path.isabs(named) or not os.path.isabs(root) or not _same_place(named, root)", "    if (not _same_place(named, root)", 'B-B02: a root that is not a full path passes'),
 (R, "        if sorted(entry['path'] for entry in manifest['files']) != sorted(KIT_FILES):", "        if False:", 'B-B02: a kit whose list omits its files passes its self-check'),
 (R, "    if os.getpid() not in {entry[0] for entry in table}:", "    if False:", 'B-B03: a table that does not hold the tool itself is taken as whole'),
 (R, "    if error_code != ERROR_NO_MORE_FILES:", "    if error_code not in (ERROR_NO_MORE_FILES, 0, 5, 299):", 'B-B03: a reading that stopped part-way is taken for the table\'s end'),
 (R, "                              capture_output=True)", "                              capture_output=True, timeout=300)", 'B-B03: a time limit that ends the Python it started'),
 (R, "    elif old_marker['bytes'] is not None:\r\n        evidence, evidence_from = old_marker['bytes'], 'the old tree'", "    elif False:\r\n        evidence, evidence_from = old_marker['bytes'], 'the old tree'", 'B-B04: a marker only in the old tree is not kept as evidence'),
 (R, "                old_marker['bytes'] = (tree_root / ORPHAN_MARKER).read_bytes()", "                old_marker['bytes'] = b''", 'B-B04: the evidence is not the old marker\'s bytes'),
 (R, "manifest['orphan_marker_time'] + ZIP_TIME_STEP))", "manifest['orphan_marker_time']))", 'B-B04: a restart inside the ZIP\'s two seconds counts as a later restart'),
 (R, "                  'evidence_file': f'{name}_ORPHAN_MARKER.json' if evidence is not None else None,", "                  'evidence_file': f'{name}_ORPHAN_MARKER.json',", 'B-B04: evidence is said to be kept when the marker could not be read'),
 (R, "    if files != wanted or folders != _folders_of(list(wanted) + [PROGRESS_FILE], manifest['empty_folders']):", "    if files != wanted:", 'B-C01: the fresh tree\'s folders are not compared'),
 (R, "    for current, _folders, names in os.walk(tree_root, onerror=stop):", "    for current, _folders, names in os.walk(tree_root):", 'B-C01: a folder that cannot be listed is read as absent'),
 (R, "            if hashlib.sha256(data).hexdigest() != listed[name]:", "            if False:", 'B-C01: the settings file is written without a check of its bytes'),
 (R, "    os.utime(tree_root / SETTINGS_FILE, (settings_time, settings_time))", "    pass", 'B-C01: the settings file\'s time is not restored'),
 (R, "        if not its_own or files != listed or folders != _folders_of(listed, manifest['empty_folders']):", "        if not its_own or files != listed:", 'B-C01: the reconciliation ignores a missing empty folder'),
 (R, "            its_own = lying.is_file() and lying.read_bytes() == manifest['manifest_bytes']", "            its_own = lying.is_file()", 'B-C01: the reconciliation accepts another manifest at the root'),
 (S, "            if final.exists() or partial.exists():           # checked before this attempt owns any file: a", "            if final.exists():", 'B-C02: an earlier attempt\'s ".partial" is written over or removed'),
 (S, "        if beside[:1] != [_hash_of_file(path)]:\r\n            return False", "        if False:\r\n            return False", 'B-C02: a kit whose ".sha256" does not agree is named'),
 (S, "            return json.loads(kit.read('KIT_MANIFEST.json')).get('software_fingerprint') == fingerprint", "            return 'software_fingerprint' in json.loads(kit.read('KIT_MANIFEST.json'))", 'B-C02: a kit of another software state is named'),
 (S, "        if _is_the_kit_of(backup_root / name, fingerprint):\r\n            return name", "        if True:\r\n            return name", 'B-C02: any file with a kit\'s name is named'),
 (K, "            with open(beside, 'wb') as handle:               # the \".sha256\" first: a kit that has its name\r\n                handle.write(f'{digest} *{name}\\r\\n'.encode('ascii'))     # always has its \".sha256\" beside it\r\n            os.replace(partial, final)", "            os.replace(partial, final)\r\n            with open(beside, 'wb') as handle:\r\n                handle.write(f'{digest} *{name}\\r\\n'.encode('ascii'))", 'B-C02: the kit is named before its ".sha256" is written'),
 (K, "            for ours in (partial, beside):                   # only what this attempt made itself", "            for ours in (partial,):", 'B-C02: a kit that failed leaves its ".sha256"'),
 (K, "        if final.exists() or partial.exists() or beside.exists():", "        if final.exists() or partial.exists():", 'B-C02: another attempt\'s ".sha256" is written over'),
 (J, "    mark_due(settings)\r\n    for leftover in discard_unfinished_writes(tree_root):", "    for leftover in discard_unfinished_writes(tree_root):", 'B-C03: the job writes no note that a backup is owed'),
 (J, "        if settings is not None and is_due(settings.tree_root) and not due_before:", "        if False:", 'B-C03: a refusal after the note says "nothing was written" and tries no backup'),
 (J, "    manifest = read_manifest(tree_root)\r\n", "    mark_due(settings)\r\n    manifest = read_manifest(tree_root)\r\n", 'B-C03: the note is written before the checks that may refuse'),
 (J, "        say(f'RESEARCH JOB - END - {now().astimezone().strftime(\"%Y-%m-%d %H:%M\")} - the {settings.role} tree at '", "        say(f'RESEARCH JOB - END - {started} - the {settings.role} tree at '", 'B-C03: the END line gives a time from before the backup'),
 (S, "    except OSError as error:\r\n        raise LaunchRefused(f'{path}: the note that a backup is owed could not be written", "    except ZeroDivisionError as error:\r\n        raise LaunchRefused(f'{path}: the note that a backup is owed could not be written", 'B-C03: a note that cannot be written is an unhandled exception'),
 (S, "Every file is read three times (hashed, '", "The whole tree is read twice (hashed, '", 'B-C03: the command says the tree is read twice'),
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
    print((how if caught else 'SURVIVED'), '|', what)
print(f'{len(FAULTS)} faults planted; {survived} survived')
