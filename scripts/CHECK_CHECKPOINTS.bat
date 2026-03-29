@echo off
REM ============================================
REM Checkpoint Verification
REM Checks if all required checkpoints exist
REM ============================================

echo ============================================
echo CHECKPOINT VERIFICATION
echo ============================================
echo.
echo Checking if all checkpoints exist...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run check
python check_checkpoints.py

echo.
pause
