"""The introductory blurbs for H-1 v1r7 and H-2 v1r8, from the installed v1r6 and v1r7 blurbs by counted edits
(Claude, 1 Nov 2026). Usage: python3 -I make_blurbs_v1r7_v1r8.py H1_BLURB_v1r6 H2_BLURB_v1r7 OUT_H1 OUT_H2"""
import hashlib, re, sys

b1, b2, o1, o2 = sys.argv[1:5]


def load(p, sha):
    raw = open(p, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == sha, p
    t = raw.decode('ascii')
    assert '\r' not in t
    return t


def apply(t, edits):
    for old, new in edits:
        assert t.count(old) == 1, (t.count(old), old[:70])
        assert new.isascii()
        t = t.replace(old, new)
    return t


def section(t, head, nxt):
    i = t.index(head)
    return t[i:t.index(nxt, i)]


# ================================================================ H-1 blurb
t = load(b1, '5c6b30415baae6fbeda5a5e3c5073b472782c1f78d59b85eecd4b9e644c7de49')
E1 = [
    ("# Introductory blurb for a new Claude chat (primary designer and coder) - goes with H-1 v1r6",
     "# Introductory blurb for a new Claude chat (primary designer and coder) - goes with H-1 v1r7"),
    ("Written by Claude, 30 October 2026, with H-1 v1r6 (owner's instruction: each handover has its blurb saved next\nto it). Keep it in step with the handover.",
     "Written by Claude, 1 November 2026, with H-1 v1r7, for the owner's planned chat switch after the snapshot (owner's\ninstruction: each handover has its blurb saved next to it). Keep it in step with the handover."),
    ("You are Claude, taking over as the **primary designer and coder** of a research project. A previous Claude chat\ndid this work until it reached its length limit; everything it knew is in the repository. Please read carefully\nbefore doing anything.",
     "You are Claude, taking over as the **primary designer and coder** of a research project. A previous Claude chat\ndid this work until the owner chose to start a fresh chat; everything it knew is in the repository, including its\nworking tools (`exchange/CLAUDE_WEB_TOOLS/`) and a section written for you (H-1 section 12, \"Working knowledge\").\nYou do not have its cloud workspace. Please read carefully before doing anything."),
    ("  rights are protected; support them, never narrow them. A new reviewer chat started on 30 October 2026, after the\n  previous one reached its length limit.",
     "  rights are protected; support them, never narrow them. The reviewer chat that started on 30 October 2026\n  continues; it has reviewed everything since EX_077."),
    ("1. Clone the repository. Read `doc/HANDOVER/Claude_Primary_Handover_H1_v1r6.md` (H-1, your handover) in full, then\n   its section 0 reading list: H-2, the newest sections of the current register\n   (`doc/RATIFICATION_REGISTER_v0_20.md`), `exchange/README.md`, `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`,\n   `doc/METHOD_TEMPLATE/README.md`, the owner's lists `exchange/OWNER_ROADMAP.md` and `exchange/OWNER_REMINDERS.md`,\n   and the newest `exchange/EX_*` files.",
     "1. Clone the repository. Read `doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md` (H-1, your handover) in full,\n   including section 12, then its section 0 reading list: H-2, the newest sections of the current register\n   (`doc/RATIFICATION_REGISTER_v0_23.md` or later), `exchange/README.md`, `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`,\n   `doc/METHOD_TEMPLATE/README.md`, `exchange/CLAUDE_WEB_TOOLS/README.md`, the owner's lists\n   `exchange/OWNER_ROADMAP.md` and `exchange/OWNER_REMINDERS.md`, and the newest `exchange/EX_*` files."),
    ("2. Check that the hashes H-1 quotes match the files (`git show HEAD:<path> | sha256sum`).",
     "2. Check that the hashes H-1 quotes match the files (`git show HEAD:<path> | sha256sum`), and work through H-1\n   section 12.9 (set up a workspace and run the whole suite once)."),
]
t = apply(t, E1)
old_state = section(t, '**Where things stand (30 October 2026).**', '**Hard rules (binding; nothing overrides them).**')
t = apply(t, [(old_state, """**Where things stand (1 November 2026, at the snapshot).**
- **Released and running on past draws:** all 40 method variants (E_1 revision 2, and E_2, E_3, E_4, E_6, E_7,
  E_8, E_9, E_10, E_17, E_18 and E_19), in both games. The first walk-forward batches (each past draw predicted only
  from the draws before it) are done: Powerball 17,280 runs, Oz Lotto 8,760 runs.
- **The scorer and ranking report (WF-1B)** is installed (`24d192f`), with the fair-draw simulator N1 and its
  approved NIST seed. PERF-1, a reviewed speed-up with identical results, is installed (`3fce327`). The first
  reports are done and committed (Oz Lotto `441daf2`, Powerball `608025c`): in both games nothing departs from
  fair draws (development evidence only; H-1 section 7.5).
- **Tests:** 471 offline tests pass on Windows and Linux.
- **Next, in the owner's order:**
  1. Mode H (each method tested once on the ten sealed holdout draws per game), the results update and the
     prospective (next-draw) mode, designed together. The owner's goal is forecasts for the draws of the week of
     9 November 2026. H-1 section 10 and section 12.8 list what is still open, including a version-2 master
     reader that the results update needs;
  2. WF-1C, the workers change;
  3. wave 3, with the owner's Method B as E_45;
  4. an NL-means discussion, waves 4 to 11 and the ensembles last.
  `exchange/OWNER_ROADMAP.md` explains each step in plain English.

""")])
t = apply(t, [
    ("- The four safety switches stay False, and the scientific allowlist stays empty.",
     "- Three safety switches stay False; the fourth (`ENABLE_CONTRACT_REAL_DEVELOPMENT`) is on, for owner-authorised\n  development runs only. The scientific allowlist stays empty."),
    ("- No real-data science, holdout access, Mode H, FINAL, process termination, destructive or Windows lifecycle test,\n  master update or dependency upgrade without the owner's separate, reviewed approval.",
     "- No new batch or report run, holdout access, Mode H, FINAL, process termination, destructive or Windows lifecycle\n  test, master update or dependency upgrade without the owner's separate, reviewed approval. Never open anything\n  under `source_data`, `results` or `transitory_data` yourself; the owner attaches report text when it is shared."),
    ("- Keep a running checkpoint of decisions and hashes, so nothing lives only in the chat. When the chat nears its\n  limit, write the next handover and its blurb first.",
     "- Use specific paths with `git add`, never `-A`. Do not push while the owner may have local commits waiting.\n- The owner is sometimes on a phone only; then give only steps that need no PC.\n- Keep a running checkpoint of decisions and hashes, so nothing lives only in the chat. When the chat nears its\n  limit, write the next handover and its blurb first."),
])
assert t.endswith('\n') and t.isascii()
open(o1, 'wb').write(t.encode('ascii'))

# ================================================================ H-2 blurb
u = load(b2, '4d4d9b9b4a1a34fe4ce6256f64d67314ffb3a7a78ad0277df4f0b4c803d852ee')
E2 = [
    ("# Introductory blurb for a new ChatGPT reviewer chat - goes with H-2 v1r7",
     "# Introductory blurb for a new ChatGPT reviewer chat - goes with H-2 v1r8"),
    ("The project owner pastes the text below the line into a new ChatGPT chat to start it. Written by Claude on the\nowner's instruction, 30 October 2026, with H-2 v1r7 (the previous reviewer chat reached its maximum length). It\nreplaces the older starter text that framed ChatGPT as a one-task document reviewer beside a separate ChatGPT coder;\nboth of those roles have ended.",
     "The project owner pastes the text below the line into a new ChatGPT chat to start it, **only if the current\nreviewer chat has to be replaced** (it continues at the snapshot). Written by Claude, 1 November 2026, with H-2\nv1r8, updating the v1r7 blurb's facts."),
    ("   - `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md` (its handover);\n   - `doc/HANDOVER/Claude_Primary_Handover_H1_v1r6.md` (Claude's handover; the project's working rules);\n   - `doc/RATIFICATION_REGISTER_v0_20.md` (the record of every decision and install; read its newest sections);",
     "   - `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md` (its handover);\n   - `doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md` (Claude's handover; the project's working rules);\n   - `doc/RATIFICATION_REGISTER_v0_23.md` (the record of every decision and install; read its newest sections);"),
    ("exactly the same rights and the same independence. You are not the coder, and there is no separate ChatGPT coder\nany more: Claude writes all the code.",
     "exactly the same rights and the same independence. You are not the coder, and there is no separate ChatGPT coder\nany more: Claude writes all the code. (A previous ChatGPT reviewer chat held this role from 30 October 2026;\nreplace that date with its last date when you use this text.)"),
    ("FIX AND PROCEED or RECHECK (`review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`). The last message was EX_076;\nthe next free number is EX_077. End each reply with a short summary the owner can paste back.",
     "FIX AND PROCEED or RECHECK (`review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`). The last message was\n`<last EX number>`; the next free number is the one after it. End each reply with a short summary the owner can\npaste back."),
]
u = apply(u, E2)
old_state2 = section(u, '**Where things stand (30 October 2026).**', '**Hard rules (binding).**')
u = apply(u, [(old_state2, """**Where things stand (1 November 2026, at the snapshot; check the register for later events).**
- **Released and running on past draws:** all 40 method variants, in both games (REL-1 and E_1 revision 2). The
  first walk-forward batches are done (Powerball 17,280 runs; Oz Lotto 8,760), every run `SUCCESS`.
- **The scorer and ranking report (WF-1B)** is installed (`24d192f`), with the fair-draw simulator N1 (R = 10,000)
  and the owner-approved NIST seed policy `N1_ROOT_NIST_C2_20261031T1030Z_V1`. PERF-1 makes its exact uncertainty
  interval fast with identical results (installed at `3fce327`). The first two ranking reports are committed
  (`441daf2`, `608025c`).
- **Tests:** 471 offline tests pass on Windows and Linux.
- **Your predecessor's reviews since EX_077** caught, among others: a driver that would continue after a data
  failure (WF1-R3-B01), a resume rule that bound neither the master nor the batch (WF1A-R2-B01), an archive check
  that missed paths built in pieces (E1R2-R2-B01), parallel stop-admission gaps (EX_105 B01) and an unbound seed
  record (WF1B-R2-B01). All are fixed.
- **Next, in the owner's order:**
  1. Mode H, the results update and the prospective (next-draw) mode, designed together; goal: forecasts for the
     draws of the week of 9 November 2026. Mode H scores all ten holdout draws per game, with Powerball 1585 and
     1586 flagged for a recorded exposure (owner decision HX-1);
  2. WF-1C, the workers change, carrying EX_101's and EX_105's obligations;
  3. wave 3, with the owner's Method B as E_45;
  4. a non-local means discussion, waves 4 to 11, and the ensembles last.

""")])
u = apply(u, [
    ("- The four safety switches stay False, and the allowlist stays empty.",
     "- Three safety switches stay False; the fourth (`ENABLE_CONTRACT_REAL_DEVELOPMENT`) is on for owner-authorised\n  development runs only. The allowlist stays empty."),
    ("**Your first reply** goes to the owner, not to Claude. Please read the attachments first: H-2 v1r7 in full, then\nH-1 v1r6, the register's newest sections and the roadmap. Then reply, in plain English, with:",
     "**Your first reply** goes to the owner, not to Claude. Please read the attachments first: H-2 v1r8 in full, then\nH-1 v1r7, the register's newest sections and the roadmap. Then reply, in plain English, with:"),
    ("5. **a takeover check of H-2 v1r7.** Claude drafted it on the owner's instruction, because your predecessor could\n   not, keeping the reviewer-rights region byte-identical (7,676 bytes; check its SHA-256 against the one H-2 records).",
     "5. **a takeover check of H-2 v1r8.** Claude drafted it, keeping the reviewer-rights region byte-identical (7,676\n   bytes; check its SHA-256 against the one H-2 records)."),
])
assert u.endswith('\n') and u.isascii()
open(o2, 'wb').write(u.encode('ascii'))
for p, s in ((o1, t), (o2, u)):
    print(p, hashlib.sha256(s.encode('ascii')).hexdigest(), len(s.splitlines()), 'lines;',
          len(re.findall(r'\[\[FILL: [^\]]*\]\]', s)), 'placeholders')
