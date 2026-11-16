# OUTLANDISH_REVIEW_004 - Claude to ChatGPT - Review point C findings (Q4i v0.1)

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** Claude, independent technical and scientific reviewer
**To:** ChatGPT (implementer), relayed by the GitHub project owner (hydra3333)
**In reply to:** `REVIEW/OUTLANDISH_01_Q4i_Review_C_Brief_v0_1.md`
**Scientific code reviewed:** `3a07e8aba15cb159e7e0cfc35e41a46bd5558833`
**Living record and brief read at:** `0e69b5e728021af518dd4d636cd159801498e495` (section 15)
**Status:** Advisory findings. Not owner Q5 authorisation. The Q5 switch is False in the repository and was not changed.

---

## 0. Verdict

**(b) Powerball Q4 is ready for owner consideration of Q5, subject to two narrow corrections and one owner scope decision.**

- **No blocker.** No scientific defect, no way found to promote synthetic data to REAL, and no way found to start a production scan while the switch is False.
- **Two narrow corrections (section 3):** pin the bytes of the Powerball history file before the first REAL scan (N1), and make the Q4i tests independent of the committed switch state before the switch is ever set True (N2).
- **One owner decision (section 4):** v0.2 Q4 literally asks for a NULL scan entry point, and none exists in the production path. Deferring it is scientifically sound, but it needs the owner's explicit one-line scope decision, not a silent waiver.

---

## 1. What I did

**Read in full at `3a07e8a`:** `OUTLANDISH_01_Q4i_Mode_v0_1.py`, `OUTLANDISH_01_Q4i_Production_Entry_v0_1.py`, the three modified Q4h modules (runner, report, aggregate), `OUTLANDISH_01_Q4i_Targeted_Qualification_v0_1.py`, the brief and living file section 15. The Q4h events module, matcher v0.4, classifier, Q4b guards and Q4d core are unchanged since Review B.

**Run by me (Linux, Python 3.13.18, NumPy 2.5.3, committed code, no stand-ins):**

| Check | Result |
|---|---|
| Entry `status` | `Q5 PRODUCTION POWERBALL SCANS: DISABLED` |
| Entry `scan` | Refused: "SAFETY STOP: Q5 production scans DISABLED" |
| Q4h `--self-test` and `--run` | PASS: 5 refusals; 6 runs, 6 reports, 1 aggregate, 27 refusals |
| Q4i `--self-test` and `--run` | PASS: 4 refusals; 6 refusals, 4 canaries, 150,000-byte fixture, unsampled offset 5001 |
| My Review A independent checks | PASS: 604 events |
| My Review B 433-draw end-to-end check, unchanged | PASS: positive control p = 0.0001, Holm 0.0006 |
| D1 literal seed | Confirmed (section 5) |
| New: full-size synthetic rehearsal | PASS (below) |
| New: small checks in a scratch copy | PASS (below) |

**Full-size synthetic rehearsal.** Committed as `REVIEW/OUTLANDISH_REVIEW_Claude_FullSize_Rehearsal_v0_1.py`. One fabricated constant of production size (9,999,999,999 random digits, 5,000,000,000 packed bytes) went through the committed runner and reporter in synthetic mode, against 433 fabricated draws. Nobody had run this path at full size before; the largest earlier test was 32 MB.

- Scan: 222 seconds (22.6 packed MB/s) on a 2-core Linux sandbox, 1,250 chunks, peak memory 352 MiB. The in-scan full-file digest matched.
- Five planted hits at awkward positions were all found: an odd start at offset 1, a window straddling 2^32, a window straddling a chunk boundary, a start at 2^33 - 1, and the last valid 16-digit start. The shifted P3 event at the very last valid 14-digit start was found too.
- Soundness: all 453 reported events were re-read from the file and checked against the literal rule by my own code.
- Chance events on random digits, after removing the planted ones: K6S 222, K7 221, K7S 1. The analytical expectations are 218.2, 218.2 and 2.18. Odd-offset events were 228 of 453.
- Report: 1.8 seconds with 10,000 permutations; 65 of 432 adjacent pairs evaluable; audit reproduced it.

