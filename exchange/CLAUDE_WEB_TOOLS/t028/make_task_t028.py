"""Write the runner's task file TASK_T028 (the probe before build step 3 is coded).

What this file is for
    TASK_T028 runs the probe CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028_probe.py in the scratch folder on the
    owner's D: drive. This script fills the template's path names, computes the probe's SHA-256 (after CRLF is
    made LF) from the repository clone, writes the task file into CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/ with CRLF
    line endings, and prints its SHA-256.

Which part of the specification it carries out
    None; it prepares a measurement for build step 3 (specification v0.6 section 17.4; build plan v0.1 section 4).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_task_t028.py <repository clone>
"""
import hashlib
import sys
from pathlib import Path

# The owner's main repository, as every task file names it.
MAIN = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
# This task's own new scratch folder (rulebook v0.7 section 2A).
SCRATCH = r'D:\DELETE_ME\a_p_r_i_r\T028'
# The probe, in the repository, and the name of its copy in the scratch folder.
PROBE_IN_REPOSITORY = 'CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028_probe.py'
PATHS = {
    'MAIN': MAIN,
    'PY': MAIN + r'\.venv\Scripts\python.exe',
    'CC': MAIN + r'\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py',
    'PROBE': MAIN + '\\' + PROBE_IN_REPOSITORY.replace('/', '\\'),
    'SCRATCH': SCRATCH,
    'SPROBE': SCRATCH + r'\TASK_T028_probe.py',
    'OLDTREE': r'D:\DELETE_ME\a_p_r_i_r\T025\tree',
    'ZIPOUT': SCRATCH + r'\zip_part_output.txt',
}


def main(repository: Path) -> int:
    """Fill the template and write the task file; return 0. Refuses (assert) if a name of the template is left
    unfilled, if a path in a command ends in a backslash before its closing quote, or if the text is not ASCII."""
    here = Path(__file__).resolve().parent
    text = (here / 'TASK_T028_template.md').read_text(encoding='ascii')
    names = dict(PATHS)
    names.update({name + 'F': path.replace('\\', '/') for name, path in PATHS.items()})
    names['PROBESHA'] = hashlib.sha256((repository / PROBE_IN_REPOSITORY).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    for name in sorted(names, key=len, reverse=True):
        text = text.replace('{{' + name + '}}', names[name])
    assert '{{' not in text and '}}' not in text, 'a name of the template was not filled'
    assert '\\"' not in text, 'a quoted path ends in a backslash: the shell would take the quote as part of it'
    data = text.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii')
    (repository / 'CLAUDE_CODE_WORKING_FOLDER_TREE' / 'inbox' / 'TASK_T028.md').write_bytes(data)
    print('probe SHA-256 (LF)', names['PROBESHA'])
    print(hashlib.sha256(data).hexdigest(), 'TASK_T028.md')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
