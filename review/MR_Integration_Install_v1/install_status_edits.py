"""Installation status edits for the ratified method-ranking integration (owner ratification 27 Oct 2026).

Applies an exact list of (old, new, expected_count) replacements to the v3 candidate editions and
writes the installed editions. Every old string must occur exactly expected_count times; every
inserted character is ASCII. Then recomputes the four governed-document hashes and writes them into
the register. Usage: python3 -I install_status_edits.py DRAFT_DIR OUT_DIR
"""
import sys, hashlib
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
R3 = 'Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md'
R2 = 'Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md'
AR = 'Predictive_Randomness_Software_Architecture_Discussion_v0_8.md'
PR = 'Predictive_Randomness_Research_Project_Proposal_v0_6.md'
RG = 'RATIFICATION_REGISTER_v0_4.md'
D = '27 October 2026'
NORM_OLD = 'These constraints are normative in R2 v0.4 (data/views) and R3 v0.4 (evaluation/freeze).'
NORM_NEW = 'These constraints are normative in R2 v0.5 (data/views) and R3 v0.5 (evaluation/freeze).'
UNTIL = ', awaiting owner ratification; until then {p} governs, except that the owner-ratified Method Ranking Measures Proposal v0.5 already governs its own subject.**'

EDITS = {
  R3: [
    # E1 header: version, date, status
    ('**Version:** 0.5 RATIFICATION CANDIDATE (26 October 2026): R3 v0.4',
     f'**Version:** 0.5 OWNER-RATIFIED {D} (drafted 26 October 2026): R3 v0.4', 1),
    ('**Date:** 26 October 2026 (v0.5 candidate; v0.4 ratified 26 October;',
     f'**Date:** {D} (v0.5 drafted 26 October, ratified 27 October; v0.4 ratified 26 October;', 1),
    ('**Status:** RATIFICATION CANDIDATE, awaiting owner ratification. Until then R3 v0.4 governs, except that the owner-ratified Method Ranking Measures Proposal v0.5 already governs its own subject.',
     f'**Status:** OWNER-RATIFIED {D}; R3 v0.4 is historical.', 1),
    # E2 header: present-authority lines
    ('**Governing project charter:** Owner-ratified consolidated Proposal v0.5 (26 October 2026).',
     f'**Governing project charter:** Owner-ratified consolidated Proposal v0.6 ({D}); Proposal v0.5 remains historical.', 1),
    ('Owner-ratified consolidated R2 v0.4 (26 October 2026); R2 v0.3 remains historical.',
     f'Owner-ratified consolidated R2 v0.5 ({D}); R2 v0.4 and R2 v0.3 remain historical.', 1),
    # E3 section 0.1 present-authority rows
    ('| Proposal v0.5 (consolidated) | Project charter and owner decisions | OWNER-RATIFIED 26 Oct 2026; v0.4 historical |',
     '| Proposal v0.6 (consolidated) | Project charter and owner decisions | OWNER-RATIFIED 27 Oct 2026; v0.5 and v0.4 historical |', 1),
    ('| R2 v0.4 (consolidated) | Training cutoffs',
     '| R2 v0.5 (consolidated) | Training cutoffs', 1),
    ('numerical contracts | OWNER-RATIFIED 26 Oct 2026; v0.3 historical |',
     'numerical contracts | OWNER-RATIFIED 27 Oct 2026; v0.4 and v0.3 historical |', 1),
    ('| RATIFICATION CANDIDATE; v0.4 OWNER-RATIFIED 26 Oct 2026; no Mode H/FINAL authority |',
     '| OWNER-RATIFIED 27 Oct 2026; v0.4 historical; no Mode H/FINAL authority |', 1),
    # E4 section 17.13 stage 0
    ('integration into the governing documents is in progress (R3 v0.5, R2 v0.5, Architecture v0.8, Proposal v0.6, register v0.4). No code. Package 2 v0.11 proceeds unchanged in parallel.',
     f'it is integrated into R3 v0.5, R2 v0.5, Architecture v0.8, Proposal v0.6 and register v0.4, owner-ratified {D}. No code. Package 2 v0.11 proceeded unchanged in parallel.', 1),
  ],
  R2: [
    ('**Version:** 0.5 RATIFICATION CANDIDATE (26 October 2026): R2 v0.4',
     f'**Version:** 0.5 OWNER-RATIFIED {D} (drafted 26 October 2026): R2 v0.4', 1),
    ('**Edition status: RATIFICATION CANDIDATE' + UNTIL.format(p='R2 v0.4'),
     f'**Edition status: OWNER-RATIFIED {D}; R2 v0.4 is historical.**', 1),
    ('**Governing charter:** Owner-ratified consolidated Proposal v0.5 (26 October 2026).',
     f'**Governing charter:** Owner-ratified consolidated Proposal v0.6 ({D}); Proposal v0.5 remains historical.', 1),
    (NORM_OLD, NORM_NEW, 1),
  ],
  AR: [
    ('**Version:** 0.8 RATIFICATION CANDIDATE (26 October 2026): Architecture v0.7',
     f'**Version:** 0.8 OWNER-RATIFIED {D} (drafted 26 October 2026): Architecture v0.7', 1),
    ('**Edition status: RATIFICATION CANDIDATE' + UNTIL.format(p='Architecture v0.7'),
     f'**Edition status: OWNER-RATIFIED {D}; Architecture v0.7 is historical.**', 1),
    ('and this Architecture v0.7 were owner-ratified 26 October 2026.',
     f'and Architecture v0.7 were owner-ratified 26 October 2026; their method-ranking integration editions, Proposal v0.6, R2 v0.5, R3 v0.5 and this Architecture v0.8, were owner-ratified {D}.', 1),
    (NORM_OLD, NORM_NEW, 1),
    # section 0.2 present-authority rows
    ('| Project Proposal v0.5 consolidated OWNER-RATIFIED | Charter/philosophy; v0.4 historical |',
     '| Project Proposal v0.6 consolidated OWNER-RATIFIED | Charter/philosophy; v0.5 and v0.4 historical |', 1),
    ('| R2 v0.4 consolidated OWNER-RATIFIED |', '| R2 v0.5 consolidated OWNER-RATIFIED |', 1),
    ('contract; v0.3 + approved erratum record historical |',
     'contract; v0.4, v0.3 + approved erratum record historical |', 1),
    ('| R3 v0.4 consolidated OWNER-RATIFIED | Evaluation/holdout/scoring; v0.3 historical |',
     '| R3 v0.5 consolidated OWNER-RATIFIED | Evaluation/holdout/scoring; v0.4 and v0.3 historical |', 1),
    ('| Architecture v0.7 consolidated OWNER-RATIFIED | Runtime and protected safety contracts; v0.6 historical |\n'
     '| Architecture v0.8 (this edition) | RATIFICATION CANDIDATE: v0.7 plus the method-ranking integration; protected 5C unchanged |',
     '| Architecture v0.8 (this edition) consolidated OWNER-RATIFIED | Runtime and protected safety contracts; v0.7 plus the method-ranking integration; protected 5C unchanged; v0.7 and v0.6 historical |', 1),
  ],
  PR: [
    ('## Comprehensive project proposal \u2014 v0.6 RATIFICATION CANDIDATE (26 October 2026)',
     f'## Comprehensive project proposal \u2014 v0.6 OWNER-RATIFIED {D} (drafted 26 October 2026)', 1),
    ('**Edition status: RATIFICATION CANDIDATE' + UNTIL.format(p='Proposal v0.5'),
     f'**Edition status: OWNER-RATIFIED {D}; Proposal v0.5 is historical.**', 1),
    ('which superseded Proposal v0.4) plus that integration.',
     'which superseded Proposal v0.4) plus the integration of the owner-ratified Method Ranking Measures Proposal v0.5.', 1),
    ('R2 v0.4 governs experimental inputs', 'R2 v0.5 governs experimental inputs', 1),
    ('R3 v0.4 governs evaluation, freeze and reporting; Architecture v0.7 governs runtime/safety',
     'R3 v0.5 governs evaluation, freeze and reporting; Architecture v0.8 governs runtime/safety', 1),
    ('The specified consolidated governing editions were **owner-ratified on 26 October 2026**.',
     f'The specified consolidated governing editions were **owner-ratified on 26 October 2026**, and their method-ranking integration editions on {D}.', 1),
    (NORM_OLD, NORM_NEW, 2),
  ],
  RG: [
    ('**Register version:** v0.4 RATIFICATION CANDIDATE (26 October 2026), adding',
     f'**Register version:** v0.4 OWNER-RATIFIED {D} (drafted 26 October 2026), adding', 1),
    ('Its content is integrated into the four editions below; once they are ratified, the file is integrated history, kept unchanged.',
     'Its content is integrated into the four editions below, owner-ratified 27 Oct 2026; the file is integrated history, kept unchanged.', 1),
    ('OWNER-RATIFIED 26 Oct 2026; superseded by this register when it is ratified |',
     'OWNER-RATIFIED 26 Oct 2026; superseded by this register (v0.4, OWNER-RATIFIED 27 Oct 2026) |', 1),
    ('**Integration editions (RATIFICATION CANDIDATES, awaiting owner ratification).**',
     f'**Integration editions (OWNER-RATIFIED {D}).**', 1),
    ('| Candidate edition (path under `doc/`) | Ratified predecessor |',
     '| Integration edition (path under `doc/`) | Ratified predecessor |', 1),
    ('| RATIFICATION CANDIDATE; adds', '| OWNER-RATIFIED 27 Oct 2026; adds', 4),
    ('**On owner ratification:** the installation step',
     f'**On owner ratification (given {D}):** the installation step', 1),
    ('**Upon owner ratification**, the operative editions are',
     f'**Upon owner ratification** (given {D}), the operative editions are', 1),
  ],
}

