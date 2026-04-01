---
name: todo
description: Session task checklist. Track what needs to be done, mark items as in-progress or completed. Visible to the user.
---

# Todo — Session Task Checklist

Track tasks within a session. Shows progress to the user.

## Usage

```bash
# List current todos
python3 todo.py list

# Add a task
python3 todo.py add "Research x402 protocol"

# Mark as in-progress
python3 todo.py start 1

# Mark as completed
python3 todo.py done 1

# Clear completed
python3 todo.py clear

# Show status
python3 todo.py status
```

## States

| State | Symbol | Meaning |
|-------|--------|---------|
| pending | `[ ]` | Not started |
| in_progress | `[~]` | Currently working on |
| completed | `[x]` | Done |

## Example Output

```
# Current Tasks

[x] Set up SUPERCLAW dev environment
[~] Build AgentGuard permission system
[ ] Build ClaudeTools enhanced tools
[ ] Build AgentMemory auto-extraction
[ ] Build AgentOrchestrator multi-agent

Progress: 1/5 completed (20%)
```

## When to Use

- Breaking down complex tasks into steps
- Showing progress on multi-step work
- Tracking what's been done in a session
- Communicating status to the user
