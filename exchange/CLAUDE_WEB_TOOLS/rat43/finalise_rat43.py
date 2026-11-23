#!/usr/bin/env python3
"""Finalise the RAT-43 files: install H-1 v9 and H-2 v5r1 with their blurbs in doc/HANDOVER/.

What this file is for
    The owner ratified H-1 v9 and H-2 v5r1 on 23 November 2026 (RAT-43, decision log entry 174). This reads the two
    candidates and their blurbs from Git at HEAD (each asserted by SHA-256), applies counted replacements (each old
    text must occur exactly once) to the status statements and to the statements the ratification itself makes out of
    date (the owner's standing instruction, entry 153), and writes the installed files. Nothing else changes; the
    exact differences are written beside this file.

Which part of the project's rules it carries out
    H-1 v8 section 8.5: "Finalising after ratification changes only the status line"; as at RAT-41, with the owner's
    instruction on out-of-date statements.

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I finalise_rat43.py <repository root> "<when>"
    <when> is the owner's ratification time as the decision log gives it, for example "23 November 2026, 15:18".
It refuses (an assertion) on a wrong candidate hash, an anchor not found exactly once, non-ASCII in new text, or a CR.
"""
import difflib
import hashlib
import os
import subprocess
import sys

# ---- constants -------------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = '174'                                                     # the decision log entry that records RAT-43
H1_CAND = 'exchange/CLAUDE_WEB_TOOLS/h1v9/out/Claude_Primary_Handover_H1_v9.md'
H1_CAND_SHA = '943077447a2b05c6eecd4a22381cf9a6591685211ec45dd1697db2d8861948b6'      # EX_281 PASS, correction applied
H1_BLURB_CAND = 'exchange/CLAUDE_WEB_TOOLS/h1v9/out/Claude_Primary_Handover_H1_v9_introductory_blurb.md'
H1_BLURB_SHA = '1cbe95bedb9741a610760b25de80e24eb3c798d9814287a4d28d8256c551dbe5'
H2_CAND = 'exchange/CLAUDE_WEB_TOOLS/h2v5r1/out/ChatGPT_Reviewer_Handover_H2_v5r1_CANDIDATE_20261123.md'
H2_CAND_SHA = '4703f51af2bb2fa5f7144ecc209a720adada2902ce51cc5fa9a0b0a28acc3d84'
H2_BLURB_CAND = 'exchange/CLAUDE_WEB_TOOLS/h2v5r1/out/ChatGPT_Reviewer_Handover_H2_v5r1_CANDIDATE_20261123_introductory_blurb.md'
H2_BLURB_SHA = 'c3335aa814dfbbc2424c0e0edec67092cd3a59666c1ff5702d9664832e5a1634'
H1_OUT = 'doc/HANDOVER/Claude_Primary_Handover_H1_v9.md'
H1_BLURB_OUT = 'doc/HANDOVER/Claude_Primary_Handover_H1_v9_introductory_blurb.md'
H2_OUT = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123.md'
H2_BLURB_OUT = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123_introductory_blurb.md'
REPO_URL = 'https://github.com/hydra3333/analysing_perceived_randomness_in_reality/blob/main/'


