# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal Agent Skills repository following Anthropic's Agent Skills standard. Each folder under `skills/` is a self-contained "skill" — a module that AI Agents (Claude, Trae, etc.) dynamically load to extend their capabilities. Skills can include scripts, reference docs, and structured instructions.

## Repository Structure

```
skills/
├── _template/                  # Standard template for new skills
├── <skill-name>/               # Each skill is a self-contained folder
│   ├── SKILL.md                # Required: YAML frontmatter + instructions
│   ├── references/             # Optional: supplementary docs
│   └── scripts/                # Optional: executable code (Python, etc.)
```

## Creating a New Skill

1. Copy `skills/_template/` and rename to `skills/<my-skill>/`.
2. Edit `SKILL.md` with required YAML frontmatter fields: `name` (slug), `description` (1-2 sentences on what it does and when to trigger).
3. Add instructions, workflows, and examples in the body.
4. Optional: add scripts to `scripts/`, reference docs to `references/`.
5. Update `README.md` and `README_zh.md` — add the skill to the showcase table and the structure diagram. Both files must be kept in sync (English + Chinese).

## SKILL.md Format

Every skill's `SKILL.md` starts with YAML frontmatter between `---` delimiters. Two fields are required by all Agents:

```yaml
---
name: skill-slug-name        # Required: unique identifier (lowercase-hyphenated)
description: ...             # Required: what it does + when to trigger + trigger phrases
---
```

For `npx skills add` (Vercel Agent Skills spec) compatibility, include these optional fields:

```yaml
---
name: skill-slug-name
description: >
  Long descriptions must use YAML folded block scalar (>) to avoid
  colon-parsing bugs. The yaml library interprets ":" followed by space
  as a nested mapping inside plain scalars.
license: MIT                 # Optional: license name
metadata:                    # Optional: string key-value pairs only
  version: "1.0.0"
  author: GavinCnod
  category: ...
---
```

The two specs are compatible — Claude Code only reads `name` and `description`, and ignores unknown fields. **Critical:** always use `description: >` (folded block scalar) for descriptions containing `: ` (colon + space), otherwise the `yaml` parser used by `npx skills` throws `Nested mappings are not allowed in compact mappings` and silently skips the skill.

## Skill Deployment

Claude Code only discovers skills under `~/.claude/skills/`. Skills in this repo must be copied or symlinked there to be used.

```bash
# For development: symlink from this repo into Claude Code's skills dir
ln -s "$(pwd)/skills/5d-strategic-thinking" ~/.claude/skills/5d-strategic-thinking
```

Validate and package a skill for distribution:

```bash
npx skills add . --list          # List discoverable skills
python ~/.claude/skills/skill-creator/scripts/package_skill.py skills/<skill-name>
```

**WARNING:** `npx skills remove <name>` may delete source files when the skill was installed from a local path (e.g., `npx skills add .`). Always commit before running remove, or only use remove on globally-installed skills.

## Important Constraints

- `name` and `description` are the only fields Claude Code uses for skill triggering. `license` and `metadata` are optional fields recognized by `npx skills add` (Vercel Agent Skills spec) and ignored by Claude Code — safe to include for cross-platform compatibility.
- Do NOT create README.md, CHANGELOG.md, or other auxiliary docs inside skill folders.
- Keep SKILL.md under 500 lines. Move detailed content to `references/`.
- Avoid duplicating information between SKILL.md and reference files.
- The `description` field is the sole mechanism for skill triggering — it must include both what the skill does and specific trigger phrases/keywords.
- `metadata` values must be strings when present (e.g., `version: "1.0.0"` not `version: 1.0.0`).

## Existing Skills

| Skill | Purpose |
|---|---|
| `5d-strategic-thinking` | Interactive strategic analysis using a 5D framework (Threads, Levels, Altitude, Perspectives, Time) |
| `blinkist-daily` | Python script that fetches Blinkist's daily free book summary via jina.ai, saves as timestamped Markdown |
| `b2b-product-blog-writing` | Interactive Q&A workflow to write ~200-word SEO-optimized English B2B product intros from source materials |

## No Build/Test Infrastructure

This repo has no build system, linter, or test runner. Skills are validated by loading them into an Agent and verifying behavior. The `blinkist-daily` Python script can be run directly: `python skills/blinkist-daily/scripts/collect_blinkist.py`.
