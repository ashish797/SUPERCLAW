#!/usr/bin/env python3
"""
Enhanced Bash — Safe shell command execution
With AgentGuard integration, timeout handling, output truncation.

Usage:
  python3 enhanced-bash.py "<command>" [options]
"""

import sys
import os
import subprocess
import json
import time

AGENTGUARD_SCRIPT = os.path.expanduser("~/.openclaw/workspace/skills/agent-guard/check-permission.py")

def check_agentguard(command):
    """Check command against AgentGuard policy."""
    if not os.path.exists(AGENTGUARD_SCRIPT):
        return {"decision": "allow", "rule": "no-agentguard", "description": "AgentGuard not installed"}
    
    try:
        result = subprocess.run(
            ["python3", AGENTGUARD_SCRIPT, f"bash:{command}"],
            capture_output=True, text=True, timeout=5
        )
        return json.loads(result.stdout)
    except Exception:
        return {"decision": "allow", "rule": "error", "description": "AgentGuard check failed"}

def run_command(command, timeout=30, max_output=10240, cwd=None, skip_guard=False):
    """Execute a command with safety checks."""
    
    # AgentGuard check
    if not skip_guard:
        guard_result = check_agentguard(command)
        if guard_result["decision"] == "deny":
            return {
                "command": command,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"DENIED by AgentGuard: {guard_result['description']}\nRule: {guard_result['rule']}",
                "duration_ms": 0,
                "truncated": False,
                "agentguard": guard_result
            }
        if guard_result["decision"] == "ask":
            return {
                "command": command,
                "exit_code": -2,
                "stdout": "",
                "stderr": f"REQUIRES APPROVAL: {guard_result['description']}\nRule: {guard_result['rule']}\nApprove this command? (This is handled by the agent, not the script)",
                "duration_ms": 0,
                "truncated": False,
                "agentguard": guard_result
            }
    
    # Execute
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        duration_ms = int((time.time() - start_time) * 1000)
        
        stdout = result.stdout
        stderr = result.stderr
        
        # Truncate output
        truncated = False
        if len(stdout) > max_output:
            stdout = stdout[:max_output] + f"\n\n[Truncated — output was {len(result.stdout)} bytes, showing first {max_output}]"
            truncated = True
        if len(stderr) > max_output:
            stderr = stderr[:max_output] + "\n\n[Truncated]"
        
        return {
            "command": command,
            "exit_code": result.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "duration_ms": duration_ms,
            "truncated": truncated
        }
    
    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds",
            "duration_ms": timeout * 1000,
            "truncated": False
        }
    except Exception as e:
        return {
            "command": command,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "duration_ms": 0,
            "truncated": False
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 enhanced-bash.py \"<command>\" [options]")
        print()
        print("Options:")
        print("  --timeout <N>     Kill after N seconds (default: 30)")
        print("  --max-output <N>  Max output bytes (default: 10240)")
        print("  --cwd <dir>       Working directory")
        print("  --no-guard        Skip AgentGuard check")
        sys.exit(1)
    
    command = sys.argv[1]
    timeout = 30
    max_output = 10240
    cwd = None
    skip_guard = False
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--timeout" and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i + 1]); i += 2
        elif sys.argv[i] == "--max-output" and i + 1 < len(sys.argv):
            max_output = int(sys.argv[i + 1]); i += 2
        elif sys.argv[i] == "--cwd" and i + 1 < len(sys.argv):
            cwd = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == "--no-guard":
            skip_guard = True; i += 1
        else:
            i += 1
    
    result = run_command(command, timeout, max_output, cwd, skip_guard)
    
    # Output
    if result["exit_code"] == -2:
        # Needs approval
        print(result["stderr"], file=sys.stderr)
        sys.exit(1)
    elif result["exit_code"] == -1:
        # Denied or error
        print(result["stderr"], file=sys.stderr)
        sys.exit(2)
    else:
        if result["stdout"]:
            print(result["stdout"], end='')
        if result["stderr"]:
            print(result["stderr"], file=sys.stderr, end='')
        if result["truncated"]:
            print(f"\n[Command completed in {result['duration_ms']}ms, output truncated]", file=sys.stderr)
        sys.exit(result["exit_code"])

if __name__ == '__main__':
    main()
