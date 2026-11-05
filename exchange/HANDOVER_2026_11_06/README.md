# HANDOVER_2026_11_06 - emergency handovers after the ChatGPT reviewer chat ended (Claude, 6 November 2026)

The ChatGPT reviewer chat reached its conversation limit on 6 November 2026 without writing a handover. On the project owner's
instruction, Claude (the surviving chat) wrote the files below, most critical first, committing each as it was finished.
None of them is owner-ratified. The new reviewer checked candidate 1 in its takeover (EX_153). H-2 v1r9 and register v0.25
are now candidate 2, with its corrections (EX_154). The copies the owner placed in doc/ at 929eff5 are candidate 1. They go into doc/HANDOVER/ in the next documentation package, with register v0.25
(reminder R-022).

## Files

| File | Bytes as stored | SHA-256 as stored | SHA-256 after CRLF->LF |
|---|---|---|---|
| `Claude_Primary_Handover_H1_v1r9_delta.md` | 19396 | `f3f78b2e75bae241321c49e5b517ef5cf424a46a26b77da0b8c28c51d00a09c5` | `a05e4b9c05df4633c340d61b84f0f48b9345f6eacacb29530e53fc9a2edaa9d5` |
| `Claude_Primary_Handover_H1_v1r9_introductory_blurb.md` | 9465 | `1ba881544c1f616d2b9aeaa0caacefce6324dd9a47b7f4c4adbd3617d6e043af` | `56d0ba6029e51b7a6fc6727fa1c7e8a660fed5832f6fec2a130f7b680e974f35` |
| `ChatGPT_Reviewer_Handover_H2_v1r9.md` | 35778 | `3a4e2e5d4917a3cf4caf3d6c15431f3ca0b760ee40a52d4e6d5c81208b667dbe` | `3a4e2e5d4917a3cf4caf3d6c15431f3ca0b760ee40a52d4e6d5c81208b667dbe` |
| `RATIFICATION_REGISTER_v0_25_CANDIDATE.md` | 271683 | `c676b1c1c4d930d1dcfe73181fcc5252215af27a1b2b07b0265c288793596a19` | `c676b1c1c4d930d1dcfe73181fcc5252215af27a1b2b07b0265c288793596a19` |
| `ChatGPT_Reviewer_Handover_H2_v1r9_introductory_blurb.md` | 9096 | `bd44901429b94552dd1a78494048c595912b7c913265052f6e5ca9a4b414172a` | `f29b2f30e445b0f52cd3acff3866294b8bda2a44629c95aca7266962dc70f97d` |

## How to use them

- **A new Claude chat:** paste the text below the line in the H-1 v1r9 blurb. It reads H-1 v1r8 (doc/HANDOVER/), then the
  delta.
- **A new ChatGPT reviewer chat:** attach the files the H-2 v1r9 blurb lists and paste the text below its line. Its first reply
  is a takeover check of H-2 v1r9.
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
