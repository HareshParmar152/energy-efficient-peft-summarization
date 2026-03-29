@echo off
REM ============================================
REM Resume Evaluation - Continue from where it left off
REM ============================================

echo ============================================
echo RESUME EVALUATION
echo ============================================
echo.
echo This will:
echo - Skip already completed experiments
echo - Use smaller batch size (4 instead of 8)
echo - Better memory management
echo.
echo Currently completed: 7 PubMed experiments
echo Remaining: 23 experiments
echo.
pause

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run evaluation
python evaluate_remaining.py

echo.
echo ============================================
echo EVALUATION COMPLETE
echo ============================================
echo.
pause
