import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R, probe_wave2 as P
from fractions import Fraction as Fr
for (lo,hi,K,n,N) in ((1,20,1,300,200),(1,35,7,300,120)):
    bs=[R.e17_logslope(P.fair(n,lo,hi,K,f'bias{hi}:{s}'),lo,hi,K)[1] for s in range(N)]
    pos=sum(b>0 for b in bs); mean=sum(bs)/len(bs)
    sd=(sum((b-mean)**2 for b in bs)/(len(bs)-1))**0.5 if False else (sum(float(b-mean)**2 for b in bs)/(len(bs)-1))**0.5
    print(f'L={hi} K={K} W={n}: {N} independent fair histories, beta>0 in {pos}, mean beta {float(mean):+.5f}, sd {sd:.5f}, mean/se {float(mean)/(sd/len(bs)**0.5):+.2f}')
