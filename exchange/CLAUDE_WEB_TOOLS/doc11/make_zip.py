"""Deterministic ZIP of a folder (top folder kept) plus a member hash list. Usage: make_zip.py SRC_DIR OUT_ZIP MEMBERS_TXT [flat]"""
import zipfile, hashlib, sys
from pathlib import Path
src, out, mem = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
flat = len(sys.argv) > 4
base = src if flat else src.parent
paths = sorted(p for p in src.rglob('*') if p.is_file())
dirs = [] if flat else sorted({q for p in paths for q in p.relative_to(base).parents if str(q) != '.'})
with zipfile.ZipFile(out, 'w') as z:
    for d in dirs:
        zi = zipfile.ZipInfo(d.as_posix() + '/', (2026, 10, 28, 20, 0, 0)); zi.external_attr = (0o40755 << 16) | 0x10
        z.writestr(zi, b'')
    for p in paths:
        zi = zipfile.ZipInfo(p.relative_to(base).as_posix(), (2026, 10, 28, 20, 0, 0)); zi.external_attr = 0o644 << 16
        zi.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(zi, p.read_bytes())
lines = []
with zipfile.ZipFile(out) as z:
    for i in z.infolist():
        if not i.is_dir():
            b = z.read(i)
            lines.append(f'{hashlib.sha256(b).hexdigest()}  {hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()}  {i.filename}')
Path(mem).write_bytes(('# ' + Path(out).name + ' members: SHA-256 as stored, SHA-256 after CRLF->LF, path\r\n' + '\r\n'.join(lines) + '\r\n').encode('ascii'))
print(hashlib.sha256(open(out, 'rb').read()).hexdigest(), out, len(lines), 'members')
