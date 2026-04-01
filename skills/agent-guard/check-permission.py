#!/usr/bin/env python3
"""
AgentGuard Permission Checker
Checks an action against the AgentGuard policy and returns the decision.

Usage:
  python3 check-permission.py "bash:rm -rf node_modules"
  python3 check-permission.py "write:.env"
  python3 check-permission.py "read:package.json"
"""

import sys
import json
import os
import fnmatch
from datetime import datetime, timezone

POLICY_PATH = os.path.expanduser("~/.openclaw/workspace/agentguard-policy.yaml")
LOG_PATH = os.path.expanduser("~/.openclaw/workspace/agentguard-log.jsonl")

def load_policy():
    """Load the YAML policy file."""
    policy = {"version": "1.0", "mode": "default", "rules": []}
    
    if not os.path.exists(POLICY_PATH):
        # Fallback to skill directory
        alt_path = os.path.join(os.path.dirname(__file__), "agentguard-policy.yaml")
        if os.path.exists(alt_path):
            policy_path = alt_path
        else:
            return policy
    else:
        policy_path = POLICY_PATH
    
    with open(policy_path, 'r') as f:
        lines = f.readlines()
    
    current_rule = {}
    for line in lines:
        stripped = line.strip()
        
        # Skip comments and empty lines
        if not stripped or stripped.startswith('#'):
            continue
        
        # Top-level keys
        if stripped.startswith('version:'):
            policy['version'] = stripped.split(':', 1)[1].strip().strip('"').strip("'")
        elif stripped.startswith('mode:'):
            policy['mode'] = stripped.split(':', 1)[1].strip()
        # Rule items
        elif stripped.startswith('- pattern:'):
            if current_rule and 'pattern' in current_rule:
                policy['rules'].append(current_rule)
            pattern = stripped.split(':', 1)[1].strip().strip('"').strip("'")
            current_rule = {'pattern': pattern}
        elif stripped.startswith('action:'):
            current_rule['action'] = stripped.split(':', 1)[1].strip()
        elif stripped.startswith('description:'):
            desc = stripped.split(':', 1)[1].strip().strip('"').strip("'")
            current_rule['description'] = desc
    
    if current_rule and 'pattern' in current_rule:
        policy['rules'].append(current_rule)
    
    return policy

def check_permission(action, policy):
    """Check an action against the policy."""
    mode = policy.get('mode', 'default')
    
    if mode == 'bypass':
        return {'action': action, 'decision': 'allow', 'rule': 'mode:bypass', 'description': 'Bypass mode'}
    
    if mode == 'plan':
        return {'action': action, 'decision': 'ask', 'rule': 'mode:plan', 'description': 'Plan mode'}
    
    for rule in policy.get('rules', []):
        pattern = rule.get('pattern', '')
        if fnmatch.fnmatch(action, pattern):
            return {
                'action': action,
                'decision': rule.get('action', 'ask'),
                'rule': pattern,
                'description': rule.get('description', '')
            }
    
    return {'action': action, 'decision': 'ask', 'rule': 'default', 'description': 'No matching rule'}

def log_decision(result, approved=None):
    """Log the decision."""
    entry = {'timestamp': datetime.now(timezone.utc).isoformat(), **result}
    if approved is not None:
        entry['approved'] = approved
    
    os.makedirs(os.path.dirname(LOG_PATH) if os.path.dirname(LOG_PATH) else '.', exist_ok=True)
    
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check-permission.py '<category>:<action>'")
        sys.exit(1)
    
    action = sys.argv[1]
    policy = load_policy()
    result = check_permission(action, policy)
    
    log_decision(result)
    print(json.dumps(result, indent=2))
    
    if result['decision'] == 'deny':
        sys.exit(2)
    elif result['decision'] == 'ask':
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
