import re
R='/home/claude/analysing_perceived_randomness_in_reality/exchange/CLAUDE_WEB_TOOLS/simplify/'
def pat(t): return r'\s+'.join(re.escape(w) for w in t.split())
def rep(s, old, new):
    m=list(re.finditer(pat(old), s)); assert len(m)==1, ('rep', len(m), old[:70])
    return s[:m[0].start()]+new+s[m[0].end():]
def between(s, start, end, new):
    m=list(re.finditer(pat(start), s)); assert len(m)==1, ('start', len(m), start[:70])
    e=re.compile(pat(end)).search(s, m[0].end()); assert e, ('end', end[:70])
    return s[:m[0].start()]+new+s[e.end():]
s=open(R+'SYSTEM_SPECIFICATION_DRAFT_v0_5.md').read()
s=rep(s,"research system - DRAFT v0.5","research system - DRAFT v0.6")
s=rep(s,"End of the specification, DRAFT v0.5.","End of the specification, DRAFT v0.6.")
s=between(s,"**Status:** DRAFT v0.5 for independent review","(decision log entry 143). Fable (High).",
r"""**Status:** DRAFT v0.6 for independent review (EX_270). It is DRAFT v0.5 with the four focused corrections and the notes of
EX_269 (R7-F01 to R7-F04, R7-N01 to R7-N03): counted changes only, in sections 5.8, 7A.2, 7A.4, 7A.5, 9, 12.4, 12.7,
14.2, 18 and 21. `SPEC_v0_5_TO_v0_6.diff` is exact. Nothing else is changed and no new mechanism is added. Not
ratified. It authorises nothing. Until the project owner ratifies it, every ratified document stands and nothing is
coded, moved, installed, run, migrated or deleted.
**Written:** 22 November 2026, by the Claude web chat (primary designer and coder), on the project owner's request of
12:56 (decision log entry 145).""")
s=rep(s,"**Companion:** the deployment design DRAFT v0.11","**Companion:** the deployment design DRAFT v0.12")
s=rep(s,"writes one small file, `results/research/<GAME>/NOT_CURRENT_FROM.json`, holding X and the reason;",
"writes one small file, `results/research/<GAME>/NOT_CURRENT_FROM.json`, holding X and one of two reasons\n  (`MISMATCH`, here; or `AWAITING_CATCH_UP`, below);")
s=rep(s,"- Nothing recomputes stored results by itself. The check is exhaustive, not a sample.",
r"""- **The two reasons are treated differently** (EX_269 R7-F01). `MISMATCH` means stored results disagree with the installed
  code, or a list is foreign: nothing is written at X or beyond until the owner's rerun. `AWAITING_CATCH_UP` is
  written only by a rerun that the owner stopped at draw N (7A.2): the results before X = N+1 are right and those
  from X on are simply not computed yet. Then the ordinary job compares only the draws before X, and **goes on to
  catch up from X in draw order exactly as for newly arrived draws:** forecasts, scores, prevailing lines, reports.
  When every draw to the last on file is done it runs the full comparison once more and removes the file only if
  that finds nothing. If something does stand in the way (a held variant in the cohort, say), the file stays, its
  reason becomes `MISMATCH` at the draw concerned, and the job says so: a catch-up never clears a real mismatch.
- Nothing recomputes stored results by itself. The check is exhaustive, not a sample.""")
s=rep(s,"The cutoff file of 5.8 is left saying N+1, so nothing after N looks current; the next job's catch-up removes it.",
"The cutoff file of\n  5.8 is left saying N+1 with the reason `AWAITING_CATCH_UP`, so nothing after N looks current; the next ordinary job\n  catches up from N+1 and removes the file when everything to the last draw is complete and agrees (5.8).")
s=rep(s,"first writes, into `results/research_set_aside/`, one ordinary ZIP of every file it is about to change, whole:",
"first writes, into `results/research_set_aside/`, one ordinary ZIP **for each game it covers** (a rerun of both games\nwrites two, so neither game can look absent), of every file of that game it is about to change, whole:")
s=rep(s,"its name and SHA-256 are then written into the barrier file.",
"its name and SHA-256 are then written into the barrier file,\nwith the stage `ARCHIVED`.")
s=rep(s,"and the reports from J on are removed. (7)",
"and the reports from J on are removed; when all of that is done the barrier's stage becomes\n`SHORTENED`. **Step 6 is carried out only while the stage is `ARCHIVED`** (EX_269 R7-F03): shortening a list that already\nends before J changes nothing, and nothing is computed until the stage is `SHORTENED`, so a crash inside step 6 is\nrepaired by doing it again; once the stage is `SHORTENED` no list is ever shortened again. (7)")
s=rep(s,"the archive is verified and recorded before step 6 and is reused, step 6 does nothing where already done, and step 7 computes only what is missing.",
"the archive is verified and\nrecorded before step 6 and is reused; step 6 is never repeated once its stage is recorded, so lines already\ncomputed again are never cut a second time; and step 7 computes only what is missing. The barrier is removed only\nwhen every dependent result agrees and the cutoff file is in its final state.")
s=rep(s,"otherwise a job adds only the new draw's files.",
"otherwise a job adds only the new\n  draw's files. **They are also all made again whenever the code that makes them is changed** (12.4), so that no file\n  made by old report code is left in the active folder (EX_269 R7-F02).")
s=rep(s,"and a list made under other code than is installed is foreign (5.6A).",
"and a list made under other code than is installed is foreign (5.6A). **It identifies this project's source\n  code and nothing more** (EX_269 R7-N03): it proves no numerical equivalence across a changed Python or library,\n  which the environment digest in each line and W-23 cover (section 13).")
s=rep(s,"- **`Check_Forecasts.bat`** recomputes stored forecasts",
"- **The print-outs are made again when their code changes** (EX_269 R7-F02). If the plan holds any `derived`-class\n  file and the stored results agree, the reinstall ends by making every league report, next-draw report and OV-1\n  print-out of both games again with the new code, before it removes its barrier. If the results do not agree, the\n  cutoff file and the move of stale reports (5.8) do the same duty until the derived-only rerun.\n- **`Check_Forecasts.bat`** recomputes stored forecasts")
s=between(s,"- **No research data is copied or changed.**","a reseeding, or a rerun.",
r"""- **No list or ledger is copied or changed.** QA's lists and ledgers stay as they were. **Before the tool finishes, and
  before its barrier is removed, it applies the ordinary rules itself with the software now installed** (EX_269
  R7-F02): it names the lists that are now foreign (5.6A); it runs the derived check (5.8); and where QA's results
  are no longer current it writes the cutoff file and moves the stale report files out of the active folder. So QA
  never comes back from this command with a report in view that the installed software and status would not have
  produced. The tool says this before the confirmation, and names the two things that settle it: a reseeding, or a
  rerun.""")
