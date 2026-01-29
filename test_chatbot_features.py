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

def test_todo_agent_basic_functionality():
    print("Testing TodoAgent basic functionality...")
    
    try:
        # Create a TodoAgent instance
        agent = TodoAgent()
        print(f"TodoAgent created. Offline mode: {agent.offline_mode}")
        
        # Test processing a general message
        user_id = uuid.uuid4()
        message = "Hello, how are you?"
        
        print(f"Processing general message: {message}")
        response = agent.process_message(user_id, message)
        print(f"General response received: {response[:100]}...")  # Print first 100 chars
        
        # Test processing a create todo message
        create_message = "Create a todo to buy groceries"
        print(f"\nProcessing create todo message: {create_message}")
        response = agent.process_message(user_id, create_message)
        print(f"Create todo response received: {response}")
        
        # Test processing a list todos message
        list_message = "Show me my todos"
        print(f"\nProcessing list todos message: {list_message}")
        response = agent.process_message(user_id, list_message)
        print(f"List todos response received: {response}")
        
        # Test processing a delete todo message
        delete_message = "Delete a todo to buy groceries"
        print(f"\nProcessing delete todo message: {delete_message}")
        response = agent.process_message(user_id, delete_message)
        print(f"Delete todo response received: {response}")
        
        # Test processing a complete todo message
        complete_message = "Mark todo to buy groceries as complete"
        print(f"\nProcessing complete todo message: {complete_message}")
        response = agent.process_message(user_id, complete_message)
        print(f"Complete todo response received: {response}")
        
        return True
    except Exception as e:
        print(f"Error in TodoAgent: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

def test_todo_agent_with_mocked_services():
    print("\n\nTesting TodoAgent with mocked database services...")
    
    try:
        # Create a TodoAgent instance
        agent = TodoAgent()
        print(f"TodoAgent created. Offline mode: {agent.offline_mode}")
        
        # Mock the database functions
        with patch('backend.src.agents.todo_agent.get_todos_by_user') as mock_get_todos, \
             patch('backend.src.agents.todo_agent.create_todo') as mock_create_todo, \
             patch('backend.src.agents.todo_agent.delete_todo') as mock_delete_todo, \
             patch('backend.src.agents.todo_agent.toggle_todo_complete') as mock_toggle_complete, \
             patch('backend.src.agents.todo_agent.get_todo_by_title') as mock_get_by_title, \
             patch('backend.src.agents.todo_agent.get_todo_by_id') as mock_get_by_id, \
             patch('backend.src.agents.todo_agent.get_db') as mock_get_db:
            
            # Create mock todo objects
            mock_todo = Mock()
            mock_todo.id = uuid.uuid4()
            mock_todo.title = "buy groceries"
            mock_todo.is_complete = False
            
            # Configure mocks
            mock_get_todos.return_value = [mock_todo]
            mock_create_todo.return_value = mock_todo
            mock_get_by_title.return_value = mock_todo
            mock_get_by_id.return_value = mock_todo
            mock_toggle_complete.return_value = mock_todo
            mock_delete_todo.return_value = True
            
            # Mock the generator function to return a mock session
            mock_session = Mock()
            mock_get_db.return_value = iter([mock_session])
            
            user_id = uuid.uuid4()
            
            # Test creating a todo
            create_message = "Create a todo to buy groceries"
            print(f"\nProcessing create todo message: {create_message}")
            response = agent.process_message(user_id, create_message)
            print(f"Create todo response: {response}")
            assert "Successfully created todo" in response
            
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
            assert "has been completed" in response or "marked as incomplete" in response
            
            # Test deleting a todo
            delete_message = "Delete todo to buy groceries"
            print(f"\nProcessing delete todo message: {delete_message}")
            response = agent.process_message(user_id, delete_message)
            print(f"Delete todo response: {response}")
            assert "has been deleted successfully" in response
            
            print("\nAll mocked tests passed!")
            return True
            
    except Exception as e:
        print(f"Error in TodoAgent with mocked services: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running comprehensive tests for TodoAgent functionality...")
    
    # Run basic functionality test
    basic_success = test_todo_agent_basic_functionality()
    
    # Run tests with mocked services
    mock_success = test_todo_agent_with_mocked_services()
    
    if basic_success and mock_success:
        print("\n✓ All tests PASSED: TodoAgent functionality works correctly!")
        print("\nThe chatbot can now:")
        print("- Create new todos with commands like 'Create a todo to buy groceries'")
        print("- List all todos with commands like 'Show me my todos'")
        print("- Mark todos as complete with commands like 'Mark todo to buy groceries as complete'")
        print("- Delete todos with commands like 'Delete todo to buy groceries'")
    else:
        print("\n✗ Some tests FAILED: TodoAgent has issues!")