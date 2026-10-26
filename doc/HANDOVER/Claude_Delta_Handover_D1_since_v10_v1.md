# Claude delta handover D-1 (since reviewer handover v10), v1

**From:** Claude, the earlier reviewer chat (author of reviewer handover v10, review methods kit v2 and the Package 2 v0.11 review).
**To:** the new Claude chat.
**Date:** 26 October 2026, late evening (Adelaide).
**Builds on:**
- reviewer handover v10 (CRLF `6ad47c56770a29e48c0dce9e61095bf55a811a1789ad4b6cb34e37697b6e6547`; Git LF `61a5127816d30e2ffc342a011e3d029d7a3a6a80bc55c368751cc9d09ed9b191`), committed at `618fe48`;
- review methods kit v2, `21d757fb41aaf220200259dd01bc49047a3c702139db85d4ad61a728ac81313c`;
- my answers to your takeover questions.

**Status:** a delta note under section 9.3 of the agreed roles position. Writing it does not make it authoritative. Reconcile it against the repository and the files it cites, as usual. It grants no run, test, data, holdout, termination or Git permission.

**After this note** the earlier Claude chat retires, and returns only in exceptional circumstances. **You take over entirely, with no cross-check by the earlier chat.**

## 1. What has happened since v10, in order

1. **Package 2 v0.11 review** (mine, in kit v2): `Claude_Review_Package2_v0_11_v1.md`, `e3466a8e87c945ee462a6914024821cbb747ade4f10ddf0f616675a98451a197`.
   - **B1 BLOCKER:** `DrawView.order_evidence` carries `master_sha256`.
     - In the scratch tree (`618fe48` plus the v0.11 overlay), `src/methods/_common/game_draws_reader_v1.py` hashes the whole master at about line 257. That part is correct, because it is orchestration-side integrity.
     - At about line 269 it places that hash into `order_evidence`. That is the leak.
   - **C1 CORRECTION:** assert the ratified R2 5.5 synthetic goldens.
2. **Package 2 v0.11-r1:** the ChatGPT coding chat has produced `Predictive_Randomness_MultiGame_Package2_v0_11r1_FOCUSED_CLAUDE_REVIEW.zip`. Its reported SHA-256 is `7bddda746f56668fbc60af9826cee83c7fd95031dfd3c9b4b474641cc2734635`.
   - Its stated purpose is to fix B1 and C1.
   - **Neither Claude chat has received it.** It and the coding chat's original blurb come to you verbatim.
3. **MR integration v2 (yours):** `Predictive_Randomness_MR_Integration_Candidates_v2.zip`, `9f087fcf4fea3ec232caff0f928e20ffeb662f6c251cdc97a23ebdaa5d04f628`, on base `618fe48`.
   - It passed my check.
   - The ChatGPT reviewer's focused review is `Independent_ChatGPT_Focused_Review_MR_Integration_Candidates_v2.md`, `66db6b1e0f67635160342c4ca30d05f99c9968f6bc15885d987e16ce5b221ea0`. It found 0 BLOCKER, 1 CORRECTION (C-v2-01) and 0 OPTIONAL.
   - **C-v2-01:** register v0.4 line 95, second sentence, says "as amended only by the already owner-ratified MR proposal". That omits the separately owner-approved O-02. The exact replacement is in that review's C-v2-01 section; use it verbatim.
   - **My optional suggestion:** reword register line 4 to "The pre-integration consolidated editions below were owner-ratified 26 October 2026". Apply it only if the owner approves.
   - I have seen no v3, no ratification and no commit after `618fe48`. If you have not received the focused review, ask the owner for it.
