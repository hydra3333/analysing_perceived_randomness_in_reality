"""Build H-1 v1r3 from the installed H-1 v1r2 by counted, exact edits (Claude, 28 Oct 2026; work item DOC-3).

Input: the Git blob of doc/HANDOVER/Claude_Primary_Handover_H1_v1r2.md (55543ba5...eac0, ASCII, LF).
Every edit replaces either an exact substring (asserted to occur once) or a whole line identified by
a unique prefix (asserted to match exactly one line). Inserted text is ASCII. Appendix B (v1r2's change
list) is kept; a new Appendix C lists the v1r3 changes.
Usage: python3 -I make_h1_v1r3.py H1_v1r2 OUT_v1r3
"""
import hashlib, sys

src, out = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0'
t = raw.decode('ascii')
count = 0


def sub(old, new):
    global t, count
    assert t.count(old) == 1, ('substring', t.count(old), old[:70])
    assert all(ord(c) < 128 for c in new)
    t = t.replace(old, new)
    count += 1


def line(prefix, new):
    global t, count
    lines = t.split('\n')
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hits) == 1, ('line', len(hits), prefix[:70])
    assert all(ord(c) < 128 for c in new)
    lines[hits[0]] = new
    t = '\n'.join(lines)
    count += 1


# ---- Header ----
line('# H-1 - Claude primary designer and coder handover',
     '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r3')
line('**Version:** v1r2 DRAFT',
     '**Version:** v1r3 DRAFT, 28 October 2026 (Adelaide, UTC+10:30). v1r3 is a records refresh (work item DOC-3): it brings v1r2 (owner-ratified 28 October 2026 and installed at `be18548`) up to date with the events and owner decisions of 28 October 2026: the E2R-1 specification, DOC-2, NAMES-1, the E1-ALIGN design, the phone exchange protocol, Python 3.15 and the indefinite oversight instruction. Appendix C lists every change; Appendix B (v1r2\'s changes) is kept. Author: Claude. Independent reviewer: the ChatGPT reviewer chat. The project owner ratifies.')
line('**Status:** DRAFT for review.',
     '**Status:** DRAFT for review. It becomes authoritative only when the owner ratifies it and installs it together with register v0.9; until then H-1 v1r2 stands. Nothing here grants any run, test, data-access, holdout, termination or Git permission.')
line('**Baseline described:**',
     '**Baseline described:** NAMES-1 installed at `52ebeaa385fd05b18c4f3805c3cd2000948e343d` (verified by Claude from GitHub: 27 renames, 27 edited and 15 added files, every blob matching its manifest; the immediate recovery check passed; section 7.1B), on top of DOC-2 at `908db9ea9d4a37b17833f5d43919804c78ef7e14` (section 7.1C), DOC-1 at `be185485693f29cf9ab28292dc6eebad00bbc32c`, TH-1 at `744afea`, the integration at `ae76c29` and Package 2 at `c542483`. Later commits up to `83d1515` are `exchange/` records only (section 1.6). The commit that installs this file cannot name itself; Claude records its ID in the post-push verification.')
line('**Replaces, for future roles:**',
     '**Replaces, for future roles:** H-1 v1r2 and v1r1 (kept as history); and, as before, Claude reviewer handover v10, ChatGPT coder handover v1.1r1, the interim note and Claude checkpoints v2 and v4. They stay in the repository as evidence. D-1 and ADD-2 are inputs to this file, not authority.')

# ---- Section 0 ----
line('2. Read, in order: this file;',
     '2. Read, in order: this file; H-2 (so you know what the reviewer will check); H-3; the review-disposition procedure (`review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`); `exchange/README.md` (the phone exchange protocol, section 1.6); the register (current edition); the governing set in section 4, including the E2R-1, NAMES-1 and E1-ALIGN specifications; the latest checkpoint file in `doc/HANDOVER/`, if newer than this file; the newest `exchange/EX_NNN_*` files, which show the latest open exchange with the reviewer.')

