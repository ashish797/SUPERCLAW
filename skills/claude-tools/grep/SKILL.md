---
name: grep
description: Fast content search using ripgrep. Search file contents with regex patterns, glob filters, context lines. Much faster and cleaner than find+grep.
---

# Grep — Fast Content Search

Search file contents using ripgrep (rg). If rg is not installed, falls back to grep -r.

## Usage

```bash
python3 grep-search.py "<pattern>" [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--path <dir>` | Directory to search | current dir |
| `--glob <pattern>` | Filter files (e.g. "*.ts") | all files |
| `--type <type>` | File type (js, py, ts, etc.) | all |
| `-i` | Case insensitive | off |
| `-n` | Show line numbers | on |
| `-C <N>` | Context lines (before and after) | 0 |
| `-A <N>` | Lines after match | 0 |
| `-B <N>` | Lines before match | 0 |
| `--files` | Only show file names | off |
| `--count` | Show match counts | off |
| `--limit <N>` | Max results | 50 |

## Examples

```bash
# Find TODO comments
python3 grep-search.py "TODO|FIXME" --type ts

# Search in specific directory with context
python3 grep-search.py "error" --path src/ -C 2

# Search with glob filter
python3 grep-search.py "import.*react" --glob "*.tsx"

# Case insensitive search
python3 grep-search.py "Error" -i

# Just list files with matches
python3 grep-search.py "TODO" --files
```

## Output Format

```
file:line:content
```

Example:
```
src/app.ts:15:const PORT = 3000;
src/app.ts:42:console.log(`Server on port ${PORT}`);
src/config.ts:3:port: 3000,
```
