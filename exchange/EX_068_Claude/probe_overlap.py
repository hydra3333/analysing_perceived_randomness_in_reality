import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R, probe_wave2 as P
from collections import Counter
h=P.fair(433,1,35,7,'overlap')
def e1(hh,lo,hi,K):
    c=Counter(x for d in hh for x in d); return {j:c[j] for j in range(lo,hi+1)}
V=dict(P.VARIANTS); V['E1']=e1
def top(s): return set(sorted(s,key=lambda j:(-s[j],j))[:7])
pairs=[('E17_BINS_C100','E19_T2'),('E17_BINS_C100','E17_LOGSLOPE'),('E2_MEAN','E2_MEDIAN'),('E2_MEAN','E2_MEAN_LAST8'),
       ('E18_C10','E18_W208_C10'),('E18_W208_C10','E18_W104_C10'),('E18_C10','E17_BINS_C100'),('E2_MEAN','E17_BINS_C100'),('E1','E2_MEAN'),('E1','E18_C10'),('E19_T2','E19_T3')]
acc={p:0 for p in pairs}; n=0
for W in range(208,434,9):
    tops={v:top(V[v](h[:W],1,35,7)) for v in set(x for p in pairs for x in p)}
    n+=1
    for a,b in pairs: acc[(a,b)]+=len(tops[a]&tops[b])
for (a,b),s in acc.items(): print(f'{a} vs {b}: mean TOP-7 overlap {s/n:.2f} of 7 over {n} targets (fair expectation 1.40)')
