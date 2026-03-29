@echo off
echo ================================================================================
echo SAMSum All 9 Experiments - 2000 Steps
echo ================================================================================
echo.
echo This will run all 9 experiments on SAMSum dataset:
echo - BART: LoRA, QLoRA, Adapters
echo - T5: LoRA, QLoRA, Adapters
echo - GPT-2: LoRA, QLoRA, Adapters
echo.
echo Estimated time: 50-70 hours (2-3 days)
echo.
echo IMPORTANT: Deactivate .venv before running!
echo.
pause

echo.
echo Deactivating virtual environment...
call deactivate 2>nul

echo.
echo Starting SAMSum experiments...
echo.

python run_samsum_all_9_experiments_2000steps.py

echo.
echo ================================================================================
echo SAMSum experiments completed!
echo Check logs in: E:\Pending Experiment data\SAMSum_Experiments\logs\
echo ================================================================================
pause
