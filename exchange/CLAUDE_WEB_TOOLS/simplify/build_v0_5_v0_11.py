import re, hashlib
R='/home/claude/analysing_perceived_randomness_in_reality/exchange/CLAUDE_WEB_TOOLS/simplify/'
def pat(t): return r'\s+'.join(re.escape(w) for w in t.split())
def rep(s, old, new):
    m=list(re.finditer(pat(old), s)); assert len(m)==1, ('rep', len(m), old[:60])
    return s[:m[0].start()]+new+s[m[0].end():]
def between(s, start, end, new):
    m=list(re.finditer(pat(start), s)); assert len(m)==1, ('start', len(m), start[:60])
    e=re.compile(pat(end)).search(s, m[0].end()); assert e, ('end', end[:60])
    return s[:m[0].start()]+new+s[e.end():]

# =========================== SPECIFICATION v0.4 -> v0.5
s=open(R+'SYSTEM_SPECIFICATION_DRAFT_v0_4.md').read()
s=rep(s,"# Predictive Randomness - specification of the active research system - DRAFT v0.4","# Predictive Randomness - specification of the active research system - DRAFT v0.5")
s=rep(s,"End of the specification, DRAFT v0.4.","End of the specification, DRAFT v0.5.")
s=between(s,"**Status:** DRAFT v0.4 for independent review","(decision log entry 137). Fable (High).",
r"""**Status:** DRAFT v0.5 for independent review (EX_268). It is DRAFT v0.4 corrected for EX_267 (R6-F01 to R6-F07, N01 to N06)
and the project owner's decisions in decision log entries 139 to 143. `SPEC_v0_4_TO_v0_5.diff` is exact: sections 7A,
12.4 (in part), 12.8 and 17.4 are new or rewritten; the other changes are the counted ones the diff shows. Not
ratified. It authorises nothing. Until the project owner ratifies it, every ratified document stands and nothing is
coded, moved, installed, run, migrated or deleted.
**Written:** 22 November 2026, by the Claude web chat (primary designer and coder), on the project owner's go of 00:14
(decision log entry 143). Fable (High).""")
s=rep(s,"**Companion:** the deployment design DRAFT v0.10","**Companion:** the deployment design DRAFT v0.11")
s=rep(s,"Shared system code is updated by a separate command, with a marker of its own.",
"Shared system code is updated by a separate command, with a marker of its own. **A\n   fault in shared code is corrected in place by a third command, after which every variant it can affect is\n   computed again** (owner; 12.8).")
s=between(s,"**Three things, and only these, change what an installed variant folder holds:**","a restore from backup (section 14).",
r"""**Three things, and only
these, change what an installed variant folder holds:** the status file, as 3.5 says; the QA software replacement
from PROD, in QA only (12.7); and a restore from backup (section 14). **One command only may overwrite a helper: the
correction of a defect (12.8).**""")
s=between(s,"**3.3A No in-place update of a helper (owner, entry 127).**","belongs in the infrastructure (12.4).",
r"""**3.3A A helper changes in exactly two ways, and the owner says which (owner, entries 127, 143).**
- **A changed idea** (a different calculation is wanted): a new file (`..._v2.py`) and a **successor variant** for each
  variant that is to use it. The old variants stay installed and running, beside the new, until the owner himself
  withdraws any of them (section 11); nothing withdraws them for him. `Who_Uses.bat` and `Make_Successors.bat` do the
  typing (section 4).
- **A defect** (the helper does not compute what was always intended): the helper is corrected in place by the
  correction command, and every variant that uses it is computed again over its whole history (12.8). The names
  stay; their fingerprints change, because the fingerprint covers the helper (3.4).
No ordinary install ever overwrites a helper.""")
s=between(s,"**The research job only ever appends to them.**","research data with PROD's (14.2).",
r"""**The research job only ever appends to them.** Lines leave a
list in exactly two ways, each only on the owner's own command with a confirmation: a historical walk-forward rerun,
which first saves the old lines in a verified archive (section 7A), and a research-data reseeding, which replaces a
QA or DEV tree's research data with PROD's (14.2).""")
s=rep(s,"Each file begins with a `HEADER`: game, family, variant and the variant's fingerprint;",
"Each file begins with a `HEADER`: game, family, variant, the variant's fingerprint, and the identity\nof the shared forecasting code the list was begun under (12.4);")
s=between(s,"**5.6A A list that does not belong to this tree's software or status","the header is the whole of the mechanism.",
r"""**5.6A A list that does not belong to this tree's software or status (owner, entry 129: "warn about them, ignore them
and continue").** A list is **foreign** when its variant is not installed here; or its header's fingerprint is not the
installed variant's; or its header's forecasting-code identity is not that of the forecasting code installed here;
or it breaks invariant 5 against this tree's status file. This arises after a research-data reseeding, a QA software
replacement, or a correction of shared code (12.8). A foreign list is named in a warning at every job, is never
appended to, and counts in no report and in neither OV-1. If the variant is installed here it is **held**: the job
computes nothing for it in that game until the owner clears the foreign list by one of three things: a rerun for
that variant (7A; the foreign list is archived and the variant is computed with this tree's own software), a
research-data reseeding, or in QA the software replacement. Nothing is moved, merged or repaired by itself, and
there is no import folder or second registry: the header is the whole of the mechanism.
**"Ignore and continue" never means a score computed without a member it should have (EX_267 N02).** A held variant
that belongs to the prevailing cohort blocks the prevailing line (10.4); and because the stored reports and OV-1
records were built with the list that is now foreign, the game's derived results are marked not current from that
variant's first draw (5.8) until the owner settles it.""")
s=between(s,"**5.8 The derived results are checked in full, because that is cheap.**","its cost is unmeasured (section 20).",
r"""**5.8 The derived results are checked in full, and what is not current is made to look not current** (EX_267 R6-F02).
- **What is stored evidence and what is only a print-out.** The score lists and the prevailing ledger are stored
  results. The league reports, the next-draw report and the exploratory OV-1 are print-outs: they are never checked,
  because they are made again from the lists whenever anything changes.
- **What the check compares.** At its start the job recomputes, in memory, every score of the game and the whole
  prevailing ledger, with the installed code, from the stored forecasts, the results on file and the status files,
  and compares **the scientific content only**. For a score line: the target, the forecast content's digest, the
  numbers drawn, the TOP and WORST matches for each barrel, and the prize divisions. For a prevailing line: the
  draw, the cohort with each member counted or "no pair", the weights, V, X, Z, and the six log-factors and running
  sums. **Not compared, because they rightly differ over time:** the version and hash of the results file quoted when
  the line was written, any code digest, the rerun's name, where and when it was computed. Those are checked only
  for being well formed. So a results file that has since grown, or scoring code rewritten without changing an
  answer, raises nothing.
- **If the content differs from some draw X on** (the scoring or OV-1 code was changed; the data came from a tree with
  other software or status; variants were added, removed or held), the game's derived results are **not current from
  X**. The job then: writes one small file, `results/research/<GAME>/NOT_CURRENT_FROM.json`, holding X and the reason;
  **moves every report file for a draw at or after X, and both OV-1 print-outs, out of the active reports folder into
  `reports/not_current/`,** so that nothing left in the active folder is stale; makes the exploratory OV-1 and the
  league reports again only up to the draw before X; writes no score, prevailing line or report at X or beyond; and
  alters no stored line. Forecasts go on, so the next draw is never lost. Every program that writes or reads a
  report honours that one file. The job says which draw, and names the command that settles it: the derived-only
  rerun (7A), which removes the file when it has finished.
- Nothing recomputes stored results by itself. The check is exhaustive, not a sample. Its cost is unmeasured
  (section 20); if it proves too slow to run at every job, it runs at every install and copy instead, which sets the
  same file.""")
