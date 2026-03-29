@echo off
echo ========================================
echo Installing Dependencies for XSum Test
echo ========================================
echo.
echo Activating virtual environment...
call research_env\Scripts\activate.bat

echo.
echo Installing PyTorch and dependencies...
echo This may take several minutes...
echo.

pip install -r requirements_xsum_test.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run: RUN_TEST_XSUM_ALL_9.bat
echo.
pause
