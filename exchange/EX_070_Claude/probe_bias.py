import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import reference_wave2 as R, probe_wave2 as P
from decimal import Decimal, getcontext
getcontext().prec = 40
# E_17's log-age sign over independent fair histories, and the covariance n*S_zy (Decimal; for scale only)
for (lo, hi, K, n, N) in ((1, 20, 1, 300, 200), (1, 35, 7, 300, 120)):
    sig, val = [], []
    for s in range(N):
        h = P.fair(n, lo, hi, K, f'bias{hi}:{s}')
        sig.append(R.e17_logage_sign(h, lo, hi, K)[1])
        a = R.log_age_coefficients(h, lo, hi)
        val.append(float(sum(Decimal(c) * Decimal(k).ln() for k, c in a.items())) / sum(R.exposures_by_age(h, lo, hi)[0].values()))
    m = sum(val) / N; sd = (sum((v - m) ** 2 for v in val) / (N - 1)) ** 0.5
    print(f'L={hi} K={K} W={n}: {N} independent fair histories, log-age sign +1 in {sum(x > 0 for x in sig)}, -1 in {sum(x < 0 for x in sig)}; '
          f'S_zy mean {m:+.5f}, sd {sd:.5f}, mean/se {m / (sd / N ** 0.5):+.2f}')