def git_bytes(root: str, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD. Refuses (CalledProcessError) a path HEAD does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def apply(text: str, edits: list, name: str) -> str:
    """Apply counted replacements: each old text must occur exactly once and each new text must be ASCII."""
    for old, new in edits:
        count = text.count(old)
        assert count == 1, f'{name}: anchor found {count} times: {old[:90]!r}'
        assert new.isascii(), f'{name}: non-ASCII in new text'
        text = text.replace(old, new)
    return text


def h1_edits(when: str) -> list:
    """The H-1 v9 changes at installation."""
    return [
        ('**Version:** v9 CANDIDATE, 23 November 2026', '**Version:** v9, 23 November 2026'),
        ('**Status:** CANDIDATE, NOT RATIFIED. The installed Claude handover is H-1 v8 (RAT-41) until the owner ratifies this\n'
         'edition. It authorises nothing.',
         f'**Status:** OWNER-RATIFIED {when} Australia/Adelaide (RAT-43; decision log entry {ENTRY}), together with the\n'
         'reviewer handover H-2 v5r1, after the reviewer\'s PASS (EX_281) and its one correction. It is the installed Claude\n'
         'handover; H-1 v8 (RAT-41) stays as history. It is the reviewed candidate (`' + H1_CAND + '`,\n'
         f'SHA-256 `{H1_CAND_SHA}`) with this status paragraph and the statements the ratification made out of\n'
         'date changed; `exchange/CLAUDE_WEB_TOOLS/rat43/H1_v9_CANDIDATE_TO_FINAL.diff` is the exact difference. It\n'
         'authorises nothing.'),
        ('**Replaces, once ratified:** H-1 v8 and its blurb (RAT-41), which stay where they are as history.',
         '**Replaces:** H-1 v8 and its blurb (RAT-41), which stay where they are as history.'),
        ('   edition: the last RAT is RAT-42 (the runner\'s rulebook v0.6); the newest EX is EX_280; the newest decision log\n'
         '   entry is 169 (the tidy-up installed), and entry 170 records this candidate.',
         f'   edition: the last RAT is RAT-43 (this handover and H-2 v5r1); the newest EX is EX_281; the newest decision log\n'
         f'   entry is {ENTRY} (RAT-43).'),
        ('step 1 and the tidy-up. The ChatGPT reviewer chat is the one that took over on 21 November 2026; it reviewed EX_266\n'
         '    to EX_280. On 23 November 2026 the reviewer committed its own H-2 v5 candidate (section 4.4), and the owner agreed\n'
         '    that Claude refresh H-1 before build step 2 (entry 166): this edition. The owner has not decided on a chat switch.',
         'step 1 and the tidy-up. The ChatGPT reviewer chat that took over on 21 November 2026 reviewed EX_266 to EX_281 and\n'
         '    ended on 23 November 2026, after committing its H-2 v5 candidate. At the owner\'s request Claude refreshed that\n'
         '    candidate as H-2 v5r1 (entry 173), and the owner ratified it with this edition (RAT-43). A new reviewer chat\n'
         '    starts from H-2 v5r1 and should verify it against the repository (section 4.4). The owner has not decided on a\n'
         '    Claude chat switch.'),
        ('  **H-2 v5** (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md` and its blurb, committed by the\n'
         '  reviewer on 23 November 2026 at `23689ef` and `31db13b`) is a candidate, not ratified. `exchange/CONTINUITY_NOW.md`\n'
         '  names the edition in force.',
         '  **In force since RAT-43 (entry ' + ENTRY + '): H-2 v5r1,** `' + H2_OUT + '` and its blurb. It is the\n'
         '  reviewer\'s own H-2 v5 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md`, committed at `23689ef`\n'
         '  and `31db13b`) with its status statements refreshed by Claude after the reviewer chat ended (entry 173); its rights\n'
         '  text and historical chapters are the reviewer\'s bytes. H-2 v4 and v5 stay as history.\n'
         '  `exchange/CONTINUITY_NOW.md` names the edition in force.'),
        ('2. **This edition** (H-1 v9), for the reviewer\'s check and the owner\'s ratification, as with v8. The reviewer\'s own\n'
         '   H-2 v5 candidate is its business; ratifying the two together is the owner\'s choice.',
         '2. **Done: this edition and H-2 v5r1 ratified (RAT-43, entry ' + ENTRY + ')** after EX_281; the reviewer chat ended and a\n'
         '   new one starts from H-2 v5r1.'),
        ('- **Waiting on the reviewer:** its check of this candidate, when the owner asks.\n'
         '- **Waiting on the owner:** ratification of this edition; his go for build step 2;',
         '- **Waiting on the reviewer:** a new reviewer chat, started by the owner from H-2 v5r1; its takeover reply.\n'
         '- **Waiting on the owner:** starting the new reviewer chat; his go for build step 2;'),
    ]


def h2_edits(when: str, h2_final_name: str) -> list:
    """The H-2 v5r1 changes at installation."""
    return [
        ('**Status: H-2 v5r1 OWNER-REVIEW CANDIDATE; NOT YET RATIFIED.**',
         f'**Status: OWNER-RATIFIED {when} Australia/Adelaide (RAT-43; decision log entry {ENTRY}), together with Claude\'s\n'
         f'H-1 v9; installed by Claude in doc/HANDOVER/ with only status statements changed (exact difference:\n'
         f'exchange/CLAUDE_WEB_TOOLS/rat43/H2_v5r1_CANDIDATE_TO_FINAL.diff; the reviewed-by-owner candidate is {H2_CAND},\n'
         f'SHA-256 {H2_CAND_SHA}). It is the operative reviewer handover; H-2 v4 and v5 stay as history.**'),
        ('The **operative, owner-ratified handover remains H-2 v4**, extended by the owner under RAT-41',
         'Until RAT-43 the operative, owner-ratified handover was H-2 v4, extended by the owner under RAT-41'),
        ('it and its prior introductory blurb have NOT been altered or superseded merely by publishing this candidate.',
         'it and its introductory blurb were not altered; RAT-43 superseded them.'),
        ('Only the owner may decide to adopt this edition.', 'The owner adopted this edition by RAT-43.'),
        ('2. The owner\'s RAT-43 decision on the H-1 v9 candidate (exchange/CLAUDE_WEB_TOOLS/h1v9/out/Claude_Primary_Handover_H1_v9.md, '
         'SHA-256 943077447a2b05c6eecd4a22381cf9a6591685211ec45dd1697db2d8861948b6, EX_281 PASS with its correction applied) and, '
         'if he chooses, on this H-2 v5r1 candidate jointly. Only after ratification are they installed in doc/HANDOVER/.',
         f'2. DONE: RAT-43 ({when}, entry {ENTRY}) ratified H-1 v9 and this H-2 v5r1 together; both installed in '
         f'doc/HANDOVER/ ({H1_OUT} and {h2_final_name}). A new reviewer chat starts from this handover and should verify '
         'it against the repository.'),
        ('2. Verify which handover is ratified: at the snapshot H-2 v4 remains IN FORCE, and H-2 v5 and this v5r1 are '
         'OWNER-REVIEW CANDIDATES. Claude\'s H-1 v8 is installed; the H-1 v9 candidate is reviewed (EX_281) and awaits '
         'RAT-43.',
         f'2. Verify which handover is ratified: since RAT-43 (entry {ENTRY}) this H-2 v5r1 and Claude\'s H-1 v9 are IN FORCE '
         'and installed in doc/HANDOVER/; H-2 v4, H-2 v5 and H-1 v8 are history.'),
        ('**Next-number checkpoint, not an allocation:** as of entry 173: next EX_282, next decision entry 174, next '
         'ratification RAT-43.',
         f'**Next-number checkpoint, not an allocation:** as of entry {ENTRY}: next EX_282, next decision entry '
         f'{int(ENTRY) + 1}, next ratification RAT-44.'),
    ]


def h2_blurb_edits(when: str, h2_final_sha: str) -> list:
    """The H-2 v5r1 blurb changes at installation."""
    return [
        ('# ChatGPT Independent Reviewer - H-2 v5r1 complete takeover blurb (23 November 2026; OWNER-REVIEW CANDIDATE)',
         '# ChatGPT Independent Reviewer - H-2 v5r1 complete takeover blurb (23 November 2026; OWNER-RATIFIED, RAT-43)'),
        ('This H-2 v5r1 and blurb are CANDIDATES pending the owner\'s acceptance/ratification.',
         f'The owner ratified H-2 v5r1 with Claude\'s H-1 v9 on {when} (RAT-43, decision log entry {ENTRY}).'),
        ('The currently ratified and operative reviewer handover remains H-2 v4 under RAT-41, with the owner\'s explicit '
         'approval of its refreshed reference edition (decision-log entries 153-154). Do NOT describe v5 or v5r1 as '
         'ratified, installed or in force until the owner says so.',
         'H-2 v5r1 is the operative reviewer handover; H-2 v4 (RAT-41) and the reviewer\'s v5 are history.'),
        ('**READ THIS COMPLETE REVIEWER HANDOVER:** [H-2 v5r1 complete candidate](' + REPO_URL + H2_CAND + ').\n'
         'Repository path: ' + H2_CAND + '\n'
         'H-2 v5r1 SHA-256 of stored GitHub bytes: ' + H2_CAND_SHA + '.',
         '**READ THIS COMPLETE REVIEWER HANDOVER:** [H-2 v5r1](' + REPO_URL + H2_OUT + ').\n'
         'Repository path: ' + H2_OUT + '\n'
         'H-2 v5r1 SHA-256 of stored GitHub bytes: ' + h2_final_sha + '. (The candidate the owner ratified, '
         + H2_CAND + ', SHA-256 ' + H2_CAND_SHA + ', differs from it only in status statements; '
         'exchange/CLAUDE_WEB_TOOLS/rat43/H2_v5r1_CANDIDATE_TO_FINAL.diff.)'),
        ('with its status statements refreshed; the exact difference is `H2_v5_TO_v5r1.diff` beside it.',
         'with its status statements refreshed; the exact difference is exchange/CLAUDE_WEB_TOOLS/h2v5r1/out/H2_v5_TO_v5r1.diff.'),
        ('It awaits the owner\'s RAT-43 decision; H-1 v8 stays the installed Claude handover until then.',
         f'The owner ratified it with this H-2 v5r1 (RAT-43); it is installed as {H1_OUT}.'),
        ('**Next numbers at the last data snapshot (not reserved):** EX_282, decision-log entry 174, RAT-43.',
         f'**Next numbers at the last data snapshot (not reserved):** EX_282, decision-log entry {int(ENTRY) + 1}, RAT-44.'),
    ]


def write_diff(old: str, new: str, old_label: str, new_label: str, path: str) -> None:
    """Write the exact unified difference between two texts."""
    lines = difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), old_label, new_label)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(lines)


