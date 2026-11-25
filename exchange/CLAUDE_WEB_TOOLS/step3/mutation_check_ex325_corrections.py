"""Workspace helper (not project code): the planted faults for the two residual corrections EX_325 asked for in slice
B (B-B02, B-C03). One fault at a time is planted in a disposable copy of the dev tree that holds the overlay; the
slice's two test modules must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_snapshot', 'test_trees_restore']
R, J = 'deploy/restore_tool.py', 'src/research/research_job.py'
FAULTS = [
 (R, "    if (role not in BACKED_UP_ROLES\r\n            or not all(", "    if (False\r\n            or not all(", 'B-B02: a role that is neither QA nor PROD passes'),
 (R, "for text in (named, root, environment, backup_root))", "for text in (named, root, environment))", 'B-B02: the backup root need not be a full path'),
 (R, "for text in (named, root, environment, backup_root))", "for text in (named, root, backup_root))", 'B-B02: the environment need not be a full path'),
 (R, "    if not text or not Path(text).is_absolute():\r\n        return False", "    if not text:\r\n        return False", 'B-B02: a path that is not a full path is taken for one'),
 (R, "    return os.path.normcase(os.path.realpath(text)) == os.path.normcase(str(Path(text)))", "    return True", 'B-B02: a path that is not its own real path passes'),
 (R, "            or not _lies_inside(environment, root) or _same_place(backup_root, root)", "            or _same_place(backup_root, root)", 'B-B02: the environment may lie outside the tree'),
 (J, "    mark_due(settings)\r\n    reached['writing'] = True\r\n", "    mark_due(settings)\r\n", 'B-C03: the job never records that it reached its first write'),
 (J, "    mark_due(settings)\r\n    reached['writing'] = True\r\n", "    reached['writing'] = True\r\n    mark_due(settings)\r\n", 'B-C03: a note that could not be written is taken for a write'),
 (J, "        if not reached['writing']:                           # refused at a guard or a read-only check", "        if not (settings is not None and (settings.tree_root / 'records' / 'SNAPSHOT_DUE').exists()):", 'B-C03: the handler goes by the note lying in the tree'),
 (J, "        elif settings.backup_root is None:                   # DEV keeps no note and makes no backup", "        elif False:", 'B-C03: DEV is told a note was written and a backup tried'),
 (J, "            # the backup that is owed is tried, and if it cannot be made the standing warning is said.\r\n            backup_for_a_job(settings, 'end', now, say)\r\n", "            # the backup that is owed is tried, and if it cannot be made the standing warning is said.\r\n", 'B-C03: the backup owed by a refused job is not tried'),
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
