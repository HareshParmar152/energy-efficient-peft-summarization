@echo off
echo ========================================
echo Fix PyTorch - Install CUDA Version
echo ========================================
echo.
echo Current Status: PyTorch CPU-only detected
echo Your GPU: NVIDIA RTX 2050 (CUDA 13.0)
echo.
echo This will:
echo 1. Uninstall CPU-only PyTorch
echo 2. Install PyTorch with CUDA 12.4 support
echo    (CUDA 12.4 is compatible with your CUDA 13.0 driver)
echo.
pause

echo.
echo Step 1: Uninstalling CPU-only PyTorch...
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -m pip uninstall -y torch torchvision torchaudio

echo.
echo Step 2: Installing PyTorch with CUDA 12.4...
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

echo.
echo Step 3: Verifying installation...
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -c "import torch; print('PyTorch Version:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version:', torch.version.cuda); print('GPU Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo If CUDA Available shows True, you're ready to go!
echo Your training will now use GPU and be 10-20x faster.
echo.
pause
