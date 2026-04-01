---
name: agentorchestrator
description: Multi-agent task decomposition and parallel execution. Break complex tasks into sub-tasks, run independent tasks in parallel using sub-agents, aggregate results. Inspired by Claude Code's AgentTool + coordinator.
---

# AgentOrchestrator — Multi-Agent Task Coordination

Break complex tasks into parallel sub-agents. What took 30 minutes sequentially now takes 5.

## How It Works

```
User: "Research x402, MCP, and A2A and compare them"
    ↓
Orchestrator analyzes task
    ↓
Identifies 3 independent sub-tasks
    ↓
Spawns 3 sub-agents in parallel (sessions_spawn)
    ↓
All 3 work simultaneously
    ↓
Results aggregated into comparison
    ↓
Delivered to user
```

## When to Use

- Research multiple topics simultaneously
- Build multiple components in parallel
- Analyze multiple files at once
- Any task that can be split into independent pieces

## Task Decomposition

When a task has multiple independent parts:

```yaml
plan:
  - id: task-1
    description: "Research x402 protocol"
    agent_prompt: "Research the x402 payment protocol. Find: how it works, key players, adoption stats, strengths, weaknesses. Return a structured summary."
    dependencies: []
    
  - id: task-2
    description: "Research MCP protocol"
    agent_prompt: "Research the MCP (Model Context Protocol). Find: architecture, adoption, strengths, weaknesses. Return a structured summary."
    dependencies: []
    
  - id: task-3
    description: "Research A2A protocol"
    agent_prompt: "Research the A2A (Agent-to-Agent) protocol by Google. Find: architecture, adoption, strengths, weaknesses. Return a structured summary."
    dependencies: []
    
  - id: task-4
    description: "Compare all three"
    agent_prompt: "Given these three analyses, create a comparison table showing strengths, weaknesses, and use cases for each protocol."
    dependencies: [task-1, task-2, task-3]
```

## Execution Rules

1. **Identify parallelism** — Tasks with no dependencies run simultaneously
2. **Spawn sub-agents** — Use `sessions_spawn` for each parallel task
3. **Wait for completion** — Collect results from all sub-agents
4. **Handle failures** — If one sub-agent fails, others continue
5. **Aggregate results** — Merge outputs into coherent response
6. **Deliver** — Present combined result to user

## Agent Preamble Integration

When you receive a complex task with multiple independent parts:

1. Analyze: Can this be split into parallel sub-tasks?
2. If yes: Create execution plan with dependencies
3. Show plan to user (optional)
4. Spawn sub-agents for parallel tasks
5. Wait for results
6. Feed results to dependent tasks
7. Aggregate and deliver

## Example User Prompts That Trigger Orchestration

- "Research X, Y, and Z and compare them"
- "Build a REST API with auth, database, and tests"
- "Analyze these 5 files for security issues"
- "Create documentation for all our skills"
- "Review and test all changes in the last week"

## Failure Handling

If a sub-agent fails:
- Other sub-agents continue
- Report partial results
- Note which task failed and why
- Offer to retry failed task