s=rep(s,"derived results the local code would not have computed are withheld (5.8).",
"derived results the local code would not have computed are\n  not current (5.8). **The tool applies both before it finishes:** the cutoff file is written and stale report files\n  are moved out before its barrier is removed.")
s=rep(s,"no command overwrites an installed helper;","no command but `Correct_Shared_Code` overwrites an installed helper, and that one only on its own question;")
s=rep(s,"- **(real)** Phase 1's oracle; the transition check.",
r"""- **EX_269's oracles.** *R7-F01:* results on file through 1700; a rerun `--from 1550 --to 1650`: nothing after 1650 is
  current; one ordinary job then gives the scientific content of a rerun without `--to`, and the cutoff file goes
  only then; the same with `--only V1` while V2 is held: the hold is not cleared and the file stays, as `MISMATCH`.
  *R7-F02:* a changed report formatter that alters no score: no old-format file remains in the active folder when
  the reinstall returns; PROD's V1 withdrawn from 1601 and QA holding reports beyond 1600: when the QA software
  replacement returns, before any job, no invalid report is in QA's active folder and the cutoff file is there.
  *R7-F03:* a rerun crashed after the archive, after some lists were shortened, after all were, and after J+3 was
  computed again, then crashed once more during recovery: the first ZIP is unchanged and verifies, no recomputed
  line is cut again, and the final content equals an uninterrupted run's. *R7-F04:* in the deployment design.
- **(real)** Phase 1's oracle; the transition check.""")
s=rep(s,"\nEnd of the specification, DRAFT v0.6.",
"| EX_269 R7-F01 a rerun stopped at N and the ordinary catch-up | 5.8; 7A.2 |\n| R7-F02 print-outs after a report-code change; QA after a software replacement | 9; 12.4; 12.7; 14.2 |\n| R7-F03 a continued rerun never shortens twice | 7A.5 |\n| R7-F04 an ordinary install and a job started meanwhile | deployment design 5 |\n| R7-N01, N02, N03 | deployment design 3.4 and section 18 here; 7A.4; 12.4 |\n\nEnd of the specification, DRAFT v0.6.")
open(R+'SYSTEM_SPECIFICATION_DRAFT_v0_6.md','w',newline='\n').write(s)

