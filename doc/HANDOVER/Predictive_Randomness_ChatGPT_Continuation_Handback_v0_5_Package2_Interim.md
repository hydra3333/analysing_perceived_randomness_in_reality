# Predictive Randomness — ChatGPT Continuation Handback v0.5

**Status:** INTERIM, SELF-CONTAINED CONTINUATION HANDOVER — 24 October 2026 (Australia/Adelaide). **Not a code release, not a new ratification, and not a substitute for the ratified repository specifications.**

**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Owner's Windows repository root:** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`  
**Prepared for:** the next ChatGPT development conversation, the independent Claude reviewer, and the owner.  
**Supersedes for *current operational continuity*:** `doc/HANDOVER/Predictive_Randomness_ChatGPT_Continuation_Handback_v0_4.md` (23 October 2026). Retain v0.4 unchanged as historical evidence; its then-active orphan-marker notice is **not** a current-state instruction.  
**Reviewer handover:** Claude maintains its own separate handover. Its *latest* text was not supplied for preparation of this document; reconcile both once available. Do not assume the archived Claude v5 is its latest handover.  
**Recommended repository destination, after review/owner choice:** `doc/HANDOVER/Predictive_Randomness_ChatGPT_Continuation_Handback_v0_5_Package2_Interim.md`.

> **Immediate operating rule.** Package 2 multi-game infrastructure **coding is authorised**. Four **incremental, uninstalled, unratified** development checkpoint ZIPs are retained under the owner's `Review` folder. They are **not** a completed or safety-reviewed implementation. **No live Oz Lotto scrape, real Oz experiment, holdout access, coordinated E-method execution, prospective FINAL, destructive coordinator test, or process termination is authorised.** `ENABLE_PROCESS_TERMINATION = False` and `ENABLE_SCIENTIFIC_COORDINATION = False` remain binding for the proposed coordinator patch. Verify actual runtime marker state locally before any permitted run.

---

## 1. Start here: authority, precedence, and a safe restart

1. Obtain the **actual current Git commit, `git status --short`, ratified documents, and any newer committed changes** before editing. The last owner-supplied authoritative **ratified-document baseline** is `057fd8c618c00d162324149e949fc71ab72ca3ce` (24 October). Owner subsequently reported committing/pushing interim checkpoint ZIPs under `Review`; **their resulting Git HEAD was not supplied**. Review ZIPs in Git are evidence, **not live source installation**. The assistant cannot infer local runtime state from Git.
2. Read the ratified Package 1 documents in the checkout: Proposal v0.4; R1 v0.4; R2 v0.3 **plus erratum v0.3 / ERR-R2-05**; R3 v0.3; Architecture v0.6; Multi-Game P3 Task Spec v0.1; `TIE_SHA256_V1` Contract Note v0.2; Ratification Register v0.2. Use these rather than the superseded original charter or Architecture v0.5. The P0–P2 POC Task Spec v0.2 remains relevant to coordinator safety.
3. Obtain **all four** incremental Package 2 ZIPs listed in section 5. They are **deltas, not cumulative complete releases**. Do not overwrite the checkout with them. Consolidate against a verified current repository tree into a separate review candidate, inspect every exact diff, and submit **one** combined package to Claude for independent review before owner-directed Windows installation/tests.
4. Do not confuse approval to **write Package 2 code** with approval to **use** a scraper or coordinator on real data. The first live Oz Lotto collection is separately gated as Package 3, followed by a mandatory STOP after a bounded structural audit and first-snapshot holdout seal.
5. Safety-critical real runtime information outranks this document: check the global `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json` marker and associated clearance/archive records in the owner's Windows checkout. A marker, if present or uncertain, blocks new coordinator runs. Never guess that it is absent, delete it casually, or bypass it.
6. **Current status supersedes historical status statements in older documents.** The old ChatGPT v0.4 handover was written *before* a manually controlled orphan-marker clearance. Subsequent user-reported clearance and a successful non-destructive fixture occurred; that does **not** prove the marker's current filesystem state in a future session. Likewise, older task documents may say Package 2 is paused: the owner **subsequently authorised Package 2 coding** in this conversation.

