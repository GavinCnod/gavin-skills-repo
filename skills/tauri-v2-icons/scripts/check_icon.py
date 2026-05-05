#!/usr/bin/env python3
"""
Tauri V2 图标检查工具 / Tauri V2 Icon Checker
验证图标文件是否符合 Tauri V2 各平台规范。
Validate icon files against Tauri V2 platform requirements.

参考 / Reference: https://v2.tauri.app/develop/icons/

用法 / Usage:
  python check_icon.py <source.png>     检查源图规格 / check source image
  python check_icon.py <icon.ico>       检查 ICO 图层 / check ICO layers
  python check_icon.py <icon.icns>      检查 ICNS 类型 / check ICNS types
  python check_icon.py <output_dir>/    检查目录下全部图标 / check entire output dir
"""

import struct
import io
import os
import sys
from pathlib import Path
from PIL import Image

_errors = []
_warnings = []


def _err(msg):
    _errors.append(msg)
    print(f"  [FAIL] {msg}")


def _warn(msg):
    _warnings.append(msg)
    print(f"  [WARN] {msg}")


def _ok(msg):
    print(f"  [OK] {msg}")


# ====================================================================
# 源图检查 / Source Image Check
# ====================================================================

def check_source(path):
    """
    Check source PNG against Tauri V2 source requirements.
    检查源图是否符合 Tauri V2 源图要求。
    """
    print(f"\n=== Source / 源图: {path} ===")

    try:
        img = Image.open(path)
    except Exception as e:
        _err(f"Cannot open / 无法打开: {e}")
        return

    w, h = img.size
    mode = img.mode

    # Square / 正方形
    if w == h:
        _ok(f"Square / 正方形: {w}x{h}")
    else:
        _err(f"Not square / 非正方形: {w}x{h}")

    # Size / 尺寸
    if w >= 1024:
        _ok(f"Size >= 1024px / 尺寸 >= 1024px (actual / 实际: {w}px)")
    elif w >= 512:
        _warn(f"Size {w}px < recommended 1024px (min 512px) / "
              f"尺寸 {w}px < 推荐 1024px (最低 512px)")
    else:
        _err(f"Size {w}px too small, min 512px required / "
             f"尺寸 {w}px 过小，最低要求 512px")

    # Color mode / 颜色模式
    if mode == 'RGBA':
        _ok(f"Color mode / 颜色模式: RGBA (32-bit, 8bit/channel / 8bit/通道)")
    elif mode in ('RGB', 'P', 'L', 'CMYK'):
        _warn(f"Color mode / 颜色模式: {mode}. "
              f"Tauri requires RGBA with alpha channel / Tauri 要求 RGBA 带透明通道")
    else:
        _err(f"Color mode / 颜色模式: {mode}. RGBA required / 需要 RGBA")

    # Alpha channel validity / Alpha 通道有效性
    if mode == 'RGBA':
        band = img.getchannel('A')
        lo, hi = band.getextrema()
        if lo == 255:
            _warn("Alpha channel is fully opaque (all 255). "
                  "Confirm this is intended / "
                  "Alpha 通道全为 255 (完全不透明)，请确认这是预期的")


# ====================================================================
# ICO 检查 / ICO Check
# ====================================================================

# Required ICO layer sizes / ICO 必需图层尺寸
REQUIRED_ICO = {16, 24, 32, 48, 64, 256}


def check_ico(path):
    """
    Check ICO file: required layers + 32px first frame order.
    检查 ICO 文件: 必需图层 + 32px 首帧顺序。
    """
    print(f"\n=== ICO: {path} ===")

    try:
        with open(path, 'rb') as f:
            data = f.read()
    except Exception as e:
        _err(f"Cannot read / 无法读取: {e}")
        return

    if len(data) < 6:
        _err("File too small, not a valid ICO / 文件太小，不是有效 ICO")
        return

    reserved, img_type, count = struct.unpack_from('<HHH', data, 0)

    if reserved != 0:
        _warn(f"Reserved field = {reserved} (expected 0) / 保留字段 = {reserved} (应为 0)")
    else:
        _ok("ICO header valid / ICO 文件头有效")

    if img_type != 1:
        _err(f"Type field = {img_type} (expected 1) / 类型字段 = {img_type} (应为 1)")
    else:
        _ok("Type = 1 (icon / 图标)")

    _ok(f"Layer count / 图层数: {count}")

    sizes = []
    for i in range(count):
        off = 6 + i * 16
        if off + 16 > len(data):
            _err(f"Layer {i} dir entry out of bounds / 图层 {i} 目录项越界")
            break
        w = data[off] if data[off] != 0 else 256
        h = data[off + 1] if data[off + 1] != 0 else 256
        sizes.append((w, h))

    size_set = {s[0] for s in sizes}
    print(f"  Size order / 尺寸序列: {[f'{w}x{h}' for w, h in sizes]}")

    missing = REQUIRED_ICO - size_set
    extra = size_set - REQUIRED_ICO

    if not missing:
        _ok(f"All required sizes present / 包含全部必需尺寸: {sorted(REQUIRED_ICO)}")
    else:
        _err(f"Missing sizes / 缺少尺寸: {sorted(missing)}")
    if extra:
        _warn(f"Extra sizes / 额外尺寸: {sorted(extra)}")

    # First frame check — critical Tauri requirement
    # 首帧检查 — Tauri 关键要求
    if sizes and sizes[0][0] == 32:
        _ok("First frame = 32px (Tauri only reads entries()[0] for window icon) / "
            "首帧 = 32px (Tauri 仅读取第一帧用于窗口图标)")
    elif sizes:
        _err(
            f"First frame = {sizes[0][0]}px, expected 32px! / "
            f"首帧 = {sizes[0][0]}px，应为 32px! "
            f"Tauri runtime only reads entries()[0]; window icon will be blurry / "
            f"Tauri 运行时只读 entries()[0]，窗口图标将缩放失真"
        )


