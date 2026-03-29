@echo off
echo ================================================================================
echo Installing PyTorch and Dependencies
echo ================================================================================
echo.
echo This will install PyTorch with CUDA support in your system Python.
echo.
pause

echo.
echo Installing PyTorch...
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo Installing transformers...
python -m pip install transformers

echo.
echo Installing peft...
python -m pip install peft

echo.
echo Installing datasets...
python -m pip install datasets

echo.
echo Installing codecarbon...
python -m pip install codecarbon

echo.
echo Installing accelerate...
python -m pip install accelerate

echo.
echo Installing bitsandbytes...
python -m pip install bitsandbytes

echo.
echo ================================================================================
echo Installation complete!
echo ================================================================================
echo.
echo Testing installation...
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

echo.
pause
