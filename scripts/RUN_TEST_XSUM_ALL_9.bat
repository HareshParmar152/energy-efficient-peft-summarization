@echo off
echo ========================================
echo Testing All 9 XSum Experiments
echo 20 Steps Only - Quick Test
echo ========================================
echo.
echo Models: BART, T5, LLaMA
echo Methods: LoRA, QLoRA, Adapters
echo Steps: 20 (test only)
echo.
echo This will test all 9 configurations quickly
echo to verify everything works before full training.
echo.
pause

echo.
echo Activating virtual environment...
call research_env\Scripts\activate.bat

echo.
echo Starting test...
python test_xsum_all_9_experiments_20steps.py

echo.
echo ========================================
echo Test Complete!
echo Check test_logs folder for results
echo ========================================
pause
