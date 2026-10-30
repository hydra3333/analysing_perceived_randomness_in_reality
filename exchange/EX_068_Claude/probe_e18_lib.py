import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R, probe_wave2 as P
from fractions import Fraction as Fr
def lib4(L,K):
    r=Fr(K,L)
    return (lambda G:R.surv_geom(2*r,G), lambda G:R.surv_geom(r,G), lambda G:R.surv_geom(r/2,G), lambda G:R.surv_nb2(2*r,G))
def e18x(hist,low,high,K,c,window=None,lib=lib4):
    L=high-low+1; W=len(hist); edges=R.bin_edges(L,K); comps=lib(L,K)
    P_=[R.bin_probs(S,edges) for S in comps]; Pf=P_[1]
    app=R.appearances(hist,low,high); gaps=R.gaps_in_window(app,W,window); G=R.projected_age(W,app)
    out={};ws={}
    for j in app:
        o=[0]*len(Pf)
        for x in gaps[j]: o[R.bin_of(x,edges)]+=1
        q=[(o[b]+c*Pf[b])/(len(gaps[j])+c) for b in range(len(Pf))]
        w=R.fit_weights(q,P_,Pf); g=G[j]
        out[j]=sum(w[i]*(comps[i](g)-comps[i](g+1)) for i in range(len(comps)))/sum(w[i]*comps[i](g) for i in range(len(comps))); ws[j]=w
    return out,ws
def last_age(prev,j):
    for a,d in enumerate(reversed(prev),1):
        if j in d: return a
    return None
cases={'rhythm (x4 at age 5, x0.25 otherwise)':(lambda i,prev,j:(4.0 if last_age(prev,j)==5 else 0.25) if j==5 else 1.0, lambda G:G==5),
       'rapid+absent (x2.5 at ages 1-2, x0.4 later)':(lambda i,prev,j:((2.5 if (last_age(prev,j) or 99)<=2 else 0.4) if j==5 else 1.0), lambda G:G<=2)}
for name,(rule,favoured) in cases.items():
    h=P.planted(433,1,35,7,name,rule)
    fav=[0,0];unf=[0,0]
    for W in range(104,433,2):
        s,w=e18x(h[:W],1,35,7,10)
        G=R.projected_age(W,R.appearances(h[:W],1,35))[5]
        top=sorted(s,key=lambda j:(-s[j],j))[:7]
        b=fav if favoured(G) else unf; b[0]+=1; b[1]+=5 in top
    print(name,': label 5 in E_18 TOP7 when favoured',fav[1],'of',fav[0],'; otherwise',unf[1],'of',unf[0],'; weights FAST FAIR SLOW REGULAR',[round(float(x),3) for x in w[5]])
hf=P.fair(433,1,35,7,'fairprobe'); ws=[]
for W in range(104,434,22):
    w=e18x(hf[:W],1,35,7,10)[1]; ws.append(sum(1-x[1] for x in w.values())/35)
print('fair MAIN: mean non-FAIR weight per target, min',round(float(min(ws)),3),'max',round(float(max(ws)),3))
