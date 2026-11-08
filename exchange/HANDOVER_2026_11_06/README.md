# HANDOVER_2026_11_06 - handovers (Claude, 6 and 8 November 2026)

**Read on 8 November 2026 or later:** start with `Claude_Primary_Handover_H1_v1r10_delta.md` and its blurb. They supersede the
6 November v1r9 delta and blurb, which stay as history. H-2 v1r9 and register v0.25 were ratified by the owner on 6 November 2026
(RAT-25) and installed in `doc/` (DOC-12); the copies here are the candidate history.

The ChatGPT reviewer chat reached its conversation limit on 6 November 2026 without writing a handover. On the project owner's
instruction, Claude (the surviving chat) wrote the files below, most critical first, committing each as it was finished.
None of them is owner-ratified. The new reviewer checked candidate 1 in its takeover (EX_153). H-2 v1r9 and register v0.25
are now candidate 3, with its corrections (EX_154, EX_156; C01 passed on RECHECK in EX_155). The copies the owner placed in doc/ at 929eff5 are candidate 1. They go into doc/HANDOVER/ in the next documentation package, with register v0.25
(reminder R-022).

## Files

| File | Bytes as stored | SHA-256 as stored | SHA-256 after CRLF->LF |
|---|---|---|---|
| `Claude_Primary_Handover_H1_v1r10_delta.md` | 25778 | `c7ef7513efc8c507469dbc94a60e694997ac660a2b69d20a58057075aa375a1e` | `b1f2e72f79f7d541b869ffa343484f0d853dc56ef21d81317a799f32f0e99850` |
| `Claude_Primary_Handover_H1_v1r10_introductory_blurb.md` | 9167 | `f08ca0f6d928bc4a4edcdff26f2f0e3f010c40741152aead2a210ea7209ee143` | `18ca7f9f4e361c2a29f88de9f271c7d7f939fcbf9b365430c1275776545387ed` |
| `Claude_Primary_Handover_H1_v1r9_delta.md` | 19396 | `f3f78b2e75bae241321c49e5b517ef5cf424a46a26b77da0b8c28c51d00a09c5` | `a05e4b9c05df4633c340d61b84f0f48b9345f6eacacb29530e53fc9a2edaa9d5` |
| `Claude_Primary_Handover_H1_v1r9_introductory_blurb.md` | 9465 | `1ba881544c1f616d2b9aeaa0caacefce6324dd9a47b7f4c4adbd3617d6e043af` | `56d0ba6029e51b7a6fc6727fa1c7e8a660fed5832f6fec2a130f7b680e974f35` |
| `ChatGPT_Reviewer_Handover_H2_v1r9.md` | 36053 | `95cc98a728b0642de9cde2b28142d53eb5e494d9a05676ce073fa1622f1b291a` | `95cc98a728b0642de9cde2b28142d53eb5e494d9a05676ce073fa1622f1b291a` |
| `RATIFICATION_REGISTER_v0_25_CANDIDATE.md` | 272225 | `e36e451750b6ffae3e9bc3a7e79100fbbcd47a3ae2eff9d334ef52f0d57605a7` | `e36e451750b6ffae3e9bc3a7e79100fbbcd47a3ae2eff9d334ef52f0d57605a7` |
| `ChatGPT_Reviewer_Handover_H2_v1r9_introductory_blurb.md` | 9096 | `bd44901429b94552dd1a78494048c595912b7c913265052f6e5ca9a4b414172a` | `f29b2f30e445b0f52cd3acff3866294b8bda2a44629c95aca7266962dc70f97d` |

## How to use them

- **A new Claude chat:** paste the text below the line in the **H-1 v1r10** blurb. It reads H-1 v1r8 (doc/HANDOVER/), then the
  v1r10 delta.
- **A new ChatGPT reviewer chat** (only if the current one, in place since 6 November 2026, has to be replaced): attach the
  files the H-2 v1r9 blurb lists (use the installed doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md and
  doc/RATIFICATION_REGISTER_v0_25.md, both ratified, plus the H-1 v1r10 delta) and paste the text below its line, updating its
  "where things stand" from the v1r10 delta first.
- **If both chats are new:** start the reviewer first, accept its takeover check, then start Claude, so that the reviewer can
  check Claude's first reply.

## Notes

- H-2 v1r9 is LF and UTF-8: its protected reviewer-rights region needs UTF-8, and it is built from v1r8's Git blob by
  exchange/CLAUDE_WEB_TOOLS/handover/build_h2_v1r9.py, which asserts that region (7,676 bytes, SHA-256 70e50dc3...).
  The other three files are ASCII with CRLF line endings.
- Register v0.25 CANDIDATE (added 6 November 2026, after the owner noticed that v0.24 was out of date) is LF and UTF-8, like
  every register edition. It is built from v0.24's Git blob by exchange/CLAUDE_WEB_TOOLS/register/make_register_v25.py, which
  keeps every v0.24 line except the version line, and inserts the new section before 'Interpretation and verification'.
- Related updates: exchange/OWNER_REMINDERS.md (R-016, R-020 (d)-(f), R-022), exchange/OWNER_ROADMAP.md (the NOW line), and
  exchange/CLAUDE_WEB_TOOLS/mhupa/slice2_checkpoint/CHECKPOINT_slice2.md (the status line).
