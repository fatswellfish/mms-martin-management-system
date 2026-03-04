# monitor_en.ps1 - 英文版本，无编码问题
while ($true) {
    Clear-Host
    Write-Host "=== [$(Get-Date -Format 'HH:mm:ss')] AI Workspace File Changes ===" -ForegroundColor Cyan
    git status --short
    Write-Host "`n(Auto-refreshing every 10 seconds. Press Ctrl+C to exit.)" -ForegroundColor Gray
    Start-Sleep -Seconds 10
}