def ascii_only(s, what):
    bad = sorted({c for c in s if ord(c) > 127} - {'\u2014'})
    assert not bad, f'non-ASCII inserted in {what}: {bad!r}'

texts = {}
for name, edits in EDITS.items():
    t = (src / name).read_bytes().decode('utf-8')
    assert '\r' not in t and t.endswith('\n') and not t.endswith('\n\n'), name
    for old, new, n in edits:
        c = t.count(old)
        assert c == n, f'{name}: expected {n} of {old[:60]!r}, found {c}'
        # every character in new that is not in old must be ASCII (the em dash is carried, not inserted)
        ascii_only(new.replace('\u2014', ''), name)
        t = t.replace(old, new)
    texts[name] = t
    print(f'{name}: {sum(e[2] for e in edits)} replacements applied')

# recompute the four governed-document hashes in the register
reg = texts[RG]
for name, v3hash in ((R3, 'e80356aadb72f52c6e695bb30960d32923ae1c9820bc759df1d6675567353c2e'),
                     (R2, '62d1c9c99e7dd33fe5c2496615229d5a67e09d3c6f6b68ada2146b60999e53da'),
                     (AR, 'd27115e095e309fc1e6d68099ee397432f561a7cb51eee722522a85493203875'),
                     (PR, 'ee552a5b530b38604e7b8b8129e5c1ba9485cbe423658e4f5d73bbd9d8b52349')):
    h = hashlib.sha256(texts[name].encode('utf-8')).hexdigest()
    assert reg.count(v3hash) == 1, (name, reg.count(v3hash))
    reg = reg.replace(v3hash, h)
    print(f'{name}: {v3hash[:8]} -> {h}')
texts[RG] = reg

for name, t in texts.items():
    (out / name).write_bytes(t.encode('utf-8'))
print(f'{RG}: {hashlib.sha256(reg.encode("utf-8")).hexdigest()}  (external manifest only)')
