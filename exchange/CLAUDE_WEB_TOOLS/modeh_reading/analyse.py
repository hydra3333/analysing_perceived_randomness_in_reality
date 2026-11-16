"""Summaries of a Mode H report (value-free). Usage: analyse.py REPORT.txt"""
import re, sys, math, statistics
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from parse_report import parse
lines, T, meta = parse(sys.argv[1])
game = 'POWERBALL' if 'POWERBALL' in sys.argv[1] or 'pb' in sys.argv[1] else 'OZLOTTO'
num = r'([-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)'

def pvals(key):
    """(unit, Z_plus, primary P_up or None, label, N1-reference P or None)"""
    out = []
    for r in T[key]:
        m = re.match(num + r'\s+(\S+)\s+(.*)$', r['rest'])
        z = float(m.group(1)); p = None if m.group(2) == '-' else float(m.group(2)); label = m.group(3)
        ref = None
        for e in r['extra']:
            mm = re.search(r'also: N1_FIXED_FORECAST_REFERENCE, Z_plus ' + num + r', P_up ' + num, e)
            if mm: ref = float(mm.group(2))
        out.append((r['unit'], z, p, label, ref))
    return out

print('=== Part B: per table, the smallest local P_up (primary label), and counts')
allp = []
for key in T:
    if key[0] != 'B': continue
    pv = pvals(key)
    prim = [(p, u, l) for u, z, p, l, ref in pv if p is not None]
    refs = [(ref, u) for u, z, p, l, ref in pv if ref is not None]
    use = prim if prim else [(r, u, 'N1_FIXED_FORECAST_REFERENCE') for r, u in refs]
    if not use:
        print(f'{key[1]:14s} no P'); continue
    mn = min(use)
    labels = sorted({l.split()[0] for _, _, l in use})
    print(f'{key[1]:14s} n={len(use):3d} minP={mn[0]:.5g} ({mn[1].split(":",1)[1]})  P<0.05: {sum(1 for p,_,_ in use if p<0.05):2d}  P<0.01: {sum(1 for p,_,_ in use if p<0.01):2d}  zpos: {sum(1 for u,z,p,l,ref in pv if z>0):2d}  labels {labels}')
    allp += [(p, key[1], u) for p, u, _ in use]
allp.sort()
print('\n=== the ten smallest local P_up anywhere in Part B (all tables, duplicates included)')
for p, k, u in allp[:10]:
    print(f'  {p:.5g}  {k:12s} {u}')
print('tables', len({k for _,k,_ in allp}), 'figures', len(allp))
