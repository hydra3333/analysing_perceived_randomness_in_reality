"""NAMES-1 v0.2 design evidence: N1-T02 against the exact allowlist (N1-C01).

Usage: python3 -I t02_check.py BASE_TREE RENAMED_TREE ALLOWLIST_TSV
Rebuilds each edited file from its predecessor by replacing only the allowlisted (line, token) sites,
and requires byte equality with the renamed file. Every other file in the tree (including pure renames
under their new paths) must be byte-identical to its predecessor. Prints every authorised change.
"""
import csv, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rename_map as R

base, tree, allow = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
rows = list(csv.DictReader(open(allow, newline=''), delimiter='\t'))
by_file = defaultdict(list)
for r in rows:
    by_file[r['old_path']].append(r)
fmap = R.files()
bad = 0
for old_rel, rs in sorted(by_file.items()):
    lines = (base / old_rel).read_bytes().decode('utf-8').split('\n')
    for r in rs:
        i = int(r['line']) - 1
        assert lines[i].count(r['old_token']) >= 1, r
        lines[i] = lines[i].replace(r['old_token'], r['new_token'], 1)
        print(f"  {r['category']:<16} {r['new_path']}:{r['line']}  {r['old_token']} -> {r['new_token']}")
    want = '\n'.join(lines).encode('utf-8')
    got = (tree / fmap.get(old_rel, old_rel)).read_bytes()
    ok = want == got
    bad += not ok
    print(('PASS ' if ok else 'FAIL ') + f'{old_rel}: {len(rs)} authorised change(s) and nothing else')
inv = {v: k for k, v in fmap.items()}
others = 0
for p in sorted(tree.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts:
        continue
    rel = p.relative_to(tree).as_posix()
    old_rel = inv.get(rel, rel)
    if old_rel in by_file:
        continue
    others += 1
    if not (base / old_rel).is_file() or (base / old_rel).read_bytes() != p.read_bytes():
        bad += 1
        print('FAIL unexpected change or addition:', rel)
n_base = sum(1 for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
n_tree = sum(1 for p in tree.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
bad += n_base != n_tree
print(f'{others} other files byte-identical (pure renames included); file count {n_base} -> {n_tree}')
print(f'{len(rows)} authorised changes in {len(by_file)} files')
print('RESULT', 'PASS' if not bad else f'FAIL ({bad})')
sys.exit(1 if bad else 0)
