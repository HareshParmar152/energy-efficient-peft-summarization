@echo off
title XSum OPT Experiments - STARTING NOW
cls
echo ========================================
echo STARTING OPT EXPERIMENTS NOW
echo ========================================
echo.
echo Model: OPT-1.3B (Meta/Facebook)
echo Experiments: E25, E26, E27
echo Expected time: 4-6 hours
echo.
echo ========================================
echo.

cd /d "E:\Energy-Efficient Project\Energy_Efficient_Project"

echo Running experiments...
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u run_xsum_llama_experiments_2000steps.py

echo.
echo ========================================
echo DONE!
echo ========================================
pause