# ---- Section 1.1 ----
sub("You prepare complete, hash-recorded packages; you never push, open pull requests or alter the canonical branch.",
    "You prepare complete, hash-recorded packages; you never open pull requests, and you never change anything in the main tree. **The one exception (owner-authorised, 28 October 2026; `exchange/README.md` v0.3):** you commit and push inside `exchange/` only, recording every exchange file from both AI chats byte-for-byte (section 1.6).")

# ---- Section 1.5: oversight status ----
sub("**Status at v1r2:** two of the three are done (the TH-1 review and its recheck; REVIEWER-DECIDED items TH1-RD-01..04; no departure found). The third is the review of DOC-1, the package that carries this edition.",
    "**Since 28 October 2026 (owner decisions):** the instruction was first extended to six reviews and is now **extended indefinitely**, with **reporting by exception**. The reviewer still lists every REVIEWER-DECIDED item and Claude still checks every one, but Claude reports one to the owner only if Claude disagrees with it, or judges it of owner interest (for example a process deviation, a newly found gap, or a decision the owner must take). Reviewer rights are unchanged and the authority is not delegated. No departure has been found in any review so far.")

# ---- Section 1.6 ----
line('- You prepare exact candidate trees and patches in disposable workspaces;',
     '- You prepare exact candidate trees and patches in disposable workspaces; the owner applies, commits and pushes everything in the main tree. You never create remote pull requests or publish releases, and you push only `exchange/` records (next bullet).')
sub("- Test every verifier in two scratch clones before delivery:",
    """- **Phone exchange protocol (`exchange/README.md` v0.3, commit `262a2c4`; owner, 28 October 2026).** When the owner relays from a phone, each message between the two AI chats is **one upload**: `EX_NNN_<Sender>.md`, or a flat `EX_NNN_<Sender>.zip` whose EX message has a `Contents:` line (no ZIP inside a ZIP). One shared, increasing `NNN` sequence; the next number is the highest in `exchange/` plus one; never reuse a number (a correction takes the next number and says `Supersedes:`). First line `# EX_NNN - <Sender> to <Recipient>`; header lines `Date`, `Project`, `Replies to`, optional `Supersedes`, `Contents` (ZIPs) and `Subject`; US-ASCII, CRLF; no personal names. **Claude records every EX file from both sides in `exchange/`, unchanged** (a ZIP also extracted to `exchange/EX_NNN_<Sender>/`), commits only there, gives the commit hash, and checks the pushed copy. Nothing in `exchange/` is ratified; only the owner moves material into the main tree. At the PC the owner may upload two files when a deliverable is itself a ZIP (EX_012 and its companion install ZIP).
- **Files shipped with CRLF** (the exchange rule) carry two hashes: as shipped, and after CRLF-to-LF conversion (the canonical identity of LF repository and package files). When an exchange file later goes into `review/`, store an **LF copy** and cite the LF hash: the owner's Git uses `core.autocrlf=true` and converts CRLF at commit, which would make a committed-phase check fail. The CRLF originals stay in `exchange/`.
- **Install order (the reviewer's N1I-C01, 28 October 2026):** commit, run `--phase committed`, and push **only after `COMMITTED PASS`**; on a STOP the commit is still local and `git reset --hard HEAD~1` removes it. Begin every install with `git pull --ff-only` (exchange records may have moved `main` on) and a clean `git status --short`. While the owner installs, Claude pushes nothing. After the push, Claude verifies from GitHub and, where specified, runs an immediate recovery check (`git revert` in a disposable clone).
- **Already-committed files:** if a file a package would add is already committed (byte-identical), the verifier treats it as guarded, not new, and the builder asserts the byte identity first (NAMES-1, section 7.1B).
- Test every verifier in two scratch clones before delivery:""")

# ---- Section 2 ----
line('- End every handback that goes to the reviewer with a short **paste-ready block**',
     '- End every handback that goes to the reviewer with a short **paste-ready block** (a fenced `text` block). The owner likes these small pastes. **When the owner is on a phone, the EX file replaces the paste block** (section 1.6); hashes in any block are computed by a tool and copied, never retyped (section 8.6).')

