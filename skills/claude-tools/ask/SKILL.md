---
name: ask
description: Ask the user structured questions with predefined options. Used by AgentGuard for approval flows and by agents for decision points.
---

# Ask — Structured User Questions

Ask users clear questions with predefined options. Used for approval flows and decision points.

## Usage

```bash
python3 ask.py "<question>" "<option1>" "<option2>" [option3] [option4]
```

## Examples

```bash
# Simple yes/no
python3 ask.py "Delete node_modules?" "Yes, delete it" "No, keep it"

# Multiple options
python3 ask.py "Which approach?" "TypeScript" "Python" "Go" "Rust"

# Approval flow (AgentGuard)
python3 ask.py "Agent wants to run: rm -rf node_modules\nThis will delete 2.3 GB.\nApprove?" "Yes, approve" "No, deny"
```

## Output

Returns the selected option number (1-based) via exit code.
Exit code 1 = first option, 2 = second option, etc.
Exit code 0 = no selection (default).

## Integration with AgentGuard

When AgentGuard returns "ask", the agent should:
1. Describe what will happen
2. Use ask.py to present options
3. Execute or deny based on user's choice
