# session_manager.ps1
Write-Host "=== OpenClaw 会话管理 ===" -ForegroundColor Cyan

# 1. 列出当前会话
Write-Host "`n当前活动会话:" -ForegroundColor Yellow
openclaw sessions list

# 2. 建议清理
Write-Host "`n建议:" -ForegroundColor Green
Write-Host "1. 如果单个会话消息超过20条，建议开始新会话" -ForegroundColor Gray
Write-Host "2. 重要结论请保存到项目文件中" -ForegroundColor Gray
Write-Host "3. 非必要对话可以定期清理" -ForegroundColor Gray

# 3. 创建新会话的快速指令
Write-Host "`n快速创建新会话:" -ForegroundColor Cyan
Write-Host "在Web界面点击: 左上角菜单 → 新建会话" -ForegroundColor Gray