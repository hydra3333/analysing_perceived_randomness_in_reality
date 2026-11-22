#!/usr/bin/env python3
"""Finalise the RAT-41 files (Claude, 22 November 2026).

Purpose: read the reviewed candidates of H-1 v8 and register v0.32 from Git at HEAD (each asserted by SHA-256), apply
counted replacements (each old text must occur exactly once), and write the files for doc/:
  doc/HANDOVER/Claude_Primary_Handover_H1_v8.md
  doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md      (the candidate blurb, unchanged bytes)
  doc/RATIFICATION_REGISTER_v0_32.md
What changes: the status paragraph or version line, and, on the owner's instruction given with RAT-41, the statements
that the ratification itself made out of date. Nothing else. The register cites the final H-1 v8 hash, so H-1 v8 is
finalised first; H-1 v8 names the register by path only (a file cannot hold the hash of a file that holds its own).
Usage: python3 -I finalise_rat41.py REPO_ROOT
It refuses (an assertion) on a wrong candidate hash, an anchor not found exactly once, non-ASCII in H-1, or a CR.
"""
import hashlib, os, subprocess, sys

# ---- constants -------------------------------------------------------------------------------------------------
H1_CAND = 'exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8.md'
H1_CAND_SHA = '2fd38130415f4c3602ac86f6f2b4250781f27f25bf204f66269424ea2c54a1f4'       # passed in EX_272 and EX_273
BLURB_CAND = 'exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8_introductory_blurb.md'
BLURB_SHA = '586ececea64fca65b1ef3872a9fec60f1d7c659e0da408eb61e62d996d556d66'
REG_CAND = 'exchange/CLAUDE_WEB_TOOLS/register/RATIFICATION_REGISTER_v0_32.md'
REG_CAND_SHA = 'f508f7714693a7cfcd821ac714a475ae67f3dbc723e7924c8b2eb35168f25229'      # passed in EX_273, hashes refreshed
H1_OUT = 'doc/HANDOVER/Claude_Primary_Handover_H1_v8.md'
BLURB_OUT = 'doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md'
REG_OUT = 'doc/RATIFICATION_REGISTER_v0_32.md'
H2 = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md'
WHEN = '22 November 2026, 17:34'            # the owner's ratification (his message's time, Australia/Adelaide)
ENTRY = '153'                               # the decision log entry that records RAT-41