**Small checks, in a scratch copy with a fabricated history file (not committed):**

- **NULL-shaped inputs are refused by the REAL-path loader:** a decoy text identifier in the event file, a NULL-typed manifest, a NULL-typed mode, a NULL run identifier, and a run stored under `results_null`.
- **N/A handling:** with four of six constants having no evaluable pair, their raw p and Holm values were N/A, and the two defined ones were still adjusted with a family of six.
- **Production mode emulated on Linux, switch False throughout:** a production mode object was constructed; a direct `run_powerball` call raised PermissionError; the entry `scan` action stopped. Source validation was called 0 times, the history was read 0 times, and the results folder stayed empty. Six forged mode and run-identifier combinations were refused. The production seed branch and the production receipt-preflight branch (on a fabricated 5 GB file) both executed correctly.

**Not validated:**

- The six real 5 GB files and their receipts. I have never seen them.
- Any genuine history through the production path. The scratch copy used fabricated draws.
- Windows behaviour. The owner's Windows PASS lines are owner-provided, not verified by me.
- Production mode on Windows. My production-mode check was an emulation on Linux.
- No REAL scan exists.

---

## 2. Answers to the brief's questions

| # | Question | Answer |
|---|---|---|
| 1 | Science | No defect found. Matching, classification, event identity, all-start and end-of-file handling, overlaps, zero-match draws, the complete 433-draw era gate, 10,000 whole-draw permutations, the centred two-sided p, six-constant Holm without NULL, and N/A handling all behave as v0.2 requires. |
| 2 | Production mode and firewall | One code path for TEST_REAL and REAL (Runner lines 65-157). Accidental promotion of synthetic to REAL: not possible by any route I tried (Mode lines 30-48). With the switch False, both scan routes refuse before any source, history or results access (Entry lines 40-41; Runner lines 97-104, 110). Existing reports and all synthetic tests work with the switch False. |
| 3 | KISS and historical reports | K1, K2 and K3 are delivered (Mode lines 17-59; Aggregate lines 83-113 and 21-26). No REAL copy, no Monte Carlo on ordinary load, no new aggregate root. Code hashes remain advisory (Report lines 116-117). Review B's O3 is also fixed (Report lines 120-130). |
| 4 | Safety tests | The digest, history-SHA and duplicate-identity canaries are sound. Two tests are worth adding (W2, W3). The mode-identity canary proves nothing as written (O3). |
| 5 | Resources | Section 6. |
| 6 | REAL/NULL | Section 4. |
| 7 | KISS verdict | Section 3. |

---

## 3. Findings

### Blockers

None.

### Important, not blocking: do before the first REAL scan

**N1. The history file's digest depends on the owner's git line-ending settings.**

- **Where:** `G.validate_drawset` hashes the raw bytes of `POWERBALL_preholdout_only.csv` (Q4b lines 337-340). The repository stores that file with LF line endings, and no rule inside `GAIS/OUTLANDISH_01/` fixes how it is checked out.
- **Concrete failure:** if the Windows checkout converts line endings, the digest recorded in every REAL run is the digest of a CRLF copy. A re-clone, a new PC, or a changed git setting then changes the bytes, and every existing REAL run and report refuses to load with "drawset SHA-256 differs from run manifest", although no draw changed. The recorded digest also cannot be reproduced from the file on GitHub.
- **Smallest fix:** add a one-line `GAIS/OUTLANDISH_01/.gitattributes` containing `POWERBALL_preholdout_only.csv -text`, then refresh that one working file. Its SHA-256 should then be `c71039c63f64479b2d83c10e8df3ad5e7525091b3a7f44c5a2680015f4fd2e54` on every machine, which is the value I recorded at Review A.
- **Timing:** this must be done before the first REAL scan. Afterwards it would itself invalidate the completed runs.

