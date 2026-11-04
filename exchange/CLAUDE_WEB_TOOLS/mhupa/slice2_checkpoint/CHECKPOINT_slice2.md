# CHECKPOINT - MHUP-A slice 2 handback (EX_147), 5 November 2026

Written so that a continuing session (any model) can finish without loss. Everything lives in the scratchpad
S = /tmp/claude-0/-home-claude/05ef2f64-c028-5b8b-a9c5-1bd6b3c075ae/scratchpad and the repo clone
R = /home/claude/analysing_perceived_randomness_in_reality (origin/main at 110eb41, push access).

## State of the work (all code and tests FINISHED; evidence runs in progress or done)

- Development tree: S/DEV (built by `sh S/tools/build_dev_slice2.sh S/BASE S/DEV S/tools 2026-11-04`; the DATE 2026-11-04 is
  deliberate: slice 1's reviewed E_1 r3 effective_date). S/dev_clone = full clone with S/DEV's src/, tests/, archive/, *.bat,
  .gitignore overlaid and src/results_master_v0_1.py deleted (the suite and mutation runs use it). DEV and dev_clone src/tests
  are identical (verified with diff -rq).
- Final evidence runs were started as one detached chain on the FINAL tree:
    S/suite_slice2_py313.log   -> DONE: "SUITE PASS: all 561 tests ran and passed"
    S/suite_slice2_py315.log   -> DONE: "SUITE PASS: all 561 tests ran and passed"
    S/mutations_slice2_py313.txt -> IN PROGRESS (85 mutants; ~75 min total; check with
        grep -c "^CAUGHT\|^EQUIVALENT\|^SURVIVED" S/mutations_slice2_py313.txt ; finished when the last line reads
        "N of 85 mutants caught; M equivalent ...; 0 survived"). Earlier partial runs are S/mutations_slice2_py313_run1_partial.txt
        and S/mutations_slice2_py313_run2_preview.txt (preview: 4 survivors, each since given a test; expect 0 survived now,
        with 9 equivalents: mutants 1, 10, 29, 30, 52(SCORE_COMPLETE-without-ledger), 56(foreign schema line), 65, 66, and the
        two reader guards 65/66 are each other's equivalents).
  If a mutant SURVIVES: add a test (pattern: S/tools/slice2_new/tests/*), copy to S/DEV/tests and S/dev_clone/tests, rerun
  `python3 -I S/tools/mhupa_slice2_mutations.py S/dev_clone --only N` to confirm, then rerun the FULL chain (suites + mutations)
  so the evidence matches the shipped tree:
    cd S/dev_clone && setsid nohup sh -c "python3 -B S/pkg_slice2/RUN_MHUPA_SLICE2_SUITE.py --repo S/dev_clone > S/suite_slice2_py313.log 2>&1; S/v315/bin/python -B S/pkg_slice2/RUN_MHUPA_SLICE2_SUITE.py --repo S/dev_clone > S/suite_slice2_py315.log 2>&1; python3 -I S/tools/mhupa_slice2_mutations.py S/dev_clone > S/mutations_slice2_py313.txt 2>&1" &
  (replace S by the full path; the Bash tool's cwd resets, use absolute paths).

## Remaining steps, in order

1. Wait for the mutation run to end with 0 survived (see above).
2. Assemble EX_147: `python3 S/tools/assemble_ex147.py S R` (needs: S/ex147_body.md with @@MUT@@/@@CONTENTS@@/@@TABLE@@
   placeholders - already written; S/MHUP_A_work_item_card_v1.md is the card at v5 - already updated; the EX_146 attachment at
   /mnt/user-data/attachments/05ef2f64-c028-5b8b-a9c5-1bd6b3c075ae/d00ee482-EX_146_ChatGPT.md must equal R/exchange/EX_146_ChatGPT.md).
   It stages R/exchange/EX_147_Claude/ (EX_147_Claude.md CRLF, EX_146_ChatGPT.md, MHUPA_Slice2_Review_v1.zip, its members list,
   mhupa_slice2_src_tests.diff, mhupa_slice1_to_slice2.diff) and R/exchange/EX_147_Claude.zip, and prints the SHA-256 of each.
3. TASK_T019: S/t019_lf.md is the LF draft with placeholders @@SHA@@ (the zip's SHA-256), @@SHA8@@ (its first 8 hex) and
   @@NFILES@@ (the number of files in the zip, from the members list line count). Fill them, write it CRLF + ASCII to
   R/CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T019.md. Overlay = 36 new + 33 replaced files, one git rm (step 6), 561 tests.
4. Also already edited in R (uncommitted, CRLF kept): CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md (rulebook v0.4, rule 7),
   exchange/OWNER_REMINDERS.md (R-019 status; new R-020), exchange/OWNER_ROADMAP.md (NOW line names EX_147 and T019).
   Also copy S/tools/{build_dev_slice2.sh,make_updater_v0_2.py,apply_slice2.py,edit_tests_slice2.py,mhupa_slice2_mutations.py,
   assemble_ex147.py} and S/pkg_slice2/RUN_MHUPA_SLICE2_SUITE.py and the folders S/tools/slice2_new, S/tools/slice2_edited into
   R/exchange/CLAUDE_WEB_TOOLS/mhupa/ (no __pycache__), as slice 1's tools were.
5. Commit everything in one commit (never `git add -A`; add exchange/ and CLAUDE_CODE_WORKING_FOLDER_TREE/ paths explicitly),
   message in the style of 3d825b3 ("exchange: EX_147 (Claude to ChatGPT): MHUP-A review slice 2 candidate v1 - ..."; name the
   561 tests, both Pythons, the mutant tally; reminder R-020; rulebook v0.4; TASK_T019; EX_146 preserved), end with the
   Co-Authored-By / Claude-Session lines of this session's reminder; push to origin main.
6. Tell the owner: the Fable task is finished (switch back to Opus); the paste-ready block for ChatGPT (EX_147's subject line,
   where the files are: exchange/EX_147_Claude.zip at the commit hash and its SHA-256, "please number your reply EX_148");
   and that TASK_T019 is ready to run ("Do inbox\TASK_T019.md").

## Facts to carry (for the handback and the owner)

- 561 tests = slice 1's 507 + 54 new (updater 15, launchers 10, mode_h 14, process_check 7, install_records 6, cli 2).
- Design interpretations (i)-(xiii) and (iii-b) are listed in S/ex147_body.md section 2; (iii) is a deviation from 5.2's
  per-pair score-line wording (one create-only ledger write) that the reviewer must rule on.
- R-020 (a): the integrated package's manifest must carry release_entries for E_1 revision 3 (both games).
- T018 PASSED (owner, 110eb41): the real committed ledgers pass the strict grammar; already cited in the body.
- Slice 1's reviewed bytes are unchanged except two test lines in test_mhupa_master_versions.py (v0_1 -> v0_2 file name).
