#!/usr/bin/env python3
"""
Blinkist Daily Book Summary Collector

Automatically fetches the daily free book summary from Blinkist
and saves it as a Markdown file.
"""

import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
import requests


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch content from URL using requests."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


def parse_daily_page(content: str) -> dict:
    """Parse the daily page to extract book information."""
    info = {
        'title': '',
        'author': '',
        'slug': '',
        'rating': '',
        'duration': '',
        'key_ideas': ''
    }
    
    # Try the new Jina markdown format first
    jina_match = re.search(r'!\[.*?\]\(.*?blinkist\.io/images/books.*?\)\n+(?:#+\s*)?([^\n]+)\n+by\s+([^\n]+)', content)
    if jina_match:
        info['title'] = jina_match.group(1).strip()
        info['author'] = jina_match.group(2).strip()
    
    # Extract title - usually in format "Title\n--------" or just prominent heading
    title_patterns = [
        r'Today[\'\u2019]s Free Blink.*?\n={3,}\n\n.*?\n\n(.+?)\n-+',  # Title after image
        r'book-title.*?>([^<]+)',
        r'\"title\"\s*:\s*\"([^\"]+)\"',
    ]
    
    if not info['title']:
        for pattern in title_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                info['title'] = match.group(1).strip()
                break
    
    # Clean up title if it matches too much content
    if info['title']:
        # If title contains image markdown, try to extract from alt text or text after it
        if '![' in info['title']:
            # Try to extract from alt text first
            alt_match = re.search(r'!\[.*?: (.*?)\]', info['title'])
            if alt_match:
                info['title'] = alt_match.group(1)
            else:
                # If no alt text match, take the last non-empty line which is usually the title
                lines = [line.strip() for line in info['title'].split('\n') if line.strip()]
                if lines:
                    info['title'] = lines[-1]
        
        # Remove any remaining newlines and extra spaces
        info['title'] = re.sub(r'\s+', ' ', info['title']).strip()

    # Try simpler approach - look for book title pattern
    if not info['title']:
        # Look for pattern: image followed by title then dashes
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '470.jpg' in line or 'blinkist.io/images/books' in line:
                # Title is usually 2-3 lines after image
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip() and 'by ' in lines[j+1] if j+1 < len(lines) else False:
                        info['title'] = lines[j].strip()
                        info['author'] = lines[j+1].replace('by ', '').strip()
                        break
                    elif lines[j].strip() and not lines[j].startswith('!'):
                        # Check if next line has author
                        if j+1 < len(lines) and lines[j+1].strip().startswith('by '):
                            info['title'] = lines[j].strip()
                            info['author'] = lines[j+1].replace('by ', '').strip()
                            break
            if info['title']:
                break
    
    # Extract author
    if not info['author']:
        author_match = re.search(r'by\s+(.+?)(?:\n|$)', content)
        if author_match:
            info['author'] = author_match.group(1).strip()
    
    # Extract rating
    rating_match = re.search(r'(\d\.\d)\s*\(\d+\s*ratings?\)', content)
    if rating_match:
        info['rating'] = rating_match.group(1)
    
    # Extract duration
    duration_match = re.search(r'(\d+)\s*mins?', content)
    if duration_match:
        info['duration'] = duration_match.group(1) + ' mins'
    
    # Extract key ideas count
    key_ideas_match = re.search(r'(\d+)\s*key\s*ideas?', content)
    if key_ideas_match:
        info['key_ideas'] = key_ideas_match.group(1)
    
    # Extract slug from URL pattern (look for the book link in the content)
    # First try to find the full book URL in the daily page
    book_link_match = re.search(r'blinkist\.com/en/reader/books/([\w-]+)', content)
    if book_link_match:
        info['slug'] = book_link_match.group(1)
    else:
        # Fallback: extract from other patterns
        slug_match = re.search(r'books/([\w-]+?)(?:-en)?(?:\?|$|\s)', content)
        if slug_match:
            info['slug'] = slug_match.group(1)
    
    # Alternative: extract from link
    if not info['slug']:
        link_match = re.search(r'blinkist\.com/en/reader/books/([\w-]+)', content)
        if link_match:
            info['slug'] = link_match.group(1)
    
    return info


