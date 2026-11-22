#!/bin/bash
# Rehearsal of the build step 1 install in disposable clones: an LF checkout and a CRLF checkout, then four cases that must STOP.
R=$1; P=$2; W=$3
V="python3 -I $P/VERIFY_STEP1_INSTALL.py"; G='grep -E PASS|STOP|FAIL'
rm -rf "$W"; mkdir -p "$W"; cd "$W"
for kind in lf crlf; do
  if [ $kind = crlf ]; then git clone -q -c core.autocrlf=true "$R" $kind; else git clone -q "$R" $kind; fi
  git -C $kind config user.email rehearsal@example.invalid; git -C $kind config user.name rehearsal
  echo "== $kind checkout (core.autocrlf=$(git -C $kind config core.autocrlf || echo unset))"
  $V --repo $kind --phase pre 2>&1 | $G
  cp -r "$P/repo_overlay/." $kind/
  git -C $kind rm -q --pathspec-from-file="$P/DELETE_PATHS.txt"
  $V --repo $kind --phase post 2>&1 | $G
  git -C $kind add src tests 2>/dev/null
  echo "git status --short, by first letter: $(git -C $kind status --short | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git -C $kind commit -q -m rehearsal
  $V --repo $kind --phase committed 2>&1 | $G | sed -E 's/\([0-9a-f]{7}\)/(commit)/'
done
echo "== cases that must STOP"
git clone -q "$R" n1; echo x > n1/src/methods/stray.py
echo "a stray file before the install:        $($V --repo n1 --phase pre 2>&1 | $G | cut -c1-70)"
git clone -q "$R" n2; cp -r "$P/repo_overlay/." n2/; git -C n2 rm -q --pathspec-from-file="$P/DELETE_PATHS.txt"; echo "# x" >> n2/src/methods/E_002/core_v1.py
echo "wrong bytes in a copied file:           $($V --repo n2 --phase post 2>&1 | $G | cut -c1-70)"
git clone -q "$R" n3; cp -r "$P/repo_overlay/." n3/
echo "the deletions left out:                 $($V --repo n3 --phase post 2>&1 | $G | cut -c1-70)"
git clone -q "$R" n4; echo >> n4/source_data/OZLOTTO_results_master.csv
echo "a results master changed:               $($V --repo n4 --phase pre 2>&1 | $G | cut -c1-70)"
