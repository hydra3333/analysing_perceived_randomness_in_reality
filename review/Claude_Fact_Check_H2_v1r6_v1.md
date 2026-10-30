# Claude factual review of H-2 v1r6 (draft) - v1

Date: 30 October 2026 (Adelaide). Reviewer of this check: Claude (the one factual review a handover receives; H-2 is the ChatGPT reviewer chat's own document).
Subject: `ChatGPT_Reviewer_Handover_H2_v1r6.md` from EX_058 (LF SHA-256 `7821a992a8ad7d61fc23aca8cbeb399d4ab7390cabba2076288580d556872d77`, 24,700 bytes).
Checked against: the live GitHub `main` (fetched by Claude; through `5645a33`, which records EX_058), registers v0.15 and v0.16 as installed, the installed contract data, and exchange/ through EX_058.

## Integrity (all PASS)

- The draft's SHA-256 and size match EX_058; LF only; UTF-8.
- The predecessor is the installed H-2 v1r5 (`67a1b3ea...a094`), and the enclosed diff applies to it.
- **The reviewer-rights region** (from `## 2.` up to the byte before `## 4.`) is 7,676 bytes with SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db` in H-2 v1r5 and in the draft: byte-identical, as stated.
- The draft is 406 bytes shorter than v1r5.

## Facts Claude verified from GitHub (so the draft need not call them owner-reported only)

- E_6 installed at `7c93320c2cce853b94e23203bb47e3f66aaa7994` (parent `6e85b78`, the T005 report): 40 A + 3 M, COMMITTED PASS repeated by Claude, 42 of 42 manifest blobs, 210 tests on Linux.
- E_3/E_4 installed at exactly `5b9edb44d4f4bf01e2d4e8cd7ec9561b32b3110e` (parent `6dc54f9`, the T006 report): 69 A + 1 M, COMMITTED PASS repeated, 69 of 69 manifest blobs, register v0.16 `d84fc3dd...c220`, 242 tests on Linux.
- The reports `REPORT_T005.md` (`6e85b78`) and `REPORT_T006.md` (`6dc54f9`) are on `main`; both RESULT: PASS.
- The owner's Windows results are owner-reported: E_6 SUITE PASS (210) before the commit; E_3/E_4 SUITE PASS (242) straight after the push, a recorded departure (register v0.17 candidate).

## Findings

**H2F6-01 (CORRECTION), line 17 and line 22: the E_3/E_4 commit and the evidence source.**
- "installed at **`5b9edb4` or later**" should be "installed at **`5b9edb4`**": that is the exact commit.
- The evidence boundary should keep the two sources apart. Suggested text for line 22: "The commits `7c93320` and `5b9edb4` and the T005/T006 reports were verified by Claude from GitHub (registers v0.16 and v0.17). The owner's Windows results are owner-reported. This reviewer could not fetch the live tree or EX_057 in this drafting session; check the live tree and the latest installed register when taking over, and do not upgrade reports to first-hand verification."

**H2F6-02 (CORRECTION), line 17: the registry state of the three methods.**
"with `FORMULA_OPEN` entries, development flags and unreleased/`NOT_YET_SPECIFIED` status" merges two different chains. Each declared variant (6 for E_3, 6 for E_4, 3 for E_6, in both games) has its own revision-1 `FORMULA_OPEN` entry, and each method folder has its `IN_DEVELOPMENT.txt`. Separately, each method's `NOT_YET_SPECIFIED` placeholder entry is kept unchanged.

Suggested text: "All three remain **non-runnable**: each declared variant has a revision-1 `FORMULA_OPEN` registry entry, each method folder holds `IN_DEVELOPMENT.txt`, and each method's separate `NOT_YET_SPECIFIED` placeholder entry is kept unchanged."

**H2F6-03 (CORRECTION), section 0 or 6: an owner decision that affects the reviewer's work is missing.** It was given after EX_058 was drafted.

Owner, 30 October 2026: the new-method template (`doc/METHOD_TEMPLATE/`) is reviewed and kept up to date whenever new findings, in Claude's assessment or the reviewer's, suggest an update is warranted. Claude proposes each update in the next package, reviewed like any other document, and each method's handback says whether it found anything for the template.

Suggested sentence for section 6 item 2 or 3: "When reviewing a method, also say whether anything found should change the template (owner, 30 October 2026); template updates are proposed by Claude and reviewed like any other document."

**H2F6-04 (OPTIONAL), section 0 or 6: the owner's order of work** (register v0.17 candidate), for context:
1. this handover round;
2. template draft 2;
3. the E_7-E_16 batch;
4. Method A as E_17 and Method B as E_45, from `doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`;
5. the non-local means discussion.

One line would do, pointing to the register.

**H2F6-05 (OPTIONAL), line 19: the final-package check.** For E_6 and E_3/E_4 too, the final ZIP after ratification was not re-reviewed: it went to `exchange/` for the record (EX_054, EX_057). This was within the reviewer's own dispositions (REG15-052-RD-02, REG16-056-RD-02), which allow only the owner's finalisation and its dependent identities to change.

The draft's sentence is accurate as a caution. Naming this basis would make it complete.

**H2F6-06 (OPTIONAL), line 15:** "Register v0.16 is owner-ratified" could add "and installed at `5b9edb4`".

## Not changed, checked and correct

The E_6 and E_3/E_4 descriptions (exact rational; discounted/power-likelihood updates for the decay variants; shared helper; six variants; score-only, no probability vector); the four switches False and the empty allowlist; CODE-3 planned only; the working lists named as non-authoritative; the cold-start reading list, including H-2 v1r4 sections 7 and 8.2; the EX numbering advice.

## Verdict

Factual PASS subject to H2F6-01..03. The optionals H2F6-04..06 are the reviewer's choice. No change to the rights region is suggested.
