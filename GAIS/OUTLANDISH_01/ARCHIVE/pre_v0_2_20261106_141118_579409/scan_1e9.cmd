@echo off
rem OUTLANDISH_01: owner-run single-thread Powerball billion-digit scan.
rem Invoke from the OUTLANDISH_01 directory after conversion and verification.
if not exist digits_pi_10_to_9.bin (
  echo Missing digits_pi_10_to_9.bin
  exit /b 2
)
if not exist digits_golden_ratio_10_to_9.bin (
  echo Missing digits_golden_ratio_10_to_9.bin
  exit /b 2
)
if not exist POWERBALL_preholdout_only.csv (
  echo Missing POWERBALL_preholdout_only.csv
  exit /b 2
)
python outlandish_powerball_stage_a.py scan --draws POWERBALL_preholdout_only.csv --digits digits_pi_10_to_9.bin digits_golden_ratio_10_to_9.bin --chunk-bytes 4000000 --progress-seconds 5
exit /b %errorlevel%
