#!/usr/bin/env python3
"""Build register v0.26 CANDIDATE from the installed v0.25 Git blob (Claude, 8 November 2026).
Usage (repository root): python3 -I exchange/CLAUDE_WEB_TOOLS/doc13/make_register_v26.py OUT
Every v0.25 line is kept, except the version line, which gains the v0.26 entry in front; the new section goes immediately before
'## Interpretation and verification'; a v0.26 current-status bullet goes first in that section. LF, UTF-8."""
import hashlib, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
V25 = 'doc/RATIFICATION_REGISTER_v0_25.md'
V25_SHA = '2ef9d17cfbc76c556e00d659677e411686c60aab263e1b0f0ef002930ee6d874'
old = subprocess.run(['git', 'show', 'HEAD:' + V25], capture_output=True, check=True).stdout.decode('utf-8')
assert hashlib.sha256(old.encode('utf-8')).hexdigest() == V25_SHA and '\r' not in old
parts = (HERE / 'register_v26_section.md').read_text(encoding='ascii').replace('\r\n', '\n')
ver = parts.split('@@VERSION@@\n')[1].split('@@SECTION@@')[0]
sec = parts.split('@@SECTION@@')[1].split('@@STATUS@@\n')[0].lstrip('\n')
status = parts.split('@@STATUS@@\n')[1]
VL = '**Register version:** '
assert old.count('\n' + VL) == 1 and ver.startswith(VL)
i = old.index('\n' + VL) + 1
assert old[i + len(VL):].startswith('v0.25 OWNER-RATIFIED')
new = old[:i] + ver + old[i + len(VL):]
H = '## Interpretation and verification\n\n'
assert new.count(H) == 1
new = new.replace(H, sec.rstrip('\n') + '\n\n' + H + status.rstrip('\n') + '\n', 1)
ol, nl = old.split('\n'), set(new.split('\n'))
missing = [l for l in ol if l not in nl and not l.startswith(VL)]
assert not missing, missing[:3]
out = new.encode('utf-8')
Path(sys.argv[1]).write_bytes(out)
print(sys.argv[1], len(out), hashlib.sha256(out).hexdigest(), 'OK')
