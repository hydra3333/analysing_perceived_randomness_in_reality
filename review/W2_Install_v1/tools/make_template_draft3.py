"""The new-method template's draft 3 from the installed draft 2, by counted edits (Claude, 30 Oct 2026).

Draft 3 adds the wave 2 findings: design note v0.1r2 section 12 (findings 1 to 5, finding 1 in the
byte-reproducibility wording of W2-O01, owner decision W2-7), the termination lesson of EX_071 (W2R1-C01) and the
code round's note on hand-written test expectations. Only README.md and METHOD_SPECIFICATION_TEMPLATE.md change;
the code skeletons are unchanged from draft 2.
Usage: python3 -I make_template_draft3.py README_DRAFT2 SPEC_DRAFT2 OUTDIR
"""
import hashlib, sys
from pathlib import Path

readme, spec, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PIN = {readme: '91eca77e9b3e0ec46d8ef2ae4186c7035f97f0caddbdde816b42e44470764b68', spec: '759ad3a0151e7292a45abfc0ea8b8b1f9ba70210511b19ebf38e5be7425a31c3'}
for p, h in PIN.items():
    assert hashlib.sha256(p.read_bytes()).hexdigest() == h, p

R = [
("# New-method template (draft 2)", "# New-method template (draft 3)"),
("**Status:** DRAFT 2, 30 October 2026, by Claude. Draft 1 was written with E_6; draft 2 adds what E_3 and E_4 taught (a shared helper, scores only, a minimum history) and what the design of wave 1 (E_7, E_8, E_9, E_10) found. It is reviewed with wave 1's design.",
 "**Status:** DRAFT 3, 30 October 2026, by Claude. Draft 1 was written with E_6; draft 2 added what E_3 and E_4 taught (a shared helper, scores only, a minimum history) and what the design of wave 1 (E_7, E_8, E_9, E_10) found; draft 3 adds what wave 2 (E_2, E_17, E_18, E_19) found in its design reviews and code (owner decision W2-7). The code skeletons are unchanged from draft 2. It is reviewed with wave 2's code."),
("put it in one module in `src/methods/_common/`, with its own test module, and keep only each method's own rule in its folder.",
 "put it in one module in `src/methods/_common/`, with its own test module, and keep only each method's own rule in its folder (wave 2: gaps between appearances)."),
("- **Exactness:** prefer exact arithmetic (`fractions.Fraction`, integers). If floats are unavoidable, say in the specification why the result is the same on Windows and Linux (no `pow`, `exp`, `log` or summation-order differences), or how the method copes with a last-bit difference.",
 "- **Published values must be byte-identical on Windows and Linux** (owner decision W2-7). Prefer exact arithmetic (`fractions.Fraction`, integers): an exact closed form, an exact finite search (E_18 tries all 15 supports of its fit) or an exact certificate (E_3/E_4's alternation, E_18's optimality conditions, E_17's certified sign). An iterative floating-point fit is allowed only with objective proof of cross-platform byte identity and canonical output and tie rules. Library functions such as `pow`, `exp` and `log` may round differently between platforms, and summation order matters."),
("- **Scores only** (E_3, E_4, E_9, E_10):", "- **Scores only** (E_3, E_4, E_9, E_10, E_2, E_17, E_18, E_19):"),
("## Things that bite (learned on E_6, E_3/E_4 and wave 1)", "## Things that bite (learned on E_6, E_3/E_4, wave 1 and wave 2)"),
("- **Compute every worked example with a tool.** The E_3/E_4 draft had two hand-worked values wrong. Ship the reference script with the specification.",
 "- **Compute every worked example with a tool,** including the expected values inside tests. The E_3/E_4 draft had two hand-worked values wrong, and so did wave 2's first helper tests (a count of events, and a bin edge). Ship the reference script with the specification."),
("Test that variants differ exactly where their correct values differ, not always (wave 1 code).",
 """Test that variants differ exactly where their correct values differ, not always (wave 1 code).
- **The sign trap** (wave 2), a sibling of the same-count trap. When a score is a monotone function of one shared per-label quantity (an age, a count) with a fitted direction, the ranking depends only on that direction's sign. Shrinkage or rescaling that cannot flip the sign cannot change the ranking, so it is not a variant setting.
- **Changing a covariate is not ranking-preserving** (wave 2, W2-B01). Replacing a model's covariate by another increasing transform (a harmonic number for a logarithm) can reverse the fitted direction, and so the ranking. Claim that two forms are equivalent only with a proof, and search for a witness.
- **Probe pooled methods with a planted single-label effect** (wave 2). Pooling over labels dilutes an effect carried by one label; E_19's first form missed a planted single-ball cycle. Design the per-label route, or say why pooling is intended.
- **Divide out what another method already measures** before claiming a new effect (E_19 divides out the age trend and each label's own level), and check with a planted effect that the claim survives.
- **Every loop that waits for a condition needs a proved exit, for every input** (wave 2, W2R1-C01). An interval that narrows until it excludes zero never does when the true value is exactly zero, so test exact zero separately. Add a cap that refuses as an error, never a guess, and test the zero case, the cap and both signs."""),
]
S = [
("**FILL IN:** why the record is byte-identical on Windows and Linux (exact arithmetic, or a stated float discipline).",
 """**FILL IN:** why the record is byte-identical on Windows and Linux (exact arithmetic, or, for an iterative floating-point fit, the objective proof and the canonical output and tie rules; README, "published values must be byte-identical").
- **Answer explicitly:** does any step repeat until a condition holds (narrowing bounds, a search, an iteration)? Say why it ends for every input, including exact ties and exact zero, and what its cap does."""),
("- **Answer explicitly:** does any variant rank exactly like an installed method (README, \"the same-count ranking trap\")? If so, what distinguishes it: its probabilities, its window, its settings? The tests check every claimed relation by comparing `ranked_groups`.",
 "- **Answer explicitly:** does any variant rank exactly like an installed method (README, \"the same-count ranking trap\" and \"the sign trap\")? If so, what distinguishes it: its probabilities, its window, its settings? Is any claimed equivalence with another formulation proved, not assumed (README, \"changing a covariate\")? The tests check every claimed relation by comparing `ranked_groups`."),
]
outdir.mkdir(parents=True, exist_ok=True)
for src, edits in ((readme, R), (spec, S)):
    t = src.read_text('ascii')
    for o, n in edits:
        c = t.count(o)
        assert c == 1, (src.name, c, o[:60])
        assert n.isascii()
        t = t.replace(o, n)
    (outdir / src.name).write_bytes(t.encode('ascii'))
    print(src.name, len(edits), 'edits', hashlib.sha256(t.encode()).hexdigest())
