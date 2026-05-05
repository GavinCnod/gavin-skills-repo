#!/usr/bin/env python3
"""
Tauri V2 图标生成工具 / Tauri V2 Icon Generator
从一张 RGBA PNG 源图生成所有平台所需图标。
Generate all platform icons from a single RGBA PNG source image.

用法 / Usage:
  python generate_icon.py <source.png> [-o <output_dir>]

参考 / Reference: https://v2.tauri.app/develop/icons/

生成内容 / Output:
  icon.ico         Windows  (16/24/32/48/64/256px, 32px as first frame / 首帧)
  icon.icns        macOS    (icp4~ic14 all PNG types / 全部 PNG 类型)
  desktop/         Linux    (32x32 / 128x128 / 128x128@2x / icon.png)
  android/         Android  (mdpi~xxxhdpi density buckets / 各密度桶)
  ios/             iOS      (AppIcon set, no alpha channel / 无透明通道)
"""

import struct
import io
import os
import sys
import argparse
from pathlib import Path
from PIL import Image

# ====================================================================
# 常量 / Constants
# ====================================================================

# Windows ICO layers: 32px must be the first frame
# Tauri runtime only reads ICO entries()[0] for window icon
# 32px 必须为首帧 — Tauri 运行时只读取第一帧用于窗口图标
# see: https://github.com/tauri-apps/tauri/issues/14596
ICO_SIZES = [32, 16, 24, 48, 64, 256]

# macOS ICNS types: (OSType, actual pixels / 实际像素)
# see: https://docs.rs/tauri-icns/latest/tauri_icns/
ICNS_TYPES = [
    ('icp4', 16),    # 16x16
    ('icp5', 32),    # 32x32
    ('icp6', 64),    # 64x64
    ('ic07', 128),   # 128x128
    ('ic08', 256),   # 256x256
    ('ic09', 512),   # 512x512
    ('ic10', 1024),  # 512x512@2x
    ('ic11', 32),    # 16x16@2x -> 32px
    ('ic12', 64),    # 32x32@2x -> 64px
    ('ic13', 256),   # 128x128@2x -> 256px
    ('ic14', 512),   # 256x256@2x -> 512px
]

# Desktop PNGs: (filename / 文件名, size / 尺寸)
DESKTOP_PNGS = [
    ('32x32.png', 32),
    ('128x128.png', 128),
    ('128x128@2x.png', 256),
    ('icon.png', 512),
]

# Android density buckets: (dir name / 目录名, launcher size, foreground size)
# Android 密度桶
ANDROID_SIZES = [
    ('mdpi',    48, 108),
    ('hdpi',    72, 162),
    ('xhdpi',   96, 216),
    ('xxhdpi', 144, 324),
    ('xxxhdpi', 192, 432),
]

# iOS AppIcon: (logical size / 逻辑尺寸, scale / 缩放, pixel size / 像素尺寸, is_extra)
IOS_SIZES = [
    (20,   1,  20,  False),
    (20,   2,  40,  False),
    (20,   3,  60,  False),
    (20,   2,  40,  True),
    (29,   1,  29,  False),
    (29,   2,  58,  False),
    (29,   3,  87,  False),
    (29,   2,  58,  True),
    (40,   1,  40,  False),
    (40,   2,  80,  False),
    (40,   3, 120,  False),
    (40,   2,  80,  True),
    (60,   2, 120,  False),
    (60,   3, 180,  False),
    (76,   1,  76,  False),
    (76,   2, 152,  False),
    (83.5, 2, 167,  False),
    (512,  2, 1024, False),
]

# ====================================================================
# 工具函数 / Utilities
# ====================================================================

