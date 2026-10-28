"""Apply exactly the reviewer's two FIX AND PROCEED corrections (EX_016: DOC3-H1-C01, DOC3-H1-C02) to the
reviewed H-1 v1r3 candidate (19d9cc59...cf01). Two counted edits, verbatim reviewer wording; nothing else.
Usage: python3 -I fix_h1_v1r3_EX016.py IN OUT"""
import hashlib, sys
raw = open(sys.argv[1], 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '19d9cc5973b35b89225e63b244d52869987a6e3d6aedef226fad22d3df04cf01'
t = raw.decode('ascii')
E = [
 ("sole ratifier, execution authoriser and committer.",
  "sole ratifier and execution authoriser, and sole committer of project files outside exchange/; Claude's owner-authorised exception is limited to committing exchange/ audit records (section 1.6)."),
 ("on a STOP the commit is still local and `git reset --hard HEAD~1` removes it.",
  "If a committed-phase STOP occurs before push, stop. Use the package's approved local recovery steps only after verifying that HEAD is the specific unpushed package commit and that neither the index nor working tree contains unrelated changes. Never run an unconditional `git reset --hard HEAD~1`; if any identity or state is uncertain, ask the owner to inspect it rather than guessing."),
]
for a, b in E:
    assert t.count(a) == 1, a[:50]; assert all(ord(c) < 128 for c in b)
    t = t.replace(a, b)
open(sys.argv[2], 'wb').write(t.encode('ascii'))
print(sys.argv[2], hashlib.sha256(t.encode()).hexdigest())
