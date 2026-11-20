### 4.7 The recovery kit (EX_250 R3-C01; decision log entry 112, item F)

- **Why.** The E: clone is a working place: its files may be edited, its environment broken, or the drive gone, at
  exactly the moment a restore is needed. So the restore must not need it.
- **What it is.** `T:\a_p_r_i_r_backups\DEPLOY_KIT_<YYYYMMDD>_<HHMMSS>_<release>.zip`, made by `init` and by every
  `update` **from the release commit's own bytes** (Git's objects, as for the release itself; never working files).
  A few small files:
  - the deploy tool itself (the same reviewed file; in a kit only `restore` and `check` are of use, because the
    others need Git);
  - `Restore_Production.bat`, which starts it with whatever Python is installed for the user (the `py` launcher, or
    `python`);
  - `HOW_TO_RESTORE.txt`: the steps in plain English, the last-resort unzip by hand included;
  - the release's hash list (`RELEASE_<commit>.json`) and the release description;
  - `KIT_MANIFEST.json`: the kit's own identity (release, time, the tool's version) and the SHA-256 of every file in it.
  Beside the zip, `<name>.zip.sha256` holds the zip's own SHA-256.
- **Nothing in it needs installing.** The tool uses the standard library only. In particular its restore-time process
  check uses no third-party package (section 8), so any Python 3 the user has will run it.
- **How it is trusted.** Before doing anything, the tool run from an unpacked kit checks its own files against
  `KIT_MANIFEST.json`, and the kit zip against its `.sha256` when the zip is at hand, and prints the kit's identity.
  A digest shows accidental change or a wrong file; it is not a signature and proves nothing against a deliberate
  attacker. That is stated, not hidden.
- **Which kit for which snapshot.** Every snapshot's manifest names the release it holds and the kit made for that
  release. The matching kit is the recommended one. Because a restore is "verify, rename, unpack, verify", a newer
  kit can restore an older snapshot; the tool says when the two do not match and goes on only if the snapshot's
  format version is one it knows.
- **`update` and `init` stop if the kit cannot be written and verified on T:** (the owner: "T: must be available").
  This is checked first, before anything in production changes. It is separate from the rule for a snapshot that
  cannot be made, where jobs go on.
- **If something is missing at a restore** (no kit, no Python at all, a kit that fails its own check): the tool does
  not start, or stops before touching anything, and says what is missing. The owner's copies of T: on USB3 and in the
  cloud hold every kit and snapshot; the Python installer kept on T: puts Python back. Beyond that, the last resort
  is the unzip by hand (section 8).
- **Not a second tool.** One program, shipped twice: in the clone for `init`, `update` and `export`; in the kit for
  `restore`.

