"""Final mechanical edits for the AI roles transition install (Claude, 27 Oct 2026).

Owner ratification, 27 October 2026: H-1 v1r1, H-2 v1r2 (with R-8..R-11 and section 3.1),
H-3 v1r1 and register v0.5, with these edits: C-FINAL-01 (H-2 v1r2 path and hash; H-1/H-3
hashes); [RECHECK] filled; the owner's oversight instruction in H-1 1.5 and H-3 7; register
statuses OWNER-RATIFIED; the H-2 footer erratum recorded in the register. H-2 itself is
installed byte-for-byte as received. Every replacement is counted; inserted text is ASCII.
Usage: python3 -I finalise_transition.py H1_v1r1 H3_v1r1 REGISTER_v0_5 H2_v1r2 OUT_DIR
"""
import sys, hashlib
from pathlib import Path

h1_in, h3_in, rg_in, h2_in, out = map(Path, sys.argv[1:6])
out.mkdir(parents=True, exist_ok=True)
D = '27 October 2026'
H2SHA = hashlib.sha256(h2_in.read_bytes()).hexdigest()
assert H2SHA == '53f3af3f0845ea8534e25e896ffc8790fe685a7df9ecad8f7d7e48cd53f234a2', H2SHA

OVERSIGHT = ("**Owner instruction, 27 October 2026:** for the first three reviews under the new roles "
             "(the owner may change the number), Claude's response to each review lists every item the "
             "reviewer marked REVIEWER-DECIDED, checks each against the ratified compliance, safety and "
             "process rules (holdout and data boundaries, risk tiers and required reviews, test and evidence "
             "requirements, gates), and flags to the owner in plain English any that departs from them, "
             "naming the rule. This is reporting only: Claude does not overrule the reviewer or narrow its "
             "rights; the owner decides.")


def load(p):
    b = p.read_bytes().decode('utf-8')
    return b.replace('\r\n', '\n')


def apply(text, edits, name):
    for old, new, n in edits:
        c = text.count(old)
        assert c == n, f'{name}: expected {n} of {old[:70]!r}, found {c}'
        bad = sorted({ch for ch in new if ord(ch) > 127})
        assert not bad, f'{name}: non-ASCII inserted {bad!r}'
        text = text.replace(old, new)
    return text


h1 = apply(load(h1_in), [
    ("H-2 also proposes R-8..R-11 (problem framing, evidence sufficiency, declining unsafe tests, material findings outside a narrow scope) for the owner's ratification; whatever the owner ratifies binds equally.",
     "H-2 also sets out R-8..R-11 (problem framing, evidence sufficiency, declining unsafe tests, material findings outside a narrow scope); the owner ratified them with H-2 on 27 October 2026, and they bind equally.", 1),
    (" Expect REVIEWER-DECIDED labels in its reviews.",
     " Expect REVIEWER-DECIDED labels in its reviews (H-2 section 3.1).\n- " + OVERSIGHT, 1),
], 'H-1')

h3 = apply(load(h3_in), [
    ("applied in v1r1 `[RECHECK]`)",
     "applied in v1r1; focused recheck PASS, `review/Independent_ChatGPT_Focused_Recheck_Claude_Transition_Docs_v1r2.md`)", 1),
    ("H-2 v1r1 (`0f9a8a98a8a56231e2730891ed71f1d2ed0b4afb890458de94b03f61c45668b5`) applied all six;",
     "H-2 v1r1 (`0f9a8a98a8a56231e2730891ed71f1d2ed0b4afb890458de94b03f61c45668b5`) applied all six; H-2 v1r2 (`53f3af3f0845ea8534e25e896ffc8790fe685a7df9ecad8f7d7e48cd53f234a2`) added section 3.1, recording the owner's reviewer-latitude decision (Claude's fact check: `review/Claude_Fact_Check_H2_v1r2_v1.md`, PASS with one footer erratum);", 1),
    ("the owner alone will check and ratify its rights section)",
     "the owner alone checked and ratified its rights section, including R-8..R-11, on 27 October 2026)", 1),
    ("| `doc/HANDOVER/Claude_Primary_Handover_H1_v1r1.md` (or a later reviewed revision) | H-1 |",
     "| `doc/HANDOVER/Claude_Primary_Handover_H1_v1r1.md` | H-1 |", 1),
    ("| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r1.md` (or a later reviewed revision) | H-2 |",
     "| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r2.md` | H-2 |", 1),
    ("| `doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` (or a later reviewed revision) | H-3 |",
     "| `doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` | H-3 |", 1),
    ("(H-1 section 1.5).\n",
     "(H-1 section 1.5).\n5. " + OVERSIGHT + "\n6. Owner ratification, 27 October 2026: H-1 v1r1, H-2 v1r2 (including R-8..R-11 and section 3.1), H-3 v1r1 and register v0.5, with the final mechanical edits recorded in `review/AI_Transition_Install_v1/`.\n", 1),
], 'H-3')