d=open(R+'DEPLOYMENT_DESIGN_DRAFT_v0_11.md').read()
d=rep(d,"# Deployment design - DRAFT v0.11 (","# Deployment design - DRAFT v0.12 (")
d=rep(d,"End of the deployment design, DRAFT v0.11.","End of the deployment design, DRAFT v0.12.")
d=between(d,"**Status:** DRAFT v0.11 for independent review","(decision log entry 143). Fable (High).",
r"""**Status:** DRAFT v0.12 for independent review (EX_270). It is DRAFT v0.11 with the focused corrections of EX_269 (R7-F02,
R7-F04, R7-N01, R7-N02): counted changes only, in sections 3.4, 5, 6, 6A, 6B, 14, 15 and 16.
`DEPLOY_v0_11_TO_v0_12.diff` is exact. Not ratified. It authorises nothing. It is the companion of the system
specification DRAFT v0.6.
**Written:** 22 November 2026, by the Claude web chat (primary designer and coder), on the project owner's request of
12:56 (decision log entry 145).""")
d=between(d,"**3.4 Helpers are never updated in place (owner).**","(example 7).",
r"""**3.4 Helpers: no install overwrites one; one command corrects a defect (owner, entries 127, 143; EX_269 R7-N01).**
`Install.bat` and `Reinstall_Infra.bat` never overwrite an installed helper. A helper changes in two ways only
(specification 3.3A). **A changed idea:** `Who_Uses.bat` finds the variants that declare the helper; `Make_Successors.bat`
prepares a successor folder for each, pointing at the new file (it refuses an existing name, changes no existing
folder, copies no marker and no status file, and withdraws nothing); the owner reviews, marks the batch, and
installs it in the ordinary way; whether and when he withdraws each old variant is his own separate act (example
7). **A defect:** `Correct_Shared_Code.bat` corrects the helper in place, on its own question, and the variants that
list it are held until the rerun (section 6C; examples 14, 15).""")
d=rep(d,"| 6 | The barrier, holding the plan; the updater's own lock is taken; `SNAPSHOT_DUE` |",
"| 6 | **The target is reserved before anything in it is changed** (EX_269 R7-F04): the target's job lock is taken by an exclusive create, which fails if a job holds it; then a fresh process check under that lock. If a job began while the backup was being made or the owner was deciding, the install refuses here, having copied nothing, and can simply be run again when the tree is quiet; no process is ever ended. Then the barrier, holding the plan; the updater's own lock; `SNAPSHOT_DUE`. The job lock is held until the barrier is removed at step 10 |")
d=rep(d,"It does not report agreement that does not exist |",
"It does not report agreement that does not exist. **If the plan held any `derived`-class file and the results agree, every league report, next-draw report and OV-1 print-out is made again with the new code here,** so that no file made by old report code is left in the active folder (EX_269 R7-F02) |")
d=rep(d,"| 13 | The barrier removed; the job lock released, last. The `POST_REPLACE` backup is attempted. The tool ends by repeating which of QA's lists are now foreign and from which draw QA's results are not current, and the two commands that settle it |",
"| 13 | **QA's research data is checked against the software now installed, before QA is released** (EX_269 R7-F02): the lists that are foreign are found; the derived check of specification 5.8 is run; where QA's results are not current, the cutoff file is written and the stale report files are moved out of the active folder. No list or ledger is altered |\n| 14 | The barrier removed; the job lock released, last. The `POST_REPLACE` backup is attempted. The tool ends by repeating which of QA's lists are now foreign and from which draw QA's results are not current, and the two commands that settle it |")
d=rep(d,"and the cutoff file written if the copied results are not current here.",
"and if the copied results are not current here the cutoff file is written and the stale report files are moved out of the active folder, before the barrier is removed.")
d=rep(d,"`PROD_POWERBALL_CORRECTION_ARCHIVE_..._BEFORE_RECOMPUTE.zip`, is written and verified;",
"for each game (`PROD_POWERBALL_CORRECTION_ARCHIVE_..._BEFORE_RECOMPUTE.zip` and\n   `PROD_OZLOTTO_CORRECTION_ARCHIVE_..._BEFORE_RECOMPUTE.zip`), is written and verified;")
d=rep(d,"the file is replaced; the checks in place;","the file is replaced; the checks in place; every league report and OV-1 print-out is made again with the new\n   code;")
d=rep(d,"QA's next job warns that V1's list (it has scores after 1600) and V3's list are foreign and ignored.",
"Before the command returns, QA's results are marked not current from draw 1601 and the report\n   files from that draw on are moved out of the active folder. QA's next job warns that V1's list (it has scores\n   after 1600) and V3's list are foreign and ignored.")
d=rep(d,"The next ordinary job catches up from 1651.","The\n   next ordinary job catches up from 1651 and removes the cutoff file when everything to the last draw is complete.")
d=rep(d,"jobs of different kinds); the kit's self-check;",
"jobs of different kinds); **an ordinary install with a job started after its first check and before step 6: the lock is refused, no file is\ncopied, a second run on a quiet tree succeeds, and nothing is terminated;** a report-code change leaving no old-format\nfile in the active reports folder; the QA software replacement returning with no stale report in view; the kit's\nself-check;")
d=rep(d,"**Carried, as reviewed:** complete-tree ZIP backups,",
"**Changed in v0.12 (EX_269):** an ordinary install takes the target's job lock, with a fresh process check, before it\nchanges anything; print-outs are made again when report code changes; the QA software replacement marks what is not\ncurrent before it releases QA; section 3.4 names the one command that corrects a helper.\n**Carried, as reviewed:** complete-tree ZIP backups,")
open(R+'DEPLOYMENT_DESIGN_DRAFT_v0_12.md','w',newline='\n').write(d)
for f in ('SYSTEM_SPECIFICATION_DRAFT_v0_6.md','DEPLOYMENT_DESIGN_DRAFT_v0_12.md'):
    b=open(R+f,'rb').read(); print(f, len(b), 'ASCII' if all(c<128 for c in b) else 'NONASCII', 'LF' if b'\r' not in b else 'CR')
