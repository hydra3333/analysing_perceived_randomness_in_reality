"""Compare function ASTs between committed coordinator v0.6 and a candidate.
The eleven protected functions must be identical; every other changed
function must then be read by hand (AST equality is not a safety proof).
Also apply the package's 'exact' diff to v0.6 and cmp with the shipped file:
  cp v06.py rebuilt.py && patch rebuilt.py < EXACT.diff && cmp rebuilt.py shipped.py
Usage: python -I 05_coordinator_ast.py v06.py candidate.py
"""
import ast, sys
PROTECTED = ['accept_ancestry_candidate', 'check_exited_worker_for_orphan', 'departed_members_check',
             'read_status', 'record_unresolved_orphan', 'register_root', 'require_no_unresolved_orphan',
             'save_new', 'status_and_result', 'status_orphan_evidence', 'terminate_owned_tree']
def funcs(p):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(ast.parse(open(p).read()))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
a, b = funcs(sys.argv[1]), funcs(sys.argv[2])
for p in PROTECTED:
    print(p, 'SAME' if p in a and a.get(p) == b.get(p) else 'DIFF/MISSING')
print('changed:', sorted(k for k in a if k in b and a[k] != b[k]))
print('added:', sorted(set(b) - set(a)), 'removed:', sorted(set(a) - set(b)))
