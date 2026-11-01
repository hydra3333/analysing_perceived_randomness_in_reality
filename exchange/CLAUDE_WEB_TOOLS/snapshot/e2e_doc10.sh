#!/bin/bash
# DOC-10 install end-to-end test in disposable clones (Claude, Linux, 1 Nov 2026).
# Usage: e2e_doc10.sh REPO PKGDIR WORKDIR   (REPO: a frozen clone of main at the package's base)
set -u
REPO=$1; P=$2; W=$3
rm -rf "$W"; mkdir -p "$W"; cd "$W"
VE=$P/VERIFY_DOC10_INSTALL.py
V() { python3 -I "$VE" --repo . --phase "$1" 2>&1 | grep -E 'PASS|STOP' | head -1; }
fresh() { cd "$W"; rm -rf r; if [ "$1" = crlf ]; then git clone -q -c core.autocrlf=true "$REPO" r; else git clone -q "$REPO" r; fi; cd r; git config user.email t@t; git config user.name t; }
overlay() { cp -r "$P/repo_overlay/." .; if [ "$1" = crlf ]; then (cd "$P/repo_overlay" && find . -type f) | while read -r f; do perl -pi -e 's/\n/\r\n/' "$f"; done; fi; }
restore_results() { git ls-files -z results | xargs -0 rm -f; git -c core.autocrlf=false checkout -- results; }
eolsum() { git ls-files --eol results | awk '{print $2}' | sort | uniq -c | tr '\n' ' '; }
echo "base: $(git -C "$REPO" rev-parse HEAD)"
for MODE in lf crlf; do
  echo "== $MODE: DOC-10 happy path"; fresh $MODE
  echo "results working-copy EOL before: $(eolsum)"
  if [ $MODE = crlf ]; then restore_results; echo "after the restore step: $(eolsum); status '$(git status --porcelain | head -3)'"; fi
  V pre; overlay $MODE; V post
  echo "results EOL after overlay: $(eolsum)"
  git add .gitattributes README.md CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md doc review 2>/dev/null
  echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git commit -q -m DOC10 2>/dev/null; V committed
  echo "status after: '$(git status --porcelain --untracked-files=all | head -3)'"
  echo "results EOL after commit: $(eolsum)"
done
echo "== crlf without the restore step (shows why step 0 exists)"
fresh crlf; echo "results working-copy EOL: $(eolsum)"; V pre; overlay crlf; V post
echo "== negatives (each must STOP)"
fresh lf; echo x > stray.txt; echo "-- pre, an untracked file:"; V pre
fresh lf; overlay lf; echo '# x' >> doc/RATIFICATION_REGISTER_v0_23.md; echo "-- post, a new file with wrong bytes:"; V post
fresh lf; overlay lf; echo '# x' >> README.md; echo "-- post, a replaced file with wrong bytes:"; V post
fresh lf; overlay lf; rm doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md; echo "-- post, a new file missing:"; V post
fresh lf; overlay lf; echo '# x' >> src/evaluation/n1.py; echo "-- post, an unexpected change:"; V post
fresh lf; overlay lf; git add -A; git commit -q -m x; echo "-- committed, a stray file committed too:"; echo y > stray2.txt; git add stray2.txt; git commit -q --amend -m x; V committed
cd "$W"; cp -r "$P" dmg; echo x >> dmg/repo_overlay/doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md; fresh lf; echo "-- damaged package:"; python3 -I "$W/dmg/VERIFY_DOC10_INSTALL.py" --repo . --phase pre 2>&1 | grep STOP | head -1
echo end
