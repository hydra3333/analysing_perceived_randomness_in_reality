#!/bin/bash
# NAMES-1 install-package end-to-end test (Claude's Linux trial). Usage: e2e_test.sh SCRATCH BASE_CLONE PKG
S=$1; NB=$2; P=$3; V="python3 -I $P/VERIFY_NAMES1_INSTALL.py --repo ."
fresh(){ cd $S; rm -rf $S/e2e_$1; git clone -q $NB $S/e2e_$1 2>/dev/null; cd $S/e2e_$1; if [ "$2" = crlf ]; then git config core.autocrlf true; git rm -rq --cached . >/dev/null; git reset -q --hard; fi; }
echo "Base: a disposable clone of GitHub main at 908db9e (DOC-2 installed for real)."
for mode in lf crlf; do
  echo "== happy path, checkout line endings: $mode"; fresh $mode $mode
  $V --phase pre 2>&1 | grep -E "PASS|STOP"
  bash $P/rename_files_for_linux_test.sh && echo "renames done (27 git mv, same list as RENAME_FILES.cmd)"
  cp -r $P/repo_overlay/. . && echo "overlay copied"
  $V --phase post 2>&1 | grep -E "PASS|STOP"
  python3 $P/RUN_NAMES1_SUITE.py --repo . | sed 's#/usr/local/bin/python3##'
  python3 $P/CHECK_NAMES1_IMPORTS.py --repo . | grep -vE "^PASS (old name|new name)"; echo "(27 old-name refusal and 27 new-name origin PASS lines omitted above)"
  bash $P/stage_for_linux_test.sh >/dev/null 2>&1; echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr -s ' ' | tr '\n' ' ')"
  git -c user.name=t -c user.email=t@t commit -qm "NAMES-1 test"; $V --phase committed 2>&1 | grep -E "PASS|STOP"
  echo "bytecode dirs left in tree: $(find . -name __pycache__ -not -path './.git/*' | wc -l)"
done
echo "== N1-T10 immediate recovery check (disposable clone of the LF test commit)"
cd $S; rm -rf e2e_rb; git clone -q $S/e2e_lf e2e_rb 2>/dev/null; cd e2e_rb; git -c user.name=t -c user.email=t@t revert --no-edit HEAD >/dev/null
echo "files differing from the pre-NAMES-1 tree after revert: $(git diff --name-only HEAD $(git -C $NB rev-parse HEAD) | wc -l)"
echo "== negative cases (each must STOP)"
fresh n1; bash $P/rename_files_for_linux_test.sh; cp -r $P/repo_overlay/. .; echo "# x" >> src/methods/_common/game_draws_reader.py; echo "tampered edited file -> $($V --phase post 2>&1 | grep -oE 'STOP.*' | cut -c1-110)"
fresh n2; bash $P/rename_files_for_linux_test.sh; cp -r $P/repo_overlay/. .; echo x > src/methods/stray.py; echo "extra file -> $($V --phase post 2>&1 | grep -oE 'STOP.*' | cut -c1-110)"
fresh n3; head -n 27 $P/rename_files_for_linux_test.sh | sed '$d' > $S/r26.sh; bash $S/r26.sh; cp -r $P/repo_overlay/. .; echo "one rename missing -> $($V --phase post 2>&1 | grep -oE 'STOP.*' | cut -c1-110)"
fresh n4; echo 'see game_draws_reader_v1' >> README.md; git -c user.name=t -c user.email=t@t commit -qam stale; bash $P/rename_files_for_linux_test.sh; cp -r $P/repo_overlay/. .; echo "stale old name in an unchanged live file -> $($V --phase post 2>&1 | grep -oE 'STOP.*' | cut -c1-110)"
fresh n5; echo x > untracked.txt; echo "dirty tree before install -> $($V --phase pre 2>&1 | grep -oE 'STOP.*' | cut -c1-70)"
fresh n6; git reset -q --hard HEAD~1; echo "DOC-2 not installed -> $($V --phase pre 2>&1 | grep -oE 'STOP.*' | cut -c1-90)"
fresh n7; bash $P/rename_files_for_linux_test.sh; cp -r $P/repo_overlay/. .; bash $P/stage_for_linux_test.sh >/dev/null 2>&1; git -c user.name=t -c user.email=t@t commit -qm x; echo y >> README.md; git -c user.name=t -c user.email=t@t commit -qam y; echo "extra change in the commit -> $($V --phase committed 2>&1 | grep -oE 'STOP.*' | cut -c1-110)"
fresh n8; bash $P/rename_files_for_linux_test.sh; cp -r $P/repo_overlay/. .; git reset -q --hard; git clean -fdq -- doc review; echo "undo (git reset --hard; git clean -fd -- doc review) -> status lines $(git status --porcelain | wc -l); $($V --phase pre 2>&1 | grep -oE 'PRE PASS|STOP.*' | head -1)"
