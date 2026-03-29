@echo off
echo ========================================
echo Multi-News All 9 Experiments - 2000 Steps
echo ========================================
echo.
echo This will run 9 experiments on Multi-News dataset:
echo - BART: LoRA, QLoRA, Adapters
echo - T5: LoRA, QLoRA, Adapters
echo - GPT-2: LoRA, QLoRA, Adapters
echo.
echo Multi-News: Multi-document summarization
echo Estimated time: 70-90 hours
echo.
pause

REM Deactivate virtual environment if active
if defined VIRTUAL_ENV (
    echo Deactivating virtual environment...
    call deactivate
)

echo.
echo Starting Multi-News experiments...
echo.

python run_multinews_all_9_experiments_2000steps.py

echo.
echo ========================================
echo Experiments completed!
echo Check: E:\Pending Experiment data\MultiNews_Experiments\
echo ========================================
pause
