"""Build the system specification DRAFT v0.3 (from v0.2) and the deployment design DRAFT v0.9 (from v0.8) by counted
replacements: the owner's decisions of 21 November 2026, 14:49 to 15:08 (decision log entry 127).
Usage: python3 -I make_v0_3_v0_9.py CLOCK"""
import hashlib, re, sys
clock = sys.argv[1]
def build(src, out, want, edits):
    raw = open(src, 'rb').read(); assert hashlib.sha256(raw).hexdigest() == want, src
    s = raw.decode('ascii')
    for a, b in edits:
        assert s.count(a) == 1, (src, s.count(a), a[:70]); s = s.replace(a, b)
    s, n = re.subn(r'\*\*Written:\*\* .*? Australia/Adelaide', f'**Written:** {clock} Australia/Adelaide', s, count=1); assert n == 1
    s.encode('ascii'); open(out, 'w', encoding='ascii', newline='\n').write(s)
    print(out, len(s.splitlines()), hashlib.sha256(s.encode()).hexdigest())

build('SYSTEM_SPECIFICATION_DRAFT_v0_2.md', 'SYSTEM_SPECIFICATION_DRAFT_v0_3.md', '33cbc41bf041724e733d541ad0c8971ae578eaf61eedbe353e1ccf66c80342d9', [
 ('research system - DRAFT v0.2\n', 'research system - DRAFT v0.3\n'),
 ('**Status:** DRAFT v0.2 for independent review (v0.1 with the owner\'s decision of 21 November 2026, 13:18, on installing:\nsections 0, 2, 12, 13, 16, 18, 19; `SPEC_v0_1_TO_v0_2.diff` is exact).',
  '**Status:** DRAFT v0.3 for independent review. v0.2 was v0.1 with the owner\'s decision of 13:18 on 21 November 2026 on\ninstalling; v0.3 adds his decisions of 14:49 to 15:08 (helpers stay add-only with no in-place update; three DEV\nconveniences; the infrastructure marker; the manifest\'s name): sections 3.3, 4, 11, 12, 16, 18, 19. The diffs\n`SPEC_v0_1_TO_v0_2.diff` and `SPEC_v0_2_TO_v0_3.diff` are exact.'),
 ('(decision log entries 121, 122, 124 and 126;', '(decision log entries 121, 122, 124, 126 and 127;'),
 ('**Companion:** the deployment design DRAFT v0.8', '**Companion:** the deployment design DRAFT v0.9'),
 ('Prefer code inside the variant\'s folder.',
  'Prefer code inside the variant\'s folder.\n\n**3.3A No in-place update of a helper (owner, 21 November 2026).** An installed helper is never overwritten, whether\nor not the change would alter results. A helper found to be wrong is corrected by a new file (`..._v2.py`) and a\n**successor variant** for each variant that used it; the old variants are withdrawn by the owner (section 11) and\ntheir markers removed in DEV. The successors are new variants and begin their own place in the prevailing OV-1. Code\nthat is expected to keep improving without changing any result belongs in the infrastructure (12.4), which can be\nupdated under its "nothing may change" check.'),
 ('is set aside automatically (5.6).',
  'is set aside automatically (5.6).\n- **Three DEV conveniences** (owner; they touch nothing outside DEV). `Who_Uses.bat <helper>` lists every variant whose\n  declaration names that helper. `Make_Successors.bat <old helper> <new helper>` copies each such variant to a new\n  folder with the next version number in its name and rewrites its helper reference and declaration; it marks\n  nothing, and the owner reviews the result. `Make_Installable.bat` accepts several variants at once, and\n  `--unmark` removes markers.'),
 ('The owner tells the reviewer the reason in the ordinary exchange.', 'The owner tells the reviewer the reason in the ordinary exchange. Several variants can be named in one command,\n  under one confirmation.'),
 ('A newly created tree (section\n  12.5) installs it and runs it until the owner withdraws it there.',
  '**In DEV the owner removes the withdrawn\n  variant\'s marker** (`Make_Installable.bat --unmark`), so that no tree created later receives it.'),
 ('Any later edit to one of them un-readies it (choice F, section 19).', 'Any later edit to one of them, or to the list, un-readies it (owner: yes, 21 November 2026).'),
 ('- **What it is:** the files named, one per line, in `deploy/INFRA_MANIFEST.txt`:', '- **What it is:** the files named, one per line, in `deploy/INFRA_MANIFEST.ini` (the owner\'s name for it; first written\n  with the phase 2 package and reviewed there; afterwards edited by hand to add or remove a file):'),
 ('| DEV | `Make_Installable.bat` | mark a finished variant, or the infrastructure, ready |', '| DEV | `Make_Installable.bat` | mark finished variants, or the infrastructure, ready; `--unmark` |\n| DEV | `Who_Uses.bat`, `Make_Successors.bat` | find the variants that use a helper; prepare their successors |'),
 ('- **Roles (F09):**', '- **Helpers and the DEV conveniences:** no command overwrites an installed helper; `Who_Uses` against planted\n  declarations; `Make_Successors` produces unmarked folders with the new reference and leaves the originals\n  untouched; batch marking, unmarking and withdrawal; an unmarked variant is not installed into a new tree.\n- **Roles (F09):**'),
 ('- **F. A readiness marker for infrastructure** as 12.2 (recommended: the same deliberate act as for a variant, and it\n  stops half-edited system code being installed by accident). Or none: the shown differences and the confirmation\n  are the whole of it.\n', ''),
 ('**For the reviewer.**', '**Decided by the owner since DRAFT v0.2 (decision log entry 127), no longer open:** a readiness marker for the\ninfrastructure (yes); the manifest is `deploy/INFRA_MANIFEST.ini`; helpers stay strictly add-only, with no in-place\nupdate route; a wrong helper is handled by successor variants, with the three DEV conveniences of section 4.\n\n**For the reviewer.**'),
 ('7. Is anything a routine owner needs missing from section 16?', '7. Is anything a routine owner needs missing from section 16?\n8. Any objection to 3.3A (no in-place helper update; successors) or to the three DEV conveniences?'),
 ('| The owner\'s question: how settings files are made and kept from being overwritten | deployment design section 1 |', '| The owner\'s question: how settings files are made and kept from being overwritten | deployment design section 1 |\n| The owner, 21 November 2026, 14:49 to 15:08: infrastructure marker; manifest name; helpers add-only; successors | 3.3A; 4; 11; 12.2; 12.4 |'),
 ('End of the specification, DRAFT v0.2.', 'End of the specification, DRAFT v0.3.'),
])
build('DEPLOYMENT_DESIGN_DRAFT_v0_8.md', 'DEPLOYMENT_DESIGN_DRAFT_v0_9.md', 'e9b88c10802f5a8e35d81df9735382f302a75458ee1dd9bb273b8e7916ac4761', [
 ('# Deployment design - DRAFT v0.8 (', '# Deployment design - DRAFT v0.9 ('),
 ('**Status:** DRAFT v0.8 for independent review (v0.7 with the owner\'s decision of 21 November 2026, 13:18: sections 0, 1,\n2 to 8, 11, 12, 14 to 16; `DEPLOY_v0_7_TO_v0_8.diff` is exact).',
  '**Status:** DRAFT v0.9 for independent review. v0.8 was v0.7 with the owner\'s decision of 13:18 on 21 November 2026; v0.9\nadds his decisions of 14:49 to 15:08 (sections 2, 3 and 14). `DEPLOY_v0_7_TO_v0_8.diff` and `DEPLOY_v0_8_TO_v0_9.diff`\nare exact.'),
 ('specification DRAFT v0.2 and says how', 'specification DRAFT v0.3 and says how'),
 ('(decision log entries 124 and 126).', '(decision log entries 124, 126 and 127).'),
 ('`Check_Tree.bat`, `Cold_Copy.bat`.', '`Check_Tree.bat`, `Cold_Copy.bat`, and the DEV\nconveniences `Who_Uses.bat` and `Make_Successors.bat`.'),
 ('- *Infrastructure:* the files listed in DEV\'s `deploy\\INFRA_MANIFEST.txt`, one path a line, when',
  '- *Infrastructure:* the files listed in DEV\'s `deploy\\INFRA_MANIFEST.ini` (one path a line under `[files]`; first written\n  with the phase 2 package and reviewed; afterwards the owner adds or removes a line by hand), when'),
 ('`Make_Installable.bat INFRA` writes that marker: every manifest file\n  and every file of the install tool, with SHA-256.', '`Make_Installable.bat INFRA` writes that marker: the manifest\n  itself, every file it lists and every file of the install tool, with SHA-256. A listed file that does not exist\n  refuses.'),
 ('## 4. Creating a tree: `Init_Tree.bat QA|PROD`', '**3.4 Helpers are never updated in place (owner).** No command overwrites an installed helper, proved harmless or not.\nA wrong helper is handled in DEV: `Who_Uses.bat` finds the variants that declare it; `Make_Successors.bat` prepares\na successor folder for each, pointing at the corrected file; the owner reviews, marks the batch, and installs it in\nthe ordinary way; he withdraws the old variants in the tree and unmarks them in DEV (example 7).\n\n## 4. Creating a tree: `Init_Tree.bat QA|PROD`'),
 ('## 15. Tests and the rehearsal', '7. **A wrong helper.** `_shared\\recurrence_gaps_v1.py` is found to be wrong. `Who_Uses.bat _shared\\recurrence_gaps_v1.py`\n   lists twelve variants in four families. The owner writes `recurrence_gaps_v2.py` and runs\n   `Make_Successors.bat _shared\\recurrence_gaps_v1.py _shared\\recurrence_gaps_v2.py`: twelve new, unmarked folders\n   (`RECUR_MEAN_ALL_V2` beside `RECUR_MEAN_ALL_V1`, and so on). He reviews them, marks the batch, and runs\n   `Install.bat PROD`: twelve variants and one helper are added; nothing installed is touched. He withdraws the\n   twelve old variants in PROD with one command and one confirmation, and unmarks them in DEV. The next research job\n   fills the successors\' history; the old variants keep their records up to the withdrawal.\n\n## 15. Tests and the rehearsal'),
 ('End of the deployment design, DRAFT v0.8.', 'End of the deployment design, DRAFT v0.9.'),
])
