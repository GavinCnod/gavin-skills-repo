---
name: blinkist-daily
description: Automatically collect Blinkist daily free book summaries. Use when the user wants to fetch the daily free Blinkist book, extract book summaries, or automate Blinkist content collection. Trigger on phrases like "Blinkist daily", "采集 Blinkist", "每日书摘", "blinkist 免费书".
---

# Blinkist Daily Collector

Automatically fetch and save Blinkist's daily free book summary.

## Overview

Blinkist offers one free book summary every 24 hours. This skill automates the collection process using jina.ai's text extraction service to bypass Cloudflare protection.

## How It Works

1. Fetches the daily free book page via jina.ai
2. Extracts book title, author, and URL slug
3. Retrieves the full book summary content
4. Saves as a formatted Markdown file

## Usage

### Manual Collection

Run the collection script:

```bash
python /root/.openclaw/workspace/skills/blinkist-daily/scripts/collect_blinkist.py
```

The script will:
- Create a timestamped Markdown file in the workspace
- Output the file path upon completion
- Include book metadata (title, author, rating, reading time)

### Automated Schedule

Set up a cron job to run daily at 10:00 AM:

```bash
# Example cron setup
0 10 * * * python /root/.openclaw/workspace/skills/blinkist-daily/scripts/collect_blinkist.py
```

## Technical Details

### Data Sources

- **Daily Page**: `https://r.jina.ai/http://www.blinkist.com/en/app/daily`
- **Book Content**: `https://r.jina.ai/http://www.blinkist.com/en/reader/books/{book-slug}-en`

### Output Format

Files are saved as: `blinkist-daily-YYYY-MM-DD.md`

Each file includes:
- Book title and author
- Rating and reading time
- Category tags
- Chapter summaries
- Key takeaways

## Dependencies

- Python 3.x
- requests library
- markdown library (optional, for formatting)

## References

See `references/parsing-rules.md` for detailed parsing logic.
