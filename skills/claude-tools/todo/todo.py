#!/usr/bin/env python3
"""
Todo — Session task checklist
Track tasks, mark as pending/in-progress/completed.

Usage:
  python3 todo.py list|add|start|done|clear|status [args]
"""

import sys
import os
import json

TODO_FILE = os.path.expanduser("~/.openclaw/workspace/.session-todos.json")

def load_todos():
    """Load todos from file."""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to file."""
    os.makedirs(os.path.dirname(TODO_FILE), exist_ok=True)
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def list_todos():
    """List all todos."""
    todos = load_todos()
    if not todos:
        print("No tasks. Add one with: python3 todo.py add \"task description\"")
        return
    
    print("# Current Tasks\n")
    for i, todo in enumerate(todos, 1):
        if todo['status'] == 'completed':
            symbol = '[x]'
        elif todo['status'] == 'in_progress':
            symbol = '[~]'
        else:
            symbol = '[ ]'
        print(f"{symbol} {i}. {todo['text']}")
    
    total = len(todos)
    done = sum(1 for t in todos if t['status'] == 'completed')
    if total > 0:
        pct = (done / total) * 100
        print(f"\nProgress: {done}/{total} completed ({pct:.0f}%)")

def add_todo(text):
    """Add a new todo."""
    todos = load_todos()
    todos.append({"text": text, "status": "pending"})
    save_todos(todos)
    print(f"Added: {text}")

def start_todo(index):
    """Mark a todo as in-progress."""
    todos = load_todos()
    idx = index - 1
    if 0 <= idx < len(todos):
        todos[idx]['status'] = 'in_progress'
        save_todos(todos)
        print(f"In progress: {todos[idx]['text']}")
    else:
        print(f"Error: Task {index} not found")

def done_todo(index):
    """Mark a todo as completed."""
    todos = load_todos()
    idx = index - 1
    if 0 <= idx < len(todos):
        todos[idx]['status'] = 'completed'
        save_todos(todos)
        print(f"Completed: {todos[idx]['text']}")
    else:
        print(f"Error: Task {index} not found")

def clear_completed():
    """Remove completed todos."""
    todos = load_todos()
    before = len(todos)
    todos = [t for t in todos if t['status'] != 'completed']
    save_todos(todos)
    print(f"Cleared {before - len(todos)} completed tasks")

def show_status():
    """Show summary status."""
    todos = load_todos()
    total = len(todos)
    pending = sum(1 for t in todos if t['status'] == 'pending')
    in_progress = sum(1 for t in todos if t['status'] == 'in_progress')
    completed = sum(1 for t in todos if t['status'] == 'completed')
    
    print(f"Total: {total} | Pending: {pending} | In Progress: {in_progress} | Completed: {completed}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 todo.py <command> [args]")
        print()
        print("Commands:")
        print("  list              Show all todos")
        print("  add <text>        Add a new todo")
        print("  start <number>    Mark as in-progress")
        print("  done <number>     Mark as completed")
        print("  clear             Remove completed todos")
        print("  status            Show summary")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        list_todos()
    elif cmd == "add":
        text = " ".join(sys.argv[2:])
        add_todo(text)
    elif cmd == "start":
        start_todo(int(sys.argv[2]))
    elif cmd == "done":
        done_todo(int(sys.argv[2]))
    elif cmd == "clear":
        clear_completed()
    elif cmd == "status":
        show_status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()
