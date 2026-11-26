# Back to the research: the owner's reframing of 26 November 2026, and Claude's comment (v0.1)

**Date:** 26 November 2026. **Author:** the Claude web chat, at the owner's request (decision log entry 330).
**For:** the owner; then the ChatGPT reviewer chat, for its own comment.
**Status:** a discussion paper. It is not an EX message, it proposes no wording for ratification, it changes no
ratified file and no code, and it authorises nothing. **Everything is paused** by the owner (entry 330): no
amendment, no slice D, no further work on build step 3 until the three have agreed a scheme. Draw values: none
appear here.

**What came just before:** Claude's paper on how the three trees behave
(`exchange/Claude_Three_Way_Discussion_How_The_Three_Trees_Behave_v0_1_20261126.md`, entry 329). The owner read it,
paused the work and wrote what follows. Its section 4, the table of what each tree does today, is still a true
account of what is built; its questions are overtaken by this wider one.

## Part 1. The owner's words, exactly as he wrote them (26 November 2026, 17:51)

~~~~
I have a perception that this project has got away from me again, complexity-wise.
It is 100% my fault, going with the flow and making some bad decisions.
We have spent an enormous amount of resources on control mechanisms, so much so that we have not been near actual research in a long time.

To reframe this project and try to get right back to core business:

This project is clearly a highly speculative research initiative, it seeks to examine the unusual and detect unusual results.
It has been said already that if something is detected then that is the time we will consider more formal approaches and proof type controls rather than stifling research now with bureaucracy.
What do I mean ? 
Well, for example this type of bureaucracy (and I worked in a very large bureaucracy and know how it stifles real work).
- seeking to overly restrict what can and cannot be done in each environment (DEV QA, PROD)
- restrict what can and cannot be (re)installed and when
- "sealing" of all kinds when we know we can re-run from the known compatible starting draws and produce exactly the same results
- hashing of most kinds as controls for what can and canot be locked or even prevent software from being changed or run at will
- nearly all the controls limiting action
- "smoke tests" (we have DEV and QA in place to prove things)
- that nature of things.

We just want to get onto real research to find if anything warrants formal attention.

So, how could things work with largely-eliminated overheads ?  
Suggestions below for you to consider and maybe flesh out and identify edge cases and then once we agree then propose aligning everything to the new scheme.
Unless you have a different more worksable proposal.

Environments:
(a) DEV where things get developed, modified, tested, (re)deployed from into QA or PROD at will.
- software (infrastructure and methods etc) can be installed into target environment QA
- software (infrastructure and methods etc) can be installed into target environment PROD
- new installation means 
* do a backup
* delete the method(s) or infrastructure from the target and "replace" with the ones being installed from DEV
* do a walk-forward from the known compatible starting draws regenerating files and reports and rankings and OV-1s
- in-place (re)installation means 
* do a backup
* delete the data files associated with the to-be-installed method(s) or infrastructure 
* delete the method(s) or infrastructure from the target and "replace" with the ones being installed from DEV
* do a walk-forward from the known compatible starting draws regenerating files and reports and rankings and OV-1s
- "make installable"  means pop a flag file I_AM_INSTALLABLE or similar into the folder on DEV, content being a hash of the py and related files
* if during the install checks, I_AM_INSTALLABLE has a different hash than the target folder (QS or PROD) then assume it is a valid reinstall
* if no I_AM_INSTALLABLE  file in DEV, it is not a candidate for (re)installation
* for infrastructure something similar could happen (t.b.a.)
- "make retired" or similar means pop a flag file I_AM_RETIRED or similar into the folder on DEV and on QA and on PROD (if those folders exist), content being a hash of the current py and related files
- when running normally eg walk-forwards, catchups etc, if a folder has I_AM_RETIRED flag file, that method no longer runs
- when "make installable" if a folder has I_AM_RETIRED flag file the I_AM_INSTALLABLE hash is updated but the method is not a candidate for installing
(b) QA is an area to verify and to prove deployed software works; it may or may nor be identical to PROD and act file PROD or be ahead of PROD.
- software can be copied back from PROD into QA
- data can be copied back from PROD into QA
- software can be installed from DEV into QA
- it acts like QA
(c) PROD is where the ongoing work happens, it is stable and has backups as previously established (as does each environment using the same mechanism).