def validate_source(img_path):
    """
    验证源图并返回 RGBA PIL Image / Validate source and return RGBA PIL Image
    """
    if not os.path.exists(img_path):
        sys.exit(f"[ERROR] File not found / 文件不存在: {img_path}")

    try:
        img = Image.open(img_path)
    except Exception as e:
        sys.exit(f"[ERROR] Cannot open image / 无法打开图像: {e}")

    if img.mode != 'RGBA':
        print(f"[INFO] Mode {img.mode} -> converting to RGBA / 模式 {img.mode} -> 转为 RGBA")
        img = img.convert('RGBA')

    w, h = img.size
    if w != h:
        sys.exit(
            f"[ERROR] Image is not square ({w}x{h}). "
            f"Tauri V2 requires a square source image / "
            f"非正方形 ({w}x{h})，Tauri V2 要求正方形源图"
        )
    if w < 512:
        sys.exit(
            f"[ERROR] Size {w}px is too small. "
            f"Minimum 512px required / 尺寸 {w}px 过小，最低要求 512px"
        )
    if w != 1024:
        print(
            f"[INFO] Recommended size is 1024x1024, current is {w}x{w} / "
            f"推荐 1024x1024，当前 {w}x{w}"
        )

    print(f"[OK] Source / 源图: {w}x{w} {img.mode}")
    return img


def _resize(img, size):
    """
    Resize RGBA image and return PNG bytes / 缩放 RGBA 图像并返回 PNG 字节
    """
    if img.size == (size, size):
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    r = img.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    r.save(buf, format='PNG')
    return buf.getvalue()


def _resize_no_alpha(img, size):
    """
    Resize and composite onto white background (iOS has no alpha channel).
    缩放并合成白底 (iOS 无透明通道)，返回 PNG 字节。
    """
    r = img.resize((size, size), Image.LANCZOS)
    bg = Image.new('RGB', (size, size), (255, 255, 255))
    bg.paste(r, (0, 0), r)
    buf = io.BytesIO()
    bg.save(buf, format='PNG')
    return buf.getvalue()


# ====================================================================
# 各格式生成 / Format Generators
# ====================================================================

def generate_ico(img, output_path):
    """
    Generate Windows .ico — 6 layers, 32px as first frame.
    生成 Windows .ico — 6 层，32px 首帧。
    """
    frames = [(s, _resize(img, s)) for s in ICO_SIZES]

    count = len(frames)
    dir_offset = 6 + count * 16   # header(6) + directory(count * 16) / 文件头 + 目录表

    dir_bytes = b''
    img_blob = b''
    off = dir_offset

    for size, png_data in frames:
        # width/height: 0 means 256 in ICO spec / 0 表示 256
        w = 0 if size >= 256 else size
        h = 0 if size >= 256 else size
        entry = struct.pack('<BBBBHHII',
            w, h,               # width, height (0 = 256)
            0, 0,               # color_count, reserved / 颜色数, 保留
            1, 32,              # planes, bit_count (32 = PNG data / PNG 数据)
            len(png_data), off, # image_size, image_offset / 图像大小, 图像偏移
        )
        dir_bytes += entry
        img_blob += png_data
        off += len(png_data)

    # ICO header: reserved(2)=0, type(2)=1, count(2)
    header = struct.pack('<HHH', 0, 1, count)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'wb') as f:
        f.write(header + dir_bytes + img_blob)

    sizes_str = ', '.join(str(s) for s in ICO_SIZES)
    print(
        f"  [ICO] {output_path}  "
        f"({count} frames / 帧: {sizes_str}, first frame / 首帧: 32px)"
    )


def generate_icns(img, output_path):
    """
    Generate macOS .icns — 11 PNG types + TOC entry.
    生成 macOS .icns — 11 个 PNG 类型 + TOC 条目。
    """
    entries = []
    for ostype, size in ICNS_TYPES:
        png_data = _resize(img, size)
        # Entry: type(4) + length(4, includes 8-byte header) + data
        # 条目: 类型(4) + 长度(4, 含自身8字节头) + 数据
        entry_len = 8 + len(png_data)
        entry = ostype.encode('ascii') + struct.pack('>I', entry_len) + png_data
        entries.append(entry)

    # TOC entry / TOC 条目
    toc_types = b''.join(t[0].encode('ascii') for t in ICNS_TYPES)
    toc = b'TOC ' + struct.pack('>I', 8 + len(toc_types)) + toc_types
    entries.insert(0, toc)

    # ICNS header: magic 'icns'(4) + total_length(4) / 文件头
    total = 8 + sum(len(e) for e in entries)
    header = b'icns' + struct.pack('>I', total)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'wb') as f:
        f.write(header)
        for e in entries:
            f.write(e)

    print(f"  [ICNS] {output_path}  ({len(ICNS_TYPES)} types / 个类型)")


