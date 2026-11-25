# H-1 v14 independent documentary cold read - PASS for continued use

Date: 2026-11-25 (Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Reviewer: ChatGPT
Authority: the owner's request to perform the cold read owed under RAT-58 (entry 286).
Status: reviewer handback, not an EX; no new ratification, operational GO or change of role.

## 1. Disposition

PASS for continued use. The H-1 v14 documentary cold read is complete. No blocker, loss of independent reviewer rights, or material weakening of the ratified science or safety contract identified. The consolidation of the live position is useful. Retain RAT-58 and the installed edition. The minor documentary corrections below are for the next ordinary refresh, not a request for a new edition now.

This is separate from EX_323 and the slice B focused recheck. No slice B working increment was reviewed as part of this task. Use the non-EX reviewer handback form (exchange/README.md v0.6) so as not to consume the next shared EX number while Claude prepares its correction reply.

## 2. Evidence and scope

Fetched main at d0db9a16c37fe9e3b4d7868565aeef2b5c56baa1 (Claude's slice B working corrections after EX_323). Reviewed H-1 v14 as installed at 8d02da8611063b49aa81dd6e5b3a48dff44764a1, against its own evidence cutoff d2b6bc99eca7f5e13c71ee1a37faa029760e2889, rather than treating later work as a defect in the edition.

Independently recomputed exact Git-byte SHA-256 of installed H-1 v14, its blurb, H-1 v13 and v7r1. H-1 v14 and blurb are US-ASCII CRLF (2075 and 58 line endings respectively, no lone LF), matching their recorded hashes. The installed files equal the builder's FINAL documents retrieved from Git. Mechanically compared sections 1, 2 and 2A with v13 (exact CRLF content preserved), and with v7r1 (same substantive text after line-ending normalization and section separator handling, not raw byte equality). Compared moved sections 0B, 0D and 0E with v13: their section content is retained exactly, with the new HISTORY wrapper and end-of-edition line outside it. The original reviewer rights in section 1.4 are intact.

Read chapter 0, sections 0A/0C, sections 1-12 as present, appendices A-C and the introductory blurb. Read EX_317, entry 270 and the relevant later log entries, current exchange protocol and file-form standard. The moved historical sections were checked by byte/content comparison rather than laboriously re-reviewing their old claims. The principal governing file identities had been verified at takeover; the Git comparison from b9af987 through the review head shows no changes to specification v0.6, deployment v0.12, coding practices, file-form v0.2, H-2 v9, root live infrastructure manifest, installed OV-1 kernel, exchange protocol or runner rulebook. The present main manifest counts independently read are 13 forecast, 17 derived, 3 other = 33. I have not re-run the builder or repeated Claude's earlier 131-hash audit, checked every historical reference in Appendix A against its original commit, re-reviewed the code, or run any project or owner-PC commands. Prior EX_317's nine explained Appendix A differences remain historical rather than unexplained changes.

## 3. Disposition of EX_317 and entry 270

- H13-C01: addressed. Section 7.3 correctly confines byte equality of the reviewed OV-1 kernel to the step 2 installation and explains CRLF conversion; no alleged suite equality test. No scientific change.
- H13-C02: substantially addressed by 0.6 and 0.7. They expressly supersede old LF verifier advice, preserve historical identities, reject normalizing present hashes and remove the old dual-clone requirement. The remaining overbroad wording is H14-C01 below.
- H13-C03: addressed by 5.3 and 0.5 item 7. Required installed inventory/log preserved, no release registry or Git outside DEV.
- H13-C04: substantially addressed. Chapter 0 prevails, the layered 0B/0D/0E sections are clearly history, the current installed state, counts, RAT-56 and the step-3 order are available from the live chapter. Section 7.1's older manifest count and 7.5's earlier state are explicitly superseded by 0.7. No need for a further consolidation round.
- H13-O01: addressed; retired checker is historical and not to be maintained. No new link engineering or retired-system work.
- H13-O02: addressed in Appendix C. V14's own no-prior-review wording is accurate; v13 had a focused prior check but not its full cold read.
- Entry 270 (a)-(h): addressed by the new reading route, current handover/register pointers, live manifest count, attributes correction and OV-1 qualification. Its six substantive recommendations are carried, with the environment digest decision now expressly attributed to the owner (entry 275). No reopening.

## 4. Corrections for the next ordinary edition only

H14-C01 - Exact file-form scope (0.6; 0.2; blurb; section 4 opening and Appendix A).

0.6 says "Files that existed before 25 November 2026 keep their form." Read literally that would also exempt previously existing living code and settings, which were deliberately converted. It also states that file bytes are the same in Git, a clone and the owner's disk without restricting that claim to tracked files covered by -text, at the same revision. The ratified standard governs instead. At the next refresh say: frozen history keeps its recorded bytes, existing living files were converted under RAT-50 and follow the current standard, the expressly named exceptions and GAIS retain their own rules, .venv and other excluded third-party/generated material are outside the standard's scope, JSONL and cloud .sh remain LF. Compare current identities exactly; historical LF hashes identify their historical bytes. Make the section 4 heading and Appendix A heading say which revision/form each table represents, rather than a blanket "Git content (LF)" and a current HEAD check for historic rows. Preserve the nine explained historical identities; no conversion, operational Git check or repeated hash audit.

H14-C02 - Wording of the preservation claim (header; 0C; Appendix C).

The claims of byte-for-byte preservation from v13 are supported. V7r1 itself is LF (925 line endings) whereas v14 is CRLF. The protected text of sections 1, 2 and 2A matches after line-ending normalization; it cannot be byte-for-byte identical to v7r1. Say exactly this, retaining the protected wording and its rights. This is a documentary precision issue, not a loss of rights, and no rewrite of the protected sections is sought.

H14-C03 - State the already-ratified exception in the abbreviated orphan rule (0.1 hard rules, blurb, section 11).

The full live chapter 0.4 and section 4.2 correctly preserve the sole RAT-40 restore exception. The shorter hard rules say all launches are blocked, with no exception, and section 11 says never clear or bypass. Preserve the general prohibition and explicitly cross-reference deployment section 12 for the single owner-approved restore exception, requiring all four conditions and retaining evidence rather than clearing in place. The ordinary job and manual clearance rules remain unchanged. No new restore path, no authority to ignore an orphan marker; the actual implementation remains under separate slice B review.

Observation: 0.1 still points to checking the historical Appendix A hashes against HEAD; 0.7 explains the nine known exceptions. At ordinary refresh make the verification instruction directly distinguish live files from historical records. The phrase in 0.6 about an idempotent workspace edit "when its new text is present" likely means the old text is present (or the new text is absent); clarify if touched. Neither warrants a separate revision or new checker.

## 5. Later events, not defects of v14 at its cutoff

Reviewer takeover accepted entry 287. Slice B owner GO entry 288 (cloud only); EX_322 submitted and EX_323 RECHECK issued; corrections are working increments and await the completed focused submission. No step-3 code installed. The method-priorities discussion and operations manual method appendix deferred/recorded in entry 289; the AI role allocation trial deferred under entry 292. Current roles and authority unchanged.

The owner has also told this reviewer that OUTLANDISH_01 is successfully completed and closed, null under the investigated matching criteria, and will not be integrated. The older backlog statement in H-1 section 9 and section 10 is superseded by that owner direction. Record it with the next ordinary update and in the appropriate roadmap/reminder when the owner directs. The draft doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md is deferred as agreed; no need to read it or discuss the methods now. No catalogue family removed.

## 6. Conclusion and process note

The consolidation reduces the risk of taking an old status as authority. A future normal edition can make the living chapter even more concise and leave technical lessons accessible on demand. The cold read is closed with no recheck needed for H-1 v14. Do not divert the present build work into another handover edition or historical maintenance. Continue slice B through its existing gates. No code, governing document, owner records or data changed by the reviewer. No new EX number used.

Reviewed document identities (exact bytes):
| File | SHA-256 |
|---|---|
| doc/HANDOVER/Claude_Primary_Handover_H1_v14.md | 24cc0579fec0f1b025216d969451457e378d1987eef96bf31f9a3bb924b5a6ac |
| doc/HANDOVER/Claude_Primary_Handover_H1_v14_introductory_blurb.md | ac70661cde58d98f2e1dcb084ddae6d4f676a688ea49dc771f845cff01f75bf8 |
| doc/HANDOVER/Claude_Primary_Handover_H1_v13.md | 37aa0196e828ddf012c83d61c66c49f814892341ffe88d1dc976609da289bbae |
| doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md | 6f968eefebf3cb13212d967ee28fe76b84ed49f319d0df0121e2d746771c97cd |

END OF HANDBACK.