s=between(s,"## 7A. The historical walk-forward rerun (owner, entries 128, 135, 136, 137)","and the prevailing report thereafter says which draws were computed again and where the first lines are.",
r"""## 7A. The historical walk-forward rerun (owner, entries 128, 135, 136, 137, 143; EX_267 R6-F03)

**7A.1 What it is.** The owner's command to compute again draws that are already computed, in the one tree he runs it
in: to try a corrected or changed method or infrastructure in QA or DEV, to rebuild derived results after a
correction, to recompute the variants a corrected shared file affects (12.8), or, in PROD, as a last resort. It is
the same walk-forward as every other run: same engine, same N-1 rule, same status files. It is never started by an
install, a correction, a copy, a job or a schedule.

**7A.2 The command and its two modes.**

    Rerun_Walk_Forward.bat --game <POWERBALL|OZLOTTO|BOTH> [--from J] [--to N] [--only <family>/<variant> ...]
    Rerun_Walk_Forward.bat --game <POWERBALL|OZLOTTO|BOTH> [--from J] --derived-only

Without `--from`, the whole history. **What each mode may change, and nothing else:**

| | Forecast rerun | Derived-only rerun |
|---|---|---|
| Purpose | forecasts are computed again | scores and OV-1 are computed again from the forecasts as they stand |
| A method runs | yes | **never** |
| Forecast lists | of the selected variants only (all, without `--only`): lines from J on are replaced | **not one byte of any forecast list changes;** every forecast keeps its first-written line and envelope |
| Score lists | of the selected variants: lines from J on are replaced | of every variant: lines from J on are replaced |
| The prevailing ledger | lines from J on are replaced | lines from J on are replaced |
| Reports and the exploratory OV-1 | made again from J on | made again from J on |
| Status files | **never touched** | **never touched** |
| Foreign lists | one within the selection is archived, removed, and its variant computed afresh; others stay foreign | untouched; they stay foreign and their variants held |
| `--only`, `--to` | allowed | **refused:** it is cheap, so it always covers the whole game to the last draw on file |

- **`--only` still rebuilds everything that depends on those variants:** the league reports of the game, the
  exploratory OV-1 and the prevailing ledger from the earliest affected draw, for all variants.
- **`--to N`** stops the recomputation after draw N. **Said plainly before the confirmation:** "everything from J on is
  archived; draws J to N are computed now; draws after N are left for the next `Run_Research.bat`, which will compute
  them as an ordinary catch-up. Until then this game's results are not current from draw N+1." The cutoff file of
  5.8 is left saying N+1, so nothing after N looks current; the next job's catch-up removes it.

**7A.3 Everything that depends on the recomputed draws is rebuilt, always** (owner, entry 135). No report or OV-1 line
computed from the old lines is left standing as if complete. The status files are never touched: withdrawals and
eligibility draws are the same after a rerun as before it, so the cohort at every draw is the same, and a rerun is
never a way to bring a withdrawn variant back or to give a variant a new eligibility draw.

**7A.4 Before anything is replaced, it is saved in one verified, clearly named ZIP (owner, entry 142).** The rerun
first writes, into `results/research_set_aside/`, one ordinary ZIP of every file it is about to change, whole:

    <ROLE>_<GAME>_<RERUN|CORRECTION>_ARCHIVE_<YYYYMMDD>_<HHMMSS>_<what>_BEFORE_RECOMPUTE.zip
    for example  PROD_POWERBALL_CORRECTION_ARCHIVE_20270105_194200_recurrence_gaps_v1_BEFORE_RECOMPUTE.zip

It holds the forecast and score lists the mode will change (a derived-only rerun archives the score lists, not the
forecast lists it leaves alone), the prevailing ledger, the reports and OV-1 print-outs of the game, and a readable
`ARCHIVE_CONTENTS.txt`: the tree, the game, the variants, each file's path and SHA-256, the command and scope the owner
confirmed, his stated reason, and the identities of the software before and after. It is read back and every member
checked against that list. **If it cannot be written or does not verify, the rerun stops and no active file has been
touched.** It says in its own first line that it is not a backup of the tree and cannot restore one. Nothing in the
system reads it again; it travels in every backup; nothing prunes it. In QA and DEV the owner may delete such ZIPs by
hand. **A forecast first made before its result was known keeps that property, in the archive;** it is the line
computed in its place that is retrospective.

**7A.5 The steps.** (1) The process checks; the job lock, held to the end. (2) The scope is shown: the mode; exactly
which lists will be replaced and which will not; what will be rebuilt; 7A.2's sentence where `--to` is used; and, in
a forecast rerun, how many forecasts first made before their results were known will be replaced. (3) **One
confirmation: the owner types the tree's role** (`QA`, `DEV` or `PROD`); anything else is no. In PROD the text first
says: "This is PROD. Lines written when their results were unknown will be replaced by lines computed now, with the
results known. The first-written lines are kept in the archive ZIP named below and in your existing backups. This
cannot be undone except by a restore from backup." (4) A barrier file holding the scope; while it exists every
launcher of the tree refuses, except this command with the same scope. (5) The archive of 7A.4, written and
verified; its name and SHA-256 are then written into the barrier file. **A rerun that is continued never makes the
archive again:** it finds the name in the barrier, checks that ZIP still verifies, and goes on, so records already
shortened are never archived in place of the first-written ones. (6) The cutoff file of 5.8 is set to J. Then the lists the mode may change are each rewritten to end
before J, the prevailing ledger likewise, and the reports from J on are removed. (7) The ordinary fill computes what
is now missing (no method, in a derived-only rerun), to N or to the last draw on file; then the prevailing lines
and the reports, draw by draw. (8) The cutoff file is removed, or moved to N+1 where `--to` was used; the barrier is
removed; the end-of-job backup is attempted. **Interrupted at any point:** the barrier keeps every job out and the
cutoff file says nothing from J on is current; the same command again continues: the archive is verified and
recorded before step 6 and is reused, step 6 does nothing where already done, and step 7 computes only what is
missing.

**7A.6 The truth about what a rerun produces** (owner, entry 136; the reviewer, entries 137, 142). Every line a rerun
writes carries, in its envelope, that its result was on file when it was computed, and the rerun's name. So, in
every tree, a rerun's results are retrospective and are shown as that: the league report's column of forecasts made
before the result was known falls accordingly, and the prevailing report says how many of its draws were computed
again, when, and in which archive the first-written lines are (10.6). Nothing else about OV-1 changes: the same
mathematics, the same conditional claim, the same words in every tree.

**7A.7 Examples.**
- *A corrected OV-1 in QA (derived-only).* QA mirrors PROD. The owner installs corrected OV-1 code into QA with
  `Reinstall_Infra.bat QA`, having been told it changes OV-1 lines from draw 1612. QA's results are not current from
  1612. `Rerun_Walk_Forward.bat --game POWERBALL --from 1612 --derived-only`: the score lists, the ledger and the
  reports go into the archive; scores and ledger are rebuilt from the stored forecasts; **every forecast line,
  including those first made before their results, is byte for byte as it was.** He compares QA's new figures with
  the archived ones and with PROD's. Nothing in PROD has changed.
- *A draw range across a withdrawal.* V1 is withdrawn from 1601. `--from 1550 --to 1650`: V1 is recomputed for 1550 to
  1600 and for nothing after; every other variant for 1550 to 1650; reports and both OV-1 records for 1550 to 1650
  are rebuilt with V1 absent from 1601 on; the game is not current from 1651 until the next ordinary job.
- *One variant after a reseeding.* QA holds its own experimental `E_002/RECUR_MEAN_ALL_V1` (other bytes than PROD's
  variant of that name). After a reseeding, PROD's list for that name is foreign and the variant is held.
  `--only E_002/RECUR_MEAN_ALL_V1`: PROD's list is archived; QA's variant is computed over its whole history; every
  report and both OV-1 records of the game are rebuilt with it; no other variant's forecast list changes.
- *PROD, the last resort.* A scoring fault is corrected, proved in QA as in the first example, and installed into
  PROD. The owner runs the derived-only rerun in PROD, types `PROD`, and the prevailing report thereafter says which
  draws were computed again and in which archive the first lines are.""")
