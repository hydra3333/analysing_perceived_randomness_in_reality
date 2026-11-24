# The project's standard for the form of its text files (line endings) - v0.1 CANDIDATE

**Date:** 24 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status:** a CANDIDATE for the
reviewer's reading and then the project owner's ratification, as a note of ratification to the specification v0.6,
beside the coding practices. The owner has decided its five open points (section 8; decision log entry 231). It is
not ratified, changes nothing by itself, and authorises nothing on the owner's PC. Ratified, it replaces the words
"LF pinned" of decision log entry 181 and the advice in the specification's section 20 on pinning line endings in
`.gitattributes`. Made from the draft of the same day (`FILE_FORM_STANDARD_v0_1_DRAFT.md`, kept beside it).

**Why it exists (the owner, 24 November 2026, decision log entries 227 to 230).** "git should never be used as an
operational gatekeeper/checker"; "I prefer being consistent if possible"; "we should create a spec ... expressly have
a list of file types and/or data types and exactly which type they use so that there is never any ambiguity";
"everything confirms to the standards ... whatever it takes to get it done (safely)"; "ensure our git settings files
stuff and github settings all do the right thing"; and a "standards" section in the operations manual.

## 1. The rule, in four sentences

1. **Every text file of the living project is in Windows form: each line ends CRLF** (carriage return, line feed),
   whether a person or a program wrote it. One kind of file is the exception, by its nature: the hash-chained
   record lists (`.jsonl`, section 3). The retired Mode H release machinery is left out by name (section 3A).
2. **Every program that writes a file says which line ending it writes;** none leaves it to the platform's default.
3. **Git converts nothing.** What is on disk is what is committed, and what GitHub shows is what the tools hash.
4. **The project's own checker says whether the rule is kept,** in the test suite and before anything is marked
   ready to install. Git is never asked.

## 2. What the standard covers, and what it does not

| | What | Rule |
|---|---|---|
| **The living project** | the repository's root files; `src\`; `deploy\`; `tests\`; the runner's tools; everything a DEV, QA or PROD tree holds; everything the project's programs write (results, lists, reports, logs, records) | section 3, without exception |
| **Frozen history** | what is only read by people and used by no program that runs in DEV, QA or PROD: `exchange\`, `review\`, `archive\`; the documents under `doc\` as ratified; the old system's own records under `results\` (the old run folders, the old reports, the retired Mode H records) | **never converted, never edited.** They are records of what was exchanged, reviewed, ratified or computed, each in the bytes it had. A file Claude adds to these folders after this standard is ratified is written in the standard's form |
| **Not this project's** | `GAIS\` | untouched |
| **Not text** | `.zip`, `.pdf` and any file holding a zero byte | no line endings |

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
| **Hash-chained record lists** | `*.jsonl` (every variant's forecast list and score list; the OV-1 ledger; the logs under `records\`) | programs only; never a person | LF | **LF: the one exception** (below) |
| Shell scripts | `*.sh` | Claude's cloud helpers under `exchange\` | LF | LF: Linux refuses anything else. None is part of the living project |

**The one exception, and why it is not a halfway house.** A line of a `.jsonl` list is the canonical encoding of one
record, byte for byte, and that encoding ends in one LF. The same bytes are what every link of the list's hash chain
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

## 4. Every program says what it writes

Python's ordinary way of writing a text file uses the platform's own line ending: the same program writes CRLF on
the owner's PC and LF in Claude's cloud workspace unless it says otherwise. So:

- **A file is written either in binary, from bytes the code made, or with its line ending named** (`newline=`). No
  write relies on the default.
- **A test reads the code and fails on any write that names none** (found today, to be corrected: 17 in the old
  system's code, most of them in its self-tests; none in the new engine).
- This becomes one line of the coding practices.

## 5. Git and GitHub: nothing converts

- **`.gitattributes` says one thing for the whole repository: `* -text`.** Git then never changes a line ending, in
  either direction, on any PC, whatever its own `core.autocrlf` setting is. The existing special lines are no
  longer needed.
- **`.gitignore`** gains the readiness markers and the marker staging folder (state of one tree, never tracked).
- **GitHub:** a push stores the bytes pushed, and there is no repository setting on GitHub that converts line
  endings; GitHub's own guidance on the subject is about `.gitattributes` and each PC's Git settings. **What
  GitHub's editor in the browser does to a file's line endings Claude could not establish** (a search found clear
  reports for other hosting products, none authoritative for GitHub). So the rule does not depend on it: **no file
  of the living project is edited or created in the browser;** files reach GitHub by a commit from a PC. If one
  ever arrives in the wrong form, the project's own checker names it at the next suite run.
- **The owner's working copy needs one refresh,** on the day: with `core.autocrlf=true` Git has, until now, written
  CRLF copies of files it stores as LF (every document he has pulled). Under `* -text` those copies would all show
  as changed. The exact, rehearsed commands for that one refresh are part of the conversion's sheet.
- **Claude's own commits:** every text file Claude adds from then on is CRLF, checked by a small script before each
  commit (`.sh` and `.jsonl` apart).

## 6. The checker (the project's own)

One piece of code, used in three places: a test of the suite (every file of the living project against section 3);
`Make_Installable` (nothing in the wrong form can be marked ready, so nothing in the wrong form can be installed);
and `Check_Tree` (the same for a tree). It names each file that does not conform and says what to do. A file with
mixed endings is a fault of its own kind.

## 7. Getting there: the conversion, safely

1. **A conversion list, made in the cloud from the repository:** every file to be converted, with its SHA-256 before
   and after.
2. **A conversion program** (standard library), run by the owner in DEV from a sheet. For each file it checks the
   SHA-256 before, writes the new file under a temporary name and renames it, checks the SHA-256 after, and proves
   that the new bytes differ from the old in line endings only. Anything unexpected refuses and changes nothing
   more. Run a second time it finds nothing to do.
3. **Everything computed from bytes is made again** (the owner, section 8: "if hashes need redoing then do it"):
   any hash a test holds for a converted file; every variant's fingerprint and the identity of the forecasting
   code, by which **DEV's research results are removed by hand and filled again once** (about 47 minutes). **A
   hash is redone openly:** the conversion's own record keeps, for each file, the SHA-256 before beside the SHA-256
   after, so that any hash recorded earlier can still be checked against the file by anyone; nothing is made to
   look as if it had always been so, and no record of the frozen history is rewritten to match.
4. **The engine's writers** are changed to the forms of section 3 (reports, read-me files, tables, status files,
   markers, records); the lists are not touched.
5. **Proof:** the whole suite before and after, in the cloud and on the owner's PC; the comparison of DEV's new fill
   with the old system's records once more (it compares scientific content, which no line ending changes); the
   checker passing on every file.
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

## 9. What the trial in the cloud found

Claude converted a copy of the repository and ran the whole suite before and after (24 November 2026; the
test-by-test comparison is `TRIAL_CRLF_SUITE_COMPARISON.txt` beside this file).

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
- Whether any file of the living project is of a kind the table of section 3 does not name; the checker refuses an
  unnamed kind, so that the table is always complete.
- The exact commands of the one refresh of the owner's working copy under `* -text`, rehearsed by the runner in a
  task clone.
- The same trial with `source_data\` converted, and the whole of it again on Windows.
