---
name: glob
description: Find files by name pattern or wildcard. Fast file discovery using glob patterns.
---

# Glob — File Pattern Matching

Find files matching a pattern. Much faster than `find` for pattern-based searches.

## Usage

```bash
python3 glob-search.py "<pattern>" [path]
```

## Examples

```bash
# Find all TypeScript files
python3 glob-search.py "**/*.ts"

# Find all JSON files in src/
python3 glob-search.py "*.json" src/

# Find config files
python3 glob-search.py "**/config.*"

# Find test files
python3 glob-search.py "**/*.test.ts"
```

## Output

Results sorted by modification time (newest first). Limited to 100 files.

```
src/main.ts (modified 2026-04-02 00:30)
src/utils.ts (modified 2026-04-02 00:25)
src/config.ts (modified 2026-04-02 00:20)
...
```