s=rep(s,"with each rerun's date and its set-aside folder;","with each rerun's date and its archive ZIP;")
s=rep(s,"The owner types one confirmation. It then rewrites that",
"The owner types one confirmation. **From before the draw is shown until the status file is written, the\n  command holds the tree's job lock and the updater's own lock,** so that no job and no results step can run in\n  between; under those locks it reads the last draw on file again and refuses if it is no longer the one it showed\n  (EX_267 R6-F07). It then rewrites that")
s=between(s,"5. **The derived results, in full** (5.8): every score and the whole prevailing ledger, recomputed and compared.","just before only if that backup was in fact made and verified** (R5-F04).",
r"""5. **The derived results, in full** (5.8): every score and the whole prevailing ledger, recomputed and compared by
   their scientific content. **An unexpected difference is a fault and stops the install.** There is one expected
   case, and it is not this check failing: an infrastructure reinstall that the owner accepted after being told,
   before anything was overwritten, that it changes derived results from draw X (12.4). There the tool reports the
   difference as what was accepted, and checks instead that the tree now shows those results as not current from X
   (5.8). It never reports "all stored values agree" when they do not (EX_267 R6-F06).
A failure stops the install with its barrier in place, so no job runs. The ways out are the same command after the
cause is corrected, or a restore from a verified backup of the owner's choosing. **The tool names the backup it took
just before only if that backup was in fact made and verified** (R5-F04).""")
s=rep(s,"So a wrong class is caught by a test, not\n  trusted.",
"So a wrong class is caught by a test, not\n  trusted. **A class is a careful label, not a proof** (EX_267 N01): a file whose effect on forecasts cannot be ruled out\n  is classed `forecast`, and a planted dependency from an `other` file into the forecasting path must fail the test.\n- **The identity of the forecasting code** is one SHA-256 over the `forecast`-class files, computed as a variant's\n  fingerprint is (3.4). Every list's header records it (5.2). So a list always says which shared forecasting code\n  it was made under, and a list made under other code than is installed is foreign (5.6A).")
s=between(s,"- **What it checks before it overwrites anything** (R5-F05;","it is never required.",
r"""- **It never changes forecasting code** (EX_267 R6-F01). A plan that would add, overwrite or remove any `forecast`-class
  file is refused by this command, which says: "this changes code that makes forecasts; that is a correction of
  shared code: `Correct_Shared_Code.bat`" (12.8).
- **What it checks before it overwrites anything** (R5-F05; there is no recomputation of the whole history). On a
  temporary copy of the software as it would be, with the target's Python and the target's own data, read only:
  the suite; the derived results **in full** (12.3, 5); and the fixed sample of forecasts (12.3, 4). The result is
  shown as one of two plain statements:
  - "No stored result changes." (Nothing differed.)
  - "**This changes stored scores or OV-1 lines,** for <game> from draw X. It is a scientific correction to derived
    results. Stored forecasts are not affected. If you install it, <game>'s scores, reports and prevailing line will
    be not current from draw X until you run the derived-only rerun." (Exhaustive: every such change is found.)
  **A difference in the forecast sample here is a fault,** since no forecasting code is in the plan: a file is
  wrongly classed. The reinstall stops and names the forecasts that differ.
- **A correction to scoring, reports or OV-1 is installable, plainly stated, and is never hidden as maintenance**
  (EX_267 R6-F01 case A, R6-F06). The owner sees the second statement before the question and may say yes. Stored
  forecasts are untouched; the derived results are not current from X (5.8) until he runs the derived-only rerun
  (7A). Nothing is recomputed by the install. Trying it in QA first costs PROD nothing, and is what QA is for; it
  is never required.""")