# ---- Section 3 ----
sub("The project builds a Python 3.14 research system on Windows 11",
    "The project builds a Python research system on Windows 11 (the project venv is Python 3.15.2 since 28 October 2026; previously 3.14)")

# ---- Section 4 ----
line('| `RATIFICATION_REGISTER_v0_5.md` |',
     '| `RATIFICATION_REGISTER_v0_8.md` | `3f217c6875d443a0cc1bba2f6c329b1fda455fb4a97bf7fe06090394736fffcf` | Lineage and status after NAMES-1 (installed at `52ebeaa`); superseded by v0.9 when that is ratified and installed |\n'
     '| `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` | `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954` | **E2R-1** (ratified 28 Oct 2026): the stage-1 method-generic contract schema and acceptance list; owner decisions D-1..D-11 (its section 14); source-tree, retirement and release policy (its section 12A) |\n'
     '| `Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md` | `07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a` | **NAMES-1** (ratified 28 Oct 2026; installed at `52ebeaa`): the one-off rename to stable file names; OPEN-N1..N3 decided (register v0.8) |\n'
     '| `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` | `d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a` | **E1-ALIGN** (design ratified 28 Oct 2026, with E1A-D1..D3; code not yet authorised): E_1 into the per-method layout; the symbol-aware firewall |')
line('**Register v0.6, installed with this file, supersedes v0.5.**',
     '**Register v0.9, installed with this file, supersedes v0.8.** A register cannot contain its own hash; v0.9\'s is in that installation\'s manifest. Registers v0.4-v0.8 are history. Use whichever edition is current.')
sub("register v0.2-v0.5; TIE v0.1;", "register v0.2-v0.8; TIE v0.1;")

# ---- Section 5.3 ----
line('- **A method-generic runtime contract replaces the E_1-specific conventions before E_2**',
     """- **A method-generic runtime contract replaces the E_1-specific conventions before E_2** (Architecture 20A; R2 5.6 stage-1 fields). Its design is **E2R-1 v0.3r3, owner-ratified 28 October 2026**; its code is the E_2-readiness package (section 9). The owner decisions recorded in its section 14:
  - D-1: `track_id` excludes the method revision; each report uses one declared revision per track.
  - D-2: synthetic and benchmark records carry the evidence tier `NOT_EVIDENCE`.
  - D-3: plain-English method texts for E_1 and E_2 are written in the E_2-readiness package.
  - D-4: `src/` holds current code only, with stable names (no version in file names), and a folder per method, `src/methods/E_<nnn>/`, which is a locator only; the scientific identity stays `E_n`.
  - D-5: a superseded revision moves to `archive/methods/E_<nnn>/r<k>/` (helpers to `archive/common/<name>/r<k>/`) with a README; no commit IDs, no stored hashes, no run-time code-identity recording; exact historical replay is not promised.
  - D-6: a method runs only if its active registry entry is `SUPPORTED` for its current revision **and** no `IN_DEVELOPMENT.txt` is present; release is the owner's two deliberate actions. Not yet implemented: it arrives with the E_2-readiness code.
  - D-7: NAMES-1 before the E_2-readiness code (now with E1-ALIGN between them; E1A-D2).
  - D-8: prospective results are shown both "as published" and "current methods".
  - D-9 to D-11: a seed policy's root is a pre-announced NIST Randomness Beacon pulse, fetched once by hand and verified; runs never fetch; roots may be switched as a new revision or variant, and every root tried is logged and counted; a root published after historical targets may be used for retrospective development runs, labelled as experiment randomisation, but a real forecast needs an already-approved root. **Carried forward to the seed-policy package:** keep a dated copy of each pulse-selection rule; reject any beacon response for a different pulse.
- **Layout (OPEN-N1 = A, owner 28 October 2026):** each method's entry file stays directly in `src/methods/` (`E_<nnn>_<Name>.py`), as the Option F wrapper requires; its folder `src/methods/E_<nnn>/` holds its method-specific modules and its `IN_DEVELOPMENT.txt` flag, created when its code first arrives. OPEN-N2: the owner's data tools and legacy test scripts keep their names for now. OPEN-N3: the stable test names of NAMES-1 section 3.
- **E1-ALIGN (design ratified 28 October 2026):** moves `canonical_bytes` and the length-prefixed tuple encoding into `_common/canonical_encoding.py` (so the shared reader no longer imports E_1 code) and E_1's five modules into `src/methods/E_001/`; keeps E_1's tie code with E_1; widens the import firewall to method folders with exact, counted, symbol-aware allowances; adds a six-encoder byte-equality guard. E1A-D1: E_1 stays revision 1 under its own structural exception; E1A-D2: NAMES-1, then E1-ALIGN, then the E_2-readiness code; E1A-D3: E_001's entry-file exemption is kept.""")

