# Gavin's Agent Skills Repository

[🇨🇳 中文说明](README_zh.md)

Welcome to my personal collection of Agent Skills. This repository serves as a portfolio of my capabilities in building tools, workflows, and specialized knowledge bases for AI agents. It is designed to be modular, scalable, and easy to integrate, following the standard Agent Skills structure inspired by Anthropic.

## 📖 Introduction

This repository is more than just a code storage; it is a showcase of "Agentic Capabilities." Each folder in the `skills/` directory represents a distinct capability—whether it's data processing, API integration, or complex workflow automation—that can be dynamically loaded by an AI agent (like Claude).

## 📂 Repository Structure

The repository is organized to ensure clarity and ease of use:

```text
gavin-skills-repo/
├── README.md           # Project Home (English)
├── README_zh.md        # Project Home (Chinese)
├── skills/             # The core directory containing all skills
│   ├── _template/      # Standard template for creating new skills
│   ├── example-skill/  # A demonstration skill
│   └── [Your Skill]/   # Your custom skills go here
└── LICENSE             # MIT License
```

## 🛠️ Available Skills

| Skill Name | Description | Path |
|------------|-------------|------|
| **Hello World** | A simple demonstration skill to verify the setup. | [`skills/example-skill`](skills/example-skill/SKILL.md) |
| *Coming Soon* | *More specialized skills are under development.* | ... |

## 🚀 How to Use

Each skill is self-contained. To use a skill:

1.  Navigate to the specific skill folder in `skills/`.
2.  Read the `SKILL.md` file to understand the skill's purpose, inputs, and usage examples.
3.  Load the skill into your agent's context or configuration system.

### Creating a New Skill

To add a new skill to this repository:

1.  Copy the `skills/_template` folder and rename it to your skill name (e.g., `skills/my-awesome-skill`).
2.  Edit `SKILL.md` to define the metadata (`name`, `description`) and provide detailed instructions.
3.  Add any necessary scripts or resources within the folder.

## 👤 About the Author

**Gavin**

I am passionate about AI Agents and building the future of automated workflows. This repository is part of my journey to define and refine what agents can do.

- **GitHub**: [Your GitHub Profile Link]
- **Blog/Website**: [Your Website Link]
- **Contact**: [Your Email or Social Media]

---
*Licensed under the [MIT License](LICENSE).*
