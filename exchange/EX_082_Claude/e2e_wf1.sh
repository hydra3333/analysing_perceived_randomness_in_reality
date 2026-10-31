#!/bin/bash
# REL-1 then WF-1A install end-to-end test in disposable clones (Claude, Linux, 31 Oct 2026).
# Usage: e2e_wf1.sh REPO WORKDIR [PYTHON]
#   REPO: a clone at main d15183e (or later exchange-only commits). The WF-1A package is rebuilt in each run with
#   that run's own REL-1 commit as its base, exactly as the final package will be rebuilt after the owner's REL-1 commit.
set -u
REPO=$1; W=$2; PY=${3:-python3}
H=/home/claude/work/wf1code; S=/tmp/claude-0/-home-claude/5e241a26-14db-516d-9aeb-bda4dbe85524/scratchpad
R1=$H/pkg_rel1
rm -rf "$W"; mkdir -p "$W"; cd "$W"
V() { python3 -I "$1" --repo . --phase "$2" 2>&1 | grep -E 'PASS|STOP' | head -1; }
fresh() { rm -rf r; if [ "$1" = crlf ]; then git clone -q -c core.autocrlf=true "$REPO" r; else git clone -q "$REPO" r; fi; cd r; git config user.email t@t; git config user.name t; }
overlay() { cp -r "$1/repo_overlay/." .; if [ "$2" = crlf ]; then (cd "$1/repo_overlay" && find . -type f) | while read -r f; do perl -pi -e 's/\n/\r\n/' "$f"; done; fi; }
FLAGS=$(cd "$S/wf1_base" && ls src/methods/E_0*/IN_DEVELOPMENT.txt | tr '\n' ' ')
echo "base: $(git -C "$REPO" rev-parse HEAD)  python: $($PY --version)"
for MODE in lf crlf; do
  echo "== $MODE: REL-1 happy path"; fresh $MODE
  V $R1/VERIFY_REL1_INSTALL.py pre; overlay $R1 $MODE; git rm -q -- $FLAGS
  V $R1/VERIFY_REL1_INSTALL.py post
  $PY -I $R1/RUN_REL1_SUITE.py --repo . | tail -2
  git add doc review src tests 2>/dev/null; echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git commit -q -m REL1 2>/dev/null; V $R1/VERIFY_REL1_INSTALL.py committed
  REL1=$(git rev-parse HEAD)
  echo "== $MODE: WF-1A happy path (base $REL1)"
  python3 -I $H/build_wf1_pkgs.py wf1a $S/wf1_dev $S/wf1_rel1 "$W/pkg_wf1a_$MODE" $REL1 | tail -1
  P=$W/pkg_wf1a_$MODE
  V $P/VERIFY_WF1A_INSTALL.py pre; overlay $P $MODE
  V $P/VERIFY_WF1A_INSTALL.py post
  $PY -I $P/RUN_WF1A_SUITE.py --repo . | tail -2
  git add .gitignore review src tests 2>/dev/null; echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git commit -q -m WF1A 2>/dev/null; V $P/VERIFY_WF1A_INSTALL.py committed
  echo "status after both: '$(git status --porcelain --untracked-files=all | head -3)'"
  cd ..
done
echo "== negatives"
fresh lf; echo x > stray.txt; echo "-- REL-1 pre, untracked file:"; V $R1/VERIFY_REL1_INSTALL.py pre; rm stray.txt
overlay $R1 lf
echo "-- REL-1 post, flags not deleted:"; V $R1/VERIFY_REL1_INSTALL.py post
git rm -q -- $FLAGS; git rm -q -- src/methods/E_006/contract.py
echo "-- REL-1 post, an extra deletion:"; V $R1/VERIFY_REL1_INSTALL.py post
git reset -q -- src/methods/E_006/contract.py; git checkout -q -- src/methods/E_006/contract.py
echo '# x' >> tests/test_rel1_release.py; echo "-- REL-1 post, new file wrong bytes:"; V $R1/VERIFY_REL1_INSTALL.py post
cp $R1/repo_overlay/tests/test_rel1_release.py tests/
V $R1/VERIFY_REL1_INSTALL.py post; git add doc review src tests; git commit -q -m R
git rm -q src/methods/E_006/beta_bernoulli.py; git commit -q --amend -m Rx; echo "-- REL-1 committed, an extra deletion in the commit:"; V $R1/VERIFY_REL1_INSTALL.py committed
cd ..; rm -rf r
fresh lf; echo "-- WF-1A pre, REL-1 not installed:"; V $W/pkg_wf1a_lf/VERIFY_WF1A_INSTALL.py pre; cd ..; rm -rf r
cp -r "$W/pkg_wf1a_lf" dmg; echo x >> dmg/repo_overlay/src/methods/_common/walk_forward.py; fresh lf; echo "-- WF-1A damaged package:"; python3 -I ../dmg/VERIFY_WF1A_INSTALL.py --repo . --phase pre 2>&1 | grep STOP | head -1; cd ..; rm -rf r dmg
echo end
