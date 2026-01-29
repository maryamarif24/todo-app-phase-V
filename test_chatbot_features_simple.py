import os
import sys
import uuid
from unittest.mock import Mock, patch

# Add backend to Python path
sys.path.insert(0, './backend')

# Set environment variables to avoid warnings
os.environ.setdefault('FRONTEND_URL', 'http://localhost:3000')
os.environ.pop('OPENROUTER_API_KEY', None)  # Remove any existing API key to trigger offline mode

from backend.src.agents.todo_agent import TodoAgent

def test_todo_agent_with_mocked_services():
    print("Testing TodoAgent with mocked database services...")
    
    try:
        # Create a TodoAgent instance
        agent = TodoAgent()
        print(f"TodoAgent created. Offline mode: {agent.offline_mode}")
        
        # Mock the database functions
        with patch('backend.src.agents.todo_agent.get_todos_by_user') as mock_get_todos, \
             patch('backend.src.agents.todo_agent.create_todo') as mock_create_todo, \
             patch('backend.src.agents.todo_agent.update_todo') as mock_update_todo, \
             patch('backend.src.agents.todo_agent.delete_todo') as mock_delete_todo, \
             patch('backend.src.agents.todo_agent.toggle_todo_complete') as mock_toggle_complete, \
             patch('backend.src.agents.todo_agent.get_todo_by_title') as mock_get_by_title, \
             patch('backend.src.agents.todo_agent.get_todo_by_id') as mock_get_by_id:
            
            # Create mock todo objects
            mock_todo = Mock()
            mock_todo.id = uuid.uuid4()
            mock_todo.user_id = uuid.uuid4()
            mock_todo.title = "buy groceries"
            mock_todo.is_complete = False
            mock_todo.description = None
            
            # Configure mocks
            mock_get_todos.return_value = [mock_todo]
            mock_create_todo.return_value = mock_todo
            mock_get_by_title.return_value = mock_todo
            mock_get_by_id.return_value = mock_todo
            mock_toggle_complete.return_value = mock_todo
            mock_delete_todo.return_value = True
            mock_update_todo.return_value = mock_todo
            
            user_id = mock_todo.user_id  # Use the same user ID as the mock todo
            
            # Test creating a todo
            create_message = "Create a todo to buy groceries"
            print(f"\nProcessing create todo message: {create_message}")
            response = agent.process_message(user_id, create_message)
            print(f"Create todo response: {response}")
            assert "[SUCCESS] Successfully created todo" in response
            
            # Test listing todos
            list_message = "Show me my todos"
            print(f"\nProcessing list todos message: {list_message}")
            response = agent.process_message(user_id, list_message)
            print(f"List todos response: {response}")
            assert "Here are your todos:" in response
            
            # Test completing a todo
            complete_message = "Mark todo to buy groceries as complete"
            print(f"\nProcessing complete todo message: {complete_message}")
            response = agent.process_message(user_id, complete_message)
            print(f"Complete todo response: {response}")
            assert "[SUCCESS] Todo" in response and ("completed" in response or "marked as incomplete" in response)
            
            # Test deleting a todo
            delete_message = "Delete todo to buy groceries"
            print(f"\nProcessing delete todo message: {delete_message}")
            response = agent.process_message(user_id, delete_message)
            print(f"Delete todo response: {response}")
            assert "[SUCCESS] Todo" in response and "deleted successfully" in response
            
            print("\nAll mocked tests passed!")
            return True
            
    except Exception as e:
        print(f"Error in TodoAgent with mocked services: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

def test_todo_agent_commands():
    print("\n\nTesting various todo commands...")
    
    try:
        # Create a TodoAgent instance
        agent = TodoAgent()
        user_id = uuid.uuid4()
        
        # Test various commands
        commands = [
            "Create a todo to walk the dog",
            "Add a todo to finish homework",
            "Make a new todo to call mom",
            "Show me my todos",
            "List all my tasks",
            "View my todos",
            "Get my tasks",
            "Mark todo to walk the dog as complete",
            "Complete the todo to finish homework",
            "Finish the task to call mom",
            "Delete todo to walk the dog",
            "Remove the todo to finish homework"
        ]
        
        for cmd in commands:
            print(f"\nTesting command: {cmd}")
            response = agent.process_message(user_id, cmd)
            print(f"Response: {response}")
        
        return True
    except Exception as e:
        print(f"Error in command testing: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running comprehensive tests for TodoAgent functionality...")
    
    # Run tests with mocked services
    mock_success = test_todo_agent_with_mocked_services()
    
    # Run command tests
    command_success = test_todo_agent_commands()
    
    if mock_success and command_success:
        print("\n[SUCCESS] All tests PASSED: TodoAgent functionality works correctly!")
        print("\nThe chatbot can now:")
        print("- Create new todos with commands like 'Create a todo to buy groceries'")
        print("- List all todos with commands like 'Show me my todos'")
        print("- Mark todos as complete with commands like 'Mark todo to buy groceries as complete'")
        print("- Delete todos with commands like 'Delete todo to buy groceries'")
        print("\nUsers can interact with the chatbot using natural language!")
    else:
        print("\n[FAILURE] Some tests FAILED: TodoAgent has issues!")