#!/usr/bin/env python3
"""
Simple test to check if the chat API endpoint is working properly.
"""

import requests
import json

def test_api_endpoints():
    """Test the API endpoints to see if they're working."""
    print("Testing API endpoints...")
    
    # Assuming the backend is running on port 7860
    base_url = "http://localhost:7860"
    
    # First, let's try to register a test user
    print("\n1. Testing user signup...")
    signup_data = {
        "email": "test_chat@example.com",
        "password": "Testpassword123!"
    }
    
    try:
        signup_resp = requests.post(f"{base_url}/auth/signup", json=signup_data)
        print(f"Signup status: {signup_resp.status_code}")
        if signup_resp.status_code != 201:
            print(f"Signup response: {signup_resp.text}")
        
        # Now try to login
        print("\n2. Testing user signin...")
        signin_data = {
            "email": "test_chat@example.com",
            "password": "Testpassword123!"
        }
        
        signin_resp = requests.post(f"{base_url}/auth/signin", json=signin_data)
        print(f"Signin status: {signin_resp.status_code}")
        if signin_resp.status_code == 200:
            token_data = signin_resp.json()
            session_data = token_data.get("session", {})
            access_token = session_data.get("token")
            print(f"Access token received: {access_token is not None}")
            
            if not access_token:
                # Try alternative structures
                access_token = session_data.get("accessToken")
                print(f"Alternative access token (accessToken): {access_token is not None}")
                
                if not access_token:
                    access_token = token_data.get("access_token")
                    print(f"Alternative access token (access_token): {access_token is not None}")
            
            # Now test the chat todo-operation endpoint
            print("\n3. Testing chat todo-operation endpoint...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            chat_payload = {
                "message": "Create a new todo: Test task from chat"
            }
            
            chat_resp = requests.post(f"{base_url}/chat/todo-operation", json=chat_payload, headers=headers)
            print(f"Chat endpoint status: {chat_resp.status_code}")
            print(f"Chat response: {chat_resp.text}")
            
            # Test getting todos
            print("\n4. Testing get todos endpoint...")
            todos_resp = requests.get(f"{base_url}/todos", headers=headers)
            print(f"Get todos status: {todos_resp.status_code}")
            if todos_resp.status_code == 200:
                todos_data = todos_resp.json()
                print(f"Number of todos returned: {len(todos_data)}")
                for todo in todos_data:
                    print(f"  - {todo.get('title', 'No title')} (ID: {todo.get('id', 'No ID')})")
            else:
                print(f"Get todos response: {todos_resp.text}")
                
        else:
            print(f"Signin response: {signin_resp.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to the backend API. Is it running on http://localhost:7860?")
        print("Please start the backend server with: cd backend && python app.py")
        return False
    except Exception as e:
        print(f"Error during API test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    print("Testing API endpoints for chat widget integration...")
    success = test_api_endpoints()
    
    if success:
        print("\nAPI endpoint test completed")
    else:
        print("\nAPI endpoint test failed")

if __name__ == "__main__":
    main()