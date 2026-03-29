@echo off
echo ========================================
echo XSum Training Progress Monitor
echo ========================================
echo.
echo Monitoring: xsum_output.log
echo Press Ctrl+C to stop monitoring
echo.
echo ========================================
echo.

powershell -Command "Get-Content xsum_output.log -Wait -Tail 30"
