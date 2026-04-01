#!/usr/bin/env python3
"""
FileEdit — Surgical file modification
Replace specific strings without touching the rest of the file.

Usage:
  python3 file-edit.py <file_path> "<old_string>" "<new_string>" [--replace-all]

Example:
  python3 file-edit.py config.yaml "port: 3000" "port: 8080"
  python3 file-edit.py src/app.ts "localhost" "example.com" --replace-all
"""

import sys
import os
import difflib

def file_edit(file_path, old_string, new_string, replace_all=False):
    """Perform surgical file edit."""
    
    # Validate inputs
    if not os.path.exists(file_path):
        return {"success": False, "error": f"File not found: {file_path}"}
    
    if old_string == new_string:
        return {"success": False, "error": "old_string and new_string must be different"}
    
    if not old_string:
        return {"success": False, "error": "old_string cannot be empty"}
    
    # Read file
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        original = f.read()
    
    # Check if old_string exists
    count = original.count(old_string)
    if count == 0:
        # Try to find similar strings
        lines = original.split('\n')
        suggestions = []
        for i, line in enumerate(lines, 1):
            similarity = difflib.SequenceMatcher(None, old_string, line).ratio()
            if similarity > 0.5:
                suggestions.append(f"  Line {i}: {line.strip()[:80]}")
        
        result = {"success": False, "error": f"String not found: '{old_string[:50]}...'"}
        if suggestions:
            result["suggestions"] = suggestions[:5]
        return result
    
    if count > 1 and not replace_all:
        return {
            "success": False,
            "error": f"Found {count} occurrences. Use --replace-all to replace all, or make old_string more specific."
        }
    
    # Perform replacement
    if replace_all:
        modified = original.replace(old_string, new_string)
        replaced = count
    else:
        modified = original.replace(old_string, new_string, 1)
        replaced = 1
    
    # Generate diff
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        original_lines, modified_lines,
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        lineterm=''
    ))
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified)
    
    return {
        "success": True,
        "file": file_path,
        "replaced": replaced,
        "diff": ''.join(diff[:50])  # Limit diff output
    }

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 file-edit.py <file_path> \"<old_string>\" \"<new_string>\" [--replace-all]")
        print()
        print("Examples:")
        print("  python3 file-edit.py config.yaml \"port: 3000\" \"port: 8080\"")
        print("  python3 file-edit.py src/app.ts \"localhost\" \"example.com\" --replace-all")
        sys.exit(1)
    
    file_path = sys.argv[1]
    old_string = sys.argv[2]
    new_string = sys.argv[3]
    replace_all = "--replace-all" in sys.argv
    
    result = file_edit(file_path, old_string, new_string, replace_all)
    
    if result["success"]:
        print(f"OK — {result['replaced']} replacement(s) in {result['file']}")
        if result.get("diff"):
            print()
            print("Diff:")
            print(result["diff"])
    else:
        print(f"ERROR — {result['error']}", file=sys.stderr)
        if result.get("suggestions"):
            print("Did you mean one of these?", file=sys.stderr)
            for s in result["suggestions"]:
                print(s, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
