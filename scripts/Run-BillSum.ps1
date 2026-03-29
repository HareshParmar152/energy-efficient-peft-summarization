# BillSum Experiments - PowerShell Runner
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "BillSum Experiments - PowerShell Runner" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Deactivate venv if active
if ($env:VIRTUAL_ENV) {
    Write-Host "Deactivating .venv..." -ForegroundColor Yellow
    deactivate
    $env:VIRTUAL_ENV = $null
    $env:PATH = $env:PATH -replace [regex]::Escape("$env:VIRTUAL_ENV\Scripts;"), ""
}

Write-Host "Checking Python..." -ForegroundColor Green
python --version
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"

Write-Host ""
Write-Host "Starting BillSum experiments..." -ForegroundColor Green
Write-Host "Auto-skip: E1, E3, E13, E15 (completed)" -ForegroundColor Gray
Write-Host "Will retry: E25, E27, E2, E14, E26 (failed)" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to cancel, or any key to start..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
python run_billsum_all_9_experiments_2000steps.py

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Experiments completed!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
