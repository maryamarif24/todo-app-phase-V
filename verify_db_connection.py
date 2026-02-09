#!/usr/bin/env python3
"""
Verification script to check database connection and user existence in the backend.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def verify_database_and_users():
    """Verify database connection and check for users."""
    print("Verifying database connection and users...")

    # Change to backend directory to load .env
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    try:
        from backend.src.models.database import sync_engine
        from sqlalchemy import text
        from sqlalchemy.exc import SQLAlchemyError

        print("Attempting to connect to the database...")
        
        with sync_engine.connect() as conn:
            print("[SUCCESS] Successfully connected to database")
            
            # Check if users table exists
            from sqlalchemy import inspect
            inspector = inspect(sync_engine)
            tables = inspector.get_table_names()
            print(f"Tables in database: {tables}")
            
            if 'users' not in tables:
                print("[ERROR] 'users' table does not exist in database!")
                return False
            else:
                print("[SUCCESS] 'users' table exists")
            
            # Count total users
            result = conn.execute(text("SELECT COUNT(*) FROM users")).fetchone()
            total_users = result[0]
            print(f"Total users in database: {total_users}")
            
            # If there are users, show a few examples
            if total_users > 0:
                sample_users = conn.execute(text("SELECT id, email FROM users LIMIT 10")).fetchall()
                print("Sample users in database:")
                for user in sample_users:
                    print(f"  - ID: {user.id}, Email: {user.email}")
            
            # Check for a specific test user
            test_emails = [
                "test_chat@example.com",
                "test@example.com",
                "admin@example.com"
            ]
            
            for email in test_emails:
                result = conn.execute(text("SELECT id, email FROM users WHERE email = :email"), 
                                    {"email": email}).fetchone()
                if result:
                    print(f"[SUCCESS] Found user: {result.email} (ID: {result.id})")
                    return True
            
            print("[INFO] No common test users found in database")
            print("You may need to create a new user account in this database.")
            return True

    except SQLAlchemyError as e:
        print(f"  [ERROR] Database connection failed: {str(e)}")
        return False
    except Exception as e:
        print(f"  [ERROR] Verification failed: {str(e)}")
        import traceback
        print(f"  [DEBUG] Full traceback: {traceback.format_exc()}")
        return False

def main():
    """Run the verification."""
    print("[INFO] Verifying database connection and users...\n")

    success = verify_database_and_users()

    if success:
        print(f"\n[SUCCESS] Database verification completed!")
        print("If users exist, authentication should work.")
        print("If no users exist, you'll need to create an account first.")
    else:
        print(f"\n[ERROR] Database verification failed!")

if __name__ == "__main__":
    main()