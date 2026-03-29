@echo off
REM ============================================
REM Evaluation Script for All Datasets
REM Evaluates: PubMed, XSum, SAMSum, BillSum
REM Total: 30 experiments
REM ============================================

echo ============================================
echo EVALUATION - ALL DATASETS
echo ============================================
echo.
echo This will evaluate 30 experiments:
echo - PubMed: 9 experiments
echo - XSum: 8 experiments
echo - SAMSum: 9 experiments
echo - BillSum: 4 experiments
echo.
echo Estimated time: 3-5 hours
echo.
pause

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run evaluation
python evaluate_all_datasets.py

echo.
echo ============================================
echo EVALUATION COMPLETE
echo ============================================
echo Check the log file for details
echo.
pause
