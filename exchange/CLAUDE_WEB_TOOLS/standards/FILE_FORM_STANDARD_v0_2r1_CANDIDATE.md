# The project's standard for the form of its text files (line endings) - v0.2 CANDIDATE (v0.1, RAT-47, with one narrow amendment and two corrections of fact)

**This edition: v0.2 CANDIDATE, 24 November 2026, evening.** It is v0.1 with three passages changed, each marked
"v0.2", all found by Claude while the conversion was being prepared and simulated (decision log entries 242,
245 and 250): **(A) section 5 and section 8 item 7: the root `.gitattributes` holds three lines, not one,** because
the one line does reach `GAIS\`, which v0.1 denied; the owner approved the three lines (decision log entry 251);
**(B) section 4:** how many writes name no line ending, where they are, and which can be corrected; **(C) section
5 and section 11:** the refresh of the owner's working copy and the staging of the converted files are done by a
program, because ordinary Git commands were not reliable for it in the simulated working copy. **The policy is unchanged, and nothing else is changed.**
Built from v0.1's Git bytes by `exchange/CLAUDE_WEB_TOOLS/standards/make_standard_v0_2.py`;
`FILE_FORM_STANDARD_v0_1_TO_v0_2.diff` beside it is the exact difference. **r1 (24 November 2026):** the reviewer's EX_310 passed (A) and (C) and (B)'s corrected count, and asked one
narrow qualification of section 4's wording (FFS2-C01), made here together with its observation on section 5's
wording; `FILE_FORM_STANDARD_v0_2_TO_v0_2r1.diff` is the exact difference from the candidate it read, and
`FILE_FORM_STANDARD_v0_1_TO_v0_2r1.diff` the whole difference from v0.1. **Not ratified; v0.1 stays in force
until the owner ratifies this.**

**Date of v0.1:** 24 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status of v0.1: OWNER-RATIFIED on 24 November 2026
(RAT-47, decision log entry 237),** as a note of ratification to the specification v0.6, beside the coding
practices, after the reviewer's FOCUSED PASS (EX_305) of the exact candidate v0.1r2 (SHA-256
`4f515726bceb31e6d92df422c8b4c0c1e8df349a780430d28bcbf40bd9204f51`), of which this is the installed text. The
owner decided its open points (section 8; decision log entries 231 and 234). **It changes nothing by itself and
authorises nothing on the owner's PC:** the conversion, every install and every run are each his own go. It
replaces the words "LF pinned" of decision log entry 181 and the advice in the specification's section 20 on
pinning line endings in `.gitattributes`. The draft, the candidates, their exact differences, the builders and
the trial's evidence are kept in `exchange/CLAUDE_WEB_TOOLS/standards/`; the exact difference from the ratified
candidate to this text is `exchange/CLAUDE_WEB_TOOLS/rat47/FILE_FORM_STANDARD_v0_1r2_CANDIDATE_TO_FINAL.diff`.
**v0.1r1 (24 November 2026):** the four clarifications of the reviewer's EX_303 are made: FFS-C01 (sections 2,
6 and 7: what is the project's own, what a tree's own untracked files become, the checker's exact scope);
FFS-C02 (sections 3 and 3B: two more kinds, the `.jsonl` wording, what conforming means exactly); FFS-C03
(section 5: `GAIS\`, and commits from the cloud); FFS-C04 (section 7: a second run, locks, a copy first,
what is and is not proved). One point was put to the owner (section 8 item 6); he has decided it. The policy is
unchanged. v0.1
and the trial's evidence stay as they were; `FILE_FORM_STANDARD_v0_1_TO_v0_1r1.diff` is the exact difference.
**v0.1r2 (24 November 2026):** the one narrow correction of the reviewer's EX_304 (which passed FFS-C01, C02 and
C03): v0.1r1 promised that the conversion could be undone from its list alone. That is not generally true and
is removed; the way back is the owner's copy, checked before the conversion begins (section 7). Nothing else
is changed; `FILE_FORM_STANDARD_v0_1r1_TO_v0_1r2.diff` is the exact difference.

**Why it exists (the owner, 24 November 2026, decision log entries 227 to 230).** "git should never be used as an
operational gatekeeper/checker"; "I prefer being consistent if possible"; "we should create a spec ... expressly have
a list of file types and/or data types and exactly which type they use so that there is never any ambiguity";
"everything confirms to the standards ... whatever it takes to get it done (safely)"; "ensure our git settings files
stuff and github settings all do the right thing"; and a "standards" section in the operations manual.

## 1. The rule, in four sentences

1. **Every text file of the living project is in Windows form: each line ends CRLF** (carriage return, line feed),
   whether a person or a program wrote it. One kind of file is the exception, by its nature: the line-record
   files (`.jsonl`, section 3). The retired Mode H release machinery is left out by name (section 3A).
2. **Every program that writes a file says which line ending it writes;** none leaves it to the platform's default.
3. **Git converts nothing in this project's part of the repository** (section 5 says exactly where). What is on
   disk is what is committed, and what GitHub shows is what the tools hash.
4. **The project's own checker says whether the rule is kept,** in the test suite and before anything is marked
   ready to install. Git is never asked.

## 2. What the standard covers, and what it does not

| | What | Rule |
|---|---|---|
| **The living project: the project's own files** | what the project's packages deliver and what the project's programs write, in these places of the repository and of a DEV, QA or PROD tree: the root's own files (launchers, settings, the licence, Git's settings files); `src\`; `deploy\`; `tests\`; the runner's tools; `source_data\`; `results\research\`; `records\`; `scratch\` | section 3, without exception |
| **Frozen history** | what is only read by people and used by no program that runs in DEV, QA or PROD: `exchange\`, `review\`, `archive\`; the documents under `doc\` as ratified; the old system's own records under `results\` (the old run folders, the old reports, the retired Mode H records) | **never converted, never edited.** They are records of what was exchanged, reviewed, ratified or computed, each in the bytes it had. A file Claude adds to these folders after this standard is ratified is written in the standard's form |
| **Not this project's** | `GAIS\` | untouched |
| **Not the project's own** | a tree's `.venv\` (other people's packages: thousands of files in their own forms; the environment's digest and verification of specification 13 govern it, never this standard); `.git\`; Python's cache folders; whatever a test writes in a temporary folder (some tests make malformed files on purpose) | **never converted, never checked by this standard** |
| **Not text, by kind** | `.zip`, `.pdf` and the other kinds section 3 names as binary | no line endings. A file of a text kind is never excused as "binary" because of what it holds (section 3B) |

*Why history is left alone (decided by the owner, section 8 item 1, on his own test: "not actively used in a
DEV/QA/PROD program running sense", "only documents to read"):* recorded hashes all over the decision log and the
exchange messages name those bytes; the reviewer's files are not Claude's to change; no program of the new system
reads them; and the old system's records are the oracle of the transition check, which is best made on untouched
files.

## 3. The list: each kind of file, and its form

"Today" is what Claude found in the repository on 24 November 2026 (Git's own listing; the engine's code).

| Kind of file | Names | Who writes it | Today | **Standard** |
|---|---|---|---|---|
| Python code | `*.py` | Claude's packages; the owner | LF (3 are CRLF on the owner's disk) | **CRLF** |
| Batch files | `*.bat`, `*.cmd` | Claude's packages | CRLF on disk, LF inside Git | **CRLF**, on disk and in Git |
| Settings, manifests, status files | `*.ini` (`ENVIRONMENT.ini`, `INFRA_MANIFEST.ini`, `VARIANT_STATUS.ini`) | the owner; `Init_Tree`; the status writer | LF | **CRLF** |
| JSON documents | `*.json` (a variant's `VARIANT.json`, registries and declarations, the readiness markers, `INSTALLED_FILES.json`, the records under `records\`, the results' verification records in `source_data\`) | Claude's packages; programs | LF | **CRLF** |
| Tables | `*.csv` (results masters and their ledgers; report tables) | the results updater; the report writer | masters and ledgers CRLF; reports LF | **CRLF** |
| Reports, read-me files, logs | `*.txt`, `*.log` | programs | LF | **CRLF** |
| Documents | `*.md` | Claude; the reviewer; the owner | mixed | **CRLF** for every new file |
| Lock and flag files | `JOB.lock`, `SNAPSHOT_DUE`, and the like | programs | LF | **CRLF** |
| Git's own settings files; project text without an extension | `.gitattributes`, `.gitignore`; `LICENSE` | Claude's packages; the owner | LF | **CRLF** (Git reads both files correctly in this form: tried by Claude with Git 2.43) |
| **Line-record files** | `*.jsonl`: every variant's forecast list and score list and the OV-1 ledger (hash-chained), and the logs under `records\` (one record a line; not all of them chained) | programs only; never a person | LF | **LF: the one exception** (below) |
| Shell scripts | `*.sh` | Claude's cloud helpers under `exchange\` | LF | LF: Linux refuses anything else. None is part of the living project |

**The one exception, and why it is not a halfway house.** Every `.jsonl` file of the project is LF, so that one
name has one rule. The reason lies in the lists: a line of a forecast list, a score list or the OV-1 ledger is the
canonical encoding of one record, byte for byte, and that
encoding ends in one LF. The same bytes are what every link of the list's hash chain
and every content digest is computed from, in the shared forecasting code and in the old system's records alike.
The line ending is therefore part of what is hashed, not a matter of presentation. These files are written only by
programs, are never opened to be edited, and display correctly in Notepad on Windows 10 and 11.

**Wherever this standard is summarised, the exception is said with it** (the owner's condition, section 8 item 2):
in the operations manual's "Standards" section, and in what the checker prints.

**Not files, and not changed:** the strings the project hashes in memory (a fingerprint's lines
`<path><TAB><sha256><LF>` of specification 3.4; the canonical encoding itself). They are definitions of a hash, and
stay exactly as the ratified specification gives them.

## 3A. Left out by name: the retired Mode H release machinery (the owner, section 8 item 5)

The old system's Mode H study and the release mechanism built for it are retired. Six of its files are pinned to
their exact bytes by its own tests, and the cloud's trial (section 9) showed that they are the only files whose
conversion changes any test. **They are not converted and not checked by this standard, and stay exactly as they
are:**

- `src/methods/_common/contract_data/install_records/INSTALL_MHUP_A_V1.json`
- `src/methods/_common/contract_data/install_records/RELEASE_BASELINE_20261031_V1.json`
- `src/methods/_common/contract_data/install_records/RELEASE_MHUP_A_V1.json`
- `src/package_tools/process_check.py`
- `src/results_master_v0_2.py` (the present results updater; decision log entry 181: it "stays untouched in DEV";
  build step 3 writes its successor `results_master_v0_3.py`, which conforms)
- `tests/fixtures/results_master_v0_1_reference.py.txt`

Also left exactly as they are, as frozen history: the sealed Mode H records and every other record of the old
system under `results\`, and the two Mode H opening records `source_data\HOLDOUT_OPENED_<GAME>.json`. **The binding
rule that the sealed Mode H records are never altered is untouched.** Every other file of the old system that still
lies in `src\` and `tests\` is ordinary code and conforms like the rest; the trial converted all of it with no test
changing. Whether the retired Mode H code and its tests leave the living project altogether is a later, separate
question.

## 3B. What "conforms" means, exactly (so that every checker gives the same answer)

- **A CRLF file:** every line ending in it is CRLF. It holds no LF that does not follow a CR, and no CR that is
  not followed by an LF. **An LF file (`.jsonl`):** it holds no CR at all.
- **An empty file conforms.** **A last line with no line ending is allowed** and is left as it is: the conversion
  changes line endings and never adds or removes one. (Whether a list's last line is torn is the engine's own
  check, not this standard's.)
- **A file of a text kind must read as UTF-8 and hold no zero byte.** One that does not is REFUSED and named; it is
  never passed over as "binary". Binary kinds are excused by their kind alone: `.zip`, `.pdf`, images (`.png`,
  `.jpg`, `.gif`, `.ico`), and Python's compiled files.
- **A file of a kind this table does not name,** found in a place the checker covers, is REFUSED and named: the
  table is extended by the owner's recorded decision before such a file is accepted. Nothing is assumed.

## 4. Every program says what it writes

Python's ordinary way of writing a text file uses the platform's own line ending: the same program writes CRLF on
the owner's PC and LF in Claude's cloud workspace unless it says otherwise. So:

- **A file is written either in binary, from bytes the code made, or with its line ending named** (`newline=`). No
  write relies on the default.
- **A test reads the code and fails on any write that names none.** (v0.2: v0.1 said here "found today, to be
  corrected: 17 in the old system's code". The test's own search finds eighteen in the project's programs, all
  in old self-tests, and none in the new engine. **Sixteen are in `src/results_master_v0_2.py`, which section 3A
  leaves exactly as it is: they stay,** and the test leaves that file out by name with the other five. Two, in
  `src/two_site_results_check_v0_7.py`, are corrected. The search covers the project's programs and excludes
  tests' own temporary-fixture writes, which section 2 exempts. **Any test that writes an actual in-scope
  project file remains subject to the standard** (r1; EX_310 FFS2-C01). That the tests' outputs are confined to
  disposable fixtures is confirmed in the review of the conversion's package.)
- This becomes one line of the coding practices.

## 5. Git and GitHub: nothing converts

- **The root `.gitattributes` holds three lines** (v0.2; the owner, section 8 item 7):

      * -text
      GAIS/** !text
      GAIS/**/*.bat text eol=crlf

  By the first, Git never changes a line ending of this project's files, in either direction, on any PC,
  whatever its own `core.autocrlf` setting is; the project's earlier special lines are no longer needed. The
  second and the third are for `GAIS\` alone (the next point).
- **`GAIS\` is left exactly as it is, and it takes two lines of the root file to do that** (v0.2; EX_303
  FFS-C03; the owner: section 8 items 6 and 7). That folder is another project's. It has two attribute files of
  its own (`GAIS/OUTLANDISH_01/.gitattributes`, `GAIS/OUTLANDISH_01/OUTLANDISH_WSL/.gitattributes`), which Git obeys
  for the paths they name, and the second tells Git to convert that project's `.py`, `.sh`, `.md` and `.bat`
  files. **v0.1 said that the root line `* -text` "does not reach `GAIS\`". That was wrong.** Those two files
  name only some kinds of file: of GAIS's 204 tracked files (24 November 2026), 173 are named by neither, and
  the root line would have governed them. On a PC whose Git converts line endings their working copies would
  then have differed from Git's bytes, unseen. The line `GAIS/** !text` takes the root file's say about text
  away for everything under `GAIS\`, so that Git does there exactly what it did before this standard (GAIS's
  own two files, and each PC's own settings). The line `GAIS/**/*.bat text eol=crlf` keeps, for GAIS alone, the
  one earlier line of the root file that applied to it. Checked by Claude in a clone made with
  `core.autocrlf=true`: with the three lines every GAIS file's stored form, form on disk and attribute are,
  file by file, what they were. Claude never writes under `GAIS\`. So the true statement is: **Git converts
  nothing anywhere in this project; under `GAIS\` Git does exactly what it did before.** The repository holds
  no other attribute file.
- **`.gitignore`** gains the readiness markers and the marker staging folder (state of one tree, never tracked).
- **GitHub:** a push stores the bytes pushed, and there is no repository setting on GitHub that converts line
  endings; GitHub's own guidance on the subject is about `.gitattributes` and each PC's Git settings. **What
  GitHub's editor in the browser does to a file's line endings Claude could not establish** (a search found clear
  reports for other hosting products, none authoritative for GitHub). So the rule does not depend on it: **no file
  of the living project is edited or created in the browser.** Files reach GitHub by a commit from the owner's
  PC or from Claude's cloud workspace, and either way the commit is checked: the bytes staged for it are in the
  standard's form (Git's own listing of the staged bytes is read for this). That is a check of a commit, which
  is what Git is for; it is never a check of whether a tree may run. If a file ever arrives in the wrong form,
  the project's own checker names it at the next suite run.
- **The owner's working copy needs one refresh,** on the day: with `core.autocrlf=true` Git has, until now, written
  CRLF copies of files it stores as LF (every document he has pulled). **v0.2: v0.1 said that under `* -text`
  those copies "would all show as changed" and that rehearsed commands would refresh them. Neither proved
  reliable.** Where Git finds a file's remembered size and time unchanged it does not read the file again.
  In Claude's simulated working copy (decision log entry 250; r1, worded as EX_310 asked) ordinary commands
  were therefore not reliable for this migration: `git status` showed none of those copies as changed; a plain
  `git add` passed over the converted files it believed unchanged (a second command with another option did
  stage them); and a forced checkout rewrote none of the 2,298 stale working copies. Left so, a later
  `git add` could put a CRLF copy of frozen history into Git. **So
  the refresh and the staging are done by a small program of the conversion's package, by content:** it stages
  each listed file with exactly the bytes it has on disk; it rewrites, with Git's own bytes, the working copy
  of every other tracked file that Git converts nothing for and that differs from Git's bytes in line endings
  only; it refuses a file that differs in more; it proves that what is on disk is what is staged or
  committed; and it commits and pushes nothing. It calls Git, as the check of a commit in the point above
  does: that is what Git is for, and it is never a check of whether a tree may run. It is rehearsed by the
  runner before the day.
- **Claude's own commits:** every text file Claude adds from then on is CRLF, checked by a small script before each
  commit (`.sh` and `.jsonl` apart).

## 6. The checker (the project's own)

One piece of code, used in three places, each with a scope that is written down (EX_303 FFS-C01). It reads files
from the disk; it never asks Git what exists.

| Where | Exactly which files it checks |
|---|---|
| **A test of the suite, in DEV** | every file under `src\`, `deploy\` and `tests\` and the root's own files, by walking those folders; Python's cache folders left out; the six files of section 3A left out by name |
| **`Make_Installable`** | exactly the files the marker it is about to write lists (a variant's declaration, its files and helpers; or the manifest, the infrastructure and the install tools). Nothing in the wrong form can be marked ready, so nothing in the wrong form can be installed |
| **`Check_Tree`, for a tree** | the files on the tree's list of installed files; its `ENVIRONMENT.ini`; every status file; and what the project's programs have written under `source_data\`, `results\research\` and `records\`, each by its kind |

**Never checked, in any of the three:** a tree's `.venv\`; `.git\`; frozen history; `GAIS\`. It names each file that
does not conform, says which rule of section 3B it breaks, and says what to do.

## 7. Getting there: the conversion, safely

1. **A conversion list, made in the cloud from the repository:** every tracked file to be converted, with its
   SHA-256 before and after.
2. **A conversion program** (standard library; it never calls Git), run by the owner in DEV from a sheet, on his
   own go. **Before it changes anything it walks DEV's own folders itself and prints what it found, by class,**
   and he confirms:

   | Class | Which files | What happens |
   |---|---|---|
   | Listed | the files of the conversion list | converted, by the rule below |
   | DEV's own settings | `ENVIRONMENT.ini` (made by hand; in no list) | converted by rule: line endings only; its SHA-256 before and after go into the conversion's record |
   | Made again, not converted | DEV's research results `results\research\`; each variant's `VARIANT_STATUS.ini` in DEV; leftovers in `records\` | removed on the owner's own go and written afresh by the corrected engine at the fill. A status file holds a check over its own bytes, and DEV's hold nothing but `ACTIVE`; **if one holds a withdrawal or an eligibility draw, the program stops for his decision** |
   | Untouched, and proved untouched | the results masters and their ledgers (CRLF already: the SHA-256 of each is the same before and after, and the ledger's record of its master's hash stays true); the updater's grabs and backups under `source_data\`, whose hashes the ledger records; the Mode H opening records; the old run folders and every other record of the old system; `transitory_data\`; the six files of section 3A; `.venv\` | nothing; the program reads the masters and ledgers and shows their hashes unchanged |
   | Anything else in those folders | a file of a text kind that is in no class above | named, and the program stops before changing anything |

   **The rule for a listed file, which also makes a second run safe** (EX_303 FFS-C04): its SHA-256 equals the
   list's "after": already converted; checked and passed over. It equals the list's "before": it is converted
   (the new file written under a temporary name and renamed into place, then hashed again), and the program
   proves that the new bytes differ from the old in line endings only. **Any third value is a STOP.** A run that
   was interrupted is therefore simply run again; the files are not claimed to change all at once.
   **The way back is the owner's copy, not the list.** Recovery is from the owner's pre-conversion copy of the
   project folder, checked before the conversion begins: the program reads the copy and goes on only if every
   file it is about to convert, and every file that is about to be removed, is in the copy with the same
   SHA-256 as in the tree. The "before" hashes it records verify, afterwards, that the original files have been
   recovered exactly. **The conversion list is not itself a backup:** making line endings uniform can turn two
   different files into the same bytes, so a path and two hashes cannot rebuild an original. No undo is built.
   **While it runs nothing else does:** it holds the tree's job lock and the updater's own lock, so no research job
   and no results update can start, and the sheet has the owner close everything else of the project first.
   **Before it runs** the owner makes his own copy of the project folder. That copy is the one way back, for
   the converted files, for DEV's own settings file and for the derived outputs that are removed.
3. **Everything computed from bytes is made again** (the owner, section 8: "if hashes need redoing then do it"):
   any hash a test holds for a converted file; every variant's fingerprint and the identity of the forecasting
   code, by which **DEV's research results are removed by hand and filled again once** (about 47 minutes). **A
   hash is redone openly:** the conversion's own record keeps, for each file, the SHA-256 before beside the SHA-256
   after, so that any hash recorded earlier can still be checked against the file by anyone; nothing is made to
   look as if it had always been so, and no record of the frozen history is rewritten to match.
4. **The engine's writers** are changed to the forms of section 3 (reports, read-me files, tables, status files,
   markers, records); the lists are not touched.
5. **Proof:** the whole suite before and after, in the cloud and on the owner's PC, its tests of N-1 isolation
   among them; the comparison of DEV's new fill with the old system's records once more (it compares scientific
   content, which no line ending changes); the checker passing on every file. **A changed line ending is no
   licence to change a calculation or to read a later draw:** the conversion's list proves, file by file, that
   nothing but line endings changed. **Old lists are not repaired:** DEV's old lists are removed, not edited, and
   no digest of an old `.jsonl` line and no sealed record is touched.
   **What is proved so far, and what is not:** the cloud's trial (section 9) covers the conversion of the tracked
   code only. It did not cover `source_data\`, the engine's changed writers, the refresh of the owner's working
   copy, or Windows. Each of those is tested, in the cloud and then on Windows, before the conversion is called
   proved; none of them is needed to ratify the standard itself.
6. **Order:** before slice A of build step 3 is packaged, because the markers and the list of installed files hash
   these bytes. QA and PROD are created afterwards and are born conforming.

## 8. Decided by the owner (24 November 2026, 18:28; decision log entry 231)

His words on the principle: "if hashes need redoing then do it even if fudging is somehow necessary - our priority
is to safely convert and move toward making everything operational." (How a hash is redone: section 7 item 3.)

1. **The scope of section 2:** frozen history is left as it is. "yes to your recommendation scope freezing historical
   documents that are not "actively used" in a DEV/QA/PROD program running sense, assuming they are "only documents
   to read"."
2. **The `.jsonl` lists stay LF,** "as long as they are noted as such in the standard and operations manual"
   (section 3; section 10).
3. **`* -text` for the whole repository:** yes (one refresh of the owner's working copy on the day).
4. **The results' verification records** (`source_data\<GAME>_results_master_init_verification.json`, LF today,
   written by the old updater): converted with everything else, "even if hashed (redo the hashes if and when
   needed)". What Claude found reads them: the new reader names the record and takes no hash of it; the old
   system's runner recorded the file's SHA-256 in its run records, which are frozen history and keep the old value;
   the conversion's record ties the two together. The results masters and their ledgers are CRLF already and are
   not changed.
5. **The six files of the retired release machinery** are left out by name: "yes to your recommendation ignoring
   retired machinery and we should note that in the standard" (section 3A).

**Put to the owner in v0.1r1 (EX_303 FFS-C03), and decided by him on 24 November 2026, 18:59 (decision log entry
234):**

6. **`GAIS\` keeps its own Git rules.** His decision 3 was "`* -text` for the whole repository". The root file
   cannot govern `GAIS\`, which has attribute files of its own (section 5), and Claude does not write there.
   His words: "ok "`GAIS\`" tree is out of scope as historical subproject, so yes to your recommendation." So
   the statement of section 5 stands: nothing converts anywhere in this project; `GAIS\` keeps that other
   project's own rules, and nothing under it is changed. (v0.2: it takes two more lines of the root file to
   make that true: item 7.)

**Put to the owner on 24 November 2026 with the fault of fact of section 5 (decision log entry 250), and decided
by him the same evening, 21:48 (decision log entry 251):**

7. **The root attribute file holds three lines** (section 5). His words: "yes to Question: may the root attribute
   file hold three lines instead of the one the standard ratified? yes to Recommendation: approve the three
   lines".

## 9. What the trial in the cloud found

Claude converted a copy of the repository and ran the whole suite before and after (24 November 2026; the
test-by-test comparison is `exchange/CLAUDE_WEB_TOOLS/standards/TRIAL_CRLF_SUITE_COMPARISON.txt`).

- **Converted:** every tracked text file under `src`, `deploy`, `tests` and the root, 669 files (239 `.py`, 419
  `.json` and a few others), with `.gitattributes` saying `* -text`.
- **Before:** 762 tests; the three tests that are known to fail, and no others.
- **After: 732 of the 762 tests gave the same result. 30 changed from passing to failing, all in five test modules
  of the retired Mode H release machinery** (`test_mhupa_install_records`, `test_mhupa_mode_h`,
  `test_mhupa_method_mode_h_cli`, `test_mhupa_process_check`, `test_mhupa_updater_v0_2`). **Every test of the new
  research engine and every test of a method's arithmetic passed unchanged.**
- **The 30 trace to six files,** each of which a test pins to its exact bytes: the three install and release
  records of the old release mechanism (`src/methods/_common/contract_data/install_records/`, canonical JSON); the
  old process tool `src/package_tools/process_check.py` (a test asserts it holds no carriage return); the present
  results updater `src/results_master_v0_2.py` and the reference copy of its predecessor under `tests/fixtures/` (a
  test holds the updater's SHA-256). **With those six put back as they were, all five modules passed again,** and
  the three known failures were the same as before.
- **So the conversion of the code costs nothing in the tests except for those six files** (open point 5).
- **Not tried yet:** `source_data\` (the trial left it alone); the engine's writers changed to write the standard's
  forms; the conversion program itself; any of it on Windows.

## 10. For the operations manual

A section "Standards", a few lines: the rule of section 1; the table of section 3, **with the `.jsonl` lists named as
the one kind that is LF and why;** the retired machinery left out by name (section 3A); what to do when the checker
names a file (in VS Code, click the `LF` or `CRLF` at the bottom right and choose; in Notepad++, Edit, EOL
Conversion).

## 11. Still to be established before the conversion is packaged

- A list of every program in the living project that writes a file, with the form it writes (section 4's test finds
  the writes; 17 are known in old code).
- Whether any file of the living project is of a kind the table of section 3 does not name (section 3B refuses
  one); Claude's count of the tracked living files found none beyond the table as it now stands.
- What the owner's DEV holds under `source_data\` and `records\` that Git does not track (the preflight of section
  7 prints it before anything is changed).
- (v0.2: not commands but a program: section 5.) The one refresh of the owner's working copy, rehearsed by the runner in a
  task clone.
- The same trial with `source_data\` converted, and the whole of it again on Windows.
