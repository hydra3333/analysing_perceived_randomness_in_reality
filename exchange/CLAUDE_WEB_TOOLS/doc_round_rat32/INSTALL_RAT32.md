# RAT-32 documentation install: H-1 v3, its blurb and register v0.30 (owner-run; about two minutes)

Ratified by the owner on 15 November 2026, about 09:10 (decision log entry 6). Three new files under doc/; nothing else
changes; nothing for Mode H. The zip and its read-only verifier are already in the repository, so nothing needs downloading.
One CMD window at the repository root. Run one block at a time; anything other than the "Expect" is a STOP: run nothing
further, change nothing, send the window to Claude.

## Block 1: up to date and clean

    cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
    git pull --ff-only
    git status --short

Expect: the pull succeeds; nothing from git status.

## Block 2: check the zip, unpack it, check the files

    "%CD%\.venv\Scripts\python.exe" -I -B exchange\CLAUDE_WEB_TOOLS\doc_round_rat32\verify_doc_round.py zip exchange\CLAUDE_WEB_TOOLS\doc_round_rat32\DOC_ROUND_RAT32.zip
    tar -xf exchange\CLAUDE_WEB_TOOLS\doc_round_rat32\DOC_ROUND_RAT32.zip
    "%CD%\.venv\Scripts\python.exe" -I -B exchange\CLAUDE_WEB_TOOLS\doc_round_rat32\verify_doc_round.py post

Expect: ZIP PASS: exactly the three expected files, every one with the expected bytes
        POST PASS: the three files are in place with the expected bytes, and nothing else changed

## Block 3: commit, check, push

    git add doc/HANDOVER/Claude_Primary_Handover_H1_v3.md doc/HANDOVER/Claude_Primary_Handover_H1_v3_introductory_blurb.md doc/RATIFICATION_REGISTER_v0_30.md
    git status --short
    git commit -m "doc: H-1 v3 and register v0.30 (owner-ratified 15 November 2026, RAT-32)"
    "%CD%\.venv\Scripts\python.exe" -I -B exchange\CLAUDE_WEB_TOOLS\doc_round_rat32\verify_doc_round.py committed

Expect: three "LF will be replaced by CRLF" warnings (harmless); status shows exactly three lines starting "A " for those
paths; the commit creates three files; COMMITTED PASS: the last commit adds exactly the three files, with the expected bytes.
Only after COMMITTED PASS:

    git push

Then tell Claude the commit id; Claude checks it from GitHub.
