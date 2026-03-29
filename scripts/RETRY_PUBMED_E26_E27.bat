@echo off
title Retry PubMed E26 & E27
cls
echo ========================================
echo RETRY PUBMED EXPERIMENTS E26 & E27
echo ========================================
echo.
echo This will retry the 2 failed experiments:
echo   E26 - GPT-2 Medium + QLoRA
echo   E27 - GPT-2 Medium + Adapters
echo.
echo All 7 completed experiments will be skipped automatically.
echo.
echo Fixed: Reduced batch size to avoid OOM
echo Estimated time: 26-30 hours total
echo.
echo ========================================
echo.
pause

echo Starting retry...
echo DO NOT CLOSE THIS WINDOW
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u run_pubmed_all_9_experiments_2000steps.py

echo.
echo ========================================
echo All PubMed Experiments Complete!
echo ========================================
echo.
pause
