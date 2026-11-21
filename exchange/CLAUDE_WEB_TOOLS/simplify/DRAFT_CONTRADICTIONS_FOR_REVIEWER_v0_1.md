# Where the drafts contradict later owner decisions - for the reviewer's double check - v0.1

**Status:** a working document by the Claude web chat, written at the project owner's request of 21 November 2026, 19:11
(decision log entry 134). It is NOT an EX message and NOT a design. It changes no draft and authorises nothing.
**The owner's rule (entry 134):** where a passage of the drafts contradicts a later owner decision, **the later decision
prevails**. This list is so that nothing contradicted survives into EX_266 unnoticed.
**Drafts examined** (line numbers are of these exact bytes):
- `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_3.md`
- `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_9.md`
(Exact hashes are in section 7.)
**Asked of the reviewer:** (1) anything missed or misread, and whether each provenance is right; (2) advice to the owner
and Claude on the open questions of section 5. The owner's process: discuss first; no EX unless he asks for one.

## 1. How the list was made

Both drafts were searched for every term touched by entries 127 to 134 and EX_264/EX_265 (cold copy, copy, flows,
appended, deletes, removal, stale, refusal, regression, backup taken just before, way back, unscored, choice, export,
scratch, sample), and each hit was read in context. A passage is listed when a later decision makes it wrong as written.
Passages that are merely incomplete (a finding asks for something new) are in section 4, not here.

Provenance is given as the decision log entry and, where the decision was relayed by the reviewer, the EX section.
"Owner" means the owner's own words; "reviewer, agreed by the owner" means a reviewer finding the owner accepted.

## 2. System specification DRAFT v0.3

