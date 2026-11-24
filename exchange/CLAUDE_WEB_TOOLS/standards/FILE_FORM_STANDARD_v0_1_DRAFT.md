# The project's standard for the form of its text files (line endings) - v0.1 DRAFT, for discussion

**Date:** 24 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status:** a DRAFT for the project
owner's reading and decisions. It is not ratified, changes nothing, and authorises nothing. When its open points
(section 8) are decided it goes to the reviewer, and then to the owner for ratification as a note of ratification to
the specification v0.6, beside the coding practices. It would replace the words "LF pinned" of decision log entry
181 and the advice in the specification's section 20 on pinning line endings in `.gitattributes`.

**Why it exists (the owner, 24 November 2026, decision log entries 227 to 230).** "git should never be used as an
operational gatekeeper/checker"; "I prefer being consistent if possible"; "we should create a spec ... expressly have
a list of file types and/or data types and exactly which type they use so that there is never any ambiguity";
"everything confirms to the standards ... whatever it takes to get it done (safely)"; "ensure our git settings files
stuff and github settings all do the right thing"; and a "standards" section in the operations manual.

## 1. The rule, in four sentences

1. **Every text file of the living project is in Windows form: each line ends CRLF** (carriage return, line feed),
   whether a person or a program wrote it. One kind of file is the exception, by its nature: the hash-chained
   record lists (`.jsonl`, section 3).
2. **Every program that writes a file says which line ending it writes;** none leaves it to the platform's default.
3. **Git converts nothing.** What is on disk is what is committed, and what GitHub shows is what the tools hash.
4. **The project's own checker says whether the rule is kept,** in the test suite and before anything is marked
   ready to install. Git is never asked.

## 2. What the standard covers, and what it does not

| | What | Rule |
|---|---|---|
| **The living project** | the repository's root files; `src\`; `deploy\`; `tests\`; the runner's tools; everything a DEV, QA or PROD tree holds; everything the project's programs write (results, lists, reports, logs, records) | section 3, without exception |
| **Frozen history** | `exchange\`, `review\`, `archive\`; the documents under `doc\` as ratified; the old system's own records under `results\` (the old run folders, the retired Mode H records and their opening records in `source_data\`) | **never converted, never edited.** They are records of what was exchanged, reviewed, ratified or computed, each in the bytes it had. A file added to these folders after this standard is ratified is written in the standard's form |
| **Not this project's** | `GAIS\` | untouched |
| **Not text** | `.zip`, `.pdf` and any file holding a zero byte | no line endings |

*Why history is left alone (Claude's recommendation; the owner may widen the scope):* recorded hashes all over the
decision log and the exchange messages name those bytes; the reviewer's files are not Claude's to change; no program
reads them; and the old system's records are the oracle of the transition check, which is best made on untouched
files. The owner has said that the retired Mode H material does not matter to him now; left as it is, it costs
nothing.

## 3. The list: each kind of file, and its form

"Today" is what Claude found in the repository on 24 November 2026 (Git's own listing; the engine's code).

| Kind of file | Names | Who writes it | Today | **Standard** |
|---|---|---|---|---|
| Python code | `*.py` | Claude's packages; the owner | LF (3 are CRLF on the owner's disk) | **CRLF** |
| Batch files | `*.bat`, `*.cmd` | Claude's packages | CRLF on disk, LF inside Git | **CRLF**, on disk and in Git |
| Settings, manifests, status files | `*.ini` (`ENVIRONMENT.ini`, `INFRA_MANIFEST.ini`, `VARIANT_STATUS.ini`) | the owner; `Init_Tree`; the status writer | LF | **CRLF** |
| JSON documents | `*.json` (a variant's `VARIANT.json`, registries, the readiness markers, `INSTALLED_FILES.json`, the records under `records\`, the results' verification records) | Claude's packages; programs | LF | **CRLF** |
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

**Not files, and not changed:** the strings the project hashes in memory (a fingerprint's lines
`<path><TAB><sha256><LF>` of specification 3.4; the canonical encoding itself). They are definitions of a hash, and
stay exactly as the ratified specification gives them.

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
- **GitHub has no setting that converts line endings;** it stores the bytes pushed to it. *(To be confirmed from
  GitHub's own documentation before this draft is final: what its web editor does to a file edited or created in
  the browser.)*
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
3. **Everything computed from bytes is made again:** the hashes the tests hold; the records the old system's tools
   check their files against; every variant's fingerprint and the identity of the forecasting code, by which
   **DEV's research results are removed by hand and filled again once** (about 47 minutes).
4. **The engine's writers** are changed to the forms of section 3 (reports, read-me files, tables, status files,
   markers, records); the lists are not touched.
5. **Proof:** the whole suite before and after, in the cloud and on the owner's PC; the comparison of DEV's new fill
   with the old system's records once more (it compares scientific content, which no line ending changes); the
   checker passing on every file.
6. **Order:** before slice A of build step 3 is packaged, because the markers and the list of installed files hash
   these bytes. QA and PROD are created afterwards and are born conforming.

## 8. Open points for the owner

1. **The scope of section 2:** frozen history left as it is (recommended), or converted too.
2. **The `.jsonl` lists stay LF** (recommended, for the reason in section 3), or are made CRLF as well, which means
   changing the shared canonical encoding and every chain.
3. **`* -text` for the whole repository** (recommended; one refresh of the owner's working copy on the day), or only
   for the living project's folders, leaving documents to Git's conversion as today.
4. **The results' verification records** (`source_data\*_init_verification.json`, LF today, written by the old
   updater): converted with everything else by the conversion program (recommended, if nothing is found to hash
   them: the trial left `source_data\` alone, so this is still to be established), or left until the new updater
   writes its own.
5. **The six files of the retired release machinery that tests pin to their bytes** (section 9). Either they are
   named in this standard as frozen records of the retired machinery and left as they are (recommended: no test
   changes, nothing of the old release records rewritten, and the owner's decision of entry 181 that
   `results_master_v0_2.py` stays untouched in DEV is kept); or they are converted too, and then two test lines
   and the old release tool's own definition of "canonical bytes" are changed to match. A later, separate question
   is whether the retired Mode H code and its tests leave the living project altogether.

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
- **Not tried yet:** the engine's writers changed to write the standard's forms; the conversion program itself; any
  of it on Windows.

## 10. For the operations manual

A section "Standards", a few lines: the rule of section 1; the table of section 3; what to do when the checker names
a file (in VS Code, click the `LF` or `CRLF` at the bottom right and choose; in Notepad++, Edit, EOL Conversion).
