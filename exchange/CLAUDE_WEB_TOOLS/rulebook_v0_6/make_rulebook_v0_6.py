#!/usr/bin/env python3
"""Make the local runner rulebook v0.6 CANDIDATE from the installed v0.5 by counted edits (Claude, 22 November 2026).

Purpose: read CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md from Git at HEAD (asserted to be the installed v0.5 bytes),
apply the edits below (every old text must occur exactly once), and write the candidate beside this file.
The installed rulebook is NOT touched: the runner obeys only the installed file, and a new edition is installed only
after the reviewer's review and the owner's ratification.
Usage: python3 -I make_rulebook_v0_6.py REPO_ROOT
It refuses (an assertion) on a wrong source hash, an anchor not found exactly once, a non-ASCII byte or a CR.
"""
import hashlib, os, subprocess, sys

# ---- constants -------------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'
SRC_SHA = 'fa7a5fe229be832880cda4704ed9e7d27af2f4b9462464f7af262e540acd5200'       # rulebook v0.5 as installed (RAT-30)
OUT = 'CLAUDE_v0_6_CANDIDATE.md'
SECTION_2A_FIRST = '## 2A. TASK_T016 only: the MHUP-A install rehearsal (narrow allowance; added in v0.5)\n'
SECTION_3_FIRST = '## 3. Where you may write\n'
# The new system's owner commands (specification section 16), named before they exist.
NEW_COMMANDS = ('`Run_Research.bat`, `Rerun_Walk_Forward.bat`, `Check_Forecasts.bat`, `Withdraw_Variant.bat`, `Install.bat`, '
                '`Reinstall_Infra.bat`, `Correct_Shared_Code.bat`, `Init_Tree.bat`, `Check_Tree.bat`, `Verify_Tree.bat`, '
                '`Run_Snapshot.bat`, `Restore.bat`, `Replace_QA_Software_From_PROD.bat`, `Reseed_Research_Data_From_PROD.bat`, '
                '`Make_Installable.bat`, `Who_Uses.bat` and `Make_Successors.bat`')

