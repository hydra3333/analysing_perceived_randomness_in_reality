#!/usr/bin/env python3
"""Builds the reviewer handover H-2 v5r1 candidate and its blurb from the reviewer's own H-2 v5 candidate.

What this file is for
    The ChatGPT reviewer chat ended on 23 November 2026 after EX_281, having said that its H-2 v5 candidate "needs a
    short status refresh to recognise the completed tidy-up before it could be ratified jointly with H-1 v9". At the
    owner's request (decision log entry 173) Claude makes that refresh, as it did on 21 November 2026 (the v3r10
    continuity candidate). It reads the reviewer's H-2 v5 and blurb from Git at HEAD (each asserted by SHA-256),
    replaces only status statements of section 0 and of the blurb by counted replacements (each old text must occur
    exactly once), asserts that everything from the historical chapters' heading to the end is byte-identical, and
    writes
        out/ChatGPT_Reviewer_Handover_H2_v5r1_CANDIDATE_20261123.md
        out/ChatGPT_Reviewer_Handover_H2_v5r1_CANDIDATE_20261123_introductory_blurb.md
        out/H2_v5_TO_v5r1.diff  and  out/H2_v5_TO_v5r1_blurb.diff
    The reviewer's files are not changed. No reviewer right, scientific rule or owner permission is changed.

Which part of the project's rules it carries out
    H-1 v8 section 8.5 (a new candidate from the exact Git blob by counted replacements, the builder travelling with
    it); H-1 v8 section 4.4 (Claude wrote a reviewer continuity candidate when the reviewer chat was lost).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_h2_v5r1.py <repository root> <H-1 v9 candidate SHA-256>
It refuses (an assertion) on any failure: a wrong input hash, an anchor not found exactly once, a changed historical
region, a non-ASCII byte in new text, a CR, or a leftover placeholder.
"""
import hashlib
import os
import subprocess
import sys

# ---- constants -------------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
V5 = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md'
V5_SHA = '54ce9f3bd62ea0bac4e591d03904af34bf3ae444e5510af2aafc62057204a8af'      # as the reviewer's blurb states it
V5_BLURB = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123_introductory_blurb.md'
V5_BLURB_SHA = '5c8686db10c124ef5aa57895c97aa02b6fb29ed2cf4189e93b3cf43cdf0e4cde'
HISTORY_HEADING = '# HISTORICAL INHERITED H-2 CHAPTERS (1-19)'                  # from here to the end: unchanged
OUT_NAME = 'ChatGPT_Reviewer_Handover_H2_v5r1_CANDIDATE_20261123.md'
OUT_BLURB = 'ChatGPT_Reviewer_Handover_H2_v5r1_CANDIDATE_20261123_introductory_blurb.md'
REPO_URL = 'https://github.com/hydra3333/analysing_perceived_randomness_in_reality/blob/main/'
OUT_PATH = 'exchange/CLAUDE_WEB_TOOLS/h2v5r1/out/' + OUT_NAME
H1V9 = 'exchange/CLAUDE_WEB_TOOLS/h1v9/out/Claude_Primary_Handover_H1_v9.md'


