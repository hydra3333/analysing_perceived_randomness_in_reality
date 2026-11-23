"""Write the runner's task file TASK_T026 (the second part of the step 2 rehearsal on Windows).

What this file is for
    TASK_T025 stopped at its step 20 and left its scratch tree in place; the owner then built that tree's Python
    environment himself. TASK_T026 runs the steps of TASK_T025 that did not run (its steps 22 to 29), on that tree.
    This script fills the template's path names, writes the task file into CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/
    with CRLF line endings, and checks that every command line of steps 4 to 10 is, character for character, a
    command line of TASK_T025 r1 as the reviewer passed it (EX_292). It prints the task file's SHA-256.

Which part of the specification it carries out
    None; it prepares a rehearsal of the install of specification v0.6 sections 3 to 11.

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_task_t026.py <repository clone>
"""
import hashlib
import re
import sys
from pathlib import Path

PACKAGE = 'STEP2_Research_Engine_v1r2'
MAIN = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
# The scratch folder is TASK_T025's: this task continues in it.
SCRATCH = r'D:\DELETE_ME\a_p_r_i_r\T025'
PATHS = {
    'MAIN': MAIN,
    'PY': MAIN + r'\.venv\Scripts\python.exe',
    'CC': MAIN + r'\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py',
    'OLDPARENT': MAIN + r'\results\real\development',
    'SCRATCH': SCRATCH,
    'TREE': SCRATCH + r'\tree',
    'SEV': SCRATCH + r'\evidence',
    'SPY': SCRATCH + r'\tree\.venv\Scripts\python.exe',
    'STOOLS': SCRATCH + rf'\tree\exchange\EX_288_Claude\{PACKAGE}\tools',
}
# The SHA-256 of TASK_T025 r1 as the reviewer passed it (EX_292).
PASSED_TASK_SHA256 = 'c9482a9a5c87edf57834d5d1118309dbab44aea553baae3ba3e1018dc5215fb5'
FIRST_COPIED_STEP, LAST_COPIED_STEP = 4, 10


def command_lines(text: str, first_step: int, last_step: int) -> list:
    """The command lines (the lines inside ``` blocks) of the steps first_step to last_step of a task file's text."""
    start = text.index(f'**{first_step}. ')
    end = text.index(f'**{last_step + 1}. ')
    return [line for block in re.findall(r'```\n(.*?)```', text[start:end], re.S) for line in block.split('\n') if line]


def main(repository: Path) -> int:
    """Fill the template, check the copied steps against TASK_T025 r1, write the task file, print its hash; return 0."""
    here = Path(__file__).resolve().parent
    inbox = repository / 'CLAUDE_CODE_WORKING_FOLDER_TREE' / 'inbox'
    text = (here / 'TASK_T026_template.md').read_text(encoding='ascii')
    names = dict(PATHS)
    names.update({name + 'F': path.replace('\\', '/') for name, path in PATHS.items()})
    for name in sorted(names, key=len, reverse=True):
        text = text.replace('{{' + name + '}}', names[name])
    assert '{{' not in text and '}}' not in text, 'a name of the template was not filled'
    passed = (inbox / 'TASK_T025.md').read_bytes()
    assert hashlib.sha256(passed).hexdigest() == PASSED_TASK_SHA256, 'TASK_T025.md is not the text the reviewer passed'
    passed_lines = command_lines(passed.decode('ascii').replace('\r\n', '\n'), 22, 28)
    copied_lines = command_lines(text, FIRST_COPIED_STEP, LAST_COPIED_STEP)
    assert copied_lines == passed_lines, 'a command of steps 4 to 10 differs from TASK_T025 r1 steps 22 to 28'
    data = text.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii')
    (inbox / 'TASK_T026.md').write_bytes(data)
    print(f'{len(copied_lines)} command lines of steps {FIRST_COPIED_STEP} to {LAST_COPIED_STEP} equal TASK_T025 r1 steps 22 to 28')
    print(hashlib.sha256(data).hexdigest(), 'TASK_T026.md')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
