#!/usr/bin/env python3
"""DOC-13: make the MHUP-1 design v0.1r6 from the ratified v0.1r5 Git blob by counted edits (Claude, 8 November 2026).

v0.1r6 = v0.1r5 with only:
  (a) amendment A1 (ratified 5 November 2026) folded in: the three passages A1 section 1 quotes are replaced by A1's rule;
  (b) LW-1: the source of results named Lotterywest-GOV where the design means the official results source (the "sibling
      Lotterywest host" refusals are left as they are: they mean other hosts);
  (c) the status lines: the title, a new version line (v0.1r5's line kept as history), and the rulebook tool list of section 8
      brought to register v0.24 future action 1 (four tools).
Nothing else changes. Usage (repository root): python3 -I exchange/CLAUDE_WEB_TOOLS/doc13/make_design_v0_1r6.py OUT
"""
import hashlib, subprocess, sys

SRC = 'doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md'
SRC_SHA = 'e5fb491ca601fa71793d143871d99c40929d20cdd8398fe92e0c6858c44a5455'
s = subprocess.run(['git', 'show', 'HEAD:' + SRC], capture_output=True, check=True).stdout
assert hashlib.sha256(s).hexdigest() == SRC_SHA, 'v0.1r5 is not the ratified bytes'
s = s.decode('utf-8')
assert '\r' not in s

EDITS = [
    # (c) title and version line
    ('# Mode H, the results update and the prospective mode - design v0.1r5\n',
     '# Mode H, the results update and the prospective mode - design v0.1r6\n'),
    ('**Version:** v0.1r5, 3 November 2026 (Adelaide, UTC+10:30). FOR THE OWNER\'S RATIFICATION:',
     '**Version:** v0.1r6, 8 November 2026 (Adelaide), OWNER-RATIFIED 8 November 2026 with DOC-13 (RAT-27) after the reviewer\'s check (EX_160, EX_161). v0.1r5 as RATIFIED by the owner on 3 November 2026 (MHUP-R; register v0.24), '
     'with **amendment A1** (RATIFIED 5 November 2026; `exchange/MHUP1_design_amendment_A1_RATIFIED.md`) folded into 5.2, 5.4 and '
     'Appendix L item L-H2, the results source named **Lotterywest-GOV** (LW-1, 4 November 2026), and the rulebook tool list of '
     'section 8 brought to register v0.24\'s future action 1. Nothing else is changed; text elsewhere that reads as before '
     'ratification (for example the schedule table of section 8 and the "Q" table of section 9) is kept as the record of the '
     'design round. **Lotterywest-GOV** means exclusively the official Western Australian Government Lotterywest website, using '
     'HTTPS and the exact hostname `www.lotterywest.wa.gov.au` (LW-1).\n'
     '**Previous edition (history):** v0.1r5, 3 November 2026 (Adelaide, UTC+10:30). FOR THE OWNER\'S RATIFICATION:'),
    # (a) A1 folded in: design 5.2, the lifecycle markers
    ('one score line per planned pair (create-only, in the Mode H score ledger) -> `SCORE_COMPLETE` (the scorer, after the last '
     'pair\'s line; it holds the ledger\'s digest)',
     'the whole Mode H score ledger, computed from one read of the targets\' outcomes, published once, create-only (temporary file, '
     'synced, linked), then validated as it stands (amendment A1, sections 2 and 3) -> `SCORE_COMPLETE` (the scorer, after the '
     'validation; it holds the ledger\'s digest)'),
    ('if the scorer stops after `SCORING_STARTED`, rerunning it finds that marker, re-verifies the same roster digest, skips every '
     'pair that already has a score line (it never re-reads an outcome for a pair already scored), scores the remaining pairs, then '
     'writes `SCORE_COMPLETE` and the seal',
     'if the scorer stops after `SCORING_STARTED`, rerunning it finds that marker, re-verifies the same roster digest and the scoring '
     'plan `SCORING_STARTED` froze, and resumes from one of two states (A1 section 4): with no ledger, it reads the outcomes again '
     'and publishes the whole ledger; with the complete ledger, it reads no outcome, validates the ledger and writes '
     '`SCORE_COMPLETE`, and a ledger that fails validation is a STOP for the owner and the reviewer; after `SCORE_COMPLETE` it reads '
     'no outcome, resumes the report file by file, then writes the seal'),
    # (a) design 5.4, scored once
    ('(5.2: the same attempt id, the same verified roster, scored pairs skipped, no outcome re-read after `SCORE_COMPLETE`)',
     '(5.2 as amended by A1: the same attempt id, the same verified roster, the ledger published whole once and validated before '
     '`SCORE_COMPLETE`, no outcome re-read once the ledger exists)'),
    # (a) Appendix L, L-H2
    ('scorer crash after one of ten targets, resume under the same attempt, one score line per pair',
     'scorer crash before the ledger\'s publication, after it and before `SCORE_COMPLETE`, and after `SCORE_COMPLETE`, each resumed '
     'under the same attempt; the twin-project byte identity of resumed and uninterrupted attempts; invalid ledgers refused before '
     '`SCORE_COMPLETE` (A1 sections 4 and 5)'),
    # (b) LW-1
    ("**C03** Lotterywest's published results", "**C03** Lotterywest-GOV's published results"),
    ("**The owner has decided that Lotterywest's published results", "**The owner has decided that Lotterywest-GOV's published results"),
    ('C03 = Lotterywest trusted', 'C03 = Lotterywest-GOV trusted'),
    ('trust Lotterywest as official', 'trust Lotterywest-GOV as official'),
    # (c) section 8's tool list (register v0.24 future action 1)
    ("the rulebook and deny-pattern additions for MHUP-A's tools (`Run_Evaluation.bat`, `Method_Mode_H.py`)",
     "the rulebook and deny-pattern additions for MHUP-A's tools (`Run_Evaluation.bat`, `Method_Mode_H.py`, `process_check.py`, "
     "the results updater v0.2; register v0.24 future action 1)"),
]
for old, new in EDITS:
    n = s.count(old)
    assert n == 1, f'expected one occurrence, found {n}: {old[:70]}'
    s = s.replace(old, new)
# plain 'Lotterywest' left (5): the two sibling-host refusals (L-U6), two titles of past review findings ("Lotterywest
# cross-checks", kept as the record of the review), and LW-1's own definition in the version line
assert s.count('Lotterywest') - s.count('Lotterywest-GOV') == 5, 'unexpected plain Lotterywest mention'
out = s.encode('utf-8')
open(sys.argv[1], 'wb').write(out)
print(sys.argv[1], len(out), hashlib.sha256(out).hexdigest())
