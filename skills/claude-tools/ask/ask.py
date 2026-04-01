#!/usr/bin/env python3
"""
Ask — Structured user questions
Present options and get user's choice.

Usage:
  python3 ask.py "<question>" "<option1>" "<option2>" [option3] [option4]

Exit codes:
  1 = first option selected
  2 = second option selected
  N = Nth option selected
  0 = no selection (default)
"""

import sys

def ask_question(question, options):
    """Ask a question with options and return the selected index."""
    
    print(f"\n{'='*50}")
    print(f"  {question}")
    print(f"{'='*50}\n")
    
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    print()
    
    while True:
        try:
            choice = input("Select (number): ").strip()
            if not choice:
                return 0  # Default — no selection
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num
            else:
                print(f"Please enter 1-{len(options)}")
        except (ValueError, EOFError):
            return 0
        except KeyboardInterrupt:
            print("\nCancelled.")
            return 0

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 ask.py \"<question>\" \"<option1>\" \"<option2>\" [option3] [option4]")
        print()
        print("Example:")
        print("  python3 ask.py \"Delete node_modules?\" \"Yes, delete\" \"No, keep it\"")
        sys.exit(1)
    
    question = sys.argv[1]
    options = sys.argv[2:]
    
    selected = ask_question(question, options)
    
    if selected > 0:
        print(f"\nSelected: {options[selected - 1]}")
    
    # Exit code = selected option (1-based)
    sys.exit(selected if selected > 0 else 0)

if __name__ == '__main__':
    main()
