"""Two figures for design v0.1r1: the series terms the certified sign needed, and the fair spread of n*S_zy at 433 MAIN draws."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from decimal import Decimal, getcontext
import reference_wave2 as R, probe_wave2 as P
getcontext().prec = 40
calls = []
orig = R.ln_bounds
R.ln_bounds = lambda k, terms: (calls.append(terms), orig(k, terms))[1]
for (lo, hi, K, W) in ((1, 35, 7, 433), (1, 20, 1, 433), (1, 47, 7, 218)):
    h = P.fair(W, lo, hi, K, f'logsign{hi}')
    for w in range(52, W + 1, 3):
        R.certified_sign(R.prime_exponents(R.log_age_coefficients(h[:w], lo, hi)))
print('largest number of series terms used by the certified sign over the 312 targets:', max(calls))
R.ln_bounds = orig
v = []
for s in range(40):
    h = P.fair(433, 1, 35, 7, f'spread:{s}')
    v.append(float(sum(Decimal(c) * Decimal(k).ln() for k, c in R.log_age_coefficients(h, 1, 35).items())))
m = sum(v) / len(v); sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5
print(f'n*S_zy over 40 independent fair MAIN histories of 433 draws: mean {m:+.0f}, standard deviation {sd:.0f}')
