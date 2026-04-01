---
name: webfetch
description: Fetch web content and extract clean readable text. Better than raw HTML — strips navigation, ads, footers. Falls back to Gbrowser for JS-heavy pages.
---

# WebFetch — Clean Web Content Extraction

Fetch URLs and extract readable content. Removes clutter, returns clean markdown.

## Usage

```bash
python3 webfetch.py <url> [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-chars <N>` | Max characters to return | 10000 |
| `--extract-mode <mode>` | markdown or text | markdown |
| `--timeout <N>` | Request timeout (seconds) | 15 |

## Examples

```bash
# Fetch a news article
python3 webfetch.py "https://example.com/article"

# Fetch with limit
python3 webfetch.py "https://example.com" --max-chars 5000

# Fetch as plain text
python3 webfetch.py "https://example.com" --extract-mode text
```

## What It Does

1. Sends HTTP request with browser-like User-Agent
2. Parses HTML
3. Removes: navigation, ads, footers, sidebars, scripts, styles
4. Extracts: main article content, headings, paragraphs, links
5. Returns clean markdown or text

## Fallback

If the page requires JavaScript (SPA, dynamic content), the agent should use Gbrowser instead:
```bash
# Start Gbrowser, navigate, snapshot
PORT=... TOKEN=...
curl -X POST "http://127.0.0.1:${PORT}/command" -d '{"command":"goto","args":["<url>"]}'
curl -X POST "http://127.0.0.1:${PORT}/command" -d '{"command":"text","args":[]}'
```
