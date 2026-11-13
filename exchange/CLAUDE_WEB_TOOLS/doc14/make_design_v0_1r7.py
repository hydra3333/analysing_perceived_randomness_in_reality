#!/usr/bin/env python3
"""DOC-14: make the MHUP-1 design v0.1r7 from the ratified v0.1r6 Git blob by counted edits (Claude, 13 November 2026).

v0.1r7 = v0.1r6 with only what the owner ratified on 11 November 2026 (after the reviewer's R-2 PASS of commit 19e45ff;
`exchange/HO2_2026_11_10/MHUPA_Owner_Ratification_Rulebook_v05_AppJ_2026_11_11.md`), using the ratified wording of
`exchange/CLAUDE_WEB_TOOLS/mhupa/t016/final/APPENDIX_J_AMENDMENTS_RATIFIED.md`:
  J-1  Appendix J step 10's Action;  J-2  the negative-test sentence for step 10;
  J-3  step 13's STOP handling;      J-4  step 17's STOP handling after the release commit;
  C-1  section 4.3: the baseline's 40 entries per game;  C-2  section 4.3: the install record's time;
and the edition's own lines: the title, the version line, the history line and the footer. Nothing else.
Usage: python3 -I make_design_v0_1r7.py V0_1R6_FILE OUT_FILE
"""
import hashlib, sys

SRC_SHA = '7332dd6c1b3f6d9ef858b1881333ded56782bc595b7f894f04a75255909beb9d'    # v0.1r6 as installed with DOC-13 (RAT-27)
src, out = sys.argv[1], sys.argv[2]
s = open(src, 'rb').read()
assert hashlib.sha256(s).hexdigest() == SRC_SHA, 'v0.1r6 is not the ratified bytes'
assert b'\r' not in s
s = s.decode('ascii')

OLD_VERSION = s.split('\n')[2]
assert OLD_VERSION.startswith('**Version:** v0.1r6, 8 November 2026 (Adelaide), OWNER-RATIFIED 8 November 2026')
OLD_HISTORY_HEAD = '**Previous edition (history):** v0.1r5, 3 November 2026'

EDITS = [
    ('title', '# Mode H, the results update and the prospective mode - design v0.1r6',
     '# Mode H, the results update and the prospective mode - design v0.1r7'),
    ('version', OLD_VERSION,
     '**Version:** v0.1r7, 13 November 2026 (Adelaide). v0.1r6 with the Appendix J amendments J-1 to J-4 and the two section 4.3 '
     'wording corrections that the owner RATIFIED on 11 November 2026, after the reviewer\'s focused review and R-2 PASS of their '
     'drafts (commit `19e45ff`; `exchange/CLAUDE_WEB_TOOLS/mhupa/t016/final/APPENDIX_J_AMENDMENTS_RATIFIED.md`; register v0.27). '
     'They were applied in MHUP-A\'s install of 13 November 2026. This edition records those ratified decisions; it makes no new '
     'decision, and nothing else is changed. **Lotterywest-GOV** means exclusively the official Western Australian Government '
     'Lotterywest website, using HTTPS and the exact hostname `www.lotterywest.wa.gov.au` (LW-1).'),
    ('history', OLD_HISTORY_HEAD,
     '**Previous editions (history):** v0.1r6, 8 November 2026 (Adelaide): ' + OLD_VERSION[len('**Version:** v0.1r6, 8 November 2026 (Adelaide), '):]
     + ' v0.1r5, 3 November 2026'),
    ('C-2', 'the UTC time and local date of the POST PASS, and the registry entries the package added.',
     'the UTC time and local date at which it is written (step 12, after POST PASS and the suite; the field keeps its name '
     '`post_pass_utc`), and the registry entries the package added.'),
    ('C-1', 'travels in MHUP-A as an ordinary reviewed member: 40 entries, the 39 variants released',
     'travels in MHUP-A as an ordinary reviewed member: 40 entries per game (80 in all), for each game the 39 variants released'),
    ('J-1', '| 10 | The suite (the barrier paths are module constants the harness patches, so the suite passes with P present) |',
     '| 10 | The suite, run by the package\'s suite runner in `--shadow` mode: after a fresh POST PASS on the live tree, it copies '
     'the installed files byte for byte into a new temporary folder without the barrier files, together with only the six '
     'development data files the accepted tests read (for each game: the results master, its ledger and its INIT verification '
     'record), and runs the suite there; the live tree keeps U, E and P throughout and is checked again afterwards (POST, and no '
     'file gained, ignored files included); the temporary folder is then removed, and a folder that cannot be removed is a STOP '
     '(J-1) |'),
    ('J-3', 'stop; do not push; E, P and U stay (fail closed: the code is committed but not released); Claude writes the fix (a further '
            'small package commit, or a reviewed revert commit), COMMITTED is rerun, then steps 14-19 |',
     'stop; do not push; E, P and U stay (fail closed). No fix forward in place: the recovery is proposed by Claude for that exact '
     'state, checked by the reviewer and approved by the owner. The normal route is abandon and rebuild: a fresh install check '
     'showing `CLEAN` before any change; reviewed `git revert` commits, newest first (nothing is reset, rewritten or deleted; every '
     'commit and record stays in the history); E and P removed after another `CLEAN`; U released last; a new package, with its own '
     'name and records, built and reviewed on the resulting commit (J-3; exceptional recovery only, never a runner action or '
     'automatic) |'),
    ('J-4', '| stop; re-create P; after the fix, delete P and rerun from step 17 |',
     '| stop; U stays held; re-create P. If the release commit was not made, Claude\'s fix is applied, P removed and step 17 '
     'rerun. If the release commit was made, do not continue: the recovery is as step 13\'s (abandon and rebuild, approved for '
     'that exact state; the release record already committed stays in the history) (J-4) |'),
    ('J-2', 'the suite fails if P is absent at step 10 in the rehearsal (proving the harness patches it, not the absence of the barrier)',
     'the step 10 runner STOPs before copying if the live P (or E, or U) is missing or foreign; STOPs if the copy differs from '
     'the live tree or the import path reaches into the live tree (the live tree\'s own `.venv` excepted); STOPs if the live tree '
     'gains any file during the suite, ignored or not; and STOPs if its temporary folder cannot be removed; P\'s own refusals are '
     'tested in `test_mhupa_gates` and `test_e2r_dispatch` (J-2)'),
    ('footer', '\n*End of design v0.1r5.*\n', '\n*End of design v0.1r7.*\n'),
]
for label, old, new in EDITS:
    n = s.count(old)
    assert n == 1, f'{label}: expected one occurrence, found {n}: {old[:70]}'
    s = s.replace(old, new)
s.encode('ascii')
open(out, 'wb').write(s.encode('ascii'))
print(f'{len(EDITS)} counted edits applied; SHA-256 {hashlib.sha256(s.encode("ascii")).hexdigest()}')
