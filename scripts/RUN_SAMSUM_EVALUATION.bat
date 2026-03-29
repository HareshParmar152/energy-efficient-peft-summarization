@echo off
REM ============================================
REM Evaluate All SAMSum Experiments
REM ============================================

echo ============================================
echo SAMSUM EVALUATION - ALL 9 EXPERIMENTS
echo ============================================
echo.
echo This will evaluate:
echo - BART: E1, E2, E3 (LoRA, QLoRA, Adapters)
echo - T5: E13, E14, E15 (LoRA, QLoRA, Adapters)
echo - GPT-2: E25, E26, E27 (LoRA, QLoRA, Adapters)
echo.
echo Estimated time: 6-9 hours
echo.
pause

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run evaluation
python evaluate_samsum_all.py

echo.
echo ============================================
echo EVALUATION COMPLETE
echo ============================================
echo.
pause