s=rep(s,"NO changes nothing. YES proceeds, whatever the backup's result:",
"NO overwrites nothing; the backup and the kit just attempted may by then exist, and are logged (EX_267 N03). YES\n  proceeds, whatever the backup's result:")
s=rep(s,"## 13. The Python environment",
r"""**12.8 Correcting defective shared code in place (owner, entries 141 to 143; EX_267 R6-F01).**
`Correct_Shared_Code.bat PROD` (or `QA`) `--reason "<the defect>"`, run from DEV, on the owner's own command.
- **What it is for:** shared code that does not compute what was always intended. **Shared code** is: the
  `forecast`-class infrastructure files (12.4); a helper under `_shared/`; a helper in a family folder. It is never
  for a variant's own files (a corrected method is a new variant) and never for a changed idea (3.3A). Which of the
  two a change is, is the owner's judgement, given in one line of reason; nothing else is asked of him.
- **What it changes in the target:** exactly the shared files that differ between DEV and the target: `forecast`-class
  files as the infrastructure marker lists them, and helpers the target holds with other bytes than DEV's. DEV's
  markers must match (the variants that use a corrected helper are marked again in DEV, since their fingerprints
  have changed). Nothing under a variant folder is written, and no status file.
- **Which variants it affects, taken widely** (the reviewer, entry 142): for a helper, every installed variant whose
  declaration lists it (3.4: a variant's list is its whole dependency, so this is a look-up, not an analysis); for a
  `forecast`-class file, every installed variant, in both games. The plan shows them by name. The fixed sample of
  forecasts is shown as information only: a sample that happens to match excuses no variant.
- **Its own question, never the install question:** after the plan, the kit and the backup attempt (reported as
  always), the text says: "This is a CORRECTION OF SHARED CODE in <role> <root>: <reason>. These <n> variants will be
  HELD: nothing of them will be forecast, scored or counted until you run the historical walk-forward rerun for
  them, over their whole history. <game>'s results will be not current from draw <first> until then. Forecasts
  already made stay exactly as they are until that rerun archives them. Type CORRECT <role> to proceed." Anything
  else is no.
- **How the hold comes about, with nothing new:** the corrected helper changes the fingerprint of each variant that
  lists it, and corrected forecasting code changes the forecasting-code identity; either way the affected variants'
  lists no longer match their headers, so they are foreign and their variants held (5.6A), in every later job,
  until the rerun. The tool writes the cutoff file of 5.8 at the affected variants' earliest first draw. **No list
  made under the old code is ever appended to under the new:** one name is one forecaster in the active record.
- **The code being replaced is kept** (the reviewer, entry 144). Before any file is overwritten, the old bytes of every
  file in the plan are saved in one small verified ZIP beside the reruns' archives
  (`<ROLE>_CORRECTED_CODE_<date>_<time>_BEFORE_CORRECTION.zip`, with the reason and each file's SHA-256). If it cannot
  be written or does not verify, nothing is overwritten. The rerun's own archive, made later, holds the old results;
  this one holds the old code that made them.
- **Then the owner runs the rerun** (7A), for those variants or for all, when he chooses: it archives what it replaces
  (7A.4) and computes the affected variants' whole history; unaffected variants' forecasts are kept as they are;
  every report and both OV-1 records of the game are rebuilt. The correction never starts the rerun itself.
- **What it never does:** change a status file (withdrawals and eligibility draws stand; a correction is not a way to
  bring back a withdrawn variant or to give anything a new eligibility draw); touch a list; run in PROD without
  `PROD` typed in its question; or run half-way: it uses the install barrier, so that a tree with some files
  corrected and others not is never runnable. The same command again finishes it.
- **In DEV** nothing is installed: editing a helper or a forecasting file there has the same effect by the same rule
  (the lists made under the old bytes become foreign), and the rerun clears it.
The steps are in the deployment design (section 6C).

## 13. The Python environment""")
s=rep(s,"- **PROD is read, never written:** not a log, lock, marker or any byte; nothing of PROD's is started.",
"- **PROD is read, never written:** no program of this project writes a log, lock, marker or any byte there, and nothing\n  of PROD's is started. **Every file read from PROD, each variant's status file included, is hashed at a first\n  reading and again at a second;** any difference, a status file changed by a withdrawal among them, refuses the\n  replacement (EX_267 R6-F04). Those hashes are kept in the tool's memory and in QA, never in PROD. (Windows may\n  itself record a file's last-access time when it is read; that is the operating system's, and is outside this\n  promise: section 20.)\n- **QA is reserved first:** the tool takes QA's job lock before it reads PROD and holds it to the end, so that no QA\n  job can start in between (EX_267 R6-F05).")
s=rep(s,"No PROD program is started. With no lock allowed,",
"No PROD program is started. (The promise is that no program of this project writes to PROD;\n  Windows may itself record a last-access time when a file is read: section 20.) With no lock allowed,")
s=rep(s,"- **Never a half-copied mixture:**",
"- **The destination is reserved first:** the tool takes the destination's job lock before it reads PROD and holds it\n  until it has finished, so that no job can start there and have its data removed under it (EX_267 R6-F05).\n- **Never a half-copied mixture:**")
s=rep(s,"reports, set-aside folders, records,","reports, the archives that reruns have set aside, records,")
s=rep(s,"records, logs, locks, set-aside folders or backups.","records, logs, locks, set-aside archives or backups.")
s=rep(s,"a rerun sets the old lines aside in the tree first, in every tree alike.",
"a rerun first saves the old lines in a verified archive ZIP in the tree, in every tree alike, and does nothing if\nthat archive cannot be made.")
s=rep(s,"Installed software is removed in exactly one case, the QA software replacement, and only in QA.",
"Installed software is removed in exactly one case, the QA software\nreplacement, and only in QA. A helper is overwritten in exactly one case, the correction of a defect (12.8).")
s=rep(s,"| DEV | `Reinstall_Infra.bat PROD` (or `QA`) | update infrastructure |",
"| DEV | `Reinstall_Infra.bat PROD` (or `QA`) | update infrastructure that makes no forecast |\n| DEV | `Correct_Shared_Code.bat PROD` (or `QA`) | correct a fault in shared code in place; the affected variants are then held until the rerun |")
s=rep(s,'"derived results withheld from draw X" (the derived-only rerun);',
'"results not current from draw X" (the derived-only rerun; or, after a correction of shared code, the rerun for the\nvariants it names);')
s=between(s,"- The file-by-file starting list for the code rounds is section 10 of the simplification design v0.1,","works from local files (deployment design).",
r"""- **What phase 1 moves** (owner, entry 139; taken from the installed tree, where `src/` is as at commit `cc0ab73`):

| Today | After phase 1 |
|---|---|
| `src/methods/E_002` to `E_019`: each family's `contract.py` and its own modules (for example E_6's `beta_bernoulli.py`), with `variants.py` | the family's shared core file (`core_v1.py`, and its other modules beside it) and one folder per variant holding `method.py` and `VARIANT.json` |
| `src/methods/E_001/*` and `contract_adapters/e_001.py` | the adapter becomes `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py`; E_1's own modules stay where the proof-of-concept suite imports them |
| `_common/recurrence_gaps.py`, `occurrence_counts.py`, `polynomial_fits.py` | `_shared/recurrence_gaps_v1.py`, `occurrence_counts_v1.py`, `polynomial_fits_v1.py` |
| Every `import` of a moved file, in `src/` and in the tests | follows the move; no other line changes |
| `Method_Contract_Runner.py` (its hand-kept table of methods) and `closure.py` (its list of code folders) | the table is built from the folder tree; the folder list follows |

  Phase 1 changes DEV's working files only. Nothing is installed anywhere by it: QA and PROD do not yet exist.
- **Phase 2's starting list** is the table of kept, changed and left-out modules in section 10 of the simplification
  design v0.1, read with this specification: the coordinator and its plumbing are not installed outside DEV; install
  and release records and Git are gone from deployment; the install tools work from local files; and the lists, the
  status file, the job and the tools are as specified here. Its first task is the exact list of what the coordinator
  plumbing imports.

**17.4 The build order: one ratified design, built in four steps, each on its own go (owner, entry 143).**
1. **The folder layout:** phase 1, above.
2. **The research engine, in DEV:** the lists, the job with its fill and catch-up, scoring, the reports, both OV-1
   scores, the status file and withdrawal (sections 3 to 11). This is the experiment itself, running on DEV's data.
3. **Trees, installs, backups and restore:** `Init_Tree`, `Install`, `Reinstall_Infra`, the checks, backups, the recovery
   kit and the restore (12.1 to 12.6, 13, 14.1), then the transition check and PROD's first job. **After this step PROD
   exists and forecasts every week,** and new methods can be added.
4. **The laboratory tools:** the QA software replacement (12.7), the research-data reseeding (14.2), the historical
   walk-forward rerun (7A), the correction of shared code (12.8) and `Check_Forecasts`.
Steps 2 and 3 are built so that step 4 adds to them and does not change them: every list header carries the
fingerprint and the forecasting-code identity from the first day, and the job's checks of 5.6A and 5.8 are in step
2, because step 4's tools rely on them. **Until step 4 is built, a fault found in shared code is not improvised around:** the affected work is stopped
or held (a withdrawal, or no job for that game) until the tools exist, or the owner restores a backup (the reviewer,
entry 144).""")
s=rep(s,"- **(real)** Phase 1's oracle; the transition check.",
r"""- **EX_267's oracles.** *R6-F01:* a ranking change that alters a sampled forecast of V1: `Reinstall_Infra` refuses the
  plan; `Correct_Shared_Code` holds every variant; no list made under the old code is appended to; after the rerun
  every active forecast of V1 carries the new identity and the first-written ones are in the archive, hashed. A
  helper used by V1 and V2 corrected: both held, V3's forecast list byte-identical throughout. A family's core
  corrected: only that family's variants held. A corrected forecasting file whose sample happens to match: every
  variant still held. A correction leaves every status file byte-identical, a withdrawn variant withdrawn and every
  eligibility draw as it was. *R6-F02:* a draw appended to the results file leaves every earlier score "agreeing";
  scoring code rewritten with the same answers agrees; one changed answer is found at its draw; a league CSV naming
  a variant now foreign is moved out of the active folder and the cutoff file names the draw. *R6-F03:* a
  derived-only rerun changes zero bytes of every forecast list and keeps every made-before-the-result envelope;
  `--only V1` rebuilds every game-level report and both OV-1 records; `--to N` leaves nothing after N current;
  `--derived-only` with `--only` or `--to` refuses; a rerun stopped after each step, then run again, gives the same
  bytes; the archive ZIP failing to verify leaves every active file untouched. *R6-F06:* a corrected scorer that
  changes draw X is foretold with X, installs on YES, leaves the tree not current from X, and nothing reports
  agreement. *R6-F07:* a job, and a results step, started between the withdrawal's display and its write: each finds
  the lock held; no score at T after a withdrawal from T; the status file is the old or the new, never between.
- **(real)** Phase 1's oracle; the transition check.""")
s=rep(s,"| - | Backups at installs: attempted, reported, never a condition; a confirmation defaulting to NO | 135, 136 |",
"| - | Backups at installs: attempted, reported, never a condition; a confirmation defaulting to NO | 135, 136 |\n| - | Defective shared code corrected in place, the affected variants then recomputed; replaces 127's no-overwrite rule for defects only | 141, 143 |\n| - | What a rerun replaces is first saved in one verified, clearly named ZIP | 142 |\n| - | The phase 1 file list in this document; one design built in four steps | 139, 143 |")
s=between(s,"**Mechanisms I chose where no decision exists, each with the leaner alternative**","**For the reviewer.**",
r"""**Mechanisms I chose where no decision exists, each with the leaner alternative** (for the reviewer to judge and the
owner to ratify with the rest; none needs an answer before the review):
1. **The job checks the derived results in full at every start** (5.8). Leaner: only at an install or a copy. If it
   proves slow when measured, the alternative stands ready and sets the same cutoff file.
2. **Any change to a `forecast`-class file is a correction of shared code, and holds every variant until a rerun**
   (12.4, 12.8), even a change believed to alter nothing. That is the price of a persistent rule that needs no
   judgement of harmlessness. Leaner in running cost, fuller in machinery: let `Check_Forecasts --all` finding every
   stored forecast unchanged stand in for the rerun. Not designed; it can be added if such changes prove common.
3. **In DEV an edited variant's or helper's old lists are foreign and wait for a rerun** (5.6A), where v0.3 moved them
   aside by itself. One rule in every tree; the cost is one command in DEV after an edit.
4. **The suite is run only where it belongs to the installed infrastructure** (12.3, 3).

**For the reviewer.**""")
s=between(s,"1. Do 5.6, 5.6A and 5.7 close R5-F01 in every path,","Do you object?",
r"""1. Does 12.8, with the header identity of 12.4 and the hold of 5.6A, close R6-F01 with no mixed history and no
   way round it?
2. Is the list of compared fields in 5.8 the right projection, and does moving stale reports out of the active
   folder, with one cutoff file, close R6-F02?
3. Does the table of 7A.2 leave any mode able to change a file it should not, or to leave a dependent result
   standing (R6-F03)?
4. Do 12.7 and 14.2, with the deployment design's 6A and 6B, now close R6-F04 and R6-F05?
5. Is item 2 of the list above acceptable as the persistent rule, at its running cost?""")
s=rep(s,"- Section 1.2 names the binding clauses by section.",
"- **A correction of forecasting code holds every variant until a full rerun,** however small the change. With many or\n  slow methods that is a long computation, unmeasured. It is the owner's choice each time.\n- Step 4 of the build order comes last. A design fault found then in a step-4 tool could reach back into steps 2\n  and 3; the header identities and the two checks are put in step 2 to make that unlikely, not impossible.\n- Section 1.2 names the binding clauses by section.")
s=rep(s,"\nEnd of the specification, DRAFT v0.5.",
"| EX_267 R6-F01 forecast-changing shared code | 12.8; 12.4; 3.3A; 5.2; 5.6A; 18 |\n| R6-F02 what the derived check compares; stale reports | 5.8; 18 |\n| R6-F03 the rerun's modes | 7A.2 (table), 7A.4, 7A.5; 18 |\n| R6-F04 status bytes hashed when PROD is read | 12.7; deployment design 6A |\n| R6-F05 the destination reserved before the copy | 12.7; 14.2; deployment design 6A, 6B |\n| R6-F06 an expected derived difference is not a failed check | 12.3 (5); 12.4 |\n| R6-F07 the withdrawal serialised | 11 |\n| N01 classes are labels; N02 a held member blocks; N03 what NO leaves | 12.4; 5.6A; 12.4 |\n| Entry 139 the phase 1 file list | 17.3 |\n| Entry 142 the archive ZIP | 7A.4 |\n| Entry 143 correction in place; the four-step build order | 12.8; 17.4 |\n\nEnd of the specification, DRAFT v0.5.")
s=rep(s,"the three statements, each produced by a planted change of the right kind;","the two statements, each produced by a planted change of the right kind; a plan holding a `forecast`-class file\n  refused and sent to the correction command;")
s=rep(s,"the set-aside folder holds the first-written lines exactly;","the archive ZIP holds the first-written lines exactly and verifies;")
open(R+'SYSTEM_SPECIFICATION_DRAFT_v0_5.md','w',newline='\n').write(s)

