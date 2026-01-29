import requests
import os

# Test the new endpoint
def test_todo_operation_endpoint():
    # Get the API URL from environment or use default
    api_url = os.getenv("API_URL", "http://localhost:8000")
    todo_op_endpoint = f"{api_url}/chat/todo-operation"

    # Sample request data - this would need a valid auth token in practice
    sample_request = {
        "message": "Hello, how are you?"
    }

    # Headers (would normally include auth token)
    headers = {
        "Content-Type": "application/json"
    }

    print(f"Testing endpoint: {todo_op_endpoint}")
    print(f"Request: {sample_request}")

    try:
        response = requests.post(todo_op_endpoint, json=sample_request, headers=headers, timeout=30)
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ Endpoint is working correctly!")
            return True
        elif response.status_code in [401, 422]:  # Unauthorized or validation error
            print(f"⚠ Expected response for missing auth/validation: {response.status_code}")
            return True
        else:
            print(f"✗ Unexpected response: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to API at {todo_op_endpoint}")
        print("Make sure the backend server is running")
        return False
    except Exception as e:
        print(f"✗ Request failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_todo_operation_endpoint()