---
name: _template
description: >
  Template for creating new agent skills. Each new skill must copy this folder
  and customize SKILL.md frontmatter — the `description` field is critical
  and must include both what the skill does and specific trigger phrases.
  Use YAML folded block scalar (>) for long descriptions to avoid colon-parsing
  issues with the `yaml` library used by npx skills.
license: MIT
metadata:
  internal: true
  category: template
---

# Skill Name

[Instructions for the Agent in imperative form. Write as "You are..." or direct commands.]

## Instructions

1. Step-by-step workflow...
2. ...

## Examples

- **Example 1**: Input → Expected output
- **Example 2**: Usage scenario

## Optional Resources

- `scripts/` — Executable code (Python/Bash) for deterministic, repeatable tasks. Delete if not needed.
- `references/` — Docs the Agent loads on demand (schemas, policies, detailed guides). Keep SKILL.md lean; put detailed reference material here. Delete if not needed.
- `assets/` — Files used in output (templates, images, fonts). Not loaded into context. Delete if not needed.

## Guidelines

- Do NOT create README.md, CHANGELOG.md, or other auxiliary docs in the skill folder.
- Keep SKILL.md under 500 lines. Split detailed content into `references/`.
- Avoid duplicating information between SKILL.md and reference files.

