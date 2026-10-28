"""Generate the frozen E1-ALIGN exact-edit allowlist from two trial trees (run once, then reviewed).
Usage: python3 -I gen_e1align_allowlist.py NAMES1_TREE E1ALIGN_TREE OUT_JSON
For every changed file: its old and new path, and its edits as exact (old text, new text) blocks,
each with enough unchanged context lines to occur exactly once in the old file. Added files are
listed with their SHA-256; files moved unchanged are listed as such. The checker then rebuilds every
new file from its old file using only these blocks, and requires byte equality."""
import difflib, hashlib, json, sys
from pathlib import Path

a, b, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
E1 = ['e1_historical_appearance_frequency', 'e1_training_view', 'e1_standalone_contract',
      'e1_common_reader_bridge', 'multigame_e1']
moves = {f'src/methods/_common/{n}.py': f'src/methods/E_001/{n}.py' for n in E1}
files = lambda t: sorted(p.relative_to(t).as_posix() for p in t.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
fa, fb = set(files(a)), set(files(b))
inv = {v: k for k, v in moves.items()}
added = sorted(fb - fa - set(moves.values()))
doc = {'moves': moves, 'added': {p: hashlib.sha256((b / p).read_bytes()).hexdigest() for p in added},
       'moved_unchanged': [], 'edited': []}
for new in sorted(fb):
    old = inv.get(new, new)
    if old not in fa:
        continue
    ob, nb = (a / old).read_bytes(), (b / new).read_bytes()
    if ob == nb:
        if old != new:
            doc['moved_unchanged'].append(new)
        continue
    ol = ob.decode('utf-8').splitlines(keepends=True); nl = nb.decode('utf-8').splitlines(keepends=True)
    otext = ''.join(ol)
    edits = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ol, nl, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        c = 1
        while True:
            lo = max(0, i1 - c)
            oblk = ''.join(ol[lo:i2]); nblk = ''.join(ol[lo:i1]) + ''.join(nl[j1:j2])
            if otext.count(oblk) == 1:
                break
            c += 1
        edits.append({'old': oblk, 'new': nblk})
    doc['edited'].append({'old_path': old, 'new_path': new, 'edits': edits})
json.dump(doc, open(out, 'w', newline='\n'), indent=1, sort_keys=False)
print(len(doc['edited']), 'edited files;', sum(len(e['edits']) for e in doc['edited']), 'edit blocks;',
      len(doc['moved_unchanged']), 'moved unchanged;', len(added), 'added')
