@echo off
echo ================================================================================
echo AUTO-RUN: E27 then XSum E26
echo ================================================================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate

echo Starting E27 (GPT-2 Adapters)...
echo ================================================================================
python train_billsum_e27.py

echo.
echo ================================================================================
echo E27 Complete! Starting XSum E26 (GPT-2 QLoRA)...
echo ================================================================================
echo.

python train_xsum_e26.py

echo.
echo ================================================================================
echo BOTH EXPERIMENTS COMPLETE!
echo ================================================================================
echo E27 (BillSum GPT-2 Adapters) - DONE
echo E26 (XSum GPT-2 QLoRA) - DONE
echo ================================================================================
pause
