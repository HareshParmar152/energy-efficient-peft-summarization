@echo off
echo ========================================
echo Download Datasets Locally
echo ========================================
echo.
echo This will download datasets to:
echo E:\Pending Experiment data\local_datasets\
echo.
echo Attempting to download:
echo - SAMSum (conversational)
echo - Multi-News (multi-document)
echo - BillSum (legislative)
echo - ArXiv (scientific papers)
echo.
pause

REM Deactivate virtual environment if active
if defined VIRTUAL_ENV (
    echo Deactivating virtual environment...
    call deactivate
)

echo.
echo Starting downloads...
echo.

python download_datasets_locally.py

echo.
echo ========================================
echo Download complete!
echo Check output above to see which datasets succeeded.
echo ========================================
pause