EDITS = [
 ('version',
  '**Version:** v0.5, 11 November 2026, ratified by the project owner the same day',
  '**Version:** v0.6 CANDIDATE, 22 November 2026: written by the Claude web chat for the reviewer\'s review and the project '
  'owner\'s ratification; NOT installed and not in force until then (v0.6: brought up to date for the system the owner '
  'ratified on 22 November 2026: section 1 says that there are two systems and three folder trees; rule 4 now covers every '
  'draw; rule 7 names the new system\'s commands ahead of their installation; new rules 11 and 12; section 2A, the '
  'allowance for TASK_T016, ended with that task and is removed, with the pointers to it in rules 5, 7, 9 and 10 and in '
  'section 2\'s heading). Before it: v0.5, 11 November 2026, ratified by the project owner the same day'),
 ('section 1, why the rules',
  'It has strict safety and governance rules, because holdout data must never be seen and the project\'s code must change '
  'only through reviewed packages.',
  'It has strict safety and governance rules: results count only when they come from the project\'s reviewed programs run '
  'by the owner, and the project\'s code changes only through reviewed packages.\n\n'
  '**Two systems, three folder trees (from 22 November 2026).** The code under `src\\` today is the project\'s first system. '
  'A new system was ratified on 22 November 2026 (`doc\\Predictive_Randomness_System_Specification_v0_6.md` and '
  '`doc\\Predictive_Randomness_Deployment_Design_v0_12.md`) and is being built in steps. It has three separate folder '
  'trees: **DEV**, which is this repository on E:; and **QA** and **PROD**, which are folders outside this repository, on '
  'other drives, each with its own data, results, Python environment and backups. **You work in DEV only,** and in DEV '
  'only as sections 3 and 4 say. Rule 11 says what that means for QA and PROD.'),
 ('section 2 heading',
  '## 2. Hard prohibitions (binding; no task file can relax them; the only exception is section 2A, for TASK_T016 alone)',
  '## 2. Hard prohibitions (binding; no task file can relax them)'),
 ('rule 4',
  '4. Never display, paste, quote or compute with an outcome for Powerball draw 1577 or later, or Oz Lotto draw 1694 or later.',
  '4. Never display, paste, quote or compute with the outcome of any draw, of either game, whatever its number. (Until '
  'v0.6 this rule named only Powerball draw 1577 or later and Oz Lotto draw 1694 or later, the former holdout. The '
  'project now treats all draws the same, so the rule covers them all.)'),
 ('rule 5, the T016 pointer',
  ' (TASK_T016 only: section 2A says exactly which package tools may touch which files there.)', ''),
 ('rule 7, the closing note',
  '(Programs named here before they are installed are simply never run once they exist. TASK_T016 only: section 2A '
  'allows the package copies of `process_check.py` and `install_records.py`, and nothing else named here.)',
  '**Nor any command of the new system, by its `.bat` or by the Python program behind it, in any tree:** ' + NEW_COMMANDS +
  '. (Programs named here before they are installed are simply never run once they exist. A later reviewed edition of '
  'this rulebook may allow named ones for a rehearsal in a task clone or a scratch folder; until an edition says so, none.)'),
 ('rule 9',
  '9. No Windows lifecycle tests, destructive tests, real-data science, Mode H, FINAL, results-master update or dependency '
  'upgrade. (TASK_T016\'s install rehearsal in its own task clone is none of these: section 2A.)',
  '9. No Windows lifecycle tests, destructive tests, real-data science, Mode H, FINAL, results-master update or dependency '
  'upgrade. No research job, historical walk-forward rerun, withdrawal, install into a tree, copy between trees, backup '
  'or restore.'),
 ('rule 10, and the two new rules',
  'Go straight to the report (and the clean-up step, if the task says so). (TASK_T016 only: a step the task marks '
  '**EXPECTED REFUSAL** is judged as section 2A, A5 says.)\n',
  'Go straight to the report (and the clean-up step, if the task says so).\n'
  '11. **The QA and PROD trees are not yours.** Never read, list, write, create, rename or delete anything in the QA tree, '
  'the PROD tree or their backup folders, wherever the owner\'s settings place them (for example `D:\\TEST_BED`, '
  '`D:\\TEST_BED_backups`, `G:\\a_p_r_i_r` and `T:\\a_p_r_i_r_backups`). Never read or edit an `ENVIRONMENT.ini` file. Never '
  'create a tree. If a task step names one of these places, that is a STOP.\n'
  '12. Never change the PC\'s date, time or time zone, and never run anything that would.\n'),
 ('section 3, the other trees',
  '- Everything else in the repository is read-only to you:',
  '- Nothing outside this repository is yours to write, and the QA and PROD trees and their backup folders are not even '
  'yours to read (section 2, rule 11).\n'
  '- Everything else in the repository is read-only to you:'),
]

def sha(data):
    """SHA-256 of bytes as 64 lower-case hex characters."""
    return hashlib.sha256(data).hexdigest()

def main():
    assert len(sys.argv) == 2, 'usage: make_rulebook_v0_6.py REPO_ROOT'
    repo = os.path.abspath(sys.argv[1])
    src = subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + SRC], check=True, capture_output=True).stdout
    assert sha(src) == SRC_SHA, 'the rulebook at HEAD is not the installed v0.5'
    text = src.decode('ascii')
    # 1. Remove section 2A whole (it ended when T016's report was committed).
    a, b = text.index(SECTION_2A_FIRST), text.index(SECTION_3_FIRST)
    assert text.count(SECTION_2A_FIRST) == 1 and text.count(SECTION_3_FIRST) == 1 and a < b
    removed = text[a:b]
    text = text[:a] + text[b:]
    # 2. The counted edits.
    for label, old, new in EDITS:
        n = text.count(old)
        assert n == 1, '%s: expected one occurrence, found %d' % (label, n)
        text = text.replace(old, new)
    # No pointer to the removed section may be left, except in the version line (its history names v0.5's section 2A).
    body = '\n'.join(l for l in text.split('\n') if not l.startswith('**Version:**'))
    assert '2A' not in body and 'T016' not in body, 'a pointer to the removed section is left'
    data = text.encode('ascii')
    assert b'\r' not in data and data.endswith(b'\n')
    with open(os.path.join(HERE, OUT), 'wb') as f:
        f.write(data)
    print('%s  %d bytes  %s   (section 2A removed: %d lines; %d counted edits)' % (sha(data), len(data), OUT, removed.count('\n'), len(EDITS)))

if __name__ == '__main__':
    main()
