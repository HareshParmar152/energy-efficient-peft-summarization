@echo off
echo ========================================
echo Reddit TIFU All 9 Experiments - 2000 Steps
echo ========================================
echo.
echo This will run 9 experiments on Reddit TIFU dataset:
echo - BART: LoRA, QLoRA, Adapters
echo - T5: LoRA, QLoRA, Adapters
echo - GPT-2: LoRA, QLoRA, Adapters
echo.
echo Estimated time: 60-80 hours
echo.
pause

REM Deactivate virtual environment if active
if defined VIRTUAL_ENV (
    echo Deactivating virtual environment...
    call deactivate
)

echo.
echo Starting Reddit TIFU experiments...
echo.

python run_reddit_tifu_all_9_experiments_2000steps.py

echo.
echo ========================================
echo Experiments completed!
echo Check: E:\Pending Experiment data\Reddit_TIFU_Experiments\
echo ========================================
pause
