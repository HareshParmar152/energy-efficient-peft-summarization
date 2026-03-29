Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing All 9 XSum Experiments" -ForegroundColor Cyan
Write-Host "20 Steps Only - Quick Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Models: BART, T5, LLaMA" -ForegroundColor Yellow
Write-Host "Methods: LoRA, QLoRA, Adapters" -ForegroundColor Yellow
Write-Host "Steps: 20 (test only)" -ForegroundColor Yellow
Write-Host ""
Write-Host "This will test all 9 configurations quickly" -ForegroundColor Green
Write-Host "to verify everything works before full training." -ForegroundColor Green
Write-Host ""

python test_xsum_all_9_experiments_20steps.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Complete!" -ForegroundColor Green
Write-Host "Check test_logs folder for results" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
