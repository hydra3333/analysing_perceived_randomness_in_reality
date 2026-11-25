"""Workspace helper (not project code): the planted faults for the two residual corrections EX_331 asked for in slice C
(C-B01 (a) and (b), both in deploy/reinstall_infra.py). One fault at a time is planted in a disposable copy of the dev
tree that holds the overlay; tests/test_trees_reinstall.py must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
R = 'deploy/reinstall_infra.py'
FAULTS = [
 ("                check_the_tree_is_as_it_was_read(settings, current, unfinished, as_they_lay)\r\n", "",
  'C-B01 (a): the tree is not compared with what the plan was worked out from'),
 ("    if common.read_barrier(root) != unfinished:", "    if False:",
  'C-B01 (a): a barrier that appeared before the first hold is not seen'),
 ("    if installed_files.read_list(root) != current:", "    if False:",
  'C-B01 (a): a list changed before the first hold is not said to be one'),
 ("             if unfinished is not None else installed_files.differences(root, current))",
  "             if unfinished is not None else [])",
  'C-B01 (a): software changed under a new plan is not seen'),
 ("    moved = (sorted(path for path, digest in as_they_lay.items() if _sha256(root / path) != digest)",
  "    moved = (sorted(path for path, digest in {}.items() if _sha256(root / path) != digest)",
  'C-B01 (a): files changed under a replacing plan are not seen'),
 ("MAY_BE_ABSENT = ('results/research',)", "MAY_BE_ABSENT = ()",
  'C-B01 (b): a tree with no research folder is refused'),
 ("        if folder in MAY_BE_ABSENT and not os.path.lexists(root / folder):",
  "        if not os.path.lexists(root / folder):",
  'C-B01 (b): a folder that must be there is read as empty when it is absent'),
]
survived = 0
for old, new, what in FAULTS:
    path = MUT / R; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', 'test_trees_reinstall'], cwd=MUT, timeout=600,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught, how = run.returncode != 0, 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what, flush=True)
print(f'{len(FAULTS)} faults planted; {survived} survived')
