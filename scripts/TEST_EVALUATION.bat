@echo off
REM ============================================
REM Test Evaluation - Single Experiment
REM Tests SAMSum E1 (BART LoRA) with 10 samples
REM ============================================

echo ============================================
echo TEST EVALUATION
echo ============================================
echo.
echo Testing evaluation on SAMSum E1 (10 samples)
echo This should take 1-2 minutes
echo.
pause

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run test
python test_evaluation_single.py

echo.
pause
