@echo off
echo ================================================================================
echo BILLSUM EXPERIMENTS - MANUAL RESTART OPTION
echo ================================================================================
echo.
echo STEP 1: Restart your computer manually
echo   - Close this window
echo   - Restart Windows
echo   - This clears GPU memory corruption
echo.
echo STEP 2: After restart, run this command:
echo   RUN_BILLSUM_EXPERIMENTS.bat
echo.
echo The script will automatically:
echo   - Skip 4 completed experiments (E1, E3, E13, E15)
echo   - Retry 5 failed experiments (E2, E14, E25, E26, E27)
echo   - Complete in ~35-44 hours
echo.
echo ================================================================================
echo.
pause