# ---- Section 5.4 ----
line('- **Architecture 2:** one standalone `.py` per method',
     '- **Architecture 2:** one standalone `.py` entry file per method (`src/methods/E_###_name.py`), with its method-specific modules in its folder (layout above), shared reviewed `_common/` modules (no shared process or mutable state), a small coordinator.')
sub("Never invoke the installer as part of an offline test.",
    "Never invoke the installer as part of an offline test. **Python (owner, 28 October 2026):** the venv went from 3.14.8 to 3.14.10 (`venv --upgrade`; no package changed), then to a new **3.15.2** venv (`py -3.15 -m venv .venv`; every package a ready-built wheel; versions as in section 7.1). The 3.14.10 venv is kept as `venv.bak` (Git ignores `venv.bak/`, but not names such as `.venv314`), with Python 3.14 installed, as the fallback; the free-threaded 3.14t was removed. The owner's data tools have not yet been run under 3.15; treat their first run as a first run.")

# ---- Section 6 ----
sub("- Line endings: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`.",
    "- Line endings: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`. `git archive` applies the `.bat` rule, so a `.bat` file's archived bytes are CRLF while its Git blob is LF: hash `.bat` files from `git show`. The owner's checkout uses `core.autocrlf=true` (Git warns \"LF will be replaced by CRLF\" when staging); it converts CRLF text to LF at commit.\n"
    "- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).** The project's text reads without an explicit encoding only touch ASCII JSON and CSV test data; all 79 tests pass on 3.15.2 (OWNER-REPORTED, 28 October 2026). The committed static firewall test reads method files with an explicit `utf-8`.")

# ---- Section 7.1: module map, suite, results ----
sub("| `src/methods/_common/game_profiles_v1.py` |", "| `src/methods/_common/game_profiles.py` |")
sub("| `src/methods/_common/game_draws_reader_v1.py` |", "| `src/methods/_common/game_draws_reader.py` |")
sub("| `src/methods/_common/e1_common_reader_bridge_v1.py`, `multigame_e1_v1.py` |", "| `src/methods/_common/e1_common_reader_bridge.py`, `multigame_e1.py` |")
sub("| `src/methods/_common/multigame_method_registry_v1.py`, `multigame_standalone_contract_v1.py`, `multigame_coordinated_manifest_v1.py` |",
    "| `src/methods/_common/multigame_method_registry.py`, `multigame_standalone_contract.py`, `multigame_coordinated_manifest.py` |")
sub("| `src/methods/_common/multigame_console_protocol_v1.py`, `multigame_worker_launch_handshake_v1.py` |",
    "| `src/methods/_common/multigame_console_protocol.py`, `multigame_worker_launch_handshake.py` |")
sub("| `src/methods/_common/multigame_ancestry_release_v1.py`, `src/coordinator_private/multigame_coordinator_exit_receipt_v2.py` |",
    "| `src/methods/_common/multigame_ancestry_release.py`, `src/coordinator_private/multigame_coordinator_exit_receipt.py` |")
sub("| `src/Powerball_Experiment_Coordinator.py`, `src/coordinator_private/multigame_launch_spec_v1.py` |",
    "| `src/Powerball_Experiment_Coordinator.py`, `src/coordinator_private/multigame_launch_spec.py` |")