**Authority classifications:** `RATIFIED` = governing owner-approved specification; `DECIDED` = routine implementation choice consistent with it; `RECOMMENDED` = proposed consequential choice awaiting owner ratification; `OPEN` = missing evidence or decision; `TESTED (Linux offline)` = a rehearsal result, **not** Windows acceptance; `CHECKPOINT` = uninstalled development code. Claude independently reviews material scientific identity, safety, source/holdout, and FINAL changes; the owner alone ratifies them. Routine low-risk engineering choices are delegated to ChatGPT.

## 2. Project and scientific boundaries — current, not 23 October snapshots

- Two selected **Australian national games**: `POWERBALL` (from draw **1144**, 19 April 2018; 7 distinct MAIN labels 1..35 plus one PB 1..20) and `OZLOTTO` (current era from draw **1474**, 17 May 2022; 7 distinct MAIN labels 1..47). Oz Lotto's three supplementary numbers stay in **raw source provenance only**; no modelling, predictions, or scoring with them. Pre-1474 Oz Lotto era is excluded. No fictitious Oz Powerball barrel.
- Authoritative draw identity is **`(game_id, draw_number)`**, *both fields*, not draw number alone. Display `POWERBALL_1577`, `OZLOTTO_1474` etc. One explicitly selected game per run; profiles are narrow frozen source-code constants, no user-configurable barrel sizes; `game_id` pattern `[A-Z][A-Z0-9]*`.
- Training/calibration view for prediction target **N** contains only draws **strictly before N**. Method prediction must not parse the target row. Date is a profile-derived function `era_date + 7 days * (draw_number - era_first_draw)`, validated against each source date. Date anomalies warn in the structural audit and block date-using methods E_14/E_54; they do not independently fail a otherwise number-valid snapshot or expose a holdout. Default U-view digests exclude dates; date-consuming new view schemas bind their profile/date domain appropriately.
- **Powerball historical-development target ceiling:** draw **1577**, with **sealed holdout 1578..1587**. **Oz Lotto historical-development target ceiling:** one less than the **first draw in the Oz holdout**, which is **not yet established**. Oz's holdout selection rule is the **ten highest draws in its first structurally accepted winning-numbers snapshot**, fixed and recorded once without inspecting outcomes. These ceilings apply to **retrospective development/backtesting only**, not to later separately authorised **prospective FINAL, routine operation, maintenance or eligible weekly retraining**. Those future modes retain N−1, freeze, and per-game holdout protocols.
- Every new view schema **of either game** binds `game_id`, era, and profile version. Preserve the special legacy E_1 Powerball U-view identity `E1_REAL_U_TRAINING_VIEW_V1` and `TIE_SHA256_V1` exactly, including the four-byte unsigned little-endian UTF-8 field-length framing; never mutate old CSV bytes to make new wrappers convenient. New result wrappers need new schema/version identities; v0.1 results without `game_id` are interpreted as POWERBALL under the versioned compatibility rule.
- R1 contains E_1..E_62, not E_63. Do not exclude formula families due to null expectations, create invented second barrels, or silently register E_63. Method support is per game: `SUPPORTED`, `UNSUPPORTED_FOR_GAME` (structural reason) or `FORMULA_OPEN`; only E_1 currently implemented in the new synthetic path.
- Synthetic and real workflows remain rigorously isolated. Failed, orphan-suspected, hash-changed or unreceipted (in coordinated/FINAL mode) results must never enter scoring, even if a canonical result file exists. Scoring must validate the frozen successful result **before** obtaining the target outcome. Each game's metrics and reference probabilities are separate; **no pooling** across games absent preregistered protocol.
- Preserve the intended user entry point `Run_Scraper.bat POWERBALL|OZLOTTO`, with existing `.venv` checks, durable per-game winning/raw snapshots, SHA-256 provenance, create-only publication, and **separate operator-controlled snapshot acceptance**. Collection does not trigger training or experiments.

