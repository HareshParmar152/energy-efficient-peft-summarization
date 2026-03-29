@echo off
title Starting GPT-2 Experiments NOW
cls
echo ========================================
echo STARTING GPT-2 EXPERIMENTS
echo ========================================
echo.
echo Model: GPT-2 Medium (355M parameters)
echo Experiments: E25, E26, E27
echo Expected time: 3-5 hours
echo.
echo Justification document created:
echo MODEL_SUBSTITUTION_JUSTIFICATION.md
echo.
echo ========================================
echo.

cd /d "E:\Energy-Efficient Project\Energy_Efficient_Project"

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u run_xsum_llama_experiments_2000steps.py

pause
