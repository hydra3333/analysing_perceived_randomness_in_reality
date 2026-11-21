# Claude takeover note, 21 November 2026 (supplements the installed handover H-1 v7r1; not a new handover)

**Status:** a working note by the outgoing Claude web chat for the Claude chat that takes over. Not reviewed, not
ratified, authorises nothing. The installed Claude handover is still doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md
(RAT-39). A full H-1 v8 is to be written after the new design is ratified.
**Written:** 21 November 2026, 18:08 Australia/Adelaide. **Why now:** the project is being redesigned from the root; the ChatGPT reviewer
chat was lost on 21 November and replaced; the outgoing Claude chat is long. The owner asked that nothing be lost.

## 1. Read in this order

1. This note. 2. exchange/CONTINUITY_NOW.md (top block). 3. H-1 v7r1 sections 0, 1 and 5 **for the hard rules, the roles, the
exchange protocol and how the owner works: all still binding.** Its design sections (MHUP-B, OV-1 registration, weekly
sessions, Appendix J installs, release records) describe a system that is being replaced: read them as history.
4. exchange/DECISIONS/DECISION_LOG.md entries 121 to the latest (the owner's words). 5. exchange/EX_259, EX_261, EX_262
(the owner's directions), then EX_264 and EX_265 (the findings and decisions EX_266 must answer). 6. The two current
drafts: exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_3.md and DEPLOYMENT_DESIGN_DRAFT_v0_9.md, and
exchange/EX_263_Claude.md (second revision). 7. For the reviewer's side:
doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r10_CONTINUITY_CANDIDATE_20261121.md section 0 (written by Claude on the
owner's instruction; its 0.9 lists where Claude's drafts are weakest).

## 2. Where things stand

- **Nothing of the new system is ratified, coded or installed.** Design work only is authorised. The earlier ratified
  documents stay formally in force until the owner ratifies the new specification. The three MHUP-B slices are not
  installed and will not be installed as built. The old system in the E: clone is as it was at main cc0ab73.
- **The reviewer:** a NEW ChatGPT reviewer chat took over on 21 November 2026 (HO-2; entry 132). The owner said he would
  accept it. It has reviewed nothing of substance yet. Its handover H-2 v3r10 is a candidate; v3r4 is the ratified one.
- **The next deliverable is EX_266_Claude:** a corrected COMPLETE system specification and deployment design. Not
  started. It is new design: say "Suggest switching to Fable (High) for this" and wait for the owner's go (MC-1).
- **EX numbers:** next is EX_266 (Claude). **Decision log:** next entry 133. **Next RAT number:** RAT-40.

## 3. The owner's decisions EX_266 must build in (entries 122 to 131; EX_265)

Families and variants only, no revisions; nothing retired automatically; add-only variants and helpers, **no in-place
helper update** (a wrong helper: a new versioned file and successor variants; Who_Uses, Make_Successors, batch
marking). DEV, QA, PROD by ENVIRONMENT.ini. **QA is NOT mandatory: PROD installs on the DEV marker
I_AM_INSTALLABLE.json alone; nothing in PROD installation refers to QA; QA is to be a capable laboratory.** An
infrastructure marker over deploy/INFRA_MANIFEST.ini. Installs from local DEV files, no Git. One research job; saved
per-draw league reports with TOP and WORST; a prevailing and an exploratory OV-1; draw numbers, never dates; the
environment not pinned; W-23 unchanged. Complete verified backups; exact restore, nothing put back; rollbacks manual.
**Choices:** A the research job runs the updater itself (--no-update to skip); B FORWARD_FROM after a successful
results check; C the owner makes a full ZIP of the E: project folder himself before phase 1 (no cold-copy script: take
the Cold_Copy tool OUT of the deployment design); D withdrawal by one WITHDRAWN_FROM line; E an optional complete
read-only copy of PROD's research data into DEV or QA, replacing the destination's active research data; F yes.
After such a copy, results for variants the destination lacks or holds differently: **warn, ignore, continue.**

## 4. What EX_266 must correct (EX_264, as refined by EX_265)

- **R5-F01:** a forecast pending at the withdrawal draw is never scored: fix specification 5.6, 5.7, 7.1, 9, 10, 11
  together, with a late-result test. (Invariant 4 needs the withdrawn exception stated.)
- **R5-F02:** each marker excluded from its own hash; exact list of hashed files; no __pycache__, .pyc or editor files;
  the same for .venv\ENVIRONMENT_VERIFIED.json; dynamic imports of scientific helpers forbidden or declared.
- **R5-F03:** each NEW variant gets a small synthetic N-1 smoke case per game in the destination, before the barrier is
  removed, writing only to that tree's scratch; an INSUFFICIENT_HISTORY result does not count as the proof.
- **R5-F04:** never promise a rollback to a backup that failed; before an infrastructure overwrite list the verified
  backups truthfully; with none, refuse the overwrite (research jobs still go on).
- **R5-F05:** replace "recompute everything at every infrastructure reinstall" with a proportionate, science-safe rule.
- **New operations to design:** Copy_From_Prod (PROD never written, not one byte; no source-side lock; coherence by
  reading before and after; destination left unchanged or detectably incomplete if interrupted); reset/replay in a
  chosen tree (whole derived results, or a game's draws from J on with optional end N; one confirmation).
- **Notes:** N01 withdrawal boundary and a fresh results check; N02 label QA/DEV OV-1 as sandbox; N03 an exact,
  parser-safe syntax for INFRA_MANIFEST.ini; Q8's conditions on Make_Successors.
- **EX_265 lists the examples and tests it wants.** Deliver full documents with exact diffs from v0.3 and v0.9.

## 5. Design leads the outgoing chat had formed (suggestions only; not decisions, not reviewed)

- Build reset/replay for DEV and QA only at first; leave a PROD reset unbuilt until the owner asks. Reset is the one
  place the append-only lists are cut: state which invariants hold during and after, and make an interrupted reset
  detectable (a barrier file, as for installs).
- For R5-F05: mark the science-critical infrastructure files in the manifest (the N-1 reader, the readout, scoring,
  OV-1, the list code). A reinstall touching none of them: the suite, the smoke cases and a fixed sample. A reinstall
  touching one: say so plainly, require a wider recomputation that the owner chooses (in QA after a copy from PROD,
  or in the target), and never call a sample a proof.
- Copy from PROD: copy to a temporary folder inside the destination tree, verify against hashes taken from PROD
  before and after, then swap; refuse if PROD changed meanwhile.
- The headers of copied lists carry PROD's variant fingerprints: the destination's job ignores, with a warning, any
  list whose variant is not installed there or whose fingerprint differs (the owner's "warn, ignore, continue").

## 6. Things to remember to do

- **Tell the owner when it is time to make his ZIP of the E: project folder:** just before phase 1 moves any source
  file. Advice given to him: include .git and the results and run folders; .venv optional; nothing of the project
  running; open the ZIP once to check; keep it off E:.
- After ratification: write H-1 v8 (carry H-1 v7r1's hard rules; fix its section 12.3 leftover); the ratification also
  covers the orphan-marker exception at a restore (deployment design section 12).
- The owner's rule for the reviewer, which he also applied to Claude on 21 November: discuss his queries first; issue
  or revise an EX only when he asks. He had EX_263 revised twice in place under the same number.
- Record every owner decision in the decision log at once, in his words; keep CONTINUITY_NOW's top block current.

## 7. How the work is done here (so the next chat need not rediscover it)

- Clone with push access (the add_repo tool); fetch and fast-forward before every commit; named paths only; push to
  main. Documents and records only; never src/ or tests/; never source_data/, results/, transitory_data/, GAIS/.
- New document versions are built from the previous one by a small Python builder of counted replacements (each old
  text asserted to occur once), kept beside the document with an exact diff; hashes are computed, never typed.
- EX files: US-ASCII, CRLF, a member table with SHA-256, a P6 "how the process went" note, a paste block for the owner.
  Decision log: append as ASCII bytes, LF. Read the clock in the command that writes (TZ=Australia/Adelaide date).
- The old code, for reading: build the staged slice-3 tree as H-1 v7r1 describes (digest ef2b67e0...1f50e9d13).

## 8. Lessons of this cycle (the outgoing chat's own errors)

1. Twice a mechanism was designed past the owner's intent and he corrected it: a restore that reinstalled later
   releases; QA as a gate between trees. **Ask what a thing is for before designing it; ask one question first.**
2. Twice a summary sentence contradicted the detail under it. Re-read the detail after writing the summary.
3. After every change of rule, search the whole document for the old wording.
4. The owner wants the smallest design that keeps the science right: N-1, the readout, scoring, the kernel and
   recoverability are the main game; administration around them is to be justified or removed.

End of the note.
