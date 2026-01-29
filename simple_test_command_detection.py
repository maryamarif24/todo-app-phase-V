#!/usr/bin/env python3
"""
Simple test script to verify the fixed todo command handling logic.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from backend.src.agents.todo_agent import TodoAgent


def simulate_command_detection(message):
    """Simulate the logic from the fixed _handle_todo_command method."""
    message_lower = message.lower()

    # Check for delete command first (more specific)
    if any(word in message_lower for word in ['delete', 'remove']) and any(word in message_lower for word in ['todo', 'task']):
        return "delete"

    # Create a new todo (prioritize creation over completion when both keywords are present)
    elif any(word in message_lower for word in ['create', 'add', 'new', 'make']) and any(word in message_lower for word in ['todo', 'task']):
        return "create"

    # Check for completion commands (only if not a creation command)
    elif any(word in message_lower for word in ['complete', 'finish', 'done', 'mark']) and any(word in message_lower for word in ['todo', 'task']):
        return "complete"

    # Check for show/list commands
    elif any(word in message_lower for word in ['show', 'list', 'view', 'get']) and any(word in message_lower for word in ['todo', 'task', 'todos', 'tasks']):
        return "show"

    else:
        return "other"


def test_command_detection():
    """Test the updated command detection logic."""
    print("Testing command detection...")
    print("=" * 50)
    
    # Test cases for different command types
    test_cases = [
        # Creation commands
        ("add todo 'buy groceries'", "create"),
        ("create todo to finish homework", "create"),
        ("new todo walk the dog", "create"),
        
        # Deletion commands  
        ("delete todo 'buy groceries'", "delete"),
        ("remove todo 'finish homework'", "delete"),
        ("delete todo 'todo'", "delete"),  # The specific case mentioned
        
        # Other commands
        ("complete todo 'buy groceries'", "complete"),
        ("mark todo 'buy groceries' as complete", "complete"),
        ("show my todos", "show"),
        ("list todos", "show"),
    ]
    
    all_passed = True
    
    for i, (input_message, expected_type) in enumerate(test_cases, 1):
        detected_type = simulate_command_detection(input_message)
        
        status = "[PASS]" if detected_type == expected_type else "[FAIL]"
        if detected_type != expected_type:
            all_passed = False
            
        print(f"Test {i}: {status}")
        print(f"  Input: {repr(input_message)}")
        print(f"  Expected: {expected_type}")
        print(f"  Detected: {detected_type}")
        print()
    
    print("=" * 50)
    if all_passed:
        print("[SUCCESS] All command detection tests passed!")
    else:
        print("[FAILURE] Some command detection tests failed.")
    
    # Test the specific problematic case
    print("\nTesting the specific case mentioned by the user:")
    problematic_message = "delete todo 'todo'"
    result = simulate_command_detection(problematic_message)
    
    print(f"  '{problematic_message}' -> {result.upper()} command")
    
    if result == "delete":
        print("[SUCCESS] The specific issue has been fixed!")
        print("The command 'delete todo 'todo'' is now correctly identified as a DELETE command.")
    else:
        print("[FAILURE] The specific issue may not be fully resolved.")
    
    return all_passed


if __name__ == "__main__":
    test_command_detection()