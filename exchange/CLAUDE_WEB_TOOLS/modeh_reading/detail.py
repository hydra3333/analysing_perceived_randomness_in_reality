"""Descriptive detail and independent arithmetic checks from a Mode H report's own figures. Usage: detail.py REPORT GAME"""
import re, sys, math
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from parse_report import parse
lines, T, meta = parse(sys.argv[1]); game = sys.argv[2]
N, K = (35, 7) if game == 'POWERBALL' else (47, 7)
num = r'([-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)'
# exact null of main matches per draw and of the 10-draw total
pm = [F(math.comb(K, k) * math.comb(N - K, K - k), math.comb(N, K)) for k in range(K + 1)]
def conv(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i + j] += x * y
    return out
tot = [F(1)]
for _ in range(10): tot = conv(tot, pm)
tail = lambda s: float(sum(tot[s:]))
mean10 = float(sum(i * p for i, p in enumerate(tot)))
sd10 = math.sqrt(float(sum(i * i * p for i, p in enumerate(tot))) - mean10 ** 2)
print(f'{game}: fair main matches over 10 draws: mean {mean10:.4f}, SD {sd10:.4f}')

A = {r['unit']: int(re.search(r'main matches (\d+)', r['extra'][0]).group(1)) for r in T[('A', 'MR7.MAIN')]}
B = {}
for r in T[('B', 'MR7.MAIN')]:
    m = re.match(num + r'\s+' + num, r['rest']); B[r['unit']] = (float(m.group(1)), float(m.group(2)))
bad = [(u, A[u], B[u][1], tail(A[u])) for u in A if abs(tail(A[u]) - B[u][1]) > 5e-6 * max(1, B[u][1]) and abs(tail(A[u]) - B[u][1]) > 1e-7]
print(f'MR7.MAIN: exact tail recomputed from each track\'s match total for {len(A)} tracks; mismatches with the report\'s P_up: {len(bad)}', bad[:3])
side = lambda u: u.split(':')[3]
for s in ('TOP', 'WORST'):
    v = sorted(A[u] for u in A if side(u) == s)
    print(f'  {s}: n={len(v)} total {sum(v)} (fair {mean10*len(v):.1f}); mean {sum(v)/len(v):.2f}; min {v[0]} max {v[-1]}; above fair {sum(1 for x in v if x>mean10)}; values {v}')
print('  top 6:', [(u.split(':',1)[1], A[u], f'{B[u][1]:.4g}') for u in sorted(A, key=lambda u: -A[u])[:6]])
print('  bottom 4:', [(u.split(':',1)[1], A[u]) for u in sorted(A, key=lambda u: A[u])[:4]])
# TOP minus WORST per variant
var = sorted({u.rsplit(':', 2)[0] for u in A})
d = [A[v + ':TOP:WF'] - A[v + ':WORST:WF'] for v in var]
print(f'  TOP minus WORST per variant: mean {sum(d)/len(d):+.2f}; TOP>WORST {sum(1 for x in d if x>0)}, equal {sum(1 for x in d if x==0)}, TOP<WORST {sum(1 for x in d if x<0)}')
smallest = min(B.values(), key=lambda t: t[1])[1]
print(f'  family: smallest P_up {smallest:.6g}; Bonferroni 80 x = {min(1, 80*smallest):.6g}')

if ('A', 'MR7.PB') in T:
    P = {r['unit']: int(re.search(r'Powerball hits (\d+)', r['extra'][0]).group(1)) for r in T[('A', 'MR7.PB')]}
    BP = {}
    for r in T[('B', 'MR7.PB')]:
        m = re.match(num + r'\s+' + num, r['rest']); BP[r['unit']] = float(m.group(2))
    bt = lambda k: sum(math.comb(10, i) * 0.05 ** i * 0.95 ** (10 - i) for i in range(k, 11))
    bad = [(u, P[u], BP[u], bt(P[u])) for u in P if abs(bt(P[u]) - BP[u]) > 1e-6]
    print(f'MR7.PB: binomial tail recomputed for {len(P)} tracks; mismatches: {len(bad)}')
    for s in ('TOP', 'WORST'):
        v = sorted(P[u] for u in P if side(u) == s)
        print(f'  {s}: total hits {sum(v)} (fair {0.5*len(v):.1f}); distribution {dict((k, v.count(k)) for k in sorted(set(v)))}')
    print('  tracks with 2 or more hits:', [(u.split(':',1)[1], P[u]) for u in P if P[u] >= 2])
    sm = min(BP.values()); print(f'  family: smallest P_up {sm:.6g}; Bonferroni 80 x = {min(1, 80*sm):.6g}')

# MR5 mean ranks
for key in [k for k in T if k[0] == 'A' and k[1].startswith('MR5')]:
    mr = {r['unit']: float(re.search(r'favoured\) ' + num, r['extra'][0]).group(1)) for r in T[key]}
    fair = float(re.search(r'fair ' + num, T[key][0]['extra'][0]).group(1))
    v = sorted(mr.values())
    print(f'{key[1]}: 40 variants; fair {fair}; mean of the 40 mean ranks {sum(v)/len(v):.3f}; below fair (favoured the drawn numbers) {sum(1 for x in v if x<fair)}, above {sum(1 for x in v if x>fair)}; min {v[0]} max {v[-1]}')
    print('   best 5:', [(u.split(':',1)[1].replace(':WF',''), mr[u]) for u in sorted(mr, key=mr.get)[:5]])
    print('   worst 3:', [(u.split(':',1)[1].replace(':WF',''), mr[u]) for u in sorted(mr, key=mr.get)[-3:]])
# MR0 division wins
wins = {}
for r in T[('A', 'MR0')]:
    w = [int(x) for x in re.search(r'wins by division ([\d ]+)', r['extra'][0]).group(1).split()]
    wins[r['unit']] = w
nd = len(next(iter(wins.values())))
print('MR0: total wins by division over the 80 tracks:', [sum(w[i] for w in wins.values()) for i in range(nd)])
print('   tracks with any win:', sum(1 for w in wins.values() if sum(w)), 'of 80;  by side:', {s: sum(1 for u, w in wins.items() if sum(w) and side(u) == s) for s in ('TOP', 'WORST')})
print('   tracks with 2+ wins:', [(u.split(':',1)[1], w) for u, w in wins.items() if sum(w) >= 2])
