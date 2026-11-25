# How the three trees behave: a paper for discussion between the owner, the reviewer and Claude (v0.1)

**Date:** 26 November 2026. **Author:** the Claude web chat, at the owner's request (decision log entry 328).
**Status:** a discussion paper. It is not an EX message, it proposes no wording for ratification, it changes no
ratified file and no code, and it authorises nothing. Slice D is not started and is not to be started before this
is settled. Draw values: none appear here.

## 1. Why this paper exists

On 26 November 2026 the owner asked what "slice D (the updater)" was, and Claude answered from the ratified design
that the updater runs in PROD only and that QA and DEV get their results by a copy from PROD. The owner replied
that this is not how he has described QA. Claude and then the reviewer each first answered with the same wrong idea
(a setting in QA's file that chooses where its results come from), and the owner rejected it. In his words to the
reviewer: "Some of our (all 3 of us) exchanges do not seem to be getting through." This paper sets out, in one
place, what he has said, what the ratified text and the code actually do today, where they differ, and the few
questions that need an answer before anything is redrafted.

## 2. What the owner has said (his words; these govern)

- **21 November 2026 (entry 136, decided):** "One science in every tree. DEV and QA act on their installed software
  and their own `ENVIRONMENT.ini`, exactly as PROD does", with "no extra administration because a tree is QA" (the
  log's record of his direction).
- **25 November 2026 (entry 305):** "DEV and QA and PROD (if they have the same software installed) can act
  identically because they have the same software ... QA should do what PROD does since the purpose of QA is to
  try things in QA before installing them to PROD ... and similar relationship of DEV to QA."
- **26 November 2026 (entry 324):** "one of QA roles QA is meant to prove things as if it were prod, \"it will have
  the same software as prod\" apart from config ini, hence if I copy prod data back to QA I should be able to run
  the updater in QA as if it were prod."
- **26 November 2026 (entry 326), rejecting the results-source setting:** "no, that is 100% incorrect. a research job
  runs in QA with whatever data is in QA, just like prod.  whether the data is put there by a copy-back job or a
  catchup job or whatever is immaterial."
- **26 November 2026 (entry 327):** "The software in QA can and will be identical at times, they should thus act
  identically according to their software." And, correcting Claude: the install tools do write into PROD
  ("apart from INSTALL and related").
- **26 November 2026 (entry 328), on DEV:** the rule "covers DEV too, because DEV runs the same engine code, that is
  correct - if I said or agreed otherwise I was wrong ... DEV needs to develop/test all available functions within
  its tree since that is its purpose, think if it as \"QA plus\" since it can install stuff too and run stuff
  without so many restrictions and checks (it cannot install into itself) although I do not know what has been
  implemented for that to happen."

**Put as one rule:** what a tree does follows from the software in it, not from the tree's name. A research job
works on the accepted results that are in its own tree. How they got there is a separate matter.

## 3. The owner's question (a): which ratified sentence did Claude mean?

Two sentences of the system specification v0.6 (ratified 22 November 2026, RAT-40):

- Section 2: "Two limits are about safety, not science: **only PROD may run the updater,** and PROD is never the
  destination of a copy."
- Section 15, "Safety rules kept": "**Only the one reviewed updater contacts Lotterywest-GOV, only in PROD;** no AI
  chat and no other program contacts any lottery site."

**Where they came from, as the decision log shows.** "The updater in PROD only, with QA and DEV receiving results
by a checked copy" first appears in Claude's own first draft of the specification (entry 125, 21 November, listed
under "also in the design"). It was never one of the choices put to the owner. Choice A, which he did decide
(entry 130), was that the research job runs the updater itself, and Claude worded it "in PROD". His direction of
entry 136 came later the same day, and Claude wrote it into section 2 with those "two limits" attached as an
exception. The reviewer passed the text and the owner ratified the whole document.

**So the plain answer:** the sentence is ratified, but it was Claude's design choice, carried through review; the
owner was never asked to decide it on its own, and it contradicts what he had directed. All three of us read it and
none of us held it against his principle. On 25 November he stated the principle again and Claude applied it to
`Verify_Tree` only.

