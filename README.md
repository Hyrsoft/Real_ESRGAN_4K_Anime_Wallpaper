# Real-ESRGAN 4K Anmie Wallpaper

一键生成高质量 4K 二次元壁纸的工具。

## 功能特性


- 使用 Real-ESRGAN AI 模型进行 4 倍超分辨率放大
- 智能 Fill 策略缩放，确保壁纸填满 4K 屏幕（3840×2160）无黑边

## 环境要求

- Python 3.6+
- FFmpeg（用于高质量缩放）

## 快速开始

### 1. 下载 Real-ESRGAN 可执行文件

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

### 2. 添加执行权限（macOS / Linux）

```bash
chmod +x realesrgan-ncnn-vulkan-20220424-macos/realesrgan-ncnn-vulkan
# 或
chmod +x realesrgan-ncnn-vulkan-20220424-ubuntu/realesrgan-ncnn-vulkan
```

### 3. 放置图片

将你想要转换的二次元图片放到项目根目录下。

### 4. 运行脚本

```bash
python upscale_pro.py
```

按提示选择图片，等待处理完成即可得到 `*_4k_wallpaper.png`。

## 工作原理

```
原始图片 → [Real-ESRGAN 4x 放大] → 超高分辨率图片 → [FFmpeg Fill 缩放] → 4K 壁纸
```

1. **平台检测**：自动识别当前操作系统并选择对应的可执行文件
2. **AI 超分放大**：使用 `realesrgan-x4plus-anime` 模型将图片放大 4 倍
3. **Fill 策略缩放**：
   - 计算图片宽高比与 4K 屏幕（16:9）的差异
   - 若图片更宽，以高度 2160 为基准缩放
   - 若图片更高，以宽度 3840 为基准缩放
   - 使用 Lanczos 算法保证缩放质量

## 致谢

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 强大的 AI 图像超分辨率工具
- [FFmpeg](https://ffmpeg.org/) - 多媒体处理瑞士军刀

## 许可证

[MIT License](LICENSE)