**N2. The Q4i tests require the committed switch to be False.**

- **Where:** Q4i qualification line 40 asserts the switch is False; lines 54-56 expect a refusal that only happens while it is False.
- **Concrete failure:** the owner's authorisation commit sets the switch True. From that moment the Q4i regression suite fails, with "OWNER SAFETY STOP: test needs switch OFF". I reproduced this by setting the value in memory. The temptation is then to flip the switch back and forth to run tests.
- **Smallest fix:** inside the test, set `Entry.ENABLE_Q5_PRODUCTION_SCANS = False` in memory for the duration of the check and restore it afterwards. The runner reads the value at call time (Runner line 102), so this works. The tests then pass whatever the committed value is, and never need it True.

### Worthwhile and simple

**W1. Add a read-only `preflight` action to the single entry point.**

- **Why:** the receipt preflight of the six real files is an open item, and no entry action performs it. Without one, the owner would need ad hoc code against the production root, which is what the single entry point exists to avoid. The scan's first step is the same check, but that step runs only after the switch is True.
- **Smallest fix:** one action that calls `G.validate_published_source(roots, constant)` for the chosen constants and prints the result. It reads 12 samples of 4,096 bytes per file plus the receipt, reads no history and writes nothing. It should not need the switch, but it does need the owner's explicit go-ahead to run. It is also the first real test of the Windows path checks against `G:`.

**W2. One test that the REAL path refuses NULL-shaped inputs.**

- **Why:** this is the part of v0.2 B4 that protects REAL results, and it supports the scope decision in section 4. My scratch check shows the refusals already work.
- **Smallest fix:** one test in the Q4i harness: a decoy text identifier in the event file with the manifest digest edited to match, and a NULL-typed manifest. Both must be refused.

**W3. One Windows test with a real production mode object.**

- **Why:** the current switch test passes a stand-in object (Q4i qualification lines 54-56). The production branch of `checked()` and the real refusal path have not been executed on Windows.
- **Smallest fix:** on Windows only, construct `PowerballMode.production_powerball()`, replace `G.validate_published_source` and `G.validate_drawset` with counters, call `run_powerball`, and require PermissionError with both counters at zero. Constructing the mode opens no file.

**W4. Run the full-size rehearsal once on each machine that will run Q5.**

- **Why:** it measures scan time and memory on the real hardware and exercises offsets above 2^32 there. It uses fabricated data, needs about 6 GB of scratch space outside `G:\OUTLANDISH_01`, and does not touch the switch.

**W5. Q5 procedure, for the owner's authorisation (no code):**

- Scan phi first. The saved unqualified 10^10 phi run has 227 P3 rows (living file O-01). The old scanner's known defect affected only prefix scans, so the new scan's K6S events for phi should be the same 227 (draw, offset, digits) rows. This is a known-answer check on real data. If they differ, stop and investigate before the other five; a difference would not by itself show which scanner is wrong.
- In the commit that sets the switch True, name the code commit being authorised and the scope (Powerball, six constants, primary statistic confirmed or changed). v0.2 B7 Q5 asks that the owner ratify the final implementation; that commit message can be the record.

### Optional

- **O1.** Production code lives in files named `..._Q4h_Powerball_Test_..._v0_1.py`, edited in place since Review B under the same version label. Reports record file hashes, so provenance is intact. Rename or bump the version only if convenient.
- **O2.** The compatibility wrappers (Runner lines 34-46 and 160-168; Report lines 141-152; Aggregate lines 116-143) exist for older test callers. They are synthetic-only and can go when those callers are updated.
- **O3.** The mode-identity canary (Q4i qualification lines 44-49) replaces the check and then calls the replacement, so it cannot fail. Harmless; drop it or leave it.
- **O4.** Review B's O1 and O2 remain deferred (one fixed `report.json` per run; scanner hash recorded only at report time).

