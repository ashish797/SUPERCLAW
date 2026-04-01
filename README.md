# SUPERCLAW — OpenClaw Code Suite

Four skills that transform OpenClaw from a good agent into a powerful multi-agent system.

Inspired by Claude Code's architecture (1.34M lines of TypeScript), adapted for OpenClaw's skill system.

## Components

### 1. AgentGuard — Permission System
Makes agents safe. Every tool/skill execution is checked against a configurable policy.

```bash
clawhub install agentguard
```
- Configurable allow/ask/deny rules
- Pattern matching (e.g., `bash:rm*`, `write:*.env`)
- Audit logging
- Modes: default, plan, auto, bypass

### 2. ClaudeTools — Enhanced Tools
Better tools for better results.

```bash
clawhub install claudetools
```
- **file-edit** — Surgical file modification (replace strings, not files)
- **grep** — Fast content search (ripgrep-powered)
- **glob** — File pattern matching
- **webfetch** — Better web content extraction
- **enhanced-bash** — Shell with timeout, output limits, AgentGuard integration

### 3. AgentMemory — Auto Memory Extraction
Your agent remembers things between sessions. No manual saving.

```bash
clawhub install agentmemory
```
- Auto-extracts decisions, preferences, context, lessons
- Deduplicates against existing memories
- Cron-based (every 2 hours) + manual trigger (/remember)
- Saves to MEMORY.md + daily files

### 4. AgentOrchestrator — Multi-Agent Coordination
Complex tasks become parallel. 30 minutes becomes 5.

```bash
clawhub install agentorchestrator
```
- Task decomposition into independent sub-tasks
- Parallel execution via sub-agents
- Result aggregation
- Failure handling (partial results, retries)

## Install All

```bash
clawhub install agentguard
clawhub install claudetools
clawhub install agentmemory
clawhub install agentorchestrator
```

## The Difference

| Before | After |
|--------|-------|
| Agent runs `rm -rf` without asking | AgentGuard asks before dangerous operations |
| Agent rewrites entire files for one-line changes | FileEdit does surgical replacements |
| Agent forgets everything between sessions | AgentMemory auto-extracts and persists |
| Complex tasks done sequentially | AgentOrchestrator runs parallel sub-agents |

## How They Stack

```
User message
    ↓
AgentOrchestrator (splits into parallel tasks)
    ↓
AgentGuard (checks permissions for each action)
    ↓
ClaudeTools (executes with better tools)
    ↓
AgentMemory (extracts learnings from interaction)
    ↓
Response to user
```

## Credits

Architecture patterns studied from:
- Claude Code (Anthropic) — leaked source, 1.34M lines
- OpenClaw — the base agent platform
- gstack (Gary Tan) — browser automation

## License

MIT
