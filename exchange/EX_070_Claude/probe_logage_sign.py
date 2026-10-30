"""E_17's log-age sign rule (W2-B01): the witness, agreement with 60-digit decimals, speed, and how often v0.1's
harmonic slope disagreed. Invented draws only."""
import sys, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from decimal import Decimal, getcontext
import reference_wave2 as R, probe_wave2 as P
getcontext().prec = 60
dec = lambda a: sum(Decimal(c) * Decimal(k).ln() for k, c in a.items())
wa = R.log_age_coefficients(R.witness_history(), 1, 35)
print('EX_069 witness: certified log-age sign', R.certified_sign(R.prime_exponents(wa)), '; 60-digit n*S_zy', dec(wa),
      '; harmonic slope positive:', R.harmonic_slope_beta(R.witness_history(), 1, 35) > 0)
worst = 0; n = 0; dis = 0
for (lo, hi, K, W) in ((1, 35, 7, 433), (1, 20, 1, 433), (1, 47, 7, 218)):
    h = P.fair(W, lo, hi, K, f'logsign{hi}')
    for w in range(52, W + 1, 3):
        a = R.log_age_coefficients(h[:w], lo, hi)
        t0 = time.perf_counter(); s1 = R.certified_sign(R.prime_exponents(a)); worst = max(worst, time.perf_counter() - t0)
        s2 = R.certified_sign({k: c for k, c in a.items() if c})
        d = dec(a); assert s1 == s2 == (d > 0) - (d < 0), (hi, w)
        b = R.harmonic_slope_beta(h[:w], lo, hi); dis += ((b > 0) - (b < 0)) != s1; n += 1
print(f'{n} targets over three barrels: the two certified routes and the 60-digit decimal sign always agree; '
      f'slowest certification {worst:.3f} s; the harmonic slope sign differed at {dis} of {n}')
