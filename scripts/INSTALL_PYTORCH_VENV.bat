@echo off
REM ============================================
REM Install PyTorch in Virtual Environment
REM ============================================

echo ============================================
echo Installing PyTorch in Virtual Environment
echo ============================================
echo.
echo This will install all required packages
echo in your .venv virtual environment
echo.
pause

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo.
echo Virtual environment activated
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing PyTorch with CUDA 11.8 support...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo.
echo Installing transformers...
pip install transformers

echo.
echo Installing peft...
pip install peft

echo.
echo Installing datasets...
pip install datasets

echo.
echo Installing evaluate (for ROUGE)...
pip install evaluate

echo.
echo Installing rouge-score...
pip install rouge-score

echo.
echo Installing codecarbon...
pip install codecarbon

echo.
echo Installing accelerate...
pip install accelerate

echo.
echo Installing bitsandbytes...
pip install bitsandbytes

echo.
echo Installing tqdm...
pip install tqdm

echo.
echo Installing adapters...
pip install adapters

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Testing installation...
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

echo.
echo ============================================
echo All packages installed successfully!
echo You can now run the evaluation scripts.
echo ============================================
echo.
pause
