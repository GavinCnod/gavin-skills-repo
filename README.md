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
│   ├── 5d-strategic-thinking/   # 5D Strategic Thinking skill, a high-level strategic analysis tool, inspired by Dan Koe's article from X
│   ├── b2b-product-blog-writing/# B2B Product Blog Writer, generates SEO-friendly intros for industrial products
│   └── blinkist-daily/          # Blinkist Daily Collector, automatically fetches daily free book summaries
└── LICENSE             # MIT Open Source License
```

## 🛠️ Skill Showcase

| Skill Name | Description | Path |
|---|---|---|
| **5D Strategic Thinking** | A high-level strategic analysis tool based on the 5-dimensional thinking framework, providing deep, comprehensive, and evolutionary perspectives. | [`skills/5d-strategic-thinking`](skills/5d-strategic-thinking/SKILL.md) |
| **Blinkist Daily Collector** | Automatically fetch and save Blinkist's daily free book summary, extracting key insights and metadata into clean Markdown. | [`skills/blinkist-daily`](skills/blinkist-daily/SKILL.md) |
| **B2B Product Blog Writer** | Generates SEO-friendly short introductions or blog content for B2B industrial products based on source materials. | [`skills/b2b-product-blog-writing`](skills/b2b-product-blog-writing/SKILL.md) |
| *Coming Soon* | *More professional skills are under development...* | ... |

## 🚀 How to Use

Each skill is self-contained. To use a skill:

1.  Enter the corresponding skill folder under the `skills/` directory.
2.  Read the `SKILL.md` file to understand the skill's purpose, input requirements, and usage examples.
3.  Load the skill into your Agent context or configuration system.

### Creating New Skills

If you want to add a new skill to this repository:

1.  Copy the `skills/_template` folder and rename it to your skill name (e.g., `skills/my-awesome-skill`).
2.  Edit `SKILL.md` to define metadata (`name`, `description`) and write detailed instruction explanations.
3.  Add any necessary scripts or resource files to the folder.

## 👤 About the Author

**Gavin Chen**

I am passionate about exploring AI Agent technology and dedicated to building future automated workflows. This repository is part of my journey to define and polish Agent capabilities.

- **GitHub**: [GavinCnod](https://github.com/GavinCnod)
- **Blog/Website**: [Gavin's Company Home](https://www.mindrose.xyz/)
- **Contact**: [contact@mindrose.xyz](mailto:contact@mindrose.xyz)

---
*This project is open source under the [MIT License](LICENSE).*
