# Reminders for the owner

Kept by the Claude web chat. This is not an EX message and is not reviewed; ChatGPT does not need it.
Claude raises each OPEN item when its "when" arrives, or whenever the owner asks. An item is marked
DONE (with the date and where it was settled) or DROPPED (with the reason); items are never deleted.
Dates are Adelaide dates. US-ASCII, CRLF.

## R-001  The owner's two further methods, and the add-a-method process

- Asked: 29 October 2026 ("I have 2 more I'd like considered later"; discuss the process for adding
  new methods).
- Status: OPEN.
- What: the owner's two further method ideas, confirmed by the owner on 30 October 2026 as
  Methods A and B in doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md, which
  supersedes the pre-exploratory GASI_thought_experiments_possibly_unexplored_areas.md:
  A, recurrence-gap spectrum (does a number that has just been drawn repel or cluster?);
  B, delay-embedding analogues (predict from what followed the past draws that looked most like
  the recent ones; also look for up/down patterns that never occur).
- R2 already lists close relatives: A is near E_17 (Discrete Recurrence Hazard Curves, also E_19);
  B is near E_45 (Delay-Embedded Nearest-Analogue Forecast, also E_27 and E_32). A and B are to
  become those methods' specifications rather than new E-numbers.
- Progress: the add-a-method process exists (the new-method template, used for E_6 and E_3/E_4).
- When (owner's revised order, 30 October 2026): A in wave 2 (with E_2, E_19, E_18), right after the
  first light counting methods; B in wave 3 (with E_27), after releases and WF-1.

## R-002  Pattern-spotting by non-local means (the NLMEANS idea)

- Asked: 30 October 2026.
- Status: OPEN (postponed by the owner, 30 October 2026).
- What: discuss, even if only to record why it is set aside, whether non-local means (NL-means, an
  image denoising method that averages each pixel with others anywhere in the image whose
  surrounding patches look alike) or a similar "non-local" technique could say anything about the
  draws. Ideas to discuss:
  - viewing the draw history in different ways: as a series of images over time, as one large image
    (draws by numbers, for example), or other imaginative arrangements;
  - applying NL-means or similar to those views, and seeing whether any structure (edges, repeated
    patches, anything) emerges that fair draws would not produce;
  - whether any such structure could be turned into a testable way of ranking numbers for the next
    draw;
  - whether it suggests some other oddball method that is easy to code.
  The owner's own view: probably not feasible, but worth discussing and recording either way.
- When (owner's revised order, 30 October 2026): straight after wave 3 (Method B), or whenever the
  owner asks. Any method it yields joins a later wave.

## R-003  Optional tidy-up of old EX copies in review/

- Asked: offered by Claude on 29 October 2026 (after the DOC-6 install).
- Status: OPEN (optional; nothing depends on it).
- What: review/ holds 10 older EX copies (EX_026 twice, EX_027 to EX_034), all identical to the
  copies in exchange/ (apart from line endings in the .md files). The owner may remove them with
  one git rm commit; Claude would give the exact commands and check the result.
- When: whenever convenient.

## R-004  The NIST Randomness Beacon root for the first stochastic method

- Asked: 30 October 2026 ("we had talked about a NIST seed ... when do we do that?").
- Status: DONE (31 October 2026; the seed record ships in WF1B_Install_v2, EX_110). Later stochastic
  methods (Method A's diagnostics, Method B's checks, wave 9) get their own seed policies the same way.
- What: decisions D-9 to D-11 (owner, 28 October 2026; in the register) say a seed policy's root is one
  pre-announced NIST Randomness Beacon pulse, fetched once by the owner by hand and checked
  independently; runs never fetch it. Roots may be switched as a new revision or variant, and every root
  tried is logged and counted. For development runs on past draws, a pulse published afterwards may be
  used, labelled as experiment randomisation; a real forecast needs a root approved beforehand.
- Not needed yet: E_1, E_6, E_3 and E_4 are deterministic and use no random numbers.
- Steps when due: the method's design note includes its seed policy; the owner picks a future pulse
  time, recorded before it arrives; after it is published, the owner fetches it in a browser and gives
  it to Claude; Claude checks it, and it goes into the register.
- Progress (30 October 2026): the releases and WF-1 design note v0.1 (EX_077, section 8.1) announces
  the pulse: NIST Beacon 2.0, chain 2, timeStamp 2026-11-06T00:00:00.000Z (10:30 am Adelaide, Friday
  6 November), field outputValue. The owner may pick another later minute before that one arrives
  (decision WF1-9). After that time: open
  https://beacon.nist.gov/beacon/2.0/pulse/time/1793923200000 in the browser, save the JSON to
  E:\TEMP and attach it to the Claude chat.
- When: at WF-1's design (owner decision W2-8, 30 October 2026). Wave 2 uses no random numbers; R3's
  N1 fair-draw simulator, used at WF-1, is the first part that does. Method A's later diagnostics,
  Method B's simulated checks and wave 9's machine learning also use random numbers.
- Progress (31 October 2026): the owner brought the pulse forward to 2026-10-31T10:30:00.000Z
  (EX_103, 92a6cef, announced before the pulse); the 6 November policy stays on record as
  REPLACED_BEFORE_PULSE, never fetched. After the pulse the owner saved it from the browser; Claude
  read it independently; both agreed. The owner APPROVED policy N1_ROOT_NIST_C2_20261031T1030Z_V1
  (pulse 2007128) on 31 October 2026; ChatGPT compared the saved file with the record (EX_111).

## R-005  E_1 revision 2 (real-capable), with CODE-3 first

- Asked: 31 October 2026 (owner decision WF1-13, option C, while WF-1A was being coded).
- History: design v0.1 sent for review in EX_086 (31 October 2026). Owner choices before review:
  ER-1 to ER-4 as recommended (one package; install and release together in two separate steps; r1
  archived complete; the adapter docstring corrected); ER-6 (an E_1-only batch plan) declined.
  EX_087: RECHECK (B01: the install's interim was not fail-closed; C01, C02, O01). v0.1r1 sent in
  EX_088; the owner chose ER-2r1 (one package, five steps behind a temporary E_1 flag).
  EX_089: B01, C01, C02 resolved; new C03 (exact refusal codes in the barrier test). v0.1r2 sent in
  EX_090 for a focused RECHECK.
  EX_091: PASS (O03 optional: T09's step-0 planning wording, applied in the code's test).
  OWNER-RATIFIED 31 October 2026: design v0.1r2 (LF fb3b26da...209a) as reviewed. Coding started the
  same day, in parallel with the REL-1 and WF-1A installs; it installs after WF-1A.
  Code candidate E1R2_Install_v1 sent for R-2 review in EX_092 (31 October 2026): 348 tests on both
  Pythons, 16/16 mutations, rehearsals PASS. Register v0.22 follows after the REL-1 and WF-1A installs.
  EX_093: RECHECK (B01: the archive check missed paths built with Path(...); importability overstated;
  O01 optional). E1R2_Install_v2 sent in EX_094 (350 tests, 19/19 mutations, rehearsals PASS).
  REL-1 installed at 6a1bed9 and WF-1A at 0d98706 (31 October 2026). The owner runs no batch until
  E_1 revision 2 is installed.
  EX_095: RECHECK PASS (O02 optional). The owner accepted the package and chose to apply O02 first:
  E1R2_Install_v3 (base 0d98706) sent in EX_096 for a focused check; TASK_T011 rehearses it. Register
  v0.22 follows the install as a document-only update (owner, 31 October 2026).
  EX_097: PASS. INSTALLED by the owner at 86d12ea (31 October 2026); Claude verified it from GitHub.
- Status: DONE (31 October 2026). Register v0.22 was installed at 2b1e7e3 (31 October 2026).
- What: E_1 revision 1's multi-game function refuses real data (kept unchanged on purpose when E_1 was
  wired into the contract), so E_1 cannot run in WF-1's walk-forward batches. The owner chose a new
  revision, E_1 r2, which accepts real development runs, with E_1's legacy runner moved to r2 too.
  Needs: CODE-3 (retirement tooling: r1 moves to archive/methods/E_001/r1/, decision D-5) first; a short
  E_1 r2 design note; the r2 declaration and registry entries (installed unreleased, then released); the
  legacy runner's release check (D2-3) and E_1's goldens reviewed for r2.
- Interim: WF-1A names E_1 in each batch plan as not in the cohort, with the reason; families have 78
  tracks until E_1 r2 joins. Then a new batch over the full cohort (40 variants, about 105 minutes
  for Powerball) gives one complete batch per game to score.
- When: after the REL-1 and WF-1A packages, before or alongside WF-1B, so E_1 can be in the first report.

## R-006  Deferred performance study (the very last stage)

- Asked: 31 October 2026 (the owner scheduled it; "need not read nor consider it now, only schedule it").
- Status: SCHEDULED, NOT ACTIVE. Nothing to do until the owner activates it.
- What: the owner's proposal doc/Deferred_Performance_Engineering_Proposal_v0_1.md (v0.1, committed
  by the owner at 1050338): a profiling-first study of where the time goes, then a decision on any
  speed-up, under the project's usual review and owner gates.
- When: at the very end of the project, after all implementation and clean-up (roadmap item 22).
- Record: the next register edition lists the proposal as owner-committed and unreviewed, with this
  stage as scheduled only; no review is asked for now.
- Added by the owner (31 October 2026, during the first Powerball batch): the walk-forward batch runs
  one method run at a time in one process, so it keeps about one logical processor busy (the owner saw
  about 4% total use on a 24-thread machine; this was never profiled, EX_099 C01) and takes hours. Study running variants in parallel to use more cores, keeping what the
  one-at-a-time order gives today: a reproducible batch, and a clean stop at the first problem.
- Brought forward by the owner (31 October 2026, WORKERS-1): parallel walk-forward batches, and the
  coordinator's worker limit raised from 6 to the machine's logical processor count (default half),
  now ship with WF-1B (roadmap item 10). The rest of this study stays FINAL and inactive.
- Changed by the owner (31 October 2026, decision WB-0): the workers change moved out of WF-1B into its
  own package, WF-1C (roadmap item 10d), designed after WF-1B with EX_101's and EX_105's obligations.
- Brought forward by the owner (1 November 2026, PERF-1): one measured hot spot in the ranking report's
  statistics (the exact Monte Carlo uncertainty interval), fixed with bit-identical results. Profiling on
  invented data found the rest of the stage is now the N1 simulation (about 80 s) and the family-maximum loop
  (about 30 s); both are left for this study. The rest of the study stays FINAL and inactive.

## R-007  EX_111 O01: cross-check the seed record's reader names

- Asked: 1 November 2026 (the owner deferred EX_111's optional O01 to a later package).
- Status: OPEN (optional; not a gate). To be folded into MHUP-A (register v0.24, future action 1).
- What: src/evaluation/seed_policies.py checks that the two source reads have different readers and
  that the fetcher differs from the verifier, but not that sources[0].read_by equals fetched_by and
  sources[1].read_by equals verified_by. The approved record already matches both. Remedy: add the two
  equalities and one invented-data negative test.
- When: in the next package that touches src/evaluation (WF-1C, or the Mode H package).

## R-008  The install verifier's wording when an expected file is missing

- Asked: noted by Claude on 1 November 2026, during the WF-1B rehearsals.
- Status: OPEN (wording only; the check itself is correct and stops). To be folded into MHUP-A's verifier
  (register v0.24, future action 1); DOC-11's verifier still has the old wording.
- What: when an expected new file is missing, the verifier's STOP message speaks of "unexpected new
  paths", which points the reader the wrong way. Reword it to name the missing paths.
- When: in the next install package's verifier.

## R-009  The new-method template, draft 4, at wave 3

- Asked: noted by Claude on 1 November 2026.
- Status: DONE (1 November 2026; installed with DOC-10 at 7bb0bfd). Brought forward from wave 3 into the snapshot.
- What: bring doc/METHOD_TEMPLATE/ up to date with what releases, WF-1A, E_1 revision 2 and WF-1B
  taught (released methods, walk-forward batches, scoring), as draft 4, in the wave 3 package.
- When: wave 3 (roadmap item 11).

## R-010  EX_113 O02: the test runner's failure-detail label

- Asked: 1 November 2026 (the owner accepted WF1B_Install_v3 and deferred EX_113's optional O02).
- Status: OPEN (optional; wording only). Comes with MHUP-A's runner (register v0.24, future action 1).
- What: when a test module fails, WF1B_Install_v3's runner heads the printed details "invented test data
  only". Some older tests read the development masters, so the label should not promise that. Claude has
  already changed the runner template to "test failure output; inspect before sharing". Until then, a
  failure log is checked before it is relayed, so no restricted outcome is forwarded.
- When: the next install package's runner (it comes from the template automatically).

## R-011  Record files under results/ must never be line-ending converted

- Asked: noted by Claude on 1 November 2026 (the Powerball report refused: its batch plan file on the owner's PC
  no longer matched its committed bytes; most likely Git rewrote it with Windows line endings).
- Status: DONE (1 November 2026; the rule installed with DOC-10 at 7bb0bfd, whose install also found and restored
  results/audit/SEARCH_LOG.csv, which had mixed line endings on the owner's PC). The cause was confirmed on 1 November 2026: both
  committed Powerball batch records were w/crlf; the owner restored them. The install's step 0 checks every
  results file (git ls-files --eol results) first.
- What: a .gitattributes rule (for example `results/** -text`, as `source_data/**` already has), in an
  owner-ratified package, so Git never converts record files; plus a check of the other committed records.
- When: the snapshot package.

## R-012  The two cold-read probes' findings (results updater; performance plan)

- Asked: the owner asked for the probes on 1 November 2026; run the same day by two fresh helpers that read the
  documents only.
- Status: PARTLY DONE. The snapshot (DOC-10, installed 7bb0bfd) settled the document findings and
  TSC-1 settled the checker finding; the rest is carried into the Mode H + update + prospective design
  (register v0.23 lists which).
- What: Claude's list of 23 findings (gaps, ambiguities, stale text). The most important: the readers accept
  only the version-1 master, so any results update makes every run and report refuse until a version-2 reader
  is designed (Mode H design); the HOLDOUT_OPENED record is defined only in code; the updater's launcher runs an
  update when given no arguments; the two-site checker's default mode drives The Lott's website automatically
  (it must never be run that way).
- When: the snapshot (documents) and the Mode H + update + prospective design (the version-2 reader).
- Where: exchange/EX_116_Claude/cold_read_probe_findings.md (the 23 findings, and which the snapshot settles).
- Progress (1 November 2026): register v0.23 records which findings the snapshot settles and which it
  carries. The owner decided A5 (TSC-1: the checker stays unchanged and is never used again). A third fresh
  helper then cold-read the new H-1 and found 20 gaps; candidate 2 of the snapshot fixes them
  (exchange/EX_116_Claude/cold_read_h1_gaps.md). Two needed the owner: HX-2 (Powerball 1587 and 1588 are
  post-holdout draws, flagged when the catch-up scores them, staying fully valid and counted; the
  holdout is not extended) and FB-1 (if the
  week-of-9-November forecasts cannot be ready, slip a week rather than rush).

## R-013  A status line for the direction document now in doc/

- Asked: the owner, 2 November 2026, having committed doc/Direction_for_operational_procedures_v0_1.md
  (the plain-English statement of where the project is heading, written from the stock-take round).
- Status: DONE (4 November 2026): DOC-11, installed by the owner at 3d4fa3c, put v0.2r1 in doc/ (its
  "Status and authority" paragraph is the status line) and register v0.24 records it (DIR-1).
- What: the document sits in doc/ with no status line and has not been through a review round. ChatGPT is
  reviewing it at the owner's request; Claude then gives it a status line (author, reviewer, status) in the
  next document package, so its standing in doc/ is clear. The copy in exchange/ stays as the working copy.
- When: the next document package (the register edition that records the Mode H design).
- Progress (3 November 2026): the reviewer passed v0.2 and its two wording improvements made v0.2r1
  (exchange/Direction_for_operational_procedures_v0_2r1.md, 3a9f6ac). The owner removed the v0.2 copy from
  doc/ (6de0d99), so doc/ has no direction document for now. The owner wants a permanent copy in doc/,
  because it is the direction to be referred to and checked against: the next document package installs
  v0.2r1 (or its successor) in doc/ with its status line.

## R-014  The owner's simplicity (KISS) review

- Asked: by the owner in the ChatGPT reviewer chat (date not recorded here): a KISS-related review after
  final implementation. Raised by ChatGPT in the stock-take round (Response 2), recorded by Claude on
  2 November 2026, scope and timing corrected the same evening from ChatGPT's account, and confirmed by the
  owner on 2 November 2026.
- Status: OPEN. Starts only when the owner explicitly asks; never automatically.
- What: a comprehensive simplicity (KISS) assessment of the whole project's machinery: the method registry,
  the add-a-method and retire-a-method procedures, local experimentation without GitHub, the amount of
  authentication and verification, and general operational simplicity. Not to be started during the Mode H
  work.
- When: after full implementation and the follow-on work (the method waves), and only when the owner asks.

## R-015  The owner's choices still to come for MHUP-1

- Asked: recorded by Claude on 3 November 2026 from the ratified design (register v0.24, future actions).
- Status: OPEN.
- What: (a) Q7: whether, after a game's Mode H is scored, the display restriction on holdout draws is
  relaxed (recommended: keep the restriction on raw draw values in the AI chats); until decided, nothing
  changes. (b) At MHUP-A's approval: because Run_Experiment.bat gains interpreter options, either authorise
  one rerun of the Windows POC suite after the install (with the owner-run byte-code checks) or accept it
  unrun with the reason recorded. (c) Confirm the backup of results/ and source_data/ (asked 2 November 2026).
- When: (b) and (c) at MHUP-A's approval; (a) before Approval 2, the first results update.

## R-016  The staged AI handover (HO-2) and the later ChatGPT reviewer handover

- Asked: the owner, 3 November 2026.
- Status: OVERTAKEN (6 November 2026) for the ChatGPT reviewer handover: the reviewer chat ended without a
  handover; see R-022. The staged Claude handover is DONE (4 November
  2026): DOC-11 installed at 3d4fa3c (EX_138); the replacement Claude chat's first reply, the reviewer's
  questions Q1-Q9 answered blind, all PASS; the owner declared HO-2 complete and authorised normal work
  (option (a)); recorded in EX_139 and EX_140. The current reviewer stays in role through at least MHUP-A's
  first substantive code review.
- What: Claude is handed over first (DOC-11, the Step 1.1 review, the new chat's verified takeover, the
  owner's go-ahead); the experienced ChatGPT reviewer stays throughout. A ChatGPT reviewer handover (a new
  H-2 edition folding in register v0.24) is considered only after the new Claude chat has shown reliable
  continuity. No simultaneous ChatGPT takeover is prepared.
- When: raise the ChatGPT reviewer handover with the owner only after the new Claude chat has resumed
  normal work reliably, or if the reviewer chat nears its own limit.

## R-017  The name Lotterywest-GOV (LW-1) in the documents not yet edited

- Asked: the owner, 4 November 2026 (wording agreed with the ChatGPT reviewer chat).
- Status: OPEN (wording only; the rule is unchanged).
- What: "Lotterywest-GOV means exclusively the official Western Australian Government Lotterywest website,
  using HTTPS and the exact hostname www.lotterywest.wa.gov.au. No other Lotterywest-branded website,
  hostname or third-party source is authorised for retrieving production draw results." Register v0.24,
  H-1 v1r8 and its blurb use it (DOC-11). The documents not edited now read "Lotterywest" as Lotterywest-GOV.
- When: the Claude Code rulebook's rule 1 with MHUP-A's rulebook change (register v0.24, future action 1);
  the design at its next edition (future action 6); H-2 with the later reviewer handover (R-016). The
  direction document is DONE: v0.3r1 (installed at dfc2d13, 4 November 2026) uses the name.

## R-018  The owner's decisions of 4 November 2026, to be recorded and carried into the work

- Asked: the owner, 4 November 2026, during the staged handover (EX_139, EX_140).
- Status: OPEN until each is recorded and carried into its place.
- What, and where each goes:
  (a) Retrying after a STOP (the first results update in particular): a STOP is always a STOP; Claude
      reports it, diagnoses the cause and proposes the recovery; the owner explicitly authorises each retry.
      A retry may proceed under the existing Approval 2 only if the refusal came before admission (master and
      ledger unchanged) and the cause is positively identified as within the original operation (for
      example an insufficient window, fixed with --months-back). If the cause is uncertain, there is partial
      transaction state, or the retry would go beyond the approval, STOP for separately reviewed recovery
      steps and the owner's approval. Goes into: register v0.25, the next H-1 edition, MHUP-B's checklist.
  (b) The direction document aligned to the release-record date: DONE (v0.3r1, installed at dfc2d13).
  (c) The template README's draft number ("DRAFT 3" in the status line of draft 4): at the next authorised
      template edition.
  (d) Interrupted sessions: MHUP-B's operator checklist says an interrupted session must be safely resolved
      before any code-changing install, and that a session cannot be resumed after the code closure has
      changed. Goes into: MHUP-B's documents, under normal review.
  (e) E1, complete historical coverage: a deferred objective. Every method eventually gets retrospective
      forecasts for every applicable past draw, including the ten holdout draws; a later method's holdout
      forecasts only through a separately designed, reviewed and owner-approved process, as development
      evidence only, never part of the sealed Mode H study. Raise with roadmap 21b's back-history design.
  (f) E2, one consolidated owner-facing report, with development, Mode H, CATCH-UP and PROSPECTIVE kept
      separate, sample sizes shown, comparisons on common draws, no pooled score. Design with the
      cross-batch report, after WF-1C (roadmap 21b).
  (g) E3: recalculating a development report's quantities is not a second accepted score; accepted
      records are never altered. Check the actual WF-1B behaviour in the cross-batch report's design.
  (h) E4: after the owner's GOAL-1 declaration and the required installs and approvals, his deliberate run
      of Run_Weekly_Session.bat is that week's authorisation; no weekly approval round. Not for unattended
      scheduling, unusual recovery, a STOP, or anything outside the approved scope; the updater stays a
      separate operation. Goes into: register v0.25, the next H-1 edition (section 10.8), MHUP-B's checklist.
  (i) The direction document v0.3r1 ratified (dfc2d13): register v0.25.
- When: register v0.25 records all of them (with MHUP-A's round); each "goes into" item at its document's
  next authorised edition.

## R-019  MHUP-A slice 2: the reviewer's integration watchpoints from the slice 1 review (EX_142-EX_146)

- Asked: the ChatGPT reviewer, EX_144 sections 2 and 3 and EX_146 section 6 (5 November 2026), accepted by Claude.
- Status: (a), (d) and (e) CARRIED in slice 2 (EX_147, 5 November 2026: sections 4 and 5 name where each is tested;
  the E_1 revision 3 effective_date is set at the integrated package's preparation; the first real-ledger
  check, your T018 run, PASSED on 5 November 2026: the committed ledgers pass the full grammar); (b) and (c)
  stay OPEN for MHUP-B (no weekly writer exists yet). Checked again at the
  integrated package's review.
- What:
  (a) The admitted first update and the study version advance (design 4.1, 5.1). Slice 1's dispatch gate
      checks only that a Mode H plan's frozen version equals the opening record's freeze_version + 1 and that
      the request pins it. That is not proof of a complete admitted first update. Slice 2's plan writer
      (Method_Walk_Forward.py --mode H), the updater v0.2's first-update admission (the UPDATE must reach at
      least holdout_last), every Mode H `run` check and the scorer must enforce the complete-range rule and
      read the study version advance record where one exists, each with synthetic negative oracles (a first
      UPDATE stopping short; a plan at a version that is not v_a or v_a'; an advance record present).
  (b) The freeze line's full shape (design 6.5). Slice 1's forecast_ledger_lines checks a known schema and a
      whole-number target only. When slice 2 defines the FREEZE_LINE_V1 contract and its writer, the reader
      must validate every required field before a line counts as present evidence or closure, and a known-
      schema but malformed line must refuse, never count as valid unrelated evidence; oracles accordingly.
  (c) The FINAL_NEXT_DRAW / CATCH_UP binding-rule mutant, equivalent in slice 1 because those modes are
      unreachable, is re-run when slice 2 makes them producible.
  (d) E_1 revision 3's effective_date (EX_146 item 4): set to the integrated package's actual preparation
      date before its final review freezes the registry bytes and digests; never the admission or release
      date. Test the real release-record producer and consumer paths once slice 2's writers exist, not only
      slice 1's mocked dates.
  (e) Integration evidence (EX_146 item 5): the updater's actually emitted ledger bytes, the Mode H plan and
      opening outputs and the weekly writers' outputs reconciled with the strict readers and gates (a real
      ledger refused by the strict grammar is a STOP, never a reason to relax it); fail-closed recovery,
      install safety and end-to-end synthetic lifecycles, with the applicable EX_131 and Appendix L items.
- When: slice 2's development; its handback names where each is tested. Slice 1 PASSED (EX_146, 5 November
  2026); the integrated package needs its own integration review.

## R-020  MHUP-A integrated package: what the package or the owner must carry (from slice 2; (d)-(f) added 6 November 2026)

- Asked: Claude, from slice 2's development (EX_147, 5 November 2026).
- Status: OPEN until the integrated package is built and reviewed (slice 2 PASSED, EX_152, 5 November 2026; the owner's "go"
  for the integrated package, 8 November 2026; the rebuild on main 009c985 ran 570 tests on each Python with one expected
  date-pinning failure, now fixed in the build, the final suite still to run on the frozen package; the package itself is not
  yet built: exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/PLAN.md).
- What:
  (a) The package manifest's `release_entries` must name E_1 revision 3 for both games, so that the install's
      release record (Appendix J step 16) releases it: the baseline record carries revision 2 as superseded and
      the registry's released set equals the baseline's unretired entries plus revision 3 (a test asserts this).
      Until that record exists, revision 3 has an install record only and is not released for CATCH-UP.
  (b) The study manifest's environment freeze refuses any file under the venv's site-packages that no RECORD
      lists (an orphan: a .pth file, a leftover of a hand install). If your venv holds one, Approval 1's
      `manifest` command refuses and names it; that is the intended outcome, and the fix is a reviewed step,
      never a hand deletion. The Windows branch of the inventory (python.exe, the DLLs, DLLs/ and Lib/) first
      runs on your machine at T016, where a refusal is a STOP to send to Claude.
  (c) Run_Experiment.bat changes (the byte-code lines of design 4.1): the design asks you, at MHUP-A's approval,
      either to authorise one rerun of the Windows POC suite after the install or to accept it unrun with the
      reason recorded (the change adds interpreter options, two variables and one refusal; no launch, handshake or
      lifecycle logic). Claude will ask when the integrated package is ready.
  (d) Added 6 November 2026. Rebase the candidate from its base (main at 2061055) onto the current main. The candidate's
      `.gitignore` is a whole-file copy made from the old base; your new lines (the GAIS `.bin` files and
      `src/GAIS/OUTLANDISH_01/ycruncher_digits/`) must survive.
  (e) Added 6 November 2026. Your commit f1883df (5 November 2026) added `pyahocorasick` to `DIRECT_PACKAGES` in
      install_upgrade_dependencies_into_venv.bat. If it is installed, the venv changes, and MHUP-A's environment freeze
      records it at Approval 1. Claude will ask whether it is installed, and whether that dependency change is to be
      recorded as approved.
      DECIDED (owner, 6 November 2026, DEP-1): "pyahocorasick i installed for an outlandish GAIS test and approved it. we
      keep it." It is an approved dependency and installed in the venv, so MHUP-A's environment freeze records it at
      Approval 1. Register v0.26 records DEP-1.
  (f) Added 6 November 2026. `src/GAIS/` (your thought experiments) now sits inside `src/`, which MHUP-A's code closure
      covers. Claude will ask whether to move it out of `src/` before Approval 1, or have the closure leave it out by a
      reviewed rule. This is a question for you, not a decision.
      DECIDED (owner, 6 November 2026, GAIS-1): "GAIS has been moved up alongside src" - a top-level GAIS/ folder, outside
      MHUP-A's code closure. The y-cruncher program is to be untracked by .gitignore and kept on disk. DONE once the
      owner's commit reaches GitHub and Claude has checked it. The integrated package then rebases onto that main.
      DONE (6 November 2026): the owner's commit 6b99029 (now 9d28b9f after the history clean-up, R-023) moved GAIS to the top
      level, and its .gitignore untracks y-cruncher.
  (g) Added 8 November 2026: **a decision for you before T016.** Appendix J's steps 2, 3, 12, 16 and 18 run process_check.py and
      install_records.py, and Claude Code's rulebook v0.4 rule 7 forbids the runner from running either in any command. Either
      (i) rulebook v0.5 allows those two tools only inside a task clone, only from the package's staging folder, only under a task
      file (reviewed with the package), or (ii) you run T016's steps yourself, with Claude Code only preparing the clone. Claude
      recommends (i), because it keeps the rehearsal in a clone that cannot push; the reviewer should see the rule change.
      The reviewer (EX_157 section 3) also prefers (i), with conditions: explicit owner approval; only those two tools, only
      in T016's synthetic clone, from the staging folder; every other safeguard unchanged; the settings denials not bypassed;
      check_task_commands.py passing; no change to the main repository; T016 still needs its own go. OPEN: your choice is
      needed before the rulebook change or the T016 task file is written.

## R-021  MHUP-1 design amendment A1 (the Mode H score ledger published whole, once): your final approval

- Asked: Claude, EX_149 (5 November 2026), after your in-principle choice of EX_148 B01 route (B).
- Status: DONE (5 November 2026): ChatGPT's EX_150 reviewed A1 favourably and you ratified it ("i hereby
  authorise and ratify that A1"); the ratified record is exchange/MHUP1_design_amendment_A1_RATIFIED.md. Still to
  do: the register and the design document record A1 in the next documentation package.
- What: exchange/EX_149_Claude/MHUP1_design_amendment_A1_draft.md (sections 1-5). Its section 6 records
  your other decision: the corrective scoring run after the Mode H seal is MHUP-B's, by the route stated
  there. When approved, the register records A1 and the integrated package carries it.

## R-022  The ChatGPT reviewer chat ended without a handover (6 November 2026): the new reviewer's takeover

- Asked: the owner, 6 November 2026 ("chatgpt has just permanently died ... without producing an updated handover doc").
- Status: DONE (6 November 2026): you accepted the new reviewer and ratified H-2 v1r9 and register v0.25 (RAT-25); you install
  them with exchange/DOC12/ (DOC-12).
  Progress (6 November 2026): the new reviewer accepted the role (EX_153; rights region verified; five documentation
  corrections, all applied as candidate 2 in EX_154). Claude's verification questions Q1-Q19 went with EX_154; you hold
  Claude's sealed answer key. Next: the reviewer's EX_155, then Claude's comparison, then your acceptance. Replace the
  candidate 1 copies you placed in doc/ at 929eff5 with candidate 2, or remove them; they are not ratified.
  Further progress (6 November 2026): EX_155 passed C01 on RECHECK and answered Q1-Q19 blind; Claude's EX_156 published the
  key (its hash matches) and found all nineteen answers agreeing. C06 and O02 are applied as candidate 3. What is left: your
  acceptance of the reviewer, then, when you wish, ratifying and installing H-2 v1r9 and register v0.25 candidate 3.
- What: Claude, as the surviving team member, wrote the following on your instruction, in exchange/HANDOVER_2026_11_06/:
  - Claude's own handover delta H-1 v1r9 and its blurb;
  - the reviewer handover H-2 v1r9 (reconstructed from H-2 v1r8 and EX_141-EX_152, with the reviewer's rights carried
    unchanged);
  - the reviewer's blurb.

  H-2 v1r9 is not the reviewer's own work, so the new reviewer must verify it against the repository before it relies on it.
  The new reviewer's first task is that takeover check. Its first review is the integrated MHUP-A install package.
  The handovers go into doc/HANDOVER/ in the next documentation package, with register v0.25.
- When: before the integrated MHUP-A package is sent for review.

## R-023  The GAIS history clean-up (6 November 2026): what is left

- Asked: the owner, 6 November 2026; done the same day (exchange/HISTORY_CLEANUP_2026_11_06/CLOSEOUT.md).
- Status: OPEN for (b) and the OUTLANDISH chat's confirmation of (d) only. The rewrite is DONE (main 9d28b9f; 27 commits
  renumbered; crosswalk commit-map.txt); (a) DONE; (c) is standing advice.
- What:
  (a) Optional: clear the leftover junk from your local .git (about 900 MiB). Copy the .git folder first, then run
      git reflog expire --expire=now --all and git gc --prune=now.
      DONE (6 November 2026, 11:27): the .git folder was copied to E:\TEMP\git_backup_before_gc; the local .git went from 982.94 MiB
      to 48.64 MiB; fsck clean; the pull fast-forwarded to cf1c6d9. Keep the copy a few days, then delete it.
  (b) Old commit IDs cited in records before 6 November 2026, 11:25, are translated with commit-map.txt. Register v0.26 cites
      the folder.
  (c) Keep E:\TEMP\repo_before_cleanup.bundle (the only copy of the old history) until you decide otherwise. A second drive is
      advisable.
  (d) The follow-on handover to your OUTLANDISH (GAIS) ChatGPT chat: the GAIS move, the ignore rules, this clean-up, and a
      recommended ignored folder for large generated files under GAIS/OUTLANDISH_01/. Done by the owner with the ChatGPT
      reviewer chat (6 November 2026); the OUTLANDISH chat's confirmation is awaited.
- When: any time; none of it blocks the integrated MHUP-A package.

## R-024  The handover documents of 8 November 2026 and the documentation round after them

- Asked: the owner, 8 November 2026.
- Status: RATIFIED (RAT-27, 8 November 2026, after the reviewer's EX_161 corrections were applied in EX_162); OPEN only until you
  install DOC-13 with exchange/DOC13/README.md and Claude verifies it from GitHub.
- Done: H-1 v1r10r1 delta and blurb (EX_157 check, EX_158 corrections, EX_159 PASS) RATIFIED by you as working supplements to
  H-1 v1r8 (RAT-26, 8 November 2026) and installed in doc/HANDOVER/ (b866e42).
- To do (Claude, then the reviewer, then you): H-2 v1r10 delta and blurb (the reviewer's insurance); the root README (GAIS/,
  create_venv.bat); the new-method template draft 5 (status line, release records after MHUP-A, data kind not run mode); the
  design v0.1r6 (A1 folded in, Lotterywest-GOV, status lines); an optional move of superseded editions into doc/superseded/;
  register v0.26 recording all of it; one DOC-13 install for you. Rulebook v0.5 waits for your R-020 (g).
- Left for later on purpose (the register prevails meanwhile): Architecture v0.10 (with MHUP-B), R3 v0.6, the E2R contract
  spec, Proposal v0.7 (each when next edited), the holdout exposure record (after Q7), the next full H-1 and H-2 editions
  (after MHUP-A).

## Standing reminders

- The stock-take round of 2 November 2026 and the owner's ratification of its positions are recorded in
  exchange/STOCKTAKE_2026_11_02_v0_8.md; the plain-English direction is
  exchange/Direction_for_operational_procedures_v0_2r1.md and the ratified MHUP-1 design is in
  exchange/EX_132_Claude/ (both in doc/ once DOC-11 is installed).
- Show the owner where the project is up to (exchange/OWNER_ROADMAP.md) at each milestone, and
  whenever asked.
- Save every downloaded ZIP to E:\TEMP, never into the repository (the browser defaults to review/).
- Model choice (owner, 2 November 2026; provisional, the owner may drop it after assessing it): before
  starting any of these, Claude stops and says "Suggest switching to Fable (High) for this" and waits for
  the owner's "go": designing a new subsystem or a major change to one (for example Mode H, the results
  update, the version-2 reader, catch-up, the prospective record); statistical design or validity
  questions; root-cause investigation of an unexplained failure or STOP; a cold-read review of a design
  before it goes to ChatGPT. Everything else (packaging, task files, install steps, roadmap and reminder
  updates, explanations, paste blocks) goes ahead without asking. When a Fable task is finished, Claude
  says so, so the owner can switch back to Opus before the everyday work. Claude cannot see which model
  is selected, so it always flags and holds; a request mixing both kinds is split at the boundary.
  Refinement (owner, 3 November 2026): Fable is to be saved for the really complex work, because the
  owner's token allowance may otherwise run out before the end of a week; so at each step Claude says which
  model it recommends (Opus 5.5 or Fable) and why in one line, recommending Fable only for the hard core
  (new HIGH design, the core of a HIGH code module, a BLOCKER-level review finding, an unexplained STOP)
  and Opus for everything else, including packaging, tests scaffolding, task files, installs, records and
  relays. Cold-read helpers can run on a cheaper model whatever the chat's model.
  Recorded as MC-1 in register v0.24 and carried in H-1 v1r8 section 2.
