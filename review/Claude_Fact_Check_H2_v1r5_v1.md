# Claude's factual review of H-2 v1r5 (draft) - v1

**Document reviewed:** `ChatGPT_Reviewer_Handover_H2_v1r5.md` (draft, EX_047_ChatGPT; LF SHA-256 `0e46443481f12e4f12ff14862502b0ec26b87a98fcc8cd20b200410ba9c356d0`; 23,804 bytes).
**Predecessor:** H-2 v1r4, installed (`73b90ea348aea5fc337097a14ec4a8669258bc6cba55ce5a2485de26575f3f3a`).
**Reviewer of record:** Claude, the other model, giving the one factual review a handover gets. Date: 29 October 2026.
**Scope:** facts, current status and safety boundaries, plus anything binding lost in the shortening. Wording and structure are the author's.

## Checked and correct

- **The reviewer-rights region is unchanged.** The region from `## 2. Reviewer rights:` up to `## 4.` is byte-identical to H-2 v1r4: 7,676 bytes, SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db` (computed by Claude). That covers R-1..R-11, the T-05 note and section 3.1. The draft has no CR bytes, and every non-ASCII byte is inside that region.
- **The CODE-2 status** (section 0) agrees with the register v0.14 candidate and Claude's GitHub check of `ced9b6c`:
  - the owner's Windows run order: 190 tests before the commit, 3 symlink skips, then COMMITTED PASS;
  - T004 (report `bce33b1`);
  - the four switches False and the allowlist empty;
  - the coordinator-side refusal, STANDALONE-only publication, the variant-exact gate re-reading the registry, and the roster as a roll-up;
  - `read_run` establishing its own gates;
  - E_1 at revision 1, with its legacy entry point gated.
- **Section 4** keeps the eight always-review subjects word for word in substance, and the RECHECK default. Its new item 4 (release and consumption trust boundaries) is accurate to E2R-R57 and E2RC2-CODE-B01/B02.
- **Section 5** keeps the hard prohibitions: no results searches; the 1577 and 1694 boundaries; the forecast-only 1577 regression; GAIS never revived; the orphan marker as a global stop that no AI clears; no-status/no-kill; the failed-group firewall; owner-only commits and pushes; no personal names.
- **The evidence caution** (section 0) and the reading rule are right: owner-reported and Claude-verified facts are not first-hand reviewer facts.

## Findings

**H2F5-01 (CORRECTION) - the dropped lessons do not live in the register.** Section 7 says the "long historical lesson list" is not restated because its "authoritative locations are the installed register and versioned `review/` evidence". The 17 lessons are in H-2 v1r4 section 7 only; the register does not hold them. The same goes for the source and review anchors table (v1r4 section 8.2).
- **Suggested fix:** in section 7, say: "The lessons of the independent review record (H-2 v1r4 section 7) and its source anchors (v1r4 section 8.2) are kept in H-2 v1r4, which stays in the repository; a new reviewer reads them at cold start." Add that to section 6 item 2.

**H2F5-02 (CORRECTION) - what the final-ZIP waiver covered.** Section 0, last bullet, says the owner waived a pre-installation check of "*final* CODE-2 ZIP-only status/hash changes". The final ZIP also corrected one install-instruction sentence ("up to 3" symlink skips instead of "the two symlink tests"), disclosed in EX_046. The owner's waiver (register v0.13) covered the final ZIP as a whole.
- **Suggested fix:** "the owner waived a reviewer check of the final CODE-2 ZIP before installation (register v0.13). It differed from the checked candidate only in status and hash lines and one disclosed install-instruction sentence (EX_046)."

**H2F5-03 (CORRECTION) - commit rights, stated exactly.** Section 5, "Repository and privacy", says the owner controls all project-tree commits "except the expressly authorised Claude commits confined to `exchange/` and the separately scoped Claude Code working-folder/report procedure". The owner authorised **Claude** to commit in and under `CLAUDE_CODE_WORKING_FOLDER_TREE/`, as well as `exchange/` (register v0.12). There Claude commits task files and runner tools. **Claude Code** commits only its own report file, through `commit-report`. Only the owner pushes Claude Code's reports.
- **Suggested fix:** "...except Claude's owner-authorised commits inside `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` (register v0.12), and Claude Code's single report-file commits there, which the owner pushes."

**H2F5-04 (OPTIONAL) - the Method Ranking proposal is history.** Section 6 item 2 lists "Method Ranking v0.5" among the operative contracts. After the integration (register v0.5), R3 v0.5 section 17 governs ranking measures, and MR v0.5 is integrated history, kept unchanged. H-2 v1r4 had the same line.
- **Suggested fix:** "R3 v0.5 section 17 (ranking measures; MR v0.5 is integrated history)". Optionally also add the E2R code scope v0.1 (`Predictive_Randomness_E2R_Code_Scope_v0_1.md`), which sets the CODE-1/2/3 boundary.

**H2F5-05 (OPTIONAL) - name E1-ALIGN's install commit.** Section 0 says "E1-ALIGN installed, with follow-up document corrections ending at `1b23fd9`". The install commit is `295118d`; `c1159c7` (the register) and `1b23fd9` (its manifest) followed.
- **Suggested fix:** "E1-ALIGN installed at `295118d` (follow-up corrections `c1159c7`, `1b23fd9`)".

**H2F5-06 (OPTIONAL) - two standing process rules a reviewer meets.** Section 0 mentions the combined round only for this round. Two standing rules affect what the reviewer receives:
- **Document-only installs** (owner, 28 October 2026; register v0.10): files only under `doc/` and `review/`. There is no verifier and no reviewer check of the install zip, only Claude's check from GitHub after the push. Content review is unchanged.
- **Combined rounds** (owner, 29 October 2026; register v0.14 candidate): register text comes to the reviewer only together with a code package or the handovers, never in a round of its own.

**Suggested fix:** one bullet in section 0 stating both.

**H2F5-07 (OPTIONAL) - EX numbering race.** This draft's message is `EX_047_ChatGPT`. Claude's `EX_047_Claude` (H-1 v1r4 and register v0.14) was pushed at 20:29 Adelaide time, and this zip was made at 20:30, so neither chat could have seen the other. Both are recorded under their own names (`1c8668e`, `6ba6284`); nothing was overwritten, and numbering continues at EX_048.
- **Suggested fix:** in section 6 item 4, "check the highest `EX_NNN` on `main` immediately before numbering; if a clash is found when recording, Claude records both under their own names and the next message takes the next free number".

## Disposition

- **No BLOCKER.** The rights region and the safety boundaries are intact.
- **The CORRECTIONs:** H2F5-01 to 03 are factual corrections for the author to make in H-2 v1r5 r1, under its own control.
- **The OPTIONALs:** H2F5-04 to 07 are the author's choice.

Claude does not need to see H-2 again before the owner's ratification if the author adopts H2F5-01 to 03 as worded, or with equivalent wording that keeps the facts. The register v0.14 then records the final hash.
