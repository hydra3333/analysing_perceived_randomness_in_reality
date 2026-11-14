## The owner's decisions of 13 November 2026, the Mode H readiness reviews, and the handover round of 14 November 2026 (register v0.29)

Paths in this section are from the repository root. In this section, "this register" means register v0.29. Every commit named
here was checked by Claude from GitHub. This section records decisions already taken and events that happened; it makes no
new decision, and nothing in it authorises a check, an approval or a run.

**The owner's decisions of 13 November 2026, 22:08** (record, verbatim:
`exchange/DECISIONS/OWNER_DECISIONS_2026_11_13b_MODEH_FIRST_Q7.md`, committed at `fd80e3e`), after Claude's MHUP-B assessment:
1. **Route 2, in principle: Mode H first, then MHUP-B.** Not yet authorisation for Approval 1. **The fixed cohort:** the 40
   variants per game released at that date form the Mode H study's fixed cohort; methods developed later cannot claim a fresh
   evaluation on the same holdout draws. **CATCH_UP** is retrospective evidence and cannot replace missed genuine prospective
   predictions. **The freeze:** no MHUP-B install and no change to the frozen code or environment between the first Approval 1
   and the sealing of both games. This settles design 4.4 item 1's choice for MHUP-B: after both games are sealed.
2. **Q7 DECIDED:** "Retain the restriction on raw draw values in the AI chats after Mode H. Approved project programs may still
   read and score those values through their controlled interfaces. Appropriate aggregate reports remain shareable." No rule
   changes and no new restriction.
3. **R-015 (b):** the Windows POC rerun is preferred: the existing non-destructive synthetic POC suite and the direct launcher
   and byte-code checks, excluding the optional `--with-timeout` process-tree termination test unless separately reviewed and
   authorised. No execution authorised.
4. **R-015 (c):** the owner will confirm the backups of `source_data/` and `results/` before Approval 1 (on the readiness sheet);
   that confirmation is **PENDING**, and no backup check and no Mode H Approval 1 has been authorised. No restore test was run
   or is required.
5. **The Approval 1 readiness sheet**, reviewed independently by the reviewer before the owner authorises anything; neither
   holdout run or opened.
6. **MHUP-B:** detailed design and code only on the owner's separate authorisation; isolated design work acceptable in
   principle, never interfering with the frozen Mode H implementation; the post-step-18 suite run kept in its design; KISS-1
   stays deferred; a proportionate process, prioritising scientific correctness, functional reliability and the agreed safety
   protections.

On 14 November 2026 the owner also asked that Claude's handovers be produced this round as **full updated documents rather than
more addenda or deltas** (the reviewer prepares its own).

**The Mode H readiness work (13-14 November 2026).** Claude (on Fable) read the installed Mode H code against design v0.1r7,
ran a full-cohort dress rehearsal of the four steps on invented data with the installed code (PASS for both games: 40 variants,
400 of 400 forecasts, one score, sealed; a second plan and a second score refused; no drawn number in any report file), and
drafted the readiness sheet and the POC rerun instructions (`exchange/CLAUDE_WEB_TOOLS/modeh_readiness/`, `52821e3`).
- **EX_167** (the reviewer): PASS WITH CORRECTIONS. **B01:** a blank-page browser start does not show that the installed updater
  can fetch and parse the official page; before either Approval 1, a narrowly scoped, separately owner-authorised, read-only
  historical fetch-and-parse check with the installed fetcher and parser, or the owner's written acceptance of the risk of a
  permanently blocked first game. **B02:** the first update is not indivisible (grab, backup, master, ledger); every unexpected
  Approval 2 result is held until a case-specific reviewed recovery. C01-C05: counts on all-success only; the Git boundary
  during the freeze; the witness push's meaning; the three families' separate error rates and catch-up against development
  evidence; Q7's records and the reports' sharing.