### Frozen accepted Powerball E_1 reference (do not approximate)

Historical **development** forecast for draw 1577, based **only on 1144..1576**:

| Reference | Exact recorded value |
|---|---|
| Historical real-U training-view SHA-256 | `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339` |
| Canonical forecast SHA-256 | `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e` |
| TOP MAIN | `[9,17,7,11,18,30,12]` |
| TOP PB | `2` |
| WORST MAIN | `[31,13,8,29,26,33,35]` |
| WORST PB | `12` |
| Historical source CSV SHA-256 | `6dc91efe2f5d3993c9c7247d979a16ad2a5082a4eaa364fad3d6ef9f31ebb1d7` |

The earlier real Powerball E_1 standalone run was already owner-authorised, independently verified, and consumed PASS; this is **not** authorisation to execute new methods or score draw 1577. The new generic profile-driven path has **Linux offline regression evidence** matching these identities. Synthetic training-view (`df21871f...`), tie (`7ce5ab1b...`) and forecast (`7b43d659...`) hashes also remain frozen regression inputs. Do not substitute a newly serialised result wrapper's hash for the legacy canonical result hash.

## 3. Process safety — independent of the multi-game project

These owner-ratified or previously accepted P2 controls remain fully binding:

- **Strict no-status/no-kill:** No termination signals unless the experiment PID **and creation time** positively match its run-status data **and** verified launched process ancestry. No matching status, no kill, even if hanging. A status PID is not authority to kill; Task Manager names are not ownership evidence. Captured wrapper root Popen handle/identity, alive ancestry and executable sanity are necessary; no `taskkill /T /F`, name-wide kill or automatic fallback.
- **`ENABLE_PROCESS_TERMINATION = False`** until a separate owner-approved, independently reviewed destructive-test gate. Do not flip it for convenience. An orphan-suspected/unknown process causes STOP and an unresolved global marker; no automatic bypass or process-name-based cleanup.
- On existing orphan marker: prominently display **SAFETY STOP**, block further launches across **both** games, inspect PID + creation times. If any process alive/uncertain, leave marker and escalate. If all exited, perform the **separately authorised manual** archive-of-original-bytes/hash + deliberate confirmed clearance procedure. Do not automate clearance or infer permission from this handover.
- Durable early `STARTED` status should be written before heavy imports when feasible; safety-critical status uses careful atomic publication, and diagnostic STOP messages are flushed. Global FAILED/orphan result firewall persists.
- Windows Console Ctrl+C and timeouts can affect child processes outside the coordinator's own kill function; do not casually run destructive watchdog, timeout or cancellation demonstrations. The original coordinator v0.6 source SHA-256 is `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`.

**Exit-receipt development (checkpoint only):** Claude required a coordinator-only, create-only `group_dir/receipts/<run_id>.json` that a worker cannot pre-create in its run folder. Issue only after coordinator Popen-observed wrapper exit **and** the v0.6 exit-time descendant/status orphan check shows no alive/unknown identity, together with strict console digest matching and group success. Bind coordinator SHA-256; group/worker/run/game/draw/method/variant IDs; captured root PID/create time; observed UTC exit and return code; status PID/create time; post-exit SHA-256 of worker `status.json`, worker manifest and canonical result. Coordinated/FINAL consumers must reverify the receipt and all hashes **before reading a result**. This mitigates accidental/method self-certification and late modifications, **not a malicious local user** (no signature). Existing POC workers cannot issue receipts. The candidate patch has `ENABLE_SCIENTIFIC_COORDINATION = False` and unchanged kill safeguards. **No Popen lifecycle Windows acceptance yet.**

## 4. Ratified documents and exact installation lineage

**Package 1 multi-game documentation** was owner-ratified 24 October 2026 following Claude's independent no-blocker review and specified corrections. Final installation ZIP:

