"""Workspace evidence (not project code): a creation run on the real software of the slice C tree, in the cloud."""
import sys
from pathlib import Path
DEV = Path('/home/claude/work/dev12'); QA = Path('/home/claude/work/e2e/qa')
sys.path[:0] = [str(DEV / 'deploy'), str(DEV / 'src'), str(DEV / 'src' / 'methods')]
import init_tree, install_readiness
from research import settings, variant_folders
(DEV / 'ENVIRONMENT.ini').write_bytes((f'[environment]\r\nrole = DEV\r\ntree_root = {DEV}\r\nvenv_dir = {DEV / ".venv"}\r\n'
                                       f'[QA]\r\ntree_root = {QA}\r\nbackup_root = {QA.parent / "qa_backups"}\r\nvenv_dir = {QA / ".venv"}\r\n').encode())
print(install_readiness.mark_infrastructure(DEV))
variants, refused = variant_folders.find_variants(DEV / 'src' / 'methods')
print(len(variants), 'variant folders;', len(refused), 'refused')
marked = 0
for v in variants:
    try:
        install_readiness.mark_variant(DEV, v.family, v.variant); marked += 1
    except install_readiness.ReadinessRefused as r:
        print('NOT MARKED', v.identity, str(r)[:300])
print('marked', marked)
said = []
code = init_tree.main(['QA'], settings.read_dev_view(DEV), say=said.append, ask=lambda prompt: 'YES')
print('exit code', code)
for line in said:
    if not line.startswith('  add: '):
        print(line[:400])
