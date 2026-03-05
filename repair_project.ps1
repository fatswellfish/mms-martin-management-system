# repair_project.ps1
Write-Host "开始修复 MMS 项目文件..." -ForegroundColor Cyan

# 1. 备份整个 models 目录
$modelsDir = "C:\Users\Martin WANG\Desktop\Project\mms\fieldops\models"
$backupDir = "C:\Users\Martin WANG\Desktop\Project\backup_models_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
if (Test-Path $modelsDir) {
    Copy-Item $modelsDir $backupDir -Recurse -Force
    Write-Host "✅ 已备份到: $backupDir" -ForegroundColor Green
}

# 2. 修复所有模型文件
$modelFiles = Get-ChildItem $modelsDir -Filter "*.py" | ForEach-Object { $_.FullName }

foreach ($file in $modelFiles) {
    Write-Host "处理: $([System.IO.Path]::GetFileName($file))" -ForegroundColor Gray
    
    # 读取并清理
    $bytes = [System.IO.File]::ReadAllBytes($file)
    $cleanBytes = $bytes | Where-Object { $_ -ne 0 }
    
    # 重新写入
    [System.IO.File]::WriteAllBytes($file, [byte[]]$cleanBytes)
    
    # 转换为 UTF-8
    $content = Get-Content $file -Encoding UTF8 -Raw
    Set-Content $file $content -Encoding UTF8
}

Write-Host "`n✅ 所有模型文件已修复" -ForegroundColor Green
Write-Host "请重新运行: python -m mms.main" -ForegroundColor White