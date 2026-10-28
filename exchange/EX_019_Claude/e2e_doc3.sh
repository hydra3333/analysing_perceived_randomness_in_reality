#!/bin/bash
# DOC-3 install end-to-end test in disposable clones (Claude, Linux). Usage: e2e_doc3.sh REPO PKGDIR WORKDIR
set -u
REPO=$1; PKG=$2; W=$3
rm -rf "$W"; mkdir -p "$W"
V() { python3 -I "$PKG/VERIFY_DOC3_INSTALL.py" --repo . --phase "$1" 2>&1 | grep -E 'PASS|STOP' | head -1; }
LIST=$(grep '^  "' "$PKG/STAGE_EXACT_FILES.cmd" | sed 's/^  "//; s/".*//; s|\\|/|g')
cd "$W"
echo "base: $(git -C "$REPO" rev-parse HEAD)"
for MODE in lf crlf; do
  echo "== $MODE: happy path"
  rm -rf r; if [ $MODE = crlf ]; then git clone -q -c core.autocrlf=true "$REPO" r; else git clone -q "$REPO" r; fi
  cd r; git config user.email t@t; git config user.name t
  V pre
  cp -r "$PKG/repo_overlay/." .
  [ $MODE = crlf ] && for f in $LIST; do case $f in *.md|*.diff|*.txt) sed -i 's/$/\r/' "$f";; esac; done
  V post
  git add -- $LIST 2>/dev/null; echo "staged: $(git diff --cached --name-status | grep -c '^A')"
  git commit -q -m DOC3 2>/dev/null; V committed
  echo "-- negative: pre after the commit"; V pre
  cd ..
done
echo "== negatives before commit"
rm -rf r; git clone -q "$REPO" r; cd r; git config user.email t@t; git config user.name t
echo x > stray.txt; echo "-- pre, untracked file:"; V pre; rm stray.txt
cp -r "$PKG/repo_overlay/." .
echo x > stray.txt; echo "-- post, extra untracked file:"; V post; rm stray.txt
echo >> exchange/README.md; echo "-- post, tracked file modified:"; V post; git checkout -q -- exchange/README.md
echo x >> doc/RATIFICATION_REGISTER_v0_9.md; echo "-- post, wrong bytes:"; V post
cp "$PKG/repo_overlay/doc/RATIFICATION_REGISTER_v0_9.md" doc/
rm review/DOC3_Register_v0_9_candidate_to_final.diff; echo "-- post, missing file:"; V post
cp "$PKG/repo_overlay/review/DOC3_Register_v0_9_candidate_to_final.diff" review/
V post
echo "== negatives after commit"
git add -- $LIST; git commit -q -m DOC3
echo y > extra.txt; git add extra.txt; git commit -q --amend -m DOC3x; echo "-- committed, extra file in the commit:"; V committed
git reset -q --soft HEAD~1; git reset -q; rm extra.txt; git add -- $LIST; git commit -q -m DOC3
echo z > stray.txt; echo "-- committed, untracked file left:"; V committed; rm stray.txt
git rm -q --cached review/DOC3_Register_v0_9_candidate_to_final.diff; git commit -q --amend -m DOC3y; echo "-- committed, one file left out (shown untracked):"; V committed
echo "-- committed STOP prints identities and the do-not-push line:"
python3 -I "$PKG/VERIFY_DOC3_INSTALL.py" --repo . --phase committed 2>&1 | grep -E '^\[|Do NOT push' | tr '\n' ' '; echo
cd ..; rm -rf r
echo "== damaged package"
cp -r "$PKG" dmg; echo x >> dmg/repo_overlay/doc/HANDOVER/Claude_Primary_Handover_H1_v1r3.md
git clone -q "$REPO" r; cd r; python3 -I ../dmg/VERIFY_DOC3_INSTALL.py --repo . --phase pre 2>&1 | grep STOP | head -1
cd ..; rm -rf r dmg
echo "end"