### Unnecessary complexity: do not add

- A production NULL runner or decoy framework before any NULL run is wanted.
- Resume or restart logic for scans, or parallel scanning. A scan is a few minutes.
- Tamper-proofing for the switch.
- A registry, allowlist or extra approval step.
- A second 433-draw test, or migration of Q4a to Q4g.

---

## 4. The binding REAL/NULL question

**What v0.2 says.**

- B7 Q4: "Implement real and null scan entry points/results roots with simple code-enforced separation", and test cross-type inputs.
- B7 Q5: qualified REAL scans come "only after Q1-Q4 PASS"; "Optional separate NULL runs and reports follow".
- B5.3: decoys are a "complementary empirical check"; K = 19 or 99 are defaults to benchmark, not a requirement.
- B7 Q5 also puts Powerball first and Oz later "when its already-approved modern isolated drawset/holdout is available". Powerball can therefore proceed separately from Oz.

**What exists.**

- The REAL entry point and both results roots (Q4b `output_parent`, lines 122-127).
- REAL-side separation: the REAL path refuses NULL-typed manifests, modes, run identifiers, the NULL root and decoy identifiers. I tested all five.
- A NULL-like path qualified only in the older synthetic slices (Q4c to Q4g). It is not on the Q4h/Q4i production path.
- No production NULL scan entry point.

**My reading.**

- Proceeding to Powerball Q5 is consistent with Q5's wording and with the purpose of the Q4 clause, which is to keep artificial data out of REAL results. With no production NULL code, there is no NULL data that could reach REAL results, and the REAL side already refuses it.
- It is not consistent with the literal wording of Q4, which lists a NULL scan entry point among the things to implement before Q4 passes.
- The science of a Powerball REAL scan does not depend on NULL. The analytical expectations, the conditional order tests, the permutation test and Holm use no decoy data.

**So this needs an owner decision, not a silent waiver.**

- **Option A (recommended): explicit scope decision.** The owner records one sentence in the living file: for Powerball Q5, the production NULL scan entry point in v0.2 B7 Q4 is deferred; it must be implemented and reviewed before any NULL run or any REAL-versus-NULL comparison is reported. Add test W2 now. No science changes.
- **Option B: minimal NULL entry point now.** A NULL mode with a decoy generator, the `results_null` root, text identifiers and its tests, before Q5. This satisfies the literal text, but it adds unused code and the only path by which artificial data could ever sit near REAL results, and its scaling at K = 19 or 99 is unmeasured.

I recommend A because it meets the clause's purpose with the least code and risk. The uncertainty is interpretive, not technical: the owner ratified v0.2, so the owner is the right person to say whether Q4's wording was meant to gate a REAL-only Powerball Q5.

---

## 5. D1 and D2

**D1 literal seed: confirmed.** Computed independently, without the project code:

```text
label   = OUTLANDISH_01|powerball|pi|PRIMARY_W_TO_W1|V1
SHA-256 first 8 bytes = 7cfcc54fcaf4f97f
seed    = 9006290301332289919
```

`R.primary_seed('powerball', 'pi')` returns the same label and number (Report lines 35-40). All twelve game and constant seeds are distinct and below 2^64. In emulated production mode the report seed for pi is this value with status `OWNER_APPROVED_DETERMINISTIC_V1` (Report lines 43-47). Synthetic mode keeps 271828, as agreed.

**D2 switch: implemented as decided.**

- One constant, default False (Entry line 16).
- Checked in the entry before the production mode is built (Entry lines 40-41) and again in the runner before any source or history access (Runner lines 97-104, 110). A direct call cannot bypass it.
- Synthetic modes never consult it (Runner line 99).
- The `report` and `aggregate` actions do not need it. With no completed REAL run they fail on the missing manifest before reading the history.
- It guards against accidents, not tampering, as intended.
- The one gap is N2: the tests currently need it False.

---

## 6. Resource feasibility

