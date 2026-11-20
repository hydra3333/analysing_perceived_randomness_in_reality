"""Build the deployment design note DRAFT v0.5 from DRAFT v0.4 by counted replacements (EX_255 E04 and its test-oracle
point; the draw-number release fields of the OV-1 amendment v0.2; decision log entry 119).
Usage: python3 -I make_note_v0_5.py V0_4_PATH OUT_PATH CLOCK_TEXT BASE_COMMIT"""
import hashlib, os, sys
src, out, clock, base = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'a339c9c760730b71394b71f334a40854cd7614c05fd5c22f6b02a5fc0647b9fe', 'not the v0.4 bytes sent as EX_254'
s = raw.decode('ascii')
def frag(name): return open(os.path.join(HERE, name), encoding='ascii').read()
def one(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)
def part(start, end, new):
    global s
    assert s.count(start) == 1 and s.count(end) == 1, (s.count(start), start[:50], s.count(end), end[:50])
    a, b = s.index(start), s.index(end); assert a < b
    s = s[:a] + new + s[b:]
def row(first, new):
    global s
    lines = s.split('\n'); hit = [i for i, l in enumerate(lines) if l.startswith(first)]
    assert len(hit) == 1, (len(hit), first[:60])
    lines[hit[0]] = new; s = '\n'.join(lines)

one('# MHUP-B deployment design note - DRAFT v0.4\n', '# MHUP-B deployment design note - DRAFT v0.5\n')
part('**Status:** DRAFT v0.4', '**Reviewer:** the ChatGPT reviewer chat.',
     '**Status:** DRAFT v0.5 for the reviewer\'s recheck. Not ratified. It authorises nothing. It makes the corrections of\n'
     'EX_255 that fall to this note (E04: when a replay after a restore equals the lost score and when it does not; one\n'
     'test oracle) and follows the OV-1 amendment v0.2 (a release record\'s first-draw numbers). EX_255 found the rest of\n'
     'v0.4 broadly sound, and it is unchanged. v0.1 to v0.4 are kept beside it; `NOTE_v0_4_TO_v0_5.diff` is exact.\n'
     f'**Written:** {clock} Australia/Adelaide, by the Claude web chat (primary designer and coder), under the project\n'
     'owner\'s go of 19 November 2026 for the design note (decision log entry 107) and his decisions of entries 116 and 119. Fable (High).\n')
one('**Base:** `main` at `cf46862`;', f'**Base:** `main` at `{base}`;')

# section 0
one('a\n   draw replayed after a restore is counted like any caught-up draw, and the score is the same. The restore notices\n   and the extra stop of v0.3 are withdrawn (section 9).',
    'a\n   draw replayed after a restore is counted like any caught-up draw. The replayed score equals the lost one when the\n   same methods, code and earlier draws are reproduced, and is labelled when they are not (section 9). The restore\n   notices and the extra stop of v0.3 are withdrawn.')

# 4.1
one('the environment against `ENVIRONMENT_VERIFIED.json`; locks and barriers present;',
    'the environment against `ENVIRONMENT_VERIFIED.json`; any release the clone holds that production lacks, with its first-draw numbers and the order of section 9; locks and barriers present;')

# 4.2
one('the release record (MHUP-B\'s has an empty entry list:\n   no roster change).',
    'the release record (MHUP-B\'s has an empty entry list:\n   no roster change; it carries each game\'s first draw, the last draw on file plus one, which is the start of the OV-1\n   score: the OV-1 amendment 2.3).')

# 4.3
one('for a roster change, with an unfinished weekly set: all as now;',
    'for a roster change, with an unfinished weekly set: all as now; for a roster change it also requires the weekly records caught up to the last draw on file, and it writes each game\'s first draw, the last draw on file plus one or a later number given on the command (the OV-1 amendment 2.3);')
one('that record, and production receives the original, with its original date.', 'that record, and production receives the original, with its original date and its original first-draw numbers.')

# section 6
one('- **At `init`:** after the data and the code are in place,',
    '- **The environment is not pinned to a draw** (the owner, entry 119): it "should live with what it receives". A draw\n  computed late runs in whatever environment production then holds; each OV-1 line records that environment\'s digest\n  (section 9). The steps above are how a change is tested, not a rule tying the environment to the draw sequence.\n'
    '- **At `init`:** after the data and the code are in place,')

