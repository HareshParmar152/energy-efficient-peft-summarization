@echo off
echo ========================================
echo XSum Experiments Status Check
echo ========================================
echo.

powershell -Command "$results = Get-ChildItem 'E:\Pending Experiment data\XSum_Experiments' -Recurse -Filter '*_results.json'; Write-Host 'Completed Experiments:' -ForegroundColor Green; Write-Host ''; foreach ($file in $results) { $data = Get-Content $file.FullName | ConvertFrom-Json; $status = if ($data.status -eq 'success') {'[OK]'} else {'[FAIL]'}; $time = [math]::Round($data.train_runtime_minutes, 1); Write-Host \"$status $($data.experiment_id) - $($data.method) - Time: $time min\"; }; Write-Host ''; Write-Host 'Expected Experiments:' -ForegroundColor Yellow; Write-Host 'E1, E2, E3 (BART), E13, E14, E15 (T5), E25, E26, E27 (LLaMA)'; Write-Host ''; $completed = $results.Count; Write-Host \"Progress: $completed/9 experiments completed\" -ForegroundColor Cyan"

echo.
pause