def generate_desktop_pngs(img, output_dir):
    """
    Generate desktop PNG icons for Linux / 生成 Linux 桌面 PNG 图标
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for fname, size in DESKTOP_PNGS:
        with open(out / fname, 'wb') as f:
            f.write(_resize(img, size))
    print(f"  [Desktop] {output_dir}/  ({len(DESKTOP_PNGS)} files / 个文件)")


def generate_android(img, output_dir):
    """
    Generate Android density-bucket icons / 生成 Android 各密度桶图标
    """
    out = Path(output_dir)
    for density, ls, fgs in ANDROID_SIZES:
        d = out / density
        d.mkdir(parents=True, exist_ok=True)
        for fname, sz in [('ic_launcher.png', ls),
                          ('ic_launcher_round.png', ls),
                          ('ic_launcher_foreground.png', fgs)]:
            with open(d / fname, 'wb') as f:
                f.write(_resize(img, sz))
    print(
        f"  [Android] {output_dir}/  "
        f"({len(ANDROID_SIZES)} buckets x 3 icons / 个密度桶 x 3 图标)"
    )


def generate_ios(img, output_dir):
    """
    Generate iOS AppIcon set (no alpha, white background).
    生成 iOS AppIcon 集 (无透明通道，白底合成)。
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for logical, scale, px, is_extra in IOS_SIZES:
        suffix = f'@{scale}x' + ('-1' if is_extra else '')
        if logical == 512:
            # Apple special case: "AppIcon-512@2x.png" without "x512"
            name = f'AppIcon-512@2x.png'
        else:
            name = f'AppIcon-{logical}x{logical}{suffix}.png'.replace('.0x', 'x')
        with open(out / name, 'wb') as f:
            f.write(_resize_no_alpha(img, px))
    print(
        f"  [iOS] {output_dir}/  "
        f"({len(IOS_SIZES)} AppIcons, no alpha / 无 Alpha)"
    )


# ====================================================================
# 主入口 / Main Entry
# ====================================================================

def main():
    parser = argparse.ArgumentParser(
        description=(
            'Tauri V2 Icon Generator — generate all platform icons from a RGBA PNG source / '
            'Tauri V2 图标生成工具 — 从 RGBA PNG 源图生成全部平台图标'
        )
    )
    parser.add_argument(
        'source',
        help='Source PNG file (1024x1024 RGBA recommended) / 源 PNG 文件 (推荐 1024x1024 RGBA)'
    )
    parser.add_argument(
        '-o', '--output', default='icons',
        help='Output directory (default: icons/) / 输出目录 (默认: icons/)'
    )
    parser.add_argument(
        '--no-desktop', action='store_true',
        help='Skip desktop PNGs / 跳过桌面 PNG'
    )
    parser.add_argument(
        '--no-android', action='store_true',
        help='Skip Android icons / 跳过 Android 图标'
    )
    parser.add_argument(
        '--no-ios', action='store_true',
        help='Skip iOS icons / 跳过 iOS 图标'
    )
    args = parser.parse_args()

    img = validate_source(args.source)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    print(f"\n[INFO] Generating icons to / 生成图标到: {out.absolute()}/\n")

    generate_ico(img, str(out / 'icon.ico'))
    generate_icns(img, str(out / 'icon.icns'))

    if not args.no_desktop:
        generate_desktop_pngs(img, str(out / 'desktop'))
    if not args.no_android:
        generate_android(img, str(out / 'android'))
    if not args.no_ios:
        generate_ios(img, str(out / 'ios'))

    print(f"\n[OK] Done / 完成 -> {out.absolute()}/")


if __name__ == '__main__':
    main()