`Predictive_Randomness_MultiGame_Package1_v0_3_RATIFIED_INSTALL.zip`  
ZIP SHA-256 `632d11eb07a475ffff503556bfe9cb5d28a0a9d47c9485d8433c6366dd0888b8`.

Contents (installed under `doc/`, per owner-reported later commit `057fd8c...`):

1. `Predictive_Randomness_Research_Project_Proposal_v0_4.md` — extended research charter (replaces v0.3 as current charter).
2. `Predictive_Randomness_R2_v0_3_Erratum_Record_v0_3.md` — approved ERR-R2-05; underlying R2 v0.3 retained.
3. `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_3.md`.
4. `Predictive_Randomness_Software_Architecture_Discussion_v0_6.md` — self-contained; its original process-safety §5C preserved.
5. `Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_1.md` — governs Package 2 scope and Package 3 separate gate.
6. `contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md`.
7. `RATIFICATION_REGISTER_v0_2.md` — first installed/current register.

The Proposal v0.4, R1 v0.4, original R2 v0.3 plus ERR-R2-05, R3 v0.3 and Architecture v0.6 are the actual science/engineering contract. POC Task Spec v0.2 still governs legacy coordinator operation. Archive v0.4 of *this handback* and earlier Package 1 review candidates as history. Do not treat old Review ZIPs as endorsed runtime files.

## 5. Package 2 four-checkpoint inventory — preserve ALL four, then consolidate

**Status for every ZIP:** `CHECKPOINT / NOT INSTALLED / NOT CLAUDE-CONSOLIDATED-REVIEWED / NOT RATIFIED AS COMPLETE PACKAGE 2`.

| Incremental checkpoint | SHA-256 (ZIP) | What it actually added | Offline test evidence |
|---|---|---|---|
| `Predictive_Randomness_MultiGame_Package2_Foundation_v0_1_CHECKPOINT.zip` | `2a98fa5ceab9810c24607ec599ebd69945a9c925b779243342dbdeca959eb51e` | Frozen profiles, per-game registry, synthetic U-view + generic E_1, synthetic bounded structural audit, create-only synthetic publisher, generic standalone consumer, disabled `Run_Scraper.bat`/dispatcher | 16 new + 13 legacy E_1 PASS (Linux) |
| `Predictive_Randomness_MultiGame_Package2_Source_Provenance_v0_3_CHECKPOINT.zip` | `e547d1ef67257bd4e414db0898409933345000415f69b781f91bda4447edfeac` | Offline source parsers/plans; robots-policy check from **supplied bytes**; no network; raw-response SHA-256 archive; label-bound Oz MAIN/SUPPLEMENTARY parsing; bounded cross-publisher comparisons; order agreement distinguished from set agreement | 42 multi-game + 13 E_1 PASS (Linux) |
| `Predictive_Randomness_MultiGame_Package2_Console_Scoring_v0_4_CHECKPOINT.zip` | `c97eb7504c7d7e6d167a2cbc11937c8864dc572a72fd0e66a0aaabedad987a39` | Method-generic BEGIN / RESULT / DIGEST / FINISH console validator; barrel-aware synthetic-only scorer, validates failure firewall before outcome callback; independent Powerball 1577 golden forecast | 50 multi-game + 13 E_1 PASS (Linux) |
| `Predictive_Randomness_MultiGame_Package2_Exit_Receipt_v0_5_CHECKPOINT.zip` | `182af12061ccdf1e65c069b28707d6275c5869c4f33913cb7f4d9a8e886a0e38` | Coordinator-only receipt issuer/consumer + 11 synthetic security tests; dormant proposed coordinator v0.7 patch/diff vs v0.6; no operational E-method launcher | 61 multi-game + 13 E_1 PASS (Linux) |

