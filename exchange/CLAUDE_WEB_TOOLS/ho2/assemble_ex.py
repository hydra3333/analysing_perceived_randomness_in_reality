"""assemble_ex.py DIR NNN BODY_FILE : writes DIR/EX_NNN_Claude.md = body + member table (CRLF, ASCII)."""
import sys, hashlib, pathlib
d = pathlib.Path(sys.argv[1]); nnn = sys.argv[2]; body = pathlib.Path(sys.argv[3]).read_text(encoding="ascii")
ex = f"EX_{nnn}_Claude.md"
members = sorted(p.name for p in d.iterdir() if p.is_file() and p.name != ex)
rows = []
for m in members:
    b = (d / m).read_bytes()
    assert all(c < 128 for c in b), m
    rows.append(f"| {m} | {hashlib.sha256(b).hexdigest()} | {hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()} |")
body = body.replace("@@CONTENTS@@", ", ".join([ex] + members))
table = "| Member | SHA-256 as stored | SHA-256 after CRLF->LF |\n|---|---|---|\n" + "\n".join(rows) + "\n"
txt = body.replace("@@TABLE@@", table).replace("\r\n", "\n")
assert all(ord(c) < 128 for c in txt)
(d / ex).write_bytes(txt.replace("\n", "\r\n").encode("ascii"))
print(ex, len(members), "members")
