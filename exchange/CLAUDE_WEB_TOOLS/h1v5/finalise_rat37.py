"""RAT-37: finalise H-1 v5 after the owner's ratification of 18 November 2026 (decision log entry 92).
Usage: python3 -I finalise_rat37.py REPO_ROOT HH:MM

Reads the ratified candidate and its blurb from h1v5/out/ (each asserted by SHA-256), changes ONLY the handover's status
line (H-1's own rule, section 9: "Finalising after ratification changes only the status line"), and writes the final
handover, the unchanged blurb and the candidate-to-final diff to h1v5/final/. Writes nothing else.
"""
import difflib, hashlib, os, sys
REPO, WHEN = sys.argv[1], sys.argv[2]
H = os.path.join(REPO, 'exchange', 'CLAUDE_WEB_TOOLS', 'h1v5')
CAND = '22a543df4d5a8e36aaf4e790128a0a279649f9328bde545e1fc6321a218abd55'
BLURB = '11387112c91238cf20ff15b629c5b7bc778ec3f3999685aeea5a1b23f757b8aa'


def rd(name, want):
    b = open(os.path.join(H, 'out', name), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == want, f'{name}: not the bytes the owner ratified'
    return b


s = rd('Claude_Primary_Handover_H1_v5_CANDIDATE.md', CAND).decode('ascii')
blurb = rd('Claude_Primary_Handover_H1_v5_CANDIDATE_introductory_blurb.md', BLURB)
lines = s.split('\n')
old = [l for l in lines if l.startswith('**Status:** CANDIDATE, written on 18 November 2026')]
assert len(old) == 1
new = (f'**Status:** OWNER-RATIFIED 18 November 2026, {WHEN} (RAT-37; record `exchange/DECISIONS/DECISION_LOG.md`, entry 92). '
       'Written on 18 November 2026 at the owner\'s request so that no knowledge is lost if the chat ends, and ratified by '
       'the owner directly: the reviewer was offered a documentary look (EX_236) and has given no ruling on this edition, so '
       'it carries no reviewer PASS. It replaces H-1 v4 (RAT-34), which stays in `doc/HANDOVER/` as history. Committed into '
       '`doc/` by Claude directly; the next register edition (v0.32) records RAT-35, RAT-36 and RAT-37. Finalising changed this '
       'line only: where the text below still says "candidate", "once ratified" or "waiting on the owner: ratifying this '
       'edition", read it with this line. `exchange/CONTINUITY_NOW.md` has the state since (the owner\'s decisions of entry 92 '
       'among them).')
final = s.replace(old[0], new)
assert final.count(new) == 1 and len(final.split('\n')) == len(lines)
final.encode('ascii')
os.makedirs(os.path.join(H, 'final'), exist_ok=True)
out = {'Claude_Primary_Handover_H1_v5.md': final.encode('ascii'), 'Claude_Primary_Handover_H1_v5_introductory_blurb.md': blurb}
for name, data in out.items():
    open(os.path.join(H, 'final', name), 'wb').write(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
diff = ''.join(difflib.unified_diff(s.splitlines(keepends=True), final.splitlines(keepends=True),
                                    'out/Claude_Primary_Handover_H1_v5_CANDIDATE.md', 'final/Claude_Primary_Handover_H1_v5.md', n=0))
open(os.path.join(H, 'final', 'H1_v5_candidate_to_final.diff'), 'wb').write(diff.encode('ascii'))
print('changed lines:', sum(1 for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')))
