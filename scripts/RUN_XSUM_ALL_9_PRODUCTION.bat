@echo off
echo ========================================
echo XSum All 9 Experiments - Production Run
echo 2000 Steps Per Experiment
echo ========================================
echo.
echo This will run ALL 9 experiments sequentially:
echo.
echo BART Experiments (E1-E3):
echo   E1: BART + LoRA
echo   E2: BART + QLoRA
echo   E3: BART + Adapters
echo.
echo T5 Experiments (E13-E15):
echo   E13: T5 + LoRA
echo   E14: T5 + QLoRA
echo   E15: T5 + Adapters
echo.
echo LLaMA Experiments (E25-E27):
echo   E25: LLaMA + LoRA
echo   E26: LLaMA + QLoRA
echo   E27: LLaMA + Adapters
echo.
echo Configuration:
echo   - Steps: 2000 per experiment
echo   - Batch size: 8
echo   - Save every: 500 steps
echo   - TRAINING ONLY (no evaluation)
echo.
echo Results will be saved to:
echo   E:\Pending Experiment data\XSum_Experiments\
echo     - BART\
echo     - T5\
echo     - LLaMA\
echo.
echo Estimated time: 8-12 hours total
echo.
echo NOTE: This is TRAINING ONLY
echo Evaluation will be done separately later
echo.
pause

echo.
echo Checking CUDA availability...
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -c "import torch; cuda_available = torch.cuda.is_available(); print('CUDA Available:', cuda_available); exit(0 if cuda_available else 1)"

if errorlevel 1 (
    echo.
    echo ========================================
    echo WARNING: CUDA NOT AVAILABLE!
    echo ========================================
    echo.
    echo Your PyTorch is CPU-only. Training will be VERY SLOW (15+ hours^).
    echo.
    echo To fix this, run: FIX_PYTORCH_CUDA.bat
    echo.
    echo Do you want to continue anyway? (Not recommended^)
    pause
)

echo.
echo Starting production run...
echo.
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe run_xsum_all_9_experiments_2000steps.py

echo.
echo ========================================
echo Production Run Complete!
echo ========================================
echo.
echo Check results at:
echo E:\Pending Experiment data\XSum_Experiments\
echo.
pause
