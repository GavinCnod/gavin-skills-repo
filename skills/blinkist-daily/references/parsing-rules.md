# Parsing Rules

This document describes the parsing rules used to extract information from Blinkist pages.

## Daily Page Parsing

### Book Title

The script attempts to extract the book title using the following patterns in order:

1. **Heading after Image**: `Today[\'\u2019]s Free Blink.*?\n={3,}\n\n.*?\n\n(.+?)\n-+`
2. **HTML Tag**: `book-title.*?>([^<]+)`
3. **JSON Structure**: `\"title\"\s*:\s*\"([^\"]+)\"`

If regex fails, it attempts a heuristic search:
- Locates lines containing image URLs (e.g., `470.jpg`, `blinkist.io/images/books`).
- Checks subsequent lines (within a 5-line window) for text followed by a line starting with `by `.

### Author

Extracted using the regex: `by\s+(.+?)(?:\n|$)`

### Rating

Extracted using the regex: `(\d\.\d)\s*\(\d+\s*ratings?\)`

### Duration

Extracted using the regex: `(\d+)\s*mins?`

### Key Ideas Count

Extracted using the regex: `(\d+)\s*key\s*ideas?`

### Slug Extraction

The slug is critical for constructing the full book URL. The script attempts to find it using:

1. **Full URL**: `blinkist\.com/en/reader/books/([\w-]+)`
2. **Path Pattern**: `books/([\w-]+?)(?:-en)?(?:\?|$|\s)`
3. **Alternative Link**: `blinkist\.com/en/reader/books/([\w-]+)`

If direct extraction fails, it scans the content more aggressively for `/books/([\w-]+)`.

## Content Cleaning

The raw content fetched via `jina.ai` contains metadata and security notices. The following cleaning rules are applied:

### Removed Lines

Lines containing any of the following strings are discarded:
- `SECURITY NOTICE`
- `EXTERNAL_UNTRUSTED`
- `Source:`
- `<<<EXTERNAL`
- `URL Source:`

### Content Extraction

- The script looks for the line starting with `Markdown Content:` to begin capturing the main text.
- Stops capturing at `<<<END_EXTERNAL_UNTRUSTED_CONTENT>>>`.
- If `Markdown Content:` is not found, it falls back to capturing all lines except those matching the removal criteria.
