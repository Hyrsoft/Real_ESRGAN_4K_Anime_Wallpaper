# Real-ESRGAN 4K Anime Wallpaper 自动初始化脚本 (Windows)
# PowerShell 脚本

$ErrorActionPreference = "Stop"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Real-ESRGAN 4K Wallpaper 初始化" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 获取脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$packageName = "realesrgan-ncnn-vulkan-20220424-windows"
$downloadUrl = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip"
$zipFile = "$packageName.zip"

Write-Host "✓ Windows 系统检测完成" -ForegroundColor Green

# 检查是否已存在
if (Test-Path $packageName) {
    Write-Host "✓ $packageName 已存在，跳过下载" -ForegroundColor Green
} else {
    Write-Host "📥 正在下载 Real-ESRGAN (Windows)..." -ForegroundColor Yellow
    Write-Host "   下载链接: $downloadUrl" -ForegroundColor Gray
    
    try {
        # 使用 System.Net.ServicePointManager 确保支持 TLS 1.2
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor [System.Net.SecurityProtocolType]::Tls12
        
        # 下载文件
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile -ErrorAction Stop
        
        Write-Host "📦 正在解压..." -ForegroundColor Yellow
        
        # 创建目标目录
        if (-not (Test-Path $packageName)) {
            New-Item -ItemType Directory -Path $packageName | Out-Null
        }
        
        # 使用 .NET 的 ZipFile 类解压到指定目录
        [System.IO.Compression.ZipFile]::ExtractToDirectory($zipFile, $packageName, $true)
        
        # 删除 zip 文件
        Remove-Item $zipFile -Force
        
        Write-Host "✓ 解压完成" -ForegroundColor Green
    } catch {
        Write-Host "❌ 下载或解压失败:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host "" -ForegroundColor Red
        Write-Host "请手动下载并解压:" -ForegroundColor Yellow
        Write-Host $downloadUrl -ForegroundColor Cyan
        exit 1
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✅ 初始化完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步:" -ForegroundColor Cyan
Write-Host "1. 将二次元图片放到项目根目录" -ForegroundColor White
Write-Host "2. 运行: python upscale_pro.py" -ForegroundColor White
Write-Host ""
