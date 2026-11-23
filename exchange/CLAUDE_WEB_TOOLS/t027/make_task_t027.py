"""Write the runner's task file TASK_T027 (the comparison once more, with the corrected tool of package v1r3).

What this file is for
    TASK_T026's comparison stopped on a fault of the comparison tool; package STEP2_Research_Engine_v1r3 corrects
    the tool (PASS in EX_294). TASK_T027 runs only that corrected tool on the scratch tree TASK_T026 left. This
    script fills the template's path names, computes the tool's SHA-256 (after CRLF is made LF) from the reviewed
    package extracted in the repository, checks that the numbers the task expects are those the corrected tool
    printed on the made-up records of the cloud's check, writes the task file into
    CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/ with CRLF line endings, and prints its SHA-256.

Which part of the specification it carries out
    None; it prepares a rehearsal of specification v0.6 section 17.3 (the transition check, made early).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_task_t027.py <repository clone>
"""
import hashlib
import sys
from pathlib import Path

PACKAGE = 'STEP2_Research_Engine_v1r3'
MAIN = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
# The scratch folder is TASK_T025's: this task continues in it.
SCRATCH = r'D:\DELETE_ME\a_p_r_i_r\T025'
# The corrected tool as the reviewer passed it (EX_294), in the package extracted in the repository.
TOOL_IN_REPOSITORY = f'exchange/EX_293_Claude/{PACKAGE}/tools/compare_fill_with_old_records.py'
# The cloud's check of the corrected tool, whose lines the task's step 7 expects again on the owner's PC.
CLOUD_CHECK = 'exchange/CLAUDE_WEB_TOOLS/step2/evidence_v1r3/COMPARE_TOOL_CHECK.txt'
PATHS = {
    'MAIN': MAIN,
    'PY': MAIN + r'\.venv\Scripts\python.exe',
    'CC': MAIN + r'\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py',
    'TOOL': MAIN + '\\' + TOOL_IN_REPOSITORY.replace('/', '\\'),
    'SCRATCH': SCRATCH,
    'TREE': SCRATCH + r'\tree',
    'SEV': SCRATCH + r'\evidence',
    'SPY': SCRATCH + r'\tree\.venv\Scripts\python.exe',
    'STOOL': SCRATCH + r'\evidence\compare_fill_with_old_records_v1r3.py',
}


def main(repository: Path) -> int:
    """Fill the template, check the expected lines against the cloud's check, write the task file; return 0."""
    here = Path(__file__).resolve().parent
    text = (here / 'TASK_T027_template.md').read_text(encoding='ascii')
    names = dict(PATHS)
    names.update({name + 'F': path.replace('\\', '/') for name, path in PATHS.items()})
    names['TOOLSHA'] = hashlib.sha256((repository / TOOL_IN_REPOSITORY).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    for name in sorted(names, key=len, reverse=True):
        text = text.replace('{{' + name + '}}', names[name])
    assert '{{' not in text and '}}' not in text, 'a name of the template was not filled'
    cloud = (repository / CLOUD_CHECK).read_text(encoding='ascii')
    expected = [line[2:].replace('**', '').strip('`') for line in text.split('\n') if line.startswith('- ') and ('part 1' in line or 'tracked rank' in line)]
    assert len(expected) == 4 and all(line in cloud for line in expected), 'an expected whole line is not in the cloud check'
    for fragment in ("equal in the new lists: 14478; INSUFFICIENT_HISTORY records before the variant's first target, where the new list has no line: 2802; DIFFERENT: 0;",
                     "equal in the new lists: 5958; INSUFFICIENT_HISTORY records before the variant's first target, where the new list has no line: 2802; DIFFERENT: 0;",
                     '(never forecast by the old development runs): 640',
                     'RESULT: PASS - COMPLETE - both games; all 34800 old score records equal the new score lists; all 20436 old development forecasts in the run folders were found in the new lists',
                     "the 5604 old INSUFFICIENT_HISTORY records all lie before their variants' first targets"):
        assert fragment in text and fragment in cloud, f'not in both the task and the cloud check: {fragment}'
    data = text.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii')
    (repository / 'CLAUDE_CODE_WORKING_FOLDER_TREE' / 'inbox' / 'TASK_T027.md').write_bytes(data)
    print('the expected lines of step 7 are lines of the cloud check; tool SHA-256 (LF)', names['TOOLSHA'])
    print(hashlib.sha256(data).hexdigest(), 'TASK_T027.md')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