sub("| `src/coordinator_private/multigame_windows_lifecycle_v1.py` |", "| `src/coordinator_private/multigame_windows_lifecycle.py` |")
sub("| `src/methods/_common/multigame_synthetic_scorer_v1.py`, `multigame_result_registry_v1.py`, `src/methods/POC_MultiGame_Synthetic_Worker.py` |",
    "| `src/methods/_common/multigame_synthetic_scorer.py`, `multigame_result_registry.py`, `src/methods/POC_MultiGame_Synthetic_Worker.py` |")
sub("**Module map** (from ADD-2 section 1; read the code itself before changing it):",
    "**Module map** (from ADD-2 section 1, with the stable names NAMES-1 gave at `52ebeaa`; NAMES-1 section 3 maps old to new; read the code itself before changing it):")
line('**Offline suite command**',
     '**Offline suite commands** (from the repository root, Linux shell form; Windows uses `;` in `PYTHONPATH`). The 60-test standard suite:')
line('`PYTHONPATH=src:src/methods:tests python -m unittest -v tests.test_multigame_v011_reader_contracts',
     '`PYTHONPATH=src:src/methods:tests python -m unittest -v tests.test_multigame_reader_contracts tests.test_multigame_static_and_timing tests.test_multigame_launch_and_manifest tests.test_multigame_exit_receipt tests.test_multigame_science_allowlist tests.test_multigame_console_and_synthetic_scorer tests.test_t05_hardening`\n'
     'The other 19 current tests: `PYTHONPATH=src:src/methods:tests python -m unittest -v tests.test_e1_standalone tests.test_multigame_windows_lifecycle_review`. Both are offline; the lifecycle-review module never starts a Windows process, and the E_1 standalone module uses invented CSVs in temporary folders. The NAMES-1 package\'s `RUN_NAMES1_SUITE.py` (in `exchange/EX_012_Claude/NAMES1_Code_Install_v1.zip`) runs all nine modules one by one and compares each with its expected count.')
line('Result at `c542483` (six modules):',
     'Result at `c542483` (six modules): 58 OK, 1 skip. At `52ebeaa` (all 79 current tests): Linux (Claude; Python 3.13.17, NumPy 2.5.3) 79 OK, 0 skipped; Windows (owner-reported, 28 October 2026) 79 OK on Python 3.14.10 and again on Python 3.15.2 (NumPy 2.5.4, SciPy 1.18.1, psutil 7.2.2), each with 2 skips: the reader-contracts symlink subtest and the exit-receipt symlink test, because the account cannot create symlinks (the hard-link subtest runs). Read every test before running it; its name or an "offline" label is not proof that it is safe (agreed position 8.2).')
sub("- Older optionals still open: resolved-path containment under `source_data`; a full review of `multigame_windows_lifecycle_v1.py` before any lifecycle gate.",
    "- Older optionals still open: resolved-path containment under `source_data`; a full review of `multigame_windows_lifecycle.py` before any lifecycle gate.\n"
    "- **A known gap (found in review, 28 October 2026; register v0.8):** the committed static import-firewall test (`test_method_loader_import_firewall_except_accepted_legacy_e1`) reads only the module part of `from X import Y`, so a method file using `from _common import game_draws_reader` would pass it. No current method uses that form. E1-ALIGN closes it; until then, Claude's review of every code package checks for that form by hand.")
sub("Python 3.14 beyond the offline suite (the owner ran the suite on 3.14.8; Claude runs 3.13)",
    "Python 3.15 beyond the offline suite (the owner ran all 79 tests on 3.15.2 at `52ebeaa`; Claude runs 3.13), the owner's data tools under 3.15")

