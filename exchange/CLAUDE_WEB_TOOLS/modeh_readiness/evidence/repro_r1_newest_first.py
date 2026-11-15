"""Reproduce the owner's FAIL of 15 November 2026 on INVENTED data: the reviewed check (blob 1cbd3294...) against a
stand-in browser whose page lists the nine draws NEWEST FIRST. No website; invented masters in a temporary folder."""
import sys, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
import gov_fetch_parse_smoke_devtest as DT
with tempfile.TemporaryDirectory() as td:
    root = DT.build(Path(td)); sys.path.insert(0, str(root / "src"))
    import results_master_v0_2 as RM
    RM.PAGE_WAIT_SECONDS, RM.WAIT_POLL_SECONDS = 1.0, 0.2
    def newest_first(g):
        blocks = DT.page(RM, root, g).split("\nDraw ")
        blocks = [blocks[0]] + ["Draw " + b for b in blocks[1:]]
        return "\n".join(reversed(blocks))
    rc, out = DT.run(root, driver=DT.FakeDriver({g: newest_first(g) for g in DT.PROFILES}))
    print(out, end=""); print("EXIT", rc)
