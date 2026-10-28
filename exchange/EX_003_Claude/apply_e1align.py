"""E1-ALIGN author-side trial (design evidence only). Applies the proposed moves to a disposable tree
that already has the NAMES-1 renames. Usage: python3 -I apply_e1align.py TREE
Every edit is an exact, counted replacement; anything unexpected stops the script."""
import re, sys
from pathlib import Path

T = Path(sys.argv[1])
M = T / 'src' / 'methods'
E1 = ['e1_historical_appearance_frequency', 'e1_training_view', 'e1_standalone_contract',
      'e1_common_reader_bridge', 'multigame_e1']
log = []


def edit(rel, old, new, count=1):
    p = T / rel
    s = p.read_bytes().decode('utf-8')
    n = s.count(old)
    assert n == count, (rel, n, old[:60])
    p.write_bytes(s.replace(old, new).encode('utf-8'))
    log.append(f'{rel}: {count} x {old.splitlines()[0][:70]!r}')


core = 'src/methods/_common/e1_historical_appearance_frequency.py'
src = (T / core).read_text(encoding='utf-8')
CB = src[src.index('def canonical_bytes('):src.index('def _integer(')]
LT = src[src.index('def _length32_tuple('):src.index('def tie_digest(')]
assert CB.endswith('\n\n\n') and LT.endswith('\n\n\n')

# 1. New shared module: the two functions, bodies byte-for-byte (only the tuple helper's name loses "_").
shared = ('"""Shared canonical encodings, moved unchanged from E_1\'s module by E1-ALIGN.\n\n'
          'canonical_bytes: the project canonical JSON encoding. length32_tuple: the ratified tuple encoding\n'
          '(4-byte unsigned little-endian UTF-8 byte length, then the bytes). No method code may live here.\n"""\n'
          'from __future__ import annotations\n\nimport json\nfrom collections.abc import Sequence\n\n\n'
          + CB + LT.replace('def _length32_tuple(', 'def length32_tuple(', 1).rstrip('\n') + '\n')
(M / '_common' / 'canonical_encoding.py').write_bytes(shared.encode('utf-8'))
log.append('src/methods/_common/canonical_encoding.py: new')

# 2. E_1 core module: remove the two definitions; import them (old private name kept by alias).
edit(core, CB, '')
edit(core, LT, '')
edit(core, 'from collections.abc import Mapping, Sequence\n',
     'from collections.abc import Mapping, Sequence\n\n'
     'from _common.canonical_encoding import canonical_bytes, length32_tuple as _length32_tuple\n')

# 3. Shared reader: import the encoding from the shared module, not from E_1.
edit('src/methods/_common/game_draws_reader.py',
     'from _common.e1_historical_appearance_frequency import canonical_bytes',
     'from _common.canonical_encoding import canonical_bytes')

# 4. Move the five E_1-only modules into the method folder.
(M / 'E_001').mkdir()
(M / 'E_001' / '__init__.py').write_bytes(
    b'"""E_1 method folder: E_1-only modules (E1-ALIGN). The entry file stays in src/methods/."""\n')
for name in E1:
    (M / '_common' / f'{name}.py').rename(M / 'E_001' / f'{name}.py')
    log.append(f'move _common/{name}.py -> E_001/{name}.py')
edit('src/methods/E_001/e1_common_reader_bridge.py', 'from .game_draws_reader import DrawView',
     'from _common.game_draws_reader import DrawView')

# 5. Re-point every import / patch target: _common.<e1 module> -> E_001.<e1 module>.
pat = re.compile(r'\b_common\.(' + '|'.join(E1) + r')\b')
for p in sorted([*(T / 'src').rglob('*.py'), *(T / 'tests').glob('*.py')]):
    s = p.read_text(encoding='utf-8')
    new, n = pat.subn(r'E_001.\1', s)
    if n:
        p.write_bytes(new.encode('utf-8'))
        log.append(f'{p.relative_to(T).as_posix()}: {n} x _common.e1_* -> E_001.e1_*')

# 6. Widen the static import firewall to method folders, with an exact, counted E_1 allowance.
FW_OLD = """    def test_method_loader_import_firewall_except_accepted_legacy_e1(self):
        accepted_legacy='E_001_Historical_Appearance_Frequency.py'
        for method in (ROOT/'src'/'methods').glob('*.py'):
            if method.name==accepted_legacy:
                # Its own previously accepted standalone historical reader is
                # grandfathered; do not modify a frozen E1 golden source file.
                continue
            contents=method.read_text('utf-8')
            tree=ast.parse(contents)
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom):
                    self.assertNotIn('game_draws_reader',node.module or '')
                elif isinstance(node,ast.Import):
                    for alias in node.names:
                        self.assertNotIn('game_draws_reader',alias.name)
            self.assertNotIn('source_data',contents)
"""
FW_NEW = """    def test_method_loader_import_firewall_except_accepted_legacy_e1(self):
        accepted_legacy='E_001_Historical_Appearance_Frequency.py'
        # E1-ALIGN: method folders are scanned too. E_1's accepted legacy references
        # inside its folder are allowed exactly (file, kind, reference, count); any
        # other reference, file or folder is rejected, and every allowance must be used.
        allowed={('E_001/e1_training_view.py','text','source_data'):1,
                 ('E_001/e1_common_reader_bridge.py','import','_common.game_draws_reader'):1}
        used={}
        methods=ROOT/'src'/'methods'
        files=sorted([*methods.glob('*.py'),*methods.glob('E_[0-9][0-9][0-9]/**/*.py')])
        for method in files:
            rel=method.relative_to(methods).as_posix()
            if rel==accepted_legacy:
                # Its own previously accepted standalone historical reader is
                # grandfathered; do not modify a frozen E1 golden source file.
                continue
            contents=method.read_text('utf-8')
            tree=ast.parse(contents)
            refs=[]
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom):
                    refs.append(node.module or '')
                elif isinstance(node,ast.Import):
                    refs.extend(alias.name for alias in node.names)
            for ref in refs:
                if 'game_draws_reader' in ref:
                    key=(rel,'import',ref)
                    self.assertIn(key,allowed,f'unauthorised reader import in {rel}')
                    used[key]=used.get(key,0)+1
            n=contents.count('source_data')
            if n:
                key=(rel,'text','source_data')
                self.assertIn(key,allowed,f'unauthorised source_data reference in {rel}')
                used[key]=used.get(key,0)+n
        self.assertEqual(used,allowed)
"""
edit('tests/test_multigame_static_and_timing.py', FW_OLD, FW_NEW)
print('\n'.join(log))
