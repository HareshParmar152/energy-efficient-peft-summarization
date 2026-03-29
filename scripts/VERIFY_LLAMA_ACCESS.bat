@echo off
echo ========================================
echo Verify LLaMA Model Access
echo ========================================
echo.
echo Checking if you can access meta-llama/Llama-2-7b-hf...
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -c "from transformers import AutoTokenizer; print('Testing access...'); tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-hf'); print('\n✓ SUCCESS! You have access to LLaMA models.'); print('You can now run all 9 experiments.')"

if errorlevel 1 (
    echo.
    echo ✗ FAILED - You don't have access yet.
    echo.
    echo Please:
    echo 1. Request access at: https://huggingface.co/meta-llama/Llama-2-7b-hf
    echo 2. Wait for approval email
    echo 3. Run LOGIN_HUGGINGFACE.bat
    echo 4. Try again
) else (
    echo.
    echo ========================================
    echo Ready to run all 9 experiments!
    echo ========================================
)

echo.
pause