# =========================== DEPLOYMENT v0.10 -> v0.11
d=open(R+'DEPLOYMENT_DESIGN_DRAFT_v0_10.md').read()
d=rep(d,"# Deployment design - DRAFT v0.10 (","# Deployment design - DRAFT v0.11 (")
d=rep(d,"End of the deployment design, DRAFT v0.10.","End of the deployment design, DRAFT v0.11.")
d=between(d,"**Status:** DRAFT v0.10 for independent review","(decision log entry 137). Fable (High).",
r"""**Status:** DRAFT v0.11 for independent review (EX_268). It is DRAFT v0.10 corrected for EX_267 (R6-F01, R6-F04 to R6-F06,
N03) and the project owner's decisions in decision log entries 141 to 143. Sections 6, 6A and 6B are rewritten and 6C
is new; the other changes are the counted ones `DEPLOY_v0_10_TO_v0_11.diff` shows. Not ratified. It authorises
nothing. It is the companion of the system specification DRAFT v0.5 and says how that document's sections 2 to 4
and 12 to 14 are carried out.
**Written:** 22 November 2026, by the Claude web chat (primary designer and coder), on the project owner's go of 00:14
(decision log entry 143). Fable (High).""")
d=rep(d,"what historical walk-forward reruns set aside (specification 7A.4); never read again",
"the verified archive ZIPs reruns write before they replace anything (specification 7A.4)")
d=rep(d,"`Install.bat`, `Reinstall_Infra.bat`, `Init_Tree.bat`, `Check_Tree.bat`, `Replace_QA_Software_From_PROD.bat`,",
"`Install.bat`, `Reinstall_Infra.bat`, `Correct_Shared_Code.bat`, `Init_Tree.bat`, `Check_Tree.bat`,\n`Replace_QA_Software_From_PROD.bat`,")
d=rep(d,"7. the derived results in full: every score and the prevailing ledger, recomputed and compared.",
"7. the derived results in full: every score and the prevailing ledger, recomputed and compared by their scientific\n   content (specification 5.8). An unexpected difference stops; the one expected case is section 6's.")
d=between(d,"## 6. Updating infrastructure: `Reinstall_Infra.bat PROD` (or `QA`)","research-data reseeding from PROD: `Reseed_Research_Data_From_PROD.bat QA` (or `DEV`) (owner; EX_265; entry 135)",
r"""## 6. Updating infrastructure: `Reinstall_Infra.bat PROD` (or `QA`) (EX_264 R5-F04, R5-F05; EX_267 R6-F01, R6-F06; entries 135, 136)

It overwrites files, so it tells the owner what it will change in the science before he answers, and it asks the
question of specification 12.4. **It never changes code that makes forecasts, never recomputes history and never
starts a rerun.**

| Step | What happens |
|---|---|
| 1 | Settings and role checked. The infrastructure marker must match. The plan is the difference between DEV's manifest files and the target's infrastructure: files to add, to overwrite and to remove, each with both hashes and its class; the text differences are shown. No path under a family folder or `_shared\` can be in it. No difference: end. **A plan holding any `forecast`-class file is refused here:** "this changes code that makes forecasts: use `Correct_Shared_Code.bat`" (section 6C) |
| 2 | The process check; the target's job lock is taken and held to the end; no updater lock, orphan marker or other unfinished operation |
| 3 | **What it would change, found before anything is overwritten.** The software as it would be is assembled in a temporary folder. With the target's Python, reading the target's data and writing nothing in the tree: the suite; every score and the whole prevailing ledger recomputed and compared with what is stored, by scientific content (exhaustive); the fixed sample of stored forecasts. Result: "No stored result changes", or "This changes stored scores or OV-1 lines, for <game> from draw X". A difference in the forecast sample is a fault (a file is wrongly classed) and stops here |
| 4 | The recovery kit for the new software state is written; the `PRE_INFRA` backup is attempted. Each result is noted exactly as it is. **No earlier backup is looked for, counted or verified** |
| 5 | **The warning and the one question** (specification 12.4, in full): the plan; step 3's statement; the warning text; "the backup just attempted: <result>"; "the recovery kit: <result>"; "Type YES to proceed. Anything else, Enter included, is NO." NO overwrites nothing; a backup ZIP, a kit and their log lines may by then exist |
| 6 | The barrier, holding the plan and step 3's statement; the updater's own lock; `SNAPSHOT_DUE` |
| 7 | New files: temporary name, hash, rename. Overwritten files are replaced by rename. Removals come after all copies |
| 8 | The whole tree's software against the old list changed by the plan |
| 9 | In place, with the target's Python: the structure; every installed variant's smoke case; the suite. **The derived results:** where step 3 said nothing changes, the full comparison is run again and must agree; where step 3 foretold a change from draw X and the owner accepted it, the tool writes the cutoff file for X and moves the stale reports out (specification 5.8), and checks that this was done. It does not report agreement that does not exist |
| 10 | `INSTALLED_FILES.json`; the log line; the updater's lock released; the barrier removed, last |
| 11 | The `POST_INFRA` backup is attempted and its result reported. If a change from draw X was accepted, the tool ends by naming the command the owner now owes that game: `Rerun_Walk_Forward.bat --game <game> --from <X> --derived-only` |

- **If step 9 fails** the barrier stays and no job runs. The ways out, said as they are: correct the cause in DEV, mark
  the infrastructure again, and run `Reinstall_Infra.bat <role> --replace-unfinished`, which shows the unfinished plan
  and the new one and asks the same question; or a manual restore of the whole tree from a backup the owner chooses.
  **`PRE_INFRA` is named as a way back only if step 4 made and verified it.**
- Backups are named `PRE_INFRA` and `POST_INFRA`.

## 6A. The QA software replacement from PROD: `Replace_QA_Software_From_PROD.bat` (owner, entries 135, 136; EX_267 R6-F04, R6-F05)

Run from DEV. The destination is QA and nothing else. What it is for and what it leaves alone: specification 12.7.

| Step | What happens |
|---|---|
| 1 | Settings checked (section 1). QA's own file says `role = QA` and PROD's own says `role = PROD`; the two roots and DEV's are three different folders. Anything else refuses: there is no option to name another destination |
| 2 | **QA is reserved:** the process check for QA; no orphan marker or unfinished operation; **QA's job lock is taken now and held to the last step,** so no QA job can start while PROD is read or QA is changed |
| 3 | **PROD is read, and found still (first reading).** No control file in PROD's `records\`; no Python process of the PROD tree in the process table. PROD's `INSTALLED_FILES.json` is read; every scientific and infrastructure file it lists is hashed and must equal the list; **every status file is read, must pass its own check, and is hashed;** nothing unexpected under PROD's `src\`. These hashes, status files included, are the first inventory; it is kept in the tool's memory and in QA, never in PROD. A PROD that does not match its own list is not copied |
| 4 | The plan, shown: what leaves QA; what arrives; "each variant's status file arrives as PROD holds it: <the withdrawals and eligibility draws>"; and "QA's research data is not touched. After this, <n> of QA's lists will not match the software and will be ignored until you reseed QA's research data from PROD or rerun those variants" (worked out from the list headers) |
| 5 | The recovery kit for the software state QA will have; the `PRE_REPLACE` backup of QA is attempted. Each result noted exactly as it is |
| 6 | **The warning and the one question:** "This REMOVES the software installed in QA <root> and puts PROD's in its place. QA's settings, Python environment and research data are kept." Then the backup's and the kit's results and the same YES-or-NO rule as section 5 |
| 7 | The barrier in QA (`records\INSTALL_IN_PROGRESS.json`), naming this operation and PROD's software fingerprint; `SNAPSHOT_DUE` |
| 8 | Every file of the first inventory is copied into `src.incoming\` and `launchers.incoming\` inside QA's root: temporary name, **the bytes written hashed against the first inventory.** PROD's files are opened for reading only |
| 9 | **PROD is read again (second reading):** the same control-file and process check, the list, and **every file's hash, every status file's included,** against the first inventory. Any difference (a withdrawal made in PROD meanwhile is one): the incoming folders are removed, QA's software is as it was, and the tool refuses ("PROD changed while it was being read") |
| 10 | The swap: QA's `src\` is renamed to `src.outgoing\`; `src.incoming\` is renamed to `src\`; each root launcher is replaced by rename; `src.outgoing\` is deleted. QA's `ENVIRONMENT.ini`, `.venv\`, `source_data\`, `results\`, `records\` and `scratch\` are never opened for writing by this step |
| 11 | QA's software is read again and must equal the first inventory. QA's own `INSTALLED_FILES.json` is written from QA's bytes; the log line. Nothing of PROD's `records\` was copied |
| 12 | With QA's Python: the structure; every status file's own check; every variant's smoke case. The suite is run only if this software's infrastructure is file for file DEV's. **If any smoke case fails, QA's `ENVIRONMENT_VERIFIED.json` is removed:** the replacement is complete, but every QA launcher refuses until the owner rebuilds QA's environment and runs `Verify_Tree.bat QA` |
| 13 | The barrier removed; the job lock released, last. The `POST_REPLACE` backup is attempted. The tool ends by repeating which of QA's lists are now foreign and from which draw QA's results are not current, and the two commands that settle it |

Stopped before step 10: QA's software is untouched; the same command starts again. Stopped during or after step 10:
the barrier keeps every QA launcher out; the same command does the whole replacement again from PROD. A half-replaced
QA is never runnable. **What is promised of PROD is that no program of this project writes to it.** Windows may update
a file's last-access time when it is read; that is not a write by this tool and is not promised away.

## 6B. The research-data reseeding from PROD: `Reseed_Research_Data_From_PROD.bat QA` (or `DEV`) (owner; EX_265; entry 135; EX_267 R6-F05)""")
d=between(d,"| 2 | **PROD is found still, by reading:** as 6A step 2, first sentence.","The barrier removed; `SNAPSHOT_DUE`. The tool reports the counts, the lists that are foreign here, and that the next `Run_Research.bat` will show what is withheld, if anything |",
r"""| 2 | **The destination is reserved:** its process check; no unfinished operation; **its job lock is taken now and held to the last step,** so that no job can start there while PROD is read and have its data removed under it |
| 3 | **PROD is found still, by reading (first reading):** no control file in PROD's `records\`; no Python process of the PROD tree. Then the inventory of PROD's research data: the accepted-results set in `source_data\` (the results files, their version ledgers, verification records and the updater's own kept copies) and everything under `results\research\`, each path with its size |
| 4 | **The summary and the one question:** what will be removed from the destination (how many lists, reports and ledgers; its last draw on file); what will arrive (the same counts for PROD); "these <n> lists from PROD will be ignored here, because the variant is not installed here, or is installed with other bytes, or was made under other forecasting code: <names>"; "the destination's software, status files, settings and environment are not changed". "This DELETES the research data now in <role> <root>. Type YES to proceed. Anything else, Enter included, is NO." No backup is taken first (owner) |
| 5 | Every inventoried file is copied into `reseed.incoming\` inside the destination's root, hashed as it is read. PROD's files are opened for reading only |
| 6 | **PROD is read again (second reading):** the control-file and process check; the same set of files; every file hashed again and equal. Any difference: `reseed.incoming\` is removed, the destination is unchanged, and the tool refuses |
| 7 | The barrier `records\RESEED_IN_PROGRESS.json` in the destination |
| 8 | The destination's `results\research\` and its accepted-results set are removed; the incoming folders are renamed into their places |
| 9 | The destination's research data is read again and must equal PROD's hashes. The derived check of specification 5.8 is run with the destination's own software, and the cutoff file written if the copied results are not current here. The barrier removed; `SNAPSHOT_DUE`; the job lock released, last. The tool reports the counts, the lists that are foreign here, and from which draw, if any, the results are not current |""")
d=rep(d,"- A set-aside folder (specification 7A.4) is not research data in use: it is neither copied from PROD nor removed\n  from the destination.",
r"""- A rerun's archive ZIP (specification 7A.4) is not research data in use: it is neither copied from PROD nor removed
  from the destination.

## 6C. Correcting defective shared code in place: `Correct_Shared_Code.bat PROD` (or `QA`) (owner, entries 141 to 143; EX_267 R6-F01)

Run from DEV. What it is for, what it never does, and why the affected variants are held: specification 12.8.

| Step | What happens |
|---|---|
| 1 | Settings and role checked. `--reason` is required. DEV's markers must match: the infrastructure marker, and the marker of every variant that lists a corrected helper |
| 2 | The plan: the `forecast`-class infrastructure files that differ between DEV and the target, and the helper files the target holds with other bytes than DEV's, each with both hashes and the text differences. Nothing else can be in it: no `derived` or `other` file (section 6 is for those), nothing under a variant folder, no status file. No difference: end |
| 3 | **The affected variants, taken widely:** for each corrected helper, every installed variant whose declaration lists it; for any `forecast`-class file, every installed variant. Shown by name, with each one's first draw per game. The fixed forecast sample is run on a temporary copy and shown as information; it excuses no variant |
| 4 | The process check; the target's job lock taken and held to the end; no orphan marker or unfinished operation |
| 5 | The recovery kit; the `PRE_CORRECTION` backup is attempted; each result noted exactly as it is |
| 6 | **Its own question** (specification 12.8): the reason; the files; the variants that will be held; from which draw each game's results will be not current; the backup's and the kit's results; "Type CORRECT <role> to proceed." Anything else is no, and nothing is overwritten |
| 7 | The barrier (`records\INSTALL_IN_PROGRESS.json`), naming this operation, the plan and the reason; the updater's own lock; `SNAPSHOT_DUE` |
| 8 | **The old bytes of every file in the plan are first saved** in one verified ZIP in `results\research_set_aside\` (`<ROLE>_CORRECTED_CODE_<date>_<time>_BEFORE_CORRECTION.zip`, with the reason and each file's SHA-256); if that fails, nothing is overwritten and the barrier stays. Then each corrected file: temporary name, hash, rename over the old. No list, no status file and no variant's own file is opened for writing |
| 9 | The whole tree's software against the old list changed by the plan. `INSTALLED_FILES.json` is rewritten with the new hashes, the new fingerprint of every variant that lists a corrected helper, and the new forecasting-code identity |
| 10 | With the target's Python: the structure; the smoke case of every affected variant; the suite (the infrastructure is DEV's only if nothing else differs; otherwise it is not run and the tool says so) |
| 11 | For each game, the cutoff file is written at the earliest first draw among the affected variants, and the reports from that draw on are moved out of the active folder (specification 5.8). The log line, with the reason. The updater's lock released; the barrier removed; the job lock released, last |
| 12 | The `POST_CORRECTION` backup is attempted. The tool ends with the exact command now owed: `Rerun_Walk_Forward.bat --game <...> --only <the affected variants>` (or without `--only` when all are affected), and says that until it is run those variants are held and those results are not current |

- **It never starts the rerun,** and it touches no research record: the old lists stay exactly as they are, foreign,
  until the owner's rerun archives them in its verified ZIP and computes the variants again.
- **Stopped at any step from 7 on:** the barrier keeps every job out, so a tree with some files corrected and others
  not is never run; the same command again finishes it (files already in place with the right hash are skipped).
  The other way out is a manual restore from a backup the owner chooses.
- If step 10 fails, the barrier stays; the cause is corrected in DEV, the markers made again, and the same command
  run with `--replace-unfinished`, which shows both plans and asks its question again.""")
