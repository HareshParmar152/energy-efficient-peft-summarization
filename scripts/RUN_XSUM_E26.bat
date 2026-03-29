@echo off
title XSum E26 - GPT-2 QLoRA
cls
echo ========================================
echo XSUM E26 EXPERIMENT
echo GPT-2 Medium + QLoRA
echo ========================================
echo.
echo This will run the missing XSum experiment:
echo   E26 - GPT-2 Medium + QLoRA
echo.
echo All 8 completed experiments will be skipped automatically.
echo.
echo Estimated time: 8-10 hours
echo.
echo ========================================
echo.
pause

echo Starting XSum E26...
echo DO NOT CLOSE THIS WINDOW
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u run_xsum_all_9_experiments_2000steps.py

echo.
echo ========================================
echo XSum E26 Complete!
echo ========================================
echo.
pause
