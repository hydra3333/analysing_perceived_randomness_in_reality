"""Write the runner's task file TASK_T025 and its two companion files (the step 2 rehearsal on Windows).

What this file is for
    TASK_T025 has the local runner rehearse the owner's install sheet for build step 2 (package
    STEP2_Research_Engine_v1r2, PASS in EX_290): parts 1 to 4 in a task clone, then parts 5 to 7 in a scratch tree
    under D:\\DELETE_ME (rulebook v0.7 section 2A). The task's commands repeat a few long paths many times, so the
    task file is written from one template with each path defined once. This script writes the three files into
    CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/ with CRLF line endings, as the other task files have, and prints their
    SHA-256.

Which part of the specification it carries out
    None; it prepares a rehearsal of the install of specification v0.6 sections 3 to 11.

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_task_t025.py <repository clone>
"""
import hashlib
import sys
from pathlib import Path

TASK = 'T025'
PACKAGE = 'STEP2_Research_Engine_v1r2'
PACKAGE_ZIP = f'exchange/CLAUDE_WEB_TOOLS/step2/package_v1r2/{PACKAGE}.zip'
MAIN = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
SCRATCH = rf'D:\DELETE_ME\a_p_r_i_r\{TASK}'
# Each name of the template and the path it stands for; F names are the same path written with / for the shell.
PATHS = {
    'MAIN': MAIN,
    'PY': MAIN + r'\.venv\Scripts\python.exe',
    'CC': MAIN + r'\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py',
    'CLONE': MAIN + rf'\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\{TASK}\r',
    'PKG': MAIN + rf'\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\{TASK}\p\{PACKAGE}',
    'EV': MAIN + rf'\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\{TASK}\e',
    'OLDPARENT': MAIN + r'\results\real\development',
    'TASKDIR': MAIN + rf'\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\{TASK}',
    'SCRATCH': SCRATCH,
    'TREE': SCRATCH + r'\tree',
    'SEV': SCRATCH + r'\evidence',
    'SPY': SCRATCH + r'\tree\.venv\Scripts\python.exe',
    'STOOLS': SCRATCH + rf'\tree\exchange\EX_288_Claude\{PACKAGE}\tools',
}
SETTINGS = ('; The settings file of the scratch tree of TASK_T025 (rulebook v0.7 section 2A). It is copied to ENVIRONMENT.ini\n'
            '; inside that scratch tree only. It names no real tree of the owner.\n'
            '[environment]\n'
            'role = DEV\n'
            f'tree_root = {SCRATCH}\\tree\n'
            f'venv_dir = {SCRATCH}\\tree\\.venv\n')
PLAN = ('# TASK_T025 overlay plan: STEP2_Research_Engine_v1r2 (EX_288; PASS in EX_290) onto main.\n'
        '# Read by tools/cc_clone.py overlay --plan. 2 REPLACE, 0 REMOVE; the other 33 overlay files are new.\n'
        '\n'
        'REPLACE .gitignore\n'
        'REPLACE tests/test_mhupa_master_versions.py\n')


def main(repository: Path) -> int:
    """Fill the template, write the three files with CRLF line endings, print each file's SHA-256; return 0."""
    here = Path(__file__).resolve().parent
    inbox = repository / 'CLAUDE_CODE_WORKING_FOLDER_TREE' / 'inbox'
    text = (here / 'TASK_T025_template.md').read_text(encoding='ascii')
    names = dict(PATHS)
    names.update({name + 'F': path.replace('\\', '/') for name, path in PATHS.items()})
    names['ZIP'] = PACKAGE_ZIP
    names['ZIPSHA'] = hashlib.sha256((repository / PACKAGE_ZIP).read_bytes()).hexdigest()
    for name in sorted(names, key=len, reverse=True):
        text = text.replace('{{' + name + '}}', names[name])
    assert '{{' not in text and '}}' not in text, 'a name of the template was not filled'
    for file_name, content in ((f'TASK_{TASK}.md', text), (f'TASK_{TASK}_overlay_plan.txt', PLAN),
                               (f'TASK_{TASK}_ENVIRONMENT.ini', SETTINGS)):
        data = content.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii')
        (inbox / file_name).write_bytes(data)
        print(hashlib.sha256(data).hexdigest(), file_name)
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