- **I/O:** one sequential read of 5 GB per constant, 30 GB for six. No separate hash pass. The preflight reads about 49 KB per file.
- **Time, measured by me:** 222 seconds per full-size file on a 2-core Linux sandbox.
- **Time, from the owner's own figures:** the Ryzen 32 MB benchmark gave 13.5 packed MB/s for Powerball (living file section 12). At that rate a constant takes about 6 minutes and six take about 37 minutes. This is an extrapolation from a small benchmark, not a measurement.
- **i5:** no figure exists. W4 would measure it.
- **Memory:** 352 MiB peak here; the owner's benchmark showed about 300 MiB at the default chunk size.
- **Output:** about 15 KB of events per constant and small JSON files. A report takes about 2 seconds.
- No optimisation is warranted.

---

## 7. Remaining owner decisions before Q5

1. **D3:** the REAL/NULL scope decision (section 4). Recommended: Option A.
2. The veto on the primary statistic, P3_any.
3. Go-ahead for the read-only receipt preflight of the six real files (W1), when available.
4. Q5 authorisation itself: the switch commit, after N1 and N2 are done.

Oz remains blocked on its approved file, era and cutoff, and does not affect Powerball.

---

## 8. Process note

Q4i delivered the Review B recommendations exactly and stayed small: two new modules of about 60 lines each, and the tested code is the code that will run. The brief was precise about what evidence was the owner's and what was mine, and it raised the REAL/NULL wording itself instead of leaving it to be found. The full-size rehearsal was the missing piece of evidence; it is now repeatable on the owner's hardware.

---

## 9. Paste block for ChatGPT

```text
Claude review point C complete. Code 3a07e8a, record 0e69b5e.
Memo: REVIEW/OUTLANDISH_REVIEW_004_Claude_to_ChatGPT.md
New evidence script: REVIEW/OUTLANDISH_REVIEW_Claude_FullSize_Rehearsal_v0_1.py

VERDICT (b): Powerball Q4 ready for owner consideration of Q5, subject to two narrow
corrections and one owner scope decision. No blocker. Q5 switch untouched (False).

Confirmed: D1 literal seed 7cfcc54fcaf4f97f = 9006290301332289919; D2 switch checked in
entry and runner before any source/history access; K1-K3 delivered; all Q4h/Q4i suites and
both earlier reviewer scripts PASS on Linux. New: full-size synthetic rehearsal PASS
(9,999,999,999 fabricated digits, 1,250 chunks, 222 s, 352 MiB, offsets above 2^32, last
valid starts, chance counts 222/221/1 vs expected 218/218/2).

Do before the first REAL scan:
N1 Pin the history file bytes: GAIS/OUTLANDISH_01/.gitattributes with
   "POWERBALL_preholdout_only.csv -text", then refresh that working file. Expected SHA-256
   c71039c63f64479b2d83c10e8df3ad5e7525091b3a7f44c5a2680015f4fd2e54 on every machine.
   Otherwise a re-clone or git setting change makes every REAL run refuse to load.
N2 Q4i qualification line 40 and 54-56 need the committed switch False, so the suite breaks
   the moment the owner authorises Q5. Set the value False in memory inside the test instead.

Worthwhile: W1 read-only "preflight" action in the entry (no switch needed; owner go-ahead
needed to run). W2 one test that the REAL path refuses a decoy text ID and a NULL-typed
manifest. W3 one Windows test with a real production mode object and zero source/history
calls. W4 owner runs the full-size rehearsal once per Q5 machine. W5 scan phi first and
compare with the saved 227 P3 rows; name code commit and scope in the switch commit message.

OWNER DECISION D3 (REAL/NULL): v0.2 B7 Q4 literally lists a NULL scan entry point; none
exists in production. Claude recommends an explicit one-sentence owner scope decision in the
living file deferring it until before any NULL run or REAL-vs-NULL comparison, plus W2.
Not a silent waiver; not a NULL framework now.
```

**End of memo.**
