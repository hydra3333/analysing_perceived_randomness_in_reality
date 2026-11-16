# Rules after the Q7 change - DRAFT r2

**Status: a draft for the reviewer's view and the project owner's decision. Nothing on this page is in force.**
Written by the Claude web chat on 16 November 2026 at the owner's request (decision log entries 43 to 46).
**r2 replaces r1** (r1 is in Git history at commit `e5272dc`). Changed: rows A6 and B1, the new sections 1A and 2A and
question Q5, after the owner's decisions of 22:51. Nothing else changed.

## 0. In plain English

Both holdouts are sealed. The owner's preference is to treat all draws the same, to need no holdout for future method
development, and to keep rules and admin to the least that safety needs. This page lists every current restriction and
proposes DROP, KEEP or CHANGE for each, with the reason. In short: **drop the rules about seeing draws; keep the rules that
protect the data, the review and the lottery websites.**

## 1. The owner's position (his words are in decision log entries 44 and 45)

1. All draws are treated the same. The AI chats may see draw values and results.
2. Catch-ups after missed weeks are the edge case, and that risk is accepted.
3. No holdout is needed for future method development.
4. A new method causes a re-ranking and a fresh comparison with chance over all draws up to the latest in the dataset; the
   new tables replace the earlier ones as the current view.
5. Anything an AI works out from raw draws in a chat is "suggestive" and is clearly stated as such; it may lead to new methods.

## 1A. The owner's decisions of 16 November 2026, 22:51 (his words; decision log entry 46)

- "I hereby remove the limitation "I can only put files in `exchange\` and the runner's folder" as long as you are always
  careful not to destroy anything - if you must, do good archiving or something."
- "Yes keep runners rules for Claude Code."
- "yes to your proposal for "Runner's two draw rules" as long as it never kills nor interferes with any other data."

## 2. Rule by rule

| # | The rule today | Proposed | Why |
|---|---|---|---|
| A1 | The AI chats never display or compute with an outcome for Powerball 1577 or later, or Oz Lotto 1694 or later (H-1 5.1; H-2 5; Q7) | **DROP** | The holdouts are sealed. Every forward forecast is frozen before its draw exists. Results on already-known draws are development or catch-up evidence by rule |
| A2 | The AI chats never open `source_data`, `results` or `transitory_data` (H-1 5.1; Q7) | **DROP for reading** | As A1. Writing stays closed (A6) |
| A3 | "No raw draws, masters, grabs, backups or score ledgers enter either AI chat" (EX_198, EX_199) | **DROP**, if the reviewer agrees for its own chat | As A1 |
| A4 | The AIs never contact a lottery website, search for results or automate one; the owner's updater is the only source | **KEEP** | Safety and the websites' terms. Nothing to do with holdouts |
| A5 | Evidence comes only from the reviewed programs and their logged runs | **KEEP**, with the owner's addition: what an AI computes in a chat is "suggestive", is said to be so, and may seed a new method through the normal route | Keeps the count of looks at the data honest |
| A6 | Claude writes only under `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`. Code, documents and data change only through packages the owner installs after review | **REMOVED BY THE OWNER (22:51)**, on his condition: nothing destroyed; archive if something must go. **How Claude will use it is section 2A**, offered for the reviewer's view and the owner's correction | r1 proposed KEEP for safety. Section 2A keeps the two protections that care alone cannot replace: the Windows test run and review for code, and no AI writes to the data |
| A7 | No install, real-data run, results update, weekly session or dependency change without the owner's go | **KEEP** | The owner's control |
| A8 | A STOP is a STOP; the orphan marker; the three switches False and the allowlist empty | **KEEP** | Operating safety; unrelated |
| A9 | The sealed Mode H studies are not reopened, rescored or edited | **KEEP** | They are the record of the one blind test |
| A10 | Evidence labels (development, Mode H, catch-up, prospective), kept apart | **KEEP as automatic labels** (the programs write them; no admin). **Design question for MHUP-B:** add one all-history descriptive table (every draw to the latest, every current method) beside them | Only results frozen before their draw can confirm anything; an all-history table is a fair descriptive view |
| A11 | The holdout exposure record; HX-2 flags on Powerball 1587 and 1588 | **CLOSE** the record with one line in register v0.31. **Design question for MHUP-B:** drop the HX-2 flag | Catch-up evidence is already labelled retrospective |
| A12 | D5: the updated masters, ledgers and reports stay uncommitted | **The owner commits them** (named paths) once this is decided | It is what lets the AI chats read them: Claude's copy holds only what is on GitHub |
| A13 | The report tool refuses any window beyond 1576 or 1693 (R3 17.3.6 and the code) | **CHANGE in MHUP-B** (code and the R3 edition) | The "missing code" |
| B1 | The local runner's rulebook, rule 4 (never display an outcome from 1577 or 1694 on) and rule 5 (never read the data folders) | **AGREED BY THE OWNER (22:51): drop or reword inside MHUP-B's rulebook edition**, on his condition that the runner "never kills nor interferes with any other data": the reworded rule says read-only, and the rulebook's write limit (its section 3) stays | No safety issue in reading. Meanwhile nothing the runner does needs a draw value |
| B2 | The rest of the runner's rulebook: task files only; never launches an experiment, the updater or a weekly session; no web; no `pip`; writes only in its own folder; never pushes | **KEEP** | **Safety.** The runner sits on the owner's PC beside the real data and can run commands |

## 2A. How Claude will use the wider write permission (Claude's own working rule)

1. **Documents** (`doc/`, `review/`, the roadmap and reminders, `README.md`): Claude may commit a document directly once it
   has been reviewed and the owner has ratified its SHA-256. The owner then only pulls. This replaces his copy-and-verify
   install steps for documents; review and ratification are unchanged.
2. **Code and tests** (`src/`, `tests/`, the `.bat` launchers, `requirements.txt`): the route is unchanged: a reviewed
   package, a rehearsal on the owner's Windows PC, the owner's install. Claude does not push code directly. What protects
   the project here is the reviewer and the test run on the machine that runs the code, and care does not replace either.
3. **Data and records** (`source_data/`, `results/`, `transitory_data/`): never written by Claude. Only the owner's programs
   on his PC write them. A push there could also collide with his uncommitted local files.
4. **Never touched:** `.claude/settings.json`, `.git` settings, the venv, `GAIS/` (the owner's side project).
5. **Nothing is deleted or overwritten.** A superseded file is moved to its `superseded/` or `archive/` folder in the same
   commit. Named-path commits only, each listed in the decision log.
6. Claude does not use the wider permission before the owner has seen the reviewer's reply to this draft.

## 3. What changes where (no separate document round)

- **On the owner's confirmation, after the reviewer's view:** one decision-log entry puts A1 to A3 into force for the chats.
- **The close-out, already due:** register v0.31 and H-1 v4 carry the new wording; the reviewer decides on H-2.
- **MHUP-B:** A10's table, A11's flag, A13 and B1.

## 4. Questions for the reviewer

- **Q1.** A1 to A3: agree, agree with conditions, or keep Q7?
- **Q2.** A10: is one all-history descriptive table acceptable beside the labelled tiers, provided it is never presented as
  confirmatory?
- **Q3.** A11: close the exposure record in register v0.31, and take the HX-2 flag to the MHUP-B design as a question?
- **Q4.** B1: is it acceptable to leave the runner's rules 4 and 5 as they are until MHUP-B's rulebook edition?
- **Q5 (new in r2).** A6 and section 2A: the owner has removed Claude's write limit. Is section 2A a sound way to use it,
  and would you add or change any condition?

End of draft r2.
