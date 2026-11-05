#!/usr/bin/env python3
"""Build H-2 v1r9 (candidate) from the installed H-2 v1r8 Git blob. Claude, 6 November 2026.

Usage (repository root): python3 -I exchange/CLAUDE_WEB_TOOLS/handover/build_h2_v1r9.py OUT
Keeps v1r8's sections 1-5 byte for byte (the protected '## 2.' to '## 4.' region included, asserted by length and SHA-256);
replaces the header and section 0 with h2_v1r9_new_parts.md's @@HEADER@@ part, and sections 6-7 with its @@SECTION6@@ part.
LF, UTF-8 (the protected region needs UTF-8; the new text is ASCII).
"""
import hashlib, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1])
V1R8 = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md'
V1R8_SHA = '4e2737c28a69ab73577fa6c39c87c04518e42ed1be47f240295e80802774b956'
REGION_LEN, REGION_SHA = 7676, '70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db'

old = subprocess.run(['git', 'show', 'HEAD:' + V1R8], capture_output=True, check=True).stdout
assert hashlib.sha256(old).hexdigest() == V1R8_SHA, 'v1r8 blob is not the expected one'
assert b'\r' not in old

def at(marker):
    assert old.count(marker) == 1, marker
    return old.index(marker) + 1

s1, s2, s4, s6 = at(b'\n## 1. '), at(b'\n## 2. '), at(b'\n## 4. '), at(b'\n## 6. ')
region = old[s2:s4]
assert len(region) == REGION_LEN and hashlib.sha256(region).hexdigest() == REGION_SHA, 'protected region changed'
kept = old[s1:s6]                       # sections 1-5, byte for byte

parts = (HERE / 'h2_v1r9_new_parts.md').read_bytes().replace(b'\r\n', b'\n')
head = parts.split(b'@@SECTION6@@\n')[0].split(b'@@HEADER@@\n')[1]
tail = parts.split(b'@@SECTION6@@\n')[1]
head.decode('ascii'); tail.decode('ascii')
new = head.rstrip(b'\n') + b'\n\n' + kept + tail
assert new.count(region) == 1
n2, n4 = new.index(b'\n## 2. ') + 1, new.index(b'\n## 4. ') + 1
assert new[n2:n4] == region
OUT.write_bytes(new)
print(OUT, len(new), hashlib.sha256(new).hexdigest(), 'region', len(region), REGION_SHA[:12], 'OK')
