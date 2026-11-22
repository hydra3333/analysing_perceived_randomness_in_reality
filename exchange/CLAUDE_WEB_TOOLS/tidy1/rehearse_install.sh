#!/bin/bash
# Rehearsal of the tidy-up install in disposable clones: an LF checkout and a CRLF checkout, then five cases that must STOP.
# Usage: rehearse_install.sh <repository clone> <extracted package folder> <work folder> <python>
R=$1; P=$2; W=$3; PY=$4
V="$PY -I $P/VERIFY_TIDY1_INSTALL.py"; C="$PY -B $P/tools/check_comments_only.py"; G='grep -E PASS|STOP|FAIL'
rm -rf "$W"; mkdir -p "$W"; cd "$W"
for kind in lf crlf; do
  if [ $kind = crlf ]; then git clone -q -c core.autocrlf=true "$R" $kind; else git clone -q "$R" $kind; fi
  git -C $kind config user.email rehearsal@example.invalid; git -C $kind config user.name rehearsal
  echo "== $kind checkout (core.autocrlf=$(git -C $kind config core.autocrlf || echo unset))"
  $V --repo $kind --phase pre 2>&1 | $G
  cp -r "$P/repo_overlay/." $kind/
  $V --repo $kind --phase post 2>&1 | $G
  $C --tree $kind | tail -2
  git -C $kind add src 2>/dev/null
  echo "git status --short, by first letter: $(git -C $kind status --short | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git -C $kind commit -q -m rehearsal
  $V --repo $kind --phase committed 2>&1 | $G | sed -E 's/\([0-9a-f]{7}\)/(commit)/'
done
echo "== cases that must STOP"
git clone -q "$R" n1; echo x > n1/src/methods/stray.py
echo "a stray file before the install:        $($V --repo n1 --phase pre 2>&1 | $G | cut -c1-70)"
git clone -q "$R" n2; cp -r "$P/repo_overlay/." n2/; echo "# x" >> n2/src/methods/E_002/core_v1.py
echo "wrong bytes in a copied file:           $($V --repo n2 --phase post 2>&1 | $G | cut -c1-70)"
git clone -q "$R" n3; cp -r "$P/repo_overlay/." n3/; git -C n3 checkout -q -- src/methods/E_019/variants.py
echo "one file not copied:                    $($V --repo n3 --phase post 2>&1 | $G | cut -c1-70)"
git clone -q "$R" n4; echo >> n4/source_data/OZLOTTO_results_master.csv
echo "a results master changed:               $($V --repo n4 --phase pre 2>&1 | $G | cut -c1-70)"
git clone -q "$R" n5; cp -r "$P/repo_overlay/." n5/; sed -i 's/^SCORE_COEFFICIENT = 1 /SCORE_COEFFICIENT = 0 /' n5/src/methods/E_004/core_v1.py
echo "a calculation changed in a copied file: $($C --tree n5 | grep -E 'CODE CHANGED|RESULT' | cut -c1-70 | tr '\n' '|')"
