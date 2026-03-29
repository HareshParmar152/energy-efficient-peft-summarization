@echo off
echo Testing Python setup...
echo.

REM Force deactivate by starting fresh cmd
echo Python version:
python --version

echo.
echo Checking PyTorch:
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"

echo.
echo Checking transformers:
python -c "import transformers; print('Transformers version:', transformers.__version__)"

echo.
echo Checking peft:
python -c "import peft; print('PEFT version:', peft.__version__)"

echo.
echo All checks passed! Ready to run experiments.
pause
