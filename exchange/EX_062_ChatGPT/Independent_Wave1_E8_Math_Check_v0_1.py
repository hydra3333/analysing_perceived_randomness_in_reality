"""Independent synthetic-only check of EX_061 wave-1 E8 equations.
Not project code. Inputs are invented complete sets with no real lottery data.
"""
from fractions import Fraction as F
from itertools import combinations, product
from reference_wave1_examples import e8


def alternate_e8(draws, labels, K, P):
    labels = tuple(labels)
    n = len(draws) // P
    assert n >= 2 and P >= 2 and K < len(labels)
    blocks = [draws[len(draws)-n*P+i*P:len(draws)-n*P+(i+1)*P] for i in range(n)]
    r = F(K, len(labels))
    means, newest, excesses = {}, {}, []
    for j in labels:
        xs = [sum(j in d for d in block) for block in blocks]  # integer period counts
        total = sum(xs)
        m = F(total, n*P)
        # One-pass integer-count variance, independent of the two-pass rate method.
        v = (F(sum(x*x for x in xs), 1)-F(total*total, n))/F(P*P*(n-1))
        t = (v-(m*(1-m)+v/n)/P)*F(P,P-1)
        means[j] = m
        newest[j] = F(xs[-1],P)
        excesses.append(t)
    t = min(max(F(0), sum(excesses,F(0))/len(labels)), r*(1-r))
    w = F(P)*t / ((P-1)*t+r*(1-r))
    scores = {j:w*newest[j]+(1-w)*means[j] for j in labels}
    assert sum(scores.values(),F(0)) == K
    assert 0 <= w <= 1
    assert all(0 <= s <= 1 for s in scores.values())
    return t,w,scores


def main():
    labels=tuple(range(1,6))
    selections=list(map(frozenset,combinations(labels,2)))
    count=0
    for draws in product(selections,repeat=4):
        got=alternate_e8(draws,labels,2,2)
        expected=e8(draws,labels,2,2)
        assert got==expected,(draws,got,expected)
        count+=1
    cap=(frozenset([2,4]),)*3 + (frozenset([1,2]),frozenset([1,3]),frozenset([1,3]))
    got=alternate_e8(cap,range(1,5),2,2)
    assert got==(F(1,4),F(1),{1:F(1),2:F(0),3:F(1),4:F(0)}),got
    print(f'PASS: {count} exhaustive 4-draw synthetic E8 cases, plus independent cap case.')
    print('E8 cap case exact:',got)

if __name__=='__main__':main()