d=rep(d,"| `INSTALLED_FILES.json` and the tree differ, no barrier |",
"| It names a correction of shared code | the correction was interrupted, or its checks failed | finishes it; with `--replace-unfinished`, goes on with a corrected plan after its own question | a manual restore |\n| `INSTALLED_FILES.json` and the tree differ, no barrier |")
d=rep(d,"| `Init_Tree`, `Install`, `Reinstall_Infra`, `Verify_Tree`, and the QA software replacement as it applies to QA |",
"| `Init_Tree`, `Install`, `Reinstall_Infra`, `Correct_Shared_Code`, `Verify_Tree`, and the QA software replacement as it applies to QA |")
d=rep(d,"| The reseeding, as it applies to its destination | no other Python process of the destination tree |",
"| The reseeding, as it applies to its destination | no other Python process of the destination tree; the destination's job lock held from before PROD is read until the end |\n| `Withdraw_Variant` | the tree's job lock and the updater's own lock, held from before the draw is shown until the status file is written |")
d=rep(d,"The old lines from 1550 on go to a set-aside folder;","The old lines from 1550 on go\n   into a verified archive ZIP;")
d=rep(d,"\n## 15. Tests and the rehearsal",
r"""14. **A fault in a shared helper.** `_shared\recurrence_gaps_v1.py` miscounts a gap; V1 and V2 list it, V3 does not. The
   owner corrects the file in DEV, marks V1 and V2 again, and runs `Correct_Shared_Code.bat PROD --reason "gap counted
   from the wrong draw"`. It shows one helper, two variants to be held, POWERBALL not current from draw 1160, and
   asks; he types `CORRECT PROD`. The helper is replaced; V1's and V2's fingerprints change; nothing else does. PROD's
   next job forecasts V3 as usual, names V1 and V2 as held, and writes no score, report or prevailing line. He runs
   `Rerun_Walk_Forward.bat --game BOTH --only <V1> <V2>`, types `PROD`: one ZIP,
   `PROD_POWERBALL_CORRECTION_ARCHIVE_..._BEFORE_RECOMPUTE.zip`, is written and verified; V1 and V2 are computed over
   their whole history; V3's forecast list is byte for byte as it was; every report and both OV-1 records are
   rebuilt. V1's withdrawal, had it had one, and both eligibility draws are exactly as before.
15. **A fault in a family's core.** `E_002\core_v1.py` is corrected the same way: only E_002's variants list it, so only
   they are held and recomputed. No new variant names are made.
16. **A fault in the shared forecasting code.** A tie is broken wrongly in the readout, a `forecast`-class file.
   `Reinstall_Infra.bat PROD` refuses the plan and names `Correct_Shared_Code.bat`. That command shows every installed
   variant as affected, though the sample of forecasts happens to show no difference, and asks. Afterwards every
   list in PROD carries the old forecasting-code identity and is foreign; the job computes nothing until the owner
   runs `Rerun_Walk_Forward.bat --game BOTH`. Stopped half-way through the correction, PROD refuses every launcher
   until the same command finishes it.

## 15. Tests and the rehearsal""")
d=rep(d,"**the three statements of an infrastructure reinstall,** each from a planted change;",
"**the two statements of an infrastructure reinstall,** each from a planted change; a plan holding a `forecast`-class file\nrefused and sent to the correction command; an accepted derived change leaving the tree not current, with no report\nof agreement; **the correction of shared code** (examples 14 to 16; a matching sample excusing no variant; no list,\nstatus file or variant file written; stopped at every step and never runnable half-corrected; `--replace-unfinished`);")
d=rep(d,"PROD changed during the copy; a busy destination;",
"PROD changed during the copy; **a PROD status file changed between the two readings of the QA software replacement:\nrefused, QA's software as it was;** a busy destination; **a destination job started while PROD is being read finds the\nlock held and refuses, and no data is removed under a running job;**")
d=rep(d,"**Carried, as reviewed:** complete-tree ZIP backups,",
"**Changed in v0.11 (EX_267):** an infrastructure reinstall can no longer carry a `forecast`-class file; the correction\nof shared code is its own command (6C); the destination of each copy holds its job lock from before PROD is read;\nevery file read from PROD, status files included, is hashed at both readings; an accepted derived change is\nreported as that and never as agreement; \"NO\" is said to overwrite nothing, not to change nothing.\n**Carried, as reviewed:** complete-tree ZIP backups,")
d=rep(d,"one default-NO question; the three statements of an infrastructure reinstall;","one default-NO question; the plain statements of an infrastructure reinstall;")
open(R+'DEPLOYMENT_DESIGN_DRAFT_v0_11.md','w',newline='\n').write(d)
for f in ('SYSTEM_SPECIFICATION_DRAFT_v0_5.md','DEPLOYMENT_DESIGN_DRAFT_v0_11.md'):
    b=open(R+f,'rb').read(); bad=[i for i,c in enumerate(b) if c>127]
    print(f, len(b), 'bytes', 'ASCII' if not bad else 'NONASCII %s'%bad[:3], 'LF' if b'\r' not in b else 'CR')
