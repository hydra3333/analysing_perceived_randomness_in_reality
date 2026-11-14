#!/usr/bin/env python3
"""Build H-1 v2 (the full consolidated Claude handover) from H-1 v1r8's ratified bytes.

Claude web chat, 14 November 2026. Usage (from anywhere):
    python3 -I make_h1_v2.py REPO OUT_FILE
REPO is a clone of main (it reads doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md through `git show HEAD:`).
The fragments and edit lists sit beside this script. Checks: v1r8's input hash; every counted edit's old text occurs
exactly once in v1r8 and once in the text it is applied to; every edit's new text survives into the output; the whole
of section 2A is byte-identical to v1r8's; the output is US-ASCII, LF, one final newline.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1R8 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md'
V1R8_SHA = '09e579ba008da0fd55e14ebd9e05d4f9b6c6bef54445fec85ca7bb120632a801'


def load_edits(name):
    ns = {}
    exec(compile((HERE / name).read_text(encoding='ascii'), name, 'exec'), ns)
    return ns['EDITS']


def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    assert text.count(start) == 1 and text.count(end) == 1, (start, end)
    return i, j


def main():
    repo, out = Path(sys.argv[1]), Path(sys.argv[2])
    raw = subprocess.run(['git', '-C', str(repo), 'show', 'HEAD:' + V1R8], capture_output=True, check=True).stdout
    assert hashlib.sha256(raw).hexdigest() == V1R8_SHA, 'v1r8 is not the ratified bytes'
    v1r8 = raw.decode('utf-8')
    i, j = between(v1r8, '### 2A. ', '## 3. Project in one paragraph')
    section_2a = v1r8[i:j]

    edits = load_edits('edits_s1_s9.py') + load_edits('edits_s7_s12.py') + load_edits('edits_appA.py')
    text = v1r8
    for k, (old, new) in enumerate(edits):
        assert v1r8.count(old) == 1, f'edit {k}: not exactly once in v1r8'
        assert text.count(old) == 1, f'edit {k}: not exactly once at application'
        text = text.replace(old, new)

    frag = lambda n: (HERE / n).read_text(encoding='ascii')
    # whole-section replacements (none of the counted edits lies inside them)
    i, j = between(text, '# H-1 - Claude primary designer', '## 1. Roles and workflow')
    text = frag('frag_00_header_s0.md') + '\n' + text[j:]
    i, j = between(text, '## 10. Next work, in order', '## 12. Working knowledge')
    text = text[:i] + frag('frag_10_11.md') + '\n' + text[j:]
    i, j = between(text, '### 12.8 Open items at DOC-11', '## Appendix A. Identities')
    text = text[:i] + frag('frag_12_8_9.md') + '\n' + text[j:]
    i = text.index('## Appendix B. Changes in v1r8')
    text = text[:i] + frag('frag_appB.md')

    for k, (old, new) in enumerate(edits):
        assert new in text, f'edit {k}: its new text did not survive'
    i, j = between(text, '### 2A. ', '## 3. Project in one paragraph')
    assert text[i:j] == section_2a, 'section 2A changed'
    data = text.encode('ascii')
    assert b'\r' not in data and data.endswith(b'\n') and not data.endswith(b'\n\n')
    out.write_bytes(data)
    print(f'H-1 v2 written: {out} ({len(data)} bytes, {text.count(chr(10))} lines, '
          f'{len(edits)} counted edits, 4 section replacements), SHA-256 {hashlib.sha256(data).hexdigest()}')


if __name__ == '__main__':
    main()