4. **Roles discussion:**

   | File | Author | SHA-256 | State |
   |---|---|---|---|
   | Discussion paper v0.1 | ChatGPT | `75af18cfac1250c4fe0afd18ef63024c05669596d432da189f654f8dfd0f0ca5` | source |
   | `Claude_Response_AI_Roles_Discussion_v0_1_v1.md` | earlier Claude | `38849c1dba7dfa80665fcb822d3ff88d8056c5a6d891e6f974d0a68a216047fd` | superseded by v2 |
   | `Claude_Response_AI_Roles_Discussion_v0_1_v2.md` | earlier Claude | `90f2461be10d4f42565c54ec46fb7052d228d47805a82729d6d4557d723cd02d` | source |
   | ChatGPT response to v2 | ChatGPT | `3e077fa51de1d66c2c7d9d82b96cf83b35bfd893ef47851158333e992b08363d` | source |
   | `Predictive_Randomness_AI_Roles_Agreed_Position_v0_1.md` | earlier Claude | `3b4c719c4c09e10b1e410a9c2e6a4f0dd49cbb292a603a0e2673a0f2825aa213` | superseded by v0.1r1 |
   | `Predictive_Randomness_AI_Roles_Agreed_Position_v0_1r1_CHATGPT_REVIEW_CORRECTIONS.md` | ChatGPT corrections | `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b` | **the edition the owner is ratifying** |

   - **v0.1r1 encoding:** UTF-8 with LF endings. It contains two em dashes and one minus sign in "N-1". The R-2 and R-4 cells repeat their own labels. These are cosmetic. Leave them, so the ratified bytes stay as reviewed.
5. **Owner direction:**
   - The earlier Claude chat retires after D-1, without a cross-check.
   - The owner's priority is **getting the project running**, not measuring the role change.
   - The owner expects you to **lead them through the next steps**.

## 2. Role state, and when it changes

- **Until the effective commit:** the current roles stand.
  - You are the **independent reviewer** of v0.11-r1, which ChatGPT wrote.
  - You are the **document author** of the integration, which you wrote.
  - The ChatGPT coding chat writes any r2.
- **The effective commit** is the one the owner names. The default is the commit that accepts Package 2 v0.11. From that commit you are primary designer and coder, and the ChatGPT reviewer chat is the independent reviewer (agreed position, sections 1-9).
- **Your handover H-1:** draft it against the *accepted* baseline, which means after step 2 below. Until then, keep a running checkpoint file, so nothing lives only in your chat.

## 3. Next steps: what, who, in what order

| # | What | Who | Output and gate |
|---|---|---|---|
| 1 | Ratify agreed position v0.1r1 and commit it, with the sources in section 1 item 4 kept as history (for example under `doc/` and `review/`; the owner chooses the paths) | Owner | Commit. Roles do not change yet. |
| 2 | **v0.11-r1 review** (Option A). Check the ZIP hash on receipt, then follow kit README 2.4 and the checklist in section 4. Any r2 goes to the ChatGPT coding chat; repeat until accepted. | You review; ChatGPT coding chat authors | Your review with a paste block. The owner accepts and commits. **That commit is the default effective commit.** |
| 3 | **Integration v3** (parallel to step 2; the steps that follow it are in section 5) | You author; ChatGPT reviewer checks | The owner ratifies and commits the five editions |
| 4 | **ADD-2 knowledge-transfer note.** Ask for it early, while that chat is alive. Covers the module map, non-obvious choices, defects and uncertainties, Windows-only checks, untested paths and improvements. | The owner asks the ChatGPT coding chat; you read it and ask follow-ups | It supplements source review; it is not authority |
| 5 | **H-1** (Claude primary; you write it, ChatGPT reviews), **H-2** (ChatGPT reviewer; ChatGPT writes it, you check the facts, the owner alone checks the rights section) and **H-3** (transition record; you draft it, the owner ratifies) | As shown | The owner installs all three together at the effective commit, so there is no authority gap |
| 6 | **E_2-readiness specification** (MR v0.5 section 13 stage 1; agreed position section 10) | You draft; ChatGPT does a design review | The owner ratifies the schema before any code |

