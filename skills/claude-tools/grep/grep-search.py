#!/usr/bin/env python3
"""
Grep — Fast content search using ripgrep
Falls back to grep -r if rg is not installed.

Usage:
  python3 grep-search.py "<pattern>" [options]
"""

import sys
import os
import subprocess
import shlex

def has_ripgrep():
    """Check if ripgrep is installed."""
    try:
        subprocess.run(["rg", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def grep_search(pattern, path=".", glob=None, file_type=None, 
                case_insensitive=False, show_line_numbers=True,
                context=0, after=0, before=0, files_only=False,
                count_only=False, limit=50):
    """Search file contents."""
    
    use_rg = has_ripgrep()
    
    if use_rg:
        cmd = ["rg", "--no-heading", "--color=never"]
        
        if case_insensitive:
            cmd.append("-i")
        if show_line_numbers:
            cmd.append("-n")
        if context > 0:
            cmd.extend(["-C", str(context)])
        if after > 0:
            cmd.extend(["-A", str(after)])
        if before > 0:
            cmd.extend(["-B", str(before)])
        if files_only:
            cmd.append("-l")
        if count_only:
            cmd.append("-c")
        if glob:
            cmd.extend(["--glob", glob])
        if file_type:
            cmd.extend(["--type", file_type])
        
        cmd.extend(["--max-count", str(limit)])
        cmd.append(pattern)
        cmd.append(path)
        
    else:
        # Fallback to grep
        cmd = ["grep", "-r", "-n"]
        if case_insensitive:
            cmd.append("-i")
        if context > 0:
            cmd.extend([f"-C{context}"])
        if after > 0:
            cmd.extend([f"-A{after}"])
        if before > 0:
            cmd.extend([f"-B{before}"])
        if files_only:
            cmd.append("-l")
        
        if glob:
            cmd.extend(["--include", glob])
        
        cmd.append(pattern)
        cmd.append(path)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout.strip()
        
        if not output:
            return {"matches": 0, "results": [], "tool": "rg" if use_rg else "grep"}
        
        lines = output.split('\n')
        
        # Limit results
        if len(lines) > limit:
            lines = lines[:limit]
            truncated = True
        else:
            truncated = False
        
        return {
            "matches": len(lines),
            "results": lines,
            "truncated": truncated,
            "tool": "rg" if use_rg else "grep"
        }
    
    except subprocess.TimeoutExpired:
        return {"matches": 0, "results": [], "error": "Search timed out (30s limit)"}
    except Exception as e:
        return {"matches": 0, "results": [], "error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 grep-search.py \"<pattern>\" [options]")
        print()
        print("Options:")
        print("  --path <dir>     Directory to search (default: .)")
        print("  --glob <pattern> File glob filter (e.g. *.ts)")
        print("  --type <type>    File type (js, py, ts, etc.)")
        print("  -i               Case insensitive")
        print("  -C <N>           Context lines")
        print("  -A <N>           Lines after match")
        print("  -B <N>           Lines before match")
        print("  --files          Only show file names")
        print("  --count          Show match counts")
        print("  --limit <N>      Max results (default: 50)")
        sys.exit(1)
    
    pattern = sys.argv[1]
    
    # Parse options
    kwargs = {}
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--path" and i + 1 < len(sys.argv):
            kwargs["path"] = sys.argv[i + 1]; i += 2
        elif arg == "--glob" and i + 1 < len(sys.argv):
            kwargs["glob"] = sys.argv[i + 1]; i += 2
        elif arg == "--type" and i + 1 < len(sys.argv):
            kwargs["file_type"] = sys.argv[i + 1]; i += 2
        elif arg == "-i":
            kwargs["case_insensitive"] = True; i += 1
        elif arg == "-n":
            kwargs["show_line_numbers"] = True; i += 1
        elif arg == "-C" and i + 1 < len(sys.argv):
            kwargs["context"] = int(sys.argv[i + 1]); i += 2
        elif arg == "-A" and i + 1 < len(sys.argv):
            kwargs["after"] = int(sys.argv[i + 1]); i += 2
        elif arg == "-B" and i + 1 < len(sys.argv):
            kwargs["before"] = int(sys.argv[i + 1]); i += 2
        elif arg == "--files":
            kwargs["files_only"] = True; i += 1
        elif arg == "--count":
            kwargs["count_only"] = True; i += 1
        elif arg == "--limit" and i + 1 < len(sys.argv):
            kwargs["limit"] = int(sys.argv[i + 1]); i += 2
        else:
            i += 1
    
    result = grep_search(pattern, **kwargs)
    
    if result.get("error"):
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    print(f"# {result['matches']} matches ({result['tool']})")
    if result.get("truncated"):
        print(f"# (truncated to {kwargs.get('limit', 50)} results)")
    print()
    
    for line in result["results"]:
        print(line)

if __name__ == '__main__':
    main()
