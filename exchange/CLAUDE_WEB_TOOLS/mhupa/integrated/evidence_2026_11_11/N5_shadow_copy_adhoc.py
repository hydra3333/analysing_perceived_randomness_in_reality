"""Ad hoc (11 Nov 2026): a barrier-free byte copy of a rehearsal tree, to test an option for Appendix J step 10 (finding N5).
Copies every tracked file and every package file exactly as it is on disk (no Git conversion); never E, P or U."""
import json, shutil, subprocess, sys
from pathlib import Path
repo, man, dest = Path(sys.argv[1]), json.load(open(sys.argv[2])), Path(sys.argv[3])
tracked = subprocess.run(['git', '-C', str(repo), 'ls-files', '-z'], capture_output=True, check=True).stdout.decode().split('\0')
paths = sorted({p for p in tracked if p} | set(man['new']))
skip = set(man['barriers'].values()) | set(man['deleted'])
n = 0
for p in paths:
    if p in skip or not (repo / p).is_file():
        continue
    (dest / p).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(repo / p, dest / p); n += 1
print('copied', n, 'files; barriers present in the copy:', [k for k, v in man['barriers'].items() if (dest / v).exists()])
