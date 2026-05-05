# Gavin's Agent Skills Repository

[🇨🇳 中文说明](README_zh.md)

Welcome to my personal Agent Skills collection. This repository not only stores skill source code accumulated in work and life, but also records various tools, workflows, and specialized knowledge bases I have built for AI Agents. This project follows Anthropic's official Agent Skills standard structure, designed for modularity, scalability, and ease of use.

## 📖 Introduction

Each folder here (located in the `skills/` directory) represents an independent "skill"—whether it's data processing, API integration, or complex workflow automation. These skills are designed to be dynamically loaded and used by AI Agents (such as Claude / Trae or other Agent tools supporting Skills), thereby extending the Agent's capability boundaries.

## 📂 Structure

The repository structure is clear and easy to browse and maintain:

```text
gavin-skills-repo/
├── README.md           # Project Home (English)
├── README_zh.md        # Project Home (Chinese)
├── skills/             # Core directory containing all skills
│   ├── _template/      # Standard template for creating new skills
│   ├── 5d-strategic-thinking/   # 5D Strategic Thinking — deep strategic analysis via 5D framework (Threads, Levels, Altitude, Perspectives, Time)
│   ├── b2b-product-blog-writing/# B2B Product Blog Writer — SEO-optimized English intros for industrial products, with interactive Q&A
│   ├── blinkist-daily/          # Blinkist Daily Collector — auto-fetches daily free book summaries
│   └── tauri-v2-icons/          # Tauri V2 Icon Toolkit — validate & generate platform icons (Windows/macOS/Linux/Android/iOS)
└── LICENSE             # MIT Open Source License
```

## 🛠️ Skill Showcase

| Skill Name | Description | Path |
|---|---|---|
| **5D Strategic Thinking** | A high-level strategic analysis tool based on the 5-Dimensional Thinking framework — Threads, Levels, Altitude, Perspectives (4 Quadrants), and Time. Provides deep, holistic, and evolutionary perspectives for complex problems and decisions. | [`skills/5d-strategic-thinking`](skills/5d-strategic-thinking/SKILL.md) |
| **Blinkist Daily Collector** | Automatically fetch and save Blinkist's daily free book summary, extracting key insights and metadata into clean Markdown. | [`skills/blinkist-daily`](skills/blinkist-daily/SKILL.md) |
| **B2B Product Blog Writer** | Write SEO-optimized English short introductions (~200 words) for B2B industrial products based on source materials (PDFs, docs). Features an interactive Q&A workflow to confirm product details. | [`skills/b2b-product-blog-writing`](skills/b2b-product-blog-writing/SKILL.md) |
| **Tauri V2 Icon Toolkit** | Validate icon files against Tauri V2 platform specs, and generate all required platform icons (Windows .ico, macOS .icns, Linux .png, Android, iOS) from a source PNG. | [`skills/tauri-v2-icons`](skills/tauri-v2-icons/SKILL.md) |

## 🚀 How to Use

### Quick Install via npx skills

```bash
# List all available skills in this repo
npx skills add GavinCnod/gavin-skills-repo --list

# Install a specific skill (supports Claude Code, Cursor, Codex, Windsurf, etc.)
npx skills add GavinCnod/gavin-skills-repo --skill blinkist-daily

# Install all skills at once (non-interactive)
npx skills add GavinCnod/gavin-skills-repo --skill '*' -y
```

Once installed, the skill is ready — invoke it in your Agent with `/skill-name` or simply describe your task and the Agent will auto-trigger.

### Manual Setup

Each skill is self-contained. To use a skill manually:

1.  Copy or symlink the desired skill folder from `skills/` into `~/.claude/skills/` (Claude Code only scans this directory).
2.  The skill will be auto-discovered — the Agent reads the `name` and `description` from `SKILL.md` frontmatter to decide when to trigger it.
3.  Some skills include standalone scripts that can be run directly, e.g.:
    ```bash
    python skills/blinkist-daily/scripts/collect_blinkist.py
    ```

### Validating and Packaging Skills

Before distributing a skill, validate and package it using the skill-creator tool:

```bash
# Validate skill structure and frontmatter
python ~/.claude/skills/skill-creator/scripts/package_skill.py skills/<skill-name>
```

This produces a `.skill` file (a zip archive) ready for distribution.

### Creating New Skills

If you want to add a new skill to this repository:

1.  Copy the `skills/_template` folder and rename it to your skill name (e.g., `skills/my-awesome-skill`).
2.  Edit `SKILL.md` — the frontmatter `description` field is critical: it must describe both what the skill does AND when to trigger (include specific trigger phrases).
3.  Add any necessary `scripts/`, `references/`, or `assets/` to the folder.
4.  Delete any unused example directories from the template.

## 👤 About the Author

**Gavin Chen**

I am passionate about exploring AI Agent technology and dedicated to building future automated workflows. This repository is part of my journey to define and polish Agent capabilities.

- **GitHub**: [GavinCnod](https://github.com/GavinCnod)
- **Blog/Website**: [Gavin's Company Home](https://www.mindrose.xyz/)
- **Contact**: [contact@mindrose.xyz](mailto:contact@mindrose.xyz)

---
*This project is open source under the [MIT License](LICENSE).*
