import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R, probe_wave2 as P
from fractions import Fraction as Fr
def e19_pl(hist, low, high, K, T, c=100, d=20, dl=20):
    h, edges = R.binned_hazard(hist, low, high, K, c)
    W=len(hist)
    # per-label O and X by residue, from a per-draw age walk
    last={j:None for j in range(low,high+1)}
    O={j:[0]*T for j in last}; X={j:[Fr(0)]*T for j in last}
    for i,dr in enumerate(hist,1):
        s=set(dr)
        for j in last:
            if last[j] is not None:
                k=i-last[j]; X[j][k%T]+=h[R.bin_of(k,edges)]
                if j in s: O[j][k%T]+=1
        for j in s: last[j]=i
    Op=[sum(O[j][q] for j in O) for q in range(T)]; Xp=[sum(X[j][q] for j in X) for q in range(T)]
    phi=[(Op[q]+d)/(Xp[q]+d) for q in range(T)]
    G=R.projected_age(W,R.appearances(hist,low,high))
    phij={j:[(O[j][q]+dl*phi[q])/(X[j][q]+dl) for q in range(T)] for j in O}
    return {j:h[R.bin_of(g,edges)]*phij[j][g%T] for j,g in G.items()}, phi, phij
for name,rule in (('two-cycle 17',lambda i,prev,j:3.0 if (j==17 and i%2) else 1.0),('fair',lambda i,prev,j:1.0)):
    h=P.planted(433,1,35,7,name,rule)
    s,phi,phij=e19_pl(h,1,35,7,2)
    rank=sorted(s,key=lambda j:-s[j])
    G=R.projected_age(433,R.appearances(h,1,35))
    print(name,'pooled phi',[round(float(x),3) for x in phi],'label17 phi',[round(float(x),3) for x in phij[17]],
          'label17 G',G[17],'rank of 17:',rank.index(17)+1,
          'max |phi_j-1| over other labels',round(max(abs(float(x)-1) for j in phij if j!=17 for x in phij[j]),3))
# planted two-cycle: how often is 17 in the top 7 when the target is odd (favoured) over walk-forward targets?
h=P.planted(433,1,35,7,'two-cycle 17',lambda i,prev,j:3.0 if (j==17 and i%2) else 1.0)
hit=tot=0
for W in range(104,433):
    # target index W (0-based i=W) is favoured for 17 when W%2==1
    s,_,_=e19_pl(h[:W],1,35,7,2)
    top=sorted(s,key=lambda j:(-s[j],j))[:7]
    if W%2==1:
        tot+=1; hit+=17 in top
print('two-cycle 17: favoured targets',tot,'17 in E_19 per-label TOP7 at',hit)
def e19_norm(hist, low, high, K, T, c=100, d=20, dl=20):
    s, phi, phij = e19_pl(hist, low, high, K, T, c, d, dl)
    h, edges = R.binned_hazard(hist, low, high, K, c)
    # overall per-label ratio, same shrinkage: (sum O + dl)/(sum X + dl), recomputed from phij's parts is not
    # available, so recompute O and X totals
    last={j:None for j in range(low,high+1)}; O={j:0 for j in last}; X={j:Fr(0) for j in last}
    for i,dr in enumerate(hist,1):
        st=set(dr)
        for j in last:
            if last[j] is not None:
                k=i-last[j]; X[j]+=h[R.bin_of(k,edges)]; O[j]+= j in st
        for j in st: last[j]=i
    G=R.projected_age(len(hist),R.appearances(hist,low,high))
    return {j:h[R.bin_of(g,edges)]*phij[j][g%T]/((O[j]+dl)/(X[j]+dl)) for j,g in G.items()}
for label,fn in (('per-label',lambda hh:e19_pl(hh,1,35,7,2)[0]),('per-label, level divided out',lambda hh:e19_norm(hh,1,35,7,2))):
    fav=[0,0]; unf=[0,0]
    for W in range(104,433):
        s=fn(h[:W]); top=sorted(s,key=lambda j:(-s[j],j))[:7]
        (fav if W%2==1 else unf)[0]+=1; (fav if W%2==1 else unf)[1]+= 17 in top
    print(label,': 17 in TOP7 at favoured',fav[1],'of',fav[0],'; at unfavoured',unf[1],'of',unf[0])
