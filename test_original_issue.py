#!/usr/bin/env python3
"""
Test script to verify that the original issue is fixed.
This simulates the INSERT that was failing before.
"""

import os
import sys
from pathlib import Path
import uuid
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_insert_todo():
    """Test inserting a todo with all the required fields."""
    print("Testing INSERT with all required fields...")

    # Change to backend directory to load .env
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    try:
        from backend.src.models.database import sync_engine
        from sqlalchemy import text

        with sync_engine.connect() as conn:
            # Create a test user first
            user_id = uuid.uuid4()
            conn.execute(text("""
                INSERT INTO users (id, email, password_hash, created_at, updated_at) 
                VALUES (:user_id, :email, :password_hash, :created_at, :updated_at)
            """), {
                "user_id": user_id,
                "email": "test_chatbot@example.com",
                "password_hash": "hashed_password_for_test",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })

            # Now test the INSERT that was failing before
            todo_id = uuid.uuid4()
            result = conn.execute(text("""
                INSERT INTO todo (id, user_id, title, description, is_complete, created_at, updated_at, completed_at, priority, due_date, reminder_enabled, reminder_time) 
                VALUES (:id, :user_id, :title, :description, :is_complete, :created_at, :updated_at, :completed_at, :priority, :due_date, :reminder_enabled, :reminder_time)
            """), {
                'id': todo_id,
                'user_id': user_id,
                'title': 'hi',
                'description': None,
                'is_complete': False,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'completed_at': None,
                'priority': 'MEDIUM',
                'due_date': None,
                'reminder_enabled': False,
                'reminder_time': None
            })

            print(f"  [SUCCESS] Successfully inserted todo with ID: {todo_id}")
            
            # Verify the todo was inserted
            verify_result = conn.execute(text("SELECT * FROM todo WHERE id = :todo_id"), {"todo_id": todo_id}).fetchone()
            if verify_result:
                print(f"  [SUCCESS] Todo verified in database: {verify_result.title}")
            else:
                print("  [ERROR] Todo not found in database after insertion")
                
            # Clean up test data
            conn.execute(text("DELETE FROM todo WHERE user_id = :user_id"), {"user_id": user_id})
            conn.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": user_id})
            
            print("  [SUCCESS] Test cleanup completed")
            
        return True

    except Exception as e:
        print(f"  [ERROR] Test failed: {str(e)}")
        import traceback
        print(f"  [DEBUG] Full traceback: {traceback.format_exc()}")
        return False

def main():
    """Run the test."""
    print("[INFO] Starting Test for Original Issue Fix...\n")

    success = test_insert_todo()

    if success:
        print(f"\n[SUCCESS] The original issue has been fixed!")
        print("The todo table now has all required columns and INSERT operations work correctly.")
        print("Chatbot should now be able to create todos without the 'column does not exist' error.")
    else:
        print(f"\n[ERROR] Test failed!")

if __name__ == "__main__":
    main()