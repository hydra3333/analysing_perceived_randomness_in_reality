# H-2 v1r11r1 - focused correction and installation plan (CANDIDATE; not authorised)

Source: EX_169_ChatGPT at Git main 959b072; Claude factual check PASS WITH CORRECTIONS (C1-C5 editorial; O1-O2 optional), reported by the owner on 14 November 2026. This is r1 of the same v1r11 supplement, not a new review of the underlying science and NOT owner ratification. Original EX_169 is immutable and remains in exchange/. This EX_170 carries the corrected full versions and a counted full-line diff.

## Scope

EX_169 -> r1 changes exactly NINE complete source-text lines: six in the v1r11 delta (C1 witness push separate from Approval 1; C2 one successful updater transaction and qualified STOP; C3 backup confirmation only; C4 unopened/SEALED disambiguation; C5 dynamic H-1 pointer; O2 named T016 tool restriction), two in the introductory blurb (C4 and C5), and one in the continuity index (O1 retired acquisition tooling clarified). The first updater STOP case in C2 is necessarily qualified as a PRE-BACKUP ADMISSION STOP; an interrupted update after master replacement can leave master/ledger mismatched (EX_167 B02). No change to scientific protocol, owner gates, reviewer rights, prior documents or installed code. The diff `H2_v1r11_TO_v1r11r1.diff` shows every changed line.

## Exact target paths (owner only, after factual recheck and approval)

- `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_delta.md`
- `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_continuity_index.md`
- `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r11_introductory_blurb.md`

The nested `H2_v1r11r1_DOC_HANDOVER_OVERLAY.zip` contains exactly the three relative target paths, LF ASCII, no others; it does not alter any existing ratified H-2 v1r4/v1r8/v1r9/v1r10, H-1, registers, code, tests, user data or safety gates. The flat copies in EX_170 are CRLF ASCII for exchange. `H2_v1r11r1_MANIFEST_SHA256.txt` lists exact digests of both representations and the nested overlay. The previous EX_169 candidate MUST NOT be installed instead of this corrected edition.

## Review, decision and installation route

1. Claude performs one focused line-diff and hash recheck against EX_169 (already fact-checked), confirms ONLY requested C1-C5/O1-O2 changes, verifies LF/CRLF equivalence, validates three-file allowlist, checks no science authority or reviewer-rights edits, and reports PASS or an exact discrepancy. No new full review is needed unless unexpected changes are found.
2. The owner alone approves or ratifies the corrected H-2 v1r11 supplement and exact three-file installation, separately from any Mode H approvals. The owner may first explicitly decide the *separate future* consolidation proposal: full H-1 v2/H-2 v2 only AFTER BOTH Mode H studies are `MODE_H_SEALED`, before MHUP-B detailed design. This proposal is NOT RATIFIED by this package.
3. Extract the nested overlay only into an owner-chosen staging folder OUTSIDE the project, compare exact archive inventory and SHA-256 against the manifest, then copy only the three LF target files into `doc/HANDOVER/` under the owner's approved manual install route. Verify tree changes list exactly three `A` files (unless an earlier candidate was manually placed: then STOP and reconcile, do not overwrite blindly). Stage exactly those paths, inspect `git diff --cached --name-only` and `git diff --cached --check` and the committed Git-blob SHA-256s (not hashes of CRLF working copies). Commit and push by the owner only.
4. Claude independently fetches the resulting committed Git contents and compares all three LF digests, confirms H-2 v1r9's protected reviewer-rights block is untouched, and records the installation commit. No previously ratified file is moved/deleted.
5. Start a fresh ChatGPT reviewer chat only after the approved handover is installed and the owner chooses to transfer. Read H-2 v1r9 FULL, v1r10 delta, v1r11r1 delta, continuity index, blurb, latest ratified H-1 delta, latest register and fresh EX messages; verify current HEAD and latest owner decisions before working. No Mode H preflight, Lotterywest-GOV request, master update, holdout opening, score, MHUP-B work or other owner-go operation is authorised by handover preparation or review.

## Relevant anchors

- EX_169 recorded unchanged at Git `959b072281bb62d74632db36698ef3dfd946f123` (owner/Claude reports factual PASS with editorial corrections).
- EX_168 was recorded before this checkpoint; r2a readiness was at `496731c9d5668f4af0c9b2d996974bdc3b6f7f94`.
- H-2 v1r9 rights region: 7,676 UTF-8 LF bytes, SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db` (verified without editing any prior file).

End of focused plan. Nothing here is an owner go.
