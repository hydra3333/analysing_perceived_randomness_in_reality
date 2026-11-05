# HANDOVER_2026_11_06 - emergency handovers after the ChatGPT reviewer chat ended (Claude, 6 November 2026)

The ChatGPT reviewer chat reached its conversation limit on 6 November 2026 without writing a handover. On the project owner's
instruction, Claude (the surviving chat) wrote the files below, most critical first, committing each as it was finished.
None of them is owner-ratified or reviewed. They go into doc/HANDOVER/ in the next documentation package, with register v0.25
(reminder R-022).

## Files

| File | Bytes as stored | SHA-256 as stored | SHA-256 after CRLF->LF |
|---|---|---|---|
| `Claude_Primary_Handover_H1_v1r9_delta.md` | 19396 | `f3f78b2e75bae241321c49e5b517ef5cf424a46a26b77da0b8c28c51d00a09c5` | `a05e4b9c05df4633c340d61b84f0f48b9345f6eacacb29530e53fc9a2edaa9d5` |
| `Claude_Primary_Handover_H1_v1r9_introductory_blurb.md` | 9428 | `ead74669df8f7191d79f731d5b6cfe15f9e91e4fd9d99d22ea0c015fd54aa2fb` | `d40ff56a2dc28315338c65040c405e3f39029f1b635c2b527717991008619f38` |
| `ChatGPT_Reviewer_Handover_H2_v1r9.md` | 33869 | `7dbc1438134a82a7bbc36920b89d0b0a73d3d95bbdc0ac7905ee069ee0c0d686` | `7dbc1438134a82a7bbc36920b89d0b0a73d3d95bbdc0ac7905ee069ee0c0d686` |
| `ChatGPT_Reviewer_Handover_H2_v1r9_introductory_blurb.md` | 8797 | `5e33b0023022a7251d8184a2cb0697a7c3cdb650b626640b96739b6927d06902` | `2674bdb52e6c05402138719ccbd1bbf184edc16f69f8e2494c1e138f718643b1` |

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
- Related updates: exchange/OWNER_REMINDERS.md (R-016, R-020 (d)-(f), R-022), exchange/OWNER_ROADMAP.md (the NOW line), and
  exchange/CLAUDE_WEB_TOOLS/mhupa/slice2_checkpoint/CHECKPOINT_slice2.md (the status line).
