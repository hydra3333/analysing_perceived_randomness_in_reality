"""Build the system specification DRAFT v0.2 from DRAFT v0.1 by counted replacements (the owner's decision of
21 November 2026, 13:18: the readiness marker alone for PROD; QA optional). Usage: python3 -I make_spec_v0_2.py IN OUT CLOCK"""
import hashlib, re, sys
src, out, clock = sys.argv[1:4]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '70cc8e708ab508747ce29ec9106eb9b0ea948020b42f32a0de440dcdd0c67e6d'
s = raw.decode('ascii')
def one(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
def part(a, b, new):
    global s
    assert s.count(a) == 1 and s.count(b) == 1, (s.count(a), a[:50], s.count(b), b[:50])
    i, j = s.index(a), s.index(b); assert i < j; s = s[:i] + new + s[j:]

one('research system - DRAFT v0.1\n', 'research system - DRAFT v0.2\n')
one('**Status:** DRAFT v0.1 for independent review.', '**Status:** DRAFT v0.2 for independent review (v0.1 with the owner\'s decision of 21 November 2026, 13:18, on installing:\nsections 0, 2, 12, 13, 16, 18, 19; `SPEC_v0_1_TO_v0_2.diff` is exact).')
s, n = re.subn(r'\*\*Written:\*\* .*? Australia/Adelaide', f'**Written:** {clock} Australia/Adelaide', s, count=1); assert n == 1
one('(decision log entries 121, 122 and 124;', '(decision log entries 121, 122, 124 and 126;')
one('**Companion:** the deployment design DRAFT v0.7', '**Companion:** the deployment design DRAFT v0.8')
one('4. **Installing is two steps and nothing more:** install into QA, where the tests run by themselves; then install the\n   very same files into PROD. **PROD refuses anything that has not passed in QA, byte for byte. There is no way\n   round that.** Shared system code is updated by a separate command, under the same rule.',
    '4. **Installing needs one thing: the marker.** `Install.bat PROD` adds every marked variant PROD lacks, checks it in\n   place and asks for one confirmation. **QA is your own test bed:** install there first whenever you want to look\n   before PROD; nothing requires it and nothing compares the two. Shared system code is updated by a separate\n   command, with a marker of its own.')
one('| Purpose | write and try methods; build installs | prove an install before PROD | the research |',
    '| Purpose | write and try methods; build installs | the owner\'s own test bed: try an install first, when he chooses | the research |')

part('## 12. Installing (owner;', '## 13. The Python environment', '''## 12. Installing (owner; EX_262 F08, F10; the owner's decision of 21 November 2026, 13:18)

**12.1 Two kinds of install, never mixed.**
- **`Install.bat PROD` (or `QA`): new variants only.** It finds every ready variant in DEV (section 4) that the target
  does not hold, shows the exact batch (variants, helper files, and what it left out and why), and adds those folders
  and any helper files that are new. `--only` narrows the batch. It never overwrites: a variant the target already
  holds is left alone even if DEV's copy has changed (changed science is a new variant), and a helper the target
  holds with different bytes is a refusal. Nothing to add ends at once, with the target untouched. For PROD the
  owner types **one** confirmation for the whole batch; nothing is confirmed per variant or activated afterwards.
- **`Reinstall_Infra.bat PROD` (or `QA`): infrastructure only** (12.4).

**12.2 What an install requires: the readiness marker, and nothing from QA (owner).**
- **The record of the decision.** At 12:54 on 21 November 2026 the owner required a successful QA verification of the
  exact files before every PROD installation, with no bypass (DRAFT v0.1 of this document designed that). At 13:18 he
  replaced it: "I am seeking an abbreviated QA mechanism that satisfies only me, and so I'd prefer revert to only
  using 'i am installable' marker in dev for installing to prod."
- **So:** a variant is installed into PROD on the strength of its marker in DEV. There is no QA pass record, no
  comparison of PROD with QA, and no required order between them.
- **QA is the owner's own test bed.** The same commands work on it. He installs a batch there when he wants to run it
  and read its reports before PROD. The system neither requires that nor checks whether it was done. QA and PROD are
  each installed from DEV and know nothing of each other.
- **What still protects PROD, with no ceremony:** the marker is bound to the files' content, so a variant edited after
  marking is not installable until it is marked again; installed variants and helpers are never overwritten; the
  install checks itself in the tree it installs into (12.3); a complete backup is taken first; one confirmation.
- **Infrastructure has a marker of the same kind:** `deploy\\INFRA_IS_INSTALLABLE.json`, made by
  `Make_Installable.bat INFRA`, listing every file of the infrastructure manifest and of the install tool with its
  hash. Any later edit to one of them un-readies it (choice F, section 19).

**12.3 What every install checks by itself, in the tree it installs into** (QA and PROD alike).
1. The structure: markers match; declarations valid; the import check; add-only kept.
2. The whole test suite, run with that tree's own Python on a temporary copy; tests are never installed.
3. **Regression of what was already there:** forecasts and scores of installed variants are recomputed from the tree's
   own canonical files and must be identical in content. After a variant install: a fixed sample. After an
   infrastructure change: every forecast and every score of every variant.
A failure stops the install with its barrier in place, so no job runs. The ways out are the same command after the
cause is corrected, or the backup taken just before.

**12.4 Infrastructure** (owner: REINSTALL INFRA).
- **What it is:** the files named, one per line, in `deploy/INFRA_MANIFEST.txt`: the reader, the readout, the list and
  job code, scoring, reports, OV-1, the guard, backup and restore, the launchers and the owner's four environment
  scripts. Nothing is infrastructure unless it is on the list; a test requires the list to hold every project module
  those files import. **Not on it, and never installed outside DEV:** documents, the exchange, tests, Git files,
  unmarked variants, DEV's results, the settings files, and the proof-of-concept coordinator and probes.
- `Reinstall_Infra.bat` shows every file it would add, overwrite or remove, with both hashes and the differences, and
  touches nothing under a family folder or `_shared/`. One confirmation for PROD.
- **An infrastructure change that alters any earlier forecast or score is a scientific change, not maintenance.** The
  full regression (12.3, 3) then fails in the target, the install stops, and the tree goes back to the backup taken
  just before. The way forward is a separately reviewed correction or new variants, never this command. Trying it
  in QA first costs PROD nothing; that is what the test bed is for.

**12.5 Creating a tree: `Init_Tree.bat QA|PROD`.** For a root that does not exist or is empty. It writes the tree's
`ENVIRONMENT.ini`; installs the infrastructure and every ready variant; copies the accepted results (QA: from PROD, or
from DEV while no PROD exists; PROD: from DEV, the first time); stops for the owner to build the environment with his
scripts; verifies it; takes the first backup. No result, score or report is ever copied into a new tree.

**12.6 Installation is release** (owner). The next research job finds the new variants and fills their history.

''')
one('then QA rebuilt and verified, which gives a new QA pass; the reviewer\n  sees both; then PROD: a backup, the rebuild, `Verify_Tree.bat PROD`.',
    'the reviewer sees it; then PROD: a backup,\n  the rebuild, `Verify_Tree.bat PROD`. Rebuilding and verifying QA first is the owner\'s option.')
one('that is a separate decision by the owner, through QA like any other.', 'that is a separate decision by the owner, by an ordinary install.')
one('| DEV | `Make_Installable.bat` | mark a finished variant ready |', '| DEV | `Make_Installable.bat` | mark a finished variant, or the infrastructure, ready |')
one('| DEV | `Install.bat QA`, then `Install.bat PROD` | add new variants |', '| DEV | `Install.bat PROD` (or `QA`) | add new variants |')
one('| DEV | `Reinstall_Infra.bat QA`, then `PROD` | update infrastructure |', '| DEV | `Reinstall_Infra.bat PROD` (or `QA`) | update infrastructure |')
one('"not the QA-tested\nbytes: <file>" (run the QA step again); "already installed with different bytes" (give the changed work a new variant\nname, or return QA to its backup from before that install and install again);',
    '"marker does not match\nits files" (finish the work and run `Make_Installable.bat` again); "already installed with different bytes" (changed\nwork needs a new variant name);')
one('`Init_Tree.bat PROD`; PROD\'s first job.', '`Init_Tree.bat PROD`; PROD\'s first job. (QA is recommended here so that the check is made before PROD exists; it is\n  not required, and the check can equally be made in PROD before PROD is declared in use.)')
part('- **Readiness and installing (F08 to F10; the QA rule), with the examples of EX_262:**', '- **Roles (F09):**',
'''- **Readiness and installing (F08 to F10), with the examples of EX_262:** two ready variants and one unfinished in DEV:
  `Install.bat` adds the two only; one is edited afterwards: its marker no longer matches and it is left out by name
  until marked again; a hand-made marker with a wrong hash is not ready; an import not on the helper list is not
  ready; a helper present with other bytes refuses; an existing variant is never overwritten; QA and PROD installed
  independently, in either order; `Reinstall_Infra.bat` changes one listed file and no variant; the infrastructure
  marker stale after an edit; an infrastructure change that alters one old forecast stops at the regression and no
  job runs; an install stopped at every step, then the command again; nothing half-installed is ever run; no tool
  or launcher writes a settings file after its creation.
''')
one('- **E. Nothing is copied back from PROD to DEV or Git**', '- **F. A readiness marker for infrastructure** as 12.2 (recommended: the same deliberate act as for a variant, and it\n  stops half-edited system code being installed by accident). Or none: the shown differences and the confirmation\n  are the whole of it.\n- **E. Nothing is copied back from PROD to DEV or Git**')
one('2. Is 12.2 a faithful and sufficient form of the owner\'s QA rule? Is check 4 (every PROD variant is in the QA pass)\n   right, or stricter than needed?',
    '2. With QA optional by the owner\'s decision (12.2), do the markers and the install\'s own checks in the target (12.3)\n   protect enough against an accident? Is the full regression in PROD at an infrastructure reinstall proportionate?')
one('| The owner, 21 November 2026: QA before every PROD installation, exact files, no bypass | 12.2, 12.3; deployment design section 3 |',
    '| The owner, 21 November 2026, 13:18: the marker alone for PROD; QA optional (replaces his 12:54 rule) | 12.2, 12.3; deployment design section 3 |\n| The owner\'s question: how settings files are made and kept from being overwritten | deployment design section 1 |')
one('End of the specification, DRAFT v0.1.', 'End of the specification, DRAFT v0.2.')
s.encode('ascii')
for w in ('QA pass', 'QA-tested', 'five checks', 'check 4', 'bypass'):
    print(repr(w), [l[:90] for l in s.split('\n') if w in l])
open(out, 'w', encoding='ascii', newline='\n').write(s); print(len(s.splitlines()), hashlib.sha256(s.encode()).hexdigest())
