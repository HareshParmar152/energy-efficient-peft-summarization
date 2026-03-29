@echo off
echo ================================================================================
echo BillSum All 9 Experiments - 2000 Steps
echo ================================================================================
echo.
echo This will run all 9 experiments on BillSum dataset:
echo - BART: LoRA, QLoRA, Adapters
echo - T5: LoRA, QLoRA, Adapters
echo - GPT-2: LoRA, QLoRA, Adapters
echo.
echo Estimated time: 60-80 hours (2.5-3.5 days)
echo.
echo IMPORTANT: Deactivate .venv before running!
echo.
pause

echo.
echo Deactivating virtual environment...
call deactivate 2>nul

echo.
echo Starting BillSum experiments...
echo.

python run_billsum_all_9_experiments_2000steps.py

echo.
echo ================================================================================
echo BillSum experiments completed!
echo Check logs in: E:\Pending Experiment data\BillSum_Experiments\logs\
echo ================================================================================
pause
