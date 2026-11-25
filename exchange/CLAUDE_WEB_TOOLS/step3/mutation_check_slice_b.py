"""Workspace helper (not project code): the planted faults for slice B (the backup, the recovery kit, restore). One
fault at a time is planted in a disposable copy of the dev tree that holds the overlay; the slice's test modules
must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_snapshot', 'test_trees_restore']
S, R, K, J = 'src/research/snapshot.py', 'deploy/restore_tool.py', 'deploy/recovery_kit.py', 'src/research/research_job.py'
FAULTS = [
 (S, "kept = [prefix + name for name in names if prefix + name not in LEFT_OUT]", "kept = [prefix + name for name in names]", 'the two control files are backed up'),
 (S, "LEFT_OUT = (DUE_PATH, LOCK_PATH)", "LEFT_OUT = (DUE_PATH, LOCK_PATH, f'{RECORDS_FOLDER}/INSTALLED_FILES.json')", 'a third file is left out of a backup'),
 (S, "        if not folders and not kept and prefix:\r\n            empty.append(relative)", "        if False:\r\n            empty.append(relative)", 'empty folders are not kept'),
 (S, "            if is_link(os.path.join(current, name)):", "            if False:", 'a link in the tree is followed or passed'),
 (S, "                _check_archive(partial, hashes, empty)\r\n", "", 'the archive is not read back'),
 (S, "            if digest.hexdigest() != expected:", "            if False:", 'a member that reads back as other bytes passes'),
 (S, "                _check_sources_again(tree_root, hashes, empty)\r\n", "", 'the sources are not read a second time'),
 (S, "        if _hash_of_file(tree_root / relative) != hashes[relative]:", "        if False:", 'a file changed during the backup passes'),
 (S, "    if files != sorted(hashes) or empty_now != sorted(empty):", "    if False:", 'a file added or removed during the backup passes'),
 (S, "                process_rule.check_no_other_process_of_tree(tree_root)\r\n                backup_root.mkdir", "                backup_root.mkdir", 'no process check before the first reading'),
 (S, "                process_rule.check_no_other_process_of_tree(tree_root)\r\n                archive_digest", "                archive_digest", 'no process check after the second reading'),
 (S, "            if (tree_root / held).exists():", "            if False:", 'a backup is made while a job or the updater holds its lock'),
 (S, "        with FileLock(tree_root / LOCK_PATH, f'backup {name}', moment.astimezone().strftime('%Y-%m-%d %H:%M')):", "        if True:", 'the backup takes no lock'),
 (S, "                os.replace(partial, final)\r\n            except BaseException:\r\n                try:\r\n                    partial.unlink()", "                os.replace(partial, final)\r\n            except BaseException:\r\n                try:\r\n                    pass", 'a failed backup leaves its ".partial"'),
 (S, "                if final.exists() or partial.exists():", "                if False:", 'a backup of the same name is written over'),
 (S, "                (tree_root / DUE_PATH).unlink()", "                pass", 'a verified backup does not remove the note that one is owed'),
 (S, "    except (BackupNotMade, LaunchRefused, OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as failure:\r\n        return SnapshotResult(False, reason=f'{failure}')", "    except (BackupNotMade, LaunchRefused, OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as failure:\r\n        try:\r\n            (tree_root / DUE_PATH).unlink()\r\n        except OSError:\r\n            pass\r\n        return SnapshotResult(False, reason=f'{failure}')", 'a failed backup removes the note that one is owed'),
 (S, "                if (tree_root / MANIFEST_NAME).exists():", "                if False:", 'a backup is made of a tree unzipped by hand and not reconciled'),
 (S, "    if settings.backup_root is None or (moment == 'start' and not is_due(settings.tree_root)):", "    if settings.backup_root is None or moment == 'start':", 'a job never tries first the backup that is owed'),
 (S, "    if not result.made:\r\n        say(STANDING_WARNING)", "    if False:\r\n        say(STANDING_WARNING)", 'no standing warning when no backup could be made'),
 (S, "    if settings.backup_root is None:\r\n        return\r\n    path = settings.tree_root / DUE_PATH", "    if True:\r\n        return\r\n    path = settings.tree_root / DUE_PATH", 'the note that a backup is owed is never written'),
 (J, "            mark_due(settings)                               # before the job's first write\r\n", "", 'the job does not write the note before its first write'),
 (J, "        backup_for_a_job(settings, 'end', now, say)          # the job's lock is released: the tree is quiet\r\n", "", 'the job makes no backup at its end'),
 (J, "        backup_for_a_job(settings, 'start', now, say)        # only if a backup is owed from earlier work\r\n", "", 'the job does not try an owed backup at its start'),
 (K, "            if marked.get(source) != hashlib.sha256(data).hexdigest():", "            if False:", 'a kit is built from a file the marker does not list'),
 (K, "                if {member: archive.read(member) for member in archive.namelist()} != contents:", "                if False:", 'the kit is not read back'),
 (K, "        contents[KIT_MANIFEST_NAME] = ", "        contents['KIT_LIST.json'] = ", 'the kit has no manifest the tool can check'),
 (R, "        if not file.is_file() or sha256_of(file) != expected:", "        if False:", 'a damaged kit passes its self-check'),
 (R, "                if found.hexdigest() != wanted:", "                if False:", 'a damaged member of the backup passes'),
 (R, "            if sorted(names[:-1]) != expected:", "            if False:", 'a backup with members its manifest does not list passes'),
 (R, "                if name.startswith('/') or ':' in name or '\\\\' in name or '..' in parts or '' in parts:", "                if False:", 'a member that would leave the tree is unpacked'),
 (R, "    if not backup.is_file() or backup.name.endswith('.partial'):", "    if not backup.is_file():", 'a ".partial" is taken for a backup'),
 (R, "    return [entry for entry in table if PYTHON_NAME.match(entry[2] or '') and entry[0] not in own]", "    return [entry for entry in table if PYTHON_NAME.match(entry[2] or '') and entry[0] != own_number]", 'the tool\'s own launcher above it is listed'),
 (R, "        if above is None or above[3] is None or current[3] is None or above[3] > current[3]:", "        if above is None:", 'a newer program with a reused number is taken for the tool\'s parent'),
 (R, "PYTHON_NAME = re.compile(r'^(python[0-9.]*w?|pyw?)\\.exe$', re.IGNORECASE)", "PYTHON_NAME = re.compile(r'^python\\.exe$')", 'pythonw.exe, py.exe and python3.15.exe are not Python'),
 (R, "PYTHON_NAME = re.compile(r'^(python[0-9.]*w?|pyw?)\\.exe$', re.IGNORECASE)", "PYTHON_NAME = re.compile(r'^(python.*|pyw?)\\.exe$', re.IGNORECASE)", 'a program whose name only begins with python is Python'),
 (R, "        check_no_other_python(read_processes, 'before the old tree is renamed')\r\n", "", 'no process check before the old tree is renamed'),
 (R, "        check_no_other_python(read_processes, 'after the old tree was renamed')\r\n", "", 'no process check after the old tree is renamed'),
 (R, "            if (set_aside / SETTINGS_FILE).is_file():        # so that no launcher runs in the tree set aside", "            if False:", 'the settings file of the tree set aside keeps its name'),
 (R, "    held_back = {name for name in (SETTINGS_FILE, ORPHAN_MARKER) if name in listed}", "    held_back = {name for name in (SETTINGS_FILE,) if name in listed}", 'an orphan marker is restored live'),
 (R, "    held_back = {name for name in (SETTINGS_FILE, ORPHAN_MARKER) if name in listed}", "    held_back = {name for name in (ORPHAN_MARKER,) if name in listed}", 'the settings file is not written last'),
 (R, "    if files != wanted or not all(", "    if False and not all(", 'a fresh tree that is not the payload passes'),
 (R, "    (tree_root / PROGRESS_FILE).unlink()", "    pass", 'the progress file is left in a restored tree'),
 (R, "    if orphan_bytes is not None:\r\n        _write_whole(", "    if False:\r\n        _write_whole(", 'the orphan marker\'s bytes are not kept as evidence'),
 (R, "    if any(started_at() <= written for _where, written in markers):", "    if False:", 'the orphan exception without a restart of the PC'),
 (R, "    check_no_other_python(read_processes, 'the fresh check that the orphan marker asks for')\r\n", "", 'the orphan exception without its fresh process check'),
 (R, "            != ORPHAN_ACKNOWLEDGEMENT:\r\n        raise RestoreRefused('the sentence was not typed. Nothing was touched.')", "            != ORPHAN_ACKNOWLEDGEMENT and False:\r\n        raise RestoreRefused('the sentence was not typed. Nothing was touched.')", 'the orphan exception without the typed sentence'),
 (R, "        if manifest['orphan_marker_time'] is not None:\r\n            markers.append(", "        if False:\r\n            markers.append(", 'an orphan marker inside the backup asks nothing'),
 (R, "        if os.path.lexists(tree_root / ORPHAN_MARKER):\r\n            markers.append(", "        if False:\r\n            markers.append(", 'an orphan marker in the old tree asks nothing'),
 (R, "'RESTORED AND READY TO RUN.' if ready else", "'RESTORED AND READY TO RUN.' if True else", '"ready" is said of an environment that did not start'),
 (R, "        if files.pop(SNAPSHOT_MANIFEST_NAME, None) is None or files != listed:", "        if False:", 'the reconciliation passes a tree that is not the backup'),
 (R, "        os.rename(lying, tree_root / f'{name}_{SNAPSHOT_MANIFEST_NAME}')", "        pass", 'the reconciliation leaves the manifest at the root'),
 (R, "'reconciliation_recorded_at': stamp", "'restored_at': stamp", 'the reconciliation\'s time is labelled as a restore\'s'),
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