# ---- New 7.1B and 7.1C before 7.2 ----
sub("### 7.2 Powerball E_1 (accepted; frozen)",
    """### 7.1B NAMES-1 - ACCEPTED and COMMITTED at `52ebeaa`

- **Scope:** the one-off rename of 27 versioned files (18 runtime modules, 9 current test modules) to stable names, with exactly the 94 allowlisted substitutions in 27 files (82 imports, 2 `mock.patch` targets, 7 file-name literals, 2 negative firewall literals, 1 docstring; `review/NAMES1_Code_Install_v1/names1_allowlist.tsv`). No behaviour, schema, identity or golden changed; E_1 stays revision 1 (N1-R03). The eleven protected coordinator functions are AST-identical to v0.6.
- **One visible record effect (N1-R01B):** a coordinator exit receipt keys `contract_modules_sha256` by the two contract files' names, so a receipt issued before NAMES-1 no longer verifies and is refused; none is converted or bypassed.
- **Installed** in one commit with the NAMES-1 v0.2 specification, the E1-ALIGN v0.2r1 specification, register v0.8 and the review history. The verifier pinned base `908db9e`; it treated six history files the owner had committed early (`2c76664`) as guarded. Owner's Windows run (Python 3.14.10): PRE, 27 renames, 42 files copied, POST, 79 tests (2 symlink skips), 63 import-origin and firewall checks, staging (27 R, 3 M, 15 A), COMMITTED PASS before push. A first attempt stopped at PRE (three downloads saved under `review/`) and was undone and restarted cleanly. Claude verified from GitHub: COMMITTED PASS; 42 A, 27 D, 3 M without rename detection; manifest `9d8664f38c33ee374ace06d29d98a4d84477af9199359e22bfcef84e1897f6a7`; and in a disposable clone `git revert` restored the pre-NAMES-1 tree exactly and the old suite passed.
- **Reviews:** design R-3 of v0.1 and the PASS recheck of v0.2; code review `review/Independent_ChatGPT_NAMES1_Code_Review_v0_1.md` (N1I-C01, install order), its recheck (EX_009), the final-candidate recheck (EX_011) and the final ZIP's mechanical check (EX_013, PASS). The final install ZIP is `exchange/EX_012_Claude/NAMES1_Code_Install_v1.zip` (`8548415c05688b788c0b9c9711bf670fd4afed64018f5c0617fc3a40811bfd9c`).

### 7.1C DOC-2 - installed at `908db9e` (two commits; owner-accepted exception)

- The E2R-1 specification v0.3r3 and register v0.7. Four of the package's eight files were already committed by the owner (`2c76664`, merged `f300f2d`), byte-identical; `908db9e` added the other four. The installer's PRE, POST and COMMITTED phases STOPPED (the last only on its one-commit rule; its blob check had passed for all eight). Claude confirmed byte identity before the owner pushed, and verified all eight files from GitHub. The owner accepted the two-commit delivery as a one-off exception (register v0.8); a STOP remains a STOP.

### 7.2 Powerball E_1 (accepted; frozen)""")
sub("- `src/methods/E_001_Historical_Appearance_Frequency.py` with `_common/e1_historical_appearance_frequency_v0_3.py`, `e1_training_view_v0_1.py`, `e1_standalone_contract_v0_1.py`; tests `tests/test_p3_e1_standalone_v0_1.py` and `tests/p3_e1_synthetic_v0_3.json`.",
    "- `src/methods/E_001_Historical_Appearance_Frequency.py` with `_common/e1_historical_appearance_frequency.py`, `e1_training_view.py`, `e1_standalone_contract.py` (stable names since NAMES-1; E1-ALIGN will move them to `src/methods/E_001/`); tests `tests/test_e1_standalone.py` and `tests/p3_e1_synthetic_v0_3.json` (a frozen fixture; its name is kept).")