# (label, old text, new text) for H-1 v8. Each old text occurs exactly once in the candidate.
H1_EDITS = [
 ('status',
  "**Status:** CANDIDATE for independent review and the owner's ratification. It authorises nothing. Until it is\n"
  "ratified, H-1 v7r1 (RAT-39) is the installed Claude handover, read with decision log entries 121 to the latest.",
  "**Status:** OWNER-RATIFIED " + WHEN + " Australia/Adelaide (RAT-41; decision log entry " + ENTRY + "), together with the\n"
  "reviewer's handover H-2 v4 and register v0.32, after the reviewer's PASS (EX_272, EX_273). It is the installed Claude\n"
  "handover; H-1 v7r1 (RAT-39) stays as history. It is the reviewed candidate\n"
  "(`exchange/CLAUDE_WEB_TOOLS/h1v8/out/`, SHA-256 `" + H1_CAND_SHA + "`) with this status\n"
  "paragraph changed and, on the owner's instruction given with the ratification, the statements that the ratification\n"
  "itself made out of date brought up to date; `exchange/CLAUDE_WEB_TOOLS/h1v8/H1_v8_CANDIDATE_TO_FINAL.diff` is the exact\n"
  "difference. It authorises nothing."),
 ('replaces', "**Replaces, once ratified:** H-1 v7r1", "**Replaces:** H-1 v7r1"),
 ('reading list',
  "entries 121 to the latest (the owner's own words; entry 147 is RAT-40);",
  "entries 121 to the latest (the owner's own words; entry 147 is RAT-40, entry\n     " + ENTRY + " is RAT-41);"),
 ('0A item 3',
  "3. **The installed register is behind.** `doc/RATIFICATION_REGISTER_v0_31.md` is the newest installed edition. Register\n"
  "   v0.32, which records RAT-34's install to RAT-40, is a written CANDIDATE (section 4.4), not installed and not\n"
  "   owner-ratified; until it is, RAT-35 to RAT-40 are recorded only in the decision log. Read the log for the last RAT number, the last entry number and the last EX number\n"
  "   before using a new one. At this edition: the last RAT is RAT-40; the newest EX is EX_271; the newest decision log\n"
  "   entry is 148 (this candidate).",
  "3. **Read the log for a number before using one.** Register v0.32 (section 4.4) is the newest edition; it records\n"
  "   RAT-34's install to RAT-40 and its own ratification. For anything later the decision log is the record. Read the\n"
  "   log for the last RAT number, the last entry number and the last EX number before using a new one. At this\n"
  "   edition: the last RAT is RAT-41; the newest EX is EX_273; the newest decision log entry is " + ENTRY + " (RAT-41)."),
 ('0B item 8',
  "handovers fully up to date at this milestone; the reviewer committed its H-2 v4 candidate that afternoon\n"
  "   (section 4.4).",
  "handovers fully up to date at this milestone; the reviewer committed its H-2 v4 that afternoon (section 4.4).\n"
  "   That evening the owner ratified both handovers and register v0.32 together (RAT-41), and he has decided that a\n"
  "   new Claude chat takes over from this edition (entry 149)."),
 ('0C note 4',
  "4. **Section 1.6, the register.** v0.31 is the newest installed; v0.32 is a written candidate, not yet ratified\n"
  "   (section 4.4).",
  "4. **Section 1.6, the register.** v0.32 is the newest (RAT-41; section 4.4)."),
 ('4.4 H-2',
  "- **The reviewer's handover (H-2).** Ratified: H-2 v3r4 (RAT-36; its file name still says CANDIDATE). **The newest is\n"
  "  the reviewer's own full edition current to RAT-40,**\n"
  "  `" + H2 + "`\n"
  "  (`@H2@`; first committed at `30826be`, its\n"
  "  latest content at `70719f5`; its blurb's latest content at `adfd973`): a candidate until the owner ratifies it. Its section 0 states the current position, the",
  "- **The reviewer's handover (H-2).** **In force: H-2 v4, the reviewer's own full edition current to RAT-40, ratified by\n"
  "  the owner on 22 November 2026 (RAT-41):**\n"
  "  `" + H2 + "`\n"
  "  (`@H2@` as ratified; first committed at `30826be`, that\n"
  "  content at `70719f5`; its blurb's at `adfd973`). Its file name still says CANDIDATE: frozen wording. It replaces H-2\n"
  "  v3r4 (RAT-36). With RAT-41 the owner asked the reviewer to check that its handover names the installed editions, so\n"
  "  a later commit may refresh its references. Its section 0 states the current position, the"),
 ('4.4 register',
  "- **The register:** `doc/RATIFICATION_REGISTER_v0_31.md` (`c6369a72753ebda016f758e623df7a40bcb7a1300a49d503ccbb93be1b3cae6d`), RAT-34.\n"
  "  **Register v0.32 is a written CANDIDATE,** not installed and not owner-ratified:\n"
  "  `exchange/CLAUDE_WEB_TOOLS/register/RATIFICATION_REGISTER_v0_32.md` (SHA-256\n"
  "  `2fd091f34ea47399693b30f51b2a677d3d4cf348d028435cbd9639366d99135c` at the reviewed commit `a30b19a`; documentary PASS in\n"
  "  EX_273). Its cells for this handover and for H-2 v4 are refreshed after this edition, so its final hash is in the\n"
  "  decision log. Until it is ratified, the decision log is the record for RAT-35 to RAT-40.",
  "- **The register:** `doc/RATIFICATION_REGISTER_v0_32.md`, ratified with this handover (RAT-41; documentary PASS in EX_273).\n"
  "  It is register v0.31 (`c6369a72753ebda016f758e623df7a40bcb7a1300a49d503ccbb93be1b3cae6d`, RAT-34) with one added section\n"
  "  that records RAT-34's install to RAT-40. A file cannot hold the hash of a file that holds its own, so register\n"
  "  v0.32's hash is in decision log entry " + ENTRY + ". For anything after RAT-41 the decision log is the record."),
 ('10 items 1 and 2',
  "1. **This handover:** the reviewer's review; the owner's ratification; installation in `doc/HANDOVER/` with its blurb.\n"
  "   The reviewer's own handover current to RAT-40 (H-2 v4, section 4.4) awaits the owner's ratification too.\n"
  "2. **The owner decides whether build step 1 starts in the present Claude chat or a new one.**",
  "1. **Done on 22 November 2026 (RAT-41):** this handover, the reviewer's H-2 v4 and register v0.32 are ratified, and\n"
  "   this handover and the register are installed in `doc/`.\n"
  "2. **A new Claude chat takes over from this edition** (owner, entries 149 and " + ENTRY + "), by the staged takeover of\n"
  "   section 0. Build step 1 starts there, on the owner's go."),
 ('12.8 waiting',
  "- **Waiting on the reviewer:** its review of this candidate.\n"
  "- **Waiting on the owner:** the ratification of this edition and of the reviewer's H-2 v4 candidate; the choice of\n"
  "  chat for build step 1; then each go of section 10.",
  "- **Waiting on the reviewer:** nothing, beyond the check of its own handover's references that the owner asked for\n"
  "  with RAT-41.\n"
  "- **Waiting on the owner:** starting the new Claude chat and accepting its takeover; then each go of section 10."),
 ('12.8 item 6',
  "  6. Register v0.32, recording RAT-34's install to RAT-40: written on 22 November 2026 at the owner's choice, as a\n"
  "     candidate, and passed by the reviewer (EX_273). Still owed: the owner's ratification, and its installation in\n"
  "     `doc/` with the handovers.",
  "  6. The next register edition, when a code package or a handover next travels (section 1.6): it records RAT-41's\n"
  "     install and what follows. Nothing further is owed on register v0.32 (ratified and installed at RAT-41)."),
]

