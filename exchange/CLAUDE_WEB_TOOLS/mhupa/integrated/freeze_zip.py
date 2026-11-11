"""Zip the built MHUP-A package reproducibly (Claude web chat, 11 November 2026, gate A).
Usage: python3 -I freeze_zip.py PKG_DIR OUT_ZIP DATE
Members in sorted order under the top folder named like PKG_DIR, each dated DATE 00:00:00, mode 0644, deflated;
directories are not stored. Prints the member count and the zip's SHA-256."""
import hashlib, sys, zipfile
from pathlib import Path

src, out, date = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3]
y, m, d = (int(x) for x in date.split('-'))
files = sorted(p for p in src.rglob('*') if p.is_file())
assert not any(p.is_symlink() for p in src.rglob('*')), 'a symlink in the package'
assert not any('__pycache__' in p.parts for p in files), 'a byte-code cache in the package'
with zipfile.ZipFile(out, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for p in files:
        info = zipfile.ZipInfo(f'{src.name}/{p.relative_to(src).as_posix()}', date_time=(y, m, d, 0, 0, 0))
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, p.read_bytes())
print(f'{len(files)} files zipped into {out}')
print('SHA-256', hashlib.sha256(out.read_bytes()).hexdigest())