def main() -> int:
    """Write the four installed files and the diffs; print their hashes; return 0."""
    root, when = os.path.abspath(sys.argv[1]), sys.argv[2]
    sources = {}
    for path, want in ((H1_CAND, H1_CAND_SHA), (H1_BLURB_CAND, H1_BLURB_SHA), (H2_CAND, H2_CAND_SHA),
                       (H2_BLURB_CAND, H2_BLURB_SHA)):
        data = git_bytes(root, path)
        assert sha(data) == want, f'{path} at HEAD is not the candidate the owner ratified'
        sources[path] = data.decode('utf-8')
    h1 = apply(sources[H1_CAND], h1_edits(when), 'H-1')
    h2 = apply(sources[H2_CAND], h2_edits(when, H2_OUT), 'H-2')
    h2_blurb = apply(sources[H2_BLURB_CAND], h2_blurb_edits(when, sha(h2.encode('utf-8'))), 'H-2 blurb')
    h1_blurb = sources[H1_BLURB_CAND]                                    # unchanged bytes, as at RAT-41
    assert h1.isascii() and h1_blurb.isascii() and h2_blurb.isascii()
    for text in (h1, h1_blurb, h2, h2_blurb):
        assert '\r' not in text and text.endswith('\n')
    for path, text in ((H1_OUT, h1), (H1_BLURB_OUT, h1_blurb), (H2_OUT, h2), (H2_BLURB_OUT, h2_blurb)):
        with open(os.path.join(root, path), 'wb') as f:
            f.write(text.encode('utf-8'))
    write_diff(sources[H1_CAND], h1, 'H1_v9_CANDIDATE', 'H1_v9_FINAL', os.path.join(HERE, 'H1_v9_CANDIDATE_TO_FINAL.diff'))
    write_diff(sources[H2_CAND], h2, 'H2_v5r1_CANDIDATE', 'H2_v5r1_FINAL',
               os.path.join(HERE, 'H2_v5r1_CANDIDATE_TO_FINAL.diff'))
    write_diff(sources[H2_BLURB_CAND], h2_blurb, 'H2_v5r1_blurb_CANDIDATE', 'H2_v5r1_blurb_FINAL',
               os.path.join(HERE, 'H2_v5r1_blurb_CANDIDATE_TO_FINAL.diff'))
    for path in (H1_OUT, H1_BLURB_OUT, H2_OUT, H2_BLURB_OUT):
        data = open(os.path.join(root, path), 'rb').read()
        print(sha(data), len(data), 'bytes', path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
