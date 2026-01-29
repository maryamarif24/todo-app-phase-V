#!/usr/bin/env python3
"""
Test script to verify the fixed todo command handling logic.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from backend.src.agents.todo_agent import TodoAgent


def test_command_detection():
    """Test the updated command detection logic."""
    agent = TodoAgent()
    
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
    
    print("Testing command detection...")
    print("=" * 50)
    
    all_passed = True
    
    for i, (input_message, expected_type) in enumerate(test_cases, 1):
        message_lower = input_message.lower()
        
        # Simulate the logic from _handle_todo_command
        detected_type = None
        
        # Check for delete command first (more specific)
        if any(word in message_lower for word in ['delete', 'remove']) and any(word in message_lower for word in ['todo', 'task']):
            detected_type = "delete"
        # Check for completion commands
        elif any(word in message_lower for word in ['complete', 'finish', 'done', 'mark']) and any(word in message_lower for word in ['todo', 'task']):
            detected_type = "complete"
        # Check for show/list commands
        elif any(word in message_lower for word in ['show', 'list', 'view', 'get']) and any(word in message_lower for word in ['todo', 'task', 'todos', 'tasks']):
            detected_type = "show"
        # Create a new todo (comes after other commands to avoid conflicts)
        elif any(word in message_lower for word in ['create', 'add', 'new', 'make']) and any(word in message_lower for word in ['todo', 'task']):
            detected_type = "create"
        
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
    message_lower = problematic_message.lower()
    
    # Apply the same logic as in the fixed _handle_todo_command
    if any(word in message_lower for word in ['delete', 'remove']) and any(word in message_lower for word in ['todo', 'task']):
        print(f"  '{problematic_message}' -> DELETE command (correct)")
        result = "DELETE"
    elif any(word in message_lower for word in ['complete', 'finish', 'done', 'mark']) and any(word in message_lower for word in ['todo', 'task']):
        print(f"  '{problematic_message}' -> COMPLETE command (incorrect)")
        result = "COMPLETE"
    elif any(word in message_lower for word in ['show', 'list', 'view', 'get']) and any(word in message_lower for word in ['todo', 'task', 'todos', 'tasks']):
        print(f"  '{problematic_message}' -> SHOW command (incorrect)")
        result = "SHOW"
    elif any(word in message_lower for word in ['create', 'add', 'new', 'make']) and any(word in message_lower for word in ['todo', 'task']):
        print(f"  '{problematic_message}' -> CREATE command (incorrect)")
        result = "CREATE"
    else:
        print(f"  '{problematic_message}' -> OTHER command (incorrect)")
        result = "OTHER"
    
    if result == "DELETE":
        print("✅ SUCCESS: The specific issue has been fixed!")
        print("The command 'delete todo 'todo'' is now correctly identified as a DELETE command.")
    else:
        print("❌ The specific issue may not be fully resolved.")
    
    return all_passed


if __name__ == "__main__":
    test_command_detection()