def git_bytes(root: str, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD. Refuses (CalledProcessError) a path HEAD does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    """Replace one passage that must occur exactly once; the new text must be ASCII. Refuses (assertion) otherwise."""
    count = text.count(old)
    assert count == 1, f'anchor found {count} times: {old[:100]!r}'
    assert new.isascii(), f'non-ASCII in new text: {new[:60]!r}'
    return text.replace(old, new)


def handover_edits(h1v9_sha: str, head: str) -> list:
    """The counted replacements of the handover: [(old, new), ...], every old text taken from H-2 v5 verbatim."""
    return [
        ('# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v5 (COMPLETE CANDIDATE; 23 November 2026)',
         '# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v5r1 (COMPLETE CANDIDATE; 23 November 2026)'),
        ('**Status: NEW H-2 v5 OWNER-REVIEW CANDIDATE; NOT YET RATIFIED.** Prepared by ChatGPT at the owner\'s express request '
         'to completely refresh the reviewer handover ahead of build step 2.',
         '**Status: H-2 v5r1 OWNER-REVIEW CANDIDATE; NOT YET RATIFIED.** H-2 v5 was prepared by ChatGPT at the owner\'s express '
         'request to completely refresh the reviewer handover ahead of build step 2. **v5r1 is a status refresh of it made '
         'by Claude at the owner\'s request (decision log entry 173)** after the reviewer chat ended on 23 November 2026, '
         'following EX_281, in which it said its v5 "needs a short status refresh to recognise the completed tidy-up". '
         'Only status statements of this section 0 changed; the historical chapters 1-19, the rights text and every rule '
         'are the reviewer\'s v5 bytes (SHA-256 ' + V5_SHA + '), asserted by the builder '
         '`exchange/CLAUDE_WEB_TOOLS/h2v5r1/make_h2_v5r1.py`; `H2_v5_TO_v5r1.diff` beside this file is the exact difference. '
         '**A new reviewer chat should verify this refresh against the repository itself** rather than trust it because '
         'Claude wrote it.'),
        ('**Evidence/status cutoff:** GitHub main 5ff5ea0e3a641774b2f58cf61e79a751698d327b (23 November 2026), decision log '
         'through entry 167, reviewer EX_280. The latest state recorded there is: step 1 INSTALLED and Windows-proved; the '
         '37-file tidy-up REVIEWED PASS but **NOT INSTALLED**, still awaiting the owner\'s separate PC-install GO. The owner '
         'has said that Claude should refresh H-1 AFTER that tidy-up is installed and BEFORE build step 2. If that '
         'installation or H-1 refresh subsequently occurs, read those newer commits and decisions as authoritative; do not '
         'silently assume either already happened.',
         '**Evidence/status cutoff:** GitHub main ' + head + ' (23 November 2026), decision log through entry 173, '
         'reviewer EX_281. The latest state recorded there is: step 1 INSTALLED and Windows-proved; **the 37-file tidy-up '
         'INSTALLED and Windows-proved** (main c7e6ed8, entry 169); **the H-1 v9 candidate** (Claude\'s refresh of H-1 v8) '
         'reviewed in EX_281 (PASS WITH ONE NARROW TEXT CORRECTION; FIX AND PROCEED), the correction applied on the owner\'s '
         'word (entry 172), SHA-256 ' + h1v9_sha + ', awaiting the owner\'s RAT-43 decision. Read any newer commits and '
         'decisions as authoritative.'),
        ('**Light method-file tidy-up (RAT-40 note 3): REVIEWED PASS, not yet installed.**',
         '**Light method-file tidy-up (RAT-40 note 3): INSTALLED AND WINDOWS-PROVED (entry 169, main '
         'c7e6ed8ec854ab50e32559062e8b73c5c5e9abd1).** On the owner\'s PC: PRE PASS; 37 files copied; POST PASS; the '
         'comments-only check (211 Python files, 37 changed, 0 problems) RESULT: PASS; the suite unchanged (571 of 571, the '
         'same known failures); the complete equivalence check RESULT: PASS - COMPLETE (Powerball 17,280/17,280, Oz Lotto '
         '8,760/8,760, MISSING 0); COMMITTED PASS; pushed. Claude verified c7e6ed8 from GitHub against all 37 manifest '
         'entries and the tested tree. The owner\'s unedited outputs are in '
         'exchange/CLAUDE_WEB_TOOLS/tidy1/evidence/owner_pc_2026_11_23/. The review record follows:'),
        ('The proposed install ZIP SHA-256 is a8d2f1136a41a361e665ef2b16e2f3ce073dff64b52e697f4588971fc812ad4c. Owner has NOT at '
         'this snapshot given its separate PC install GO; after that GO the owner runs the sheet including comments-only, '
         'matching suite and **complete** 26,040-forecast equivalence. The reviewer has NOT independently run Windows/cloud '
         'tests, and must not say the tidy-up was installed or accepted on Windows until evidence arrives.',
         'The install ZIP SHA-256 was a8d2f1136a41a361e665ef2b16e2f3ce073dff64b52e697f4588971fc812ad4c; the owner gave its '
         'install GO in entry 168. The reviewer did not itself run Windows or cloud tests; the Windows evidence is the '
         'owner\'s run above.'),
        ('3. Post-layout light header, dependency list and missing-comments tidy-up, with NO scientific computation change '
         'and complete equivalence rerun, BEFORE QA or PROD install. At this cutoff: source reviewed PASS, local install '
         'still pending.',
         '3. Post-layout light header, dependency list and missing-comments tidy-up, with NO scientific computation change '
         'and complete equivalence rerun, BEFORE QA or PROD install. **DONE: installed and Windows-proved at c7e6ed8 '
         '(entry 169).**'),
        ('**Then NOTE-3 TIDY:** REVIEWED but installation pending; this is a separate owner GO, not a fifth grand redesign '
         'stage.',
         '**Then NOTE-3 TIDY:** DONE (installed and Windows-proved, entry 169); it was a separate owner GO, not a fifth grand '
         'redesign stage.'),
        ('Before step 2 the new Claude handover is to be refreshed by Claude AFTER the tidy-up is actually installed, as '
         'requested by the owner (entry 166).',
         'Before step 2 the Claude handover is refreshed (entry 166): the H-1 v9 candidate (entry 170), reviewed in EX_281 '
         'and corrected (entry 172), awaits the owner\'s RAT-43 decision.'),
        ('A future owner-authorised runner task requiring access still needs its SPECIFIC narrowly reviewed amendment or the '
         'owner personally runs a reviewed read-only sheet.',
         'A future owner-authorised runner task requiring access still needs its SPECIFIC narrowly reviewed amendment or the '
         'owner personally runs a reviewed read-only sheet. **EX_281 H1V9-C01:** the present full suite prints known FAILED '
         'results, and under rulebook v0.6 rule 10 the runner must STOP when they appear; a complete suite baseline is '
         'therefore an owner-run sheet unless the owner first approves a narrowly reviewed rulebook exception. T024 was '
         'historical, not a standing exception.'),
        ('- **EX_279-EX_280:** comments-only tidy-up. EX_280 PASS on 23 November; local installation still pending as of '
         'entry 167.',
         '- **EX_279-EX_280:** comments-only tidy-up. EX_280 PASS on 23 November; installed and Windows-proved at c7e6ed8 '
         '(entries 168-169).'),
        ('- **Known existing old-system suite failures:**',
         '- **EX_281 (H-1 v9 candidate):** documentary PASS WITH ONE NARROW TEXT CORRECTION (H1V9-C01, section 8.6 runner '
         'wording); FIX AND PROCEED; applied by Claude on the owner\'s word without another review round (entry 172), '
         'candidate SHA-256 ' + h1v9_sha + '. Its count correction: the reviewed v8-to-v9 diff was 307 lines added and '
         '222 removed (entry 170 said 304/203; corrected in entry 172). **The reviewer chat then ended** (entry 173); this '
         'v5r1 status refresh was written by Claude at the owner\'s request.\n'
         '- **Known existing old-system suite failures:**'),
        ('1. On the owner\'s own PC-install GO, install and verify reviewed TIDY1_Method_Comments_v1 and retain complete '
         'source+run evidence. A cloud 17,400/17,400 is PARTIAL, not the required complete 26,040/26,040.\n'
         '2. After that confirmed installation, Claude refreshes H-1 v8 into its next COMPLETE edition and blurb before '
         'stage 2 starts (owner entry 166). Review and owner ratification as applicable. The present reviewer H-2 v5 '
         'candidate is independent of that future H-1 build and must be reconciled against it at ratification; no future '
         'H-1 hash is invented.',
         '1. DONE: the tidy-up installed and Windows-proved with the complete 26,040/26,040 equivalence (entry 169).\n'
         '2. The owner\'s RAT-43 decision on the H-1 v9 candidate (' + H1V9 + ', SHA-256 ' + h1v9_sha + ', EX_281 '
         'PASS with its correction applied) and, if he chooses, on this H-2 v5r1 candidate jointly. Only after ratification '
         'are they installed in doc/HANDOVER/.'),
        ('1. Before writing a reviewer response, fetch GitHub current HEAD and read current decision log, latest EX, source '
         'files, manifest and complete diff. At the cutoff this is entry 167 and EX_280, but timestamps and EX counters '
         'expire immediately on a new commit.\n'
         '2. Verify which handover is ratified: at the snapshot H-2 v4 remains IN FORCE, H-2 v5 is an OWNER-REVIEW '
         'CANDIDATE. Claude\'s H-1 v8 is installed; a future refresh was requested but not yet installed.',
         '1. Before writing a reviewer response, fetch GitHub current HEAD and read current decision log, latest EX, source '
         'files, manifest and complete diff. At the cutoff this is entry 173 and EX_281, but timestamps and EX counters '
         'expire immediately on a new commit.\n'
         '2. Verify which handover is ratified: at the snapshot H-2 v4 remains IN FORCE, and H-2 v5 and this v5r1 are '
         'OWNER-REVIEW CANDIDATES. Claude\'s H-1 v8 is installed; the H-1 v9 candidate is reviewed (EX_281) and awaits '
         'RAT-43.'),
        ('**Next-number checkpoint, not an allocation:** as of entry 167: next EX_281, next decision entry 168, next '
         'ratification RAT-43.',
         '**Next-number checkpoint, not an allocation:** as of entry 173: next EX_282, next decision entry 174, next '
         'ratification RAT-43.'),
    ]


def blurb_edits(v5r1_sha: str, h1v9_sha: str, head: str) -> list:
    """The counted replacements of the blurb: [(old, new), ...]."""
    return [
        ('# ChatGPT Independent Reviewer - H-2 v5 complete takeover blurb (23 November 2026; OWNER-REVIEW CANDIDATE)',
         '# ChatGPT Independent Reviewer - H-2 v5r1 complete takeover blurb (23 November 2026; OWNER-REVIEW CANDIDATE)'),
        ('This H-2 v5 and blurb are NEW CANDIDATES pending the owner\'s acceptance/ratification.',
         'This H-2 v5r1 and blurb are CANDIDATES pending the owner\'s acceptance/ratification. **The previous reviewer chat '
         'wrote H-2 v5 and ended on 23 November 2026 after EX_281; Claude made this v5r1 status refresh of it at the '
         'owner\'s request (decision log entry 173), changing only status statements. Verify it against the repository '
         'yourself; do not trust it because Claude wrote it.**'),
        ('Do NOT describe the present v5 as ratified, installed or in force until the owner says so.',
         'Do NOT describe v5 or v5r1 as ratified, installed or in force until the owner says so.'),
        ('**READ THIS COMPLETE NEW REVIEWER HANDOVER (once the owner accepts it):** [H-2 v5 complete candidate]'
         '(https://github.com/hydra3333/analysing_perceived_randomness_in_reality/blob/main/doc/HANDOVER/'
         'ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md).\n'
         'Repository path: doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md\n'
         'H-2 v5 SHA-256 of stored GitHub bytes: 54ce9f3bd62ea0bac4e591d03904af34bf3ae444e5510af2aafc62057204a8af.\n'
         'Its live section 0 is current through main 5ff5ea0e3a641774b2f58cf61e79a751698d327b, decision-log entry 167 and '
         'reviewer EX_280.',
         '**READ THIS COMPLETE REVIEWER HANDOVER:** [H-2 v5r1 complete candidate](' + REPO_URL + OUT_PATH + ').\n'
         'Repository path: ' + OUT_PATH + '\n'
         'H-2 v5r1 SHA-256 of stored GitHub bytes: ' + v5r1_sha + '. It is the reviewer\'s H-2 v5 (' + V5_SHA + ') '
         'with its status statements refreshed; the exact difference is `H2_v5_TO_v5r1.diff` beside it.\n'
         'Its live section 0 is current through main ' + head + ', decision-log entry 173 and reviewer EX_281.'),
        ('(https://github.com/hydra333/analysing_perceived_randomness_in_reality/blob/main/doc/'
         'Predictive_Randomness_Deployment_Design_v0_12.md)',
         '(https://github.com/hydra3333/analysing_perceived_randomness_in_reality/blob/main/doc/'
         'Predictive_Randomness_Deployment_Design_v0_12.md)'),
        ('**THE LIGHT TIDY-UP HAS REVIEW PASS BUT IS NOT YET RECORDED AS INSTALLED.**',
         '**THE LIGHT TIDY-UP IS INSTALLED AND WINDOWS-PROVED** (main c7e6ed8, entry 169: comments-only check PASS, the '
         'suite unchanged, the complete equivalence check PASS - COMPLETE, 26,040/26,040). Its review record:'),
        ('Reviewer EX_280 PASS is not a Windows install GO. At entry 167, Claude awaits the owner\'s own GO to run the '
         'sheet, including COMPLETE 26,040 forecast equivalence.',
         'Reviewer EX_280 PASS was not a Windows install GO; the owner gave his own GO (entry 168) and ran the sheet.'),
        ('**After successful tidy-up INSTALL:** the owner has directed Claude to refresh H-1 into its next complete edition '
         'before build step 2. At this H-2 v5 cutoff H-1 v8 is still the installed Claude handover; do not make up its '
         'successor name, commit or hash. H-2 v5 here is a full CURRENT CANDIDATE, not a declaration that the tidy-up or '
         'H-1 revision has happened.',
         '**The H-1 refresh:** Claude wrote the H-1 v9 candidate (entry 170; ' + H1V9 + '); EX_281 passed it with one '
         'narrow correction (section 8.6: the runner must STOP on the suite\'s known FAILED results under rulebook v0.6 '
         'rule 10), applied on the owner\'s word (entry 172); SHA-256 ' + h1v9_sha + '. It awaits the owner\'s RAT-43 '
         'decision; H-1 v8 stays the installed Claude handover until then.'),
        ('Read the full H-2 v5, then the actual ratified documents', 'Read the full H-2 v5r1, then the actual ratified documents'),
        ('**Next numbers at the last data snapshot (not reserved):** EX_281, decision-log entry 168, RAT-43.',
         '**Next numbers at the last data snapshot (not reserved):** EX_282, decision-log entry 174, RAT-43.'),
    ]


def main() -> int:
    """Build the candidate, its blurb and the two diffs; print their hashes; return 0."""
    root, h1v9_sha = os.path.abspath(sys.argv[1]), sys.argv[2]
    head = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'], check=True, capture_output=True,
                          text=True).stdout.strip()
    assert sha(git_bytes(root, H1V9)) == h1v9_sha, 'the H-1 v9 candidate at HEAD is not the one named'
    v5 = git_bytes(root, V5)
    assert sha(v5) == V5_SHA, 'H-2 v5 at HEAD is not the reviewer\'s candidate'
    blurb = git_bytes(root, V5_BLURB)
    assert sha(blurb) == V5_BLURB_SHA, 'the H-2 v5 blurb at HEAD is not the reviewer\'s'
    text = v5.decode('utf-8')
    history = text[text.index(HISTORY_HEADING):]
    for old, new in handover_edits(h1v9_sha, head):
        text = replace_once(text, old, new)
    assert text[text.index(HISTORY_HEADING):] == history, 'the historical chapters changed'
    assert '\r' not in text and '@@' not in text
    out_bytes = text.encode('utf-8')
    new_blurb = blurb.decode('ascii')
    for old, new in blurb_edits(sha(out_bytes), h1v9_sha, head):
        new_blurb = replace_once(new_blurb, old, new)
    assert new_blurb.isascii() and '\r' not in new_blurb and 'hydra333/' not in new_blurb
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, OUT_NAME), 'wb') as f:
        f.write(out_bytes)
    with open(os.path.join(OUT, OUT_BLURB), 'wb') as f:
        f.write(new_blurb.encode('ascii'))
    print('historical chapters unchanged:', len(history.encode('utf-8')), 'bytes,', sha(history.encode('utf-8')))
    for name in (OUT_NAME, OUT_BLURB):
        data = open(os.path.join(OUT, name), 'rb').read()
        print(sha(data), len(data), 'bytes', name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
