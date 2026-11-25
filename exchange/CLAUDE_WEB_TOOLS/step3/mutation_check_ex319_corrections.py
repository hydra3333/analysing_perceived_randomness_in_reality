"""Workspace helper (not project code): the planted faults for the corrections EX_319 asked for (A-B01, A-B02,
A-C01, A-C02, A-C03). One fault at a time is planted in a disposable copy of the dev tree that holds the slice; the
slice's test modules must fail. A fault no test catches is printed as SURVIVED."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_launch_guard', 'test_trees_check_tree', 'test_trees_readiness']
E, G, W, R = 'src/research/environment_marker.py', 'src/research/launch_guard.py', 'src/research/withdraw.py', 'src/research/process_rule.py'
M, C, I = 'deploy/make_installable.py', 'deploy/check_tree.py', 'deploy/install_import_check.py'
FAULTS = [
 (E, "        lines.append(f'base python\\t{version}\\t{program}\\t{program_digest}\\n')", "        lines.append(f'base python\\t{version}\\t{program}\\n')", 'A-B01: the base program enters the digest by its path and version only'),
 (E, "        lines.append(f'base python\\t{version}\\t{program}\\t{program_digest}\\n')", "        lines.append(f'base python\\t{program}\\t{program_digest}\\n')", 'A-B01: the base Python\'s version is left out of the digest'),
 (E, "        program_digest = hashlib.sha256(Path(program).read_bytes()).hexdigest()", "        program_digest = hashlib.sha256(Path(program).read_bytes()).hexdigest() if Path(program).is_file() else ''", 'A-B01: a base program that cannot be read is passed over'),
 (E, "os.walk(venv_dir / folder, onerror=_stop_at_a_folder_that_cannot_be_read)", "os.walk(venv_dir / folder)", 'A-B01: a folder that cannot be listed is left out of the digest'),
 (E, "    if missing:\r\n        raise EnvironmentRefused(", "    if False:\r\n        raise EnvironmentRefused(", 'A-B01: a digest is given for an environment that lacks a part of the inventory'),
 (E, "            parts_found.add(PROGRAMS_FOLDER)", "            pass", 'A-B01: an environment with Scripts is said to lack it'),
 (E, ".hexdigest(), len(paths) + 1", ".hexdigest(), len(paths)", 'A-B01: the count leaves out the base program that was hashed'),
 (G, "    check_no_unfinished_operation(settings.tree_root)\r\n    say(f'Reading", "    say(f'Reading", 'A-B02: the job under its lock does not look for an unfinished operation'),
 (G, "    if settings.role not in INSTALLED_ROLES:\r\n        return\r\n    try:", "    if True:\r\n        return\r\n    try:", 'A-B02: the software is never compared with its list'),
 (W, "            check_software_is_as_installed(settings)\r\n", "", 'A-B02: a withdrawal is written in a tree whose software differs from its list'),
 (W, "            check_no_unfinished_operation(tree_root)\r\n", "", 'A-B02: a withdrawal is written while an operation is unfinished'),
 (W, "            check_no_unfinished_operation(tree_root)\r\n            check_software_is_as_installed(settings)\r\n            for leftover in discard_unfinished_writes(tree_root):", "            for leftover in discard_unfinished_writes(tree_root):\r\n                pass\r\n            check_no_unfinished_operation(tree_root)\r\n            check_software_is_as_installed(settings)\r\n            for leftover in ():", 'A-B02: the withdrawal tidies the staging folder before it refuses'),
 (W, "        check_no_orphan_marker(tree_root)\r\n", "", 'A-B02: the withdrawal\'s own orphan-marker check is lost'),
 (M, "        check_no_unfinished_operation(tree_root)\r\n", "", 'A-B02: Make_Installable writes markers while an operation is unfinished'),
 (M, "        check_no_orphan_marker(tree_root)\r\n", "", 'A-B02: Make_Installable writes markers beside the orphan marker'),
 (R, "            if not after or not (after.isalnum() or after in NAME_CONTINUES):", "            if True:", 'A-C01: a folder whose name begins like the tree\'s is taken for the tree'),
 (R, "            if not after or not (after.isalnum() or after in NAME_CONTINUES):", "            if not after:", 'A-C01: the tree is named only where the text ends with its path'),
 (R, "NAME_CONTINUES = '_-.~'", "NAME_CONTINUES = ''", 'A-C01: T:\\a_p_r_i_r_backups is taken for T:\\a_p_r_i_r'),
 (R, "            at = text.find(wanted, at + 1)", "            at = -1", 'A-C01: only the first place the path stands in an argument is looked at'),
 (C, "Environment: verification marker present (", "Environment: verified (", 'A-C02: a marker that is present is called a verified environment'),
 (C, "Nothing was found by the checks this command makes. It starts nothing and does '", "Nothing is wrong. It starts nothing and does '", 'A-C02: the closing line says nothing is wrong'),
 (I, "node.value.id in names_of_path_module):", "node.value.id == PATH_MODULE):", 'A-C03: sys.path under another name of sys is not found'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', *MODULES], cwd=MUT, timeout=300,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught = run.returncode != 0
        how = 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what)
print(f'{len(FAULTS)} faults planted; {survived} survived')
