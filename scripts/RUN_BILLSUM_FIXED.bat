@echo off
echo ================================================================================
echo BillSum Experiments - FIXED VERSION
echo ================================================================================
echo.
echo This will:
echo   1. Deactivate .venv (if active)
echo   2. Use system Python (which has all packages)
echo   3. Run BillSum experiments
echo.
echo Auto-skip completed: E1, E3, E13, E15
echo Will retry failed: E25, E27, E2, E14, E26
echo.
echo Expected time: 35-44 hours
echo.
pause

echo.
echo Deactivating .venv...
if defined VIRTUAL_ENV (
    call deactivate
)

echo.
echo Checking Python and PyTorch...
python --version
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

echo.
echo Starting BillSum experiments...
echo.

python run_billsum_all_9_experiments_2000steps.py

echo.
echo ================================================================================
echo Experiments completed!
echo ================================================================================
pause
