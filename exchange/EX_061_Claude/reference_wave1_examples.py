"""Exact reference formulas for wave 1 (E_7, E_8, E_9, E_10), for the design note's worked examples.
Draws are given oldest first; the newest draw has age 0. Labels low..high, K drawn per draw."""
from fractions import Fraction as F

def counts(draws, labels, last=None):
    use = draws if last is None else draws[-last:]
    return {j: sum(1 for d in use if j in d) for j in labels}

def e7(draws, labels, K, M, c):            # M None = full history
    use = draws if M is None else draws[-M:]
    r, k = F(K, len(labels)), counts(use, labels)
    return {j: (c * r + k[j]) / (c + len(use)) for j in labels}

def e9(draws, labels, lam):
    n = len(draws)
    return {j: sum((lam ** (n - 1 - i) for i, d in enumerate(draws) if j in d), F(0)) for j in labels}

def e10(draws, labels, S, Lw):              # Lw None = all eligible draws
    use = draws if Lw is None else draws[-Lw:]
    kS, kL = counts(use, labels, S), counts(use, labels)
    return {j: F(kS[j], S) - F(kL[j] - kS[j], len(use) - S) for j in labels}

def e8(draws, labels, K, P):
    L, r = len(labels), F(K, len(labels))
    n = len(draws) // P
    blocks = [draws[len(draws) - (n - b) * P: len(draws) - (n - b - 1) * P] for b in range(n)]   # oldest .. newest
    m, latest, t = {}, {}, []
    for j in labels:
        p = [F(sum(1 for d in bl if j in d), P) for bl in blocks]
        mj = sum(p, F(0)) / n
        V = sum(((x - mj) ** 2 for x in p), F(0)) / (n - 1)
        t.append((V - (mj * (1 - mj) + V / n) / P) * F(P, P - 1))
        m[j], latest[j] = mj, p[-1]
    t2 = min(max(F(0), sum(t, F(0)) / L), r * (1 - r))
    w = (P * t2) / ((P - 1) * t2 + r * (1 - r))
    return t2, w, {j: w * latest[j] + (1 - w) * m[j] for j in labels}

if __name__ == '__main__':
    labels, K = range(1, 6), 2
    ex = [{1, 2}, {1, 3}, {2, 4}, {1, 5}]
    show = lambda d: ', '.join(f'{j}: {v}' for j, v in d.items())
    print('E_7 M=2 c=2 :', show(e7(ex, labels, K, 2, 2)), '| sum', sum(e7(ex, labels, K, 2, 2).values()))
    print('E_7 full c=2:', show(e7(ex, labels, K, None, 2)))
    print('E_9 lam=1/2 :', show(e9(ex, labels, F(1, 2))))
    print('E_10 S=2 L=4:', show(e10(ex, labels, 2, 4)))
    t2, w, s = e8(ex, labels, K, 2); print('E_8 P=2     : tau2', t2, 'w', w, '|', show(s), '| sum', sum(s.values()))
    ex2 = [{1, 2}, {3, 4}, {1, 2}, {3, 4}, {1, 5}, {1, 5}, {1, 3}, {1, 2}]
    t2, w, s = e8(ex2, labels, K, 2); print('E_8 ex2 P=2 : tau2', t2, 'w', w, '|', show(s), '| sum', sum(s.values()))
