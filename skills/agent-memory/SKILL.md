---
name: agentmemory
description: Auto-extraction of memories from conversations. Periodically analyzes recent messages and saves important facts, decisions, preferences, and context to MEMORY.md and daily memory files.
---

# AgentMemory — Automatic Memory Extraction

Your agent remembers things between sessions. No manual saving required.

## How It Works

```
Conversation happens
    ↓
Every 2 hours (cron) or on /remember command
    ↓
Agent reviews recent messages
    ↓
Extracts: decisions, preferences, context, lessons
    ↓
Deduplicates against existing memories
    ↓
Saves to MEMORY.md (long-term) + memory/YYYY-MM-DD.md (daily)
```

## What Gets Saved

| Category | Example |
|----------|---------|
| **Decisions** | "Chose TypeScript over Python for AgentRouter project" |
| **Preferences** | "User prefers concise responses" |
| **Context** | "Working on AgentRouter — meta-registry for agents. Repo: ashish797/agent-first-web" |
| **Lessons** | "Don't modify production OpenClaw — always use SUPERCLAW dev environment" |
| **People** | "hasH — developer, interested in AI agents, timezone GMT+5:30" |

## What Does NOT Get Saved

- Sensitive data (API keys, passwords, tokens)
- Temporary information (current time, weather)
- Things already in memory
- Greetings and small talk

## Manual Trigger

Add to agent preamble:
```
When user says "/remember", extract memories from the current session and save to memory files.
```

## Cron Setup

```bash
openclaw cron add \
  --name "agentmemory" \
  --schedule "0 */2 * * *" \
  --text "Extract key memories from recent conversations. Read recent messages, identify important facts/decisions/preferences not already in memory files. Update MEMORY.md and memory/YYYY-MM-DD.md. Deduplicate. Only save genuinely new information."
```

## Memory File Format

### MEMORY.md (long-term index)
```markdown
# Memory

- [AgentRouter Project](memory/agentrouter.md) — Meta-registry for AI agents, repo at ashish797/agent-first-web
- [hasH Preferences](memory/hash-preferences.md) — Concise responses, TypeScript preferred, timezone GMT+5:30
- [SUPERCLAW Rule](memory/superclaw-rule.md) — Never modify production, always use dev environment
```

### memory/YYYY-MM-DD.md (daily notes)
```markdown
# 2026-04-02

## Decisions
- Started SUPERCLAW dev environment for safe development
- Chose AgentGuard as first build (foundation for everything else)

## Context
- Building 4 OpenClaw skills: AgentGuard, ClaudeTools, AgentMemory, AgentOrchestrator
- Studying Claude Code leaked source (1.34M lines TypeScript)
- Gbrowser installed and working (gstack browse engine)

## Lessons
- Always check if a server is running before trying to connect
- YAML parsing in Python needs careful indentation handling
```

## Deduplication

Before saving new memories:
1. Read existing MEMORY.md
2. Read existing daily files for recent dates
3. Compare new memories against existing
4. Only add genuinely new information
5. Update existing entries if they've changed (don't duplicate)
