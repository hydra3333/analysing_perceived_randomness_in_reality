# H-2 v1r11 - Review/installation plan (CANDIDATE, not authorised)

Scope: new independent-ChatGPT-reviewer continuity files only. The author deliberately does NOT rewrite, move or delete existing H-2 v1r4/v1r8/v1r9/v1r10, H-1, H-3, roles, register, design, code, tests or owner working lists. No change to authorisations, no permission to run science. The owner asked ChatGPT to prepare all its own handover-related documents after EX_168; this is the proposed package and its exact location.

## File placement after independent factual review and explicit owner approval

| Candidate file | Proposed repository path | Purpose |
|---|---|---|
| `ChatGPT_Reviewer_Handover_H2_v1r11_delta.md` | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_delta.md` | current status and continuing binding inheritance |
| `ChatGPT_Reviewer_Handover_H2_v1r11_continuity_index.md` | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_continuity_index.md` | complete decision/evidence/deferred-work map |
| `ChatGPT_Reviewer_Handover_H2_v1r11_introductory_blurb.md` | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_introductory_blurb.md` | paste-ready startup text for a new reviewer chat |

For convenience the inner `H2_v1r11_DOC_HANDOVER_OVERLAY.zip` contains ONLY those three paths with LF line endings, already placed under `doc/HANDOVER/`; no current file is overwritten. The same documents appear as flat CRLF ASCII members of `EX_169_ChatGPT.zip` under their bare names for the one-upload AI-to-AI exchange protocol. LF and CRLF hashes differ by design, contents otherwise equal after line-ending normalisation. Read the manifest for exact hashes. Keep the overlay in a staging folder outside the repository; do not commit the ZIP itself as an installed handover file.

## Review checklist (Claude, then owner; no new science work)

1. Check repository current HEAD and source names; compare these new documents to H-2 v1r9, the ratified H-2 v1r10 delta, latest register, latest H-1 and EX_164-EX_168. Confirm every current historical fact or identify an EXACT correction. In particular: RAT-28/29/30, 571/571 test-only fix, current reviewer EX_168, readiness r2a, no execution gos, D1-D7 pending and Q7 decided.
2. Independently check the old H-2 v1r9 rights-region bytes: from the anchored heading `## 2.` through immediately before anchored `## 4.` in Git LF form; expected 7,676 bytes, SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db`. Do NOT modify that region. Check that all prior documents remain in place, including v1r4 and v1r8.
3. Confirm the package adds ONLY three new `doc/HANDOVER/` files with no other tree changes. The installed `doc/HANDOVER` LF SHA-256s are supplied in the manifest. Compare the inner overlay's member inventory and each digest with the manifest; refuse path traversals, symlinks, duplicates or other paths. The reviewer has not executed a Windows installer, since no new owner-run installer is required for three new Markdown files.
4. Get the owner's **specific ratification/approval of this H-2 reviewer handover update** before any main-tree installation. No EX record committed by Claude creates ratification. The owner commits and pushes after checking the staged diff includes exactly the three paths; Claude independently re-reads GitHub bytes afterward and reports verified full identities. Do not amend an earlier commit or rewrite historical handovers. Candidate files in `exchange/` remain evidence, not authority.
5. New reviewer chat must be told to read v1r9 + v1r10 + v1r11 in sequence, verify rights/authority and answer the owner before undertaking work. No new reviewer chat is mandatory until the owner wants to transfer.

## External verification hints (owner's Windows CMD; NOT a command to execute now)

- Stage only: `git add doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_delta.md doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_continuity_index.md doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_introductory_blurb.md`.
- Check before commit: `git diff --cached --name-only`, `git diff --cached --check` and `git status --short` (exactly three added files; no deletion/rename); a script should additionally check the three staged *byte* SHA-256 values against the manifest, since CRLF working copies may differ from LF Git blobs.
- After commit and before push, verify SHA-256 from `git show HEAD:<path>` (Git byte content, not `certutil` on CRLF checkout), and verify historical H-2 rights still match. Then the owner pushes. Claude's independent read of GitHub is the final installed-byte check.
- Do not install during a Mode H closure freeze unless the owner explicitly reviews the exact scope; even a docs-only change must not create another reason to `git pull` that rewrites local frozen files. Better to complete this documentation before Approval 1, as requested.

## Status of this install plan

DRAFT ONLY. No GitHub write, no owner ratification, no Python test, no Lotterywest request, no POC run, no Mode H approval. Prepared on the current reviewer chat's instruction and for the owner's later placement/commit decision. All package digests are generated locally for verification, not external timestamps.
