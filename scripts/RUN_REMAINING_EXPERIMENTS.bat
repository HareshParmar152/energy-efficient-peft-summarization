@echo off
title XSum - Final 4 Experiments (E15, E25, E26, E27)
cls
echo ========================================
echo XSUM REMAINING EXPERIMENTS
echo ========================================
echo.
echo This will run the final 4 experiments:
echo   E15 - T5 + Adapters
echo   E25 - LLaMA + LoRA
echo   E26 - LLaMA + QLoRA
echo   E27 - LLaMA + Adapters
echo.
echo The script will automatically skip any completed experiments.
echo.
echo Estimated time: 6-10 hours total
echo.
echo ========================================
echo.

echo Checking current status...
powershell -Command "$completed = @(); Get-ChildItem 'E:\Pending Experiment data\XSum_Experiments' -Recurse -Filter '*_results.json' | ForEach-Object { $data = Get-Content $_.FullName | ConvertFrom-Json; if ($data.status -eq 'success') { $completed += $data.experiment_id } }; Write-Host \"Completed: $($completed.Count)/9\" -ForegroundColor Green; $all = @('E1','E2','E3','E13','E14','E15','E25','E26','E27'); $pending = $all | Where-Object {$completed -notcontains $_}; Write-Host \"Will run: [$($pending -join ', ')]\" -ForegroundColor Yellow"

echo.
echo ========================================
echo.
echo Starting experiments...
echo DO NOT CLOSE THIS WINDOW
echo.
echo ========================================
echo.

C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -u run_xsum_all_9_experiments_2000steps.py

echo.
echo ========================================
echo All Experiments Complete!
echo ========================================
echo.
echo Check results at:
echo E:\Pending Experiment data\XSum_Experiments\
echo.
pause
