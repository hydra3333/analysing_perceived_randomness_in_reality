import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R, probe_wave2 as P
from fractions import Fraction as Fr
# 1. linear independence of the four components' bin vectors (exact rank)
def rank(M):
    M=[r[:] for r in M]; rk=0; cols=len(M[0])
    for c in range(cols):
        piv=next((i for i in range(rk,len(M)) if M[i][c]!=0),None)
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for i in range(len(M)):
            if i!=rk and M[i][c]!=0:
                f=M[i][c]/M[rk][c]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        rk+=1
    return rk
for L,K in ((35,7),(20,1),(47,7),(10,2)):
    e=R.bin_edges(L,K); Pm=[R.bin_probs(S,e) for S in R.components(L,K)]
    print(f'L={L} K={K}: {len(e)+1} bins, rank of the 4 component bin vectors = {rank(Pm)}; each sums to 1: {all(sum(p)==1 for p in Pm)}')
# 2. E_18 prior-strength sensitivity with the final 4-law library
h=P.fair(433,1,35,7,'overlap')
def top(s): return set(sorted(s,key=lambda j:(-s[j],j))[:7])
acc={2:0,40:0}; n=0
for W in range(208,434,9):
    t10=top(R.e18(h[:W],1,35,7,10)[0]); n+=1
    for c in acc: acc[c]+=len(t10&top(R.e18(h[:W],1,35,7,c)[0]))
print('E_18 ALL: TOP7 shared with c=10:', {c:round(v/n,2) for c,v in acc.items()}, 'over', n, 'targets')
# 3. E_19 planted 2-cycle with the final reference function
hc=P.planted(433,1,35,7,'two-cycle 17',lambda i,prev,j:3.0 if (j==17 and i%2) else 1.0)
fav=[0,0];unf=[0,0]
for W in range(104,433):
    s=R.e19(hc[:W],1,35,7,2)[0]; tp=sorted(s,key=lambda j:(-s[j],j))[:7]
    b=fav if W%2==1 else unf; b[0]+=1; b[1]+=17 in tp
print('E_19 T2 final: 17 in TOP7 favoured',fav[1],'of',fav[0],'; unfavoured',unf[1],'of',unf[0])
# 4. E_17 slope spread on fair MAIN (independent histories) vs clustering
