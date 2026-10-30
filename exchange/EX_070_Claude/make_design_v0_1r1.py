"""Design v0.1r1 from v0.1 by counted edits (Claude, 30 Oct 2026): W2-B01 (owner chose the faithful Method A
sign), W2-C01 (E_18's completed-gap fitting stated), W2-O01 (owner adopted the byte-reproducibility wording).
Usage: python3 -I make_design_v0_1r1.py V0_1 OUT"""
import hashlib, sys
src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '3192c255e0817fa139bf8d85d4762686c0888bc080c0a4e5cb60b038c4923c01'
t = raw.decode('ascii')
E = [
# 1 version
("**Version:** v0.1 DRAFT for the reviewer, 30 October 2026. Author: Claude. Ratifier: the project owner.",
 "**Version:** v0.1r1 DRAFT for the reviewer's focused RECHECK, 30 October 2026. It resolves EX_069's three findings: W2-B01 (E_17's slope variant is replaced by Method A's own log-age rule, decided exactly; owner decision W2-3), W2-C01 (E_18's fitting from completed gaps only, and its limits, are stated) and W2-O01 (the template finding is reworded as a byte-reproducibility rule; owner decision W2-7). Nothing else changes. Author: Claude. Ratifier: the project owner."),
# 2 plain English
("If recently drawn numbers come up more often (\"hot\") or less often, E_17 learns that from the data, including its direction, and ranks accordingly.",
 "If recently drawn numbers come up more often (\"hot\") or less often, E_17 learns that from the data, including its direction, and ranks accordingly. One variant is exactly your Method A's rule, using its own log of the age."),
# 3 censoring
("""- **The open stretch since the last appearance** is not a completed gap. It enters the hazard estimates only as at-risk exposures without an event (right-censored), and it is the predictor's input G_j.""",
 """- **The open stretch since the last appearance** is not a completed gap. It is every method's input G_j. How it enters each estimate differs:
  - **E_17 and E_19** estimate hazards from exposures (3.3), so the open stretch enters them as at-risk exposures without an event: proper right-censoring.
  - **E_18** fits its mixture weights from completed gaps only (4.4), so the open stretch does not enter the fit; it only says where the fitted hazard is read.
  - **E_2** estimates no hazard: its characteristic interval comes from completed gaps, and G_j is compared with it."""),
# 4 E_17 slope form
("""- **Slope (Method A's A3 predictor):** a least-squares line in the covariate z = H_k, the k-th harmonic number 1 + 1/2 + ... + 1/k, fitted over all exposures:

  beta = S_zy / S_zz,  and  s_j = ybar + beta (H_{G_j} - zbar)

  Here S_zy = sum of (z - zbar)(y - ybar) and S_zz = sum of (z - zbar)^2, over exposures; y is 1 for an event; zbar and ybar are the means. beta = 0 if S_zz = 0.
""",
 """- **Log-age sign (Method A's A3 predictor, exactly in its ranking; owner decision W2-3):** with n = sum of R_k exposures and e = sum of E_k events, the integers a_k = n E_k - e R_k (they sum to 0) give

  n S_zy = sum_k a_k ln k,  sigma = sign(n S_zy) in {+1, 0, -1},  and  s_j = sigma G_j

  Here S_zy = sum over exposures of (z - zbar)(y - ybar), with the covariate z = ln(age), as Method A has it; y is 1 for an event.
"""),
# 5 why paragraph
("""**Why the slope form is Method A's predictor, exactly in its ranking.** Method A fits a logistic regression of appearance on log(gap), with mild shrinkage of the slope towards 0, and ranks by the fitted chance at the projected age. Three facts make the exact form above rank the same way:
1. **Only the sign of the slope matters for the ranking.** The fitted chance is a strictly increasing (positive slope) or strictly decreasing (negative slope) function of the age. So the ranking is "longest absent first" or "most recently drawn first", and equal ages tie.
2. **Shrinkage towards 0 never changes that sign,** so a ridge penalty of any fixed size has no effect on the ranking. None is used.
3. **The logistic slope has the sign of S_zy.** With the intercept profiled out, the log-likelihood is concave in the slope, and its derivative at slope 0 is S_zy, the score statistic. So the maximum-likelihood slope has the sign of S_zy, which is the sign of beta.
""",
 """**Why this is Method A's predictor, exactly in its ranking.** Method A fits a logistic regression of appearance on log(gap), with mild shrinkage of the slope towards 0, and ranks by the fitted chance at the projected age. Three facts make sigma G_j rank the same way:
1. **Only the sign of the slope matters for the ranking.** The fitted chance is a strictly increasing (positive slope) or strictly decreasing (negative slope) function of the age. So the ranking is "longest absent first" or "most recently drawn first", and equal ages tie.
2. **Shrinkage towards 0 never changes that sign,** so a ridge penalty of any fixed size has no effect on the ranking. None is used.
3. **The logistic slope has the sign of S_zy, for the same covariate.** With the intercept profiled out, the log-likelihood is concave in the slope, and its derivative at slope 0 is S_zy, the score statistic. So the maximum-likelihood slope has the sign of S_zy (or is infinite with that sign, if the data separate).

**This needs Method A's own covariate.** v0.1 used the harmonic number H_k in place of ln k and claimed the same ranking. EX_069 (W2-B01) proved that false with an exact witness: another increasing transform of the age can reverse the sign. On fair invented draws, the two signs differed at 10 of 312 targets (section 8). The harmonic slope is withdrawn.

**How the sign is decided exactly.** sum_k a_k ln k = sum_p e_p ln p over the primes p dividing the ages, with integers e_p = sum_k a_k v_p(k) (v_p(k) is the power of p in k).
- **Bounds:** rational lower and upper bounds on each ln p come from ln p = a ln 2 + 2 atanh((m - 1)/(m + 1)), with p = 2^a m and 1 <= m < 2, and ln 2 = 2 atanh(1/3). The atanh series is summed for a fixed number of terms, and its tail is bounded by a geometric series.
- **The loop:** the number of terms doubles until the bounds on sum_p e_p ln p exclude 0.
- **It always ends.** The logs of distinct primes are linearly independent over the rationals (by unique factorisation), so sum_p e_p ln p is 0 only when every e_p is 0. The method then returns sigma = 0 without any bound.
- **The cost:** at most 0.007 s per target in the probes; 8 terms sufficed at every probed target.
- **The published scores** are the integers sigma G_j, exactly representable in float64. They are not Method A's fitted chances, which would need an iterative fit, but they rank identically.
"""),
# 6 the H_k paragraph
("""H_k replaces log k so that everything stays exact. H_k - ln k falls from 1 at k = 1 towards Euler's constant 0.577..., so the covariates differ by at most 0.43, mostly at age 1. The two signs can differ only when the trend is close to zero. When beta = 0, every label scores the same:""",
 """When sigma = 0, every label scores the same:"""),
# 7 E_18 fitting data
("- **The data:** j's completed gaps (all, or those with both ends inside the newest S draws) are binned with section 3.4's bins.",
 "- **The data:** j's completed gaps (all, or those with both ends inside the newest S draws) are binned with section 3.4's bins. Only completed gaps are used (W2-C01): this is a descriptive fit of the gaps seen, not a censored-likelihood fit."),
# 8 E_18 limitation
("- **Why four components:** with FAST, FAIR and REGULAR only, a label with rapid returns and long absences was not representable. SLOW was added, and the rapid-plus-absent probe then works (section 8).",
 """- **Why four components:** with FAST, FAIR and REGULAR only, a label with rapid returns and long absences was not representable. SLOW was added, and the rapid-plus-absent probe then works (section 8).
- **The limits of fitting completed gaps only** (W2-C01), stated and accepted for revision 1:
  - **A current long absence does not enter the fit.** A number in the middle of a long absence has no completed gap for it yet, so its fit leans, slightly, towards its shorter past gaps.
  - **Long gaps are under-represented.** A gap of length g fits within a span of S draws at only S - g of its possible positions. The windowed variants show this most: for POWERBALL with S = 104, a 40-draw gap carries about 0.6 of a 1-draw gap's chance of being counted. The effect is the same for every label, and it can move weight towards FAST and away from SLOW.
  - **A censored-likelihood fit,** which would use the open stretch and remove both effects, would be a separate variant with its own design review."""),
# 9 variants table
("| E_17 | `HAZARD_LOGSLOPE_V1` | slope on H_k, all exposures | 52 | Method A's predictor |",
 "| E_17 | `HAZARD_LOGAGE_SIGN_V1` | sign of the log-age trend, all exposures | 52 | Method A's predictor, exactly in its ranking |"),
# 10 relation
("- **E_17 `HAZARD_LOGSLOPE_V1` ranks purely by projected age:** longest absent first if beta > 0, most recently drawn first if beta < 0,",
 "- **E_17 `HAZARD_LOGAGE_SIGN_V1` ranks purely by projected age:** longest absent first if sigma = +1, most recently drawn first if sigma = -1,"),
("The tests check each exact relation (E_17's slope ranking against a pure age ordering;",
 "The tests check each exact relation (E_17's log-age ranking against a pure age ordering;"),
# 11 probes
("""- **E_17's slope on fair draws:**
  - over independent fair histories (W = 300), it was positive in 99 of 200 POWERBALL histories (mean -0.03 standard errors from 0) and 69 of 120 MAIN ones (mean +1.49 standard errors); no bias is evident;
  - its spread was about 0.0025 (POWERBALL) and 0.0053 (MAIN);
  - within one history, consecutive targets share their sign, because they share their draws.""",
 """- **E_17's log-age sign on fair draws:**
  - over independent fair histories (W = 300), it was +1 in 99 of 200 POWERBALL histories and 69 of 120 MAIN ones (the mean of S_zy at -0.46 and +1.25 standard errors from 0); no bias is evident;
  - within one history, consecutive targets share their sign, because they share their draws.
- **The exact sign rule** (W2-B01):
  - on EX_069's witness history, it gives -1 (60-digit decimal value of n S_zy: -2798.499...), while v0.1's harmonic slope was positive;
  - over 312 targets of three invented histories (all three barrels), it agreed with a 60-digit decimal computation, and with the second route of section 10, every time;
  - the harmonic slope's sign differed from it at 10 of the 312."""),
("- **Speed,** one target at the full invented history, exact fractions: the slowest variants (E_18's) took about 0.2 s for Powerball MAIN (433 draws), 0.3 s for POWERBALL and 0.5 s for Oz Lotto MAIN (218 draws). All others took 0.02 s or less.",
 "- **Speed,** one target at the full invented history, exact fractions: the slowest variants (E_18's) took between 0.1 and 0.5 s per target across runs (Powerball 433 draws, Oz Lotto 218). All others took 0.02 s or less."),
("| Clustering: a number drawn last draw is 1.6x as likely | E_17's slope -0.036 (fair spread about 0.005); age-1 bin hazard 0.272 against about 0.19 |",
 "| Clustering: a number drawn last draw is 1.6x as likely | E_17's log-age sign -1 (n S_zy about -5.75 million; over 40 fair histories of the same size its standard deviation was about 0.65 million); age-1 bin hazard 0.272 against about 0.19 |"),
# 12 worked example
("""   - beta = 362495/1270704 = 0.2853 > 0, so the ranking is longest absent first;
   - label 9 is first, at 0.4025, then labels 2 and 10, tied (age 5).""",
 """   - a_k for ages 1 to 7: -308, 44, -48, 8, -17, 254, 67 (n = 81 exposures, e = 14 events);
   - the prime exponents are e_2 = 314, e_3 = 206, e_5 = -17 and e_7 = 67, and n S_zy = 546.98 > 0, so sigma = +1: longest absent first;
   - the scores are the projected ages: label 9 first (6), then labels 2 and 10, tied (5)."""),
# 13 verify
("- **E_17:** bin sums from the per-age counts, against direct per-bin counting; S_zy and S_zz by the centred two-pass form, against the raw-sum form. The ranking is checked to be the pure age ordering in the direction of beta's sign.",
 "- **E_17:** bin sums from the per-age counts, against direct per-bin counting. The log-age sign by the prime-exponent route, against bounds on each ln k taken directly, without factorising; the two must agree. The ranking is checked to be the pure age ordering in the direction of sigma."),
# 14 template finding 1 + new 5
("""This design found four things for the template. Draft 3 would add them, in the code package, as "things that bite" and checklist items:
1. **No iterative floating-point fits in published values.** Logistic regression, EM and the like, in floating point, break the Windows/Linux byte identity (library functions such as `log`, `exp` and `pow` may round differently). Prefer an exact closed form, an exact finite search (E_18's 15 supports) or an exact certificate (E_3/E_4's alternation, E_18's KKT check).""",
 """This design found five things for the template. Draft 3 would add them, in the code package, as "things that bite" and checklist items:
1. **Published values must be byte-identical on Windows and Linux** (owner decision W2-7, after W2-O01). Exact arithmetic is preferred: an exact closed form, an exact finite search (E_18's 15 supports) or an exact certificate (E_3/E_4's alternation, E_18's KKT check, E_17's certified sign). An iterative floating-point fit is allowed only with objective proof of cross-platform byte identity and canonical output and tie rules. Library functions such as `log`, `exp` and `pow` may round differently between platforms."""),
("""4. **Divide out what another method already measures** before claiming a new effect (E_19 divides out the age trend and the label's level), and check with a planted effect that the claim survives.""",
 """4. **Divide out what another method already measures** before claiming a new effect (E_19 divides out the age trend and the label's level), and check with a planted effect that the claim survives.
5. **Changing a covariate is not ranking-preserving** (W2-B01). Replacing a model's covariate by another increasing transform can reverse the fitted direction, and so the ranking. Claim that two forms are equivalent only with a proof, and search for a witness."""),
# 14b worked-example heading and helper contents
("3. **E_17, slope:**", "3. **E_17, log-age sign:**"),
("  - harmonic numbers.", "  - the certified sign of an integer combination of logs (4.2), by both routes."),
# 15 decisions
("""- **W2-3 (RECOMMENDED): Method A becomes E_17 as in section 4.2, and its diagnostics come later.**""",
 """- **W2-3 (OWNER-DECIDED 30 October 2026, after EX_069): Method A becomes E_17 with Method A's own log-age rule (section 4.2), and its diagnostics come later.** The owner chose the faithful rule (EX_069's choice A) over keeping v0.1's harmonic slope as a renamed surrogate, or both."""),
("""  - **The options:**
    - (b) build the diagnostics in wave 2, which means settling R-004 now;
    - (c) only the logistic slope, without the binned variants.""",
 """  - **The options still open on the diagnostics' timing:** (b) build them in wave 2, which means settling R-004 now."""),
("- **W2-7 (RECOMMENDED): the template's draft 3** with the four findings of section 12, in the code package.",
 "- **W2-7 (OWNER-DECIDED 30 October 2026, after EX_069): the template's draft 3** with the five findings of section 12, in the code package, finding 1 in the byte-reproducibility wording of W2-O01."),
]
for o, n in E:
    c = t.count(o)
    assert c == 1, (c, o[:70])
    assert n.isascii(), o[:40]
    t = t.replace(o, n)
open(out, 'wb').write(t.encode('ascii'))
print(len(E), 'edits;', out, hashlib.sha256(t.encode()).hexdigest())
