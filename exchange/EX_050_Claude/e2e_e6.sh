#!/bin/bash
# E_6 package install end-to-end test in disposable clones (Claude, Linux). Usage: e2e_e6.sh REPO PKGDIR WORKDIR [PYTHON]
set -u
REPO=$1; PKG=$2; W=$3; PY=${4:-python3}
rm -rf "$W"; mkdir -p "$W"; cd "$W"
V() { python3 -I "$PKG/VERIFY_E6_INSTALL.py" --repo . --phase "$1" 2>&1 | grep -E 'PASS|STOP' | head -1; }
fresh() { rm -rf r; if [ "$1" = crlf ]; then git clone -q -c core.autocrlf=true "$REPO" r; else git clone -q "$REPO" r; fi; cd r; git config user.email t@t; git config user.name t; }
echo "base: $(git -C "$REPO" rev-parse HEAD)  python: $($PY --version)"
for MODE in lf crlf; do
  echo "== $MODE: happy path"; fresh $MODE
  V pre; cp -r "$PKG/repo_overlay/." .
  [ $MODE = crlf ] && (cd "$PKG/repo_overlay" && find . -type f) | while read -r f; do perl -pi -e 's/\n/\r\n/' "$f"; done
  V post
  $PY -I "$PKG/RUN_E6_SUITE.py" --repo . | tail -2
  echo "status lines after the suite: $(git status --porcelain --untracked-files=all | grep -cv '^??') non-new"
  git add doc review src tests 2>/dev/null; echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git commit -q -m E6 2>/dev/null; V committed
  cd ..
done
echo "== negatives"
fresh lf; echo x > stray.txt; echo "-- pre, untracked file:"; V pre; rm stray.txt
cp -r "$PKG/repo_overlay/." .
echo '# x' >> src/methods/_common/game_profiles.py; echo "-- post, existing file modified:"; V post; git checkout -q -- src/methods/_common/game_profiles.py
echo '# x' >> src/methods/E_006/beta_bernoulli.py; echo "-- post, new file wrong bytes:"; V post; cp "$PKG/repo_overlay/src/methods/E_006/beta_bernoulli.py" src/methods/E_006/
echo '{}' > src/methods/_common/contract_data/extra.json; echo "-- post, extra data file:"; V post; rm src/methods/_common/contract_data/extra.json
echo '# x' >> src/methods/Method_Contract_Runner.py; echo "-- post, replaced file wrong bytes:"; V post; cp "$PKG/repo_overlay/src/methods/Method_Contract_Runner.py" src/methods/
V post; git add doc review src tests; git commit -q -m E6
echo y > extra.txt; git add extra.txt; git commit -q --amend -m E6x; echo "-- committed, extra file in the commit:"; V committed
cd ..; rm -rf r
cp -r "$PKG" dmg; echo x >> dmg/repo_overlay/src/methods/E_006/contract.py; fresh lf; echo "-- damaged package:"; python3 -I ../dmg/VERIFY_E6_INSTALL.py --repo . --phase pre 2>&1 | grep STOP | head -1; cd ..; rm -rf r dmg
echo end
