import re, subprocess, hashlib
H1="doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md"
t=subprocess.run(["git","show","HEAD:"+H1],capture_output=True).stdout.decode().split("\n")
# all blobs at HEAD plus the two historical ones H-1 names
blobs=set()
for p in subprocess.run(["git","ls-tree","-r","--name-only","HEAD"],capture_output=True).stdout.decode().split("\n"):
    if p and not p.startswith(("source_data/","results/","transitory_data/")):
        blobs.add(hashlib.sha256(subprocess.run(["git","show","HEAD:"+p],capture_output=True).stdout).hexdigest())
for ref in ["63c19e7:exchange/README.md","423bd19:CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md"]:
    blobs.add(hashlib.sha256(subprocess.run(["git","show",ref],capture_output=True).stdout).hexdigest())
excluded_lines={310,311,325}  # 7.3 computed digests, 7.5 masters
tot=ok=exc=0; bad=[]
for i,l in enumerate(t,1):
    for h in re.findall(r'`([0-9a-f]{64})`',l):
        tot+=1
        if i in excluded_lines: exc+=1
        elif h in blobs: ok+=1
        else: bad.append((i,h[:12]))
print(f"64-hex values quoted in H-1: {tot}; excluded by rule: {exc}; matched a committed blob: {ok}; unmatched: {bad}")
