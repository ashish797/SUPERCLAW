#!/usr/bin/env python3
"""
WebFetch — Clean web content extraction
Fetches URLs and extracts readable content. Removes clutter.

Usage:
  python3 webfetch.py <url> [options]
"""

import sys
import os
import subprocess
import re
import html
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    """Extract readable content from HTML."""
    
    SKIP_TAGS = {'script', 'style', 'nav', 'footer', 'aside', 'header', 'noscript', 'svg', 'iframe'}
    CONTENT_TAGS = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'pre', 'code', 'blockquote', 'article', 'main', 'section', 'div', 'span', 'a', 'strong', 'em', 'br'}
    
    def __init__(self):
        super().__init__()
        self.content = []
        self.skip_depth = 0
        self.in_content = False
        self.current_tag = None
        self.current_text = []
        self.links = []
        self.base_url = None
        
    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        
        attrs_dict = dict(attrs)
        
        if tag == 'a':
            href = attrs_dict.get('href', '')
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                self.links.append(href)
        
        if tag in self.CONTENT_TAGS and self.skip_depth == 0:
            self.current_tag = tag
            self.current_text = []
    
    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        
        if tag == self.current_tag and self.current_text:
            text = ' '.join(self.current_text).strip()
            text = re.sub(r'\s+', ' ', text)
            if len(text) > 10:  # Skip tiny fragments
                self.content.append(text)
            self.current_tag = None
            self.current_text = []
    
    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        stripped = data.strip()
        if stripped:
            self.current_text.append(stripped)
    
    def get_content(self, max_chars=10000):
        result = '\n\n'.join(self.content)
        if len(result) > max_chars:
            result = result[:max_chars] + "\n\n[Truncated — content exceeded max_chars limit]"
        return result

def webfetch(url, max_chars=10000, extract_mode="markdown", timeout=15):
    """Fetch and extract clean content from a URL."""
    
    try:
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
        with urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get('Content-Type', '')
            raw_html = response.read().decode('utf-8', errors='replace')
        
        # Extract content
        extractor = ContentExtractor()
        extractor.feed(raw_html)
        
        clean_content = extractor.get_content(max_chars)
        
        return {
            "success": True,
            "url": url,
            "content": clean_content,
            "content_type": content_type,
            "length": len(clean_content)
        }
    
    except HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
    except URLError as e:
        return {"success": False, "error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 webfetch.py <url> [options]")
        print()
        print("Options:")
        print("  --max-chars <N>     Max characters (default: 10000)")
        print("  --extract-mode <m>  markdown or text (default: markdown)")
        print("  --timeout <N>       Timeout in seconds (default: 15)")
        sys.exit(1)
    
    url = sys.argv[1]
    max_chars = 10000
    extract_mode = "markdown"
    timeout = 15
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--max-chars" and i + 1 < len(sys.argv):
            max_chars = int(sys.argv[i + 1]); i += 2
        elif sys.argv[i] == "--extract-mode" and i + 1 < len(sys.argv):
            extract_mode = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == "--timeout" and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i + 1]); i += 2
        else:
            i += 1
    
    result = webfetch(url, max_chars, extract_mode, timeout)
    
    if result["success"]:
        print(result["content"])
    else:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        print()
        print("Tip: For JavaScript-heavy pages, use Gbrowser instead.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
