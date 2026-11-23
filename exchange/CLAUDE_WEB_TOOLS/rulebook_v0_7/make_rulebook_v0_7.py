"""Make the CANDIDATE of the runner's rulebook v0.7 from the installed v0.6, by counted edits.

What this file is for
    The owner asked (decision log entries 180 to 185) for an edition of the Claude Code runner's rulebook that
    lets the runner rehearse the new system's commands in one scratch folder on his D: drive. This script reads
    the installed rulebook (CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md, v0.6), applies the edits listed below, each
    of which must match exactly once, and writes the candidate and the exact diff beside itself. The candidate
    has no force: the rulebook changes only after the reviewer's review and the owner's ratification (RAT-44).

Which part of the specification it carries out
    None of the system specification; H-1 v9 section 8.6 (the narrow rulebook amendment before a runner rehearsal).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_rulebook_v0_7.py <repository clone>
"""
import difflib
import hashlib
import sys
from pathlib import Path

INSTALLED = 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'
# The SHA-256 the installed v0.6 must have, so that the edits are made to the text they were written for.
INSTALLED_SHA256_START = 'f92f17f60db63990'
CANDIDATE_NAME = 'CLAUDE_v0_7_CANDIDATE.md'
DIFF_NAME = 'CLAUDE_v0_6_TO_v0_7_CANDIDATE.diff'

SECTION_2A = r'''## 2A. The scratch folder on D: (rehearsals only; owner, decision log entries 180 to 182)

The project owner has given one folder of his D: drive to rehearsals: **`D:\DELETE_ME\`**. Nothing in it is kept. This section is the only place where rules 3, 4, 5, 7, 9 and 10 and sections 3, 5 and 7 give way, and only as far as it says. Rules 1, 2, 6, 8, 11 and 12 are not touched by it.

1. **Only when a task file says so.** A task file that uses this section says "section 2A", names the folder it works in (usually `D:\DELETE_ME\a_p_r_i_r\<task id>\`) and gives every command to run. You run those commands, exactly as written, and no others. Where a command asks a question (for example to type `YES`, `WITHDRAW` or a role), type what the task file gives for it.
2. **What you may do there.** Under `D:\DELETE_ME\` you may create, read, change and delete any file or folder a task needs: batch files, code, data, reports, logs, whole trees. Before a task's first write there, make the check the task file gives that `D:\DELETE_ME` is an ordinary folder on drive D: (not a link, a junction or a substituted drive). If it is not, that is a STOP. Every path you use there is a full path that begins `D:\DELETE_ME\`. A step that would write anywhere else on D:, or anywhere else outside `CLAUDE_CODE_WORKING_FOLDER_TREE\`, is a STOP.
3. **Real results may be used there** (owner, decision log entry 184). A task may copy this repository's accepted results and records (from its `source_data` and `results` folders, or from a task clone) into a scratch tree, and you may read and run the system on anything under `D:\DELETE_ME\`, real draws included. Copying is by reading only: nothing is ever written to this repository's `source_data`, `results` or `transitory_data`, nor to a task clone's. **What a scratch run computes is a rehearsal, not a result of the project.**
4. **Nothing leaves the scratch folder** (owner, decision log entry 185). Everything in it and everything created there (software, data, results, reports, logs, environments) stays under `D:\DELETE_ME\` until it is deleted there. Nothing of it is ever copied, moved or sent anywhere else: not into this repository or a task clone, not to another drive or folder, not over the network. The one thing that leaves is your report in `outbox\`, which records what the commands printed (item 8). A step that would copy or move anything out of `D:\DELETE_ME\` is a STOP.
5. **Which commands, and only against scratch trees.** The new system's commands that rule 7 names (`Init_Tree`, `Install`, `Reinstall_Infra`, `Check_Tree`, `Verify_Tree`, `Make_Installable`, `Run_Research`, `Withdraw_Variant`, `Run_Snapshot`, `Restore` and, once they exist, the tools of build step 4), each only when the task file names it and only against a tree whose root lies under `D:\DELETE_ME\`. A settings file, a command line or a step that names the real DEV tree as a target (rather than as a place to copy from by reading), the real QA or PROD tree, or any of their backup folders, is a STOP (rule 11 is unchanged).
6. **Never, even there.** The results updater in any version, any scraper or results-check program, the old coordinator and its launchers, and anything else that contacts a lottery website (rules 1 and 2). A push. Anything that changes the PC's date, time or time zone (rule 12). Ending another process. Clearing or bypassing an orphan marker of the real tree (rule 6).
7. **A scratch tree's Python environment.** Each tree needs its own `.venv` inside it. You may build it with that tree's own copies of `create_venv.bat` and then `install_upgrade_dependencies_into_venv.bat`, started by their full paths under `D:\DELETE_ME\` (each works on the folder it lies in). The package downloads those two scripts make are the one network use this section adds. **Never run this repository's own copies of those scripts, and never change the main `.venv`:** it is the environment of the owner's real runs. Inside a scratch tree use that tree's own Python by its full path; everywhere else section 5 is unchanged. A scratch environment holds whatever package versions are current on the day it is built: nothing computed in it says anything about the owner's environments.
8. **The report.** As for every task: each command, its exit code and its output (section 7: what the commands print, which is counts, timings and check lines, never the contents of a data file). At the end, also list every folder the task created under `D:\DELETE_ME\` and say whether it was removed. If the task file says to clean up, delete only what this task created.
9. **A STOP is still a STOP** (rule 10). On a STOP in a scratch folder, leave the folder exactly as it is, so that the web chat can ask for what it holds; do not clean up unless the task file says to clean up after a STOP.

'''