**Local evidence verification performed for this handback:** All four checkpoint ZIPs are present in the assistant's working container and their ZIP SHA-256 values above match the actual files. Their accompanying `README_CHECKPOINT.md` files were read. Their Linux test totals are **those recorded in checkpoint readmes/transcripts**, not newly executed or Windows-certified by preparation of this handback. Claude reported a quick manifest check of v0.3 and v0.4; it explicitly deferred the consolidated independent review. Checkpoint v0.5 contains the exact coordinator v0.6→v0.7 proposed diff and an independent review note, **not** Claude acceptance of v0.7.

**Overlay caution:** v0.1 + v0.3 + v0.4 add independent new files; v0.5 adds two new files plus **a candidate replacement of `src/Powerball_Experiment_Coordinator.py`**, which must be compared byte-for-byte against actual Git HEAD and independently reviewed for process safety. New code is not known to have been applied to the live checkout. The owner said checkpoint archives are committed under `Review`; that is archival, not installation or acceptance. New tests are partly cumulative: **74/74** is the latest combined rehearsal total, not 74 additional tests.

### Confirmed implemented versus deliberately absent

**Implemented/prototyped offline:** narrow profiles and registry, synthetic prefix reader, future-row poison safety, metadata-only auditor with holdout-value redaction, synthetic create-only snapshot fixtures, source-policy evaluator using caller-supplied text (not a live network client), independently labelled source adapters/parsers from fixtures, bounded discrepancy reporter, console parser, synthetic scorer, coordinator-owned receipt *functions*, proposed dormant coordinator hook, and frozen Powerball 1577 regression.

**Not implemented or not complete:** actual network fetching and working on-demand live scraper, operator source HTTP response adapter end-to-end, durable real snapshot acceptance ledger and final Oz first-snapshot holdout seal, accepted Windows `.bat` execution, method-generic real E-method launch / root-run handshake / worker manifest producer, coordinator Popen process-lifecycle integration, coordinated `verify_and_consume`, prospective FINAL, real scoring, ratified walk-forward, full reporting and E_2..E_62 methods. Existing E_1 runner and Powerball source CSVs are unchanged.

## 6. Source-selection resolution — research v2 supersedes v1

Claude's independent `Claude_Research_Historical_Results_Sources_v2.md` (24 October; real browser inspection) **supersedes v1 entirely**. It verified robots directives permit crawling at `oz.lotterywest.com` and `lotterywest.wa.gov.au`; Oz Lotto per-draw URLs exist; fields labelled "Main Numbers" and "Supplementary"; first-era Oz Lotto draw 1474 agreed with The Lott on early-number sequence by hash. Powerball training 1144..1577 agreed across three publishers in 434/434 comparisons. Claude corrected v1's erroneous "robots refused" finding. Its research was bounded and did not open Powerball holdout results or bulk-collect Oz results.

**Agreed operational strategy for coding:** `Lotterywest` serves as the **official source common to both games** while keeping the **existing Powerball pipeline and accepted snapshot** untouched (`powerball.net` year archives + Lotterywest for drawn order). Proposed Oz primary: Lotterywest per-draw `.../oz-lotto/results/draw/N`. Secondary Oz verification: `lottodraw.com.au` with bounded cross-publisher checks. Use pluggable per-(source, game) adapters in one shared fetch/validate/immutable-publish framework; the old Powerball source need not be migrated merely for uniformity.

- Source order is **`SOURCE_ORDER_UNVERIFIED`** until a documented cross-publisher check; winning **set** agreement alone is not proof of physical drawn order. Keep exactly `DRAWN_ORDER_VERIFIED` / `SOURCE_ORDER_UNVERIFIED` / `SORTED` distinctions.
- Count every expected draw number; incomplete archives are failures (an earlier third-party copy missed PB 1584 and Oz 1701–1702). Source dates are provenance, verified against profiles; numerical discrepancies block acceptance while date anomalies block date methods only.
- User explicitly considers factual winning numbers public information; this does not authorise anti-bot evasion. Follow robots, use honest project identification, rate limiting, backoff, raw-response hashes, and no browser impersonation or undocumented The Lott API. Do **not** make contacting the operators a prerequisite; owner declined contacting them.
- Do not copy raw source HTML needlessly into public Git; keep archival hashes/provenance and distinguish actual fetched bytes from synthetic fixtures. The owner considers source-result CSV public-data publication acceptable. No live scraper has been exercised. The Lott nominal broadcast time vs Lotterywest's local display is unresolved; do not invent timezone/cutoff—use independently established closing-time rules when prospective publication is actually designed.

