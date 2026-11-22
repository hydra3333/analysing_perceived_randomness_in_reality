#!/usr/bin/env python3
"""Install the ratified local runner rulebook v0.6 (RAT-42; Claude, 22 November 2026).

Purpose: read the reviewed candidate from Git at HEAD (asserted by SHA-256; PASS in EX_274), change ONLY the status
words of its version line, and write it over CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md, which must hold the installed
v0.5 bytes when this runs (Git keeps v0.5 in its history).
Usage: python3 -I finalise_rat42.py REPO_ROOT
It refuses (an assertion) on a wrong candidate or target hash, or if the status text is not found exactly once.
"""
import hashlib, os, subprocess, sys

# ---- constants -------------------------------------------------------------------------------------------------
CAND = 'exchange/CLAUDE_WEB_TOOLS/rulebook_v0_6/CLAUDE_v0_6_CANDIDATE.md'
CAND_SHA = '9d2cae3c780344797e6054b1eeeee875db5efc84aa8384ea7b4fa53ca4e8830f'      # reviewed in EX_274
TARGET = 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'
TARGET_SHA = 'fa7a5fe229be832880cda4704ed9e7d27af2f4b9462464f7af262e540acd5200'    # rulebook v0.5 as installed (RAT-30)
OLD = ("**Version:** v0.6 CANDIDATE, 22 November 2026: written by the Claude web chat for the reviewer's review and the project "
       "owner's ratification; NOT installed and not in force until then (v0.6:")
NEW = ("**Version:** v0.6, 22 November 2026, ratified by the project owner the same day (RAT-42) after the reviewer's PASS "
       "(EX_274) (v0.6:")

def sha(data):
    """SHA-256 of bytes as 64 lower-case hex characters."""
    return hashlib.sha256(data).hexdigest()

def main():
    assert len(sys.argv) == 2, 'usage: finalise_rat42.py REPO_ROOT'
    repo = os.path.abspath(sys.argv[1])
    cand = subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + CAND], check=True, capture_output=True).stdout
    assert sha(cand) == CAND_SHA, 'the candidate at HEAD is not the reviewed bytes'
    target = os.path.join(repo, TARGET)
    assert sha(open(target, 'rb').read().replace(b'\r\n', b'\n')) == TARGET_SHA, 'the installed rulebook is not v0.5'
    text = cand.decode('ascii')
    assert text.count(OLD) == 1, 'status text: expected one occurrence'
    data = text.replace(OLD, NEW).encode('ascii')
    assert b'\r' not in data and data.endswith(b'\n')
    with open(target, 'wb') as f:
        f.write(data)
    print('%s  %d bytes  %s' % (sha(data), len(data), TARGET))

if __name__ == '__main__':
    main()
