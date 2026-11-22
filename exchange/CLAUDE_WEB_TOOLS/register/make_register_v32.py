#!/usr/bin/env python3
"""Make the register v0.32 candidate from the installed register v0.31 by two counted insertions (Claude, 22 November 2026).

Purpose: the version line, and the new section (register_v32_section.md, beside this file) placed before
"## Interpretation and verification". Nothing of v0.31 is changed or removed.
Every "@@SHA:<path>@@" in the section is replaced by the SHA-256 of that file's bytes as Git stores them at HEAD.
Usage: python3 -I make_register_v32.py REPO_ROOT OUT_FILE
It refuses (an assertion) if v0.31 at HEAD is not the installed bytes, if an anchor does not occur exactly once, if the
section is not US-ASCII with LF, or if a placeholder is left unfilled.
"""
import hashlib, os, re, subprocess, sys

# ---- constants -------------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = 'doc/RATIFICATION_REGISTER_v0_31.md'                                     # the register being extended
SRC_SHA = 'c6369a72753ebda016f758e623df7a40bcb7a1300a49d503ccbb93be1b3cae6d'        # v0.31 as installed at 0044de8 (RAT-34)
SECTION_FILE = 'register_v32_section.md'                                            # the one new section
OLD_VERSION = '**Register version:** v0.31, 17 November 2026, OWNER-RATIFIED'       # start of v0.31's version line
NEW_VERSION = ('**Register version:** v0.32, 22 November 2026, CANDIDATE for the owner\'s ratification (with H-1 v8; written by '
               'Claude from the records; for the reviewer\'s review), recording the RAT-34 install (`0044de8`), RAT-35 to RAT-40, '
               'the MHUP-B code plan and its three reviewed slices (not installed), the owner\'s course correction of 20 and '
               '21 November 2026, the new system ratified as RAT-40 (`4de0fe4`) and EX_216 to EX_272; '
               'v0.31, 17 November 2026, OWNER-RATIFIED')
ANCHOR = '\n## Interpretation and verification\n'                                    # the section goes just before this

def git_bytes(repo, path):
    """Return the bytes of <path> at HEAD. Example: git_bytes(repo, 'exchange/README.md') -> b'# exchange/ ...'."""
    return subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + path], check=True, capture_output=True).stdout

def sha(data):
    """SHA-256 of bytes as 64 lower-case hex characters."""
    return hashlib.sha256(data).hexdigest()

def main():
    assert len(sys.argv) == 3, 'usage: make_register_v32.py REPO_ROOT OUT_FILE'
    repo, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    src = git_bytes(repo, SRC_PATH)
    assert sha(src) == SRC_SHA, 'v0.31 at HEAD is not the installed bytes'
    text = src.decode('utf-8')
    section_bytes = open(os.path.join(HERE, SECTION_FILE), 'rb').read()
    section = section_bytes.decode('ascii')                       # refuses any non-ASCII character
    assert '\r' not in section and section.endswith('\n\n') and section.startswith('## '), 'section shape'
    paths = re.findall(r'@@SHA:(.+?)@@', section)
    section = re.sub(r'@@SHA:(.+?)@@', lambda m: sha(git_bytes(repo, m.group(1))), section)
    assert '@@' not in section, 'unfilled placeholder'
    for label, old, new in (('version', OLD_VERSION, NEW_VERSION), ('section', ANCHOR, '\n' + section + ANCHOR[1:])):
        n = text.count(old)
        assert n == 1, '%s: expected one occurrence, found %d' % (label, n)
        text = text.replace(old, new)
    data = text.encode('utf-8')
    assert b'\r' not in data and data.endswith(b'\n')
    with open(out, 'wb') as f:
        f.write(data)
    print('2 counted insertions; %d hashes filled; %d bytes; SHA-256 %s' % (len(paths), len(data), sha(data)))

if __name__ == '__main__':
    main()
