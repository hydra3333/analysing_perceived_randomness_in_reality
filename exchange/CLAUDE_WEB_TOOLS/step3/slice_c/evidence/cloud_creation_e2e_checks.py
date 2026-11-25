"""Workspace evidence (not project code): the real start of a tree's own Python on the checks program."""
import sys, time
from pathlib import Path
DEV = Path('/home/claude/work/dev12'); QA = Path('/home/claude/work/e2e/qa')
sys.path[:0] = [str(DEV / 'deploy'), str(DEV / 'src'), str(DEV / 'src' / 'methods')]
import install_common as common
own = QA / '.venv' / 'bin' / 'python'
began = time.monotonic()
lines = []
found = common.checks_with_target_python(own, QA, QA, common.ALL_VARIANTS, True, True, say=lines.append)
print('with the tree\'s own Python:', round(time.monotonic() - began, 1), 's')
print(' smoke asked:', found['smoke']['asked'], '; failures:', len(found['smoke']['failures']))
for failure in found['smoke']['failures'][:5]:
    print('  ', failure[:300])
print(' sample:', found['sample'], '; derived:', found['derived'], '; unreadable:', found['unreadable'], '; marker:', found['marker'])
print(' faults that stop:', common.faults_that_stop(found))
print(' scratch left:', sorted(p.name for p in (QA / 'scratch').iterdir()) if (QA / 'scratch').exists() else None)
try:
    common.checks_with_target_python(Path('/home/claude/work/venv315/bin/python'), QA, QA, common.ALL_VARIANTS, False, False, say=lines.append)
    print('with another Python: NOT REFUSED')
except common.InstallRefused as refusal:
    print('with another Python: refused:', str(refusal)[:160])
