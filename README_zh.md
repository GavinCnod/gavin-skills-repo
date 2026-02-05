# Gavin 的 Agent 技能库 (Gavin's Agent Skills Repository)

[🇺🇸 English Readme](README.md)

欢迎来到我的个人 Agent Skills 收藏库。这个仓库不仅用于存储代码，更是我个人能力的展示窗口，记录了我为 AI Agent 构建的各种工具、工作流和专业知识库。本项目参照了 Anthropic 官方的 Agent Skills 标准结构，设计上追求模块化、可扩展性和易用性。

## 📖 简介 (Introduction)

这里的每一个文件夹（位于 `skills/` 目录下）都代表一种独立的“技能”——无论是数据处理、API 集成，还是复杂的工作流自动化。这些技能被设计为可以被 AI Agent（如 Claude）动态加载和使用，从而扩展 Agent 的能力边界。

## 📂 仓库结构 (Structure)

仓库结构清晰明了，方便浏览和维护：

```text
gavin-skills-repo/
├── README.md           # 项目主页 (英文)
├── README_zh.md        # 项目主页 (中文)
├── skills/             # 核心目录，存放所有技能
│   ├── _template/      # 标准模板，用于快速创建新技能
│   ├── example-skill/  # 示例技能，用于演示结构
│   └── [Your Skill]/   # 你开发的自定义技能
└── LICENSE             # MIT 开源许可证
```

## 🛠️ 技能列表 (Skill Showcase)

| 技能名称 (Skill Name) | 描述 (Description) | 路径 (Path) |
|-------------------|-------------------|------------|
| **Hello World** | 一个简单的演示技能，用于验证配置和理解结构。 | [`skills/example-skill`](skills/example-skill/SKILL.md) |
| **5D 战略思维 (5D Strategic Thinking)** | 基于五维思维框架的高阶战略分析工具，提供深度、全面和进化的视角。 | [`skills/5d-strategic-thinking`](skills/5d-strategic-thinking/SKILL.md) |
| *Coming Soon* | *更多专业技能正在开发中...* | ... |

## 🚀 使用指南 (How to Use)

每个技能都是自包含的。要使用某个技能：

1.  进入 `skills/` 目录下对应的技能文件夹。
2.  阅读 `SKILL.md` 文件，了解该技能的用途、输入要求和使用示例。
3.  将该技能加载到你的 Agent 上下文或配置系统中。

### 创建新技能

如果你想向此仓库添加新技能：

1.  复制 `skills/_template` 文件夹，并将其重命名为你的技能名称（例如 `skills/my-awesome-skill`）。
2.  编辑 `SKILL.md`，定义元数据（`name`, `description`）并编写详细的指令说明。
3.  在文件夹中添加任何必要的脚本或资源文件。

## 👤 关于作者 (About the Author)

**Gavin**

我热衷于探索 AI Agent 技术，致力于构建未来的自动化工作流。这个仓库是我定义和打磨 Agent 能力之旅的一部分。

- **GitHub**: [你的 GitHub 个人主页链接]
- **博客/网站**: [你的个人网站链接]
- **联系方式**: [你的邮箱或社交媒体]

---
*本项目基于 [MIT License](LICENSE) 开源。*
