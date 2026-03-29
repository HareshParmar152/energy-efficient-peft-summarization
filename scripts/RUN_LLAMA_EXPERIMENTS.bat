@echo off
title XSum GPT-2 Experiments (E25, E26, E27)
cls
echo ========================================
echo XSUM GPT-2 EXPERIMENTS
echo Decoder-Only Architecture - 4GB GPU
echo ========================================
echo.
echo This will run 3 GPT-2 experiments:
echo   E25 - GPT-2 Medium + LoRA
echo   E26 - GPT-2 Medium + QLoRA
echo   E27 - GPT-2 Medium + Adapters
echo.
echo Model: GPT-2 Medium (355M parameters)
echo Note: Using 4-bit quantization for efficiency
echo.
echo Estimated time: 3-5 hours total
echo.
echo ========================================
echo.
pause

echo Starting GPT-2 experiments...
echo DO NOT CLOSE THIS WINDOW
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u run_xsum_llama_experiments_2000steps.py

echo.
echo ========================================
echo GPT-2 Experiments Complete!
echo ========================================
echo.
pause
