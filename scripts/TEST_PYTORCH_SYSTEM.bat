@echo off
title Test PyTorch with System Python
cls
echo ========================================
echo TESTING PYTORCH WITH SYSTEM PYTHON
echo ========================================
echo.
echo Python Path: C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe
echo.
echo Testing PyTorch import...
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -c "import torch; print('PyTorch Version:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
pause
