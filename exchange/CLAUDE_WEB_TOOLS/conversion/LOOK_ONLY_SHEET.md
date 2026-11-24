# A look-only run of the conversion program in the real DEV tree: the owner's sheet

**Only on the owner's own go. It changes nothing.** 24 November 2026; decision log entry 246.

**What it is for.** The conversion to the file-form standard (`doc/FILE_FORM_STANDARD_v0_1.md`, RAT-47) will stop,
before it changes anything, at any file in the project folder that it cannot place. Git knows only the tracked
files; this look shows what the real folder holds besides. Finding that out now costs a minute; finding it out
on the day costs the day.

**What the look does.** It walks the project's own folders (the root's files, `src`, `deploy`, `tests`, `.claude`,
`.vscode`, the runner's tools, `source_data`, `results\research`, `records`, `scratch`), reads the files there, and
prints what a real run would do with each class of them. It never enters `.venv`, `.git`, `exchange`, `doc` or
`transitory_data`.

**What it does not do.** It writes nothing in the project folder, takes no lock, copies nothing, removes nothing,
starts no other program, contacts nothing, and prints no content of any file: only file names, counts and
SHA-256 values. Nothing is installed: the three files it uses lie under `exchange\` and are run from there. The
one file that is written is the output file in `E:\TEMP`, made by the `>` of the command line itself.

**The three files** (`exchange\CLAUDE_WEB_TOOLS\conversion\look_kit\`; each committed in Windows form, so the bytes
on disk after a pull are the bytes committed):

| File | SHA-256 |
|---|---|
| `convert_to_file_form.py` (the program; the look is its `--look`) | `dd690abe28b27aede35c1951025e8835e0d80c45de63ce1704ed254bedcaceb7` |
| `file_form.py` (the standard's rule; the program refuses any other) | `1d77cb9dd48ce50bc9d35b777b43df077303a810e1cb874466be166e1b6920cf` |
| `CONVERSION_LIST.json` (today's list, 686 files) | `94be7098e64976c7c15431779de2b139ba14f53b5b99a105fc69e7f219f574b6` |

## The steps (Windows CMD)

```bat
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git pull --ff-only
certutil -hashfile exchange\CLAUDE_WEB_TOOLS\conversion\look_kit\convert_to_file_form.py SHA256
.venv\Scripts\python.exe -I -B exchange\CLAUDE_WEB_TOOLS\conversion\look_kit\convert_to_file_form.py --tree . --list exchange\CLAUDE_WEB_TOOLS\conversion\look_kit\CONVERSION_LIST.json --look > E:\TEMP\FILE_FORM_look.txt 2>&1
type E:\TEMP\FILE_FORM_look.txt
```

**Expected.**
- `certutil` prints the program's SHA-256 from the table above. If it prints another value, stop there.
- The second line of the output names the list's SHA-256 from the table above.
- The last line begins `FILE-FORM CONVERSION - END - LOOKED ONLY; nothing was changed.` and then says one of two
  things, **neither of which is a failure of the look:** `A real run would find nothing to stop it.` or `The
  findings above would stop a real run before it changed anything.` The findings are what the look is for.
- A line `THE PACKAGE'S OWN FILES, not yet here .. 12 file(s)` is expected: nothing is installed yet.
- **A line beginning `STOP:` or a Python traceback is a STOP:** do nothing further.

**Then:** send Claude the file `E:\TEMP\FILE_FORM_look.txt` (or paste what `type` printed). It holds file names,
counts and hashes only.