Notes: 
1. absolutely everythig everything is CRLF and is guaranteed to produce/write only CRLF (and github conforms)
2. Each environment has a config file something notionally like this or json equivalent:
```
[environment]
; the environment config file is almost identical across environments
; with the role different and which dictates which environment section to use:
role = DEV
; role=QA
; role=PROD

[DEV]
in here goes the DEV folder paths etc etc,  whatever is necessary and unique to an environment, perhaps even a venv path
the same for each environment pointing to the right paths for that environment,
the same keys, the only difference being the specified paths

[QA]
in here goes the QA folder paths etc similar ro DEV

[PROD]
in here goes the PROD folder paths etc similar ro DEV
```
So, the environments all notionally act the same
- doing all the same things
- dev may have extra stuff for doing installs etc

2. So instead of lots of complexity and many controls and hashes and locked/sealed records etc
- we have a few flag files and whatnot and anything else minimum-complexity
- some data/json files controlling (eg starting draw numbers for

Claude first you to for comment in a form somehow also containing and/or referencing the above so that chatgpt can see it.
The to chatgpt for comment.
Thanks.
~~~~

## Part 2. Claude's comment

### 2.1 The short answer

I agree with the direction, and I think the scheme works. It is simpler than what we have built, it matches
how you have described the trees all along, and it rests on a fact that is true of this system: **everything a
tree holds, except a few small things, can be made again from the official results and the software.** Most of
the controls we built protect records that never needed protecting, because they can be recomputed.

Four things in this comment:

1. **Three small things should be kept,** each a few lines of code, because each guards against real damage or
   keeps a later formal test possible (2.3 and 2.4).
2. **One refinement makes your scheme simpler still:** one kind of install, not two (2.5).
3. **The edge cases,** each with the simplest answer I can see (2.7).
4. **The largest overhead has not been the code but the process around it,** and much of that was my doing (2.9).

### 2.2 What the controls were for, and what replaces them

| What we built | What it was for | In your scheme |
|---|---|---|
| Add-only installs; refusal to change forecasting code; the two statements before a reinstall | never to change a stored forecast | replace the software and compute again |
| Hash-chained lists, digests, "not current" markers, the archive before a rerun | to prove a record was not altered | nothing: the record is whatever the software computes now |
| The list of installed files; the verified-environment marker; `Verify_Tree`; the smoke cases | to refuse a tree whose software or Python had changed | nothing: DEV and QA are where things are proved |
| The readiness marker bound to hashes and the suite | to stop an unready variant being installed | your flag file `I_AM_INSTALLABLE` |
| The status file with a withdrawal draw | to stop a defective variant | your flag file `I_AM_RETIRED` |
| The barrier files and the "finish it or replace it" rules for an interrupted install | to recover a half-done install exactly | a backup first; run the install again |
| The process check before every command | to stop two commands colliding | one lock file per tree (2.4) |
| Roles that forbid (updater in PROD only; no verifying in DEV) | caution | the trees act the same |

### 2.3 The one scientific point, and a one-line remedy

"We can re-run from the starting draws and produce exactly the same results" is true, and N-1 stays enforced by
the engine, so a recomputed forecast for a draw never sees that draw. What recomputing cannot tell apart is
this: **a method written or adjusted after its results were visible will look better over those same draws than
it deserves.** That is not cheating; it is what exploration is. It only matters at the moment you describe: when
something looks unusual and deserves formal attention. Then the first question will be "over which draws was this
method's code already fixed?"

That question can be kept answerable for one line of cost: **when a method's code arrives in a tree, or changes
there, the install writes down the last draw that tree held at that moment.** For example: "in place since draw
1602". Every draw after that number is evidence gathered after the code was fixed; every draw up to it is a
walk-forward over history that was already known. Nothing is locked, nothing is refused, and a reinstall simply
writes a new number. It could be one extra line in the tree's own copy of `I_AM_INSTALLABLE`. The two OV-1 scores we
already have map onto it directly: one over all draws, one over the draws after that number.

Two free safeguards already exist and need no code: Git keeps the dated history of every method's source in DEV,
and each backup is dated.

**This is a statistical-validity point, so I ask the reviewer for its own view of it (question R1).**

### 2.4 Three small things I would keep

1. **A tree must be what its settings say it is.** With one settings file of the same form everywhere, the one
   mistake that could damage PROD is a file in the QA folder that says `role = PROD`: QA's job would then write
   into PROD's folders. One comparison prevents it: the path in the role's own section must be the folder the file
   lies in, or the command stops and says so. And the settings file is never copied between trees.
2. **One lock file per tree,** so that a job and an install cannot write the same files at the same moment. If a
   crash leaves it behind, the message says to delete it by hand. No inspection of other processes.
3. **The "in place since draw" number** of 2.3.

Everything else in today's guard would go.

### 2.5 A refinement: one kind of install, and the tree rebuilds what is out of date

You describe two cases (a new install; an in-place reinstall), each ending in a walk-forward from the start.
They can be one, and the cost can be much smaller:

- **Each method's data already records the fingerprint of the software that made it** (it is in the first line of
  its files today). Today a mismatch is refused. In the simple scheme the same comparison would mean **"this
  method's data is out of date: delete it and fill it again from its starting draw".**
