@echo off
echo ================================================================================
echo AUTO-RUN: Remaining 4 Experiments (E27, XSum E26, E2, E14)
echo ================================================================================
echo.
echo This will run:
echo 1. E27 - BillSum GPT-2 Adapters (EASY - 70%% success)
echo 2. E26 - XSum GPT-2 QLoRA (MEDIUM - 50%% success)
echo 3. E2  - BillSum BART QLoRA (HARD - 40%% success)
echo 4. E14 - BillSum T5 QLoRA (HARD - 40%% success)
echo.
echo Total estimated time: 6-10 hours
echo.
pause

REM Activate virtual environment
call .venv\Scripts\activate

echo.
echo ================================================================================
echo [1/4] Starting E27 (BillSum GPT-2 Adapters)...
echo ================================================================================
python train_billsum_e27.py

echo.
echo ================================================================================
echo [2/4] Starting XSum E26 (GPT-2 QLoRA)...
echo ================================================================================
python train_xsum_e26.py

echo.
echo ================================================================================
echo [3/4] Starting E2 (BillSum BART QLoRA)...
echo ================================================================================
python train_billsum_e2.py

echo.
echo ================================================================================
echo [4/4] Starting E14 (BillSum T5 QLoRA)...
echo ================================================================================
python train_billsum_e14.py

echo.
echo ================================================================================
echo ALL 4 EXPERIMENTS COMPLETE!
echo ================================================================================
echo E27 (BillSum GPT-2 Adapters) - DONE
echo E26 (XSum GPT-2 QLoRA) - DONE
echo E2  (BillSum BART QLoRA) - DONE
echo E14 (BillSum T5 QLoRA) - DONE
echo.
echo Check results in:
echo - E:/Pending Experiment data/BillSum_Experiments/GPT2/results/E27_results.json
echo - E:/Pending Experiment data/XSum_Experiments/GPT2/results/E26_results.json
echo - E:/Pending Experiment data/BillSum_Experiments/BART/results/E2_results.json
echo - E:/Pending Experiment data/BillSum_Experiments/T5/results/E14_results.json
echo ================================================================================
pause