# ---- Section 8.6: lessons ----
sub("Give every revision a distinct ZIP and folder name, name the exact folder in the commands, ask the owner to clear superseded extracted folders, and read the install log's paths before saying it is safe to commit.",
    """Give every revision a distinct ZIP and folder name, name the exact folder in the commands, ask the owner to clear superseded extracted folders, and read the install log's paths before saying it is safe to commit.
- **Push before the committed check** (the reviewer's N1I-C01): earlier install instructions pushed first, so a wrong commit could have been published before the check stopped it. Commit, check, then push (section 1.6). The fix caught the DOC-2 deviation before anything was pushed.
- **The owner sometimes saves files into the repository** (EX files and ZIPs under `review/`, or history files committed early). A verifier's PRE then STOPs. Tell the owner to save downloads outside the repository (for example `E:\\TEMP`) and to say before committing anything outside a package. When a phase STOPs and later steps were run anyway, undo and restart from PRE rather than continuing.
- **Static import guards must be symbol-aware.** E1-ALIGN v0.1 and v0.2 each missed a form the reviewer found: `from _common import game_draws_reader` (E1A-B01) and `from methods import E_001` (E1A2-C01). Check the module **and** every imported name, count textual mentions too, and add a mutation test for each counterexample. The same gap exists in the committed firewall test (section 7.1).
- **Prove "nothing else changed" with a frozen, exact allowlist** of (old block, new block) edits applied to the predecessor and compared byte for byte, not with regex categories such as "looks like an import" (E1A-C01).
- **Count before claiming.** The E1-ALIGN proposal claimed three encoder copies; there are six.
- **Hashes:** a ZIP hash retyped into a paste block was wrong twice in one message. Compute every hash with a tool and copy it.
- **Shell pitfalls:** `open(p,'wb').write(open(p,'rb').read())` truncates the file before reading it; an unquoted heredoc expands backticks (`` `name` `` became empty); `git archive` converts `.bat` files to CRLF; `rm -rf` of the shell's own working directory breaks later commands.
- **A new folder the ratified tests did not foresee** (`exchange/`, whose files deliberately contain old names) needs an exemption; flag such exemptions to the reviewer rather than deciding them silently.""")

# ---- Section 9 ----
line('1. **Done:** the first package under the new roles',
     '1. **Done:** TH-1 (`744afea`); DOC-1 (`be18548`); the E2R-1 specification v0.3r3 (ratified 28 October 2026) and DOC-2 (`908db9e`); NAMES-1 (`52ebeaa`); the E1-ALIGN design v0.2r1 (ratified 28 October 2026); Python 3.15.2 (28 October 2026).')
line('2. **Next: the E_2-readiness specification**',
     '2. **Next: DOC-3**, this file (H-1 v1r3) and register v0.9, which records the NAMES-1 commit and the move to Python 3.15. The reviewer may also refresh H-2. Then **the E1-ALIGN code package** (HIGH; it needs the owner\'s authorisation): rebase the ratified v0.2r1 trial (`exchange/EX_008_Claude/`: `apply_e1align.py`, `test_e1_align.py`, `e1align_checks.py`, `e1align_allowlist.json`) on the installed NAMES-1 tree (its `src/` and `tests/` are byte-identical to the trial\'s base); add the verifier and the install package in the NAMES-1 pattern; independent code RECHECK; the owner\'s Windows run of all 84 tests.')
line('3. **E_2-readiness offline code**, after that ratification:',
     '3. **E_2-readiness stage-1 offline code**, after E1-ALIGN (E2R-1 v0.3r3 is ratified): schema types and validators; registry status and the D-6 admission rule; per-channel probability-kind validators; IS capability as a declaration only; separate product, mode and score status; per-track provenance on the orchestration side; the scorer-only post-outcome record type with no data path; a migration rule; the D-3 method texts for E_1 and E_2. Synthetic fixtures and the development prefix only; review with R-2 reproduction and an R-4 T-05 oracle. The seed-policy package follows when a method needs seeds.')
sub("6. **Owner decision still open from the agreed position (section 11):** whether to scope the oracle prototypes. (The transport choice was decided on 27 October 2026; section 1.6.)",
    "6. **Owner decision still open from the agreed position (section 11):** whether to scope the oracle prototypes. (The transport choice was decided on 27 October 2026; section 1.6.)\n"
    "7. **Housekeeping, owner's choice:** the first run of the data tools under Python 3.15; later, delete `venv.bak` and uninstall Python 3.14; a later owner-scoped tidy-up of the owner tools' and legacy tests' versioned names (OPEN-N2, deferred).")

