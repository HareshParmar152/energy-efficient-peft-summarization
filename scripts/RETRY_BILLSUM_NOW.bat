@echo off
echo ================================================================================
echo BILLSUM EXPERIMENTS - RETRY NOW (NO RESTART)
echo ================================================================================
echo.
echo FIXES APPLIED:
echo   ✓ CUDA environment variables set (CUDA_LAUNCH_BLOCKING=1)
echo   ✓ Device-side assertions enabled (TORCH_USE_CUDA_DSA=1)
echo   ✓ GPU reset at script start
echo   ✓ Aggressive GPU cleanup before each experiment
echo   ✓ 30-second delay between experiments
echo   ✓ Enhanced error handling
echo.
echo EXPERIMENTS TO RETRY (5 failed):
echo   - E25: GPT-2 LoRA
echo   - E27: GPT-2 Adapters
echo   - E2: BART QLoRA
echo   - E14: T5 QLoRA
echo   - E26: GPT-2 QLoRA
echo.
echo ALREADY COMPLETED (4 will be skipped):
echo   ✓ E1: BART LoRA
echo   ✓ E3: BART Adapters
echo   ✓ E13: T5 LoRA
echo   ✓ E15: T5 Adapters
echo.
echo Expected time: 35-44 hours (1.5-2 days)
echo.
echo ================================================================================
echo.
echo Press any key to start, or Ctrl+C to cancel...
pause >nul
echo.
echo Starting BillSum experiments...
echo.

REM Deactivate any existing venv
call deactivate 2>nul

REM Run the script
python run_billsum_all_9_experiments_2000steps.py

echo.
echo ================================================================================
echo EXPERIMENTS COMPLETED
echo ================================================================================
echo.
echo Check results in: E:\Pending Experiment data\BillSum_Experiments
echo.
pause
