@echo off
title Experiment Status Check
cls
echo ========================================
echo XSUM EXPERIMENTS STATUS
echo ========================================
echo.

powershell -Command "$completed = @(); Get-ChildItem 'E:\Pending Experiment data\XSum_Experiments' -Recurse -Filter '*_results.json' | ForEach-Object { $data = Get-Content $_.FullName | ConvertFrom-Json; if ($data.status -eq 'success') { $completed += $data.experiment_id; $time = [math]::Round($data.train_runtime_minutes, 1); Write-Host \"✓ $($data.experiment_id) - $($data.method) - ${time} min\" -ForegroundColor Green } }; Write-Host ''; $all = @('E1','E2','E3','E13','E14','E15','E25','E26','E27'); $pending = $all | Where-Object {$completed -notcontains $_}; Write-Host \"Completed: $($completed.Count)/9\" -ForegroundColor Green; Write-Host \"Pending: [$($pending -join ', ')]\" -ForegroundColor Yellow; Write-Host ''; Write-Host 'Press any key to refresh...'"

pause >nul
goto :eof