def git_bytes(repo, path):
    """Return the bytes of <path> at HEAD. Example: git_bytes(repo, 'exchange/README.md') -> b'# exchange/ ...'."""
    return subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + path], check=True, capture_output=True).stdout

def sha(data):
    """SHA-256 of bytes as 64 lower-case hex characters."""
    return hashlib.sha256(data).hexdigest()

def apply(text, edits, what):
    """Apply each (label, old, new); every old text must occur exactly once. Returns the new text."""
    for label, old, new in edits:
        n = text.count(old)
        assert n == 1, '%s, %s: expected one occurrence, found %d' % (what, label, n)
        text = text.replace(old, new)
    return text

def main():
    assert len(sys.argv) == 2, 'usage: finalise_rat41.py REPO_ROOT'
    repo = os.path.abspath(sys.argv[1])
    h1 = git_bytes(repo, H1_CAND); blurb = git_bytes(repo, BLURB_CAND); reg = git_bytes(repo, REG_CAND)
    assert sha(h1) == H1_CAND_SHA and sha(blurb) == BLURB_SHA and sha(reg) == REG_CAND_SHA, 'a candidate is not the reviewed bytes'
    h2 = sha(git_bytes(repo, H2)); h2b = sha(git_bytes(repo, H2.replace('.md', '_introductory_blurb.md')))

    # 1. H-1 v8.
    h1_final = apply(h1.decode('ascii'), [(l, o.replace('@H2@', h2), n.replace('@H2@', h2)) for l, o, n in H1_EDITS], 'H-1 v8')
    h1_bytes = h1_final.encode('ascii')
    assert b'\r' not in h1_bytes and h1_bytes.endswith(b'\n') and not h1_bytes.endswith(b'\n\n')
    h1_sha = sha(h1_bytes)

    # 2. Register v0.32 (it cites the final H-1 v8 hash).
    reg_edits = [
     ('version',
      "**Register version:** v0.32, 22 November 2026, CANDIDATE for the owner's ratification (with H-1 v8; written by Claude from the records; for the reviewer's review), recording",
      "**Register version:** v0.32, 22 November 2026, OWNER-RATIFIED " + WHEN + " (RAT-41, with H-1 v8 and the reviewer's H-2 v4; written by Claude from the records; reviewed in EX_273), recording"),
     ('entry range', "entries 62 to 150, which this section indexes.", "entries 62 to " + ENTRY + ", which this section indexes."),
     ('item 12',
      "12. **The handovers at this milestone** (22 November 2026; entries 148 to 150): Claude's H-1 v8 candidate, passed by the\n"
      "    reviewer with one pointer correction, which was applied (EX_272); the reviewer's own H-2 v4 candidate; this register.\n"
      "    The owner has decided that a new Claude chat takes over once H-1 v8 is ratified (entry 149).",
      "12. **The handovers at this milestone** (22 November 2026; entries 148 to " + ENTRY + "): Claude's H-1 v8, passed by the reviewer\n"
      "    (EX_272, EX_273); the reviewer's own H-2 v4; this register, passed in EX_273. **RAT-41** (below). The owner has decided\n"
      "    that a new Claude chat takes over from H-1 v8 (entry 149)."),
     ('row H-2 v3r4', "RAT-36; `d5e810c`; the operative reviewer handover until the owner ratifies a successor;",
      "RAT-36; `d5e810c`; superseded by H-2 v4 at RAT-41;"),
     ('row H-1 v7r1', "RAT-39; `7f9edc0`; the installed Claude handover until the owner ratifies H-1 v8;",
      "RAT-39; `7f9edc0`; superseded by H-1 v8 at RAT-41;"),
     ('row H-1 v8',
      "| `" + H1_CAND + "` and its blurb | Claude; the reviewer (EX_272) | CANDIDATE, not ratified; `" + H1_CAND_SHA + "`; blurb `" + BLURB_SHA + "` |",
      "| `" + H1_OUT + "` and its blurb | Claude; the reviewer (EX_272, EX_273) | OWNER-RATIFIED 22 Nov 2026 (RAT-41); `" + h1_sha + "`; the reviewed candidate `" + H1_CAND + "` `" + H1_CAND_SHA + "`; blurb (the candidate's bytes unchanged) `" + BLURB_SHA + "` |"),
     ('row H-2 v4',
      "| `" + H2 + "` and its blurb | the reviewer | CANDIDATE, not ratified; `" + h2 + "`; blurb `" + h2b + "` |",
      "| `" + H2 + "` and its blurb | the reviewer | OWNER-RATIFIED 22 Nov 2026 (RAT-41) at these bytes (main `70719f5`; blurb `adfd973`); the file name still says CANDIDATE; `" + h2 + "`; blurb `" + h2b + "` |"),
     ('future actions 1 and 2',
      "1. The reviewer's review of this register. The owner's ratification of it and of the two handovers (the next free number is\n"
      "   RAT-41), and their installation in `doc/`.\n"
      "2. A new Claude chat takes over once H-1 v8 is ratified (owner, entry 149).",
      "1. Done: the reviewer's review of this register (EX_273) and RAT-41. Claude commits this register and H-1 v8 into `doc/`\n"
      "   directly and checks them from GitHub; the next register edition records that commit.\n"
      "2. A new Claude chat takes over from H-1 v8 (owner, entry 149)."),
     ('ratification paragraph',
      "**The ratification of this register.** Not yet given. If the owner ratifies it, the finalisation changes only this\n"
      "register's version line, this paragraph and the status cells of the table above for the files ratified with it.",
      "**RAT-41 (owner, " + WHEN + "; entry " + ENTRY + ").** After the reviewer's PASS of H-1 v8 (EX_272, EX_273) and its documentary\n"
      "PASS of this register (EX_273), Claude asked whether the owner ratifies the two handovers and this register, with\n"
      "\"ratify all three together as RAT-41\" as the recommended option 1. The owner answered: \"Option 1 approved ... all three\n"
      "are ratified.\" **Ratified:** H-1 v8 and its blurb; the reviewer's H-2 v4 and its blurb; this register. H-1 v8 replaces\n"
      "H-1 v7r1 as the installed Claude handover, and H-2 v4 replaces H-2 v3r4 as the reviewer's. In the same message the\n"
      "owner gave a standing instruction: when Claude detects out-of-date statements, \"please strongly consider fixing them\".\n"
      "So, after the review, this register changed in its version line, this paragraph, the status cells of four rows of the\n"
      "table above, item 12, the entry range in its opening paragraph and future actions 1 and 2, and in nothing else\n"
      "(`exchange/CLAUDE_WEB_TOOLS/register/REGISTER_v0_32_CANDIDATE_TO_FINAL.diff`); H-1 v8 changed in its status paragraph and in\n"
      "the statements that the ratification itself made out of date (`exchange/CLAUDE_WEB_TOOLS/h1v8/H1_v8_CANDIDATE_TO_FINAL.diff`).\n"
      "RAT-41 authorises no code, build step, run or install on the owner's PC."),
    ]
    reg_final = apply(reg.decode('utf-8'), reg_edits, 'register')
    reg_bytes = reg_final.encode('utf-8')
    assert b'\r' not in reg_bytes and reg_bytes.endswith(b'\n')

    for path, data in ((H1_OUT, h1_bytes), (BLURB_OUT, blurb), (REG_OUT, reg_bytes)):
        full = os.path.join(repo, path)
        assert not os.path.exists(full), path + ' already exists: nothing is overwritten'
        with open(full, 'wb') as f:
            f.write(data)
        print('%s  %d bytes  %s' % (sha(data), len(data), path))

if __name__ == '__main__':
    main()
