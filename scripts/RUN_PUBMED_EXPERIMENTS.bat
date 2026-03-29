@echo off
title PubMed GPT-2 Experiments (E28, E29, E30)
cls
echo ========================================
echo PUBMED GPT-2 EXPERIMENTS
echo Decoder-Only Architecture - 4GB GPU
echo ========================================
echo.
echo This will run 3 GPT-2 experiments on PubMed:
echo   E28 - GPT-2 Medium + LoRA
echo   E29 - GPT-2 Medium + QLoRA
echo   E30 - GPT-2 Medium + Adapters
echo.
echo Model: GPT-2 Medium (355M parameters)
echo Dataset: PubMed (biomedical literature)
echo Note: Using 4-bit quantization for efficiency
echo.
echo Estimated time: 5-7 hours total
echo.
echo ========================================
echo.
pause

echo Starting PubMed experiments...
echo DO NOT CLOSE THIS WINDOW
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u run_pubmed_experiments_2000steps.py

echo.
echo ========================================
echo PubMed Experiments Complete!
echo ========================================
echo.
pause
