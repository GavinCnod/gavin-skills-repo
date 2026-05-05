# Tauri V2 Icon Specifications

Reference: https://v2.tauri.app/develop/icons/

## Source Image Requirements

| Property | Requirement |
|----------|------------|
| Format | PNG (SVG not directly supported; rasterize to PNG first) |
| Shape | Square (width == height) |
| Color | RGBA (32-bit, 8 bits/channel) |
| Recommended size | 1024 x 1024 px |
| Minimum size | 512 x 512 px |

## ICO (Windows)

**Layers required:** 16, 24, 32, 48, 64, 256 px (6 layers)

**Critical: 32px must be the first layer.** Tauri runtime only reads `entries()[0]` from the ICO for the window icon. If a different size (e.g., 256px) is first, the window icon will appear blurry when downscaled. Desktop shortcuts and Explorer use all embedded layers correctly.

See: https://github.com/tauri-apps/tauri/issues/14596

**Binary format (for verification):**
- Header: `reserved`(2B,=0) + `type`(2B,=1) + `count`(2B)
- Directory entries: width(1B) height(1B) color_count(1B) reserved(1B) planes(2B) bit_count(2B) img_size(4B) img_offset(4B)
- width/height = 0 means 256 in ICO spec
- bit_count = 32 means PNG-compressed data

## ICNS (macOS)

OSTypes and their actual pixel dimensions (PNG data embedded per entry):

| OSType | Logical | Actual px |
|--------|---------|-----------|
| `icp4` | 16x16 | 16 |
| `icp5` | 32x32 | 32 |
| `icp6` | 64x64 | 64 |
| `ic07` | 128x128 | 128 |
| `ic08` | 256x256 | 256 |
| `ic09` | 512x512 | 512 |
| `ic10` | 512x512@2x | 1024 |
| `ic11` | 16x16@2x | 32 |
| `ic12` | 32x32@2x | 64 |
| `ic13` | 128x128@2x | 256 |
| `ic14` | 256x256@2x | 512 |

Total: 11 types. TOC entry (`TOC `) is optional but recommended.

Binary: `icns`(4B magic) + total_len(4B BE) + entries...
Each entry: OSType(4B ASCII) + entry_len(4B BE, includes 8B header) + PNG_data

## Desktop PNGs (Linux)

| Filename | Size |
|----------|------|
| `32x32.png` | 32x32 |
| `128x128.png` | 128x128 |
| `128x128@2x.png` | 256x256 |
| `icon.png` | 512x512 |

## Android

Density buckets (standard Android scaling):

| Density | Launcher | Foreground |
|---------|----------|------------|
| mdpi (1x) | 48x48 | 108x108 |
| hdpi (1.5x) | 72x72 | 162x162 |
| xhdpi (2x) | 96x96 | 216x216 |
| xxhdpi (3x) | 144x144 | 324x324 |
| xxxhdpi (4x) | 192x192 | 432x432 |

Files: `ic_launcher.png`, `ic_launcher_round.png`, `ic_launcher_foreground.png`

## iOS AppIcon

**No alpha channel** — composite onto white (#FFFFFF) background.
Naming: `AppIcon-{W}x{H}@{scale}x{-1 for extra}.png`

| Logical | Scale | Actual px | Extra? |
|---------|-------|-----------|--------|
| 20 | @1x | 20 | no |
| 20 | @2x | 40 | no |
| 20 | @3x | 60 | no |
| 20 | @2x | 40 | yes |
| 29 | @1x | 29 | no |
| 29 | @2x | 58 | no |
| 29 | @3x | 87 | no |
| 29 | @2x | 58 | yes |
| 40 | @1x | 40 | no |
| 40 | @2x | 80 | no |
| 40 | @3x | 120 | no |
| 40 | @2x | 80 | yes |
| 60 | @2x | 120 | no |
| 60 | @3x | 180 | no |
| 76 | @1x | 76 | no |
| 76 | @2x | 152 | no |
| 83.5 | @2x | 167 | no |
| 512 | @2x | 1024 | no |

Special: `AppIcon-512@2x.png` drops the `x512` part (Apple naming quirk).

## SVG Source Notes

SVG is not a direct source for the scripts; rasterize to 1024x1024 RGBA PNG first.
Use `cairosvg` or `svglib` for conversion, or render via a headless browser for complex SVGs.