| # | Draft passage (section, line) | Contradicted by | What EX_266 must say |
|---|---|---|---|
| S1 | 0 item 6 (31) "a list that is only ever added to"; 5.1 (137) "Lines are only ever appended" | Reset/replay removes lines (owner; EX_265 s6, s7B; entry 128 item 6). A copy from PROD replaces the destination's lists wholesale (owner; EX_265 s1; entry 128 item 1) | Appending is the rule of every ordinary operation. Reset and reseed are the two named, owner-invoked exceptions, each with one confirmation, and the document states which invariants hold during and after each |
| S2 | 15 (437-439) "No program deletes research data; the only removal of bytes is a torn last line"; 5.7 (190) "the only removal of bytes the system ever makes" | The same two decisions | As S1. The torn-line rule stays for ordinary jobs |
| S3 | 2 (72-73) "Nothing flows ... from PROD to QA or DEV, except the accepted official results" | Complete read-only copy of PROD's research data into DEV or QA (owner; EX_265 s1; entry 128 item 1) | The copy from PROD becomes the one other permitted flow. Unchanged: nothing flows from QA or DEV to PROD (EX_262 s2.4); QA's results are never copied to PROD |
| S4 | 14 (429-430) "PROD's research exist only in PROD and its backups. Nothing is copied back to DEV or to Git by the system (choice E)" | Choice E decided as the copy above (EX_265 s1, s8) | PROD's research may be copied into DEV or QA on the owner's command. Still true and kept: nothing goes to Git; no Git export is required (EX_265 s8; reviewer's observation 2, entry 134) |
| S5 | 12.5 (393) "No result, score or report is ever copied into a new tree" | The copy from PROD (as S3) | Creating a tree still copies no result. A later, separate copy from PROD may |
| S6 | 5.6 invariant 1 (176-178): a list whose fingerprint differs from the installed variant's is "a refusal" in QA and PROD, and in DEV is moved to `_stale` | After a copy from PROD, lists for variants the destination lacks or holds differently: "warn about them, ignore them and continue" (owner, entry 129) | Two different cases. A tree's own list that disagrees with its installed variant is still a refusal (a fault). A list that came from PROD for a variant the tree lacks or holds differently is warned about and ignored, not refused and not moved. See question Q-b for where each lives |
| S7 | 5.7 (187-189) "any FORECAST whose result is on file and has no score line is scored" | R5-F01: a forecast pending at the withdrawal draw is never scored (reviewer, agreed by the owner; EX_264 R5-F01; EX_265 s2; entry 128 item 2) | The withdrawal boundary enters the scoring rule and the next-work rule; the same in 5.6, 7.1, 9, 10.4 and 11. Section 11 (330-331) already says "left unscored"; 5.7 must agree with it |
| S8 | 12.3 item 3 (370-372) "After an infrastructure change: every forecast and every score of every variant"; 12.4 (385-388) "The full regression ... then fails in the target" | No automatic full-history recomputation in PROD (owner; EX_265 s6; entry 128 item 6) | A proportionate, science-safe rule (R5-F05), with an exception path for science-critical changes; never a sample presented as proof |
| S9 | 12.3 (373-374) "The ways out are ... the backup taken just before"; 12.4 (386-387) "the tree goes back to the backup taken just before" | R5-F04: never promise a rollback to a backup that may not exist; rollbacks are manual, from a verified backup the owner chooses (owner; EX_265 s5; entry 128 item 5) | Name the truthful routes for both a successful and a failed pre-change backup. Whether a destructive overwrite is refused when no verified backup exists: OPEN with the owner (section 3, item 4) |
| S10 | 14 (418-419) "If a backup cannot be made, the job goes on ... One exception: a PROD installation stops ... if the recovery kit cannot be written" | If the owner confirms R5-F04's refusal (open), a second exception | Add the exception, or not, as the owner decides |
| S11 | 2 table (66) "Backups: Git, and the cold copy of section 17"; 17.2 (473-483) a "verified cold ZIP", its dry run, "Making it needs its own go", `.venv` left out by default; 17.3 (499) "an unpacked cold copy" | Choice C: the owner himself makes a full ZIP of the whole project folder on E: (ignored run folders and `.git` included) when Claude says it is time; no cold-copy script (owner; entries 130, 131) | Replace with the owner's own ZIP. No tool, no dry run, no go for a tool. Claude tells him when (before phase 1 moves any source file). The rollback is unchanged: unpack that ZIP into a new folder |
| S12 | 19 (539-556) choices A to E listed as open, with Claude's recommendations; "Decided since DRAFT v0.2" lists only entry 127 | A, B, D (entry 130); C (entry 131); E (entry 128 item 1; EX_265 s1, s8); F (entry 127) | Section 19 becomes a table of decided choices with their entries. No owner choice is left open on the drafts, apart from R5-F04 if it is still open then |

Checked and **not** contradicted (listed so the reviewer can disagree): 7.1's results step and `--no-update` match choice A;
10.2 and 10.3 match choice B; 11 matches choice D apart from S7; 4's `Make_Successors` matches EX_264 Q8 in outline
(its three conditions are to be written in, section 4); 0 item 4 and 12.2 match the owner's "marker alone" rule.

## 3. Deployment design DRAFT v0.9

| # | Draft passage (section, line) | Contradicted by | What EX_266 must say |
|---|---|---|---|
| D1 | 1 (44-45) the `[cold_backup]` section of DEV's settings file | Choice C (entries 130, 131) | Removed |
| D2 | 2 (106-107) `Cold_Copy.bat` among DEV's tools | The same | Removed |
| D3 | 13 (294-301) the whole cold-copy section | The same | Replaced by one paragraph: the owner's ZIP, when, and what it is for |
| D4 | 15 (346-347) tests of "the cold copy's dry run and its refusal to leave DEV's root" | The same | Removed |
| D5 | 3.3 item 5 (132) "everything after infrastructure"; 6 step 9 (176-178) the full regression; 14 example 3 (314-318) | No automatic full-history recomputation in PROD (EX_265 s6; entry 128 item 6) | As S8 |
| D6 | 6 (171) "The same eleven steps" applied to infrastructure, including 5 step 5 (161): "if it cannot be made: NO ROLLBACK POINT WAS CREATED, and it goes on"; 6 (178) "the way back is the PRE_INFRA backup" | R5-F04 (EX_265 s5; entry 128 item 5) | For an infrastructure overwrite: list the verified backups truthfully, with what restoring each would lose; refuse with none (if the owner confirms). Variant installs, which only add files, keep "goes on with a warning" (the owner's standing rule; the reviewer applied the refusal to destructive overwrites only) |
| D7 | 0 item 4 (22-23) "or the backup taken just before is restored"; 8 table (192) "restore the backup taken at step 5" | R5-F04 | That backup may not exist: name the route for each case |
| D8 | 16 (359-360) "Withdrawn: ... the `export` mode ... (specification choice E)" | Choice E decided as the copy from PROD | Keep the old `export` (to the clone and Git) withdrawn; add the new copy-from-PROD operation |

## 4. Not contradictions: what EX_266 must add (so the reviewer sees the whole scope)

From EX_264 and EX_265, all agreed by the owner (entry 128):
- **R5-F02:** each marker excluded from its own hash; the exact list of hashed files; no `__pycache__`, `.pyc` or editor
  files; the same for `ENVIRONMENT_VERIFIED.json`; dynamic imports of scientific helpers forbidden or declared.
- **R5-F03:** a small synthetic N-1 smoke case per new variant per game, in the destination, before the barrier goes,
  writing only to that tree's scratch; a declared insufficient-history result does not count as the proof. Neither
  draft names a scratch folder in a QA or PROD tree yet.
- **The copy from PROD** and **the reset/replay** operations (EX_265 s1, s6, s7), with the process rules each needs.
- Notes **N01** (withdrawal boundary and a fresh results check), **N02** (QA and DEV OV-1 labelled as sandbox), **N03**
  (an exact, parser-safe syntax for `deploy/INFRA_MANIFEST.ini`).
- **EX_264 Q8's conditions on `Make_Successors`:** refuse a name collision; rewrite nothing existing; copy no marker.
  And the reviewer's observation 3 (entry 134): it never withdraws anything.
- The tests EX_265 s8 lists.

## 5. Records (not drafts) that lag a decision

| # | Record | What it says | Status |
|---|---|---|---|
| R1 | `exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21.md` section 2 | "Decision log: next entry 133" | 133 was the note's own entry. Noted in entry 134; the note is a dated record and is not edited |
| R2 | `exchange/CONTINUITY_NOW.md`, lower sections | Reviewer status, "If a chat ends", MHUP-B resumption, the full order: as at 18-19 November | Brought up to date with entry 134 (commit `c45e583`) |
| R3 | H-2 v3r10 section 0.8 | Choices A to D "NOT formally chosen as at EX_265" | True when written; decided in entries 130 and 131. The reviewer's file: not edited by Claude. The reviewer noticed it itself (entry 132) |
| R4 | Decision log entry 128 item 5 | Records "with none, the overwrite is refused" as owner-agreed | In EX_265 s5 the sentence is the reviewer's recommendation. OPEN with the owner. The reviewer's view: entry 128 stands unless the owner corrects it |
| R5 | H-1 v7r1, design sections (MHUP-B, OV-1 registration, weekly sessions, Appendix J), section 5.3 (revisions and release rule) and section 11 ("open now: the cloud code round") | The old system | By design until H-1 v8, after ratification (entries 133, 134). Section 11's "open now" is overtaken by entry 122 ("No source-code implementation ... is authorised") |

## 6. Questions on which Claude asks the reviewer's advice (no decision exists yet)

- **Q-a.** Anything above missed, misread or wrongly sourced?
- **Q-b. Where do copied lists live?** After a copy, QA may hold a variant of the same name as PROD's but with other
  bytes. Its own lists and PROD's copied lists would go to the same path (specification 5.1). "Ignore" needs one of them
  to be elsewhere, or a header check that keeps them apart. Which is simpler and safe?
- **Q-c. A reset in QA or DEV and the prevailing OV-1.** A reset from draw J can remove `FORWARD_FROM` lines and the
  prevailing ledger's lines from J on, which changes who counts in the replayed score. With N02 (sandbox labels), is it
  enough that a QA or DEV prevailing score is labelled sandbox and never claims the 2.5% bound, or is something more
  needed?
- **Q-d. `FORWARD_FROM` in QA and DEV.** It is defined by a successful check of the official source (choice B), which
  never happens in QA or DEV (they receive results by copy). Should a successful checked copy from PROD count there, as
  a sandbox start?
- **Q-e. Scope of the copy.** EX_265 s1 also allows an owner-selected export folder and an optional passive export; the
  takeover note narrowed it to DEV or QA. Include the export folder, or leave it out unless the owner asks?
- **Q-f. The GitHub source ZIP.** EX_259 s3 planned an owner-downloaded GitHub source ZIP. Entry 131 says the owner will
  "instead do a full ZIP of the project folder tree on E:". Claude reads the GitHub ZIP as no longer planned. That is the
  owner's to confirm; the reviewer may comment.

## 7. Exact identities

| File | SHA-256 (Git blob content at main `c45e583`) |
|---|---|
| `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_3.md` | `bbf727696e196a2cd39a52c947f8106adc8934f36faa355b859f91d63d40f1d1` |
| `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_9.md` | `3665f7be2ab6e5165ab5be1ef32d042bce26ef8e1812a19f39360f59c9ce471f` |

End of document v0.1.
