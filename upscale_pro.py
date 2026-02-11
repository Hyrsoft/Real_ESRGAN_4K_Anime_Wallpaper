#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

# --- 配置区 ---
# 支持的图片格式
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

# 目标分辨率配置
TARGET_WIDTH = 3840
TARGET_HEIGHT = 2160
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT # 1.777...

# 可执行文件配置
# 如果为相对路径，则相对于脚本所在目录；如果为绝对路径，则使用绝对路径
EXE_NAME_MACOS = "realesrgan-ncnn-vulkan-20220424-macos/realesrgan-ncnn-vulkan"
EXE_NAME_LINUX = "realesrgan-ncnn-vulkan-20220424-ubuntu/realesrgan-ncnn-vulkan"
EXE_NAME_WINDOWS = "realesrgan-ncnn-vulkan-20220424-windows/realesrgan-ncnn-vulkan.exe"
EXE_PATH = None  # 默认为 None，表示使用上述配置；可在此设置自定义路径

# models 路径配置
# 根据不同平台的可执行文件位置配置对应的 models 路径
MODELS_PATH_MACOS = "realesrgan-ncnn-vulkan-20220424-macos/models"
MODELS_PATH_LINUX = "realesrgan-ncnn-vulkan-20220424-ubuntu/models"
MODELS_PATH_WINDOWS = "realesrgan-ncnn-vulkan-20220424-windows/models"
MODELS_PATH = None  # 默认为 None，自动根据平台选择；可在此设置自定义路径

def get_image_info(image_path):
    """使用 ffprobe 获取图片宽高"""
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', str(image_path)
    ]
    result = subprocess.check_output(cmd).decode('utf-8').strip()
    w, h = map(int, result.split('x'))
    return w, h

def main():
    curr_dir = Path(__file__).parent.absolute()
    
    # 1. 自动检测平台并获取可执行文件
    print("--- Step 1: 平台检测 ---")
    
    # 自动检测操作系统
    if sys.platform == "darwin":
        platform_name = "macOS"
        exe_name = EXE_NAME_MACOS
        models_name = MODELS_PATH_MACOS
    elif sys.platform.startswith("linux"):
        platform_name = "Linux"
        exe_name = EXE_NAME_LINUX
        models_name = MODELS_PATH_LINUX
    elif sys.platform.startswith("win"):
        platform_name = "Windows"
        exe_name = EXE_NAME_WINDOWS
        models_name = MODELS_PATH_WINDOWS
    else:
        platform_name = "Unknown"
        exe_name = EXE_NAME_MACOS
        models_name = MODELS_PATH_MACOS
    
    print(f"检测到平台: {platform_name}")
    
    # 确定可执行文件路径
    if EXE_PATH is None:
        # 默认在脚本所在目录查找
        exe_path = curr_dir / exe_name
    else:
        # 使用配置的路径
        exe_path = Path(EXE_PATH)
        if not exe_path.is_absolute():
            exe_path = curr_dir / exe_path
    
    if not exe_path.exists():
        print(f"错误: 找不到可执行文件 {exe_path}")
        return

    # 确定 models 路径
    if MODELS_PATH is None:
        # 默认根据平台选择对应的 models 路径
        models_path = curr_dir / models_name
    else:
        # 使用配置的路径
        models_path = Path(MODELS_PATH)
        if not models_path.is_absolute():
            models_path = curr_dir / models_path

    # 2. 图片选择
    print("\n--- Step 2: 选择输入图片 ---")
    imgs = sorted([f for f in curr_dir.iterdir() if f.suffix.lower() in EXTENSIONS])
    
    if not imgs:
        print("当前目录下没有找到图片文件。")
        return

    for i, img in enumerate(imgs):
        print(f"[{i+1}] {img.name}")
    
    try:
        idx = int(input(f"请输入图片编号 (1-{len(imgs)}): ")) - 1
        input_img = imgs[idx]
    except (ValueError, IndexError):
        print("选择无效。")
        return

    # 3. 执行 Real-ESRGAN 放大 (4倍)
    output_upscaled = curr_dir / f"{input_img.stem}_upscaled.png"
    print(f"\n--- Step 3: 正在进行 AI 超分放大 (x4)... ---", flush=True)
    print(f"输入图片: {input_img}", flush=True)
    print(f"输出图片: {output_upscaled}", flush=True)
    print(f"Models 路径: {models_path}", flush=True)
    
    # -n realesrgan-x4plus-anime 是针对二次元图片的推荐模型
    upscale_cmd = [
        str(exe_path),
        "-i", str(input_img),
        "-o", str(output_upscaled),
        "-n", "realesrgan-x4plus-anime",
        "-s", "4",
        "-m", str(models_path)
    ]
    print(f"执行命令: {' '.join(upscale_cmd)}", flush=True)
    # 实时打印输出
    process = subprocess.Popen(upscale_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(line, end='', flush=True)
    process.wait()
    
    if process.returncode != 0:
        print(f"错误: realesrgan 执行失败 (返回码: {process.returncode})", flush=True)
        return
    
    if not output_upscaled.exists():
        print(f"错误: 输出文件未生成 {output_upscaled}", flush=True)
        return
    
    print(f"✅ 超分完成！", flush=True)

    # 4. 计算比例并执行 FFmpeg 缩放
    print(f"\n--- Step 4: 正在根据比例执行 Fill 策略缩放... ---")
    w, h = get_image_info(output_upscaled)
    current_ratio = w / h
    
    final_output = curr_dir / f"{input_img.stem}_4k_wallpaper.png"

    # 根据文档逻辑判断
    if current_ratio > TARGET_RATIO:
        # 情况一：图片更宽，以高度 2160 为基准
        vf_scale = f"scale=-1:{TARGET_HEIGHT}:flags=lanczos"
    else:
        # 情况二：图片更高，以宽度 3840 为基准
        vf_scale = f"scale={TARGET_WIDTH}:-1:flags=lanczos"

    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", str(output_upscaled),
        "-vf", vf_scale,
        str(final_output)
    ]
    
    subprocess.run(ffmpeg_cmd)
    
    # 清理中间文件 (可选)
    if output_upscaled.exists():
        os.remove(output_upscaled)

    print(f"\n✅ 处理完成！")
    print(f"最终壁纸: {final_output.name}")

if __name__ == "__main__":
    main()