def parse_book_content(content: str) -> str:
    """Parse the full book content and format as markdown."""
    # Find the actual markdown content section
    lines = content.split('\n')
    formatted_lines = []
    in_content = False
    
    for line in lines:
        # Skip security notices and metadata
        if any(skip in line for skip in ['SECURITY NOTICE', 'EXTERNAL_UNTRUSTED', 'Source:', '<<<EXTERNAL']):
            continue
        if line.startswith('Title:') and 'URL Source:' in content:
            # Extract author from title line if present
            if ' by ' in line:
                continue
        if line.startswith('URL Source:'):
            continue
        if line.startswith('Markdown Content:'):
            in_content = True
            continue
        if line.strip() == '<<<END_EXTERNAL_UNTRUSTED_CONTENT>>>':
            break
        if in_content:
            formatted_lines.append(line)
    
    result = '\n'.join(formatted_lines).strip()
    
    # If no content extracted, return cleaned original
    if not result:
        for line in lines:
            if any(skip in line for skip in ['SECURITY NOTICE', 'EXTERNAL_UNTRUSTED', 'Source:', '<<<']):
                continue
            if line.startswith('Title:') or line.startswith('URL Source:'):
                continue
            formatted_lines.append(line)
        result = '\n'.join(formatted_lines).strip()
    
    return result


def save_markdown(info: dict, content: str, output_dir: Path = None) -> Path:
    """Save the book summary as a Markdown file."""
    if output_dir is None:
        # Use current working directory by default for cross-platform compatibility
        output_dir = Path.cwd()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"blinkist-daily-{date_str}.md"
    filepath = output_dir / filename
    
    # Build markdown content
    md_content = f"""# Blinkist 每日书摘 - {date_str}

> **Created Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **Source**: [Blinkist Daily Free](https://www.blinkist.com/en/app/daily)

---

## 📚 Free Blinkist Daily

# {info['title'] or 'Unknown Title'}
**Author**: {info['author'] or 'Unknown Author'}

**Rating**: ⭐ {info['rating'] or 'N/A'}/5  
**Reading Time**: {info['duration'] or 'Unknown'}  
**Key Ideas**: {info['key_ideas'] or 'N/A'} Key Ideas

---

{content}

---

*Provided by Blinkist*
"""
    
    filepath.write_text(md_content, encoding='utf-8')
    return filepath


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Blinkist Daily Book Summary Collector')
    parser.add_argument('--output', '-o', type=Path, default=None, help='Output directory for the markdown file')
    args = parser.parse_args()

    print("Fetching Blinkist daily free book...")
    
    # Fetch daily page
    daily_url = 'https://r.jina.ai/http://www.blinkist.com/en/app/daily'
    daily_content = fetch_url(daily_url)
    
    if not daily_content:
        print("ERROR: Failed to fetch daily page")
        sys.exit(1)
    
    print("OK Daily page fetched")
    
    # Parse book info
    info = parse_daily_page(daily_content)
    print(f"Book found: {info['title'] or 'N/A'} by {info['author'] or 'N/A'}")
    
    if not info['slug']:
        print("WARNING: Could not extract book slug, trying alternative method...")
        # Try to find slug in the content more aggressively
        possible_slugs = re.findall(r'/books/([\w-]+)', daily_content)
        if possible_slugs:
            info['slug'] = possible_slugs[0]
            print(f"OK Found slug: {info['slug']}")
    
    if not info['slug']:
        print("ERROR: Could not determine book slug")
        # Save what we have anyway
        content = parse_book_content(daily_content)
        filepath = save_markdown(info, content, output_dir=args.output)
        print(f"Partial content saved to: {filepath}")
        sys.exit(0)
    
    # Fetch full book content
    # Use the slug directly as it already contains the full book identifier
    book_url = f"https://r.jina.ai/http://www.blinkist.com/en/reader/books/{info['slug']}"
    print(f"Fetching book content from: {book_url}")
    
    book_content = fetch_url(book_url)
    
    if not book_content:
        print("WARNING: Failed to fetch full book content, using daily page content")
        book_content = daily_content
    else:
        print("OK Full book content fetched")
    
    # Parse and format content
    parsed_content = parse_book_content(book_content)
    
    # Save to file
    filepath = save_markdown(info, parsed_content, output_dir=args.output)
    print(f"Book summary saved to: {filepath}")
    
    return filepath


if __name__ == '__main__':
    main()