# section 7
one('That costs time, never research validity, and under\n  the OV-1 amendment it does not change the OV-1 score either (section 9).',
    'That costs time, never research validity. What a replay\n  gives for the OV-1 score is stated in section 9.')

# section 8, after a restore
one('Ordinary work, each step on its usual go: the updater brings the results forward;',
    'Ordinary work, each step on its usual go: `update` first puts back any later release from its saved record (section\n9); the updater brings the results forward;')

# section 9
part('## 9. OV-1 after a restore: nothing special', '## 10. The production guard (D5; EX_248 B06)', frag('note_v0_5_section_9.md'))

# section 12
one('the fresh tree equals the snapshot file for file, environment included, with nothing\n  extra;',
    'the fresh tree is exactly the allowed set of section 8 step 6 (the payload, plus the restore record, plus the orphan\n  evidence file if any, less a live orphan marker), environment included, and one file more or fewer refuses;')
one('- **OV-1 after a restore:** nothing in this layer. The OV-1 amendment\'s own tests show a replay giving the same lines.',
    '- **OV-1 after a restore:** nothing in this layer. The OV-1 amendment\'s own tests show a replay giving the same lines\n  when the cohort is reproduced, and qualified lines when it is not.')
one('an original release record brought back by `update`; a replayed\n  forecast for a draw after that release date is CATCH-UP, never PROSPECTIVE; revisions are not pooled.',
    'an original release record brought back by `update` keeps its first-draw\n  numbers; a replayed forecast for a draw at or above that number is CATCH-UP, never PROSPECTIVE, and below it is\n  development; revisions are not pooled.')

# section 15
row('| C | OV-1 after a restore:', '| C | OV-1 after a restore: no special rule; a replay equals the lost score when the cohort, code and earlier draws are reproduced, and is labelled when not (entries 116, 119) | 9 |\n| - | The environment is not pinned to a draw (entry 119) | 6, 9 |')

# section 17
part('- **A point for the reviewer\'s judgement (labels):**', '- I have not traced every reader of old records',
     '- **Labels after a restore:** `update` brings back the original install and release records (section 4.3), so a\n'
     '  variant keeps its original first-draw numbers, and a replayed forecast for a draw at or above that number is\n'
     '  labelled CATCH-UP as it would have been. No date is consulted (the OV-1 amendment 2.3).\n'
     '- **W-23 and "changing the environment at will".** Section 6 keeps W-23 for every dependency upgrade, as the owner\n'
     '  decided (entry 116). His later words (entry 119) are about not pinning the environment to draws; whether he also\n'
     '  wants W-23 itself lightened is his to say, and would be a rule change for review. This note does not change it.\n')

# section 18
one('## 18. Where each finding of EX_248, EX_250 and EX_252 landed', '## 18. Where each finding of EX_248, EX_250, EX_252 and EX_255 landed')
row('| Section 3, labels |', '| Section 3, labels | A replayed forecast by a variant whose original release was put back | CATCH-UP at or above the release\'s original first draw, never PROSPECTIVE; revisions never pooled; a fixture | 4.3, 12 |')
one('| EX_253 | The owner\'s direction: no restore-specific OV-1 rules | Section 9 replaced; the amendment sent with this note | 9 |\n',
    '| EX_253 | The owner\'s direction: no restore-specific OV-1 rules | Section 9 replaced; the amendment sent with this note | 9 |\n'
    '| EX_255 E04 | "The score is the same after a restore" was said without conditions; the amendment\'s own examples differ | The conditions for equality are stated; differences are labelled by each line\'s standing and investigable by digest; the order (later releases first, then the catch-up); nothing from the set-aside tree | 0, 7, 9 |\n'
    '| EX_255 E01, as it touches this note | A release put back after a restore must not get a newer boundary | The original record returns with its original first-draw numbers; the release step writes the numbers; `check` lists a release production lacks | 4.1, 4.2, 4.3 |\n'
    '| EX_255 section 6, test oracle | A test still said the fresh tree is the snapshot "with nothing extra" | The oracle is the allowed set of section 8 step 6 | 12 |\n')

s.encode('ascii'); assert '\r' not in s
for stale in ('the score is the same', 'nothing\n  extra', 'release date is CATCH', 'AMENDMENT_DRAFT_v0_1'):
    assert stale not in s, stale
open(out, 'w', encoding='ascii', newline='\n').write(s)
print(len(s.splitlines()), 'lines', hashlib.sha256(s.encode()).hexdigest())
