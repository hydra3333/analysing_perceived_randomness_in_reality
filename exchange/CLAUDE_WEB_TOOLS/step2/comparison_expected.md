Then the comparison. It prints one line for every new test, so put it in a file and look at the rest. **In the first
command, type the baseline folder of part 1 in place of `BASELINE`** (`E:\TEMP\TIDY1_evidence\suite_after`, or
`E:\TEMP\STEP2_evidence\suite_before` if you made a new one):

```bat
.venv\Scripts\python.exe -B "E:\TEMP\STEP2_Research_Engine_v1r2\tools\compare_suite_reports.py" "BASELINE" "E:\TEMP\STEP2_evidence\suite_after" > "E:\TEMP\STEP2_evidence\comparison.txt"
findstr /v /b /c:"NEW: " /c:"MODULE NEW: " "E:\TEMP\STEP2_evidence\comparison.txt"
find /c "NEW: " "E:\TEMP\STEP2_evidence\comparison.txt"
```

Expected from `findstr` (every line that is not about a new test), exactly these:
`before: 45 modules; unittest ran 571 tests; identified here: 571`;
`after: 52 modules; unittest ran 762 tests; identified here: 762`;
**`tests in both runs: 571; with the same result: 571`**;
three entries `FAILS IN BOTH RUNS` (the failures that exist today: `test_gitignore_lines`, with the words
`FAILURE LINES DIFFER` and its two long lines, which is expected because that test prints a set in a different
order each run; and two tests of `test_multigame_reader_contracts`);
and the last line `RESULT: DIFFERENCES FOUND - each needs an explanation`. **Here that last line is expected:** the
only differences are the 7 new test modules and their 191 new tests. `find /c` prints **198** (191 lines `NEW:` and
7 lines `MODULE NEW:`).
**A STOP is any line beginning `CHANGED`, `DISAPPEARED`, `MODULE CHANGED`, `MODULE DISAPPEARED`,
`NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`, a `tests in both runs` line whose two numbers differ, or a count other
than 198.**
