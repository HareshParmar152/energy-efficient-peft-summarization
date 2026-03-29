@echo off
echo ================================================================================
echo BILLSUM EXPERIMENTS - RESTART AND RETRY
echo ================================================================================
echo.
echo This will:
echo   1. Restart your computer to clear GPU memory
echo   2. Automatically run BillSum experiments after restart
echo.
echo The script will auto-skip the 4 completed experiments:
echo   - E1: BART LoRA (DONE)
echo   - E3: BART Adapters (DONE)
echo   - E13: T5 LoRA (DONE)
echo   - E15: T5 Adapters (DONE)
echo.
echo And retry the 5 failed experiments:
echo   - E25: GPT-2 LoRA
echo   - E27: GPT-2 Adapters
echo   - E2: BART QLoRA
echo   - E14: T5 QLoRA
echo   - E26: GPT-2 QLoRA
echo.
echo ================================================================================
echo.
pause
echo.
echo Setting up auto-run after restart...
echo.

REM Create a startup script
set STARTUP_SCRIPT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\run_billsum_after_restart.bat

echo @echo off > "%STARTUP_SCRIPT%"
echo timeout /t 30 >> "%STARTUP_SCRIPT%"
echo cd /d "%CD%" >> "%STARTUP_SCRIPT%"
echo call RUN_BILLSUM_EXPERIMENTS.bat >> "%STARTUP_SCRIPT%"
echo del "%%~f0" >> "%STARTUP_SCRIPT%"

echo ✓ Startup script created
echo.
echo Your computer will restart in 10 seconds...
echo After restart, BillSum experiments will start automatically in 30 seconds.
echo.
timeout /t 10

shutdown /r /t 0
