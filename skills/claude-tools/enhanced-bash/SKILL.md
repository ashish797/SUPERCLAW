---
name: enhanced-bash
description: Enhanced shell command execution with AgentGuard integration, timeout handling, output truncation, and structured results. Use instead of raw exec for all bash commands.
---

# Enhanced Bash — Safe Shell Execution

Run shell commands with safety checks, timeouts, and output management.

## Usage

```bash
python3 enhanced-bash.py "<command>" [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--timeout <N>` | Kill after N seconds | 30 |
| `--max-output <N>` | Max output bytes | 10240 (10KB) |
| `--cwd <dir>` | Working directory | current |
| `--no-guard` | Skip AgentGuard check | off |

## Features

### AgentGuard Integration
Every command is checked against the AgentGuard policy before execution:
- Safe commands (ls, cat, git status) → auto-execute
- Moderate commands (rm, curl) → ask user
- Dangerous commands (sudo, eval) → block

### Timeout Handling
Commands are killed after the timeout period. Default 30 seconds.

### Output Truncation
Large outputs are truncated to prevent context overflow. Default 10KB.

### Structured Result
```json
{
  "command": "ls -la",
  "exit_code": 0,
  "stdout": "...",
  "stderr": "",
  "duration_ms": 150,
  "truncated": false
}
```

## Examples

```bash
# Safe command (auto-execute)
python3 enhanced-bash.py "ls -la"

# With timeout
python3 enhanced-bash.py "npm install" --timeout 120

# In specific directory
python3 enhanced-bash.py "git status" --cwd /path/to/repo

# Long output (truncated)
python3 enhanced-bash.py "find / -name '*.log'" --max-output 5000
```
