import re, sys, hashlib, subprocess
R='/home/claude/analysing_perceived_randomness_in_reality/exchange/CLAUDE_WEB_TOOLS/simplify/'
def section(text, n, nxt):
    i=text.index('\n## %s. '%n)+1; j=text.index('\n## %s. '%nxt)+1; return text[i:j]
def rep_ws(s, old, new):
    pat=r'\s+'.join(re.escape(w) for w in old.split())
    m=re.findall(pat, s); assert len(m)==1, (len(m), old[:70])
    return re.sub(pat, lambda _: new, s)
# ---- specification
old=open(R+'SYSTEM_SPECIFICATION_DRAFT_v0_3.md').read(); t=open('spec_v0_4_template.md').read()
s1=section(old,1,2); s6=section(old,6,7); s8=section(old,8,9)
s8n=rep_ws(s8,"A forecast is scored once, when its target's result is on file.",
  "A forecast is scored at most once, when its target's result is on file, and\nnever if its variant is withdrawn from that draw (section 11).")
for k,v in (('1',s1),('6',s6),('8',s8n)):
    m='@@KEEP %s@@\n'%k; assert t.count(m)==1; t=t.replace(m,v)
assert '@@' not in t
new=t; open(R+'SYSTEM_SPECIFICATION_DRAFT_v0_4.md','w',newline='\n').write(new)
assert section(new,1,2)==s1 and section(new,6,7)==s6
# ---- deployment
old=open(R+'DEPLOYMENT_DESIGN_DRAFT_v0_9.md').read(); t=open('deploy_v0_10_template.md').read()
d1=section(old,1,2); d10=section(old,10,11); d11=section(old,11,12); d12=section(old,12,13); d14=section(old,14,15)
d1n=rep_ws(d1,"[cold_backup] root = T:\\a_p_r_i_r_cold","").replace("copy_from = G:\\a_p_r_i_r\n    \n","copy_from = G:\\a_p_r_i_r\n")
d1n=re.sub(r'(copy_from = G:\\a_p_r_i_r\n)\s*\n(\*\*A QA or PROD)', r'\1\n\2', d1n)
d10n=rep_ws(d10,"`PRE_INFRA`, `POST_INFRA`, `PRE_VERIFY` or `POST_VERIFY`. Every one is complete.",
  "`PRE_INFRA`, `POST_INFRA`, `PRE_REPLACE`, `POST_REPLACE`, `RERUN`, `PRE_VERIFY` or `POST_VERIFY`. Every one is complete,\n  and every one is an attempt whose result is reported as it is.")
d10n=rep_ws(d10n,"- Nothing prunes a backup root. The owner copies PROD's backup root to other media himself.",
  "- Nothing prunes a backup root. The owner copies PROD's backup root to other media himself.\n- `Check_Tree.bat <role>` lists, read-only, the full path, size and date of every backup ZIP in that tree's backup root.\n  It verifies none of them, and no install asks for it (owner, entry 136).")
d11n=rep_ws(d11,"written at every creation, install and reinstall, for the software state that results.",
  "written at every creation, install, reinstall and QA software\nreplacement, for the software state that results. If it cannot be written, that is said and asked about (default\nNO); it is never a stop by itself (owner, entry 136).")
d14n=rep_ws(d14,"""3. **Infrastructure.** `src\\evaluation\\reports.py` is improved and `Make_Installable.bat INFRA` run.
   `Reinstall_Infra.bat PROD` shows one file to overwrite and no variant; one confirmation; `PRE_INFRA`; the file
   replaced; the suite; the full regression finds no difference; `POST_INFRA`. Had the change altered one old
   forecast, the install would have stopped there with no job able to run, and `PRE_INFRA` would be restored. Trying
   it in QA first would have shown the same without touching PROD.""",
"""3. **Infrastructure.** `src\\evaluation\\reports.py` (class `derived`) is improved and `Make_Installable.bat INFRA` run.
   `Reinstall_Infra.bat PROD` shows one file to overwrite and no variant; on a temporary copy it recomputes every
   score and the prevailing ledger and says "No stored result changes"; the kit is written and the `PRE_INFRA` backup
   made, and both are reported; the warning; the owner types YES; the file is replaced; the checks in place;
   `POST_INFRA`. Trying it in QA first would have shown the same without touching PROD, and is never required.""")
d14n=rep_ws(d14n,"and a new `FORWARD_FROM`.","and a new eligibility draw in the variant's status file.")
d14n=rep_ws(d14n,"""nothing installed is touched. He withdraws the
   twelve old variants in PROD with one command and one confirmation, and unmarks them in DEV. The next research job
   fills the successors' history; the old variants keep their records up to the withdrawal.""",
"""nothing installed is touched. **Nothing has
   withdrawn the twelve old variants:** they go on running beside their successors. When the owner decides to, he
   withdraws them in PROD with one command and one confirmation, and unmarks them in DEV. The next research job
   fills the successors' history; the old variants keep their records up to the withdrawal.""")
d14n=rep_ws(d14n,"a test bed: it can be restored to an earlier backup or created again; PROD is not affected either way.",
  "the owner's laboratory: its software can be replaced from PROD's, it can be restored to an earlier backup, or it can\n   be created again; PROD is not affected either way.")
for k,v in (('1',d1n),('10',d10n),('11',d11n),('12',d12),('14',d14n)):
    m='@@KEEP %s@@\n'%k; assert t.count(m)==1; t=t.replace(m,v)
assert '@@' not in t
t=t.replace("Sections 11 and 12 are byte-identical to\nv0.9; sections 1, 10 and 14 are v0.9's with the counted changes the diff shows; the rest is rewritten.",
            "Section 12 is byte-identical to v0.9;\nsections 1, 10, 11 and 14 are v0.9's with the counted changes the diff shows; the rest is rewritten.")
assert "Section 12 is byte-identical" in t
open(R+'DEPLOYMENT_DESIGN_DRAFT_v0_10.md','w',newline='\n').write(t)
assert section(t,12,13)==d12
for f in ('SYSTEM_SPECIFICATION_DRAFT_v0_4.md','DEPLOYMENT_DESIGN_DRAFT_v0_10.md'):
    b=open(R+f,'rb').read(); bad=[(i,c) for i,c in enumerate(b) if c>127]
    print(f, len(b), 'bytes', 'ASCII' if not bad else 'NONASCII at %s'%bad[:3], 'LF' if b'\r' not in b else 'CR', 'longest line', max(len(l) for l in b.split(b'\n')))
