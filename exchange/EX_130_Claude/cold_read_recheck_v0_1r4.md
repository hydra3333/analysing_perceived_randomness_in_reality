# Recheck of revised v0.1r4 against cold_read_v0_1r4.md (Q1-Q18)

Read: the revised `v0_1r4.md` (802 lines; changed hunks found by `diff` against the saved pre-cold-read draft), repository at `3a9f6ac` via `git show` only. No data folders, no web, no outcomes. Line numbers are revised-draft lines. ASCII check of the draft: 0 non-ASCII bytes; no personal name found.

## 1. Q1-Q18

| Q | Verdict | New text (quoted, shortened) |
|---|---|---|
| Q1 roster change after U released | APPLIED | J step 18 "Release **U** (`release-install-lock` ...)" after step 17's release commit; step 16 "it refuses while P exists, before COMMITTED PASS, while any session lock exists, and, for a roster-changing package, while any weekly set is unfinished". Leftover wording: see N2. |
| Q2 repeated checks vs U | APPLIED | "**The install check** (`process_check.py check-no-runs --install <package>`, used at steps 2, 5, 7, 11 and 14) ... no updater lock, except, from step 3 to step 18, exactly U with this package's content". |
| Q3 unnamed U tool | APPLIED | "taken by `process_check.py take-install-lock --package <P>` ... released by `process_check.py release-install-lock --package <P>`"; 6.1 command list; K "`process_check.py` (all its commands)"; PRE verifies `process_check.py`'s SHA-256 for MHUP-A. |
| Q4 Mode H tickets | APPLIED | "no target above `holdout_last` in either game with a ticket in a weekly session's attempts ledger and no freeze line ... (Mode H and WF-1A attempts ledgers are not read ...)"; L-R6 "Mode H tickets present do not refuse". |
| Q5 deadlock | APPLIED | "**if the package changes the roster** (its release record will name entries, or it retires a variant)"; 4.3 "An install that changes no roster ... is not refused on this ground, so a defect that stops a set from finishing can always be fixed by a package". Minor: see N4. |
| Q6 nested launch, `-I` | APPLIED | 4.1 "every launcher also sets `PYTHONDONTWRITEBYTECODE=1` before that probe ... the process tool, which runs with `-I`, is given `-B -X pycache_prefix=<the folder>` directly"; 6.1 command line with `-I -B -X pycache_prefix=...`. Re-tested on CPython 3.13: with `-I -B -X pycache_prefix=<absent>`, a planted `__pycache__` sentinel was not imported and the folder was not created. Placement of (a) needs one more word: see N1. |
| Q7 self-test vs permitted differences | APPLIED | 7 "and the edits the existing self-test needs to agree with the additions (its fixtures `opened_root` and `t_gate`, lines 801-803 and 826-832, gain the two freeze fields of 4.2; `t_update_adds`, lines 851-857, runs its second update with a `MODE_H_SEALED` marker present ...)"; admission now "after which the master's last draw is at least ... `holdout_last`"; L "Existing tests" line fixed. |
| Q8 "delete the lock by hand" message | APPLIED | J "**The updater's refusal message** (lines 662-663) still says 'check, then delete the lock by hand'; during an install that advice must not be followed"; A7 adds the same; the checklist says so. |
| Q9 D3 scope | APPLIED (wording); owner confirmation still needed | J "the WF-1A driver's own records (`Method_Walk_Forward.py plan` and `run` write a plan folder, a search-log row, attempts lines and segment records before any gate call ...) ... each may append a search-log row or write a plan, segment or report file"; step 12 STOP "the file or row stays and is disclosed". See N3. |
| Q10 straddle residual | APPLIED (pending owner confirmation) | Check at step 5 "immediately before the gate copy" and step 7 after it; "**Residual risk, stated for the owner:** ... (ii) a contract run started after step 5's check and finished before step 7's ... could have read a mix of old and new gate modules"; L-I7 "a child straddling step 6 is the stated D3 residual". |
| Q11 step 6/7 STOP under live process | APPLIED | Step 7 "not `CLEAN`: stop; keep E, P, U and the copied files; ... rerun this step (restore only if the owner abandons the install)". |
| Q12 git status lists E and P | APPLIED | 4.2 `.gitignore` lines now include "the two install barriers `src/methods/E_001/IN_DEVELOPMENT.txt` and `src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt`"; J "from step 8 (the overlay) none appears in `git status`; ... no `git status` is read until step 12". |
| Q13 Appendix E X vs U | APPLIED | New row "The updater while the install holds U (Appendix J steps 3-18), any stage", refused in every column; the normal row's X cell "runs (the updater reads no orphan marker and not P)". |
| Q14 section 2 barrier order | APPLIED | Line 71 "while it exists every dispatch-gated run refuses; E and P are placed after the install takes the updater's own lock and removed before it is released". |
| Q15 exact batch lines, exit code | APPLIED, one ambiguity | 4.1 (a)-(d) give every line verbatim; `set "RC=10"`, `goto :finish`. Checked against `Run_Experiment.bat` at `3a9f6ac` (blob `dda9b4f5c3b4`): line 31 is the probe, 32 `if errorlevel 1 goto :prefix_failed`, 41 `"%PY%" -u %*`, 69-72 the `:prefix_failed` block ending in `goto :finish`, 76 `:finish`. All correct. See N1 for (a)'s placement. |
| Q16 admission under the lock; one game | APPLIED | 4.1 "(read under the updater's lock, today's line 599, where refusal (1) is also re-checked)"; "Approval 2 and any retry name one game (`--games G`)". |
| Q17 step 3/14 STOP cells | APPLIED | Step 3 distinguishes "content `INSTALL ...`: an earlier install did not finish" from "Any other content: an update is running or crashed"; steps 15 and 18 have their own failure cells. |
| Q18 stale items | APPLIED | L "gains the L-U1, L-U6 and L-U7 cases"; 7 "and the error text of line 47 renamed"; 4.3 "run after POST PASS and the suite, before staging (Appendix J step 12)"; B.2 B05 "(the install order was revised again for EX_129 B02: see B.3 and Appendix J)". |

