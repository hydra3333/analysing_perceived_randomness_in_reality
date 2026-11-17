"""Applies the reviewer's two corrections of EX_225 (RC-225-1, RC-225-2) to the supplement v0.8 amendment candidate and
to code plan v0.2, giving the two ratification candidates. Counted edits only; every old text must occur exactly once.

Usage: python3 -I make_ratification_candidates.py SUP_CANDIDATE PLAN_V0_2 SUP_OUT PLAN_OUT
SUP_CANDIDATE is MHUPB_DESIGN_SUPPLEMENT_v0_8_AMENDMENT_CANDIDATE.md as stored (CRLF; SHA-256 8e57b291...a571);
PLAN_V0_2 is codeplan/MHUPB_CODE_PLAN_DRAFT_v0_2.md as stored (CRLF; SHA-256 b5d9fff6...7983).
Both outputs are US-ASCII with CRLF, like their sources.
"""
import hashlib
import sys

SUP_SHA = '8e57b291982d430739c95f3a6f969757b76a87c27a4b6af7e7e9b1a08ecba571'
PLAN_SHA = 'b5d9fff652578e13b313a926ca215b2a6693935747bfa5c1fca5a230b0d17983'


def load(path, sha):
    raw = open(path, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == sha, 'not the expected bytes: ' + path
    s = raw.decode('ascii').replace('\r\n', '\n')
    assert '\r' not in s
    return s


def apply(s, edits, label):
    for old, new in edits:
        n = s.count(old)
        assert n == 1, f'{label}: expected one occurrence, found {n}: {old[:70]!r}'
        s = s.replace(old, new)
    assert all(ord(c) < 128 for c in s), label + ': not US-ASCII'
    return s


def save(path, s, label, count):
    open(path, 'wb').write(s.replace('\n', '\r\n').encode('ascii'))
    lines = s.split('\n')
    print(f'{label}: {count} counted edits; {len(lines) - 1} lines; longest line {max(map(len, lines))}')


SUP = [
    ("# MHUP-B design supplement - v0.8 (AMENDMENT CANDIDATE)",
     "# MHUP-B design supplement - v0.8 (RATIFICATION CANDIDATE)"),
    ("**Status: AMENDMENT CANDIDATE, by the Claude web chat (17 November 2026).**",
     "**Status: RATIFICATION CANDIDATE, by the Claude web chat (17 November 2026).**"),
    ("""B03, B04, C01, C02, C03) and follow the owner's directions OD-1 to OD-4 (decision log entries 69 and 70). Everything not
listed in section 1A is v0.7's text, unchanged; the builder `make_supplement_v0_8.py` makes it from v0.7's bytes by
counted edits.""",
     """B03, B04, C01, C02, C03) and to the reviewer's focused recheck (EX_225: RC-225-1 and RC-225-2), and follow the owner's
directions OD-1 to OD-4 (decision log entries 69 and 70). Everything not listed in section 1A is v0.7's text, unchanged;
the builders `make_supplement_v0_8.py` (v0.7 to the amendment candidate) and `make_ratification_candidates.py` (EX_225's
two corrections) make it from v0.7's bytes by counted edits."""),
    ("""v0.8, EX_223 (the review of the code plan, which asked for these amendments). **Gates left""",
     """v0.8, EX_223 (the review of the code plan, which asked for these amendments) and EX_225 (the focused recheck: a pass
with two corrections, RC-225-1 and RC-225-2, both applied). **Gates left"""),
    ("""| Owner OD-4 (v0.8) | A stopped stream stays stopped; no second registration in MHUP-B | 6.8 |
""",
     """| Owner OD-4 (v0.8) | A stopped stream stays stopped; no second registration in MHUP-B | 6.8 |
| EX_225 RC-225-1, RC-225-2 (v0.8) | What local records can and cannot establish about a missed week; repeating an admission already made changes nothing | 6.8; 4 rule 2A; 5.1 |
"""),
    ("""| 11, 12, 13, 14 | The ER-6 note; three alternatives; the decisions O-5 to O-7; the code round's added proofs |
""",
     """| 11, 12, 13, 14 | The ER-6 note; three alternatives; the decisions O-5 to O-7; the code round's added proofs |
| After EX_225: 4 rule 2A, 5.1, 6.8, 13, 14 | A repeated admission of the same attempt is a no-op; a publication is not made twice from the same inputs; the missed rule's operating assumptions and its reconciliation with earlier records; the cut-off shown to the owner as a conservative choice; the matching code-round tests |
"""),
    ("""   ledger; otherwise it is not admitted and the table is unchanged. So the canonical""",
     """   ledger; otherwise it is not admitted and the table is unchanged. The one exception is a repeat: if exactly that
   attempt is already listed, with the same score-ledger digest, keys' scope and scoring policy, the admission succeeds
   and changes nothing (the file is not rewritten), so an interrupted job can resume and publish. The same attempt
   identity with any difference still refuses, as does any key supplied by another source (EX_225 RC-225-2). So the canonical"""),
    ("""overwritten and never abandoned silently (v0.8; EX_223 B02).""",
     """overwritten and never abandoned silently (v0.8; EX_223 B02). Each publication's manifest pins its inputs; a publication
whose inputs equal those of the latest logged one is not made again, and the publish command reports the table as up to
date. No two search-log rows name the same publication (EX_225 RC-225-2)."""),
    ("""  only if it is durable before C(T) and T's result is not then in the master; otherwise the recorder refuses to write
  one.""",
     """  only if it is durable before C(T) and T's result is not then in the master; otherwise the recorder refuses to write
  one. The master is only a further check here: a result absent from the master is never taken as evidence that C(T)
  has not passed or that no result exists (EX_225)."""),
    ("""    a person. After C(T) it records the fact from the forecast ledger, whose whole chain it has first verified, and
    labels the line as recorded after the cut-off from the records, which is a weaker witness than a pre-outcome line.""",
     """    a person. After C(T) it records the fact from the forecast ledger, once it has verified the ledger's whole chain and
    reconciled it with every earlier record that names it (below), and labels the line as recorded after the cut-off
    from local records, which is a weaker witness than a pre-outcome line."""),
    ("""  become a pre-cut-off line. If the ledger's chain does not verify, or its times do not run forward, absence is not
  established and nothing is recorded: an absence of evidence is never evidence of absence.""",
     """  become a pre-cut-off line.
- **What the missed rule rests on (EX_225 RC-225-1).** The rule is valid only under three operating assumptions, which
  the registration states: the writers operate as specified, append-only, and nothing is later truncated, replaced or
  suppressed; the PC's clock and the order of its events are trustworthy relative to the real cut-off; and no eligible
  freeze line is ever removed or hidden after the fact. They are the trust the design already places in the freeze
  time and the deadline (design 6.4: the clock is no witness). A verified chain is local operational evidence only: as
  design 6.5 says, it shows that the lines agree with each other, and by itself it proves neither when they were
  written nor that the whole ledger was never replaced. A missed line is therefore never presented as independent
  proof of absence or of timing. **Reconciliation:** before writing a missed line the recorder checks the forecast
  ledger against every earlier record that names part of it. Every forecast-ledger extent (length and digest) and
  every freeze-line digest named in the OV-1 ledger, the witness ledger or a league publication's manifest must still
  be there, at the same position, with the same bytes; and no record of any kind may name a freeze line for T that the
  ledger does not hold. If the chain does not verify, its times do not run forward or lie after the recorder's own
  clock, or any reconciliation fails or cannot be completed, absence is not established and nothing is recorded: the
  target is blocked, never turned into missed. An absence of evidence is never evidence of absence. The rule needs no
  outside witness and no step by the owner in a missed week."""),
    ("""    written; a ledger that does not verify). Nothing is written for that target or any later one until it resolves. No""",
     """    written; a ledger that does not verify or reconcile). Nothing is written for that target or any later one until it resolves. No"""),
    ("""of section 1A; the owner gave his directions on 17 November 2026 (decision log entries 69 and 70).""",
     """of section 1A; the owner gave his directions on 17 November 2026 (decision log entries 69 and 70). The reviewer's
focused recheck (EX_225) passed them with two corrections, RC-225-1 and RC-225-2, both applied in this edition, and
recommends that the owner ratify this corrected edition together with the code plan once it has checked the two
corrections."""),
    ("""- O-5. The opportunity rule, the cut-off and the failure rules of 6.5 and 6.8 (his directions OD-2, OD-3 and OD-4).""",
     """- O-5. The opportunity rule, the cut-off and the failure rules of 6.5 and 6.8 (his directions OD-2, OD-3 and OD-4),
  with the missed rule's operating assumptions. The cut-off is written as 01:30 UTC on the draw date: noon in Adelaide
  in daylight time and 11:00 in standard time. That is a conservative choice, never later than his noon, not an exact
  translation of "noon Adelaide time" (EX_225 R-1)."""),
    ("""finished with the same bytes or marked incomplete, never logged as complete.
""",
     """finished with the same bytes or marked incomplete, never logged as complete.

After EX_225 the code round must also show: the missed status refused, and the target blocked, for a torn, truncated or
replaced forecast ledger, for a prefix that conflicts with an extent or freeze-line digest recorded earlier in the OV-1
ledger, the witness ledger or a publication manifest, for a freeze-line time after the recorder's clock, and for a
clock that runs backwards; a repeated admission of the same attempt succeeding without rewriting the source file, and
the same identity with different bytes or scope refusing; crashes before and after admission, between admission and
publication, after the search-log row and during the repair of `current`, each ending with exactly one canonical score
per key and one `WEEKLY_TABLE` row per completed publication; a torn or duplicated search-log row.
"""),
]

PLAN = [
    ("# MHUP-B code plan - DRAFT v0.2 (for the reviewer's focused recheck, then the owner's ratification)",
     "# MHUP-B code plan - v0.3 (RATIFICATION CANDIDATE)"),
    ("**Status: DRAFT v0.2, by the Claude web chat, 17 November 2026 (Adelaide).",
     "**Status: RATIFICATION CANDIDATE v0.3, by the Claude web chat, 17 November 2026 (Adelaide)."),
    ("""`exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_8_AMENDMENT_CANDIDATE.md` ("Sup v0.8"), which goes to the same
recheck and the same ratification.""",
     """`exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_8_RATIFICATION_CANDIDATE.md` ("Sup v0.8"), which goes to the
same ratification.

**What changed from v0.2.** The reviewer's focused recheck (EX_225) passed v0.2 with two corrections, both applied here
and in Sup v0.8: RC-225-1, what local records can and cannot establish about a missed week (L5; 6.6); and RC-225-2, a
repeated admission of the same attempt changes nothing and no publication is made twice (L4; L8; 9). R-5's conditions
for the report-only form are added to L8, and section 12 records the answers. Nothing else changed.
`CANDIDATE_TO_RATIFICATION_CANDIDATE_PLAN.diff` shows every changed line; v0.2 stays beside this file."""),
    ("""| OD-6 | Three technical review slices, one install | 4 | - |
""",
     """| OD-6 | Three technical review slices, one install | 4 | - |
| EX_225 RC-225-1 | What local records can and cannot show about a missed week; reconciliation with earlier records | L5; 6.6 | 6.8 |
| EX_225 RC-225-2 | A repeated admission of the same attempt is a no-op; one row per publication; resume after any crash | L4; L8; 9 | 4 rule 2A; 5.1 |
| EX_225 R-5 | The report-only form: a pinned, authorised batch; resumable; tested with both plan kinds | L8 | - |
"""),
    ("""Otherwise it refuses, names the first conflicting key, and changes nothing. An""",
     """Otherwise it refuses, names the first conflicting key, and changes nothing. A repeat for exactly the
  attempt already listed, with the same score-ledger digest, keys' scope and scoring policy, succeeds and changes nothing
  (the file is not rewritten), so the job goes on to publish; the same identity with any difference refuses (EX_225
  RC-225-2). An"""),
    ("""     input pinned so the bytes can be rebuilt exactly (the source file's digest and entries, each ledger's verified
     length and digest, the roster with release dates).""",
     """     input pinned so the bytes can be rebuilt exactly (the source file's digest and entries, each ledger's verified
     length and digest, the forecast ledger's included, the roster with release dates)."""),
    ("""  so none is reused. A failed `current` copy is repaired from the archive.""",
     """  so none is reused. A failed `current` copy is repaired from the archive. A `publish` whose pinned inputs equal those of
  the latest logged publication writes nothing and reports the table as up to date, so a rerun after a crash that
  followed the row never makes a second publication; and before appending a row the writer checks that no row already
  names the manifest (EX_225 RC-225-2)."""),
    ("""  `current` copy (section 9); a manifest whose inputs have changed is marked incomplete, not finished wrongly;""",
     """  `current` copy (section 9); a manifest whose inputs have changed is marked incomplete, not finished wrongly; a
  repeated `admit` of the same attempt changes no byte, and the same identity with different bytes or scope refuses;
  crashes before and after admission, between admission and publication, after the row and during the `current`
  repair, each ending with exactly one canonical score per key and one row per publication; a torn or duplicated
  search-log row;"""),
    ("""  - *missed* (`MISSED_NO_FREEZE`), for a target with no pre-cut-off freeze line: written after C(T), from the verified
    forecast ledger, naming that ledger's length and digest as read, and labelled as recorded after the cut-off;""",
     """  - *missed* (`MISSED_NO_FREEZE`), for a target with no pre-cut-off freeze line: written after C(T), from the forecast
    ledger once its chain verifies and it reconciles with every earlier record (6.6), naming that ledger's length and
    digest as read, and labelled as recorded after the cut-off from local records;"""),
    ("""  the records alone, with the cut-off tested one second before, at, and one second after; a missed line refused when
  the forecast ledger's chain is broken or its times run backwards; a freeze line appended after the cut-off never""",
     """  the records alone, with the cut-off tested one second before, at, and one second after; a missed line refused, and
  the target blocked, when the forecast ledger is torn, truncated or replaced, its chain is broken, its times run
  backwards or lie after the recorder's clock, or it conflicts with an extent or freeze-line digest named earlier in
  the OV-1 ledger, the witness ledger or a publication manifest (EX_225 RC-225-1); a freeze line appended after the
  cut-off never"""),
    ("""  scores of O-4 are made, with no forecast run again. Rerunning the command with the batch it printed continues
  from the records alone: an unfinished batch is run on, a batch without a report is reported, an unadmitted fill is
  admitted.""",
     """  scores of O-4 are made, with no forecast run again. That form uses only an authorised batch at its own pin and the
  accepted outcome reader, never changes the batch's forecasts, refuses any key a canonical source already supplies,
  and is tested with a version-1 batch and a version-2 batch (EX_225 R-5); running it for O-4 still needs its own go.
  Rerunning the command with the batch it printed continues from the records alone: an unfinished batch is run on, a
  batch without a report is reported, an unadmitted attempt is admitted, an admitted one is not admitted again (L4),
  and an unpublished table is published."""),
    ("""| Missed | no pre-cut-off freeze line for the target | factor 1, a `MISSED_NO_FREEZE` line, written after the cut-off from the verified forecast ledger |""",
     """| Missed | no pre-cut-off freeze line for the target | factor 1, a `MISSED_NO_FREEZE` line, written after the cut-off from the forecast ledger, verified and reconciled |"""),
    ("""a ledger whose chain or times fail |""",
     """a ledger whose chain, times or reconciliation fail |"""),
    ("""  earlier than the line before), so it can never become a pre-cut-off line. The recorder writes the missed line only
  after C(T) and only from a ledger whose whole chain it has verified; a broken chain blocks, because an absence of
  evidence is not evidence of absence. Skipping a draw by a rule that uses only information from before the draw keeps
  the score a fair-draw supermartingale, exactly as V = 0 does. The times are the PC's clock, the same trust the
  design already places in `PROSPECTIVE` (Sup 6.4).""",
     """  earlier than the line before), so it can never become a pre-cut-off line. Skipping a draw by a rule that uses only
  information from before the draw keeps the score a fair-draw supermartingale, exactly as V = 0 does.
- **What that rests on (EX_225 RC-225-1; Sup v0.8 6.8).** Three operating assumptions, stated in the registration: the
  writers append as specified and nothing is later truncated, replaced or suppressed; the PC's clock and event order
  are trustworthy relative to the real cut-off (the trust the design already places in `PROSPECTIVE` and the deadline;
  the clock is no witness); no eligible freeze line is removed or hidden after the fact. A verified chain is local
  evidence that the lines agree; it does not prove when they were written or that the ledger was never replaced
  (design 6.5). So the recorder writes a missed line only after C(T), only from a ledger whose whole chain verifies,
  and only once the ledger reconciles with every earlier record that names part of it: each forecast-ledger extent
  and freeze-line digest named in the OV-1 ledger, the witness ledger or a publication manifest must be there
  unchanged, and no record may name a freeze line for T that the ledger lacks. Any failure, or a time after the
  recorder's clock, blocks the target; it is never turned into missed, because an absence of evidence is not
  evidence of absence. The missed line is labelled as recorded after the cut-off from local records, and is never
  presented as independent proof of absence or of timing. No owner step and no outside witness are needed."""),
    ("""| `publish` | before and after: the manifest; each archive member; the `WEEKLY_TABLE` row; each step of the `current` copy | a row only for a complete set; the same publication finished with the same bytes, or marked incomplete; no version reused |""",
     """| `publish` | before and after: the manifest; each archive member; the `WEEKLY_TABLE` row; each step of the `current` copy | a row only for a complete set; the same publication finished with the same bytes, or marked incomplete; no version reused; a rerun after the row publishes nothing new and adds no row |"""),
    ("""| `admit` | the source file's replacement | the old file or the new file, never a mixture; no key admitted twice |""",
     """| `admit` | the source file's replacement | the old file or the new file, never a mixture; no key admitted twice; a repeat of the same attempt succeeds and changes no byte |"""),
    ("""**For the focused recheck (the points where this plan goes beyond the exact words of EX_223):**""",
     """**Put to the focused recheck (the points where this plan went beyond the exact words of EX_223); EX_225's answers
follow the list:**"""),
    ("""OD-1 to OD-6 as directions (entries 69, 70). **RECOMMENDED:** everything else in sections 4 to 10. **OPEN:** R-1 to R-6;
the owner's ratification of this plan and of Sup v0.8.""",
     """OD-1 to OD-6 as directions (entries 69, 70). **RECOMMENDED:** everything else in sections 4 to 10.

**EX_225's answers:** R-1 accepted, to be shown to the owner as a conservative choice, not an exact translation of
"noon Adelaide time" (Sup v0.8 13, O-5); R-2 the arithmetic and the stop argument passed, the evidence wording
corrected by RC-225-1; R-3 and R-4 accepted, with RC-225-2; R-5 accepted, with RC-225-2's restart behaviour and its
conditions (L8); R-6 passed, subject to the two corrections; the probe is never claimed to prove the production
software (6.5). **OPEN:** the reviewer's check of the two corrections; then the owner's ratification of this plan and
of Sup v0.8, together. Ratification authorises no code (entry 67)."""),
    ("""End of draft v0.2.""",
     """End of v0.3."""),
]

if __name__ == '__main__':
    sup_in, plan_in, sup_out, plan_out = sys.argv[1:5]
    save(sup_out, apply(load(sup_in, SUP_SHA), SUP, 'supplement'), 'supplement', len(SUP))
    save(plan_out, apply(load(plan_in, PLAN_SHA), PLAN, 'plan'), 'plan', len(PLAN))