# ---- Section 10 ----
sub("no orphan-marker clearance by any chat.",
    "no orphan-marker clearance by any chat; no commit by Claude outside `exchange/`.")

# ---- Appendix A ----
sub("| Committed coordinator v0.6 (AST anchor) |",
    "| H-1 v1r2 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r2.md`, `55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0` |\n"
    "| H-2 v1r3 (current reviewer handover) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md`, `a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1` |\n"
    "| Claude checkpoint v4 | `doc/HANDOVER/Claude_Checkpoint_v4.md`, `d7634683d3d40edaa27c91576531cb198f1358613ca84c2e67e42096a1a6456e` |\n"
    "| Exchange protocol v0.3 | `exchange/README.md` at `262a2c4`, `a20589e5c5bdeed043e78815f86b1a71679426f17528aedfb14aef7d72ed10ef` |\n"
    "| NAMES-1 install manifest | `review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `9d8664f38c33ee374ace06d29d98a4d84477af9199359e22bfcef84e1897f6a7` |\n"
    "| DOC-2 install manifest | `review/DOC2_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `c3b373a3222d716963a1894ccc9d84f5737fa4af673d74b1fca18fdf1c39f8a0` |\n"
    "| Committed coordinator v0.6 (AST anchor) |")
sub("`744afea` TH-1 installed; `b14116b` review-disposition procedure; the commit installing this file (recorded externally).",
    "`744afea` TH-1 installed; `b14116b` review-disposition procedure; `be18548` DOC-1 (H-1 v1r2, H-2 v1r3, register v0.6); `319fd11` and `38fc60e` snapshots (E2R-1 review history, checkpoint v4); `6891196`, `06a672f` and `262a2c4` the exchange README v0.1-v0.3; `2c76664` (merged `f300f2d`) ten history files committed by the owner; `908db9e` DOC-2; `52ebeaa` NAMES-1; exchange records EX_001..EX_014 in `exchange/` (up to `83d1515`); the commit installing this file (recorded externally).")

# ---- Appendix C ----
sub("*End of H-1.*",
    """## Appendix C. Changes in v1r3 (records refresh DOC-3)

v1r3 is v1r2 with the following changes and nothing else; the exact diff travels with the DOC-3 package.

1. Header, section 0 and Appendix A: the baseline is NAMES-1 at `52ebeaa`; the reading list adds the exchange protocol, the three new specifications and the newest EX files; new identities and commits.
2. Section 1.1 and section 10: Claude commits and pushes inside `exchange/` only.
3. Section 1.5: the oversight instruction, extended indefinitely with reporting by exception.
4. Section 1.6: the phone exchange protocol; CRLF and LF identities; LF copies under `review/`; commit, check, then push; `git pull --ff-only` first; already-committed files.
5. Section 2: the EX file replaces the paste block on a phone; hashes are never retyped.
6. Section 3 and section 5.4: Python 3.15.2, the fallback, the data tools not yet run under 3.15.
7. Section 4: register v0.8 and the E2R-1, NAMES-1 and E1-ALIGN specifications; register v0.9 installed with this file.
8. Section 5.3: E2R-1 decisions D-1..D-11, the layout (OPEN-N1..N3), E1-ALIGN and E1A-D1..D3.
9. Section 6: archived `.bat` bytes, the owner's `core.autocrlf=true`, Python 3.15's UTF-8 default.
10. Section 7: the stable module names; the 60 + 19 suite commands and results on 3.14.10 and 3.15.2; the known firewall gap; new sections 7.1B (NAMES-1) and 7.1C (DOC-2); E_1's file names.
11. Section 8.6: eight lessons from 28 October 2026.
12. Section 9: the done list; DOC-3, E1-ALIGN code, E_2-readiness code; housekeeping.

*End of H-1.*""")

assert t.endswith('\n') and all(ord(c) < 128 for c in t)
open(out, 'wb').write(t.encode('ascii'))
print(out, hashlib.sha256(t.encode()).hexdigest(), count, 'edits', len(t.splitlines()), 'lines')
