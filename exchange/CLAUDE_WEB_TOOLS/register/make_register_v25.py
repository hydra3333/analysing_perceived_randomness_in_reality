#!/usr/bin/env python3
"""Build register v0.25 CANDIDATE from the installed v0.24 Git blob. Claude, 6 November 2026.
Usage (repository root): python3 -I exchange/CLAUDE_WEB_TOOLS/register/make_register_v25.py OUT
Everything of v0.24 is kept byte for byte, except: the version line gains the v0.25 entry in front; the new section goes
immediately before '## Interpretation and verification'; a v0.25 current-status bullet goes first in that section. LF, UTF-8."""
import hashlib, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
V24 = 'doc/RATIFICATION_REGISTER_v0_24.md'
V24_SHA = '9d9fde67961d76fcc4823e97ac339c12e8b7e68ba309167652bd2c568f5c81ae'
old = subprocess.run(['git', 'show', 'HEAD:' + V24], capture_output=True, check=True).stdout.decode('utf-8')
assert hashlib.sha256(old.encode('utf-8')).hexdigest() == V24_SHA and '\r' not in old
parts = (HERE / 'register_v25_section.md').read_text(encoding='ascii').replace('\r\n', '\n')
ver = parts.split('@@VERSION@@\n')[1].split('\n@@SECTION@@\n')[0]
sec = parts.split('@@SECTION@@\n')[1].split('@@STATUS@@\n')[0]
status = parts.split('@@STATUS@@\n')[1]
VL = '**Register version:** '
assert old.count('\n' + VL) == 1 and ver.startswith(VL)
new = old.replace('\n' + VL, '\n' + ver + 'v0.24', 1) if False else old
i = new.index('\n' + VL) + 1
assert new[i + len(VL):].startswith('v0.24 OWNER-RATIFIED')
new = new[:i] + ver + new[i + len(VL):]
H = '## Interpretation and verification\n\n'
assert new.count(H) == 1
new = new.replace(H, sec.rstrip('\n') + '\n\n' + H + status.rstrip('\n') + '\n', 1)
new = new.replace('# Predictive Randomness — Ratification Register\n', '# Predictive Randomness — Ratification Register\n', 1)
Path(sys.argv[1]).write_bytes(new.encode('utf-8'))
# every v0.24 line must survive unchanged except the version line
ol, nl = old.split('\n'), new.split('\n')
missing = [l for l in ol if l not in set(nl) and not l.startswith(VL)]
assert not missing, missing[:3]
print(sys.argv[1], len(new.encode()), hashlib.sha256(new.encode()).hexdigest(), 'OK')