The owner's own standing rule is narrower and is not in question: the one results source is Lotterywest-GOV,
reached only by his approved tools; no AI chat and no local runner ever contacts a lottery website.

## 4. The owner's question (b): what each tree does today

"Built" below means: **installed** in DEV by build step 2; **passed** means written and reviewed in the cloud
(slices A, B, C of build step 3) and not installed anywhere; **not written** means slice D or build step 4.
There is no QA tree and no PROD tree yet.

| # | What | DEV | QA | PROD | Where it is said | Built |
|---|---|---|---|---|---|---|
| 1 | The results step of the research job | copies results from the tree its settings name; never the website | the same | runs the updater | specification 2, 7.1 | installed (the copy); the updater's launch from the job is not written |
| 2 | The updater's own launcher | not part of the new system in DEV | refuses | runs | deployment design 2, 15 | not written (slice D) |
| 3 | The settings file | may hold `[results] copy_from` | may hold it | must not hold it (refused) | deployment design 1 | installed and passed |
| 4 | Creating a tree (`Init_Tree`) | not a target | first results from PROD, or from DEV while no PROD exists; `copy_from` = PROD is written into its settings | first results from DEV | specification 12.5 | passed |
| 5 | Checks before a job starts | the environment marker and the list of installed files are not asked for | both must be there and match | as QA | deployment design 9 | passed |
| 6 | Which variants run | every variant folder with a valid declaration, finished or not; a folder that fails its checks is passed over | installed variants only; a failing folder refuses the job | as QA | specification 2, 4 | installed |
| 7 | A variant with no status file | one is made, as active | refused | refused | specification 3.5 | installed |
| 8 | `Verify_Tree` | refuses ("nothing to verify": DEV has no marker) | runs | runs | deployment design 7 | passed |
| 9 | Backups, the recovery kit, restore | none by these tools (DEV has no backup root; Git and the owner's own ZIP) | its own backup root | its own backup root | specification 2, 14 | passed |
| 10 | The install tools (`Init_Tree`, `Install`, `Reinstall_Infra`, `Make_Installable`, `Check_Tree`) | run from DEV only; never install into DEV | a target | a target | specification 12 | passed |
| 11 | Copies between trees (the QA software replacement; the research-data reseeding) | reseeding may fill DEV | both may fill QA | read only; never a destination | specification 12.7, 14.2 | not written (build step 4) |
| 12 | Tests, documents, Git, the exchange | here only | none | none | deployment design 2 | as it is |

Everything not in the table is written once and behaves the same in every tree: forecasts, N-1, scoring, the
league and the reports, OV-1, withdrawal, the historical walk-forward rerun, the job lock and the process rule.

**How the project works today, before any of this is installed:** the only tree is DEV, and its accepted results
are the ones the owner fetches there with the old system's updater v0.2. So the new design, as ratified, would
have taken the updater away from the one tree that runs it now.

## 5. What the owner's rule changes, as Claude now reads it (for the three of us to confirm)

**Rows 1 to 4 change. Rows 5 to 12 are not touched by what he has said about the updater.**

- **Row 1:** the job's results step is the same in every tree: it runs the reviewed updater in its own tree, and
  `--no-update` leaves it out. Copying from PROD is no longer a step of any job.
- **Row 2:** one updater, one launcher, the same behaviour in every tree. The "refuses outside PROD" guard planned
  for slice D is not built.
- **Rows 3 and 4:** no tree's settings say where results come from; `Init_Tree` stops writing `copy_from`.
- **The two sentences of section 3** lose "only PROD may run the updater" and "only in PROD". "PROD is never the
  destination of a copy" stays. So does "nothing run for QA or DEV, and no copy of any kind, ever writes a byte
  of PROD" (specification 15); the install tools run for PROD do write into PROD, as the owner says.
- **Copying PROD's data into QA or DEV** becomes only what the owner called it: a separate operation he runs when
  he chooses.

**What does not change:** N-1, scoring and OV-1; Lotterywest-GOV over HTTPS as the only source, through the
owner's reviewed updater with every one of its checks; that no AI chat and no local runner ever runs it or
contacts a lottery website; that QA is never a gate; that the install tools run from DEV.

**What it touches that is already written:** `src/research/results_step.py` and the settings reader (installed in
DEV by build step 2; passed again in slice A); `Init_Tree` (slice C, passed). The ratified text: specification
sections 0, 2, 7.1, 12.5, 15, 18 and 19; deployment design sections 1, 2 and 15; the build plan of step 3,
section 5. It would be an amendment for the owner's ratification (RAT-61) after the reviewer's view.

## 6. The questions that need an answer first

**Q1. How does PROD's data get into QA or DEV, now that the job no longer copies it?**
*Why it matters:* the owner's own example begins "if I copy prod data back to QA".
*What exists:* the research-data reseeding (specification 14.2) makes the destination's research data exactly
PROD's: accepted results, forecasts, scores, reports and OV-1 records, wiped and replaced. It is ratified but
belongs to build step 4 and is not written. The lighter thing, a checked copy of the accepted results alone, is
written and installed today, as the job's results step.
*Options:* (a) the reseeding only; until build step 4, a QA tree gets PROD's results only at its creation.
(b) Also keep the checked copy of results alone, as its own small command, reusing the code that exists.
*Claude's leaning:* (b), because the code is already written and reviewed and the reseeding is some way off; but
(a) is less to own. The owner's call.

**Q2. DEV as "QA plus": which functions must work inside DEV's own tree that do not today?**
*Why it matters:* the owner says DEV "needs to develop/test all available functions within its tree" and does not
know what has been implemented.
*What the table shows:* rows 5, 6 and 7 are DEV running "without so many restrictions and checks", which is what
he describes. Row 1 (the updater) is settled by his rule. **The open part is rows 8 and 9:** `Verify_Tree`, backups
and restore do not operate on the DEV tree at all. As designed, DEV tries those functions on a tree it creates
(QA, or a scratch tree in the joined rehearsal), not on itself.
*Options:* (a) leave rows 8 and 9 as they are: those functions act on an installed tree, and DEV is the source
tree with Git, documents and unfinished work in it. (b) Make them work on DEV's own tree too: DEV would need a
backup root and a verified-environment marker, and "the DEV tree" would have to be defined for a backup (the Git
folder, the documents, the exchange). That reopens slices A, B and C, which have passed.
*Claude's leaning:* (a), for cost and because a restore over the Git clone is a risk of its own. But this is
exactly the kind of reading that went wrong before, so it is asked, not assumed.

**Q3. Three trees, three visits to the website.**
With one behaviour everywhere, a job in DEV, in QA and in PROD each fetch the same draws unless `--no-update` is
given. That is the owner's to accept; Claude proposes no limit and no new control. One useful consequence: the
three results files are fetched independently and should be byte for byte the same, so a difference would be a
finding.

**Q4. For the reviewer:** does anything outside the two documents bind "PROD only" (R-017's own wording, the
register, H-2)? Claude finds no such restriction in the owner's standing rules or in the runner's rulebook, which
forbids the runner the updater in every tree and stays as it is.

**Q5. The order of work.** Claude's proposal: answers to Q1 to Q3; then one narrow amendment drafted (the model
rule applies: Fable), the reviewer's view, the owner's ratification; then slice D written to the amended text,
with the small changes to `results_step.py`, the settings reader and `Init_Tree` carried in the same slice so that
nothing passed is reopened twice.

## 7. How the process went wrong, and one small suggestion

The owner's principles are in the decision log, in his words. But designs and reviews have been checked clause
against clause and against earlier clauses, not against those principles; a clause that was internally consistent
and well tested passed three readers while contradicting him. The suggestion, for discussion and not done: one
short page of the owner's standing principles in his own words (for example "identical software acts identically
in every tree"; "QA is never a gate"; "a job works on what is in its tree"; the main-game principle), which every
design and every review is held against first. It would be a page, not a process.

## 8. Where things stand

Slices A, B and C of build step 3 have passed independent review (EX_321, EX_327, EX_333). Nothing of build step 3
is installed. Slice D is not started. Nothing is authorised on the owner's PC. The record is decision log entries
324 to 328.