## 2. The 16 v0.1r4 Appendix D anchors

All 16 VERIFIED against `3a9f6ac`. Each blob prefix matches `git rev-parse`, and each quoted line matches the stored line (CRLF and indentation stripped):
- `results_master_v0_1.py` `7e3e67ba2061`: 60, 146-149, 657-663, 599, 622-627, 662-663, 686, 801-803, 826-832, 851-857.
- `contract_runner.py` `fa94da83a179`: 24, 125-126.
- `Run_Experiment.bat` `dda9b4f5c3b4`: 31, 32, 69-72.
- `Run_Results_Updater.bat` `1f31084cad2a`: 47.

## 3. Cross-references and tables

- **Appendix J step numbers elsewhere.** All correct for the 19-step table:
  - 4.3: install record step 12, release record step 16, the install check at steps 2 and 16.
  - 7: lock steps 3 and 18.
  - B.2 C05 row: steps 12, 13, 16, 17.
  - B.3: steps 2, 5, 7, 11, 14; L-I6 "step 3 to step 17"; step 7; steps 2 and 16.
  - Appendix E: steps 3-18; steps 2, 5, 7, 11, 14.
  - L-R6: step 16.
  - L-I3: steps 6 to 14; L-I5: P until step 15, U until step 18; L-I6: steps 3 to 17, then 18; L-I7: steps 5, 6, 7.
  - Inside J: step 13's "then steps 14-19" and step 17's "rerun from step 17".
- **Appendix E column count.** Every table row from the header (line 564) to the last row has 8 cells, including the four edited rows (586-589).

## 4. New contradictions or gaps