# ====================================================================
# ICNS 检查 / ICNS Check
# ====================================================================

# Required ICNS types and their pixel sizes / 必需的 ICNS 类型及像素尺寸
REQUIRED_ICNS = {
    'icp4': 16,  'icp5': 32,  'icp6': 64,
    'ic07': 128, 'ic08': 256, 'ic09': 512, 'ic10': 1024,
    'ic11': 32,  'ic12': 64,  'ic13': 256,  'ic14': 512,
}


def check_icns(path):
    """
    Check ICNS file: required OSTypes and correct pixel dimensions.
    检查 ICNS 文件: 必需的 OSType 和正确的像素尺寸。
    """
    print(f"\n=== ICNS: {path} ===")

    try:
        with open(path, 'rb') as f:
            data = f.read()
    except Exception as e:
        _err(f"Cannot read / 无法读取: {e}")
        return

    if len(data) < 8:
        _err("File too small, not a valid ICNS / 文件太小，不是有效 ICNS")
        return

    magic = data[0:4]
    total_len = struct.unpack_from('>I', data, 4)[0]

    if magic != b'icns':
        _err(f"Invalid magic / 魔数无效: {magic}")
        return
    _ok("ICNS header valid / ICNS 文件头有效")

    if total_len != len(data):
        _warn(f"Declared size {total_len} != actual {len(data)} / "
              f"声明大小 {total_len} != 实际 {len(data)}")
    else:
        _ok(f"File size / 文件大小: {total_len} bytes")

    found = {}
    pos = 8
    while pos + 8 <= len(data):
        etype = data[pos:pos + 4].decode('ascii', errors='replace')
        elen = struct.unpack_from('>I', data, pos + 4)[0]
        if elen < 8 or pos + elen > len(data):
            _warn(f"Entry {etype} bad length, stopping parse / {etype} 长度异常，停止解析")
            break

        if etype == 'TOC ':
            pos += elen
            continue

        # Try reading embedded PNG to get actual pixel size
        # 尝试读取内嵌 PNG 获取实际像素尺寸
        try:
            png = Image.open(io.BytesIO(data[pos + 8:pos + elen]))
            found[etype] = max(png.size)  # should be square / 应为正方形
        except Exception:
            found[etype] = 0
            _warn(f"{etype}: Cannot decode PNG data / PNG 数据无法解析")
        pos += elen

    print(f"  Found types / 找到的类型: {[(t, f'{s}px') for t, s in found.items()]}")

    for rtype, rsize in REQUIRED_ICNS.items():
        if rtype not in found:
            _err(f"Missing ICNS type / 缺少 ICNS 类型: {rtype} ({rsize}px)")
        elif found[rtype] != rsize:
            _err(f"{rtype} size wrong: {found[rtype]}px (expected {rsize}px) / "
                 f"{rtype} 尺寸错误: {found[rtype]}px (应为 {rsize}px)")
        else:
            _ok(f"{rtype}: {rsize}px")

    extra = set(found) - set(REQUIRED_ICNS)
    if extra:
        _warn(f"Extra types / 额外类型: {sorted(extra)}")


# ====================================================================
# 目录全面检查 / Directory Check
# ====================================================================

