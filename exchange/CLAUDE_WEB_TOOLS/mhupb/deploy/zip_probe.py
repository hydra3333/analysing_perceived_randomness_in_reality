"""A design-stage PROBE for the deployment design note (19-20 November 2026). NOT project code, not a test, not installed.
It answers three questions about Python's own zipfile on an invented tree of the size the owner measured (about 81,500
files, 211 MB): does it write the ZIP64 form past 65,535 entries; does a manifest-checked round trip give back every
byte; roughly how long and how big. Cloud, Linux, invented files: the times are an indication only, and whether Windows
File Explorer opens the result can only be shown on the owner's PC.
Usage: python3 -I zip_probe.py WORK_DIR [FILES] [TOTAL_MB]
"""
import hashlib, json, os, random, sys, time, zipfile
work = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 81500; mb = int(sys.argv[3]) if len(sys.argv) > 3 else 211
tree, out, back = (os.path.join(work, x) for x in ('tree', 'snap.zip.partial', 'restored'))
rnd = random.Random(20261119)
size = mb * 1024 * 1024 // n
t0 = time.time()
for i in range(n):                                   # invented records: JSON text with hex digests, like run records
    d = os.path.join(tree, 'results', f'g{i % 2}', f'batch{i % 40:02d}', f'run{i // 500:04d}')
    os.makedirs(d, exist_ok=True)
    body = {'schema': 'INVENTED_V1', 'n': i, 'digests': []}
    while len(json.dumps(body)) < size:
        body['digests'].append('%064x' % rnd.getrandbits(256))
    with open(os.path.join(d, f'record_{i:06d}.json'), 'w', encoding='ascii') as fh:
        json.dump(body, fh)
os.makedirs(os.path.join(tree, 'empty_folder'))
t1 = time.time()
manifest, total = [], 0
with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for dp, dn, fn in os.walk(tree):
        dn.sort()
        rel = os.path.relpath(dp, tree).replace(os.sep, '/')
        if not dn and not fn:
            z.writestr(rel + '/', b'')
        for f in sorted(fn):
            p = os.path.join(dp, f); raw = open(p, 'rb').read()
            name = (rel + '/' + f) if rel != '.' else f
            z.write(p, name); manifest.append([name, len(raw), hashlib.sha256(raw).hexdigest()]); total += len(raw)
    z.writestr('SNAPSHOT_MANIFEST.json', json.dumps({'files': manifest}, separators=(',', ':')))
t2 = time.time()
raw = open(out, 'rb').read()
zip64 = b'PK\x06\x06' in raw[-200000:] and b'PK\x06\x07' in raw[-200000:]
with zipfile.ZipFile(out) as z:                      # the read-back check: every member against the manifest
    names = set(z.namelist())
    listed = json.loads(z.read('SNAPSHOT_MANIFEST.json'))['files']
    bad = sum(1 for name, sz, h in listed if hashlib.sha256(z.read(name)).hexdigest() != h)
    extra = names - {m[0] for m in listed} - {'SNAPSHOT_MANIFEST.json', 'empty_folder/'}
t3 = time.time()
with zipfile.ZipFile(out) as z:
    z.extractall(back)
same = all(hashlib.sha256(open(os.path.join(back, name), 'rb').read()).hexdigest() == h for name, sz, h in listed)
t4 = time.time()
print(f'python {sys.version.split()[0]}; files {len(manifest)}; bytes {total} ({total / 1048576:.0f} MB)')
print(f'zip bytes {len(raw)} ({len(raw) / 1048576:.0f} MB); entries {len(names)}; ZIP64 end records present: {zip64}')
print(f'read-back mismatches {bad}; unexpected members {len(extra)}; empty folder restored: {os.path.isdir(os.path.join(back, "empty_folder"))}')
print(f'restored tree equals the manifest: {same}')
print(f'seconds: make tree {t1 - t0:.0f}; write zip {t2 - t1:.0f}; read-back check {t3 - t2:.0f}; extract and compare {t4 - t3:.0f}')
