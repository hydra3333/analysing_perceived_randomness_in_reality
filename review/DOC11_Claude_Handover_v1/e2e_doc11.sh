#!/bin/bash
# DOC-11 install end-to-end test in disposable clones (Claude, Linux, 3 Nov 2026).
# Usage: e2e_doc11.sh REPO PKGDIR WORKDIR   (REPO: a clone of main at or after the package's base)
set -u
REPO=$1; P=$2; W=$3
rm -rf "$W"; mkdir -p "$W"; cd "$W"
VE=$P/VERIFY_DOC11_INSTALL.py
V() { python3 -I "$VE" --repo . --phase "$1" 2>&1 | grep -E 'PASS|STOP' | head -1; }
fresh() { cd "$W"; rm -rf r; if [ "$1" = crlf ]; then git clone -q -c core.autocrlf=true "$REPO" r; else git clone -q "$REPO" r; fi; cd r; git config user.email t@t; git config user.name t; }
overlay() { cp -r "$P/repo_overlay/." .; if [ "$1" = crlf ]; then (cd "$P/repo_overlay" && find . -type f) | while read -r f; do perl -pi -e 's/\n/\r\n/' "$f"; done; fi; }
echo "base: $(git -C "$REPO" rev-parse HEAD)"
for MODE in lf crlf; do
  echo "== $MODE: DOC-11 happy path"; fresh $MODE
  echo "status before: '$(git status --porcelain | head -3)'"
  V pre; overlay $MODE; V post
  git add doc review 2>/dev/null
  echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git commit -q -m DOC11 2>/dev/null; V committed
  echo "status after: '$(git status --porcelain --untracked-files=all | head -3)'"
done
echo "== negatives (each must STOP)"
fresh lf; echo x > stray.txt; echo "-- pre, an untracked file:"; V pre
fresh lf; overlay lf; echo '# x' >> doc/RATIFICATION_REGISTER_v0_24.md; echo "-- post, a new file with wrong bytes:"; V post
fresh lf; overlay lf; rm doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md; echo "-- post, a new file missing:"; V post
fresh lf; overlay lf; echo '# x' >> doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md; echo "-- post, a guarded file changed:"; V post
fresh lf; overlay lf; echo '# x' >> src/evaluation/n1.py; echo "-- post, an unexpected change:"; V post
fresh lf; overlay lf; git add -A; git commit -q -m x; echo "-- committed, a stray file committed too:"; echo y > stray2.txt; git add stray2.txt; git commit -q --amend -m x; V committed
cd "$W"; cp -r "$P" dmg; echo x >> dmg/repo_overlay/doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md; fresh lf; echo "-- damaged package:"; cp -r "$W/dmg/repo_overlay/." .; python3 -I "$W/dmg/VERIFY_DOC11_INSTALL.py" --repo . --phase post 2>&1 | grep -E 'STOP|PASS' | head -1
echo end
