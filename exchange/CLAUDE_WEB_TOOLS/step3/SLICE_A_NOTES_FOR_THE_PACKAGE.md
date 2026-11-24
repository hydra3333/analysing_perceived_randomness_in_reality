# Slice A of build step 3: notes for the package (a working file; not a design, not a rule)

Kept by the Claude web chat while slice A is written, so that the package's note can be made from it and so that
another chat can go on. The authority is the specification v0.6, the deployment design v0.12, the coding practices
and the file-form standard v0.2. Decision log entries 264 to 266 and 270 to 274 are the record. Everything in
`overlay/` is working files: not a package, not reviewed, nothing installed.

## 1. What the overlay holds (25 November 2026, after step 2 of the remaining work)

Sixteen files, all CRLF, laid out as they go into the tree.

| File | New or changed | What it is |
|---|---|---|
| `ENVIRONMENT.example.ini` | changed | the rewritten example (entry 211) |
| `Make_Installable.bat`, `Check_Tree.bat` | new | the two launchers of this slice, in DEV |
| `deploy/INFRA_MANIFEST.ini` | changed | `[files]` gains `deploy/file_form.py` and `src/research/installed_files.py` (both `other`); the new `[install_tool]` section has seven files |
| `deploy/deploy_command.py` | new | the one program behind DEV's install launchers (two commands so far) |
| `deploy/install_import_check.py`, `deploy/install_readiness.py`, `deploy/make_installable.py` | new | the static import check; the two readiness markers; the command |
| `deploy/check_tree.py` | new | `Check_Tree`: the owner's read-only look at one tree |
| `src/research/settings.py` | changed | DEV's entries for QA and PROD and the cross-tree checks |
| `src/research/code_identity.py` | changed | the `[install_tool]` list; see reading 2 |
| `src/research/installed_files.py` | new | the list of installed files: made, written, read, compared with the tree |
| `tests/test_trees_settings.py` (32), `test_trees_readiness.py` (40), `test_trees_installed_files.py` (22), `test_trees_check_tree.py` (22) | new | 116 tests |

## 2. Still to write

1. The check of the environment's digest over the fixed inventory (specification 13), with the question of one
   digest or two (reading 7). `Check_Tree` then also says whether `ENVIRONMENT_VERIFIED.json` is present.
2. The launch guard with the process rule (deployment design 9; build plan 4A). The names of the
   unfinished-operation files come with it; `Check_Tree`'s "Locks" then lists them too (today it lists the job
   lock, the updater's lock and the orphan marker).

## 3. Readings and choices to put to the reviewer with the slice (each RECOMMENDED, none decided by Claude alone)

1. **A variant may import its own listed files as well as its helpers; the tool itself refuses a variant that
   imports an infrastructure file not classed `forecast`** (entry 225; H-1 v13 section 0E item 14).
2. **The manifest in an installed tree.** A QA or PROD tree holds the manifest as DEV has it, and the manifest
   names the install tool's files, which are never installed there. So the manifest's reader requires a `[files]`
   path to exist in every tree, and an `[install_tool]` path to exist only where that list is asked for, which is
   DEV (`read_install_tool_list`). Specification 12.4 says "a path that does not exist ... refuses"; this is how it
   is kept without making every job in QA and PROD refuse.
3. **The list of installed files** is `records/INSTALLED_FILES.json`: `kind`; `files` (the manifest, every
   `[files]` file, every variant's declaration, declared files and helpers, each once, with its SHA-256);
   `variants` (family, variant, fingerprint); `status_files` (names only). Its code is infrastructure in every
   tree, class `other`. It is made from the tree as it stands; a variant folder that fails its checks refuses the
   making. DEV keeps no list.
4. **Nothing else lies under `src`** (deployment design 9), as the reviewer recommended at the takeover (entry
   270): anything under `src` that is neither a listed file nor a listed status file is a difference, Python's
   cache folder included (named once, not entered) and a link (named, not read). Inside a variant folder the
   fingerprint still passes over caches, as specification 3.4 says. No command removes anything.
5. **`Check_Tree`** takes `DEV`, `QA` or `PROD`, is run from DEV with DEV's Python and DEV's code, and runs no code
   of the tree it looks at. It writes nothing anywhere and takes no lock. What it calls found (exit code 1): the
   tree differing from its list; a variant folder or a status file failing its checks; a file not in its form.
   What it only reports: what is ready in DEV, how the tree compares with DEV (an install is the owner's act),
   the backup ZIPs (listed with full path, size and date; none verified), the locks. A tree not created yet is
   said as such, with `Init_Tree.bat <role>`.
6. **The form check's files in `Check_Tree`** (standard section 6): the tree's list of installed files (in DEV,
   which keeps none, the manifest's two lists and each variant's hashed files); `ENVIRONMENT.ini`; every status
   file; every file under `results/research` and `records`; and under `source_data` the files lying directly in
   it. Left as they are: the two opening records of the retired first study (standard 3A) and the updater's kept
   copies in `source_data`'s sub-folders (standard 7 lists them as untouched). The concrete reason: a walk of all
   of `source_data` would report, in DEV, files that the standard itself says are never converted.
7. **OPEN, for the owner with the slice: one environment digest or two** (entry 270, the reviewer's preference:
   one, computed once at a job's start, used for verification and for new envelopes; old envelopes untouched).
8. **What a QA or PROD tree gains outside `src`:** `deploy/INFRA_MANIFEST.ini` (the engine reads it in every
   tree) and `deploy/file_form.py` (the owner, entry 265). The deployment design's section 2 picture shows no
   `deploy` folder; the two files are on the list of installed files.
9. **The unratified narrow amendment** of the deployment design's section 2 ("standard library only" for the
   install tools, except the process rule, which uses psutil; entry 222) goes with the launch guard.

## 4. The cloud's evidence so far (Claude's, not Windows'; Python 3.15.0b4 on Linux)

- `main` at `1e9ad25`: 54 modules, 830 tests, the three known failing tests (entry 273).
- With the sixteen files: **58 modules, 946 tests; all 830 earlier tests with the same result; the 116 new tests
  OK.**
- Planted faults in the two new programs and the manifest reader (`mutation_check_installed_files_and_check_tree.py`
  beside this file): 23 planted, 23 caught.
- `Check_Tree DEV` on the real files of a disposable clone, read-only: 40 variants, 169 files checked for form,
  none found, under a second.
- Not shown anywhere yet: a launcher on Windows; a real QA or PROD tree (none exists; the list of installed files
  is written for the first time by `Init_Tree`, slice C).