- **So an install is only:** a backup; copy the folders whose flag hash differs from the target's; write the
  "since draw" number; run the research job. The job finds what is out of date and rebuilds exactly that, then makes
  the league, the reports and OV-1 again. A new method and a changed method are the same case.
- **Infrastructure** (the engine itself) gets one fingerprint for the whole of it. If it differs from the one the
  data was made with, the job rebuilds everything. No classing of files by what they can change.

**What it costs, from your own PC:** a first fill of both games with all 40 methods took 46 to 47 minutes,
unattended (decision log entries 208 and 260). So an infrastructure change costs about that today, and
more as methods are added. A new or changed method costs only its own share, about a minute or two.

The principle in one sentence: **nothing is refused because of a hash; a difference means "rebuild that part".**

### 2.6 The scheme, fleshed out (for discussion, not a design)

- **In every tree, the same:** `Run_Research` (fetch new results unless `--no-update`; rebuild whatever is out of
  date; catch up; make the league, reports and OV-1 again); a backup; a restore.
- **From DEV:** make installable (write the flag with the hash of the folder's files); install into QA or PROD
  (2.5); retire (write `I_AM_RETIRED` into the folder in every tree that has it).
- **Into QA from PROD:** copy the software; copy the data. Each takes a backup of QA first.
- **Starting draws:** each game's known compatible starting draw and each method's own minimum history are already
  small declared values; they stay as they are.

### 2.7 Edge cases, with the simplest answer I can see

1. **An install stops half-way** (power, a full disk). Run it again: it copies what is still different. If the
   tree is broken, restore the backup it took.
2. **A job stops half-way.** Run it again. A method whose files are incomplete is rebuilt.
3. **The flag is older than the files** (a file edited in DEV after "make installable"). The install recomputes
   the hash; if it is not the flag's, that folder is skipped and named: "make it installable again". This is the
   meaning of the flag, not an extra control.
4. **A method exists in the target but no longer in DEV.** Left alone. Retiring is the way to stop it.
5. **Retired: what happens to its past results?** Two honest choices. (a) They stay in the records and the league,
   marked retired, and it simply makes no new forecasts. (b) They vanish at the next rebuild. I recommend (a) as the
   meaning of "retired", because dropping methods that did badly makes the rest look better than they are
   (question 2). To remove a method entirely, as for a faulty one, delete its folder and rebuild.
6. **A helper file shared by several methods changes.** "The py and related files" must include the helpers a
   method uses, so every method that uses it gets a new hash and is rebuilt.
7. **Python or a package is upgraded.** Numbers can shift in the last decimal places. The job writes the Python
   and package versions into its log; after an upgrade, rebuild everything once. Nothing refuses.
8. **The official results change other than by growing** (a correction at the source). The job says from which
   draw, and everything is rebuilt. Nothing stays refused.
9. **Software copied back from PROD into QA.** QA's data is then out of date for whatever differs, and QA's next
   job rebuilds it. The retired flags and "since draw" numbers come with the folders.
10. **Data copied back from PROD into QA.** QA's data is replaced whole, after a backup. If QA's software differs
    from PROD's, the next job rebuilds what differs.
11. **QA ahead of PROD.** Allowed; nothing depends on it.
12. **DEV.** The same commands. A method runs in DEV with or without the installable flag (it is being worked
    on); a retired one does not run.
13. **Everything CRLF.** Already nearly so: Git converts nothing (`* -text`), and the standard has every text file
    CRLF with one exception, the line-record files (`.jsonl`), which are LF because each line is hashed with its line
    ending (the chains and digests). If those go, the exception goes with them. Two project records are still LF (the
    decision log and the continuity page) and would be converted once. My cloud helper scripts (`.sh`) are not part of
    the system and cannot be CRLF on Linux; I would keep them out of the trees.
14. **The old system's code** (the coordinator, Mode H, the updater v0.2) is not installed in QA or PROD and
    is not used by any of this. The sealed Mode H records are never touched. Your standing rules about them stay
    true without any code of the new scheme having to enforce them.

### 2.8 What stays exactly as it is

N-1 in the engine. Games never pooled. The scoring and OV-1 arithmetic. Lotterywest-GOV as the only source,
through your reviewed updater with all its checks of the source, minus the Mode H remnants (already decided). No
AI chat and no local runner ever contacts a lottery website. No program ends another process. Nothing changes the
PC's date, time or zone. Nothing runs on your PC without your go.

### 2.9 What happens to what is built, and the overhead that is not code

**The code, plainly.** The research engine of build step 2 (about 4,400 lines, installed in DEV) is mostly what the
simple scheme needs: N-1, forecasting, scoring, the league, the reports and OV-1. It would lose its chains, its "not
current" handling and its copy-from-PROD step. Slices A, B and C of build step 3 (about 7,200 lines of code, some of
it the engine's own files changed, and 8,900 lines of tests; passed and not installed) are mostly the controls you
list. The backup and restore of slice B can be kept as it is or cut down to "zip the tree, read it back"; most of
slices A and C would be set aside and replaced by an install script a small fraction of their size. That work is spent
whichever way you decide, so it should not weigh on the decision.

**The process.** The correction rounds of slice C, on 25 and 26 November, went largely on what happens if a research
job finishes during the seconds in which you read a reinstall warning. Two AIs, five EX messages, 36 planted faults. Your
scheme does not need that tool at all. For the exploratory phase I suggest, for the three of us to agree:

- **Review where the science is:** N-1, scoring, OV-1, the mathematics of each new method. The install and copy
  scripts get one reading for a single question: can this destroy data that cannot be made again?
- **No hash tables in messages** (a Git commit names the bytes), no planted-fault campaigns for admin scripts,
  tests in proportion.
- **One short page of the scheme** in place of the 1,250-line specification and the 610-line deployment design,
  with the science sections kept by reference. One ratification.
- **A handover of a few pages,** and a decision log that holds decisions.

### 2.10 Questions

**For the owner:**
1. "(b) QA ... it acts like QA": I read this as "it acts like PROD". Right?
2. Retired: past results stay, marked retired (2.7 item 5, my recommendation), or vanish?
3. One kind of install, with the job rebuilding what is out of date (2.5), in place of your two cases: agreed?
4. An infrastructure change rebuilds everything, about 47 minutes today: acceptable as the one simple rule?
5. Backups: at each install and on demand only, or after every job as well? And is DEV backed up by the same
   mechanism (its tree holds Git and all the documents), or by Git and your own copies as now?
6. Your last note stops mid-sentence: "some data/json files controlling (eg starting draw numbers for". What was
   the rest?
7. The lighter process of 2.9: yes, no, or in part?

**For the reviewer:**
- **R1.** Is one "in place since draw N" number for each method in each tree enough to keep walk-forward evidence
  and after-the-fact evidence apart, should something ever warrant formal attention? If not, what is the least
  that would be?
- **R2.** Does anything in the scoring or in OV-1 depend on the chains or digests, so that it would break without
  them?
- **R3.** Is there any control beyond the three of 2.4 that you would insist on keeping, and what damage does it
  prevent?
- **R4.** Your view of 2.9, since it changes your own role most.

### 2.11 What I am not sure of

- Whether rebuilding one method at a time is as simple inside the engine as I describe. I believe so, because the
  engine already fills a new method's history by itself; I have not traced every case.
- The 46 to 47 minutes is one measurement on your PC with 40 methods; it will grow.
- Whether the reviewer will see a scientific need I have missed in 2.3.

**How this comment was made:** on Fable, by the session's own label. If we agree a scheme, writing it down and
aligning everything to it is a "Suggest switching to Fable (High)" point, and I would hold there for your go.
