# Real-ESRGAN 4K Anmie Wallpaper

一键生成高质量 4K 二次元壁纸的工具。

## 功能特性

- 使用 Real-ESRGAN AI 模型进行 4 倍超分辨率放大
- 可选缩放策略：
  - **保持原有比例**：4K DPI，保留原始纵横比，适合各种尺寸的图片
  - **裁剪成标准 4K**：输出固定 3840×2160 分辨率，适合全屏显示
- 自动平台检测，支持 macOS、Linux、Windows

## 环境要求

- Python 3.6+
- FFmpeg（用于高质量缩放）

## 快速开始

### 方式一：自动初始化（推荐）

#### macOS / Linux

在项目根目录打开终端，运行：

```bash
chmod +x setup.sh
./setup.sh
```

脚本会自动：
- 检测操作系统（macOS 或 Linux）
- 下载对应的 Real-ESRGAN 预编译包
- 解压到正确位置
- 设置执行权限

#### Windows

在项目根目录打开 PowerShell，运行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

脚本会自动：
- 下载 Windows 版本的 Real-ESRGAN
- 解压到正确位置
- 完成初始化

### 方式二：手动下载（如遇网络问题）

#### 1. 下载 Real-ESRGAN 可执行文件

前往 [Real-ESRGAN README](https://github.com/xinntao/Real-ESRGAN) 下载对应平台的预编译包：

- **macOS**: `realesrgan-ncnn-vulkan-*-macos.zip`
- **Linux**: `realesrgan-ncnn-vulkan-*-ubuntu.zip`
- **Windows**: `realesrgan-ncnn-vulkan-*-windows.zip`

下载后解压到项目根目录，目录结构应如下：

```
Real_ESRGAN_4k_Anime_wallpaper/
├── upscale_pro.py
├── realesrgan-ncnn-vulkan-20220424-macos/
│   ├── realesrgan-ncnn-vulkan
│   └── models/
├── realesrgan-ncnn-vulkan-20220424-ubuntu/
│   ├── realesrgan-ncnn-vulkan
│   └── models/
└── realesrgan-ncnn-vulkan-20220424-windows/
    ├── realesrgan-ncnn-vulkan.exe
    └── models/
```

#### 2. 添加执行权限（macOS / Linux）

```bash
chmod +x realesrgan-ncnn-vulkan-20220424-macos/realesrgan-ncnn-vulkan
# 或
chmod +x realesrgan-ncnn-vulkan-20220424-ubuntu/realesrgan-ncnn-vulkan
```

#### 3. 放置图片

将你想要转换的二次元图片放到项目根目录下。

### 运行主程序

使用上述任一初始化方式完成 Real-ESRGAN 的配置后，放置图片并运行：

```bash
python upscale_pro.py
```

按提示进行以下操作：

1. **选择输入图片**：从列表中选择要处理的二次元图片
2. **选择输出方式**：
   - `[1]` 保持原有比例 (缩放至 4K 框内) - 保留原始纵横比，不会被裁剪
   - `[2]` 裁剪成标准 4K (3840×2160) - 从中心裁剪出标准 4K 分辨率
3. 等待处理完成，得到 `*_4k_wallpaper.png`

## 工作原理

```
原始图片 → [Real-ESRGAN 4x 放大] → 超高分辨率图片 → [输出方式选择] → 4K 壁纸
```

1. **平台检测**：自动识别当前操作系统并选择对应的可执行文件
2. **AI 超分放大**：使用 `realesrgan-x4plus-anime` 模型将图片放大 4 倍
3. **灵活处理方式**：
   
   **方式一：保持原有比例**
   - 计算图片宽高比与 4K 屏幕（16:9）的差异
   - 若图片更宽，以高度 2160 为基准缩放
   - 若图片更高，以宽度 3840 为基准缩放
   - 使用 Lanczos 算法保证缩放质量
   
   **方式二：裁剪成标准 4K**
   - 计算缩放比例，确保能覆盖整个 3840×2160 目标区域
   - 从中心位置裁剪出标准 4K 分辨率内容
   - 同样使用 Lanczos 算法保证质量

## 致谢

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 强大的 AI 图像超分辨率工具
- [FFmpeg](https://ffmpeg.org/) - 多媒体处理瑞士军刀

## 许可证

[MIT License](LICENSE)
