"""Draft 2 of the new-method template's README and specification template, by counted edits from draft 1
(Claude, 30 Oct 2026). Usage: python3 -I make_template_draft2.py INSTALLED_TEMPLATE_DIR OUT_DIR
The inputs are the installed draft-1 files (at 7c93320 and later). Every old string must occur exactly once;
inserted text is ASCII. The code skeletons (*.py.txt) change in the wave-1 code package, proved there by the
template trial; they are not edited here."""
import hashlib, sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
WANT = {'README.md': 'f17e2d6eb489797415252689038078047011b7aa7ba2e24f987c265078df3e26'}


def build(name, edits):
    raw = (src / name).read_bytes()
    if name in WANT:
        assert hashlib.sha256(raw).hexdigest() == WANT[name], name
    t = raw.decode('utf-8')
    for old, new in edits:
        assert t.count(old) == 1, (name, old[:70])
        assert all(ord(c) < 128 for c in new), (name, old[:40])
        t = t.replace(old, new)
    (out / name).write_bytes(t.encode('utf-8'))
    print(name, hashlib.sha256(t.encode()).hexdigest(), len(edits), 'edits')


out.mkdir(parents=True, exist_ok=True)
build('README.md', [
    ('# New-method template (draft 1)', '# New-method template (draft 2)'),
    ("**Status:** DRAFT 1, 30 October 2026, written with E_6 by Claude and reviewed with it. It will be revised after E_3 and E_4 (methods that share a helper and output scores only), and proved by the E_7-E_16 batch.",
     "**Status:** DRAFT 2, 30 October 2026, by Claude. Draft 1 was written with E_6; draft 2 adds what E_3 and E_4 taught (a shared helper, scores only, a minimum history) and what the design of wave 1 (E_7, E_8, E_9, E_10) found. It is reviewed with wave 1's design.\n"
     "**Kept up to date** (owner, 30 October 2026): whenever a method's design, review, code or install shows something this template should say or do differently, in Claude's assessment or the reviewer's, Claude proposes the update in the next package, and it is reviewed like any other document. Each method's handback says whether it found anything for the template."),
    ("| Its mathematics | `src/methods/E_<nnn>/model.py` (name it for what it does) | `method_folder/model.py.txt` |",
     "| Its mathematics | `src/methods/E_<nnn>/model.py` (name it for what it does), or a shared helper in `src/methods/_common/` used by several methods | `method_folder/model.py.txt` |"),
    ("**3. Fill in the mathematics** (`model.py`), at every `FILL IN:` marker.",
     "**3. Fill in the mathematics** (`model.py`), at every `FILL IN:` marker.\n"
     "- **Or a shared helper:** when several methods need the same calculation (E_3 and E_4: polynomial fits; wave 1: occurrence counts), put it in one module in `src/methods/_common/`, with its own test module, and keep only each method's own rule in its folder. Every method that uses the helper names it in its specification. A change to the helper is a new revision of every method that uses it (E2R-R14A), so fix its behaviour as carefully as a method's."),
    ("  - a `ProbabilityVector` only if the declaration says it has one.",
     "  - a `ProbabilityVector` only if the declaration says it has one.\n"
     "- **Scores only** (E_3, E_4, E_9, E_10): if the values are not chances (a curve can leave [0, 1]; a difference of rates is not a chance), declare `probability_kind` `NONE`, return no `ProbabilityVector`, and say why in the specification and the registry texts. Converting scores into chances by an invented transformation is not \"marking\"; publishing the scores themselves is.\n"
     "- **Too little history:** if the eligible draws are fewer than the declared `minimum_history_draws`, return an empty `MethodOutput` (no barrels). The contract then records `INSUFFICIENT_HISTORY`: published, no ticket. `verify()` must accept that record when it recomputes the same shortage, and refuse it otherwise."),
    ("**10. Planted-defect (mutation) checks.** For every property the tests claim, plant a defect in a disposable copy and show that a test fails (E_6: 14 defects). A defect that no test catches is a missing test; E_6 found one this way.",
     "**10. Planted-defect (mutation) checks.** For every property the tests claim, plant a defect in a disposable copy and show that a test fails (E_6: 14 defects; E_3/E_4: 27). Plan at least one defect per variant setting and one per verification rule. A defect that no test catches is a missing test: E_6 found one this way (every variant computed as the first), and E_3/E_4 another (a certificate accepting one alternation too few).\n\n"
     "**Several methods in one package** (E_3/E_4; wave 1): one shared helper with its own tests, one generator for all the declarations and entries, one test module for the methods, one `ADAPTERS` line per method, and one mutation tool covering all of them. Each method still gets its own folder, flag, variants and registry chains, and is released on its own."),
    ("## Things that bite (learned on E_6)", "## Things that bite (learned on E_6, E_3/E_4 and wave 1)"),
    ("- **A test that can only pass is not evidence.** Make sure each variant's own setting is tested against the formula computed in the test itself, not through the module's own lookup.",
     "- **A test that can only pass is not evidence.** Make sure each variant's own setting is tested against the formula computed in the test itself, not through the module's own lookup.\n"
     "- **The same-count ranking trap.** Every number is at risk in every draw, so all numbers share the same number of draws. Any score that depends only on a number's own count over the same draws (a posterior mean, a credible bound, a shrunk rate) is a monotone function of that count, and ranks exactly like counting over those draws: like E_1 over the full history. Check a new method's ranking against E_1 and against its own family before claiming it differs; if it does not differ, say so and say what does (its probabilities, for example).\n"
     "- **Forgetting rates can coincide.** A decayed count at E_6's factor ranks exactly like E_6's decay variant. Choose settings that do not duplicate an installed method, or say that they do.\n"
     "- **Compute every worked example with a tool.** The E_3/E_4 draft had two hand-worked values wrong. Ship the reference script with the specification.\n"
     "- **Never ask the Claude Code runner to count or filter output.** Ask for the whole output in its report and count it yourself (TASK_T005)."),
])
build('METHOD_SPECIFICATION_TEMPLATE.md', [
    ("**FILL IN** any overlap with other methods, stated plainly, for example \"with setting X it ranks exactly like E_1\". Overlap is reported (rank correlation), never a reason to exclude.",
     "**FILL IN** any overlap with other methods, stated plainly, for example \"with setting X it ranks exactly like E_1\". Overlap is reported (rank correlation), never a reason to exclude.\n"
     "- **Answer explicitly:** does any variant rank exactly like an installed method (README, \"the same-count ranking trap\")? If so, what distinguishes it: its probabilities, its window, its settings? The tests check every claimed relation by comparing `ranked_groups`."),
    ("**FILL IN:** a tiny case small enough to check by hand, with exact expected values for every variant. The tests check it exactly.",
     "**FILL IN:** a tiny case small enough to check by hand, with exact expected values for every variant. Compute the values with a reference script, not by hand, and ship the script with this specification. The tests check them exactly."),
    ("**FILL IN:**\n- the tests (README step 8);\n- the planted defects, one or more per property claimed (README step 10).",
     "**FILL IN:**\n- the tests (README step 8);\n- the planted defects, one or more per property claimed, per variant setting and per verification rule (README step 10);\n- whether anything found should change this template (owner, 30 October 2026)."),
])
