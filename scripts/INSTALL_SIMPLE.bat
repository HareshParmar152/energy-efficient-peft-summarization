@echo off
REM ============================================
REM Simple Installation Script
REM ============================================

echo ============================================
echo Installing All Required Packages
echo ============================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Virtual environment activated
echo.

REM Install PyTorch first (special index URL)
echo [1/2] Installing PyTorch with CUDA support...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo [2/2] Installing other packages...
pip install transformers peft adapters datasets evaluate rouge-score accelerate bitsandbytes codecarbon tqdm sentencepiece protobuf

echo.
echo ============================================
echo Testing Installation
echo ============================================
python -c "import torch; print('✓ PyTorch:', torch.__version__); print('✓ CUDA:', torch.cuda.is_available())"
python -c "import transformers; print('✓ Transformers:', transformers.__version__)"
python -c "import peft; print('✓ PEFT installed')"
python -c "import datasets; print('✓ Datasets installed')"
python -c "import evaluate; print('✓ Evaluate installed')"

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo You can now run: .\TEST_EVALUATION.bat
echo.
pause
