"""Apply the NAMES-1 candidate map to a disposable tree (design evidence only). Usage: apply_trial.py TREE"""
import re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import rename_map as R
tree = Path(sys.argv[1])
for old, new in R.files().items():
    (tree / old).rename(tree / new)
bare = R.bare()
pat = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, bare), key=len, reverse=True)) + r')\b')
report = {}
for p in sorted(list((tree / 'src').rglob('*.py')) + list((tree / 'tests').glob('*.py')) + list((tree / 'tests').rglob('*.py'))):
    txt = p.read_text(encoding='utf-8')
    new, n = pat.subn(lambda m: bare[m.group(1)], txt)
    if n:
        p.write_text(new, encoding='utf-8')
        report[p.relative_to(tree).as_posix()] = n
for k, v in sorted(report.items()):
    print(f'{v:4d}  {k}')
print('files edited:', len(report), ' substitutions:', sum(report.values()))
