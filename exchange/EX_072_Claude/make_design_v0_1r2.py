"""Design v0.1r2 from v0.1r1 by counted edits (Claude, 30 Oct 2026): W2R1-C01 (verify()'s second route gets an
independent exact-zero test and a refusal cap), W2R1-C02 (the stale W2-3 option relabelled; documentary FIX AND
PROCEED) and W2R1-O01 (the survival-fit sentence made precise). Usage: python3 -I make_design_v0_1r2.py V0_1R1 OUT"""
import hashlib, sys
src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '2b832830a4489cc1fd742e1eb0042571b521e7decbdbfbb963b4e97eea06e4b0'
t = raw.decode('ascii')
E = [
("**Version:** v0.1r1 DRAFT for the reviewer's focused RECHECK, 30 October 2026. It resolves EX_069's three findings:",
 "**Version:** v0.1r2 DRAFT for the reviewer's focused RECHECK, 30 October 2026. It resolves EX_071's findings: W2R1-C01 (verify()'s second sign route gets an independent exact-zero test and a refusal cap; section 10), W2R1-C02 (a stale option line in W2-3 relabelled) and W2R1-O01 (section 4.4's survival-fit sentence made precise). Nothing else changes. v0.1r1 resolved EX_069's three findings:"),
("- **The loop:** the number of terms doubles until the bounds on sum_p e_p ln p exclude 0.",
 "- **The loop:** the number of terms doubles until the bounds on sum_p e_p ln p exclude 0. A cap of 1,024 terms is a defensive limit (8 always sufficed in the probes): reaching it is refused as an error, never guessed."),
("  - **A censored-likelihood fit,** which would use the open stretch and remove both effects, would be a separate variant with its own design review.",
 "  - **A future survival likelihood** handling right censoring and window selection (the left-boundary and ascertainment effects of counting only gaps inside a span) could address these effects. It would be a separate variant with its own design review."),
("- **E_17:** bin sums from the per-age counts, against direct per-bin counting. The log-age sign by the prime-exponent route, against bounds on each ln k taken directly, without factorising; the two must agree. The ranking is checked to be the pure age ordering in the direction of sigma.",
 """- **E_17:** bin sums from the per-age counts, against direct per-bin counting. The ranking is checked to be the pure age ordering in the direction of sigma. The log-age sign by two routes, which must agree:
  - **Route 1 (the method):** prime exponents by trial division, then bounds on each ln p (section 4.2). An empty exponent map gives sigma = 0 exactly.
  - **Route 2 (verify()), with its own exact-zero test** (W2R1-C01): the prime exponents are recomputed independently, from a smallest-prime-factor sieve. If they all vanish, sigma = 0 exactly. Otherwise the value is not 0, and bounds on each ln k taken directly, without factorising, must exclude 0. That loop therefore ends; the same 1,024-term cap refuses as an error.
  - **Why a zero test is needed:** a direct interval can never exclude 0 when the value is exactly 0. EX_071's eight-draw witness (2 labels, 1 per draw: {1}, {1}, {2}, {2}, {1}, {1}, {1}, {2}) has a_k = 6, -12, 0, 6 at ages 1 to 4. Then 6 ln 1 - 12 ln 2 + 6 ln 4 = 0, while every direct interval straddles 0.
  - **The tests:** that zero case (both routes give 0, and bounds alone are refused at the cap), and nonzero agreement in both signs (EX_069's witness, -1; this note's worked example, +1)."""),
("  - **The options still open on the diagnostics' timing:** (b) build them in wave 2, which means settling R-004 now.",
 "  - **Not selected under owner decision W2-3:** building the diagnostics in wave 2. It would need a new owner decision, and settling R-004 first."),
("  - the worked examples and the bins of the three real barrels;",
 "  - the worked examples and the bins of the three real barrels;\n  - the log-age sign's zero case and its two-route agreement in both signs (section 10);"),
]
for o, n in E:
    c = t.count(o)
    assert c == 1, (c, o[:70])
    assert n.isascii(), o[:40]
    t = t.replace(o, n)
open(out, 'wb').write(t.encode('ascii'))
print(len(E), 'edits;', out, hashlib.sha256(t.encode()).hexdigest())
