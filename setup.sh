#!/bin/bash

# Real-ESRGAN 4K Anime Wallpaper 自动初始化脚本
# 支持 macOS 和 Linux 系统

set -e

echo "================================"
echo "Real-ESRGAN 4K Wallpaper 初始化"
echo "================================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    PACKAGE_NAME="realesrgan-ncnn-vulkan-20220424-macos"
    DOWNLOAD_URL="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-macos.zip"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    PACKAGE_NAME="realesrgan-ncnn-vulkan-20220424-ubuntu"
    DOWNLOAD_URL="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip"
else
    echo "❌ 不支持的操作系统: $OSTYPE"
    echo "请使用 setup.ps1 脚本在 Windows 上运行"
    exit 1
fi

echo "✓ 检测到操作系统: $OS_TYPE"

# 检查是否已存在
if [ -d "$PACKAGE_NAME" ]; then
    echo "✓ $PACKAGE_NAME 已存在，跳过下载"
else
    echo "📥 正在下载 Real-ESRGAN ($OS_TYPE)..."
    
    # 检查 curl 或 wget
    if command -v curl &> /dev/null; then
        curl -L -o "${PACKAGE_NAME}.zip" "$DOWNLOAD_URL"
    elif command -v wget &> /dev/null; then
        wget -O "${PACKAGE_NAME}.zip" "$DOWNLOAD_URL"
    else
        echo "❌ 找不到 curl 或 wget，请手动下载:"
        echo "$DOWNLOAD_URL"
        exit 1
    fi
    
    echo "📦 正在解压..."
    mkdir -p "$PACKAGE_NAME"
    unzip -q "${PACKAGE_NAME}.zip" -d "$PACKAGE_NAME"
    rm "${PACKAGE_NAME}.zip"
    echo "✓ 解压完成"
fi

# 添加执行权限
if [ -f "$PACKAGE_NAME/realesrgan-ncnn-vulkan" ]; then
    chmod +x "$PACKAGE_NAME/realesrgan-ncnn-vulkan"
    echo "✓ 已设置执行权限"
fi

echo ""
echo "================================"
echo "✅ 初始化完成！"
echo "================================"
echo ""
echo "下一步："
echo "1. 将二次元图片放到项目根目录"
echo "2. 运行: python upscale_pro.py"
echo ""
