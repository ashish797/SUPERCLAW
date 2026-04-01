---
name: file-edit
description: Surgical file editing — replace specific strings without touching the rest of the file. Inspired by Claude Code's FileEditTool. Use instead of writing entire files when making targeted changes.
---

# FileEdit — Surgical File Modification

Replace specific text in files without rewriting the entire file. Preserves formatting, whitespace, and surrounding content.

## Usage

```bash
python3 file-edit.py <file_path> "<old_string>" "<new_string>" [--replace-all]
```

## Examples

### Change a single line
```bash
python3 file-edit.py config.yaml "port: 3000" "port: 8080"
```

### Replace all occurrences
```bash
python3 file-edit.py src/app.ts "localhost" "example.com" --replace-all
```

### Add content after a marker
```bash
python3 file-edit.py README.md "## License" "## New Section\n\nContent here\n\n## License"
```

## How It Differs from Writing Entire Files

| Approach | What happens | Risk |
|----------|-------------|------|
| Write entire file | Reads old, writes new — entire file replaced | Formatting loss, merge conflicts, race conditions |
| FileEdit (this tool) | Finds old_string, replaces with new_string | Minimal — only touched lines change |

## AgentGuard Integration

Always check permission before editing:
```bash
python3 ~/.openclaw/workspace/skills/agent-guard/check-permission.py "write:<file_path>"
```

If decision is `ask`, describe the change to the user and wait for approval.
If decision is `deny`, refuse and explain why.
If decision is `allow`, proceed.
