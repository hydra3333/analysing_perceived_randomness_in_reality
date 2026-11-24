# A look-only run of the conversion program in the real DEV tree: the owner's sheet (r1)

**Only on the owner's own go. It changes nothing.** 24 November 2026; decision log entries 246 and 247.
**r1:** the two corrections of the reviewer's EX_308 are made in the kit (it prints no content of a status file;
it names every link, junction or other reparse point and never enters or reads one), and its sheet precautions
are taken up below. The first sheet and the first kit (`look_kit\`) stay as they were reviewed; use this sheet and
`look_kit_r1\`.

**What it is for.** The conversion to the file-form standard (`doc/FILE_FORM_STANDARD_v0_1.md`, RAT-47) will stop,
before it changes anything, at any file in the project folder that it cannot place. Git knows only the tracked
files; this look shows what the real folder holds besides. Finding that out now costs a minute; finding it out
on the day costs the day.

**What the look does.** It walks the project's own folders (the root's files, `src`, `deploy`, `tests`, `.claude`,
`.vscode`, the runner's tools, `source_data`, `results\research`, `records`, `scratch`), reads the files there, and
prints what a real run would do with each class of them. It never enters `.venv`, `.git`, `exchange`, `doc` or
`transitory_data`. A link, a junction or any other reparse point it meets in those folders is named as a finding and
is neither entered nor read.

**What it does not do.** It writes nothing in the project folder, takes no lock, copies nothing, removes nothing,
starts no other program, contacts nothing, and prints no content of any file: only file names, counts and
SHA-256 values. Nothing is installed: the three files it uses lie under `exchange\` and are run from there. The
one file that is written is the output file in `E:\TEMP`, made by the `>` of the command line itself.

**The three files** (`exchange\CLAUDE_WEB_TOOLS\conversion\look_kit_r1\`; each committed in Windows form, so the
bytes on disk after a pull are the bytes committed):

| File | SHA-256 |
|---|---|
| `convert_to_file_form.py` (the program; the look is its `--look`) | `0dc02db3fd69e23590f0ee54f59372870856b054edeaad5da937385881d05bde` |
| `file_form.py` (the standard's rule; the program refuses any other) | `e27e57b43a18108cc0a343b921a15e1f40c80fa2756e070d1cac4f4a7c78310c` |
| `CONVERSION_LIST.json` (today's list, 686 files) | `a60fcd78562b7903afe689bcea796fb3cc7bbb74c7b90f9fdf61d262f25544a9` |

## Before the look

**Nothing else of the project is running:** no research job, no results update, no runner task.

**The pull is a separate step, and not part of "changes nothing":** it updates the working copy, as every pull
does. Do it first.

```bat
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git pull --ff-only
```

## The look (Windows CMD, in the same folder)

```bat
certutil -hashfile exchange\CLAUDE_WEB_TOOLS\conversion\look_kit_r1\convert_to_file_form.py SHA256
certutil -hashfile exchange\CLAUDE_WEB_TOOLS\conversion\look_kit_r1\file_form.py SHA256
certutil -hashfile exchange\CLAUDE_WEB_TOOLS\conversion\look_kit_r1\CONVERSION_LIST.json SHA256
.venv\Scripts\python.exe -I -B exchange\CLAUDE_WEB_TOOLS\conversion\look_kit_r1\convert_to_file_form.py --tree . --list exchange\CLAUDE_WEB_TOOLS\conversion\look_kit_r1\CONVERSION_LIST.json --look > E:\TEMP\FILE_FORM_look.txt 2>&1
type E:\TEMP\FILE_FORM_look.txt
```

**Expected.**
- The three `certutil` lines print the three SHA-256 values of the table above, in its order. If any differs,
  stop there and run nothing.
- No compiled copy of the rule can stand in for it: the program reads `file_form.py` itself, checks those bytes
  against the list, and runs exactly those bytes; Python's own import cache is not used, read or written.
- The second line of the output names the list's SHA-256 from the table above.
- The last line begins `FILE-FORM CONVERSION - END - LOOKED ONLY; nothing was changed.` and then says one of two
  things, **neither of which is a failure of the look:** `A real run would find nothing to stop it.` or `The
  findings above would stop a real run before it changed anything.` The findings are what the look is for.
- A line `THE PACKAGE'S OWN FILES, not yet here .. 12 file(s)` is expected: nothing is installed yet.
- **A line beginning `STOP:` or a Python traceback is a STOP:** do nothing further.
- **If a finding names a lock file, do nothing about the lock:** tell Claude. A lock is cleared only by the
  project's own procedure for it, never on the strength of this look.

**Then:** send Claude the file `E:\TEMP\FILE_FORM_look.txt` (or paste what `type` printed). It holds file names,
counts and hashes only.
