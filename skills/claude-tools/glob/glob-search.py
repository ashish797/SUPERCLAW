#!/usr/bin/env python3
"""
Glob — File pattern matching
Find files by name pattern. Sorted by modification time (newest first).

Usage:
  python3 glob-search.py "<pattern>" [path]
  
Examples:
  python3 glob-search.py "**/*.ts"
  python3 glob-search.py "*.json" src/
  python3 glob-search.py "**/config.*"
"""

import sys
import os
import glob as globmod
from pathlib import Path

def glob_search(pattern, search_path=".", limit=100):
    """Search for files matching a glob pattern."""
    
    # If pattern doesn't contain **, and path is given, combine them
    if search_path != ".":
        full_pattern = os.path.join(search_path, pattern)
    else:
        full_pattern = pattern
    
    # Use Python's glob with recursive support
    matches = globmod.glob(full_pattern, recursive=True)
    
    # Get modification times and sort (newest first)
    file_info = []
    for match in matches:
        try:
            mtime = os.path.getmtime(match)
            size = os.path.getsize(match)
            file_info.append((match, mtime, size))
        except OSError:
            continue
    
    # Sort by modification time (newest first)
    file_info.sort(key=lambda x: x[1], reverse=True)
    
    # Limit results
    truncated = len(file_info) > limit
    file_info = file_info[:limit]
    
    return {
        "count": len(file_info),
        "truncated": truncated,
        "files": [
            {
                "path": f[0],
                "modified": f[1],
                "size": f[2]
            }
            for f in file_info
        ]
    }

def format_size(size):
    """Format file size humanely."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.0f}{unit}"
        size /= 1024
    return f"{size:.0f}TB"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 glob-search.py \"<pattern>\" [path]")
        print()
        print("Examples:")
        print("  python3 glob-search.py \"**/*.ts\"")
        print("  python3 glob-search.py \"*.json\" src/")
        print("  python3 glob-search.py \"**/config.*\"")
        sys.exit(1)
    
    pattern = sys.argv[1]
    search_path = sys.argv[2] if len(sys.argv) > 2 else "."
    
    result = glob_search(pattern, search_path)
    
    if result["count"] == 0:
        print(f"No files matching '{pattern}'")
        sys.exit(0)
    
    print(f"# {result['count']} files found")
    if result["truncated"]:
        print("# (truncated to 100 results)")
    print()
    
    for f in result["files"]:
        from datetime import datetime
        mod_time = datetime.fromtimestamp(f["modified"]).strftime("%Y-%m-%d %H:%M")
        print(f"{f['path']} ({format_size(f['size'])}, modified {mod_time})")

if __name__ == '__main__':
    main()