## 7. Exact next engineering work, in safety-preserving order

**This is the work to pick up, not a request for a new research programme.** Package 2 code authorisation is still in effect, but no execution gate changes.

1. **Reconcile tree before new edits.** Get the owner-reported `git rev-parse HEAD` and `git status --short` and, preferably, a current repository ZIP or exact Git source. Reconstruct the four *incremental* overlays in a scratch tree on that baseline. Confirm no unreviewed alteration to ratified documents, E_1 source, Powerball CSVs or v0.6 P2 safety functions. If source in the checkout differs, stop and reconcile rather than overwriting it.
2. **Resolve coordinator/scientific-worker interface on paper and offline first.** Existing coordinator is POC-only. Plan the game-qualified `--game` + target + run ID/root handshake, per-method wrapper command, worker `manifest.json` production and console protocol, and ownership-safe `exit_receipt` issuance. The current receipt hook is **dormant**; no POC receipt and no E-method launch. Cross-check Claude's six binding receipt design points and v0.6 safe-exit semantics. Do not fabricate a PASS record from a worker's self-report.
3. **Implement offline synthetic integration** including malformed/missing BEGIN/FINISH, manifest hash or target mismatch, forged receipt, source overwrite, same draw number in different games, unresolved global marker, group FAIL, Popen wrapper exit-before-receipt; maintain process termination off. Distinguish static/synthetic checks from actual Windows subprocess lifecycle tests.
4. **Finish source-independent scraper publishing and launcher** without live collection: common network-aware interface only if safe, actual adapter/parser tests against supplied **synthetic or allowed bounded archived** fixtures, robots behaviour (empty Disallow vs unavailable fail closed), immutable separate winning/raw outputs, SHA-256, acceptance ledger, `.venv` preservation, create-only collision tests and bounded cross-publisher checks. `Run_Scraper.bat POWERBALL|OZLOTTO` may exist but live mode stays disabled.
5. **Bring the scorer and E_1 reader together end-to-end on synthetic fixtures**, test intrinsic barrel-only Oz scoring, nil PB channel, native-score tie mid-ranks and outcome access *only* after PASS/firewall. Reconfirm Powerball 1577 frozen digest/TOP/WORST and synthetic goldens. Do not implement real walk-forward or score held-out Powerball draws.
6. **Prepare the one consolidated Package 2 Claude review ZIP** with current Git/source identity, all new/changed files, file SHA-256, exact v0.6→candidate coordinator diff, synthetic test transcripts, failure/orphan test cases, DECIDED/RECOMMENDED/OPEN status, explicit limited threat model, and safe Windows test plan. Independent Claude review precedes installation/testing. The owner then runs safe Windows synthetic acceptance only after resolving review findings.
7. **Separate Package 3 gate:** after the approved/reviewed code passes owner Windows tests, request independent owner authorisation for the **first real Oz Lotto scrape**, bounded structural audit and ten-highest holdout seal. STOP there; scientific Oz method execution needs its own subsequent approval.

### Key unresolved or not-yet-ratified items (do not solve by inventing assumptions)

- Actual coordinator v0.7 scientific launcher, console/receipt lifecycle and Windows behaviour; exact v0.6 diff review and process-ownership safety gate.
- Trusted worker manifest schema, profile/view hash binding and real run-root handshake; whether new generic result schemas are complete and accepted.
- Actual Oz Lotto first accepted snapshot and permanently fixed holdout boundary, receipt of official era source fields; no holdout values should ever be printed.
- Prospective FINAL closing/deadline clock, timezone evidence, E_54 known-before-draw external covariates, real per-game score publication.
- E_1 zero-burn-in historical walk-forward 1145..1577 (recommended, **not ratified**), later E_2..E_62 methods and E_63 placement (separate owner choice).
- Full Windows 3.14.8 `.venv` acceptance; source-dependent bot/format/terms drift; any changes in real source beyond the reviewed checkpoint.
- Whether any newly submitted Claude handover contains decisions not included here; obtain it when available.

