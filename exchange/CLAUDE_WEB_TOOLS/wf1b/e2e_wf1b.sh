#!/bin/bash
# WF-1B install end-to-end test in disposable clones (Claude, Linux, 31 Oct 2026).
# Usage: e2e_wf1b.sh REPO PKGDIR WORKDIR [PYTHON]   (REPO: a frozen clone of main at the package's base)
set -u
REPO=$1; P=$2; W=$3; PY=${4:-python3}
rm -rf "$W"; mkdir -p "$W"; cd "$W"
VE=$P/VERIFY_WF1B_INSTALL.py
V() { python3 -I "$VE" --repo . --phase "$1" 2>&1 | grep -E 'PASS|STOP' | head -1; }
fresh() { cd "$W"; rm -rf r; if [ "$1" = crlf ]; then git clone -q -c core.autocrlf=true "$REPO" r; else git clone -q "$REPO" r; fi; cd r; git config user.email t@t; git config user.name t; }
overlay() { cp -r "$P/repo_overlay/." .; if [ "$1" = crlf ]; then (cd "$P/repo_overlay" && find . -type f ! -name '*.bat') | while read -r f; do perl -pi -e 's/\n/\r\n/' "$f"; done; fi; }
echo "base: $(git -C "$REPO" rev-parse HEAD)  python: $($PY --version)"
for MODE in lf crlf; do
  echo "== $MODE: WF-1B happy path"; fresh $MODE
  V pre; overlay $MODE; V post
  $PY -I $P/RUN_WF1B_SUITE.py --repo . | tail -3
  git add .gitignore Run_Method_Rankings.bat doc review src tests 2>/dev/null
  echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git commit -q -m WF1B 2>/dev/null; V committed
  echo "status after: '$(git status --porcelain --untracked-files=all | head -3)'"
done
echo "== negatives (each must STOP)"
fresh lf; echo x > stray.txt; echo "-- pre, an untracked file:"; V pre
fresh lf; overlay lf; echo '# x' >> src/evaluation/report.py; echo "-- post, a new file with wrong bytes:"; V post
fresh lf; overlay lf; rm tests/test_wf1b_static.py; echo "-- post, a new file missing:"; V post
fresh lf; overlay lf; echo '# x' >> src/methods/_common/walk_forward.py; echo "-- post, an unexpected change:"; V post
fresh lf; overlay lf; git add -A; git commit -q -m x; echo "-- committed, a stray file committed too:"; echo y > stray2.txt; git add stray2.txt; git commit -q --amend -m x; V committed
cd "$W"; cp -r "$P" dmg; echo x >> dmg/repo_overlay/src/evaluation/numerics.py; fresh lf; echo "-- damaged package:"; python3 -I "$W/dmg/VERIFY_WF1B_INSTALL.py" --repo . --phase pre 2>&1 | grep STOP | head -1
echo end
