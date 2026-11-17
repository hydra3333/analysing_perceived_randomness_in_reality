"""Builds MHUP-B code plan DRAFT v0.2 from DRAFT v0.1 by whole-block replacements and counted edits.

Usage: python3 -I make_plan_v0_2.py V0_1_FILE NEW_BLOCKS_DIR OUT_FILE
V0_1_FILE is the plan v0.1 as stored (CRLF). A block runs from a heading line up to (not including) the next named
heading. Every heading and every old text is asserted to occur exactly once. Output: US-ASCII, CRLF.
"""
import sys
from pathlib import Path

src, blocks_dir, out = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
s = open(src, 'rb').read().decode('ascii').replace('\r\n', '\n')


def block(start, end, name):
    """Replace from the line starting with `start` up to the line starting with `end` (or to the end of the file)."""
    global s
    new = (blocks_dir / name).read_text(encoding='ascii')
    a = s.index('\n' + start) + 1 if start else 0
    assert start == '' or s.count('\n' + start) == 1, start
    if end is None:
        b = len(s)
    else:
        assert s.count('\n' + end) == 1, end
        b = s.index('\n' + end) + 1
    assert a < b
    s = s[:a] + new + s[b:]


def edit(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)


block('', '## 0. In plain English', 'b_header.md')
block('## 0. In plain English', '## 1. Scope', 'b_0.md')
block('## 1. Scope', '## 2. What reading the installed code showed', 'b_1.md')
block('## 3. The baseline', '## 4. The package: files, by layer', 'b_3.md')
block('## 4. The package: files, by layer', '## 5. Layer by layer', 'b_4.md')
block('### L4. The league table', '### L5. OV-1', 'b_L4.md')
block('### L5. OV-1', '### L6. The window contract', 'b_L5.md')
block('### L6. The window contract', '### L7. The consolidated report', 'b_L6.md')
block('### L8. The orchestrator', "## 6. OV-1's numerical contract", 'b_L8.md')
block('**6.6 Failure semantics', '## 7. Isolation of the live path', 'b_66.md')
block('## 7. Isolation of the live path', '## 8. The source schemas', 'b_7.md')
block('## 8. The source schemas', '## 9. Interruption and restart', 'b_8.md')
block('## 9. Interruption and restart', '## 10. Windows gates and the install', 'b_9.md')
block('## 10. Windows gates and the install', '## 11. Documents that travel', 'b_10.md')
block('## 11. Documents that travel', '## 12. Decisions and questions', 'b_11.md')
block('## 12. Decisions and questions', None, 'b_12_to_end.md')

# ---------------------------------------------------------------- section 2: counted edits
edit("""  Decision log entry 58 also records the answer "only the new or changed variants are computed". This conflict is put
  to the owner as OD-1 (section 12).""",
     """  Decision log entry 58 also records the answer "only the new or changed variants are computed". **Decided (OD-1, entry
  69):** plans of the new kind may name their variants, in two kinds of run (L6; Sup v0.8 7.1A).""")
edit("""- **CF-7. The development and Mode H score ledgers are git-ignored** (`.gitignore` lines for
  `results/real/development/scores/` and `results/real/holdout/scores/`): they exist only on the owner's PC. So "the
  adapters against the actual schemas" (EX_213) cannot be shown on real records from the repository. Section 8 says how.""",
     """- **CF-7. The development and Mode H score ledgers were git-ignored.** The owner committed them on 17 November 2026
  (`cc665ce`; OD-5, entry 70), so both AIs can now read the real records. Claude's one-time census of them passed
  (section 8).""")
edit("""  score ledger through that function alone. Method code never sees it. Question CP-Q5.""",
     """  score ledger through that function alone. Method code never sees it. The reviewer accepts this with conditions
  (EX_223 CP-Q5), which are in L2.
- **CF-10. E_1's development scores are for its old revision.** The census (section 8) shows the development score
  records of E_1 carry revision 2, now superseded; revision 3 has scores only in the sealed Mode H ledgers, which are
  shown and never summed. So in the first league table E_1 revision 3 would read `NO_SCORES`. A routine fill for it,
  and for every variant's holdout targets, is among the first runs the package makes possible (L6; section 12A).""")