# (old text, new text, what it is)
EDITS = (
    ('**Version:** v0.6, 22 November 2026, ratified by the project owner the same day (RAT-42) after the reviewer\'s PASS (EX_274) (v0.6:',
     '**Version:** v0.7 CANDIDATE, 23 November 2026. **NOT YET REVIEWED OR RATIFIED: until it is, v0.6 is the rulebook.** (v0.7: new section 2A, the scratch folder on the owner\'s D: drive for rehearsals of the new system\'s commands, real results included, nothing ever leaving it (owner, decision log entries 180 to 185); rules 3, 4, 5, 7, 9 and 10 and sections 3, 5 and 7 point to it and are otherwise unchanged; rule 10 gains the one exception for the test suite\'s known failures.) Before it: v0.6, 22 November 2026, ratified by the project owner the same day (RAT-42) after the reviewer\'s PASS (EX_274) (v0.6:',
     'the version line'),
    ('Never display, paste, quote or compute with the outcome of any draw, of either game, whatever its number.',
     'Never display, paste, quote or compute with the outcome of any draw, of either game, whatever its number, except by running the project\'s own programs in the scratch folder as section 2A says.',
     'rule 4: the scratch folder'),
    ('you never open those folders yourself, and you never copy a data value into a report.',
     'you never open those folders yourself, and you never copy a data value into a report. (Section 2A: a task may copy them into the scratch folder by reading; under `D:\\DELETE_ME\\` you may read anything.)',
     'rule 5: the scratch folder'),
    ('- Never put in a report: any outcome of a draw (section 2, rule 4), the contents of any data file, personal details, or anything from outside this repository.',
     '- Never put in a report: any outcome of a draw (section 2, rule 4), the contents of any data file, personal details, or anything from outside this repository (what the commands of a section 2A task print excepted).',
     'section 7'),
    ('The only network use allowed is `git clone` from GitHub done by `tools\\cc_clone.py`.',
     'The only network use allowed is `git clone` from GitHub done by `tools\\cc_clone.py`, and, under section 2A only, the package downloads made by a scratch tree\'s own two environment scripts.',
     'rule 3: the one added network use'),
    ('Also never run `create_venv.bat`. Never run `pip` or change the venv.',
     'Also never run `create_venv.bat`. Never run `pip` or change the venv. (Section 2A: a scratch tree\'s own environment only, never the main one.)',
     'rule 7: the environment scripts'),
    ('(Programs named here before they are installed are simply never run once they exist. A later reviewed edition of this rulebook may allow named ones for a rehearsal in a task clone or a scratch folder; until an edition says so, none.)',
     '(Programs named here before they are installed are simply never run once they exist. Section 2A of this edition allows named ones, against trees in the scratch folder only and only when a task file names them; everywhere else, none.)',
     'rule 7: the allowance'),
    ('No research job, historical walk-forward rerun, withdrawal, install into a tree, copy between trees, backup or restore.',
     'No research job, historical walk-forward rerun, withdrawal, install into a tree, copy between trees, backup or restore. (Section 2A allows these for scratch trees under `D:\\DELETE_ME\\`; never for the real DEV, QA or PROD tree.)',
     'rule 9'),
    ('Go straight to the report (and the clean-up step, if the task says so).',
     'Go straight to the report (and the clean-up step, if the task says so). **One exception, and only where a task file says so and names the tests:** when a task runs the project\'s test suite and then its comparison tool, the word `FAILED` on a module\'s line and the comparison\'s lines `FAILS IN BOTH RUNS` are not a STOP for the tests the task file lists as failing before the task. Any other failure, any `CHANGED` or `DISAPPEARED` line, or a failing test the task file does not list, is a STOP.',
     'rule 10: the suite\'s known failures'),
    ('## 3. Where you may write\n', SECTION_2A + '## 3. Where you may write\n', 'the new section 2A'),
    ('- Nothing outside this repository is yours to write, and the QA and PROD trees and their backup folders are not even yours to read (section 2, rule 11).',
     '- Nothing outside this repository is yours to write, except the scratch folder `D:\\DELETE_ME\\` as section 2A says; and the QA and PROD trees and their backup folders are not even yours to read (section 2, rule 11).',
     'section 3'),
    ('Do not activate the venv, and do not use any other Python. Do not create virtual environments.',
     'Do not activate the venv, and do not use any other Python. Do not create virtual environments. (Section 2A: inside a scratch tree, that tree\'s own environment and Python.)',
     'section 5'),
)


def main(repository: Path) -> int:
    """Write the candidate and the diff beside this file; print what was done; return 0."""
    here = Path(__file__).resolve().parent
    text = (repository / INSTALLED).read_text(encoding='ascii')
    digest = hashlib.sha256((repository / INSTALLED).read_bytes()).hexdigest()
    assert digest.startswith(INSTALLED_SHA256_START), f'the installed rulebook is not the v0.6 these edits were written for: {digest}'
    new = text
    for old, replacement, what in EDITS:
        assert new.count(old) == 1, f'{what}: the old text is found {new.count(old)} times, not once'
        new = new.replace(old, replacement)
    assert new.isascii()
    (here / CANDIDATE_NAME).write_text(new, encoding='ascii', newline='\n')
    diff = ''.join(difflib.unified_diff(text.splitlines(keepends=True), new.splitlines(keepends=True),
                                        'CLAUDE.md (v0.6, installed)', 'CLAUDE.md (v0.7 CANDIDATE)', n=0))
    (here / DIFF_NAME).write_text(diff, encoding='ascii', newline='\n')
    print(f'{len(EDITS)} edits, each matched once; v0.6 {digest[:12]}... -> candidate '
          f'{hashlib.sha256(new.encode("ascii")).hexdigest()}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