- **r2** (`bbaa2e3`): all applied; the one-off read-only check `gov_fetch_parse_smoke.py` (Git blob
  `1cbd32941234661d422c32f53bbf3b5343af2ff7`; the installed `BrowserFetcher.fetch` and `parse_gov` unchanged, 31 May to 31 July
  2026, the quarantine closed, nine draws per game compared in memory with the master, nothing written, draw numbers and counts
  only) and its development test (13 of 13 cases on invented data with a stand-in browser; no website contacted); the POC
  instructions r3.
- **EX_168** (the reviewer): **PASS**, zero blocking findings; B01 and B02 closed at the instructions level; the master
  comparison kept; the earlier two-site checker's fetches of the same page are context, not a substitute; a Powerball-only rerun
  of the check is acceptable after Oz Lotto is sealed and before Powerball's Approval 1, on its own go; N01-N03 (wording of
  "writes nothing", a second identity check of the file on disk, `-B` and caches) applied as **r2a** (`496731c`) without a
  further recheck.
- **Open for the owner:** decisions D1 to D7 of the sheet's section 9 (Oz Lotto first; both games decided now; the witness push;
  the official-page check or the written risk acceptance; the updated masters left uncommitted until both seals; the reports
  shared after both seals; the order of his gos). Nothing was authorised or run; no AI chat contacted any lottery website.

