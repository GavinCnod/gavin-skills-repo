# Gavin 的 Agent 技能库 (Gavin's Agent Skills Repository)

[🇺🇸 English Readme](README.md)

欢迎来到我的个人 Agent Skills 收藏库。这个仓库不仅用于存储工作生活中积累的Skill源码，记录了我为 AI Agent 构建的各种工具、工作流和专业知识库。本项目参照了 Anthropic 官方的 Agent Skills 标准结构，设计上追求模块化、可扩展性和易用性。

## 📖 简介 (Introduction)

这里的每一个文件夹（位于 `skills/` 目录下）都代表一种独立的“技能”——无论是数据处理、API 集成，还是复杂的工作流自动化。这些技能被设计为可以被 AI Agent（如 Claude / Trae 或其他支持 Skill 的 Agent 工具）动态加载和使用，从而扩展 Agent 的能力边界。

## 📂 仓库结构 (Structure)

仓库结构清晰明了，方便浏览和维护：

```text
gavin-skills-repo/
├── README.md           # 项目主页 (英文)
├── README_zh.md        # 项目主页 (中文)
├── skills/             # 核心目录，存放所有技能
│   ├── _template/      # 标准模板，用于快速创建新技能
│   ├── 5d-strategic-thinking/   # 5D 战略思维 — 基于五维框架（Threads, Levels, Altitude, Perspectives, Time）的深度战略分析工具
│   ├── b2b-product-blog-writing/# B2B 工业产品博客写作 — SEO 优化的英文产品介绍，包含交互式 Q&A 工作流
│   ├── blinkist-daily/          # Blinkist 每日书摘采集器 — 自动抓取每日免费书籍摘要
│   └── tauri-v2-icons/          # Tauri V2 图标工具包 — 验证并生成全平台应用图标（Windows/macOS/Linux/Android/iOS）
└── LICENSE             # MIT 开源许可证
```

## 🛠️ 技能列表 (Skill Showcase)

| 技能名称 (Skill Name) | 描述 (Description) | 路径 (Path) |
|-------------------|-------------------|------------|
| **5D 战略思维 (5D Strategic Thinking)** | 基于五维思维框架（Threads, Levels, Altitude, Perspectives, Time）的高阶战略分析工具，为复杂问题和决策提供深度、全面和进化的视角。 | [`skills/5d-strategic-thinking`](skills/5d-strategic-thinking/SKILL.md) |
| **Blinkist 每日书摘 (Blinkist Daily)** | 自动采集 Blinkist 每日免费书籍摘要，并提取核心观点生成 Markdown 笔记。 | [`skills/blinkist-daily`](skills/blinkist-daily/SKILL.md) |
| **B2B 工业产品博客写作 (B2B Product Blog Writing)** | 根据提供的源文件（PDF、文档等）为 B2B 工业产品撰写 SEO 优化的英文短介绍（约 200 字）。包含交互式 Q&A 工作流确认产品细节。 | [`skills/b2b-product-blog-writing`](skills/b2b-product-blog-writing/SKILL.md) |
| **Tauri V2 图标工具包 (Tauri V2 Icon Toolkit)** | 验证图标文件是否符合 Tauri V2 平台规范，并从源 PNG 生成全平台所需图标（Windows .ico、macOS .icns、Linux .png、Android、iOS）。 | [`skills/tauri-v2-icons`](skills/tauri-v2-icons/SKILL.md) |

## 🚀 使用指南 (How to Use)

### 通过 npx skills 快速安装

```bash
# 列出仓库中所有可用技能
npx skills add GavinCnod/gavin-skills-repo --list

# 安装指定技能（支持 Claude Code、Cursor、Codex、Windsurf 等）
npx skills add GavinCnod/gavin-skills-repo --skill blinkist-daily

# 一键安装所有技能（非交互模式）
npx skills add GavinCnod/gavin-skills-repo --skill '*' -y
```

安装后即可使用——在 Agent 中输入 `/skill-name` 调用，或直接描述你的任务，Agent 会自动触发对应技能。

### 手动安装

每个技能都是自包含的。要手动使用某个技能：

1.  将目标技能文件夹从 `skills/` 复制或软链接到 `~/.claude/skills/`（Claude Code 仅扫描此目录）。
2.  技能会被自动发现——Agent 通过 `SKILL.md` 的 frontmatter 中的 `name` 和 `description` 决定何时触发。
3.  部分技能包含可独立运行的脚本，例如：
    ```bash
    python skills/blinkist-daily/scripts/collect_blinkist.py
    ```

### 验证与打包技能

分发技能前，使用 skill-creator 工具进行验证和打包：

```bash
# 验证技能结构和 frontmatter
python ~/.claude/skills/skill-creator/scripts/package_skill.py skills/<skill-name>
```

此命令会生成一个 `.skill` 文件（zip 压缩包），可直接分发。

### 创建新技能

如果你想向此仓库添加新技能：

1.  复制 `skills/_template` 文件夹，并将其重命名为你的技能名称（例如 `skills/my-awesome-skill`）。
2.  编辑 `SKILL.md`——frontmatter 中的 `description` 字段至关重要：必须同时描述技能功能与触发条件（包含具体触发短语）。
3.  在文件夹中添加必要的 `scripts/`、`references/` 或 `assets/` 资源。
4.  删除模板中不需要的示例目录。

## 👤 关于作者 (About the Author)

**Gavin Chen**

我热衷于探索 AI Agent 技术，致力于构建未来的自动化工作流。这个仓库是我定义和打磨 Agent 能力之旅的一部分。

- **GitHub**: [GavinCnod](https://github.com/GavinCnod)
- **博客/网站**: [Gavin的公司主页](https://www.mindrose.xyz/)
- **联系方式**: [contact@mindrose.xyz](mailto:contact@mindrose.xyz)

---
*本项目基于 [MIT License](LICENSE) 开源。*
