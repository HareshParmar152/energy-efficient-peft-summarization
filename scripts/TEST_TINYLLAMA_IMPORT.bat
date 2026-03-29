@echo off
title Test TinyLlama Import
cls
echo ========================================
echo TESTING TINYLLAMA MODEL ACCESS
echo ========================================
echo.
echo This will verify:
echo   1. PyTorch with CUDA is working
echo   2. All required libraries are installed
echo   3. TinyLlama model can be loaded
echo.
echo Note: First run will download the model (~4.4GB)
echo.
echo ========================================
echo.
pause

echo Running test...
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u TEST_TINYLLAMA_IMPORT.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
pause
