# SUPERCLAW — Dev Environment Rules

## CRITICAL RULES

1. ALL code changes go in `/data/.openclaw/workspace/SUPERCLAW/` ONLY
2. NEVER modify anything in production OpenClaw (`/usr/local/lib/node_modules/openclaw/`)
3. NEVER modify production skills (`~/.openclaw/workspace/skills/`)
4. NEVER restart or modify the running OpenClaw process
5. SUPERCLAW is for building and testing ONLY
6. When ready, we deploy by copying skills to production or publishing to ClawHub

## Structure

```
SUPERCLAW/
├── openclaw-dev/          # Fresh OpenClaw clone (modify here)
│   └── skills/
│       ├── agent-guard/    # Phase 1: Permission system
│       ├── claude-tools/   # Phase 2: Enhanced tools
│       │   ├── file-edit/
│       │   ├── grep/
│       │   ├── glob/
│       │   ├── webfetch/
│       │   └── enhanced-bash/
│       ├── agent-memory/   # Phase 3: Auto memory extraction
│       └── agent-orchestrator/ # Phase 4: Multi-agent coordination
│
├── claude-code-study/     # Reference only (DO NOT modify)
│   └── src/tools/         # Read Claude Code tool implementations
│
└── ROADMAP.md             # Build tracking
```

## How to Deploy

When a skill is ready:
1. Test in SUPERCLAW
2. Copy to production: `cp -r SUPERCLAW/openclaw-dev/skills/NAME ~/.openclaw/workspace/skills/`
3. OR publish to ClawHub: `clawhub publish ./skill --slug name`

Last updated: 2026-04-02
