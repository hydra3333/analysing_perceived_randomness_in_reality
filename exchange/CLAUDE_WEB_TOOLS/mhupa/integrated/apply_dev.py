"""Apply the DEV tree's changes (vs BASE) to a full clone: copy changed/new files, delete removed ones. Prints counts."""
import sys, shutil, pathlib
B, D, T = map(pathlib.Path, sys.argv[1:4])
n = 0
for p in D.rglob('*'):
    if not p.is_file() or '__pycache__' in p.parts: continue
    rel = p.relative_to(D); b = B / rel
    if b.is_file() and b.read_bytes() == p.read_bytes(): continue
    (T / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, T / rel); n += 1
gone = [p.relative_to(B) for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not (D / p.relative_to(B)).exists()]
for g in gone: (T / g).unlink()
print('copied', n, 'removed', [str(g) for g in gone])
