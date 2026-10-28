"""NAMES-1 N1-T03 evidence: AST equality of every edited module, modulo the allowlisted substitutions.
Usage: python3 -I ast_check.py BASE_TREE RENAMED_TREE
For each edited .py file: parse the predecessor; apply the map's whole-word substitutions to every
import name, alias target module, and string constant (docstrings included); compare ast.dump with
the new file's AST. Equal dumps mean nothing but those names changed."""
import ast, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rename_map as R

base, tree = Path(sys.argv[1]), Path(sys.argv[2])
bare, fmap = R.bare(), R.files()
pat = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, bare), key=len, reverse=True)) + r')\b')
sub = lambda s: pat.sub(lambda m: bare[m.group(1)], s)

class Sub(ast.NodeTransformer):
    def visit_ImportFrom(self, n):
        if n.module: n.module = sub(n.module)
        for a in n.names: a.name = sub(a.name)
        return n
    def visit_Import(self, n):
        for a in n.names: a.name = sub(a.name)
        return n
    def visit_Constant(self, n):
        if isinstance(n.value, str): n.value = sub(n.value)
        return n

bad = 0; count = 0
inv = {v: k for k, v in fmap.items()}
for p in sorted({*(tree / 'src').rglob('*.py'), *(tree / 'tests').rglob('*.py')}):
    rel = p.relative_to(tree).as_posix(); old = inv.get(rel, rel)
    ob, nb = (base / old).read_bytes(), p.read_bytes()
    if ob == nb:
        continue
    count += 1
    a = ast.dump(Sub().visit(ast.parse(ob.decode('utf-8'))), include_attributes=False)
    b = ast.dump(ast.parse(nb.decode('utf-8')), include_attributes=False)
    ok = a == b; bad += not ok
    print(('PASS ' if ok else 'FAIL ') + f'{rel}: AST equal to predecessor with the map applied')
print(f'{count} edited modules checked'); print('RESULT', 'PASS' if not bad else f'FAIL ({bad})'); sys.exit(1 if bad else 0)