**N1. WORDING. "(a) before line 31" can be read as before the `:verify_python` label (line 30).**
- `Run_Experiment.bat` line 26 is `goto :verify_python`, so a line placed between 22 and 29 is skipped on the activation path.
- Fix: "(a) immediately after line 30 (`:verify_python`)", or "after line 21". Either keeps the probe covered on both paths.

**N2. WORDING. U is still held when the release record is written, but the text still says "the barriers removed".**
- Where: Terms (line 24), section 2 (line 73), 4.3 (line 164, "after the barriers are removed (Appendix J step 16)"), section 8 (line 328) and B.2 C05.
- Fix: "after E and P are removed (U is released after the release commit)".

**N3. CORRECTION (process). D3's extension is recorded as decided, but you said it is pending the owner's confirmation.**
- Where: work-item card (line 37), section 9 DECIDED (line 360), Appendix J, Appendix K's D3 row and B.3 all present the extension (the WF-1A driver and the seconds-long gate-copy residual) as an owner decision "extended the same day".
- Fix: until the owner confirms, mark the extension as PROPOSED/OPEN in section 9 and the card. Alternatively, get the confirmation before EX_130 goes out. Otherwise the reviewer will read a decision that has not been made, which EX_129 section 5 warns against.

**N4. WORDING. The install check needs to know whether a package "changes the roster", but no source is named.**
- Fix: "read from the package manifest (its release entries and retirements)". This makes step 2's result reproducible.

**N5. WORDING. L-U3 omits the inherited-variable case.**
- 4.1 and B.3 C02 say the import test covers "the variable already set by a parent and the probe run first".
- Appendix L's L-U3 (line 788) does not mention it. Add it there.

**N6. WORDING. The `-X pycache_prefix=...` value is written in batch syntax.**
- 6.1 writes `-X pycache_prefix=%ROOT%transitory_data\no_pycache_ever`. The orchestrator runs the tool with `Popen`, where `%ROOT%` is not expanded, and an interactive install console has no `%ROOT%` either.
- Fix: say the orchestrator passes the absolute path, and give the install instructions' exact command.

**N7. WORDING (minor). How step 12 completes after a stray D3 file is left open.**
- After a STOP for a stray D3 file, "the file or row stays", but step 12 still requires `git status` to show "exactly" the listed paths.
- Fix: say Claude's written fix states how the stray file is committed or listed, so that the rerun of step 12 can pass.

No contradiction found in the four edited Appendix E rows, the 4.1 admission paragraph, 4.2, or section 7.

## 5. EX_129 coverage (revised draft)

| Finding | Verdict | Reason |
|---|---|---|
| B01 | RESOLVED | Admission (3) is decided on the ledger row read under the lock (line 599), placed before line 629, and leaves master and ledger at `v_f` on a STOP. It is retryable, one game per run. The self-test fixture edits are now permitted differences. L-U7(a)-(f) are present. |
| B02 | RESOLVED, conditional on N3 | U stops the old and the new updater from step 3 to step 18 (verified in code). The named install check runs at steps 2, 5, 7, 11 and 14 and expects this package's U. Checks immediately before and after the gate copy close the window except for the stated seconds-long straddle. D3 covers the POC path, the report tool and the WF-1A driver, with residuals stated. Step 7 waits rather than restores. E and P are git-ignored. L-I5, L-I6 and L-I7 are present. This holds only once the owner confirms the extended D3 (N3). |
| C01 | RESOLVED | One rule for both branches. It is enforced by the install check and again by the release tool. U is held through the release commit, so no session can open while the roster changes. Mode H and WF-1A tickets are excluded. A non-roster package can always install, so there is no deadlock. L-R6 covers all of this. N4 is wording. |
| C02 | RESOLVED (Windows checks still depend on the owner's POC-rerun decision) | The prefix plus `-B` holds for direct and nested launches once `PYTHONDONTWRITEBYTECODE=1` is set before the probe. The `-I` process tool gets `-B -X pycache_prefix`. Both were reproduced on CPython. The exact batch lines match the real file, apart from N1's placement word. The `NONE` reference is fixed. |
