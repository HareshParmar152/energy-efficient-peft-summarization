@echo off
echo ============================================
echo BILLSUM EVALUATION - 4 EXPERIMENTS
echo ============================================
echo.
echo This will evaluate:
echo - E1 (BART LoRA)
echo - E3 (BART Adapters)
echo - E13 (T5 LoRA)
echo - E15 (T5 Adapters)
echo.
echo Estimated time: 3-4 hours
echo.
pause

call .venv\Scripts\activate.bat
python evaluate_billsum_all.py

echo.
echo ============================================
echo EVALUATION COMPLETE
echo ============================================
echo Check the log file for details
pause