# ---------------------------------------------------------------- L1, L2, L3, L7: counted edits
edit("""  from Appendix E and cross-checked by a second, independently written "what should happen" function (R-4).""",
     """  from Appendix E and cross-checked by a second, independently written "what should happen" function (R-4). The
  mode-to-pin rule has its own negative cases for `REAL_DEVELOPMENT`, `CATCH_UP` and `FINAL_NEXT_DRAW` at
  `last_draw(v)`, at `last_draw(v) + 1` and beyond, and T-05 shows that no admitted combination changes a
  method-facing byte (EX_223 CP-Q9).""")
edit("""  environment digest; the previous line's digest. No witness or publication status.""",
     """  environment digest; the previous line's digest. No witness or publication status. A line's freeze time is never
  earlier than the line before it: the writer refuses to append if the clock is behind (Sup v0.8 6.8 relies on it).
- **Reading "scored" (CF-9; EX_223 CP-Q5).** `score_identities.scored_identities` gives the forecasting half only the
  target, the scored record's digest, the policy id and whether every record a freeze line names has its routine score
  line. A target is closed only by score lines that carry the digests of the records its own freeze line names: a
  foreign, malformed or duplicated score identity refuses, and never closes a target. It exposes no match count,
  ranking, score or outcome, imports nothing from the evaluator, and a static test shows the forecasting half reads
  the score ledger nowhere else. A taint test plants a marker in every outcome-derived field of a score ledger and
  shows it reaches no run request, task or view.""")
edit("""  `frozen_at_utc`; effective class; exposure flag (`EXPOSED_DRAWS`; Powerball 1587 and 1588 carry HX-2).""",
     """  `frozen_at_utc`; effective class; exposure flag (`EXPOSED_DRAWS`; Powerball 1587 and 1588 carry HX-2); the drawn
  numbers, as the WF-1B score record holds them; and whether the draw's date in the master is its derived date (OV-1
  stops on a draw that is off the weekly rule, Sup v0.8 6.8).""")
edit("""- **Labels for the forward and catch-up family tables (RECOMMENDED; CP-Q4).** Their window and roster grow from report to
  report, so they are not a family fixed in advance. Use R3's existing labels and invent none: `EXPLORATORY_COHORT`,
  and `BONFERRONI_REFERENCE_UNCALIBRATED` on any Bonferroni arithmetic, under the heading "secondary".""",
     """- **Labels for the forward and catch-up family tables (EX_223 CP-Q4: accepted, with this precision).** Their window and
  roster grow from report to report, so they are not a family fixed in advance: `EXPLORATORY_COHORT`, under the
  heading "secondary". `BONFERRONI_REFERENCE_UNCALIBRATED` is put only on Bonferroni arithmetic whose prerequisites
  actually fail (the family, the fixed grid or an input's validity). Local figures keep their own labels and `LOW_N`;
  catch-up stays apart from the prospective column; the sealed Mode H report's own calibration is quoted, not redone.
  No confirmatory family is made from a secondary table. No new label is invented.""")

# ---------------------------------------------------------------- section 6: counted edits
edit("""small: the exact counts and one function, the upper end of `exp`. If the certificate fails, the program refuses and
writes no factor line.""",
     """small: the exact counts and one function, the upper end of `exp`. The certificate is a hard refusal (EX_223 CP-Q2),
and it is separate from the pointwise claim of 6.2, which has its own proof.

**It is computed and sealed before the outcome (EX_223 C02).** The certificate depends on the weights alone, not on the
drawn numbers. So the whole factor table of a draw (every possible X, each lambda) is built and certified when the
eligibility line is written, and its digest goes into that line. If it cannot be built and certified then, no
eligibility line is written, and that is decided before the result exists. At scoring the table is rebuilt, must equal
the sealed digest, and the factor line only looks up the observed X.""")
edit("""- restart: the ledger rebuilt from its eligibility lines and the score ledger equals the stored bytes.""",
     """- restart: the ledger rebuilt from its eligibility lines and the score ledger equals the stored bytes;
- X rebuilt two ways from the fixed score identities (TOP minus WORST matches; the weights of the drawn numbers) and
  required to agree and to lie in the sealed table's support; a corrupt score line, a score line under another policy
  and an out-of-support X each planted once (EX_223 C02, CP-Q9);
- the probe's `decimal` checks are feasibility evidence only. The proofs are the written remainder bounds and the
  exact-fraction oracle (EX_223 CP-Q2).""")

assert all(ord(c) < 128 for c in s) and '\r' not in s and '@@' not in s
open(out, 'wb').write(s.replace('\n', '\r\n').encode('ascii'))
print(f'{s.count(chr(10))} lines; longest line {max(len(l) for l in s.split(chr(10)))}')
