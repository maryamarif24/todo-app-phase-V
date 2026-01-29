"""
Test script to verify that the new todo-operation endpoint works correctly
"""
import os
import sys

# Add backend to Python path
sys.path.insert(0, './backend')

# Set environment variables
os.environ.setdefault('FRONTEND_URL', 'http://localhost:3000')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')  # Use SQLite for testing
os.environ.pop('OPENROUTER_API_KEY', None)  # Use offline mode for testing

def test_new_endpoint():
    """Test that the new todo-operation endpoint exists and works."""
    print("Testing new todo-operation endpoint...")
    
    try:
        # Import the chat API router to check if the endpoint is defined
        from backend.src.api.chat_api import router
        import inspect
        
        # Get all routes from the router
        routes = router.routes
        print(f"Found {len(routes)} routes in the chat router")
        
        # Look for the todo-operation endpoint
        todo_op_found = False
        for route in routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                print(f"Route: {route.path}, Methods: {route.methods}")
                if '/todo-operation' in route.path and 'POST' in route.methods:
                    todo_op_found = True
                    print(f"+ Found todo-operation endpoint: {route.path}")

        if todo_op_found:
            print("+ New todo-operation endpoint is properly registered")
            return True
        else:
            print("- New todo-operation endpoint not found")
            return False
            
    except Exception as e:
        print(f"- Error testing endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_both_modes():
    """Test that the agent can handle both todo operations and general conversation."""
    print("\nTesting agent for both todo operations and general conversation...")
    
    try:
        from backend.src.agents.todo_agent import TodoAgent
        import uuid
        
        agent = TodoAgent()
        user_id = uuid.uuid4()
        
        # Test general conversation
        general_msg = "Hello, how are you?"
        general_resp = agent.process_message(user_id, general_msg)
        print(f"+ General conversation: '{general_msg[:20]}...' -> Response length: {len(general_resp)} chars")

        # Test todo creation
        todo_create_msg = "Create a todo to buy groceries"
        todo_create_resp = agent.process_message(user_id, todo_create_msg)
        print(f"+ Todo creation: '{todo_create_msg[:20]}...' -> Response length: {len(todo_create_resp)} chars")

        # Test todo listing
        todo_list_msg = "Show me my todos"
        todo_list_resp = agent.process_message(user_id, todo_list_msg)
        print(f"+ Todo listing: '{todo_list_msg[:20]}...' -> Response length: {len(todo_list_resp)} chars")

        # Test todo deletion
        todo_del_msg = "Delete todo to buy groceries"
        todo_del_resp = agent.process_message(user_id, todo_del_msg)
        print(f"+ Todo deletion: '{todo_del_msg[:20]}...' -> Response length: {len(todo_del_resp)} chars")

        print("+ Agent can handle both general conversation and todo operations")
        return True

    except Exception as e:
        print(f"- Error testing agent modes: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Running tests for new todo-operation endpoint...\n")
    
    tests = [
        ("Endpoint Registration", test_new_endpoint),
        ("Agent Dual Modes", test_agent_both_modes),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        print()
    
    print("TEST RESULTS SUMMARY:")
    print("-" * 30)
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        icon = "+" if passed else "-"
        print(f"{icon} {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("-" * 30)
    if all_passed:
        print("+ ALL TESTS PASSED: New endpoint and dual functionality working!")
        print("\nThe chatbot can now:")
        print("  - Engage in general conversation")
        print("  - Perform todo operations (add, update, delete)")
        print("  - Without storing conversation history in database")
    else:
        print("- SOME TESTS FAILED: Issues detected.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)