**Sources for H-1:**
- the repository at the effective commit;
- v10;
- this note;
- coder handover v1.1r1;
- ADD-2;
- MR v0.5 and the installed editions;
- kit v2;
- agreed position v0.1r1.

**H-3** records the agreed-position ratification and the effective commit. Record those in the *next* register edition, not in v3. That keeps v3 a narrow fix.

## 4. B1 and C1 closure checklist for v0.11-r1

From my response v2, section 6. Your review confirms all of these:
- **No hash in the view:** no `DrawView` attribute holds a 64-hex value equal to the master, ledger or INIT-record file hash.
- **`order_evidence` contents:** only the evidence record's file name and the status label `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`.
- **T-05 test for each of the three view kinds:** use a fixture ledger re-pinned to a master whose rows at and after N have been changed. Every method-visible field, every array's contents and bytes, the schema, the digest and the capability data must be identical. Orchestration-side provenance may differ (agreed position, section 5).
- **Manifest:** the master SHA, ledger version and INIT identity remain in the run manifest and receipt, on the orchestration side.
- **The old order-evidence test** (about line 143 of the reader tests) is updated, and the closure text no longer says "separately bound SHA metadata" for the view.
- **R2 5.5 / TIE v0.2 goldens asserted:** `df21871f...` (training view), `7ce5ab1b...` (MAIN label-3 tie) and `7b43d659...` (canonical forecast). They come from `tests/p3_e1_synthetic_v0_3.json` at target 1152, using the committed v0.3 module. Kit script 06 recomputes them.
- **Standalone-runner synthetic set:** `3851fa46...` / `8a7f917a...` is kept and labelled as distinct from the ratified set.
- **Unchanged elsewhere:**
  - the full suite reruns offline (v0.11 gave 56 OK and 1 skip);
  - the exact coordinator diff still rebuilds the shipped coordinator;
  - all 11 protected ASTs are identical (kit script 05);
  - all three switches are `False`;
  - `_COORDINATED_SCIENCE_ALLOWLIST` is empty;
  - the real E_1 goldens are still asserted.
- **Scope:** the delta is limited to B1 and C1, plus any declared extras, each of which you review.

## 5. Integration v3: shortest closure

1. Apply C-v2-01 verbatim, and the line-4 wording only if the owner approves it.
2. Regenerate the register SHA-256 and the package manifest.
3. Ship the v2-to-v3 diff, with proof that the other four editions are byte-identical to v2.
4. The ChatGPT reviewer does a mechanical check: diff scope, verbatim text and hashes.
5. The owner ratifies and commits.
6. Check after the push with `git show HEAD:<path> | sha256sum` against the manifest.

## 6. Points not in v10

- **Paste blocks:** label each paste block with its destination chat. The owner was once confused about which chat a block was for.
- **When consolidating agreed text, copy the agreed wording verbatim.** In agreed-position v0.1 I paraphrased replacement wording that had already been agreed, and ChatGPT had to restore it in v0.1r1. Restyle only your own new text.
- **Integration authorship:** you drafted v1 and v2. I checked both for the owner. In v1 I missed two cross-reference relics, which the ChatGPT reviewer caught; the kit README now includes a cross-reference check (2.3 item 6).
- **New boundary rules in the agreed position** that bind your work as primary:
  - no lottery-results searches by any project session;
  - no pushes or pull requests;
  - the Git transport is a proposed default (`git diff --binary`, then `git apply --check`), pending a separate owner decision;
  - R-2 reproduction is gated by safety and authority;
  - R-4 oracles are proportionate;
  - risk tier is set by what is touched;
  - the RECONSIDER class;
  - the two-round rule applies on unchanged evidence;
  - mixed-author changes go back to the other model.
- **Same-model checks:** a second Claude chat is never the independent review. That includes this one.

## 7. Closing

You have everything this chat holds that matters: v10, the kit with every script, input and review, the takeover answers and this note.

If something contradicts the repository, the repository and the owner's ratified records win. Tell the owner. Do not resolve it silently.

*End of document.*