**The reviewer's handover: H-2 v1r11, then the full H-2 v2 (14 November 2026).** At the owner's request the reviewer wrote
its own continuity refresh: a delta on H-2 v1r9 and v1r10, a continuity index and a blurb (EX_169), leaving H-2 v1r9's rights
region untouched (7,676 LF bytes, SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db`, checked by
Claude). Claude's factual check (recorded with EX_169 at `959b072`): PASS WITH CORRECTIONS, five corrections and two optional
points. **EX_170** (r1) applied exactly those nine lines (Claude's diff check: PASS; recorded at `ac2c063`). The owner then
asked for one full document instead of layers, and the reviewer wrote **H-2 v2** (EX_172): one file and its blurb, sections 1
to 5 byte-identical to the ratified H-2 v1r8 and v1r9 (the rights region unchanged), the rest consolidating H-2 v1r9, its
v1r10 delta and the v1r11 r1 content. Claude's factual check is EX_173. H-2 v1r11 r1 is never installed; H-2 v2 awaits the
owner's ratification and installation. This register does not ratify it.

**The Claude handover H-1 v2 (14 November 2026).** At the owner's instruction, a full consolidated edition replacing H-1 v1r8
and all its deltas (v1r9, v1r10, v1r10r1, v1r10r2, v1r10r3), built from v1r8's ratified bytes by counted edits and section
replacements (`exchange/CLAUDE_WEB_TOOLS/h1v2/make_h1_v2.py`), with a section-by-section account of where every part of the
v1r10r3 delta went (its Appendix B), and a new introductory blurb. It changes no rule. Sent with this register as EX_171.
**EX_172** (the reviewer's documentary review): PASS WITH CORRECTIONS; both files rebuilt byte for byte from v1r8 and v0.28;
no binding loss; C01 (point to the full H-2 v2, not to layers), C02 (R-015 (c) still pending) and C03 (no inference from
absence), each a FIX AND PROCEED, applied in EX_173. CANDIDATE until the owner ratifies and installs it.

**Future actions (updating register v0.27's list; not authorisations).**
1. The owner's decisions D1 to D7; then the preparatory checks, each with its own go: the Windows POC rerun (R-015 (b)), the
   updater's offline self-test, the read-only official-page check, the backup confirmation (R-015 (c)) and the tree checks;
   then Approvals 1 to 4 per game, each separately, with the freeze from the first Approval 1 until both games are sealed.
2. One owner-run documentation install of five files (H-1 v2 and its blurb, H-2 v2 and its blurb, this register), after the
   owner's ratification of the final files and before the first Approval 1, so that no `doc/` change is pending during the
   freeze.
3. After both seals: this register's next edition records the study; the holdout exposure record's next edition (Q7, the
   opening records); the full H-1 and H-2 editions refreshed; then MHUP-B (its design on the owner's authorisation),
   carrying A7's interrupted-update recovery, the corrective scoring run (A1 section 6), R-019 (b) and (c), R-018 (a), (d) and
   (h), the tests-only fix for the tests pinned to the version-1 masters and the J-1 step 10 wording they make inaccurate, a
   whole-suite run after the release step in its isolated rehearsals, and T017.
4. Q7 into the design's next edition (section 9 and the Q7 rows), H-2's next full edition and the holdout exposure record.
5. Unchanged from register v0.27: WF-1C; the method waves; KISS-1 when the owner asks; the next editions of R3, E2R-1,
   Architecture (v0.10, with MHUP-B) and the proposal.

**Out-of-date statements (register v0.29).** This register prevails, and the files are not edited:
- **Register v0.27, future action 2** ("Q7 before Approval 2; the owner's backup confirmation and POC-suite choice at MHUP-A's
  approval"): Q7 is decided; the backup confirmation and the POC rerun are preparatory checks before Approval 1.
- **Design v0.1r7, section 9's Q7 rows and the "OPEN, for the owner" paragraph; Appendix K's row "unchanged until Q7 is
  decided":** Q7 is decided (above); the rules named there stay as they are.
- **Design v0.1r7, section 4.4 item 1 and the plan table in section 8** ("MHUP-B is installed before Approval 1 ... or after the
  Mode H score is sealed"; "installed before Approval 1"): the owner chose after both games are sealed; the dates in the plan
  table have passed (FB-1).
- **H-1 v1r8 and the H-1 v1r10r3 delta:** replaced by H-1 v2 once it is ratified and installed; until then they are in force.
- **H-2 v1r9 and its v1r10 delta, their status statements** ("nothing installed", R-020 (g) open): superseded by H-2 v2 once
  it is installed. **H-2 v1r11 r1** (EX_169, EX_170): superseded by H-2 v2 before installation; never installed.
- **The readiness drafts r1 and r2:** superseded by r2a.

| Document (path) | Author / check | Status and Git-content SHA-256 |
|---|---|---|
| `doc/RATIFICATION_REGISTER_v0_28.md` | Claude, from the records | OWNER-APPROVED 13 Nov 2026; installed at `cce4858`; superseded by this register; `79ff491ffebae33715f1d434104324ff8301e6adf78177080c784e5f18a38e62` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v2.md` | Claude, from H-1 v1r8 and the records | CANDIDATE 14 Nov 2026, for the reviewer's documentary check and the owner's ratification; `@H1V2@` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v2_introductory_blurb.md` | Claude | CANDIDATE 14 Nov 2026; `@H1V2B@` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md` | the reviewer (EX_172); Claude's factual check (EX_173) | CANDIDATE 14 Nov 2026, for the owner's ratification; `@H2V2@` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2_introductory_blurb.md` | the reviewer (EX_172) | CANDIDATE 14 Nov 2026; `@H2V2B@` |
| `exchange/DECISIONS/OWNER_DECISIONS_2026_11_13b_MODEH_FIRST_Q7.md` | the owner's words, recorded by Claude | OWNER DECISION 13 Nov 2026; as stored `68d919a7272276a20ae527ba929453e5397c81d9fee389ff54b4f0b05a3aac31` |
| `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/APPROVAL_1_READINESS_SHEET_DRAFT.md` (r2a) | Claude; the reviewer (EX_167, EX_168 PASS) | REVIEWED DRAFT; authorises nothing; as stored `7f85d98fc948499b0841e5de9546bb801d649c01dd87528d3176738eca71b583` |
| `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/OWNER_POC_RERUN_R015b_DRAFT.md` (r3) | Claude; the reviewer (EX_168 PASS) | REVIEWED DRAFT; not run; as stored `c0f1c59f38290dc53773efa534f95df1c8df285aa9520797d98a9ea3af99959a` |
| `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/gov_fetch_parse_smoke.py` | Claude; the reviewer (EX_168 PASS) | REVIEWED; not run; Git blob `1cbd32941234661d422c32f53bbf3b5343af2ff7`, SHA-256 `f3d9785a278419fe978815991b17c6c0bdaa9784cd68833adb22da48b1f0af2a` |