def check_dir(path):
    """
    Check an entire output directory for all platform icons.
    检查输出目录下的全部平台图标。
    """
    d = Path(path)
    print(f"\n=== Directory / 检查目录: {d} ===")

    # icon.ico / icon.icns
    for f in ['icon.ico', 'icon.icns']:
        fp = d / f
        if fp.exists():
            (check_ico if f.endswith('.ico') else check_icns)(str(fp))
        else:
            _warn(f"Not found / 未找到: {f}")

    # Desktop PNGs / 桌面 PNG
    desk = d / 'desktop'
    if desk.is_dir():
        print(f"\n-- Desktop PNGs / 桌面 PNG: {desk} --")
        for fname, es in [('32x32.png', 32), ('128x128.png', 128),
                          ('128x128@2x.png', 256), ('icon.png', 512)]:
            fp = desk / fname
            if fp.exists():
                try:
                    im = Image.open(fp)
                    if im.size == (es, es):
                        _ok(f"{fname}: {es}x{es}")
                    else:
                        _err(f"{fname}: {im.size} (expected / 应为 {es}x{es})")
                except Exception:
                    _err(f"{fname}: Cannot open / 无法打开")
            else:
                _warn(f"Missing / 缺少: {fname}")

    # Android / Android 图标
    adr = d / 'android'
    if adr.is_dir():
        print(f"\n-- Android: {adr} --")
        for density, ls, fgs in [('mdpi', 48, 108), ('hdpi', 72, 162),
                                  ('xhdpi', 96, 216), ('xxhdpi', 144, 324),
                                  ('xxxhdpi', 192, 432)]:
            dd = adr / density
            if not dd.is_dir():
                _warn(f"Missing density dir / 缺少目录: {density}")
                continue
            for fname, es in [('ic_launcher.png', ls), ('ic_launcher_round.png', ls),
                              ('ic_launcher_foreground.png', fgs)]:
                fp = dd / fname
                if fp.exists():
                    im = Image.open(fp)
                    if im.size == (es, es):
                        _ok(f"{density}/{fname}: {es}x{es}")
                    else:
                        _err(f"{density}/{fname}: {im.size} (expected / 应为 {es}x{es})")
                else:
                    _warn(f"Missing / 缺少: {density}/{fname}")

    # iOS / iOS AppIcon
    iosd = d / 'ios'
    if iosd.is_dir():
        print(f"\n-- iOS: {iosd} --")
        for fname, es in [
            ('AppIcon-20x20@1x.png', 20), ('AppIcon-20x20@2x.png', 40),
            ('AppIcon-20x20@3x.png', 60), ('AppIcon-20x20@2x-1.png', 40),
            ('AppIcon-29x29@1x.png', 29), ('AppIcon-29x29@2x.png', 58),
            ('AppIcon-29x29@3x.png', 87), ('AppIcon-29x29@2x-1.png', 58),
            ('AppIcon-40x40@1x.png', 40), ('AppIcon-40x40@2x.png', 80),
            ('AppIcon-40x40@3x.png', 120), ('AppIcon-40x40@2x-1.png', 80),
            ('AppIcon-60x60@2x.png', 120), ('AppIcon-60x60@3x.png', 180),
            ('AppIcon-76x76@1x.png', 76), ('AppIcon-76x76@2x.png', 152),
            ('AppIcon-83.5x83.5@2x.png', 167), ('AppIcon-512@2x.png', 1024),
        ]:
            fp = iosd / fname
            if not fp.exists():
                _warn(f"Missing / 缺少: {fname}")
                continue
            try:
                im = Image.open(fp)
                if im.size != (es, es):
                    _err(f"{fname}: {im.size} (expected / 应为 {es}x{es})")
                elif im.mode != 'RGB':
                    _warn(f"{fname}: {es}x{es} but mode={im.mode} "
                          f"(iOS should have no alpha / iOS 应无透明通道)")
                else:
                    _ok(f"{fname}: {es}x{es} RGB")
            except Exception:
                _err(f"{fname}: Cannot open / 无法打开")


# ====================================================================
# 主入口 / Main Entry
# ====================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        sys.exit(f"[ERROR] Path not found / 路径不存在: {path}")

    if os.path.isdir(path):
        check_dir(path)
    else:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.ico':
            check_ico(path)
        elif ext == '.icns':
            check_icns(path)
        elif ext == '.png':
            # Large PNG -> source check; small PNG -> basic info
            # 大图 -> 源图检查; 小图 -> 仅显示基本信息
            img = Image.open(path)
            if max(img.size) >= 256:
                check_source(path)
            else:
                print(f"\n=== PNG: {path} ===")
                print(f"  Size / 尺寸: {img.size[0]}x{img.size[1]}  "
                      f"|  Mode / 模式: {img.mode}")
                _warn("Small PNG, cannot determine usage; showing basic info only / "
                      "小尺寸 PNG，无法判断用途，仅显示基本信息")
        else:
            _err(f"Unsupported file type / 不支持的类型: {ext}")

    # Summary / 汇总
    print(f"\n{'=' * 50}")
    nerr, nwarn = len(_errors), len(_warnings)
    if nerr == 0 and nwarn == 0:
        print("[OK] All checks passed / 全部检查通过")
    elif nerr == 0:
        print(f"[OK] Passed ({nwarn} warning(s) / 个警告)")
    else:
        print(f"[FAIL] {nerr} error(s), {nwarn} warning(s) / {nerr} 个错误, {nwarn} 个警告")
        sys.exit(1)


if __name__ == '__main__':
    main()
