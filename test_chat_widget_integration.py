#!/usr/bin/env python3
"""
Test script to verify that the chat widget integration with the dashboard is working properly.
This script will test the todo creation via the chat API endpoint and verify it appears in the todos API.
"""

import os
import sys
from pathlib import Path
import uuid
from datetime import datetime
import requests

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_chat_widget_integration():
    """Test the integration between chat widget and dashboard."""
    print("Testing chat widget integration with dashboard...")

    # Load environment variables
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    from dotenv import load_dotenv
    load_dotenv()

    try:
        from backend.src.models.database import sync_engine
        from sqlalchemy import inspect, text
        from backend.src.models.entities import User, Todo
        from backend.src.api.auth import pwd_context
        import json

        with sync_engine.connect() as conn:
            trans = conn.begin()
            
            # Create a test user
            test_user_id = uuid.uuid4()
            hashed_password = pwd_context.hash("testpassword")
            conn.execute(text("""
                INSERT INTO users (id, email, password_hash, created_at, updated_at) 
                VALUES (:user_id, :email, :password_hash, :created_at, :updated_at)
            """), {
                "user_id": test_user_id,
                "email": "test_chat_integration@example.com",
                "password_hash": hashed_password,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })

            # Get the current count of todos for this user
            result = conn.execute(text("SELECT COUNT(*) FROM todo WHERE user_id = :user_id"), {"user_id": test_user_id})
            initial_count = result.fetchone()[0]
            print(f"Initial todo count for user: {initial_count}")

            # Now test the chat API endpoint to create a todo
            # We'll need to simulate the backend API call directly
            from backend.src.main import app
            from fastapi.testclient import TestClient
            
            client = TestClient(app)
            
            # First, authenticate to get a token (we'll simulate this)
            login_data = {
                "username": "test_chat_integration@example.com",
                "password": "testpassword"
            }
            
            login_response = client.post("/auth/login", data=login_data)
            if login_response.status_code != 200:
                print(f"Login failed: {login_response.json()}")
                return False
                
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                print("No access token received from login")
                return False
                
            print("Successfully authenticated")
            
            # Now test the chat todo-operation endpoint
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            chat_payload = {
                "message": "Create a new todo: Buy groceries"
            }
            
            print("Sending chat message to create todo...")
            chat_response = client.post("/chat/todo-operation", json=chat_payload, headers=headers)
            
            print(f"Chat response status: {chat_response.status_code}")
            if chat_response.status_code != 200:
                print(f"Chat API error: {chat_response.json()}")
                return False
            
            response_data = chat_response.json()
            print(f"Chat response: {response_data}")
            
            # Check if the todo was created in the database
            result = conn.execute(text("SELECT COUNT(*) FROM todo WHERE user_id = :user_id"), {"user_id": test_user_id})
            final_count = result.fetchone()[0]
            print(f"Final todo count for user: {final_count}")
            
            if final_count > initial_count:
                print("✓ Todo was successfully created in the database")
                
                # Get the newly created todo to verify its content
                new_todos = conn.execute(text("SELECT * FROM todo WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 1"), 
                                        {"user_id": test_user_id}).fetchall()
                if new_todos:
                    new_todo = new_todos[0]
                    print(f"New todo created: {new_todo.title}")
                    
                    # Now test the GET /todos endpoint to see if it's returned
                    todos_response = client.get("/todos", headers=headers)
                    if todos_response.status_code == 200:
                        todos_data = todos_response.json()
                        print(f"Retrieved {len(todos_data)} todos from /todos endpoint")
                        
                        # Check if our new todo is in the response
                        todo_found = False
                        for todo in todos_data:
                            if todo.get('title') == new_todo.title:
                                todo_found = True
                                print(f"✓ Todo found in /todos endpoint response: {todo.get('title')}")
                                break
                        
                        if not todo_found:
                            print("✗ New todo was not found in the /todos endpoint response")
                            print("Available todos:", [t.get('title') if isinstance(t, dict) else getattr(t, 'title', 'unknown') for t in todos_data])
                            
                    else:
                        print(f"Failed to get todos: {todos_response.status_code}, {todos_response.json()}")
                        
            else:
                print("✗ Todo was not created in the database")
                
            # Clean up
            conn.execute(text("DELETE FROM todo WHERE user_id = :user_id"), {"user_id": test_user_id})
            conn.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": test_user_id})
            
            trans.commit()
            print("✓ Integration test completed")
            
            return True

    except Exception as e:
        print(f"  [ERROR] Integration test failed: {str(e)}")
        import traceback
        print(f"  [DEBUG] Full traceback: {traceback.format_exc()}")
        return False

def main():
    """Run the integration test."""
    print("[INFO] Starting Chat Widget Integration Test...\n")

    success = test_chat_widget_integration()

    if success:
        print(f"\n[SUCCESS] Chat widget integration test completed successfully!")
        print("The chat widget should be able to create todos that appear in the dashboard.")
    else:
        print(f"\n[ERROR] Chat widget integration test failed!")

if __name__ == "__main__":
    main()