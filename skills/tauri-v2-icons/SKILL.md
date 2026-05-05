---
name: tauri-v2-icons
description: >
  Tauri V2 icon toolkit — validate icon files against Tauri V2 platform requirements
  and generate all required platform icons from a source PNG/SVG.
  Use when: (1) Checking if PNG/ICO/ICNS icon files meet Tauri V2 specs,
  (2) Generating Windows (.ico), macOS (.icns), Linux (.png), Android, and iOS icons
  from a source image, (3) User mentions "Tauri icon", "app icon", "generate icons",
  "check icons", "icon.ico", "icon.icns", "tauri icon 生成", "检查图标".
license: MIT
metadata:
  version: "1.0.0"
  author: GavinCnod
  category: development-automation-tools
---

# Tauri V2 Icon Toolkit

Two scripts covering the full icon workflow for Tauri V2 apps:

- `scripts/check_icon.py` — validate against Tauri V2 specs
- `scripts/generate_icon.py` — generate all platform icons from a source

**Full spec reference:** `references/tauri-icon-spec.md` — read when detailed format requirements are needed beyond what the scripts report.

## Decision: Check or Generate?

- User provides a **single large PNG/SVG** → **Generate** all platform icons
- User provides a **.ico, .icns, or small .png** → **Check** against Tauri V2 specs
- User asks **"is this valid?"** → **Check**
- User asks **"generate/make/create icons"** → **Generate**

## Check Icons

```bash
python scripts/check_icon.py <file-or-directory>
```

| Input | Behavior |
|-------|----------|
| Source PNG (>=256px) | Check square, RGBA, 32-bit, size >=512px |
| `.ico` | Verify 6 required layers (16/24/32/48/64/256) + 32px first frame |
| `.icns` | Verify 11 required OSTypes (icp4~ic14) with correct pixel sizes |
| Output directory | Recursively check ICO, ICNS, desktop PNGs, Android, iOS |

## Generate Icons

```bash
python scripts/generate_icon.py <source.png> [-o <output_dir>]
```

Flags: `--no-desktop`, `--no-android`, `--no-ios`

Requires **Pillow** (`pip install Pillow`). Source must be square RGBA PNG, >=512px (1024px recommended).

Output structure:

```
<output>/
├── icon.ico              # Windows: 6 layers, 32px first
├── icon.icns             # macOS: 11 OSTypes + TOC
├── desktop/              # Linux: 32x32, 128x128, 128x128@2x, icon.png
├── android/{mdpi..xxxhdpi}/  # launcher, round, foreground
└── ios/                  # 18 AppIcons, no alpha (white bg)
```

## SVG Source

SVG is not directly supported. Rasterize to 1024x1024 RGBA PNG first, then run generate:

```python
import cairosvg
cairosvg.svg2png(url="source.svg", write_to="app-icon.png", output_width=1024, output_height=1024)
```

For complex SVGs (gradients, filters), render via a headless browser for accurate rasterization, then convert to RGBA with Pillow.

## Common Pitfalls

- **ICO first frame**: Tauri runtime only reads `entries()[0]`. If 256px is first, window icon scales down → blurry. Always place 32px first.
- **iOS alpha**: iOS AppIcons must have no transparency. The generate script composites onto white background automatically.
- **ICNS naming**: `icp6` is 64x64 (not 48x48 as in some Apple docs); the `tauri-icns` crate uses 64x64.
- **Source not RGBA**: If source is RGB, the generate script auto-converts to RGBA but warns. Ensure the source has an alpha channel for proper transparency.
- **HDMI launcher size**: 72px (standard Android 1.5x), not 49px as occasionally misreported.
