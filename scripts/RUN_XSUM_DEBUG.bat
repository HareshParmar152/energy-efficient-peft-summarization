@echo off
echo Starting XSum experiments with error capture...
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe run_xsum_all_9_experiments_2000steps.py 2>&1 | tee xsum_console_output.txt

echo.
echo Script finished. Check xsum_console_output.txt for full output.
pause
