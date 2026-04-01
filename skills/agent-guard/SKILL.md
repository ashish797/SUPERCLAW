---
name: agentguard
description: Permission system for OpenClaw agents. Checks every tool/skill execution against a configurable policy. Blocks dangerous operations, asks before sensitive operations, auto-approves safe ones. Inspired by Claude Code's permission system.
---

# AgentGuard — Permission System for OpenClaw

Every agent execution goes through AgentGuard. Dangerous operations are blocked or require approval.

## How It Works

```
Agent wants to run: rm -rf node_modules
    ↓
AgentGuard checks policy
    ↓
Policy says: bash:rm* → ASK
    ↓
Agent asks user: "This will delete node_modules. Approve? [y/N]"
    ↓
User decides
```

## Permission Modes

| Mode | Behavior |
|------|----------|
| `allow` | Auto-approve. No prompt. |
| `ask` | Show user what will happen, wait for approval. |
| `deny` | Block. Never execute. |

## Policy File

Located at: `~/.openclaw/workspace/agentguard-policy.yaml`

```yaml
# AgentGuard Policy
version: "1.0"
mode: default  # default | plan | auto | bypass

rules:
  # READ operations — always safe
  - pattern: "read:*"
    action: allow
    description: "All read operations are safe"

  # WRITE operations — ask by default
  - pattern: "write:*.md"
    action: allow
    description: "Markdown edits are safe"
  - pattern: "write:*.env"
    action: ask
    description: "Contains secrets — ask before editing"
  - pattern: "write:*"
    action: ask
    description: "Ask before any other writes"

  # BASH operations — categorized by safety
  - pattern: "bash:git*"
    action: allow
    description: "Git operations are safe"
  - pattern: "bash:npm*"
    action: allow
    description: "Package management is safe"
  - pattern: "bash:ls*"
    action: allow
    description: "Listing files is safe"
  - pattern: "bash:cat*"
    action: allow
    description: "Reading files is safe"
  - pattern: "bash:find*"
    action: allow
    description: "Finding files is safe"
  - pattern: "bash:echo*"
    action: allow
    description: "Echo is safe"
  - pattern: "bash:mkdir*"
    action: allow
    description: "Creating directories is safe"
  - pattern: "bash:cp*"
    action: ask
    description: "Ask before copying"
  - pattern: "bash:mv*"
    action: ask
    description: "Ask before moving"
  - pattern: "bash:rm*"
    action: ask
    description: "Ask before deleting"
  - pattern: "bash:chmod*"
    action: ask
    description: "Ask before changing permissions"
  - pattern: "bash:docker*"
    action: ask
    description: "Ask before Docker operations"
  - pattern: "bash:curl*"
    action: ask
    description: "Ask before HTTP requests"
  - pattern: "bash:wget*"
    action: ask
    description: "Ask before downloads"
  - pattern: "bash:pip*"
    action: ask
    description: "Ask before Python package operations"
  - pattern: "bash:sudo*"
    action: deny
    description: "Never allow sudo"
  - pattern: "bash:eval*"
    action: deny
    description: "Never allow eval"
  - pattern: "bash:*"
    action: ask
    description: "Ask for any other bash command"

  # DEPLOYMENT — always deny auto-deploy
  - pattern: "deploy:*"
    action: deny
    description: "Never auto-deploy"
```

## Usage in Agent Preamble

Add to your agent's preamble or AGENTS.md:

```
Before executing any bash command or writing any file:
1. Read ~/.openclaw/workspace/agentguard-policy.yaml
2. Match the command against rules (first match wins)
3. If action is 'allow': proceed without asking
4. If action is 'ask': describe what will happen and ask user
5. If action is 'deny': refuse and explain why
5. Log all decisions to ~/.openclaw/workspace/agentguard-log.jsonl
```

## Log File

All permission decisions are logged to: `~/.openclaw/workspace/agentguard-log.jsonl`

```json
{"timestamp":"2026-04-02T00:45:00Z","action":"bash:rm -rf node_modules","decision":"ask","rule":"bash:rm*","approved":true}
{"timestamp":"2026-04-02T00:45:01Z","action":"write:.env","decision":"ask","rule":"write:*.env","approved":false}
```

## Customization

Edit `agentguard-policy.yaml` to customize:

```yaml
# Add a new rule
- pattern: "bash:kubectl*"
  action: deny
  description: "Never allow kubectl without explicit approval"

# Make everything auto-approve (dangerous!)
mode: bypass

# Plan mode — show what would happen, don't execute
mode: plan
```
