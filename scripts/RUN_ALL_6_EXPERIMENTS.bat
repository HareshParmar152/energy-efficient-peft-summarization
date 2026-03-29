@echo off
REM Run All 6 Pending Experiments Sequentially
REM This will automatically start each experiment when the previous completes

echo ================================================================================
echo SEQUENTIAL TRAINING OF 6 PENDING EXPERIMENTS
echo ================================================================================
echo.
echo This batch file will run all 6 experiments one after another:
echo   1. E25 - BillSum GPT-2 LoRA (EASIEST)
echo   2. E27 - BillSum GPT-2 Adapters (EASY)
echo   3. E26 - XSum GPT-2 QLoRA (MEDIUM)
echo   4. E2 - BillSum BART QLoRA (HARD)
echo   5. E14 - BillSum T5 QLoRA (HARD)
echo   6. E26 - BillSum GPT-2 QLoRA (HARDEST)
echo.
echo Expected total time: 10-15 hours
echo.
echo Press Ctrl+C to stop at any time
echo ================================================================================
echo.

pause

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the orchestrator script
python run_all_6_experiments_sequential.py

echo.
echo ================================================================================
echo ALL EXPERIMENTS COMPLETED
echo ================================================================================
echo.
echo Check the results JSON files in:
echo   E:/Pending Experiment data/BillSum_Experiments/
echo   E:/Pending Experiment data/XSum_Experiments/
echo.

pause
