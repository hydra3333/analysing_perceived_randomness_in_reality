import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R, probe_wave2 as P
def last_age(prev,j):
    for a,d in enumerate(reversed(prev),1):
        if j in d: return a
    return None
h=P.planted(433,1,35,7,'rhythm (x4 at age 5, x0.25 otherwise)',lambda i,prev,j:(4.0 if last_age(prev,j)==5 else 0.25) if j==5 else 1.0)
for stat,n in (('mean',None),('median',None),('mean',8)):
    fav=[0,0];unf=[0,0]
    for W in range(104,433):
        s=R.e2(h[:W],1,35,7,stat,n); G=R.projected_age(W,R.appearances(h[:W],1,35))[5]
        top=sorted(s,key=lambda j:(-s[j],j))[:7]; b=fav if G==5 else unf; b[0]+=1; b[1]+=5 in top
    print(f'E_2 {stat}{"" if n is None else " last "+str(n)}: label 5 in TOP7 when its projected age is 5: {fav[1]} of {fav[0]}; otherwise {unf[1]} of {unf[0]}')
