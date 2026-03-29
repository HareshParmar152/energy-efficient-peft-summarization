@echo off
echo ========================================
echo HuggingFace Login for LLaMA Access
echo ========================================
echo.
echo This will prompt you to enter your HuggingFace token.
echo.
echo If you don't have a token yet:
echo 1. Go to https://huggingface.co/settings/tokens
echo 2. Create a new token (Read access)
echo 3. Copy the token (starts with hf_...)
echo.
pause

echo.
echo Installing huggingface_hub...
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -m pip install -q huggingface_hub

echo.
echo Please paste your HuggingFace token when prompted...
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -c "from huggingface_hub import login; login()"

echo.
echo ========================================
echo Login Complete!
echo ========================================
echo.
echo Now run: VERIFY_LLAMA_ACCESS.bat
echo.
pause
