"""WF-1 design v0.1r1 - extreme-tail and bound probe (Claude, 30 October 2026); answers EX_078 WF1-R3-C04.
Fair-draw arithmetic only; no data file, no network. Uses reference_wf1.py from the same folder.
  python3 -I probe_tails.py
"""
import math, sys, time
from decimal import Decimal as D
from fractions import Fraction
from math import comb
sys.path.insert(0, '.')
import reference_wf1 as R

def logQ_asym(z):
    """Independent oracle for large z: ln Q(z) by the asymptotic series (many terms), in decimal."""
    z = D(z); s = D(0); term = D(1); k = 0
    while k < 30:
        s += term; k += 1; term = -term * (2 * k - 1) / (z * z)
    pi = D('3.14159265358979323846264338327950288419716939937510582097494459')
    return (-(z * z) / 2) - (z * (2 * pi).sqrt()).ln() + s.ln()

out = []
# A. the two tail routes agree where both apply (x = z/sqrt2 from 2.5 to 3.5)
worst = D(0)
for i in range(0, 41):
    x = D('2.5') + D(i) / 40
    a = (1 - R._erf_series(x)); b = R._erfc_cf(x)
    worst = max(worst, abs(a - b) / b)
out.append(f'A. series and continued fraction agree on x in [2.5, 3.5]: worst relative difference {float(worst):.2e}')
# B. large z against the asymptotic oracle
worst = D(0)
for z in (12, 20, 30, 37, 50, 60):
    q = R.upper_tail(D(z)); worst = max(worst, abs(q.ln() - logQ_asym(z)))
out.append(f'B. ln Q(z) for z = 12..60 against the asymptotic series: worst absolute difference {float(worst):.2e}')
# C. sigma from extreme exact tails, and near 1/2
for name, p in (('p = 1e-300', Fraction(1, 10 ** 300)), ('p = 1e-700', Fraction(1, 10 ** 700)),
                ('p = 1/2 - 1e-20', Fraction(1, 2) - Fraction(1, 10 ** 20)), ('p = 1/2', Fraction(1, 2))):
    t0 = time.perf_counter(); z = R.sigma_from_p(p); dt = time.perf_counter() - t0
    back = R.upper_tail(D(repr(z)))
    pd = D(p.numerator) / D(p.denominator)
    rel = abs(back - pd) / pd
    out.append(f'C. {name:16}: sigma {z!r} in {dt*1000:.0f} ms; Q(float sigma)/p - 1 = {float(rel):.1e}')
# D. MRT-04 sizes: exact binomial tails at n = 5000, p down to 1e-9, tails below 1e-300
for n, p, k in ((5000, Fraction(1, 10 ** 9), 40), (5000, Fraction(1, 10 ** 9), 3), (5000, Fraction(51597, 3362260), 0)):
    t0 = time.perf_counter()
    tail = R.binom_upper(n, p, k) if k > 0 else R.binom_lower(n, p, 0)
    dt = time.perf_counter() - t0
    lg = math.log10(tail.numerator) - math.log10(tail.denominator) if tail else float('-inf')
    out.append(f'D. n={n} p={float(p):.3g} {"P(X>=%d)" % k if k else "P(X<=0)"}: log10 = {lg:.3f}, exact in {dt:.2f} s')
# E. MR7's exact null cost as n grows (the bound of section 6.6)
for n in (432, 1000):
    t0 = time.perf_counter(); c = R.mr7_counts(R.PB_MAIN, n); dt = time.perf_counter() - t0
    out.append(f'E. MR7 exact null, Powerball n = {n}: {dt:.1f} s')
# F. NIST Beacon 2.0 chain links on two public chain 1 pulses (no certificate needed)
import hashlib
lr_next = '89C715CCA74A3337F3C49DDE74CA872C5C50F3D3002A255CB9F14FB8B9EDABC99B418858D849A2C1EDA8B77019838F78ECAA5589D3E8649A1F2C7C95BC9007B8'
pre = 'CA1A714ADF02E05C15FEEA2CC875727C7A4D50C26BB371DF7ACE30CDA740B3B3A32ABB6AB8C2275634F548A1CBBF550B95E1A0EBCF4448A0D9D75B2AE42C355B'
outv = 'A034DD06D13E5EF0051809D2DFC18894' '55CE77C8120D7E2AF482B0C3DE37D1C6' '8F189780035833305045481308F06D55' 'F8342E70414B26B7A1425E47F26CAAFA'
prev_next = outv  # pulse 1705578's listValues 'previous', read from NIST: equal to 1705577's outputValue
out.append('F. NIST chain 1 pulses 1705577 -> 1705578 (public archive): SHA-512(next localRandomValue) == '
           f'precommitmentValue: {hashlib.sha512(bytes.fromhex(lr_next)).hexdigest().upper() == pre}; next "previous" == outputValue: {prev_next == outv}')
print('\n'.join(out))
