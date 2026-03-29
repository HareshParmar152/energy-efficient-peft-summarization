@echo off
REM This starts a completely fresh command prompt without any venv
REM Then runs the BillSum experiments

echo ================================================================================
echo Starting BillSum Experiments (Fresh Environment)
echo ================================================================================
echo.
echo This will:
echo   1. Open a new command window (no venv)
echo   2. Run BillSum experiments
echo   3. Auto-skip completed experiments
echo   4. Retry failed experiments
echo.
echo Expected time: 35-44 hours
echo.
pause

REM Start a new cmd window without inheriting environment
start "BillSum Experiments" cmd /k "cd /d "%~dp0" && python run_billsum_all_9_experiments_2000steps.py && pause"

echo.
echo New window opened! Check the "BillSum Experiments" window.
echo You can close this window now.
pause