H1SHA = hashlib.sha256(h1.encode('ascii')).hexdigest()
H3SHA = hashlib.sha256(h3.encode('ascii')).hexdigest()

rg = apply(load(rg_in), [
    ('**Register version:** v0.5 RATIFICATION CANDIDATE (27 October 2026), recording',
     f'**Register version:** v0.5 OWNER-RATIFIED {D}, recording', 1),
    ('| `HANDOVER/Claude_Primary_Handover_H1_v1r1.md` | Claude; reviewed by the ChatGPT reviewer chat | RATIFICATION CANDIDATE; `[H1-SHA]` |',
     f'| `HANDOVER/Claude_Primary_Handover_H1_v1r1.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 27 Oct 2026; `{H1SHA}` |', 1),
    ('| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r1.md` | ChatGPT reviewer chat; facts checked by Claude; rights section checked by the owner alone | RATIFICATION CANDIDATE; `[H2-SHA]` |',
     f'| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r2.md` | ChatGPT reviewer chat; facts checked by Claude; rights section checked by the owner alone | OWNER-RATIFIED 27 Oct 2026, including R-8..R-11 and section 3.1; `{H2SHA}`. Erratum: its closing line reads "End of H-2 v1r1 DRAFT"; the file is v1r2 and is installed unchanged. |', 1),
    ('| `HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` | Claude; facts checked by the ChatGPT reviewer chat | RATIFICATION CANDIDATE; `[H3-SHA]` |',
     f'| `HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` | Claude; facts checked by the ChatGPT reviewer chat | OWNER-RATIFIED 27 Oct 2026; `{H3SHA}` |', 1),
    ('| `RATIFICATION_REGISTER_v0_4.md` | OWNER-RATIFIED 27 Oct 2026; superseded by this register when it is ratified |',
     '| `RATIFICATION_REGISTER_v0_4.md` | OWNER-RATIFIED 27 Oct 2026; superseded by this register (v0.5, OWNER-RATIFIED 27 Oct 2026) |', 1),
    ('Claude as author keeps only routine choices that affect no scope, acceptance or review gate.',
     'Claude as author keeps only routine choices that affect no scope, acceptance or review gate. **Owner instruction, 27 October 2026:** for the first three reviews under the new roles, Claude checks every REVIEWER-DECIDED item against the ratified compliance, safety and process rules and flags any departure to the owner; reporting only (H-1 section 1.5). The transition documents below carry their authoring-time "DRAFT" headers; this register records their ratification.', 1),
], 'register')
assert '[H1-SHA]' not in rg and '[H2-SHA]' not in rg and '[H3-SHA]' not in rg and '[RECHECK]' not in h3

(out / 'Claude_Primary_Handover_H1_v1r1.md').write_bytes(h1.encode('ascii'))
(out / 'AI_Roles_Transition_Record_H3_v1r1.md').write_bytes(h3.encode('ascii'))
(out / 'RATIFICATION_REGISTER_v0_5.md').write_bytes(rg.encode('utf-8'))
(out / 'ChatGPT_Reviewer_Handover_H2_v1r2.md').write_bytes(h2_in.read_bytes())
print('H-1', H1SHA); print('H-2', H2SHA); print('H-3', H3SHA)
print('register v0.5 (external manifest only)', hashlib.sha256(rg.encode('utf-8')).hexdigest())
