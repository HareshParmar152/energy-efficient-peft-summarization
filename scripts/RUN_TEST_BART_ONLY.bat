@echo off
echo ========================================
echo Testing BART XSum Experiments Only
echo 20 Steps - Quick Test
echo ========================================
echo.
echo This will test 3 BART configurations:
echo 1. BART + LoRA
echo 2. BART + QLoRA  
echo 3. BART + Adapters
echo.
pause

echo.
echo Activating virtual environment...
call research_env\Scripts\activate.bat

echo.
echo Starting BART test...
python test_xsum_bart_only_20steps.py

echo.
echo ========================================
echo Test Complete!
echo Check test_logs folder for results
echo ========================================
pause