## 8. What a future ChatGPT chat should actually receive

**Preferred normal transfer = ONE current ChatGPT handover, not two handovers that must be mentally merged.** Give the next ChatGPT chat:

1. **This** `Predictive_Randomness_ChatGPT_Continuation_Handback_v0_5_Package2_Interim.md` as the **current** ChatGPT continuation handover; explicitly state it supersedes v0.4 for current status.
2. The **current checked-out repository snapshot/source identity**, or access to the exact committed Git revision plus the latest ratified docs. The authoritative specs are the actual committed files, **not excerpts quoted here**.
3. **All four** incremental Package 2 ZIPs **if implementation must continue**. They are not included in this Markdown and are not a completed installable overlay. Include Claude's independent source research v2 and any newer Claude code-review findings relevant to the next work.
4. Claude's own **latest** reviewer handover for its separate conversation if coordinating a new Claude reviewer. Do not use this ChatGPT document as a replacement for Claude's independently maintained reviewer knowledge.

**Do not make the old v0.4 ChatGPT handover a mandatory second input.** Include it only if investigating the October 23 orphan incident or checking historic claims. This v0.5 is explicitly intended to carry forward its durable safety and scientific constraints while removing obsolete incident-specific startup instructions.

**Suggested exact opener for a new ChatGPT session:**

> You are continuing development of `hydra3333/analysing_perceived_randomness_in_reality`. Please fully read `Predictive_Randomness_ChatGPT_Continuation_Handback_v0_5_Package2_Interim.md` plus the current ratified repository documents and the four Package 2 checkpoint ZIPs. Treat v0.4 as historical, not as the current safety-state record. Package 2 offline coding is authorised but the checkpoints are not installed; all live scraping, holdout opening, scientific coordination and termination remain separately gated. Independently verify Git HEAD/working-tree status, runtime safety marker state and source hashes before suggesting source installation or execution. Preserve Claude's independent-review and owner-ratification gates. First report a concise orientation and any genuine baseline discrepancies, then continue the authorised Package 2 work.

## 9. Status ledger — dated, brief, and not stronger than evidence

| Date | Event | Status |
|---|---|---|
| 23 Oct 2026 | ChatGPT handback v0.4 ratified as incident-time recovery document; then-active unresolved marker | Historical; warning is not proof marker is active now |
| 23–24 Oct 2026 | Owner-approved manual orphan clearance and successful ordinary non-destructive fixture reported after handback v0.4 | Past reported outcome; verify current runtime marker on restart |
| 24 Oct 2026 | Multi-game Package 1 final docs owner-ratified and subsequently owner-reported committed/pushed | **RATIFIED**; last supplied Git HEAD `057fd8c...` |
| 24 Oct 2026 | Owner authorised Package 2 coding (NOT Package 3 scrape/science) | **AUTHORISED — coding only** |
| 24 Oct 2026 | Four Package 2 engineering checkpoints created, owner placed archives under `Review` and pushed; latest v0.5 has 61+13 Linux offline PASS | **CHECKPOINT**, not reviewed/installed |
| 24 Oct 2026 | Claude source research v2 superseded v1; Lotterywest common official source strategy accepted | **DECIDED for implementation**, no live scrape |
| 24 Oct 2026 | Owner requested a refreshed handover because earlier one was out of date | This **interim v0.5**, no new scientific or process authorisation |

**End of interim ChatGPT handover v0.5.** This document itself does not issue an approval, install source, execute tests or alter Git. All scientifically or safety-consequential changes still require the previously agreed Claude/owner gates.
